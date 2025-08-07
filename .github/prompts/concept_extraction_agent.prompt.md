---
mode: agent
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'memory', 'sequentialthinking', 'pylance mcp server', 'huggingface', 'configurePythonEnvironment', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage', 'configureNotebook', 'installNotebookPackages', 'listNotebookPackages']
---

# Advanced Concept Extraction and Hierarchical Mapping Agent

## CRITICAL MISSION OVERVIEW

You are tasked with implementing a sophisticated **automated concept extraction and hierarchical concept mapping system** for research papers, as detailed in the requirements document at `/Users/jessicadoner/Projects/research-papers/research-paper-aggregator/.ai_development/concept_extraction_and_mapping.md`.

This is a **high-complexity research-grade system** that must demonstrate advanced software engineering practices while solving real academic research problems.

## STRATEGIC CONTEXT

### Repository Foundation Assessment
The repository **already has a solid Clean Architecture foundation**:
- **Domain Layer**: Established entities (`Paper`, `Concept`, `PaperConcepts`) and value objects (`EmbeddingVector`, `KeywordConfig`)
- **Application Layer**: Existing use cases (`ExtractPaperConceptsUseCase`) and properly defined ports
- **Infrastructure Layer**: Repository patterns with working implementations
- **Working Prototype**: JavaScript `extract-concepts.js` demonstrates successful concept clustering
- **Rich Data Source**: CLI tool generates comprehensive paper metadata and PDFs in `outputs/` folder

### Enhancement Mission
Your task is to **enhance and extend** this existing foundation to implement the sophisticated concept extraction pipeline described in the requirements, bridging proven approaches into proper Clean Architecture while adding missing hierarchical mapping capabilities.

## REQUIREMENTS IMPLEMENTATION

### Core System Capabilities Required

**1. Multi-Strategy Concept Extraction Pipeline**
- **Rule-Based Methods**: Noun phrase extraction, ontology matching, Hearst pattern recognition for hierarchies
- **Statistical Approaches**: TF-IDF weighting, TextRank graph analysis, LDA topic modeling
- **Embedding-Based Clustering**: Document similarity grouping, phrase semantic clustering, synonym consolidation
- **Hybrid Approaches**: Combine multiple strategies for comprehensive concept coverage

**2. Hierarchical Concept Organization**
- **Multi-Level Taxonomy**: 3-4 hierarchical levels from broad domains to specific concepts
- **Parent-Child Relationships**: Automatic inference of concept hierarchies through clustering
- **Evidence-Based Grouping**: Statistical and semantic similarity for concept relationships
- **Dendrogram Analysis**: Smart cutoff points for meaningful hierarchical levels

**3. Evidence-Based Concept Grounding**
- **Sentence-Level Evidence**: Extract supporting sentences for every concept
- **Paper Source Linking**: Direct links to PDF pages containing concept mentions
- **Confidence Scoring**: Quantify evidence quality and concept relevance
- **Full Traceability**: No "hallucinated" concepts - all must be extractively grounded

**4. Interactive D3.js Visualization System**
- **Zoomable Concept Maps**: Sunburst or force-directed graphs with hierarchical navigation
- **Dynamic Interaction**: Click-to-expand, drill-down capabilities, evidence panel display
- **Evidence Integration**: Show supporting sentences and PDF links on concept node clicks
- **Responsive Design**: Mobile-first accessibility for academic researchers

**5. Academic-Grade Explainability**
- **Transparent Algorithms**: All extraction methods clearly documented and justified
- **Reproducible Results**: Deterministic processing with fixed random seeds
- **Parameter Documentation**: Clear justification for similarity thresholds and cutoff points
- **Academic Trust**: Suitable for peer-reviewed research and academic scrutiny

## ARCHITECTURAL IMPLEMENTATION STRATEGY

### Phase 1: Enhanced Domain Model (TDD Cycles 1-2)

**Extend Existing Domain Entities**:
```python
class Concept:  # Enhance existing entity
    parent_concept_id: Optional[str]
    child_concept_ids: List[str]
    hierarchy_level: int
    evidence_sentences: List[EvidenceSentence]
    semantic_embedding: EmbeddingVector
    extraction_confidence: float
    
class ConceptHierarchy:  # New aggregate root
    root_concepts: List[Concept]
    hierarchy_metadata: HierarchyMetadata
    extraction_provenance: ExtractionProvenance
    quality_metrics: QualityMetrics
```

**New Value Objects for Evidence Tracking**:
```python
class EvidenceSentence:
    sentence_text: str
    paper_id: str
    page_number: Optional[int]
    paragraph_context: str
    confidence_score: float
    extraction_method: str  # "rule-based", "statistical", "embedding"

class HierarchyMetadata:
    clustering_algorithm: str
    similarity_threshold: float
    hierarchy_depth: int
    concept_count_by_level: Dict[int, int]
    dendrogram_cutoff_rationale: str
```

