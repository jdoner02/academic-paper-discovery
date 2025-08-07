"""
SentenceTransformerEmbeddingService - Infrastructure service for generating semantic embeddings.

This service provides concrete implementation of embedding generation using
the sentence-transformers library, following Clean Architecture principles
by implementing infrastructure concerns outside the domain layer.

Educational Notes:
- Shows Infrastructure layer implementing application ports
- Demonstrates integration with ML libraries (sentence-transformers)
- Illustrates dependency inversion with abstract interfaces
- Shows how to encapsulate ML model complexity in infrastructure

Design Decisions:
- Uses sentence-transformers for state-of-the-art embeddings
- Provides caching and batching capabilities for efficiency
- Handles model loading and lifecycle management
- Abstracts model-specific details from domain layer

Use Cases:
- Generate embeddings for concept extraction
- Enable semantic similarity analysis
- Support concept clustering and relationships
- Integrate with research paper analysis pipelines
"""

from typing import List, Optional, Dict, Any
import numpy as np
from datetime import datetime, timezone
import logging

from src.domain.value_objects.embedding_vector import EmbeddingVector

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

# Configure logging
logger = logging.getLogger(__name__)


class SentenceTransformerEmbeddingService:
    """
    Infrastructure service for generating semantic embeddings using sentence-transformers.

    This service encapsulates the complexity of ML model management while providing
    a clean interface for the application layer to generate embeddings.

    Educational Note:
    Infrastructure services implement the technical details of external systems
    while providing domain-friendly interfaces. This maintains Clean Architecture
    by keeping ML concerns out of the domain layer.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None,
        cache_embeddings: bool = True,
    ):
        """
        Initialize the embedding service with model configuration.

        Educational Note:
        Constructor handles infrastructure setup including model loading,
        device configuration, and caching strategy initialization.

        Args:
            model_name: Name of sentence-transformers model to use
            device: Device to run model on ('cpu', 'cuda', etc.)
            cache_embeddings: Whether to cache computed embeddings
        """
        self._model_name = model_name
        self._device = device
        self._cache_embeddings = cache_embeddings
        self._model = None
        self._embedding_cache: Dict[str, EmbeddingVector] = {}
        self._load_model()

    def _load_model(self):
        """
        Load the sentence-transformers model.

        Educational Note:
        Lazy loading pattern allows service initialization without
        immediately consuming model resources. Error handling ensures
        graceful degradation if model loading fails.
        """
        try:
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise RuntimeError(
                    "sentence-transformers library not installed. "
                    "Install with: pip install sentence-transformers"
                )

            self._model = SentenceTransformer(self._model_name, device=self._device)
            logger.info(f"Loaded embedding model: {self._model_name}")

        except ImportError:
            raise RuntimeError(
                "sentence-transformers library not installed. "
                "Install with: pip install sentence-transformers"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load model {self._model_name}: {str(e)}")

    def generate_embedding(self, text: str) -> EmbeddingVector:
        """
        Generate embedding vector for a single text.

        Educational Note:
        Single-text interface provides convenient API while leveraging
        batch processing internally for efficiency. Caching reduces
        redundant computation for repeated texts.

        Args:
            text: Text to generate embedding for

        Returns:
            EmbeddingVector containing semantic representation

        Raises:
            ValueError: If text is empty or invalid
            RuntimeError: If model fails to generate embedding
        """
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")

        # Check cache first
        if self._cache_embeddings and text in self._embedding_cache:
            return self._embedding_cache[text]

        try:
            # Generate embedding using sentence-transformers
            embedding_array = self._model.encode([text], convert_to_numpy=True)[0]

            # Convert to domain value object
            embedding_vector = EmbeddingVector.from_numpy(
                embedding_array, model_name=self._model_name
            )

            # Cache if enabled
            if self._cache_embeddings:
                self._embedding_cache[text] = embedding_vector

            return embedding_vector

        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding for text: {str(e)}")

    def generate_embeddings_batch(self, texts: List[str]) -> List[EmbeddingVector]:
        """
        Generate embeddings for multiple texts efficiently.

        Educational Note:
        Batch processing leverages model efficiency for multiple inputs
        while maintaining clean individual result mapping. This is
        crucial for performance when processing many concepts.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of EmbeddingVectors corresponding to input texts

        Raises:
            ValueError: If texts list is empty
            RuntimeError: If batch processing fails
        """
        if not texts:
            raise ValueError("Cannot generate embeddings for empty text list")

        # Filter out empty texts and track indices
        valid_texts = []
        valid_indices = []

        for i, text in enumerate(texts):
            if text and text.strip():
                valid_texts.append(text)
                valid_indices.append(i)

        if not valid_texts:
            raise ValueError("No valid texts found for embedding generation")

        try:
            # Check cache for existing embeddings
            cached_results = {}
            uncached_texts = []
            uncached_indices = []

            if self._cache_embeddings:
                for i, text in enumerate(valid_texts):
                    if text in self._embedding_cache:
                        cached_results[valid_indices[i]] = self._embedding_cache[text]
                    else:
                        uncached_texts.append(text)
                        uncached_indices.append(valid_indices[i])
            else:
                uncached_texts = valid_texts
                uncached_indices = valid_indices

            # Generate embeddings for uncached texts
            new_embeddings = {}
            if uncached_texts:
                embedding_arrays = self._model.encode(
                    uncached_texts, convert_to_numpy=True
                )

                for i, (text, embedding_array) in enumerate(
                    zip(uncached_texts, embedding_arrays)
                ):
                    embedding_vector = EmbeddingVector.from_numpy(
                        embedding_array, model_name=self._model_name
                    )

                    # Cache if enabled
                    if self._cache_embeddings:
                        self._embedding_cache[text] = embedding_vector

                    new_embeddings[uncached_indices[i]] = embedding_vector

            # Combine cached and new results
            results = [None] * len(texts)

            # Add cached results
            for index, embedding in cached_results.items():
                results[index] = embedding

            # Add new results
            for index, embedding in new_embeddings.items():
                results[index] = embedding

            # Filter out None results (empty texts)
            final_results = [
                embedding for embedding in results if embedding is not None
            ]

            return final_results

        except Exception as e:
            raise RuntimeError(f"Failed to generate batch embeddings: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.

        Educational Note:
        Provides transparency about model configuration and capabilities
        for debugging and system monitoring purposes.

        Returns:
            Dictionary containing model information
        """
        if not self._model:
            return {"status": "not_loaded"}

        return {
            "model_name": self._model_name,
            "device": str(self._device) if self._device else "auto",
            "cache_enabled": self._cache_embeddings,
            "cached_embeddings": len(self._embedding_cache),
            "embedding_dimension": self._model.get_sentence_embedding_dimension(),
            "max_sequence_length": getattr(self._model, "max_seq_length", "unknown"),
            "status": "loaded",
        }

    def clear_cache(self):
        """
        Clear the embedding cache to free memory.

        Educational Note:
        Cache management methods allow fine-grained control over
        memory usage, especially important for long-running processes.
        """
        self._embedding_cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about embedding cache usage.

        Educational Note:
        Monitoring methods help understand system performance
        and resource utilization patterns.

        Returns:
            Dictionary containing cache statistics
        """
        return {
            "cached_entries": len(self._embedding_cache),
            "total_memory_mb": len(self._embedding_cache)
            * 384
            // (1024 * 1024),  # Approximate
        }

    def warm_up_cache(self, texts: List[str]):
        """
        Pre-generate embeddings for frequently used texts.

        Educational Note:
        Cache warming strategies improve performance by pre-computing
        embeddings for known frequent queries or analysis patterns.

        Args:
            texts: List of texts to pre-generate embeddings for
        """
        if not self._cache_embeddings:
            return

        print(f"🔥 Warming up embedding cache with {len(texts)} texts...")

        try:
            self.generate_embeddings_batch(texts)
            print(f"✅ Cache warmed up with {len(self._embedding_cache)} embeddings")
        except Exception as e:
            print(f"⚠️ Cache warm-up failed: {str(e)}")

    def __str__(self) -> str:
        """String representation showing service configuration."""
        return f"SentenceTransformerEmbeddingService(model={self._model_name}, cached={len(self._embedding_cache)})"


class MockEmbeddingService:
    """
    Mock embedding service for testing purposes.

    Educational Note:
    Mock implementations enable testing without external dependencies
    while maintaining the same interface contract as the real service.
    """

    def __init__(self, dimension: int = 384):
        """Initialize mock service with configurable dimension."""
        self._dimension = dimension
        self._model_name = "mock-model"

    def generate_embedding(self, text: str) -> EmbeddingVector:
        """Generate deterministic mock embedding based on text hash."""
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")

        # Create deterministic embedding based on text hash
        np.random.seed(hash(text) % (2**31))
        vector = np.random.normal(0, 1, self._dimension)
        vector = vector / np.linalg.norm(vector)  # Normalize to unit vector

        return EmbeddingVector.from_numpy(vector, model_name=self._model_name)

    def generate_embeddings_batch(self, texts: List[str]) -> List[EmbeddingVector]:
        """Generate mock embeddings for multiple texts."""
        return [
            self.generate_embedding(text) for text in texts if text and text.strip()
        ]

    def get_model_info(self) -> Dict[str, Any]:
        """Return mock model information."""
        return {
            "model_name": self._model_name,
            "embedding_dimension": self._dimension,
            "status": "mock",
        }

    def clear_cache(self):
        """No-op for mock service."""
        pass

    def get_cache_stats(self) -> Dict[str, int]:
        """Return empty cache stats for mock."""
        return {"cached_entries": 0, "total_memory_mb": 0}

    def warm_up_cache(self, texts: List[str]):
        """No-op for mock service."""
        pass
