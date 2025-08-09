"""
Simple ConceptHierarchy for GitHub Classroom.

A clean, educational implementation focusing on core domain concepts
without the complexity that confuses students.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

from src.domain.entities.concept import Concept


@dataclass
class ConceptHierarchy:
    """
    A simplified educational implementation of ConceptHierarchy.

    This represents a hierarchy of research concepts extracted from academic papers.
    Designed to be pedagogically clear for students learning domain modeling.
    """

    def __init__(
        self,
        hierarchy_id: str,
        concepts: List[Concept] = None,
        root_concepts: List[Concept] = None,
        all_concepts: List[Concept] = None,
        evidence_sentences=None,
        hierarchy_metadata=None,
        extraction_provenance=None,
    ):
        """
        Create a new concept hierarchy.

        This constructor supports both the simplified educational interface and
        backward compatibility with existing tests.

        Args:
            hierarchy_id: Unique identifier for this hierarchy
            concepts: Simple list of concepts (new educational interface)
            root_concepts: Top-level concepts (legacy test interface)
            all_concepts: All concepts in hierarchy (legacy test interface)
            evidence_sentences: Supporting evidence (legacy, optional)
            hierarchy_metadata: Metadata about hierarchy (legacy, optional)
            extraction_provenance: Source information (legacy, optional)

        Raises:
            ValueError: If hierarchy_id is empty or no concepts provided
        """
        if not hierarchy_id or not hierarchy_id.strip():
            raise ValueError("Hierarchy ID cannot be empty")

        # Handle both new and legacy interfaces
        if concepts is not None:
            # New simplified interface
            concept_list = concepts
        elif all_concepts is not None:
            # Legacy test interface
            concept_list = all_concepts
        elif root_concepts is not None:
            # Legacy test interface with just root concepts
            concept_list = root_concepts
            # Validate root concepts have level 0
            for concept in root_concepts:
                if hasattr(concept, "concept_level") and concept.concept_level != 0:
                    raise ValueError("Root concepts must have concept_level = 0")
        else:
            concept_list = []

        if not concept_list:
            raise ValueError("Hierarchy must contain at least one concept")

        # Validate all concepts
        for concept in concept_list:
            if not isinstance(concept, Concept):
                raise TypeError("All items in concepts list must be Concept instances")

        self._hierarchy_id = hierarchy_id.strip()
        self._concepts = list(concept_list)  # Create defensive copy

        # Store legacy attributes for backward compatibility
        self._root_concepts = root_concepts or []
        self._all_concepts = all_concepts or concept_list
        self._evidence_sentences = evidence_sentences or []
        self._hierarchy_metadata = hierarchy_metadata
        self._extraction_provenance = extraction_provenance

    @property
    def hierarchy_id(self) -> str:
        """Get the unique identifier for this hierarchy."""
        return self._hierarchy_id

    @property
    def concepts(self) -> List[Concept]:
        """Get the concepts in this hierarchy."""
        return list(self._concepts)  # Return defensive copy

    @property
    def root_concepts(self) -> List[Concept]:
        """Get root concepts (for backward compatibility)."""
        return list(self._root_concepts)

    @property
    def all_concepts(self) -> List[Concept]:
        """Get all concepts (for backward compatibility)."""
        return list(self._all_concepts)

    @property
    def evidence_sentences(self) -> List:
        """Get evidence sentences (for backward compatibility)."""
        return list(self._evidence_sentences)

    @property
    def hierarchy_metadata(self):
        """Get hierarchy metadata (for backward compatibility)."""
        return self._hierarchy_metadata

    @property
    def extraction_provenance(self):
        """Get extraction provenance (for backward compatibility)."""
        return self._extraction_provenance

    def __len__(self) -> int:
        """Return the number of concepts in this hierarchy."""
        return len(self._concepts)

    def __eq__(self, other) -> bool:
        """Check equality with another ConceptHierarchy."""
        if not isinstance(other, ConceptHierarchy):
            return False
        return (
            self._hierarchy_id == other._hierarchy_id
            and self._concepts == other._concepts
        )

    def __str__(self) -> str:
        """Return string representation of the hierarchy."""
        return f"ConceptHierarchy(id='{self._hierarchy_id}', concepts={len(self._concepts)})"
