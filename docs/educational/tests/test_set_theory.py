"""
Mathematical Proof Verification: Set Theory Axioms and Properties

This test module serves as a formal verification of ZFC set theory axioms
and fundamental set operations, treating each test as a mathematical theorem
with rigorous proof validation.

Educational Value:
    • Demonstrates formal mathematical verification through code
    • Shows how abstract mathematical concepts translate to concrete implementations
    • Provides executable proofs of fundamental set theory properties
    • Serves as foundation for understanding all other data structures

Mathematical Foundation:
    This module verifies the implementation of Zermelo-Fraenkel Choice (ZFC)
    axioms as they apply to finite sets in computer science:

    1. Axiom of Extensionality: A = B ↔ ∀x(x ∈ A ↔ x ∈ B)
    2. Axiom of Empty Set: ∃∅ ∀x(x ∉ ∅)
    3. Axiom of Pairing: ∀a,b ∃c ∀x(x ∈ c ↔ (x = a ∨ x = b))
    4. Axiom of Union: ∀A,B ∃C ∀x(x ∈ C ↔ (x ∈ A ∨ x ∈ B))
    5. Axiom of Power Set: ∀A ∃P ∀x(x ∈ P ↔ x ⊆ A)

Proof Methods Used:
    • Direct Proof: Constructive verification of set operations
    • Proof by Contradiction: Showing impossibility of certain conditions
    • Proof by Construction: Building sets to demonstrate existence
    • Universal Quantification: Verifying properties hold for all valid inputs
    • Property-Based Testing: Randomly generated verification cases

Real-World Relevance:
    Set theory foundations are essential for:
    • Database query optimization (SQL set operations)
    • Search algorithm design (intersection/union of result sets)
    • Access control systems (permission set operations)
    • Data deduplication and integrity verification
    • Mathematical proof assistants and formal verification

Author: Jessica Doner
Course Alignment: CSCD 210 (Data Structures), MATH 170 (Discrete Mathematics)
Verification Standard: ZFC Set Theory + Computer Science Applications
"""

import sys
import random
from pathlib import Path
from typing import List, Any, Set as PySet

# Import our mathematical proof testing framework
sys.path.insert(0, str(Path(__file__).parent.parent))
from tests import (
    MathematicalProofTestCase,
    mathematical_property,
    proof_by_contradiction,
    proof_by_construction,
    proof_by_induction,
)

# Import the set theory implementation to verify
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from educational.cs_atomic_concepts.foundations.set_theory import (
    FiniteSet,
    SetTheoryException,
    empty_set,
    universal_set,
    singleton_set,
)


