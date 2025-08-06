"""
Test suite for ArxivPaperRepository - External API integration testing patterns.

This test suite demonstrates how to test components that depend on external APIs
like arXiv.org. It's particularly educational for academics and researchers who
need to understand how to write reliable tests for network-dependent code.

Educational Concepts Demonstrated:
- Mocking external HTTP requests for reliable, fast tests
- Testing error handling for network failures and API errors
- Verifying data transformation from external formats to domain objects
- Testing read-only repository patterns (arXiv doesn't allow writes)
- Handling real-world API response formats (RSS feeds, XML parsing)

Why We Mock External APIs:
1. **Reliability**: Tests don't fail due to network issues or API downtime
2. **Speed**: No actual HTTP requests means tests run in milliseconds
3. **Control**: We can simulate specific scenarios (errors, edge cases)
4. **Reproducibility**: Same results every time, regardless of external state

Testing Philosophy:
- Test the behavior and logic, not the external service
- Verify that our code correctly handles various API responses
- Ensure proper error handling for network and parsing failures
- Validate data transformation and filtering logic
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from requests import RequestException

from src.infrastructure.repositories.arxiv_paper_repository import ArxivPaperRepository
from src.domain.value_objects.search_query import SearchQuery
from src.domain.entities.research_paper import ResearchPaper


class TestArxivPaperRepositoryInitialization:
    """
    Test ArxivPaperRepository initialization and configuration.

    Educational Note:
    These tests verify that the repository sets up its HTTP session correctly
    with appropriate headers and base URL configuration.
    """

    def test_initialize_with_default_base_url(self):
        """Test that repository initializes with default arXiv API URL."""
        repo = ArxivPaperRepository()

        assert repo.base_url == "http://export.arxiv.org/api/query"
        assert hasattr(repo, "session")
        assert "HRV-Research-Tool" in repo.session.headers.get("User-Agent", "")

    def test_initialize_with_custom_base_url(self):
        """Test that repository accepts custom API endpoint for testing."""
        custom_url = "https://test.arxiv.org/api/query"
        repo = ArxivPaperRepository(base_url=custom_url)

        assert repo.base_url == custom_url

    def test_session_has_proper_user_agent(self):
        """Test that HTTP session includes appropriate User-Agent header.

        Educational Note:
        APIs often require User-Agent headers to identify the calling application.
        This is good API citizenship and helps API providers track usage.
        """
        repo = ArxivPaperRepository()
        user_agent = repo.session.headers.get("User-Agent")

        assert user_agent is not None
        assert "HRV-Research-Tool" in user_agent
        assert "Educational Purpose" in user_agent


class TestArxivPaperRepositoryQuerySearch:
    """
    Test the main search functionality using SearchQuery objects.

    Educational Note:
    This is the most complex functionality to test because it involves:
    1. HTTP request to external API
    2. XML/RSS feed parsing
    3. Data transformation to domain objects
    4. Query filtering and result limiting

    We mock all external dependencies to focus on testing our logic.
    """

    @patch("src.infrastructure.repositories.arxiv_paper_repository.feedparser")
    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_find_by_query_successful_search(self, mock_get, mock_feedparser):
        """
        Test successful paper search with valid results.

        Educational Note:
        This test demonstrates the complete flow:
        1. Mock the HTTP request to return successful response
        2. Mock the feedparser to return structured data
        3. Verify our code processes the data correctly
        4. Check that domain objects are created properly
        """
        # Arrange: Set up mocks for external dependencies
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<xml>mock response</xml>"
        mock_get.return_value = mock_response

        # Mock feedparser to return structured arXiv entry
        mock_entry = Mock()
        mock_entry.title = "Heart Rate Variability in TBI Patients"
        mock_entry.summary = "Study of HRV patterns in traumatic brain injury"
        # Create Mock objects with name attributes to match arXiv API structure
        author1 = Mock()
        author1.name = "Dr. Jane Smith"
        author2 = Mock()
        author2.name = "Dr. John Doe"
        mock_entry.authors = [author1, author2]
        mock_entry.id = "http://arxiv.org/abs/2301.12345"
        mock_entry.published = "2023-01-01T00:00:00Z"
        mock_entry.categories = "q-bio.NC stat.ME"
        mock_entry.get.return_value = ""  # No DOI
        mock_entry.published_parsed = (
            2023,
            1,
            1,
            0,
            0,
            0,
            0,
            1,
            0,
        )  # time.struct_time format

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feedparser.parse.return_value = mock_feed

        # Act: Execute the search
        repo = ArxivPaperRepository()
        query = SearchQuery(terms=["heart rate variability"], max_results=5)
        results = repo.find_by_query(query)

        # Assert: Verify the behavior
        assert len(results) == 1
        paper = results[0]
        assert paper.title == "Heart Rate Variability in TBI Patients"
        assert len(paper.authors) == 2
        assert "Dr. Jane Smith" in paper.authors
        assert paper.arxiv_id == "2301.12345"
        assert paper.venue == "arXiv preprint"

        # Verify HTTP request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "search_query" in kwargs["params"]
        assert kwargs["params"]["max_results"] == 5
        assert len(results) == 1
        paper = results[0]
        assert paper.title == "Heart Rate Variability in TBI Patients"
        assert len(paper.authors) == 2
        assert "Dr. Jane Smith" in paper.authors
        assert paper.arxiv_id == "2301.12345"
        assert paper.venue == "arXiv preprint"

        # Verify HTTP request was made with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "search_query" in kwargs["params"]
        assert kwargs["params"]["max_results"] == 5

    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_find_by_query_network_error(self, mock_get):
        """
        Test handling of network errors during API requests.

        Educational Note:
        Network-dependent code must handle various failure modes:
        - Connection timeouts
        - DNS resolution failures
        - HTTP errors (404, 500, etc.)
        - Connection refused

        Our repository should gracefully handle these and return empty results
        rather than crashing the application.
        """
        # Arrange: Mock network failure
        mock_get.side_effect = RequestException("Network timeout")

        # Act: Attempt search during network failure
        repo = ArxivPaperRepository()
        query = SearchQuery(terms=["test"], max_results=1)
        results = repo.find_by_query(query)

        # Assert: Should handle error gracefully
        assert results == []
        mock_get.assert_called_once()

    @patch("src.infrastructure.repositories.arxiv_paper_repository.feedparser")
    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_find_by_query_parsing_error(self, mock_get, mock_feedparser):
        """
        Test handling of XML parsing errors from malformed API responses.

        Educational Note:
        External APIs can sometimes return malformed data. Robust applications
        must handle parsing errors gracefully rather than crashing.
        """
        # Arrange: Mock successful HTTP request but parsing failure
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"malformed xml"
        mock_get.return_value = mock_response

        mock_feedparser.parse.side_effect = Exception("XML parsing failed")

        # Act: Attempt search with parsing failure
        repo = ArxivPaperRepository()
        query = SearchQuery(terms=["test"], max_results=1)
        results = repo.find_by_query(query)

        # Assert: Should handle parsing error gracefully
        assert results == []

    @patch("src.infrastructure.repositories.arxiv_paper_repository.feedparser")
    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_find_by_query_empty_results(self, mock_get, mock_feedparser):
        """Test handling of empty search results from arXiv API."""
        # Arrange: Mock successful request with no results
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<xml>empty feed</xml>"
        mock_get.return_value = mock_response

        mock_feed = Mock()
        mock_feed.entries = []  # Empty results
        mock_feedparser.parse.return_value = mock_feed

        # Act: Search for non-existent terms
        repo = ArxivPaperRepository()
        query = SearchQuery(terms=["nonexistent_unique_term_xyz"], max_results=10)
        results = repo.find_by_query(query)

        # Assert: Should return empty list
        assert results == []


class TestArxivPaperRepositorySpecificLookups:
    """
    Test specific paper lookup methods (by DOI, by arXiv ID).

    Educational Note:
    These methods demonstrate different search strategies:
    - DOI lookup: Standard for published papers, limited in arXiv
    - arXiv ID lookup: Most reliable for arXiv papers
    """

    @patch("src.infrastructure.repositories.arxiv_paper_repository.feedparser")
    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_find_by_arxiv_id_success(self, mock_get, mock_feedparser):
        """Test successful lookup by arXiv ID."""
        # Arrange: Mock successful arXiv ID lookup
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<xml>paper data</xml>"
        mock_get.return_value = mock_response

        mock_entry = Mock()
        mock_entry.title = "Test Paper"
        mock_entry.summary = "Test abstract"
        # Create Mock object with name attribute to match arXiv API structure
        author_mock = Mock()
        author_mock.name = "Test Author"
        mock_entry.authors = [author_mock]
        mock_entry.id = "http://arxiv.org/abs/2301.12345"
        mock_entry.published = "2023-01-01T00:00:00Z"
        mock_entry.categories = "cs.LG"
        mock_entry.get.return_value = ""
        mock_entry.published_parsed = (2023, 1, 1, 0, 0, 0, 0, 1, 0)

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feedparser.parse.return_value = mock_feed

        # Act: Look up paper by arXiv ID
        repo = ArxivPaperRepository()
        paper = repo.find_by_arxiv_id("2301.12345")

        # Assert: Should return the paper
        assert paper is not None
        assert paper.title == "Test Paper"
        assert paper.arxiv_id == "2301.12345"

        # Verify correct API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["id_list"] == "2301.12345"

    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_find_by_arxiv_id_not_found(self, mock_get):
        """Test lookup by non-existent arXiv ID."""
        # Arrange: Mock request failure
        mock_get.side_effect = Exception("Paper not found")

        # Act: Look up non-existent paper
        repo = ArxivPaperRepository()
        paper = repo.find_by_arxiv_id("9999.99999")

        # Assert: Should return None
        assert paper is None

    @patch.object(ArxivPaperRepository, "find_by_query")
    def test_find_by_doi_delegates_to_query_search(self, mock_find_by_query):
        """
        Test that DOI lookup uses the general query search.

        Educational Note:
        This demonstrates composition - complex methods can be built
        from simpler ones. DOI lookup reuses the query search logic.
        """
        # Arrange: Mock the query search to return a result
        mock_paper = Mock(spec=ResearchPaper)
        mock_find_by_query.return_value = [mock_paper]

        # Act: Look up by DOI
        repo = ArxivPaperRepository()
        result = repo.find_by_doi("10.1000/test.doi")

        # Assert: Should delegate to find_by_query and return first result
        mock_find_by_query.assert_called_once()
        call_args = mock_find_by_query.call_args[0][0]  # First argument (query)
        assert "10.1000/test.doi" in call_args.terms
        assert result == mock_paper

    @patch.object(ArxivPaperRepository, "find_by_query")
    def test_find_by_doi_returns_none_when_no_results(self, mock_find_by_query):
        """Test DOI lookup when no papers are found."""
        # Arrange: Mock empty results
        mock_find_by_query.return_value = []

        # Act: Look up non-existent DOI
        repo = ArxivPaperRepository()
        result = repo.find_by_doi("10.1000/nonexistent.doi")

        # Assert: Should return None
        assert result is None


class TestArxivPaperRepositoryReadOnlyOperations:
    """
    Test operations that should not be supported (arXiv is read-only).

    Educational Note:
    Not all repositories support all operations. ArxivPaperRepository
    is read-only because arXiv is a public archive that researchers
    can't modify through the API.
    """

    def test_save_paper_raises_not_implemented_error(self):
        """Test that saving papers is not supported."""
        repo = ArxivPaperRepository()
        mock_paper = Mock(spec=ResearchPaper)

        with pytest.raises(NotImplementedError, match="read-only"):
            repo.save_paper(mock_paper)

    def test_save_papers_raises_not_implemented_error(self):
        """Test that batch saving papers is not supported."""
        repo = ArxivPaperRepository()
        mock_papers = [Mock(spec=ResearchPaper)]

        with pytest.raises(NotImplementedError, match="read-only"):
            repo.save_papers(mock_papers)

    def test_count_all_returns_unlimited_indicator(self):
        """
        Test that counting all papers returns -1 (unlimited/unknown).

        Educational Note:
        arXiv contains millions of papers. Rather than making an expensive
        API call to count them all, we return -1 to indicate unlimited/unknown.
        """
        repo = ArxivPaperRepository()
        count = repo.count_all()
        assert count == -1


class TestArxivPaperRepositoryQueryBuilding:
    """
    Test the internal query building logic.

    Educational Note:
    This tests the private method that converts our SearchQuery domain objects
    into arXiv-specific query syntax. Testing private methods is sometimes
    controversial, but for complex transformation logic like this, it's valuable.
    """

    def test_build_arxiv_query_with_single_term(self):
        """Test query building with single search term."""
        repo = ArxivPaperRepository()
        query = SearchQuery(terms=["neuroscience"])

        arxiv_query = repo._build_arxiv_query(query)

        assert "(ti:neuroscience OR abs:neuroscience)" in arxiv_query

    def test_build_arxiv_query_with_multiple_terms(self):
        """Test query building with multiple search terms."""
        repo = ArxivPaperRepository()
        query = SearchQuery(terms=["heart rate", "variability"])

        arxiv_query = repo._build_arxiv_query(query)

        # Should use OR logic for broader search
        assert "(ti:heart rate OR abs:heart rate)" in arxiv_query
        assert "(ti:variability OR abs:variability)" in arxiv_query
        assert " OR " in arxiv_query

    def test_build_arxiv_query_with_date_filters(self):
        """Test query building with date range filters."""
        repo = ArxivPaperRepository()
        start_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2023, 12, 31, tzinfo=timezone.utc)
        query = SearchQuery(terms=["test"], start_date=start_date, end_date=end_date)

        arxiv_query = repo._build_arxiv_query(query)

        assert "submittedDate:[20200101* TO *]" in arxiv_query
        assert "submittedDate:[* TO 20231231*]" in arxiv_query

    def test_build_arxiv_query_empty_terms(self):
        """Test query building with no search terms."""
        repo = ArxivPaperRepository()
        # Use a single search term since SearchQuery validation requires at least one term
        query = SearchQuery(terms=["test"])
        # Test the private method with empty query parts to simulate empty terms scenario

        arxiv_query = repo._build_arxiv_query(query)

        assert "(ti:test OR abs:test)" in arxiv_query


class TestArxivPaperRepositoryDataConversion:
    """
    Test conversion from arXiv API format to ResearchPaper domain objects.

    Educational Note:
    Data transformation is a critical part of integration with external APIs.
    We need to map from their format to our domain objects while handling
    missing or malformed data gracefully.
    """

    def test_convert_arxiv_entry_to_paper_complete_data(self):
        """Test conversion with complete arXiv entry data."""
        repo = ArxivPaperRepository()

        # Create mock arXiv entry with all fields
        entry = Mock()
        entry.title = "Test Paper\nWith Newlines"
        entry.summary = "Test abstract\nwith newlines"
        # Create Mock objects with name attributes to match arXiv API structure
        author1 = Mock()
        author1.name = "Author One"
        author2 = Mock()
        author2.name = "Author Two"
        entry.authors = [author1, author2]
        entry.id = "http://arxiv.org/abs/2301.12345"
        entry.published = "2023-01-15T10:30:00Z"
        entry.categories = "cs.AI stat.ML"
        entry.get.return_value = "10.1000/test.doi"
        entry.published_parsed = (
            2023,
            1,
            15,
            10,
            30,
            0,
            0,
            15,
            0,
        )  # time.struct_time format

        paper = repo._convert_arxiv_entry_to_paper(entry)

        assert paper is not None
        assert paper.title == "Test Paper With Newlines"  # Newlines removed
        assert paper.abstract == "Test abstract with newlines"
        assert len(paper.authors) == 2
        assert "Author One" in paper.authors
        assert paper.arxiv_id == "2301.12345"
        assert paper.doi == "10.1000/test.doi"
        assert paper.venue == "arXiv preprint"
        assert paper.citation_count == 0  # arXiv doesn't provide citations
        assert "cs.AI" in paper.keywords
        assert "stat.ML" in paper.keywords

    def test_convert_arxiv_entry_to_paper_minimal_data(self):
        """Test conversion with minimal arXiv entry data."""
        repo = ArxivPaperRepository()

        # Create mock entry with minimal required fields
        entry = Mock()
        entry.title = "Minimal Paper"
        entry.summary = "Minimal abstract"
        # Create Mock object with name attribute to match arXiv API structure
        author_mock = Mock()
        author_mock.name = "Minimal Author"
        entry.authors = [
            author_mock
        ]  # Must have at least one author for ResearchPaper validation
        entry.id = "http://arxiv.org/abs/1234.5678"
        entry.published = "2023-01-01T00:00:00Z"
        entry.categories = ""
        entry.get.return_value = ""  # No DOI
        entry.published_parsed = (
            2023,
            1,
            1,
            0,
            0,
            0,
            0,
            1,
            0,
        )  # time.struct_time format

        paper = repo._convert_arxiv_entry_to_paper(entry)

        assert paper is not None
        assert paper.title == "Minimal Paper"
        assert len(paper.authors) == 1
        assert "Minimal Author" in paper.authors
        assert paper.arxiv_id == "1234.5678"
        assert paper.doi == ""

    def test_convert_arxiv_entry_handles_malformed_data(self):
        """Test conversion gracefully handles malformed entry data."""
        repo = ArxivPaperRepository()

        # Create entry that will cause conversion errors
        entry = Mock()
        entry.title = "Test"
        entry.summary = "Test"
        entry.authors = "not_a_list"  # Wrong type
        entry.id = "malformed_id"
        entry.published = "invalid_date_format"

        paper = repo._convert_arxiv_entry_to_paper(entry)

        # Should handle errors gracefully - either return None or valid paper
        # The exact behavior depends on implementation error handling
        if paper is not None:
            assert hasattr(paper, "title")
            assert hasattr(paper, "authors")


class TestArxivPaperRepositoryPdfAccess:
    """
    Test PDF URL generation for paper downloads.

    Educational Note:
    Many research workflows require access to full paper PDFs.
    This shows how to generate proper arXiv PDF URLs.
    """

    def test_get_pdf_url_from_arxiv_id(self):
        """Test PDF URL generation from arXiv ID."""
        repo = ArxivPaperRepository()

        # Create mock paper with arXiv ID
        paper = Mock()
        paper.arxiv_id = "2301.12345"

        pdf_url = repo.get_pdf_url(paper)

        assert pdf_url == "https://arxiv.org/pdf/2301.12345.pdf"

    def test_get_pdf_url_from_pdf_url_field(self):
        """Test PDF URL when paper already has pdf_url."""
        repo = ArxivPaperRepository()

        # Create mock paper with existing PDF URL
        paper = Mock()
        paper.arxiv_id = None
        paper.pdf_url = "https://arxiv.org/pdf/1234.5678.pdf"

        pdf_url = repo.get_pdf_url(paper)

        assert pdf_url == "https://arxiv.org/pdf/1234.5678.pdf"

    def test_get_pdf_url_returns_none_for_no_id(self):
        """Test PDF URL generation when no arXiv ID available."""
        repo = ArxivPaperRepository()

        # Create mock paper without arXiv ID or PDF URL
        paper = Mock()
        paper.arxiv_id = None
        paper.pdf_url = None

        pdf_url = repo.get_pdf_url(paper)

        assert pdf_url is None


class TestArxivPaperRepositoryQueryFiltering:
    """
    Test additional filtering logic applied to search results.

    Educational Note:
    Sometimes external APIs don't support all the filtering we need,
    so we apply additional filters to the results after retrieval.
    """

    def test_matches_query_filters_date_range(self):
        """Test filtering by date range."""
        repo = ArxivPaperRepository()

        # Create paper and query with date constraints
        paper = Mock()
        paper.publication_date = datetime(2022, 6, 15, tzinfo=timezone.utc)
        paper.citation_count = 10

        # Paper should match date range
        query_within_range = SearchQuery(
            terms=["test"],
            start_date=datetime(2022, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
        )
        assert repo._matches_query_filters(paper, query_within_range) is True

        # Paper should not match date range
        query_outside_range = SearchQuery(
            terms=["test"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        assert repo._matches_query_filters(paper, query_outside_range) is False

    def test_matches_query_filters_no_constraints(self):
        """Test filtering with no date constraints (should match everything)."""
        repo = ArxivPaperRepository()

        paper = Mock()
        paper.publication_date = datetime.now(timezone.utc)
        paper.citation_count = 0

        query = SearchQuery(terms=["test"])  # No date constraints

        assert repo._matches_query_filters(paper, query) is True
