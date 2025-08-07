"""
GUI Application Tests - Research Paper Concept Explorer

This module contains tests for the Flask web interface and concept visualization
functionality. Demonstrates testing patterns for web applications with
Clean Architecture.

Educational Notes:
- Shows Flask application testing patterns
- Demonstrates mock usage for external dependencies
- Tests JSON API endpoints for visualization data
- Validates web interface integration with domain model

Design Patterns Applied:
- Test Fixtures: setUp/tearDown for consistent test environment
- Mock Objects: Isolate web layer from domain dependencies
- Assertion Patterns: Comprehensive validation of web responses
"""

import pytest
import json
import tempfile
import os
from pathlib import Path

# Add src to path for imports
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gui.app import AcademicResearchApp


class TestConceptExplorerApp:
    """Test suite for the GUI Flask application"""

    def setup_method(self):
        """Set up test fixtures before each test"""
        self.app = AcademicResearchApp()
        self.app.app.config["TESTING"] = True
        self.client = self.app.app.test_client()

    def test_homepage_loads_successfully(self):
        """Test that the main interface loads without errors"""
        response = self.client.get("/")

        assert response.status_code == 200
        assert b"Research Paper Concept Explorer" in response.data
        assert b"concept-visualization" in response.data

    def test_domains_api_returns_valid_json(self):
        """Test the domains API endpoint returns proper JSON structure"""
        response = self.client.get("/api/domains")

        assert response.status_code == 200
        assert response.content_type == "application/json"

        data = json.loads(response.data)
        assert isinstance(data, list)

        # Should have at least the heart_rate_variability domain
        domain_names = [domain["name"] for domain in data]
        assert "heart_rate_variability" in domain_names

    def test_domain_concepts_api_with_valid_domain(self):
        """Test concepts API with a valid domain returns hierarchy"""
        response = self.client.get("/api/domains/heart_rate_variability/concepts")

        assert response.status_code == 200
        assert response.content_type == "application/json"

        data = json.loads(response.data)
        assert "name" in data
        assert "children" in data
        assert data["name"] == "heart_rate_variability"

    def test_domain_concepts_api_with_invalid_domain(self):
        """Test concepts API with invalid domain returns 404"""
        response = self.client.get("/api/domains/nonexistent_domain/concepts")

        assert response.status_code == 404

        data = json.loads(response.data)
        assert "error" in data
        assert "not found" in data["error"].lower()

    def test_concept_evidence_api_with_valid_concept(self):
        """Test evidence API returns sentences for valid concept"""
        # First get available concepts
        concepts_response = self.client.get(
            "/api/domains/heart_rate_variability/concepts"
        )
        concepts_data = json.loads(concepts_response.data)

        # Find a concept with evidence
        def find_concept_with_evidence(node):
            if "evidence_sentences" in node and node["evidence_sentences"]:
                return node["name"]

            if "children" in node:
                for child in node["children"]:
                    result = find_concept_with_evidence(child)
                    if result:
                        return result
            return None

        concept_name = find_concept_with_evidence(concepts_data)

        if concept_name:
            response = self.client.get(f"/api/concepts/{concept_name}/evidence")

            assert response.status_code == 200
            assert response.content_type == "application/json"

            data = json.loads(response.data)
            assert "concept" in data
            assert "evidence_sentences" in data
            assert isinstance(data["evidence_sentences"], list)

    def test_concept_evidence_api_with_invalid_concept(self):
        """Test evidence API with nonexistent concept returns 404"""
        response = self.client.get("/api/concepts/nonexistent_concept/evidence")

        assert response.status_code == 404

        data = json.loads(response.data)
        assert "error" in data

    def test_pdf_serve_endpoint_exists(self):
        """Test that PDF serving endpoint is available"""
        # Test with a non-existent PDF (should return 404)
        response = self.client.get("/api/pdf/nonexistent.pdf")

        # Should return 404 for non-existent file, not 500 error
        assert response.status_code == 404

    def test_static_files_accessible(self):
        """Test that CSS and JS static files are accessible"""
        # Test CSS file
        css_response = self.client.get("/static/css/main.css")
        assert css_response.status_code == 200
        assert "text/css" in css_response.content_type

        # Test JS files
        js_response = self.client.get("/static/js/main.js")
        assert js_response.status_code == 200
        assert (
            "javascript" in js_response.content_type
            or "text/plain" in js_response.content_type
        )

        viz_response = self.client.get("/static/js/visualization.js")
        assert viz_response.status_code == 200

    def test_api_error_handling(self):
        """Test that API endpoints handle errors gracefully"""
        # Test with malformed requests
        response = self.client.get("/api/domains//concepts")
        # Should handle empty domain name gracefully
        assert response.status_code in [404, 400]

        # Test non-existent API endpoint
        response = self.client.get("/api/nonexistent")
        assert response.status_code == 404


class TestVisualizationDataStructure:
    """Test the data structure required for D3.js visualizations"""

    def setup_method(self):
        """Set up test fixtures"""
        self.app = AcademicResearchApp()
        self.app.app.config["TESTING"] = True
        self.client = self.app.app.test_client()

    def test_hierarchy_structure_for_d3js(self):
        """Test that concept hierarchy follows D3.js requirements"""
        response = self.client.get("/api/domains/heart_rate_variability/concepts")
        data = json.loads(response.data)

        # D3.js hierarchy requirements
        assert "name" in data
        assert "children" in data or "value" in data

        # Recursively check structure
        def validate_node(node):
            assert "name" in node

            if "children" in node:
                assert isinstance(node["children"], list)
                for child in node["children"]:
                    validate_node(child)
            else:
                # Leaf nodes should have value
                assert "value" in node or "frequency" in node

        validate_node(data)

    def test_evidence_data_structure(self):
        """Test evidence data follows expected structure"""
        # Get concepts first
        concepts_response = self.client.get(
            "/api/domains/heart_rate_variability/concepts"
        )
        concepts_data = json.loads(concepts_response.data)

        # Find a concept with evidence
        def find_concept_with_evidence(node):
            if "evidence_sentences" in node and node["evidence_sentences"]:
                return node["name"]

            if "children" in node:
                for child in node["children"]:
                    result = find_concept_with_evidence(child)
                    if result:
                        return result
            return None

        concept_name = find_concept_with_evidence(concepts_data)

        if concept_name:
            response = self.client.get(f"/api/concepts/{concept_name}/evidence")
            data = json.loads(response.data)

            # Validate evidence structure
            for evidence in data["evidence_sentences"]:
                assert "sentence" in evidence
                assert "source_file" in evidence
                # Optional fields
                if "confidence_score" in evidence:
                    assert isinstance(evidence["confidence_score"], (int, float))


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
