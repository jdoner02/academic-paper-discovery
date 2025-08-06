/**
 * ConceptNode Entity Unit Tests
 * 
 * These tests verify the ConceptNode entity behavior, focusing on hierarchical 
 * relationships, evidence aggregation, and domain logic using the actual API.
 */

import { ConceptNode } from '../../src/domain/entities/ConceptNode';
import { EmbeddingVector } from '../../src/domain/value_objects/EmbeddingVector';

describe('ConceptNode Entity', () => {
  let parentEmbedding: EmbeddingVector;
  let childEmbedding: EmbeddingVector;

  beforeEach(() => {
    parentEmbedding = new EmbeddingVector([0.5, 0.8, 0.1, 0.3, 0.7]);
    childEmbedding = new EmbeddingVector([0.4, 0.9, 0.0, 0.2, 0.6]);
  });

  describe('Entity Creation and Identity', () => {
    it('should create concept node with required properties', () => {
      const concept = new ConceptNode(
        'hrv-analysis',
        'Heart Rate Variability Analysis',
        parentEmbedding
      );

      expect(concept.id).toBe('hrv-analysis');
      expect(concept.label).toBe('Heart Rate Variability Analysis');
      expect(concept.embedding).toBe(parentEmbedding);
      expect(concept.hierarchyLevel).toBe(0);
      expect(concept.parentId).toBeUndefined();
    });

    it('should create concept node with hierarchy information', () => {
      const concept = new ConceptNode(
        'child-concept',
        'Child Concept',
        childEmbedding,
        'parent-id',
        2
      );

      expect(concept.id).toBe('child-concept');
      expect(concept.label).toBe('Child Concept');
      expect(concept.parentId).toBe('parent-id');
      expect(concept.hierarchyLevel).toBe(2);
    });

    it('should have identity-based equality', () => {
      const concept1 = new ConceptNode('same-id', 'Name 1', parentEmbedding);
      const concept2 = new ConceptNode('same-id', 'Name 2', childEmbedding);
      const concept3 = new ConceptNode('different-id', 'Name 1', parentEmbedding);

      expect(concept1.equals(concept2)).toBe(true);
      expect(concept1.equals(concept3)).toBe(false);
    });

    it('should validate required properties', () => {
      expect(() => new ConceptNode('', 'Valid Name', parentEmbedding))
        .toThrow('Concept ID cannot be empty');

      expect(() => new ConceptNode('valid-id', '', parentEmbedding))
        .toThrow('Concept label cannot be empty');

      expect(() => new ConceptNode('valid-id', 'Valid Name', null as any))
        .toThrow('Embedding vector is required');
    });
  });

  describe('Hierarchical Relationships', () => {
    let parentConcept: ConceptNode;
    let childConcept: ConceptNode;

    beforeEach(() => {
      parentConcept = new ConceptNode('parent', 'Parent Concept', parentEmbedding);
      childConcept = new ConceptNode('child', 'Child Concept', childEmbedding);
    });

    it('should add child concepts', () => {
      parentConcept.addChild('child-1');
      parentConcept.addChild('child-2');

      expect(parentConcept.childIds).toContain('child-1');
      expect(parentConcept.childIds).toContain('child-2');
      expect(parentConcept.childCount).toBe(2);
    });

    it('should prevent duplicate child relationships', () => {
      parentConcept.addChild('child-1');
      parentConcept.addChild('child-1'); // Should not duplicate

      expect(parentConcept.childIds).toEqual(['child-1']);
      expect(parentConcept.childCount).toBe(1);
    });

    it('should remove child concepts', () => {
      parentConcept.addChild('child-1');
      parentConcept.addChild('child-2');
      parentConcept.removeChild('child-1');

      expect(parentConcept.childIds).not.toContain('child-1');
      expect(parentConcept.childIds).toContain('child-2');
      expect(parentConcept.childCount).toBe(1);
    });

    it('should set parent relationship', () => {
      childConcept.setParent('parent-id', 1);

      expect(childConcept.parentId).toBe('parent-id');
      expect(childConcept.hierarchyLevel).toBe(1);
      expect(childConcept.isRootNode()).toBe(false);
    });

    it('should clear parent relationship', () => {
      childConcept.setParent('parent-id', 2);
      childConcept.clearParent();

      expect(childConcept.parentId).toBeUndefined();
      expect(childConcept.hierarchyLevel).toBe(0);
      expect(childConcept.isRootNode()).toBe(true);
    });

    it('should detect root and leaf nodes', () => {
      const rootConcept = new ConceptNode('root', 'Root', parentEmbedding);
      const leafConcept = new ConceptNode('leaf', 'Leaf', childEmbedding, 'parent', 1);

      expect(rootConcept.isRootNode()).toBe(true);
      expect(leafConcept.isRootNode()).toBe(false);
      expect(rootConcept.isLeafNode()).toBe(true);
      expect(leafConcept.isLeafNode()).toBe(true);

      rootConcept.addChild('child-id');
      expect(rootConcept.isLeafNode()).toBe(false);
    });

    it('should prevent self-referential relationships', () => {
      expect(() => parentConcept.addChild('parent'))
        .toThrow('Concept cannot be its own child');

      expect(() => childConcept.setParent('child', 1))
        .toThrow('Concept cannot be its own parent');
    });
  });

  describe('Evidence Management', () => {
    let concept: ConceptNode;

    beforeEach(() => {
      concept = new ConceptNode('test', 'Test Concept', parentEmbedding);
    });

    it('should add evidence with confidence scores', () => {
      concept.addEvidence('evidence-1', 0.85);
      concept.addEvidence('evidence-2', 0.75);

      expect(concept.evidenceCount).toBe(2);
      expect(concept.getEvidenceConfidence('evidence-1')).toBe(0.85);
      expect(concept.getEvidenceConfidence('evidence-2')).toBe(0.75);
    });

    it('should calculate evidence strength as average confidence', () => {
      concept.addEvidence('evidence-1', 0.8);
      concept.addEvidence('evidence-2', 0.6);
      concept.addEvidence('evidence-3', 1.0);

      const expectedStrength = (0.8 + 0.6 + 1.0) / 3;
      expect(concept.calculateEvidenceStrength()).toBeCloseTo(expectedStrength, 2);
    });

    it('should return zero strength when no evidence', () => {
      expect(concept.calculateEvidenceStrength()).toBe(0);
    });

    it('should filter evidence by confidence threshold', () => {
      concept.addEvidence('low-conf', 0.3);
      concept.addEvidence('med-conf', 0.6);
      concept.addEvidence('high-conf', 0.9);

      const highConfidenceEvidence = concept.getEvidenceAboveThreshold(0.7);
      expect(highConfidenceEvidence).toEqual(['high-conf']);

      const mediumConfidenceEvidence = concept.getEvidenceAboveThreshold(0.5);
      expect(mediumConfidenceEvidence).toEqual(['med-conf', 'high-conf']);
    });

    it('should validate confidence score range', () => {
      expect(() => concept.addEvidence('invalid', -0.1))
        .toThrow('Confidence score must be between 0 and 1');

      expect(() => concept.addEvidence('invalid', 1.5))
        .toThrow('Confidence score must be between 0 and 1');
    });
  });

  describe('Semantic Operations', () => {
    let concept1: ConceptNode;
    let concept2: ConceptNode;
    let concept3: ConceptNode;

    beforeEach(() => {
      concept1 = new ConceptNode('c1', 'Concept 1', parentEmbedding);
      concept2 = new ConceptNode('c2', 'Concept 2', childEmbedding);
      concept3 = new ConceptNode('c3', 'Concept 3', new EmbeddingVector([0.1, 0.2, 0.3, 0.4, 0.5]));
    });

    it('should calculate semantic similarity with other concepts', () => {
      const similarity = concept1.calculateSimilarity(concept2);

      expect(typeof similarity).toBe('number');
      expect(similarity).toBeGreaterThanOrEqual(-1);
      expect(similarity).toBeLessThanOrEqual(1);
    });

    it('should calculate evidence-weighted similarity', () => {
      concept1.addEvidence('evidence-1', 0.8);
      concept2.addEvidence('evidence-2', 0.6);

      const baseSimilarity = concept1.calculateSimilarity(concept2);
      const weightedSimilarity = concept1.calculateEvidenceWeightedSimilarity(concept2);

      expect(weightedSimilarity).toBeGreaterThan(0);
      expect(weightedSimilarity).not.toBe(baseSimilarity);
    });

    it('should find similar concepts above threshold', () => {
      // Add evidence to make concepts meaningful
      concept1.addEvidence('evidence-1', 0.9);
      concept2.addEvidence('evidence-2', 0.8);
      concept3.addEvidence('evidence-3', 0.7);

      const candidates = [concept2, concept3];
      const similar = concept1.findSimilarConcepts(candidates, 0.1); // Low threshold

      expect(similar.length).toBeGreaterThanOrEqual(0);
      expect(similar.length).toBeLessThanOrEqual(2);
      
      // All returned concepts should meet the threshold
      similar.forEach(candidate => {
        const similarity = concept1.calculateSimilarity(candidate);
        expect(similarity).toBeGreaterThanOrEqual(0.1);
      });
    });
  });

  describe('Utility Methods', () => {
    it('should generate consistent hash codes', () => {
      const concept1 = new ConceptNode('same-id', 'Name 1', parentEmbedding);
      const concept2 = new ConceptNode('same-id', 'Name 2', childEmbedding);

      expect(concept1.hashCode()).toBe(concept2.hashCode());
    });

    it('should provide readable string representation', () => {
      const concept = new ConceptNode('test-id', 'Test Concept', parentEmbedding, 'parent-id', 2);
      const stringRep = concept.toString();

      expect(stringRep).toContain('test-id');
      expect(stringRep).toContain('Test Concept');
      expect(stringRep).toContain('2');
    });
  });
});
