"""
Keyword Configuration - Value object for search keyword management.

This module demonstrates how to model configuration data as domain value objects,
ensuring that keyword-based search behavior is properly encapsulated and validated.
It shows configuration-driven functionality in Clean Architecture.

Educational Notes:
- Value Object Pattern: Immutable configuration with validation
- Configuration as Code: YAML-based configuration with domain modeling
- Strategy Pattern: Different search strategies encapsulated as objects
- Single Responsibility: Each class handles one aspect of configuration

Design Decisions:
- Immutability: Configuration objects cannot be modified after creation
- Validation: Ensures configuration data is valid and complete
- Type Safety: Uses type hints for better development experience
- Extensibility: Easy to add new search strategies and keyword categories

Use Cases:
- Automated Research: Configure search terms for different research domains
- Customizable Searches: Researchers can modify search behavior via config
- Reproducible Results: Configuration files ensure consistent search behavior
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
import yaml
from pathlib import Path


@dataclass(frozen=True)
class SearchStrategy:
    """
    Value object representing a specific search strategy configuration.

    This demonstrates how to encapsulate search behavior configuration
    while maintaining immutability and validation.

    Educational Note:
    - Immutable value object (frozen=True)
    - Uses descriptive field names matching config files
    - Provides sensible defaults for optional fields
    - Validates data integrity in __post_init__
    """

    name: str
    description: str
    primary_keywords: List[str]
    secondary_keywords: List[str] = field(default_factory=list)
    search_limit: int = 50
    date_range: dict = field(default_factory=dict)
    exclusion_keywords: List[str] = field(default_factory=list)

    def __post_init__(self):
        """
        Validate search strategy configuration after initialization.

        Educational Note:
        - Post-init validation ensures data integrity
        - Raises informative errors for configuration issues
        - Validates both required fields and business rules
        """
        if not self.name:
            raise ValueError("Search strategy must have a name")
        if not self.description:
            raise ValueError("Search strategy must have a description")
        if not self.primary_keywords:
            raise ValueError("Search strategy must have at least one primary keyword")
        if self.search_limit <= 0:
            raise ValueError("search_limit must be positive")

    def get_all_terms(self) -> List[str]:
        """
        Get all search terms for this strategy.

        Educational Note:
        - Combines primary and secondary keywords
        - Uses set() for deduplication
        - Returns list for consistent API

        Returns:
            Combined list of all terms from primary and secondary keywords
        """
        all_terms = self.primary_keywords.copy()
        all_terms.extend(self.secondary_keywords)
        return list(set(all_terms))  # Remove duplicates

    def build_search_query(self) -> str:
        """
        Build a search query string from the strategy configuration.

        Educational Note:
        - Constructs boolean search queries for academic databases
        - Primary keywords use AND logic (all must be present)
        - Secondary keywords use OR logic (any can be present)
        - Quotes ensure exact phrase matching

        Returns:
            Formatted search query string suitable for academic databases
        """
        # Primary keywords must all be present (AND logic)
        query_parts = [f'"{term}"' for term in self.primary_keywords]

        # Secondary keywords add flexibility (OR logic)
        if self.secondary_keywords:
            optional_part = " OR ".join(f'"{term}"' for term in self.secondary_keywords)
            query_parts.append(f"({optional_part})")

        return " AND ".join(query_parts)


@dataclass(frozen=True)
class SearchConfiguration:
    """
    Value object for general search configuration settings.

    This encapsulates global search behavior that applies across
    all search strategies.
    """

    default_strategy: str
    citation_threshold: int
    start_year: int
    end_year: int
    exclude_terms: List[str] = field(default_factory=list)
    include_preprints: bool = True
    max_concurrent_searches: int = 3

    def __post_init__(self):
        """Validate search configuration after initialization."""
        if self.citation_threshold < 0:
            raise ValueError("Citation threshold cannot be negative")
        if self.start_year > self.end_year:
            raise ValueError("Start year cannot be after end year")
        if self.end_year > datetime.now().year + 1:
            raise ValueError("End year cannot be more than one year in the future")
        if self.max_concurrent_searches <= 0:
            raise ValueError("max_concurrent_searches must be positive")


@dataclass(frozen=True)
class KeywordConfig:
    """
    Main configuration value object for keyword-based search functionality.

    This demonstrates how to model complex configuration as a domain object,
    providing a clean interface for configuration-driven behavior while
    maintaining Clean Architecture principles.

    Educational Notes:
    - Aggregates all keyword and search configuration
    - Provides factory method for loading from YAML files
    - Validates configuration completeness and consistency
    - Encapsulates configuration behavior in domain layer
    """

    search_strategies: Dict[str, SearchStrategy]
    search_configuration: SearchConfiguration

    def __post_init__(self):
        """
        Validate the complete keyword configuration.

        Educational Note:
        - Domain validation at the object level ensures data integrity
        - Post-init validation catches configuration errors early
        - Follows fail-fast principle for better debugging
        """
        if not self.search_strategies:
            raise ValueError("At least one search strategy must be defined")

        # Validate that default strategy exists
        default_strategy = self.search_configuration.default_strategy
        if default_strategy not in self.search_strategies:
            raise ValueError(
                f"Default strategy '{default_strategy}' not found in available strategies"
            )

    @classmethod
    def from_yaml_file(cls, file_path: Path) -> "KeywordConfig":
        """
        Factory method to create KeywordConfig from YAML file.

        This demonstrates the Factory Pattern for object creation
        from external configuration sources.

        Args:
            file_path: Path to YAML configuration file

        Returns:
            KeywordConfig instance with loaded configuration

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If configuration is invalid or incomplete
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                config_data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")

        # Parse search strategies
        strategies = {}
        strategy_data = config_data.get("strategies", {})
        for name, strategy_config in strategy_data.items():
            strategies[name] = SearchStrategy(
                name=strategy_config.get("name", name),
                description=strategy_config.get("description", ""),
                primary_keywords=strategy_config.get("primary_keywords", []),
                secondary_keywords=strategy_config.get("secondary_keywords", []),
                search_limit=strategy_config.get("search_limit", 50),
                date_range=strategy_config.get("date_range", {}),
                exclusion_keywords=strategy_config.get("exclusion_keywords", []),
            )

        # Parse search configuration
        search_config_data = config_data.get("search_configuration", {})
        pub_date_range = search_config_data.get("publication_date_range", {})

        search_config = SearchConfiguration(
            default_strategy=search_config_data.get("default_strategy", ""),
            citation_threshold=search_config_data.get("citation_threshold", 0),
            start_year=pub_date_range.get("start_year", 2015),
            end_year=pub_date_range.get("end_year", 2025),
            exclude_terms=search_config_data.get("exclude_terms", []),
            include_preprints=search_config_data.get("include_preprints", True),
            max_concurrent_searches=search_config_data.get(
                "max_concurrent_searches", 3
            ),
        )

        return cls(
            search_strategies=strategies,
            search_configuration=search_config,
        )

    def get_strategy(self, strategy_name: Optional[str] = None) -> SearchStrategy:
        """
        Get a search strategy by name, with fallback to default.

        Args:
            strategy_name: Name of strategy to retrieve, or None for default

        Returns:
            SearchStrategy instance

        Raises:
            ValueError: If specified strategy doesn't exist
        """
        name = strategy_name or self.search_configuration.default_strategy

        if name not in self.search_strategies:
            available = list(self.search_strategies.keys())
            raise ValueError(f"Strategy '{name}' not found. Available: {available}")

        return self.search_strategies[name]

    def get_all_terms(self) -> List[str]:
        """
        Get all keywords from all configured strategies.

        Educational Note:
        - Consolidates keywords from multiple strategies
        - Uses set() to eliminate duplicates efficiently
        - Returns list for consistent API

        Returns:
            Combined list of all search terms from all strategies
        """
        all_terms = []

        # Collect terms from all configured strategies
        for strategy in self.search_strategies.values():
            all_terms.extend(strategy.primary_keywords)
            all_terms.extend(strategy.secondary_keywords)

        return list(set(all_terms))  # Remove duplicates

    def list_strategies(self) -> List[str]:
        """
        Get list of available search strategy names.

        Returns:
            List of strategy names
        """
        return list(self.search_strategies.keys())
