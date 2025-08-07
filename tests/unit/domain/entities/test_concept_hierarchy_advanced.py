"""
Unit tests for ConceptHierarchy advanced operations.

This test suite validates the sophisticated business logic of the ConceptHierarchy
aggregate root, focusing on advanced operations required for academic research.

Educational Notes - Advanced Domain Testing:
- Tests complex business rules that require deep domain knowledge
- Validates sophisticated algorithms for hierarchy manipulation
- Ensures academic-grade quality and consistency requirements
- Demonstrates testing of aggregate root coordination responsibilities

Educational Notes - TDD Cycle 2 Focus:
- Building on basic domain model from Cycle 1
- Adding sophisticated business operations and validation
- Ensuring system meets academic research quality standards
- Preparing foundation for multi-strategy extraction in Phase 2

Testing Patterns Applied:
- Arrange-Act-Assert pattern for clear test structure
- Given-When-Then scenarios for complex business logic
- Property-based testing for invariant validation
- State-based testing for aggregate root behavior
"""

import pytest
from datetime import datetime, timezone
from typing import List, Dict, Set

from src.domain.entities.concept_hierarchy import ConceptHierarchy
from src.domain.entities.concept import Concept
from src.domain.value_objects.evidence_sentence import EvidenceSentence
from src.domain.value_objects.hierarchy_metadata import HierarchyMetadata
from src.domain.value_objects.extraction_provenance import ExtractionProvenance
from src.domain.common.validation import DomainValidationError


