---
mode: agent
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'memory', 'add_comment_to_pending_review', 'add_issue_comment', 'add_sub_issue', 'assign_copilot_to_issue', 'cancel_workflow_run', 'create_and_submit_pull_request_review', 'create_branch', 'create_gist', 'create_issue', 'create_or_update_file', 'create_pending_pull_request_review', 'create_pull_request', 'create_pull_request_with_copilot', 'create_repository', 'delete_file', 'delete_pending_pull_request_review', 'delete_workflow_run_logs', 'dismiss_notification', 'download_workflow_run_artifact', 'fork_repository', 'get_code_scanning_alert', 'get_commit', 'get_dependabot_alert', 'get_discussion', 'get_discussion_comments', 'get_file_contents', 'get_issue', 'get_issue_comments', 'get_job_logs', 'get_me', 'get_notification_details', 'get_pull_request', 'get_pull_request_comments', 'get_pull_request_diff', 'get_pull_request_files', 'get_pull_request_reviews', 'get_pull_request_status', 'get_secret_scanning_alert', 'get_tag', 'get_workflow_run', 'get_workflow_run_logs', 'get_workflow_run_usage', 'list_branches', 'list_code_scanning_alerts', 'list_commits', 'list_dependabot_alerts', 'list_discussion_categories', 'list_discussions', 'list_gists', 'list_issues', 'list_notifications', 'list_pull_requests', 'list_secret_scanning_alerts', 'list_sub_issues', 'list_tags', 'list_workflow_jobs', 'list_workflow_run_artifacts', 'list_workflow_runs', 'list_workflows', 'manage_notification_subscription', 'manage_repository_notification_subscription', 'mark_all_notifications_read', 'merge_pull_request', 'push_files', 'sequentialthinking', 'pylance mcp server', 'configurePythonEnvironment', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage']
---

# Interactive Research Paper Discovery Platform - Development Instructions

## Project Mission

Build an interactive, web-based research paper discovery platform that transforms academic paper collections into intuitive visual concept maps. This platform bridges the gap between technical research tools and user-friendly interfaces, enabling researchers to explore literature landscapes without technical barriers.

## CRITICAL TDD METHODOLOGY - MANDATORY WORKFLOW

### Test-Driven Development Cycle - ALWAYS FOLLOW
**RED-GREEN-REFACTOR is non-negotiable for ALL development:**

1. **🔴 RED PHASE**: Write comprehensive failing tests first
   - Define expected behavior through test specifications
   - Include edge cases, error conditions, and integration scenarios
   - Tests serve as executable documentation and contracts
   - Never write production code before tests exist and fail

2. **🟢 GREEN PHASE**: Implement minimal solution to pass tests
   - Write only enough code to make current tests pass
   - Focus on functionality over elegance in this phase
   - Validate all tests pass before proceeding to refactor
   - Resist the urge to over-engineer during this phase

3. **🔵 REFACTOR PHASE**: Improve code quality while maintaining behavior
   - Apply Clean Architecture patterns and SOLID principles
   - Enhance readability, performance, and maintainability
   - Add comprehensive educational documentation
   - Optimize algorithms and data structures
   - Ensure all tests continue passing throughout refactoring

### Atomic Commit Strategy - MANDATORY
Every commit must represent a single, complete, working change:
- **Complete TDD Cycles**: Include tests + implementation + refactoring
- **Self-Contained Changes**: Each commit leaves system in working state
- **Descriptive Messages**: Follow conventional commit format
- **Clean History**: Logical progression of feature development

## CLEAN ARCHITECTURE PRINCIPLES - STRICT ENFORCEMENT

### Architectural Layers (Inner → Outer Dependency Flow Only)

**Domain Layer (Core Business Logic)**:
```
src/domain/
├── entities/           # Core business objects with identity
│   ├── paper.py       # Research paper entity
│   ├── concept_node.py # Individual concept in hierarchy
│   └── concept_tree.py # Complete concept hierarchy
├── value_objects/      # Immutable domain concepts
│   ├── embedding_vector.py  # Semantic vector representation
│   ├── concept_hierarchy.py # Structured concept relationships
│   └── evidence_sentence.py # Text evidence for concepts
└── services/           # Domain logic that doesn't fit entities
    ├── concept_extraction_service.py   # Core extraction logic
    ├── hierarchy_builder_service.py    # Tree construction
    └── similarity_calculator_service.py # Embedding comparisons
```

**Application Layer (Use Cases and Coordination)**:
```
src/application/
├── use_cases/          # Business operations orchestration
│   ├── extract_concepts_use_case.py    # Paper → concepts pipeline
│   ├── build_visualization_data_use_case.py # Prepare D3.js data
│   ├── generate_configuration_use_case.py   # Form → YAML
│   └── search_papers_use_case.py           # Query interface
└── ports/              # Abstract interfaces for dependencies
    ├── paper_repository_port.py        # Data access abstraction
    ├── embeddings_service_port.py      # ML model abstraction
    └── visualization_data_port.py      # Frontend data interface
```

