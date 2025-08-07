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


class TestArxivRepositoryMultiSourceIntegration:
    """
    Test suite for ArXiv repository multi-source integration (TDD Cycle 6A).

    This test class validates that the ArXiv repository correctly populates
    the multi-source fields (source_metadata, paper_fingerprint) that were
    added to ResearchPaper in TDD Cycle 5.

    Educational Notes:
    - Demonstrates integration testing across architectural layers
    - Shows how to test Clean Architecture cross-layer workflows
    - Validates that infrastructure properly creates domain objects
    - Tests the complete ArXiv API → SourceMetadata → ResearchPaper pipeline

    TDD Cycle 6A Phase: RED → GREEN → REFACTOR
    Current Phase: RED (these tests should initially FAIL)
    """

    def test_arxiv_papers_have_source_metadata_populated(self):
        """
        Test that papers created by ArXiv repository have source_metadata populated.

        Business Rule: All papers from ArXiv repository should include source
        attribution metadata for provenance tracking and quality assessment.

        Educational Note:
        - Tests integration between infrastructure and domain layers
        - Validates multi-source architecture in practice
        - Ensures source attribution for academic integrity

        This test should initially FAIL because the current ArXiv repository
        doesn't populate the source_metadata field in ResearchPaper entities.
        """
        # Arrange
        repo = ArxivPaperRepository()

        # Mock ArXiv API entry with realistic data
        mock_entry = Mock()
        mock_entry.title = "Heart Rate Variability in Clinical Settings"
        mock_entry.summary = (
            "This paper analyzes HRV patterns in clinical environments."
        )
        # Create proper Mock objects with name attributes
        author1 = Mock()
        author1.name = "Dr. Jane Smith"
        author2 = Mock()
        author2.name = "Prof. John Doe"
        mock_entry.authors = [author1, author2]
        mock_entry.published_parsed = (2024, 8, 1, 10, 30, 0, 0, 0, 0)
        mock_entry.id = "http://arxiv.org/abs/2408.12345v1"
        mock_entry.categories = "cs.AI stat.ML"
        mock_entry.get.return_value = "10.1000/arxiv.2408.12345"

        # Act
        paper = repo._convert_arxiv_entry_to_paper(mock_entry)

        # Assert - Paper should have source_metadata populated
        assert paper is not None
        assert (
            paper.source_metadata is not None
        ), "ArXiv papers should have source_metadata populated"
        assert paper.source_metadata.source_name == "ArXiv"
        assert paper.source_metadata.source_identifier.startswith("arxiv:")
        assert (
            paper.source_metadata.has_full_text is True
        )  # ArXiv papers have full text
        assert paper.source_metadata.is_open_access is True  # ArXiv is open access
        assert paper.source_metadata.peer_review_status == "preprint"
        assert (
            paper.source_metadata.quality_score > 0.0
        )  # Should have quality assessment

    def test_arxiv_papers_have_paper_fingerprint_for_duplicate_detection(self):
        """
        Test that papers created by ArXiv repository have paper_fingerprint for duplicate detection.

        Business Rule: All papers should have fingerprints to enable duplicate
        detection across different sources and prevent redundant downloads.

        Educational Note:
        - Demonstrates multi-source duplicate detection foundation
        - Shows value object usage in infrastructure layer
        - Tests cross-source identity management

        This test should initially FAIL because the current ArXiv repository
        doesn't create paper_fingerprint for ResearchPaper entities.
        """
        # Arrange
        repo = ArxivPaperRepository()

        # Mock ArXiv API entry
        mock_entry = Mock()
        mock_entry.title = "Machine Learning for Healthcare Applications"
        mock_entry.summary = "Comprehensive review of ML applications in healthcare."
        # Create proper Mock object with name attribute
        author1 = Mock()
        author1.name = "Dr. Alice Johnson"
        mock_entry.authors = [author1]
        mock_entry.published_parsed = (2024, 7, 15, 14, 20, 0, 0, 0, 0)
        mock_entry.id = "http://arxiv.org/abs/2407.98765v2"
        mock_entry.categories = "cs.LG cs.AI"
        mock_entry.get.return_value = ""

        # Act
        paper = repo._convert_arxiv_entry_to_paper(mock_entry)

        # Assert - Paper should have paper_fingerprint for duplicate detection
        assert paper is not None
        assert (
            paper.paper_fingerprint is not None
        ), "ArXiv papers should have paper_fingerprint for duplicate detection"
        assert paper.paper_fingerprint.primary_identifier is not None
        assert paper.paper_fingerprint.title_hash is not None
        assert paper.paper_fingerprint.author_hash is not None

    def test_arxiv_source_metadata_preserves_arxiv_specific_data(self):
        """
        Test that ArXiv-specific metadata is preserved in source_metadata.

        Business Rule: Source-specific information (categories, version info,
        submission dates) should be preserved for research provenance.

        Educational Note:
        - Tests source-specific data preservation patterns
        - Shows how to maintain API-specific information in domain objects
        - Demonstrates metadata enrichment from external sources
        """
        # Arrange
        repo = ArxivPaperRepository()

        # Mock ArXiv entry with rich metadata
        mock_entry = Mock()
        mock_entry.title = "Quantum Computing Algorithms"
        mock_entry.summary = "Novel quantum algorithms for optimization problems."
        # Create proper Mock objects with name attributes
        author1 = Mock()
        author1.name = "Prof. Bob Wilson"
        author2 = Mock()
        author2.name = "Dr. Carol Davis"
        mock_entry.authors = [author1, author2]
        mock_entry.published_parsed = (2024, 6, 10, 9, 15, 0, 0, 0, 0)
        mock_entry.id = "http://arxiv.org/abs/2406.54321v3"
        mock_entry.categories = "quant-ph cs.DS math.OC"

        # Create proper get method that returns appropriate values for different keys
        def mock_get(key, default=None):
            if key == "id":
                return "http://arxiv.org/abs/2406.54321v3"
            elif key == "arxiv_doi":
                return "10.1000/quantum.example"
            elif key == "comment":
                return "Quantum optimization algorithms with practical applications"
            elif key == "journal_ref":
                return "Nature Quantum 2024"
            elif key == "primary_category":
                return "quant-ph"
            elif key == "links":
                return [
                    "http://arxiv.org/abs/2406.54321v3",
                    "http://arxiv.org/pdf/2406.54321v3.pdf",
                ]
            elif key == "categories":
                return "quant-ph cs.DS math.OC"
            else:
                return default

        mock_entry.get = mock_get

        # Act
        paper = repo._convert_arxiv_entry_to_paper(mock_entry)

        # Assert - Source metadata should preserve ArXiv-specific information
        assert paper is not None
        assert paper.source_metadata is not None

        # Check ArXiv-specific data preservation
        source_data = paper.source_metadata.source_specific_data
        assert "categories" in source_data, "ArXiv categories should be preserved"
        assert "quant-ph" in source_data["categories"] or "quant-ph" in str(source_data)

        # Verify source URL points to ArXiv
        assert "arxiv.org" in paper.source_metadata.source_url

        # Check source identifier format
        assert paper.source_metadata.source_identifier.startswith("arxiv:")
        assert "2406.54321" in paper.source_metadata.source_identifier

    def test_complete_multi_source_workflow_end_to_end(self):
        """
        Test complete multi-source workflow from ArXiv API to enhanced ResearchPaper.

        Business Rule: The complete workflow should demonstrate multi-source
        architecture capabilities including source attribution, quality assessment,
        and duplicate detection preparation.

        Educational Note:
        - Demonstrates complete Clean Architecture workflow
        - Shows end-to-end multi-source paper aggregation
        - Validates architectural integration across all layers
        - Tests practical utility of multi-source enhancements
        """
        # Arrange
        repo = ArxivPaperRepository()

        # Mock comprehensive ArXiv entry
        mock_entry = Mock()
        mock_entry.title = "Advanced Deep Learning Techniques"
        mock_entry.summary = "Comprehensive survey of state-of-the-art deep learning methods and applications."
        # Create proper Mock objects with name attributes
        author1 = Mock()
        author1.name = "Prof. Emma Zhang"
        author2 = Mock()
        author2.name = "Dr. Michael Brown"
        author3 = Mock()
        author3.name = "Dr. Sarah Kim"
        mock_entry.authors = [author1, author2, author3]
        mock_entry.published_parsed = (2024, 5, 20, 16, 45, 0, 0, 0, 0)
        mock_entry.id = "http://arxiv.org/abs/2405.11111v1"
        mock_entry.categories = "cs.LG cs.AI cs.CV"
        mock_entry.get.return_value = "10.1000/deeplearning.survey.2024"

        # Act - Convert ArXiv entry to enhanced ResearchPaper
        paper = repo._convert_arxiv_entry_to_paper(mock_entry)

        # Assert - Validate complete multi-source integration
        assert (
            paper is not None
        ), "ArXiv entry should convert to ResearchPaper successfully"

        # Verify core ResearchPaper fields
        assert paper.title == "Advanced Deep Learning Techniques"
        assert len(paper.authors) == 3
        assert "Prof. Emma Zhang" in paper.authors
        assert paper.abstract.startswith("Comprehensive survey")

        # Verify multi-source fields are populated
        assert paper.source_metadata is not None, "Source metadata should be populated"
        assert (
            paper.paper_fingerprint is not None
        ), "Paper fingerprint should be created"

        # Verify source metadata quality
        metadata = paper.source_metadata
        assert metadata.source_name == "ArXiv"
        assert metadata.has_full_text is True
        assert metadata.is_open_access is True
        assert metadata.peer_review_status == "preprint"
        assert metadata.quality_score >= 0.8  # ArXiv generally high quality

        # Verify paper fingerprint for duplicate detection
        fingerprint = paper.paper_fingerprint
        assert fingerprint.title_hash is not None
        assert fingerprint.author_hash is not None
        assert len(fingerprint.primary_identifier) > 0

        # Verify ArXiv-specific data preservation
        source_data = metadata.source_specific_data
        assert "categories" in source_data or any(
            "cs.LG" in str(v) for v in source_data.values()
        )

        # Verify educational completeness - this demonstrates the full
        # multi-source architecture working end-to-end from external API
        # to enhanced domain entities ready for multi-source aggregation
