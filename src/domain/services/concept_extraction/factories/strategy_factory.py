"""
Concept Extraction Strategy Factory

Educational Notes:
- Demonstrates Factory pattern for strategy creation
- Shows proper dependency injection and configuration
- Illustrates how to encapsulate object creation complexity

Design Patterns Applied:
- Factory Pattern: Creates appropriate strategy instances
- Dependency Injection: Strategies receive their dependencies
- Configuration Pattern: Strategy creation driven by configuration
"""

from typing import Dict, List, Any, Optional
import logging

from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..strategies.rule_based_strategy import RuleBasedExtractionStrategy
from ..strategies.statistical_strategy import StatisticalExtractionStrategy
from ..strategies.embedding_strategy import EmbeddingBasedExtractionStrategy
from src.domain.value_objects.extraction.extraction_result import StrategyConfiguration


class ConceptExtractionStrategyFactory:
    """
    Factory for creating concept extraction strategy instances.
    
    Educational Notes:
    - Encapsulates strategy creation logic
    - Provides single point for strategy configuration
    - Enables easy addition of new strategies
    """
    
    @staticmethod
    def create_strategy(
        strategy_name: str,
        config: StrategyConfiguration
    ) -> ConceptExtractionStrategy:
        """
        Create strategy instance based on name and configuration.
        
        Args:
            strategy_name: Name of strategy to create
            config: Configuration for strategy
            
        Returns:
            Configured strategy instance
            
        Raises:
            ValueError: If strategy name is not recognized
        """
        strategy_map = {
            "rule_based": RuleBasedExtractionStrategy,
            "statistical": StatisticalExtractionStrategy,
            "embedding": EmbeddingBasedExtractionStrategy,
        }
        
        if strategy_name not in strategy_map:
            available = ", ".join(strategy_map.keys())
            raise ValueError(
                f"Unknown strategy '{strategy_name}'. "
                f"Available strategies: {available}"
            )
        
        strategy_class = strategy_map[strategy_name]
        return strategy_class(config)
    
    @staticmethod
    def create_all_strategies(
        config: StrategyConfiguration
    ) -> List[ConceptExtractionStrategy]:
        """
        Create all available strategy instances.
        
        Args:
            config: Configuration for all strategies
            
        Returns:
            List of all configured strategy instances
        """
        return [
            ConceptExtractionStrategyFactory.create_strategy(name, config)
            for name in ["rule_based", "statistical", "embedding"]
        ]
    
    @staticmethod
    def get_available_strategies() -> List[str]:
        """Get list of available strategy names."""
        return ["rule_based", "statistical", "embedding"]
