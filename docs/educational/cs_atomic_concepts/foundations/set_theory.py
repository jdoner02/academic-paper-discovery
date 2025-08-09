"""
Atomic Concept: Set Theory - Mathematical Foundation of Computer Science

This module implements set theory from first principles, demonstrating the mathematical
foundation underlying all computer science data structures and algorithms.

Educational Philosophy:
    "Every data structure is fundamentally a set with additional constraints and operations."

Learning Objectives:
    ✓ Understand sets as unordered collections of distinct elements
    ✓ Implement set operations (union, intersection, difference, etc.)
    ✓ Recognize how sets relate to arrays, hash tables, and databases
    ✓ Apply set theory to algorithm analysis and formal verification

Real-World Applications:
    • Database operations (SQL SELECT with WHERE clauses)
    • Search engines (query result intersections)
    • Access control systems (permission sets)
    • Social networks (friend recommendation algorithms)
    • Data deduplication and uniqueness constraints

Mathematical Definition:
    A set S is a well-defined collection of distinct objects called elements.
    For any object x and set S, either x ∈ S (x is in S) or x ∉ S (x is not in S).

    Axioms (ZFC Set Theory simplified for CS):
    1. Extensionality: Sets are equal iff they have the same elements
    2. Empty Set: ∅ exists and contains no elements
    3. Pairing: For any a,b there exists a set {a,b}
    4. Union: For any sets A,B there exists A ∪ B
    5. Power Set: For any set A there exists P(A) = {X : X ⊆ A}

Prerequisites:
    None - this is a foundational concept

Performance Characteristics:
    Operation     | This Implementation | Optimized (hash table)
    --------------|---------------------|---------------------
    Membership    | O(n)               | O(1) average
    Union         | O(n + m)           | O(n + m)
    Intersection  | O(n * m)           | O(min(n,m))
    Difference    | O(n * m)           | O(n)

    Note: This implementation prioritizes clarity over performance.
    Production systems use hash tables for O(1) average-case membership testing.

Common Misconceptions:
    ❌ "Sets are just arrays without duplicates"
    ✅ Sets are mathematical objects; arrays are implementation details

    ❌ "Set order matters in programming"
    ✅ Mathematical sets are unordered; some implementations maintain insertion order

    ❌ "Sets can contain anything"
    ✅ Elements must be immutable/hashable in most programming implementations

Author: Jessica Doner
Course: CSCD 210 - Data Structures
Complexity: Foundational (accessible to high school students with basic Python)
"""

from typing import Any, Iterator, List, Set as PythonSet, Union, Optional, Callable
from abc import ABC, abstractmethod
import copy

# Type alias for cleaner signatures
Element = Any
SetLike = Union["FiniteSet", List[Element], PythonSet[Element]]


class SetTheoryException(Exception):
    """Custom exception for set theory violations."""

    pass


