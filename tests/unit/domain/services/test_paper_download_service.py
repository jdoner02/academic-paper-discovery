"""
Test suite for PaperDownloadService - Domain service testing patterns.

This test suite demonstrates how to test domain services that coordinate
complex business operations across multiple entities. It's educational for
academics and researchers learning about:

Educational Concepts Demonstrated:
- Testing domain services in Clean Architecture
- Mocking file system operations for reproducible tests
- Testing HTTP download functionality without actual network calls
- Verifying business logic for file organization and metadata generation
- Error handling patterns for network and file operations
- Progress tracking and user feedback mechanisms

Why We Mock File and Network Operations:
1. **Speed**: Tests run instantly without actual downloads or file creation
2. **Reliability**: Tests don't depend on network connectivity or disk space
3. **Control**: We can simulate specific scenarios (network failures, disk full, etc.)
4. **Isolation**: Tests focus on business logic rather than infrastructure

Testing Philosophy for Domain Services:
- Test the coordination and orchestration logic
- Verify error handling and recovery mechanisms
- Ensure proper file organization and naming
- Validate metadata generation and persistence
- Test progress tracking and user feedback
"""

import pytest
import json
from unittest.mock import Mock, patch, mock_open, MagicMock
from pathlib import Path
from datetime import datetime, timezone
import requests

from src.domain.services.paper_download_service import PaperDownloadService
from src.domain.entities.research_paper import ResearchPaper


class TestPaperDownloadServiceInitialization:
    """
    Test PaperDownloadService initialization and configuration.

    Educational Note:
    These tests verify proper setup of the download service including
    directory configuration and HTTP session setup.
    """

    def test_initialize_with_default_output_directory(self):
        """Test service initializes with default 'outputs' directory."""
        service = PaperDownloadService()

        assert str(service.base_output_dir) == "outputs"
        assert hasattr(service, "session")
        assert isinstance(service.session, requests.Session)

    def test_initialize_with_custom_output_directory(self):
        """Test service accepts custom output directory."""
        custom_dir = "/custom/research/papers"
        service = PaperDownloadService(base_output_dir=custom_dir)

        assert str(service.base_output_dir) == custom_dir

    def test_http_session_has_proper_user_agent(self):
        """Test that HTTP session includes appropriate User-Agent header.

        Educational Note:
        Good API citizenship requires identifying your application to
        servers. This helps them track usage and provide appropriate
        rate limiting or support.
        """
        service = PaperDownloadService()
        user_agent = service.session.headers.get("User-Agent")

        assert user_agent is not None
        assert "Research-Paper-Aggregator" in user_agent
        assert "Educational Purpose" in user_agent


class TestPaperDownloadServiceBatchDownload:
    """
    Test batch downloading functionality with progress tracking.

    Educational Note:
    Batch operations are common in research workflows. These tests show
    how to handle multiple downloads, progress reporting, and error recovery.
    """

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    @patch("builtins.open", mock_open())
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_download_papers_successful_batch(
        self, mock_json_dump, mock_requests_get, mock_mkdir
    ):
        """
        Test successful batch download with progress tracking.

        Educational Note:
        This comprehensive test demonstrates the full download workflow:
        1. Directory creation
        2. Multiple paper downloads
        3. Progress callback execution
        4. Metadata generation
        5. Result compilation
        """
        # Arrange: Set up test papers
        paper1 = ResearchPaper(
            title="Paper One",
            authors=["Author A"],
            abstract="First test paper",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/paper1",
            arxiv_id="2301.12345",
        )
        paper2 = ResearchPaper(
            title="Paper Two",
            authors=["Author B"],
            abstract="Second test paper",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/paper2",
            arxiv_id="2301.67890",
        )
        papers = [paper1, paper2]

        # Mock successful HTTP responses
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [
            b"PDF content chunk 1",
            b"PDF content chunk 2",
        ]
        mock_requests_get.return_value = mock_response

        # Mock progress callback
        progress_callback = Mock()

        # Act: Execute batch download
        service = PaperDownloadService()
        results = service.download_papers(papers, "test_strategy", progress_callback)

        # Assert: Verify results
        assert len(results) == 2
        assert "Paper One" in results
        assert "Paper Two" in results
        assert not any(
            result.startswith("Download failed") for result in results.values()
        )

        # Verify progress callback was called correctly
        assert progress_callback.call_count == 2
        progress_callback.assert_any_call(1, 2, "Paper One")
        progress_callback.assert_any_call(2, 2, "Paper Two")

        # Verify directory creation
        mock_mkdir.assert_called()

        # Verify metadata was saved
        mock_json_dump.assert_called_once()

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    def test_download_papers_handles_network_failures(
        self, mock_requests_get, mock_mkdir
    ):
        """
        Test graceful handling of network failures during batch download.

        Educational Note:
        Robust systems must handle partial failures gracefully. Individual
        download failures shouldn't crash the entire batch operation.
        """
        # Arrange: Create test paper
        paper = ResearchPaper(
            title="Network Failure Paper",
            authors=["Author C"],
            abstract="Test paper for network failure",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/network_fail",
            arxiv_id="2301.99999",
        )

        # Mock network failure
        mock_requests_get.side_effect = requests.ConnectionError("Network timeout")

        # Act: Attempt download with network failure
        service = PaperDownloadService()
        results = service.download_papers([paper], "test_strategy")

        # Assert: Should handle failure gracefully
        assert len(results) == 1
        assert "Network Failure Paper" in results
        assert results["Network Failure Paper"].startswith("Download failed")

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    def test_download_papers_with_no_pdf_url(self, mock_mkdir):
        """Test handling of papers without downloadable PDF URLs."""
        # Arrange: Create paper without arXiv ID or PDF URL
        paper = ResearchPaper(
            title="No PDF Paper",
            authors=["Author D"],
            abstract="Paper without downloadable PDF",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/no_pdf",
            # No arxiv_id or pdf_url
        )

        # Act: Attempt download
        service = PaperDownloadService()
        results = service.download_papers([paper], "test_strategy")

        # Assert: Should report no PDF URL available
        assert len(results) == 1
        assert results["No PDF Paper"] == "Download failed - No PDF URL available"


