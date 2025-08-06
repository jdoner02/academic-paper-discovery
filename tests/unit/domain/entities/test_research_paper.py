"""
Unit tests for the ResearchPaper domain entity.

This module tests the core business logic of research papers, including
validation rules, behavior, and invariants. Following TDD principles,
these tests define the expected behavior before implementation.

Educational Notes:
- We're testing the domain entity in isolation (unit testing)
- Tests are organized by behavior/scenario, not just methods
- Each test has a clear Arrange-Act-Assert structure
- We test both happy paths and edge cases

Testing Strategy:
1. Test object creation and validation
2. Test business rules and invariants
3. Test behavior methods
4. Test equality and representation
"""

import pytest
from datetime import datetime, timezone
from typing import List

# Import our domain entity
from src.domain.entities.research_paper import ResearchPaper


class TestResearchPaperCreation:
    """
    Test suite for ResearchPaper creation and validation.

    Educational Note:
    - Grouping related tests in classes improves organization
    - Class names should clearly describe what's being tested
    """

    def test_create_valid_research_paper(self, sample_authors, sample_publication_date):
        """
        Test creating a ResearchPaper with valid data.

        This is our first test - it defines what a valid ResearchPaper looks like.
        Following TDD, we write this test first, then implement just enough
        to make it pass.

        Educational Note:
        - Arrange-Act-Assert pattern makes tests clear
        - We use descriptive variable names
        - Fixtures provide reusable test data
        """
        # Arrange - Set up test data
        title = "Heart Rate Variability in Traumatic Brain Injury Patients"
        abstract = (
            "This study examines HRV patterns in TBI patients using ECG analysis."
        )
        doi = "10.1000/test.2024.001"
        arxiv_id = "2024.0001"
        url = "https://arxiv.org/abs/2024.0001"

        # Act - Create the research paper
        paper = ResearchPaper(
            title=title,
            authors=sample_authors,
            abstract=abstract,
            publication_date=sample_publication_date,
            doi=doi,
            arxiv_id=arxiv_id,
            url=url,
        )

        # Assert - Verify the paper was created correctly
        assert paper.title == title
        assert paper.authors == sample_authors
        assert paper.abstract == abstract
        assert paper.publication_date == sample_publication_date
        assert paper.doi == doi
        assert paper.arxiv_id == arxiv_id
        assert paper.url == url

    def test_create_paper_with_minimal_required_fields(self, sample_publication_date):
        """
        Test creating a ResearchPaper with only required fields.

        This test helps us identify what fields are truly required
        versus optional for our domain model.
        """
        # Arrange - minimal required data
        title = "Minimal HRV Study"
        authors = ["Dr. Test Author"]
        doi = "10.1000/minimal.2024"

        # Act - Create paper with minimal fields
        paper = ResearchPaper(
            title=title,
            authors=authors,
            publication_date=sample_publication_date,
            doi=doi,
        )

        # Assert - Verify required fields are set and optional fields have defaults
        assert paper.title == title
        assert paper.authors == authors
        assert paper.publication_date == sample_publication_date
        assert paper.doi == doi
        assert paper.abstract == ""  # Default value
        assert paper.arxiv_id is None  # Default value
        assert paper.citation_count == 0  # Default value

    def test_reject_paper_with_empty_title(
        self, sample_authors, sample_publication_date
    ):
        """
        Test that papers with empty titles are rejected.

        Business Rule: Every research paper must have a meaningful title.
        This is a domain invariant that should always be enforced.
        """
        # Arrange - empty title
        empty_title = ""
        doi = "10.1000/empty.title"

        # Act & Assert - Should raise ValueError
        with pytest.raises(ValueError, match="non-empty title"):
            ResearchPaper(
                title=empty_title,
                authors=sample_authors,
                publication_date=sample_publication_date,
                doi=doi,
            )

    def test_reject_paper_with_no_authors(self, sample_publication_date):
        """
        Test that papers without authors are rejected.

        Business Rule: Every research paper must have at least one author.
        Anonymous papers are not valid in academic contexts.
        """
        # Arrange - no authors
        title = "A Paper With No Authors"
        empty_authors = []
        doi = "10.1000/no.authors"

        # Act & Assert - Should raise ValueError
        with pytest.raises(ValueError, match="at least one author"):
            ResearchPaper(
                title=title,
                authors=empty_authors,
                publication_date=sample_publication_date,
                doi=doi,
            )

    def test_reject_paper_with_future_publication_date(self, sample_authors):
        """
        Test that papers with future publication dates are rejected.

        Business Rule: Papers cannot be published in the future.
        This prevents data entry errors and ensures data integrity.
        """
        # Arrange - future publication date
        title = "Paper From The Future"
        future_date = datetime(2030, 1, 1, tzinfo=timezone.utc)
        doi = "10.1000/future.paper"

        # Act & Assert - Should raise ValueError
        with pytest.raises(ValueError, match="cannot be in the future"):
            ResearchPaper(
                title=title,
                authors=sample_authors,
                publication_date=future_date,
                doi=doi,
            )


