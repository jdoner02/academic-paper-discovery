"""
Tests for Concept entity with semantic embedding capabilities.

This test suite validates the enhanced Concept entity that supports
semantic embeddings for advanced concept analysis and similarity.

Educational Notes:
- Tests both basic concept functionality and new semantic features
- Demonstrates testing strategy for AI/ML enhanced domain objects
- Shows how to test semantic similarity without external dependencies
- Validates backward compatibility with non-embedding concepts
"""

import pytest
import numpy as np
from datetime import datetime, timezone

from src.domain.entities.concept import Concept
from src.domain.value_objects.embedding_vector import EmbeddingVector


class TestConceptCreation:
    """Tests for concept creation and validation."""

    def test_create_basic_concept_without_embedding(self):
        """Test creating concept without semantic embedding (backward compatibility)."""
        concept = Concept(
            text="heart rate variability",
            frequency=5,
            relevance_score=0.85,
            source_papers={"paper1", "paper2"},
            source_domain="medical",
            extraction_method="tfidf",
        )

        assert concept.text == "heart rate variability"
        assert concept.frequency == 5
        assert concept.relevance_score == 0.85
        assert concept.source_papers == {"paper1", "paper2"}
        assert concept.source_domain == "medical"
        assert concept.extraction_method == "tfidf"
        assert concept.embedding is None
        assert not concept.has_semantic_data()

    def test_create_concept_with_embedding(self):
        """Test creating concept with semantic embedding."""
        vector = np.array([0.1, 0.2, 0.3, 0.4])
        embedding = EmbeddingVector(vector)

        concept = Concept(
            text="hrv analysis",
            frequency=3,
            relevance_score=0.75,
            source_papers={"paper3"},
            extraction_method="sentence_transformer",
            embedding=embedding,
        )

        assert concept.text == "hrv analysis"
        assert concept.embedding is not None
        assert concept.has_semantic_data()
        assert np.allclose(concept.embedding.vector, vector)

    def test_reject_empty_concept_text(self):
        """Test validation rejects empty concept text."""
        with pytest.raises(ValueError, match="Concept text cannot be empty"):
            Concept(text="", frequency=1, relevance_score=0.5)

    def test_reject_negative_frequency(self):
        """Test validation rejects negative frequency."""
        with pytest.raises(ValueError, match="Concept frequency cannot be negative"):
            Concept(text="test", frequency=-1, relevance_score=0.5)

    def test_reject_invalid_relevance_score(self):
        """Test validation rejects relevance scores outside [0.0, 1.0]."""
        with pytest.raises(
            ValueError, match="Relevance score must be between 0.0 and 1.0"
        ):
            Concept(text="test", frequency=1, relevance_score=1.5)

    def test_reject_invalid_extraction_method(self):
        """Test validation rejects invalid extraction methods."""
        with pytest.raises(ValueError, match="Invalid extraction method"):
            Concept(
                text="test",
                frequency=1,
                relevance_score=0.5,
                extraction_method="invalid_method",
            )

    def test_valid_extraction_methods(self):
        """Test all valid extraction methods are accepted."""
        valid_methods = [
            "tfidf",
            "named_entity",
            "keyword",
            "transformer",
            "semantic_embedding",
            "sentence_transformer",
            "manual",
            "unknown",
        ]

        for method in valid_methods:
            concept = Concept(
                text="test concept",
                frequency=1,
                relevance_score=0.5,
                extraction_method=method,
            )
            assert concept.extraction_method == method


