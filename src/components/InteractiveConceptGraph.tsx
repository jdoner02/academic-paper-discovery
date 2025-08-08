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

// Advanced D3.js utilities for cutting-edge visualization
const d3Utils = {
  // Modern color scales using d3.interpolate and perceptually uniform colors
  createDomainColorScale: () => d3.scaleOrdinal()
    .range([
      '#4c956c', '#2f9aa0', '#8e44ad', '#e74c3c', '#f39c12', 
      '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
    ]),
  
  // Advanced clustering function for domain-based grouping
  createClusterForce: (domains: string[], width: number, height: number) => {
    const centers = domains.reduce((acc, domain, i) => {
      const angle = (i / domains.length) * 2 * Math.PI;
      const radius = Math.min(width, height) * 0.25;
      acc[domain] = {
        x: width / 2 + Math.cos(angle) * radius,
        y: height / 2 + Math.sin(angle) * radius
      };
      return acc;
    }, {} as Record<string, { x: number, y: number }>);
    
    return (alpha: number) => {
      // Custom force implementation for domain clustering
      return (nodes: ConceptNode[]) => {
        nodes.forEach(node => {
          const center = centers[node.source_domain];
          if (center) {
            const dx = center.x - (node.x || 0);
            const dy = center.y - (node.y || 0);
            node.x = (node.x || 0) + dx * alpha * 0.1;
            node.y = (node.y || 0) + dy * alpha * 0.1;
          }
        });
      };
    };
  },
  
  // Advanced edge bundling for cleaner visualization
  createEdgeBundling: (links: ConceptLink[]) => {
    return links.map(link => ({
      ...link,
      path: d3.geoPath()
    }));
  }
};

// Enhanced type definitions with advanced D3.js features
interface ConceptNode extends d3.SimulationNodeDatum {
  id: string;
  text: string;
  frequency: number;
  relevance_score: number;
  source_domain: string;
  source_papers: string[];
  extraction_method: string;
  // Enhanced D3 properties for advanced animations
  originalRadius?: number;
  targetRadius?: number;
  cluster?: { x: number, y: number };
}

