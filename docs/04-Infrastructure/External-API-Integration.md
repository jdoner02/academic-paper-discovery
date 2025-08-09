# External API Integration - Academic Paper Source Adapters

## 🎯 Overview

The External API Integration system provides a unified interface for accessing multiple academic paper sources including arXiv, PubMed, Google Scholar, Semantic Scholar, and institutional repositories. This demonstrates the Adapter Pattern, port-based architecture, and sophisticated error handling for external service integration.

## 🏗️ Integration Architecture

### Design Principles

**Unified Interface:**
- Single port interface for all paper sources
- Consistent data models across different APIs
- Standardized error handling and retry logic
- Transparent rate limiting and caching

**Adapter Pattern Implementation:**
- Each external service has its own adapter
- Adapters translate between external formats and domain models
- Isolates external API changes from business logic
- Enables easy addition of new paper sources

**Resilience and Reliability:**
- Circuit breaker pattern for failing services
- Exponential backoff retry strategies
- Fallback mechanisms for service unavailability
- Comprehensive monitoring and alerting

## 📋 Paper Source Port Interface

### Port Definition

```python
# research-core/src/application/ports/paper_source_port.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, AsyncIterator
from dataclasses import dataclass
from datetime import datetime, date
import asyncio

from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.search_query import SearchQuery
from ...domain.value_objects.doi import DOI
from ...domain.exceptions.domain_exceptions import (
    PaperSourceError,
    RateLimitExceededError,
    ServiceUnavailableError
)

@dataclass(frozen=True)
class SearchMetadata:
    """
    Metadata about search results from external sources.
    
    Educational Notes:
    - Immutable value object for search context
    - Provides transparency about search execution
    - Enables analytics and optimization
    """
    source: str
    total_results: int
    results_returned: int
    search_time_ms: int
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset_time: Optional[datetime] = None
    query_cost: Optional[float] = None
    cached_results: bool = False

@dataclass(frozen=True)
class SearchResult:
    """Complete search result with papers and metadata."""
    papers: List[ResearchPaper]
    metadata: SearchMetadata
    next_page_token: Optional[str] = None
    has_more_results: bool = False

class PaperSourcePort(ABC):
    """
    Port interface for academic paper sources.
    
    This interface demonstrates:
    - Hexagonal architecture with port-adapter pattern
    - Consistent interface across different external services
    - Async/await for non-blocking I/O operations
    - Rich error handling for external service issues
    - Pagination support for large result sets
    """
    
    @abstractmethod
    async def search_papers(
        self, 
        query: SearchQuery,
        max_results: int = 100,
        page_token: Optional[str] = None
    ) -> SearchResult:
        """
        Search for papers using the given query.
        
        Args:
            query: SearchQuery value object with search criteria
            max_results: Maximum number of results to return
            page_token: Token for pagination (if supported)
            
        Returns:
            SearchResult with papers and metadata
            
        Raises:
            PaperSourceError: General API error
            RateLimitExceededError: Rate limit exceeded
            ServiceUnavailableError: Service temporarily unavailable
        """
        pass
    
    @abstractmethod
    async def get_paper_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """
        Retrieve a specific paper by its DOI.
        
        Args:
            doi: DOI value object for the paper
            
        Returns:
            ResearchPaper if found, None otherwise
            
        Raises:
            PaperSourceError: API error during retrieval
        """
        pass
    
    @abstractmethod
    async def get_paper_by_id(self, source_id: str) -> Optional[ResearchPaper]:
        """
        Retrieve a paper by its source-specific ID.
        
        Args:
            source_id: Source-specific identifier
            
        Returns:
            ResearchPaper if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_cited_papers(
        self, 
        paper: ResearchPaper,
        max_results: int = 50
    ) -> List[ResearchPaper]:
        """
        Get papers that cite the given paper.
        
        Args:
            paper: The paper to find citations for
            max_results: Maximum number of citing papers to return
            
        Returns:
            List of papers that cite the given paper
        """
        pass
    
    @abstractmethod
    async def get_references(
        self, 
        paper: ResearchPaper,
        max_results: int = 50
    ) -> List[ResearchPaper]:
        """
        Get papers referenced by the given paper.
        
        Args:
            paper: The paper to find references for
            max_results: Maximum number of references to return
            
        Returns:
            List of papers referenced by the given paper
        """
        pass
    
    @abstractmethod
    async def stream_papers(
        self, 
        query: SearchQuery
    ) -> AsyncIterator[ResearchPaper]:
        """
        Stream papers for large result sets.
        
        Args:
            query: SearchQuery value object with search criteria
            
        Yields:
            Individual ResearchPaper objects
            
        Note:
            Use this for processing large datasets without loading
            all results into memory at once.
        """
        pass
    
    @abstractmethod
    async def get_source_info(self) -> Dict[str, Any]:
        """
        Get information about this paper source.
        
        Returns:
            Dictionary with source metadata like rate limits,
            supported features, API version, etc.
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the source is available and responding.
        
        Returns:
            True if source is healthy, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of this paper source (e.g., 'arxiv', 'pubmed')."""
        pass
    
    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Whether this source supports streaming results."""
        pass
    
    @property
    @abstractmethod
    def supports_citations(self) -> bool:
        """Whether this source supports citation lookup."""
        pass
    
    @property
    @abstractmethod
    def rate_limit_info(self) -> Dict[str, Any]:
        """Current rate limit information."""
        pass
```

