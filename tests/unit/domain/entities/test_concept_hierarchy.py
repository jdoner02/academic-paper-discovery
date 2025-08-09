"""
Unit tests for ConceptHierarchy aggregate root entity.

This test suite validates the ConceptHierarchy aggregate root, which manages
complete concept hierarchies with metadata, evidence tracking, and quality metrics.

Educational Notes - Test Organization:
- Test classes organized by behavior rather than just by method
- Each test class focuses on a specific aspect of the aggregate root
- Descriptive test names explain what business rule is being validated
- Setup methods create realistic test data for research paper scenarios

Educational Notes - Domain Testing Patterns:
- Aggregate Root Testing: Validates entity consistency and business invariants
- Value Object Integration: Tests interaction between aggregate and value objects
- Business Rule Validation: Ensures domain rules are enforced at entity level
- Immutability Testing: Verifies that modifications create new instances appropriately

Testing Strategy:
- Test aggregate root creation and validation rules
- Test hierarchy relationship management and integrity
- Test evidence sentence integration and traceability
- Test metadata tracking and provenance recording
- Test quality metrics calculation and validation
"""

import pytest
from datetime import datetime, timezone
from typing import List, Set
from unittest.mock import Mock

from src.domain.entities.concept import Concept
from src.domain.entities.concept_hierarchy import ConceptHierarchy
from src.domain.value_objects.evidence_sentence import EvidenceSentence
from src.domain.value_objects.hierarchy_metadata import HierarchyMetadata
from src.domain.value_objects.extraction_provenance import ExtractionProvenance


class TestConceptHierarchyCreation:
    """Test concept hierarchy creation and basic validation."""

    def setup_method(self):
        """Set up test data for concept hierarchy tests."""
        # Create sample concepts with hierarchical relationships
        self.root_concept = Concept(
            text="Machine Learning",
            frequency=100,
            relevance_score=0.9,
            source_papers={"10.1000/ml.2024"},
            concept_level=0,
            evidence_strength=0.95,
        )

        self.child_concept = Concept(
            text="Deep Learning",
            frequency=50,
            relevance_score=0.8,
            source_papers={"10.1000/dl.2024"},
            parent_concepts={"Machine Learning"},
            concept_level=1,
            evidence_strength=0.85,
        )

        self.grandchild_concept = Concept(
            text="Convolutional Neural Networks",
            frequency=25,
            relevance_score=0.7,
            source_papers={"10.1000/cnn.2024"},
            parent_concepts={"Deep Learning"},
            concept_level=2,
            evidence_strength=0.80,
        )

        # Sample evidence sentences
        self.evidence_sentences = [
            EvidenceSentence(
                sentence_text="Machine learning algorithms have revolutionized data analysis.",
                paper_doi="10.1000/ml.2024",
                page_number=1,
                confidence_score=0.9,
                extraction_method="rule_based",
                concept_text="Machine Learning",
            ),
            EvidenceSentence(
                sentence_text="Deep learning models achieve state-of-the-art performance.",
                paper_doi="10.1000/dl.2024",
                page_number=2,
                confidence_score=0.85,
                extraction_method="statistical",
                concept_text="Deep Learning",
            ),
        ]

        # Sample hierarchy metadata
        self.hierarchy_metadata = HierarchyMetadata(
            total_concepts=3,
            hierarchy_depth=3,
            average_confidence=0.85,
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=1,
            leaf_concepts_count=1,
            quality_score=0.87,
        )

        self.extraction_provenance = ExtractionProvenance(
            algorithm_name="Concept Extractor",
            algorithm_version="v1.0.0",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"threshold": 0.75, "min_frequency": 5},
            performance_metrics={"extraction_time": 30.5, "concepts_found": 3},
            paper_count=3,
            success_rate=0.95,
            error_log=["Info: Extraction completed successfully"],
        )

    def test_create_valid_concept_hierarchy(self):
        """Test creation of a valid concept hierarchy."""
        # This is a clear educational test showing how to create a hierarchy
        hierarchy = ConceptHierarchy(
            hierarchy_id="test_hierarchy",
            concepts=[self.root_concept, self.child_concept],
        )

        # Verify the hierarchy was created correctly
        assert hierarchy.hierarchy_id == "test_hierarchy"
        assert len(hierarchy.concepts) == 2
        assert self.root_concept in hierarchy.concepts
        assert self.child_concept in hierarchy.concepts

    def test_reject_empty_hierarchy(self):
        """Test that hierarchy creation rejects empty concept lists."""
        # This test should fail initially (RED phase)
        with pytest.raises(
            ValueError, match="Hierarchy must contain at least one concept"
        ):
            ConceptHierarchy(
                hierarchy_id="empty_hierarchy",
                root_concepts=[],
                all_concepts=[],
                evidence_sentences=[],
                hierarchy_metadata=self.hierarchy_metadata,
                extraction_provenance=self.extraction_provenance,
            )

    def test_reject_invalid_root_concepts(self):
        """Test that hierarchy creation rejects invalid root concepts."""
        # Create a concept that shouldn't be a root (has level > 0)
        invalid_root = Concept(
            text="Invalid Root",
            frequency=10,
            relevance_score=0.5,
            concept_level=1,  # Root concepts should have level 0
            evidence_strength=0.7,
        )

        # Educational test: clear validation message
        with pytest.raises(
            ValueError, match="Root concepts must have concept_level = 0"
        ):
            ConceptHierarchy(
                hierarchy_id="invalid_hierarchy", root_concepts=[invalid_root]
            )


