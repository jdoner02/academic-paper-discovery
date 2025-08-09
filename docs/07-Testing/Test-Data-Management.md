# Test Data Management for Research Systems

> **Context**: Effective test data management is crucial for academic research systems where data quality, reproducibility, and domain accuracy directly impact research outcomes. This guide provides comprehensive strategies for managing test data across all testing levels.

## 🗄️ Test Data Architecture

### Data Classification Framework

Our test data strategy recognizes different categories of data with varying requirements for authenticity, privacy, and maintenance:

```python
"""
Test data classification for academic research systems.

This framework ensures appropriate data handling across different
testing scenarios while maintaining research validity and privacy.
"""

class TestDataCategory(Enum):
    """
    Educational classification of test data types.
    
    Each category has different requirements for authenticity,
    privacy protection, and maintenance strategies.
    """
    
    # Synthetic data designed for specific test scenarios
    SYNTHETIC = "synthetic"
    
    # Anonymized real data with identifying information removed
    ANONYMIZED_REAL = "anonymized_real"
    
    # Curated examples from public domain research
    PUBLIC_DOMAIN = "public_domain"
    
    # Generated data following realistic statistical distributions
    STATISTICALLY_REALISTIC = "statistically_realistic"
    
    # Minimal data for basic functionality testing
    MINIMAL_VALID = "minimal_valid"
    
    # Edge cases and boundary condition data
    EDGE_CASES = "edge_cases"

class TestDataRequirements:
    """
    Requirements framework for different testing contexts.
    
    Educational Value: Shows how to systematically think about
    test data requirements across different testing levels.
    """
    
    def __init__(self, 
                 authenticity_level: float,  # 0.0 = completely synthetic, 1.0 = real data
                 privacy_sensitivity: str,   # "public", "internal", "restricted"
                 volume_requirements: int,   # Number of records needed
                 domain_coverage: List[str], # Research domains to cover
                 update_frequency: str):     # "static", "periodic", "dynamic"
        
        self.authenticity_level = authenticity_level
        self.privacy_sensitivity = privacy_sensitivity
        self.volume_requirements = volume_requirements
        self.domain_coverage = domain_coverage
        self.update_frequency = update_frequency
    
    @classmethod
    def for_unit_tests(cls) -> "TestDataRequirements":
        """Requirements for fast, isolated unit tests."""
        return cls(
            authenticity_level=0.3,  # Can be quite synthetic
            privacy_sensitivity="public",
            volume_requirements=10,   # Small datasets
            domain_coverage=["medical", "computer_science"],
            update_frequency="static"
        )
    
    @classmethod
    def for_integration_tests(cls) -> "TestDataRequirements":
        """Requirements for cross-component integration tests."""
        return cls(
            authenticity_level=0.7,  # Should be realistic
            privacy_sensitivity="internal",
            volume_requirements=100,  # Medium datasets
            domain_coverage=["medical", "computer_science", "physics", "biology"],
            update_frequency="periodic"
        )
    
    @classmethod
    def for_e2e_tests(cls) -> "TestDataRequirements":
        """Requirements for end-to-end workflow tests."""
        return cls(
            authenticity_level=0.9,  # Must be very realistic
            privacy_sensitivity="internal",
            volume_requirements=1000, # Large datasets
            domain_coverage=["all_supported_domains"],
            update_frequency="dynamic"
        )
```

### Data Storage and Organization

```
tests/
├── fixtures/
│   ├── __init__.py
│   ├── data/
│   │   ├── research_papers/
│   │   │   ├── unit_test_papers.json          # Small, focused datasets
│   │   │   ├── integration_test_papers.json   # Medium, realistic datasets
│   │   │   ├── e2e_test_papers.json          # Large, comprehensive datasets
│   │   │   └── edge_case_papers.json         # Boundary conditions
│   │   ├── concepts/
│   │   │   ├── medical_concepts.json
│   │   │   ├── cs_concepts.json
│   │   │   └── concept_relationships.json
│   │   ├── embeddings/
│   │   │   ├── sample_embeddings.pkl
│   │   │   └── similarity_matrices.npy
│   │   └── configurations/
│   │       ├── test_search_configs.yaml
│   │       └── domain_specific_configs/
│   ├── builders/
│   │   ├── paper_builder.py              # Fluent builders for test data
│   │   ├── concept_builder.py
│   │   └── search_query_builder.py
│   ├── factories/
│   │   ├── research_paper_factory.py     # Factory methods for objects
│   │   ├── concept_factory.py
│   │   └── embedding_factory.py
│   └── generators/
│       ├── synthetic_paper_generator.py  # Algorithmic data generation
│       ├── concept_relationship_generator.py
│       └── realistic_dataset_generator.py
```

