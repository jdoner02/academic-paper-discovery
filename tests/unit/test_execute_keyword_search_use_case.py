"""
Test suite for ExecuteKeywordSearchUseCase - validates application layer orchestration.

This test suite demonstrates how to test Use Cases that orchestrate multiple
domain objects and infrastructure components. It shows proper mocking
strategies and integration testing approaches.

Educational Notes:
- Use Case Testing: Focus on business workflow validation, not implementation details
- Mock Strategy: Mock infrastructure dependencies, test domain orchestration
- Test Organization: Group by business scenarios, not technical methods
- Integration Points: Validate interaction between application and domain layers
"""

import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path
from typing import List
from datetime import datetime, timezone

from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.keyword_config import (
    KeywordConfig,
    SearchStrategy,
    SearchConfiguration,
)


class TestExecuteKeywordSearchUseCaseCreation:
    """Test creation and initialization of ExecuteKeywordSearchUseCase."""

    def test_create_use_case_with_valid_repository(self):
        """Use case should initialize with valid repository and default config path."""
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)

        # Act - Should succeed since config file exists
        use_case = ExecuteKeywordSearchUseCase(mock_repository)

        # Assert
        assert use_case.repository == mock_repository
        assert use_case.keyword_config is not None

    def test_create_use_case_with_custom_config_path(self, tmp_path):
        """Use case should accept custom configuration file path."""
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        config_file = tmp_path / "custom_keywords.yaml"

        # Create minimal valid YAML config
        config_content = """
strategies:
  basic:
    description: "Core HRV research"
    primary_keywords: ["heart rate variability"]
    secondary_keywords: ["HRV"]
    search_limit: 50

search_configuration:
  default_strategy: "basic"
  citation_threshold: 5
  exclude_terms: ["animal", "in vitro"]
"""
        config_file.write_text(config_content)

        # Act
        use_case = ExecuteKeywordSearchUseCase(mock_repository, config_file)

        # Assert
        assert use_case.repository == mock_repository
        assert use_case.keyword_config is not None

    def test_reject_invalid_repository(self):
        """Use case should reject objects that don't implement PaperRepositoryPort."""
        # Arrange
        invalid_repository = Mock()  # Not spec'd as PaperRepositoryPort

        # Act & Assert
        with pytest.raises(
            TypeError, match="Repository must implement PaperRepositoryPort"
        ):
            ExecuteKeywordSearchUseCase(invalid_repository)

    def test_reject_nonexistent_config_file(self):
        """Use case should raise FileNotFoundError for nonexistent config files."""
        # Arrange
        mock_repository = Mock(spec=PaperRepositoryPort)
        nonexistent_path = Path("nonexistent_config.yaml")

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            ExecuteKeywordSearchUseCase(mock_repository, nonexistent_path)


