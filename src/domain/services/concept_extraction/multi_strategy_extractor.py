"""
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

class MultiStrategyConceptExtractor:
    """
    Orchestrator for multi-strategy concept extraction.

    Educational Note:
    This class implements the Composite pattern to combine results from
    multiple extraction strategies, demonstrating how to aggregate
    diverse algorithmic approaches for comprehensive concept coverage.

    Design Patterns Applied:
    - Composite Pattern: Treats individual strategies and strategy combinations uniformly
    - Strategy Pattern: Delegates to pluggable extraction strategies
    - Template Method: Defines common workflow for multi-strategy extraction
    """

    def __init__(self, strategies: Optional[List[ConceptExtractionStrategy]] = None):
        """Initialize with extraction strategies."""
        if strategies is None:
            # Default strategy configuration
            self.strategies = [
                RuleBasedExtractionStrategy(),
                StatisticalExtractionStrategy(),
                EmbeddingBasedExtractionStrategy(),
            ]
        else:
            self.strategies = strategies

    def extract_concepts_comprehensive(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """
        Extract concepts using all configured strategies.

        Educational Note:
        Orchestrates multiple extraction strategies and consolidates
        their results, demonstrating how to combine diverse approaches
        for comprehensive concept coverage.
        """
        all_concepts = []
        strategy_results = {}

        # Execute each strategy
        for i, strategy in enumerate(self.strategies):
            try:
                strategy_name = strategy.__class__.__name__.replace(
                    "ExtractionStrategy", ""
                ).lower()
                result = strategy.extract_concepts(text, config)

                # Apply strategy weights if configured
                if strategy_name in config.strategy_weights:
                    weight = config.strategy_weights[strategy_name]
                    weighted_concepts = self._apply_strategy_weight(
                        result.concepts, weight
                    )
                    all_concepts.extend(weighted_concepts)
                else:
                    all_concepts.extend(result.concepts)

                strategy_results[strategy_name] = {
                    "concept_count": len(result.concepts),
                    "metadata": result.metadata,
                }

            except Exception as e:
                logging.warning(f"Strategy {strategy.__class__.__name__} failed: {e}")
                continue

        # Consolidate results
        if config.consolidate_results:
            consolidated_concepts = self._consolidate_multi_strategy_results(
                all_concepts, config
            )
        else:
            consolidated_concepts = all_concepts

        # Create final result metadata
        final_metadata = {
            "extraction_method": "multi_strategy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "strategies_used": list(strategy_results.keys()),
            "strategy_results": strategy_results,
            "total_raw_concepts": len(all_concepts),
            "total_consolidated_concepts": len(consolidated_concepts),
        }

        if "strategy_weights" in config.__dict__ and config.strategy_weights:
            final_metadata["weighted_combination"] = True
            final_metadata["weights_applied"] = config.strategy_weights

        return ExtractionResult(concepts=consolidated_concepts, metadata=final_metadata)

    def _apply_strategy_weight(
        self, concepts: List[Concept], weight: float
    ) -> List[Concept]:
        """Apply weight to concept relevance scores."""
        weighted_concepts = []
        for concept in concepts:
            weighted_concept = Concept(
                text=concept.text,
                frequency=concept.frequency,
                relevance_score=concept.relevance_score * weight,
                extraction_method=concept.extraction_method,
            )
            weighted_concepts.append(weighted_concept)
        return weighted_concepts

    def _consolidate_multi_strategy_results(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Consolidate concepts from multiple strategies."""
        # Group concepts by text similarity
        concept_groups = defaultdict(list)

        for concept in concepts:
            # Simple grouping by exact text match for now
            # In full implementation, would use semantic similarity
            group_key = concept.text.lower().strip()
            concept_groups[group_key].append(concept)

        consolidated = []
        for text, group in concept_groups.items():
            if len(group) == 1:
                consolidated.append(group[0])
            else:
                # Merge concepts from multiple strategies
                merged_concept = self._merge_multi_strategy_concepts(group)
                consolidated.append(merged_concept)

        # Sort by combined relevance and frequency
        consolidated.sort(key=lambda c: (c.relevance_score * c.frequency), reverse=True)

        # Apply final filtering
        return consolidated[
            : config.max_concepts_per_strategy * 2
        ]  # Allow more for multi-strategy

    def _merge_multi_strategy_concepts(self, concepts: List[Concept]) -> Concept:
        """Merge concepts from multiple strategies."""
        # Use the highest relevance concept as base
        primary = max(concepts, key=lambda c: c.relevance_score)

        # Combine evidence from all strategies
        total_frequency = sum(c.frequency for c in concepts)
        weighted_relevance = (
            sum(c.relevance_score * c.frequency for c in concepts) / total_frequency
            if total_frequency > 0
            else primary.relevance_score
        )

        return Concept(
            text=primary.text,
            frequency=total_frequency,
            relevance_score=weighted_relevance,
            extraction_method="semantic_embedding",
        )

