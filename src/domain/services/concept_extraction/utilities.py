"""
Common Utilities for Concept Extraction

Educational Notes:
- Contains shared constants and utility functions
- Demonstrates separation of cross-cutting concerns
- Shows proper utility module organization
"""

import re
import logging
from typing import Any, Callable
from functools import wraps

# COMMON CONSTANTS FOR TEXT PROCESSING
# =============================================================================

# Regular expression patterns for consistent text processing
WORD_EXTRACTION_PATTERN = r"\b[a-zA-Z]{3,}\b"
SENTENCE_SPLIT_PATTERN = r"[.!?]+"


# =============================================================================
# COMMON HELPER METHODS FOR EXTRACTION STRATEGIES
# =============================================================================


def _safe_extraction(extraction_method_name: str):
    """
    Decorator for safe concept extraction with consistent error handling.

    Educational Note:
    This decorator demonstrates the Decorator Pattern applied to error handling,
    providing consistent logging and graceful degradation across all extraction
    strategies while maintaining the Strategy Pattern's interface.
    """

    def decorator(extraction_func):
        def wrapper(self, *args, **kwargs):
            try:
                return extraction_func(self, *args, **kwargs)
            except Exception as e:
                logging.warning(f"{extraction_method_name} extraction failed: {e}")
                return (
                    []
                    if extraction_func.__name__.startswith("extract_")
                    else ExtractionResult(concepts=[], metadata={})
                )

        return wrapper

    return decorator


# Educational Note: Value objects for extraction configuration and results
@dataclass(frozen=True)

