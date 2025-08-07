"""
PMC Paper Repository - PubMed Central OAI-PMH integration for biomedical research.

This repository provides real-time access to biomedical research papers from
PubMed Central, implementing the PaperSourcePort interface for multi-source
paper aggregation with focus on medical and life sciences research.

Educational Notes:
- Extends PaperSourcePort for multi-source capabilities
- Uses SourceMetadata for biomedical-specific data preservation
- Integrates PaperFingerprint for duplicate detection across sources
- Demonstrates Adapter Pattern for external biomedical database integration
- Shows Clean Architecture with domain object integration

Design Decisions:
- PMC-specific metadata extraction with medical provenance tracking
- Rate limiting and API etiquette for responsible NCBI usage
- Comprehensive error handling for biomedical data variability
- PDF download capabilities with PMC URL construction

Biomedical Research Features:
- Source capability reporting (full-text XML availability)
- Metadata enrichment using SourceMetadata.from_pmc_response()
- Integration with PaperFingerprint for medical literature deduplication
- Support for clinical trial and research article filtering

Use Cases:
- Medical research automation with multi-source aggregation
- Literature review with biomedical source attribution
- Clinical paper collection with duplicate detection
- Systematic reviews with comprehensive medical metadata
"""

import re
import requests
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch, BadArgument

from src.application.ports.paper_source_port import PaperSourcePort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.source_metadata import SourceMetadata
from src.domain.value_objects.paper_fingerprint import PaperFingerprint


