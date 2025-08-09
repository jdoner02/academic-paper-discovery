# Paper Discovery Use Case - Primary Research Workflow

## 🎯 Overview

The `DiscoverPapersUseCase` is the primary application service that orchestrates the academic paper discovery workflow. It demonstrates Clean Architecture's application layer by coordinating domain objects, external services, and business rules to fulfill the core user need: finding relevant research papers.

## 🏗️ Use Case Architecture

### Application Layer Responsibilities

**What the Application Layer Does:**
- **Orchestrates** domain objects to fulfill business use cases
- **Coordinates** between different domain services and external dependencies
- **Handles** application-level concerns (transactions, security, validation)
- **Translates** between external interfaces and domain concepts
- **Manages** workflow and process coordination

**What the Application Layer Does NOT Do:**
- **Business Logic**: That belongs in the domain layer
- **Data Access**: That's handled by infrastructure implementations
- **User Interface**: That's managed by interface adapters
- **Framework Details**: Those are infrastructure concerns

## 📋 Use Case Definition

### Command Pattern Implementation

```python
# research-core/src/application/commands/discover_papers_command.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass(frozen=True)
class DiscoverPapersCommand:
    """
    Command for paper discovery use case.
    
    This command demonstrates:
    - Command pattern for decoupling request from execution
    - Immutable data transfer objects
    - Input validation at application boundary
    - Clear separation of concerns
    
    Educational Notes:
    - Commands represent user intentions, not implementation details
    - Immutable to prevent accidental modification during processing
    - Contains all information needed to execute the use case
    - Validation ensures command integrity before processing
    """
    
    # Core search parameters
    search_terms: List[str]
    domain_configuration: Optional[str] = None
    
    # Filtering parameters
    max_results: int = 50
    publication_date_start: Optional[datetime] = None
    publication_date_end: Optional[datetime] = None
    min_citation_count: int = 0
    
    # Output parameters
    include_abstracts: bool = True
    include_concepts: bool = False
    sort_by: str = "relevance"  # relevance, date, citations
    
    # User context
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate command parameters."""
        self._validate_search_terms()
        self._validate_max_results()
        self._validate_date_range()
        self._validate_sort_option()
    
    def _validate_search_terms(self):
        """Validate search terms are provided and meaningful."""
        if not self.search_terms:
            raise ValueError("Search terms are required")
        
        if not any(term.strip() for term in self.search_terms):
            raise ValueError("At least one non-empty search term required")
        
        # Remove empty terms and limit length
        cleaned_terms = [term.strip() for term in self.search_terms if term.strip()]
        if len(cleaned_terms) > 10:
            raise ValueError("Maximum 10 search terms allowed")
        
        # Replace with cleaned terms (immutable, so we validate original)
        if len(cleaned_terms) != len(self.search_terms):
            object.__setattr__(self, 'search_terms', cleaned_terms)
    
    def _validate_max_results(self):
        """Validate result count limits."""
        if self.max_results <= 0:
            raise ValueError("Max results must be positive")
        if self.max_results > 1000:
            raise ValueError("Max results cannot exceed 1000")
    
    def _validate_date_range(self):
        """Validate publication date range."""
        if (self.publication_date_start and self.publication_date_end and 
            self.publication_date_start > self.publication_date_end):
            raise ValueError("Start date must be before end date")
    
    def _validate_sort_option(self):
        """Validate sort option."""
        valid_sorts = ["relevance", "date", "citations", "title"]
        if self.sort_by not in valid_sorts:
            raise ValueError(f"Sort option must be one of: {valid_sorts}")
```

### Use Case Implementation

