"""
Integration tests for domain services with entities and value objects.

These tests validate that domain services properly coordinate with entities
and value objects to implement complex business operations. They focus on
business logic integration without external dependencies.

Educational Notes:
- Domain services orchestrate business operations across multiple entities
- They maintain domain invariants and business rules
- Integration tests validate coordination between domain objects
- Focus on business logic rather than technical infrastructure

Design Patterns Tested:
- Domain Service Pattern: Complex business operations
- Entity coordination: Identity-based object interactions
- Value Object composition: Immutable domain concepts
- Business rule enforcement: Domain invariant validation
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, patch, mock_open

from src.domain.services.paper_download_service import PaperDownloadService
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.keyword_config import KeywordConfig, SearchStrategy


class TestPaperDownloadServiceDomainIntegration:
    """
    Test integration between PaperDownloadService and domain entities.

    Educational Note:
    These tests validate that domain services properly work with entities
    and value objects to implement business operations while maintaining
    domain invariants and business rules.
    """

    @pytest.fixture
    def sample_papers(self):
        """Create sample research papers for download testing."""
        return [
            ResearchPaper(
                title="Cybersecurity in Cloud Computing",
                authors=["Dr. Alice Johnson", "Prof. Bob Smith"],
                abstract="Comprehensive analysis of cybersecurity challenges in cloud computing environments.",
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                doi="10.1000/cloud.2023.001",
                arxiv_id="2306.12345",
                citation_count=45,
                keywords=["cybersecurity", "cloud computing"],
            ),
            ResearchPaper(
                title="Machine Learning for Threat Detection",
                authors=["Dr. Carol Zhang"],
                abstract="Novel machine learning approaches for detecting cybersecurity threats in real-time.",
                publication_date=datetime(2023, 8, 20, tzinfo=timezone.utc),
                doi="10.1000/ml.2023.002",
                arxiv_id="2308.67890",
                citation_count=32,
                keywords=["machine learning", "threat detection"],
            ),
        ]

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    @patch("builtins.open", mock_open())
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_download_service_entity_integration(
        self, mock_json_dump, mock_requests_get, mock_mkdir, sample_papers
    ):
        """
        Test that download service properly integrates with ResearchPaper entities.

        Educational Note:
        This test validates that domain services can work with entities to
        implement complex business operations while respecting entity
        boundaries and maintaining business invariants.
        """
        # Arrange: Mock successful HTTP response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"PDF content chunk"]
        mock_requests_get.return_value = mock_response

        # Create download service
        download_service = PaperDownloadService()

        # Act: Download papers using entity data
        results = download_service.download_papers(
            papers=sample_papers, strategy_name="test_strategy"
        )

        # Assert: Service should work with entity attributes
        assert len(results) == 2
        assert "Cybersecurity in Cloud Computing" in results
        assert "Machine Learning for Threat Detection" in results

        # Verify that entity data was used for file naming
        for paper_title, result_path in results.items():
            if not result_path.startswith("Download failed"):
                # Should use sanitized version of entity title
                sanitized_title = paper_title.replace(" ", "_")
                assert sanitized_title in result_path

        # Verify metadata generation used entity attributes
        mock_json_dump.assert_called_once()
        metadata = mock_json_dump.call_args[0][0]

        # Should include entity information
        assert "papers" in metadata
        paper_metadata = metadata["papers"]
        assert len(paper_metadata) == 2

        # Check that entity attributes were preserved
        titles = [paper["title"] for paper in paper_metadata]
        assert "Cybersecurity in Cloud Computing" in titles
        assert "Machine Learning for Threat Detection" in titles

    def test_filename_sanitization_with_entity_titles(self, sample_papers):
        """
        Test filename sanitization using real entity title data.

        Educational Note:
        This test shows how domain services must handle the variability
        in entity data while maintaining business rules (safe filenames).
        """
        download_service = PaperDownloadService()

        # Test sanitization with actual entity titles
        for paper in sample_papers:
            sanitized = download_service._sanitize_filename(paper.title)

            # Should be safe for file system
            assert "/" not in sanitized
            assert "\\" not in sanitized
            assert ":" not in sanitized

            # Should preserve meaningful content
            assert len(sanitized) > 0
            assert not sanitized.startswith(" ")
            assert not sanitized.endswith(" ")

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    def test_pdf_url_extraction_from_entities(self, mock_mkdir, sample_papers):
        """
        Test PDF URL extraction using entity data.

        Educational Note:
        This demonstrates how domain services extract data from entities
        according to business rules while handling missing or incomplete data.
        """
        download_service = PaperDownloadService()

        for paper in sample_papers:
            pdf_url = download_service._get_pdf_url(paper)

            if hasattr(paper, "arxiv_id") and paper.arxiv_id:
                # Should generate arXiv PDF URL from entity data
                expected_url = f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"
                assert pdf_url == expected_url
            else:
                # Should handle entities without PDF sources
                assert pdf_url is None

    def test_entity_data_preservation_in_metadata(self, sample_papers):
        """
        Test that entity data is properly preserved in metadata generation.

        Educational Note:
        Domain services must preserve entity integrity when transforming
        data for different purposes (like metadata serialization).
        """
        download_service = PaperDownloadService()

        # Create mock output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            with patch("builtins.open", mock_open()) as mock_file:
                with patch("json.dump") as mock_json_dump:
                    # Act: Generate metadata from entities
                    download_service._save_metadata(
                        papers=sample_papers,
                        output_dir=output_dir,
                        strategy_name="test_strategy",
                    )

                    # Assert: Entity data should be preserved
                    mock_json_dump.assert_called_once()
                    metadata = mock_json_dump.call_args[0][0]

                    # Check download info
                    assert metadata["download_info"]["total_papers"] == len(
                        sample_papers
                    )
                    assert metadata["download_info"]["strategy_name"] == "test_strategy"

                    # Check individual paper data preservation
                    papers_metadata = metadata["papers"]
                    assert len(papers_metadata) == len(sample_papers)

                    for i, paper_meta in enumerate(papers_metadata):
                        original_paper = sample_papers[i]

                        # Core entity attributes should be preserved
                        assert paper_meta["title"] == original_paper.title
                        assert paper_meta["authors"] == original_paper.authors
                        assert paper_meta["doi"] == original_paper.doi
                        assert paper_meta["arxiv_id"] == original_paper.arxiv_id


class TestSearchQueryValueObjectIntegration:
    """
    Test integration between SearchQuery value objects and other domain components.

    Educational Note:
    Value object integration tests ensure that immutable domain concepts
    work correctly with other domain objects and maintain their invariants.
    """

    def test_search_query_with_keyword_config_integration(self):
        """
        Test SearchQuery integration with KeywordConfig value objects.

        Educational Note:
        This test validates that value objects can work together to create
        complex domain behaviors while maintaining immutability and invariants.
        """
        # Arrange: Create search strategy and configuration
        strategy = SearchStrategy(
            name="cybersecurity_research",
            description="Cybersecurity research papers",
            primary_terms=["cybersecurity", "network security"],
            secondary_terms=["threat detection", "encryption"],
            excluded_terms=["tutorial"],
            max_results=100,
        )

        config = KeywordConfig(
            strategies=[strategy], default_strategy="cybersecurity_research"
        )

        # Act: Build search query from configuration
        search_query = strategy.build_search_query(
            start_year=2020, end_year=2024, min_citations=10
        )

        # Assert: Value objects should integrate correctly
        assert isinstance(search_query, SearchQuery)
        assert search_query.terms == tuple(strategy.get_all_terms())
        assert search_query.start_year == 2020
        assert search_query.end_year == 2024
        assert search_query.min_citations == 10

        # Verify value object immutability is maintained
        original_terms = search_query.terms
        assert search_query.terms is original_terms  # Same object reference

        # Should be usable in collections (hashable)
        query_set = {search_query}
        assert len(query_set) == 1

    def test_search_query_date_range_validation_integration(self):
        """
        Test SearchQuery date validation with real research scenarios.

        Educational Note:
        Value object integration includes validation that prevents invalid
        business states from being created or persisted.
        """
        # Valid query should work
        valid_query = SearchQuery(
            terms=["machine learning", "cybersecurity"],
            start_year=2020,
            end_year=2023,
            max_results=50,
        )

        # Test with research paper date filtering
        test_date = datetime(2022, 6, 15, tzinfo=timezone.utc)
        assert valid_query.is_within_date_range(test_date)

        # Edge cases should be handled correctly
        edge_start_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
        edge_end_date = datetime(2023, 12, 31, tzinfo=timezone.utc)
        assert valid_query.is_within_date_range(edge_start_date)
        assert valid_query.is_within_date_range(edge_end_date)

        # Outside range should be rejected
        too_early = datetime(2019, 12, 31, tzinfo=timezone.utc)
        too_late = datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert not valid_query.is_within_date_range(too_early)
        assert not valid_query.is_within_date_range(too_late)

    def test_value_object_equality_and_hashing_integration(self):
        """
        Test value object equality and hashing behavior in collections.

        Educational Note:
        Value objects must implement proper equality and hashing to work
        correctly in Python collections and enable deduplication.
        """
        # Create identical queries
        query1 = SearchQuery(
            terms=["cybersecurity", "AI"],
            start_year=2020,
            end_year=2024,
            max_results=100,
        )

        query2 = SearchQuery(
            terms=["cybersecurity", "AI"],
            start_year=2020,
            end_year=2024,
            max_results=100,
        )

        # Value objects should be equal based on values
        assert query1 == query2
        assert hash(query1) == hash(query2)

        # Should work in sets (deduplication)
        query_set = {query1, query2}
        assert len(query_set) == 1  # Deduplicated

        # Should work in dictionaries as keys
        query_dict = {query1: "result1", query2: "result2"}
        assert len(query_dict) == 1  # Same key
        assert query_dict[query1] == "result2"  # Last value wins


class TestDomainServiceEntityCoordination:
    """
    Test coordination between domain services and multiple entities.

    Educational Note:
    These tests validate complex business operations that span multiple
    domain objects while maintaining business invariants and rules.
    """

    def test_download_service_coordinates_multiple_entities(self):
        """
        Test that download service properly coordinates operations across multiple entities.

        Educational Note:
        Domain services often need to coordinate operations across multiple
        entities while maintaining consistency and business rules.
        """
        # Create entities with different characteristics
        papers = [
            ResearchPaper(
                title="Paper with arXiv ID",
                authors=["Author 1"],
                abstract="Has downloadable PDF",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                doi="10.1000/arxiv.2023.001",
                arxiv_id="2301.12345",
            ),
            ResearchPaper(
                title="Paper without PDF source",
                authors=["Author 2"],
                abstract="No downloadable PDF available",
                publication_date=datetime(2023, 2, 1, tzinfo=timezone.utc),
                doi="10.1000/nopdf.2023.002",
                # No arxiv_id or pdf_url
            ),
        ]

        download_service = PaperDownloadService()

        # Test URL extraction coordination
        paper_with_pdf = papers[0]
        paper_without_pdf = papers[1]

        pdf_url_1 = download_service._get_pdf_url(paper_with_pdf)
        pdf_url_2 = download_service._get_pdf_url(paper_without_pdf)

        # Should handle entities differently based on their data
        assert pdf_url_1 == "https://arxiv.org/pdf/2301.12345.pdf"
        assert pdf_url_2 is None

        # Should create appropriate filenames for all entities
        filename_1 = download_service._sanitize_filename(paper_with_pdf.title)
        filename_2 = download_service._sanitize_filename(paper_without_pdf.title)

        assert filename_1 == "Paper_with_arXiv_ID"
        assert filename_2 == "Paper_without_PDF_source"

    def test_business_rule_enforcement_across_entities(self, sample_papers):
        """
        Test that business rules are enforced consistently across entities.

        Educational Note:
        Domain services must enforce business rules consistently regardless
        of which specific entities they're working with.
        """
        download_service = PaperDownloadService()

        # Test filename length limits (business rule)
        long_title_paper = ResearchPaper(
            title="A" * 200,  # Very long title
            authors=["Test Author"],
            abstract="Test abstract",
            publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            doi="10.1000/long.2023.001",
        )

        sanitized_long = download_service._sanitize_filename(long_title_paper.title)
        assert len(sanitized_long) == 100  # Business rule: max 100 chars
        assert sanitized_long.endswith("...")  # Should indicate truncation

        # Test normal title (no truncation needed)
        normal_paper = sample_papers[0]
        sanitized_normal = download_service._sanitize_filename(normal_paper.title)
        assert len(sanitized_normal) < 100
        assert not sanitized_normal.endswith("...")

        # Business rule should be applied consistently
        assert isinstance(sanitized_long, str)
        assert isinstance(sanitized_normal, str)
        assert len(sanitized_long) <= 100
        assert len(sanitized_normal) <= 100
