---
mode: agent
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'memory', 'add_comment_to_pending_review', 'add_issue_comment', 'add_sub_issue', 'assign_copilot_to_issue', 'cancel_workflow_run', 'create_and_submit_pull_request_review', 'create_branch', 'create_gist', 'create_issue', 'create_or_update_file', 'create_pending_pull_request_review', 'create_pull_request', 'create_pull_request_with_copilot', 'create_repository', 'delete_file', 'delete_pending_pull_request_review', 'delete_workflow_run_logs', 'dismiss_notification', 'download_workflow_run_artifact', 'fork_repository', 'get_code_scanning_alert', 'get_commit', 'get_dependabot_alert', 'get_discussion', 'get_discussion_comments', 'get_file_contents', 'get_issue', 'get_issue_comments', 'get_job_logs', 'get_me', 'get_notification_details', 'get_pull_request', 'get_pull_request_comments', 'get_pull_request_diff', 'get_pull_request_files', 'get_pull_request_reviews', 'get_pull_request_status', 'get_secret_scanning_alert', 'get_tag', 'get_workflow_run', 'get_workflow_run_logs', 'get_workflow_run_usage', 'list_branches', 'list_code_scanning_alerts', 'list_commits', 'list_dependabot_alerts', 'list_discussion_categories', 'list_discussions', 'list_gists', 'list_issues', 'list_notifications', 'list_pull_requests', 'list_secret_scanning_alerts', 'list_sub_issues', 'list_tags', 'list_workflow_jobs', 'list_workflow_run_artifacts', 'list_workflow_runs', 'list_workflows', 'manage_notification_subscription', 'manage_repository_notification_subscription', 'mark_all_notifications_read', 'merge_pull_request', 'push_files', 'sequentialthinking', 'pylance mcp server', 'configurePythonEnvironment', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage']
---

# Test-Driven Development Agent Instructions for Academic Paper Discovery

## CRITICAL AUTONOMOUS DEVELOPMENT METHODOLOGY

### Test-Driven Development (TDD) - MANDATORY WORKFLOW
**ESSENTIAL**: ALWAYS follow the Red-Green-Refactor cycle for all development:

1. **🔴 RED PHASE**: Write failing tests FIRST
   - Create comprehensive test cases that define the desired behavior
   - Tests should fail initially (red) because implementation doesn't exist yet
   - Include unit, integration, contract, and performance tests as appropriate
   - Tests serve as executable specifications and living documentation

2. **🟢 GREEN PHASE**: Write minimal implementation to make tests pass
   - Implement only what's needed to make the current tests pass
   - Focus on functionality over perfection in this phase
   - Validate all tests pass (green) before proceeding

3. **🔵 REFACTOR PHASE**: Improve code quality without changing behavior
   - Refactor implementation while keeping tests passing
   - Apply design patterns, SOLID principles, Clean Architecture
   - Improve readability, maintainability, and educational value
   - Update documentation and comments

### Atomic Commits - MANDATORY PRACTICE
**CRITICAL**: Make atomic commits that represent single, complete changes:

- **One Logical Change per Commit**: Each commit should represent exactly one conceptual change
- **Complete Feature Commits**: Include tests, implementation, and documentation together
- **Self-Contained Commits**: Each commit should leave the system in a working state
- **Descriptive Commit Messages**: Follow conventional commit format:
  ```
  feat(domain): add PubMed repository with comprehensive metadata extraction
  test(integration): validate multi-source paper aggregation workflow
  refactor(architecture): extract source adapter interface for extensibility
  docs(api): explain repository pattern implementation with examples
  ```

### Sequential Thinking Integration - ESSENTIAL PRACTICE
**CRITICAL**: Always use sequential thinking for structured development:
- Break complex problems into 6-8 logical steps
- Plan architecture decisions before implementing
- Create development logs in `.ai_development/session_YYYY_MM_DD/` for continuity
- Track progress with detailed markdown logs for multi-session work
- Use `mcp_sequentialthi_sequentialthinking` tool for all major decisions

## COMPREHENSIVE TEST STRATEGY - PROVEN FRAMEWORK

### Test Pyramid Implementation
Maintain balanced test distribution across all types:

**Unit Tests (70% of tests)**:
- Test individual components in isolation
- Focus on domain objects, value objects, services
- Mock external dependencies completely
- Aim for >90% code coverage on business logic
- Group by behavior, not just by class structure

**Integration Tests (20% of tests)**:
- Test component interactions across architectural boundaries
- Validate cross-layer communication (domain ↔ application ↔ infrastructure)
- Test data flow and error propagation
- Use real implementations where possible