class FiniteSet:
    """
    Mathematical set implementation demonstrating core set theory concepts.

    This class prioritizes educational clarity over performance optimization.
    It implements mathematical set operations from first principles.

    Design Principles:
        • Immutable after creation (like mathematical sets)
        • Clear method names matching mathematical notation
        • Extensive validation and error messaging for learning
        • Support for both educational and practical use cases

    Examples:
        >>> # Basic set creation and membership
        >>> A = FiniteSet([1, 2, 3, 3, 2])  # Duplicates automatically removed
        >>> print(A)  # {1, 2, 3}
        >>> print(2 in A)  # True
        >>> print(4 in A)  # False

        >>> # Set operations
        >>> B = FiniteSet([3, 4, 5])
        >>> print(A.union(B))        # {1, 2, 3, 4, 5}
        >>> print(A.intersection(B)) # {3}
        >>> print(A.difference(B))   # {1, 2}

        >>> # Mathematical properties
        >>> print(A.is_subset_of(A.union(B)))  # True
        >>> print(A.union(B) == B.union(A))    # True (commutative)
    """

    def __init__(self, elements: Optional[List[Element]] = None):
        """
        Create a finite set from a list of elements.

        Args:
            elements: List of elements to include. Duplicates are automatically removed.
                     If None, creates empty set.

        Mathematical Property:
            Implements the Axiom of Extensionality - sets are defined by their elements.

        Examples:
            >>> empty_set = FiniteSet()
            >>> number_set = FiniteSet([1, 2, 3, 3, 2])  # Becomes {1, 2, 3}
            >>> mixed_set = FiniteSet(['a', 1, 'b', 2])
        """
        if elements is None:
            self._elements = []
        else:
            # Validate that all elements are hashable for mathematical rigor
            self._validate_hashable_elements(elements)

            # Remove duplicates while preserving some insertion order for display
            seen = set()
            unique_elements = []
            for element in elements:
                if element not in seen:
                    unique_elements.append(element)
                    seen.add(element)
            self._elements = unique_elements

    def _validate_hashable_elements(self, elements: List[Element]) -> None:
        """
        Validate that all elements are hashable.

        Mathematical Reasoning:
            Set elements must be immutable and hashable to maintain
            mathematical properties like equality testing and membership.

        Args:
            elements: List of elements to validate

        Raises:
            SetTheoryException: If any element is unhashable
        """
        for element in elements:
            try:
                hash(element)
            except TypeError as e:
                raise SetTheoryException(
                    f"Set elements must be hashable (immutable). "
                    f"Element {element} of type {type(element)} is not hashable. "
                    f"Use immutable types like numbers, strings, tuples, or frozensets. "
                    f"Original error: {str(e)}"
                )

    def __contains__(self, element: Element) -> bool:
        """
        Test set membership: element ∈ self

        Args:
            element: Element to test for membership

        Returns:
            True if element is in the set, False otherwise

        Mathematical Property:
            For every set S and element x: either x ∈ S or x ∉ S (Law of Excluded Middle)

        Time Complexity: O(n) where n is the size of the set
        """
        return element in self._elements

    def __eq__(self, other: "FiniteSet") -> bool:
        """
        Test set equality: self = other

        Args:
            other: Another FiniteSet to compare with

        Returns:
            True if sets contain exactly the same elements

        Mathematical Property:
            Axiom of Extensionality: A = B iff ∀x(x ∈ A ↔ x ∈ B)

        Examples:
            >>> FiniteSet([1, 2, 3]) == FiniteSet([3, 2, 1])  # True
            >>> FiniteSet([1, 2]) == FiniteSet([1, 2, 3])     # False
        """
        if not isinstance(other, FiniteSet):
            return False

        # Two sets are equal iff they have the same elements
        return set(self._elements) == set(other._elements)

    def __hash__(self) -> int:
        """
        Make sets hashable so they can be elements of other sets.

        Returns:
            Hash value based on frozenset of elements

        Mathematical Property:
            Enables construction of sets of sets, power sets, etc.
        """
        try:
            return hash(frozenset(self._elements))
        except TypeError:
            # Some elements might not be hashable
            raise SetTheoryException(
                "Set contains unhashable elements and cannot be hashed. "
                "Consider using only immutable elements like numbers, strings, or tuples."
            )

    def __len__(self) -> int:
        """
        Return cardinality (size) of the set: |S|

        Returns:
            Number of elements in the set

        Mathematical Property:
            Cardinality is well-defined for finite sets
        """
        return len(self._elements)

    def __iter__(self) -> Iterator[Element]:
        """
        Make set iterable for use in loops and comprehensions.

        Yields:
            Each element in the set (order not mathematically meaningful)
        """
        return iter(self._elements)

    def __str__(self) -> str:
        """
        String representation using mathematical set notation.

        Returns:
            String in format {element1, element2, ...} or ∅ for empty set
        """
        if not self._elements:
            return "∅"  # Empty set symbol

        elements_str = ", ".join(str(element) for element in self._elements)
        return f"{{{elements_str}}}"

    def __repr__(self) -> str:
        """
        Programmer-friendly representation showing constructor call.

        Returns:
            String that could recreate this object
        """
        return f"FiniteSet({self._elements})"

    # Core Set Operations

    def union(self, other: SetLike) -> "FiniteSet":
        """
        Set union: self ∪ other

        Args:
            other: Another set-like object

        Returns:
            New set containing all elements from both sets

        Mathematical Properties:
            • Commutative: A ∪ B = B ∪ A
            • Associative: (A ∪ B) ∪ C = A ∪ (B ∪ C)
            • Identity: A ∪ ∅ = A
            • Idempotent: A ∪ A = A

        Examples:
            >>> A = FiniteSet([1, 2, 3])
            >>> B = FiniteSet([3, 4, 5])
            >>> print(A.union(B))  # {1, 2, 3, 4, 5}
        """
        other_set = self._normalize_to_set(other)

        # Mathematical definition: x ∈ (A ∪ B) iff (x ∈ A) ∨ (x ∈ B)
        union_elements = list(self._elements)
        for element in other_set:
            if element not in self._elements:
                union_elements.append(element)

        return FiniteSet(union_elements)

    def intersection(self, other: SetLike) -> "FiniteSet":
        """
        Set intersection: self ∩ other

        Args:
            other: Another set-like object

        Returns:
            New set containing elements present in both sets

        Mathematical Properties:
            • Commutative: A ∩ B = B ∩ A
            • Associative: (A ∩ B) ∩ C = A ∩ (B ∩ C)
            • Identity: A ∩ U = A (where U is universal set)
            • Null: A ∩ ∅ = ∅

        Examples:
            >>> A = FiniteSet([1, 2, 3])
            >>> B = FiniteSet([3, 4, 5])
            >>> print(A.intersection(B))  # {3}
        """
        other_set = self._normalize_to_set(other)

        # Mathematical definition: x ∈ (A ∩ B) iff (x ∈ A) ∧ (x ∈ B)
        intersection_elements = []
        for element in self._elements:
            if element in other_set:
                intersection_elements.append(element)

        return FiniteSet(intersection_elements)

    def difference(self, other: SetLike) -> "FiniteSet":
        """
        Set difference (relative complement): self - other or self \\ other

        Args:
            other: Another set-like object

        Returns:
            New set containing elements in self but not in other

        Mathematical Properties:
            • Non-commutative: A - B ≠ B - A (generally)
            • A - A = ∅
            • A - ∅ = A
            • ∅ - A = ∅

        Examples:
            >>> A = FiniteSet([1, 2, 3])
            >>> B = FiniteSet([3, 4, 5])
            >>> print(A.difference(B))  # {1, 2}
            >>> print(B.difference(A))  # {4, 5}
        """
        other_set = self._normalize_to_set(other)

        # Mathematical definition: x ∈ (A - B) iff (x ∈ A) ∧ (x ∉ B)
        difference_elements = []
        for element in self._elements:
            if element not in other_set:
                difference_elements.append(element)

        return FiniteSet(difference_elements)

    def symmetric_difference(self, other: SetLike) -> "FiniteSet":
        """
        Symmetric difference: self ⊕ other = (self - other) ∪ (other - self)

        Args:
            other: Another set-like object

        Returns:
            New set containing elements in either set but not in both

        Mathematical Properties:
            • Commutative: A ⊕ B = B ⊕ A
            • Associative: (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)
            • Identity: A ⊕ ∅ = A
            • Self-inverse: A ⊕ A = ∅

        Examples:
            >>> A = FiniteSet([1, 2, 3])
            >>> B = FiniteSet([3, 4, 5])
            >>> print(A.symmetric_difference(B))  # {1, 2, 4, 5}
        """
        other_set = self._normalize_to_set(other)

        # Mathematical definition: x ∈ (A ⊕ B) iff (x ∈ A) ⊕ (x ∈ B)
        # Where ⊕ is exclusive or (XOR)
        return self.difference(other_set).union(other_set.difference(self))

    # Set Relationship Tests

    def is_subset_of(self, other: SetLike) -> bool:
        """
        Test subset relationship: self ⊆ other

        Args:
            other: Another set-like object

        Returns:
            True if all elements of self are also in other

        Mathematical Property:
            A ⊆ B iff ∀x(x ∈ A → x ∈ B)

        Examples:
            >>> A = FiniteSet([1, 2])
            >>> B = FiniteSet([1, 2, 3])
            >>> print(A.is_subset_of(B))  # True
            >>> print(B.is_subset_of(A))  # False
        """
        other_set = self._normalize_to_set(other)

        # Every element of self must be in other
        for element in self._elements:
            if element not in other_set:
                return False
        return True

    def is_proper_subset_of(self, other: SetLike) -> bool:
        """
        Test proper subset relationship: self ⊂ other

        Args:
            other: Another set-like object

        Returns:
            True if self is a subset of other and self ≠ other

        Mathematical Property:
            A ⊂ B iff (A ⊆ B) ∧ (A ≠ B)
        """
        other_set = self._normalize_to_set(other)
        return self.is_subset_of(other_set) and self != other_set

    def is_superset_of(self, other: SetLike) -> bool:
        """
        Test superset relationship: self ⊇ other

        Args:
            other: Another set-like object

        Returns:
            True if all elements of other are also in self

        Mathematical Property:
            A ⊇ B iff B ⊆ A
        """
        other_set = self._normalize_to_set(other)
        return other_set.is_subset_of(self)

    def is_disjoint_from(self, other: SetLike) -> bool:
        """
        Test if sets are disjoint (have no elements in common).

        Args:
            other: Another set-like object

        Returns:
            True if sets have no common elements

        Mathematical Property:
            A and B are disjoint iff A ∩ B = ∅

        Examples:
            >>> A = FiniteSet([1, 2, 3])
            >>> B = FiniteSet([4, 5, 6])
            >>> print(A.is_disjoint_from(B))  # True
        """
        return len(self.intersection(other)) == 0

    # Advanced Operations

    def cardinality(self) -> int:
        """
        Return the cardinality (number of elements) of the set.

        Returns:
            Integer representing |self|

        Mathematical Property:
            For finite sets, cardinality is simply the count of elements.
            This extends to infinite sets using different mathematics.
        """
        return len(self)

    def power_set(self) -> "FiniteSet":
        """
        Generate the power set: P(self) = {X : X ⊆ self}

        Returns:
            Set of all subsets of this set

        Mathematical Properties:
            • |P(A)| = 2^|A| for finite sets
            • ∅ ∈ P(A) for any set A
            • A ∈ P(A) for any set A

        Examples:
            >>> A = FiniteSet([1, 2])
            >>> P_A = A.power_set()
            >>> print(P_A)  # {∅, {1}, {2}, {1,2}}

        Warning:
            Power set size grows exponentially! Use only with small sets.
        """
        if len(self) > 10:
            raise SetTheoryException(
                f"Power set of size {len(self)} would have {2**len(self)} elements. "
                "This is too large for educational demonstration. Use sets with ≤10 elements."
            )

        subsets = []
        elements = list(self._elements)

        # Generate all 2^n subsets using binary representation
        for i in range(2 ** len(elements)):
            subset_elements = []
            for j in range(len(elements)):
                if i & (1 << j):  # Check if j-th bit is set
                    subset_elements.append(elements[j])
            subsets.append(FiniteSet(subset_elements))

        return FiniteSet(subsets)

    def cartesian_product(self, other: SetLike) -> "FiniteSet":
        """
        Cartesian product: self × other = {(a,b) : a ∈ self, b ∈ other}

        Args:
            other: Another set-like object

        Returns:
            Set of all ordered pairs (a,b) where a ∈ self and b ∈ other

        Mathematical Properties:
            • |A × B| = |A| × |B|
            • A × B ≠ B × A (generally)
            • A × ∅ = ∅ × A = ∅

        Examples:
            >>> A = FiniteSet([1, 2])
            >>> B = FiniteSet(['a', 'b'])
            >>> print(A.cartesian_product(B))  # {(1,'a'), (1,'b'), (2,'a'), (2,'b')}
        """
        other_set = self._normalize_to_set(other)

        if len(self) * len(other_set) > 100:
            raise SetTheoryException(
                f"Cartesian product would have {len(self) * len(other_set)} elements. "
                "This is too large for educational demonstration. Use smaller sets."
            )

        product_elements = []
        for a in self._elements:
            for b in other_set:
                product_elements.append((a, b))

        return FiniteSet(product_elements)

    # Utility Methods

    def add_element(self, element: Element) -> "FiniteSet":
        """
        Return new set with element added (sets are immutable).

        Args:
            element: Element to add to the set

        Returns:
            New FiniteSet containing all original elements plus the new element

        Note:
            This returns a new set rather than modifying the existing one,
            following the mathematical principle that sets are immutable objects.
        """
        if element in self._elements:
            return FiniteSet(self._elements)  # No change needed
        else:
            return FiniteSet(self._elements + [element])

    def remove_element(self, element: Element) -> "FiniteSet":
        """
        Return new set with element removed (sets are immutable).

        Args:
            element: Element to remove from the set

        Returns:
            New FiniteSet containing all original elements except the specified one

        Raises:
            SetTheoryException: If element is not in the set
        """
        if element not in self._elements:
            raise SetTheoryException(f"Element {element} is not in the set {self}")

        new_elements = [e for e in self._elements if e != element]
        return FiniteSet(new_elements)

    def to_list(self) -> List[Element]:
        """
        Convert set to list (for interfacing with other code).

        Returns:
            List containing all elements (order not guaranteed)

        Warning:
            Converting to list loses the mathematical properties of sets.
            Use only when necessary for interfacing with non-set-aware code.
        """
        return list(self._elements)

    def to_python_set(self) -> PythonSet[Element]:
        """
        Convert to Python's built-in set type.

        Returns:
            Python set containing the same elements

        Note:
            Python's set is optimized for performance but less educational.
            Use this for production code after understanding the concepts.
        """
        return set(self._elements)

    def _normalize_to_set(self, other: SetLike) -> "FiniteSet":
        """
        Convert various set-like objects to FiniteSet for operations.

        Args:
            other: Set-like object (FiniteSet, list, or Python set)

        Returns:
            FiniteSet equivalent of the input

        Raises:
            SetTheoryException: If input cannot be converted to a set
        """
        if isinstance(other, FiniteSet):
            return other
        elif isinstance(other, (list, set)):
            return FiniteSet(list(other))
        else:
            raise SetTheoryException(
                f"Cannot perform set operation with object of type {type(other)}. "
                "Expected FiniteSet, list, or set."
            )


