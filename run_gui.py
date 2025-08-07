#!/usr/bin/env python3
"""
Research Paper Concept Explorer - GUI Application Launcher

This script launches the Flask web application for exploring research concepts.
Run this to start the interactive concept visualization interface.

Usage:
    python3 run_gui.py

Then open your browser to http://localhost:5000
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from gui.app import AcademicResearchApp

if __name__ == "__main__":
    app = AcademicResearchApp()
    print("Starting Academic Research Interface...")
    print("Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop the server")

    try:
        # Run with debug mode for development on port 5001 to avoid macOS port conflicts
        app.run(debug=True, host="localhost", port=5001)
    except KeyboardInterrupt:
        print("\n👋 Research interface stopped. Happy researching!")
    except Exception as e:
        print(f"❌ Failed to start application: {str(e)}")
        print("💡 Check your configuration and try again.")
