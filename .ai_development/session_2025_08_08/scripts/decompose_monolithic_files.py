#!/usr/bin/env python3
"""
Monolithic File Decomposition Script

This script decomposes the massive multi_strategy_concept_extractor.py file (1,504 lines)
into proper Clean Architecture modules following the Strategy pattern.

Educational Notes:
- Demonstrates proper application of Single Responsibility Principle
- Shows how to decompose monolithic classes using Strategy pattern
- Illustrates Clean Architecture module organization
- Provides template for breaking up large domain services

Design Principles Applied:
- Strategy Pattern: Each extraction strategy becomes its own module
- Factory Pattern: Strategy creation separated into factory
- Value Object extraction: Common value objects moved to value_objects/
- Interface Segregation: Abstract interfaces separated from implementations
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
import re


class MonolithicFileDecomposer:
    """
    Decomposes large monolithic files into Clean Architecture compliant modules.

    Educational Notes:
    - Uses systematic approach to file decomposition
    - Maintains educational documentation in extracted modules
    - Preserves import relationships and dependencies
    - Creates proper module hierarchy following Clean Architecture
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.src_path = self.base_path / "src"
        self.operations_log: List[str] = []

    def decompose_multi_strategy_extractor(self):
        """Decompose the massive multi_strategy_concept_extractor.py file."""
        print("🔧 Decomposing multi_strategy_concept_extractor.py (1,504 lines)...")

        source_file = (
            self.src_path / "domain/services/multi_strategy_concept_extractor.py"
        )
        if not source_file.exists():
            print(f"❌ Source file not found: {source_file}")
            return

        content = source_file.read_text()

        # Create target module structure for Strategy pattern
        self._create_strategy_module_structure()

        # Extract and create each component
        self._extract_common_utilities(content)
        self._extract_value_objects(content)
        self._extract_strategy_interface(content)
        self._extract_rule_based_strategy(content)
        self._extract_statistical_strategy(content)
        self._extract_embedding_strategy(content)
        self._extract_orchestrator(content)
        self._create_strategy_factory(content)

        # Create consolidated imports module
        self._create_imports_module()

        # Backup original file and replace with new structure
        self._backup_and_replace_original(source_file)

        print("✅ Multi-strategy extractor decomposition completed!")
        self._print_decomposition_summary()

    def _create_strategy_module_structure(self):
        """Create proper module structure for Strategy pattern."""
        directories = [
            "src/domain/services/concept_extraction",
            "src/domain/services/concept_extraction/strategies",
            "src/domain/services/concept_extraction/factories",
            "src/domain/value_objects/extraction",
        ]

        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)

            # Create __init__.py for Python module recognition
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Module initialization."""\n')

            self._log_operation(f"Created module directory: {directory}")

    def _extract_common_utilities(self, content: str):
        """Extract common utility functions."""
        utilities_content = self._extract_section(
            content, "# COMMON CONSTANTS FOR TEXT PROCESSING", "class ExtractionResult:"
        )

        utilities_file = (
            self.src_path / "domain/services/concept_extraction/utilities.py"
        )
        utilities_file.write_text(self._create_utilities_module(utilities_content))
        self._log_operation("Created utilities.py")

    def _extract_value_objects(self, content: str):
        """Extract value objects to appropriate location."""
        # Extract ExtractionResult
        extraction_result = self._extract_class_definition(content, "ExtractionResult")

        # Extract StrategyConfiguration
        strategy_config = self._extract_class_definition(
            content, "StrategyConfiguration"
        )

        # Create extraction value objects file
        value_objects_content = self._create_extraction_value_objects(
            extraction_result, strategy_config
        )

        value_objects_file = (
            self.src_path / "domain/value_objects/extraction/extraction_result.py"
        )
        value_objects_file.write_text(value_objects_content)
        self._log_operation("Created extraction value objects")

    def _extract_strategy_interface(self, content: str):
        """Extract abstract strategy interface."""
        interface_content = self._extract_class_definition(
            content, "ConceptExtractionStrategy"
        )

        interface_file = (
            self.src_path
            / "domain/services/concept_extraction/concept_extraction_strategy.py"
        )
        interface_file.write_text(self._create_strategy_interface(interface_content))
        self._log_operation("Created strategy interface")

    def _extract_rule_based_strategy(self, content: str):
        """Extract rule-based strategy implementation."""
        strategy_content = self._extract_class_definition(
            content, "RuleBasedExtractionStrategy"
        )

        strategy_file = (
            self.src_path
            / "domain/services/concept_extraction/strategies/rule_based_strategy.py"
        )
        strategy_file.write_text(self._create_rule_based_strategy(strategy_content))
        self._log_operation("Created rule-based strategy")

    def _extract_statistical_strategy(self, content: str):
        """Extract statistical strategy implementation."""
        strategy_content = self._extract_class_definition(
            content, "StatisticalExtractionStrategy"
        )

        strategy_file = (
            self.src_path
            / "domain/services/concept_extraction/strategies/statistical_strategy.py"
        )
        strategy_file.write_text(self._create_statistical_strategy(strategy_content))
        self._log_operation("Created statistical strategy")

    def _extract_embedding_strategy(self, content: str):
        """Extract embedding-based strategy implementation."""
        strategy_content = self._extract_class_definition(
            content, "EmbeddingBasedExtractionStrategy"
        )

        strategy_file = (
            self.src_path
            / "domain/services/concept_extraction/strategies/embedding_strategy.py"
        )
        strategy_file.write_text(self._create_embedding_strategy(strategy_content))
        self._log_operation("Created embedding strategy")

    def _extract_orchestrator(self, content: str):
        """Extract main orchestrator class."""
        orchestrator_content = self._extract_class_definition(
            content, "MultiStrategyConceptExtractor"
        )

        orchestrator_file = (
            self.src_path
            / "domain/services/concept_extraction/multi_strategy_extractor.py"
        )
        orchestrator_file.write_text(self._create_orchestrator(orchestrator_content))
        self._log_operation("Created orchestrator")

    def _create_strategy_factory(self, content: str):
        """Create strategy factory for Clean Architecture."""
        _ = content  # Not needed for factory creation
        factory_content = self._create_factory_module()

        factory_file = (
            self.src_path
            / "domain/services/concept_extraction/factories/strategy_factory.py"
        )
        factory_file.write_text(factory_content)
        self._log_operation("Created strategy factory")

    def _create_imports_module(self):
        """Create consolidated imports module."""
        imports_content = '''"""
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
'''

        init_file = self.src_path / "domain/services/concept_extraction/__init__.py"
        init_file.write_text(imports_content)
        self._log_operation("Created concept extraction public API")

    def _extract_section(self, content: str, start_marker: str, end_marker: str) -> str:
        """Extract a section of code between markers."""
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker, start_idx)

        if start_idx == -1 or end_idx == -1:
            return ""

        return content[start_idx:end_idx]

    def _extract_class_definition(self, content: str, class_name: str) -> str:
        """Extract complete class definition including docstring and methods."""
        pattern = rf"^class {class_name}.*?(?=^class|\Z)"
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

        if match:
            return match.group(0)
        return ""

    def _create_utilities_module(self, utilities_content: str) -> str:
        """Create utilities module with proper imports."""
        return f'''"""
Common Utilities for Concept Extraction

Educational Notes:
- Contains shared constants and utility functions
- Demonstrates separation of cross-cutting concerns
- Shows proper utility module organization
"""

