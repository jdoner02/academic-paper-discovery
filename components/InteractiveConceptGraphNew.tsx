/**
 * InteractiveConceptGraph - Production-ready D3.js visualization of research concepts
 * 
 * This component creates a beautiful, interactive force-directed graph visualization
 * of research concepts extracted from academic papers. It provides filtering,
 * search, and detailed exploration capabilities for understanding research domains.
 * 
 * Educational Notes:
 * - Demonstrates production-ready React + D3.js integration
 * - Shows proper state management for complex visualizations
 * - Implements responsive design and accessibility features
 * - Uses TypeScript for type safety and better developer experience
 * 
 * Features:
 * - Interactive force-directed graph layout
 * - Domain-based color coding and filtering
 * - Search functionality across concept names
 * - Relevance score filtering
 * - Zoom and pan capabilities
 * - Node click for detailed information
 * - Responsive design for all screen sizes
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as d3 from 'd3';
import { ConceptNode, ConceptLink, GraphData } from '../types/conceptGraph';
import { fetchGraphData } from '../services/graphDataService';

// Domain color mapping for consistent visualization
const DOMAIN_COLORS: { [key: string]: string } = {
  'ai_driven_cyber_defense': '#3B82F6',
  'post_quantum_cryptography_implementation': '#8B5CF6',
  'water_infrastructure_incident_response': '#06B6D4',
  'healthcare_privacy_compliance': '#10B981',
  'industrial_iot_security': '#F59E0B',
  'government_ransomware_defense': '#6366F1',
  'local_government_cybersecurity': '#6366F1',
  'medical_device_cybersecurity': '#10B981',
  'water_treatment_scada_security': '#06B6D4',
  'quantum_cryptanalysis_threats': '#8B5CF6',
  'default': '#6B7280'
};

// Research domain display names
const DOMAIN_NAMES: { [key: string]: string } = {
  'ai_driven_cyber_defense': 'AI-Driven Cyber Defense',
  'post_quantum_cryptography_implementation': 'Post-Quantum Cryptography',
  'water_infrastructure_incident_response': 'Water Infrastructure Security',
  'healthcare_privacy_compliance': 'Healthcare Security & Privacy',
  'industrial_iot_security': 'Industrial IoT Security',
  'government_ransomware_defense': 'Government Ransomware Defense',
  'local_government_cybersecurity': 'Local Government Cybersecurity',
  'medical_device_cybersecurity': 'Medical Device Security',
  'water_treatment_scada_security': 'Water Treatment SCADA Security',
  'quantum_cryptanalysis_threats': 'Quantum Cryptanalysis Threats'
};

/**
 * Main InteractiveConceptGraph component
 */
