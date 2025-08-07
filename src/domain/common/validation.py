"""
Domain Validation Utilities - Common validation patterns for domain objects.

This module provides reusable validation functions that enforce domain
business rules consistently across all domain objects.

Educational Notes - Validation Pattern:
- Centralizes validation logic to ensure consistency
- Provides clear, standardized error messages for domain violations
- Demonstrates separation of validation concerns from business logic
- Enables easy testing and modification of validation rules

Educational Notes - Functional Programming Approach:
- Pure functions with no side effects enable easy testing
- Predictable behavior improves code reliability
- Composable validators can be combined for complex validation
- Clear input/output contracts make behavior explicit

Design Principles Applied:
- Single Responsibility: Each function validates one specific concern
- Open/Closed: New validators can be added without modifying existing ones
- Fail Fast: Invalid data is caught as early as possible
- Clear Error Messages: Help developers understand and fix domain violations
"""

from typing import Any, Union


class DomainValidationError(ValueError):
    """
    Specialized exception for domain validation failures.

    Educational Notes - Custom Exception Pattern:
    - Provides specific exception type for domain validation errors
    - Enables targeted exception handling in application layer
    - Maintains clear separation between domain and technical errors
    - Improves debugging and error tracking in complex systems
    """

    pass


def validate_non_empty_string(value: str, field_name: str) -> None:
    """
    Validate that a string field contains meaningful content.

    Args:
        value: The string value to validate
        field_name: Name of the field for error messages

    Raises:
        DomainValidationError: If the string is empty or whitespace-only

    Educational Notes - Input Validation:
    - Prevents empty or meaningless data from entering domain objects
    - Provides clear feedback about which field failed validation
    - Uses strip() to catch whitespace-only strings that appear valid
    - Consistent error message format across all domain objects
    """
    if not value or not value.strip():
        raise DomainValidationError(f"{field_name} cannot be empty or whitespace-only")


def validate_positive_integer(value: int, field_name: str) -> None:
    """
    Validate that an integer field contains a positive value.

    Args:
        value: The integer value to validate
        field_name: Name of the field for error messages

    Raises:
        DomainValidationError: If the integer is not positive

    Educational Notes - Business Rule Validation:
    - Enforces domain business rules about positive values
    - Common pattern for counts, IDs, and page numbers
    - Clear error message indicates expected valid range
    - Separates validation logic from business object constructors
    """
    if value <= 0:
        raise DomainValidationError(f"{field_name} must be positive (greater than 0)")


def validate_probability_score(value: float, field_name: str) -> None:
    """
    Validate that a float represents a valid probability (0.0 to 1.0).

    Args:
        value: The float value to validate
        field_name: Name of the field for error messages

    Raises:
        DomainValidationError: If the value is not a valid probability

    Educational Notes - Domain-Specific Validation:
    - Enforces mathematical constraints for probability values
    - Common pattern for confidence scores and quality metrics
    - Uses inclusive bounds to allow exactly 0.0 and 1.0
    - Clear mathematical context in error message
    """
    if not (0.0 <= value <= 1.0):
        raise DomainValidationError(
            f"{field_name} must be a valid probability between 0.0 and 1.0 (inclusive)"
        )


def validate_positive_count(
    value: int, field_name: str, allow_zero: bool = False
) -> None:
    """
    Validate that an integer represents a valid count.

    Args:
        value: The integer value to validate
        field_name: Name of the field for error messages
        allow_zero: Whether zero is considered a valid count

    Raises:
        DomainValidationError: If the count is invalid

    Educational Notes - Flexible Validation:
    - Provides configurable validation for different use cases
    - Some counts can be zero (like child concepts), others cannot
    - Clear indication of whether zero is allowed in error message
    - Demonstrates parameter-driven validation behavior
    """
    minimum_value = 0 if allow_zero else 1
    if value < minimum_value:
        bound_description = "non-negative" if allow_zero else "positive"
        raise DomainValidationError(f"{field_name} must be {bound_description}")


def validate_required_field(value: Any, field_name: str) -> None:
    """
    Validate that a required field is not None.

    Args:
        value: The value to validate
        field_name: Name of the field for error messages

    Raises:
        DomainValidationError: If the value is None

    Educational Notes - Null Object Validation:
    - Prevents None values from causing runtime errors
    - Clear indication that field is required for domain object
    - Separates None checking from type-specific validation
    - Essential for maintaining domain object integrity
    """
    if value is None:
        raise DomainValidationError(f"{field_name} is required and cannot be None")


def validate_minimum_length(value: str, minimum: int, field_name: str) -> None:
    """
    Validate that a string meets minimum length requirements.

    Args:
        value: The string to validate
        minimum: Minimum required length
        field_name: Name of the field for error messages

    Raises:
        DomainValidationError: If the string is too short

    Educational Notes - Length Validation:
    - Ensures meaningful content in text fields
    - Prevents single-character or very short values that may be typos
    - Clear indication of minimum requirement in error message
    - Common pattern for descriptions, names, and content fields
    """
    if len(value) < minimum:
        raise DomainValidationError(
            f"{field_name} must be at least {minimum} characters long"
        )


def validate_maximum_length(value: str, maximum: int, field_name: str) -> None:
    """
    Validate that a string doesn't exceed maximum length limits.

    Args:
        value: The string to validate
        maximum: Maximum allowed length
        field_name: Name of the field for error messages

    Raises:
        DomainValidationError: If the string is too long

    Educational Notes - Constraint Validation:
    - Prevents extremely long values that may cause system issues
    - Enforces practical limits for storage and display
    - Clear indication of maximum limit in error message
    - Important for user input fields and external data
    """
    if len(value) > maximum:
        raise DomainValidationError(f"{field_name} cannot exceed {maximum} characters")


def validate_string_format(
    value: str, pattern: str, field_name: str, description: str
) -> None:
    """
    Validate that a string matches a specific format pattern.

    Args:
        value: The string to validate
        pattern: Regular expression pattern to match
        field_name: Name of the field for error messages
        description: Human-readable description of the expected format

    Raises:
        DomainValidationError: If the string doesn't match the pattern

    Educational Notes - Format Validation:
    - Ensures data matches expected patterns (emails, DOIs, etc.)
    - Uses regular expressions for flexible pattern matching
    - Provides human-readable description of expected format
    - Essential for external identifiers and structured data
    """
    import re

    if not re.match(pattern, value):
        raise DomainValidationError(
            f"{field_name} must match the format: {description}"
        )
