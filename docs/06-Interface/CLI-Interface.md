# Command Line Interface (CLI) Design

> **Context**: The CLI serves as the primary interface for researchers and developers to interact with the Academic Paper Discovery System. It transforms user commands into use case executions while providing an intuitive, efficient research workflow.

## 🎯 Interface Design Philosophy

The CLI embodies the **principle of least surprise** - experienced researchers should be able to accomplish common tasks intuitively while having access to advanced features when needed. The interface follows Unix philosophy: do one thing well, be composable, and provide clear feedback.

**Design Goals:**
- **Research-Focused**: Commands map directly to research workflows
- **Composable**: Output can be piped to other tools for analysis
- **Extensible**: New research domains can be added through configuration
- **Educational**: Help and examples teach both tool usage and research methodology

## 🏗️ CLI Architecture and Clean Architecture Integration

### Interface Layer Responsibilities

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import click

@dataclass
class CLIContext:
    """
    CLI execution context carrying state across commands.
    
    Educational Value: Demonstrates how interface layers
    maintain minimal state while delegating business logic
    to appropriate application layer use cases.
    """
    config_path: Optional[str] = None
    output_format: str = "table"
    verbose: bool = False
    debug: bool = False
    working_directory: str = "."
    
    def get_config_file(self) -> str:
        """Resolve configuration file path."""
        if self.config_path:
            return self.config_path
        
        # Default configuration discovery
        possible_configs = [
            f"{self.working_directory}/config/default.yaml",
            f"{self.working_directory}/config.yaml",
            "~/.academic-papers/config.yaml"
        ]
        
        for config_path in possible_configs:
            if os.path.exists(os.path.expanduser(config_path)):
                return config_path
        
        raise ConfigurationError("No configuration file found")

class CLICommand(ABC):
    """
    Abstract base for all CLI commands.
    
    Educational Value: Shows command pattern implementation
    in interface layer, enabling consistent command handling
    and easy extension for new research operations.
    """
    
    @abstractmethod
    def execute(self, 
                args: Dict[str, Any], 
                context: CLIContext) -> 'CommandResult':
        """Execute the command with given arguments and context."""
        pass
    
    @abstractmethod
    def get_help_text(self) -> str:
        """Provide comprehensive help including examples."""
        pass
    
    @abstractmethod
    def validate_arguments(self, args: Dict[str, Any]) -> None:
        """Validate command arguments before execution."""
        pass
```

### Main CLI Entry Point

```python
import click
from pathlib import Path
from src.interface.cli.commands import (
    SearchCommand,
    ConfigCommand,
    AnalyzeCommand,
    ExportCommand
)
from src.application.use_cases.execute_keyword_search_use_case import ExecuteKeywordSearchUseCase
from src.infrastructure.repositories.in_memory_paper_repository import InMemoryPaperRepository

@click.group()
@click.option('--config', '-c', 
              help='Configuration file path')
@click.option('--format', '-f', 
              type=click.Choice(['table', 'json', 'csv', 'markdown']),
              default='table',
              help='Output format')
@click.option('--verbose', '-v', 
              is_flag=True,
              help='Enable verbose output')
@click.option('--debug', 
              is_flag=True,
              help='Enable debug mode')
@click.pass_context
def cli(ctx, config, format, verbose, debug):
    """
    Academic Paper Discovery System CLI.
    
    A comprehensive tool for discovering, analyzing, and organizing
    academic research papers with advanced concept extraction and
    knowledge graph capabilities.
    
    Educational Value: This CLI demonstrates clean architecture
    principles by serving as a thin interface layer that delegates
    all business logic to use cases in the application layer.
    
    Examples:
        # Basic search in medical research domain
        academic-papers search "heart rate variability" --domain medical
        
        # Literature review with date constraints
        academic-papers search "machine learning healthcare" \\
            --start-date 2020-01-01 --max-results 100
        
        # Export results for further analysis
        academic-papers search "traumatic brain injury" \\
            --format csv --output results.csv
    """
    # Initialize CLI context
    ctx.ensure_object(dict)
    ctx.obj['context'] = CLIContext(
        config_path=config,
        output_format=format,
        verbose=verbose,
        debug=debug,
        working_directory=str(Path.cwd())
    )
    
    # Set up logging based on verbosity
    setup_logging(verbose, debug)
    
    # Validate configuration accessibility
    try:
        config_file = ctx.obj['context'].get_config_file()
        if verbose:
            click.echo(f"Using configuration: {config_file}")
    except ConfigurationError as e:
        click.echo(f"Configuration error: {e}", err=True)
        ctx.exit(1)
