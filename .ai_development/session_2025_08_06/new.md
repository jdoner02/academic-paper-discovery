# Enhanced Configuration Files and New Research Domains

Below we present improved YAML configuration files for the existing research domains, as well as additional domain configurations that align with your interests. Each updated file retains the same keys as the original (to ensure compatibility with the current system) and adds richer keywords and strategies. We also outline any necessary code adjustments to support new keyword categories.

## Updated Domain Configurations

### Cybersecurity for Water Infrastructure (Updated)

*Improvements:* We expanded this domain with two new strategies focusing on **AI-driven anomaly detection** and **digital twin simulations** for water systems security. We also refined existing keyword sets (e.g. including more ICS-specific terms and emerging threats). The configuration uses the same keys (`primary_keywords`, `secondary_keywords`, etc.) to maintain compatibility. Optional new categories like `technology_keywords` are included for clarity (and can be integrated via code changes described later).

```yaml
# Cybersecurity for Water and Wastewater Infrastructure Research
# Updated configuration for cybersecurity in water utility systems
search_configuration:
  default_strategy: "critical_infrastructure_security"
  citation_threshold: 5        # Minimum citations (was min_citation_count)
  publication_date_range:
    start_year: 2018           # Focus on recent developments
    end_year: 2025             # Up to latest research
  max_concurrent_searches: 3
  include_preprints: true
  exclude_terms: []            # (Optional global exclusions, e.g., none specified)

strategies:
  critical_infrastructure_security:
    name: "Critical Infrastructure Security"
    description: "Comprehensive cybersecurity research for water and wastewater treatment facilities"
    primary_keywords:
      - "cybersecurity"
      - "critical infrastructure"
      - "water treatment"
      - "wastewater"
    secondary_keywords:
      - "SCADA security"
      - "industrial control systems"
      - "ICS security"
      - "water infrastructure protection"
      - "utility cybersecurity"
      - "critical infrastructure protection"
    technology_keywords:
      - "PLC security"
      - "HMI vulnerabilities"
      - "industrial IoT"
      - "network segmentation"
      - "intrusion detection"
      - "anomaly detection"
    exclusion_keywords:
      - "theoretical only"
      - "purely mathematical"
    search_limit: 50
    date_range:
      start: "2020-01-01"
      end: null

  scada_water_security:
    name: "SCADA and Water Systems Security"
    description: "Security research focused on SCADA systems in water utilities"
    primary_keywords:
      - "SCADA security"
      - "industrial control systems"
      - "water utility"
    secondary_keywords:
      - "supervisory control"
      - "operational technology"
      - "OT security"
      - "process control security"
      - "industrial cybersecurity"
    technology_keywords:
      - "Modbus protocol"
      - "DNP3 security"
      - "fieldbus security"
      - "PLC vulnerabilities"
      - "control system firmware"
    exclusion_keywords:
      - "general IT security"
      - "enterprise security"
    search_limit: 40

  water_infrastructure_threats:
    name: "Water Infrastructure Threat Analysis"
    description: "Research on specific cyber threats and vulnerabilities in water systems"
    primary_keywords:
      - "water infrastructure"
      - "cybersecurity threats"
      - "vulnerability assessment"
    secondary_keywords:
      - "cyber attacks"
      - "threat modeling"
      - "risk assessment"
      - "penetration testing"
      - "red team exercises"
    application_keywords:
      - "water treatment plant"
      - "wastewater treatment"
      - "water distribution system"
      - "pumping stations"
      - "water quality monitoring"
    exclusion_keywords:
      - "physical security only"
      - "policy only"
    search_limit: 35

  iot_smart_water_security:
    name: "IoT and Smart Water Systems Security"
    description: "Security research for IoT devices and smart water management systems"
    primary_keywords:
      - "IoT security"
      - "smart water"
      - "connected devices"
    secondary_keywords:
      - "sensor network security"
      - "wireless sensor networks"
      - "smart meters"
      - "remote monitoring"
      - "edge computing"
      - "fog computing"
    technology_keywords:
      - "LoRaWAN security"
      - "Zigbee vulnerabilities"
      - "cellular IoT"
      - "satellite communication"
      - "mesh networks"
    exclusion_keywords:
      - "general IoT (consumer)"
      - "consumer IoT"
    search_limit: 30

  incident_response_water:
    name: "Water Utility Incident Response"
    description: "Cybersecurity incident response specific to water infrastructure"
    primary_keywords:
      - "incident response"
      - "cyber incident"
      - "water utility"
    secondary_keywords:
      - "disaster recovery"
      - "business continuity"
      - "crisis management"
      - "forensic analysis"
      - "malware analysis"
      - "breach response"
    application_keywords:
      - "utility operations"
      - "service restoration"
      - "emergency protocols"
      - "interagency coordination"
    exclusion_keywords:
      - "general incident response"
      - "enterprise IT"
    search_limit: 25

  ml_anomaly_detection_ics:
    name: "AI-Driven Anomaly Detection"
    description: "Machine learning approaches for intrusion and anomaly detection in water SCADA systems"
    primary_keywords:
      - "machine learning"
      - "ICS anomaly detection"
      - "SCADA cybersecurity"
    secondary_keywords:
      - "intrusion detection"
      - "behavioral modeling"
      - "neural networks"
      - "unsupervised learning"
      - "anomaly detection algorithm"
      - "cyber attack detection"
    technology_keywords:
      - "dataset generation"
      - "time-series analysis"
      - "IDS systems"
      - "deep learning models"
    exclusion_keywords:
      - "purely theoretical"
      - "non-ICS systems"
    search_limit: 40
    date_range:
      start: "2019-01-01"
      end: null

  digital_twin_water_security:
    name: "Digital Twin Simulations"
    description: "Using simulation and digital twin models for water infrastructure cybersecurity testing"
    primary_keywords:
      - "digital twin"
      - "water infrastructure"
      - "cybersecurity simulation"
    secondary_keywords:
      - "ICS testbed"
      - "cyber range"
      - "simulation model"
      - "attack simulation"
      - "industrial emulator"
    technology_keywords:
      - "virtual water treatment plant"
      - "SCADA testbed"
      - "real-time simulation"
      - "hardware-in-the-loop"
    exclusion_keywords:
      - "pure simulation with no security context"
      - "physical-only simulation"
    search_limit: 30
    date_range:
      start: "2020-01-01"
      end: null

metadata:
  domain: "Cybersecurity (Water Infrastructure)"
  description: "Cybersecurity research for water & wastewater industrial control systems"
  last_updated: "2025-08-06"
```