## 🏗️ Test Data Builders and Factories

### Fluent Builder Pattern Implementation

```python
from datetime import date, datetime
from typing import List, Optional
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.doi import DOI
from src.domain.value_objects.paper_id import PaperId

class ResearchPaperTestBuilder:
    """
    Fluent builder for creating research papers in tests.
    
    Educational Value: Demonstrates the Builder pattern for
    creating complex test objects with readable, chainable methods.
    This pattern makes tests more maintainable and expressive.
    
    Usage Example:
        paper = (ResearchPaperTestBuilder()
                .with_title("Heart Rate Variability in Athletes")
                .with_authors(["Smith, J.", "Johnson, A."])
                .with_publication_date(date(2023, 1, 15))
                .with_medical_domain()
                .with_high_citation_count()
                .build())
    """
    
    def __init__(self):
        """Initialize builder with sensible defaults."""
        self._id = PaperId.generate()
        self._title = "Default Test Paper Title"
        self._authors = ["Test Author"]
        self._publication_date = date(2023, 1, 1)
        self._doi = None
        self._abstract = "Default test abstract content."
        self._content = "Default test paper content."
        self._keywords = []
        self._citation_count = 0
        self._research_domain = "general"
        self._quality_indicators = {}
    
    def with_id(self, paper_id: PaperId) -> "ResearchPaperTestBuilder":
        """Set specific paper ID (useful for testing entity equality)."""
        self._id = paper_id
        return self
    
    def with_title(self, title: str) -> "ResearchPaperTestBuilder":
        """Set paper title."""
        self._title = title
        return self
    
    def with_authors(self, authors: List[str]) -> "ResearchPaperTestBuilder":
        """Set paper authors."""
        self._authors = authors
        return self
    
    def with_single_author(self, author: str) -> "ResearchPaperTestBuilder":
        """Convenience method for single author papers."""
        self._authors = [author]
        return self
    
    def with_publication_date(self, pub_date: date) -> "ResearchPaperTestBuilder":
        """Set publication date."""
        self._publication_date = pub_date
        return self
    
    def with_recent_publication(self, days_ago: int = 30) -> "ResearchPaperTestBuilder":
        """Set recent publication date (useful for recency testing)."""
        from datetime import timedelta
        self._publication_date = date.today() - timedelta(days=days_ago)
        return self
    
    def with_doi(self, doi_string: str) -> "ResearchPaperTestBuilder":
        """Set DOI for the paper."""
        self._doi = DOI(doi_string)
        return self
    
    def with_abstract(self, abstract: str) -> "ResearchPaperTestBuilder":
        """Set paper abstract."""
        self._abstract = abstract
        return self
    
    def with_content(self, content: str) -> "ResearchPaperTestBuilder":
        """Set full paper content."""
        self._content = content
        return self
    
    def with_keywords(self, keywords: List[str]) -> "ResearchPaperTestBuilder":
        """Set paper keywords."""
        self._keywords = keywords
        return self
    
    def with_citation_count(self, count: int) -> "ResearchPaperTestBuilder":
        """Set citation count."""
        self._citation_count = count
        return self
    
    def with_high_citation_count(self) -> "ResearchPaperTestBuilder":
        """Set high citation count (useful for quality testing)."""
        self._citation_count = 150
        return self
    
    def with_low_citation_count(self) -> "ResearchPaperTestBuilder":
        """Set low citation count."""
        self._citation_count = 2
        return self
    
    def with_medical_domain(self) -> "ResearchPaperTestBuilder":
        """Configure paper as medical research."""
        self._research_domain = "medical"
        self._keywords.extend(["medicine", "clinical research", "healthcare"])
        self._abstract = "This medical research study investigates clinical outcomes..."
        return self
    
    def with_computer_science_domain(self) -> "ResearchPaperTestBuilder":
        """Configure paper as computer science research."""
        self._research_domain = "computer_science"
        self._keywords.extend(["algorithms", "computational methods", "software"])
        self._abstract = "This computer science research presents novel algorithms..."
        return self
    
    def with_hrv_research_content(self) -> "ResearchPaperTestBuilder":
        """Configure paper with HRV-specific content."""
        self._title = "Heart Rate Variability Analysis in Clinical Settings"
        self._keywords.extend([
            "heart rate variability", "HRV", "autonomic nervous system",
            "cardiac health", "physiological monitoring"
        ])
        self._abstract = """
        This study presents a comprehensive analysis of heart rate variability (HRV)
        metrics in clinical populations. We examined RMSSD, pNN50, and frequency domain
        measures across 200 participants to establish baseline parameters for
        diagnostic applications.
        """
        self._content = """
        Heart rate variability (HRV) represents the variation in time intervals
        between consecutive heartbeats. This physiological phenomenon reflects
        the dynamic interplay between sympathetic and parasympathetic nervous
        system activities...
        
        Methods: We collected 5-minute ECG recordings from participants in
        controlled laboratory conditions. R-R intervals were extracted using
        validated algorithms and processed to calculate time domain metrics...
        """
        return self
    
    def with_edge_case_title(self) -> "ResearchPaperTestBuilder":
        """Configure paper with edge case title (empty, very long, special chars)."""
        self._title = "A" * 500  # Very long title
        return self
    
    def with_minimal_valid_data(self) -> "ResearchPaperTestBuilder":
        """Configure paper with minimal valid data (boundary testing)."""
        self._title = "A"  # Minimal title
        self._authors = ["X"]  # Minimal author
        self._abstract = "X"  # Minimal abstract
        return self
    
    def with_quality_indicators(self, **indicators) -> "ResearchPaperTestBuilder":
        """Set quality indicators for testing quality assessment."""
        self._quality_indicators.update(indicators)
        return self
    
    def with_high_quality_indicators(self) -> "ResearchPaperTestBuilder":
        """Set indicators for high-quality papers."""
        return self.with_quality_indicators(
            peer_reviewed=True,
            impact_factor=8.5,
            methodology_score=0.9,
            reproducibility_score=0.85
        )
    
    def build(self) -> ResearchPaper:
        """Build the final ResearchPaper instance."""
        paper = ResearchPaper(
            id=self._id,
            title=self._title,
            authors=self._authors,
            publication_date=self._publication_date,
            doi=self._doi,
            abstract=self._abstract,
            content=self._content,
            keywords=self._keywords,
            citation_count=self._citation_count
        )
        
        # Apply quality indicators if specified
        if self._quality_indicators:
            paper = paper.with_quality_indicators(self._quality_indicators)
        
        return paper
    
    def build_list(self, count: int) -> List[ResearchPaper]:
        """Build a list of papers with varying characteristics."""
        papers = []
        for i in range(count):
            # Create variations for more realistic test data
            builder = ResearchPaperTestBuilder()
            
            if i % 3 == 0:
                builder = builder.with_medical_domain()
            elif i % 3 == 1:
                builder = builder.with_computer_science_domain()
            
            if i % 4 == 0:
                builder = builder.with_high_citation_count()
            
            # Add unique elements
            paper = (builder
                    .with_title(f"{self._title} - Variation {i+1}")
                    .with_authors([f"Author {i+1}"])
                    .with_recent_publication(days_ago=i*10)
                    .build())
            
            papers.append(paper)
        
        return papers

# Usage examples in tests
class TestResearchPaperBuilder:
    """Example usage of the ResearchPaperTestBuilder."""
    
    def test_builder_creates_valid_paper(self):
        """Test basic builder functionality."""
        paper = (ResearchPaperTestBuilder()
                .with_title("Test Paper")
                .with_authors(["Test Author"])
                .build())
        
        assert paper.title == "Test Paper"
        assert paper.authors == ("Test Author",)
    
    def test_builder_creates_hrv_research_paper(self):
        """Test domain-specific builder methods."""
        paper = (ResearchPaperTestBuilder()
                .with_hrv_research_content()
                .with_high_citation_count()
                .build())
        
        assert "Heart Rate Variability" in paper.title
        assert "heart rate variability" in paper.keywords
        assert paper.citation_count > 100
    
    def test_builder_creates_paper_list(self):
        """Test bulk creation of test papers."""
        papers = (ResearchPaperTestBuilder()
                 .with_title("Base Paper")
                 .build_list(5))
        
        assert len(papers) == 5
        assert all("Base Paper" in paper.title for paper in papers)
        assert all(paper.id != papers[0].id for paper in papers[1:])  # Unique IDs
```