```python
# research-core/src/application/use_cases/discover_papers_use_case.py

from typing import List, Optional
import asyncio
from datetime import datetime
import logging

from ..commands.discover_papers_command import DiscoverPapersCommand
from ..responses.discover_papers_response import DiscoverPapersResponse
from ..ports.paper_repository_port import PaperRepositoryPort
from ..ports.search_service_port import SearchServicePort
from ..ports.config_repository_port import ConfigRepositoryPort
from ..ports.concept_extractor_port import ConceptExtractorPort
from ..ports.quality_scorer_port import QualityScorerPort
from ..ports.analytics_port import AnalyticsPort

from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.search_query import SearchQuery
from ...domain.value_objects.paper_collection import PaperCollection
from ...domain.services.paper_ranking_service import PaperRankingService
from ...domain.services.duplicate_detection_service import DuplicateDetectionService
from ...domain.exceptions.domain_exceptions import (
    ConfigurationNotFoundError,
    SearchServiceError,
    DuplicateDetectionError
)

logger = logging.getLogger(__name__)

class DiscoverPapersUseCase:
    """
    Primary use case for discovering academic papers.
    
    This use case demonstrates:
    - Clean Architecture application layer patterns
    - Dependency inversion with port interfaces
    - Comprehensive error handling and logging
    - Domain service coordination
    - Cross-cutting concern management
    
    Educational Notes:
    - Shows how to orchestrate multiple domain services
    - Demonstrates transaction management patterns
    - Illustrates proper error handling at application layer
    - Examples of logging and monitoring integration
    - Shows how to handle both sync and async operations
    
    Design Decisions:
    - Uses dependency injection for testability
    - Separates coordination logic from business logic
    - Handles both individual and batch paper processing
    - Provides comprehensive error recovery mechanisms
    """
    
    def __init__(
        self,
        paper_repository: PaperRepositoryPort,
        search_service: SearchServicePort,
        config_repository: ConfigRepositoryPort,
        concept_extractor: ConceptExtractorPort,
        quality_scorer: QualityScorerPort,
        analytics: AnalyticsPort,
        ranking_service: PaperRankingService,
        duplicate_detector: DuplicateDetectionService
    ):
        """
        Initialize use case with required dependencies.
        
        Args:
            paper_repository: Port for paper persistence
            search_service: Port for external paper search
            config_repository: Port for domain configuration access
            concept_extractor: Port for concept extraction services
            quality_scorer: Port for paper quality assessment
            analytics: Port for usage analytics and metrics
            ranking_service: Domain service for paper ranking
            duplicate_detector: Domain service for duplicate detection
        """
        self._paper_repository = paper_repository
        self._search_service = search_service
        self._config_repository = config_repository
        self._concept_extractor = concept_extractor
        self._quality_scorer = quality_scorer
        self._analytics = analytics
        self._ranking_service = ranking_service
        self._duplicate_detector = duplicate_detector
    
    async def execute(self, command: DiscoverPapersCommand) -> DiscoverPapersResponse:
        """
        Execute the paper discovery workflow.
        
        This method demonstrates the complete application layer workflow:
        1. Input validation and preprocessing
        2. Configuration retrieval and validation
        3. Domain object creation and orchestration
        4. External service coordination
        5. Business rule application
        6. Result processing and formatting
        7. Error handling and recovery
        8. Analytics and monitoring
        
        Args:
            command: Validated discovery command
            
        Returns:
            Response containing discovered papers and metadata
            
        Raises:
            ConfigurationNotFoundError: If domain configuration not found
            SearchServiceError: If external search services fail
            ValidationError: If command validation fails
        """
        logger.info(f"Starting paper discovery for terms: {command.search_terms}")
        start_time = datetime.utcnow()
        
        try:
            # 1. Load and validate domain configuration
            config = await self._load_domain_configuration(command)
            
            # 2. Create domain search query
            search_query = await self._create_search_query(command, config)
            
            # 3. Execute search across multiple sources
            raw_papers = await self._execute_multi_source_search(search_query)
            
            # 4. Apply duplicate detection and deduplication
            deduplicated_papers = await self._remove_duplicates(raw_papers)
            
            # 5. Enrich papers with additional data
            enriched_papers = await self._enrich_papers(deduplicated_papers, command)
            
            # 6. Apply domain-specific ranking and filtering
            ranked_papers = await self._rank_and_filter_papers(
                enriched_papers, search_query, config
            )
            
            # 7. Create paper collection domain object
            paper_collection = PaperCollection(
                papers=ranked_papers[:command.max_results],
                query=search_query,
                metadata={
                    'total_found': len(raw_papers),
                    'after_deduplication': len(deduplicated_papers),
                    'after_filtering': len(ranked_papers),
                    'search_duration_ms': self._calculate_duration_ms(start_time),
                    'configuration_used': config.name if config else None
                }
            )
            
            # 8. Store results for future reference
            await self._store_discovery_results(paper_collection, command)
            
            # 9. Record analytics
            await self._record_analytics(command, paper_collection, start_time)
            
            # 10. Create and return response
            response = DiscoverPapersResponse.from_domain(paper_collection)
            
            logger.info(
                f"Paper discovery completed: {len(response.papers)} papers found "
                f"in {response.metadata['search_duration_ms']}ms"
            )
            
            return response
            
        except Exception as e:
            # Comprehensive error handling with proper logging
            logger.error(f"Paper discovery failed: {e}", exc_info=True)
            await self._record_error_analytics(command, e, start_time)
            
            # Re-raise with additional context
            if isinstance(e, (ConfigurationNotFoundError, SearchServiceError)):
                raise
            else:
                raise SearchServiceError(f"Unexpected error during discovery: {e}") from e
    
    async def _load_domain_configuration(self, command: DiscoverPapersCommand):
        """
        Load and validate domain-specific configuration.
        
        Domain configurations define:
        - Search strategies and keywords
        - Ranking algorithms and weights
        - Filtering criteria and thresholds
        - Source priorities and preferences
        """
        if not command.domain_configuration:
            # Use default configuration
            return await self._config_repository.get_default_configuration()
        
        config = await self._config_repository.get_configuration(
            command.domain_configuration
        )
        
        if not config:
            raise ConfigurationNotFoundError(
                f"Configuration '{command.domain_configuration}' not found"
            )
        
        # Validate configuration completeness
        config.validate()
        
        logger.debug(f"Loaded configuration: {config.name}")
        return config
    
    async def _create_search_query(self, command: DiscoverPapersCommand, config) -> SearchQuery:
        """
        Create domain search query from command and configuration.
        
        This method demonstrates:
        - Translation between application and domain concepts
        - Configuration-driven behavior modification
        - Business rule application from domain layer
        """
        # Expand search terms using configuration
        expanded_terms = list(command.search_terms)
        if config and config.search_strategy:
            expanded_terms.extend(config.search_strategy.secondary_keywords)
        
        # Create domain search query
        search_query = SearchQuery.create(
            terms=expanded_terms,
            domain=command.domain_configuration,
            date_range_start=command.publication_date_start,
            date_range_end=command.publication_date_end,
            min_citation_count=command.min_citation_count,
            max_results=command.max_results * 2,  # Get more for filtering
            exclude_terms=config.search_strategy.exclude_terms if config else []
        )
        
        logger.debug(f"Created search query: {search_query}")
        return search_query
    
    async def _execute_multi_source_search(self, query: SearchQuery) -> List[ResearchPaper]:
        """
        Execute search across multiple academic sources in parallel.
        
        This method demonstrates:
        - Parallel processing for performance
        - Error handling for external service failures
        - Aggregation of results from multiple sources
        - Graceful degradation when sources are unavailable
        """
        # Define search sources with priorities
        search_tasks = [
            self._search_source("arxiv", query),
            self._search_source("pubmed", query),
            self._search_source("semantic_scholar", query),
            self._search_source("google_scholar", query)
        ]
        
        # Execute searches in parallel with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*search_tasks, return_exceptions=True),
                timeout=30.0  # 30 second timeout for all searches
            )
        except asyncio.TimeoutError:
            logger.warning("Search timeout - using partial results")
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Aggregate successful results
        all_papers = []
        successful_sources = 0
        
        for i, result in enumerate(results):
            source_name = ["arxiv", "pubmed", "semantic_scholar", "google_scholar"][i]
            
            if isinstance(result, Exception):
                logger.warning(f"Search failed for {source_name}: {result}")
                continue
            
            if isinstance(result, list):
                all_papers.extend(result)
                successful_sources += 1
                logger.debug(f"Found {len(result)} papers from {source_name}")
        
        # Ensure we have results from at least one source
        if successful_sources == 0:
            raise SearchServiceError("All search sources failed")
        
        logger.info(f"Found {len(all_papers)} papers from {successful_sources} sources")
        return all_papers
    
    async def _search_source(self, source_name: str, query: SearchQuery) -> List[ResearchPaper]:
        """Search a specific source with error handling."""
        try:
            return await self._search_service.search_source(source_name, query)
        except Exception as e:
            logger.warning(f"Search failed for {source_name}: {e}")
            return []  # Return empty list for graceful degradation
    
    async def _remove_duplicates(self, papers: List[ResearchPaper]) -> List[ResearchPaper]:
        """
        Remove duplicate papers using domain service.
        
        Demonstrates:
        - Domain service usage for complex business logic
        - Error handling for domain operations
        - Logging of business-relevant metrics
        """
        if not papers:
            return papers
        
        try:
            original_count = len(papers)
            deduplicated = await self._duplicate_detector.remove_duplicates(papers)
            duplicates_removed = original_count - len(deduplicated)
            
            if duplicates_removed > 0:
                logger.info(f"Removed {duplicates_removed} duplicate papers")
            
            return deduplicated
            
        except Exception as e:
            logger.error(f"Duplicate detection failed: {e}")
            # Fall back to original papers if deduplication fails
            return papers
    
    async def _enrich_papers(
        self, 
        papers: List[ResearchPaper], 
        command: DiscoverPapersCommand
    ) -> List[ResearchPaper]:
        """
        Enrich papers with additional data based on command requirements.
        
        Enrichment may include:
        - Concept extraction from abstracts
        - Quality score calculation
        - Citation network analysis
        - Author reputation scores
        """
        if not papers:
            return papers
        
        enriched_papers = []
        
        for paper in papers:
            try:
                # Extract concepts if requested
                if command.include_concepts and not paper.concepts:
                    paper.extract_concepts(self._concept_extractor)
                
                # Calculate quality score
                if not paper.quality_score:
                    paper.calculate_quality_score(self._quality_scorer)
                
                enriched_papers.append(paper)
                
            except Exception as e:
                logger.warning(f"Failed to enrich paper {paper.identifier}: {e}")
                # Include paper without enrichment
                enriched_papers.append(paper)
        
        logger.debug(f"Enriched {len(enriched_papers)} papers")
        return enriched_papers
    
    async def _rank_and_filter_papers(
        self,
        papers: List[ResearchPaper],
        query: SearchQuery,
        config
    ) -> List[ResearchPaper]:
        """
        Apply domain-specific ranking and filtering.
        
        This method demonstrates:
        - Domain service coordination
        - Configuration-driven business logic
        - Complex filtering and ranking operations
        """
        if not papers:
            return papers
        
        # Apply relevance filtering
        relevant_papers = [
            paper for paper in papers
            if paper.is_relevant_to(query)
        ]
        
        # Apply configuration-specific filtering
        if config and config.filtering_criteria:
            relevant_papers = [
                paper for paper in relevant_papers
                if config.filtering_criteria.matches(paper)
            ]
        
        # Apply domain-specific ranking
        ranked_papers = self._ranking_service.rank_papers(
            papers=relevant_papers,
            query=query,
            ranking_strategy=config.ranking_strategy if config else None
        )
        
        logger.debug(
            f"Filtered {len(papers)} -> {len(relevant_papers)} papers, "
            f"ranked by {config.ranking_strategy.name if config else 'default'}"
        )
        
        return ranked_papers
    
    async def _store_discovery_results(
        self,
        collection: PaperCollection,
        command: DiscoverPapersCommand
    ) -> None:
        """
        Store discovery results for future reference and caching.
        
        Demonstrates:
        - Asynchronous persistence operations
        - Error handling for storage failures
        - Graceful degradation when storage is unavailable
        """
        try:
            await self._paper_repository.save_collection(collection)
            logger.debug(f"Stored collection with {len(collection.papers)} papers")
        except Exception as e:
            logger.warning(f"Failed to store discovery results: {e}")
            # Don't fail the entire operation if storage fails
    
    async def _record_analytics(
        self,
        command: DiscoverPapersCommand,
        collection: PaperCollection,
        start_time: datetime
    ) -> None:
        """Record analytics for monitoring and optimization."""
        try:
            await self._analytics.record_search_event(
                user_id=command.user_id,
                session_id=command.session_id,
                search_terms=command.search_terms,
                domain=command.domain_configuration,
                results_count=len(collection.papers),
                duration_ms=self._calculate_duration_ms(start_time),
                success=True
            )
        except Exception as e:
            logger.warning(f"Failed to record analytics: {e}")
    
    async def _record_error_analytics(
        self,
        command: DiscoverPapersCommand,
        error: Exception,
        start_time: datetime
    ) -> None:
        """Record error analytics for debugging and monitoring."""
        try:
            await self._analytics.record_search_error(
                user_id=command.user_id,
                session_id=command.session_id,
                search_terms=command.search_terms,
                error_type=type(error).__name__,
                error_message=str(error),
                duration_ms=self._calculate_duration_ms(start_time)
            )
        except Exception as e:
            logger.warning(f"Failed to record error analytics: {e}")
    
    def _calculate_duration_ms(self, start_time: datetime) -> int:
        """Calculate duration in milliseconds."""
        return int((datetime.utcnow() - start_time).total_seconds() * 1000)
```