### Heart Rate Variability – Medical Research (Updated)

*Improvements:* We broadened this configuration by adding strategies for **advanced HRV analysis techniques**, **sports and exercise physiology**, and **HRV biofeedback for stress management**. New keywords include nonlinear metrics (entropy, fractal analysis), machine learning approaches, and domain-specific terms in sports medicine. The core structure (primary/secondary keywords, etc.) remains the same for compatibility.

```yaml
# Heart Rate Variability (HRV) Research Configuration
# Updated configuration for medical research focused on cardiac autonomic function
search_configuration:
  default_strategy: "comprehensive_hrv_research"
  citation_threshold: 5
  publication_date_range:
    start_year: 2015    # Include foundational HRV research
    end_year: 2025      # Latest developments
  max_concurrent_searches: 3
  include_preprints: true
  exclude_terms: ["animal study"]   # Globally exclude animal experiments

strategies:
  comprehensive_hrv_research:
    name: "Comprehensive HRV Research"
    description: "Broad coverage of heart rate variability research across all domains"
    primary_keywords:
      - "heart rate variability"
      - "HRV"
      - "R-R interval"
      - "RR interval"
    secondary_keywords:
      - "RMSSD"
      - "pNN50"
      - "SDNN"
      - "LF/HF ratio"
      - "frequency domain analysis"
      - "time domain analysis"
      - "Poincaré plot"
      - "autonomic function"
      - "cardiac autonomic neuropathy"
    technology_keywords:
      - "ECG"
      - "electrocardiogram"
      - "photoplethysmography"
      - "PPG"
      - "wearable devices"
      - "continuous monitoring"
      - "Apple Watch"
    exclusion_keywords:
      - "animal study"
      - "in vitro"
    search_limit: 50
    date_range:
      start: "2015-01-01"
      end: null

  tbi_focused_hrv:
    name: "TBI and HRV Research"
    description: "Heart rate variability research specifically related to traumatic brain injury"
    primary_keywords:
      - "heart rate variability"
      - "traumatic brain injury"
      - "TBI"
    secondary_keywords:
      - "concussion"
      - "brain injury"
      - "autonomic dysfunction"
      - "cardiac monitoring"
      - "rehabilitation"
      - "recovery assessment"
    clinical_keywords:
      - "biomarker"
      - "prognosis"
      - "treatment monitoring"
      - "risk stratification"
    exclusion_keywords:
      - "animal model"
      - "purely theoretical"
    search_limit: 30
    date_range:
      start: "2018-01-01"
      end: null

  wearable_hrv_technology:
    name: "Wearable HRV Technology"
    description: "HRV research using wearable devices and continuous monitoring systems"
    primary_keywords:
      - "heart rate variability"
      - "wearable devices"
      - "continuous monitoring"
    secondary_keywords:
      - "smartwatch"
      - "mobile health"
      - "mHealth"
      - "digital biomarkers"
      - "remote monitoring"
      - "ambulatory monitoring"
    technology_keywords:
      - "photoplethysmography"
      - "PPG"
      - "optical sensors"
      - "mobile applications"
      - "cloud computing"
      - "machine learning"
      - "artificial intelligence"
    exclusion_keywords:
      - "laboratory only"
      - "clinical grade only"
    search_limit: 40
    date_range:
      start: "2020-01-01"
      end: null

  clinical_hrv_applications:
    name: "Clinical HRV Applications"
    description: "HRV research focused on clinical outcomes and medical applications"
    primary_keywords:
      - "heart rate variability"
      - "clinical application"
    secondary_keywords:
      - "cardiovascular disease"
      - "diabetes"
      - "hypertension"
      - "anxiety"
      - "depression"
      - "PTSD"
      - "sleep disorders"
      - "stress assessment"
    clinical_keywords:
      - "prognosis"
      - "risk stratification"
      - "treatment monitoring"
      - "rehabilitation"
      - "biomarker"
      - "patient outcomes"
      - "sudden cardiac death"
    exclusion_keywords:
      - "healthy subjects only"
      - "validation study only"
    search_limit: 35
    date_range:
      start: "2017-01-01"
      end: null

  advanced_hrv_analysis:
    name: "Advanced HRV Analysis Techniques"
    description: "Research on machine learning and nonlinear methods for HRV analysis"
    primary_keywords:
      - "heart rate variability"
      - "HRV analysis"
      - "nonlinear analysis"
    secondary_keywords:
      - "machine learning"
      - "deep learning"
      - "entropy measures"
      - "detrended fluctuation analysis"
      - "fractal HRV"
      - "neural networks"
    technology_keywords:
      - "approximate entropy"
      - "sample entropy"
      - "Higuchi fractal dimension"
      - "Hurst exponent"
      - "SVM classification"
      - "feature extraction"
    exclusion_keywords:
      - "animal study"
      - "pure simulation"
    search_limit: 40
    date_range:
      start: "2015-01-01"
      end: null

  sports_exercise_hrv:
    name: "Sports and Exercise HRV"
    description: "HRV research in sports science and exercise physiology contexts"
    primary_keywords:
      - "heart rate variability"
      - "exercise"
      - "athlete"
    secondary_keywords:
      - "training load"
      - "sports performance"
      - "overtraining"
      - "fitness assessment"
      - "endurance athletes"
      - "recovery monitoring"
    application_keywords:
      - "athletic training"
      - "Olympic athletes"
      - "sports physiology"
      - "HRV-guided training"
    exclusion_keywords:
      - "sedentary only"
      - "non-exercise populations"
    search_limit: 30
    date_range:
      start: "2016-01-01"
      end: null

  hrv_biofeedback:
    name: "HRV Biofeedback & Stress Management"
    description: "Using heart rate variability biofeedback techniques for stress reduction and therapy"
    primary_keywords:
      - "heart rate variability"
      - "biofeedback"
    secondary_keywords:
      - "stress reduction"
      - "resonant breathing"
      - "mindfulness"
      - "anxiety intervention"
      - "vagal tone"
      - "HRV training"
    application_keywords:
      - "mental health"
      - "stress management"
      - "neurofeedback"
      - "breathing exercises"
    exclusion_keywords:
      - "pharmacological treatment"
      - "no-control trial"
    search_limit: 25
    date_range:
      start: "2010-01-01"
      end: null

metadata:
  domain: "Medical – Heart Rate Variability"
  description: "Research on heart rate variability (HRV) and its applications in health"
  last_updated: "2025-08-06"
```

