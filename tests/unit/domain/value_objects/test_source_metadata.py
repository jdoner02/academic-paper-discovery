"""
Unit tests for SourceMetadata - Multi-source paper metadata system.

This module tests the SourceMetadata value object that tracks which academic
databa        assert metadata.source_name == "PubMed"
        assert metadata.source_identifier == "pmid:37123456"
        assert metadata.source_url.startswith("https://pubmed.ncbi.nlm.nih.gov/")
        assert metadata.has_full_text is True  # PMC ID available = full text access
        assert metadata.is_open_access is True  # PMC available
        assert metadata.peer_review_status == "peer_reviewed"
        assert "Deep Learning" in metadata.source_specific_data['mesh_terms']
        assert metadata.quality_score > 0.8  # PubMed has excellent metadataer came from, along with source-specific metadata and capabilities.
This is essential for multi-source aggregation where papers from ArXiv, PubMed,
and Google Scholar need proper attribution and handling.

Educational Notes:
The SourceMetadata implements the Value Object pattern to encapsulate all
information about a paper's source, including:
- Source identification and capabilities
- Source-specific identifiers and metadata
- Data quality and reliability indicators
- Download and access permissions

Key Multi-Source Challenges:
Academic papers from different sources present unique challenges:
- Different identifier systems (DOI, ArXiv ID, PMID, Google Scholar ID)
- Varying metadata completeness (abstracts, keywords, citation counts)
- Different access permissions (open access, subscription, preprint)
- Source-specific quality indicators (peer review status, publication venue)
- Rate limiting and API constraints per source
- Citation count variations across sources

Design Patterns Demonstrated:
- Value Object Pattern: Immutable source metadata with value-based equality
- Builder Pattern: Flexible construction from various source responses
- Strategy Pattern: Source-specific metadata extraction strategies
- Factory Pattern: Create from different source API responses

Testing Strategy:
Following TDD to ensure robust source metadata handling:
1. Test basic source metadata creation from different sources
2. Test source-specific identifier extraction and normalization
3. Test metadata quality assessment and completeness scoring
4. Test source capability detection (full-text, citations, etc.)
5. Test metadata merging from multiple sources for same paper

Architecture Integration:
SourceMetadata works with:
- PaperSourcePort: Defines contracts for source-specific metadata
- PaperFingerprint: Provides paper identity for cross-source matching
- Multi-source repositories: Track source of each paper for proper attribution
- Download services: Determine best source for full-text access
"""

import pytest
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from src.domain.entities.research_paper import ResearchPaper