```

### Search Command Implementation

```python
@cli.command()
@click.argument('terms', nargs=-1, required=True)
@click.option('--domain', '-d',
              help='Research domain configuration (medical, cs, etc.)')
@click.option('--start-date', 
              type=click.DateTime(formats=['%Y-%m-%d']),
              help='Earliest publication date (YYYY-MM-DD)')
@click.option('--end-date',
              type=click.DateTime(formats=['%Y-%m-%d']),
              help='Latest publication date (YYYY-MM-DD)')
@click.option('--max-results', '-n',
              type=click.IntRange(1, 1000),
              default=50,
              help='Maximum number of results')
@click.option('--sort-by',
              type=click.Choice(['relevance', 'date', 'citations']),
              default='relevance',
              help='Sort criteria for results')
@click.option('--output', '-o',
              type=click.Path(),
              help='Output file path')
@click.option('--extract-concepts',
              is_flag=True,
              help='Extract concepts from discovered papers')
@click.pass_context
def search(ctx, terms, domain, start_date, end_date, max_results, 
           sort_by, output, extract_concepts):
    """
    Search for academic papers using advanced discovery algorithms.
    
    TERMS: One or more search terms (space-separated)
    
    This command demonstrates the interface layer's role in clean
    architecture: validating input, coordinating with use cases,
    and formatting output appropriately.
    
    Examples:
        # Basic search
        academic-papers search "machine learning"
        
        # Medical research with date constraints
        academic-papers search "heart rate variability" "exercise" \\
            --domain medical --start-date 2020-01-01
        
        # Export with concept extraction
        academic-papers search "traumatic brain injury" \\
            --extract-concepts --format json --output tbi_research.json
    """
    context = ctx.obj['context']
    
    try:
        # Create and execute search command
        search_command = SearchCommand()
        
        # Prepare arguments
        search_args = {
            'terms': list(terms),
            'domain': domain,
            'start_date': start_date,
            'end_date': end_date,
            'max_results': max_results,
            'sort_by': sort_by,
            'extract_concepts': extract_concepts
        }
        
        # Validate arguments
        search_command.validate_arguments(search_args)
        
        # Execute search through application layer
        result = search_command.execute(search_args, context)
        
        # Format and display results
        output_formatter = OutputFormatterFactory.create(context.output_format)
        formatted_output = output_formatter.format_search_results(result.papers)
        
        if output:
            # Write to file
            with open(output, 'w') as f:
                f.write(formatted_output)
            click.echo(f"Results written to {output}")
        else:
            # Display to console
            click.echo(formatted_output)
        
        # Display summary statistics
        if context.verbose:
            click.echo(f"\nSearch completed:")
            click.echo(f"  Papers found: {len(result.papers)}")
            click.echo(f"  Search time: {result.execution_time:.2f}s")
            if extract_concepts:
                click.echo(f"  Concepts extracted: {len(result.concepts)}")
    
    except ValidationError as e:
        click.echo(f"Validation error: {e}", err=True)
        ctx.exit(1)
    except SearchError as e:
        click.echo(f"Search error: {e}", err=True)
        ctx.exit(1)
    except Exception as e:
        if context.debug:
            raise
        click.echo(f"Unexpected error: {e}", err=True)
        ctx.exit(1)
