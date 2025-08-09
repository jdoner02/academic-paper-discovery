# Clean Architecture Implementation

## Overview

This document details how the Academic Paper Discovery System implements Clean Architecture principles to achieve maintainability, testability, and independence from external frameworks.

## Clean Architecture Principles

### Dependency Rule
Dependencies must point inward toward the domain. Outer layers can depend on inner layers, but never the reverse.

```
┌─────────────────────────────────────────────────────────┐
│                    Interface Layer                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │               Infrastructure Layer                │   │
│  │  ┌─────────────────────────────────────────┐   │   │
│  │  │            Application Layer             │   │   │
│  │  │  ┌─────────────────────────────────┐   │   │   │
│  │  │  │         Domain Layer            │   │   │   │
│  │  │  │                                 │   │   │   │
│  │  │  └─────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

**Domain Layer (Innermost)**
- Business entities and value objects
- Domain services containing business logic
- Domain events for business occurrences
- No dependencies on external frameworks

**Application Layer**
- Use cases orchestrating domain objects
- Interfaces (ports) for external dependencies
- Application services for cross-cutting concerns
- Depends only on domain layer

**Infrastructure Layer**
- Implementations of application interfaces
- External API integrations
- Database and file system access
- Framework-specific code

**Interface Layer (Outermost)**
- User interfaces (CLI, Web, API)
- Controllers and presenters
- Input/output formatting
- Framework adapters

## Implementation Structure

### Directory Organization

```
src/
├── domain/                     # Domain Layer
│   ├── entities/              # Business entities with identity
│   ├── value_objects/         # Immutable domain concepts
│   ├── services/              # Domain business logic
│   ├── events/                # Domain events
│   └── exceptions/            # Domain-specific exceptions
├── application/               # Application Layer
│   ├── use_cases/             # Business use cases
│   ├── ports/                 # Interface contracts
│   ├── services/              # Application services
│   └── commands/              # Command objects
├── infrastructure/            # Infrastructure Layer
│   ├── repositories/          # Data access implementations
│   ├── external_apis/         # Third-party integrations
│   ├── services/              # Technical services
│   └── adapters/              # Port implementations
└── interface/                 # Interface Layer
    ├── cli/                   # Command-line interface
    ├── web/                   # Web interface
    └── api/                   # REST API
```

## Domain Layer Design

### Entity Design Pattern

Entities have identity and lifecycle management:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ResearchPaper:
    """
    Research Paper Entity - Core domain object with identity.
    
    Demonstrates:
    - Entity pattern with DOI as natural key
    - Rich domain model with behavior
    - Immutable design with validation
    """
    doi: DOI
    title: str
    authors: List[str]
    abstract: str
    publication_date: datetime
    metadata: PaperMetadata
    
    def __post_init__(self):
        self._validate_required_fields()
        self._validate_business_rules()
    
    def is_recent(self, days: int = 365) -> bool:
        """Business logic: determine if paper is recent."""
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.publication_date >= cutoff_date
    
    def extract_keywords(self) -> List[str]:
        """Business logic: extract key terms from paper."""
        # Domain logic for keyword extraction
        pass
```

### Value Object Design Pattern

Value objects are immutable and defined by their attributes:

```python
@dataclass(frozen=True)
class SearchQuery:
    """
    Search Query Value Object - Immutable search parameters.
    
    Demonstrates:
    - Value object pattern with attribute equality
    - Immutable design for thread safety
    - Rich validation logic
    """
    terms: Tuple[str, ...]
    date_range: Optional[DateRange]
    max_results: int
    include_abstracts: bool
    
    def __post_init__(self):
        self._validate_search_terms()
        self._validate_result_limits()
    
    def to_api_params(self) -> Dict[str, Any]:
        """Convert to external API format."""
        # Transformation logic
        pass
```

### Domain Service Pattern

Domain services contain business logic that doesn't naturally fit in entities:

```python
class ConceptExtractionService:
    """
    Domain Service for concept extraction business logic.
    
    Demonstrates:
    - Domain service pattern for cross-entity logic
    - Pure business logic without infrastructure dependencies
    - Testable domain behavior
    """
    
    def extract_concepts(self, papers: List[ResearchPaper]) -> ConceptGraph:
        """Extract and relate concepts across multiple papers."""
        # Pure domain logic for concept extraction
        pass
    
    def identify_research_gaps(self, concepts: ConceptGraph) -> List[ResearchGap]:
        """Business logic to identify gaps in research coverage."""
        # Domain logic for gap analysis
        pass
```