class TestSourceMetadataCreation:
    """
    Test creation of SourceMetadata value objects from different sources.

    Educational Note:
    These tests define how source metadata is extracted and normalized
    from different academic databases, establishing the foundation for
    multi-source paper aggregation with proper source attribution.
    """

    def test_create_arxiv_source_metadata(self):
        """
        Test source metadata creation for ArXiv papers.

        Educational Note:
        ArXiv papers have unique characteristics:
        - ArXiv-specific identifiers and categories
        - Preprint status and version information
        - Open access availability
        - Limited peer review information
        """
        # This will fail until we implement SourceMetadata
        from src.domain.value_objects.source_metadata import SourceMetadata

        # Simulate ArXiv API response metadata
        arxiv_response = {
            "id": "2308.12345v1",
            "title": "Novel Quantum Algorithms for Machine Learning",
            "authors": [{"name": "Carol Zhang"}],
            "primary_category": "quant-ph",
            "categories": ["quant-ph", "cs.LG"],
            "abstract": "We present novel quantum algorithms...",
            "published": "2023-08-22T14:30:00Z",
            "updated": "2023-08-22T14:30:00Z",
            "journal_ref": None,
            "doi": None,
            "comment": "Submitted to Quantum Computing Journal",
            "links": [
                {"href": "http://arxiv.org/abs/2308.12345v1", "rel": "alternate"},
                {
                    "href": "http://arxiv.org/pdf/2308.12345v1",
                    "rel": "related",
                    "type": "application/pdf",
                },
            ],
        }

        metadata = SourceMetadata.from_arxiv_response(arxiv_response)

        assert metadata.source_name == "ArXiv"
        assert metadata.source_identifier == "arxiv:2308.12345"  # Version normalized
        assert metadata.source_url == "http://arxiv.org/abs/2308.12345"  # Canonical URL
        assert metadata.has_full_text is True
        assert metadata.is_open_access is True
        assert metadata.peer_review_status == "preprint"
        assert "quant-ph" in metadata.source_specific_data["categories"]
        assert metadata.quality_score > 0.7  # ArXiv has good metadata quality

    def test_create_pubmed_source_metadata(self):
        """
        Test source metadata creation for PubMed papers.

        Educational Note:
        PubMed papers have different characteristics:
        - PMID identifiers and MeSH terms
        - Peer review status from journal publication
        - Abstract and citation information
        - Potential paywall restrictions
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        # Simulate PubMed API response metadata
        pubmed_response = {
            "pmid": "37123456",
            "title": "Deep Learning Applications in Medical Imaging",
            "authors": [
                {
                    "lastname": "Smith",
                    "forename": "John",
                    "affiliation": "Stanford University",
                },
                {"lastname": "Johnson", "forename": "Alice", "affiliation": "MIT"},
            ],
            "journal": "Nature Medicine",
            "pub_date": "2023-06-15",
            "abstract": "Deep learning has revolutionized medical imaging...",
            "doi": "10.1038/s41591-023-01234-x",
            "pmc_id": "PMC10234567",
            "mesh_terms": [
                "Deep Learning",
                "Medical Imaging",
                "Artificial Intelligence",
            ],
            "publication_types": ["Journal Article", "Research Support"],
            "issn": "1546-170X",
            "volume": "29",
            "issue": "6",
            "pages": "1234-1245",
        }

        metadata = SourceMetadata.from_pubmed_response(pubmed_response)

        assert metadata.source_name == "PubMed"
        assert metadata.source_identifier == "pmid:37123456"
        assert metadata.source_url.startswith("https://pubmed.ncbi.nlm.nih.gov/")
        assert metadata.has_full_text is True  # PMC ID available = full text access
        assert metadata.is_open_access is True  # PMC available
        assert metadata.peer_review_status == "peer_reviewed"
        assert "Deep Learning" in metadata.source_specific_data["mesh_terms"]
        assert metadata.quality_score > 0.8  # PubMed has excellent metadata

    def test_create_google_scholar_source_metadata(self):
        """
        Test source metadata creation for Google Scholar papers.

        Educational Note:
        Google Scholar papers have limited but broad characteristics:
        - No standardized identifiers (relies on URL/title matching)
        - Broad coverage including grey literature
        - Citation counts from multiple sources
        - Variable metadata quality
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        # Simulate Google Scholar scraping result
        scholar_response = {
            "title": "Blockchain Security in Healthcare Systems",
            "authors": ["David Kim", "Elena Rodriguez"],
            "venue": "International Conference on Blockchain Technology",
            "year": "2023",
            "url": "https://example.com/blockchain-healthcare-2023.pdf",
            "abstract": "This paper explores blockchain security...",
            "citations": 28,
            "cited_by_url": "https://scholar.google.com/scholar?cites=12345678901234567890",
            "pdf_url": "https://example.com/blockchain-healthcare-2023.pdf",
            "cluster_id": "12345678901234567890",
        }

        metadata = SourceMetadata.from_google_scholar_response(scholar_response)

        assert metadata.source_name == "Google Scholar"
        assert metadata.source_identifier.startswith("scholar:")
        assert metadata.source_url == scholar_response['url']
        assert metadata.has_full_text is True  # PDF available
        assert metadata.is_open_access is True  # Directly accessible PDF
        assert metadata.peer_review_status == "unknown"  # Can't determine from Scholar
        assert metadata.source_specific_data['cluster_id'] == '12345678901234567890'
        assert metadata.quality_score > 0.7  # High score due to citations and rich metadata


