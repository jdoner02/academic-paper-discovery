"""
EmbeddingVector Value Object - Represents semantic embedding vectors for concepts.

This value object demonstrates Clean Architecture principles by encapsulating
the mathematical representation of semantic meaning while maintaining immutability
and value semantics.

Educational Notes:
- Shows Value Object pattern with semantic equality and immutability
- Demonstrates encapsulation of mathematical operations
- Illustrates domain-specific constraints and validation
- Shows how to integrate ML/AI concepts into domain modeling

Design Decisions:
- Immutable tuple representation for memory efficiency
- Cached norm calculation for performance
- Semantic similarity methods for research analysis
- Dimension validation for model compatibility

Use Cases:
- Semantic similarity analysis between research concepts
- Concept clustering and grouping
- Vector space operations for research exploration
- Integration with transformer models and embeddings
"""

from typing import Tuple, Union, List
import math
from dataclasses import dataclass
from functools import cached_property
import numpy as np


@dataclass(frozen=True)
class EmbeddingVector:
    """
    Represents a semantic embedding vector for research concepts.

    An embedding vector is an immutable value object that encapsulates
    the semantic representation of text as a high-dimensional vector.
    This enables mathematical operations for semantic similarity analysis.

    Attributes:
        vector: Tuple of float values representing the embedding
        model_name: Name of the model used to generate this embedding
        dimension: Number of dimensions in the vector
    """

    vector: Tuple[float, ...]
    model_name: str = "unknown"

    def __post_init__(self):
        """
        Validate embedding vector business rules.

        Educational Note:
        Domain validation ensures embedding vectors meet mathematical
        requirements for semantic analysis operations.
        """
        if self.vector is None:
            raise ValueError("Embedding vector cannot be None")

        if len(self.vector) == 0:
            raise ValueError("Embedding vector must have dimensions")

        # Check for numeric types and finite values
        if not np.isfinite(self.vector).all():
            raise ValueError("Embedding vector contains invalid numeric values")

    @property
    def dimension(self) -> int:
        """Get the dimensionality of this embedding vector."""
        return len(self.vector)

    @cached_property
    def norm(self) -> float:
        """
        Calculate and cache the Euclidean norm of the vector.

        Educational Note:
        Cached property pattern provides performance optimization
        for expensive calculations that don't change over object lifetime.
        """
        return math.sqrt(sum(x * x for x in self.vector))

    def cosine_similarity(self, other: "EmbeddingVector") -> float:
        """
        Calculate cosine similarity with another embedding vector.

        Educational Note:
        Cosine similarity is the standard metric for semantic similarity
        in NLP and information retrieval. It measures the cosine of the
        angle between two vectors, ignoring magnitude differences.

        Returns:
            Float between -1.0 and 1.0, where 1.0 is identical direction
        """
        if not isinstance(other, EmbeddingVector):
            raise TypeError(
                "Can only calculate similarity with another EmbeddingVector"
            )

        if self.dimension != other.dimension:
            raise ValueError(
                f"Vector dimensions must match: {self.dimension} vs {other.dimension}"
            )

        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(self.vector, other.vector))

        # Handle zero vectors
        if self.norm == 0.0 or other.norm == 0.0:
            return 0.0

        return dot_product / (self.norm * other.norm)

    def euclidean_distance(self, other: "EmbeddingVector") -> float:
        """
        Calculate Euclidean distance to another embedding vector.

        Educational Note:
        Euclidean distance provides an alternative similarity metric
        that considers magnitude differences. Useful for clustering
        and nearest neighbor analysis.
        """
        if not isinstance(other, EmbeddingVector):
            raise TypeError("Can only calculate distance with another EmbeddingVector")

        if self.dimension != other.dimension:
            raise ValueError(
                f"Vector dimensions must match: {self.dimension} vs {other.dimension}"
            )

        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.vector, other.vector)))

    def manhattan_distance(self, other: "EmbeddingVector") -> float:
        """Calculate Manhattan (L1) distance to another embedding vector."""
        if not isinstance(other, EmbeddingVector):
            raise TypeError("Can only calculate distance with another EmbeddingVector")

        if self.dimension != other.dimension:
            raise ValueError(
                f"Vector dimensions must match: {self.dimension} vs {other.dimension}"
            )

        return sum(abs(a - b) for a, b in zip(self.vector, other.vector))

    def to_numpy(self) -> np.ndarray:
        """
        Convert to NumPy array for mathematical operations.

        Educational Note:
        Provides bridge to scientific computing ecosystem while
        maintaining domain object integrity.
        """
        return np.array(self.vector)

    @classmethod
    def from_list(
        cls, values: List[float], model_name: str = "unknown"
    ) -> "EmbeddingVector":
        """
        Create embedding vector from list of values.

        Educational Note:
        Factory method pattern provides convenient construction
        while maintaining value object immutability.
        """
        return cls(vector=tuple(values), model_name=model_name)

    @classmethod
    def from_numpy(
        cls, array: np.ndarray, model_name: str = "unknown"
    ) -> "EmbeddingVector":
        """Create embedding vector from NumPy array."""
        return cls(vector=tuple(array.tolist()), model_name=model_name)

    def __str__(self) -> str:
        """String representation showing key properties."""
        preview = (
            str(self.vector[:3]) + "..." if self.dimension > 3 else str(self.vector)
        )
        return f"EmbeddingVector(dim={self.dimension}, model={self.model_name}, preview={preview})"

    def __len__(self) -> int:
        """Enable len() function for dimension access."""
        return self.dimension