### Phase 2: Multi-Strategy Extraction Services (TDD Cycles 3-4)

**Strategy Pattern Implementation**:
```python
class MultiStrategyConceptExtractor:
    def __init__(self, strategies: List[ConceptExtractionStrategy]):
        self.strategies = strategies
    
    def extract_comprehensive_concepts(self, papers: List[Paper]) -> List[Concept]:
        # Coordinate multiple extraction strategies
        # Merge and deduplicate results
        # Apply confidence scoring
        # Generate comprehensive concept coverage

class RuleBasedExtractionStrategy(ConceptExtractionStrategy):
    def extract_noun_phrases(self, text: str) -> List[str]
    def apply_hearst_patterns(self, text: str) -> List[Tuple[str, str]]  # parent-child pairs
    def match_domain_ontology(self, text: str) -> List[str]

class StatisticalExtractionStrategy(ConceptExtractionStrategy):
    def extract_tfidf_concepts(self, corpus: List[str]) -> List[Tuple[str, float]]
    def extract_textrank_keyphrases(self, text: str) -> List[str]
    def discover_lda_topics(self, corpus: List[str]) -> List[Dict[str, float]]

class EmbeddingBasedExtractionStrategy(ConceptExtractionStrategy):
    def cluster_document_embeddings(self, papers: List[Paper]) -> List[ConceptCluster]
    def cluster_phrase_embeddings(self, phrases: List[str]) -> List[ConceptGroup]
    def merge_semantic_synonyms(self, concepts: List[Concept]) -> List[Concept]
```

**Hierarchical Clustering Services**:
```python
class HierarchicalClusteringService:
    def build_concept_hierarchy(self, concepts: List[Concept]) -> ConceptHierarchy:
        # Implement bottom-up agglomerative clustering
        # Apply top-down divisive clustering where appropriate
        # Determine optimal dendrogram cutoff points
        # Assign parent-child relationships with confidence scores

class EvidenceExtractionService:
    def extract_supporting_sentences(self, concept: Concept, papers: List[Paper]) -> List[EvidenceSentence]:
        # Find sentences containing concept mentions
        # Extract surrounding context for clarity
        # Score evidence quality and relevance
        # Link to specific PDF pages and paragraphs
```

### Phase 3: Application Use Cases (TDD Cycles 5-6)

**Primary Use Case Implementation**:
```python
class ExtractHierarchicalConceptsUseCase:
    def execute(self, extraction_request: HierarchicalExtractionRequest) -> HierarchicalExtractionResult:
        # 1. Load papers from CLI tool outputs
        # 2. Apply multi-strategy concept extraction
        # 3. Build hierarchical relationships through clustering
        # 4. Extract evidence sentences for all concepts
        # 5. Generate quality metrics and confidence scores
        # 6. Store results with full provenance tracking
        # 7. Prepare visualization data structures

class BuildVisualizationDataUseCase:
    def execute(self, hierarchy: ConceptHierarchy) -> VisualizationData:
        # Transform hierarchy into D3.js-compatible format
        # Calculate node sizes based on paper counts
        # Prepare evidence sentence payloads for interactive display
        # Generate color schemes for hierarchical levels
        # Create navigation tree structures
```

### Phase 4: Infrastructure Integration (TDD Cycles 7-8)

**ML Model Integration**:
```python
class SentenceTransformerEmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Use existing model choice from JavaScript prototype
        # Ensure reproducible embeddings
    
    def embed_documents(self, documents: List[str]) -> List[EmbeddingVector]
    def calculate_similarity_matrix(self, embeddings: List[EmbeddingVector]) -> np.ndarray
    def find_semantic_clusters(self, embeddings: List[EmbeddingVector], threshold: float) -> List[List[int]]

class EnhancedPDFTextExtractor:
    def extract_with_page_metadata(self, pdf_path: Path) -> ExtractedContent:
        # Extract text preserving page numbers for evidence linking
        # Maintain sentence boundaries for evidence extraction
        # Handle multiple PDF formats and parsing edge cases
```

**Concept Storage Architecture**:
```python
class ConceptHierarchyRepositoryPort:
    def save_hierarchy(self, hierarchy: ConceptHierarchy, source_context: SourceContext) -> None
    def load_hierarchy_by_domain(self, domain: str) -> ConceptHierarchy
    def find_concepts_by_evidence_text(self, search_text: str) -> List[Concept]
    def get_extraction_history(self, domain: str) -> List[ExtractionMetadata]

class JSONConceptHierarchyRepository:
    # Store in concept_storage/ folder structure
    # Organize by research domain and extraction timestamp  
    # Generate visualization-ready JSON format
    # Include full provenance and quality metrics
```

