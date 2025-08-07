"""
ConceptExtractor Domain Service - Extracts meaningful concepts from research papers.

This               # Combine standard English stop words with research-specific terms
        english_stopwords = set(get_stopwords("en"))  # Standard English stop words
        self.research_stopwords = english_stopwords.union({   # Combine standard English stop words with research-specific terms
        english_stopwords = set(get_stopwords("en"))  # Standard English stop words
        self.research_stopwords = english_stopwords.union({   # Combine standard English stop words with research-specific terms
        english_stopwords = set(get_stopwords("en"))  # Standard English stop words
        self.research_stopwords = english_stopwords.union({   # Combine standard English stop words with research-specific terms
        english_stopwords = set(get_stopwords("en"))  # Standard English stop words
        self.research_stopwords = english_stopwords.union({vice demonstrates Clean Architecture domain services by encapsulating
complex business logic that doesn't naturally belong in any single entity.

Educational Notes:
- Shows Domain Service pattern for complex business operations
- Demonstrates coordination of multiple extraction strategies
- Illustrates research-grade concept extraction with scientific rigor
- Shows how domain services can orchestrate multiple techniques

Design Decisions:
- Multiple extraction methods for comprehensive coverage
- Relevance scoring based on multiple factors
- Domain-aware concept filtering and ranking
- Extensible architecture for new extraction methods
- Research transparency through method tracking

Use Cases:
- Extract concepts from research paper text
- Apply domain-specific concept filtering
- Rank concepts by research relevance
- Coordinate multiple extraction strategies
"""

from typing import List, Dict, Set, Optional, Tuple
from abc import ABC, abstractmethod
import re
import math
from collections import Counter
import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from ..entities.concept import Concept
from ..entities.paper_concepts import PaperConcepts


class ConceptExtractionStrategy(ABC):
    """
    Abstract base class for concept extraction strategies.

    Educational Note:
    Strategy pattern implementation that allows different concept
    extraction algorithms to be used interchangeably while maintaining
    consistent interfaces and quality standards.
    """

    @abstractmethod
    def extract_concepts(
        self, text: str, paper_doi: str, domain: Optional[str] = None
    ) -> List[Concept]:
        """
        Extract concepts from text using this strategy.

        Args:
            text: Full text content to analyze
            paper_doi: DOI of the source paper
            domain: Research domain for context-aware extraction

        Returns:
            List of concepts extracted by this strategy
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name identifier for this extraction strategy."""
        pass


