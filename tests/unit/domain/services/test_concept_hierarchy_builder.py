"""
Tests for ConceptHierarchyBuilder domain service.

This test suite validates the ConceptHierarchyBuilder service that constructs
hierarchical relationships between concepts using semantic analysis and
evidence-based grounding.

Educational Notes:
- Tests domain service pattern for complex business logic
- Demonstrates semantic similarity-based hierarchy construction
- Shows evidence-based concept grounding for research applications
- Validates clustering algorithms for knowledge organization
- Tests immutability preservation in hierarchy operations

Architecture Notes:
- Domain service operates only on domain entities (Concept)
- No infrastructure dependencies (follows Clean Architecture)
- Business logic for concept relationship detection
- Configurable algorithms for different research domains
"""

import pytest
import numpy as np
from typing import List, Dict, Set
from unittest.mock import Mock

from src.domain.entities.concept import Concept
from src.domain.value_objects.embedding_vector import EmbeddingVector
from src.domain.services.concept_hierarchy_builder import ConceptHierarchyBuilder


class TestConceptHierarchyBuilder:
    """Tests for basic concept hierarchy construction."""

    def test_create_hierarchy_builder_with_default_config(self):
        """Test creating hierarchy builder with default configuration."""
        builder = ConceptHierarchyBuilder()

        assert builder.similarity_threshold == 0.7
        assert builder.parent_child_threshold == 0.6
        assert builder.cluster_threshold == 0.8
        assert builder.evidence_weight_factor == 0.1

    def test_create_hierarchy_builder_with_custom_config(self):
        """Test creating hierarchy builder with custom thresholds."""
        builder = ConceptHierarchyBuilder(
            similarity_threshold=0.75,
            parent_child_threshold=0.65,
            cluster_threshold=0.85,
            evidence_weight_factor=0.15,
        )

        assert builder.similarity_threshold == 0.75
        assert builder.parent_child_threshold == 0.65
        assert builder.cluster_threshold == 0.85
        assert builder.evidence_weight_factor == 0.15

    def test_build_hierarchy_from_flat_concept_list(self):
        """Test building hierarchy from flat list of concepts with embeddings."""
        # Create test concepts with embeddings representing different specificity levels
        general_vector = np.array([1.0, 0.0, 0.0, 0.0])  # Medicine
        specific_vector = np.array(
            [0.9, 0.1, 0.0, 0.0]
        )  # Cardiology (similar to medicine)
        very_specific_vector = np.array(
            [0.85, 0.15, 0.0, 0.0]
        )  # Heart surgery (similar to cardiology)

        concepts = [
            Concept(
                text="medicine",
                frequency=100,
                relevance_score=0.9,
                embedding=EmbeddingVector(general_vector),
            ),
            Concept(
                text="cardiology",
                frequency=50,
                relevance_score=0.8,
                embedding=EmbeddingVector(specific_vector),
            ),
            Concept(
                text="heart surgery",
                frequency=20,
                relevance_score=0.7,
                embedding=EmbeddingVector(very_specific_vector),
            ),
        ]

        builder = ConceptHierarchyBuilder()
        hierarchical_concepts = builder.build_hierarchy(concepts)

        # Find concepts by text for testing
        medicine_concept = next(
            c for c in hierarchical_concepts if c.text == "medicine"
        )
        cardiology_concept = next(
            c for c in hierarchical_concepts if c.text == "cardiology"
        )
        surgery_concept = next(
            c for c in hierarchical_concepts if c.text == "heart surgery"
        )

        # Verify hierarchy structure
        assert medicine_concept.is_root_concept()
        assert medicine_concept.concept_level == 0
        assert "cardiology" in medicine_concept.child_concepts

        assert (
            not cardiology_concept.is_root_concept()
            and not cardiology_concept.is_leaf_concept()
        )
        assert cardiology_concept.concept_level == 1
        assert "medicine" in cardiology_concept.parent_concepts
        assert "heart surgery" in cardiology_concept.child_concepts

        assert surgery_concept.is_leaf_concept()
        assert surgery_concept.concept_level == 2
        assert "cardiology" in surgery_concept.parent_concepts

    def test_build_hierarchy_handles_concepts_without_embeddings(self):
        """Test hierarchy building gracefully handles concepts without embeddings."""
        concepts = [
            Concept(
                text="concept without embedding", frequency=10, relevance_score=0.5
            ),
            Concept(
                text="concept with embedding",
                frequency=15,
                relevance_score=0.6,
                embedding=EmbeddingVector(np.array([0.1, 0.2, 0.3])),
            ),
        ]

        builder = ConceptHierarchyBuilder()
        hierarchical_concepts = builder.build_hierarchy(concepts)

        # Should return concepts unchanged when no relationships can be determined
        assert len(hierarchical_concepts) == 2
        for concept in hierarchical_concepts:
            assert concept.is_root_concept()  # No relationships established
            assert concept.concept_level == 0

    def test_build_hierarchy_prevents_circular_relationships(self):
        """Test that hierarchy building prevents circular parent-child relationships."""
        # Create concepts that might create circular relationships
        vector_a = np.array([1.0, 0.0])
        vector_b = np.array([0.0, 1.0])

        concepts = [
            Concept(
                text="concept a",
                frequency=10,
                relevance_score=0.5,
                embedding=EmbeddingVector(vector_a),
                parent_concepts={"concept b"},  # Pre-existing relationship
            ),
            Concept(
                text="concept b",
                frequency=10,
                relevance_score=0.5,
                embedding=EmbeddingVector(vector_b),
            ),
        ]

        builder = ConceptHierarchyBuilder()
        hierarchical_concepts = builder.build_hierarchy(concepts)

        # Should not create circular relationships
        concept_a = next(c for c in hierarchical_concepts if c.text == "concept a")
        concept_b = next(c for c in hierarchical_concepts if c.text == "concept b")

        # One should be parent, other child, but not both
        if "concept b" in concept_a.parent_concepts:
            assert "concept a" not in concept_b.parent_concepts
        if "concept a" in concept_b.parent_concepts:
            assert "concept b" not in concept_a.parent_concepts


