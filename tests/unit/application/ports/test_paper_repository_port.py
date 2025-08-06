"""
Unit tests for the PaperRepositoryPort interface.

This module tests the abstract interface that defines how the application
layer accesses research paper data. As a port (interface), it defines
the contract that concrete implementations must follow.

Educational Notes:
- Testing interfaces helps document expected behavior
- Tests serve as specifications for implementation
- We test that the interface can be properly subclassed
- Mock implementations help test use cases that depend on this port

Testing Strategy:
1. Test interface definition and abstract methods
2. Test that concrete implementations must implement all methods
3. Test method signatures and return types
4. Provide test fixtures for use case testing
"""

import pytest
from abc import ABC
from typing import List, Optional
from unittest.mock import Mock

# Import domain objects
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery

# Import will work after we create the port
from src.application.ports.paper_repository_port import PaperRepositoryPort


class TestPaperRepositoryPortInterface:
    """
    Test suite for the PaperRepositoryPort interface definition.

    Educational Note:
    Testing abstract interfaces ensures they're properly defined
    and documents the contract for implementations.
    """

    def test_paper_repository_port_is_abstract(self):
        """
        Test that PaperRepositoryPort cannot be instantiated directly.

        This ensures implementers must provide concrete implementations.
        """
        # Act & Assert - Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            PaperRepositoryPort()

    def test_paper_repository_port_has_required_methods(self):
        """
        Test that the port defines all required abstract methods.
        """
        # Arrange - Get all abstract methods
        abstract_methods = PaperRepositoryPort.__abstractmethods__

        # Assert - Required methods are defined as abstract
        expected_methods = {
            "find_by_query",
            "find_by_doi",
            "find_by_arxiv_id",
            "save_paper",
            "save_papers",
            "count_all",
        }

        assert abstract_methods == expected_methods

    def test_concrete_implementation_must_implement_all_methods(self):
        """
        Test that concrete implementations must implement all abstract methods.
        """

        # Arrange - Create incomplete implementation
        class IncompleteRepository(PaperRepositoryPort):
            # Missing implementations - should not be instantiable
            pass

        # Act & Assert - Should not be able to instantiate incomplete implementation
        with pytest.raises(TypeError):
            IncompleteRepository()


