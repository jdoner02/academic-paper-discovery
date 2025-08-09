#!/usr/bin/env node

/**
 * Concept Data Preparation Script
 * 
 * This script processes the concept storage directory and creates optimized
 * datasets for the D3.js visualization. It aggregates concepts across domains,
 * creates meaningful relationships, and prepares filtered datasets.
 * 
 * Educational Notes:
 * - Demonstrates Node.js file system operations
 * - Shows data aggregation and filtering techniques
 * - Implements graph relationship inference algorithms
 * - Provides example of ETL (Extract, Transform, Load) pipeline
 * 
 * Usage: node scripts/prepare-concept-data.js
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONCEPT_STORAGE_PATH = path.join(__dirname, '..', 'concept_storage', 'concepts');
const OUTPUT_PATH = path.join(__dirname, '..', 'public', 'data');
const MIN_RELEVANCE_SCORE = 0.7;
const MAX_CONCEPTS_PER_DOMAIN = 20;

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_PATH)) {
  fs.mkdirSync(OUTPUT_PATH, { recursive: true });
}

/**
 * Load and process concept data from all domains
 */
async function processConceptData() {
  const domains = fs.readdirSync(CONCEPT_STORAGE_PATH).filter(item => {
    return fs.statSync(path.join(CONCEPT_STORAGE_PATH, item)).isDirectory();
  });

  console.log(`Found ${domains.length} research domains:`);
  domains.forEach(domain => console.log(`  - ${domain}`));

  const allNodes = [];
  const domainStatistics = {};

  for (const domain of domains) {
    console.log(`\nProcessing domain: ${domain}`);
    const domainPath = path.join(CONCEPT_STORAGE_PATH, domain);
    const domainConcepts = await loadDomainConcepts(domainPath, domain);
    
    // Filter and limit concepts per domain
    const filteredConcepts = domainConcepts
      .filter(concept => concept.relevance_score >= MIN_RELEVANCE_SCORE)
      .sort((a, b) => b.relevance_score - a.relevance_score)
      .slice(0, MAX_CONCEPTS_PER_DOMAIN);
    
    allNodes.push(...filteredConcepts);
    
    domainStatistics[domain] = {
      total_concepts: domainConcepts.length,
      filtered_concepts: filteredConcepts.length,
      avg_relevance: filteredConcepts.reduce((sum, c) => sum + c.relevance_score, 0) / filteredConcepts.length,
      top_concepts: filteredConcepts.slice(0, 5).map(c => c.text)
    };
    
    console.log(`  Loaded ${filteredConcepts.length} concepts (filtered from ${domainConcepts.length})`);
  }

  // Generate relationships
  console.log('\nGenerating concept relationships...');
  const links = generateConceptLinks(allNodes);
  
  // Create final dataset
  const graphData = {
    nodes: allNodes,
    links: links,
    domains: domains,
    domain_statistics: domainStatistics,
    metadata: {
      generated_at: new Date().toISOString(),
      total_concepts: allNodes.length,
      total_connections: links.length,
      domains_count: domains.length,
      min_relevance_filter: MIN_RELEVANCE_SCORE,
      max_concepts_per_domain: MAX_CONCEPTS_PER_DOMAIN
    }
  };

  // Save processed data
  const outputFile = path.join(OUTPUT_PATH, 'concept-graph-data.json');
  fs.writeFileSync(outputFile, JSON.stringify(graphData, null, 2));
  console.log(`\nSaved processed data to: ${outputFile}`);
  
  // Create domain-specific datasets
  for (const domain of domains) {
    const domainNodes = allNodes.filter(node => node.source_domain === domain);
    const domainLinks = links.filter(link => 
      allNodes.find(n => n.id === link.source)?.source_domain === domain ||
      allNodes.find(n => n.id === link.target)?.source_domain === domain
    );
    
    const domainData = {
      domain,
      nodes: domainNodes,
      links: domainLinks,
      statistics: domainStatistics[domain]
    };
    
    const domainFile = path.join(OUTPUT_PATH, `${domain}.json`);
    fs.writeFileSync(domainFile, JSON.stringify(domainData, null, 2));
  }
  
  console.log(`Created ${domains.length} domain-specific datasets`);
  
  // Print summary statistics
  console.log('\n' + '='.repeat(50));
  console.log('CONCEPT DATA PROCESSING SUMMARY');
  console.log('='.repeat(50));
  console.log(`Total domains: ${domains.length}`);
  console.log(`Total concepts: ${allNodes.length}`);
  console.log(`Total relationships: ${links.length}`);
  console.log(`Average concepts per domain: ${(allNodes.length / domains.length).toFixed(1)}`);
  
  const topDomains = Object.entries(domainStatistics)
    .sort((a, b) => b[1].filtered_concepts - a[1].filtered_concepts)
    .slice(0, 5);
  
  console.log('\nTop 5 domains by concept count:');
  topDomains.forEach(([domain, stats], index) => {
    console.log(`  ${index + 1}. ${domain}: ${stats.filtered_concepts} concepts`);
  });
}

