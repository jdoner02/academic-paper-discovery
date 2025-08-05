"""
Execute Keyword Searcfrom typing import List, Optional
from pathlib import Path

from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.keyword_config import KeywordConfig, SearchStrategyase - Application layer orchestration for keyword-based searches.

This use case demonstrates how to orchestrate domain objects and repository operations
to implement keyword-based search functionality. It shows the Application layer's
role in coordinating between domain logic and infrastructure components.

Educational Notes:
- Use Case Pattern: Encapsulates specific business operations
- Domain Orchestration: Coordinates domain objects to fulfill business requirements
- Dependency Inversion: Depends on abstractions (ports) not implementations
- Configuration-Driven: Uses domain configuration objects for flexible behavior

Design Decisions:
- Single Responsibility: Focuses only on keyword search execution
- Immutable Operations: Doesn't modify existing data, only queries
- Error Handling: Provides clear error messages for configuration issues
- Extensible Design: Easy to add new search strategies and keyword sources

Use Cases:
- Automated Research: Execute predefined search strategies
- Custom Searches: Use specific keyword combinations
- Batch Processing: Execute multiple searches with different strategies
"""

from typing import List, Optional
from pathlib import Path

from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.domain.entities.research_paper import ResearchPaper
from src.domain.value_objects.search_query import SearchQuery
from src.domain.value_objects.keyword_config import KeywordConfig, SearchStrategy


