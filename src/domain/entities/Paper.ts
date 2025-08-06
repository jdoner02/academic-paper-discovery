/**
 * Paper Entity - Core Domain Entity for Academic Research Papers
 * 
 * This class demonstrates Clean Architecture Entity patterns and Domain-Driven Design principles.
 * As a domain entity, it encapsulates business rules and behavior while maintaining independence
 * from infrastructure concerns.
 * 
 * Educational Notes:
 * - Shows Entity pattern with identity-based equality (DOI, ArXiv ID, or title/authors)
 * - Demonstrates Factory Method pattern for object creation with different identity strategies
 * - Illustrates Value Object composition (EmbeddingVector, EvidenceSentence)
 * - Implements Domain Event concepts through processing metadata
 * - Maintains Rich Domain Model with business behavior, not just data containers
 * 
 * Design Decisions:
 * - Private constructor enforces factory method usage for controlled object creation
 * - Immutable identity after creation prevents entity identity corruption
 * - Mutable processing metadata allows for lifecycle state changes
 * - Static factory methods handle different paper identity strategies
 * 
 * SOLID Principles Applied:
 * - Single Responsibility: Manages paper identity, validation, and business behavior
 * - Open/Closed: Extensible through inheritance, closed for modification of core identity
 * - Liskov Substitution: Any Paper instance can be used polymorphically
 * - Interface Segregation: Clean separation of creation, identity, and processing concerns
 * - Dependency Inversion: Depends on domain value objects, not infrastructure details
 * 
 * Clean Architecture Compliance:
 * - Domain Layer: Pure business logic with no external dependencies
 * - Business Rules: Validation and behavior rules encapsulated within entity
 * - Technology Independence: No framework or database dependencies
 * 
 * Use Cases:
 * - Academic paper identity management across different sources (DOI, ArXiv, manual entry)
 * - Content processing pipeline tracking with metadata
 * - Concept extraction preparation and validation
 * - Research paper aggregation and deduplication
 */

import { EmbeddingVector } from '../value_objects/EmbeddingVector';
import { EvidenceSentence } from '../value_objects/EvidenceSentence';

// Domain Constants - Business Rules and Validation Patterns
const VALIDATION_PATTERNS = {
    DOI: /^10\.\d+\/.+$/,
    ARXIV_ID: /^\d{4}\.\d{4,5}(v\d+)?$/
} as const;

const CONTENT_LIMITS = {
    DEFAULT_SUMMARY_LENGTH: 500,
    TRUNCATION_THRESHOLD: 0.7,
    MIN_SUMMARY_BUFFER: 10
} as const;

const ERROR_MESSAGES = {
    INVALID_DOI: "Invalid DOI format. Expected format: 10.xxxx/xxxxx",
    INVALID_ARXIV: "Invalid ArXiv ID format. Expected format: YYYY.NNNNN or YYYY.NNNNNvN",
    EMPTY_TITLE: "Title cannot be empty",
    EMPTY_AUTHORS: "Authors array cannot be empty",
    INVALID_AUTHOR: "Invalid author format: author names cannot be empty strings",
    IDENTITY_REQUIRED: "Papers require either DOI, ArXiv ID, or non-empty title with authors for identity"
} as const;

// Domain Types - Processing Metadata Structure for Paper Lifecycle Tracking
export interface ProcessingMetadata {
    processedAt: string;
    extractionModel: string;
    conceptCount: number;
    confidenceScore: number;
}

export interface PaperProps {
    doi?: string | null;
    arxivId?: string | null;
    title: string;
    authors: string[];
    abstract?: string;
    fullText?: string;
    publishedDate?: Date;
    journal?: string;
    url?: string;
}

export interface ValidationResult {
    isValid: boolean;
    missingFields: string[];
    errors: string[];
}

export class Paper {
    private readonly _doi: string | null;
    private readonly _arxivId: string | null;
    private readonly _title: string;
    private readonly _authors: readonly string[];
    private readonly _abstract: string;
    private readonly _fullText?: string;
    private readonly _publishedDate?: Date;
    private readonly _journal?: string;
    private readonly _url?: string;
    private readonly _identity: string;
    private readonly _createdAt: Date;
    private _processingMetadata?: ProcessingMetadata;