class TestSemanticSimilarityAnalysis:
    """Tests for semantic similarity calculations."""

    def test_calculate_semantic_similarity_with_embeddings(self):
        """Test calculating cosine similarity between concept embeddings."""
        concept1 = Concept(
            text="heart rate variability",
            frequency=10,
            relevance_score=0.7,
            embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0])),
        )
        concept2 = Concept(
            text="cardiac monitoring",
            frequency=8,
            relevance_score=0.6,
            embedding=EmbeddingVector(np.array([0.8, 0.6, 0.0])),
        )

        builder = ConceptHierarchyBuilder()
        similarity = builder.calculate_semantic_similarity(concept1, concept2)

        # Should return cosine similarity value between 0 and 1
        assert 0.0 <= similarity <= 1.0
        # Specific expected value based on vectors above
        expected = 0.8  # cos(θ) for these vectors
        assert abs(similarity - expected) < 0.01

    def test_calculate_semantic_similarity_without_embeddings_returns_zero(self):
        """Test similarity calculation returns 0 when embeddings are missing."""
        concept1 = Concept(
            text="concept without embedding", frequency=5, relevance_score=0.5
        )
        concept2 = Concept(
            text="concept with embedding",
            frequency=3,
            relevance_score=0.4,
            embedding=EmbeddingVector(np.array([0.1, 0.2, 0.3])),
        )

        builder = ConceptHierarchyBuilder()
        similarity = builder.calculate_semantic_similarity(concept1, concept2)

        assert similarity == 0.0

    def test_calculate_semantic_similarity_identical_concepts(self):
        """Test similarity calculation for identical concept embeddings."""
        vector = np.array([0.5, 0.5, 0.5, 0.5])
        concept = Concept(
            text="test concept",
            frequency=10,
            relevance_score=0.8,
            embedding=EmbeddingVector(vector),
        )

        builder = ConceptHierarchyBuilder()
        similarity = builder.calculate_semantic_similarity(concept, concept)

        # Self-similarity should be 1.0
        assert abs(similarity - 1.0) < 0.001


