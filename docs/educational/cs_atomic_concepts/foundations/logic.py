"""
Atomic Concept: Logic - Boolean Reasoning and Propositional Calculus

This module implements logical reasoning from first principles, demonstrating
the mathematical foundation underlying all programming conditionals, boolean
algebra, and formal verification in computer science.

Educational Philosophy:
    "Every if statement is an application of logical reasoning, and every
     computer program is essentially a complex logical proof."

Learning Objectives:
    ✓ Understand propositions as statements that are either true or false
    ✓ Implement logical operators (AND, OR, NOT, IMPLIES, etc.)
    ✓ Apply truth tables and logical equivalences
    ✓ Recognize logic in programming constructs and algorithm design

Real-World Applications:
    • Programming conditionals (if, while, for loop conditions)
    • Database queries (WHERE clauses with AND/OR)
    • Search engines (boolean search queries)
    • Circuit design (digital logic gates)
    • Artificial intelligence (rule-based systems)
    • Formal verification (proving program correctness)

Mathematical Definition:
    Propositional logic deals with propositions (statements that are either
    true or false) and logical connectives that combine them.

    Core Components:
    • Proposition: A statement that is either true or false
    • Logical connectives: ∧ (AND), ∨ (OR), ¬ (NOT), → (IMPLIES), ↔ (IFF)
    • Truth values: True (T, 1) and False (F, 0)
    • Truth tables: Define the meaning of logical connectives

Prerequisites:
    set_theory - Logic operates on sets of true/false values

Performance Characteristics:
    All operations are O(1) for individual propositions.
    Complex formulas have cost proportional to their structure.

Common Misconceptions:
    ❌ "True/false in programming is the same as mathematical logic"
    ✅ Programming booleans implement mathematical logic principles

    ❌ "Logic is just for theoretical computer science"
    ✅ Every program uses logical reasoning extensively

    ❌ "IMPLIES (→) works like cause and effect"
    ✅ Mathematical implication is about logical consistency, not causation

Author: Jessica Doner
Course: CSCD 210 - Data Structures
Complexity: Foundational (accessible to middle school students)
"""

from typing import Any, List, Dict, Union, Callable
from abc import ABC, abstractmethod
from enum import Enum


class TruthValue(Enum):
    """
    Represents the two possible truth values in propositional logic.

    This explicit enumeration makes the connection to mathematical logic clear
    and prevents confusion with Python's built-in True/False which have
    additional programming semantics.
    """

    TRUE = True
    FALSE = False

    def __bool__(self) -> bool:
        """Allow use in boolean contexts like if statements."""
        return self.value

    def __str__(self) -> str:
        """String representation using mathematical notation."""
        return "T" if self.value else "F"

    def __repr__(self) -> str:
        """Programmer representation."""
        return f"TruthValue.{self.name}"


# Convenience constants for cleaner code
T = TruthValue.TRUE
F = TruthValue.FALSE


