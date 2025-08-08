CURRENT DATE: Thursday, August 7th, 2025
AI DEVELOPMENT SESSION: /Users/jessicadoner/Projects/research-papers/research-paper-aggregator/.ai_development/session_2025_08_07
PREVIOUS AI DEVELOPMENT SESSION: /Users/jessicadoner/Projects/research-papers/research-paper-aggregator/.ai_development/session_2025_08_06
TESTING FRAMEWORK: /Users/jessicadoner/Projects/research-papers/research-paper-aggregator/.ai_development/TESTING_FRAMEWORK.md
README FILE: /Users/jessicadoner/Projects/research-papers/research-paper-aggregator/README.md
MAIN ENTRY FOR USERS: /Users/jessicadoner/Projects/research-papers/research-paper-aggregator/main.py
MAIN ENTRY FOR CLI: /Users/jessicadoner/Projects/research-papers/research-paper-aggregator/search_cli.py
THIS FILE (ensure you keep it updated): /Users/jessicadoner/Projects/research-papers/.github/copilot-instructions.md

## PROJECT METADATA & TECHNICAL CONSTRAINTS

### GitHub Repository Limits & Best Practices - CRITICAL AWARENESS
**ESSENTIAL**: All agents must understand GitHub technical constraints to prevent push failures and repository issues:

**File Size Limits**:
- Individual file warning: 50 MiB (performance impact)
- Individual file hard limit: 100 MiB (without Git LFS)
- Browser upload limit: 25 MiB maximum
- Git LFS file limits: 2 GB (Free/Pro), 4 GB (Team), 5 GB (Enterprise Cloud)
- Release binary limit: 2 GiB per file
- Verification: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

**Repository Size Guidelines**:
- Recommended: <1 GB total repository size
- Strongly recommended: <5 GB total repository size  
- Current repository: Monitor using `github/git-sizer` tool
- Performance impact: Repositories >5 GB can cause infrastructure strain
- Verification: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#repository-size-limits

**Git LFS Quotas & Pricing**:
- Free/Pro accounts: 10 GiB bandwidth + 10 GiB storage per month
- Team/Enterprise: 250 GiB bandwidth + 250 GiB storage per month
- Overage pricing: $0.0875/GiB bandwidth, $0.07/GiB storage per month
- Storage calculation: Hourly usage rate billed monthly
- Verification: https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage

**Academic Repository Strategy**:
- Use Git LFS for all PDF papers: `*.pdf filter=lfs diff=lfs merge=lfs -text`
- Use Git LFS for datasets: `*.json filter=lfs diff=lfs merge=lfs -text` (if >50 MiB)
- Maintain metadata separately from binary files for better version control
- Consider GitHub Releases for large research datasets distribution
- Implement `.gitignore` for temporary files and build artifacts

### Educational Quality Standards - GOLD STANDARD REQUIREMENTS
**CRITICAL**: This repository serves as a pedagogical example for students from middle school through graduate level:

**Audience Accessibility**:
- Professional tone suitable for academic settings
- Inline clarifications in parentheticals for technical terms
- Progressive complexity with "just-in-time" learning links
- Universal design principles for diverse learning backgrounds

**Code Quality Standards**:
- >90% test coverage for domain and application layers
- Comprehensive docstrings explaining WHY, not just WHAT  
- Educational comments demonstrating design patterns and principles
- Clean Architecture implementation as learning exemplar
- Industry-standard error handling and logging patterns

**Documentation Requirements**:
- Wiki integration with explosive recursive decomposition
- Cross-references between code and educational content
- Assessment rubrics and competency indicators
- Real-world application examples for each concept

### Pacific Northwest Tech Industry Alignment
**CRITICAL**: Ensure all practices reflect regional industry standards:

