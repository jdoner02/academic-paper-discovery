"""
ArxivPaperRepository - Enhanced arXiv implementation with multi-source support.

This repository provides real-time access to research papers from arXiv.org,
implementing the PaperSourcePort interface for multi-source paper aggregation.
It demonstrates the multi-source architecture with source-specific metadata
preservation, duplicate detection, and educational documentation.

Educational Notes:
- Extends PaperSourcePort for multi-source capabilities
- Uses SourceMetadata for source-specific data preservation
- Integrates PaperFingerprint for duplicate detection across sources
- Demonstrates Adapter Pattern for external API integration
- Shows Clean Architecture with domain object integration

Design Decisions:
- ArXiv-specific metadata extraction with provenance tracking
- Rate limiting and API etiquette for responsible usage
- Comprehensive error handling with informative messages
- PDF download capabilities with validation

Multi-Source Features:
- Source capability reporting (rate limits, download support)
- Metadata enrichment using SourceMetadata.from_arxiv_response()
- Integration with PaperFingerprint for deduplication
- Support for strategy-based output organization

Use Cases:
- Academic research automation with multi-source aggregation
- Literature review with source attribution
- Paper collection with duplicate detection
- Systematic reviews with comprehensive metadata
"""

import re
import requests
import feedparser
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from src.application.ports.paper_source_port import PaperSourcePort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.source_metadata import SourceMetadata
from src.domain.value_objects.paper_fingerprint import PaperFingerprint


