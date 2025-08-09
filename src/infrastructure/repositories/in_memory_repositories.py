"""
In-Memory Concept Repository Infrastructure Adapter

Implements ConceptRepository and MappingRepository ports for testing and development.

Educational Purpose:
- Demonstrates Repository pattern implementation
- Shows in-memory storage for testing and prototyping
- Illustrates transaction boundaries and data consistency
- Examples of query optimization and indexing strategies

Real-World Application:
- Testing environments for unit and integration tests
- Development environments for rapid prototyping
- Cache layer for frequently accessed concepts
- Temporary storage during data migration
"""

from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from threading import Lock
from collections import defaultdict

from src.application.use_cases.concept_integration import (
    ConceptRepository,
    MappingRepository,
)
from src.domain.entities.atomic_concept import AtomicConcept, ConceptLevel, ConceptType
from src.domain.value_objects.concept_mapping import (
    ConceptMapping,
    ConceptRelationship,
    RelationshipType,
)


@dataclass
class RepositoryStatistics:
    """
    Value object for repository performance statistics.

    Educational Pattern: Metrics Collection
    - Provides insights into repository usage patterns
    - Enables performance monitoring and optimization
    - Supports capacity planning and tuning decisions
    """

    concept_count: int = 0
    mapping_count: int = 0
    total_relationships: int = 0
    queries_executed: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def hit_ratio(self) -> float:
        """Calculate cache hit ratio for performance monitoring."""
        total_queries = self.cache_hits + self.cache_misses
        return self.cache_hits / total_queries if total_queries > 0 else 0.0


