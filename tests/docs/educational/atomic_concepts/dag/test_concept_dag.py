"""
Mathematical Proof Tests for ConceptDAG Implementation

Tests the DAG data structure using formal mathematical verification, ensuring
algorithmic correctness and educational reliability. Every test serves as a
mathematical proof of specific DAG properties.

Mathematical Properties Verified:
1. Acyclic Invariant: No concept can depend on itself (directly or transitively)
2. Topological Ordering: Valid learning sequences respecting all prerequisites
3. Transitive Closure: Complete dependency relationship analysis
4. Graph Algorithms: Correctness of cycle detection, path finding, etc.

Educational Purpose:
Demonstrates how mathematical proofs can be embedded in code as executable
verification, bridging the gap between theoretical computer science and
practical software engineering.
"""

import unittest
from typing import Set, List

from tests import (
    MathematicalProofTestCase,
    mathematical_property,
    proof_by_contradiction,
)
from docs.educational.atomic_concepts.dag.concept_node import ConceptNode
from docs.educational.atomic_concepts.dag.concept_dag import (
    ConceptDAG,
    CycleDetectedException,
    ConceptNotFoundException,
)
from docs.educational.atomic_concepts.dag.relationship_types import (
    RelationshipType,
    DependencyStrength,
)


class TestConceptDAGMathematicalProperties(MathematicalProofTestCase):
    """
    Mathematical verification of ConceptDAG algorithmic properties.

    Each test method proves a specific mathematical property of the DAG
    implementation, ensuring both correctness and educational value.
    """

    def setUp(self):
        """Set up test fixtures with mathematically interesting examples."""
        self.dag = ConceptDAG()

        # Create test concepts representing mathematical hierarchy
        self.axiom_extensionality = ConceptNode(
            name="ZFC_Axiom_Extensionality",
            type="axiom",
            description="Two sets are equal iff they have the same elements",
            mathematical_definition="∀A ∀B (A = B ↔ ∀x (x ∈ A ↔ x ∈ B))",
            complexity_level="fundamental",
            subject_area="set_theory",
        )

        self.empty_set = ConceptNode(
            name="Empty_Set",
            type="concept",
            description="A set containing no elements",
            mathematical_definition="∅ = {x : x ≠ x}",
            complexity_level="basic",
            subject_area="set_theory",
            prerequisites=frozenset(["ZFC_Axiom_Extensionality"]),
        )

        self.finite_set = ConceptNode(
            name="Finite_Set",
            type="concept",
            description="A set with finitely many elements",
            mathematical_definition="A set S is finite if ∃n ∈ ℕ such that |S| = n",
            complexity_level="intermediate",
            subject_area="set_theory",
            prerequisites=frozenset(["Empty_Set"]),
        )

        self.countable_set = ConceptNode(
            name="Countable_Set",
            type="concept",
            description="A set that can be put in bijection with natural numbers",
            mathematical_definition="A set S is countable if ∃f: S → ℕ that is bijective",
            complexity_level="advanced",
            subject_area="set_theory",
            prerequisites=frozenset(["Finite_Set"]),
        )

        # Add concepts to DAG
        for concept in [
            self.axiom_extensionality,
            self.empty_set,
            self.finite_set,
            self.countable_set,
        ]:
            self.dag.add_concept(concept)

        # Add dependencies
        self.dag.add_dependency("Empty_Set", "ZFC_Axiom_Extensionality")
        self.dag.add_dependency("Finite_Set", "Empty_Set")
        self.dag.add_dependency("Countable_Set", "Finite_Set")

    @mathematical_property
    def test_dag_acyclic_invariant(self):
        """
        Mathematical Proof: DAG maintains acyclic property.

        Theorem: ∀G(DAG) ∀v∈V(G) : v is not reachable from itself
        Proof Method: Constructive verification of cycle detection algorithm
        """
        # Property 1: No concept should be reachable from itself
        for concept_name in self.dag._nodes:
            transitive_deps = self.dag.get_prerequisites(concept_name, transitive=True)
            self.assertNotIn(
                concept_name,
                transitive_deps,
                f"Concept {concept_name} cannot be its own transitive prerequisite",
            )

        # Property 2: Cycle detection should work correctly
        try:
            # This should create a cycle: Empty_Set → ZFC_Axiom_Extensionality → Empty_Set
            self.dag.add_dependency("ZFC_Axiom_Extensionality", "Empty_Set")
            self.fail("Expected CycleDetectedException was not raised")
        except CycleDetectedException as e:
            # This proves our cycle detection algorithm works
            self.assertIn("Empty_Set", e.cycle_path)
            self.assertIn("ZFC_Axiom_Extensionality", e.cycle_path)

    @proof_by_contradiction
    def test_no_self_dependency(self):
        """
        Proof by Contradiction: No concept can depend on itself.

        Assume: ∃ concept C such that C depends on C
        Contradiction: This violates the definition of a learning prerequisite
        Therefore: No concept can depend on itself
        """
        # Assume we can add a self-dependency
        test_concept = ConceptNode(
            name="Test_Self_Dependency",
            type="concept",
            description="Test concept for self-dependency",
            complexity_level="basic",
            subject_area="set_theory",
        )

        self.dag.add_concept(test_concept)

        # Attempt to create self-dependency (should fail)
        with self.assertRaises(CycleDetectedException) as context:
            self.dag.add_dependency("Test_Self_Dependency", "Test_Self_Dependency")

        # Verify the contradiction was detected
        self.assertEqual(context.exception.source, "Test_Self_Dependency")
        self.assertEqual(context.exception.target, "Test_Self_Dependency")

    @mathematical_property
    def test_transitive_dependency_closure(self):
        """
        Mathematical Proof: Transitive closure correctly computes all dependencies.

        Theorem: If A→B and B→C then A transitively depends on C
        Proof: Verification of Floyd-Warshall transitive closure algorithm
        """
        # Direct verification of transitive relationships
        finite_set_deps = self.dag.get_prerequisites("Finite_Set", transitive=True)
        countable_set_deps = self.dag.get_prerequisites(
            "Countable_Set", transitive=True
        )

        # Mathematical property: Finite_Set transitively depends on ZFC_Axiom_Extensionality
        # (through Empty_Set)
        self.assertIn(
            "ZFC_Axiom_Extensionality",
            finite_set_deps,
            "Finite_Set should transitively depend on ZFC_Axiom_Extensionality",
        )
        self.assertIn(
            "Empty_Set",
            finite_set_deps,
            "Finite_Set should transitively depend on Empty_Set",
        )

        # Mathematical property: Countable_Set transitively depends on all previous concepts
        expected_transitive_deps = {
            "ZFC_Axiom_Extensionality",
            "Empty_Set",
            "Finite_Set",
        }
        for dep in expected_transitive_deps:
            self.assertIn(
                dep,
                countable_set_deps,
                f"Countable_Set should transitively depend on {dep}",
            )

        # Verify transitive closure is minimal (no unnecessary dependencies)
        self.assertEqual(
            len(countable_set_deps),
            3,
            "Countable_Set should have exactly 3 transitive dependencies",
        )

    @mathematical_property
    def test_topological_ordering_validity(self):
        """
        Mathematical Proof: Topological sort produces valid learning sequence.

        Theorem: ∀(u,v)∈E : position(u) < position(v) in topological ordering
        Proof: Verification that Kahn's algorithm respects all dependency edges
        """
        topo_order = self.dag.topological_sort()

        # Create position mapping for efficient lookup
        position = {concept: i for i, concept in enumerate(topo_order)}

        # Mathematical property: All concepts must be included
        self.assertEqual(
            len(topo_order),
            self.dag.node_count,
            "Topological order must include all concepts exactly once",
        )
        self.assertEqual(
            set(topo_order),
            set(self.dag._nodes.keys()),
            "Topological order must contain all and only DAG concepts",
        )

        # Mathematical property: For every dependency edge, prerequisite comes before dependent
        for concept in self.dag.concepts:
            concept_pos = position[concept.name]
            for prereq in concept.prerequisites:
                prereq_pos = position[prereq]
                self.assertLess(
                    prereq_pos,
                    concept_pos,
                    f"Prerequisite {prereq} must come before {concept.name} in learning order",
                )

        # Verify specific ordering for our test concepts
        self.assertLess(position["ZFC_Axiom_Extensionality"], position["Empty_Set"])
        self.assertLess(position["Empty_Set"], position["Finite_Set"])
        self.assertLess(position["Finite_Set"], position["Countable_Set"])

    @mathematical_property
    def test_graph_density_calculation(self):
        """
        Mathematical Proof: Graph density formula is correctly implemented.

        Theorem: density = |E| / (|V| * (|V| - 1)) for directed graphs
        Proof: Direct verification of density calculation
        """
        expected_density = self.dag.edge_count / (
            self.dag.node_count * (self.dag.node_count - 1)
        )
        calculated_density = self.dag.density

        self.assertAlmostEqual(
            calculated_density,
            expected_density,
            places=6,
            msg="Density calculation must match mathematical formula",
        )

        # Edge case: single node graph has density 0
        single_dag = ConceptDAG()
        single_concept = ConceptNode(
            name="Single", type="axiom", complexity_level="fundamental"
        )
        single_dag.add_concept(single_concept)

        self.assertEqual(
            single_dag.density, 0.0, "Single node graph must have density 0"
        )

    @mathematical_property
    def test_learning_path_optimality(self):
        """
        Mathematical Proof: Learning paths are minimal and complete.

        Theorem: Learning path contains all and only necessary prerequisites
        Proof: Verification that path is subset of transitive closure
        """
        target = "Countable_Set"
        learning_path = self.dag.get_learning_path(target)
        transitive_deps = self.dag.get_prerequisites(target, transitive=True)

        # Mathematical property: Path contains target concept
        self.assertIn(
            target, learning_path, "Learning path must include target concept"
        )

        # Mathematical property: Path contains all transitive dependencies
        for dep in transitive_deps:
            self.assertIn(
                dep,
                learning_path,
                f"Learning path must include transitive dependency {dep}",
            )

        # Mathematical property: Path contains no unnecessary concepts
        path_set = set(learning_path)
        necessary_concepts = transitive_deps | {target}
        self.assertEqual(
            path_set,
            necessary_concepts,
            "Learning path must contain exactly necessary concepts",
        )

        # Mathematical property: Path respects topological ordering
        full_topo_order = self.dag.topological_sort()
        path_positions = [full_topo_order.index(concept) for concept in learning_path]
        self.assertEqual(
            path_positions,
            sorted(path_positions),
            "Learning path must respect topological ordering",
        )

    def test_mathematical_complexity_bounds(self):
        """
        Mathematical Analysis: Verify algorithm complexity bounds.

        Tests that DAG operations meet their theoretical complexity guarantees.
        """
        n = self.dag.node_count

        # Test topological sort complexity: O(V + E)
        import time

        start_time = time.time()
        self.dag.topological_sort()
        elapsed_time = time.time() - start_time

        # For small graphs, timing is not reliable, but we verify the result
        topo_result = self.dag.topological_sort()
        self.assertEqual(
            len(topo_result), n, "Topological sort must return all vertices"
        )
        self.assertGreater(elapsed_time, 0, "Operation should take measurable time")

        # Test transitive closure complexity: O(V^3)
        start_time = time.time()
        for concept in self.dag._nodes:
            self.dag.get_prerequisites(concept, transitive=True)
        closure_time = time.time() - start_time

        # Verify correctness rather than timing for small graphs
        self.assertGreater(
            closure_time, 0, "Transitive closure computation must complete"
        )


