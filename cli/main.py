#!/usr/bin/env python3
"""
Research Paper Aggregator - Main CLI Entry Point

This is the primary command-line interface for the research paper aggregator.
Demonstrates Clean Architecture with clear separation of concerns.

Usage:
    python cli/main.py --help
    python cli/main.py search --keywords "cybersecurity quantum cryptography"
    python cli/main.py extract --papers ./papers/
    python cli/main.py gui --port 8080

Educational Notes:
- Shows Clean Architecture in practice
- Demonstrates command pattern for CLI operations
- Implements dependency injection for testability
"""

import sys
import argparse
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    """Main entry point demonstrating Clean Architecture principles."""
    parser = argparse.ArgumentParser(
        description="Research Paper Aggregator - Clean Architecture Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search --keywords "quantum cryptography post-quantum"
  %(prog)s extract --papers ./research_papers/
  %(prog)s web --port 3000
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for research papers")
    search_parser.add_argument("--keywords", required=True, help="Search keywords")
    search_parser.add_argument("--config", help="Configuration file path")

    # Extract command
    extract_parser = subparsers.add_parser(
        "extract", help="Extract concepts from papers"
    )
    extract_parser.add_argument(
        "--papers", required=True, help="Path to papers directory"
    )

    # Web interface command
    web_parser = subparsers.add_parser("web", help="Start web interface")
    web_parser.add_argument("--port", type=int, default=3000, help="Port number")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route to appropriate handler
    if args.command == "search":
        handle_search(args)
    elif args.command == "extract":
        handle_extract(args)
    elif args.command == "web":
        handle_web(args)


def handle_search(args):
    """Handle search command using Clean Architecture patterns."""
    print(f"🔍 Searching for papers with keywords: {args.keywords}")

    # Dependency injection following Clean Architecture
    repository = ArxivPaperRepository()
    use_case = ExecuteKeywordSearchUseCase(repository)

    # Execute use case
    results = use_case.execute(args.keywords)

    print(f"✅ Found {len(results)} papers")
    for paper in results[:5]:  # Show first 5
        print(f"  📄 {paper.title}")


def handle_extract(args):
    """Handle concept extraction command."""
    print(f"🧠 Extracting concepts from papers in: {args.papers}")
    # Implementation would go here


def handle_web(args):
    """Handle web interface startup."""
    print(f"🌐 Starting web interface on port {args.port}")
    print("Run: cd src/web && npm run dev")


if __name__ == "__main__":
    main()
