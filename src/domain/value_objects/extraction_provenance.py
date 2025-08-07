"""
ExtractionProvenance - Value object tracking complete audit trail for concept extraction.

This value object captures comprehensive provenance information for research
reproducibility, algorithm comparison, and scientific transparency.

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

Design Decisions:
- Immutable provenance prevents tampering with audit trail
- Complete parameter capture ensures reproducibility
- Rich comparison methods enable scientific evaluation
- Error analysis supports algorithm improvement

Use Cases:
- Academic Reproducibility: Enable exact reproduction of research results
- Algorithm Evaluation: Compare extraction methods scientifically
- Quality Control: Track and improve extraction performance
- Peer Review: Provide transparent methodology for academic scrutiny
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
import json
from copy import deepcopy


@dataclass(frozen=True)
class ExtractionProvenance:
    """
    Complete provenance tracking for concept extraction processes.

    This value object captures all information needed to reproduce,
    evaluate, and compare concept extraction runs.

    Attributes:
        algorithm_name: Name of the extraction algorithm used
        algorithm_version: Version string for exact algorithm identification
        extraction_timestamp: When the extraction was performed
        parameters: Dictionary of all algorithm parameters used
        performance_metrics: Dictionary of performance measurements
        paper_count: Number of papers processed in this extraction
        success_rate: Proportion of successful extractions (0.0 to 1.0)
        error_log: List of errors and warnings encountered
    """

    algorithm_name: str
    algorithm_version: str
    extraction_timestamp: datetime
    parameters: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    paper_count: int
    success_rate: float
    error_log: List[str] = field(default_factory=list)

    def __post_init__(self):
        """
        Validate extraction provenance for research standards.

        Educational Notes - Audit Integrity:
        - Ensures algorithm identification is meaningful and traceable
        - Validates success rates are valid probabilities
        - Prevents negative counts that would indicate data corruption
        - Maintains immutable copies to prevent audit trail tampering
        """
        # Validate algorithm identification
        if not self.algorithm_name or not self.algorithm_name.strip():
            raise ValueError("Algorithm name cannot be empty")

        if not self.algorithm_version or not self.algorithm_version.strip():
            raise ValueError("Algorithm version cannot be empty")

        # Validate success rate
        if not (0.0 <= self.success_rate <= 1.0):
            raise ValueError("Success rate must be between 0.0 and 1.0")

        # Validate paper count
        if self.paper_count < 0:
            raise ValueError("Paper count must be non-negative")

        # Create immutable copies of mutable data to maintain audit integrity
        object.__setattr__(self, "parameters", deepcopy(dict(self.parameters)))
        object.__setattr__(
            self, "performance_metrics", deepcopy(dict(self.performance_metrics))
        )
        object.__setattr__(self, "error_log", list(self.error_log))

    def get_algorithm_identifier(self) -> str:
        """
        Get a unique identifier for the algorithm and version.

        Returns:
            String uniquely identifying the algorithm and version

        Educational Notes - Reproducibility:
        - Provides exact algorithm identification for reproduction
        - Enables tracking of algorithm evolution over time
        - Critical for scientific reproducibility requirements
        """
        return f"{self.algorithm_name} v{self.algorithm_version}"

    def get_reproduction_info(self) -> Dict[str, Any]:
        """
        Get all information needed to reproduce this extraction.

        Returns:
            Dictionary containing complete reproduction information

        Educational Notes - Scientific Reproducibility:
        - Provides complete parameter set for exact reproduction
        - Includes algorithm version for precise method identification
        - Enables other researchers to replicate results exactly
        """
        return {
            "algorithm": self.algorithm_name,
            "version": self.algorithm_version,
            "parameters": deepcopy(self.parameters),
            "timestamp": self.extraction_timestamp.isoformat(),
            "paper_count": self.paper_count,
        }

    def analyze_errors(self) -> Dict[str, Any]:
        """
        Analyze error patterns and categorize issues.

        Returns:
            Dictionary containing error analysis and categorization

        Educational Notes - Quality Improvement:
        - Categorizes errors to identify systematic issues
        - Enables targeted algorithm improvements
        - Supports debugging and optimization efforts
        """
        error_count = 0
        warning_count = 0
        info_count = 0
        error_patterns = []

        for log_entry in self.error_log:
            if log_entry.startswith("Error:"):
                error_count += 1
                error_patterns.append(log_entry[7:].strip())  # Remove "Error: " prefix
            elif log_entry.startswith("Warning:"):
                warning_count += 1
            elif log_entry.startswith("Info:"):
                info_count += 1

        return {
            "total_entries": len(self.error_log),
            "error_count": error_count,
            "warning_count": warning_count,
            "info_count": info_count,
            "error_patterns": error_patterns,
            "error_rate": error_count / max(1, len(self.error_log)),
        }

    def generate_reproduction_guide(self) -> str:
        """
        Generate a complete guide for reproducing this extraction.

        Returns:
            Multi-line string with step-by-step reproduction instructions

        Educational Notes - Academic Standards:
        - Provides clear instructions for research reproduction
        - Includes all necessary parameters and settings
        - Formatted for inclusion in research methodology sections
        """
        params_json = json.dumps(self.parameters, indent=2, default=str)
        metrics_json = json.dumps(self.performance_metrics, indent=2, default=str)

        guide_lines = [
            "Reproduction Guide",
            "==================",
            f"Algorithm: {self.algorithm_name} v{self.algorithm_version}",
            f"Extraction Date: {self.extraction_timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Papers Processed: {self.paper_count}",
            "",
            "Required Parameters:",
            params_json,
            "",
            "Expected Performance Metrics:",
            metrics_json,
            "",
            f"Expected Success Rate: {self.success_rate:.1%}",
            "",
            "Notes:",
            f"- Ensure exact algorithm version {self.algorithm_version} is used",
            "- All parameters must match exactly for reproduction",
            "- Random seed should be set if specified in parameters",
            "- Verify paper set matches original extraction corpus",
        ]

        return "\n".join(guide_lines)

    def verify_reproduction(
        self, reproduction_metrics: Dict[str, Any], tolerance: float = 0.05
    ) -> bool:
        """
        Verify if a reproduction attempt matches original results.

        Args:
            reproduction_metrics: Performance metrics from reproduction attempt
            tolerance: Acceptable relative difference for numeric metrics

        Returns:
            True if reproduction is within acceptable tolerance

        Educational Notes - Verification:
        - Enables validation of reproduction attempts
        - Accounts for minor variations due to system differences
        - Provides objective assessment of reproduction success
        """
        for key, original_value in self.performance_metrics.items():
            if key not in reproduction_metrics:
                return False

            repro_value = reproduction_metrics[key]

            # Handle numeric comparisons with tolerance
            if isinstance(original_value, (int, float)) and isinstance(
                repro_value, (int, float)
            ):
                if original_value == 0:
                    if abs(repro_value) > tolerance:
                        return False
                else:
                    relative_diff = abs(repro_value - original_value) / abs(
                        original_value
                    )
                    if relative_diff > tolerance:
                        return False
            else:
                # Exact match required for non-numeric values
                if original_value != repro_value:
                    return False

        return True

    @staticmethod
    def compare_performance(
        provenance1: "ExtractionProvenance", provenance2: "ExtractionProvenance"
    ) -> Dict[str, Any]:
        """
        Compare performance between two extraction runs.

        Args:
            provenance1: First extraction provenance
            provenance2: Second extraction provenance

        Returns:
            Dictionary containing detailed performance comparison

        Educational Notes - Scientific Comparison:
        - Enables objective comparison of different algorithms
        - Identifies strengths and weaknesses of each approach
        - Supports evidence-based algorithm selection
        """
        comparison = {
            "algorithms": {
                "first": provenance1.get_algorithm_identifier(),
                "second": provenance2.get_algorithm_identifier(),
            },
            "success_rates": {
                "first": provenance1.success_rate,
                "second": provenance2.success_rate,
                "difference": provenance2.success_rate - provenance1.success_rate,
            },
            "paper_processing": {
                "first": provenance1.paper_count,
                "second": provenance2.paper_count,
            },
        }

        # Compare specific performance metrics if available
        common_metrics = set(provenance1.performance_metrics.keys()) & set(
            provenance2.performance_metrics.keys()
        )

        for metric in common_metrics:
            val1 = provenance1.performance_metrics[metric]
            val2 = provenance2.performance_metrics[metric]

            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                comparison[f"{metric}_comparison"] = {
                    "first": val1,
                    "second": val2,
                    "difference": val2 - val1,
                    "relative_change": (
                        ((val2 - val1) / val1 * 100) if val1 != 0 else float("inf")
                    ),
                }

        # Determine advantages
        if "extraction_time" in common_metrics:
            time1 = provenance1.performance_metrics["extraction_time"]
            time2 = provenance2.performance_metrics["extraction_time"]
            comparison["speed_advantage"] = (
                provenance1.get_algorithm_identifier()
                if time1 < time2
                else provenance2.get_algorithm_identifier()
            )
            comparison["speed_factor"] = max(time1, time2) / min(time1, time2)

        comparison["quality_advantage"] = (
            provenance1.get_algorithm_identifier()
            if provenance1.success_rate > provenance2.success_rate
            else provenance2.get_algorithm_identifier()
        )

        return comparison

    @staticmethod
    def generate_method_comparison(
        provenance1: "ExtractionProvenance", provenance2: "ExtractionProvenance"
    ) -> Dict[str, Any]:
        """
        Generate a scientific comparison suitable for research publication.

        Args:
            provenance1: First extraction method provenance
            provenance2: Second extraction method provenance

        Returns:
            Dictionary containing publication-ready comparison

        Educational Notes - Academic Publication:
        - Provides standardized comparison format for research papers
        - Includes statistical significance assessment where applicable
        - Follows academic standards for method comparison reporting
        """
        performance_comparison = ExtractionProvenance.compare_performance(
            provenance1, provenance2
        )

        # Extract key performance indicators
        method1_name = provenance1.algorithm_name
        method2_name = provenance2.algorithm_name

        comparison = {
            "methods_compared": [method1_name, method2_name],
            "performance_summary": performance_comparison,
            "methodology_differences": {
                "parameters_method1": provenance1.parameters,
                "parameters_method2": provenance2.parameters,
            },
        }

        # Determine performance advantages
        common_metrics = set(provenance1.performance_metrics.keys()) & set(
            provenance2.performance_metrics.keys()
        )

        if "precision" in common_metrics and "recall" in common_metrics:
            precision1 = provenance1.performance_metrics["precision"]
            precision2 = provenance2.performance_metrics["precision"]
            recall1 = provenance1.performance_metrics["recall"]
            recall2 = provenance2.performance_metrics["recall"]

            comparison["better_precision"] = (
                method1_name if precision1 > precision2 else method2_name
            )
            comparison["better_recall"] = (
                method1_name if recall1 > recall2 else method2_name
            )

            if "f1_score" in common_metrics:
                f1_1 = provenance1.performance_metrics["f1_score"]
                f1_2 = provenance2.performance_metrics["f1_score"]
                comparison["better_f1"] = method1_name if f1_1 > f1_2 else method2_name

        # Statistical significance placeholder (would require actual statistical testing)
        comparison["statistical_significance"] = (
            "Statistical testing required for significance assessment"
        )

        return comparison
