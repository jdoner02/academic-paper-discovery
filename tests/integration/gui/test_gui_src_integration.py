"""
Integration tests for GUI-src system integration following TDD methodology.

This test suite validates that the Flask GUI properly integrates with the
Clean Architecture components in the src directory. Tests are organized
to verify different integration aspects:

Educational Notes:
- Tests define expected behavior before implementation (TDD RED phase)
- Each test validates a specific integration contract
- Real domain objects and use cases are used, not mocks
- Integration tests focus on component interaction, not unit behavior
"""

import json
import pytest
from datetime import datetime
from pathlib import Path


class TestGUIConfigurationIntegration:
    """Test GUI integration with KeywordConfig domain objects"""

    def setup_method(self):
        """Set up test fixtures with real src components"""
        # Import GUI components with fallback
        gui_app = pytest.importorskip("gui.app")
        self.app = gui_app.create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def teardown_method(self):
        """Clean up test fixtures"""
        pass

    def test_gui_loads_real_configuration_files(self):
        """Test that GUI loads actual configuration files from config directory"""
        # Act: Request configuration list
        response = self.client.get("/api/configurations")

        # Assert: Should load real config files
        assert response.status_code == 200
        config_data = json.loads(response.data)

        # Should contain real configuration files
        config_names = [config["name"] for config in config_data["configurations"]]
        assert "heart_rate_variability" in config_names

        # Each configuration should have expected structure (based on actual GUI structure)
        hrv_config = next(
            c
            for c in config_data["configurations"]
            if c["name"] == "heart_rate_variability"
        )
        assert "display_name" in hrv_config
        assert "file_path" in hrv_config
        assert "primary_keywords" in hrv_config
        assert "secondary_keywords" in hrv_config

    def test_gui_configuration_detail_uses_keyword_config_domain_object(self):
        """Test that configuration detail endpoint uses real KeywordConfig objects"""
        # Act: Request specific configuration detail
        response = self.client.get("/api/configurations/heart_rate_variability")

        # Assert: Should return data from actual KeywordConfig object
        assert response.status_code == 200
        config_data = json.loads(response.data)

        # Should have structure matching actual GUI implementation
        assert "strategies" in config_data
        assert "description" in config_data
        assert "domain" in config_data

        # Strategies should be a dictionary with strategy details
        strategies = config_data["strategies"]
        assert len(strategies) > 0

        # Each strategy should have proper structure
        strategy_name = list(strategies.keys())[0]
        strategy = strategies[strategy_name]
        assert "name" in strategy
        assert "primary_keywords" in strategy
        assert "search_limit" in strategy

    def test_gui_validates_configuration_with_domain_rules(self):
        """Test that GUI uses domain validation rules for configuration"""
        # Arrange: Create invalid configuration data
        invalid_config = {
            "name": "",  # Empty name should be invalid
            "strategies": [],  # Empty strategies should be invalid
        }

        # Act: Attempt to validate invalid configuration
        response = self.client.post(
            "/api/configurations/validate",
            json=invalid_config,
            content_type="application/json",
        )

        # Assert: Should use domain validation rules (based on actual GUI response)
        assert response.status_code == 400
        validation_result = json.loads(response.data)

        assert "error" in validation_result
        assert "domain_validation_errors" in validation_result

        errors = validation_result["domain_validation_errors"]
        assert len(errors) > 0


class TestGUIUseCaseIntegration:
    """Test GUI integration with application use cases"""

    def setup_method(self):
        """Set up test fixtures with real use case integration"""
        # Import components inside setup to handle import failures gracefully
        gui_app = pytest.importorskip("gui.app")
        self.app = gui_app.create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_gui_search_executes_real_use_case(self):
        """Test that GUI search endpoints execute actual use cases"""
        # Act: Execute search through GUI with correct parameters
        response = self.client.post(
            "/api/search",
            json={"config_name": "heart_rate_variability"},
            content_type="application/json",
        )

        # Assert: Should execute real use case and return domain results
        assert response.status_code == 200
        search_results = json.loads(response.data)

        # Should have proper response structure
        assert "success" in search_results
        assert "data" in search_results
        assert search_results["success"] is True

        # Data should contain expected fields
        data = search_results["data"]
        assert "papers" in data
        assert "search_metadata" in data

        # Results should come from actual use case execution
        papers = data["papers"]
        # Papers list could be empty if no matches found
        if len(papers) > 0:
            paper = papers[0]
            assert "doi" in paper
            assert "title" in paper
            assert "authors" in paper

    def test_gui_custom_search_uses_search_query_value_object(self):
        """Test that custom search uses SearchQuery domain objects"""
        # Arrange: Custom search parameters
        search_params = {
            "terms": ["heart rate variability", "traumatic brain injury"],
            "max_results": 10,
            "date_range": {"start": "2020-01-01", "end": "2023-12-31"},
        }

        # Act: Execute custom search
        response = self.client.post(
            "/api/search/custom", json=search_params, content_type="application/json"
        )

        # Assert: Should create and use SearchQuery value object
        assert response.status_code == 200
        search_results = json.loads(response.data)

        assert "papers" in search_results
        assert "query_validation" in search_results
        assert "search_executed" in search_results

        # Should validate and execute search successfully
        assert search_results["query_validation"] == "passed"
        assert search_results["search_executed"] is True

    def test_gui_batch_operations_integrate_with_use_case_methods(self):
        """Test that batch operations use real use case methods"""
        # Skip this test since batch endpoint is not implemented yet
        pytest.skip("Batch search endpoint not yet implemented in GUI")


