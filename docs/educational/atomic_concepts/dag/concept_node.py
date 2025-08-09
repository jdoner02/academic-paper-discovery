"""
Concept Node Implementation for Atomic Educational Concepts

Represents individual mathematical and computer science concepts as nodes in the
dependency DAG. Each node contains rich metadata for educational purposes while
maintaining mathematical precision for algorithmic operations.

Mathematical Foundation:
- Each concept is a mathematical object with defined properties
- Immutable after creation to ensure graph consistency
- Hashable to enable efficient set operations and graph algorithms

Educational Purpose:
Demonstrates object-oriented design, immutability patterns, and the mathematical
modeling of abstract knowledge as computational objects.
"""

from dataclasses import dataclass, field
from typing import Set, Dict, Any, Optional, FrozenSet
from uuid import uuid4, UUID

from .relationship_types import RelationshipType, DependencyStrength, RelationshipSpec


@dataclass(frozen=True, order=True)
class ConceptNode:
    """
    Immutable representation of an atomic educational concept.

    Mathematical Properties:
    - Immutable (frozen=True) ensures graph integrity
    - Hashable enables efficient set operations
    - Ordered enables topological sorting algorithms

    Educational Properties:
    - Rich metadata supports adaptive learning systems
    - Mathematical definitions provide formal precision
    - Complexity tracking enables curriculum sequencing
    """

    # Core Identity
    name: str = field(compare=True)
    concept_id: UUID = field(default_factory=uuid4, compare=False)

    # Educational Metadata
    type: str = field(
        default="concept", compare=False
    )  # axiom, theorem, concept, algorithm
    description: str = field(default="", compare=False)
    mathematical_definition: str = field(default="", compare=False)

    # Taxonomic Classification
    subject_area: str = field(default="mathematics", compare=False)
    complexity_level: str = field(
        default="fundamental", compare=False
    )  # fundamental, basic, intermediate, advanced
    cognitive_load: int = field(default=1, compare=False)  # 1-10 scale

    # Dependency Information (stored as frozenset for immutability)
    prerequisites: FrozenSet[str] = field(default_factory=frozenset, compare=False)
    dependency_metadata: Dict[str, RelationshipSpec] = field(
        default_factory=dict, compare=False
    )

    # Educational Support
    examples: tuple[str, ...] = field(default_factory=tuple, compare=False)
    common_misconceptions: tuple[str, ...] = field(default_factory=tuple, compare=False)
    pedagogical_notes: str = field(default="", compare=False)

    # Computational Properties
    learning_objectives: tuple[str, ...] = field(default_factory=tuple, compare=False)
    assessment_criteria: tuple[str, ...] = field(default_factory=tuple, compare=False)

    def __post_init__(self):
        """
        Validate mathematical and educational constraints after initialization.

        Mathematical Invariants:
        - Name must be non-empty and valid identifier
        - Complexity level must be from defined set
        - Cognitive load must be positive integer
        """
        if not self.name or not self.name.strip():
            raise ValueError("Concept name cannot be empty")

        if not self.name.replace("_", "").replace("-", "").replace(" ", "").isalnum():
            raise ValueError(f"Concept name '{self.name}' contains invalid characters")

        valid_complexities = {"fundamental", "basic", "intermediate", "advanced"}
        if self.complexity_level not in valid_complexities:
            raise ValueError(f"Complexity level must be one of {valid_complexities}")

        if (
            not isinstance(self.cognitive_load, int)
            or self.cognitive_load < 1
            or self.cognitive_load > 10
        ):
            raise ValueError("Cognitive load must be integer between 1 and 10")

    @property
    def is_axiom(self) -> bool:
        """Mathematical property: Is this concept an axiom (no prerequisites)?"""
        return self.type == "axiom" and len(self.prerequisites) == 0

    @property
    def is_fundamental(self) -> bool:
        """Educational property: Is this a fundamental concept?"""
        return self.complexity_level == "fundamental"

    @property
    def dependency_count(self) -> int:
        """Graph property: Number of direct dependencies."""
        return len(self.prerequisites)

    def has_prerequisite(self, concept_name: str) -> bool:
        """Check if this concept has a specific prerequisite."""
        return concept_name in self.prerequisites

    def get_relationship_to(self, prerequisite: str) -> Optional[RelationshipSpec]:
        """Get the relationship specification to a prerequisite concept."""
        return self.dependency_metadata.get(prerequisite)

    def get_strong_dependencies(
        self, threshold: DependencyStrength = DependencyStrength.STRONG
    ) -> Set[str]:
        """
        Get prerequisites with dependency strength above threshold.

        Useful for identifying critical vs. optional prerequisites in curriculum design.
        """
        return {
            prereq
            for prereq, (_, strength) in self.dependency_metadata.items()
            if strength >= threshold
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert concept to dictionary for serialization/visualization.

        Useful for JSON export to D3.js visualization systems.
        """
        return {
            "id": str(self.concept_id),
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "mathematical_definition": self.mathematical_definition,
            "subject_area": self.subject_area,
            "complexity_level": self.complexity_level,
            "cognitive_load": self.cognitive_load,
            "prerequisites": list(self.prerequisites),
            "dependency_count": self.dependency_count,
            "is_axiom": self.is_axiom,
            "is_fundamental": self.is_fundamental,
            "examples": list(self.examples),
            "learning_objectives": list(self.learning_objectives),
        }

    def __str__(self) -> str:
        """Human-readable representation for debugging and logging."""
        prereq_count = len(self.prerequisites)
        return f"ConceptNode('{self.name}', {self.type}, {prereq_count} deps)"

    def __repr__(self) -> str:
        """Detailed representation for development and debugging."""
        return (
            f"ConceptNode(name='{self.name}', type='{self.type}', "
            f"complexity='{self.complexity_level}', prerequisites={self.prerequisites})"
        )
