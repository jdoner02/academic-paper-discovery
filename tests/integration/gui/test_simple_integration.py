"""
Simple integration test to verify TDD approach works.
"""

import pytest


class TestSimpleIntegration:
    """Simple test to verify test discovery works"""

    def test_simple_assertion(self):
        """Simple test that always passes"""
        assert True

    def test_import_gui(self):
        """Test that we can import GUI components"""
        from gui.app import create_app

        app = create_app()
        assert app is not None