# Factory Functions for Common Sets


def empty_set() -> FiniteSet:
    """
    Create the empty set ∅.

    Returns:
        Empty FiniteSet

    Mathematical Property:
        The empty set is unique and is a subset of every set.

    Examples:
        >>> empty = empty_set()
        >>> A = FiniteSet([1, 2, 3])
        >>> print(empty.is_subset_of(A))  # True
        >>> print(A.union(empty) == A)   # True
    """
    return FiniteSet([])


def universal_set(elements: List[Element]) -> FiniteSet:
    """
    Create a universal set for a given context.

    Args:
        elements: All possible elements in this context

    Returns:
        FiniteSet containing all specified elements

    Note:
        In formal set theory, there is no universal set (Russell's Paradox).
        This function creates a "universal set" for a specific finite context.

    Examples:
        >>> digits = universal_set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> odds = FiniteSet([1, 3, 5, 7, 9])
        >>> evens = digits.difference(odds)
        >>> print(evens)  # {0, 2, 4, 6, 8}
    """
    return FiniteSet(elements)


def singleton_set(element: Element) -> FiniteSet:
    """
    Create a singleton set {element}.

    Args:
        element: The single element to include

    Returns:
        FiniteSet containing only the specified element

    Mathematical Property:
        For any element a, the singleton set {a} exists (Axiom of Pairing).

    Examples:
        >>> single = singleton_set(42)
        >>> print(single)  # {42}
        >>> print(42 in single)  # True
        >>> print(len(single))   # 1
    """
    return FiniteSet([element])


