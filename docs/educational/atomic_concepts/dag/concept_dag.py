"""
Directed Acyclic Graph (DAG) Implementation for Educational Concept Dependencies

This module implements a complete DAG data structure from scratch, designed specifically
for modeling mathematical and computer science concept dependencies. Built with
mathematical rigor and educational purpose.

Mathematical Foundation:
- Graph G = (V, E) where V = concepts, E = dependency relationships
- Maintains acyclic invariant: ∀v ∈ V, v is not reachable from itself
- Supports topological ordering for valid learning sequences
- Provides transitive closure for complete dependency analysis

Educational Purpose:
- Demonstrates graph algorithms from first principles
- Shows mathematical proof of algorithmic correctness
- Provides foundation for adaptive learning systems
- Exhibits clean architecture and design patterns

Complexity Analysis:
- Add node: O(1)
- Add edge: O(V) for cycle detection
- Topological sort: O(V + E)
- Transitive closure: O(V³) using Floyd-Warshall
"""

from typing import Dict, Set, List, Optional, Iterator, Tuple, Any
from collections import defaultdict, deque
import json
from pathlib import Path

from .concept_node import ConceptNode
from .relationship_types import RelationshipType, DependencyStrength, RelationshipSpec


class CycleDetectedException(Exception):
    """
    Raised when attempting to add an edge that would create a cycle.

    Mathematical Significance:
    Preserves the DAG invariant that no concept can depend on itself,
    which would create impossible prerequisite chains.
    """

    def __init__(self, source: str, target: str, cycle_path: List[str]):
        self.source = source
        self.target = target
        self.cycle_path = cycle_path
        super().__init__(
            f"Adding edge {source} → {target} would create cycle: {' → '.join(cycle_path)}"
        )


class ConceptNotFoundException(Exception):
    """Raised when referencing a concept that doesn't exist in the DAG."""

    pass


