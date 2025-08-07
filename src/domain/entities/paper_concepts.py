"""
PaperConcepts Entity - Links research papers with their extracted concepts.

This entity demonstrates the relationship between papers and concepts while
maintaining Clean Architecture principles and research data integrity.

Educational Notes:
- Shows Entity pattern for managing paper-concept relationships
- Demonstrates aggregation of concepts for a specific paper
- Illustrates domain logic for concept ranking and filtering
- Shows how entities can coordinate multiple domain concepts

Design Decisions:
- Paper DOI serves as primary identifier
- Concepts are stored as immutable collection
- Extraction metadata preserved for research transparency
- Concept ranking enables significance analysis
- Domain association allows cross-domain comparisons

Use Cases:
- Managing concepts extracted from individual papers
- Ranking concepts by relevance within a paper
- Filtering concepts by significance thresholds
- Generating concept summaries for papers
"""

from typing import List, Set, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone
from .concept import Concept


@dataclass(frozen=True)
class PaperConcepts:
    """
    Represents the complete set of concepts extracted from a research paper.

    This entity manages the relationship between a research paper and all
    concepts extracted from it, providing methods for analysis, filtering,
    and ranking of concepts based on various criteria.

    Attributes:
        paper_doi: DOI of the paper (primary identifier)
        paper_title: Title of the paper for reference
        concepts: List of concepts extracted from this paper
        extraction_timestamp: When concept extraction was performed
        extraction_method: Primary method used for extraction
        total_concept_count: Total number of concepts found
        processing_metadata: Additional metadata about extraction process
    """

    paper_doi: str
    paper_title: str
    concepts: List[Concept]
    extraction_timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    extraction_method: str = "mixed"
    total_concept_count: int = field(init=False)
    processing_metadata: Dict[str, str] = field(default_factory=dict)
    extraction_metadata: Optional[Dict[str, Any]] = field(default=None)  # Enhanced extraction metadata

    def __post_init__(self):
        """
        Validate business rules and compute derived attributes.

        Educational Note:
        Post-initialization validation ensures entity consistency
        and computes derived fields that depend on the concepts list.
        """
        if not self.paper_doi or not self.paper_doi.strip():
            raise ValueError("Paper DOI cannot be empty")

        if not self.paper_title or not self.paper_title.strip():
            raise ValueError("Paper title cannot be empty")

        if not isinstance(self.concepts, list):
            raise ValueError("Concepts must be provided as a list")

        # Validate all concepts belong to this paper
        for concept in self.concepts:
            if not isinstance(concept, Concept):
                raise ValueError("All items in concepts list must be Concept instances")
            if self.paper_doi not in concept.source_papers:
                raise ValueError(
                    f"Concept '{concept.text}' does not reference this paper"
                )

        # Set computed field
        object.__setattr__(self, "total_concept_count", len(self.concepts))

    def __str__(self) -> str:
        """String representation emphasizing paper identity and concept count."""
        return f"PaperConcepts({self.paper_doi}, {self.total_concept_count} concepts)"

    def __eq__(self, other) -> bool:
        """
        Equality based on paper DOI (identity).

        Educational Note:
        Entity equality based on identifier, not all attributes.
        Two PaperConcepts instances are equal if they represent
        the same paper, regardless of extraction differences.
        """
        if not isinstance(other, PaperConcepts):
            return False
        return self.paper_doi == other.paper_doi

    def __hash__(self) -> int:
        """Hash based on paper DOI for set operations."""
        return hash(self.paper_doi)

    @property
    def has_hierarchical_relationships(self) -> bool:
        """
        Check if this paper concepts contains hierarchical concept relationships.
        
        Educational Note:
        Business logic property that determines if concepts have been organized
        into hierarchical structures with parent-child relationships.
        """
        if self.extraction_metadata and self.extraction_metadata.get("has_hierarchical_relationships"):
            return True
        
        # Check if any concepts have hierarchical relationships
        for concept in self.concepts:
            if concept.parent_concepts or concept.child_concepts:
                return True
        
        return False

    def get_top_concepts(
        self, limit: int = 10, min_relevance: float = 0.0
    ) -> List[Concept]:
        """
        Get the most relevant concepts from this paper.

        Educational Note:
        Business logic method that applies domain knowledge about
        concept importance, combining relevance scores with frequency
        to identify the most significant concepts in a paper.

        Args:
            limit: Maximum number of concepts to return
            min_relevance: Minimum relevance threshold

        Returns:
            List of top concepts sorted by relevance score
        """
        if limit <= 0:
            raise ValueError("Limit must be positive")

        if not (0.0 <= min_relevance <= 1.0):
            raise ValueError("Min relevance must be between 0.0 and 1.0")

        # Filter by minimum relevance and sort by relevance score descending
        filtered_concepts = [
            concept
            for concept in self.concepts
            if concept.relevance_score >= min_relevance
        ]

        sorted_concepts = sorted(
            filtered_concepts,
            key=lambda c: (c.relevance_score, c.frequency),
            reverse=True,
        )

        return sorted_concepts[:limit]

    def get_concepts_by_method(self, extraction_method: str) -> List[Concept]:
        """
        Filter concepts by their extraction method.

        Educational Note:
        Enables analysis of extraction method effectiveness by
        allowing researchers to examine concepts found by specific
        techniques (TF-IDF, named entities, etc.).

        Args:
            extraction_method: Method used to extract concepts

        Returns:
            List of concepts extracted using the specified method
        """
        return [
            concept
            for concept in self.concepts
            if concept.extraction_method == extraction_method
        ]

    def get_significant_concepts(
        self, min_frequency: int = 2, min_relevance: float = 0.1
    ) -> List[Concept]:
        """
        Get concepts that meet significance thresholds.

        Educational Note:
        Combines multiple significance criteria to identify
        concepts that are both frequent and relevant, filtering
        out noise and low-value extractions.

        Args:
            min_frequency: Minimum frequency threshold
            min_relevance: Minimum relevance threshold

        Returns:
            List of significant concepts sorted by relevance
        """
        significant = [
            concept
            for concept in self.concepts
            if concept.is_significant(min_frequency, min_relevance)
        ]

        return sorted(significant, key=lambda c: c.relevance_score, reverse=True)

    def get_concept_distribution(self) -> Dict[str, int]:
        """
        Get distribution of concepts by extraction method.

        Educational Note:
        Provides analytics about the extraction process by showing
        how many concepts were found by each method, useful for
        evaluating extraction strategy effectiveness.

        Returns:
            Dictionary mapping extraction methods to concept counts
        """
        distribution = {}
        for concept in self.concepts:
            method = concept.extraction_method
            distribution[method] = distribution.get(method, 0) + 1

        return distribution

    def calculate_concept_diversity(self) -> float:
        """
        Calculate concept diversity using Shannon entropy.

        Educational Note:
        Applies information theory to measure conceptual diversity
        within a paper, where higher entropy indicates more diverse
        concept coverage and lower entropy indicates focused topics.

        Returns:
            Shannon entropy of concept relevance distribution
        """
        import math

        if not self.concepts:
            return 0.0

        # Calculate entropy based on relevance score distribution
        total_relevance = sum(concept.relevance_score for concept in self.concepts)
        if total_relevance == 0:
            return 0.0

        entropy = 0.0
        for concept in self.concepts:
            if concept.relevance_score > 0:
                probability = concept.relevance_score / total_relevance
                entropy -= probability * math.log2(probability)

        return entropy

    def find_concept_by_text(self, concept_text: str) -> Optional[Concept]:
        """
        Find a specific concept by its text representation.

        Educational Note:
        Provides lookup functionality for finding specific concepts
        within a paper's concept collection, useful for targeted
        analysis and concept relationship mapping.

        Args:
            concept_text: Text of the concept to find

        Returns:
            Concept instance if found, None otherwise
        """
        concept_text = concept_text.lower().strip()
        for concept in self.concepts:
            if concept.text.lower().strip() == concept_text:
                return concept
        return None

    def merge_similar_concepts(
        self, similarity_threshold: float = 0.8
    ) -> "PaperConcepts":
        """
        Create new instance with similar concepts merged.

        Educational Note:
        Demonstrates concept consolidation logic that reduces
        redundancy by merging conceptually similar terms while
        preserving research lineage through synonym tracking.

        Args:
            similarity_threshold: Minimum similarity for merging

        Returns:
            New PaperConcepts instance with merged concepts
        """
        # This is a placeholder for more sophisticated similarity detection
        # In practice, this would use semantic similarity models
        merged_concepts = []
        processed = set()

        for concept in self.concepts:
            if concept.text in processed:
                continue

            # Find similar concepts (simplified text-based matching)
            similar_concepts = [
                other
                for other in self.concepts
                if other != concept
                and other.text not in processed
                and self._is_text_similar(
                    concept.text, other.text, similarity_threshold
                )
            ]

            # Merge similar concepts
            merged_concept = concept
            for similar in similar_concepts:
                merged_concept = merged_concept.merge_with_synonym(similar)
                processed.add(similar.text)

            merged_concepts.append(merged_concept)
            processed.add(concept.text)

        return PaperConcepts(
            paper_doi=self.paper_doi,
            paper_title=self.paper_title,
            concepts=merged_concepts,
            extraction_timestamp=self.extraction_timestamp,
            extraction_method=self.extraction_method,
            processing_metadata=self.processing_metadata,
        )

    def _is_text_similar(self, text1: str, text2: str, threshold: float) -> bool:
        """
        Simple text similarity check (placeholder for more sophisticated methods).

        Educational Note:
        Simplified similarity detection that could be replaced with
        more sophisticated methods like edit distance, semantic embeddings,
        or domain-specific similarity measures.
        """
        # Simple Jaccard similarity on words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return False

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return (intersection / union) >= threshold

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Educational Note:
        Provides clean serialization interface that preserves
        all entity data and relationships for persistence or
        data exchange between system components.
        """
        return {
            "paper_doi": self.paper_doi,
            "paper_title": self.paper_title,
            "concepts": [concept.to_dict() for concept in self.concepts],
            "extraction_timestamp": self.extraction_timestamp.isoformat(),
            "extraction_method": self.extraction_method,
            "total_concept_count": self.total_concept_count,
            "processing_metadata": self.processing_metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PaperConcepts":
        """
        Create instance from dictionary data.

        Educational Note:
        Factory method for deserialization that reconstructs
        the complete entity with all relationships and validates
        business rules through normal constructor path.
        """
        concepts = [
            Concept.from_dict(concept_data) for concept_data in data["concepts"]
        ]
        extraction_timestamp = datetime.fromisoformat(data["extraction_timestamp"])

        return cls(
            paper_doi=data["paper_doi"],
            paper_title=data["paper_title"],
            concepts=concepts,
            extraction_timestamp=extraction_timestamp,
            extraction_method=data.get("extraction_method", "mixed"),
            processing_metadata=data.get("processing_metadata", {}),
        )
