"""
PaperRepositoryPort - Abstract interface for research paper data access.

This port defines the contract that concrete repository implementations must
follow. It represents the boundary between the application layer and the
infrastructure layer, following the Dependency Inversion Principle.

Educational Notes:
- This is a port (interface) in hexagonal architecture
- Defines WHAT the application needs, not HOW it's implemented
- Infrastructure layer will provide concrete implementations (adapters)
- Enables easy testing with mock implementations
- Follows Repository Pattern from Domain-Driven Design

Design Principles Applied:
- Dependency Inversion: Application depends on abstraction, not concretion
- Interface Segregation: Contains only methods needed by application
- Single Responsibility: Focused only on paper data access

Repository Pattern Benefits:
- Encapsulates data access logic
- Provides a consistent interface for different data sources
- Enables unit testing without database dependencies
- Supports multiple implementations (database, API, cache, etc.)
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.research_paper import ResearchPaper
from domain.value_objects.search_query import SearchQuery


class PaperRepositoryPort(ABC):
    """
    Abstract repository interface for research paper data access.

    This port defines all the data access operations that the application
    layer needs to work with research papers. Concrete implementations
    will be provided by the infrastructure layer.

    Educational Note:
    Using ABC (Abstract Base Class) ensures that concrete implementations
    must provide all required methods. This enforces the contract at
    runtime and helps catch implementation errors early.

    Repository Pattern:
    - Provides a collection-like interface for domain objects
    - Encapsulates the logic needed to access data sources
    - Centralizes common data access functionality
    - Enables easier unit testing and maintainability
    """

    @abstractmethod
    def find_by_query(self, query: SearchQuery) -> List[ResearchPaper]:
        """
        Find research papers matching the given search query.

        This is the primary search method that takes a SearchQuery value object
        and returns a list of matching ResearchPaper entities. The concrete
        implementation will handle the actual search logic.

        Args:
            query: SearchQuery value object containing search parameters

        Returns:
            List[ResearchPaper]: List of papers matching the query.
                                Empty list if no matches found.

        Raises:
            RepositoryError: If search operation fails

        Educational Note:
        - Returns domain objects (ResearchPaper), not data structures
        - Takes domain objects (SearchQuery) as parameters
        - This keeps the repository focused on domain concepts
        - Error handling is implementation-specific but should be consistent
        """
        pass

    @abstractmethod
    def find_by_doi(self, doi: str) -> Optional[ResearchPaper]:
        """
        Find a research paper by its DOI (Digital Object Identifier).

        DOIs are unique identifiers for academic papers, so this method
        should return at most one paper.

        Args:
            doi: The DOI string to search for

        Returns:
            Optional[ResearchPaper]: The paper if found, None otherwise

        Raises:
            RepositoryError: If lookup operation fails

        Educational Note:
        DOI lookup is a common operation in academic systems, so we
        provide a dedicated method rather than forcing users to construct
        a SearchQuery for this simple case.
        """
        pass

    @abstractmethod
    def find_by_arxiv_id(self, arxiv_id: str) -> Optional[ResearchPaper]:
        """
        Find a research paper by its ArXiv identifier.

        ArXiv is a popular preprint server, especially for physics and
        computer science papers. ArXiv IDs are unique.

        Args:
            arxiv_id: The ArXiv ID string to search for

        Returns:
            Optional[ResearchPaper]: The paper if found, None otherwise

        Raises:
            RepositoryError: If lookup operation fails

        Educational Note:
        Like DOI lookup, this is a common enough operation to warrant
        its own method. It also demonstrates how the repository can
        support multiple identification schemes.
        """
        pass

    @abstractmethod
    def save_paper(self, paper: ResearchPaper) -> None:
        """
        Save a single research paper to the repository.

        This method handles both creating new papers and updating existing ones.
        The implementation should use the paper's identity (DOI or ArXiv ID)
        to determine whether this is a create or update operation.

        Args:
            paper: The ResearchPaper entity to save

        Raises:
            RepositoryError: If save operation fails
            ValidationError: If paper data is invalid

        Educational Note:
        - Repository handles the persistence details
        - Application doesn't need to know about create vs update logic
        - Domain object identity determines the operation type
        - This follows the Repository pattern's collection semantics
        """
        pass

    @abstractmethod
    def count_all(self) -> int:
        """
        Count total number of research papers in the repository.

        This method provides a quick way to get the total count of papers
        without retrieving all data. Useful for health checks, statistics,
        and pagination calculations.

        Returns:
            int: Total number of research papers stored

        Raises:
            RepositoryError: If count operation fails

        Educational Note:
        Count operations are useful for:
        - Health check endpoints to verify repository accessibility
        - Statistics and monitoring dashboards
        - Pagination calculations in UI layers
        - Performance monitoring of data growth
        """
        pass

    @abstractmethod
    def save_papers(self, papers: List[ResearchPaper]) -> None:
        """
        Save multiple research papers in a batch operation.

        This method should be more efficient than calling save_paper
        multiple times, especially for large batches. The implementation
        might use database transactions or batch APIs.

        Args:
            papers: List of ResearchPaper entities to save

        Raises:
            RepositoryError: If batch save operation fails
            ValidationError: If any paper data is invalid

        Educational Note:
        Batch operations are important for performance when dealing with
        large datasets. This method provides an optimization opportunity
        while maintaining the same semantics as individual saves.
        """
        pass


# Educational Notes for Students:
#
# 1. Port vs Adapter Pattern:
#    - Port: Interface defined by application (this file)
#    - Adapter: Concrete implementation in infrastructure layer
#    - This separation enables dependency inversion
#
# 2. Repository Pattern Benefits:
#    - Encapsulates data access complexity
#    - Provides domain-oriented interface
#    - Enables easy testing with mocks
#    - Supports multiple data sources
#
# 3. Abstract Base Classes:
#    - Enforce implementation contracts at runtime
#    - Provide clear documentation of required methods
#    - Enable isinstance() checks for type safety
#    - Python's way of defining interfaces
#
# 4. Domain-Focused Design:
#    - Methods take/return domain objects, not primitives
#    - Method names reflect business operations
#    - Error handling follows domain concepts
#    - Implementation details are hidden from application
#
# 5. Testing Strategy:
#    - Interface can be tested with mock implementations
#    - Tests define expected behavior for all implementations
#    - Concrete implementations tested separately
#    - Application layer tested using mocks of this interface