class TestResearchPaperBehavior:
    """
    Test suite for ResearchPaper behavior and methods.

    Educational Note:
    - Separate class for behavior tests keeps organization clear
    - Behavior tests focus on what the object does, not just what it contains
    """

    def test_paper_equality_based_on_identity(
        self, sample_authors, sample_publication_date
    ):
        """
        Test that papers are equal if they have the same identity (DOI or ArXiv ID).

        Business Rule: Papers with the same DOI or ArXiv ID are the same paper,
        even if other metadata differs (different versions, etc.).
        """
        # Arrange - two papers with same DOI but different metadata
        doi = "10.1000/same.paper"

        paper1 = ResearchPaper(
            title="Original Title",
            authors=["Author One"],
            publication_date=sample_publication_date,
            doi=doi,
            abstract="Original abstract",
        )

        paper2 = ResearchPaper(
            title="Updated Title",
            authors=["Author One", "Author Two"],  # Different authors
            publication_date=sample_publication_date,
            doi=doi,  # Same DOI
            abstract="Updated abstract",  # Different abstract
        )

        # Act & Assert - Papers should be equal based on identity
        assert paper1 == paper2
        assert hash(paper1) == hash(paper2)  # Hash consistency

    def test_paper_string_representation(self, sample_authors, sample_publication_date):
        """
        Test that papers have a useful string representation.

        Educational Note:
        - Good __str__ methods make debugging easier
        - Should include key identifying information
        """
        # Arrange
        title = "A Study of Heart Rate Variability in Athletes"
        doi = "10.1000/athlete.hrv"

        paper = ResearchPaper(
            title=title,
            authors=sample_authors,
            publication_date=sample_publication_date,
            doi=doi,
        )

        # Act
        str_repr = str(paper)

        # Assert - Should contain key information
        assert "Heart Rate Variability" in str_repr
        assert "Dr. Jane Smith" in str_repr  # First author from fixture
        assert "2024" in str_repr  # Publication year

    def test_paper_is_hrv_relevant(
        self, sample_authors, sample_publication_date, hrv_keywords
    ):
        """
        Test detection of HRV-relevant papers.

        Business Rule: Papers are HRV-relevant if they contain specific
        keywords in title or abstract. This is core domain logic.
        """
        # Arrange - paper with HRV content
        title = "Analysis of Heart Rate Variability in Clinical Settings"
        abstract = "We studied HRV patterns using ECG monitoring in 100 patients."
        doi = "10.1000/hrv.study"

        paper = ResearchPaper(
            title=title,
            authors=sample_authors,
            publication_date=sample_publication_date,
            doi=doi,
            abstract=abstract,
        )

        # Act & Assert
        assert paper.is_hrv_relevant() is True

    def test_paper_is_not_hrv_relevant(self, sample_authors, sample_publication_date):
        """
        Test that non-HRV papers are correctly identified.

        This ensures our relevance detection doesn't have false positives.
        """
        # Arrange - paper without HRV content
        title = "Machine Learning Applications in Software Engineering"
        abstract = "This paper discusses neural networks for code optimization."
        doi = "10.1000/ml.software"

        paper = ResearchPaper(
            title=title,
            authors=sample_authors,
            publication_date=sample_publication_date,
            doi=doi,
            abstract=abstract,
        )

        # Act & Assert
        assert paper.is_hrv_relevant() is False