class TestConceptHierarchyAdvancedOperations:
    """
    Test suite for advanced ConceptHierarchy business operations.

    Educational Notes - Aggregate Root Testing:
    - Tests complex coordination between entities and value objects
    - Validates business invariants across the entire aggregate
    - Ensures consistency is maintained during complex operations
    - Demonstrates testing of sophisticated domain logic
    """

    def setup_method(self):
        """Set up test fixtures for advanced hierarchy operations."""
        # Create test concepts with parent-child relationships
        self.root_concept = Concept(
            text="Machine Learning",
            frequency=100,
            relevance_score=0.95,
            concept_level=0,
            evidence_strength=0.9,
            parent_concepts=(),
            child_concepts=("Neural Networks", "Supervised Learning"),
        )

        self.child_concept_1 = Concept(
            text="Neural Networks",
            frequency=80,
            relevance_score=0.88,
            concept_level=1,
            evidence_strength=0.85,
            parent_concepts=("Machine Learning",),
            child_concepts=("Deep Learning",),  # Only reference existing child
        )

        self.child_concept_2 = Concept(
            text="Supervised Learning",
            frequency=75,
            relevance_score=0.82,
            concept_level=1,
            evidence_strength=0.80,
            parent_concepts=("Machine Learning",),
            child_concepts=(),  # No children to keep it simple
        )

        self.grandchild_concept = Concept(
            text="Deep Learning",
            frequency=60,
            relevance_score=0.90,
            concept_level=2,
            evidence_strength=0.92,
            parent_concepts=("Neural Networks",),
            child_concepts=(),
        )

        # Create test evidence sentences
        self.evidence_sentences = [
            EvidenceSentence(
                sentence_text="Machine learning algorithms are fundamental to AI.",
                paper_doi="10.1000/ml.2024",
                page_number=1,
                confidence_score=0.95,
                extraction_method="statistical",
                concept_text="Machine Learning",
            ),
            EvidenceSentence(
                sentence_text="Neural networks mimic biological neural structures.",
                paper_doi="10.1000/nn.2024",
                page_number=3,
                confidence_score=0.88,
                extraction_method="embedding_based",
                concept_text="Neural Networks",
            ),
        ]

        # Create test hierarchy
        self.test_hierarchy = ConceptHierarchy.create_from_extraction_results(
            concepts=[
                self.root_concept,
                self.child_concept_1,
                self.child_concept_2,
                self.grandchild_concept,
            ],
            evidence_sentences=self.evidence_sentences,
            extraction_method="test_extraction",
            extraction_parameters={"threshold": 0.8},
        )

    def test_validate_hierarchy_consistency(self):
        """Test that hierarchy validates parent-child relationship consistency."""
        # This test should fail initially (RED phase)
        # ConceptHierarchy should have method to validate all relationships are bidirectional

        # Test valid hierarchy passes validation
        assert self.test_hierarchy.validate_hierarchy_consistency() == True

        # Test that inconsistent relationships are detected
        inconsistent_concept = Concept(
            text="Orphaned Concept",
            frequency=20,
            relevance_score=0.5,
            concept_level=1,
            evidence_strength=0.6,
            parent_concepts=("Non-Existent Parent",),  # Parent doesn't exist
            child_concepts=(),
        )

        with pytest.raises(
            ValueError,  # Changed from DomainValidationError to ValueError
            match="Parent concept 'Non-Existent Parent' not found in hierarchy",
        ):
            self.test_hierarchy.add_concept(inconsistent_concept)

    def test_detect_circular_dependencies(self):
        """Test that circular dependencies in concept relationships are detected."""
        # This test should fail initially (RED phase)

        # Create concepts that would form a circular dependency
        # First, add both concepts without circular references
        concept_a = Concept(
            text="Concept A",
            frequency=50,
            relevance_score=0.7,
            concept_level=1,
            evidence_strength=0.7,
            parent_concepts=(),
            child_concepts=("Concept B",),
        )

        concept_b = Concept(
            text="Concept B",
            frequency=50,
            relevance_score=0.7,
            concept_level=2,
            evidence_strength=0.7,
            parent_concepts=("Concept A",),
            child_concepts=(),  # Start without circular reference
        )

        # Use factory method to bypass individual add_concept validation
        # This simulates what could happen with bulk import or corrupted data
        hierarchy = ConceptHierarchy.create_from_extraction_results(
            concepts=[concept_a, concept_b],
            evidence_sentences=[],
            extraction_method="test_circular",
            extraction_parameters={},
        )

        # Now manually create the circular reference by modifying the hierarchy directly
        # This simulates data corruption or import issues
        circular_concept_b = Concept(
            text="Concept B",
            frequency=50,
            relevance_score=0.7,
            concept_level=2,
            evidence_strength=0.7,
            parent_concepts=("Concept A",),
            child_concepts=("Concept A",),  # This creates a cycle
        )

        # Directly modify the hierarchy to create circular reference
        hierarchy.concepts["Concept B"] = circular_concept_b

        # Now test that circular dependencies are detected
        cycles = hierarchy.detect_circular_dependencies()
        assert len(cycles) > 0, "Should detect circular dependency"

        # Test hierarchy without circular dependencies
        clean_hierarchy = self.test_hierarchy
        clean_cycles = clean_hierarchy.detect_circular_dependencies()
        assert len(clean_cycles) == 0, "Clean hierarchy should have no cycles"

    def test_calculate_hierarchy_quality_score(self):
        """Test comprehensive hierarchy quality assessment."""
        # This test should fail initially (RED phase)

        quality_score = self.test_hierarchy.calculate_hierarchy_quality_score()

        # Quality score should be between 0.0 and 1.0
        assert 0.0 <= quality_score <= 1.0

        # Quality score should be meaningful (not just 0 or 1)
        assert (
            quality_score > 0.0
        ), "Quality score should reflect actual hierarchy quality"

    def test_find_concept_path(self):
        """Test finding navigation paths between concepts in hierarchy."""
        # This test should fail initially (RED phase)

        # Test path from root to leaf concept
        path = self.test_hierarchy.find_concept_path(
            "Machine Learning", "Deep Learning"
        )
        expected_path = ["Machine Learning", "Neural Networks", "Deep Learning"]
        assert path == expected_path

        # Test path between sibling concepts (should go through common parent)
        sibling_path = self.test_hierarchy.find_concept_path(
            "Neural Networks", "Supervised Learning"
        )
        expected_sibling_path = [
            "Neural Networks",
            "Machine Learning",
            "Supervised Learning",
        ]
        assert sibling_path == expected_sibling_path

        # Test path to non-existent concept
        with pytest.raises(
            ValueError, match="Concept 'Non-Existent' not found in hierarchy"
        ):
            self.test_hierarchy.find_concept_path("Machine Learning", "Non-Existent")

    def test_get_concept_ancestors(self):
        """Test retrieving all ancestor concepts for a given concept."""
        # This test should fail initially (RED phase)

        ancestors = self.test_hierarchy.get_concept_ancestors("Deep Learning")
        expected_ancestors = ["Neural Networks", "Machine Learning"]
        assert ancestors == expected_ancestors

        # Root concept should have no ancestors
        root_ancestors = self.test_hierarchy.get_concept_ancestors("Machine Learning")
        assert root_ancestors == []

        # Test with non-existent concept
        with pytest.raises(ValueError, match="Concept 'Non-Existent' not found"):
            self.test_hierarchy.get_concept_ancestors("Non-Existent")

    def test_get_concept_descendants(self):
        """Test retrieving all descendant concepts for a given concept."""
        # This test should fail initially (RED phase)

        descendants = self.test_hierarchy.get_concept_descendants("Machine Learning")
        expected_descendants = {
            "Neural Networks",
            "Supervised Learning",
            "Deep Learning",
            "CNNs",
            "Classification",
            "Regression",
        }
        assert set(descendants) == expected_descendants

        # Leaf concept should have no descendants
        leaf_descendants = self.test_hierarchy.get_concept_descendants("Deep Learning")
        assert leaf_descendants == []

    def test_rebalance_hierarchy(self):
        """Test automatic hierarchy rebalancing for optimal structure."""
        # This test should fail initially (RED phase)

        # Create an unbalanced hierarchy (too deep on one side)
        unbalanced_hierarchy = self._create_unbalanced_hierarchy()

        original_balance_score = unbalanced_hierarchy.calculate_balance_score()

        # Rebalance the hierarchy
        rebalanced_hierarchy = unbalanced_hierarchy.rebalance_hierarchy()

        # Rebalanced hierarchy should have better balance score
        new_balance_score = rebalanced_hierarchy.calculate_balance_score()
        assert new_balance_score > original_balance_score

        # Should maintain all original concepts
        assert len(rebalanced_hierarchy.concepts) == len(unbalanced_hierarchy.concepts)

        # Should preserve concept relationships (just reorganize structure)
        original_concept_texts = set(unbalanced_hierarchy.concepts.keys())
        rebalanced_concept_texts = set(rebalanced_hierarchy.concepts.keys())
        assert original_concept_texts == rebalanced_concept_texts

    def test_merge_hierarchies(self):
        """Test merging two concept hierarchies while maintaining consistency."""
        # This test should fail initially (RED phase)

        # Create a second hierarchy to merge
        other_hierarchy = self._create_compatible_hierarchy()

        # Merge hierarchies
        merged_hierarchy = self.test_hierarchy.merge_with(other_hierarchy)

        # Merged hierarchy should contain concepts from both
        original_count = len(self.test_hierarchy.concepts)
        other_count = len(other_hierarchy.concepts)

        # May be less than sum due to duplicate concept merging
        assert len(merged_hierarchy.concepts) <= original_count + other_count
        assert len(merged_hierarchy.concepts) >= max(original_count, other_count)

        # Should maintain hierarchy validity
        assert merged_hierarchy.validate_hierarchy_consistency() == True

    def test_split_hierarchy_by_domain(self):
        """Test splitting a large hierarchy into domain-specific sub-hierarchies."""
        # This test should fail initially (RED phase)

        # Create a multi-domain hierarchy
        multi_domain_hierarchy = self._create_multi_domain_hierarchy()

        # Split by domains
        domain_hierarchies = multi_domain_hierarchy.split_by_domain()

        # Should create separate hierarchies for each domain
        assert len(domain_hierarchies) >= 2

        # Each sub-hierarchy should be valid
        for domain, hierarchy in domain_hierarchies.items():
            assert hierarchy.validate_hierarchy_consistency() == True
            assert len(hierarchy.concepts) > 0

        # All original concepts should be preserved across splits
        total_concepts_after_split = sum(
            len(h.concepts) for h in domain_hierarchies.values()
        )
        # May have some duplication for bridging concepts
        assert total_concepts_after_split >= len(multi_domain_hierarchy.concepts)

    def test_prune_low_quality_concepts(self):
        """Test removing concepts with insufficient evidence or quality."""
        # This test should fail initially (RED phase)

        # Create hierarchy with some low-quality concepts
        hierarchy_with_noise = self._create_hierarchy_with_noise()

        original_count = len(hierarchy_with_noise.concepts)

        # Prune concepts below quality threshold
        pruned_hierarchy = hierarchy_with_noise.prune_low_quality_concepts(
            min_evidence_score=0.7, min_relevance_score=0.6
        )

        # Should have fewer concepts after pruning
        assert len(pruned_hierarchy.concepts) < original_count

        # Remaining concepts should meet quality criteria
        for concept in pruned_hierarchy.concepts.values():
            assert concept.evidence_strength >= 0.7
            assert concept.relevance_score >= 0.6

        # Should maintain hierarchy validity after pruning
        assert pruned_hierarchy.validate_hierarchy_consistency() == True

    def _create_unbalanced_hierarchy(self) -> ConceptHierarchy:
        """Helper method to create an unbalanced hierarchy for testing."""
        # Implementation will be added in GREEN phase
        pass

    def _create_compatible_hierarchy(self) -> ConceptHierarchy:
        """Helper method to create a hierarchy compatible for merging."""
        # Implementation will be added in GREEN phase
        pass

    def _create_multi_domain_hierarchy(self) -> ConceptHierarchy:
        """Helper method to create a hierarchy spanning multiple domains."""
        # Implementation will be added in GREEN phase
        pass

    def _create_hierarchy_with_noise(self) -> ConceptHierarchy:
        """Helper method to create a hierarchy with low-quality concepts."""
        # Implementation will be added in GREEN phase
        pass