```

### Command Pattern Implementation

```python
class SearchCommand(CLICommand):
    """
    Search command implementation using clean architecture principles.
    
    Educational Value: Demonstrates how interface layer commands
    delegate to application layer use cases while handling
    interface-specific concerns like validation and formatting.
    """
    
    def __init__(self):
        # Initialize use case with dependencies
        # Note: In production, use dependency injection container
        self._search_use_case = self._create_search_use_case()
    
    def _create_search_use_case(self) -> ExecuteKeywordSearchUseCase:
        """
        Create use case with required dependencies.
        
        Educational Value: Shows dependency assembly at interface layer.
        In production systems, this would be handled by a DI container.
        """
        # Create infrastructure dependencies
        paper_repository = InMemoryPaperRepository()
        embedding_service = SentenceTransformerEmbeddingService()
        
        # Create application services
        paper_discovery_service = PaperDiscoveryService(
            paper_repository=paper_repository,
            embedding_service=embedding_service
        )
        
        # Create use case
        return ExecuteKeywordSearchUseCase(
            paper_discovery_service=paper_discovery_service
        )
    
    def validate_arguments(self, args: Dict[str, Any]) -> None:
        """
        Validate command arguments at interface layer.
        
        Educational Value: Shows separation between interface
        validation (format, ranges) and domain validation (business rules).
        """
        # Validate search terms
        if not args['terms'] or len(args['terms']) == 0:
            raise ValidationError("At least one search term required")
        
        # Validate date range
        if args['start_date'] and args['end_date']:
            if args['start_date'] > args['end_date']:
                raise ValidationError("Start date must be before end date")
        
        # Validate domain
        if args['domain']:
            available_domains = self._get_available_domains()
            if args['domain'] not in available_domains:
                raise ValidationError(
                    f"Unknown domain '{args['domain']}'. "
                    f"Available: {', '.join(available_domains)}"
                )
    
    def execute(self, 
                args: Dict[str, Any], 
                context: CLIContext) -> 'CommandResult':
        """
        Execute search command by delegating to use case.
        
        Educational Value: Shows how interface layer transforms
        CLI arguments into domain objects and delegates to use cases.
        """
        # Load configuration
        config = self._load_configuration(context, args['domain'])
        
        # Create search query domain object
        search_query = self._create_search_query(args, config)
        
        # Execute use case
        search_request = SearchRequest(
            query=search_query,
            extract_concepts=args['extract_concepts']
        )
        
        use_case_result = self._search_use_case.execute(search_request)
        
        # Transform use case result to CLI result
        return CommandResult(
            papers=use_case_result.papers,
            concepts=use_case_result.concepts if args['extract_concepts'] else [],
            execution_time=use_case_result.execution_time,
            metadata=use_case_result.metadata
        )
    
    def _create_search_query(self, 
                            args: Dict[str, Any], 
                            config: ResearchDomainConfig) -> SearchQuery:
        """
        Transform CLI arguments to domain search query.
        
        Educational Value: Shows interface layer responsibility
        for transforming external representations to domain objects.
        """
        # Create date range if specified
        date_range = None
        if args['start_date'] or args['end_date']:
            date_range = DateRange(
                start_date=args['start_date'],
                end_date=args['end_date']
            )
        
        # Map CLI sort criteria to domain enum
        sort_criteria_map = {
            'relevance': SortCriteria.RELEVANCE,
            'date': SortCriteria.PUBLICATION_DATE_DESC,
            'citations': SortCriteria.CITATION_COUNT_DESC
        }
        
        return SearchQuery(
            terms=args['terms'],
            date_range=date_range,
            domain_filters=config.domain_filters,
            max_results=args['max_results'],
            sort_criteria=sort_criteria_map[args['sort_by']]
        )
    
    def get_help_text(self) -> str:
        """Comprehensive help text with research workflow examples."""
        return """
        Search for academic papers using advanced discovery algorithms.
        
        RESEARCH WORKFLOW EXAMPLES:
        
        1. Literature Review Workflow:
           # Discover recent papers in a field
           academic-papers search "heart rate variability" \\
               --start-date 2020-01-01 --max-results 100
           
           # Extract concepts for analysis
           academic-papers search "HRV exercise training" \\
               --extract-concepts --format json --output hrv_concepts.json
        
        2. Systematic Review Workflow:
           # Search specific medical domain
           academic-papers search "traumatic brain injury" "cognitive assessment" \\
               --domain medical --max-results 200
           
           # Refine by publication period
           academic-papers search "TBI cognitive assessment" \\
               --start-date 2015-01-01 --end-date 2023-12-31
        
        3. Cross-Domain Research:
           # Compare concepts across domains
           academic-papers search "machine learning healthcare" \\
               --domain cs --extract-concepts
           
           academic-papers search "artificial intelligence medical diagnosis" \\
               --domain medical --extract-concepts
        
        OUTPUT FORMATS:
        - table: Human-readable console output (default)
        - json: Machine-readable structured data
        - csv: Spreadsheet-compatible format
        - markdown: Documentation-friendly format
        
        CONFIGURATION:
        The CLI uses YAML configuration files to define research domains,
        search strategies, and default parameters. Configuration files
        are searched in this order:
        1. --config argument
        2. ./config/default.yaml
        3. ./config.yaml
        4. ~/.academic-papers/config.yaml
        """
