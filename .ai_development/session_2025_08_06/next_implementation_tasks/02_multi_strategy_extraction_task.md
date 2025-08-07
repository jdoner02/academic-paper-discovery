# Task 02: Multi-Strategy Concept Extraction Services Implementation

## Priority: HIGH (TDD Cycles 3-4)
**Estimated Time**: 8-10 hours  
**Prerequisites**: Task 01 (Domain Model Enhancement) completed  
**Dependencies**: Enhanced domain model with evidence support

## Objective
Implement the multi-strategy concept extraction pipeline as specified in the concept extraction analysis, combining rule-based, statistical, and embedding-based approaches for comprehensive concept coverage.

## Current State Assessment
Based on analysis of `/Users/jessicadoner/Projects/research-papers/research-paper-aggregator/src/`:

### Existing Components ✅
- `infrastructure/services/sentence_transformer_embedding_service.py` - Basic embedding generation
- `application/use_cases/extract_paper_concepts_use_case.py` - Single-strategy extraction
- `domain/services/` - Empty directory ready for new services

### Missing Critical Components ❌
- Rule-based noun phrase and pattern extraction
- Statistical TF-IDF and TextRank implementations
- Embedding-based clustering and synonym detection
- Strategy coordination and result merging
- Confidence scoring across different extraction methods

## Implementation Requirements

### 1. Strategy Pattern Foundation (Red Phase)
Create comprehensive tests for the strategy pattern implementation:

```python
# Test file: tests/unit/domain/services/test_multi_strategy_extractor.py
class TestMultiStrategyConceptExtractor:
    def test_coordinates_multiple_extraction_strategies(self):
        # Test that extractor runs all strategies and merges results
        
    def test_handles_strategy_failures_gracefully(self):
        # Test resilience when individual strategies fail
        
    def test_merges_overlapping_concepts_correctly(self):
        # Test deduplication of concepts found by multiple strategies
```

**Domain Services to Create**:
- `src/domain/services/concept_extraction_strategy.py` (Abstract base)
- `src/domain/services/multi_strategy_concept_extractor.py`
- `src/domain/services/rule_based_extraction_strategy.py`
- `src/domain/services/statistical_extraction_strategy.py`
- `src/domain/services/embedding_extraction_strategy.py`

### 2. Rule-Based Extraction Strategy (Green Phase)
Implement transparent, explainable rule-based extraction:

```python
# Create: src/domain/services/rule_based_extraction_strategy.py
class RuleBasedExtractionStrategy(ConceptExtractionStrategy):
    """
    Rule-based concept extraction using linguistic patterns.
    
    Educational Notes:
    - Demonstrates symbolic AI approach to NLP
    - Shows explicit pattern matching vs black-box ML
    - Illustrates transparency requirements for academic trust
    
    Methods:
    - Noun phrase extraction using POS tagging
    - Hearst pattern matching for hierarchical relationships
    - Technical term identification through capitalization patterns
    - Acronym and abbreviation detection
    """
    
    def extract_noun_phrases(self, text: str) -> List[ConceptCandidate]:
        """Extract noun phrases using spaCy POS tagging."""
        
    def apply_hearst_patterns(self, text: str) -> List[Tuple[str, str]]:
        """Find 'X is a Y' hierarchical relationships."""
        
    def identify_technical_terms(self, text: str) -> List[ConceptCandidate]:
        """Identify capitalized terms and acronyms."""
        
    def filter_generic_terms(self, candidates: List[ConceptCandidate]) -> List[ConceptCandidate]:
        """Remove non-specific terms like 'approach', 'method'."""
```

### 3. Statistical Extraction Strategy (Green Phase)
Implement mathematical approaches for concept importance:

```python
# Create: src/domain/services/statistical_extraction_strategy.py
class StatisticalExtractionStrategy(ConceptExtractionStrategy):
    """
    Statistical concept extraction using TF-IDF, TextRank, and LDA.
    
    Educational Notes:
    - Demonstrates information theory application to text analysis
    - Shows PageRank algorithm adaptation for NLP
    - Illustrates probabilistic topic modeling principles
    
    Methods:
    - TF-IDF scoring for term importance
    - TextRank graph-based ranking
    - LDA topic modeling for theme discovery
    """
    
    def calculate_tfidf_scores(self, corpus: List[str]) -> Dict[str, float]:
        """Calculate TF-IDF scores for all terms in corpus."""
        
    def extract_textrank_concepts(self, text: str) -> List[ConceptCandidate]:
        """Use TextRank algorithm for keyphrase extraction."""
        
    def discover_lda_topics(self, corpus: List[str]) -> List[TopicModel]:
        """Apply LDA topic modeling for concept themes."""
```

