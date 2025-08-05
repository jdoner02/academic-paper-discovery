"""
Test cases for count_all method in paper repositories.

This test module ensures that the count_all method works correctly
across all repository implementations.
"""

import pytest
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.infrastructure.repositories.sqlite_paper_repository import (
    SQLitePaperRepository,
)
from src.domain.entities.research_paper import ResearchPaper
from datetime import datetime, date, timezone


@pytest.fixture
def sample_papers():
    """Create sample papers for testing."""
    return [
        ResearchPaper(
            doi="10.1000/182",
            title="HRV Analysis in TBI Patients",
            abstract="Heart rate variability analysis in traumatic brain injury patients.",
            publication_date=datetime(2023, 1, 15, tzinfo=timezone.utc),
            authors=["Dr. Smith", "Dr. Johnson"],
            venue="Journal of Medical Research",
            arxiv_id="2301.00001",
            citation_count=15,
        ),
        ResearchPaper(
            doi="10.1000/183",
            title="Apple Watch ECG Validation",
            abstract="Validation of Apple Watch ECG for medical research applications.",
            publication_date=datetime(2023, 2, 20, tzinfo=timezone.utc),
            authors=["Dr. Brown", "Dr. Davis"],
            venue="Digital Health Journal",
            arxiv_id="2302.00001",
            citation_count=8,
        ),
        ResearchPaper(
            doi="10.1000/184",
            title="Machine Learning for HRV",
            abstract="Machine learning approaches for heart rate variability analysis.",
            publication_date=datetime(2023, 3, 10, tzinfo=timezone.utc),
            authors=["Dr. Wilson", "Dr. Garcia"],
            venue="AI in Medicine",
            citation_count=22,
        ),
    ]


class TestInMemoryRepositoryCountAll:
    """Test count_all method for InMemoryPaperRepository."""

    def test_count_all_empty_repository(self):
        """Test count_all returns 0 for empty repository."""
        repository = InMemoryPaperRepository()
        assert repository.count_all() == 0

    def test_count_all_single_paper(self, sample_papers):
        """Test count_all returns correct count for single paper."""
        repository = InMemoryPaperRepository()
        repository.save_paper(sample_papers[0])
        assert repository.count_all() == 1

    def test_count_all_multiple_papers(self, sample_papers):
        """Test count_all returns correct count for multiple papers."""
        repository = InMemoryPaperRepository()
        repository.save_papers(sample_papers)
        assert repository.count_all() == 3

    def test_count_all_after_duplicate_save(self, sample_papers):
        """Test count_all handles duplicate saves correctly."""
        repository = InMemoryPaperRepository()
        repository.save_paper(sample_papers[0])
        repository.save_paper(sample_papers[0])  # Duplicate save
        assert repository.count_all() == 1

    def test_count_all_performance(self):
        """Test count_all performance with many papers."""
        repository = InMemoryPaperRepository()

        # Create many papers
        papers = []
        for i in range(1000):
            paper = ResearchPaper(
                doi=f"10.1000/{i}",
                title=f"Test Paper {i}",
                abstract=f"Abstract for paper {i}",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                authors=[f"Author {i}"],
                venue="Test Journal",
                citation_count=i,
            )
            papers.append(paper)

        repository.save_papers(papers)
        assert repository.count_all() == 1000


class TestSQLiteRepositoryCountAll:
    """Test count_all method for SQLitePaperRepository."""

    def test_count_all_empty_repository(self):
        """Test count_all returns 0 for empty repository."""
        repository = SQLitePaperRepository(":memory:")
        assert repository.count_all() == 0

    def test_count_all_single_paper(self, sample_papers):
        """Test count_all returns correct count for single paper."""
        repository = SQLitePaperRepository(":memory:")
        repository.save_paper(sample_papers[0])
        assert repository.count_all() == 1

    def test_count_all_multiple_papers(self, sample_papers):
        """Test count_all returns correct count for multiple papers."""
        repository = SQLitePaperRepository(":memory:")
        repository.save_papers(sample_papers)
        assert repository.count_all() == 3

    def test_count_all_after_duplicate_save(self, sample_papers):
        """Test count_all handles duplicate saves correctly."""
        repository = SQLitePaperRepository(":memory:")
        repository.save_paper(sample_papers[0])
        repository.save_paper(sample_papers[0])  # Duplicate save
        assert repository.count_all() == 1

    def test_count_all_after_update(self, sample_papers):
        """Test count_all remains stable after paper updates."""
        repository = SQLitePaperRepository(":memory:")
        repository.save_paper(sample_papers[0])

        # Update the paper
        updated_paper = ResearchPaper(
            doi=sample_papers[0].doi,  # Same DOI
            title="Updated Title",
            abstract=sample_papers[0].abstract,
            publication_date=sample_papers[0].publication_date,
            authors=sample_papers[0].authors,
            venue=sample_papers[0].venue,
            citation_count=100,  # Updated citation count
        )
        repository.save_paper(updated_paper)

        # Count should remain 1
        assert repository.count_all() == 1

    def test_count_all_performance(self):
        """Test count_all performance with many papers."""
        repository = SQLitePaperRepository(":memory:")

        # Create many papers
        papers = []
        for i in range(1000):
            paper = ResearchPaper(
                doi=f"10.1000/{i}",
                title=f"Test Paper {i}",
                abstract=f"Abstract for paper {i}",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                authors=[f"Author {i}"],
                venue="Test Journal",
                citation_count=i,
            )
            papers.append(paper)

        repository.save_papers(papers)
        assert repository.count_all() == 1000


class TestCountAllConsistency:
    """Test consistency between repository implementations."""

    def test_both_repositories_return_same_count(self, sample_papers):
        """Test that both repositories return the same count for same data."""
        memory_repo = InMemoryPaperRepository()
        sqlite_repo = SQLitePaperRepository(":memory:")

        # Save same papers to both repositories
        memory_repo.save_papers(sample_papers)
        sqlite_repo.save_papers(sample_papers)

        # Both should return same count
        assert memory_repo.count_all() == sqlite_repo.count_all()
        assert memory_repo.count_all() == 3
