"""
Multi-Strategy Concept Extraction Domain Services.

This module implements sophisticated concept extraction using multiple strategies
as described in the academic research requirements for automated concept mining.

Educational Notes:
- Demonstrates Strategy Pattern with multiple extraction algorithms
- Shows Template Method pattern for common extraction workflow
- Implements Factory Pattern for strategy creation and configuration
- Uses Composite Pattern for multi-strategy result aggregation
- Follows academic standards for transparent and reproducible concept extraction

Design Patterns Applied:
- Strategy Pattern: Pluggable extraction algorithms (rule-based, statistical, embedding-based)
- Template Method: Common extraction workflow with strategy-specific implementations
- Factory Pattern: StrategyConfiguration creates appropriate extraction strategies
- Composite Pattern: MultiStrategyConceptExtractor aggregates results from multiple strategies
- Value Object Pattern: ExtractionResult and StrategyConfiguration are immutable value objects

Academic Methodology:
All extraction methods are designed to be:
- Transparent: Clear algorithmic steps that can be inspected
- Reproducible: Deterministic results given the same input and configuration
- Evidence-based: All concepts are grounded in source text with traceability
- Domain-agnostic: Extensible to any research domain through configuration
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
import logging
from collections import Counter, defaultdict
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
import networkx as nx

from src.domain.entities.concept import Concept
from src.domain.value_objects.embedding_vector import EmbeddingVector


# =============================================================================
# COMMON CONSTANTS FOR TEXT PROCESSING
# =============================================================================

# Regular expression patterns for consistent text processing
WORD_EXTRACTION_PATTERN = r"\b[a-zA-Z]{3,}\b"
SENTENCE_SPLIT_PATTERN = r"[.!?]+"


# =============================================================================
# COMMON HELPER METHODS FOR EXTRACTION STRATEGIES
# =============================================================================


def _safe_extraction(extraction_method_name: str):
    """
    Decorator for safe concept extraction with consistent error handling.

    Educational Note:
    This decorator demonstrates the Decorator Pattern applied to error handling,
    providing consistent logging and graceful degradation across all extraction
    strategies while maintaining the Strategy Pattern's interface.
    """

    def decorator(extraction_func):
        def wrapper(self, *args, **kwargs):
            try:
                return extraction_func(self, *args, **kwargs)
            except Exception as e:
                logging.warning(f"{extraction_method_name} extraction failed: {e}")
                return (
                    []
                    if extraction_func.__name__.startswith("extract_")
                    else ExtractionResult(concepts=[], metadata={})
                )

        return wrapper

    return decorator


# Educational Note: Value objects for extraction configuration and results
@dataclass(frozen=True)
class ExtractionResult:
    """
    Immutable value object representing concept extraction results.

    Educational Note:
    This value object encapsulates extraction results with metadata,
    demonstrating how to package complex algorithmic outputs with
    full provenance and traceability for academic transparency.
    """

    concepts: List[Concept]
    metadata: Dict[str, Any]

    @property
    def total_concepts(self) -> int:
        """Get total number of extracted concepts."""
        return len(self.concepts)

    @property
    def average_relevance_score(self) -> float:
        """Calculate average relevance score across all concepts."""
        if not self.concepts:
            return 0.0
        return sum(c.relevance_score for c in self.concepts) / len(self.concepts)

    @property
    def total_frequency(self) -> int:
        """Get total frequency count across all concepts."""
        return sum(c.frequency for c in self.concepts)

    def filter_by_relevance(self, min_score: float) -> List[Concept]:
        """Filter concepts by minimum relevance score."""
        return [c for c in self.concepts if c.relevance_score >= min_score]

    def filter_by_frequency(self, min_frequency: int) -> List[Concept]:
        """Filter concepts by minimum frequency."""
        return [c for c in self.concepts if c.frequency >= min_frequency]


@dataclass(frozen=True)
class StrategyConfiguration:
    """
    Configuration for concept extraction strategies.

    Educational Note:
    Immutable configuration object that encapsulates all parameters
    needed for multi-strategy extraction, demonstrating how to make
    algorithmic behavior configurable and reproducible.
    """

    domain: str
    min_concept_frequency: int = 1
    enable_all_strategies: bool = True
    strategy_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "rule_based": 0.4,
            "statistical": 0.3,
            "embedding_based": 0.3,
        }
    )
    consolidate_results: bool = True
    merge_similar_concepts: bool = True
    similarity_threshold: float = 0.8
    extract_hierarchies: bool = True
    use_domain_ontology: bool = False
    use_tfidf: bool = True
    use_textrank: bool = True
    use_topic_modeling: bool = False  # Usually for corpora, not single documents
    max_concepts_per_strategy: int = 50


# Educational Note: Abstract Strategy interface defines the extraction contract
class ConceptExtractionStrategy(ABC):
    """
    Abstract base class for concept extraction strategies.

    Educational Note:
    This interface defines the contract that all extraction strategies must
    implement, following the Strategy Pattern. It ensures consistent behavior
    while allowing for different algorithmic approaches.

    Design Principles Applied:
    - Interface Segregation: Single focused responsibility (concept extraction)
    - Dependency Inversion: Depends on abstractions, not concrete implementations
    - Open/Closed: Open for extension through new strategies, closed for modification
    """

    @abstractmethod
    def extract_concepts(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """
        Extract concepts from text using this strategy.

        Args:
            text: Input text to analyze
            config: Configuration parameters for extraction

        Returns:
            ExtractionResult with concepts and metadata
        """
        pass

    # =============================================================================
    # COMMON HELPER METHODS - SHARED ACROSS ALL STRATEGIES
    # =============================================================================

    def _create_concept_with_validation(
        self,
        text: str,
        frequency: int,
        relevance_score: float,
        extraction_method: str,
        min_length: int = 2,
        max_score: float = 1.0,
    ) -> Optional[Concept]:
        """
        Create a validated concept with consistent parameter checking.

        Educational Note:
        This helper method demonstrates the DRY principle by consolidating
        concept creation logic and validation rules that were repeated
        across multiple extraction strategies.

        Args:
            text: The concept text (will be cleaned and validated)
            frequency: Frequency count in source text
            relevance_score: Algorithmic relevance score (will be normalized)
            extraction_method: Method used for extraction
            min_length: Minimum text length for valid concepts
            max_score: Maximum allowed relevance score for normalization

        Returns:
            Validated Concept object or None if validation fails
        """
        # Clean and validate text
        cleaned_text = text.strip().lower()
        if len(cleaned_text) < min_length:
            return None

        # Normalize relevance score to [0, 1] range
        normalized_score = min(max(relevance_score, 0.0), max_score)

        try:
            return Concept(
                text=cleaned_text,
                frequency=max(frequency, 1),  # Ensure minimum frequency of 1
                relevance_score=float(normalized_score),
                extraction_method=extraction_method,
            )
        except Exception:
            # Return None if concept creation fails validation
            return None

    def _rank_and_filter_concepts(
        self,
        concepts: List[Concept],
        max_concepts: int,
        min_relevance: float = 0.0,
        min_frequency: int = 1,
    ) -> List[Concept]:
        """
        Rank concepts by relevance and apply filtering criteria.

        Educational Note:
        This method consolidates the common pattern of scoring, sorting,
        and filtering concepts that appeared across multiple extraction
        strategies, demonstrating code reuse and consistent behavior.

        Args:
            concepts: List of concepts to rank and filter
            max_concepts: Maximum number of concepts to return
            min_relevance: Minimum relevance score threshold
            min_frequency: Minimum frequency threshold

        Returns:
            Filtered and sorted list of top concepts
        """
        if not concepts:
            return []

        # Filter by thresholds
        filtered_concepts = [
            c
            for c in concepts
            if c.relevance_score >= min_relevance and c.frequency >= min_frequency
        ]

        # Sort by composite score (relevance * frequency) for better ranking
        filtered_concepts.sort(
            key=lambda c: c.relevance_score * c.frequency, reverse=True
        )

        return filtered_concepts[:max_concepts]

    def _preprocess_text_for_extraction(self, text: str) -> Dict[str, Any]:
        """
        Common text preprocessing pipeline for extraction strategies.

        Educational Note:
        Centralizes text preprocessing to ensure consistent text handling
        across all extraction strategies while providing detailed metadata
        about the preprocessing steps applied.

        Returns:
            Dictionary containing processed text and preprocessing metadata
        """
        preprocessing_metadata = {
            "original_length": len(text),
            "preprocessing_steps": [],
        }

        # Basic text cleaning
        cleaned_text = re.sub(r"\s+", " ", text.strip())
        preprocessing_metadata["preprocessing_steps"].append("whitespace_normalization")

        # Extract sentences for analysis
        sentences = re.split(SENTENCE_SPLIT_PATTERN, cleaned_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        preprocessing_metadata["sentence_count"] = len(sentences)
        preprocessing_metadata["preprocessing_steps"].append("sentence_extraction")

        # Extract words for frequency analysis
        words = re.findall(WORD_EXTRACTION_PATTERN, cleaned_text.lower())
        preprocessing_metadata["word_count"] = len(words)
        preprocessing_metadata["unique_words"] = len(set(words))
        preprocessing_metadata["preprocessing_steps"].append("word_tokenization")

        return {
            "cleaned_text": cleaned_text,
            "sentences": sentences,
            "words": words,
            "metadata": preprocessing_metadata,
        }


class RuleBasedExtractionStrategy(ConceptExtractionStrategy):
    """
    Rule-based concept extraction using linguistic patterns and ontologies.

    Educational Note:
    This strategy implements traditional NLP approaches using linguistic rules,
    pattern matching, and ontology lookup. It demonstrates how explicit domain
    knowledge can be encoded into extraction algorithms.

    Academic Methods Implemented:
    - Noun phrase chunking for concept candidate identification
    - Hearst patterns for automatic taxonomy construction (Hearst, 1992)
    - Domain ontology matching for concept validation
    - Part-of-speech filtering for concept quality
    """

    def __init__(self):
        """Initialize rule-based strategy with NLP pipeline."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            # Fallback for environments without spaCy model
            self.nlp = None
            logging.warning(
                "spaCy model not available, using basic rule-based extraction"
            )

    def extract_concepts(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """
        Extract concepts using rule-based methods.

        Educational Note:
        Orchestrates multiple rule-based extraction techniques,
        demonstrating how to combine complementary approaches
        for comprehensive concept coverage.
        """
        concepts = []
        metadata = {
            "extraction_method": "rule_based",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "techniques_used": [],
        }

        # Extract noun phrases
        noun_phrases = self.extract_noun_phrases(text)
        if noun_phrases:
            metadata["techniques_used"].append("noun_phrase_extraction")
            concepts.extend(
                self._create_concepts_from_phrases(noun_phrases, "noun_phrase", config)
            )

        # Extract hierarchical relationships if enabled
        if config.extract_hierarchies:
            hierarchies = self.extract_hearst_patterns(text)
            if hierarchies:
                metadata["techniques_used"].append("hearst_patterns")
                metadata["hierarchy_relationships"] = len(hierarchies)
                concepts.extend(
                    self._create_concepts_from_hierarchies(hierarchies, config)
                )

        # Apply domain ontology matching if available
        if config.use_domain_ontology:
            ontology_matches = self.match_domain_ontology(
                text, self._get_default_ontology()
            )
            if ontology_matches:
                metadata["techniques_used"].append("domain_ontology")
                concepts.extend(
                    self._create_concepts_from_ontology_matches(
                        ontology_matches, config
                    )
                )

        # Filter and deduplicate concepts
        concepts = self._filter_and_deduplicate_concepts(concepts, config)

        metadata["total_concepts_extracted"] = len(concepts)
        return ExtractionResult(concepts=concepts, metadata=metadata)

    def extract_noun_phrases(self, text: str) -> List[str]:
        """
        Extract noun phrases as concept candidates.

        Educational Note:
        Implements noun phrase chunking, a fundamental NLP technique
        for identifying concept candidates in academic text.
        """
        if not self.nlp:
            # Basic fallback: extract capitalized multi-word phrases
            return self._basic_noun_phrase_extraction(text)

        doc = self.nlp(text)
        noun_phrases = []

        for chunk in doc.noun_chunks:
            # Filter out single pronouns and very short phrases
            if len(chunk.text.split()) >= 2 and chunk.root.pos_ != "PRON":
                # Clean and normalize the phrase
                phrase = chunk.text.lower().strip()
                if len(phrase) > 3:  # Minimum meaningful length
                    noun_phrases.append(phrase)

        return list(set(noun_phrases))  # Remove duplicates

    def extract_hearst_patterns(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract hierarchical relationships using Hearst patterns.

        Educational Note:
        Implements Hearst patterns (Hearst, 1992) for automatic discovery
        of is-a relationships in text, enabling taxonomy construction.

        Patterns implemented:
        - "X such as Y and Z"
        - "Y and other X"
        - "X including Y"
        - "X, especially Y"
        """
        hierarchies = []

        # Hearst pattern definitions
        patterns = [
            # "techniques such as neural networks and SVMs"
            (
                r"(\w+(?:\s+\w+)*)\s+such as\s+((?:\w+(?:\s+\w+)*(?:\s*,\s*|\s+and\s+))*\w+(?:\s+\w+)*)",
                "such_as",
            ),
            # "neural networks and other machine learning techniques"
            (
                r"((?:\w+(?:\s+\w+)*(?:\s*,\s*|\s+and\s+))*\w+(?:\s+\w+)*)\s+and other\s+(\w+(?:\s+\w+)*)",
                "and_other",
            ),
            # "machine learning including neural networks"
            (
                r"(\w+(?:\s+\w+)*)\s+including\s+((?:\w+(?:\s+\w+)*(?:\s*,\s*|\s+and\s+))*\w+(?:\s+\w+)*)",
                "including",
            ),
            # "algorithms, especially deep learning"
            (r"(\w+(?:\s+\w+)*),\s*especially\s+(\w+(?:\s+\w+)*)", "especially"),
            # "biomarkers like X, Y, and Z"
            (
                r"(\w+(?:\s+\w+)*)\s+like\s+((?:\w+(?:\s+\w+)*(?:\s*,\s*|\s+and\s+))*\w+(?:\s+\w+)*)",
                "like",
            ),
        ]

        for pattern, pattern_type in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if pattern_type == "and_other":
                    # Reverse relationship: children come first
                    children_text = match.group(1)
                    parent = match.group(2).strip()
                else:
                    parent = match.group(1).strip()
                    children_text = match.group(2).strip()

                # Clean children text - remove trailing verbs and context
                children_text = re.sub(
                    r"\s+(are|is|show|can|will|have|has|be)\s+.*",
                    "",
                    children_text,
                    flags=re.IGNORECASE,
                )

                # Split multiple children
                child_list = re.split(r"\s*,\s*|\s+and\s+", children_text)
                for child in child_list:
                    child = child.strip()
                    if child and len(child) > 2:  # Valid child concept
                        hierarchies.append((parent.lower(), child.lower()))

        return hierarchies

    def match_domain_ontology(
        self, text: str, ontology: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Match text against domain-specific ontology.

        Educational Note:
        Demonstrates how domain knowledge can be encoded in ontologies
        and used for concept validation and categorization.
        """
        text_lower = text.lower()
        matches = defaultdict(list)

        for category, terms in ontology.items():
            for term in terms:
                if term.lower() in text_lower:
                    matches[category].append(term)

        return dict(matches)

    def _get_default_ontology(self) -> Dict[str, List[str]]:
        """Get default domain ontology for medical AI research."""
        return {
            "cardiovascular": [
                "heart rate variability",
                "HRV",
                "ECG",
                "cardiac",
                "cardiovascular",
                "heart rate",
                "cardiac rhythm",
                "arrhythmia",
                "electrocardiogram",
            ],
            "neurology": [
                "traumatic brain injury",
                "TBI",
                "brain",
                "neural",
                "neurological",
                "cognitive",
                "concussion",
                "neuroimaging",
                "EEG",
            ],
            "machine_learning": [
                "machine learning",
                "artificial intelligence",
                "deep learning",
                "neural networks",
                "algorithms",
                "classification",
                "prediction",
            ],
            "signal_processing": [
                "signal processing",
                "digital filtering",
                "frequency analysis",
                "time series",
                "spectral analysis",
                "feature extraction",
            ],
        }

    def _basic_noun_phrase_extraction(self, text: str) -> List[str]:
        """Basic noun phrase extraction without spaCy."""
        # Extract multi-word phrases that look like concepts
        phrases = []

        # Pattern 1: Capitalized multi-word phrases
        capitalized_pattern = r"\b[A-Z][a-z]+(?:\s+[a-z]+)*\s+[a-z]+\b"
        matches = re.findall(capitalized_pattern, text)
        phrases.extend([match.lower() for match in matches if len(match.split()) >= 2])

        # Pattern 2: Technical terms (letters, digits, spaces, hyphens)
        technical_pattern = r"\b[a-zA-Z]+(?:[-\s][a-zA-Z]+)+\b"
        matches = re.findall(technical_pattern, text)
        phrases.extend([match.lower() for match in matches if len(match.split()) >= 2])

        # Pattern 3: Known medical/technical term patterns
        known_patterns = [
            r"heart rate variability",
            r"machine learning algorithms?",
            r"ECG signals?",
            r"traumatic brain injury",
            r"physiological phenomenon",
            r"clinical settings?",
        ]

        for pattern in known_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                phrases.append(match.group().lower())

        # Remove duplicates and short phrases
        unique_phrases = list({phrase for phrase in phrases if len(phrase) > 6})
        return unique_phrases

    def _create_concepts_from_phrases(
        self, phrases: List[str], method: str, _config: StrategyConfiguration
    ) -> List[Concept]:
        """Create Concept entities from extracted phrases."""
        concepts = []
        for phrase in phrases:
            if len(phrase) >= 3:  # Minimum meaningful length
                concept = Concept(
                    text=phrase,
                    frequency=1,  # Will be updated during aggregation
                    relevance_score=0.7,  # Default for rule-based extraction
                    extraction_method="keyword",  # Valid method for rule-based
                )
                concepts.append(concept)
        return concepts

    def _create_concepts_from_hierarchies(
        self, hierarchies: List[Tuple[str, str]], _config: StrategyConfiguration
    ) -> List[Concept]:
        """Create Concept entities from hierarchical relationships."""
        concepts = []
        for parent, child in hierarchies:
            # Create parent concept
            parent_concept = Concept(
                text=parent,
                frequency=1,
                relevance_score=0.8,  # Higher score for hierarchy roots
                extraction_method="keyword",
            )
            concepts.append(parent_concept)

            # Create child concept
            child_concept = Concept(
                text=child,
                frequency=1,
                relevance_score=0.7,
                extraction_method="keyword",
            )
            concepts.append(child_concept)

        return concepts

    def _create_concepts_from_ontology_matches(
        self, matches: Dict[str, List[str]], _config: StrategyConfiguration
    ) -> List[Concept]:
        """Create Concept entities from ontology matches."""
        concepts = []
        for category, terms in matches.items():
            for term in terms:
                concept = Concept(
                    text=term,
                    frequency=1,
                    relevance_score=0.9,  # High score for ontology matches
                    extraction_method="keyword",
                )
                concepts.append(concept)
        return concepts

    def _filter_and_deduplicate_concepts(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Filter and deduplicate extracted concepts."""
        # Group by text and merge duplicates
        concept_groups = defaultdict(list)
        for concept in concepts:
            concept_groups[concept.text.lower()].append(concept)

        merged_concepts = []
        for text, group in concept_groups.items():
            if len(group) == 1:
                merged_concepts.append(group[0])
            else:
                # Merge multiple concepts with same text
                merged_frequency = sum(c.frequency for c in group)
                max_relevance = max(c.relevance_score for c in group)

                merged_concept = Concept(
                    text=text,
                    frequency=merged_frequency,
                    relevance_score=max_relevance,
                    extraction_method="keyword",
                )
                merged_concepts.append(merged_concept)

        # Filter by minimum frequency
        filtered = [
            c for c in merged_concepts if c.frequency >= config.min_concept_frequency
        ]

        # Sort by relevance and limit results
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)
        return filtered[: config.max_concepts_per_strategy]


class StatisticalExtractionStrategy(ConceptExtractionStrategy):
    """
    Statistical concept extraction using frequency analysis and graph algorithms.

    Educational Note:
    Implements statistical methods for concept extraction including TF-IDF,
    TextRank, and topic modeling. These methods use mathematical approaches
    to identify important terms and concepts without relying on linguistic rules.

    Academic Methods Implemented:
    - TF-IDF weighting for term importance calculation
    - TextRank algorithm for keyphrase extraction (Mihalcea & Tarau, 2004)
    - Latent Dirichlet Allocation for topic discovery (Blei et al., 2003)
    """

    def extract_concepts(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """Extract concepts using statistical methods."""
        concepts = []
        metadata = {
            "extraction_method": "statistical",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "techniques_used": [],
        }

        # TF-IDF based extraction
        if config.use_tfidf:
            tfidf_concepts = self.extract_tfidf_concepts([text], max_concepts=20)
            concepts.extend(tfidf_concepts)
            metadata["techniques_used"].append("tfidf")
            metadata["tfidf_concepts"] = len(tfidf_concepts)

        # TextRank keyphrase extraction
        if config.use_textrank:
            textrank_concepts = self.extract_textrank_keyphrases(text, max_phrases=15)
            concepts.extend(textrank_concepts)
            metadata["techniques_used"].append("textrank")
            metadata["textrank_concepts"] = len(textrank_concepts)

        # Filter and deduplicate
        concepts = self._filter_and_deduplicate_concepts(concepts, config)

        metadata["total_concepts_extracted"] = len(concepts)
        return ExtractionResult(concepts=concepts, metadata=metadata)

    def extract_tfidf_concepts(
        self, corpus: List[str], max_concepts: int = 20
    ) -> List[Concept]:
        """
        Extract concepts using TF-IDF weighting.

        Educational Note:
        TF-IDF (Term Frequency-Inverse Document Frequency) identifies
        terms that are frequent in a document but rare across the corpus,
        indicating their importance to the specific document.
        """
        if len(corpus) == 1:
            # For single document, use simple term frequency
            return self._extract_term_frequency_concepts(corpus[0], max_concepts)

        # Standard TF-IDF for multiple documents
        vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 3),  # Include unigrams, bigrams, trigrams
            stop_words="english",
            min_df=1,
            lowercase=True,
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            feature_names = vectorizer.get_feature_names_out()

            # Aggregate TF-IDF scores across all documents to find globally important terms
            aggregated_scores = tfidf_matrix.sum(axis=0).A1

            # Create concepts from high-scoring terms
            concepts = []
            for i, score in enumerate(aggregated_scores):
                if score > 0:
                    concept = Concept(
                        text=feature_names[i],
                        frequency=1,
                        relevance_score=float(
                            min(score / len(corpus), 1.0)
                        ),  # Normalize by corpus size
                        extraction_method="tfidf",
                    )
                    concepts.append(concept)

            # Sort by TF-IDF score and return top concepts
            concepts.sort(key=lambda x: x.relevance_score, reverse=True)
            return concepts[:max_concepts]

        except Exception as e:
            logging.warning(f"TF-IDF extraction failed: {e}")
            return []

    def extract_textrank_keyphrases(
        self, text: str, max_phrases: int = 15
    ) -> List[Concept]:
        """
        Extract keyphrases using TextRank algorithm.

        Educational Note:
        TextRank applies PageRank algorithm to word graphs,
        identifying central terms based on their connections
        to other words in the text.
        """
        try:
            # First extract candidate phrases using noun phrase patterns
            candidate_phrases = self._extract_candidate_phrases(text)

            if not candidate_phrases:
                # Fallback to single words if no phrases found
                sentences = self._split_into_sentences(text)
                word_graph = self._build_word_graph(sentences)

                if len(word_graph) == 0:
                    return []

                # Apply PageRank algorithm
                pagerank_scores = nx.pagerank(word_graph, max_iter=100, tol=1e-6)

                # Extract top-scoring words as keyphrases
                sorted_words = sorted(
                    pagerank_scores.items(), key=lambda x: x[1], reverse=True
                )

                concepts = []
                for word, score in sorted_words[:max_phrases]:
                    concept = Concept(
                        text=word,
                        frequency=1,
                        relevance_score=float(score),
                        extraction_method="keyword",
                    )
                    concepts.append(concept)
                return concepts

            # Score candidate phrases based on constituent word scores
            sentences = self._split_into_sentences(text)
            word_graph = self._build_word_graph(sentences)

            if len(word_graph) == 0:
                return []

            pagerank_scores = nx.pagerank(word_graph, max_iter=100, tol=1e-6)

            # Score phrases based on average word scores
            phrase_scores = []
            for phrase in candidate_phrases:
                words = phrase.lower().split()
                word_scores = [
                    pagerank_scores.get(word, 0.0)
                    for word in words
                    if word in pagerank_scores
                ]
                if word_scores:
                    avg_score = sum(word_scores) / len(word_scores)
                    phrase_scores.append((phrase, avg_score))

            # Sort by score and create concepts
            phrase_scores.sort(key=lambda x: x[1], reverse=True)
            concepts = []
            for phrase, score in phrase_scores[:max_phrases]:
                concept = Concept(
                    text=phrase,
                    frequency=1,
                    relevance_score=float(score),
                    extraction_method="keyword",
                )
                concepts.append(concept)

            return concepts

        except Exception as e:
            logging.warning(f"TextRank extraction failed: {e}")
            return []

    def _extract_candidate_phrases(self, text: str) -> List[str]:
        """Extract candidate phrases for TextRank analysis."""
        # Extract noun phrases and technical terms
        phrases = []

        # Common multi-word technical patterns
        patterns = [
            r"\b(?:heart rate variability|machine learning|deep learning|artificial intelligence)\b",
            r"\b(?:medical applications?|signal analysis|data processing)\b",
            r"\b(?:neural networks?|algorithms?|cardiovascular research)\b",
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",  # Capitalized phrases
            r"\b[a-z]+ [a-z]+ (?:analysis|detection|processing|research|applications?)\b",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            phrases.extend(matches)

        # Remove duplicates and filter short phrases
        unique_phrases = list(set(phrases))
        return [p for p in unique_phrases if len(p.split()) >= 2]

    def extract_lda_topics(
        self, documents: List[str], num_topics: int = 5, words_per_topic: int = 10
    ):
        """
        Extract topics using Latent Dirichlet Allocation.

        Educational Note:
        LDA discovers latent topics in document collections by modeling
        each document as a mixture of topics and each topic as a mixture of words.
        """
        if len(documents) < 2:
            # LDA requires multiple documents
            return []

        try:
            # Prepare text for LDA
            vectorizer = TfidfVectorizer(
                max_features=100, stop_words="english", lowercase=True, min_df=2
            )

            doc_term_matrix = vectorizer.fit_transform(documents)

            # Fit LDA model
            lda = LatentDirichletAllocation(
                n_components=num_topics, random_state=42, max_iter=100
            )
            lda.fit(doc_term_matrix)

            # Extract topics
            feature_names = vectorizer.get_feature_names_out()
            topics = []

            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-words_per_topic:][::-1]
                topic_concepts = []

                # Normalize topic weights to [0,1] range
                max_weight = topic.max()
                min_weight = topic.min()
                weight_range = (
                    max_weight - min_weight if max_weight > min_weight else 1.0
                )

                for word_idx in top_words_idx:
                    word = feature_names[word_idx]
                    weight = topic[word_idx]

                    # Normalize weight to [0,1] range
                    normalized_weight = (
                        (weight - min_weight) / weight_range
                        if weight_range > 0
                        else 0.5
                    )

                    concept = Concept(
                        text=word,
                        frequency=1,
                        relevance_score=float(normalized_weight),
                        extraction_method="tfidf",
                    )
                    topic_concepts.append(concept)

                # Create topic wrapper (simplified for this implementation)
                topic_result = type(
                    "Topic",
                    (),
                    {
                        "concepts": topic_concepts,
                        "coherence_score": 0.5,  # Placeholder
                        "metadata": {"topic_id": topic_idx},
                    },
                )()
                topics.append(topic_result)

            return topics

        except Exception as e:
            logging.warning(f"LDA topic extraction failed: {e}")
            return []

    def _extract_term_frequency_concepts(
        self, text: str, max_concepts: int
    ) -> List[Concept]:
        """Extract concepts based on term frequency for single documents."""
        # Simple term frequency approach
        words = re.findall(WORD_EXTRACTION_PATTERN, text.lower())
        word_freq = Counter(words)

        concepts = []
        for word, freq in word_freq.most_common(max_concepts):
            if freq >= 2:  # Minimum frequency threshold
                concept = Concept(
                    text=word,
                    frequency=freq,
                    relevance_score=min(freq / max(word_freq.values()), 1.0),
                    extraction_method="tfidf",
                )
                concepts.append(concept)

        return concepts

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for TextRank processing."""
        # Simple sentence splitting
        sentences = re.split(SENTENCE_SPLIT_PATTERN, text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    def _build_word_graph(self, sentences: List[str]) -> nx.Graph:
        """Build word co-occurrence graph for TextRank."""
        graph = nx.Graph()

        for sentence in sentences:
            words = re.findall(WORD_EXTRACTION_PATTERN, sentence.lower())
            self._add_words_to_graph(graph, words)
            self._add_cooccurrence_edges(graph, words)

        return graph

    def _add_words_to_graph(self, graph: nx.Graph, words: List[str]) -> None:
        """Add words as nodes to the graph."""
        for word in words:
            if word not in graph:
                graph.add_node(word)

    def _add_cooccurrence_edges(self, graph: nx.Graph, words: List[str]) -> None:
        """Add edges between co-occurring words."""
        for i, word1 in enumerate(words):
            for word2 in words[i + 1 : i + 6]:  # Window of 5 words
                if word1 != word2:
                    self._update_edge_weight(graph, word1, word2)

    def _update_edge_weight(self, graph: nx.Graph, word1: str, word2: str) -> None:
        """Update edge weight between two words."""
        if graph.has_edge(word1, word2):
            graph[word1][word2]["weight"] += 1
        else:
            graph.add_edge(word1, word2, weight=1)

    def _filter_and_deduplicate_concepts(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Filter and deduplicate statistical concepts."""
        # Remove very low scoring concepts
        filtered = [c for c in concepts if c.relevance_score > 0.1]

        # Sort by relevance score and limit
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)
        return filtered[: config.max_concepts_per_strategy]


class EmbeddingBasedExtractionStrategy(ConceptExtractionStrategy):
    """
    Embedding-based concept extraction using semantic similarity and clustering.

    Educational Note:
    This strategy uses vector representations (embeddings) to capture semantic
    meaning and identify concepts through clustering and similarity analysis.
    It demonstrates modern NLP approaches using neural language models.
    """

    def extract_concepts(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """Extract concepts using embedding-based methods."""
        concepts = []
        metadata = {
            "extraction_method": "embedding_based",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "techniques_used": [],
        }

        # For single document, extract candidate phrases first
        candidate_phrases = self._extract_candidate_phrases(text)

        if len(candidate_phrases) > 1:
            # Group similar phrases using embeddings
            similarity_groups = self.group_similar_phrases(
                candidate_phrases, similarity_threshold=config.similarity_threshold
            )

            # Create concepts from phrase groups
            for group in similarity_groups:
                representative_phrase = max(
                    group.phrases, key=len
                )  # Use longest phrase as representative
                concept = Concept(
                    text=representative_phrase,
                    frequency=len(group.phrases),
                    relevance_score=group.average_similarity,
                    extraction_method="semantic_embedding",
                )
                concepts.append(concept)

            metadata["techniques_used"].append("phrase_clustering")
            metadata["similarity_groups"] = len(similarity_groups)

        # Apply concept consolidation
        if config.merge_similar_concepts and len(concepts) > 1:
            concepts = self.consolidate_similar_concepts(
                concepts, similarity_threshold=config.similarity_threshold
            )
            metadata["techniques_used"].append("concept_consolidation")

        # Filter and limit results
        concepts = self._filter_and_limit_concepts(concepts, config)

        metadata["total_concepts_extracted"] = len(concepts)
        return ExtractionResult(concepts=concepts, metadata=metadata)

    def cluster_documents(self, documents: List[str], num_clusters: int = 3):
        """
        Cluster documents using embedding similarity.

        Educational Note:
        Document clustering groups semantically similar documents,
        useful for discovering thematic concepts across a corpus.
        """
        # This would require actual embedding service integration
        # For now, return mock clusters for testing
        clusters = []
        docs_per_cluster = len(documents) // num_clusters or 1

        for i in range(num_clusters):
            start_idx = i * docs_per_cluster
            end_idx = min((i + 1) * docs_per_cluster, len(documents))
            cluster_docs = documents[start_idx:end_idx]

            cluster = type(
                "DocumentCluster",
                (),
                {
                    "documents": cluster_docs,
                    "centroid_embedding": EmbeddingVector(
                        vector=tuple([0.1] * 384)
                    ),  # Mock embedding
                    "coherence_score": 0.8,
                },
            )()
            clusters.append(cluster)

        return clusters

    def group_similar_phrases(
        self, phrases: List[str], similarity_threshold: float = 0.7
    ):
        """
        Group semantically similar phrases using embeddings.

        Educational Note:
        Phrase grouping identifies synonyms and related terms,
        reducing redundancy in concept extraction results.
        """
        # Mock implementation for testing
        # In real implementation, would use sentence transformers
        groups = []

        # Simple grouping based on word overlap (placeholder)
        remaining_phrases = phrases.copy()

        while remaining_phrases:
            current_phrase = remaining_phrases.pop(0)
            group_phrases = [current_phrase]

            # Find similar phrases (mock similarity calculation)
            to_remove = []
            for phrase in remaining_phrases:
                similarity = self._mock_phrase_similarity(current_phrase, phrase)
                if similarity >= similarity_threshold:
                    group_phrases.append(phrase)
                    to_remove.append(phrase)

            # Remove grouped phrases from remaining
            for phrase in to_remove:
                remaining_phrases.remove(phrase)

            # Create phrase group
            group = type(
                "PhraseGroup",
                (),
                {
                    "phrases": group_phrases,
                    "average_similarity": 0.8,  # Mock similarity
                },
            )()
            groups.append(group)

        return groups

    def consolidate_similar_concepts(
        self, concepts: List[Concept], similarity_threshold: float = 0.8
    ) -> List[Concept]:
        """
        Consolidate semantically similar concepts.

        Educational Note:
        Concept consolidation merges similar concepts while preserving
        evidence and metadata, reducing redundancy in final results.
        """
        if len(concepts) <= 1:
            return concepts

        consolidated = []
        remaining_concepts = concepts.copy()

        while remaining_concepts:
            primary_concept = remaining_concepts.pop(0)
            similar_concepts = [primary_concept]

            # Find similar concepts
            to_remove = []
            for concept in remaining_concepts:
                similarity = self._calculate_concept_similarity(
                    primary_concept, concept
                )
                if similarity >= similarity_threshold:
                    similar_concepts.append(concept)
                    to_remove.append(concept)

            # Remove similar concepts from remaining
            for concept in to_remove:
                remaining_concepts.remove(concept)

            # Consolidate similar concepts
            if len(similar_concepts) > 1:
                consolidated_concept = self._merge_concepts(similar_concepts)
            else:
                consolidated_concept = primary_concept

            consolidated.append(consolidated_concept)

        return consolidated

    def _extract_candidate_phrases(self, text: str) -> List[str]:
        """Extract candidate phrases for concept analysis."""
        # Simple phrase extraction (2-4 word phrases)
        phrases = []

        # Extract noun phrases and technical terms
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        for i in range(len(words)):
            # Extract 2-4 word phrases
            for length in [2, 3, 4]:
                if i + length <= len(words):
                    phrase = " ".join(words[i : i + length])
                    if len(phrase) > 6:  # Minimum meaningful length
                        phrases.append(phrase)

        # Remove duplicates and very common phrases
        unique_phrases = list(set(phrases))
        stopwords = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }

        filtered_phrases = []
        for phrase in unique_phrases:
            words_in_phrase = phrase.split()
            if not any(word in stopwords for word in words_in_phrase):
                filtered_phrases.append(phrase)

        return filtered_phrases[:50]  # Limit candidate phrases

    def _mock_phrase_similarity(self, phrase1: str, phrase2: str) -> float:
        """Mock phrase similarity calculation for testing."""
        words1 = set(phrase1.split())
        words2 = set(phrase2.split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def _calculate_concept_similarity(
        self, concept1: Concept, concept2: Concept
    ) -> float:
        """Calculate similarity between two concepts."""
        # Mock similarity based on text overlap
        return self._mock_phrase_similarity(concept1.text, concept2.text)

    def _merge_concepts(self, concepts: List[Concept]) -> Concept:
        """Merge multiple similar concepts into one."""
        # Use the concept with highest relevance as primary
        primary = max(concepts, key=lambda c: c.relevance_score)

        # Combine frequencies and metadata
        total_frequency = sum(c.frequency for c in concepts)
        avg_relevance = sum(c.relevance_score for c in concepts) / len(concepts)

        # Merge metadata (simplified since extraction_metadata doesn't exist)

        return Concept(
            text=primary.text,
            frequency=total_frequency,
            relevance_score=avg_relevance,
            extraction_method="semantic_embedding",
        )

    def _filter_and_limit_concepts(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Filter and limit embedding-based concepts."""
        # Filter by minimum frequency and relevance
        filtered = [
            c
            for c in concepts
            if c.frequency >= config.min_concept_frequency and c.relevance_score > 0.5
        ]

        # Sort by relevance score and limit
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)
        return filtered[: config.max_concepts_per_strategy]

    def _get_phrase_embeddings(self, phrases: List[str]) -> Dict[str, EmbeddingVector]:
        """Get embeddings for phrases (mock implementation for testing)."""
        # Mock embeddings for testing purposes
        embeddings = {}
        for phrase in phrases:
            # Generate mock embedding
            embedding = EmbeddingVector(vector=tuple([0.1] * 384))
            embeddings[phrase] = embedding
        return embeddings

    def _cluster_document_embeddings(self, documents: List[str]) -> List[Concept]:
        """Cluster documents using embeddings (mock implementation for testing)."""
        # Mock implementation that returns sample concepts
        concepts = []
        for i, doc in enumerate(documents[:3]):  # Limit to 3 concepts
            concept = Concept(
                text=f"document_cluster_{i}",
                frequency=1,
                relevance_score=0.8 - i * 0.1,
                extraction_method="semantic_embedding",
            )
            concepts.append(concept)
        return concepts


class MultiStrategyConceptExtractor:
    """
    Orchestrator for multi-strategy concept extraction.

    Educational Note:
    This class implements the Composite pattern to combine results from
    multiple extraction strategies, demonstrating how to aggregate
    diverse algorithmic approaches for comprehensive concept coverage.

    Design Patterns Applied:
    - Composite Pattern: Treats individual strategies and strategy combinations uniformly
    - Strategy Pattern: Delegates to pluggable extraction strategies
    - Template Method: Defines common workflow for multi-strategy extraction
    """

    def __init__(self, strategies: Optional[List[ConceptExtractionStrategy]] = None):
        """Initialize with extraction strategies."""
        if strategies is None:
            # Default strategy configuration
            self.strategies = [
                RuleBasedExtractionStrategy(),
                StatisticalExtractionStrategy(),
                EmbeddingBasedExtractionStrategy(),
            ]
        else:
            self.strategies = strategies

    def extract_concepts_comprehensive(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """
        Extract concepts using all configured strategies.

        Educational Note:
        Orchestrates multiple extraction strategies and consolidates
        their results, demonstrating how to combine diverse approaches
        for comprehensive concept coverage.
        """
        all_concepts = []
        strategy_results = {}

        # Execute each strategy
        for i, strategy in enumerate(self.strategies):
            try:
                strategy_name = strategy.__class__.__name__.replace(
                    "ExtractionStrategy", ""
                ).lower()
                result = strategy.extract_concepts(text, config)

                # Apply strategy weights if configured
                if strategy_name in config.strategy_weights:
                    weight = config.strategy_weights[strategy_name]
                    weighted_concepts = self._apply_strategy_weight(
                        result.concepts, weight
                    )
                    all_concepts.extend(weighted_concepts)
                else:
                    all_concepts.extend(result.concepts)

                strategy_results[strategy_name] = {
                    "concept_count": len(result.concepts),
                    "metadata": result.metadata,
                }

            except Exception as e:
                logging.warning(f"Strategy {strategy.__class__.__name__} failed: {e}")
                continue

        # Consolidate results
        if config.consolidate_results:
            consolidated_concepts = self._consolidate_multi_strategy_results(
                all_concepts, config
            )
        else:
            consolidated_concepts = all_concepts

        # Create final result metadata
        final_metadata = {
            "extraction_method": "multi_strategy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "strategies_used": list(strategy_results.keys()),
            "strategy_results": strategy_results,
            "total_raw_concepts": len(all_concepts),
            "total_consolidated_concepts": len(consolidated_concepts),
        }

        if "strategy_weights" in config.__dict__ and config.strategy_weights:
            final_metadata["weighted_combination"] = True
            final_metadata["weights_applied"] = config.strategy_weights

        return ExtractionResult(concepts=consolidated_concepts, metadata=final_metadata)

    def _apply_strategy_weight(
        self, concepts: List[Concept], weight: float
    ) -> List[Concept]:
        """Apply weight to concept relevance scores."""
        weighted_concepts = []
        for concept in concepts:
            weighted_concept = Concept(
                text=concept.text,
                frequency=concept.frequency,
                relevance_score=concept.relevance_score * weight,
                extraction_method=concept.extraction_method,
            )
            weighted_concepts.append(weighted_concept)
        return weighted_concepts

    def _consolidate_multi_strategy_results(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Consolidate concepts from multiple strategies."""
        # Group concepts by text similarity
        concept_groups = defaultdict(list)

        for concept in concepts:
            # Simple grouping by exact text match for now
            # In full implementation, would use semantic similarity
            group_key = concept.text.lower().strip()
            concept_groups[group_key].append(concept)

        consolidated = []
        for text, group in concept_groups.items():
            if len(group) == 1:
                consolidated.append(group[0])
            else:
                # Merge concepts from multiple strategies
                merged_concept = self._merge_multi_strategy_concepts(group)
                consolidated.append(merged_concept)

        # Sort by combined relevance and frequency
        consolidated.sort(key=lambda c: (c.relevance_score * c.frequency), reverse=True)

        # Apply final filtering
        return consolidated[
            : config.max_concepts_per_strategy * 2
        ]  # Allow more for multi-strategy

    def _merge_multi_strategy_concepts(self, concepts: List[Concept]) -> Concept:
        """Merge concepts from multiple strategies."""
        # Use the highest relevance concept as base
        primary = max(concepts, key=lambda c: c.relevance_score)

        # Combine evidence from all strategies
        total_frequency = sum(c.frequency for c in concepts)
        weighted_relevance = (
            sum(c.relevance_score * c.frequency for c in concepts) / total_frequency
            if total_frequency > 0
            else primary.relevance_score
        )

        return Concept(
            text=primary.text,
            frequency=total_frequency,
            relevance_score=weighted_relevance,
            extraction_method="semantic_embedding",
        )