class TestParentChildDetection:
    """Tests for parent-child relationship detection."""

    def test_detect_parent_child_relationships_by_frequency_and_similarity(self):
        """Test detecting parent-child relationships using frequency and similarity heuristics."""
        # Parent: high frequency, general term
        parent_concept = Concept(
            text="cardiovascular disease",
            frequency=100,
            relevance_score=0.9,
            embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0, 0.0])),
        )

        # Child: lower frequency, specific term, similar embedding
        child_concept = Concept(
            text="myocardial infarction",
            frequency=30,
            relevance_score=0.8,
            embedding=EmbeddingVector(np.array([0.9, 0.1, 0.0, 0.0])),
        )

        concepts = [parent_concept, child_concept]
        builder = ConceptHierarchyBuilder()
        relationships = builder.detect_parent_child_relationships(concepts)

        # Should detect parent-child relationship
        assert "cardiovascular disease" in relationships
        assert "myocardial infarction" in relationships["cardiovascular disease"]

    def test_detect_parent_child_relationships_requires_sufficient_similarity(self):
        """Test that parent-child detection requires semantic similarity above threshold."""
        # Concepts with low similarity should not be related
        concept1 = Concept(
            text="heart disease",
            frequency=100,
            relevance_score=0.9,
            embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0])),
        )
        concept2 = Concept(
            text="computer programming",
            frequency=50,
            relevance_score=0.8,
            embedding=EmbeddingVector(np.array([0.0, 1.0, 0.0])),
        )

        concepts = [concept1, concept2]
        builder = ConceptHierarchyBuilder()
        relationships = builder.detect_parent_child_relationships(concepts)

        # Should not detect relationships for dissimilar concepts
        assert len(relationships) == 0

    def test_detect_parent_child_relationships_frequency_heuristic(self):
        """Test that higher frequency concepts become parents of lower frequency ones."""
        high_freq_concept = Concept(
            text="medicine",
            frequency=200,
            relevance_score=0.9,
            embedding=EmbeddingVector(np.array([1.0, 0.0])),
        )
        low_freq_concept = Concept(
            text="pediatric cardiology",
            frequency=5,
            relevance_score=0.7,
            embedding=EmbeddingVector(np.array([0.9, 0.1])),
        )

        concepts = [low_freq_concept, high_freq_concept]  # Order shouldn't matter
        builder = ConceptHierarchyBuilder()
        relationships = builder.detect_parent_child_relationships(concepts)

        # High frequency should be parent of low frequency
        assert "medicine" in relationships
        assert "pediatric cardiology" in relationships["medicine"]


class TestConceptLevelAssignment:
    """Tests for hierarchical level assignment."""

    def test_assign_concept_levels_from_relationships(self):
        """Test assigning concept levels based on parent-child relationships."""
        relationships = {
            "medicine": {"cardiology", "neurology"},
            "cardiology": {"heart surgery"},
            "neurology": {"brain surgery"},
        }

        concepts = [
            Concept(text="medicine", frequency=100, relevance_score=0.9),
            Concept(text="cardiology", frequency=50, relevance_score=0.8),
            Concept(text="neurology", frequency=45, relevance_score=0.8),
            Concept(text="heart surgery", frequency=20, relevance_score=0.7),
            Concept(text="brain surgery", frequency=15, relevance_score=0.7),
        ]

        builder = ConceptHierarchyBuilder()
        levels = builder.assign_concept_levels(concepts, relationships)

        # Check level assignments
        assert levels["medicine"] == 0  # Root
        assert levels["cardiology"] == 1  # Child of root
        assert levels["neurology"] == 1  # Child of root
        assert levels["heart surgery"] == 2  # Grandchild
        assert levels["brain surgery"] == 2  # Grandchild

    def test_assign_concept_levels_handles_disconnected_concepts(self):
        """Test level assignment for concepts not in any relationships."""
        relationships = {
            "parent": {"child"},
        }

        concepts = [
            Concept(text="parent", frequency=50, relevance_score=0.8),
            Concept(text="child", frequency=30, relevance_score=0.7),
            Concept(text="unrelated", frequency=20, relevance_score=0.6),
        ]

        builder = ConceptHierarchyBuilder()
        levels = builder.assign_concept_levels(concepts, relationships)

        # Connected concepts get proper levels
        assert levels["parent"] == 0
        assert levels["child"] == 1

        # Unrelated concept becomes root
        assert levels["unrelated"] == 0


