"""
Domain layer package - Core Business Logic Layer

This package contains the core business logic of the Research Paper Aggregator.
It's the innermost layer of our Clean Architecture implementation, containing:

- Entities: Objects with identity and lifecycle (e.g., ResearchPaper)
- Value Objects: Immutable objects without identity (e.g., SearchQuery, KeywordConfig)
- Domain Services: Business logic that doesn't naturally fit in entities
- Domain Events: Notifications of important domain occurrences

Educational Note - Clean Architecture Principles:
The domain layer should not depend on any external frameworks or libraries.
It represents pure business logic and should be testable in isolation.

Key Design Patterns Demonstrated:
- Entity Pattern: ResearchPaper has identity and lifecycle
- Value Object Pattern: SearchQuery and KeywordConfig are immutable
- Domain Service Pattern: Complex business logic extracted from entities
- Repository Pattern Interface: Defined here, implemented in infrastructure

SOLID Principles Applied:
- Single Responsibility: Each class has one reason to change
- Open/Closed: Extensible through interfaces, closed for modification
- Liskov Substitution: All implementations can substitute their interfaces
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depends on abstractions, not concretions
"""
