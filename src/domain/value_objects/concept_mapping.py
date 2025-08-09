"""
Concept Mapping Value Objects

Immutable objects representing relationships and mappings between atomic concepts.

Educational Purpose:
- Demonstrates Value Object pattern with immutability
- Shows composition and aggregation of business concepts
- Illustrates defensive programming and validation
- Examples of rich domain modeling

Real-World Application:
- Knowledge graph construction in educational platforms
- Prerequisite tracking in learning management systems
- Dependency analysis in formal verification
- Curriculum design and learning path optimization
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, FrozenSet
from enum import Enum
from abc import ABC, abstractmethod
import json
from datetime import datetime


class RelationshipType(Enum):
    """
    Types of relationships between concepts.

    Educational Note: Using enums provides type safety and clear semantics
    for business relationships. Each relationship type has specific meaning
    and may require different processing logic.
    """

    PREREQUISITE = "prerequisite"  # A must be learned before B
    ENABLES = "enables"  # A makes B learnable
    RELATED = "related"  # A and B are conceptually related
    SPECIALIZES = "specializes"  # B is a specific case of A
    GENERALIZES = "generalizes"  # A is a general case of B
    EQUIVALENT = "equivalent"  # A and B are logically equivalent
    CONFLICTS = "conflicts"  # A and B cannot both be true
    APPLIES_TO = "applies_to"  # A is used in the context of B


class MappingStrength(Enum):
    """
    Strength of concept relationships.

    Educational Pattern: Enum with semantic meaning
    - Provides graduated scale for relationship strength
    - Enables filtering and prioritization in algorithms
    - Makes business rules explicit and testable
    """

    WEAK = 0.3  # Loosely related
    MODERATE = 0.6  # Clearly related
    STRONG = 0.8  # Tightly coupled
    ESSENTIAL = 1.0  # Absolutely required

    def __float__(self) -> float:
        """Allow arithmetic operations with strength values."""
        return self.value


@dataclass(frozen=True)
class ConceptRelationship:
    """
    Value object representing a relationship between two concepts.

    Educational Patterns:
    - Value Object: Immutable, compared by value not identity
    - Composition: Contains other value objects (enums)
    - Defensive Programming: Validates inputs thoroughly

    Real-World Usage:
    - Knowledge graph edges with semantic meaning
    - Learning analytics for prerequisite tracking
    - Curriculum design tools for dependency analysis
    """

    source_concept_id: str
    target_concept_id: str
    relationship_type: RelationshipType
    strength: MappingStrength
    explanation: Optional[str] = None
    evidence_score: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """
        Value object validation.

        Educational Note: Validation in constructor ensures
        object invariants are maintained throughout lifetime.
        Immutability prevents corruption after creation.
        """
        if not self.source_concept_id or not self.source_concept_id.strip():
            raise ValueError("Source concept ID cannot be empty")

        if not self.target_concept_id or not self.target_concept_id.strip():
            raise ValueError("Target concept ID cannot be empty")

        if self.source_concept_id == self.target_concept_id:
            raise ValueError("Concept cannot have relationship with itself")

        if not 0.0 <= self.evidence_score <= 1.0:
            raise ValueError("Evidence score must be between 0.0 and 1.0")

    def is_bidirectional(self) -> bool:
        """
        Check if this relationship type is inherently bidirectional.

        Business Logic: Some relationships (like 'related' or 'equivalent')
        imply the reverse relationship exists, while others (like 'prerequisite')
        are strictly directional.
        """
        bidirectional_types = {
            RelationshipType.RELATED,
            RelationshipType.EQUIVALENT,
            RelationshipType.CONFLICTS,
        }
        return self.relationship_type in bidirectional_types

    def get_inverse_relationship(self) -> Optional["ConceptRelationship"]:
        """
        Get the inverse relationship if it exists.

        Educational Pattern: Domain Logic Encapsulation
        - Business rules for relationship inversion are kept in domain
        - Makes the model self-consistent and reduces client complexity
        """
        inverse_mappings = {
            RelationshipType.PREREQUISITE: RelationshipType.ENABLES,
            RelationshipType.ENABLES: RelationshipType.PREREQUISITE,
            RelationshipType.SPECIALIZES: RelationshipType.GENERALIZES,
            RelationshipType.GENERALIZES: RelationshipType.SPECIALIZES,
            RelationshipType.RELATED: RelationshipType.RELATED,
            RelationshipType.EQUIVALENT: RelationshipType.EQUIVALENT,
            RelationshipType.CONFLICTS: RelationshipType.CONFLICTS,
        }

        inverse_type = inverse_mappings.get(self.relationship_type)
        if not inverse_type:
            return None

        return ConceptRelationship(
            source_concept_id=self.target_concept_id,
            target_concept_id=self.source_concept_id,
            relationship_type=inverse_type,
            strength=self.strength,
            explanation=f"Inverse of: {self.explanation}" if self.explanation else None,
            evidence_score=self.evidence_score,
            metadata=self.metadata.copy(),
        )

    def is_strong_relationship(self) -> bool:
        """Check if this is a strong relationship for filtering."""
        return self.strength.value >= MappingStrength.STRONG.value

    def calculate_weight(self) -> float:
        """
        Calculate numerical weight for graph algorithms.

        Educational Algorithm: Combines multiple factors to create
        a single metric useful for pathfinding and ranking algorithms.
        """
        base_weight = float(self.strength)
        evidence_factor = self.evidence_score

        # Type-specific weight modifiers
        type_weights = {
            RelationshipType.PREREQUISITE: 1.0,  # Critical for learning paths
            RelationshipType.ENABLES: 1.0,  # Critical for learning paths
            RelationshipType.EQUIVALENT: 0.9,  # High importance
            RelationshipType.SPECIALIZES: 0.8,  # Important hierarchy
            RelationshipType.GENERALIZES: 0.8,  # Important hierarchy
            RelationshipType.RELATED: 0.6,  # Moderate importance
            RelationshipType.APPLIES_TO: 0.7,  # Application context
            RelationshipType.CONFLICTS: 0.4,  # Lower weight for conflicts
        }

        type_weight = type_weights.get(self.relationship_type, 0.5)

        return base_weight * evidence_factor * type_weight

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for serialization."""
        return {
            "source": self.source_concept_id,
            "target": self.target_concept_id,
            "type": self.relationship_type.value,
            "strength": self.strength.name,
            "explanation": self.explanation or "",
            "evidence_score": str(self.evidence_score),
            "weight": str(self.calculate_weight()),
            "created_at": self.created_at.isoformat(),
            "metadata": json.dumps(self.metadata) if self.metadata else "{}",
        }


