"""
Concept Entity - Represents a research concept with hierarchical relationships.

This entity demonstrates advanced Clean Architecture domain modeling by encapsulating
the business rules around research concepts while supporting hierarchical relationships,
semantic clustering, and evidence-based grounding.

Educational Notes:
- Shows Entity pattern with identity and hierarchical relationships
- Demonstrates value validation in domain layer with complex business rules
- Illustrates immutable data structures for research integrity
- Shows how domain objects can represent complex research relationships
- Demonstrates hierarchical concept modeling for knowledge organization
- Shows evidence-based concept grounding for research quality assurance

Design Decisions:
- Concept text serves as natural identifier for research concepts
- Hierarchical relationships tracked through parent/child concept sets
- Evidence strength quantifies how well-grounded concepts are in source text
- Cluster IDs enable semantic grouping of related concepts
- Immutability preserved through copy-on-write pattern for hierarchy operations
- Validation prevents circular references and maintains hierarchy integrity

Hierarchical Concept Design Patterns:
- Root concepts: Broad domain terms with no parents (concept_level = 0)
- Intermediate concepts: Mid-level terms with both parents and children
- Leaf concepts: Specific terms with no children (most granular level)
- Evidence strength: Measures how well-supported the concept is by source text
- Clusters: Group semantically related concepts across different hierarchy branches

Use Cases:
- Research concept extraction from academic papers with hierarchy discovery
- Concept frequency analysis across research domains with parent-child relationships
- Semantic similarity analysis between concepts at different hierarchy levels
- Research trend identification with hierarchical concept evolution tracking
- Evidence-based concept validation for research quality assurance
- Concept clustering for knowledge organization and visualization
"""

from typing import Set, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.domain.value_objects.embedding_vector import EmbeddingVector


