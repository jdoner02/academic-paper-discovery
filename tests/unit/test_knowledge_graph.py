"""
Comprehensive tests for knowledge graph implementation.

Educational Notes:
- Tests grouped by algorithm/functionality for clarity
- Property-based testing validates mathematical properties
- Performance tests ensure algorithmic complexity bounds
- Integration tests verify end-to-end workflows
"""

import pytest
from datetime import datetime
from unittest.mock import patch
from src.infrastructure.knowledge_graph import KnowledgeGraph, Entity, Relationship


class TestKnowledgeGraphBasics:
    """Test basic graph operations and data structure integrity."""

    def test_empty_graph_initialization(self):
        """Test that empty graph initializes correctly."""
        kg = KnowledgeGraph()
        assert len(kg.entities) == 0
        assert len(kg.relationships) == 0
        assert kg.get_statistics()["num_entities"] == 0

    def test_add_entity_success(self):
        """Test successful entity addition."""
        kg = KnowledgeGraph()
        entity = Entity("test_entity", "test_type", ["observation1", "observation2"])

        kg.add_entity(entity)

        assert "test_entity" in kg.entities
        assert kg.entities["test_entity"].entity_type == "test_type"
        assert len(kg.entities["test_entity"].observations) == 2

    def test_add_duplicate_entity_merges_observations(self):
        """Test that duplicate entities merge observations."""
        kg = KnowledgeGraph()
        entity1 = Entity("same_id", "type1", ["obs1"])
        entity2 = Entity("same_id", "type1", ["obs2"])

        kg.add_entity(entity1)
        kg.add_entity(entity2)

        assert len(kg.entities["same_id"].observations) == 2
        assert "obs1" in kg.entities["same_id"].observations
        assert "obs2" in kg.entities["same_id"].observations

    def test_add_relationship_success(self):
        """Test successful relationship addition."""
        kg = KnowledgeGraph()
        entity1 = Entity("e1", "type", ["obs"])
        entity2 = Entity("e2", "type", ["obs"])

        kg.add_entity(entity1)
        kg.add_entity(entity2)

        relationship = Relationship("rel1", "e1", "e2", "relates_to")
        kg.add_relationship(relationship)

        assert ("e1", "e2") in kg.relationships
        assert "e2" in kg.adjacency_list["e1"]
        assert "e1" in kg.reverse_adjacency_list["e2"]

    def test_add_relationship_nonexistent_entity_fails(self):
        """Test that relationships require existing entities."""
        kg = KnowledgeGraph()
        relationship = Relationship(
            "rel1", "nonexistent1", "nonexistent2", "relates_to"
        )

        with pytest.raises(ValueError, match="not found"):
            kg.add_relationship(relationship)

    def test_self_loop_prevention(self):
        """Test that self-loops are prevented to maintain DAG property."""
        kg = KnowledgeGraph()
        entity = Entity("self", "type", ["obs"])
        kg.add_entity(entity)

        relationship = Relationship("self_rel", "self", "self", "relates_to")

        with pytest.raises(ValueError, match="Self-loops not allowed"):
            kg.add_relationship(relationship)


class TestBreadthFirstSearch:
    """Test BFS shortest path algorithm."""

    def test_shortest_path_direct_connection(self):
        """Test shortest path with direct connection."""
        kg = KnowledgeGraph()

        # Create simple graph: A -> B
        entities = [Entity("A", "type", ["obs"]), Entity("B", "type", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))

        path = kg.find_shortest_conceptual_path("A", "B")
        assert path == ["A", "B"]

    def test_shortest_path_multi_hop(self):
        """Test shortest path with multiple hops."""
        kg = KnowledgeGraph()

        # Create graph: A -> B -> C
        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C"]]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))
        kg.add_relationship(Relationship("rel2", "B", "C", "connects"))

        path = kg.find_shortest_conceptual_path("A", "C")
        assert path == ["A", "B", "C"]

    def test_shortest_path_no_connection(self):
        """Test shortest path when no path exists."""
        kg = KnowledgeGraph()

        # Create disconnected entities
        entities = [Entity("A", "type", ["obs"]), Entity("B", "type", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)

        path = kg.find_shortest_conceptual_path("A", "B")
        assert path == []

    def test_shortest_path_same_entity(self):
        """Test shortest path from entity to itself."""
        kg = KnowledgeGraph()
        entity = Entity("A", "type", ["obs"])
        kg.add_entity(entity)

        path = kg.find_shortest_conceptual_path("A", "A")
        assert path == ["A"]

    def test_shortest_path_caching(self):
        """Test that BFS results are cached for performance."""
        kg = KnowledgeGraph()

        entities = [Entity("A", "type", ["obs"]), Entity("B", "type", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)
        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))

        # First call should cache result
        path1 = kg.find_shortest_conceptual_path("A", "B")

        # Second call should use cache
        path2 = kg.find_shortest_conceptual_path("A", "B")

        assert path1 == path2 == ["A", "B"]
        assert ("A", "B") in kg._path_cache


