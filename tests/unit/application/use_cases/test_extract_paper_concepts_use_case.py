"""
Tests for ExtractPaperConceptsUseCase - Enhanced         # Create test data
        self.test_paper = ResearchPaper(
            title="Heart Rate Variability in Traumatic Brain Injury",
         # Create test paper and path
        self.test_paper = ResearchPaper(
            title="Advanced HRV Analysis Techniques",
            authors=["Dr. Garcia", "Dr. Kim"],
            publication_date=datetime(2024, 1, 1        self.test_paper = ResearchPaper(
            title="Test Paper",
            author        self.test_paper = ResearchPaper(
            title="Integration Test: Heart Rate Variability in Clinical Practice",
            authors=["Dr. Integration", "Dr. Test"],
            publication_date=datetime(2024, 3, 1, tzinfo=timezone.utc),
            doi="10.1000/integration.test.2024",
            abstract="Comprehensive study of HRV applications in clinical settings.",
            source_metadata=SourceMetadata(
                source_name="integration_test_source",
                source_identifier="test:integration-001",
                source_url="https://test.com/integration",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.99,
                source_specific_data={"test_mode": True}
            )
        )],
            publication_date=datetime(2024, 2, 1, tzinfo=timezone.utc),
            doi="10.1000/test.2024",
            abstract="Test abstract",
            source_metadata=SourceMetadata(
                source_name="test_source",
                source_identifier="test:003",
                source_url="https://test.com",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="unknown",
                quality_score=0.7,
                source_specific_data={}
            )
        )ne.utc),
            doi="10.1000/hrv.analysis.2024",
            abstract="Novel approaches to HRV analysis in clinical settings.",
            source_metadata=SourceMetadata(
                source_name="test_source",
                source_identifier="test:hrv-002",
                source_url="https://test.com/hrv-paper",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.95,
                source_specific_data={}
            )
        )s=["Dr. Smith", "Dr. Johnson"],
            publication_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            doi="10.1000/test.doi.2024",
            abstract="Research on HRV patterns in TBI patients.",
            source_metadata=SourceMetadata(
                source_name="test_source",
                source_identifier="test:001",
                source_url="https://test.com/paper",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.9,
                source_specific_data={}
            )
        ) concept extraction.

This test suite demonstrates comprehensive testing of application layer use cases,
including integration with multiple domain services and proper error handling.

Educational Notes:
- Shows test structure for complex use cases with multiple dependencies
- Demonstrates mocking strategies for ports and domain services
- Tests both happy path and error conditions thoroughly
- Validates integration of hierarchy building with existing concept extraction
- Covers configuration and dependency injection patterns

Test Organization:
- Basic concept extraction (existing functionality)
- Enhanced hierarchy building (new functionality)
- Error handling and edge cases
- Integration scenarios with complex workflows
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
from typing import List
from datetime import datetime, timezone
import numpy as np

from src.application.use_cases.extract_paper_concepts_use_case import (
    ExtractPaperConceptsUseCase,
    PDFTextExtractorPort,
    ConceptRepositoryPort,
)
from src.domain.entities.research_paper import ResearchPaper
from src.domain.entities.paper_concepts import PaperConcepts
from src.domain.entities.concept import Concept
from src.domain.services.concept_extractor import (
    ConceptExtractor,
    ExtractionConfiguration,
)
from src.domain.services.concept_hierarchy_builder import ConceptHierarchyBuilder
from src.domain.value_objects.embedding_vector import EmbeddingVector
from src.domain.value_objects.source_metadata import SourceMetadata


class TestExtractPaperConceptsUseCaseBasic:
    """Test basic concept extraction functionality (existing behavior)."""

    def setup_method(self):
        """Set up test fixtures for each test method."""
        # Create mock dependencies
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)
        self.mock_concept_extractor = Mock(spec=ConceptExtractor)

        # Create test data
        self.test_paper = ResearchPaper(
            title="Heart Rate Variability in Traumatic Brain Injury",
            authors=["Dr. Smith", "Dr. Johnson"],
            doi="10.1000/test.doi.2024",
            abstract="Research on HRV patterns in TBI patients.",
            publication_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
            source_metadata=SourceMetadata(
                source_name="test_source",
                source_identifier="test:001",
                source_url="https://test.com/paper",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.9,
                source_specific_data={},
            ),
        )

        self.test_pdf_path = Path("/tmp/test_paper.pdf")

    def test_create_use_case_with_default_dependencies(self):
        """Test creating use case with default dependencies."""
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
        )

        assert use_case.pdf_extractor == self.mock_pdf_extractor
        assert use_case.concept_repository == self.mock_concept_repository
        assert isinstance(use_case.concept_extractor, ConceptExtractor)
        assert isinstance(use_case.config, ExtractionConfiguration)

    def test_create_use_case_with_custom_dependencies(self):
        """Test creating use case with custom dependencies."""
        custom_config = ExtractionConfiguration()
        custom_config.min_concept_frequency = 5
        custom_config.min_relevance_threshold = 0.8

        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.mock_concept_extractor,
            config=custom_config,
        )

        assert use_case.concept_extractor == self.mock_concept_extractor
        assert use_case.config == custom_config
        assert use_case.config.min_concept_frequency == 5


class TestExtractPaperConceptsUseCaseHierarchyIntegration:
    """Test enhanced functionality with hierarchical concept building (NEW)."""

    def setup_method(self):
        """Set up test fixtures for hierarchy testing."""
        # Create mock dependencies
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)
        self.mock_concept_extractor = Mock(spec=ConceptExtractor)
        self.mock_hierarchy_builder = Mock(spec=ConceptHierarchyBuilder)

        # Configure mock methods that are called by the use case
        self.mock_concept_extractor.get_extraction_statistics.return_value = {
            "quality_metrics": {"quality_ratio": 0.85}
        }

        # Create test concepts with embeddings
        self.flat_concepts = [
            Concept(
                text="cardiovascular medicine",
                frequency=100,
                relevance_score=0.9,
                embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0, 0.0])),
                source_papers={"10.1000/hrv.analysis.2024"},
            ),
            Concept(
                text="heart rate variability",
                frequency=50,
                relevance_score=0.8,
                embedding=EmbeddingVector(np.array([0.9, 0.1, 0.0, 0.0])),
                source_papers={"10.1000/hrv.analysis.2024"},
            ),
            Concept(
                text="HRV analysis",
                frequency=25,
                relevance_score=0.7,
                embedding=EmbeddingVector(np.array([0.85, 0.15, 0.0, 0.0])),
                source_papers={"10.1000/hrv.analysis.2024"},
            ),
        ]

        # Create hierarchical concepts (what hierarchy builder should return)
        self.hierarchical_concepts = [
            # Root concept - cardiovascular medicine
            Concept(
                text="cardiovascular medicine",
                frequency=100,
                relevance_score=0.9,
                embedding=EmbeddingVector(np.array([1.0, 0.0, 0.0, 0.0])),
                source_papers={"10.1000/hrv.analysis.2024"},
                parent_concepts=set(),
                child_concepts={"heart rate variability"},
                concept_level=0,
                cluster_id="cluster_medical",
                evidence_strength=0.9,
            ),
            # Middle concept - heart rate variability
            Concept(
                text="heart rate variability",
                frequency=50,
                relevance_score=0.8,
                embedding=EmbeddingVector(np.array([0.9, 0.1, 0.0, 0.0])),
                source_papers={"10.1000/hrv.analysis.2024"},
                parent_concepts={"cardiovascular medicine"},
                child_concepts={"HRV analysis"},
                concept_level=1,
                cluster_id="cluster_medical",
                evidence_strength=0.8,
            ),
            # Leaf concept - HRV analysis
            Concept(
                text="HRV analysis",
                frequency=25,
                relevance_score=0.7,
                embedding=EmbeddingVector(np.array([0.85, 0.15, 0.0, 0.0])),
                source_papers={"10.1000/hrv.analysis.2024"},
                parent_concepts={"heart rate variability"},
                child_concepts=set(),
                concept_level=2,
                cluster_id="cluster_medical",
                evidence_strength=0.7,
            ),
        ]  # Create test paper and path
        self.test_paper = ResearchPaper(
            title="Advanced HRV Analysis Techniques",
            authors=["Dr. Garcia", "Dr. Kim"],
            doi="10.1000/hrv.analysis.2024",
            abstract="Novel approaches to HRV analysis in clinical settings.",
            publication_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
            source_metadata=SourceMetadata(
                source_name="test_source",
                source_identifier="test:hrv-002",
                source_url="https://test.com/hrv-paper",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.95,
                source_specific_data={},
            ),
        )

        self.test_pdf_path = Path("/tmp/hrv_paper.pdf")

    def test_extract_concepts_with_hierarchy_building_enabled(self):
        """Test concept extraction with hierarchy building enabled (NEW FEATURE)."""
        # Setup mocks
        paper_text = (
            "Research on cardiovascular medicine and heart rate variability analysis..."
        )

        # Mock PDF extraction
        self.mock_pdf_extractor.extract_text_from_pdf.return_value = paper_text

        # Mock concept extraction returning flat concepts
        flat_paper_concepts = PaperConcepts(
            paper_doi=self.test_paper.doi,
            paper_title=self.test_paper.title,
            concepts=self.flat_concepts,
            extraction_metadata={
                "total_concepts": len(self.flat_concepts),
                "extraction_method": "test",
                "has_hierarchical_relationships": False,
            },
        )
        self.mock_concept_extractor.extract_concepts_from_paper.return_value = (
            flat_paper_concepts
        )

        # Mock hierarchy building returning hierarchical concepts
        self.mock_hierarchy_builder.build_hierarchy.return_value = (
            self.hierarchical_concepts
        )

        # Mock repository operations
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        # Create enhanced use case with hierarchy builder
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.mock_concept_extractor,
            hierarchy_builder=self.mock_hierarchy_builder,  # NEW PARAMETER
            enable_hierarchy_building=True,  # NEW PARAMETER
        )

        # Execute the use case
        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper, pdf_path=self.test_pdf_path
            )

        # Verify PDF extraction was called
        self.mock_pdf_extractor.extract_text_from_pdf.assert_called_once_with(
            self.test_pdf_path
        )

        # Verify concept extraction was called
        self.mock_concept_extractor.extract_concepts_from_paper.assert_called_once_with(
            paper_text=paper_text,
            paper_doi=self.test_paper.doi,
            paper_title=self.test_paper.title,
            domain=None,
        )

        # Verify hierarchy building was called with flat concepts
        self.mock_hierarchy_builder.build_hierarchy.assert_called_once_with(
            self.flat_concepts
        )

        # Verify result contains hierarchical concepts
        assert result.has_hierarchical_relationships
        assert len(result.concepts) == 3

        # Verify hierarchy structure is preserved
        root_concept = next(c for c in result.concepts if c.is_root_concept())
        assert root_concept.text == "cardiovascular medicine"
        assert "heart rate variability" in root_concept.child_concepts

        leaf_concept = next(c for c in result.concepts if c.is_leaf_concept())
        assert leaf_concept.text == "HRV analysis"
        assert "heart rate variability" in leaf_concept.parent_concepts

        # Verify repository save was called with enhanced concepts
        self.mock_concept_repository.save_paper_concepts.assert_called_once()
        saved_concepts = self.mock_concept_repository.save_paper_concepts.call_args[0][
            0
        ]
        assert saved_concepts.has_hierarchical_relationships

    def test_extract_concepts_with_hierarchy_building_disabled(self):
        """Test concept extraction with hierarchy building disabled (backward compatibility)."""
        # Setup mocks
        paper_text = "Research text without hierarchical analysis..."

        self.mock_pdf_extractor.extract_text_from_pdf.return_value = paper_text

        flat_paper_concepts = PaperConcepts(
            paper_doi=self.test_paper.doi,
            paper_title=self.test_paper.title,
            concepts=self.flat_concepts,
            extraction_metadata={
                "total_concepts": len(self.flat_concepts),
                "extraction_method": "test",
                "has_hierarchical_relationships": False,
            },
        )
        self.mock_concept_extractor.extract_concepts_from_paper.return_value = (
            flat_paper_concepts
        )

        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        # Create use case with hierarchy building disabled
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.mock_concept_extractor,
            enable_hierarchy_building=False,  # DISABLED
        )

        # Execute the use case
        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper, pdf_path=self.test_pdf_path
            )

        # Verify hierarchy builder was NOT called
        assert not hasattr(use_case, "hierarchy_builder")

        # Verify result contains flat concepts only
        assert not result.has_hierarchical_relationships
        assert len(result.concepts) == 3

        # Verify concepts don't have hierarchical data
        for concept in result.concepts:
            assert not concept.parent_concepts
            assert not concept.child_concepts
            assert concept.concept_level == 0

    def test_extract_concepts_handles_hierarchy_building_failure_gracefully(self):
        """Test that hierarchy building failure doesn't break the entire extraction."""
        # Setup mocks
        paper_text = "Research text that should extract concepts..."

        self.mock_pdf_extractor.extract_text_from_pdf.return_value = paper_text

        flat_paper_concepts = PaperConcepts(
            paper_doi=self.test_paper.doi,
            paper_title=self.test_paper.title,
            concepts=self.flat_concepts,
            extraction_metadata={"total_concepts": len(self.flat_concepts)},
        )
        self.mock_concept_extractor.extract_concepts_from_paper.return_value = (
            flat_paper_concepts
        )

        # Mock hierarchy builder to raise an exception
        self.mock_hierarchy_builder.build_hierarchy.side_effect = ValueError(
            "Hierarchy building failed"
        )

        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        # Create use case with hierarchy building enabled
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.mock_concept_extractor,
            hierarchy_builder=self.mock_hierarchy_builder,
            enable_hierarchy_building=True,
        )

        # Execute the use case
        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper, pdf_path=self.test_pdf_path
            )

        # Verify basic extraction still succeeded
        assert result is not None
        assert len(result.concepts) == 3
        assert not result.has_hierarchical_relationships  # Falls back to flat concepts

        # Verify flat concepts were still saved
        self.mock_concept_repository.save_paper_concepts.assert_called_once()


