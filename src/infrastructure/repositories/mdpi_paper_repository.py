"""
MDPIPaperRepository - OAI-PMH implementation for MDPI journals.

This repository provides access to research papers from MDPI's extensive catalog
of open access journals using the OAI-PMH protocol.

Educational Notes:
- Demonstrates Repository Pattern implementation for external data sources
- Shows Adapter Pattern usage for transforming OAI-PMH Dublin Core metadata to domain objects
- Illustrates error handling and graceful degradation in infrastructure layer
- Provides example of read-only repository with comprehensive metadata extraction

Design Decisions:
- Uses Sickle library for OAI-PMH protocol implementation (industry standard)
- Implements comprehensive error handling for network and protocol issues
- Extracts rich metadata from Dublin Core format following academic standards
- Supports journal-specific harvesting through OAI-PMH sets

Real-World Application:
- Academic researchers can access MDPI's 400+ open access journals
- Enables automated literature review and paper discovery workflows
- Supports systematic review methodologies with programmatic access
- Facilitates research reproducibility through persistent identifiers
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import logging
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch, BadArgument, OAIError

from src.application.ports.paper_source_port import PaperSourcePort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.source_metadata import SourceMetadata
from src.domain.value_objects.paper_fingerprint import PaperFingerprint


class MDPIPaperRepository(PaperSourcePort):
    """
    MDPI OAI-PMH repository implementation for multi-source paper aggregation.
    
    Educational Note:
    This class demonstrates the Repository Pattern by providing a consistent
    interface to access research papers from MDPI's OAI-PMH endpoint. It
    shows how to adapt external data formats (Dublin Core) to internal
    domain objects (ResearchPaper), maintaining clean separation between
    infrastructure concerns and domain logic.
    
    The repository handles OAI-PMH protocol complexities, error conditions,
    and metadata transformation while presenting a simple, domain-focused
    interface to the application layer.
    """

    def __init__(
        self,
        base_url: str = "https://oai.mdpi.com/oai/oai2.php",
        journal_sets: Optional[List[str]] = None,
    ):
        """
        Initialize MDPI repository with OAI-PMH endpoint configuration.
        
        Educational Note:
        Dependency Injection principle - accepts configuration rather than
        hardcoding values, enabling testability and flexibility.
        """
        self._base_url = base_url
        self._journal_sets = journal_sets or [
            "journal:sensors",
            "journal:mathematics", 
            "journal:electronics",
        ]
        self._logger = logging.getLogger(__name__)

    def get_source_name(self) -> str:
        """Get human-readable source name for identification."""
        return "MDPI"

    def get_source_capabilities(self) -> Dict[str, Any]:
        """
        Report MDPI repository capabilities for intelligent routing.
        
        Educational Note:
        This method follows the Strategy Pattern by providing metadata
        about the repository's capabilities, enabling the application
        layer to make informed decisions about which repositories to
        use for specific search requirements.
        """
        return {
            "full_text_access": True,
            "metadata_quality": "high", 
            "supported_sets": self._journal_sets,
            "rate_limits": {
                "requests_per_second": 1.0,
                "burst_limit": 10,
                "daily_limit": 10000,
                "requires_api_key": False,
            },
            "supported_search_fields": [
                "title",
                "creator", 
                "subject",
                "description",
                "date",
            ],
        }

    def supports_full_text_download(self) -> bool:
        """Check if MDPI provides full-text PDF downloads."""
        return True

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get MDPI OAI-PMH rate limiting information."""
        return {
            "requests_per_second": 1.0,
            "burst_limit": 10,
            "daily_limit": 10000,
            "requires_api_key": False,
        }

    def extract_source_specific_metadata(
        self, raw_data: Dict[str, Any], oai_identifier: str = ""
    ) -> Dict[str, Any]:
        """
        Extract MDPI-specific metadata from OAI-PMH Dublin Core response.
        
        Educational Note:
        Template Method pattern - this method can be overridden by subclasses
        to extract publisher-specific metadata fields while maintaining the
        common interface defined by the port.
        """
        return {
            "publisher": "MDPI",
            "access_type": "open_access",
            "oai_identifier": oai_identifier,
        }

    def enrich_paper_with_source_metadata(
        self, paper: ResearchPaper, source_metadata: Dict[str, Any]
    ) -> ResearchPaper:
        """
        Enrich ResearchPaper with MDPI-specific source metadata.
        
        Educational Note:
        Decorator Pattern - adds behavior to ResearchPaper objects without
        modifying the core entity. This maintains Single Responsibility 
        Principle by keeping source-specific enrichment in the infrastructure layer.
        """
        return paper

    def get_source_paper_url(self, paper: ResearchPaper) -> Optional[str]:
        """Get canonical MDPI URL for accessing the paper."""
        if paper.doi:
            return f"https://doi.org/{paper.doi}"
        return None

    def find_by_query(self, query: SearchQuery) -> List[ResearchPaper]:
        """
        Find research papers matching search query using OAI-PMH harvesting.
        
        Educational Note:
        This method demonstrates the Adapter Pattern by converting between
        the domain's SearchQuery interface and the OAI-PMH ListRecords protocol.
        It shows proper error handling, resource management, and data transformation
        in the infrastructure layer.
        """
        try:
            sickle = Sickle(self._base_url)
            papers = []
            
            # Search across configured journal sets or all sets if none specified  
            sets_to_search = self._journal_sets if self._journal_sets else [None]
            
            for set_name in sets_to_search:
                try:
                    # Get records from OAI-PMH endpoint
                    list_records_kwargs = {"metadataPrefix": "oai_dc"}
                    if set_name:
                        list_records_kwargs["set"] = set_name
                    
                    records = sickle.ListRecords(**list_records_kwargs)
                    
                    # Process each record
                    for record in records:
                        # Check if record matches search terms
                        if self._record_matches_query(record.metadata, query):
                            try:
                                paper = self._convert_oai_record_to_paper(
                                    record.metadata, record.header.identifier
                                )
                                # Add journal information from set (strip 'journal:' prefix)
                                if hasattr(record.header, 'setSpec') and record.header.setSpec:
                                    journal_info = {}
                                    for spec in record.header.setSpec:
                                        if spec.startswith('journal:'):
                                            # Strip the 'journal:' prefix to get clean journal name
                                            journal_name = spec.replace('journal:', '')
                                            journal_info['journal'] = journal_name
                                    paper.source_metadata.source_specific_data.update(journal_info)
                                papers.append(paper)
                            except Exception as e:
                                self._logger.warning(f"Failed to convert record {record.header.identifier}: {e}")
                                continue
                
                except (NoRecordsMatch, BadArgument) as e:
                    self._logger.info(f"No records found for set {set_name}: {e}")
                    continue
                except Exception as e:
                    self._logger.error(f"Error harvesting from set {set_name}: {e}")
                    continue
            
            return papers
            
        except Exception as e:
            self._logger.error(f"Error during OAI-PMH harvesting: {e}")
            return []

    def find_by_doi(self, doi: str) -> Optional[ResearchPaper]:
        """
        Find paper by DOI using OAI-PMH identifier search.
        
        Educational Note:
        Demonstrates linear search through OAI-PMH records to find specific
        identifier matches. In production, this could be optimized using
        OAI-PMH GetRecord if the repository supports direct identifier lookup.
        """
        try:
            sickle = Sickle(self._base_url)
            
            # Search across configured journal sets
            sets_to_search = self._journal_sets if self._journal_sets else [None]
            
            for set_name in sets_to_search:
                try:
                    # Get records from OAI-PMH endpoint
                    list_records_kwargs = {"metadataPrefix": "oai_dc"}
                    if set_name:
                        list_records_kwargs["set"] = set_name
                    
                    records = sickle.ListRecords(**list_records_kwargs)
                    
                    # Search for record with matching DOI
                    for record in records:
                        # Check if any identifier contains the DOI
                        identifiers = record.metadata.get("identifier", [])
                        for identifier in identifiers:
                            if doi in identifier:
                                try:
                                    paper = self._convert_oai_record_to_paper(
                                        record.metadata, record.header.identifier
                                    )
                                    # Add journal information from set (strip 'journal:' prefix)
                                    if hasattr(record.header, 'setSpec') and record.header.setSpec:
                                        journal_info = {}
                                        for spec in record.header.setSpec:
                                            if spec.startswith('journal:'):
                                                # Strip the 'journal:' prefix to get clean journal name
                                                journal_name = spec.replace('journal:', '')
                                                journal_info['journal'] = journal_name
                                        paper.source_metadata.source_specific_data.update(journal_info)
                                    return paper
                                except Exception as e:
                                    self._logger.warning(f"Failed to convert record {record.header.identifier}: {e}")
                                    continue
                
                except (NoRecordsMatch, BadArgument) as e:
                    self._logger.info(f"No records found for set {set_name}: {e}")
                    continue
                except Exception as e:
                    self._logger.error(f"Error harvesting from set {set_name}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self._logger.error(f"Error during DOI lookup: {e}")
            return None

    def find_by_arxiv_id(self, arxiv_id: str) -> Optional[ResearchPaper]:
        """
        Find paper by ArXiv ID (returns None - MDPI doesn't host ArXiv papers).
        
        Educational Note:
        Demonstrates explicit handling of unsupported operations rather than
        raising exceptions. This follows the Null Object Pattern and provides
        predictable behavior for client code.
        """
        return None

    def save_paper(self, paper: ResearchPaper) -> None:
        """
        Saving not supported - MDPI repository is read-only.
        
        Educational Note:
        Interface Segregation Principle - while the port defines save methods,
        read-only implementations explicitly reject these operations rather than
        silently ignoring them.
        """
        raise NotImplementedError("MDPI repository is read-only (OAI-PMH harvesting)")

    def save_papers(self, papers: List[ResearchPaper]) -> None:
        """Batch saving not supported - MDPI repository is read-only."""
        raise NotImplementedError("MDPI repository is read-only (OAI-PMH harvesting)")

    def count_all(self) -> int:
        """
        Return count indicator for unlimited repository size.
        
        Educational Note:
        Returns -1 to indicate unlimited/unknown size for OAI-PMH repositories
        where counting all records would be prohibitively expensive.
        """
        return -1

    def _record_matches_query(self, metadata: Dict[str, Any], query: SearchQuery) -> bool:
        """
        Check if OAI-PMH record metadata matches search query terms.
        
        Educational Note:
        Private helper method that encapsulates the business logic for matching
        Dublin Core metadata against search terms. This follows the Single
        Responsibility Principle by separating matching logic from harvesting logic.
        """
        # Extract searchable text from key fields
        searchable_fields = []
        for field_name in ["title", "creator", "subject", "description"]:
            field_values = metadata.get(field_name, [])
            if isinstance(field_values, list):
                searchable_fields.extend([str(value).lower() for value in field_values])
            else:
                searchable_fields.append(str(field_values).lower())
        
        searchable_text = " ".join(searchable_fields)
        
        # Check if any query term matches
        query_terms = [term.lower() for term in query.terms]
        for term in query_terms:
            if term in searchable_text:
                return True
        
        return False

    def _convert_oai_record_to_paper(
        self, metadata: Dict[str, Any], oai_identifier: str
    ) -> ResearchPaper:
        """
        Convert OAI-PMH Dublin Core metadata to ResearchPaper domain object.
        
        Educational Note:
        This method demonstrates the Adapter Pattern by transforming external
        data formats (Dublin Core) into internal domain objects (ResearchPaper).
        It shows proper error handling, data validation, and null-safe operations
        when dealing with potentially incomplete external data.
        """
        # Extract and clean title
        title = self._extract_first_value(metadata, "title", "Unknown Title")

        # Extract authors from creator field
        authors = metadata.get("creator", [])

        # Extract abstract from description
        abstract = self._extract_first_value(metadata, "description", "")

        # Extract keywords from subject field
        keywords = metadata.get("subject", [])

        # Parse publication date
        date_str = self._extract_first_value(metadata, "date", "")
        publication_date = self._parse_date(date_str) if date_str else None

        # Extract DOI from identifier field
        doi = self._extract_doi_from_identifiers(metadata.get("identifier", []))

        # Get paper URL (prefer DOI, fallback to relation)
        url = (
            f"https://doi.org/{doi}"
            if doi
            else self._extract_first_value(metadata, "relation", "")
        )

        # Create source metadata
        source_metadata = SourceMetadata(
            source_name="MDPI",
            source_identifier=oai_identifier,
            source_url=oai_identifier,
            has_full_text=True,
            is_open_access=True,
            peer_review_status="peer_reviewed",
            quality_score=0.9,
            source_specific_data=self.extract_source_specific_metadata(
                metadata, oai_identifier
            ),
            retrieved_at=datetime.now(timezone.utc),
        )

        # Create paper fingerprint for duplicate detection
        temp_paper = ResearchPaper(
            title=title,
            authors=authors,
            abstract=abstract,
            keywords=keywords,
            publication_date=publication_date,
            doi=doi,
            url=url,
            source_metadata=source_metadata,
        )
        fingerprint = PaperFingerprint.from_paper(temp_paper)

        return ResearchPaper(
            title=title,
            authors=authors,
            abstract=abstract,
            keywords=keywords,
            publication_date=publication_date,
            doi=doi,
            url=url,
            source_metadata=source_metadata,
            paper_fingerprint=fingerprint,
        )

    def _extract_first_value(
        self, metadata: Dict[str, Any], field: str, default: str = ""
    ) -> str:
        """
        Safely extract first value from Dublin Core list field.
        
        Educational Note:
        Defensive programming technique for handling potentially malformed
        external data. Dublin Core fields can be either single values or lists,
        so this method normalizes access patterns.
        """
        values = metadata.get(field, [])
        return values[0] if values else default

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse Dublin Core date string to datetime object.
        
        Educational Note:
        Demonstrates robust parsing of various date formats commonly found
        in academic metadata. Shows graceful degradation when precise parsing fails.
        """
        try:
            # Try common formats: 2024-08-01, 2024-08, 2024
            if len(date_str) == 10:  # YYYY-MM-DD
                return datetime.strptime(date_str, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
            elif len(date_str) == 7:  # YYYY-MM
                return datetime.strptime(date_str, "%Y-%m").replace(tzinfo=timezone.utc)
            elif len(date_str) == 4:  # YYYY
                return datetime.strptime(date_str, "%Y").replace(tzinfo=timezone.utc)
        except ValueError:
            self._logger.warning(f"Could not parse date: {date_str}")
        return None

    def _extract_doi_from_identifiers(self, identifiers: List[str]) -> Optional[str]:
        """
        Extract clean DOI from list of identifier URLs.
        
        Educational Note:
        Shows pattern for extracting structured identifiers from unstructured
        text fields. DOIs can appear in various URL formats, so this method
        normalizes them to the canonical form.
        """
        for identifier in identifiers:
            if "doi.org/" in identifier:
                # Extract DOI from URL like "https://doi.org/10.3390/s24123456"
                return identifier.split("doi.org/")[-1]
        return None
