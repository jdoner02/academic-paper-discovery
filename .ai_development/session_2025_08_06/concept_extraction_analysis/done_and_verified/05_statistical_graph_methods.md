# AI Agent Instructions: Statistical and Graph-Based Concept Extraction Methods

## Academic Context and Learning Objectives

**For Students**: Statistical methods in NLP predate modern deep learning and form the mathematical foundation for understanding text as data. These approaches treat documents as collections of features (words, phrases) and apply mathematical transformations to identify important patterns.

**Domain Knowledge**: This draws from **information theory** (TF-IDF), **graph theory** (TextRank), and **statistical modeling** (LDA). Key concepts include **term frequency analysis**, **PageRank algorithms**, and **probabilistic topic modeling** - all fundamental to modern information retrieval.

## Original Document Section Analysis

```markdown
2. Statistical and Graph-Based Methods

These treat the text analytically, without heavy semantic modeling:

• Term Frequency / TF-IDF: Simply counting word or phrase frequencies in the corpus (and maybe weighting by inverse document frequency to downrank very common terms) can highlight which terms are significant in each document and across the domain. Many early keyword extraction methods rely on variants of this. TF-IDF can be effective for single-word terms or very domain-specific jargon that appears frequently. However, it tends to favor very frequent words (which might be too general like "algorithm" if many papers use it) and might miss important but infrequent concepts (e.g., a seminal concept mentioned in only one paper). Also, it doesn't inherently group synonyms (e.g., "CNN" vs "convolutional neural network" would appear as separate tokens). Despite these issues, it's often a good baseline to include – for example, one might ensure that any term that is extremely frequent in the corpus is included in the concept list (as it likely represents a core topic of the collection).

• Keyword Graph and TextRank: As referenced earlier, TextRank is an unsupervised algorithm that builds a graph of words connected by co-occurrence (within a window in the text), then runs a ranking algorithm to score nodes (words) by centrality. Usually it's applied to single documents to get keyphrases. An extension, TopicRank, clusters similar words/phrases first, then ranks clusters – this is useful to avoid redundancy and to represent a broader concept by multiple terms. Graph-based methods like this are appealing because they consider the contextual network of terms – a word that co-occurs with many other high-importance words will get a higher score. They are fully unsupervised and easily reproducible. For explainability, one can inspect the graph to see why a term was ranked highly (e.g. it's connected to many others). In practice for our use case, a graph method could be used to extract initial candidates from each paper (or from the whole corpus) by treating each paper's text as a small graph. It won't give a hierarchy, but it can enrich the pool of candidate concepts. We must be careful, though, because graph methods often yield common phrases that are somewhat generic (depending on window size and other parameters) – they might need filtering.

• Statistical Topic Modeling (LDA): Latent Dirichlet Allocation (LDA) is a generative model that discovers "topics" in a collection of documents, where each topic is a probability distribution over words. Running LDA on our corpus could yield topics that roughly correspond to subdomains or themes. For example, one topic might heavily weight words {network, neural, learning, deep, model}, which we can label as "deep neural networks", while another topic weights {theorem, proof, graph, conjecture} perhaps "theoretical computer science". Basic LDA yields a flat set of topics. There are hierarchical variants like hLDA that arrange topics in a tree by introducing a nested Chinese Restaurant Process prior. LDA's advantages: it's unsupervised and has a solid theoretical footing; it tends to produce coherent groups of terms, which can be interpreted by humans as concepts. It is also relatively explainable: each topic is defined by a small set of highly weighted terms, which can serve as a description. And it's reproducible if the random seed is fixed. However, LDA has some downsides for us: it treats topics as probability distributions rather than explicit phrases, so to get a concise concept label one often has to manually interpret the top words. Also, LDA assumes a generative model that may not fit well if our corpus is small or if papers are very heterogeneous. It might mix unrelated things or split a single real concept into multiple topics. Hyperparameter tuning (e.g. number of topics) is needed and not always obvious. Nonetheless, LDA could be used in combination with other methods – e.g. the set of top words from each topic can suggest concept groupings, or it could help determine a broad categorization of papers which we then refine with phrase extraction.
```

## Implementation Requirements and Architecture Mapping

### Domain Layer Components Required

**Value Objects**:
- `TfIdfScore` - Term frequency-inverse document frequency calculation
- `GraphNode` - Represents words/phrases in co-occurrence graph
- `TopicDistribution` - Probability distribution over words for LDA topics

**Services**:
- `StatisticalConceptExtractor` - Coordinates statistical extraction methods
- `GraphBasedExtractor` - Implements TextRank and TopicRank algorithms
- `TopicModelingService` - LDA-based concept discovery

### Application Layer Components Required

**Use Cases**:
- `ExtractConceptsWithStatisticsUseCase` - Statistical concept extraction pipeline
- `DiscoverTopicsWithLDAUseCase` - Topic modeling for concept discovery
- `RankConceptsWithGraphsUseCase` - Graph-based concept ranking

**Ports**:
- `TopicModelPort` - Interface for topic modeling algorithms
- `GraphAnalysisPort` - Interface for graph-based analysis

### Infrastructure Layer Components Required

**Services**:
- `SklearnTfIdfExtractor` - scikit-learn based TF-IDF implementation
- `NetworkxTextRankExtractor` - NetworkX graph-based TextRank
- `GensimLDAService` - Gensim library LDA implementation

## Mathematical Foundations and Algorithms

### TF-IDF Scoring
```
TF-IDF(t,d,D) = TF(t,d) × IDF(t,D)

where:
TF(t,d) = frequency of term t in document d
IDF(t,D) = log(|D| / |{d ∈ D : t ∈ d}|)
```