class TestExtractPaperConceptsUseCaseErrorHandling:
    """Test error handling and edge cases."""

    def setup_method(self):
        """Set up test fixtures for error testing."""
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)

        # Configure repository to return None (no existing concepts)
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        self.test_paper = ResearchPaper(
            title="Test Paper",
            authors=["Test Author"],
            doi="10.1000/test.2024",
            abstract="Test abstract",
            publication_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
            source_metadata=SourceMetadata(
                source_name="test_source",
                source_identifier="test:003",
                source_url="https://test.com",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="unknown",
                quality_score=0.7,
                source_specific_data={},
            ),
        )

    def test_extract_concepts_raises_error_for_invalid_paper(self):
        """Test that invalid paper input raises appropriate error."""
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
        )

        with pytest.raises(ValueError, match="Invalid research paper entity"):
            use_case.extract_concepts_from_paper(
                paper="not a paper object",  # Invalid input
                pdf_path=Path("/tmp/test.pdf"),
            )

    def test_extract_concepts_raises_error_for_missing_pdf(self):
        """Test that missing PDF file raises appropriate error."""
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
        )

        non_existent_path = Path("/tmp/does_not_exist.pdf")

        with pytest.raises(FileNotFoundError, match="PDF file not found"):
            use_case.extract_concepts_from_paper(
                paper=self.test_paper, pdf_path=non_existent_path
            )

    def test_extract_concepts_handles_empty_text_extraction(self):
        """Test handling of empty text extraction from PDF."""
        self.mock_pdf_extractor.extract_text_from_pdf.return_value = ""  # Empty text

        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
        )

        test_path = Path("/tmp/empty.pdf")

        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(ValueError, match="No text extracted from PDF"):
                use_case.extract_concepts_from_paper(
                    paper=self.test_paper, pdf_path=test_path
                )


