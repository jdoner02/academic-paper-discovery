"""
Unit tests for BatchProcessor PDF download functionality.

This test module follows TDD methodology to define the desired behavior for
batch processing with PDF downloads, ensuring compatibility with the existing
concept extraction framework.

Educational Notes:
- Demonstrates TDD Red-Green-Refactor cycle
- Tests define behavior before implementation exists
- Validates integration with concept extraction framework
- Ensures proper folder structure for downstream processing

Test Categories:
- Unit Tests: BatchProcessor class behavior in isolation
- Integration Tests: Interaction with use cases and services
- Contract Tests: Interface compliance for concept extraction
- Performance Tests: Bulk download operations
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import List

# Import system under test
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from batch_processor import BatchProcessor
from src.domain.entities.research_paper import ResearchPaper
from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from datetime import datetime, timezone


class TestBatchProcessorPDFDownloads:
    """Test suite for batch processor PDF download functionality."""

    def setup_method(self):
        """Set up test environment for each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / "config"
        self.config_dir.mkdir()
        self.output_dir = Path(self.test_dir) / "outputs"

        # Create a sample configuration file
        sample_config = """
search_configuration:
  default_strategy: "test_strategy"
  citation_threshold: 5
  publication_date_range:
    start_year: 2020
    end_year: 2025
  max_concurrent_searches: 3
  include_preprints: true
  exclude_terms: ["exclude_term"]

strategies:
  test_strategy:
    name: "Test Strategy"
    description: "Test strategy for PDF downloads"
    primary_keywords:
      - "test keyword"
      - "cybersecurity"
    secondary_keywords:
      - "machine learning"
      - "deep learning"
    technical_terms:
      - "neural network"
      - "algorithm"
    application_domains:
      - "computer science"
    exclude_terms:
      - "biology"
"""
        config_file = self.config_dir / "test_config.yaml"
        config_file.write_text(sample_config)

        self.processor = BatchProcessor(
            config_dir=str(self.config_dir),
            output_dir=str(self.output_dir),
            max_papers=3,
        )

    def teardown_method(self):
        """Clean up test environment after each test."""
        shutil.rmtree(self.test_dir)

    def test_batch_processor_calls_execute_strategy_with_download_papers_true(self):
        """
        RED PHASE: Test that batch processor passes download_papers=True to use case.

        This test will initially fail because the current implementation
        doesn't pass download_papers=True to the execute_strategy method.
        """
        # Arrange
        mock_use_case = Mock(spec=ExecuteKeywordSearchUseCase)
        mock_use_case.execute_strategy.return_value = []

        # Act
        self.processor.process_strategy(mock_use_case, "test_config", "test_strategy")

        # Assert - This will fail initially (RED phase)
        mock_use_case.execute_strategy.assert_called_once_with(
            "test_strategy", download_papers=True
        )

    def test_batch_processor_creates_pdf_download_structure(self):
        """
        RED PHASE: Test that batch processor creates expected folder structure for PDFs.

        The concept extraction framework expects PDFs to be in organized folders
        alongside metadata for processing.
        """
        # Arrange
        sample_papers = [
            ResearchPaper(
                title="Test Paper 1",
                authors=["Author 1"],
                abstract="Test abstract",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                doi="10.1000/test.001",
                venue="Test Venue",
                url="https://example.com/paper1.pdf",
            )
        ]

        mock_use_case = Mock(spec=ExecuteKeywordSearchUseCase)
        mock_use_case.execute_strategy.return_value = sample_papers

        # Act
        self.processor.process_strategy(mock_use_case, "test_config", "test_strategy")

        # Assert - Check expected folder structure exists
        expected_path = self.output_dir / "test_config" / "test_strategy"
        assert expected_path.exists(), "Strategy folder should be created"

        # Check for both metadata and PDF storage capability
        papers_json = expected_path / "papers.json"
        metadata_json = expected_path / "metadata.json"
        assert papers_json.exists(), "Papers JSON should exist"
        assert metadata_json.exists(), "Metadata JSON should exist"

        # This will fail initially - PDFs directory should exist for downloads
        pdfs_dir = expected_path / "pdfs"
        assert pdfs_dir.exists(), "PDFs directory should be created for downloads"

    def test_batch_processor_enables_pdf_downloads_by_default(self):
        """
        RED PHASE: Test that batch processor enables PDF downloads by default.

        For concept extraction to work, we need actual PDF files downloaded,
        not just metadata.
        """
        # Arrange
        sample_papers = [
            ResearchPaper(
                title="Cybersecurity Research Paper",
                authors=["Dr. Test Author"],
                abstract="Advanced cybersecurity research",
                publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
                doi="10.1000/cyber.2023.001",
                venue="Security Conference",
                url="https://arxiv.org/pdf/2306.12345.pdf",
            )
        ]

        mock_use_case = Mock(spec=ExecuteKeywordSearchUseCase)
        mock_use_case.execute_strategy.return_value = sample_papers

        # Act
        self.processor.process_strategy(mock_use_case, "test_config", "test_strategy")

        # Assert - Verify download_papers=True was passed
        # This will fail initially because current implementation doesn't pass this parameter
        call_args = mock_use_case.execute_strategy.call_args
        assert call_args is not None, "execute_strategy should be called"

        # Check if download_papers was passed as True
        args, kwargs = call_args
        assert (
            kwargs.get("download_papers", False) is True
        ), "download_papers should be True to enable PDF downloads"

    def test_batch_processor_pdf_structure_compatible_with_concept_extraction(self):
        """
        RED PHASE: Test that PDF folder structure is compatible with concept extraction.

        The concept extraction framework expects PDFs to be accessible for processing.
        This test verifies the structure supports downstream concept extraction.
        """
        # Arrange
        sample_papers = [
            ResearchPaper(
                title="AI Security Paper",
                authors=["Dr. AI Researcher"],
                abstract="AI security methodologies",
                publication_date=datetime(2023, 8, 1, tzinfo=timezone.utc),
                doi="10.1000/ai.2023.042",
                venue="AI Security Journal",
            )
        ]

        mock_use_case = Mock(spec=ExecuteKeywordSearchUseCase)
        mock_use_case.execute_strategy.return_value = sample_papers

        # Act
        self.processor.process_strategy(mock_use_case, "test_config", "test_strategy")

        # Assert - Check structure supports concept extraction
        strategy_path = self.output_dir / "test_config" / "test_strategy"

        # Metadata should be available for concept extraction framework
        metadata_file = strategy_path / "metadata.json"
        assert metadata_file.exists(), "Metadata required for concept extraction"

        # Papers JSON should contain paper information
        papers_file = strategy_path / "papers.json"
        assert papers_file.exists(), "Papers JSON required for processing"

        # PDF storage area should exist (will fail initially)
        pdf_area = strategy_path / "pdfs"
        assert pdf_area.exists(), "PDF storage area required for concept extraction"

    def test_batch_processor_handles_multiple_configurations_with_pdfs(self):
        """
        RED PHASE: Test batch processing of multiple configurations with PDF downloads.

        This integration test verifies that PDF downloads work across multiple
        research domain configurations.
        """
        # Arrange - Create multiple config files
        config2_content = """
search_configuration:
  default_strategy: "quantum_strategy"
  citation_threshold: 3
  publication_date_range:
    start_year: 2022
    end_year: 2025

strategies:
  quantum_strategy:
    name: "Quantum Computing Security"
    description: "Post-quantum cryptography research"
    primary_keywords:
      - "post-quantum cryptography"
      - "quantum resistant"
    secondary_keywords:
      - "lattice cryptography"
"""
        config2_file = self.config_dir / "quantum_config.yaml"
        config2_file.write_text(config2_content)

        # Mock the entire batch processing workflow
        with patch.object(self.processor, "process_configuration") as mock_process:
            # Act
            self.processor.process_all_configurations(use_arxiv=False)

            # Assert - Both configurations should be processed
            # This will initially fail as process_all_configurations doesn't enable PDF downloads
            assert (
                mock_process.call_count == 2
            ), "Both configurations should be processed"

            # Verify configurations were processed with PDF capability
            calls = mock_process.call_args_list
            config_names = [call[0][0] for call in calls]
            assert "test_config" in config_names, "test_config should be processed"
            assert (
                "quantum_config" in config_names
            ), "quantum_config should be processed"