class TestConceptClustering:
    """Tests for semantic concept clustering."""

    def test_create_concept_clusters_from_similarity(self):
        """Test creating concept clusters based on embedding similarity."""
        # Create concepts with similar embeddings for clustering
        concepts = [
            Concept(
                text="heart attack",
                frequency=30,
                relevance_score=0.8,
                embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0])),
            ),
            Concept(
                text="myocardial infarction",
                frequency=25,
                relevance_score=0.8,
                embedding=EmbeddingVector(np.array([0.95, 0.05, 0.0])),
            ),
            Concept(
                text="cardiac arrest",
                frequency=20,
                relevance_score=0.7,
                embedding=EmbeddingVector(np.array([0.9, 0.1, 0.0])),
            ),
            Concept(
                text="computer virus",  # Unrelated concept
                frequency=15,
                relevance_score=0.6,
                embedding=EmbeddingVector(np.array([0.0, 0.0, 1.0])),
            ),
        ]

        builder = ConceptHierarchyBuilder()
        clusters = builder.create_concept_clusters(concepts)

        # Cardiac concepts should be clustered together
        cardiac_concepts = {"heart attack", "myocardial infarction", "cardiac arrest"}
        cardiac_cluster_ids = {
            clusters[concept] for concept in cardiac_concepts if concept in clusters
        }

        # All cardiac concepts should have the same cluster ID
        assert len(cardiac_cluster_ids) == 1

        # Computer virus should be in different cluster or unassigned
        if "computer virus" in clusters:
            assert clusters["computer virus"] not in cardiac_cluster_ids

    def test_create_concept_clusters_requires_minimum_similarity(self):
        """Test that clustering requires minimum similarity threshold."""
        # Concepts with low similarity should not be clustered
        concepts = [
            Concept(
                text="concept a",
                frequency=10,
                relevance_score=0.5,
                embedding=EmbeddingVector(np.array([1.0, 0.0])),
            ),
            Concept(
                text="concept b",
                frequency=10,
                relevance_score=0.5,
                embedding=EmbeddingVector(np.array([0.0, 1.0])),
            ),
        ]

        builder = ConceptHierarchyBuilder(cluster_threshold=0.9)  # High threshold
        clusters = builder.create_concept_clusters(concepts)

        # No clusters should be formed due to low similarity
        assert len(clusters) == 0


