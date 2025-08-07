"""
Infrastructure Layer

This directory contains the infrastructure implementations for our research aggregation system.

Purpose:
The infrastructure layer implements the ports (interfaces) defined in the application layer,
providing concrete implementations for external concerns like data persistence, APIs, and external services.

Clean Architecture Role:
- Dependency Direction: Infrastructure depends on Application layer, not the reverse
- Interface Implementation: Concrete implementations of application ports
- External Concerns: Handles databases, APIs, file systems, and other I/O operations
- Flexibility: Multiple implementations of the same port for different environments

Directory Structure:
- repositories/: Data access implementations
- apis/: External API integrations
- databases/: Database-specific implementations
- config/: Configuration and settings

Implementations:
- InMemoryPaperRepository: In-memory storage for testing and development
- DatabasePaperRepository: Database persistence (PostgreSQL/SQLite)
- PubMedRepository: PubMed API integration for medical papers
- ArXivRepository: arXiv API integration for preprint papers

Educational Notes:
This layer demonstrates:
- Repository Pattern: Different storage implementations with same interface
- Adapter Pattern: External APIs adapted to our domain models
- Strategy Pattern: Pluggable implementations based on configuration
- Dependency Inversion: High-level policies don't depend on low-level details
"""
