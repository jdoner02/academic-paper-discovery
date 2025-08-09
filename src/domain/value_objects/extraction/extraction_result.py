"""
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

class ExtractionResult:
    """
    Immutable value object representing concept extraction results.

    Educational Note:
    This value object encapsulates extraction results with metadata,
    demonstrating how to package complex algorithmic outputs with
    full provenance and traceability for academic transparency.
    """

    concepts: List[Concept]
    metadata: Dict[str, Any]

    @property
    def total_concepts(self) -> int:
        """Get total number of extracted concepts."""
        return len(self.concepts)

    @property
    def average_relevance_score(self) -> float:
        """Calculate average relevance score across all concepts."""
        if not self.concepts:
            return 0.0
        return sum(c.relevance_score for c in self.concepts) / len(self.concepts)

    @property
    def total_frequency(self) -> int:
        """Get total frequency count across all concepts."""
        return sum(c.frequency for c in self.concepts)

    def filter_by_relevance(self, min_score: float) -> List[Concept]:
        """Filter concepts by minimum relevance score."""
        return [c for c in self.concepts if c.relevance_score >= min_score]

    def filter_by_frequency(self, min_frequency: int) -> List[Concept]:
        """Filter concepts by minimum frequency."""
        return [c for c in self.concepts if c.frequency >= min_frequency]


@dataclass(frozen=True)


class StrategyConfiguration:
    """
    Configuration for concept extraction strategies.

    Educational Note:
    Immutable configuration object that encapsulates all parameters
    needed for multi-strategy extraction, demonstrating how to make
    algorithmic behavior configurable and reproducible.
    """

    domain: str
    min_concept_frequency: int = 1
    enable_all_strategies: bool = True
    strategy_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "rule_based": 0.4,
            "statistical": 0.3,
            "embedding_based": 0.3,
        }
    )
    consolidate_results: bool = True
    merge_similar_concepts: bool = True
    similarity_threshold: float = 0.8
    extract_hierarchies: bool = True
    use_domain_ontology: bool = False
    use_tfidf: bool = True
    use_textrank: bool = True
    use_topic_modeling: bool = False  # Usually for corpora, not single documents
    max_concepts_per_strategy: int = 50


# Educational Note: Abstract Strategy interface defines the extraction contract