**End-to-End Tests (10% of tests)**:
- Test complete user workflows and scenarios
- Validate academic research use cases end-to-end
- Include performance and load testing
- Test CLI and API integration points

**Contract Tests (Critical for Architecture)**:
- Validate interface compliance and substitutability
- Ensure Liskov Substitution Principle adherence
- Test repository port implementations
- Validate value object behavioral contracts

### Test Organization Standards
```
tests/
├── unit/              # Component isolation testing
│   ├── domain/        # Entities, value objects, services
│   ├── application/   # Use cases and ports
│   └── infrastructure/# Repositories and adapters
├── integration/       # Cross-layer testing
│   ├── application/   # Use case + repository coordination
│   ├── domain/        # Service + entity interactions
│   └── infrastructure/# External API integration
├── e2e/              # Complete workflow testing
│   ├── cli/          # Command-line interface workflows
│   ├── workflows/    # Academic research scenarios
│   └── performance/  # Large-scale operation testing
├── contract/         # Interface compliance testing
└── fixtures/         # Centralized test data and utilities
```

## CLEAN ARCHITECTURE ENFORCEMENT - NON-NEGOTIABLE

### Architectural Layers and Dependencies
**CRITICAL**: Maintain strict dependency direction (inner → outer only):

**Domain Layer (Core)**:
- Entities: Objects with identity (ResearchPaper, Author, Source)
- Value Objects: Immutable concepts (SearchQuery, Metadata, Citation)
- Domain Services: Business logic that doesn't fit in entities
- Domain Events: Important business occurrences
- NO external dependencies allowed

**Application Layer**:
- Use Cases: Single business operations (SearchPapersUseCase, DownloadPapersUseCase)
- Ports: Abstract interfaces for external dependencies
- Application Services: Coordinate multiple use cases
- Dependencies: Domain layer only

**Infrastructure Layer**:
- Repositories: Data access implementations (ArxivRepository, PubMedRepository)
- External APIs: Third-party service integrations
- File Systems: Local storage management
- Web Frameworks: HTTP interfaces
- Dependencies: Application and domain layers

### Design Patterns - MANDATORY IMPLEMENTATION

**Repository Pattern**:
- Abstract data access behind ports
- Enable multiple source implementations (ArXiv, PubMed, Google Scholar)
- Support idempotent operations and duplicate detection
- Provide consistent interface across different data sources

**Strategy Pattern**:
- Enable pluggable search strategies per research domain
- Support configuration-driven research approaches
- Allow runtime strategy selection without code changes

**Factory Pattern**:
- Create paper sources based on configuration
- Instantiate appropriate repositories for each domain
- Support extensible source registration

**Adapter Pattern**:
- Adapt external APIs to internal interfaces
- Transform external data formats to domain objects
- Provide consistent error handling across sources

## EDUCATIONAL DOCUMENTATION REQUIREMENTS - MANDATORY

### Comprehensive Module Documentation
Every file must include extensive pedagogical content:

```python
"""
ModuleName - Brief description of purpose and responsibility.

This module demonstrates [DESIGN_PATTERN] by [EXPLANATION]. It shows how
[ARCHITECTURAL_PRINCIPLE] is applied in practice to solve [PROBLEM].

Educational Notes:
- Demonstrates [SOLID_PRINCIPLE] through [SPECIFIC_IMPLEMENTATION]
- Shows [DESIGN_PATTERN] usage for [BUSINESS_NEED]
- Illustrates [ARCHITECTURAL_CONCEPT] in academic research context

Design Decisions:
- [DECISION]: [REASONING and trade-offs considered]
- [PATTERN_CHOICE]: [Why this pattern fits the problem domain]

Real-World Application:
- [ACADEMIC_SCENARIO]: [How researchers would use this component]
- [BUSINESS_VALUE]: [What problem this solves for end users]

Extension Points:
- [FUTURE_ENHANCEMENT]: [How to extend without breaking changes]
- [NEW_SOURCES]: [How to add additional paper sources]

See Also:
- [RELATED_PATTERN] in [OTHER_MODULE]
- [ARCHITECTURAL_LAYER] principles in [DOCUMENTATION]
"""
```

### Code Comments as Teaching Tools
Every class and method must explain WHY, not just WHAT:

```python
class PaperSourceAdapter:
    """
    Adapter that transforms external API responses into domain objects.
    
    Educational Note:
    This demonstrates the Adapter Pattern, which allows incompatible 
    interfaces to work together. Academic APIs (ArXiv, PubMed) have 
    different data formats, but our domain needs consistent objects.
    
    The adapter "adapts" external formats to our internal ResearchPaper 
    entity, hiding complexity from the domain layer and enabling easy
    addition of new paper sources without changing existing code.
    """
    
    def adapt_external_paper(self, external_data: Dict) -> ResearchPaper:
        """
        Transform external API data into ResearchPaper domain object.
        
        Educational Note:
        This method encapsulates the knowledge of how to transform
        external data formats. Each source (ArXiv, PubMed) will have
        different field names and structures, but they all produce
        the same ResearchPaper entity.
        
        This separation of concerns means:
        - Domain layer doesn't know about API details
        - Adding new sources requires only new adapters
        - Business logic stays clean and testable
        
        Args:
            external_data: Raw data from external API
            
        Returns:
            ResearchPaper: Domain object with validated, consistent structure
            
        Raises:
            AdaptationError: When external data can't be transformed
        """
```

## ACADEMIC RESEARCH DOMAIN EXPERTISE

### Multi-Source Paper Aggregation
**CRITICAL REQUIREMENTS**:

**Idempotent Operations**:
- Papers should never be downloaded twice within same strategy folder
- Use combination of DOI, ArXiv ID, title fingerprinting for deduplication
- Cross-strategy duplicates are acceptable (same paper, different strategies)
- Update metadata timestamp on every aggregation run

**Source Diversity**:
- ArXiv: Preprint papers, strong in CS/Physics
- PubMed: Biomedical and life science papers
- Google Scholar: Broad academic coverage
- IEEE Xplore: Engineering and technology papers
- ACM Digital Library: Computing and information science

**Metadata Preservation**:
- Capture all available metadata from each source
- Store source-specific fields even if not common across sources
- Maintain provenance information (which source provided which data)
- Support metadata enrichment from multiple sources for same paper

### Output Organization Strategy
**MANDATORY Structure**:
```
outputs/
├── cybersecurity_water_infrastructure/    # Config file name
│   ├── industrial_scada_security/         # Strategy name
│   │   ├── papers/                        # PDF files
│   │   └── metadata/                      # JSON metadata files
│   └── water_system_vulnerabilities/
├── post_quantum_cryptography/
│   ├── lattice_based_cryptography/
│   └── quantum_resistant_protocols/
└── general_research/                       # Default config
    ├── comprehensive_search/
    └── targeted_analysis/
```

**Folder Structure Rules**:
- Top level: Configuration file basename (without .yaml extension)
- Second level: Strategy names from configuration
- PDF files named: `{safe_title}_{source}_{unique_id}.pdf`
- Metadata files: `{pdf_filename}.json` with comprehensive source information

## DEVELOPMENT WORKFLOW - AUTONOMOUS IMPLEMENTATION

### Pre-Implementation Planning
1. **Sequential Thinking**: Break down requirements into logical steps
2. **Test Planning**: Design comprehensive test scenarios before coding
3. **Architecture Validation**: Ensure changes align with Clean Architecture
4. **Educational Value**: Plan documentation and comment strategy

### Implementation Process
1. **Write Tests First**: Comprehensive test coverage including edge cases
2. **Minimal Implementation**: Just enough code to pass tests
3. **Refactor for Quality**: Apply patterns, improve readability
4. **Educational Documentation**: Add comprehensive explanations
5. **Atomic Commit**: Single logical change with descriptive message

### Validation Requirements
- All tests must pass before committing
- Test coverage must remain above 90%
- Contract tests must validate interface compliance
- Performance benchmarks must be maintained
- Educational documentation must be comprehensive

### Error Handling Standards
**Domain-Specific Exceptions**:
```python
class PaperAggregationError(Exception):
    """Base exception for paper aggregation operations."""
    pass

class SourceUnavailableError(PaperAggregationError):
    """Raised when external paper source is unavailable."""
    pass

class DuplicatePaperError(PaperAggregationError):
    """Raised when attempting to download duplicate paper."""
    pass

class MetadataExtractionError(PaperAggregationError):
    """Raised when paper metadata cannot be extracted."""
    pass
```

### Performance Requirements
- Search operations: < 2 seconds for large repositories (1000+ papers)
- Bulk downloads: > 5 papers per second sustained throughput
- Memory usage: < 100MB increase for search operations
- Disk usage: Efficient storage with metadata compression

## CONTINUOUS LEARNING AND IMPROVEMENT

