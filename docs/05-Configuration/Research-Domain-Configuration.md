# Research Domain Configuration - YAML-Based Strategy System

## 🎯 Overview

The Research Domain Configuration system is a sophisticated YAML-based approach to defining domain-specific search strategies, filtering criteria, and ranking algorithms. This system demonstrates configuration-driven behavior, enabling domain experts to customize the paper discovery system without code changes.

## 🏗️ Configuration Architecture

### Design Principles

**Configuration as Code:**
- Human-readable YAML format for domain experts
- Version-controlled configuration files
- Validation rules ensure correctness
- Hot-reloading enables runtime updates
- Extensible structure supports new domains

**Domain-Driven Configuration:**
- Each configuration represents a research domain
- Domain experts define optimal search strategies
- Validation rules prevent invalid configurations
- Fallback mechanisms ensure system reliability

## 📋 Configuration Structure

### Base Configuration Schema

```yaml
# config/schemas/domain_configuration.yaml

# Meta information about the configuration
name: "artificial_intelligence_security"
description: "AI/ML system security, adversarial machine learning, and AI-powered cybersecurity tools"
version: "1.2.0"
created_by: "domain_expert@university.edu"
last_updated: "2024-08-07"

# Search configuration parameters
search_configuration:
  default_strategy: "adversarial_machine_learning_defense"
  citation_threshold: 5                    # Minimum citations for inclusion
  publication_date_range:
    start_year: 2015                      # Include foundational research
    end_year: 2025                        # Latest developments
  max_concurrent_searches: 3              # Performance optimization
  include_preprints: true                 # Include non-peer-reviewed papers
  exclude_terms: 
    - "AI ethics"                         # Focus on security, not ethics
    - "machine learning performance"      # Focus on security, not optimization
    - "general AI applications"           # Focus on security applications

# Search strategies define how to find relevant papers
strategies:
  adversarial_machine_learning_defense:
    name: "Adversarial Machine Learning and Model Robustness"
    description: "Defense mechanisms against adversarial attacks on ML models"
    weight: 1.0                           # Primary strategy
    
    # Primary keywords have highest weight in search
    primary_keywords:
      - "adversarial machine learning"
      - "adversarial attacks"
      - "ML model robustness"
      - "adversarial defense"
      - "AI security"
    
    # Secondary keywords expand search scope
    secondary_keywords:
      - "adversarial examples"
      - "model poisoning"
      - "data poisoning"
      - "evasion attacks"
      - "backdoor attacks"
      - "trojan attacks"
      - "model stealing"
      - "membership inference"
    
    # Technical terms for precise matching
    technical_terms:
      - "adversarial training"
      - "defensive distillation"
      - "gradient masking"
      - "certified defense"
      - "randomized smoothing"
      - "input preprocessing"
      - "detection methods"
      - "verification techniques"
    
    # Application domains for context
    application_domains:
      - "computer vision"
      - "natural language processing"
      - "autonomous systems"
      - "medical diagnosis"
      - "financial systems"
      - "cybersecurity applications"
    
    # Terms to exclude from this strategy
    exclude_terms:
      - "model accuracy"
      - "training efficiency"
      - "general ML optimization"

# Ranking configuration defines how to score and order papers
ranking:
  algorithm: "weighted_combination"
  weights:
    relevance_score: 0.4                  # Keyword matching and semantic similarity
    citation_impact: 0.25                 # Citation count and growth
    venue_prestige: 0.15                  # Publication venue ranking
    recency_factor: 0.1                   # Publication date recency
    author_reputation: 0.1                # Author h-index and reputation
  
  # Boost factors for specific criteria
  boost_factors:
    peer_reviewed: 1.2                    # Prefer peer-reviewed papers
    high_impact_venue: 1.5                # Boost papers from top venues
    recent_publication: 1.3               # Boost papers from last 2 years
    multiple_citations: 1.1               # Boost well-cited papers

# Filtering criteria for result refinement
filtering:
  minimum_quality_score: 0.3              # Exclude low-quality papers
  maximum_age_years: 10                   # Exclude very old papers
  required_languages: ["english"]         # Language restrictions
  
  # Venue filtering
  preferred_venues:
    conferences:
      - "NeurIPS"
      - "ICML" 
      - "ICLR"
      - "CVPR"
      - "ICCV"
      - "ACL"
      - "EMNLP"
    journals:
      - "Nature"
      - "Science"
      - "JMLR"
      - "TPAMI"
      - "TACL"
  
  # Author filtering
  exclude_authors: []                     # Problematic authors to exclude
  preferred_institutions:                 # Boost papers from top institutions
    - "MIT"
    - "Stanford"
    - "Carnegie Mellon"
    - "UC Berkeley"
    - "Google Research"
    - "OpenAI"
    - "DeepMind"

# Concept extraction configuration
concept_extraction:
  enabled: true
  min_confidence: 0.7                     # Minimum confidence for concepts
  max_concepts_per_paper: 10              # Limit concept extraction
  
  # Concept categories to extract
  extract_categories:
    - "methodologies"
    - "datasets"
    - "evaluation_metrics"
    - "applications"
    - "limitations"
  
  # Domain-specific concept patterns
  concept_patterns:
    methodologies:
      - ".*defense.*"
      - ".*detection.*"
      - ".*mitigation.*"
    datasets:
      - ".*dataset.*"
      - ".*benchmark.*"
      - ".*corpus.*"

# Quality assessment configuration
quality_assessment:
  enabled: true
  factors:
    citation_count:
      weight: 0.3
      normalization: "log_scale"          # Logarithmic normalization
    venue_impact:
      weight: 0.25
      source: "venue_rankings.yaml"      # External venue ranking file
    author_metrics:
      weight: 0.2
      metrics: ["h_index", "citation_count", "collaboration_index"]
    content_quality:
      weight: 0.15
      metrics: ["abstract_length", "reference_count", "figure_count"]
    novelty_score:
      weight: 0.1
      calculation: "semantic_uniqueness"  # How unique compared to existing work

# Validation rules for configuration correctness
validation:
  required_fields:
    - "name"
    - "search_configuration"
    - "strategies"
  
  field_constraints:
    citation_threshold:
      min: 0
      max: 1000
    max_concurrent_searches:
      min: 1
      max: 10
    publication_date_range:
      start_year:
        min: 1950
        max: 2024
      end_year:
        min: 1950
        max: 2030
  
  strategy_constraints:
    min_primary_keywords: 3
    max_primary_keywords: 20
    min_secondary_keywords: 5
    max_secondary_keywords: 50
    max_exclude_terms: 20
  
  ranking_constraints:
    weights_sum: 1.0                      # All weights must sum to 1.0
    min_weight: 0.0
    max_weight: 1.0

# Analytics and monitoring
analytics:
  track_usage: true
  metrics_to_collect:
    - "search_frequency"
    - "result_quality_feedback"
    - "configuration_effectiveness"
    - "user_satisfaction_scores"
  
  performance_targets:
    average_relevance_score: 0.8
    user_satisfaction_threshold: 4.0
    search_completion_rate: 0.95
```