## Application Layer Design

### Use Case Pattern

Use cases orchestrate domain objects to fulfill business requirements:

```python
from abc import ABC, abstractmethod

class PaperDiscoveryUseCase:
    """
    Paper Discovery Use Case - Orchestrates domain objects.
    
    Demonstrates:
    - Use case pattern for business workflows
    - Dependency inversion through ports
    - Clear separation of concerns
    """
    
    def __init__(
        self,
        paper_repository: PaperRepositoryPort,
        search_service: SearchServicePort,
        concept_extractor: ConceptExtractionService
    ):
        self._paper_repository = paper_repository
        self._search_service = search_service
        self._concept_extractor = concept_extractor
    
    async def execute(self, query: SearchQuery) -> DiscoveryResult:
        """Execute paper discovery workflow."""
        # 1. Search for papers
        raw_papers = await self._search_service.search(query)
        
        # 2. Create domain objects
        papers = [ResearchPaper.from_raw_data(data) for data in raw_papers]
        
        # 3. Extract concepts
        concepts = self._concept_extractor.extract_concepts(papers)
        
        # 4. Persist results
        await self._paper_repository.save_batch(papers)
        
        return DiscoveryResult(papers=papers, concepts=concepts)
```

### Port Interface Pattern

Ports define contracts for external dependencies:

```python
class PaperRepositoryPort(ABC):
    """
    Paper Repository Port - Interface for data persistence.
    
    Demonstrates:
    - Port/Adapter pattern for dependency inversion
    - Abstract interface independent of implementation
    - Clear contract definition
    """
    
    @abstractmethod
    async def save(self, paper: ResearchPaper) -> None:
        """Save a single research paper."""
        pass
    
    @abstractmethod
    async def find_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """Find paper by DOI identifier."""
        pass
    
    @abstractmethod
    async def search_by_concepts(self, concepts: List[str]) -> List[ResearchPaper]:
        """Search papers by related concepts."""
        pass
```

## Infrastructure Layer Design

### Repository Implementation Pattern

Adapters implement port interfaces for specific technologies:

```python
class InMemoryPaperRepository(PaperRepositoryPort):
    """
    In-Memory Paper Repository - Adapter for testing and demos.
    
    Demonstrates:
    - Adapter pattern implementing port interface
    - Simple implementation for testing
    - Clear separation from domain logic
    """
    
    def __init__(self):
        self._papers: Dict[DOI, ResearchPaper] = {}
    
    async def save(self, paper: ResearchPaper) -> None:
        """Save paper to in-memory storage."""
        self._papers[paper.doi] = paper
    
    async def find_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """Find paper by DOI in memory."""
        return self._papers.get(doi)
```

### External API Adapter Pattern

Adapters encapsulate external service integration:

```python
class ArxivSearchAdapter(SearchServicePort):
    """
    arXiv Search Adapter - External API integration.
    
    Demonstrates:
    - Adapter pattern for external services
    - Error handling and resilience
    - API-specific logic isolation
    """
    
    def __init__(self, client: ArxivClient, rate_limiter: RateLimiter):
        self._client = client
        self._rate_limiter = rate_limiter
    
    async def search(self, query: SearchQuery) -> List[RawPaperData]:
        """Search arXiv API with rate limiting."""
        await self._rate_limiter.acquire()
        
        try:
            results = await self._client.search(query.to_arxiv_format())
            return [self._transform_result(result) for result in results]
        except ArxivAPIError as e:
            # Handle API-specific errors
            raise SearchServiceError(f"arXiv search failed: {e}")
```

## Dependency Injection

### Manual Dependency Injection

Simple dependency injection without frameworks:

```python
class DependencyContainer:
    """
    Simple dependency injection container.
    
    Demonstrates:
    - Manual dependency injection
    - Composition root pattern
    - Clean architecture assembly
    """
    
    def __init__(self, config: Configuration):
        self._config = config
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        # Infrastructure layer
        self._paper_repository = self._create_paper_repository()
        self._search_service = self._create_search_service()
        
        # Application layer
        self._concept_extractor = ConceptExtractionService()
        self._discovery_use_case = PaperDiscoveryUseCase(
            self._paper_repository,
            self._search_service,
            self._concept_extractor
        )
    
    def get_discovery_use_case(self) -> PaperDiscoveryUseCase:
        return self._discovery_use_case
```

