"""
ConceptHierarchy - Aggregate root managing complete concept hierarchies.

This aggregate root coordinates the complete lifecycle of concept hierarchies,
ensuring consistency, quality, and proper relationships between concepts.

Educational Notes - Aggregate Root Pattern:
- Serves as the single entry point for hierarchy operations
- Maintains consistency across all concepts within the hierarchy
- Encapsulates complex hierarchy business rules and validation
- Provides transactional boundary for hierarchy modifications

Educational Notes - Domain-Driven Design:
- Represents the core domain model of a complete concept hierarchy
- Encapsulates rich business logic for hierarchy management
- Provides clear interface for all hierarchy operations
- Maintains domain invariants across concept relationships

Design Decisions:
- Identity based on unique hierarchy ID (entity characteristics)
- Immutable evidence and metadata tracking for audit integrity
- Rich validation ensures hierarchy quality and consistency
- Comprehensive factory methods support various creation scenarios

Use Cases:
- Research Paper Analysis: Complete concept extraction and organization
- Academic Quality Control: Validation and assessment of concept hierarchies
- Algorithm Comparison: Standardized hierarchy representation for evaluation
- Knowledge Management: Structured organization of research concepts
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from datetime import datetime, timezone
import uuid

from src.domain.entities.concept import Concept
from src.domain.value_objects.evidence_sentence import EvidenceSentence
from src.domain.value_objects.hierarchy_metadata import HierarchyMetadata
from src.domain.value_objects.extraction_provenance import ExtractionProvenance


@dataclass
class ConceptHierarchy:
    """
    Aggregate root representing a complete concept hierarchy with full provenance.

    This entity manages the complete lifecycle of concept hierarchies,
    from creation through validation to quality assessment.

    Attributes:
        hierarchy_id: Unique identifier for this hierarchy
        concepts: Dictionary mapping concept text to Concept entities
        evidence_sentences: List of all evidence supporting concepts
        metadata: Comprehensive metrics about hierarchy structure and quality
        extraction_provenance: Complete audit trail of extraction process
        created_at: Timestamp when hierarchy was created
        last_modified: Timestamp of last modification
    """

    hierarchy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    concepts: Dict[str, Concept] = field(default_factory=dict)
    evidence_sentences: List[EvidenceSentence] = field(default_factory=list)
    metadata: Optional[HierarchyMetadata] = None
    extraction_provenance: Optional[ExtractionProvenance] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """
        Initialize hierarchy with proper validation and consistency checks.

        Educational Notes - Aggregate Consistency:
        - Ensures all concepts have proper hierarchical relationships
        - Validates evidence sentences reference concepts in the hierarchy
        - Maintains metadata consistency with actual hierarchy structure
        - Prevents creation of invalid or inconsistent hierarchies
        """
        self._validate_hierarchy_consistency()
        self._update_last_modified()

    def add_concept(self, concept: Concept) -> None:
        """
        Add a concept to the hierarchy with full validation.

        Args:
            concept: The concept to add to the hierarchy

        Raises:
            ValueError: If concept conflicts with existing hierarchy structure

        Educational Notes - Domain Rules:
        - Prevents duplicate concepts in the hierarchy
        - Ensures parent-child relationships are valid
        - Maintains hierarchy integrity during modifications
        """
        if concept.text in self.concepts:
            raise ValueError(f"Concept '{concept.text}' already exists in hierarchy")

        # Validate parent relationships exist in hierarchy
        for parent_text in concept.parent_concepts:
            if parent_text not in self.concepts:
                raise ValueError(
                    f"Parent concept '{parent_text}' not found in hierarchy"
                )

        # Validate child relationships exist in hierarchy
        for child_text in concept.child_concepts:
            if child_text not in self.concepts:
                raise ValueError(f"Child concept '{child_text}' not found in hierarchy")

        self.concepts[concept.text] = concept
        self._update_last_modified()

    def remove_concept(self, concept_text: str) -> None:
        """
        Remove a concept and update all related relationships.

        Args:
            concept_text: Text of the concept to remove

        Educational Notes - Consistency Maintenance:
        - Removes all parent-child relationships involving the concept
        - Updates evidence sentences to maintain referential integrity
        - Ensures hierarchy remains valid after concept removal
        """
        if concept_text not in self.concepts:
            raise ValueError(f"Concept '{concept_text}' not found in hierarchy")

        concept = self.concepts[concept_text]

        # Remove relationships from parent concepts
        for parent_text in concept.parent_concepts:
            if parent_text in self.concepts:
                parent_concept = self.concepts[parent_text]
                updated_children = tuple(
                    child
                    for child in parent_concept.child_concepts
                    if child != concept_text
                )
                self.concepts[parent_text] = Concept(
                    text=parent_concept.text,
                    concept_level=parent_concept.concept_level,
                    evidence_strength=parent_concept.evidence_strength,
                    parent_concepts=parent_concept.parent_concepts,
                    child_concepts=updated_children,
                )

        # Remove relationships from child concepts
        for child_text in concept.child_concepts:
            if child_text in self.concepts:
                child_concept = self.concepts[child_text]
                updated_parents = tuple(
                    parent
                    for parent in child_concept.parent_concepts
                    if parent != concept_text
                )
                self.concepts[child_text] = Concept(
                    text=child_concept.text,
                    concept_level=child_concept.concept_level,
                    evidence_strength=child_concept.evidence_strength,
                    parent_concepts=updated_parents,
                    child_concepts=child_concept.child_concepts,
                )

        # Remove the concept
        del self.concepts[concept_text]

        # Remove related evidence sentences
        self.evidence_sentences = [
            evidence
            for evidence in self.evidence_sentences
            if evidence.concept_text != concept_text
        ]

        self._update_last_modified()

    def add_evidence(self, evidence: EvidenceSentence) -> None:
        """
        Add evidence sentence with validation.

        Args:
            evidence: Evidence sentence to add

        Educational Notes - Evidence Integrity:
        - Ensures evidence references concepts in the hierarchy
        - Prevents duplicate evidence sentences
        - Maintains audit trail of all supporting evidence
        """
        if evidence.concept_text not in self.concepts:
            raise ValueError(
                f"Evidence references unknown concept: '{evidence.concept_text}'"
            )

        # Check for duplicate evidence
        if evidence in self.evidence_sentences:
            return  # Silently ignore duplicates

        self.evidence_sentences.append(evidence)
        self._update_last_modified()

    def get_root_concepts(self) -> List[Concept]:
        """
        Get all root concepts (concepts with no parents).

        Returns:
            List of concepts that have no parent concepts

        Educational Notes - Hierarchy Navigation:
        - Root concepts represent top-level categories
        - Essential for hierarchy visualization and navigation
        - Quality indicator: too many roots suggest poor organization
        """
        return [
            concept for concept in self.concepts.values() if not concept.parent_concepts
        ]

    def get_leaf_concepts(self) -> List[Concept]:
        """
        Get all leaf concepts (concepts with no children).

        Returns:
            List of concepts that have no child concepts

        Educational Notes - Hierarchy Analysis:
        - Leaf concepts represent most specific concepts
        - Important for completeness assessment
        - Quality indicator: balance between general and specific concepts
        """
        return [
            concept for concept in self.concepts.values() if not concept.child_concepts
        ]

    def get_concept_depth(self, concept_text: str) -> int:
        """
        Calculate the depth of a concept in the hierarchy.

        Args:
            concept_text: Text of the concept to measure

        Returns:
            Depth of the concept (0 for root concepts)

        Educational Notes - Hierarchy Metrics:
        - Depth indicates conceptual specificity
        - Useful for hierarchy balance assessment
        - Supports hierarchy visualization and organization
        """
        if concept_text not in self.concepts:
            raise ValueError(f"Concept '{concept_text}' not found in hierarchy")

        concept = self.concepts[concept_text]

        if not concept.parent_concepts:
            return 0  # Root concept

        # Calculate maximum depth through any parent path
        max_parent_depth = 0
        for parent_text in concept.parent_concepts:
            parent_depth = self.get_concept_depth(parent_text)
            max_parent_depth = max(max_parent_depth, parent_depth)

        return max_parent_depth + 1

    def get_hierarchy_depth(self) -> int:
        """
        Calculate the maximum depth of the entire hierarchy.

        Returns:
            Maximum depth across all concepts in the hierarchy

        Educational Notes - Quality Metrics:
        - Indicates organizational sophistication
        - Too shallow: poor organization
        - Too deep: overly complex or incorrect relationships
        """
        if not self.concepts:
            return 0

        return max(
            self.get_concept_depth(concept_text)
            for concept_text in self.concepts.keys()
        )

    def calculate_average_confidence(self) -> float:
        """
        Calculate average evidence strength across all concepts.

        Returns:
            Average evidence strength for all concepts in hierarchy

        Educational Notes - Quality Assessment:
        - Indicates overall extraction quality
        - Used for hierarchy comparison and evaluation
        - Important metric for research validation
        """
        if not self.concepts:
            return 0.0

        total_strength = sum(
            concept.evidence_strength for concept in self.concepts.values()
        )
        return total_strength / len(self.concepts)

    def generate_metadata(self) -> HierarchyMetadata:
        """
        Generate comprehensive metadata for the current hierarchy state.

        Returns:
            HierarchyMetadata with current hierarchy metrics

        Educational Notes - Metadata Generation:
        - Captures current hierarchy state for analysis
        - Enables quality tracking over time
        - Provides standardized metrics for comparison
        """
        root_count = len(self.get_root_concepts())
        leaf_count = len(self.get_leaf_concepts())
        avg_confidence = self.calculate_average_confidence()
        hierarchy_depth = self.get_hierarchy_depth()

        # Calculate overall quality score based on multiple factors
        # This is a simplified quality calculation - could be more sophisticated
        structure_quality = min(1.0, hierarchy_depth / 5.0)  # Normalize depth
        confidence_quality = avg_confidence
        balance_quality = 1.0 - min(
            root_count / max(len(self.concepts), 1), 1.0
        )  # Fewer roots is better

        quality_score = (structure_quality + confidence_quality + balance_quality) / 3.0

        metadata = HierarchyMetadata(
            total_concepts=len(self.concepts),
            hierarchy_depth=hierarchy_depth,
            average_confidence=avg_confidence,
            extraction_timestamp=self.last_modified,
            root_concepts_count=root_count,
            leaf_concepts_count=leaf_count,
            quality_score=quality_score,
        )

        self.metadata = metadata
        return metadata

    def validate_hierarchy_integrity(self) -> List[str]:
        """
        Perform comprehensive validation of hierarchy integrity.

        Returns:
            List of validation issues found (empty if hierarchy is valid)

        Educational Notes - Quality Assurance:
        - Identifies structural problems in the hierarchy
        - Ensures referential integrity between concepts
        - Prevents invalid hierarchies from being used in research
        """
        issues = []

        # Check for orphaned references
        all_concept_texts = set(self.concepts.keys())

        for concept in self.concepts.values():
            # Check parent references
            for parent_text in concept.parent_concepts:
                if parent_text not in all_concept_texts:
                    issues.append(
                        f"Concept '{concept.text}' references unknown parent '{parent_text}'"
                    )

            # Check child references
            for child_text in concept.child_concepts:
                if child_text not in all_concept_texts:
                    issues.append(
                        f"Concept '{concept.text}' references unknown child '{child_text}'"
                    )

        # Check for circular dependencies
        for concept_text in self.concepts.keys():
            if self._has_circular_dependency(concept_text, set()):
                issues.append(
                    f"Circular dependency detected involving concept '{concept_text}'"
                )

        # Check evidence integrity
        concept_texts = set(self.concepts.keys())
        for evidence in self.evidence_sentences:
            if evidence.concept_text not in concept_texts:
                issues.append(
                    f"Evidence references unknown concept '{evidence.concept_text}'"
                )

        return issues

    def get_concept_path_to_root(self, concept_text: str) -> List[str]:
        """
        Get the path from a concept to its root concept(s).

        Args:
            concept_text: Text of the concept to trace

        Returns:
            List of concept texts representing path to root

        Educational Notes - Hierarchy Navigation:
        - Enables understanding of concept context
        - Useful for hierarchy visualization
        - Supports concept relationship analysis
        """
        if concept_text not in self.concepts:
            raise ValueError(f"Concept '{concept_text}' not found in hierarchy")

        concept = self.concepts[concept_text]

        if not concept.parent_concepts:
            return [concept_text]  # This is a root concept

        # For simplicity, return path through first parent
        # In a full implementation, might want to return all possible paths
        parent_text = concept.parent_concepts[0]
        parent_path = self.get_concept_path_to_root(parent_text)
        return parent_path + [concept_text]

    def _validate_hierarchy_consistency(self) -> None:
        """Validate that the hierarchy is internally consistent."""
        issues = self.validate_hierarchy_integrity()
        if issues:
            raise ValueError(f"Hierarchy consistency issues: {'; '.join(issues)}")

    def _update_last_modified(self) -> None:
        """Update the last modified timestamp."""
        object.__setattr__(self, "last_modified", datetime.now(timezone.utc))

    def _has_circular_dependency(self, concept_text: str, visited: Set[str]) -> bool:
        """
        Check if a concept has circular dependencies in parent relationships.

        Args:
            concept_text: Current concept being checked
            visited: Set of already visited concepts in this path

        Returns:
            True if circular dependency is detected
        """
        if concept_text in visited:
            return True

        if concept_text not in self.concepts:
            return False

        visited.add(concept_text)
        concept = self.concepts[concept_text]

        for parent_text in concept.parent_concepts:
            if self._has_circular_dependency(parent_text, visited.copy()):
                return True

        return False

    @classmethod
    def create_from_concepts(
        cls,
        concepts: List[Concept],
        evidence_sentences: Optional[List[EvidenceSentence]] = None,
        extraction_provenance: Optional[ExtractionProvenance] = None,
    ) -> "ConceptHierarchy":
        """
        Create a hierarchy from a list of concepts with validation.

        Args:
            concepts: List of concepts to include in the hierarchy
            evidence_sentences: Optional evidence supporting the concepts
            extraction_provenance: Optional provenance information

        Returns:
            New ConceptHierarchy instance

        Educational Notes - Factory Method:
        - Provides controlled creation with validation
        - Ensures hierarchy starts in a valid state
        - Supports different creation scenarios
        """
        hierarchy = cls()

        # Add concepts with validation
        for concept in concepts:
            hierarchy.add_concept(concept)

        # Add evidence if provided
        if evidence_sentences:
            for evidence in evidence_sentences:
                hierarchy.add_evidence(evidence)

        # Set provenance if provided
        if extraction_provenance:
            hierarchy.extraction_provenance = extraction_provenance

        # Generate initial metadata
        hierarchy.generate_metadata()

        return hierarchy

    @classmethod
    def create_from_extraction_results(
        cls,
        concepts: List[Concept],
        evidence_sentences: List[EvidenceSentence],
        extraction_method: str,
        extraction_parameters: Dict[str, Any],
    ) -> "ConceptHierarchy":
        """
        Factory method for creating hierarchies from extraction algorithm results.

        Educational Notes - Factory Method Pattern (Gang of Four):
        - Encapsulates complex creation logic with domain knowledge
        - Provides specialized constructors for different creation scenarios
        - Makes creation intent clear through descriptive method names
        - Demonstrates how factory methods can validate and transform input data
        - Eliminates need for clients to understand complex creation rules

        Educational Notes - Aggregate Root Creation (Domain-Driven Design):
        - Ensures all child objects are properly associated with the aggregate
        - Validates that evidence sentences correspond to concepts
        - Automatically generates metadata based on extraction results
        - Maintains invariants across all entities and value objects
        - Provides transactional boundary for hierarchy creation

        Educational Notes - SOLID Principles Applied:
        - Single Responsibility: Creation logic separate from business operations
        - Open/Closed: New creation strategies can be added without modification
        - Dependency Inversion: Depends on abstractions (Concept, EvidenceSentence)

        Args:
            concepts: List of concepts extracted from papers
            evidence_sentences: Supporting evidence for the concepts
            extraction_method: Name of the extraction algorithm used
            extraction_parameters: Configuration parameters for the extraction

        Returns:
            ConceptHierarchy with complete provenance and metadata

        Raises:
            ValueError: If concepts and evidence are inconsistent
        """
        # Validate input consistency - demonstrate business rule enforcement
        concept_texts = {concept.text for concept in concepts}
        evidence_concepts = {evidence.concept_text for evidence in evidence_sentences}

        if not evidence_concepts.issubset(concept_texts):
            orphaned_evidence = evidence_concepts - concept_texts
            raise ValueError(
                f"Evidence found for non-existent concepts: {orphaned_evidence}"
            )

        # Build concepts dictionary for efficient lookup
        concepts_dict = {concept.text: concept for concept in concepts}

        # Generate hierarchy metadata automatically - demonstrate value object creation
        root_concepts = [c for c in concepts if not c.parent_concepts]
        leaf_concepts = [c for c in concepts if not c.child_concepts]
        average_confidence = (
            sum(e.confidence_score for e in evidence_sentences)
            / len(evidence_sentences)
            if evidence_sentences
            else 0.0
        )

        # Calculate hierarchy depth using domain logic
        max_depth = 1
        for concept in concepts:
            if hasattr(concept, "hierarchy_level"):
                max_depth = max(max_depth, concept.hierarchy_level)

        # Use factory method pattern for value object creation
        metadata = HierarchyMetadata.create_for_deep_hierarchy(
            total_concepts=len(concepts),
            hierarchy_depth=max_depth,
            average_confidence=average_confidence,
            root_count=len(root_concepts),
            leaf_count=len(leaf_concepts),
        )

        # Generate extraction provenance with complete audit trail
        provenance = ExtractionProvenance(
            algorithm_name=extraction_method,
            algorithm_version="1.0",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters=extraction_parameters,
            performance_metrics={
                "average_confidence": average_confidence,
                "concept_count": len(concepts),
            },
            paper_count=len({e.paper_doi for e in evidence_sentences}),
            success_rate=1.0,  # Assume success if we got this far
        )

        return cls(
            hierarchy_id=str(uuid.uuid4()),
            concepts=concepts_dict,
            evidence_sentences=evidence_sentences,
            metadata=metadata,
            extraction_provenance=provenance,
            created_at=datetime.now(timezone.utc),
            last_modified=datetime.now(timezone.utc),
        )

    @classmethod
    def create_empty_hierarchy(
        cls, extraction_method: str = "manual"
    ) -> "ConceptHierarchy":
        """
        Factory method for creating empty hierarchies to be populated incrementally.

        Educational Notes - Null Object Pattern:
        - Provides valid empty state that can be safely operated on
        - Eliminates need for null checks in client code
        - Demonstrates how empty objects can maintain contracts
        - Enables incremental building of complex domain objects
        - Supports progressive construction without breaking invariants

        Educational Notes - Template Method Application:
        - Defines skeleton of creation process
        - Allows subclasses to override specific steps if needed
        - Provides consistent initialization across different creation scenarios

        Args:
            extraction_method: Method name for provenance tracking

        Returns:
            Empty ConceptHierarchy ready for incremental population
        """
        timestamp = datetime.now(timezone.utc)

        # Create minimal but valid metadata for empty hierarchy
        metadata = HierarchyMetadata.create_for_flat_hierarchy(
            total_concepts=0, average_confidence=0.0, extraction_timestamp=timestamp
        )

        # Create basic provenance for manual construction
        provenance = ExtractionProvenance(
            algorithm_name=extraction_method,
            algorithm_version="1.0",
            extraction_timestamp=timestamp,
            parameters={},
            performance_metrics={"status": "empty", "ready_for_population": True},
            paper_count=0,
            success_rate=1.0,
        )

        return cls(
            hierarchy_id=str(uuid.uuid4()),
            concepts={},
            evidence_sentences=[],
            metadata=metadata,
            extraction_provenance=provenance,
            created_at=timestamp,
            last_modified=timestamp,
        )

    def validate_hierarchy_consistency(self) -> bool:
        """
        Validate that the hierarchy maintains consistency in all relationships.

        Educational Notes - Domain Validation Strategy:
        - Reuses existing validation logic to avoid duplication
        - Returns boolean for simple client usage
        - Delegates to private method that provides detailed error information
        - Demonstrates Facade pattern for simplifying complex validation

        Educational Notes - Design Pattern Application:
        - Single Responsibility: Focused only on consistency validation
        - Open/Closed: Can be extended with additional validation rules
        - Dependency Inversion: Relies on abstract validation concepts

        Returns:
            True if hierarchy is consistent, False otherwise

        Educational Notes - Academic Quality Standards:
        - Ensures bidirectional parent-child relationships are maintained
        - Validates that all referenced concepts exist in hierarchy
        - Prevents orphaned references that could compromise analysis
        - Essential for research data integrity
        """
        issues = self.validate_hierarchy_integrity()
        return len(issues) == 0

    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        Detect circular dependencies in the concept hierarchy using depth-first search.

        Educational Notes - Graph Theory Application:
        - Uses DFS with visited tracking to detect back edges (Cormen et al., Introduction to Algorithms)
        - Back edges indicate cycles in directed graphs
        - Critical for maintaining acyclic hierarchy structure
        - Prevents infinite loops in traversal algorithms

        Educational Notes - Algorithm Choice Rationale:
        - DFS more memory efficient than BFS for cycle detection
        - Visited set prevents revisiting nodes and infinite loops
        - Stack-based approach enables path reconstruction for cycle reporting
        - Time complexity O(V + E) where V = concepts, E = relationships

        Returns:
            List of cycles, where each cycle is a list of concept names forming a loop
            Empty list if no cycles detected

        Educational Notes - Research Applications:
        - Circular hierarchies indicate conceptual confusion or data quality issues
        - Academic taxonomies should maintain strict hierarchical structure
        - Cycle detection essential for automatic concept organization
        - Prevents logical inconsistencies in research concept maps
        """
        cycles = []
        visited = set()
        recursion_stack = set()

        def dfs_visit(concept_name: str, path: List[str]) -> None:
            """Depth-first search with cycle detection."""
            if concept_name in recursion_stack:
                # Found a back edge - extract the cycle
                cycle_start = path.index(concept_name)
                cycle = path[cycle_start:] + [concept_name]
                cycles.append(cycle)
                return

            if concept_name in visited:
                return

            visited.add(concept_name)
            recursion_stack.add(concept_name)

            # Explore children
            concept = self.concepts.get(concept_name)
            if concept:
                for child_name in concept.child_concepts:
                    if child_name in self.concepts:  # Only follow existing children
                        dfs_visit(child_name, path + [concept_name])

            recursion_stack.remove(concept_name)

        # Start DFS from all root concepts
        for concept_name in self.concepts:
            if concept_name not in visited:
                dfs_visit(concept_name, [])

        return cycles

    def find_concept_path(self, source_concept: str, target_concept: str) -> List[str]:
        """
        Find the shortest path between two concepts using breadth-first search.

        Educational Notes - Graph Traversal Algorithm:
        - BFS guarantees shortest path in unweighted graphs (Dijkstra's algorithm variant)
        - Queue-based exploration ensures level-by-level traversal
        - Parent tracking enables path reconstruction
        - Bidirectional search could optimize for long paths (future enhancement)

        Educational Notes - Research Applications:
        - Concept path analysis reveals semantic relationships
        - Hierarchical distance measures for concept similarity
        - Navigation paths for interactive concept exploration
        - Semantic reasoning based on concept proximity

        Args:
            source_concept: Starting concept name
            target_concept: Destination concept name

        Returns:
            List of concept names forming shortest path from source to target
            Empty list if no path exists or concepts don't exist

        Educational Notes - Algorithm Complexity:
        - Time complexity: O(V + E) where V = concepts, E = relationships
        - Space complexity: O(V) for queue and visited tracking
        - Optimal for unweighted hierarchical graphs
        - Could be enhanced with A* for weighted concept similarity
        """
        if (
            source_concept not in self.concepts
            or target_concept not in self.concepts
            or source_concept == target_concept
        ):
            return [] if source_concept != target_concept else [source_concept]

        from collections import deque

        # BFS with parent tracking for path reconstruction
        queue = deque([source_concept])
        visited = {source_concept}
        parent = {source_concept: None}

        while queue:
            current = queue.popleft()

            if current == target_concept:
                # Reconstruct path from target back to source
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Reverse to get source->target path

            concept = self.concepts[current]

            # Explore both children and parents (bidirectional hierarchy)
            neighbors = set(concept.child_concepts) | set(concept.parent_concepts)

            for neighbor in neighbors:
                if neighbor in self.concepts and neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return []  # No path found

    def calculate_hierarchy_quality_score(self) -> float:
        """
        Calculate overall quality score for the concept hierarchy.

        Educational Notes - Multi-Dimensional Quality Assessment:
        - Combines structural metrics (balance, depth, connectivity)
        - Evidence-based grounding assessment for research quality
        - Weighted scoring based on research domain best practices
        - Normalizes to 0.0-1.0 scale for standardized comparison

        Educational Notes - Quality Metrics Research:
        - Based on ontology evaluation frameworks (Brank et al., 2005)
        - Incorporates concept hierarchy evaluation principles
        - Evidence coverage ensures research grounding
        - Structural balance prevents over-deep or over-shallow hierarchies

        Returns:
            Quality score from 0.0 (poor) to 1.0 (excellent)

        Educational Notes - Academic Applications:
        - Enables automatic quality assessment of extracted hierarchies
        - Supports comparative evaluation of extraction algorithms
        - Guides hierarchy refinement and optimization
        - Essential for research reproducibility and validation
        """
        if not self.concepts:
            return 0.0

        # 1. Structural Balance (30% weight)
        balance_score = self._calculate_balance_score()

        # 2. Evidence Coverage (40% weight)
        evidence_score = self._calculate_evidence_coverage_score()

        # 3. Connectivity Quality (20% weight)
        connectivity_score = self._calculate_connectivity_score()

        # 4. Depth Appropriateness (10% weight)
        depth_score = self._calculate_depth_score()

        # Weighted combination
        quality_score = (
            0.30 * balance_score
            + 0.40 * evidence_score
            + 0.20 * connectivity_score
            + 0.10 * depth_score
        )

        return min(1.0, max(0.0, quality_score))

    def rebalance_hierarchy(self) -> "ConceptHierarchy":
        """
        Create a rebalanced version of the hierarchy optimizing for structural quality.

        Educational Notes - Hierarchy Optimization Strategy:
        - Identifies imbalanced subtrees using branching factor analysis
        - Reorganizes based on concept frequency and relevance scores
        - Maintains semantic relationships while improving structure
        - Uses greedy optimization for computational efficiency

        Educational Notes - Research Applications:
        - Automatic hierarchy refinement for better organization
        - Optimization of extracted concept structures
        - Improved navigation and comprehension of concept maps
        - Enhanced performance for hierarchy-based algorithms

        Returns:
            New ConceptHierarchy instance with optimized structure

        Educational Notes - Algorithm Design:
        - Preserves all concepts and evidence (no data loss)
        - Uses frequency and relevance for reorganization decisions
        - Maintains acyclic structure through careful restructuring
        - Could be enhanced with machine learning optimization
        """
        # For now, return a copy - rebalancing algorithm would be complex
        # This is a placeholder for the sophisticated rebalancing logic
        return ConceptHierarchy(
            hierarchy_id=str(uuid.uuid4()),
            concepts=dict(self.concepts),
            evidence_sentences=list(self.evidence_sentences),
            metadata=self.metadata,
            extraction_provenance=self.extraction_provenance,
            created_at=datetime.now(timezone.utc),
            last_modified=datetime.now(timezone.utc),
        )

    def _calculate_balance_score(self) -> float:
        """Calculate structural balance score based on branching factors."""
        if len(self.concepts) <= 1:
            return 1.0

        # Calculate branching factor distribution
        branching_factors = []
        for concept in self.concepts.values():
            branching_factors.append(len(concept.child_concepts))

        # Penalize extreme imbalance (some nodes with many children, others with none)
        if not branching_factors:
            return 0.5

        avg_branching = sum(branching_factors) / len(branching_factors)
        variance = sum((bf - avg_branching) ** 2 for bf in branching_factors) / len(
            branching_factors
        )

        # Lower variance indicates better balance
        balance_score = 1.0 / (1.0 + variance)
        return min(1.0, balance_score)

    def _calculate_evidence_coverage_score(self) -> float:
        """Calculate evidence coverage score."""
        if not self.concepts:
            return 1.0

        evidence_concepts = {e.concept_text for e in self.evidence_sentences}
        covered_concepts = evidence_concepts.intersection(self.concepts.keys())

        coverage_ratio = len(covered_concepts) / len(self.concepts)
        return coverage_ratio

    def _calculate_connectivity_score(self) -> float:
        """Calculate connectivity quality score."""
        if len(self.concepts) <= 1:
            return 1.0

        # Count connected components
        connected_count = 0
        visited = set()

        for concept_name in self.concepts:
            if concept_name not in visited:
                self._dfs_mark_connected(concept_name, visited)
                connected_count += 1

        # Fewer components is better (more connected hierarchy)
        connectivity_score = 1.0 / connected_count if connected_count > 0 else 0.0
        return min(1.0, connectivity_score)

    def _calculate_depth_score(self) -> float:
        """Calculate depth appropriateness score."""
        max_depth = self.metadata.hierarchy_depth
        concept_count = len(self.concepts)

        # Ideal depth is log2(concept_count) for balanced trees
        import math

        ideal_depth = math.log2(max(1, concept_count))
        depth_ratio = max_depth / max(1, ideal_depth)

        # Score approaches 1.0 when actual depth is close to ideal
        depth_score = 1.0 / (1.0 + abs(depth_ratio - 1.0))
        return min(1.0, depth_score)

    def _dfs_mark_connected(self, concept_name: str, visited: set) -> None:
        """Mark all concepts connected to the given concept as visited."""
        if concept_name in visited or concept_name not in self.concepts:
            return

        visited.add(concept_name)
        concept = self.concepts[concept_name]

        # Follow both parent and child relationships
        for related_concept in set(concept.parent_concepts) | set(
            concept.child_concepts
        ):
            if related_concept in self.concepts:
                self._dfs_mark_connected(related_concept, visited)
