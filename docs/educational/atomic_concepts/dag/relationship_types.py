"""
Relationship Types for Concept Dependencies

Defines the mathematical structure of relationships between atomic concepts,
providing both semantic meaning and computational properties for dependency modeling.

Mathematical Foundation:
- Dependency relationships form a partially ordered set (poset)
- Relationship strength provides weighted graph capabilities
- Type safety ensures only valid relationships can be created

Educational Value:
Demonstrates enumeration design patterns, type systems, and mathematical
modeling of abstract relationships in computer science.
"""

from enum import Enum, auto
from typing import Union


class RelationshipType(Enum):
    """
    Mathematical classification of concept dependency relationships.

    Each type represents a different semantic meaning while maintaining
    the mathematical property that all relationships contribute to the
    overall partial ordering of concepts.
    """

    # Direct logical prerequisites
    PREREQUISITE = "prerequisite"  # A directly requires B
    FOUNDATION = "foundation"  # A builds fundamentally upon B

    # Semantic relationships
    SPECIALIZATION = "specialization"  # A is a specific case of B
    GENERALIZATION = "generalization"  # A generalizes concept B

    # Applied relationships
    APPLICATION = "application"  # A applies concept B
    EXTENSION = "extension"  # A extends concept B

    # Meta-relationships
    ANALOGY = "analogy"  # A is analogous to B (weaker dependency)
    MOTIVATION = "motivation"  # A motivates learning B

    def __str__(self) -> str:
        return self.value

    @property
    def creates_dependency(self) -> bool:
        """
        Mathematical property: Does this relationship type create a dependency edge?

        Some relationships (like ANALOGY) provide semantic connections without
        creating strict prerequisite dependencies in the DAG.
        """
        return self in {
            RelationshipType.PREREQUISITE,
            RelationshipType.FOUNDATION,
            RelationshipType.SPECIALIZATION,
            RelationshipType.APPLICATION,
        }


class DependencyStrength(Enum):
    """
    Mathematical weighting of dependency relationships.

    Provides numerical values for graph algorithms that need weighted edges,
    while maintaining educational semantic meaning.
    """

    ESSENTIAL = 1.0  # Cannot understand A without mastering B
    STRONG = 0.8  # Significant understanding gap without B
    MODERATE = 0.6  # Helpful but not critical prerequisite
    WEAK = 0.4  # Provides context or motivation
    REFERENCE = 0.2  # Mentioned or briefly used

    def __float__(self) -> float:
        return self.value

    def __gt__(self, other: "DependencyStrength") -> bool:
        """Enable mathematical comparison of dependency strengths."""
        return self.value > other.value

    def __lt__(self, other: "DependencyStrength") -> bool:
        """Enable mathematical comparison of dependency strengths."""
        return self.value < other.value


# Type alias for relationship specifications
RelationshipSpec = tuple[RelationshipType, DependencyStrength]
