# Concept Extraction Domain Service

> **Context**: Concept extraction is the intellectual heart of the Academic Paper Discovery System. This domain service transforms raw research papers into structured knowledge graphs, enabling semantic search and discovery of research relationships.

## 🎯 Purpose and Domain Significance

The `ConceptExtractionService` represents a **core domain service** that encapsulates the complex business logic of knowledge discovery from academic texts. Unlike entities or value objects, this service contains algorithmic knowledge that doesn't naturally fit within any single entity.

**Domain Role:**
- **Knowledge Discovery**: Extract meaningful concepts from research papers
- **Semantic Relationships**: Identify connections between concepts
- **Research Intelligence**: Enable advanced search beyond keyword matching
- **Academic Insights**: Support literature review and research gap analysis

## 🏗️ Domain Service Architecture

### Service Interface Design

```python
from abc import ABC, abstractmethod
from typing import List, Set, Dict, Optional
from domain.entities.research_paper import ResearchPaper
from domain.entities.concept import Concept
from domain.value_objects.concept_id import ConceptId

class ConceptExtractionService(ABC):
    """
    Abstract domain service for concept extraction.
    
    Educational Value: Demonstrates domain service pattern
    in Domain-Driven Design, separating complex business
    logic from entities while keeping it within the domain layer.
    
    This abstraction allows multiple extraction strategies
    while maintaining consistent domain interfaces.
    """
    
    @abstractmethod
    async def extract_concepts(self, 
                              paper: ResearchPaper) -> Set[Concept]:
        """
        Extract core concepts from a research paper.
        
        Args:
            paper: Research paper to analyze
            
        Returns:
            Set of extracted concepts with metadata
            
        Raises:
            ConceptExtractionError: If extraction fails
        """
        pass
    
    @abstractmethod
    async def extract_relationships(self, 
                                   concepts: Set[Concept]) -> List['ConceptRelationship']:
        """
        Identify relationships between extracted concepts.
        
        Args:
            concepts: Set of concepts to analyze for relationships
            
        Returns:
            List of identified concept relationships
        """
        pass
    
    @abstractmethod
    async def extract_hierarchies(self, 
                                 concepts: Set[Concept]) -> 'ConceptHierarchy':
        """
        Build hierarchical concept structure.
        
        Educational Value: Shows how domain services can
        orchestrate complex algorithms while maintaining
        clear business semantics.
        """
        pass
    
    @abstractmethod
    def assess_extraction_quality(self, 
                                 paper: ResearchPaper,
                                 extracted_concepts: Set[Concept]) -> 'QualityMetrics':
        """
        Assess the quality of concept extraction.
        
        Returns metrics for monitoring and improvement.
        """
        pass
```

### Multi-Strategy Implementation

