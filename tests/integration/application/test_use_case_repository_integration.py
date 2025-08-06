"""
Integration tests for ExecuteKeywordSearchUseCase with real repositories.

These tests validate the complete workflow from configuration loading through
search execution and result processing. They ensure that the use case properly
coordinates between repositories, configuration, and domain objects.

Educational Notes:
- Integration tests use real implementations, not mocks
- They validate architectural boundaries and data flow
- Configuration integration is essential for research tools
- Error scenarios test system resilience

Design Patterns Tested:
- Repository Pattern: Data access abstraction
- Strategy Pattern: Configurable search strategies
- Command Pattern: Use case execution
- Dependency Injection: Loose coupling between components
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from datetime import datetime, timezone

from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.domain.entities.research_paper import ResearchPaper
from tests.fixtures import SAMPLE_CONFIGS


class TestExecuteKeywordSearchUseCaseIntegration:
    """
    Integration tests for the complete keyword search workflow.

    Educational Note:
    These tests demonstrate how application layer components integrate
    with infrastructure and domain layers to deliver business value.
    """

    @pytest.fixture
    def temp_config_file(self):
        """Create temporary configuration file for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(SAMPLE_CONFIGS["cybersecurity"], f)
            yield str(config_path)

    @pytest.fixture
    def populated_repository(self):
        """Create repository with sample data for search testing."""
        repository = InMemoryPaperRepository()

        # Add sample papers that should match searches
        papers = [
            ResearchPaper(
                title="Advanced Cybersecurity Threat Detection Using Deep Learning",
                authors=["Dr. Alice Johnson"],
                abstract="This paper presents advanced cybersecurity threat detection methods using deep learning approaches for network security analysis.",
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                doi="10.1000/cyber.2023.001",
                citation_count=45,
                keywords=["cybersecurity", "deep learning", "threat detection"],
            ),
            ResearchPaper(
                title="Network Security Protocols in Cloud Computing",
                authors=["Prof. Bob Smith"],
                abstract="Analysis of network security protocols specifically designed for cloud computing environments and distributed systems.",
                publication_date=datetime(2023, 8, 20, tzinfo=timezone.utc),
                doi="10.1000/network.2023.002",
                citation_count=32,
                keywords=["network security", "cloud computing", "protocols"],
            ),
            ResearchPaper(
                title="Information Security in IoT Devices",
                authors=["Dr. Carol Zhang", "Prof. David Lee"],
                abstract="Comprehensive study of information security challenges in Internet of Things devices and proposed mitigation strategies.",
                publication_date=datetime(2023, 4, 10, tzinfo=timezone.utc),
                doi="10.1000/iot.2023.003",
                citation_count=28,
                keywords=["information security", "IoT", "device security"],
            ),
            # Paper that should be filtered out (too few citations)
            ResearchPaper(
                title="Basic Tutorial on Security",
                authors=["Student Writer"],
                abstract="A basic tutorial covering elementary security concepts for beginners.",
                publication_date=datetime(2023, 1, 15, tzinfo=timezone.utc),
                doi="10.1000/tutorial.2023.004",
                citation_count=2,  # Below threshold
                keywords=["tutorial", "basic security"],
            ),
        ]

        repository.save_papers(papers)
        return repository

    def test_use_case_integration_with_configuration_and_repository(
        self, temp_config_file, populated_repository
    ):
        """
        Test complete integration: configuration + use case + repository.

        Educational Note:
        This test validates the entire search workflow from configuration
        loading through result filtering and demonstrates how Clean Architecture
        enables testable, maintainable integrations.
        """
        # Arrange: Create use case with real repository and configuration
        use_case = ExecuteKeywordSearchUseCase(
            repository=populated_repository, config_path=temp_config_file
        )

        # Act: Execute default strategy
        results = use_case.execute_strategy()

        # Assert: Verify integration worked correctly
        assert len(results) == 3  # Should exclude tutorial paper (too few citations)

        # Verify all results match search criteria
        titles = [paper.title for paper in results]
        assert "Advanced Cybersecurity Threat Detection Using Deep Learning" in titles
        assert "Network Security Protocols in Cloud Computing" in titles
        assert "Information Security in IoT Devices" in titles
        assert "Basic Tutorial on Security" not in titles  # Filtered out

        # Verify citation filtering worked
        assert all(paper.citation_count >= 5 for paper in results)

    def test_strategy_execution_with_custom_parameters(
        self, temp_config_file, populated_repository
    ):
        """
        Test strategy execution with parameter overrides.

        Educational Note:
        This demonstrates how the Strategy pattern enables flexible
        configuration while maintaining clean separation of concerns.
        """
        # Arrange
        use_case = ExecuteKeywordSearchUseCase(
            repository=populated_repository, config_path=temp_config_file
        )

        # Act: Execute with custom max_results
        results = use_case.execute_strategy(
            strategy_name="comprehensive_cybersecurity",
            max_results=2,  # Override default
        )

        # Assert: Should return only 2 results due to limit
        assert len(results) == 2

        # Should return highest citation count papers first
        citation_counts = [paper.citation_count for paper in results]
        assert citation_counts == sorted(citation_counts, reverse=True)

    def test_custom_search_integration(self, temp_config_file, populated_repository):
        """
        Test custom search functionality integration.

        Educational Note:
        Custom searches bypass predefined strategies, showing how the
        application layer can support both configured and ad-hoc operations.
        """
        # Arrange
        use_case = ExecuteKeywordSearchUseCase(
            repository=populated_repository, config_path=temp_config_file
        )

        # Act: Execute custom search
        results = use_case.execute_custom_search(
            required_terms=["network security"],
            optional_terms=["cloud"],
            max_results=10,
            min_citations=30,  # Higher threshold
        )

        # Assert: Should find only the cloud computing paper
        assert len(results) == 1
        assert results[0].title == "Network Security Protocols in Cloud Computing"
        assert results[0].citation_count >= 30

    def test_batch_strategy_execution_integration(
        self, temp_config_file, populated_repository
    ):
        """
        Test execution of all available strategies.

        Educational Note:
        Batch operations demonstrate how application layer components
        can coordinate complex workflows while maintaining error isolation.
        """
        # Arrange
        use_case = ExecuteKeywordSearchUseCase(
            repository=populated_repository, config_path=temp_config_file
        )

        # Act: Execute all strategies
        all_results = use_case.execute_all_strategies()

        # Assert: Should return results for all configured strategies
        assert "comprehensive_cybersecurity" in all_results
        assert len(all_results["comprehensive_cybersecurity"]) == 3

    def test_configuration_error_propagation(self, populated_repository):
        """
        Test that configuration errors propagate correctly through the system.

        Educational Note:
        Error handling integration ensures that configuration problems
        are reported clearly to users rather than causing cryptic failures.
        """
        # Arrange: Use non-existent config file
        with pytest.raises(FileNotFoundError):
            ExecuteKeywordSearchUseCase(
                repository=populated_repository, config_path="/nonexistent/config.yaml"
            )

    def test_repository_integration_with_filtering(
        self, temp_config_file, populated_repository
    ):
        """
        Test integration between use case filtering and repository queries.

        Educational Note:
        This test validates that the application layer properly coordinates
        with repositories to apply business rules (like exclusion filters).
        """
        # Arrange: Add paper with excluded term
        excluded_paper = ResearchPaper(
            title="Cybersecurity Tutorial for Beginners",
            authors=["Tutorial Author"],
            abstract="A comprehensive tutorial covering cybersecurity basics and fundamental concepts.",
            publication_date=datetime(2023, 5, 1, tzinfo=timezone.utc),
            doi="10.1000/excluded.2023.001",
            citation_count=15,  # Above threshold but should be excluded
            keywords=["cybersecurity", "tutorial"],
        )
        populated_repository.save_paper(excluded_paper)

        use_case = ExecuteKeywordSearchUseCase(
            repository=populated_repository, config_path=temp_config_file
        )

        # Act: Execute strategy with exclusion filters
        results = use_case.execute_strategy("comprehensive_cybersecurity")

        # Assert: Tutorial paper should be excluded despite matching primary terms
        titles = [paper.title for paper in results]
        assert "Cybersecurity Tutorial for Beginners" not in titles

        # Other papers should still be included
        assert len(results) >= 3  # Original papers that match criteria