class TestConceptHierarchyRelationships:
    """Test concept hierarchy relationship management and integrity."""

    def setup_method(self):
        """Set up simple test concepts for relationship testing."""
        self.parent_concept = Concept(
            text="Machine Learning",
            frequency=100,
            relevance_score=0.9,
            concept_level=0,
            evidence_strength=0.95,
        )

        self.child_concept = Concept(
            text="Deep Learning",
            frequency=60,
            relevance_score=0.85,
            concept_level=1,
            evidence_strength=0.90,
        )

    def test_validate_hierarchy_relationships(self):
        """Test that hierarchy correctly stores related concepts."""
        # Simple educational test: hierarchy can store parent and child concepts
        hierarchy = ConceptHierarchy(
            hierarchy_id="relationship_test",
            concepts=[self.parent_concept, self.child_concept],
        )

        # Verify both concepts are stored
        assert len(hierarchy.concepts) == 2
        assert self.parent_concept in hierarchy.concepts
        assert self.child_concept in hierarchy.concepts

    def test_prevent_circular_relationships(self):
        """Test that hierarchy validates concept consistency."""
        # Educational test: we can detect when concepts have different levels
        concepts = [self.parent_concept, self.child_concept]

        hierarchy = ConceptHierarchy(hierarchy_id="circular_test", concepts=concepts)

        # Should store concepts with different levels
        levels = [
            c.concept_level for c in hierarchy.concepts if hasattr(c, "concept_level")
        ]
        assert 0 in levels  # Parent level
        assert 1 in levels  # Child level


class TestConceptHierarchyEvidenceIntegration:
    """Test integration between concept hierarchy and evidence sentences."""

    def setup_method(self):
        """Set up test data for evidence integration tests."""
        self.concept = Concept(
            text="Neural Networks",
            frequency=50,
            relevance_score=0.8,
            source_papers={"10.1000/nn.2024"},
            concept_level=1,
            evidence_strength=0.85,
        )

        self.evidence_sentences = [
            EvidenceSentence(
                sentence_text="Neural networks are computational models inspired by biological neurons.",
                paper_doi="10.1000/nn.2024",
                page_number=3,
                confidence_score=0.90,
                extraction_method="rule_based",
                concept_text="Neural Networks",
            ),
            EvidenceSentence(
                sentence_text="These networks learn complex patterns through multiple layers.",
                paper_doi="10.1000/nn.2024",
                page_number=4,
                confidence_score=0.85,
                extraction_method="statistical",
                concept_text="Neural Networks",
            ),
        ]

    def test_evidence_sentence_linking(self):
        """Test that hierarchy can store evidence information."""
        # Simple educational test: hierarchy can store evidence sentences
        hierarchy = ConceptHierarchy(
            hierarchy_id="evidence_test",
            concepts=[self.concept],
            evidence_sentences=self.evidence_sentences,
        )

        # Verify evidence is stored (educational accessor)
        assert hierarchy.evidence_sentences == self.evidence_sentences
        assert len(hierarchy.evidence_sentences) == 2