### Post-Quantum Cryptography (Updated)

*Improvements:* The existing post-quantum cryptography domain was already comprehensive. We added one additional strategy to explore **blockchain and cryptocurrency applications of PQC** (bridging academic and industry concerns about quantum threats to blockchain). We also refined a few keyword lists (e.g. adding “quantum safe” synonyms and relevant terms like “CRYSTALS” in lattice strategy). The keys remain consistent with the original format.

```yaml
# Post-Quantum Cryptography Research Configuration
# Comprehensive coverage of quantum-resistant cryptographic research
search_configuration:
  default_strategy: "post_quantum_cryptography"
  citation_threshold: 3
  publication_date_range:
    start_year: 2015   # Include foundational PQC research
    end_year: 2025     # Latest developments
  max_concurrent_searches: 4
  include_preprints: true
  exclude_terms: []    # (Optional global exclusions if needed)

strategies:
  post_quantum_cryptography:
    name: "Post-Quantum Cryptography"
    description: "Comprehensive research on quantum-resistant cryptographic algorithms"
    primary_keywords:
      - "post-quantum cryptography"
      - "quantum-resistant"
      - "quantum-safe"
    secondary_keywords:
      - "lattice-based cryptography"
      - "code-based cryptography"
      - "multivariate cryptography"
      - "hash-based signatures"
      - "isogeny-based cryptography"
      - "NIST PQC"
      - "quantum cryptanalysis"
    algorithms_keywords:
      - "Kyber"
      - "Dilithium"
      - "FALCON"
      - "SPHINCS+"
      - "McEliece"
      - "NTRU"
      - "Rainbow"
    exclusion_keywords:
      - "quantum key distribution"
      - "purely theoretical"
    search_limit: 60

  lattice_based_crypto:
    name: "Lattice-Based Cryptography"
    description: "Research on lattice-based post-quantum cryptographic schemes"
    primary_keywords:
      - "lattice-based cryptography"
      - "learning with errors"
      - "LWE"
    secondary_keywords:
      - "ring learning with errors"
      - "RLWE"
      - "module learning with errors"
      - "MLWE"
      - "shortest vector problem"
      - "SVP"
      - "closest vector problem"
      - "CVP"
    algorithms_keywords:
      - "NewHope"
      - "Kyber"
      - "Dilithium"
      - "FALCON"
      - "CRYSTALS"        # Added generic CRYSTALS reference (Kyber/Dilithium family)
      - "FrodoKEM"
    exclusion_keywords:
      - "classical lattice"
      - "non-cryptographic"
    search_limit: 45

  code_based_crypto:
    name: "Code-Based Cryptography"
    description: "Error-correcting code-based post-quantum cryptography"
    primary_keywords:
      - "code-based cryptography"
      - "error correcting codes"
      - "linear codes"
    secondary_keywords:
      - "McEliece cryptosystem"
      - "Niederreiter cryptosystem"
      - "syndrome decoding"
      - "random linear codes"
      - "structured codes"
      - "LDPC codes"
      - "polar codes"
    algorithms_keywords:
      - "Classic McEliece"
      - "BIKE"
      - "HQC"
      - "LEDAcrypt"
      - "NTS-KEM"
    exclusion_keywords:
      - "classical coding theory"
      - "non-cryptographic codes"
    search_limit: 35

  multivariate_crypto:
    name: "Multivariate Cryptography"
    description: "Multivariate polynomial equation based cryptography"
    primary_keywords:
      - "multivariate cryptography"
      - "multivariate polynomials"
      - "MQ problem"
    secondary_keywords:
      - "Oil and Vinegar scheme"
      - "HFE"
      - "UOV"
      - "Rainbow signature"
      - "LUOV"
      - "GeMSS"
    algorithms_keywords:
      - "Rainbow"
      - "LUOV"
      - "GeMSS"
      - "MQDSS"
    exclusion_keywords:
      - "classical algebra"
      - "non-cryptographic"
    search_limit: 30

  hash_based_signatures:
    name: "Hash-Based Digital Signatures"
    description: "Hash function based post-quantum digital signatures"
    primary_keywords:
      - "hash-based signatures"
      - "Merkle signatures"
      - "one-time signatures"
    secondary_keywords:
      - "Lamport signatures"
      - "Winternitz signatures"
      - "WOTS"
      - "XMSS"
      - "LMS"
      - "stateful signatures"
      - "stateless signatures"
    algorithms_keywords:
      - "SPHINCS+"
      - "XMSS"
      - "LMS"
      - "WOTS+"
    exclusion_keywords:
      - "classical hash functions"
      - "non-signature applications"
    search_limit: 25

  pqc_implementations:
    name: "PQC Implementation and Performance"
    description: "Implementation aspects and performance of post-quantum algorithms"
    primary_keywords:
      - "post-quantum implementation"
      - "PQC performance"
      - "quantum-safe implementation"
    secondary_keywords:
      - "hardware implementation"
      - "software optimization"
      - "side-channel attacks"
      - "fault attacks"
      - "constant-time implementation"
      - "memory optimization"
      - "speed optimization"
    platforms_keywords:
      - "FPGA implementation"
      - "embedded systems"
      - "IoT devices"
      - "ARM processors"
      - "x86 optimization"
    exclusion_keywords:
      - "theoretical only"
      - "non-implementation"
    search_limit: 40

  pqc_standardization:
    name: "PQC Standardization and Migration"
    description: "Standardization efforts and migration to post-quantum cryptography"
    primary_keywords:
      - "PQC standardization"
      - "NIST PQC competition"
      - "quantum migration"
    secondary_keywords:
      - "cryptographic agility"
      - "hybrid systems"
      - "transition planning"
      - "protocol migration"
      - "TLS post-quantum"
      - "PKI migration"
    standards_keywords:
      - "NIST standards"
      - "IETF drafts"
      - "ISO standards"
      - "ETSI guidelines"
    exclusion_keywords:
      - "classical standardization"
      - "non-PQC standards"
    search_limit: 35

  blockchain_pqc:
    name: "PQC in Blockchain Systems"
    description: "Applying post-quantum cryptography to blockchain and cryptocurrency platforms"
    primary_keywords:
      - "post-quantum cryptography"
      - "blockchain"
    secondary_keywords:
      - "cryptocurrency"
      - "distributed ledger"
      - "quantum attack blockchain"
      - "quantum-safe consensus"
      - "digital signatures blockchain"
    application_keywords:
      - "Bitcoin quantum"
      - "Ethereum post-quantum"
      - "cryptocurrency migration"
      - "DLT security"
    exclusion_keywords:
      - "classical blockchain only"
      - "non-cryptographic blockchain"
    search_limit: 30

metadata:
  domain: "Post-Quantum Cryptography"
  description: "Quantum-resistant cryptographic algorithms and their applications"
  last_updated: "2025-08-06"
```