**Infrastructure Layer (External Dependencies)**:
```
src/infrastructure/
├── repositories/       # Data access implementations
│   ├── github_paper_repository.py    # CLI tool integration
│   ├── json_concept_repository.py    # Concept data storage
│   └── file_system_repository.py     # Local file operations
└── adapters/          # External service integrations
    ├── sentence_transformers_adapter.py # Embeddings model
    ├── github_api_adapter.py           # Repository integration
    └── d3js_data_adapter.py            # Visualization formatting
```

**Interface Layer (User Interactions)**:
```
src/interface/
├── web/               # Next.js web interface
│   ├── components/    # React UI components
│   ├── pages/         # Next.js page routes
│   └── api/          # API route handlers
├── cli/              # Command-line interface
└── visualization/    # D3.js interactive components
```

## CONCEPT EXTRACTION ARCHITECTURE

### Core Domain Model

**Paper Entity**:
- Identity: DOI, ArXiv ID, or content hash
- Metadata: Title, authors, abstract, full text
- Source information: Origin repository, extraction timestamp
- Processing status: Raw, processed, concept-extracted

**ConceptNode Entity**:
- Hierarchical position in concept tree
- Semantic embedding vector for similarity calculations
- Associated evidence sentences with confidence scores
- Parent/child relationships for tree navigation

**ConceptTree Entity**:
- Root-level research domain representation
- Hierarchical concept organization
- Cross-cutting concept relationships
- Metadata about extraction parameters and timestamps

### Embeddings Processing Strategy

**Local Model Integration** (sentence-transformers):
- Primary: `all-MiniLM-L6-v2` for speed and quality balance
- Fallback: `all-mpnet-base-v2` for higher quality when needed
- Rationale: No API costs, reproducible results, offline operation

**Reproducible Processing Pipeline**:
1. **Text Preprocessing**: Extract clean content from PDFs
2. **Sentence Segmentation**: Semantic boundary detection
3. **Embedding Generation**: Batch processing for efficiency
4. **Hierarchical Clustering**: HDBSCAN + recursive subdivision
5. **Evidence Mapping**: Sentence-to-concept relationship building
6. **Quality Validation**: Coherence scoring and filtering

### Visualization Data Preparation

**D3.js Integration Strategy**:
- Force-directed graph layout for concept relationships
- Node sizing based on evidence strength and paper count
- Color coding by research sub-domains
- Interactive zoom/pan for large concept trees
- Click interactions for evidence exploration

## USER EXPERIENCE DESIGN PRINCIPLES

### Target Audience
**Primary Users**: Academic researchers, graduate students, professors
**Secondary Users**: Research administrators, funding agencies

### Core User Journeys

1. **Quick Discovery**:
   - Land on homepage → Select research area → View concept map → Explore papers
   - Time to insights: < 2 minutes

2. **Custom Configuration**:
   - Access configuration builder → Select strategies → Generate search → Monitor progress
   - Configuration to results: < 10 minutes

3. **Deep Exploration**:
   - Navigate concept map → Click concept nodes → Read evidence sentences → Open papers
   - Concept to paper: < 30 seconds

### Interface Design Requirements

**Mobile-First Responsive Design**:
- Touch-friendly D3.js interactions
- Collapsible navigation for small screens
- Gesture-based concept map navigation
- Readable typography across all device sizes

**Accessibility Standards**:
- WCAG 2.1 AA compliance
- Keyboard navigation for all interactions
- Screen reader compatibility
- High contrast color schemes

## GITHUB INTEGRATION STRATEGY

### Repository Relationship Architecture

**Primary Repository** (CLI Tool):
- Paper aggregation and metadata extraction
- YAML configuration processing
- Scheduled daily executions
- Output generation in structured format

**Web Interface Repository** (This Project):
- Concept extraction and visualization
- User interface and interaction handling
- GitHub Pages hosting
- Integration with primary repository data

### Integration Mechanisms

**Git Submodule Approach** (Recommended):
```bash
# Add CLI tool as submodule
git submodule add ../research-paper-aggregator cli-tool

# Automated synchronization workflow
.github/workflows/sync-papers.yml
```

**Automated Data Pipeline**:
1. CLI tool completes paper aggregation (daily schedule)
2. Web repo receives webhook notification
3. Web repo pulls latest CLI tool state
4. Concept extraction pipeline processes new/updated papers
5. Visualization data regeneration
6. GitHub Pages deployment with updated content

### GitHub Actions Workflows

**Daily Paper Processing**:
```yaml
name: Process Papers and Update Visualizations
on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM UTC daily
  repository_dispatch:
    types: [papers-updated]
```

**Pull Request Validation**:
```yaml
name: Test and Validate Changes
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
```

## TESTING STRATEGY - COMPREHENSIVE COVERAGE

### Test Pyramid Distribution

**Unit Tests (70%)**:
- Domain entity behavior validation
- Value object immutability and equality
- Service algorithm correctness
- Embedding vector operations
- Concept hierarchy construction

