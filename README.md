# Research Paper Aggregator 🔍📚
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://img.shields.io/badge/coverage-95%25-green.svg)](htmlcov/index.html)

> **🎯 One-Click Academic Research Discovery** - Clone, run, and start discovering papers across multiple research domains in under 2 minutes!

**Perfect for**: Researchers, PhD students, academics, and anyone who needs to stay current with literature in cybersecurity, post-quantum cryptography, medical research, or any academic domain.

---

## ✨ What This Does

Research Paper Aggregator transforms tedious literature searches into automated discovery pipelines. Instead of manually searching through multiple academic databases, our system:

- **🤖 Automates Literature Discovery**: Runs intelligent searches across arXiv and other databases
- **📂 Organizes Results**: Downloads papers with structured metadata and organized folders  
- **🔄 Provides Continuous Updates**: Set up automated daily/weekly research monitoring
- **🎯 Multi-Domain Support**: Pre-configured for cybersecurity, cryptography, medical research, and more
- **🖥️ User-Friendly Interface**: Interactive menu system - no command-line expertise needed

## 🚨 The Academic Research Problem

Staying current with rapidly evolving fields is overwhelming:

- **Information Overload**: Thousands of papers published daily across multiple venues

- **Keyword Variations**: Different fields use varying terminology for similar concepts
- **Domain Fragmentation**: Papers appear across multiple specialized journals and conferences
- **Manual Process**: Copy-pasting search terms and managing PDF downloads is time-intensive
- **Inconsistent Metadata**: Different sources format author names, dates, and abstracts differently

## The Solution

Research Paper Aggregator automates intelligent paper discovery across multiple academic domains using:

- **🔍 Multi-Domain Support**: Pre-configured for cybersecurity, post-quantum cryptography, medical research, and more
- **📥 Automated Downloads**: One-click PDF downloads with organized folder structure
- **🏗️ Clean Architecture**: Extensible design supporting multiple academic databases
- **⚙️ Production Ready**: Cron job automation for continuous research monitoring
- **📊 Rich Metadata**: Standardized paper information across all sources
- **🎯 Interactive Menu**: User-friendly interface - just run `python3 main.py`

## ⚡ Super Quick Start (2 Minutes)

### 1. Clone and Run
```bash
# Clone the repository
git clone https://github.com/jessicadoner/research-paper-aggregator.git
cd research-paper-aggregator

# Install dependencies
pip install -e .

# Run the interactive menu system
python3 main.py
```

### 2. Choose Your Research Domain
The interactive menu will show you available research domains:
- **🫀 Medical Research** (Heart Rate Variability, TBI studies, wearable technology)
- **🔒 Cybersecurity Water Infrastructure** (SCADA security, critical infrastructure, IoT)  
- **🔐 Post Quantum Cryptography** (Lattice-based, code-based, NIST standards)

### 3. Select Strategy and Go!
Pick a research strategy, choose your options, and watch as papers are automatically discovered and downloaded!

**🎉 That's it!** No complex configuration needed - perfect for busy academics.

## ⚡ Command Line Interface (Advanced)

### Using the Legacy CLI (Optional)
If you prefer command-line interfaces, you can also use the original CLI:

```bash
# List available research strategies
python3 search_research.py --list-strategies

# Search for cybersecurity infrastructure papers
python3 search_research.py --strategy scada_security --limit 10

# Download the latest post-quantum cryptography papers
python3 search_research.py --strategy lattice_cryptography --download --limit 5
```

### Custom Search Terms
```bash
# Search with custom keywords for any domain
python3 search_research.py --custom "quantum computing" "cryptography" "security"

# Use different data sources
python3 search_research.py --source arxiv --strategy comprehensive_search
python3 search_research.py --source sample --custom "research terms" --limit 3  # Demo mode
```

## 📋 Available Research Domains & Strategies

### 🫀 Medical Research
- **Broad HRV Research**: Comprehensive search across all Heart Rate Variability applications
- **Clinical Applications**: Hospital-based studies, patient populations, diagnostic applications
- **TBI Focused**: Traumatic Brain Injury research combined with physiological monitoring
- **Wearable Technology**: Consumer devices, Apple Watch, Fitbit, research-grade monitors