## 📊 Response Pattern

### Response Data Transfer Object

```python
# research-core/src/application/responses/discover_papers_response.py

from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.paper_collection import PaperCollection

@dataclass(frozen=True)
class DiscoverPapersResponse:
    """
    Response for paper discovery use case.
    
    This response demonstrates:
    - Clean separation between domain and application concerns
    - Immutable data transfer objects
    - Rich metadata for client applications
    - Proper error information handling
    
    Educational Notes:
    - Responses should be serializable for API transmission
    - Include metadata useful for pagination and caching
    - Provide enough information for rich user interfaces
    - Keep domain objects separate from API representations
    """
    
    papers: List[Dict[str, Any]]  # Serialized paper data
    total_found: int
    query_metadata: Dict[str, Any]
    search_metadata: Dict[str, Any]
    performance_metadata: Dict[str, Any]
    
    @classmethod
    def from_domain(cls, collection: PaperCollection) -> 'DiscoverPapersResponse':
        """
        Create response from domain paper collection.
        
        This method demonstrates:
        - Translation from domain objects to DTOs
        - Data formatting for external consumption
        - Metadata extraction and organization
        """
        return cls(
            papers=[cls._serialize_paper(paper) for paper in collection.papers],
            total_found=len(collection.papers),
            query_metadata={
                'terms': collection.query.terms,
                'domain': collection.query.domain,
                'date_range_start': collection.query.date_range_start,
                'date_range_end': collection.query.date_range_end,
                'filters_applied': collection.query.get_active_filters()
            },
            search_metadata={
                'sources_used': collection.metadata.get('sources_used', []),
                'duplicates_removed': collection.metadata.get('duplicates_removed', 0),
                'configuration_used': collection.metadata.get('configuration_used')
            },
            performance_metadata={
                'search_duration_ms': collection.metadata.get('search_duration_ms', 0),
                'total_processed': collection.metadata.get('total_found', 0),
                'after_filtering': collection.metadata.get('after_filtering', 0)
            }
        )
    
    @staticmethod
    def _serialize_paper(paper: ResearchPaper) -> Dict[str, Any]:
        """Serialize paper entity for external consumption."""
        return {
            'id': str(paper.id),
            'identifier': str(paper.identifier),
            'title': paper.title,
            'authors': [str(author) for author in paper.authors],
            'abstract': paper.abstract,
            'publication_date': paper.publication_date.isoformat(),
            'venue': paper.venue,
            'keywords': paper.keywords,
            'concepts': [str(concept) for concept in paper.concepts],
            'citation_count': paper.citation_count,
            'quality_score': paper.quality_score,
            'age_days': paper.age_in_days
        }
```