class TestConceptSemanticSimilarity:
    """Tests for semantic similarity functionality."""

    def test_semantic_similarity_with_embeddings(self):
        """Test semantic similarity calculation between concepts with embeddings."""
        # Create two concepts with similar embeddings
        vector1 = np.array([1.0, 0.0, 0.0])  # Unit vector along x-axis
        vector2 = np.array([0.8, 0.6, 0.0])  # Vector at angle to x-axis

        embedding1 = EmbeddingVector(vector1)
        embedding2 = EmbeddingVector(vector2)

        concept1 = Concept(
            text="heart rate variability",
            frequency=5,
            relevance_score=0.8,
            embedding=embedding1,
        )

        concept2 = Concept(
            text="cardiac variability",
            frequency=3,
            relevance_score=0.7,
            embedding=embedding2,
        )

        similarity = concept1.semantic_similarity(concept2)
        assert similarity is not None
        assert 0.0 <= similarity <= 1.0
        assert similarity == pytest.approx(
            0.8, abs=0.01
        )  # cos(θ) where vectors form specific angle

    def test_semantic_similarity_without_embeddings_returns_none(self):
        """Test semantic similarity returns None when concepts lack embeddings."""
        concept1 = Concept(text="concept1", frequency=1, relevance_score=0.5)
        concept2 = Concept(text="concept2", frequency=1, relevance_score=0.5)

        assert concept1.semantic_similarity(concept2) is None

    def test_semantic_similarity_with_partial_embeddings_returns_none(self):
        """Test semantic similarity returns None when only one concept has embedding."""
        embedding = EmbeddingVector(np.array([1.0, 0.0, 0.0]))
        concept1 = Concept(
            text="concept1", frequency=1, relevance_score=0.5, embedding=embedding
        )
        concept2 = Concept(text="concept2", frequency=1, relevance_score=0.5)

        assert concept1.semantic_similarity(concept2) is None
        assert concept2.semantic_similarity(concept1) is None

    def test_semantic_similarity_rejects_non_concept(self):
        """Test semantic similarity validation rejects non-Concept objects."""
        embedding = EmbeddingVector(np.array([1.0, 0.0]))
        concept = Concept(
            text="test", frequency=1, relevance_score=0.5, embedding=embedding
        )

        with pytest.raises(
            ValueError, match="Can only calculate similarity with another Concept"
        ):
            concept.semantic_similarity("not a concept")

    def test_find_similar_concepts(self):
        """Test finding similar concepts from a collection."""
        # Create base concept
        base_vector = np.array([1.0, 0.0, 0.0])
        base_embedding = EmbeddingVector(base_vector)
        base_concept = Concept(
            text="heart rate variability",
            frequency=5,
            relevance_score=0.8,
            embedding=base_embedding,
        )

        # Create similar concept (high similarity)
        similar_vector = np.array([0.9, 0.436, 0.0])  # ~0.9 cosine similarity
        similar_embedding = EmbeddingVector(similar_vector)
        similar_concept = Concept(
            text="cardiac variability",
            frequency=3,
            relevance_score=0.7,
            embedding=similar_embedding,
        )

        # Create dissimilar concept (low similarity)
        dissimilar_vector = np.array([0.0, 0.0, 1.0])  # 0.0 cosine similarity
        dissimilar_embedding = EmbeddingVector(dissimilar_vector)
        dissimilar_concept = Concept(
            text="quantum computing",
            frequency=2,
            relevance_score=0.6,
            embedding=dissimilar_embedding,
        )

        # Find similar concepts with threshold 0.8
        candidates = [similar_concept, dissimilar_concept]
        similar_results = base_concept.find_similar_concepts(
            candidates, similarity_threshold=0.8
        )

        assert len(similar_results) == 1
        assert similar_results[0][0] == similar_concept
        assert similar_results[0][1] >= 0.8

    def test_find_similar_concepts_excludes_self(self):
        """Test finding similar concepts excludes the concept itself."""
        embedding = EmbeddingVector(np.array([1.0, 0.0]))
        concept = Concept(
            text="test concept", frequency=1, relevance_score=0.5, embedding=embedding
        )

        # Should exclude itself from results
        similar_results = concept.find_similar_concepts(
            [concept], similarity_threshold=0.0
        )
        assert len(similar_results) == 0

    def test_find_similar_concepts_without_embedding_returns_empty(self):
        """Test finding similar concepts returns empty list when base concept has no embedding."""
        concept_without_embedding = Concept(
            text="test", frequency=1, relevance_score=0.5
        )
        concept_with_embedding = Concept(
            text="other",
            frequency=1,
            relevance_score=0.5,
            embedding=EmbeddingVector(np.array([1.0, 0.0])),
        )

        similar_results = concept_without_embedding.find_similar_concepts(
            [concept_with_embedding]
        )
        assert len(similar_results) == 0

    def test_find_similar_concepts_invalid_threshold(self):
        """Test finding similar concepts validates threshold parameter."""
        embedding = EmbeddingVector(np.array([1.0, 0.0]))
        concept = Concept(
            text="test", frequency=1, relevance_score=0.5, embedding=embedding
        )

        with pytest.raises(
            ValueError, match="Similarity threshold must be between 0.0 and 1.0"
        ):
            concept.find_similar_concepts([], similarity_threshold=1.5)

    def test_find_similar_concepts_sorted_by_similarity(self):
        """Test similar concepts are returned sorted by similarity (highest first)."""
        base_embedding = EmbeddingVector(np.array([1.0, 0.0, 0.0]))
        base_concept = Concept(
            text="base", frequency=1, relevance_score=0.5, embedding=base_embedding
        )

        # Create concepts with different similarity levels
        high_sim_embedding = EmbeddingVector(
            np.array([0.95, 0.31, 0.0])
        )  # ~0.95 similarity
        medium_sim_embedding = EmbeddingVector(
            np.array([0.8, 0.6, 0.0])
        )  # ~0.8 similarity
        low_sim_embedding = EmbeddingVector(
            np.array([0.6, 0.8, 0.0])
        )  # ~0.6 similarity

        concepts = [
            Concept(
                text="low",
                frequency=1,
                relevance_score=0.5,
                embedding=low_sim_embedding,
            ),
            Concept(
                text="high",
                frequency=1,
                relevance_score=0.5,
                embedding=high_sim_embedding,
            ),
            Concept(
                text="medium",
                frequency=1,
                relevance_score=0.5,
                embedding=medium_sim_embedding,
            ),
        ]

        similar_results = base_concept.find_similar_concepts(
            concepts, similarity_threshold=0.5
        )

        assert len(similar_results) == 3
        # Should be sorted by similarity (highest first)
        similarities = [score for _, score in similar_results]
        assert similarities == sorted(similarities, reverse=True)
        assert similar_results[0][0].text == "high"
        assert similar_results[1][0].text == "medium"
        assert similar_results[2][0].text == "low"