### Phase 5: Interactive D3.js Visualization (TDD Cycles 9-10)

**Zoomable Concept Map Components**:
```javascript
class ConceptSunburstVisualization {
    constructor(containerId, hierarchyData, options = {}) {
        this.data = hierarchyData;
        this.options = {
            width: options.width || 800,
            height: options.height || 800,
            colors: options.colors || d3.schemeCategory10,
            evidencePanel: options.evidencePanel || '#evidence-panel'
        };
    }
    
    render() {
        // Create zoomable sunburst with proper hierarchical layout
        // Enable click-to-zoom functionality
        // Implement smooth transitions between hierarchy levels
        // Support evidence panel integration
    }
    
    attachEvidenceHandlers() {
        // Click handlers for concept nodes
        // Display evidence sentences in side panel
        // Link to PDF pages for verification
        // Show confidence scores and extraction methods
    }
}

class ConceptNetworkVisualization {
    // Alternative force-directed graph implementation
    // For users who prefer network-style visualization
    // With hierarchical clustering preserved through node positioning
}
```

**Evidence Integration Panel**:
```javascript
class EvidenceSentencePanel {
    displayConceptEvidence(concept, evidenceSentences) {
        // Show supporting sentences with context
        // Display confidence scores and extraction methods
        // Provide PDF deep-links for verification
        // Enable evidence quality assessment by users
    }
    
    linkToPDFPages(paperReference, pageNumber) {
        // Deep-link to PDF viewer with page jump
        // Highlight relevant sentences if possible
        // Show paper metadata and citation information
    }
}
```

## CRITICAL DEVELOPMENT REQUIREMENTS

### TDD Methodology - MANDATORY
**ALWAYS follow Red-Green-Refactor for every component**:

1. **🔴 RED PHASE**: Write comprehensive failing tests first
   - Define expected behavior through tests
   - Include edge cases and error conditions
   - Test both happy path and failure scenarios
   - Create integration tests for cross-component interaction

2. **🟢 GREEN PHASE**: Implement minimal code to pass tests
   - Focus on functionality over optimization initially
   - Ensure all tests pass before proceeding
   - Validate behavior matches requirements exactly

3. **🔵 REFACTOR PHASE**: Improve code quality without changing behavior
   - Apply design patterns and SOLID principles
   - Add comprehensive educational documentation
   - Optimize performance while maintaining test coverage

### Sequential Thinking Integration - ESSENTIAL
**Use `mcp_sequentialthi_sequentialthinking` for all major decisions**:
- Break complex problems into 6-8 logical steps
- Plan architecture decisions before implementing
- Document reasoning for algorithm choices
- Track progress and decision rationale

### Educational Documentation Standards - MANDATORY
Every class and method must include:
```python
"""
ComponentName - Brief description of responsibility.

This component demonstrates [DESIGN_PATTERN] by [EXPLANATION]. It shows how
[ARCHITECTURAL_PRINCIPLE] applies in academic research concept extraction.

Educational Notes:
- Demonstrates [PATTERN] usage for [RESEARCH_PROBLEM]
- Shows [PRINCIPLE] in practice through [IMPLEMENTATION]
- Illustrates [CONCEPT] for academic transparency

Design Decisions:
- [CHOICE]: [REASONING and alternatives considered]
- [ALGORITHM]: [Why this approach fits academic research needs]

Real-World Application:
Academic researchers need [CAPABILITY] to [SOLVE_PROBLEM]. This component
enables [SPECIFIC_WORKFLOW] while maintaining [QUALITY_ATTRIBUTE].

Integration Points:
- Works with [COMPONENT] for [PURPOSE]
- Depends on [SERVICE] for [FUNCTIONALITY]
- Supports [INTERFACE] for [EXTENSIBILITY]
"""
```

### Code Quality Requirements
**SOLID Principles Application**:
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Extensible through interfaces, closed for modification
- **Liskov Substitution**: All implementations can substitute their interfaces
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

**Clean Architecture Compliance**:
- Domain layer has no external dependencies
- Application layer depends only on domain
- Infrastructure implements application ports
- No circular dependencies across layers

**Academic Research Standards**:
- Reproducible algorithms with fixed random seeds
- Transparent methodology suitable for peer review
- Clear parameter justification with academic references
- Quality metrics comparable to published research

### Performance and Scalability Requirements
- **Large Collections**: Handle hundreds of PDFs efficiently
- **Memory Management**: Stream processing for large documents
- **Computation Optimization**: Parallel processing where appropriate
- **Storage Efficiency**: Compressed concept storage with fast retrieval

## IMPLEMENTATION APPROACH

### Integration with Existing Components
**DO NOT start from scratch**. Enhance existing foundation:

