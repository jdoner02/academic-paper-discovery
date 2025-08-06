#!/usr/bin/env node
/**
 * Concept Extraction Script - Real embeddings-based concept extraction from research papers
 * 
 * This script demonstrates the "locally first" approach by processing research papers during
 * build time to generate embeddings and extract concepts. The resulting concept maps are
 * saved as static JSON files that can be served by GitHub Pages.
 * 
 * Features:
 * - Reads research papers from CLI tool outputs directory
 * - Uses sentence-transformers for high-quality embeddings
 * - Clusters concepts using cosine similarity
 * - Generates real concept relationships from paper abstracts
 * - Outputs structured data compatible with domain entities
 * 
 * Educational Notes:
 * - Shows build-time vs runtime processing trade-offs
 * - Demonstrates Clean Architecture compliance in scripts
 * - Illustrates practical embeddings usage for concept discovery
 * - Shows how to bridge CLI tools with web applications
 */

const fs = require('fs').promises;
const path = require('path');
const { pipeline } = require('@xenova/transformers');

// Configuration
const CONFIG = {
    sourceDataPath: '../../research-paper-aggregator/outputs',
    outputPath: './public/data',
    maxPapersPerDomain: 20, // Limit for demo purposes
    embeddingModel: 'Xenova/all-MiniLM-L6-v2',
    conceptSimilarityThreshold: 0.7
};

/**
 * ResearchPaperData - Value object representing parsed paper data
 * 
 * Educational Notes:
 * This follows the domain-driven design principle of creating value objects
 * for data that has meaning but no identity. The paper data is immutable
 * once created and represents a concept from our domain.
 */
class ResearchPaperData {
    constructor(title, abstract, authors, keywords, venue, publicationDate) {
        this.title = title;
        this.abstract = abstract;
        this.authors = authors;
        this.keywords = keywords;
        this.venue = venue;
        this.publicationDate = publicationDate;
        
        // Generate a simple ID for concept mapping
        this.id = this._generateId(title);
    }
    
    _generateId(title) {
        return title
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, '')
            .replace(/\s+/g, '_')
            .substring(0, 50);
    }
    
    /**
     * Extract concept-relevant text for embedding generation
     * Combines title and abstract as they contain the most concept-dense information
     */
    getConceptText() {
        return `${this.title}. ${this.abstract}`;
    }
}

/**
 * ConceptCluster - Represents a group of related concepts from papers
 * 
 * Educational Notes:
 * This class demonstrates the Factory pattern combined with domain modeling.
 * It creates ConceptNode-compatible data structures that align with our
 * domain entities while handling the complexity of clustering.
 */
class ConceptCluster {
    constructor(name, papers, embedding) {
        this.name = name;
        this.papers = papers;
        this.embedding = embedding;
        this.relationships = [];
    }
    
    /**
     * Convert to domain entity format (ConceptNode-compatible)
     */
    toDomainEntity() {
        return {
            id: this._generateId(),
            name: this.name,
            description: this._generateDescription(),
            papers: this.papers.map(paper => ({
                id: paper.id,
                title: paper.title,
                authors: paper.authors,
                venue: paper.venue,
                publicationDate: paper.publicationDate
            })),
            relationships: this.relationships.map(rel => ({
                targetId: rel.targetId,
                strength: rel.strength,
                type: 'semantic_similarity'
            }))
        };
    }
    
    _generateId() {
        return this.name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
    }
    
    _generateDescription() {
        const commonKeywords = this._extractCommonKeywords();
        const paperCount = this.papers.length;
        return `Research cluster containing ${paperCount} papers focusing on ${this.name}. ` +
               `Common themes: ${commonKeywords.join(', ')}.`;
    }
    
    _extractCommonKeywords() {
        const keywordCounts = {};
        this.papers.forEach(paper => {
            if (paper.keywords) {
                paper.keywords.forEach(keyword => {
                    keywordCounts[keyword] = (keywordCounts[keyword] || 0) + 1;
                });
            }
        });
        
        return Object.entries(keywordCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3)
            .map(entry => entry[0]);
    }
}

/**
 * ConceptExtractorService - Core business logic for concept extraction
 * 
 * Educational Notes:
 * This service demonstrates Clean Architecture's application layer patterns:
 * - Single Responsibility: Only handles concept extraction
 * - Dependency Inversion: Could be abstracted behind ports
 * - Domain Focus: Creates domain-compatible entities
 */
class ConceptExtractorService {
    constructor() {
        this.embedder = null;
    }
    