class TestConceptEmbeddingManagement:
    """Tests for embedding management functionality."""

    def test_add_embedding_to_concept(self):
        """Test adding embedding to an existing concept."""
        concept = Concept(text="test", frequency=1, relevance_score=0.5)
        assert not concept.has_semantic_data()

        embedding = EmbeddingVector(np.array([0.1, 0.2, 0.3]))
        enhanced_concept = concept.add_embedding(embedding)

        assert enhanced_concept.has_semantic_data()
        assert enhanced_concept.embedding == embedding
        assert enhanced_concept.text == concept.text  # Other properties preserved
        assert enhanced_concept.frequency == concept.frequency

    def test_add_embedding_validates_input(self):
        """Test adding embedding validates the embedding parameter."""
        concept = Concept(text="test", frequency=1, relevance_score=0.5)

        with pytest.raises(
            ValueError, match="Embedding must be an EmbeddingVector instance"
        ):
            concept.add_embedding("not an embedding")

    def test_has_semantic_data(self):
        """Test has_semantic_data correctly identifies embedding presence."""
        concept_without = Concept(text="test", frequency=1, relevance_score=0.5)
        concept_with = Concept(
            text="test",
            frequency=1,
            relevance_score=0.5,
            embedding=EmbeddingVector(np.array([1.0, 0.0])),
        )

        assert not concept_without.has_semantic_data()
        assert concept_with.has_semantic_data()