### Factory Pattern for Complex Objects

```python
class ConceptTestFactory:
    """
    Factory for creating concept test data with realistic relationships.
    
    Educational Value: Demonstrates Factory pattern for creating
    complex object graphs with proper relationships and dependencies.
    """
    
    @staticmethod
    def create_medical_concept_hierarchy() -> List[Concept]:
        """Create a realistic medical concept hierarchy for testing."""
        concepts = []
        
        # Root medical concepts
        cardiovascular = Concept(
            id=ConceptId.generate(),
            name="cardiovascular system",
            category="anatomical_system",
            confidence=0.95,
            description="The system responsible for circulating blood throughout the body"
        )
        concepts.append(cardiovascular)
        
        # Child concepts
        hrv = Concept(
            id=ConceptId.generate(),
            name="heart rate variability",
            category="physiological_measure",
            confidence=0.92,
            parent_concept=cardiovascular.id,
            description="Variation in time intervals between consecutive heartbeats"
        )
        concepts.append(hrv)
        
        # Grandchild concepts
        rmssd = Concept(
            id=ConceptId.generate(),
            name="RMSSD",
            category="hrv_metric",
            confidence=0.88,
            parent_concept=hrv.id,
            description="Root mean square of successive differences between heartbeats"
        )
        concepts.append(rmssd)
        
        pnn50 = Concept(
            id=ConceptId.generate(),
            name="pNN50",
            category="hrv_metric",
            confidence=0.86,
            parent_concept=hrv.id,
            description="Percentage of successive heartbeat intervals differing by >50ms"
        )
        concepts.append(pnn50)
        
        return concepts
    
    @staticmethod
    def create_interdisciplinary_concepts() -> List[Concept]:
        """Create concepts that span multiple research domains."""
        return [
            Concept(
                id=ConceptId.generate(),
                name="machine learning",
                category="computational_method",
                confidence=0.94,
                domains=["computer_science", "medicine", "physics"],
                description="Computational methods for pattern recognition and prediction"
            ),
            Concept(
                id=ConceptId.generate(),
                name="signal processing",
                category="analytical_technique",
                confidence=0.91,
                domains=["engineering", "medicine", "physics"],
                description="Methods for analyzing and manipulating signals"
            ),
            Concept(
                id=ConceptId.generate(),
                name="statistical analysis",
                category="analytical_method",
                confidence=0.89,
                domains=["statistics", "medicine", "psychology", "economics"],
                description="Mathematical methods for analyzing and interpreting data"
            )
        ]
    
    @staticmethod
    def create_concept_relationships(concepts: List[Concept]) -> List[ConceptRelationship]:
        """Create realistic relationships between concepts."""
        relationships = []
        
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts[i+1:], i+1):
                # Create relationships based on conceptual similarity
                if concept1.category == concept2.category:
                    relationship = ConceptRelationship(
                        from_concept=concept1.id,
                        to_concept=concept2.id,
                        relationship_type="related_to",
                        strength=0.7,
                        evidence_count=15
                    )
                    relationships.append(relationship)
                
                elif concept1.name in concept2.description.lower():
                    relationship = ConceptRelationship(
                        from_concept=concept1.id,
                        to_concept=concept2.id,
                        relationship_type="mentioned_in",
                        strength=0.6,
                        evidence_count=8
                    )
                    relationships.append(relationship)
        
        return relationships

class SearchQueryTestFactory:
    """Factory for creating various search query configurations."""
    
    @staticmethod
    def create_basic_medical_query() -> SearchQuery:
        """Create a basic medical research query."""
        return SearchQuery(
            terms=["heart rate variability", "clinical research"],
            domain_filters=["medical"],
            max_results=50,
            sort_criteria=SortCriteria.RELEVANCE_DESC
        )
    
    @staticmethod
    def create_complex_interdisciplinary_query() -> SearchQuery:
        """Create a complex query spanning multiple domains."""
        return SearchQuery(
            terms=["machine learning", "medical diagnosis", "neural networks"],
            domain_filters=["computer_science", "medical"],
            date_range=DateRange(
                start_date=date(2020, 1, 1),
                end_date=date(2023, 12, 31)
            ),
            max_results=100,
            sort_criteria=SortCriteria.CITATION_COUNT_DESC,
            extract_concepts=True,
            similarity_threshold=0.8
        )
    
    @staticmethod
    def create_edge_case_queries() -> List[SearchQuery]:
        """Create edge case queries for boundary testing."""
        return [
            # Minimal query
            SearchQuery(terms=["a"]),
            
            # Maximum complexity query
            SearchQuery(
                terms=["term"] * 50,  # Many terms
                domain_filters=["medical", "cs", "physics", "biology", "chemistry"],
                max_results=1000,  # Maximum results
                extract_concepts=True,
                similarity_threshold=0.99  # Very high threshold
            ),
            
            # Empty results query
            SearchQuery(
                terms=["nonexistent_research_term_xyz123"],
                domain_filters=["obscure_domain"]
            )
        ]
```