### 🔒 Cybersecurity Water Infrastructure
- **SCADA Security**: Supervisory Control and Data Acquisition system vulnerabilities
- **Critical Infrastructure Protection**: Power grid, water treatment, municipal systems
- **IoT Security**: Internet of Things devices in water management systems
- **Network Intrusion Detection**: Monitoring and protecting water infrastructure networks

### 🔐 Post Quantum Cryptography
- **Lattice-Based Cryptography**: NTRU, LWE, Ring-LWE cryptographic systems
- **Code-Based Cryptography**: McEliece, Niederreiter, and error-correcting codes
- **NIST Standardization**: Post-quantum cryptography standardization process
- **Quantum-Resistant Protocols**: TLS, SSH, and other protocol adaptations

## 🔧 Advanced Configuration

### Adding Your Own Research Domain
1. Create a new YAML file in `config/` directory:

```yaml
# config/my_research_domain.yaml
strategies:
  comprehensive_search:
    base_terms:
      - "primary research concept"
      - "alternative terminology"
    domain_terms:
      - "specific application area"
    method_terms:
      - "research methodology"
    exclusion_terms:
      - "terms to exclude"

metadata:
  domain: "My Research Domain"
  description: "Description of your research area"
  last_updated: "2024-01-15"
```

2. Run `python3 main.py` - your domain will automatically appear in the menu!

## 📈 Production Deployment

### Automated Daily Research Updates

Set up cron jobs to automatically discover new papers:

```bash
# Edit your crontab
crontab -e

# Add these lines for automated research monitoring:

# Daily cybersecurity research check (9 AM)
0 9 * * * cd /path/to/research-paper-aggregator && python3 main.py --config cybersecurity_water_infrastructure.yaml --strategy scada_security --auto-download >> ~/logs/research_cyber.log 2>&1

# Weekly post-quantum cryptography survey (Monday 8 AM)  
0 8 * * 1 cd /path/to/research-paper-aggregator && python3 main.py --config post_quantum_cryptography.yaml --strategy lattice_cryptography --limit 20 --auto-download >> ~/logs/research_pqc.log 2>&1

# Monthly broad research review (1st of month, 7 AM)
0 7 1 * * cd /path/to/research-paper-aggregator && python3 main.py --config search_keywords.yaml --strategy broad_hrv_research --limit 30 --auto-download >> ~/logs/research_medical.log 2>&1
```

### Research Team Deployment

For research teams, set up a centralized server:

```bash
# 1. Set up a dedicated research server
mkdir -p ~/hrv-research-server/{logs,outputs,config}
cd ~/hrv-research-server
git clone https://github.com/yourusername/hrv-research-aggregator.git
cd hrv-research-aggregator

# 2. Install system-wide
pip install -e .

# 3. Configure custom search strategies
cp config/search_keywords.yaml ~/hrv-research-server/config/team_strategies.yaml
# Edit ~/hrv-research-server/config/team_strategies.yaml with your team's keywords

# 4. Set up automated runs
python3 search_hrv.py --config ~/hrv-research-server/config/team_strategies.yaml \
  --strategy your_custom_strategy --download \
  --output-dir ~/hrv-research-server/outputs/$(date +%Y-%m-%d)
```

### Monitoring and Alerts

Monitor your automated research pipeline:

```bash
# Create monitoring script
cat > ~/monitor_hrv_research.sh << 'EOF'
#!/bin/bash
LOG_DIR=~/logs
ALERT_EMAIL="your-email@domain.com"

# Check if searches are running successfully
if ! tail -n 10 "$LOG_DIR/hrv_tbi.log" | grep -q "completed successfully"; then
    echo "HRV TBI search may have failed - check logs" | mail -s "HRV Research Alert" $ALERT_EMAIL
fi

# Check disk space for downloads
USAGE=$(df ~/research | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $USAGE -gt 80 ]; then
    echo "Research storage is ${USAGE}% full - consider archiving old papers" | mail -s "HRV Storage Alert" $ALERT_EMAIL
fi
EOF

chmod +x ~/monitor_hrv_research.sh

# Run monitoring check daily at 6 PM
echo "0 18 * * * ~/monitor_hrv_research.sh" | crontab -
```