class TestConceptSerialization:
    """Tests for concept serialization with embedding support."""

    def test_serialize_concept_without_embedding(self):
        """Test serializing concept without embedding (backward compatibility)."""
        concept = Concept(
            text="test concept",
            frequency=3,
            relevance_score=0.7,
            source_papers={"paper1", "paper2"},
            source_domain="test_domain",
            extraction_method="tfidf",
        )

        data = concept.to_dict()

        assert data["text"] == "test concept"
        assert data["frequency"] == 3
        assert data["relevance_score"] == 0.7
        assert set(data["source_papers"]) == {"paper1", "paper2"}
        assert data["source_domain"] == "test_domain"
        assert data["extraction_method"] == "tfidf"
        assert "embedding" not in data

    def test_serialize_concept_with_embedding(self):
        """Test serializing concept with embedding."""
        vector = np.array([0.1, 0.2, 0.3, 0.4])
        embedding = EmbeddingVector(vector)
        concept = Concept(
            text="embedded concept",
            frequency=2,
            relevance_score=0.8,
            embedding=embedding,
        )

        data = concept.to_dict()

        assert data["text"] == "embedded concept"
        assert data["frequency"] == 2
        assert data["relevance_score"] == 0.8
        assert "embedding" in data
        assert np.allclose(data["embedding"], vector)

    def test_deserialize_concept_without_embedding(self):
        """Test deserializing concept without embedding data."""
        data = {
            "text": "deserialized concept",
            "frequency": 4,
            "relevance_score": 0.9,
            "source_papers": ["paper1", "paper2"],
            "source_domain": "test",
            "extraction_method": "keyword",
            "created_at": "2024-01-01T00:00:00+00:00",
            "synonyms": ["synonym1"],
        }

        concept = Concept.from_dict(data)

        assert concept.text == "deserialized concept"
        assert concept.frequency == 4
        assert concept.relevance_score == 0.9
        assert concept.source_papers == {"paper1", "paper2"}
        assert concept.synonyms == {"synonym1"}
        assert concept.embedding is None
        assert not concept.has_semantic_data()

    def test_deserialize_concept_with_embedding(self):
        """Test deserializing concept with embedding data."""
        vector_data = [0.1, 0.2, 0.3, 0.4]
        data = {
            "text": "embedded deserialized",
            "frequency": 1,
            "relevance_score": 0.6,
            "source_papers": [],
            "extraction_method": "sentence_transformer",
            "created_at": "2024-01-01T00:00:00+00:00",
            "synonyms": [],
            "embedding": vector_data,
        }

        concept = Concept.from_dict(data)

        assert concept.text == "embedded deserialized"
        assert concept.has_semantic_data()
        assert concept.embedding is not None
        assert np.allclose(concept.embedding.vector, vector_data)

    def test_roundtrip_serialization_with_embedding(self):
        """Test complete roundtrip serialization preserves embedding data."""
        original_vector = np.array([0.5, -0.3, 0.8, 0.1])
        original_embedding = EmbeddingVector(original_vector)
        original_concept = Concept(
            text="roundtrip test",
            frequency=7,
            relevance_score=0.85,
            source_papers={"paper1", "paper2", "paper3"},
            source_domain="medical",
            extraction_method="semantic_embedding",
            synonyms={"alt term", "synonym"},
            embedding=original_embedding,
        )

        # Serialize and deserialize
        data = original_concept.to_dict()
        restored_concept = Concept.from_dict(data)

        # Verify all fields preserved
        assert restored_concept.text == original_concept.text
        assert restored_concept.frequency == original_concept.frequency
        assert restored_concept.relevance_score == original_concept.relevance_score
        assert restored_concept.source_papers == original_concept.source_papers
        assert restored_concept.source_domain == original_concept.source_domain
        assert restored_concept.extraction_method == original_concept.extraction_method
        assert restored_concept.synonyms == original_concept.synonyms
        assert restored_concept.has_semantic_data()
        assert np.allclose(restored_concept.embedding.vector, original_vector)


