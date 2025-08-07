# Concept Extraction and Hierarchical Mapping Implementation Plan
**Session: August 6, 2025**

## Project Context and Current State Analysis

### Repository Assessment ✅ COMPLETE

**Clean Architecture Foundation** - STRONG:
- **Domain Layer**: Well-established entities (`Paper`, `Concept`, `PaperConcepts`) and value objects (`EmbeddingVector`, `KeywordConfig`)
- **Application Layer**: Use cases (`ExtractPaperConceptsUseCase`) and ports properly defined  
- **Infrastructure Layer**: Repository patterns implemented with in-memory and persistent storage options
- **TDD Framework**: Comprehensive test coverage with educational documentation standards

**Existing Concept Extraction Capability** - PARTIAL:
- **Python Domain Services**: `ConceptExtractor` with strategy pattern implementation
- **JavaScript Prototype**: Working `extract-concepts.js` with embedding-based clustering and hierarchy building
- **Data Pipeline**: Rich metadata from CLI tool (`outputs/` folder with PDFs and comprehensive JSON metadata)
- **Visualization Foundation**: Basic concept mapping structures exist

**Integration Opportunities Identified**:
- CLI tool generates comprehensive metadata.json files with abstracts, titles, authors, DOIs
- JavaScript prototype successfully demonstrates hierarchical concept clustering
- Python Clean Architecture provides proper domain modeling foundation
- Gap exists between prototype and full requirements implementation

## Requirements Analysis

### Core Requirements from Concept Extraction Document

1. **Multi-Strategy Concept Extraction**:
   - Rule-based extraction (noun phrases, ontology matching, Hearst patterns)
   - Statistical methods (TF-IDF, TextRank, topic modeling)
   - Embedding-based clustering (document similarity, phrase embeddings)
   - Supervised approaches (where applicable)

2. **Hierarchical Concept Organization**:
   - Bottom-up agglomerative clustering
   - Top-down divisive clustering  
   - Concept parent-child relationship inference
   - Multi-level taxonomy construction (3-4 levels optimal)

3. **Evidence-Based Grounding**:
   - Extract supporting sentences for each concept
   - Link concepts to source paper locations
   - Maintain full traceability for academic trust
   - No "hallucinated" concepts - all must be present in text

4. **Interactive D3.js Visualization**:
   - Zoomable concept maps (sunburst or tree layouts)
   - Click-to-expand functionality
   - Evidence sentence display on node click
   - PDF deep-linking for verification

5. **Explainability and Reproducibility**:
   - Transparent algorithms with parameter justification
   - Deterministic results (fixed random seeds)
   - Step-by-step process documentation
   - Academic-grade methodology suitable for researchers

## Implementation Strategy

### Phase 1: Enhanced Domain Model (TDD Cycles 1-2)
**Expand existing domain entities to support hierarchical concept mapping**

**New Domain Entities** (extend existing):
```python
# Enhance existing Concept entity
class Concept:  # Existing - enhance with hierarchy support
    parent_concept_id: Optional[str]
    child_concept_ids: List[str] 
    hierarchy_level: int
    evidence_sentences: List[EvidenceSentence]

# New hierarchical structure entity  
class ConceptHierarchy:
    root_concepts: List[Concept]
    hierarchy_metadata: HierarchyMetadata
    extraction_provenance: ExtractionProvenance
```

**New Value Objects**:
```python
class EvidenceSentence:  # Already exists - enhance
    sentence_text: str
    paper_id: str
    page_number: Optional[int]
    confidence_score: float
    extraction_method: str

class HierarchyMetadata:
    clustering_algorithm: str  
    similarity_threshold: float
    hierarchy_depth: int
    concept_count: int

class ExtractionProvenance:
    extraction_timestamp: datetime
    algorithm_versions: Dict[str, str]
    parameter_settings: Dict[str, Any]
    quality_metrics: QualityMetrics
```

### Phase 2: Multi-Strategy Extraction Services (TDD Cycles 3-4)
**Implement the comprehensive extraction pipeline described in requirements**

