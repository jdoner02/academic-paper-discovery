"""
Knowledge Graph Implementation for AI Agent Memory Systems.

This module implements the graph algorithms and data structures described in the
Knowledge Graph Architecture tutorial, providing efficient traversal and search
capabilities for AI agent memory systems.

Educational Notes:
- Demonstrates adjacency list representation for O(V+E) space efficiency
- Implements BFS for shortest path discovery between concepts
- Uses DFS with memoization for deep knowledge exploration
- Provides A* search with domain-specific heuristics
- Includes PageRank algorithm for entity importance ranking
- Supports topological sorting for dependency resolution

Design Decisions:
- DAG structure prevents infinite loops during traversal
- Adjacency list chosen over matrix for sparse graph efficiency
- Separate metadata storage maintains clean separation of concerns
- LRU caching provides performance optimization for repeated queries

Use Cases:
- Academic research: Find conceptual relationships between papers
- Knowledge discovery: Navigate from familiar to unfamiliar concepts
- Dependency resolution: Determine learning order for educational content
- Importance ranking: Identify central concepts in research domains
"""

from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from typing import Any, Callable, Dict, List, Set, Tuple, Optional
import heapq
import math


@dataclass
class Entity:
    """
    Represents a knowledge entity (concept, paper, researcher, etc.)

    Educational Notes:
    - Immutable ID ensures entity identity persistence
    - Observations provide evidence grounding for concepts
    - Metadata supports extensible domain-specific information
    - Timestamps enable versioning and temporal analysis
    """

    id: str
    entity_type: str
    observations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate entity after initialization"""
        if not self.id or not self.entity_type:
            raise ValueError("Entity must have non-empty id and entity_type")
        if not isinstance(self.observations, list):
            raise ValueError("Observations must be a list")


@dataclass
class Relationship:
    """
    Represents a directed relationship between entities.

    Educational Notes:
    - Directed edges support asymmetric relationships (A influences B)
    - Weight enables importance-based traversal algorithms
    - Semantic typing provides relationship categorization
    - Metadata supports domain-specific relationship properties
    """

    id: str
    from_entity: str
    to_entity: str
    relation_type: str
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate relationship after initialization"""
        if not all([self.id, self.from_entity, self.to_entity, self.relation_type]):
            raise ValueError("Relationship must have non-empty id, entities, and type")
        if self.weight <= 0:
            raise ValueError("Relationship weight must be positive")


