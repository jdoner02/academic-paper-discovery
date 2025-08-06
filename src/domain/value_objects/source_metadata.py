"""
SourceMetadata - Multi-source paper metadata tracking and quality assessment.

This value object encapsulates all information about a paper's source, including
source-specific identifiers, capabilities, metadata quality, and access permissions.
Essential for multi-source aggregation where papers from ArXiv, PubMed, and
Google Scholar need proper attribution and intelligent merging.

Educational Notes:
The SourceMetadata implements the Value Object pattern to provide immutable
source attribution for academic papers. This enables:

Key Multi-Source Capabilities:
1. Source Attribution: Track which database provided each paper
2. Quality Assessment: Score metadata completeness and reliability
3. Capability Detection: Identify what each source can provide (full-text, citations, etc.)
4. Access Permissions: Track open access status and download availability
5. Metadata Normalization: Standardize data across different source formats

Design Patterns Applied:
1. Value Object Pattern: Immutable, compared by value, safely shareable
2. Factory Method Pattern: from_*_response() methods for source-specific creation
3. Strategy Pattern: Different quality assessment strategies per source type
4. Builder Pattern: Flexible construction from various source API responses

Architecture Integration:
SourceMetadata works with:
- PaperSourcePort: Defines contracts for source-specific metadata extraction
- PaperFingerprint: Provides paper identity for cross-source duplicate detection
- Multi-source repositories: Track provenance of each paper
- Enhanced download service: Select best source for full-text access
- Metadata merging service: Combine information from multiple sources

Academic Source Characteristics:

ArXiv:
- Strengths: Open access, full-text always available, rich category classification
- Weaknesses: Preprint status, limited peer review information
- Identifiers: ArXiv ID (e.g., "2308.12345v1")
- Quality: High for technical fields, moderate overall

PubMed:
- Strengths: Peer-reviewed, rich metadata, MeSH terms, journal information
- Weaknesses: Often paywalled, limited to life sciences
- Identifiers: PMID, DOI, PMC ID
- Quality: Excellent for medical/biological sciences

Google Scholar:
- Strengths: Broad coverage, grey literature, conference papers, citation counts
- Weaknesses: Inconsistent metadata, no standardized identifiers
- Identifiers: Cluster ID, URL-based
- Quality: Variable, depends on original source
"""

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Any, Union
from datetime import datetime, timezone