class Proposition:
    """
    A proposition is a statement that is either true or false.

    In propositional logic, propositions are the atomic units of reasoning.
    They can be combined using logical connectives to form complex statements.

    Examples:
        >>> p = Proposition("It is raining", True)
        >>> q = Proposition("I carry an umbrella", False)
        >>> print(p)  # "It is raining: T"
        >>> print(q)  # "I carry an umbrella: F"

        >>> # Create propositions from variables
        >>> x = Proposition("x > 5", None)  # Truth value to be determined
        >>> print(x.evaluate_with(x=7))  # Would need evaluation context
    """

    def __init__(
        self, statement: str, truth_value: Union[bool, TruthValue, None] = None
    ):
        """
        Create a proposition with a statement and optional truth value.

        Args:
            statement: Human-readable description of the proposition
            truth_value: Whether the statement is true or false (None if unknown)
        """
        self.statement = statement
        if truth_value is None:
            self._truth_value = None
        elif isinstance(truth_value, TruthValue):
            self._truth_value = truth_value
        else:
            self._truth_value = TruthValue.TRUE if truth_value else TruthValue.FALSE

    @property
    def truth_value(self) -> TruthValue:
        """Get the truth value of this proposition."""
        if self._truth_value is None:
            raise ValueError(f"Truth value not set for proposition: {self.statement}")
        return self._truth_value

    @truth_value.setter
    def truth_value(self, value: Union[bool, TruthValue]):
        """Set the truth value of this proposition."""
        if isinstance(value, TruthValue):
            self._truth_value = value
        else:
            self._truth_value = TruthValue.TRUE if value else TruthValue.FALSE

    def is_true(self) -> bool:
        """Check if this proposition is true."""
        return self.truth_value == TruthValue.TRUE

    def is_false(self) -> bool:
        """Check if this proposition is false."""
        return self.truth_value == TruthValue.FALSE

    def __str__(self) -> str:
        """String representation showing statement and truth value."""
        if self._truth_value is None:
            return f'"{self.statement}": ?'
        return f'"{self.statement}": {self._truth_value}'

    def __repr__(self) -> str:
        """Programmer representation."""
        return f'Proposition("{self.statement}", {self._truth_value})'

    def __eq__(self, other) -> bool:
        """Two propositions are equal if they have the same truth value."""
        if not isinstance(other, Proposition):
            return False
        try:
            return self.truth_value == other.truth_value
        except ValueError:
            return False  # Can't compare if truth values not set


class LogicalOperator(ABC):
    """
    Abstract base class for logical operators (connectives).

    This demonstrates object-oriented design principles while teaching logic.
    Each operator is an object that can be applied to propositions.
    """

    @abstractmethod
    def apply(self, *propositions: Proposition) -> Proposition:
        """Apply this logical operator to the given propositions."""
        pass

    @abstractmethod
    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return the truth table for this operator."""
        pass

    @abstractmethod
    def symbol(self) -> str:
        """Return the mathematical symbol for this operator."""
        pass


class NotOperator(LogicalOperator):
    """
    Logical negation: ¬P (NOT P)

    The negation of a proposition has the opposite truth value.

    Truth Table:
        P | ¬P
        --|---
        T | F
        F | T

    Programming Equivalent: not operator
    Circuit Equivalent: NOT gate (inverter)
    """

    def apply(self, p: Proposition) -> Proposition:
        """Apply logical NOT to a proposition."""
        result_value = TruthValue.FALSE if p.is_true() else TruthValue.TRUE
        result_statement = f"¬({p.statement})"
        return Proposition(result_statement, result_value)

    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return truth table for NOT operation."""
        return {(T,): F, (F,): T}

    def symbol(self) -> str:
        return "¬"