```python
from enum import Enum
from dataclasses import dataclass

class ExtractionStrategy(Enum):
    """Available concept extraction strategies."""
    STATISTICAL_TFIDF = "statistical_tfidf"
    EMBEDDINGS_CLUSTERING = "embeddings_clustering"  
    RULE_BASED_NLP = "rule_based_nlp"
    HYBRID_ENSEMBLE = "hybrid_ensemble"

@dataclass
class ExtractionConfig:
    """Configuration for concept extraction strategies."""
    strategy: ExtractionStrategy
    confidence_threshold: float = 0.7
    max_concepts_per_paper: int = 50
    enable_relationship_detection: bool = True
    enable_hierarchy_building: bool = True

class MultiStrategyConceptExtractionService(ConceptExtractionService):
    """
    Concrete implementation supporting multiple extraction strategies.
    
    Educational Value: Demonstrates strategy pattern within
    domain services, allowing runtime algorithm selection
    while maintaining consistent domain interfaces.
    """
    
    def __init__(self, 
                 config: ExtractionConfig,
                 embedding_service: 'EmbeddingServicePort',
                 nlp_processor: 'NLPProcessorPort'):
        self._config = config
        self._embedding_service = embedding_service
        self._nlp_processor = nlp_processor
        self._strategies = self._build_strategy_map()
    
    def _build_strategy_map(self) -> Dict[ExtractionStrategy, 'ExtractionAlgorithm']:
        """Build map of available extraction algorithms."""
        return {
            ExtractionStrategy.STATISTICAL_TFIDF: StatisticalTFIDFExtractor(
                self._config
            ),
            ExtractionStrategy.EMBEDDINGS_CLUSTERING: EmbeddingsClusteringExtractor(
                self._embedding_service,
                self._config
            ),
            ExtractionStrategy.RULE_BASED_NLP: RuleBasedNLPExtractor(
                self._nlp_processor,
                self._config
            ),
            ExtractionStrategy.HYBRID_ENSEMBLE: HybridEnsembleExtractor(
                self._embedding_service,
                self._nlp_processor,
                self._config
            )
        }
    
    async def extract_concepts(self, 
                              paper: ResearchPaper) -> Set[Concept]:
        """
        Extract concepts using configured strategy.
        
        Educational Value: Shows how domain services orchestrate
        complex algorithms while providing clean abstractions
        to application layer use cases.
        """
        # Validate paper readiness for extraction
        if not self._is_paper_extractable(paper):
            raise ConceptExtractionError(
                f"Paper {paper.id} not suitable for concept extraction"
            )
        
        # Select and execute extraction strategy
        extractor = self._strategies[self._config.strategy]
        raw_concepts = await extractor.extract(paper)
        
        # Apply domain-specific filtering and validation
        validated_concepts = self._validate_concepts(raw_concepts, paper)
        
        # Enhance concepts with domain metadata
        enhanced_concepts = self._enhance_concepts(validated_concepts, paper)
        
        # Apply confidence filtering
        filtered_concepts = self._filter_by_confidence(
            enhanced_concepts, 
            self._config.confidence_threshold
        )
        
        # Limit result size
        final_concepts = self._limit_concepts(
            filtered_concepts,
            self._config.max_concepts_per_paper
        )
        
        return final_concepts
    
    def _is_paper_extractable(self, paper: ResearchPaper) -> bool:
        """
        Validate paper meets requirements for concept extraction.
        
        Educational Value: Shows defensive programming in
        domain services, ensuring preconditions are met.
        """
        # Check minimum content length
        if len(paper.content) < MIN_EXTRACTABLE_LENGTH:
            return False
        
        # Check content quality indicators
        if paper.content_quality_score < MIN_QUALITY_THRESHOLD:
            return False
        
        # Check language support
        if paper.language not in SUPPORTED_LANGUAGES:
            return False
        
        # Check for sufficient structured content
        if not self._has_sufficient_structure(paper):
            return False
        
        return True
    
    def _validate_concepts(self, 
                          concepts: Set[Concept], 
                          paper: ResearchPaper) -> Set[Concept]:
        """
        Apply domain-specific concept validation rules.
        
        Educational Value: Demonstrates how domain services
        enforce business rules and maintain data quality.
        """
        validated = set()
        
        for concept in concepts:
            # Validate concept meets domain standards
            if self._is_valid_academic_concept(concept):
                # Check relevance to paper domain
                if self._is_relevant_to_paper(concept, paper):
                    # Verify concept uniqueness
                    if not self._is_duplicate_concept(concept, validated):
                        validated.add(concept)
        
        return validated
    
    def _enhance_concepts(self, 
                         concepts: Set[Concept], 
                         paper: ResearchPaper) -> Set[Concept]:
        """
        Enhance concepts with domain-specific metadata.
        
        Educational Value: Shows how domain services can
        enrich data with business intelligence.
        """
        enhanced = set()
        
        for concept in concepts:
            # Add paper-specific context
            context_metadata = self._extract_context_metadata(concept, paper)
            
            # Add domain classification
            domain_classification = self._classify_domain(concept, paper)
            
            # Calculate importance score
            importance_score = self._calculate_importance(concept, paper)
            
            # Create enhanced concept
            enhanced_concept = concept.with_enhancements(
                context_metadata=context_metadata,
                domain_classification=domain_classification,
                importance_score=importance_score,
                source_paper_id=paper.id
            )
            
            enhanced.add(enhanced_concept)
        
        return enhanced
```

### Relationship Detection Algorithm

