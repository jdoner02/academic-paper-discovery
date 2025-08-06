import { ExtractConceptsUseCase } from '../../src/application/use_cases/ExtractConceptsUseCase';
import { PaperRepositoryPort } from '../../src/application/ports/PaperRepositoryPort';
import { ConceptRepositoryPort } from '../../src/application/ports/ConceptRepositoryPort';
import { EmbeddingServicePort } from '../../src/application/ports/EmbeddingServicePort';
import { Paper } from '../../src/domain/entities/Paper';
import { ConceptNode } from '../../src/domain/entities/ConceptNode';
import { EmbeddingVector } from '../../src/domain/value_objects/EmbeddingVector';

/**
 * ExtractConceptsUseCase Integration Test Suite
 * 
 * This test suite validates the ExtractConceptsUseCase following Test-Driven Development
 * principles and integration testing best practices. It demonstrates use case orchestration
 * testing patterns and serves as executable documentation for business logic coordination.
 * 
 * Educational Notes:
 * - Integration tests validate coordination between multiple components
 * - Tests focus on business workflows rather than individual object behavior
 * - Mock objects isolate the use case from external dependencies
 * - Tests demonstrate Clean Architecture dependency inversion principles
 * 
 * Test Organization:
 * 1. Use Case Orchestration: End-to-end business workflow validation
 * 2. Error Handling: Graceful failure scenarios and error propagation
 * 3. Repository Integration: Data access coordination and persistence
 * 4. Service Integration: External service coordination (embeddings, etc.)
 */

