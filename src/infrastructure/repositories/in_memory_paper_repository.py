"""
InMemoryPaperRepository - In-memory implementation of PaperRepositoryPort.

This repository provides an in-memory storage implementation of the paper repository
interface. It's primarily used for testing, development, and demonstration purposes.

Educational Notes:
- Demonstrates Repository Pattern with concrete implementation
- Shows how to implement search and filtering logic
- Provides fast, lightweight storage for testing
- Illustrates separation between interface and implementation

Design Decisions:
- Uses dictionaries for O(1) lookup by DOI and ArXiv ID
- Implements comprehensive search filtering logic
- Provides detailed error handling and validation
- Maintains all papers in memory for simplicity

Use Cases:
- Unit testing of application layer
- Development and prototyping
- Integration testing
- Demonstration of full system functionality
"""

from typing import List, Optional, Dict
from datetime import datetime

from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery


class InMemoryPaperRepository(PaperRepositoryPort):
    """
    In-memory implementation of the paper repository interface.

    This repository stores research papers in memory using dictionaries
    for fast lookup by identifier. It implements all required repository
    operations including search, retrieval, and persistence.

    Educational Notes:
    - Concrete implementation of the repository port
    - Demonstrates the Repository Pattern in practice
    - Shows how different storage mechanisms can use the same interface
    - Provides baseline for comparing with other implementations

    Storage Strategy:
    - Primary storage: Dictionary keyed by DOI
    - Secondary index: Dictionary keyed by ArXiv ID
    - All papers stored in memory for fast access
    - No persistence between application restarts
    """

    def __init__(self) -> None:
        """
        Initialize the in-memory repository.

        Creates empty storage dictionaries for papers.

        Educational Note:
        Constructor initializes the storage structures but doesn't
        load any data. This keeps the repository lightweight and
        allows for clean test setups.
        """
        # Primary storage indexed by DOI
        self._papers_by_doi: Dict[str, ResearchPaper] = {}

        # Secondary index for ArXiv papers
        self._papers_by_arxiv: Dict[str, ResearchPaper] = {}

        # Keep track of all papers for search operations
        # Educational Note: This redundancy optimizes different access patterns
        self._all_papers: List[ResearchPaper] = []

    def find_by_query(self, query: SearchQuery) -> List[ResearchPaper]:
        """
        Find papers matching the given search query.

        This method implements comprehensive search functionality by filtering
        papers based on the criteria specified in the SearchQuery.

        Args:
            query: SearchQuery containing search criteria

        Returns:
            List[ResearchPaper]: Papers matching the search criteria,
                               limited by max_results and sorted by relevance

        Educational Note:
        This method demonstrates how to implement complex filtering logic
        in the repository layer. It applies multiple filters in sequence
        and implements basic relevance scoring.
        """
        if not query:
            return []

        # Start with all papers
        matching_papers = self._all_papers.copy()

        # Apply text-based filtering
        if query.terms:
            matching_papers = self._filter_by_search_terms(matching_papers, query.terms)

        # Apply date range filtering
        if query.start_date or query.end_date:
            matching_papers = self._filter_by_date_range(
                matching_papers, query.start_date, query.end_date
            )

        # Apply citation threshold filtering
        if query.min_citations > 0:
            matching_papers = self._filter_by_citation_count(
                matching_papers, query.min_citations
            )

        # Sort by relevance (simple implementation)
        sorted_papers = self._sort_by_relevance(matching_papers, query.terms)

        # Apply result limit
        limited_papers = sorted_papers[: query.max_results]

        return limited_papers

    def find_by_doi(self, doi: str) -> Optional[ResearchPaper]:
        """
        Find a paper by its DOI.

        Args:
            doi: Digital Object Identifier

        Returns:
            ResearchPaper if found, None otherwise

        Educational Note:
        This method demonstrates O(1) lookup using dictionary indexing.
        The DOI serves as the primary key for paper identification.
        """
        if not doi:
            return None

        return self._papers_by_doi.get(doi)

    def find_by_arxiv_id(self, arxiv_id: str) -> Optional[ResearchPaper]:
        """
        Find a paper by its ArXiv ID.

        Args:
            arxiv_id: ArXiv identifier

        Returns:
            ResearchPaper if found, None otherwise

        Educational Note:
        This method shows how to implement secondary indexing.
        ArXiv ID serves as an alternative identifier for preprint papers.
        """
        if not arxiv_id:
            return None

        return self._papers_by_arxiv.get(arxiv_id)

    def save_paper(self, paper: ResearchPaper) -> None:
        """
        Save a single research paper to the repository.

        Args:
            paper: ResearchPaper to save

        Raises:
            ValueError: If paper is None or invalid

        Educational Note:
        This method demonstrates how to maintain multiple indexes
        and ensure data consistency across different access patterns.
        """
        if paper is None:
            raise ValueError("Paper cannot be None")

        # Store in primary index (DOI)
        if paper.doi:
            # Remove old version if it exists
            old_paper = self._papers_by_doi.get(paper.doi)
            if old_paper:
                self._remove_from_all_indexes(old_paper)

            self._papers_by_doi[paper.doi] = paper

        # Store in secondary index (ArXiv ID)
        if paper.arxiv_id:
            # Remove old version if it exists
            old_paper = self._papers_by_arxiv.get(paper.arxiv_id)
            if old_paper:
                self._remove_from_all_indexes(old_paper)

            self._papers_by_arxiv[paper.arxiv_id] = paper

        # Add to main list if not already present
        if paper not in self._all_papers:
            self._all_papers.append(paper)
        else:
            # Update existing paper in the list
            for i, existing_paper in enumerate(self._all_papers):
                if existing_paper == paper or (
                    paper.doi and existing_paper.doi == paper.doi
                ):
                    self._all_papers[i] = paper
                    break

    def save_papers(self, papers: List[ResearchPaper]) -> None:
        """
        Save multiple research papers to the repository.

        Args:
            papers: List of ResearchPaper objects to save

        Raises:
            ValueError: If any paper in the list is None

        Educational Note:
        This method demonstrates batch operations and input validation.
        It provides better performance than multiple individual saves.
        """
        if not papers:  # Handle empty list gracefully
            return

        # Validate all papers first
        for i, paper in enumerate(papers):
            if paper is None:
                raise ValueError(
                    f"All papers must be non-None. Found None at index {i}"
                )

        # Save all papers
        for paper in papers:
            self.save_paper(paper)

    def count_all(self) -> int:
        """
        Count total number of research papers in the repository.

        Returns:
            int: Total number of papers stored in memory

        Educational Note:
        Simple count operation using len() on the primary storage dictionary.
        This demonstrates how the in-memory implementation can provide
        extremely fast count operations.
        """
        return len(self._papers_by_doi)

    def _filter_by_search_terms(
        self, papers: List[ResearchPaper], terms: List[str]
    ) -> List[ResearchPaper]:
        """
        Filter papers by search terms in title, abstract, and keywords.

        Args:
            papers: Papers to filter
            terms: Search terms to match

        Returns:
            List[ResearchPaper]: Papers matching any of the search terms

        Educational Note:
        This method implements basic text search functionality.
        It searches across multiple fields and uses case-insensitive matching.
        """
        if not terms:
            return papers

        matching_papers = []

        for paper in papers:
            # Check if any search term appears in the paper
            paper_text = self._get_searchable_text(paper).lower()

            for term in terms:
                if term.lower() in paper_text:
                    matching_papers.append(paper)
                    break  # Found match, no need to check other terms for this paper

        return matching_papers

    def _filter_by_date_range(
        self,
        papers: List[ResearchPaper],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> List[ResearchPaper]:
        """
        Filter papers by publication date range.

        Args:
            papers: Papers to filter
            start_date: Earliest publication date (inclusive)
            end_date: Latest publication date (inclusive)

        Returns:
            List[ResearchPaper]: Papers within the date range

        Educational Note:
        This method shows how to implement date range filtering.
        It handles None values gracefully to support partial ranges.
        """
        if not start_date and not end_date:
            return papers

        matching_papers = []

        for paper in papers:
            if not paper.publication_date:
                continue  # Skip papers without publication date

            # Check start date constraint
            if start_date and paper.publication_date < start_date:
                continue

            # Check end date constraint
            if end_date and paper.publication_date > end_date:
                continue

            matching_papers.append(paper)

        return matching_papers

    def _filter_by_citation_count(
        self, papers: List[ResearchPaper], min_citations: int
    ) -> List[ResearchPaper]:
        """
        Filter papers by minimum citation count.

        Args:
            papers: Papers to filter
            min_citations: Minimum number of citations required

        Returns:
            List[ResearchPaper]: Papers with citation count >= min_citations

        Educational Note:
        This method demonstrates simple numeric filtering.
        It's used to find highly-cited or influential papers.
        """
        return [paper for paper in papers if paper.citation_count >= min_citations]

    def _sort_by_relevance(
        self, papers: List[ResearchPaper], search_terms: List[str]
    ) -> List[ResearchPaper]:
        """
        Sort papers by relevance to search terms.

        Args:
            papers: Papers to sort
            search_terms: Terms to calculate relevance against

        Returns:
            List[ResearchPaper]: Papers sorted by relevance (descending)

        Educational Note:
        This implements a simple relevance scoring algorithm.
        Production systems would use more sophisticated ranking
        like TF-IDF or machine learning models.
        """
        if not search_terms:
            # Sort by citation count if no search terms
            return sorted(papers, key=lambda p: p.citation_count, reverse=True)

        def calculate_relevance_score(paper: ResearchPaper) -> float:
            """Calculate simple relevance score for a paper."""
            score = 0.0
            paper_text = self._get_searchable_text(paper).lower()

            for term in search_terms:
                term_lower = term.lower()

                # Title matches are weighted heavily
                if term_lower in paper.title.lower():
                    score += 10.0

                # Abstract matches have medium weight
                if term_lower in paper.abstract.lower():
                    score += 5.0

                # Keyword matches have high weight
                for keyword in paper.keywords:
                    if term_lower in keyword.lower():
                        score += 8.0

                # Venue matches have low weight
                if paper.venue and term_lower in paper.venue.lower():
                    score += 2.0

            # Boost score based on citation count
            score += paper.citation_count * 0.1

            return score

        return sorted(papers, key=calculate_relevance_score, reverse=True)

    def _get_searchable_text(self, paper: ResearchPaper) -> str:
        """
        Get all searchable text from a paper.

        Args:
            paper: ResearchPaper to extract text from

        Returns:
            str: Combined searchable text

        Educational Note:
        This method centralizes text extraction logic for search operations.
        It combines multiple fields into a single searchable string.
        """
        searchable_parts = [
            paper.title,
            paper.abstract,
            " ".join(paper.authors),
            " ".join(paper.keywords),
            paper.venue or "",
        ]

        return " ".join(searchable_parts)

    def _remove_from_all_indexes(self, paper: ResearchPaper) -> None:
        """
        Remove a paper from all storage indexes.

        Args:
            paper: ResearchPaper to remove

        Educational Note:
        This helper method ensures data consistency when updating papers.
        It removes the old version from all indexes before adding the new version.
        """
        # Remove from DOI index
        if paper.doi and paper.doi in self._papers_by_doi:
            del self._papers_by_doi[paper.doi]

        # Remove from ArXiv index
        if paper.arxiv_id and paper.arxiv_id in self._papers_by_arxiv:
            del self._papers_by_arxiv[paper.arxiv_id]

        # Remove from main list
        if paper in self._all_papers:
            self._all_papers.remove(paper)

    def __len__(self) -> int:
        """
        Return the number of papers in the repository.

        Educational Note:
        This method enables len() function usage and provides
        convenient way to check repository size.
        """
        return len(self._all_papers)

    def __contains__(self, paper: ResearchPaper) -> bool:
        """
        Check if a paper exists in the repository.

        Args:
            paper: ResearchPaper to check

        Returns:
            bool: True if paper exists, False otherwise

        Educational Note:
        This method enables 'in' operator usage and provides
        convenient way to check paper existence.
        """
        return paper in self._all_papers


# Educational Notes for Students:
#
# 1. Repository Implementation Strategy:
#    - Use multiple indexes for different access patterns (DOI, ArXiv ID)
#    - Maintain consistency across all storage structures
#    - Optimize for common operations (search, lookup by ID)
#    - Provide comprehensive error handling and validation
#
# 2. Search Implementation Patterns:
#    - Multi-step filtering: text → date → citations → sorting
#    - Case-insensitive text matching for better user experience
#    - Relevance scoring combines multiple factors (title, abstract, citations)
#    - Graceful handling of missing or None values
#
# 3. Data Structure Choices:
#    - Dictionaries for O(1) lookup by identifier
#    - Lists for maintaining order and enabling search
#    - Multiple indexes for different access patterns
#    - Memory efficiency vs. query performance trade-offs
#
# 4. Interface Implementation:
#    - All abstract methods from port interface must be implemented
#    - Method signatures must match exactly
#    - Return types and error handling should be consistent
#    - Add helper methods for complex operations
#
# 5. Testing Considerations:
#    - Repository should work with real data, not mocks
#    - Test all interface methods thoroughly
#    - Verify data persistence across operations
#    - Test edge cases and error conditions
