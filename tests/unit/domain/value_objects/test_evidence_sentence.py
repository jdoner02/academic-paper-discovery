"""
Unit tests for EvidenceSentence value object.

This test suite validates the EvidenceSentence value object, which tracks
supporting sentences for concepts with full traceability to source papers.

Educational Notes - Value Object Testing:
- Immutability testing ensures value objects cannot be modified after creation
- Equality testing validates that value objects with same data are considered equal
- Validation testing ensures business rules are enforced at creation time
- Hash testing ensures value objects can be used in sets and as dictionary keys

Educational Notes - Academic Research Requirements:
- Evidence grounding ensures no "hallucinated" concepts in research
- Source paper linking enables researchers to verify concept claims
- Confidence scoring provides transparency about extraction quality
- Method tracking enables comparison between extraction strategies

Value Object Pattern Benefits:
- Immutable state prevents accidental modification of evidence data
- Equality by value enables deduplication of identical evidence sentences
- No identity means evidence sentences are interchangeable if data matches
- Validation ensures evidence integrity at the domain boundary
"""

import pytest
from datetime import datetime, timezone

from src.domain.value_objects.evidence_sentence import EvidenceSentence
from src.domain.common.validation import DomainValidationError


class TestEvidenceSentenceCreation:
    """Test evidence sentence creation and validation."""

    def test_create_valid_evidence_sentence(self):
        """Test creation of a valid evidence sentence."""
        # This test should fail initially (RED phase)
        evidence = EvidenceSentence(
            sentence_text="Neural networks are computational models inspired by biological neurons.",
            paper_doi="10.1000/neural.networks.2024",
            page_number=5,
            confidence_score=0.92,
            extraction_method="rule_based",
            concept_text="Neural Networks",
        )

        assert (
            evidence.sentence_text
            == "Neural networks are computational models inspired by biological neurons."
        )
        assert evidence.paper_doi == "10.1000/neural.networks.2024"
        assert evidence.page_number == 5
        assert evidence.confidence_score == 0.92
        assert evidence.extraction_method == "rule_based"
        assert evidence.concept_text == "Neural Networks"

    def test_reject_empty_sentence_text(self):
        """Test that evidence sentence rejects empty or whitespace-only text."""
        # This test should fail initially (RED phase)
        with pytest.raises(ValueError, match="Evidence sentence text cannot be empty"):
            EvidenceSentence(
                sentence_text="   ",  # Whitespace only
                paper_doi="10.1000/test.2024",
                page_number=1,
                confidence_score=0.8,
                extraction_method="statistical",
                concept_text="Test Concept",
            )

    def test_reject_invalid_confidence_score(self):
        """Test that evidence sentence rejects confidence scores outside [0.0, 1.0]."""
        # This test should fail initially (RED phase)
        with pytest.raises(
            DomainValidationError,
            match="Invalid evidence sentence: Confidence score must be a valid probability between 0.0 and 1.0",
        ):
            EvidenceSentence(
                sentence_text="Valid sentence text.",
                paper_doi="10.1000/test.2024",
                page_number=1,
                confidence_score=1.5,  # Invalid - greater than 1.0
                extraction_method="embedding_based",
                concept_text="Test Concept",
            )

    def test_reject_invalid_page_number(self):
        """Test that evidence sentence rejects negative page numbers."""
        # This test should fail initially (RED phase)
        with pytest.raises(ValueError, match="Page number must be positive"):
            EvidenceSentence(
                sentence_text="Valid sentence text.",
                paper_doi="10.1000/test.2024",
                page_number=-1,  # Invalid - negative page number
                confidence_score=0.8,
                extraction_method="rule_based",
                concept_text="Test Concept",
            )


class TestEvidenceSentenceValueObjectBehavior:
    """Test value object characteristics of EvidenceSentence."""

    def test_evidence_sentence_equality(self):
        """Test that evidence sentences with identical data are equal."""
        # This test should fail initially (RED phase)
        evidence1 = EvidenceSentence(
            sentence_text="Machine learning algorithms process data efficiently.",
            paper_doi="10.1000/ml.efficiency.2024",
            page_number=10,
            confidence_score=0.85,
            extraction_method="statistical",
            concept_text="Machine Learning",
        )

        evidence2 = EvidenceSentence(
            sentence_text="Machine learning algorithms process data efficiently.",
            paper_doi="10.1000/ml.efficiency.2024",
            page_number=10,
            confidence_score=0.85,
            extraction_method="statistical",
            concept_text="Machine Learning",
        )

        assert evidence1 == evidence2
        assert hash(evidence1) == hash(evidence2)

    def test_evidence_sentence_inequality(self):
        """Test that evidence sentences with different data are not equal."""
        # This test should fail initially (RED phase)
        evidence1 = EvidenceSentence(
            sentence_text="Deep learning requires large datasets.",
            paper_doi="10.1000/deep.learning.2024",
            page_number=5,
            confidence_score=0.90,
            extraction_method="rule_based",
            concept_text="Deep Learning",
        )

        evidence2 = EvidenceSentence(
            sentence_text="Deep learning requires large datasets.",
            paper_doi="10.1000/deep.learning.2024",
            page_number=6,  # Different page number
            confidence_score=0.90,
            extraction_method="rule_based",
            concept_text="Deep Learning",
        )

        assert evidence1 != evidence2
        assert hash(evidence1) != hash(evidence2)

    def test_evidence_sentence_immutability(self):
        """Test that evidence sentence is immutable after creation."""
        # This test should fail initially (RED phase)
        evidence = EvidenceSentence(
            sentence_text="Original sentence text.",
            paper_doi="10.1000/original.2024",
            page_number=1,
            confidence_score=0.8,
            extraction_method="original_method",
            concept_text="Original Concept",
        )

        # Should not be able to modify attributes (frozen dataclass)
        with pytest.raises(AttributeError):
            evidence.sentence_text = "Modified text"

        with pytest.raises(AttributeError):
            evidence.confidence_score = 0.9


