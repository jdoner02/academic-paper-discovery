# HRV Research Development Prompts

## Project Overview
This repository contains tools and algorithms for Heart Rate Variability (HRV) analysis in traumatic brain injury research, with a focus on Apple Watch and ECG data processing.

## Key Development Prompts for GitHub Copilot

### Data Processing Prompts
- "Create a function to validate R-R intervals from Apple Watch data, removing physiologically impossible values"
- "Implement artifact detection for ECG signals using published medical algorithms"
- "Build a data quality assessment pipeline for wearable device recordings"
- "Create a standardized data structure for multi-device HRV recordings"

### HRV Analysis Prompts  
- "Calculate time-domain HRV metrics (RMSSD, pNN50, SDNN) with proper error handling"
- "Implement frequency-domain analysis using Welch's method with appropriate windowing"
- "Create Poincaré plot analysis following Brennan et al. methodology"
- "Build sample entropy calculation for non-linear HRV analysis"

### Statistical Analysis Prompts
- "Compare HRV metrics between TBI patients and controls using appropriate statistical tests"
- "Implement effect size calculations with confidence intervals for medical research"
- "Create longitudinal analysis pipeline for tracking HRV changes over time"
- "Build multiple comparison correction for HRV parameter analysis"

### Research Workflow Prompts
- "Design a reproducible analysis pipeline with full audit trail logging"
- "Create batch processing system for analyzing multiple subject datasets"
- "Implement data export functionality for statistical software (R, SPSS)"
- "Build visualization tools for research publications"

### Apple Watch Integration Prompts
- "Integrate with HealthKit to collect heart rate and HRV data"
- "Handle Apple Watch data permissions and privacy properly"
- "Create background processing for continuous HRV monitoring"
- "Validate data quality across different Apple Watch models"

### ECG Device Integration Prompts
- "Parse EDF files from clinical ECG devices with proper error handling"
- "Convert between different ECG sampling rates (250Hz, 500Hz, 1000Hz)"
- "Implement gain and offset corrections for different ECG amplifiers"
- "Create universal ECG data format for multi-device compatibility"

### Testing and Validation Prompts
- "Write property-based tests for HRV calculation algorithms"
- "Create test datasets with known HRV values for algorithm validation"
- "Implement cross-validation against established HRV analysis software"
- "Build performance benchmarks for large-scale data processing"

### Documentation Prompts
- "Generate clinical interpretation guidelines for HRV parameters"
- "Create API documentation with medical context and parameter ranges"
- "Write algorithm documentation with peer-reviewed citations"
- "Build user guides for non-technical researchers"

## Domain-Specific Context

### Medical Terminology
- R-R intervals: Time between consecutive heartbeats
- RMSSD: Root mean square of successive differences
- pNN50: Percentage of successive R-R intervals >50ms apart
- SDNN: Standard deviation of all R-R intervals
- LF/HF ratio: Low frequency to high frequency power ratio

### Research Context
- TBI: Traumatic Brain Injury
- ANS: Autonomic Nervous System
- HRV: Heart Rate Variability
- ECG: Electrocardiogram
- PPG: Photoplethysmography (Apple Watch method)

### Technical Standards
- Sampling rates: 250Hz minimum for HRV analysis
- Recording duration: 5 minutes minimum for frequency analysis
- Data quality: >80% valid intervals required
- Statistical power: Minimum 20 subjects per group recommended

## Example Usage Patterns

### When working on data validation:
```python
# Copilot will understand this context and provide medical-appropriate validation
def validate_ecg_signal(signal, sampling_rate):
    # Should implement physiological range checking
    # Should detect and flag artifacts
    # Should calculate signal quality metrics
```

### When implementing HRV calculations:
```python  
# Copilot will provide research-grade implementations
def calculate_time_domain_hrv(rr_intervals):
    # Should follow established medical algorithms
    # Should include proper error handling
    # Should validate input data ranges
```

### When creating statistical analyses:
```python
# Copilot will suggest appropriate statistical methods
def compare_hrv_groups(control_data, patient_data):
    # Should test for normality first
    # Should use appropriate statistical tests
    # Should calculate effect sizes
    # Should handle multiple comparisons
```

## Research Quality Guidelines

Always ensure:
1. **Reproducibility**: Use fixed random seeds, document all parameters
2. **Medical Accuracy**: Validate against published algorithms and normal ranges
3. **Statistical Rigor**: Use appropriate tests, report effect sizes and confidence intervals
4. **Data Quality**: Implement robust validation and quality assessment
5. **Documentation**: Include clinical context and interpretation guidelines

## Commit Message Examples

```
feat(hrv): implement RMSSD calculation following Task Force guidelines
test(ecg): add validation tests for R-peak detection accuracy
fix(apple-watch): handle edge case in HealthKit data parsing
docs(analysis): add clinical interpretation for frequency domain metrics
refactor(pipeline): extract HRV calculations into domain service
perf(processing): optimize FFT computation for large datasets
```