## 📖 Complete CLI Reference

### Core Commands

```bash
# Basic search strategies
python3 search_hrv.py --strategy <strategy_name>
python3 search_hrv.py --custom <keyword1> <keyword2> ...
python3 search_hrv.py --list-strategies

# Download control
python3 search_hrv.py --download                    # Download PDFs when available
python3 search_hrv.py --output-dir /custom/path     # Custom download location
python3 search_hrv.py --limit 25                    # Limit results (default: 10)

# Data sources
python3 search_hrv.py --source arxiv                # Real arXiv papers (default)
python3 search_hrv.py --source sample               # Demo data for testing

# Configuration
python3 search_hrv.py --config /custom/keywords.yaml # Custom keyword file
```

### Example Workflows

```bash
# 1. Explore available research areas
python3 search_hrv.py --list-strategies
# Output: broad_hrv_research, tbi_focused, wearable_technology, clinical_applications

# 2. Quick research overview (no downloads)
python3 search_hrv.py --strategy broad_hrv_research --limit 15

# 3. Focused research with downloads
python3 search_hrv.py --strategy tbi_focused --download --limit 10 --output-dir ~/research/tbi_papers

# 4. Custom research query
python3 search_hrv.py --custom "heart rate variability" "machine learning" "deep learning" --download

# 5. Testing with sample data
python3 search_hrv.py --source sample --custom "ECG" "wearable"
```

### Output Structure

Downloaded papers are organized automatically:

```
outputs/
└── 2025-01-15_tbi_focused/           # Date and strategy
    ├── papers/
    │   ├── paper_1.pdf               # Downloaded PDFs
    │   ├── paper_2.pdf
    │   └── ...
    ├── metadata.json                 # All paper information
    └── search_summary.json           # Search configuration and stats
```

## 🏗️ Architecture Overview

This system follows **Clean Architecture** principles for maintainability and extensibility:

### 🔵 Domain Layer (Business Logic)
- **Entities**: `ResearchPaper`, `Author` - Core business objects with identity
- **Value Objects**: `SearchQuery`, `KeywordConfig` - Immutable data structures  
- **Domain Services**: Business logic that doesn't fit naturally in entities

### 🟡 Application Layer (Use Cases)
- **Ports**: Abstract interfaces (`PaperRepository`, `DownloadService`)
- **Use Cases**: `ExecuteKeywordSearchUseCase` - Application business rules
- **Orchestration**: Coordinates domain objects and infrastructure services

### � Infrastructure Layer (External Concerns)
- **Repositories**: `ArxivPaperRepository` - Concrete data access implementations
- **Services**: `PaperDownloadService` - PDF download and file management
- **Adapters**: CLI interface, configuration loading, external API clients

### 🔄 Dependency Flow
```
CLI → Use Cases → Domain ← Infrastructure
         ↓           ↑
    Application → Ports ← Adapters
```

## 🛠️ Development Setup

### Development Environment

```bash
# Clone and set up development environment
git clone https://github.com/jdoner02/hrv-research-aggregator.git
cd hrv-research-aggregator

# Install with development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test categories
pytest tests/unit/           # Fast unit tests only  
pytest tests/integration/    # Slower integration tests
pytest -k "test_search"      # Tests matching pattern
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Type checking  
mypy src

# Linting
flake8 src tests

# Run all quality checks
./scripts/quality_check.sh
```

## 🔧 Configuration

### Search Strategies

Customize research focus by editing `config/search_keywords.yaml`:

```yaml
strategies:
  my_custom_research:
    name: "My Custom Research Focus"
    description: "Papers on specific HRV applications"
    primary_keywords:
      - "heart rate variability"
      - "HRV analysis"
    secondary_keywords:
      - "my specific domain"
      - "my target application"
    exclusion_keywords:
      - "exclude these terms"
    search_limit: 50
    date_range:
      start: "2020-01-01"
      end: null  # null means present
```

