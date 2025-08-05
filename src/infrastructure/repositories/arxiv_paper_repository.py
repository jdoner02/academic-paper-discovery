"""
ArxivPaperRepository - arXiv API implementation of PaperRepositoryPort.

This repository provides real-time access to research papers from arXiv.org,
the largest repository of preprints in physics, mathematics, computer science,
and related fields including biomedical research.

Educational Notes:
- Demonstrates Repository Pattern with external API integration
- Shows how Clean Architecture enables swapping data sources
- Implements the same interface as InMemoryPaperRepository
- Provides real research paper discovery and access

Design Decisions:
- Uses arXiv API v1 for paper search and metadata retrieval
- Implements proper error handling for network requests
- Provides PDF download capabilities through arXiv URLs
- Maintains compatibility with existing SearchQuery value objects

Use Cases:
- Real research paper discovery for HRV studies
- Academic research automation
- Literature review assistance
- Paper collection for systematic reviews
"""

import re
import requests
import feedparser
from typing import List, Optional, Dict
from datetime import datetime, timezone

from application.ports.paper_repository_port import PaperRepositoryPort
from domain.entities.research_paper import ResearchPaper
from domain.value_objects.search_query import SearchQuery


class ArxivPaperRepository(PaperRepositoryPort):
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
        Convert arXiv API entry to ResearchPaper domain entity.

        Maps arXiv-specific fields to our domain model while handling
        missing or malformed data gracefully.
        """
        try:
            # Extract basic metadata
            title = entry.title.replace("\n", " ").strip()
            abstract = entry.summary.replace("\n", " ").strip()

            # Extract authors
            authors = []
            if hasattr(entry, "authors"):
                authors = [author.name for author in entry.authors]
            elif hasattr(entry, "author"):
                authors = [entry.author]

            # Extract publication date
            published_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_tuple = entry.published_parsed
                published_date = datetime(*pub_tuple[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "published"):
                # Parse date string manually
                try:
                    published_date = datetime.fromisoformat(
                        entry.published.replace("Z", "+00:00")
                    )
                except:
                    published_date = datetime.now(timezone.utc)

            # Extract arXiv ID and generate DOI if available
            arxiv_id = entry.id.split("/")[-1]
            doi = entry.get("arxiv_doi", "")

            # Extract categories as keywords
            keywords = []
            if hasattr(entry, "categories"):
                keywords.extend(entry.categories.split())
            if hasattr(entry, "arxiv_primary_category"):
                keywords.append(entry.arxiv_primary_category.get("term", ""))

            # Add arXiv URL for PDF access
            pdf_url = entry.id.replace("/abs/", "/pdf/") + ".pdf"

            # Create ResearchPaper entity
            paper = ResearchPaper(
                title=title,
                authors=authors,
                abstract=abstract,
                publication_date=published_date,
                doi=doi,
                venue="arXiv preprint",
                citation_count=0,  # arXiv doesn't provide citation counts
                keywords=keywords,
                arxiv_id=arxiv_id,
                url=pdf_url,  # Use url field instead of pdf_url
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