const InteractiveConceptGraph: React.FC = () => {
  // State management
  const svgRef = useRef<SVGSVGElement>(null);
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [minRelevance, setMinRelevance] = useState(0.7);
  const [selectedNode, setSelectedNode] = useState<ConceptNode | null>(null);
  const [availableDomains, setAvailableDomains] = useState<string[]>([]);

  // Debug state rendering
  console.log('🎯 COMPONENT STATE:', { 
    isLoading, 
    error, 
    hasGraphData: graphData.nodes.length > 0, 
    nodeCount: graphData.nodes.length,
    linkCount: graphData.links.length,
    selectedDomain,
    searchTerm,
    minRelevance
  });

  // D3 simulation reference
  const simulationRef = useRef<d3.Simulation<ConceptNode, ConceptLink> | null>(null);

  /**
   * Load concept data from the static JSON file.
   *
   * The heavy lifting is delegated to the {@link fetchGraphData} service which
   * hides the details of talking to the network and validating the response.
   * This keeps the React component focused on rendering, illustrating the
   * Separation of Concerns principle.
   */
  const loadConceptData = async () => {
    console.log('🔄 Starting data load...');
    setIsLoading(true);
    setError(null);

    try {
      // Fetch and validate the dataset. The default URL inside the service
      // uses an absolute path (/data/...), which works regardless of the
      // current route—crucial for Next.js static deployments such as GitHub Pages.
      const data = await fetchGraphData();
      console.log(`✅ Loaded ${data.nodes.length} nodes`);

      setGraphData(data);

      // Derive list of domains for the filter UI. The Array.from + Set pattern
      // demonstrates basic functional programming in TypeScript.
      const domains = Array.from(new Set(data.nodes.map((n) => n.source_domain))).filter(Boolean) as string[];
      setAvailableDomains(domains);
      console.log('🎯 Available domains:', domains);
    } catch (err) {
      console.error('❌ Error loading concept data:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to load concept data';
      setError(errorMessage);
      setGraphData({ nodes: [], links: [] });
    } finally {
      console.log('🏁 Data loading finished, setting loading to false');
      setIsLoading(false);
    }
  };

  /**
   * Filter nodes based on current search and filter criteria
   */
  const filteredNodes = React.useMemo(() => {
    return graphData.nodes.filter((node: ConceptNode) => {
      // Search filter
      if (searchTerm && !node.text.toLowerCase().includes(searchTerm.toLowerCase())) {
        return false;
      }
      
      // Domain filter
      if (selectedDomain !== 'all' && node.source_domain !== selectedDomain) {
        return false;
      }
      
      // Relevance filter
      if (node.relevance_score < minRelevance) {
        return false;
      }
      
      return true;
    });
  }, [graphData.nodes, searchTerm, selectedDomain, minRelevance]);

  /**
   * Filter links to only include connections between visible nodes
   */
  const filteredLinks = React.useMemo(() => {
    const visibleNodeIds = new Set(filteredNodes.map((n: ConceptNode) => n.id));
    return graphData.links.filter((link: ConceptLink) => {
      const sourceId = typeof link.source === 'string' ? link.source : link.source.id;
      const targetId = typeof link.target === 'string' ? link.target : link.target.id;
      return visibleNodeIds.has(sourceId) && visibleNodeIds.has(targetId);
    });
  }, [filteredNodes, graphData.links]);

  /**
   * Initialize and update the D3 force simulation
   */
  const updateVisualization = useCallback(() => {
    console.log('🎨 updateVisualization called:', { 
      hasGraphData: graphData.nodes.length > 0,
      filteredNodesLength: filteredNodes.length,
      filteredLinksLength: filteredLinks.length,
      hasSvgRef: !!svgRef.current 
    });
    
    if (!svgRef.current || filteredNodes.length === 0) {
      console.log('⏭️ Skipping visualization - missing requirements');
      return;
    }
    
    console.log('🎯 Creating D3 visualization...');

    const svg = d3.select(svgRef.current);
    const width = 1200;
    const height = 800;

    // Clear previous visualization
    svg.selectAll('*').remove();

    // Set SVG dimensions
    svg.attr('width', width).attr('height', height);

    // Create zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event: any) => {
        container.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Create main container group
    const container = svg.append('g');

    // Create force simulation
    const simulation = d3.forceSimulation<ConceptNode>(filteredNodes)
      .force('link', d3.forceLink<ConceptNode, ConceptLink>(filteredLinks)
        .id((d: ConceptNode) => d.id)
        .distance((d: ConceptLink) => Math.max(50, 150 / (d.strength || 1)))
        .strength((d: ConceptLink) => (d.strength || 0.5) * 0.7))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius((d: any) => ((d as ConceptNode).size || 10) + 5));

    simulationRef.current = simulation;

    // Create links
    const link = container.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(filteredLinks)
      .enter().append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', (d: ConceptLink) => Math.sqrt((d.strength || 0.5) * 3));

    // Create nodes
    const node = container.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(filteredNodes)
      .enter().append('circle')
      .attr('r', (d: ConceptNode) => Math.max(8, (d.size || 10)))
      .attr('fill', (d: ConceptNode) => d.color || DOMAIN_COLORS[d.source_domain] || DOMAIN_COLORS.default)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', (event: any, d: ConceptNode) => {
        setSelectedNode(d);
      })
      .on('mouseover', function(event: any, d: ConceptNode) {
        d3.select(this).attr('stroke', '#333').attr('stroke-width', 3);
        // Show tooltip
        container.append('text')
          .attr('id', 'tooltip')
          .attr('x', d.x || 0)
          .attr('y', (d.y || 0) - 20)
          .attr('text-anchor', 'middle')
          .attr('fill', '#333')
          .attr('font-size', '12px')
          .attr('font-weight', 'bold')
          .text(d.display_text || d.text);
      })
      .on('mouseout', function() {
        d3.select(this).attr('stroke', '#fff').attr('stroke-width', 2);
        container.select('#tooltip').remove();
      });

    // Add drag behavior
    const drag = d3.drag<SVGCircleElement, ConceptNode>()
      .on('start', (event: any, d: ConceptNode) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on('drag', (event: any, d: ConceptNode) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on('end', (event: any, d: ConceptNode) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });

    node.call(drag);

    // Add labels for important nodes
    const label = container.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(filteredNodes.filter((d: ConceptNode) => d.relevance_score > 0.9))
      .enter().append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '.35em')
      .attr('font-size', '10px')
      .attr('fill', '#333')
      .attr('pointer-events', 'none')
      .text((d: ConceptNode) => d.display_text || d.text);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: ConceptNode) => d.x || 0)
        .attr('cy', (d: ConceptNode) => d.y || 0);

      label
        .attr('x', (d: ConceptNode) => d.x || 0)
        .attr('y', (d: ConceptNode) => d.y || 0);
    });
  }, [filteredNodes, filteredLinks]);

  // Load data on component mount
  useEffect(() => {
    console.log('🚀 useEffect called - about to load concept data');
    loadConceptData();
  }, []); // Remove dependency on loadConceptData

  // Update visualization when filtered data changes
  useEffect(() => {
    updateVisualization();
  }, [updateVisualization]);

  // Handle search input with debouncing
  const debouncedSearch = useCallback(
    debounce((term: string) => setSearchTerm(term), 300),
    []
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600">Loading concept graph...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center max-w-md">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">Failed to Load Data</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={loadConceptData}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with controls */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Research Concept Graph</h1>
              <p className="text-sm text-gray-600">
                Showing {filteredNodes.length} concepts from {availableDomains.length} research domains
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
              {/* Search */}
              <input
                type="text"
                placeholder="Search concepts..."
                className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                onChange={(e) => debouncedSearch(e.target.value)}
              />
              
              {/* Domain filter */}
              <select
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Domains</option>
                {availableDomains.map(domain => (
                  <option key={domain} value={domain}>
                    {DOMAIN_NAMES[domain] || domain.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
              
              {/* Relevance filter - accessible form design */}
              <div className="flex items-center space-x-2">
                <label htmlFor="relevance-slider" className="text-sm text-gray-600">Min Relevance:</label>
                <input
                  id="relevance-slider"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={minRelevance}
                  onChange={(e) => setMinRelevance(parseFloat(e.target.value))}
                  className="w-20"
                  aria-label={`Minimum relevance score: ${minRelevance}`}
                />
                <span className="text-sm text-gray-600 w-8">{minRelevance.toFixed(1)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main visualization area */}
      <div className="flex">
        <div className="flex-1">
          <svg
            ref={svgRef}
            className="w-full"
            style={{ height: 'calc(100vh - 120px)' }}
          />
        </div>
        
        {/* Sidebar for selected node details */}
        {selectedNode && (
          <div className="w-80 bg-white border-l border-gray-200 p-6 overflow-y-auto" style={{ height: 'calc(100vh - 120px)' }}>
            <div className="mb-4">
              <button
                onClick={() => setSelectedNode(null)}
                className="float-right text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {selectedNode.display_text || selectedNode.text}
              </h3>
              <div 
                className="w-4 h-4 rounded-full inline-block mr-2"
                style={{ backgroundColor: selectedNode.color || DOMAIN_COLORS[selectedNode.source_domain] || DOMAIN_COLORS.default }}
              />
              <span className="text-sm text-gray-600">
                {DOMAIN_NAMES[selectedNode.source_domain] || selectedNode.source_domain.replace(/_/g, ' ')}
              </span>
            </div>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Metrics</h4>
                <div className="text-sm text-gray-600 space-y-1">
                  <div>Frequency: {selectedNode.frequency}</div>
                  <div>Relevance: {selectedNode.relevance_score.toFixed(3)}</div>
                  <div>Extraction: {selectedNode.extraction_method}</div>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Source Papers</h4>
                <div className="text-sm text-gray-600 space-y-1">
                  {selectedNode.source_papers.slice(0, 3).map((paper) => (
                    <div key={paper} className="truncate" title={paper}>
                      {paper.replace('local/', '')}
                    </div>
                  ))}
                  {selectedNode.source_papers.length > 3 && (
                    <div className="text-xs text-gray-500">
                      +{selectedNode.source_papers.length - 3} more papers
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Domain legend */}
      <div className="fixed bottom-4 left-4 bg-white rounded-lg shadow-lg p-4 max-w-xs">
        <h4 className="font-semibold text-gray-900 mb-2">Research Domains</h4>
        <div className="grid grid-cols-1 gap-1 text-xs">
          {Object.entries(DOMAIN_COLORS).slice(0, -1).map(([domain, color]) => (
            <div key={domain} className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
              <span className="text-gray-600 truncate">
                {DOMAIN_NAMES[domain] || domain.replace(/_/g, ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Simple debounce function
function debounce<T extends (...args: any[]) => void>(func: T, delay: number): T {
  let timeoutId: NodeJS.Timeout;
  return ((...args: any[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  }) as T;
}

export default InteractiveConceptGraph;