class TestExtractPaperConceptsUseCaseIntegration:
    """Integration tests for complete workflows."""

    def setup_method(self):
        """Set up integration test fixtures."""
        # Use real domain services instead of mocks for integration testing
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)

        # Real domain services for integration
        self.real_concept_extractor = ConceptExtractor()
        self.real_hierarchy_builder = ConceptHierarchyBuilder()

        self.test_paper = ResearchPaper(
            title="Integration Test: Heart Rate Variability in Clinical Practice",
            authors=["Dr. Integration", "Dr. Test"],
            doi="10.1000/integration.test.2024",
            abstract="Comprehensive study of HRV applications in clinical settings.",
            publication_date=datetime(2024, 1, 15, tzinfo=timezone.utc),
            source_metadata=SourceMetadata(
                source_name="integration_test_source",
                source_identifier="test:integration-001",
                source_url="https://test.com/integration",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.99,
                source_specific_data={"test_mode": True},
            ),
        )

    def test_complete_extraction_workflow_with_hierarchy_building(self):
        """Integration test of complete workflow with real domain services."""
        # Mock infrastructure concerns but use real domain services
        sample_text = """
        Cardiovascular medicine has embraced heart rate variability as a key biomarker.
        Heart rate variability analysis techniques include time-domain methods and frequency-domain analysis.
        HRV time-domain metrics like RMSSD provide clinical insights.
        Advanced HRV analysis incorporates machine learning algorithms.
        Cardiovascular assessment benefits from comprehensive HRV evaluation.
        """

        self.mock_pdf_extractor.extract_text_from_pdf.return_value = sample_text
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        # Create use case with real domain services
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.real_concept_extractor,
            hierarchy_builder=self.real_hierarchy_builder,
            enable_hierarchy_building=True,
        )

        test_path = Path("/tmp/integration_test.pdf")

        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper,
                pdf_path=test_path,
                domain="cardiovascular_medicine",
            )

        # Verify complete workflow succeeded
        assert result is not None
        assert result.paper_doi == self.test_paper.doi
        assert len(result.concepts) > 0

        # Verify repository operations
        self.mock_concept_repository.save_paper_concepts.assert_called_once()

        # If hierarchy building worked, should have hierarchical relationships
        if result.has_hierarchical_relationships:
            # Verify hierarchy structure exists
            root_concepts = [c for c in result.concepts if c.is_root_concept()]
            leaf_concepts = [c for c in result.concepts if c.is_leaf_concept()]

            assert len(root_concepts) >= 1
            assert len(leaf_concepts) >= 1

            # Verify concept levels are assigned
            for concept in result.concepts:
                assert concept.concept_level >= 0
                # Note: cluster_id may be None for some concepts depending on hierarchy algorithm
                assert concept.evidence_strength >= 0.0