## 📊 Synthetic Data Generation

### Algorithmic Data Generation

```python
import random
import numpy as np
from faker import Faker
from typing import Generator, Dict, Any

class RealisticResearchDataGenerator:
    """
    Generates synthetic research data following realistic distributions.
    
    Educational Value: Shows how to create statistically realistic
    test data that maintains the characteristics of real research
    datasets while avoiding privacy concerns.
    """
    
    def __init__(self, seed: int = 42):
        """Initialize generator with reproducible random seed."""
        self.fake = Faker()
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)
        
        # Load realistic distributions from analysis of real data
        self._load_realistic_distributions()
    
    def _load_realistic_distributions(self):
        """Load statistical distributions based on real research data analysis."""
        # Title length distribution (based on analysis of real papers)
        self.title_length_mean = 85
        self.title_length_std = 25
        
        # Author count distribution
        self.author_count_weights = {1: 0.15, 2: 0.25, 3: 0.30, 4: 0.20, 5: 0.10}
        
        # Citation count follows power law distribution
        self.citation_alpha = 2.5  # Power law exponent
        
        # Publication date distribution (more recent papers)
        self.recent_publication_bias = 0.7  # 70% from last 5 years
        
        # Domain-specific keyword distributions
        self.domain_keywords = {
            "medical": [
                "clinical", "patients", "treatment", "diagnosis", "therapy",
                "cardiovascular", "cardiac", "heart", "blood", "health",
                "disease", "medicine", "hospital", "physician", "nursing"
            ],
            "computer_science": [
                "algorithm", "computational", "software", "programming",
                "artificial intelligence", "machine learning", "data mining",
                "neural networks", "optimization", "performance", "system"
            ],
            "physics": [
                "quantum", "particle", "energy", "wave", "electromagnetic",
                "theoretical", "experimental", "measurement", "model", "physics"
            ]
        }
    
    def generate_research_paper(self, 
                               domain: str = None,
                               quality_level: str = "medium") -> ResearchPaper:
        """
        Generate a single realistic research paper.
        
        Args:
            domain: Research domain ("medical", "computer_science", "physics")
            quality_level: "high", "medium", "low" affects citation count, etc.
        """
        # Select domain randomly if not specified
        if domain is None:
            domain = random.choice(["medical", "computer_science", "physics"])
        
        # Generate title with realistic length and domain-specific terms
        title = self._generate_realistic_title(domain)
        
        # Generate authors with realistic distribution
        authors = self._generate_realistic_authors()
        
        # Generate publication date with recent bias
        publication_date = self._generate_realistic_publication_date()
        
        # Generate abstract based on domain
        abstract = self._generate_realistic_abstract(domain, title)
        
        # Generate keywords
        keywords = self._generate_realistic_keywords(domain, title, abstract)
        
        # Generate citation count based on quality level and age
        citation_count = self._generate_realistic_citation_count(
            quality_level, publication_date
        )
        
        # Generate DOI
        doi = self._generate_realistic_doi()
        
        return ResearchPaper(
            id=PaperId.generate(),
            title=title,
            authors=authors,
            publication_date=publication_date,
            doi=doi,
            abstract=abstract,
            keywords=keywords,
            citation_count=citation_count
        )
    
    def generate_paper_collection(self, 
                                  count: int,
                                  domain_distribution: Dict[str, float] = None) -> List[ResearchPaper]:
        """
        Generate a collection of papers with realistic distributions.
        
        Args:
            count: Number of papers to generate
            domain_distribution: {"medical": 0.4, "cs": 0.4, "physics": 0.2}
        """
        if domain_distribution is None:
            domain_distribution = {
                "medical": 0.35,
                "computer_science": 0.35,
                "physics": 0.30
            }
        
        papers = []
        for _ in range(count):
            # Select domain based on distribution
            domain = np.random.choice(
                list(domain_distribution.keys()),
                p=list(domain_distribution.values())
            )
            
            # Select quality level with realistic distribution
            quality_level = np.random.choice(
                ["low", "medium", "high"],
                p=[0.3, 0.5, 0.2]  # Most papers are medium quality
            )
            
            paper = self.generate_research_paper(domain, quality_level)
            papers.append(paper)
        
        return papers
    
    def _generate_realistic_title(self, domain: str) -> str:
        """Generate title with realistic length and domain-specific content."""
        # Sample base title patterns
        patterns = [
            "A {method} Approach to {problem} in {context}",
            "{adjective} Analysis of {phenomenon} Using {technique}",
            "The Role of {factor} in {process}: A {study_type} Study",
            "{comparative} Evaluation of {methods} for {application}",
            "Novel {technique} for {application} in {domain_context}"
        ]
        
        pattern = random.choice(patterns)
        domain_keywords = self.domain_keywords[domain]
        
        # Fill in pattern with domain-appropriate terms
        title = pattern.format(
            method=random.choice(["Novel", "Comprehensive", "Systematic", "Advanced"]),
            problem=random.choice(domain_keywords[:5]),
            context=random.choice(domain_keywords[5:10]),
            adjective=random.choice(["Quantitative", "Qualitative", "Statistical", "Experimental"]),
            phenomenon=random.choice(domain_keywords),
            technique=random.choice(["Machine Learning", "Statistical Analysis", "Computational Modeling"]),
            study_type=random.choice(["Longitudinal", "Cross-sectional", "Retrospective"]),
            factor=random.choice(domain_keywords),
            process=random.choice(domain_keywords),
            comparative=random.choice(["Comparative", "Comprehensive", "Systematic"]),
            methods=random.choice(["Methods", "Techniques", "Approaches"]),
            application=random.choice(domain_keywords),
            domain_context=domain.replace("_", " ").title()
        )
        
        # Ensure realistic title length
        target_length = max(30, int(np.random.normal(self.title_length_mean, self.title_length_std)))
        if len(title) > target_length:
            title = title[:target_length-3] + "..."
        
        return title
    
    def _generate_realistic_authors(self) -> List[str]:
        """Generate realistic author list with proper formatting."""
        # Sample number of authors from realistic distribution
        author_count = np.random.choice(
            list(self.author_count_weights.keys()),
            p=list(self.author_count_weights.values())
        )
        
        authors = []
        for _ in range(author_count):
            # Generate realistic academic names
            last_name = self.fake.last_name()
            first_initial = self.fake.first_name()[0]
            middle_initial = random.choice([None, self.fake.first_name()[0]])
            
            if middle_initial:
                author = f"{last_name}, {first_initial}.{middle_initial}."
            else:
                author = f"{last_name}, {first_initial}."
            
            authors.append(author)
        
        return authors
    
    def _generate_realistic_publication_date(self) -> date:
        """Generate publication date with bias toward recent years."""
        current_year = date.today().year
        
        if random.random() < self.recent_publication_bias:
            # Recent papers (last 5 years)
            year = random.randint(current_year - 5, current_year)
        else:
            # Older papers
            year = random.randint(1990, current_year - 6)
        
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Safe day range for all months
        
        return date(year, month, day)
    
    def _generate_realistic_abstract(self, domain: str, title: str) -> str:
        """Generate domain-appropriate abstract content."""
        domain_templates = {
            "medical": [
                "This study investigates {topic} in {population}. We conducted a {study_type} analysis of {n} participants to examine {outcome}. Results show {finding} with statistical significance (p < 0.05). These findings have implications for {application}.",
                "Background: {background}. Methods: We analyzed {data} from {n} {subjects}. Results: Our analysis revealed {finding}. Conclusions: {conclusion}."
            ],
            "computer_science": [
                "We present a novel {method} for {problem}. Our approach improves upon existing methods by {improvement}. Experimental evaluation on {dataset} demonstrates {performance} improvement. The proposed method achieves {metric} of {value}.",
                "This paper introduces {algorithm} to address {challenge}. We validate our approach through {evaluation} and compare against {baselines}. Results show {improvement} in {metrics}."
            ],
            "physics": [
                "We report experimental observations of {phenomenon} under {conditions}. Measurements were performed using {equipment} with {precision} accuracy. Our results confirm theoretical predictions of {theory} and provide evidence for {discovery}.",
                "Theoretical analysis of {system} reveals {insight}. We develop a {model} that predicts {behavior}. Numerical simulations validate our theoretical framework and demonstrate {agreement}."
            ]
        }
        
        template = random.choice(domain_templates[domain])
        domain_keywords = self.domain_keywords[domain]
        
        # Fill template with appropriate terms
        abstract = template.format(
            topic=random.choice(domain_keywords),
            population=random.choice(["patients", "participants", "subjects"]),
            study_type=random.choice(["retrospective", "prospective", "cross-sectional"]),
            n=random.randint(50, 500),
            outcome=random.choice(domain_keywords),
            finding=f"significant {random.choice(['improvement', 'correlation', 'difference'])}",
            application=random.choice(["clinical practice", "patient care", "diagnostic applications"]),
            method=random.choice(["algorithm", "technique", "approach"]),
            problem=random.choice(domain_keywords),
            improvement=random.choice(["efficiency", "accuracy", "performance"]),
            dataset=random.choice(["benchmark datasets", "real-world data", "synthetic data"]),
            performance=f"{random.randint(10, 50)}%",
            subjects=random.choice(["participants", "patients", "subjects"]),
            phenomenon=random.choice(domain_keywords),
            conditions=random.choice(["controlled conditions", "laboratory settings", "field conditions"])
        )
        
        return abstract
    
    def _generate_realistic_keywords(self, domain: str, title: str, abstract: str) -> List[str]:
        """Generate realistic keywords based on domain and content."""
        domain_keywords = self.domain_keywords[domain]
        
        # Extract potential keywords from title and abstract
        content_words = set()
        for text in [title.lower(), abstract.lower()]:
            words = text.split()
            content_words.update(word.strip('.,()[]') for word in words if len(word) > 4)
        
        # Select 3-7 keywords combining domain keywords and content words
        keyword_count = random.randint(3, 7)
        
        # Choose some domain keywords
        domain_sample = random.sample(domain_keywords, min(3, len(domain_keywords)))
        
        # Choose some content-based keywords
        content_sample = random.sample(list(content_words), min(2, len(content_words)))
        
        keywords = domain_sample + content_sample
        return keywords[:keyword_count]
    
    def _generate_realistic_citation_count(self, quality_level: str, publication_date: date) -> int:
        """Generate realistic citation count based on quality and age."""
        # Age factor (older papers have more time to accumulate citations)
        age_years = (date.today() - publication_date).days / 365.25
        age_factor = min(1.0, age_years / 10.0)  # Full factor after 10 years
        
        # Quality multipliers
        quality_multipliers = {"low": 0.3, "medium": 1.0, "high": 3.0}
        quality_factor = quality_multipliers[quality_level]
        
        # Base citation count from power law distribution
        base_citations = np.random.pareto(self.citation_alpha) * 10
        
        # Apply factors
        realistic_citations = int(base_citations * age_factor * quality_factor)
        
        return max(0, realistic_citations)  # Ensure non-negative
    
    def _generate_realistic_doi(self) -> DOI:
        """Generate realistic DOI."""
        prefix = random.choice(["10.1000", "10.1038", "10.1126", "10.1016", "10.1109"])
        suffix = f"{random.randint(100000, 999999)}"
        return DOI(f"{prefix}/{suffix}")
```

