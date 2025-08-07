# 🔬 Research Paper Discovery Platform

**Interactive exploration of academic literature through concept visualization**

[![GitHub Pages](https://img.shields.io/badge/demo-live-brightgreen)](https://jdoner02.github.io/academic-paper-discovery/)
[![Research Domains](https://img.shields.io/badge/domains-30-blue)](#)
[![Research Papers](https://img.shields.io/badge/papers-1161-orange)](#)
[![Extracted Concepts](https://img.shields.io/badge/concepts-3000-purple)](#)

## ✨ Features

### 🎯 **For Researchers**
- **30 Research Domains**: Cybersecurity, quantum cryptography, incident response, healthcare security, and more
- **Interactive Concept Maps**: Click concepts to explore evidence sentences from source papers
- **Direct PDF Access**: Click evidence sentences to open full research papers
- **Mobile Responsive**: Full functionality on all devices
- **Real Research Data**: 1,161 papers with 3,000 extracted concepts

### 🔧 **For Developers** 
- **Static GitHub Pages Deployment**: No server infrastructure required
- **Clean Architecture**: Separation of data preparation and client-side application
- **Modern Web Technologies**: D3.js visualizations, Bootstrap 5, responsive design
- **Educational Documentation**: Comprehensive code comments and design explanations

## 🚀 Live Demo

**Visit the platform**: [https://jdoner02.github.io/academic-paper-discovery/](https://jdoner02.github.io/academic-paper-discovery/)

### How to Use:
1. **Select Domain**: Choose from 30+ research domains (cybersecurity, quantum cryptography, etc.)
2. **Explore Concepts**: Interactive bubble chart shows extracted concepts by frequency
3. **View Evidence**: Click concepts to see supporting sentences from papers
4. **Access Papers**: Click evidence sentences to open PDFs directly

## 🏗️ Architecture

### Static Data Pipeline
```
Research Papers (PDFs) → Concept Extraction → Static JSON Files → GitHub Pages
```

**Data Preparation**:
- `scripts/build_static_data.py` - Transforms concept storage into web-optimized JSON
- `static_data/` - Optimized data files for fast client-side loading
- Automatic domain indexing and concept aggregation

**Client-Side Application**:
- `index.html` - Single-page application with D3.js visualizations
- Pure client-side JavaScript (no server required)
- Bootstrap 5 responsive design
- Interactive concept exploration

### Research Domains Available

| Domain | Papers | Focus Area |
|--------|--------|------------|
| **Post-Quantum Cryptography** | 49 | Quantum-resistant cryptographic systems |
| **Medical Device Cybersecurity** | 50 | Healthcare IoT and device security |
| **Incident Response Optimization** | 49 | Emergency response and disaster recovery |
| **AI-Driven Cyber Defense** | 45 | Machine learning in cybersecurity |
| **Water Infrastructure Security** | 47 | Critical infrastructure protection |
| **Election System Security** | 49 | Voting technology and election integrity |
| **Grid Communication Security** | 44 | Smart grid and power system security |
| **...and 23 more domains** | 868 | Comprehensive cybersecurity research |

## 🛠️ Development

### Prerequisites
- Python 3.8+ (for data preparation)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/jdoner02/academic-paper-discovery.git
cd academic-paper-discovery
```

2. **Build static data** (if concept storage is updated):
```bash
python scripts/build_static_data.py
```

3. **Start local server**:
```bash
python -m http.server 8080
```

4. **Open browser**: Visit `http://localhost:8080`

### Data Structure

```
static_data/
├── domains.json              # Domain index with metadata
├── statistics.json           # Overall platform statistics  
├── {domain}/
│   └── concepts.json         # Concept data with evidence sentences
outputs/
├── {domain}/
│   └── {strategy}/
│       └── pdfs/            # Research paper PDFs
concept_storage/
└── concepts/
    └── {domain}/            # Raw extracted concept data
```

## 📊 Data Sources

All research papers are sourced from:
- **ArXiv.org**: Computer science, mathematics, physics preprints
- **MDPI Journals**: Open-access academic publications
- **Academic Repositories**: Peer-reviewed research across domains

## 🎓 Educational Value

This project demonstrates:

**Modern Web Development**:
- Static site generation and deployment
- Client-side data visualization with D3.js
- Responsive design principles
- Progressive enhancement

**Data Science Pipeline**:
- Academic text processing and concept extraction
- Data transformation for web consumption
- Statistical analysis and visualization

**Software Architecture**:
- Clean separation of data preparation and presentation
- Scalable static deployment strategy
- Performance optimization for large datasets

## 🔄 Updates

The platform is updated with new research papers and domains regularly. The static data generation process allows for easy updates without server downtime.

**Last Updated**: August 7, 2025
- 30 research domains
- 1,161 research papers
- 3,000+ extracted concepts

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Adding new research domains
- Improving concept extraction algorithms
- Enhancing the user interface
- Adding new visualization types

## 📞 Contact

- **Repository**: [github.com/jdoner02/academic-paper-discovery](https://github.com/jdoner02/academic-paper-discovery)
- **Issues**: [Report bugs or request features](https://github.com/jdoner02/academic-paper-discovery/issues)
- **Discussions**: [Join community discussions](https://github.com/jdoner02/academic-paper-discovery/discussions)

---

**Transform your literature review process with interactive concept exploration** 🚀