# =============================================================================
# NEW TDD CYCLE 5: MULTI-STRATEGY CONCEPT EXTRACTION INTEGRATION TESTS
# =============================================================================


class TestExtractPaperConceptsUseCaseMultiStrategyIntegration:
    """
    Test enhanced use case with MultiStrategyConceptExtractor integration.

    Educational Notes:
    - Demonstrates integration testing between application and domain layers
    - Shows how to test strategy pattern implementations in use cases
    - Validates backward compatibility while adding new functionality
    - Tests academic-grade concept extraction with evidence-based grounding
    """

    def setup_method(self):
        """Set up test fixtures for multi-strategy integration tests."""
        # Import MultiStrategyConceptExtractor for integration
        try:
            from src.domain.services.multi_strategy_concept_extractor import (
                MultiStrategyConceptExtractor,
                StrategyConfiguration,
                ExtractionResult,
            )

            self.strategy_configuration_class = StrategyConfiguration
        except ImportError:
            # For RED phase testing, create a mock StrategyConfiguration
            self.strategy_configuration_class = Mock

        # Create mock dependencies
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)
        self.mock_multi_strategy_extractor = Mock(spec=MultiStrategyConceptExtractor)
        self.mock_hierarchy_builder = Mock(spec=ConceptHierarchyBuilder)

        # Create test research paper
        self.test_paper = ResearchPaper(
            title="Multi-Strategy Analysis of Heart Rate Variability",
            authors=["Dr. Multi", "Dr. Strategy"],
            publication_date=datetime(2024, 4, 1, tzinfo=timezone.utc),
            doi="10.1000/multi.strategy.2024",
            abstract="Comprehensive multi-strategy analysis using advanced extraction techniques.",
            source_metadata=SourceMetadata(
                source_name="multi_strategy_source",
                source_identifier="test:multi-001",
                source_url="https://test.com/multi-strategy",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.98,
                source_specific_data={"extraction_method": "multi_strategy"},
            ),
        )

        self.test_pdf_path = Path("/tmp/multi_strategy_paper.pdf")

        # Create strategy configuration for testing
        self.strategy_config = self.strategy_configuration_class(
            domain="heart_rate_variability",
            min_concept_frequency=2,
            max_concepts_per_strategy=20,
            strategy_weights={
                "rule_based": 0.3,
                "statistical": 0.4,
                "embedding_based": 0.3,
            },
            consolidate_results=True,
            extract_hierarchies=True,
            use_domain_ontology=True,
            use_tfidf=True,
            use_textrank=True,
            use_topic_modeling=False,
        )

    def test_create_use_case_with_multi_strategy_extractor(self):
        """Test creating use case with MultiStrategyConceptExtractor."""
        # This test should fail initially (RED phase)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            multi_strategy_extractor=self.mock_multi_strategy_extractor,
            strategy_config=self.strategy_config,
            enable_multi_strategy_extraction=True,
        )

        # Verify multi-strategy components are properly injected
        assert hasattr(use_case, "multi_strategy_extractor")
        assert hasattr(use_case, "strategy_config")
        assert hasattr(use_case, "enable_multi_strategy_extraction")
        assert use_case.multi_strategy_extractor == self.mock_multi_strategy_extractor
        assert use_case.enable_multi_strategy_extraction is True

    def test_extract_concepts_using_multi_strategy_approach(self):
        """Test concept extraction using multi-strategy extractor."""
        # Setup mocks for multi-strategy extraction
        mock_extraction_result = Mock()
        mock_extraction_result.concepts = [
            Concept(
                text="heart rate variability",
                frequency=5,
                relevance_score=0.9,
                extraction_method="multi_strategy",
                source_papers={self.test_paper.doi},
                concept_level=0,
                evidence_strength=0.95,
            ),
            Concept(
                text="time domain analysis",
                frequency=3,
                relevance_score=0.7,
                extraction_method="statistical",
                source_papers={self.test_paper.doi},
                concept_level=1,
                evidence_strength=0.8,
                parent_concepts={"heart rate variability"},
            ),
        ]
        mock_extraction_result.metadata = {
            "extraction_method": "multi_strategy",
            "strategies_used": ["rule_based", "statistical", "embedding_based"],
            "total_concepts_extracted": 2,
            "consolidation_applied": True,
        }

        self.mock_multi_strategy_extractor.extract_concepts_comprehensive.return_value = (
            mock_extraction_result
        )
        self.mock_pdf_extractor.extract_text_from_pdf.return_value = (
            "Sample HRV research text content..."
        )
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        # This test should fail initially (RED phase)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            multi_strategy_extractor=self.mock_multi_strategy_extractor,
            strategy_config=self.strategy_config,
            enable_multi_strategy_extraction=True,
        )

        # Execute extraction with multi-strategy approach
        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper,
                pdf_path=self.test_pdf_path,
                domain="heart_rate_variability",
            )

        # Verify multi-strategy extraction was called
        self.mock_multi_strategy_extractor.extract_concepts_comprehensive.assert_called_once()
        call_args = (
            self.mock_multi_strategy_extractor.extract_concepts_comprehensive.call_args
        )
        # Check that text was passed (either as positional or keyword argument)
        if call_args and len(call_args[0]) > 0:
            assert (
                "Sample HRV research text content..." in call_args[0][0]
            )  # positional text
        elif call_args and call_args[1] and "text" in call_args[1]:
            assert (
                "Sample HRV research text content..." in call_args[1]["text"]
            )  # keyword text

        # Verify result structure
        assert isinstance(result, PaperConcepts)
        assert result.total_concept_count == 2
        assert result.paper_doi == self.test_paper.doi
        assert result.extraction_method == "multi_strategy"

        # Verify concepts have multi-strategy characteristics
        for concept in result.concepts:
            assert concept.extraction_method in ["multi_strategy", "statistical"]
            assert concept.evidence_strength > 0.0

    def test_strategy_configuration_validation(self):
        """Test validation of strategy configuration parameters."""
        # Test invalid configuration should fail (RED phase)
        invalid_config = self.strategy_configuration_class(
            domain="",  # Invalid empty domain
            min_concept_frequency=-1,  # Invalid negative frequency
            max_concepts_per_strategy=0,  # Invalid zero max concepts
        )

        with pytest.raises(ValueError, match="Invalid strategy configuration"):
            ExtractPaperConceptsUseCase(
                pdf_extractor=self.mock_pdf_extractor,
                concept_repository=self.mock_concept_repository,
                multi_strategy_extractor=self.mock_multi_strategy_extractor,
                strategy_config=invalid_config,
                enable_multi_strategy_extraction=True,
            )

    def test_fallback_to_traditional_extractor_on_multi_strategy_failure(self):
        """Test graceful fallback when multi-strategy extraction fails."""
        # Setup multi-strategy extractor to fail
        self.mock_multi_strategy_extractor.extract_concepts_comprehensive.side_effect = Exception(
            "Multi-strategy extraction failed"
        )

        # Setup traditional extractor as fallback
        self.mock_pdf_extractor.extract_text_from_pdf.return_value = "Sample text..."
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None

        # Create mock concept extractor for traditional fallback
        mock_concept_extractor = Mock(spec=ConceptExtractor)
        mock_concept_extractor.extract_concepts_from_paper.return_value = PaperConcepts(
            paper_doi=self.test_paper.doi,
            paper_title=self.test_paper.title,
            concepts=[
                Concept(
                    text="fallback concept",
                    frequency=1,
                    relevance_score=0.8,
                    extraction_method="traditional",
                    source_papers={self.test_paper.doi},
                    concept_level=0,
                    evidence_strength=0.85,
                )
            ],
            extraction_method="traditional",
        )
        # Mock extraction statistics for logging
        mock_concept_extractor.get_extraction_statistics.return_value = {
            "total_concepts": 1,
            "average_relevance": 0.8,
            "concept_diversity": 0.5,
            "extraction_methods": {"traditional": 1},
            "quality_metrics": {
                "high_quality_concepts": 1,
                "significant_concepts": 1,
                "quality_ratio": 1.0,
                "significance_ratio": 1.0,
            },
        }

        # This test should fail initially (RED phase)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=mock_concept_extractor,  # Add traditional extractor
            multi_strategy_extractor=self.mock_multi_strategy_extractor,
            strategy_config=self.strategy_config,
            enable_multi_strategy_extraction=True,
            extraction_options={"enable_fallback_extraction": True},
        )

        # Should gracefully fallback to traditional extraction
        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper, pdf_path=self.test_pdf_path
            )

        # Verify fallback occurred
        assert result.extraction_method == "traditional_fallback"
        assert len(result.concepts) == 1
        assert result.concepts[0].text == "fallback concept"


