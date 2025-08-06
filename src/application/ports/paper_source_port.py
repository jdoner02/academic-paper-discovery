"""
PaperSourcePort - Multi-source repository abstraction for academic papers.

This port extends the existing PaperRepositoryPort to support multiple academic
databases (ArXiv, PubMed, Google Scholar, IEEE Xplore) while maintaining
Clean Architecture principles and backward compatibility.

Educational Notes:
- Repository Pattern: Abstracts data access across multiple external APIs
- Port/Adapter Pattern: Enables pluggable source implementations
- Interface Segregation: Clients depend only on methods they use
- Dependency Inversion: High-level modules depend on abstractions

Design Principles Applied:
- Single Responsibility: Each source handles one academic database
- Open/Closed: New sources can be added without modifying existing code
- Liskov Substitution: Any source can replace another in client code
- Interface Segregation: Source-specific methods are clearly separated

Multi-Source Considerations:
- Each source provides different metadata completeness
- Rate limiting varies significantly across sources
- Full-text access availability differs by source
- Citation formats and identifiers are source-specific

Usage Example:
    class ArxivPaperSource(PaperSourcePort):
        def get_source_name(self) -> str:
            return "ArXiv"
        
        def supports_full_text_download(self) -> bool:
            return True
            
        def get_rate_limit_info(self) -> Dict[str, Any]:
            return {"requests_per_second": 0.5, "burst_limit": 10}

Architecture Integration:
This port sits in the Application layer (Clean Architecture) and is implemented
by Infrastructure layer adapters. Domain layer entities (ResearchPaper) flow
through this interface without depending on specific source implementations.
"""

from abc import abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper


class PaperSourcePort(PaperRepositoryPort):
    """
    Abstract interface for multi-source academic paper repositories.
    
    Extends PaperRepositoryPort to support source identification, capability 
    reporting, and source-specific metadata handling while maintaining 
    backward compatibility with existing single-source implementations.
    
    Educational Note:
    This interface demonstrates how to extend existing abstractions in Clean
    Architecture without breaking existing contracts. Legacy code using
    PaperRepositoryPort continues to work, while new code can leverage
    multi-source capabilities.
    
    Source Capabilities:
    Different academic databases provide different capabilities:
    - ArXiv: Full PDFs, preprints, physics/CS focus
    - PubMed: Medical literature, abstracts, PMID identifiers  
    - Google Scholar: Broad coverage, citation counts, limited API
    - IEEE Xplore: Engineering papers, conference proceedings
    
    Each source implementation should accurately report its capabilities
    to enable intelligent routing and user expectations management.
    """
    
    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the human-readable name of this paper source.
        
        Returns:
            str: Source name (e.g., "ArXiv", "PubMed", "Google Scholar")
            
        Educational Note:
        Source identification is crucial for:
        - User feedback and transparency
        - Debugging and logging
        - Citation provenance tracking
        - Rate limiting coordination
        """
        pass
    
    @abstractmethod
    def get_source_capabilities(self) -> Dict[str, Any]:
        """
        Get detailed capability information for this source.
        
        Returns:
            Dict containing capability flags and limits:
            - "full_text_access": bool - Can download full PDFs
            - "metadata_richness": str - "high", "medium", "low"
            - "search_operators": List[str] - Supported search operators
            - "date_range_support": bool - Can filter by date
            - "citation_tracking": bool - Provides citation counts
            
        Educational Note:
        Capability reporting enables:
        - Intelligent source selection for specific queries
        - User interface adaptation based on available features
        - Fallback strategies when preferred sources are unavailable
        - Performance optimization by routing queries appropriately
        """
        pass
    
    @abstractmethod
    def supports_full_text_download(self) -> bool:
        """
        Check if this source provides full-text PDF downloads.
        
        Returns:
            bool: True if full PDFs are available, False for abstracts only
            
        Educational Note:
        Full-text availability varies dramatically across sources:
        - ArXiv: Freely available PDFs for most papers
        - PubMed: Abstract only, with links to publisher sites
        - Google Scholar: Mixed, depends on publisher policies
        - IEEE Xplore: Requires institutional access
        
        This information helps set user expectations and guide download strategies.
        """
        pass
    
    @abstractmethod
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        Get rate limiting information for this source.
        
        Returns:
            Dict containing rate limit details:
            - "requests_per_second": float - Maximum request rate
            - "burst_limit": int - Maximum burst requests
            - "daily_limit": Optional[int] - Daily request limit if any
            - "requires_api_key": bool - Whether API key is needed
            
        Educational Note:
        Academic APIs have varying rate limits:
        - ArXiv: ~0.5 requests/second, no authentication
        - PubMed: Higher limits with API key registration
        - Google Scholar: Very restrictive, requires careful management
        - IEEE Xplore: Depends on subscription level
        
        Respecting rate limits is crucial for:
        - Maintaining API access
        - Being a good citizen of the academic ecosystem
        - Avoiding IP-based blocking
        """
        pass
    
    @abstractmethod
    def extract_source_specific_metadata(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract source-specific metadata from raw API response.
        
        Args:
            raw_data: Raw response data from source API
            
        Returns:
            Dict containing source-specific metadata fields
            
        Educational Note:
        Each source provides unique metadata fields:
        - ArXiv: "arxiv_id", "categories", "primary_category", "version"
        - PubMed: "pmid", "pmcid", "mesh_terms", "publication_types"
        - Google Scholar: "cited_by_count", "versions", "cluster_id"
        - IEEE Xplore: "doi", "ieee_id", "conference_info", "keywords"
        
        Preserving source-specific metadata enables:
        - Rich citation generation
        - Source verification and validation
        - Advanced filtering and categorization
        - Research provenance tracking
        """
        pass
    
    @abstractmethod
    def enrich_paper_with_source_metadata(
        self, 
        paper: ResearchPaper, 
        source_metadata: Dict[str, Any]
    ) -> ResearchPaper:
        """
        Enrich a ResearchPaper with source-specific metadata.
        
        Args:
            paper: Base ResearchPaper entity
            source_metadata: Source-specific metadata from extract_source_specific_metadata
            
        Returns:
            ResearchPaper: Enhanced paper with source-specific information
            
        Educational Note:
        This method demonstrates the Decorator pattern in domain modeling.
        The base ResearchPaper entity maintains its core identity while
        being enriched with source-specific information that doesn't
        change its fundamental nature.
        
        The enrichment process should:
        - Preserve existing paper metadata
        - Add source-specific fields to appropriate attributes
        - Update retrieval timestamp and provenance information
        - Maintain data integrity and validation rules
        """
        pass
    
    @abstractmethod
    def get_source_paper_url(self, paper: ResearchPaper) -> Optional[str]:
        """
        Get the canonical URL for accessing this paper at its source.
        
        Args:
            paper: ResearchPaper to get source URL for
            
        Returns:
            Optional[str]: Source URL if available, None otherwise
            
        Educational Note:
        Source URLs provide:
        - Direct access to the paper at its origin
        - Citation linking and provenance
        - Verification of paper authenticity
        - Access to source-specific metadata and updates
        
        URL formats vary by source:
        - ArXiv: "https://arxiv.org/abs/{arxiv_id}"
        - PubMed: "https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        - DOI: "https://doi.org/{doi}" (for papers with DOI)
        """
        pass
