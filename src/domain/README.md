# Domain Layer - Business Logic Core

The domain layer contains the heart of our academic paper discovery system. This is where we define **what** our system does, independent of **how** it does it.

## Educational Notes

### Why Domain Layer Matters

The domain layer is the most important part of Clean Architecture because:

1. **Business Rules Live Here**: Core logic that would exist regardless of technology
2. **Technology Independent**: No databases, frameworks, or external dependencies
3. **Testable**: Pure business logic is easy to unit test
4. **Stable**: Changes least frequently as business rules are more stable than technology

### Domain-Driven Design Patterns

#### Entities (`entities/`)
Objects with identity that persist over time:
- `ResearchPaper`: Has DOI, title, content - identity persists even if content changes
- `Concept`: Represents academic concepts with hierarchical relationships
- `ConceptHierarchy`: Manages parent-child relationships between concepts

#### Value Objects (`value_objects/`)
Immutable objects defined by their values:
- `SearchQuery`: Encapsulates search criteria and parameters
- `KeywordConfig`: Configuration for keyword extraction strategies
- `PaperFingerprint`: Unique identifier combining multiple paper attributes

#### Domain Services (`services/`)
Business logic that doesn't naturally fit in entities:
- `ConceptExtractor`: Sophisticated algorithms for extracting concepts from text
- `ConceptHierarchyBuilder`: Logic for constructing concept relationships

## Key Design Decisions

### Entity vs Value Object Decision Framework

**Use Entity When:**
- Object has unique identity (DOI, UUID, etc.)
- Identity persists through attribute changes
- Object has lifecycle and mutable state
- Equality based on identity, not attributes

**Use Value Object When:**
- Object represents a concept without identity
- Immutable after creation
- Equality based on all attributes
- Can be freely shared and cached

### Example: Why ResearchPaper is an Entity

```python
# Identity-based equality
paper1 = ResearchPaper(doi="10.1234/example", title="Original Title")
paper2 = ResearchPaper(doi="10.1234/example", title="Updated Title")
assert paper1 == paper2  # Same DOI = same paper, despite different titles
```

### Example: Why SearchQuery is a Value Object

```python
# Value-based equality
query1 = SearchQuery(terms=["machine learning"], date_range=(2020, 2023))
query2 = SearchQuery(terms=["machine learning"], date_range=(2020, 2023))
assert query1 == query2  # Same values = same query
```

## Concept Map Connections

- [Entity Pattern](../../../concept_storage/concepts/domain_modeling/entity_pattern.md)
- [Value Object Pattern](../../../concept_storage/concepts/domain_modeling/value_object_pattern.md)
- [Domain Services](../../../concept_storage/concepts/domain_modeling/domain_services.md)
- [Ubiquitous Language](../../../concept_storage/concepts/domain_modeling/ubiquitous_language.md)

## Industry Applications

This domain modeling approach is used in:
- **E-commerce**: Product (entity) vs Price (value object)
- **Financial Systems**: Account (entity) vs Money (value object)
- **Content Management**: Article (entity) vs Tag (value object)
- **Academic Research**: Paper (entity) vs Citation (value object)

## Best Practices Demonstrated

1. **Rich Domain Models**: Entities contain behavior, not just data
2. **Immutable Value Objects**: Thread-safe and cacheable
3. **Expressive Type System**: Types that communicate intent
4. **Validation at Boundaries**: Domain objects validate their own invariants

Study this layer first to understand the problem domain before diving into technical implementation details.