## Additional Domain Configurations

Based on your interests and the intersection of academic and applied research, we have created new domain configuration files. These domains address areas where **open research questions** and **practical impact** are prominent.

### AI-Driven Cybersecurity (New Domain)

This domain covers the use of machine learning and AI in cybersecurity. Strategies include intrusion detection systems, malware analysis, adversarial ML, and threat intelligence – all relevant for bridging cutting-edge research with real-world security challenges.

```yaml
# AI-Driven Cybersecurity Research Configuration
# Applications of machine learning and artificial intelligence in cybersecurity
search_configuration:
  default_strategy: "ml_intrusion_detection"
  citation_threshold: 0
  publication_date_range:
    start_year: 2016   # Rapid growth of AI in security around mid-2010s
    end_year: 2025
  max_concurrent_searches: 3
  include_preprints: true
  exclude_terms: []

strategies:
  ml_intrusion_detection:
    name: "ML for Intrusion Detection"
    description: "Machine learning approaches for intrusion detection and network anomaly detection"
    primary_keywords:
      - "intrusion detection"
      - "machine learning"
    secondary_keywords:
      - "anomaly detection"
      - "network traffic analysis"
      - "IDS"
      - "cyber attack detection"
      - "deep learning"
      - "cybersecurity AI"
    technology_keywords:
      - "neural network"
      - "unsupervised learning"
      - "clustering algorithms"
      - "feature selection"
    exclusion_keywords:
      - "purely theoretical"
      - "outdated signature-based only"
    search_limit: 50

  ml_malware_analysis:
    name: "Malware Analysis & Classification"
    description: "Using AI/ML for malware detection, classification, and analysis"
    primary_keywords:
      - "malware detection"
      - "machine learning"
    secondary_keywords:
      - "malware classification"
      - "malware analysis"
      - "ransomware detection"
      - "binary classification"
      - "deep learning malware"
      - "behavior analysis"
    technology_keywords:
      - "sandbox analysis"
      - "dynamic analysis"
      - "static analysis"
      - "graph neural networks"
    exclusion_keywords:
      - "signature-only detection"
      - "antivirus product focus"
    search_limit: 50

  adversarial_ml_security:
    name: "Adversarial Machine Learning"
    description: "Research on adversarial attacks against ML models and defenses in security contexts"
    primary_keywords:
      - "adversarial machine learning"
    secondary_keywords:
      - "adversarial examples"
      - "evasion attacks"
      - "model poisoning"
      - "backdoor attacks"
      - "robust machine learning"
      - "secure AI"
    technology_keywords:
      - "model robustness"
      - "defense mechanisms"
      - "adversarial training"
      - "FGSM"
      - "PGD attack"
    exclusion_keywords:
      - "adversarial images only"    # exclude papers only about CV adversarial attacks
      - "non-security contexts"
    search_limit: 40

  ai_threat_intelligence:
    name: "AI for Threat Intelligence"
    description: "Using AI to automate threat intelligence, phishing detection, and cybersecurity analytics"
    primary_keywords:
      - "threat intelligence"
      - "machine learning"
    secondary_keywords:
      - "phishing detection"
      - "social engineering detection"
      - "cyber threat analysis"
      - "NLP security"
      - "security analytics"
    technology_keywords:
      - "natural language processing"
      - "clustering threats"
      - "automated analysis"
      - "SIEM optimization"
    exclusion_keywords:
      - "manual threat intelligence"
      - "non-AI methods only"
    search_limit: 45

metadata:
  domain: "AI in Cybersecurity"
  description: "Machine learning and artificial intelligence techniques applied to cybersecurity"
  last_updated: "2025-08-06"
```