class TestConceptBusinessLogic:
    """Tests for concept business logic operations."""

    def test_add_paper_occurrence_preserves_embedding(self):
        """Test that adding paper occurrence preserves semantic embedding."""
        vector = np.array([0.1, 0.2, 0.3])
        embedding = EmbeddingVector(vector)
        original = Concept(
            text="machine learning",
            frequency=2,
            relevance_score=0.7,
            source_papers={"paper1"},
            embedding=embedding,
        )

        updated = original.add_paper_occurrence("paper2")

        assert updated.frequency == 3
        assert updated.source_papers == {"paper1", "paper2"}
        assert updated.embedding is not None
        assert np.allclose(updated.embedding.vector, vector)
        assert updated.text == original.text

    def test_merge_with_synonym_preserves_primary_embedding(self):
        """Test merging concepts preserves the primary concept's embedding."""
        primary_vector = np.array([0.1, 0.2, 0.3])
        primary_embedding = EmbeddingVector(primary_vector)
        primary = Concept(
            text="AI",
            frequency=5,
            relevance_score=0.9,
            embedding=primary_embedding,
        )

        synonym_vector = np.array([0.4, 0.5, 0.6])
        synonym_embedding = EmbeddingVector(synonym_vector)
        synonym = Concept(
            text="artificial intelligence",
            frequency=3,
            relevance_score=0.8,
            embedding=synonym_embedding,
        )

        merged = primary.merge_with_synonym(synonym)

        assert merged.frequency == 8  # Combined frequency
        assert "artificial intelligence" in merged.synonyms
        assert merged.embedding is not None
        assert np.allclose(merged.embedding.vector, primary_vector)

    def test_concept_equality_ignores_embedding(self):
        """Test that concept equality is based on text, not embedding."""
        vector1 = np.array([0.1, 0.2, 0.3])
        vector2 = np.array([0.4, 0.5, 0.6])

        concept1 = Concept(
            text="neural networks",
            frequency=1,
            relevance_score=0.5,
            embedding=EmbeddingVector(vector1),
        )

        concept2 = Concept(
            text="neural networks",
            frequency=10,
            relevance_score=0.9,
            embedding=EmbeddingVector(vector2),
        )

        assert concept1 == concept2
        assert hash(concept1) == hash(concept2)


