"""
ConceptHierarchyBuilder - Advanced domain service for automated concept hierarchy construction.

This domain service implements sophisticated algorithms for transforming flat concept lists
into rich hierarchical knowledge structures using semantic analysis, frequency heuristics,
and evidence-based relationship detection.

Educational Notes - Clean Architecture Principles:
- Domain Service Pattern: Complex business logic that spans multiple entities
- Dependency Inversion: Operates on domain entities, independent of infrastructure concerns
- Single Responsibility: Focused solely on hierarchy construction algorithms
- Open/Closed: Extensible through configuration without modifying core algorithms

Educational Notes - Advanced Algorithms:
- Semantic Similarity: Cosine similarity between embedding vectors for relationship detection
- Parent-Child Heuristics: Frequency-based generality detection + semantic similarity scoring
- Cycle Prevention: Single-parent selection algorithm ensures clean tree structures
- Evidence Grounding: Multi-factor scoring combining frequency, relevance, and text coverage
- Hierarchical Leveling: Breadth-first traversal for consistent depth assignment

Algorithm Complexity Analysis:
- build_hierarchy(): O(n²) for pairwise similarity + O(n+r) for BFS traversal
- Memory complexity: O(n+r) where n=concepts, r=relationships
- Critical bottleneck: Similarity matrix calculation for large concept sets (>1000)

Design Patterns Demonstrated:
- Strategy Pattern: Configurable thresholds adapt algorithm behavior to domains
- Template Method: build_hierarchy() orchestrates well-defined algorithmic phases
- Builder Pattern: Immutable concept enhancement with new relationship data
- Extract Method: Complex algorithms decomposed into focused helper methods

Research Applications:
- Transform research paper concept extractions into structured knowledge graphs
- Enable D3.js visualization of concept hierarchies for research exploration
- Support evidence-based filtering of low-quality concepts in academic literature
- Facilitate semantic search and concept recommendation in research databases

Performance Considerations:
- O(n²) similarity calculations become expensive for >1000 concepts
- Embedding vector operations benefit from numpy vectorization
- Relationship filtering reduces memory footprint for sparse hierarchies
- Breadth-first traversal scales well with hierarchy depth variations
"""

from typing import List, Dict, Set, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import uuid
from collections import defaultdict, deque

from src.domain.entities.concept import Concept


@dataclass
class HierarchyConfiguration:
    """
    Configuration parameters for concept hierarchy building.

    Educational Notes:
    - Demonstrates configuration pattern for domain services
    - Allows customization for different research domains
    - Provides sensible defaults based on research experience
    - Enables algorithm tuning without code changes
    """

    similarity_threshold: float = 0.7  # Minimum similarity for any relationship
    parent_child_threshold: float = 0.6  # Threshold for parent-child relationship
    cluster_threshold: float = 0.8  # Higher threshold for tight clustering
    evidence_weight_factor: float = 0.1  # Weight for text-based evidence calculation
    frequency_ratio_threshold: float = 2.0  # Min ratio for parent-child by frequency