    /**
     * Creates a new Paper entity with identity and metadata.
     */
    private constructor(props: PaperProps, identity: string) {
        // Validate required fields
        if (!props.title || props.title.trim().length === 0) {
            throw new Error('Paper title is required');
        }

        if (!props.authors || props.authors.length === 0) {
            throw new Error('Paper must have at least one author');
        }

        // Validate author names - no empty strings
        for (const author of props.authors) {
            if (!author || author.trim().length === 0) {
                throw new Error('Invalid author format');
            }
        }

        // Validate DOI format if provided
        if (props.doi && !Paper.isValidDOI(props.doi)) {
            throw new Error('Invalid DOI format: ' + props.doi);
        }

        // Validate ArXiv ID format if provided
        if (props.arxivId && !Paper.isValidArXivId(props.arxivId)) {
            throw new Error('Invalid ArXiv ID format: ' + props.arxivId);
        }

        // Set identity and metadata
        this._doi = props.doi || null;
        this._arxivId = props.arxivId || null;
        this._title = props.title.trim();
        this._authors = Object.freeze([...props.authors]);
        this._abstract = props.abstract?.trim() || '';
        this._fullText = props.fullText?.trim();
        this._publishedDate = props.publishedDate;
        this._journal = props.journal?.trim();
        this._url = props.url?.trim();
        this._identity = identity;
        this._createdAt = new Date();
    }

    /**
     * Creates a paper with DOI as primary identity.
     */
    static createWithDoi(props: Omit<PaperProps, 'arxivId'> & { doi: string }): Paper {
        if (!props.doi || props.doi.trim().length === 0) {
            throw new Error('DOI is required for createWithDoi');
        }

        return new Paper(
            { ...props, doi: props.doi, arxivId: null },
            props.doi
        );
    }

    /**
     * Creates a paper with ArXiv ID as primary identity.
     */
    static createWithArxivId(props: Omit<PaperProps, 'doi'> & { arxivId: string }): Paper {
        if (!props.arxivId || props.arxivId.trim().length === 0) {
            throw new Error('ArXiv ID is required for createWithArxivId');
        }

        return new Paper(
            { ...props, doi: null, arxivId: props.arxivId },
            props.arxivId
        );
    }

    /**
     * Creates a paper without external ID, using content-based identity.
     */
    static createWithoutExternalId(props: Omit<PaperProps, 'doi' | 'arxivId'>): Paper {
        // Check if we have enough content for identity generation
        if ((!props.title || props.title.trim().length === 0) && 
            (!props.authors || props.authors.length === 0)) {
            throw new Error('Insufficient content for identity generation - identity required');
        }
        
        if (!props.title || props.title.trim().length === 0) {
            throw new Error('Title is required for identity generation');
        }

        if (!props.authors || props.authors.length === 0) {
            throw new Error('Authors are required for identity generation');
        }

        // Generate content-based identity
        const content = props.title.trim() + ':' + props.authors.join(',');
        if (content.length < 10) {
            throw new Error('Insufficient content for identity generation - identity required');
        }

        const contentHash = Paper.simpleHash(content);
        const identity = 'content:' + contentHash;

        return new Paper(
            { ...props, doi: null, arxivId: null },
            identity
        );
    }

    /**
     * Gets the paper's unique identity.
     */
    get identity(): string {
        return this._identity;
    }

    /**
     * Gets the paper's DOI if available.
     */
    get doi(): string | null {
        return this._doi;
    }

    /**
     * Gets the paper's ArXiv ID if available.
     */
    get arxivId(): string | null {
        return this._arxivId;
    }

    /**
     * Gets the paper's title.
     */
    get title(): string {
        return this._title;
    }

    /**
     * Gets the paper's authors as readonly array.
     */
    get authors(): readonly string[] {
        return this._authors;
    }

    /**
     * Gets the paper's abstract.
     */
    get abstract(): string {
        return this._abstract;
    }

    /**
     * Gets the paper's full text if available.
     */
    get fullText(): string | undefined {
        return this._fullText;
    }

    /**
     * Gets the paper's published date if available.
     */
    get publishedDate(): Date | undefined {
        return this._publishedDate;
    }

    /**
     * Gets the paper's journal if available.
     */
    get journal(): string | undefined {
        return this._journal;
    }

    /**
     * Gets the paper's URL if available.
     */
    get url(): string | undefined {
        return this._url;
    }

    /**
     * Gets when the paper was created in the system.
     */
    get createdAt(): Date {
        return this._createdAt;
    }

    /**
     * Gets hash code for consistent hashing based on identity.
     */
    hashCode(): number {
        return Paper.simpleHashNumber(this._identity);
    }

    /**
     * Checks if paper is ready for concept processing.
     */
    isReadyForProcessing(): boolean {
        const validation = this.validateRequiredFields();
        if (!validation.isValid) {
            return false;
        }

        // Require either full text or substantial abstract
        const hasContent = this._fullText || this._abstract.length >= 200;
        if (!hasContent) {
            return false;
        }

        return true;
    }

