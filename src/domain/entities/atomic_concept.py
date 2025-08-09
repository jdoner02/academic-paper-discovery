"""
Atomic Concept Domain Entity

Represents fundamental mathematical and logical concepts that serve as building blocks
for more complex knowledge domains.

Educational Purpose:
- Demonstrates Domain Entity pattern with rich business logic
- Shows immutability and value object composition
- Illustrates how domain entities encapsulate business rules
- Examples of defensive programming and validation

Real-World Application:
- Used in educational platforms to model prerequisite knowledge
- Applied in AI systems for knowledge representation
- Utilized in formal verification and theorem proving systems
"""

from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict, Any
from enum import Enum
import re
from datetime import datetime


class ConceptLevel(Enum):
    """
    Academic levels for concept complexity.

    Educational Note: Enums provide type safety and clear business rules.
    This prevents invalid states and makes the domain model self-documenting.
    """

    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    RESEARCH = "research"

    @classmethod
    def from_string(cls, level_str: str) -> "ConceptLevel":
        """
        Factory method for creating ConceptLevel from string.

        Educational Pattern: Factory Method
        - Encapsulates object creation logic
        - Provides validation and error handling
        - Makes client code cleaner and more robust
        """
        level_mapping = {
            "elementary": cls.ELEMENTARY,
            "middle_school": cls.MIDDLE_SCHOOL,
            "high_school": cls.HIGH_SCHOOL,
            "undergraduate": cls.UNDERGRADUATE,
            "graduate": cls.GRADUATE,
            "research": cls.RESEARCH,
        }

        normalized = level_str.lower().replace(" ", "_").replace("-", "_")
        if normalized not in level_mapping:
            raise ValueError(f"Invalid concept level: {level_str}")

        return level_mapping[normalized]


class ConceptType(Enum):
    """
    Types of mathematical/logical concepts.

    Educational Note: This taxonomy helps organize knowledge
    and enables different processing strategies for each type.
    """

    AXIOM = "axiom"  # Fundamental assumptions
    THEOREM = "theorem"  # Proven statements
    DEFINITION = "definition"  # Formal concept definitions
    LEMMA = "lemma"  # Supporting propositions
    COROLLARY = "corollary"  # Direct consequences
    CONJECTURE = "conjecture"  # Unproven propositions
    ALGORITHM = "algorithm"  # Computational procedures


@dataclass(frozen=True)
class ConceptMetadata:
    """
    Value object containing concept metadata.

    Educational Pattern: Value Object
    - Immutable to prevent accidental modification
    - Groups related data with clear meaning
    - Provides validation in constructor
    - Enables safe passing without defensive copying
    """

    timestamp: datetime
    source: str
    confidence_score: float
    pedagogical_notes: List[str] = field(default_factory=list)
    historical_context: Optional[str] = None
    applications: List[str] = field(default_factory=list)

    def __post_init__(self):
        """
        Validation in value object constructor.

        Educational Note: Defensive programming ensures object invariants
        are maintained throughout the object's lifetime.
        """
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")

        if not self.source.strip():
            raise ValueError("Source cannot be empty")