## 🔌 arXiv Adapter Implementation

### arXiv-Specific Implementation

```python
# research-core/src/infrastructure/adapters/arxiv_adapter.py

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Optional, Dict, Any, AsyncIterator
from datetime import datetime, date
import re
import logging
from urllib.parse import quote

from ...application.ports.paper_source_port import (
    PaperSourcePort, 
    SearchResult, 
    SearchMetadata
)
from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.search_query import SearchQuery
from ...domain.value_objects.doi import DOI
from ...domain.value_objects.paper_id import PaperId
from ...domain.exceptions.domain_exceptions import (
    PaperSourceError,
    RateLimitExceededError,
    ServiceUnavailableError
)

logger = logging.getLogger(__name__)

class ArxivAdapter(PaperSourcePort):
    """
    Adapter for arXiv API integration.
    
    This adapter demonstrates:
    - REST API integration with XML response parsing
    - Rate limiting and respectful API usage
    - Error handling for external service issues
    - Data transformation from external format to domain models
    - Async/await for non-blocking operations
    
    Educational Notes:
    - Adapter Pattern: Translates between arXiv API and our domain
    - Dependency Inversion: Implements port interface
    - Single Responsibility: Only handles arXiv-specific logic
    - Open/Closed: Easy to extend without modifying existing code
    """
    
    def __init__(
        self, 
        base_url: str = "http://export.arxiv.org/api/query",
        max_requests_per_second: float = 0.5,  # arXiv recommendation
        timeout_seconds: int = 30,
        max_retries: int = 3
    ):
        self._base_url = base_url
        self._request_delay = 1.0 / max_requests_per_second
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._last_request_time = 0.0
        self._session: Optional[aiohttp.ClientSession] = None
    
    @property
    def source_name(self) -> str:
        """Name of this paper source."""
        return "arxiv"
    
    @property
    def supports_streaming(self) -> bool:
        """arXiv supports streaming through pagination."""
        return True
    
    @property
    def supports_citations(self) -> bool:
        """arXiv does not provide citation information."""
        return False
    
    @property
    def rate_limit_info(self) -> Dict[str, Any]:
        """Current rate limit information for arXiv."""
        return {
            "requests_per_second": 0.5,
            "recommendation": "No more than 1 request every 3 seconds",
            "burst_limit": None,
            "current_delay": self._request_delay
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    'User-Agent': 'Research-Paper-Aggregator/1.0 (Educational Project)'
                }
            )
        return self._session
    
    async def _rate_limited_request(self, url: str, params: Dict[str, Any]) -> str:
        """
        Make a rate-limited request to arXiv API.
        
        Educational Notes:
        - Implements respectful API usage
        - Prevents overwhelming external services
        - Uses exponential backoff for retries
        """
        session = await self._get_session()
        
        # Enforce rate limiting
        current_time = asyncio.get_event_loop().time()
        time_since_last = current_time - self._last_request_time
        if time_since_last < self._request_delay:
            await asyncio.sleep(self._request_delay - time_since_last)
        
        self._last_request_time = asyncio.get_event_loop().time()
        
        # Make request with retries
        for attempt in range(self._max_retries):
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 429:
                        # Rate limited - wait longer
                        wait_time = (2 ** attempt) * self._request_delay
                        logger.warning(f"Rate limited by arXiv, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                        continue
                    elif response.status >= 500:
                        # Server error - retry
                        if attempt < self._max_retries - 1:
                            wait_time = 2 ** attempt
                            logger.warning(f"arXiv server error {response.status}, retrying in {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            raise ServiceUnavailableError(f"arXiv service unavailable: {response.status}")
                    else:
                        raise PaperSourceError(f"arXiv API error: {response.status}")
                        
            except asyncio.TimeoutError:
                if attempt < self._max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"arXiv request timeout, retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise ServiceUnavailableError("arXiv API timeout")
            except aiohttp.ClientError as e:
                if attempt < self._max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"arXiv client error: {e}, retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise PaperSourceError(f"arXiv connection error: {e}")
        
        raise PaperSourceError("Max retries exceeded for arXiv API")
    
    def _build_search_query(self, query: SearchQuery) -> str:
        """
        Build arXiv-specific query string.
        
        Educational Notes:
        - Transforms domain SearchQuery to external API format
        - Handles different search field mappings
        - Demonstrates data translation in adapter pattern
        """
        query_parts = []
        
        # Add search terms to appropriate fields
        if query.terms:
            # Search in title, abstract, and comments
            terms_query = " AND ".join(f'"{term}"' for term in query.terms)
            query_parts.append(f"(ti:{terms_query} OR abs:{terms_query})")
        
        # Add author constraints
        if query.authors:
            author_queries = []
            for author in query.authors:
                # arXiv author search format
                author_queries.append(f'au:"{author}"')
            query_parts.append(f"({' OR '.join(author_queries)})")
        
        # Add date range if specified
        if query.date_range:
            if query.date_range.start_date:
                start_date = query.date_range.start_date.strftime("%Y%m%d")
                query_parts.append(f"submittedDate:[{start_date}0000 TO *]")
            if query.date_range.end_date:
                end_date = query.date_range.end_date.strftime("%Y%m%d")
                query_parts.append(f"submittedDate:[* TO {end_date}2359]")
        
        # Combine all parts
        full_query = " AND ".join(query_parts) if query_parts else "all:*"
        
        logger.debug(f"Built arXiv query: {full_query}")
        return full_query
    
    def _parse_atom_feed(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse arXiv Atom feed response.
        
        Educational Notes:
        - XML parsing and data extraction
        - Error handling for malformed responses
        - Defensive programming with missing fields
        """
        try:
            root = ET.fromstring(xml_content)
            
            # Define namespaces used in arXiv Atom feed
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            entries = []
            for entry in root.findall('atom:entry', namespaces):
                try:
                    # Extract basic information
                    entry_data = {}
                    
                    # Title
                    title_elem = entry.find('atom:title', namespaces)
                    entry_data['title'] = title_elem.text.strip() if title_elem is not None else "No Title"
                    
                    # Abstract
                    summary_elem = entry.find('atom:summary', namespaces)
                    entry_data['abstract'] = summary_elem.text.strip() if summary_elem is not None else ""
                    
                    # Authors
                    authors = []
                    for author in entry.findall('atom:author', namespaces):
                        name_elem = author.find('atom:name', namespaces)
                        if name_elem is not None:
                            authors.append(name_elem.text.strip())
                    entry_data['authors'] = authors
                    
                    # arXiv ID and URL
                    id_elem = entry.find('atom:id', namespaces)
                    if id_elem is not None:
                        arxiv_url = id_elem.text.strip()
                        # Extract arXiv ID from URL
                        arxiv_id = arxiv_url.split('/')[-1]
                        entry_data['arxiv_id'] = arxiv_id
                        entry_data['url'] = arxiv_url
                    
                    # Published date
                    published_elem = entry.find('atom:published', namespaces)
                    if published_elem is not None:
                        # Parse ISO datetime
                        published_str = published_elem.text.strip()
                        entry_data['published_date'] = datetime.fromisoformat(
                            published_str.replace('Z', '+00:00')
                        ).date()
                    
                    # Updated date
                    updated_elem = entry.find('atom:updated', namespaces)
                    if updated_elem is not None:
                        updated_str = updated_elem.text.strip()
                        entry_data['updated_date'] = datetime.fromisoformat(
                            updated_str.replace('Z', '+00:00')
                        ).date()
                    
                    # Categories (subject classifications)
                    categories = []
                    for category in entry.findall('atom:category', namespaces):
                        term = category.get('term')
                        if term:
                            categories.append(term)
                    entry_data['categories'] = categories
                    
                    # DOI (if available)
                    doi_elem = entry.find('arxiv:doi', namespaces)
                    if doi_elem is not None:
                        entry_data['doi'] = doi_elem.text.strip()
                    
                    # Journal reference (if available)
                    journal_elem = entry.find('arxiv:journal_ref', namespaces)
                    if journal_elem is not None:
                        entry_data['journal_reference'] = journal_elem.text.strip()
                    
                    # Comment (if available)
                    comment_elem = entry.find('arxiv:comment', namespaces)
                    if comment_elem is not None:
                        entry_data['comment'] = comment_elem.text.strip()
                    
                    entries.append(entry_data)
                    
                except Exception as e:
                    logger.warning(f"Error parsing arXiv entry: {e}")
                    continue
            
            return entries
            
        except ET.ParseError as e:
            raise PaperSourceError(f"Invalid XML response from arXiv: {e}")
        except Exception as e:
            raise PaperSourceError(f"Error parsing arXiv response: {e}")
    
    def _create_research_paper(self, entry_data: Dict[str, Any]) -> ResearchPaper:
        """
        Create ResearchPaper entity from arXiv entry data.
        
        Educational Notes:
        - Data transformation from external format to domain model
        - Handling optional fields and missing data
        - Domain entity creation with validation
        """
        try:
            # Create paper ID
            arxiv_id = entry_data.get('arxiv_id', '')
            paper_id = PaperId.create_arxiv_id(arxiv_id)
            
            # Handle DOI if present
            doi = None
            if entry_data.get('doi'):
                try:
                    doi = DOI(entry_data['doi'])
                except ValueError:
                    logger.warning(f"Invalid DOI in arXiv entry: {entry_data['doi']}")
            
            # Create research paper
            paper = ResearchPaper.create(
                paper_id=paper_id,
                title=entry_data.get('title', 'No Title'),
                authors=entry_data.get('authors', []),
                abstract=entry_data.get('abstract', ''),
                doi=doi,
                publication_date=entry_data.get('published_date'),
                url=entry_data.get('url', ''),
                source='arxiv'
            )
            
            # Add arXiv-specific metadata
            if entry_data.get('categories'):
                paper.add_keywords(entry_data['categories'])
            
            if entry_data.get('journal_reference'):
                paper.set_venue(entry_data['journal_reference'])
            
            if entry_data.get('comment'):
                paper.add_note(f"arXiv comment: {entry_data['comment']}")
            
            return paper
            
        except Exception as e:
            logger.error(f"Error creating ResearchPaper from arXiv data: {e}")
            raise PaperSourceError(f"Failed to create paper from arXiv data: {e}")
    
    async def search_papers(
        self, 
        query: SearchQuery,
        max_results: int = 100,
        page_token: Optional[str] = None
    ) -> SearchResult:
        """Search for papers on arXiv."""
        start_time = datetime.now()
        
        try:
            # Build arXiv query
            arxiv_query = self._build_search_query(query)
            
            # Set up pagination
            start_index = 0
            if page_token:
                try:
                    start_index = int(page_token)
                except ValueError:
                    logger.warning(f"Invalid page token: {page_token}")
            
            # Prepare API parameters
            params = {
                'search_query': arxiv_query,
                'start': start_index,
                'max_results': min(max_results, 1000),  # arXiv limit
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            # Make API request
            logger.info(f"Searching arXiv: {arxiv_query}")
            xml_response = await self._rate_limited_request(self._base_url, params)
            
            # Parse response
            entries = self._parse_atom_feed(xml_response)
            
            # Convert to domain objects
            papers = []
            for entry_data in entries:
                try:
                    paper = self._create_research_paper(entry_data)
                    papers.append(paper)
                except Exception as e:
                    logger.warning(f"Failed to create paper from arXiv entry: {e}")
                    continue
            
            # Calculate search time
            search_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Create metadata
            metadata = SearchMetadata(
                source=self.source_name,
                total_results=len(entries),  # arXiv doesn't provide total count
                results_returned=len(papers),
                search_time_ms=int(search_time),
                cached_results=False
            )
            
            # Determine if there are more results
            has_more = len(entries) == max_results
            next_token = str(start_index + max_results) if has_more else None
            
            return SearchResult(
                papers=papers,
                metadata=metadata,
                next_page_token=next_token,
                has_more_results=has_more
            )
            
        except Exception as e:
            logger.error(f"arXiv search failed: {e}")
            if isinstance(e, (PaperSourceError, RateLimitExceededError, ServiceUnavailableError)):
                raise
            else:
                raise PaperSourceError(f"Unexpected error during arXiv search: {e}")
    
    async def get_paper_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """Retrieve paper by DOI from arXiv."""
        # arXiv doesn't have good DOI search, so we'll search by DOI string
        query = SearchQuery(
            terms=[str(doi)],
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=1
        )
        
        result = await self.search_papers(query, max_results=1)
        
        # Look for exact DOI match
        for paper in result.papers:
            if paper.doi == doi:
                return paper
        
        return None
    
    async def get_paper_by_id(self, source_id: str) -> Optional[ResearchPaper]:
        """Retrieve paper by arXiv ID."""
        try:
            # arXiv ID format: "1234.5678" or "math-ph/0123456"
            params = {
                'id_list': source_id,
                'max_results': 1
            }
            
            xml_response = await self._rate_limited_request(self._base_url, params)
            entries = self._parse_atom_feed(xml_response)
            
            if entries:
                return self._create_research_paper(entries[0])
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get arXiv paper by ID {source_id}: {e}")
            return None
    
    async def get_cited_papers(
        self, 
        paper: ResearchPaper,
        max_results: int = 50
    ) -> List[ResearchPaper]:
        """arXiv does not provide citation information."""
        logger.warning("arXiv does not support citation lookup")
        return []
    
    async def get_references(
        self, 
        paper: ResearchPaper,
        max_results: int = 50
    ) -> List[ResearchPaper]:
        """arXiv does not provide reference information."""
        logger.warning("arXiv does not support reference lookup")
        return []
    
    async def stream_papers(
        self, 
        query: SearchQuery
    ) -> AsyncIterator[ResearchPaper]:
        """Stream papers from arXiv using pagination."""
        page_token = None
        batch_size = 100
        
        while True:
            try:
                result = await self.search_papers(
                    query, 
                    max_results=batch_size,
                    page_token=page_token
                )
                
                # Yield each paper
                for paper in result.papers:
                    yield paper
                
                # Check if there are more results
                if not result.has_more_results or not result.next_page_token:
                    break
                
                page_token = result.next_page_token
                
                # Add small delay between batches
                await asyncio.sleep(self._request_delay)
                
            except Exception as e:
                logger.error(f"Error during arXiv streaming: {e}")
                break
    
    async def get_source_info(self) -> Dict[str, Any]:
        """Get information about arXiv source."""
        return {
            "name": self.source_name,
            "description": "arXiv preprint repository",
            "base_url": self._base_url,
            "supports_streaming": self.supports_streaming,
            "supports_citations": self.supports_citations,
            "rate_limit": self.rate_limit_info,
            "api_documentation": "https://arxiv.org/help/api/user-manual",
            "coverage": {
                "disciplines": [
                    "Physics", "Mathematics", "Computer Science", 
                    "Quantitative Biology", "Statistics", "Economics"
                ],
                "start_year": 1991,
                "update_frequency": "Daily"
            }
        }
    
    async def health_check(self) -> bool:
        """Check if arXiv is available."""
        try:
            # Simple query to test connectivity
            params = {
                'search_query': 'all:test',
                'max_results': 1
            }
            
            await self._rate_limited_request(self._base_url, params)
            return True
            
        except Exception as e:
            logger.warning(f"arXiv health check failed: {e}")
            return False
    
    async def close(self):
        """Clean up resources."""
        if self._session and not self._session.closed:
            await self._session.close()
```

