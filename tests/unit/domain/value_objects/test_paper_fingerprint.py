"""
Unit tests for PaperFingerprint - Duplicate detection across sources.

This module tests the PaperFingerprint value object that enables identification
of the same paper across different academic databases. Academic papers often
appear in multiple sources (ArXiv, PubMed, Google Scholar) and we need robust
duplicate detection to avoid processing the same paper multiple times.

Educational Notes:
- Value Object Pattern: Immutable objects identified by their attributes
- Hashing Strategy: Multiple fields combined for robust identification
- Academic Paper Identity: Papers have multiple identifiers (DOI, ArXiv ID, PMID)
- Fuzzy Matching: Title similarity handles minor formatting differences

Design Patterns Demonstrated:
- Value Object Pattern: Identity based on attributes, not reference
- Strategy Pattern: Multiple fingerprinting strategies for different scenarios
- Builder Pattern: Flexible construction from various paper attributes
- Template Method Pattern: Common fingerprinting algorithm with pluggable components

Duplicate Detection Challenges:
Academic papers present unique challenges for duplicate detection:
- Same paper may have different titles (preprint vs published version)
- Multiple identifiers: DOI, ArXiv ID, PMID, PubMed Central ID
- Author name variations: "J. Smith" vs "John Smith" vs "Smith, J."
- Publication date differences between preprint and final publication
- Abstract formatting differences across sources

Testing Strategy:
Following TDD approach to define robust duplicate detection behavior:
1. Test basic fingerprint creation from paper attributes
2. Test equality detection for obvious duplicates (same DOI)
3. Test similarity detection for near-duplicates (title variations)
4. Test edge cases (missing identifiers, corrupt data)
5. Test performance with large datasets

Architecture Integration:
PaperFingerprint is a domain value object that encapsulates the logic
for paper identity determination. It works with the multi-source repository
system to prevent duplicate processing and storage.
"""

import pytest
from datetime import datetime, timezone
from typing import Optional

from src.domain.entities.research_paper import ResearchPaper


class TestPaperFingerprintCreation:
    """
    Test creation of PaperFingerprint value objects.
    
    Educational Note:
    These tests define how paper fingerprints are created from research papers,
    establishing the core identity mechanism for duplicate detection.
    """
    
    def test_create_fingerprint_from_paper_with_doi(self):
        """
        Test fingerprint creation for paper with DOI.
        
        Educational Note:
        DOI (Digital Object Identifier) is the gold standard for academic
        paper identification. When available, it should be the primary
        component of the fingerprint.
        """
        # This will fail until we implement PaperFingerprint
        from src.domain.value_objects.paper_fingerprint import PaperFingerprint
        
        paper = ResearchPaper(
            title="Deep Learning for Cybersecurity Threat Detection",
            authors=["Dr. Alice Johnson", "Prof. Bob Smith"],
            abstract="A comprehensive study of deep learning applications in cybersecurity.",
            publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
            doi="10.1000/cyber.2023.001",
            citation_count=42,
            keywords=["cybersecurity", "deep learning", "threat detection"],
        )
        
        fingerprint = PaperFingerprint.from_paper(paper)
        
        assert fingerprint is not None
        assert fingerprint.primary_identifier == "doi:10.1000/cyber.2023.001"
        assert "deep learning cybersecurity" in fingerprint.title_hash.lower()
        assert len(fingerprint.author_hash) > 0
    
    def test_create_fingerprint_from_paper_with_arxiv_id(self):
        """
        Test fingerprint creation for paper with ArXiv ID but no DOI.
        
        Educational Note:
        ArXiv papers often don't have DOIs initially. ArXiv ID becomes
        the primary identifier, but we must handle version numbers properly.
        """
        from src.domain.value_objects.paper_fingerprint import PaperFingerprint
        
        paper = ResearchPaper(
            title="Novel Quantum Algorithms for Machine Learning",
            authors=["Dr. Carol Zhang"],
            abstract="Exploration of quantum computing applications in ML.",
            publication_date=datetime(2023, 8, 22, tzinfo=timezone.utc),
            arxiv_id="2308.12345v1",  # Note version number
            citation_count=15,
            keywords=["quantum computing", "machine learning"],
        )
        
        fingerprint = PaperFingerprint.from_paper(paper)
        
        assert fingerprint.primary_identifier == "arxiv:2308.12345"  # Version stripped
        assert "quantum algorithms machine learning" in fingerprint.title_hash.lower()
        assert "c zhang" in fingerprint.author_hash.lower()  # Initial-based normalization
    
    def test_create_fingerprint_from_paper_without_identifiers(self):
        """
        Test fingerprint creation for paper without standard identifiers.
        
        Educational Note:
        Some sources (like Google Scholar) may not provide DOI or ArXiv ID.
        We need to create fingerprints from title and author information,
        with appropriate normalization for robustness.
        """
        from src.domain.value_objects.paper_fingerprint import PaperFingerprint
        
        paper = ResearchPaper(
            title="Blockchain Applications in Healthcare: A Survey",
            authors=["Dr. David Kim", "Prof. Elena Rodriguez"],
            abstract="Comprehensive survey of blockchain applications in healthcare systems.",
            publication_date=datetime(2023, 4, 10, tzinfo=timezone.utc),
            # No DOI or ArXiv ID
            citation_count=28,
            keywords=["blockchain", "healthcare", "survey"],
        )
        
        fingerprint = PaperFingerprint.from_paper(paper)
        
        # Should create composite identifier from title+authors
        assert fingerprint.primary_identifier.startswith("composite:")
        assert "blockchain" in fingerprint.title_hash.lower()
        assert "healthcare" in fingerprint.title_hash.lower()
        assert "d kim" in fingerprint.author_hash.lower()
        assert "e rodriguez" in fingerprint.author_hash.lower()


