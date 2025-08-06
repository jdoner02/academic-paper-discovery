"""
Integration Tests - Testing component interactions and system boundaries.

Integration tests verify that different components of our Clean Architecture
work correctly together. Unlike unit tests that test components in isolation,
integration tests validate that the interfaces between layers function properly
and that data flows correctly through the system.

Educational Notes:
- Integration tests validate architectural boundaries
- They test the "seams" where components connect
- Focus on data transformation between layers
- Verify error propagation and handling
- Test configuration and dependency injection

Integration Test Categories:
1. Application Integration: Use cases + repositories
2. Domain Integration: Services + entities + value objects
3. Infrastructure Integration: External APIs + file systems

Testing Philosophy:
- Use real domain objects, mock external dependencies
- Test realistic data flows and transformations
- Verify proper error handling across boundaries
- Focus on architectural compliance and design validation

Directory Structure:
- application/: Tests for application layer integration
- domain/: Tests for domain layer component integration
- infrastructure/: Tests for infrastructure layer integration

Design Patterns Demonstrated:
- Repository Pattern: Data access abstraction
- Dependency Injection: Loose coupling between layers
- Adapter Pattern: External system integration
- Command Pattern: Use case execution and coordination
"""
