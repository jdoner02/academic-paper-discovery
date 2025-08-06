"""
Contract Tests - API interface compliance validation.

These tests validate that implementations comply with their defined contracts
and interfaces. They ensure architectural boundaries are respected and that
components can be safely substituted or extended.

Educational Notes:
- Contract tests validate interface compliance rather than implementation details
- They ensure Liskov Substitution Principle is maintained
- Focus on behavioral contracts, not just method signatures
- Critical for maintaining architectural integrity in Clean Architecture

Contract Areas Tested:
- Repository interface compliance
- Use case interface contracts
- Domain service contracts
- Value object behavioral contracts
"""

import pytest
from abc import ABC
from datetime import datetime, timezone
from typing import List, Optional

from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.infrastructure.repositories.arxiv_paper_repository import ArxivPaperRepository
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery


class TestRepositoryPortContract:
    """
    Test that all repository implementations comply with the port contract.

    Educational Note:
    The Repository Port defines the contract that all repository implementations
    must fulfill. These tests ensure any repository implementation can be
    substituted without breaking the application layer.

    This demonstrates the Dependency Inversion Principle - the application
    depends on abstractions (ports) not concretions (implementations).
    """

    @pytest.fixture(
        params=[
            InMemoryPaperRepository,
            # ArxivPaperRepository - Commented out due to external API dependency
        ]
    )
    def repository_implementation(self, request):
        """
        Provide different repository implementations for contract testing.

        Educational Note:
        This fixture tests multiple implementations against the same contract,
        ensuring they're truly interchangeable as required by Clean Architecture.
        """
        return request.param()

    @pytest.fixture
    def sample_papers(self):
        """Sample papers for contract testing."""
        return [
            ResearchPaper(
                title="Contract Test Paper 1",
                authors=["Dr. Contract Tester"],
                abstract="First paper for testing repository contracts",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                doi="10.1000/contract.2023.001",
                arxiv_id="2301.00001",
                venue="Contract Testing Journal",
                citation_count=42,
                keywords=["contract", "testing", "repository"],
            ),
            ResearchPaper(
                title="Contract Test Paper 2",
                authors=["Prof. Interface Validator"],
                abstract="Second paper for testing repository contracts",
                publication_date=datetime(2023, 2, 1, tzinfo=timezone.utc),
                doi="10.1000/contract.2023.002",
                arxiv_id="2302.00001",
                venue="Contract Testing Journal",
                citation_count=35,
                keywords=["interface", "validation", "testing"],
            ),
        ]

    def test_repository_implements_port_interface(self, repository_implementation):
        """
        Test that repository implementations properly implement the port interface.

        Educational Note:
        This test validates that implementations actually implement the required
        interface. In Python, this means checking isinstance with the ABC.
        """
        assert isinstance(repository_implementation, PaperRepositoryPort)

        # Verify all required methods are present
        assert hasattr(repository_implementation, "save_paper")
        assert hasattr(repository_implementation, "save_papers")
        assert hasattr(repository_implementation, "find_by_query")
        assert hasattr(repository_implementation, "find_by_doi")
        assert hasattr(repository_implementation, "find_by_arxiv_id")
        assert hasattr(repository_implementation, "count_all")

    def test_save_paper_contract(self, repository_implementation, sample_papers):
        """
        Test save_paper method contract compliance.

        Educational Note:
        The contract specifies that save_paper should accept a ResearchPaper
        and return None. It should store the paper such that it can be
        retrieved later.
        """
        paper = sample_papers[0]

        # Contract: Method should accept ResearchPaper and return None
        result = repository_implementation.save_paper(paper)
        assert result is None

        # Contract: Saved paper should be retrievable
        found_paper = repository_implementation.find_by_doi(paper.doi)
        assert found_paper is not None
        assert found_paper.title == paper.title

    def test_save_papers_contract(self, repository_implementation, sample_papers):
        """
        Test save_papers method contract compliance.

        Educational Note:
        The contract specifies that save_papers should accept a list of
        ResearchPaper objects and return None. All papers should be stored.
        """
        # Contract: Method should accept List[ResearchPaper] and return None
        result = repository_implementation.save_papers(sample_papers)
        assert result is None

        # Contract: All saved papers should be retrievable
        for paper in sample_papers:
            found_paper = repository_implementation.find_by_doi(paper.doi)
            assert found_paper is not None
            assert found_paper.title == paper.title

    def test_find_by_query_contract(self, repository_implementation, sample_papers):
        """
        Test find_by_query method contract compliance.

        Educational Note:
        The contract specifies that this method should accept a SearchQuery
        and return a list of matching ResearchPaper objects, possibly empty.
        """
        # Setup: Save papers first
        repository_implementation.save_papers(sample_papers)

        # Create a search query for contract testing
        query = SearchQuery(terms=["contract"])

        # Contract: Method should accept SearchQuery and return List[ResearchPaper]
        results = repository_implementation.find_by_query(query)
        assert isinstance(results, list)
        assert all(isinstance(paper, ResearchPaper) for paper in results)

        # Contract: Should find relevant papers
        assert len(results) >= 1  # At least one paper should match

        # Contract: Should return empty list for non-matching query
        empty_query = SearchQuery(terms=["nonexistent_term_xyz"])
        empty_results = repository_implementation.find_by_query(empty_query)
        assert isinstance(empty_results, list)
        assert len(empty_results) == 0

    def test_find_by_doi_contract(self, repository_implementation, sample_papers):
        """
        Test find_by_doi method contract compliance.

        Educational Note:
        The contract specifies that this method should find papers by their
        unique DOI identifier and return Optional[ResearchPaper].
        """
        paper = sample_papers[0]
        repository_implementation.save_paper(paper)

        # Contract: Method should accept DOI string and return Optional[ResearchPaper]
        result = repository_implementation.find_by_doi(paper.doi)
        assert result is not None
        assert isinstance(result, ResearchPaper)

        # Contract: Should find exact DOI match
        assert result.doi == paper.doi

        # Contract: Should return None for non-existent DOI
        empty_result = repository_implementation.find_by_doi("10.9999/nonexistent.doi")
        assert empty_result is None

    def test_find_by_arxiv_id_contract(self, repository_implementation, sample_papers):
        """
        Test find_by_arxiv_id method contract compliance.

        Educational Note:
        The contract specifies that this method should find papers by their
        ArXiv identifier and return Optional[ResearchPaper].
        """
        paper = sample_papers[0]
        repository_implementation.save_paper(paper)

        # Contract: Method should accept arxiv_id string and return Optional[ResearchPaper]
        result = repository_implementation.find_by_arxiv_id(paper.arxiv_id)
        assert result is not None
        assert isinstance(result, ResearchPaper)

        # Contract: Should find papers by the specified ArXiv ID
        assert result.arxiv_id == paper.arxiv_id

        # Contract: Should return None for non-existent ArXiv ID
        empty_result = repository_implementation.find_by_arxiv_id("9999.99999")
        assert empty_result is None

    def test_repository_isolation_contract(
        self, repository_implementation, sample_papers
    ):
        """
        Test that repository instances are properly isolated.

        Educational Note:
        Each repository instance should manage its own data. This contract
        ensures that different instances don't interfere with each other.
        """
        # Create second repository instance
        second_repo = type(repository_implementation)()

        # Save papers to first repository
        repository_implementation.save_papers(sample_papers)

        # Contract: Second repository should be empty initially
        query = SearchQuery(terms=["contract"])
        results_repo1 = repository_implementation.find_by_query(query)
        results_repo2 = second_repo.find_by_query(query)

        assert len(results_repo1) >= 1  # First repo has papers
        assert len(results_repo2) == 0  # Second repo is empty

    def test_repository_consistency_contract(
        self, repository_implementation, sample_papers
    ):
        """
        Test that repository operations are consistent.

        Educational Note:
        The contract guarantees that once a paper is saved, it remains
        accessible through all relevant query methods until explicitly removed.
        """
        paper = sample_papers[0]
        repository_implementation.save_paper(paper)

        # Contract: Paper should be findable through multiple query methods
        doi_result = repository_implementation.find_by_doi(paper.doi)
        arxiv_result = repository_implementation.find_by_arxiv_id(paper.arxiv_id)
        search_query = SearchQuery(terms=paper.keywords[:1])
        search_results = repository_implementation.find_by_query(search_query)

        # All queries should find the same paper
        assert doi_result is not None
        assert arxiv_result is not None
        assert len(search_results) >= 1

        # The paper found should be consistent across all queries
        assert doi_result.doi == paper.doi
        assert arxiv_result.doi == paper.doi
        assert any(p.doi == paper.doi for p in search_results)


