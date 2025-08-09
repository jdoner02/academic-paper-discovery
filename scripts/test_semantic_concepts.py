#!/usr/bin/env python3
"""
Test script for semantic embeddings integration with concepts.

This script demonstrates the enhanced concept extraction and semantic
similarity analysis capabilities using real sentence-transformers embeddings.

Run with: PYTHONPATH=src python3 scripts/test_semantic_concepts.py
"""

import sys
import os
import numpy as np
from typing import List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from domain.entities.concept import Concept
from domain.value_objects.embedding_vector import EmbeddingVector
from infrastructure.services.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
    MockEmbeddingService,
)


def test_mock_embeddings():
    """Test semantic concepts with mock embeddings (no external dependencies)."""
    print("🧪 Testing semantic concepts with mock embeddings...\n")

    # Create mock embedding service
    mock_service = MockEmbeddingService(dimension=384)

    # Create concepts with mock embeddings
    concept_texts = [
        "heart rate variability",
        "cardiac variability",
        "hrv analysis",
        "quantum computing",
        "machine learning",
    ]

    concepts = []
    for text in concept_texts:
        embedding = mock_service.generate_embedding(text)
        concept = Concept(
            text=text,
            frequency=3,
            relevance_score=0.8,
            extraction_method="sentence_transformer",
            embedding=embedding,
        )
        concepts.append(concept)

    # Test semantic similarity
    print("🔍 Testing semantic similarity analysis:")
    base_concept = concepts[0]  # "heart rate variability"

    for other_concept in concepts[1:]:
        similarity = base_concept.semantic_similarity(other_concept)
        print(f"  '{base_concept.text}' ↔ '{other_concept.text}': {similarity:.3f}")

    # Test finding similar concepts
    print(f"\n🎯 Finding concepts similar to '{base_concept.text}' (threshold=0.3):")
    similar_concepts = base_concept.find_similar_concepts(
        concepts[1:], similarity_threshold=0.3
    )

    for concept, score in similar_concepts:
        print(f"  📋 {concept.text}: {score:.3f}")

    # Test serialization with embeddings
    print(f"\n💾 Testing serialization with embeddings:")
    concept_dict = base_concept.to_dict()
    print(f"  Serialized concept keys: {list(concept_dict.keys())}")
    print(f"  Embedding dimensions: {len(concept_dict['embedding'])}")

    # Test deserialization
    restored_concept = Concept.from_dict(concept_dict)
    print(f"  Restored concept has embedding: {restored_concept.has_semantic_data()}")
    print(
        f"  Original vs restored similarity: {base_concept.semantic_similarity(restored_concept):.3f}"
    )

    print("\n✅ Mock embedding tests completed successfully!")


