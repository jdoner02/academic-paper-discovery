import { ConceptNode } from '../../domain/entities/ConceptNode';

/**
 * ConceptRepositoryPort - Abstract interface for concept data persistence operations.
 * 
 * This port defines the contract for storing and retrieving extracted concepts,
 * demonstrating the Repository pattern in the application layer. It enables
 * the application to persist concept hierarchies without depending on specific
 * storage implementations.
 * 
 * Educational Notes:
 * - Shows Repository pattern for complex domain aggregates (concept hierarchies)
 * - Demonstrates application layer defining its persistence needs
 * - Enables different storage strategies (JSON, database, cache) without code changes
 * - Supports concept evolution and versioning through abstract interface
 * 
 * Design Decisions:
 * - Async operations support various storage backends
 * - Batch operations optimize performance for large concept sets
 * - Query methods enable flexible concept retrieval for visualization
 * - Hierarchical operations respect domain model relationships
 * 
 * Real-World Application:
 * Research concept extraction generates hierarchical data that needs persistent
 * storage for visualization, caching, and incremental updates. This interface
 * allows the application logic to work with concepts without knowing if they're
 * stored in files, databases, or memory.
 * 
 * Integration Points:
 * - Used by ExtractConceptsUseCase to persist extracted concept hierarchies
 * - Used by BuildVisualizationDataUseCase to retrieve concepts for display
 * - Implemented by infrastructure layer (JsonConceptRepository, DatabaseConceptRepository)
 * - Mocked in tests for isolated use case validation
 */

export interface ConceptRepositoryPort {
    /**
     * Store a collection of related concept nodes.
     * 
     * Educational Note:
     * This method demonstrates batch persistence for domain aggregates.
     * Concepts are often created in hierarchical groups that should be
     * persisted atomically to maintain referential integrity.
     * 
     * @param concepts Array of ConceptNode entities to store
     * @param sourceContext Metadata about the source papers
     * @returns Promise resolving when storage completes
     * @throws RepositoryError when persistence fails
     */
    saveConcepts(concepts: ConceptNode[], sourceContext: ConceptSourceContext): Promise<void>;

    /**
     * Retrieve all concepts related to specific source papers.
     * 
     * Educational Note:
     * This method shows how repository interfaces can provide domain-specific
     * queries that understand the relationships between entities (papers → concepts).
     * 
     * @param paperIds Array of Paper entity IDs
     * @returns Promise of ConceptNode entities extracted from those papers
     * @throws RepositoryError when retrieval fails
     */
    findConceptsByPaperIds(paperIds: string[]): Promise<ConceptNode[]>;

    /**
     * Retrieve root-level concepts (concepts with no parents).
     * 
     * Educational Note:
     * This method demonstrates domain-aware queries that understand
     * the hierarchical structure of concepts. Root concepts represent
     * the highest-level themes in the research domain.
     * 
     * @returns Promise of top-level ConceptNode entities
     * @throws RepositoryError when filtering fails
     */
    findRootConcepts(): Promise<ConceptNode[]>;

    /**
     * Retrieve complete concept hierarchy starting from root concepts.
     * 
     * Educational Note:
     * This method shows how repository interfaces can provide complex
     * aggregate retrieval that respects domain model relationships
     * and supports specific use cases like visualization.
     * 
     * @param rootConceptIds Array of root concept IDs to expand
     * @returns Promise of complete ConceptNode hierarchies
     * @throws RepositoryError when hierarchy reconstruction fails
     */
    findConceptHierarchies(rootConceptIds: string[]): Promise<ConceptNode[]>;

    /**
     * Find concepts similar to a given concept above a threshold.
     * 
     * Educational Note:
     * This method demonstrates domain-specific repository operations that
     * leverage the semantic capabilities of the domain model (embedding
     * vectors and similarity calculations).
     * 
     * @param targetConcept Concept to find similarities for
     * @param similarityThreshold Minimum similarity score (0-1)
     * @returns Promise of similar ConceptNode entities
     * @throws RepositoryError when similarity search fails
     */
    findSimilarConcepts(targetConcept: ConceptNode, similarityThreshold: number): Promise<ConceptNode[]>;

    /**
     * Delete concepts and their hierarchical relationships.
     * 
     * Educational Note:
     * This method shows how repository operations must respect domain
     * model constraints. Deleting concepts requires careful handling
     * of hierarchical relationships to maintain data integrity.
     * 
     * @param conceptIds Array of concept IDs to delete
     * @returns Promise resolving when deletion completes
     * @throws RepositoryError when deletion fails or violates constraints
     */
    deleteConcepts(conceptIds: string[]): Promise<void>;
}

/**
 * Context metadata for concept storage operations.
 * 
 * Educational Note:
 * This interface demonstrates how repository operations can include
 * metadata that supports auditing, versioning, and traceability
 * without cluttering the core domain model.
 */
export interface ConceptSourceContext {
    /** IDs of source papers that generated these concepts */
    sourcePaperIds: string[];
    
    /** Timestamp when concepts were extracted */
    extractedAt: Date;
    
    /** Algorithm version used for concept extraction */
    extractionAlgorithmVersion: string;
    
    /** Configuration parameters used during extraction */
    extractionParameters: Record<string, any>;
    
    /** Quality metrics for the extraction process */
    qualityMetrics?: {
        averageConfidenceScore: number;
        conceptCount: number;
        hierarchyDepth: number;
    };
}