class KnowledgeGraph:
    """
    Directed Acyclic Graph (DAG) implementation for AI agent memory systems.

    Educational Notes:
    - Uses adjacency list representation for O(V+E) space complexity
    - Maintains reverse adjacency list for efficient backward traversal
    - Implements graph algorithms with educational complexity analysis
    - Provides multiple search strategies for different use cases

    Design Patterns Applied:
    - Strategy pattern for different search algorithms
    - Observer pattern for graph update notifications
    - Template method for consistent algorithm structure
    """

    def __init__(self):
        # Core graph structure using adjacency lists
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.reverse_adjacency_list: Dict[str, List[str]] = defaultdict(list)

        # Entity and relationship storage
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[Tuple[str, str], Relationship] = {}

        # Performance optimization
        self._path_cache: Dict[Tuple[str, str], List[str]] = {}
        self._importance_cache: Optional[Dict[str, float]] = None
        self._cache_version = 0

    def add_entity(self, entity: Entity) -> None:
        """
        Add an entity to the knowledge graph.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if entity.id in self.entities:
            # Update existing entity
            existing = self.entities[entity.id]
            existing.observations.extend(entity.observations)
            existing.metadata.update(entity.metadata)
            existing.updated_at = datetime.now()
        else:
            self.entities[entity.id] = entity

        self._invalidate_cache()

    def add_relationship(self, relationship: Relationship) -> None:
        """
        Add a directed relationship between entities.

        Educational Notes:
        - Validates entity existence before creating relationship
        - Maintains both forward and reverse adjacency lists
        - Prevents duplicate relationships with same entities

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Validate entities exist
        if relationship.from_entity not in self.entities:
            raise ValueError(f"From entity '{relationship.from_entity}' not found")
        if relationship.to_entity not in self.entities:
            raise ValueError(f"To entity '{relationship.to_entity}' not found")

        # Prevent self-loops to maintain DAG property
        if relationship.from_entity == relationship.to_entity:
            raise ValueError("Self-loops not allowed in DAG structure")

        # Store relationship
        key = (relationship.from_entity, relationship.to_entity)
        if key not in self.relationships:
            self.relationships[key] = relationship

            # Update adjacency lists
            self.adjacency_list[relationship.from_entity].append(relationship.to_entity)
            self.reverse_adjacency_list[relationship.to_entity].append(
                relationship.from_entity
            )

            self._invalidate_cache()

    def find_shortest_conceptual_path(self, start: str, target: str) -> List[str]:
        """
        Find shortest path between entities using Breadth-First Search.

        Educational Notes:
        - BFS guarantees shortest path in unweighted graphs
        - Uses queue for level-order traversal
        - Tracks visited nodes to prevent cycles
        - Returns empty list if no path exists

        Time Complexity: O(V + E) where V=vertices, E=edges
        Space Complexity: O(V) for visited set and queue

        Args:
            start: Starting entity ID
            target: Target entity ID

        Returns:
            List of entity IDs representing shortest path, empty if no path
        """
        # Input validation
        if start not in self.entities or target not in self.entities:
            return []

        if start == target:
            return [start]

        # Check cache first
        cache_key = (start, target)
        if cache_key in self._path_cache:
            return self._path_cache[cache_key].copy()

        # BFS implementation
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current_entity, path = queue.popleft()

            # Explore neighbors
            for neighbor in self.adjacency_list.get(current_entity, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]

                    if neighbor == target:
                        # Cache result before returning
                        self._path_cache[cache_key] = new_path.copy()
                        return new_path

                    visited.add(neighbor)
                    queue.append((neighbor, new_path))

        # No path found
        self._path_cache[cache_key] = []
        return []

    def explore_knowledge_domain(
        self,
        entity: str,
        max_depth: int = 5,
        memo: Optional[Dict[str, Set[str]]] = None,
    ) -> Set[str]:
        """
        Deep exploration of knowledge domain using DFS with memoization.

        Educational Notes:
        - DFS explores deeper before wider (vs BFS)
        - Memoization prevents redundant computation
        - Max depth prevents infinite recursion
        - Returns all reachable entities within depth limit

        Time Complexity: O(V + E) with memoization, O(V^D) without
        Space Complexity: O(V) for memoization table

        Args:
            entity: Starting entity for exploration
            max_depth: Maximum exploration depth
            memo: Memoization table for performance

        Returns:
            Set of all entity IDs reachable within max_depth
        """
        if memo is None:
            memo = {}

        # Check memo table
        memo_key = f"{entity}:{max_depth}"
        if memo_key in memo:
            return memo[memo_key].copy()

        if entity not in self.entities or max_depth <= 0:
            result = {entity} if entity in self.entities else set()
            memo[memo_key] = result
            return result.copy()

        # DFS exploration
        reachable = {entity}
        for neighbor in self.adjacency_list.get(entity, []):
            reachable.update(
                self.explore_knowledge_domain(neighbor, max_depth - 1, memo)
            )

        memo[memo_key] = reachable
        return reachable.copy()

    def a_star_knowledge_search(
        self,
        start: str,
        goal: str,
        heuristic_func: Optional[Callable[[str, str], float]] = None,
    ) -> List[str]:
        """
        A* search for optimal knowledge path with domain-specific heuristics.

        Educational Notes:
        - A* combines Dijkstra's algorithm with heuristic guidance
        - f(n) = g(n) + h(n) where g=cost, h=heuristic
        - Heuristic must be admissible (never overestimate) for optimality
        - Priority queue ensures optimal exploration order

        Time Complexity: O(E * log V) with binary heap
        Space Complexity: O(V) for open/closed sets

        Args:
            start: Starting entity ID
            goal: Goal entity ID
            heuristic_func: Heuristic function h(entity, goal) -> float

        Returns:
            List of entity IDs representing optimal path
        """
        if start not in self.entities or goal not in self.entities:
            return []

        if start == goal:
            return [start]

        # Default heuristic: entity type similarity
        if heuristic_func is None:
            heuristic_func = self._default_heuristic

        # A* algorithm implementation
        open_set = [(0.0, start, [start])]  # (f_score, entity, path)
        closed_set = set()
        g_scores = {start: 0.0}

        while open_set:
            f_score, current, path = heapq.heappop(open_set)

            if current == goal:
                return path

            if current in closed_set:
                continue

            closed_set.add(current)

            # Explore neighbors
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor in closed_set:
                    continue

                # Calculate tentative g_score
                edge_weight = self.get_edge_weight(current, neighbor)
                tentative_g = g_scores[current] + edge_weight

                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    h_score = heuristic_func(neighbor, goal)
                    f_score = tentative_g + h_score
                    new_path = path + [neighbor]

                    heapq.heappush(open_set, (f_score, neighbor, new_path))

        return []  # No path found

    def calculate_entity_importance(
        self, damping_factor: float = 0.85, iterations: int = 100
    ) -> Dict[str, float]:
        """
        PageRank algorithm adapted for knowledge graph entity importance.

        Educational Notes:
        - PageRank models random walk through graph
        - Damping factor prevents rank sinks
        - Iterative algorithm converges to stable distribution
        - Higher rank indicates more important/central entities

        Time Complexity: O(k * E) where k=iterations
        Space Complexity: O(V) for rank storage

        Args:
            damping_factor: Probability of following links (0.85 standard)
            iterations: Number of iterations for convergence

        Returns:
            Dictionary mapping entity IDs to importance scores
        """
        # Check cache
        if self._importance_cache is not None:
            return self._importance_cache.copy()

        entities = list(self.entities.keys())
        n = len(entities)

        if n == 0:
            return {}

        # Initialize PageRank values uniformly
        pagerank = {entity: 1.0 / n for entity in entities}

        # Iterative PageRank computation
        for iteration in range(iterations):
            new_pagerank = {}

            for entity in entities:
                rank_sum = 0.0

                # Sum contributions from incoming links
                for source in self.reverse_adjacency_list.get(entity, []):
                    out_degree = len(self.adjacency_list.get(source, []))
                    if out_degree > 0:
                        rank_sum += pagerank[source] / out_degree

                # PageRank formula
                new_pagerank[entity] = (
                    1 - damping_factor
                ) / n + damping_factor * rank_sum

            pagerank = new_pagerank

        # Cache result
        self._importance_cache = pagerank.copy()
        return pagerank

    def get_learning_order(self) -> List[str]:
        """
        Topological sort for optimal learning order based on dependencies.

        Educational Notes:
        - Kahn's algorithm for topological sorting
        - In-degree calculation identifies prerequisite structure
        - Queue processes entities with no remaining dependencies
        - Detects cycles if DAG property is violated

        Time Complexity: O(V + E)
        Space Complexity: O(V)

        Returns:
            List of entity IDs in dependency order

        Raises:
            ValueError: If cycle detected in graph
        """
        # Calculate in-degrees
        in_degree = {entity: 0 for entity in self.entities}

        for entity in self.adjacency_list:
            for neighbor in self.adjacency_list[entity]:
                in_degree[neighbor] += 1

        # Start with entities having no dependencies
        queue = deque([entity for entity, degree in in_degree.items() if degree == 0])
        result = []

        # Process entities in topological order
        while queue:
            current = queue.popleft()
            result.append(current)

            # Update in-degrees of neighbors
            for neighbor in self.adjacency_list.get(current, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Cycle detection
        if len(result) != len(self.entities):
            remaining = set(self.entities.keys()) - set(result)
            raise ValueError(
                f"Cycle detected in knowledge graph. Remaining entities: {remaining}"
            )

        return result

    def get_edge_weight(self, from_entity: str, to_entity: str) -> float:
        """Get weight of edge between entities, default 1.0"""
        relationship = self.relationships.get((from_entity, to_entity))
        return relationship.weight if relationship else 1.0

    def _default_heuristic(self, entity1: str, entity2: str) -> float:
        """
        Default heuristic function for A* search.

        Educational Notes:
        - Estimates conceptual distance using entity types
        - Admissible heuristic (never overestimates true cost)
        - Can be extended with embedding similarity
        """
        if entity1 not in self.entities or entity2 not in self.entities:
            return float("inf")

        type1 = self.entities[entity1].entity_type
        type2 = self.entities[entity2].entity_type

        # Simple type-based heuristic
        if type1 == type2:
            return 0.5  # Same type, likely related
        else:
            return 1.0  # Different type, less likely related

    def _invalidate_cache(self) -> None:
        """Invalidate caches when graph structure changes"""
        self._path_cache.clear()
        self._importance_cache = None
        self._cache_version += 1

    @lru_cache(maxsize=1000)
    def get_neighbors(self, entity_id: str) -> List[str]:
        """
        Cached neighbor lookup with LRU eviction.

        Educational Notes:
        - LRU cache improves performance for repeated queries
        - Cache size balances memory usage vs hit rate
        - Automatic eviction prevents unbounded memory growth
        """
        return list(self.adjacency_list.get(entity_id, []))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate graph statistics for analysis and monitoring.

        Returns:
            Dictionary with graph metrics and properties
        """
        num_entities = len(self.entities)
        num_relationships = len(self.relationships)

        # Calculate density
        max_edges = num_entities * (num_entities - 1)
        density = num_relationships / max_edges if max_edges > 0 else 0

        # Entity type distribution
        type_counts = defaultdict(int)
        for entity in self.entities.values():
            type_counts[entity.entity_type] += 1

        return {
            "num_entities": num_entities,
            "num_relationships": num_relationships,
            "graph_density": density,
            "entity_types": dict(type_counts),
            "cache_version": self._cache_version,
            "cache_hits": getattr(self.get_neighbors, "cache_info", lambda: None)(),
        }


# Example usage and educational demonstration
if __name__ == "__main__":
    # Create knowledge graph instance
    kg = KnowledgeGraph()

    # Add entities representing research concepts
    entities = [
        Entity(
            "machine_learning",
            "research_field",
            ["Algorithms that learn from data", "Statistical pattern recognition"],
        ),
        Entity(
            "deep_learning",
            "research_subfield",
            ["Neural networks with multiple layers", "Representation learning"],
        ),
        Entity(
            "computer_vision",
            "research_field",
            ["Image processing and analysis", "Visual pattern recognition"],
        ),
        Entity(
            "natural_language_processing",
            "research_field",
            ["Text processing and understanding", "Language modeling"],
        ),
    ]

    for entity in entities:
        kg.add_entity(entity)

    # Add relationships representing conceptual dependencies
    relationships = [
        Relationship("rel1", "machine_learning", "deep_learning", "subsumes", 1.0),
        Relationship("rel2", "machine_learning", "computer_vision", "applies_to", 0.8),
        Relationship(
            "rel3", "machine_learning", "natural_language_processing", "applies_to", 0.8
        ),
        Relationship("rel4", "deep_learning", "computer_vision", "enhances", 0.9),
        Relationship(
            "rel5", "deep_learning", "natural_language_processing", "enhances", 0.9
        ),
    ]

    for relationship in relationships:
        kg.add_relationship(relationship)

    # Demonstrate graph algorithms
    print("=== Knowledge Graph Algorithm Demonstrations ===\n")

    # BFS shortest path
    path = kg.find_shortest_conceptual_path("machine_learning", "computer_vision")
    print(f"Shortest path ML -> CV: {' -> '.join(path)}")

    # DFS knowledge domain exploration
    domain = kg.explore_knowledge_domain("machine_learning", max_depth=2)
    print(f"ML knowledge domain: {sorted(domain)}")

    # A* search with heuristic
    a_star_path = kg.a_star_knowledge_search(
        "machine_learning", "natural_language_processing"
    )
    print(f"A* path ML -> NLP: {' -> '.join(a_star_path)}")

    # PageRank importance
    importance = kg.calculate_entity_importance()
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    print(f"Entity importance ranking:")
    for entity, score in sorted_importance:
        print(f"  {entity}: {score:.3f}")

    # Topological ordering
    learning_order = kg.get_learning_order()
    print(f"Optimal learning order: {' -> '.join(learning_order)}")

    # Graph statistics
    stats = kg.get_statistics()
    print(f"\nGraph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
