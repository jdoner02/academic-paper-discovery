"""
Domain value objects package.

This package contains value objects - immutable objects that represent concepts
without identity. Value objects are compared by their values, not their identity.

Educational Notes:
- Value objects have no conceptual identity
- They are immutable once created
- Equality is based on all attributes
- They are safe to share between different contexts
- Often used to encapsulate validation logic
- Should be small and focused on a single concept

Examples of value objects in HRV research:
- SearchQuery: Encapsulates search parameters
- QualityScore: Represents data quality metrics
- Citation: Represents a bibliographic citation
- DateRange: Represents a time period
"""