class TestValueObjectContracts:
    """
    Test that value objects comply with value object behavioral contracts.

    Educational Note:
    Value objects must be immutable, have value-based equality, and be
    hashable. These contracts are essential for domain model integrity.
    """

    def test_search_query_immutability_contract(self):
        """
        Test that SearchQuery maintains immutability contract.

        Educational Note:
        Value objects must be immutable after creation. This contract
        prevents accidental state changes that could cause bugs.
        """
        query = SearchQuery(
            terms=["machine learning"], max_results=50, min_citations=10
        )

        # Contract: Properties should return immutable collections
        assert isinstance(query.terms, tuple)

        # Contract: Direct mutation of properties should not be possible
        original_terms = query.terms
        # query.terms cannot be reassigned (property without setter)

        # Contract: Returned collections should be immutable
        with pytest.raises(AttributeError):
            query.terms.append("new term")  # tuple.append doesn't exist

    def test_search_query_equality_contract(self):
        """
        Test that SearchQuery implements value-based equality contract.

        Educational Note:
        Value objects must implement equality based on their values,
        not object identity. This is crucial for collections and caching.
        """
        query1 = SearchQuery(terms=["AI"], max_results=50, min_citations=10)

        query2 = SearchQuery(terms=["AI"], max_results=50, min_citations=10)

        query3 = SearchQuery(
            terms=["AI"], max_results=25, min_citations=10  # Different max_results
        )

        # Contract: Equal values should be equal
        assert query1 == query2
        assert query1 is not query2  # Different objects

        # Contract: Different values should not be equal
        assert query1 != query3

        # Contract: Should not be equal to different types
        assert query1 != "not a search query"
        assert query1 != 42

    def test_search_query_hashability_contract(self):
        """
        Test that SearchQuery implements hashability contract.

        Educational Note:
        Value objects should be hashable so they can be used in sets and
        as dictionary keys. This requires implementing __hash__.
        """
        query1 = SearchQuery(terms=["AI"], max_results=50, min_citations=10)

        query2 = SearchQuery(terms=["AI"], max_results=50, min_citations=10)

        # Contract: Equal objects should have equal hashes
        assert hash(query1) == hash(query2)

        # Contract: Should be usable in sets
        query_set = {query1, query2}
        assert len(query_set) == 1  # Should deduplicate equal queries

        # Contract: Should be usable as dictionary keys
        query_dict = {query1: "value1", query2: "value2"}
        assert len(query_dict) == 1  # Should overwrite with same key

    def test_value_object_validation_contract(self):
        """
        Test that value objects validate their data contracts.

        Educational Note:
        Value objects should validate their invariants on creation and
        reject invalid data with clear error messages.
        """
        # Contract: Should reject empty terms
        with pytest.raises(ValueError, match="must have at least one search term"):
            SearchQuery(terms=[], max_results=50)

        # Contract: Should reject invalid max_results
        with pytest.raises(ValueError, match="max_results must be positive"):
            SearchQuery(terms=["AI"], max_results=0)

        # Contract: Should reject negative min_citations
        with pytest.raises(ValueError, match="min_citations cannot be negative"):
            SearchQuery(terms=["AI"], max_results=50, min_citations=-1)


class TestUseCaseContracts:
    """
    Test that use cases comply with application service contracts.

    Educational Note:
    Use cases represent application business rules and should have
    well-defined contracts for inputs, outputs, and error handling.
    """

    def test_use_case_error_handling_contract(self):
        """
        Test that use cases handle errors according to their contracts.

        Educational Note:
        Use cases should translate infrastructure errors into domain
        errors and provide meaningful error messages to callers.
        """
        # This would test that use cases:
        # - Handle repository failures gracefully
        # - Provide meaningful error messages
        # - Don't leak infrastructure details
        # - Maintain transactional integrity
        pass

    def test_use_case_input_validation_contract(self):
        """
        Test that use cases validate inputs according to their contracts.

        Educational Note:
        Use cases should validate all inputs and reject invalid requests
        with clear validation error messages.
        """
        # This would test that use cases:
        # - Validate all input parameters
        # - Reject invalid inputs with clear messages
        # - Don't process invalid requests
        # - Maintain domain invariants
        pass
