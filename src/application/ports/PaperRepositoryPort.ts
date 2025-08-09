import { Paper } from '../../domain/entities/Paper';

/**
 * PaperRepositoryPort - Abstract interface for paper data access operations.
 * 
 * This port demonstrates the Dependency Inversion Principle by defining the interface
 * that the application layer needs, without depending on specific implementations.
 * The infrastructure layer will provide concrete implementations of this interface.
 * 
 * Educational Notes:
 * - Shows Port pattern in Clean Architecture for external dependencies
 * - Demonstrates dependency inversion - application defines what it needs
 * - Enables testability through dependency injection and mocking
 * - Separates business logic from data access concerns
 * 
 * Design Decisions:
 * - Async methods support various data sources (files, APIs, databases)
 * - Promise-based API for consistent error handling
 * - Filter methods enable flexible paper retrieval strategies
 * - Repository pattern abstracts data access complexity
 * 
 * Real-World Application:
 * Academic research tools need flexible data access - papers might come from
 * ArXiv APIs, local files, databases, or web scraping. This interface allows
 * the application logic to remain unchanged regardless of data source.
 * 
 * Integration Points:
 * - Used by ExtractConceptsUseCase to retrieve papers for processing
 * - Implemented by infrastructure layer (ArxivPaperRepository, FilePaperRepository)
 * - Mocked in unit tests for isolated use case testing
 * - Supports future data source additions without application changes
 */

export interface PaperRepositoryPort {
    /**
     * Retrieve all available papers from the data source.
     * 
     * Educational Note:
     * This method demonstrates the Repository pattern's query interface.
     * The application layer calls this without knowing if papers come from
     * a database, API, or file system.
     * 
     * @returns Promise of all available Paper entities
     * @throws RepositoryError when data access fails
     */
    findAll(): Promise<Paper[]>;

    /**
     * Retrieve papers that match specific criteria.
     * 
     * Educational Note:
     * This method shows how repository interfaces can provide flexible
     * filtering while maintaining abstraction. The implementation details
     * of filtering (SQL queries, API parameters, etc.) are hidden.
     * 
     * @param criteria Filtering criteria for paper selection
     * @returns Promise of matching Paper entities
     * @throws RepositoryError when filtering fails
     */
    findByQuery(criteria: PaperQueryCriteria): Promise<Paper[]>;

    /**
     * Retrieve a specific paper by its unique identifier.
     * 
     * Educational Note:
     * Identity-based retrieval is fundamental to entity management.
     * This method supports use cases that need to process specific papers.
     * 
     * @param id Unique identifier for the paper
     * @returns Promise of Paper entity or undefined if not found
     * @throws RepositoryError when retrieval fails
     */
    findById(id: string): Promise<Paper | undefined>;

    /**
     * Retrieve papers that have sufficient text content for concept extraction.
     * 
     * Educational Note:
     * This method demonstrates domain-specific repository methods that
     * support particular use cases. The filtering logic understands
     * what constitutes "sufficient" content for concept extraction.
     * 
     * @returns Promise of Papers suitable for concept extraction
     * @throws RepositoryError when filtering fails
     */
    findWithSufficientContent(): Promise<Paper[]>;
}

/**
 * Criteria for querying papers from the repository.
 * 
 * Educational Note:
 * This interface demonstrates the Specification pattern by encapsulating
 * query criteria in a structured way. It provides type safety and
 * clear contracts for filtering operations.
 */
export interface PaperQueryCriteria {
    /** Search terms to match against paper content */
    searchTerms?: string[];
    
    /** Filter by publication date range */
    dateRange?: {
        startDate?: Date;
        endDate?: Date;
    };
    
    /** Filter by minimum abstract length for quality */
    minAbstractLength?: number;
    
    /** Filter by paper source (ArXiv, manual upload, etc.) */
    source?: string;
    
    /** Limit number of results for performance */
    limit?: number;
}

/**
 * Error thrown when repository operations fail.
 * 
 * Educational Note:
 * Domain-specific exceptions provide clear error boundaries and
 * enable appropriate error handling at each architectural layer.
 */
export class RepositoryError extends Error {
    constructor(message: string, public readonly cause?: Error) {
        super(message);
        this.name = 'RepositoryError';
    }
}
