"""
Atomic Concept Integration CLI

Command-line interface for integrating atomic concepts into the knowledge graph.

Educational Purpose:
- Demonstrates Clean Architecture wiring with Dependency Injection
- Shows how to compose use cases with infrastructure adapters
- Illustrates configuration management and error handling
- Examples of professional CLI design patterns

Real-World Application:
- Content management system batch operations
- Educational resource import tools
- Knowledge graph maintenance utilities
- Data migration and synchronization tools
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional
import json

# Application and domain imports
from src.application.use_cases.concept_integration import (
    IntegrateConceptsUseCase,
    GenerateLearningPathUseCase,
    IntegrationResult,
)

# Infrastructure imports
from src.infrastructure.adapters.json_concept_loader import JsonConceptLoader
from src.infrastructure.repositories.in_memory_repositories import (
    InMemoryConceptRepository,
    InMemoryMappingRepository,
)


class ConceptIntegrationCLI:
    """
    Command-line interface for atomic concept integration.

    Educational Patterns:
    - Facade Pattern: Simplifies complex subsystem interactions
    - Dependency Injection: Configurable component wiring
    - Command Pattern: Encapsulates operations as objects
    - Configuration Management: Centralized setup and customization

    Real-World Usage:
    - Batch processing tools for educational content
    - System administration utilities
    - Data pipeline components
    - Integration testing frameworks
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize CLI with dependency injection setup.

        Educational Pattern: Constructor Injection
        - Configures all dependencies in one place
        - Enables testing with mock implementations
        - Provides clear separation of concerns
        """
        # Set up logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self._logger = logging.getLogger(__name__)

        # Initialize infrastructure components
        self._concept_repository = InMemoryConceptRepository(self._logger)
        self._mapping_repository = InMemoryMappingRepository(self._logger)
        self._concept_loader = JsonConceptLoader(logger=self._logger)

        # Initialize use cases with dependency injection
        self._integration_use_case = IntegrateConceptsUseCase(
            concept_repository=self._concept_repository,
            mapping_repository=self._mapping_repository,
            concept_loader=self._concept_loader,
            logger=self._logger,
        )

        self._learning_path_use_case = GenerateLearningPathUseCase(
            concept_repository=self._concept_repository,
            mapping_repository=self._mapping_repository,
            logger=self._logger,
        )

        self._logger.info("Initialized Atomic Concept Integration CLI")

    def integrate_concepts(
        self,
        source_path: str,
        domain: str,
        force_update: bool = False,
        output_format: str = "json",
    ) -> bool:
        """
        Execute concept integration from source path.

        Educational Pattern: Use Case Orchestration
        - Delegates to application layer use case
        - Handles presentation layer concerns (formatting, output)
        - Provides user-friendly error messages and feedback

        Args:
            source_path: Path to concept source (file or directory)
            domain: Target domain for concepts
            force_update: Whether to update existing concepts
            output_format: Format for results (json, text, summary)

        Returns:
            True if integration succeeded, False otherwise
        """
        self._logger.info(f"Starting concept integration from {source_path}")

        try:
            # Validate source path exists
            if not Path(source_path).exists():
                print(f"ERROR: Source path does not exist: {source_path}")
                return False

            # Execute integration use case
            result = self._integration_use_case.execute(
                source_path=source_path, domain=domain, force_update=force_update
            )

            # Output results in requested format
            self._output_integration_results(result, output_format)

            # Return success/failure
            return result.result in [
                IntegrationResult.SUCCESS,
                IntegrationResult.PARTIAL_SUCCESS,
            ]

        except Exception as e:
            self._logger.error(f"Integration failed with exception: {str(e)}")
            print(f"ERROR: Integration failed: {str(e)}")
            return False

    def generate_learning_paths(
        self,
        target_concepts: list[str],
        domain: str,
        max_depth: int = 10,
        output_format: str = "text",
    ) -> bool:
        """
        Generate learning paths for target concepts.

        Educational Pattern: Query Operation
        - Read-only operation with formatted output
        - Handles multiple output formats for different use cases
        - Provides educational value through path explanation
        """
        self._logger.info(
            f"Generating learning paths for {len(target_concepts)} concepts"
        )

        try:
            # Execute learning path use case
            paths = self._learning_path_use_case.execute(
                target_concept_ids=target_concepts, domain=domain, max_depth=max_depth
            )

            # Output paths in requested format
            self._output_learning_paths(paths, output_format)

            return len(paths) > 0

        except Exception as e:
            self._logger.error(f"Learning path generation failed: {str(e)}")
            print(f"ERROR: Learning path generation failed: {str(e)}")
            return False

    def show_repository_status(self) -> None:
        """
        Display current repository statistics and status.

        Educational Pattern: Status Reporting
        - Provides visibility into system state
        - Supports monitoring and debugging
        - Demonstrates metrics collection
        """
        concept_stats = self._concept_repository.get_statistics()
        mapping_stats = self._mapping_repository.get_statistics()

        print("\n=== Repository Status ===")
        print(f"Concepts: {concept_stats.concept_count}")
        print(f"Mappings: {mapping_stats.mapping_count}")
        print(f"Relationships: {mapping_stats.total_relationships}")
        print(f"Queries executed: {concept_stats.queries_executed}")
        print(f"Cache hit ratio: {concept_stats.hit_ratio():.2%}")
        print(f"Last updated: {concept_stats.last_updated}")

    def list_domains(self) -> list[str]:
        """
        List all available domains in the repository.

        Educational Pattern: Data Discovery
        - Enables exploration of available content
        - Supports dynamic UI population
        - Provides metadata about repository contents
        """
        # Get all concepts and extract unique domains
        all_concepts = self._concept_repository.search(
            {}
        )  # Empty criteria = all concepts
        domains = {concept.domain for concept in all_concepts}

        print("\n=== Available Domains ===")
        for domain in sorted(domains):
            domain_concepts = self._concept_repository.find_by_domain(domain)
            print(f"{domain}: {len(domain_concepts)} concepts")

        return sorted(domains)

    def _output_integration_results(self, result, output_format: str) -> None:
        """
        Output integration results in specified format.

        Educational Pattern: Presentation Layer Logic
        - Separates business logic from presentation
        - Supports multiple output formats
        - Provides user-friendly result reporting
        """
        if output_format == "json":
            # JSON format for programmatic consumption
            result_data = {
                "result": result.result.value,
                "concepts_processed": result.concepts_processed,
                "concepts_created": result.concepts_created,
                "concepts_updated": result.concepts_updated,
                "relationships_created": result.relationships_created,
                "processing_time_ms": result.processing_time_ms,
                "domain": result.domain,
                "errors": result.errors,
                "warnings": result.warnings,
            }
            print(json.dumps(result_data, indent=2))

        elif output_format == "summary":
            # Brief summary format
            print(
                f"Integration {result.result.value}: {result.concepts_created} created, "
                f"{result.concepts_updated} updated in {result.processing_time_ms}ms"
            )

        else:  # text format (default)
            # Detailed text format for human reading
            print("\n=== Integration Results ===")
            print(f"Result: {result.result.value}")
            print(f"Domain: {result.domain}")
            print(f"Concepts processed: {result.concepts_processed}")
            print(f"Concepts created: {result.concepts_created}")
            print(f"Concepts updated: {result.concepts_updated}")
            print(f"Relationships created: {result.relationships_created}")
            print(f"Processing time: {result.processing_time_ms}ms")

            if result.errors:
                print(f"\nErrors ({len(result.errors)}):")
                for error in result.errors:
                    print(f"  - {error}")

            if result.warnings:
                print(f"\nWarnings ({len(result.warnings)}):")
                for warning in result.warnings:
                    print(f"  - {warning}")

    def _output_learning_paths(
        self, paths: dict[str, list[str]], output_format: str
    ) -> None:
        """Output learning paths in specified format."""
        if output_format == "json":
            print(json.dumps(paths, indent=2))

        else:  # text format (default)
            print("\n=== Learning Paths ===")
            for concept_id, path in paths.items():
                print(f"\nPath to '{concept_id}':")
                for i, step in enumerate(path, 1):
                    print(f"  {i}. {step}")

                if len(path) > 1:
                    print(f"  Total steps: {len(path)}")


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create CLI argument parser with educational command structure.

    Educational Pattern: Command Line Interface Design
    - Subcommands for different operations
    - Consistent argument naming and help text
    - Validation and type conversion
    """
    parser = argparse.ArgumentParser(
        description="Atomic Concept Integration CLI - Manage knowledge graph concepts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Integrate concepts from JSON file
  python concept_cli.py integrate ./concepts/math.json mathematics
  
  # Generate learning paths
  python concept_cli.py paths empty_set,power_set mathematics
  
  # Show repository status
  python concept_cli.py status
  
  # List available domains
  python concept_cli.py domains
        """,
    )

    # Global options
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Integration command
    integrate_parser = subparsers.add_parser(
        "integrate", help="Integrate concepts from source"
    )
    integrate_parser.add_argument(
        "source_path", help="Path to concept source (file or directory)"
    )
    integrate_parser.add_argument("domain", help="Target domain for concepts")
    integrate_parser.add_argument(
        "--force-update", action="store_true", help="Update existing concepts"
    )
    integrate_parser.add_argument(
        "--output-format",
        choices=["text", "json", "summary"],
        default="text",
        help="Output format for results",
    )

    # Learning paths command
    paths_parser = subparsers.add_parser(
        "paths", help="Generate learning paths for concepts"
    )
    paths_parser.add_argument(
        "concepts", help="Comma-separated list of target concept IDs"
    )
    paths_parser.add_argument("domain", help="Domain to search for paths")
    paths_parser.add_argument(
        "--max-depth", type=int, default=10, help="Maximum path depth (default: 10)"
    )
    paths_parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format for paths",
    )

    # Status command
    subparsers.add_parser("status", help="Show repository status and statistics")

    # Domains command
    subparsers.add_parser("domains", help="List available domains")

    return parser


def main() -> int:
    """
    Main CLI entry point.

    Educational Pattern: Application Entry Point
    - Handles command line parsing and validation
    - Coordinates high-level application flow
    - Provides consistent error handling and exit codes

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return 1

    try:
        # Initialize CLI with configuration
        cli = ConceptIntegrationCLI(verbose=args.verbose)

        # Execute command
        success = True

        if args.command == "integrate":
            success = cli.integrate_concepts(
                source_path=args.source_path,
                domain=args.domain,
                force_update=args.force_update,
                output_format=args.output_format,
            )

        elif args.command == "paths":
            concept_list = [c.strip() for c in args.concepts.split(",")]
            success = cli.generate_learning_paths(
                target_concepts=concept_list,
                domain=args.domain,
                max_depth=args.max_depth,
                output_format=args.output_format,
            )

        elif args.command == "status":
            cli.show_repository_status()

        elif args.command == "domains":
            cli.list_domains()

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