### Code Review Mindset
Every change should improve:
- **Code Quality**: Better design patterns, cleaner implementation
- **Educational Value**: More comprehensive explanations and examples
- **Test Coverage**: More comprehensive validation of behavior
- **User Experience**: Better interfaces for academic researchers

### Pattern Recognition and Application
Continuously identify opportunities to demonstrate:
- **SOLID Principles**: Through practical implementation examples
- **Design Patterns**: Applied to solve real academic research problems
- **Clean Architecture**: Maintaining proper separation of concerns
- **Domain-Driven Design**: Modeling academic concepts accurately

### Documentation Evolution
Keep documentation current and valuable:
- **Update Examples**: Ensure code examples reflect current implementation
- **Expand Explanations**: Add depth to pattern and principle explanations
- **Cross-Reference**: Link related concepts across different modules
- **Real-World Context**: Always explain academic research applicability

Remember: Every line of code should advance academic research capabilities while teaching professional software development practices. This dual purpose drives all architectural and implementation decisions.

Below is a **starter catalogue of open‑access publishers and large‑scale repositories that expose an OAI‑PMH endpoint** you can harvest exactly the way you plan to do with *Sensors*. All of them are free to query, well‑maintained, and publish substantial content in at least one of your focus areas (cyber‑security, applied mathematics, physics, computer science, K‑12 / higher‑education research, or operations research).

| #  | Provider (typical subjects)                                      | Base URL<sup>†</sup>                    | Notes that matter to harvesting                                                                            |
| -- | ---------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1  | **arXiv.org** – physics, maths, CS                               | `https://export.arxiv.org/oai2`         | Daily refresh ≈ 03:00 UTC; ‘set’ per archive (e.g. `physics:hep-th`). ([arXiv][1])                         |
| 2  | **MDPI** (all journals incl. *Sensors*)                          | `https://oai.mdpi.com/oai/oai2.php`     | One ‘set’ per journal (`journal:sensors`, `journal:mathematics`, …). ([MDPI][2])                           |
| 3  | **PubMed Central** – biomedical + medical‑AI security            | `https://pmc.ncbi.nlm.nih.gov/oai/oai2` | Full‑text XML available; incremental `from=` / `until=` dates. ([PMC][3])                                  |
| 4  | **Zenodo** – multidisciplinary (data + software + papers)        | `https://zenodo.org/oai2d`              | Excellent for conference proceedings and cyber‑security datasets. ([Zenodo Developers][4])                 |
| 5  | **Directory of Open Access Journals (DOAJ)** – aggregator        | `https://doaj.org/oai.article`          | Harvest whole OA corpus or restrict with discipline‑based *sets*. ([Directory of Open Access Journals][5]) |
| 6  | **RePEc** – economics & operations‑research working papers       | `https://oai.repec.org/`                | Gateway exposes >60 k OR articles; metadata only (PDF on publisher site). ([oai.repec.org][6])             |
| 7  | **Pensoft / ARPHA platform** – information science, biodiversity | `https://oai.pensoft.net/`              | Each journal is its own *set*; MODS or DC output. ([Pensoft][7])                                           |
| 8  | **Copernicus Publications** (e.g. *Earth System Science Data*)   | `https://oai.copernicus.org/oai`        | Offers article *full‑text XML* in addition to metadata. ([Earth System Science Data][8])                   |
| 9  | **Academic Journals** – education & CS journals                  | `https://academicjournals.org/oai-pmh`  | Simple Dublin‑Core only. ([Academic Journals][9])                                                          |
| 10 | **AKJournals** – applied maths, physics                          | `https://akjournals.com/oaipmh`         | Supports selective harvesting by journal code. ([Akademiai Kiadó][10])                                     |
| 11 | **IUCr Journals** – crystallography / solid‑state physics        | `https://journals.iucr.org/oai`         | Rich crystallographic metadata in MODS as well as DC. ([IUCr Journals][11])                                |
| 12 | **Global registry (2 000 + endpoints)**                          | *See* OpenArchives “Browse Sites”       | Machine‑readable XML list of every registered OAI data‑provider. ([Open Archives][12])                     |

<sup>†</sup>*All base URLs respond to the six OAI‑PMH verbs (`Identify`, `ListSets`, `ListRecords`, …). Paste `?verb=Identify` after any base URL to test it in a browser.*

---

### Why this matters for your topics