class TestExecuteKeywordSearchUseCaseStrategyExecution:
    """Test execution of predefined search strategies."""

    @pytest.fixture
    def mock_repository(self):
        """Create mock repository for testing."""
        repository = Mock(spec=PaperRepositoryPort)
        return repository

    @pytest.fixture
    def sample_config_file(self, tmp_path):
        """Create sample configuration file for testing."""
        config_file = tmp_path / "test_keywords.yaml"
        config_content = """
strategies:
  basic:
    description: "Core HRV research"
    primary_keywords: ["heart rate variability"]
    secondary_keywords: ["HRV"]
    search_limit: 50
  medical:
    description: "Medical applications"
    primary_keywords: ["heart rate variability", "TBI"]
    secondary_keywords: ["HRV", "traumatic brain injury"]
    search_limit: 100

search_configuration:
  default_strategy: "basic"
  citation_threshold: 5
  exclude_terms: ["animal", "in vitro"]
"""
        config_file.write_text(config_content)
        return config_file

    @pytest.fixture
    def sample_papers(self):
        """Create sample research papers for testing."""
        return [
            ResearchPaper(
                title="HRV Analysis in Healthy Subjects",
                authors=["Smith, J.", "Doe, A."],
                publication_date=datetime(2023, 5, 15, tzinfo=timezone.utc),
                abstract="Study of heart rate variability in normal population",
                doi="10.1000/test1",
                venue="Cardiology Journal",
                citation_count=10,
            ),
            ResearchPaper(
                title="Animal Studies of HRV",
                authors=["Johnson, B."],
                publication_date=datetime(2022, 3, 10, tzinfo=timezone.utc),
                abstract="Heart rate variability research in animal models",
                doi="10.1000/test2",
                venue="Animal Research",
                citation_count=8,
            ),
            ResearchPaper(
                title="HRV in TBI Patients",
                authors=["Wilson, C."],
                publication_date=datetime(2023, 7, 20, tzinfo=timezone.utc),
                abstract="Heart rate variability analysis in traumatic brain injury patients",
                doi="10.1000/test3",
                venue="Neurology",
                citation_count=15,
            ),
        ]

    @pytest.fixture
    def use_case(self, mock_repository, sample_config_file):
        """Create use case instance for testing."""
        return ExecuteKeywordSearchUseCase(mock_repository, sample_config_file)

    def test_execute_default_strategy(self, use_case, mock_repository, sample_papers):
        """Should execute default strategy when none specified."""
        # Arrange
        mock_repository.find_by_query.return_value = sample_papers

        # Act
        results = use_case.execute_strategy()

        # Assert
        assert len(results) == 2  # Animal study should be filtered out
        assert results[0].title == "HRV Analysis in Healthy Subjects"
        assert results[1].title == "HRV in TBI Patients"

        # Verify repository was called with correct query
        mock_repository.find_by_query.assert_called_once()
        call_args = mock_repository.find_by_query.call_args[0][0]
        assert isinstance(call_args, SearchQuery)
        assert "heart rate variability" in call_args.terms
        assert call_args.max_results == 50

    def test_execute_specific_strategy(self, use_case, mock_repository, sample_papers):
        """Should execute specified strategy with correct parameters."""
        # Arrange
        mock_repository.find_by_query.return_value = sample_papers

        # Act
        results = use_case.execute_strategy("medical")

        # Assert
        assert len(results) == 2  # Animal study filtered out

        # Verify repository called with medical strategy parameters
        call_args = mock_repository.find_by_query.call_args[0][0]
        assert call_args.max_results == 100  # Medical strategy has different max
        assert "TBI" in call_args.terms  # Medical strategy includes medical terms

    def test_execute_nonexistent_strategy(self, use_case):
        """Should raise ValueError for nonexistent strategy."""
        # Act & Assert
        with pytest.raises(ValueError, match="Strategy 'nonexistent' not found"):
            use_case.execute_strategy("nonexistent")

    def test_execute_strategy_with_max_results_override(
        self, use_case, mock_repository, sample_papers
    ):
        """Should override max results when specified."""
        # Arrange
        mock_repository.find_by_query.return_value = sample_papers

        # Act
        use_case.execute_strategy("basic", max_results=25)

        # Assert
        call_args = mock_repository.find_by_query.call_args[0][0]
        assert call_args.max_results == 25  # Should use override, not strategy default


