"""
ExtractPaperConceptsUseCase - Application layer orchestration for concept extraction.

This use case demonstrates Clean Architecture principles by orchestrating
domain services while maintaining proper dependency direction and separation
of concerns.

Educational Notes:
- Shows Application Layer pattern for coordinating domain services
- Demonstrates Dependency Injection and Inversion of Control
- Illustrates error handling and logging in application services
- Shows how to maintain business rules while delegating to domain services

Design Decisions:
- Repository pattern for data access abstraction
- Domain service orchestration for complex business logic
- Error handling with meaningful user messages
- Logging for monitoring and debugging
- Configuration-driven behavior for flexibility

Use Cases:
- Extracting concepts from individual research papers
- Batch processing of research paper collections
- Domain-specific concept extraction workflows
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import TimeoutError
import logging

from src.domain.entities.research_paper import ResearchPaper
from src.domain.entities.paper_concepts import PaperConcepts
from src.domain.entities.concept import Concept
from src.domain.services.concept_extractor import ConceptExtractor
from src.domain.services.concept_hierarchy_builder import ConceptHierarchyBuilder
from src.application.ports.pdf_extractor_port import PDFTextExtractorPort
from src.application.ports.concept_repository_port import ConceptRepositoryPort

# Try to import multi-strategy components (optional for backward compatibility)
try:
    from src.domain.services.multi_strategy_concept_extractor import (
        MultiStrategyConceptExtractor,
        StrategyConfiguration,
        ExtractionResult,
    )

    MULTI_STRATEGY_AVAILABLE = True
except ImportError:
    # For backward compatibility when multi-strategy components not available
    MultiStrategyConceptExtractor = None
    StrategyConfiguration = None
    ExtractionResult = None
    MULTI_STRATEGY_AVAILABLE = False

from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path
import json
from datetime import datetime, timezone

from src.domain.entities.research_paper import ResearchPaper
from src.domain.entities.paper_concepts import PaperConcepts
from src.domain.entities.concept import Concept
from src.domain.services.concept_extractor import (
    ConceptExtractor,
    ExtractionConfiguration,
)
from src.domain.services.concept_hierarchy_builder import ConceptHierarchyBuilder

# TDD Cycle 5: Import MultiStrategyConceptExtractor for enhanced functionality
try:
    from src.domain.services.multi_strategy_concept_extractor import (
        MultiStrategyConceptExtractor,
        StrategyConfiguration,
        ExtractionResult,
    )
except ImportError:
    # Graceful fallback if multi-strategy components not available
    MultiStrategyConceptExtractor = None
    StrategyConfiguration = None
    ExtractionResult = None


# Educational Note: Constants improve maintainability and reduce magic strings
class ExtractPaperConceptsMessages:
    """
    Message constants for extraction use case.

    Educational Note:
    Centralizing string constants follows the DRY principle and makes
    internationalization easier while improving maintainability.
    """

    CONCEPTS_EXIST = "Concepts already exist for {}, skipping extraction"
    EXTRACTING_TEXT = "Extracting text from {}..."
    EXTRACTED_CHARACTERS = "Extracted {} characters of text"
    EXTRACTING_CONCEPTS = "Extracting concepts for {}..."
    EXTRACTED_CONCEPTS_COUNT = "Extracted {} concepts"
    BUILDING_HIERARCHIES = "Building concept hierarchies..."
    BUILT_HIERARCHIES = "Built hierarchies for {} concepts"
    HIERARCHY_FAILED = "Hierarchy building failed: {}"
    EXTRACTION_COMPLETE = "Extraction complete - Quality: {:.2%}"
    PROCESSING_DOMAIN = "Processing domain: {}"
    PAPERS_DIRECTORY = "Papers directory: {}"
    FOUND_PDF_FILES = "Found {} PDF files"
    PROCESSING_FILE = "Processing {}/{}: {}"
    DOMAIN_COMPLETE = "=== Domain Processing Complete ==="
    SUCCESSFULLY_PROCESSED = "Successfully processed: {} papers"
    ERRORS_ENCOUNTERED = "Errors encountered: {} papers"

    # Error messages
    ERROR_INVALID_PAPER = "Invalid research paper entity"
    ERROR_PDF_NOT_FOUND = "PDF file not found: {}"
    ERROR_NO_TEXT_EXTRACTED = "No text extracted from PDF: {}"
    ERROR_PROCESSING_PAPER = "Error extracting concepts from {}: {}"
    ERROR_FAILED_TO_PROCESS = "Failed to process {}: {}"
    ERROR_DIRECTORY_NOT_FOUND = "Papers directory not found: {}"
    ERROR_NO_PDF_FILES = "No PDF files found in {}"


class PDFTextExtractorPort(ABC):
    """
    Port for PDF text extraction abstraction.

    Educational Note:
    This port follows the Dependency Inversion Principle by defining
    the interface that the application layer needs without depending
    on specific PDF extraction implementations.
    """

    @abstractmethod
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be processed
        """
        pass