# Educational Demonstrations


def demonstrate_set_properties():
    """
    Demonstrate key mathematical properties of sets with examples.

    This function provides a comprehensive educational demonstration
    showing how set operations follow mathematical laws.
    """
    print("Set Theory Educational Demonstration")
    print("=" * 40)

    # Create example sets
    A = FiniteSet([1, 2, 3])
    B = FiniteSet([3, 4, 5])
    C = FiniteSet([5, 6, 7])
    empty = empty_set()

    print(f"A = {A}")
    print(f"B = {B}")
    print(f"C = {C}")
    print(f"∅ = {empty}")
    print()

    # Demonstrate commutative laws
    print("Commutative Laws:")
    print(f"A ∪ B = {A.union(B)}")
    print(f"B ∪ A = {B.union(A)}")
    print(f"Equal? {A.union(B) == B.union(A)}")
    print()

    print(f"A ∩ B = {A.intersection(B)}")
    print(f"B ∩ A = {B.intersection(A)}")
    print(f"Equal? {A.intersection(B) == B.intersection(A)}")
    print()

    # Demonstrate associative laws
    print("Associative Laws:")
    left_union = A.union(B).union(C)
    right_union = A.union(B.union(C))
    print(f"(A ∪ B) ∪ C = {left_union}")
    print(f"A ∪ (B ∪ C) = {right_union}")
    print(f"Equal? {left_union == right_union}")
    print()

    # Demonstrate identity laws
    print("Identity Laws:")
    print(f"A ∪ ∅ = {A.union(empty)}")
    print(f"Equal to A? {A.union(empty) == A}")
    print()

    # Demonstrate subset relationships
    print("Subset Relationships:")
    subset = FiniteSet([1, 2])
    print(f"Let S = {subset}")
    print(f"S ⊆ A? {subset.is_subset_of(A)}")
    print(f"A ⊆ S? {A.is_subset_of(subset)}")
    print(f"S ⊂ A? {subset.is_proper_subset_of(A)}")
    print()

    # Demonstrate De Morgan's laws
    print("De Morgan's Laws:")
    universal = FiniteSet([1, 2, 3, 4, 5, 6, 7])
    complement_a = universal.difference(A)
    complement_b = universal.difference(B)

    # ¬(A ∪ B) = ¬A ∩ ¬B
    left_demorgan = universal.difference(A.union(B))
    right_demorgan = complement_a.intersection(complement_b)
    print(f"Universal set U = {universal}")
    print(f"¬A = {complement_a}")
    print(f"¬B = {complement_b}")
    print(f"¬(A ∪ B) = {left_demorgan}")
    print(f"¬A ∩ ¬B = {right_demorgan}")
    print(f"De Morgan's Law holds? {left_demorgan == right_demorgan}")


