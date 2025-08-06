# Domain Entities Package

"""
Domain Entities - Objects with Identity and Lifecycle.

Entities are the core business objects that have:
- A unique identity that persists through changes
- A lifecycle with creation, modification, and potential deletion
- Business behavior and rules, not just data
- Equality based on identity, not attributes

Educational Notes:
Entities represent the "things" that matter to the business domain.
In academic research, these are concepts like papers (with DOI identity),
concept nodes (with position in hierarchy), and concept trees (with
scope and domain identity).

The key distinction from Value Objects:
- Entities: Identity-based equality, mutable state, complex lifecycle
- Value Objects: Attribute-based equality, immutable, simple creation

Entity Design Patterns:
- Rich domain models with business behavior
- Identity assignment strategies (natural vs surrogate keys)
- Encapsulation of business rules and validation
- Factory methods for complex construction
- Repository interfaces for persistence abstraction

Real-World Application:
Research papers have persistent identity (DOI, ArXiv ID) that survives
metadata updates. Concept nodes maintain identity within hierarchies
even as their relationships change. These natural identities make
entities the appropriate pattern choice.
"""

# Import all entity classes for convenient access
# These will be created in TDD Cycle 1