class TestPaperDownloadServiceSingleDownload:
    """
    Test single paper download functionality.

    Educational Note:
    Single downloads are useful for targeted paper retrieval or
    when users want specific papers without running full searches.
    """

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    @patch("builtins.open", mock_open())
    def test_download_single_paper_success(self, mock_requests_get, mock_mkdir):
        """Test successful single paper download."""
        # Arrange: Create test paper
        paper = ResearchPaper(
            title="Single Download Paper",
            authors=["Solo Author"],
            abstract="Test single download",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/single",
            arxiv_id="2301.11111",
        )

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"PDF content"]
        mock_requests_get.return_value = mock_response

        # Act: Download single paper
        service = PaperDownloadService()
        result_path = service.download_single_paper(paper)

        # Assert: Should return valid path
        assert result_path is not None
        assert "Single_Download_Paper.pdf" in str(result_path)

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    def test_download_single_paper_network_failure(self, mock_requests_get, mock_mkdir):
        """Test single paper download with network failure."""
        # Arrange: Create test paper
        paper = ResearchPaper(
            title="Failed Download Paper",
            authors=["Failed Author"],
            abstract="Test failed download",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/failed",
            arxiv_id="2301.00000",
        )

        # Mock network failure
        mock_requests_get.side_effect = requests.RequestException("Download failed")

        # Act: Attempt download
        service = PaperDownloadService()
        result_path = service.download_single_paper(paper)

        # Assert: Should return None for failure
        assert result_path is None

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    def test_download_single_paper_with_custom_output_dir(self, mock_mkdir):
        """Test single paper download with custom output directory."""
        # Arrange: Create test paper and custom directory
        paper = ResearchPaper(
            title="Custom Dir Paper",
            authors=["Custom Author"],
            abstract="Test custom directory",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/custom",
            # No PDF URL to test early return
        )
        custom_dir = Path("/custom/download/dir")

        # Act: Attempt download with custom directory
        service = PaperDownloadService()
        result_path = service.download_single_paper(paper, custom_dir)

        # Assert: Should return None (no PDF URL) but use custom directory
        assert result_path is None