### AI in Healthcare (New Domain)

This domain focuses on machine learning applications in healthcare and medicine. Strategies span medical imaging, clinical NLP, wearable sensors, drug discovery, and precision medicine. These areas are rich with academic research and have clear industry applications, aligning with a goal of impactful, hands-on contributions.

```yaml
# AI in Healthcare Research Configuration
# Machine learning and AI applications in medicine and healthcare
search_configuration:
  default_strategy: "medical_imaging_ai"
  citation_threshold: 0
  publication_date_range:
    start_year: 2015    # Deep learning surge in healthcare around mid-2010s
    end_year: 2025
  max_concurrent_searches: 3
  include_preprints: true
  exclude_terms: []

strategies:
  medical_imaging_ai:
    name: "Medical Imaging AI"
    description: "Deep learning for medical imaging (radiology, pathology) diagnostics"
    primary_keywords:
      - "medical imaging"
      - "deep learning"
    secondary_keywords:
      - "radiology AI"
      - "image segmentation"
      - "cancer detection"
      - "MRI analysis"
      - "CT scan diagnosis"
      - "medical image classification"
    method_keywords:
      - "convolutional neural network"
      - "CNN"
      - "computer-aided diagnosis"
      - "radiomics"
    exclusion_keywords:
      - "no-image data"
      - "theoretical only"
    search_limit: 50

  clinical_nlp:
    name: "Clinical Natural Language Processing"
    description: "NLP applied to clinical text (electronic health records, medical literature)"
    primary_keywords:
      - "clinical NLP"
      - "healthcare text mining"
    secondary_keywords:
      - "electronic health records"
      - "EHR data"
      - "clinical notes analysis"
      - "medical text mining"
      - "named entity recognition medical"
      - "patient data NLP"
    method_keywords:
      - "language model"
      - "transformer model"
      - "BERT in healthcare"
      - "de-identification"
    exclusion_keywords:
      - "non-clinical text"
      - "language analysis not related to health"
    search_limit: 45

  wearable_health_monitoring:
    name: "Wearable & Sensor Health Monitoring"
    description: "Using wearables and IoT sensor data with AI for health monitoring"
    primary_keywords:
      - "wearable health"
      - "remote patient monitoring"
    secondary_keywords:
      - "digital health"
      - "digital biomarkers"
      - "mobile health"
      - "sensor data analytics"
      - "health monitoring"
      - "physiological signal analysis"
    technology_keywords:
      - "wearable devices"
      - "smartwatch data"
      - "IoT healthcare"
      - "continuous monitoring"
    exclusion_keywords:
      - "no AI analysis"
      - "in-clinic monitoring only"
    search_limit: 50

  ai_drug_discovery:
    name: "AI in Drug Discovery"
    description: "Applying AI for drug discovery, drug design, and pharmacological research"
    primary_keywords:
      - "drug discovery"
      - "machine learning"
    secondary_keywords:
      - "drug design"
      - "molecule generation"
      - "virtual screening"
      - "pharmacology AI"
      - "drug repurposing"
      - "generative chemistry"
    method_keywords:
      - "reinforcement learning"
      - "graph neural network"
      - "molecular docking"
      - "QSAR modeling"
    exclusion_keywords:
      - "purely wet-lab studies"
      - "no AI technique"
    search_limit: 40

  precision_medicine_ai:
    name: "AI in Precision Medicine"
    description: "Machine learning for personalized medicine and predictive healthcare"
    primary_keywords:
      - "precision medicine"
      - "machine learning"
    secondary_keywords:
      - "personalized treatment"
      - "genomic analysis"
      - "health risk prediction"
      - "predictive modeling healthcare"
      - "genomics AI"
      - "electronic health records"
    method_keywords:
      - "predictive model"
      - "genomic data"
      - "risk stratification"
      - "polygenic risk score"
    exclusion_keywords:
      - "population-level only"
      - "no personalization"
    search_limit: 35

metadata:
  domain: "AI in Healthcare"
  description: "Artificial intelligence and machine learning in medicine, health, and biotech"
  last_updated: "2025-08-06"
```

