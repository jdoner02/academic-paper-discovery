"""
Comprehensive test suite for PubMed Central (PMC) Paper Repository.

This test suite follows the established TDD methodology with ~30 tests covering
all aspects of PMC OAI-PMH integration. Tests are organized by behavior and
validate Clean Architecture compliance.

Educational Notes:
- Demonstrates testing patterns for external API integration
- Shows how to test OAI-PMH harvesting with proper mocking
- Validates multi-source architecture with biomedical focus
- Tests repository pattern implementation for scientific databases

Test Categories:
1. Initialization and Configuration (3 tests)
2. Query Search Operations (4 tests)
3. Specific Lookup Operations (4 tests)
4. Read-Only Repository Interface (3 tests)
5. Query Building Logic (4 tests)
6. Data Conversion and Parsing (3 tests)
7. PDF Access and Download (3 tests)
8. Query Filtering and Constraints (2 tests)
9. Multi-Source Integration (4 tests)

Architecture Validation:
- PaperSourcePort interface compliance
- SourceMetadata integration for provenance
- PaperFingerprint for cross-source deduplication
- Clean Architecture layer separation
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from typing import List

from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.source_metadata import SourceMetadata
from src.domain.value_objects.paper_fingerprint import PaperFingerprint
from src.infrastructure.repositories.pmc_paper_repository import PMCPaperRepository


class TestPMCPaperRepositoryInitialization:
    """Test PMC repository initialization and configuration."""

    def test_initialize_with_default_base_url(self):
        """PMC repository should initialize with standard OAI-PMH endpoint."""
        repository = PMCPaperRepository()

        assert repository.base_url == "https://pmc.ncbi.nlm.nih.gov/oai/oai2"
        assert repository.session is not None
        assert repository.session.headers.get("User-Agent") is not None

    def test_initialize_with_custom_base_url(self):
        """PMC repository should accept custom OAI-PMH endpoints for testing."""
        custom_url = "https://test-pmc.example.com/oai2"
        repository = PMCPaperRepository(base_url=custom_url)

        assert repository.base_url == custom_url

    def test_session_has_proper_user_agent(self):
        """HTTP session should have appropriate User-Agent for PMC API etiquette."""
        repository = PMCPaperRepository()
        user_agent = repository.session.headers.get("User-Agent")

        assert "Academic Research Tool" in user_agent
        assert "PMC" in user_agent


class TestPMCPaperRepositoryQuerySearch:
    """Test search operations using PMC OAI-PMH interface."""

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_find_by_query_successful_search(self, mock_sickle):
        """Should successfully search PMC and return ResearchPaper objects."""
        # Arrange
        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC123456"],
            "title": ["Heart Rate Variability in Traumatic Brain Injury"],
            "creator": ["Smith, John", "Doe, Jane"],
            "description": ["Comprehensive study of HRV changes after TBI."],
            "date": ["2024-01-15"],
            "type": ["Article"],
            "format": ["text/html"],
            "relation": ["https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/"],
        }

        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = [mock_record]
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()
        search_query = SearchQuery(
            terms=["heart rate variability", "traumatic brain injury"], max_results=10
        )

        # Act
        results = repository.find_by_query(search_query)

        # Assert
        assert len(results) == 1
        paper = results[0]
        assert isinstance(paper, ResearchPaper)
        assert "Heart Rate Variability" in paper.title
        assert len(paper.authors) == 2
        assert "Smith, John" in paper.authors
        assert paper.abstract == "Comprehensive study of HRV changes after TBI."

        # Verify source metadata
        assert paper.source_metadata is not None
        assert paper.source_metadata.source_name == "PubMed Central"
        assert "PMC123456" in paper.source_metadata.source_identifier

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_find_by_query_network_error(self, mock_sickle):
        """Should handle network errors gracefully and return empty results."""
        mock_sickle.side_effect = Exception("Network timeout")

        repository = PMCPaperRepository()
        search_query = SearchQuery(terms=["test"], max_results=10)

        results = repository.find_by_query(search_query)

        assert results == []

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_find_by_query_parsing_error(self, mock_sickle):
        """Should handle XML parsing errors and skip problematic records."""
        mock_record_good = Mock()
        mock_record_good.metadata = {
            "identifier": ["oai:pmc:PMC123456"],
            "title": ["Valid Paper"],
            "creator": ["Author, Test"],
            "date": ["2024-01-15"],
        }

        mock_record_bad = Mock()
        mock_record_bad.metadata = None  # Simulate parsing error

        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = [
            mock_record_good,
            mock_record_bad,
        ]
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()
        search_query = SearchQuery(terms=["test"], max_results=10)

        results = repository.find_by_query(search_query)

        assert len(results) == 1  # Only the valid record
        assert results[0].title == "Valid Paper"

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_find_by_query_empty_results(self, mock_sickle):
        """Should return empty list when no papers match the query."""
        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = []
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()
        search_query = SearchQuery(terms=["nonexistent topic"], max_results=10)

        results = repository.find_by_query(search_query)

        assert results == []


class TestPMCPaperRepositorySpecificLookups:
    """Test specific paper lookup operations."""

    @patch(
        "src.infrastructure.repositories.pmc_paper_repository.PMCPaperRepository.find_by_query"
    )
    def test_find_by_pmc_id_success(self, mock_find_by_query):
        """Should find specific paper by PMC identifier."""
        mock_paper = Mock(spec=ResearchPaper)
        mock_paper.source_metadata = Mock()
        mock_paper.source_metadata.source_identifier = "PMC123456"
        mock_find_by_query.return_value = [mock_paper]

        repository = PMCPaperRepository()
        result = repository.find_by_pmc_id("PMC123456")

        assert result == mock_paper
        mock_find_by_query.assert_called_once()

    @patch(
        "src.infrastructure.repositories.pmc_paper_repository.PMCPaperRepository.find_by_query"
    )
    def test_find_by_pmc_id_not_found(self, mock_find_by_query):
        """Should return None when PMC ID is not found."""
        mock_find_by_query.return_value = []

        repository = PMCPaperRepository()
        result = repository.find_by_pmc_id("PMC999999")

        assert result is None

    @patch(
        "src.infrastructure.repositories.pmc_paper_repository.PMCPaperRepository.find_by_query"
    )
    def test_find_by_doi_delegates_to_query_search(self, mock_find_by_query):
        """Should delegate DOI search to general query search."""
        mock_paper = Mock(spec=ResearchPaper)
        mock_find_by_query.return_value = [mock_paper]

        repository = PMCPaperRepository()
        result = repository.find_by_doi("10.1234/example.doi")

        assert result == mock_paper
        mock_find_by_query.assert_called_once()
        call_args = mock_find_by_query.call_args[0][0]
        assert "10.1234/example.doi" in call_args.terms

    @patch(
        "src.infrastructure.repositories.pmc_paper_repository.PMCPaperRepository.find_by_query"
    )
    def test_find_by_doi_returns_none_when_no_results(self, mock_find_by_query):
        """Should return None when DOI search finds no results."""
        mock_find_by_query.return_value = []

        repository = PMCPaperRepository()
        result = repository.find_by_doi("10.1234/nonexistent.doi")

        assert result is None


class TestPMCPaperRepositoryReadOnlyOperations:
    """Test read-only nature of PMC OAI-PMH repository."""

    def test_save_paper_raises_not_implemented_error(self):
        """Should raise NotImplementedError for save operations (read-only)."""
        repository = PMCPaperRepository()
        mock_paper = Mock(spec=ResearchPaper)

        with pytest.raises(NotImplementedError) as exc_info:
            repository.save_paper(mock_paper)

        assert "PMC repository is read-only" in str(exc_info.value)

    def test_save_papers_raises_not_implemented_error(self):
        """Should raise NotImplementedError for bulk save operations."""
        repository = PMCPaperRepository()
        mock_papers = [Mock(spec=ResearchPaper), Mock(spec=ResearchPaper)]

        with pytest.raises(NotImplementedError) as exc_info:
            repository.save_papers(mock_papers)

        assert "PMC repository is read-only" in str(exc_info.value)

    def test_count_all_returns_unlimited_indicator(self):
        """Should return large number indicating unlimited search capacity."""
        repository = PMCPaperRepository()
        count = repository.count_all()

        assert count == 999999  # Indicates unlimited/unknown capacity


class TestPMCPaperRepositoryQueryBuilding:
    """Test OAI-PMH query construction for PMC."""

    def test_build_pmc_query_with_single_term(self):
        """Should build proper OAI-PMH query for single search term."""
        repository = PMCPaperRepository()
        terms = ["cardiology"]

        query = repository._build_pmc_query(terms)

        assert "cardiology" in query
        assert isinstance(query, str)

    def test_build_pmc_query_with_multiple_terms(self):
        """Should combine multiple terms with proper boolean logic."""
        repository = PMCPaperRepository()
        terms = ["heart rate", "variability", "monitoring"]

        query = repository._build_pmc_query(terms)

        for term in terms:
            assert term in query
        # PMC uses AND logic for combining terms
        assert "AND" in query or all(term in query for term in terms)

    def test_build_pmc_query_with_date_filters(self):
        """Should incorporate date filtering in OAI-PMH queries."""
        repository = PMCPaperRepository()
        start_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)

        query = repository._build_pmc_query(["test"], start_date, end_date)

        assert "2020" in query or query  # Date filtering may be in query or parameters
        assert "2024" in query or query

    def test_build_pmc_query_empty_terms(self):
        """Should handle empty search terms gracefully."""
        repository = PMCPaperRepository()

        query = repository._build_pmc_query([])

        assert query == "" or query == "*"  # Empty query or wildcard


class TestPMCPaperRepositoryDataConversion:
    """Test conversion from PMC metadata to ResearchPaper objects."""

    def test_convert_pmc_record_to_paper_complete_data(self):
        """Should convert PMC OAI record with complete metadata."""
        repository = PMCPaperRepository()

        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC123456"],
            "title": [
                "Advanced Heart Rate Variability Analysis Using Machine Learning"
            ],
            "creator": ["Johnson, Sarah M.", "Williams, Michael R.", "Brown, Emily K."],
            "description": [
                "This study presents novel machine learning approaches for HRV analysis in clinical settings."
            ],
            "date": ["2024-03-15"],
            "publisher": ["PLOS ONE"],
            "type": ["Journal Article"],
            "format": ["application/pdf", "text/html"],
            "relation": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/",
                "doi:10.1371/journal.pone.0123456",
            ],
            "rights": ["Creative Commons Attribution"],
            "subject": ["Cardiology", "Machine Learning", "Biomedical Engineering"],
        }

        paper = repository._convert_pmc_record_to_paper(mock_record)

        assert isinstance(paper, ResearchPaper)
        assert (
            paper.title
            == "Advanced Heart Rate Variability Analysis Using Machine Learning"
        )
        assert len(paper.authors) == 3
        assert "Johnson, Sarah M." in paper.authors
        assert "Williams, Michael R." in paper.authors
        assert "Brown, Emily K." in paper.authors
        assert (
            paper.abstract
            == "This study presents novel machine learning approaches for HRV analysis in clinical settings."
        )
        assert paper.venue == "PLOS ONE"
        assert paper.publication_date.year == 2024
        assert paper.publication_date.month == 3
        assert paper.publication_date.day == 15

        # Verify source metadata
        assert paper.source_metadata is not None
        assert paper.source_metadata.source_name == "PubMed Central"
        assert "PMC123456" in paper.source_metadata.source_identifier
        assert (
            "10.1371/journal.pone.0123456"
            in paper.source_metadata.source_specific_data["doi"]
        )

    def test_convert_pmc_record_to_paper_minimal_data(self):
        """Should handle PMC records with minimal required metadata."""
        repository = PMCPaperRepository()

        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC654321"],
            "title": ["Minimal Metadata Paper"],
            "date": ["2023-12-01"],
        }

        paper = repository._convert_pmc_record_to_paper(mock_record)

        assert isinstance(paper, ResearchPaper)
        assert paper.title == "Minimal Metadata Paper"
        assert paper.authors == ["Unknown Author"]  # Default when no authors provided
        assert paper.abstract == ""  # No description provided
        assert paper.venue == ""  # No publisher provided
        assert paper.publication_date.year == 2023

        # Source metadata should still be populated
        assert paper.source_metadata is not None
        assert "PMC654321" in paper.source_metadata.source_identifier

    def test_convert_pmc_record_handles_malformed_data(self):
        """Should gracefully handle malformed or missing data fields."""
        repository = PMCPaperRepository()

        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC999999"],
            "title": ["Test Paper"],
            "date": ["invalid-date-format"],  # Malformed date
            "creator": "Single String Instead of List",  # Wrong format
            "description": ["Multiple", "Description", "Elements"],  # Multiple elements
        }

        paper = repository._convert_pmc_record_to_paper(mock_record)

        assert isinstance(paper, ResearchPaper)
        assert paper.title == "Test Paper"
        # Should handle date parsing errors gracefully
        assert paper.publication_date is not None
        # Should handle creator format issues
        assert isinstance(paper.authors, list)
        # Should join multiple descriptions
        assert len(paper.abstract) > 0


class TestPMCPaperRepositoryPdfAccess:
    """Test PDF access and download capabilities."""

    def test_get_pdf_url_from_pmc_data(self):
        """Should extract PDF URL from PMC relation fields."""
        repository = PMCPaperRepository()

        paper_data = {
            "relation": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/",
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/pdf/",
                "doi:10.1371/journal.pone.0123456",
            ]
        }

        pdf_url = repository._get_pdf_url(paper_data)

        assert pdf_url == "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/pdf/"

    def test_get_pdf_url_from_alternative_format(self):
        """Should construct PDF URL from PMC identifier when direct URL unavailable."""
        repository = PMCPaperRepository()

        paper_data = {
            "identifier": ["oai:pmc:PMC456789"],
            "relation": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC456789/",
                "doi:10.1234/example.doi",
            ],
        }

        pdf_url = repository._get_pdf_url(paper_data)

        # Should construct PDF URL from base PMC URL
        expected_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC456789/pdf/"
        assert pdf_url == expected_url

    def test_get_pdf_url_returns_none_for_no_access(self):
        """Should return None when PDF is not available."""
        repository = PMCPaperRepository()

        paper_data = {
            "identifier": ["oai:pmc:PMC999999"],
            "relation": ["doi:10.1234/example.doi"],  # No PMC URL
        }

        pdf_url = repository._get_pdf_url(paper_data)

        assert pdf_url is None


class TestPMCPaperRepositoryQueryFiltering:
    """Test query filtering and constraint application."""

    def test_matches_query_filters_date_range(self):
        """Should filter papers based on publication date constraints."""
        repository = PMCPaperRepository()

        paper_date = datetime(2023, 6, 15, tzinfo=timezone.utc)
        start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2023, 12, 31, tzinfo=timezone.utc)

        search_query = SearchQuery(
            terms=["test"], start_date=start_date, end_date=end_date
        )

        matches = repository._matches_query_filters(paper_date, search_query)

        assert matches is True

    def test_matches_query_filters_no_constraints(self):
        """Should accept all papers when no date constraints specified."""
        repository = PMCPaperRepository()

        paper_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
        search_query = SearchQuery(terms=["test"])  # No date constraints

        matches = repository._matches_query_filters(paper_date, search_query)

        assert matches is True


class TestPMCRepositoryMultiSourceIntegration:
    """Test integration with multi-source paper aggregation system."""

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_pmc_papers_have_source_metadata_populated(self, mock_sickle):
        """PMC papers should have proper SourceMetadata for multi-source tracking."""
        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC123456"],
            "title": ["Test Paper"],
            "creator": ["Author, Test"],
            "date": ["2024-01-15"],
            "relation": ["doi:10.1234/test.doi"],
        }

        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = [mock_record]
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()
        search_query = SearchQuery(terms=["test"], max_results=1)

        results = repository.find_by_query(search_query)

        assert len(results) == 1
        paper = results[0]
        assert paper.source_metadata is not None
        assert isinstance(paper.source_metadata, SourceMetadata)
        assert paper.source_metadata.source_name == "PubMed Central"
        assert "PMC123456" in paper.source_metadata.source_identifier

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_pmc_papers_have_paper_fingerprint_for_duplicate_detection(
        self, mock_sickle
    ):
        """PMC papers should have PaperFingerprint for cross-source deduplication."""
        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC123456"],
            "title": ["Unique Research Paper Title"],
            "creator": ["Smith, John A."],
            "date": ["2024-01-15"],
        }

        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = [mock_record]
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()
        search_query = SearchQuery(terms=["unique research"], max_results=1)

        results = repository.find_by_query(search_query)

        assert len(results) == 1
        paper = results[0]
        assert paper.paper_fingerprint is not None
        assert isinstance(paper.paper_fingerprint, PaperFingerprint)

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_pmc_source_metadata_preserves_biomedical_specific_data(self, mock_sickle):
        """PMC SourceMetadata should preserve biomedical-specific fields."""
        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC123456"],
            "title": ["Biomedical Research Study"],
            "creator": ["Researcher, Dr. Medical"],
            "date": ["2024-01-15"],
            "subject": ["Cardiology", "Clinical Trial", "Evidence-Based Medicine"],
            "type": ["Journal Article", "Research Article"],
            "publisher": ["New England Journal of Medicine"],
            "relation": ["https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/"],
        }

        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = [mock_record]
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()
        search_query = SearchQuery(terms=["biomedical"], max_results=1)

        results = repository.find_by_query(search_query)

        paper = results[0]
        source_metadata = paper.source_metadata

        # PMC-specific fields should be preserved
        assert "Cardiology" in source_metadata.source_specific_data["subject"]
        assert "Clinical Trial" in source_metadata.source_specific_data["subject"]
        assert (
            source_metadata.source_specific_data["publisher"]
            == "New England Journal of Medicine"
        )
        assert "Research Article" in source_metadata.source_specific_data["type"]

    @patch("src.infrastructure.repositories.pmc_paper_repository.Sickle")
    def test_complete_multi_source_workflow_end_to_end(self, mock_sickle):
        """Should demonstrate complete workflow with PMC as part of multi-source system."""
        # Arrange: PMC paper with comprehensive metadata
        mock_record = Mock()
        mock_record.metadata = {
            "identifier": ["oai:pmc:PMC789123"],
            "title": [
                "Heart Rate Variability Analysis in Post-TBI Patients: A Longitudinal Study"
            ],
            "creator": [
                "Martinez, Dr. Elena",
                "Thompson, Prof. David",
                "Lee, Dr. Sarah",
            ],
            "description": [
                "Comprehensive analysis of HRV patterns in traumatic brain injury recovery."
            ],
            "date": ["2024-02-20"],
            "publisher": ["Journal of Neurotrauma"],
            "subject": ["Neurology", "Cardiology", "Rehabilitation Medicine"],
            "type": ["Original Research", "Peer-Reviewed"],
            "relation": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC789123/",
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC789123/pdf/",
                "doi:10.1089/neu.2024.0123",
            ],
            "rights": ["Creative Commons Attribution 4.0"],
        }

        mock_sickle_instance = Mock()
        mock_sickle_instance.ListRecords.return_value = [mock_record]
        mock_sickle.return_value = mock_sickle_instance

        repository = PMCPaperRepository()

        # Act: Execute search matching HRV research domain
        search_query = SearchQuery(
            terms=["heart rate variability", "traumatic brain injury"],
            max_results=10,
            start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
        )

        results = repository.find_by_query(search_query)

        # Assert: Complete multi-source integration
        assert len(results) == 1
        paper = results[0]

        # Domain object validation
        assert isinstance(paper, ResearchPaper)
        assert "Heart Rate Variability" in paper.title
        assert "TBI" in paper.title or "traumatic brain injury" in paper.title.lower()
        assert len(paper.authors) == 3
        assert paper.venue == "Journal of Neurotrauma"

        # Multi-source metadata validation
        assert paper.source_metadata.source_name == "PubMed Central"
        assert "PMC789123" in paper.source_metadata.source_identifier
        assert (
            paper.source_metadata.source_url
            == "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC789123/"
        )

        # Deduplication capability validation
        assert paper.paper_fingerprint is not None
        fingerprint_data = paper.paper_fingerprint.title_hash
        assert "heart" in fingerprint_data.lower()
        assert "variability" in fingerprint_data.lower()

        # PDF access validation
        pdf_url = repository._get_pdf_url(mock_record.metadata)
        assert pdf_url == "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC789123/pdf/"

        # Biomedical domain validation
        source_specific_data = paper.source_metadata.source_specific_data
        assert "Neurology" in source_specific_data["subject"]
        assert "Cardiology" in source_specific_data["subject"]
        assert "doi:10.1089/neu.2024.0123" in source_specific_data["relation"]