## 🔧 Configuration Implementation

### Domain Configuration Value Object

```python
# research-core/src/domain/value_objects/domain_configuration.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml
from pathlib import Path

@dataclass(frozen=True)
class SearchStrategy:
    """
    Value object representing a search strategy.
    
    Educational Notes:
    - Immutable value object ensures thread safety
    - Rich validation prevents invalid configurations
    - Clear separation between data and behavior
    - Demonstrates composition over inheritance
    """
    name: str
    description: str
    weight: float
    primary_keywords: List[str]
    secondary_keywords: List[str]
    technical_terms: List[str]
    application_domains: List[str]
    exclude_terms: List[str]
    
    def __post_init__(self):
        """Validate strategy configuration."""
        self._validate_name()
        self._validate_weight()
        self._validate_keywords()
        self._validate_terms()
    
    def _validate_name(self):
        """Validate strategy name."""
        if not self.name or not self.name.strip():
            raise ValueError("Strategy name is required")
        if len(self.name) > 100:
            raise ValueError("Strategy name too long (max 100 characters)")
    
    def _validate_weight(self):
        """Validate strategy weight."""
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("Strategy weight must be between 0.0 and 1.0")
    
    def _validate_keywords(self):
        """Validate keyword lists."""
        if len(self.primary_keywords) < 3:
            raise ValueError("At least 3 primary keywords required")
        if len(self.primary_keywords) > 20:
            raise ValueError("Too many primary keywords (max 20)")
        
        if len(self.secondary_keywords) < 5:
            raise ValueError("At least 5 secondary keywords required")
        if len(self.secondary_keywords) > 50:
            raise ValueError("Too many secondary keywords (max 50)")
    
    def _validate_terms(self):
        """Validate term lists."""
        if len(self.exclude_terms) > 20:
            raise ValueError("Too many exclude terms (max 20)")
        
        # Check for overlap between included and excluded terms
        all_included = set(self.primary_keywords + self.secondary_keywords + self.technical_terms)
        excluded = set(self.exclude_terms)
        
        overlap = all_included.intersection(excluded)
        if overlap:
            raise ValueError(f"Terms cannot be both included and excluded: {overlap}")
    
    def get_all_keywords(self) -> List[str]:
        """Get all keywords for this strategy."""
        return self.primary_keywords + self.secondary_keywords + self.technical_terms
    
    def calculate_term_relevance(self, text: str) -> float:
        """Calculate how relevant text is to this strategy."""
        text_lower = text.lower()
        
        # Score based on keyword presence and weights
        primary_score = sum(1.0 for kw in self.primary_keywords if kw.lower() in text_lower)
        secondary_score = sum(0.5 for kw in self.secondary_keywords if kw.lower() in text_lower)
        technical_score = sum(0.7 for term in self.technical_terms if term.lower() in text_lower)
        
        # Penalty for excluded terms
        exclude_penalty = sum(0.3 for term in self.exclude_terms if term.lower() in text_lower)
        
        total_score = primary_score + secondary_score + technical_score - exclude_penalty
        max_possible = len(self.primary_keywords) + len(self.secondary_keywords) * 0.5 + len(self.technical_terms) * 0.7
        
        return max(0.0, min(1.0, total_score / max_possible if max_possible > 0 else 0.0))

@dataclass(frozen=True)
class RankingConfiguration:
    """Configuration for paper ranking algorithms."""
    algorithm: str
    weights: Dict[str, float]
    boost_factors: Dict[str, float]
    
    def __post_init__(self):
        """Validate ranking configuration."""
        self._validate_algorithm()
        self._validate_weights()
        self._validate_boost_factors()
    
    def _validate_algorithm(self):
        """Validate ranking algorithm."""
        valid_algorithms = ["weighted_combination", "neural_ranking", "gradient_boosting"]
        if self.algorithm not in valid_algorithms:
            raise ValueError(f"Invalid ranking algorithm. Must be one of: {valid_algorithms}")
    
    def _validate_weights(self):
        """Validate ranking weights."""
        weight_sum = sum(self.weights.values())
        if not 0.95 <= weight_sum <= 1.05:  # Allow small floating point errors
            raise ValueError(f"Ranking weights must sum to 1.0, got {weight_sum}")
        
        for factor, weight in self.weights.items():
            if not 0.0 <= weight <= 1.0:
                raise ValueError(f"Weight for {factor} must be between 0.0 and 1.0")

@dataclass(frozen=True)
class FilteringCriteria:
    """Criteria for filtering search results."""
    minimum_quality_score: float
    maximum_age_years: int
    required_languages: List[str]
    preferred_venues: Dict[str, List[str]]
    exclude_authors: List[str]
    preferred_institutions: List[str]
    
    def matches(self, paper) -> bool:
        """Check if paper matches filtering criteria."""
        # Quality score check
        if paper.quality_score and paper.quality_score < self.minimum_quality_score:
            return False
        
        # Age check
        if paper.age_in_days > self.maximum_age_years * 365:
            return False
        
        # Language check (if paper has language information)
        if hasattr(paper, 'language') and paper.language:
            if paper.language.lower() not in [lang.lower() for lang in self.required_languages]:
                return False
        
        # Author exclusion check
        paper_authors = [str(author).lower() for author in paper.authors]
        excluded_authors = [author.lower() for author in self.exclude_authors]
        if any(excluded in author for excluded in excluded_authors for author in paper_authors):
            return False
        
        return True

@dataclass(frozen=True)
class DomainConfiguration:
    """
    Complete domain configuration for research paper discovery.
    
    This value object demonstrates:
    - Complex domain configuration management
    - Immutable configuration with validation
    - Composition of multiple configuration aspects
    - Factory methods for configuration loading
    """
    name: str
    description: str
    version: str
    created_by: str
    last_updated: str
    search_configuration: Dict[str, Any]
    strategies: Dict[str, SearchStrategy]
    ranking: RankingConfiguration
    filtering: FilteringCriteria
    concept_extraction: Dict[str, Any]
    quality_assessment: Dict[str, Any]
    validation: Dict[str, Any]
    analytics: Dict[str, Any]
    
    def __post_init__(self):
        """Validate complete configuration."""
        self._validate_metadata()
        self._validate_search_configuration()
        self._validate_strategies()
    
    def _validate_metadata(self):
        """Validate configuration metadata."""
        if not self.name or not self.name.strip():
            raise ValueError("Configuration name is required")
        
        if not self.description or len(self.description.strip()) < 10:
            raise ValueError("Configuration description must be at least 10 characters")
        
        if not self.version or not self.version.strip():
            raise ValueError("Configuration version is required")
    
    def _validate_search_configuration(self):
        """Validate search configuration parameters."""
        required_fields = ["default_strategy", "citation_threshold", "publication_date_range"]
        for field in required_fields:
            if field not in self.search_configuration:
                raise ValueError(f"Required search configuration field missing: {field}")
        
        # Validate citation threshold
        citation_threshold = self.search_configuration.get("citation_threshold", 0)
        if not 0 <= citation_threshold <= 1000:
            raise ValueError("Citation threshold must be between 0 and 1000")
        
        # Validate date range
        date_range = self.search_configuration.get("publication_date_range", {})
        start_year = date_range.get("start_year")
        end_year = date_range.get("end_year")
        
        if start_year and end_year and start_year > end_year:
            raise ValueError("Start year must be before end year")
    
    def _validate_strategies(self):
        """Validate search strategies."""
        if not self.strategies:
            raise ValueError("At least one search strategy is required")
        
        default_strategy = self.search_configuration.get("default_strategy")
        if default_strategy and default_strategy not in self.strategies:
            raise ValueError(f"Default strategy '{default_strategy}' not found in strategies")
    
    @classmethod
    def from_yaml_file(cls, file_path: Path) -> 'DomainConfiguration':
        """
        Load domain configuration from YAML file.
        
        This factory method demonstrates:
        - Configuration loading from external files
        - Error handling for file operations
        - Validation during object construction
        - Separation of data loading from business logic
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            return cls._from_dict(data)
            
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {file_path}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'DomainConfiguration':
        """Create configuration from dictionary data."""
        # Parse strategies
        strategies = {}
        for strategy_name, strategy_data in data.get("strategies", {}).items():
            strategies[strategy_name] = SearchStrategy(
                name=strategy_data["name"],
                description=strategy_data["description"],
                weight=strategy_data.get("weight", 1.0),
                primary_keywords=strategy_data["primary_keywords"],
                secondary_keywords=strategy_data["secondary_keywords"],
                technical_terms=strategy_data.get("technical_terms", []),
                application_domains=strategy_data.get("application_domains", []),
                exclude_terms=strategy_data.get("exclude_terms", [])
            )
        
        # Parse ranking configuration
        ranking_data = data.get("ranking", {})
        ranking = RankingConfiguration(
            algorithm=ranking_data.get("algorithm", "weighted_combination"),
            weights=ranking_data.get("weights", {}),
            boost_factors=ranking_data.get("boost_factors", {})
        )
        
        # Parse filtering criteria
        filtering_data = data.get("filtering", {})
        filtering = FilteringCriteria(
            minimum_quality_score=filtering_data.get("minimum_quality_score", 0.0),
            maximum_age_years=filtering_data.get("maximum_age_years", 10),
            required_languages=filtering_data.get("required_languages", ["english"]),
            preferred_venues=filtering_data.get("preferred_venues", {}),
            exclude_authors=filtering_data.get("exclude_authors", []),
            preferred_institutions=filtering_data.get("preferred_institutions", [])
        )
        
        return cls(
            name=data["name"],
            description=data["description"],
            version=data.get("version", "1.0.0"),
            created_by=data.get("created_by", "unknown"),
            last_updated=data.get("last_updated", datetime.now().isoformat()),
            search_configuration=data["search_configuration"],
            strategies=strategies,
            ranking=ranking,
            filtering=filtering,
            concept_extraction=data.get("concept_extraction", {}),
            quality_assessment=data.get("quality_assessment", {}),
            validation=data.get("validation", {}),
            analytics=data.get("analytics", {})
        )
    
    def get_default_strategy(self) -> SearchStrategy:
        """Get the default search strategy."""
        default_name = self.search_configuration.get("default_strategy")
        if not default_name or default_name not in self.strategies:
            # Return first strategy if default not specified or invalid
            return next(iter(self.strategies.values()))
        return self.strategies[default_name]
    
    def get_strategy(self, strategy_name: str) -> Optional[SearchStrategy]:
        """Get a specific search strategy by name."""
        return self.strategies.get(strategy_name)
    
    def get_all_keywords(self) -> List[str]:
        """Get all keywords from all strategies."""
        all_keywords = []
        for strategy in self.strategies.values():
            all_keywords.extend(strategy.get_all_keywords())
        return list(set(all_keywords))  # Remove duplicates
    
    def validate(self) -> None:
        """Perform comprehensive validation of the configuration."""
        # Validation is already performed in __post_init__
        # This method can be extended for runtime validation
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "created_by": self.created_by,
            "last_updated": self.last_updated,
            "search_configuration": self.search_configuration,
            "strategies": {
                name: {
                    "name": strategy.name,
                    "description": strategy.description,
                    "weight": strategy.weight,
                    "primary_keywords": strategy.primary_keywords,
                    "secondary_keywords": strategy.secondary_keywords,
                    "technical_terms": strategy.technical_terms,
                    "application_domains": strategy.application_domains,
                    "exclude_terms": strategy.exclude_terms
                }
                for name, strategy in self.strategies.items()
            },
            "ranking": {
                "algorithm": self.ranking.algorithm,
                "weights": self.ranking.weights,
                "boost_factors": self.ranking.boost_factors
            },
            "filtering": {
                "minimum_quality_score": self.filtering.minimum_quality_score,
                "maximum_age_years": self.filtering.maximum_age_years,
                "required_languages": self.filtering.required_languages,
                "preferred_venues": self.filtering.preferred_venues,
                "exclude_authors": self.filtering.exclude_authors,
                "preferred_institutions": self.filtering.preferred_institutions
            },
            "concept_extraction": self.concept_extraction,
            "quality_assessment": self.quality_assessment,
            "validation": self.validation,
            "analytics": self.analytics
        }
```

