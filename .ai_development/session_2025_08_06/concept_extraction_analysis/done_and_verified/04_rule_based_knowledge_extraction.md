# AI Agent Instructions: Rule-Based and Knowledge-Based Concept Extraction

## Academic Context and Learning Objectives

**For Students**: Rule-based extraction represents the earliest approaches to computational linguistics, dating back to the 1950s. These methods use explicit patterns and linguistic rules that humans can easily understand and verify. In contrast to modern machine learning approaches, rule-based systems are completely transparent - you can trace exactly why a concept was extracted.

**Domain Knowledge**: This approach stems from **symbolic AI** - the classical paradigm where knowledge is represented explicitly through symbols and rules rather than learned patterns. Rule-based NLP builds on **formal grammar theory** and **computational linguistics**, using techniques like regular expressions, context-free grammars, and ontological knowledge bases.

## Original Document Section Analysis

```markdown
1. Rule-Based and Knowledge-Based Extraction

These approaches rely on human-defined patterns or existing knowledge bases/ontologies:

• Rule-Based (Symbolic) Methods: These use linguistic rules or patterns to identify concepts. A simple example is extracting all noun phrases (NPs) from the text, since most key concepts in academic papers are noun phrases (e.g., "convolutional neural network", "quantum entanglement"). Tools like spaCy or NLTK can do NP chunking out-of-the-box. More refined rule-based methods might apply domain-specific filters (e.g., ignore generic words like "approach", "system" as standalone concepts, or enforce that a concept phrase contains at least one technical adjective or acronym). Rule-based extraction is fast and transparent – one can literally list the patterns being used. However, its recall can be limited (it might miss unconventional phrasing) and precision may suffer without extensive tweaking (many NPs are not actually meaningful concepts on their own). It also does nothing to unify synonyms or variants; "neural network" vs "neural networks" vs "artificial neural network" would all appear separately unless we add normalization rules.

• Dictionary- or Ontology-Based: If we have a list of known relevant concepts (a dictionary or an ontology of terms), we can simply scan the text for occurrences of those terms. For example, if analyzing biomedical papers, one could use the UMLS thesaurus to tag occurrences of medical concepts. Or for computer science, use the CSO terms. This approach is high precision – when a match is found, we know exactly what it refers to – but can be low recall if the dictionary is incomplete or if authors use new terms not in it. It also inherits any bias of the source ontology. Nonetheless, as mentioned, the CSO Classifier successfully uses an ontology-driven approach to detect research topics in papers. They combine it with a syntactic expansion step (to catch synonyms or hyponyms of ontology terms) and a contextual similarity step (to verify the paper's text context matches the candidate topic). For our system, if a relevant ontology exists, we could incorporate it to either validate extracted concepts (e.g., flag if a found term is in the known list of domain concepts) or to provide structure (e.g., use ontology relations as edges in our concept hierarchy). However, academic research often ventures beyond established taxonomies; so while this can anchor well-known concepts, we'll still need to handle novel or domain-specific terms.

• Hearst Pattern-Based Hypernym Extraction: A specific form of rule-based method to build hierarchies is using lexical patterns (first introduced by Hearst, 1992) to find "is-a" relationships in text. For instance, sentences like "X is a Y" or "Y such as X and Z" can indicate Y is a broader category and X, Z are examples (subtypes). Applying these patterns to a corpus of papers could automatically yield a set of candidate parent-child concept relations. This is interpretable (the evidence for the relation is literally the sentence matched by the pattern) and has been used in ontology induction research. Its drawback is that not all concept relations are stated in such explicit ways in research papers – authors often assume the reader knows the hierarchy and may not write those defining sentences. Also, parsing has to be accurate to avoid false matches. Still, if available, we can use patterns as an extra source of hierarchical edges to corroborate our other clustering-based hierarchy.
```

## Implementation Requirements and Architecture Mapping

### Domain Layer Components Required

**Entities**:
- `RuleBasedExtractor` - Coordinates multiple rule-based extraction strategies
- `ConceptPattern` - Represents linguistic patterns for concept identification

**Value Objects**:
- `NounPhraseRule` - Encapsulates noun phrase extraction patterns
- `HearstPattern` - Represents hypernym relationship patterns ("X is a Y")
- `OntologyTerm` - Links concepts to external knowledge bases

### Application Layer Components Required

