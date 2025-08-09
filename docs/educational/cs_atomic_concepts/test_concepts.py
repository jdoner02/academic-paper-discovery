"""
Test Suite for CS Atomic Concepts Educational Library

This comprehensive test suite validates the educational implementations
while serving as additional learning resources for students.

Educational Value:
    • Shows how to write proper unit tests
    • Demonstrates edge cases and error conditions
    • Provides additional examples of concept usage
    • Validates mathematical properties through code

Testing Philosophy:
    "Every test should teach something, and every concept should be tested."

Author: Jessica Doner
Institution: Eastern Washington University
"""

import unittest
import sys
from pathlib import Path

# Add the source directory to the path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from cs_atomic_concepts.foundations.set_theory import (
    FiniteSet,
    SetTheoryException,
    empty_set,
    universal_set,
    singleton_set,
)
from cs_atomic_concepts.foundations.logic import (
    Proposition,
    TruthValue,
    T,
    F,
    NOT,
    AND,
    OR,
    IMPLIES,
    IFF,
    XOR,
    LogicalFormula,
)


class TestSetTheory(unittest.TestCase):
    """
    Test cases for set theory implementation.

    These tests validate both mathematical correctness and edge cases,
    serving as executable documentation of set theory properties.
    """

    def setUp(self):
        """Set up test fixtures - common sets used across tests."""
        self.set_a = FiniteSet([1, 2, 3])
        self.set_b = FiniteSet([3, 4, 5])
        self.set_c = FiniteSet([1, 2])
        self.empty = empty_set()

    def test_set_creation_removes_duplicates(self):
        """Test that sets automatically remove duplicate elements."""
        # Educational note: This tests the fundamental property of sets
        set_with_duplicates = FiniteSet([1, 2, 2, 3, 3, 3])
        expected_elements = {1, 2, 3}
        actual_elements = set(set_with_duplicates.to_list())

        self.assertEqual(actual_elements, expected_elements)
        self.assertEqual(len(set_with_duplicates), 3)

    def test_membership_operations(self):
        """Test set membership using the 'in' operator."""
        # Test basic membership
        self.assertTrue(1 in self.set_a)
        self.assertTrue(3 in self.set_a)
        self.assertFalse(4 in self.set_a)

        # Test empty set membership
        self.assertFalse(1 in self.empty)

    def test_set_equality(self):
        """Test set equality based on elements, not order."""
        # Sets with same elements in different order should be equal
        set1 = FiniteSet([1, 2, 3])
        set2 = FiniteSet([3, 2, 1])
        set3 = FiniteSet([1, 2, 4])

        self.assertEqual(set1, set2)  # Same elements, different order
        self.assertNotEqual(set1, set3)  # Different elements

    def test_union_operation(self):
        """Test set union (∪) operation and its mathematical properties."""
        # Basic union
        union_result = self.set_a.union(self.set_b)
        expected = FiniteSet([1, 2, 3, 4, 5])
        self.assertEqual(union_result, expected)

        # Test commutative property: A ∪ B = B ∪ A
        union_ab = self.set_a.union(self.set_b)
        union_ba = self.set_b.union(self.set_a)
        self.assertEqual(union_ab, union_ba)

        # Test identity property: A ∪ ∅ = A
        union_with_empty = self.set_a.union(self.empty)
        self.assertEqual(union_with_empty, self.set_a)

        # Test idempotent property: A ∪ A = A
        union_with_self = self.set_a.union(self.set_a)
        self.assertEqual(union_with_self, self.set_a)

    def test_intersection_operation(self):
        """Test set intersection (∩) operation and its properties."""
        # Basic intersection
        intersection_result = self.set_a.intersection(self.set_b)
        expected = FiniteSet([3])
        self.assertEqual(intersection_result, expected)

        # Test commutative property: A ∩ B = B ∩ A
        intersection_ab = self.set_a.intersection(self.set_b)
        intersection_ba = self.set_b.intersection(self.set_a)
        self.assertEqual(intersection_ab, intersection_ba)

        # Test null property: A ∩ ∅ = ∅
        intersection_with_empty = self.set_a.intersection(self.empty)
        self.assertEqual(intersection_with_empty, self.empty)

        # Test with disjoint sets
        disjoint_set = FiniteSet([6, 7, 8])
        disjoint_intersection = self.set_a.intersection(disjoint_set)
        self.assertEqual(disjoint_intersection, self.empty)

    def test_difference_operation(self):
        """Test set difference (-) operation."""
        # Basic difference
        difference_result = self.set_a.difference(self.set_b)
        expected = FiniteSet([1, 2])
        self.assertEqual(difference_result, expected)

        # Test non-commutative property: A - B ≠ B - A (generally)
        diff_ab = self.set_a.difference(self.set_b)
        diff_ba = self.set_b.difference(self.set_a)
        self.assertNotEqual(diff_ab, diff_ba)

        # Test A - A = ∅
        self_difference = self.set_a.difference(self.set_a)
        self.assertEqual(self_difference, self.empty)

        # Test A - ∅ = A
        difference_with_empty = self.set_a.difference(self.empty)
        self.assertEqual(difference_with_empty, self.set_a)

    def test_subset_relationships(self):
        """Test subset and superset relationships."""
        # Test proper subset
        self.assertTrue(self.set_c.is_subset_of(self.set_a))
        self.assertTrue(self.set_c.is_proper_subset_of(self.set_a))
        self.assertFalse(self.set_a.is_proper_subset_of(self.set_c))

        # Test superset
        self.assertTrue(self.set_a.is_superset_of(self.set_c))
        self.assertFalse(self.set_c.is_superset_of(self.set_a))

        # Every set is a subset of itself
        self.assertTrue(self.set_a.is_subset_of(self.set_a))

        # Empty set is subset of every set
        self.assertTrue(self.empty.is_subset_of(self.set_a))
        self.assertTrue(self.empty.is_subset_of(self.empty))

    def test_power_set_generation(self):
        """Test power set generation with size validation."""
        # Test small set power set
        small_set = FiniteSet([1, 2])
        power_set = small_set.power_set()

        # Power set should have 2^n elements
        self.assertEqual(len(power_set), 4)  # 2^2 = 4

        # Should contain empty set and the set itself
        self.assertTrue(any(len(subset) == 0 for subset in power_set))
        self.assertTrue(any(subset == small_set for subset in power_set))

        # Test size limit protection
        large_set = FiniteSet(list(range(15)))
        with self.assertRaises(SetTheoryException):
            large_set.power_set()  # Should raise exception for large sets

    def test_cartesian_product(self):
        """Test Cartesian product operation."""
        set_x = FiniteSet([1, 2])
        set_y = FiniteSet(["a", "b"])
        product = set_x.cartesian_product(set_y)

        # Should have |X| × |Y| elements
        self.assertEqual(len(product), 4)  # 2 × 2 = 4

        # Check specific elements exist
        product_list = product.to_list()
        self.assertTrue((1, "a") in product_list)
        self.assertTrue((1, "b") in product_list)
        self.assertTrue((2, "a") in product_list)
        self.assertTrue((2, "b") in product_list)

    def test_set_factory_functions(self):
        """Test factory functions for creating special sets."""
        # Test empty set
        empty = empty_set()
        self.assertEqual(len(empty), 0)

        # Test singleton set
        single = singleton_set(42)
        self.assertEqual(len(single), 1)
        self.assertTrue(42 in single)

        # Test universal set
        universe = universal_set([1, 2, 3, 4, 5])
        self.assertEqual(len(universe), 5)
        for i in range(1, 6):
            self.assertTrue(i in universe)


