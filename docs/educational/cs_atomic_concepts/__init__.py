"""
Computer Science Atomic Concepts Educational Library

A comprehensive Python library where each file represents a single, atomic computer science concept.
The folder structure itself demonstrates object-oriented programming relationships through
inheritance (IS-A), composition (HAS-A), and aggregation (USES-A) patterns.

Educational Philosophy:
    "Every concept should be understandable in isolation, yet show its connections to the whole."

Library Structure Demonstrates OOP Principles:
    📁 foundations/         - Base mathematical concepts (inheritance roots)
    📁 abstractions/        - Abstract base classes and interfaces
    📁 concrete_structures/ - Concrete implementations (IS-A relationships)
        📁 linear/          - Sequential access patterns
        📁 trees/           - Hierarchical structures
        📁 graphs/          - Network structures
    📁 algorithms/          - Computational procedures
    📁 design_patterns/     - Reusable software solutions

Learning Progression (Pedagogical Sequence):
    1. Mathematical Foundations → Abstract Concepts → Concrete Structures
    2. Individual Data Structures → Algorithms That Use Them
    3. Simple Patterns → Complex System Design

Each Module Provides:
    ✓ Mathematical definition from first principles
    ✓ Runnable Python implementation with examples
    ✓ Performance analysis and Big-O characteristics
    ✓ Common use cases and real-world applications
    ✓ Relationship demonstrations with other concepts
    ✓ Test suite validating core properties
    ✓ Common misconceptions and debugging tips

Integration with Research Framework:
    This library integrates with the academic paper discovery system,
    allowing students to see how theoretical CS concepts apply to
    real research problems and implementations.

Usage Examples:
    >>> from cs_atomic_concepts.foundations import set_theory
    >>> from cs_atomic_concepts.concrete_structures.linear import stack
    >>> from cs_atomic_concepts.algorithms import sorting

    >>> # See mathematical foundations
    >>> universe = set_theory.UniversalSet(['a', 'b', 'c', 'd'])
    >>> subset_a = universe.subset(['a', 'b'])
    >>> subset_b = universe.subset(['b', 'c'])
    >>> print(subset_a.union(subset_b))  # Demonstrates set operations

    >>> # See data structure implementation
    >>> call_stack = stack.Stack(implementation='linked_list')
    >>> call_stack.push('main()')
    >>> call_stack.push('calculate()')
    >>> print(call_stack.peek())  # 'calculate()'

    >>> # See algorithm application
    >>> numbers = [64, 34, 25, 12, 22, 11, 90]
    >>> sorted_numbers = sorting.merge_sort(numbers)
    >>> print(f"Sorted: {sorted_numbers}")

Author: Jessica Doner
Institution: Eastern Washington University
Course Applications: CSCD 210, CSCD 211, CSCD 320, CSCD 350
License: MIT (Educational Use)
Version: 1.0.0 - Foundational Implementation

Educational Standards Alignment:
    - AP Computer Science A: All data structures and algorithms
    - AP Computer Science Principles: Computational thinking practices
    - ACM Computer Science Curricula: CS1, CS2, and DS&A requirements
    - Pacific Northwest Tech Industry: Practical skills for career preparation
"""

from typing import Dict, List, Set, Any, Optional
import sys
import importlib
from pathlib import Path

__version__ = "1.0.0"
__author__ = "Jessica Doner"
__institution__ = "Eastern Washington University"

# Educational metadata for the entire library
LIBRARY_METADATA = {
    "concepts_count": 0,  # Will be populated by discovery
    "learning_objectives": [
        "Understand fundamental mathematical foundations of computer science",
        "Implement and analyze core data structures from first principles",
        "Apply algorithmic thinking to solve computational problems",
        "Recognize and implement common design patterns",
        "Understand performance characteristics and trade-offs",
        "Connect theoretical concepts to practical applications",
    ],
    "skill_progression": [
        "Novice: Understands basic concepts and can follow examples",
        "Developing: Can implement simple versions with guidance",
        "Proficient: Independently implements and analyzes concepts",
        "Advanced: Optimizes implementations and handles edge cases",
        "Mastered: Teaches others and creates novel applications",
    ],
    "course_alignment": {
        "CSCD_210": ["foundations", "concrete_structures/linear"],
        "CSCD_211": ["concrete_structures/trees", "algorithms/sorting"],
        "CSCD_320": ["algorithms/graph", "design_patterns"],
        "CSCD_350": ["algorithms/advanced", "computational_theory"],
    },
}


def discover_concepts() -> Dict[str, List[str]]:
    """
    Automatically discover all available concepts in the library.

    Returns:
        Dictionary mapping categories to lists of available concepts.

    Educational Value:
        Demonstrates dynamic module discovery and reflection - advanced Python concepts
        that show how libraries can be self-documenting and extensible.
    """
    concepts = {}
    library_root = Path(__file__).parent

    for category_path in library_root.iterdir():
        if category_path.is_dir() and not category_path.name.startswith("__"):
            category_name = category_path.name
            concepts[category_name] = []

            # Recursively find all Python files
            for python_file in category_path.rglob("*.py"):
                if not python_file.name.startswith("__"):
                    # Convert path to import name
                    relative_path = python_file.relative_to(library_root)
                    concept_name = (
                        str(relative_path).replace("/", ".").replace(".py", "")
                    )
                    concepts[category_name].append(concept_name)

    return concepts