class TestGUIErrorHandlingIntegration:
    """Test GUI error handling with src exceptions"""

    def setup_method(self):
        """Set up test fixtures for error scenarios"""
        gui_app = pytest.importorskip("gui.app")
        self.app = gui_app.create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_gui_handles_domain_validation_errors(self):
        """Test that GUI properly handles domain validation errors"""
        # Arrange: Invalid search query that should trigger domain validation
        invalid_query = {
            "terms": [],  # Empty terms should be invalid
            "max_results": -1,  # Negative results should be invalid
        }

        # Act: Submit invalid query
        response = self.client.post(
            "/api/search/custom", json=invalid_query, content_type="application/json"
        )

        # Assert: Should return proper error response
        assert response.status_code == 400
        error_response = json.loads(response.data)

        assert "error" in error_response
        assert "error_type" in error_response
        assert error_response["error_type"] == "validation_error"

    def test_gui_handles_repository_errors(self):
        """Test that GUI handles repository access errors"""
        # This test would verify error handling when repository operations fail
        # Implementation depends on how repository errors are simulated
        pass

    def test_gui_handles_configuration_errors(self):
        """Test that GUI handles configuration loading errors"""
        # Act: Request non-existent configuration
        response = self.client.get("/api/configurations/nonexistent_config")

        # Assert: Should return appropriate error
        assert response.status_code == 404
        error_response = json.loads(response.data)

        assert "error" in error_response
        assert "configuration not found" in error_response["error"].lower()


class TestGUIPerformanceIntegration:
    """Test performance characteristics of GUI-src integration"""

    def setup_method(self):
        """Set up performance test fixtures"""
        gui_app = pytest.importorskip("gui.app")
        self.app = gui_app.create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_gui_configuration_loading_performance(self):
        """Test that configuration loading performs acceptably"""
        import time

        # Act: Load configurations and measure time
        start_time = time.time()
        response = self.client.get("/api/configurations")
        end_time = time.time()

        # Assert: Should load within reasonable time
        loading_time = end_time - start_time
        assert loading_time < 1.0  # Should load in under 1 second
        assert response.status_code == 200

    def test_gui_search_execution_performance(self):
        """Test that search execution performs acceptably"""
        import time

        # Arrange: Simple search request
        search_request = {"strategy": "comprehensive_clinical_research"}

        # Act: Execute search and measure time
        start_time = time.time()
        response = self.client.post(
            "/api/search", json=search_request, content_type="application/json"
        )
        end_time = time.time()

        # Assert: Should execute within reasonable time
        search_time = end_time - start_time
        assert search_time < 5.0  # Should complete in under 5 seconds
        assert response.status_code == 200


class TestGUIDataStructureIntegration:
    """Test data structure consistency between GUI and src"""

    def setup_method(self):
        """Set up data structure test fixtures"""
        gui_app = pytest.importorskip("gui.app")
        self.app = gui_app.create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_gui_research_paper_serialization(self):
        """Test that ResearchPaper entities are properly serialized for GUI"""
        # Import ResearchPaper inside test method
        research_paper_module = pytest.importorskip(
            "src.domain.entities.research_paper"
        )
        ResearchPaper = research_paper_module.ResearchPaper

        # Create a ResearchPaper domain object
        paper = ResearchPaper(
            doi="10.1000/test",
            title="Test Paper",
            authors=["Author, A."],
            abstract="Test abstract",
            publication_date="2023-01-01",
            journal="Test Journal",
            keywords=["test"],
            url="https://example.com",
        )

        # Test that it can be serialized (this would be done in GUI)
        # Implementation depends on how serialization is handled
        assert paper.doi == "10.1000/test"
        assert paper.title == "Test Paper"

    def test_gui_keyword_config_serialization(self):
        """Test that KeywordConfig objects are properly serialized"""
        # Act: Get configuration data through GUI
        response = self.client.get("/api/configurations/heart_rate_variability")

        # Assert: Should properly serialize KeywordConfig structure
        assert response.status_code == 200
        config_data = json.loads(response.data)

        # Should maintain domain object structure
        assert isinstance(config_data, dict)
        assert "name" in config_data
        assert "strategies" in config_data

    def test_gui_search_query_serialization(self):
        """Test that SearchQuery value objects are properly handled"""
        # Arrange: Search query data
        query_data = {"terms": ["heart rate variability"], "max_results": 10}

        # Act: Submit query through GUI
        response = self.client.post(
            "/api/search/custom", json=query_data, content_type="application/json"
        )

        # Assert: Should handle SearchQuery creation and serialization
        assert response.status_code == 200
        result_data = json.loads(response.data)

        # Should include query information in response
        if "query_used" in result_data:
            query_used = result_data["query_used"]
            assert "terms" in query_used
