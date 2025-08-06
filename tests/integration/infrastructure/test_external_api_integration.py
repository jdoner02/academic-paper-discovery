"""
Integration tests for ArxivPaperRepository with external API simulation.

These tests validate that the ArxivPaperRepository correctly integrates with
external APIs while properly implementing the repository port interface.
They use sophisticated mocking to simulate real API interactions.

Educational Notes:
- Infrastructure integration tests external system boundaries
- They validate adapter pattern implementation
- Mock external APIs to ensure consistent, fast testing
- Test both happy path and error scenarios

Design Patterns Tested:
- Adapter Pattern: External API integration
- Repository Pattern: Data access abstraction
- Gateway Pattern: External service access
"""

import pytest
import responses
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from src.infrastructure.repositories.arxiv_paper_repository import ArxivPaperRepository
from src.domain.value_objects.search_query import SearchQuery
from src.domain.entities.research_paper import ResearchPaper
from tests.fixtures import MOCK_ARXIV_RESPONSES


class TestArxivRepositoryExternalIntegration:
    """
    Test ArxivPaperRepository integration with external arXiv API.

    Educational Note:
    These integration tests validate that our repository correctly
    implements the adapter pattern to integrate with external APIs
    while maintaining clean architectural boundaries.
    """

    @patch("src.infrastructure.repositories.arxiv_paper_repository.feedparser.parse")
    @patch(
        "src.infrastructure.repositories.arxiv_paper_repository.requests.Session.get"
    )
    def test_arxiv_api_integration_with_real_response_format(
        self, mock_get, mock_feedparser
    ):
        """
        Test integration with realistic arXiv API response format.

        Educational Note:
        This test uses the actual arXiv API response format to ensure
        our adapter correctly handles real-world data structures.
        """
        # Arrange: Mock feedparser response with realistic data
        mock_feedparser.return_value = Mock(
            entries=[
                {
                    "id": "http://arxiv.org/abs/2306.12345v1",
                    "title": "Deep Learning Approaches for Cybersecurity Threat Detection",
                    "summary": "This paper presents novel deep learning approaches for detecting cybersecurity threats in network traffic analysis and monitoring systems.",
                    "authors": [Mock(name="Alice Johnson"), Mock(name="Bob Smith")],
                    "published": "2023-06-15T00:00:00Z",
                    "links": [
                        {
                            "rel": "alternate",
                            "href": "http://arxiv.org/abs/2306.12345v1",
                        },
                        {
                            "rel": "related",
                            "href": "http://arxiv.org/pdf/2306.12345v1.pdf",
                            "type": "application/pdf",
                        },
                    ],
                }
            ]
        )

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "mock atom xml response"
        mock_get.return_value = mock_response

        # Create repository and search query
        repository = ArxivPaperRepository()
        query = SearchQuery(terms=["cybersecurity", "deep learning"], max_results=10)

        # Act: Execute search
        results = repository.find_by_query(query)

        # Assert: Should correctly parse real API response format
        assert len(results) == 1
        paper = results[0]

        assert (
            paper.title == "Deep Learning Approaches for Cybersecurity Threat Detection"
        )
        assert "Alice Johnson" in paper.authors
        assert "Bob Smith" in paper.authors
        assert paper.arxiv_id == "2306.12345"
        assert "cybersecurity threats" in paper.abstract

    @responses.activate
    def test_arxiv_api_error_handling_integration(self):
        """
        Test integration with arXiv API error responses.

        Educational Note:
        Infrastructure components must gracefully handle external system
        failures and translate them into domain-appropriate responses.
        """
        # Arrange: Mock API error
        responses.add(
            responses.GET,
            "http://export.arxiv.org/api/query",
            status=503,
            body="Service Unavailable",
        )

        repository = ArxivPaperRepository()
        query = SearchQuery(terms=["test"], max_results=10)

        # Act & Assert: Should handle API errors gracefully
        with pytest.raises(Exception):  # Should propagate meaningful error
            repository.find_by_query(query)

    @responses.activate
    def test_arxiv_query_parameter_integration(self):
        """
        Test that search queries are correctly translated to arXiv API parameters.

        Educational Note:
        This test validates the adapter's translation between domain concepts
        (SearchQuery) and external API requirements (arXiv query syntax).
        """
        # Arrange: Mock successful response
        responses.add(
            responses.GET,
            "http://export.arxiv.org/api/query",
            body=MOCK_ARXIV_RESPONSES["empty_results"]["feed"],
            content_type="application/atom+xml",
        )

        repository = ArxivPaperRepository()

        # Complex search query with multiple parameters
        query = SearchQuery(
            terms=["machine learning", "cybersecurity"],
            start_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 12, 31, tzinfo=timezone.utc),
            max_results=50,
            min_citations=10,
        )

        # Act: Execute search
        repository.find_by_query(query)

        # Assert: Verify API call parameters
        assert len(responses.calls) == 1
        request_url = responses.calls[0].request.url

        # Should include search terms
        assert "machine%20learning" in request_url or "machine+learning" in request_url
        assert "cybersecurity" in request_url

        # Should include result limit
        assert "max_results=50" in request_url

    def test_arxiv_id_specific_lookup_integration(self):
        """
        Test direct arXiv ID lookup integration.

        Educational Note:
        This test validates that the repository can handle specific
        document lookups in addition to general search queries.
        """
        with patch("feedparser.parse") as mock_feedparser:
            # Mock successful arXiv ID lookup
            mock_feedparser.return_value = Mock(
                entries=[
                    {
                        "id": "http://arxiv.org/abs/2306.12345v1",
                        "title": "Specific Paper Title",
                        "summary": "Specific paper abstract",
                        "authors": [Mock(name="Author Name")],
                        "published": "2023-06-15T00:00:00Z",
                        "links": [
                            {
                                "rel": "alternate",
                                "href": "http://arxiv.org/abs/2306.12345v1",
                            },
                            {
                                "rel": "related",
                                "href": "http://arxiv.org/pdf/2306.12345v1.pdf",
                                "type": "application/pdf",
                            },
                        ],
                    }
                ]
            )

            repository = ArxivPaperRepository()

            # Act: Find by specific arXiv ID
            paper = repository.find_by_arxiv_id("2306.12345")

            # Assert: Should return specific paper
            assert paper is not None
            assert paper.arxiv_id == "2306.12345"
            assert paper.title == "Specific Paper Title"