## 🧪 Testing Strategies

### Unit Testing

```python
# tests/unit/application/test_discover_papers_use_case.py

import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from application.use_cases.discover_papers_use_case import DiscoverPapersUseCase
from application.commands.discover_papers_command import DiscoverPapersCommand
from domain.entities.research_paper import ResearchPaper
from domain.value_objects.doi import DOI
from domain.value_objects.author import Author

class TestDiscoverPapersUseCase:
    """Test suite for paper discovery use case."""
    
    @pytest.fixture
    def use_case(self):
        """Create use case with mocked dependencies."""
        return DiscoverPapersUseCase(
            paper_repository=Mock(),
            search_service=Mock(),
            config_repository=Mock(),
            concept_extractor=Mock(),
            quality_scorer=Mock(),
            analytics=Mock(),
            ranking_service=Mock(),
            duplicate_detector=Mock()
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_valid_command_returns_papers(self, use_case):
        """Test successful paper discovery workflow."""
        # Arrange
        command = DiscoverPapersCommand(
            search_terms=["machine learning", "security"],
            domain_configuration="ai_security",
            max_results=10
        )
        
        # Mock domain configuration
        mock_config = Mock()
        mock_config.name = "ai_security"
        mock_config.search_strategy.secondary_keywords = ["artificial intelligence"]
        mock_config.search_strategy.exclude_terms = []
        use_case._config_repository.get_configuration = AsyncMock(return_value=mock_config)
        
        # Mock search results
        mock_papers = [
            self._create_mock_paper("10.1000/paper1", "ML Security Paper 1"),
            self._create_mock_paper("10.1000/paper2", "ML Security Paper 2")
        ]
        use_case._search_service.search_source = AsyncMock(return_value=mock_papers)
        
        # Mock duplicate detection
        use_case._duplicate_detector.remove_duplicates = AsyncMock(return_value=mock_papers)
        
        # Mock ranking
        use_case._ranking_service.rank_papers = Mock(return_value=mock_papers)
        
        # Mock storage
        use_case._paper_repository.save_collection = AsyncMock()
        use_case._analytics.record_search_event = AsyncMock()
        
        # Act
        response = await use_case.execute(command)
        
        # Assert
        assert len(response.papers) == 2
        assert response.total_found == 2
        assert response.query_metadata['domain'] == "ai_security"
        assert "machine learning" in response.query_metadata['terms']
        
        # Verify repository interactions
        use_case._config_repository.get_configuration.assert_called_once_with("ai_security")
        use_case._paper_repository.save_collection.assert_called_once()
        use_case._analytics.record_search_event.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_with_invalid_configuration_raises_error(self, use_case):
        """Test that invalid configuration raises appropriate error."""
        # Arrange
        command = DiscoverPapersCommand(
            search_terms=["test"],
            domain_configuration="nonexistent_config"
        )
        
        use_case._config_repository.get_configuration = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(ConfigurationNotFoundError):
            await use_case.execute(command)
    
    @pytest.mark.asyncio
    async def test_execute_handles_search_service_failure_gracefully(self, use_case):
        """Test graceful handling of search service failures."""
        # Arrange
        command = DiscoverPapersCommand(search_terms=["test"])
        
        use_case._config_repository.get_default_configuration = AsyncMock(return_value=Mock())
        use_case._search_service.search_source = AsyncMock(side_effect=Exception("Service down"))
        
        # Act & Assert
        with pytest.raises(SearchServiceError):
            await use_case.execute(command)
    
    def _create_mock_paper(self, doi: str, title: str) -> ResearchPaper:
        """Helper to create mock paper for testing."""
        return ResearchPaper(
            identifier=DOI(doi),
            title=title,
            authors=[Author("Test Author")],
            abstract="Test abstract for paper about machine learning security and related topics.",
            publication_date=datetime(2023, 1, 15)
        )

class TestDiscoverPapersCommand:
    """Test suite for discovery command validation."""
    
    def test_create_command_with_valid_data_succeeds(self):
        """Test creating command with valid data."""
        # Act
        command = DiscoverPapersCommand(
            search_terms=["machine learning", "security"],
            max_results=50
        )
        
        # Assert
        assert command.search_terms == ["machine learning", "security"]
        assert command.max_results == 50
    
    def test_create_command_with_empty_search_terms_raises_error(self):
        """Test that empty search terms raise validation error."""
        # Act & Assert
        with pytest.raises(ValueError, match="Search terms are required"):
            DiscoverPapersCommand(search_terms=[])
    
    def test_create_command_with_invalid_max_results_raises_error(self):
        """Test that invalid max results raise validation error."""
        # Act & Assert
        with pytest.raises(ValueError, match="Max results must be positive"):
            DiscoverPapersCommand(
                search_terms=["test"],
                max_results=0
            )
```