## 🔄 Data Lifecycle Management

### Test Data Refresh and Maintenance

```python
class TestDataManager:
    """
    Manages the lifecycle of test data across different environments.
    
    Educational Value: Shows how to maintain test data quality
    over time while handling updates, migrations, and cleanup.
    """
    
    def __init__(self, data_directory: Path):
        self.data_directory = data_directory
        self.version_file = data_directory / "data_version.json"
        self.metadata_file = data_directory / "data_metadata.json"
    
    def refresh_test_data(self, force: bool = False) -> bool:
        """
        Refresh test data if needed based on staleness criteria.
        
        Returns True if data was refreshed, False if current data is still valid.
        """
        if not self._needs_refresh() and not force:
            return False
        
        print("Refreshing test data...")
        
        # Generate new synthetic data
        generator = RealisticResearchDataGenerator()
        
        # Refresh different categories of test data
        self._refresh_unit_test_data(generator)
        self._refresh_integration_test_data(generator)
        self._refresh_e2e_test_data(generator)
        
        # Update version and metadata
        self._update_data_version()
        self._update_metadata()
        
        print("Test data refresh completed.")
        return True
    
    def _needs_refresh(self) -> bool:
        """Determine if test data needs to be refreshed."""
        if not self.version_file.exists():
            return True
        
        with open(self.version_file) as f:
            version_info = json.load(f)
        
        last_refresh = datetime.fromisoformat(version_info["last_refresh"])
        days_since_refresh = (datetime.now() - last_refresh).days
        
        # Refresh if data is older than 30 days
        return days_since_refresh > 30
    
    def _refresh_unit_test_data(self, generator: RealisticResearchDataGenerator):
        """Refresh unit test datasets."""
        # Small, focused datasets for unit tests
        medical_papers = generator.generate_paper_collection(
            count=20,
            domain_distribution={"medical": 1.0}
        )
        
        cs_papers = generator.generate_paper_collection(
            count=20,
            domain_distribution={"computer_science": 1.0}
        )
        
        # Save to JSON files
        self._save_papers_to_json(medical_papers, "unit_test_medical_papers.json")
        self._save_papers_to_json(cs_papers, "unit_test_cs_papers.json")
    
    def _refresh_integration_test_data(self, generator: RealisticResearchDataGenerator):
        """Refresh integration test datasets."""
        # Medium-sized, diverse datasets for integration tests
        mixed_papers = generator.generate_paper_collection(
            count=100,
            domain_distribution={"medical": 0.4, "computer_science": 0.4, "physics": 0.2}
        )
        
        self._save_papers_to_json(mixed_papers, "integration_test_papers.json")
    
    def _refresh_e2e_test_data(self, generator: RealisticResearchDataGenerator):
        """Refresh end-to-end test datasets."""
        # Large, comprehensive datasets for E2E tests
        large_dataset = generator.generate_paper_collection(
            count=1000,
            domain_distribution={"medical": 0.35, "computer_science": 0.35, "physics": 0.30}
        )
        
        self._save_papers_to_json(large_dataset, "e2e_test_papers.json")
    
    def _save_papers_to_json(self, papers: List[ResearchPaper], filename: str):
        """Save papers to JSON file with proper serialization."""
        data_file = self.data_directory / "research_papers" / filename
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert papers to serializable format
        papers_data = [paper.to_dict() for paper in papers]
        
        with open(data_file, 'w') as f:
            json.dump(papers_data, f, indent=2, default=str)
    
    def validate_test_data_integrity(self) -> List[str]:
        """
        Validate the integrity of test data files.
        
        Returns list of validation errors (empty if all valid).
        """
        errors = []
        
        # Check required files exist
        required_files = [
            "research_papers/unit_test_medical_papers.json",
            "research_papers/integration_test_papers.json",
            "research_papers/e2e_test_papers.json"
        ]
        
        for file_path in required_files:
            full_path = self.data_directory / file_path
            if not full_path.exists():
                errors.append(f"Required test data file missing: {file_path}")
                continue
            
            # Validate file content
            try:
                with open(full_path) as f:
                    data = json.load(f)
                
                if not isinstance(data, list):
                    errors.append(f"Invalid format in {file_path}: expected list")
                    continue
                
                # Validate sample papers
                for i, paper_data in enumerate(data[:5]):  # Check first 5
                    validation_errors = self._validate_paper_data(paper_data, file_path, i)
                    errors.extend(validation_errors)
                    
            except json.JSONDecodeError as e:
                errors.append(f"JSON decode error in {file_path}: {e}")
            except Exception as e:
                errors.append(f"Error validating {file_path}: {e}")
        
        return errors
    
    def _validate_paper_data(self, paper_data: Dict[str, Any], file_path: str, index: int) -> List[str]:
        """Validate individual paper data structure."""
        errors = []
        
        required_fields = ["id", "title", "authors", "publication_date"]
        for field in required_fields:
            if field not in paper_data:
                errors.append(f"Missing required field '{field}' in {file_path}[{index}]")
        
        # Validate data types and constraints
        if "title" in paper_data and not isinstance(paper_data["title"], str):
            errors.append(f"Invalid title type in {file_path}[{index}]")
        
        if "authors" in paper_data and not isinstance(paper_data["authors"], list):
            errors.append(f"Invalid authors type in {file_path}[{index}]")
        
        if "citation_count" in paper_data and paper_data["citation_count"] < 0:
            errors.append(f"Negative citation count in {file_path}[{index}]")
        
        return errors
```