class TestSourceMetadataCapabilities:
    """
    Test source capability detection and reporting.

    Educational Note:
    Different sources have different capabilities for paper access,
    metadata richness, and additional services. We need to track
    these capabilities to optimize our paper aggregation strategy.
    """

    def test_arxiv_capabilities(self):
        """
        Test ArXiv-specific capabilities detection.

        Educational Note:
        ArXiv provides excellent capabilities for preprints:
        - Always open access with full PDF
        - Rich category and subject classification
        - Version tracking for paper evolution
        - LaTeX source code availability
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        arxiv_metadata = SourceMetadata(
            source_name="ArXiv",
            source_identifier="arxiv:2308.12345",
            source_url="http://arxiv.org/abs/2308.12345v1",
            has_full_text=True,
            is_open_access=True,
            peer_review_status="preprint",
            quality_score=0.8,
            source_specific_data={
                "categories": ["quant-ph", "cs.LG"],
                "version": "v1",
                "has_latex_source": True,
            },
        )

        capabilities = arxiv_metadata.get_source_capabilities()

        assert "full_text_download" in capabilities
        assert "category_classification" in capabilities
        assert "version_tracking" in capabilities
        assert "latex_source" in capabilities
        assert "open_access" in capabilities
        assert "preprint_status" in capabilities

    def test_pubmed_capabilities(self):
        """
        Test PubMed-specific capabilities detection.

        Educational Note:
        PubMed provides excellent metadata for peer-reviewed papers:
        - Rich metadata with MeSH terms and abstracts
        - Peer review status and publication venue information
        - Citation tracking and related articles
        - Integration with PMC for some full-text access
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        pubmed_metadata = SourceMetadata(
            source_name="PubMed",
            source_identifier="pmid:37123456",
            source_url="https://pubmed.ncbi.nlm.nih.gov/37123456/",
            has_full_text=False,
            is_open_access=True,  # PMC available
            peer_review_status="peer_reviewed",
            quality_score=0.9,
            source_specific_data={
                "mesh_terms": ["Deep Learning", "Medical Imaging"],
                "pmc_id": "PMC10234567",
                "journal_impact_factor": 87.2,
            },
        )

        capabilities = pubmed_metadata.get_source_capabilities()

        assert "mesh_classification" in capabilities
        assert "peer_review_status" in capabilities
        assert "citation_tracking" in capabilities
        assert "journal_metrics" in capabilities
        assert "abstract_available" in capabilities
        assert "pmc_integration" in capabilities

    def test_google_scholar_capabilities(self):
        """
        Test Google Scholar-specific capabilities detection.

        Educational Note:
        Google Scholar provides broad coverage but limited metadata:
        - Wide coverage including grey literature and conference papers
        - Citation counts aggregated from multiple sources
        - Limited metadata quality and standardization
        - Variable full-text access depending on publisher policies
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        scholar_metadata = SourceMetadata(
            source_name="Google Scholar",
            source_identifier="scholar:12345678901234567890",
            source_url="https://example.com/paper.pdf",
            has_full_text=True,
            is_open_access=True,
            peer_review_status="unknown",
            quality_score=0.6,
            source_specific_data={
                "cluster_id": "12345678901234567890",
                "citations": 28,
                "cited_by_url": "https://scholar.google.com/scholar?cites=...",
            },
        )

        capabilities = scholar_metadata.get_source_capabilities()

        assert "broad_coverage" in capabilities
        assert "citation_counts" in capabilities
        assert "grey_literature" in capabilities
        assert "conference_papers" in capabilities
        assert "citation_graph" in capabilities


class TestSourceMetadataQuality:
    """
    Test metadata quality assessment across sources.

    Educational Note:
    Quality assessment helps prioritize sources and identify the most
    reliable metadata for each paper. This is crucial when multiple
    sources provide different information about the same paper.
    """

    def test_quality_score_calculation(self):
        """
        Test quality score calculation based on available metadata.

        Educational Note:
        Quality scores help determine which source to trust when multiple
        sources provide conflicting information about the same paper.
        Factors include metadata completeness, source reliability, and
        data freshness.
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        # High quality: PubMed with complete metadata
        high_quality = SourceMetadata(
            source_name="PubMed",
            source_identifier="pmid:12345",
            source_url="https://pubmed.ncbi.nlm.nih.gov/12345/",
            has_full_text=True,
            is_open_access=True,
            peer_review_status="peer_reviewed",
            quality_score=0.0,  # Will be calculated
            source_specific_data={
                "doi": "10.1038/example",
                "abstract": "Complete abstract available",
                "mesh_terms": ["Term1", "Term2"],
                "journal": "Nature",
                "authors_with_affiliations": True,
            },
        )

        # Medium quality: ArXiv with good metadata
        medium_quality = SourceMetadata(
            source_name="ArXiv",
            source_identifier="arxiv:2308.12345",
            source_url="http://arxiv.org/abs/2308.12345",
            has_full_text=True,
            is_open_access=True,
            peer_review_status="preprint",
            quality_score=0.0,  # Will be calculated
            source_specific_data={
                "categories": ["cs.LG"],
                "abstract": "Abstract available",
                "version": "v1",
            },
        )

        # Low quality: Google Scholar with minimal metadata
        low_quality = SourceMetadata(
            source_name="Google Scholar",
            source_identifier="scholar:123456789",
            source_url="https://example.com/paper.pdf",
            has_full_text=False,
            is_open_access=False,
            peer_review_status="unknown",
            quality_score=0.0,  # Will be calculated
            source_specific_data={"citations": 5},
        )

        high_score = high_quality.calculate_quality_score()
        medium_score = medium_quality.calculate_quality_score()
        low_score = low_quality.calculate_quality_score()

        assert high_score > medium_score > low_score
        assert high_score >= 0.8
        assert medium_score >= 0.6
        assert low_score >= 0.3

    def test_metadata_completeness_assessment(self):
        """
        Test assessment of metadata field completeness.

        Educational Note:
        Completeness assessment identifies missing fields that might be
        available from other sources, enabling intelligent source merging
        for comprehensive paper metadata.
        """
        from src.domain.value_objects.source_metadata import SourceMetadata

        complete_metadata = SourceMetadata(
            source_name="PubMed",
            source_identifier="pmid:12345",
            source_url="https://pubmed.ncbi.nlm.nih.gov/12345/",
            has_full_text=True,
            is_open_access=True,
            peer_review_status="peer_reviewed",
            quality_score=0.9,
            source_specific_data={
                "doi": "10.1038/example",
                "abstract": "Full abstract",
                "keywords": ["AI", "ML"],
                "authors": [{"name": "John Smith", "affiliation": "MIT"}],
                "journal": "Nature",
                "publication_date": "2023-06-15",
            },
        )

        incomplete_metadata = SourceMetadata(
            source_name="Google Scholar",
            source_identifier="scholar:123456",
            source_url="https://example.com/paper.pdf",
            has_full_text=False,
            is_open_access=False,
            peer_review_status="unknown",
            quality_score=0.5,
            source_specific_data={"title": "Paper Title"},  # Minimal data
        )

        complete_score = complete_metadata.assess_completeness()
        incomplete_score = incomplete_metadata.assess_completeness()

        assert complete_score > 0.8
        assert incomplete_score < 0.5
        assert complete_score > incomplete_score


class TestSourceMetadataMerging:
    """
    Test merging metadata from multiple sources for the same paper.

    Educational Note:
    When the same paper appears in multiple sources (e.g., ArXiv preprint
    later published in PubMed), we need to intelligently merge metadata
    to create the most complete and accurate representation.
    """

    def test_merge_arxiv_and_pubmed_metadata(self):
        """
        Test merging ArXiv preprint with PubMed published version.

        Educational Note:
        Common scenario: Paper starts as ArXiv preprint, gets published
        in peer-reviewed journal indexed by PubMed. We want to combine
        ArXiv's full-text access with PubMed's peer review status.
        """
        # This will be implemented in next iteration
        pass  # Placeholder for future implementation

    def test_conflict_resolution_in_metadata_merge(self):
        """
        Test resolution of conflicting metadata between sources.

        Educational Note:
        When sources provide conflicting information (different author
        spellings, citation counts, etc.), we need clear rules for
        which source takes precedence based on reliability and recency.
        """
        # This will be implemented in next iteration
        pass  # Placeholder for future implementation
