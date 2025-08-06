# 🔍📚 Academic Paper Discovery

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A general-purpose academic research paper discovery and aggregation tool built with **Clean Architecture** principles. Perfect for CS students learning domain-driven design, SOLID principles, and architectural patterns.

## ✨ Features

- 🌍 **Multi-Domain Support**: Research any field via YAML configuration files
- 🎯 **Intelligent Search Strategies**: Pre-configured and custom search approaches  
- 📥 **Automated Downloads**: Papers organized in domain-specific folders
- 🔄 **Duplicate Prevention**: Smart deduplication of papers
- 🏗️ **Educational Codebase**: Extensive pedagogical documentation
- 🎮 **Interactive Menu**: User-friendly domain and strategy selection
- 🧪 **Comprehensive Tests**: 102 unit tests with 90%+ coverage goals

## 🏗️ Architecture

This project demonstrates **Clean Architecture** with clear separation of concerns:

```
📦 Domain Layer (Business Logic)
├── 📝 Entities: ResearchPaper
├── 💎 Value Objects: SearchQuery, KeywordConfig, SearchStrategy
└── 🔧 Services: PaperDownloadService

📦 Application Layer (Use Cases) 
└── 🎯 ExecuteKeywordSearchUseCase

📦 Infrastructure Layer (External)
├── 🌐 ArxivPaperRepository
└── 💾 InMemoryPaperRepository
```

### 🎓 Educational Value

Perfect for learning:
- **SOLID Principles**: Single Responsibility, Open/Closed, Dependency Inversion
- **Design Patterns**: Repository, Strategy, Factory, Command, Facade
- **Domain-Driven Design**: Entities, Value Objects, Domain Services
- **Clean Architecture**: Layer separation and dependency inversion
- **Test-Driven Development**: Comprehensive unit testing

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- Internet connection for arXiv API

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jdoner02/academic-paper-discovery.git
   cd academic-paper-discovery
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### 🎮 Usage

The interactive menu guides you through:

1. **Select Research Domain**: Choose from available YAML configurations
2. **Pick Search Strategy**: Select from predefined research strategies  
3. **Configure Download**: Preview or download papers to local folders
4. **Set Parameters**: Adjust number of papers and other settings

## 📋 Available Research Domains

### 🔐 Cybersecurity & Water Infrastructure
- Critical Infrastructure Security
- SCADA Systems Security  
- Threat Analysis & IoT Security
- Incident Response

### 🔒 Post-Quantum Cryptography
- Quantum-Resistant Algorithms
- Lattice-Based Cryptography
- Code-Based & Multivariate Schemes
- Implementation & Standards

### ❤️ Heart Rate Variability (HRV)
- Medical Applications & TBI Research
- Technology & Wearables Integration
- Analysis Methods & Algorithms
- Clinical Studies

## 🛠️ Configuration

Create new research domains by adding YAML files to `config/`:

```yaml
strategies:
  strategy_name:
    description: "Brief description"
    primary_keywords:
      - "main term 1"
      - "main term 2"
    secondary_keywords:  
      - "supporting term 1"
      - "supporting term 2"
    search_limit: 50
    date_range:
      start_year: 2020
      end_year: 2024

search_configuration:
  default_strategy: "strategy_name"
  citation_threshold: 5
  exclude_terms: ["exclude1", "exclude2"]
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/unit/test_keyword_config.py -v
```

**Test Coverage**: 102 unit tests covering domain logic, value objects, and use cases.

## 📁 Project Structure

```
academic-paper-discovery/
├── 📂 config/                    # YAML configuration files
│   ├── cybersecurity_water_infrastructure.yaml
│   ├── post_quantum_cryptography.yaml
│   └── heart_rate_variability.yaml
├── 📂 src/
│   ├── 📂 domain/               # Business logic (no external dependencies)
│   │   ├── 📂 entities/         # Core business objects  
│   │   ├── 📂 value_objects/    # Immutable domain concepts
│   │   └── 📂 services/         # Domain services
│   ├── 📂 application/          # Use cases and ports
│   │   ├── 📂 use_cases/        # Business workflows
│   │   └── 📂 ports/            # Abstract interfaces
│   └── 📂 infrastructure/       # External systems integration
│       └── 📂 repositories/     # Data access implementations
├── 📂 tests/
│   ├── 📂 unit/                 # Component-level tests
│   └── 📂 integration/          # System-level tests  
├── 📂 outputs/                  # Downloaded papers (organized by domain/date)
├── main.py                      # Interactive menu application
├── search_research.py           # CLI script interface
└── README.md
```

## 🔧 Command Line Interface

For advanced users, use the CLI directly:

```bash
# List available strategies
python search_research.py --list-strategies

# Search with a specific strategy  
python search_research.py --strategy critical_infrastructure_security --limit 10

# Custom search terms
python search_research.py --custom "quantum computing" "security" --download
```

## 🤝 Contributing

This project welcomes contributions! Areas for enhancement:

- 🌐 Additional data sources (PubMed, Google Scholar, etc.)
- 📊 Advanced filtering and ranking algorithms  
- 🎨 Web interface or GUI
- 📈 Analytics and visualization features
- 🔧 Performance optimizations
- 📚 Additional research domain configurations

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes with comprehensive tests
4. Run the test suite: `python -m pytest`
5. Submit a pull request

## 📖 Learning Resources

### Clean Architecture
- [Uncle Bob's Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design Fundamentals](https://www.pluralsight.com/courses/domain-driven-design-fundamentals)

### Design Patterns  
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)

### Python Best Practices
- [Clean Code in Python](https://github.com/zedr/clean-code-python)
- [Test-Driven Development](https://testdriven.io/courses/tdd-flask/)

## 🎯 Educational Focus

This codebase is specifically designed for **Computer Science education**:

- **Clean Architecture**: Demonstrates proper layer separation and dependency inversion
- **SOLID Principles**: Each principle is illustrated with concrete examples
- **Design Patterns**: Repository, Strategy, Factory, Command, and Facade patterns
- **Domain-Driven Design**: Rich domain models with ubiquitous language
- **Test-Driven Development**: Comprehensive test suite with high coverage
- **Type Safety**: Full type hints throughout the codebase

### Key Learning Outcomes

Students working with this codebase will understand:

1. **How to structure large applications** using Clean Architecture
2. **Dependency management** and inversion of control
3. **Domain modeling** and business logic separation  
4. **Test strategies** for different architectural layers
5. **Configuration management** and external system integration
6. **Code quality** practices and maintainable design

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **arXiv API**: For providing access to academic papers
- **Clean Architecture Community**: For architectural guidance
- **Python Testing Community**: For testing best practices

---

**Built with ❤️ for Computer Science Education**

*Transform this codebase for your own research domain and learn Clean Architecture principles in the process!*