```

## 🔧 Configuration and Domain Management

### Configuration Command

```python
@cli.command()
@click.option('--list-domains', 
              is_flag=True,
              help='List available research domains')
@click.option('--show-config',
              is_flag=True, 
              help='Display current configuration')
@click.option('--validate',
              is_flag=True,
              help='Validate configuration files')
@click.option('--create-template',
              type=click.Path(),
              help='Create configuration template at path')
@click.pass_context
def config(ctx, list_domains, show_config, validate, create_template):
    """
    Manage system configuration and research domains.
    
    Educational Value: Shows how CLI provides configuration
    management capabilities while delegating to appropriate
    application services.
    
    Examples:
        # See available research domains
        academic-papers config --list-domains
        
        # Validate current configuration
        academic-papers config --validate
        
        # Create new configuration template
        academic-papers config --create-template ./my-config.yaml
    """
    context = ctx.obj['context']
    config_command = ConfigCommand()
    
    if list_domains:
        domains = config_command.list_available_domains(context)
        click.echo("Available research domains:")
        for domain in domains:
            click.echo(f"  {domain.name}: {domain.description}")
    
    elif show_config:
        config_data = config_command.show_current_config(context)
        formatted_config = yaml.dump(config_data, default_flow_style=False)
        click.echo("Current configuration:")
        click.echo(formatted_config)
    
    elif validate:
        validation_result = config_command.validate_configuration(context)
        if validation_result.is_valid:
            click.echo("✓ Configuration is valid")
        else:
            click.echo("✗ Configuration validation failed:")
            for error in validation_result.errors:
                click.echo(f"  {error}")
    
    elif create_template:
        config_command.create_template(create_template)
        click.echo(f"Configuration template created at {create_template}")
    
    else:
        click.echo("No action specified. Use --help for options.")
```

## 📊 Output Formatting and Results Display

### Flexible Output Formatting

```python
from abc import ABC, abstractmethod
from typing import List
import json
import csv
from tabulate import tabulate

class OutputFormatter(ABC):
    """
    Abstract output formatter for different display formats.
    
    Educational Value: Demonstrates strategy pattern for
    output formatting in interface layer.
    """
    
    @abstractmethod
    def format_search_results(self, papers: List[ResearchPaper]) -> str:
        """Format search results for display."""
        pass
    
    @abstractmethod
    def format_concepts(self, concepts: List[Concept]) -> str:
        """Format extracted concepts for display."""
        pass

class TableOutputFormatter(OutputFormatter):
    """Console-friendly table output formatter."""
    
    def format_search_results(self, papers: List[ResearchPaper]) -> str:
        """Format papers as readable table."""
        if not papers:
            return "No papers found."
        
        # Prepare table data
        table_data = []
        for paper in papers:
            table_data.append([
                paper.title[:50] + ("..." if len(paper.title) > 50 else ""),
                ", ".join(paper.authors[:2]) + ("..." if len(paper.authors) > 2 else ""),
                paper.publication_date.year if paper.publication_date else "N/A",
                paper.doi.value if paper.doi else "N/A"
            ])
        
        headers = ["Title", "Authors", "Year", "DOI"]
        return tabulate(table_data, headers=headers, tablefmt="grid")
    
    def format_concepts(self, concepts: List[Concept]) -> str:
        """Format concepts as readable table."""
        if not concepts:
            return "No concepts extracted."
        
        table_data = []
        for concept in concepts:
            table_data.append([
                concept.name,
                concept.category,
                f"{concept.confidence:.2f}",
                concept.frequency
            ])
        
        headers = ["Concept", "Category", "Confidence", "Frequency"]
        return tabulate(table_data, headers=headers, tablefmt="simple")

