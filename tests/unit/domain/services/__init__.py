"""
Domain Service Tests - Validating business logic that spans multiple entities.

Domain services contain business logic that doesn't naturally fit within a single
entity or value object. They coordinate between multiple domain objects and
implement complex business operations while remaining within the domain layer.
These tests ensure that domain services properly implement business rules.

Educational Notes:
- Domain services contain business logic that spans multiple entities
- They remain within the domain layer (no external dependencies)
- Should be stateless and focused on specific business operations
- Different from application services (which coordinate with infrastructure)

Design Patterns:
- Service Pattern: Encapsulates business operations as services
- Strategy Pattern: Different algorithms for business operations
- Template Method: Common workflow with varying implementations

When to Use Domain Services:
1. Business logic spans multiple entities
2. Operation doesn't naturally belong to any single entity
3. Complex business rules need coordination
4. Stateless operations that transform domain objects

Testing Philosophy:
Domain service tests should:
1. Focus on business rule validation
2. Test with real domain objects (minimal mocking)
3. Verify state changes in coordinated entities
4. Ensure proper error handling for business rule violations
5. Test edge cases and boundary conditions

SOLID Principles in Domain Services:
- Single Responsibility: Each service has one business purpose
- Open/Closed: Extensible through strategy patterns
- Dependency Inversion: Depend on abstractions, not concretions
"""