class ConceptDAG:
    """
    Directed Acyclic Graph for modeling educational concept dependencies.

    Mathematical Properties:
    - Maintains acyclic invariant through cycle detection
    - Supports efficient topological ordering
    - Provides transitive closure computation
    - Enables shortest path analysis for learning sequences

    Educational Features:
    - Rich concept metadata for adaptive learning
    - Dependency strength weighting for curriculum design
    - Visualization export for interactive learning tools
    - Formal verification of graph properties
    """

    def __init__(self):
        """Initialize empty DAG with mathematical invariants."""
        # Core graph structure
        self._nodes: Dict[str, ConceptNode] = {}
        self._adjacency_list: Dict[str, Set[str]] = defaultdict(
            set
        )  # concept → dependents
        self._reverse_adjacency: Dict[str, Set[str]] = defaultdict(
            set
        )  # concept → prerequisites

        # Cached computations (invalidated on modification)
        self._topological_order: Optional[List[str]] = None
        self._transitive_closure: Optional[Dict[str, Set[str]]] = None

        # Graph statistics
        self._edge_count: int = 0

    def add_concept(self, concept: ConceptNode) -> None:
        """
        Add a concept node to the DAG.

        Mathematical Operation:
        Adds vertex v to graph G = (V, E), updating V = V ∪ {v}

        Args:
            concept: ConceptNode to add to the graph

        Raises:
            ValueError: If concept already exists with different definition
        """
        if concept.name in self._nodes:
            existing = self._nodes[concept.name]
            if existing != concept:
                raise ValueError(
                    f"Concept '{concept.name}' already exists with different definition"
                )
            return  # Idempotent operation

        self._nodes[concept.name] = concept
        self._adjacency_list[concept.name] = set()
        self._reverse_adjacency[concept.name] = set()

        # Invalidate cached computations
        self._invalidate_caches()

    def add_dependency(
        self,
        dependent: str,
        prerequisite: str,
        relationship_type: RelationshipType = RelationshipType.PREREQUISITE,
        strength: DependencyStrength = DependencyStrength.STRONG,
    ) -> None:
        """
        Add dependency edge with cycle detection.

        Mathematical Operation:
        Adds directed edge (prerequisite, dependent) to graph if it preserves acyclic property.

        Args:
            dependent: Concept that depends on prerequisite
            prerequisite: Concept that is required first
            relationship_type: Semantic type of dependency
            strength: How critical this dependency is

        Raises:
            ConceptNotFoundException: If either concept doesn't exist
            CycleDetectedException: If edge would create cycle
        """
        # Validate concepts exist
        if dependent not in self._nodes:
            raise ConceptNotFoundException(f"Dependent concept '{dependent}' not found")
        if prerequisite not in self._nodes:
            raise ConceptNotFoundException(
                f"Prerequisite concept '{prerequisite}' not found"
            )

        # Check for cycle before adding edge
        if self._would_create_cycle(prerequisite, dependent):
            cycle_path = self._find_cycle_path(prerequisite, dependent)
            raise CycleDetectedException(prerequisite, dependent, cycle_path)

        # Add edge to graph structure
        self._adjacency_list[prerequisite].add(dependent)
        self._reverse_adjacency[dependent].add(prerequisite)
        self._edge_count += 1

        # Update concept node with dependency metadata (create new immutable version)
        old_concept = self._nodes[dependent]
        new_prerequisites = old_concept.prerequisites | {prerequisite}
        new_metadata = old_concept.dependency_metadata.copy()
        new_metadata[prerequisite] = (relationship_type, strength)

        updated_concept = ConceptNode(
            name=old_concept.name,
            concept_id=old_concept.concept_id,
            type=old_concept.type,
            description=old_concept.description,
            mathematical_definition=old_concept.mathematical_definition,
            subject_area=old_concept.subject_area,
            complexity_level=old_concept.complexity_level,
            cognitive_load=old_concept.cognitive_load,
            prerequisites=frozenset(new_prerequisites),
            dependency_metadata=new_metadata,
            examples=old_concept.examples,
            common_misconceptions=old_concept.common_misconceptions,
            pedagogical_notes=old_concept.pedagogical_notes,
            learning_objectives=old_concept.learning_objectives,
            assessment_criteria=old_concept.assessment_criteria,
        )

        self._nodes[dependent] = updated_concept
        self._invalidate_caches()

    def _would_create_cycle(self, source: str, target: str) -> bool:
        """
        Check if adding edge source → target would create a cycle.

        Mathematical Algorithm:
        Uses DFS from target to see if source is reachable.
        If source is reachable from target, then target → source path exists,
        and adding source → target would create a cycle.

        Time Complexity: O(V + E)
        """
        if source == target:
            return True

        visited: Set[str] = set()
        stack = [target]

        while stack:
            current = stack.pop()
            if current == source:
                return True

            if current in visited:
                continue

            visited.add(current)
            # Add all nodes that current depends on (going backward in dependency chain)
            stack.extend(self._reverse_adjacency[current])

        return False

    def _find_cycle_path(self, source: str, target: str) -> List[str]:
        """
        Find the path that would create a cycle when adding source → target.

        Used for detailed error reporting when cycle detection fails.
        """
        # Find path from target back to source
        parent: Dict[str, Optional[str]] = {target: None}
        queue = deque([target])

        while queue:
            current = queue.popleft()

            for prerequisite in self._reverse_adjacency[current]:
                if prerequisite not in parent:
                    parent[prerequisite] = current
                    if prerequisite == source:
                        # Reconstruct path
                        path = [source]
                        node = current
                        while node is not None:
                            path.append(node)
                            node = parent[node]
                        path.append(target)  # Complete the cycle
                        return path
                    queue.append(prerequisite)

        return [source, target]  # Fallback if no path found

    def topological_sort(self) -> List[str]:
        """
        Compute topological ordering of concepts using Kahn's algorithm.

        Mathematical Guarantee:
        Returns ordering where for every dependency edge u → v,
        u appears before v in the ordering.

        Educational Use:
        Provides valid learning sequence respecting all prerequisites.

        Time Complexity: O(V + E)
        Space Complexity: O(V)

        Returns:
            List of concept names in topologically sorted order

        Raises:
            RuntimeError: If graph contains cycles (should never happen due to invariants)
        """
        if self._topological_order is not None:
            return self._topological_order.copy()

        # Kahn's Algorithm
        in_degree = {name: len(self._reverse_adjacency[name]) for name in self._nodes}
        queue = deque([name for name, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            # Remove current node and update in-degrees
            for dependent in self._adjacency_list[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Verify we processed all nodes (ensures no cycles)
        if len(result) != len(self._nodes):
            remaining = set(self._nodes.keys()) - set(result)
            raise RuntimeError(f"Cycle detected in DAG! Remaining nodes: {remaining}")

        self._topological_order = result
        return result.copy()

    def get_prerequisites(
        self, concept_name: str, transitive: bool = False
    ) -> Set[str]:
        """
        Get prerequisites for a concept.

        Args:
            concept_name: Name of the concept
            transitive: If True, returns all transitive prerequisites

        Returns:
            Set of prerequisite concept names
        """
        if concept_name not in self._nodes:
            raise ConceptNotFoundException(f"Concept '{concept_name}' not found")

        if not transitive:
            return self._reverse_adjacency[concept_name].copy()

        # Compute transitive closure if needed
        if self._transitive_closure is None:
            self._compute_transitive_closure()

        return self._transitive_closure[concept_name].copy()

    def get_dependents(self, concept_name: str, transitive: bool = False) -> Set[str]:
        """
        Get concepts that depend on the given concept.

        Args:
            concept_name: Name of the concept
            transitive: If True, returns all transitive dependents

        Returns:
            Set of dependent concept names
        """
        if concept_name not in self._nodes:
            raise ConceptNotFoundException(f"Concept '{concept_name}' not found")

        if not transitive:
            return self._adjacency_list[concept_name].copy()

        # For transitive dependents, we need reverse transitive closure
        if self._transitive_closure is None:
            self._compute_transitive_closure()

        transitive_dependents = set()
        for other_concept, other_prerequisites in self._transitive_closure.items():
            if concept_name in other_prerequisites:
                transitive_dependents.add(other_concept)

        return transitive_dependents

    def _compute_transitive_closure(self) -> None:
        """
        Compute transitive closure using Floyd-Warshall algorithm.

        Mathematical Definition:
        Transitive closure R* is the smallest transitive relation containing R.
        For concepts: if A depends on B and B depends on C, then A transitively depends on C.

        Time Complexity: O(V³)
        Space Complexity: O(V²)
        """
        concepts = list(self._nodes.keys())
        n = len(concepts)
        concept_to_index = {concept: i for i, concept in enumerate(concepts)}

        # Initialize adjacency matrix
        closure = [[False] * n for _ in range(n)]

        # Set direct dependencies
        for i, concept in enumerate(concepts):
            for prereq in self._reverse_adjacency[concept]:
                j = concept_to_index[prereq]
                closure[i][j] = True

        # Floyd-Warshall for transitive closure
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])

        # Convert back to concept names
        self._transitive_closure = {}
        for i, concept in enumerate(concepts):
            prerequisites = {concepts[j] for j in range(n) if closure[i][j]}
            self._transitive_closure[concept] = prerequisites

    def get_learning_path(self, target_concept: str) -> List[str]:
        """
        Get optimal learning path to master a target concept.

        Returns topologically sorted list of all prerequisites plus target.
        """
        if target_concept not in self._nodes:
            raise ConceptNotFoundException(
                f"Target concept '{target_concept}' not found"
            )

        all_prerequisites = self.get_prerequisites(target_concept, transitive=True)
        relevant_concepts = all_prerequisites | {target_concept}

        # Filter topological order to only include relevant concepts
        full_order = self.topological_sort()
        return [concept for concept in full_order if concept in relevant_concepts]

    def get_concept_by_complexity(self, complexity_level: str) -> List[ConceptNode]:
        """Get all concepts at a specific complexity level."""
        return [
            concept
            for concept in self._nodes.values()
            if concept.complexity_level == complexity_level
        ]

    def get_axioms(self) -> List[ConceptNode]:
        """Get all axiomatic concepts (no prerequisites)."""
        return [concept for concept in self._nodes.values() if concept.is_axiom]

    def _invalidate_caches(self) -> None:
        """Invalidate cached computations when graph is modified."""
        self._topological_order = None
        self._transitive_closure = None

    # Properties for mathematical analysis
    @property
    def node_count(self) -> int:
        """Number of vertices in the graph."""
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        """Number of edges in the graph."""
        return self._edge_count

    @property
    def density(self) -> float:
        """
        Graph density: ratio of actual edges to maximum possible edges.

        For directed graph: density = E / (V * (V-1))
        """
        if self.node_count <= 1:
            return 0.0
        max_edges = self.node_count * (self.node_count - 1)
        return self.edge_count / max_edges

    @property
    def concepts(self) -> Iterator[ConceptNode]:
        """Iterator over all concept nodes."""
        return iter(self._nodes.values())

    def __len__(self) -> int:
        """Number of concepts in the DAG."""
        return len(self._nodes)

    def __contains__(self, concept_name: str) -> bool:
        """Check if concept exists in DAG."""
        return concept_name in self._nodes

    def __getitem__(self, concept_name: str) -> ConceptNode:
        """Get concept by name."""
        if concept_name not in self._nodes:
            raise ConceptNotFoundException(f"Concept '{concept_name}' not found")
        return self._nodes[concept_name]

    def to_dict(self) -> Dict[str, Any]:
        """
        Export DAG to dictionary format for JSON serialization.

        Perfect for D3.js visualization integration.
        """
        return {
            "nodes": [concept.to_dict() for concept in self._nodes.values()],
            "edges": [
                {
                    "source": prereq,
                    "target": concept_name,
                    "relationship_type": (
                        str(self._nodes[concept_name].get_relationship_to(prereq)[0])
                        if self._nodes[concept_name].get_relationship_to(prereq)
                        else "prerequisite"
                    ),
                    "strength": (
                        float(self._nodes[concept_name].get_relationship_to(prereq)[1])
                        if self._nodes[concept_name].get_relationship_to(prereq)
                        else 0.8
                    ),
                }
                for concept_name, concept in self._nodes.items()
                for prereq in concept.prerequisites
            ],
            "metadata": {
                "node_count": self.node_count,
                "edge_count": self.edge_count,
                "density": self.density,
                "is_dag": True,  # Guaranteed by invariants
            },
        }

    def export_to_json(self, filepath: Path) -> None:
        """Export DAG to JSON file for external tools."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def __str__(self) -> str:
        """Human-readable DAG summary."""
        return f"ConceptDAG({self.node_count} concepts, {self.edge_count} dependencies)"

    def __repr__(self) -> str:
        """Detailed DAG representation."""
        return (
            f"ConceptDAG(nodes={self.node_count}, edges={self.edge_count}, "
            f"density={self.density:.3f})"
        )