### Integration Testing

```python
# tests/integration/test_paper_discovery_workflow.py

import pytest
from datetime import datetime

from application.use_cases.discover_papers_use_case import DiscoverPapersUseCase
from application.commands.discover_papers_command import DiscoverPapersCommand
from infrastructure.dependency_injection import create_container

class TestPaperDiscoveryWorkflow:
    """Integration tests for complete paper discovery workflow."""
    
    @pytest.fixture
    async def container(self):
        """Create dependency injection container for testing."""
        return create_container(environment="test")
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_end_to_end_paper_discovery(self, container):
        """Test complete paper discovery workflow with real dependencies."""
        # Arrange
        use_case = container.get(DiscoverPapersUseCase)
        command = DiscoverPapersCommand(
            search_terms=["machine learning", "security"],
            domain_configuration="ai_security",
            max_results=5
        )
        
        # Act
        response = await use_case.execute(command)
        
        # Assert
        assert len(response.papers) > 0
        assert response.total_found > 0
        assert all('machine learning' in paper['title'].lower() or 
                  'machine learning' in paper['abstract'].lower() 
                  for paper in response.papers[:3])  # Check top 3 results
        
        # Verify metadata
        assert 'search_duration_ms' in response.performance_metadata
        assert response.performance_metadata['search_duration_ms'] > 0
        assert response.query_metadata['domain'] == "ai_security"
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_paper_discovery_with_date_filtering(self, container):
        """Test paper discovery with publication date filtering."""
        # Arrange
        use_case = container.get(DiscoverPapersUseCase)
        command = DiscoverPapersCommand(
            search_terms=["deep learning"],
            publication_date_start=datetime(2020, 1, 1),
            publication_date_end=datetime(2023, 12, 31),
            max_results=10
        )
        
        # Act
        response = await use_case.execute(command)
        
        # Assert
        assert len(response.papers) > 0
        
        # Verify all papers are within date range
        for paper in response.papers:
            pub_date = datetime.fromisoformat(paper['publication_date'].replace('Z', '+00:00'))
            assert datetime(2020, 1, 1) <= pub_date <= datetime(2023, 12, 31)
```