    /**
     * Checks if paper is ready for concept extraction.
     * (Alias for isReadyForProcessing to match test expectations)
     */
    isReadyForConceptExtraction(): boolean {
        return this.isReadyForProcessing();
    }

    /**
     * Gets the processing metadata.
     */
    get processingMetadata(): ProcessingMetadata | undefined {
        return this._processingMetadata;
    }

    /**
     * Adds processing metadata to track concept extraction results.
     */
    addProcessingMetadata(metadata: ProcessingMetadata): void {
        this._processingMetadata = metadata;
    }    /**
     * Checks if paper has been processed for concept extraction.
     */
    isProcessed(): boolean {
        return this._processingMetadata !== undefined && this._processingMetadata !== null;
    }

    /**
     * Validates that paper has all required fields for processing.
     */
    validateRequiredFields(): ValidationResult {
        const errors: string[] = [];
        const missingFields: string[] = [];

        // Check identity
        if (!this._identity) {
            missingFields.push('identity');
            errors.push('Paper must have identity');
        }

        // Check required metadata
        if (!this._title) {
            missingFields.push('title');
        }

        if (!this._authors || this._authors.length === 0) {
            missingFields.push('authors');
        }

        // Validate author names
        if (this._authors) {
            for (const author of this._authors) {
                if (!author || author.trim().length === 0) {
                    errors.push('All author names must be non-empty');
                    break;
                }
            }
        }

        return {
            isValid: errors.length === 0 && missingFields.length === 0,
            missingFields,
            errors
        };
    }

    /**
     * Generates content summary for concept extraction.
     */
    generateSummary(maxLength: number = 500): string {
        // Start with title and authors
        const authorList = this._authors.length <= 3 
            ? this._authors.join(', ')
            : this._authors.slice(0, 3).join(', ') + ' et al.';
        
        let summary = this._title + ' by ' + authorList + '.\n\n';
        
        // Calculate remaining space for abstract
        const remainingLength = maxLength - summary.length;
        
        if (remainingLength <= 10) {
            // Not enough space, just return title truncated
            return this._title.substring(0, maxLength - 3) + '...';
        }
        
        // Add abstract, truncating if necessary
        if (this._abstract.length <= remainingLength) {
            summary += this._abstract;
        } else {
            const truncated = this._abstract.substring(0, remainingLength - 3);
            const lastSentenceEnd = Math.max(
                truncated.lastIndexOf('.'),
                truncated.lastIndexOf('!'),
                truncated.lastIndexOf('?')
            );
            
            if (lastSentenceEnd > truncated.length * 0.7) {
                summary += truncated.substring(0, lastSentenceEnd + 1);
            } else {
                summary += truncated + '...';
            }
        }

        return summary;
    }

    /**
     * Generates content summary for display.
     * (Alias for generateSummary to match test expectations)
     */
    generateContentSummary(maxLength: number = 500): string {
        return this.generateSummary(maxLength);
    }

    /**
     * Checks equality based on paper identity.
     */
    equals(other: Paper): boolean {
        if (!(other instanceof Paper)) {
            return false;
        }

        return this._identity === other._identity;
    }

    /**
     * Creates string representation for debugging.
     */
    toString(): string {
        const authors = this._authors.length <= 2 
            ? this._authors.join(', ')
            : this._authors[0] + ' et al.';
        
        return 'Paper(' + this._identity + ', "' + this._title + '" by ' + authors + ')';
    }

    /**
     * Validates DOI format according to academic standards.
     */
    private static isValidDOI(doi: string): boolean {
        // Basic DOI format: 10.xxxx/xxxxx
        const doiRegex = /^10\.\d{4,}\/\S+$/;
        return doiRegex.test(doi);
    }

    /**
     * Validates ArXiv ID format according to ArXiv standards.
     */
    private static isValidArXivId(arxivId: string): boolean {
        // Modern ArXiv format: arXiv:YYMM.NNNNN[vN] or just YYMM.NNNNN[vN]
        // Legacy format: subject-class/YYMMnnn
        const modernRegex = /^(arXiv:)?\d{4}\.\d{4,5}(v\d+)?$/i;
        const legacyRegex = /^[a-z-]+(\.[A-Z]{2})?\/\d{7}$/;
        
        return modernRegex.test(arxivId) || legacyRegex.test(arxivId);
    }

    /**
     * Simple hash function for content-based IDs.
     */
    private static simpleHash(str: string): string {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash).toString(16);
    }

    /**
     * Simple hash function that returns number for hashCode method.
     */
    private static simpleHashNumber(str: string): number {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash);
    }
}
