"""
Value Object Tests - Validating immutable domain concepts.

Value objects represent concepts in the domain that are defined by their attributes
rather than their identity. They are immutable and can be freely shared since they
have no identity. These tests ensure proper value object behavior, immutability,
and validation.

Educational Notes:
- Value objects are defined by their attributes, not identity
- They are immutable after creation
- Equality is based on all attribute values
- Can be freely shared and cached since they're immutable

Design Patterns:
- Value Object Pattern: Immutable objects defined by attributes
- Flyweight Pattern: Can be shared safely due to immutability

Testing Focus:
1. Immutability after creation
2. Equality based on all attributes
3. Hash consistency for use in collections
4. Validation of attribute values
5. Proper construction and factory methods

SOLID Principles Demonstrated:
- Single Responsibility: Each value object has one reason to change
- Open/Closed: Extensible through composition, not modification
- Liskov Substitution: Value objects of same type are interchangeable
- Interface Segregation: Focused, cohesive interfaces
- Dependency Inversion: No dependencies on concrete implementations

Common Value Object Characteristics:
- Immutable after creation
- Equality based on all attributes
- Implements __hash__ for use in sets/dicts
- Comprehensive validation in constructor
- No identity - replaceable with equivalent instances
"""
