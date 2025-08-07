"""
Test suite for batch processor concept extraction integration.

This test suite follows TDD principles to define the expected behavior of concept
extraction integration in the batch processor. It ensures that after papers are
downloaded, concepts are extracted and hierarchies are built for GUI visualization.

Educational Notes:
- Demonstrates Test-Driven Development (TDD) for Clean Architecture
- Shows how to test integration between application layers
- Uses mock objects to isolate system under test
- Validates both individual and batch concept extraction workflows
- Tests error handling and edge cases for robust implementation

Design Patterns Demonstrated:
- Dependency Injection for testability
- Repository Pattern for data access abstraction
- Strategy Pattern for different extraction approaches
- Observer Pattern for progress tracking
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timezone

# Import system under test
import sys

src_path = str(Path(__file__).parent.parent.parent / "src")
root_path = str(Path(__file__).parent.parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from batch_processor import BatchProcessor
from src.domain.entities.research_paper import ResearchPaper
from src.domain.entities.concept import Concept
from src.domain.entities.paper_concepts import PaperConcepts


class TestBatchProcessorConceptExtraction:
    """
    Test batch processor concept extraction integration.

    Educational Notes:
    These tests define the expected behavior for concept extraction integration:
    1. After papers are downloaded, concepts should be extracted from PDFs
    2. Concept hierarchies should be built for visualization
    3. JSON files should be created for GUI consumption
    4. Error handling should be robust for missing PDFs or extraction failures
    """

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def sample_research_papers(self):
        """Create sample research papers for testing."""
        return [
            ResearchPaper(
                title="Heart Rate Variability in Athletes",
                authors=["Dr. Sarah Johnson", "Prof. Michael Chen"],
                abstract="This study examines HRV patterns in elite athletes...",
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                doi="10.1234/hrv-athletes-2023",
                venue="Journal of Sports Medicine",
                keywords=["heart rate variability", "athletes", "performance"],
            ),
            ResearchPaper(
                title="Machine Learning for HRV Analysis",
                authors=["Dr. Lisa Wang", "Prof. David Kumar"],
                abstract="We present a novel ML approach for HRV analysis...",
                publication_date=datetime(2023, 8, 22, tzinfo=timezone.utc),
                doi="10.1234/ml-hrv-2023",
                venue="IEEE Transactions on Biomedical Engineering",
                keywords=["machine learning", "HRV", "signal processing"],
            ),
        ]

    @pytest.fixture
    def sample_concepts(self):
        """Create sample extracted concepts for testing (as dictionaries for JSON serialization)."""
        return [
            {
                "text": "heart rate variability",
                "frequency": 15,
                "relevance_score": 0.95,
                "evidence_strength": 0.88,
            },
            {
                "text": "athletes performance",
                "frequency": 8,
                "relevance_score": 0.85,
                "evidence_strength": 0.76,
            },
            {
                "text": "machine learning algorithms",
                "frequency": 12,
                "relevance_score": 0.92,
                "evidence_strength": 0.83,
            },
        ]

    @pytest.fixture
    def mock_concept_extractor(self, sample_concepts):
        """Create mock concept extractor that returns sample concepts."""
        extractor = Mock()
        extractor.extract_from_directory.return_value = {
            "concepts": sample_concepts,
            "total_extracted": len(sample_concepts),
            "processing_time": 45.2,
            "quality_score": 0.87,
        }
        return extractor

    @pytest.fixture
    def mock_hierarchy_builder(self):
        """Create mock hierarchy builder for testing."""
        builder = Mock()
        builder.build_hierarchy.return_value = {
            "root_concepts": [
                {
                    "id": "hrv-root",
                    "name": "Heart Rate Variability",
                    "level": 0,
                    "children": [
                        {
                            "id": "hrv-athletes",
                            "name": "Athletes Performance",
                            "level": 1,
                            "children": [],
                        },
                        {
                            "id": "hrv-ml",
                            "name": "Machine Learning Analysis",
                            "level": 1,
                            "children": [],
                        },
                    ],
                }
            ],
            "total_concepts": 3,
            "max_depth": 2,
        }
        return builder

    def test_batch_processor_integrates_concept_extraction(
        self,
        temp_output_dir,
        sample_research_papers,
        mock_concept_extractor,
        mock_hierarchy_builder,
    ):
        """
        Test that batch processor integrates concept extraction after paper download.

        Educational Note:
        This test defines the core integration requirement: after papers are processed,
        concepts should be extracted and saved for GUI consumption.
        """
        # Arrange: Setup batch processor with concept extraction enabled
        processor = BatchProcessor(
            output_dir=str(temp_output_dir),
            enable_concept_extraction=True,  # New parameter to control feature
            concept_extractor=mock_concept_extractor,
            hierarchy_builder=mock_hierarchy_builder,
        )

        # Create mock strategy directory with PDFs
        strategy_dir = temp_output_dir / "test_config" / "test_strategy"
        pdfs_dir = strategy_dir / "pdfs"
        pdfs_dir.mkdir(parents=True)

        # Create mock PDF files
        (pdfs_dir / "paper1.pdf").touch()
        (pdfs_dir / "paper2.pdf").touch()

        # Act: Process papers with concept extraction
        processor.save_strategy_results(
            papers=sample_research_papers,
            output_path=strategy_dir,
            config_name="test_config",
            strategy_name="test_strategy",
        )

        # Assert: Concept extraction was called
        mock_concept_extractor.extract_from_directory.assert_called_once_with(pdfs_dir)

        # Assert: Concept files were created
        assert (strategy_dir / "concepts.json").exists()
        assert (strategy_dir / "concept_hierarchy.json").exists()

        # Assert: Concept data has expected structure
        with open(strategy_dir / "concepts.json") as f:
            concepts_data = json.load(f)

        assert "concepts" in concepts_data
        assert "extraction_metadata" in concepts_data
        assert concepts_data["extraction_metadata"]["total_extracted"] == 3

    def test_concept_hierarchy_creation_for_gui(
        self,
        temp_output_dir,
        sample_research_papers,
        mock_concept_extractor,
        mock_hierarchy_builder,
    ):
        """
        Test that concept hierarchies are created in format compatible with GUI D3.js visualization.

        Educational Note:
        This test ensures the output format matches what the GUI visualization expects,
        demonstrating integration testing across application layers.
        """
        # Arrange: Setup processor with hierarchy builder
        processor = BatchProcessor(
            output_dir=str(temp_output_dir),
            enable_concept_extraction=True,
            concept_extractor=mock_concept_extractor,
            hierarchy_builder=mock_hierarchy_builder,
        )

        strategy_dir = temp_output_dir / "test_config" / "test_strategy"
        pdfs_dir = strategy_dir / "pdfs"
        pdfs_dir.mkdir(parents=True)
        (pdfs_dir / "paper1.pdf").touch()

        # Act: Process with hierarchy building
        processor.save_strategy_results(
            papers=sample_research_papers,
            output_path=strategy_dir,
            config_name="test_config",
            strategy_name="test_strategy",
        )

        # Assert: Hierarchy builder was called
        mock_hierarchy_builder.build_hierarchy.assert_called_once()

        # Assert: Hierarchy file has GUI-compatible structure
        with open(strategy_dir / "concept_hierarchy.json") as f:
            hierarchy_data = json.load(f)

        assert "root_concepts" in hierarchy_data
        assert "visualization_metadata" in hierarchy_data

        # Verify D3.js hierarchical structure
        root_concept = hierarchy_data["root_concepts"][0]
        assert "id" in root_concept
        assert "name" in root_concept
        assert "level" in root_concept
        assert "children" in root_concept
        assert isinstance(root_concept["children"], list)

    def test_concept_extraction_error_handling(
        self, temp_output_dir, sample_research_papers
    ):
        """
        Test robust error handling when concept extraction fails.

        Educational Note:
        This test ensures the system degrades gracefully when concept extraction
        encounters errors, maintaining system stability.
        """
        # Arrange: Setup processor with failing concept extractor
        failing_extractor = Mock()
        failing_extractor.extract_from_directory.side_effect = Exception(
            "PDF processing failed"
        )

        processor = BatchProcessor(
            output_dir=str(temp_output_dir),
            enable_concept_extraction=True,
            concept_extractor=failing_extractor,
        )

        strategy_dir = temp_output_dir / "test_config" / "test_strategy"
        pdfs_dir = strategy_dir / "pdfs"
        pdfs_dir.mkdir(parents=True)
        (pdfs_dir / "corrupted.pdf").touch()

        # Act & Assert: Processing should not crash
        processor.save_strategy_results(
            papers=sample_research_papers,
            output_path=strategy_dir,
            config_name="test_config",
            strategy_name="test_strategy",
        )

        # Assert: Regular paper processing still completed
        assert (strategy_dir / "papers.json").exists()
        assert (strategy_dir / "metadata.json").exists()

        # Assert: Error was logged but concept files were not created
        assert not (strategy_dir / "concepts.json").exists()
        assert not (strategy_dir / "concept_hierarchy.json").exists()

    def test_concept_extraction_skipped_when_disabled(
        self, temp_output_dir, sample_research_papers, mock_concept_extractor
    ):
        """
        Test that concept extraction is skipped when disabled.

        Educational Note:
        This test ensures concept extraction is optional and doesn't impact
        core paper processing functionality when disabled.
        """
        # Arrange: Setup processor with concept extraction disabled
        processor = BatchProcessor(
            output_dir=str(temp_output_dir),
            enable_concept_extraction=False,  # Disabled
            concept_extractor=mock_concept_extractor,
        )

        strategy_dir = temp_output_dir / "test_config" / "test_strategy"
        strategy_dir.mkdir(parents=True)

        # Act: Process papers
        processor.save_strategy_results(
            papers=sample_research_papers,
            output_path=strategy_dir,
            config_name="test_config",
            strategy_name="test_strategy",
        )

        # Assert: Concept extraction was not called
        mock_concept_extractor.extract_from_directory.assert_not_called()

        # Assert: Only standard files were created
        assert (strategy_dir / "papers.json").exists()
        assert (strategy_dir / "metadata.json").exists()
        assert not (strategy_dir / "concepts.json").exists()
        assert not (strategy_dir / "concept_hierarchy.json").exists()

    def test_batch_concept_extraction_across_strategies(
        self, temp_output_dir, mock_concept_extractor, mock_hierarchy_builder
    ):
        """
        Test concept extraction across multiple strategies in batch processing.

        Educational Note:
        This test ensures concept extraction works properly when processing
        multiple strategies within a single configuration.
        """
        # Arrange: Setup processor for batch processing
        processor = BatchProcessor(
            output_dir=str(temp_output_dir),
            enable_concept_extraction=True,
            concept_extractor=mock_concept_extractor,
            hierarchy_builder=mock_hierarchy_builder,
        )

        # Create multiple strategy directories
        config_name = "test_config"
        strategies = ["strategy1", "strategy2", "strategy3"]

        for strategy in strategies:
            strategy_dir = temp_output_dir / config_name / strategy
            pdfs_dir = strategy_dir / "pdfs"
            pdfs_dir.mkdir(parents=True)
            (pdfs_dir / f"{strategy}_paper.pdf").touch()

        # Act: Process all strategies
        for strategy in strategies:
            strategy_dir = temp_output_dir / config_name / strategy
            processor.save_strategy_results(
                papers=[],  # Empty for this test
                output_path=strategy_dir,
                config_name=config_name,
                strategy_name=strategy,
            )

        # Assert: Concept extraction called for each strategy
        assert mock_concept_extractor.extract_from_directory.call_count == len(
            strategies
        )

        # Assert: Each strategy has concept files
        for strategy in strategies:
            strategy_dir = temp_output_dir / config_name / strategy
            assert (strategy_dir / "concepts.json").exists()
            assert (strategy_dir / "concept_hierarchy.json").exists()

    def test_concept_data_format_for_gui_api(
        self,
        temp_output_dir,
        sample_research_papers,
        mock_concept_extractor,
        mock_hierarchy_builder,
    ):
        """
        Test that concept data format matches GUI API expectations.

        Educational Note:
        This test ensures the JSON output format is compatible with the GUI's
        D3.js visualization framework and API endpoints.
        """
        # Arrange: Setup processor with both extractors
        processor = BatchProcessor(
            output_dir=str(temp_output_dir),
            enable_concept_extraction=True,
            concept_extractor=mock_concept_extractor,
            hierarchy_builder=mock_hierarchy_builder,
        )

        strategy_dir = temp_output_dir / "hrv_research" / "comprehensive_analysis"
        pdfs_dir = strategy_dir / "pdfs"
        pdfs_dir.mkdir(parents=True)
        (pdfs_dir / "hrv_paper.pdf").touch()

        # Act: Process papers
        processor.save_strategy_results(
            papers=sample_research_papers,
            output_path=strategy_dir,
            config_name="hrv_research",
            strategy_name="comprehensive_analysis",
        )

        # Assert: GUI API compatible structure in hierarchy file
        with open(strategy_dir / "concept_hierarchy.json") as f:
            hierarchy_data = json.load(f)

        # Verify GUI API compatibility
        assert "domain" in hierarchy_data["visualization_metadata"]
        assert "strategy" in hierarchy_data["visualization_metadata"]
        assert "generated_at" in hierarchy_data["visualization_metadata"]
        assert "total_concepts" in hierarchy_data["visualization_metadata"]

        # Verify D3.js sunburst/tree structure
        assert "root_concepts" in hierarchy_data
        assert isinstance(hierarchy_data["root_concepts"], list)

        # Verify each concept has required fields for D3.js
        for concept in hierarchy_data["root_concepts"]:
            assert "id" in concept
            assert "name" in concept
            assert "level" in concept
            assert "children" in concept