import re
import logging
from typing import Any, Callable
from functools import wraps

{utilities_content}
'''

    def _create_extraction_value_objects(
        self, extraction_result: str, strategy_config: str
    ) -> str:
        """Create value objects module."""
        return f'''"""
Extraction Value Objects

Educational Notes:
- Demonstrates Value Object pattern implementation
- Shows immutable data structures for domain concepts
- Illustrates proper encapsulation of extraction metadata
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from src.domain.entities.concept import Concept

{extraction_result}

{strategy_config}
'''

    def _create_strategy_interface(self, interface_content: str) -> str:
        """Create strategy interface module."""
        return f'''"""
Concept Extraction Strategy Interface

Educational Notes:
- Demonstrates Strategy pattern interface definition
- Shows proper abstract base class design
- Illustrates contract definition for pluggable algorithms
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration

{interface_content}
'''

    def _create_rule_based_strategy(self, strategy_content: str) -> str:
        """Create rule-based strategy module."""
        return f'''"""
Rule-Based Concept Extraction Strategy

Educational Notes:
- Implements Strategy pattern for rule-based extraction
- Demonstrates algorithmic approach to concept identification
- Shows proper separation of extraction logic
"""

import re
import spacy
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import Counter, defaultdict

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..utilities import _safe_extraction, COMMON_STOP_WORDS

