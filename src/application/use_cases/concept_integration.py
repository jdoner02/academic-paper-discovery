"""
Concept Integration Use Cases

Application layer use cases for atomic concept integration and management.

Educational Purpose:
- Demonstrates Use Case pattern from Clean Architecture
- Shows orchestration of domain logic without business rules
- Illustrates dependency inversion with ports/adapters
- Examples of transaction boundaries and error handling

Real-World Application:
- Educational platform course content integration
- Knowledge management system content ingestion
- Learning analytics and progress tracking
- Curriculum design and optimization tools
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

# Domain imports
from src.domain.entities.atomic_concept import AtomicConcept, ConceptLevel, ConceptType
from src.domain.value_objects.concept_mapping import (
    ConceptMapping,
    ConceptRelationship,
    RelationshipType,
    MappingStrength,
)


# Ports (Abstract Interfaces) - Dependency Inversion Principle
class ConceptRepository(ABC):
    """
    Port for concept persistence operations.

    Educational Pattern: Repository Pattern
    - Abstracts data access from business logic
    - Enables testing with mock implementations
    - Supports multiple storage backends (files, databases, APIs)
    """

    @abstractmethod
    def find_by_id(self, concept_id: str) -> Optional[AtomicConcept]:
        """Find concept by unique identifier."""
        pass

    @abstractmethod
    def find_by_domain(self, domain: str) -> List[AtomicConcept]:
        """Find all concepts in a domain."""
        pass

    @abstractmethod
    def save(self, concept: AtomicConcept) -> None:
        """Save concept to storage."""
        pass

    @abstractmethod
    def save_many(self, concepts: List[AtomicConcept]) -> None:
        """Save multiple concepts efficiently."""
        pass

    @abstractmethod
    def search(self, criteria: Dict[str, Any]) -> List[AtomicConcept]:
        """Search concepts by criteria."""
        pass


class MappingRepository(ABC):
    """
    Port for concept mapping persistence.

    Educational Pattern: Separation of Concerns
    - Mappings and concepts have different storage needs
    - Allows independent optimization of each repository
    - Supports complex queries on relationship data
    """

    @abstractmethod
    def find_by_domain(self, domain: str) -> Optional[ConceptMapping]:
        """Find mapping for a domain."""
        pass

    @abstractmethod
    def save(self, mapping: ConceptMapping) -> None:
        """Save mapping to storage."""
        pass

    @abstractmethod
    def find_relationships(self, concept_id: str) -> List[ConceptRelationship]:
        """Find all relationships for a concept."""
        pass


class ConceptLoader(ABC):
    """
    Port for loading concepts from external sources.

    Educational Pattern: Strategy Pattern
    - Different sources (JSON, XML, API) can have different loaders
    - Enables plugin architecture for content sources
    - Supports testing with mock data sources
    """

    @abstractmethod
    def load_concepts(self, source_path: str) -> List[Dict[str, Any]]:
        """Load raw concept data from source."""
        pass

    @abstractmethod
    def validate_format(self, data: Dict[str, Any]) -> bool:
        """Validate data format before processing."""
        pass


class EventPublisher(ABC):
    """
    Port for publishing domain events.

    Educational Pattern: Observer Pattern / Event-Driven Architecture
    - Enables loose coupling between components
    - Supports integration with external systems
    - Allows for audit trails and analytics
    """

    @abstractmethod
    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publish an event."""
        pass


# Use Case Results and Errors
class IntegrationResult(Enum):
    """Results of concept integration operations."""

    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    VALIDATION_ERROR = "validation_error"
    STORAGE_ERROR = "storage_error"
    DEPENDENCY_ERROR = "dependency_error"


@dataclass
class ConceptIntegrationSummary:
    """
    Value object summarizing integration results.

    Educational Pattern: Result Object
    - Encapsulates operation results with detailed information
    - Enables rich error reporting and debugging
    - Supports analytics and monitoring
    """

    result: IntegrationResult
    concepts_processed: int
    concepts_created: int
    concepts_updated: int
    relationships_created: int
    errors: List[str]
    warnings: List[str]
    processing_time_ms: int
    domain: str
    timestamp: datetime