class AndOperator(LogicalOperator):
    """
    Logical conjunction: P ∧ Q (P AND Q)

    The conjunction is true only when both propositions are true.

    Truth Table:
        P | Q | P∧Q
        --|---|----
        T | T | T
        T | F | F
        F | T | F
        F | F | F

    Programming Equivalent: and operator
    Circuit Equivalent: AND gate
    """

    def apply(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply logical AND to two propositions."""
        result_value = (
            TruthValue.TRUE if (p.is_true() and q.is_true()) else TruthValue.FALSE
        )
        result_statement = f"({p.statement}) ∧ ({q.statement})"
        return Proposition(result_statement, result_value)

    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return truth table for AND operation."""
        return {(T, T): T, (T, F): F, (F, T): F, (F, F): F}

    def symbol(self) -> str:
        return "∧"


class OrOperator(LogicalOperator):
    """
    Logical disjunction: P ∨ Q (P OR Q)

    The disjunction is true when at least one proposition is true.

    Truth Table:
        P | Q | P∨Q
        --|---|----
        T | T | T
        T | F | T
        F | T | T
        F | F | F

    Programming Equivalent: or operator
    Circuit Equivalent: OR gate
    """

    def apply(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply logical OR to two propositions."""
        result_value = (
            TruthValue.TRUE if (p.is_true() or q.is_true()) else TruthValue.FALSE
        )
        result_statement = f"({p.statement}) ∨ ({q.statement})"
        return Proposition(result_statement, result_value)

    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return truth table for OR operation."""
        return {(T, T): T, (T, F): T, (F, T): T, (F, F): F}

    def symbol(self) -> str:
        return "∨"


class ImpliesOperator(LogicalOperator):
    """
    Logical implication: P → Q (P IMPLIES Q)

    The implication is false only when P is true and Q is false.
    Read as "if P then Q" or "P implies Q".

    Truth Table:
        P | Q | P→Q
        --|---|----
        T | T | T
        T | F | F
        F | T | T
        F | F | T

    Key Insight: When the premise (P) is false, the implication is vacuously true.

    Programming Equivalent: if P: Q (but note: programming if doesn't return boolean)
    Mathematical Use: Theorems ("if hypothesis then conclusion")
    """

    def apply(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply logical IMPLIES to two propositions."""
        # P → Q is equivalent to ¬P ∨ Q
        result_value = (
            TruthValue.FALSE if (p.is_true() and q.is_false()) else TruthValue.TRUE
        )
        result_statement = f"({p.statement}) → ({q.statement})"
        return Proposition(result_statement, result_value)

    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return truth table for IMPLIES operation."""
        return {(T, T): T, (T, F): F, (F, T): T, (F, F): T}

    def symbol(self) -> str:
        return "→"


class IffOperator(LogicalOperator):
    """
    Logical biconditional: P ↔ Q (P IF AND ONLY IF Q)

    The biconditional is true when both propositions have the same truth value.
    Read as "P if and only if Q" or "P iff Q".

    Truth Table:
        P | Q | P↔Q
        --|---|----
        T | T | T
        T | F | F
        F | T | F
        F | F | T

    Mathematical Use: Definitions ("A triangle is equilateral iff all sides are equal")
    Programming Use: Equality comparisons (==)
    """

    def apply(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply logical IFF to two propositions."""
        # P ↔ Q is equivalent to (P → Q) ∧ (Q → P)
        result_value = (
            TruthValue.TRUE if (p.truth_value == q.truth_value) else TruthValue.FALSE
        )
        result_statement = f"({p.statement}) ↔ ({q.statement})"
        return Proposition(result_statement, result_value)

    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return truth table for IFF operation."""
        return {(T, T): T, (T, F): F, (F, T): F, (F, F): T}

    def symbol(self) -> str:
        return "↔"


class XorOperator(LogicalOperator):
    """
    Exclusive OR: P ⊕ Q (P XOR Q)

    XOR is true when exactly one proposition is true (exclusive disjunction).

    Truth Table:
        P | Q | P⊕Q
        --|---|----
        T | T | F
        T | F | T
        F | T | T
        F | F | F

    Note: XOR is the negation of IFF (biconditional)

    Programming Use: Boolean toggle operations, parity checking
    Circuit Use: Half-adder circuits, error detection
    """

    def apply(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply logical XOR to two propositions."""
        result_value = (
            TruthValue.TRUE if (p.truth_value != q.truth_value) else TruthValue.FALSE
        )
        result_statement = f"({p.statement}) ⊕ ({q.statement})"
        return Proposition(result_statement, result_value)

    def truth_table(self) -> Dict[tuple, TruthValue]:
        """Return truth table for XOR operation."""
        return {(T, T): F, (T, F): T, (F, T): T, (F, F): F}

    def symbol(self) -> str:
        return "⊕"


# Operator instances for convenient use
NOT = NotOperator()
AND = AndOperator()
OR = OrOperator()
IMPLIES = ImpliesOperator()
IFF = IffOperator()
XOR = XorOperator()


class LogicalFormula:
    """
    Represents a complex logical formula built from propositions and operators.

    This class demonstrates how simple logical concepts can be composed
    into complex reasoning systems, mirroring how programming combines
    simple boolean operations into sophisticated logic.

    Examples:
        >>> p = Proposition("It's raining", True)
        >>> q = Proposition("Streets are wet", True)
        >>> r = Proposition("I have an umbrella", False)

        >>> # Create formula: (p → q) ∧ (p → r)
        >>> formula = LogicalFormula()
        >>> implication1 = formula.implies(p, q)
        >>> implication2 = formula.implies(p, r)
        >>> conclusion = formula.and_op(implication1, implication2)
    """

    def __init__(self):
        """Initialize an empty logical formula."""
        self.variables = {}  # Map variable names to propositions

    # Convenience methods that mirror the operators

    def not_op(self, p: Proposition) -> Proposition:
        """Apply NOT operator."""
        return NOT.apply(p)

    def and_op(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply AND operator."""
        return AND.apply(p, q)

    def or_op(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply OR operator."""
        return OR.apply(p, q)

    def implies(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply IMPLIES operator."""
        return IMPLIES.apply(p, q)

    def iff(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply IFF operator."""
        return IFF.apply(p, q)

    def xor(self, p: Proposition, q: Proposition) -> Proposition:
        """Apply XOR operator."""
        return XOR.apply(p, q)


def demonstrate_truth_tables():
    """
    Generate and display truth tables for all logical operators.

    This educational function helps students understand how each operator
    works by showing all possible input/output combinations.
    """
    print("Truth Tables for Logical Operators")
    print("=" * 40)

    operators = [NOT, AND, OR, IMPLIES, IFF, XOR]

    for op in operators:
        print(f"\n{op.__class__.__name__} ({op.symbol()}):")
        print("-" * 20)

        table = op.truth_table()

        if len(list(table.keys())[0]) == 1:  # Unary operator (NOT)
            print("P | ¬P")
            print("--|---")
            for inputs, output in table.items():
                print(f"{inputs[0]} | {output}")
        else:  # Binary operators
            symbol = op.symbol()
            print(f"P | Q | P{symbol}Q")
            print("--|---|----")
            for inputs, output in table.items():
                print(f"{inputs[0]} | {inputs[1]} | {output}")


def demonstrate_logical_equivalences():
    """
    Demonstrate important logical equivalences used in computer science.

    These equivalences are fundamental to:
    • Boolean algebra (circuit optimization)
    • Program optimization (short-circuit evaluation)
    • Formal verification (proof techniques)
    """
    print("\nLogical Equivalences")
    print("=" * 30)

    # Create test propositions
    p = Proposition("P", True)
    q = Proposition("Q", False)

    print(f"Using P = {p.truth_value}, Q = {q.truth_value}")
    print()

    # De Morgan's Laws
    print("De Morgan's Laws:")
    not_p_and_q = NOT.apply(AND.apply(p, q))
    not_p_or_not_q = OR.apply(NOT.apply(p), NOT.apply(q))
    print(f"¬(P ∧ Q) = {not_p_and_q.truth_value}")
    print(f"¬P ∨ ¬Q = {not_p_or_not_q.truth_value}")
    print(f"Equal? {not_p_and_q.truth_value == not_p_or_not_q.truth_value}")
    print()

    # Implication equivalence
    print("Implication Equivalence:")
    p_implies_q = IMPLIES.apply(p, q)
    not_p_or_q = OR.apply(NOT.apply(p), q)
    print(f"P → Q = {p_implies_q.truth_value}")
    print(f"¬P ∨ Q = {not_p_or_q.truth_value}")
    print(f"Equal? {p_implies_q.truth_value == not_p_or_q.truth_value}")
    print()

    # Double negation
    print("Double Negation:")
    double_neg_p = NOT.apply(NOT.apply(p))
    print(f"P = {p.truth_value}")
    print(f"¬¬P = {double_neg_p.truth_value}")
    print(f"Equal? {p.truth_value == double_neg_p.truth_value}")


def demonstrate_programming_applications():
    """
    Show how logical operators appear in everyday programming.

    This connects abstract mathematical logic to concrete programming
    examples that students encounter daily.
    """
    print("\nProgramming Applications")
    print("=" * 30)

    print("1. Input Validation:")
    age = 25
    has_license = True

    age_check = Proposition(f"age >= 18 (age={age})", age >= 18)
    license_check = Proposition("has_license", has_license)
    can_drive = AND.apply(age_check, license_check)

    print(f"   {age_check}")
    print(f"   {license_check}")
    print(f"   Can drive: {can_drive}")
    print("   Code: if age >= 18 and has_license: allow_driving()")
    print()

    print("2. Error Handling:")
    file_exists = Proposition("file_exists", False)
    readable = Proposition("file_readable", True)

    should_proceed = AND.apply(file_exists, readable)
    should_error = NOT.apply(should_proceed)

    print(f"   {file_exists}")
    print(f"   {readable}")
    print(f"   Should proceed: {should_proceed}")
    print(f"   Should show error: {should_error}")
    print("   Code: if not (file_exists and readable): show_error()")
    print()

    print("3. Loop Conditions:")
    counter = 5
    max_attempts = 3
    success = False

    more_attempts = Proposition(
        f"counter < max (counter={counter}, max={max_attempts})", counter < max_attempts
    )
    not_success = Proposition("not success", not success)
    continue_loop = AND.apply(more_attempts, not_success)

    print(f"   {more_attempts}")
    print(f"   {not_success}")
    print(f"   Continue loop: {continue_loop}")
    print("   Code: while counter < max_attempts and not success:")


# Educational demonstrations and utilities
def evaluate_formula_with_truth_values(formula_text: str, **variable_values) -> bool:
    """
    Evaluate a logical formula given truth values for variables.

    Args:
        formula_text: Description of the formula
        **variable_values: Truth values for variables (e.g., p=True, q=False)

    Returns:
        Boolean result of evaluating the formula

    Note:
        This is a simplified evaluator for educational purposes.
        Real implementations would parse complex logical expressions.
    """
    print(f"Evaluating: {formula_text}")
    for var, value in variable_values.items():
        print(f"  {var} = {value}")

    # This would need a real parser for complex formulas
    # For now, just demonstrate the concept
    return True


# Module constants for educational reference
PREREQUISITES = ["set_theory"]

LEARNING_OBJECTIVES = [
    "Understand propositions and truth values",
    "Apply logical operators (AND, OR, NOT, IMPLIES, IFF, XOR)",
    "Read and construct truth tables",
    "Recognize logical equivalences",
    "Connect logic to programming constructs",
]

BIG_O_COMPLEXITY = {
    "single_operation": "O(1)",
    "formula_evaluation": "O(n) where n is formula complexity",
    "truth_table_generation": "O(2^n) where n is number of variables",
}

COMMON_APPLICATIONS = [
    "Programming conditionals and boolean expressions",
    "Database query WHERE clauses",
    "Search engine boolean queries",
    "Digital circuit design",
    "Formal verification and theorem proving",
    "Artificial intelligence rule systems",
]

if __name__ == "__main__":
    # Run educational demonstrations
    demonstrate_truth_tables()
    demonstrate_logical_equivalences()
    demonstrate_programming_applications()

    print("\n" + "=" * 50)
    print("Interactive Examples:")
    print("Try creating your own logical formulas!")
    print("  from cs_atomic_concepts.foundations.logic import *")
    print("  p = Proposition('It is sunny', True)")
    print("  q = Proposition('I go swimming', False)")
    print("  implication = IMPLIES.apply(p, q)")
    print("  print(implication)")