```python
    async def extract_relationships(self, 
                                   concepts: Set[Concept]) -> List['ConceptRelationship']:
        """
        Identify semantic relationships between concepts.
        
        Educational Value: Demonstrates complex domain logic
        for relationship discovery in academic knowledge graphs.
        """
        relationships = []
        concept_list = list(concepts)
        
        # Pairwise relationship analysis
        for i, concept_a in enumerate(concept_list):
            for concept_b in concept_list[i+1:]:
                relationship = await self._analyze_concept_pair(
                    concept_a, 
                    concept_b
                )
                
                if relationship is not None:
                    relationships.append(relationship)
        
        # Group relationships by type for validation
        grouped_relationships = self._group_relationships_by_type(relationships)
        
        # Apply domain-specific relationship validation
        validated_relationships = self._validate_relationships(
            grouped_relationships,
            concepts
        )
        
        return validated_relationships
    
    async def _analyze_concept_pair(self, 
                                   concept_a: Concept, 
                                   concept_b: Concept) -> Optional['ConceptRelationship']:
        """
        Analyze potential relationship between two concepts.
        
        Uses multiple signals: semantic similarity, co-occurrence,
        domain knowledge, and citation patterns.
        """
        # Calculate semantic similarity
        similarity_score = await self._calculate_semantic_similarity(
            concept_a, 
            concept_b
        )
        
        # Analyze co-occurrence patterns
        cooccurrence_score = self._calculate_cooccurrence(
            concept_a, 
            concept_b
        )
        
        # Apply domain-specific relationship rules
        domain_relationship = self._identify_domain_relationship(
            concept_a, 
            concept_b
        )
        
        # Combine signals to determine relationship
        relationship_type = self._determine_relationship_type(
            similarity_score,
            cooccurrence_score,
            domain_relationship
        )
        
        if relationship_type is None:
            return None
        
        # Calculate confidence based on signal strength
        confidence = self._calculate_relationship_confidence(
            similarity_score,
            cooccurrence_score,
            domain_relationship
        )
        
        return ConceptRelationship(
            source_concept=concept_a.id,
            target_concept=concept_b.id,
            relationship_type=relationship_type,
            confidence=confidence,
            evidence=self._collect_relationship_evidence(
                concept_a, 
                concept_b, 
                relationship_type
            )
        )
```

### Hierarchical Concept Organization

```python
    async def extract_hierarchies(self, 
                                 concepts: Set[Concept]) -> 'ConceptHierarchy':
        """
        Build hierarchical concept structure from flat concept set.
        
        Educational Value: Demonstrates complex domain algorithms
        for knowledge organization and taxonomy construction.
        """
        # Group concepts by domain and specificity
        concept_groups = self._group_concepts_by_domain(concepts)
        
        hierarchies = {}
        
        for domain, domain_concepts in concept_groups.items():
            # Build domain-specific hierarchy
            domain_hierarchy = await self._build_domain_hierarchy(
                domain, 
                domain_concepts
            )
            
            hierarchies[domain] = domain_hierarchy
        
        # Identify cross-domain relationships
        cross_domain_links = self._identify_cross_domain_links(hierarchies)
        
        # Build unified concept hierarchy
        unified_hierarchy = ConceptHierarchy(
            domain_hierarchies=hierarchies,
            cross_domain_links=cross_domain_links,
            metadata=self._generate_hierarchy_metadata(concepts)
        )
        
        return unified_hierarchy
    
    async def _build_domain_hierarchy(self, 
                                     domain: str, 
                                     concepts: Set[Concept]) -> 'DomainHierarchy':
        """
        Build hierarchy within a specific research domain.
        
        Uses concept specificity, semantic relationships,
        and domain knowledge to organize concepts hierarchically.
        """
        # Calculate concept specificity scores
        specificity_scores = await self._calculate_specificity_scores(
            concepts,
            domain
        )
        
        # Identify root concepts (most general)
        root_concepts = self._identify_root_concepts(
            concepts,
            specificity_scores
        )
        
        # Build tree structure from roots
        hierarchy_tree = self._build_hierarchy_tree(
            root_concepts,
            concepts,
            specificity_scores
        )
        
        # Validate hierarchy consistency
        validated_hierarchy = self._validate_hierarchy(hierarchy_tree)
        
        return DomainHierarchy(
            domain=domain,
            root_concepts=root_concepts,
            hierarchy_tree=validated_hierarchy,
            specificity_scores=specificity_scores
        )
```

## 🔍 Quality Assessment and Monitoring

### Extraction Quality Metrics

