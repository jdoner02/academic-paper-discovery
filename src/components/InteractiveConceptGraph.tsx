/**
 * InteractiveConceptGraph - Beautiful and intuitive concept graph visualization
 * 
 * This component transforms the research paper discovery platform into an interactive
 * concept exploration tool, allowing users to navigate through research domains and
 * discover connections between concepts, papers, and research areas.
 * 
 * Educational Notes:
 * - Demonstrates D3.js integration with React for data visualization
 * - Shows force-directed graph algorithms for natural layout
 * - Implements interactive filtering and search capabilities  
 * - Uses modern React patterns (hooks, context, suspense)
 * - Responsive design for desktop and mobile research workflows
 * 
 * Design Decisions:
 * - Force-directed layout for organic concept clustering
 * - Color coding by research domain for quick visual recognition
 * - Node sizes proportional to concept relevance/frequency
 * - Interactive zoom, pan, and node selection for exploration
 * - Sidebar details panel for deep-dive into selected concepts
 * - Search and filter controls for focused exploration
 * 
 * Use Cases:
 * - Research literature discovery and exploration
 * - Understanding concept relationships across papers
 * - Identifying knowledge gaps and research opportunities
 * - Educational tool for learning research methodologies
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as d3 from 'd3';
import { debounce } from 'lodash';

// Type definitions for our concept graph data
interface ConceptNode {
  id: string;
  text: string;
  frequency: number;
  relevance_score: number;
  source_domain: string;
  source_papers: string[];
  extraction_method: string;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface ConceptLink {
  source: string | ConceptNode;
  target: string | ConceptNode;
  strength: number;
  relationship_type: string;
}

interface GraphData {
  nodes: ConceptNode[];
  links: ConceptLink[];
}

interface SelectedConcept extends ConceptNode {
  connectedNodes: ConceptNode[];
  connectedPapers: string[];
}

// Color scheme for different research domains
const DOMAIN_COLORS = {
  'ai_driven_cyber_defense': '#3B82F6',      // Blue
  'quantum_cryptography': '#8B5CF6',        // Purple  
  'water_infrastructure': '#06B6D4',        // Cyan
  'healthcare_security': '#10B981',         // Green
  'iot_security': '#F59E0B',                // Orange
  'post_quantum_crypto': '#EF4444',         // Red
  'government_security': '#6366F1',         // Indigo
  'critical_infrastructure': '#84CC16',     // Lime
  'default': '#6B7280'                      // Gray
};

const RESEARCH_DOMAINS = [
  { id: 'ai_driven_cyber_defense', name: 'AI-Driven Cyber Defense', color: DOMAIN_COLORS['ai_driven_cyber_defense'] },
  { id: 'post_quantum_cryptography_implementation', name: 'Post-Quantum Cryptography', color: DOMAIN_COLORS['post_quantum_crypto'] },
  { id: 'water_infrastructure_incident_response', name: 'Water Infrastructure Security', color: DOMAIN_COLORS['water_infrastructure'] },
  { id: 'healthcare_privacy_compliance', name: 'Healthcare Security', color: DOMAIN_COLORS['healthcare_security'] },
  { id: 'industrial_iot_security', name: 'IoT Security', color: DOMAIN_COLORS['iot_security'] },
  { id: 'local_government_cybersecurity', name: 'Government Security', color: DOMAIN_COLORS['government_security'] }
];

/**
 * Main InteractiveConceptGraph component
 */