@dataclass(frozen=True)
class ConceptMapping:
    """
    Value object representing a complete mapping between concepts in a domain.

    Educational Patterns:
    - Aggregate of Value Objects: Composes multiple relationships
    - Collection Wrapper: Provides domain-specific operations on collections
    - Immutability: Prevents accidental modification of mappings

    Real-World Usage:
    - Complete knowledge graph for a subject domain
    - Learning path generation for educational platforms
    - Dependency analysis for curriculum design
    """

    concept_ids: FrozenSet[str]
    relationships: Tuple[ConceptRelationship, ...]
    domain: str
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """
        Validate mapping consistency.

        Educational Note: Aggregate validation ensures that
        all contained objects form a consistent whole.
        """
        if not self.domain or not self.domain.strip():
            raise ValueError("Domain cannot be empty")

        if len(self.concept_ids) == 0:
            raise ValueError("Mapping must contain at least one concept")

        # Validate that all relationships reference concepts in the mapping
        for rel in self.relationships:
            if rel.source_concept_id not in self.concept_ids:
                raise ValueError(
                    f"Relationship source '{rel.source_concept_id}' not in concept set"
                )
            if rel.target_concept_id not in self.concept_ids:
                raise ValueError(
                    f"Relationship target '{rel.target_concept_id}' not in concept set"
                )

    def get_prerequisites(self, concept_id: str) -> Set[str]:
        """
        Get all prerequisites for a given concept.

        Business Logic: Finds all concepts that must be learned
        before the given concept can be understood.
        """
        if concept_id not in self.concept_ids:
            raise ValueError(f"Concept '{concept_id}' not in mapping")

        prerequisites = set()
        for rel in self.relationships:
            if (
                rel.target_concept_id == concept_id
                and rel.relationship_type == RelationshipType.PREREQUISITE
            ):
                prerequisites.add(rel.source_concept_id)

        return prerequisites

    def get_enabled_concepts(self, concept_id: str) -> Set[str]:
        """
        Get all concepts enabled by learning the given concept.

        Business Logic: Finds concepts that become learnable
        after mastering the given concept.
        """
        if concept_id not in self.concept_ids:
            raise ValueError(f"Concept '{concept_id}' not in mapping")

        enabled = set()
        for rel in self.relationships:
            if (
                rel.source_concept_id == concept_id
                and rel.relationship_type == RelationshipType.ENABLES
            ):
                enabled.add(rel.target_concept_id)

        return enabled

    def get_foundational_concepts(self) -> Set[str]:
        """
        Get concepts with no prerequisites (learning starting points).

        Educational Algorithm: Identifies entry points into a knowledge domain
        that can be learned without prior concepts.
        """
        foundational = set(self.concept_ids)

        # Remove concepts that have prerequisites
        for rel in self.relationships:
            if rel.relationship_type == RelationshipType.PREREQUISITE:
                foundational.discard(rel.target_concept_id)

        return foundational

    def get_advanced_concepts(self) -> Set[str]:
        """
        Get concepts that enable many others (high-impact concepts).

        Educational Algorithm: Identifies concepts that unlock
        significant portions of a knowledge domain.
        """
        enablement_counts = {}

        for rel in self.relationships:
            if rel.relationship_type == RelationshipType.ENABLES:
                source = rel.source_concept_id
                enablement_counts[source] = enablement_counts.get(source, 0) + 1

        # Return concepts that enable 3 or more others
        return {concept for concept, count in enablement_counts.items() if count >= 3}

    def calculate_concept_centrality(self, concept_id: str) -> float:
        """
        Calculate centrality score for a concept in the graph.

        Educational Algorithm: Measures how "central" a concept is
        by counting its connections to other concepts.
        """
        if concept_id not in self.concept_ids:
            return 0.0

        weighted_score = 0.0

        for rel in self.relationships:
            if (
                rel.source_concept_id == concept_id
                or rel.target_concept_id == concept_id
            ):
                weighted_score += rel.calculate_weight()

        # Normalize by total possible connections
        max_connections = len(self.concept_ids) - 1
        if max_connections == 0:
            return 0.0

        return weighted_score / max_connections

    def get_learning_paths(self, target_concept: str) -> List[List[str]]:
        """
        Generate possible learning paths to reach a target concept.

        Educational Algorithm: Uses topological sorting to find
        valid sequences of concept learning that respect prerequisites.

        Note: This is a simplified version. A full implementation would
        use graph algorithms like DFS or BFS with cycle detection.
        """
        if target_concept not in self.concept_ids:
            raise ValueError(f"Target concept '{target_concept}' not in mapping")

        # Simplified implementation - just get direct prerequisites
        prerequisites = self.get_prerequisites(target_concept)
        if not prerequisites:
            return [[target_concept]]  # No prerequisites needed

        # Return paths through each prerequisite
        paths = []
        for prereq in prerequisites:
            paths.append([prereq, target_concept])

        return paths

    def filter_by_strength(self, min_strength: MappingStrength) -> "ConceptMapping":
        """
        Create new mapping with only strong relationships.

        Educational Pattern: Filtering with Immutability
        - Creates new object rather than modifying existing one
        - Allows different views of the same data
        - Maintains referential transparency
        """
        filtered_relationships = tuple(
            rel
            for rel in self.relationships
            if rel.strength.value >= min_strength.value
        )

        return ConceptMapping(
            concept_ids=self.concept_ids,
            relationships=filtered_relationships,
            domain=self.domain,
            version=f"{self.version}-filtered",
            metadata={
                **self.metadata,
                "filter_applied": f"min_strength_{min_strength.name}",
            },
        )

    def get_relationship_matrix(self) -> Dict[Tuple[str, str], ConceptRelationship]:
        """
        Get relationships as a matrix for efficient lookup.

        Educational Pattern: Data Structure Transformation
        - Optimizes for different access patterns
        - Trades memory for lookup speed
        - Demonstrates performance considerations in domain design
        """
        matrix = {}
        for rel in self.relationships:
            key = (rel.source_concept_id, rel.target_concept_id)
            matrix[key] = rel
        return matrix

    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary for serialization."""
        return {
            "concept_ids": list(self.concept_ids),
            "relationships": [rel.to_dict() for rel in self.relationships],
            "domain": self.domain,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "statistics": {
                "concept_count": len(self.concept_ids),
                "relationship_count": len(self.relationships),
                "foundational_concepts": len(self.get_foundational_concepts()),
                "advanced_concepts": len(self.get_advanced_concepts()),
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> "ConceptMapping":
        """
        Factory method to create mapping from dictionary.

        Educational Pattern: Factory Method with Validation
        - Handles data transformation and validation
        - Provides backward compatibility
        - Centralizes object creation logic
        """
        # Parse relationships
        relationships = []
        for rel_data in data.get("relationships", []):
            rel = ConceptRelationship(
                source_concept_id=rel_data["source"],
                target_concept_id=rel_data["target"],
                relationship_type=RelationshipType(rel_data["type"]),
                strength=MappingStrength[rel_data["strength"]],
                explanation=rel_data.get("explanation"),
                evidence_score=float(rel_data.get("evidence_score", 1.0)),
            )
            relationships.append(rel)

        # Parse timestamp if present
        created_at = datetime.now()
        if "created_at" in data:
            created_at = datetime.fromisoformat(data["created_at"])

        return cls(
            concept_ids=frozenset(data["concept_ids"]),
            relationships=tuple(relationships),
            domain=data["domain"],
            version=data.get("version", "1.0"),
            created_at=created_at,
            metadata=data.get("metadata", {}),
        )


# Educational Example Usage
def create_example_mapping() -> ConceptMapping:
    """
    Create an example concept mapping for educational demonstration.

    Educational Purpose:
    - Shows how to construct complex value objects
    - Demonstrates relationship modeling
    - Illustrates business logic in action
    """

    # Define concepts in ZFC set theory
    concepts = {"extensionality", "empty_set", "pairing", "union", "power_set"}

    # Define relationships
    relationships = [
        # Empty set depends on extensionality
        ConceptRelationship(
            source_concept_id="extensionality",
            target_concept_id="empty_set",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=MappingStrength.ESSENTIAL,
            explanation="Extensionality needed to prove uniqueness of empty set",
        ),
        # Pairing depends on extensionality
        ConceptRelationship(
            source_concept_id="extensionality",
            target_concept_id="pairing",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=MappingStrength.STRONG,
            explanation="Extensionality ensures uniqueness of pairs",
        ),
        # Union uses pairing
        ConceptRelationship(
            source_concept_id="pairing",
            target_concept_id="union",
            relationship_type=RelationshipType.PREREQUISITE,
            strength=MappingStrength.MODERATE,
            explanation="Union can be constructed using pairing",
        ),
        # Power set is related to all others
        ConceptRelationship(
            source_concept_id="union",
            target_concept_id="power_set",
            relationship_type=RelationshipType.RELATED,
            strength=MappingStrength.WEAK,
            explanation="Both deal with set construction",
        ),
    ]

    return ConceptMapping(
        concept_ids=frozenset(concepts),
        relationships=tuple(relationships),
        domain="zfc_set_theory",
        version="1.0",
        metadata={"description": "Basic ZFC axioms and constructions"},
    )


if __name__ == "__main__":
    # Demonstrate usage
    mapping = create_example_mapping()

    print(f"Domain: {mapping.domain}")
    print(f"Concepts: {len(mapping.concept_ids)}")
    print(f"Relationships: {len(mapping.relationships)}")
    print(f"Foundational concepts: {mapping.get_foundational_concepts()}")
    print(f"Advanced concepts: {mapping.get_advanced_concepts()}")

    # Show learning paths
    if "union" in mapping.concept_ids:
        paths = mapping.get_learning_paths("union")
        print(f"Learning paths to 'union': {paths}")

    # Show centrality scores
    for concept in sorted(mapping.concept_ids):
        centrality = mapping.calculate_concept_centrality(concept)
        print(f"Centrality of '{concept}': {centrality:.3f}")