## Testing Strategy

### Layer-Specific Testing

Each layer has specific testing approaches:

**Domain Layer Testing**
```python
class TestResearchPaper:
    """Test domain entities and value objects."""
    
    def test_paper_creation_with_valid_data(self):
        """Test entity creation with business validation."""
        paper = ResearchPaper(
            doi=DOI("10.1000/182"),
            title="Test Paper",
            authors=["Author 1"],
            abstract="Test abstract",
            publication_date=datetime.now(),
            metadata=PaperMetadata()
        )
        assert paper.is_recent()
    
    def test_paper_keyword_extraction(self):
        """Test domain business logic."""
        # Test business logic methods
        pass
```

**Application Layer Testing**
```python
class TestPaperDiscoveryUseCase:
    """Test use cases with mocked dependencies."""
    
    async def test_discovery_workflow(self):
        """Test complete discovery workflow."""
        # Arrange - Mock all dependencies
        mock_repository = Mock(spec=PaperRepositoryPort)
        mock_search_service = Mock(spec=SearchServicePort)
        mock_concept_extractor = Mock(spec=ConceptExtractionService)
        
        use_case = PaperDiscoveryUseCase(
            mock_repository,
            mock_search_service,
            mock_concept_extractor
        )
        
        # Act
        result = await use_case.execute(SearchQuery(...))
        
        # Assert - Verify interactions and results
        mock_search_service.search.assert_called_once()
        mock_repository.save_batch.assert_called_once()
        assert len(result.papers) > 0
```

**Infrastructure Layer Testing**
```python
class TestArxivSearchAdapter:
    """Test infrastructure adapters."""
    
    async def test_arxiv_search_integration(self):
        """Test real API integration."""
        adapter = ArxivSearchAdapter(real_client, rate_limiter)
        query = SearchQuery(terms=("machine learning",))
        
        results = await adapter.search(query)
        
        assert len(results) > 0
        assert all(result.title for result in results)
```

## Error Handling Strategy

### Domain Exceptions

Domain layer defines business-specific exceptions:

```python
class DomainException(Exception):
    """Base exception for domain layer."""
    pass

class InvalidPaperDataError(DomainException):
    """Raised when paper data violates business rules."""
    pass

class ConceptExtractionError(DomainException):
    """Raised when concept extraction fails."""
    pass
```

### Application Error Handling

Application layer handles and translates exceptions:

```python
class PaperDiscoveryUseCase:
    
    async def execute(self, query: SearchQuery) -> DiscoveryResult:
        try:
            # Business logic
            pass
        except SearchServiceError as e:
            # Handle infrastructure failures
            raise DiscoveryError(f"Search failed: {e}")
        except DomainException as e:
            # Handle domain violations
            raise DiscoveryError(f"Domain validation failed: {e}")
```

## Configuration Management

### Environment-Specific Configuration

Configuration follows the dependency rule:

```python
@dataclass
class ApplicationConfiguration:
    """Application-level configuration."""
    search_timeout: int
    max_concurrent_searches: int
    batch_size: int

@dataclass
class InfrastructureConfiguration:
    """Infrastructure-specific configuration."""
    arxiv_api_key: str
    database_url: str
    cache_settings: CacheConfiguration
```

## Related Documents

- [[System-Architecture]]: Overall system design
- [[Module-Boundaries]]: Component organization
- [[Repository-Implementation]]: Data access patterns
- [[Testing-Strategy]]: Quality assurance approach
- [[Domain-Services]]: Business logic coordination
- [[Port-Interfaces]]: Contract definitions

## Benefits Achieved

### Testability
- Each layer can be tested in isolation
- Dependencies are easily mocked
- Business logic is separated from technical concerns

### Maintainability
- Clear separation of concerns
- Dependency inversion enables flexibility
- Changes in one layer don't affect others

### Independence
- Framework independence in core business logic
- Database independence through repository pattern
- UI independence through ports and adapters

### Educational Value
- Demonstrates SOLID principles in practice
- Shows real-world application of design patterns
- Provides clear examples of architectural decisions
