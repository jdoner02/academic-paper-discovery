/**
 * Test suite for Paper domain entity.
 *
 * This test module demonstrates Test-Driven Development (TDD) by defining the
 * complete behavior of the Paper entity before implementation. The tests serve
 * as both specification and validation for the core business logic.
 *
 * Educational Notes:
 * - Papers are entities because they have persistent identity (DOI, ArXiv ID)
 * - Identity-based equality means papers are the same if they have the same ID
 * - Rich domain models include behavior, not just data storage
 * - Immutability after creation ensures data consistency and thread safety
 *
 * Test Organization:
 * Tests are grouped by behavioral capabilities rather than just implementation
 * details, making them serve as living documentation of what Papers can do
 * in the research domain.
 */

// These imports will fail initially - that's the RED phase!
import { Paper } from '@/domain/entities/Paper';
import { EmbeddingVector } from '@/domain/value_objects/EmbeddingVector';
import { EvidenceSentence } from '@/domain/value_objects/EvidenceSentence';

describe('Paper Entity - Creation and Identity', () => {
  /**
   * Test paper creation and identity management.
   * 
   * Educational Note:
   * Entity identity is crucial in domain modeling. Papers have natural
   * identities (DOI, ArXiv ID) that persist even when metadata changes.
   * This reflects how researchers think about papers - same paper,
   * updated information.
   */

  test('should create paper with DOI as primary identity', () => {
    /**
     * Test creating a paper with DOI as primary identity.
     * 
     * Educational Note:
     * DOI (Digital Object Identifier) is the gold standard for academic
     * paper identification. It's immutable and globally unique.
     */
    // Arrange
    const doi = "10.1000/xyz123";
    const title = "Machine Learning in Academic Research";
    const authors = ["Smith, J.", "Johnson, A."];
    const abstract = "This paper explores ML applications in research.";
    
    // Act
    const paper = Paper.createWithDoi({
      doi,
      title,
      authors,
      abstract
    });
    
    // Assert
    expect(paper.doi).toBe(doi);
    expect(paper.title).toBe(title);
    expect(paper.authors).toEqual(authors);
    expect(paper.abstract).toBe(abstract);
    expect(paper.identity).toBe(doi); // DOI serves as identity
  });

  test('should create paper with ArXiv ID as primary identity', () => {
    /**
     * Test creating a paper with ArXiv ID as primary identity.
     * 
     * Educational Note:
     * ArXiv papers often don't have DOIs initially. The ArXiv ID
     * serves as the persistent identifier for preprints.
     */
    // Arrange
    const arxivId = "2301.12345";
    const title = "Novel Approaches to Paper Discovery";
    const authors = ["Davis, C."];
    
    // Act
    const paper = Paper.createWithArxivId({
      arxivId,
      title,
      authors
    });
    
    // Assert
    expect(paper.arxivId).toBe(arxivId);
    expect(paper.identity).toBe(arxivId);
    expect(paper.doi).toBeNull(); // No DOI for preprints
  });

  test('should have identity-based equality', () => {
    /**
     * Test that paper equality is based on identity, not attributes.
     * 
     * Educational Note:
     * Entity equality is about identity, not current state. Two papers
     * with the same DOI are the same paper, even if other attributes differ.
     * This reflects real-world scenarios where metadata gets updated.
     */
    // Arrange
    const doi = "10.1000/same-paper";
    
    const paper1 = Paper.createWithDoi({
      doi,
      title: "Original Title",
      authors: ["Smith, J."]
    });
    
    const paper2 = Paper.createWithDoi({
      doi,
      title: "Updated Title", // Different title
      authors: ["Smith, J.", "Johnson, A."] // Different authors
    });
    
    // Act & Assert
    expect(paper1.equals(paper2)).toBe(true); // Same identity = same paper
    expect(paper1.hashCode()).toBe(paper2.hashCode()); // Consistent hashing
  });

  test('should require identity for creation', () => {
    /**
     * Test that papers require some form of identity.
     * 
     * Educational Note:
     * Entities must have identity. Papers without DOI or ArXiv ID
     * need content-based identity generation to maintain entity semantics.
     */
    // Arrange & Act & Assert
    expect(() => {
      Paper.createWithoutExternalId({
        title: "", // Empty title can't generate identity
        authors: [] // Empty authors can't generate identity
      });
    }).toThrow("identity required");
  });
});