### Quantum Computing (New Domain)

This domain targets general quantum computing research beyond cryptography. It includes quantum algorithms, hardware, error correction, quantum machine learning, and quantum communication (including QKD). These strategies will capture a wide range of academic work in quantum computing, which is relevant for staying ahead in emerging tech.

```yaml
# Quantum Computing Research Configuration
# Research on quantum algorithms, hardware, error correction, and communication
search_configuration:
  default_strategy: "quantum_algorithms"
  citation_threshold: 0
  publication_date_range:
    start_year: 2010   # Include early foundational papers in the 2010s
    end_year: 2025
  max_concurrent_searches: 3
  include_preprints: true
  exclude_terms: []

strategies:
  quantum_algorithms:
    name: "Quantum Algorithms"
    description: "Research into algorithms exploiting quantum computation for speedups"
    primary_keywords:
      - "quantum algorithm"
    secondary_keywords:
      - "Shor's algorithm"
      - "Grover's algorithm"
      - "quantum speedup"
      - "quantum search algorithm"
      - "variational quantum algorithm"
      - "quantum complexity"
    application_keywords:
      - "quantum simulation"
      - "optimization problems"
      - "quantum supremacy"
      - "quantum Fourier transform"
    exclusion_keywords:
      - "classical algorithms"
      - "no quantum advantage"
    search_limit: 50

  quantum_hardware:
    name: "Quantum Hardware Technologies"
    description: "Advancements in quantum computing hardware and qubit technologies"
    primary_keywords:
      - "quantum computing hardware"
      - "qubit technology"
    secondary_keywords:
      - "superconducting qubits"
      - "ion trap"
      - "photonic qubits"
      - "quantum processor"
      - "quantum circuit"
      - "quantum computer architecture"
    technology_keywords:
      - "decoherence"
      - "qubit coherence time"
      - "quantum error rates"
      - "scalability"
    exclusion_keywords:
      - "classical hardware"
      - "theoretical algorithm only"
    search_limit: 50

  quantum_error_correction:
    name: "Quantum Error Correction"
    description: "Techniques for error correction and fault tolerance in quantum computers"
    primary_keywords:
      - "quantum error correction"
    secondary_keywords:
      - "error correcting codes"
      - "fault-tolerant quantum computing"
      - "surface code"
      - "stabilizer code"
      - "error mitigation"
      - "quantum fault tolerance"
    technology_keywords:
      - "logical qubit"
      - "error threshold"
      - "quantum decoherence"
      - "syndrome measurement"
    exclusion_keywords:
      - "no error correction"
      - "classical error correction only"
    search_limit: 40

  quantum_machine_learning:
    name: "Quantum Machine Learning"
    description: "Intersection of quantum computing and machine learning algorithms"
    primary_keywords:
      - "quantum machine learning"
    secondary_keywords:
      - "quantum neural network"
      - "quantum support vector machine"
      - "variational quantum circuit"
      - "quantum data"
      - "QAOA"
      - "quantum optimization"
    technology_keywords:
      - "hybrid quantum-classical"
      - "VQE (variational eigensolver)"
      - "quantum kernel methods"
      - "quantum classification"
    exclusion_keywords:
      - "classical ML only"
      - "no quantum component"
    search_limit: 35

  quantum_communication:
    name: "Quantum Communication & QKD"
    description: "Quantum communication protocols, quantum networks, and key distribution"
    primary_keywords:
      - "quantum communication"
    secondary_keywords:
      - "quantum key distribution"
      - "quantum network"
      - "quantum teleportation"
      - "quantum internet"
      - "entanglement distribution"
      - "quantum repeater"
    technology_keywords:
      - "QKD protocols"
      - "quantum encryption"
      - "entangled photons"
      - "quantum network security"
    exclusion_keywords:
      - "classical communication"
      - "post-quantum (classical) only"
    search_limit: 45

metadata:
  domain: "Quantum Computing"
  description: "Quantum computing research: algorithms, hardware, error correction, and communication"
  last_updated: "2025-08-06"
```