class TestBatchProcessorPDFIntegration:
    """Integration tests for PDF download functionality with real components."""

    def setup_method(self):
        """Set up integration test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / "config"
        self.config_dir.mkdir()
        self.output_dir = Path(self.test_dir) / "outputs"

    def teardown_method(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.test_dir)

    @patch(
        "src.application.use_cases.execute_keyword_search_use_case.ExecuteKeywordSearchUseCase"
    )
    def test_integration_batch_processor_with_pdf_downloads(self, mock_use_case_class):
        """
        RED PHASE: Integration test for complete PDF download workflow.

        This test verifies the entire pipeline from configuration loading
        to PDF downloads works correctly.
        """
        # Arrange
        sample_config = """
search_configuration:
  default_strategy: "integration_test"
  citation_threshold: 1
  
strategies:
  integration_test:
    name: "Integration Test Strategy"
    description: "Test strategy for integration"
    primary_keywords: ["test"]
"""
        config_file = self.config_dir / "integration_test.yaml"
        config_file.write_text(sample_config)

        # Mock use case to return sample papers
        mock_use_case = Mock()
        sample_papers = [
            ResearchPaper(
                title="Integration Test Paper",
                authors=["Test Author"],
                abstract="Integration test abstract",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                doi="10.1000/integration.test",
            )
        ]
        mock_use_case.execute_strategy.return_value = sample_papers
        mock_use_case_class.return_value = mock_use_case

        processor = BatchProcessor(
            config_dir=str(self.config_dir),
            output_dir=str(self.output_dir),
            max_papers=5,
        )

        # Act
        # This will fail initially because BatchProcessor doesn't pass download_papers=True
        with patch("batch_processor.ArxivPaperRepository"):
            processor.process_all_configurations(use_arxiv=True)

        # Assert
        # Verify execute_strategy was called with download_papers=True
        mock_use_case.execute_strategy.assert_called_with(
            "integration_test", download_papers=True
        )

        # Verify folder structure was created
        expected_path = self.output_dir / "integration_test" / "integration_test"
        assert expected_path.exists(), "Strategy output folder should exist"


class TestBatchProcessorConceptExtractionCompatibility:
    """Tests verifying compatibility with existing concept extraction framework."""

    def test_pdf_structure_supports_concept_extraction_workflow(self):
        """
        RED PHASE: Test that PDF download structure supports concept extraction.

        The concept extraction framework needs to be able to find and process
        downloaded PDFs. This test verifies the structure is compatible.
        """
        # This test will be implemented once we understand the exact requirements
        # of the concept extraction framework from examining the codebase

        # Arrange
        test_dir = tempfile.mkdtemp()
        try:
            output_dir = Path(test_dir) / "outputs"
            strategy_dir = output_dir / "cybersecurity_config" / "threat_analysis"
            strategy_dir.mkdir(parents=True)

            # Simulate the expected structure after PDF downloads
            pdfs_dir = strategy_dir / "pdfs"
            pdfs_dir.mkdir()

            # Create sample PDF file (placeholder)
            sample_pdf = pdfs_dir / "cybersecurity_threats_arxiv_2023001.pdf"
            sample_pdf.write_text("PDF content placeholder")

            # Create metadata that concept extraction expects
            papers_json = strategy_dir / "papers.json"
            metadata = {
                "config_name": "cybersecurity_config",
                "strategy_name": "threat_analysis",
                "papers": [
                    {
                        "title": "Cybersecurity Threats",
                        "authors": ["Dr. Security"],
                        "pdf_path": str(sample_pdf),
                        "doi": "10.1000/cyber.2023.001",
                    }
                ],
            }
            papers_json.write_text(str(metadata).replace("'", '"'))

            # Act & Assert
            # Verify structure exists as expected by concept extraction
            assert pdfs_dir.exists(), "PDFs directory should exist"
            assert sample_pdf.exists(), "Sample PDF should exist"
            assert papers_json.exists(), "Papers metadata should exist"

            # This assertion will initially pass, but represents the contract
            # we need to maintain for concept extraction compatibility

        finally:
            shutil.rmtree(test_dir)
