#!/usr/bin/env python3
"""
Research Paper Aggregator - Main Menu Interface

A user-friendly menu system for academic research paper discovery and download.
Simply run this file to get started with research aggregation across multiple domains.

Educational Purpose:
This file demonstrates several important Computer Science concepts and design patterns:

Design Patterns Implemented:
- Command Pattern: Menu choices execute specific commands/actions
- Factory Pattern: Dynamic loading of configuration files
- Strategy Pattern: Different search strategies are pluggable
- Facade Pattern: Simple interface hiding complex underlying systems

SOLID Principles Demonstrated:
- Single Responsibility: Each method has one clear purpose
- Open/Closed: Easy to add new research domains without modifying existing code
- Dependency Inversion: Depends on abstractions (KeywordConfig) not concrete implementations

Architecture Pattern:
- Clean Architecture: UI layer depends on application layer, not infrastructure
- Separation of Concerns: Menu logic separate from business logic
- Dependency Injection: Use cases receive their dependencies

Usage:
    python3 main.py

Features:
- Interactive menu for research domain selection
- Strategy selection within each domain
- Automated paper discovery and download
- Clean Architecture implementation for educational purposes
- Domain-driven design with proper layering
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.domain.value_objects.keyword_config import KeywordConfig
from src.application.use_cases.execute_keyword_search_use_case import (
    ExecuteKeywordSearchUseCase,
)
from src.infrastructure.repositories.arxiv_paper_repository import ArxivPaperRepository
from src.infrastructure.repositories.in_memory_paper_repository import (
    InMemoryPaperRepository,
)


class ResearchMenuInterface:
    """
    Interactive menu interface for research paper aggregation.

    This class demonstrates several important CS concepts:

    Design Pattern: Facade Pattern
    - Provides a simple interface to complex subsystem operations
    - Hides the complexity of Clean Architecture layers from the user
    - Single point of interaction for the entire system

    Object-Oriented Principles:
    - Encapsulation: Menu logic is contained within this class
    - Single Responsibility: Only handles user interaction and menu flow
    - Information Hiding: Internal methods are private (prefixed with _)

    Educational Notes:
    - Shows proper file system operations with pathlib
    - Demonstrates exception handling best practices
    - Uses type hints for better code documentation
    - Implements user input validation and error recovery

    Real-world Applications:
    - Command-line interfaces for enterprise applications
    - Administrative tools and utilities
    - System configuration and setup wizards
    """

    def __init__(self):
        self.config_dir = Path(__file__).parent / "config"
        self.available_configs = self._discover_config_files()

    def _discover_config_files(self) -> Dict[str, Path]:
        """Discover all YAML configuration files in the config directory."""
        configs = {}
        if not self.config_dir.exists():
            print(f"❌ Config directory not found: {self.config_dir}")
            return configs

        for config_file in self.config_dir.glob("*.yaml"):
            # Create user-friendly names from filenames
            name = config_file.stem.replace("_", " ").title()
            configs[name] = config_file

        return configs

    def _load_config(self, config_path: Path) -> Optional[KeywordConfig]:
        """Load a keyword configuration from file."""
        try:
            return KeywordConfig.from_yaml_file(str(config_path))
        except Exception as e:
            print(f"❌ Error loading config {config_path}: {e}")
            return None

    def _display_welcome(self):
        """Display welcome message and system info."""
        print("\n" + "=" * 70)
        print("🔍📚 RESEARCH PAPER AGGREGATOR")
        print("=" * 70)
        print("🎯 Intelligent Academic Research Discovery System")
        print("🏗️  Clean Architecture • 🤖 arXiv Integration • 📥 Auto-Download")
        print("=" * 70)

    def _display_domain_menu(self) -> Optional[str]:
        """Display research domain selection menu."""
        if not self.available_configs:
            print("❌ No configuration files found in config directory!")
            return None

        print("\n📂 Available Research Domains:")
        print("-" * 50)

        domain_list = list(self.available_configs.keys())
        for i, domain in enumerate(domain_list, 1):
            config_file = self.available_configs[domain].name
            print(f"  {i}. {domain}")
            print(f"     📄 {config_file}")
            print()

        print("  0. Exit")
        print("-" * 50)

        while True:
            try:
                choice = input("\n🎯 Select research domain (number): ").strip()

                if choice == "0":
                    return None

                choice_num = int(choice)
                if 1 <= choice_num <= len(domain_list):
                    selected_domain = domain_list[choice_num - 1]
                    print(f"\n✅ Selected: {selected_domain}")
                    return selected_domain
                else:
                    print("❌ Invalid choice. Please select a number from the menu.")

            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                return None

    def _display_strategy_menu(
        self, config: KeywordConfig, domain_name: str
    ) -> Optional[str]:
        """Display strategy selection menu for the chosen domain."""
        strategies = config.list_strategies()

        print(f"\n🔬 Research Strategies for {domain_name}:")
        print("-" * 60)

        for i, strategy_name in enumerate(strategies, 1):
            strategy = config.get_strategy(strategy_name)
            if strategy:
                print(f"  {i}. {strategy.name}")
                print(f"     📝 {strategy.description}")
                print(
                    f"     🎯 {len(strategy.primary_keywords)} primary + {len(strategy.secondary_keywords)} secondary terms"
                )
                print(f"     📊 Max results: {strategy.search_limit}")
                print()

        print("  0. Back to domain selection")
        print("-" * 60)

        while True:
            try:
                choice = input("\n🔍 Select research strategy (number): ").strip()

                if choice == "0":
                    return None

                choice_num = int(choice)
                if 1 <= choice_num <= len(strategies):
                    selected_strategy = strategies[choice_num - 1]
                    print(f"\n✅ Selected: {selected_strategy}")
                    return selected_strategy
                else:
                    print("❌ Invalid choice. Please select a number from the menu.")

            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Returning to domain menu...")
                return None

    def _display_action_menu(self) -> tuple[bool, bool, int]:
        """Display action selection menu (search options)."""
        print("\n⚙️  Search Configuration:")
        print("-" * 40)
        print("  1. Preview papers (no download)")
        print("  2. Download papers to local folder")
        print("  0. Back to strategy selection")
        print("-" * 40)

        # Get action choice
        while True:
            try:
                action = input("\n📥 Choose action (number): ").strip()
                if action == "0":
                    return False, False, 0
                elif action == "1":
                    download = False
                    break
                elif action == "2":
                    download = True
                    break
                else:
                    print("❌ Invalid choice. Please select 1, 2, or 0.")
            except KeyboardInterrupt:
                return False, False, 0

        # Get paper limit
        while True:
            try:
                limit_input = input(
                    "\n📊 Number of papers to retrieve (default 10): "
                ).strip()
                if not limit_input:
                    limit = 10
                    break
                limit = int(limit_input)
                if limit > 0:
                    break
                else:
                    print("❌ Please enter a positive number.")
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                return False, False, 0

        # Get data source choice
        print("\n🌐 Data Source:")
        print("  1. arXiv (real papers)")
        print("  2. Sample data (for testing)")

        while True:
            try:
                source = input("\n🔗 Select data source (default 1): ").strip()
                if not source or source == "1":
                    use_arxiv = True
                    break
                elif source == "2":
                    use_arxiv = False
                    break
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")
            except KeyboardInterrupt:
                return False, False, 0

        return use_arxiv, download, limit

    def _execute_search(
        self,
        config: KeywordConfig,
        strategy_name: str,
        use_arxiv: bool,
        download: bool,
        limit: int,
    ):
        """Execute the research paper search."""
        print(f"\n🚀 Executing search...")
        print("-" * 50)

        try:
            # Set up repository based on user choice
            if use_arxiv:
                print("🔄 Setting up arXiv API repository...")
                repository = ArxivPaperRepository()
            else:
                print("🔄 Setting up sample data repository...")
                repository = InMemoryPaperRepository()

            # Create use case
            use_case = ExecuteKeywordSearchUseCase(
                repository=repository,
                config_path=None,  # We already have the config loaded
                keyword_config=config,
            )

            # Execute search
            print(f"🔍 Searching for papers using '{strategy_name}' strategy...")
            results = use_case.execute_strategy(
                strategy_name=strategy_name, max_results=limit, download_papers=download
            )

            # Display results
            print(f"\n✅ Search completed successfully!")
            print(f"📊 Found {len(results)} papers")

            if download and results:
                print(f"📥 Papers downloaded to: outputs/")

            # Show first few results
            if results:
                print(f"\n📋 Results Preview (showing first 3):")
                print("=" * 60)
                for i, paper in enumerate(results[:3], 1):
                    print(f"{i}. {paper.title}")
                    print(
                        f"   👥 Authors: {', '.join(paper.authors[:2])}{'...' if len(paper.authors) > 2 else ''}"
                    )
                    print(f"   📅 Date: {paper.publication_date}")
                    if paper.venue:
                        print(f"   📰 Journal: {paper.venue}")
                    print()

                if len(results) > 3:
                    print(f"   ... and {len(results) - 3} more papers")

        except Exception as e:
            print(f"❌ Error during search: {e}")
            print("Please check your internet connection and try again.")

    def run(self):
        """Run the interactive menu system."""
        self._display_welcome()

        while True:
            # Step 1: Select research domain
            domain_name = self._display_domain_menu()
            if not domain_name:
                print("\n👋 Thank you for using Research Paper Aggregator!")
                break

            # Step 2: Load configuration
            config_path = self.available_configs[domain_name]
            config = self._load_config(config_path)
            if not config:
                print("❌ Failed to load configuration. Returning to main menu.")
                continue

            while True:
                # Step 3: Select strategy
                strategy_name = self._display_strategy_menu(config, domain_name)
                if not strategy_name:
                    break  # Back to domain selection

                # Step 4: Configure search options
                use_arxiv, download, limit = self._display_action_menu()
                if not use_arxiv and not download and limit == 0:
                    continue  # Back to strategy selection

                # Step 5: Execute search
                self._execute_search(config, strategy_name, use_arxiv, download, limit)

                # Ask if user wants to do another search
                print("\n🔄 Search Operations:")
                print("  1. Search with different strategy")
                print("  2. Switch to different research domain")
                print("  0. Exit program")

                while True:
                    try:
                        next_action = input(
                            "\n➡️  What would you like to do next? "
                        ).strip()
                        if next_action == "0":
                            print("\n👋 Thank you for using Research Paper Aggregator!")
                            return
                        elif next_action == "1":
                            break  # Continue with strategy selection
                        elif next_action == "2":
                            break  # Go back to domain selection
                        else:
                            print("❌ Invalid choice. Please select 0, 1, or 2.")
                    except KeyboardInterrupt:
                        print("\n\n👋 Thank you for using Research Paper Aggregator!")
                        return

                if next_action == "2":
                    break  # Break out of strategy loop to domain selection


def main():
    """Main entry point for the Research Paper Aggregator."""
    try:
        menu = ResearchMenuInterface()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using Research Paper Aggregator!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists.")


if __name__ == "__main__":
    main()