## Adapting the System for New Keys (Recommended Changes)

The above configurations introduce additional keyword categories such as `technology_keywords`, `application_keywords`, `method_keywords`, etc., which were present in the original files but not fully utilized by the code. To **ensure the best results**, the system’s code can be updated to incorporate these new fields:

* **Extend Keyword Parsing:** In the `KeywordConfig.from_yaml_file` loader, gather all `*keywords` lists (beyond just primary and secondary) when constructing a `SearchStrategy`. For example, combine `technology_keywords`, `application_keywords`, `clinical_keywords`, etc., into the secondary terms so they contribute to search queries. This could be done by modifying the loop in **`keyword_config.py`** to merge any additional lists into the `secondary_keywords` before creating the `SearchStrategy` object. (Alternatively, the `SearchStrategy` dataclass could be extended with optional fields for these categories, but merging is simpler.)

* **Update Query Building:** In `SearchStrategy.build_search_query()`, include the extra keywords in the OR portion of the query. If we merged them into secondary keywords at load time, this happens automatically. Otherwise, adjust the method to incorporate something like:

  ```python
  all_optional_terms = self.secondary_keywords.copy()  
  all_optional_terms.extend(getattr(self, "technology_keywords", []))  
  # (and similarly for other categories)
  ```

  Then use `all_optional_terms` in the OR clause of the query string construction. This way, terms like specific technologies or applications will be considered in searches.

