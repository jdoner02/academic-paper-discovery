"""
Domain services package.

Domain services contain business logic that doesn't naturally fit within
any single entity or value object. They coordinate complex operations
between multiple domain objects.

Educational Note:
- Domain services implement business logic that spans multiple entities
- They should be stateless and focused on a single responsibility
- Use dependency injection for external concerns
"""

from .paper_download_service import PaperDownloadService
from .concept_extractor import (
    ConceptExtractor,
    ConceptExtractionStrategy,
    TFIDFConceptExtractor,
    ExtractionConfiguration,
)
from .multi_strategy_concept_extractor import (
    ConceptExtractionStrategy as MultiStrategyInterface,
    RuleBasedExtractionStrategy,
    StatisticalExtractionStrategy,
    EmbeddingBasedExtractionStrategy,
    MultiStrategyConceptExtractor,
    ExtractionResult,
    StrategyConfiguration,
)

__all__ = [
    "PaperDownloadService",
    "ConceptExtractor",
    "ConceptExtractionStrategy",
    "TFIDFConceptExtractor",
    "ExtractionConfiguration",
    "MultiStrategyInterface",
    "RuleBasedExtractionStrategy",
    "StatisticalExtractionStrategy",
    "EmbeddingBasedExtractionStrategy",
    "MultiStrategyConceptExtractor",
    "ExtractionResult",
    "StrategyConfiguration",
]
