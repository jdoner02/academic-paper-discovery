"""
Entity Tests - Validating objects with identity and lifecycle.

Entities are domain objects that have a unique identity that persists throughout
their lifecycle. Unlike value objects, entities are defined by their identity
rather than their attributes. These tests ensure proper entity behavior,
identity management, and business rule enforcement.

Educational Notes:
- Entities have unique identities (usually an ID or natural key)
- Identity persists even when other attributes change
- Entities can be mutable and have behavior
- Equality is based on identity, not attribute values

Design Patterns:
- Identity Field Pattern: Entities use unique identifiers
- Domain Model Pattern: Rich objects with behavior, not just data

Testing Focus:
1. Identity comparison and equality
2. Business rule validation
3. State changes and behavior
4. Invariant maintenance
5. Lifecycle management

Common Entity Characteristics:
- Has unique identifier
- Mutable state allowed
- Behavior methods that enforce business rules
- Equality based on identity
- May aggregate other domain objects
"""
