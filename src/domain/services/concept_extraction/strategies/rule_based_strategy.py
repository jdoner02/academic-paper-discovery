"""
Rule-Based Concept Extraction Strategy

Educational Notes:
- Implements Strategy pattern for rule-based extraction
- Demonstrates algorithmic approach to concept identification
- Shows proper separation of extraction logic
"""

import re
import spacy
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import Counter, defaultdict

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..utilities import _safe_extraction, COMMON_STOP_WORDS

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