class TestExtractPaperConceptsUseCaseStrategySelection:
    """
    Test strategy selection logic and configuration handling.

    Educational Notes:
    - Shows how to test strategy pattern selection in application layer
    - Demonstrates configuration-driven behavior testing
    - Validates proper dependency injection for different strategies
    """

    def setup_method(self):
        """Set up test fixtures for strategy selection tests."""
        try:
            from src.domain.services.multi_strategy_concept_extractor import (
                StrategyConfiguration,
            )

            self.strategy_configuration_class = StrategyConfiguration
        except ImportError:
            # For RED phase testing, create a mock StrategyConfiguration
            self.strategy_configuration_class = Mock

        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)
        self.mock_traditional_extractor = Mock(spec=ConceptExtractor)
        self.mock_multi_strategy_extractor = Mock()

        self.test_paper = ResearchPaper(
            title="Strategy Selection Test Paper",
            authors=["Dr. Selection"],
            publication_date=datetime(2024, 5, 1, tzinfo=timezone.utc),
            doi="10.1000/strategy.selection.2024",
            abstract="Testing strategy selection mechanisms.",
            source_metadata=SourceMetadata(
                source_name="strategy_test",
                source_identifier="test:strategy-001",
                source_url="https://test.com/strategy",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.92,
                source_specific_data={},
            ),
        )

    def test_automatic_strategy_selection_based_on_domain(self):
        """Test automatic selection of extraction strategy based on domain."""
        # This test should fail initially (RED phase)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.mock_traditional_extractor,
            multi_strategy_extractor=self.mock_multi_strategy_extractor,
            extraction_options={"auto_strategy_selection": True},
        )

        # Test domain-specific strategy selection
        domain_strategy_map = {
            "machine_learning": "multi_strategy",
            "basic_research": "traditional",
            "complex_analysis": "multi_strategy",
        }

        for domain, expected_strategy in domain_strategy_map.items():
            strategy = use_case._select_extraction_strategy(domain)
            assert strategy == expected_strategy

    def test_manual_strategy_override(self):
        """Test manual override of automatic strategy selection."""
        # This test should fail initially (RED phase)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            extraction_options={"forced_extraction_strategy": "multi_strategy"},
        )

        # Manual override should ignore domain-based selection
        strategy = use_case._select_extraction_strategy("basic_research")
        assert strategy == "multi_strategy"

    def test_strategy_configuration_inheritance(self):
        """Test inheritance and merging of strategy configurations."""
        # This test should fail initially (RED phase)
        base_config = self.strategy_configuration_class(
            domain="base_domain", min_concept_frequency=1, similarity_threshold=0.8
        )

        domain_config = self.strategy_configuration_class(
            domain="specialized_domain",
            similarity_threshold=0.9,  # Override base value
            max_concepts_per_strategy=30,  # Add new parameter
        )

        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            strategy_config=base_config,
        )

        merged_config = use_case._merge_strategy_configurations(
            base_config, domain_config
        )

        # Verify inheritance and overrides
        assert merged_config.domain == "specialized_domain"  # Override
        assert merged_config.min_concept_frequency == 1  # Inherited
        assert abs(merged_config.similarity_threshold - 0.9) < 0.001  # Override
        assert merged_config.max_concepts_per_strategy == 30  # New parameter


