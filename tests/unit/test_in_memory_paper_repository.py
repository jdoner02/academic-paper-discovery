"""
Test suite for InMemoryPaperRepository.

This test suite validates the behavior of the InMemoryPaperRepository,
which provides an in-memory implementation of the PaperRepositoryPort interface.

Educational Notes:
- Tests verify proper implementation of the repository port interface
- Tests ensure data persistence across multiple method calls
- Tests validate search and filtering functionality
- Tests cover edge cases and error conditions

Test Organization:
1. Interface compliance tests - Verify proper port implementation
2. Data persistence tests - Verify data storage and retrieval
3. Search functionality tests - Verify query-based search operations
4. Edge case tests - Error conditions and boundary cases

Testing Strategy:
- Test real data persistence (not mocked)
- Use sample HRV research papers for realistic testing
- Verify all interface methods work correctly
- Test integration between different repository methods
"""

import unittest
from datetime import datetime, timezone
from typing import List

from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery


class TestInMemoryPaperRepositoryInterface(unittest.TestCase):
    """
    Test interface compliance for InMemoryPaperRepository.

    This test class validates that InMemoryPaperRepository properly
    implements the PaperRepositoryPort interface.

    Educational Note:
    These tests ensure the repository follows the contract defined
    by the port interface, enabling substitutability with other implementations.
    """

    def test_implements_paper_repository_port(self):
        """
        Test that InMemoryPaperRepository implements PaperRepositoryPort.

        This verifies proper interface inheritance and implementation.
        """
        repository = InMemoryPaperRepository()

        # Should be an instance of the port interface
        self.assertIsInstance(repository, PaperRepositoryPort)

    def test_has_all_required_methods(self):
        """
        Test that InMemoryPaperRepository has all required interface methods.

        This ensures all abstract methods from the port are implemented.
        """
        repository = InMemoryPaperRepository()

        # Check all required methods exist and are callable
        required_methods = [
            "find_by_query",
            "find_by_doi",
            "find_by_arxiv_id",
            "save_paper",
            "save_papers",
        ]

        for method_name in required_methods:
            with self.subTest(method=method_name):
                self.assertTrue(hasattr(repository, method_name))
                method = getattr(repository, method_name)
                self.assertTrue(callable(method))