class ExecuteKeywordSearchUseCase:
    """
    Use case for executing keyword-based searches using configuration-driven strategies.

    This demonstrates the Application layer's role in orchestrating domain objects
    and infrastructure components to fulfill specific business requirements.

    Educational Notes:
    - Coordinates KeywordConfig (domain) with PaperRepository (infrastructure)
    - Translates search strategies into SearchQuery value objects
    - Handles business logic for search execution and result filtering
    - Provides clear separation between configuration and execution
    """

    def __init__(
        self, repository: PaperRepositoryPort, config_path: Optional[Path] = None
    ):
        """
        Initialize use case with repository and optional configuration path.

        Args:
            repository: Repository for accessing research papers
            config_path: Path to keyword configuration file, or None for default

        Raises:
            TypeError: If repository doesn't implement required interface
            FileNotFoundError: If configuration file doesn't exist
        """
        if not isinstance(repository, PaperRepositoryPort):
            raise TypeError("Repository must implement PaperRepositoryPort interface")

        self.repository = repository

        # Load configuration from file or use default path
        if config_path is None:
            # Default to config directory relative to this file
            current_dir = Path(__file__).parent.parent.parent.parent
            config_path = current_dir / "config" / "search_keywords.yaml"

        self.keyword_config = KeywordConfig.from_yaml_file(config_path)

    def execute_strategy(
        self, strategy_name: Optional[str] = None, max_results: Optional[int] = None
    ) -> List[ResearchPaper]:
        """
        Execute a search using a predefined strategy from configuration.

        This method demonstrates how to translate high-level search strategies
        into concrete SearchQuery objects and execute them through the repository.

        Args:
            strategy_name: Name of strategy to use, or None for default
            max_results: Override for maximum results, or None to use strategy default

        Returns:
            List of research papers matching the search strategy

        Raises:
            ValueError: If strategy doesn't exist or configuration is invalid
        """
        # Get the search strategy from configuration
        strategy = self.keyword_config.get_strategy(strategy_name)

        # Build search query from strategy
        search_query = self._build_search_query_from_strategy(strategy, max_results)

        # Execute search through repository
        results = self.repository.find_by_query(search_query)

        # Apply additional filtering based on configuration
        filtered_results = self._apply_configuration_filters(results)

        return filtered_results

    def execute_custom_search(
        self,
        required_terms: List[str],
        optional_terms: Optional[List[str]] = None,
        max_results: int = 50,
        min_citations: Optional[int] = None,
    ) -> List[ResearchPaper]:
        """
        Execute a custom search with specified terms.

        This method allows for ad-hoc searches while still applying global
        configuration settings for filtering and exclusions.

        Args:
            required_terms: Terms that must be present in results
            optional_terms: Terms that should be present but aren't required
            max_results: Maximum number of results to return
            min_citations: Minimum citation count, or None to use config default

        Returns:
            List of research papers matching the custom search

        Raises:
            ValueError: If required terms are empty or invalid
        """
        if not required_terms:
            raise ValueError("At least one required term must be provided")

        # Use global configuration for citation threshold if not specified
        if min_citations is None:
            min_citations = self.keyword_config.search_configuration.citation_threshold

        # Build search query
        all_terms = required_terms.copy()
        if optional_terms:
            all_terms.extend(optional_terms)

        # Create search query with date range from configuration
        search_query = SearchQuery(
            terms=all_terms,
            start_date=None,  # Could be derived from configuration
            end_date=None,  # Could be derived from configuration
            max_results=max_results,
            min_citations=min_citations,
        )

        # Execute search
        results = self.repository.find_by_query(search_query)

        # Apply configuration-based filtering
        filtered_results = self._apply_configuration_filters(results)

        return filtered_results

    def execute_all_strategies(self) -> dict[str, List[ResearchPaper]]:
        """
        Execute all configured search strategies and return results by strategy name.

        This method demonstrates batch processing capabilities and provides
        a comprehensive view of all available search results.

        Returns:
            Dictionary mapping strategy names to their search results
        """
        results = {}

        for strategy_name in self.keyword_config.list_strategies():
            try:
                strategy_results = self.execute_strategy(strategy_name)
                results[strategy_name] = strategy_results
            except Exception as e:
                # Log error but continue with other strategies
                # In production, would use proper logging
                print(f"Error executing strategy '{strategy_name}': {e}")
                results[strategy_name] = []

        return results

    def get_available_strategies(self) -> List[str]:
        """
        Get list of available search strategy names.

        Returns:
            List of strategy names that can be used with execute_strategy
        """
        return self.keyword_config.list_strategies()

    def get_strategy_info(self, strategy_name: str) -> SearchStrategy:
        """
        Get detailed information about a specific search strategy.

        Args:
            strategy_name: Name of strategy to get information about

        Returns:
            SearchStrategy object with detailed configuration

        Raises:
            ValueError: If strategy doesn't exist
        """
        return self.keyword_config.get_strategy(strategy_name)

    def _build_search_query_from_strategy(
        self, strategy: SearchStrategy, max_results_override: Optional[int] = None
    ) -> SearchQuery:
        """
        Build a SearchQuery from a SearchStrategy configuration.

        This private method handles the translation between configuration
        and domain objects, demonstrating proper encapsulation.

        Args:
            strategy: SearchStrategy to convert to SearchQuery
            max_results_override: Override for max results

        Returns:
            SearchQuery object ready for repository execution
        """
        # Combine all strategy terms
        all_terms = strategy.get_all_terms()

        # Use override or strategy default for max results
        max_results = max_results_override or strategy.max_results

        # Use configuration for citation threshold
        min_citations = self.keyword_config.search_configuration.citation_threshold

        # Create search query
        # Note: Could extend this to use publication date range from configuration
        return SearchQuery(
            terms=all_terms,
            start_date=None,  # Could use config.search_configuration.start_year
            end_date=None,  # Could use config.search_configuration.end_year
            max_results=max_results,
            min_citations=min_citations,
        )

    def _apply_configuration_filters(
        self, results: List[ResearchPaper]
    ) -> List[ResearchPaper]:
        """
        Apply global configuration filters to search results.

        This method demonstrates how to apply consistent filtering rules
        across all search operations based on global configuration.

        Args:
            results: Raw search results from repository

        Returns:
            Filtered results based on configuration settings
        """
        filtered_results = []
        exclude_terms = self.keyword_config.search_configuration.exclude_terms

        for paper in results:
            # Check if paper should be excluded based on title/abstract content
            should_exclude = False

            # Check title and abstract for exclude terms
            text_to_check = []
            if paper.title:
                text_to_check.append(paper.title.lower())
            if paper.abstract:
                text_to_check.append(paper.abstract.lower())

            for text in text_to_check:
                for exclude_term in exclude_terms:
                    if exclude_term.lower() in text:
                        should_exclude = True
                        break
                if should_exclude:
                    break

            if not should_exclude:
                filtered_results.append(paper)

        return filtered_results
