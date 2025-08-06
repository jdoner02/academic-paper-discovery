# Domain Value Objects Package

"""
Domain Value Objects - Immutable Objects Without Identity.

Value Objects are immutable objects that:
- Have no identity - equality is based on all attributes
- Cannot be changed after creation (immutability)
- Can be freely shared and copied
- Represent concepts rather than things

Educational Notes:
Value Objects capture domain concepts that are defined by their
characteristics rather than their identity. In research paper analysis,
concepts like embedding vectors, evidence sentences, and concept
hierarchies are values - they matter because of what they contain,
not who they are.

Key Design Principles:
- Immutability: Cannot be changed after creation
- Value Equality: Two objects with same attributes are identical
- Self-Validation: Ensure validity on construction
- Side-Effect Free Functions: Operations return new objects
- Expressiveness: Make domain concepts explicit in code

Common Patterns:
- Factory methods for complex construction
- Validation in constructors with clear error messages
- Fluent APIs for composing operations
- Null Object pattern for representing absence
- Comparison operations based on all attributes

Real-World Application:
An embedding vector represents semantic meaning - two vectors with
identical values are interchangeable. Evidence sentences capture
textual support for concepts - the text content defines the value,
not any notion of identity.
"""

# Import all value object classes for convenient access
# These will be created in TDD Cycle 1