    async initialize() {
        console.log('Initializing embeddings model...');
        this.embedder = await pipeline('feature-extraction', CONFIG.embeddingModel);
        console.log('✅ Embeddings model loaded');
    }
    
    /**
     * Extract concepts from a collection of research papers
     */
    async extractConcepts(papers) {
        console.log(`Processing ${papers.length} papers for concept extraction...`);
        
        // Generate embeddings for all papers
        const papersWithEmbeddings = await this._generateEmbeddings(papers);
        
        // Cluster papers by semantic similarity
        const clusters = await this._clusterBySimilarity(papersWithEmbeddings);
        
        // Generate relationships between clusters
        const clustersWithRelationships = await this._generateRelationships(clusters);
        
        console.log(`✅ Generated ${clustersWithRelationships.length} concept clusters`);
        return clustersWithRelationships.map(cluster => cluster.toDomainEntity());
    }
    
    async _generateEmbeddings(papers) {
        console.log('Generating embeddings...');
        const results = [];
        
        for (let i = 0; i < papers.length; i++) {
            const paper = papers[i];
            console.log(`  Processing ${i + 1}/${papers.length}: ${paper.title.substring(0, 50)}...`);
            
            const conceptText = paper.getConceptText();
            const output = await this.embedder(conceptText, { pooling: 'mean', normalize: true });
            const embedding = Array.from(output.data);
            
            results.push({ paper, embedding });
        }
        
        return results;
    }
    
    async _clusterBySimilarity(papersWithEmbeddings) {
        console.log('Clustering by semantic similarity...');
        
        // Simple hierarchical clustering based on cosine similarity
        const clusters = [];
        const used = new Set();
        
        for (let i = 0; i < papersWithEmbeddings.length; i++) {
            if (used.has(i)) continue;
            
            const mainPaper = papersWithEmbeddings[i];
            const clusterPapers = [mainPaper.paper];
            used.add(i);
            
            // Find similar papers
            for (let j = i + 1; j < papersWithEmbeddings.length; j++) {
                if (used.has(j)) continue;
                
                const similarity = this._cosineSimilarity(
                    mainPaper.embedding, 
                    papersWithEmbeddings[j].embedding
                );
                
                if (similarity > CONFIG.conceptSimilarityThreshold) {
                    clusterPapers.push(papersWithEmbeddings[j].paper);
                    used.add(j);
                }
            }
            
            // Create cluster with generated name
            const clusterName = this._generateClusterName(clusterPapers);
            const avgEmbedding = this._averageEmbeddings(
                clusterPapers.map(paper => 
                    papersWithEmbeddings.find(p => p.paper.id === paper.id).embedding
                )
            );
            
            clusters.push(new ConceptCluster(clusterName, clusterPapers, avgEmbedding));
        }
        
        return clusters;
    }
    
    async _generateRelationships(clusters) {
        console.log('Generating cluster relationships...');
        
        for (let i = 0; i < clusters.length; i++) {
            for (let j = i + 1; j < clusters.length; j++) {
                const similarity = this._cosineSimilarity(
                    clusters[i].embedding,
                    clusters[j].embedding
                );
                
                if (similarity > 0.3) { // Lower threshold for relationships
                    clusters[i].relationships.push({
                        targetId: clusters[j]._generateId(),
                        strength: similarity
                    });
                    clusters[j].relationships.push({
                        targetId: clusters[i]._generateId(),
                        strength: similarity
                    });
                }
            }
        }
        
        return clusters;
    }
    
    _cosineSimilarity(vecA, vecB) {
        const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
        const magA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
        const magB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
        return dotProduct / (magA * magB);
    }
    
    _averageEmbeddings(embeddings) {
        if (embeddings.length === 0) return [];
        
        const avgEmbedding = new Array(embeddings[0].length).fill(0);
        embeddings.forEach(embedding => {
            embedding.forEach((value, i) => {
                avgEmbedding[i] += value;
            });
        });
        
        return avgEmbedding.map(value => value / embeddings.length);
    }
    
    _generateClusterName(papers) {
        // Extract common terms from titles
        const allWords = papers
            .flatMap(paper => paper.title.toLowerCase().split(/\s+/))
            .filter(word => word.length > 3)
            .filter(word => !['using', 'with', 'from', 'analysis', 'study', 'approach'].includes(word));
        
        const wordCounts = {};
        allWords.forEach(word => {
            wordCounts[word] = (wordCounts[word] || 0) + 1;
        });
        
        const commonWords = Object.entries(wordCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3)
            .map(entry => entry[0]);
        
        if (commonWords.length > 0) {
            return commonWords.map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
        }
        
        return papers[0].title.substring(0, 20) + '...';
    }
}