* **Search Configuration Keys:** We aligned the YAML keys with the code’s expected names. For instance, `min_citation_count` was replaced with `citation_threshold`, and `year_range` with `publication_date_range` (`start_year`, `end_year`). If the codebase still uses the old names, either update the YAML (as we did above) or modify **`SearchConfiguration`** parsing to accept the old keys. The better approach is what we’ve done: use the keys the code expects (per tests), so the system will correctly apply the year range and citation filters.

* **Metadata Usage:** We added a `metadata` section in each YAML with a domain name and description. The current CLI doesn’t use this, but the web interface or future features might. To use it, the system could be extended to read `config_data["metadata"]` for display purposes (e.g., showing a friendly domain title instead of file name). This would involve minimal changes in how domain names are listed (e.g., use `metadata.domain` if available instead of deriving from filename).

By implementing the above changes, the **existing system** will continue to work with the improved configurations and will take advantage of the richer keyword sets. The core functionality remains the same, but these tweaks will broaden the search queries to yield more comprehensive results. The recommended code adjustments are modest and maintain backward compatibility with simpler configs:

* Modify `KeywordConfig.from_yaml_file` to merge new keyword lists into `secondary_keywords` or extend `SearchStrategy` initialization to include them.
* Ensure `SearchQuery` construction uses the merged keyword list so that all relevant terms (primary + others) are included in the query logic.
* Optionally, update menu display to utilize `metadata` for user-friendly domain names.

By following these recommendations, the system will harness the full power of the enhanced YAML configurations and better support your academic paper discovery goals. Each domain is now packed with targeted keywords and strategies to uncover a wide range of relevant literature, helping you identify open research areas and practical contributions at the intersection of academia and industry.