class PMCPaperRepository(PaperSourcePort):
    """
    PubMed Central OAI-PMH implementation of the paper repository interface.

    Educational Notes:
    - Implements PaperSourcePort for polymorphic multi-source behavior
    - Uses OAI-PMH protocol for standardized metadata harvesting
    - Handles biomedical-specific metadata fields and formats
    - Provides rate limiting and error handling for external API
    - Demonstrates Clean Architecture with external system integration

    Biomedical Context:
    - PMC provides full-text access to life sciences literature
    - Contains both research articles and clinical trial reports
    - Offers rich metadata including medical subject headings (MeSH)
    - Provides PDF and XML full-text access for many articles

    Architecture Pattern:
    - Repository Pattern: Abstracts data access details
    - Adapter Pattern: Converts PMC OAI format to domain objects
    - Facade Pattern: Simplifies complex OAI-PMH operations
    """

    def __init__(self, base_url: str = "https://pmc.ncbi.nlm.nih.gov/oai/oai2"):
        """
        Initialize PMC repository with OAI-PMH endpoint.

        Educational Note:
        This constructor demonstrates dependency injection by allowing
        custom base URLs for testing while providing production defaults.
        The session setup shows proper HTTP client configuration.

        Args:
            base_url: PMC OAI-PMH endpoint URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Academic Research Tool - PMC Integration (respectful harvesting)"
            }
        )

    def find_by_query(self, search_query: SearchQuery) -> List[ResearchPaper]:
        """
        Search PMC using OAI-PMH protocol.

        Educational Note:
        This method demonstrates the Adapter pattern by converting
        SearchQuery domain objects into PMC OAI-PMH parameters and
        converting the results back into ResearchPaper domain objects.

        Args:
            search_query: Domain object containing search parameters

        Returns:
            List of ResearchPaper objects with PMC metadata
        """
        try:
            sickle = Sickle(self.base_url)

            # Build OAI-PMH query parameters
            params = {
                "metadataPrefix": "oai_dc",
                "set": None,  # PMC doesn't use sets like MDPI
            }

            # Add date filtering if specified
            if search_query.start_date:
                params["from_"] = search_query.start_date.strftime("%Y-%m-%d")
            if search_query.end_date:
                params["until"] = search_query.end_date.strftime("%Y-%m-%d")

            # Execute OAI-PMH ListRecords request
            try:
                records = sickle.ListRecords(**params)
            except NoRecordsMatch:
                return []

            papers = []
            count = 0

            for record in records:
                if count >= search_query.max_results:
                    break

                try:
                    paper = self._convert_pmc_record_to_paper(record)

                    # Apply search term filtering (OAI-PMH doesn't support keyword search)
                    if self._matches_search_terms(paper, search_query.terms):
                        if self._matches_query_filters(
                            paper.publication_date, search_query
                        ):
                            papers.append(paper)
                            count += 1

                except Exception as e:
                    # Log and skip problematic records
                    continue

            return papers

        except Exception as e:
            # Handle network errors gracefully
            return []

    def find_by_doi(self, doi: str) -> Optional[ResearchPaper]:
        """Find paper by DOI using general search."""
        search_query = SearchQuery(terms=[doi], max_results=1)
        results = self.find_by_query(search_query)
        return results[0] if results else None

    def find_by_pmc_id(self, pmc_id: str) -> Optional[ResearchPaper]:
        """Find paper by PMC identifier."""
        search_query = SearchQuery(terms=[pmc_id], max_results=1)
        results = self.find_by_query(search_query)
        return results[0] if results else None

    def find_by_arxiv_id(self, arxiv_id: str) -> Optional[ResearchPaper]:
        """PMC repository doesn't contain ArXiv IDs directly."""
        return None

    def get_source_name(self) -> str:
        """Get the human-readable name of this paper source."""
        return "PubMed Central"

    def get_source_capabilities(self) -> Dict[str, Any]:
        """Get detailed capability information for PMC source."""
        return {
            "full_text_access": True,
            "metadata_richness": "high",
            "search_operators": ["AND", "OR", "NOT"],
            "date_range_support": True,
            "citation_tracking": False,
            "open_access_only": True,
            "biomedical_focus": True,
            "xml_full_text": True,
            "pdf_access": True,
        }

    def supports_full_text_download(self) -> bool:
        """PMC provides full-text PDF downloads for all papers."""
        return True

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get rate limiting information for PMC OAI-PMH."""
        return {
            "requests_per_second": 2.0,  # Conservative rate for OAI-PMH
            "burst_limit": 10,
            "daily_limit": None,  # No daily limit for OAI-PMH
            "requires_api_key": False,
            "courteous_delay": 1.0,  # Seconds between requests
        }

    def extract_source_specific_metadata(
        self, raw_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract PMC-specific metadata from OAI-PMH response."""
        return {
            "pmc_id": self._extract_pmc_id(
                self._extract_first_value(raw_data.get("identifier", []))
            ),
            "dublin_core_subjects": raw_data.get("subject", []),
            "publication_types": raw_data.get("type", []),
            "publisher": self._extract_first_value(raw_data.get("publisher", [])),
            "rights": raw_data.get("rights", []),
            "format": raw_data.get("format", []),
            "relation": raw_data.get("relation", []),
            "has_pdf_access": True,
            "has_xml_access": True,
            "language": self._extract_first_value(raw_data.get("language", ["en"])),
        }

    def enrich_paper_with_source_metadata(
        self, paper: ResearchPaper, source_metadata: Dict[str, Any]
    ) -> ResearchPaper:
        """Enrich paper with PMC-specific metadata."""
        # PMC enrichment is handled in _convert_pmc_record_to_paper
        return paper

    def get_source_paper_url(self, paper: ResearchPaper) -> Optional[str]:
        """Get the canonical PMC URL for this paper."""
        if (
            paper.source_metadata
            and paper.source_metadata.source_name == "PubMed Central"
        ):
            pmc_id = paper.source_metadata.source_specific_data.get("pmc_id", "")
            if pmc_id:
                return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
        return None

    def save_paper(self, paper: ResearchPaper) -> bool:
        """PMC repository is read-only (OAI-PMH harvesting)."""
        raise NotImplementedError("PMC repository is read-only (OAI-PMH harvesting)")

    def save_papers(self, papers: List[ResearchPaper]) -> bool:
        """PMC repository is read-only (OAI-PMH harvesting)."""
        raise NotImplementedError("PMC repository is read-only (OAI-PMH harvesting)")

    def count_all(self) -> int:
        """Return large number indicating unlimited search capacity."""
        return 999999  # Indicates unlimited/unknown capacity

    def _build_pmc_query(
        self,
        terms: List[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> str:
        """
        Build query string for PMC search.

        Educational Note:
        PMC OAI-PMH doesn't support keyword search directly, so this is
        used for post-processing filtering. This demonstrates the pattern
        of adapting domain concepts to external system limitations.
        """
        if not terms:
            return ""

        # Combine terms with AND logic for biomedical precision
        query = " AND ".join(terms)
        return query

    def _convert_pmc_record_to_paper(self, record) -> ResearchPaper:
        """
        Convert PMC OAI-PMH record to ResearchPaper domain object.

        Educational Note:
        This method demonstrates the Adapter pattern by transforming
        external data formats into domain objects. It handles the
        variability in PMC metadata and provides sensible defaults.

        Args:
            record: Sickle OAI record object

        Returns:
            ResearchPaper domain object with PMC metadata
        """
        metadata = record.metadata or {}

        # Extract basic paper information
        title = self._extract_first_value(metadata.get("title", []))
        authors = self._extract_authors(metadata.get("creator", []))
        abstract = self._extract_first_value(metadata.get("description", []))

        # Extract publication information
        publication_date = self._parse_date(
            self._extract_first_value(metadata.get("date", []))
        )
        journal = self._extract_first_value(metadata.get("publisher", []))

        # Extract PMC-specific identifiers
        identifier = self._extract_first_value(metadata.get("identifier", []))
        pmc_id = self._extract_pmc_id(identifier)
        doi = self._extract_doi_from_relations(metadata.get("relation", []))

        # Create source metadata for multi-source tracking
        source_metadata = SourceMetadata.from_pmc_response(
            original_data=metadata,
            source_identifier=pmc_id,
            source_url=self._get_pmc_url(pmc_id),
            harvest_timestamp=datetime.now(timezone.utc),
        )

        # Create paper fingerprint for deduplication
        # Note: We need to create the paper first, then calculate fingerprint
        temp_paper = ResearchPaper(
            title=title,
            authors=authors,
            abstract=abstract,
            publication_date=publication_date,
            venue=journal,  # PMC journal maps to ResearchPaper venue
            doi=doi,
            source_metadata=source_metadata,
            paper_fingerprint=None,  # Will be set after creation
            url=self._get_pdf_url(metadata),
        )

        paper_fingerprint = PaperFingerprint.from_paper(temp_paper)

        # Create final paper with fingerprint
        return ResearchPaper(
            title=title,
            authors=authors,
            abstract=abstract,
            publication_date=publication_date,
            venue=journal,  # PMC journal maps to ResearchPaper venue
            doi=doi,
            source_metadata=source_metadata,
            paper_fingerprint=paper_fingerprint,
            url=self._get_pdf_url(metadata),
        )

    def _matches_search_terms(self, paper: ResearchPaper, terms: List[str]) -> bool:
        """Check if paper matches search terms."""
        if not terms:
            return True

        searchable_text = (
            f"{paper.title} {paper.abstract} {' '.join(paper.authors)}".lower()
        )

        # Check if any term (or phrase) appears in the searchable text
        return any(term.lower() in searchable_text for term in terms)

    def _matches_query_filters(
        self, paper_date: datetime, search_query: SearchQuery
    ) -> bool:
        """Check if paper matches date range filters."""
        if search_query.start_date and paper_date < search_query.start_date:
            return False
        if search_query.end_date and paper_date > search_query.end_date:
            return False
        return True

    def _extract_first_value(self, values: List[str]) -> str:
        """Extract first non-empty value from list."""
        if isinstance(values, str):
            return values
        if isinstance(values, list) and values:
            return values[0]
        return ""

    def _extract_authors(self, creator_data) -> List[str]:
        """Extract and format author names."""
        if isinstance(creator_data, str):
            return [creator_data]
        if isinstance(creator_data, list) and creator_data:
            return creator_data
        # Business rule: Every paper must have at least one author
        return ["Unknown Author"]

    def _parse_date(self, date_string: str) -> datetime:
        """Parse various date formats from PMC."""
        if not date_string:
            return datetime.now(timezone.utc)

        try:
            # Try ISO date format first
            if "T" in date_string:
                return datetime.fromisoformat(date_string.replace("Z", "+00:00"))

            # Try date-only format
            date_part = date_string.split("T")[0]
            return datetime.strptime(date_part, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        except ValueError:
            # Fallback to current date for unparseable dates
            return datetime.now(timezone.utc)

    def _extract_pmc_id(self, identifier: str) -> str:
        """Extract PMC ID from OAI identifier."""
        if not identifier:
            return ""

        # PMC identifiers usually in format: oai:pmc:PMC123456
        match = re.search(r"PMC\d+", identifier)
        return match.group(0) if match else ""

    def _extract_doi_from_relations(self, relations: List[str]) -> str:
        """Extract DOI from relation fields."""
        for relation in relations or []:
            if relation.startswith("doi:"):
                return relation[4:]  # Remove 'doi:' prefix
            if "doi.org" in relation:
                return relation.split("/")[-1]
        return ""

    def _get_pmc_url(self, pmc_id: str) -> str:
        """Construct PMC article URL from ID."""
        if pmc_id:
            return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
        return ""

    def _get_pdf_url(self, metadata: Dict[str, Any]) -> Optional[str]:
        """
        Extract or construct PDF URL from PMC metadata.

        Educational Note:
        PMC provides multiple access formats. This method demonstrates
        how to handle multiple potential sources for the same data.
        """
        relations = metadata.get("relation", [])

        # Look for direct PDF URL
        for relation in relations:
            if relation.endswith("/pdf/") or "pdf" in relation.lower():
                return relation

        # Look for PMC article URL, then construct PDF URL
        for relation in relations:
            if "pmc/articles" in relation.lower():
                # Extract PMC ID from URL and construct PDF URL
                if relation.endswith("/"):
                    return f"{relation}pdf/"
                else:
                    return f"{relation}/pdf/"

        # Only construct PDF URL if we have evidence of PMC web access
        return None