class TestPaperFingerprintEquality:
    """
    Test equality detection between paper fingerprints.
    
    Educational Note:
    Fingerprint equality is the core mechanism for duplicate detection.
    We need to handle various scenarios where the same paper might appear
    with slight variations across different sources.
    """
    
    def test_papers_with_same_doi_are_equal(self):
        """
        Test that papers with the same DOI are considered duplicates.
        
        Educational Note:
        DOI uniquely identifies academic papers. Even if other metadata
        differs (title capitalization, author formatting), same DOI
        means same paper.
        """
        from src.domain.value_objects.paper_fingerprint import PaperFingerprint
        
        paper1 = ResearchPaper(
            title="Deep Learning for Cybersecurity Threat Detection",
            authors=["Dr. Alice Johnson", "Prof. Bob Smith"],
            abstract="A comprehensive study...",
            publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
            doi="10.1000/cyber.2023.001",
            citation_count=42,
        )
        
        paper2 = ResearchPaper(
            title="DEEP LEARNING FOR CYBERSECURITY THREAT DETECTION",  # Different case
            authors=["Alice Johnson", "B. Smith"],  # Different formatting
            abstract="A comprehensive study of deep learning...",  # Slightly different
            publication_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
            doi="10.1000/cyber.2023.001",  # Same DOI
            citation_count=45,  # Different citation count
        )
        
        fingerprint1 = PaperFingerprint.from_paper(paper1)
        fingerprint2 = PaperFingerprint.from_paper(paper2)
        
        assert fingerprint1 == fingerprint2
        assert hash(fingerprint1) == hash(fingerprint2)
    
    def test_papers_with_same_arxiv_id_are_equal(self):
        """
        Test that papers with the same ArXiv ID are considered duplicates.
        
        Educational Note:
        ArXiv papers may appear in different versions (v1, v2, etc.) but
        represent the same work. We normalize by stripping version numbers
        for duplicate detection.
        """
        from src.domain.value_objects.paper_fingerprint import PaperFingerprint
        
        paper1 = ResearchPaper(
            title="Novel Quantum Algorithms",
            authors=["Dr. Carol Zhang"],
            abstract="Exploration of quantum computing...",
            publication_date=datetime(2023, 8, 22, tzinfo=timezone.utc),
            arxiv_id="2308.12345v1",
            citation_count=15,
        )
        
        paper2 = ResearchPaper(
            title="Novel Quantum Algorithms for Machine Learning",  # Extended title
            authors=["Carol Zhang"],  # No title
            abstract="Exploration of quantum computing applications in ML.",
            publication_date=datetime(2023, 8, 25, tzinfo=timezone.utc),  # Later date
            arxiv_id="2308.12345v2",  # Different version
            citation_count=18,
        )
        
        fingerprint1 = PaperFingerprint.from_paper(paper1)
        fingerprint2 = PaperFingerprint.from_paper(paper2)
        
        assert fingerprint1 == fingerprint2
    
    def test_papers_with_similar_titles_and_authors_are_equal(self):
        """
        Test fuzzy matching for papers without standard identifiers.
        
        Educational Note:
        When DOI/ArXiv ID are unavailable, we rely on title and author
        similarity. This requires careful normalization and similarity
        thresholds to balance false positives vs false negatives.
        """
        from src.domain.value_objects.paper_fingerprint import PaperFingerprint
        
        paper1 = ResearchPaper(
            title="Blockchain Applications in Healthcare: A Survey",
            authors=["Dr. David Kim", "Prof. Elena Rodriguez"],
            abstract="Survey of blockchain in healthcare...",
            publication_date=datetime(2023, 4, 10, tzinfo=timezone.utc),
            citation_count=28,
        )

        paper2 = ResearchPaper(
            title="Blockchain Applications in Healthcare: A Survey",  # Same title
            authors=["David Kim", "Elena Rodriguez"],  # No titles (should normalize to same)
            abstract="Comprehensive survey of blockchain applications...",
            publication_date=datetime(2023, 4, 12, tzinfo=timezone.utc),
            citation_count=30,
        )
        
        fingerprint1 = PaperFingerprint.from_paper(paper1)
        fingerprint2 = PaperFingerprint.from_paper(paper2)
        
        assert fingerprint1 == fingerprint2


