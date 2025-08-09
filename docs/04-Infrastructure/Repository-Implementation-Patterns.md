# Repository Implementation Patterns - Data Access Layer

## 🎯 Overview

The Repository Implementation Patterns demonstrate various approaches to data persistence in the research paper aggregator system. This includes in-memory repositories for testing and demos, PostgreSQL repositories for production, Redis-based caching, and file system repositories for research data storage.

## 🏗️ Repository Architecture

### Design Principles

**Repository Pattern:**
- Encapsulates data access logic
- Provides collection-like interface for domain entities
- Abstracts storage implementation details
- Enables easy testing with mock implementations
- Supports multiple storage backends

**Data Access Patterns:**
- Unit of Work for transaction management
- Specification Pattern for complex queries
- Data Mapper for object-relational mapping
- Identity Map for object identity management
- Lazy Loading for performance optimization

## 📋 Base Repository Interface

### Abstract Repository Definition

```python
# research-core/src/application/ports/paper_repository_port.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Set
from uuid import UUID
from datetime import datetime, date

from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.paper_id import PaperId
from ...domain.value_objects.doi import DOI
from ...domain.value_objects.search_query import SearchQuery

class PaperRepositoryPort(ABC):
    """
    Repository port interface for research papers.
    
    This interface demonstrates:
    - Repository pattern for data access abstraction
    - Collection-like interface for domain entities
    - Support for various query patterns
    - Async operations for scalability
    - Specification pattern for complex queries
    
    Educational Notes:
    - Port-Adapter pattern: Defines interface implemented by adapters
    - Dependency Inversion: High-level modules depend on abstraction
    - Single Responsibility: Only handles paper data access
    - Interface Segregation: Focused on paper-specific operations
    """
    
    @abstractmethod
    async def save(self, paper: ResearchPaper) -> None:
        """
        Save or update a research paper.
        
        Args:
            paper: ResearchPaper entity to persist
            
        Note:
            Implementation should handle both insert and update cases
            based on whether the paper already exists.
        """
        pass
    
    @abstractmethod
    async def save_batch(self, papers: List[ResearchPaper]) -> None:
        """
        Save multiple papers in a batch operation.
        
        Args:
            papers: List of ResearchPaper entities to persist
            
        Note:
            Should be more efficient than individual saves for large datasets.
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, paper_id: PaperId) -> Optional[ResearchPaper]:
        """
        Retrieve a paper by its unique identifier.
        
        Args:
            paper_id: Unique identifier for the paper
            
        Returns:
            ResearchPaper if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """
        Retrieve a paper by its DOI.
        
        Args:
            doi: Digital Object Identifier
            
        Returns:
            ResearchPaper if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_title(self, title: str) -> List[ResearchPaper]:
        """
        Find papers with matching or similar titles.
        
        Args:
            title: Paper title to search for
            
        Returns:
            List of papers with similar titles
        """
        pass
    
    @abstractmethod
    async def search(
        self, 
        query: SearchQuery, 
        offset: int = 0, 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """
        Search papers using the given query criteria.
        
        Args:
            query: SearchQuery with search criteria
            offset: Number of results to skip (for pagination)
            limit: Maximum number of results to return
            
        Returns:
            List of matching papers
        """
        pass
    
    @abstractmethod
    async def search_by_keywords(
        self, 
        keywords: List[str], 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """
        Search papers by keywords.
        
        Args:
            keywords: List of keywords to search for
            limit: Maximum number of results to return
            
        Returns:
            List of papers matching the keywords
        """
        pass
    
    @abstractmethod
    async def get_by_authors(
        self, 
        authors: List[str], 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """
        Find papers by author names.
        
        Args:
            authors: List of author names to search for
            limit: Maximum number of results to return
            
        Returns:
            List of papers by the specified authors
        """
        pass
    
    @abstractmethod
    async def get_by_date_range(
        self, 
        start_date: date, 
        end_date: date,
        limit: int = 100
    ) -> List[ResearchPaper]:
        """
        Find papers published within a date range.
        
        Args:
            start_date: Earliest publication date
            end_date: Latest publication date
            limit: Maximum number of results to return
            
        Returns:
            List of papers published in the date range
        """
        pass
    
    @abstractmethod
    async def get_recent_papers(
        self, 
        days: int = 30, 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """
        Get recently published papers.
        
        Args:
            days: Number of days back to search
            limit: Maximum number of results to return
            
        Returns:
            List of recently published papers
        """
        pass
    
    @abstractmethod
    async def get_similar_papers(
        self, 
        paper: ResearchPaper, 
        limit: int = 10
    ) -> List[ResearchPaper]:
        """
        Find papers similar to the given paper.
        
        Args:
            paper: Reference paper to find similarities to
            limit: Maximum number of similar papers to return
            
        Returns:
            List of similar papers
        """
        pass
    
    @abstractmethod
    async def exists(self, paper_id: PaperId) -> bool:
        """
        Check if a paper exists in the repository.
        
        Args:
            paper_id: Paper identifier to check
            
        Returns:
            True if paper exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        Get total number of papers in the repository.
        
        Returns:
            Total count of papers
        """
        pass
    
    @abstractmethod
    async def count_by_source(self, source: str) -> int:
        """
        Get count of papers from a specific source.
        
        Args:
            source: Source name (e.g., 'arxiv', 'pubmed')
            
        Returns:
            Count of papers from the specified source
        """
        pass
    
    @abstractmethod
    async def delete(self, paper_id: PaperId) -> bool:
        """
        Delete a paper from the repository.
        
        Args:
            paper_id: Identifier of paper to delete
            
        Returns:
            True if paper was deleted, False if not found
        """
        pass
    
    @abstractmethod
    async def get_all_sources(self) -> Set[str]:
        """
        Get all unique source names in the repository.
        
        Returns:
            Set of source names
        """
        pass
    
    @abstractmethod
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get repository statistics.
        
        Returns:
            Dictionary with statistics like total papers,
            papers by source, date range, etc.
        """
        pass
```

