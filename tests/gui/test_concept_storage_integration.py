"""
Test-Driven Development for GUI-Concept Storage Integration
RED PHASE: Tests for missing /api/domains/{domain}/hierarchy endpoint

This module demonstrates TDD methodology by writing failing tests FIRST
before implementing the functionality to connect real concept storage
to the GUI visualization endpoints.

Educational Notes:
- RED-GREEN-REFACTOR: Following strict TDD cycle
- Contract Testing: Validating API response format for D3.js visualization
- Integration Testing: Testing connection between stored data and API endpoints
- Real Data Testing: Moving from mock data to actual concept hierarchies

Design Decisions:
- Test Real Data: Validate actual concept hierarchy files, not mocks
- API Contract: Ensure response format matches D3.js expectations
- Error Handling: Test both success and failure scenarios
- Performance: Test with real data volume for production readiness

Use Cases:
- GUI Integration: Test that visualization can load real concept data
- Domain Validation: Test handling of valid/invalid domain names
- Data Format: Test that JSON structure matches visualization requirements
"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch

from gui.app import create_app


class TestDomainHierarchyAPIEndpoint:
    """
    RED PHASE: Tests for missing /api/domains/{domain}/hierarchy endpoint.

    Educational Notes:
    - These tests will FAIL initially because the endpoint doesn't exist
    - Tests define the expected behavior before implementation
    - Following TDD methodology: fail first, then implement to pass
    """

    @pytest.fixture
    def client(self):
        """Create test client for Flask app."""
        app = create_app({"TESTING": True})
        with app.test_client() as client:
            yield client

    def test_domain_hierarchy_endpoint_exists(self, client):
        """
        RED PHASE: Test that /api/domains/{domain}/hierarchy endpoint exists.

        Educational Note:
        This test will FAIL because the endpoint doesn't exist yet.
        This is the "RED" phase of TDD - defining expected behavior.
        """
        # Test with a known domain from our concept storage
        response = client.get("/api/domains/industrial_iot_security/hierarchy")

        # This will fail initially - endpoint doesn't exist
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_domain_hierarchy_returns_json(self, client):
        """
        RED PHASE: Test that endpoint returns proper JSON structure.

        Educational Note:
        This test defines the expected JSON structure that D3.js visualization needs.
        """
        response = client.get("/api/domains/industrial_iot_security/hierarchy")

        assert response.status_code == 200
        assert response.content_type == "application/json"

        data = json.loads(response.data)

        # Test expected structure for D3.js visualization
        assert "root_concepts" in data, "Missing root_concepts key for D3.js"
        assert isinstance(data["root_concepts"], list), "root_concepts should be a list"

    def test_domain_hierarchy_contains_real_concept_data(self, client):
        """
        RED PHASE: Test that endpoint returns real concept data from storage.

        Educational Note:
        This test validates that we're serving real extracted concepts,
        not mock data like the current /api/concepts endpoint.
        """
        response = client.get("/api/domains/industrial_iot_security/hierarchy")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Validate real concept data structure
        if data["root_concepts"]:
            concept = data["root_concepts"][0]

            # These fields should exist in real concept data
            required_fields = ["text", "frequency", "relevance_score", "source_papers"]
            for field in required_fields:
                assert field in concept, f"Missing required field: {field}"

            # Validate real data types and values
            assert isinstance(concept["frequency"], int), "frequency should be integer"
            assert isinstance(
                concept["relevance_score"], float
            ), "relevance_score should be float"
            assert isinstance(
                concept["source_papers"], list
            ), "source_papers should be list"

    def test_domain_hierarchy_handles_valid_domains(self, client):
        """
        RED PHASE: Test endpoint works with all valid domains from concept storage.

        Educational Note:
        Test multiple domains to ensure the endpoint works with our
        actual extracted concept data, not just one example.
        """
        # These domains exist in our concept_storage/concepts/ directory
        valid_domains = [
            "industrial_iot_security",
            "water_infrastructure_incident_response",
            "quantum_cryptanalysis_threats",
            "healthcare_privacy_compliance",
        ]

        for domain in valid_domains:
            response = client.get(f"/api/domains/{domain}/hierarchy")

            assert response.status_code == 200, f"Domain {domain} should return 200"

            data = json.loads(response.data)
            assert "root_concepts" in data, f"Domain {domain} missing root_concepts"

    def test_domain_hierarchy_handles_invalid_domain(self, client):
        """
        RED PHASE: Test error handling for non-existent domains.

        Educational Note:
        Good API design includes proper error handling.
        Test that invalid domains return appropriate 404 responses.
        """
        response = client.get("/api/domains/nonexistent_domain/hierarchy")

        assert response.status_code == 404, "Invalid domain should return 404"

        data = json.loads(response.data)
        assert "error" in data, "Error response should include error message"
        assert "success" in data, "Error response should include success=False"
        assert data["success"] is False, "Error response success should be False"

    def test_domain_hierarchy_data_volume_realistic(self, client):
        """
        RED PHASE: Test that endpoint handles realistic data volumes.

        Educational Note:
        Test with real concept hierarchy files to ensure the endpoint
        can handle the actual data volume from our extractions.
        """
        response = client.get("/api/domains/industrial_iot_security/hierarchy")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Real concept hierarchies should have substantial content
        # (Our actual files have thousands of concepts)
        assert len(data["root_concepts"]) > 10, "Should have substantial concept data"

        # Response should be reasonably sized but not empty
        response_size = len(response.data)
        assert response_size > 1000, "Response should contain substantial data"
        assert response_size < 10_000_000, "Response should not be excessively large"


class TestAPIConceptsRealDataIntegration:
    """
    RED PHASE: Tests for /api/concepts endpoint to serve real data.

    Educational Notes:
    - Current endpoint serves mock data, tests will validate real data integration
    - Tests define transition from mock to real concept storage
    """

    @pytest.fixture
    def client(self):
        """Create test client for Flask app."""
        app = create_app({"TESTING": True})
        with app.test_client() as client:
            yield client

    def test_api_concepts_serves_real_extracted_data(self, client):
        """
        RED PHASE: Test that /api/concepts serves real concept data, not mocks.

        Educational Note:
        This test will initially pass with mock data, but should validate
        real concept data from our concept_storage directory structure.
        """
        response = client.get("/api/concepts")

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "concepts" in data
        assert "success" in data
        assert data["success"] is True

        # Validate this is real data, not mock data
        if data["concepts"]:
            concept = data["concepts"][0]

            # Real concepts should have extraction metadata that mock data doesn't have
            real_data_indicators = [
                "extraction_method",  # tfidf, textrank, etc.
                "created_at",  # ISO timestamp
                "source_domain",  # industrial_iot_security, etc.
                "relevance_score",  # float between 0-1
            ]

            # All indicators should be present for real data
            for indicator in real_data_indicators:
                assert indicator in concept, f"Missing real data field: {indicator}"

            # Validate data types for real concept fields
            assert isinstance(concept["frequency"], int), "frequency should be integer"
            assert isinstance(
                concept["relevance_score"], float
            ), "relevance_score should be float"
            assert isinstance(
                concept["source_papers"], list
            ), "source_papers should be list"
            assert concept["extraction_method"] in [
                "tfidf",
                "textrank",
                "yake",
            ], "Should have valid extraction method"

    def test_api_concepts_aggregates_from_multiple_domains(self, client):
        """
        RED PHASE: Test that /api/concepts aggregates concepts from all domains.

        Educational Note:
        Real implementation should aggregate concepts from all extracted domains,
        not just serve a fixed mock list of 20 items.
        """
        response = client.get("/api/concepts")

        assert response.status_code == 200
        data = json.loads(response.data)

        concepts = data["concepts"]

        if concepts:
            # Check if we have diversity in source domains
            domains = set()
            for concept in concepts:
                if "source_domain" in concept:
                    domains.add(concept["source_domain"])

            # Should have concepts from multiple domains (we have 30+ domains)
            assert (
                len(domains) > 5
            ), f"Should aggregate from multiple domains, got {len(domains)}"

            # Should have realistic number of concepts (not just 20 mock items)
            assert (
                len(concepts) > 50
            ), f"Should have substantial concepts, got {len(concepts)}"

    def test_api_concepts_search_filters_real_data(self, client):
        """
        RED PHASE: Test that search filtering works with real concept text.

        Educational Note:
        Test search functionality against actual extracted concept terms,
        not artificial mock data patterns.
        """
        # Search for a term that should exist in our cybersecurity domains
        response = client.get("/api/concepts?search=security")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Should find security-related concepts from real data
        concepts = data["concepts"]
        assert len(concepts) > 0, "Should find security-related concepts"

        # Verify search actually filtered (returned concepts should contain search term)
        for concept in concepts[:5]:  # Check first 5 concepts
            concept_text = concept.get("text", "").lower()
            assert (
                "security" in concept_text
            ), f"Concept '{concept_text}' should contain search term"

    def test_api_concepts_category_filters_by_domain(self, client):
        """
        RED PHASE: Test that category filtering works with real domain structure.

        Educational Note:
        Category filtering should map to our actual source_domain structure,
        not artificial "Machine Learning" vs "NLP" categories.
        """
        # Filter by a real domain category from our concept storage
        response = client.get("/api/concepts?category=industrial_iot_security")

        assert response.status_code == 200
        data = json.loads(response.data)

        concepts = data["concepts"]
        if concepts:
            # All returned concepts should be from the specified domain
            for concept in concepts:
                assert (
                    concept.get("source_domain") == "industrial_iot_security"
                ), f"Concept should be from industrial_iot_security domain"

    def test_api_concepts_realistic_data_volume(self, client):
        """
        RED PHASE: Test that endpoint handles realistic concept volumes.

        Educational Note:
        Real concept extraction produces hundreds or thousands of concepts,
        not just 20 mock items. Test with realistic data scale.
        """
        response = client.get("/api/concepts")

        assert response.status_code == 200
        data = json.loads(response.data)

        concepts = data["concepts"]

        # Should have substantial concept data from real extraction
        assert (
            len(concepts) > 100
        ), f"Should have realistic concept count, got {len(concepts)}"

        # Response should be reasonable size but substantial
        response_size = len(response.data)
        assert response_size > 5000, "Response should contain substantial data"
        assert response_size < 50_000_000, "Response should not be excessively large"


class TestAPIConceptsRealDataIntegration:
    """
    RED PHASE: Tests for /api/concepts endpoint to serve real data.

    Educational Notes:
    - Current endpoint serves mock data, tests will validate real data integration
    - Tests define transition from mock to real concept storage
    """

    @pytest.fixture
    def client(self):
        """Create test client for Flask app."""
        app = create_app({"TESTING": True})
        with app.test_client() as client:
            yield client

    def test_api_concepts_serves_real_extracted_data(self, client):
        """
        RED PHASE: Test that /api/concepts serves real concept data, not mocks.

        Educational Note:
        This test will initially pass with mock data, but should be modified
        to validate real concept data from our concept_storage.
        """
        response = client.get("/api/concepts")

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "concepts" in data
        assert "success" in data
        assert data["success"] is True

        # Validate this is real data, not mock data
        if data["concepts"]:
            concept = data["concepts"][0]

            # Real concepts should have extraction metadata
            # Mock concepts use simple structure like {"id": "concept_1", "name": "Concept 1"}
            real_data_indicators = [
                "extraction_method",
                "created_at",
                "source_domain",
                "relevance_score",
            ]

            # At least some indicators should be present for real data
            real_indicators_present = sum(
                1 for indicator in real_data_indicators if indicator in concept
            )

            assert (
                real_indicators_present > 0
            ), "Should serve real concept data with metadata"

    def test_api_concepts_aggregates_from_multiple_domains(self, client):
        """
        RED PHASE: Test that /api/concepts aggregates concepts from all domains.

        Educational Note:
        Real implementation should aggregate concepts from all extracted domains,
        not just serve a fixed mock list.
        """
        response = client.get("/api/concepts")

        assert response.status_code == 200
        data = json.loads(response.data)

        # Real aggregation should have concepts from multiple domains
        concepts = data["concepts"]

        if concepts:
            # Check if we have diversity in source domains
            domains = set()
            for concept in concepts:
                if "source_domain" in concept:
                    domains.add(concept["source_domain"])

            # Should have concepts from multiple domains, not just one
            assert len(domains) > 1, "Should aggregate concepts from multiple domains"


# Integration test to validate the full workflow
class TestConceptStorageToGUIIntegration:
    """
    RED PHASE: Integration tests for complete concept storage to GUI workflow.

    Educational Notes:
    - Tests end-to-end integration from stored JSON files to GUI endpoints
    - Validates the complete data pipeline for D3.js visualization
    """

    @pytest.fixture
    def client(self):
        """Create test client for Flask app."""
        app = create_app({"TESTING": True})
        with app.test_client() as client:
            yield client

    def test_concept_hierarchy_files_exist_for_testing(self):
        """
        RED PHASE: Validate that test data exists for integration testing.

        Educational Note:
        Before testing API integration, verify that the underlying
        concept hierarchy files exist and are properly formatted.
        """
        outputs_dir = Path("outputs")
        assert outputs_dir.exists(), "outputs directory should exist"

        # Find at least one concept_hierarchy.json file
        hierarchy_files = list(outputs_dir.glob("**/concept_hierarchy.json"))
        assert (
            len(hierarchy_files) > 0
        ), "Should have concept hierarchy files for testing"

        # Validate file structure
        test_file = hierarchy_files[0]
        with open(test_file, "r") as f:
            data = json.load(f)

        assert "root_concepts" in data, "Hierarchy files should have root_concepts"
        assert isinstance(data["root_concepts"], list), "root_concepts should be list"

    def test_gui_can_load_real_concept_hierarchies(self, client):
        """
        RED PHASE: Test that GUI can successfully load and serve real hierarchies.

        Educational Note:
        This integration test validates the complete workflow:
        concept extraction → storage → API → visualization
        """
        # This test will fail until we implement the missing endpoint

        # Get list of available domains from concept storage
        concept_storage_dir = Path("concept_storage/concepts")
        if concept_storage_dir.exists():
            domains = [d.name for d in concept_storage_dir.iterdir() if d.is_dir()]

            # Test at least one domain
            if domains:
                test_domain = domains[0]
                response = client.get(f"/api/domains/{test_domain}/hierarchy")

                # This will fail until endpoint is implemented
                assert (
                    response.status_code == 200
                ), f"Should load hierarchy for {test_domain}"

                data = json.loads(response.data)
                assert "root_concepts" in data, "Should return hierarchy structure"