const InteractiveConceptGraph: React.FC = () => {
  // State management for the visualization
  const svgRef = useRef<SVGSVGElement>(null);
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [selectedConcept, setSelectedConcept] = useState<SelectedConcept | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [minRelevance, setMinRelevance] = useState(0.5);

  // D3 simulation reference
  const simulationRef = useRef<d3.Simulation<ConceptNode, ConceptLink> | null>(null);

  /**
   * Load concept data from the API endpoint
   */
  const loadConceptData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/concepts');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setGraphData({ 
        nodes: data.nodes || [], 
        links: data.links || [] 
      });
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load concept data');
      
      // Fallback to mock data for development
      console.warn('Failed to load from API, using mock data:', err);
      
      const mockNodes: ConceptNode[] = [
        {
          id: 'neural-networks',
          text: 'Neural Networks',
          frequency: 126,
          relevance_score: 0.89,
          source_domain: 'ai_driven_cyber_defense',
          source_papers: ['Synergistic Approach in Network Intrusion Detection'],
          extraction_method: 'tfidf'
        },
        {
          id: 'quantum-cryptography',
          text: 'Quantum Cryptography',
          frequency: 95,
          relevance_score: 0.95,
          source_domain: 'post_quantum_cryptography_implementation',
          source_papers: ['Post-Quantum Cryptography Implementation'],
          extraction_method: 'embedding'
        },
        {
          id: 'intrusion-detection',
          text: 'Intrusion Detection',
          frequency: 130,
          relevance_score: 0.92,
          source_domain: 'ai_driven_cyber_defense',
          source_papers: ['Network Intrusion Detection Systems'],
          extraction_method: 'tfidf'
        },
        {
          id: 'iot-security',
          text: 'IoT Security',
          frequency: 88,
          relevance_score: 0.87,
          source_domain: 'industrial_iot_security',
          source_papers: ['Industrial IoT Security Framework'],
          extraction_method: 'statistical'
        },
        {
          id: 'water-infrastructure',
          text: 'Water Infrastructure',
          frequency: 67,
          relevance_score: 0.85,
          source_domain: 'water_infrastructure_incident_response',
          source_papers: ['Critical Water Infrastructure Protection'],
          extraction_method: 'embedding'
        },
        {
          id: 'machine-learning',
          text: 'Machine Learning',
          frequency: 145,
          relevance_score: 0.93,
          source_domain: 'ai_driven_cyber_defense',
          source_papers: ['ML for Cybersecurity Applications'],
          extraction_method: 'tfidf'
        },
        {
          id: 'encryption',
          text: 'Encryption',
          frequency: 112,
          relevance_score: 0.88,
          source_domain: 'post_quantum_cryptography_implementation',
          source_papers: ['Advanced Encryption Standards'],
          extraction_method: 'statistical'
        },
        {
          id: 'healthcare-security',
          text: 'Healthcare Security',
          frequency: 76,
          relevance_score: 0.84,
          source_domain: 'healthcare_privacy_compliance',
          source_papers: ['HIPAA Compliance in Digital Health'],
          extraction_method: 'embedding'
        }
      ];

      const mockLinks: ConceptLink[] = [
        { source: 'neural-networks', target: 'machine-learning', strength: 0.8, relationship_type: 'implements' },
        { source: 'intrusion-detection', target: 'machine-learning', strength: 0.7, relationship_type: 'uses' },
        { source: 'neural-networks', target: 'intrusion-detection', strength: 0.9, relationship_type: 'enables' },
        { source: 'quantum-cryptography', target: 'encryption', strength: 0.95, relationship_type: 'enhances' },
        { source: 'iot-security', target: 'intrusion-detection', strength: 0.6, relationship_type: 'requires' },
        { source: 'water-infrastructure', target: 'iot-security', strength: 0.7, relationship_type: 'depends_on' },
        { source: 'healthcare-security', target: 'encryption', strength: 0.8, relationship_type: 'requires' }
      ];

      setGraphData({ nodes: mockNodes, links: mockLinks });
    } finally {
      setIsLoading(false);
    }
  }, []);

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
    if (!svgRef.current || filteredNodes.length === 0) return;

    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 600;

    // Clear previous visualization
    svg.selectAll('*').remove();

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
        .distance((d: ConceptLink) => 100 / d.strength)
        .strength((d: ConceptLink) => d.strength))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30));

    simulationRef.current = simulation;

    // Create links
    const link = container.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(filteredLinks)
      .enter().append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', (d: ConceptLink) => Math.sqrt(d.strength * 5));

    // Create nodes
    const node = container.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(filteredNodes)
      .enter().append('circle')
      .attr('r', (d: ConceptNode) => Math.sqrt(d.frequency) / 2 + 5)
      .attr('fill', (d: ConceptNode) => (DOMAIN_COLORS as any)[d.source_domain] || DOMAIN_COLORS.default)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .call(d3.drag<SVGCircleElement, ConceptNode>()
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
        }))
      .on('click', (event: any, d: ConceptNode) => {
        // Find connected nodes and papers
        const connectedNodeIds = new Set<string>();
        filteredLinks.forEach(link => {
          const sourceId = typeof link.source === 'string' ? link.source : link.source.id;
          const targetId = typeof link.target === 'string' ? link.target : link.target.id;
          
          if (sourceId === d.id) connectedNodeIds.add(targetId);
          if (targetId === d.id) connectedNodeIds.add(sourceId);
        });

        const connectedNodes = filteredNodes.filter(n => connectedNodeIds.has(n.id));
        const connectedPapers = [...new Set([...d.source_papers, ...connectedNodes.flatMap(n => n.source_papers)])];

        setSelectedConcept({
          ...d,
          connectedNodes,
          connectedPapers
        });
      });

    // Create node labels
    const label = container.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(filteredNodes)
      .enter().append('text')
      .text((d: ConceptNode) => d.text)
      .attr('font-size', '12px')
      .attr('fill', '#333')
      .attr('text-anchor', 'middle')
      .attr('dy', -15)
      .style('pointer-events', 'none');

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => (d.source as ConceptNode).x!)
        .attr('y1', d => (d.source as ConceptNode).y!)
        .attr('x2', d => (d.target as ConceptNode).x!)
        .attr('y2', d => (d.target as ConceptNode).y!);

      node
        .attr('cx', d => d.x!)
        .attr('cy', d => d.y!);

      label
        .attr('x', d => d.x!)
        .attr('y', d => d.y!);
    });

    // Add hover effects
    node
      .on('mouseenter', function(event: any, d: ConceptNode) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', Math.sqrt(d.frequency) / 2 + 8)
          .attr('stroke-width', 3);
      })
      .on('mouseleave', function(event: any, d: ConceptNode) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', Math.sqrt(d.frequency) / 2 + 5)
          .attr('stroke-width', 2);
      });

  }, [filteredNodes, filteredLinks]);

  // Debounced search to avoid excessive filtering
  const debouncedSearch = useCallback(
    debounce((term: string) => setSearchTerm(term), 300),
    []
  );

  // Load data on component mount
  useEffect(() => {
    loadConceptData();
  }, [loadConceptData]);

  // Update visualization when filtered data changes
  useEffect(() => {
    updateVisualization();
  }, [updateVisualization]);

  // Cleanup simulation on unmount
  useEffect(() => {
    return () => {
      if (simulationRef.current) {
        simulationRef.current.stop();
      }
    };
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">Loading research concept graph...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-lg font-semibold text-red-800 mb-2">Error Loading Concepts</h3>
          <p className="text-red-600">{error}</p>
          <button 
            onClick={loadConceptData}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Research Concept Graph</h1>
          <p className="text-gray-600">Explore connections between research concepts and papers</p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Control Panel */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Search */}
            <div className="bg-white rounded-lg shadow p-4">
              <label htmlFor="search-input" className="block text-sm font-medium text-gray-700 mb-2">
                Search Concepts
              </label>
              <input
                id="search-input"
                type="text"
                placeholder="Enter concept name..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                onChange={(e) => debouncedSearch(e.target.value)}
              />
            </div>

            {/* Domain Filter */}
            <div className="bg-white rounded-lg shadow p-4">
              <label htmlFor="domain-select" className="block text-sm font-medium text-gray-700 mb-2">
                Research Domain
              </label>
              <select
                id="domain-select"
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Domains</option>
                {RESEARCH_DOMAINS.map(domain => (
                  <option key={domain.id} value={domain.id}>
                    {domain.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Relevance Filter */}
            <div className="bg-white rounded-lg shadow p-4">
              <label htmlFor="relevance-slider" className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Relevance: {minRelevance.toFixed(2)}
              </label>
              <input
                id="relevance-slider"
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={minRelevance}
                onChange={(e) => setMinRelevance(parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Legend */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Domain Colors</h3>
              <div className="space-y-2">
                {RESEARCH_DOMAINS.map(domain => (
                  <div key={domain.id} className="flex items-center">
                    <div 
                      className="w-4 h-4 rounded-full mr-2"
                      style={{ backgroundColor: domain.color }}
                    ></div>
                    <span className="text-xs text-gray-600">{domain.name}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Statistics */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Graph Statistics</h3>
              <div className="space-y-1 text-sm text-gray-600">
                <div>Concepts: {filteredNodes.length}</div>
                <div>Connections: {filteredLinks.length}</div>
                <div>Domains: {new Set(filteredNodes.map(n => n.source_domain)).size}</div>
              </div>
            </div>
          </div>

          {/* Main Visualization */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow">
              
              {/* Graph Container */}
              <div className="p-4">
                <svg 
                  ref={svgRef}
                  width="100%"
                  height="600"
                  viewBox="0 0 800 600"
                  className="border border-gray-200 rounded"
                >
                </svg>
              </div>

              {/* Selected Concept Details */}
              {selectedConcept && (
                <div className="border-t border-gray-200 p-4 bg-gray-50">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {selectedConcept.text}
                    </h3>
                    <button
                      onClick={() => setSelectedConcept(null)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ✕
                    </button>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Concept Details</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        <div>Frequency: {selectedConcept.frequency}</div>
                        <div>Relevance: {selectedConcept.relevance_score.toFixed(3)}</div>
                        <div>Domain: {selectedConcept.source_domain.replace(/_/g, ' ')}</div>
                        <div>Method: {selectedConcept.extraction_method}</div>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Connected Concepts</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        {selectedConcept.connectedNodes.map(node => (
                          <div key={node.id} className="truncate">
                            • {node.text}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {selectedConcept.connectedPapers.length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-medium text-gray-700 mb-2">Related Papers</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        {selectedConcept.connectedPapers.slice(0, 3).map(paper => (
                          <div key={paper} className="truncate">
                            📄 {paper}
                          </div>
                        ))}
                        {selectedConcept.connectedPapers.length > 3 && (
                          <div className="text-blue-600">
                            +{selectedConcept.connectedPapers.length - 3} more papers
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InteractiveConceptGraph;
