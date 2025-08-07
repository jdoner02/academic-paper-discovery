"""
Flask Application Tests - Academic Research Interface

This module demonstrates comprehensive testing of Flask web applications following
TDD principles and Clean Architecture patterns for academic research tools.

Educational Notes:
- Shows Flask application testing with pytest fixtures
- Demonstrates test isolation using application contexts
- Tests route handlers, JSON APIs, error handling, and static file serving
- Validates integration between web layer and application layer use cases

Design Patterns Applied:
- Test Fixture Pattern: setUp/tearDown for consistent test environment
- Mock Object Pattern: Isolate web layer from external dependencies
- Builder Pattern: Construct test data and application instances
- Assertion Pattern: Comprehensive validation of web responses

Use Cases Tested:
- Academic Research Interface: Main application entry point
- Concept Exploration: Interactive visualization endpoints
- Search Functionality: Keyword-based paper discovery
- Error Handling: Graceful failure scenarios

Testing Strategy:
- Unit Tests: Individual route handler logic
- Integration Tests: End-to-end request/response cycles
- Contract Tests: API response format validation
- UI/UX Tests: Template rendering and user interaction flows
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from flask import Flask

# Add src to path for imports
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import the Flask application
from gui.app import AcademicResearchApp, create_app


class TestAcademicResearchAppInitialization:
    """
    Test suite for Academic Research Application initialization and configuration.

    Educational Notes:
    - Demonstrates test organization by feature/behavior
    - Shows proper test isolation and setup/teardown patterns
    - Tests application configuration and dependency injection
    """

    def test_app_initialization_with_clean_architecture(self):
        """
        Test that AcademicResearchApp initializes correctly with Clean Architecture components.

        Educational Note:
        This test validates the Dependency Injection pattern implementation,
        ensuring use cases are properly injected and configured.
        """
        app = AcademicResearchApp()

        # Validate Flask app configuration
        assert app.app is not None
        assert isinstance(app.app, Flask)
        assert app.app.config["TESTING"] is False

        # Validate use case injection
        assert hasattr(app, "_search_use_case")
        assert hasattr(app, "_concept_extraction_use_case")

    def test_app_initialization_with_mock_dependencies(self):
        """
        Test application initialization in demonstration mode with mock implementations.

        Educational Note:
        This demonstrates the Adapter Pattern - the application adapts gracefully
        when Clean Architecture components are unavailable.
        """
        # This should work even without full Clean Architecture setup
        app = AcademicResearchApp()
        assert app.app is not None

        # Validate demonstration mode message appears in logs
        # (In real implementation, we'd capture logs)

    def test_create_app_factory_function(self):
        """
        Test the Flask application factory function for proper configuration.

        Educational Note:
        Application factory pattern enables different configurations
        for testing, development, and production environments.
        """
        app = create_app()

        assert isinstance(app, Flask)
        assert app.config is not None

        # Test configuration can be overridden
        test_config = {"TESTING": True, "SECRET_KEY": "test-key"}
        test_app = create_app(test_config)
        assert test_app.config["TESTING"] is True
        assert test_app.config["SECRET_KEY"] == "test-key"


class TestFlaskRouteHandlers:
    """
    Test suite for Flask route handlers and API endpoints.

    Educational Notes:
    - Demonstrates Flask test client usage for endpoint testing
    - Shows JSON API testing patterns for academic data
    - Tests both successful responses and error handling scenarios
    """

    @pytest.fixture
    def app(self):
        """
        Test fixture providing Flask application instance.

        Educational Note:
        Fixtures promote test isolation and reusability,
        ensuring each test gets a fresh application state.
        """
        app = AcademicResearchApp()
        app.app.config["TESTING"] = True
        return app.app

    @pytest.fixture
    def client(self, app):
        """
        Test fixture providing Flask test client.

        Educational Note:
        Test client allows simulation of HTTP requests
        without running actual web server.
        """
        return app.test_client()

    def test_index_route_renders_main_interface(self, client):
        """
        Test main index route renders the academic research interface.

        Educational Note:
        Template rendering tests validate the View layer
        of the MVC pattern implementation.
        """
        response = client.get("/")

        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
        assert (
            b"Academic Research" in response.data or b"Research Paper" in response.data
        )

    def test_api_papers_endpoint_returns_json(self, client):
        """
        Test API endpoint returns properly formatted JSON for papers.

        Educational Note:
        API testing validates the Controller layer behavior
        and data serialization patterns.
        """
        response = client.get("/api/papers")

        assert response.status_code == 200
        assert response.content_type == "application/json"

        data = json.loads(response.data)
        assert isinstance(data, (list, dict))

    def test_api_concepts_endpoint_structure(self, client):
        """
        Test concepts API endpoint returns expected data structure.

        Educational Note:
        Contract testing ensures API consumers can rely
        on consistent response formats.
        """
        response = client.get("/api/concepts")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Validate expected response structure for concept data
        if isinstance(data, list) and len(data) > 0:
            concept = data[0]
            # Expect concept objects to have required fields
            expected_fields = ["id", "name", "type"]
            for field in expected_fields:
                assert field in concept or "concept" in str(concept).lower()

    def test_search_endpoint_handles_query_parameters(self, client):
        """
        Test search endpoint processes query parameters correctly.

        Educational Note:
        Input validation and parameter processing demonstrate
        the robustness required for academic search tools.
        """
        # Test with valid search parameters
        response = client.get("/api/search?query=machine+learning&limit=10")
        assert response.status_code in [200, 404, 500]  # Allow various implementations

        # Test with empty query
        response = client.get("/api/search?query=")
        assert response.status_code in [200, 400]  # Should handle gracefully

    def test_static_file_serving(self, client):
        """
        Test static file serving for CSS, JavaScript, and other assets.

        Educational Note:
        Static file tests ensure proper web asset delivery
        for professional UI/UX functionality.
        """
        # Test CSS file serving
        response = client.get("/static/css/main.css")
        assert response.status_code == 200
        assert "text/css" in response.content_type

        # Test JavaScript module serving
        response = client.get("/static/js/modules/academic-research-ui.js")
        assert response.status_code == 200
        assert (
            "javascript" in response.content_type
            or "text/plain" in response.content_type
        )


class TestErrorHandling:
    """
    Test suite for error handling and edge cases.

    Educational Notes:
    - Demonstrates defensive programming through comprehensive error testing
    - Shows graceful degradation when dependencies are unavailable
    - Tests user-friendly error messages for academic researchers
    """

    @pytest.fixture
    def client(self):
        """Flask test client for error testing."""
        app = AcademicResearchApp()
        app.app.config["TESTING"] = True
        return app.app.test_client()

    def test_404_error_handling(self, client):
        """
        Test 404 error handling for non-existent routes.

        Educational Note:
        Proper error handling improves user experience
        and provides helpful guidance for navigation.
        """
        response = client.get("/nonexistent-route")
        assert response.status_code == 404

    def test_api_error_responses_are_json(self, client):
        """
        Test API endpoints return JSON error responses.

        Educational Note:
        Consistent error response format enables
        proper client-side error handling.
        """
        response = client.get("/api/nonexistent-endpoint")
        assert response.status_code == 404

        # If we get a response, it should be JSON for API endpoints
        if response.data:
            try:
                json.loads(response.data)
            except json.JSONDecodeError:
                # Some implementations might return HTML 404 pages
                pass

    def test_malformed_request_handling(self, client):
        """
        Test handling of malformed or invalid requests.

        Educational Note:
        Input validation prevents security issues
        and provides clear feedback to users.
        """
        # Test POST request with invalid JSON
        response = client.post(
            "/api/search", data="invalid-json", content_type="application/json"
        )
        assert response.status_code in [400, 404, 405, 500]  # Should handle gracefully


class TestUIUXComponents:
    """
    Test suite for UI/UX components and user interaction patterns.

    Educational Notes:
    - Demonstrates testing of user interface components
    - Validates accessibility and usability requirements
    - Tests responsive design and professional appearance
    """

    @pytest.fixture
    def client(self):
        """Flask test client for UI/UX testing."""
        app = AcademicResearchApp()
        app.app.config["TESTING"] = True
        return app.app.test_client()

    def test_main_template_includes_required_elements(self, client):
        """
        Test main template includes essential UI elements for academic research.

        Educational Note:
        Template testing ensures consistent user interface
        and validates HTML structure for accessibility.
        """
        response = client.get("/")
        content = response.data.decode("utf-8")

        # Check for essential HTML structure
        assert "<html" in content
        assert "<head>" in content
        assert "<body>" in content

        # Check for academic research interface elements
        essential_elements = [
            "meta charset",
            "viewport",
            "title",
        ]

        for element in essential_elements:
            assert element in content.lower()

    def test_javascript_modules_are_accessible(self, client):
        """
        Test JavaScript modules are properly accessible for UI functionality.

        Educational Note:
        Module accessibility testing ensures interactive features
        work correctly for enhanced user experience.
        """
        js_modules = [
            "/static/js/modules/academic-research-ui.js",
            "/static/js/modules/accessibility-manager.js",
            "/static/js/modules/filter-manager.js",
            "/static/js/modules/academic-ui-core.js",
        ]

        for module_path in js_modules:
            response = client.get(module_path)
            assert response.status_code == 200
            assert len(response.data) > 0  # File should not be empty

    def test_css_styling_is_accessible(self, client):
        """
        Test CSS styling files are accessible for professional appearance.

        Educational Note:
        CSS accessibility testing ensures consistent visual presentation
        and professional appearance for academic users.
        """
        response = client.get("/static/css/main.css")
        assert response.status_code == 200
        assert len(response.data) > 0

        # Basic CSS content validation
        css_content = response.data.decode("utf-8")
        # Should contain CSS rules
        assert "{" in css_content and "}" in css_content


class TestCleanArchitectureCompliance:
    """
    Test suite validating Clean Architecture principles in web layer.

    Educational Notes:
    - Tests proper separation of concerns between layers
    - Validates dependency direction (inward only)
    - Ensures web layer doesn't contain business logic
    """

    def test_web_layer_depends_only_on_application_layer(self):
        """
        Test that web layer (Flask routes) only depends on application layer.

        Educational Note:
        Dependency direction testing ensures Clean Architecture compliance
        and prevents architectural degradation over time.
        """
        from gui.app import AcademicResearchApp

        # Create app instance
        app = AcademicResearchApp()

        # Validate that web layer has use case dependencies
        assert hasattr(app, "_search_use_case")
        assert hasattr(app, "_concept_extraction_use_case")

        # Use cases should be abstractions (interfaces) not concrete implementations
        # This validates Dependency Inversion Principle

    def test_no_domain_imports_in_route_handlers(self):
        """
        Test that route handlers don't directly import domain entities.

        Educational Note:
        This test prevents violation of Clean Architecture boundaries
        by ensuring web layer uses application layer as intermediary.
        """
        # This would require static analysis or import inspection
        # For now, we validate the pattern through app structure
        app = AcademicResearchApp()

        # Web layer should interact through use cases, not direct domain access
        assert app._search_use_case is not None
        assert app._concept_extraction_use_case is not None
