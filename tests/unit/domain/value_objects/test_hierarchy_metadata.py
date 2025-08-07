"""
Unit tests for HierarchyMetadata value object.

This test suite validates the HierarchyMetadata value object, which provides
comprehensive metrics and quality assessment for concept hierarchies.

Educational Notes - Metadata Pattern:
- Encapsulates computed metrics about complex domain objects
- Provides quality assessment without coupling to computation logic
- Enables comparison and ranking of different hierarchy versions
- Separates metrics from core domain logic (Single Responsibility)

Educational Notes - Research Quality Metrics:
- Hierarchy depth indicates conceptual complexity and organization quality
- Node count tracks scale and comprehensiveness of concept coverage
- Average confidence reflects overall extraction quality across all concepts
- Coverage metrics ensure no important concepts are missed

Value Object Design Benefits:
- Immutable metrics prevent accidental modification after computation
- Value-based equality enables comparison of hierarchy quality
- Encapsulated validation ensures metric consistency and validity
- Clear interface separates metric computation from metric storage
"""

import pytest
from datetime import datetime, timezone

from src.domain.value_objects.hierarchy_metadata import HierarchyMetadata
from src.domain.common.validation import DomainValidationError


class TestHierarchyMetadataCreation:
    """Test hierarchy metadata creation and validation."""

    def test_create_valid_hierarchy_metadata(self):
        """Test creation of valid hierarchy metadata."""
        # This test should fail initially (RED phase)
        metadata = HierarchyMetadata(
            total_concepts=150,
            hierarchy_depth=4,
            average_confidence=0.87,
            extraction_timestamp=datetime(2024, 8, 6, 12, 0, 0, tzinfo=timezone.utc),
            root_concepts_count=8,
            leaf_concepts_count=89,
            quality_score=0.92,
        )

        assert metadata.total_concepts == 150
        assert metadata.hierarchy_depth == 4
        assert abs(metadata.average_confidence - 0.87) < 0.001
        assert metadata.root_concepts_count == 8
        assert metadata.leaf_concepts_count == 89
        assert abs(metadata.quality_score - 0.92) < 0.001

    def test_reject_negative_concept_counts(self):
        """Test that hierarchy metadata rejects negative concept counts."""
        # This test should fail initially (RED phase)
        from src.domain.common.validation import DomainValidationError

        with pytest.raises(
            DomainValidationError, match="Total concepts must be non-negative"
        ):
            HierarchyMetadata(
                total_concepts=-5,  # Invalid - negative count
                hierarchy_depth=3,
                average_confidence=0.8,
                extraction_timestamp=datetime.now(timezone.utc),
                root_concepts_count=5,
                leaf_concepts_count=10,
                quality_score=0.85,
            )

    def test_reject_invalid_confidence_score(self):
        """Test that hierarchy metadata rejects invalid confidence scores."""
        # This test should fail initially (RED phase)
        with pytest.raises(
            DomainValidationError,
            match="Invalid hierarchy metadata: Average confidence must be a valid probability between 0.0 and 1.0",
        ):
            HierarchyMetadata(
                total_concepts=100,
                hierarchy_depth=3,
                average_confidence=1.2,  # Invalid - greater than 1.0
                extraction_timestamp=datetime.now(timezone.utc),
                root_concepts_count=5,
                leaf_concepts_count=60,
                quality_score=0.85,
            )

    def test_reject_inconsistent_concept_counts(self):
        """Test that metadata rejects inconsistent root/leaf vs total counts."""
        # This test should fail initially (RED phase)
        with pytest.raises(
            DomainValidationError,
            match="Invalid hierarchy metadata: Root and leaf concept counts cannot exceed total concepts",
        ):
            HierarchyMetadata(
                total_concepts=50,
                hierarchy_depth=3,
                average_confidence=0.8,
                extraction_timestamp=datetime.now(timezone.utc),
                root_concepts_count=30,
                leaf_concepts_count=40,  # 30 + 40 = 70 > 50 total
                quality_score=0.85,
            )


class TestHierarchyMetadataValueObjectBehavior:
    """Test value object characteristics of HierarchyMetadata."""

    def test_hierarchy_metadata_equality(self):
        """Test that metadata with identical values are equal."""
        # This test should fail initially (RED phase)
        timestamp = datetime(2024, 8, 6, 15, 30, 0, tzinfo=timezone.utc)

        metadata1 = HierarchyMetadata(
            total_concepts=200,
            hierarchy_depth=5,
            average_confidence=0.89,
            extraction_timestamp=timestamp,
            root_concepts_count=12,
            leaf_concepts_count=120,
            quality_score=0.91,
        )

        metadata2 = HierarchyMetadata(
            total_concepts=200,
            hierarchy_depth=5,
            average_confidence=0.89,
            extraction_timestamp=timestamp,
            root_concepts_count=12,
            leaf_concepts_count=120,
            quality_score=0.91,
        )

        assert metadata1 == metadata2
        assert hash(metadata1) == hash(metadata2)

    def test_hierarchy_metadata_inequality(self):
        """Test that metadata with different values are not equal."""
        # This test should fail initially (RED phase)
        timestamp = datetime(2024, 8, 6, 15, 30, 0, tzinfo=timezone.utc)

        metadata1 = HierarchyMetadata(
            total_concepts=200,
            hierarchy_depth=5,
            average_confidence=0.89,
            extraction_timestamp=timestamp,
            root_concepts_count=12,
            leaf_concepts_count=120,
            quality_score=0.91,
        )

        metadata2 = HierarchyMetadata(
            total_concepts=250,  # Different total concepts
            hierarchy_depth=5,
            average_confidence=0.89,
            extraction_timestamp=timestamp,
            root_concepts_count=12,
            leaf_concepts_count=120,
            quality_score=0.91,
        )

        assert metadata1 != metadata2
        assert hash(metadata1) != hash(metadata2)

    def test_hierarchy_metadata_immutability(self):
        """Test that hierarchy metadata is immutable after creation."""
        # This test should fail initially (RED phase)
        metadata = HierarchyMetadata(
            total_concepts=100,
            hierarchy_depth=3,
            average_confidence=0.85,
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=8,
            leaf_concepts_count=55,
            quality_score=0.88,
        )

        # Should not be able to modify attributes (frozen dataclass)
        with pytest.raises(AttributeError):
            metadata.total_concepts = 150

        with pytest.raises(AttributeError):
            metadata.quality_score = 0.95


