"""
Unit tests for ExtractionProvenance value object.

This test suite validates the ExtractionProvenance value object, which tracks
the complete audit trail of concept extraction processes for research reproducibility.

Educational Notes - Provenance Pattern:
- Captures complete audit trail for research reproducibility requirements
- Enables comparison of different extraction strategies and their effectiveness
- Provides transparency about extraction process for academic peer review
- Supports debugging and improvement of extraction algorithms

Educational Notes - Research Reproducibility:
- Algorithm version tracking enables exact reproduction of results
- Parameter logging allows researchers to understand extraction configuration
- Performance metrics help evaluate and improve extraction strategies
- Error tracking identifies edge cases and algorithm limitations

Value Object Design Benefits:
- Immutable provenance prevents tampering with audit trail
- Complete encapsulation ensures all necessary tracking data is captured
- Value semantics enable comparison of extraction runs
- Rich interface provides multiple views of provenance data
"""

import pytest
from datetime import datetime, timezone
from typing import Dict, Any

from src.domain.value_objects.extraction_provenance import ExtractionProvenance


class TestExtractionProvenanceCreation:
    """Test extraction provenance creation and validation."""

    def test_create_valid_extraction_provenance(self):
        """Test creation of valid extraction provenance."""
        # This test should fail initially (RED phase)
        parameters = {
            "similarity_threshold": 0.8,
            "max_hierarchy_depth": 5,
            "confidence_threshold": 0.7,
            "extraction_strategies": ["rule_based", "statistical", "embedding_based"],
        }

        performance_metrics = {
            "extraction_time_seconds": 45.7,
            "concepts_extracted": 156,
            "average_confidence": 0.84,
            "memory_usage_mb": 128.5,
        }

        provenance = ExtractionProvenance(
            algorithm_name="Multi-Strategy Concept Extractor",
            algorithm_version="v2.1.0",
            extraction_timestamp=datetime(2024, 8, 6, 15, 0, 0, tzinfo=timezone.utc),
            parameters=parameters,
            performance_metrics=performance_metrics,
            paper_count=25,
            success_rate=0.92,
            error_log=[
                "Warning: Low confidence concept on page 5",
                "Info: Hierarchy depth exceeded recommendation",
            ],
        )

        assert provenance.algorithm_name == "Multi-Strategy Concept Extractor"
        assert provenance.algorithm_version == "v2.1.0"
        assert provenance.paper_count == 25
        assert abs(provenance.success_rate - 0.92) < 0.001
        assert len(provenance.error_log) == 2

    def test_reject_empty_algorithm_name(self):
        """Test that provenance rejects empty algorithm names."""
        # This test should fail initially (RED phase)
        with pytest.raises(ValueError, match="Algorithm name cannot be empty"):
            ExtractionProvenance(
                algorithm_name="   ",  # Whitespace only
                algorithm_version="v1.0.0",
                extraction_timestamp=datetime.now(timezone.utc),
                parameters={},
                performance_metrics={},
                paper_count=10,
                success_rate=0.8,
                error_log=[],
            )

    def test_reject_invalid_success_rate(self):
        """Test that provenance rejects invalid success rates."""
        # This test should fail initially (RED phase)
        with pytest.raises(
            ValueError, match="Success rate must be between 0.0 and 1.0"
        ):
            ExtractionProvenance(
                algorithm_name="Test Algorithm",
                algorithm_version="v1.0.0",
                extraction_timestamp=datetime.now(timezone.utc),
                parameters={},
                performance_metrics={},
                paper_count=10,
                success_rate=1.5,  # Invalid - greater than 1.0
                error_log=[],
            )

    def test_reject_negative_paper_count(self):
        """Test that provenance rejects negative paper counts."""
        # This test should fail initially (RED phase)
        with pytest.raises(ValueError, match="Paper count must be non-negative"):
            ExtractionProvenance(
                algorithm_name="Test Algorithm",
                algorithm_version="v1.0.0",
                extraction_timestamp=datetime.now(timezone.utc),
                parameters={},
                performance_metrics={},
                paper_count=-5,  # Invalid - negative count
                success_rate=0.8,
                error_log=[],
            )