class InMemoryConceptRepository(ConceptRepository):
    """
    In-memory implementation of ConceptRepository port.

    Educational Patterns:
    - Repository Pattern: Encapsulates data access logic
    - Unit of Work: Manages transaction boundaries
    - Index Strategy: Multiple indexes for query optimization
    - Thread Safety: Concurrent access protection

    Real-World Usage:
    - Unit testing with predictable data
    - Development environment for rapid iteration
    - Caching layer for production systems
    - Proof-of-concept implementations
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize in-memory repository with indexing structures.

        Educational Pattern: Index Design
        - Primary index by ID for O(1) lookups
        - Secondary indexes for common query patterns
        - Thread-safe operations with proper locking
        """
        self._logger = logger or logging.getLogger(__name__)
        self._lock = Lock()  # Thread safety for concurrent access

        # Primary storage
        self._concepts: Dict[str, AtomicConcept] = {}

        # Secondary indexes for query optimization
        self._domain_index: Dict[str, Set[str]] = defaultdict(set)
        self._level_index: Dict[ConceptLevel, Set[str]] = defaultdict(set)
        self._type_index: Dict[ConceptType, Set[str]] = defaultdict(set)
        self._tag_index: Dict[str, Set[str]] = defaultdict(set)

        # Performance tracking
        self._stats = RepositoryStatistics()

        self._logger.info("Initialized in-memory concept repository")

    def find_by_id(self, concept_id: str) -> Optional[AtomicConcept]:
        """
        Find concept by unique identifier.

        Educational Pattern: Primary Key Lookup
        - O(1) lookup time using dictionary
        - Thread-safe access with locking
        - Performance metrics collection
        """
        with self._lock:
            self._stats.queries_executed += 1

            if concept_id in self._concepts:
                self._stats.cache_hits += 1
                concept = self._concepts[concept_id]
                self._logger.debug(f"Found concept: {concept_id}")
                return concept
            else:
                self._stats.cache_misses += 1
                self._logger.debug(f"Concept not found: {concept_id}")
                return None

    def find_by_domain(self, domain: str) -> List[AtomicConcept]:
        """
        Find all concepts in a domain using secondary index.

        Educational Pattern: Secondary Index Query
        - Uses pre-built index for efficient domain queries
        - Avoids full table scan for better performance
        - Maintains index consistency with primary storage
        """
        with self._lock:
            self._stats.queries_executed += 1

            concept_ids = self._domain_index.get(domain, set())
            concepts = [
                self._concepts[cid] for cid in concept_ids if cid in self._concepts
            ]

            self._logger.debug(f"Found {len(concepts)} concepts in domain: {domain}")
            return concepts

    def save(self, concept: AtomicConcept) -> None:
        """
        Save a single concept with index maintenance.

        Educational Pattern: Transaction Management
        - Atomic operation ensuring consistency
        - Index updates coordinated with primary storage
        - Error handling prevents partial updates
        """
        with self._lock:
            try:
                # Remove from old indexes if updating
                self._remove_from_indexes(concept.id)

                # Save to primary storage
                self._concepts[concept.id] = concept

                # Update indexes
                self._add_to_indexes(concept)

                # Update statistics
                self._stats.concept_count = len(self._concepts)
                self._stats.last_updated = datetime.now()

                self._logger.debug(f"Saved concept: {concept.id}")

            except Exception as e:
                self._logger.error(f"Failed to save concept {concept.id}: {str(e)}")
                raise

    def save_many(self, concepts: List[AtomicConcept]) -> None:
        """
        Save multiple concepts efficiently in batch.

        Educational Pattern: Batch Processing
        - Optimizes multiple operations into single transaction
        - Reduces lock overhead for better performance
        - All-or-nothing semantics for consistency
        """
        with self._lock:
            try:
                saved_count = 0

                for concept in concepts:
                    # Remove from old indexes if updating
                    self._remove_from_indexes(concept.id)

                    # Save to primary storage
                    self._concepts[concept.id] = concept

                    # Update indexes
                    self._add_to_indexes(concept)

                    saved_count += 1

                # Update statistics once at the end
                self._stats.concept_count = len(self._concepts)
                self._stats.last_updated = datetime.now()

                self._logger.info(f"Batch saved {saved_count} concepts")

            except Exception as e:
                self._logger.error(f"Failed to batch save concepts: {str(e)}")
                raise

    def search(self, criteria: Dict[str, Any]) -> List[AtomicConcept]:
        """
        Search concepts using multiple criteria with index optimization.

        Educational Pattern: Query Optimization
        - Uses indexes when possible for better performance
        - Falls back to full scan only when necessary
        - Combines multiple criteria efficiently
        """
        with self._lock:
            self._stats.queries_executed += 1

            # Start with all concepts if no indexed criteria
            candidate_ids = set(self._concepts.keys())

            # Apply indexed criteria to narrow candidates
            if "domain" in criteria:
                domain_ids = self._domain_index.get(criteria["domain"], set())
                candidate_ids &= domain_ids

            if "level" in criteria:
                level = criteria["level"]
                if isinstance(level, str):
                    level = ConceptLevel.from_string(level)
                level_ids = self._level_index.get(level, set())
                candidate_ids &= level_ids

            if "concept_type" in criteria:
                concept_type = criteria["concept_type"]
                if isinstance(concept_type, str):
                    concept_type = ConceptType(concept_type)
                type_ids = self._type_index.get(concept_type, set())
                candidate_ids &= type_ids

            if "tags" in criteria:
                # Find concepts that have all required tags
                required_tags = set(criteria["tags"])
                for tag in required_tags:
                    tag_ids = self._tag_index.get(tag.lower(), set())
                    candidate_ids &= tag_ids

            # Get candidate concepts
            candidates = [
                self._concepts[cid] for cid in candidate_ids if cid in self._concepts
            ]

            # Apply non-indexed criteria with full object matching
            results = []
            for concept in candidates:
                if concept.matches_search_criteria(criteria):
                    results.append(concept)

            self._logger.debug(
                f"Search returned {len(results)} concepts from {len(candidates)} candidates"
            )
            return results

    def _add_to_indexes(self, concept: AtomicConcept) -> None:
        """
        Add concept to all secondary indexes.

        Educational Pattern: Index Maintenance
        - Keeps indexes synchronized with primary data
        - Handles multiple index types consistently
        - Supports efficient query operations
        """
        # Domain index
        self._domain_index[concept.domain].add(concept.id)

        # Level index
        self._level_index[concept.level].add(concept.id)

        # Type index
        self._type_index[concept.concept_type].add(concept.id)

        # Tag index
        for tag in concept.tags:
            self._tag_index[tag.lower()].add(concept.id)

    def _remove_from_indexes(self, concept_id: str) -> None:
        """
        Remove concept from all secondary indexes.

        Educational Pattern: Cleanup Strategy
        - Ensures indexes don't contain stale references
        - Handles updates by removing old entries
        - Maintains index integrity during modifications
        """
        if concept_id not in self._concepts:
            return  # Nothing to remove

        concept = self._concepts[concept_id]

        # Remove from domain index
        self._domain_index[concept.domain].discard(concept_id)

        # Remove from level index
        self._level_index[concept.level].discard(concept_id)

        # Remove from type index
        self._type_index[concept.concept_type].discard(concept_id)

        # Remove from tag indexes
        for tag in concept.tags:
            self._tag_index[tag.lower()].discard(concept_id)

    def get_statistics(self) -> RepositoryStatistics:
        """Get repository performance statistics."""
        with self._lock:
            # Update current counts
            self._stats.concept_count = len(self._concepts)
            return self._stats

    def clear(self) -> None:
        """
        Clear all data from repository.

        Educational Pattern: Reset Operation
        - Useful for testing and development
        - Ensures clean state between test runs
        - Resets both data and statistics
        """
        with self._lock:
            self._concepts.clear()
            self._domain_index.clear()
            self._level_index.clear()
            self._type_index.clear()
            self._tag_index.clear()
            self._stats = RepositoryStatistics()

            self._logger.info("Cleared all repository data")