@dataclass(frozen=True)
class SourceMetadata:
    """
    Immutable metadata about a paper's source and access characteristics.

    Educational Note:
    This Value Object encapsulates all source-specific information needed
    for multi-source paper aggregation. It's immutable to ensure consistent
    source attribution throughout the system.

    Design Decision: Comprehensive source tracking
    Rather than just storing a source name, we capture full context about
    the source's capabilities, data quality, and access permissions.
    This enables intelligent source selection and metadata merging.

    Attributes:
        source_name: Human-readable source name ("ArXiv", "PubMed", "Google Scholar")
        source_identifier: Source-specific unique identifier with prefix
        source_url: Direct URL to paper in source system
        has_full_text: Whether full-text is available from this source
        is_open_access: Whether paper is freely accessible
        peer_review_status: "peer_reviewed", "preprint", "unknown"
        quality_score: 0.0-1.0 assessment of metadata quality and completeness
        source_specific_data: Dict of source-specific metadata fields
        retrieved_at: When this metadata was collected (for freshness)
        access_restrictions: Any access limitations or requirements
    """

    source_name: str
    source_identifier: str
    source_url: str
    has_full_text: bool
    is_open_access: bool
    peer_review_status: str  # "peer_reviewed", "preprint", "unknown"
    quality_score: float
    source_specific_data: Dict[str, Any]
    retrieved_at: Optional[datetime] = None
    access_restrictions: Optional[List[str]] = None

    @classmethod
    def from_arxiv_response(cls, arxiv_data: Dict[str, Any]) -> "SourceMetadata":
        """
        Factory method to create SourceMetadata from ArXiv API response.

        Educational Note:
        ArXiv responses have a specific structure with entries, categories,
        and version information. This factory method normalizes the ArXiv
        format into our standard SourceMetadata structure.

        ArXiv-specific features handled:
        - Version normalization (strip v1, v2, etc. for primary identifier)
        - Category mapping to subject classifications
        - PDF link extraction from entry links
        - Preprint status assignment

        Args:
            arxiv_data: Raw response from ArXiv API

        Returns:
            SourceMetadata with ArXiv-specific attribution and capabilities
        """
        # Extract and normalize ArXiv ID (remove version for identifier)
        arxiv_id = arxiv_data.get("id", "")
        # Remove version suffix for consistent identification
        normalized_id = arxiv_id.split("v")[0] if "v" in arxiv_id else arxiv_id
        if normalized_id.startswith("http://arxiv.org/abs/"):
            normalized_id = normalized_id.replace("http://arxiv.org/abs/", "")

        source_identifier = f"arxiv:{normalized_id}"

        # Extract source URL (prefer abs URL over PDF)
        source_url = f"http://arxiv.org/abs/{normalized_id}"

        # ArXiv papers are always open access preprints with full-text
        has_full_text = True
        is_open_access = True
        peer_review_status = "preprint"

        # Extract ArXiv-specific metadata
        source_specific_data = {
            "original_id": arxiv_data.get("id", ""),
            "categories": arxiv_data.get("categories", []),
            "primary_category": arxiv_data.get("primary_category", ""),
            "comment": arxiv_data.get("comment", ""),
            "journal_ref": arxiv_data.get("journal_ref"),
            "version": arxiv_id.split("v")[-1] if "v" in arxiv_id else "v1",
            "has_latex_source": True,  # ArXiv provides LaTeX source
            "submission_history": arxiv_data.get("links", []),
        }

        # Calculate quality score for ArXiv
        quality_score = cls._calculate_arxiv_quality_score(
            arxiv_data, source_specific_data
        )

        return cls(
            source_name="ArXiv",
            source_identifier=source_identifier,
            source_url=source_url,
            has_full_text=has_full_text,
            is_open_access=is_open_access,
            peer_review_status=peer_review_status,
            quality_score=quality_score,
            source_specific_data=source_specific_data,
            retrieved_at=datetime.now(timezone.utc),
            access_restrictions=None,  # ArXiv has no access restrictions
        )

    @classmethod
    def from_pubmed_response(cls, pubmed_data: Dict[str, Any]) -> "SourceMetadata":
        """
        Factory method to create SourceMetadata from PubMed API response.

        Educational Note:
        PubMed responses contain rich metadata with MeSH terms, journal
        information, and publication details. This factory normalizes
        PubMed's XML-like structure into our standard format.

        PubMed-specific features handled:
        - PMID as primary identifier
        - MeSH term extraction for subject classification
        - Journal impact factor and publication venue information
        - PMC availability for full-text access determination

        Args:
            pubmed_data: Raw response from PubMed API

        Returns:
            SourceMetadata with PubMed-specific attribution and capabilities
        """
        pmid = pubmed_data.get("pmid", "")
        source_identifier = f"pmid:{pmid}"
        source_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        # Determine full-text availability (PMC or DOI-based)
        pmc_id = pubmed_data.get("pmc_id")
        has_full_text = bool(pmc_id)
        is_open_access = bool(pmc_id)  # PMC implies open access

        # PubMed papers are peer-reviewed
        peer_review_status = "peer_reviewed"

        # Extract PubMed-specific metadata
        source_specific_data = {
            "pmid": pmid,
            "pmc_id": pubmed_data.get("pmc_id"),
            "doi": pubmed_data.get("doi"),
            "mesh_terms": pubmed_data.get("mesh_terms", []),
            "publication_types": pubmed_data.get("publication_types", []),
            "journal": pubmed_data.get("journal", ""),
            "journal_issn": pubmed_data.get("issn"),
            "volume": pubmed_data.get("volume"),
            "issue": pubmed_data.get("issue"),
            "pages": pubmed_data.get("pages"),
            "author_affiliations": [
                author.get("affiliation")
                for author in pubmed_data.get("authors", [])
                if author.get("affiliation")
            ],
        }

        # Calculate quality score for PubMed
        quality_score = cls._calculate_pubmed_quality_score(
            pubmed_data, source_specific_data
        )

        # Determine access restrictions
        access_restrictions = []
        if not is_open_access:
            access_restrictions.append("subscription_required")

        return cls(
            source_name="PubMed",
            source_identifier=source_identifier,
            source_url=source_url,
            has_full_text=has_full_text,
            is_open_access=is_open_access,
            peer_review_status=peer_review_status,
            quality_score=quality_score,
            source_specific_data=source_specific_data,
            retrieved_at=datetime.now(timezone.utc),
            access_restrictions=access_restrictions if access_restrictions else None,
        )

    @classmethod
    def from_google_scholar_response(
        cls, scholar_data: Dict[str, Any]
    ) -> "SourceMetadata":
        """
        Factory method to create SourceMetadata from Google Scholar response.

        Educational Note:
        Google Scholar doesn't have a formal API, so this handles scraped
        data with variable quality and completeness. The focus is on
        extracting what's available while being robust to missing fields.

        Scholar-specific features handled:
        - Cluster ID as quasi-identifier
        - Citation count extraction
        - PDF availability detection
        - Venue information (conferences, journals, etc.)

        Args:
            scholar_data: Scraped data from Google Scholar

        Returns:
            SourceMetadata with Google Scholar attribution
        """
        # Create identifier from cluster ID or URL hash
        cluster_id = scholar_data.get("cluster_id")
        if cluster_id:
            source_identifier = f"scholar:{cluster_id}"
        else:
            # Fall back to URL-based identifier
            url = scholar_data.get("url", "")
            url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            source_identifier = f"scholar:{url_hash}"

        source_url = scholar_data.get("url", "")

        # Determine full-text availability from PDF URL
        pdf_url = scholar_data.get("pdf_url")
        has_full_text = bool(pdf_url)
        is_open_access = has_full_text  # If PDF available, assume open access

        # Google Scholar can't reliably determine peer review status
        peer_review_status = "unknown"

        # Extract Google Scholar-specific metadata
        source_specific_data = {
            "cluster_id": cluster_id,
            "citations": scholar_data.get("citations", 0),
            "cited_by_url": scholar_data.get("cited_by_url"),
            "pdf_url": pdf_url,
            "venue": scholar_data.get("venue", ""),
            "year": scholar_data.get("year"),
            "snippet": scholar_data.get("snippet", ""),
            "related_url": scholar_data.get("related_url"),
        }

        # Calculate quality score for Google Scholar
        quality_score = cls._calculate_scholar_quality_score(
            scholar_data, source_specific_data
        )

        # Determine access restrictions
        access_restrictions = []
        if not is_open_access:
            access_restrictions.append("access_varies")

        return cls(
            source_name="Google Scholar",
            source_identifier=source_identifier,
            source_url=source_url,
            has_full_text=has_full_text,
            is_open_access=is_open_access,
            peer_review_status=peer_review_status,
            quality_score=quality_score,
            source_specific_data=source_specific_data,
            retrieved_at=datetime.now(timezone.utc),
            access_restrictions=access_restrictions if access_restrictions else None,
        )

    def get_source_capabilities(self) -> Set[str]:
        """
        Get set of capabilities this source provides.

        Educational Note:
        Different sources excel at different capabilities. This method
        returns a standardized set of capability flags that can be used
        to select the best source for specific research needs.

        Common capabilities:
        - full_text_download: Can provide complete paper text
        - citation_tracking: Provides citation counts and relationships
        - peer_review_status: Can determine if paper is peer-reviewed
        - metadata_rich: Provides comprehensive metadata
        - open_access: Papers are freely available

        Returns:
            Set of capability strings for this source
        """
        capabilities = set()

        # Universal capabilities based on source characteristics
        if self.has_full_text:
            capabilities.add("full_text_download")
        if self.is_open_access:
            capabilities.add("open_access")
        if self.peer_review_status != "unknown":
            capabilities.add("peer_review_status")

        # Source-specific capabilities
        if self.source_name == "ArXiv":
            capabilities.update(
                [
                    "category_classification",
                    "version_tracking",
                    "latex_source",
                    "preprint_status",
                ]
            )
            if self.source_specific_data.get("has_latex_source"):
                capabilities.add("latex_source")

        elif self.source_name == "PubMed":
            capabilities.update(
                [
                    "mesh_classification",
                    "journal_metrics",
                    "abstract_available",
                    "citation_tracking",
                ]
            )
            if self.source_specific_data.get("pmc_id"):
                capabilities.add("pmc_integration")
            if self.source_specific_data.get("mesh_terms"):
                capabilities.add("mesh_classification")

        elif self.source_name == "Google Scholar":
            capabilities.update(
                [
                    "broad_coverage",
                    "grey_literature",
                    "conference_papers",
                    "citation_graph",
                ]
            )
            if self.source_specific_data.get("citations", 0) > 0:
                capabilities.add("citation_counts")

        return capabilities

    def calculate_quality_score(self) -> float:
        """
        Calculate comprehensive quality score for this source's metadata.

        Educational Note:
        Quality scoring helps prioritize sources when multiple sources
        provide information about the same paper. The score considers:
        - Metadata completeness (more fields = higher score)
        - Source reliability (PubMed > ArXiv > Google Scholar)
        - Data freshness (newer = better)
        - Access characteristics (open access preferred)

        Returns:
            Quality score from 0.0 (poor) to 1.0 (excellent)
        """
        if self.source_name == "ArXiv":
            return self._calculate_arxiv_quality_score({}, self.source_specific_data)
        elif self.source_name == "PubMed":
            return self._calculate_pubmed_quality_score({}, self.source_specific_data)
        elif self.source_name == "Google Scholar":
            return self._calculate_scholar_quality_score({}, self.source_specific_data)
        else:
            return 0.5  # Default middle score for unknown sources

    def assess_completeness(self) -> float:
        """
        Assess completeness of available metadata fields.

        Educational Note:
        Completeness assessment identifies gaps that might be filled
        by other sources. This enables intelligent metadata merging
        where each source contributes its strongest metadata fields.

        Returns:
            Completeness score from 0.0 (minimal) to 1.0 (comprehensive)
        """
        # Define expected fields for comprehensive metadata
        expected_fields = {
            "title",
            "authors",
            "abstract",
            "keywords",
            "publication_date",
            "doi",
            "journal",
            "volume",
            "pages",
            "subject_classification",
        }

        # Count available fields in source-specific data
        available_fields = set(self.source_specific_data.keys())

        # Add standard fields that are always present
        if self.has_full_text:
            available_fields.add("full_text")
        if self.peer_review_status != "unknown":
            available_fields.add("peer_review_status")

        # Calculate completeness ratio
        overlap = available_fields.intersection(expected_fields)
        completeness = len(overlap) / len(expected_fields)

        # Bonus for source-specific high-value fields
        if self.source_name == "PubMed" and "mesh_terms" in available_fields:
            completeness += 0.1
        if self.source_name == "ArXiv" and "categories" in available_fields:
            completeness += 0.1
        if "citations" in available_fields:
            completeness += 0.1

        return min(1.0, completeness)  # Cap at 1.0

    @staticmethod
    def _calculate_arxiv_quality_score(
        arxiv_data: Dict[str, Any], specific_data: Dict[str, Any]
    ) -> float:
        """Calculate quality score specific to ArXiv papers."""
        score = 0.7  # Base score for ArXiv reliability

        # Bonus for categories (subject classification)
        if specific_data.get("categories"):
            score += 0.1

        # Bonus for journal reference (published version available)
        if specific_data.get("journal_ref"):
            score += 0.1

        # Bonus for comments (additional context)
        if specific_data.get("comment"):
            score += 0.05

        return min(1.0, score)

    @staticmethod
    def _calculate_pubmed_quality_score(
        pubmed_data: Dict[str, Any], specific_data: Dict[str, Any]
    ) -> float:
        """Calculate quality score specific to PubMed papers."""
        score = 0.8  # High base score for PubMed reliability

        # Bonus for MeSH terms (rich subject classification)
        if specific_data.get("mesh_terms"):
            score += 0.1

        # Bonus for PMC availability (full-text access)
        if specific_data.get("pmc_id"):
            score += 0.05

        # Bonus for author affiliations (institutional context)
        if specific_data.get("author_affiliations"):
            score += 0.05

        return min(1.0, score)

    @staticmethod
    def _calculate_scholar_quality_score(
        scholar_data: Dict[str, Any], specific_data: Dict[str, Any]
    ) -> float:
        """Calculate quality score specific to Google Scholar papers."""
        score = 0.5  # Lower base score due to variable quality

        # Bonus for citation count (impact indicator)
        citations = specific_data.get("citations", 0)
        if citations > 0:
            score += min(0.2, citations / 100)  # Up to 0.2 bonus for citations

        # Bonus for PDF availability
        if specific_data.get("pdf_url"):
            score += 0.1

        # Bonus for venue information
        if specific_data.get("venue"):
            score += 0.05

        return min(1.0, score)

    def __str__(self) -> str:
        """Human-readable representation for debugging."""
        return (
            f"SourceMetadata({self.source_name}: {self.source_identifier}, "
            f"quality={self.quality_score:.2f}, open_access={self.is_open_access})"
        )

    def __repr__(self) -> str:
        """Developer representation for debugging."""
        return (
            f"SourceMetadata(source_name='{self.source_name}', "
            f"source_identifier='{self.source_identifier}', "
            f"quality_score={self.quality_score:.2f})"
        )
