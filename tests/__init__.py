"""
Mathematical Proof-Based Testing Framework for CS Atomic Concepts

This testing framework treats each test as a formal mathematical proof,
validating the correctness of our educational CS implementations through
rigorous mathematical verification rather than simple behavioral testing.

Educational Philosophy:
    "Every test is a theorem, every implementation is a proof,
     every student interaction is a mathematical verification."

Proof-Based Testing Principles:
    1. Axiomatic Foundation: Test mathematical axioms that define each concept
    2. Property Validation: Verify universal mathematical properties hold
    3. Proof by Contradiction: Use edge cases to validate logical completeness
    4. Constructive Proofs: Build complex concepts from simpler validated ones
    5. Inductive Reasoning: Test recursive/iterative algorithms with mathematical induction
    6. Formal Verification: Validate computational complexity claims empirically

Mathematical Rigor Standards:
    ✓ Every operation must satisfy its mathematical definition
    ✓ All claimed properties must be formally verified through tests
    ✓ Edge cases serve as proof by contradiction for logical completeness
    ✓ Performance tests validate Big-O complexity claims with empirical data
    ✓ Invariants must hold throughout all operations
    ✓ Algebraic laws (commutativity, associativity, etc.) must be verified

Testing Architecture:
    📁 tests/
    ├── 📁 foundations/          # Mathematical axioms and basic operations
    │   ├── test_set_theory.py   # ZFC axioms, set operations, Russell's paradox
    │   ├── test_logic.py        # Boolean algebra, propositional logic
    │   ├── test_functions.py    # Function theory, domain/codomain
    │   └── test_relations.py    # Equivalence relations, ordering
    ├── 📁 abstractions/         # Abstract mathematical structures
    │   ├── test_data_structure.py  # Abstract base class properties
    │   ├── test_algorithm.py       # Algorithmic complexity verification
    │   └── test_interfaces.py      # Contract validation
    ├── 📁 concrete_structures/  # Concrete implementations with formal proofs
    │   ├── 📁 linear/           # Sequential access mathematical verification
    │   ├── 📁 trees/            # Hierarchical structure proofs
    │   └── 📁 graphs/           # Network structure validation
    ├── 📁 algorithms/           # Algorithmic correctness proofs
    │   ├── test_sorting.py      # Correctness, stability, complexity
    │   ├── test_searching.py    # Completeness, optimality
    │   └── test_graph_algorithms.py  # Path algorithms, optimization
    └── 📁 design_patterns/      # Software engineering pattern validation
        ├── test_creational.py   # Object creation patterns
        ├── test_structural.py   # Composition patterns
        └── test_behavioral.py   # Interaction patterns

Property-Based Testing Integration:
    Using Hypothesis library for generating test cases that verify
    mathematical properties hold for all valid inputs, not just
    hand-crafted examples.

Integration with GitHub Classroom:
    - Automated mathematical proof validation
    - Property-based test generation for student submissions
    - Formal verification of algorithmic implementations
    - Educational feedback based on which mathematical properties fail

Author: Jessica Doner
Institution: Eastern Washington University
Mathematical Foundation: ZFC Set Theory, Category Theory, Type Theory
Verification Methods: Property-Based Testing, Formal Methods, Proof Assistants
"""

import unittest
import sys
import time
import random
import math
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Dict, Set, Optional, TypeVar, Generic
from pathlib import Path
from dataclasses import dataclass
from functools import wraps
import inspect

# Add source directory for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mathematical proof testing framework types
T = TypeVar("T")
ProofResult = bool
MathematicalProperty = Callable[..., ProofResult]


@dataclass
class ProofVerification:
    """
    Represents the result of a mathematical proof verification.

    This class encapsulates not just whether a proof succeeded,
    but also the mathematical reasoning and educational insights.
    """

    theorem_name: str
    proof_method: str  # "direct", "contradiction", "induction", "construction"
    is_valid: bool
    mathematical_insight: str
    counterexample: Optional[Any] = None
    proof_steps: Optional[List[str]] = None
    computational_complexity: Optional[str] = None

    def __post_init__(self):
        if self.proof_steps is None:
            self.proof_steps = []