## 🎯 Test Environment Configuration

### Environment-Specific Data Configuration

```python
class TestEnvironmentConfig:
    """
    Configuration for different testing environments.
    
    Educational Value: Shows how to adapt test data strategy
    for different environments (local, CI, staging, production).
    """
    
    @staticmethod
    def get_config(environment: str) -> Dict[str, Any]:
        """Get environment-specific test data configuration."""
        
        configs = {
            "local": {
                "data_volume": "small",
                "refresh_frequency": "manual",
                "use_real_data": False,
                "privacy_level": "public",
                "performance_requirements": "relaxed"
            },
            
            "ci": {
                "data_volume": "minimal",
                "refresh_frequency": "never",  # Use cached data
                "use_real_data": False,
                "privacy_level": "public",
                "performance_requirements": "fast"
            },
            
            "staging": {
                "data_volume": "large",
                "refresh_frequency": "weekly",
                "use_real_data": "anonymized",
                "privacy_level": "internal",
                "performance_requirements": "realistic"
            },
            
            "performance": {
                "data_volume": "extra_large",
                "refresh_frequency": "monthly",
                "use_real_data": "anonymized",
                "privacy_level": "internal",
                "performance_requirements": "production_like"
            }
        }
        
        return configs.get(environment, configs["local"])
```