class ConceptRepositoryPort(ABC):
    """
    Port for concept persistence abstraction.

    Educational Note:
    Repository pattern abstraction that allows the application
    to store and retrieve concept data without depending on
    specific storage implementations (JSON, database, etc.).
    """

    @abstractmethod
    def save_paper_concepts(self, paper_concepts: PaperConcepts) -> None:
        """Save paper concepts to storage."""
        pass

    @abstractmethod
    def find_paper_concepts_by_doi(self, doi: str) -> Optional[PaperConcepts]:
        """Find paper concepts by paper DOI."""
        pass

    @abstractmethod
    def find_all_concepts_in_domain(self, domain: str) -> List[PaperConcepts]:
        """Find all paper concepts in a specific domain."""
        pass

    @abstractmethod
    def get_extraction_statistics(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics about concept extractions."""
        pass


class ExtractPaperConceptsUseCase:
    """
    Application use case for extracting concepts from research papers.

    Educational Note:
    This use case orchestrates the complete concept extraction workflow,
    demonstrating how the application layer coordinates domain services
    and infrastructure concerns while maintaining clean boundaries.
    """

    def __init__(
        self,
        pdf_extractor: PDFTextExtractorPort,
        concept_repository: ConceptRepositoryPort,
        concept_extractor: Optional[ConceptExtractor] = None,
        config: Optional[ExtractionConfiguration] = None,
        hierarchy_builder: Optional[ConceptHierarchyBuilder] = None,
        enable_hierarchy_building: bool = False,
        # TDD Cycle 5: Enhanced constructor with multi-strategy capabilities
        multi_strategy_extractor: Optional[Any] = None,
        strategy_config: Optional[Any] = None,
        enable_multi_strategy_extraction: bool = False,
        extraction_options: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the use case with required dependencies.

        Educational Note:
        Constructor injection demonstrates Dependency Inversion Principle,
        allowing the use case to work with any implementation of the
        required ports while maintaining testability.

        Args:
            pdf_extractor: Port for PDF text extraction
            concept_repository: Port for concept persistence
            concept_extractor: Domain service for concept extraction
            config: Configuration for extraction process
            hierarchy_builder: Domain service for concept hierarchy building
            enable_hierarchy_building: Whether to enable hierarchical concept processing
            multi_strategy_extractor: Enhanced domain service for multi-strategy extraction
            strategy_config: Configuration for multi-strategy behavior
            enable_multi_strategy_extraction: Whether to use multi-strategy approach
            extraction_options: Additional configuration options
        """
        # Core dependencies (unchanged for backward compatibility)
        self.pdf_extractor = pdf_extractor
        self.concept_repository = concept_repository
        self.concept_extractor = concept_extractor or ConceptExtractor()
        self.config = config or ExtractionConfiguration()
        self.enable_hierarchy_building = enable_hierarchy_building

        # Only create hierarchy builder when needed
        if enable_hierarchy_building:
            self.hierarchy_builder = hierarchy_builder or ConceptHierarchyBuilder()

        # TDD Cycle 5: Enhanced multi-strategy capabilities
        self.multi_strategy_extractor = multi_strategy_extractor
        self.strategy_config = strategy_config
        self.enable_multi_strategy_extraction = enable_multi_strategy_extraction

        # Extract configuration from extraction_options with defaults
        options = extraction_options or {}
        self.enable_fallback_extraction = options.get(
            "enable_fallback_extraction", True
        )
        self.forced_extraction_strategy = options.get("forced_extraction_strategy")
        self.auto_strategy_selection = options.get("auto_strategy_selection", False)
        self.extraction_timeout_seconds = options.get("extraction_timeout_seconds", 300)
        self.enable_timeout_handling = options.get("enable_timeout_handling", False)
        self.accept_partial_results = options.get("accept_partial_results", False)
        self.min_success_rate = options.get("min_success_rate", 0.5)

        # Validate configuration if multi-strategy extraction is enabled
        if self.enable_multi_strategy_extraction:
            self._validate_multi_strategy_configuration()

    def extract_concepts_from_paper(
        self,
        paper: ResearchPaper,
        pdf_path: Path,
        domain: Optional[str] = None,
        force_reextraction: bool = False,
    ) -> PaperConcepts:
        """
        Extract concepts from a single research paper.

        Educational Note:
        Main use case method that orchestrates the entire concept
        extraction workflow. Refactored to use extracted methods
        following the Single Responsibility Principle.

        Args:
            paper: Research paper entity
            pdf_path: Path to the PDF file
            domain: Research domain for context-aware extraction
            force_reextraction: Whether to re-extract if concepts already exist

        Returns:
            PaperConcepts entity with extracted concepts

        Raises:
            ValueError: If paper or PDF path is invalid
            FileNotFoundError: If PDF file doesn't exist
        """
        # Validation phase
        self._validate_extraction_inputs(paper, pdf_path)

        # Check for existing concepts
        if not force_reextraction:
            existing_concepts = self._check_existing_concepts(paper.doi)
            if existing_concepts:
                return existing_concepts

        try:
            # Text extraction phase
            paper_text = self._extract_text_from_pdf(pdf_path)

            # Concept extraction phase
            paper_concepts = self._extract_concepts_from_text(paper_text, paper, domain)

            # Hierarchy building phase (if enabled)
            if self.enable_hierarchy_building:
                paper_concepts = self._apply_hierarchy_building(paper_concepts)

            # Persistence phase
            self.concept_repository.save_paper_concepts(paper_concepts)

            # Success reporting phase
            self._log_extraction_success(paper_concepts)

            return paper_concepts

        except Exception as e:
            print(
                ExtractPaperConceptsMessages.ERROR_PROCESSING_PAPER.format(paper.doi, e)
            )
            raise

    def _validate_extraction_inputs(self, paper: ResearchPaper, pdf_path: Path) -> None:
        """
        Validate inputs for concept extraction.

        Educational Note:
        Extracted validation method following Single Responsibility Principle.
        Makes the main method more readable and validation logic reusable.
        """
        if not isinstance(paper, ResearchPaper):
            raise ValueError(ExtractPaperConceptsMessages.ERROR_INVALID_PAPER)

        if not pdf_path.exists():
            raise FileNotFoundError(
                ExtractPaperConceptsMessages.ERROR_PDF_NOT_FOUND.format(pdf_path)
            )

    def _check_existing_concepts(self, doi: str) -> Optional[PaperConcepts]:
        """
        Check if concepts already exist for a paper.

        Educational Note:
        Extracted method that encapsulates the logic for checking
        existing concepts, improving readability and testability.
        """
        existing_concepts = self.concept_repository.find_paper_concepts_by_doi(doi)
        if existing_concepts:
            print(ExtractPaperConceptsMessages.CONCEPTS_EXIST.format(doi))
        return existing_concepts

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from PDF file with validation.

        Educational Note:
        Extracted method that handles text extraction and validation,
        following the Single Responsibility Principle.
        """
        print(ExtractPaperConceptsMessages.EXTRACTING_TEXT.format(pdf_path.name))
        paper_text = self.pdf_extractor.extract_text_from_pdf(pdf_path)

        if not paper_text.strip():
            raise ValueError(
                ExtractPaperConceptsMessages.ERROR_NO_TEXT_EXTRACTED.format(pdf_path)
            )

        print(ExtractPaperConceptsMessages.EXTRACTED_CHARACTERS.format(len(paper_text)))
        return paper_text

    def _extract_concepts_from_text(
        self, paper_text: str, paper: ResearchPaper, domain: Optional[str]
    ) -> PaperConcepts:
        """
        Extract concepts from paper text using domain service.

        Educational Note:
        Enhanced extraction method that supports both traditional and multi-strategy
        approaches, demonstrating the Strategy Pattern where extraction algorithms
        can be selected based on configuration and domain requirements.
        """
        print(ExtractPaperConceptsMessages.EXTRACTING_CONCEPTS.format(paper.title))

        # TDD Cycle 5: Enhanced extraction with multi-strategy support
        if self.enable_multi_strategy_extraction and self.multi_strategy_extractor:
            return self._extract_concepts_multi_strategy(paper_text, paper, domain)
        else:
            return self._extract_concepts_traditional(paper_text, paper, domain)

    def _extract_concepts_traditional(
        self, paper_text: str, paper: ResearchPaper, domain: Optional[str]
    ) -> PaperConcepts:
        """
        Extract concepts using traditional single-strategy approach.

        Educational Note:
        Maintains backward compatibility with existing extraction workflow
        while providing clear separation from multi-strategy approach.
        """
        paper_concepts = self.concept_extractor.extract_concepts_from_paper(
            paper_text=paper_text,
            paper_doi=paper.doi,
            paper_title=paper.title,
            domain=domain,
        )
        print(
            ExtractPaperConceptsMessages.EXTRACTED_CONCEPTS_COUNT.format(
                paper_concepts.total_concept_count
            )
        )
        return paper_concepts

    def _extract_concepts_multi_strategy(
        self, paper_text: str, paper: ResearchPaper, domain: Optional[str]
    ) -> PaperConcepts:
        """
        Extract concepts using enhanced multi-strategy approach.

        Educational Note:
        Demonstrates integration between application and domain layers,
        using sophisticated multi-strategy extraction with error handling
        and fallback mechanisms for robust concept extraction.
        """
        try:
            # Execute multi-strategy extraction
            extraction_result = (
                self.multi_strategy_extractor.extract_concepts_comprehensive(
                    text=paper_text,
                    config=self.strategy_config,
                    domain=domain or "general",
                )
            )

            # Validate partial results if configured
            if not self.accept_partial_results:
                success_rate = extraction_result.metadata.get("success_rate", 1.0)
                if success_rate < self.min_success_rate:
                    raise ValueError(
                        f"Extraction quality below threshold: {success_rate:.2f} < {self.min_success_rate}"
                    )

            # Convert extraction result to PaperConcepts entity
            paper_concepts = PaperConcepts(
                paper_doi=paper.doi,
                paper_title=paper.title,
                concepts=list(extraction_result.concepts),
                extraction_method="multi_strategy",
                processing_metadata=extraction_result.metadata,
            )

            print(
                ExtractPaperConceptsMessages.EXTRACTED_CONCEPTS_COUNT.format(
                    paper_concepts.total_concept_count
                )
            )
            return paper_concepts

        except TimeoutError as e:
            # Handle timeout errors with custom message
            if self.enable_timeout_handling:
                raise TimeoutError("Concept extraction timed out") from e
            else:
                raise
        except Exception as e:
            print(f"Multi-strategy extraction failed: {e}")
            if self.enable_fallback_extraction:
                print("Falling back to traditional extraction...")
                return self._extract_concepts_traditional_fallback(
                    paper_text, paper, domain
                )
            else:
                raise

    def _extract_concepts_traditional_fallback(
        self, paper_text: str, paper: ResearchPaper, domain: Optional[str]
    ) -> PaperConcepts:
        """
        Fallback to traditional extraction when multi-strategy fails.

        Educational Note:
        Demonstrates graceful degradation pattern, ensuring system robustness
        when sophisticated features fail by falling back to simpler approaches.
        """
        original_concepts = self.concept_extractor.extract_concepts_from_paper(
            paper_text=paper_text,
            paper_doi=paper.doi,
            paper_title=paper.title,
            domain=domain,
        )

        # Create new instance with fallback extraction method (dataclass is frozen)
        paper_concepts = PaperConcepts(
            paper_doi=original_concepts.paper_doi,
            paper_title=original_concepts.paper_title,
            concepts=original_concepts.concepts,
            extraction_metadata=original_concepts.extraction_metadata,
            extraction_method="traditional_fallback",
            processing_metadata={
                "fallback_used": True,
                "original_method": "multi_strategy",
                "fallback_reason": "multi_strategy_extraction_failed",
            },
        )

        print(
            ExtractPaperConceptsMessages.EXTRACTED_CONCEPTS_COUNT.format(
                paper_concepts.total_concept_count
            )
        )
        return paper_concepts

    def _apply_hierarchy_building(self, paper_concepts: PaperConcepts) -> PaperConcepts:
        """
        Apply hierarchical concept organization.

        Educational Note:
        Extracted method that handles hierarchy building with proper error
        handling. This method demonstrates the Strategy pattern where
        hierarchy building is an optional enhancement strategy.

        Args:
            paper_concepts: Original flat concept structure

        Returns:
            Enhanced paper concepts with hierarchical relationships
        """
        try:
            print(ExtractPaperConceptsMessages.BUILDING_HIERARCHIES)
            hierarchical_concepts = self.hierarchy_builder.build_hierarchy(
                paper_concepts.concepts
            )

            # Create enhanced paper concepts with hierarchical metadata
            enhanced_concepts = PaperConcepts(
                paper_doi=paper_concepts.paper_doi,
                paper_title=paper_concepts.paper_title,
                concepts=hierarchical_concepts,
                extraction_timestamp=paper_concepts.extraction_timestamp,
                extraction_method=paper_concepts.extraction_method,
                processing_metadata=paper_concepts.processing_metadata,
                extraction_metadata={
                    **(paper_concepts.extraction_metadata or {}),
                    "has_hierarchical_relationships": True,
                    "hierarchy_building_enabled": True,
                },
            )

            print(
                ExtractPaperConceptsMessages.BUILT_HIERARCHIES.format(
                    len(hierarchical_concepts)
                )
            )
            return enhanced_concepts

        except Exception as hierarchy_error:
            print(ExtractPaperConceptsMessages.HIERARCHY_FAILED.format(hierarchy_error))
            # Return original concepts on hierarchy building failure
            return paper_concepts

    def _log_extraction_success(self, paper_concepts: PaperConcepts) -> None:
        """
        Log successful extraction statistics.

        Educational Note:
        Extracted method for success reporting, following Single Responsibility
        Principle and making logging behavior consistent and testable.
        """
        try:
            stats = self.concept_extractor.get_extraction_statistics(paper_concepts)
            quality_ratio = stats["quality_metrics"]["quality_ratio"]
            print(
                ExtractPaperConceptsMessages.EXTRACTION_COMPLETE.format(quality_ratio)
            )
        except (KeyError, ZeroDivisionError) as e:
            # Handle cases where no concepts were extracted or statistics unavailable
            print(
                f"Extraction completed for {paper_concepts.paper_doi} ({paper_concepts.total_concept_count} concepts)"
            )
            print(f"Note: Detailed statistics unavailable - {str(e)}")

    def extract_concepts_from_domain(
        self,
        domain_name: str,
        papers_directory: Path,
        metadata_file: Optional[Path] = None,
        force_reextraction: bool = False,
    ) -> List[PaperConcepts]:
        """
        Extract concepts from all papers in a domain directory.

        Educational Note:
        Batch processing method that demonstrates transaction management,
        error recovery, and progress reporting for large-scale operations.
        Now refactored to use extracted helper methods for better maintainability.

        Args:
            domain_name: Name of the research domain
            papers_directory: Directory containing PDF files
            metadata_file: Optional metadata.json file with paper information
            force_reextraction: Whether to re-extract existing concepts

        Returns:
            List of PaperConcepts for all processed papers
        """
        # Validation phase
        self._validate_domain_inputs(papers_directory)

        # Setup phase
        print(ExtractPaperConceptsMessages.PROCESSING_DOMAIN.format(domain_name))
        print(ExtractPaperConceptsMessages.PAPERS_DIRECTORY.format(papers_directory))

        papers_metadata = self._load_domain_metadata(metadata_file)
        pdf_files = self._find_pdf_files(papers_directory)

        # Processing phase
        return self._process_pdf_files(
            pdf_files, papers_metadata, domain_name, force_reextraction
        )

    def _validate_domain_inputs(self, papers_directory: Path) -> None:
        """
        Validate inputs for domain processing.

        Educational Note:
        Extracted validation method that centralizes input validation,
        following the Fail Fast principle.
        """
        if not papers_directory.exists():
            raise FileNotFoundError(
                ExtractPaperConceptsMessages.ERROR_DIRECTORY_NOT_FOUND.format(
                    papers_directory
                )
            )

    def _load_domain_metadata(self, metadata_file: Optional[Path]) -> Dict[str, Any]:
        """
        Load domain metadata from JSON file.

        Educational Note:
        Extracted method that handles metadata loading with proper error handling,
        demonstrating the Single Responsibility Principle.
        """
        papers_metadata = {}
        if metadata_file and metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                papers_metadata = {
                    paper["doi"]: paper for paper in metadata.get("papers", [])
                }
        return papers_metadata

    def _find_pdf_files(self, papers_directory: Path) -> List[Path]:
        """
        Find all PDF files in the directory.

        Educational Note:
        Extracted method that handles file discovery with validation,
        making the main method more focused and testable.
        """
        pdf_files = list(papers_directory.glob("*.pdf"))
        if not pdf_files:
            raise ValueError(
                ExtractPaperConceptsMessages.ERROR_NO_PDF_FILES.format(papers_directory)
            )

        print(ExtractPaperConceptsMessages.FOUND_PDF_FILES.format(len(pdf_files)))
        return pdf_files

    def _process_pdf_files(
        self,
        pdf_files: List[Path],
        papers_metadata: Dict[str, Any],
        domain_name: str,
        force_reextraction: bool,
    ) -> List[PaperConcepts]:
        """
        Process all PDF files and extract concepts.

        Educational Note:
        Extracted method that handles the main processing loop with
        error recovery and progress reporting.
        """
        results = []
        errors = []

        for i, pdf_path in enumerate(pdf_files, 1):
            print(
                ExtractPaperConceptsMessages.PROCESSING_FILE.format(
                    i, len(pdf_files), pdf_path.name
                )
            )

            try:
                paper = self._create_paper_from_pdf(
                    pdf_path, papers_metadata, domain_name
                )
                paper_concepts = self.extract_concepts_from_paper(
                    paper=paper,
                    pdf_path=pdf_path,
                    domain=domain_name,
                    force_reextraction=force_reextraction,
                )
                results.append(paper_concepts)

            except Exception as e:
                error_msg = ExtractPaperConceptsMessages.ERROR_FAILED_TO_PROCESS.format(
                    pdf_path.name, e
                )
                print(f"ERROR: {error_msg}")
                errors.append(error_msg)
                continue

        # Report final results
        self._report_domain_results(results, errors)
        return results

    def _report_domain_results(
        self, results: List[PaperConcepts], errors: List[str]
    ) -> None:
        """
        Report domain processing results.

        Educational Note:
        Extracted method that handles result reporting with consistent formatting,
        demonstrating separation of concerns.
        """
        print(f"\n{ExtractPaperConceptsMessages.DOMAIN_COMPLETE}")
        print(ExtractPaperConceptsMessages.SUCCESSFULLY_PROCESSED.format(len(results)))
        print(ExtractPaperConceptsMessages.ERRORS_ENCOUNTERED.format(len(errors)))

        if errors:
            print("\nErrors:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more errors")

        return results

    def _create_paper_from_pdf(
        self, pdf_path: Path, metadata: Dict[str, Any], domain: str
    ) -> ResearchPaper:
        """
        Create ResearchPaper entity from PDF file and metadata.

        Educational Note:
        Helper method that demonstrates entity creation with
        fallback strategies when complete metadata isn't available.
        The domain parameter is used for context-aware paper creation.
        """
        # Try to extract paper info from filename
        filename = pdf_path.stem

        # Look for matching metadata
        matching_paper = None
        for doi, paper_data in metadata.items():
            if filename in paper_data.get("title", "").replace(" ", "_"):
                matching_paper = paper_data
                break

        if matching_paper:
            # Create paper from metadata with domain context
            keywords = matching_paper.get("keywords", [])
            if domain and domain not in keywords:
                keywords.append(domain)  # Add domain as keyword for context

            return ResearchPaper(
                title=matching_paper["title"],
                authors=matching_paper.get("authors", ["Unknown Author"]),
                abstract=matching_paper.get("abstract", ""),
                publication_date=datetime.fromisoformat(
                    matching_paper["publication_date"]
                ),
                doi=matching_paper["doi"],
                arxiv_id=matching_paper.get("arxiv_id"),
                citation_count=matching_paper.get("citation_count", 0),
                keywords=keywords,
            )
        else:
            # Create minimal paper from filename with domain context
            return ResearchPaper(
                title=filename.replace("_", " "),
                authors=["Unknown Author"],
                abstract="",
                publication_date=datetime.now(timezone.utc),
                doi=f"local/{filename}",
                citation_count=0,
                keywords=[domain] if domain else [],  # Use domain for keyword context
            )

    def get_domain_concept_statistics(self, domain: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics about concepts in a domain.

        Educational Note:
        Analytics method that demonstrates how use cases can provide
        business intelligence by coordinating domain services and
        repository queries to generate insights.

        Args:
            domain: Research domain to analyze

        Returns:
            Dictionary with comprehensive concept statistics
        """
        try:
            # Get basic repository statistics
            repo_stats = self.concept_repository.get_extraction_statistics(domain)

            # Get all paper concepts in domain
            all_paper_concepts = self.concept_repository.find_all_concepts_in_domain(
                domain
            )

            if not all_paper_concepts:
                return {
                    "domain": domain,
                    "total_papers": 0,
                    "total_concepts": 0,
                    "error": "No papers found in domain",
                }

            # Calculate advanced statistics
            total_papers = len(all_paper_concepts)
            all_concepts = []
            for paper_concepts in all_paper_concepts:
                all_concepts.extend(paper_concepts.concepts)

            # Concept frequency analysis
            concept_frequency = {}
            for concept in all_concepts:
                text = concept.text.lower()
                concept_frequency[text] = concept_frequency.get(text, 0) + 1

            # Most common concepts
            top_concepts = sorted(
                concept_frequency.items(), key=lambda x: x[1], reverse=True
            )[:20]

            return {
                "domain": domain,
                "total_papers": total_papers,
                "total_concepts": len(all_concepts),
                "unique_concepts": len(concept_frequency),
                "avg_concepts_per_paper": round(len(all_concepts) / total_papers, 2),
                "top_concepts": top_concepts,
                "repository_stats": repo_stats,
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            return {
                "domain": domain,
                "error": str(e),
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            }

    def generate_concept_visualization_data(
        self, domain: str, output_path: Path
    ) -> None:
        """
        Generate JSON data files for concept visualization.

        Educational Note:
        Data export method that prepares domain data for consumption
        by external visualization tools, demonstrating how use cases
        can serve as integration points between internal domain logic
        and external presentation layers.

        Args:
            domain: Research domain to export
            output_path: Directory to write visualization data
        """
        try:
            # Get all paper concepts
            all_paper_concepts = self.concept_repository.find_all_concepts_in_domain(
                domain
            )

            if not all_paper_concepts:
                print(f"No papers found in domain: {domain}")
                return

            # Create output directory
            output_path.mkdir(parents=True, exist_ok=True)

            # Export paper concepts
            papers_data = []
            for paper_concepts in all_paper_concepts:
                papers_data.append(paper_concepts.to_dict())

            papers_file = output_path / "papers_concepts.json"
            with open(papers_file, "w", encoding="utf-8") as f:
                json.dump(papers_data, f, indent=2, ensure_ascii=False)

            # Export concept network data
            concept_network = self._build_concept_network(all_paper_concepts)
            network_file = output_path / "concept_network.json"
            with open(network_file, "w", encoding="utf-8") as f:
                json.dump(concept_network, f, indent=2, ensure_ascii=False)

            # Export domain statistics
            stats = self.get_domain_concept_statistics(domain)
            stats_file = output_path / "domain_statistics.json"
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)

            print(f"Visualization data exported to {output_path}")

        except Exception as e:
            print(f"Error generating visualization data: {e}")
            raise

    def _build_concept_network(
        self, all_paper_concepts: List[PaperConcepts]
    ) -> Dict[str, Any]:
        """
        Build concept co-occurrence network for visualization.

        Educational Note:
        Helper method that demonstrates graph construction from
        domain data, creating visualization-ready network structures
        that can be consumed by D3.js or similar libraries.
        """
        # Collect all concepts and their relationships
        concepts = {}
        edges = []

        for paper_concepts in all_paper_concepts:
            paper_concept_texts = [c.text for c in paper_concepts.concepts]

            # Add concepts as nodes
            for concept in paper_concepts.concepts:
                if concept.text not in concepts:
                    concepts[concept.text] = {
                        "id": concept.text,
                        "frequency": concept.frequency,
                        "relevance": concept.relevance_score,
                        "domain": concept.source_domain,
                        "papers": list(concept.source_papers),
                    }
                else:
                    # Merge concept data
                    existing = concepts[concept.text]
                    existing["frequency"] += concept.frequency
                    existing["relevance"] = max(
                        existing["relevance"], concept.relevance_score
                    )
                    existing["papers"].extend(concept.source_papers)
                    existing["papers"] = list(set(existing["papers"]))

            # Add co-occurrence edges
            for i, concept1 in enumerate(paper_concept_texts):
                for concept2 in paper_concept_texts[i + 1 :]:
                    edge = {
                        "source": concept1,
                        "target": concept2,
                        "weight": 1,
                        "paper": paper_concepts.paper_doi,
                    }
                    edges.append(edge)

        return {
            "nodes": list(concepts.values()),
            "edges": edges,
            "metadata": {
                "total_papers": len(all_paper_concepts),
                "total_concepts": len(concepts),
                "total_relationships": len(edges),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
        }

    # =============================================================================
    # TDD CYCLE 5: ENHANCED MULTI-STRATEGY EXTRACTION METHODS
    # =============================================================================

    def _validate_multi_strategy_configuration(self) -> None:
        """
        Validate multi-strategy extraction configuration.

        Educational Note:
        Configuration validation demonstrates fail-fast principle,
        catching configuration errors early in the application lifecycle
        rather than during runtime execution.

        Raises:
            ValueError: If strategy configuration is invalid
        """
        if self.enable_multi_strategy_extraction and not self.multi_strategy_extractor:
            raise ValueError(
                "Multi-strategy extraction enabled but no extractor provided"
            )

        if not self.strategy_config:
            return

        self._validate_strategy_config_domain()
        self._validate_strategy_config_frequency()
        self._validate_strategy_config_max_concepts()

    def _validate_strategy_config_domain(self) -> None:
        """Validate strategy configuration domain."""
        # Handle dictionary configuration
        if isinstance(self.strategy_config, dict):
            if (
                "domain" in self.strategy_config
                and self.strategy_config["domain"] is None
            ):
                raise ValueError("Invalid configuration: domain cannot be None")
        # Handle object configuration
        elif (
            hasattr(self.strategy_config, "domain") and not self.strategy_config.domain
        ):
            raise ValueError("Invalid strategy configuration: domain cannot be empty")

    def _validate_strategy_config_frequency(self) -> None:
        """Validate strategy configuration frequency."""
        # Handle dictionary configuration
        if isinstance(self.strategy_config, dict):
            if "min_concept_frequency" in self.strategy_config:
                if self.strategy_config["min_concept_frequency"] < 0:
                    raise ValueError(
                        "Invalid configuration: negative frequency not allowed"
                    )
        # Handle object configuration
        elif hasattr(self.strategy_config, "min_concept_frequency"):
            if self.strategy_config.min_concept_frequency < 0:
                raise ValueError(
                    "Invalid strategy configuration: negative frequency not allowed"
                )

    def _validate_strategy_config_max_concepts(self) -> None:
        """Validate strategy configuration max concepts."""
        # Handle dictionary configuration
        if isinstance(self.strategy_config, dict):
            if "max_concepts_per_strategy" in self.strategy_config:
                max_concepts = self.strategy_config["max_concepts_per_strategy"]
                if not isinstance(max_concepts, int):
                    raise TypeError(
                        "Invalid configuration: max_concepts_per_strategy must be integer"
                    )
                if max_concepts <= 0:
                    raise ValueError(
                        "Invalid configuration: max concepts must be positive"
                    )
            if "strategy_weights" in self.strategy_config:
                weights = self.strategy_config["strategy_weights"]
                if isinstance(weights, dict):
                    for strategy, weight in weights.items():
                        if weight > 1.0:
                            raise ValueError(
                                "Invalid configuration: strategy weights must be <= 1.0"
                            )
        # Handle object configuration
        elif hasattr(self.strategy_config, "max_concepts_per_strategy"):
            if self.strategy_config.max_concepts_per_strategy <= 0:
                raise ValueError(
                    "Invalid strategy configuration: max concepts must be positive"
                )

    def _select_extraction_strategy(self, domain: Optional[str] = None) -> str:
        """
        Select appropriate extraction strategy based on domain and configuration.

        Educational Note:
        Strategy selection demonstrates business rule implementation in
        application layer, translating domain expertise into algorithmic decisions.

        Args:
            domain: Research domain to extract concepts for

        Returns:
            Selected strategy name ("multi_strategy" or "traditional")
        """
        # Manual override takes precedence
        if self.forced_extraction_strategy:
            return self.forced_extraction_strategy

        # Auto strategy selection based on domain complexity
        if self.auto_strategy_selection and domain:
            complex_domains = {
                "machine_learning",
                "complex_analysis",
                "multi_modal_research",
            }
            if domain in complex_domains:
                return "multi_strategy"
            else:
                return "traditional"

        # Default based on configuration
        return (
            "multi_strategy" if self.enable_multi_strategy_extraction else "traditional"
        )

    def _merge_strategy_configurations(
        self, base_config: Any, domain_config: Any
    ) -> Any:
        """
        Merge base and domain-specific strategy configurations.

        Educational Note:
        Configuration merging demonstrates composition and inheritance patterns
        applied to value objects, allowing flexible configuration hierarchies.

        Args:
            base_config: Base strategy configuration
            domain_config: Domain-specific overrides

        Returns:
            Merged configuration object
        """
        # For testing phase, implement basic merging logic
        # In production, this would use proper StrategyConfiguration merging
        if not hasattr(base_config, "__dict__") or not hasattr(
            domain_config, "__dict__"
        ):
            return domain_config

        # Create a merged configuration (simplified implementation)
        merged_attrs = {**base_config.__dict__, **domain_config.__dict__}

        # Create new configuration object with merged attributes
        merged_config = type(base_config)(**merged_attrs)
        return merged_config