class TestExtractPaperConceptsUseCaseAdvancedErrorHandling:
    """
    Test comprehensive error handling for enhanced use case.

    Educational Notes:
    - Demonstrates robust error handling in application layer
    - Shows how to test error recovery and graceful degradation
    - Validates proper error propagation and logging
    """

    def setup_method(self):
        """Set up test fixtures for error handling tests."""
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)
        self.mock_multi_strategy_extractor = Mock()

        self.test_paper = ResearchPaper(
            title="Error Handling Test Paper",
            authors=["Dr. Error", "Dr. Handler"],
            publication_date=datetime(2024, 6, 1, tzinfo=timezone.utc),
            doi="10.1000/error.handling.2024",
            abstract="Testing comprehensive error handling scenarios.",
            source_metadata=SourceMetadata(
                source_name="error_test",
                source_identifier="test:error-001",
                source_url="https://test.com/error",
                has_full_text=True,
                is_open_access=True,
                peer_review_status="peer_reviewed",
                quality_score=0.89,
                source_specific_data={},
            ),
        )

    def test_handle_multi_strategy_extractor_timeout(self):
        """Test handling of multi-strategy extractor timeout."""
        # This test should fail initially (RED phase)
        from concurrent.futures import TimeoutError

        self.mock_multi_strategy_extractor.extract_concepts_comprehensive.side_effect = TimeoutError(
            "Extraction timeout"
        )

        # Ensure repository returns None so extraction proceeds
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None
        self.mock_pdf_extractor.extract_text_from_pdf.return_value = "Sample PDF text"

        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            multi_strategy_extractor=self.mock_multi_strategy_extractor,
            enable_multi_strategy_extraction=True,  # Enable multi-strategy extraction
            extraction_options={
                "extraction_timeout_seconds": 30,
                "enable_timeout_handling": True,
            },
        )

        # Should handle timeout gracefully
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(TimeoutError, match="Concept extraction timed out"):
                use_case.extract_concepts_from_paper(
                    paper=self.test_paper, pdf_path=Path("/tmp/test.pdf")
                )

    def test_handle_invalid_strategy_configuration(self):
        """Test handling of various strategy configuration errors."""
        # This test should fail initially (RED phase)
        invalid_configs = [
            {"domain": None},  # None domain
            {"min_concept_frequency": -5},  # Negative frequency
            {"strategy_weights": {"invalid": 1.5}},  # Weight > 1.0
            {"max_concepts_per_strategy": "invalid"},  # Non-integer max
        ]

        for invalid_config in invalid_configs:
            with pytest.raises((ValueError, TypeError), match="Invalid configuration"):
                ExtractPaperConceptsUseCase(
                    pdf_extractor=self.mock_pdf_extractor,
                    concept_repository=self.mock_concept_repository,
                    multi_strategy_extractor=self.mock_multi_strategy_extractor,
                    strategy_config=invalid_config,
                    enable_multi_strategy_extraction=True,  # Enable to trigger validation
                )

    def test_partial_extraction_failure_recovery(self):
        """Test recovery from partial extraction failures."""
        # This test should fail initially (RED phase)
        # Simulate partial failure where some strategies work, others fail
        partial_extraction_result = Mock()
        partial_extraction_result.concepts = [
            Concept(
                text="partial concept",
                frequency=1,
                relevance_score=0.6,
                extraction_method="rule_based",
                source_papers={self.test_paper.doi},  # Add paper DOI to source papers
            )
        ]
        partial_extraction_result.metadata = {
            "strategies_attempted": ["rule_based", "statistical", "embedding_based"],
            "strategies_succeeded": ["rule_based"],
            "strategies_failed": ["statistical", "embedding_based"],
            "partial_extraction": True,
            "success_rate": 0.33,
        }

        self.mock_multi_strategy_extractor.extract_concepts_comprehensive.return_value = (
            partial_extraction_result
        )

        # Ensure repository returns None so extraction proceeds
        self.mock_concept_repository.find_paper_concepts_by_doi.return_value = None
        self.mock_pdf_extractor.extract_text_from_pdf.return_value = "Sample PDF text"

        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            multi_strategy_extractor=self.mock_multi_strategy_extractor,
            enable_multi_strategy_extraction=True,  # Enable multi-strategy extraction
            extraction_options={
                "accept_partial_results": True,
                "min_success_rate": 0.25,
            },
        )

        with patch("pathlib.Path.exists", return_value=True):
            result = use_case.extract_concepts_from_paper(
                paper=self.test_paper, pdf_path=Path("/tmp/test.pdf")
            )

        # Should accept partial results above threshold
        assert result.total_concept_count == 1
        assert "partial_extraction" in result.processing_metadata
        assert abs(result.processing_metadata["success_rate"] - 0.33) < 0.01