## 💾 In-Memory Repository Implementation

### Development and Testing Repository

```python
# research-core/src/infrastructure/repositories/in_memory_paper_repository.py

from typing import List, Optional, Dict, Any, Set
from datetime import datetime, date, timedelta
import asyncio
from collections import defaultdict
import logging

from ...application.ports.paper_repository_port import PaperRepositoryPort
from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.paper_id import PaperId
from ...domain.value_objects.doi import DOI
from ...domain.value_objects.search_query import SearchQuery

logger = logging.getLogger(__name__)

class InMemoryPaperRepository(PaperRepositoryPort):
    """
    In-memory implementation of paper repository.
    
    This implementation demonstrates:
    - Repository pattern for data persistence
    - Thread-safe operations with asyncio
    - Collection-like interface for domain entities
    - Search and filtering capabilities
    - Performance optimizations with indexing
    
    Educational Notes:
    - Repository Pattern: Encapsulates data access logic
    - Strategy Pattern: Different search strategies
    - Observer Pattern: Could notify on changes
    - Template Method: Common search structure
    - Factory Pattern: Creates domain objects from data
    
    Use Cases:
    - Unit testing with controlled data
    - Development and prototyping
    - Demo environments
    - Small-scale applications
    - Caching layer for other repositories
    """
    
    def __init__(self):
        # Primary storage: paper_id -> ResearchPaper
        self._papers: Dict[str, ResearchPaper] = {}
        
        # Indexes for fast lookups
        self._doi_index: Dict[str, str] = {}  # doi -> paper_id
        self._title_index: Dict[str, Set[str]] = defaultdict(set)  # normalized_title -> paper_ids
        self._author_index: Dict[str, Set[str]] = defaultdict(set)  # author -> paper_ids
        self._keyword_index: Dict[str, Set[str]] = defaultdict(set)  # keyword -> paper_ids
        self._source_index: Dict[str, Set[str]] = defaultdict(set)  # source -> paper_ids
        self._date_index: Dict[date, Set[str]] = defaultdict(set)  # date -> paper_ids
        
        # Statistics cache
        self._stats_cache: Optional[Dict[str, Any]] = None
        self._stats_cache_time: Optional[datetime] = None
        
        # Async lock for thread safety
        self._lock = asyncio.Lock()
    
    async def save(self, paper: ResearchPaper) -> None:
        """Save or update a research paper."""
        async with self._lock:
            paper_id_str = str(paper.paper_id)
            
            # Remove from indexes if updating
            if paper_id_str in self._papers:
                await self._remove_from_indexes(self._papers[paper_id_str])
            
            # Store paper
            self._papers[paper_id_str] = paper
            
            # Update indexes
            await self._add_to_indexes(paper)
            
            # Invalidate stats cache
            self._stats_cache = None
            
            logger.debug(f"Saved paper: {paper.title}")
    
    async def save_batch(self, papers: List[ResearchPaper]) -> None:
        """Save multiple papers efficiently."""
        async with self._lock:
            for paper in papers:
                paper_id_str = str(paper.paper_id)
                
                # Remove from indexes if updating
                if paper_id_str in self._papers:
                    await self._remove_from_indexes(self._papers[paper_id_str])
                
                # Store paper
                self._papers[paper_id_str] = paper
                
                # Update indexes
                await self._add_to_indexes(paper)
            
            # Invalidate stats cache
            self._stats_cache = None
            
            logger.info(f"Saved batch of {len(papers)} papers")
    
    async def get_by_id(self, paper_id: PaperId) -> Optional[ResearchPaper]:
        """Retrieve paper by ID."""
        async with self._lock:
            return self._papers.get(str(paper_id))
    
    async def get_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """Retrieve paper by DOI."""
        async with self._lock:
            paper_id = self._doi_index.get(str(doi))
            if paper_id:
                return self._papers.get(paper_id)
            return None
    
    async def get_by_title(self, title: str) -> List[ResearchPaper]:
        """Find papers with matching titles."""
        async with self._lock:
            normalized_title = self._normalize_title(title)
            paper_ids = self._title_index.get(normalized_title, set())
            
            results = []
            for paper_id in paper_ids:
                if paper_id in self._papers:
                    results.append(self._papers[paper_id])
            
            return results
    
    async def search(
        self, 
        query: SearchQuery, 
        offset: int = 0, 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """Search papers using query criteria."""
        async with self._lock:
            # Start with all papers
            candidate_ids = set(self._papers.keys())
            
            # Filter by search terms
            if query.terms:
                term_matches = set()
                for term in query.terms:
                    # Search in titles
                    for title_words, paper_ids in self._title_index.items():
                        if term.lower() in title_words:
                            term_matches.update(paper_ids)
                    
                    # Search in keywords
                    for keyword, paper_ids in self._keyword_index.items():
                        if term.lower() in keyword.lower():
                            term_matches.update(paper_ids)
                
                candidate_ids = candidate_ids.intersection(term_matches)
            
            # Filter by authors
            if query.authors:
                author_matches = set()
                for author in query.authors:
                    author_key = self._normalize_author(author)
                    author_matches.update(self._author_index.get(author_key, set()))
                
                candidate_ids = candidate_ids.intersection(author_matches)
            
            # Filter by date range
            if query.date_range:
                date_matches = set()
                for date_key, paper_ids in self._date_index.items():
                    if self._is_date_in_range(date_key, query.date_range):
                        date_matches.update(paper_ids)
                
                candidate_ids = candidate_ids.intersection(date_matches)
            
            # Convert to papers and sort
            results = []
            for paper_id in candidate_ids:
                if paper_id in self._papers:
                    results.append(self._papers[paper_id])
            
            # Sort by relevance (simple publication date for now)
            results.sort(key=lambda p: p.publication_date or date.min, reverse=True)
            
            # Apply pagination
            return results[offset:offset + limit]
    
    async def search_by_keywords(
        self, 
        keywords: List[str], 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """Search papers by keywords."""
        async with self._lock:
            matching_ids = set()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                for indexed_keyword, paper_ids in self._keyword_index.items():
                    if keyword_lower in indexed_keyword.lower():
                        matching_ids.update(paper_ids)
            
            # Convert to papers
            results = []
            for paper_id in matching_ids:
                if paper_id in self._papers:
                    results.append(self._papers[paper_id])
                if len(results) >= limit:
                    break
            
            return results
    
    async def get_by_authors(
        self, 
        authors: List[str], 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """Find papers by authors."""
        async with self._lock:
            matching_ids = set()
            
            for author in authors:
                author_key = self._normalize_author(author)
                matching_ids.update(self._author_index.get(author_key, set()))
            
            # Convert to papers
            results = []
            for paper_id in matching_ids:
                if paper_id in self._papers:
                    results.append(self._papers[paper_id])
                if len(results) >= limit:
                    break
            
            return results
    
    async def get_by_date_range(
        self, 
        start_date: date, 
        end_date: date,
        limit: int = 100
    ) -> List[ResearchPaper]:
        """Find papers in date range."""
        async with self._lock:
            matching_ids = set()
            
            for date_key, paper_ids in self._date_index.items():
                if start_date <= date_key <= end_date:
                    matching_ids.update(paper_ids)
            
            # Convert to papers and sort by date
            results = []
            for paper_id in matching_ids:
                if paper_id in self._papers:
                    results.append(self._papers[paper_id])
            
            results.sort(key=lambda p: p.publication_date or date.min, reverse=True)
            return results[:limit]
    
    async def get_recent_papers(
        self, 
        days: int = 30, 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """Get recently published papers."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        return await self.get_by_date_range(start_date, end_date, limit)
    
    async def get_similar_papers(
        self, 
        paper: ResearchPaper, 
        limit: int = 10
    ) -> List[ResearchPaper]:
        """Find similar papers using simple keyword matching."""
        async with self._lock:
            if not paper.keywords:
                return []
            
            # Score papers by keyword overlap
            paper_scores = {}
            target_keywords = set(kw.lower() for kw in paper.keywords)
            
            for paper_id, stored_paper in self._papers.items():
                # Skip the same paper
                if paper_id == str(paper.paper_id):
                    continue
                
                if stored_paper.keywords:
                    stored_keywords = set(kw.lower() for kw in stored_paper.keywords)
                    overlap = len(target_keywords.intersection(stored_keywords))
                    if overlap > 0:
                        # Simple similarity score
                        total_keywords = len(target_keywords.union(stored_keywords))
                        similarity = overlap / total_keywords
                        paper_scores[stored_paper] = similarity
            
            # Sort by similarity and return top results
            similar_papers = sorted(
                paper_scores.keys(), 
                key=lambda p: paper_scores[p], 
                reverse=True
            )
            
            return similar_papers[:limit]
    
    async def exists(self, paper_id: PaperId) -> bool:
        """Check if paper exists."""
        async with self._lock:
            return str(paper_id) in self._papers
    
    async def count(self) -> int:
        """Get total number of papers."""
        async with self._lock:
            return len(self._papers)
    
    async def count_by_source(self, source: str) -> int:
        """Get count by source."""
        async with self._lock:
            return len(self._source_index.get(source, set()))
    
    async def delete(self, paper_id: PaperId) -> bool:
        """Delete a paper."""
        async with self._lock:
            paper_id_str = str(paper_id)
            
            if paper_id_str not in self._papers:
                return False
            
            paper = self._papers[paper_id_str]
            
            # Remove from all indexes
            await self._remove_from_indexes(paper)
            
            # Remove from primary storage
            del self._papers[paper_id_str]
            
            # Invalidate stats cache
            self._stats_cache = None
            
            logger.debug(f"Deleted paper: {paper.title}")
            return True
    
    async def get_all_sources(self) -> Set[str]:
        """Get all unique sources."""
        async with self._lock:
            return set(self._source_index.keys())
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics with caching."""
        async with self._lock:
            # Check cache validity (5 minutes)
            now = datetime.now()
            if (self._stats_cache and self._stats_cache_time and
                (now - self._stats_cache_time).seconds < 300):
                return self._stats_cache
            
            # Calculate fresh statistics
            total_papers = len(self._papers)
            
            # Count by source
            source_counts = {
                source: len(paper_ids) 
                for source, paper_ids in self._source_index.items()
            }
            
            # Date range
            if self._date_index:
                earliest_date = min(self._date_index.keys())
                latest_date = max(self._date_index.keys())
            else:
                earliest_date = latest_date = None
            
            # Author count
            unique_authors = len(self._author_index)
            
            # Keyword count
            unique_keywords = len(self._keyword_index)
            
            stats = {
                "total_papers": total_papers,
                "source_counts": source_counts,
                "date_range": {
                    "earliest": earliest_date,
                    "latest": latest_date
                },
                "unique_authors": unique_authors,
                "unique_keywords": unique_keywords,
                "last_updated": now.isoformat()
            }
            
            # Cache the results
            self._stats_cache = stats
            self._stats_cache_time = now
            
            return stats
    
    # Helper methods for indexing
    
    async def _add_to_indexes(self, paper: ResearchPaper) -> None:
        """Add paper to all indexes."""
        paper_id_str = str(paper.paper_id)
        
        # DOI index
        if paper.doi:
            self._doi_index[str(paper.doi)] = paper_id_str
        
        # Title index
        normalized_title = self._normalize_title(paper.title)
        self._title_index[normalized_title].add(paper_id_str)
        
        # Author index
        for author in paper.authors:
            author_key = self._normalize_author(author)
            self._author_index[author_key].add(paper_id_str)
        
        # Keyword index
        if paper.keywords:
            for keyword in paper.keywords:
                keyword_key = keyword.lower()
                self._keyword_index[keyword_key].add(paper_id_str)
        
        # Source index
        self._source_index[paper.source].add(paper_id_str)
        
        # Date index
        if paper.publication_date:
            self._date_index[paper.publication_date].add(paper_id_str)
    
    async def _remove_from_indexes(self, paper: ResearchPaper) -> None:
        """Remove paper from all indexes."""
        paper_id_str = str(paper.paper_id)
        
        # DOI index
        if paper.doi and str(paper.doi) in self._doi_index:
            del self._doi_index[str(paper.doi)]
        
        # Title index
        normalized_title = self._normalize_title(paper.title)
        self._title_index[normalized_title].discard(paper_id_str)
        if not self._title_index[normalized_title]:
            del self._title_index[normalized_title]
        
        # Author index
        for author in paper.authors:
            author_key = self._normalize_author(author)
            self._author_index[author_key].discard(paper_id_str)
            if not self._author_index[author_key]:
                del self._author_index[author_key]
        
        # Keyword index
        if paper.keywords:
            for keyword in paper.keywords:
                keyword_key = keyword.lower()
                self._keyword_index[keyword_key].discard(paper_id_str)
                if not self._keyword_index[keyword_key]:
                    del self._keyword_index[keyword_key]
        
        # Source index
        self._source_index[paper.source].discard(paper_id_str)
        if not self._source_index[paper.source]:
            del self._source_index[paper.source]
        
        # Date index
        if paper.publication_date:
            self._date_index[paper.publication_date].discard(paper_id_str)
            if not self._date_index[paper.publication_date]:
                del self._date_index[paper.publication_date]
    
    def _normalize_title(self, title: str) -> str:
        """Normalize title for indexing."""
        return title.lower().strip()
    
    def _normalize_author(self, author: str) -> str:
        """Normalize author name for indexing."""
        return author.lower().strip()
    
    def _is_date_in_range(self, check_date: date, date_range) -> bool:
        """Check if date is within the given range."""
        if date_range.start_date and check_date < date_range.start_date:
            return False
        if date_range.end_date and check_date > date_range.end_date:
            return False
        return True
    
    async def clear(self) -> None:
        """Clear all data (useful for testing)."""
        async with self._lock:
            self._papers.clear()
            self._doi_index.clear()
            self._title_index.clear()
            self._author_index.clear()
            self._keyword_index.clear()
            self._source_index.clear()
            self._date_index.clear()
            self._stats_cache = None
            
            logger.info("Cleared all repository data")
```

