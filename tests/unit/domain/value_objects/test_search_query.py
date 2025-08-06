"""
Unit tests for the SearchQuery domain value object.

This module tests the SearchQuery value object, which encapsulates search
parameters for finding research papers. As a value object, it should be
immutable and comparable by value, not identity.

Educational Notes:
- Value objects represent concepts without identity (unlike entities)
- They should be immutable to prevent accidental modification
- Equality is based on all attributes, not identity
- They often encapsulate validation logic for complex data

Testing Strategy:
1. Test object creation and validation
2. Test immutability characteristics
3. Test equality and hashing behavior
4. Test business logic methods
5. Test edge cases and error conditions
"""

import pytest
from datetime import datetime, timezone, timedelta
from typing import List

# Import will work after we create the value object
from src.domain.value_objects.search_query import SearchQuery


class TestSearchQueryCreation:
    """
    Test suite for SearchQuery creation and validation.
    
    Educational Note:
    - Value objects should validate their data upon creation
    - Invalid combinations should be rejected early
    """
    
    def test_create_valid_search_query(self):
        """
        Test creating a SearchQuery with valid parameters.
        
        This defines the basic structure and validation of our search queries.
        """
        # Arrange
        terms = ["heart rate variability", "HRV analysis"]
        start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 1, 1, tzinfo=timezone.utc) 
        max_results = 50
        min_citations = 5
        
        # Act
        query = SearchQuery(
            terms=terms,
            start_date=start_date,
            end_date=end_date,
            max_results=max_results,
            min_citations=min_citations
        )
        
        # Assert
        assert query.terms == tuple(terms)  # Converted to tuple internally
        assert query.start_date == start_date
        assert query.end_date == end_date
        assert query.max_results == max_results
        assert query.min_citations == min_citations

    def test_create_minimal_search_query(self):
        """
        Test creating a SearchQuery with only required fields.
        
        This helps identify what's truly required vs optional.
        """
        # Arrange - minimal required data
        terms = ["HRV"]
        
        # Act
        query = SearchQuery(terms=terms)
        
        # Assert - Check defaults are applied
        assert query.terms == tuple(terms)  # Converted to tuple internally
        assert query.start_date is None
        assert query.end_date is None
        assert query.max_results == 100  # Default value
        assert query.min_citations == 0  # Default value

    def test_reject_empty_search_terms(self):
        """
        Test that queries with no search terms are rejected.
        
        Business Rule: A search query must have at least one search term.
        """
        # Arrange
        empty_terms = []
        
        # Act & Assert
        with pytest.raises(ValueError, match="at least one search term"):
            SearchQuery(terms=empty_terms)

    def test_reject_invalid_date_range(self):
        """
        Test that queries with end_date before start_date are rejected.
        
        Business Rule: Date ranges must be logically consistent.
        """
        # Arrange - invalid date range
        terms = ["HRV"]
        start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2023, 1, 1, tzinfo=timezone.utc)  # Before start_date
        
        # Act & Assert
        with pytest.raises(ValueError, match="start_date cannot be after end_date"):
            SearchQuery(
                terms=terms,
                start_date=start_date,
                end_date=end_date
            )

    def test_reject_negative_max_results(self):
        """
        Test that negative max_results values are rejected.
        
        Business Rule: Result limits must be positive numbers.
        """
        # Arrange
        terms = ["HRV"]
        negative_max_results = -10
        
        # Act & Assert
        with pytest.raises(ValueError, match="max_results must be positive"):
            SearchQuery(terms=terms, max_results=negative_max_results)

    def test_reject_negative_min_citations(self):
        """
        Test that negative citation minimums are rejected.
        """
        # Arrange
        terms = ["HRV"]
        negative_citations = -5
        
        # Act & Assert
        with pytest.raises(ValueError, match="min_citations cannot be negative"):
            SearchQuery(terms=terms, min_citations=negative_citations)


