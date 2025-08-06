"""
SearchQuery value object for the HRV research aggregation domain.

This module defines the SearchQuery value object, which encapsulates all the
parameters needed to search for research papers. As a value object, it is
immutable and provides validation for search parameters.

Educational Notes:
- Value objects represent concepts without identity (unlike entities)
- They encapsulate validation logic and business rules
- Immutability makes them safe to pass around the system
- Equality is based on all attributes, not object identity
- They can contain behavior related to their data

Domain Context:
In HRV research, search queries often involve:
- Multiple search terms (keywords, phrases)
- Date ranges for publication filtering
- Quality thresholds (minimum citations)
- Result limitations for performance

Architectural Pattern:
This follows the Value Object pattern from Domain-Driven Design,
where complex data is encapsulated with its validation rules.
"""

from datetime import datetime
from typing import List, Optional, Tuple


class SearchQuery:
    """
    Value object representing search parameters for research papers.

    This encapsulates all the criteria used to find relevant HRV research
    papers, including search terms, date constraints, and quality filters.

    Educational Notes:
    - Implemented manually (not dataclass) for better control over hashability
    - All attributes are made private and accessed via properties
    - Validation happens in constructor to ensure invariants
    - Methods are pure functions (no side effects)

    Attributes:
        terms: Tuple of search terms/keywords to match (immutable and hashable)
        start_date: Optional earliest publication date to include
        end_date: Optional latest publication date to include
        max_results: Maximum number of results to return (default: 100)
        min_citations: Minimum citation count filter (default: 0)

    Business Rules:
    1. Must have at least one search term
    2. Date range must be logically consistent
    3. Result limits must be positive
    4. Citation minimums cannot be negative
    """

    def __init__(
        self,
        terms: List[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_results: int = 100,
        min_citations: int = 0,
    ) -> None:
        """
        Initialize a SearchQuery with validation.

        Educational Note:
        Manual implementation allows us to convert list to tuple for
        hashability while maintaining a convenient interface.

        Args:
            terms: List of search terms (converted to tuple internally)
            start_date: Optional earliest publication date
            end_date: Optional latest publication date
            max_results: Maximum results to return
            min_citations: Minimum citation threshold

        Raises:
            ValueError: If any business rules are violated
        """
        # Convert list to tuple for immutability and hashability
        self._terms = tuple(terms) if terms else tuple()
        self._start_date = start_date
        self._end_date = end_date
        self._max_results = max_results
        self._min_citations = min_citations

        # Validate after initialization
        self._validate()

    def _validate(self) -> None:
        """
        Validate the SearchQuery business rules.

        Educational Note:
        Private method to keep validation logic centralized.
        Called only during initialization since object is immutable.

        Raises:
            ValueError: If any business rules are violated
        """
        # Business Rule 1: Must have at least one search term
        if not self._terms:
            raise ValueError("SearchQuery must have at least one search term")

        # Business Rule 2: Date range validation
        if (
            self._start_date is not None
            and self._end_date is not None
            and self._start_date > self._end_date
        ):
            raise ValueError("start_date cannot be after end_date")

        # Business Rule 3: Result limits must be positive
        if self._max_results <= 0:
            raise ValueError("max_results must be positive")

        # Business Rule 4: Citation minimums cannot be negative
        if self._min_citations < 0:
            raise ValueError("min_citations cannot be negative")

    # Properties for immutable access
    @property
    def terms(self) -> Tuple[str, ...]:
        """Get the search terms as an immutable tuple."""
        return self._terms

    @property
    def start_date(self) -> Optional[datetime]:
        """Get the start date constraint."""
        return self._start_date

    @property
    def end_date(self) -> Optional[datetime]:
        """Get the end date constraint."""
        return self._end_date

    @property
    def max_results(self) -> int:
        """Get the maximum results limit."""
        return self._max_results

    @property
    def min_citations(self) -> int:
        """Get the minimum citations threshold."""
        return self._min_citations

    def __eq__(self, other) -> bool:
        """
        Check equality based on all attributes.

        Educational Note:
        Value objects are equal if all their attributes are equal.
        This is different from entity equality which is based on identity.
        """
        if not isinstance(other, SearchQuery):
            return False

        return (
            self._terms == other._terms
            and self._start_date == other._start_date
            and self._end_date == other._end_date
            and self._max_results == other._max_results
            and self._min_citations == other._min_citations
        )

    def __hash__(self) -> int:
        """
        Generate hash based on all attributes.

        Educational Note:
        Objects that are equal must have the same hash value.
        Using a tuple of all attributes ensures this property.
        """
        return hash(
            (
                self._terms,
                self._start_date,
                self._end_date,
                self._max_results,
                self._min_citations,
            )
        )

    def has_date_range(self) -> bool:
        """
        Check if this query includes date range constraints.

        This is useful for optimizing search strategies - queries with
        date constraints might use different search approaches.

        Returns:
            bool: True if both start_date and end_date are specified

        Educational Note:
        This is a query method - it asks questions about the object's state
        without modifying it. Pure functions like this are safe to call
        multiple times and have no side effects.
        """
        return self.start_date is not None and self.end_date is not None

    def to_query_string(self, separator: str = " AND ") -> str:
        """
        Convert search terms to a formatted query string.

        This method allows different search adapters to format the query
        according to their specific requirements (e.g., PubMed, Google Scholar).

        Args:
            separator: String to join multiple terms (default: " AND ")

        Returns:
            str: Formatted query string combining all search terms

        Educational Note:
        This is a conversion method that transforms the value object's
        data into a different representation. The method is pure - it
        doesn't modify the object and always returns the same result
        for the same input.
        """
        # Wrap terms with spaces in quotes for exact phrase matching
        formatted_terms = []
        for term in self.terms:
            if " " in term:
                formatted_terms.append(f'"{term}"')
            else:
                formatted_terms.append(term)

        return separator.join(formatted_terms)

    def is_within_date_range(self, publication_date: datetime) -> bool:
        """
        Check if a publication date falls within this query's date range.

        This method is used to filter search results based on publication
        date constraints. If no date constraints are specified, all dates
        are considered valid.

        Args:
            publication_date: The publication date to check

        Returns:
            bool: True if the date is within range (or no range specified)

        Educational Note:
        This demonstrates how value objects can encapsulate business logic
        related to their data. The logic for "is this date valid for this
        query" belongs with the query itself, not scattered throughout
        the application.
        """
        # No date constraints = always valid
        if not self.has_date_range():
            # Check individual constraints if only one is specified
            if self.start_date is not None and publication_date < self.start_date:
                return False
            if self.end_date is not None and publication_date > self.end_date:
                return False
            return True

        # Both constraints specified - check range
        return self.start_date <= publication_date <= self.end_date

    def matches_citation_threshold(self, citation_count: int) -> bool:
        """
        Check if a paper's citation count meets this query's minimum threshold.

        Args:
            citation_count: Number of citations the paper has received

        Returns:
            bool: True if citation count meets or exceeds minimum
        """
        return citation_count >= self.min_citations

    def __str__(self) -> str:
        """
        Provide a human-readable string representation.

        Educational Note:
        Good string representations help with debugging and logging.
        They should include the most important identifying information.
        """
        terms_str = ", ".join(self.terms)
        parts = [f"terms=[{terms_str}]"]

        if self.has_date_range():
            parts.append(f"dates={self.start_date.date()} to {self.end_date.date()}")
        elif self.start_date:
            parts.append(f"after={self.start_date.date()}")
        elif self.end_date:
            parts.append(f"before={self.end_date.date()}")

        if self.max_results != 100:  # Only show if not default
            parts.append(f"max_results={self.max_results}")

        if self.min_citations > 0:  # Only show if filtering is active
            parts.append(f"min_citations={self.min_citations}")

        return f"SearchQuery({', '.join(parts)})"


# Educational Notes for Students:
#
# 1. Value Object Characteristics:
#    - Immutable (frozen=True)
#    - Equality based on values, not identity
#    - Contains both data and behavior
#    - Encapsulates validation rules
#
# 2. Business Logic Placement:
#    - Date range validation belongs in the SearchQuery
#    - Query formatting logic belongs here too
#    - This keeps business rules close to the data they govern
#
# 3. Design Patterns Used:
#    - Value Object (DDD pattern)
#    - Validation in constructor (__post_init__)
#    - Query methods (has_date_range, is_within_date_range)
#    - Conversion methods (to_query_string)
#
# 4. Why This Design:
#    - Prevents invalid queries from being created
#    - Makes search logic testable and reusable
#    - Encapsulates complexity of search parameter handling
#    - Provides a stable interface for different search adapters
#
# 5. Testing Strategy:
#    - Test all validation rules
#    - Test all business logic methods
#    - Test equality and immutability
#    - Test edge cases and error conditions
