# HRV Research Aggregator

A clean architecture system for aggregating Heart Rate Variability (HRV) research papers from multiple academic sources. This project demonstrates Domain-Driven Design (DDD), Clean Architecture (Hexagonal Architecture), and Test-Driven Development (TDD) principles in Python.

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles with clear separation of concerns:

### Domain Layer (Inner Circle)
- **Entities**: Core business objects with identity (`ResearchPaper`, `Author`)
- **Value Objects**: Immutable objects without identity (`SearchQuery`, `QualityScore`)
- **Domain Services**: Business logic that doesn't naturally fit in entities
- **Domain Events**: Notifications of important domain occurrences

### Application Layer (Use Cases)
- **Ports**: Abstract interfaces defining what the application needs
- **Use Cases**: Application-specific business rules and orchestration
- **Application Services**: Coordinate between domain and infrastructure

### Infrastructure Layer (Outer Circle)
- **Adapters**: Concrete implementations of ports
- **External Services**: API clients, databases, file systems
- **Configuration**: Settings and dependency injection

## 🎯 Educational Goals

This project serves as a comprehensive example for students learning:

- **Clean Architecture**: How to structure applications for maintainability
- **Domain-Driven Design**: Expressing business logic in code
- **SOLID Principles**: Writing maintainable, extensible code
- **Test-Driven Development**: Building quality through testing
- **Python Best Practices**: Type hints, dataclasses, async programming

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip or poetry for dependency management

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd hrv-research-aggregator

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Quick Start

The system includes a command-line interface for immediate use:

```bash
# List available search strategies
python3 search_hrv.py --list-strategies

# Search using a predefined strategy with sample data
python3 search_hrv.py --source sample --strategy broad_hrv_research --limit 5

# Search real arXiv papers
python3 search_hrv.py --source arxiv --strategy tbi_focused --limit 10

# Custom search with keywords
python3 search_hrv.py --custom "heart rate variability" "Apple Watch" --limit 5

# Download papers (arXiv source only)
python3 search_hrv.py --source arxiv --custom HRV ECG --download --limit 3
```

### Configuration

Search strategies are defined in `config/search_keywords.yaml` and can be customized for your research needs.

### Development Setup

```bash
# Install pre-commit hooks (optional)
pre-commit install

# Format code
black src tests
isort src tests

# Type checking
mypy src

# Linting
flake8 src tests
```

## 📁 Project Structure

```
hrv-research-aggregator/
├── src/
│   ├── domain/                 # Business logic (inner layer)
│   │   ├── entities/          # Core business objects
│   │   ├── value_objects/     # Immutable value types
│   │   └── services/          # Domain services
│   ├── application/           # Use cases (middle layer)
│   │   ├── ports/            # Abstract interfaces
│   │   └── use_cases/        # Application business rules
│   └── infrastructure/       # External concerns (outer layer)
│       ├── adapters/         # Concrete implementations
│       └── config/           # Configuration management
├── tests/
│   ├── unit/                 # Fast, isolated tests
│   └── integration/          # Slower, end-to-end tests
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## 🧪 Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Test-Driven Development**: Write tests first, then implementation
- **High Coverage**: Maintain >90% test coverage

## 🔍 Key Concepts Demonstrated

### 1. Dependency Inversion Principle
- High-level modules don't depend on low-level modules
- Both depend on abstractions (ports)
- Easy to swap implementations (ArXiv, Semantic Scholar, etc.)

### 2. Single Responsibility Principle
- Each class has one reason to change
- Clear, focused responsibilities
- Easy to understand and maintain

### 3. Domain-Driven Design
- Ubiquitous language in code
- Rich domain models
- Business logic in the domain layer

### 4. Test-Driven Development
- Red-Green-Refactor cycles
- Comprehensive test coverage
- Tests as living documentation

## 🔬 Research Focus

This system specifically targets Heart Rate Variability (HRV) research, including:
- ECG signal processing papers
- Wearable device studies
- Traumatic brain injury research
- Physiological monitoring systems

## 🤝 Contributing

This project is designed for educational purposes. When contributing:

1. Follow TDD practices (write tests first)
2. Maintain the clean architecture boundaries
3. Add pedagogical comments explaining design decisions
4. Ensure all tests pass and coverage remains high
5. Use conventional commits for clear history

## 📚 Learning Resources

- [Clean Architecture by Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design by Eric Evans](https://domainlanguage.com/ddd/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