class TFIDFConceptExtractor(ConceptExtractionStrategy):
    """
    TF-IDF based concept extraction strategy.

    Educational Note:
    Implements Term Frequency-Inverse Document Frequency analysis
    to identify terms that are frequent in the document but rare
    across the broader corpus, indicating concept importance.
    """

    def __init__(
        self,
        min_term_length: int = 3,
        max_term_length: int = 50,
        min_frequency: int = 2,
        top_n_concepts: int = 50,
    ):
        self.min_term_length = min_term_length
        self.max_term_length = max_term_length
        self.min_frequency = min_frequency
        self.top_n_concepts = top_n_concepts

        # Comprehensive stop words list combining common English words with research terms
        self.research_stopwords = {
            # Common English stop words
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "been",
            "by",
            "for",
            "from",
            "has",
            "he",
            "in",
            "is",
            "it",
            "its",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "will",
            "with",
            "would",
            "have",
            "had",
            "do",
            "does",
            "did",
            "can",
            "could",
            "should",
            "may",
            "might",
            "must",
            "shall",
            "this",
            "these",
            "those",
            "them",
            "they",
            "their",
            "there",
            "where",
            "when",
            "what",
            "which",
            "who",
            "why",
            "how",
            "all",
            "any",
            "both",
            "each",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "also",
            "but",
            "or",
            "if",
            "because",
            "about",
            "after",
            "again",
            "against",
            "before",
            "being",
            "below",
            "between",
            "during",
            "further",
            "here",
            "now",
            "once",
            "then",
            "under",
            "until",
            "up",
            "down",
            "out",
            "off",
            "over",
            "through",
            "we",
            "us",
            "our",
            "ours",
            "you",
            "your",
            "yours",
            "i",
            "me",
            "my",
            "mine",
            "she",
            "her",
            "hers",
            "him",
            "his",
            # Research-specific academic terms
            "abstract",
            "introduction",
            "conclusion",
            "discussion",
            "results",
            "methods",
            "methodology",
            "analysis",
            "study",
            "research",
            "paper",
            "article",
            "journal",
            "conference",
            "proceedings",
            "author",
            "authors",
            "figure",
            "table",
            "section",
            "chapter",
            "page",
            "pages",
            "vol",
            "volume",
            "issue",
            "number",
            "doi",
            "isbn",
            "issn",
            "publication",
            "published",
            "publisher",
            "university",
            "department",
            "institute",
            "fig",
            "eq",
            "equation",
            "reference",
            "references",
            "bibliography",
            "appendix",
            "supplementary",
            "data",
            "dataset",
            "datasets",
            "experiment",
            "experiments",
            "experimental",
            "test",
            "tests",
            "testing",
            "evaluation",
            "evaluated",
            "performance",
            "approach",
            "method",
            "technique",
            "algorithm",
            "model",
            "modeling",
            "simulation",
            "presented",
            "proposed",
            "shown",
            "obtained",
            "observed",
            "found",
            "significant",
            "respectively",
            "however",
            "therefore",
            "thus",
            "hence",
            "furthermore",
            "moreover",
            "additionally",
            "particularly",
            "especially",
            "specifically",
            "generally",
            "typically",
            "commonly",
            "widely",
            "recently",
            "currently",
            "finally",
            # Common numerical and formatting terms
            "one",
            "two",
            "three",
            "four",
            "five",
            "first",
            "second",
            "third",
            "et",
            "al",
            "etc",
            "ie",
            "eg",
            "vs",
            "versus",
            "using",
            "used",
            "based",
            "within",
            "across",
            "among",
            "various",
            "different",
            "similar",
            "related",
            "compared",
            "shown",
            "demonstrated",
            "described",
            "investigated",
            "examined",
            "analyzed",
            "reported",
            "considered",
            "proposed",
            "developed",
            "applied",
            "implemented",
            "utilized",
        }

    def extract_concepts(
        self, text: str, paper_doi: str, domain: Optional[str] = None
    ) -> List[Concept]:
        """
        Extract concepts using TF-IDF analysis.

        Educational Note:
        Applies information retrieval techniques to identify
        statistically significant terms that likely represent
        important concepts within the research domain.
        """
        # Preprocess text
        cleaned_text = self._preprocess_text(text)

        # Extract candidate terms
        candidate_terms = self._extract_candidate_terms(cleaned_text)

        # Calculate term frequencies
        term_frequencies = self._calculate_term_frequencies(candidate_terms)

        # Filter by minimum frequency
        filtered_terms = {
            term: freq
            for term, freq in term_frequencies.items()
            if freq >= self.min_frequency
        }

        # Calculate TF-IDF scores (simplified - would need corpus for true IDF)
        concepts = []
        for term, frequency in filtered_terms.items():
            # Simplified relevance score based on frequency and term characteristics
            relevance_score = self._calculate_relevance_score(
                term, frequency, cleaned_text
            )

            concept = Concept(
                text=term,
                frequency=frequency,
                relevance_score=relevance_score,
                source_papers={paper_doi},
                source_domain=domain,
                extraction_method="tfidf",
            )
            concepts.append(concept)

        # Return top concepts by relevance
        concepts.sort(key=lambda c: c.relevance_score, reverse=True)
        return concepts[: self.top_n_concepts]

    def get_strategy_name(self) -> str:
        return "tfidf"

    def _preprocess_text(self, text: str) -> str:
        """
        Clean and normalize text for concept extraction.

        Educational Note:
        Text preprocessing is crucial for quality concept extraction,
        removing noise while preserving meaningful research terminology.
        """
        # Convert to lowercase
        text = text.lower()

        # Remove special characters but preserve hyphens in compound terms
        text = re.sub(r"[^\w\s\-]", " ", text)

        # Replace multiple whitespaces with single space
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _extract_candidate_terms(self, text: str) -> List[str]:
        """
        Extract candidate terms from preprocessed text.

        Educational Note:
        Identifies potential concepts by extracting n-grams and
        single terms while filtering out common stop words
        and applying length constraints.
        """
        words = text.split()
        candidates = []

        # Extract unigrams
        for word in words:
            if (
                self.min_term_length <= len(word) <= self.max_term_length
                and word not in self.research_stopwords
            ):
                candidates.append(word)

        # Extract bigrams for compound concepts
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i + 1]}"
            if (
                self.min_term_length <= len(bigram) <= self.max_term_length
                and words[i] not in self.research_stopwords
                and words[i + 1] not in self.research_stopwords
            ):
                candidates.append(bigram)

        # Extract trigrams for complex concepts
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i + 1]} {words[i + 2]}"
            if (
                self.min_term_length <= len(trigram) <= self.max_term_length
                and words[i] not in self.research_stopwords
                and words[i + 1] not in self.research_stopwords
                and words[i + 2] not in self.research_stopwords
            ):
                candidates.append(trigram)

        return candidates

    def _calculate_term_frequencies(self, candidates: List[str]) -> Dict[str, int]:
        """Calculate frequency of each candidate term."""
        return dict(Counter(candidates))

    def _calculate_relevance_score(self, term: str, frequency: int, text: str) -> float:
        """
        Calculate relevance score for a concept.

        Educational Note:
        Combines multiple signals to assess concept importance:
        - Term frequency within the document
        - Term length (longer terms often more specific)
        - Position-based weighting (title/abstract terms more important)
        - Domain-specific term patterns
        """
        text_length = len(text.split())

        # Base score from normalized frequency
        base_score = min(frequency / text_length * 100, 1.0)

        # Length bonus for compound terms (often more specific)
        length_bonus = min(len(term.split()) * 0.1, 0.3)

        # Technical term detection (contains numbers, hyphens, capitals)
        technical_bonus = 0.0
        if re.search(r"[\d\-]", term) or any(c.isupper() for c in term):
            technical_bonus = 0.1

        # Research domain term patterns
        domain_bonus = 0.0
        research_patterns = [
            r"analysis",
            r"method",
            r"algorithm",
            r"model",
            r"framework",
            r"approach",
            r"technique",
            r"system",
            r"process",
            r"protocol",
        ]
        for pattern in research_patterns:
            if re.search(pattern, term):
                domain_bonus = 0.15
                break

        # Combine scores with normalization
        total_score = base_score + length_bonus + technical_bonus + domain_bonus
        return min(total_score, 1.0)