class JSONOutputFormatter(OutputFormatter):
    """Machine-readable JSON output formatter."""
    
    def format_search_results(self, papers: List[ResearchPaper]) -> str:
        """Format papers as JSON."""
        papers_data = [self._paper_to_dict(paper) for paper in papers]
        return json.dumps(papers_data, indent=2, default=str)
    
    def format_concepts(self, concepts: List[Concept]) -> str:
        """Format concepts as JSON."""
        concepts_data = [self._concept_to_dict(concept) for concept in concepts]
        return json.dumps(concepts_data, indent=2, default=str)
    
    def _paper_to_dict(self, paper: ResearchPaper) -> Dict[str, Any]:
        """Convert research paper to dictionary representation."""
        return {
            "id": paper.id.value,
            "title": paper.title,
            "authors": paper.authors,
            "publication_date": paper.publication_date,
            "doi": paper.doi.value if paper.doi else None,
            "abstract": paper.abstract,
            "keywords": paper.keywords,
            "metadata": paper.metadata
        }

class OutputFormatterFactory:
    """Factory for creating appropriate output formatters."""
    
    _formatters = {
        'table': TableOutputFormatter,
        'json': JSONOutputFormatter,
        'csv': CSVOutputFormatter,
        'markdown': MarkdownOutputFormatter
    }
    
    @classmethod
    def create(cls, format_type: str) -> OutputFormatter:
        """Create formatter for specified format type."""
        if format_type not in cls._formatters:
            raise ValueError(f"Unknown format type: {format_type}")
        
        return cls._formatters[format_type]()
```

## 🎓 Educational Value and Design Patterns

### Interface Layer Principles

**Key Responsibilities:**
1. **Input Validation**: Format and range validation (not business rule validation)
2. **Argument Parsing**: Transform CLI arguments to domain objects
3. **Use Case Coordination**: Delegate business logic to application layer
4. **Output Formatting**: Present results in user-friendly formats
5. **Error Handling**: Provide meaningful error messages and exit codes

**Educational Benefits:**
- Demonstrates clean separation between interface and business logic
- Shows command pattern implementation for extensible CLI design
- Illustrates strategy pattern for flexible output formatting
- Provides examples of configuration management in command-line tools

### Design Patterns Applied

1. **Command Pattern**: Each CLI command encapsulates a complete operation
2. **Strategy Pattern**: Pluggable output formatters for different display needs
3. **Factory Pattern**: Create appropriate formatters and use cases
4. **Template Method**: Consistent command execution flow with customization points

## 🔗 Related Concepts

- [[Web-Interface]]: Browser-based alternative to CLI interface
- [[API-Design]]: RESTful service interfaces for programmatic access
- [[Execute-Keyword-Search-UseCase]]: Primary application layer use case
- [[Configuration-Management-UseCase]]: Configuration handling business logic
- [[Research-Domain-Configuration]]: YAML-based domain configuration system

## 🚀 Usage Examples

### Basic Research Workflow

```bash
# Start research on a topic
academic-papers search "heart rate variability exercise"

# Refine search with domain and date constraints
academic-papers search "HRV training adaptation" \
    --domain medical --start-date 2020-01-01

# Extract concepts for analysis
academic-papers search "HRV exercise training" \
    --extract-concepts --format json --output hrv_analysis.json
```

### Advanced Research Pipeline

```bash
# Systematic literature review workflow
academic-papers search "traumatic brain injury cognitive assessment" \
    --domain medical --max-results 200 \
    --format csv --output tbi_papers.csv

# Analyze configuration for reproducibility
academic-papers config --show-config > research_config.yaml

# Validate setup before major analysis
academic-papers config --validate
```

---

*The CLI interface demonstrates how the interface layer in clean architecture can provide powerful, user-friendly access to complex research capabilities while maintaining clear separation of concerns and excellent educational value.*

#interface #cli #commands #research-workflow #educational
