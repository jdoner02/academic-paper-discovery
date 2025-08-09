#!/usr/bin/env python3
"""
Research Paper Aggregator - Single Executable Launcher

This is the unified entry point for the research paper aggregator that combines:
- Web server for static frontend files
- API endpoints for concept data
- Live concept monitoring and updates
- Auto-browser launching for user convenience

Usage:
    python research_paper_launcher.py
    OR double-click the compiled executable

Educational Notes:
- Demonstrates unified application architecture
- Shows Clean Architecture with embedded web server
- Implements graceful shutdown and error handling
- Provides both GUI and programmatic interfaces
"""

import sys
import os
import json
import time
import threading
import webbrowser
import signal
from pathlib import Path
from typing import Dict, Any, Optional
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import application modules
try:
    from src.educational.atomic_concepts.dag.json_concept_parser import (
        JSONConceptParser,
    )
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError as e:
    print(f"Warning: Some optional features unavailable: {e}")
    JSONConceptParser = None
    Observer = None
    FileSystemEventHandler = None


class ResearchPaperServer:
    """
    Unified server combining static file serving with concept API.

    Educational Notes:
    - Demonstrates single responsibility principle through modular design
    - Shows composition pattern with embedded file handler
    - Implements Observer pattern for live updates
    """

    def __init__(self, port: int = 3001, static_dir: str = "frontend/out"):
        self.port = port
        self.static_dir = Path(static_dir)
        self.server = None
        self.observer = None
        self.concept_parser = None
        self.running = False

        # Initialize concept parser if available
        if JSONConceptParser:
            try:
                self.concept_parser = JSONConceptParser("concept_definitions")
                print("✅ Concept parser initialized successfully")
            except Exception as e:
                print(f"⚠️ Concept parser initialization failed: {e}")

    def setup_file_watcher(self):
        """Set up file system monitoring for live concept updates."""
        if not (Observer and FileSystemEventHandler and self.concept_parser):
            return

        class ConceptFileHandler(FileSystemEventHandler):
            def __init__(self, server_instance):
                self.server = server_instance

            def on_created(self, event):
                if event.src_path.endswith(".json"):
                    print(f"📄 New concept file: {event.src_path}")
                    self.server.update_concept_data()

            def on_modified(self, event):
                if event.src_path.endswith(".json"):
                    print(f"📝 Updated concept file: {event.src_path}")
                    self.server.update_concept_data()

        try:
            self.observer = Observer()
            event_handler = ConceptFileHandler(self)

            # Watch concept directories
            watch_dirs = ["concept_definitions", "data/concept_storage"]
            for watch_dir in watch_dirs:
                if Path(watch_dir).exists():
                    self.observer.schedule(event_handler, watch_dir, recursive=True)
                    print(f"👀 Watching {watch_dir} for changes")

            self.observer.start()
            print("✅ File watcher started successfully")
        except Exception as e:
            print(f"⚠️ File watcher setup failed: {e}")

    def update_concept_data(self):
        """Update concept visualization data."""
        if not self.concept_parser:
            return

        try:
            # Clear caches and reload
            self.concept_parser.concepts_cache.clear()
            self.concept_parser.metadata_cache.clear()
            concepts = self.concept_parser.load_all_concepts()

            # Generate D3 visualization data
            d3_data = self.concept_parser.create_d3_visualization_data()

            # Save to static file for frontend consumption
            output_file = self.static_dir / "concept-graph-data.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w") as f:
                json.dump(d3_data, f, indent=2)

            print(f"📊 Concept data updated: {len(concepts)} concepts loaded")

        except Exception as e:
            print(f"❌ Failed to update concept data: {e}")

    def create_request_handler(self):
        """Create custom HTTP request handler with API and static file serving."""
        static_dir = self.static_dir
        server_instance = self

        class UnifiedRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                # Change to static directory for file serving
                if static_dir.exists():
                    os.chdir(static_dir)
                super().__init__(*args, **kwargs)

            def do_GET(self):
                """Handle GET requests with API routing and static file fallback."""
                path = urlparse(self.path).path

                # API endpoints
                if path == "/api/concepts":
                    self.serve_concepts_api()
                elif path == "/api/health":
                    self.serve_health_api()
                elif path == "/api/status":
                    self.serve_status_api()
                else:
                    # Static file serving with SPA routing support
                    self.serve_static_file(path)

            def serve_concepts_api(self):
                """Serve concept data API endpoint."""
                try:
                    # Load concept data
                    concept_file = static_dir / "concept-graph-data.json"
                    if concept_file.exists():
                        with open(concept_file) as f:
                            data = json.load(f)
                    else:
                        # Fallback: generate on-the-fly
                        if server_instance.concept_parser:
                            data = (
                                server_instance.concept_parser.create_d3_visualization_data()
                            )
                        else:
                            data = {"nodes": [], "links": []}

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())

                except Exception as e:
                    self.send_error(500, f"Concept data error: {str(e)}")

            def serve_health_api(self):
                """Serve health check endpoint."""
                health_data = {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "concept_parser": server_instance.concept_parser is not None,
                    "file_watcher": server_instance.observer is not None,
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(health_data).encode())

            def serve_status_api(self):
                """Serve application status endpoint."""
                try:
                    concept_count = 0
                    if server_instance.concept_parser:
                        concepts = server_instance.concept_parser.load_all_concepts()
                        concept_count = len(concepts)

                    status_data = {
                        "application": "Research Paper Aggregator",
                        "version": "1.0.0",
                        "concept_count": concept_count,
                        "server_port": server_instance.port,
                        "uptime": time.time()
                        - getattr(server_instance, "start_time", time.time()),
                    }

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps(status_data).encode())

                except Exception as e:
                    self.send_error(500, f"Status error: {str(e)}")

            def serve_static_file(self, path):
                """Serve static files with SPA routing support."""
                # Handle root path
                if path == "/":
                    path = "/index.html"

                # Convert to file system path
                file_path = static_dir / path.lstrip("/")

                # If file doesn't exist and it's not an asset, serve index.html (SPA routing)
                if not file_path.exists() and not any(
                    ext in path
                    for ext in [".js", ".css", ".png", ".jpg", ".ico", ".json"]
                ):
                    file_path = static_dir / "index.html"

                if file_path.exists() and file_path.is_file():
                    # Serve the file
                    try:
                        with open(file_path, "rb") as f:
                            content = f.read()

                        self.send_response(200)

                        # Set appropriate content type
                        if file_path.suffix == ".html":
                            self.send_header("Content-Type", "text/html")
                        elif file_path.suffix == ".js":
                            self.send_header("Content-Type", "application/javascript")
                        elif file_path.suffix == ".css":
                            self.send_header("Content-Type", "text/css")
                        elif file_path.suffix == ".json":
                            self.send_header("Content-Type", "application/json")
                        elif file_path.suffix in [".png", ".jpg", ".jpeg"]:
                            self.send_header(
                                "Content-Type", f"image/{file_path.suffix[1:]}"
                            )

                        self.end_headers()
                        self.wfile.write(content)

                    except Exception as e:
                        self.send_error(500, f"File serving error: {str(e)}")
                else:
                    self.send_error(404, "File not found")

            def log_message(self, format, *args):
                """Override to provide cleaner logging."""
                message = format % args
                if not any(skip in message for skip in ["favicon.ico", ".map"]):
                    print(f"🌐 {message}")

        return UnifiedRequestHandler

    def start(self):
        """Start the unified server."""
        print(f"\n🚀 Starting Research Paper Aggregator...")
        print(f"📂 Static files: {self.static_dir}")
        print(f"🔗 Server port: {self.port}")

        self.start_time = time.time()

        # Verify static directory exists
        if not self.static_dir.exists():
            print(f"⚠️ Static directory not found: {self.static_dir}")
            print("   Building frontend first...")
            self.build_frontend()

        # Update concept data initially
        self.update_concept_data()

        # Setup file watcher
        self.setup_file_watcher()

        try:
            # Create and start server
            handler_class = self.create_request_handler()
            self.server = socketserver.TCPServer(("", self.port), handler_class)
            self.server.allow_reuse_address = True

            print(f"✅ Server started successfully on http://localhost:{self.port}")
            print(f"🎯 Opening application in browser...")

            # Open browser after a short delay
            def open_browser():
                time.sleep(1)  # Give server time to start
                try:
                    webbrowser.open(f"http://localhost:{self.port}")
                except Exception as e:
                    print(f"⚠️ Could not open browser automatically: {e}")
                    print(f"   Please manually open: http://localhost:{self.port}")

            threading.Thread(target=open_browser, daemon=True).start()

            # Start serving
            self.running = True
            print("📡 Server is running... Press Ctrl+C to stop")
            self.server.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested by user")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.stop()

    def build_frontend(self):
        """Build the frontend to static files."""
        print("🔨 Building frontend...")
        frontend_dir = Path("frontend")

        if not frontend_dir.exists():
            print("❌ Frontend directory not found")
            return False

        # Change to frontend directory and build
        original_dir = os.getcwd()
        try:
            os.chdir(frontend_dir)

            # Install dependencies if needed
            if not Path("node_modules").exists():
                print("📦 Installing Node.js dependencies...")
                os.system("npm install")

            # Build for export
            print("⚙️ Building Next.js application...")
            result = os.system("npm run build && npm run export")

            if result == 0:
                print("✅ Frontend built successfully")
                return True
            else:
                print("❌ Frontend build failed")
                return False

        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
        finally:
            os.chdir(original_dir)

    def stop(self):
        """Stop the server gracefully."""
        print("🛑 Stopping server...")
        self.running = False

        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("✅ File watcher stopped")

        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("✅ HTTP server stopped")

        print("👋 Research Paper Aggregator stopped")


def main():
    """Main entry point for the unified application."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Research Paper Aggregator - Unified Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start with default settings
  %(prog)s --port 8080        # Use custom port
  %(prog)s --no-browser       # Don't auto-open browser
  %(prog)s --build            # Force rebuild frontend
        """,
    )

    parser.add_argument(
        "--port", type=int, default=3001, help="Port for web server (default: 3001)"
    )

    parser.add_argument(
        "--static-dir",
        default="frontend/out",
        help="Directory containing static files (default: frontend/out)",
    )

    parser.add_argument(
        "--no-browser", action="store_true", help="Don't automatically open browser"
    )

    parser.add_argument(
        "--build", action="store_true", help="Force rebuild frontend before starting"
    )

    args = parser.parse_args()

    # Create and configure server
    server = ResearchPaperServer(port=args.port, static_dir=args.static_dir)

    # Force build if requested
    if args.build:
        server.build_frontend()

    # Handle shutdown signals gracefully
    def signal_handler(signum, frame):
        print(f"\n🔄 Received signal {signum}")
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the server
    try:
        server.start()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