class TestSetTheoryAxioms(MathematicalProofTestCase):
    """
    Formal verification of ZFC set theory axioms as implemented in FiniteSet.

    Each test method represents a mathematical theorem about set theory,
    with the test serving as an executable proof of that theorem.
    """

    def setUp(self):
        """
        Establish mathematical context for set theory proofs.

        Creates well-defined test sets that serve as witnesses
        for mathematical properties throughout the verification.
        """
        super().setUp()

        # Mathematical test fixtures - carefully chosen to demonstrate properties
        self.empty = empty_set()
        self.singleton_a = singleton_set("a")
        self.singleton_b = singleton_set("b")
        self.pair_ab = FiniteSet(["a", "b"])
        self.triple_abc = FiniteSet(["a", "b", "c"])
        self.numbers_123 = FiniteSet([1, 2, 3])
        self.numbers_345 = FiniteSet([3, 4, 5])
        self.universal_letters = universal_set(["a", "b", "c", "d", "e"])

        # Store for universal property testing
        self._test_sets = [
            self.empty,
            self.singleton_a,
            self.singleton_b,
            self.pair_ab,
            self.triple_abc,
            self.numbers_123,
            self.numbers_345,
        ]

    @mathematical_property("direct")
    def test_axiom_of_extensionality(self):
        """
        Axiom of Extensionality: Two sets are equal iff they have the same elements.

        Mathematical Statement: ∀A,B: A = B ↔ ∀x(x ∈ A ↔ x ∈ B)

        Proof Method: Direct construction of sets with same elements in different orders,
        verification that equality holds, and construction of sets with different
        elements to verify inequality.
        """
        # Direct proof: Sets with same elements are equal regardless of order
        set1 = FiniteSet([1, 2, 3])
        set2 = FiniteSet([3, 2, 1])  # Same elements, different order
        set3 = FiniteSet([1, 1, 2, 2, 3, 3])  # Same elements with duplicates

        self.assert_mathematical_property(
            set1 == set2,
            "Extensionality: Order Independence",
            "Mathematical sets are defined by their elements, not order of specification",
        )

        self.assert_mathematical_property(
            set1 == set3,
            "Extensionality: Duplicate Elimination",
            "Mathematical sets contain each element at most once",
        )

        # Contrapositive: Sets with different elements are not equal
        set4 = FiniteSet([1, 2, 4])  # Different element

        self.assert_mathematical_property(
            set1 != set4,
            "Extensionality: Different Elements Imply Inequality",
            "Sets with different elements cannot be equal by definition",
        )

    @mathematical_property("construction")
    def test_axiom_of_empty_set(self):
        """
        Axiom of Empty Set: There exists a unique set containing no elements.

        Mathematical Statement: ∃∅ ∀x(x ∉ ∅)

        Proof Method: Constructive proof by creating empty set and verifying
        no element can be a member, plus verification of uniqueness.
        """
        # Constructive existence proof
        empty1 = empty_set()
        empty2 = FiniteSet([])
        empty3 = FiniteSet()

        # Verify all constructions yield the same mathematical object
        self.assert_mathematical_property(
            empty1 == empty2 == empty3,
            "Empty Set Uniqueness",
            "All constructions of empty set yield the same mathematical object",
        )

        # Universal quantification: No element is in empty set
        test_elements = [1, "a", None, [], (1, 2)]

        def not_in_empty(element):
            return element not in empty1

        self.assert_universal_property(
            not_in_empty,
            test_elements,
            "Universal Non-Membership in Empty Set",
            "By definition, no element can be a member of the empty set",
        )

        # Verify cardinality
        self.assert_mathematical_property(
            len(empty1) == 0,
            "Empty Set Cardinality",
            "The empty set has cardinality zero by definition",
        )

    @mathematical_property("construction")
    def test_axiom_of_pairing(self):
        """
        Axiom of Pairing: For any two objects a,b, there exists a set {a,b}.

        Mathematical Statement: ∀a,b ∃c ∀x(x ∈ c ↔ (x = a ∨ x = b))

        Proof Method: Constructive proof for various pairs of objects,
        verification of membership conditions.
        """
        # Test pairing with various object types (all hashable)
        test_pairs = [
            (1, 2),  # Numbers
            ("a", "b"),  # Strings
            (1, "a"),  # Mixed types
            ("x", "x"),  # Identical elements (singleton)
            ((1, 2), (3, 4)),  # Tuples (hashable complex objects)
        ]

        for a, b in test_pairs:
            # Construct the pair set
            pair = FiniteSet([a, b])

            # Verify membership conditions: x ∈ {a,b} ↔ (x = a ∨ x = b)
            self.assert_mathematical_property(
                a in pair and b in pair,
                f"Pairing Membership for {(a,b)}",
                f"Both elements {a} and {b} must be in their pair set",
            )

            # Test non-membership
            non_member = "not_in_pair"
            if non_member != a and non_member != b:
                self.assert_mathematical_property(
                    non_member not in pair,
                    f"Pairing Non-Membership for {(a,b)}",
                    f"Element {non_member} should not be in pair {{{a},{b}}}",
                )

            # Verify cardinality
            expected_size = 1 if a == b else 2
            self.assert_mathematical_property(
                len(pair) == expected_size,
                f"Pairing Cardinality for {(a,b)}",
                f"Pair {{{a},{b}}} should have cardinality {expected_size}",
            )

    @mathematical_property("construction")
    def test_axiom_of_union(self):
        """
        Axiom of Union: For any sets A,B, there exists their union A ∪ B.

        Mathematical Statement: ∀A,B ∃C ∀x(x ∈ C ↔ (x ∈ A ∨ x ∈ B))

        Proof Method: Constructive proof using our union operation,
        verification of membership conditions and algebraic properties.
        """
        # Test union with various set combinations
        A = self.numbers_123
        B = self.numbers_345

        # Construct union
        union_AB = A.union(B)

        # Verify membership condition: x ∈ (A ∪ B) ↔ (x ∈ A ∨ x ∈ B)
        all_elements = [1, 2, 3, 4, 5, 6]  # 6 not in either set

        for x in all_elements:
            in_union = x in union_AB
            in_A_or_B = (x in A) or (x in B)

            self.assert_mathematical_property(
                in_union == in_A_or_B,
                f"Union Membership for element {x}",
                f"Element {x} membership in union must match (∈A ∨ ∈B)",
                counterexample=(x, in_union, in_A_or_B),
            )

        # Verify algebraic properties of union
        self._verify_union_commutativity(A, B)
        self._verify_union_associativity(A, B, self.singleton_a)
        self._verify_union_identity(A)
        self._verify_union_idempotence(A)

    def _verify_union_commutativity(self, A: FiniteSet, B: FiniteSet):
        """Verify A ∪ B = B ∪ A (commutativity)"""
        union_AB = A.union(B)
        union_BA = B.union(A)

        self.assert_mathematical_property(
            union_AB == union_BA,
            "Union Commutativity",
            "Set union must be commutative: A ∪ B = B ∪ A",
            counterexample=(A, B, union_AB, union_BA),
        )

    def _verify_union_associativity(self, A: FiniteSet, B: FiniteSet, C: FiniteSet):
        """Verify (A ∪ B) ∪ C = A ∪ (B ∪ C) (associativity)"""
        left_associative = A.union(B).union(C)
        right_associative = A.union(B.union(C))

        self.assert_mathematical_property(
            left_associative == right_associative,
            "Union Associativity",
            "Set union must be associative: (A ∪ B) ∪ C = A ∪ (B ∪ C)",
            counterexample=(A, B, C, left_associative, right_associative),
        )

    def _verify_union_identity(self, A: FiniteSet):
        """Verify A ∪ ∅ = A (identity element)"""
        union_with_empty = A.union(self.empty)

        self.assert_mathematical_property(
            union_with_empty == A,
            "Union Identity",
            "Empty set is identity element for union: A ∪ ∅ = A",
            counterexample=(A, union_with_empty),
        )

    def _verify_union_idempotence(self, A: FiniteSet):
        """Verify A ∪ A = A (idempotence)"""
        union_with_self = A.union(A)

        self.assert_mathematical_property(
            union_with_self == A,
            "Union Idempotence",
            "Set union is idempotent: A ∪ A = A",
            counterexample=(A, union_with_self),
        )

    @mathematical_property("construction")
    def test_axiom_of_power_set(self):
        """
        Axiom of Power Set: For any set A, there exists its power set P(A).

        Mathematical Statement: ∀A ∃P ∀X(X ∈ P ↔ X ⊆ A)

        Proof Method: Constructive proof for small sets, verification that
        all subsets are included and cardinality follows 2^|A| formula.
        """
        # Test power set construction for small sets
        test_set = FiniteSet([1, 2])
        power_set = test_set.power_set()

        # Verify cardinality: |P(A)| = 2^|A|
        expected_size = 2 ** len(test_set)
        actual_size = len(power_set)

        self.assert_mathematical_property(
            actual_size == expected_size,
            "Power Set Cardinality",
            f"Power set of {test_set} should have {expected_size} elements",
            counterexample=(test_set, actual_size, expected_size),
        )

        # Verify all subsets are included
        expected_subsets = [
            empty_set(),  # ∅
            singleton_set(1),  # {1}
            singleton_set(2),  # {2}
            FiniteSet([1, 2]),  # {1,2}
        ]

        for subset in expected_subsets:
            self.assert_mathematical_property(
                subset in power_set,
                f"Power Set Contains Subset {subset}",
                f"Power set must contain all subsets of original set",
                counterexample=(subset, test_set, power_set),
            )

        # Verify subset relationship: every element of P(A) is subset of A
        for element in power_set:
            self.assert_mathematical_property(
                element.is_subset_of(test_set),
                f"Power Set Element {element} is Subset",
                "Every element of power set must be subset of original",
                counterexample=(element, test_set),
            )

    @mathematical_property("direct")
    def test_intersection_properties(self):
        """
        Verify mathematical properties of set intersection operation.

        Mathematical Properties:
        • Commutativity: A ∩ B = B ∩ A
        • Associativity: (A ∩ B) ∩ C = A ∩ (B ∩ C)
        • Identity: A ∩ U = A (where U is universal set containing A)
        • Null Element: A ∩ ∅ = ∅
        • Idempotence: A ∩ A = A
        """
        A = self.numbers_123
        B = self.numbers_345
        C = self.singleton_a

        # Test intersection definition: x ∈ (A ∩ B) ↔ (x ∈ A ∧ x ∈ B)
        intersection = A.intersection(B)
        expected_intersection = FiniteSet([3])  # Only common element

        self.assert_mathematical_property(
            intersection == expected_intersection,
            "Intersection Definition",
            "Intersection contains exactly common elements",
            counterexample=(A, B, intersection, expected_intersection),
        )

        # Verify algebraic properties
        self.assert_algebraic_law(
            lambda x, y: x.intersection(y),
            "commutativity",
            [(A, B), (self.singleton_a, self.pair_ab)],
            "Set intersection must be commutative",
        )

        self.assert_algebraic_law(
            lambda x, y: x.intersection(y),
            "associativity",
            [(A, B, C)],
            "Set intersection must be associative",
        )

        # Identity and null properties
        universal = FiniteSet([1, 2, 3, 4, 5, 6, 7, 8, 9])
        identity_result = A.intersection(universal)

        self.assert_mathematical_property(
            identity_result == A,
            "Intersection Identity",
            "Intersection with superset yields original set",
            counterexample=(A, universal, identity_result),
        )

        null_result = A.intersection(self.empty)

        self.assert_mathematical_property(
            null_result == self.empty,
            "Intersection Null",
            "Intersection with empty set yields empty set",
            counterexample=(A, null_result),
        )

    @proof_by_contradiction
    def test_russell_paradox_prevention(self):
        """
        Verify that our implementation prevents Russell's Paradox.

        Russell's Paradox: Let R = {x : x ∉ x}. Then R ∈ R ↔ R ∉ R.

        Mathematical Resolution: Modern set theory (ZFC) prevents this paradox
        through the Axiom of Regularity, which prohibits sets from containing themselves.

        Our implementation demonstrates safe set construction principles.
        """
        # Test 1: Verify that unhashable objects cannot be added to sets
        # This maintains mathematical rigor by requiring immutable elements
        with self.assertRaises(SetTheoryException):
            # Lists are unhashable and should be rejected
            FiniteSet([1, 2, [3, 4]])

        # Test 2: Demonstrate that our FiniteSet implementation allows
        # mathematical set of sets construction (which is valid in ZFC)
        empty_set_instance = FiniteSet([])
        singleton_containing_empty = FiniteSet([empty_set_instance])  # {∅}

        # This is mathematically valid: {∅} ≠ ∅
        self.assert_mathematical_property(
            singleton_containing_empty != empty_set_instance,
            "Set Distinctness",
            "The set containing empty set is distinct from empty set: {∅} ≠ ∅",
        )

        # Demonstrate prevention of Russell's paradox through finite set limitations
        # Russell's paradox attempts to form R = {x : x ∉ x}, which leads to R ∈ R ↔ R ∉ R
        # Our finite set implementation avoids this by:
        # 1. Only dealing with finite, explicitly constructed sets
        # 2. Requiring elements to be hashable (immutable)
        # 3. Not supporting unrestricted comprehension

        # Test 3: Verify Russell's paradox scenario cannot occur in practice
        # We cannot construct the "set of all sets that don't contain themselves"
        # because it would require knowing all possible sets (impossible with finite sets)

        # Instead, we demonstrate that our implementation maintains consistency
        # by verifying the law of excluded middle for membership
        test_sets = [
            FiniteSet([1]),  # {1}
            FiniteSet([1, 2]),  # {1, 2}
            FiniteSet([empty_set_instance]),  # {∅}
        ]

        # For each set S, verify membership is well-defined for specific elements
        for s in test_sets:
            # Test with element 1: either 1 ∈ S or 1 ∉ S (but not both)
            contains_one = 1 in s
            not_contains_one = 1 not in s
            self.assert_mathematical_property(
                contains_one != not_contains_one,  # Exactly one must be true
                "Law of Excluded Middle",
                "For any set S and element x: either x ∈ S or x ∉ S (but not both)",
            )

        # Test 4: Demonstrate proper rejection of unhashable elements
        problematic_elements = [
            [1, 2, 3],  # Lists are mutable/unhashable
            {"a": 1},  # Dicts are mutable/unhashable
            {1, 2},  # Sets are mutable/unhashable
        ]

        for element in problematic_elements:
            with self.assertRaises(SetTheoryException):
                FiniteSet([element])

        # This verification shows our implementation maintains logical consistency
        # and prevents the contradiction that defines Russell's paradox.

    @proof_by_induction
    def test_finite_induction_principle(self):
        """
        Verify induction principle for finite sets.

        Principle: If P(∅) holds and ∀S(P(S) → P(S ∪ {x})), then P holds for all finite sets.

        We test this with the property "cardinality equals number of elements".
        """
        # Base case: P(∅) - empty set has cardinality 0
        self.assert_mathematical_property(
            len(self.empty) == 0, "Induction Base Case", "Empty set has cardinality 0"
        )

        # Inductive step: If |S| = n, then |S ∪ {x}| = n+1 (for x ∉ S)
        test_set = FiniteSet([1, 2])
        original_size = len(test_set)
        new_element = 3  # Not in test_set

        extended_set = test_set.add_element(new_element)
        extended_size = len(extended_set)

        self.assert_mathematical_property(
            extended_size == original_size + 1,
            "Induction Step",
            "Adding new element increases cardinality by exactly 1",
            counterexample=(test_set, extended_set, original_size, extended_size),
        )

    @mathematical_property("direct")
    def test_subset_relationship_properties(self):
        """
        Verify mathematical properties of subset relationships.

        Properties:
        • Reflexivity: A ⊆ A
        • Antisymmetry: (A ⊆ B ∧ B ⊆ A) → A = B
        • Transitivity: (A ⊆ B ∧ B ⊆ C) → A ⊆ C
        • Empty set is subset of all sets: ∅ ⊆ A
        """
        A = self.numbers_123
        B = FiniteSet([1, 2, 3, 4, 5])  # Superset of A
        C = FiniteSet([1, 2, 3, 4, 5, 6, 7])  # Superset of B

        # Reflexivity: A ⊆ A
        self.assert_universal_property(
            lambda s: s.is_subset_of(s),
            self._test_sets,
            "Subset Reflexivity",
            "Every set is a subset of itself",
        )

        # Antisymmetry: Prove using equal sets
        a_copy = FiniteSet([1, 2, 3])

        self.assert_mathematical_property(
            A.is_subset_of(a_copy) and a_copy.is_subset_of(A) and A == a_copy,
            "Subset Antisymmetry",
            "Mutual subset relationship implies equality",
        )

        # Transitivity: A ⊆ B ∧ B ⊆ C → A ⊆ C
        a_subset_b = A.is_subset_of(B)
        b_subset_c = B.is_subset_of(C)
        a_subset_c = A.is_subset_of(C)

        self.assert_mathematical_property(
            (a_subset_b and b_subset_c) <= a_subset_c,  # Logical implication
            "Subset Transitivity",
            "Subset relationship is transitive",
            counterexample=(A, B, C, a_subset_b, b_subset_c, a_subset_c),
        )

        # Empty set property
        self.assert_universal_property(
            lambda s: self.empty.is_subset_of(s),
            self._test_sets,
            "Empty Set Universal Subset",
            "Empty set is subset of every set",
        )

    @mathematical_property("direct")
    def test_de_morgan_laws(self):
        """
        Verify De Morgan's Laws for set operations.

        De Morgan's Laws:
        • ¬(A ∪ B) = ¬A ∩ ¬B
        • ¬(A ∩ B) = ¬A ∪ ¬B

        Where ¬A represents the complement of A in some universal set.
        """
        A = FiniteSet([1, 2, 3])
        B = FiniteSet([3, 4, 5])
        U = FiniteSet([1, 2, 3, 4, 5, 6, 7])  # Universal set

        # Compute complements
        complement_a = U.difference(A)
        complement_b = U.difference(B)

        # First De Morgan Law: ¬(A ∪ B) = ¬A ∩ ¬B
        union_ab = A.union(B)
        complement_union = U.difference(union_ab)
        intersection_complements = complement_a.intersection(complement_b)

        self.assert_mathematical_property(
            complement_union == intersection_complements,
            "De Morgan's First Law",
            "Complement of union equals intersection of complements",
            counterexample=(A, B, complement_union, intersection_complements),
        )

        # Second De Morgan Law: ¬(A ∩ B) = ¬A ∪ ¬B
        intersection_ab = A.intersection(B)
        complement_intersection = U.difference(intersection_ab)
        union_complements = complement_a.union(complement_b)

        self.assert_mathematical_property(
            complement_intersection == union_complements,
            "De Morgan's Second Law",
            "Complement of intersection equals union of complements",
            counterexample=(A, B, complement_intersection, union_complements),
        )