class TestExtractionProvenanceValueObjectBehavior:
    """Test value object characteristics of ExtractionProvenance."""

    def test_extraction_provenance_equality(self):
        """Test that provenance with identical data are equal."""
        # This test should fail initially (RED phase)
        timestamp = datetime(2024, 8, 6, 10, 30, 0, tzinfo=timezone.utc)
        parameters = {"threshold": 0.8, "max_depth": 4}
        metrics = {"time": 30.5, "concepts": 100}
        errors = ["Warning: Low confidence", "Info: Processing complete"]

        provenance1 = ExtractionProvenance(
            algorithm_name="Research Extractor",
            algorithm_version="v1.5.2",
            extraction_timestamp=timestamp,
            parameters=parameters,
            performance_metrics=metrics,
            paper_count=20,
            success_rate=0.88,
            error_log=errors,
        )

        provenance2 = ExtractionProvenance(
            algorithm_name="Research Extractor",
            algorithm_version="v1.5.2",
            extraction_timestamp=timestamp,
            parameters=parameters,
            performance_metrics=metrics,
            paper_count=20,
            success_rate=0.88,
            error_log=errors,
        )

        assert provenance1 == provenance2
        assert hash(provenance1) == hash(provenance2)

    def test_extraction_provenance_inequality(self):
        """Test that provenance with different data are not equal."""
        # This test should fail initially (RED phase)
        timestamp = datetime(2024, 8, 6, 10, 30, 0, tzinfo=timezone.utc)

        provenance1 = ExtractionProvenance(
            algorithm_name="Research Extractor",
            algorithm_version="v1.5.2",
            extraction_timestamp=timestamp,
            parameters={"threshold": 0.8},
            performance_metrics={"time": 30.5},
            paper_count=20,
            success_rate=0.88,
            error_log=[],
        )

        provenance2 = ExtractionProvenance(
            algorithm_name="Research Extractor",
            algorithm_version="v1.5.3",  # Different version
            extraction_timestamp=timestamp,
            parameters={"threshold": 0.8},
            performance_metrics={"time": 30.5},
            paper_count=20,
            success_rate=0.88,
            error_log=[],
        )

        assert provenance1 != provenance2
        assert hash(provenance1) != hash(provenance2)

    def test_extraction_provenance_immutability(self):
        """Test that extraction provenance is immutable after creation."""
        # This test should fail initially (RED phase)
        provenance = ExtractionProvenance(
            algorithm_name="Test Algorithm",
            algorithm_version="v1.0.0",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"test": "value"},
            performance_metrics={"metric": 1.0},
            paper_count=10,
            success_rate=0.9,
            error_log=["test error"],
        )

        # Should not be able to modify attributes (frozen dataclass)
        with pytest.raises(AttributeError):
            provenance.algorithm_name = "Modified Algorithm"

        with pytest.raises(AttributeError):
            provenance.success_rate = 0.95


class TestExtractionProvenanceAuditCapabilities:
    """Test extraction provenance audit and tracking capabilities."""

    def test_provenance_algorithm_identification(self):
        """Test provenance provides clear algorithm identification."""
        # This test should fail initially (RED phase)
        provenance = ExtractionProvenance(
            algorithm_name="Advanced Multi-Strategy Extractor",
            algorithm_version="v3.2.1",
            extraction_timestamp=datetime(2024, 8, 6, 12, 0, tzinfo=timezone.utc),
            parameters={"strategy_weights": {"rule": 0.4, "stat": 0.3, "embed": 0.3}},
            performance_metrics={"total_time": 120.5, "concepts_found": 245},
            paper_count=50,
            success_rate=0.94,
            error_log=["Info: High-quality extraction completed"],
        )

        # Should provide clear algorithm identification
        algorithm_id = provenance.get_algorithm_identifier()
        assert "Advanced Multi-Strategy Extractor" in algorithm_id
        assert "v3.2.1" in algorithm_id

        # Should indicate exact reproduction requirements
        reproduction_info = provenance.get_reproduction_info()
        assert reproduction_info["algorithm"] == "Advanced Multi-Strategy Extractor"
        assert reproduction_info["version"] == "v3.2.1"
        assert "strategy_weights" in str(reproduction_info["parameters"])

    def test_provenance_performance_analysis(self):
        """Test provenance enables performance analysis and optimization."""
        # This test should fail initially (RED phase)
        fast_extraction = ExtractionProvenance(
            algorithm_name="Speed-Optimized Extractor",
            algorithm_version="v2.0.0",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"optimization": "speed", "cache_enabled": True},
            performance_metrics={"extraction_time": 25.3, "concepts_per_second": 8.5},
            paper_count=30,
            success_rate=0.86,
            error_log=[],
        )

        thorough_extraction = ExtractionProvenance(
            algorithm_name="Quality-Optimized Extractor",
            algorithm_version="v2.0.0",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"optimization": "quality", "deep_analysis": True},
            performance_metrics={"extraction_time": 95.7, "concepts_per_second": 2.8},
            paper_count=30,
            success_rate=0.97,
            error_log=["Info: Deep semantic analysis completed"],
        )

        # Should enable performance comparison
        comparison = ExtractionProvenance.compare_performance(
            fast_extraction, thorough_extraction
        )
        assert comparison["speed_advantage"] == "Speed-Optimized Extractor"
        assert comparison["quality_advantage"] == "Quality-Optimized Extractor"
        assert comparison["speed_factor"] > 3.0  # Fast extraction is >3x faster

    def test_provenance_error_analysis(self):
        """Test provenance enables error analysis and debugging."""
        # This test should fail initially (RED phase)
        problematic_extraction = ExtractionProvenance(
            algorithm_name="Experimental Extractor",
            algorithm_version="v0.9.1",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"experimental_features": True, "beta_algorithms": ["new_nlp"]},
            performance_metrics={"extraction_time": 75.2, "concepts_extracted": 89},
            paper_count=20,
            success_rate=0.65,  # Low success rate
            error_log=[
                "Error: NLP model failed on paper 5",
                "Warning: Low confidence concepts detected",
                "Error: Memory limit exceeded during processing",
                "Info: Fallback to basic extraction",
            ],
        )

        # Should categorize and analyze errors
        error_analysis = problematic_extraction.analyze_errors()
        assert error_analysis["error_count"] == 2
        assert error_analysis["warning_count"] == 1
        assert error_analysis["info_count"] == 1
        assert "NLP model" in str(error_analysis["error_patterns"])
        assert "Memory limit" in str(error_analysis["error_patterns"])


