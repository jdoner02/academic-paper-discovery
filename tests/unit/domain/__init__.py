"""
Domain Layer Tests - Testing the heart of our business logic.

The domain layer contains the core business logic and rules of our application.
It is independent of external concerns and focuses purely on the problem domain.
These tests ensure that our business logic is correct, robust, and well-encapsulated.

Educational Notes:
- Domain layer is the most important part of Clean Architecture
- Contains entities, value objects, and domain services
- Should have no dependencies on external frameworks or infrastructure
- Business rules and logic are encapsulated here

Clean Architecture Principles:
1. Domain entities represent core business concepts
2. Value objects represent immutable domain concepts
3. Domain services contain business logic that doesn't fit naturally in entities
4. All dependencies point inward (Dependency Rule)

Directory Structure:
- entities/: Tests for objects with identity and lifecycle
- value_objects/: Tests for immutable domain concepts
- services/: Tests for domain business logic

Testing Philosophy:
Domain tests should be the most comprehensive since they test the most
critical business logic. They should not require mocks since domain
objects should be self-contained.
"""
