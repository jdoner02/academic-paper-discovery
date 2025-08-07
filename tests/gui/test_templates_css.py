"""
CSS and Template Tests - Academic Research Interface

This module tests CSS styling and HTML template components for the academic
research interface, focusing on professional appearance, accessibility, and
responsive design principles.

Educational Notes:
- Demonstrates testing strategies for frontend styling and markup
- Shows validation of responsive design and cross-browser compatibility
- Tests accessibility compliance in HTML structure and CSS implementation
- Validates professional UI/UX patterns for academic applications

Testing Approach:
- Template Structure: Validate HTML5 semantic markup and accessibility
- CSS Architecture: Test modular styling and responsive design patterns
- Visual Consistency: Ensure professional appearance across components
- Performance: Validate efficient CSS and optimized template loading

Design Principles Tested:
- Mobile-First Design: Responsive breakpoints and fluid layouts
- Accessibility-First: WCAG 2.1 AA compliance in markup and styling
- Progressive Enhancement: Core functionality without JavaScript
- Performance Optimization: Efficient CSS delivery and minimal overhead
"""

import pytest
import re
from pathlib import Path
from typing import List, Dict, Any
import tempfile
import os


class TestHTMLTemplateStructure:
    """
    Test suite for HTML template structure and semantic markup.

    Educational Notes:
    - Validates HTML5 semantic elements for academic content
    - Tests accessibility attributes and proper document structure
    - Ensures responsive design meta tags and viewport configuration
    """

    @pytest.fixture
    def template_path(self):
        """Path to main HTML template."""
        return Path(__file__).parent.parent.parent / "gui" / "templates" / "index.html"

    def test_html5_document_structure(self, template_path):
        """
        Test HTML5 document has proper structure and DOCTYPE.

        Educational Note:
        Proper document structure ensures cross-browser compatibility
        and validates semantic markup for academic content.
        """
        content = template_path.read_text(encoding="utf-8")

        # Check for HTML5 DOCTYPE
        assert "<!DOCTYPE html>" in content, "HTML5 DOCTYPE declaration missing"

        # Check for essential HTML structure
        essential_elements = [
            "<html",
            "<head>",
            "<body>",
            "</html>",
            "</head>",
            "</body>",
        ]

        for element in essential_elements:
            assert (
                element in content
            ), f"Essential element '{element}' missing from template"

    def test_meta_tags_for_responsive_design(self, template_path):
        """
        Test meta tags for responsive design and mobile compatibility.

        Educational Note:
        Responsive design meta tags ensure proper mobile experience
        for academic researchers using various devices.
        """
        content = template_path.read_text(encoding="utf-8")

        # Check for viewport meta tag
        viewport_pattern = (
            r'<meta\s+name="viewport"\s+content="[^"]*width=device-width[^"]*"'
        )
        assert re.search(
            viewport_pattern, content
        ), "Responsive viewport meta tag missing"

        # Check for character encoding
        charset_pattern = r'<meta\s+charset="utf-8"'
        assert re.search(
            charset_pattern, content, re.IGNORECASE
        ), "UTF-8 charset declaration missing"

    def test_accessibility_attributes(self, template_path):
        """
        Test accessibility attributes in HTML template.

        Educational Note:
        Accessibility attributes ensure the interface is usable
        by researchers with disabilities and assistive technologies.
        """
        content = template_path.read_text(encoding="utf-8")

        # Check for language attribute
        lang_pattern = r'<html[^>]*lang="[^"]*"'
        assert re.search(
            lang_pattern, content
        ), "HTML lang attribute missing for screen readers"

        # Check for accessibility features
        accessibility_features = ["aria-", "role=", "alt=", "title="]

        # At least some accessibility attributes should be present
        found_features = sum(
            1 for feature in accessibility_features if feature in content
        )
        assert found_features >= 2, "Insufficient accessibility attributes in template"

    def test_semantic_html_elements(self, template_path):
        """
        Test use of semantic HTML5 elements for academic content.

        Educational Note:
        Semantic elements improve accessibility and SEO while
        providing clear content structure for academic information.
        """
        content = template_path.read_text(encoding="utf-8")

        # Check for semantic elements appropriate for academic content
        semantic_elements = [
            "<main",
            "<header",
            "<nav",
            "<section",
            "<article",
            "<aside",
        ]

        # Should use at least some semantic elements for academic content
        found_semantic = sum(1 for element in semantic_elements if element in content)
        assert (
            found_semantic >= 2
        ), "Insufficient semantic HTML5 elements for academic content"

    def test_script_and_link_tags(self, template_path):
        """
        Test proper inclusion of CSS and JavaScript resources.

        Educational Note:
        Resource inclusion testing ensures all necessary assets
        are properly linked for full functionality.
        """
        content = template_path.read_text(encoding="utf-8")

        # Check for CSS inclusion
        css_pattern = r'<link[^>]*rel="stylesheet"[^>]*href="[^"]*\.css"'
        assert re.search(css_pattern, content), "CSS stylesheet not properly linked"

        # Check for JavaScript inclusion
        js_pattern = r'<script[^>]*src="[^"]*\.js"'
        js_found = re.search(js_pattern, content)

        # JavaScript might be included inline or at end of body
        inline_js = "<script>" in content
        assert js_found or inline_js, "JavaScript not properly included"