# Use Cases (Application Layer)
class IntegrateConceptsUseCase:
    """
    Use case for integrating atomic concepts from external sources.

    Educational Patterns:
    - Use Case Pattern: Orchestrates domain operations
    - Dependency Inversion: Depends on abstractions (ports)
    - Single Responsibility: Focused on one business operation
    - Command Pattern: Encapsulates a complete operation

    Real-World Usage:
    - Importing course content from curriculum databases
    - Integrating research papers into knowledge graphs
    - Loading textbook content into learning platforms
    """

    def __init__(
        self,
        concept_repository: ConceptRepository,
        mapping_repository: MappingRepository,
        concept_loader: ConceptLoader,
        event_publisher: Optional[EventPublisher] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Dependency Injection Constructor.

        Educational Note: Dependencies are injected as abstractions,
        not concrete implementations. This enables testing and
        flexibility in deployment environments.
        """
        self._concept_repo = concept_repository
        self._mapping_repo = mapping_repository
        self._loader = concept_loader
        self._event_publisher = event_publisher
        self._logger = logger or logging.getLogger(__name__)

    def execute(
        self, source_path: str, domain: str, force_update: bool = False
    ) -> ConceptIntegrationSummary:
        """
        Execute the concept integration use case.

        Educational Pattern: Template Method
        - Defines the algorithm skeleton with specific steps
        - Each step can be overridden for different scenarios
        - Provides consistent error handling and logging

        Args:
            source_path: Path to source data (file, URL, etc.)
            domain: Target domain for concepts
            force_update: Whether to update existing concepts

        Returns:
            Summary of integration results
        """
        start_time = datetime.now()
        summary = ConceptIntegrationSummary(
            result=IntegrationResult.SUCCESS,
            concepts_processed=0,
            concepts_created=0,
            concepts_updated=0,
            relationships_created=0,
            errors=[],
            warnings=[],
            processing_time_ms=0,
            domain=domain,
            timestamp=start_time,
        )

        try:
            # Step 1: Load and validate source data
            raw_data = self._load_source_data(source_path, summary)
            if summary.result == IntegrationResult.VALIDATION_ERROR:
                return self._finalize_summary(summary, start_time)

            # Step 2: Create domain entities
            concepts = self._create_concepts(raw_data, domain, summary)
            if not concepts and not summary.errors:
                summary.warnings.append("No valid concepts found in source data")

            # Step 3: Check for existing concepts
            existing_concepts = self._check_existing_concepts(concepts, summary)

            # Step 4: Save new/updated concepts
            self._save_concepts(concepts, existing_concepts, force_update, summary)

            # Step 5: Create and save relationships
            self._create_relationships(concepts, domain, summary)

            # Step 6: Publish integration events
            self._publish_events(summary)

        except Exception as e:
            self._logger.error(f"Integration failed: {str(e)}", exc_info=True)
            summary.errors.append(f"Unexpected error: {str(e)}")
            summary.result = IntegrationResult.STORAGE_ERROR

        return self._finalize_summary(summary, start_time)

    def _load_source_data(
        self, source_path: str, summary: ConceptIntegrationSummary
    ) -> List[Dict[str, Any]]:
        """
        Load and validate source data.

        Educational Pattern: Error Handling Strategy
        - Validates input early to fail fast
        - Accumulates errors for comprehensive reporting
        - Logs detailed information for debugging
        """
        try:
            self._logger.info(f"Loading concepts from: {source_path}")
            raw_data = self._loader.load_concepts(source_path)

            if not raw_data:
                summary.errors.append("No data found in source")
                summary.result = IntegrationResult.VALIDATION_ERROR
                return []

            # Validate each concept's format
            valid_data = []
            for i, concept_data in enumerate(raw_data):
                if self._loader.validate_format(concept_data):
                    valid_data.append(concept_data)
                else:
                    summary.warnings.append(f"Invalid format for concept at index {i}")

            summary.concepts_processed = len(valid_data)
            self._logger.info(f"Loaded {len(valid_data)} valid concepts")
            return valid_data

        except Exception as e:
            self._logger.error(f"Failed to load source data: {str(e)}")
            summary.errors.append(f"Data loading error: {str(e)}")
            summary.result = IntegrationResult.VALIDATION_ERROR
            return []

    def _create_concepts(
        self,
        raw_data: List[Dict[str, Any]],
        domain: str,
        summary: ConceptIntegrationSummary,
    ) -> List[AtomicConcept]:
        """
        Create domain entities from raw data.

        Educational Pattern: Factory Method with Error Handling
        - Transforms external data into domain objects
        - Validates business rules during creation
        - Accumulates errors without stopping processing
        """
        concepts = []

        for concept_data in raw_data:
            try:
                # Set domain if not specified
                if "domain" not in concept_data:
                    concept_data["domain"] = domain

                concept = AtomicConcept.from_dict(concept_data)
                concepts.append(concept)

            except Exception as e:
                self._logger.warning(
                    f"Failed to create concept from {concept_data.get('id', 'unknown')}: {str(e)}"
                )
                summary.warnings.append(f"Concept creation error: {str(e)}")

        self._logger.info(f"Created {len(concepts)} concept entities")
        return concepts

    def _check_existing_concepts(
        self, concepts: List[AtomicConcept], summary: ConceptIntegrationSummary
    ) -> Dict[str, AtomicConcept]:
        """
        Check for existing concepts in repository.

        Educational Pattern: Bulk Operations Optimization
        - Minimizes database queries by batching lookups
        - Provides information for update decisions
        - Enables conflict resolution strategies
        """
        existing = {}

        for concept in concepts:
            try:
                existing_concept = self._concept_repo.find_by_id(concept.id)
                if existing_concept:
                    existing[concept.id] = existing_concept
            except Exception as e:
                self._logger.warning(
                    f"Error checking existing concept {concept.id}: {str(e)}"
                )
                summary.warnings.append(f"Repository query error: {str(e)}")

        self._logger.info(f"Found {len(existing)} existing concepts")
        return existing

    def _save_concepts(
        self,
        concepts: List[AtomicConcept],
        existing: Dict[str, AtomicConcept],
        force_update: bool,
        summary: ConceptIntegrationSummary,
    ) -> None:
        """
        Save concepts with update logic.

        Educational Pattern: Business Rule Implementation
        - Implements update/create logic based on business rules
        - Handles concurrency and conflict resolution
        - Provides detailed tracking for audit purposes
        """
        concepts_to_save = []

        for concept in concepts:
            if concept.id in existing:
                if force_update:
                    concepts_to_save.append(concept)
                    summary.concepts_updated += 1
                else:
                    summary.warnings.append(
                        f"Concept {concept.id} exists, skipping (use force_update=True)"
                    )
            else:
                concepts_to_save.append(concept)
                summary.concepts_created += 1

        if concepts_to_save:
            try:
                self._concept_repo.save_many(concepts_to_save)
                self._logger.info(f"Saved {len(concepts_to_save)} concepts")
            except Exception as e:
                self._logger.error(f"Failed to save concepts: {str(e)}")
                summary.errors.append(f"Save error: {str(e)}")
                summary.result = IntegrationResult.STORAGE_ERROR

    def _create_relationships(
        self,
        concepts: List[AtomicConcept],
        domain: str,
        summary: ConceptIntegrationSummary,
    ) -> None:
        """
        Create and save concept relationships.

        Educational Pattern: Aggregate Coordination
        - Coordinates between multiple domain objects
        - Maintains consistency across related entities
        - Handles complex business logic for relationships
        """
        relationships = []
        concept_map = {c.id: c for c in concepts}

        # Create relationships based on concept dependencies
        for concept in concepts:
            for prereq_id in concept.prerequisites:
                if prereq_id in concept_map:
                    rel = ConceptRelationship(
                        source_concept_id=prereq_id,
                        target_concept_id=concept.id,
                        relationship_type=RelationshipType.PREREQUISITE,
                        strength=MappingStrength.STRONG,
                        explanation=f"Required for understanding {concept.name}",
                    )
                    relationships.append(rel)

            for enabled_id in concept.enables:
                if enabled_id in concept_map:
                    rel = ConceptRelationship(
                        source_concept_id=concept.id,
                        target_concept_id=enabled_id,
                        relationship_type=RelationshipType.ENABLES,
                        strength=MappingStrength.STRONG,
                        explanation=f"Enables learning of {concept_map[enabled_id].name}",
                    )
                    relationships.append(rel)

        if relationships:
            try:
                mapping = ConceptMapping(
                    concept_ids=frozenset(concept_map.keys()),
                    relationships=tuple(relationships),
                    domain=domain,
                )
                self._mapping_repo.save(mapping)
                summary.relationships_created = len(relationships)
                self._logger.info(f"Created {len(relationships)} relationships")

            except Exception as e:
                self._logger.error(f"Failed to save relationships: {str(e)}")
                summary.errors.append(f"Relationship save error: {str(e)}")

    def _publish_events(self, summary: ConceptIntegrationSummary) -> None:
        """
        Publish integration events for external systems.

        Educational Pattern: Event-Driven Architecture
        - Decouples integration from downstream processing
        - Enables audit trails and analytics
        - Supports integration with external systems
        """
        if not self._event_publisher:
            return

        try:
            event_data = {
                "domain": summary.domain,
                "concepts_created": summary.concepts_created,
                "concepts_updated": summary.concepts_updated,
                "relationships_created": summary.relationships_created,
                "result": summary.result.value,
                "timestamp": summary.timestamp.isoformat(),
            }

            self._event_publisher.publish("concept_integration_completed", event_data)

        except Exception as e:
            self._logger.warning(f"Failed to publish events: {str(e)}")
            summary.warnings.append(f"Event publishing error: {str(e)}")

    def _finalize_summary(
        self, summary: ConceptIntegrationSummary, start_time: datetime
    ) -> ConceptIntegrationSummary:
        """Finalize summary with processing time and result assessment."""
        end_time = datetime.now()
        duration = end_time - start_time
        summary.processing_time_ms = int(duration.total_seconds() * 1000)

        # Assess final result
        if summary.errors:
            if summary.concepts_created > 0 or summary.concepts_updated > 0:
                summary.result = IntegrationResult.PARTIAL_SUCCESS
            else:
                summary.result = IntegrationResult.STORAGE_ERROR
        elif summary.warnings and summary.concepts_processed == 0:
            summary.result = IntegrationResult.VALIDATION_ERROR

        self._logger.info(
            f"Integration completed: {summary.result.value} in {summary.processing_time_ms}ms"
        )
        return summary


class GenerateLearningPathUseCase:
    """
    Use case for generating optimal learning paths through concepts.

    Educational Patterns:
    - Algorithm Encapsulation: Complex pathfinding logic in use case
    - Strategy Pattern: Different path generation strategies
    - Specification Pattern: Configurable path requirements

    Real-World Usage:
    - Personalized learning recommendations
    - Curriculum sequencing for courses
    - Prerequisite planning for students
    """

    def __init__(
        self,
        concept_repository: ConceptRepository,
        mapping_repository: MappingRepository,
        logger: Optional[logging.Logger] = None,
    ):
        self._concept_repo = concept_repository
        self._mapping_repo = mapping_repository
        self._logger = logger or logging.getLogger(__name__)

    def execute(
        self, target_concept_ids: List[str], domain: str, max_depth: int = 10
    ) -> Dict[str, List[str]]:
        """
        Generate learning paths to target concepts.

        Educational Algorithm: Topological sorting with optimization
        - Finds valid learning sequences respecting prerequisites
        - Optimizes for shortest path or specific criteria
        - Handles multiple target concepts efficiently

        Args:
            target_concept_ids: Concepts to learn
            domain: Domain to search within
            max_depth: Maximum path length

        Returns:
            Dictionary mapping concept IDs to learning paths
        """
        self._logger.info(
            f"Generating learning paths for {len(target_concept_ids)} concepts in {domain}"
        )

        try:
            # Load domain mapping
            mapping = self._mapping_repo.find_by_domain(domain)
            if not mapping:
                self._logger.warning(f"No mapping found for domain: {domain}")
                return {}

            paths = {}
            for concept_id in target_concept_ids:
                if concept_id in mapping.concept_ids:
                    path = self._find_optimal_path(concept_id, mapping, max_depth)
                    paths[concept_id] = path
                else:
                    self._logger.warning(
                        f"Concept {concept_id} not found in domain {domain}"
                    )

            return paths

        except Exception as e:
            self._logger.error(f"Path generation failed: {str(e)}")
            return {}

    def _find_optimal_path(
        self, target_id: str, mapping: ConceptMapping, max_depth: int
    ) -> List[str]:
        """
        Find optimal learning path using simplified topological sort.

        Educational Note: This is a simplified implementation.
        Production systems would use more sophisticated algorithms
        like A* search or dynamic programming for optimization.
        """
        # Get all prerequisites recursively
        all_prereqs = self._get_all_prerequisites(target_id, mapping, max_depth)

        # Sort by foundational concepts first
        foundational = mapping.get_foundational_concepts()
        path = []

        # Add foundational prerequisites first
        for concept_id in all_prereqs:
            if concept_id in foundational:
                path.append(concept_id)

        # Add non-foundational prerequisites
        for concept_id in all_prereqs:
            if concept_id not in foundational and concept_id not in path:
                path.append(concept_id)

        # Add target concept
        if target_id not in path:
            path.append(target_id)

        return path

    def _get_all_prerequisites(
        self,
        concept_id: str,
        mapping: ConceptMapping,
        max_depth: int,
        visited: Optional[Set[str]] = None,
    ) -> Set[str]:
        """Recursively get all prerequisites with cycle detection."""
        if visited is None:
            visited = set()

        if concept_id in visited or max_depth <= 0:
            return set()

        visited.add(concept_id)
        all_prereqs = set()

        direct_prereqs = mapping.get_prerequisites(concept_id)
        all_prereqs.update(direct_prereqs)

        # Recursively get prerequisites of prerequisites
        for prereq in direct_prereqs:
            indirect_prereqs = self._get_all_prerequisites(
                prereq, mapping, max_depth - 1, visited.copy()
            )
            all_prereqs.update(indirect_prereqs)

        return all_prereqs


# Educational Example Usage
def demonstrate_use_cases():
    """
    Demonstrate use case patterns with mock implementations.

    Educational Purpose:
    - Shows how to wire up dependencies
    - Demonstrates error handling and logging
    - Illustrates business operations in action
    """

    # Mock implementations for demonstration
    class MockConceptRepository(ConceptRepository):
        def __init__(self):
            self.concepts = {}

        def find_by_id(self, concept_id: str) -> Optional[AtomicConcept]:
            return self.concepts.get(concept_id)

        def find_by_domain(self, domain: str) -> List[AtomicConcept]:
            return [c for c in self.concepts.values() if c.domain == domain]

        def save(self, concept: AtomicConcept) -> None:
            self.concepts[concept.id] = concept

        def save_many(self, concepts: List[AtomicConcept]) -> None:
            for concept in concepts:
                self.save(concept)

        def search(self, criteria: Dict[str, Any]) -> List[AtomicConcept]:
            return list(self.concepts.values())  # Simplified

    class MockMappingRepository(MappingRepository):
        def __init__(self):
            self.mappings = {}

        def find_by_domain(self, domain: str) -> Optional[ConceptMapping]:
            return self.mappings.get(domain)

        def save(self, mapping: ConceptMapping) -> None:
            self.mappings[mapping.domain] = mapping

        def find_relationships(self, concept_id: str) -> List[ConceptRelationship]:
            return []  # Simplified

    class MockConceptLoader(ConceptLoader):
        def load_concepts(self, source_path: str) -> List[Dict[str, Any]]:
            # Return sample concept data
            return [
                {
                    "id": "test_concept",
                    "name": "Test Concept",
                    "formal_statement": "Test formal statement",
                    "informal_description": "A concept for testing purposes",
                    "concept_type": "definition",
                    "level": "undergraduate",
                }
            ]

        def validate_format(self, data: Dict[str, Any]) -> bool:
            required_fields = ["id", "name", "formal_statement", "informal_description"]
            return all(field in data for field in required_fields)

    # Wire up dependencies
    concept_repo = MockConceptRepository()
    mapping_repo = MockMappingRepository()
    loader = MockConceptLoader()

    # Execute integration use case
    integration_use_case = IntegrateConceptsUseCase(
        concept_repository=concept_repo,
        mapping_repository=mapping_repo,
        concept_loader=loader,
    )

    result = integration_use_case.execute(
        source_path="/mock/path", domain="test_domain"
    )

    print(f"Integration Result: {result.result.value}")
    print(f"Concepts Created: {result.concepts_created}")
    print(f"Processing Time: {result.processing_time_ms}ms")

    # Execute learning path use case
    path_use_case = GenerateLearningPathUseCase(
        concept_repository=concept_repo, mapping_repository=mapping_repo
    )

    paths = path_use_case.execute(
        target_concept_ids=["test_concept"], domain="test_domain"
    )

    print(f"Learning Paths: {paths}")


if __name__ == "__main__":
    demonstrate_use_cases()