/**
 * Load concept data from a specific domain directory
 */
async function loadDomainConcepts(domainPath, domainName) {
  const concepts = [];
  
  try {
    const files = fs.readdirSync(domainPath);
    
    for (const file of files) {
      if (file.endsWith('.json') && file !== '_index.json') {
        const filePath = path.join(domainPath, file);
        const rawData = fs.readFileSync(filePath, 'utf8');
        const paperData = JSON.parse(rawData);
        
        if (paperData.concepts && Array.isArray(paperData.concepts)) {
          paperData.concepts.forEach((concept, index) => {
            // Clean up concept text (remove extra spaces, normalize)
            const cleanText = concept.text.toLowerCase().trim().replace(/\s+/g, ' ');
            
            concepts.push({
              id: `${domainName}-${cleanText.replace(/\s/g, '-')}-${index}`,
              text: cleanText,
              frequency: concept.frequency || 1,
              relevance_score: concept.relevance_score || 0,
              source_domain: domainName,
              source_papers: concept.source_papers || [paperData.paper_title || 'Unknown Paper'],
              extraction_method: concept.extraction_method || 'unknown',
              created_at: concept.created_at,
              // Add display properties for D3.js
              display_text: concept.text, // Keep original formatting for display
              size: Math.max(5, Math.min(30, concept.frequency / 5)), // Node size based on frequency
              color: getDomainColor(domainName)
            });
          });
        }
      }
    }
  } catch (error) {
    console.error(`Error loading concepts from domain ${domainName}:`, error.message);
  }
  
  return concepts;
}

/**
 * Generate concept relationships based on similarity and domain connections
 */
function generateConceptLinks(nodes) {
  const links = [];
  const conceptGroups = new Map();
  
  // Group similar concepts
  nodes.forEach(node => {
    const key = node.text.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
    if (!conceptGroups.has(key)) {
      conceptGroups.set(key, []);
    }
    conceptGroups.get(key).push(node);
  });
  
  // Create cross-domain similarity links
  conceptGroups.forEach(group => {
    if (group.length > 1) {
      for (let i = 0; i < group.length; i++) {
        for (let j = i + 1; j < group.length; j++) {
          const nodeA = group[i];
          const nodeB = group[j];
          
          if (nodeA.source_domain !== nodeB.source_domain) {
            const strength = Math.min(nodeA.relevance_score, nodeB.relevance_score);
            links.push({
              source: nodeA.id,
              target: nodeB.id,
              strength: strength,
              relationship_type: 'similar_concept',
              weight: strength * 2 // Stronger weight for similar concepts
            });
          }
        }
      }
    }
  });
  
  // Create domain-based relationships for high-relevance concepts
  const domainGroups = new Map();
  nodes.forEach(node => {
    if (!domainGroups.has(node.source_domain)) {
      domainGroups.set(node.source_domain, []);
    }
    domainGroups.get(node.source_domain).push(node);
  });
  
  domainGroups.forEach(domainConcepts => {
    const topConcepts = domainConcepts
      .filter(concept => concept.relevance_score > 0.8)
      .sort((a, b) => b.relevance_score - a.relevance_score)
      .slice(0, 8); // Connect top 8 concepts within each domain
    
    for (let i = 0; i < topConcepts.length; i++) {
      for (let j = i + 1; j < topConcepts.length; j++) {
        const nodeA = topConcepts[i];
        const nodeB = topConcepts[j];
        
        links.push({
          source: nodeA.id,
          target: nodeB.id,
          strength: (nodeA.relevance_score + nodeB.relevance_score) / 2,
          relationship_type: 'domain_related',
          weight: 1
        });
      }
    }
  });
  
  return links;
}

/**
 * Get color for a domain (matching the frontend color scheme)
 */
function getDomainColor(domain) {
  const domainColors = {
    'ai_driven_cyber_defense': '#3B82F6',
    'post_quantum_cryptography_implementation': '#8B5CF6',
    'water_infrastructure_incident_response': '#06B6D4',
    'healthcare_privacy_compliance': '#10B981',
    'industrial_iot_security': '#F59E0B',
    'government_ransomware_defense': '#6366F1',
    'local_government_cybersecurity': '#6366F1',
    'medical_device_cybersecurity': '#10B981',
    'water_treatment_scada_security': '#06B6D4',
    'water_iot_smart_monitoring_security': '#06B6D4',
    'quantum_cryptanalysis_threats': '#8B5CF6',
    'quantum_safe_protocols': '#8B5CF6',
    'default': '#6B7280'
  };
  
  return domainColors[domain] || domainColors.default;
}

// Run the script
if (require.main === module) {
  processConceptData().catch(console.error);
}

module.exports = { processConceptData };