class InMemoryMappingRepository(MappingRepository):
    """
    In-memory implementation of MappingRepository port.

    Educational Patterns:
    - Repository Pattern: Specialized for mapping storage
    - Composite Aggregate: Manages complex object relationships
    - Query Optimization: Indexes for relationship queries
    - Consistency Management: Ensures mapping integrity

    Real-World Usage:
    - Testing knowledge graph operations
    - Development environment for relationship analysis
    - Caching layer for mapping data
    - Temporary storage during data processing
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize in-memory mapping repository with relationship indexes."""
        self._logger = logger or logging.getLogger(__name__)
        self._lock = Lock()

        # Primary storage for mappings by domain
        self._mappings: Dict[str, ConceptMapping] = {}

        # Relationship indexes for efficient queries
        self._relationship_index: Dict[str, List[ConceptRelationship]] = defaultdict(
            list
        )
        self._reverse_relationship_index: Dict[str, List[ConceptRelationship]] = (
            defaultdict(list)
        )

        # Performance tracking
        self._stats = RepositoryStatistics()

        self._logger.info("Initialized in-memory mapping repository")

    def find_by_domain(self, domain: str) -> Optional[ConceptMapping]:
        """
        Find mapping for a specific domain.

        Educational Pattern: Domain-Based Partitioning
        - Partitions data by domain for scalability
        - Enables domain-specific optimizations
        - Supports multi-tenant scenarios
        """
        with self._lock:
            self._stats.queries_executed += 1

            if domain in self._mappings:
                self._stats.cache_hits += 1
                mapping = self._mappings[domain]
                self._logger.debug(f"Found mapping for domain: {domain}")
                return mapping
            else:
                self._stats.cache_misses += 1
                self._logger.debug(f"No mapping found for domain: {domain}")
                return None

    def save(self, mapping: ConceptMapping) -> None:
        """
        Save mapping with relationship index updates.

        Educational Pattern: Aggregate Persistence
        - Saves complex object with all relationships
        - Maintains indexes for efficient relationship queries
        - Ensures consistency across related data structures
        """
        with self._lock:
            try:
                # Remove old indexes if updating
                self._remove_mapping_from_indexes(mapping.domain)

                # Save to primary storage
                self._mappings[mapping.domain] = mapping

                # Update relationship indexes
                self._add_mapping_to_indexes(mapping)

                # Update statistics
                self._stats.mapping_count = len(self._mappings)
                self._stats.total_relationships = sum(
                    len(m.relationships) for m in self._mappings.values()
                )
                self._stats.last_updated = datetime.now()

                self._logger.debug(f"Saved mapping for domain: {mapping.domain}")

            except Exception as e:
                self._logger.error(
                    f"Failed to save mapping for {mapping.domain}: {str(e)}"
                )
                raise

    def find_relationships(self, concept_id: str) -> List[ConceptRelationship]:
        """
        Find all relationships involving a concept.

        Educational Pattern: Bidirectional Index
        - Uses both forward and reverse indexes
        - Provides complete relationship view
        - Optimizes for relationship-heavy queries
        """
        with self._lock:
            self._stats.queries_executed += 1

            # Get relationships where concept is source
            outgoing = self._relationship_index.get(concept_id, [])

            # Get relationships where concept is target
            incoming = self._reverse_relationship_index.get(concept_id, [])

            # Combine and deduplicate
            all_relationships = outgoing + incoming
            unique_relationships = []
            seen = set()

            for rel in all_relationships:
                rel_key = (
                    rel.source_concept_id,
                    rel.target_concept_id,
                    rel.relationship_type,
                )
                if rel_key not in seen:
                    unique_relationships.append(rel)
                    seen.add(rel_key)

            self._logger.debug(
                f"Found {len(unique_relationships)} relationships for concept: {concept_id}"
            )
            return unique_relationships

    def _add_mapping_to_indexes(self, mapping: ConceptMapping) -> None:
        """
        Add mapping relationships to indexes.

        Educational Pattern: Index Population
        - Builds indexes from aggregate data
        - Handles bidirectional relationships
        - Optimizes for common query patterns
        """
        for relationship in mapping.relationships:
            # Forward index (source -> relationship)
            self._relationship_index[relationship.source_concept_id].append(
                relationship
            )

            # Reverse index (target -> relationship)
            self._reverse_relationship_index[relationship.target_concept_id].append(
                relationship
            )

    def _remove_mapping_from_indexes(self, domain: str) -> None:
        """
        Remove mapping relationships from indexes.

        Educational Pattern: Index Cleanup
        - Removes stale index entries during updates
        - Maintains index accuracy and performance
        - Prevents memory leaks from orphaned references
        """
        if domain not in self._mappings:
            return

        old_mapping = self._mappings[domain]

        for relationship in old_mapping.relationships:
            # Remove from forward index
            if relationship.source_concept_id in self._relationship_index:
                self._relationship_index[relationship.source_concept_id] = [
                    r
                    for r in self._relationship_index[relationship.source_concept_id]
                    if not (
                        r.source_concept_id == relationship.source_concept_id
                        and r.target_concept_id == relationship.target_concept_id
                        and r.relationship_type == relationship.relationship_type
                    )
                ]

            # Remove from reverse index
            if relationship.target_concept_id in self._reverse_relationship_index:
                self._reverse_relationship_index[relationship.target_concept_id] = [
                    r
                    for r in self._reverse_relationship_index[
                        relationship.target_concept_id
                    ]
                    if not (
                        r.source_concept_id == relationship.source_concept_id
                        and r.target_concept_id == relationship.target_concept_id
                        and r.relationship_type == relationship.relationship_type
                    )
                ]

    def get_domain_statistics(self, domain: str) -> Dict[str, int]:
        """
        Get statistics for a specific domain.

        Educational Pattern: Analytics Support
        - Provides domain-specific metrics
        - Supports monitoring and optimization
        - Enables capacity planning per domain
        """
        with self._lock:
            mapping = self._mappings.get(domain)
            if not mapping:
                return {}

            return {
                "concept_count": len(mapping.concept_ids),
                "relationship_count": len(mapping.relationships),
                "foundational_concepts": len(mapping.get_foundational_concepts()),
                "advanced_concepts": len(mapping.get_advanced_concepts()),
            }

    def get_statistics(self) -> RepositoryStatistics:
        """Get repository performance statistics."""
        with self._lock:
            # Update current counts
            self._stats.mapping_count = len(self._mappings)
            self._stats.total_relationships = sum(
                len(m.relationships) for m in self._mappings.values()
            )
            return self._stats

    def clear(self) -> None:
        """Clear all mapping data from repository."""
        with self._lock:
            self._mappings.clear()
            self._relationship_index.clear()
            self._reverse_relationship_index.clear()
            self._stats = RepositoryStatistics()

            self._logger.info("Cleared all mapping repository data")


