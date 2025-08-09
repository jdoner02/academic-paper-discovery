# Research Paper Aggregator

🔍 **Intelligent academic research paper discovery and aggregation** following Clean Architecture principles and educational best practices.

## 🏗️ Architecture Overview

This repository demonstrates **Clean Architecture** in a real-world academic research context:

```
research-paper-aggregator/
├── src/                        # Clean Architecture implementation
│   ├── domain/                 # Business logic and entities  
│   ├── application/            # Use cases and ports
│   ├── infrastructure/         # External dependencies
│   └── web/                    # Next.js frontend
├── cli/                        # Command-line interfaces
├── config/                     # Configuration management
├── data/                       # Research data (Git LFS)
├── tests/                      # Comprehensive test suite
└── docs/                       # Technical documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git LFS (for research data)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/research-paper-aggregator.git
cd research-paper-aggregator

# Install Python dependencies
pip install -e .

# Install Node.js dependencies
cd src/web && npm install

# Setup Git LFS
git lfs install
git lfs pull
```

### Usage

#### Command Line Interface
```bash
# Search for papers
python cli/main.py search --keywords "quantum cryptography post-quantum"

# Extract concepts from papers
python cli/main.py extract --papers ./data/research_outputs/

# Start web interface
python cli/main.py web --port 3000
```

#### Web Interface
```bash
cd src/web
npm run dev
# Open http://localhost:3000
```

## 🎓 Educational Goals

This repository serves as a **comprehensive educational example** demonstrating:

### Clean Architecture Principles
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Single Responsibility**: Each component has one reason to change
- **Open/Closed**: Open for extension, closed for modification

### Software Engineering Best Practices
- **Test-Driven Development**: >90% test coverage
- **Git LFS Management**: Proper handling of large academic datasets
- **Configuration Management**: YAML-based, environment-specific configs
- **Documentation**: Comprehensive, pedagogically-focused documentation

### Domain-Driven Design
- **Entities**: ResearchPaper, Concept, Author
- **Value Objects**: SearchQuery, KeywordConfig, PaperFingerprint
- **Use Cases**: ExecuteKeywordSearchUseCase, ExtractPaperConceptsUseCase
- **Repositories**: Abstract data access patterns

## 📊 Research Domains

Current support for research paper discovery in:

- **Cybersecurity**: Network security, cryptography, incident response
- **Post-Quantum Cryptography**: Migration strategies, implementation challenges  
- **Healthcare Technology**: Medical devices, privacy compliance
- **Critical Infrastructure**: Water systems, smart grids, IoT security
- **Programming Education**: CS1/CS2 pedagogy, cognitive load theory

## 🧪 Testing Strategy

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests
```

## 🌟 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed contribution guidelines following academic best practices.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🎯 Learning Objectives

Students using this repository will learn:

1. **Clean Architecture Implementation** in Python
2. **Domain-Driven Design** for complex academic domains
3. **Test-Driven Development** with high coverage standards
4. **Git LFS Management** for academic repositories
5. **Configuration-Driven Development** with YAML
6. **Modern Web Development** with React/Next.js
7. **Command-Line Interface Design** with Python argparse
8. **Documentation Best Practices** for educational code

---

**Built with ❤️ for Computer Science Education at Eastern Washington University**
