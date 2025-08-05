"""
Test configuration and fixtures for the HRV Research Aggregator.

This file contains pytest configuration and shared fixtures that are used
across multiple test modules. It's automatically discovered by pytest and
provides a centralized place for test setup.

Educational Note:
- conftest.py is a special pytest file that defines fixtures and configuration
- Fixtures provide reusable test data and setup/teardown logic
- The scope parameter controls fixture lifetime (function, class, module, session)
"""

import pytest
from datetime import datetime, timezone
from typing import List

# We'll import our domain objects as we create them
# from src.domain.entities.research_paper import ResearchPaper
# from src.domain.entities.author import Author
# from src.domain.value_objects.search_query import SearchQuery


@pytest.fixture
def sample_authors() -> List[str]:
    """
    Provides sample author data for testing.

    Educational Note:
    - Fixtures are functions marked with @pytest.fixture
    - They provide reusable test data or setup logic
    - Other tests can use this by including 'sample_authors' as a parameter
    """
    return ["Dr. Jane Smith", "Prof. John Doe", "Dr. Sarah Johnson"]


@pytest.fixture
def sample_publication_date() -> datetime:
    """
    Provides a consistent publication date for testing.

    Educational Note:
    - Using timezone-aware datetimes prevents timezone-related bugs
    - Fixed test dates ensure reproducible test results
    """
    return datetime(2024, 1, 15, tzinfo=timezone.utc)


@pytest.fixture
def hrv_keywords() -> List[str]:
    """
    Provides HRV-related keywords for testing relevance detection.

    Educational Note:
    - Domain-specific test data helps verify business rules
    - This fixture encapsulates knowledge about what makes a paper relevant
    """
    return [
        "heart rate variability",
        "HRV",
        "R-R interval",
        "cardiac autonomic",
        "vagal tone",
    ]


# We'll add more fixtures as we develop the system
# @pytest.fixture
# def sample_research_paper(sample_authors, sample_publication_date):
#     """Creates a valid ResearchPaper for testing."""
#     pass