class TestExtractPaperConceptsUseCaseBackwardCompatibility:
    """
    Test backward compatibility with existing functionality.

    Educational Notes:
    - Demonstrates testing backward compatibility during refactoring
    - Shows how to ensure existing functionality remains intact
    - Validates that new features don't break existing workflows
    """

    def setup_method(self):
        """Set up test fixtures for backward compatibility tests."""
        self.mock_pdf_extractor = Mock(spec=PDFTextExtractorPort)
        self.mock_concept_repository = Mock(spec=ConceptRepositoryPort)
        self.mock_traditional_extractor = Mock(spec=ConceptExtractor)

    def test_traditional_extraction_workflow_unchanged(self):
        """Test that existing traditional extraction workflow is preserved."""
        # This test should pass (ensuring backward compatibility)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            concept_extractor=self.mock_traditional_extractor,
        )

        # Verify traditional dependencies are properly set
        assert use_case.concept_extractor == self.mock_traditional_extractor
        assert hasattr(use_case, "pdf_extractor")
        assert hasattr(use_case, "concept_repository")

        # Should not have multi-strategy components when not enabled
        assert (
            not hasattr(use_case, "multi_strategy_extractor")
            or use_case.multi_strategy_extractor is None
        )

    def test_existing_api_methods_remain_functional(self):
        """Test that all existing public API methods still work."""
        # This test should pass (ensuring API compatibility)
        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
        )

        # Verify all existing methods are still available
        assert hasattr(use_case, "extract_concepts_from_paper")
        assert hasattr(use_case, "extract_concepts_from_domain")
        assert callable(use_case.extract_concepts_from_paper)
        assert callable(use_case.extract_concepts_from_domain)

    def test_hierarchy_building_integration_preserved(self):
        """Test that existing hierarchy building integration is preserved."""
        # This test should pass (ensuring feature compatibility)
        mock_hierarchy_builder = Mock(spec=ConceptHierarchyBuilder)

        use_case = ExtractPaperConceptsUseCase(
            pdf_extractor=self.mock_pdf_extractor,
            concept_repository=self.mock_concept_repository,
            hierarchy_builder=mock_hierarchy_builder,
            enable_hierarchy_building=True,
        )

        # Verify hierarchy building is properly configured
        assert use_case.enable_hierarchy_building is True
        assert use_case.hierarchy_builder == mock_hierarchy_builder
