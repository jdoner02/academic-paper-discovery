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
        # Create empty hierarchy first
        hierarchy = ConceptHierarchy()

        # Add root concept
        hierarchy.add_concept(self.root_concept)

        # Update child concept to include the parent-child relationship
        # and add it to root concept
        root_with_child = Concept(
            text="Machine Learning",
            frequency=100,
            relevance_score=0.9,
            source_papers={"10.1000/ml.2024"},
            concept_level=0,
            evidence_strength=0.95,
            child_concepts={"Deep Learning"},
        )

        # Replace the root concept with updated version
        hierarchy.concepts[self.root_concept.text] = root_with_child

        # Now add the child concept
        hierarchy.add_concept(self.child_concept)

        assert hierarchy.hierarchy_id is not None
        assert len(hierarchy.concepts) == 2
        assert "Machine Learning" in hierarchy.concepts
        assert "Deep Learning" in hierarchy.concepts

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
        # This test should fail initially (RED phase)
        invalid_root = Concept(
            text="Invalid Root",
            frequency=10,
            relevance_score=0.5,
            concept_level=1,  # Root concepts should have level 0
            evidence_strength=0.7,
        )

        with pytest.raises(
            ValueError, match="Root concepts must have concept_level = 0"
        ):
            ConceptHierarchy(
                hierarchy_id="invalid_hierarchy",
                root_concepts=[invalid_root],
                all_concepts=[invalid_root],
                evidence_sentences=[],
                hierarchy_metadata=self.hierarchy_metadata,
                extraction_provenance=self.extraction_provenance,
            )


class TestConceptHierarchyRelationships:
    """Test concept hierarchy relationship management and integrity."""

    def setup_method(self):
        """Set up test data for relationship tests."""
        self.setup_test_hierarchy()

    def setup_test_hierarchy(self):
        """Create a more complex test hierarchy for relationship testing."""
        # Machine Learning (root)
        # ├── Deep Learning
        # │   ├── Convolutional Neural Networks
        # │   └── Recurrent Neural Networks
        # └── Traditional ML
        #     ├── Decision Trees
        #     └── Support Vector Machines

        self.concepts = {
            "Machine Learning": Concept(
                text="Machine Learning",
                frequency=100,
                relevance_score=0.9,
                concept_level=0,
                evidence_strength=0.95,
            ),
            "Deep Learning": Concept(
                text="Deep Learning",
                frequency=60,
                relevance_score=0.85,
                parent_concepts={"Machine Learning"},
                concept_level=1,
                evidence_strength=0.90,
            ),
            "Traditional ML": Concept(
                text="Traditional ML",
                frequency=40,
                relevance_score=0.80,
                parent_concepts={"Machine Learning"},
                concept_level=1,
                evidence_strength=0.85,
            ),
            "Convolutional Neural Networks": Concept(
                text="Convolutional Neural Networks",
                frequency=30,
                relevance_score=0.75,
                parent_concepts={"Deep Learning"},
                concept_level=2,
                evidence_strength=0.80,
            ),
            "Recurrent Neural Networks": Concept(
                text="Recurrent Neural Networks",
                frequency=25,
                relevance_score=0.70,
                parent_concepts={"Deep Learning"},
                concept_level=2,
                evidence_strength=0.78,
            ),
        }

        self.hierarchy_metadata = HierarchyMetadata(
            clustering_algorithm="agglomerative",
            similarity_threshold=0.75,
            hierarchy_depth=3,
            concept_count_by_level={0: 1, 1: 2, 2: 2},
            extraction_timestamp=datetime.now(timezone.utc),
        )

    def test_validate_hierarchy_relationships(self):
        """Test that hierarchy correctly validates parent-child relationships."""
        # This test should fail initially (RED phase)
        hierarchy = ConceptHierarchy(
            hierarchy_id="relationship_test",
            root_concepts=[self.concepts["Machine Learning"]],
            all_concepts=list(self.concepts.values()),
            evidence_sentences=[],
            hierarchy_metadata=self.hierarchy_metadata,
            extraction_provenance=ExtractionProvenance({}, {}, set()),
        )

        # Should correctly identify children of Machine Learning
        ml_children = hierarchy.get_children_of_concept("Machine Learning")
        assert len(ml_children) == 2
        assert "Deep Learning" in [c.text for c in ml_children]
        assert "Traditional ML" in [c.text for c in ml_children]

        # Should correctly identify parent of Deep Learning
        dl_parent = hierarchy.get_parent_of_concept("Deep Learning")
        assert dl_parent is not None
        assert dl_parent.text == "Machine Learning"

    def test_prevent_circular_relationships(self):
        """Test that hierarchy prevents circular parent-child relationships."""
        # This test should fail initially (RED phase)
        circular_concepts = [
            Concept(
                text="Concept A",
                frequency=10,
                relevance_score=0.5,
                parent_concepts={"Concept B"},  # Creates circular dependency
                concept_level=1,
            ),
            Concept(
                text="Concept B",
                frequency=10,
                relevance_score=0.5,
                parent_concepts={"Concept A"},  # Creates circular dependency
                concept_level=1,
            ),
        ]

        with pytest.raises(
            ValueError, match="Circular relationships detected in hierarchy"
        ):
            ConceptHierarchy(
                hierarchy_id="circular_test",
                root_concepts=[],
                all_concepts=circular_concepts,
                evidence_sentences=[],
                hierarchy_metadata=self.hierarchy_metadata,
                extraction_provenance=ExtractionProvenance({}, {}, set()),
            )


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
        """Test that evidence sentences are correctly linked to concepts."""
        # This test should fail initially (RED phase)
        hierarchy = ConceptHierarchy(
            hierarchy_id="evidence_test",
            root_concepts=[self.concept],
            all_concepts=[self.concept],
            evidence_sentences=self.evidence_sentences,
            hierarchy_metadata=HierarchyMetadata(
                "test", 0.5, 1, {0: 1}, datetime.now(timezone.utc)
            ),
            extraction_provenance=ExtractionProvenance({}, {}, {"10.1000/nn.2024"}),
        )

        # Should return evidence sentences for the concept
        concept_evidence = hierarchy.get_evidence_for_concept("Neural Networks")
        assert len(concept_evidence) == 2
        assert all(ev.concept_text == "Neural Networks" for ev in concept_evidence)

        # Should calculate average confidence score
        avg_confidence = hierarchy.get_average_evidence_confidence("Neural Networks")
        assert abs(avg_confidence - 0.875) < 0.001  # (0.90 + 0.85) / 2


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
        """Test calculation of overall hierarchy quality score."""
        # This test should fail initially (RED phase)
        hierarchy = ConceptHierarchy(
            hierarchy_id="quality_test",
            root_concepts=[self.concepts[0]],
            all_concepts=self.concepts,
            evidence_sentences=self.evidence_sentences,
            hierarchy_metadata=HierarchyMetadata(
                "test", 0.5, 3, {0: 1, 1: 1, 2: 1}, datetime.now(timezone.utc)
            ),
            extraction_provenance=ExtractionProvenance({}, {}, set()),
        )

        quality_score = hierarchy.calculate_overall_quality_score()
        assert 0.0 <= quality_score <= 1.0
        assert quality_score > 0.8  # Should be high quality with good evidence

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