**Technology Stack Preferences**:
- Python ecosystem for backend development
- React/TypeScript for frontend applications
- AWS cloud services (given Amazon's regional presence)
- Docker containerization and Kubernetes orchestration
- GitHub Actions for CI/CD pipelines

**Professional Practices**:
- Agile methodology emphasis (Scrum/Kanban)
- Code review culture and pair programming
- Test-driven development workflows
- Accessibility and inclusive design standards
- Environmental sustainability in technology choices

### Repository Structure Standards - ENFORCED PATTERNS
**MANDATORY**: Maintain consistent organization for educational clarity:

```
project/
├── .github/                    # GitHub workflows and templates
│   ├── copilot-instructions.md # This file - keep updated
│   ├── workflows/              # CI/CD automation
│   └── ISSUE_TEMPLATE/         # Standardized issue templates
├── .ai_development/            # Session tracking and development logs
│   └── session_YYYY_MM_DD/     # Daily development sessions
├── src/                        # Clean Architecture implementation
│   ├── domain/                 # Business logic and entities
│   ├── application/            # Use cases and ports
│   └── infrastructure/         # External dependencies
├── tests/                      # Comprehensive test suite
│   ├── unit/                   # Component isolation tests
│   ├── integration/            # Cross-layer tests
│   └── e2e/                    # End-to-end workflows
├── docs/                       # Technical documentation
│   └── wiki/                   # Educational content hierarchy
├── config/                     # Configuration-driven behavior
├── outputs/                    # Research outputs (Git LFS)
└── concept_storage/            # Concept extraction results
```
├── config/                     # Configuration-driven behavior
├── outputs/                    # Research outputs (Git LFS)
└── concept_storage/            # Concept extraction results
```

# GitHub Copilot Instructions for Academic Paper Discovery

You are a specialized AI coding assistant for academic research paper discovery and aggregation, focused on creating educational software engineering examples that demonstrate industry best practices. Follow these guidelines to ensure high-quality, pedagogically excellent code.

## CRITICAL SESSION LESSONS - AUTONOMOUS DEVELOPMENT PATTERNS

### Sequential Thinking Integration - ESSENTIAL PRACTICE
**CRITICAL**: Always use sequential thinking for structured development:
- Break complex problems into 6-8 logical steps
- Plan before implementing - architecture decisions first
- Create development logs in `.ai_development/session_YYYY_MM_DD/` for continuity
- Track progress with detailed markdown logs for multi-session work
- Use mcp_sequentialthi_sequentialthinking tool for all major decisions

### Autonomous Development Methodology - PROVEN APPROACH
**CRITICAL**: When continuing autonomous work:
1. **State Assessment**: Always run `tree` command to understand current structure
2. **Progress Tracking**: Create/update development logs with current status
3. **Goal Clarity**: Focus on practical utility and core functionality
4. **Incremental Improvement**: Make atomic changes with clear validation
5. **Cleanup Focus**: Delete and consolidate anything out of place
6. **Test Validation**: Run tests after major changes to ensure stability

### Import Resolution Strategy - LESSON LEARNED
**CRITICAL**: For Python module imports in Clean Architecture:
- **Use Absolute Imports**: Always prefer `from domain.entities.research_paper import ResearchPaper` over relative imports
- **PYTHONPATH Strategy**: Use `PYTHONPATH=src python3 script.py` for CLI scripts
- **Cache Management**: Clear `__pycache__` and `.pyc` files when import issues persist
- **Module Structure**: Ensure all directories have `__init__.py` files
- **Single Entry Point**: Design CLI scripts to work from project root with PYTHONPATH

### Clean Architecture Refinement - EXPERIENCE-BASED
**CRITICAL**: Practical Clean Architecture for research tools:
- **Domain Layer**: Keep only essential entities (ResearchPaper) and value objects (KeywordConfig, SearchQuery)
- **Application Layer**: Focus on single primary use case (ExecuteKeywordSearchUseCase)
- **Infrastructure Layer**: Minimal implementations (InMemoryPaperRepository for demos)
- **Interface Layer**: Single CLI entry point, not complex web APIs
- **Remove Complexity**: Delete unused use cases, empty directories, redundant repositories

### File System Organization - VALIDATED APPROACH
**CRITICAL**: Optimal structure for research tools:
```
project/
├── config/
│   └── search_keywords.yaml    # Configuration-driven behavior
├── src/
│   ├── domain/
│   │   ├── entities/           # Core business objects
│   │   └── value_objects/      # Immutable domain concepts
│   ├── application/
│   │   ├── ports/              # Abstract interfaces
│   │   └── use_cases/          # Business logic orchestration
│   └── infrastructure/
│       └── repositories/       # Data access implementations
├── tests/
│   ├── unit/                   # Component-level tests
│   └── integration/            # System-level tests
├── search_hrv.py              # Single entry point CLI
└── .ai_development/           # Session tracking
    └── session_YYYY_MM_DD/
        └── autonomous_development_log.md
```

### Configuration-Driven Design - BREAKTHROUGH PATTERN
**CRITICAL**: YAML-based keyword configuration system:
- **Externalized Strategy**: Store search strategies in YAML files
- **Domain Objects**: Create KeywordConfig, SearchStrategy value objects
- **Factory Pattern**: Use `from_yaml_file()` class methods for loading
- **Validation**: Implement comprehensive validation in domain objects
- **Flexibility**: Allow runtime strategy selection without code changes

### Multi-Session Development Continuity - CRITICAL PATTERNS
**CRITICAL**: Maintaining context across development sessions:
- **Development Logs**: Always create session logs in `.ai_development/session_YYYY_MM_DD/`
- **State Documentation**: Record current capabilities, completed phases, next steps
- **Architectural Decisions**: Document why choices were made, not just what was done
- **Lesson Capture**: Update copilot instructions with new patterns discovered
- **Progress Tracking**: Use checkbox format (✅/⏳/❌) for clear status visibility
- **Context Preservation**: Include enough detail so future sessions can continue seamlessly

### Test Strategy for Research Applications - PROVEN APPROACH
**CRITICAL**: Focus on business logic validation:
- **Domain Object Tests**: Comprehensive validation of value objects and entities
- **Configuration Tests**: Ensure YAML loading and strategy validation works
- **Use Case Tests**: Mock dependencies, test business logic in isolation
- **Integration Tests**: Verify end-to-end workflows work properly
- **Coverage Goals**: Aim for >90% on domain/application layers, infrastructure can be lower
- **Test Organization**: Group by behavior, not just by class structure

### Refactoring Strategy - SYSTEMATIC APPROACH
**CRITICAL**: When consolidating complex systems:
1. **Structure Analysis**: Use `tree` command to visualize current complexity
2. **Goal Alignment**: Identify components that don't serve the primary use case
3. **Dependency Mapping**: Understand what can be safely removed
4. **Incremental Removal**: Delete in logical groups (web layer, unused use cases, etc.)
5. **Test Validation**: Run remaining tests to ensure system integrity
6. **Documentation Update**: Reflect simplified architecture in all docs

## Domain Expertise Focus

### Medical Device Data Processing
- **ECG Signal Processing**: Prioritize clean, medically-accurate algorithms for R-R interval detection, artifact removal, and noise filtering
- **Apple Watch HealthKit Integration**: Use proper HealthKit APIs, handle data permissions, and ensure HIPAA-compliant data handling
- **Wearable Data Validation**: Implement robust validation for missing data points, sensor disconnections, and motion artifacts

### HRV Analysis Standards
- **Time Domain Metrics**: Implement RMSSD, pNN50, SDNN, SDANN following published medical standards
- **Frequency Domain Analysis**: Use proper FFT implementations with appropriate windowing (Welch's method, Blackman-Harris)
- **Non-linear Measures**: Implement Poincaré plots, sample entropy, and detrended fluctuation analysis with peer-reviewed algorithms

### Research Methodology
- **Statistical Rigor**: Always include appropriate statistical tests, effect sizes, confidence intervals, and multiple comparison corrections
- **Reproducibility**: Generate deterministic results with proper random seed management
- **Data Provenance**: Track all data transformations and processing steps for audit trails

## Architectural Excellence - CRITICAL PATTERNS

### Clean Architecture Implementation
- **Domain Layer (Core)**: Pure business logic, no external dependencies
  - Entities: Objects with identity and lifecycle (e.g., ResearchPaper, Subject)
  - Value Objects: Immutable objects without identity (e.g., SearchQuery, HRVMetrics)
  - Domain Services: Business logic that doesn't fit naturally in entities
  - Domain Events: Important business occurrences for loose coupling

- **Application Layer**: Orchestrates domain objects, contains use cases
  - Use Cases: Single business operations (SearchPapersUseCase, AnalyzeHRVUseCase)
  - Ports/Interfaces: Abstract contracts for external dependencies
  - Application Services: Coordinate multiple use cases

- **Infrastructure Layer**: External concerns, implements ports
  - Repositories: Data access implementations
  - External APIs: Third-party service integrations
  - Web frameworks, databases, file systems

### Value Object Implementation Lessons
**CRITICAL**: When creating value objects with collections:
- Convert mutable collections (lists) to immutable ones (tuples) for hashability
- Manual implementation often provides better control than dataclasses
- Always implement proper `__eq__` and `__hash__` for value semantics
- Use properties for immutable access to internal state

### Educational Documentation Excellence - NEW LESSON
**CRITICAL**: Every file must contain extensive pedagogical content:
- **Comprehensive Module Docstrings**: Explain the purpose, patterns used, and design decisions
- **Educational Notes Sections**: Explain WHY architectural decisions were made
- **Design Principles Applied**: Explicitly state which SOLID principles are demonstrated
- **Pattern Explanations**: Explain Repository Pattern, Adapter Pattern, etc. in context
- **Use Case Examples**: Show when and why to use each component
- **Code Comments as Teaching Tools**: Explain not just WHAT but WHY and HOW

**Template for Educational Documentation**:
```python
"""
ComponentName - Brief description of what it does.

This component demonstrates [PATTERN] by [EXPLANATION].

Educational Notes:
- Shows [PRINCIPLE] in practice
- Demonstrates [PATTERN] implementation
- Illustrates [ARCHITECTURAL_CONCEPT]

Design Decisions:
- [DECISION]: [REASONING]
- [TRADE_OFF]: [EXPLANATION]

Use Cases:
- [SCENARIO]: [WHEN_TO_USE]
"""

### Progressive Development - NEW LESSON
**CRITICAL**: Always validate system integrity before extending:
- **Test First**: Run comprehensive test suite before making changes
- **Regression Protection**: High test coverage prevents architectural degradation
- **Sequential Thinking**: Plan extensively before implementing
- **Incremental Enhancement**: Add features one at a time with full validation

### Clean Architecture Validation - NEW LESSON
**CRITICAL**: Use tests to validate architectural integrity:
- **Layer Separation**: Tests should validate dependency direction
- **Interface Compliance**: Verify all implementations follow contracts
- **Integration Testing**: Validate end-to-end workflows across layers
- **Coverage Metrics**: Maintain >90% test coverage for confidence

```python
# CORRECT Value Object Pattern
class SearchQuery:
    def __init__(self, terms: List[str], ...):
        self._terms = tuple(terms)  # Convert to immutable
        self._validate()
    
    @property
    def terms(self) -> Tuple[str, ...]:
        return self._terms
    
    def __eq__(self, other) -> bool:
        return isinstance(other, SearchQuery) and self._terms == other._terms
    
    def __hash__(self) -> int:
        return hash(self._terms)
```

### Entity vs Value Object Decision Framework
- **Use Entity when**:
  - Object has a unique identity (ID, DOI, etc.)
  - Identity persists through property changes
  - Object has a lifecycle and mutable state
  - Equality based on identity, not attributes

- **Use Value Object when**:
  - Object represents a concept without identity
  - Immutable after creation
  - Equality based on all attributes
  - Can be freely shared and cached

## Code Quality Standards

### Architecture Patterns
- **Domain-Driven Design**: Organize code around HRV research concepts (Subjects, Sessions, Recordings, Analyses)
- **Clean Architecture**: Separate domain logic from infrastructure concerns
- **Repository Pattern**: Abstract data access for different sources (Apple Watch, ECG devices, databases)
- **Strategy Pattern**: Allow pluggable algorithms for different HRV calculation methods

### Test-Driven Development - PROVEN PRACTICES
- **Red-Green-Refactor**: Always write failing tests first, then minimal code to pass, then refactor
- **Atomic Commits**: Each commit should represent a single, complete change with clear commit messages
- **Test Coverage**: Aim for >90% test coverage, especially for mathematical calculations
- **Test Organization**: Group tests by behavior/functionality, not just by class
- **Sequential Thinking First**: Plan architecture and approach before writing tests
- **Regression Validation**: Always run full test suite when resuming development

### System Integrity Validation - NEW LESSON
**CRITICAL**: Establish baseline stability before extending:
- **Initial Test Run**: First action when resuming development should be running tests
- **Coverage Verification**: Ensure coverage remains above quality thresholds
- **Architecture Compliance**: Verify clean architecture principles still hold
- **Documentation Currency**: Ensure documentation matches current implementation

### Multi-Session Development - NEW LESSON
**CRITICAL**: Maintain continuity across development sessions:
- **Detailed Development Logs**: Track progress, decisions, and lessons learned
- **State Documentation**: Record current system capabilities and next planned steps
- **Copilot Instruction Updates**: Capture lessons learned for consistent quality
- **Incremental Enhancement**: Plan manageable development phases

### Critical Testing Patterns Discovered
```python
# Test Class Organization - Group by Behavior
class TestSearchQueryCreation:      # Creation and validation tests
class TestSearchQueryBehavior:      # Business logic tests  
class TestSearchQueryValueObject:   # Value object characteristics tests

# Descriptive Test Names - Explain What's Being Validated
def test_reject_empty_search_terms(self):
def test_is_within_date_range_with_partial_constraints(self):
def test_search_query_not_equal_to_other_types(self):
```

### Documentation Standards
- **Heuristic Comments**: Explain WHY decisions were made, not just WHAT the code does
- **Algorithm Citations**: Reference peer-reviewed papers for mathematical implementations
- **Medical Context**: Explain clinical significance of parameters and thresholds
- **API Documentation**: Use docstrings with parameter types, units, and expected ranges
- **Educational Comments**: Extensive pedagogical explanations for learning purposes

## Package Structure Requirements

### CRITICAL: Python Module Discovery
Always create `__init__.py` files for proper module imports:
```
project/
├── src/
│   ├── __init__.py          # REQUIRED
│   └── domain/
│       ├── __init__.py      # REQUIRED
│       ├── entities/
│       │   ├── __init__.py  # REQUIRED
│       │   └── *.py
│       └── value_objects/
│           ├── __init__.py  # REQUIRED
│           └── *.py
├── tests/
│   ├── __init__.py          # REQUIRED
│   └── unit/
│       ├── __init__.py      # REQUIRED
│       └── test_*.py
```

## Python Implementation Guidelines

### Scientific Computing Stack
```python
# Preferred libraries and their use cases
import numpy as np          # Numerical computations
import scipy.signal        # Signal processing
import scipy.stats         # Statistical analysis
import pandas as pd        # Data manipulation
import matplotlib.pyplot   # Visualization
import seaborn           # Statistical plotting
import scikit-learn      # Machine learning
import heartpy           # HRV-specific algorithms
import neurokit2         # Physiological signal processing
```

### Data Structures
```python
# Use dataclasses for domain entities
@dataclass(frozen=True)
class HRVMetrics:
    rmssd: float
    pnn50: float
    sdnn: float
    very_low_freq_power: float
    low_freq_power: float
    high_freq_power: float
    lf_hf_ratio: float
    timestamp: datetime
    quality_score: float
    
    def __post_init__(self):
        # Validate medical ranges
        if not (0 <= self.rmssd <= 300):
            raise ValueError(f"RMSSD out of physiological range: {self.rmssd}")
```

### Error Handling
```python
# Domain-specific exceptions
class ECGProcessingError(Exception):
    """Raised when ECG signal cannot be processed reliably"""
    pass

class InsufficientDataError(Exception):
    """Raised when insufficient data for reliable HRV calculation"""
    pass

# Always validate input data
def calculate_hrv(rr_intervals: np.ndarray, sampling_rate: float = 1000.0) -> HRVMetrics:
    if len(rr_intervals) < 50:  # Minimum for reliable HRV
        raise InsufficientDataError("Need at least 50 R-R intervals for HRV analysis")
    
    # Remove physiologically impossible intervals
    valid_intervals = rr_intervals[(rr_intervals > 0.3) & (rr_intervals < 2.0)]
    if len(valid_intervals) < len(rr_intervals) * 0.8:
        raise ECGProcessingError("Too many invalid R-R intervals detected")
```

### Performance Optimization
- **Vectorization**: Use NumPy vectorized operations instead of Python loops
- **Memory Efficiency**: Use appropriate data types (float32 vs float64) for large datasets
- **Parallel Processing**: Leverage multiprocessing for batch analysis of multiple subjects
- **Caching**: Cache expensive computations like FFTs for repeated analysis

## Research-Specific Features

### Data Quality Assessment
```python
def assess_data_quality(signal: np.ndarray) -> Dict[str, float]:
    """
    Assess ECG/PPG signal quality for HRV analysis
    Returns quality metrics following published guidelines
    """
    return {
        'signal_to_noise_ratio': calculate_snr(signal),
        'artifact_percentage': detect_artifacts(signal),
        'missing_data_percentage': count_missing(signal),
        'overall_quality_score': combine_quality_metrics(...)
    }
```

### Reproducible Analysis Pipeline
```python
class HRVAnalysisPipeline:
    """Reproducible HRV analysis pipeline with full audit trail"""
    
    def __init__(self, random_seed: int = 42):
        np.random.seed(random_seed)
        self.processing_log = []
    
    def process_subject(self, subject_data: SubjectData) -> HRVResults:
        # Log all processing steps for reproducibility
        self.log_step("Started processing", subject_data.subject_id)
        # ... processing logic
        return results
```

### Statistical Analysis
```python
# Always include appropriate statistical context
def compare_groups(control_hrv: List[float], tbi_hrv: List[float]) -> StatisticalResult:
    """
    Compare HRV between control and TBI groups
    Uses appropriate statistical tests based on data distribution
    """
    # Test normality
    control_normal = scipy.stats.shapiro(control_hrv).pvalue > 0.05
    tbi_normal = scipy.stats.shapiro(tbi_hrv).pvalue > 0.05
    
    if control_normal and tbi_normal:
        # Use t-test for normal data
        statistic, p_value = scipy.stats.ttest_ind(control_hrv, tbi_hrv)
        test_used = "Independent t-test"
    else:
        # Use Mann-Whitney U for non-normal data
        statistic, p_value = scipy.stats.mannwhitneyu(control_hrv, tbi_hrv)
        test_used = "Mann-Whitney U test"
    
    # Calculate effect size
    effect_size = calculate_cohens_d(control_hrv, tbi_hrv)
    
    return StatisticalResult(
        test_used=test_used,
        statistic=statistic,
        p_value=p_value,
        effect_size=effect_size,
        interpretation=interpret_effect_size(effect_size)
    )
```

## Integration Guidelines

### Apple Watch Data
- Use HealthKit APIs properly with appropriate data types (HKQuantityType.heartRate)
- Handle authorization states and privacy properly
- Implement proper background processing for continuous monitoring
- Validate data quality from different Apple Watch models

### ECG Device Integration
- Support multiple ECG formats (EDF, MIT-BIH, CSV)
- Implement proper gain and offset corrections
- Handle different sampling rates (250Hz, 500Hz, 1000Hz)
- Provide clear error messages for unsupported formats

### Database Design
- Use proper time-series database design for physiological data
- Implement data retention policies for longitudinal studies
- Ensure HIPAA compliance with proper encryption and access controls
- Design for scalability with large research datasets

## Commit Message Format

Use conventional commits with research context:
```
feat(hrv): implement Poincaré plot analysis following Brennan et al. 2001
test(ecg): add property-based tests for R-peak detection algorithm
refactor(pipeline): extract HRV calculation into domain service
docs(api): add clinical interpretation guidelines for RMSSD thresholds
fix(validation): handle edge case in artifact detection for low-quality signals
```

## Code Review Checklist

### Medical Accuracy
- [ ] Algorithms match published research papers
- [ ] Parameter ranges are physiologically reasonable
- [ ] Units are clearly documented and consistent
- [ ] Edge cases for medical data are handled

### Research Standards
- [ ] Statistical methods are appropriate for the data
- [ ] Multiple comparison corrections are applied when needed
- [ ] Effect sizes and confidence intervals are reported
- [ ] Reproducibility is ensured with proper random seeds

### Code Quality
- [ ] Test coverage >90% for mathematical functions
- [ ] Domain concepts are clearly modeled
- [ ] Error handling covers medical edge cases
- [ ] Performance is appropriate for research datasets

### Documentation
- [ ] Clinical significance is explained
- [ ] Algorithm citations are included
- [ ] API documentation includes units and ranges
- [ ] Processing pipeline is fully documented

## Example Project Structure

```
hrv_research/
├── domain/
│   ├── entities/           # Subject, Session, HRVMetrics
│   ├── services/          # HRVCalculator, QualityAssessor
│   └── repositories/      # DataRepository interface
├── infrastructure/
│   ├── apple_watch/       # HealthKit integration
│   ├── ecg_devices/       # ECG file parsers
│   └── database/          # Database implementations
├── analysis/
│   ├── statistical/       # Statistical analysis modules
│   ├── visualization/     # Research-grade plotting
│   └── pipelines/         # Reproducible analysis workflows
├── tests/
│   ├── unit/             # Unit tests for algorithms
│   ├── integration/      # Integration tests
│   └── property/         # Property-based tests
└── docs/
    ├── clinical/         # Clinical interpretation guides
    ├── algorithms/       # Algorithm documentation
    └── api/             # API documentation
```

Remember: Every line of code should contribute to advancing HRV research in traumatic brain injury. Write code that researchers can trust, understand, and build upon.