class TestLogic(unittest.TestCase):
    """
    Test cases for logical reasoning implementation.

    These tests validate logical operators and demonstrate their
    properties through executable examples.
    """

    def setUp(self):
        """Set up test fixtures - common propositions used across tests."""
        self.prop_true = Proposition("Always true", True)
        self.prop_false = Proposition("Always false", False)
        self.prop_p = Proposition("P", True)
        self.prop_q = Proposition("Q", False)

    def test_proposition_creation_and_properties(self):
        """Test basic proposition creation and truth value handling."""
        # Test creation with boolean
        prop = Proposition("Test statement", True)
        self.assertTrue(prop.is_true())
        self.assertFalse(prop.is_false())

        # Test creation with TruthValue enum
        prop_enum = Proposition("Test with enum", TruthValue.FALSE)
        self.assertFalse(prop_enum.is_true())
        self.assertTrue(prop_enum.is_false())

        # Test string representation
        self.assertIn("Test statement", str(prop))
        self.assertIn("T", str(prop))

    def test_not_operator(self):
        """Test logical NOT operation and double negation."""
        # Basic NOT operation
        not_true = NOT.apply(self.prop_true)
        not_false = NOT.apply(self.prop_false)

        self.assertTrue(not_true.is_false())
        self.assertTrue(not_false.is_true())

        # Test double negation: ¬¬P = P
        double_negation = NOT.apply(NOT.apply(self.prop_p))
        self.assertEqual(self.prop_p.truth_value, double_negation.truth_value)

        # Validate truth table
        truth_table = NOT.truth_table()
        self.assertEqual(truth_table[(T,)], F)
        self.assertEqual(truth_table[(F,)], T)

    def test_and_operator(self):
        """Test logical AND operation and its properties."""
        # Test all combinations
        tt = AND.apply(self.prop_true, self.prop_true)
        tf = AND.apply(self.prop_true, self.prop_false)
        ft = AND.apply(self.prop_false, self.prop_true)
        ff = AND.apply(self.prop_false, self.prop_false)

        self.assertTrue(tt.is_true())  # T ∧ T = T
        self.assertTrue(tf.is_false())  # T ∧ F = F
        self.assertTrue(ft.is_false())  # F ∧ T = F
        self.assertTrue(ff.is_false())  # F ∧ F = F

        # Test commutative property: P ∧ Q = Q ∧ P
        pq = AND.apply(self.prop_p, self.prop_q)
        qp = AND.apply(self.prop_q, self.prop_p)
        self.assertEqual(pq.truth_value, qp.truth_value)

    def test_or_operator(self):
        """Test logical OR operation and its properties."""
        # Test all combinations
        tt = OR.apply(self.prop_true, self.prop_true)
        tf = OR.apply(self.prop_true, self.prop_false)
        ft = OR.apply(self.prop_false, self.prop_true)
        ff = OR.apply(self.prop_false, self.prop_false)

        self.assertTrue(tt.is_true())  # T ∨ T = T
        self.assertTrue(tf.is_true())  # T ∨ F = T
        self.assertTrue(ft.is_true())  # F ∨ T = T
        self.assertTrue(ff.is_false())  # F ∨ F = F

        # Test commutative property: P ∨ Q = Q ∨ P
        pq = OR.apply(self.prop_p, self.prop_q)
        qp = OR.apply(self.prop_q, self.prop_p)
        self.assertEqual(pq.truth_value, qp.truth_value)

    def test_implies_operator(self):
        """Test logical IMPLIES operation."""
        # Test all combinations - critical for understanding implication
        tt = IMPLIES.apply(self.prop_true, self.prop_true)
        tf = IMPLIES.apply(self.prop_true, self.prop_false)
        ft = IMPLIES.apply(self.prop_false, self.prop_true)
        ff = IMPLIES.apply(self.prop_false, self.prop_false)

        self.assertTrue(tt.is_true())  # T → T = T
        self.assertTrue(tf.is_false())  # T → F = F (only false case!)
        self.assertTrue(ft.is_true())  # F → T = T (vacuously true)
        self.assertTrue(ff.is_true())  # F → F = T (vacuously true)

        # Test equivalence: P → Q ≡ ¬P ∨ Q
        implies_result = IMPLIES.apply(self.prop_p, self.prop_q)
        equivalent_result = OR.apply(NOT.apply(self.prop_p), self.prop_q)
        self.assertEqual(implies_result.truth_value, equivalent_result.truth_value)

    def test_iff_operator(self):
        """Test logical IF-AND-ONLY-IF operation."""
        # Test all combinations
        tt = IFF.apply(self.prop_true, self.prop_true)
        tf = IFF.apply(self.prop_true, self.prop_false)
        ft = IFF.apply(self.prop_false, self.prop_true)
        ff = IFF.apply(self.prop_false, self.prop_false)

        self.assertTrue(tt.is_true())  # T ↔ T = T
        self.assertTrue(tf.is_false())  # T ↔ F = F
        self.assertTrue(ft.is_false())  # F ↔ T = F
        self.assertTrue(ff.is_true())  # F ↔ F = T

        # Test equivalence: P ↔ Q ≡ (P → Q) ∧ (Q → P)
        iff_result = IFF.apply(self.prop_p, self.prop_q)
        p_implies_q = IMPLIES.apply(self.prop_p, self.prop_q)
        q_implies_p = IMPLIES.apply(self.prop_q, self.prop_p)
        equivalent_result = AND.apply(p_implies_q, q_implies_p)
        self.assertEqual(iff_result.truth_value, equivalent_result.truth_value)

    def test_xor_operator(self):
        """Test exclusive OR operation."""
        # Test all combinations
        tt = XOR.apply(self.prop_true, self.prop_true)
        tf = XOR.apply(self.prop_true, self.prop_false)
        ft = XOR.apply(self.prop_false, self.prop_true)
        ff = XOR.apply(self.prop_false, self.prop_false)

        self.assertTrue(tt.is_false())  # T ⊕ T = F
        self.assertTrue(tf.is_true())  # T ⊕ F = T
        self.assertTrue(ft.is_true())  # F ⊕ T = T
        self.assertTrue(ff.is_false())  # F ⊕ F = F

        # Test relationship: P ⊕ Q ≡ ¬(P ↔ Q)
        xor_result = XOR.apply(self.prop_p, self.prop_q)
        iff_result = IFF.apply(self.prop_p, self.prop_q)
        not_iff_result = NOT.apply(iff_result)
        self.assertEqual(xor_result.truth_value, not_iff_result.truth_value)

    def test_logical_formula_composition(self):
        """Test building complex formulas from simple propositions."""
        formula = LogicalFormula()

        # Build: (P ∧ Q) ∨ (¬P ∧ ¬Q)
        p_and_q = formula.and_op(self.prop_p, self.prop_q)
        not_p = formula.not_op(self.prop_p)
        not_q = formula.not_op(self.prop_q)
        not_p_and_not_q = formula.and_op(not_p, not_q)

        complex_formula = formula.or_op(p_and_q, not_p_and_not_q)

        # This should be equivalent to P ↔ Q
        iff_result = formula.iff(self.prop_p, self.prop_q)
        self.assertEqual(complex_formula.truth_value, iff_result.truth_value)

    def test_demorgans_laws(self):
        """Test De Morgan's Laws - fundamental for boolean algebra."""
        # First De Morgan's Law: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q
        p_and_q = AND.apply(self.prop_p, self.prop_q)
        not_p_and_q = NOT.apply(p_and_q)

        not_p = NOT.apply(self.prop_p)
        not_q = NOT.apply(self.prop_q)
        not_p_or_not_q = OR.apply(not_p, not_q)

        self.assertEqual(not_p_and_q.truth_value, not_p_or_not_q.truth_value)

        # Second De Morgan's Law: ¬(P ∨ Q) ≡ ¬P ∧ ¬Q
        p_or_q = OR.apply(self.prop_p, self.prop_q)
        not_p_or_q = NOT.apply(p_or_q)

        not_p_and_not_q = AND.apply(not_p, not_q)

        self.assertEqual(not_p_or_q.truth_value, not_p_and_not_q.truth_value)


