"""
Multi-Strategy Concept Extraction - Decomposed Module Reference

This file has been decomposed into multiple modules following Clean Architecture
and the Strategy pattern for better maintainability and testability.

New Module Structure:
- concept_extraction/
  ├── __init__.py                    # Public API
  ├── concept_extraction_strategy.py # Abstract strategy interface
  ├── multi_strategy_extractor.py    # Main orchestrator
  ├── utilities.py                   # Common utilities
  ├── strategies/
  │   ├── rule_based_strategy.py     # Rule-based extraction
  │   ├── statistical_strategy.py    # Statistical extraction
  │   └── embedding_strategy.py      # Embedding-based extraction
  └── factories/
      └── strategy_factory.py        # Strategy creation

Value Objects moved to:
- domain/value_objects/extraction/extraction_result.py

Usage:
    from src.domain.services.concept_extraction import MultiStrategyConceptExtractor
    
    extractor = MultiStrategyConceptExtractor()
    results = extractor.extract_concepts(text, config)

Educational Benefits:
- Single Responsibility Principle: Each strategy in its own module
- Strategy Pattern: Clean separation of algorithms
- Factory Pattern: Centralized strategy creation
- Open/Closed Principle: Easy to add new strategies
- Testability: Each component can be tested in isolation
"""

# For backward compatibility, import the main extractor
from src.domain.services.concept_extraction import MultiStrategyConceptExtractor

# Re-export for existing code
__all__ = ["MultiStrategyConceptExtractor"]
