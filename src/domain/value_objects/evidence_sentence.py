"""
EvidenceSentence - Value object representing supporting evidence for extracted concepts.

This value object encapsulates a sentence from a research paper that provides
evidence for a specific concept, with full traceability and quality metrics.

Educational Notes - Value Object Pattern (Domain-Driven Design):
- Immutable state prevents accidental modification of evidence data
- Equality by value enables deduplication of identical evidence sentences
- No identity means evidence sentences are interchangeable if data matches
- Rich behavior provides useful operations without breaking encapsulation
- Demonstrates how value objects encapsulate both data and related behavior

Educational Notes - SOLID Principles Demonstrated:
- Single Responsibility: Only responsible for evidence sentence representation
- Open/Closed: Can be extended with new methods without modification
- Liskov Substitution: Any EvidenceSentence can substitute for another
- Interface Segregation: Provides focused interface for evidence operations
- Dependency Inversion: Depends on abstractions through validation utilities

Educational Notes - Academic Research Requirements:
- Evidence grounding ensures no "hallucinated" concepts in research
- Source paper linking enables researchers to verify concept claims
- Confidence scoring provides transparency about extraction quality
- Method tracking enables comparison between extraction strategies
- Full audit trail supports peer review and scientific reproducibility

Design Decisions:
- Frozen dataclass ensures immutability for audit trail integrity
- Common validation utilities promote consistency and maintainability
- Rich methods demonstrate value object behavior beyond simple data storage
- Clear separation between validation and business logic

Design Patterns Applied:
- Value Object Pattern: Immutable objects with equality by value
- Template Method Pattern: Consistent validation approach across domain
- Strategy Pattern: Different extraction methods can be plugged in
- Builder Pattern: Complex creation through factory methods

Use Cases:
- Academic Research: Provides verifiable evidence for extracted concepts
- Quality Assessment: Enables ranking of evidence by confidence and method
- Reproducibility: Full provenance tracking for scientific reproducibility
- Algorithm Comparison: Enables evaluation of different extraction methods
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Tuple
import re

from src.domain.common.validation import (
    validate_non_empty_string,
    validate_positive_integer,
    validate_probability_score,
    DomainValidationError,
)


@dataclass(frozen=True)
class EvidenceSentence:
    """
    Represents a sentence from a research paper that provides evidence for a concept.

    This value object captures the complete context needed to verify and assess
    the quality of concept extraction evidence.

    Attributes:
        sentence_text: The actual sentence text from the source paper
        paper_doi: DOI or identifier of the source paper for verification
        page_number: Page number where the sentence appears
        confidence_score: Extraction confidence between 0.0 and 1.0
        extraction_method: Name of the method used to extract this evidence
        concept_text: The specific concept this sentence supports
    """

    sentence_text: str
    paper_doi: str
    page_number: int
    confidence_score: float
    extraction_method: str
    concept_text: str

    def __post_init__(self):
        """
        Validate evidence sentence data for research quality standards.

        Educational Notes - Template Method Pattern:
        - Uses common validation utilities to ensure consistent behavior
        - Demonstrates separation of validation concerns from business logic
        - Each validation focuses on a single responsibility (SRP)
        - Promotes code reuse and maintainability across domain objects

        Educational Notes - Fail Fast Principle:
        - Validation occurs immediately upon object creation
        - Invalid data is caught as early as possible in the process
        - Clear error messages help developers identify and fix issues
        - Prevents invalid objects from propagating through the system

        Educational Notes - Domain Invariants:
        - Ensures all evidence sentences meet minimum quality standards
        - Prevents creation of objects that violate domain business rules
        - Maintains data integrity required for academic research
        - Supports reproducible and trustworthy research results
        """
        try:
            # Demonstrate Single Responsibility: Each validator has one purpose
            validate_non_empty_string(self.sentence_text, "Evidence sentence text")
            validate_non_empty_string(self.paper_doi, "Paper DOI")
            validate_non_empty_string(self.extraction_method, "Extraction method")
            validate_non_empty_string(self.concept_text, "Concept text")

            # Demonstrate Domain-Specific Validation
            validate_probability_score(self.confidence_score, "Confidence score")
            validate_positive_integer(self.page_number, "Page number")

        except DomainValidationError as e:
            # Wrap domain validation errors with context for better debugging
            raise DomainValidationError(f"Invalid evidence sentence: {e}")

    @classmethod
    def create_high_confidence_evidence(
        cls,
        sentence_text: str,
        paper_doi: str,
        page_number: int,
        extraction_method: str,
        concept_text: str,
    ) -> "EvidenceSentence":
        """
        Factory method for creating high-confidence evidence sentences.

        Educational Notes - Factory Method Pattern:
        - Provides named constructors for different creation scenarios
        - Encapsulates complex creation logic in domain-meaningful methods
        - Makes intent clear through method naming
        - Allows for different validation or default rules per creation type

        Args:
            sentence_text: The evidence sentence from the research paper
            paper_doi: DOI or identifier of the source paper
            page_number: Page number where evidence appears
            extraction_method: Method used to extract this evidence
            concept_text: The concept this evidence supports

        Returns:
            EvidenceSentence with confidence score of 0.9
        """
        return cls(
            sentence_text=sentence_text,
            paper_doi=paper_doi,
            page_number=page_number,
            confidence_score=0.9,  # High confidence threshold
            extraction_method=extraction_method,
            concept_text=concept_text,
        )

    @classmethod
    def create_from_extraction_result(
        cls,
        sentence_text: str,
        paper_doi: str,
        page_number: int,
        confidence_score: float,
        extraction_method: str,
        concept_text: str,
    ) -> "EvidenceSentence":
        """
        Factory method for creating evidence from extraction algorithm results.

        Educational Notes - Named Constructor Pattern:
        - Clarifies the source and context of the evidence sentence
        - Provides validation specific to extraction algorithm outputs
        - Makes creation intent explicit in the calling code
        - Supports different confidence score ranges per extraction method

        Args:
            sentence_text: The evidence sentence from the research paper
            paper_doi: DOI or identifier of the source paper
            page_number: Page number where evidence appears
            confidence_score: Algorithm-computed confidence (0.0 to 1.0)
            extraction_method: Specific algorithm used for extraction
            concept_text: The concept this evidence supports

        Returns:
            EvidenceSentence with algorithm-provided confidence score
        """
        return cls(
            sentence_text=sentence_text,
            paper_doi=paper_doi,
            page_number=page_number,
            confidence_score=confidence_score,
            extraction_method=extraction_method,
            concept_text=concept_text,
        )

    def get_paper_reference(self) -> str:
        """
        Generate a formatted reference string for this evidence.

        Returns:
            A formatted string suitable for academic citation

        Educational Notes - Academic Standards:
        - Provides standard format for paper references in research
        - Enables quick verification of evidence sources
        - Includes page number for precise location within paper
        """
        return f"{self.paper_doi}, page {self.page_number}"

    def get_extraction_info(self) -> Dict[str, Any]:
        """
        Get comprehensive extraction context information.

        Returns:
            Dictionary containing extraction method, confidence, and concept

        Educational Notes - Transparency:
        - Provides complete context for how evidence was extracted
        - Enables researchers to assess extraction quality
        - Supports comparison of different extraction methods
        """
        return {
            "method": self.extraction_method,
            "confidence": self.confidence_score,
            "concept": self.concept_text,
            "source": self.get_paper_reference(),
        }

    def is_high_quality(self, threshold: float = 0.8) -> bool:
        """
        Assess whether this evidence meets high quality standards.

        Args:
            threshold: Minimum confidence score for high quality (default 0.8)

        Returns:
            True if evidence confidence meets or exceeds threshold

        Educational Notes - Quality Assessment:
        - Provides objective quality assessment based on confidence
        - Enables filtering of low-quality evidence in research
        - Threshold can be adjusted based on research requirements
        """
        return self.confidence_score >= threshold

    def get_sentence_length_category(self) -> str:
        """
        Categorize sentence length for evidence quality assessment.

        Returns:
            Category string: "short", "medium", "long", or "very_long"

        Educational Notes - Evidence Quality:
        - Sentence length can indicate evidence quality and specificity
        - Very short sentences may lack context
        - Very long sentences may be too complex or off-topic
        - Medium-length sentences often provide best evidence quality
        """
        word_count = len(self.sentence_text.split())

        if word_count < 5:
            return "short"
        elif word_count < 15:
            return "medium"
        elif word_count < 30:
            return "long"
        else:
            return "very_long"

    def contains_technical_terms(self) -> bool:
        """
        Check if evidence sentence contains technical or domain-specific terms.

        Returns:
            True if sentence appears to contain technical terminology

        Educational Notes - Domain Relevance:
        - Technical terms often indicate higher relevance to research concepts
        - Can help assess whether evidence is domain-appropriate
        - Simple heuristic based on capitalization and compound words
        """
        # Simple heuristic: look for capitalized terms, compound words, or domain indicators
        technical_indicators = [
            r"[A-Z][a-z]+(?:[A-Z][a-z]+)+",  # CamelCase terms
            r"\b[A-Z]{2,}\b",  # Acronyms
            r"\b\w+[-_]\w+\b",  # Hyphenated/underscore terms
            r"\b(?:algorithm|method|technique|approach|framework|model|system)\b",  # Domain terms
        ]

        text = self.sentence_text
        for pattern in technical_indicators:
            if re.search(pattern, text):
                return True

        return False

    @staticmethod
    def group_by_concept(
        evidence_list: List["EvidenceSentence"],
    ) -> Dict[str, List["EvidenceSentence"]]:
        """
        Group evidence sentences by their associated concept.

        Args:
            evidence_list: List of evidence sentences to group

        Returns:
            Dictionary mapping concept texts to lists of supporting evidence

        Educational Notes - Evidence Organization:
        - Enables researchers to see all evidence for each concept
        - Supports concept validation by examining supporting evidence
        - Facilitates quality assessment across concepts
        """
        grouped: Dict[str, List["EvidenceSentence"]] = {}

        for evidence in evidence_list:
            concept = evidence.concept_text
            if concept not in grouped:
                grouped[concept] = []
            grouped[concept].append(evidence)

        return grouped

    @staticmethod
    def filter_by_confidence(
        evidence_list: List["EvidenceSentence"], min_confidence: float
    ) -> List["EvidenceSentence"]:
        """
        Filter evidence sentences by minimum confidence threshold.

        Args:
            evidence_list: List of evidence sentences to filter
            min_confidence: Minimum confidence score (0.0 to 1.0)

        Returns:
            List of evidence sentences meeting confidence threshold

        Educational Notes - Quality Control:
        - Enables researchers to focus on high-confidence evidence
        - Supports quality control in concept validation
        - Allows adjustment of quality standards based on research needs
        """
        return [
            evidence
            for evidence in evidence_list
            if evidence.confidence_score >= min_confidence
        ]

    @staticmethod
    def get_confidence_statistics(
        evidence_list: List["EvidenceSentence"],
    ) -> Dict[str, float]:
        """
        Calculate confidence statistics across a list of evidence sentences.

        Args:
            evidence_list: List of evidence sentences to analyze

        Returns:
            Dictionary containing mean, min, max, and standard deviation of confidence scores

        Educational Notes - Statistical Analysis:
        - Provides overview of evidence quality across concept extraction
        - Enables comparison of extraction methods or parameter settings
        - Supports quality assessment and algorithm improvement
        """
        if not evidence_list:
            return {"mean": 0.0, "min": 0.0, "max": 0.0, "std_dev": 0.0}

        confidences = [ev.confidence_score for ev in evidence_list]

        mean_conf = sum(confidences) / len(confidences)
        min_conf = min(confidences)
        max_conf = max(confidences)

        # Calculate standard deviation
        variance = sum((x - mean_conf) ** 2 for x in confidences) / len(confidences)
        std_dev = variance**0.5

        return {"mean": mean_conf, "min": min_conf, "max": max_conf, "std_dev": std_dev}
