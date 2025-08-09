# Academic Paper Discovery Platform

🔬 **Educational implementation of Clean Architecture for research paper discovery and aggregation**

A comprehensive educational platform demonstrating Clean Architecture principles through practical academic research tools. This project serves as both a functional research paper discovery system and a learning resource for software engineering best practices.

[![Test Coverage](https://img.shields.io/badge/coverage-48%25-yellow)](./tests)
[![Clean Architecture](https://img.shields.io/badge/architecture-clean-blue)](./src)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://python.org)
[![Educational](https://img.shields.io/badge/purpose-educational-green)](#educational-objectives)

## 🎯 Educational Objectives

This project demonstrates professional software engineering concepts through a real-world research application:

### 🏗️ **Architecture Patterns**
- **Clean Architecture**: Strict layer separation with comprehensive documentation
- **Domain-Driven Design**: Research concepts modeled as first-class domain objects  
- **Test-Driven Development**: Red-Green-Refactor methodology with educational examples
- **Repository Pattern**: Abstract data access across multiple research databases
- **Strategy Pattern**: Pluggable search algorithms and concept extraction methods

### 🎓 **Learning Outcomes**
- Understanding Clean Architecture principles in practice
- Implementing SOLID principles in real-world scenarios
- Building maintainable, testable software systems
- Working with external APIs and data processing pipelines
- Creating comprehensive documentation and educational materials

## ✨ Features

### 🔍 **For Researchers**
- **Multi-Source Search**: Query ArXiv, PMC, MDPI, and other research databases
- **Intelligent Filtering**: Configure search strategies with domain-specific keywords
- **PDF Management**: Automatic paper download and organization
- **Concept Extraction**: AI-powered extraction of key concepts from research papers
- **Interactive Visualization**: Web-based concept mapping and exploration
- **Batch Processing**: Efficient processing of large research collections

### 🔧 **For Developers**  
- **Clean Architecture**: Pure domain logic separated from infrastructure concerns
- **Comprehensive Testing**: >90% test coverage goal with educational test examples
- **Configuration-Driven**: YAML-based research domain configuration
- **Multiple Interfaces**: CLI, menu-driven, and web interfaces for different use cases
- **Educational Documentation**: Every design decision explained with learning context

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Git
- Basic understanding of object-oriented programming

### Installation

```bash
# Clone the repository
git clone https://github.com/jdoner02/academic-paper-discovery.git
cd academic-paper-discovery

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -m pytest tests/unit/ -x
```

### Basic Usage

```bash
# List available research strategies
python search_cli.py --list-strategies

# Search for papers using a specific strategy
python search_cli.py --strategy autonomous_incident_response --limit 10

# Custom keyword search
python search_cli.py --custom "machine learning" "cybersecurity" --limit 5

# Interactive menu interface (beginner-friendly)
python main.py

# Batch process multiple configurations
python batch_processor.py
```

## 🏗️ Architecture Overview

This project implements **Clean Architecture** with strict dependency rules:

```
📦 Domain Layer (Business Logic)
├── 📝 Entities: ResearchPaper, Concept, ConceptHierarchy
├── 💎 Value Objects: SearchQuery, KeywordConfig, EvidenceSentence
└── 🔧 Services: ConceptExtractor, HierarchyBuilder, PaperDownloadService

📦 Application Layer (Use Cases) 
├── 🎯 ExecuteKeywordSearchUseCase: Orchestrates paper discovery
├── 🔍 ExtractPaperConceptsUseCase: Manages concept extraction
└── 🔌 Ports: Abstract interfaces for external dependencies

📦 Infrastructure Layer (External Concerns)
├── 🗃️ Repositories: ArxivRepository, PMCRepository, InMemoryRepository
├── 🌐 External APIs: Research database integrations
└── 📁 File System: PDF storage and configuration management

📦 Interface Layer (User Interaction)
├── 🖥️ CLI: search_cli.py (primary command-line interface)
├── 📋 Menu: main.py (user-friendly guided interface)  
├── ⚡ Batch: batch_processor.py (bulk operations)
└── 🌐 Web: Interactive visualization frontend
```

### Key Architectural Principles

- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Interface Segregation**: Clients depend only on methods they use
- **Dependency Injection**: Dependencies provided rather than created

## 📚 Educational Resources

### Learning Path

1. **Start Here**: [`src/domain/entities/research_paper.py`](src/domain/entities/research_paper.py) - Core domain model
2. **Value Objects**: [`src/domain/value_objects/search_query.py`](src/domain/value_objects/search_query.py) - Immutable value concepts  
3. **Use Cases**: [`src/application/use_cases/execute_keyword_search_use_case.py`](src/application/use_cases/execute_keyword_search_use_case.py) - Business workflows
4. **Repositories**: [`src/infrastructure/repositories/arxiv_paper_repository.py`](src/infrastructure/repositories/arxiv_paper_repository.py) - Data access patterns
5. **Integration**: [`search_cli.py`](search_cli.py) - Bringing it all together

### Documentation Structure

- [`docs/`](docs/) - Comprehensive architectural documentation
- [`tests/unit/`](tests/unit/) - Educational test examples with detailed comments
- [`config/`](config/) - Research domain configurations demonstrating strategy pattern
- [`.ai_development/`](.ai_development/) - Development session logs and lessons learned

### Key Learning Examples

```python
# Domain Entity - Research Paper with business rules
from src.domain.entities.research_paper import ResearchPaper

paper = ResearchPaper(
    title="Machine Learning in Cybersecurity",
    authors=["Dr. Jane Smith", "Prof. Bob Wilson"],
    abstract="A comprehensive review...",
    publication_date=datetime(2024, 1, 15),
    doi="10.1000/example.2024"
)

# Value Object - Immutable search configuration  
from src.domain.value_objects.search_query import SearchQuery

query = SearchQuery(
    terms=["machine learning", "cybersecurity"],
    max_results=50,
    min_citations=10
)

# Use Case - Clean separation of business logic
from src.application.use_cases.execute_keyword_search_use_case import ExecuteKeywordSearchUseCase

use_case = ExecuteKeywordSearchUseCase(repository=arxiv_repo)
results = use_case.execute_strategy("cybersecurity_ml")
```

## 🧪 Testing Strategy

This project follows **Test-Driven Development** with educational focus:

```bash
# Run all tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test categories
python -m pytest tests/unit/domain/          # Domain logic tests
python -m pytest tests/unit/application/     # Use case tests  
python -m pytest tests/unit/infrastructure/  # Integration tests

# Follow TDD Red-Green-Refactor cycle
python -m pytest tests/unit/domain/entities/test_research_paper.py -v
```

### Test Organization

- **Domain Tests**: Validate business rules and domain logic
- **Application Tests**: Verify use case orchestration and workflows
- **Infrastructure Tests**: Ensure external integrations work correctly
- **Integration Tests**: Test complete workflows end-to-end

## 🔧 Configuration

Research domains are configured using YAML files in [`config/`](config/):

```yaml
# config/cybersecurity_ml.yaml
search_configuration:
  default_strategy: "ml_security"
  citation_threshold: 5
  publication_date_range:
    start_year: 2020
    end_year: 2025

strategies:
  ml_security:
    name: "Machine Learning in Cybersecurity"
    description: "AI and ML applications in cybersecurity research"
    primary_keywords:
      - "machine learning cybersecurity"
      - "AI security"
    secondary_keywords:
      - "neural networks security"
      - "deep learning threats"
    max_results: 50
```

## 🌐 Web Interface

Interactive visualization platform available at: [GitHub Pages Demo](https://jdoner02.github.io/academic-paper-discovery/)

Features:
- **Interactive Concept Maps**: D3.js visualizations of research landscapes
- **Real-time Filtering**: Search and filter concepts dynamically
- **Evidence Navigation**: Click concepts to view supporting evidence
- **Mobile Responsive**: Full functionality across all devices

## 📈 Project Status

### Current State
- ✅ **Core Architecture**: Clean Architecture foundation implemented
- ✅ **Primary Use Cases**: Paper discovery and concept extraction working
- ✅ **Multiple Interfaces**: CLI, menu, and web interfaces available
- ✅ **Test Foundation**: 445 passing tests with core functionality covered
- ⏳ **Documentation**: Comprehensive educational documentation in progress
- ⏳ **Test Coverage**: Working toward >90% coverage goal

### Roadmap
1. **Enhanced Documentation**: Complete educational guides and examples
2. **Test Coverage**: Achieve >90% test coverage with comprehensive examples
3. **Advanced Features**: Semantic search, citation analysis, research trends
4. **Performance**: Optimization for large-scale research collections

## 🤝 Contributing

This is an educational project welcoming contributions that enhance learning value:

1. **Educational Focus**: Prioritize clear, well-documented examples over features
2. **Clean Architecture**: Maintain strict layer separation and dependency rules  
3. **Test Coverage**: Include comprehensive tests with educational comments
4. **Documentation**: Explain the "why" behind architectural decisions

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see [`LICENSE`](LICENSE) for details.

## 🙏 Acknowledgments

- **Clean Architecture**: Inspired by Robert C. Martin's architectural principles
- **Domain-Driven Design**: Concepts from Eric Evans' domain modeling approach
- **Educational Community**: Built for students and educators in computer science
- **Open Source Research**: Supporting open access to academic research tools

---

**🎓 Educational Note**: This project demonstrates professional software engineering practices in a real-world context. Every architectural decision includes educational explanations to support learning and understanding of Clean Architecture principles.