class TestFileSystemIntegration:
    """
    Test file system integration for configuration and downloads.

    Educational Note:
    File system integration tests ensure that the application properly
    handles external file operations while maintaining data integrity.
    """

    def test_configuration_file_loading_integration(self):
        """
        Test integration between configuration system and file system.

        Educational Note:
        Configuration integration tests ensure that external YAML files
        are properly loaded and validated before being used in the domain.
        """
        import tempfile
        import yaml
        from pathlib import Path
        from src.domain.value_objects.keyword_config import KeywordConfig

        # Arrange: Create temporary configuration file
        config_data = {
            "search_configuration": {
                "min_citation_threshold": 10,
                "publication_year_start": 2020,
                "publication_year_end": 2024,
                "max_concurrent_searches": 3,
            },
            "strategies": [
                {
                    "name": "test_strategy",
                    "description": "Test strategy for integration",
                    "primary_terms": ["machine learning"],
                    "secondary_terms": ["AI"],
                    "excluded_terms": ["tutorial"],
                    "max_results": 50,
                }
            ],
            "default_strategy": "test_strategy",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            # Act: Load configuration from file system
            config = KeywordConfig.from_yaml_file(str(config_path))

            # Assert: Should successfully integrate file data with domain objects
            assert isinstance(config, KeywordConfig)
            assert len(config.strategies) == 1
            assert config.strategies[0].name == "test_strategy"
            assert config.default_strategy == "test_strategy"

    def test_download_directory_creation_integration(self):
        """
        Test integration between download service and file system.

        Educational Note:
        This test validates that domain services can successfully
        coordinate with file system operations while maintaining
        business logic separation.
        """
        import tempfile
        from pathlib import Path
        from src.domain.services.paper_download_service import PaperDownloadService

        with tempfile.TemporaryDirectory() as temp_base_dir:
            # Arrange: Create download service with temporary directory
            service = PaperDownloadService(base_output_dir=temp_base_dir)

            # Act: Create output directory
            with patch(
                "src.domain.services.paper_download_service.datetime"
            ) as mock_datetime:
                mock_datetime.now.return_value = datetime(2023, 8, 5, 10, 30, 0)

                output_dir = service._create_output_directory("test_strategy")

            # Assert: Directory should be created with proper structure
            assert output_dir.exists()
            assert output_dir.is_dir()
            assert "2023-08-05_test_strategy" in str(output_dir)

    @patch("src.domain.services.paper_download_service.requests.Session.get")
    def test_pdf_download_file_integration(self, mock_requests_get):
        """
        Test integration between download service and file system for PDF storage.

        Educational Note:
        This test validates that the domain service properly coordinates
        network operations with file system storage while handling errors.
        """
        import tempfile
        from pathlib import Path
        from src.domain.services.paper_download_service import PaperDownloadService
        from src.domain.entities.research_paper import ResearchPaper

        # Arrange: Mock successful download response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"Mock PDF content"]
        mock_requests_get.return_value = mock_response

        paper = ResearchPaper(
            title="Test Paper for Download",
            authors=["Test Author"],
            abstract="Test abstract",
            publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            doi="10.1000/test.2023.001",
            arxiv_id="2301.12345",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = PaperDownloadService(base_output_dir=temp_dir)
            output_dir = Path(temp_dir) / "test_output"
            output_dir.mkdir()

            # Act: Download paper to file system
            result_path = service._download_paper_pdf(paper, output_dir)

            # Assert: File should be created with proper content
            assert result_path is not None
            assert result_path.exists()
            assert result_path.suffix == ".pdf"
            assert "Test_Paper_for_Download" in result_path.name

            # Verify file content
            with open(result_path, "rb") as f:
                content = f.read()
                assert content == b"Mock PDF content"


class TestNetworkResilienceIntegration:
    """
    Test network resilience and error handling integration.

    Educational Note:
    Network resilience tests ensure that the application gracefully
    handles various network conditions and external system failures.
    """

    @responses.activate
    def test_network_timeout_handling_integration(self):
        """
        Test integration of network timeout handling.

        Educational Note:
        Timeout handling tests ensure that the application doesn't hang
        indefinitely when external systems are slow or unresponsive.
        """
        import requests

        # Arrange: Mock timeout response
        responses.add(
            responses.GET,
            "http://export.arxiv.org/api/query",
            body=requests.exceptions.Timeout("Request timeout"),
        )

        repository = ArxivPaperRepository()
        query = SearchQuery(terms=["test"], max_results=10)

        # Act & Assert: Should handle timeout gracefully
        with pytest.raises(requests.exceptions.Timeout):
            repository.find_by_query(query)

    @responses.activate
    def test_network_connection_error_integration(self):
        """
        Test integration of network connection error handling.

        Educational Note:
        Connection error tests ensure that network failures are properly
        translated into domain-appropriate error messages.
        """
        import requests

        # Arrange: Mock connection error
        responses.add(
            responses.GET,
            "http://export.arxiv.org/api/query",
            body=requests.exceptions.ConnectionError("Connection failed"),
        )

        repository = ArxivPaperRepository()
        query = SearchQuery(terms=["test"], max_results=10)

        # Act & Assert: Should handle connection errors gracefully
        with pytest.raises(requests.exceptions.ConnectionError):
            repository.find_by_query(query)

    def test_malformed_api_response_integration(self):
        """
        Test integration with malformed external API responses.

        Educational Note:
        Malformed response handling ensures that unexpected data formats
        don't cause application crashes or data corruption.
        """
        with patch("feedparser.parse") as mock_feedparser:
            # Arrange: Mock malformed response
            mock_feedparser.return_value = Mock(
                entries=[
                    {
                        # Missing required fields to test resilience
                        "id": "malformed-id",
                        "title": None,  # Invalid title
                        "summary": "",  # Empty summary
                        "authors": [],  # No authors
                        "published": "invalid-date-format",
                        "links": [],  # No links
                    }
                ]
            )

            repository = ArxivPaperRepository()
            query = SearchQuery(terms=["test"], max_results=10)

            # Act: Process malformed response
            results = repository.find_by_query(query)

            # Assert: Should handle malformed data gracefully
            # Implementation should either skip malformed entries or provide defaults
            assert isinstance(results, list)
            # Specific behavior depends on implementation -
            # either empty list or papers with default values