class TestPaperDownloadServiceFileManagement:
    """
    Test file management functionality including naming and organization.

    Educational Note:
    File management is crucial for research tools. These tests show proper
    filename sanitization, directory structure, and organization patterns.
    """

    @patch("src.domain.services.paper_download_service.datetime")
    def test_create_output_directory_structure(self, mock_datetime):
        """Test creation of organized output directory structure."""
        # Arrange: Mock current date
        mock_now = datetime(2025, 8, 5, 10, 30, 0)
        mock_datetime.now.return_value = mock_now

        # Act: Create output directory
        service = PaperDownloadService()
        with patch.object(Path, "mkdir") as mock_mkdir:
            output_dir = service._create_output_directory("test_strategy")

        # Assert: Verify directory structure
        expected_name = "2025-08-05_test_strategy"
        assert expected_name in str(output_dir)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_sanitize_filename_removes_problematic_characters(self):
        """
        Test filename sanitization for cross-platform compatibility.

        Educational Note:
        Different operating systems have different filename restrictions.
        Sanitization ensures files work across Windows, macOS, and Linux.
        """
        service = PaperDownloadService()

        # Test various problematic characters
        test_cases = [
            ("Normal Title", "Normal_Title"),
            ("Title: With Colon", "Title__With_Colon"),
            ("Title/With\\Slash", "Title_With_Slash"),
            ("Title*With?Special|Chars<>", "Title_With_Special_Chars__"),
            ("   Extra   Spaces   ", "Extra_Spaces"),
        ]

        for input_title, expected in test_cases:
            result = service._sanitize_filename(input_title)
            assert result == expected

    def test_sanitize_filename_limits_length(self):
        """Test that very long filenames are truncated appropriately."""
        service = PaperDownloadService()

        # Create very long title
        long_title = "A" * 150  # 150 characters
        result = service._sanitize_filename(long_title)

        # Should be truncated to 100 characters with ellipsis
        assert len(result) == 100
        assert result.endswith("...")

    def test_get_pdf_url_from_arxiv_id(self):
        """Test PDF URL generation from arXiv ID."""
        service = PaperDownloadService()

        # Create paper with arXiv ID
        paper = Mock()
        paper.arxiv_id = "2301.12345"

        # Simulate hasattr behavior
        def mock_hasattr(obj, attr):
            return attr == "arxiv_id"

        with patch("builtins.hasattr", side_effect=mock_hasattr):
            url = service._get_pdf_url(paper)

        assert url == "https://arxiv.org/pdf/2301.12345.pdf"

    def test_get_pdf_url_from_pdf_url_field(self):
        """Test PDF URL extraction from existing pdf_url field."""
        service = PaperDownloadService()

        # Create paper with direct PDF URL
        paper = Mock()
        paper.pdf_url = "https://example.com/paper.pdf"

        def mock_hasattr(obj, attr):
            return attr == "pdf_url"

        with patch("builtins.hasattr", side_effect=mock_hasattr):
            url = service._get_pdf_url(paper)

        assert url == "https://example.com/paper.pdf"

    def test_get_pdf_url_returns_none_for_no_source(self):
        """Test PDF URL extraction when no URL source is available."""
        service = PaperDownloadService()

        # Create paper without PDF sources
        paper = Mock()

        def mock_hasattr(obj, attr):
            return False  # No pdf_url or arxiv_id

        with patch("builtins.hasattr", side_effect=mock_hasattr):
            url = service._get_pdf_url(paper)

        assert url is None


class TestPaperDownloadServiceMetadata:
    """
    Test metadata generation and persistence functionality.

    Educational Note:
    Metadata is crucial for research workflows. It enables searchability,
    reproducibility, and proper citation of downloaded papers.
    """

    @patch("builtins.open", mock_open())
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_save_metadata_complete_information(self, mock_json_dump):
        """Test metadata generation with complete paper information."""
        # Arrange: Create test papers with full metadata
        paper1 = ResearchPaper(
            title="Complete Paper 1",
            authors=["Author A", "Author B"],
            abstract="First complete paper for metadata test",
            publication_date=datetime(2023, 1, 15, tzinfo=timezone.utc),
            doi="10.1000/complete1",
            venue="Test Journal",
            citation_count=42,
            keywords=["keyword1", "keyword2"],
            arxiv_id="2301.12345",
        )

        papers = [paper1]
        output_dir = Path("/test/output")
        strategy_name = "test_metadata_strategy"

        # Act: Save metadata
        service = PaperDownloadService()
        service._save_metadata(papers, output_dir, strategy_name)

        # Assert: Verify metadata structure
        mock_json_dump.assert_called_once()
        call_args = mock_json_dump.call_args[0][0]  # First argument to json.dump

        # Check download_info section
        assert "download_info" in call_args
        download_info = call_args["download_info"]
        assert download_info["strategy_name"] == strategy_name
        assert download_info["total_papers"] == 1
        assert download_info["download_directory"] == str(output_dir)
        assert "timestamp" in download_info

        # Check papers section
        assert "papers" in call_args
        papers_data = call_args["papers"]
        assert len(papers_data) == 1

        paper_data = papers_data[0]
        assert paper_data["title"] == "Complete Paper 1"
        assert paper_data["authors"] == ["Author A", "Author B"]
        assert paper_data["doi"] == "10.1000/complete1"
        assert paper_data["arxiv_id"] == "2301.12345"

    @patch("builtins.open", mock_open())
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_save_metadata_minimal_information(self, mock_json_dump):
        """Test metadata generation with minimal paper information."""
        # Arrange: Create paper with minimal required fields
        paper = ResearchPaper(
            title="Minimal Paper",
            authors=["Single Author"],
            abstract="Minimal abstract",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/minimal",
        )

        # Act: Save metadata
        service = PaperDownloadService()
        service._save_metadata([paper], Path("/test"), "minimal_strategy")

        # Assert: Should handle minimal data gracefully
        mock_json_dump.assert_called_once()
        call_args = mock_json_dump.call_args[0][0]

        paper_data = call_args["papers"][0]
        assert paper_data["title"] == "Minimal Paper"
        assert "arxiv_id" not in paper_data or paper_data["arxiv_id"] is None