**Enhanced Domain Services**:
```python
class MultiStrategyConceptExtractor:
    strategies: List[ConceptExtractionStrategy]
    
    # Implement all extraction methods from requirements:
    # - Rule-based: noun phrases, ontology lookup, Hearst patterns
    # - Statistical: TF-IDF, TextRank, topic modeling (LDA)
    # - Embedding-based: document clustering, phrase similarity
    # - Consolidation: duplicate removal, synonym merging

class HierarchicalClusteringService:
    # Implement clustering approaches from requirements:
    # - Bottom-up agglomerative clustering
    # - Top-down divisive clustering  
    # - Multi-level hierarchy construction
    # - Parent-child relationship inference

class EvidenceExtractionService:
    # Extract supporting sentences for concepts
    # Link concepts to paper locations
    # Generate confidence scores for evidence quality
```

**Extraction Strategy Implementations** (Strategy Pattern):
```python
class RuleBasedExtractionStrategy:
    def extract_noun_phrases(self, text: str) -> List[str]
    def apply_hearst_patterns(self, text: str) -> List[Tuple[str, str]]  # parent-child
    def match_ontology_terms(self, text: str, ontology: Ontology) -> List[str]

class StatisticalExtractionStrategy:
    def extract_tfidf_concepts(self, corpus: List[str]) -> List[str]
    def extract_textrank_concepts(self, text: str) -> List[str]
    def extract_lda_topics(self, corpus: List[str]) -> List[str]

class EmbeddingBasedExtractionStrategy:
    def cluster_documents(self, papers: List[Paper]) -> List[ConceptCluster]
    def cluster_phrases(self, phrases: List[str]) -> List[ConceptGroup]
    def calculate_semantic_similarity(self, phrase1: str, phrase2: str) -> float
```

### Phase 3: Enhanced Application Use Cases (TDD Cycles 5-6)
**Orchestrate the extraction pipeline with proper Clean Architecture patterns**

**New Use Cases**:
```python
class ExtractHierarchicalConceptsUseCase:
    def execute(self, papers: List[Paper], config: ExtractionConfig) -> ConceptHierarchy:
        # 1. Extract candidate concepts using multiple strategies
        # 2. Consolidate and deduplicate concepts  
        # 3. Build hierarchical relationships
        # 4. Extract evidence sentences
        # 5. Generate visualization data
        # 6. Store results with full provenance

class BuildVisualizationDataUseCase:
    def execute(self, hierarchy: ConceptHierarchy) -> VisualizationData:
        # Transform concept hierarchy into D3.js-compatible format
        # Include node sizes, colors, relationship data
        # Embed evidence sentences and paper links
        # Generate interactive navigation structure

class ValidateConceptExtractionUseCase:
    def execute(self, extraction_results: ConceptHierarchy) -> ValidationReport:
        # Quality assessment of extracted concepts
        # Coverage analysis (ensure all papers represented)
        # Hierarchy coherence validation
        # Evidence grounding verification
```

**Enhanced Repository Ports**:
```python
class ConceptHierarchyRepositoryPort:
    def save_hierarchy(self, hierarchy: ConceptHierarchy, source_context: SourceContext) -> None
    def load_hierarchy(self, paper_ids: List[str]) -> ConceptHierarchy
    def find_concepts_by_evidence(self, search_text: str) -> List[Concept]
    def get_hierarchy_metadata(self, hierarchy_id: str) -> HierarchyMetadata
```

### Phase 4: Infrastructure Implementation (TDD Cycles 7-8)
**Implement concrete storage, ML model integration, and PDF processing**

**Infrastructure Services**:
```python
# Extend existing PDF extraction
class EnhancedPDFTextExtractor:
    def extract_text_with_metadata(self, pdf_path: Path) -> ExtractedContent:
        # Extract text with page numbers for evidence linking
        # Preserve sentence boundaries for evidence extraction
        # Handle multiple PDF formats and edge cases

# ML Model Integration  
class SentenceTransformerEmbeddingService:
    def embed_documents(self, documents: List[str]) -> List[EmbeddingVector]
    def embed_phrases(self, phrases: List[str]) -> List[EmbeddingVector]
    def calculate_similarity_matrix(self, embeddings: List[EmbeddingVector]) -> np.ndarray

# Concept Storage
class JSONConceptHierarchyRepository:
    def save_hierarchy(self, hierarchy: ConceptHierarchy) -> None:
        # Store in `concept_storage/` folder structure
        # Organize by research domain and extraction timestamp
        # Include visualization-ready JSON format

class DatabaseConceptHierarchyRepository:
    # Optional: Full database implementation for production use
```