### 4. Embedding-Based Extraction Strategy (Refactor Phase)
Implement semantic similarity-based extraction:

```python
# Create: src/domain/services/embedding_extraction_strategy.py
class EmbeddingExtractionStrategy(ConceptExtractionStrategy):
    """
    Embedding-based concept extraction using semantic similarity.
    
    Educational Notes:
    - Demonstrates distributed representation in NLP
    - Shows vector space model applications
    - Illustrates unsupervised learning for concept discovery
    
    Methods:
    - Document clustering for concept areas
    - Phrase clustering for synonym detection
    - Hierarchical clustering for concept organization
    """
    
    def cluster_documents_by_similarity(self, papers: List[ResearchPaper]) -> List[ConceptCluster]:
        """Group papers by semantic similarity."""
        
    def cluster_phrase_embeddings(self, phrases: List[str]) -> List[ConceptGroup]:
        """Group semantically similar phrases."""
        
    def detect_synonyms_through_clustering(self, concepts: List[Concept]) -> List[ConceptGroup]:
        """Merge concepts that are semantic synonyms."""
```

## Infrastructure Integration Requirements

### 1. Enhanced PDF Text Extraction
```python
# Enhance: src/infrastructure/services/pdf_extractor.py
class EnhancedPDFTextExtractor:
    """
    PDF text extraction with page and sentence metadata for evidence linking.
    
    Educational Notes:
    - Shows document processing pipeline design
    - Demonstrates metadata preservation for traceability
    - Illustrates structured data extraction from unstructured sources
    """
    
    def extract_with_sentence_boundaries(self, pdf_path: Path) -> ExtractedContent:
        """Extract text preserving sentence boundaries and page numbers."""
        
    def extract_with_section_headers(self, pdf_path: Path) -> StructuredDocument:
        """Extract text with section structure for better concept context."""
```

### 2. External Library Integrations
```python
# Create: src/infrastructure/services/spacy_linguistic_processor.py
class SpacyLinguisticProcessor:
    """spaCy integration for linguistic analysis."""
    
# Create: src/infrastructure/services/sklearn_statistical_processor.py
class SklearnStatisticalProcessor:
    """scikit-learn integration for statistical analysis."""
    
# Create: src/infrastructure/services/networkx_graph_processor.py
class NetworkxGraphProcessor:
    """NetworkX integration for TextRank graph analysis."""
```

## Test Strategy

### Unit Tests for Each Strategy
```python
# Example test structure for rule-based strategy
class TestRuleBasedExtractionStrategy:
    def test_extracts_technical_noun_phrases(self):
        text = "We propose a convolutional neural network for image classification."
        strategy = RuleBasedExtractionStrategy()
        concepts = strategy.extract_concepts(text)
        assert "convolutional neural network" in [c.name for c in concepts]
        
    def test_applies_hearst_patterns_correctly(self):
        text = "Machine learning is a subset of artificial intelligence."
        strategy = RuleBasedExtractionStrategy()
        relations = strategy.apply_hearst_patterns(text)
        assert ("machine learning", "artificial intelligence") in relations
```

### Integration Tests Across Strategies
```python
class TestMultiStrategyIntegration:
    def test_strategies_complement_each_other(self):
        # Test that different strategies find different types of concepts
        
    def test_concept_merging_preserves_evidence(self):
        # Test that evidence is preserved when merging concepts from different strategies
        
    def test_confidence_scoring_reflects_strategy_agreement(self):
        # Test that concepts found by multiple strategies get higher confidence
```

### Performance Tests
```python
class TestExtractionPerformance:
    def test_processes_hundred_papers_within_time_limit(self):
        # Test scalability requirements
        
    def test_memory_usage_remains_reasonable(self):
        # Test memory efficiency with large document collections
```

## Educational Documentation Requirements