class TestHierarchyMetadataQualityAssessment:
    """Test hierarchy metadata quality assessment capabilities."""

    def test_hierarchy_density_calculation(self):
        """Test calculation of hierarchy density metrics."""
        # This test should fail initially (RED phase)
        metadata = HierarchyMetadata(
            total_concepts=120,
            hierarchy_depth=4,
            average_confidence=0.86,
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=6,
            leaf_concepts_count=72,
            quality_score=0.89,
        )

        # Should calculate meaningful density metrics
        density = metadata.calculate_hierarchy_density()
        assert abs(density - (120 / 4)) < 0.001  # concepts per level

        # Should calculate leaf ratio
        leaf_ratio = metadata.calculate_leaf_ratio()
        assert abs(leaf_ratio - (72 / 120)) < 0.001  # leaf concepts / total

    def test_hierarchy_balance_assessment(self):
        """Test assessment of hierarchy balance and structure quality."""
        # This test should fail initially (RED phase)
        well_balanced = HierarchyMetadata(
            total_concepts=100,
            hierarchy_depth=4,
            average_confidence=0.9,
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=5,  # Few roots - good
            leaf_concepts_count=50,  # Moderate leaves - balanced
            quality_score=0.92,
        )

        poorly_balanced = HierarchyMetadata(
            total_concepts=100,
            hierarchy_depth=2,  # Shallow - poor structure
            average_confidence=0.6,  # Low confidence
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=25,  # Too many roots - poor organization
            leaf_concepts_count=5,  # Too few leaves - incomplete
            quality_score=0.45,
        )

        assert well_balanced.is_well_balanced(min_depth=3, max_root_ratio=0.1) is True
        assert (
            poorly_balanced.is_well_balanced(min_depth=3, max_root_ratio=0.1) is False
        )

    def test_metadata_quality_comparison(self):
        """Test comparison of different hierarchy metadata for quality ranking."""
        # This test should fail initially (RED phase)
        high_quality = HierarchyMetadata(
            total_concepts=200,
            hierarchy_depth=5,
            average_confidence=0.93,
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=8,
            leaf_concepts_count=110,
            quality_score=0.94,
        )

        medium_quality = HierarchyMetadata(
            total_concepts=150,
            hierarchy_depth=3,
            average_confidence=0.78,
            extraction_timestamp=datetime.now(timezone.utc),
            root_concepts_count=15,
            leaf_concepts_count=75,
            quality_score=0.72,
        )

        # Should enable quality comparison
        assert high_quality.is_higher_quality_than(medium_quality) is True
        assert medium_quality.is_higher_quality_than(high_quality) is False


class TestHierarchyMetadataResearchApplications:
    """Test hierarchy metadata usage in research scenarios."""

    def test_metadata_progress_tracking(self):
        """Test metadata enables tracking extraction progress over time."""
        # This test should fail initially (RED phase)
        early_extraction = HierarchyMetadata(
            total_concepts=50,
            hierarchy_depth=2,
            average_confidence=0.7,
            extraction_timestamp=datetime(2024, 8, 1, 10, 0, tzinfo=timezone.utc),
            root_concepts_count=8,
            leaf_concepts_count=25,
            quality_score=0.65,
        )

        later_extraction = HierarchyMetadata(
            total_concepts=180,
            hierarchy_depth=4,
            average_confidence=0.88,
            extraction_timestamp=datetime(2024, 8, 6, 16, 0, tzinfo=timezone.utc),
            root_concepts_count=10,
            leaf_concepts_count=95,
            quality_score=0.89,
        )

        # Should show clear improvement metrics
        improvement = later_extraction.calculate_improvement_over(early_extraction)
        assert improvement["concept_growth"] > 2.0  # More than doubled
        assert improvement["quality_improvement"] > 0.2  # Significant quality gain
        assert improvement["confidence_improvement"] > 0.1  # Better confidence

    def test_metadata_research_summary(self):
        """Test metadata provides comprehensive research summary."""
        # This test should fail initially (RED phase)
        metadata = HierarchyMetadata(
            total_concepts=175,
            hierarchy_depth=4,
            average_confidence=0.85,
            extraction_timestamp=datetime(2024, 8, 6, 14, 30, tzinfo=timezone.utc),
            root_concepts_count=9,
            leaf_concepts_count=88,
            quality_score=0.87,
        )

        # Should generate comprehensive research summary
        summary = metadata.generate_research_summary()
        assert "175 concepts" in summary
        assert "4 levels deep" in summary
        assert "85%" in summary or "0.85" in summary  # Confidence representation
        assert "87%" in summary or "0.87" in summary  # Quality representation
        assert summary.count("\n") >= 3  # Multi-line summary
