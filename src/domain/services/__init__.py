# Domain Services Package

"""
Domain Services - Business Logic That Doesn't Fit in Entities.

Domain Services contain business logic that:
- Operates on multiple entities or value objects
- Doesn't naturally belong to a single entity
- Represents a domain concept that is naturally an operation
- Maintains stateless behavior (no instance variables)

Educational Notes:
Domain Services solve the problem of where to put business logic
that spans multiple domain objects. They maintain the domain layer's
purity while providing a home for complex operations.

When to Use Domain Services:
- Operations involving multiple entities
- Calculations using domain knowledge
- Complex validation across object boundaries
- Algorithms that are domain concepts themselves

Design Principles:
- Stateless: No instance state, only behavior
- Dependency Injection: Receive dependencies as parameters
- Pure Functions: Predictable outputs for given inputs
- Single Responsibility: Each service has one clear purpose
- Interface Segregation: Small, focused interfaces

Examples in This Domain:
- ConceptExtractionService: Transforms papers into concept hierarchies
- HierarchyBuilderService: Constructs hierarchical relationships
- SimilarityCalculatorService: Computes semantic relationships

Academic Context:
Concept extraction is naturally a service - it operates on collections
of papers and produces concept trees. The algorithm itself is a
domain concept that researchers understand and discuss.
"""

# Import all domain service classes for convenient access
# These will be created in TDD Cycle 2-4