class TestPaperRepositoryPortBehavior:
    """
    Test suite for PaperRepositoryPort behavior with mock implementation.

    Educational Note:
    These tests define the expected behavior that concrete implementations
    should follow. They serve as both specification and regression tests.
    """

    @pytest.fixture
    def mock_repository(self):
        """
        Create a mock repository for testing use cases.

        Educational Note:
        Mock objects allow us to test application logic without
        depending on concrete implementations.
        """
        mock_repo = Mock(spec=PaperRepositoryPort)
        return mock_repo

    @pytest.fixture
    def sample_papers(self):
        """
        Provide sample research papers for testing.
        """
        from datetime import datetime, timezone

        return [
            ResearchPaper(
                title="Heart Rate Variability in Healthy Adults",
                authors=["Dr. Smith", "Dr. Johnson"],
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                doi="10.1000/test1",
                abstract="HRV analysis in healthy population",
                venue="Journal of Cardiovascular Research",
            ),
            ResearchPaper(
                title="ECG Signal Processing Methods",
                authors=["Dr. Brown"],
                publication_date=datetime(2023, 2, 1, tzinfo=timezone.utc),
                doi="10.1000/test2",
                abstract="ECG processing techniques",
                venue="IEEE Transactions on Biomedical Engineering",
            ),
        ]

    @pytest.fixture
    def sample_query(self):
        """
        Provide a sample search query for testing.
        """
        return SearchQuery(terms=["heart rate variability"])

    def test_find_by_query_returns_list_of_papers(
        self, mock_repository, sample_papers, sample_query
    ):
        """
        Test that find_by_query returns a list of ResearchPaper objects.

        This defines the contract for query-based searches.
        """
        # Arrange
        mock_repository.find_by_query.return_value = sample_papers

        # Act
        results = mock_repository.find_by_query(sample_query)

        # Assert
        assert isinstance(results, list)
        assert all(isinstance(paper, ResearchPaper) for paper in results)
        assert len(results) == 2
        mock_repository.find_by_query.assert_called_once_with(sample_query)

    def test_find_by_query_returns_empty_list_when_no_results(
        self, mock_repository, sample_query
    ):
        """
        Test that find_by_query returns empty list when no papers match.

        This ensures graceful handling of no-result scenarios.
        """
        # Arrange
        mock_repository.find_by_query.return_value = []

        # Act
        results = mock_repository.find_by_query(sample_query)

        # Assert
        assert results == []
        assert isinstance(results, list)

    def test_find_by_doi_returns_single_paper_or_none(
        self, mock_repository, sample_papers
    ):
        """
        Test that find_by_doi returns a single paper or None.

        DOI lookups should return at most one paper since DOIs are unique.
        """
        # Arrange - Test found case
        mock_repository.find_by_doi.return_value = sample_papers[0]

        # Act
        result = mock_repository.find_by_doi("10.1000/test1")

        # Assert
        assert isinstance(result, ResearchPaper)
        assert result.doi == "10.1000/test1"

        # Test not found case
        mock_repository.find_by_doi.return_value = None
        result_not_found = mock_repository.find_by_doi("10.1000/nonexistent")
        assert result_not_found is None

    def test_find_by_arxiv_id_returns_single_paper_or_none(
        self, mock_repository, sample_papers
    ):
        """
        Test that find_by_arxiv_id returns a single paper or None.

        ArXiv ID lookups should return at most one paper since IDs are unique.
        """
        from datetime import datetime, timezone

        # Arrange
        arxiv_paper = ResearchPaper(
            title="Machine Learning for HRV",
            authors=["Dr. AI"],
            publication_date=datetime(2023, 3, 1, tzinfo=timezone.utc),
            arxiv_id="2301.12345",
            abstract="ML approaches to HRV",
        )
        mock_repository.find_by_arxiv_id.return_value = arxiv_paper

        # Act
        result = mock_repository.find_by_arxiv_id("2301.12345")

        # Assert
        assert isinstance(result, ResearchPaper)
        assert result.arxiv_id == "2301.12345"

    def test_save_paper_accepts_research_paper(self, mock_repository, sample_papers):
        """
        Test that save_paper accepts a ResearchPaper object.

        This defines the contract for saving individual papers.
        """
        # Arrange
        paper_to_save = sample_papers[0]
        mock_repository.save_paper.return_value = None  # Void method

        # Act
        mock_repository.save_paper(paper_to_save)

        # Assert
        mock_repository.save_paper.assert_called_once_with(paper_to_save)

    def test_save_papers_accepts_list_of_papers(self, mock_repository, sample_papers):
        """
        Test that save_papers accepts a list of ResearchPaper objects.

        This defines the contract for batch saving operations.
        """
        # Arrange
        mock_repository.save_papers.return_value = None  # Void method

        # Act
        mock_repository.save_papers(sample_papers)

        # Assert
        mock_repository.save_papers.assert_called_once_with(sample_papers)


# Educational Notes for Students:
#
# 1. Interface Testing Benefits:
#    - Documents expected behavior for implementers
#    - Ensures interface is properly designed
#    - Provides regression testing for contract changes
#    - Enables confident refactoring
#
# 2. Mock Testing Strategy:
#    - Use mocks to test interactions without dependencies
#    - Mock objects implement the same interface as real objects
#    - Focus on testing the contract, not implementation details
#    - Mocks enable fast, isolated unit tests
#
# 3. Fixture Usage:
#    - Fixtures provide reusable test data
#    - Keep fixtures simple and focused
#    - Use fixtures to set up common test scenarios
#    - Fixtures improve test readability and maintainability
#
# 4. Port Pattern Benefits:
#    - Enables dependency inversion principle
#    - Makes application layer testable in isolation
#    - Allows easy swapping of implementations
#    - Provides clear boundaries between layers
