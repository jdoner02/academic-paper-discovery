import { ExtractConceptsUseCase } from '../../src/application/use_cases/ExtractConceptsUseCase';
import { PaperRepositoryPort } from '../../src/application/ports/PaperRepositoryPort';
import { ConceptRepositoryPort } from '../../src/application/ports/ConceptRepositoryPort';
import { EmbeddingsServicePort } from '../../src/application/ports/EmbeddingsServicePort';
import { Paper } from '../../src/domain/entities/Paper';
import { ConceptNode } from '../../src/domain/entities/ConceptNode';
import { EmbeddingVector } from '../../src/domain/value_objects/EmbeddingVector';

/**
 * ExtractConceptsUseCase Integration Test Suite
 * 
 * This test suite validates the ExtractConceptsUseCase following Test-Driven Development
 * principles and integration testing best practices.
 * 
 * Educational Notes:
 * - Integration tests validate coordination between multiple components
 * - Tests focus on business workflows rather than individual object behavior
 * - Mock objects isolate the use case from external dependencies
 * - Tests demonstrate Clean Architecture dependency inversion principles
 */

describe('ExtractConceptsUseCase', () => {
  // Mock implementations for dependencies
  let mockPaperRepository: jest.Mocked<PaperRepositoryPort>;
  let mockConceptRepository: jest.Mocked<ConceptRepositoryPort>;
  let mockEmbeddingsService: jest.Mocked<EmbeddingsServicePort>;
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
      findConceptHierarchies: jest.fn(),
      findSimilarConcepts: jest.fn(),
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

  describe('Core Use Case Workflow', () => {
    test('extracts concepts from single paper successfully', async () => {
      // RED PHASE: This test will fail because ExtractConceptsUseCase doesn't exist yet
      
      // Arrange - Set up mock responses
      mockPaperRepository.findById.mockResolvedValue(samplePaper);
      mockEmbeddingsService.generateEmbedding.mockResolvedValue(sampleEmbedding);
      mockConceptRepository.saveConcepts.mockResolvedValue();

      // Act - Execute the use case
      const result = await extractConceptsUseCase.execute({
        paperId: samplePaper.identity,
        maxConcepts: 5,
        confidenceThreshold: 0.7,
      });

      // Assert - Verify expected outcomes
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.concepts).toHaveLength(5);
      expect(result.processingTimeMs).toBeGreaterThan(0);

      // Verify repository interactions occurred
      expect(mockPaperRepository.findById).toHaveBeenCalledWith(samplePaper.identity);
      expect(mockConceptRepository.saveConcepts).toHaveBeenCalled();
      expect(mockEmbeddingsService.generateEmbedding).toHaveBeenCalled();
    });

    test('handles paper not found gracefully', async () => {
      // Arrange
      mockPaperRepository.findById.mockResolvedValue(undefined);

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

    test('processes multiple papers efficiently', async () => {
      // Arrange
      const papers = [samplePaper, samplePaper]; // Simplified for testing
      mockPaperRepository.findAll.mockResolvedValue(papers);
      mockEmbeddingsService.batchGenerateEmbeddings.mockResolvedValue([sampleEmbedding, sampleEmbedding]);
      mockConceptRepository.saveConcepts.mockResolvedValue();

      // Act
      const result = await extractConceptsUseCase.executeBatch({
        paperIds: papers.map(p => p.identity),
        buildHierarchy: true,
        maxDepth: 3,
      });

      // Assert
      expect(result.success).toBe(true);
      expect(result.totalConceptsExtracted).toBeGreaterThan(0);
      
      // Verify batch processing occurred
      expect(mockEmbeddingsService.batchGenerateEmbeddings).toHaveBeenCalled();
    });

    test('validates input parameters', async () => {
      // Act & Assert - Invalid confidence threshold
      await expect(extractConceptsUseCase.execute({
        paperId: samplePaper.identity,
        maxConcepts: 5,
        confidenceThreshold: 1.5, // Invalid: > 1.0
      })).rejects.toThrow('Confidence threshold must be between 0 and 1');

      // Act & Assert - Invalid max concepts
      await expect(extractConceptsUseCase.execute({
        paperId: samplePaper.identity,
        maxConcepts: 0, // Invalid: must be positive
        confidenceThreshold: 0.7,
      })).rejects.toThrow('Max concepts must be greater than 0');
    });
  });
});