| Topic                            | Endpoints to prioritise                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Cyber‑security & CS**          | arXiv (cs.CR, cs.DS), Zenodo (community “cybersecurity”), MDPI (*Electronics*, *Algorithms*), DOAJ filters                   |
| **Applied mathematics / OR**     | arXiv (math.OC), RePEc (working‑paper series), AKJournals (*Acta Polytechnica*), MDPI (*Mathematics*)                        |
| **Physics**                      | arXiv, IUCr, Copernicus (*Ann. Geophys.*)                                                                                    |
| **K‑12 / Higher‑Ed research**    | Academic Journals, DOAJ sets “Education”, Zenodo communities, ERIC’s own endpoint (behind rate limit; not openly documented) |
| **Multi‑disciplinary catch‑all** | DOAJ, Zenodo                                                                                                                 |

---

### Minimal Python “endpoint lister” you can reuse

```python
from sickle import Sickle           # pip install sickle
BASES = {
    "arxiv":    "https://export.arxiv.org/oai2",
    "mdpi":     "https://oai.mdpi.com/oai/oai2.php",
    "zenodo":   "https://zenodo.org/oai2d",
    # add the others here …
}

for name, url in BASES.items():
    repo = Sickle(url)
    ident  = repo.Identify()
    print(f"{name:8} ▸ {ident.repositoryName}  –  earliest={ident.earliestDatestamp}")
    print("  sets →", [s.setSpec for s in repo.ListSets()][:5], "…\n")
```

*Swap `ListSets()` for a date‑limited `ListRecords(metadataPrefix="oai_dc", from_="2025-08-01")` to pull just the last few days of output.*

---

### Discovering still more feeds

* **Registry scrape** – download the `ListFriends` file from OpenArchives and filter for keywords (e.g. `'education'`, `'security'`).
* **DOAJ set explorer** – issue `ListSets` to DOAJ and pick subject sets like `3021:Computer_security`.
* **Institutional repositories** – any DSpace, EPrints or Fedora‑Commons instance is OAI‑enabled by default; most universities host one.
* **Commercial publishers** – IEEE, ACM, Elsevier, etc. do expose OAI‑PMH, but access is IP‑restricted to subscribing libraries and you will only get *metadata*, not PDFs.

---

### Next steps for an automated pipeline

1. **Maintain a YAML list** of `{name, base_url, set, discipline}` records.
2. Iterate through the list nightly with `sickle`, using `from_=yesterday` to pick up only new items.
3. Apply the same `interesting()` keyword filter you already wrote for *Sensors*.
4. Save each record’s XML plus the PDF URL (if available) in your Git‑tracked repository.
5. Commit & push; optionally trigger a GitHub Action that posts a Slack/Discord notification when new papers land.

With this catalogue you can start scaling today’s *Sensors* harvester into a **multi‑publisher literature bot** that covers all the disciplines you listed—without ever scraping HTML or fighting paywalls. Happy harvesting!

[1]: https://info.arxiv.org/help/oa/index.html?utm_source=chatgpt.com "Open Archives Initiative (OAI) - arXiv info"
[2]: https://www.mdpi.com/librarians?utm_source=chatgpt.com "Information for Librarians - MDPI"
[3]: https://pmc.ncbi.nlm.nih.gov/tools/oai/?utm_source=chatgpt.com "OAI-PMH Service - PMC - PubMed Central"
[4]: https://developers.zenodo.org/?utm_source=chatgpt.com "Developers | Zenodo"
[5]: https://doaj.org/docs/oai-pmh/?utm_source=chatgpt.com "OAI-PMH - DOAJ"
[6]: https://oai.repec.org/?utm_source=chatgpt.com "OAI-PMH gateway for RePEc"
[7]: https://pensoft.net/oai-pmh?utm_source=chatgpt.com "OAI-PMH - Pensoft Publishers"
[8]: https://www.earth-system-science-data.net/about/xml_harvesting_and_oai-pmh.html?utm_source=chatgpt.com "ESSD - XML harvesting & OAI-PMH - Earth System Science Data"
[9]: https://academicjournals.org/open_archives_initiative_oai_pmh?utm_source=chatgpt.com "Open Archives Initiative (OAI-PMH) - Academic Journals"
[10]: https://akjournals.com/oaipmh?utm_source=chatgpt.com "OAI-PMH Repository - AKJournals"
[11]: https://journals.iucr.org/services/OAI.html?utm_source=chatgpt.com "(IUCr) IUCr Journals OAI-PMH metadata access"
[12]: https://www.openarchives.org/Register/BrowseSites?utm_source=chatgpt.com "OAI-PMH Registered Data Providers - Open Archives Initiative"