## 🔗 Related Concepts

- [[Testing-Strategy]]: Overall testing approach and architecture
- [[Unit-Testing-Patterns]]: Specific patterns for unit test data
- [[Integration-Testing]]: Cross-component testing data requirements
- [[Performance-Testing]]: Large-scale data for performance validation
- [[Test-Environment-Management]]: Managing different testing environments

## 🚀 Implementation Guidelines

### For Development Teams

1. **Prioritize Realistic Data**: Test data should mirror real-world research scenarios
2. **Maintain Data Quality**: Regular validation and refresh cycles
3. **Respect Privacy**: Never use real personal or sensitive data in tests
4. **Version Control Data**: Track test data changes like code changes
5. **Automate Generation**: Use automated tools for consistent, reproducible test data

### For Research Teams

1. **Validate Domain Accuracy**: Ensure test data reflects real research patterns
2. **Contribute Domain Knowledge**: Help developers understand realistic data characteristics
3. **Review Test Scenarios**: Validate that tests cover actual research workflows
4. **Provide Feedback**: Report when test data doesn't match real-world expectations

---

*This comprehensive test data management strategy ensures reliable, maintainable, and realistic test data that supports confident development and validation of the Academic Paper Discovery System.*

#test-data #data-management #testing #quality-assurance #research-validation
