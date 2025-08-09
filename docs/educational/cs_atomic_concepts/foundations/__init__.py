"""
Mathematical Foundations of Computer Science

This package contains the fundamental mathematical concepts that underlie
all computer science data structures, algorithms, and computational thinking.

Educational Philosophy:
    "Before we can build computational structures, we must understand
     the mathematical foundations upon which they rest."

Package Contents:
    📁 set_theory.py       - Sets as collections of distinct elements
    📁 logic.py           - Boolean logic and propositional calculus
    📁 relations.py       - Mathematical relations and their properties
    📁 functions.py       - Mathematical functions and mappings
    📁 graph_theory.py    - Graphs, vertices, edges, and connectivity
    📁 number_theory.py   - Numbers, arithmetic, and mathematical proofs

Learning Sequence:
    The concepts in this package build upon each other in a specific order
    designed for maximum pedagogical value:

    1. set_theory    → Everything starts with collections of objects
    2. logic         → Rules for reasoning about sets and membership
    3. relations     → How sets can be related to each other
    4. functions     → Special relations with unique mappings
    5. graph_theory  → Sets with connectivity structure
    6. number_theory → Discrete mathematics for algorithm analysis

Real-World Connection:
    These mathematical foundations appear everywhere in computer science:
    • Databases use set theory (SQL operations)
    • Programming uses logic (if statements, boolean expressions)
    • Data structures use relations (parent-child in trees)
    • Algorithms use functions (input → output mappings)
    • Networks use graph theory (routing, social networks)
    • Cryptography uses number theory (RSA, prime numbers)

Course Alignment:
    CSCD 210: set_theory, logic, relations
    CSCD 211: functions, graph_theory basics
    CSCD 320: advanced graph_theory, number_theory
    MATH 161: All concepts with formal mathematical rigor

Prerequisites:
    High school algebra and basic logical reasoning.
    No prior programming experience required.

Author: Jessica Doner
Institution: Eastern Washington University
"""

from .set_theory import (
    FiniteSet,
    SetTheoryException,
    empty_set,
    universal_set,
    singleton_set,
    demonstrate_set_properties,
)

# Package metadata
__all__ = [
    # Core classes
    "FiniteSet",
    "SetTheoryException",
    # Factory functions
    "empty_set",
    "universal_set",
    "singleton_set",
    # Educational demonstrations
    "demonstrate_set_properties",
    # Package information
    "FOUNDATIONS_CONCEPTS",
    "LEARNING_SEQUENCE",
    "get_concept_info",
]

# Educational metadata for the entire foundations package
FOUNDATIONS_CONCEPTS = {
    "set_theory": {
        "description": "Collections of distinct elements with operations",
        "prerequisites": [],
        "applications": ["Database operations", "Data deduplication", "Logic"],
        "complexity": "Beginner",
        "status": "Complete",
    },
    "logic": {
        "description": "Boolean reasoning and propositional calculus",
        "prerequisites": ["set_theory"],
        "applications": ["Programming conditionals", "Circuit design", "Proofs"],
        "complexity": "Beginner",
        "status": "Planned",
    },
    "relations": {
        "description": "How mathematical objects relate to each other",
        "prerequisites": ["set_theory", "logic"],
        "applications": ["Database relationships", "Tree structures", "Equivalence"],
        "complexity": "Intermediate",
        "status": "Planned",
    },
    "functions": {
        "description": "Mappings between sets with unique outputs",
        "prerequisites": ["set_theory", "relations"],
        "applications": ["Algorithms", "Hash functions", "Data transformations"],
        "complexity": "Intermediate",
        "status": "Planned",
    },
    "graph_theory": {
        "description": "Networks of vertices connected by edges",
        "prerequisites": ["set_theory", "relations"],
        "applications": ["Social networks", "Routing algorithms", "Dependencies"],
        "complexity": "Advanced",
        "status": "Planned",
    },
    "number_theory": {
        "description": "Properties of integers and mathematical proofs",
        "prerequisites": ["logic", "functions"],
        "applications": ["Cryptography", "Algorithm analysis", "Optimization"],
        "complexity": "Advanced",
        "status": "Planned",
    },
}

LEARNING_SEQUENCE = [
    "set_theory",  # Foundation: collections and membership
    "logic",  # Reasoning: true/false and logical operations
    "relations",  # Connections: how objects relate
    "functions",  # Mappings: special relations with unique outputs
    "graph_theory",  # Networks: connected structures
    "number_theory",  # Analysis: mathematical properties for algorithms
]


def get_concept_info(concept_name: str) -> dict:
    """
    Get detailed information about a foundational concept.

    Args:
        concept_name: Name of the concept (e.g., 'set_theory')

    Returns:
        Dictionary with concept metadata including description,
        prerequisites, applications, and learning resources.

    Examples:
        >>> info = get_concept_info('set_theory')
        >>> print(info['description'])
        'Collections of distinct elements with operations'
        >>> print(info['prerequisites'])
        []
    """
    if concept_name not in FOUNDATIONS_CONCEPTS:
        available = ", ".join(FOUNDATIONS_CONCEPTS.keys())
        raise ValueError(f"Unknown concept '{concept_name}'. Available: {available}")

    return FOUNDATIONS_CONCEPTS[concept_name].copy()


def get_learning_path(target_concept: str) -> list:
    """
    Get the optimal learning path to understand a target concept.

    Args:
        target_concept: The concept you want to learn

    Returns:
        List of concepts to study in order, ending with target concept.

    Examples:
        >>> path = get_learning_path('functions')
        >>> print(path)
        ['set_theory', 'logic', 'relations', 'functions']
    """
    if target_concept not in FOUNDATIONS_CONCEPTS:
        available = ", ".join(FOUNDATIONS_CONCEPTS.keys())
        raise ValueError(f"Unknown concept '{target_concept}'. Available: {available}")

    # Build dependency graph and return topological order
    visited = set()
    path = []

    def visit(concept):
        if concept in visited:
            return
        visited.add(concept)

        # Visit prerequisites first
        for prereq in FOUNDATIONS_CONCEPTS[concept]["prerequisites"]:
            visit(prereq)

        path.append(concept)

    visit(target_concept)
    return path


def demonstrate_foundations():
    """
    Comprehensive demonstration of mathematical foundations concepts.

    This function shows how the foundational concepts work together
    and provides examples of their applications in computer science.
    """
    print("Mathematical Foundations of Computer Science")
    print("=" * 50)
    print()

    print("Available Concepts:")
    for i, concept in enumerate(LEARNING_SEQUENCE, 1):
        info = FOUNDATIONS_CONCEPTS[concept]
        status_symbol = "✅" if info["status"] == "Complete" else "⏳"
        print(f"{i}. {status_symbol} {concept} ({info['complexity']})")
        print(f"   {info['description']}")
        if info["prerequisites"]:
            prereqs = ", ".join(info["prerequisites"])
            print(f"   Prerequisites: {prereqs}")
        print()

    print("Learning Path Examples:")
    for concept in ["functions", "graph_theory"]:
        if FOUNDATIONS_CONCEPTS[concept]["status"] != "Complete":
            path = get_learning_path(concept)
            print(f"To learn {concept}: {' → '.join(path)}")

    print()
    print("Set Theory Demonstration (Currently Available):")
    print("-" * 30)
    demonstrate_set_properties()


if __name__ == "__main__":
    demonstrate_foundations()