### Phase 5: Interactive Visualization (TDD Cycles 9-10)
**Create D3.js-based interactive concept maps**

**D3.js Visualization Components**:
```javascript
// Zoomable Sunburst Concept Map
class ConceptSunburstViz {
    constructor(containerId, hierarchyData)
    render()
    enableZoomNavigation()
    attachEvidenceClickHandlers()
    updateNodeSizes()  // Based on paper counts
}

// Force-Directed Graph Alternative
class ConceptNetworkViz {
    constructor(containerId, hierarchyData)
    simulateForces()
    enableDragInteraction()
    highlightPathways()
}

// Evidence Panel Integration
class EvidenceSentencePanel {
    displayEvidence(concept, evidenceSentences)
    linkToPDFPages(paperReference, pageNumber)
    showConfidenceScores()
}
```

**Next.js Integration**:
```typescript
// API routes for serving concept data
pages/api/concepts/[domain].ts
pages/api/evidence/[conceptId].ts

// Interactive concept map page
pages/concepts/[domain].tsx
components/ConceptVisualization.tsx
components/EvidencePanel.tsx
```

## Development Session Plan

### Session Structure (10 TDD Cycles)

**TDD Cycles 1-2: Enhanced Domain Model** (2 days)
- Extend existing `Concept` entity with hierarchy support
- Create `ConceptHierarchy` aggregate root
- Add evidence sentence mapping value objects
- Comprehensive test coverage for hierarchical relationships

**TDD Cycles 3-4: Multi-Strategy Extraction** (3 days)  
- Implement rule-based, statistical, and embedding extraction strategies
- Create hierarchical clustering service
- Add evidence extraction and linking
- Bridge JavaScript clustering algorithms into Clean Architecture

**TDD Cycles 5-6: Application Orchestration** (2 days)
- Create `ExtractHierarchicalConceptsUseCase`
- Add visualization data preparation use case
- Implement concept validation and quality assessment
- Error handling and result reporting

**TDD Cycles 7-8: Infrastructure Implementation** (2 days)
- Enhanced PDF text extraction with metadata
- ML model integration (sentence-transformers)
- Concept hierarchy storage (JSON and optional database)
- Integration with existing CLI tool outputs

**TDD Cycles 9-10: Interactive Visualization** (2 days)
- D3.js concept map implementations (sunburst + network)
- Evidence sentence panel with PDF linking
- Next.js API integration
- End-to-end interaction testing

### Quality Assurance Strategy

**Test-Driven Development**:
- Write failing tests first for each component
- Maintain >90% test coverage on domain and application layers
- Include contract tests for all ports
- End-to-end testing for complete concept extraction workflows

**Educational Documentation**:
- Comprehensive module docstrings explaining design decisions
- Algorithm explanation with academic references
- Real-world application examples for researchers
- Cross-references between architectural components

**Code Quality Standards**:
- SOLID principles demonstrated throughout
- Clean Architecture boundaries strictly enforced
- Design patterns clearly documented and justified
- Academic-grade methodology with reproducible results

### Success Criteria

**Technical Success**:
- ✅ Comprehensive concept extraction from paper collections
- ✅ Multi-level hierarchical concept organization  
- ✅ Evidence-based grounding with full traceability
- ✅ Interactive D3.js visualization with evidence drill-down
- ✅ Integration with existing CLI tool and Clean Architecture

**Educational Success**:
- ✅ Clear demonstration of TDD methodology
- ✅ Practical application of Clean Architecture patterns
- ✅ Domain-driven design in academic research context
- ✅ Advanced design patterns (Strategy, Repository, Adapter)
- ✅ ML integration within Clean Architecture boundaries

**Research Success**:
- ✅ Transparent and explainable concept extraction
- ✅ Reproducible results suitable for academic use
- ✅ Full evidence traceability for researcher trust
- ✅ Scalable to large paper collections (hundreds of PDFs)
- ✅ Domain-agnostic approach extensible to any research field

---

**Next Action**: Create agent prompt for implementation based on this comprehensive plan.

**Implementation Priority**: Begin with TDD Cycles 1-2 to establish enhanced domain model, then proceed systematically through the pipeline implementation.

**Risk Mitigation**: Extensive testing, incremental development, and integration with existing working components minimize implementation risks.