def test_real_embeddings():
    """Test semantic concepts with real sentence-transformers embeddings."""
    print("🚀 Testing semantic concepts with real sentence-transformers...\n")

    try:
        # Create real embedding service
        embedding_service = SentenceTransformerEmbeddingService(
            model_name="all-MiniLM-L6-v2", cache_embeddings=True
        )

        # Display model info
        model_info = embedding_service.get_model_info()
        print(f"📊 Model Info:")
        print(f"  Model: {model_info['model_name']}")
        print(f"  Dimensions: {model_info['embedding_dimension']}")
        print(f"  Device: {model_info['device']}")
        print()

        # Create concepts with real embeddings for HRV research
        hrv_concepts = [
            "heart rate variability",
            "cardiac rhythm analysis",
            "autonomic nervous system",
            "parasympathetic activity",
            "sympathetic nervous system",
            "traumatic brain injury",
            "neurological assessment",
            "quantum cryptography",  # Should be different
            "blockchain technology",  # Should be different
        ]

        print("🔮 Generating embeddings for HRV research concepts...")
        concepts_with_embeddings = []

        for text in hrv_concepts:
            embedding = embedding_service.generate_embedding(text)
            concept = Concept(
                text=text,
                frequency=5,
                relevance_score=0.85,
                source_domain="medical_research",
                extraction_method="sentence_transformer",
                embedding=embedding,
            )
            concepts_with_embeddings.append(concept)

        # Analyze semantic relationships
        print(f"\n🧠 Semantic similarity analysis from '{hrv_concepts[0]}':")
        base_concept = concepts_with_embeddings[0]

        similarities = []
        for other_concept in concepts_with_embeddings[1:]:
            similarity = base_concept.semantic_similarity(other_concept)
            similarities.append((other_concept.text, similarity))
            print(f"  📊 {similarity:.3f}: {other_concept.text}")

        # Find most similar concepts
        print(f"\n🎯 Most similar concepts (threshold=0.4):")
        similar_concepts = base_concept.find_similar_concepts(
            concepts_with_embeddings[1:], similarity_threshold=0.4
        )

        for concept, score in similar_concepts[:5]:  # Top 5
            print(f"  🔗 {score:.3f}: {concept.text}")

        # Test batch processing
        print(f"\n⚡ Testing batch embedding generation:")
        batch_texts = [
            "rmssd calculation",
            "pnn50 analysis",
            "frequency domain hrv",
            "time domain metrics",
        ]

        batch_embeddings = embedding_service.generate_embeddings_batch(batch_texts)
        print(f"  Generated {len(batch_embeddings)} embeddings in batch")

        # Show cache statistics
        cache_stats = embedding_service.get_cache_stats()
        print(f"  Cache entries: {cache_stats['cached_entries']}")

        print("\n✅ Real embedding tests completed successfully!")

    except RuntimeError as e:
        print(f"⚠️ Real embedding test failed: {e}")
        print(
            "💡 Make sure sentence-transformers is installed: pip install sentence-transformers"
        )
        return False

    except Exception as e:
        print(f"❌ Unexpected error in real embedding test: {e}")
        return False

    return True


def demonstrate_concept_clustering():
    """Demonstrate concept clustering using semantic embeddings."""
    print("🔬 Demonstrating concept clustering with embeddings...\n")

    try:
        embedding_service = SentenceTransformerEmbeddingService()

        # Create diverse research concepts
        research_concepts = {
            "medical": [
                "heart rate variability analysis",
                "cardiac autonomic function",
                "parasympathetic nervous system",
                "traumatic brain injury recovery",
            ],
            "technology": [
                "machine learning algorithms",
                "neural network architectures",
                "deep learning models",
                "artificial intelligence systems",
            ],
            "security": [
                "post quantum cryptography",
                "hash based signatures",
                "cryptographic protocols",
                "cybersecurity frameworks",
            ],
        }

        all_concepts = []
        for category, texts in research_concepts.items():
            for text in texts:
                embedding = embedding_service.generate_embedding(text)
                concept = Concept(
                    text=text,
                    frequency=1,
                    relevance_score=0.7,
                    source_domain=category,
                    extraction_method="sentence_transformer",
                    embedding=embedding,
                )
                all_concepts.append(concept)

        # Demonstrate clustering by finding similar concepts for each category
        print("🎯 Concept clustering analysis:")

        for category, texts in research_concepts.items():
            print(f"\n📂 {category.upper()} cluster:")

            # Find the first concept from this category
            category_concept = next(c for c in all_concepts if c.text == texts[0])

            # Find similar concepts across all domains
            similar = category_concept.find_similar_concepts(
                [c for c in all_concepts if c != category_concept],
                similarity_threshold=0.3,
            )

            # Show top 3 most similar
            for concept, score in similar[:3]:
                domain_match = "✅" if concept.source_domain == category else "🔀"
                print(
                    f"    {domain_match} {score:.3f}: {concept.text} ({concept.source_domain})"
                )

        print("\n✅ Concept clustering demonstration completed!")

    except Exception as e:
        print(f"❌ Clustering demonstration failed: {e}")


def main():
    """Run all semantic embedding tests."""
    print("🔬 Semantic Embedding Integration Tests")
    print("=" * 50)

    # Always run mock tests (no external dependencies)
    test_mock_embeddings()
    print("\n" + "=" * 50)

    # Try real embeddings if available
    if test_real_embeddings():
        print("\n" + "=" * 50)
        demonstrate_concept_clustering()

    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    main()