class TestCSSArchitecture:
    """
    Test suite for CSS architecture and styling patterns.

    Educational Notes:
    - Validates modular CSS architecture and maintainable styling
    - Tests responsive design implementation and mobile-first approach
    - Ensures consistent visual hierarchy for academic content
    """

    @pytest.fixture
    def css_file_path(self):
        """Path to main CSS file."""
        return (
            Path(__file__).parent.parent.parent / "gui" / "static" / "css" / "main.css"
        )

    def test_css_file_exists_and_not_empty(self, css_file_path):
        """
        Test CSS file exists and contains styling rules.

        Educational Note:
        CSS presence validation ensures visual styling is available
        for professional appearance of academic interface.
        """
        assert css_file_path.exists(), "Main CSS file does not exist"

        content = css_file_path.read_text(encoding="utf-8")
        assert len(content.strip()) > 0, "CSS file is empty"

        # Check for basic CSS structure
        assert (
            "{" in content and "}" in content
        ), "CSS file does not contain valid CSS rules"

    def test_responsive_design_implementation(self, css_file_path):
        """
        Test responsive design patterns in CSS.

        Educational Note:
        Responsive design testing ensures academic researchers
        can use the interface effectively on various devices.
        """
        content = css_file_path.read_text(encoding="utf-8")

        # Check for media queries
        media_query_patterns = [
            r"@media\s*\([^)]*max-width[^)]*\)",
            r"@media\s*\([^)]*min-width[^)]*\)",
            r"@media\s*screen",
            r"@media\s*\([^)]*device-width[^)]*\)",
        ]

        found_media_queries = any(
            re.search(pattern, content) for pattern in media_query_patterns
        )

        # Also check for flexible units
        flexible_units = ["%", "em", "rem", "vw", "vh", "fr"]
        found_flexible = any(unit in content for unit in flexible_units)

        # Should have either media queries or flexible units for responsiveness
        assert (
            found_media_queries or found_flexible
        ), "No responsive design patterns found in CSS"

    def test_accessibility_css_features(self, css_file_path):
        """
        Test CSS features that support accessibility.

        Educational Note:
        Accessibility CSS ensures inclusive design for researchers
        with visual impairments and other accessibility needs.
        """
        content = css_file_path.read_text(encoding="utf-8")

        # Check for accessibility-friendly CSS properties
        accessibility_properties = [
            "focus",
            "outline",
            "font-size",
            "line-height",
            "contrast",
            "color",
        ]

        found_a11y = sum(
            1 for prop in accessibility_properties if prop in content.lower()
        )
        assert found_a11y >= 3, "Insufficient accessibility-focused CSS properties"

    def test_professional_styling_elements(self, css_file_path):
        """
        Test CSS contains professional styling elements for academic interface.

        Educational Note:
        Professional styling validation ensures the interface meets
        academic standards and provides credible visual presentation.
        """
        content = css_file_path.read_text(encoding="utf-8")

        # Check for professional design elements
        professional_elements = [
            "font-family",
            "margin",
            "padding",
            "border",
            "background",
            "color",
            "transition",
            "box-shadow",
        ]

        found_professional = sum(
            1 for element in professional_elements if element in content.lower()
        )
        assert found_professional >= 5, "Insufficient professional styling elements"

    def test_css_organization_and_structure(self, css_file_path):
        """
        Test CSS organization follows best practices.

        Educational Note:
        CSS organization testing ensures maintainable styling
        and follows professional development practices.
        """
        content = css_file_path.read_text(encoding="utf-8")

        # Check for CSS organization patterns
        organization_indicators = [
            "/*",  # Comments for organization
            "class=",  # Class-based styling
            ":hover",  # Interactive states
            ":focus",  # Accessibility states
        ]

        # CSS should show signs of organization
        found_organization = sum(
            1 for indicator in organization_indicators if indicator in content
        )
        assert found_organization >= 2, "CSS lacks organizational structure"


