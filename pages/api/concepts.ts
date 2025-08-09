/**
 * Concepts API Endpoint - Serves concept data for the interactive graph
 * 
 * This API endpoint reads the concept storage directory and returns
 * structured concept data with relationships for the graph visualization.
 * 
 * Educational Notes:
 * - Demonstrates Next.js API routes for backend functionality
 * - Shows file system operations and JSON data processing
 * - Implements error handling and data validation
 * - Provides RESTful API design patterns
 * 
 * Design Decisions:
 * - Read directly from concept_storage for real-time data
 * - Return standardized format for frontend consumption
 * - Include relationship inference from shared domains
 * - Implement basic caching for performance
 * 
 * Use Cases:
 * - Frontend concept graph data loading
 * - Real-time concept exploration
 * - Research domain analysis
 * - Academic paper relationship discovery
 */

import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

interface ConceptData {
  text: string;
  frequency: number;
  relevance_score: number;
  source_papers: string[];
  source_domain: string;
  extraction_method: string;
  created_at: string;
}

interface ConceptNode {
  id: string;
  text: string;
  frequency: number;
  relevance_score: number;
  source_domain: string;
  source_papers: string[];
  extraction_method: string;
}

interface ConceptLink {
  source: string;
  target: string;
  strength: number;
  relationship_type: string;
}

interface GraphData {
  nodes: ConceptNode[];
  links: ConceptLink[];
  domains: string[];
  statistics: {
    total_concepts: number;
    total_connections: number;
    domains_count: number;
    papers_count: number;
  };
}

/**
 * Load concept data from a specific domain directory
 */
async function loadDomainConcepts(domainPath: string, domainName: string): Promise<ConceptNode[]> {
  const concepts: ConceptNode[] = [];
  
  try {
    const files = fs.readdirSync(domainPath);
    
    for (const file of files) {
      if (file.endsWith('.json') && file !== '_index.json') {
        const filePath = path.join(domainPath, file);
        const rawData = fs.readFileSync(filePath, 'utf8');
        const paperData = JSON.parse(rawData);
        
        if (paperData.concepts && Array.isArray(paperData.concepts)) {
          // Process concepts from this paper
          paperData.concepts.forEach((concept: ConceptData, index: number) => {
            concepts.push({
              id: `${domainName}-${concept.text}-${index}`,
              text: concept.text,
              frequency: concept.frequency,
              relevance_score: concept.relevance_score,
              source_domain: domainName,
              source_papers: concept.source_papers || [paperData.paper_title || 'Unknown Paper'],
              extraction_method: concept.extraction_method
            });
          });
        }
      }
    }
  } catch (error) {
    console.error(`Error loading concepts from domain ${domainName}:`, error);
  }
  
  return concepts;
}

/**
 * Generate concept relationships based on shared domains and similar concepts
 */
function generateConceptLinks(nodes: ConceptNode[]): ConceptLink[] {
  const links: ConceptLink[] = [];
  const conceptGroups = new Map<string, ConceptNode[]>();
  
  // Group concepts by similar text (for now, exact matches)
  nodes.forEach(node => {
    const key = node.text.toLowerCase().trim();
    if (!conceptGroups.has(key)) {
      conceptGroups.set(key, []);
    }
    conceptGroups.get(key)!.push(node);
  });
  
  // Create links between similar concepts from different domains
  conceptGroups.forEach(group => {
    if (group.length > 1) {
      for (let i = 0; i < group.length; i++) {
        for (let j = i + 1; j < group.length; j++) {
          const nodeA = group[i];
          const nodeB = group[j];
          
          if (nodeA.source_domain !== nodeB.source_domain) {
            // Cross-domain concept relationship
            const strength = Math.min(nodeA.relevance_score, nodeB.relevance_score);
            links.push({
              source: nodeA.id,
              target: nodeB.id,
              strength: strength,
              relationship_type: 'similar_concept'
            });
          }
        }
      }
    }
  });
  
  // Create domain-based relationships for high-relevance concepts
  const domainGroups = new Map<string, ConceptNode[]>();
  nodes.forEach(node => {
    if (!domainGroups.has(node.source_domain)) {
      domainGroups.set(node.source_domain, []);
    }
    domainGroups.get(node.source_domain)!.push(node);
  });
  
  domainGroups.forEach(domainConcepts => {
    // Sort by relevance and connect top concepts within domain
    const topConcepts = domainConcepts
      .filter(concept => concept.relevance_score > 0.8)
      .sort((a, b) => b.relevance_score - a.relevance_score)
      .slice(0, 5);
    
    for (let i = 0; i < topConcepts.length; i++) {
      for (let j = i + 1; j < topConcepts.length; j++) {
        const nodeA = topConcepts[i];
        const nodeB = topConcepts[j];
        
        links.push({
          source: nodeA.id,
          target: nodeB.id,
          strength: (nodeA.relevance_score + nodeB.relevance_score) / 2,
          relationship_type: 'domain_related'
        });
      }
    }
  });
  
  return links;
}

/**
 * Main API handler
 */
export default async function handler(req: NextApiRequest, res: NextApiResponse<GraphData | { error: string }>) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    // Concept storage is in the project root
    const conceptStoragePath = path.join(process.cwd(), 'concept_storage', 'concepts');
    
    if (!fs.existsSync(conceptStoragePath)) {
      return res.status(404).json({ 
        error: `Concept storage directory not found at: ${conceptStoragePath}` 
      });
    }
    
    const domains = fs.readdirSync(conceptStoragePath).filter(item => {
      return fs.statSync(path.join(conceptStoragePath, item)).isDirectory();
    });
    
    // Load concepts from all domains
    const allNodes: ConceptNode[] = [];
    
    for (const domain of domains) {
      const domainPath = path.join(conceptStoragePath, domain);
      const domainConcepts = await loadDomainConcepts(domainPath, domain);
      allNodes.push(...domainConcepts);
    }
    
    // Filter and deduplicate concepts
    const uniqueNodes = new Map<string, ConceptNode>();
    allNodes.forEach(node => {
      const key = `${node.source_domain}-${node.text}`;
      const existing = uniqueNodes.get(key);
      
      if (!existing || node.relevance_score > existing.relevance_score) {
        uniqueNodes.set(key, node);
      }
    });
    
    const nodes = Array.from(uniqueNodes.values())
      .filter(node => node.relevance_score > 0.7) // Filter for quality
      .slice(0, 100); // Limit for performance
    
    // Generate relationships
    const links = generateConceptLinks(nodes);
    
    // Calculate statistics
    const uniquePapers = new Set<string>();
    nodes.forEach(node => {
      node.source_papers.forEach(paper => uniquePapers.add(paper));
    });
    
    const graphData: GraphData = {
      nodes,
      links,
      domains,
      statistics: {
        total_concepts: nodes.length,
        total_connections: links.length,
        domains_count: domains.length,
        papers_count: uniquePapers.size
      }
    };
    
    // Set cache headers for performance
    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=600');
    
    return res.status(200).json(graphData);
    
  } catch (error) {
    console.error('Error processing concepts:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