class TestPaperDownloadServiceSummaryAndReporting:
    """
    Test download summary and reporting functionality.

    Educational Note:
    Progress reporting and result summaries help users understand
    the success rate of their downloads and identify potential issues.
    """

    def test_get_download_summary_all_successful(self):
        """Test summary generation for completely successful downloads."""
        service = PaperDownloadService()

        results = {
            "Paper 1": "/path/to/paper1.pdf",
            "Paper 2": "/path/to/paper2.pdf",
            "Paper 3": "/path/to/paper3.pdf",
        }

        summary = service.get_download_summary(results)

        assert summary["total_attempted"] == 3
        assert summary["successful_downloads"] == 3
        assert summary["failed_downloads"] == 0
        assert summary["success_rate"] == 100.0

    def test_get_download_summary_mixed_results(self):
        """Test summary generation for mixed success/failure results."""
        service = PaperDownloadService()

        results = {
            "Success Paper": "/path/to/success.pdf",
            "Failed Paper 1": "Download failed - Network timeout",
            "Another Success": "/path/to/another.pdf",
            "Failed Paper 2": "Download failed - No PDF URL available",
        }

        summary = service.get_download_summary(results)

        assert summary["total_attempted"] == 4
        assert summary["successful_downloads"] == 2
        assert summary["failed_downloads"] == 2
        assert summary["success_rate"] == 50.0

    def test_get_download_summary_all_failed(self):
        """Test summary generation for completely failed downloads."""
        service = PaperDownloadService()

        results = {
            "Failed Paper 1": "Download failed - Network error",
            "Failed Paper 2": "Download failed - File not found",
        }

        summary = service.get_download_summary(results)

        assert summary["total_attempted"] == 2
        assert summary["successful_downloads"] == 0
        assert summary["failed_downloads"] == 2
        assert summary["success_rate"] == 0.0

    def test_get_download_summary_empty_results(self):
        """Test summary generation for empty results."""
        service = PaperDownloadService()

        results = {}
        summary = service.get_download_summary(results)

        assert summary["total_attempted"] == 0
        assert summary["successful_downloads"] == 0
        assert summary["failed_downloads"] == 0
        assert summary["success_rate"] == 0  # Should handle division by zero


class TestPaperDownloadServiceErrorHandling:
    """
    Test comprehensive error handling across different failure modes.

    Educational Note:
    Robust error handling is essential for research tools that depend on
    external resources (network, file system, remote APIs). Users need
    clear feedback about what went wrong and how to address issues.
    """

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    @patch("builtins.open")
    def test_download_handles_file_write_errors(
        self, mock_open, mock_requests_get, mock_mkdir
    ):
        """Test handling of file system errors during download."""
        # Arrange: Mock successful HTTP response but file write error
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"content"]
        mock_requests_get.return_value = mock_response

        # Mock file write error
        mock_open.side_effect = IOError("Disk full")

        paper = ResearchPaper(
            title="File Error Paper",
            authors=["Error Author"],
            abstract="Test file error",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/file_error",
            arxiv_id="2301.00001",
        )

        # Act: Attempt download
        service = PaperDownloadService()
        result_path = service._download_paper_pdf(paper, Path("/test"))

        # Assert: Should handle file error gracefully
        assert result_path is None

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    def test_download_handles_http_errors(self, mock_requests_get, mock_mkdir):
        """Test handling of HTTP errors (404, 500, etc.)."""
        # Arrange: Mock HTTP error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_requests_get.return_value = mock_response

        paper = ResearchPaper(
            title="HTTP Error Paper",
            authors=["HTTP Author"],
            abstract="Test HTTP error",
            publication_date=datetime.now(timezone.utc),
            doi="10.1000/http_error",
            arxiv_id="2301.00002",
        )

        # Act: Attempt download
        service = PaperDownloadService()
        result_path = service._download_paper_pdf(paper, Path("/test"))

        # Assert: Should handle HTTP error gracefully
        assert result_path is None