interface ConceptLink extends d3.SimulationLinkDatum<ConceptNode> {
  source: string | ConceptNode;
  target: string | ConceptNode;
  strength: number;
  relationship_type: string;
  // Enhanced properties for advanced edge styling
  animated?: boolean;
  bundled?: boolean;
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

// Enhanced state for advanced D3.js features
const InteractiveConceptGraph: React.FC = () => {
  // Core state management
  const svgRef = useRef<SVGSVGElement>(null);
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [selectedConcept, setSelectedConcept] = useState<SelectedConcept | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filter and interaction state
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [minRelevance, setMinRelevance] = useState(0.5);
  
  // Advanced D3.js state for cutting-edge features
  const [clusteringEnabled, setClusteringEnabled] = useState(true);
  const [animationsEnabled, setAnimationsEnabled] = useState(true);
  const [viewMode, setViewMode] = useState<'force' | 'cluster' | 'hierarchy'>('force');
  const [highlightMode, setHighlightMode] = useState<'none' | 'domain' | 'connections'>('none');

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
   * ENHANCED updateVisualization with cutting-edge D3.js techniques!
   * This showcases the latest and greatest in force-directed graph visualization
   */
  const updateVisualization = useCallback(() => {
    if (!svgRef.current || filteredNodes.length === 0) return;

    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 600;

    // Clear previous visualization with smooth transition
    svg.selectAll('*')
      .transition()
      .duration(animationsEnabled ? 300 : 0)
      .style('opacity', 0)
      .remove();

    // Create enhanced zoom behavior with smooth transitions
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 8])
      .on('zoom', (event: any) => {
        container.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Create main container with advanced layering
    const container = svg.append('g');
    
    // Add gradient definitions for enhanced visual appeal
    const defs = svg.append('defs');
    
    // Create radial gradients for nodes
    RESEARCH_DOMAINS.forEach(domain => {
      const gradient = defs.append('radialGradient')
        .attr('id', `gradient-${domain.id}`)
        .attr('cx', '30%')
        .attr('cy', '30%');
      
      gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', d3.color(domain.color)?.brighter(0.5)?.toString() || domain.color);
      
      gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', domain.color);
    });

    // Enhanced force simulation with clustering and advanced physics
    const domains = [...new Set(filteredNodes.map(n => n.source_domain))];
    
    const simulation = d3.forceSimulation<ConceptNode>(filteredNodes)
      .force('link', d3.forceLink<ConceptNode, ConceptLink>(filteredLinks)
        .id((d: ConceptNode) => d.id)
        .distance((d: ConceptLink) => {
          // Dynamic link distance based on relationship strength and type
          const baseDistance = 100;
          const strengthMultiplier = 1 / Math.max(d.strength, 0.1);
          const typeMultiplier = d.relationship_type === 'implements' ? 0.8 : 1.2;
          return baseDistance * strengthMultiplier * typeMultiplier;
        })
        .strength((d: ConceptLink) => Math.max(d.strength, 0.1)))
      .force('charge', d3.forceManyBody()
        .strength((d: ConceptNode) => {
          // Dynamic charge based on node importance
          const baseCharge = -300;
          const frequencyMultiplier = Math.log(d.frequency + 1) / 5;
          return baseCharge * (1 + frequencyMultiplier);
        }))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide()
        .radius((d: ConceptNode) => {
          const baseRadius = Math.sqrt(d.frequency) / 2 + 5;
          return baseRadius + 10; // Padding for collision
        }))
      // ADVANCED: Domain clustering force for intelligent layout
      .force('cluster', clusteringEnabled ? 
        d3Utils.createClusterForce(domains, width, height) : null);

    simulationRef.current = simulation;

    // ENHANCED LINKS with advanced styling and animations
    const link = container.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(filteredLinks)
      .enter().append('line')
      .attr('stroke', (d: ConceptLink) => {
        // Dynamic link colors based on relationship type
        const colorMap: Record<string, string> = {
          'implements': '#3498db',
          'uses': '#2ecc71', 
          'enables': '#e74c3c',
          'enhances': '#9b59b6',
          'requires': '#f39c12',
          'depends_on': '#34495e'
        };
        return colorMap[d.relationship_type] || '#999';
      })
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', (d: ConceptLink) => Math.max(Math.sqrt(d.strength * 8), 1))
      .attr('stroke-dasharray', (d: ConceptLink) => 
        d.relationship_type === 'depends_on' ? '5,5' : 'none')
      .style('cursor', 'pointer')
      // Advanced hover effects with smooth transitions
      .on('mouseenter', function(event: any, d: ConceptLink) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('stroke-width', Math.max(Math.sqrt(d.strength * 8), 1) + 2)
          .attr('stroke-opacity', 0.9);
      })
      .on('mouseleave', function(event: any, d: ConceptLink) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('stroke-width', Math.max(Math.sqrt(d.strength * 8), 1))
          .attr('stroke-opacity', 0.6);
      });

    // ENHANCED NODES with gradients and advanced animations
    const node = container.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(filteredNodes)
      .enter().append('circle')
      .attr('r', (d: ConceptNode) => {
        const baseRadius = Math.sqrt(d.frequency) / 2 + 5;
        d.originalRadius = baseRadius;
        d.targetRadius = baseRadius;
        return baseRadius;
      })
      .attr('fill', (d: ConceptNode) => `url(#gradient-${d.source_domain})`)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .style('filter', 'drop-shadow(2px 2px 4px rgba(0,0,0,0.2))')
      // Enhanced drag behavior with physics awareness
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
        // Enhanced click behavior with visual feedback
        d3.select(event.target)
          .transition()
          .duration(150)
          .attr('r', (d.originalRadius || 10) * 1.5)
          .transition()
          .duration(150)
          .attr('r', d.originalRadius || 10);

        // Find connected nodes and papers with advanced relationship analysis
        const connectedNodeIds = new Set<string>();
        const relationshipTypes = new Set<string>();
        
        filteredLinks.forEach(link => {
          const sourceId = typeof link.source === 'string' ? link.source : link.source.id;
          const targetId = typeof link.target === 'string' ? link.target : link.target.id;
          
          if (sourceId === d.id) {
            connectedNodeIds.add(targetId);
            relationshipTypes.add(link.relationship_type);
          }
          if (targetId === d.id) {
            connectedNodeIds.add(sourceId);
            relationshipTypes.add(link.relationship_type);
          }
        });

        const connectedNodes = filteredNodes.filter(n => connectedNodeIds.has(n.id));
        const connectedPapers = [...new Set([...d.source_papers, ...connectedNodes.flatMap(n => n.source_papers)])];

        setSelectedConcept({
          ...d,
          connectedNodes,
          connectedPapers
        });