describe('ExtractConceptsUseCase', () => {
  // Mock implementations for dependencies
  let mockPaperRepository: jest.Mocked<PaperRepositoryPort>;
  let mockConceptRepository: jest.Mocked<ConceptRepositoryPort>;
  let mockEmbeddingService: jest.Mocked<EmbeddingServicePort>;
  let extractConceptsUseCase: ExtractConceptsUseCase;

  // Test data setup
  const samplePaper = Paper.createWithDoi({
    doi: '10.1000/test-paper',
    title: 'Machine Learning in Healthcare', 
    authors: ['Dr. Smith', 'Dr. Johnson'],
    abstract: 'This paper explores machine learning applications in healthcare...',
    publishedDate: new Date('2024-01-15')
  });

  const sampleEmbedding = new EmbeddingVector([0.1, 0.2, 0.3, 0.4, 0.5]);

  beforeEach(() => {
    // Create mock implementations following repository port interfaces
    mockPaperRepository = {
      findById: jest.fn(),
      findAll: jest.fn(),
      findByQuery: jest.fn(),
      findWithSufficientContent: jest.fn(),
    };

    mockConceptRepository = {
      saveConcepts: jest.fn(),
      findConceptsByPaperIds: jest.fn(),
      findRootConcepts: jest.fn(),
      findConceptHierarchy: jest.fn(),
      findConceptsByEmbeddingSimilarity: jest.fn(),
    };

    mockEmbeddingsService = {
      generateEmbedding: jest.fn(),
      calculateSimilarity: jest.fn(),
      batchGenerateEmbeddings: jest.fn(),
    };

    extractConceptsUseCase = new ExtractConceptsUseCase(
      mockPaperRepository,
      mockConceptRepository,
      mockEmbeddingsService
    );
  });

  describe('Use Case Orchestration', () => {
    /**
     * This test group validates end-to-end business workflows:
     * - Complete paper processing pipeline
     * - Concept extraction and hierarchy building
     * - Repository coordination and data persistence
     * - Service integration for embeddings generation
     */

    test('extracts concepts from single paper successfully', async () => {
      // RED PHASE: This test will fail because ExtractConceptsUseCase doesn't exist yet
      
      // Arrange - Set up mock responses
      mockPaperRepository.findById.mockResolvedValue(samplePaper);
      mockEmbeddingsService.generateEmbedding.mockResolvedValue(sampleEmbedding);
      mockConceptRepository.save.mockResolvedValue();

      // Act - Execute the use case
      const result = await extractConceptsUseCase.execute({
        paperId: samplePaper.id,
        maxConcepts: 5,
        confidenceThreshold: 0.7,
      });

      // Assert - Verify expected outcomes
      expect(result).toBeDefined();
      expect(result.concepts).toHaveLength(5);
      expect(result.success).toBe(true);
      expect(result.processingTime).toBeGreaterThan(0);

      // Verify repository interactions
      expect(mockPaperRepository.findById).toHaveBeenCalledWith(samplePaper.id);
      expect(mockConceptRepository.save).toHaveBeenCalled();
      expect(mockEmbeddingsService.generateEmbedding).toHaveBeenCalled();
    });

    test('processes multiple papers and builds concept hierarchy', async () => {
      // Arrange - Multiple papers for hierarchy testing
      const papers = [samplePaper, samplePaper]; // Simplified for testing
      mockPaperRepository.findAll.mockResolvedValue(papers);
      mockEmbeddingsService.batchGenerateEmbeddings.mockResolvedValue([sampleEmbedding, sampleEmbedding]);
      mockConceptRepository.save.mockResolvedValue();

      // Act
      const result = await extractConceptsUseCase.executeBatch({
        paperIds: papers.map(p => p.id),
        buildHierarchy: true,
        maxDepth: 3,
      });

      // Assert
      expect(result.success).toBe(true);
      expect(result.conceptHierarchy).toBeDefined();
      expect(result.conceptHierarchy.rootConcepts.length).toBeGreaterThan(0);
      
      // Verify batch processing occurred
      expect(mockEmbeddingsService.batchGenerateEmbeddings).toHaveBeenCalled();
      expect(mockConceptRepository.save).toHaveBeenCalledTimes(result.conceptHierarchy.totalConcepts);
    });

    test('handles empty paper collection gracefully', async () => {
      // Arrange
      mockPaperRepository.findAll.mockResolvedValue([]);

      // Act
      const result = await extractConceptsUseCase.executeBatch({
        paperIds: [],
        buildHierarchy: false,
      });

      // Assert
      expect(result.success).toBe(true);
      expect(result.concepts).toHaveLength(0);
      expect(result.message).toContain('No papers provided for processing');
    });
  });

  describe('Error Handling', () => {
    /**
     * This test group validates error scenarios and recovery:
     * - Repository failures and error propagation
     * - Service unavailability handling
     * - Invalid input validation
     * - Partial failure recovery
     */

    test('handles paper not found gracefully', async () => {
      // Arrange
      mockPaperRepository.findById.mockResolvedValue(null);

      // Act
      const result = await extractConceptsUseCase.execute({
        paperId: 'non-existent-id',
        maxConcepts: 5,
        confidenceThreshold: 0.7,
      });

      // Assert
      expect(result.success).toBe(false);
      expect(result.error).toContain('Paper not found');
      expect(result.concepts).toHaveLength(0);
    });

    test('handles embeddings service failure', async () => {
      // Arrange
      mockPaperRepository.findById.mockResolvedValue(samplePaper);
      mockEmbeddingsService.generateEmbedding.mockRejectedValue(
        new Error('Embeddings service unavailable')
      );

      // Act
      const result = await extractConceptsUseCase.execute({
        paperId: samplePaper.id,
        maxConcepts: 5,
        confidenceThreshold: 0.7,
      });

      // Assert
      expect(result.success).toBe(false);
      expect(result.error).toContain('Failed to generate embeddings');
      
      // Verify no concepts were saved on failure
      expect(mockConceptRepository.save).not.toHaveBeenCalled();
    });

    test('validates input parameters', async () => {
      // Act & Assert - Invalid confidence threshold
      await expect(extractConceptsUseCase.execute({
        paperId: samplePaper.id,
        maxConcepts: 5,
        confidenceThreshold: 1.5, // Invalid: > 1.0
      })).rejects.toThrow('Confidence threshold must be between 0 and 1');

      // Act & Assert - Invalid max concepts
      await expect(extractConceptsUseCase.execute({
        paperId: samplePaper.id,
        maxConcepts: 0, // Invalid: must be positive
        confidenceThreshold: 0.7,
      })).rejects.toThrow('Max concepts must be greater than 0');
    });
  });

  describe('Repository Integration', () => {
    /**
     * This test group validates data access coordination:
     * - Proper repository method calls
     * - Data transformation and persistence
     * - Transaction-like behavior for consistency
     * - Query optimization strategies
     */

    test('coordinates paper and concept repository interactions', async () => {
      // Arrange
      mockPaperRepository.findById.mockResolvedValue(samplePaper);
      mockEmbeddingsService.generateEmbedding.mockResolvedValue(sampleEmbedding);
      mockConceptRepository.save.mockResolvedValue();

      // Act
      await extractConceptsUseCase.execute({
        paperId: samplePaper.id,
        maxConcepts: 3,
        confidenceThreshold: 0.8,
      });

      // Assert - Verify interaction sequence
      expect(mockPaperRepository.findById).toHaveBeenCalledBefore(
        mockEmbeddingsService.generateEmbedding as jest.Mock
      );
      expect(mockEmbeddingsService.generateEmbedding).toHaveBeenCalledBefore(
        mockConceptRepository.save as jest.Mock
      );
    });

    test('handles repository transaction failures', async () => {
      // Arrange
      mockPaperRepository.findById.mockResolvedValue(samplePaper);
      mockEmbeddingsService.generateEmbedding.mockResolvedValue(sampleEmbedding);
      mockConceptRepository.save.mockRejectedValue(new Error('Database connection failed'));

      // Act
      const result = await extractConceptsUseCase.execute({
        paperId: samplePaper.id,
        maxConcepts: 5,
        confidenceThreshold: 0.7,
      });

      // Assert
      expect(result.success).toBe(false);
      expect(result.error).toContain('Failed to save concepts');
    });
  });

  describe('Service Integration', () => {
    /**
     * This test group validates external service coordination:
     * - Embeddings generation and caching strategies  
     * - Batch processing optimization
     * - Service timeout and retry logic
     * - Performance monitoring integration
     */

    test('optimizes embeddings generation with batch processing', async () => {
      // Arrange
      const multiplePapers = Array(10).fill(samplePaper);
      mockPaperRepository.findAll.mockResolvedValue(multiplePapers);
      mockEmbeddingsService.batchGenerateEmbeddings.mockResolvedValue(
        Array(10).fill(sampleEmbedding)
      );
      mockConceptRepository.save.mockResolvedValue();

      // Act
      const result = await extractConceptsUseCase.executeBatch({
        paperIds: multiplePapers.map(p => p.id),
        buildHierarchy: true,
      });

      // Assert
      expect(result.success).toBe(true);
      // Should use batch processing for efficiency
      expect(mockEmbeddingsService.batchGenerateEmbeddings).toHaveBeenCalledTimes(1);
      // Should not call single embedding generation
      expect(mockEmbeddingsService.generateEmbedding).not.toHaveBeenCalled();
    });

    test('falls back to individual processing on batch failure', async () => {
      // Arrange
      const multiplePapers = [samplePaper, samplePaper];
      mockPaperRepository.findAll.mockResolvedValue(multiplePapers);
      mockEmbeddingsService.batchGenerateEmbeddings.mockRejectedValue(
        new Error('Batch processing failed')
      );
      mockEmbeddingsService.generateEmbedding.mockResolvedValue(sampleEmbedding);
      mockConceptRepository.save.mockResolvedValue();

      // Act
      const result = await extractConceptsUseCase.executeBatch({
        paperIds: multiplePapers.map(p => p.id),
        buildHierarchy: false,
      });

      // Assert
      expect(result.success).toBe(true);
      // Should fall back to individual processing
      expect(mockEmbeddingsService.generateEmbedding).toHaveBeenCalledTimes(2);
      expect(result.message).toContain('Fell back to individual processing');
    });
  });
});
