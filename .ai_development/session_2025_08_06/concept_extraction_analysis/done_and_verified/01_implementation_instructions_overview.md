# AI Agent Instructions: Introduction and Problem Overview Implementation

## MISSION OVERVIEW
You are implementing the foundational components for an automated concept extraction and hierarchical mapping system for research papers. This subsection focuses on establishing the core domain model and architectural foundation that will support the entire concept extraction pipeline.

## EDUCATIONAL CONTEXT
This system serves **STEM students and faculty** from diverse backgrounds (CS, Math, Physics, Engineering, Cybersecurity) at Eastern Washington University. Your implementation must be:
- **Academically rigorous** - Suitable for peer review and educational use
- **Transparent and explainable** - Every decision must be traceable and justifiable  
- **Cross-disciplinary accessible** - Clear documentation for non-CS backgrounds
- **Production quality** - Clean Architecture principles with comprehensive testing

## TECHNICAL REQUIREMENTS

### Phase 1: Enhanced Domain Model Implementation

#### 1.1 Extend Concept Entity (`src/domain/entities/concept.py`)

**Current State Analysis**: Examine the existing Concept entity and enhance it to support hierarchical relationships and evidence grounding.

**Implementation Requirements**:
```python
"""
Enhanced Concept Entity - Hierarchical Concept Representation

This entity represents a research concept extracted from academic papers with full
hierarchical and evidence support. It demonstrates the Entity pattern from Domain-Driven
Design by having a unique identity and rich behavior.

Educational Notes:
- Entities have identity and lifecycle (concepts persist across papers)
- Value Objects are immutable data containers (evidence sentences)
- Aggregates maintain consistency boundaries (concept hierarchies)

Design Decisions:
- Uses composition over inheritance for evidence collection
- Immutable evidence list prevents accidental modification
- Parent-child relationships enable tree traversal algorithms
"""

@dataclass(frozen=False)  # Mutable for lifecycle management
class Concept:
    # Identity and core properties
    concept_id: str
    name: str
    description: str
    
    # Hierarchical relationships
    parent_concept_id: Optional[str] = None
    child_concept_ids: List[str] = field(default_factory=list)
    hierarchy_level: int = 0
    
    # Evidence and validation
    evidence_sentences: List[EvidenceSentence] = field(default_factory=list)
    supporting_papers: List[str] = field(default_factory=list)
    
    # Quality metrics
    confidence_score: float = 0.0
    extraction_method: str = ""
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_evidence(self, evidence: EvidenceSentence) -> None:
        """Add evidence sentence with validation"""
        # Implementation with validation logic
        
    def get_ancestor_path(self) -> List[str]:
        """Return path from root to this concept"""
        # Implementation for hierarchy traversal
        
    def calculate_support_strength(self) -> float:
        """Calculate evidence strength across papers"""
        # Implementation combining paper count and evidence quality
```

#### 1.2 Create Evidence Sentence Value Object (`src/domain/value_objects/evidence_sentence.py`)

**Educational Note**: Value Objects represent concepts without identity. Evidence sentences are immutable data that describe the same concept regardless of context.

```python
"""
Evidence Sentence Value Object - Concept Grounding Support

This value object provides traceable evidence for concept extraction, ensuring
academic integrity by linking every concept to its source text. It demonstrates
the Value Object pattern by being immutable and equality-based.

Design Principles Applied:
- Immutability prevents accidental modification of evidence
- Value equality enables deduplication of identical evidence
- Rich behavior encapsulates domain logic for evidence assessment
"""

@dataclass(frozen=True)
class EvidenceSentence:
    sentence_text: str
    paper_id: str
    page_number: Optional[int] = None
    paragraph_context: str = ""
    confidence_score: float = 0.0
    extraction_timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate evidence sentence constraints"""
        # Implementation with academic-grade validation
        
    def contains_concept(self, concept_name: str) -> bool:
        """Check if sentence contains concept mention"""
        # Implementation with fuzzy matching
        
    def get_context_window(self, window_size: int = 50) -> str:
        """Extract context around concept mention"""
        # Implementation for evidence presentation
```

#### 1.3 Create Concept Hierarchy Aggregate (`src/domain/entities/concept_hierarchy.py`)

**Educational Note**: Aggregates maintain consistency boundaries. A concept hierarchy ensures that parent-child relationships remain valid across all operations.

```python
"""
Concept Hierarchy Aggregate Root - Hierarchical Knowledge Structure

This aggregate maintains consistency of concept relationships and provides
operations for hierarchy traversal and validation. It demonstrates the
Aggregate pattern by encapsulating complex domain rules.

Educational Notes:
- Aggregates are consistency boundaries in Domain-Driven Design
- They ensure invariants are maintained across related entities
- Rich domain behavior prevents invalid state transitions
"""

class ConceptHierarchy:
    def __init__(self, root_concepts: List[Concept]):
        # Implementation with consistency validation
        
    def add_concept(self, concept: Concept, parent_id: Optional[str] = None) -> None:
        """Add concept maintaining hierarchy constraints"""
        # Implementation with cycle detection
        
    def get_concept_path(self, concept_id: str) -> List[Concept]:
        """Get path from root to concept"""
        # Implementation with graph traversal
        
    def validate_hierarchy_integrity(self) -> List[str]:
        """Validate hierarchy for cycles and orphans"""
        # Implementation with graph algorithms
```