### Environment Variables

```bash
# Optional configuration via environment variables
export HRV_DEFAULT_LIMIT=20
export HRV_DEFAULT_OUTPUT_DIR=~/my_research
export HRV_DEFAULT_CONFIG=~/my_keywords.yaml
```

## ❗ Troubleshooting

### Common Issues

**Q: "ModuleNotFoundError: No module named 'feedparser'"**
```bash
# Install missing dependencies
pip install feedparser PyYAML

# Or reinstall the package
pip install -e .
```

**Q: "No papers found" for arXiv searches**
```bash
# Test with sample data first
python3 search_hrv.py --source sample --custom "test"

# Check internet connection and arXiv availability
curl -s "http://export.arxiv.org/api/query?search_query=heart+rate+variability&max_results=1"
```

**Q: PDF downloads failing**
```bash
# Check download directory permissions
ls -la outputs/
mkdir -p outputs && chmod 755 outputs

# Test with a small download first
python3 search_hrv.py --custom "HRV" --download --limit 1
```

**Q: Cron jobs not running**
```bash
# Check cron service is running
sudo systemctl status cron  # Linux
launchctl list | grep cron  # macOS

# Check cron logs
tail -f /var/log/cron.log    # Linux  
grep cron /var/log/system.log # macOS

# Test cron job manually
cd /path/to/hrv-research-aggregator && python3 search_hrv.py --strategy tbi_focused --limit 1
```

### Getting Help

- 📖 **Documentation**: Check inline help with `python3 search_hrv.py --help`
- 🐛 **Bug Reports**: [Create an issue](https://github.com/jdoner02/hrv-research-aggregator/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/jdoner02/hrv-research-aggregator/discussions)
- 📧 **Contact**: jessica@jessicadoner.com

## 🤝 Contributing

We welcome contributions! This project serves both production use and educational purposes.

### Quick Contribution Guide

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Follow** our development practices:
   - Write tests first (TDD)
   - Maintain Clean Architecture boundaries  
   - Add docstrings and type hints
   - Keep test coverage >90%
4. **Commit** with conventional format: `feat: add amazing feature`
5. **Push** and create a Pull Request

### Development Principles

- **Test-Driven Development**: Write failing tests first, then make them pass
- **Clean Architecture**: Respect layer boundaries and dependency directions
- **Domain-Driven Design**: Use ubiquitous language from HRV research domain
- **Educational Value**: Code should teach Clean Architecture principles

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📊 Project Stats

- **🏗️ Architecture**: Clean Architecture with 3 distinct layers
- **🧪 Test Coverage**: 95%+ on domain and application layers  
- **📚 Documentation**: Comprehensive inline documentation and examples
- **🔌 Extensibility**: Plugin architecture for new paper sources
- **⚡ Performance**: Async operations and connection pooling
- **🛡️ Type Safety**: Full type hints with mypy validation

## 🔮 Roadmap

### Upcoming Features

- **📊 Analytics Dashboard**: Web interface for search trends and paper discovery
- **🤖 AI Classification**: Automatic paper categorization using machine learning
- **📈 Citation Tracking**: Monitor citation networks and research impact
- **🔔 Smart Alerts**: ML-powered notifications for papers matching your interests
- **🌐 Multi-Source**: Support for PubMed, IEEE, Semantic Scholar APIs
- **📱 Mobile App**: iOS/Android app for researcher on-the-go access

### Integration Opportunities

- **🔬 Research Platforms**: Mendeley, Zotero, EndNote integration
- **📊 Analytics Tools**: Export to R, Python pandas, Jupyter notebooks  
- **☁️ Cloud Deployment**: AWS, GCP, Azure deployment guides
- **🤝 Team Collaboration**: Shared research libraries and annotation tools

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Heart Rate Variability Research Community** for domain expertise and feedback
- **Clean Architecture Community** for architectural patterns and best practices
- **arXiv.org** for providing free access to scientific papers
- **Contributors** who have helped improve this project

---

**⭐ If this project helps your research, please give it a star on GitHub!**

**🔬 Built by researchers, for researchers. Happy researching! 🫀📚**

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
