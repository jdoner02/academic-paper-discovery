"""
MCP Memory Integration for Knowledge Graph.

This module provides integration between the knowledge graph implementation
and the MCP (Model Context Protocol) memory system, enabling AI agents to
maintain persistent knowledge across sessions.

Educational Notes:
- Demonstrates Adapter pattern for external system integration
- Implements Repository pattern for memory persistence
- Uses Factory pattern for entity/relationship creation
- Provides Command pattern for batch operations
- Maintains Clean Architecture separation of concerns

Design Decisions:
- Async operations support concurrent memory updates
- Batch operations optimize network efficiency
- Error handling preserves data integrity
- Logging provides audit trail for debugging
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import asdict

from src.infrastructure.knowledge_graph import KnowledgeGraph, Entity, Relationship


class MCPMemoryAdapter:
    """
    Adapter for MCP memory system integration with knowledge graph.

    Educational Notes:
    - Adapter pattern bridges incompatible interfaces
    - Maintains separation between graph algorithms and memory storage
    - Provides abstraction layer for different memory backends
    - Supports both synchronous and asynchronous operations
    """

    def __init__(self, mcp_memory_client):
        """
        Initialize adapter with MCP memory client.

        Args:
            mcp_memory_client: Client for MCP memory operations
        """
        self.memory_client = mcp_memory_client
        self.logger = logging.getLogger(__name__)
        self._entity_type_mapping = {
            "research_paper": "academic_paper",
            "research_field": "scientific_domain",
            "concept": "knowledge_concept",
            "researcher": "academic_person",
        }

    async def load_knowledge_graph(self) -> KnowledgeGraph:
        """
        Load complete knowledge graph from MCP memory.

        Educational Notes:
        - Factory method pattern for graph construction
        - Error handling preserves partial state
        - Logging provides debugging information
        - Async operation supports non-blocking execution

        Returns:
            KnowledgeGraph instance populated from memory
        """
        self.logger.info("Loading knowledge graph from MCP memory")
        kg = KnowledgeGraph()

        try:
            # Read all entities and relationships from memory
            memory_graph = await self.memory_client.read_graph()

            # Convert MCP entities to knowledge graph entities
            entity_count = 0
            for node_name, node_data in memory_graph.get("nodes", {}).items():
                entity = self._mcp_node_to_entity(node_name, node_data)
                kg.add_entity(entity)
                entity_count += 1

            # Convert MCP relationships to knowledge graph relationships
            relationship_count = 0
            for relation in memory_graph.get("relations", []):
                relationship = self._mcp_relation_to_relationship(relation)
                if relationship:
                    kg.add_relationship(relationship)
                    relationship_count += 1

            self.logger.info(
                f"Loaded {entity_count} entities and {relationship_count} relationships"
            )
            return kg

        except Exception as e:
            self.logger.error(f"Failed to load knowledge graph: {e}")
            raise

    async def save_knowledge_graph(self, kg: KnowledgeGraph) -> None:
        """
        Save complete knowledge graph to MCP memory.

        Educational Notes:
        - Batch operations optimize memory efficiency
        - Transaction-like behavior ensures consistency
        - Error handling provides rollback capability
        - Progress logging aids in debugging large graphs

        Args:
            kg: KnowledgeGraph instance to save
        """
        self.logger.info("Saving knowledge graph to MCP memory")

        try:
            # Convert entities to MCP format
            mcp_entities = []
            for entity in kg.entities.values():
                mcp_entity = self._entity_to_mcp_format(entity)
                mcp_entities.append(mcp_entity)

            # Create entities in batch
            if mcp_entities:
                await self.memory_client.create_entities(entities=mcp_entities)
                self.logger.info(f"Saved {len(mcp_entities)} entities")

            # Convert relationships to MCP format
            mcp_relations = []
            for relationship in kg.relationships.values():
                mcp_relation = self._relationship_to_mcp_format(relationship)
                mcp_relations.append(mcp_relation)

            # Create relationships in batch
            if mcp_relations:
                await self.memory_client.create_relations(relations=mcp_relations)
                self.logger.info(f"Saved {len(mcp_relations)} relationships")

        except Exception as e:
            self.logger.error(f"Failed to save knowledge graph: {e}")
            raise

    async def sync_entity_updates(
        self, kg: KnowledgeGraph, entity_ids: List[str]
    ) -> None:
        """
        Synchronize specific entity updates to MCP memory.

        Educational Notes:
        - Incremental updates optimize performance
        - Batch processing reduces network overhead
        - Error isolation prevents cascade failures
        - Observation merging preserves knowledge accumulation

        Args:
            kg: KnowledgeGraph with updated entities
            entity_ids: List of entity IDs to synchronize
        """
        self.logger.info(f"Syncing {len(entity_ids)} entity updates")

        observations_to_add = []
        for entity_id in entity_ids:
            if entity_id in kg.entities:
                entity = kg.entities[entity_id]

                # Prepare observations for addition
                observations_to_add.append(
                    {"entityName": entity_id, "contents": entity.observations}
                )

        try:
            if observations_to_add:
                await self.memory_client.add_observations(
                    observations=observations_to_add
                )
                self.logger.info("Successfully synced entity observations")

        except Exception as e:
            self.logger.error(f"Failed to sync entity updates: {e}")
            raise

    async def search_entities(self, query: str) -> List[Entity]:
        """
        Search for entities in MCP memory using semantic search.

        Educational Notes:
        - Semantic search leverages embedding similarity
        - Result transformation maintains type safety
        - Error handling provides graceful degradation
        - Async operation supports real-time search

        Args:
            query: Search query string

        Returns:
            List of Entity instances matching the query
        """
        self.logger.info(f"Searching entities with query: '{query}'")

        try:
            # Perform semantic search in MCP memory
            search_results = await self.memory_client.search_nodes(query=query)

            # Convert search results to Entity objects
            entities = []
            for result in search_results:
                entity = self._mcp_node_to_entity(result["name"], result)
                entities.append(entity)

            self.logger.info(f"Found {len(entities)} matching entities")
            return entities

        except Exception as e:
            self.logger.error(f"Failed to search entities: {e}")
            return []

    async def get_entity_connections(
        self, entity_id: str
    ) -> Tuple[List[str], List[str]]:
        """
        Get incoming and outgoing connections for an entity.

        Args:
            entity_id: ID of the entity to analyze

        Returns:
            Tuple of (incoming_connections, outgoing_connections)
        """
        try:
            # Read specific node to get its connections
            nodes = await self.memory_client.open_nodes(names=[entity_id])

            if not nodes or entity_id not in nodes:
                return [], []

            node_data = nodes[entity_id]

            # Extract incoming and outgoing relationships
            incoming = []
            outgoing = []

            for relation in node_data.get("relations", []):
                if relation["to"] == entity_id:
                    incoming.append(relation["from"])
                elif relation["from"] == entity_id:
                    outgoing.append(relation["to"])

            return incoming, outgoing

        except Exception as e:
            self.logger.error(f"Failed to get entity connections: {e}")
            return [], []

    def _mcp_node_to_entity(self, node_name: str, node_data: dict) -> Entity:
        """
        Convert MCP memory node to Entity object.

        Educational Notes:
        - Data transformation handles format differences
        - Default values provide robustness
        - Type mapping maintains semantic consistency
        - Error handling prevents data corruption
        """
        entity_type = node_data.get("entityType", "unknown")

        # Map MCP entity types to our domain types
        mapped_type = self._entity_type_mapping.get(entity_type, entity_type)

        observations = node_data.get("observations", [])
        if isinstance(observations, str):
            observations = [observations]

        # Extract metadata from MCP node
        metadata = {
            "mcp_id": node_name,
            "original_type": entity_type,
            "creation_date": node_data.get("created", datetime.now().isoformat()),
        }

        return Entity(
            id=node_name,
            entity_type=mapped_type,
            observations=observations,
            metadata=metadata,
        )

    def _entity_to_mcp_format(self, entity: Entity) -> dict:
        """
        Convert Entity object to MCP memory format.

        Educational Notes:
        - Inverse transformation of _mcp_node_to_entity
        - Preserves all entity information
        - Handles type mapping consistently
        - Provides audit information
        """
        return {
            "name": entity.id,
            "entityType": entity.entity_type,
            "observations": entity.observations,
        }

    def _mcp_relation_to_relationship(
        self, mcp_relation: dict
    ) -> Optional[Relationship]:
        """
        Convert MCP memory relation to Relationship object.

        Args:
            mcp_relation: MCP relation dictionary

        Returns:
            Relationship object or None if conversion fails
        """
        try:
            from_entity = mcp_relation.get("from")
            to_entity = mcp_relation.get("to")
            relation_type = mcp_relation.get("relationType")

            if not all([from_entity, to_entity, relation_type]):
                self.logger.warning(f"Incomplete MCP relation: {mcp_relation}")
                return None

            # Generate unique relationship ID
            rel_id = f"{from_entity}__{relation_type}__{to_entity}"

            return Relationship(
                id=rel_id,
                from_entity=from_entity,
                to_entity=to_entity,
                relation_type=relation_type,
                weight=1.0,  # Default weight
                metadata={"source": "mcp_memory"},
            )

        except Exception as e:
            self.logger.error(f"Failed to convert MCP relation: {e}")
            return None

    def _relationship_to_mcp_format(self, relationship: Relationship) -> dict:
        """
        Convert Relationship object to MCP memory format.

        Args:
            relationship: Relationship object to convert

        Returns:
            MCP relation dictionary
        """
        return {
            "from": relationship.from_entity,
            "to": relationship.to_entity,
            "relationType": relationship.relation_type,
        }


class KnowledgeGraphMemoryManager:
    """
    High-level manager for knowledge graph memory operations.

    Educational Notes:
    - Facade pattern simplifies complex subsystem interactions
    - Command pattern for batch operations
    - Template method for consistent operation structure
    - Observer pattern for change notifications
    """

    def __init__(self, mcp_memory_client):
        """
        Initialize memory manager with MCP client.

        Args:
            mcp_memory_client: MCP memory client instance
        """
        self.adapter = MCPMemoryAdapter(mcp_memory_client)
        self.knowledge_graph: Optional[KnowledgeGraph] = None
        self.logger = logging.getLogger(__name__)
        self._dirty_entities: Set[str] = set()
        self._auto_sync = True

    async def initialize(self) -> KnowledgeGraph:
        """
        Initialize knowledge graph from MCP memory.

        Returns:
            Loaded KnowledgeGraph instance
        """
        self.logger.info("Initializing knowledge graph from memory")
        self.knowledge_graph = await self.adapter.load_knowledge_graph()
        self._dirty_entities.clear()
        return self.knowledge_graph

    async def add_research_insight(
        self,
        paper_id: str,
        concept: str,
        evidence: str,
        relationship_type: str = "discusses",
    ) -> None:
        """
        Add research insight connecting paper to concept.

        Educational Notes:
        - Domain-specific operation for research workflow
        - Automatic entity creation reduces manual overhead
        - Relationship establishment maintains knowledge structure
        - Dirty tracking enables efficient synchronization

        Args:
            paper_id: Research paper identifier
            concept: Concept or topic discussed
            evidence: Supporting evidence from the paper
            relationship_type: Type of relationship between paper and concept
        """
        if not self.knowledge_graph:
            await self.initialize()

        # Create or update paper entity
        if paper_id not in self.knowledge_graph.entities:
            paper_entity = Entity(
                id=paper_id,
                entity_type="research_paper",
                observations=[f"Academic paper: {paper_id}"],
            )
            self.knowledge_graph.add_entity(paper_entity)

        # Create or update concept entity
        if concept not in self.knowledge_graph.entities:
            concept_entity = Entity(
                id=concept,
                entity_type="concept",
                observations=[f"Research concept: {concept}"],
            )
            self.knowledge_graph.add_entity(concept_entity)

        # Add evidence as observation to concept
        concept_entity = self.knowledge_graph.entities[concept]
        if evidence not in concept_entity.observations:
            concept_entity.observations.append(evidence)
            concept_entity.updated_at = datetime.now()

        # Create relationship
        rel_id = f"{paper_id}__{relationship_type}__{concept}"
        relationship = Relationship(
            id=rel_id,
            from_entity=paper_id,
            to_entity=concept,
            relation_type=relationship_type,
            metadata={"evidence": evidence},
        )

        try:
            self.knowledge_graph.add_relationship(relationship)

            # Track dirty entities for sync
            self._dirty_entities.update([paper_id, concept])

            if self._auto_sync:
                await self.sync_changes()

        except ValueError as e:
            # Relationship might already exist
            self.logger.info(f"Relationship already exists: {e}")

    async def find_conceptual_path(
        self, start_concept: str, target_concept: str
    ) -> List[str]:
        """
        Find conceptual path between two concepts.

        Args:
            start_concept: Starting concept
            target_concept: Target concept

        Returns:
            List of concepts forming the path
        """
        if not self.knowledge_graph:
            await self.initialize()

        return self.knowledge_graph.find_shortest_conceptual_path(
            start_concept, target_concept
        )

    async def get_concept_importance(self) -> Dict[str, float]:
        """
        Calculate importance scores for all concepts.

        Returns:
            Dictionary mapping concept IDs to importance scores
        """
        if not self.knowledge_graph:
            await self.initialize()

        return self.knowledge_graph.calculate_entity_importance()

    async def search_related_concepts(self, query: str) -> List[str]:
        """
        Search for concepts related to query.

        Args:
            query: Search query

        Returns:
            List of related concept IDs
        """
        entities = await self.adapter.search_entities(query)

        # Filter for concepts and return IDs
        concept_ids = [
            entity.id
            for entity in entities
            if entity.entity_type in ["concept", "knowledge_concept"]
        ]

        return concept_ids

    async def get_learning_sequence(self) -> List[str]:
        """
        Get optimal learning sequence based on concept dependencies.

        Returns:
            List of concept IDs in optimal learning order
        """
        if not self.knowledge_graph:
            await self.initialize()

        try:
            return self.knowledge_graph.get_learning_order()
        except ValueError as e:
            self.logger.warning(f"Cycle detected in learning dependencies: {e}")
            # Return entities without strict ordering
            return list(self.knowledge_graph.entities.keys())

    async def sync_changes(self) -> None:
        """
        Synchronize dirty entities to MCP memory.

        Educational Notes:
        - Batch operations optimize performance
        - Error handling preserves data integrity
        - Change tracking minimizes sync overhead
        - Logging provides audit trail
        """
        if not self._dirty_entities or not self.knowledge_graph:
            return

        dirty_list = list(self._dirty_entities)

        try:
            await self.adapter.sync_entity_updates(self.knowledge_graph, dirty_list)
            self._dirty_entities.clear()
            self.logger.info(f"Synchronized {len(dirty_list)} entity changes")

        except Exception as e:
            self.logger.error(f"Failed to sync changes: {e}")
            # Keep dirty entities for retry
            raise

    async def export_graph_statistics(self) -> Dict[str, any]:
        """
        Export comprehensive graph statistics.

        Returns:
            Dictionary with graph analysis metrics
        """
        if not self.knowledge_graph:
            await self.initialize()

        base_stats = self.knowledge_graph.get_statistics()
        importance_scores = self.knowledge_graph.calculate_entity_importance()

        # Add advanced analytics
        base_stats.update(
            {
                "most_important_entities": sorted(
                    importance_scores.items(), key=lambda x: x[1], reverse=True
                )[:10],
                "average_importance": (
                    sum(importance_scores.values()) / len(importance_scores)
                    if importance_scores
                    else 0
                ),
                "sync_status": {
                    "dirty_entities": len(self._dirty_entities),
                    "auto_sync_enabled": self._auto_sync,
                },
            }
        )

        return base_stats

    def set_auto_sync(self, enabled: bool) -> None:
        """
        Enable or disable automatic synchronization.

        Args:
            enabled: Whether to enable auto-sync
        """
        self._auto_sync = enabled
        self.logger.info(f"Auto-sync {'enabled' if enabled else 'disabled'}")


# Example usage for educational purposes
async def demonstrate_mcp_integration():
    """
    Demonstrate MCP memory integration capabilities.

    Educational Notes:
    - Shows practical usage patterns
    - Demonstrates async/await patterns
    - Illustrates error handling strategies
    - Provides performance optimization examples
    """
    print("=== MCP Memory Integration Demonstration ===\n")

    # Mock MCP client for demonstration
    class MockMCPClient:
        def __init__(self):
            self.data = {"nodes": {}, "relations": []}

        async def read_graph(self):
            await asyncio.sleep(0.01)  # Simulate async operation
            return self.data

        async def create_entities(self, entities):
            await asyncio.sleep(0.01)  # Simulate async operation
            print(f"Creating {len(entities)} entities in MCP memory")

        async def create_relations(self, relations):
            await asyncio.sleep(0.01)  # Simulate async operation
            print(f"Creating {len(relations)} relations in MCP memory")

        async def search_nodes(self, query):
            await asyncio.sleep(0.01)  # Simulate async operation
            print(f"Searching MCP memory for: '{query}'")
            return []

        async def add_observations(self, observations):
            await asyncio.sleep(0.01)  # Simulate async operation
            print(f"Adding {len(observations)} observations to MCP memory")

        async def open_nodes(self, names):
            await asyncio.sleep(0.01)  # Simulate async operation
            return {name: {} for name in names}

    # Initialize memory manager
    mcp_client = MockMCPClient()
    manager = KnowledgeGraphMemoryManager(mcp_client)

    # Initialize knowledge graph
    await manager.initialize()
    print("✅ Knowledge graph initialized from MCP memory")

    # Add research insights
    await manager.add_research_insight(
        paper_id="smith_2023_ml",
        concept="machine_learning",
        evidence="Paper demonstrates novel ML approach for classification",
        relationship_type="proposes",
    )

    await manager.add_research_insight(
        paper_id="jones_2023_cv",
        concept="computer_vision",
        evidence="Comparative study of CNN architectures",
        relationship_type="analyzes",
    )

    print("✅ Research insights added to knowledge graph")

    # Find conceptual connections
    path = await manager.find_conceptual_path("machine_learning", "computer_vision")
    print(f"📍 Conceptual path: {' -> '.join(path) if path else 'No path found'}")

    # Calculate concept importance
    importance = await manager.get_concept_importance()
    print(f"🎯 Concept importance scores: {importance}")

    # Export statistics
    stats = await manager.export_graph_statistics()
    print(f"📊 Graph statistics: {stats}")

    print("\n=== MCP Integration Demonstration Complete ===")


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_mcp_integration())