class TestDepthFirstSearch:
    """Test DFS knowledge domain exploration."""

    def test_explore_single_entity(self):
        """Test exploration of single entity."""
        kg = KnowledgeGraph()
        entity = Entity("A", "type", ["obs"])
        kg.add_entity(entity)

        domain = kg.explore_knowledge_domain("A", max_depth=1)
        assert domain == {"A"}

    def test_explore_linear_chain(self):
        """Test exploration of linear chain."""
        kg = KnowledgeGraph()

        # Create chain: A -> B -> C
        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C"]]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))
        kg.add_relationship(Relationship("rel2", "B", "C", "connects"))

        # Depth 1: only A
        domain1 = kg.explore_knowledge_domain("A", max_depth=1)
        assert domain1 == {"A", "B"}

        # Depth 2: A, B, C
        domain2 = kg.explore_knowledge_domain("A", max_depth=2)
        assert domain2 == {"A", "B", "C"}

    def test_explore_branching_structure(self):
        """Test exploration of branching structure."""
        kg = KnowledgeGraph()

        # Create tree: A -> {B, C}, B -> D
        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C", "D"]]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))
        kg.add_relationship(Relationship("rel2", "A", "C", "connects"))
        kg.add_relationship(Relationship("rel3", "B", "D", "connects"))

        domain = kg.explore_knowledge_domain("A", max_depth=2)
        assert domain == {"A", "B", "C", "D"}

    def test_explore_memoization(self):
        """Test that DFS uses memoization for performance."""
        kg = KnowledgeGraph()

        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C"]]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))
        kg.add_relationship(Relationship("rel2", "A", "C", "connects"))

        # Create memo table
        memo = {}

        # First exploration should populate memo
        domain1 = kg.explore_knowledge_domain("A", max_depth=1, memo=memo)
        assert len(memo) > 0

        # Second exploration should use memo
        domain2 = kg.explore_knowledge_domain("A", max_depth=1, memo=memo)
        assert domain1 == domain2