## 🧪 Testing External Integrations

### Adapter Testing Strategy

```python
# tests/unit/infrastructure/test_arxiv_adapter.py

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import date

from infrastructure.adapters.arxiv_adapter import ArxivAdapter
from domain.value_objects.search_query import SearchQuery, DateRange
from domain.value_objects.doi import DOI
from domain.exceptions.domain_exceptions import (
    PaperSourceError,
    ServiceUnavailableError
)

class TestArxivAdapter:
    """Test suite for arXiv adapter."""
    
    @pytest.fixture
    def adapter(self):
        """Create arXiv adapter for testing."""
        return ArxivAdapter(
            max_requests_per_second=10.0,  # Faster for testing
            timeout_seconds=5,
            max_retries=2
        )
    
    @pytest.fixture
    def sample_arxiv_response(self):
        """Sample arXiv XML response for testing."""
        return '''<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <id>http://arxiv.org/abs/2401.12345v1</id>
                <title>Sample Machine Learning Paper</title>
                <summary>This is a sample abstract about machine learning.</summary>
                <author>
                    <name>John Doe</name>
                </author>
                <author>
                    <name>Jane Smith</name>
                </author>
                <published>2024-01-15T10:30:00Z</published>
                <updated>2024-01-15T10:30:00Z</updated>
                <category term="cs.LG" />
                <category term="cs.AI" />
            </entry>
        </feed>'''
    
    def test_adapter_properties(self, adapter):
        """Test adapter property values."""
        assert adapter.source_name == "arxiv"
        assert adapter.supports_streaming is True
        assert adapter.supports_citations is False
        
        rate_info = adapter.rate_limit_info
        assert "requests_per_second" in rate_info
        assert rate_info["requests_per_second"] == 10.0
    
    def test_build_search_query_basic_terms(self, adapter):
        """Test building search query with basic terms."""
        # Arrange
        query = SearchQuery(
            terms=["machine learning", "neural networks"],
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=100
        )
        
        # Act
        arxiv_query = adapter._build_search_query(query)
        
        # Assert
        assert "machine learning" in arxiv_query
        assert "neural networks" in arxiv_query
        assert "ti:" in arxiv_query or "abs:" in arxiv_query
    
    def test_build_search_query_with_authors(self, adapter):
        """Test building search query with author constraints."""
        # Arrange
        query = SearchQuery(
            terms=["quantum computing"],
            authors=["John Doe", "Jane Smith"],
            date_range=None,
            venue_filter=None,
            max_results=100
        )
        
        # Act
        arxiv_query = adapter._build_search_query(query)
        
        # Assert
        assert "quantum computing" in arxiv_query
        assert "au:" in arxiv_query
        assert "John Doe" in arxiv_query
        assert "Jane Smith" in arxiv_query
    
    def test_build_search_query_with_date_range(self, adapter):
        """Test building search query with date constraints."""
        # Arrange
        date_range = DateRange(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        )
        query = SearchQuery(
            terms=["deep learning"],
            authors=[],
            date_range=date_range,
            venue_filter=None,
            max_results=100
        )
        
        # Act
        arxiv_query = adapter._build_search_query(query)
        
        # Assert
        assert "submittedDate:" in arxiv_query
        assert "20230101" in arxiv_query
        assert "20231231" in arxiv_query
    
    def test_parse_atom_feed_valid_response(self, adapter, sample_arxiv_response):
        """Test parsing valid arXiv Atom feed."""
        # Act
        entries = adapter._parse_atom_feed(sample_arxiv_response)
        
        # Assert
        assert len(entries) == 1
        entry = entries[0]
        
        assert entry['title'] == "Sample Machine Learning Paper"
        assert entry['abstract'] == "This is a sample abstract about machine learning."
        assert len(entry['authors']) == 2
        assert "John Doe" in entry['authors']
        assert "Jane Smith" in entry['authors']
        assert entry['arxiv_id'] == "2401.12345v1"
        assert "cs.LG" in entry['categories']
        assert "cs.AI" in entry['categories']
    
    def test_parse_atom_feed_invalid_xml(self, adapter):
        """Test parsing invalid XML raises appropriate error."""
        # Arrange
        invalid_xml = "This is not valid XML"
        
        # Act & Assert
        with pytest.raises(PaperSourceError, match="Invalid XML response"):
            adapter._parse_atom_feed(invalid_xml)
    
    def test_create_research_paper_from_entry(self, adapter):
        """Test creating ResearchPaper from arXiv entry data."""
        # Arrange
        entry_data = {
            'title': 'Test Paper',
            'abstract': 'Test abstract',
            'authors': ['Author One', 'Author Two'],
            'arxiv_id': '2401.12345',
            'published_date': date(2024, 1, 15),
            'url': 'http://arxiv.org/abs/2401.12345',
            'categories': ['cs.LG', 'cs.AI'],
            'doi': '10.1000/test.doi'
        }
        
        # Act
        paper = adapter._create_research_paper(entry_data)
        
        # Assert
        assert paper.title == 'Test Paper'
        assert paper.abstract == 'Test abstract'
        assert len(paper.authors) == 2
        assert paper.source == 'arxiv'
        assert str(paper.doi) == '10.1000/test.doi'
        assert paper.url == 'http://arxiv.org/abs/2401.12345'
    
    @pytest.mark.asyncio
    async def test_search_papers_success(self, adapter, sample_arxiv_response):
        """Test successful paper search."""
        # Arrange
        query = SearchQuery(
            terms=["machine learning"],
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=10
        )
        
        with patch.object(adapter, '_rate_limited_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = sample_arxiv_response
            
            # Act
            result = await adapter.search_papers(query, max_results=10)
            
            # Assert
            assert len(result.papers) == 1
            assert result.metadata.source == "arxiv"
            assert result.metadata.results_returned == 1
            assert result.metadata.search_time_ms > 0
            
            # Verify API call
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert 'search_query' in call_args[0][1]  # params
    
    @pytest.mark.asyncio
    async def test_search_papers_with_pagination(self, adapter, sample_arxiv_response):
        """Test paper search with pagination."""
        # Arrange
        query = SearchQuery(
            terms=["AI"],
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=10
        )
        
        with patch.object(adapter, '_rate_limited_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = sample_arxiv_response
            
            # Act
            result = await adapter.search_papers(query, max_results=10, page_token="50")
            
            # Assert
            call_args = mock_request.call_args
            params = call_args[0][1]
            assert params['start'] == 50
    
    @pytest.mark.asyncio
    async def test_get_paper_by_id_success(self, adapter, sample_arxiv_response):
        """Test retrieving paper by arXiv ID."""
        # Arrange
        arxiv_id = "2401.12345"
        
        with patch.object(adapter, '_rate_limited_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = sample_arxiv_response
            
            # Act
            paper = await adapter.get_paper_by_id(arxiv_id)
            
            # Assert
            assert paper is not None
            assert paper.title == "Sample Machine Learning Paper"
            
            # Verify API call
            call_args = mock_request.call_args
            params = call_args[0][1]
            assert params['id_list'] == arxiv_id
    
    @pytest.mark.asyncio
    async def test_get_paper_by_id_not_found(self, adapter):
        """Test retrieving non-existent paper by ID."""
        # Arrange
        empty_response = '''<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
        </feed>'''
        
        with patch.object(adapter, '_rate_limited_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = empty_response
            
            # Act
            paper = await adapter.get_paper_by_id("nonexistent.id")
            
            # Assert
            assert paper is None
    
    @pytest.mark.asyncio
    async def test_rate_limiting_enforcement(self, adapter):
        """Test that rate limiting is properly enforced."""
        # Arrange
        adapter._request_delay = 0.1  # 100ms delay
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value="<feed></feed>")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Act - Make two requests rapidly
            start_time = asyncio.get_event_loop().time()
            await adapter._rate_limited_request("http://test.com", {})
            await adapter._rate_limited_request("http://test.com", {})
            end_time = asyncio.get_event_loop().time()
            
            # Assert - Second request should be delayed
            assert (end_time - start_time) >= 0.1
    
    @pytest.mark.asyncio
    async def test_rate_limit_error_handling(self, adapter):
        """Test handling of rate limit errors from arXiv."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # First request returns 429 (rate limited)
            # Second request succeeds
            mock_responses = [
                AsyncMock(status=429),
                AsyncMock(status=200, text=AsyncMock(return_value="<feed></feed>"))
            ]
            
            mock_get.return_value.__aenter__.side_effect = mock_responses
            
            # Act - Should retry and succeed
            response = await adapter._rate_limited_request("http://test.com", {})
            
            # Assert
            assert response == "<feed></feed>"
            assert mock_get.call_count == 2
    
    @pytest.mark.asyncio
    async def test_service_unavailable_error(self, adapter):
        """Test handling of service unavailable errors."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock(status=503)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Act & Assert
            with pytest.raises(ServiceUnavailableError):
                await adapter._rate_limited_request("http://test.com", {})
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, adapter):
        """Test successful health check."""
        with patch.object(adapter, '_rate_limited_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = "<feed></feed>"
            
            # Act
            is_healthy = await adapter.health_check()
            
            # Assert
            assert is_healthy is True
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self, adapter):
        """Test failed health check."""
        with patch.object(adapter, '_rate_limited_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = ServiceUnavailableError("Service down")
            
            # Act
            is_healthy = await adapter.health_check()
            
            # Assert
            assert is_healthy is False
    
    @pytest.mark.asyncio
    async def test_stream_papers(self, adapter):
        """Test streaming papers with pagination."""
        # Arrange
        query = SearchQuery(
            terms=["test"],
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=100
        )
        
        # Mock multiple pages of results
        with patch.object(adapter, 'search_papers', new_callable=AsyncMock) as mock_search:
            # First page has results and indicates more
            # Second page has no results
            from application.ports.paper_source_port import SearchResult, SearchMetadata
            from domain.entities.research_paper import ResearchPaper
            from domain.value_objects.paper_id import PaperId
            
            sample_paper = ResearchPaper.create(
                paper_id=PaperId.create_arxiv_id("test.123"),
                title="Test Paper",
                authors=["Test Author"],
                abstract="Test abstract",
                source="arxiv"
            )
            
            mock_search.side_effect = [
                SearchResult(
                    papers=[sample_paper],
                    metadata=SearchMetadata(
                        source="arxiv",
                        total_results=1,
                        results_returned=1,
                        search_time_ms=100
                    ),
                    next_page_token="100",
                    has_more_results=True
                ),
                SearchResult(
                    papers=[],
                    metadata=SearchMetadata(
                        source="arxiv",
                        total_results=0,
                        results_returned=0,
                        search_time_ms=50
                    ),
                    next_page_token=None,
                    has_more_results=False
                )
            ]
            
            # Act
            papers = []
            async for paper in adapter.stream_papers(query):
                papers.append(paper)
            
            # Assert
            assert len(papers) == 1
            assert papers[0].title == "Test Paper"
            assert mock_search.call_count == 2
    
    @pytest.mark.asyncio
    async def test_cleanup_resources(self, adapter):
        """Test resource cleanup."""
        # Arrange - Create a mock session
        mock_session = AsyncMock()
        mock_session.closed = False
        adapter._session = mock_session
        
        # Act
        await adapter.close()
        
        # Assert
        mock_session.close.assert_called_once()
```

## 🔗 Related Documentation

- **[[Paper-Discovery-UseCase]]**: How adapters integrate with the main discovery workflow
- **[[Research-Paper-Entity]]**: Domain model that adapters populate
- **[[Error-Handling-Patterns]]**: Comprehensive error handling strategies
- **[[Configuration-Management]]**: How adapter behavior is configured
- **[[Caching-Strategy]]**: Performance optimization for external API calls

## 🚀 Extension Points

### Additional Adapters

1. **PubMed Adapter**: Medical research papers
2. **Google Scholar Adapter**: Broad academic coverage
3. **Semantic Scholar Adapter**: AI-powered paper analysis
4. **IEEE Xplore Adapter**: Engineering and computer science
5. **ACM Digital Library Adapter**: Computing research

### Enhanced Features

1. **Circuit Breaker Pattern**: Automatic service degradation
2. **Response Caching**: Intelligent caching strategies
3. **Parallel Searching**: Concurrent searches across sources
4. **Result Merging**: Deduplication and ranking across sources
5. **Quality Scoring**: Source-specific quality assessment

---

*The External API Integration system demonstrates how to build robust, resilient interfaces to external services while maintaining clean architecture principles and comprehensive error handling.*
