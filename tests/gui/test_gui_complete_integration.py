"""
TDD Cycle 3 - GUI Integration Tests

RED PHASE: Test suite for complete frontend-backend integration
focusing on template data provision and JavaScript API integration.

Educational Notes:
- Tests validate end-to-end GUI workflows
- Ensures real data flows from API to frontend
- Validates GitHub Pages deployment readiness
"""

import json
import pytest
from unittest.mock import patch, mock_open
import sys
import os

# Add gui directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../gui"))


class TestGUITemplateIntegration:
    """
    RED PHASE: Test template data integration with real concept storage.

    Educational Note:
    These tests validate that Flask templates receive proper data
    from our concept storage to display accurate statistics and
    enable proper frontend-backend integration.
    """

    def test_main_route_provides_concept_statistics(self, client):
        """
        RED PHASE: Test that main route provides real concept/paper counts.

        Currently the main route doesn't provide statistics to templates,
        but the index.html template expects total_concepts and total_papers.
        """
        response = client.get("/")

        assert response.status_code == 200

        # Check if response contains actual concept/paper counts
        html_content = response.data.decode("utf-8")

        # Should have real statistics, not placeholder zeros
        assert (
            "0 Papers" not in html_content
        ), "Should show real paper count, not placeholder"
        assert (
            "0 Concepts" not in html_content
        ), "Should show real concept count, not placeholder"

        # Should contain non-zero counts from our real data
        import re

        # Look for stat-number spans followed by stat-label spans with Papers/Concepts
        paper_pattern = r'<span class="stat-number">(\d+)</span>\s*<span class="stat-label">Papers</span>'
        concept_pattern = r'<span class="stat-number">(\d+)</span>\s*<span class="stat-label">Concepts</span>'

        paper_match = re.search(paper_pattern, html_content)
        concept_match = re.search(concept_pattern, html_content)

        assert paper_match, "Should display paper count in UI"
        assert concept_match, "Should display concept count in UI"

        paper_count = int(paper_match.group(1))
        concept_count = int(concept_match.group(1))

        assert paper_count > 0, "Should show actual paper count from concept storage"
        assert (
            concept_count > 0
        ), "Should show actual concept count from concept storage"

    def test_template_receives_real_data_variables(self, client):
        """
        GREEN PHASE: Test that template context includes real data variables.

        The template should receive total_concepts and total_papers
        variables calculated from actual concept storage data.
        """
        # Mock template rendering to capture context
        with patch("app.render_template") as mock_render:
            mock_render.return_value = "mocked template"

            response = client.get("/")

            # Verify render_template was called with proper context
            assert mock_render.called, "render_template should be called"

            call_args = mock_render.call_args
            # Arguments: call_args[0] is positional args, call_args[1] is keyword args
            context = call_args[1] if call_args[1] else {}

            # Should provide real statistics in template context
            assert "total_concepts" in context, "Template should receive total_concepts"
            assert "total_papers" in context, "Template should receive total_papers"

            # Values should be from real data, not placeholders
            assert context["total_concepts"] > 0, "Should have real concept count"
            assert context["total_papers"] > 0, "Should have real paper count"


