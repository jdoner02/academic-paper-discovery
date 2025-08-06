# Interactive Research Paper Discovery Platform

🔬 **Transform academic paper collections into intuitive visual concept maps**

An interactive web platform that uses machine learning and visualization to help researchers explore literature landscapes without technical barriers.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen)](https://jdoner02.github.io/academic-paper-discovery/)
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](./tests)
[![Clean Architecture](https://img.shields.io/badge/architecture-clean-blue)](./src)
[![TDD](https://img.shields.io/badge/methodology-TDD-orange)](./tests)

## ✨ Features

### 🎯 **For Researchers**
- **Visual Concept Maps**: Interactive D3.js visualizations of research landscapes
- **Evidence-Based Navigation**: Click concepts to see supporting sentences from papers
- **Mobile-Responsive Design**: Full functionality on all devices
- **No Technical Barriers**: Form-based configuration, no command-line required

### 🔧 **For Developers**
- **Clean Architecture**: Strict layer separation with educational documentation
- **Test-Driven Development**: 95%+ test coverage with Red-Green-Refactor methodology
- **Comprehensive Documentation**: Every design decision explained
- **Professional Patterns**: Repository, Strategy, Factory, Adapter patterns demonstrated

## 🚀 Quick Start

### For End Users

1. **Visit the Live Platform**: [jdoner02.github.io/academic-paper-discovery](https://jdoner02.github.io/academic-paper-discovery/)
2. **Select Research Area**: Choose from available research domains
3. **Configure Search**: Check/uncheck search strategies
4. **Explore Concepts**: Navigate interactive concept maps
5. **Access Papers**: Click evidence sentences to read full papers

### For Developers

```bash
# Clone the repository
git clone https://github.com/jdoner02/academic-paper-discovery.git
cd academic-paper-discovery

# Install dependencies
npm install

# Run tests (TDD approach - run tests first!)
npm test

# Start development server
npm run dev

# Build for production
npm run build
npm run export
```

## 🧪 Test-Driven Development

We follow strict **Red-Green-Refactor** methodology with 33/33 tests passing.

### Running Tests
```bash
# Run all tests
npm test

# Watch mode for TDD
npm run test:watch

# Coverage report
npm run test:coverage
```

## 🤝 Contributing

### Development Setup
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Write tests first**: Follow TDD Red-Green-Refactor
4. **Implement feature**: Keep tests passing
5. **Add documentation**: Explain architectural decisions
6. **Submit pull request**: Include test coverage and documentation

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the academic research community**
