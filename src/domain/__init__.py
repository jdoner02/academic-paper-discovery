"""
Domain layer package.

This package contains the core business logic of the HRV Research Aggregator.
It's the innermost layer of our Clean Architecture, containing:

- Entities: Objects with identity and lifecycle
- Value Objects: Immutable objects without identity  
- Domain Services: Business logic that doesn't naturally fit in entities
- Domain Events: Notifications of important domain occurrences

Educational Note:
The domain layer should not depend on any external frameworks or libraries.
It represents pure business logic and should be testable in isolation.
"""