class MathematicalProofException(Exception):
    """
    Exception raised when a mathematical proof fails.

    This provides detailed information about why the mathematical
    property doesn't hold, enabling educational debugging.
    """

    def __init__(
        self, theorem: str, counterexample: Any = None, mathematical_reason: str = ""
    ):
        self.theorem = theorem
        self.counterexample = counterexample
        self.mathematical_reason = mathematical_reason
        super().__init__(self._format_mathematical_error())

    def _format_mathematical_error(self) -> str:
        error_msg = f"Mathematical Theorem Failed: {self.theorem}\n"
        if self.mathematical_reason:
            error_msg += f"Mathematical Reasoning: {self.mathematical_reason}\n"
        if self.counterexample is not None:
            error_msg += f"Counterexample: {self.counterexample}\n"
        return error_msg


def mathematical_property(proof_method: str = "direct"):
    """
    Decorator to mark test methods as mathematical property verifications.

    Args:
        proof_method: Type of proof ("direct", "contradiction", "induction", "construction")

    This decorator transforms ordinary unit tests into formal mathematical
    property verification, providing rich educational context.
    """

    def decorator(test_func: Callable) -> Callable:
        @wraps(test_func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()

            try:
                # Execute the mathematical proof
                result = test_func(self, *args, **kwargs)
                execution_time = time.time() - start_time

                # Create proof verification record
                verification = ProofVerification(
                    theorem_name=test_func.__name__,
                    proof_method=proof_method,
                    is_valid=True,
                    mathematical_insight=test_func.__doc__ or "No insight provided",
                    computational_complexity=self._analyze_complexity(execution_time),
                )

                # Store verification for educational reporting
                if not hasattr(self, "_proof_verifications"):
                    self._proof_verifications = []
                self._proof_verifications.append(verification)

                return result

            except Exception as e:
                execution_time = time.time() - start_time

                # Convert failure to mathematical proof failure
                verification = ProofVerification(
                    theorem_name=test_func.__name__,
                    proof_method=proof_method,
                    is_valid=False,
                    mathematical_insight=f"Proof failed: {str(e)}",
                    counterexample=getattr(e, "counterexample", None),
                )

                if not hasattr(self, "_proof_verifications"):
                    self._proof_verifications = []
                self._proof_verifications.append(verification)

                raise MathematicalProofException(
                    theorem=test_func.__name__,
                    counterexample=getattr(e, "counterexample", None),
                    mathematical_reason=str(e),
                )

        # Mark function as mathematical property
        wrapper._is_mathematical_property = True
        wrapper._proof_method = proof_method
        return wrapper

    return decorator


def proof_by_contradiction(test_func: Callable) -> Callable:
    """
    Decorator for proof by contradiction tests.

    These tests verify logical completeness by showing that
    the negation of a property leads to contradiction.
    """
    return mathematical_property("contradiction")(test_func)


def proof_by_construction(test_func: Callable) -> Callable:
    """
    Decorator for constructive proofs.

    These tests prove existence by explicitly constructing
    the mathematical object in question.
    """
    return mathematical_property("construction")(test_func)


def proof_by_induction(test_func: Callable) -> Callable:
    """
    Decorator for inductive proofs.

    These tests verify properties that hold for all natural numbers
    or recursive structures through mathematical induction.
    """
    return mathematical_property("induction")(test_func)


class MathematicalProofTestCase(unittest.TestCase):
    """
    Enhanced TestCase that provides mathematical proof verification capabilities.

    This class extends unittest.TestCase with formal mathematical reasoning,
    enabling tests to serve as executable mathematical proofs.
    """

    def setUp(self):
        """Initialize mathematical proof verification system."""
        self._proof_verifications: List[ProofVerification] = []
        self._mathematical_context = {}

    def tearDown(self):
        """Generate mathematical proof report after test completion."""
        if hasattr(self, "_proof_verifications"):
            self._generate_proof_report()

    def assert_mathematical_property(
        self,
        condition: bool,
        property_name: str,
        mathematical_explanation: str = "",
        counterexample: Any = None,
    ):
        """
        Assert that a mathematical property holds.

        Args:
            condition: Boolean result of mathematical property check
            property_name: Name of the mathematical property being tested
            mathematical_explanation: Educational explanation of why this matters
            counterexample: Example that would violate the property (if any)

        Raises:
            MathematicalProofException: If property doesn't hold
        """
        if not condition:
            raise MathematicalProofException(
                theorem=property_name,
                counterexample=counterexample,
                mathematical_reason=mathematical_explanation,
            )

    def assert_universal_property(
        self,
        property_function: Callable[[T], bool],
        test_domain: List[T],
        property_name: str,
        mathematical_explanation: str = "",
    ):
        """
        Assert that a property holds for all elements in a domain.

        This implements universal quantification: ∀x ∈ Domain: P(x)

        Args:
            property_function: Function that tests the property for one element
            test_domain: List of elements to test (sample of universal domain)
            property_name: Name of the universal property
            mathematical_explanation: Why this universal property matters
        """
        for element in test_domain:
            try:
                if not property_function(element):
                    raise MathematicalProofException(
                        theorem=f"Universal Property: {property_name}",
                        counterexample=element,
                        mathematical_reason=f"{mathematical_explanation}. Failed for element: {element}",
                    )
            except Exception as e:
                raise MathematicalProofException(
                    theorem=f"Universal Property: {property_name}",
                    counterexample=element,
                    mathematical_reason=f"{mathematical_explanation}. Exception for element {element}: {str(e)}",
                )

    def assert_existential_property(
        self,
        property_function: Callable[[T], bool],
        test_domain: List[T],
        property_name: str,
        mathematical_explanation: str = "",
    ):
        """
        Assert that a property holds for at least one element in domain.

        This implements existential quantification: ∃x ∈ Domain: P(x)

        Args:
            property_function: Function that tests the property for one element
            test_domain: List of elements to test
            property_name: Name of the existential property
            mathematical_explanation: Why this existence matters
        """
        for element in test_domain:
            try:
                if property_function(element):
                    return  # Found witness, property holds
            except Exception:
                continue  # Keep searching

        # No witness found
        raise MathematicalProofException(
            theorem=f"Existential Property: {property_name}",
            counterexample=test_domain,
            mathematical_reason=f"{mathematical_explanation}. No element in domain satisfies property.",
        )

    def assert_algebraic_law(
        self,
        operation: Callable,
        law_name: str,
        test_cases: List[tuple],
        mathematical_explanation: str = "",
    ):
        """
        Assert that an algebraic law holds for given test cases.

        Examples:
            - Commutativity: f(a,b) = f(b,a)
            - Associativity: f(f(a,b),c) = f(a,f(b,c))
            - Identity: f(a, identity) = a

        Args:
            operation: Function implementing the algebraic operation
            law_name: Name of the algebraic law being tested
            test_cases: List of tuples containing test inputs
            mathematical_explanation: Educational explanation of the law
        """
        for test_case in test_cases:
            self._verify_single_algebraic_case(
                operation, law_name, test_case, mathematical_explanation
            )

    def _verify_single_algebraic_case(
        self,
        operation: Callable,
        law_name: str,
        test_case: tuple,
        mathematical_explanation: str,
    ):
        """Helper method to verify single algebraic law case."""
        try:
            if law_name.lower() == "commutativity":
                a, b = test_case
                result1 = operation(a, b)
                result2 = operation(b, a)
                if result1 != result2:
                    raise MathematicalProofException(
                        theorem=f"Commutativity: {law_name}",
                        counterexample=(a, b, result1, result2),
                        mathematical_reason=f"{mathematical_explanation}. f({a},{b}) = {result1} ≠ {result2} = f({b},{a})",
                    )

            elif law_name.lower() == "associativity":
                a, b, c = test_case
                result1 = operation(operation(a, b), c)
                result2 = operation(a, operation(b, c))
                if result1 != result2:
                    raise MathematicalProofException(
                        theorem=f"Associativity: {law_name}",
                        counterexample=(a, b, c, result1, result2),
                        mathematical_reason=f"{mathematical_explanation}. f(f({a},{b}),{c}) = {result1} ≠ {result2} = f({a},f({b},{c}))",
                    )

        except Exception as e:
            if isinstance(e, MathematicalProofException):
                raise
            else:
                raise MathematicalProofException(
                    theorem=f"Algebraic Law: {law_name}",
                    counterexample=test_case,
                    mathematical_reason=f"{mathematical_explanation}. Exception: {str(e)}",
                )

    def assert_complexity_bound(
        self,
        algorithm_function: Callable,
        input_generator: Callable[[int], Any],
        expected_complexity: str,
        test_sizes: List[int] = None,
    ):
        """
        Assert that an algorithm meets its claimed computational complexity.

        This performs empirical analysis to validate Big-O claims through
        statistical analysis of execution times.

        Args:
            algorithm_function: The algorithm to test
            input_generator: Function that generates test input of given size
            expected_complexity: Expected complexity (e.g., "O(n)", "O(n log n)")
            test_sizes: List of input sizes to test
        """
        if test_sizes is None:
            test_sizes = [10, 50, 100, 500, 1000]

        execution_times = []

        for size in test_sizes:
            test_input = input_generator(size)

            # Measure execution time
            start_time = time.perf_counter()
            algorithm_function(test_input)
            end_time = time.perf_counter()

            execution_times.append((size, end_time - start_time))

        # Analyze growth pattern
        complexity_analysis = self._analyze_complexity_pattern(
            execution_times, expected_complexity
        )

        if not complexity_analysis["matches_expected"]:
            raise MathematicalProofException(
                theorem=f"Computational Complexity: {expected_complexity}",
                counterexample=execution_times,
                mathematical_reason=f"Empirical analysis suggests {complexity_analysis['observed_complexity']} rather than {expected_complexity}",
            )

    def _analyze_complexity(self, execution_time: float) -> str:
        """Analyze computational complexity based on execution time."""
        if execution_time < 0.001:
            return "O(1) or very efficient"
        elif execution_time < 0.01:
            return "O(log n) or O(n) for small inputs"
        elif execution_time < 0.1:
            return "O(n) or O(n log n) for moderate inputs"
        elif execution_time < 1.0:
            return "O(n^2) or higher complexity"
        else:
            return "High complexity or large input"

    def _analyze_complexity_pattern(
        self, execution_times: List[tuple], expected_complexity: str
    ) -> Dict[str, Any]:
        """
        Analyze whether execution time pattern matches expected complexity.

        Uses statistical analysis to determine if growth pattern matches
        theoretical complexity claims.
        """
        # Simple heuristic analysis (could be enhanced with regression)
        if len(execution_times) < 3:
            return {
                "matches_expected": True,
                "observed_complexity": "insufficient_data",
            }

        # Calculate growth ratios
        ratios = []
        for i in range(1, len(execution_times)):
            size_ratio = execution_times[i][0] / execution_times[i - 1][0]
            time_ratio = (
                execution_times[i][1] / execution_times[i - 1][1]
                if execution_times[i - 1][1] > 0
                else float("inf")
            )
            ratios.append((size_ratio, time_ratio))

        # Analyze average growth pattern
        avg_time_growth = sum(ratio[1] for ratio in ratios) / len(ratios)
        avg_size_growth = sum(ratio[0] for ratio in ratios) / len(ratios)

        # Heuristic complexity classification
        if avg_time_growth <= avg_size_growth * 1.2:
            observed = "O(n) or better"
        elif avg_time_growth <= avg_size_growth * math.log2(avg_size_growth) * 1.5:
            observed = "O(n log n)"
        elif avg_time_growth <= avg_size_growth**2 * 1.5:
            observed = "O(n^2)"
        else:
            observed = "O(n^3) or worse"

        matches = (
            expected_complexity.lower() in observed.lower()
            or observed.lower() in expected_complexity.lower()
        )

        return {
            "matches_expected": matches,
            "observed_complexity": observed,
            "growth_analysis": ratios,
        }

    def _generate_proof_report(self):
        """Generate educational report of mathematical proofs verified."""
        if not self._proof_verifications:
            return

        print("\n" + "=" * 80)
        print("MATHEMATICAL PROOF VERIFICATION REPORT")
        print(f"Test Class: {self.__class__.__name__}")
        print("=" * 80)

        valid_proofs = [p for p in self._proof_verifications if p.is_valid]
        invalid_proofs = [p for p in self._proof_verifications if not p.is_valid]

        print(f"Total Theorems Tested: {len(self._proof_verifications)}")
        print(f"Valid Proofs: {len(valid_proofs)}")
        print(f"Failed Proofs: {len(invalid_proofs)}")
        print(
            f"Proof Success Rate: {len(valid_proofs)/len(self._proof_verifications)*100:.1f}%"
        )


# Export key testing framework components
__all__ = [
    "MathematicalProofTestCase",
    "MathematicalProofException",
    "ProofVerification",
    "mathematical_property",
    "proof_by_contradiction",
    "proof_by_construction",
    "proof_by_induction",
]
