#!/usr/bin/env python3
"""
Research Paper Search - Single Entry Point CLI Script

This script demonstrates the keyword-based search system built with Clean Architecture.
It loads keyword configurations from YAML and executes searches using different strategies
across multiple research domains including cybersecurity, post-quantum cryptography, and medical research.

Usage Examples:
    python search_research.py --strategy scada_security
    python search_research.py --strategy lattice_cryptography --limit 10
    python search_research.py --custom "quantum computing" "cryptography"
    python search_research.py --list-strategies

Educational Notes:
- Demonstrates Clean Architecture in practice with single entry point
- Shows how domain objects (KeywordConfig) drive application behavior
- Illustrates dependency injection with repository pattern
- Maintains separation of concerns while providing practical utility

Architecture Layers Used:
- Domain: KeywordConfig, SearchStrategy, SearchConfiguration value objects
- Application: ExecuteKeywordSearchUseCase orchestrates the search logic
- Infrastructure: InMemoryPaperRepository (with sample data for demonstration)
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
            f"   Required terms: {', '.join(strategy.required_terms) if strategy.required_terms else 'None'}"
        )
        if strategy.optional_terms:
            print(f"   Optional terms: {', '.join(strategy.optional_terms)}")
        if strategy.technology_terms:
            print(f"   Technology terms: {', '.join(strategy.technology_terms)}")
        print(f"   Max results: {strategy.max_results}")


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

    args = parser.parse_args()

    # Load configuration
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