class TestInMemoryPaperRepositoryBasicOperations(unittest.TestCase):
    """
    Test basic CRUD operations for InMemoryPaperRepository.

    This test class validates fundamental storage and retrieval operations.

    Educational Note:
    These tests focus on the core repository responsibilities:
    saving, retrieving, and managing paper entities.
    """

    def setUp(self):
        """Set up test fixtures for basic operations tests."""
        self.repository = InMemoryPaperRepository()

        # Create sample research papers for testing
        self.sample_paper_1 = ResearchPaper(
            title="Heart Rate Variability in Traumatic Brain Injury: A Systematic Review",
            authors=["Dr. Sarah Chen", "Dr. Michael Rodriguez"],
            abstract="A comprehensive systematic review examining HRV changes in TBI patients...",
            publication_date=datetime(2023, 8, 15, tzinfo=timezone.utc),
            venue="Journal of Neurotrauma",
            doi="10.1089/neu.2023.0123",
            citation_count=45,
            keywords=["HRV", "TBI", "autonomic dysfunction", "systematic review"],
        )

        self.sample_paper_2 = ResearchPaper(
            title="Autonomic Dysfunction Following Mild Traumatic Brain Injury",
            authors=["Dr. Jennifer Park", "Dr. David Kumar", "Dr. Lisa Thompson"],
            abstract="Investigation of autonomic nervous system dysfunction in mild TBI...",
            publication_date=datetime(2023, 6, 20, tzinfo=timezone.utc),
            venue="Clinical Neurophysiology",
            doi="10.1016/j.clinph.2023.0456",
            arxiv_id="2306.12345",
            citation_count=28,
            keywords=["mild TBI", "autonomic dysfunction", "HRV analysis"],
        )

        self.sample_paper_3 = ResearchPaper(
            title="Machine Learning Approaches to HRV Analysis in Clinical Settings",
            authors=["Dr. Alex Wang", "Dr. Maria Santos"],
            abstract="Application of machine learning techniques for HRV analysis...",
            publication_date=datetime(2023, 4, 10, tzinfo=timezone.utc),
            venue="IEEE Transactions on Biomedical Engineering",
            doi="10.1109/TBME.2023.0789",
            citation_count=67,
            keywords=[
                "machine learning",
                "HRV",
                "clinical analysis",
                "biomedical engineering",
            ],
        )

    def test_save_single_paper_success(self):
        """
        Test successful saving of a single research paper.

        This verifies the basic save operation works correctly.
        """
        # Save the paper
        self.repository.save_paper(self.sample_paper_1)

        # Verify it can be retrieved by DOI
        retrieved_paper = self.repository.find_by_doi(self.sample_paper_1.doi)

        self.assertEqual(retrieved_paper, self.sample_paper_1)

    def test_save_multiple_papers_success(self):
        """
        Test successful saving of multiple research papers.

        This verifies the batch save operation works correctly.
        """
        papers = [self.sample_paper_1, self.sample_paper_2, self.sample_paper_3]

        # Save all papers
        self.repository.save_papers(papers)

        # Verify all can be retrieved
        for paper in papers:
            with self.subTest(doi=paper.doi):
                retrieved_paper = self.repository.find_by_doi(paper.doi)
                self.assertEqual(retrieved_paper, paper)

    def test_find_by_doi_returns_correct_paper(self):
        """
        Test that find_by_doi returns the correct paper.

        This verifies DOI-based lookup works accurately.
        """
        # Save multiple papers
        self.repository.save_papers([self.sample_paper_1, self.sample_paper_2])

        # Retrieve specific paper by DOI
        retrieved_paper = self.repository.find_by_doi(self.sample_paper_2.doi)

        self.assertEqual(retrieved_paper, self.sample_paper_2)
        self.assertNotEqual(retrieved_paper, self.sample_paper_1)

    def test_find_by_doi_returns_none_for_nonexistent_paper(self):
        """
        Test that find_by_doi returns None for non-existent papers.

        This verifies proper handling of missing papers.
        """
        # Don't save any papers

        # Try to retrieve non-existent paper
        retrieved_paper = self.repository.find_by_doi("10.1000/nonexistent")

        self.assertIsNone(retrieved_paper)

    def test_find_by_arxiv_id_returns_correct_paper(self):
        """
        Test that find_by_arxiv_id returns the correct paper.

        This verifies ArXiv ID-based lookup works accurately.
        """
        # Save paper with ArXiv ID
        self.repository.save_paper(self.sample_paper_2)

        # Retrieve by ArXiv ID
        retrieved_paper = self.repository.find_by_arxiv_id(self.sample_paper_2.arxiv_id)

        self.assertEqual(retrieved_paper, self.sample_paper_2)

    def test_find_by_arxiv_id_returns_none_for_nonexistent_paper(self):
        """
        Test that find_by_arxiv_id returns None for non-existent papers.

        This verifies proper handling of missing ArXiv papers.
        """
        # Try to retrieve non-existent ArXiv paper
        retrieved_paper = self.repository.find_by_arxiv_id("2099.99999")

        self.assertIsNone(retrieved_paper)