# Educational Example Usage
def demonstrate_repositories():
    """
    Demonstrate repository patterns with sample data.

    Educational Purpose:
    - Shows how to use repository implementations
    - Demonstrates query patterns and performance
    - Illustrates transaction and consistency management
    """

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("demo")

    # Create repositories
    concept_repo = InMemoryConceptRepository(logger)
    mapping_repo = InMemoryMappingRepository(logger)

    # Create sample concepts
    concept1 = AtomicConcept(
        id="extensionality",
        name="Axiom of Extensionality",
        formal_statement="∀A ∀B (A = B ↔ ∀x (x ∈ A ↔ x ∈ B))",
        informal_description="Two sets are equal if and only if they have the same elements",
        concept_type=ConceptType.AXIOM,
        level=ConceptLevel.UNDERGRADUATE,
        domain="set_theory",
        tags={"zfc", "axiom", "foundation"},
    )

    concept2 = AtomicConcept(
        id="empty_set",
        name="Empty Set",
        formal_statement="∃A ∀x (x ∉ A)",
        informal_description="The set containing no elements",
        concept_type=ConceptType.DEFINITION,
        level=ConceptLevel.HIGH_SCHOOL,
        domain="set_theory",
        prerequisites={"extensionality"},
        tags={"basic_sets"},
    )

    # Demonstrate concept repository operations
    print("=== Concept Repository Demo ===")

    # Save concepts
    concept_repo.save_many([concept1, concept2])

    # Query by ID
    found = concept_repo.find_by_id("extensionality")
    print(f"Found by ID: {found.name if found else 'Not found'}")

    # Query by domain
    domain_concepts = concept_repo.find_by_domain("set_theory")
    print(f"Concepts in set_theory: {len(domain_concepts)}")

    # Search with criteria
    search_results = concept_repo.search(
        {"domain": "set_theory", "level": ConceptLevel.UNDERGRADUATE, "tags": ["axiom"]}
    )
    print(f"Search results: {len(search_results)}")

    # Show statistics
    stats = concept_repo.get_statistics()
    print(
        f"Repository stats: {stats.concept_count} concepts, hit ratio: {stats.hit_ratio():.2f}"
    )

    # Demonstrate mapping repository
    print("\n=== Mapping Repository Demo ===")

    # Create and save mapping
    from src.domain.value_objects.concept_mapping import (
        ConceptMapping,
        ConceptRelationship,
        RelationshipType,
        MappingStrength,
    )

    relationship = ConceptRelationship(
        source_concept_id="extensionality",
        target_concept_id="empty_set",
        relationship_type=RelationshipType.PREREQUISITE,
        strength=MappingStrength.ESSENTIAL,
    )

    mapping = ConceptMapping(
        concept_ids=frozenset(["extensionality", "empty_set"]),
        relationships=(relationship,),
        domain="set_theory",
    )

    mapping_repo.save(mapping)

    # Query mapping
    found_mapping = mapping_repo.find_by_domain("set_theory")
    print(
        f"Found mapping: {len(found_mapping.concept_ids) if found_mapping else 0} concepts"
    )

    # Query relationships
    relationships = mapping_repo.find_relationships("extensionality")
    print(f"Relationships for extensionality: {len(relationships)}")

    # Show mapping statistics
    mapping_stats = mapping_repo.get_statistics()
    print(
        f"Mapping stats: {mapping_stats.mapping_count} mappings, {mapping_stats.total_relationships} relationships"
    )


if __name__ == "__main__":
    demonstrate_repositories()
