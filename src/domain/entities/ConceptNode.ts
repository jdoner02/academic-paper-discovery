import { EmbeddingVector } from '../value_objects/EmbeddingVector';

/**
 * ConceptNode - Individual concept within hierarchical research topic structure.
 * 
 * This entity demonstrates Clean Architecture principles by maintaining identity while
 * encapsulating complex hierarchical relationships and evidence management.
 * 
 * Educational Notes:
 * - Shows Entity pattern with clear identity and lifecycle management
 * - Demonstrates bidirectional relationship management in domain entities
 * - Illustrates aggregation of value objects for complex data structures
 * - Exemplifies domain logic encapsulation following DDD principles
 * 
 * Design Decisions:
 * - Hierarchical Position: Enables tree navigation and relationship queries
 * - Evidence Aggregation: Links abstract concepts to concrete textual support
 * - Semantic Vectors: Enables similarity calculations for concept clustering
 * - Identity Management: Supports entity lifecycle and change tracking
 * 
 * Real-World Application:
 * Academic researchers need to understand how concepts relate within research domains.
 * This entity models individual nodes in concept hierarchies, enabling researchers
 * to navigate from broad themes to specific implementation details while maintaining
 * clear evidence trails back to source papers.
 * 
 * Integration Points:
 * - Works with EmbeddingVector for semantic similarity calculations
 * - Aggregates EvidenceSentence instances for textual evidence
 * - Participates in concept tree structures for hierarchical navigation
 * - Interfaces with visualization layer for interactive concept mapping
 */

export class ConceptNode {
    private readonly _id: string;
    private readonly _label: string;
    private readonly _embedding: EmbeddingVector;
    private _parentId?: string;
    private _hierarchyLevel: number;
    private readonly _childIds: string[] = [];
    private readonly _evidenceMap: Map<string, number> = new Map();
    private readonly _createdAt: Date;

    /**
     * Creates a new ConceptNode with required domain properties.
     * 
     * Educational Note:
     * Entity constructors validate business invariants and establish identity.
     * Unlike value objects, entities can have mutable state through controlled methods.
     * 
     * @param id Unique identifier for this concept
     * @param label Human-readable concept name
     * @param embedding Semantic vector for similarity calculations
     * @param parentId Optional parent concept ID for hierarchy
     * @param hierarchyLevel Depth in concept tree (0 = root)
     */
    constructor(
        id: string, 
        label: string, 
        embedding: EmbeddingVector,
        parentId?: string,
        hierarchyLevel: number = 0
    ) {
        if (!id || id.trim().length === 0) {
            throw new Error('Concept ID cannot be empty');
        }

        if (!label || label.trim().length === 0) {
            throw new Error('Concept label cannot be empty');
        }

        if (!embedding) {
            throw new Error('Embedding vector is required');
        }

        this._id = id.trim();
        this._label = label.trim();
        this._embedding = embedding;
        this._parentId = parentId;
        this._hierarchyLevel = hierarchyLevel;
        this._createdAt = new Date();
    }

    // Getters for immutable properties
    get id(): string { return this._id; }
    get label(): string { return this._label; }
    get embedding(): EmbeddingVector { return this._embedding; }
    get parentId(): string | undefined { return this._parentId; }
    get hierarchyLevel(): number { return this._hierarchyLevel; }
    get childIds(): string[] { return [...this._childIds]; }
    get evidenceCount(): number { return this._evidenceMap.size; }
    get childCount(): number { return this._childIds.length; }
    get createdAt(): Date { return new Date(this._createdAt.getTime()); }

    /**
     * Implements identity-based equality for entities.
     * 
     * Educational Note:
     * Entities are equal if they have the same identity (ID), regardless
     * of other properties. This enables tracking entities through state changes.
     */
    equals(other: ConceptNode): boolean {
        if (!other || !(other instanceof ConceptNode)) {
            return false;
        }
        return this._id === other._id;
    }