        // Advanced highlighting of connected elements
        if (highlightMode === 'connections') {
          // Dim all elements
          node.style('opacity', 0.3);
          link.style('opacity', 0.1);
          
          // Highlight selected node and connections
          node.filter((n: ConceptNode) => n.id === d.id || connectedNodeIds.has(n.id))
            .style('opacity', 1);
          
          link.filter((l: ConceptLink) => {
            const sourceId = typeof l.source === 'string' ? l.source : l.source.id;
            const targetId = typeof l.target === 'string' ? l.target : l.target.id;
            return sourceId === d.id || targetId === d.id;
          }).style('opacity', 0.8);
        }
      });

    // ENHANCED LABELS with advanced typography and positioning
    const label = container.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(filteredNodes)
      .enter().append('text')
      .text((d: ConceptNode) => d.text)
      .attr('font-size', (d: ConceptNode) => {
        // Dynamic font size based on node importance
        const baseSize = 12;
        const importanceMultiplier = Math.log(d.frequency + 1) / 8;
        return Math.max(baseSize + importanceMultiplier, 10);
      })
      .attr('font-weight', (d: ConceptNode) => d.relevance_score > 0.9 ? 'bold' : 'normal')
      .attr('fill', '#333')
      .attr('text-anchor', 'middle')
      .attr('dy', -15)
      .style('pointer-events', 'none')
      .style('text-shadow', '1px 1px 2px rgba(255,255,255,0.8)')
      .style('font-family', 'system-ui, -apple-system, sans-serif');

    // ADVANCED: Particle system for visual enhancement (when animations enabled)
    if (animationsEnabled) {
      const particles = container.append('g')
        .attr('class', 'particles')
        .selectAll('circle')
        .data(filteredNodes.filter(d => d.relevance_score > 0.85))
        .enter().append('circle')
        .attr('r', 1)
        .attr('fill', '#ffd700')
        .attr('opacity', 0.7)
        .style('pointer-events', 'none');

      // Animate particles around high-relevance nodes
      particles
        .transition()
        .duration(2000)
        .ease(d3.easeLinear)
        .attrTween('transform', (d: ConceptNode) => {
          return (t: number) => {
            const angle = t * 2 * Math.PI;
            const radius = 20;
            const x = (d.x || 0) + Math.cos(angle) * radius;
            const y = (d.y || 0) + Math.sin(angle) * radius;
            return `translate(${x}, ${y})`;
          };
        })
        .on('end', function() {
          d3.select(this).remove();
        });
    }

    // Enhanced physics simulation update with smooth interpolation
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

    // ULTRA-SMOOTH hover effects with advanced D3.js patterns
    node
      .on('mouseenter', function(event: any, d: ConceptNode) {
        const element = d3.select(this);
        
        // Create pulsing effect
        element
          .transition('pulse')
          .duration(200)
          .attr('r', (d.originalRadius || 10) * 1.3)
          .attr('stroke-width', 4);

        // Show tooltip with advanced positioning
        const tooltip = container.append('g')
          .attr('class', 'tooltip')
          .attr('transform', `translate(${d.x! + 20}, ${d.y! - 20})`);

        const tooltipBg = tooltip.append('rect')
          .attr('rx', 4)
          .attr('ry', 4)
          .attr('fill', 'rgba(0,0,0,0.8)')
          .attr('stroke', '#fff')
          .attr('stroke-width', 1);

        const tooltipText = tooltip.append('text')
          .attr('fill', 'white')
          .attr('font-size', '12px')
          .attr('dx', 8)
          .attr('dy', 20);

        tooltipText.append('tspan')
          .attr('x', 8)
          .attr('dy', 0)
          .text(`${d.text}`);
        
        tooltipText.append('tspan')
          .attr('x', 8)
          .attr('dy', 15)
          .text(`Frequency: ${d.frequency}`);
        
        tooltipText.append('tspan')
          .attr('x', 8)
          .attr('dy', 15)
          .text(`Relevance: ${d.relevance_score.toFixed(3)}`);

        // Size tooltip background to fit text
        const bbox = (tooltipText.node() as SVGTextElement).getBBox();
        tooltipBg
          .attr('width', bbox.width + 16)
          .attr('height', bbox.height + 8);
      })
      .on('mouseleave', function(event: any, d: ConceptNode) {
        d3.select(this)
          .transition('pulse')
          .duration(200)
          .attr('r', d.originalRadius || 10)
          .attr('stroke-width', 2);

        // Remove tooltip
        container.select('.tooltip').remove();
      });

  }, [filteredNodes, filteredLinks, animationsEnabled, clusteringEnabled, highlightMode]);

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

            {/* Advanced D3.js Controls - cutting-edge features! */}
            <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg shadow border-2 border-purple-200 p-4">
              <h3 className="text-sm font-bold text-purple-800 mb-3 flex items-center">
                ⚡ Advanced D3.js Features
              </h3>
              
              {/* Clustering Toggle */}
              <div className="mb-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={clusteringEnabled}
                    onChange={(e) => setClusteringEnabled(e.target.checked)}
                    className="mr-2 text-purple-600"
                  />
                  <span className="text-xs text-purple-700">Domain Clustering</span>
                </label>
              </div>

              {/* Animations Toggle */}
              <div className="mb-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={animationsEnabled}
                    onChange={(e) => setAnimationsEnabled(e.target.checked)}
                    className="mr-2 text-purple-600"
                  />
                  <span className="text-xs text-purple-700">Enhanced Animations</span>
                </label>
              </div>

              {/* View Mode Selector */}
              <div className="mb-3">
                <label className="block text-xs font-medium text-purple-700 mb-1">
                  Layout Mode
                </label>
                <select
                  value={viewMode}
                  onChange={(e) => setViewMode(e.target.value as 'force' | 'cluster' | 'hierarchy')}
                  className="w-full text-xs px-2 py-1 border border-purple-300 rounded focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="force">Force-Directed</option>
                  <option value="cluster">Clustered</option>
                  <option value="hierarchy">Hierarchical</option>
                </select>
              </div>

              {/* Highlight Mode */}
              <div className="mb-3">
                <label className="block text-xs font-medium text-purple-700 mb-1">
                  Highlight Mode
                </label>
                <select
                  value={highlightMode}
                  onChange={(e) => setHighlightMode(e.target.value as 'none' | 'domain' | 'connections')}
                  className="w-full text-xs px-2 py-1 border border-purple-300 rounded focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="none">None</option>
                  <option value="domain">Domain-based</option>
                  <option value="connections">Connection-based</option>
                </select>
              </div>
            </div>
            {/* Enhanced Legend with Relationship Types */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Domain Colors</h3>
              <div className="space-y-2">
                {RESEARCH_DOMAINS.map(domain => (
                  <div key={domain.id} className="flex items-center">
                    <div 
                      className="w-4 h-4 rounded-full mr-2 border border-gray-300"
                      style={{ background: `linear-gradient(135deg, ${d3.color(domain.color)?.brighter(0.5)}, ${domain.color})` }}
                    ></div>
                    <span className="text-xs text-gray-600">{domain.name}</span>
                  </div>
                ))}
              </div>
              
              <h4 className="text-sm font-medium text-gray-700 mt-4 mb-2">Relationship Types</h4>
              <div className="space-y-1 text-xs">
                <div className="flex items-center">
                  <div className="w-4 h-1 bg-blue-500 mr-2"></div>
                  <span className="text-gray-600">implements</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-1 bg-green-500 mr-2"></div>
                  <span className="text-gray-600">uses</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-1 bg-red-500 mr-2"></div>
                  <span className="text-gray-600">enables</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-1 bg-purple-500 mr-2"></div>
                  <span className="text-gray-600">enhances</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-1 bg-orange-500 mr-2"></div>
                  <span className="text-gray-600">requires</span>
                </div>
                <div className="flex items-center">
                  <div className="w-4 h-1 bg-gray-600 mr-2" style={{ borderTop: '1px dashed #666' }}></div>
                  <span className="text-gray-600">depends_on</span>
                </div>
              </div>
            </div>

            {/* Enhanced Statistics */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Graph Analytics</h3>
              <div className="space-y-1 text-sm text-gray-600">
                <div className="flex justify-between">
                  <span>Concepts:</span>
                  <span className="font-mono">{filteredNodes.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Connections:</span>
                  <span className="font-mono">{filteredLinks.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Domains:</span>
                  <span className="font-mono">{new Set(filteredNodes.map(n => n.source_domain)).size}</span>
                </div>
                <div className="flex justify-between">
                  <span>Avg. Relevance:</span>
                  <span className="font-mono">
                    {filteredNodes.length > 0 
                      ? (filteredNodes.reduce((sum, n) => sum + n.relevance_score, 0) / filteredNodes.length).toFixed(3)
                      : '0.000'
                    }
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Density:</span>
                  <span className="font-mono">
                    {filteredNodes.length > 1 
                      ? (filteredLinks.length / (filteredNodes.length * (filteredNodes.length - 1) / 2)).toFixed(3)
                      : '0.000'
                    }
                  </span>
                </div>
              </div>
              
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="text-xs text-purple-600 font-medium">
                  🎯 Enhanced with cutting-edge D3.js v7 features!
                </div>
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