**Educational Note**: TF-IDF balances local importance (frequency in document) with global rarity (inverse document frequency). High scores indicate terms that are important to specific documents but not common across the entire corpus.

### TextRank Algorithm
```
TR(Vi) = (1-d) + d × Σ(TR(Vj) / |Out(Vj)|)

where:
Vi = node i in the graph
d = damping factor (typically 0.85)
Out(Vj) = outgoing edges from node j
```

**Educational Note**: TextRank applies Google's PageRank algorithm to text - words that co-occur with many other important words receive higher scores.

### LDA Generative Process
```
For each document d:
  1. Choose θd ~ Dirichlet(α)  // topic distribution
  2. For each word position n:
     a. Choose topic zn ~ Multinomial(θd)
     b. Choose word wn ~ Multinomial(βzn)
```

**Educational Note**: LDA assumes documents are mixtures of topics, and topics are mixtures of words. The model discovers these latent (hidden) topic structures through statistical inference.

## Critical Analysis and Technical Challenges

### Advantages for Research Applications
1. **Mathematical Rigor**: Well-understood statistical foundations
2. **Reproducible Results**: Deterministic algorithms with fixed parameters
3. **Scalability**: Efficient computation for large document collections
4. **Interpretability**: Clear mathematical explanations for rankings

### Technical Limitations to Address
1. **Synonym Problem**: "neural network" and "CNN" treated as different terms
2. **Context Insensitivity**: "network" could mean computer or neural networks
3. **Parameter Sensitivity**: Window sizes, topic counts need careful tuning
4. **Frequency Bias**: Rare but important concepts may be missed

### Educational Notes for Cross-Disciplinary Students

**For Mathematics Students**: These methods apply **linear algebra** (vector spaces, matrix decomposition) and **probability theory** (Bayesian inference, Dirichlet distributions) to linguistic data.

**For Physics Students**: Statistical mechanics concepts like **energy landscapes** and **phase transitions** have analogies in topic modeling convergence.

**For Engineering Students**: Signal processing techniques like **frequency analysis** and **filtering** apply directly to text analysis.

## Implementation Strategy and File Mapping

### Existing Files to Examine
```bash
# Check current statistical implementations
src/domain/services/
src/infrastructure/services/
tests/unit/domain/services/test_statistical_extractor.py
```

### Files to Create/Enhance

**Domain Services**:
```python
# src/domain/services/statistical_concept_extractor.py
class StatisticalConceptExtractor:
    """
    Demonstrates statistical approaches to concept extraction.
    
    Educational Notes:
    - Shows TF-IDF mathematical foundations
    - Illustrates graph theory application to NLP
    - Demonstrates probabilistic topic modeling
    
    Design Decisions:
    - TF-IDF: Balances term frequency with document frequency
    - TextRank: Uses co-occurrence graphs for term importance
    - LDA: Discovers latent topic structures in collections
    """
```

**Infrastructure Implementations**:
```python
# src/infrastructure/services/textrank_extractor.py
class TextRankConceptExtractor:
    """
    TextRank algorithm implementation for keyphrase extraction.
    
    Educational Notes:
    - Demonstrates PageRank adaptation for text analysis
    - Shows graph construction from linguistic data
    - Illustrates centrality measures in networks
    """
```

### Test Strategy
- **Unit Tests**: Verify mathematical calculations (TF-IDF scores, PageRank convergence)
- **Integration Tests**: Test against known academic corpora with ground truth
- **Property-Based Tests**: Ensure ranking stability across parameter variations
- **Performance Tests**: Validate scalability with large document collections

## AI Agent Implementation Instructions

### Phase 1: TF-IDF Foundation (TDD Cycle)
1. **Red Phase**: Write tests for TF-IDF calculation with sample documents
2. **Green Phase**: Implement basic term frequency and IDF calculations
3. **Refactor Phase**: Add phrase-level TF-IDF and filtering

### Phase 2: Graph-Based Ranking (TDD Cycle)
1. **Red Phase**: Write tests for TextRank on academic abstracts
2. **Green Phase**: Implement word co-occurrence graph construction
3. **Refactor Phase**: Add TopicRank clustering and phrase ranking

### Phase 3: Topic Modeling Integration (TDD Cycle)
1. **Red Phase**: Write tests for LDA topic discovery
2. **Green Phase**: Implement basic LDA with fixed hyperparameters
3. **Refactor Phase**: Add hierarchical LDA and topic coherence metrics

### Validation Criteria
- ✅ Extract high-frequency domain-specific terms with TF-IDF
- ✅ Rank concepts by centrality in co-occurrence networks
- ✅ Discover coherent topics that align with research themes
- ✅ Filter generic terms while preserving important concepts
- ✅ Provide mathematical explanations for all rankings

### Integration with Existing Architecture
This component integrates with:
- **Domain Entities**: `Concept` with confidence scores and statistical metrics
- **Application Use Cases**: Multi-strategy extraction combining statistical and rule-based
- **Infrastructure Services**: Text preprocessing and corpus management

### Performance Considerations
- **Memory Efficiency**: Use sparse matrices for large vocabularies
- **Computational Complexity**: O(V²) for TF-IDF, O(E×I) for TextRank convergence
- **Parallelization**: Document-level TF-IDF can be computed in parallel
- **Caching**: Store computed embeddings and graph structures for reuse

Remember: Statistical methods provide the **quantitative foundation** for concept importance - they answer "how important is this term mathematically?" while other methods answer "what does this term mean semantically?"