class TestLibraryIntegration(unittest.TestCase):
    """
    Test integration between different concepts in the library.

    These tests demonstrate how foundational concepts work together
    and validate the educational connections between modules.
    """

    def test_set_and_logic_integration(self):
        """Test how set theory and logic concepts integrate."""
        # Create sets representing truth sets of propositions
        true_props = FiniteSet(["P", "R", "S"])
        false_props = FiniteSet(["Q", "T"])

        # Test proposition membership in truth sets
        self.assertTrue("P" in true_props)
        self.assertFalse("Q" in true_props)

        # Union of truth sets represents OR operation
        all_props = true_props.union(false_props)
        expected_all = FiniteSet(["P", "Q", "R", "S", "T"])
        self.assertEqual(all_props, expected_all)

        # Intersection of complementary sets should be empty
        intersection = true_props.intersection(false_props)
        self.assertEqual(intersection, empty_set())

    def test_educational_metadata_consistency(self):
        """Test that educational metadata is consistent across modules."""
        from cs_atomic_concepts.foundations.set_theory import (
            PREREQUISITES as set_prereqs,
        )
        from cs_atomic_concepts.foundations.logic import PREREQUISITES as logic_prereqs

        # Set theory should have no prerequisites (foundational)
        self.assertEqual(set_prereqs, [])

        # Logic should build on set theory
        self.assertIn("set_theory", logic_prereqs)


