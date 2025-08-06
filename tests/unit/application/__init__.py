"""
Application Layer Tests - Testing the orchestration of business logic.

This module contains tests for the application layer of our Clean Architecture implementation.
The application layer is responsible for orchestrating domain objects and coordinating
business operations through use cases.

Educational Notes:
- Application layer tests focus on workflow orchestration, not business rules
- Use cases should be tested in isolation using mocked dependencies (ports)
- These tests verify that the application correctly delegates to domain objects
- They ensure proper error handling and input validation at the application boundary

Directory Structure:
- use_cases/: Tests for business operation orchestration
- ports/: Tests for abstract interfaces and contracts

Testing Philosophy:
Application layer tests should verify that use cases correctly:
1. Validate input parameters
2. Delegate to appropriate domain services and repositories
3. Handle errors gracefully
4. Return appropriate results or raise meaningful exceptions
"""
