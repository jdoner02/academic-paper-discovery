"""
Real-time JSON concept loader for D3.js visua            # Save to file that the web            # Save to file for web consumption
            with open(VISUALIZATION_DATA_FILE, 'w') as f:age can fetch
            with open(VISUALIZATION_DATA_FILE, 'w') as f:zation.
Watches for new JSON concept files and automatically updates the graph.
"""

import json
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import http.server
import socketserver
import threading
from typing import Dict, Any

from src.educational.atomic_concepts.dag.json_concept_parser import JSONConceptParser

# Constants
VISUALIZATION_DATA_FILE = "visualization_data.json"


class ConceptFileHandler(FileSystemEventHandler):
    """Handle file system events for concept JSON files."""

    def __init__(self, parser: JSONConceptParser, server_instance):
        self.parser = parser
        self.server = server_instance

    def on_created(self, event):
        if event.src_path.endswith(".json"):
            print(f"New concept file detected: {event.src_path}")
            self.update_visualization()

    def on_modified(self, event):
        if event.src_path.endswith(".json"):
            print(f"Concept file updated: {event.src_path}")
            self.update_visualization()

    def update_visualization(self):
        """Reload concepts and update the visualization data."""
        try:
            # Reload all concepts
            self.parser.concepts_cache.clear()
            self.parser.metadata_cache.clear()
            concepts = self.parser.load_all_concepts()

            # Generate new D3 data
            d3_data = self.parser.create_d3_visualization_data()

            # Save to file that the web page can fetch
            with open("visualization_data.json", "w") as f:
                json.dump(d3_data, f, indent=2)

            print(f"Updated visualization with {len(concepts)} concepts")

        except Exception as e:
            print(f"Error updating visualization: {e}")