**Use Cases**:
- `ExtractConceptsWithRulesUseCase` - Orchestrates rule-based extraction pipeline
- `ValidateConceptsAgainstOntologyUseCase` - Cross-references with external knowledge

**Ports**:
- `OntologyRepositoryPort` - Interface for external knowledge bases
- `LinguisticPatternPort` - Interface for pattern matching services

### Infrastructure Layer Components Required

**Services**:
- `SpacyNounPhraseExtractor` - Implementation using spaCy NLP library
- `CSOOntologyRepository` - Computer Science Ontology integration
- `HearstPatternMatcher` - Regex-based hypernym pattern detection

## Critical Analysis and Technical Challenges

### Advantages for Academic Trust
1. **Complete Transparency**: Every extraction decision can be traced to explicit rules
2. **Reproducible Results**: Same input always produces same output
3. **Domain Expert Validation**: Rules can be reviewed and refined by subject matter experts
4. **No External Dependencies**: Works without internet access or proprietary APIs

### Technical Limitations to Address
1. **Synonym Detection**: "neural network" vs "artificial neural network" treated as separate
2. **Context Sensitivity**: "network" could mean computer networks vs neural networks
3. **Linguistic Variation**: Authors use different phrasings for same concepts
4. **Coverage Limitations**: New terminology not captured by predefined patterns

### Educational Notes for Cross-Disciplinary Students

**For Physics/Engineering Students**: Rule-based systems are analogous to control systems - you define explicit transfer functions rather than learning them from data. The precision is high but requires expert knowledge to design the rules.

**For Mathematics Students**: This approach uses **formal language theory** - patterns are essentially regular expressions or context-free grammars applied to natural language.

## Implementation Strategy and File Mapping

### Existing Files to Examine
```bash
# Check current rule-based implementations
src/domain/services/
src/infrastructure/services/
tests/unit/domain/services/
```

### Files to Create/Enhance

**Domain Services**:
```python
# src/domain/services/rule_based_extractor.py
class RuleBasedConceptExtractor:
    """
    Demonstrates symbolic AI approach to concept extraction.
    
    Educational Notes:
    - Shows explicit pattern matching vs black-box ML
    - Illustrates linguistic rule application
    - Demonstrates transparency in AI decision-making
    """
```

**Infrastructure Implementations**:
```python
# src/infrastructure/services/spacy_noun_phrase_extractor.py
class SpacyNounPhraseExtractor:
    """
    SpaCy-based noun phrase extraction for academic papers.
    
    Educational Notes:
    - Demonstrates dependency parsing in NLP
    - Shows part-of-speech tagging application
    - Illustrates named entity recognition techniques
    """
```

### Test Strategy
- **Unit Tests**: Verify pattern matching accuracy with known examples
- **Integration Tests**: Test against real paper abstracts
- **Property-Based Tests**: Ensure rules work across linguistic variations

## AI Agent Implementation Instructions

### Phase 1: Basic Rule Implementation (TDD Cycle)
1. **Red Phase**: Write tests for noun phrase extraction from sample academic text
2. **Green Phase**: Implement minimal SpaCy-based extractor
3. **Refactor Phase**: Add domain-specific filtering rules

### Phase 2: Ontology Integration (TDD Cycle) 
1. **Red Phase**: Write tests for CSO ontology term matching
2. **Green Phase**: Implement basic dictionary lookup
3. **Refactor Phase**: Add contextual validation

### Phase 3: Hearst Pattern Detection (TDD Cycle)
1. **Red Phase**: Write tests for "is-a" relationship extraction
2. **Green Phase**: Implement regex-based pattern matching
3. **Refactor Phase**: Add confidence scoring

### Validation Criteria
- ✅ Extract technical terms from academic abstracts
- ✅ Filter out generic non-concepts ("approach", "method")
- ✅ Detect hypernym relationships from definitional sentences
- ✅ Cross-reference against domain ontologies
- ✅ Maintain complete traceability of extraction decisions

### Integration with Existing Architecture
This component integrates with:
- **Domain Entities**: `Concept`, `ResearchPaper` for storing extracted concepts
- **Application Use Cases**: `ExtractPaperConceptsUseCase` as one extraction strategy
- **Infrastructure Services**: PDF text extraction for input processing

Remember: Rule-based extraction forms the **foundation layer** for our hybrid approach - it provides high-precision, explainable concept identification that can be validated by domain experts and serves as a baseline for more advanced techniques.