# Module-level constants for educational reference
PREREQUISITES = []  # This is a foundational concept

# Educational metadata
LEARNING_OBJECTIVES = [
    "Understand mathematical definition of sets",
    "Implement core set operations from first principles",
    "Recognize set theory as foundation for data structures",
    "Apply set operations to solve computational problems",
]

# Complexity constants to avoid duplication
O_N_M_COMPLEXITY = "O(n * m)"

BIG_O_COMPLEXITY = {
    "membership_test": "O(n)",
    "union": "O(n + m)",
    "intersection": O_N_M_COMPLEXITY,
    "difference": O_N_M_COMPLEXITY,
    "subset_test": O_N_M_COMPLEXITY,
}

COMMON_APPLICATIONS = [
    "Database query optimization",
    "Search engine result filtering",
    "Access control and permissions",
    "Data deduplication",
    "Mathematical proof verification",
]

if __name__ == "__main__":
    # Run educational demonstration
    demonstrate_set_properties()

    print("\n" + "=" * 40)
    print("Interactive Examples:")
    print("Try creating your own sets and experimenting with operations!")
    print("  from cs_atomic_concepts.foundations.set_theory import FiniteSet")
    print("  A = FiniteSet([1, 2, 3])")
    print("  B = FiniteSet([3, 4, 5])")
    print("  print(A.union(B))")
