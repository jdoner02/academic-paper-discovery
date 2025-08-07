# Clean Architecture Overview

## Introduction for Cross-Disciplinary Students

**For Non-CS Students**: Clean Architecture is a software design pattern that organizes code into concentric layers, similar to how scientific disciplines separate theoretical foundations from experimental procedures. Just as physics separates fundamental laws (like Maxwell's equations) from engineering applications (like antenna design), Clean Architecture separates core business logic from implementation details.

## Core Principles

### 1. Dependency Inversion
**Outer layers depend on inner layers, never the reverse.**

```
Infrastructure → Application → Domain
    (Web UI)      (Use Cases)   (Entities)
```

**Physics Analogy**: Just as engineering applications depend on physical laws (not the reverse), our web interface depends on business rules, but business rules don't depend on web frameworks.

### 2. Separation of Concerns
Each layer has a single, well-defined responsibility:

- **Domain Layer**: Pure business logic (concept extraction rules, academic requirements)
- **Application Layer**: Orchestrates domain objects (extraction workflows, validation)
- **Infrastructure Layer**: External concerns (databases, APIs, file systems)

## Layer Breakdown for Academic Context

### Domain Layer (Core Academic Logic)
**Purpose**: Contains the essential knowledge about concept extraction that would remain true regardless of technology changes.

**Mathematical Analogy**: Like axioms in mathematics - these are the fundamental truths about academic concept extraction that don't change whether you implement them in Python, Java, or any other language.

**Key Components**:
- `Concept` entity - What makes a research concept valid
- `ResearchPaper` entity - Academic paper representation
- `ConceptHierarchy` aggregate - How concepts organize hierarchically
- `EvidenceSentence` value object - Supporting text for concepts

### Application Layer (Research Workflows)
**Purpose**: Orchestrates domain objects to achieve specific academic goals.

**Laboratory Analogy**: Like experimental procedures that combine basic scientific principles to achieve research objectives.

**Key Components**:
- `ExtractPaperConceptsUseCase` - Complete concept extraction workflow
- `BuildVisualizationDataUseCase` - Prepare data for D3.js display
- Repository ports - Abstract interfaces for data storage

### Infrastructure Layer (Technical Implementation)
**Purpose**: Handles technical details like databases, file systems, and external APIs.

**Engineering Analogy**: Like choosing specific materials and manufacturing processes to build a device - the core physics remains the same, but implementation varies.

**Key Components**:
- PDF text extraction services
- Embedding model integrations (Sentence-BERT)
- JSON storage repositories
- Web framework integrations

## Benefits for Academic Software

### 1. **Testability**
Each layer can be tested independently, ensuring research-grade reliability.

### 2. **Maintainability** 
Domain logic (the academic concepts) remains stable even as technology changes.

### 3. **Extensibility**
New extraction methods can be added without changing core academic principles.

### 4. **Academic Trust**
Clear separation makes the system transparent and auditable for peer review.

## Real-World Example: Concept Extraction

```python
# Domain Layer - Pure academic logic
class Concept:
    def __init__(self, name: str, evidence_sentences: List[EvidenceSentence]):
        self._validate_academic_requirements(name, evidence_sentences)
        # Core academic validation - no dependencies on databases or web frameworks

# Application Layer - Research workflow
class ExtractPaperConceptsUseCase:
    def execute(self, paper: ResearchPaper) -> List[Concept]:
        # Orchestrates domain objects to achieve academic goals
        # Uses abstract interfaces (ports) for external dependencies

# Infrastructure Layer - Technical implementation  
class SentenceBertEmbeddingService:
    def generate_embeddings(self, text: str) -> EmbeddingVector:
        # Technical implementation using specific ML libraries
        # Can be swapped out without affecting core academic logic
```

## Design Patterns Used

### Repository Pattern
- **Purpose**: Abstracts data storage concerns from business logic.
- **Academic Benefit**: Researchers can focus on concept extraction algorithms without worrying about database details.

### Strategy Pattern  
- **Purpose**: Allows multiple extraction algorithms (rule-based, statistical, embedding-based).
- **Academic Benefit**: Different research approaches can coexist and be compared objectively.

### Factory Pattern
- **Purpose**: Creates domain objects with proper validation.
- **Academic Benefit**: Ensures all concepts meet academic quality standards.

## Integration with Academic Workflow

This architecture supports the complete academic research lifecycle:

1. **Literature Collection** (Infrastructure) → PDF parsing and metadata extraction
2. **Concept Extraction** (Domain) → Core academic algorithms 
3. **Knowledge Organization** (Application) → Hierarchical structuring workflows
4. **Visualization** (Infrastructure) → Interactive D3.js displays
5. **Academic Validation** (Domain) → Evidence grounding and quality metrics

The separation ensures that the core academic value (concept extraction knowledge) remains independent of changing technologies, making the system suitable for long-term research use and academic publication.