class TestUseCaseErrorIntegration:
    """
    Test error handling integration across application boundaries.

    Educational Note:
    Error integration testing ensures that failures in one component
    are handled gracefully by the application layer without cascading
    failures or data corruption.
    """

    def test_repository_error_handling_integration(self, temp_config_file):
        """Test graceful handling of repository errors."""

        # Create a repository that will simulate errors
        class FailingRepository(InMemoryPaperRepository):
            def find_by_query(self, query):
                raise RuntimeError("Database connection failed")

        failing_repo = FailingRepository()
        use_case = ExecuteKeywordSearchUseCase(
            repository=failing_repo, config_path=temp_config_file
        )

        # Repository errors should propagate but be catchable
        with pytest.raises(RuntimeError, match="Database connection failed"):
            use_case.execute_strategy()

    def test_configuration_validation_integration(self, populated_repository):
        """Test integration of configuration validation with use case execution."""
        # Create invalid configuration
        invalid_config = {
            "strategies": {},  # No strategies defined
            "default_strategy": "nonexistent",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "invalid_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(invalid_config, f)

            # Should raise validation error during initialization
            with pytest.raises(ValueError):
                ExecuteKeywordSearchUseCase(
                    repository=populated_repository, config_path=str(config_path)
                )


class TestConfigurationIntegration:
    """
    Test configuration system integration with application components.

    Educational Note:
    Configuration integration tests ensure that YAML-based configuration
    properly drives application behavior and that changes in configuration
    files correctly affect system behavior.
    """

    def test_multiple_strategy_configuration_integration(self, populated_repository):
        """Test integration with configuration containing multiple strategies."""
        multi_strategy_config = {
            "search_configuration": {
                "min_citation_threshold": 10,
                "publication_year_start": 2022,
                "publication_year_end": 2024,
                "max_concurrent_searches": 2,
                "default_strategy": "deep_learning_security",
            },
            "strategies": {
                "deep_learning_security": {
                    "name": "deep_learning_security",
                    "description": "Focus on deep learning in cybersecurity",
                    "primary_keywords": ["deep learning", "cybersecurity"],
                    "secondary_keywords": ["neural networks", "AI security"],
                    "exclusion_keywords": ["tutorial"],
                    "search_limit": 50,
                },
                "network_protocols": {
                    "name": "network_protocols",
                    "description": "Network security protocols",
                    "primary_keywords": ["network security", "protocols"],
                    "secondary_keywords": ["encryption", "authentication"],
                    "exclusion_keywords": ["basic", "introduction"],
                    "search_limit": 30,
                },
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "multi_strategy.yaml"
            with open(config_path, "w") as f:
                yaml.dump(multi_strategy_config, f)

            use_case = ExecuteKeywordSearchUseCase(
                repository=populated_repository, config_path=str(config_path)
            )

            # Test that both strategies are available
            strategies = use_case.get_available_strategies()
            assert "deep_learning_security" in strategies
            assert "network_protocols" in strategies

            # Test execution of different strategies
            dl_results = use_case.execute_strategy("deep_learning_security")
            net_results = use_case.execute_strategy("network_protocols")

            # Results should differ based on search terms
            assert isinstance(dl_results, list)
            assert isinstance(net_results, list)