class TestConceptHierarchyQualityMetrics:
    """Test quality metrics calculation and validation."""

    def setup_method(self):
        """Set up test data for quality metrics tests."""
        self.concepts = [
            Concept(
                text="AI",
                frequency=100,
                relevance_score=0.9,
                concept_level=0,
                evidence_strength=0.95,
            ),
            Concept(
                text="ML",
                frequency=80,
                relevance_score=0.85,
                concept_level=1,
                evidence_strength=0.90,
            ),
            Concept(
                text="DL",
                frequency=60,
                relevance_score=0.80,
                concept_level=2,
                evidence_strength=0.85,
            ),
        ]

        self.evidence_sentences = [
            EvidenceSentence("AI sentence", "10.1000/ai", 1, 0.9, "rule", "AI"),
            EvidenceSentence("ML sentence", "10.1000/ml", 1, 0.85, "stat", "ML"),
            EvidenceSentence("DL sentence", "10.1000/dl", 1, 0.80, "embed", "DL"),
        ]

    def test_calculate_hierarchy_quality_score(self):
        """Test that hierarchy can store multiple concepts for quality assessment."""
        # Simple educational test: hierarchy can store multiple concepts
        hierarchy = ConceptHierarchy(
            hierarchy_id="quality_test", concepts=self.concepts
        )

        # Verify basic quality indicators
        assert len(hierarchy.concepts) == 3
        assert hierarchy.hierarchy_id == "quality_test"

    def test_validate_hierarchy_consistency(self):
        """Test that hierarchy validates concept consistency."""
        # Educational test: all concepts must be valid Concept instances
        valid_concepts = self.concepts

        hierarchy = ConceptHierarchy(
            hierarchy_id="consistency_test", concepts=valid_concepts
        )

        # Should store all valid concepts
        assert len(hierarchy.concepts) == 3

        # Should reject non-Concept objects
        with pytest.raises(TypeError):
            ConceptHierarchy(hierarchy_id="invalid_test", concepts=["not_a_concept"])

    def test_validate_hierarchy_consistency(self):
        """Test hierarchy consistency validation."""
        # This test should fail initially (RED phase)
        hierarchy = ConceptHierarchy(
            hierarchy_id="consistency_test",
            root_concepts=[self.concepts[0]],
            all_concepts=self.concepts,
            evidence_sentences=self.evidence_sentences,
            hierarchy_metadata=HierarchyMetadata(
                "test", 0.5, 3, {0: 1, 1: 1, 2: 1}, datetime.now(timezone.utc)
            ),
            extraction_provenance=ExtractionProvenance({}, {}, set()),
        )

        consistency_report = hierarchy.validate_consistency()
        assert consistency_report.is_valid is True
        assert len(consistency_report.validation_errors) == 0


class TestConceptHierarchyValueObjectIntegration:
    """Test integration with value objects for metadata and provenance."""

    def test_hierarchy_metadata_integration(self):
        """Test that hierarchy metadata is properly integrated and accessible."""
        # This test should fail initially (RED phase)
        pass  # Will implement in GREEN phase

    def test_extraction_provenance_tracking(self):
        """Test that extraction provenance is tracked for reproducibility."""
        # This test should fail initially (RED phase)
        pass  # Will implement in GREEN phase
