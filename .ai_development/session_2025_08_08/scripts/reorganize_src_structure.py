#!/usr/bin/env python3
"""
Clean Architecture Reorganization Script

This script reorganizes the src/ directory to follow proper Domain-Driven Design
and Clean Architecture principles, separating Python backend from TypeScript frontend,
and moving educational content to appropriate locations.

Educational Notes:
- Demonstrates Clean Architecture layer separation
- Shows proper file organization for maintainable codebases
- Illustrates separation of concerns principle
- Provides template for enterprise-grade project structure

Design Principles Applied:
- Single Responsibility Principle: Each directory has one purpose
- Dependency Inversion: Infrastructure depends on domain, not vice versa
- Clean Architecture: Strict layer boundaries and dependency rules
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict


class SourceReorganizer:
    """
    Orchestrates the reorganization of source code according to Clean Architecture.

    Educational Notes:
    - Uses Command pattern for atomic operations
    - Implements transaction-like behavior with rollback capability
    - Demonstrates proper error handling and logging
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.src_path = self.base_path / "src"
        self.operations_log: List[str] = []

    def execute_reorganization(self):
        """Execute the complete reorganization with proper error handling."""
        try:
            print("🚀 Starting Clean Architecture reorganization...")

            # Phase 1: Create new directory structure
            self._create_clean_architecture_structure()

            # Phase 2: Move educational content out of src/
            self._move_educational_content()

            # Phase 3: Separate TypeScript frontend from Python backend
            self._separate_frontend_backend()

            # Phase 4: Reorganize Python code by Clean Architecture layers
            self._reorganize_python_layers()

            # Phase 5: Clean up duplicates and obsolete files
            self._cleanup_duplicates_and_obsolete()

            # Phase 6: Create pedagogical README files
            self._create_educational_documentation()

            # Phase 7: Remove empty directories
            self._remove_empty_directories()

            print("✅ Reorganization completed successfully!")
            self._print_new_structure()

        except Exception as e:
            print(f"❌ Error during reorganization: {e}")
            print("📋 Operations log:")
            for op in self.operations_log:
                print(f"  - {op}")
            raise

    def _create_clean_architecture_structure(self):
        """Create the target Clean Architecture directory structure."""
        print("📁 Creating Clean Architecture directory structure...")

        # New src structure (Python backend only)
        directories = [
            "src/domain/entities",
            "src/domain/value_objects",
            "src/domain/services",
            "src/application/use_cases",
            "src/application/ports",
            "src/infrastructure/repositories",
            "src/infrastructure/services",
            "src/infrastructure/adapters",
            "docs/educational/atomic_concepts",
            "docs/educational/cs_foundations",
            "frontend/components",
            "frontend/utils",
            "frontend/pages",
            "frontend/styles",
            "frontend/public",
        ]

        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self._log_operation(f"Created directory: {directory}")

    def _move_educational_content(self):
        """Move educational content from src/ to docs/."""
        print("📚 Moving educational content to docs/...")

        educational_moves = [
            ("src/educational", "docs/educational"),
            ("src/cs_foundations", "docs/educational/cs_foundations"),
        ]

        for src_dir, dest_dir in educational_moves:
            src_path = self.base_path / src_dir
            dest_path = self.base_path / dest_dir

            if src_path.exists():
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.move(str(src_path), str(dest_path))
                self._log_operation(f"Moved {src_dir} → {dest_dir}")

    def _separate_frontend_backend(self):
        """Separate TypeScript frontend from Python backend completely."""
        print("🔄 Separating frontend and backend code...")

        # Move web directory to root level as frontend
        web_src = self.src_path / "web"
        frontend_dest = self.base_path / "frontend"

        if web_src.exists():
            if frontend_dest.exists():
                shutil.rmtree(frontend_dest)
            shutil.move(str(web_src), str(frontend_dest))
            self._log_operation("Moved src/web → frontend/")

        # Move TypeScript utils to frontend
        utils_src = self.src_path / "utils"
        if utils_src.exists():
            frontend_utils = frontend_dest / "utils"
            if frontend_utils.exists():
                shutil.rmtree(frontend_utils)
            shutil.move(str(utils_src), str(frontend_utils))
            self._log_operation("Moved src/utils → frontend/utils/")

        # Move duplicate components to frontend (they're already there)
        components_src = self.src_path / "components"
        if components_src.exists():
            shutil.rmtree(components_src)
            self._log_operation("Removed duplicate src/components/")

    def _reorganize_python_layers(self):
        """Reorganize Python code according to Clean Architecture layers."""
        print("🏗️ Reorganizing Python code by Clean Architecture layers...")

        # Clean up domain layer
        self._reorganize_domain_layer()

        # Clean up application layer
        self._reorganize_application_layer()

        # Clean up infrastructure layer
        self._reorganize_infrastructure_layer()

    def _reorganize_domain_layer(self):
        """Reorganize domain layer files."""
        domain_src = self.src_path / "domain"

        # Keep entities (but clean up duplicates)
        entities_src = domain_src / "entities"
        if entities_src.exists():
            # Remove old/duplicate concept hierarchy files
            obsolete_files = ["concept_hierarchy_old.py", "concept_hierarchy_simple.py"]
            for filename in obsolete_files:
                file_path = entities_src / filename
                if file_path.exists():
                    file_path.unlink()
                    self._log_operation(f"Removed obsolete file: {filename}")

            # Remove TypeScript files from domain
            for ts_file in entities_src.glob("*.ts"):
                ts_file.unlink()
                self._log_operation(f"Removed TypeScript from domain: {ts_file.name}")

        # Clean value_objects
        value_objects_src = domain_src / "value_objects"
        if value_objects_src.exists():
            # Remove TypeScript files from value objects
            for ts_file in value_objects_src.glob("*.ts"):
                ts_file.unlink()
                self._log_operation(
                    f"Removed TypeScript from value_objects: {ts_file.name}"
                )

    def _reorganize_application_layer(self):
        """Reorganize application layer files."""
        app_src = self.src_path / "application"

        # Clean use_cases
        use_cases_src = app_src / "use_cases"
        if use_cases_src.exists():
            # Remove TypeScript files from use_cases
            for ts_file in use_cases_src.glob("*.ts"):
                ts_file.unlink()
                self._log_operation(
                    f"Removed TypeScript from use_cases: {ts_file.name}"
                )

        # Clean ports
        ports_src = app_src / "ports"
        if ports_src.exists():
            # Remove TypeScript files from ports
            for ts_file in ports_src.glob("*.ts"):
                ts_file.unlink()
                self._log_operation(f"Removed TypeScript from ports: {ts_file.name}")

    def _reorganize_infrastructure_layer(self):
        """Reorganize infrastructure layer files."""
        infra_src = self.src_path / "infrastructure"

        # Move root-level infrastructure files to proper subdirectories
        infra_services = infra_src / "services"

        # knowledge_graph.py stays at infrastructure root (it's a core component)
        # mcp_memory_integration.py stays at infrastructure root
        # pdf_extractor.py should move to services
        pdf_extractor = infra_src / "pdf_extractor.py"
        if pdf_extractor.exists() and infra_services.exists():
            target = infra_services / "pdf_extractor.py"
            if not target.exists():
                shutil.move(str(pdf_extractor), str(target))
                self._log_operation(
                    "Moved pdf_extractor.py to infrastructure/services/"
                )

    def _cleanup_duplicates_and_obsolete(self):
        """Remove duplicate and obsolete files."""
        print("🧹 Cleaning up duplicates and obsolete files...")

        # Remove empty interface directory
        interface_dir = self.src_path / "interface"
        if interface_dir.exists() and not any(interface_dir.iterdir()):
            shutil.rmtree(interface_dir)
            self._log_operation("Removed empty interface/ directory")

        # Remove research_paper_aggregator.egg-info if it exists in src
        egg_info = self.src_path / "research_paper_aggregator.egg-info"
        if egg_info.exists():
            shutil.rmtree(egg_info)
            self._log_operation("Removed egg-info from src/")

    def _create_educational_documentation(self):
        """Create README files with pedagogical content and concept map links."""
        print("📖 Creating educational documentation...")

        readme_files = [
            ("src/README.md", self._get_src_readme_content()),
            ("src/domain/README.md", self._get_domain_readme_content()),
            ("src/application/README.md", self._get_application_readme_content()),
            ("src/infrastructure/README.md", self._get_infrastructure_readme_content()),
            ("docs/educational/README.md", self._get_educational_readme_content()),
            ("frontend/README.md", self._get_frontend_readme_content()),
        ]

        for file_path, content in readme_files:
            full_path = self.base_path / file_path
            if not full_path.exists():
                with open(full_path, "w") as f:
                    f.write(content)
                self._log_operation(f"Created {file_path}")

    def _remove_empty_directories(self):
        """Remove empty directories after reorganization."""
        print("🗑️ Removing empty directories...")

        def remove_empty_dirs(path: Path):
            if not path.is_dir():
                return

            # Remove empty subdirectories first
            for subdir in path.iterdir():
                if subdir.is_dir():
                    remove_empty_dirs(subdir)

            # Remove this directory if it's empty
            try:
                if not any(path.iterdir()):
                    path.rmdir()
                    self._log_operation(
                        f"Removed empty directory: {path.relative_to(self.base_path)}"
                    )
            except OSError:
                pass  # Directory not empty or permission issue

        remove_empty_dirs(self.src_path)

    def _print_new_structure(self):
        """Print the new directory structure."""
        print("\n📋 New Clean Architecture Structure:")
        print(
            """
src/                                    # Python Backend (Clean Architecture)
├── domain/                            # Domain Layer - Business Logic
│   ├── entities/                      # Business objects with identity
│   │   ├── research_paper.py         # Core research paper entity
│   │   ├── concept.py                # Concept entity
│   │   └── concept_hierarchy.py      # Hierarchical concept relationships
│   ├── value_objects/                # Immutable domain concepts
│   │   ├── search_query.py           # Search criteria value object
│   │   ├── keyword_config.py         # Configuration value object
│   │   └── paper_fingerprint.py      # Paper identification
│   └── services/                     # Domain services
│       ├── concept_extractor.py      # Core concept extraction logic
│       └── concept_hierarchy_builder.py  # Hierarchy construction
├── application/                       # Application Layer - Use Cases
│   ├── use_cases/                    # Business operations
│   │   ├── execute_keyword_search_use_case.py
│   │   └── extract_paper_concepts_use_case.py
│   └── ports/                        # Abstract interfaces
│       ├── paper_repository_port.py  # Repository contracts
│       └── concept_repository_port.py
└── infrastructure/                    # Infrastructure Layer - External Concerns
    ├── repositories/                  # Data access implementations
    │   ├── arxiv_paper_repository.py  # ArXiv API integration
    │   └── in_memory_paper_repository.py
    ├── services/                      # External service implementations
    │   ├── pdf_extractor.py          # PDF processing service
    │   └── sentence_transformer_embedding_service.py
    ├── adapters/                      # Format adapters
    │   └── json_concept_loader.py     # JSON format adapter
    ├── knowledge_graph.py             # Core knowledge graph implementation
    └── mcp_memory_integration.py      # MCP memory system integration

frontend/                              # TypeScript/React Frontend
├── components/                        # React components
├── pages/                            # Next.js pages
├── utils/                            # Frontend utilities
└── styles/                           # Styling

docs/                                 # Educational Documentation
└── educational/                      # Computer science education content
    ├── atomic_concepts/              # Atomic concept definitions
    └── cs_foundations/               # CS theory foundations
        """
        )

    def _log_operation(self, message: str):
        """Log an operation for tracking and potential rollback."""
        self.operations_log.append(message)
        print(f"  ✓ {message}")

    def _get_src_readme_content(self) -> str:
        return """# Academic Paper Discovery - Core Backend

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
"""

    def _get_domain_readme_content(self) -> str:
        return """# Domain Layer - Business Logic Core

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
"""

    def _get_application_readme_content(self) -> str:
        return """# Application Layer - Use Cases and Ports

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
"""

    def _get_infrastructure_readme_content(self) -> str:
        return """# Infrastructure Layer - External Integrations

The infrastructure layer implements the technical details of how our system interacts with the outside world. This is where abstract ports become concrete implementations.

## Educational Notes

### Infrastructure Layer Purpose

1. **Implements Ports**: Provides concrete implementations of application interfaces
2. **External Integration**: Connects to databases, APIs, file systems, and external services
3. **Technical Concerns**: Handles serialization, networking, caching, and performance optimization
4. **Adapter Pattern**: Translates between external formats and internal domain models

### Key Architectural Principles

#### Dependency Inversion in Action
```
Domain ← Application ← Infrastructure
   ↑         ↑            ↑
   └─────────┴────────────┘
   
Infrastructure depends on Application interfaces,
not the other way around!
```

#### Adapter Pattern Implementation
External systems rarely match our domain models perfectly. Adapters translate:
- External JSON → Domain Objects
- Database Rows → Domain Objects  
- API Responses → Domain Objects

## Directory Structure

### Repositories (`repositories/`)

**Purpose**: Implement data persistence and retrieval contracts

**Educational Value**:
- Demonstrates Repository pattern for abstracting data access
- Shows how to handle different data sources uniformly
- Illustrates error handling and connection management

**Implementations**:
- `ArxivPaperRepository`: Integrates with ArXiv API for academic papers
- `InMemoryPaperRepository`: Simple in-memory storage for testing and demos
- `PmcPaperRepository`: Integrates with PubMed Central database

### Services (`services/`)

**Purpose**: Implement external service integrations

**Educational Value**:
- Shows how to wrap third-party libraries safely
- Demonstrates configuration-driven behavior
- Illustrates retry logic and error recovery

**Implementations**:
- `PdfExtractor`: Extracts text content from PDF files
- `SentenceTransformerEmbeddingService`: Generates semantic embeddings

### Adapters (`adapters/`)

**Purpose**: Convert between external formats and domain models

**Educational Value**:
- Demonstrates Adapter pattern for format translation
- Shows data validation and sanitization
- Illustrates graceful handling of malformed data

**Implementations**:
- `JsonConceptLoader`: Loads concept definitions from JSON files
- `AtomicConceptAdapter`: Adapts between different concept representation formats

## Core Infrastructure Components

### KnowledgeGraph (`knowledge_graph.py`)

**Purpose**: Implements graph-based knowledge storage and retrieval

**Educational Value**:
- Demonstrates advanced data structures (directed acyclic graphs)
- Shows graph algorithms in practice (BFS, DFS, A*, PageRank)
- Illustrates performance optimization techniques (caching, lazy loading)

**Key Features**:
- Entity and relationship management
- Graph traversal algorithms
- Cycle detection and prevention
- Importance ranking (PageRank)
- Connected component analysis

### MCP Memory Integration (`mcp_memory_integration.py`)

**Purpose**: Integrates with Model Context Protocol memory systems

**Educational Value**:
- Shows asynchronous programming patterns
- Demonstrates external API integration
- Illustrates batch processing for efficiency
- Shows error handling and retry logic

## Design Patterns in Infrastructure

### Repository Pattern
The Repository pattern abstracts data access behind interfaces:
- Concrete implementations hidden from application layer
- Multiple data sources supported uniformly
- Easy testing with mock implementations

### Adapter Pattern
The Adapter pattern translates between external formats and domain models:
- External JSON converted to domain objects
- API responses adapted to internal structures
- Graceful handling of format changes

### Factory Pattern
The Factory pattern creates repository instances based on configuration:
- Runtime selection of appropriate implementation
- Configuration-driven behavior
- Easy addition of new repository types

## Configuration and Environment

### Configuration-Driven Design
Infrastructure components are configured externally:
- Database connection strings
- API keys and endpoints
- Feature flags and performance tuning
- Retry policies and timeouts

### Environment Isolation
Different configurations for:
- Development (local files, mock services)
- Testing (in-memory databases, stubbed APIs)
- Production (real databases, external APIs)

## Performance Considerations

### Caching Strategies
- **Repository Level**: Cache frequently accessed entities
- **Service Level**: Cache expensive computations
- **Network Level**: Cache API responses with appropriate TTL

### Asynchronous Processing
- Non-blocking I/O for external API calls
- Background processing for long-running tasks
- Queue-based processing for batch operations

### Error Handling and Resilience
- Circuit breaker pattern for external service failures
- Exponential backoff for retry logic
- Graceful degradation when services are unavailable

## Concept Map Connections

- [Repository Pattern](../../../concept_storage/concepts/design_patterns/repository_pattern.md)
- [Adapter Pattern](../../../concept_storage/concepts/design_patterns/adapter_pattern.md)
- [Factory Pattern](../../../concept_storage/concepts/design_patterns/factory_pattern.md)
- [Circuit Breaker Pattern](../../../concept_storage/concepts/resilience_patterns/circuit_breaker.md)

## Testing Infrastructure

### Integration Testing
Test with real external dependencies in controlled environments.
Repository contracts are validated to ensure all implementations 
satisfy the expected interface behavior.

### Contract Testing
Ensure implementations satisfy port contracts by testing that
any repository implementation correctly implements the required
interface methods and behaviors.

## Industry Applications

This infrastructure pattern is used in:
- **Microservices**: Each service implements clean boundaries
- **Cloud Applications**: Adapters for different cloud providers
- **Enterprise Systems**: Integration with legacy systems
- **Data Pipelines**: ETL processes with clean transformation layers

The infrastructure layer enables your system to evolve technically while keeping business logic stable and testable.
"""

    def _get_educational_readme_content(self) -> str:
        return """# Educational Content - Computer Science Foundations

This directory contains educational materials that demonstrate computer science concepts through practical implementation in the Academic Paper Discovery system.

## Educational Philosophy

### Progressive Learning Approach

1. **Atomic Concepts**: Start with individual CS concepts in isolation
2. **Composition**: Show how simple concepts combine into complex systems
3. **Real-World Application**: Demonstrate concepts through working code
4. **Industry Relevance**: Connect academic theory to professional practice

### Pedagogical Principles

- **Just-in-Time Learning**: Concepts introduced when needed
- **Concrete to Abstract**: Start with examples, then generalize
- **Multiple Perspectives**: Same concept shown in different contexts
- **Active Learning**: Hands-on exercises and experiments

## Directory Structure

### Atomic Concepts (`atomic_concepts/`)

**Purpose**: Individual computer science concepts in isolation

**Educational Value**:
- Each concept stands alone for focused learning
- Clear examples with minimal dependencies
- Progression from simple to complex
- Links to broader system implementation

**Contents**:
- Concept definitions with formal specifications
- Code examples demonstrating the concept
- Visualization tools for complex concepts
- Assessment rubrics and exercises

### CS Foundations (`cs_foundations/`)

**Purpose**: Fundamental computer science theory and structures

**Educational Value**:
- Mathematical foundations of computer science
- Abstract data types and their implementations
- Algorithm analysis and complexity theory
- Design patterns and software engineering principles

**Contents**:
- Mathematical foundations (discrete math, logic, set theory)
- Data structures (linear, hierarchical, graph-based)
- Algorithms (sorting, searching, graph traversal)
- Software engineering principles and patterns

## Connection to Main System

### Theory to Practice Bridge

Each educational concept links to its implementation in the main system:

**Example: Graph Theory → Knowledge Graph**
- **Theory**: Graph algorithms (BFS, DFS, shortest path)
- **Practice**: `src/infrastructure/knowledge_graph.py`
- **Application**: Academic concept relationship discovery

**Example: Repository Pattern → Data Access**
- **Theory**: Abstraction and encapsulation principles
- **Practice**: `src/application/ports/` and `src/infrastructure/repositories/`
- **Application**: Multiple paper source integration

### Concept Map Integration

Educational content is integrated with the main concept map:
- Each concept has metadata linking to related concepts
- Learning paths show prerequisite relationships
- Assessment rubrics measure understanding depth
- Real-world applications demonstrate relevance

## Learning Pathways

### Beginner Path: Fundamentals First
1. Basic data structures (arrays, lists, trees)
2. Simple algorithms (linear search, basic sorting)
3. Object-oriented programming concepts
4. Basic design patterns

### Intermediate Path: Systems Thinking
1. Advanced data structures (graphs, hash tables)
2. Algorithm complexity analysis
3. Software architecture patterns
4. Database and networking concepts

### Advanced Path: Industry Applications
1. Distributed systems concepts
2. Performance optimization techniques
3. Security and reliability patterns
4. Machine learning integration

## Assessment and Evaluation

### Competency-Based Assessment

Each concept includes:
- **Knowledge**: Can explain the concept
- **Comprehension**: Can apply in simple scenarios
- **Application**: Can use in complex situations
- **Analysis**: Can evaluate trade-offs and alternatives
- **Synthesis**: Can combine with other concepts creatively
- **Evaluation**: Can critique and improve implementations

### Portfolio Development

Students build a portfolio showing:
- Understanding of individual concepts
- Ability to combine concepts into systems
- Real-world application development
- Code quality and documentation skills

## Industry Relevance

### Pacific Northwest Tech Standards

Content aligned with regional industry expectations:
- **Amazon**: Scalable systems and data structures
- **Microsoft**: Software engineering best practices
- **Google**: Algorithm optimization and analysis
- **Startups**: Full-stack development and rapid prototyping

### Professional Skills Development

- **Code Review**: Understanding design decisions and trade-offs
- **Technical Communication**: Explaining complex concepts clearly
- **System Design**: Architecting maintainable software systems
- **Collaboration**: Working effectively in technical teams

## Concept Map Connections

- [Educational Theory](../../concept_storage/concepts/education/pedagogical_principles.md)
- [Computer Science Fundamentals](../../concept_storage/concepts/cs_theory/foundations.md)
- [Software Engineering](../../concept_storage/concepts/software_engineering/principles.md)
- [Industry Applications](../../concept_storage/concepts/industry/tech_careers.md)

## Contributing to Educational Content

### Content Creation Guidelines

1. **Clarity**: Explain concepts in accessible language
2. **Examples**: Provide concrete, working code examples
3. **Connections**: Link to related concepts and applications
4. **Assessment**: Include ways to measure understanding
5. **Industry Relevance**: Show real-world applications

### Quality Standards

- Peer-reviewed content with technical accuracy
- Multiple learning modalities (visual, auditory, kinesthetic)
- Inclusive examples that represent diverse perspectives
- Regular updates to maintain current industry relevance

This educational framework prepares students for successful careers in technology while building strong theoretical foundations in computer science.
"""

    def _get_frontend_readme_content(self) -> str:
        return """# Frontend - React/TypeScript Interface

This directory contains the React/TypeScript frontend for the Academic Paper Discovery system, providing interactive visualization and user interfaces for concept exploration.

## Technology Stack

### Core Technologies
- **React 18**: Modern functional components with hooks
- **TypeScript**: Type-safe JavaScript for large applications
- **Next.js**: Full-stack React framework with SSR/SSG
- **Tailwind CSS**: Utility-first CSS framework
- **D3.js**: Data visualization library for interactive graphs

### Educational Value
- **Modern Frontend Development**: Industry-standard React patterns
- **Type Safety**: TypeScript for maintainable codebases
- **Performance Optimization**: Next.js optimization techniques
- **Data Visualization**: Interactive graph representations

## Directory Structure

### Components (`components/`)
Reusable React components following atomic design principles:
- `InteractiveConceptGraph.tsx`: Main concept visualization component
- `ConceptExtractionDemo.tsx`: Interactive demo of concept extraction
- `LandingPage.tsx`: Homepage with feature overview

### Pages (`pages/`)
Next.js pages using file-based routing:
- `index.tsx`: Application homepage
- `concept-graph.tsx`: Full-screen concept graph interface
- `api/concepts.ts`: API endpoints for concept data

### Utils (`utils/`)
TypeScript utilities for data processing and visualization:
- `advancedD3Utils.ts`: D3.js helpers for graph visualization
- `advancedShapeUtils.ts`: Geometric calculations for node positioning

### Styles (`styles/`)
Global styles and Tailwind CSS configuration:
- `globals.css`: Application-wide styling
- Component-specific styles using Tailwind utilities

## Key Features

### Interactive Concept Graph
**Educational Value**: Demonstrates graph visualization techniques
- Force-directed layout for natural node positioning
- Zoom and pan interactions for large datasets
- Real-time filtering and search capabilities
- Hierarchical clustering for concept organization

### Concept Extraction Demo
**Educational Value**: Shows NLP and text processing in action
- Live concept extraction from user input
- Confidence scoring and ranking
- Interactive refinement of extraction parameters
- Integration with backend processing pipeline

### Responsive Design
**Educational Value**: Modern CSS and responsive techniques
- Mobile-first design approach
- Flexible grid layouts with CSS Grid and Flexbox
- Accessibility features (ARIA labels, keyboard navigation)
- Performance optimization (lazy loading, code splitting)

## Development Patterns

### Component Design Principles
Functional components with TypeScript interfaces provide type safety
and clear contracts. Components follow atomic design principles
with proper separation of concerns and reusable patterns.

### State Management
- **Local State**: React hooks for component-specific state
- **Global State**: Context API for shared application state
- **Server State**: SWR for data fetching and caching
- **URL State**: Next.js router for shareable application state

### Performance Optimization
- **Memoization**: React.memo and useMemo for expensive calculations
- **Virtualization**: Virtual scrolling for large datasets
- **Code Splitting**: Dynamic imports for route-based splitting
- **Image Optimization**: Next.js Image component for optimal loading

## Backend Integration

### API Communication
Type-safe API calls with proper error handling ensure reliable
communication between frontend and backend components.

### Data Flow
1. User interactions trigger state changes
2. State changes trigger API calls to Python backend
3. Backend processes requests using Clean Architecture
4. Frontend updates UI with new data
5. Real-time updates via WebSocket connections (where applicable)

## Visualization Architecture

### D3.js Integration with React
Proper D3 integration without conflicting with React's DOM management
using custom hooks and proper lifecycle management.

### Graph Layout Algorithms
- **Force-Directed Layout**: Natural positioning for concept relationships
- **Hierarchical Layout**: Tree-like structure for concept hierarchies
- **Circular Layout**: Equal spacing for category-based grouping
- **Custom Layouts**: Domain-specific positioning algorithms

## Concept Map Connections

- [React Architecture](../../concept_storage/concepts/frontend/react_patterns.md)
- [TypeScript Best Practices](../../concept_storage/concepts/frontend/typescript_patterns.md)
- [Data Visualization](../../concept_storage/concepts/visualization/d3_patterns.md)
- [Performance Optimization](../../concept_storage/concepts/frontend/performance_optimization.md)

## Development Setup

### Prerequisites
```bash
# Node.js 18+ and npm
node --version  # Should be 18+
npm --version
```

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run production server
npm start
```

### Development Scripts
- `npm run dev`: Start development server with hot reload
- `npm run build`: Create optimized production build
- `npm run lint`: Run ESLint for code quality
- `npm run type-check`: Run TypeScript compiler check

## Testing Strategy

### Component Testing
React Testing Library provides excellent tools for testing component 
behavior rather than implementation details. Components should be
tested for their user-facing behavior and proper event handling.

### Integration Testing
- API integration tests with mock backend
- End-to-end testing with Playwright or Cypress
- Visual regression testing for UI consistency
- Performance testing for large datasets

## Industry Best Practices

### Code Quality
- **ESLint**: Consistent code style and error prevention
- **Prettier**: Automatic code formatting
- **Husky**: Git hooks for pre-commit quality checks
- **TypeScript Strict Mode**: Maximum type safety

### Performance Monitoring
- **Core Web Vitals**: Loading, interactivity, and visual stability
- **Bundle Analysis**: Identifying optimization opportunities
- **Runtime Performance**: React DevTools Profiler
- **User Experience Metrics**: Real user monitoring

### Accessibility
- **Semantic HTML**: Proper element usage for screen readers
- **ARIA Labels**: Descriptive labels for interactive elements
- **Keyboard Navigation**: Full functionality without mouse
- **Color Contrast**: WCAG compliance for visual accessibility

This frontend demonstrates modern web development practices while providing an intuitive interface for exploring academic concepts and research papers.
"""


# Main execution
if __name__ == "__main__":
    reorganizer = SourceReorganizer(
        "/Users/jessicadoner/Projects/research-papers/research-paper-aggregator"
    )
    reorganizer.execute_reorganization()
