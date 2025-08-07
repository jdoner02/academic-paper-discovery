# Research Paper Aggregator - Documentation Wiki

## Overview
This wiki provides comprehensive documentation for the Research Paper Aggregator system, designed for academic concept extraction and hierarchical mapping. The system serves STEM students and faculty across Computer Science, Mathematics, Physics, Engineering, and Cybersecurity disciplines.

## 🏗️ Architecture Documentation

### [[Clean Architecture Overview]]
- Domain-Driven Design principles
- Layer separation and dependencies
- SOLID principles application

### [[Domain Layer]]
- [[Entities]] - Core business objects with identity
- [[Value Objects]] - Immutable domain concepts
- [[Domain Services]] - Business logic coordination
- [[Aggregates]] - Consistency boundaries

### [[Application Layer]]
- [[Use Cases]] - Business operations orchestration
- [[Ports]] - Interface definitions for external dependencies
- [[Application Services]] - Cross-cutting concerns

### [[Infrastructure Layer]]
- [[Repositories]] - Data access implementations
- [[External Services]] - Third-party integrations
- [[Configuration]] - System setup and parameters

## 🧠 Concept Extraction System

### [[Concept Extraction Pipeline]]
- [[Multi-Strategy Extraction]] - Hybrid approach combining multiple methods
- [[Rule-Based Extraction]] - Linguistic patterns and ontologies
- [[Statistical Methods]] - TF-IDF, TextRank, LDA topic modeling
- [[Embedding-Based Clustering]] - Semantic similarity and hierarchical organization

### [[Hierarchical Organization]]
- [[Concept Hierarchies]] - Tree structures and taxonomies
- [[Evidence Grounding]] - Sentence-level support and traceability
- [[Quality Metrics]] - Validation and confidence scoring

## 🎨 Visualization System

### [[Interactive D3.js Visualization]]
- [[Concept Sunburst]] - Zoomable hierarchical visualization
- [[Force-Directed Networks]] - Alternative visualization approach
- [[Evidence Panels]] - Interactive evidence display and PDF linking

### [[User Interface Design]]
- [[Academic UX Principles]] - Design for research workflows
- [[Onboarding System]] - User guidance and tutorials
- [[Accessibility]] - Cross-disciplinary user support

## 🔬 Academic Integration

### [[Educational Documentation]]
- [[Pedagogical Principles]] - Learning-focused code documentation
- [[Cross-Disciplinary Support]] - Background knowledge scaffolding
- [[Research Methodology]] - Academic rigor and reproducibility

### [[Testing Framework]]
- [[Test-Driven Development]] - Red-Green-Refactor methodology
- [[Property-Based Testing]] - Mathematical invariants validation
- [[Integration Testing]] - End-to-end workflow validation

## 🚀 Getting Started

### [[Installation Guide]]
- System requirements and dependencies
- Development environment setup
- Configuration and deployment

### [[User Guides]]
- [[Faculty Guide]] - Research workflow integration
- [[Student Guide]] - Learning and exploration features
- [[Developer Guide]] - Contributing and extending the system

## 📊 Data Flow and Processing

### [[Paper Collection Pipeline]]
- [[PDF Processing]] - Text extraction and metadata parsing
- [[Source Integration]] - ArXiv, PMC, MDPI repositories
- [[Data Validation]] - Quality assurance and filtering

### [[Concept Storage]]
- [[JSON Storage Format]] - Structured concept representation
- [[Visualization Data]] - D3.js compatible data preparation
- [[Evidence Linking]] - PDF page and sentence references

## 🔧 Development Resources

### [[API Documentation]]
- Domain entity interfaces
- Use case specifications
- Service contracts

### [[Code Examples]]
- Implementation patterns
- Testing examples
- Integration samples

### [[Contributing Guidelines]]
- Code style and standards
- Review process
- Academic documentation requirements

---

## Quick Navigation
- [[Technical Architecture Overview]] - System design principles
- [[Concept Extraction Methods]] - NLP pipeline documentation
- [[Visualization Components]] - Interactive UI elements
- [[Academic Standards]] - Research-grade quality requirements