class TestExecuteKeywordSearchUseCaseCustomSearch:
    """Test custom search functionality."""

    @pytest.fixture
    def use_case(self, tmp_path):
        """Create use case for custom search testing."""
        mock_repository = Mock(spec=PaperRepositoryPort)
        config_file = tmp_path / "custom_test.yaml"
        config_content = """
strategies:
  basic:
    description: "Basic HRV research"
    primary_keywords: ["heart rate variability"]
    secondary_keywords: ["HRV"]
    search_limit: 50

search_configuration:
  default_strategy: "basic"  
  citation_threshold: 10
  exclude_terms: ["animal"]
"""
        config_file.write_text(config_content)
        return ExecuteKeywordSearchUseCase(mock_repository, config_file)

    def test_execute_custom_search_with_required_terms(self, use_case):
        """Should execute custom search with specified terms."""
        # Arrange
        sample_papers = [
            ResearchPaper(
                title="Custom HRV Study",
                authors=["Custom, A."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                abstract="Custom research on heart rate variability",
                doi="10.1000/test1",
                venue="Custom Journal",
                citation_count=12,
            )
        ]
        use_case.repository.find_by_query.return_value = sample_papers

        # Act
        results = use_case.execute_custom_search(
            required_terms=["hrv", "custom"], max_results=25
        )

        # Assert
        assert len(results) == 1
        assert results[0].title == "Custom HRV Study"

        # Verify query construction
        call_args = use_case.repository.find_by_query.call_args[0][0]
        assert "hrv" in call_args.terms
        assert "custom" in call_args.terms
        assert call_args.max_results == 25
        assert call_args.min_citations == 10  # From configuration

    def test_execute_custom_search_with_optional_terms(self, use_case):
        """Should include optional terms in search query."""
        # Arrange
        use_case.repository.find_by_query.return_value = []

        # Act
        use_case.execute_custom_search(
            required_terms=["hrv"], optional_terms=["tbi", "stress"], max_results=30
        )

        # Assert
        call_args = use_case.repository.find_by_query.call_args[0][0]
        expected_terms = ["hrv", "tbi", "stress"]
        for term in expected_terms:
            assert term in call_args.terms

    def test_execute_custom_search_with_min_citations_override(self, use_case):
        """Should use specified min citations instead of configuration default."""
        # Arrange
        use_case.repository.find_by_query.return_value = []

        # Act
        use_case.execute_custom_search(
            required_terms=["heart rate variability"], min_citations=20
        )

        # Assert
        call_args = use_case.repository.find_by_query.call_args[0][0]
        assert call_args.min_citations == 20  # Override, not config default of 10

    def test_custom_search_reject_empty_required_terms(self, use_case):
        """Should reject custom search with no required terms."""
        # Act & Assert
        with pytest.raises(
            ValueError, match="At least one required term must be provided"
        ):
            use_case.execute_custom_search(required_terms=[])


class TestExecuteKeywordSearchUseCaseBatchOperations:
    """Test batch operations and strategy management."""

    @pytest.fixture
    def use_case_with_multiple_strategies(self, tmp_path):
        """Create use case with multiple strategies for batch testing."""
        mock_repository = Mock(spec=PaperRepositoryPort)
        config_file = tmp_path / "batch_test.yaml"
        config_content = """
strategies:
  basic:
    description: "Basic HRV"
    primary_keywords: ["heart rate variability"]
    secondary_keywords: ["HRV"]
    search_limit: 25
  medical:
    description: "Medical HRV"
    primary_keywords: ["heart rate variability", "TBI"]
    secondary_keywords: ["HRV", "traumatic brain injury"]
    search_limit: 50
  analysis:
    description: "HRV Analysis"
    primary_keywords: ["heart rate variability"]
    secondary_keywords: ["HRV", "frequency domain analysis"]
    search_limit: 30

search_configuration:
  default_strategy: "basic"
  citation_threshold: 5
  exclude_terms: []
"""
        config_file.write_text(config_content)
        return ExecuteKeywordSearchUseCase(mock_repository, config_file)

    def test_execute_all_strategies(self, use_case_with_multiple_strategies):
        """Should execute all configured strategies and return results by name."""
        # Arrange
        mock_papers = [
            ResearchPaper(
                doi="10.1000/test1",
                title="Test Paper",
                abstract="Test abstract",
                authors=["Test, A."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=10,
                venue="Test Journal",
            )
        ]
        use_case_with_multiple_strategies.repository.find_by_query.return_value = (
            mock_papers
        )

        # Act
        results = use_case_with_multiple_strategies.execute_all_strategies()

        # Assert
        assert len(results) == 3  # Three strategies defined
        assert "basic" in results
        assert "medical" in results
        assert "analysis" in results

        # Each strategy should have results
        for strategy_name, strategy_results in results.items():
            assert len(strategy_results) == 1
            assert strategy_results[0].title == "Test Paper"

        # Repository should be called once per strategy
        assert (
            use_case_with_multiple_strategies.repository.find_by_query.call_count == 3
        )

    def test_get_available_strategies(self, use_case_with_multiple_strategies):
        """Should return list of available strategy names."""
        # Act
        strategies = use_case_with_multiple_strategies.get_available_strategies()

        # Assert
        assert len(strategies) == 3
        assert "basic" in strategies
        assert "medical" in strategies
        assert "analysis" in strategies

    def test_get_strategy_info(self, use_case_with_multiple_strategies):
        """Should return detailed information about specific strategy."""
        # Act
        strategy_info = use_case_with_multiple_strategies.get_strategy_info("medical")

        # Assert
        assert isinstance(strategy_info, SearchStrategy)
        assert strategy_info.description == "Medical HRV"
        assert strategy_info.search_limit == 50  # From fixture config
        assert "heart rate variability" in strategy_info.primary_keywords
        assert "TBI" in strategy_info.primary_keywords

    def test_get_strategy_info_nonexistent(self, use_case_with_multiple_strategies):
        """Should raise ValueError for nonexistent strategy."""
        # Act & Assert
        with pytest.raises(ValueError, match="Strategy 'nonexistent' not found"):
            use_case_with_multiple_strategies.get_strategy_info("nonexistent")


class TestExecuteKeywordSearchUseCaseFiltering:
    """Test configuration-based filtering functionality."""

    @pytest.fixture
    def use_case_with_exclusions(self, tmp_path):
        """Create use case with exclusion terms for filtering tests."""
        mock_repository = Mock(spec=PaperRepositoryPort)
        config_file = tmp_path / "filter_test.yaml"
        config_content = """
strategies:
  basic:
    description: "Basic HRV research"
    primary_keywords: ["heart rate variability"]
    secondary_keywords: ["HRV"]
    search_limit: 50

search_configuration:
  default_strategy: "basic"
  citation_threshold: 5
  exclude_terms: ["animal", "in vitro", "cell culture"]
"""
        config_file.write_text(config_content)
        return ExecuteKeywordSearchUseCase(mock_repository, config_file)

    def test_filter_excluded_terms_in_title(self, use_case_with_exclusions):
        """Should filter out papers with excluded terms in title."""
        # Arrange
        papers_with_exclusions = [
            ResearchPaper(
                doi="10.1000/good",
                title="HRV in Human Subjects",
                abstract="Good human study",
                authors=["Human, A."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=10,
                venue="Human Journal",
            ),
            ResearchPaper(
                doi="10.1000/bad1",
                title="Animal Studies of HRV",
                abstract="Study in animals",
                authors=["Animal, B."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=8,
                venue="Animal Journal",
            ),
            ResearchPaper(
                doi="10.1000/bad2",
                title="HRV in Cell Culture",
                abstract="Cell culture experiments",
                authors=["Culture, C."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=6,
                venue="Cell Journal",
            ),
        ]
        use_case_with_exclusions.repository.find_by_query.return_value = (
            papers_with_exclusions
        )

        # Act
        results = use_case_with_exclusions.execute_strategy()

        # Assert
        assert len(results) == 1
        assert results[0].title == "HRV in Human Subjects"

    def test_filter_excluded_terms_in_abstract(self, use_case_with_exclusions):
        """Should filter out papers with excluded terms in abstract."""
        # Arrange
        papers_with_exclusions = [
            ResearchPaper(
                doi="10.1000/good",
                title="HRV Research",
                abstract="Human heart rate variability study",
                authors=["Human, A."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=10,
                venue="Human Journal",
            ),
            ResearchPaper(
                doi="10.1000/bad",
                title="HRV Research",
                abstract="This study used in vitro methods to analyze HRV",
                authors=["Vitro, B."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=8,
                venue="Lab Journal",
            ),
        ]
        use_case_with_exclusions.repository.find_by_query.return_value = (
            papers_with_exclusions
        )

        # Act
        results = use_case_with_exclusions.execute_strategy()

        # Assert
        assert len(results) == 1
        assert results[0].abstract == "Human heart rate variability study"

    def test_case_insensitive_filtering(self, use_case_with_exclusions):
        """Should filter excluded terms regardless of case."""
        # Arrange
        papers_with_case_variations = [
            ResearchPaper(
                doi="10.1000/good",
                title="HRV in Humans",
                abstract="Human study",
                authors=["Human, A."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=10,
                venue="Human Journal",
            ),
            ResearchPaper(
                doi="10.1000/bad1",
                title="ANIMAL Studies of HRV",  # Uppercase
                abstract="Animal research",
                authors=["Animal, B."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=8,
                venue="Animal Journal",
            ),
            ResearchPaper(
                doi="10.1000/bad2",
                title="HRV Analysis",
                abstract="This study used In Vitro methods",  # Mixed case
                authors=["Vitro, C."],
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                citation_count=6,
                venue="Lab Journal",
            ),
        ]
        use_case_with_exclusions.repository.find_by_query.return_value = (
            papers_with_case_variations
        )

        # Act
        results = use_case_with_exclusions.execute_strategy()

        # Assert
        assert len(results) == 1
        assert results[0].title == "HRV in Humans"