def get_concept_dependencies(concept_name: str) -> List[str]:
    """
    Analyze a concept's dependencies to suggest learning order.

    Args:
        concept_name: Name of concept to analyze (e.g., 'concrete_structures.linear.stack')

    Returns:
        List of prerequisite concepts that should be learned first.

    Educational Value:
        Shows how to build dependency graphs for learning optimization -
        connects to graph theory and topological sorting concepts.
    """
    try:
        # Dynamic import to inspect dependencies
        module = importlib.import_module(f"cs_atomic_concepts.{concept_name}")

        # Look for explicitly declared dependencies
        if hasattr(module, "PREREQUISITES"):
            return module.PREREQUISITES

        # Analyze imports as implicit dependencies
        dependencies = []
        if hasattr(module, "__file__"):
            # This is a simplified version - real implementation would parse AST
            pass

        return dependencies
    except ImportError:
        return []


def create_learning_path(target_concept: str) -> List[str]:
    """
    Generate optimal learning path to understand a target concept.

    Args:
        target_concept: The concept you want to learn

    Returns:
        Ordered list of concepts to study, from foundations to target.

    Educational Value:
        Demonstrates practical application of graph algorithms (topological sort)
        to educational optimization - theory applied to real problems.
    """
    # Implementation would use topological sorting on dependency graph
    # For now, provide basic progression

    foundations = ["foundations.set_theory", "foundations.logic"]
    abstractions = ["abstractions.data_structure", "abstractions.algorithm"]

    if "linear" in target_concept:
        return foundations + abstractions + [target_concept]
    elif "trees" in target_concept:
        return (
            foundations
            + abstractions
            + ["concrete_structures.linear.array"]
            + [target_concept]
        )
    else:
        return foundations + [target_concept]


def demonstrate_concept_relationships() -> str:
    """
    Generate a visual representation of how concepts relate to each other.

    Returns:
        String representation showing inheritance and composition relationships.

    Educational Value:
        Shows meta-programming techniques and demonstrates how code can be
        self-documenting and generate its own educational materials.
    """
    relationship_map = """
    CS Atomic Concepts - Relationship Diagram
    ========================================
    
    Mathematical Foundations (IS-A hierarchy root):
    ├── Set Theory → Logic → Functions → Relations
    └── Graph Theory → Tree Theory → Linear Structures
    
    Abstract Concepts (Interface definitions):
    ├── DataStructure (abstract base class)
    │   ├── LinearStructure (IS-A DataStructure)
    │   ├── TreeStructure (IS-A DataStructure)  
    │   └── GraphStructure (IS-A DataStructure)
    └── Algorithm (abstract base class)
        ├── SortingAlgorithm (IS-A Algorithm)
        ├── SearchAlgorithm (IS-A Algorithm)
        └── GraphAlgorithm (IS-A Algorithm)
    
    Concrete Implementations (Demonstrates all relationship types):
    ├── Array (IS-A LinearStructure)
    ├── LinkedList (IS-A LinearStructure)
    ├── Stack (IS-A LinearStructure, HAS-A Array|LinkedList)
    ├── Queue (IS-A LinearStructure, HAS-A CircularBuffer)
    ├── BinaryTree (IS-A TreeStructure, HAS-A Node)
    ├── Heap (IS-A BinaryTree, USES-A ComparisonFunction)
    └── Graph (IS-A GraphStructure, HAS-A AdjacencyList, USES-A VertexSet)
    
    Legend:
    IS-A    = Inheritance (Liskov substitution principle)
    HAS-A   = Composition (ownership relationship)
    USES-A  = Aggregation (dependency relationship)
    """
    return relationship_map


# Auto-discovery on import
_available_concepts = discover_concepts()
LIBRARY_METADATA["concepts_count"] = sum(
    len(concepts) for concepts in _available_concepts.values()
)

# Export key functions for educational use
__all__ = [
    "discover_concepts",
    "get_concept_dependencies",
    "create_learning_path",
    "demonstrate_concept_relationships",
    "LIBRARY_METADATA",
]

if __name__ == "__main__":
    print("Computer Science Atomic Concepts Library")
    print("=" * 50)
    print(f"Version: {__version__}")
    print(f"Total concepts available: {LIBRARY_METADATA['concepts_count']}")
    print("\nConcept categories:")

    for category, concepts in _available_concepts.items():
        print(f"  📁 {category}: {len(concepts)} concepts")

    print("\nRelationship demonstration:")
    print(demonstrate_concept_relationships())

    print("\nTo get started:")
    print("  from cs_atomic_concepts.foundations import set_theory")
    print("  help(set_theory)")
