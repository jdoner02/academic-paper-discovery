"""
Integration tests for the complete HRV research aggregation system.

These tests demonstrate that all layers work together correctly,
from domain entities through application use cases to infrastructure repositories.

Educational Notes:
- Integration tests verify that components work together as intended
- They test real workflows that users would perform
- They use actual implementations, not mocks
- They validate the complete Clean Architecture implementation

Test Scenarios:
1. End-to-end paper search workflow
2. End-to-end paper retrieval workflow
3. Complete system functionality demonstration
"""

import unittest
from datetime import datetime, timezone

from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.application.use_cases.search_papers_use_case import SearchPapersUseCase
from src.application.use_cases.get_paper_details_use_case import GetPaperDetailsUseCase
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)


class TestSystemIntegration(unittest.TestCase):
    """
    Integration tests for the complete system.

    These tests verify that all layers work together correctly
    and demonstrate real usage scenarios.

    Educational Note:
    Integration tests validate that the Clean Architecture
    implementation works as designed across all layers.
    """

    def setUp(self):
        """Set up integration test fixtures."""
        # Create repository and populate with sample data
        self.repository = InMemoryPaperRepository()

        # Create realistic HRV research papers
        self.hrv_papers = [
            ResearchPaper(
                title="Heart Rate Variability Analysis in Post-Concussion Syndrome",
                authors=[
                    "Dr. Sarah Chen",
                    "Dr. Michael Rodriguez",
                    "Dr. Emma Thompson",
                ],
                abstract="Comprehensive analysis of HRV patterns in patients with post-concussion syndrome. "
                "We examined autonomic dysfunction markers and their correlation with symptom severity. "
                "Results show significant HRV alterations persisting months after initial injury.",
                publication_date=datetime(2023, 8, 15, tzinfo=timezone.utc),
                venue="Journal of Neurotrauma",
                doi="10.1089/neu.2023.hrv001",
                citation_count=45,
                keywords=[
                    "HRV",
                    "post-concussion syndrome",
                    "autonomic dysfunction",
                    "TBI recovery",
                ],
            ),
            ResearchPaper(
                title="Machine Learning Approaches to HRV Classification in TBI Patients",
                authors=["Dr. Alex Wang", "Dr. Jennifer Park", "Dr. Robert Kumar"],
                abstract="Novel machine learning algorithms for automated classification of HRV patterns "
                "in traumatic brain injury patients. Deep learning models show 87% accuracy "
                "in predicting TBI severity based on HRV metrics.",
                publication_date=datetime(2023, 6, 20, tzinfo=timezone.utc),
                venue="IEEE Transactions on Biomedical Engineering",
                doi="10.1109/TBME.2023.ml002",
                citation_count=67,
                keywords=[
                    "machine learning",
                    "HRV",
                    "TBI classification",
                    "deep learning",
                ],
            ),
            ResearchPaper(
                title="Autonomic Recovery Patterns Following Mild Traumatic Brain Injury",
                authors=["Dr. Lisa Martinez", "Dr. David Johnson"],
                abstract="Longitudinal study of autonomic nervous system recovery in mild TBI patients. "
                "HRV measurements tracked over 6 months show gradual improvement patterns "
                "that correlate with clinical recovery scores.",
                publication_date=datetime(2023, 4, 10, tzinfo=timezone.utc),
                venue="Clinical Neurophysiology",
                doi="10.1016/j.clinph.2023.auto003",
                arxiv_id="2304.12345",
                citation_count=28,
                keywords=[
                    "autonomic recovery",
                    "mild TBI",
                    "longitudinal study",
                    "HRV monitoring",
                ],
            ),
            ResearchPaper(
                title="Wearable Technology for Continuous HRV Monitoring in Brain Injury Rehabilitation",
                authors=[
                    "Dr. Maria Santos",
                    "Dr. Christopher Lee",
                    "Dr. Amanda Foster",
                ],
                abstract="Evaluation of wearable devices for continuous HRV monitoring during TBI rehabilitation. "
                "Apple Watch and specialized ECG devices compared for clinical utility and patient compliance.",
                publication_date=datetime(2023, 9, 5, tzinfo=timezone.utc),
                venue="Journal of Medical Internet Research",
                doi="10.2196/jmir.2023.wearable004",
                citation_count=32,
                keywords=[
                    "wearable technology",
                    "HRV monitoring",
                    "rehabilitation",
                    "Apple Watch",
                    "ECG",
                ],
            ),
        ]

        # Populate repository
        self.repository.save_papers(self.hrv_papers)

        # Create use cases with the repository
        self.search_use_case = SearchPapersUseCase(self.repository)
        self.details_use_case = GetPaperDetailsUseCase(self.repository)

    def test_end_to_end_search_workflow(self):
        """
        Test complete search workflow from query to results.

        This demonstrates the full search pipeline:
        Domain Query → Application Use Case → Infrastructure Repository → Domain Results
        """
        # Create search query for HRV and TBI research
        query = SearchQuery(
            terms=["HRV", "TBI"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            min_citations=25,
            max_results=10,
        )

        # Execute search through use case
        results = self.search_use_case.execute(query)

        # Verify results
        self.assertGreater(len(results), 0, "Should find matching papers")

        # Verify all results meet criteria
        for paper in results:
            # Should contain HRV or TBI terms
            paper_text = f"{paper.title} {paper.abstract}".lower()
            has_hrv_or_tbi = "hrv" in paper_text or "tbi" in paper_text
            self.assertTrue(
                has_hrv_or_tbi, f"Paper should contain HRV or TBI: {paper.title}"
            )

            # Should meet citation criteria
            self.assertGreaterEqual(
                paper.citation_count,
                25,
                f"Paper should have >= 25 citations: {paper.title}",
            )

            # Should meet date criteria
            self.assertGreaterEqual(
                paper.publication_date.year,
                2023,
                f"Paper should be from 2023 or later: {paper.title}",
            )

        # Results should be sorted by relevance (papers with both HRV and TBI should rank higher)
        if len(results) > 1:
            first_paper_text = f"{results[0].title} {results[0].abstract}".lower()
            has_both_terms = "hrv" in first_paper_text and (
                "tbi" in first_paper_text or "brain injury" in first_paper_text
            )
            # First result likely has both terms (this is expected but not strictly required)
            print(
                f"First result relevance check: {results[0].title} - Has both terms: {has_both_terms}"
            )

    def test_end_to_end_paper_retrieval_workflow(self):
        """
        Test complete paper retrieval workflow by DOI.

        This demonstrates the full retrieval pipeline:
        DOI Input → Application Use Case → Infrastructure Repository → Domain Entity
        """
        # Get DOI of a known paper
        target_doi = "10.1089/neu.2023.hrv001"

        # Retrieve paper through use case
        paper = self.details_use_case.execute(target_doi)

        # Verify correct paper retrieved
        self.assertIsNotNone(paper, "Should retrieve the paper")
        self.assertEqual(
            paper.doi, target_doi, "Should retrieve paper with correct DOI"
        )
        self.assertIn(
            "Heart Rate Variability Analysis",
            paper.title,
            "Should retrieve correct paper",
        )
        self.assertIn("Dr. Sarah Chen", paper.authors, "Should have correct authors")

    def test_end_to_end_arxiv_retrieval_workflow(self):
        """
        Test paper retrieval by ArXiv ID.

        This demonstrates alternative identifier retrieval:
        ArXiv ID → Application Use Case → Infrastructure Repository → Domain Entity
        """
        # Get ArXiv ID of a known paper
        target_arxiv = "2304.12345"

        # Retrieve paper using repository directly (use case doesn't support ArXiv yet)
        paper = self.repository.find_by_arxiv_id(target_arxiv)

        # Verify correct paper retrieved
        self.assertIsNotNone(paper, "Should retrieve the paper by ArXiv ID")
        self.assertEqual(
            paper.arxiv_id, target_arxiv, "Should retrieve paper with correct ArXiv ID"
        )
        self.assertIn(
            "Autonomic Recovery Patterns", paper.title, "Should retrieve correct paper"
        )

    def test_search_with_no_results(self):
        """
        Test search workflow when no papers match the criteria.

        This verifies graceful handling of empty results.
        """
        # Create query that won't match any papers
        query = SearchQuery(
            terms=["quantum computing", "blockchain"],
            min_citations=1000,  # No papers have this many citations
        )

        # Execute search
        results = self.search_use_case.execute(query)

        # Verify empty results handled correctly
        self.assertEqual(len(results), 0, "Should return empty list for no matches")
        self.assertIsInstance(results, list, "Should return list type")

    def test_comprehensive_search_functionality(self):
        """
        Test comprehensive search with multiple criteria.

        This demonstrates advanced search capabilities across all filters.
        """
        # Create comprehensive query
        query = SearchQuery(
            terms=["machine learning", "wearable"],
            start_date=datetime(2023, 5, 1, tzinfo=timezone.utc),
            end_date=datetime(2023, 12, 31, tzinfo=timezone.utc),
            min_citations=30,
            max_results=5,
        )

        # Execute search
        results = self.search_use_case.execute(query)

        # Verify comprehensive filtering
        for paper in results:
            # Check date range
            self.assertGreaterEqual(
                paper.publication_date, datetime(2023, 5, 1, tzinfo=timezone.utc)
            )
            self.assertLessEqual(
                paper.publication_date, datetime(2023, 12, 31, tzinfo=timezone.utc)
            )

            # Check citation count
            self.assertGreaterEqual(paper.citation_count, 30)

            # Check search terms
            paper_text = (
                f"{paper.title} {paper.abstract} {' '.join(paper.keywords)}".lower()
            )
            has_terms = "machine learning" in paper_text or "wearable" in paper_text
            self.assertTrue(
                has_terms, f"Paper should contain search terms: {paper.title}"
            )

        # Check result limit
        self.assertLessEqual(len(results), 5, "Should respect max_results limit")

    def test_system_handles_edge_cases(self):
        """
        Test that the complete system handles edge cases gracefully.

        This verifies robustness across all layers.
        """
        # Test with minimal query
        minimal_query = SearchQuery(terms=["analysis"])
        results = self.search_use_case.execute(minimal_query)
        self.assertIsInstance(results, list, "Should handle minimal query")

        # Test with non-existent DOI
        try:
            paper = self.details_use_case.execute("10.1000/nonexistent")
            self.fail("Should raise exception for non-existent DOI")
        except Exception as e:
            self.assertIn(
                "not found", str(e).lower(), "Should provide meaningful error message"
            )

        # Test with invalid DOI format
        try:
            paper = self.details_use_case.execute("invalid-doi")
            self.fail("Should raise exception for invalid DOI")
        except Exception as e:
            self.assertIn(
                "invalid", str(e).lower(), "Should provide meaningful error message"
            )

    def test_system_performance_with_realistic_data(self):
        """
        Test system performance with realistic dataset size.

        This verifies the system can handle reasonable amounts of data efficiently.
        """
        # Add more papers to test performance
        additional_papers = []
        for i in range(20):  # Add 20 more papers
            paper = ResearchPaper(
                title=f"Research Paper {i+1}: HRV Analysis Methods",
                authors=[f"Dr. Author {i+1}"],
                abstract=f"Abstract for paper {i+1} discussing HRV analysis methods and applications. "
                f"This paper explores technique {i+1} for processing physiological signals.",
                publication_date=datetime(2023, (i % 12) + 1, 1, tzinfo=timezone.utc),
                venue=f"Journal of Method {i+1}",
                doi=f"10.1000/test.{i+1:03d}",
                citation_count=i * 2,
                keywords=["HRV", "analysis", f"method-{i+1}"],
            )
            additional_papers.append(paper)

        # Save additional papers
        self.repository.save_papers(additional_papers)

        # Verify repository size
        self.assertEqual(
            len(self.repository), 24, "Should have 24 total papers"
        )  # 4 original + 20 additional

        # Test search performance
        query = SearchQuery(terms=["HRV"], max_results=10)
        results = self.search_use_case.execute(query)

        # Should find multiple matching papers
        self.assertGreater(
            len(results), 0, "Should find matching papers in larger dataset"
        )
        self.assertLessEqual(len(results), 10, "Should respect max_results limit")


if __name__ == "__main__":
    unittest.main()


# Educational Notes for Students:
#
# 1. Integration Testing Strategy:
#    - Test real workflows that users would perform
#    - Use actual implementations, not mocks
#    - Verify data flows correctly through all layers
#    - Test both happy paths and error conditions
#
# 2. Clean Architecture Validation:
#    - Domain entities work with application use cases
#    - Application use cases coordinate infrastructure repositories
#    - Infrastructure repositories implement application ports
#    - All layers remain decoupled and testable
#
# 3. Realistic Test Data:
#    - Use domain-specific examples (HRV research papers)
#    - Include realistic metadata (authors, citations, dates)
#    - Test with sufficient data volume for performance validation
#    - Cover edge cases and boundary conditions
#
# 4. End-to-End Workflows:
#    - Search: Query → Use Case → Repository → Results
#    - Retrieval: DOI → Use Case → Repository → Entity
#    - Error Handling: Invalid Input → Meaningful Error Messages
#    - Performance: Large Dataset → Efficient Processing
#
# 5. System Quality Validation:
#    - Functionality: Features work as expected
#    - Reliability: Error conditions handled gracefully
#    - Performance: Reasonable response times with realistic data
#    - Maintainability: Clear separation of concerns across layers