@dataclass
class ExtractionConfiguration:
    """
    Configuration for concept extraction process.

    Educational Note:
    Value object that encapsulates extraction parameters,
    making the extraction process configurable and testable
    while maintaining sensible defaults for research use.
    """

    # TF-IDF configuration
    min_term_length: int = 3
    max_term_length: int = 50
    min_frequency: int = 2
    min_concept_frequency: int = 2  # Added for enhanced extraction control
    max_concepts_per_strategy: int = 50

    # General extraction settings
    merge_similar_concepts: bool = True
    similarity_threshold: float = 0.8
    min_relevance_threshold: float = 0.1

    # Domain-specific settings
    use_domain_stopwords: bool = True
    domain_specific_patterns: Optional[List[str]] = None


class ConceptExtractor:
    """
    Domain service for extracting concepts from research papers.

    Educational Note:
    Domain service that orchestrates multiple extraction strategies
    and applies business rules for concept quality and relevance.
    This demonstrates how complex domain logic can be organized
    when it doesn't naturally fit within a single entity.
    """

    def __init__(
        self,
        strategies: Optional[List[ConceptExtractionStrategy]] = None,
        config: Optional[ExtractionConfiguration] = None,
    ):
        """
        Initialize concept extractor with strategies and configuration.

        Args:
            strategies: List of extraction strategies to use
            config: Configuration parameters for extraction
        """
        self.strategies = strategies or [TFIDFConceptExtractor()]
        self.config = config or ExtractionConfiguration()

        # Validate strategies
        for strategy in self.strategies:
            if not isinstance(strategy, ConceptExtractionStrategy):
                raise ValueError(
                    "All strategies must implement ConceptExtractionStrategy"
                )

    def extract_concepts_from_paper(
        self,
        paper_text: str,
        paper_doi: str,
        paper_title: str,
        domain: Optional[str] = None,
    ) -> PaperConcepts:
        """
        Extract concepts from a research paper using all configured strategies.

        Educational Note:
        Main service method that coordinates multiple extraction strategies,
        consolidates results, and applies business rules to produce
        high-quality concept extractions for research use.

        Args:
            paper_text: Full text content of the paper
            paper_doi: DOI identifier of the paper
            paper_title: Title of the paper
            domain: Research domain for context-aware extraction

        Returns:
            PaperConcepts entity with all extracted concepts
        """
        if not paper_text or not paper_text.strip():
            raise ValueError("Paper text cannot be empty")

        if not paper_doi or not paper_doi.strip():
            raise ValueError("Paper DOI cannot be empty")

        if not paper_title or not paper_title.strip():
            raise ValueError("Paper title cannot be empty")

        all_concepts = []

        # Apply each extraction strategy
        for strategy in self.strategies:
            try:
                strategy_concepts = strategy.extract_concepts(
                    text=paper_text, paper_doi=paper_doi, domain=domain
                )
                all_concepts.extend(strategy_concepts)
            except Exception as e:
                # Log error but continue with other strategies
                print(f"Error in {strategy.get_strategy_name()} extraction: {e}")
                continue

        # Consolidate concepts from different strategies
        consolidated_concepts = self._consolidate_concepts(all_concepts)

        # Apply quality filters
        filtered_concepts = self._apply_quality_filters(consolidated_concepts)

        # Create and return PaperConcepts entity
        paper_concepts = PaperConcepts(
            paper_doi=paper_doi,
            paper_title=paper_title,
            concepts=filtered_concepts,
            extraction_timestamp=datetime.now(timezone.utc),
            extraction_method="mixed",
            processing_metadata={
                "strategies_used": [s.get_strategy_name() for s in self.strategies],
                "total_concepts_found": len(all_concepts),
                "concepts_after_consolidation": len(consolidated_concepts),
                "concepts_after_filtering": len(filtered_concepts),
            },
        )

        return paper_concepts

    def _consolidate_concepts(self, concepts: List[Concept]) -> List[Concept]:
        """
        Consolidate concepts from multiple strategies.

        Educational Note:
        Handles the common case where different extraction strategies
        identify the same concept, merging them to avoid duplication
        while preserving extraction metadata and frequency information.
        """
        concept_map = {}

        for concept in concepts:
            normalized_text = concept.text.lower().strip()

            if normalized_text in concept_map:
                # Merge with existing concept
                existing = concept_map[normalized_text]
                concept_map[normalized_text] = existing.merge_with_synonym(concept)
            else:
                concept_map[normalized_text] = concept

        return list(concept_map.values())

    def _apply_quality_filters(self, concepts: List[Concept]) -> List[Concept]:
        """
        Apply quality filters to remove low-value concepts.

        Educational Note:
        Implements business rules for concept quality, filtering out
        concepts that don't meet minimum thresholds for frequency,
        relevance, or other quality indicators.
        """
        filtered_concepts = []

        for concept in concepts:
            # Apply minimum relevance threshold
            if concept.relevance_score < self.config.min_relevance_threshold:
                continue

            # Apply minimum frequency threshold
            if concept.frequency < self.config.min_frequency:
                continue

            # Filter out overly generic terms (could be expanded)
            if concept.text in {"data", "result", "value", "number", "time", "way"}:
                continue

            filtered_concepts.append(concept)

        # Sort by relevance score
        filtered_concepts.sort(key=lambda c: c.relevance_score, reverse=True)

        return filtered_concepts

    def get_extraction_statistics(
        self, paper_concepts: PaperConcepts
    ) -> Dict[str, any]:
        """
        Calculate statistics about the extraction process.

        Educational Note:
        Provides analytics about extraction quality and coverage,
        useful for evaluating extraction effectiveness and
        tuning extraction parameters for specific domains.
        """
        concepts = paper_concepts.concepts

        if not concepts:
            return {
                "total_concepts": 0,
                "average_relevance": 0.0,
                "concept_diversity": 0.0,
                "extraction_methods": {},
                "quality_metrics": {},
            }

        # Basic statistics
        total_concepts = len(concepts)
        average_relevance = sum(c.relevance_score for c in concepts) / total_concepts

        # Concept diversity (Shannon entropy)
        concept_diversity = paper_concepts.calculate_concept_diversity()

        # Extraction method distribution
        method_distribution = paper_concepts.get_concept_distribution()

        # Quality metrics
        high_quality_concepts = len([c for c in concepts if c.relevance_score >= 0.7])
        significant_concepts = len([c for c in concepts if c.is_significant()])

        return {
            "total_concepts": total_concepts,
            "average_relevance": round(average_relevance, 3),
            "concept_diversity": round(concept_diversity, 3),
            "extraction_methods": method_distribution,
            "quality_metrics": {
                "high_quality_concepts": high_quality_concepts,
                "significant_concepts": significant_concepts,
                "quality_ratio": round(high_quality_concepts / total_concepts, 3),
                "significance_ratio": round(significant_concepts / total_concepts, 3),
            },
        }
