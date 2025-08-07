"""
Test suite for MDPIPaperRepository - OAI-PMH implementation for MDPI journals.

This test suite validates the MDPI repository implementation that harvests papers
from MDPI's OAI-PMH endpoint (https://oai.mdpi.com/oai/oai2.php). MDPI publishes
numerous open access journals including Sensors, Mathematics, Electronics, and more.

Educational Notes:
- Tests written FIRST following TDD Red-Green-Refactor methodology
- Demonstrates testing of external API integrations with mocking
- Validates OAI-PMH protocol compliance and Dublin Core metadata handling
- Shows proper error handling for network and parsing failures
- Tests source-specific capabilities and metadata preservation

Testing Strategy:
- Mock external OAI-PMH calls to avoid dependency on live services
- Test both successful and error scenarios comprehensively
- Validate domain object creation from OAI-PMH Dublin Core metadata
- Ensure proper integration with multi-source architecture

OAI-PMH Context:
MDPI's OAI-PMH endpoint provides structured metadata in Dublin Core format,
with optional MODS for enhanced bibliographic information. Each journal
is available as a separate 'set' (e.g., 'journal:sensors', 'journal:mathematics').
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from typing import List, Optional

# Import domain objects and interfaces
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.source_metadata import SourceMetadata
from src.domain.value_objects.paper_fingerprint import PaperFingerprint
from src.application.ports.paper_source_port import PaperSourcePort

# Import the repository we're testing (will fail initially - RED phase)
from src.infrastructure.repositories.mdpi_paper_repository import MDPIPaperRepository


class TestMDPIPaperRepositoryInterface:
    """Test that MDPI repository properly implements PaperSourcePort interface."""

    def test_mdpi_repository_implements_paper_source_port(self):
        """Verify MDPI repository implements the PaperSourcePort interface."""
        repository = MDPIPaperRepository()
        assert isinstance(repository, PaperSourcePort)

    def test_mdpi_repository_has_all_required_methods(self):
        """Verify all abstract methods from PaperSourcePort are implemented."""
        repository = MDPIPaperRepository()

        # Test source identification methods
        assert hasattr(repository, "get_source_name")
        assert hasattr(repository, "get_source_capabilities")
        assert callable(getattr(repository, "get_source_name"))
        assert callable(getattr(repository, "get_source_capabilities"))

        # Test repository methods inherited from PaperRepositoryPort
        assert hasattr(repository, "find_by_query")
        assert hasattr(repository, "find_by_doi")
        assert hasattr(repository, "find_by_arxiv_id")
        assert hasattr(repository, "save_paper")
        assert hasattr(repository, "save_papers")
        assert hasattr(repository, "count_all")


class TestMDPIPaperRepositoryInitialization:
    """Test MDPI repository initialization and configuration."""

    def test_initialize_with_default_oai_endpoint(self):
        """Test repository initializes with correct default OAI-PMH endpoint."""
        repository = MDPIPaperRepository()
        assert repository.get_source_name() == "MDPI"
        # Should use the official MDPI OAI-PMH endpoint
        assert "oai.mdpi.com" in repository._base_url

    def test_initialize_with_custom_endpoint(self):
        """Test repository can be initialized with custom OAI-PMH endpoint."""
        custom_url = "https://test-oai.mdpi.com/oai/oai2.php"
        repository = MDPIPaperRepository(base_url=custom_url)
        assert repository._base_url == custom_url

    def test_default_journal_set_configuration(self):
        """Test repository has sensible default journal set configuration."""
        repository = MDPIPaperRepository()
        capabilities = repository.get_source_capabilities()

        # Should support multiple MDPI journals by default
        assert "supported_sets" in capabilities
        default_sets = capabilities["supported_sets"]
        assert "journal:sensors" in default_sets
        assert "journal:mathematics" in default_sets
        assert "journal:electronics" in default_sets


class TestMDPIPaperRepositorySourceCapabilities:
    """Test MDPI repository source identification and capabilities."""

    def test_get_source_name_returns_mdpi(self):
        """Test source name identification."""
        repository = MDPIPaperRepository()
        assert repository.get_source_name() == "MDPI"

    def test_get_source_capabilities_structure(self):
        """Test source capabilities return correct structure and values."""
        repository = MDPIPaperRepository()
        capabilities = repository.get_source_capabilities()

        # Required capability fields
        assert "full_text_access" in capabilities
        assert "metadata_quality" in capabilities
        assert "rate_limits" in capabilities
        assert "supported_search_fields" in capabilities
        assert "supported_sets" in capabilities

        # MDPI-specific capabilities
        assert (
            capabilities["full_text_access"] is True
        )  # MDPI provides open access PDFs
        assert capabilities["metadata_quality"] == "high"  # MDPI has good metadata
        assert "requests_per_second" in capabilities["rate_limits"]

    def test_supported_search_fields(self):
        """Test MDPI repository reports correct searchable fields."""
        repository = MDPIPaperRepository()
        capabilities = repository.get_source_capabilities()

        search_fields = capabilities["supported_search_fields"]
        # OAI-PMH typically supports these Dublin Core fields
        assert "title" in search_fields
        assert "creator" in search_fields
        assert "subject" in search_fields
        assert "description" in search_fields
        assert "date" in search_fields


class TestMDPIPaperRepositoryOAIHarvesting:
    """Test OAI-PMH harvesting functionality with mocked responses."""

    @patch("src.infrastructure.repositories.mdpi_paper_repository.Sickle")
    def test_find_by_query_successful_harvest(self, mock_sickle_class):
        """Test successful paper discovery using OAI-PMH ListRecords."""
        # Setup mock OAI-PMH response
        mock_sickle = Mock()
        mock_sickle_class.return_value = mock_sickle

        # Create mock OAI-PMH record in Dublin Core format
        mock_record = Mock()
        mock_record.header.identifier = "oai:mdpi.com:sensors-20-123456"
        mock_record.header.setSpec = ["journal:sensors"]
        mock_record.metadata = {
            "title": ["Heart Rate Variability Analysis in Wearable Sensors"],
            "creator": ["Smith, John", "Doe, Jane"],
            "subject": ["heart rate variability", "wearable sensors", "healthcare"],
            "description": [
                "This paper analyzes heart rate variability using modern wearable sensor technology."
            ],
            "date": ["2024-08-01"],
            "type": ["Text"],
            "identifier": ["https://doi.org/10.3390/s24123456"],
            "relation": ["https://www.mdpi.com/1424-8220/24/12/3456"],
            "coverage": [],
            "rights": ["© 2024 by the authors. Open access article."],
            "language": ["en"],
        }
        mock_sickle.ListRecords.return_value = [mock_record]

        # Test the search
        repository = MDPIPaperRepository(journal_sets=["journal:sensors"])
        query = SearchQuery(terms=["heart rate variability"])
        papers = repository.find_by_query(query)

        # Verify results
        assert len(papers) == 1
        paper = papers[0]
        assert isinstance(paper, ResearchPaper)
        assert "Heart Rate Variability" in paper.title
        assert "Smith, John" in paper.authors
        assert paper.doi == "10.3390/s24123456"

        # Verify source metadata is populated
        assert paper.source_metadata is not None
        assert paper.source_metadata.source_name == "MDPI"
        assert "sensors" in paper.source_metadata.source_specific_data["journal"]

    @patch("src.infrastructure.repositories.mdpi_paper_repository.Sickle")
    def test_find_by_query_with_journal_filtering(self, mock_sickle_class):
        """Test OAI-PMH harvesting with specific journal set filtering."""
        mock_sickle = Mock()
        mock_sickle_class.return_value = mock_sickle

        repository = MDPIPaperRepository(journal_sets=["journal:sensors"])
        query = SearchQuery(terms=["sensor technology"])
        repository.find_by_query(query)

        # Verify ListRecords was called with correct set parameter
        mock_sickle.ListRecords.assert_called_once()
        call_args = mock_sickle.ListRecords.call_args
        assert call_args[1]["set"] == "journal:sensors"

    @patch("src.infrastructure.repositories.mdpi_paper_repository.Sickle")
    def test_find_by_query_handles_oai_errors(self, mock_sickle_class):
        """Test proper error handling for OAI-PMH protocol errors."""
        from sickle.oaiexceptions import NoRecordsMatch, BadArgument

        mock_sickle = Mock()
        mock_sickle_class.return_value = mock_sickle
        mock_sickle.ListRecords.side_effect = NoRecordsMatch(
            "No records match the given criteria"
        )

        repository = MDPIPaperRepository()
        query = SearchQuery(terms=["nonexistent topic"])
        papers = repository.find_by_query(query)

        # Should return empty list, not raise exception
        assert papers == []

    @patch("src.infrastructure.repositories.mdpi_paper_repository.Sickle")
    def test_find_by_query_handles_network_errors(self, mock_sickle_class):
        """Test graceful handling of network connectivity issues."""
        import requests

        mock_sickle = Mock()
        mock_sickle_class.return_value = mock_sickle
        mock_sickle.ListRecords.side_effect = requests.exceptions.ConnectionError(
            "Network unreachable"
        )

        repository = MDPIPaperRepository()
        query = SearchQuery(terms=["any topic"])
        papers = repository.find_by_query(query)

        # Should return empty list and log error
        assert papers == []


class TestMDPIPaperRepositorySpecificLookups:
    """Test DOI and ArXiv ID lookups via OAI-PMH."""

    @patch("src.infrastructure.repositories.mdpi_paper_repository.Sickle")
    def test_find_by_doi_success(self, mock_sickle_class):
        """Test successful DOI-based paper lookup."""
        mock_sickle = Mock()
        mock_sickle_class.return_value = mock_sickle

        # Mock a record with the requested DOI
        mock_record = Mock()
        mock_record.header.identifier = "oai:mdpi.com:sensors-20-123456"
        mock_record.header.setSpec = ["journal:sensors"]
        mock_record.metadata = {
            "title": ["Sensor Technology Advances"],
            "creator": ["Author, Test"],
            "identifier": ["https://doi.org/10.3390/s24123456"],
            "date": ["2024-01-15"],
        }
        mock_sickle.ListRecords.return_value = [mock_record]

        repository = MDPIPaperRepository()
        paper = repository.find_by_doi("10.3390/s24123456")

        assert paper is not None
        assert isinstance(paper, ResearchPaper)
        assert paper.doi == "10.3390/s24123456"

    def test_find_by_arxiv_id_returns_none(self):
        """Test that ArXiv ID lookup returns None (MDPI doesn't have ArXiv papers)."""
        repository = MDPIPaperRepository()
        paper = repository.find_by_arxiv_id("2401.12345")

        # MDPI journals don't typically contain ArXiv papers
        assert paper is None


class TestMDPIPaperRepositoryMetadataProcessing:
    """Test Dublin Core metadata processing and domain object creation."""

    def test_convert_dublin_core_to_research_paper(self):
        """Test conversion from Dublin Core metadata to ResearchPaper entity."""
        repository = MDPIPaperRepository()

        # Sample Dublin Core metadata from MDPI OAI-PMH
        dublin_core_metadata = {
            "title": ["Advanced Machine Learning for Healthcare Sensors"],
            "creator": ["Johnson, Alice", "Brown, Bob", "Chen, Carol"],
            "subject": ["machine learning", "healthcare", "IoT sensors"],
            "description": [
                "This study explores advanced machine learning techniques for healthcare sensor data analysis."
            ],
            "date": ["2024-07-15"],
            "identifier": ["https://doi.org/10.3390/s24143210"],
            "type": ["Text"],
            "language": ["en"],
            "rights": ["© 2024 by the authors. Licensed under CC BY 4.0."],
        }

        paper = repository._convert_oai_record_to_paper(
            dublin_core_metadata, "oai:mdpi.com:sensors-24-143210"
        )

        assert isinstance(paper, ResearchPaper)
        assert paper.title == "Advanced Machine Learning for Healthcare Sensors"
        assert len(paper.authors) == 3
        assert "Johnson, Alice" in paper.authors
        assert paper.doi == "10.3390/s24143210"
        assert paper.publication_date.year == 2024
        assert paper.publication_date.month == 7

    def test_source_metadata_population(self):
        """Test that SourceMetadata is properly populated for MDPI papers."""
        repository = MDPIPaperRepository()

        dublin_core_metadata = {
            "title": ["Test Paper"],
            "creator": ["Test Author"],
            "date": ["2024-01-01"],
            "identifier": ["https://doi.org/10.3390/test123"],
        }

        paper = repository._convert_oai_record_to_paper(
            dublin_core_metadata, "oai:mdpi.com:sensors-24-test"
        )

        assert paper.source_metadata is not None
        assert paper.source_metadata.source_name == "MDPI"
        assert paper.source_metadata.source_url.startswith("oai:mdpi.com")
        assert "oai_identifier" in paper.source_metadata.source_specific_data

    def test_paper_fingerprint_generation(self):
        """Test that PaperFingerprint is generated for duplicate detection."""
        repository = MDPIPaperRepository()

        dublin_core_metadata = {
            "title": ["Unique Research Paper Title"],
            "creator": ["Unique Author"],
            "date": ["2024-01-01"],
            "identifier": ["https://doi.org/10.3390/unique123"],
        }

        paper = repository._convert_oai_record_to_paper(
            dublin_core_metadata, "oai:test"
        )

        assert paper.paper_fingerprint is not None
        assert isinstance(paper.paper_fingerprint, PaperFingerprint)


class TestMDPIPaperRepositoryReadOnlyOperations:
    """Test read-only nature of OAI-PMH repository operations."""

    def test_save_paper_raises_not_implemented(self):
        """Test that save operations are not supported (read-only repository)."""
        repository = MDPIPaperRepository()
        paper = Mock(spec=ResearchPaper)

        with pytest.raises(NotImplementedError):
            repository.save_paper(paper)

    def test_save_papers_raises_not_implemented(self):
        """Test that batch save operations are not supported."""
        repository = MDPIPaperRepository()
        papers = [Mock(spec=ResearchPaper)]

        with pytest.raises(NotImplementedError):
            repository.save_papers(papers)

    def test_count_all_returns_unlimited_indicator(self):
        """Test that count_all indicates unlimited/unknown size."""
        repository = MDPIPaperRepository()
        count = repository.count_all()

        # Should return -1 or large number to indicate unlimited/unknown
        assert count == -1 or count > 1000000


class TestMDPIPaperRepositoryIntegration:
    """Test integration with multi-source architecture."""

    @patch("src.infrastructure.repositories.mdpi_paper_repository.Sickle")
    def test_multi_source_metadata_preservation(self, mock_sickle_class):
        """Test that MDPI-specific metadata is preserved in SourceMetadata."""
        mock_sickle = Mock()
        mock_sickle_class.return_value = mock_sickle

        mock_record = Mock()
        mock_record.header.identifier = "oai:mdpi.com:sensors-24-123"
        mock_record.header.setSpec = ["journal:sensors"]
        mock_record.metadata = {
            "title": ["MDPI Test Paper"],
            "creator": ["MDPI Author"],
            "date": ["2024-01-01"],
            "identifier": ["https://doi.org/10.3390/s24010123"],
        }
        mock_sickle.ListRecords.return_value = [mock_record]

        repository = MDPIPaperRepository(journal_sets=["journal:sensors"])
        query = SearchQuery(terms=["test"])
        papers = repository.find_by_query(query)

        paper = papers[0]
        metadata = paper.source_metadata

        # Verify MDPI-specific metadata preservation
        assert metadata.source_name == "MDPI"
        assert "journal" in metadata.source_specific_data
        assert metadata.source_specific_data["journal"] == "sensors"
        assert "oai_identifier" in metadata.source_specific_data

    def test_paper_fingerprint_enables_duplicate_detection(self):
        """Test that generated fingerprints enable cross-source duplicate detection."""
        repository = MDPIPaperRepository()

        # Create two papers with same content but different source identifiers
        metadata1 = {
            "title": ["Duplicate Detection Test Paper"],
            "creator": ["Same Author"],
            "date": ["2024-01-01"],
            "identifier": ["https://doi.org/10.3390/test123"],
        }

        paper1 = repository._convert_oai_record_to_paper(
            metadata1, "oai:mdpi.com:test-1"
        )
        paper2 = repository._convert_oai_record_to_paper(
            metadata1, "oai:mdpi.com:test-2"
        )

        # Should have same fingerprint for duplicate detection
        assert paper1.paper_fingerprint == paper2.paper_fingerprint


# Educational Notes for Students:
#
# 1. TDD Methodology:
#    - Tests written BEFORE implementation (Red phase)
#    - Tests define expected behavior and API design
#    - Implementation will be driven by making these tests pass
#
# 2. Mock-Heavy Testing:
#    - External API calls must be mocked for reliable testing
#    - Mocks allow testing error scenarios without network dependencies
#    - Test both successful and failure paths comprehensively
#
# 3. OAI-PMH Protocol Testing:
#    - Tests validate proper handling of Dublin Core metadata
#    - Error handling for OAI-PMH specific exceptions
#    - Support for set-based harvesting (journal-specific queries)
#
# 4. Clean Architecture Validation:
#    - Tests verify proper interface implementation
#    - Domain objects (ResearchPaper) are created correctly
#    - Infrastructure concerns (OAI-PMH) don't leak to domain
#
# 5. Multi-Source Integration:
#    - Tests ensure SourceMetadata and PaperFingerprint integration
#    - Enables duplicate detection across different sources
#    - Source-specific capabilities are properly reported
