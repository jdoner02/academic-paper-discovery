"""
Infrastructure Layer Tests - Testing external system integrations.

The infrastructure layer contains implementations that interact with external
systems like databases, APIs, file systems, and third-party services. These
tests ensure that our adapters properly implement the port interfaces and
handle external system interactions correctly.

Educational Notes:
- Infrastructure layer implements the ports defined by the application layer
- Contains adapters that translate between domain concepts and external systems
- Should be the most "disposable" part of the architecture
- Tests here often require mocking of external dependencies

Design Patterns:
- Adapter Pattern: Adapts external interfaces to our port interfaces
- Repository Pattern: Abstracts data access behind a domain-friendly interface
- Gateway Pattern: Provides access to external services

Testing Challenges:
1. External dependencies need to be mocked
2. Network calls, file I/O, and database operations are slow
3. External APIs may change or be unreliable
4. Need to test both success and failure scenarios

Directory Structure:
- repositories/: Tests for data access implementations

Testing Philosophy:
Infrastructure tests should:
1. Mock external systems to ensure fast, reliable tests
2. Test error handling for external system failures
3. Verify proper translation between external and domain formats
4. Ensure port contract compliance
5. Test configuration and connection management
"""
