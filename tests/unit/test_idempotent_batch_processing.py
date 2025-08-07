"""
Tests for idempotent batch processing with metadata tracking.

This test module follows TDD methodology to define idempotent behavior where:
- Papers are not downloaded multiple times
- Metadata tracks last download dates
- Daily runs only fetch new papers
- Folder structure remains consistent across runs

Educational Notes:
- Demonstrates idempotent operations in batch processing
- Tests incremental update patterns
- Validates metadata-driven deduplication
- Ensures clean folder structure without date stamps
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from typing import List

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from batch_processor import BatchProcessor
from src.domain.entities.research_paper import ResearchPaper


class TestIdempotentBatchProcessing:
    """Test suite for idempotent batch processing functionality."""

    def setup_method(self):
        """Set up test environment for each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / "config"
        self.config_dir.mkdir()
        self.output_dir = Path(self.test_dir) / "outputs"

        # Create sample configuration
        sample_config = """
search_configuration:
  default_strategy: "idempotent_test"
  citation_threshold: 1
  publication_date_range:
    start_year: 2023
    end_year: 2025

strategies:
  idempotent_test:
    name: "Idempotent Test Strategy" 
    description: "Test strategy for idempotent operations"
    primary_keywords:
      - "cybersecurity"
      - "machine learning"
"""
        config_file = self.config_dir / "test_config.yaml"
        config_file.write_text(sample_config)

        self.processor = BatchProcessor(
            config_dir=str(self.config_dir),
            output_dir=str(self.output_dir),
            max_papers=5,
        )

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_batch_processor_creates_consistent_folder_structure_without_dates(self):
        """
        RED PHASE: Test that folder structure is consistent across runs (no date stamps).

        The output should be: outputs/config_name/strategy_name/
        NOT: outputs/2025-08-07_strategy_name/
        """
        # Act
        output_path = self.processor.create_output_structure(
            "test_config", "idempotent_test"
        )

        # Assert - Structure should be predictable without date stamps
        expected_path = self.output_dir / "test_config" / "idempotent_test"
        assert (
            output_path == expected_path
        ), f"Expected {expected_path}, got {output_path}"
        assert output_path.exists(), "Output directory should be created"

        # Verify no date stamps in the path
        path_parts = str(output_path).split("/")
        for part in path_parts:
            assert not part.startswith("20"), f"Found date stamp in path: {part}"

    def test_batch_processor_tracks_download_metadata_with_timestamps(self):
        """
        RED PHASE: Test that metadata includes last download timestamps for idempotent operations.

        This will fail initially because current metadata doesn't track download timestamps.
        """
        # Arrange
        sample_papers = [
            ResearchPaper(
                title="Test Paper 1",
                authors=["Author 1"],
                abstract="Test abstract",
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                doi="10.1000/test.001",
            )
        ]

        output_path = self.output_dir / "test_config" / "idempotent_test"
        output_path.mkdir(parents=True)

        # Act
        self.processor.save_strategy_results(
            sample_papers, output_path, "test_config", "idempotent_test"
        )

        # Assert - Metadata should include download tracking
        metadata_file = output_path / "metadata.json"
        assert metadata_file.exists(), "Metadata file should exist"

        with open(metadata_file) as f:
            metadata = json.load(f)

        # This will fail initially - metadata should track last download date
        assert (
            "last_download_date" in metadata
        ), "Metadata should track last download date"
        assert (
            "downloaded_papers" in metadata
        ), "Metadata should track downloaded papers"

    def test_batch_processor_skips_already_downloaded_papers(self):
        """
        RED PHASE: Test that already downloaded papers are skipped in subsequent runs.

        This ensures idempotent behavior - same papers aren't downloaded multiple times.
        """
        # Arrange - Simulate existing metadata from previous run
        output_path = self.output_dir / "test_config" / "idempotent_test"
        output_path.mkdir(parents=True)

        # Create existing metadata with downloaded papers
        existing_metadata = {
            "last_download_date": "2025-08-06T12:00:00Z",
            "downloaded_papers": {
                "10.1000/test.001": {
                    "title": "Test Paper 1",
                    "download_date": "2025-08-06T12:00:00Z",
                    "file_path": "pdfs/test_paper_1.pdf",
                }
            },
            "strategy_metadata": {
                "config_name": "test_config",
                "strategy_name": "idempotent_test",
            },
        }

        metadata_file = output_path / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(existing_metadata, f)

        # Act - Process the same papers again
        sample_papers = [
            ResearchPaper(
                title="Test Paper 1",  # Same paper as in metadata
                authors=["Author 1"],
                abstract="Test abstract",
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                doi="10.1000/test.001",
            ),
            ResearchPaper(
                title="Test Paper 2",  # New paper
                authors=["Author 2"],
                abstract="New test abstract",
                publication_date=datetime(2023, 8, 1, tzinfo=timezone.utc),
                doi="10.1000/test.002",
            ),
        ]

        # Mock the use case to return these papers
        mock_use_case = Mock()
        mock_use_case.execute_strategy.return_value = sample_papers

        # This will fail initially because current implementation doesn't check for existing downloads
        with patch.object(
            self.processor, "_should_download_paper"
        ) as mock_should_download:
            mock_should_download.side_effect = (
                lambda paper, metadata: paper.doi != "10.1000/test.001"
            )

            self.processor.process_strategy(
                mock_use_case, "test_config", "idempotent_test"
            )

            # Verify that only new paper would be downloaded (Test Paper 2)
            assert mock_should_download.call_count == 2, "Should check both papers"

    def test_batch_processor_updates_metadata_incrementally(self):
        """
        RED PHASE: Test that metadata is updated incrementally with new downloads.

        Each run should add new papers to metadata without losing existing entries.
        """
        # Arrange - Start with existing metadata
        output_path = self.output_dir / "test_config" / "idempotent_test"
        output_path.mkdir(parents=True)

        existing_metadata = {
            "last_download_date": "2025-08-06T12:00:00Z",
            "downloaded_papers": {
                "10.1000/existing.001": {
                    "title": "Existing Paper",
                    "download_date": "2025-08-06T12:00:00Z",
                }
            },
        }

        metadata_file = output_path / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(existing_metadata, f)

        # Act - Add new papers
        new_papers = [
            ResearchPaper(
                title="New Paper 1",
                authors=["New Author"],
                abstract="New abstract",
                publication_date=datetime(2023, 8, 1, tzinfo=timezone.utc),
                doi="10.1000/new.001",
            )
        ]

        # This will fail initially - save_strategy_results doesn't merge with existing metadata
        self.processor.save_strategy_results(
            new_papers, output_path, "test_config", "idempotent_test"
        )

        # Assert - Metadata should contain both existing and new papers
        with open(metadata_file) as f:
            updated_metadata = json.load(f)

        assert "downloaded_papers" in updated_metadata
        downloaded_papers = updated_metadata["downloaded_papers"]

        # Should contain both existing and new papers
        assert (
            "10.1000/existing.001" in downloaded_papers
        ), "Should preserve existing papers"
        assert "10.1000/new.001" in downloaded_papers, "Should add new papers"

        # Last download date should be updated
        assert (
            updated_metadata["last_download_date"]
            > existing_metadata["last_download_date"]
        )

    def test_batch_processor_supports_incremental_daily_runs(self):
        """
        RED PHASE: Test that daily runs work incrementally without duplication.

        This simulates running the batch processor multiple times and ensures
        it only downloads new papers each time.
        """
        # This test will define the behavior for incremental updates
        # and will fail initially because the current implementation
        # doesn't support this workflow

        # Arrange - First run
        mock_use_case = Mock()
        day1_papers = [
            ResearchPaper(
                title="Day 1 Paper",
                authors=["Author 1"],
                abstract="First day abstract",
                publication_date=datetime(2023, 8, 1, tzinfo=timezone.utc),
                doi="10.1000/day1.001",
            )
        ]
        mock_use_case.execute_strategy.return_value = day1_papers

        # Act - First run
        self.processor.process_strategy(mock_use_case, "test_config", "idempotent_test")

        # Arrange - Second run with additional papers
        day2_papers = day1_papers + [
            ResearchPaper(
                title="Day 2 Paper",
                authors=["Author 2"],
                abstract="Second day abstract",
                publication_date=datetime(2023, 8, 2, tzinfo=timezone.utc),
                doi="10.1000/day2.001",
            )
        ]
        mock_use_case.execute_strategy.return_value = day2_papers

        # Act - Second run (should only download new paper)
        # This will fail because current implementation would download all papers again
        with patch.object(
            self.processor, "_get_existing_metadata"
        ) as mock_get_metadata:
            mock_get_metadata.return_value = {
                "downloaded_papers": {"10.1000/day1.001": {"title": "Day 1 Paper"}}
            }

            self.processor.process_strategy(
                mock_use_case, "test_config", "idempotent_test"
            )

            # Verify metadata contains both papers but only new one was "downloaded"
            output_path = self.output_dir / "test_config" / "idempotent_test"
            metadata_file = output_path / "metadata.json"

            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)

                downloaded_papers = metadata.get("downloaded_papers", {})
                assert "10.1000/day1.001" in downloaded_papers
                assert "10.1000/day2.001" in downloaded_papers


class TestBatchProcessorMetadataManagement:
    """Tests for metadata management in idempotent operations."""

    def test_metadata_includes_required_fields_for_idempotence(self):
        """
        RED PHASE: Test that metadata includes all fields needed for idempotent operations.
        """
        # This test will fail initially because current metadata doesn't include
        # the fields needed for idempotent operations

        # The metadata should include:
        # - last_download_date
        # - downloaded_papers (keyed by DOI)
        # - paper_count_per_run (for tracking growth)
        # - strategy_config_hash (to detect config changes)

        pass  # Will implement once we understand exact requirements
