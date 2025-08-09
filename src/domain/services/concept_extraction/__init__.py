"""
Concept Extraction Module - Public API

This module provides a clean public interface to the concept extraction subsystem,
following Clean Architecture principles.

Educational Notes:
- Demonstrates Facade pattern for complex subsystem
- Shows proper module organization for maintainability
- Provides single entry point for concept extraction functionality
- Illustrates how to hide internal complexity from clients

Design Patterns Applied:
- Facade Pattern: Simple interface to complex subsystem
- Factory Pattern: Strategy creation handled internally
- Strategy Pattern: Multiple extraction algorithms available
"""

from .multi_strategy_extractor import MultiStrategyConceptExtractor
from .concept_extraction_strategy import ConceptExtractionStrategy
from .strategies.rule_based_strategy import RuleBasedExtractionStrategy
from .strategies.statistical_strategy import StatisticalExtractionStrategy
from .strategies.embedding_strategy import EmbeddingBasedExtractionStrategy
from .factories.strategy_factory import ConceptExtractionStrategyFactory
from ..value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration

__all__ = [
    "MultiStrategyConceptExtractor",
    "ConceptExtractionStrategy", 
    "RuleBasedExtractionStrategy",
    "StatisticalExtractionStrategy",
    "EmbeddingBasedExtractionStrategy",
    "ConceptExtractionStrategyFactory",
    "ExtractionResult",
    "StrategyConfiguration",
]