def run_educational_test_suite():
    """
    Run the complete test suite with educational commentary.

    This function provides a guided tour through the test results,
    explaining what each test validates and why it matters.
    """
    print("CS Atomic Concepts Educational Test Suite")
    print("=" * 50)
    print()
    print("This test suite validates the mathematical correctness")
    print("of our educational implementations and demonstrates")
    print("proper testing practices for computer science concepts.")
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSetTheory))
    suite.addTests(loader.loadTestsFromTestCase(TestLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestLibraryIntegration))

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Educational summary
    print("\n" + "=" * 50)
    print("Educational Test Summary")
    print("=" * 50)

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = total_tests - failures - errors

    print(f"Total tests run: {total_tests}")
    print(f"Successful tests: {successes}")
    print(f"Failed tests: {failures}")
    print(f"Error tests: {errors}")

    if failures == 0 and errors == 0:
        print("\n🎉 All tests passed! The mathematical implementations")
        print("   are correct and ready for educational use.")
    else:
        print(f"\n⚠️  Some tests failed. This indicates either:")
        print("   • A bug in the implementation")
        print("   • An incorrect understanding of the mathematical concept")
        print("   • A test that needs to be updated")

    print(f"\nTest Coverage:")
    print(f"  ✅ Set theory fundamentals and operations")
    print(f"  ✅ Logical reasoning and truth tables")
    print(f"  ✅ Mathematical property validation")
    print(f"  ✅ Integration between concepts")
    print(f"  ✅ Error handling and edge cases")

    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the educational test suite
    success = run_educational_test_suite()

    print("\n" + "=" * 50)
    print("Next Steps:")
    if success:
        print("• Implement additional foundational concepts (relations, functions)")
        print("• Create abstract base classes for data structures")
        print("• Build concrete implementations demonstrating inheritance")
        print("• Add comprehensive documentation and examples")
    else:
        print("• Fix failing tests to ensure mathematical correctness")
        print("• Review implementations against mathematical definitions")
        print("• Update test cases if requirements have changed")

    sys.exit(0 if success else 1)