describe('Paper Entity - Business Behavior', () => {
  /**
   * Test paper business behavior and domain operations.
   * 
   * Educational Note:
   * Rich domain models include behavior relevant to the business domain.
   * Papers aren't just data containers - they can validate themselves,
   * provide derived information, and enforce business rules.
   */

  test('should determine research readiness', () => {
    /**
     * Test that papers can determine if they're ready for concept extraction.
     * 
     * Educational Note:
     * Business logic belongs in domain entities. Papers know what
     * constitutes sufficient content for meaningful analysis.
     */
    // Arrange - Paper with sufficient content
    const completePaper = Paper.createWithDoi({
      doi: "10.1000/complete",
      title: "Complete Research Paper",
      authors: ["Smith, J."],
      abstract: "Detailed abstract with sufficient content for analysis.",
      fullText: "Full paper content with multiple paragraphs and sections..."
    });
    
    // Arrange - Paper with insufficient content
    const incompletePaper = Paper.createWithDoi({
      doi: "10.1000/incomplete",
      title: "Title Only",
      authors: ["Smith, J."]
      // No abstract or full text
    });
    
    // Act & Assert
    expect(completePaper.isReadyForConceptExtraction()).toBe(true);
    expect(incompletePaper.isReadyForConceptExtraction()).toBe(false);
  });

  test('should track processing metadata', () => {
    /**
     * Test that papers can track their processing status and metadata.
     * 
     * Educational Note:
     * Papers need to track processing state for efficient pipeline operations.
     * This prevents reprocessing and provides audit trails.
     */
    // Arrange
    const paper = Paper.createWithDoi({
      doi: "10.1000/test",
      title: "Test Paper",
      authors: ["Test Author"]
    });
    
    const processingMetadata = {
      processedAt: "2025-08-05T10:30:00Z",
      extractionModel: "all-MiniLM-L6-v2",
      conceptCount: 15,
      confidenceScore: 0.89
    };
    
    // Act
    paper.addProcessingMetadata(processingMetadata);
    
    // Assert
    expect(paper.isProcessed()).toBe(true);
    expect(paper.processingMetadata?.conceptCount).toBe(15);
    expect(paper.processingMetadata?.confidenceScore).toBe(0.89);
  });

  test('should validate author format', () => {
    /**
     * Test that papers validate author name formats.
     * 
     * Educational Note:
     * Domain entities should validate their own data consistency.
     * Author names have academic conventions that should be enforced.
     */
    // Arrange & Act & Assert - Valid author formats
    const validAuthors = ["Smith, J.", "Johnson, A.B.", "van der Berg, C."];
    const paper = Paper.createWithDoi({
      doi: "10.1000/valid-authors",
      title: "Test Paper",
      authors: validAuthors
    });
    expect(paper.authors).toEqual(validAuthors);
    
    // Arrange & Act & Assert - Invalid author formats
    expect(() => {
      Paper.createWithDoi({
        doi: "10.1000/invalid",
        title: "Test Paper",
        authors: [""] // Empty author name
      });
    }).toThrow("Invalid author format");
  });

  test('should generate content summary', () => {
    /**
     * Test that papers can generate content summaries for display.
     * 
     * Educational Note:
     * Domain objects should provide derived information useful for
     * the business domain. Summaries help researchers quickly assess relevance.
     */
    // Arrange
    const paper = Paper.createWithDoi({
      doi: "10.1000/summary-test",
      title: "Advanced Machine Learning Techniques for Natural Language Processing",
      authors: ["Smith, J.", "Johnson, A.", "Brown, C."],
      abstract: "This paper presents novel approaches to NLP using deep learning. " +
               "We demonstrate significant improvements in text classification and " +
               "sentiment analysis tasks through innovative neural architectures.",
      fullText: "Extended content about neural networks and language models..."
    });
    
    // Act
    const summary = paper.generateContentSummary(100);
    
    // Assert
    expect(summary.length).toBeLessThanOrEqual(100);
    expect(summary.toLowerCase()).toMatch(/machine learning|ml/);
    expect(summary.toLowerCase()).toMatch(/nlp|natural language/);
    expect(summary).toMatch(/\.{3}$/); // Truncation indicator
  });
});