## 🐘 PostgreSQL Repository Implementation

### Production Database Repository

```python
# research-core/src/infrastructure/repositories/postgresql_paper_repository.py

from typing import List, Optional, Dict, Any, Set
from datetime import datetime, date, timedelta
import asyncio
import logging
import json
from uuid import UUID

import asyncpg
from asyncpg import Pool, Connection, Record

from ...application.ports.paper_repository_port import PaperRepositoryPort
from ...domain.entities.research_paper import ResearchPaper
from ...domain.value_objects.paper_id import PaperId
from ...domain.value_objects.doi import DOI
from ...domain.value_objects.search_query import SearchQuery
from ...domain.exceptions.domain_exceptions import (
    RepositoryError,
    PaperNotFoundError
)

logger = logging.getLogger(__name__)

class PostgreSQLPaperRepository(PaperRepositoryPort):
    """
    PostgreSQL implementation of paper repository.
    
    This implementation demonstrates:
    - Production-ready database integration
    - Async database operations with connection pooling
    - SQL query optimization and indexing
    - Transaction management and error handling
    - Full-text search capabilities
    - Data mapping between database and domain models
    
    Educational Notes:
    - Repository Pattern: Encapsulates database-specific logic
    - Data Mapper Pattern: Maps between database records and domain objects
    - Unit of Work Pattern: Could be extended for transaction management
    - Query Object Pattern: Complex queries as objects
    - Connection Pool Pattern: Efficient database connection management
    
    Database Schema:
    - research_papers: Main table with paper data
    - paper_authors: Many-to-many relationship for authors
    - paper_keywords: Many-to-many relationship for keywords
    - full_text_index: Optimized search index
    """
    
    def __init__(self, connection_pool: Pool):
        self._pool = connection_pool
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize database schema if needed."""
        if self._initialized:
            return
        
        async with self._pool.acquire() as conn:
            # Create tables if they don't exist
            await self._create_tables(conn)
            await self._create_indexes(conn)
            
        self._initialized = True
        logger.info("PostgreSQL repository initialized")
    
    async def _create_tables(self, conn: Connection) -> None:
        """Create database tables."""
        # Main papers table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS research_papers (
                id VARCHAR(255) PRIMARY KEY,
                title TEXT NOT NULL,
                abstract TEXT,
                doi VARCHAR(255) UNIQUE,
                url TEXT,
                source VARCHAR(100) NOT NULL,
                publication_date DATE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                citation_count INTEGER DEFAULT 0,
                quality_score FLOAT,
                venue TEXT,
                metadata JSONB
            )
        ''')
        
        # Authors table (many-to-many)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS paper_authors (
                paper_id VARCHAR(255) REFERENCES research_papers(id) ON DELETE CASCADE,
                author_name TEXT NOT NULL,
                author_order INTEGER DEFAULT 0,
                PRIMARY KEY (paper_id, author_name)
            )
        ''')
        
        # Keywords table (many-to-many)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS paper_keywords (
                paper_id VARCHAR(255) REFERENCES research_papers(id) ON DELETE CASCADE,
                keyword TEXT NOT NULL,
                PRIMARY KEY (paper_id, keyword)
            )
        ''')
        
        # Update triggers for timestamp
        await conn.execute('''
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        ''')
        
        await conn.execute('''
            DROP TRIGGER IF EXISTS update_research_papers_updated_at ON research_papers;
            CREATE TRIGGER update_research_papers_updated_at 
                BEFORE UPDATE ON research_papers 
                FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        ''')
    
    async def _create_indexes(self, conn: Connection) -> None:
        """Create database indexes for performance."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_papers_doi ON research_papers(doi)",
            "CREATE INDEX IF NOT EXISTS idx_papers_source ON research_papers(source)",
            "CREATE INDEX IF NOT EXISTS idx_papers_date ON research_papers(publication_date)",
            "CREATE INDEX IF NOT EXISTS idx_papers_created ON research_papers(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_authors_name ON paper_authors(author_name)",
            "CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON paper_keywords(keyword)",
            
            # Full-text search index
            '''CREATE INDEX IF NOT EXISTS idx_papers_fulltext 
             ON research_papers USING gin(to_tsvector('english', title || ' ' || COALESCE(abstract, '')))''',
            
            # Composite indexes for common queries
            "CREATE INDEX IF NOT EXISTS idx_papers_source_date ON research_papers(source, publication_date DESC)",
            "CREATE INDEX IF NOT EXISTS idx_papers_date_desc ON research_papers(publication_date DESC NULLS LAST)",
        ]
        
        for index_sql in indexes:
            try:
                await conn.execute(index_sql)
            except Exception as e:
                logger.warning(f"Failed to create index: {e}")
    
    async def save(self, paper: ResearchPaper) -> None:
        """Save or update a research paper."""
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                # Check if paper exists
                exists = await conn.fetchval(
                    "SELECT COUNT(*) FROM research_papers WHERE id = $1",
                    str(paper.paper_id)
                )
                
                if exists:
                    await self._update_paper(conn, paper)
                else:
                    await self._insert_paper(conn, paper)
    
    async def _insert_paper(self, conn: Connection, paper: ResearchPaper) -> None:
        """Insert new paper."""
        # Insert main paper record
        await conn.execute('''
            INSERT INTO research_papers 
            (id, title, abstract, doi, url, source, publication_date, 
             citation_count, quality_score, venue, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        ''', 
            str(paper.paper_id),
            paper.title,
            paper.abstract,
            str(paper.doi) if paper.doi else None,
            paper.url,
            paper.source,
            paper.publication_date,
            paper.citation_count,
            paper.quality_score,
            paper.venue,
            json.dumps(paper.metadata) if paper.metadata else None
        )
        
        # Insert authors
        if paper.authors:
            for i, author in enumerate(paper.authors):
                await conn.execute('''
                    INSERT INTO paper_authors (paper_id, author_name, author_order)
                    VALUES ($1, $2, $3)
                ''', str(paper.paper_id), author, i)
        
        # Insert keywords
        if paper.keywords:
            for keyword in paper.keywords:
                await conn.execute('''
                    INSERT INTO paper_keywords (paper_id, keyword)
                    VALUES ($1, $2)
                ''', str(paper.paper_id), keyword)
        
        logger.debug(f"Inserted paper: {paper.title}")
    
    async def _update_paper(self, conn: Connection, paper: ResearchPaper) -> None:
        """Update existing paper."""
        # Update main paper record
        await conn.execute('''
            UPDATE research_papers 
            SET title = $2, abstract = $3, doi = $4, url = $5, 
                publication_date = $6, citation_count = $7, 
                quality_score = $8, venue = $9, metadata = $10
            WHERE id = $1
        ''', 
            str(paper.paper_id),
            paper.title,
            paper.abstract,
            str(paper.doi) if paper.doi else None,
            paper.url,
            paper.publication_date,
            paper.citation_count,
            paper.quality_score,
            paper.venue,
            json.dumps(paper.metadata) if paper.metadata else None
        )
        
        # Delete existing authors and keywords
        await conn.execute(
            "DELETE FROM paper_authors WHERE paper_id = $1",
            str(paper.paper_id)
        )
        await conn.execute(
            "DELETE FROM paper_keywords WHERE paper_id = $1",
            str(paper.paper_id)
        )
        
        # Insert updated authors
        if paper.authors:
            for i, author in enumerate(paper.authors):
                await conn.execute('''
                    INSERT INTO paper_authors (paper_id, author_name, author_order)
                    VALUES ($1, $2, $3)
                ''', str(paper.paper_id), author, i)
        
        # Insert updated keywords
        if paper.keywords:
            for keyword in paper.keywords:
                await conn.execute('''
                    INSERT INTO paper_keywords (paper_id, keyword)
                    VALUES ($1, $2)
                ''', str(paper.paper_id), keyword)
        
        logger.debug(f"Updated paper: {paper.title}")
    
    async def save_batch(self, papers: List[ResearchPaper]) -> None:
        """Save multiple papers efficiently."""
        if not papers:
            return
        
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                # Prepare batch data
                paper_data = []
                author_data = []
                keyword_data = []
                
                for paper in papers:
                    paper_data.append((
                        str(paper.paper_id),
                        paper.title,
                        paper.abstract,
                        str(paper.doi) if paper.doi else None,
                        paper.url,
                        paper.source,
                        paper.publication_date,
                        paper.citation_count,
                        paper.quality_score,
                        paper.venue,
                        json.dumps(paper.metadata) if paper.metadata else None
                    ))
                    
                    # Collect author data
                    for i, author in enumerate(paper.authors):
                        author_data.append((str(paper.paper_id), author, i))
                    
                    # Collect keyword data
                    if paper.keywords:
                        for keyword in paper.keywords:
                            keyword_data.append((str(paper.paper_id), keyword))
                
                # Use COPY for efficient bulk insert
                await conn.copy_records_to_table(
                    'research_papers',
                    records=paper_data,
                    columns=['id', 'title', 'abstract', 'doi', 'url', 'source',
                            'publication_date', 'citation_count', 'quality_score',
                            'venue', 'metadata']
                )
                
                if author_data:
                    await conn.copy_records_to_table(
                        'paper_authors',
                        records=author_data,
                        columns=['paper_id', 'author_name', 'author_order']
                    )
                
                if keyword_data:
                    await conn.copy_records_to_table(
                        'paper_keywords',
                        records=keyword_data,
                        columns=['paper_id', 'keyword']
                    )
        
        logger.info(f"Saved batch of {len(papers)} papers")
    
    async def get_by_id(self, paper_id: PaperId) -> Optional[ResearchPaper]:
        """Retrieve paper by ID."""
        async with self._pool.acquire() as conn:
            # Get main paper data
            paper_record = await conn.fetchrow(
                "SELECT * FROM research_papers WHERE id = $1",
                str(paper_id)
            )
            
            if not paper_record:
                return None
            
            return await self._build_paper_from_record(conn, paper_record)
    
    async def get_by_doi(self, doi: DOI) -> Optional[ResearchPaper]:
        """Retrieve paper by DOI."""
        async with self._pool.acquire() as conn:
            paper_record = await conn.fetchrow(
                "SELECT * FROM research_papers WHERE doi = $1",
                str(doi)
            )
            
            if not paper_record:
                return None
            
            return await self._build_paper_from_record(conn, paper_record)
    
    async def search(
        self, 
        query: SearchQuery, 
        offset: int = 0, 
        limit: int = 100
    ) -> List[ResearchPaper]:
        """Search papers using full-text search and filters."""
        async with self._pool.acquire() as conn:
            # Build dynamic query
            conditions = []
            params = []
            param_index = 1
            
            # Full-text search on terms
            if query.terms:
                search_terms = ' & '.join(query.terms)
                conditions.append(f'''
                    to_tsvector('english', title || ' ' || COALESCE(abstract, '')) 
                    @@ plainto_tsquery('english', ${param_index})
                ''')
                params.append(search_terms)
                param_index += 1
            
            # Author filter
            if query.authors:
                author_placeholders = ', '.join(f'${i}' for i in range(param_index, param_index + len(query.authors)))
                conditions.append(f'''
                    EXISTS (
                        SELECT 1 FROM paper_authors pa 
                        WHERE pa.paper_id = rp.id 
                        AND pa.author_name = ANY(ARRAY[{author_placeholders}])
                    )
                ''')
                params.extend(query.authors)
                param_index += len(query.authors)
            
            # Date range filter
            if query.date_range:
                if query.date_range.start_date:
                    conditions.append(f'publication_date >= ${param_index}')
                    params.append(query.date_range.start_date)
                    param_index += 1
                if query.date_range.end_date:
                    conditions.append(f'publication_date <= ${param_index}')
                    params.append(query.date_range.end_date)
                    param_index += 1
            
            # Build final query
            where_clause = ' AND '.join(conditions) if conditions else 'TRUE'
            
            sql = f'''
                SELECT * FROM research_papers rp
                WHERE {where_clause}
                ORDER BY publication_date DESC NULLS LAST
                LIMIT ${param_index} OFFSET ${param_index + 1}
            '''
            params.extend([limit, offset])
            
            # Execute query
            records = await conn.fetch(sql, *params)
            
            # Build paper objects
            papers = []
            for record in records:
                paper = await self._build_paper_from_record(conn, record)
                papers.append(paper)
            
            return papers
    
    async def _build_paper_from_record(self, conn: Connection, record: Record) -> ResearchPaper:
        """Build ResearchPaper from database record."""
        paper_id_str = record['id']
        
        # Get authors
        author_records = await conn.fetch('''
            SELECT author_name FROM paper_authors 
            WHERE paper_id = $1 
            ORDER BY author_order
        ''', paper_id_str)
        authors = [r['author_name'] for r in author_records]
        
        # Get keywords
        keyword_records = await conn.fetch('''
            SELECT keyword FROM paper_keywords 
            WHERE paper_id = $1
        ''', paper_id_str)
        keywords = [r['keyword'] for r in keyword_records]
        
        # Parse metadata
        metadata = json.loads(record['metadata']) if record['metadata'] else {}
        
        # Create domain objects
        paper_id = PaperId.from_string(paper_id_str)
        doi = DOI(record['doi']) if record['doi'] else None
        
        # Create ResearchPaper
        paper = ResearchPaper.create(
            paper_id=paper_id,
            title=record['title'],
            authors=authors,
            abstract=record['abstract'] or '',
            doi=doi,
            publication_date=record['publication_date'],
            url=record['url'] or '',
            source=record['source']
        )
        
        # Set additional properties
        if keywords:
            paper.add_keywords(keywords)
        if record['venue']:
            paper.set_venue(record['venue'])
        if record['citation_count']:
            paper.set_citation_count(record['citation_count'])
        if record['quality_score']:
            paper.set_quality_score(record['quality_score'])
        if metadata:
            paper.update_metadata(metadata)
        
        return paper
    
    # Additional methods following similar patterns...
    # (Implementation details for other methods would follow similar structure)
    
    async def count(self) -> int:
        """Get total number of papers."""
        async with self._pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM research_papers")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive repository statistics."""
        async with self._pool.acquire() as conn:
            # Total papers
            total = await conn.fetchval("SELECT COUNT(*) FROM research_papers")
            
            # Count by source
            source_counts = await conn.fetch('''
                SELECT source, COUNT(*) as count 
                FROM research_papers 
                GROUP BY source 
                ORDER BY count DESC
            ''')
            
            # Date range
            date_range = await conn.fetchrow('''
                SELECT MIN(publication_date) as earliest, 
                       MAX(publication_date) as latest
                FROM research_papers 
                WHERE publication_date IS NOT NULL
            ''')
            
            # Top authors
            top_authors = await conn.fetch('''
                SELECT author_name, COUNT(*) as paper_count
                FROM paper_authors
                GROUP BY author_name
                ORDER BY paper_count DESC
                LIMIT 10
            ''')
            
            return {
                "total_papers": total,
                "source_counts": {r['source']: r['count'] for r in source_counts},
                "date_range": {
                    "earliest": date_range['earliest'],
                    "latest": date_range['latest']
                },
                "top_authors": [
                    {"name": r['author_name'], "papers": r['paper_count']}
                    for r in top_authors
                ],
                "last_updated": datetime.now().isoformat()
            }
```

