"""
ConceptRepositoryPort - Port for concept persistence and retrieval.

This port defines the interface for concept data access, following the
Repository pattern and Port/Adapter pattern in Clean Architecture.
It provides abstraction between the application layer and data storage.

Educational Notes:
- Shows Repository pattern for data access abstraction
- Demonstrates Port/Adapter pattern for external dependencies
- Illustrates domain entity persistence contracts
- Provides interface for different storage implementations

Design Decisions:
- Abstract interface separates business logic from storage
- Entity-based methods maintain domain model integrity
- Query methods support flexible concept retrieval
- Batch operations enable efficient data processing

Use Cases:
- Storing extracted concepts from research papers
- Retrieving concepts for analysis and comparison
- Managing concept relationships and hierarchies
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.entities.paper_concepts import PaperConcepts
from src.domain.entities.concept import Concept


class ConceptRepositoryPort(ABC):
    """
    Abstract port for concept data persistence and retrieval.

    This interface defines the contract for storing and retrieving
    concept data, enabling different storage implementations while
    maintaining consistent application layer integration.

    Educational Notes:
    - Abstract base class ensures implementation compliance
    - Entity-based methods maintain domain model integrity
    - Optional return types handle missing data gracefully
    - Batch operations support efficient data processing
    """

    @abstractmethod
    def save_paper_concepts(self, paper_concepts: PaperConcepts) -> None:
        """
        Store paper concepts in the repository.

        Args:
            paper_concepts: PaperConcepts entity to store

        Raises:
            ValueError: If paper_concepts is invalid
            RuntimeError: If storage operation fails

        Educational Notes:
        - Entity-based storage maintains domain model integrity
        - Void return indicates fire-and-forget storage
        - Clear error contracts enable robust error handling
        """
        pass

    @abstractmethod
    def find_paper_concepts_by_doi(self, doi: str) -> Optional[PaperConcepts]:
        """
        Retrieve paper concepts by DOI.

        Args:
            doi: DOI of the paper to retrieve concepts for

        Returns:
            Optional[PaperConcepts]: Paper concepts if found, None otherwise

        Educational Notes:
        - DOI serves as natural identifier for research papers
        - Optional return type handles missing data gracefully
        - Entity return maintains domain model consistency
        """
        pass

    @abstractmethod
    def find_concepts_by_text(self, concept_text: str) -> List[Concept]:
        """
        Find concepts by text content.

        Args:
            concept_text: Text to search for in concepts

        Returns:
            List[Concept]: List of matching concepts (empty if none found)

        Educational Notes:
        - Text-based search enables concept discovery
        - List return type supports multiple matches
        - Empty list pattern avoids None handling complexity
        """
        pass

    @abstractmethod
    def get_all_paper_concepts(self) -> List[PaperConcepts]:
        """
        Retrieve all paper concepts from the repository.

        Returns:
            List[PaperConcepts]: List of all stored paper concepts

        Educational Notes:
        - Batch retrieval supports analysis workflows
        - List return type provides consistent interface
        - Useful for system-wide concept analysis
        """
        pass

    @abstractmethod
    def delete_paper_concepts(self, doi: str) -> bool:
        """
        Delete paper concepts by DOI.

        Args:
            doi: DOI of the paper concepts to delete

        Returns:
            bool: True if concepts were deleted, False if not found

        Educational Notes:
        - Boolean return indicates operation success
        - DOI-based deletion maintains data consistency
        - Supports concept repository maintenance
        """
        pass

    @abstractmethod
    def count_papers_with_concepts(self) -> int:
        """
        Count the number of papers with stored concepts.

        Returns:
            int: Number of papers in the repository

        Educational Notes:
        - Simple metric for repository monitoring
        - Integer return provides exact count
        - Useful for system statistics and reporting
        """
        pass