class TestInMemoryPaperRepositorySearchFunctionality(unittest.TestCase):
    """
    Test search functionality for InMemoryPaperRepository.

    This test class validates query-based search operations and filtering.

    Educational Note:
    These tests verify that the repository can filter papers based on
    various search criteria defined in SearchQuery value objects.
    """

    def setUp(self):
        """Set up test fixtures with populated repository."""
        self.repository = InMemoryPaperRepository()

        # Create diverse set of papers for search testing
        self.hrv_paper = ResearchPaper(
            title="Heart Rate Variability in Chronic Fatigue Syndrome",
            authors=["Dr. Emma Wilson"],
            abstract="Analysis of HRV patterns in chronic fatigue syndrome patients...",
            publication_date=datetime(2023, 9, 1, tzinfo=timezone.utc),
            venue="Autonomic Neuroscience",
            doi="10.1016/j.autneu.2023.0001",
            citation_count=15,
            keywords=["HRV", "chronic fatigue", "autonomic dysfunction"],
        )

        self.tbi_paper = ResearchPaper(
            title="Traumatic Brain Injury and Cardiac Autonomic Function",
            authors=["Dr. Robert Johnson", "Dr. Kate Miller"],
            abstract="Investigation of cardiac autonomic function following TBI...",
            publication_date=datetime(2023, 7, 15, tzinfo=timezone.utc),
            venue="Journal of Neurotrauma",
            doi="10.1089/neu.2023.0002",
            citation_count=32,
            keywords=["TBI", "cardiac function", "autonomic dysfunction"],
        )

        self.ml_paper = ResearchPaper(
            title="Deep Learning for Physiological Signal Analysis",
            authors=["Dr. Alan Zhang", "Dr. Sophie Brown"],
            abstract="Application of deep learning to physiological signal processing...",
            publication_date=datetime(2023, 5, 10, tzinfo=timezone.utc),
            venue="Nature Machine Intelligence",
            doi="10.1038/s42256-023-0003",
            citation_count=89,
            keywords=["deep learning", "physiological signals", "signal processing"],
        )

        self.old_paper = ResearchPaper(
            title="Historical Perspectives on Heart Rate Analysis",
            authors=["Dr. Charles Davis"],
            abstract="Historical review of heart rate analysis techniques...",
            publication_date=datetime(2020, 3, 1, tzinfo=timezone.utc),
            venue="History of Medicine",
            doi="10.1177/hist.2020.0001",
            citation_count=12,
            keywords=["historical", "heart rate", "analysis techniques"],
        )

        # Populate repository
        self.repository.save_papers(
            [self.hrv_paper, self.tbi_paper, self.ml_paper, self.old_paper]
        )

    def test_find_by_query_returns_matching_papers(self):
        """
        Test that find_by_query returns papers matching search terms.

        This verifies basic text-based search functionality.
        """
        # Search for HRV-related papers
        query = SearchQuery(terms=["HRV"])

        results = self.repository.find_by_query(query)

        # Should return the HRV paper
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.hrv_paper)

    def test_find_by_query_returns_multiple_matches(self):
        """
        Test that find_by_query returns multiple matching papers.

        This verifies search can return multiple results.
        """
        # Search for papers mentioning "autonomic"
        query = SearchQuery(terms=["autonomic"])

        results = self.repository.find_by_query(query)

        # Should return both HRV and TBI papers (both mention autonomic)
        self.assertEqual(len(results), 2)
        result_dois = [paper.doi for paper in results]
        self.assertIn(self.hrv_paper.doi, result_dois)
        self.assertIn(self.tbi_paper.doi, result_dois)

    def test_find_by_query_filters_by_date_range(self):
        """
        Test that find_by_query properly filters by date range.

        This verifies date-based filtering functionality.
        """
        # Search for papers from 2023 only
        query = SearchQuery(
            terms=["analysis"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 12, 31, tzinfo=timezone.utc),
        )

        results = self.repository.find_by_query(query)

        # Should exclude the 2020 paper
        result_years = [paper.publication_date.year for paper in results]
        self.assertTrue(all(year == 2023 for year in result_years))
        self.assertNotIn(self.old_paper, results)

    def test_find_by_query_filters_by_citation_count(self):
        """
        Test that find_by_query filters by minimum citation count.

        This verifies citation-based filtering functionality.
        """
        # Search for highly cited papers (>30 citations)
        query = SearchQuery(
            terms=["learning", "function", "analysis"], min_citations=30  # Broad terms
        )

        results = self.repository.find_by_query(query)

        # Should return papers with citation_count >= 30
        for paper in results:
            with self.subTest(paper=paper.title):
                self.assertGreaterEqual(paper.citation_count, 30)

    def test_find_by_query_respects_max_results_limit(self):
        """
        Test that find_by_query respects the max_results limit.

        This verifies result limiting functionality.
        """
        # Search with broad terms but limit to 2 results
        query = SearchQuery(
            terms=["analysis", "function"],  # Should match multiple papers
            max_results=2,
        )

        results = self.repository.find_by_query(query)

        # Should return at most 2 results
        self.assertLessEqual(len(results), 2)

    def test_find_by_query_returns_empty_list_for_no_matches(self):
        """
        Test that find_by_query returns empty list when no papers match.

        This verifies proper handling of no results.
        """
        # Search for terms that don't exist in any paper
        query = SearchQuery(terms=["nonexistent", "fictional"])

        results = self.repository.find_by_query(query)

        self.assertEqual(len(results), 0)
        self.assertIsInstance(results, list)