class ConceptVisualizationServer:
    """
    HTTP server for the concept visualization with auto-refresh.
    """

    def __init__(self, port: int = 3001):
        self.port = port
        self.parser = JSONConceptParser()
        self.observer = Observer()

    def start_file_watcher(self):
        """Start watching for file changes."""
        event_handler = ConceptFileHandler(self.parser, self)

        # Watch the concept definitions directory
        concepts_path = Path("concept_definitions")
        if concepts_path.exists():
            self.observer.schedule(event_handler, str(concepts_path), recursive=True)

        self.observer.start()
        print(f"Started watching {concepts_path} for changes...")

    def generate_initial_data(self):
        """Generate initial visualization data."""
        try:
            concepts = self.parser.load_all_concepts()
            d3_data = self.parser.create_d3_visualization_data()

            # Save to file for web consumption
            with open(VISUALIZATION_DATA_FILE, "w") as f:
                json.dump(d3_data, f, indent=2)

            print(f"Generated initial data with {len(concepts)} concepts")
            return d3_data

        except Exception as e:
            print(f"Error generating initial data: {e}")
            return {"nodes": [], "links": [], "metadata": {}}

    def create_enhanced_html(self) -> str:
        """Create an enhanced HTML page with auto-refresh capability."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atomic Concept Knowledge Graph - Live Updates</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.2em;
        }
        
        .status {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 8px 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .status.live {
            background: rgba(76, 175, 80, 0.3);
        }
        
        .controls {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,123,255,0.4);
        }
        
        .btn.active {
            background: linear-gradient(135deg, #28a745, #1e7e34);
        }
        
        .visualization-container {
            height: 600px;
            position: relative;
            overflow: hidden;
        }
        
        #graph-svg {
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, #f8f9fa 0%, #e9ecef 100%);
        }
        
        .node {
            cursor: pointer;
            stroke: #fff;
            stroke-width: 3px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
            transition: all 0.3s ease;
        }
        
        .node:hover {
            stroke: #333;
            stroke-width: 4px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));
            transform: scale(1.1);
        }
        
        .link {
            stroke: #999;
            stroke-opacity: 0.6;
            stroke-width: 2px;
            marker-end: url(#arrowhead);
        }
        
        .node-text {
            font-size: 12px;
            font-weight: 600;
            fill: #333;
            text-anchor: middle;
            pointer-events: none;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }
        
        .stats {
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-top: 1px solid #e9ecef;
            text-align: center;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .stat-item {
            background: white;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #007bff;
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 1em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .concept-info {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 500px;
            z-index: 1000;
            display: none;
        }
        
        .concept-info h3 {
            margin-top: 0;
            color: #333;
            font-size: 1.5em;
        }
        
        .auto-refresh {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 123, 255, 0.9);
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
        }
        
        .domain-legend {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 10px;
            font-size: 0.85em;
        }
        
        .domain-legend h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }
        
        .legend-color {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="status live" id="status">🟢 Live Updates</div>
            <h1>Atomic Concept Knowledge Graph</h1>
            <p>Explosive Recursive Decomposition of Mathematical Axioms</p>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="refreshData()">🔄 Refresh Now</button>
            <button class="btn" onclick="togglePhysics()" id="physics-btn">⏸️ Pause Physics</button>
            <button class="btn" onclick="resetZoom()">🎯 Reset View</button>
            <button class="btn" onclick="showAllDomains()">🌐 Show All Domains</button>
            <button class="btn" onclick="focusOnFoundations()">🏗️ Focus on Foundations</button>
        </div>
        
        <div class="visualization-container">
            <svg id="graph-svg">
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                            refX="9" refY="3.5" orient="auto">
                        <polygon points="0 0, 10 3.5, 0 7" fill="#999" />
                    </marker>
                </defs>
                <g class="links"></g>
                <g class="nodes"></g>
                <g class="texts"></g>
            </svg>
            
            <div class="domain-legend" id="domain-legend">
                <h4>Domains</h4>
            </div>
        </div>
        
        <div class="stats">
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-value" id="node-count">0</span>
                    <span class="stat-label">Concepts</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="edge-count">0</span>
                    <span class="stat-label">Dependencies</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="domain-count">0</span>
                    <span class="stat-label">Domains</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="last-update">Never</span>
                    <span class="stat-label">Last Update</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="concept-info" id="concept-info">
        <h3 id="concept-name"></h3>
        <p id="concept-description"></p>
        <p><strong>Level:</strong> <span id="concept-level"></span></p>
        <p><strong>Difficulty:</strong> <span id="concept-difficulty"></span>/10</p>
        <p><strong>Dependencies:</strong> <span id="concept-dependencies"></span></p>
    </div>
    
    <div class="auto-refresh">
        Auto-refresh every 5 seconds
    </div>

    <script>
        // Global variables
        let currentData = null;
        let simulation = null;
        let svg = null;
        let physicsEnabled = true;
        let domainColors = {};
        
        // Color palette for domains
        const colorPalette = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
        ];
        
        // Initialize visualization
        function initVisualization() {
            const container = document.querySelector('.visualization-container');
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            svg = d3.select("#graph-svg")
                .attr("width", width)
                .attr("height", height);
            
            // Create simulation
            simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(d => d.id).distance(100))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("collision", d3.forceCollide().radius(30));
            
            // Add zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.1, 4])
                .on("zoom", (event) => {
                    svg.selectAll("g").attr("transform", event.transform);
                });
            
            svg.call(zoom);
        }
        
        // Load data from server
        async function loadData() {
            try {
                const response = await fetch('/visualization_data.json');
                const data = await response.json();
                
                if (data.nodes && data.nodes.length > 0) {
                    visualizeData(data);
                    updateStatus('🟢 Live - Last updated: ' + new Date().toLocaleTimeString());
                    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
                } else {
                    updateStatus('⚠️ No data available');
                }
            } catch (error) {
                console.error('Error loading data:', error);
                updateStatus('🔴 Connection error');
            }
        }
        
        // Update status indicator
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
        
        // Visualize the data
        function visualizeData(data) {
            currentData = data;
            
            // Assign colors to domains
            const domains = [...new Set(data.nodes.map(n => n.group))];
            domains.forEach((domain, i) => {
                if (!domainColors[domain]) {
                    domainColors[domain] = colorPalette[i % colorPalette.length];
                }
            });
            
            // Update domain legend
            updateDomainLegend(domains);
            
            // Update statistics
            updateStats(data.metadata);
            
            // Prepare nodes with colors
            const nodes = data.nodes.map(d => ({
                ...d,
                color: domainColors[d.group] || '#999'
            }));
            
            const links = data.links;
            
            // Update link elements
            svg.select(".links")
                .selectAll("line")
                .data(links)
                .join("line")
                .attr("class", "link");
            
            // Update node elements
            svg.select(".nodes")
                .selectAll("circle")
                .data(nodes)
                .join("circle")
                .attr("class", "node")
                .attr("r", d => Math.max(8, d.size * 2))
                .attr("fill", d => d.color)
                .on("mouseover", showTooltip)
                .on("mouseout", hideTooltip)
                .on("click", showConceptInfo);
            
            // Update text elements
            svg.select(".texts")
                .selectAll("text")
                .data(nodes)
                .join("text")
                .attr("class", "node-text")
                .text(d => d.name.length > 15 ? d.name.substring(0, 15) + "..." : d.name);
            
            // Update simulation
            simulation.nodes(nodes);
            simulation.force("link").links(links);
            
            // Add drag behavior
            svg.select(".nodes").selectAll("circle")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // Restart simulation
            simulation.alpha(1).restart();
            
            // Update positions on tick
            simulation.on("tick", () => {
                svg.select(".links").selectAll("line")
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
                
                svg.select(".nodes").selectAll("circle")
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
                
                svg.select(".texts").selectAll("text")
                    .attr("x", d => d.x)
                    .attr("y", d => d.y + 4);
            });
        }
        
        function updateDomainLegend(domains) {
            const legend = document.getElementById('domain-legend');
            const existingItems = legend.querySelectorAll('.legend-item');
            existingItems.forEach(item => item.remove());
            
            domains.forEach(domain => {
                const item = document.createElement('div');
                item.className = 'legend-item';
                item.innerHTML = `
                    <div class="legend-color" style="background-color: ${domainColors[domain]}"></div>
                    <span>${domain}</span>
                `;
                legend.appendChild(item);
            });
        }
        
        function updateStats(metadata) {
            document.getElementById('node-count').textContent = metadata.total_concepts || 0;
            document.getElementById('edge-count').textContent = metadata.total_dependencies || 0;
            document.getElementById('domain-count').textContent = metadata.domains ? metadata.domains.length : 0;
        }
        
        function showTooltip(event, d) {
            const tooltip = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("position", "absolute")
                .style("background", "rgba(0,0,0,0.9)")
                .style("color", "white")
                .style("padding", "10px")
                .style("border-radius", "5px")
                .style("font-size", "14px")
                .style("pointer-events", "none")
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px")
                .style("z-index", "1001")
                .html(`<strong>${d.name}</strong><br>${d.description.substring(0, 100)}...`);
        }
        
        function hideTooltip() {
            d3.selectAll(".tooltip").remove();
        }
        
        function showConceptInfo(event, d) {
            const info = document.getElementById('concept-info');
            const dependencies = currentData.links
                .filter(link => link.target === d.id || link.target.id === d.id)
                .map(link => {
                    const sourceId = link.source.id || link.source;
                    const sourceNode = currentData.nodes.find(n => n.id === sourceId);
                    return sourceNode ? sourceNode.name : sourceId;
                })
                .join(", ") || "None";
            
            document.getElementById('concept-name').textContent = d.name;
            document.getElementById('concept-description').textContent = d.description;
            document.getElementById('concept-level').textContent = d.level || 'Unknown';
            document.getElementById('concept-difficulty').textContent = d.difficulty || 'Unknown';
            document.getElementById('concept-dependencies').textContent = dependencies;
            
            info.style.display = 'block';
            
            // Hide after 8 seconds
            setTimeout(() => {
                info.style.display = 'none';
            }, 8000);
        }
        
        // Control functions
        function refreshData() {
            loadData();
        }
        
        function togglePhysics() {
            physicsEnabled = !physicsEnabled;
            const btn = document.getElementById('physics-btn');
            
            if (physicsEnabled) {
                simulation.alpha(0.3).restart();
                btn.textContent = '⏸️ Pause Physics';
                btn.classList.remove('active');
            } else {
                simulation.stop();
                btn.textContent = '▶️ Start Physics';
                btn.classList.add('active');
            }
        }
        
        function resetZoom() {
            const container = document.querySelector('.visualization-container');
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            svg.transition()
                .duration(750)
                .call(d3.zoom().transform, d3.zoomIdentity.translate(width/2, height/2).scale(1));
        }
        
        function showAllDomains() {
            svg.select(".nodes").selectAll("circle").style("opacity", 1);
            svg.select(".texts").selectAll("text").style("opacity", 1);
            svg.select(".links").selectAll("line").style("opacity", 0.6);
        }
        
        function focusOnFoundations() {
            svg.select(".nodes").selectAll("circle")
                .style("opacity", d => d.group === 'logic' || d.group === 'set_theory' ? 1 : 0.3);
            svg.select(".texts").selectAll("text")
                .style("opacity", d => d.group === 'logic' || d.group === 'set_theory' ? 1 : 0.3);
            svg.select(".links").selectAll("line").style("opacity", 0.3);
        }
        
        // Drag handlers
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        
        // Initialize and start auto-refresh
        window.addEventListener('load', () => {
            initVisualization();
            loadData();
            
            // Auto-refresh every 5 seconds
            setInterval(loadData, 5000);
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            initVisualization();
            if (currentData) {
                visualizeData(currentData);
            }
        });
        
        // Close concept info when clicking outside
        document.addEventListener('click', (event) => {
            const info = document.getElementById('concept-info');
            if (!info.contains(event.target) && !event.target.closest('.node')) {
                info.style.display = 'none';
            }
        });
    </script>
</body>
</html>"""

    def start_server(self):
        """Start the HTTP server with live concept visualization."""

        class ConceptRequestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/" or self.path == "/index.html":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(self.server.html_content.encode())
                elif self.path == f"/{VISUALIZATION_DATA_FILE}":
                    try:
                        with open(VISUALIZATION_DATA_FILE, "r") as f:
                            data = f.read()
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(data.encode())
                    except FileNotFoundError:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(b'{"nodes": [], "links": [], "metadata": {}}')
                else:
                    super().do_GET()

        # Generate initial data
        self.generate_initial_data()

        # Start file watcher
        self.start_file_watcher()

        # Start HTTP server
        with socketserver.TCPServer(("", self.port), ConceptRequestHandler) as httpd:
            httpd.html_content = self.create_enhanced_html()
            print(
                f"🚀 Concept Visualization Server running at http://localhost:{self.port}"
            )
            print(
                "📊 Real-time updates enabled - add new JSON files to see them appear instantly!"
            )

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server...")
                self.observer.stop()
                self.observer.join()


if __name__ == "__main__":
    server = ConceptVisualizationServer()
    server.start_server()