class TestUIUXPatterns:
    """
    Test suite for UI/UX patterns and user experience elements.

    Educational Notes:
    - Tests user interface patterns specific to academic research tools
    - Validates interaction design and user workflow support
    - Ensures consistent visual hierarchy and information architecture
    """

    @pytest.fixture
    def template_content(self):
        """Content of the main HTML template."""
        template_path = (
            Path(__file__).parent.parent.parent / "gui" / "templates" / "index.html"
        )
        return template_path.read_text(encoding="utf-8")

    @pytest.fixture
    def css_content(self):
        """Content of the main CSS file."""
        css_path = (
            Path(__file__).parent.parent.parent / "gui" / "static" / "css" / "main.css"
        )
        if css_path.exists():
            return css_path.read_text(encoding="utf-8")
        return ""

    def test_navigation_patterns(self, template_content):
        """
        Test navigation patterns appropriate for academic research.

        Educational Note:
        Navigation testing ensures researchers can efficiently
        move through the interface and access key features.
        """
        # Check for navigation elements
        nav_elements = ["<nav", "menu", "navigation", "href=", "button"]

        found_navigation = sum(
            1 for element in nav_elements if element in template_content.lower()
        )
        assert (
            found_navigation >= 2
        ), "Insufficient navigation elements for academic interface"

    def test_content_hierarchy_elements(self, template_content):
        """
        Test content hierarchy elements for academic information.

        Educational Note:
        Content hierarchy testing ensures academic information
        is presented with clear structure and visual organization.
        """
        # Check for heading hierarchy
        heading_pattern = r"<h[1-6]"
        headings_found = len(re.findall(heading_pattern, template_content))

        # Academic content should have clear heading structure
        assert headings_found >= 1, "No heading hierarchy found for academic content"

        # Check for content organization elements
        content_elements = ["<section", "<article", "<div", "class=", "id="]

        found_content_org = sum(
            1 for element in content_elements if element in template_content
        )
        assert found_content_org >= 3, "Insufficient content organization elements"

    def test_interactive_elements(self, template_content):
        """
        Test interactive elements for user engagement.

        Educational Note:
        Interactive element testing ensures researchers can
        effectively interact with academic data and features.
        """
        # Check for interactive elements
        interactive_elements = [
            "<button",
            "<input",
            "<select",
            "<form",
            "onclick=",
            "onchange=",
            'type="button"',
            'type="text"',
        ]

        found_interactive = sum(
            1 for element in interactive_elements if element in template_content.lower()
        )
        assert (
            found_interactive >= 2
        ), "Insufficient interactive elements for academic research interface"

    def test_visual_feedback_patterns(self, css_content):
        """
        Test visual feedback patterns in CSS for user interactions.

        Educational Note:
        Visual feedback testing ensures users receive clear
        indication of their interactions and system state.
        """
        if not css_content:
            pytest.skip("CSS file not available for testing")

        # Check for interactive state styling
        feedback_patterns = [
            ":hover",
            ":focus",
            ":active",
            "transition",
            "transform",
            "opacity",
        ]

        found_feedback = sum(
            1 for pattern in feedback_patterns if pattern in css_content.lower()
        )
        assert found_feedback >= 2, "Insufficient visual feedback patterns in CSS"


class TestPerformanceAndOptimization:
    """
    Test suite for performance and optimization aspects.

    Educational Notes:
    - Tests efficient resource loading and minimal overhead
    - Validates optimized CSS and HTML structure
    - Ensures fast loading for academic research workflows
    """

    @pytest.fixture
    def all_static_files(self):
        """All static files in the GUI."""
        static_path = Path(__file__).parent.parent.parent / "gui" / "static"
        files = []

        for suffix in ["*.css", "*.js", "*.html"]:
            files.extend(static_path.rglob(suffix))

        return files

    def test_file_sizes_are_reasonable(self, all_static_files):
        """
        Test static files have reasonable sizes for web delivery.

        Educational Note:
        File size testing ensures good performance for academic
        researchers with varying internet connection speeds.
        """
        size_limits = {
            ".css": 100 * 1024,  # 100KB limit for CSS
            ".js": 200 * 1024,  # 200KB limit for JavaScript
            ".html": 50 * 1024,  # 50KB limit for HTML
        }

        for file_path in all_static_files:
            file_size = file_path.stat().st_size
            file_extension = file_path.suffix.lower()

            if file_extension in size_limits:
                limit = size_limits[file_extension]
                assert (
                    file_size <= limit
                ), f"File {file_path.name} ({file_size} bytes) exceeds size limit ({limit} bytes)"

    def test_minimal_external_dependencies(self, all_static_files):
        """
        Test minimal external dependencies for faster loading.

        Educational Note:
        Dependency testing ensures the interface loads quickly
        and doesn't rely heavily on external services.
        """
        external_deps = []

        for file_path in all_static_files:
            if file_path.suffix.lower() in [".html", ".css", ".js"]:
                content = file_path.read_text(encoding="utf-8")

                # Check for external CDN links
                external_patterns = [
                    r"https?://cdn\.",
                    r"https?://cdnjs\.",
                    r"https?://unpkg\.",
                    r"https?://jsdelivr\.",
                    r'@import\s+url\s*\(\s*["\']?https?://',
                ]

                for pattern in external_patterns:
                    matches = re.findall(pattern, content)
                    external_deps.extend(matches)

        # Allow some external dependencies but keep them minimal
        assert (
            len(external_deps) <= 5
        ), f"Too many external dependencies: {len(external_deps)}"