class TestInMemoryPaperRepositoryEdgeCases(unittest.TestCase):
    """
    Test edge cases and error conditions for InMemoryPaperRepository.

    This test class validates proper handling of unusual inputs and error conditions.

    Educational Note:
    Edge case testing ensures the repository is robust and handles
    unexpected inputs gracefully without crashing.
    """

    def setUp(self):
        """Set up test fixtures for edge case testing."""
        self.repository = InMemoryPaperRepository()

    def test_save_paper_handles_none_input(self):
        """
        Test that save_paper handles None input appropriately.

        This verifies proper error handling for invalid input.
        """
        with self.assertRaises(ValueError) as context:
            self.repository.save_paper(None)

        self.assertIn("Paper cannot be None", str(context.exception))

    def test_save_papers_handles_empty_list(self):
        """
        Test that save_papers handles empty list input.

        This verifies proper handling of edge case input.
        """
        # Should not raise an error
        self.repository.save_papers([])

        # Repository should still be empty
        query = SearchQuery(terms=["any"])
        results = self.repository.find_by_query(query)
        self.assertEqual(len(results), 0)

    def test_save_papers_handles_none_in_list(self):
        """
        Test that save_papers handles None values in the list.

        This verifies proper error handling for invalid list contents.
        """
        valid_paper = ResearchPaper(
            title="Valid Paper",
            authors=["Dr. Test"],
            publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            doi="10.1000/valid",
        )

        with self.assertRaises(ValueError) as context:
            self.repository.save_papers([valid_paper, None])

        self.assertIn("All papers must be non-None", str(context.exception))

    def test_duplicate_doi_overwrites_existing_paper(self):
        """
        Test that saving a paper with duplicate DOI overwrites the existing one.

        This verifies proper handling of duplicate identifiers.
        """
        # Create two papers with same DOI but different content
        paper_v1 = ResearchPaper(
            title="Original Title",
            authors=["Dr. Original"],
            publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            doi="10.1000/duplicate",
            citation_count=10,
        )

        paper_v2 = ResearchPaper(
            title="Updated Title",
            authors=["Dr. Updated"],
            publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            doi="10.1000/duplicate",
            citation_count=20,
        )

        # Save first version
        self.repository.save_paper(paper_v1)

        # Save second version (should overwrite)
        self.repository.save_paper(paper_v2)

        # Retrieve and verify it's the updated version
        retrieved_paper = self.repository.find_by_doi("10.1000/duplicate")
        self.assertEqual(retrieved_paper.title, "Updated Title")
        self.assertEqual(retrieved_paper.citation_count, 20)


if __name__ == "__main__":
    unittest.main()


# Educational Notes for Students:
#
# 1. Infrastructure Testing Strategy:
#    - Test real implementations, not mocks
#    - Verify interface compliance with isinstance checks
#    - Test data persistence across multiple operations
#    - Cover both happy path and error conditions
#
# 2. Repository Testing Patterns:
#    - Test all CRUD operations (Create, Read, Update, Delete)
#    - Verify search and filtering functionality
#    - Test edge cases like empty results and invalid input
#    - Ensure proper error handling and meaningful error messages
#
# 3. Search Functionality Testing:
#    - Test various search criteria combinations
#    - Verify filtering works correctly (dates, citations, etc.)
#    - Test result limiting and pagination concepts
#    - Ensure search returns expected data structures
#
# 4. Data Setup Strategies:
#    - Use realistic test data that represents actual use cases
#    - Create diverse datasets to test filtering capabilities
#    - Use setUp methods to prepare consistent test environments
#    - Clean test data ensures repeatable test results
#
# 5. Edge Case Considerations:
#    - Test with None values and empty collections
#    - Test duplicate data handling
#    - Test boundary conditions (empty results, large datasets)
#    - Verify graceful degradation under unusual conditions