@dataclass(frozen=True)
class Concept:
    """
    Represents a research concept with hierarchical relationships and semantic clustering.

    A concept is an immutable entity representing a key idea, term, or theme
    found in research literature. Concepts maintain identity through their
    text representation and support hierarchical relationships for knowledge
    organization and evidence-based grounding for research quality assurance.

    Educational Notes:
    - Demonstrates Entity pattern with semantic embeddings integration
    - Shows hierarchical relationship modeling in domain entities
    - Illustrates evidence-based concept grounding for research applications
    - Demonstrates semantic clustering capabilities for knowledge organization
    - Shows how domain objects can leverage AI/ML capabilities while maintaining Clean Architecture
    - Maintains immutability through copy-on-write pattern for all operations

    Attributes:
        text: The textual representation of the concept (primary identifier)
        frequency: Number of times concept appears across papers
        relevance_score: Computed relevance score (0.0 to 1.0)
        source_papers: Set of DOIs where this concept was found
        source_domain: Research domain where concept was extracted
        extraction_method: Method used to extract this concept
        created_at: Timestamp when concept was first identified
        synonyms: Related terms that represent the same concept
        embedding: Optional semantic vector representation for similarity analysis

        # Hierarchical Relationship Fields
        parent_concepts: Set of concept text identifiers for broader concepts
        child_concepts: Set of concept text identifiers for more specific concepts
        concept_level: Depth in hierarchy (0 = root level, higher = more specific)
        cluster_id: Optional identifier for grouping semantically related concepts
        evidence_strength: Measure of how well-grounded concept is in source text (0.0-1.0)
    """

    text: str
    frequency: int
    relevance_score: float
    source_papers: Set[str] = field(default_factory=set)
    source_domain: Optional[str] = None
    extraction_method: str = "unknown"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    synonyms: Set[str] = field(default_factory=set)
    embedding: Optional[EmbeddingVector] = None

    # Hierarchical concept fields
    parent_concepts: Set[str] = field(default_factory=set)
    child_concepts: Set[str] = field(default_factory=set)
    concept_level: int = 0
    cluster_id: Optional[str] = None
    evidence_strength: float = 1.0

    def __post_init__(self):
        """
        Validate business rules for hierarchical research concepts.

        Educational Notes:
        Domain validation ensures data integrity at the entity level,
        preventing invalid states that could compromise research quality.
        Extended to include hierarchy validation rules that prevent
        circular references and maintain concept tree integrity.

        Validation Rules Applied:
        - Basic concept validation (text, frequency, relevance, extraction method)
        - Hierarchy validation (level >= 0, evidence strength in [0.0, 1.0])
        - Self-reference prevention (concept cannot be its own parent/child)
        - Business rule enforcement for research integrity
        """
        if not self.text or not self.text.strip():
            raise ValueError("Concept text cannot be empty")

        if self.frequency < 0:
            raise ValueError("Concept frequency cannot be negative")

        if not (0.0 <= self.relevance_score <= 1.0):
            raise ValueError("Relevance score must be between 0.0 and 1.0")

        if self.extraction_method not in [
            "tfidf",
            "named_entity",
            "keyword",
            "transformer",
            "semantic_embedding",
            "sentence_transformer",
            "manual",
            "unknown",
            # TDD Cycle 5: Add multi-strategy extraction methods
            "multi_strategy",
            "statistical",
            "rule_based",
            "embedding_based",
            "traditional",
            "traditional_fallback",
        ]:
            raise ValueError(f"Invalid extraction method: {self.extraction_method}")

        # Validate hierarchy fields
        if self.concept_level < 0:
            raise ValueError("Concept level cannot be negative")

        if not (0.0 <= self.evidence_strength <= 1.0):
            raise ValueError("Evidence strength must be between 0.0 and 1.0")

        # Prevent self-references in hierarchy
        normalized_text = self.text.lower().strip()
        if any(
            parent.lower().strip() == normalized_text for parent in self.parent_concepts
        ):
            raise ValueError("Concept cannot be its own parent")

        if any(
            child.lower().strip() == normalized_text for child in self.child_concepts
        ):
            raise ValueError("Concept cannot be its own child")

    def __str__(self) -> str:
        """String representation emphasizing concept identity and frequency."""
        domain_info = f" ({self.source_domain})" if self.source_domain else ""
        return f"Concept({self.text}{domain_info}, freq={self.frequency}, score={self.relevance_score:.3f})"

    def __eq__(self, other) -> bool:
        """
        Equality based on concept text (identity).

        Educational Note:
        Entity equality is based on identity (text), not all attributes.
        This ensures concepts with the same text are considered identical
        regardless of frequency or other metadata differences.
        """
        if not isinstance(other, Concept):
            return False
        return self.text.lower().strip() == other.text.lower().strip()

    def __hash__(self) -> int:
        """Hash based on normalized concept text for set operations."""
        return hash(self.text.lower().strip())

    def is_significant(
        self, min_frequency: int = 2, min_relevance: float = 0.1
    ) -> bool:
        """
        Determine if concept meets significance thresholds.

        Educational Note:
        Business logic method that encodes domain knowledge about
        what constitutes a "significant" research concept based on
        frequency and relevance thresholds.

        Args:
            min_frequency: Minimum frequency threshold for significance
            min_relevance: Minimum relevance score threshold

        Returns:
            True if concept meets both frequency and relevance thresholds
        """
        return self.frequency >= min_frequency and self.relevance_score >= min_relevance

    def add_paper_occurrence(self, doi: str) -> "Concept":
        """
        Create new concept instance with additional paper association.

        Educational Note:
        Since concepts are immutable (frozen=True), this method creates
        a new instance with updated paper associations and frequency.
        This preserves immutability while allowing concept evolution.

        Args:
            doi: DOI of paper where concept was found

        Returns:
            New Concept instance with updated associations
        """
        if not doi or not doi.strip():
            raise ValueError("DOI cannot be empty")

        new_papers = self.source_papers.copy()
        new_papers.add(doi)

        # Only increment frequency if this is a new paper
        new_frequency = self.frequency + (0 if doi in self.source_papers else 1)

        return Concept(
            text=self.text,
            frequency=new_frequency,
            relevance_score=self.relevance_score,
            source_papers=new_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=self.created_at,
            synonyms=self.synonyms,
            embedding=self.embedding,  # Preserve embedding data
            parent_concepts=self.parent_concepts,
            child_concepts=self.child_concepts,
            concept_level=self.concept_level,
            cluster_id=self.cluster_id,
            evidence_strength=self.evidence_strength,
        )

    def merge_with_synonym(self, synonym_concept: "Concept") -> "Concept":
        """
        Merge this concept with a synonym to create unified concept.

        Educational Note:
        Demonstrates domain logic for concept consolidation, combining
        frequency counts and paper associations while preserving research
        lineage through synonym tracking.

        Args:
            synonym_concept: Another concept to merge as synonym

        Returns:
            New concept with combined data from both concepts
        """
        if not isinstance(synonym_concept, Concept):
            raise ValueError("Can only merge with another Concept")

        combined_papers = self.source_papers.union(synonym_concept.source_papers)
        # Use sum of frequencies if no papers, otherwise count unique papers
        combined_frequency = (
            len(combined_papers)
            if combined_papers
            else self.frequency + synonym_concept.frequency
        )
        combined_synonyms = self.synonyms.union({synonym_concept.text}).union(
            synonym_concept.synonyms
        )

        # Use higher relevance score between the two concepts
        max_relevance = max(self.relevance_score, synonym_concept.relevance_score)

        return Concept(
            text=self.text,  # Keep original text as primary identifier
            frequency=combined_frequency,
            relevance_score=max_relevance,
            source_papers=combined_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=min(self.created_at, synonym_concept.created_at),
            synonyms=combined_synonyms,
            embedding=self.embedding,  # Keep primary concept's embedding
            parent_concepts=self.parent_concepts,
            child_concepts=self.child_concepts,
            concept_level=self.concept_level,
            cluster_id=self.cluster_id,
            evidence_strength=self.evidence_strength,
        )

    def get_paper_coverage_ratio(self, total_papers_in_domain: int) -> float:
        """
        Calculate what percentage of domain papers contain this concept.

        Educational Note:
        Provides research analytics by calculating concept prevalence
        within a specific research domain, useful for identifying
        core themes versus niche topics.

        Args:
            total_papers_in_domain: Total number of papers in the domain

        Returns:
            Ratio of papers containing this concept (0.0 to 1.0)
        """
        if total_papers_in_domain <= 0:
            return 0.0

        return len(self.source_papers) / total_papers_in_domain

    def semantic_similarity(self, other: "Concept") -> Optional[float]:
        """
        Calculate semantic similarity with another concept using embeddings.

        Educational Note:
        Demonstrates how domain entities can leverage AI/ML capabilities
        while maintaining clean separation of concerns. The actual similarity
        calculation is delegated to the EmbeddingVector value object.

        Args:
            other: Another concept to compare semantic similarity with

        Returns:
            Cosine similarity score (0.0 to 1.0) if both concepts have embeddings,
            None if either concept lacks embedding data

        Raises:
            ValueError: If other is not a Concept instance
        """
        if not isinstance(other, Concept):
            raise ValueError("Can only calculate similarity with another Concept")

        if self.embedding is None or other.embedding is None:
            return None

        return self.embedding.cosine_similarity(other.embedding)

    def find_similar_concepts(
        self, concepts: List["Concept"], similarity_threshold: float = 0.7
    ) -> List[tuple["Concept", float]]:
        """
        Find semantically similar concepts from a collection.

        Educational Note:
        Shows how domain entities can provide high-level business operations
        by orchestrating lower-level value object capabilities. This enables
        semantic clustering and concept relationship discovery.

        Args:
            concepts: Collection of concepts to search for similarity
            similarity_threshold: Minimum similarity score for inclusion (0.0 to 1.0)

        Returns:
            List of (concept, similarity_score) tuples sorted by similarity (highest first)

        Raises:
            ValueError: If similarity threshold is not between 0.0 and 1.0
        """
        if not (0.0 <= similarity_threshold <= 1.0):
            raise ValueError("Similarity threshold must be between 0.0 and 1.0")

        if self.embedding is None:
            return []

        similar_concepts = []

        for concept in concepts:
            if concept == self:  # Skip self
                continue

            similarity = self.semantic_similarity(concept)
            if similarity is not None and similarity >= similarity_threshold:
                similar_concepts.append((concept, similarity))

        # Sort by similarity score (highest first)
        similar_concepts.sort(key=lambda x: x[1], reverse=True)
        return similar_concepts

    def has_semantic_data(self) -> bool:
        """
        Check if concept has semantic embedding data available.

        Educational Note:
        Provides clean interface for checking semantic capabilities
        without exposing internal embedding implementation details.

        Returns:
            True if concept has embedding vector, False otherwise
        """
        return self.embedding is not None

    def add_embedding(self, embedding: EmbeddingVector) -> "Concept":
        """
        Create new concept instance with semantic embedding data.

        Educational Note:
        Since concepts are immutable, this method creates a new instance
        with embedding data while preserving all other concept metadata.
        This allows semantic enhancement of existing concepts.

        Args:
            embedding: Semantic vector representation of the concept

        Returns:
            New Concept instance with embedding data

        Raises:
            ValueError: If embedding is None or invalid
        """
        if not isinstance(embedding, EmbeddingVector):
            raise ValueError("Embedding must be an EmbeddingVector instance")

        return Concept(
            text=self.text,
            frequency=self.frequency,
            relevance_score=self.relevance_score,
            source_papers=self.source_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=self.created_at,
            synonyms=self.synonyms,
            embedding=embedding,
        )

    def to_dict(self) -> dict:
        """
        Convert concept to dictionary for serialization.

        Educational Note:
        Provides clean serialization interface for persistence or
        API responses while maintaining data integrity. Handles
        embedding serialization when present.
        """
        result = {
            "text": self.text,
            "frequency": self.frequency,
            "relevance_score": self.relevance_score,
            "source_papers": list(self.source_papers),
            "source_domain": self.source_domain,
            "extraction_method": self.extraction_method,
            "created_at": self.created_at.isoformat(),
            "synonyms": list(self.synonyms),
        }

        # Include embedding data if present
        if self.embedding is not None:
            result["embedding"] = list(self.embedding.vector)

        return result

    @classmethod
    def from_dict(cls, data: dict) -> "Concept":
        """
        Create concept from dictionary data.

        Educational Note:
        Factory method for deserialization that handles type conversion
        and maintains business rule validation through normal constructor.
        Handles embedding reconstruction when present in data.
        """
        created_at = datetime.fromisoformat(data["created_at"])

        # Reconstruct embedding if present
        embedding = None
        if "embedding" in data and data["embedding"] is not None:
            embedding = EmbeddingVector.from_list(data["embedding"])

        return cls(
            text=data["text"],
            frequency=data["frequency"],
            relevance_score=data["relevance_score"],
            source_papers=set(data.get("source_papers", [])),
            source_domain=data.get("source_domain"),
            extraction_method=data.get("extraction_method", "unknown"),
            created_at=created_at,
            synonyms=set(data.get("synonyms", [])),
            embedding=embedding,
            parent_concepts=set(data.get("parent_concepts", [])),
            child_concepts=set(data.get("child_concepts", [])),
            concept_level=data.get("concept_level", 0),
            cluster_id=data.get("cluster_id"),
            evidence_strength=data.get("evidence_strength", 1.0),
        )

    # Hierarchical Concept Navigation and Management Methods
    # =====================================================
    # These methods demonstrate hierarchical relationship management in domain entities
    # following the copy-on-write immutability pattern for maintaining data integrity.

    def add_parent_concept(self, parent_text: str) -> "Concept":
        """
        Add parent concept relationship, returning new immutable instance.

        Educational Notes:
        - Demonstrates copy-on-write pattern for immutable entity updates
        - Shows hierarchical relationship management in domain layer
        - Validates business rules (no empty parent text) at entity level
        - Maintains all existing entity state while adding new relationship

        Args:
            parent_text: Text identifier of parent concept (must be non-empty)

        Returns:
            New concept instance with parent relationship added

        Raises:
            ValueError: If parent_text is empty or whitespace-only
        """
        if not parent_text or not parent_text.strip():
            raise ValueError("Parent concept text cannot be empty")

        new_parents = self.parent_concepts.copy()
        new_parents.add(parent_text)

        return Concept(
            text=self.text,
            frequency=self.frequency,
            relevance_score=self.relevance_score,
            source_papers=self.source_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=self.created_at,
            synonyms=self.synonyms,
            embedding=self.embedding,
            parent_concepts=new_parents,
            child_concepts=self.child_concepts,
            concept_level=self.concept_level,
            cluster_id=self.cluster_id,
            evidence_strength=self.evidence_strength,
        )

    def add_child_concept(self, child_text: str) -> "Concept":
        """
        Add child concept relationship, returning new immutable instance.

        Educational Notes:
        - Demonstrates hierarchical relationship management from parent perspective
        - Shows how domain entities can manage bidirectional relationships
        - Maintains immutability while expanding concept hierarchy downward

        Args:
            child_text: Text identifier of child concept (must be non-empty)

        Returns:
            New concept instance with child relationship added

        Raises:
            ValueError: If child_text is empty or whitespace-only
        """
        if not child_text or not child_text.strip():
            raise ValueError("Child concept text cannot be empty")

        new_children = self.child_concepts.copy()
        new_children.add(child_text)

        return Concept(
            text=self.text,
            frequency=self.frequency,
            relevance_score=self.relevance_score,
            source_papers=self.source_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=self.created_at,
            synonyms=self.synonyms,
            embedding=self.embedding,
            parent_concepts=self.parent_concepts,
            child_concepts=new_children,
            concept_level=self.concept_level,
            cluster_id=self.cluster_id,
            evidence_strength=self.evidence_strength,
        )

    def is_root_concept(self) -> bool:
        """
        Check if this is a root concept in the hierarchy (no parents).

        Educational Notes:
        - Business logic method that encodes domain knowledge about hierarchy structure
        - Root concepts represent top-level domain categories in research taxonomies
        - Useful for hierarchy traversal algorithms and visualization systems

        Returns:
            True if concept has no parent concepts (is at root level)
        """
        return len(self.parent_concepts) == 0

    def is_leaf_concept(self) -> bool:
        """
        Check if this is a leaf concept in the hierarchy (no children).

        Educational Notes:
        - Leaf concepts represent the most specific terms in research taxonomies
        - Often correspond to very specific techniques, diseases, or technical terms
        - Useful for detailed analysis and precise research categorization

        Returns:
            True if concept has no child concepts (is at leaf level)
        """
        return len(self.child_concepts) == 0

    def get_hierarchy_depth(self) -> int:
        """
        Get hierarchy depth (same as concept_level for clarity).

        Educational Notes:
        - Provides semantic alias for concept_level to improve code readability
        - Depth 0 = root level, higher numbers = more specific concepts
        - Useful for hierarchy visualization and traversal algorithms

        Returns:
            Concept level in hierarchy (0 = root, higher = more specific)
        """
        return self.concept_level

    def set_cluster(self, cluster_id: str) -> "Concept":
        """
        Set semantic cluster assignment, returning new immutable instance.

        Educational Notes:
        - Demonstrates semantic clustering support in domain entities
        - Clusters group related concepts that may not have direct hierarchy relationships
        - Enables cross-cutting concept organization beyond strict hierarchies
        - Useful for concept visualization and similarity-based grouping

        Args:
            cluster_id: Identifier for concept cluster (e.g., "cardiac_concepts_001")

        Returns:
            New concept instance with cluster assignment
        """
        return Concept(
            text=self.text,
            frequency=self.frequency,
            relevance_score=self.relevance_score,
            source_papers=self.source_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=self.created_at,
            synonyms=self.synonyms,
            embedding=self.embedding,
            parent_concepts=self.parent_concepts,
            child_concepts=self.child_concepts,
            concept_level=self.concept_level,
            cluster_id=cluster_id,
            evidence_strength=self.evidence_strength,
        )

    def update_evidence_strength(self, evidence_strength: float) -> "Concept":
        """
        Update evidence strength scoring, returning new immutable instance.

        Educational Notes:
        - Demonstrates evidence-based concept grounding in research applications
        - Evidence strength measures how well-supported a concept is by source text
        - Higher scores indicate concepts with strong textual evidence
        - Lower scores may indicate concepts needing manual verification
        - Useful for research quality assurance and concept validation workflows

        Args:
            evidence_strength: New evidence strength score (0.0-1.0)
                             0.0 = no evidence, 1.0 = very strong evidence

        Returns:
            New concept instance with updated evidence strength

        Raises:
            ValueError: If evidence_strength not in range [0.0, 1.0]
        """
        if not (0.0 <= evidence_strength <= 1.0):
            raise ValueError("Evidence strength must be between 0.0 and 1.0")

        return Concept(
            text=self.text,
            frequency=self.frequency,
            relevance_score=self.relevance_score,
            source_papers=self.source_papers,
            source_domain=self.source_domain,
            extraction_method=self.extraction_method,
            created_at=self.created_at,
            synonyms=self.synonyms,
            embedding=self.embedding,
            parent_concepts=self.parent_concepts,
            child_concepts=self.child_concepts,
            concept_level=self.concept_level,
            cluster_id=self.cluster_id,
            evidence_strength=evidence_strength,
        )