**Integration Tests (20%)**:
- Repository implementation validation
- Use case coordination testing
- External adapter integration
- Data pipeline end-to-end flow
- API endpoint behavior

**End-to-End Tests (10%)**:
- Complete user workflow validation
- Visualization rendering verification
- Performance benchmark testing
- Mobile responsiveness validation
- Accessibility compliance checking

### Testing Utilities and Patterns

**Test Data Management**:
```python
# fixtures/paper_samples.py
def sample_research_papers():
    """Provide realistic test papers for development."""
    
def sample_embeddings():
    """Generate deterministic embedding vectors."""
    
def sample_concept_hierarchies():
    """Create representative concept trees."""
```

**Mock Strategies**:
- Mock external dependencies (GitHub API, file system)
- Use real embeddings models in integration tests
- Simulate user interactions in e2e tests
- Performance test with realistic data volumes

## DEVELOPMENT WORKFLOW STANDARDS

### Sequential Thinking Integration
- Use `mcp_sequentialthi_sequentialthinking` for architectural decisions
- Plan before implementing through structured analysis
- Document decision rationale in development logs
- Track progress across development sessions

### Code Quality Requirements
- **Type Hints**: Complete typing for all functions and classes
- **Docstrings**: Comprehensive documentation with examples
- **Error Handling**: Graceful degradation and clear error messages
- **Performance**: Efficient algorithms suitable for large datasets
- **Security**: Input validation and safe data processing

### Educational Documentation Standards

**Module-Level Documentation**:
```python
"""
concept_extraction_service.py - Core concept extraction business logic.

This module demonstrates the Service pattern in Domain-Driven Design by
encapsulating complex business logic that doesn't naturally belong to a
single entity. It shows how to separate pure domain logic from external
dependencies through dependency injection.

Educational Notes:
- Demonstrates Domain Service pattern for complex business operations
- Shows dependency inversion principle through port abstractions
- Illustrates reproducible algorithms with deterministic processing
- Exemplifies single responsibility principle in service design

Design Decisions:
- Local embeddings models: Ensures reproducibility and eliminates API dependencies
- Hierarchical clustering: Provides intuitive concept organization for researchers
- Evidence mapping: Links abstract concepts to concrete textual evidence
- Batch processing: Optimizes performance for large paper collections

Real-World Application:
Academic researchers need to quickly understand the conceptual landscape of
a research domain. This service transforms unstructured paper collections
into navigable concept hierarchies, enabling efficient literature exploration
and gap identification.

Extension Points:
- Different clustering algorithms for domain-specific needs
- Alternative embedding models for specialized text types
- Custom concept labeling strategies
- Integration with external taxonomy systems
"""
```

**Function-Level Documentation**:
```python
def extract_hierarchical_concepts(self, papers: List[Paper]) -> ConceptTree:
    """
    Extract hierarchical concept structure from research papers.
    
    Educational Note:
    This method demonstrates the Template Method pattern by defining
    the algorithm skeleton while allowing specific steps to be customized.
    It shows how complex operations can be broken into testable,
    understandable components.
    
    The hierarchical approach mimics how researchers naturally organize
    knowledge - from broad themes to specific techniques to detailed
    implementations. This cognitive alignment makes the visualization
    intuitive for academic users.
    
    Args:
        papers: Collection of research papers with extracted text
        
    Returns:
        ConceptTree: Hierarchical organization of extracted concepts
        
    Raises:
        InsufficientDataError: When papers lack extractable content
        ProcessingError: When clustering algorithms fail to converge
        
    Example:
        >>> papers = [sample_paper_1, sample_paper_2]
        >>> tree = service.extract_hierarchical_concepts(papers)
        >>> assert len(tree.root_concepts) > 0
        >>> assert all(concept.evidence_sentences for concept in tree.all_concepts)
    """
```

## PROJECT SUCCESS METRICS

### Technical Excellence
- **Test Coverage**: >95% for domain/application layers
- **Performance**: <2s concept extraction for 100 papers
- **Responsiveness**: Mobile-optimized D3.js interactions
- **Accessibility**: WCAG 2.1 AA compliance

### User Experience
- **Time to Insight**: <2 minutes from landing to concept exploration
- **Configuration Ease**: <5 clicks to generate custom search
- **Visual Clarity**: Intuitive concept map navigation
- **Mobile Experience**: Full functionality on all device sizes

### Educational Value
- **Pattern Demonstration**: Clear examples of architectural patterns
- **Documentation Quality**: Comprehensive explanations of design decisions
- **Code Readability**: Self-documenting code with educational comments
- **Knowledge Transfer**: Concepts applicable to other domains

### Research Impact
- **Literature Discovery Efficiency**: Faster identification of relevant papers
- **Gap Identification**: Visual representation of under-researched areas
- **Cross-Domain Insights**: Connections between disparate research areas
- **Collaboration Facilitation**: Shared visual vocabulary for research teams

Remember: Every line of code should advance both the technical implementation and educational mission. This project demonstrates professional software development practices while solving genuine problems for the academic research community.