{strategy_content}
'''

    def _create_statistical_strategy(self, strategy_content: str) -> str:
        """Create statistical strategy module."""
        return f'''"""
Statistical Concept Extraction Strategy

Educational Notes:
- Implements Strategy pattern for statistical extraction
- Demonstrates machine learning approach to concept identification
- Shows proper integration of sklearn algorithms
"""

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..utilities import _safe_extraction

{strategy_content}
'''

    def _create_embedding_strategy(self, strategy_content: str) -> str:
        """Create embedding strategy module."""
        return f'''"""
Embedding-Based Concept Extraction Strategy

Educational Notes:
- Implements Strategy pattern for embedding-based extraction
- Demonstrates neural network approach to concept identification
- Shows proper integration of modern NLP techniques
"""

import numpy as np
import networkx as nx
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import defaultdict

from src.domain.entities.concept import Concept
from src.domain.value_objects.embedding_vector import EmbeddingVector
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..utilities import _safe_extraction

{strategy_content}
'''

    def _create_orchestrator(self, orchestrator_content: str) -> str:
        """Create orchestrator module."""
        return f'''"""
Multi-Strategy Concept Extractor Orchestrator

Educational Notes:
- Demonstrates Composite pattern for strategy aggregation
- Shows proper orchestration of multiple extraction strategies
- Illustrates result consolidation and ranking algorithms
"""

from typing import List, Dict, Any, Optional, Set
from collections import defaultdict, Counter
import logging

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from .concept_extraction_strategy import ConceptExtractionStrategy
from .strategies.rule_based_strategy import RuleBasedExtractionStrategy
from .strategies.statistical_strategy import StatisticalExtractionStrategy
from .strategies.embedding_strategy import EmbeddingBasedExtractionStrategy

{orchestrator_content}
'''

    def _create_factory_module(self) -> str:
        """Create strategy factory module."""
        return '''"""
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
'''

    def _backup_and_replace_original(self, source_file: Path):
        """Backup original file and replace with new structure reference."""
        # Create backup
        backup_file = source_file.with_suffix(".py.backup")
        shutil.copy2(source_file, backup_file)
        self._log_operation(f"Created backup: {backup_file.name}")

        # Replace with new structure reference
        new_content = '''"""
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
'''

        source_file.write_text(new_content)
        self._log_operation("Replaced original with structure reference")

    def _print_decomposition_summary(self):
        """Print summary of decomposition results."""
        print("\n📊 Decomposition Summary:")
        print("  🎯 Strategy Pattern Implementation:")
        print("    - Abstract interface: concept_extraction_strategy.py")
        print("    - Rule-based strategy: strategies/rule_based_strategy.py")
        print("    - Statistical strategy: strategies/statistical_strategy.py")
        print("    - Embedding strategy: strategies/embedding_strategy.py")
        print("  🏭 Factory Pattern:")
        print("    - Strategy factory: factories/strategy_factory.py")
        print("  🎭 Orchestrator:")
        print("    - Multi-strategy extractor: multi_strategy_extractor.py")
        print("  📦 Value Objects:")
        print("    - Extraction results: value_objects/extraction/extraction_result.py")
        print("  🔧 Utilities:")
        print("    - Common utilities: utilities.py")

        print(
            f"\n✨ Decomposed 1,504 lines into {len(self.operations_log)} focused modules!"
        )
        print("🎓 This demonstrates proper application of:")
        print("  - Single Responsibility Principle")
        print("  - Strategy Pattern")
        print("  - Factory Pattern")
        print("  - Clean Architecture layer separation")

    def _log_operation(self, message: str):
        """Log an operation for tracking."""
        self.operations_log.append(message)
        print(f"  ✓ {message}")


def main():
    """Execute monolithic file decomposition."""
    current_dir = os.getcwd()

    if Path(current_dir).name != "research-paper-aggregator":
        print("❌ Please run this script from the research-paper-aggregator directory")
        exit(1)

    decomposer = MonolithicFileDecomposer(current_dir)
    decomposer.decompose_multi_strategy_extractor()


if __name__ == "__main__":
    main()
