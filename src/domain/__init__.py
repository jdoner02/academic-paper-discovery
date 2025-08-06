# Domain Layer - Pure Business Logic

"""
Domain Layer for Research Paper Discovery Platform.

This layer contains the core business logic and domain model for academic
paper concept extraction and visualization. It represents the heart of the
application - the concepts, rules, and behaviors that exist regardless of
external dependencies.

Educational Notes:
The Domain Layer in Clean Architecture must:
- Contain no dependencies on external frameworks or libraries
- Define the business entities, value objects, and domain services
- Encapsulate the most important business rules and logic
- Be testable in complete isolation
- Remain stable when outer layers change

Components:
- entities/: Objects with identity and lifecycle (Paper, ConceptNode, ConceptTree)
- value_objects/: Immutable objects without identity (EmbeddingVector, EvidenceSentence)
- services/: Domain logic that doesn't naturally fit in entities

Design Principles Applied:
- Entity vs Value Object distinction based on identity requirements
- Rich domain models with behavior, not just data structures
- Domain services for operations spanning multiple entities
- Immutable value objects for thread safety and predictability

Academic Context:
Research paper analysis involves complex conceptual relationships that
mirror how researchers naturally think about literature. The domain model
reflects these natural concepts: papers contain concepts, concepts form
hierarchies, evidence supports concepts, and relationships connect ideas.
"""

from .entities import *
from .value_objects import *
from .services import *
