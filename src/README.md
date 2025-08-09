# Academic Paper Discovery - Core Backend

This directory contains the Python backend implementation following Clean Architecture principles.

## Architecture Overview

This implementation demonstrates **Clean Architecture** by Uncle Bob Martin, organizing code into distinct layers with clear dependency rules:

```
Domain ← Application ← Infrastructure
   ↑         ↑            ↑
   └─────────┴────────────┘
   (Dependencies point inward)
```

## Educational Value

### Clean Architecture Principles Demonstrated

1. **Dependency Inversion**: Infrastructure depends on domain abstractions
2. **Single Responsibility**: Each layer has one primary concern
3. **Open/Closed Principle**: Easy to extend without modifying existing code
4. **Interface Segregation**: Small, focused interfaces in ports/

### Domain-Driven Design Concepts

- **Entities**: Objects with identity (`ResearchPaper`, `Concept`)
- **Value Objects**: Immutable concepts (`SearchQuery`, `KeywordConfig`)
- **Domain Services**: Business logic that doesn't fit in entities
- **Repositories**: Abstract data access patterns

## Layer Responsibilities

### Domain Layer (`domain/`)
- Contains business rules and logic
- No dependencies on external frameworks
- Defines the core problem we're solving

### Application Layer (`application/`)
- Orchestrates domain objects
- Defines use cases and abstract interfaces
- Coordinates between domain and infrastructure

### Infrastructure Layer (`infrastructure/`)
- Implements external concerns
- Database access, file systems, APIs
- Adapts external formats to domain models

## Concept Map Connections

- [Clean Architecture Pattern](../../concept_storage/concepts/software_architecture/clean_architecture.md)
- [Domain-Driven Design](../../concept_storage/concepts/software_design/domain_driven_design.md)
- [Repository Pattern](../../concept_storage/concepts/design_patterns/repository_pattern.md)
- [Dependency Inversion](../../concept_storage/concepts/solid_principles/dependency_inversion.md)

## Getting Started

1. Start with `domain/` to understand the business concepts
2. Review `application/use_cases/` to see how domain objects are orchestrated
3. Examine `infrastructure/` to understand external integrations

## Testing Strategy

- **Unit Tests**: Focus on domain logic and individual components
- **Integration Tests**: Test use cases with real implementations
- **Acceptance Tests**: Validate entire workflows end-to-end

This structure supports Test-Driven Development and maintains high code quality through clear separation of concerns.