## 🔄 Error Handling Strategy

### Application-Level Exceptions

```python
# research-core/src/application/exceptions/application_exceptions.py

class ApplicationException(Exception):
    """Base exception for application layer errors."""
    pass

class UseCaseExecutionError(ApplicationException):
    """Raised when use case execution fails."""
    
    def __init__(self, use_case_name: str, message: str, original_error: Exception = None):
        self.use_case_name = use_case_name
        self.original_error = original_error
        super().__init__(f"{use_case_name}: {message}")

class InvalidCommandError(ApplicationException):
    """Raised when command validation fails."""
    pass

class ServiceUnavailableError(ApplicationException):
    """Raised when external services are unavailable."""
    pass
```

### Error Recovery Patterns

```python
# Error recovery and graceful degradation examples

async def _execute_multi_source_search_with_fallback(self, query: SearchQuery):
    """Execute search with fallback strategies."""
    primary_sources = ["arxiv", "semantic_scholar"]
    fallback_sources = ["pubmed", "google_scholar"]
    
    # Try primary sources first
    papers = await self._try_sources(primary_sources, query)
    
    if not papers:
        logger.warning("Primary sources failed, trying fallback sources")
        papers = await self._try_sources(fallback_sources, query)
    
    if not papers:
        # Last resort: try cached results
        papers = await self._get_cached_results(query)
    
    return papers or []  # Never return None
```