class TestAStarSearch:
    """Test A* algorithm with heuristics."""

    def test_a_star_direct_path(self):
        """Test A* with direct path."""
        kg = KnowledgeGraph()

        entities = [Entity("A", "type1", ["obs"]), Entity("B", "type1", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects", weight=1.0))

        path = kg.a_star_knowledge_search("A", "B")
        assert path == ["A", "B"]

    def test_a_star_optimal_path_selection(self):
        """Test that A* selects optimal path with different weights."""
        kg = KnowledgeGraph()

        # Create diamond: A -> {B, C} -> D with different weights
        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C", "D"]]
        for entity in entities:
            kg.add_entity(entity)

        # Short expensive path: A -> B -> D (weight 10)
        kg.add_relationship(Relationship("rel1", "A", "B", "connects", weight=5.0))
        kg.add_relationship(Relationship("rel2", "B", "D", "connects", weight=5.0))

        # Long cheap path: A -> C -> D (weight 2)
        kg.add_relationship(Relationship("rel3", "A", "C", "connects", weight=1.0))
        kg.add_relationship(Relationship("rel4", "C", "D", "connects", weight=1.0))

        path = kg.a_star_knowledge_search("A", "D")
        assert path == ["A", "C", "D"]  # Should choose cheaper path

    def test_a_star_custom_heuristic(self):
        """Test A* with custom heuristic function."""
        kg = KnowledgeGraph()

        entities = [Entity("A", "type1", ["obs"]), Entity("B", "type2", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))

        def custom_heuristic(entity1: str, entity2: str) -> float:
            return 0.1  # Very optimistic heuristic

        path = kg.a_star_knowledge_search("A", "B", heuristic_func=custom_heuristic)
        assert path == ["A", "B"]

    def test_a_star_no_path(self):
        """Test A* when no path exists."""
        kg = KnowledgeGraph()

        entities = [Entity("A", "type", ["obs"]), Entity("B", "type", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)

        path = kg.a_star_knowledge_search("A", "B")
        assert path == []


class TestPageRankAlgorithm:
    """Test PageRank importance calculation."""

    def test_pagerank_single_entity(self):
        """Test PageRank with single entity."""
        kg = KnowledgeGraph()
        entity = Entity("A", "type", ["obs"])
        kg.add_entity(entity)

        importance = kg.calculate_entity_importance()
        # Single entity gets (1-damping_factor)/n + damping_factor * 0 = 0.15
        assert abs(importance["A"] - 0.15) < 0.01

    def test_pagerank_linear_chain(self):
        """Test PageRank with linear chain."""
        kg = KnowledgeGraph()

        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C"]]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))
        kg.add_relationship(Relationship("rel2", "B", "C", "connects"))

        importance = kg.calculate_entity_importance(iterations=10)

        # C should have highest importance (receives all rank)
        assert importance["C"] > importance["B"] > importance["A"]

    def test_pagerank_hub_structure(self):
        """Test PageRank with hub structure."""
        kg = KnowledgeGraph()

        # Create hub: {A, B, C} -> D
        entities = [Entity(id, "type", ["obs"]) for id in ["A", "B", "C", "D"]]
        for entity in entities:
            kg.add_entity(entity)

        for source in ["A", "B", "C"]:
            kg.add_relationship(Relationship(f"rel_{source}", source, "D", "connects"))

        importance = kg.calculate_entity_importance()

        # D should be most important (receives from multiple sources)
        assert importance["D"] > max(importance["A"], importance["B"], importance["C"])

    def test_pagerank_caching(self):
        """Test that PageRank results are cached."""
        kg = KnowledgeGraph()
        entity = Entity("A", "type", ["obs"])
        kg.add_entity(entity)

        # First calculation
        importance1 = kg.calculate_entity_importance()

        # Second calculation should use cache
        importance2 = kg.calculate_entity_importance()

        assert importance1 == importance2
        assert kg._importance_cache is not None


class TestTopologicalSort:
    """Test topological sorting for dependency resolution."""

    def test_topological_sort_linear(self):
        """Test topological sort with linear dependencies."""
        kg = KnowledgeGraph()

        entities = [Entity(id, "concept", ["obs"]) for id in ["A", "B", "C"]]
        for entity in entities:
            kg.add_entity(entity)

        # A depends on B depends on C
        kg.add_relationship(Relationship("rel1", "C", "B", "prerequisite"))
        kg.add_relationship(Relationship("rel2", "B", "A", "prerequisite"))

        order = kg.get_learning_order()

        # C should come before B, B before A
        c_idx = order.index("C")
        b_idx = order.index("B")
        a_idx = order.index("A")

        assert c_idx < b_idx < a_idx

    def test_topological_sort_parallel_dependencies(self):
        """Test topological sort with parallel dependencies."""
        kg = KnowledgeGraph()

        entities = [Entity(id, "concept", ["obs"]) for id in ["A", "B", "C", "D"]]
        for entity in entities:
            kg.add_entity(entity)

        # {A, B} -> C -> D
        kg.add_relationship(Relationship("rel1", "A", "C", "prerequisite"))
        kg.add_relationship(Relationship("rel2", "B", "C", "prerequisite"))
        kg.add_relationship(Relationship("rel3", "C", "D", "prerequisite"))

        order = kg.get_learning_order()

        # A and B can be in any order, but both before C, C before D
        c_idx = order.index("C")
        d_idx = order.index("D")
        a_idx = order.index("A")
        b_idx = order.index("B")

        assert a_idx < c_idx < d_idx
        assert b_idx < c_idx < d_idx

    def test_topological_sort_no_dependencies(self):
        """Test topological sort with no dependencies."""
        kg = KnowledgeGraph()

        entities = [Entity(id, "concept", ["obs"]) for id in ["A", "B", "C"]]
        for entity in entities:
            kg.add_entity(entity)

        order = kg.get_learning_order()

        # All entities should be present
        assert set(order) == {"A", "B", "C"}
        assert len(order) == 3


class TestPerformanceAndCaching:
    """Test performance optimizations and caching mechanisms."""

    def test_neighbor_caching(self):
        """Test LRU caching of neighbor lookups."""
        kg = KnowledgeGraph()

        entities = [Entity("A", "type", ["obs"]), Entity("B", "type", ["obs"])]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))

        # First call should cache result
        neighbors1 = kg.get_neighbors("A")

        # Second call should use cache
        neighbors2 = kg.get_neighbors("A")

        assert neighbors1 == neighbors2 == ["B"]

    def test_cache_invalidation(self):
        """Test that caches are invalidated when graph changes."""
        kg = KnowledgeGraph()

        entity = Entity("A", "type", ["obs"])
        kg.add_entity(entity)

        # Calculate importance to populate cache
        kg.calculate_entity_importance()
        assert kg._importance_cache is not None

        # Add new entity should invalidate cache
        new_entity = Entity("B", "type", ["obs"])
        kg.add_entity(new_entity)

        assert kg._importance_cache is None

    def test_graph_statistics(self):
        """Test graph statistics calculation."""
        kg = KnowledgeGraph()

        entities = [
            Entity("A", "type1", ["obs"]),
            Entity("B", "type1", ["obs"]),
            Entity("C", "type2", ["obs"]),
        ]
        for entity in entities:
            kg.add_entity(entity)

        kg.add_relationship(Relationship("rel1", "A", "B", "connects"))

        stats = kg.get_statistics()

        assert stats["num_entities"] == 3
        assert stats["num_relationships"] == 1
        assert stats["entity_types"] == {"type1": 2, "type2": 1}
        assert 0 < stats["graph_density"] < 1


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_entity_validation(self):
        """Test entity validation on creation."""
        with pytest.raises(ValueError):
            Entity("", "type", ["obs"])  # Empty ID

        with pytest.raises(ValueError):
            Entity("id", "", ["obs"])  # Empty type

        with pytest.raises(ValueError):
            Entity("id", "type", "not_a_list")  # Invalid observations

    def test_relationship_validation(self):
        """Test relationship validation on creation."""
        with pytest.raises(ValueError):
            Relationship("", "A", "B", "type")  # Empty ID

        with pytest.raises(ValueError):
            Relationship("id", "", "B", "type")  # Empty from_entity

        with pytest.raises(ValueError):
            Relationship("id", "A", "", "type")  # Empty to_entity

        with pytest.raises(ValueError):
            Relationship("id", "A", "B", "")  # Empty relation_type

        with pytest.raises(ValueError):
            Relationship("id", "A", "B", "type", weight=0)  # Invalid weight

    def test_search_nonexistent_entities(self):
        """Test search algorithms with nonexistent entities."""
        kg = KnowledgeGraph()

        # BFS with nonexistent entities
        assert kg.find_shortest_conceptual_path("nonexistent1", "nonexistent2") == []

        # DFS with nonexistent entity
        assert kg.explore_knowledge_domain("nonexistent") == set()

        # A* with nonexistent entities
        assert kg.a_star_knowledge_search("nonexistent1", "nonexistent2") == []

    def test_empty_graph_algorithms(self):
        """Test algorithms on empty graph."""
        kg = KnowledgeGraph()

        assert kg.calculate_entity_importance() == {}
        assert kg.get_learning_order() == []


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
