"""
Concept Extraction Strategy Interface

Educational Notes:
- Demonstrates Strategy pattern interface definition
- Shows proper abstract base class design
- Illustrates contract definition for pluggable algorithms
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration

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