### Phase 2: Application Layer Use Cases

#### 2.1 Create Foundation Use Case (`src/application/use_cases/extract_hierarchical_concepts_use_case.py`)

```python
"""
Extract Hierarchical Concepts Use Case - Core Business Logic

This use case orchestrates the concept extraction pipeline, demonstrating
the Use Case pattern by encapsulating a complete business operation.

Architectural Benefits:
- Decouples business logic from technical implementation
- Enables testing without external dependencies
- Provides clear API for different interfaces (CLI, GUI, API)
"""

class ExtractHierarchicalConceptsUseCase:
    def __init__(self, 
                 paper_repository: PaperRepositoryPort,
                 concept_extractor: ConceptExtractionPort,
                 hierarchy_builder: HierarchyBuildingPort):
        # Dependency injection for testability
        
    def execute(self, request: HierarchicalExtractionRequest) -> HierarchicalExtractionResult:
        """Extract and organize concepts from paper collection"""
        # Implementation with progress tracking and error handling
```

### Phase 3: Infrastructure Integration

#### 3.1 Create Repository Interfaces (`src/application/ports/`)

Create port interfaces for:
- `ConceptRepositoryPort` - Concept persistence
- `ConceptExtractionPort` - Algorithm interface
- `HierarchyBuildingPort` - Structure creation
- `VisualizationDataPort` - GUI data preparation

### Phase 4: Comprehensive Testing Strategy

#### 4.1 Domain Model Tests (`tests/unit/domain/`)

**Test Philosophy**: Academic systems require >90% test coverage with focus on correctness over speed.

```python
"""
Test Strategy for Concept Domain Model

Educational Notes:
- Unit tests validate individual component behavior
- Integration tests verify component interaction
- Property-based tests explore edge cases systematically
- Academic software requires reproducible test results
"""

class TestConceptEntity:
    def test_concept_creation_with_valid_data(self):
        """Verify concept creation follows domain rules"""
        
    def test_evidence_addition_maintains_consistency(self):
        """Ensure evidence collection preserves integrity"""
        
    def test_hierarchy_relationship_validation(self):
        """Validate parent-child constraints"""
```

## IMPLEMENTATION APPROACH

### Step 1: Domain Model Analysis
1. **Examine existing entities** in `src/domain/entities/`
2. **Identify gaps** compared to requirements
3. **Plan enhancement strategy** maintaining backward compatibility

### Step 2: Test-Driven Development
1. **Write failing tests** for enhanced domain model
2. **Implement minimal code** to pass tests
3. **Refactor for quality** while maintaining test coverage

### Step 3: Documentation Excellence
1. **Add comprehensive docstrings** with academic context
2. **Include usage examples** for educational value
3. **Document design decisions** with rationale

### Step 4: Validation and Review
1. **Run test suite** ensuring >90% coverage
2. **Validate Clean Architecture** compliance
3. **Review educational documentation** quality

## SUCCESS CRITERIA

### Technical Success
- ✅ Enhanced Concept entity with hierarchical support
- ✅ Evidence Sentence value object with validation
- ✅ Concept Hierarchy aggregate with consistency rules
- ✅ >90% test coverage on domain model
- ✅ Clean Architecture compliance maintained

### Educational Success
- ✅ Comprehensive docstrings with domain context
- ✅ Cross-disciplinary explanations for STEM fields
- ✅ Clear examples and usage patterns
- ✅ Academic-grade documentation standards

### Research Standards Success
- ✅ Transparent algorithmic decisions
- ✅ Evidence-based concept grounding
- ✅ Reproducible test results
- ✅ Peer-review suitable documentation

## PEDAGOGICAL SCAFFOLDING

### For Computer Science Students
Focus on **design patterns** (Entity, Value Object, Aggregate) and **Clean Architecture** principles. Emphasize how domain-driven design creates maintainable, testable code.

### For Mathematics Students
Explain **graph theory foundations** of hierarchical structures. Connect tree algorithms to concept hierarchy operations like traversal and validation.

### For Physics/Engineering Students
Use **systems thinking** analogies. Compare concept extraction to **signal processing** where concepts are signals and noise must be filtered out while preserving information.

### For All Students
Emphasize **academic integrity** in software design. Show how transparent, evidence-based systems build trust in research tools.

## QUALITY ASSURANCE

1. **Run existing test suite** to ensure no regressions
2. **Validate domain model** against Clean Architecture principles
3. **Review documentation** for academic appropriateness
4. **Check pedagogical explanations** for clarity and accuracy

Begin implementation with the enhanced Concept entity, following Test-Driven Development practices and maintaining comprehensive documentation throughout the process.