## 🔧 Configuration Management Use Case

### Configuration Repository Port

```python
# research-core/src/application/ports/config_repository_port.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path

from domain.value_objects.domain_configuration import DomainConfiguration

class ConfigRepositoryPort(ABC):
    """
    Port interface for configuration management.
    
    This interface demonstrates:
    - Repository pattern for configuration data
    - Abstraction of configuration storage
    - Support for different configuration sources
    - Hot-reloading and caching capabilities
    """
    
    @abstractmethod
    async def get_configuration(self, name: str) -> Optional[DomainConfiguration]:
        """Get domain configuration by name."""
        pass
    
    @abstractmethod
    async def get_all_configurations(self) -> List[DomainConfiguration]:
        """Get all available domain configurations."""
        pass
    
    @abstractmethod
    async def get_default_configuration(self) -> DomainConfiguration:
        """Get the default domain configuration."""
        pass
    
    @abstractmethod
    async def save_configuration(self, config: DomainConfiguration) -> None:
        """Save or update a domain configuration."""
        pass
    
    @abstractmethod
    async def delete_configuration(self, name: str) -> bool:
        """Delete a domain configuration."""
        pass
    
    @abstractmethod
    async def validate_configuration(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate configuration data and return error messages."""
        pass
    
    @abstractmethod
    async def reload_configurations(self) -> None:
        """Reload all configurations from storage."""
        pass
```