class TestConceptHierarchy:
    """Tests for hierarchical concept features and relationships."""

    def test_create_concept_with_hierarchy_fields(self):
        """Test creating concept with hierarchical relationship fields."""
        concept = Concept(
            text="cardiac arrhythmia",
            frequency=3,
            relevance_score=0.8,
            parent_concepts={"cardiovascular disease"},
            child_concepts={"atrial fibrillation", "ventricular tachycardia"},
            concept_level=1,
            cluster_id="cardiac_cluster_001",
            evidence_strength=0.92,
        )

        assert concept.parent_concepts == {"cardiovascular disease"}
        assert concept.child_concepts == {
            "atrial fibrillation",
            "ventricular tachycardia",
        }
        assert concept.concept_level == 1
        assert concept.cluster_id == "cardiac_cluster_001"
        assert concept.evidence_strength == 0.92

    def test_concept_hierarchy_defaults(self):
        """Test that hierarchy fields have appropriate default values."""
        concept = Concept(
            text="basic concept",
            frequency=1,
            relevance_score=0.5,
        )

        assert concept.parent_concepts == set()
        assert concept.child_concepts == set()
        assert concept.concept_level == 0
        assert concept.cluster_id is None
        assert concept.evidence_strength == 1.0

    def test_add_parent_concept_preserves_immutability(self):
        """Test adding parent concept returns new instance."""
        original = Concept(
            text="heart rate variability",
            frequency=5,
            relevance_score=0.7,
        )

        updated = original.add_parent_concept("autonomic nervous system")

        assert original.parent_concepts == set()
        assert updated.parent_concepts == {"autonomic nervous system"}
        assert updated.text == original.text
        assert updated.frequency == original.frequency

    def test_add_child_concept_preserves_immutability(self):
        """Test adding child concept returns new instance."""
        original = Concept(
            text="cardiac monitoring",
            frequency=3,
            relevance_score=0.6,
        )

        updated = original.add_child_concept("ECG analysis")

        assert original.child_concepts == set()
        assert updated.child_concepts == {"ECG analysis"}
        assert updated.text == original.text

    def test_hierarchy_validation_rejects_negative_level(self):
        """Test validation rejects negative concept levels."""
        with pytest.raises(ValueError, match="Concept level cannot be negative"):
            Concept(
                text="test concept",
                frequency=1,
                relevance_score=0.5,
                concept_level=-1,
            )

    def test_hierarchy_validation_rejects_invalid_evidence_strength(self):
        """Test validation rejects evidence strength outside [0.0, 1.0]."""
        with pytest.raises(
            ValueError, match="Evidence strength must be between 0.0 and 1.0"
        ):
            Concept(
                text="test concept",
                frequency=1,
                relevance_score=0.5,
                evidence_strength=1.5,
            )

    def test_prevent_self_reference_in_parent_concepts(self):
        """Test validation prevents self-reference in parent concepts."""
        with pytest.raises(ValueError, match="Concept cannot be its own parent"):
            Concept(
                text="circular concept",
                frequency=1,
                relevance_score=0.5,
                parent_concepts={"circular concept"},
            )

    def test_prevent_self_reference_in_child_concepts(self):
        """Test validation prevents self-reference in child concepts."""
        with pytest.raises(ValueError, match="Concept cannot be its own child"):
            Concept(
                text="circular concept",
                frequency=1,
                relevance_score=0.5,
                child_concepts={"circular concept"},
            )

    def test_is_root_concept(self):
        """Test identification of root concepts (no parents)."""
        root_concept = Concept(
            text="medicine",
            frequency=10,
            relevance_score=0.9,
            child_concepts={"cardiology", "neurology"},
        )

        child_concept = Concept(
            text="cardiology",
            frequency=5,
            relevance_score=0.8,
            parent_concepts={"medicine"},
        )

        assert root_concept.is_root_concept()
        assert not child_concept.is_root_concept()

    def test_is_leaf_concept(self):
        """Test identification of leaf concepts (no children)."""
        parent_concept = Concept(
            text="cardiovascular disease",
            frequency=8,
            relevance_score=0.85,
            child_concepts={"heart attack", "stroke"},
        )

        leaf_concept = Concept(
            text="heart attack",
            frequency=3,
            relevance_score=0.7,
            parent_concepts={"cardiovascular disease"},
        )

        assert not parent_concept.is_leaf_concept()
        assert leaf_concept.is_leaf_concept()

    def test_get_hierarchy_depth(self):
        """Test calculating hierarchy depth from concept level."""
        level_0 = Concept(
            text="root concept",
            frequency=1,
            relevance_score=0.5,
            concept_level=0,
        )

        level_3 = Concept(
            text="deep concept",
            frequency=1,
            relevance_score=0.5,
            concept_level=3,
        )

        assert level_0.get_hierarchy_depth() == 0
        assert level_3.get_hierarchy_depth() == 3

    def test_set_cluster_assignment(self):
        """Test setting cluster assignment returns new instance."""
        original = Concept(
            text="neural plasticity",
            frequency=4,
            relevance_score=0.8,
        )

        clustered = original.set_cluster("neuroscience_cluster_007")

        assert original.cluster_id is None
        assert clustered.cluster_id == "neuroscience_cluster_007"
        assert clustered.text == original.text

    def test_update_evidence_strength(self):
        """Test updating evidence strength returns new instance."""
        original = Concept(
            text="synaptic transmission",
            frequency=6,
            relevance_score=0.75,
            evidence_strength=0.8,
        )

        updated = original.update_evidence_strength(0.95)

        assert original.evidence_strength == 0.8
        assert updated.evidence_strength == 0.95
        assert updated.text == original.text
