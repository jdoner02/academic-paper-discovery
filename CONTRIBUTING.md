# Contributing to HRV Research Aggregator

Thank you for your interest in contributing to HRV Research Aggregator! This project serves both production research needs and educational purposes, so contributions should maintain high code quality and clear educational value.

## 🚀 Quick Start for Contributors

### Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/yourusername/hrv-research-aggregator.git
cd hrv-research-aggregator

# 3. Set up development environment
pip install -e ".[dev]"

# 4. Set up pre-commit hooks (recommended)
pip install pre-commit
pre-commit install

# 5. Run tests to ensure everything works
pytest --cov=src --cov-report=html
```

### Making Changes

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes following our guidelines (see below)

# 3. Run quality checks
black src tests
isort src tests
mypy src
flake8 src tests
pytest --cov=src

# 4. Commit with conventional format
git commit -m "feat: add amazing new feature"

# 5. Push and create Pull Request
git push origin feature/your-feature-name
```

## 🏗️ Architecture Guidelines

This project follows **Clean Architecture** principles. Please respect these boundaries:

### Domain Layer (`src/domain/`)
- **Pure business logic only** - no external dependencies
- **Rich domain models** with behavior, not anemic data containers
- **Ubiquitous language** from HRV research domain
- **High test coverage** (>95%) with fast unit tests

```python
# ✅ Good: Rich domain object with behavior
class SearchQuery:
    def __init__(self, terms: List[str], date_range: Optional[DateRange] = None):
        self._terms = tuple(terms)  # Immutable
        self._date_range = date_range
        self._validate()
    
    def is_within_date_range(self, paper_date: datetime) -> bool:
        """Business logic for date filtering."""
        # Implementation here...

# ❌ Avoid: Anemic data container
class SearchQuery:
    def __init__(self, terms: List[str]):
        self.terms = terms  # Mutable, no behavior
```

### Application Layer (`src/application/`)
- **Orchestrate domain objects** - don't contain business logic
- **Abstract interfaces (ports)** for external dependencies
- **Use case implementations** that coordinate domain and infrastructure

```python
# ✅ Good: Use case orchestrates domain objects
class ExecuteKeywordSearchUseCase:
    def __init__(self, repository: PaperRepository):
        self._repository = repository  # Depends on abstraction
    
    def execute(self, search_query: SearchQuery) -> SearchResults:
        # Orchestrate domain objects and repository
        papers = self._repository.find_by_keywords(search_query)
        return SearchResults.from_papers(papers)

# ❌ Avoid: Business logic in application layer
class ExecuteKeywordSearchUseCase:
    def execute(self, search_query: SearchQuery) -> SearchResults:
        # Don't put domain logic here
        if len(search_query.terms) < 2:
            raise ValueError("Need at least 2 terms")  # Domain logic!
```

### Infrastructure Layer (`src/infrastructure/`)
- **Implement ports** defined in application layer
- **Handle external concerns** (APIs, files, databases)
- **No business logic** - pure technical implementation

## 📝 Code Style Guidelines

### General Python Style

We use automated tools to maintain consistency:

```bash
# Format code (run before committing)
black src tests
isort src tests

# Type checking (required)
mypy src

# Linting (fix issues before committing)
flake8 src tests
```

### Documentation Standards

Every module should include comprehensive educational documentation:

```python
"""
ArxivPaperRepository - Concrete implementation of PaperRepository for arXiv.org.

This component demonstrates the Adapter Pattern by implementing the abstract 
PaperRepository port defined in the application layer. It handles the technical 
details of communicating with arXiv's RSS API while exposing a clean domain interface.

Educational Notes:
- Shows Dependency Inversion Principle: high-level modules depend on abstractions
- Demonstrates Repository Pattern: encapsulates data access logic
- Illustrates Clean Architecture: infrastructure implements application ports

Design Decisions:
- RSS API over REST API: Better for bulk paper discovery
- Feedparser library: Mature, handles XML parsing edge cases reliably
- OR query strategy: Maximizes paper discovery for research applications

Use Cases:
- Research discovery: Find papers across multiple keyword combinations
- Automated monitoring: Scheduled searches for new publications
- Bulk analysis: Download papers for meta-analysis research
"""

class ArxivPaperRepository:
    """Concrete repository for accessing arXiv.org papers via RSS API."""
    
    def find_by_keywords(self, query: SearchQuery) -> List[ResearchPaper]:
        """
        Search arXiv for papers matching the query keywords.
        
        Args:
            query: SearchQuery value object containing search terms and filters
            
        Returns:
            List of ResearchPaper entities with arXiv metadata
            
        Raises:
            RepositoryError: If arXiv API is unavailable or returns invalid data
            
        Educational Note:
            This method demonstrates how infrastructure adapters translate
            between external APIs and domain objects, maintaining clean boundaries.
        """
        # Implementation...
```

### Test Standards

We follow Test-Driven Development (TDD) principles:

#### 1. Test Organization by Behavior
```python
# ✅ Good: Organize by behavior, not just class structure
class TestSearchQueryCreation:
    """Test search query creation and validation."""
    
    def test_create_query_with_valid_terms(self):
        """Should create query when given valid search terms."""
    
    def test_reject_empty_search_terms(self):
        """Should raise ValueError when given empty terms."""

class TestSearchQueryBehavior:
    """Test search query business logic."""
    
    def test_is_within_date_range_with_constraints(self):
        """Should correctly filter papers by date when date range specified."""

# ❌ Avoid: Generic test classes without behavioral focus
class TestSearchQuery:
    def test_method_1(self):  # What behavior is this testing?
        pass
```

#### 2. Descriptive Test Names
```python
# ✅ Good: Test name explains the behavior being validated
def test_arxiv_repository_handles_network_timeout_gracefully(self):
    """Should return empty results when arXiv API times out."""

def test_search_query_filters_papers_by_date_range_when_specified(self):
    """Should exclude papers outside date range when range is specified."""

# ❌ Avoid: Generic or unclear test names  
def test_repository_error(self):  # What error? What should happen?
def test_search_works(self):      # What does "works" mean specifically?
```

#### 3. High Coverage Requirements
- **Domain layer**: 95%+ coverage (business logic must be tested)
- **Application layer**: 90%+ coverage (use cases are critical)
- **Infrastructure layer**: 70%+ coverage (external dependencies may be mocked)

```bash
# Check coverage before submitting PR
pytest --cov=src --cov-report=term --cov-fail-under=90
```

## 🎯 Types of Contributions

### 🐛 Bug Reports
- Use GitHub Issues with the "bug" label
- Include steps to reproduce, expected behavior, actual behavior
- Provide system information (Python version, OS, dependencies)

### ✨ Feature Requests  
- Use GitHub Discussions for feature ideas first
- Once refined, create GitHub Issues with "enhancement" label
- Explain the research use case and expected impact

### 📖 Documentation Improvements
- README updates for clarity or missing information
- Code documentation for better educational value
- Tutorial or guide contributions

### 🔧 Code Contributions

#### New Paper Sources
To add support for a new academic database:

1. **Create repository implementation** in `src/infrastructure/repositories/`
2. **Follow the PaperRepository interface** defined in `src/application/ports/`
3. **Add comprehensive tests** for the new repository
4. **Update configuration** to support the new source
5. **Add documentation** explaining the new source's capabilities

Example:
```python
# src/infrastructure/repositories/pubmed_paper_repository.py
class PubmedPaperRepository(PaperRepository):
    """Repository implementation for PubMed papers."""
    
    def find_by_keywords(self, query: SearchQuery) -> List[ResearchPaper]:
        # Implementation using PubMed API
```

#### New Search Features
To enhance search capabilities:

1. **Start with domain objects** - what new value objects or entities are needed?
2. **Update use cases** - how does this change the application flow?
3. **Implement infrastructure** - what external services or APIs are required?
4. **Write tests first** - TDD approach ensures good design

## 🚨 Pull Request Guidelines

### Before Submitting
- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black src tests && isort src tests`
- [ ] Type checking passes: `mypy src`
- [ ] Linting passes: `flake8 src tests`
- [ ] Test coverage meets requirements: `pytest --cov=src --cov-fail-under=90`
- [ ] Documentation updated for any new features
- [ ] CHANGELOG.md updated (if applicable)

### Pull Request Description
Include:
- **Summary**: What does this PR accomplish?
- **Motivation**: Why is this change needed?
- **Testing**: How was this tested?
- **Breaking Changes**: Any API changes or migration requirements?
- **Screenshots**: For UI changes (if any)

### Review Process
1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by at least one maintainer
3. **Architecture review** for significant changes
4. **Educational review** - does this maintain/improve learning value?

## 🎓 Educational Contributions

Since this project serves educational purposes, consider:

### Adding Educational Examples
- **Code comments** explaining architectural decisions
- **Test examples** demonstrating TDD practices
- **Documentation** showing Clean Architecture benefits
- **Tutorials** for specific use cases

### Pattern Demonstrations
- **New design patterns** relevant to research applications
- **Refactoring examples** showing architecture improvements
- **Anti-pattern warnings** showing what to avoid

## 📚 Resources for Contributors

### Clean Architecture
- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert Martin
- [Clean Architecture in Python](https://github.com/Enforcer/clean-architecture-example)

### Domain-Driven Design
- [Domain-Driven Design](https://domainlanguage.com/ddd/) by Eric Evans
- [Python DDD Examples](https://github.com/jordifierro/python-ddd-example)

### HRV Research Domain
- [Heart Rate Variability Standards](https://www.ahajournals.org/doi/full/10.1161/01.CIR.93.5.1043)
- [HRV Analysis Methods](https://physionet.org/content/hrv-analysis/)

## 🤝 Community

- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/hrv-research-aggregator/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/hrv-research-aggregator/issues)
- 📧 **Email**: research@yourdomain.com

## 🎉 Recognition

All contributors will be:
- Listed in the project README
- Mentioned in release notes for their contributions
- Given appropriate attribution in code comments

Thank you for helping advance HRV research through better tooling! 🫀📚