    /**
     * Provides consistent hash code based on entity identity.
     * 
     * Educational Note:
     * Hash codes must be stable for entity identity and consistent with equality.
     * This enables using entities as Map keys or in Sets reliably.
     */
    hashCode(): number {
        let hash = 0;
        for (let i = 0; i < this._id.length; i++) {
            const char = this._id.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return hash;
    }

    /**
     * Add a child concept to this node's hierarchy.
     * 
     * Educational Note:
     * This method demonstrates entity state management while maintaining
     * business invariants. It prevents duplicate relationships and maintains
     * hierarchy integrity.
     */
    addChild(childId: string): void {
        if (!childId || childId.trim().length === 0) {
            throw new Error('Child concept ID cannot be empty');
        }

        const trimmedChildId = childId.trim();
        if (trimmedChildId === this._id) {
            throw new Error('Concept cannot be its own child');
        }

        if (!this._childIds.includes(trimmedChildId)) {
            this._childIds.push(trimmedChildId);
        }
    }

    /**
     * Remove a child concept from this node's hierarchy.
     * 
     * Educational Note:
     * Demonstrates safe state modification with proper cleanup.
     * The method is idempotent - removing non-existent children is safe.
     */
    removeChild(childId: string): void {
        const index = this._childIds.indexOf(childId);
        if (index !== -1) {
            this._childIds.splice(index, 1);
        }
    }

    /**
     * Set parent concept and update hierarchy level.
     * 
     * Educational Note:
     * This method coordinates multiple properties to maintain consistency.
     * It shows how entities can have complex state transitions while
     * preserving business invariants.
     */
    setParent(parentId: string, hierarchyLevel: number): void {
        if (!parentId || parentId.trim().length === 0) {
            throw new Error('Parent concept ID cannot be empty');
        }

        if (parentId === this._id) {
            throw new Error('Concept cannot be its own parent');
        }

        this._parentId = parentId.trim();
        this._hierarchyLevel = hierarchyLevel;
    }

    /**
     * Clear parent relationship, making this a root concept.
     */
    clearParent(): void {
        this._parentId = undefined;
        this._hierarchyLevel = 0;
    }

    /**
     * Determine if this is a root concept (no parent).
     */
    isRootNode(): boolean {
        return this._parentId === undefined;
    }

    /**
     * Determine if this is a leaf concept (no children).
     */
    isLeafNode(): boolean {
        return this._childIds.length === 0;
    }

    /**
     * Add evidence sentence with confidence score.
     * 
     * Educational Note:
     * This method manages the aggregation of evidence data while
     * maintaining domain constraints on confidence scores.
     */
    addEvidence(evidenceId: string, confidence: number): void {
        if (!evidenceId || evidenceId.trim().length === 0) {
            throw new Error('Evidence ID cannot be empty');
        }

        if (confidence < 0 || confidence > 1) {
            throw new Error('Confidence score must be between 0 and 1');
        }

        this._evidenceMap.set(evidenceId.trim(), confidence);
    }

    /**
     * Get confidence score for specific evidence.
     */
    getEvidenceConfidence(evidenceId: string): number | undefined {
        return this._evidenceMap.get(evidenceId);
    }

    /**
     * Calculate overall evidence strength as average confidence.
     * 
     * Educational Note:
     * This method demonstrates domain calculation logic that aggregates
     * multiple data points into a single meaningful metric for business use.
     */
    calculateEvidenceStrength(): number {
        if (this._evidenceMap.size === 0) {
            return 0;
        }

        const totalConfidence = Array.from(this._evidenceMap.values())
            .reduce((sum, confidence) => sum + confidence, 0);
        
        return totalConfidence / this._evidenceMap.size;
    }

    /**
     * Get evidence IDs above confidence threshold.
     * 
     * Educational Note:
     * This method shows how entities can provide filtered views of their
     * data based on business criteria, supporting various use cases.
     */
    getEvidenceAboveThreshold(threshold: number): string[] {
        return Array.from(this._evidenceMap.entries())
            .filter(([, confidence]) => confidence >= threshold)
            .map(([evidenceId]) => evidenceId);
    }

    /**
     * Calculate semantic similarity with another concept.
     * 
     * Educational Note:
     * This method delegates to the embedding vector for the core calculation,
     * following the principle of leveraging value objects for specialized logic.
     */
    calculateSimilarity(other: ConceptNode): number {
        return this._embedding.cosineSimilarity(other._embedding);
    }

    /**
     * Calculate evidence-weighted similarity with another concept.
     * 
     * Educational Note:
     * This method demonstrates how entities can combine multiple domain
     * concepts (similarity + evidence strength) to create more sophisticated
     * business calculations.
     */
    calculateEvidenceWeightedSimilarity(other: ConceptNode): number {
        const baseSimilarity = this.calculateSimilarity(other);
        const thisStrength = this.calculateEvidenceStrength();
        const otherStrength = other.calculateEvidenceStrength();
        
        // Weight the similarity by the average evidence strength
        const evidenceMultiplier = (thisStrength + otherStrength) / 2;
        
        return baseSimilarity * Math.max(evidenceMultiplier, 0.1); // Prevent zero multiplication
    }

    /**
     * Find concepts similar above threshold from candidate list.
     * 
     * Educational Note:
     * This method shows how entities can perform complex filtering and
     * analysis operations, encapsulating business logic within domain objects.
     */
    findSimilarConcepts(candidates: ConceptNode[], threshold: number): ConceptNode[] {
        return candidates.filter(candidate => {
            const similarity = this.calculateSimilarity(candidate);
            return similarity >= threshold;
        });
    }

    /**
     * String representation for debugging and logging.
     */
    toString(): string {
        return `ConceptNode(id=${this._id}, label="${this._label}", level=${this._hierarchyLevel})`;
    }
}
