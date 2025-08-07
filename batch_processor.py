#!/usr/bin/env python3
"""
Batch Processing Module for Research Paper Aggregation

This module implements comprehensive batch processing functionality that:
1. Processes all YAML configuration files in the config/ directory
2. Executes all strategies within each configuration
3. Organizes results into outputs/config_name/strategy_name/ structure
4. Ensures maximum 100 papers per strategy with deduplication
5. Stores results in JSON format for further processing
6. Extracts concepts from downloaded PDFs for GUI visualization

Educational Notes:
- Demonstrates batch processing patterns in Clean Architecture
- Shows file system organization for research data management
- Implements deduplication algorithms for paper collections
- Uses JSON serialization for persistent storage
- Follows Domain-Driven Design principles for academic research
- Integrates concept extraction for enhanced research insights

Design Patterns Applied:
- Strategy Pattern: Different search strategies within configurations
- Repository Pattern: Abstract data access for different sources
- Factory Pattern: Dynamic configuration loading
- Observer Pattern: Progress tracking and logging
- Dependency Injection: Testable concept extraction components

SOLID Principles Demonstrated:
- Single Responsibility: Each function has one clear purpose
- Open/Closed: Easy to extend with new configuration formats and concept extraction methods
- Dependency Inversion: Depends on abstractions, not concrete implementations
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import yaml
import logging

# Add src to path for imports
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.domain.value_objects.keyword_config import KeywordConfig
from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.infrastructure.repositories.arxiv_paper_repository import ArxivPaperRepository
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from src.domain.entities.research_paper import ResearchPaper

# Concept extraction imports (with graceful fallback)
try:
    from src.application.use_cases.extract_paper_concepts_use_case import (
        ExtractPaperConceptsUseCase,
    )
    from src.domain.services.concept_extractor import ConceptExtractor
    from src.domain.services.concept_hierarchy_builder import ConceptHierarchyBuilder
    from src.infrastructure.pdf_extractor import PyPDF2TextExtractor
    from src.infrastructure.json_concept_repository import JSONConceptRepository

    CONCEPT_EXTRACTION_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Concept extraction components not available: {e}")
    CONCEPT_EXTRACTION_AVAILABLE = False


class BatchProcessor:
    """
    Comprehensive batch processing system for research paper aggregation with concept extraction.

    This class demonstrates several important Computer Science concepts:

    Design Pattern: Command Pattern
    - Encapsulates batch processing operations as objects
    - Allows for queuing, logging, and undo operations
    - Separates invoker (CLI) from receiver (actual processing logic)

    Educational Notes:
    - Shows proper file system operations with pathlib
    - Implements progress tracking for long-running operations
    - Uses JSON for cross-platform data interchange
    - Demonstrates error handling in batch operations
    - Integrates concept extraction for enhanced research insights

    Real-world Applications:
    - ETL (Extract, Transform, Load) pipelines
    - Academic research data processing
    - Content management systems
    - Document processing workflows
    - Research concept discovery and visualization
    """

    def __init__(
        self,
        config_dir: str = "config",
        output_dir: str = "outputs",
        max_papers: int = 100,
        enable_concept_extraction: bool = False,
        concept_extractor=None,
        hierarchy_builder=None,
    ):
        """
        Initialize batch processor with configuration and output paths.

        Args:
            config_dir: Directory containing YAML configuration files
            output_dir: Base directory for organized output structure
            max_papers: Maximum papers to store per strategy (for performance)
            enable_concept_extraction: Whether to extract concepts from downloaded papers
            concept_extractor: Optional custom concept extractor (for testing)
            hierarchy_builder: Optional custom hierarchy builder (for testing)

        Educational Notes:
        - Uses pathlib for cross-platform file operations
        - Initializes data structures for deduplication tracking
        - Sets up logging for audit trail and debugging
        - Supports optional concept extraction for enhanced functionality
        """
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.max_papers = max_papers

        # Concept extraction configuration
        self.enable_concept_extraction = enable_concept_extraction
        self._concept_extractor = concept_extractor
        self._hierarchy_builder = hierarchy_builder

        self.processed_papers: Set[str] = set()  # Track DOIs for deduplication
        self.processing_stats = {
            "configs_processed": 0,
            "strategies_processed": 0,
            "papers_found": 0,
            "papers_stored": 0,
            "duplicates_filtered": 0,
            "concepts_extracted": 0,
            "errors": [],
        }

    def discover_configurations(self) -> Dict[str, Path]:
        """
        Discover all YAML configuration files in the config directory.

        Returns:
            Dictionary mapping config name to file path

        Educational Notes:
        - Uses pathlib glob patterns for file discovery
        - Handles missing directories gracefully
        - Creates user-friendly names from file paths
        - Demonstrates defensive programming practices
        """
        if not self.config_dir.exists():
            raise FileNotFoundError(
                f"Configuration directory not found: {self.config_dir}"
            )

        configs = {}
        for config_file in self.config_dir.glob("*.yaml"):
            # Use stem (filename without extension) as config name
            config_name = config_file.stem
            configs[config_name] = config_file

        return configs

    def load_configuration(self, config_path: Path) -> KeywordConfig:
        """
        Load a keyword configuration from YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            Loaded KeywordConfig object

        Raises:
            Exception: If configuration cannot be loaded or parsed

        Educational Notes:
        - Demonstrates proper exception handling with context
        - Uses domain objects (KeywordConfig) for type safety
        - Shows how to wrap external library exceptions
        """
        try:
            return KeywordConfig.from_yaml_file(str(config_path))
        except Exception as e:
            error_msg = f"Failed to load configuration {config_path}: {e}"
            self.processing_stats["errors"].append(error_msg)
            raise Exception(error_msg) from e

    def create_output_structure(self, config_name: str, strategy_name: str) -> Path:
        """
        Create the organized output directory structure.

        Args:
            config_name: Name of the configuration (e.g., 'heart_rate_variability')
            strategy_name: Name of the strategy (e.g., 'comprehensive_hrv_research')

        Returns:
            Path to the created strategy directory

        Educational Notes:
        - Creates nested directory structure as required
        - Uses pathlib for cross-platform compatibility
        - Implements the exact folder structure specified in requirements
        - Handles existing directories gracefully
        - Creates PDFs subdirectory for concept extraction compatibility
        """
        strategy_dir = self.output_dir / config_name / strategy_name
        strategy_dir.mkdir(parents=True, exist_ok=True)

        # Create PDFs subdirectory for downloaded papers (concept extraction compatibility)
        pdfs_dir = strategy_dir / "pdfs"
        pdfs_dir.mkdir(exist_ok=True)

        return strategy_dir

    def deduplicate_papers(self, papers: List[ResearchPaper]) -> List[ResearchPaper]:
        """
        Remove duplicate papers based on DOI and maintain most recent papers.

        Args:
            papers: List of research papers to deduplicate

        Returns:
            List of unique papers, sorted by publication date (most recent first)

        Educational Notes:
        - Implements deduplication algorithm using DOI as unique identifier
        - Handles papers without DOIs by using title similarity
        - Sorts by publication date to ensure most recent papers are kept
        - Updates global tracking set to prevent cross-strategy duplicates
        """
        unique_papers = []
        local_dois = set()

        # Sort papers by publication date (most recent first)
        sorted_papers = sorted(papers, key=lambda p: p.publication_date, reverse=True)

        for paper in sorted_papers:
            # Use DOI as primary deduplication key
            paper_key = (
                paper.doi if paper.doi else f"title:{paper.title.lower().strip()}"
            )

            # Check both local (within this batch) and global (across all strategies) duplicates
            if paper_key not in local_dois and paper_key not in self.processed_papers:
                unique_papers.append(paper)
                local_dois.add(paper_key)
                self.processed_papers.add(paper_key)

                # Respect maximum papers limit
                if len(unique_papers) >= self.max_papers:
                    break
            else:
                self.processing_stats["duplicates_filtered"] += 1

        return unique_papers

    def serialize_papers(self, papers: List[ResearchPaper]) -> List[Dict]:
        """
        Convert ResearchPaper objects to JSON-serializable dictionaries.

        Args:
            papers: List of ResearchPaper domain objects

        Returns:
            List of dictionaries ready for JSON serialization

        Educational Notes:
        - Demonstrates data transformation between domain and infrastructure layers
        - Handles datetime serialization for JSON compatibility
        - Preserves all important research paper metadata
        - Uses ISO format for dates to ensure cross-platform compatibility
        """
        serialized = []
        for paper in papers:
            paper_dict = {
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "publication_date": (
                    paper.publication_date.isoformat()
                    if paper.publication_date
                    else None
                ),
                "doi": paper.doi,
                "venue": paper.venue,
                "citation_count": paper.citation_count,
                "keywords": paper.keywords,
                "url": getattr(paper, "url", None),  # Handle optional URL field
            }
            serialized.append(paper_dict)
        return serialized

    def _get_existing_metadata(self, metadata_file: Path) -> dict:
        """
        Load existing metadata for incremental updates.

        Args:
            metadata_file: Path to metadata.json file

        Returns:
            Dictionary containing existing metadata, or empty structure if file doesn't exist

        Educational Notes:
        - Enables idempotent operations by preserving existing download history
        - Handles missing files gracefully for first-time runs
        - Returns consistent structure for reliable merging
        """
        if not metadata_file.exists():
            return {
                "downloaded_papers": {},
                "processing_metadata": {},
                "strategy_metadata": {},
                "file_structure": {},
            }

        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                existing_metadata = json.load(f)

            # Ensure downloaded_papers exists and is a dictionary
            if "downloaded_papers" not in existing_metadata:
                existing_metadata["downloaded_papers"] = {}
            elif isinstance(existing_metadata["downloaded_papers"], list):
                # Convert old list format to new dictionary format
                old_list = existing_metadata["downloaded_papers"]
                existing_metadata["downloaded_papers"] = {}
                for paper_key in old_list:
                    existing_metadata["downloaded_papers"][paper_key] = {
                        "download_date": existing_metadata.get(
                            "last_download_date", "unknown"
                        ),
                        "legacy_entry": True,
                    }

            return existing_metadata

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"    ⚠️  Could not load existing metadata: {e}")
            return {
                "downloaded_papers": {},
                "processing_metadata": {},
                "strategy_metadata": {},
                "file_structure": {},
            }

    def _should_download_paper(
        self, paper: ResearchPaper, existing_metadata: dict
    ) -> bool:
        """
        Check if a paper should be downloaded based on existing metadata.

        Args:
            paper: Research paper to check
            existing_metadata: Existing metadata containing downloaded papers

        Returns:
            True if paper should be downloaded, False if already downloaded

        Educational Notes:
        - Implements idempotent behavior by checking download history
        - Uses DOI as primary identifier, falls back to title matching
        - Prevents duplicate downloads across multiple runs
        """
        downloaded_papers = existing_metadata.get("downloaded_papers", {})
        paper_key = paper.doi if paper.doi else f"title:{paper.title.lower().strip()}"

        return paper_key not in downloaded_papers

    def save_strategy_results(
        self,
        papers: List[ResearchPaper],
        output_path: Path,
        config_name: str,
        strategy_name: str,
    ) -> None:
        """
        Save strategy results to JSON file with metadata.

        Args:
            papers: List of research papers to save
            output_path: Directory path for saving results
            config_name: Configuration name for metadata
            strategy_name: Strategy name for metadata

        Educational Notes:
        - Creates comprehensive metadata for research provenance
        - Uses JSON for cross-platform data interchange
        - Includes processing statistics for quality assessment
        - Implements proper file error handling
        """
        results_file = output_path / "papers.json"
        metadata_file = output_path / "metadata.json"

        # Load existing metadata for incremental updates
        existing_metadata = self._get_existing_metadata(metadata_file)
        current_time = datetime.now(timezone.utc).isoformat()

        # Prepare main results data
        results_data = {
            "config_name": config_name,
            "strategy_name": strategy_name,
            "processed_at": current_time,
            "total_papers": len(papers),
            "papers": self.serialize_papers(papers),
        }

        # Merge new papers with existing downloaded papers
        downloaded_papers = existing_metadata.get("downloaded_papers", {}).copy()
        for paper in papers:
            paper_key = (
                paper.doi if paper.doi else f"title:{paper.title.lower().strip()}"
            )
            downloaded_papers[paper_key] = {
                "title": paper.title,
                "download_date": current_time,
                "file_path": f"pdfs/{paper.title.replace(' ', '_').replace('/', '_')}.pdf",  # Expected PDF path
            }

        # Prepare metadata for research provenance (merge with existing)
        metadata = {
            "processing_metadata": {
                "processed_at": current_time,
                "processor_version": "1.0.0",
                "max_papers_limit": self.max_papers,
                "deduplication_enabled": True,
                "concept_extraction_enabled": self.enable_concept_extraction,
            },
            "strategy_metadata": {
                "config_name": config_name,
                "strategy_name": strategy_name,
                "papers_found": len(papers),
            },
            "file_structure": {
                "papers_file": "papers.json",
                "metadata_file": "metadata.json",
                "concepts_file": (
                    "concepts.json" if self.enable_concept_extraction else None
                ),
                "hierarchy_file": (
                    "concept_hierarchy.json" if self.enable_concept_extraction else None
                ),
            },
            # Track last download date for idempotent operations
            "last_download_date": current_time,
            # Track downloaded papers with detailed metadata (merged with existing)
            "downloaded_papers": downloaded_papers,
        }

        try:
            # Save main results
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)

            # Save metadata
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"    ✅ Saved {len(papers)} papers to {results_file}")

            # Extract concepts if enabled
            if self.enable_concept_extraction:
                self._extract_and_save_concepts(output_path, config_name, strategy_name)

        except Exception as e:
            error_msg = f"Failed to save results for {config_name}/{strategy_name}: {e}"
            self.processing_stats["errors"].append(error_msg)
            print(f"    ❌ {error_msg}")

    def _extract_and_save_concepts(
        self, output_path: Path, config_name: str, strategy_name: str
    ) -> None:
        """
        Extract concepts from downloaded PDFs and save hierarchy for GUI.

        Args:
            output_path: Strategy output directory containing PDFs
            config_name: Configuration name for context
            strategy_name: Strategy name for context

        Educational Notes:
        - Integrates concept extraction with batch processing
        - Creates GUI-compatible concept hierarchy files
        - Handles errors gracefully to maintain system stability
        - Uses dependency injection for testability
        """
        # If extractors are injected (testing mode), skip availability check
        if self._concept_extractor is not None or self._hierarchy_builder is not None:
            try:
                print(f"    🧠 Extracting concepts for {strategy_name}...")

                pdfs_dir = output_path / "pdfs"
                if not pdfs_dir.exists() or not any(pdfs_dir.glob("*.pdf")):
                    print(f"    ⚠️  No PDFs found in {pdfs_dir}")
                    return

                # Use injected extractors (for testing)
                concept_extractor = self._concept_extractor
                hierarchy_builder = self._hierarchy_builder

                # Extract concepts from PDFs
                if hasattr(concept_extractor, "extract_from_directory"):
                    # Mock extractor (for testing)
                    extraction_result = concept_extractor.extract_from_directory(
                        pdfs_dir
                    )
                else:
                    # Real concept extraction using use case
                    extraction_result = self._extract_concepts_with_use_case(pdfs_dir)

                if not extraction_result or not extraction_result.get("concepts"):
                    print(f"    ⚠️  No concepts extracted for {strategy_name}")
                    return

                # Build concept hierarchy
                if hasattr(hierarchy_builder, "build_hierarchy"):
                    # Mock hierarchy builder (for testing)
                    hierarchy_result = hierarchy_builder.build_hierarchy(
                        extraction_result["concepts"]
                    )
                else:
                    # Real hierarchy building
                    hierarchy_result = self._build_concept_hierarchy(
                        extraction_result["concepts"]
                    )

                # Save concepts and hierarchy files
                self._save_concept_files(
                    output_path,
                    extraction_result,
                    hierarchy_result,
                    config_name,
                    strategy_name,
                )

                concept_count = len(extraction_result.get("concepts", []))
                self.processing_stats["concepts_extracted"] += concept_count
                print(f"    ✅ Extracted and saved {concept_count} concepts")

            except Exception as e:
                error_msg = (
                    f"Concept extraction failed for {config_name}/{strategy_name}: {e}"
                )
                self.processing_stats["errors"].append(error_msg)
                print(f"    ❌ {error_msg}")
            return

        # Production mode - check if concept extraction is available
        if not CONCEPT_EXTRACTION_AVAILABLE:
            print(f"    ⚠️  Concept extraction not available for {strategy_name}")
            return

        try:
            print(f"    🧠 Extracting concepts for {strategy_name}...")

            pdfs_dir = output_path / "pdfs"
            if not pdfs_dir.exists() or not any(pdfs_dir.glob("*.pdf")):
                print(f"    ⚠️  No PDFs found in {pdfs_dir}")
                return

            # Extract concepts from PDFs using production use case
            extraction_result = self._extract_concepts_with_use_case(pdfs_dir)

            if not extraction_result or not extraction_result.get("concepts"):
                print(f"    ⚠️  No concepts extracted for {strategy_name}")
                return

            # Build concept hierarchy using production hierarchy builder
            hierarchy_result = self._build_concept_hierarchy(
                extraction_result["concepts"]
            )

            # Save concepts and hierarchy files
            self._save_concept_files(
                output_path,
                extraction_result,
                hierarchy_result,
                config_name,
                strategy_name,
            )

            concept_count = len(extraction_result.get("concepts", []))
            self.processing_stats["concepts_extracted"] += concept_count
            print(f"    ✅ Extracted and saved {concept_count} concepts")

        except Exception as e:
            error_msg = (
                f"Concept extraction failed for {config_name}/{strategy_name}: {e}"
            )
            self.processing_stats["errors"].append(error_msg)
            print(f"    ❌ {error_msg}")

    def _create_default_concept_extractor(self):
        """Create default concept extractor for production use."""
        if not CONCEPT_EXTRACTION_AVAILABLE:
            return None

        # Create real concept extraction use case
        pdf_extractor = PyPDF2TextExtractor()
        concept_repo = JSONConceptRepository(storage_directory="concept_storage")

        return ExtractPaperConceptsUseCase(
            pdf_extractor=pdf_extractor, concept_repository=concept_repo
        )

    def _create_default_hierarchy_builder(self):
        """Create default hierarchy builder for production use."""
        if not CONCEPT_EXTRACTION_AVAILABLE:
            return None

        return ConceptHierarchyBuilder()

    def _extract_concepts_with_use_case(self, pdfs_dir: Path) -> Dict:
        """Extract concepts using the real use case."""
        # Create extraction use case
        use_case = self._create_default_concept_extractor()
        if not use_case:
            return {"concepts": [], "total_extracted": 0}

        # Process all PDFs in directory using the correct method
        paper_concepts_list = use_case.extract_concepts_from_domain(
            domain_name=pdfs_dir.parent.name,  # Use strategy name as domain
            papers_directory=pdfs_dir,
        )

        # Extract all concepts from all papers into a flat list
        all_concepts = []
        for paper_concepts in paper_concepts_list:
            all_concepts.extend(paper_concepts.concepts)

        # Convert Concept objects to dictionaries for JSON serialization
        concept_dicts = [concept.to_dict() for concept in all_concepts]

        return {"concepts": concept_dicts, "total_extracted": len(concept_dicts)}

    def _build_concept_hierarchy(self, concept_dicts: List[Dict]) -> Dict:
        """Build concept hierarchy using real hierarchy builder."""
        hierarchy_builder = self._create_default_hierarchy_builder()
        if not hierarchy_builder:
            return {"root_concepts": [], "total_concepts": 0}

        # Convert concept dictionaries back to Concept objects for hierarchy builder
        from src.domain.entities.concept import Concept

        concepts = [Concept.from_dict(concept_dict) for concept_dict in concept_dicts]

        # Build hierarchy and return in expected format
        hierarchical_concepts = hierarchy_builder.build_hierarchy(concepts)

        # Convert back to dictionaries for JSON serialization
        hierarchical_dicts = [concept.to_dict() for concept in hierarchical_concepts]

        # Find root concepts (concepts with no parents)
        root_concepts = [c for c in hierarchical_dicts if not c.get("parent_concepts")]

        return {
            "root_concepts": root_concepts,
            "total_concepts": len(hierarchical_dicts),
        }

    def _save_concept_files(
        self,
        output_path: Path,
        extraction_result: Dict,
        hierarchy_result: Dict,
        config_name: str,
        strategy_name: str,
    ) -> None:
        """Save concept and hierarchy files for GUI consumption."""
        current_time = datetime.now(timezone.utc).isoformat()

        # Save individual concepts file
        concepts_file = output_path / "concepts.json"
        concepts_data = {
            "concepts": extraction_result.get("concepts", []),
            "extraction_metadata": {
                "total_extracted": extraction_result.get("total_extracted", 0),
                "processing_time": extraction_result.get("processing_time", 0),
                "quality_score": extraction_result.get("quality_score", 0),
                "extracted_at": current_time,
                "config_name": config_name,
                "strategy_name": strategy_name,
            },
        }

        with open(concepts_file, "w", encoding="utf-8") as f:
            json.dump(concepts_data, f, indent=2, ensure_ascii=False)

        # Save concept hierarchy file for GUI visualization
        hierarchy_file = output_path / "concept_hierarchy.json"
        hierarchy_data = {
            "root_concepts": hierarchy_result.get("root_concepts", []),
            "visualization_metadata": {
                "domain": config_name,
                "strategy": strategy_name,
                "generated_at": current_time,
                "total_concepts": hierarchy_result.get("total_concepts", 0),
                "max_depth": hierarchy_result.get("max_depth", 0),
                "visualization_type": "d3_hierarchy",
            },
        }

        with open(hierarchy_file, "w", encoding="utf-8") as f:
            json.dump(hierarchy_data, f, indent=2, ensure_ascii=False)

    def process_strategy(
        self,
        use_case: ExecuteKeywordSearchUseCase,
        config_name: str,
        strategy_name: str,
    ) -> None:
        """
        Process a single strategy within a configuration.

        Args:
            use_case: Configured search use case for executing strategies
            config_name: Name of the parent configuration
            strategy_name: Name of the strategy to process

        Educational Notes:
        - Demonstrates Clean Architecture use case execution
        - Implements comprehensive error handling for robustness
        - Tracks processing statistics for monitoring
        - Creates organized output structure as specified
        - Integrates concept extraction for enhanced insights
        """
        try:
            print(f"  🔍 Processing strategy: {strategy_name}")

            # Create output directory structure first
            output_path = self.create_output_structure(config_name, strategy_name)

            # Execute the search strategy with PDF downloads enabled, using the correct output directory
            papers = use_case.execute_strategy(
                strategy_name, download_papers=True, output_dir=output_path
            )

            if not papers:
                print(f"    ⚠️  No papers found for strategy {strategy_name}")
                return

            # Check for existing metadata for idempotent filtering
            metadata_file = output_path / "metadata.json"

            # Load existing metadata for idempotent filtering
            existing_metadata = self._get_existing_metadata(metadata_file)

            # Filter papers to skip already downloaded ones
            new_papers = []
            for paper in papers:
                if self._should_download_paper(paper, existing_metadata):
                    new_papers.append(paper)
                else:
                    print(f"    ⏭️  Skipping already downloaded: {paper.title[:50]}...")

            if not new_papers:
                print(
                    f"    ✅ All papers already downloaded for strategy {strategy_name}"
                )
                return

            # Apply deduplication and limit to only new papers
            unique_papers = self.deduplicate_papers(new_papers)

            # Save results with metadata
            self.save_strategy_results(
                unique_papers, output_path, config_name, strategy_name
            )

            # Extract concepts if enabled
            if self.enable_concept_extraction:
                self._extract_and_save_concepts(output_path, config_name, strategy_name)

            # Update statistics
            self.processing_stats["strategies_processed"] += 1
            self.processing_stats["papers_found"] += len(papers)
            self.processing_stats["papers_stored"] += len(unique_papers)
            print(
                f"    📊 Found {len(papers)} papers, {len(papers) - len(new_papers)} already downloaded, {len(unique_papers)} new papers saved"
            )

        except Exception as e:
            error_msg = (
                f"Error processing strategy {strategy_name} in {config_name}: {e}"
            )
            self.processing_stats["errors"].append(error_msg)
            print(f"    ❌ {error_msg}")

    def process_configuration(
        self, config_name: str, config_path: Path, repository
    ) -> None:
        """
        Process all strategies within a single configuration file.

        Args:
            config_name: Name of the configuration
            config_path: Path to the configuration YAML file
            repository: Paper repository for search execution

        Educational Notes:
        - Demonstrates configuration-driven processing
        - Shows proper resource management and cleanup
        - Implements strategy iteration with error isolation
        - Uses dependency injection for repository flexibility
        """
        try:
            print(f"\n📂 Processing configuration: {config_name}")

            # Load configuration
            config = self.load_configuration(config_path)

            # Create use case with injected repository
            use_case = ExecuteKeywordSearchUseCase(repository)
            use_case.keyword_config = config  # Inject configuration

            # Process each strategy in the configuration
            strategy_names = config.list_strategies()
            print(f"  📋 Found {len(strategy_names)} strategies")

            for strategy_name in strategy_names:
                self.process_strategy(use_case, config_name, strategy_name)

            self.processing_stats["configs_processed"] += 1
            print(f"  ✅ Configuration {config_name} processed successfully")

        except Exception as e:
            error_msg = f"Error processing configuration {config_name}: {e}"
            self.processing_stats["errors"].append(error_msg)
            print(f"  ❌ {error_msg}")

    def run_all_configurations(self, use_arxiv: bool = True) -> None:
        """
        Process all discovered configurations in the config directory.

        Args:
            use_arxiv: Whether to use arXiv API or sample data for testing

        Educational Notes:
        - Demonstrates batch processing orchestration
        - Implements comprehensive error handling and recovery
        - Provides detailed progress reporting and statistics
        - Uses repository pattern for flexible data sources
        """
        start_time = datetime.now(timezone.utc)
        print("🚀 Starting batch processing of research paper configurations...")
        print(f"   📂 Config directory: {self.config_dir}")
        print(f"   💾 Output directory: {self.output_dir}")
        print(f"   📄 Max papers per strategy: {self.max_papers}")
        print(
            f"   🧠 Concept extraction: {'enabled' if self.enable_concept_extraction else 'disabled'}"
        )

        try:
            # Discover all configuration files
            configs = self.discover_configurations()
            print(f"\n🔍 Discovered {len(configs)} configuration files:")
            for config_name in configs.keys():
                print(f"   📄 {config_name}")

            # Choose repository based on configuration
            if use_arxiv:
                repository = ArxivPaperRepository()
                print("\n🔗 Using arXiv API for paper search")
            else:
                repository = InMemoryPaperRepository()
                print("\n💾 Using sample data for testing")

            # Process each configuration
            for config_name, config_path in configs.items():
                self.process_configuration(config_name, config_path, repository)

        except Exception as e:
            error_msg = f"Critical error in batch processing: {e}"
            self.processing_stats["errors"].append(error_msg)
            print(f"❌ {error_msg}")

        # Print comprehensive summary
        self.print_processing_summary(start_time)

    def print_processing_summary(self, start_time: datetime) -> None:
        """
        Print comprehensive processing statistics and summary.

        Args:
            start_time: When processing began

        Educational Notes:
        - Provides detailed metrics for monitoring and debugging
        - Calculates processing performance indicators
        - Summarizes results for user understanding
        - Includes error reporting for troubleshooting
        """
        end_time = datetime.now(timezone.utc)
        processing_time = (end_time - start_time).total_seconds()

        print(f"\n{'=' * 60}")
        print("📈 BATCH PROCESSING SUMMARY")
        print(f"{'=' * 60}")
        print(
            f"📂 Configurations processed: {self.processing_stats['configs_processed']}"
        )
        print(
            f"🔍 Strategies processed: {self.processing_stats['strategies_processed']}"
        )
        print(f"📄 Papers found: {self.processing_stats['papers_found']}")
        print(f"💾 Papers stored: {self.processing_stats['papers_stored']}")
        print(f"🔄 Duplicates filtered: {self.processing_stats['duplicates_filtered']}")
        print(f"🧠 Concepts extracted: {self.processing_stats['concepts_extracted']}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")

        if self.processing_stats["errors"]:
            print(f"\n⚠️  Errors encountered: {len(self.processing_stats['errors'])}")
            for error in self.processing_stats["errors"]:
                print(f"  ❌ {error}")

        print(f"\n📁 Results organized in: {self.output_dir}")
        print("   Structure: outputs/config_name/strategy_name/")
        print("   Files: papers.json, metadata.json")
        if self.enable_concept_extraction:
            print("   Concept files: concepts.json, concept_hierarchy.json")


def run_batch_processing(
    config_dir: str = "config",
    output_dir: str = "outputs",
    max_papers: int = 100,
    use_arxiv: bool = True,
    enable_concept_extraction: bool = False,
) -> None:
    """
    Entry point for batch processing functionality.

    Args:
        config_dir: Directory containing YAML configuration files
        output_dir: Base directory for organized output structure
        max_papers: Maximum papers to store per strategy
        use_arxiv: Whether to use arXiv API or sample data
        enable_concept_extraction: Whether to extract concepts from downloaded papers

    Educational Notes:
    - Provides clean entry point for CLI integration
    - Demonstrates proper error handling for main functions
    - Encapsulates batch processing complexity
    - Follows single responsibility principle
    - Supports concept extraction for enhanced functionality
    """
    try:
        processor = BatchProcessor(
            config_dir=config_dir,
            output_dir=output_dir,
            max_papers=max_papers,
            enable_concept_extraction=enable_concept_extraction,
        )
        processor.run_all_configurations(use_arxiv=use_arxiv)

    except Exception as e:
        print(f"❌ Fatal error in batch processing: {e}")
        return False

    return True


if __name__ == "__main__":
    # Example usage with concept extraction enabled
    success = run_batch_processing(
        config_dir="config",
        output_dir="outputs",
        max_papers=50,  # Smaller limit for faster testing
        use_arxiv=True,
        enable_concept_extraction=True,  # Enable concept extraction
    )

    exit_code = 0 if success else 1
    exit(exit_code)