class TestExtractionProvenanceResearchApplications:
    """Test extraction provenance usage in research scenarios."""

    def test_provenance_research_reproducibility(self):
        """Test provenance enables complete research reproducibility."""
        # This test should fail initially (RED phase)
        original_research = ExtractionProvenance(
            algorithm_name="Research Paper Concept Extractor",
            algorithm_version="v1.8.3",
            extraction_timestamp=datetime(2024, 6, 15, 14, 30, tzinfo=timezone.utc),
            parameters={
                "confidence_threshold": 0.75,
                "hierarchy_depth": 4,
                "extraction_strategies": ["rule_based", "statistical"],
                "similarity_threshold": 0.82,
                "random_seed": 42,
            },
            performance_metrics={
                "total_extraction_time": 180.5,
                "concepts_extracted": 312,
                "average_confidence": 0.847,
                "papers_processed": 75,
            },
            paper_count=75,
            success_rate=0.93,
            error_log=["Info: Extraction completed successfully"],
        )

        # Should enable exact reproduction
        reproduction_guide = original_research.generate_reproduction_guide()
        assert "Research Paper Concept Extractor v1.8.3" in reproduction_guide
        assert "confidence_threshold: 0.75" in reproduction_guide
        assert "random_seed: 42" in reproduction_guide
        assert "Expected: 312 concepts" in reproduction_guide

        # Should verify reproduction success
        reproduction_metrics = {
            "concepts_extracted": 312,
            "average_confidence": 0.847,
            "papers_processed": 75,
        }

        is_successful_reproduction = original_research.verify_reproduction(
            reproduction_metrics
        )
        assert is_successful_reproduction is True

    def test_provenance_method_comparison(self):
        """Test provenance enables scientific comparison of extraction methods."""
        # This test should fail initially (RED phase)
        method_a = ExtractionProvenance(
            algorithm_name="Rule-Based Extractor",
            algorithm_version="v2.1.0",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"rule_confidence": 0.9, "strict_matching": True},
            performance_metrics={"precision": 0.92, "recall": 0.67, "f1_score": 0.77},
            paper_count=100,
            success_rate=0.89,
            error_log=["Info: High precision, moderate recall"],
        )

        method_b = ExtractionProvenance(
            algorithm_name="Embedding-Based Extractor",
            algorithm_version="v1.5.2",
            extraction_timestamp=datetime.now(timezone.utc),
            parameters={"embedding_model": "sentence-transformers", "similarity": 0.75},
            performance_metrics={"precision": 0.78, "recall": 0.91, "f1_score": 0.84},
            paper_count=100,
            success_rate=0.94,
            error_log=["Info: High recall, good overall performance"],
        )

        # Should enable scientific method comparison
        comparison = ExtractionProvenance.generate_method_comparison(method_a, method_b)
        assert comparison["better_precision"] == "Rule-Based Extractor"
        assert comparison["better_recall"] == "Embedding-Based Extractor"
        assert comparison["better_f1"] == "Embedding-Based Extractor"
        assert comparison["statistical_significance"] is not None
