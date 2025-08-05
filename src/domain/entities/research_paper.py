"""
ResearchPaper domain entity.

This module contains the core ResearchPaper entity, which represents a scientific
research paper in our domain. As an entity, it has identity and encapsulates
the business rules related to research papers.

Educational Notes:
- This is a domain entity (has identity and lifecycle)
- Contains business logic and validation rules
- Uses dataclass for clean, immutable-by-default implementation
- Implements domain-specific behavior (HRV relevance detection)
- Follows Single Responsibility Principle

Design Decisions:
- DOI or ArXiv ID serves as identity for equality comparison
- Immutable by default (frozen=True) to prevent invalid state changes
- Rich validation in __post_init__ to enforce business rules
- Domain-specific methods for HRV relevance detection
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
import re


@dataclass(frozen=True)
class ResearchPaper:
    """
    Domain entity representing a scientific research paper.
    
    This entity encapsulates the core business rules for research papers
    in the HRV research domain. It validates data integrity and provides
    domain-specific behavior.
    
    Educational Note:
    - @dataclass(frozen=True) creates an immutable class
    - Immutability prevents invalid state changes and makes testing easier
    - The frozen parameter generates __eq__ and __hash__ methods automatically
    
    Business Rules Enforced:
    1. Every paper must have a non-empty title
    2. Every paper must have at least one author
    3. Publication dates cannot be in the future
    4. Either DOI or ArXiv ID is required for identity
    """
    
    # Required fields - these define the core identity and metadata
    title: str
    authors: List[str]
    publication_date: datetime
    
    # Optional metadata fields
    abstract: str = ""
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    venue: Optional[str] = None
    citation_count: int = 0
    
    # Computed fields with default factory
    # Educational Note: field(default_factory=list) creates a new list for each instance
    # This prevents the mutable default argument anti-pattern
    keywords: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """
        Validate business rules after object creation.
        
        This method is called automatically by dataclass after __init__.
        It's where we enforce domain invariants and business rules.
        
        Educational Note:
        - __post_init__ is a dataclass feature for post-creation validation
        - We validate business rules here, not just data types
        - Raising ValueError for business rule violations is appropriate
        """
        self._validate_title()
        self._validate_authors()
        self._validate_publication_date()
        self._validate_identity_fields()
    
    def _validate_title(self) -> None:
        """
        Validate that the title is meaningful.
        
        Business Rule: Every research paper must have a non-empty, meaningful title.
        """
        if not self.title or not self.title.strip():
            raise ValueError("Research paper must have a non-empty title")
        
        # Check for reasonable title length (not just whitespace or too short)
        if len(self.title.strip()) < 5:
            raise ValueError("Title must be at least 5 characters long")
    
    def _validate_authors(self) -> None:
        """
        Validate author information.
        
        Business Rule: Every research paper must have at least one author.
        Anonymous papers are not valid in academic contexts.
        """
        if not self.authors:
            raise ValueError("Research paper must have at least one author")
        
        # Validate that authors are meaningful (not empty strings)
        valid_authors = [author.strip() for author in self.authors if author.strip()]
        if not valid_authors:
            raise ValueError("All authors cannot be empty strings")
    
    def _validate_publication_date(self) -> None:
        """
        Validate publication date constraints.
        
        Business Rule: Papers cannot be published in the future.
        This prevents data entry errors and ensures data integrity.
        """
        if not self.publication_date:
            raise ValueError("Publication date is required")
        
        # Ensure timezone-aware datetime
        if self.publication_date.tzinfo is None:
            raise ValueError("Publication date must be timezone-aware")
        
        # Check that publication date is not in the future
        now = datetime.now(timezone.utc)
        if self.publication_date > now:
            raise ValueError("Publication date cannot be in the future")
    
    def _validate_identity_fields(self) -> None:
        """
        Validate that at least one identity field is present.
        
        Business Rule: Papers need either DOI or ArXiv ID for proper identification.
        This ensures we can deduplicate and reference papers uniquely.
        """
        if not self.doi and not self.arxiv_id:
            raise ValueError("Paper must have either DOI or ArXiv ID for identification")
    
    def is_hrv_relevant(self) -> bool:
        """
        Determine if this paper is relevant to HRV research.
        
        This method implements domain-specific business logic to identify
        papers that are relevant to Heart Rate Variability research.
        
        Educational Note:
        - This is domain behavior, not just data storage
        - The logic is encapsulated within the entity
        - Could be extracted to a domain service if it becomes more complex
        
        Returns:
            bool: True if paper is relevant to HRV research
        """
        # Define HRV-related keywords
        # Educational Note: In a real system, these might come from configuration
        # or a more sophisticated domain service
        hrv_keywords = [
            "heart rate variability",
            "hrv",
            "r-r interval",
            "rr interval", 
            "cardiac autonomic",
            "vagal tone",
            "autonomic nervous system",
            "heart rate dynamics",
            "cardiac arrhythmia",
            "ecg analysis",
            "ppg signal",
            "wearable monitoring",
            "traumatic brain injury",
            "tbi",
            "concussion"
        ]
        
        # Combine title and abstract for searching
        text_to_search = (self.title + " " + self.abstract).lower()
        
        # Check if any HRV keywords are present
        return any(keyword in text_to_search for keyword in hrv_keywords)
    
    def get_identity(self) -> str:
        """
        Get the unique identifier for this paper.
        
        Returns DOI if available, otherwise ArXiv ID.
        This is used for equality comparison and deduplication.
        
        Educational Note:
        - Entities need a way to determine identity
        - This method encapsulates the identity logic
        - Useful for hashing and equality operations
        """
        return self.doi or self.arxiv_id or ""
    
    def __eq__(self, other: object) -> bool:
        """
        Define equality based on identity, not all attributes.
        
        Two papers are equal if they have the same identity (DOI or ArXiv ID),
        even if other metadata differs (different versions, etc.).
        
        Educational Note:
        - Entity equality is based on identity, not attributes
        - This is different from value objects, which compare all attributes
        - Frozen dataclass generates __eq__ based on all fields, so we override
        """
        if not isinstance(other, ResearchPaper):
            return False
        
        return self.get_identity() == other.get_identity()
    
    def __hash__(self) -> int:
        """
        Define hash based on identity.
        
        Since we override __eq__, we must also override __hash__ to maintain
        the hash-equality contract: equal objects must have equal hashes.
        """
        return hash(self.get_identity())
    
    def __str__(self) -> str:
        """
        Provide a human-readable string representation.
        
        Educational Note:
        - Good __str__ methods make debugging easier
        - Include key identifying information
        - Keep it concise but informative
        """
        authors_str = ", ".join(self.authors[:2])  # Show first 2 authors
        if len(self.authors) > 2:
            authors_str += f" et al. ({len(self.authors)} total)"
        
        return f"ResearchPaper('{self.title[:50]}...', {authors_str}, {self.publication_date.year})"
    
    def __repr__(self) -> str:
        """
        Provide a developer-friendly representation.
        
        Should be unambiguous and ideally eval()-able for debugging.
        """
        return (f"ResearchPaper(title='{self.title}', "
                f"authors={self.authors}, "
                f"publication_date={self.publication_date}, "
                f"doi='{self.doi}', arxiv_id='{self.arxiv_id}')")


# Educational Note:
# This implementation demonstrates several key concepts:
# 
# 1. Domain Entity: Has identity and lifecycle
# 2. Business Rule Validation: Enforces domain constraints
# 3. Rich Domain Model: Contains behavior, not just data
# 4. Immutability: Prevents invalid state changes
# 5. Single Responsibility: Focuses on research paper concerns
# 6. Type Safety: Uses type hints for better IDE support and documentation
#
# Next steps:
# 1. Run tests to see if they pass (Green phase)
# 2. Refactor if needed while keeping tests green
# 3. Add more sophisticated behavior as requirements emerge