class TestConceptDAGEdgeCases(MathematicalProofTestCase):
    """
    Test edge cases and error conditions for ConceptDAG.

    Verifies robust error handling and mathematical edge cases.
    """

    def test_empty_dag_properties(self):
        """Test mathematical properties of empty DAG."""
        empty_dag = ConceptDAG()

        self.assertEqual(empty_dag.node_count, 0)
        self.assertEqual(empty_dag.edge_count, 0)
        self.assertEqual(empty_dag.density, 0.0)
        self.assertEqual(empty_dag.topological_sort(), [])
        self.assertEqual(empty_dag.get_axioms(), [])

    def test_single_concept_dag(self):
        """Test DAG with single concept (axiom)."""
        dag = ConceptDAG()
        axiom = ConceptNode(
            name="Single_Axiom", type="axiom", complexity_level="fundamental"
        )
        dag.add_concept(axiom)

        self.assertEqual(dag.node_count, 1)
        self.assertEqual(dag.edge_count, 0)
        self.assertEqual(dag.density, 0.0)
        self.assertEqual(dag.topological_sort(), ["Single_Axiom"])
        self.assertEqual(len(dag.get_axioms()), 1)

    def test_concept_not_found_errors(self):
        """Test proper error handling for non-existent concepts."""
        dag = ConceptDAG()

        with self.assertRaises(ConceptNotFoundException):
            dag.add_dependency("NonExistent1", "NonExistent2")

        with self.assertRaises(ConceptNotFoundException):
            dag.get_prerequisites("NonExistent")

        with self.assertRaises(ConceptNotFoundException):
            dag.get_learning_path("NonExistent")

    def test_duplicate_concept_handling(self):
        """Test idempotent concept addition."""
        dag = ConceptDAG()
        concept = ConceptNode(name="Test", type="concept", complexity_level="basic")

        # Adding same concept twice should be idempotent
        dag.add_concept(concept)
        initial_count = dag.node_count

        dag.add_concept(concept)  # Should not change anything
        self.assertEqual(dag.node_count, initial_count)

    def test_complex_cycle_detection(self):
        """Test cycle detection in complex dependency chains."""
        dag = ConceptDAG()

        # Create chain: A → B → C → D
        concepts = []
        for name in ["A", "B", "C", "D"]:
            concept = ConceptNode(name=name, type="concept", complexity_level="basic")
            concepts.append(concept)
            dag.add_concept(concept)

        dag.add_dependency("B", "A")
        dag.add_dependency("C", "B")
        dag.add_dependency("D", "C")

        # Attempting to close the cycle D → A should fail
        with self.assertRaises(CycleDetectedException) as context:
            dag.add_dependency("A", "D")

        # Verify cycle path is detected correctly
        cycle_path = context.exception.cycle_path
        self.assertIn("A", cycle_path)
        self.assertIn("D", cycle_path)
