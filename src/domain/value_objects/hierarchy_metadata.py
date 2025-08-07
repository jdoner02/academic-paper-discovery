"""
HierarchyMetadata - Value object providing comprehensive metrics for concept hierarchies.

This value object encapsulates quality metrics, structural information, and
performance data for concept hierarchies in research applications.

Educational Notes - Metadata Pattern (Domain-Driven Design):
- Separates metrics computation from core domain logic (Single Responsibility)
- Encapsulates complex quality assessment without coupling to hierarchy structure
- Provides standardized metrics for comparing different hierarchy versions
- Enables quality tracking and improvement over time
- Demonstrates how metadata objects support analysis without polluting core entities

Educational Notes - SOLID Principles Demonstrated:
- Single Responsibility: Only responsible for hierarchy quality metrics
- Open/Closed: New metrics can be added without modifying existing ones
- Liskov Substitution: All metadata instances provide consistent interface
- Interface Segregation: Focused interface for quality assessment operations
- Dependency Inversion: Uses abstract validation patterns, not concrete implementations

Educational Notes - Research Quality Assessment:
- Hierarchy depth indicates conceptual organization quality
- Node distribution metrics reveal structural balance
- Confidence statistics show extraction quality across all concepts
- Coverage metrics ensure comprehensive concept identification
- Quality scores enable objective comparison of different approaches

Educational Notes - Design Patterns Applied:
- Value Object Pattern: Immutable metrics with equality by value
- Strategy Pattern: Different quality assessment strategies can be plugged in
- Template Method Pattern: Consistent validation approach across domain
- Factory Method Pattern: Multiple ways to create metadata for different scenarios

Design Decisions:
- Immutable state prevents metric tampering after computation
- Common validation utilities ensure consistency across domain objects
- Rich statistical methods provide objective quality assessment
- Comparison methods enable ranking of different approaches
- Clear separation between calculation and validation concerns

Use Cases:
- Research Quality Control: Assess hierarchy quality before publication
- Algorithm Comparison: Compare extraction strategies objectively
- Progress Tracking: Monitor improvement over multiple extraction runs
- Academic Standards: Provide transparent quality metrics for peer review
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List
import math

from src.domain.common.validation import (
    validate_positive_count,
    validate_probability_score,
    validate_required_field,
    DomainValidationError,
)


@dataclass(frozen=True)
class HierarchyMetadata:
    """
    Comprehensive metadata about a concept hierarchy's structure and quality.

    This value object provides standardized metrics for assessing the quality,
    structure, and performance characteristics of concept hierarchies.

    Attributes:
        total_concepts: Total number of concepts in the hierarchy
        hierarchy_depth: Maximum depth of the concept hierarchy
        average_confidence: Mean confidence score across all concepts
        extraction_timestamp: When the hierarchy was created
        root_concepts_count: Number of root-level concepts
        leaf_concepts_count: Number of leaf concepts (no children)
        quality_score: Overall quality assessment (0.0 to 1.0)
    """

    total_concepts: int
    hierarchy_depth: int
    average_confidence: float
    extraction_timestamp: datetime
    root_concepts_count: int
    leaf_concepts_count: int
    quality_score: float

    def __post_init__(self):
        """
        Validate hierarchy metadata for research quality standards.

        Educational Notes - Comprehensive Validation Strategy:
        - Uses common validation utilities for consistency
        - Enforces business rules about hierarchy structure
        - Prevents invalid metrics that could mislead research
        - Demonstrates composition of simple validators for complex validation

        Educational Notes - Data Integrity for Research:
        - Ensures all counts are positive and logical
        - Validates confidence and quality scores are probabilities
        - Prevents inconsistent structural metrics
        - Maintains research data integrity standards required for academic work

        Educational Notes - Defensive Programming:
        - Validation occurs at object creation to fail fast
        - Clear error messages help identify specific validation failures
        - Contextual error wrapping provides debugging information
        - Prevents invalid objects from being used in calculations
        """
        try:
            # Validate structural metrics using common utilities
            validate_positive_count(
                self.total_concepts,
                "Total concepts",
                allow_zero=True,  # Allow zero for empty hierarchies
            )
            validate_positive_count(
                self.hierarchy_depth, "Hierarchy depth", allow_zero=False
            )
            validate_positive_count(
                self.root_concepts_count,
                "Root concepts count",
                allow_zero=True,  # Allow zero for empty hierarchies
            )
            validate_positive_count(
                self.leaf_concepts_count, "Leaf concepts count", allow_zero=True
            )

            # Validate probability-based metrics
            validate_probability_score(self.average_confidence, "Average confidence")
            validate_probability_score(self.quality_score, "Quality score")

            # Validate required timestamp
            validate_required_field(self.extraction_timestamp, "Extraction timestamp")

            # Validate structural consistency - business rule validation
            if (
                self.root_concepts_count + self.leaf_concepts_count
                > self.total_concepts
            ):
                raise DomainValidationError(
                    "Root and leaf concept counts cannot exceed total concepts"
                )

        except DomainValidationError as e:
            # Wrap validation errors with context for better debugging
            raise DomainValidationError(f"Invalid hierarchy metadata: {e}")

    @classmethod
    def create_for_flat_hierarchy(
        cls,
        total_concepts: int,
        average_confidence: float,
        extraction_timestamp: Optional[datetime] = None,
    ) -> "HierarchyMetadata":
        """
        Factory method for creating metadata for flat (single-level) hierarchies.

        Educational Notes - Factory Method Pattern:
        - Provides specialized constructors for common hierarchy types
        - Encapsulates business logic about flat hierarchy characteristics
        - Makes creation intent clear through descriptive method names
        - Demonstrates how factory methods can encode domain knowledge

        Args:
            total_concepts: Number of concepts in the flat hierarchy
            average_confidence: Mean confidence across all concepts
            extraction_timestamp: When extraction occurred (defaults to now)

        Returns:
            HierarchyMetadata configured for a flat hierarchy structure
        """
        timestamp = extraction_timestamp or datetime.now()

        # Flat hierarchy characteristics: depth=1, all concepts are both root and leaf
        return cls(
            total_concepts=total_concepts,
            hierarchy_depth=1,
            average_confidence=average_confidence,
            extraction_timestamp=timestamp,
            root_concepts_count=total_concepts,  # All concepts are roots in flat hierarchy
            leaf_concepts_count=total_concepts,  # All concepts are leaves in flat hierarchy
            quality_score=average_confidence
            * 0.7,  # Penalty for lack of hierarchy structure
        )

    @classmethod
    def create_for_deep_hierarchy(
        cls,
        total_concepts: int,
        hierarchy_depth: int,
        average_confidence: float,
        root_count: int,
        leaf_count: int,
        extraction_timestamp: Optional[datetime] = None,
    ) -> "HierarchyMetadata":
        """
        Factory method for creating metadata for deep hierarchical structures.

        Educational Notes - Complex Object Creation:
        - Handles the complexity of deep hierarchy metrics
        - Encapsulates quality score calculation for hierarchical structures
        - Provides validation specific to deep hierarchy constraints
        - Demonstrates domain knowledge encoding in factory methods

        Args:
            total_concepts: Total number of concepts across all levels
            hierarchy_depth: Maximum depth of the hierarchy
            average_confidence: Mean confidence across all concepts
            root_count: Number of root-level concepts
            leaf_count: Number of leaf concepts
            extraction_timestamp: When extraction occurred (defaults to now)

        Returns:
            HierarchyMetadata configured for a deep hierarchical structure
        """
        timestamp = extraction_timestamp or datetime.now()

        # Calculate quality bonus for hierarchical organization
        depth_bonus = min(0.2, hierarchy_depth * 0.05)  # Bonus for deeper organization
        balance_penalty = (
            abs(root_count - leaf_count) / total_concepts * 0.1
        )  # Penalty for imbalance

        quality_score = min(1.0, average_confidence + depth_bonus - balance_penalty)

        return cls(
            total_concepts=total_concepts,
            hierarchy_depth=hierarchy_depth,
            average_confidence=average_confidence,
            extraction_timestamp=timestamp,
            root_concepts_count=root_count,
            leaf_concepts_count=leaf_count,
            quality_score=quality_score,
        )

    def calculate_hierarchy_density(self) -> float:
        """
        Calculate the density of concepts per hierarchy level.

        Returns:
            Average number of concepts per hierarchy level

        Educational Notes - Structural Analysis:
        - Higher density may indicate better concept organization
        - Very low density might suggest over-deep hierarchies
        - Helps assess whether hierarchy structure is appropriate
        """
        return self.total_concepts / self.hierarchy_depth

    def calculate_leaf_ratio(self) -> float:
        """
        Calculate the ratio of leaf concepts to total concepts.

        Returns:
            Proportion of concepts that are leaves (0.0 to 1.0)

        Educational Notes - Hierarchy Balance:
        - High leaf ratio may indicate good conceptual detail
        - Very low leaf ratio might suggest incomplete extraction
        - Balanced hierarchies typically have moderate leaf ratios
        """
        return self.leaf_concepts_count / self.total_concepts

    def calculate_root_ratio(self) -> float:
        """
        Calculate the ratio of root concepts to total concepts.

        Returns:
            Proportion of concepts that are roots (0.0 to 1.0)

        Educational Notes - Organization Quality:
        - Low root ratio suggests good conceptual organization
        - High root ratio may indicate poor hierarchy structure
        - Well-organized hierarchies have few, meaningful root concepts
        """
        return self.root_concepts_count / self.total_concepts

    def is_well_balanced(
        self, min_depth: int = 3, max_root_ratio: float = 0.15
    ) -> bool:
        """
        Assess whether the hierarchy is well-balanced structurally.

        Args:
            min_depth: Minimum acceptable hierarchy depth
            max_root_ratio: Maximum acceptable ratio of root concepts

        Returns:
            True if hierarchy meets balance criteria

        Educational Notes - Quality Assessment:
        - Well-balanced hierarchies have sufficient depth for organization
        - Too many root concepts suggest poor conceptual grouping
        - Quality thresholds based on research best practices
        """
        depth_ok = self.hierarchy_depth >= min_depth
        root_ratio_ok = self.calculate_root_ratio() <= max_root_ratio
        confidence_ok = (
            self.average_confidence >= 0.7
        )  # Reasonable confidence threshold

        return depth_ok and root_ratio_ok and confidence_ok

    def is_higher_quality_than(self, other: "HierarchyMetadata") -> bool:
        """
        Compare quality with another hierarchy metadata.

        Args:
            other: Another hierarchy metadata to compare against

        Returns:
            True if this hierarchy has higher overall quality

        Educational Notes - Quality Comparison:
        - Enables objective comparison of different extraction approaches
        - Considers multiple quality dimensions (confidence, structure, completeness)
        - Supports algorithm evaluation and improvement
        """
        return self.quality_score > other.quality_score

    def calculate_improvement_over(
        self, baseline: "HierarchyMetadata"
    ) -> Dict[str, float]:
        """
        Calculate improvement metrics compared to a baseline hierarchy.

        Args:
            baseline: Baseline hierarchy metadata for comparison

        Returns:
            Dictionary containing various improvement metrics

        Educational Notes - Progress Tracking:
        - Enables quantitative assessment of algorithm improvements
        - Supports iterative development and optimization
        - Provides clear metrics for research progress reporting
        """
        concept_growth = self.total_concepts / baseline.total_concepts
        quality_improvement = self.quality_score - baseline.quality_score
        confidence_improvement = self.average_confidence - baseline.average_confidence

        # Calculate structural improvements
        depth_improvement = self.hierarchy_depth - baseline.hierarchy_depth
        balance_improvement = (
            baseline.calculate_root_ratio() - self.calculate_root_ratio()
        )  # Lower root ratio is better

        return {
            "concept_growth": concept_growth,
            "quality_improvement": quality_improvement,
            "confidence_improvement": confidence_improvement,
            "depth_improvement": depth_improvement,
            "balance_improvement": balance_improvement,
            "overall_improvement": (quality_improvement + confidence_improvement) / 2,
        }

    def generate_research_summary(self) -> str:
        """
        Generate a comprehensive research summary of hierarchy metrics.

        Returns:
            Multi-line string summarizing hierarchy characteristics

        Educational Notes - Research Communication:
        - Provides clear, human-readable summary for research reports
        - Includes key metrics needed for academic evaluation
        - Formatted for inclusion in research papers or documentation
        """
        leaf_ratio = self.calculate_leaf_ratio()
        root_ratio = self.calculate_root_ratio()
        density = self.calculate_hierarchy_density()

        summary_lines = [
            "Concept Hierarchy Analysis Summary",
            "=====================================",
            f"Total Concepts: {self.total_concepts}",
            f"Hierarchy Depth: {self.hierarchy_depth} levels deep",
            f"Average Extraction Confidence: {self.average_confidence:.1%}",
            f"Overall Quality Score: {self.quality_score:.1%}",
            "",
            "Structural Metrics:",
            f"  Root Concepts: {self.root_concepts_count} ({root_ratio:.1%} of total)",
            f"  Leaf Concepts: {self.leaf_concepts_count} ({leaf_ratio:.1%} of total)",
            f"  Hierarchy Density: {density:.1f} concepts per level",
            "",
            f"Quality Assessment: {'Well-balanced' if self.is_well_balanced() else 'Needs improvement'}",
            f"Extraction Date: {self.extraction_timestamp.strftime('%Y-%m-%d %H:%M UTC')}",
        ]

        return "\n".join(summary_lines)

    def get_quality_breakdown(self) -> Dict[str, Any]:
        """
        Get detailed breakdown of quality factors and their contributions.

        Returns:
            Dictionary containing detailed quality analysis

        Educational Notes - Quality Transparency:
        - Breaks down overall quality into component factors
        - Enables understanding of quality strengths and weaknesses
        - Supports targeted improvement of specific quality aspects
        """
        structural_quality = (
            1.0 - self.calculate_root_ratio()
        )  # Lower root ratio is better
        confidence_quality = self.average_confidence
        depth_quality = min(
            1.0, self.hierarchy_depth / 5.0
        )  # Normalize depth (5+ levels = full score)
        balance_quality = 1.0 - abs(
            0.6 - self.calculate_leaf_ratio()
        )  # Target ~60% leaves

        return {
            "overall_quality": self.quality_score,
            "components": {
                "structural_quality": structural_quality,
                "confidence_quality": confidence_quality,
                "depth_quality": depth_quality,
                "balance_quality": balance_quality,
            },
            "strengths": self._identify_quality_strengths(),
            "improvement_areas": self._identify_improvement_areas(),
        }

    def _identify_quality_strengths(self) -> List[str]:
        """Identify the strongest quality aspects of this hierarchy."""
        strengths = []

        if self.average_confidence >= 0.9:
            strengths.append("Excellent extraction confidence")
        elif self.average_confidence >= 0.8:
            strengths.append("High extraction confidence")

        if self.hierarchy_depth >= 5:
            strengths.append("Good conceptual depth")

        if self.calculate_root_ratio() <= 0.1:
            strengths.append("Well-organized root structure")

        if 0.4 <= self.calculate_leaf_ratio() <= 0.7:
            strengths.append("Balanced leaf distribution")

        return strengths

    def _identify_improvement_areas(self) -> List[str]:
        """Identify areas where hierarchy quality could be improved."""
        improvements = []

        if self.average_confidence < 0.7:
            improvements.append("Increase extraction confidence")

        if self.hierarchy_depth < 3:
            improvements.append("Develop deeper conceptual organization")

        if self.calculate_root_ratio() > 0.2:
            improvements.append("Reduce number of root concepts")

        if self.calculate_leaf_ratio() < 0.3:
            improvements.append("Add more specific leaf concepts")
        elif self.calculate_leaf_ratio() > 0.8:
            improvements.append("Add more intermediate organizing concepts")

        return improvements
