# Contributing to Academic Paper Discovery Platform

Thank you for your interest in contributing to the Academic Paper Discovery Platform! This project serves both as a functional research tool and educational demonstration of Clean Architecture principles, so contributions should maintain high code quality and clear pedagogical value.

## 🚀 Quick Start for Contributors

### Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/jdoner02/academic-paper-discovery.git
cd academic-paper-discovery

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
- **Pure business logic** - no external dependencies
- **Research domain concepts** modeled as entities and value objects
- **Comprehensive test coverage** with fast unit tests
- **Educational documentation** explaining design decisions

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

# Contributing to Academic Paper Discovery Platform

Thank you for your interest in contributing to the Academic Paper Discovery Platform! This project serves as both a functional research tool and educational demonstration of Clean Architecture principles in software engineering.

## 🎯 Project Mission

This repository demonstrates professional software engineering practices through a real-world academic research application. We welcome contributions that enhance either the research capabilities or the educational value of the codebase.

## 🚀 Quick Start for Contributors

### Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/yourusername/academic-paper-discovery.git
cd academic-paper-discovery

# 3. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Set up Node.js dependencies (for web interface)
npm install

# 5. Run tests to ensure everything works
pytest --cov=src
npm test
```

### Making Changes

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes following our guidelines (see below)

# 3. Run quality checks
python -m pytest --cov=src
python -m mypy src
python -m black src tests
npm test

# 4. Commit with descriptive message
git commit -m "feat: add semantic search capability to concept graph"

# 5. Push and create Pull Request
git push origin feature/your-feature-name
```

## 🏗️ Architecture Guidelines

This project follows **Clean Architecture** principles for educational purposes. Please respect these layer boundaries:

### Domain Layer (`src/domain/`)
- **Pure business logic** - no external dependencies
- **Research domain concepts** modeled as entities and value objects
- **High test coverage** with fast unit tests
- **Educational documentation** explaining design decisions

```python
# ✅ Good: Domain entity with clear business purpose
class ResearchPaper:
    def __init__(self, title: str, authors: List[str], doi: str):
        self.title = title
        self.authors = tuple(authors)  # Immutable
        self.doi = doi
        self._validate()
    
    def is_relevant_to_query(self, search_query: SearchQuery) -> bool:
        """Domain logic for relevance determination."""
        return search_query.matches_paper_content(self.title, self.abstract)
```

### Application Layer (`src/application/`)
- **Use cases** that orchestrate domain objects
- **Abstract interfaces** for external dependencies  
- **Application services** that coordinate multiple use cases

```python
# ✅ Good: Use case orchestrates domain and infrastructure
class SearchPapersUseCase:
    def __init__(self, paper_repository: PaperRepository):
        self._repository = paper_repository
    
    def execute(self, search_query: SearchQuery) -> SearchResults:
        papers = self._repository.find_by_keywords(search_query)
        return SearchResults.from_papers(papers)
```

### Infrastructure Layer (`src/infrastructure/`)
- **External service implementations** (ArXiv API, PMC, etc.)
- **Database/file system access**
- **Web frameworks and UI components**

## 📚 Educational Contribution Guidelines

Since this project serves educational purposes, contributions should:

### 1. Include Learning Context
```python
def breadth_first_search(self, start: str, target: str) -> List[str]:
    """
    Find shortest path using BFS algorithm.
    
    Educational Notes:
    - Demonstrates BFS for unweighted graphs
    - Time complexity: O(V + E)
    - Space complexity: O(V) for queue and visited set
    
    Real-world Applications:
    - Social network friend suggestions
    - Research concept relationship discovery
    - Academic paper citation analysis
    """
```

### 2. Demonstrate Design Patterns
When implementing features, explicitly document which patterns you're using:
- Repository Pattern for data access
- Strategy Pattern for different search algorithms
- Observer Pattern for real-time updates
- Factory Pattern for configuration loading

### 3. Maintain Test Coverage
- Unit tests for domain logic (>90% coverage goal)
- Integration tests for use cases
- End-to-end tests for user workflows
- Performance tests for search algorithms

## 🔬 Research Domain Contributions

We welcome contributions that enhance the academic research capabilities:

### New Research Databases
- Support for additional academic databases (IEEE, ACM, etc.)
- Enhanced metadata extraction
- Citation network analysis

### Concept Extraction Improvements
- Better natural language processing
- Domain-specific concept recognition
- Semantic relationship mapping

### Visualization Enhancements
- Interactive graph exploration features
- Research domain clustering
- Timeline visualization of research trends

## 🎨 Web Interface Contributions

The interactive concept graph is built with:
- Next.js 14 with TypeScript
- D3.js v7 for visualization
- Responsive design for academic users

### UI/UX Guidelines
- Clean, academic presentation
- Accessibility compliance
- Mobile-responsive design
- Professional color scheme
- Clear typography for readability

## 📋 Pull Request Guidelines

### PR Description Template
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Educational improvement
- [ ] Documentation update
- [ ] Performance improvement

## Educational Value
How does this change improve the learning experience?

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Architecture Compliance
- [ ] Follows Clean Architecture principles
- [ ] Respects layer boundaries
- [ ] Includes appropriate documentation
```

### Code Review Focus Areas
1. **Architectural Integrity**: Does the change respect Clean Architecture?
2. **Educational Value**: Will students learn from this code?
3. **Test Coverage**: Are there appropriate tests?
4. **Documentation**: Is the purpose and design clear?
5. **Academic Appropriateness**: Suitable for academic environment?

## 🚫 What We Don't Accept

- Code without educational documentation
- Violations of Clean Architecture principles
- Changes that break existing tests
- Non-academic or commercial focused features
- Generated code without human review and documentation

## 🤝 Community Guidelines

- Be respectful and professional
- Focus on educational value
- Explain your reasoning in discussions
- Help others learn through code reviews
- Maintain academic standards

## 📞 Getting Help

- Create an issue for questions
- Use discussions for architectural decisions
- Tag `@maintainers` for urgent reviews
- Check existing issues before creating new ones

---

Thank you for helping make this project a valuable educational resource for software engineering and academic research!

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

### Academic Research Tools
- [ArXiv API Documentation](https://arxiv.org/help/api)
- [PMC API Documentation](https://www.ncbi.nlm.nih.gov/pmc/tools/developers/)

## 🤝 Community

- 💬 **Discussions**: [GitHub Discussions](https://github.com/jdoner02/academic-paper-discovery/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/jdoner02/academic-paper-discovery/issues)
- 📧 **Contact**: Open an issue for questions

## 🎉 Recognition

All contributors will be:
- Listed in the project README
- Mentioned in release notes for their contributions
- Given appropriate attribution in code comments

Thank you for helping advance research through better tooling! 🫀📚
