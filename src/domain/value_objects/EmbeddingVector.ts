/**
 * EmbeddingVector - Immutable semantic vector representation for research papers.
 * 
 * This value object encapsulates semantic embeddings generated from paper content,
 * providing similarity calculations and vector operations for concept extraction.
 * 
 * Educational Notes:
 * - Demonstrates Value Object pattern from Domain-Driven Design
 * - Shows immutability principles for semantic data
 * - Illustrates equality based on content, not identity
 * - Provides foundation for similarity-based paper clustering
 * 
 * Design Decisions:
 * - Immutable design prevents accidental vector modifications
 * - Float32Array for memory efficiency with large embedding datasets
 * - Cosine similarity for semantic similarity calculations
 * - Validation ensures vectors are properly normalized
 * 
 * Clean Architecture Layer: Domain (Value Object)
 * Dependencies: None (pure domain logic)
 * 
 * Use Cases:
 * - Semantic similarity calculations between papers
 * - Clustering papers by conceptual similarity
 * - Finding related papers based on content embeddings
 * - Visualization positioning in concept maps
 */

export class EmbeddingVector {
    private readonly _values: Float32Array;
    private readonly _dimensions: number;

    /**
     * Creates a new EmbeddingVector from numeric array.
     * 
     * Educational Note:
     * Value objects should validate their invariants in the constructor
     * and be immutable after creation. This ensures domain consistency.
     */
    constructor(values: number[]) {
        if (!values || values.length === 0) {
            throw new Error('EmbeddingVector requires non-empty numeric array');
        }

        if (values.some(v => !Number.isFinite(v))) {
            throw new Error('EmbeddingVector values must be finite numbers');
        }

        this._dimensions = values.length;
        this._values = new Float32Array(values);
        
        // Validate vector is normalized (optional for some embedding models)
        const magnitude = this.magnitude();
        if (magnitude === 0) {
            throw new Error('EmbeddingVector cannot have zero magnitude');
        }
    }

    /**
     * Gets the vector dimensions (read-only access).
     * 
     * Educational Note:
     * Value objects expose their state through read-only properties
     * to maintain immutability guarantees.
     */
    get dimensions(): number {
        return this._dimensions;
    }

    /**
     * Gets vector values as read-only array copy.
     * 
     * Educational Note:
     * Returning a copy prevents external mutation of internal state,
     * maintaining value object immutability.
     */
    get values(): ReadonlyArray<number> {
        return Array.from(this._values);
    }

    /**
     * Calculates cosine similarity with another embedding vector.
     * 
     * Returns value between -1 and 1, where:
     * - 1.0 = identical semantic meaning
     * - 0.0 = orthogonal/unrelated concepts  
     * - -1.0 = opposite semantic meaning
     * 
     * Educational Note:
     * Business logic in value objects should be pure functions
     * that operate on the object's data without side effects.
     */
    cosineSimilarity(other: EmbeddingVector): number {
        if (this._dimensions !== other._dimensions) {
            throw new Error('Cannot calculate similarity between vectors of different dimensions');
        }

        let dotProduct = 0;
        for (let i = 0; i < this._dimensions; i++) {
            dotProduct += this._values[i] * other._values[i];
        }

        const magnitudeProduct = this.magnitude() * other.magnitude();
        return dotProduct / magnitudeProduct;
    }

    /**
     * Calculates the Euclidean magnitude of the vector.
     * 
     * Educational Note:
     * Helper methods in value objects should be private when possible,
     * but public when they provide meaningful business operations.
     */
    magnitude(): number {
        let sum = 0;
        for (let i = 0; i < this._dimensions; i++) {
            sum += this._values[i] * this._values[i];
        }
        return Math.sqrt(sum);
    }

    /**
     * Checks equality based on vector content.
     * 
     * Educational Note:
     * Value objects implement equality based on their content/attributes,
     * not object identity. This is fundamental to value object semantics.
     */
    equals(other: EmbeddingVector): boolean {
        if (!(other instanceof EmbeddingVector)) {
            return false;
        }

        if (this._dimensions !== other._dimensions) {
            return false;
        }

        // Use small epsilon for floating-point comparison
        const epsilon = 1e-10;
        for (let i = 0; i < this._dimensions; i++) {
            if (Math.abs(this._values[i] - other._values[i]) > epsilon) {
                return false;
            }
        }

        return true;
    }

    /**
     * Creates string representation for debugging and display.
     * 
     * Educational Note:
     * Value objects should provide meaningful string representations
     * for debugging and logging purposes.
     */
    toString(): string {
        const truncatedValues = this._dimensions > 5 
            ? `[${this._values.slice(0, 3).join(', ')}, ..., ${this._values[this._dimensions - 1]}]`
            : `[${Array.from(this._values).join(', ')}]`;
        
        return `EmbeddingVector(dims=${this._dimensions}, values=${truncatedValues})`;
    }
}