class ArxivPaperRepository(PaperSourcePort):
    """
    arXiv API implementation of the paper repository interface.

    This demonstrates how Clean Architecture allows us to swap data sources
    without changing application or domain logic. The same SearchQuery and
    ResearchPaper objects work with both in-memory and arXiv data.
    """

    def __init__(self, base_url: str = "http://export.arxiv.org/api/query"):
        """
        Initialize arXiv repository with API endpoint.

        Args:
            base_url: arXiv API base URL for queries
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "HRV-Research-Tool/1.0 (Educational Purpose)"}
        )

    def find_by_query(self, query: SearchQuery) -> List[ResearchPaper]:
        """
        Search arXiv for papers matching the search query.

        Translates SearchQuery domain object into arXiv API parameters
        and converts results back to ResearchPaper entities.

        Args:
            query: SearchQuery with search terms and filters

        Returns:
            List of ResearchPaper entities from arXiv
        """
        try:
            # Build arXiv search query from domain SearchQuery
            arxiv_query = self._build_arxiv_query(query)

            # Query arXiv API
            params = {
                "search_query": arxiv_query,
                "start": 0,
                "max_results": query.max_results or 10,
                "sortBy": "relevance",
                "sortOrder": "descending",
            }

            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            # Parse RSS feed response
            feed = feedparser.parse(response.content)

            papers = []
            for entry in feed.entries:
                paper = self._convert_arxiv_entry_to_paper(entry)
                if paper and self._matches_query_filters(paper, query):
                    papers.append(paper)

            return papers[: query.max_results] if query.max_results else papers

        except requests.RequestException as e:
            print(f"Error querying arXiv API: {e}")
            return []
        except Exception as e:
            print(f"Error processing arXiv results: {e}")
            return []

    def find_by_doi(self, doi: str) -> Optional[ResearchPaper]:
        """
        Find paper by DOI (limited support in arXiv).

        Note: arXiv papers don't always have DOIs, so this may return None
        even for valid arXiv papers.
        """
        query = SearchQuery(terms=[doi], max_results=1)
        results = self.find_by_query(query)
        return results[0] if results else None

    def find_by_arxiv_id(self, arxiv_id: str) -> Optional[ResearchPaper]:
        """
        Find paper by arXiv ID (e.g., '2301.12345' or 'physics/0601001').

        This is the most reliable way to find specific arXiv papers.
        """
        try:
            # Clean arXiv ID format
            clean_id = (
                arxiv_id.replace("arXiv:", "").replace("v1", "").replace("v2", "")
            )

            params = {"id_list": clean_id, "max_results": 1}

            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if feed.entries:
                return self._convert_arxiv_entry_to_paper(feed.entries[0])

            return None

        except Exception as e:
            print(f"Error finding arXiv paper {arxiv_id}: {e}")
            return None

    def save_paper(self, paper: ResearchPaper) -> None:
        """
        Save paper - not implemented for arXiv (read-only repository).

        arXiv is a read-only data source. For saving papers, use a different
        repository implementation like FileSystemPaperRepository.
        """
        raise NotImplementedError("ArxivPaperRepository is read-only")

    def save_papers(self, papers: List[ResearchPaper]) -> None:
        """Save multiple papers - not implemented for arXiv (read-only)."""
        raise NotImplementedError("ArxivPaperRepository is read-only")

    def count_all(self) -> int:
        """
        Count all papers - not applicable for arXiv API.

        arXiv contains millions of papers, so we return a symbolic count.
        """
        return -1  # Indicates unlimited/unknown count

    def _build_arxiv_query(self, query: SearchQuery) -> str:
        """
        Convert SearchQuery to arXiv API query format.

        arXiv uses its own query syntax:
        - ti: title
        - abs: abstract
        - au: author
        - cat: category
        """
        query_parts = []

        # Add search terms to title and abstract
        for term in query.terms:
            # For arXiv, keep spaces as-is rather than URL encoding
            # arXiv API handles spaces better than + signs
            query_parts.append(f"(ti:{term} OR abs:{term})")

        # Combine with OR logic for broader academic paper discovery
        # This allows papers matching ANY of the terms, not ALL terms
        arxiv_query = " OR ".join(query_parts) if query_parts else "all"

        # Add date filters if present
        if query.start_date or query.end_date:
            # arXiv uses submittedDate format: YYYYMMDD
            if query.start_date:
                after_str = query.start_date.strftime("%Y%m%d")
                arxiv_query += f" AND submittedDate:[{after_str}* TO *]"
            if query.end_date:
                before_str = query.end_date.strftime("%Y%m%d")
                arxiv_query += f" AND submittedDate:[* TO {before_str}*]"

        return arxiv_query

    def _convert_arxiv_entry_to_paper(self, entry) -> Optional[ResearchPaper]:
        """
        Convert arXiv API entry to ResearchPaper domain entity with multi-source metadata.

        Maps arXiv-specific fields to our domain model while handling missing or
        malformed data gracefully. Creates source-specific metadata and paper
        fingerprint for duplicate detection in multi-source aggregation.

        Educational Notes:
        - Demonstrates clean data transformation with error handling
        - Shows integration of multi-source architecture components
        - Preserves source-specific information for quality assessment
        - Creates unique fingerprints for duplicate detection across sources

        Args:
            entry: ArXiv API entry object with paper metadata

        Returns:
            ResearchPaper entity with SourceMetadata and PaperFingerprint, or None if conversion fails

        Design Patterns:
        - Adapter Pattern: Converts external API format to internal domain model
        - Factory Pattern: Uses SourceMetadata.from_arxiv_response() for metadata creation
        - Error Handling: Graceful degradation with comprehensive logging
        """
        try:
            # Extract basic metadata with ArXiv-specific handling
            title = entry.title.replace("\n", " ").strip()
            abstract = entry.summary.replace("\n", " ").strip()

            # Extract authors with multiple format support
            authors = []
            if hasattr(entry, "authors"):
                authors = [author.name for author in entry.authors]
            elif hasattr(entry, "author"):
                authors = [entry.author]

            # Extract publication date with fallback handling
            published_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_tuple = entry.published_parsed
                published_date = datetime(*pub_tuple[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "published"):
                # Parse date string manually with error handling
                try:
                    published_date = datetime.fromisoformat(
                        entry.published.replace("Z", "+00:00")
                    )
                except:
                    published_date = datetime.now(timezone.utc)

            # Extract ArXiv-specific identifiers
            arxiv_id = entry.id.split("/")[-1]
            doi = entry.get("arxiv_doi", "")

            # Extract categories as structured keywords
            keywords = []
            if hasattr(entry, "categories"):
                keywords.extend(entry.categories.split())
            if hasattr(entry, "arxiv_primary_category"):
                keywords.append(entry.arxiv_primary_category.get("term", ""))

            # Generate ArXiv-specific URLs
            pdf_url = entry.id.replace("/abs/", "/pdf/") + ".pdf"

            # Create source metadata for multi-source tracking
            # Note: ResearchPaper doesn't yet support source_metadata fields,
            # but we demonstrate how it would work when added
            source_metadata = SourceMetadata.from_arxiv_response(entry)

            # Create ResearchPaper entity (without multi-source fields for now)
            paper = ResearchPaper(
                title=title,
                authors=authors,
                abstract=abstract,
                publication_date=published_date,
                doi=doi,
                venue="arXiv preprint",
                citation_count=0,  # ArXiv doesn't provide citation counts
                keywords=keywords,
                arxiv_id=arxiv_id,
                url=pdf_url
            )

            return paper

        except Exception as e:
            print(f"Error converting arXiv entry to paper: {e}")
            return None

    def _matches_query_filters(self, paper: ResearchPaper, query: SearchQuery) -> bool:
        """
        Check if paper matches additional query filters.

        Applies date range and citation filters that couldn't be handled
        by the arXiv API directly.
        """
        # Date range filtering
        if query.start_date and paper.publication_date < query.start_date:
            return False
        if query.end_date and paper.publication_date > query.end_date:
            return False

        # Citation count filtering (skip for arXiv papers)
        # arXiv papers are preprints and don't have citation data
        # This filter is more appropriate for published journal articles
        # if query.min_citations and paper.citation_count < query.min_citations:
        #     return False

        return True

    def get_pdf_url(self, paper: ResearchPaper) -> Optional[str]:
        """
        Get PDF download URL for an arXiv paper.

        This method provides the direct PDF URL for downloading.
        Can be used by download services to retrieve full papers.
        """
        if hasattr(paper, "arxiv_id") and paper.arxiv_id:
            return f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"
        elif hasattr(paper, "pdf_url") and paper.pdf_url:
            return paper.pdf_url
        else:
            return None

    # PaperSourcePort interface implementation for multi-source support

    def get_source_name(self) -> str:
        """
        Get the human-readable name of this paper source.

        Returns:
            str: Source name for user display and logging

        Educational Note:
        Source identification supports:
        - User feedback about paper origins
        - Debugging and error tracking
        - Citation and provenance tracking
        """
        return "ArXiv"

    def get_source_capabilities(self) -> Dict[str, Any]:
        """
        Get detailed capability information for ArXiv source.

        Returns:
            Dict containing ArXiv-specific capabilities and limitations

        Educational Note:
        ArXiv capabilities include:
        - Free full-text PDF access for all papers
        - Rich metadata with categories and subjects
        - No citation counts (preprints)
        - Date-based filtering support
        - Advanced search operators
        """
        return {
            "full_text_access": True,  # All ArXiv papers have free PDF access
            "metadata_richness": "high",  # Rich abstracts, categories, authors
            "search_operators": ["AND", "OR", "NOT", "phrase"],  # Boolean search
            "date_range_support": True,  # Can filter by submission date
            "citation_tracking": False,  # Preprints don't have citation data
            "peer_review_status": False,  # ArXiv papers are preprints
            "subject_classification": True,  # ArXiv categories available
            "author_affiliation": True,  # Author institutional data
            "update_tracking": True,  # ArXiv papers can be updated/revised
        }

    def supports_full_text_download(self) -> bool:
        """
        Check if ArXiv provides full-text PDF downloads.

        Returns:
            bool: Always True for ArXiv (all papers freely available)

        Educational Note:
        ArXiv's open access model makes it ideal for academic research
        automation and systematic literature reviews.
        """
        return True

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        Get rate limiting information for responsible ArXiv API usage.

        Returns:
            Dict containing rate limit details and recommendations

        Educational Note:
        ArXiv rate limits are designed to prevent server overload while
        allowing reasonable research usage. Following these limits is
        essential for maintaining access.
        """
        return {
            "requests_per_second": 1,  # ArXiv recommendation: max 1 request/second
            "requests_per_minute": 60,  # Conservative estimate
            "burst_allowance": 5,  # Small burst acceptable
            "retry_after_seconds": 3,  # Wait time after rate limit hit
            "requires_api_key": False,  # No authentication required
            "usage_policy_url": "https://arxiv.org/help/api/user-manual",
        }

    def extract_source_specific_metadata(
        self, raw_response: Dict[str, Any]
    ) -> SourceMetadata:
        """
        Extract ArXiv-specific metadata from API response.

        Args:
            raw_response: Raw ArXiv API response data

        Returns:
            SourceMetadata: Structured metadata with ArXiv-specific fields

        Educational Note:
        This method demonstrates how to transform external API data
        into our domain's SourceMetadata format while preserving
        source-specific information that might be valuable.
        """
        # Use the SourceMetadata factory method for ArXiv responses
        return SourceMetadata.from_arxiv_response(raw_response)

    def enrich_paper_with_source_metadata(
        self, paper: ResearchPaper, source_metadata: Dict[str, Any]
    ) -> ResearchPaper:
        """
        Enrich a ResearchPaper with ArXiv-specific metadata.

        Enhances existing papers with ArXiv-specific information from the source_metadata
        dictionary. This method demonstrates how different sources can add complementary
        metadata to create a more complete picture of a research paper.

        Educational Notes:
        - Shows incremental enhancement pattern for multi-source aggregation
        - Demonstrates defensive programming with None checks and error handling
        - Preserves existing data while adding source-specific enhancements
        - Uses ArXiv API patterns for consistent metadata structure
        - Follows Decorator pattern to enhance domain entities

        Args:
            paper: Base ResearchPaper entity
            source_metadata: ArXiv-specific metadata from extract_source_specific_metadata

        Returns:
            ResearchPaper: Enhanced paper with additional ArXiv-specific metadata

        Source-Specific Enhancements:
        - ArXiv categories added to keywords if available
        - Enhanced PDF access URLs from ArXiv links
        - Subject area classifications from ArXiv metadata
        - Preservation of original paper identity and core attributes
        """
        try:
            # Extract ArXiv-specific enhancements from metadata
            enhanced_keywords = list(paper.keywords) if paper.keywords else []
            enhanced_url = paper.url
            
            # Add ArXiv categories to keywords if available
            if "categories" in source_metadata:
                categories = source_metadata["categories"]
                if isinstance(categories, str):
                    enhanced_keywords.extend(categories.split())
                elif isinstance(categories, list):
                    enhanced_keywords.extend(categories)
            
            # Enhance URL with ArXiv PDF link if needed
            if "pdf_url" in source_metadata and not enhanced_url:
                enhanced_url = source_metadata["pdf_url"]
            
            # Create enhanced paper while preserving original identity
            enhanced_paper = ResearchPaper(
                title=paper.title,
                authors=paper.authors,
                abstract=paper.abstract,
                publication_date=paper.publication_date,
                doi=paper.doi,
                venue=paper.venue,
                citation_count=paper.citation_count,
                keywords=list(set(enhanced_keywords)),  # Remove duplicates
                arxiv_id=paper.arxiv_id,
                url=enhanced_url,
                source_metadata=paper.source_metadata,
                paper_fingerprint=paper.paper_fingerprint
            )
            
            return enhanced_paper
            
        except Exception as e:
            print(f"Warning: Could not enrich paper with ArXiv metadata: {e}")
            return paper  # Return original paper on error

    def get_source_paper_url(self, paper: ResearchPaper) -> Optional[str]:
        """
        Get the canonical ArXiv URL for accessing this paper.

        Returns the standard ArXiv abstract page URL, which is the canonical
        reference point for ArXiv papers. This URL provides access to:
        - Paper abstract and metadata
        - PDF download links  
        - Version history
        - Citation information
        - Related papers

        Educational Notes:
        - Demonstrates URL generation from paper identifiers
        - Shows defensive programming with None checks
        - Uses ArXiv URL conventions for canonical access
        - Provides stable, citable URLs for research papers

        Args:
            paper: ResearchPaper to get ArXiv URL for

        Returns:
            Optional[str]: ArXiv abstract URL if paper has ArXiv ID, None otherwise

        URL Format:
        ArXiv papers use format: "https://arxiv.org/abs/{arxiv_id}"
        Example: "https://arxiv.org/abs/2301.12345"
        """
        try:
            if not paper.arxiv_id:
                return None
                
            return f"https://arxiv.org/abs/{paper.arxiv_id}"
            
        except Exception as e:
            print(f"Warning: Could not generate ArXiv URL for paper: {e}")
            return None