class TestPaperFingerprintSimilarity:
    """
    Test similarity detection for near-duplicates.
    
    Educational Note:
    Beyond exact equality, we need similarity detection for cases where
    papers might be related but not identical (different versions,
    extended abstracts, conference vs journal versions).
    """
    
    def test_calculate_similarity_score(self):
        """
        Test similarity scoring between potentially related papers.
        
        Educational Note:
        Similarity scoring helps identify:
        - Conference vs journal versions of same work
        - Preprint vs published versions
        - Extended versions of workshop papers
        - Papers by same authors on very similar topics
        """
        # This will be implemented after basic equality works
        pass  # Will implement in next iteration
    
    def test_similarity_threshold_handling(self):
        """
        Test configurable similarity thresholds for different use cases.
        
        Educational Note:
        Different research scenarios need different similarity thresholds:
        - High threshold (0.9+): Only near-identical papers
        - Medium threshold (0.7-0.9): Likely same work, different versions
        - Low threshold (0.5-0.7): Related work by same authors
        """
        # This will be implemented after basic similarity works
        pass  # Will implement in next iteration


class TestPaperFingerprintPerformance:
    """
    Test performance characteristics of fingerprinting system.
    
    Educational Note:
    Duplicate detection must be efficient enough to handle thousands
    of papers in reasonable time. We test for performance regressions
    and scalability characteristics.
    """
    
    def test_fingerprint_creation_performance(self):
        """
        Test that fingerprint creation is fast enough for large datasets.
        
        Educational Note:
        We may need to process thousands of papers from multiple sources.
        Fingerprint creation should be O(1) with respect to database size
        and fast enough for real-time duplicate detection.
        """
        # This will be implemented after basic functionality works
        pass  # Will implement in next iteration
    
    def test_hash_collision_resistance(self):
        """
        Test that hash collisions are rare for different papers.
        
        Educational Note:
        Good hash functions minimize collisions while being fast to compute.
        We need to verify that different papers produce different hashes
        with very high probability.
        """
        # This will be implemented after basic functionality works
        pass  # Will implement in next iteration