class TestEvidenceStrengthCalculation:
    """Tests for evidence-based concept grounding."""

    def test_calculate_evidence_strength_from_frequency_and_relevance(self):
        """Test calculating evidence strength from concept metadata."""
        concept = Concept(
            text="well supported concept",
            frequency=50,
            relevance_score=0.9,
            source_papers={"paper1", "paper2", "paper3"},
        )

        builder = ConceptHierarchyBuilder()
        evidence_strength = builder.calculate_evidence_strength(
            concept,
            source_text="This is sample source text containing well supported concept multiple times.",
        )

        # Should return value between 0.0 and 1.0
        assert 0.0 <= evidence_strength <= 1.0

        # Higher frequency and relevance should result in higher evidence
        assert evidence_strength > 0.5

    def test_calculate_evidence_strength_with_low_support(self):
        """Test evidence strength calculation for poorly supported concepts."""
        concept = Concept(
            text="weakly supported concept",
            frequency=1,
            relevance_score=0.2,
            source_papers={"paper1"},
        )

        builder = ConceptHierarchyBuilder()
        evidence_strength = builder.calculate_evidence_strength(
            concept, source_text="Brief mention of concept."
        )

        # Should return lower evidence strength
        assert 0.0 <= evidence_strength <= 1.0
        assert evidence_strength < 0.5

    def test_calculate_evidence_strength_handles_missing_source_text(self):
        """Test evidence calculation when source text is not provided."""
        concept = Concept(
            text="test concept",
            frequency=10,
            relevance_score=0.7,
        )

        builder = ConceptHierarchyBuilder()
        evidence_strength = builder.calculate_evidence_strength(concept, source_text="")

        # Should fall back to frequency and relevance only
        assert 0.0 <= evidence_strength <= 1.0


class TestConceptHierarchyBuilderIntegration:
    """Integration tests for the complete hierarchy building process."""

    def test_complete_hierarchy_building_workflow(self):
        """Test the complete workflow from flat concepts to hierarchical structure."""
        # Create a realistic set of medical concepts with embeddings
        concepts = [
            Concept(
                text="medicine",
                frequency=200,
                relevance_score=0.95,
                embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0, 0.0, 0.0])),
            ),
            Concept(
                text="cardiology",
                frequency=80,
                relevance_score=0.9,
                embedding=EmbeddingVector(np.array([0.9, 0.1, 0.0, 0.0, 0.0])),
            ),
            Concept(
                text="heart failure",
                frequency=40,
                relevance_score=0.8,
                embedding=EmbeddingVector(np.array([0.8, 0.2, 0.0, 0.0, 0.0])),
            ),
            Concept(
                text="acute myocardial infarction",
                frequency=15,
                relevance_score=0.75,
                embedding=EmbeddingVector(np.array([0.75, 0.25, 0.0, 0.0, 0.0])),
            ),
            Concept(
                text="neurology",  # Different branch
                frequency=70,
                relevance_score=0.85,
                embedding=EmbeddingVector(np.array([0.0, 0.0, 1.0, 0.0, 0.0])),
            ),
        ]

        builder = ConceptHierarchyBuilder()
        hierarchical_concepts = builder.build_hierarchy(concepts)

        # Verify we got the same number of concepts back
        assert len(hierarchical_concepts) == len(concepts)

        # Verify hierarchy structure was established
        medicine_concept = next(
            c for c in hierarchical_concepts if c.text == "medicine"
        )
        cardiology_concept = next(
            c for c in hierarchical_concepts if c.text == "cardiology"
        )

        # Medicine should be root with cardiology as child
        assert medicine_concept.is_root_concept()
        assert medicine_concept.concept_level == 0
        assert len(medicine_concept.child_concepts) > 0

        # Cardiology should have medicine as parent
        assert not cardiology_concept.is_root_concept()
        assert cardiology_concept.concept_level >= 1
        assert len(cardiology_concept.parent_concepts) > 0

        # All concepts should have evidence strength calculated
        for concept in hierarchical_concepts:
            assert 0.0 <= concept.evidence_strength <= 1.0

    def test_build_hierarchy_preserves_concept_immutability(self):
        """Test that hierarchy building preserves original concept immutability."""
        original_concept = Concept(
            text="original concept",
            frequency=10,
            relevance_score=0.7,
            embedding=EmbeddingVector(np.array([0.1, 0.2, 0.3])),
        )

        builder = ConceptHierarchyBuilder()
        hierarchical_concepts = builder.build_hierarchy([original_concept])

        # Original concept should be unchanged
        assert original_concept.parent_concepts == set()
        assert original_concept.child_concepts == set()
        assert original_concept.concept_level == 0
        assert original_concept.cluster_id is None

        # Result should be different instances
        result_concept = hierarchical_concepts[0]
        assert result_concept is not original_concept