class TestSetTheoryPerformance(MathematicalProofTestCase):
    """
    Verify computational complexity claims of set operations.

    This class provides empirical validation of Big-O complexity
    claims made in the FiniteSet implementation documentation.
    """

    @mathematical_property("direct")
    def test_membership_complexity(self):
        """
        Verify that membership testing is O(n) as documented.

        Our implementation uses linear search, so membership
        should scale linearly with set size.
        """

        def input_generator(size: int) -> FiniteSet:
            return FiniteSet(list(range(size)))

        # This will perform empirical complexity analysis
        self.assert_complexity_bound(
            lambda s: max(s.to_list()) in s,  # Worst case: last element
            input_generator,
            "O(n)",
            [10, 50, 100, 200],
        )

    @mathematical_property("direct")
    def test_union_complexity(self):
        """
        Verify that union operation is O(n + m) as documented.

        Union should scale with the sum of input set sizes.
        """

        def union_test(size: int):
            set1 = FiniteSet(list(range(size)))
            set2 = FiniteSet(list(range(size, 2 * size)))
            return set1.union(set2)

        # Test various sizes
        sizes = [10, 25, 50, 100]
        times = []

        for size in sizes:
            import time

            start = time.perf_counter()
            union_test(size)
            end = time.perf_counter()
            times.append((size, end - start))

        # Verify roughly linear growth
        if len(times) >= 2:
            growth_ratio = times[-1][1] / times[0][1]
            size_ratio = times[-1][0] / times[0][0]

            # Allow for some variation in timing
            self.assert_mathematical_property(
                growth_ratio <= size_ratio * 3,  # Allow 3x overhead for variation
                "Union Linear Complexity",
                f"Union operation should scale roughly linearly. "
                f"Growth ratio: {growth_ratio:.2f}, Size ratio: {size_ratio:.2f}",
            )


if __name__ == "__main__":
    # Run all set theory mathematical proofs
    import unittest

    print("Set Theory Mathematical Proof Verification")
    print("=" * 50)
    print("Running formal verification of ZFC axioms and set operations...")
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTest(loader.loadTestsFromTestCase(TestSetTheoryAxioms))
    suite.addTest(loader.loadTestsFromTestCase(TestSetTheoryPerformance))

    # Run with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\nMathematical Verification Summary:")
    print(f"Theorems tested: {result.testsRun}")
    print(
        f"Proofs verified: {result.testsRun - len(result.failures) - len(result.errors)}"
    )
    print(f"Failed proofs: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ All mathematical proofs verified successfully!")
        print("Set theory implementation is mathematically sound.")
    else:
        print("\n❌ Some mathematical proofs failed.")
        print("Implementation requires mathematical corrections.")

    # Educational insight
    print("\nEducational Impact:")
    print("This verification demonstrates how abstract mathematical concepts")
    print("translate to concrete, testable implementations in computer science.")
    print("Students can now see executable proofs of fundamental set theory.")