## 🧪 Repository Testing Patterns

### Comprehensive Repository Tests

```python
# tests/unit/infrastructure/test_in_memory_repository.py

import pytest
import asyncio
from datetime import date, timedelta
from typing import List

from infrastructure.repositories.in_memory_paper_repository import InMemoryPaperRepository
from domain.entities.research_paper import ResearchPaper
from domain.value_objects.paper_id import PaperId
from domain.value_objects.doi import DOI
from domain.value_objects.search_query import SearchQuery, DateRange

class TestInMemoryPaperRepository:
    """Test suite for in-memory paper repository."""
    
    @pytest.fixture
    async def repository(self):
        """Create empty repository for testing."""
        repo = InMemoryPaperRepository()
        yield repo
        await repo.clear()  # Clean up after each test
    
    @pytest.fixture
    def sample_papers(self) -> List[ResearchPaper]:
        """Create sample papers for testing."""
        papers = []
        
        # Paper 1: Machine Learning
        paper1 = ResearchPaper.create(
            paper_id=PaperId.create_arxiv_id("2401.001"),
            title="Deep Learning for Computer Vision",
            authors=["Alice Smith", "Bob Johnson"],
            abstract="This paper explores deep learning techniques for computer vision applications.",
            doi=DOI("10.1000/test.001"),
            publication_date=date(2024, 1, 15),
            source="arxiv"
        )
        paper1.add_keywords(["deep learning", "computer vision", "neural networks"])
        papers.append(paper1)
        
        # Paper 2: Natural Language Processing
        paper2 = ResearchPaper.create(
            paper_id=PaperId.create_arxiv_id("2401.002"),
            title="Transformer Models for Natural Language Processing",
            authors=["Charlie Brown", "Diana Wilson"],
            abstract="An analysis of transformer architectures in NLP tasks.",
            doi=DOI("10.1000/test.002"),
            publication_date=date(2024, 2, 20),
            source="arxiv"
        )
        paper2.add_keywords(["transformers", "NLP", "language models"])
        papers.append(paper2)
        
        # Paper 3: Older paper
        paper3 = ResearchPaper.create(
            paper_id=PaperId.create_doi_id("10.1000/old.paper"),
            title="Classical Machine Learning Approaches",
            authors=["Alice Smith", "Frank Miller"],
            abstract="Traditional machine learning methods and their applications.",
            doi=DOI("10.1000/old.paper"),
            publication_date=date(2020, 5, 10),
            source="pubmed"
        )
        paper3.add_keywords(["machine learning", "classification", "regression"])
        papers.append(paper3)
        
        return papers
    
    @pytest.mark.asyncio
    async def test_save_and_retrieve_paper(self, repository, sample_papers):
        """Test saving and retrieving a single paper."""
        # Arrange
        paper = sample_papers[0]
        
        # Act
        await repository.save(paper)
        retrieved = await repository.get_by_id(paper.paper_id)
        
        # Assert
        assert retrieved is not None
        assert retrieved.title == paper.title
        assert retrieved.authors == paper.authors
        assert retrieved.doi == paper.doi
        assert retrieved.publication_date == paper.publication_date
    
    @pytest.mark.asyncio
    async def test_save_batch_papers(self, repository, sample_papers):
        """Test batch saving of multiple papers."""
        # Act
        await repository.save_batch(sample_papers)
        
        # Assert
        count = await repository.count()
        assert count == len(sample_papers)
        
        # Verify each paper can be retrieved
        for paper in sample_papers:
            retrieved = await repository.get_by_id(paper.paper_id)
            assert retrieved is not None
            assert retrieved.title == paper.title
    
    @pytest.mark.asyncio
    async def test_get_by_doi(self, repository, sample_papers):
        """Test retrieving paper by DOI."""
        # Arrange
        paper = sample_papers[0]
        await repository.save(paper)
        
        # Act
        retrieved = await repository.get_by_doi(paper.doi)
        
        # Assert
        assert retrieved is not None
        assert retrieved.paper_id == paper.paper_id
    
    @pytest.mark.asyncio
    async def test_get_by_title(self, repository, sample_papers):
        """Test retrieving papers by title."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        # Act
        results = await repository.get_by_title("Deep Learning for Computer Vision")
        
        # Assert
        assert len(results) == 1
        assert results[0].title == "Deep Learning for Computer Vision"
    
    @pytest.mark.asyncio
    async def test_search_by_terms(self, repository, sample_papers):
        """Test searching papers by terms."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        query = SearchQuery(
            terms=["deep learning"],
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=100
        )
        
        # Act
        results = await repository.search(query)
        
        # Assert
        assert len(results) == 2  # Two papers mention "deep learning"
        titles = [r.title for r in results]
        assert "Deep Learning for Computer Vision" in titles
        assert "Classical Machine Learning Approaches" in titles
    
    @pytest.mark.asyncio
    async def test_search_by_authors(self, repository, sample_papers):
        """Test searching papers by authors."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        query = SearchQuery(
            terms=[],
            authors=["Alice Smith"],
            date_range=None,
            venue_filter=None,
            max_results=100
        )
        
        # Act
        results = await repository.search(query)
        
        # Assert
        assert len(results) == 2  # Alice Smith authored two papers
        for result in results:
            assert "Alice Smith" in result.authors
    
    @pytest.mark.asyncio
    async def test_search_by_date_range(self, repository, sample_papers):
        """Test searching papers by date range."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        date_range = DateRange(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )
        
        query = SearchQuery(
            terms=[],
            authors=[],
            date_range=date_range,
            venue_filter=None,
            max_results=100
        )
        
        # Act
        results = await repository.search(query)
        
        # Assert
        assert len(results) == 2  # Two papers from 2024
        for result in results:
            assert result.publication_date.year == 2024
    
    @pytest.mark.asyncio
    async def test_get_recent_papers(self, repository, sample_papers):
        """Test getting recent papers."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        # Act
        results = await repository.get_recent_papers(days=365)
        
        # Assert
        assert len(results) == 2  # Two papers from last year
        
        # Results should be sorted by date (newest first)
        assert results[0].publication_date >= results[1].publication_date
    
    @pytest.mark.asyncio
    async def test_get_similar_papers(self, repository, sample_papers):
        """Test finding similar papers."""
        # Arrange
        await repository.save_batch(sample_papers)
        target_paper = sample_papers[0]  # Deep learning paper
        
        # Act
        similar = await repository.get_similar_papers(target_paper)
        
        # Assert
        assert len(similar) > 0
        
        # Should not include the same paper
        similar_ids = [p.paper_id for p in similar]
        assert target_paper.paper_id not in similar_ids
    
    @pytest.mark.asyncio
    async def test_exists_check(self, repository, sample_papers):
        """Test checking if paper exists."""
        # Arrange
        paper = sample_papers[0]
        
        # Act & Assert - Before saving
        assert await repository.exists(paper.paper_id) is False
        
        # Save and check again
        await repository.save(paper)
        assert await repository.exists(paper.paper_id) is True
    
    @pytest.mark.asyncio
    async def test_count_operations(self, repository, sample_papers):
        """Test various count operations."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        # Act & Assert
        total_count = await repository.count()
        assert total_count == len(sample_papers)
        
        arxiv_count = await repository.count_by_source("arxiv")
        assert arxiv_count == 2
        
        pubmed_count = await repository.count_by_source("pubmed")
        assert pubmed_count == 1
    
    @pytest.mark.asyncio
    async def test_delete_paper(self, repository, sample_papers):
        """Test deleting a paper."""
        # Arrange
        paper = sample_papers[0]
        await repository.save(paper)
        
        # Verify it exists
        assert await repository.exists(paper.paper_id) is True
        
        # Act
        deleted = await repository.delete(paper.paper_id)
        
        # Assert
        assert deleted is True
        assert await repository.exists(paper.paper_id) is False
        assert await repository.get_by_id(paper.paper_id) is None
    
    @pytest.mark.asyncio
    async def test_get_statistics(self, repository, sample_papers):
        """Test getting repository statistics."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        # Act
        stats = await repository.get_statistics()
        
        # Assert
        assert stats["total_papers"] == len(sample_papers)
        assert "source_counts" in stats
        assert stats["source_counts"]["arxiv"] == 2
        assert stats["source_counts"]["pubmed"] == 1
        assert "date_range" in stats
        assert "unique_authors" in stats
        assert "unique_keywords" in stats
    
    @pytest.mark.asyncio
    async def test_get_all_sources(self, repository, sample_papers):
        """Test getting all unique sources."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        # Act
        sources = await repository.get_all_sources()
        
        # Assert
        assert "arxiv" in sources
        assert "pubmed" in sources
        assert len(sources) == 2
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, repository, sample_papers):
        """Test thread safety with concurrent operations."""
        # Arrange
        papers_batch_1 = sample_papers[:2]
        papers_batch_2 = sample_papers[2:]
        
        # Act - Concurrent saves
        await asyncio.gather(
            repository.save_batch(papers_batch_1),
            repository.save_batch(papers_batch_2)
        )
        
        # Assert
        total_count = await repository.count()
        assert total_count == len(sample_papers)
    
    @pytest.mark.asyncio
    async def test_update_existing_paper(self, repository, sample_papers):
        """Test updating an existing paper."""
        # Arrange
        paper = sample_papers[0]
        await repository.save(paper)
        
        # Modify the paper
        paper.set_citation_count(100)
        paper.add_keywords(["updated", "modified"])
        
        # Act
        await repository.save(paper)  # Should update, not insert
        
        # Assert
        retrieved = await repository.get_by_id(paper.paper_id)
        assert retrieved.citation_count == 100
        assert "updated" in retrieved.keywords
        assert "modified" in retrieved.keywords
        
        # Should still only have one copy
        total_count = await repository.count()
        assert total_count == 1
    
    @pytest.mark.asyncio
    async def test_search_pagination(self, repository, sample_papers):
        """Test search with pagination."""
        # Arrange
        await repository.save_batch(sample_papers)
        
        query = SearchQuery(
            terms=["learning"],  # Should match all papers
            authors=[],
            date_range=None,
            venue_filter=None,
            max_results=100
        )
        
        # Act - Get first page
        page1 = await repository.search(query, offset=0, limit=2)
        
        # Act - Get second page
        page2 = await repository.search(query, offset=2, limit=2)
        
        # Assert
        assert len(page1) == 2
        assert len(page2) <= 1  # Depends on how many papers match
        
        # No overlap between pages
        page1_ids = {p.paper_id for p in page1}
        page2_ids = {p.paper_id for p in page2}
        assert page1_ids.isdisjoint(page2_ids)
```

## 🔗 Related Documentation

- **[[Research-Paper-Entity]]**: Domain entity that repositories persist
- **[[Paper-Discovery-UseCase]]**: How repositories support business workflows
- **[[Database-Schema-Design]]**: Detailed database schema and optimization
- **[[Caching-Strategy]]**: Redis-based caching for performance
- **[[Testing-Strategies]]**: Comprehensive testing approaches for repositories

## 🚀 Extension Points

### Advanced Repository Features

1. **Elasticsearch Repository**: Full-text search and analytics
2. **Redis Cache Repository**: High-performance caching layer
3. **File System Repository**: Research data and document storage
4. **MongoDB Repository**: Document-based storage for flexibility
5. **Composite Repository**: Combines multiple storage backends

### Performance Optimizations

1. **Connection Pooling**: Optimize database connections
2. **Query Optimization**: Advanced SQL query patterns
3. **Bulk Operations**: Efficient batch processing
4. **Read Replicas**: Separate read/write database instances
5. **Sharding**: Horizontal scaling strategies

---

*The Repository Implementation Patterns demonstrate how to build robust, scalable data access layers that support both development efficiency and production performance requirements.*