### Configuration Management Use Case

```python
# research-core/src/application/use_cases/manage_configuration_use_case.py

from typing import List, Optional, Dict, Any
import logging

from ..commands.configuration_commands import (
    CreateConfigurationCommand,
    UpdateConfigurationCommand,
    DeleteConfigurationCommand,
    ValidateConfigurationCommand
)
from ..responses.configuration_responses import (
    ConfigurationResponse,
    ConfigurationListResponse,
    ValidationResponse
)
from ..ports.config_repository_port import ConfigRepositoryPort
from ..ports.analytics_port import AnalyticsPort

from ...domain.value_objects.domain_configuration import DomainConfiguration
from ...domain.exceptions.domain_exceptions import (
    ConfigurationNotFoundError,
    ConfigurationValidationError,
    DuplicateConfigurationError
)

logger = logging.getLogger(__name__)

class ManageConfigurationUseCase:
    """
    Use case for managing domain configurations.
    
    This use case demonstrates:
    - CRUD operations for configurations
    - Validation and error handling
    - Analytics and monitoring integration
    - Hot-reloading capabilities
    """
    
    def __init__(
        self,
        config_repository: ConfigRepositoryPort,
        analytics: AnalyticsPort
    ):
        self._config_repository = config_repository
        self._analytics = analytics
    
    async def create_configuration(
        self, 
        command: CreateConfigurationCommand
    ) -> ConfigurationResponse:
        """Create a new domain configuration."""
        logger.info(f"Creating configuration: {command.name}")
        
        try:
            # Check if configuration already exists
            existing = await self._config_repository.get_configuration(command.name)
            if existing:
                raise DuplicateConfigurationError(f"Configuration '{command.name}' already exists")
            
            # Validate configuration data
            validation_errors = await self._config_repository.validate_configuration(
                command.config_data
            )
            if validation_errors:
                raise ConfigurationValidationError(
                    f"Configuration validation failed: {validation_errors}"
                )
            
            # Create domain configuration
            config = DomainConfiguration._from_dict(command.config_data)
            
            # Save configuration
            await self._config_repository.save_configuration(config)
            
            # Record analytics
            await self._analytics.record_configuration_created(
                config_name=config.name,
                created_by=command.user_id
            )
            
            logger.info(f"Configuration created successfully: {config.name}")
            return ConfigurationResponse.from_domain(config)
            
        except Exception as e:
            logger.error(f"Failed to create configuration: {e}")
            await self._analytics.record_configuration_error(
                operation="create",
                config_name=command.name,
                error=str(e),
                user_id=command.user_id
            )
            raise
    
    async def update_configuration(
        self, 
        command: UpdateConfigurationCommand
    ) -> ConfigurationResponse:
        """Update an existing domain configuration."""
        logger.info(f"Updating configuration: {command.name}")
        
        try:
            # Check if configuration exists
            existing = await self._config_repository.get_configuration(command.name)
            if not existing:
                raise ConfigurationNotFoundError(f"Configuration '{command.name}' not found")
            
            # Validate updated configuration data
            validation_errors = await self._config_repository.validate_configuration(
                command.config_data
            )
            if validation_errors:
                raise ConfigurationValidationError(
                    f"Configuration validation failed: {validation_errors}"
                )
            
            # Create updated domain configuration
            updated_config = DomainConfiguration._from_dict(command.config_data)
            
            # Save updated configuration
            await self._config_repository.save_configuration(updated_config)
            
            # Trigger hot reload if requested
            if command.hot_reload:
                await self._config_repository.reload_configurations()
            
            # Record analytics
            await self._analytics.record_configuration_updated(
                config_name=updated_config.name,
                updated_by=command.user_id,
                changes=self._calculate_changes(existing, updated_config)
            )
            
            logger.info(f"Configuration updated successfully: {updated_config.name}")
            return ConfigurationResponse.from_domain(updated_config)
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            await self._analytics.record_configuration_error(
                operation="update",
                config_name=command.name,
                error=str(e),
                user_id=command.user_id
            )
            raise
    
    async def delete_configuration(
        self, 
        command: DeleteConfigurationCommand
    ) -> bool:
        """Delete a domain configuration."""
        logger.info(f"Deleting configuration: {command.name}")
        
        try:
            # Check if configuration exists
            existing = await self._config_repository.get_configuration(command.name)
            if not existing:
                raise ConfigurationNotFoundError(f"Configuration '{command.name}' not found")
            
            # Prevent deletion of default configuration
            default_config = await self._config_repository.get_default_configuration()
            if existing.name == default_config.name:
                raise ConfigurationValidationError("Cannot delete default configuration")
            
            # Delete configuration
            success = await self._config_repository.delete_configuration(command.name)
            
            if success:
                # Record analytics
                await self._analytics.record_configuration_deleted(
                    config_name=command.name,
                    deleted_by=command.user_id
                )
                
                logger.info(f"Configuration deleted successfully: {command.name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete configuration: {e}")
            await self._analytics.record_configuration_error(
                operation="delete",
                config_name=command.name,
                error=str(e),
                user_id=command.user_id
            )
            raise
    
    async def list_configurations(self) -> ConfigurationListResponse:
        """List all available domain configurations."""
        try:
            configs = await self._config_repository.get_all_configurations()
            default_config = await self._config_repository.get_default_configuration()
            
            return ConfigurationListResponse(
                configurations=[
                    ConfigurationResponse.from_domain(config) 
                    for config in configs
                ],
                default_configuration=default_config.name,
                total_count=len(configs)
            )
            
        except Exception as e:
            logger.error(f"Failed to list configurations: {e}")
            raise
    
    async def validate_configuration(
        self, 
        command: ValidateConfigurationCommand
    ) -> ValidationResponse:
        """Validate configuration data without saving."""
        try:
            # Perform repository-level validation
            repo_errors = await self._config_repository.validate_configuration(
                command.config_data
            )
            
            # Perform domain-level validation
            domain_errors = []
            try:
                DomainConfiguration._from_dict(command.config_data)
            except Exception as e:
                domain_errors.append(str(e))
            
            all_errors = repo_errors + domain_errors
            is_valid = len(all_errors) == 0
            
            return ValidationResponse(
                is_valid=is_valid,
                errors=all_errors,
                warnings=self._generate_warnings(command.config_data) if is_valid else []
            )
            
        except Exception as e:
            logger.error(f"Failed to validate configuration: {e}")
            return ValidationResponse(
                is_valid=False,
                errors=[f"Validation error: {e}"],
                warnings=[]
            )
    
    def _calculate_changes(
        self, 
        old_config: DomainConfiguration, 
        new_config: DomainConfiguration
    ) -> Dict[str, Any]:
        """Calculate changes between configurations for analytics."""
        changes = {}
        
        # Compare basic metadata
        if old_config.description != new_config.description:
            changes["description_changed"] = True
        
        # Compare strategies
        old_strategies = set(old_config.strategies.keys())
        new_strategies = set(new_config.strategies.keys())
        
        if old_strategies != new_strategies:
            changes["strategies_modified"] = {
                "added": list(new_strategies - old_strategies),
                "removed": list(old_strategies - new_strategies)
            }
        
        # Compare ranking weights
        if old_config.ranking.weights != new_config.ranking.weights:
            changes["ranking_weights_changed"] = True
        
        return changes
    
    def _generate_warnings(self, config_data: Dict[str, Any]) -> List[str]:
        """Generate warnings for configuration data."""
        warnings = []
        
        # Check for potential performance issues
        search_config = config_data.get("search_configuration", {})
        max_concurrent = search_config.get("max_concurrent_searches", 3)
        
        if max_concurrent > 5:
            warnings.append(
                "High concurrent search limit may impact performance"
            )
        
        # Check for overly broad search strategies
        strategies = config_data.get("strategies", {})
        for strategy_name, strategy_data in strategies.items():
            primary_keywords = strategy_data.get("primary_keywords", [])
            if len(primary_keywords) > 15:
                warnings.append(
                    f"Strategy '{strategy_name}' has many primary keywords, "
                    "which may reduce search precision"
                )
        
        return warnings
```

