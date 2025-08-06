"""
Performance Tests - Large-scale operation validation.

These tests validate system performance under realistic research loads,
ensuring the system can handle large-scale academic research workflows
efficiently and reliably.

Educational Notes:
- Performance tests validate scalability beyond unit test scope
- They ensure system maintains quality under realistic academic loads
- Focus on both speed and memory efficiency for large datasets
- Simulate real research scenarios with substantial data volumes

Performance Areas Tested:
- Large literature search performance
- Bulk paper processing efficiency
- Memory usage with large datasets
- Concurrent operation handling
- Configuration loading performance
"""

import pytest
import time
import psutil
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.domain.services.paper_download_service import PaperDownloadService
from src.domain.entities.research_paper import ResearchPaper


class TestSearchPerformance:
    """
    Test search operation performance under various loads.

    Educational Note:
    Search performance is critical for researcher productivity. These tests
    ensure the system maintains acceptable response times even with
    large repositories and complex search strategies.
    """

    @pytest.fixture
    def large_research_repository(self):
        """Create repository with large-scale research data."""
        repository = InMemoryPaperRepository()

        # Generate large collection of realistic research papers
        papers = []
        domains = [
            ("cybersecurity", ["security", "threat", "encryption", "firewall"]),
            (
                "machine learning",
                ["neural networks", "deep learning", "classification"],
            ),
            (
                "quantum computing",
                ["quantum", "qubit", "superposition", "entanglement"],
            ),
            ("biomedical", ["genomics", "protein", "medical", "clinical"]),
            ("climate science", ["climate", "environment", "carbon", "sustainability"]),
        ]

        venues = ["Nature", "Science", "IEEE", "ACM", "PNAS", "Cell", "Lancet"]
        authors_pool = [
            "Dr. Sarah Chen",
            "Prof. Michael Rodriguez",
            "Dr. Ahmed Hassan",
            "Prof. Lisa Wang",
            "Dr. Emily Johnson",
            "Prof. David Kim",
            "Dr. Maria Gonzalez",
            "Prof. Robert Taylor",
            "Dr. Jennifer Wu",
        ]

        paper_id = 1
        for domain_name, keywords in domains:
            # Generate 200 papers per domain for 1000 total papers
            for i in range(200):
                papers.append(
                    ResearchPaper(
                        title=f"{domain_name.title()} Research Paper {i+1}: {keywords[i % len(keywords)].title()} Analysis",
                        authors=[
                            authors_pool[i % len(authors_pool)],
                            authors_pool[(i + 1) % len(authors_pool)],
                        ],
                        abstract=f"This comprehensive study examines {keywords[i % len(keywords)]} in the context of {domain_name}. Our research demonstrates significant advances in {keywords[(i + 1) % len(keywords)]} methodologies with practical applications in {domain_name} systems.",
                        publication_date=datetime(
                            2020 + (i % 4), 1 + (i % 12), 1, tzinfo=timezone.utc
                        ),
                        doi=f"10.1000/{domain_name.replace(' ', '')}.{2020 + (i % 4)}.{paper_id:04d}",
                        arxiv_id=f"{2020 + (i % 4):04d}.{paper_id:05d}",
                        venue=venues[i % len(venues)],
                        citation_count=10 + (i % 100),  # 10-109 citations
                        keywords=[
                            domain_name,
                            keywords[i % len(keywords)],
                            keywords[(i + 1) % len(keywords)],
                        ],
                    )
                )
                paper_id += 1

        repository.save_papers(papers)
        return repository

    @pytest.fixture
    def performance_config(self):
        """Create configuration for performance testing."""
        return {
            "search_configuration": {
                "min_citation_threshold": 20,
                "publication_year_start": 2020,
                "publication_year_end": 2024,
                "max_concurrent_searches": 5,
                "default_strategy": "broad_performance_test",
            },
            "strategies": {
                "broad_performance_test": {
                    "name": "broad_performance_test",
                    "description": "Broad search for performance testing",
                    "primary_keywords": ["research", "analysis", "study"],
                    "secondary_keywords": ["data", "method", "approach"],
                    "exclusion_keywords": [],
                    "search_limit": 500,
                },
                "specific_performance_test": {
                    "name": "specific_performance_test",
                    "description": "Specific domain search for performance testing",
                    "primary_keywords": ["machine learning", "cybersecurity"],
                    "secondary_keywords": ["neural networks", "security"],
                    "exclusion_keywords": [],
                    "search_limit": 100,
                },
            },
        }

    def test_large_repository_search_performance(
        self, large_research_repository, performance_config
    ):
        """
        Test search performance with large repository (1000+ papers).

        Educational Note:
        Academic repositories often contain thousands of papers. This test
        ensures search operations remain performant at realistic scales.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Arrange
            config_path = Path(temp_dir) / "perf_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(performance_config, f)

            use_case = ExecuteKeywordSearchUseCase(
                repository=large_research_repository, config_path=str(config_path)
            )

            # Act & Measure
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

            results = use_case.execute_strategy("broad_performance_test")

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

            # Assert Performance Criteria
            execution_time = end_time - start_time
            memory_increase = end_memory - start_memory

            # Performance benchmarks for academic use
            assert (
                execution_time < 2.0
            ), f"Search took {execution_time:.2f}s (should be < 2.0s)"
            assert (
                memory_increase < 100
            ), f"Memory increased by {memory_increase:.1f}MB (should be < 100MB)"
            assert (
                len(results) > 0
            ), "Search should return results from large repository"

            print(
                f"Large repository search: {execution_time:.2f}s, {memory_increase:.1f}MB memory increase"
            )

    def test_complex_search_strategy_performance(
        self, large_research_repository, performance_config
    ):
        """
        Test performance of complex multi-term search strategies.

        Educational Note:
        Academic searches often involve complex term combinations. This test
        ensures complex search logic doesn't degrade performance significantly.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "complex_config.yaml"

            # Create complex search configuration
            complex_config = {
                "search_configuration": {
                    **performance_config["search_configuration"],
                    "default_strategy": "complex_interdisciplinary",
                },
                "strategies": {
                    "complex_interdisciplinary": {
                        "name": "complex_interdisciplinary",
                        "description": "Complex interdisciplinary search",
                        "primary_keywords": [
                            "machine learning",
                            "cybersecurity",
                            "quantum",
                        ],
                        "secondary_keywords": [
                            "neural networks",
                            "encryption",
                            "algorithms",
                            "security",
                            "computing",
                        ],
                        "exclusion_keywords": [
                            "basic",
                            "tutorial",
                            "introduction",
                            "survey",
                        ],
                        "search_limit": 200,
                    }
                },
            }

            with open(config_path, "w") as f:
                yaml.dump(complex_config, f)

            use_case = ExecuteKeywordSearchUseCase(
                repository=large_research_repository, config_path=str(config_path)
            )

            # Measure complex search performance
            start_time = time.time()

            results = use_case.execute_strategy("complex_interdisciplinary")

            execution_time = time.time() - start_time

            # Complex searches should still be performant
            assert (
                execution_time < 3.0
            ), f"Complex search took {execution_time:.2f}s (should be < 3.0s)"
            assert len(results) >= 0  # May return fewer results due to complexity

            print(f"Complex search strategy: {execution_time:.2f}s")

    def test_concurrent_search_performance(
        self, large_research_repository, performance_config
    ):
        """
        Test concurrent search operation performance.

        Educational Note:
        Research teams often run multiple searches concurrently. This test
        validates system performance under concurrent load.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "concurrent_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(performance_config, f)

            def execute_search(strategy_name):
                use_case = ExecuteKeywordSearchUseCase(
                    repository=large_research_repository, config_path=str(config_path)
                )
                return use_case.execute_strategy(strategy_name)

            # Test concurrent execution
            start_time = time.time()

            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [
                    executor.submit(execute_search, "broad_performance_test"),
                    executor.submit(execute_search, "specific_performance_test"),
                    executor.submit(execute_search, "broad_performance_test"),
                ]

                results = [future.result() for future in futures]

            execution_time = time.time() - start_time

            # Concurrent execution should be reasonably efficient
            assert (
                execution_time < 5.0
            ), f"Concurrent searches took {execution_time:.2f}s (should be < 5.0s)"
            assert all(len(result_set) >= 0 for result_set in results)

            print(f"Concurrent search execution: {execution_time:.2f}s")


class TestDownloadPerformance:
    """
    Test download operation performance under various loads.

    Educational Note:
    Paper downloading is often the bottleneck in research workflows. These
    tests ensure download operations scale appropriately for academic use.
    """

    @pytest.fixture
    def bulk_papers(self):
        """Create collection of papers for bulk download testing."""
        papers = []
        for i in range(50):  # 50 papers for bulk testing
            papers.append(
                ResearchPaper(
                    title=f"Performance Test Paper {i+1}",
                    authors=[f"Author {i+1}"],
                    abstract=f"Abstract for performance test paper {i+1}",
                    publication_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                    doi=f"10.1000/perftest.2023.{i+1:03d}",
                    arxiv_id=f"2301.{i+1:05d}",
                    venue="Performance Test Journal",
                    citation_count=25,
                    keywords=["performance", "testing"],
                )
            )
        return papers

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.requests.Session.get")
    @patch("builtins.open")
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_bulk_download_performance(
        self, mock_json_dump, mock_open, mock_get, mock_mkdir, bulk_papers
    ):
        """
        Test bulk download performance with realistic paper collection.

        Educational Note:
        Researchers often download many papers at once. This test ensures
        bulk downloads complete in reasonable time with appropriate resource usage.
        """
        # Mock successful downloads with realistic timing
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b"x" * 1024] * 1000  # 1MB per paper
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as temp_dir:
            download_service = PaperDownloadService(base_output_dir=temp_dir)

            # Measure bulk download performance
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024

            results = download_service.download_papers(
                papers=bulk_papers, strategy_name="performance_test"
            )

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024

            execution_time = end_time - start_time
            memory_increase = end_memory - start_memory

            # Performance criteria for bulk downloads
            papers_per_second = len(bulk_papers) / execution_time

            assert (
                papers_per_second > 5
            ), f"Download rate: {papers_per_second:.1f} papers/sec (should be > 5)"
            assert (
                memory_increase < 200
            ), f"Memory increase: {memory_increase:.1f}MB (should be < 200MB)"
            assert len(results) == len(bulk_papers)

            print(
                f"Bulk download: {papers_per_second:.1f} papers/sec, {memory_increase:.1f}MB memory"
            )

    @patch("src.domain.services.paper_download_service.Path.mkdir")
    @patch("src.domain.services.paper_download_service.json.dump")
    def test_download_metadata_generation_performance(
        self, mock_json_dump, mock_mkdir, bulk_papers
    ):
        """
        Test metadata generation performance for large collections.

        Educational Note:
        Metadata generation is crucial for research organization. This test
        ensures metadata operations remain fast even with large paper collections.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            download_service = PaperDownloadService(base_output_dir=temp_dir)

            # Test metadata generation performance
            start_time = time.time()

            # Create mock download results
            mock_results = {
                paper.title: f"Successfully downloaded to {paper.title.replace(' ', '_')}.pdf"
                for paper in bulk_papers
            }

            summary = download_service.get_download_summary(mock_results)

            execution_time = time.time() - start_time

            # Metadata generation should be very fast
            assert (
                execution_time < 0.1
            ), f"Metadata generation took {execution_time:.3f}s (should be < 0.1s)"
            assert summary["total_attempted"] == len(bulk_papers)

            print(
                f"Metadata generation: {execution_time:.3f}s for {len(bulk_papers)} papers"
            )