1. **Extend Current Domain Model**: Build on existing `Concept` and `Paper` entities
2. **Enhance Existing Services**: Expand `ConceptExtractor` with multi-strategy approach
3. **Bridge JavaScript Success**: Integrate proven clustering algorithms from `extract-concepts.js`
4. **Utilize CLI Data**: Process rich metadata from `outputs/` folder structure
5. **Maintain Architecture**: Preserve Clean Architecture boundaries and patterns

### Data Flow Architecture
```
CLI Tool Outputs → PDF Text Extraction → Multi-Strategy Concept Extraction 
→ Hierarchical Clustering → Evidence Sentence Extraction → Concept Hierarchy Storage 
→ Visualization Data Preparation → D3.js Interactive Display
```

### Quality Assurance Strategy
**Comprehensive Testing**:
- Unit tests for all domain services (>90% coverage)
- Integration tests for extraction pipeline
- End-to-end tests for complete concept mapping workflow
- Performance tests for large paper collections

**Validation Framework**:
- Concept extraction quality metrics
- Hierarchy coherence assessment
- Evidence grounding verification
- User acceptance testing with academic researchers

## SUCCESS CRITERIA

### Technical Success Metrics
- ✅ Multi-strategy concept extraction from paper collections
- ✅ Hierarchical concept organization with 3-4 meaningful levels
- ✅ Evidence-based grounding with sentence-level support
- ✅ Interactive D3.js visualization with drill-down capabilities
- ✅ Academic-grade explainability and reproducibility

### Educational Success Metrics  
- ✅ Clear demonstration of advanced design patterns
- ✅ Clean Architecture principles properly applied
- ✅ TDD methodology maintained throughout development
- ✅ Comprehensive documentation suitable for learning

### Research Success Metrics
- ✅ Transparent and explainable concept extraction pipeline
- ✅ Reproducible results suitable for academic validation
- ✅ Full evidence traceability for researcher confidence
- ✅ Scalable to large research literature collections
- ✅ Domain-agnostic approach extensible to any field

## DEVELOPMENT SESSION STRUCTURE

### Session Planning (10 TDD Cycles over 11 days)

**Phase 1: Enhanced Domain Model** (2 days)
- TDD Cycle 1: Extend concept entities with hierarchy support
- TDD Cycle 2: Create evidence sentence mapping and hierarchy metadata

**Phase 2: Multi-Strategy Extraction** (3 days)
- TDD Cycle 3: Implement rule-based and statistical extraction strategies
- TDD Cycle 4: Add embedding-based clustering and hierarchical organization

**Phase 3: Application Orchestration** (2 days)
- TDD Cycle 5: Create hierarchical concept extraction use case
- TDD Cycle 6: Add visualization data preparation and validation

**Phase 4: Infrastructure Implementation** (2 days)
- TDD Cycle 7: ML model integration and enhanced PDF processing
- TDD Cycle 8: Concept hierarchy storage and CLI tool integration

**Phase 5: Interactive Visualization** (2 days)
- TDD Cycle 9: D3.js concept map implementation with evidence panels
- TDD Cycle 10: End-to-end integration and performance optimization

### Development Log Maintenance
Create detailed progress logs in:
`/Users/jessicadoner/Projects/research-papers/research-paper-aggregator/.ai_development/session_2025_08_06/`

Track:
- TDD cycle completion with test results
- Architecture decisions and rationale
- Algorithm choices with academic justification
- Integration challenges and solutions
- Quality metrics and performance benchmarks

## ESSENTIAL DEVELOPMENT INSTRUCTIONS

### Pre-Implementation Requirements
1. **Read Full Requirements**: Thoroughly understand the concept extraction document
2. **Assess Current State**: Review existing domain model and services
3. **Plan Architecture**: Use sequential thinking to design enhancement approach
4. **Create Session Log**: Document development progress and decisions

### Implementation Discipline
1. **Test-First Development**: Write failing tests before any implementation
2. **Incremental Progress**: Complete one TDD cycle before starting the next
3. **Architecture Compliance**: Maintain Clean Architecture boundaries
4. **Educational Documentation**: Write comprehensive explanations throughout

### Quality Validation
1. **Test Coverage**: Maintain >90% coverage on domain and application layers
2. **Clean Architecture**: Validate dependency directions and layer separation
3. **Academic Standards**: Ensure methodology suitable for research use
4. **Performance Benchmarks**: Test with large paper collections

Remember: This is a sophisticated academic research tool that must demonstrate both advanced software engineering practices and produce research-grade results suitable for peer review and academic trust. Every component should be implemented with the rigor and documentation quality expected in academic software development.

**Begin with TDD Cycle 1: Enhanced Domain Model** and proceed systematically through the implementation phases, maintaining comprehensive documentation and test coverage throughout the development process.