## 📊 Performance Considerations

### Asynchronous Processing

```python
# Performance optimization patterns

async def _process_papers_in_batches(self, papers: List[ResearchPaper], batch_size: int = 10):
    """Process papers in batches to optimize memory and performance."""
    results = []
    
    for i in range(0, len(papers), batch_size):
        batch = papers[i:i + batch_size]
        batch_results = await asyncio.gather(
            *[self._process_single_paper(paper) for paper in batch],
            return_exceptions=True
        )
        
        # Filter out exceptions and log errors
        for j, result in enumerate(batch_results):
            if isinstance(result, Exception):
                logger.warning(f"Failed to process paper {batch[j].identifier}: {result}")
            else:
                results.append(result)
    
    return results
```

### Caching Strategy

```python
# Caching for frequently accessed data

@cached(ttl=3600)  # Cache for 1 hour
async def _get_domain_configuration(self, domain_name: str):
    """Get domain configuration with caching."""
    return await self._config_repository.get_configuration(domain_name)

@cached(ttl=300)  # Cache for 5 minutes
async def _search_with_cache(self, query: SearchQuery):
    """Search with result caching for identical queries."""
    cache_key = query.get_cache_key()
    cached_result = await self._cache.get(cache_key)
    
    if cached_result:
        logger.debug(f"Cache hit for query: {query}")
        return cached_result
    
    result = await self._execute_search(query)
    await self._cache.set(cache_key, result, ttl=300)
    
    return result
```

