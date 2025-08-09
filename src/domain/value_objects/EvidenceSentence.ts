/**
 * EvidenceSentence - Immutable text evidence with confidence scoring.
 * 
 * This value object represents textual evidence supporting concept extraction,
 * with confidence scores and formatting capabilities for display in concept maps.
 * 
 * Educational Notes:
 * - Demonstrates Value Object pattern for domain-specific text data
 * - Shows confidence modeling for uncertain NLP extractions
 * - Illustrates display formatting separation from core domain logic
 * - Provides foundation for evidence-based concept validation
 * 
 * Design Decisions:
 * - Immutable design prevents accidental evidence modification
 * - Confidence score as percentage (0-100) for intuitive interpretation
 * - Text truncation with smart word boundaries for display
 * - Validation ensures evidence integrity and meaningful content
 * 
 * Clean Architecture Layer: Domain (Value Object)
 * Dependencies: None (pure domain logic)
 * 
 * Use Cases:
 * - Supporting concept extraction with textual evidence
 * - Displaying evidence in interactive concept maps
 * - Ranking evidence by confidence for user interfaces
 * - Validating concept accuracy through source text
 */

export class EvidenceSentence {
    private readonly _text: string;
    private readonly _confidence: number;
    private readonly _sourcePosition: number;

    /**
     * Creates a new EvidenceSentence with text and confidence score.
     * 
     * Educational Note:
     * Value objects validate their business invariants in the constructor.
     * This ensures that invalid evidence never enters the domain model.
     * 
     * @param text The textual evidence (must be meaningful content)
     * @param confidence Confidence score 0-100 (percentage)
     * @param sourcePosition Character position in source document
     */
    constructor(text: string, confidence: number, sourcePosition: number = 0) {
        if (!text || text.trim().length === 0) {
            throw new Error('EvidenceSentence requires non-empty text content');
        }

        if (text.trim().length < 10) {
            throw new Error('EvidenceSentence text must be at least 10 characters for meaningful evidence');
        }

        if (!Number.isFinite(confidence) || confidence < 0 || confidence > 100) {
            throw new Error('EvidenceSentence confidence must be between 0 and 100');
        }

        if (!Number.isInteger(sourcePosition) || sourcePosition < 0) {
            throw new Error('EvidenceSentence sourcePosition must be non-negative integer');
        }

        this._text = text.trim();
        this._confidence = confidence;
        this._sourcePosition = sourcePosition;
    }

    /**
     * Gets the evidence text content (read-only).
     * 
     * Educational Note:
     * Value objects expose their state through read-only properties
     * to prevent external mutations that would violate immutability.
     */
    get text(): string {
        return this._text;
    }

    /**
     * Gets the confidence score as percentage 0-100 (read-only).
     * 
     * Educational Note:
     * Confidence modeling is crucial for NLP-extracted evidence
     * where uncertainty is inherent to the extraction process.
     */
    get confidence(): number {
        return this._confidence;
    }

    /**
     * Gets the source document position (read-only).
     * 
     * Educational Note:
     * Source position enables traceability back to original document
     * for validation and citation purposes in research contexts.
     */
    get sourcePosition(): number {
        return this._sourcePosition;
    }

    /**
     * Returns truncated text for display with smart word boundaries.
     * 
     * Educational Note:
     * Presentation logic in value objects should be simple formatting
     * that doesn't require external dependencies or complex business rules.
     * 
     * @param maxLength Maximum character length for display
     * @returns Truncated text with "..." if needed
     */
    truncateForDisplay(maxLength: number = 100): string {
        if (this._text.length <= maxLength) {
            return this._text;
        }

        // Find last complete word within limit
        const truncated = this._text.substring(0, maxLength);
        const lastSpaceIndex = truncated.lastIndexOf(' ');
        
        if (lastSpaceIndex > maxLength * 0.7) {
            // Use word boundary if it's not too far back
            return truncated.substring(0, lastSpaceIndex) + '...';
        } else {
            // Hard truncate with ellipsis
            return truncated + '...';
        }
    }

    /**
     * Returns confidence level as qualitative description.
     * 
     * Educational Note:
     * Converting quantitative confidence to qualitative labels
     * helps non-technical users interpret evidence reliability.
     */
    getConfidenceLevel(): 'Low' | 'Medium' | 'High' | 'Very High' {
        if (this._confidence >= 90) return 'Very High';
        if (this._confidence >= 75) return 'High';
        if (this._confidence >= 50) return 'Medium';
        return 'Low';
    }

    /**
     * Checks if evidence meets minimum confidence threshold.
     * 
     * Educational Note:
     * Business rules about confidence thresholds belong in the domain
     * as they represent research methodology decisions.
     */
    isHighConfidence(threshold: number = 75): boolean {
        return this._confidence >= threshold;
    }

    /**
     * Checks equality based on content and confidence.
     * 
     * Educational Note:
     * Value objects implement equality based on all their attributes.
     * Two evidence sentences are equal if they have the same text,
     * confidence, and source position.
     */
    equals(other: EvidenceSentence): boolean {
        if (!(other instanceof EvidenceSentence)) {
            return false;
        }

        return this._text === other._text &&
               this._confidence === other._confidence &&
               this._sourcePosition === other._sourcePosition;
    }

    /**
     * Creates string representation for debugging and display.
     * 
     * Educational Note:
     * Value object string representations should show all relevant
     * attributes for debugging and logging purposes.
     */
    toString(): string {
        const displayText = this.truncateForDisplay(50);
        return `EvidenceSentence(confidence=${this._confidence}%, pos=${this._sourcePosition}, text="${displayText}")`;
    }

    /**
     * Creates formatted display string for user interfaces.
     * 
     * Educational Note:
     * Separating debugging representation (toString) from user-facing
     * formatting (toDisplayString) follows single responsibility principle.
     */
    toDisplayString(): string {
        const confidenceLevel = this.getConfidenceLevel();
        const displayText = this.truncateForDisplay(150);
        return `${displayText} (${confidenceLevel} confidence)`;
    }
}
