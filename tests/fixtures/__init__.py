"""
Test Fixtures - Shared test data and utilities for comprehensive testing.

This module provides reusable test data, mock responses, and utility functions
that support unit, integration, end-to-end, and contract testing. Fixtures
ensure consistent test data across all test types while avoiding duplication.

Educational Notes:
- Fixtures provide controlled, repeatable test data
- Centralized test data management improves maintainability
- Real-world-like data helps validate actual usage scenarios
- Proper fixtures enable comprehensive integration testing

Testing Philosophy:
- Use realistic data that mirrors actual research scenarios
- Provide both minimal and comprehensive data sets
- Include edge cases and error scenarios
- Ensure data is deterministic for reliable testing

Fixture Categories:
- Sample research papers with various metadata completeness
- Mock API responses from arXiv and other sources
- Configuration files for different research domains
- File system structures for download testing
- Network response scenarios (success, failure, timeout)
"""

from datetime import datetime, timezone
from typing import Dict, List, Any
from pathlib import Path
import json

# Sample research papers for testing
SAMPLE_PAPERS = [
    {
        "title": "Deep Learning Approaches for Cybersecurity Threat Detection",
        "authors": ["Dr. Alice Johnson", "Prof. Bob Smith"],
        "abstract": "This paper presents novel deep learning approaches for detecting cybersecurity threats in network traffic. We propose a convolutional neural network architecture that achieves 95% accuracy in threat classification.",
        "publication_date": datetime(2023, 6, 15, tzinfo=timezone.utc),
        "doi": "10.1000/cybersec.2023.001",
        "arxiv_id": "2306.12345",
        "venue": "IEEE Cybersecurity Conference",
        "citation_count": 42,
        "keywords": ["cybersecurity", "deep learning", "threat detection"],
    },
    {
        "title": "Quantum-Resistant Cryptographic Protocols",
        "authors": ["Dr. Carol Zhang"],
        "abstract": "An analysis of post-quantum cryptographic protocols and their implementation challenges in modern distributed systems.",
        "publication_date": datetime(2023, 8, 22, tzinfo=timezone.utc),
        "doi": "10.1000/quantum.2023.002",
        "arxiv_id": "2308.67890",
        "venue": "Journal of Quantum Computing",
        "citation_count": 28,
        "keywords": ["quantum cryptography", "post-quantum", "protocols"],
    },
    {
        "title": "Machine Learning for Network Intrusion Detection",
        "authors": ["Prof. David Lee", "Dr. Emma Wilson"],
        "abstract": "Comparative study of machine learning algorithms for network intrusion detection systems, focusing on real-time performance and accuracy.",
        "publication_date": datetime(2023, 4, 10, tzinfo=timezone.utc),
        "doi": "10.1000/intrusion.2023.003",
        "venue": "ACM Security Symposium",
        "citation_count": 67,
        "keywords": ["machine learning", "intrusion detection", "networks"],
    },
]

# Mock arXiv API responses
MOCK_ARXIV_RESPONSES = {
    "successful_search": {
        "feed": {
            "entry": [
                {
                    "id": "http://arxiv.org/abs/2306.12345v1",
                    "title": "Deep Learning Approaches for Cybersecurity Threat Detection",
                    "summary": "This paper presents novel deep learning approaches...",
                    "author": [{"name": "Alice Johnson"}, {"name": "Bob Smith"}],
                    "published": "2023-06-15T00:00:00Z",
                    "links": [
                        {
                            "rel": "alternate",
                            "href": "http://arxiv.org/abs/2306.12345v1",
                        },
                        {
                            "rel": "related",
                            "href": "http://arxiv.org/pdf/2306.12345v1.pdf",
                            "type": "application/pdf",
                        },
                    ],
                }
            ]
        }
    },
    "empty_results": {"feed": {"entry": []}},
    "network_error": "ConnectionError: Network timeout",
}

# Sample configuration files
SAMPLE_CONFIGS = {
    "cybersecurity": {
        "search_configuration": {
            "min_citation_threshold": 5,
            "publication_year_start": 2020,
            "publication_year_end": 2024,
            "max_concurrent_searches": 3,
            "default_strategy": "comprehensive_cybersecurity",
        },
        "strategies": {
            "comprehensive_cybersecurity": {
                "name": "comprehensive_cybersecurity",
                "description": "Comprehensive cybersecurity research covering multiple domains",
                "primary_keywords": [
                    "cybersecurity",
                    "network security",
                    "information security",
                ],
                "secondary_keywords": [
                    "threat detection",
                    "vulnerability assessment",
                    "security protocols",
                ],
                "exclusion_keywords": ["tutorial", "survey only"],
                "search_limit": 100,
            }
        },
    }
}


def create_temp_config_file(config_data: Dict[str, Any], temp_dir: Path) -> Path:
    """
    Create a temporary configuration file for testing.

    Educational Note:
    This utility function demonstrates how to create temporary test files
    that can be safely used in tests without cluttering the file system.
    """
    import yaml

    config_file = temp_dir / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    return config_file


def create_mock_pdf_content() -> bytes:
    """Generate mock PDF content for download testing."""
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n..."


# Network scenarios for testing
NETWORK_SCENARIOS = {
    "success": {"status_code": 200, "content": create_mock_pdf_content()},
    "not_found": {"status_code": 404, "content": b"Not Found"},
    "server_error": {"status_code": 500, "content": b"Internal Server Error"},
    "timeout": {"exception": "requests.exceptions.Timeout"},
    "connection_error": {"exception": "requests.exceptions.ConnectionError"},
}
