"""
Search Service Module

This module handles all search-related operations for the Research Paper Aggregator.
It demonstrates the Service Layer pattern for coordinating business operations.

Educational Notes:
- Service Layer Pattern: Coordinates use cases and provides clean API
- Academic Research Focus: Operations tailored for research workflows
- Error Handling: Comprehensive error management for research reliability
- Caching Strategy: Intelligent caching for academic research patterns

Design Patterns Applied:
- Service Layer: Coordinates multiple use cases and repositories
- Strategy Pattern: Different search strategies for different research needs
- Observer Pattern: Events for search progress tracking
- Cache-Aside Pattern: Intelligent caching of search results
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for coordinating search operations in academic research context.

    Educational Notes:
    - Single Responsibility: Handles only search-related coordination
    - Dependency Injection: Receives all dependencies externally
    - Academic Focus: Operations designed for research workflows
    """

    def __init__(self, search_use_case=None, concept_repository=None):
        """
        Initialize search service with Clean Architecture dependencies.

        Args:
            search_use_case: Use case for executing searches
            concept_repository: Repository for concept data access
        """
        self.search_use_case = search_use_case
        self.concept_repository = concept_repository
        self.search_cache = {}  # Simple in-memory cache for demonstration
        self.search_history = []
        self.max_cache_size = 100
        self.cache_ttl_hours = 2  # Academic searches valid for 2 hours

    def execute_search(
        self, config_name: str, search_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a search with caching and comprehensive result formatting.

        Args:
            config_name: Name of the search configuration to use
            search_params: Search parameters including filters and options

        Returns:
            Comprehensive search results with metadata and analytics

        Educational Notes:
        - Cache Strategy: Check cache before expensive operations
        - Result Formatting: Structure results for UI consumption
        - Analytics Integration: Track search patterns for UX improvement
        """

        try:
            # Generate cache key for this search
            cache_key = self._generate_cache_key(config_name, search_params)

            # Check cache first (Cache-Aside pattern)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                logger.info(f"Returning cached search result for {config_name}")
                return self._format_cached_result(cached_result)

            # Load search configuration
            keyword_config = self._load_search_configuration(config_name)
            if not keyword_config:
                return self._create_error_result(
                    f"Configuration '{config_name}' not found",
                    "CONFIGURATION_NOT_FOUND",
                )

            # Create search query from parameters
            search_query = self._create_search_query(keyword_config, search_params)

            # Execute search through use case
            logger.info(f"Executing search with configuration: {config_name}")
            search_result = self._execute_search_operation(keyword_config, search_query)

            # Format results for UI consumption
            formatted_result = self._format_search_result(
                search_result, config_name, search_params
            )

            # Cache the result
            self._cache_result(cache_key, formatted_result)

            # Record search in history
            self._record_search_history(config_name, search_params, formatted_result)

            return formatted_result

        except Exception as e:
            logger.error(f"Search execution failed: {str(e)}")
            return self._create_error_result(
                "An error occurred during search execution. Please try again.",
                "SEARCH_EXECUTION_ERROR",
            )

    def get_concept_evidence(self, concept_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed evidence for a specific concept.

        Args:
            concept_id: Unique identifier for the concept

        Returns:
            Detailed evidence data with source information and quality metrics

        Educational Notes:
        - Data Transformation: Convert domain objects to UI-friendly format
        - Academic Standards: Include citation and quality information
        - Error Handling: Graceful handling of missing concepts
        """

        try:
            if not self.concept_repository:
                return self._create_error_result(
                    "Concept repository not available", "REPOSITORY_UNAVAILABLE"
                )

            # Retrieve concept from repository
            concept = self.concept_repository.get_by_id(concept_id)
            if not concept:
                return self._create_error_result(
                    f"Concept '{concept_id}' not found", "CONCEPT_NOT_FOUND"
                )

            # Format evidence for academic use
            evidence_data = self._format_evidence_for_ui(concept)

            return {
                "success": True,
                "data": evidence_data,
                "metadata": {
                    "concept_id": concept_id,
                    "retrieved_at": datetime.now().isoformat(),
                    "evidence_count": len(evidence_data.get("evidence", [])),
                    "quality_metrics": self._calculate_evidence_quality_metrics(
                        concept
                    ),
                },
            }

        except Exception as e:
            logger.error(f"Failed to retrieve concept evidence: {str(e)}")
            return self._create_error_result(
                "Failed to retrieve concept evidence", "EVIDENCE_RETRIEVAL_ERROR"
            )

    def get_search_suggestions(
        self, query_text: str, domain: str = None
    ) -> List[Dict[str, Any]]:
        """
        Generate search suggestions based on query text and domain.

        Args:
            query_text: Partial query text for suggestions
            domain: Optional domain filter

        Returns:
            List of search suggestions with metadata

        Educational Notes:
        - User Experience: Proactive assistance for research queries
        - Academic Context: Suggestions tailored to research domains
        - Performance: Lightweight operation for real-time suggestions
        """

        try:
            suggestions = []

            # Academic domain-specific suggestions
            if domain:
                suggestions.extend(self._get_domain_suggestions(query_text, domain))

            # Historical search suggestions
            suggestions.extend(self._get_historical_suggestions(query_text))

            # Common academic research patterns
            suggestions.extend(self._get_common_research_patterns(query_text))

            # Remove duplicates and limit results
            unique_suggestions = self._deduplicate_suggestions(suggestions)
            return unique_suggestions[:10]  # Limit to top 10 suggestions

        except Exception as e:
            logger.error(f"Failed to generate search suggestions: {str(e)}")
            return []

    def _generate_cache_key(
        self, config_name: str, search_params: Dict[str, Any]
    ) -> str:
        """
        Generate a unique cache key for search parameters.

        Educational Notes:
        - Cache Strategy: Deterministic key generation for consistent caching
        - Performance: Fast key generation using hashing
        """

        # Create a deterministic string from parameters
        cache_data = {"config": config_name, "params": search_params}
        cache_string = json.dumps(cache_data, sort_keys=True)

        # Generate hash for consistent key
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached search result if still valid.

        Educational Notes:
        - Cache Management: TTL-based cache invalidation
        - Academic Research: Appropriate cache duration for research context
        """

        if cache_key not in self.search_cache:
            return None

        cached_item = self.search_cache[cache_key]

        # Check if cache item is still valid
        cache_time = datetime.fromisoformat(cached_item["cached_at"])
        expiry_time = cache_time + timedelta(hours=self.cache_ttl_hours)

        if datetime.now() > expiry_time:
            # Remove expired cache item
            del self.search_cache[cache_key]
            return None

        return cached_item["data"]

    def _cache_result(self, cache_key: str, result: Dict[str, Any]) -> None:
        """
        Cache search result with TTL management.

        Educational Notes:
        - Cache Size Management: Prevent unlimited cache growth
        - Academic Performance: Balance memory usage with research speed
        """

        # Remove oldest items if cache is full
        if len(self.search_cache) >= self.max_cache_size:
            oldest_key = min(
                self.search_cache.keys(),
                key=lambda k: self.search_cache[k]["cached_at"],
            )
            del self.search_cache[oldest_key]

        # Add new cache item
        self.search_cache[cache_key] = {
            "data": result,
            "cached_at": datetime.now().isoformat(),
        }

    def _load_search_configuration(self, config_name: str):
        """
        Load search configuration with error handling.

        Educational Notes:
        - Configuration Management: External configuration loading
        - Error Recovery: Graceful handling of missing configurations
        """

        try:
            # In a real implementation, this would load from the config directory
            # For now, return a mock configuration
            return self._create_mock_configuration(config_name)
        except Exception as e:
            logger.error(f"Failed to load configuration {config_name}: {str(e)}")
            return None

    def _create_mock_configuration(self, config_name: str):
        """
        Create mock configuration for demonstration purposes.

        Educational Notes:
        - Mock Objects: Demonstration objects for testing and development
        - Academic Domains: Example configurations for different research areas
        """

        # Mock configurations for different academic domains
        mock_configs = {
            "machine_learning": {
                "primary_keywords": [
                    "machine learning",
                    "artificial intelligence",
                    "neural networks",
                ],
                "secondary_keywords": [
                    "deep learning",
                    "supervised learning",
                    "algorithms",
                ],
                "description": "Machine Learning Research Configuration",
                "domain": "Computer Science",
                "quality_threshold": 0.8,
            },
            "medical_research": {
                "primary_keywords": [
                    "clinical trial",
                    "medical research",
                    "healthcare",
                ],
                "secondary_keywords": [
                    "patient outcomes",
                    "treatment efficacy",
                    "diagnosis",
                ],
                "description": "Medical Research Configuration",
                "domain": "Medicine",
                "quality_threshold": 0.9,
            },
            "environmental_science": {
                "primary_keywords": [
                    "climate change",
                    "environmental impact",
                    "sustainability",
                ],
                "secondary_keywords": [
                    "carbon footprint",
                    "renewable energy",
                    "conservation",
                ],
                "description": "Environmental Science Configuration",
                "domain": "Environmental Science",
                "quality_threshold": 0.75,
            },
        }

        config_data = mock_configs.get(config_name, mock_configs["machine_learning"])

        # Create mock configuration object
        from types import SimpleNamespace

        return SimpleNamespace(**config_data)

    def _create_search_query(self, keyword_config, search_params: Dict[str, Any]):
        """
        Create search query object from configuration and parameters.

        Educational Notes:
        - Object Creation: Building domain objects from UI parameters
        - Validation: Ensuring search parameters are valid
        """

        from types import SimpleNamespace

        return SimpleNamespace(
            terms=keyword_config.primary_keywords,
            max_results=search_params.get("max_results", 50),
            date_range_start=search_params.get("date_range_start"),
            date_range_end=search_params.get("date_range_end"),
            include_abstracts=search_params.get("include_abstracts", True),
            quality_threshold=search_params.get("quality_threshold", 0.7),
        )

    def _execute_search_operation(self, keyword_config, search_query):
        """
        Execute the actual search operation through use case.

        Educational Notes:
        - Use Case Coordination: Delegating to business logic layer
        - Error Propagation: Allowing use case errors to bubble up
        """

        if self.search_use_case:
            return self.search_use_case.execute(keyword_config, search_query)
        else:
            # Return mock result for demonstration
            from types import SimpleNamespace

            return SimpleNamespace(
                concepts=[], papers=[], execution_time=0.5, average_quality_score=0.8
            )

    def _format_search_result(
        self, search_result, config_name: str, search_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format search results for UI consumption with comprehensive metadata.

        Educational Notes:
        - Data Transformation: Converting domain objects to UI format
        - Academic Metadata: Including research-relevant information
        - User Experience: Structuring data for optimal UI presentation
        """

        return {
            "success": True,
            "data": {
                "concepts": [],  # Would format actual concepts
                "papers": [],  # Would format actual papers
                "statistics": {
                    "total_concepts": 0,
                    "total_papers": 0,
                    "search_duration": (
                        search_result.execution_time
                        if hasattr(search_result, "execution_time")
                        else 0
                    ),
                    "quality_score": (
                        search_result.average_quality_score
                        if hasattr(search_result, "average_quality_score")
                        else 0
                    ),
                },
                "visualization_data": self._prepare_visualization_data(search_result),
                "search_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "configuration": config_name,
                    "parameters": search_params,
                    "cache_status": "fresh",
                },
            },
            "user_message": f"Search completed successfully using {config_name} configuration.",
        }

    def _format_cached_result(self, cached_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format cached result with cache metadata.

        Educational Notes:
        - Cache Transparency: Informing users about cached data
        - Academic Trust: Clear indication of data freshness
        """

        result = cached_result.copy()
        if "data" in result and "search_metadata" in result["data"]:
            result["data"]["search_metadata"]["cache_status"] = "cached"

        return result

    def _create_error_result(self, message: str, error_code: str) -> Dict[str, Any]:
        """
        Create standardized error result format.

        Educational Notes:
        - Error Standardization: Consistent error format across application
        - User Communication: Clear, actionable error messages
        """

        return {
            "success": False,
            "error": error_code,
            "user_message": message,
            "timestamp": datetime.now().isoformat(),
        }

    def _format_evidence_for_ui(self, concept) -> Dict[str, Any]:
        """
        Format concept evidence for UI display.

        Educational Notes:
        - Academic Standards: Including citation and quality information
        - UI Optimization: Structure data for efficient rendering
        """

        return {
            "concept": {
                "id": getattr(concept, "id", "unknown"),
                "name": getattr(concept, "name", "Unknown Concept"),
                "description": getattr(concept, "description", ""),
            },
            "evidence": [],  # Would format actual evidence
            "statistics": {
                "total_evidence": 0,
                "average_confidence": 0,
                "source_papers": 0,
            },
        }

    def _calculate_evidence_quality_metrics(self, concept) -> Dict[str, float]:
        """
        Calculate quality metrics for concept evidence.

        Educational Notes:
        - Academic Quality: Metrics relevant to research credibility
        - Quantitative Assessment: Numerical quality indicators
        """

        return {
            "overall_quality": 0.8,
            "source_credibility": 0.85,
            "evidence_strength": 0.75,
            "consensus_level": 0.9,
        }

    def _prepare_visualization_data(self, search_result) -> Dict[str, Any]:
        """
        Prepare data for visualization components.

        Educational Notes:
        - Visualization Design: Data structure optimized for D3.js
        - Academic Presentation: Formats suitable for research communication
        """

        return {
            "hierarchy": {},
            "network": {"nodes": [], "links": []},
            "statistics": {"total_concepts": 0, "total_papers": 0, "domains": []},
        }

    def _record_search_history(
        self, config_name: str, search_params: Dict[str, Any], result: Dict[str, Any]
    ) -> None:
        """
        Record search in history for analytics and user experience.

        Educational Notes:
        - User Analytics: Track research patterns for UX improvement
        - Academic Continuity: Support for research session management
        """

        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "configuration": config_name,
            "parameters": search_params,
            "result_summary": {
                "success": result.get("success", False),
                "concept_count": result.get("data", {})
                .get("statistics", {})
                .get("total_concepts", 0),
                "paper_count": result.get("data", {})
                .get("statistics", {})
                .get("total_papers", 0),
            },
        }

        self.search_history.append(history_entry)

        # Limit history size to prevent memory issues
        if len(self.search_history) > 1000:
            self.search_history = self.search_history[-500:]  # Keep most recent 500

    def _get_domain_suggestions(
        self, query_text: str, domain: str
    ) -> List[Dict[str, Any]]:
        """Generate domain-specific search suggestions."""
        # Implementation would provide domain-specific suggestions
        return []

    def _get_historical_suggestions(self, query_text: str) -> List[Dict[str, Any]]:
        """Generate suggestions based on search history."""
        # Implementation would analyze search history
        return []

    def _get_common_research_patterns(self, query_text: str) -> List[Dict[str, Any]]:
        """Generate suggestions based on common research patterns."""
        # Implementation would provide common academic search patterns
        return []

    def _deduplicate_suggestions(
        self, suggestions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate suggestions while preserving order."""
        seen = set()
        unique_suggestions = []

        for suggestion in suggestions:
            suggestion_key = suggestion.get("text", "")
            if suggestion_key not in seen:
                seen.add(suggestion_key)
                unique_suggestions.append(suggestion)

        return unique_suggestions