class TestSearchQueryBehavior:
    """
    Test suite for SearchQuery behavior and methods.
    
    Educational Note:
    - Value objects can contain behavior, not just data
    - Methods should be pure functions (no side effects)
    """
    
    def test_query_contains_date_range(self):
        """
        Test the has_date_range method for detecting date constraints.
        """
        # Arrange & Act - query with date range
        query_with_dates = SearchQuery(
            terms=["HRV"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        
        # Query without date range
        query_without_dates = SearchQuery(terms=["HRV"])
        
        # Assert
        assert query_with_dates.has_date_range() is True
        assert query_without_dates.has_date_range() is False

    def test_format_query_string(self):
        """
        Test conversion of search terms to query string.
        
        This method might be used by different search adapters.
        """
        # Arrange
        terms = ["heart rate variability", "HRV analysis", "ECG"]
        query = SearchQuery(terms=terms)
        
        # Act
        query_string = query.to_query_string()
        
        # Assert - Should combine terms appropriately
        assert "heart rate variability" in query_string
        assert "HRV analysis" in query_string
        assert "ECG" in query_string

    def test_is_within_date_range(self):
        """
        Test date range checking functionality.
        
        This is used to filter papers by publication date.
        """
        # Arrange
        start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        query = SearchQuery(
            terms=["HRV"],
            start_date=start_date,
            end_date=end_date
        )
        
        # Test dates
        date_in_range = datetime(2023, 6, 1, tzinfo=timezone.utc)
        date_before_range = datetime(2022, 6, 1, tzinfo=timezone.utc)
        date_after_range = datetime(2024, 6, 1, tzinfo=timezone.utc)
        
        # Act & Assert
        assert query.is_within_date_range(date_in_range) is True
        assert query.is_within_date_range(date_before_range) is False
        assert query.is_within_date_range(date_after_range) is False

    def test_is_within_date_range_with_no_constraints(self):
        """
        Test that papers are always in range when no date constraints exist.
        """
        # Arrange
        query = SearchQuery(terms=["HRV"])  # No date constraints
        any_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
        
        # Act & Assert
        assert query.is_within_date_range(any_date) is True

    def test_is_within_date_range_with_partial_constraints(self):
        """
        Test date range checking with only start or end date specified.
        """
        # Test with only start date
        query_start_only = SearchQuery(
            terms=["HRV"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        
        # Test with only end date  
        query_end_only = SearchQuery(
            terms=["HRV"],
            end_date=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        
        test_date_early = datetime(2022, 6, 1, tzinfo=timezone.utc)
        test_date_middle = datetime(2023, 6, 1, tzinfo=timezone.utc)
        test_date_late = datetime(2024, 6, 1, tzinfo=timezone.utc)
        
        # Assert start date only behavior
        assert query_start_only.is_within_date_range(test_date_early) is False
        assert query_start_only.is_within_date_range(test_date_middle) is True
        assert query_start_only.is_within_date_range(test_date_late) is True
        
        # Assert end date only behavior
        assert query_end_only.is_within_date_range(test_date_early) is True
        assert query_end_only.is_within_date_range(test_date_middle) is True
        assert query_end_only.is_within_date_range(test_date_late) is False


class TestSearchQueryValueObjectCharacteristics:
    """
    Test suite for value object characteristics.
    
    Educational Note:
    - Value objects should be immutable
    - Equality should be based on values, not identity
    - Should be hashable for use in sets/dictionaries
    """
    
    def test_search_query_equality(self):
        """
        Test that SearchQueries with same values are equal.
        
        Value object equality is based on all attributes, not identity.
        """
        # Arrange - two queries with identical values
        terms = ["HRV", "heart rate variability"]
        start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        query1 = SearchQuery(
            terms=terms,
            start_date=start_date,
            max_results=50
        )
        
        query2 = SearchQuery(
            terms=terms,
            start_date=start_date,
            max_results=50
        )
        
        # Act & Assert
        assert query1 == query2
        assert query1 is not query2  # Different objects
        assert hash(query1) == hash(query2)  # Hash consistency

    def test_search_query_inequality(self):
        """
        Test that SearchQueries with different values are not equal.
        """
        # Arrange - queries with different values
        query1 = SearchQuery(terms=["HRV"], max_results=50)
        query2 = SearchQuery(terms=["HRV"], max_results=100)  # Different max_results
        
        # Act & Assert
        assert query1 != query2

    def test_search_query_not_equal_to_other_types(self):
        """
        Test that SearchQuery is not equal to objects of different types.
        """
        # Arrange
        query = SearchQuery(terms=["HRV"])
        not_a_query = "not a search query"
        
        # Act & Assert
        assert query != not_a_query
        assert not_a_query != query

    def test_search_query_immutability(self):
        """
        Test that SearchQuery is immutable after creation.
        
        Educational Note:
        - Immutability prevents accidental modification
        - Makes value objects safe to share between components
        """
        # Arrange
        query = SearchQuery(terms=["HRV"])
        
        # Act & Assert - Should not be able to modify attributes
        with pytest.raises(AttributeError):
            query.terms = ["different terms"]
        
        with pytest.raises(AttributeError):
            query.max_results = 200

    def test_search_query_string_representation(self):
        """
        Test that SearchQuery has useful string representation.
        """
        # Arrange
        query = SearchQuery(
            terms=["HRV", "heart rate variability"],
            max_results=50,
            min_citations=5
        )
        
        # Act
        str_repr = str(query)
        
        # Assert - Should include key information
        assert "HRV" in str_repr
        assert "50" in str_repr  # max_results
        assert "5" in str_repr   # min_citations

    def test_search_query_string_with_date_range(self):
        """
        Test string representation with different date configurations.
        """
        # Test with both dates
        query_with_range = SearchQuery(
            terms=["HRV"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        
        # Test with only start date
        query_with_start = SearchQuery(
            terms=["HRV"],
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        
        # Test with only end date
        query_with_end = SearchQuery(
            terms=["HRV"],
            end_date=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        
        # Act & Assert
        range_str = str(query_with_range)
        start_str = str(query_with_start)
        end_str = str(query_with_end)
        
        assert "dates=" in range_str
        assert "after=" in start_str
        assert "before=" in end_str


# Educational Note:
# This comprehensive test suite ensures our SearchQuery value object:
# 1. Validates input properly
# 2. Behaves as an immutable value object
# 3. Provides useful business methods
# 4. Has proper equality semantics
# 5. Handles edge cases gracefully
#
# Next step: Create the application layer use cases that will use this value object!