## 🧪 Testing Strategies

### Configuration Testing

```python
# tests/unit/domain/test_domain_configuration.py

import pytest
from pathlib import Path
import tempfile
import yaml

from domain.value_objects.domain_configuration import (
    DomainConfiguration,
    SearchStrategy,
    RankingConfiguration,
    FilteringCriteria
)
from domain.exceptions.domain_exceptions import ConfigurationError

class TestDomainConfiguration:
    """Test suite for domain configuration value objects."""
    
    def test_create_valid_search_strategy(self):
        """Test creating a valid search strategy."""
        # Arrange & Act
        strategy = SearchStrategy(
            name="Test Strategy",
            description="A test search strategy",
            weight=1.0,
            primary_keywords=["keyword1", "keyword2", "keyword3"],
            secondary_keywords=["secondary1", "secondary2", "secondary3", "secondary4", "secondary5"],
            technical_terms=["technical1", "technical2"],
            application_domains=["domain1", "domain2"],
            exclude_terms=["exclude1", "exclude2"]
        )
        
        # Assert
        assert strategy.name == "Test Strategy"
        assert strategy.weight == 1.0
        assert len(strategy.primary_keywords) == 3
        assert len(strategy.get_all_keywords()) == 10  # 3 + 5 + 2
    
    def test_search_strategy_validates_keywords(self):
        """Test that search strategy validates keyword requirements."""
        # Act & Assert
        with pytest.raises(ValueError, match="At least 3 primary keywords required"):
            SearchStrategy(
                name="Invalid Strategy",
                description="Strategy with too few keywords",
                weight=1.0,
                primary_keywords=["keyword1", "keyword2"],  # Too few
                secondary_keywords=["sec1", "sec2", "sec3", "sec4", "sec5"],
                technical_terms=[],
                application_domains=[],
                exclude_terms=[]
            )
    
    def test_search_strategy_calculates_relevance(self):
        """Test relevance calculation for search strategy."""
        # Arrange
        strategy = SearchStrategy(
            name="ML Strategy",
            description="Machine learning strategy",
            weight=1.0,
            primary_keywords=["machine learning", "neural networks", "deep learning"],
            secondary_keywords=["AI", "artificial intelligence", "ML", "algorithms", "models"],
            technical_terms=["CNN", "RNN", "transformer"],
            application_domains=["computer vision", "NLP"],
            exclude_terms=["ethics", "bias"]
        )
        
        text = "This paper presents a machine learning approach using neural networks for computer vision applications."
        
        # Act
        relevance = strategy.calculate_term_relevance(text)
        
        # Assert
        assert 0.0 <= relevance <= 1.0
        assert relevance > 0.5  # Should be relevant due to keywords
    
    def test_domain_configuration_from_yaml_file(self):
        """Test loading domain configuration from YAML file."""
        # Arrange
        config_data = {
            "name": "test_domain",
            "description": "A test domain configuration",
            "version": "1.0.0",
            "search_configuration": {
                "default_strategy": "test_strategy",
                "citation_threshold": 5,
                "publication_date_range": {
                    "start_year": 2020,
                    "end_year": 2024
                }
            },
            "strategies": {
                "test_strategy": {
                    "name": "Test Strategy",
                    "description": "A test strategy",
                    "weight": 1.0,
                    "primary_keywords": ["test1", "test2", "test3"],
                    "secondary_keywords": ["sec1", "sec2", "sec3", "sec4", "sec5"],
                    "technical_terms": ["tech1"],
                    "application_domains": ["domain1"],
                    "exclude_terms": ["exclude1"]
                }
            },
            "ranking": {
                "algorithm": "weighted_combination",
                "weights": {
                    "relevance_score": 0.4,
                    "citation_impact": 0.3,
                    "venue_prestige": 0.3
                },
                "boost_factors": {
                    "peer_reviewed": 1.2
                }
            },
            "filtering": {
                "minimum_quality_score": 0.3,
                "maximum_age_years": 10,
                "required_languages": ["english"],
                "preferred_venues": {},
                "exclude_authors": [],
                "preferred_institutions": []
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = Path(f.name)
        
        try:
            # Act
            config = DomainConfiguration.from_yaml_file(temp_path)
            
            # Assert
            assert config.name == "test_domain"
            assert "test_strategy" in config.strategies
            assert config.get_default_strategy().name == "Test Strategy"
            
        finally:
            temp_path.unlink()  # Clean up
    
    def test_domain_configuration_validates_required_fields(self):
        """Test that domain configuration validates required fields."""
        # Arrange
        invalid_data = {
            "description": "Missing name field",
            # "name" field is missing
            "search_configuration": {},
            "strategies": {}
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Configuration name is required"):
            DomainConfiguration._from_dict(invalid_data)
    
    def test_ranking_configuration_validates_weights(self):
        """Test that ranking configuration validates weight sums."""
        # Act & Assert
        with pytest.raises(ValueError, match="Ranking weights must sum to 1.0"):
            RankingConfiguration(
                algorithm="weighted_combination",
                weights={
                    "relevance_score": 0.5,
                    "citation_impact": 0.3,
                    "venue_prestige": 0.3  # Sum = 1.1, invalid
                },
                boost_factors={}
            )
    
    def test_filtering_criteria_matches_paper(self):
        """Test that filtering criteria correctly matches papers."""
        # Arrange
        criteria = FilteringCriteria(
            minimum_quality_score=0.5,
            maximum_age_years=5,
            required_languages=["english"],
            preferred_venues={},
            exclude_authors=["Problematic Author"],
            preferred_institutions=[]
        )
        
        # Create mock paper that should match
        mock_paper = type('MockPaper', (), {
            'quality_score': 0.7,
            'age_in_days': 365,  # 1 year old
            'authors': [type('Author', (), {'__str__': lambda self: "Good Author"})()]
        })()
        
        # Act
        matches = criteria.matches(mock_paper)
        
        # Assert
        assert matches is True
    
    @pytest.mark.parametrize("invalid_weight", [-0.1, 1.1, 2.0])
    def test_search_strategy_validates_weight_range(self, invalid_weight):
        """Test that search strategy validates weight range."""
        with pytest.raises(ValueError, match="Strategy weight must be between 0.0 and 1.0"):
            SearchStrategy(
                name="Test Strategy",
                description="Test description",
                weight=invalid_weight,
                primary_keywords=["k1", "k2", "k3"],
                secondary_keywords=["s1", "s2", "s3", "s4", "s5"],
                technical_terms=[],
                application_domains=[],
                exclude_terms=[]
            )
```