class TestConceptHierarchyNavigationOperations:
    """
    Test suite for concept hierarchy navigation and traversal operations.

    Educational Notes - Tree Traversal Algorithms:
    - Tests depth-first and breadth-first traversal strategies
    - Validates path-finding algorithms in directed acyclic graphs
    - Ensures efficient navigation for large hierarchies
    - Demonstrates graph algorithm implementation in domain context
    """

    def setup_method(self):
        """Set up test fixtures for navigation testing."""
        # Create a more complex hierarchy for navigation testing
        self.complex_hierarchy = self._create_complex_test_hierarchy()

    def test_depth_first_traversal(self):
        """Test depth-first traversal of concept hierarchy."""
        # This test should fail initially (RED phase)

        traversal_order = self.complex_hierarchy.traverse_depth_first("Root Concept")

        # Should visit all reachable concepts
        assert len(traversal_order) > 0

        # Should start with the specified root
        assert traversal_order[0] == "Root Concept"

        # Should visit children before siblings (depth-first property)
        self._validate_depth_first_order(traversal_order)

    def test_breadth_first_traversal(self):
        """Test breadth-first traversal of concept hierarchy."""
        # This test should fail initially (RED phase)

        traversal_order = self.complex_hierarchy.traverse_breadth_first("Root Concept")

        # Should visit all reachable concepts
        assert len(traversal_order) > 0

        # Should start with specified root
        assert traversal_order[0] == "Root Concept"

        # Should visit all concepts at level N before any at level N+1
        self._validate_breadth_first_order(traversal_order)

    def test_find_shortest_path(self):
        """Test finding shortest path between any two concepts."""
        # This test should fail initially (RED phase)

        shortest_path = self.complex_hierarchy.find_shortest_path(
            "Root Concept", "Deep Leaf Concept"
        )

        # Path should exist and be non-empty
        assert len(shortest_path) > 0
        assert shortest_path[0] == "Root Concept"
        assert shortest_path[-1] == "Deep Leaf Concept"

        # Should be the actual shortest path (verify by comparing with all possible paths)
        all_paths = self.complex_hierarchy.find_all_paths(
            "Root Concept", "Deep Leaf Concept"
        )
        assert len(shortest_path) == min(len(path) for path in all_paths)

    def _create_complex_test_hierarchy(self) -> ConceptHierarchy:
        """Helper method to create complex hierarchy for navigation testing."""
        # Implementation will be added in GREEN phase
        pass

    def _validate_depth_first_order(self, traversal_order: List[str]) -> None:
        """Helper method to validate depth-first traversal order."""
        # Implementation will be added in GREEN phase
        pass

    def _validate_breadth_first_order(self, traversal_order: List[str]) -> None:
        """Helper method to validate breadth-first traversal order."""
        # Implementation will be added in GREEN phase
        pass