class TestResearchPaperEdgeCases:
    """
    Test suite for edge cases and error conditions.

    Educational Note:
    - Edge case testing ensures robustness
    - These tests often reveal assumptions in our design
    """

    def test_paper_with_very_long_title(self, sample_authors, sample_publication_date):
        """
        Test handling of extremely long titles.

        Should we truncate? Reject? This test helps us decide.
        """
        # Arrange - very long title
        long_title = "A" * 300  # 300 character title
        doi = "10.1000/long.title"

        # Act - Should handle long titles gracefully
        paper = ResearchPaper(
            title=long_title,
            authors=sample_authors,
            publication_date=sample_publication_date,
            doi=doi,
        )

        # Assert - Title should be preserved as-is
        assert paper.title == long_title
        assert len(paper.title) == 300

    def test_paper_with_unicode_characters(self, sample_publication_date):
        """
        Test handling of international characters in metadata.

        Academic papers often contain special characters, accents, etc.
        """
        # Arrange - paper with unicode characters
        title = "Étude de la variabilité du rythme cardiaque chez les athlètes"
        authors = ["Dr. François Müller", "Prof. José García-López"]
        doi = "10.1000/unicode.test"

        # Act
        paper = ResearchPaper(
            title=title,
            authors=authors,
            publication_date=sample_publication_date,
            doi=doi,
        )

        # Assert - Should handle unicode correctly
        assert paper.title == title
        assert paper.authors == authors
        assert "François" in paper.authors[0]
        assert "José" in paper.authors[1]

    def test_paper_without_standard_identifiers_allowed_for_multi_source_support(
        self, sample_authors, sample_publication_date
    ):
        """
        Test that papers without DOI or ArXiv ID are now allowed for multi-source support.

        Educational Note:
        The validation was relaxed to support sources like Google Scholar
        that may not provide standard academic identifiers. PaperFingerprint
        will create composite identifiers from title+author combinations.
        """
        # Arrange - paper without DOI or ArXiv ID
        title = "Conference Paper Without Standard Identifiers"

        # Act - Should succeed with multi-source support
        paper = ResearchPaper(
            title=title,
            authors=sample_authors,
            publication_date=sample_publication_date,
            # No DOI or ArXiv ID provided - this is now allowed
        )

        # Assert - Paper created successfully
        assert paper.title == title
        assert paper.authors == sample_authors
        assert paper.doi is None
        assert paper.arxiv_id is None

    def test_paper_with_missing_abstract(self, sample_authors, sample_publication_date):
        """
        Test handling of papers without abstracts.

        Some papers (especially older ones) might not have abstracts.
        """
        # Arrange - paper without abstract (using default empty string)
        title = "A Paper Without Abstract"
        doi = "10.1000/no.abstract"

        # Act
        paper = ResearchPaper(
            title=title,
            authors=sample_authors,
            publication_date=sample_publication_date,
            doi=doi,
            # No abstract provided - should use default
        )

        # Assert
        assert paper.abstract == ""
        # Should still be able to check HRV relevance (won't match due to empty abstract)
        assert paper.is_hrv_relevant() is False


# Educational Note:
# At this point, all tests are skipped because we haven't implemented
# ResearchPaper yet. This is the "Red" phase of TDD:
# 1. RED: Write failing tests
# 2. GREEN: Write minimal code to make tests pass
# 3. REFACTOR: Improve code quality while keeping tests green
#
# Next step: Implement ResearchPaper to make these tests pass!
