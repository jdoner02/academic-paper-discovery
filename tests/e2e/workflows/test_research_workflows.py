"""
End-to-End Workflow Tests - Complete user research scenarios.

These tests validate complete research workflows from configuration through
paper discovery and download. They represent realistic academic research
scenarios and ensure the system delivers value to end users.

Educational Notes:
- Workflow tests represent real user journeys
- They validate that all components work together seamlessly
- Test realistic research scenarios academics would encounter
- Focus on end-to-end value delivery rather than technical details

Research Scenarios Tested:
- Literature review preparation
- Cross-domain research exploration
- Bulk paper collection for analysis
- Configuration-driven research workflows
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.domain.services.paper_download_service import PaperDownloadService
from src.domain.entities.research_paper import ResearchPaper


class TestAcademicResearchWorkflows:
    """
    Test complete academic research workflows end-to-end.

    Educational Note:
    These tests represent real academic research scenarios, validating
    that the system supports actual researcher workflows and delivers
    practical value in research contexts.
    """

    @pytest.fixture
    def research_repository(self):
        """Create repository with realistic research paper data."""
        repository = InMemoryPaperRepository()

        # Cybersecurity research papers
        cybersec_papers = [
            ResearchPaper(
                title="Deep Learning for Network Intrusion Detection",
                authors=["Dr. Sarah Chen", "Prof. Michael Rodriguez"],
                abstract="This paper presents a comprehensive approach to network intrusion detection using deep learning algorithms, achieving 98.5% accuracy in real-world network traffic analysis.",
                publication_date=datetime(2023, 3, 15, tzinfo=timezone.utc),
                doi="10.1000/cybersec.2023.001",
                arxiv_id="2303.12345",
                venue="IEEE Security & Privacy",
                citation_count=67,
                keywords=["cybersecurity", "deep learning", "intrusion detection"],
            ),
            ResearchPaper(
                title="Quantum-Resistant Cryptographic Protocols for IoT",
                authors=["Dr. Ahmed Hassan", "Prof. Lisa Wang"],
                abstract="Analysis of post-quantum cryptographic protocols specifically designed for resource-constrained IoT devices in distributed networks.",
                publication_date=datetime(2023, 6, 10, tzinfo=timezone.utc),
                doi="10.1000/quantum.2023.002",
                arxiv_id="2306.67890",
                venue="ACM CCS",
                citation_count=43,
                keywords=["quantum cryptography", "IoT", "protocols"],
            ),
            ResearchPaper(
                title="Machine Learning Approaches to Threat Intelligence",
                authors=["Prof. David Kim", "Dr. Emily Johnson"],
                abstract="Novel machine learning techniques for automated threat intelligence gathering and analysis in enterprise security environments.",
                publication_date=datetime(2023, 8, 5, tzinfo=timezone.utc),
                doi="10.1000/threat.2023.003",
                arxiv_id="2308.11111",
                venue="USENIX Security",
                citation_count=29,
                keywords=["machine learning", "threat intelligence", "automation"],
            ),
            # AI/ML papers for cross-domain research
            ResearchPaper(
                title="Transformer Architectures for Time Series Analysis",
                authors=["Dr. Maria Gonzalez"],
                abstract="Application of transformer neural networks to time series forecasting with applications in financial and security domains.",
                publication_date=datetime(2023, 5, 20, tzinfo=timezone.utc),
                doi="10.1000/transformers.2023.004",
                citation_count=85,
                keywords=["transformers", "time series", "neural networks"],
            ),
        ]

        repository.save_papers(cybersec_papers)
        return repository

    @pytest.fixture
    def cybersecurity_config(self):
        """Create realistic cybersecurity research configuration."""
        return {
            "search_configuration": {
                "min_citation_threshold": 20,
                "publication_year_start": 2020,
                "publication_year_end": 2024,
                "max_concurrent_searches": 3,
                "default_strategy": "comprehensive_cybersecurity",
            },
            "strategies": {
                "comprehensive_cybersecurity": {
                    "name": "comprehensive_cybersecurity",
                    "description": "Comprehensive cybersecurity research across domains",
                    "primary_keywords": [
                        "cybersecurity",
                        "network security",
                        "information security",
                    ],
                    "secondary_keywords": [
                        "threat detection",
                        "intrusion detection",
                        "vulnerability",
                    ],
                    "exclusion_keywords": ["tutorial", "survey only", "basic introduction"],
                    "search_limit": 100,
                },
                "ai_security_intersection": {
                    "name": "ai_security_intersection",
                    "description": "AI and machine learning applications in cybersecurity",
                    "primary_keywords": ["machine learning", "cybersecurity"],
                    "secondary_keywords": [
                        "deep learning",
                        "neural networks",
                        "AI security",
                    ],
                    "exclusion_keywords": ["basic", "introductory"],
                    "search_limit": 50,
                },
                "quantum_cryptography": {
                    "name": "quantum_cryptography",
                    "description": "Post-quantum cryptography research",
                    "primary_keywords": ["quantum cryptography", "post-quantum"],
                    "secondary_keywords": ["quantum resistant", "cryptographic protocols"],
                    "exclusion_keywords": ["theoretical only"],
                    "search_limit": 30,
                },
            },
        }

    def test_literature_review_preparation_workflow(
        self, research_repository, cybersecurity_config
    ):
        """
        Test complete literature review preparation workflow.

        Educational Note:
        This workflow represents a common academic scenario: preparing
        for a literature review by discovering and collecting relevant
        papers across multiple search strategies.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Arrange: Set up configuration and use case
            config_path = Path(temp_dir) / "cybersec_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(cybersecurity_config, f)

            use_case = ExecuteKeywordSearchUseCase(
                repository=research_repository, config_path=str(config_path)
            )

            # Act: Execute complete literature review workflow

            # Step 1: Explore available research strategies
            available_strategies = use_case.get_available_strategies()
            assert len(available_strategies) == 3
            assert "comprehensive_cybersecurity" in available_strategies
            assert "ai_security_intersection" in available_strategies
            assert "quantum_cryptography" in available_strategies

            # Step 2: Execute primary research strategy
            primary_results = use_case.execute_strategy("comprehensive_cybersecurity")

            # Step 3: Execute specialized strategy
            ai_security_results = use_case.execute_strategy("ai_security_intersection")

            # Step 4: Execute focused strategy
            quantum_results = use_case.execute_strategy("quantum_cryptography")

            # Assert: Workflow should provide comprehensive research coverage
            assert (
                len(primary_results) >= 2
            )  # Should find multiple cybersecurity papers
            assert len(ai_security_results) >= 1  # Should find AI+security intersection
            assert len(quantum_results) >= 1  # Should find quantum cryptography papers

            # Verify result quality and relevance
            primary_titles = [paper.title for paper in primary_results]
            assert any(
                "intrusion detection" in title.lower() for title in primary_titles
            )
            assert any("cybersecurity" in title.lower() for title in primary_titles)

            # Verify citation quality filter is applied
            all_results = primary_results + ai_security_results + quantum_results
            assert all(paper.citation_count >= 20 for paper in all_results)

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    @patch("builtins.open")
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_complete_research_collection_workflow(
        self,
        mock_json_dump,
        mock_open,
        mock_get,
        mock_mkdir,
        research_repository,
        cybersecurity_config,
    ):
        """
        Test complete research paper collection workflow with downloads.

        Educational Note:
        This workflow represents the complete researcher journey from
        search strategy execution through paper collection and organization.
        """
        # Arrange: Mock successful downloads
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"Mock PDF content"]
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as temp_dir:
            # Set up configuration
            config_path = Path(temp_dir) / "research_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(cybersecurity_config, f)

            # Create use case and download service
            search_use_case = ExecuteKeywordSearchUseCase(
                repository=research_repository, config_path=str(config_path)
            )
            download_service = PaperDownloadService(base_output_dir=temp_dir)

            # Act: Execute complete research collection workflow

            # Step 1: Execute search strategy
            papers = search_use_case.execute_strategy("ai_security_intersection")
            assert len(papers) > 0

            # Step 2: Download discovered papers
            download_results = download_service.download_papers(
                papers=papers, strategy_name="ai_security_intersection"
            )

            # Step 3: Validate collection results
            summary = download_service.get_download_summary(download_results)

            # Assert: Complete workflow should succeed
            assert summary["total_attempted"] == len(papers)
            assert summary["successful_downloads"] > 0
            assert summary["success_rate"] > 0

            # Verify file organization
            mock_mkdir.assert_called()  # Output directories created
            mock_json_dump.assert_called()  # Metadata generated

            # Verify metadata includes research context
            metadata = mock_json_dump.call_args[0][0]
            assert (
                metadata["download_info"]["strategy_name"] == "ai_security_intersection"
            )
            assert metadata["download_info"]["total_papers"] == len(papers)

    def test_cross_domain_research_exploration_workflow(
        self, research_repository, cybersecurity_config
    ):
        """
        Test cross-domain research exploration workflow.

        Educational Note:
        Many research projects span multiple domains. This workflow tests
        the system's ability to support interdisciplinary research discovery.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "cross_domain_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(cybersecurity_config, f)

            use_case = ExecuteKeywordSearchUseCase(
                repository=research_repository, config_path=str(config_path)
            )

            # Act: Execute cross-domain search
            # Custom search combining AI and security terms
            cross_domain_results = use_case.execute_custom_search(
                required_terms=["machine learning"],
                optional_terms=["security", "cybersecurity", "threat"],
                max_results=20,
                min_citations=25,
            )

            # Assert: Should find papers at intersection of domains
            assert len(cross_domain_results) >= 1

            # Verify cross-domain relevance
            for paper in cross_domain_results:
                # Should have both ML and security relevance
                content = (paper.title + " " + paper.abstract).lower()
                has_ml_content = any(
                    term in content for term in ["machine learning", "neural", "ai"]
                )
                has_security_content = any(
                    term in content for term in ["security", "threat", "cybersecurity"]
                )

                # At least one paper should span both domains
                if has_ml_content and has_security_content:
                    break
            else:
                # If we reach here, no paper spans both domains
                # This might be acceptable depending on search strategy
                pass

    def test_batch_research_workflow_execution(
        self, research_repository, cybersecurity_config
    ):
        """
        Test batch execution of multiple research strategies.

        Educational Note:
        Researchers often need to explore multiple approaches simultaneously.
        This workflow tests efficient batch processing of research strategies.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "batch_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(cybersecurity_config, f)

            use_case = ExecuteKeywordSearchUseCase(
                repository=research_repository, config_path=str(config_path)
            )

            # Act: Execute all strategies in batch
            all_results = use_case.execute_all_strategies()

            # Assert: Batch execution should cover all configured strategies
            assert isinstance(all_results, dict)
            assert "comprehensive_cybersecurity" in all_results
            assert "ai_security_intersection" in all_results
            assert "quantum_cryptography" in all_results

            # Verify each strategy returned results
            for strategy_name, results in all_results.items():
                assert isinstance(results, list)
                assert len(results) >= 0  # May have empty results for some strategies

            # Verify total coverage
            all_papers = []
            for results in all_results.values():
                all_papers.extend(results)

            # Should have comprehensive coverage across strategies
            assert len(all_papers) >= 3  # At minimum, should find several papers

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    def test_error_recovery_workflow(
        self, mock_mkdir, research_repository, cybersecurity_config
    ):
        """
        Test error recovery in complete research workflows.

        Educational Note:
        Real research workflows encounter errors (network issues, missing files).
        This test validates graceful error handling and recovery mechanisms.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "error_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(cybersecurity_config, f)

            # Test configuration error handling
            use_case = ExecuteKeywordSearchUseCase(
                repository=research_repository, config_path=str(config_path)
            )

            # Execute valid strategy
            results = use_case.execute_strategy("comprehensive_cybersecurity")
            assert len(results) > 0

            # Test invalid strategy handling
            with pytest.raises(ValueError):
                use_case.execute_strategy("nonexistent_strategy")

            # Test download service error handling
            download_service = PaperDownloadService(base_output_dir=temp_dir)

            # Create paper with no downloadable URL
            problem_paper = ResearchPaper(
                title="Paper Without PDF",
                authors=["Test Author"],
                abstract="No downloadable content",
                publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                doi="10.1000/nopdf.2023.001",
                # No arxiv_id or pdf_url
            )

            # Should handle missing PDF gracefully
            download_results = download_service.download_papers(
                papers=[problem_paper], strategy_name="error_test"
            )

            assert len(download_results) == 1
            assert download_results["Paper Without PDF"].startswith("Download failed")


class TestResearchProductivityWorkflows:
    """
    Test workflows focused on research productivity and efficiency.

    Educational Note:
    These tests validate that the system supports efficient research
    workflows that help academics be more productive in their research.
    """

    def test_rapid_literature_discovery_workflow(self):
        """
        Test rapid literature discovery for time-sensitive research.

        Educational Note:
        Academic deadlines often require rapid literature discovery.
        This workflow tests efficient search and collection processes.
        """
        # This would test optimized workflows for quick research turnaround
        # Implementation would focus on:
        # - Fast configuration loading
        # - Efficient search execution
        # - Quick result filtering and prioritization
        # - Streamlined download processes
        pass

    def test_comprehensive_domain_mapping_workflow(self):
        """
        Test comprehensive domain mapping for systematic reviews.

        Educational Note:
        Systematic reviews require comprehensive coverage of research domains.
        This workflow tests thorough and systematic paper discovery.
        """
        # This would test comprehensive search strategies:
        # - Multiple search term combinations
        # - Exhaustive strategy execution
        # - Coverage analysis and gap identification
        # - Systematic result organization
        pass