## 🔗 Related Documentation

- **[[Research-Paper-Entity]]**: Core domain object being discovered
- **[[Search-Query-ValueObject]]**: Search parameters and validation
- **[[Configuration-Management-UseCase]]**: Domain configuration handling
- **[[External-API-Integration]]**: External service coordination
- **[[Repository-Implementation]]**: Data persistence strategies
- **[[Error-Handling-Patterns]]**: Application-level error management

## 🚀 Extension Points

### Future Enhancements

1. **ML-Powered Ranking**: Use machine learning models for personalized ranking
2. **Real-time Updates**: Stream new papers as they become available
3. **Collaborative Filtering**: Recommend papers based on user behavior
4. **Multi-language Support**: Search papers in multiple languages
5. **Visual Search**: Find papers using images or diagrams

### Configuration Points

1. **Search Strategies**: Pluggable search algorithms and ranking methods
2. **Source Priorities**: Configurable source weighting and selection
3. **Quality Thresholds**: Adjustable quality and relevance criteria
4. **Performance Tuning**: Configurable timeouts, batch sizes, and concurrency

---

*The DiscoverPapersUseCase serves as the primary orchestrator of the paper discovery workflow, demonstrating how Clean Architecture's application layer coordinates domain objects and external services to fulfill complex business requirements.*