@dataclass
class AtomicConcept:
    """
    Domain entity representing a fundamental mathematical or logical concept.

    Educational Patterns Demonstrated:
    - Entity Pattern: Has identity and encapsulates business logic
    - Aggregate Root: Manages consistency of related objects
    - Domain Events: Can raise events for integration
    - Specification Pattern: Used for complex queries

    Real-World Usage:
    - Knowledge management systems
    - Educational platforms with prerequisite tracking
    - AI reasoning systems
    - Formal verification tools
    """

    # Identity - what makes this concept unique
    id: str
    name: str

    # Core concept definition
    formal_statement: str
    informal_description: str
    mathematical_definition: Optional[str] = None

    # Classification
    concept_type: ConceptType = ConceptType.DEFINITION
    level: ConceptLevel = ConceptLevel.UNDERGRADUATE
    domain: str = "mathematics"
    subdomain: Optional[str] = None

    # Relationships to other concepts
    prerequisites: Set[str] = field(default_factory=set)
    enables: Set[str] = field(default_factory=set)
    related_concepts: Set[str] = field(default_factory=set)

    # Educational content
    examples: List[Dict[str, Any]] = field(default_factory=list)
    counterexamples: List[Dict[str, Any]] = field(default_factory=list)
    proof_sketches: List[Dict[str, Any]] = field(default_factory=list)

    # Metadata
    metadata: Optional[ConceptMetadata] = None
    tags: Set[str] = field(default_factory=set)

    def __post_init__(self):
        """
        Entity validation and initialization.

        Educational Note: Entities should validate their invariants
        to maintain consistency and prevent invalid states.
        """
        self._validate_identity()
        self._validate_content()
        self._normalize_relationships()

    def _validate_identity(self) -> None:
        """
        Validate entity identity requirements.

        Business Rule: Atomic concepts must have unique, meaningful identifiers
        that follow naming conventions for interoperability.
        """
        if not self.id or not self.id.strip():
            raise ValueError("Atomic concept must have a non-empty ID")

        if not self.name or not self.name.strip():
            raise ValueError("Atomic concept must have a non-empty name")

        # Educational: Regex validation for naming conventions
        id_pattern = r"^[a-zA-Z][a-zA-Z0-9_]*$"
        if not re.match(id_pattern, self.id):
            raise ValueError(
                f"Concept ID '{self.id}' must start with letter and contain only "
                "letters, numbers, and underscores"
            )

    def _validate_content(self) -> None:
        """
        Validate concept content requirements.

        Business Rule: All concepts must have meaningful descriptions
        that support learning and understanding.
        """
        if not self.formal_statement.strip():
            raise ValueError("Formal statement cannot be empty")

        if not self.informal_description.strip():
            raise ValueError("Informal description cannot be empty")

        if len(self.informal_description) < 10:
            raise ValueError("Informal description must be at least 10 characters")

    def _normalize_relationships(self) -> None:
        """
        Normalize relationship data for consistency.

        Educational Note: Data normalization prevents inconsistencies
        and makes the model more reliable for business operations.
        """
        # Remove self-references (a concept cannot be its own prerequisite)
        self.prerequisites.discard(self.id)
        self.enables.discard(self.id)
        self.related_concepts.discard(self.id)

        # Convert to lowercase for case-insensitive matching
        self.tags = {tag.lower().strip() for tag in self.tags if tag.strip()}

    # Business Logic Methods

    def add_prerequisite(self, prerequisite_id: str) -> None:
        """
        Add a prerequisite concept.

        Business Rule: Prerequisites form a directed acyclic graph (DAG)
        to prevent circular dependencies in learning paths.

        Educational Pattern: Command Method
        - Encapsulates a business operation
        - Maintains object invariants
        - Provides clear interface for domain operations
        """
        if prerequisite_id == self.id:
            raise ValueError("Concept cannot be its own prerequisite")

        if prerequisite_id in self.enables:
            raise ValueError(
                f"Cannot add {prerequisite_id} as prerequisite: "
                "it would create a circular dependency"
            )

        self.prerequisites.add(prerequisite_id)

    def add_enabled_concept(self, enabled_id: str) -> None:
        """
        Add a concept that this one enables.

        Business Rule: Maintain consistency between prerequisites and enables
        to support bidirectional navigation of the knowledge graph.
        """
        if enabled_id == self.id:
            raise ValueError("Concept cannot enable itself")

        if enabled_id in self.prerequisites:
            raise ValueError(
                f"Cannot enable {enabled_id}: it's a prerequisite of this concept"
            )

        self.enables.add(enabled_id)

    def is_foundational(self) -> bool:
        """
        Check if this is a foundational concept (has no prerequisites).

        Business Rule: Foundational concepts serve as entry points
        into knowledge domains and should be learned first.
        """
        return len(self.prerequisites) == 0

    def is_advanced(self) -> bool:
        """
        Check if this is an advanced concept (enables many others).

        Business Logic: Advanced concepts are those that unlock
        significant portions of a knowledge domain.
        """
        return len(self.enables) >= 3

    def calculate_complexity_score(self) -> float:
        """
        Calculate a complexity score based on prerequisites and level.

        Educational Algorithm: Demonstrates how business rules can be
        implemented as calculations that support decision-making.

        Returns:
            Float between 0.0 (simple) and 1.0 (complex)
        """
        # Base complexity from academic level
        level_scores = {
            ConceptLevel.ELEMENTARY: 0.1,
            ConceptLevel.MIDDLE_SCHOOL: 0.2,
            ConceptLevel.HIGH_SCHOOL: 0.3,
            ConceptLevel.UNDERGRADUATE: 0.5,
            ConceptLevel.GRADUATE: 0.7,
            ConceptLevel.RESEARCH: 0.9,
        }

        base_score = level_scores.get(self.level, 0.5)

        # Additional complexity from prerequisites
        prereq_complexity = min(len(self.prerequisites) * 0.1, 0.4)

        # Type-based complexity modifier
        type_modifiers = {
            ConceptType.AXIOM: 0.0,  # Axioms are foundational
            ConceptType.DEFINITION: 0.1,  # Definitions are basic
            ConceptType.THEOREM: 0.3,  # Theorems require proof
            ConceptType.ALGORITHM: 0.2,  # Algorithms have implementation complexity
            ConceptType.CONJECTURE: 0.4,  # Conjectures are speculative
        }

        type_modifier = type_modifiers.get(self.concept_type, 0.1)

        # Combine scores with weights
        final_score = (
            (base_score * 0.5) + (prereq_complexity * 0.3) + (type_modifier * 0.2)
        )
        return min(final_score, 1.0)

    def get_learning_prerequisites(self) -> List[str]:
        """
        Get prerequisites in suggested learning order.

        Business Logic: Sorts prerequisites by complexity to suggest
        an optimal learning sequence for students.

        Note: This would typically query other AtomicConcept entities
        to get their complexity scores for proper sorting.
        """
        # For now, return as list (would be enhanced with actual sorting)
        return sorted(list(self.prerequisites))

    def matches_search_criteria(self, criteria: Dict[str, Any]) -> bool:
        """
        Check if concept matches search criteria.

        Educational Pattern: Specification Pattern
        - Encapsulates complex business rules for queries
        - Makes filtering logic reusable and testable
        - Supports composition of multiple criteria
        """
        # Search by domain
        if "domain" in criteria and criteria["domain"] != self.domain:
            return False

        # Search by level
        if "level" in criteria and criteria["level"] != self.level:
            return False

        # Search by type
        if "concept_type" in criteria and criteria["concept_type"] != self.concept_type:
            return False

        # Search by keywords in name or description
        if "keywords" in criteria:
            searchable_text = f"{self.name} {self.informal_description}".lower()
            keywords = [kw.lower() for kw in criteria["keywords"]]
            if not any(kw in searchable_text for kw in keywords):
                return False

        # Search by tags
        if "tags" in criteria:
            required_tags = set(tag.lower() for tag in criteria["tags"])
            if not required_tags.issubset(self.tags):
                return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Educational Note: Separation of concerns - domain entities
        shouldn't know about persistence, but can provide data
        for infrastructure adapters to serialize.
        """
        return {
            "id": self.id,
            "name": self.name,
            "formal_statement": self.formal_statement,
            "informal_description": self.informal_description,
            "mathematical_definition": self.mathematical_definition,
            "concept_type": self.concept_type.value,
            "level": self.level.value,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "prerequisites": list(self.prerequisites),
            "enables": list(self.enables),
            "related_concepts": list(self.related_concepts),
            "examples": self.examples,
            "counterexamples": self.counterexamples,
            "proof_sketches": self.proof_sketches,
            "tags": list(self.tags),
            "complexity_score": self.calculate_complexity_score(),
            "is_foundational": self.is_foundational(),
            "is_advanced": self.is_advanced(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AtomicConcept":
        """
        Factory method to create from dictionary.

        Educational Pattern: Factory Method with validation
        - Centralizes object creation logic
        - Provides data validation and transformation
        - Handles backward compatibility and migration
        """
        # Handle enum conversions
        concept_type = ConceptType(data.get("concept_type", "definition"))
        level = ConceptLevel.from_string(data.get("level", "undergraduate"))

        # Create metadata if present
        metadata = None
        if "metadata" in data:
            metadata = ConceptMetadata(**data["metadata"])

        return cls(
            id=data["id"],
            name=data["name"],
            formal_statement=data["formal_statement"],
            informal_description=data["informal_description"],
            mathematical_definition=data.get("mathematical_definition"),
            concept_type=concept_type,
            level=level,
            domain=data.get("domain", "mathematics"),
            subdomain=data.get("subdomain"),
            prerequisites=set(data.get("prerequisites", [])),
            enables=set(data.get("enables", [])),
            related_concepts=set(data.get("related_concepts", [])),
            examples=data.get("examples", []),
            counterexamples=data.get("counterexamples", []),
            proof_sketches=data.get("proof_sketches", []),
            metadata=metadata,
            tags=set(data.get("tags", [])),
        )

    def __str__(self) -> str:
        """String representation for debugging and logging."""
        return f"AtomicConcept(id='{self.id}', name='{self.name}', level={self.level.value})"

    def __repr__(self) -> str:
        """Developer representation showing key attributes."""
        return (
            f"AtomicConcept(id='{self.id}', type={self.concept_type.value}, "
            f"prerequisites={len(self.prerequisites)}, enables={len(self.enables)})"
        )


# Educational Example Usage
def create_example_concepts() -> List[AtomicConcept]:
    """
    Create example atomic concepts for educational demonstration.

    Educational Purpose:
    - Shows how to use the AtomicConcept entity properly
    - Demonstrates relationship building between concepts
    - Illustrates validation and business rule enforcement
    """

    # Foundational axiom - no prerequisites
    extensionality = AtomicConcept(
        id="zfc_axiom_extensionality",
        name="Axiom of Extensionality",
        formal_statement="∀A ∀B (A = B ↔ ∀x (x ∈ A ↔ x ∈ B))",
        informal_description="Two sets are equal if and only if they have the same elements",
        concept_type=ConceptType.AXIOM,
        level=ConceptLevel.UNDERGRADUATE,
        domain="set_theory",
        subdomain="zfc_axioms",
        tags={"zfc", "axiom", "set_equality", "foundation"},
    )

    # Empty set concept - depends on extensionality
    empty_set = AtomicConcept(
        id="empty_set_concept",
        name="Empty Set",
        formal_statement="∃A ∀x (x ∉ A)",
        informal_description="A set containing no elements, denoted ∅ or {}",
        concept_type=ConceptType.DEFINITION,
        level=ConceptLevel.HIGH_SCHOOL,
        domain="set_theory",
        subdomain="basic_sets",
        prerequisites={"zfc_axiom_extensionality"},
        tags={"empty_set", "basic_sets", "cardinality"},
    )

    # Add the relationship bidirectionally
    extensionality.add_enabled_concept("empty_set_concept")

    return [extensionality, empty_set]


if __name__ == "__main__":
    # Demonstrate usage
    concepts = create_example_concepts()

    for concept in concepts:
        print(f"\n{concept}")
        print(f"Complexity Score: {concept.calculate_complexity_score():.2f}")
        print(f"Foundational: {concept.is_foundational()}")
        print(f"Prerequisites: {concept.prerequisites}")
        print(f"Enables: {concept.enables}")
