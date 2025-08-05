"""
Application layer package.

This package contains the application services, use cases, and ports that
orchestrate domain objects to fulfill business use cases. It's the middle
layer of our Clean Architecture.

Key Components:
- Use Cases: Single business operations (SearchPapersUseCase, etc.)
- Ports: Abstract interfaces for external dependencies
- Application Services: Coordinate multiple use cases
- DTOs: Data Transfer Objects for crossing boundaries

Educational Notes:
- Application layer depends on domain layer but not infrastructure
- Use cases contain application-specific business logic
- Ports define what the application needs from external systems
- This layer orchestrates domain objects without containing business rules

Clean Architecture Principle:
The application layer translates external requests into domain operations
and coordinates the domain objects to fulfill the use case.
"""
