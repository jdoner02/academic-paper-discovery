"""
Application Layer Integration Tests.

These tests validate that application layer components (use cases and ports)
integrate correctly with domain and infrastructure layers. They focus on
testing the orchestration logic and ensuring proper delegation to domain
services and repositories.

Educational Notes:
- Application layer coordinates business operations
- Use cases should delegate to domain objects and repositories
- Tests validate proper error handling and data flow
- Configuration integration is critical for research tools

Testing Focus:
- Use case execution with real repositories
- Configuration loading and strategy selection
- Error propagation from infrastructure to application
- Batch operations and workflow coordination
"""
