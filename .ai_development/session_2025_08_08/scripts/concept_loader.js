#!/usr/bin/env node

/**
 * Concept Loader - Dynamic JSON Concept Discovery and Hierarchical Organization
 * 
 * Educational Purpose:
 * Demonstrates recursive file system traversal, JSON parsing, and graph data structure
 * construction from hierarchical folder structures. Students learn how filesystem
 * organization can mirror mathematical concept relationships.
 * 
 * Features:
 * - Recursive directory traversal following Clean Architecture principles
 * - JSON schema validation for educational concept objects
 * - Automatic relationship inference from folder hierarchy
 * - D3.js compatible data transformation
 * - Real-time file watching for live updates
 */

const fs = require('fs');
const path = require('path');
const chokidar = require('chokidar');

class ConceptLoader {
    constructor(conceptsDir = './concept_definitions') {
        this.conceptsDir = path.resolve(conceptsDir);
        this.concepts = new Map();
        this.relationships = new Set();
        this.outputPath = './public/concept-graph-data.json';
        
        console.log(`🔍 Initializing Concept Loader for: ${this.conceptsDir}`);
    }

    /**
     * Recursively discover all JSON concept files
     * Educational Note: Demonstrates recursive algorithms and file system traversal
     */
    async discoverConcepts() {
        console.log('📚 Discovering concept files...');
        
        const concepts = [];
        await this._traverseDirectory(this.conceptsDir, concepts);
        
        console.log(`✅ Found ${concepts.length} concept files`);
        return concepts;
    }