/**
 * PaperDataLoader - Infrastructure concern for loading research papers
 * 
 * Educational Notes:
 * This demonstrates the adapter pattern, adapting the CLI tool's output format
 * to our domain entities. In full Clean Architecture, this would be in the
 * infrastructure layer.
 */
class PaperDataLoader {
    async loadAllPapers() {
        console.log('Loading research papers from CLI outputs...');
        
        const papers = [];
        const sourcePath = path.resolve(__dirname, CONFIG.sourceDataPath);
        
        try {
            const directories = await fs.readdir(sourcePath, { withFileTypes: true });
            
            for (const dir of directories) {
                if (dir.isDirectory()) {
                    console.log(`Loading from ${dir.name}...`);
                    const domainPapers = await this._loadFromDirectory(
                        path.join(sourcePath, dir.name)
                    );
                    papers.push(...domainPapers.slice(0, CONFIG.maxPapersPerDomain));
                }
            }
            
            console.log(`✅ Loaded ${papers.length} papers from ${directories.length} domains`);
            return papers;
        } catch (error) {
            console.error('Error loading papers:', error);
            return [];
        }
    }
    
    async _loadFromDirectory(dirPath) {
        try {
            const metadataPath = path.join(dirPath, 'metadata.json');
            const metadataContent = await fs.readFile(metadataPath, 'utf-8');
            const metadata = JSON.parse(metadataContent);
            
            return metadata.papers
                .filter(paper => paper.abstract && paper.abstract.length > 50)
                .map(paper => new ResearchPaperData(
                    paper.title,
                    paper.abstract,
                    paper.authors || [],
                    paper.keywords || [],
                    paper.venue || 'Unknown',
                    paper.publication_date
                ));
        } catch (error) {
            console.warn(`Could not load from ${dirPath}:`, error.message);
            return [];
        }
    }
}

/**
 * ConceptMapGenerator - Orchestrates the concept extraction pipeline
 * 
 * Educational Notes:
 * This is the application service that coordinates all the components.
 * It demonstrates the Facade pattern, providing a simple interface
 * for complex concept extraction operations.
 */
class ConceptMapGenerator {
    constructor() {
        this.loader = new PaperDataLoader();
        this.extractor = new ConceptExtractorService();
    }
    
    async generate() {
        console.log('🚀 Starting concept map generation...\n');
        
        // Initialize embeddings service
        await this.extractor.initialize();
        
        // Load research papers
        const papers = await this.loader.loadAllPapers();
        if (papers.length === 0) {
            throw new Error('No papers loaded. Check source data path.');
        }
        
        // Extract concepts
        const concepts = await this.extractor.extractConcepts(papers);
        
        // Generate output data
        const conceptMap = {
            metadata: {
                generatedAt: new Date().toISOString(),
                totalPapers: papers.length,
                totalConcepts: concepts.length,
                embeddingModel: CONFIG.embeddingModel,
                version: '1.0.0'
            },
            concepts: concepts,
            papers: papers.map(paper => ({
                id: paper.id,
                title: paper.title,
                authors: paper.authors,
                abstract: paper.abstract,
                keywords: paper.keywords,
                venue: paper.venue,
                publicationDate: paper.publicationDate
            }))
        };
        
        // Ensure output directory exists
        const outputDir = path.resolve(__dirname, CONFIG.outputPath);
        await fs.mkdir(outputDir, { recursive: true });
        
        // Write output file
        const outputFile = path.join(outputDir, 'research-concept-map.json');
        await fs.writeFile(outputFile, JSON.stringify(conceptMap, null, 2));
        
        console.log(`\n✅ Concept map generated successfully!`);
        console.log(`   Output: ${outputFile}`);
        console.log(`   Papers: ${papers.length}`);
        console.log(`   Concepts: ${concepts.length}`);
        console.log(`   Relationships: ${concepts.reduce((sum, c) => sum + c.relationships.length, 0)}`);
        
        return conceptMap;
    }
}

// Main execution
async function main() {
    try {
        const generator = new ConceptMapGenerator();
        await generator.generate();
        process.exit(0);
    } catch (error) {
        console.error('❌ Error generating concept map:', error);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { ConceptMapGenerator, ResearchPaperData, ConceptCluster };
