import { EmbeddingVector } from '../../domain/value_objects/EmbeddingVector';

/**
 * EmbeddingServicePort - Abstract interface for semantic embedding generation.
 * 
 * This port defines the contract for generating semantic embeddings from text,
 * demonstrating how the application layer can depend on AI/ML services without
 * coupling to specific implementations. It enables flexible embedding strategies
 * while maintaining clean separation of concerns.
 * 
 * Educational Notes:
 * - Shows Port/Adapter pattern for external AI/ML service integration
 * - Demonstrates dependency inversion for machine learning components
 * - Enables testing with mock embeddings for deterministic results
 * - Supports different embedding models without application code changes
 * 
 * Design Decisions:
 * - Async operations support both local and remote embedding services
 * - Batch processing optimizes performance for large text collections
 * - Error handling addresses common ML service failures (rate limits, model errors)
 * - Configuration interface allows model-specific parameter tuning
 * 
 * Real-World Application:
 * Academic concept extraction requires high-quality semantic embeddings to
 * identify conceptual relationships. This interface allows the application
 * to work with various embedding services (local sentence-transformers,
 * OpenAI API, Cohere, etc.) without changing business logic.
 * 
 * Integration Points:
 * - Used by ExtractConceptsUseCase for sentence and concept embedding generation
 * - Implemented by infrastructure layer (SentenceTransformersAdapter, OpenAIAdapter)
 * - Mocked in tests with deterministic vectors for reproducible results
 * - Supports embedding model evolution and experimentation
 */

export interface EmbeddingServicePort {
    /**
     * Generate embedding vector for a single text input.
     * 
     * Educational Note:
     * This method demonstrates the basic interface for text-to-vector
     * transformation. It abstracts the complexity of tokenization,
     * model inference, and vector normalization.
     * 
     * @param text Input text to generate embedding for
     * @param options Configuration for embedding generation
     * @returns Promise of EmbeddingVector for the input text
     * @throws EmbeddingError when generation fails
     */
    generateEmbedding(text: string, options?: EmbeddingOptions): Promise<EmbeddingVector>;

    /**
     * Generate embedding vectors for multiple text inputs efficiently.
     * 
     * Educational Note:
     * Batch processing is crucial for performance with ML services.
     * This method enables optimizations like batched inference and
     * reduced network overhead for remote services.
     * 
     * @param texts Array of input texts to generate embeddings for
     * @param options Configuration for batch embedding generation
     * @returns Promise of EmbeddingVector array matching input order
     * @throws EmbeddingError when batch generation fails
     */
    generateBatchEmbeddings(texts: string[], options?: EmbeddingOptions): Promise<EmbeddingVector[]>;

    /**
     * Get information about the embedding model capabilities.
     * 
     * Educational Note:
     * This method demonstrates how ports can expose metadata about
     * underlying implementations to support application decisions
     * about processing strategies and compatibility.
     * 
     * @returns Promise of embedding model metadata
     */
    getModelInfo(): Promise<EmbeddingModelInfo>;

    /**
     * Validate that text is suitable for embedding generation.
     * 
     * Educational Note:
     * This method shows how ports can provide domain-specific validation
     * that prevents common errors (empty text, excessive length) before
     * expensive operations are attempted.
     * 
     * @param text Input text to validate
     * @param options Configuration for validation
     * @returns Promise resolving if text is valid
     * @throws EmbeddingError if text is unsuitable for embedding
     */
    validateText(text: string, options?: EmbeddingOptions): Promise<void>;

    /**
     * Calculate semantic similarity between two text inputs.
     * 
     * Educational Note:
     * This convenience method demonstrates how ports can provide
     * higher-level operations that combine multiple steps (embedding + similarity)
     * for common use cases, improving performance and simplifying usage.
     * 
     * @param text1 First text for comparison
     * @param text2 Second text for comparison  
     * @param options Configuration for similarity calculation
     * @returns Promise of similarity score between 0 and 1
     * @throws EmbeddingError when similarity calculation fails
     */
    calculateTextSimilarity(text1: string, text2: string, options?: EmbeddingOptions): Promise<number>;
}

/**
 * Configuration options for embedding generation.
 * 
 * Educational Note:
 * This interface demonstrates how ports can expose configurable parameters
 * while maintaining abstraction. Different embedding services might have
 * different parameters, but common ones are standardized here.
 */
export interface EmbeddingOptions {
    /** Model-specific parameters for embedding generation */
    modelParameters?: Record<string, any>;
    
    /** Maximum text length to process (service-dependent) */
    maxTextLength?: number;
    
    /** Whether to normalize embedding vectors */
    normalize?: boolean;
    
    /** Batch size for batch operations */
    batchSize?: number;
    
    /** Timeout for embedding generation operations */
    timeoutMs?: number;
}

/**
 * Information about the embedding model capabilities and characteristics.
 * 
 * Educational Note:
 * This interface demonstrates how ports can provide metadata about
 * underlying implementations to support intelligent application behavior
 * without tight coupling.
 */
export interface EmbeddingModelInfo {
    /** Name/identifier of the embedding model */
    modelName: string;
    
    /** Dimensionality of generated embedding vectors */
    dimensions: number;
    
    /** Maximum text length the model can process */
    maxSequenceLength: number;
    
    /** Whether the model produces normalized vectors */
    isNormalized: boolean;
    
    /** Description of the model's training data and capabilities */
    description: string;
    
    /** Version identifier for the model */
    version: string;
}

/**
 * Error thrown when embedding generation operations fail.
 * 
 * Educational Note:
 * Domain-specific exceptions provide clear error boundaries and
 * enable appropriate error handling strategies for different
 * types of failures (network, model, validation, etc.).
 */
export class EmbeddingError extends Error {
    constructor(
        message: string, 
        public readonly errorType: EmbeddingErrorType,
        public readonly cause?: Error
    ) {
        super(message);
        this.name = 'EmbeddingError';
    }
}

/**
 * Types of embedding-related errors for specific handling.
 */
export enum EmbeddingErrorType {
    /** Text input validation failed */
    INVALID_INPUT = 'INVALID_INPUT',
    
    /** Embedding service is unavailable */
    SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
    
    /** Request exceeded service rate limits */
    RATE_LIMITED = 'RATE_LIMITED',
    
    /** Model-specific error during inference */
    MODEL_ERROR = 'MODEL_ERROR',
    
    /** Network/communication error with service */
    NETWORK_ERROR = 'NETWORK_ERROR',
    
    /** Unknown or unexpected error */
    UNKNOWN = 'UNKNOWN'
}
