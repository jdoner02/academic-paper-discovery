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
- KeywordConfig: Configuration for research paper keyword searches
- PaperFingerprint: Identity mechanism for duplicate paper detection across sources
- SourceMetadata: Multi-source paper metadata tracking and quality assessment
- QualityScore: Represents data quality metrics
- Citation: Represents a bibliographic citation
- DateRange: Represents a time period
"""

from .keyword_config import KeywordConfig
from .search_query import SearchQuery
from .paper_fingerprint import PaperFingerprint
from .source_metadata import SourceMetadata

__all__ = [
    "KeywordConfig",
    "SearchQuery",
    "PaperFingerprint",
    "SourceMetadata",
]