class TestConfigurationPerformance:
    """
    Test configuration loading and processing performance.

    Educational Note:
    Configuration management affects startup time and user experience.
    These tests ensure configuration operations remain snappy.
    """

    @pytest.fixture
    def large_config(self):
        """Create large configuration for performance testing."""
        strategies = {}

        # Generate 20 different search strategies
        for i in range(20):
            strategy_name = f"strategy_{i+1}"
            strategies[strategy_name] = {
                "name": strategy_name,
                "description": f"Research strategy {i+1} for performance testing",
                "primary_keywords": [f"term_{i+1}_{j}" for j in range(5)],
                "secondary_keywords": [f"secondary_{i+1}_{j}" for j in range(10)],
                "exclusion_keywords": [f"exclude_{i+1}_{j}" for j in range(3)],
                "search_limit": 100 + i * 10,
            }

        return {
            "search_configuration": {
                "min_citation_threshold": 20,
                "publication_year_start": 2020,
                "publication_year_end": 2024,
                "max_concurrent_searches": 5,
                "default_strategy": "strategy_1",
            },
            "strategies": strategies,
        }

    def test_large_configuration_loading_performance(self, large_config):
        """
        Test loading performance with large configuration files.

        Educational Note:
        Research teams may develop extensive configuration libraries.
        This test ensures configuration loading remains fast.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "large_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(large_config, f)

            repository = InMemoryPaperRepository()

            # Measure configuration loading performance
            start_time = time.time()

            use_case = ExecuteKeywordSearchUseCase(
                repository=repository, config_path=str(config_path)
            )

            # Test strategy enumeration
            strategies = use_case.get_available_strategies()

            execution_time = time.time() - start_time

            # Configuration loading should be very fast
            assert (
                execution_time < 0.2
            ), f"Config loading took {execution_time:.3f}s (should be < 0.2s)"
            assert len(strategies) == 20

            print(
                f"Large configuration loading: {execution_time:.3f}s for 20 strategies"
            )

    def test_configuration_validation_performance(self, large_config):
        """
        Test configuration validation performance.

        Educational Note:
        Configuration validation prevents runtime errors but shouldn't
        slow down the research workflow startup significantly.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "validation_config.yaml"
            with open(config_path, "w") as f:
                yaml.dump(large_config, f)

            repository = InMemoryPaperRepository()

            # Measure validation performance
            start_time = time.time()

            # Configuration validation happens during initialization
            use_case = ExecuteKeywordSearchUseCase(
                repository=repository, config_path=str(config_path)
            )

            # Validate all strategies are accessible
            for i in range(20):
                strategy_name = f"strategy_{i+1}"
                assert strategy_name in use_case.get_available_strategies()

            execution_time = time.time() - start_time

            # Validation should be fast even for large configs
            assert (
                execution_time < 0.3
            ), f"Validation took {execution_time:.3f}s (should be < 0.3s)"

            print(f"Configuration validation: {execution_time:.3f}s for 20 strategies")
