# Application Layer - Use Cases and Ports

The application layer orchestrates domain objects to fulfill specific use cases. This is where we define **how** the system accomplishes business goals.

## Educational Notes

### Application Layer Responsibilities

1. **Use Case Orchestration**: Coordinates domain objects to fulfill business scenarios
2. **Interface Definition**: Defines contracts for external dependencies (ports)
3. **Transaction Management**: Ensures data consistency across operations
4. **Security Enforcement**: Implements authorization and access control
5. **Workflow Coordination**: Manages complex multi-step processes

### Key Patterns Demonstrated

#### Use Case Pattern
Each use case represents a single business operation:
- `ExecuteKeywordSearchUseCase`: Orchestrates paper search workflow
- `ExtractPaperConceptsUseCase`: Manages concept extraction from papers

#### Port-Adapter Pattern (Hexagonal Architecture)
Ports define interfaces for external dependencies:
- `PaperRepositoryPort`: Abstract contract for paper storage
- `ConceptRepositoryPort`: Abstract contract for concept storage
- `PdfExtractorPort`: Abstract contract for PDF processing

### Dependency Direction

```
Use Cases → Domain Objects
Use Cases → Ports (Interfaces)
Infrastructure → Ports (Implementations)
```

The application layer depends on domain abstractions, not concrete implementations.

## Use Cases (`use_cases/`)

### ExecuteKeywordSearchUseCase

**Purpose**: Coordinate paper discovery based on keyword strategies

**Educational Value**:
- Demonstrates Command pattern for encapsulating operations
- Shows transaction-like behavior with rollback capability
- Illustrates error handling and logging best practices

**Workflow**:
1. Validate search parameters
2. Load keyword configuration
3. Execute search across multiple sources
4. Filter and rank results
5. Store results for future reference

### ExtractPaperConceptsUseCase

**Purpose**: Extract and structure concepts from academic papers

**Educational Value**:
- Shows Strategy pattern for pluggable algorithms
- Demonstrates batch processing patterns
- Illustrates progress tracking and error recovery

**Workflow**:
1. Load paper content
2. Apply concept extraction strategies
3. Build concept hierarchies
4. Validate extracted concepts
5. Store in knowledge graph

## Ports (`ports/`)

### Why Ports Matter

Ports enable:
- **Testability**: Mock implementations for unit tests
- **Flexibility**: Swap implementations without changing business logic
- **Isolation**: Business logic independent of technical details

### Port Design Principles

1. **Interface Segregation**: Small, focused contracts
2. **Stable Abstractions**: Change less frequently than implementations
3. **Domain-Centric**: Designed from domain perspective, not technical constraints

## Concept Map Connections

- [Use Case Pattern](../../../concept_storage/concepts/application_architecture/use_case_pattern.md)
- [Port-Adapter Pattern](../../../concept_storage/concepts/application_architecture/hexagonal_architecture.md)
- [Command Pattern](../../../concept_storage/concepts/design_patterns/command_pattern.md)
- [Strategy Pattern](../../../concept_storage/concepts/design_patterns/strategy_pattern.md)

## Testing Strategy

### Use Case Testing
```python
def test_execute_keyword_search_use_case():
    # Arrange: Mock all dependencies
    mock_repository = MockPaperRepository()
    mock_extractor = MockPdfExtractor()
    use_case = ExecuteKeywordSearchUseCase(mock_repository, mock_extractor)
    
    # Act: Execute the use case
    result = use_case.execute(search_query)
    
    # Assert: Verify business logic worked correctly
    assert len(result.papers) == expected_count
    assert all(paper.matches_criteria(search_query) for paper in result.papers)
```

### Port Testing
```python
def test_paper_repository_port_contract():
    # Test that all implementations satisfy the contract
    repositories = [InMemoryPaperRepository(), ArxivPaperRepository()]
    for repo in repositories:
        assert isinstance(repo, PaperRepositoryPort)
        # Test contract compliance
```

## Industry Best Practices

1. **Single Responsibility**: Each use case does one thing well
2. **Dependency Inversion**: Depend on interfaces, not implementations
3. **Open/Closed Principle**: Easy to add new use cases without modification
4. **Fail Fast**: Validate inputs early and provide clear error messages

This layer bridges pure business logic with technical implementation, making your system both flexible and maintainable.
