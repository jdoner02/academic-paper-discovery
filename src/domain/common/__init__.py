"""
Domain Common Utilities - Shared domain logic and validation patterns.

This module contains shared utilities used across multiple domain components,
demonstrating the DRY (Don't Repeat Yourself) principle while maintaining
clean separation of concerns.

Educational Notes - Common Module Pattern:
- Centralizes shared validation logic to prevent code duplication
- Provides consistent error messages and validation standards
- Maintains domain independence by containing only pure domain logic
- Enables easy testing and modification of shared behaviors

Design Principles Applied:
- Single Responsibility: Each validator has one clear purpose
- Open/Closed: Validators can be extended without modification
- DRY: Eliminates code duplication across value objects
- Consistency: Standardized error messages and validation logic
"""
