#!/usr/bin/env python3
"""
Research Paper Search and Concept Extraction - Single Entry Point CLI Script

This script demonstrates the keyword-based search system and concept extraction
built with Clean Architecture. It loads keyword configurations from YAML and
executes searches using different strategies across multiple research domains
including cybersecurity, post-quantum cryptography, and medical research.

New: Concept extraction capabilities for analyzing collected papers and
generating concept maps, embeddings, and visualization data.

Usage Examples:
    # Search and download papers
    python search_cli.py --strategy scada_security
    python search_cli.py --strategy lattice_cryptography --limit 10
    python search_cli.py --custom "quantum computing" "cryptography"
    python search_cli.py --list-strategies

    # Extract concepts from papers
    python search_cli.py extract-concepts --domain heart_rate_variability
    python search_cli.py extract-concepts --domain all --force
    python search_cli.py concept-stats --domain cybersecurity_water_infrastructure
    python search_cli.py export-viz --domain post_quantum_cryptography

Educational Notes:
- Demonstrates Clean Architecture in practice with single entry point
- Shows how domain objects (KeywordConfig) drive application behavior
- Illustrates dependency injection with repository pattern
- Maintains separation of concerns while providing practical utility
- Extends functionality with concept extraction and analysis

Architecture Layers Used:
- Domain: KeywordConfig, SearchStrategy, Concept, PaperConcepts entities
- Application: ExecuteKeywordSearchUseCase, ExtractPaperConceptsUseCase
- Infrastructure: InMemoryPaperRepository, JSONConceptRepository, PDFTextExtractor
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from domain.value_objects.keyword_config import KeywordConfig
from application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)
from infrastructure.repositories.arxiv_paper_repository import (
    ArxivPaperRepository,
)
from domain.entities.research_paper import ResearchPaper
from domain.services.paper_download_service import PaperDownloadService
from datetime import datetime, timezone

# Import batch processor
from batch_processor import run_batch_processing

# Import concept extraction components
try:
    from application.use_cases.extract_paper_concepts_use_case import (
        ExtractPaperConceptsUseCase,
    )
    from infrastructure.pdf_extractor import PyPDF2TextExtractor
    from infrastructure.json_concept_repository import JSONConceptRepository

    CONCEPT_EXTRACTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Concept extraction not available: {e}")
    CONCEPT_EXTRACTION_AVAILABLE = False


def setup_sample_repository() -> InMemoryPaperRepository:
    """
    Create sample repository with HRV research papers for demonstration.

    Educational Notes:
    - In a real system, this would connect to actual databases or APIs
    - This demonstrates the Repository Pattern's flexibility
    - Shows how infrastructure can be swapped without changing domain/application logic
    """
    sample_papers = [
        ResearchPaper(
            title="Heart Rate Variability in Traumatic Brain Injury: A Systematic Review",
            authors=["Smith, J.", "Johnson, A.", "Brown, K."],
            abstract="This systematic review examines heart rate variability changes following traumatic brain injury. We analyzed 45 studies involving 2,847 patients with TBI. Results show significant reductions in RMSSD and frequency domain measures in acute TBI patients compared to controls.",
            publication_date=datetime(2023, 3, 15, tzinfo=timezone.utc),
            doi="10.1016/j.clinph.2023.03.015",
            venue="Clinical Neurophysiology",
            citation_count=42,
            keywords=[
                "heart rate variability",
                "traumatic brain injury",
                "autonomic dysfunction",
                "RMSSD",
            ],
        ),
        ResearchPaper(
            title="Apple Watch-Based HRV Monitoring for Concussion Assessment",
            authors=["Davis, M.", "Wilson, R.", "Taylor, S."],
            abstract="We evaluated the feasibility of using Apple Watch for continuous HRV monitoring in concussion patients. Our study included 78 athletes with sport-related concussions. Apple Watch HRV metrics showed significant correlations with clinical recovery measures.",
            publication_date=datetime(2023, 8, 22, tzinfo=timezone.utc),
            doi="10.1089/neu.2023.0145",
            venue="Journal of Neurotrauma",
            citation_count=28,
            keywords=[
                "Apple Watch",
                "concussion",
                "heart rate variability",
                "wearable devices",
                "sports medicine",
            ],
        ),
        ResearchPaper(
            title="RMSSD and pNN50 as Biomarkers of Autonomic Recovery After Mild TBI",
            authors=["Garcia, L.", "Martinez, C.", "Anderson, P."],
            abstract="This longitudinal study tracked HRV recovery in 156 mild TBI patients over 6 months. RMSSD and pNN50 showed progressive improvement, with normalization occurring at 3-4 months post-injury. These metrics may serve as objective biomarkers of autonomic recovery.",
            publication_date=datetime(2023, 11, 8, tzinfo=timezone.utc),
            doi="10.1017/S1355617723000456",
            venue="Journal of the International Neuropsychological Society",
            citation_count=35,
            keywords=[
                "RMSSD",
                "pNN50",
                "mild traumatic brain injury",
                "longitudinal study",
                "biomarkers",
            ],
        ),
        ResearchPaper(
            title="Frequency Domain Analysis of HRV in Severe Traumatic Brain Injury",
            authors=["Thompson, K.", "Lee, H.", "Clark, D."],
            abstract="We performed frequency domain analysis of HRV in 89 severe TBI patients in the ICU. Very low frequency power was significantly reduced in non-survivors. LF/HF ratio showed prognostic value for 6-month outcomes.",
            publication_date=datetime(2022, 12, 3, tzinfo=timezone.utc),
            doi="10.1097/CCM.0000000000005234",
            venue="Critical Care Medicine",
            citation_count=58,
            keywords=[
                "frequency domain",
                "severe traumatic brain injury",
                "ICU",
                "prognosis",
                "mortality",
            ],
        ),
        ResearchPaper(
            title="Machine Learning Approaches to HRV-Based TBI Classification",
            authors=["Patel, R.", "Singh, A.", "Zhou, Y."],
            abstract="We developed machine learning models using HRV features to classify TBI severity. Random forest models achieved 87% accuracy in distinguishing mild from moderate-severe TBI using time and frequency domain features.",
            publication_date=datetime(2023, 5, 17, tzinfo=timezone.utc),
            doi="10.1109/TBME.2023.3271845",
            venue="IEEE Transactions on Biomedical Engineering",
            citation_count=51,
            keywords=[
                "machine learning",
                "classification",
                "random forest",
                "feature extraction",
                "TBI severity",
            ],
        ),
    ]

    repository = InMemoryPaperRepository()
    for paper in sample_papers:
        repository.save_paper(paper)

    return repository


def load_keyword_config(
    config_path: str = "config/search_keywords.yaml",
) -> KeywordConfig:
    """
    Load keyword configuration from YAML file.

    Educational Notes:
    - Demonstrates how domain objects encapsulate business logic
    - Shows configuration-driven behavior using value objects
    - Illustrates error handling for missing configuration files
    """
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Error: Configuration file not found: {config_path}")
        print("Make sure you're running from the project root directory.")
        sys.exit(1)

    try:
        return KeywordConfig.from_yaml_file(str(config_file))
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def print_search_results(
    results: List[ResearchPaper], strategy_name: str, limit: Optional[int] = None
):
    """
    Display search results in a formatted manner.

    Educational Notes:
    - Demonstrates separation of presentation logic from business logic
    - Shows how domain entities can be used for display purposes
    - Illustrates practical output formatting for research use
    """
    display_results = results[:limit] if limit else results

    print(f"\n🔍 Search Results for '{strategy_name}' strategy:")
    print(f"Found {len(results)} papers (showing {len(display_results)})")
    print("=" * 80)

    for i, paper in enumerate(display_results, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors)}")
        print(f"   Journal: {paper.venue}")
        print(f"   Date: {paper.publication_date.strftime('%Y-%m-%d')}")
        print(f"   DOI: {paper.doi}")
        print(f"   Keywords: {', '.join(paper.keywords)}")
        print(f"   Abstract: {paper.abstract[:200]}...")

    if len(results) > len(display_results):
        print(f"\n... and {len(results) - len(display_results)} more results")


def list_available_strategies(keyword_config: KeywordConfig):
    """
    Display all available search strategies from the configuration.

    Educational Notes:
    - Shows how domain objects expose their internal structure appropriately
    - Demonstrates configuration introspection capabilities
    - Illustrates user-friendly display of system capabilities
    """
    print("\n📋 Available Search Strategies:")
    print("=" * 50)

    for strategy_name, strategy in keyword_config.search_strategies.items():
        print(f"\n🎯 {strategy_name}")
        print(f"   Description: {strategy.description}")
        print(
            f"   Primary keywords: {', '.join(strategy.primary_keywords) if strategy.primary_keywords else 'None'}"
        )
        if strategy.secondary_keywords:
            print(f"   Secondary keywords: {', '.join(strategy.secondary_keywords)}")
        if strategy.exclusion_keywords:
            print(f"   Exclusion keywords: {', '.join(strategy.exclusion_keywords)}")
        print(f"   Max results: {strategy.search_limit}")


def handle_concept_commands(args):
    """
    Handle concept extraction related subcommands.

    Educational Notes:
    - Demonstrates subcommand routing in CLI applications
    - Shows conditional module importing for optional features
    - Implements comprehensive error handling for missing dependencies
    """
    if not CONCEPT_EXTRACTION_AVAILABLE:
        print("❌ Concept extraction not available. Missing dependencies.")
        print("Please ensure all required packages are installed.")
        sys.exit(1)

    if args.command == "extract-concepts":
        handle_extract_concepts(args)
    elif args.command == "concept-stats":
        handle_concept_stats(args)
    elif args.command == "export-viz":
        handle_export_viz(args)
    elif args.command == "batch-process":
        handle_batch_processing(args)


def handle_batch_processing(args):
    """
    Handle batch processing command for all configurations and strategies.

    Args:
        args: Parsed command line arguments containing batch processing parameters

    Educational Notes:
    - Demonstrates delegation to specialized processing modules
    - Shows how CLI interfaces can wrap complex business logic
    - Implements parameter validation and error handling
    - Provides user feedback for long-running operations
    """
    print("🚀 Initiating batch processing for all configurations...")
    print(f"📂 Config directory: {args.config_dir}")
    print(f"📁 Output directory: {args.output_dir}")
    print(f"📄 Max papers per strategy: {args.max_papers}")
    print(f"🔗 Data source: {args.source}")
    print("=" * 60)

    try:
        # Validate directories exist
        config_path = Path(args.config_dir)
        if not config_path.exists():
            print(f"❌ Configuration directory does not exist: {config_path}")
            sys.exit(1)

        # Run batch processing with specified parameters
        run_batch_processing(
            config_dir=args.config_dir,
            output_dir=args.output_dir,
            max_papers=args.max_papers,
            use_arxiv=(args.source == "arxiv"),
        )

    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        sys.exit(1)


def handle_extract_concepts(args):
    """Extract concepts from papers in a domain."""
    print(f"🧠 Extracting concepts from domain: {args.domain}")

    # Set up concept extraction use case
    pdf_extractor = PyPDF2TextExtractor()
    concept_repository = JSONConceptRepository(Path("concept_storage"))
    extract_use_case = ExtractPaperConceptsUseCase(pdf_extractor, concept_repository)

    try:
        if args.domain == "all":
            # Process all domains
            outputs_dir = Path("outputs")
            if not outputs_dir.exists():
                print("❌ No outputs directory found. Please run some searches first.")
                sys.exit(1)

            for domain_dir in outputs_dir.iterdir():
                if domain_dir.is_dir() and not domain_dir.name.startswith("."):
                    print(f"\n📂 Processing domain: {domain_dir.name}")
                    process_domain(
                        extract_use_case, domain_dir.name, domain_dir, args.force
                    )
        else:
            # Process specific domain - map to actual directory name
            domain_mapping = {
                "heart_rate_variability": "2025-08-05_Comprehensive HRV Research",
                "hrv": "2025-08-05_Comprehensive HRV Research",
                "tbi_hrv": "2025-08-05_TBI and HRV Research",
                "cryptography": "2025-08-05_Post-Quantum Cryptography",
                "post_quantum": "2025-08-05_Post-Quantum Cryptography",
                "digital_signatures": "2025-08-05_Hash-Based Digital Signatures",
                "infrastructure": "2025-08-05_Critical Infrastructure Security",
                "water_utility": "2025-08-05_Water Utility Incident Response",
            }

            if args.papers_dir:
                papers_dir = Path(args.papers_dir)
            else:
                # Find actual directory name
                actual_domain = domain_mapping.get(args.domain, args.domain)
                papers_dir = Path(f"outputs/{actual_domain}")

            if not papers_dir.exists():
                print(f"❌ Papers directory not found: {papers_dir}")
                if args.domain in domain_mapping:
                    print(f"Domain '{args.domain}' maps to: {actual_domain}")
                print("Available domains:")
                outputs_dir = Path("outputs")
                if outputs_dir.exists():
                    for item in outputs_dir.iterdir():
                        if item.is_dir():
                            # Show both actual name and mapped aliases
                            aliases = [
                                k for k, v in domain_mapping.items() if v == item.name
                            ]
                            alias_str = (
                                f" (aliases: {', '.join(aliases)})" if aliases else ""
                            )
                            print(f"  - {item.name}{alias_str}")
                print("Make sure you have downloaded papers for this domain first.")
                sys.exit(1)

            process_domain(extract_use_case, args.domain, papers_dir, args.force)

    except Exception as e:
        print(f"❌ Concept extraction failed: {e}")
        sys.exit(1)


def handle_concept_stats(args):
    """Show concept extraction statistics."""
    concept_repository = JSONConceptRepository(Path("concept_storage"))

    try:
        stats = concept_repository.get_extraction_statistics(args.domain)

        print(f"\n📊 Concept Extraction Statistics")
        if args.domain:
            print(f"Domain: {args.domain}")
        else:
            print("All Domains")
        print("=" * 50)

        if "error" in stats:
            print(f"❌ Error: {stats['error']}")
            return

        print(f"📄 Total Papers: {stats.get('total_papers', 0)}")
        print(f"🧠 Total Concepts: {stats.get('total_concepts', 0)}")
        print(f"📊 Unique Concepts: {stats.get('unique_concepts', 0)}")
        print(f"⚖️ Avg Concepts/Paper: {stats.get('concepts_per_paper', 0)}")

        if "domains" in stats and stats["domains"]:
            print(f"\n📂 Domain Breakdown:")
            for domain_name, domain_stats in stats["domains"].items():
                print(
                    f"  • {domain_name}: {domain_stats.get('paper_count', 0)} papers, "
                    f"{domain_stats.get('concept_count', 0)} concepts"
                )

        if "concept_frequency" in stats and stats["concept_frequency"]:
            print(f"\n🔝 Top Concepts:")
            for i, (concept, freq) in enumerate(
                list(stats["concept_frequency"].items())[:10], 1
            ):
                print(f"  {i:2}. {concept} (frequency: {freq})")

    except Exception as e:
        print(f"❌ Failed to get statistics: {e}")
        sys.exit(1)


def handle_export_viz(args):
    """Export concept data for visualization."""
    concept_repository = JSONConceptRepository(Path("concept_storage"))

    try:
        output_path = Path(args.output_dir) / args.domain
        concept_repository.export_domain_for_visualization(args.domain, output_path)

        print(f"✅ Visualization data exported for domain: {args.domain}")
        print(f"📁 Files saved to: {output_path}")
        print(f"🌐 Ready for web visualization!")

    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)


def process_domain(extract_use_case, domain_name, papers_dir, force_reextraction):
    """Process a single domain directory for concept extraction."""
    try:
        # Look for metadata file
        metadata_file = papers_dir / "metadata.json"

        results = extract_use_case.extract_concepts_from_domain(
            domain_name=domain_name,
            papers_directory=papers_dir,
            metadata_file=metadata_file if metadata_file.exists() else None,
            force_reextraction=force_reextraction,
        )

        print(f"✅ Successfully processed {len(results)} papers in {domain_name}")

        # Show quick stats
        total_concepts = sum(pc.total_concept_count for pc in results)
        avg_concepts = total_concepts / len(results) if results else 0
        print(
            f"🧠 Extracted {total_concepts} total concepts (avg: {avg_concepts:.1f} per paper)"
        )

    except Exception as e:
        print(f"❌ Failed to process domain {domain_name}: {e}")


def main():
    """
    Main CLI entry point demonstrating keyword-based search system.

    Educational Notes:
    - Shows Clean Architecture in practice with single entry point
    - Demonstrates dependency injection and inversion of control
    - Illustrates how application layer orchestrates domain and infrastructure
    """
    parser = argparse.ArgumentParser(
        description="Search HRV research papers using keyword-based strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --strategy broad_hrv_research
  %(prog)s --strategy tbi_focused --limit 5
  %(prog)s --custom "heart rate variability" "Apple Watch"
  %(prog)s --list-strategies
        """,
    )

    parser.add_argument(
        "--strategy",
        "-s",
        help="Use a predefined search strategy from the configuration",
    )

    parser.add_argument(
        "--custom",
        "-c",
        nargs="+",
        help="Perform custom search with specified keywords",
    )

    parser.add_argument(
        "--limit", "-l", type=int, help="Limit the number of results displayed"
    )

    parser.add_argument(
        "--list-strategies",
        action="store_true",
        help="List all available search strategies",
    )

    parser.add_argument(
        "--download",
        "-d",
        action="store_true",
        help="Download PDFs of found papers (uses arXiv when available)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        default="outputs",
        help="Output directory for downloaded papers (default: outputs)",
    )

    parser.add_argument(
        "--source",
        choices=["sample", "arxiv"],
        default="sample",
        help="Data source: 'sample' for demo data, 'arxiv' for real arXiv papers",
    )

    parser.add_argument(
        "--config",
        default="config/search_keywords.yaml",
        help="Path to keyword configuration file (default: config/search_keywords.yaml)",
    )

    # Concept extraction subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Extract concepts command
    extract_parser = subparsers.add_parser(
        "extract-concepts", help="Extract concepts from downloaded papers"
    )
    extract_parser.add_argument(
        "--domain",
        required=True,
        help="Research domain to process (e.g., heart_rate_variability, cybersecurity_water_infrastructure, all)",
    )
    extract_parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract concepts even if they already exist",
    )
    extract_parser.add_argument(
        "--papers-dir",
        help="Directory containing papers (default: outputs/DOMAIN_NAME)",
    )

    # Concept statistics command
    stats_parser = subparsers.add_parser(
        "concept-stats", help="Show concept extraction statistics"
    )
    stats_parser.add_argument(
        "--domain", help="Domain to analyze (default: all domains)"
    )

    # Export visualization data command
    viz_parser = subparsers.add_parser(
        "export-viz", help="Export concept data for web visualization"
    )
    viz_parser.add_argument("--domain", required=True, help="Domain to export")
    viz_parser.add_argument(
        "--output-dir",
        default="concept_data",
        help="Output directory for visualization files (default: concept_data)",
    )

    # Batch processing command
    batch_parser = subparsers.add_parser(
        "batch-process", help="Process all configurations and strategies automatically"
    )
    batch_parser.add_argument(
        "--config-dir",
        default="config",
        help="Directory containing configuration files (default: config)",
    )
    batch_parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Output directory for organized results (default: outputs)",
    )
    batch_parser.add_argument(
        "--max-papers",
        type=int,
        default=100,
        help="Maximum papers per strategy (default: 100)",
    )
    batch_parser.add_argument(
        "--source",
        choices=["sample", "arxiv"],
        default="arxiv",
        help="Data source for batch processing (default: arxiv)",
    )

    args = parser.parse_args()

    # Handle concept extraction commands
    if args.command:
        handle_concept_commands(args)
        return

    # Load configuration for search commands
    print("🔄 Loading keyword configuration...")
    keyword_config = load_keyword_config(args.config)

    # Set up repository based on source choice
    if args.source == "arxiv":
        print("🔄 Setting up arXiv API repository...")
        repository = ArxivPaperRepository()
    else:
        print("🔄 Setting up sample research paper repository...")
        repository = setup_sample_repository()

    # Create use case (dependency injection)
    search_use_case = ExecuteKeywordSearchUseCase(repository)

    # Set up download service if needed
    download_service = None
    if args.download:
        download_service = PaperDownloadService(args.output_dir)

    # Handle different command modes
    if args.list_strategies:
        list_available_strategies(keyword_config)
        return

    # Execute search based on arguments
    results = None
    strategy_name = None

    if args.strategy:
        # Execute predefined strategy
        if args.strategy not in keyword_config.search_strategies:
            print(f"Error: Strategy '{args.strategy}' not found in configuration.")
            print("Use --list-strategies to see available options.")
            sys.exit(1)

        print(f"🔄 Executing '{args.strategy}' search strategy...")
        results = search_use_case.execute_strategy(args.strategy)
        strategy_name = args.strategy
        print_search_results(results, args.strategy, args.limit)

    elif args.custom:
        # Execute custom search
        print(f"🔄 Executing custom search with keywords: {', '.join(args.custom)}")
        results = search_use_case.execute_custom_search(args.custom)
        strategy_name = "custom_search"
        print_search_results(results, "custom search", args.limit)

    else:
        # Default: execute the default strategy
        default_strategy = keyword_config.search_configuration.default_strategy
        print(f"🔄 No strategy specified, using default: '{default_strategy}'")
        results = search_use_case.execute_strategy(default_strategy)
        strategy_name = default_strategy
        print_search_results(results, default_strategy, args.limit)

    print(f"\n✅ Search completed successfully!")

    # Handle downloading if requested
    if args.download and results:
        print(f"\n📥 Starting paper downloads...")
        download_service = PaperDownloadService(base_output_dir=args.output_dir)

        def progress_callback(current: int, total: int, paper_title: str):
            print(f"  📄 [{current}/{total}] Downloading: {paper_title[:60]}...")

        try:
            downloaded_files = download_service.download_papers(
                papers=results,  # results is already a List[ResearchPaper]
                strategy_name=strategy_name,
                progress_callback=progress_callback,
            )

            print(
                f"\n✅ Download completed! {len(downloaded_files)} papers downloaded."
            )
            print(
                f"📁 Files saved to: {download_service._create_output_directory(strategy_name)}"
            )

        except Exception as e:
            print(f"\n❌ Download failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