    async _traverseDirectory(dir, concepts, relativePath = '') {
        const items = await fs.promises.readdir(dir);
        
        for (const item of items) {
            const fullPath = path.join(dir, item);
            const newRelativePath = path.join(relativePath, item);
            const stats = await fs.promises.stat(fullPath);
            
            if (stats.isDirectory()) {
                // Recursive descent - fundamental CS concept
                await this._traverseDirectory(fullPath, concepts, newRelativePath);
            } else if (item.endsWith('.json')) {
                try {
                    const content = await fs.promises.readFile(fullPath, 'utf8');
                    const concept = JSON.parse(content);
                    
                    // Add hierarchical metadata from folder structure
                    concept.file_path = newRelativePath;
                    concept.hierarchy_level = relativePath.split(path.sep).length;
                    concept.parent_domain = path.dirname(newRelativePath).replace(/\//g, '.');
                    
                    // Validate concept structure
                    if (this._validateConcept(concept)) {
                        concepts.push(concept);
                        this.concepts.set(concept.id, concept);
                    }
                } catch (error) {
                    console.warn(`⚠️  Failed to parse ${fullPath}: ${error.message}`);
                }
            }
        }
    }

    /**
     * Validate concept JSON structure
     * Educational Note: Input validation is critical in production systems
     */
    _validateConcept(concept) {
        const required = ['id', 'name', 'type', 'domain'];
        const missing = required.filter(field => !concept[field]);
        
        if (missing.length > 0) {
            console.warn(`⚠️  Concept missing required fields: ${missing.join(', ')}`);
            return false;
        }
        
        return true;
    }

    /**
     * Build relationships from explicit dependencies and implicit hierarchy
     * Educational Note: Combines explicit graph edges with inferred structural relationships
     */
    buildRelationships() {
        console.log('🔗 Building concept relationships...');
        
        const relationships = [];
        
        for (const [conceptId, concept] of this.concepts) {
            // Explicit prerequisites (strong dependencies)
            if (concept.prerequisites) {
                concept.prerequisites.forEach(prereq => {
                    relationships.push({
                        source: prereq,
                        target: conceptId,
                        type: 'prerequisite',
                        strength: 0.9
                    });
                });
            }
            
            // Explicit dependencies (medium dependencies)
            if (concept.depends_on) {
                concept.depends_on.forEach(dep => {
                    relationships.push({
                        source: dep,
                        target: conceptId,
                        type: 'depends_on',
                        strength: 0.7
                    });
                });
            }
            
            // Enablement relationships (what this concept enables)
            if (concept.enables) {
                concept.enables.forEach(enabled => {
                    relationships.push({
                        source: conceptId,
                        target: enabled,
                        type: 'enables',
                        strength: 0.6
                    });
                });
            }
            
            // Hierarchical relationships (weak structural dependencies)
            this._addHierarchicalRelationships(concept, relationships);
        }
        
        console.log(`✅ Built ${relationships.length} relationships`);
        return relationships;
    }

    /**
     * Infer relationships from folder hierarchy
     * Educational Note: Demonstrates how physical organization can represent logical relationships
     */
    _addHierarchicalRelationships(concept, relationships) {
        const pathParts = concept.file_path.split(path.sep);
        
        // Create "part_of" relationships up the hierarchy
        for (let i = pathParts.length - 2; i >= 0; i--) {
            const parentPath = pathParts.slice(0, i + 1).join('.');
            relationships.push({
                source: concept.id,
                target: parentPath,
                type: 'part_of',
                strength: 0.3
            });
        }
    }

    /**
     * Generate D3.js compatible graph data
     * Educational Note: Data transformation for visualization libraries
     */
    generateD3Data() {
        console.log('🎨 Generating D3.js visualization data...');
        
        const nodes = Array.from(this.concepts.values()).map(concept => ({
            id: concept.id,
            name: concept.name,
            type: concept.type,
            domain: concept.domain,
            subdomain: concept.subdomain,
            level: concept.level,
            hierarchy_level: concept.hierarchy_level,
            parent_domain: concept.parent_domain,
            formal_statement: concept.formal_statement,
            informal_description: concept.informal_description,
            examples: concept.examples,
            difficulty: concept.difficulty || 5,
            // Visual properties for D3.js
            group: concept.domain,
            size: this._calculateNodeSize(concept),
            color: this._getNodeColor(concept)
        }));
        
        const links = this.buildRelationships().map(rel => ({
            source: rel.source,
            target: rel.target,
            type: rel.type,
            strength: rel.strength,
            // Visual properties for D3.js
            distance: this._calculateLinkDistance(rel),
            strokeWidth: rel.strength * 3
        }));
        
        const data = {
            nodes,
            links,
            metadata: {
                total_concepts: nodes.length,
                total_relationships: links.length,
                domains: [...new Set(nodes.map(n => n.domain))],
                types: [...new Set(nodes.map(n => n.type))],
                levels: [...new Set(nodes.map(n => n.level))],
                generated: new Date().toISOString()
            }
        };
        
        console.log(`✅ Generated D3 data: ${nodes.length} nodes, ${links.length} links`);
        return data;
    }

    /**
     * Calculate node size based on concept complexity
     * Educational Note: Visual encoding of quantitative data
     */
    _calculateNodeSize(concept) {
        let size = 10; // Base size
        
        // Size based on examples (more examples = more complex)
        if (concept.examples) size += concept.examples.length * 2;
        
        // Size based on dependencies (more dependencies = more fundamental)
        if (concept.prerequisites) size += concept.prerequisites.length;
        if (concept.depends_on) size += concept.depends_on.length;
        
        // Size based on difficulty
        if (concept.difficulty) size += concept.difficulty;
        
        // Size based on hierarchy level (deeper = more specific)
        size += concept.hierarchy_level || 0;
        
        return Math.min(size, 30); // Cap maximum size
    }

    /**
     * Assign colors based on concept domain
     * Educational Note: Categorical color encoding for graph visualization
     */
    _getNodeColor(concept) {
        const colorMap = {
            'set_theory': '#FF6B6B',
            'logic': '#4ECDC4',
            'algebra': '#45B7D1',
            'analysis': '#96CEB4',
            'topology': '#FECA57',
            'geometry': '#FF9FF3',
            'number_theory': '#54A0FF',
            'combinatorics': '#FD79A8'
        };
        
        return colorMap[concept.domain] || '#95A5A6';
    }

    /**
     * Calculate link distance based on relationship strength
     * Educational Note: Visual encoding of relationship strength through spacing
     */
    _calculateLinkDistance(relationship) {
        const baseDistance = 100;
        const strengthMultiplier = 1 - relationship.strength; // Stronger = closer
        return baseDistance * (0.5 + strengthMultiplier);
    }

    /**
     * Save visualization data for web application
     */
    async saveVisualizationData(data) {
        await fs.promises.writeFile(
            this.outputPath, 
            JSON.stringify(data, null, 2),
            'utf8'
        );
        console.log(`💾 Saved visualization data to ${this.outputPath}`);
    }

    /**
     * Watch for file changes and regenerate data
     * Educational Note: File system events and reactive programming
     */
    startWatching() {
        console.log('👀 Starting file watcher for live updates...');
        
        const watcher = chokidar.watch(this.conceptsDir, {
            ignored: /(^|[/\\])\../,
            persistent: true
        });
        
        watcher.on('change', async (path) => {
            console.log(`📝 File changed: ${path}`);
            await this.loadAndGenerate();
        });
        
        watcher.on('add', async (path) => {
            console.log(`➕ File added: ${path}`);
            await this.loadAndGenerate();
        });
        
        watcher.on('unlink', async (path) => {
            console.log(`❌ File removed: ${path}`);
            await this.loadAndGenerate();
        });
    }

    /**
     * Main workflow: Load concepts and generate visualization data
     */
    async loadAndGenerate() {
        try {
            this.concepts.clear();
            await this.discoverConcepts();
            const d3Data = this.generateD3Data();
            await this.saveVisualizationData(d3Data);
            console.log('🎉 Concept loading complete!');
            return d3Data;
        } catch (error) {
            console.error('❌ Error loading concepts:', error);
            throw error;
        }
    }
}

// CLI interface
async function main() {
    const loader = new ConceptLoader();
    
    // Initial load
    await loader.loadAndGenerate();
    
    // Start watching for changes
    if (process.argv.includes('--watch')) {
        loader.startWatching();
        console.log('🔄 Watching for changes... Press Ctrl+C to stop.');
        
        // Keep process alive
        process.on('SIGINT', () => {
            console.log('\n👋 Stopping file watcher...');
            process.exit(0);
        });
    }
}

// Export for programmatic use
module.exports = ConceptLoader;

// Run if called directly
if (require.main === module) {
    main().catch(console.error);
}