class TestEvidenceSentenceResearchApplications:
    """Test evidence sentence usage in research scenarios."""

    def test_evidence_sentence_paper_linking(self):
        """Test evidence sentence provides proper paper linking for verification."""
        # This test should fail initially (RED phase)
        evidence = EvidenceSentence(
            sentence_text="Convolutional layers extract hierarchical features from images.",
            paper_doi="10.1000/cnn.vision.2024",
            page_number=12,
            confidence_score=0.88,
            extraction_method="embedding_based",
            concept_text="Convolutional Neural Networks",
        )

        # Should provide clear paper reference for verification
        paper_reference = evidence.get_paper_reference()
        assert "10.1000/cnn.vision.2024" in paper_reference
        assert "page 12" in paper_reference

    def test_evidence_sentence_extraction_context(self):
        """Test evidence sentence provides extraction method context."""
        # This test should fail initially (RED phase)
        evidence = EvidenceSentence(
            sentence_text="Support vector machines optimize margin separation.",
            paper_doi="10.1000/svm.optimization.2024",
            page_number=8,
            confidence_score=0.93,
            extraction_method="rule_based",
            concept_text="Support Vector Machines",
        )

        # Should indicate how the evidence was extracted
        extraction_info = evidence.get_extraction_info()
        assert extraction_info["method"] == "rule_based"
        assert extraction_info["confidence"] == 0.93
        assert extraction_info["concept"] == "Support Vector Machines"

    def test_evidence_sentence_quality_assessment(self):
        """Test evidence sentence supports quality assessment operations."""
        # This test should fail initially (RED phase)
        high_quality_evidence = EvidenceSentence(
            sentence_text="Random forests combine multiple decision trees to improve accuracy.",
            paper_doi="10.1000/random.forests.2024",
            page_number=15,
            confidence_score=0.95,
            extraction_method="rule_based",
            concept_text="Random Forests",
        )

        low_quality_evidence = EvidenceSentence(
            sentence_text="The method works well.",  # Vague, low quality
            paper_doi="10.1000/vague.paper.2024",
            page_number=3,
            confidence_score=0.45,
            extraction_method="statistical",
            concept_text="Unknown Method",
        )

        assert high_quality_evidence.is_high_quality(threshold=0.8) is True
        assert low_quality_evidence.is_high_quality(threshold=0.8) is False

        # Should be able to compare evidence quality
        assert (
            high_quality_evidence.confidence_score
            > low_quality_evidence.confidence_score
        )


class TestEvidenceSentenceCollectionOperations:
    """Test evidence sentence usage in collections and aggregations."""

    def test_evidence_sentence_deduplication(self):
        """Test that identical evidence sentences can be deduplicated."""
        # This test should fail initially (RED phase)
        evidence1 = EvidenceSentence(
            sentence_text="Gradient descent optimizes neural network parameters.",
            paper_doi="10.1000/gradient.descent.2024",
            page_number=7,
            confidence_score=0.87,
            extraction_method="statistical",
            concept_text="Gradient Descent",
        )

        evidence2 = EvidenceSentence(
            sentence_text="Gradient descent optimizes neural network parameters.",
            paper_doi="10.1000/gradient.descent.2024",
            page_number=7,
            confidence_score=0.87,
            extraction_method="statistical",
            concept_text="Gradient Descent",
        )

        evidence_set = {evidence1, evidence2}
        assert len(evidence_set) == 1  # Should deduplicate identical evidence

    def test_evidence_sentence_grouping_by_concept(self):
        """Test evidence sentences can be grouped by concept text."""
        # This test should fail initially (RED phase)
        evidence_list = [
            EvidenceSentence(
                "DL sentence 1", "10.1000/dl1", 1, 0.9, "rule", "Deep Learning"
            ),
            EvidenceSentence(
                "ML sentence 1", "10.1000/ml1", 1, 0.8, "stat", "Machine Learning"
            ),
            EvidenceSentence(
                "DL sentence 2", "10.1000/dl2", 2, 0.85, "embed", "Deep Learning"
            ),
        ]

        grouped = EvidenceSentence.group_by_concept(evidence_list)
        assert len(grouped["Deep Learning"]) == 2
        assert len(grouped["Machine Learning"]) == 1
        assert all(
            ev.concept_text == "Deep Learning" for ev in grouped["Deep Learning"]
        )
        assert all(
            ev.concept_text == "Machine Learning" for ev in grouped["Machine Learning"]
        )