class TestGUIJavaScriptIntegration:
    """
    RED PHASE: Test JavaScript frontend integration with API endpoints.

    Educational Note:
    These tests validate that the frontend JavaScript can properly
    consume our API endpoints and display real concept data.
    """

    def test_concepts_dashboard_loads_real_data(self, client):
        """
        RED PHASE: Test that concepts dashboard can fetch and display real concept data.

        The research dashboard should be able to load concept data
        from our /api/concepts endpoint and display it properly.
        """
        # Test the underlying API that dashboard should consume
        response = client.get("/api/concepts?limit=20")

        assert response.status_code == 200
        data = json.loads(response.data)

        # API should provide data suitable for dashboard display
        assert "concepts" in data, "API should provide concepts list"
        assert "total" in data, "API should provide total count"
        assert "domains_available" in data, "API should provide available domains"

        concepts = data["concepts"]
        assert len(concepts) > 0, "Should have real concepts to display"

        # Each concept should have metadata for dashboard display
        for concept in concepts[:3]:  # Check first few
            assert "text" in concept, "Concept should have display text"
            assert "source_domain" in concept, "Concept should have domain info"
            assert "relevance_score" in concept, "Concept should have relevance data"
            assert "frequency" in concept, "Concept should have frequency data"

    def test_concept_search_functionality_works(self, client):
        """
        RED PHASE: Test that concept search returns filtered results.

        The frontend should be able to search concepts and get
        relevant filtered results from the API.
        """
        # Test search functionality
        response = client.get("/api/concepts?search=security")

        assert response.status_code == 200
        data = json.loads(response.data)

        concepts = data["concepts"]
        assert len(concepts) > 0, "Search should return matching concepts"

        # Results should be relevant to search term
        search_term = "security"
        found_relevant = False
        for concept in concepts:
            concept_text = concept.get("text", "").lower()
            paper_title = concept.get("paper_title", "").lower()
            domain = concept.get("source_domain", "").lower()

            if (
                search_term in concept_text
                or search_term in paper_title
                or search_term in domain
            ):
                found_relevant = True
                break

        assert (
            found_relevant
        ), f"Search results should contain '{search_term}' relevance"

    def test_domain_filtering_functionality_works(self, client):
        """
        RED PHASE: Test that domain filtering returns domain-specific concepts.

        The frontend should be able to filter concepts by domain
        and get domain-specific results.
        """
        # First get available domains
        response = client.get("/api/concepts?limit=100")
        data = json.loads(response.data)

        available_domains = data.get("domains_available", [])
        assert len(available_domains) > 0, "Should have available domains"

        # Test filtering by first available domain
        test_domain = available_domains[0]
        response = client.get(f"/api/concepts?category={test_domain}")

        assert response.status_code == 200
        data = json.loads(response.data)

        concepts = data["concepts"]
        assert len(concepts) > 0, f"Should have concepts for domain '{test_domain}'"

        # All returned concepts should be from the requested domain
        for concept in concepts:
            assert (
                concept.get("source_domain") == test_domain
            ), f"Filtered concept should be from domain '{test_domain}'"


class TestGUIWorkflowIntegration:
    """
    RED PHASE: Test complete user workflows for GitHub Pages deployment.

    Educational Note:
    These tests validate end-to-end user journeys that will work
    when deployed to GitHub Pages as a static site.
    """

    def test_complete_concept_exploration_workflow(self, client):
        """
        RED PHASE: Test complete workflow from landing page to concept details.

        User should be able to: load main page -> select domain ->
        explore concepts -> view concept details with evidence.
        """
        # Step 1: Load main page
        response = client.get("/")
        assert response.status_code == 200

        # Step 2: Get available domains for selection
        response = client.get("/api/domains")
        assert response.status_code == 200
        domains_data = json.loads(response.data)

        available_domains = domains_data.get("domains", [])
        assert len(available_domains) > 0, "Should have selectable domains"

        # Step 3: Load concept hierarchy for a domain
        test_domain = available_domains[0]
        response = client.get(f"/api/domains/{test_domain}/hierarchy")
        assert response.status_code == 200
        hierarchy_data = json.loads(response.data)

        assert "root_concepts" in hierarchy_data, "Should provide concept hierarchy"
        concepts = hierarchy_data["root_concepts"]
        assert len(concepts) > 0, "Domain should have explorable concepts"

        # Step 4: Verify concept has exploration metadata
        concept = concepts[0]
        assert "text" in concept, "Concept should have display text"
        assert "source_papers" in concept, "Concept should link to source papers"
        assert "frequency" in concept, "Concept should have usage frequency"

    def test_static_file_serving_compatibility(self, client):
        """
        RED PHASE: Test that static files are served properly for deployment.

        GitHub Pages needs all static assets (CSS, JS) to be accessible
        and properly linked from templates.
        """
        # Test main CSS file accessibility
        response = client.get("/static/css/main.css")
        # Note: This might 404 if file doesn't exist - that's the point of RED phase

        # Test main JavaScript files accessibility
        js_files = [
            "/static/js/concept-visualization.js",
            "/static/js/research-dashboard.js",
            "/static/js/evidence-explorer.js",
        ]

        accessible_js_files = 0
        for js_file in js_files:
            response = client.get(js_file)
            if response.status_code == 200:
                accessible_js_files += 1

        # Should have accessible JavaScript files for functionality
        assert accessible_js_files > 0, "Should have accessible JavaScript files"

        # If we can't access main CSS, that's a deployment issue
        css_response = client.get("/static/css/main.css")
        if css_response.status_code == 404:
            pytest.fail(
                "Main CSS file not accessible - needed for GitHub Pages deployment"
            )
