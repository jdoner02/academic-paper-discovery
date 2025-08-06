# 🚀 Research Paper Aggregator - Quick Start Guide

## Instant Setup (2 Minutes)

### 1. Clone and Install
```bash
git clone https://github.com/jessicadoner/research-paper-aggregator.git
cd research-paper-aggregator
pip install -e .
```

### 2. Launch Interactive Menu
```bash
python3 main.py
```

## 🎯 What You'll See

### Main Menu
```
======================================================================
🔍📚 RESEARCH PAPER AGGREGATOR
======================================================================
🎯 Intelligent Academic Research Discovery System
🏗️  Clean Architecture • 🤖 arXiv Integration • 📥 Auto-Download
======================================================================
📂 Available Research Domains:
--------------------------------------------------
  1. Cybersecurity Water Infrastructure
  2. Search Keywords (Medical/HRV Research)  
  3. Post Quantum Cryptography
  0. Exit
--------------------------------------------------
🎯 Select research domain (number):
```

### Domain Strategy Menu
After selecting a domain, you'll see available research strategies:
```
🔐 Post Quantum Cryptography Research Strategies:
--------------------------------------------------
  1. Lattice Cryptography
  2. Code Based Cryptography
  3. NIST Standards
  4. Quantum Resistant Protocols
  0. Back to main menu
--------------------------------------------------
```

### Action Menu
Choose what to do with the search results:
```
📋 Available Actions:
--------------------------------------------------
  1. 🔍 Preview papers (display results)
  2. 📥 Download papers (PDF + metadata)
  3. 🎯 Custom search (your own terms)
  0. Back to strategies
--------------------------------------------------
```

## 🔧 Advanced Usage

### Command Line Interface (Optional)
```bash
# Use PYTHONPATH for module imports
PYTHONPATH=src python3 search_research.py --strategy lattice_cryptography --limit 5

# Custom search terms
PYTHONPATH=src python3 search_research.py --custom "quantum computing" "security"
```

### Adding New Domains
1. Create `config/your_domain.yaml`:
```yaml
strategies:
  your_strategy:
    base_terms: ["primary", "concepts"]
    domain_terms: ["specific", "applications"] 
    method_terms: ["research", "methods"]
    exclusion_terms: ["exclude", "these"]

metadata:
  domain: "Your Research Domain"
  description: "Domain description"
  last_updated: "2024-01-15"
```

2. Restart `python3 main.py` - it will auto-discover your domain!

## 🎉 That's It!

You now have a powerful research aggregation system with:
- ✅ Interactive menu interface
- ✅ Multi-domain support (cybersecurity, cryptography, medical)
- ✅ Automated arXiv paper discovery
- ✅ PDF download with organized folders
- ✅ Extensible configuration system
- ✅ Clean Architecture implementation

Perfect for busy researchers who want "one-click" paper discovery! 🚀