### Integration Testing with Real Configurations

```python
# tests/integration/test_configuration_loading.py

import pytest
from pathlib import Path

from infrastructure.repositories.yaml_config_repository import YamlConfigRepository
from application.use_cases.manage_configuration_use_case import ManageConfigurationUseCase

class TestConfigurationLoading:
    """Integration tests for configuration loading."""
    
    @pytest.fixture
    def config_repository(self):
        """Create configuration repository for testing."""
        config_dir = Path(__file__).parent.parent.parent / "config"
        return YamlConfigRepository(config_directory=config_dir)
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_load_all_real_configurations(self, config_repository):
        """Test loading all real configuration files."""
        # Act
        configs = await config_repository.get_all_configurations()
        
        # Assert
        assert len(configs) > 0
        
        # Verify each configuration is valid
        for config in configs:
            assert config.name
            assert config.description
            assert len(config.strategies) > 0
            assert config.get_default_strategy() is not None
            
            # Validate configuration structure
            config.validate()
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_load_ai_security_configuration(self, config_repository):
        """Test loading the AI security configuration specifically."""
        # Act
        config = await config_repository.get_configuration("artificial_intelligence_security")
        
        # Assert
        assert config is not None
        assert config.name == "artificial_intelligence_security"
        assert "adversarial_machine_learning_defense" in config.strategies
        
        # Verify strategy content
        ml_strategy = config.get_strategy("adversarial_machine_learning_defense")
        assert "adversarial machine learning" in ml_strategy.primary_keywords
        assert "adversarial attacks" in ml_strategy.primary_keywords
```

## 🔗 Related Documentation

- **[[System-Architecture]]**: How configurations fit into the overall system
- **[[Paper-Discovery-UseCase]]**: How configurations drive paper discovery
- **[[Validation-Rules]]**: Configuration validation and business rules
- **[[Configuration-Management-UseCase]]**: CRUD operations for configurations
- **[[External-API-Integration]]**: How configurations affect external service calls

## 🚀 Extension Points

### Future Enhancements

1. **Machine Learning Configuration**: AI-powered configuration optimization
2. **A/B Testing**: Compare configuration effectiveness
3. **User Personalization**: User-specific configuration preferences
4. **Dynamic Updates**: Real-time configuration updates based on performance
5. **Template System**: Configuration templates for common domains

### Configuration Patterns

1. **Inheritance**: Base configurations with domain-specific overrides
2. **Composition**: Combine multiple configuration aspects
3. **Versioning**: Track configuration changes over time
4. **Migration**: Automatic updates for configuration schema changes

---

*The Research Domain Configuration system demonstrates how sophisticated business logic can be externalized into configuration files, enabling domain experts to customize system behavior without code changes while maintaining type safety and validation.*