### Strategy Pattern Explanation
Each strategy must document:
1. **Theoretical Foundation**: Mathematical or linguistic principles
2. **Algorithm Steps**: Clear explanation of processing steps
3. **Strengths and Limitations**: When to use each approach
4. **Parameter Tuning**: How to adjust for different domains
5. **Example Outputs**: Concrete examples with academic papers

### Cross-Disciplinary Education
```python
"""
TF-IDF (Term Frequency-Inverse Document Frequency) Explanation:

For Mathematics Students:
TF-IDF applies information theory to text analysis. The formula:
TF-IDF(t,d,D) = TF(t,d) × log(|D| / |{d ∈ D : t ∈ d}|)

This balances local importance (how often a term appears in a document)
with global rarity (how unique the term is across the collection).

For Physics Students:
Think of TF as the "amplitude" of a term's signal in a document, and
IDF as a filter that amplifies rare signals and dampens common noise.

For Engineering Students:
TF-IDF is a feature extraction technique that converts text into
numerical vectors suitable for machine learning algorithms.
"""
```

## Validation Criteria

### Functional Requirements ✅
- [ ] Each strategy extracts different types of concepts effectively
- [ ] Strategies can be combined without conflicts
- [ ] Concept deduplication works across strategy boundaries
- [ ] Evidence links are preserved through all extraction steps
- [ ] Confidence scores reflect extraction quality

### Quality Requirements ✅
- [ ] >90% test coverage on all extraction strategies
- [ ] Performance scales to hundreds of academic papers
- [ ] Memory usage remains under reasonable limits
- [ ] All extraction decisions are explainable and traceable

### Academic Requirements ✅
- [ ] Rule-based strategy is completely transparent
- [ ] Statistical methods use well-established algorithms
- [ ] Embedding methods use open, inspectable models
- [ ] All parameters have academic justification

## Implementation Steps

### Step 1: Red Phase (Strategy Pattern Foundation)
1. Create abstract base class for extraction strategies
2. Write comprehensive tests for multi-strategy coordination
3. Define interfaces for concept merging and confidence scoring
4. Run tests to confirm appropriate failures

### Step 2: Green Phase (Individual Strategies)
1. Implement rule-based strategy with spaCy integration
2. Implement statistical strategy with scikit-learn integration
3. Implement embedding strategy with sentence-transformers
4. Create multi-strategy coordinator
5. Ensure all tests pass

### Step 3: Refactor Phase (Optimization and Documentation)
1. Add comprehensive educational documentation
2. Optimize performance for large document collections
3. Add configurable parameters for domain adaptation
4. Create usage examples and tutorials

## Files Modified/Created

### New Domain Services
```
src/domain/services/concept_extraction_strategy.py
src/domain/services/multi_strategy_concept_extractor.py
src/domain/services/rule_based_extraction_strategy.py
src/domain/services/statistical_extraction_strategy.py
src/domain/services/embedding_extraction_strategy.py
```

### New Infrastructure Services
```
src/infrastructure/services/spacy_linguistic_processor.py
src/infrastructure/services/sklearn_statistical_processor.py
src/infrastructure/services/networkx_graph_processor.py
```

### Enhanced Files
```
src/infrastructure/services/pdf_extractor.py (enhanced)
src/application/use_cases/extract_paper_concepts_use_case.py (updated)
```

### Test Files
```
tests/unit/domain/services/test_multi_strategy_extractor.py
tests/unit/domain/services/test_rule_based_strategy.py
tests/unit/domain/services/test_statistical_strategy.py
tests/unit/domain/services/test_embedding_strategy.py
tests/integration/test_multi_strategy_extraction.py
tests/performance/test_extraction_scalability.py
```

## Next Task Dependencies
This task enables:
- **Task 03**: Hierarchical Clustering and Organization
- **Task 04**: Evidence Extraction and Linking
- **GUI Development**: Provides the core extraction engine

## Success Metrics
- Successfully extracts concepts using multiple complementary strategies
- Achieves higher concept coverage than any single strategy alone
- Maintains academic transparency and explainability standards
- Scales efficiently to large research paper collections
- Provides foundation for hierarchical concept organization

**Ready for Implementation**: This task builds directly on Task 01 and provides the core extraction capabilities needed for the interactive GUI system.
