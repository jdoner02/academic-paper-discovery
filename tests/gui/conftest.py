"""
Pytest Configuration and Test Utilities for GUI Testing

This module provides test configuration, fixtures, and utilities for comprehensive
GUI testing following Test-Driven Development principles.

Educational Notes:
- Demonstrates pytest configuration for web application testing
- Shows test fixture patterns for Flask application testing
- Provides utilities for integration testing and mock management
- Establishes patterns for Clean Architecture testing compliance

Testing Framework:
- pytest: Main testing framework with advanced fixture support
- Flask-Testing: Specialized Flask application testing utilities
- Mock/Patch: Isolation testing and dependency mocking
- Coverage: Test coverage measurement and reporting

Test Organization:
- Unit Tests: Individual component testing with mocks
- Integration Tests: Cross-layer interaction testing
- Contract Tests: Interface compliance validation
- UI/UX Tests: User interface and experience validation
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add gui directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../gui"))
import sys

# Add src to path for Clean Architecture imports
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def project_root_path():
    """
    Project root path fixture for accessing project files.

    Educational Note:
    Session-scoped fixtures provide shared resources across all tests,
    improving test performance and consistency.
    """
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def gui_path(project_root_path):
    """
    GUI directory path fixture for accessing GUI components.

    Educational Note:
    Path fixtures ensure consistent file access across tests
    and handle path resolution differences across environments.
    """
    return project_root_path / "gui"


@pytest.fixture
def temp_directory():
    """
    Temporary directory fixture for test file operations.

    Educational Note:
    Temporary directories provide isolated test environments
    and ensure tests don't interfere with actual project files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_clean_architecture_components():
    """
    Mock Clean Architecture components for testing.

    Educational Note:
    Mock fixtures enable testing web layer in isolation,
    following Clean Architecture dependency inversion principles.
    """
    mock_search_use_case = Mock()
    mock_concept_extraction_use_case = Mock()

    # Configure mock return values for realistic testing
    mock_search_use_case.execute.return_value = {
        "papers": [],
        "total_count": 0,
        "search_metadata": {"query": "test", "filters": {}},
    }

    mock_concept_extraction_use_case.execute.return_value = {
        "concepts": [],
        "hierarchy": {},
        "extraction_metadata": {"source": "test", "timestamp": "2024-01-01"},
    }

    return {
        "search_use_case": mock_search_use_case,
        "concept_extraction_use_case": mock_concept_extraction_use_case,
    }


@pytest.fixture
def flask_app_config():
    """
    Flask application configuration for testing.

    Educational Note:
    Test configuration ensures proper Flask testing environment
    with appropriate settings for web layer validation.
    """
    return {
        "TESTING": True,
        "SECRET_KEY": "test-secret-key-for-academic-research",
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for easier testing
        "DEBUG": False,  # Disable debug mode in tests
    }


class TestConfigurationManager:
    """
    Test configuration management utilities.

    Educational Notes:
    - Provides centralized test configuration management
    - Ensures consistent test environment setup
    - Handles test-specific configuration overrides
    """

    @staticmethod
    def get_test_config():
        """Get standard test configuration."""
        return {
            "testing_mode": True,
            "mock_external_services": True,
            "test_data_path": Path(__file__).parent / "fixtures",
            "coverage_threshold": 90,
        }

    @staticmethod
    def setup_test_environment():
        """Set up test environment variables and paths."""
        os.environ["TESTING"] = "true"
        os.environ["FLASK_ENV"] = "testing"

        # Ensure test directories exist
        test_fixtures_dir = Path(__file__).parent / "fixtures"
        test_fixtures_dir.mkdir(exist_ok=True)


class MockDataFactory:
    """
    Factory for creating mock data for testing.

    Educational Notes:
    - Demonstrates Factory pattern for test data creation
    - Provides realistic test data for academic research scenarios
    - Ensures consistent test data across different test modules
    """

    @staticmethod
    def create_mock_research_paper():
        """Create mock research paper data."""
        return {
            "id": "test-paper-001",
            "title": "Advanced Heart Rate Variability Analysis in TBI Research",
            "authors": ["Dr. Jane Smith", "Dr. John Doe"],
            "abstract": "This paper explores HRV analysis techniques...",
            "doi": "10.1234/test.2024.001",
            "publication_date": "2024-01-15",
            "keywords": ["HRV", "TBI", "analysis"],
            "source": "test_source",
        }

    @staticmethod
    def create_mock_concept_hierarchy():
        """Create mock concept hierarchy data."""
        return {
            "id": "hrv_analysis",
            "name": "Heart Rate Variability Analysis",
            "type": "research_domain",
            "children": [
                {
                    "id": "time_domain",
                    "name": "Time Domain Analysis",
                    "type": "analysis_method",
                    "children": [],
                },
                {
                    "id": "frequency_domain",
                    "name": "Frequency Domain Analysis",
                    "type": "analysis_method",
                    "children": [],
                },
            ],
        }

    @staticmethod
    def create_mock_search_results():
        """Create mock search results data."""
        return {
            "papers": [MockDataFactory.create_mock_research_paper()],
            "total_count": 1,
            "search_metadata": {
                "query": "HRV analysis",
                "filters": {"date_range": "2024", "source": "all"},
                "execution_time": 0.125,
            },
        }


# Test markers for organizing test execution
pytest_markers = [
    "unit: Individual component tests",
    "integration: Cross-component interaction tests",
    "ui: User interface and experience tests",
    "performance: Performance and optimization tests",
    "accessibility: Accessibility compliance tests",
    "contract: Interface contract validation tests",
]


# Configure pytest markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    for marker in pytest_markers:
        config.addinivalue_line("markers", marker)


# Test collection and organization helpers
def pytest_collection_modifyitems(config, items):
    """Modify test collection for better organization."""
    # Add markers based on test file names and paths
    for item in items:
        # Mark tests based on file location
        if "test_flask_app" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_javascript" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        elif "test_templates_css" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        elif "test_services" in item.nodeid:
            item.add_marker(pytest.mark.unit)

        # Mark accessibility tests
        if "accessibility" in item.name.lower():
            item.add_marker(pytest.mark.accessibility)

        # Mark performance tests
        if "performance" in item.name.lower() or "optimization" in item.name.lower():
            item.add_marker(pytest.mark.performance)


@pytest.fixture
def client():
    """
    Create test client for GUI Flask application.

    Educational Note:
    This fixture provides a test client that can make HTTP requests
    to our Flask application without running a full server.
    """
    from app import create_app

    app = create_app({"TESTING": True})

    with app.test_client() as client:
        with app.app_context():
            yield client