```python
    def assess_extraction_quality(self, 
                                 paper: ResearchPaper,
                                 extracted_concepts: Set[Concept]) -> 'QualityMetrics':
        """
        Comprehensive quality assessment of concept extraction.
        
        Educational Value: Shows how domain services can
        provide self-monitoring and quality assurance capabilities.
        """
        # Calculate coverage metrics
        coverage_metrics = self._calculate_coverage_metrics(
            paper, 
            extracted_concepts
        )
        
        # Assess concept quality
        concept_quality = self._assess_individual_concept_quality(
            extracted_concepts
        )
        
        # Evaluate relationship coherence
        relationship_coherence = self._evaluate_relationship_coherence(
            extracted_concepts
        )
        
        # Check domain consistency
        domain_consistency = self._check_domain_consistency(
            paper, 
            extracted_concepts
        )
        
        # Calculate overall quality score
        overall_quality = self._calculate_overall_quality(
            coverage_metrics,
            concept_quality,
            relationship_coherence,
            domain_consistency
        )
        
        return QualityMetrics(
            overall_score=overall_quality,
            coverage=coverage_metrics,
            concept_quality=concept_quality,
            relationship_coherence=relationship_coherence,
            domain_consistency=domain_consistency,
            extraction_timestamp=datetime.utcnow(),
            assessment_metadata=self._generate_assessment_metadata(paper)
        )
    
    def _calculate_coverage_metrics(self, 
                                   paper: ResearchPaper, 
                                   concepts: Set[Concept]) -> 'CoverageMetrics':
        """
        Calculate how well concepts cover the paper content.
        
        Measures comprehensiveness of concept extraction.
        """
        # Analyze concept distribution across paper sections
        section_coverage = self._analyze_section_coverage(paper, concepts)
        
        # Calculate keyword coverage
        keyword_coverage = self._calculate_keyword_coverage(paper, concepts)
        
        # Assess abstract vs full text coverage
        abstract_coverage = self._assess_abstract_coverage(paper, concepts)
        
        # Evaluate concept density
        concept_density = len(concepts) / len(paper.content.split())
        
        return CoverageMetrics(
            section_coverage=section_coverage,
            keyword_coverage=keyword_coverage,
            abstract_coverage=abstract_coverage,
            concept_density=concept_density,
            total_concepts_extracted=len(concepts)
        )
```

## 🎓 Educational Value and Design Patterns

### Domain Service Pattern

**Key Characteristics:**
1. **Domain Logic**: Contains complex business algorithms that don't fit in entities
2. **Stateless**: No persistent state, operates on provided parameters
3. **Interface-Based**: Abstracts implementation details from clients
4. **Testable**: Clear inputs/outputs enable comprehensive testing

**Educational Benefits:**
- Demonstrates proper separation of concerns in Domain-Driven Design
- Shows how to handle complex algorithms within domain layer
- Illustrates strategy pattern for algorithm selection
- Provides examples of quality monitoring and self-assessment

### SOLID Principles Application

1. **Single Responsibility**: Focused solely on concept extraction logic
2. **Open/Closed**: Extensible through strategy pattern without modification
3. **Liskov Substitution**: All implementations behave consistently
4. **Interface Segregation**: Clean separation of extraction concerns
5. **Dependency Inversion**: Depends on abstractions for external services

## 🔗 Related Concepts

- [[Research-Paper-Entity]]: Primary input for concept extraction
- [[Concept-Entity]]: Output domain objects representing extracted knowledge
- [[Embedding-Services]]: Infrastructure supporting semantic analysis
- [[Knowledge-Graph-Management]]: Consumer of extracted concepts and relationships
- [[Domain-Events]]: Events triggered by extraction completion

## 🚀 Usage Examples

### Basic Concept Extraction

```python
# Configure extraction service
extraction_config = ExtractionConfig(
    strategy=ExtractionStrategy.HYBRID_ENSEMBLE,
    confidence_threshold=0.8,
    max_concepts_per_paper=30
)

extraction_service = MultiStrategyConceptExtractionService(
    config=extraction_config,
    embedding_service=embedding_service,
    nlp_processor=nlp_processor
)

# Extract concepts from research paper
paper = research_paper_repository.get_by_id(paper_id)
concepts = await extraction_service.extract_concepts(paper)

# Extract relationships between concepts
relationships = await extraction_service.extract_relationships(concepts)

# Build concept hierarchy
hierarchy = await extraction_service.extract_hierarchies(concepts)
```

### Quality-Focused Extraction

```python
# Extract concepts with quality assessment
concepts = await extraction_service.extract_concepts(paper)
quality_metrics = extraction_service.assess_extraction_quality(paper, concepts)

# Only proceed if quality meets threshold
if quality_metrics.overall_score >= MINIMUM_QUALITY_THRESHOLD:
    # Store concepts and relationships
    concept_repository.store_concepts(concepts)
    relationship_repository.store_relationships(relationships)
else:
    # Log quality issue and potentially retry with different strategy
    logger.warning(f"Low quality extraction for paper {paper.id}: {quality_metrics}")
```

---

*The ConceptExtractionService demonstrates how domain services can encapsulate complex business algorithms while maintaining clean architecture principles and providing educational value through clear abstractions and comprehensive quality monitoring.*

#domain #service #concept-extraction #knowledge-graph #nlp #educational