class ConceptHierarchyBuilder:
    """
    Domain service for building hierarchical concept structures.

    Educational Notes:
    - Domain service pattern for complex business operations
    - Uses semantic analysis to detect conceptual relationships
    - Maintains immutability of all concept entities
    - Configurable algorithms for different research domains

    The hierarchy building process:
    1. Calculate semantic similarities between all concept pairs
    2. Detect parent-child relationships using similarity and frequency heuristics
    3. Assign concept levels based on hierarchy depth from roots
    4. Create semantic clusters for concepts not in hierarchy relationships
    5. Calculate evidence strength for each concept based on multiple factors
    """

    def __init__(
        self,
        similarity_threshold: float = 0.7,
        parent_child_threshold: float = 0.6,
        cluster_threshold: float = 0.8,
        evidence_weight_factor: float = 0.1,
    ):
        """
        Initialize hierarchy builder with configuration parameters.

        Args:
            similarity_threshold: Minimum similarity for any relationship detection [0,1]
            parent_child_threshold: Minimum similarity for parent-child relationships [0,1]
            cluster_threshold: Minimum similarity for concept clustering [0,1]
            evidence_weight_factor: Weight factor for text-based evidence calculation [0,1]

        Educational Notes:
        - Constructor validation prevents algorithmic errors downstream
        - Reasonable defaults based on empirical research concept analysis
        - Each threshold controls different aspects of hierarchy construction
        - Lower thresholds = more permissive relationships, higher = stricter

        Raises:
            ValueError: If any threshold is outside valid range [0,1]
        """
        # Validate all threshold parameters
        self._validate_threshold("similarity_threshold", similarity_threshold)
        self._validate_threshold("parent_child_threshold", parent_child_threshold)
        self._validate_threshold("cluster_threshold", cluster_threshold)
        self._validate_threshold("evidence_weight_factor", evidence_weight_factor)

        # Store validated parameters
        self.similarity_threshold = similarity_threshold
        self.parent_child_threshold = parent_child_threshold
        self.cluster_threshold = cluster_threshold
        self.evidence_weight_factor = evidence_weight_factor

    def _validate_threshold(self, name: str, value: float) -> None:
        """
        Validate that a threshold parameter is within acceptable range.

        Args:
            name: Parameter name for error messages
            value: Threshold value to validate

        Raises:
            ValueError: If value is not in range [0,1]

        Educational Notes:
        - Helper method following DRY principle
        - Provides clear error messages for debugging
        - Centralizes validation logic for maintainability
        """
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")

    def build_hierarchy(self, concepts: List[Concept]) -> List[Concept]:
        """
        Build hierarchical relationships from flat concept list.

        Educational Notes:
        - Main orchestration method that coordinates all hierarchy building steps
        - Demonstrates complex domain logic coordination in Clean Architecture
        - Preserves immutability by creating new concept instances
        - Handles edge cases gracefully (no embeddings, circular relationships)

        Args:
            concepts: Flat list of concepts to organize hierarchically

        Returns:
            List of concepts with hierarchical relationships established
        """
        if not concepts:
            return []

        # Step 1: Detect parent-child relationships using semantic similarity
        relationships = self.detect_parent_child_relationships(concepts)

        # Step 2: Assign hierarchical levels based on detected relationships
        concept_levels = self.assign_concept_levels(concepts, relationships)

        # Step 3: Create semantic clusters for related but non-hierarchical concepts
        clusters = self.create_concept_clusters(concepts)

        # Step 4: Build new concept instances with hierarchy information
        hierarchical_concepts = []
        for concept in concepts:
            # Calculate parent and child sets for this concept
            parents = set()
            children = set()

            # Find parents (concepts that have this as a child)
            for parent_text, child_set in relationships.items():
                if concept.text in child_set:
                    parents.add(parent_text)

            # Find children (concepts this has as children)
            if concept.text in relationships:
                children = relationships[concept.text]

            # Calculate evidence strength
            evidence_strength = self.calculate_evidence_strength(concept)

            # Create new concept with hierarchy information
            hierarchical_concept = Concept(
                text=concept.text,
                frequency=concept.frequency,
                relevance_score=concept.relevance_score,
                source_papers=concept.source_papers,
                source_domain=concept.source_domain,
                extraction_method=concept.extraction_method,
                created_at=concept.created_at,
                synonyms=concept.synonyms,
                embedding=concept.embedding,
                parent_concepts=parents,
                child_concepts=children,
                concept_level=concept_levels.get(concept.text, 0),
                cluster_id=clusters.get(concept.text),
                evidence_strength=evidence_strength,
            )

            hierarchical_concepts.append(hierarchical_concept)

        return hierarchical_concepts

    def calculate_semantic_similarity(
        self, concept1: Concept, concept2: Concept
    ) -> float:
        """
        Calculate semantic similarity between two concepts using embeddings.

        Educational Notes:
        - Demonstrates semantic analysis in domain services
        - Uses cosine similarity for vector comparison
        - Handles cases where embeddings are missing gracefully
        - Returns normalized similarity score for consistent comparison

        Args:
            concept1: First concept for comparison
            concept2: Second concept for comparison

        Returns:
            Cosine similarity score between 0.0 and 1.0 (0.0 if no embeddings)
        """
        if not concept1.embedding or not concept2.embedding:
            return 0.0

        # Calculate cosine similarity between embedding vectors
        vec1 = concept1.embedding.vector
        vec2 = concept2.embedding.vector

        # Handle edge case of zero vectors
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(vec1, vec2) / (norm1 * norm2)

    def detect_parent_child_relationships(
        self, concepts: List[Concept]
    ) -> Dict[str, Set[str]]:
        """
        Detect parent-child relationships using similarity and frequency heuristics.

        Educational Notes:
        - Complex business logic for relationship detection
        - Uses multiple heuristics: semantic similarity + frequency analysis
        - Higher frequency concepts typically represent more general categories
        - Lower frequency concepts represent more specific instances
        - Prevents circular relationships through careful ordering
        - Creates proper hierarchy by selecting most similar parent for each child

        Args:
            concepts: List of concepts to analyze for relationships

        Returns:
            Dictionary mapping parent concept text to set of child concept texts
        """
        # First pass: find all potential relationships
        potential_relationships: List[Tuple[str, str, float, int]] = []

        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts):
                if i >= j:  # Avoid duplicate comparisons and self-comparison
                    continue

                similarity = self.calculate_semantic_similarity(concept1, concept2)

                # Skip if similarity too low for any relationship
                if similarity < self.parent_child_threshold:
                    continue

                # Determine parent-child relationship based on frequency heuristic
                # Higher frequency concept is typically more general (parent)
                if concept1.frequency > concept2.frequency:
                    # concept1 might be parent of concept2
                    if (
                        concept1.frequency >= concept2.frequency * 1.5
                    ):  # More restrictive threshold
                        freq_ratio = concept1.frequency / concept2.frequency
                        potential_relationships.append(
                            (concept1.text, concept2.text, similarity, freq_ratio)
                        )
                elif concept2.frequency > concept1.frequency:
                    # concept2 might be parent of concept1
                    if (
                        concept2.frequency >= concept1.frequency * 1.5
                    ):  # More restrictive threshold
                        freq_ratio = concept2.frequency / concept1.frequency
                        potential_relationships.append(
                            (concept2.text, concept1.text, similarity, freq_ratio)
                        )

        # Second pass: select best parent for each child to avoid multiple parents
        relationships: Dict[str, Set[str]] = defaultdict(set)
        child_to_best_parent: Dict[str, Tuple[str, float]] = (
            {}
        )  # child -> (parent, combined_score)

        for parent, child, similarity, freq_ratio in potential_relationships:
            # Combined score strongly favors similarity over frequency difference
            # This creates proper hierarchical chains rather than flat parent-child pairs
            combined_score = similarity * 0.9 + min(
                freq_ratio / 20.0, 0.1
            )  # Cap freq bonus at 0.1

            if (
                child not in child_to_best_parent
                or combined_score > child_to_best_parent[child][1]
            ):
                child_to_best_parent[child] = (parent, combined_score)

        # Build final relationships from best parent selections
        for child, (parent, _) in child_to_best_parent.items():
            relationships[parent].add(child)

        return dict(relationships)

    def assign_concept_levels(
        self, concepts: List[Concept], relationships: Dict[str, Set[str]]
    ) -> Dict[str, int]:
        """
        Assign hierarchical levels to concepts based on parent-child relationships.

        Educational Notes:
        - Implements breadth-first traversal for level assignment
        - Root concepts (no parents) get level 0
        - Each child level is parent level + 1
        - Handles disconnected concepts by making them roots
        - Prevents infinite loops in case of circular relationships

        Args:
            concepts: List of all concepts
            relationships: Parent-child relationship mapping

        Returns:
            Dictionary mapping concept text to hierarchical level
        """
        levels: Dict[str, int] = {}

        # Find all concept texts that appear as children
        all_children = set()
        for children_set in relationships.values():
            all_children.update(children_set)

        # Root concepts are those that appear as parents but not as children
        root_concepts = set(relationships.keys()) - all_children

        # Also include concepts not in any relationships as roots
        all_concept_texts = {concept.text for concept in concepts}
        concepts_in_relationships = set(relationships.keys()) | all_children
        unrelated_concepts = all_concept_texts - concepts_in_relationships
        root_concepts.update(unrelated_concepts)

        # If no roots found, make all concepts roots (disconnected graph)
        if not root_concepts:
            return {concept.text: 0 for concept in concepts}

        # Breadth-first assignment of levels
        queue = deque([(root, 0) for root in root_concepts])

        while queue:
            concept_text, level = queue.popleft()

            # Skip if already assigned (handles potential cycles)
            if concept_text in levels:
                continue

            levels[concept_text] = level

            # Add children to queue with increased level
            if concept_text in relationships:
                for child in relationships[concept_text]:
                    if child not in levels:  # Avoid revisiting
                        queue.append((child, level + 1))

        return levels

    def create_concept_clusters(self, concepts: List[Concept]) -> Dict[str, str]:
        """
        Create semantic clusters of highly similar concepts.

        Educational Notes:
        - Demonstrates clustering algorithm for concept organization
        - Uses higher similarity threshold than parent-child detection
        - Creates clusters for concepts that are semantically similar but not hierarchical
        - Useful for finding synonym groups and related concept families
        - Generates unique cluster IDs for each semantic group

        Args:
            concepts: List of concepts to cluster

        Returns:
            Dictionary mapping concept text to cluster ID
        """
        clusters: Dict[str, str] = {}
        concept_to_cluster: Dict[str, str] = {}

        # Compare all concept pairs for clustering
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts):
                if i >= j:  # Avoid duplicate comparisons
                    continue

                similarity = self.calculate_semantic_similarity(concept1, concept2)

                # Only cluster highly similar concepts
                if similarity < self.cluster_threshold:
                    continue

                # Check if either concept is already clustered
                cluster_id1 = concept_to_cluster.get(concept1.text)
                cluster_id2 = concept_to_cluster.get(concept2.text)

                if cluster_id1 and cluster_id2:
                    # Both already clustered - merge clusters if different
                    if cluster_id1 != cluster_id2:
                        # Merge into cluster_id1, update all concept_id2 concepts
                        for concept_text, cluster_id in concept_to_cluster.items():
                            if cluster_id == cluster_id2:
                                concept_to_cluster[concept_text] = cluster_id1
                elif cluster_id1:
                    # Add concept2 to concept1's cluster
                    concept_to_cluster[concept2.text] = cluster_id1
                elif cluster_id2:
                    # Add concept1 to concept2's cluster
                    concept_to_cluster[concept1.text] = cluster_id2
                else:
                    # Create new cluster for both concepts
                    new_cluster_id = f"cluster_{str(uuid.uuid4())[:8]}"
                    concept_to_cluster[concept1.text] = new_cluster_id
                    concept_to_cluster[concept2.text] = new_cluster_id

        return concept_to_cluster

    def calculate_evidence_strength(
        self, concept: Concept, source_text: str = ""
    ) -> float:
        """
        Calculate evidence strength for concept grounding.

        Educational Notes:
        - Demonstrates evidence-based concept validation for research applications
        - Combines multiple indicators: frequency, relevance, paper count
        - Higher scores indicate concepts with strong textual support
        - Lower scores may indicate concepts needing manual verification
        - Uses configurable weighting for different evidence factors

        Args:
            concept: Concept to calculate evidence strength for
            source_text: Optional source text for additional evidence calculation

        Returns:
            Evidence strength score between 0.0 and 1.0
        """
        # Base evidence from concept metadata
        frequency_score = min(
            concept.frequency / 100.0, 1.0
        )  # Normalize by max expected frequency
        relevance_score = concept.relevance_score
        paper_count_score = min(
            len(concept.source_papers) / 10.0, 1.0
        )  # Normalize by max expected papers

        # Text-based evidence if source text provided
        text_score = 0.0
        if source_text and concept.text:
            # Simple text coverage calculation
            text_occurrences = source_text.lower().count(concept.text.lower())
            text_score = min(text_occurrences * self.evidence_weight_factor, 1.0)

        # Weighted combination of evidence factors
        evidence_strength = (
            frequency_score * 0.3
            + relevance_score * 0.4
            + paper_count_score * 0.2
            + text_score * 0.1
        )

        return min(evidence_strength, 1.0)  # Ensure upper bound
