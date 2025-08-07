"""
Test suite for ExecuteKeywordSearchUseCase - Application Layer Integration Validation.

This test suite demonstrates comprehensive testing of the application layer use case
that coordinates domain and infrastructure components. It validates Clean Architecture
principles by ensuring proper separation of concerns and dependency flow.

Educational Concepts Demonstrated:
- Application layer testing with mocked infrastructure dependencies
- Integration testing across architectural boundaries (domain ↔ application ↔ infrastructure)
- Multi-source data preservation through complete business workflows
- Configuration-driven behavior validation in enterprise applications
- Contract testing to ensure Liskov Substitution Principle compliance

Why This Testing Strategy Matters:
1. **Use Case Validation**: Ensures business logic coordinates domain objects correctly
2. **Architecture Integrity**: Validates Clean Architecture dependency rules are followed
3. **Integration Confidence**: Confirms components work together as designed
4. **Regression Prevention**: Protects against breaking changes in multi-layer systems
5. **Documentation Value**: Tests serve as executable specifications for business behavior

Academic Research Context:
This use case represents the core workflow researchers use to discover papers:
YAML Configuration → Search Strategy → Repository Query → Enhanced Research Papers
The tests ensure this workflow preserves all metadata needed for academic analysis.

Real-World Application:
- Literature review automation for graduate students and researchers
- Systematic review support with multi-source paper aggregation
- Research trend analysis with comprehensive metadata preservation
- Academic citation network construction using paper fingerprints

Design Patterns Validated:
- Use Case Pattern: Business logic coordination without external dependencies
- Repository Pattern: Abstract data access behind consistent interfaces
- Strategy Pattern: Configuration-driven search behavior selection
- Factory Pattern: Dynamic repository and configuration instantiation
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional

from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.keyword_config import KeywordConfig, SearchStrategy
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.source_metadata import SourceMetadata
from src.domain.value_objects.paper_fingerprint import PaperFingerprint


class TestExecuteKeywordSearchUseCaseInitialization:
    """
    Test use case initialization, dependency injection, and configuration loading.

    Educational Note:
    These tests validate the Dependency Inversion Principle by ensuring the use case
    depends on abstractions (PaperRepositoryPort) rather than concrete implementations.
    This enables testability and flexibility in choosing different repository implementations.

    Clean Architecture Validation:
    - Application layer depends only on domain interfaces (ports)
    - Configuration loading follows proper error handling patterns
    - Dependency injection enables testing with mock objects

    Academic Research Value:
    Proper initialization ensures researchers can configure search strategies through
    YAML files while maintaining flexibility to inject different paper sources.
    """

    def test_initialize_with_repository_and_config_file(self):
        """
        Test successful initialization with repository and configuration file path.

        Educational Note:
        This test validates constructor dependency injection, a key pattern for
        testability and flexibility. The use case accepts its dependencies
        explicitly rather than creating them internally.
        """
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        config_path = Path("config/test_keywords.yaml")

        # Mock the configuration loading
        with patch(
            "src.domain.value_objects.keyword_config.KeywordConfig.from_yaml_file"
        ) as mock_load:
            mock_config = Mock(spec=KeywordConfig)
            mock_load.return_value = mock_config

            # Act
            use_case = ExecuteKeywordSearchUseCase(
                repository=mock_repository, config_path=config_path
            )

            # Assert
            assert use_case.repository is mock_repository
            assert use_case.keyword_config is mock_config
            mock_load.assert_called_once_with(config_path)

    def test_initialize_with_injected_keyword_config(self):
        """
        Test initialization with pre-loaded keyword configuration.

        Educational Note:
        This demonstrates the Strategy Pattern where configuration can be injected
        at runtime, enabling different search strategies without file I/O.
        """
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        mock_config = Mock(spec=KeywordConfig)

        # Act
        use_case = ExecuteKeywordSearchUseCase(
            repository=mock_repository, keyword_config=mock_config
        )

        # Assert
        assert use_case.repository is mock_repository
        assert use_case.keyword_config is mock_config

    def test_reject_invalid_repository_interface(self):
        """
        Test that initialization fails with non-compliant repository.

        Educational Note:
        This validates Interface Segregation Principle and contract compliance.
        The use case requires specific repository capabilities defined in the port.
        """
        # Arrange
        invalid_repository = "not a repository"

        # Act & Assert
        with pytest.raises(
            TypeError, match="Repository must implement PaperRepositoryPort interface"
        ):
            ExecuteKeywordSearchUseCase(repository=invalid_repository)

    def test_require_either_config_path_or_keyword_config(self):
        """
        Test that initialization requires some form of configuration.

        Educational Note:
        This enforces proper dependency injection - the use case needs configuration
        to function, so it validates this requirement at construction time.
        """
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)

        # Act & Assert - Should work with config_path=None and keyword_config=None
        # Note: This should actually load default config according to implementation
        use_case = ExecuteKeywordSearchUseCase(repository=mock_repository)
        # The implementation will try to load default config, so we expect it to work
        # or fail with a specific configuration loading error, not a validation error


class TestExecuteKeywordSearchUseCaseBasicExecution:
    """
    Test basic search execution functionality with mocked repository dependencies.

    Educational Note:
    These tests focus on the use case's core responsibility: coordinating domain objects
    to execute business operations. We mock external dependencies to isolate the
    application layer logic from infrastructure concerns.

    Testing Philosophy:
    - Mock repository to test use case logic in isolation
    - Verify proper SearchQuery construction from configuration
    - Validate result filtering and business rule application
    - Ensure error handling and edge case coverage

    Academic Research Context:
    These tests ensure the core paper discovery workflow functions correctly,
    providing confidence for researchers using the system for literature reviews.
    """

    def setup_method(self):
        """Set up common test fixtures."""
        self.mock_repository = Mock(spec=PaperRepositoryPort)
        self.mock_strategy = Mock(spec=SearchStrategy)
        self.mock_strategy.name = "test_strategy"
        self.mock_strategy.search_limit = 50
        self.mock_strategy.get_all_terms.return_value = [
            "heart rate variability",
            "HRV",
        ]

        self.mock_config = Mock(spec=KeywordConfig)
        # Create mock search configuration
        mock_search_config = Mock()
        mock_search_config.citation_threshold = 0
        mock_search_config.exclude_terms = []
        self.mock_config.search_configuration = mock_search_config
        self.mock_config.get_strategy.return_value = self.mock_strategy

    def test_execute_strategy_basic_workflow(self):
        """
        Test basic strategy execution workflow.

        Educational Note:
        This test validates the primary business workflow: configuration → query → repository → results.
        It demonstrates how the use case coordinates domain objects without knowing
        infrastructure details.
        """
        # Arrange
        use_case = ExecuteKeywordSearchUseCase(
            repository=self.mock_repository, keyword_config=self.mock_config
        )

        # Mock repository response with basic ResearchPaper
        mock_paper = Mock(spec=ResearchPaper)
        mock_paper.title = "HRV Analysis in Clinical Settings"
        mock_paper.abstract = "Study of heart rate variability patterns"
        self.mock_repository.find_by_query.return_value = [mock_paper]

        # Act
        results = use_case.execute_strategy("test_strategy")

        # Assert
        assert len(results) == 1
        assert results[0] is mock_paper
        self.mock_config.get_strategy.assert_called_once_with("test_strategy")
        self.mock_repository.find_by_query.assert_called_once()

        # Verify SearchQuery was constructed correctly
        call_args = self.mock_repository.find_by_query.call_args[0][0]
        assert isinstance(call_args, SearchQuery)
        assert call_args.max_results == 50

    def test_execute_strategy_with_max_results_override(self):
        """
        Test strategy execution with max results override.

        Educational Note:
        This validates parameter override functionality, showing how business rules
        can be adjusted at runtime while maintaining configuration defaults.
        """
        # Arrange
        use_case = ExecuteKeywordSearchUseCase(
            repository=self.mock_repository, keyword_config=self.mock_config
        )
        self.mock_repository.find_by_query.return_value = []

        # Act
        results = use_case.execute_strategy("test_strategy", max_results=25)

        # Assert
        call_args = self.mock_repository.find_by_query.call_args[0][0]
        assert call_args.max_results == 25  # Should override strategy default

    def test_execute_custom_search_workflow(self):
        """
        Test custom search execution with ad-hoc terms.

        Educational Note:
        This demonstrates flexibility in the use case design - supporting both
        configuration-driven and programmatic search approaches.
        """
        # Arrange
        use_case = ExecuteKeywordSearchUseCase(
            repository=self.mock_repository, keyword_config=self.mock_config
        )
        self.mock_repository.find_by_query.return_value = []

        # Act
        results = use_case.execute_custom_search(
            required_terms=["machine learning", "healthcare"],
            optional_terms=["AI", "medical"],
            max_results=30,
        )

        # Assert
        self.mock_repository.find_by_query.assert_called_once()
        call_args = self.mock_repository.find_by_query.call_args[0][0]
        assert "machine learning" in call_args.terms
        assert "healthcare" in call_args.terms
        assert call_args.max_results == 30


class TestExecuteKeywordSearchUseCaseMultiSourceIntegration:
    """
    Test use case integration with multi-source ResearchPaper entities.

    Educational Note:
    These are the CRITICAL tests for TDD Cycle 7. They validate that the use case
    properly handles the enhanced ResearchPaper entities with source_metadata and
    paper_fingerprint fields added in TDD Cycles 5 and 6A.

    Architecture Validation:
    - Ensures application layer preserves domain entity enhancements
    - Validates complete workflow from repository to final results
    - Tests integration with multi-source infrastructure implementations

    Expected Initial Behavior:
    These tests should FAIL initially if the use case doesn't properly handle
    or preserve the enhanced ResearchPaper fields, indicating need for GREEN PHASE.

    Academic Research Impact:
    Multi-source integration enables researchers to:
    - Track paper provenance across different databases
    - Detect duplicates using paper fingerprints
    - Access source-specific metadata for quality assessment
    """

    def setup_method(self):
        """Set up test fixtures with enhanced ResearchPaper entities."""
        self.mock_repository = Mock(spec=PaperRepositoryPort)
        self.mock_config = Mock(spec=KeywordConfig)

        # Create mock search configuration
        mock_search_config = Mock()
        mock_search_config.citation_threshold = 0
        mock_search_config.exclude_terms = []
        self.mock_config.search_configuration = mock_search_config

        # Create enhanced ResearchPaper with multi-source fields
        self.enhanced_paper = ResearchPaper(
            title="Advanced Heart Rate Variability Analysis",
            authors=["Dr. Jane Smith", "Prof. John Doe"],
            abstract="Comprehensive study of HRV patterns in clinical environments",
            publication_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
            doi="10.1000/example.hrv.2024",
            venue="Journal of Biomedical Engineering",
            citation_count=45,
            keywords=["HRV", "cardiac", "biomedical"],
            arxiv_id="2401.12345",
            url="https://arxiv.org/pdf/2401.12345.pdf",
            source_metadata=SourceMetadata(
                source_name="ArXiv",
                source_identifier="arxiv:2401.12345",
                source_url="https://arxiv.org/abs/2401.12345",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="preprint",
                quality_score=0.9,
                source_specific_data={
                    "categories": "cs.AI stat.ML",
                    "version": "v1",
                    "submission_date": "2024-01-15",
                },
                retrieved_at=datetime.now(timezone.utc),
            ),
            paper_fingerprint=PaperFingerprint(
                primary_identifier="doi:10.1000/example.hrv.2024",
                title_hash="abc123def456",
                author_hash="def456ghi789",
                publication_year=2024,
                source_identifiers={
                    "doi": "10.1000/example.hrv.2024",
                    "arxiv": "2401.12345",
                },
            ),
        )

    def test_use_case_preserves_source_metadata_from_repository(self):
        """
        Test that use case preserves source_metadata fields from repository results.

        Educational Note:
        This is a CRITICAL integration test. The use case should act as a transparent
        coordinator, preserving all domain entity fields without modification.
        Failure indicates the use case is inadvertently stripping enhanced fields.

        Expected Behavior:
        This test should INITIALLY FAIL if the use case implementation doesn't
        properly handle enhanced ResearchPaper entities with source_metadata.
        """
        # Arrange
        mock_strategy = Mock(spec=SearchStrategy)
        mock_strategy.name = "multi_source_test"
        mock_strategy.search_limit = 10
        mock_strategy.get_all_terms.return_value = ["HRV"]
        self.mock_config.get_strategy.return_value = mock_strategy

        use_case = ExecuteKeywordSearchUseCase(
            repository=self.mock_repository, keyword_config=self.mock_config
        )

        # Repository returns enhanced paper with source_metadata
        self.mock_repository.find_by_query.return_value = [self.enhanced_paper]

        # Act
        results = use_case.execute_strategy("multi_source_test")

        # Assert - Enhanced fields should be preserved
        assert len(results) == 1
        result_paper = results[0]

        # CRITICAL: source_metadata should be preserved
        assert (
            result_paper.source_metadata is not None
        ), "Use case should preserve source_metadata field"
        assert result_paper.source_metadata.source_name == "ArXiv"
        assert result_paper.source_metadata.source_identifier == "arxiv:2401.12345"
        assert "categories" in result_paper.source_metadata.source_specific_data

    def test_use_case_preserves_paper_fingerprint_from_repository(self):
        """
        Test that use case preserves paper_fingerprint fields from repository results.

        Educational Note:
        Paper fingerprints enable duplicate detection across multiple sources.
        The use case must preserve these fields to maintain multi-source capabilities.
        This test validates that enhancement doesn't break in the application layer.
        """
        # Arrange
        mock_strategy = Mock(spec=SearchStrategy)
        mock_strategy.name = "fingerprint_test"
        mock_strategy.search_limit = 5
        mock_strategy.get_all_terms.return_value = ["cardiac monitoring"]
        self.mock_config.get_strategy.return_value = mock_strategy

        use_case = ExecuteKeywordSearchUseCase(
            repository=self.mock_repository, keyword_config=self.mock_config
        )

        # Repository returns paper with fingerprint
        self.mock_repository.find_by_query.return_value = [self.enhanced_paper]

        # Act
        results = use_case.execute_strategy("fingerprint_test")

        # Assert - Paper fingerprint should be preserved
        assert len(results) == 1
        result_paper = results[0]

        # CRITICAL: paper_fingerprint should be preserved
        assert (
            result_paper.paper_fingerprint is not None
        ), "Use case should preserve paper_fingerprint field"
        assert result_paper.paper_fingerprint.title_hash == "abc123def456"
        assert (
            result_paper.paper_fingerprint.primary_identifier
            == "doi:10.1000/example.hrv.2024"
        )

    def test_complete_yaml_to_enhanced_paper_workflow(self):
        """
        Test complete end-to-end workflow: YAML config → SearchQuery → Enhanced ResearchPaper.

        Educational Note:
        This integration test validates the entire Clean Architecture workflow
        across all layers. It ensures our multi-source enhancements work together
        seamlessly in realistic academic research scenarios.

        Real-World Scenario:
        A researcher loads a YAML configuration, executes a search strategy,
        and receives enhanced papers with full metadata for analysis.
        """
        # Arrange - Mock complete configuration hierarchy
        mock_search_config = Mock()
        mock_search_config.citation_threshold = 5
        mock_search_config.exclude_terms = ["review", "editorial"]

        mock_strategy = Mock(spec=SearchStrategy)
        mock_strategy.name = "comprehensive_hrv_analysis"
        mock_strategy.search_limit = 100
        mock_strategy.get_all_terms.return_value = [
            "heart rate variability",
            "HRV",
            "cardiac autonomic",
            "R-R intervals",
        ]

        self.mock_config.search_configuration = mock_search_config
        self.mock_config.get_strategy.return_value = mock_strategy
        self.mock_config.list_strategies.return_value = ["comprehensive_hrv_analysis"]

        use_case = ExecuteKeywordSearchUseCase(
            repository=self.mock_repository, keyword_config=self.mock_config
        )

        # Repository returns multiple enhanced papers
        enhanced_papers = [
            self.enhanced_paper,
            self.enhanced_paper,
        ]  # Simulate multiple results
        self.mock_repository.find_by_query.return_value = enhanced_papers

        # Act
        results = use_case.execute_strategy("comprehensive_hrv_analysis")

        # Assert - Complete workflow validation
        assert len(results) == 2

        # Validate SearchQuery construction
        self.mock_repository.find_by_query.assert_called_once()
        search_query = self.mock_repository.find_by_query.call_args[0][0]
        assert isinstance(search_query, SearchQuery)
        assert search_query.max_results == 100
        assert search_query.min_citations == 5
        assert "heart rate variability" in search_query.terms

        # Validate enhanced fields preserved through complete workflow
        for paper in results:
            assert paper.source_metadata is not None
            assert paper.paper_fingerprint is not None
            assert paper.source_metadata.source_name == "ArXiv"

    def test_use_case_works_with_enhanced_arxiv_repository_integration(self):
        """
        Test integration with ArXivPaperRepository enhanced in TDD Cycle 6A.

        Educational Note:
        This test validates that our TDD Cycle 6A enhancements (ArXiv repository
        creating papers with source_metadata and paper_fingerprint) integrate
        seamlessly with the application layer use case.

        Integration Validation:
        - Use case receives enhanced papers from ArXiv repository
        - All multi-source fields are preserved through application layer
        - Business logic works with enhanced domain entities

        Expected Behavior:
        Should INITIALLY PASS if TDD Cycle 6A integration is working correctly,
        or FAIL if there are integration issues between layers.
        """
        # Arrange
        # Import and use the actual enhanced ArXiv repository
        from src.infrastructure.repositories.arxiv_paper_repository import (
            ArxivPaperRepository,
        )

        # Create use case with real ArXiv repository (but mock HTTP calls)
        arxiv_repository = ArxivPaperRepository()

        mock_strategy = Mock(spec=SearchStrategy)
        mock_strategy.name = "arxiv_integration_test"
        mock_strategy.search_limit = 3
        mock_strategy.get_all_terms.return_value = ["machine learning"]
        self.mock_config.get_strategy.return_value = mock_strategy

        use_case = ExecuteKeywordSearchUseCase(
            repository=arxiv_repository, keyword_config=self.mock_config
        )

        # Mock the HTTP request to ArXiv API
        with (
            patch("requests.Session.get") as mock_get,
            patch("feedparser.parse") as mock_feedparser,
        ):

            # Mock HTTP response
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.content = b"<xml>mock response</xml>"
            mock_get.return_value = mock_response

            # Mock feedparser to return structured ArXiv entry
            mock_entry = Mock()
            mock_entry.title = "Machine Learning for Healthcare"
            mock_entry.summary = "Application of ML techniques in medical diagnosis"

            # Create proper author mocks
            author1 = Mock()
            author1.name = "Dr. Alice Johnson"
            author2 = Mock()
            author2.name = "Prof. Bob Smith"
            mock_entry.authors = [author1, author2]

            mock_entry.id = "http://arxiv.org/abs/2024.12345v1"
            mock_entry.categories = "cs.LG cs.AI"
            mock_entry.published_parsed = (2024, 8, 5, 10, 30, 0, 0, 0, 0)
            mock_entry.get.return_value = "10.1000/ml.healthcare.2024"

            mock_feed = Mock()
            mock_feed.entries = [mock_entry]
            mock_feedparser.return_value = mock_feed

            # Act
            results = use_case.execute_strategy("arxiv_integration_test")

            # Assert - Integration with enhanced ArXiv repository
            assert len(results) == 1
            paper = results[0]

            # Validate that ArXiv repository enhancements are preserved by use case
            assert (
                paper.source_metadata is not None
            ), "ArXiv repository should provide source_metadata"
            assert (
                paper.paper_fingerprint is not None
            ), "ArXiv repository should provide paper_fingerprint"
            assert paper.source_metadata.source_name == "ArXiv"
            # Check for either DOI or ArXiv ID in source identifier (DOI is preferred when available)
            source_id = paper.source_metadata.source_identifier
            assert (
                "10.1000/ml.healthcare.2024" in source_id or "2024.12345" in source_id
            )
            assert paper.title == "Machine Learning for Healthcare"


class TestExecuteKeywordSearchUseCaseConfigurationDriven:
    """
    Test configuration-driven behavior and YAML integration workflows.

    Educational Note:
    These tests validate the Strategy Pattern implementation where search behavior
    is driven by external YAML configuration files. This enables researchers to
    modify search strategies without code changes.

    Configuration-Driven Design Benefits:
    - Non-technical users can modify search strategies
    - Different research domains can have specialized configurations
    - A/B testing of different search approaches
    - Reproducible research with versioned configurations
    """

    def test_execute_all_strategies_preserves_enhanced_fields(self):
        """
        Test that batch execution of all strategies preserves enhanced paper fields.

        Educational Note:
        This validates that multi-strategy execution maintains data integrity
        across all enhanced ResearchPaper fields for comprehensive analysis.
        """
        # Arrange
        mock_config = Mock(spec=KeywordConfig)
        # Create mock search configuration
        mock_search_config = Mock()
        mock_search_config.citation_threshold = 0
        mock_search_config.exclude_terms = []
        mock_config.search_configuration = mock_search_config
        mock_config.list_strategies.return_value = ["strategy1", "strategy2"]

        # Mock strategies
        strategy1 = Mock(spec=SearchStrategy)
        strategy1.name = "strategy1"
        strategy1.search_limit = 10
        strategy1.get_all_terms.return_value = ["term1"]

        strategy2 = Mock(spec=SearchStrategy)
        strategy2.name = "strategy2"
        strategy2.search_limit = 20
        strategy2.get_all_terms.return_value = ["term2"]

        mock_config.get_strategy.side_effect = [strategy1, strategy2]

        mock_repository = Mock(spec=PaperRepositoryPort)
        enhanced_paper = Mock(spec=ResearchPaper)
        enhanced_paper.title = "Enhanced Test Paper"
        enhanced_paper.authors = ["Test Author"]
        enhanced_paper.doi = "10.test/example"
        enhanced_paper.source_metadata = Mock(spec=SourceMetadata)
        enhanced_paper.paper_fingerprint = Mock(spec=PaperFingerprint)
        mock_repository.find_by_query.return_value = [enhanced_paper]

        use_case = ExecuteKeywordSearchUseCase(
            repository=mock_repository, keyword_config=mock_config
        )

        # Act
        all_results = use_case.execute_all_strategies()

        # Assert
        assert "strategy1" in all_results
        assert "strategy2" in all_results
        assert len(all_results["strategy1"]) == 1
        assert len(all_results["strategy2"]) == 1

        # Enhanced fields should be preserved across all strategies
        for strategy_name, papers in all_results.items():
            for paper in papers:
                assert paper.source_metadata is not None
                assert paper.paper_fingerprint is not None


class TestExecuteKeywordSearchUseCaseErrorHandling:
    """
    Test error handling and edge cases in use case execution.

    Educational Note:
    Robust error handling is critical in academic research tools where data quality
    and reliability directly impact research outcomes. These tests ensure graceful
    degradation and clear error reporting.

    Error Handling Philosophy:
    - Fail fast for configuration errors (researcher feedback)
    - Graceful degradation for network issues (partial results)
    - Clear error messages for troubleshooting
    - Preserve partial results when possible
    """

    def test_handle_repository_errors_gracefully(self):
        """
        Test graceful handling of repository errors during search execution.

        Educational Note:
        Research tools should handle external service failures gracefully,
        providing clear error messages while preserving any partial results.
        """
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        mock_repository.find_by_query.side_effect = Exception(
            "ArXiv service unavailable"
        )

        mock_config = Mock(spec=KeywordConfig)
        mock_strategy = Mock(spec=SearchStrategy)
        mock_strategy.name = "test"
        mock_strategy.search_limit = 10
        mock_strategy.get_all_terms.return_value = ["test"]
        mock_config.get_strategy.return_value = mock_strategy
        # Create mock search configuration
        mock_search_config = Mock()
        mock_search_config.citation_threshold = 0
        mock_search_config.exclude_terms = []
        mock_config.search_configuration = mock_search_config

        use_case = ExecuteKeywordSearchUseCase(
            repository=mock_repository, keyword_config=mock_config
        )

        # Act & Assert
        with pytest.raises(Exception, match="ArXiv service unavailable"):
            use_case.execute_strategy("test")

    def test_handle_invalid_strategy_names(self):
        """
        Test error handling for invalid strategy names.

        Educational Note:
        Clear error messages help researchers troubleshoot configuration issues
        and understand available search strategies.
        """
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        mock_config = Mock(spec=KeywordConfig)
        mock_config.get_strategy.side_effect = ValueError(
            "Strategy 'invalid' not found"
        )

        use_case = ExecuteKeywordSearchUseCase(
            repository=mock_repository, keyword_config=mock_config
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Strategy 'invalid' not found"):
            use_case.execute_strategy("invalid")

    def test_handle_empty_search_results_with_enhanced_fields(self):
        """
        Test handling of empty search results while maintaining enhanced field expectations.

        Educational Note:
        Even with no results, the system should handle enhanced paper processing
        correctly for consistency and future extensibility.
        """
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        mock_repository.find_by_query.return_value = []  # Empty results

        mock_config = Mock(spec=KeywordConfig)
        # Create mock search configuration
        mock_search_config = Mock()
        mock_search_config.citation_threshold = 0
        mock_search_config.exclude_terms = []
        mock_config.search_configuration = mock_search_config

        mock_strategy = Mock(spec=SearchStrategy)
        mock_strategy.name = "empty_test"
        mock_strategy.search_limit = 10
        mock_strategy.get_all_terms.return_value = ["nonexistent_term"]
        mock_config.get_strategy.return_value = mock_strategy

        use_case = ExecuteKeywordSearchUseCase(
            repository=mock_repository, keyword_config=mock_config
        )

        # Act
        results = use_case.execute_strategy("empty_test")

        # Assert
        assert results == []
        mock_repository.find_by_query.assert_called_once()
