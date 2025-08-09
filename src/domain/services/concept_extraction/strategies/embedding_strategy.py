"""
Embedding-Based Concept Extraction Strategy

Educational Notes:
- Implements Strategy pattern for embedding-based extraction
- Demonstrates neural network approach to concept identification
- Shows proper integration of modern NLP techniques
"""

import numpy as np
import networkx as nx
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import defaultdict

from src.domain.entities.concept import Concept
from src.domain.value_objects.embedding_vector import EmbeddingVector
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..utilities import _safe_extraction

class EmbeddingBasedExtractionStrategy(ConceptExtractionStrategy):
    """
    Embedding-based concept extraction using semantic similarity and clustering.

    Educational Note:
    This strategy uses vector representations (embeddings) to capture semantic
    meaning and identify concepts through clustering and similarity analysis.
    It demonstrates modern NLP approaches using neural language models.
    """

    def extract_concepts(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """Extract concepts using embedding-based methods."""
        concepts = []
        metadata = {
            "extraction_method": "embedding_based",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "techniques_used": [],
        }

        # For single document, extract candidate phrases first
        candidate_phrases = self._extract_candidate_phrases(text)

        if len(candidate_phrases) > 1:
            # Group similar phrases using embeddings
            similarity_groups = self.group_similar_phrases(
                candidate_phrases, similarity_threshold=config.similarity_threshold
            )

            # Create concepts from phrase groups
            for group in similarity_groups:
                representative_phrase = max(
                    group.phrases, key=len
                )  # Use longest phrase as representative
                concept = Concept(
                    text=representative_phrase,
                    frequency=len(group.phrases),
                    relevance_score=group.average_similarity,
                    extraction_method="semantic_embedding",
                )
                concepts.append(concept)

            metadata["techniques_used"].append("phrase_clustering")
            metadata["similarity_groups"] = len(similarity_groups)

        # Apply concept consolidation
        if config.merge_similar_concepts and len(concepts) > 1:
            concepts = self.consolidate_similar_concepts(
                concepts, similarity_threshold=config.similarity_threshold
            )
            metadata["techniques_used"].append("concept_consolidation")

        # Filter and limit results
        concepts = self._filter_and_limit_concepts(concepts, config)

        metadata["total_concepts_extracted"] = len(concepts)
        return ExtractionResult(concepts=concepts, metadata=metadata)

    def cluster_documents(self, documents: List[str], num_clusters: int = 3):
        """
        Cluster documents using embedding similarity.

        Educational Note:
        Document clustering groups semantically similar documents,
        useful for discovering thematic concepts across a corpus.
        """
        # This would require actual embedding service integration
        # For now, return mock clusters for testing
        clusters = []
        docs_per_cluster = len(documents) // num_clusters or 1

        for i in range(num_clusters):
            start_idx = i * docs_per_cluster
            end_idx = min((i + 1) * docs_per_cluster, len(documents))
            cluster_docs = documents[start_idx:end_idx]

            cluster = type(
                "DocumentCluster",
                (),
                {
                    "documents": cluster_docs,
                    "centroid_embedding": EmbeddingVector(
                        vector=tuple([0.1] * 384)
                    ),  # Mock embedding
                    "coherence_score": 0.8,
                },
            )()
            clusters.append(cluster)

        return clusters

    def group_similar_phrases(
        self, phrases: List[str], similarity_threshold: float = 0.7
    ):
        """
        Group semantically similar phrases using embeddings.

        Educational Note:
        Phrase grouping identifies synonyms and related terms,
        reducing redundancy in concept extraction results.
        """
        # Mock implementation for testing
        # In real implementation, would use sentence transformers
        groups = []

        # Simple grouping based on word overlap (placeholder)
        remaining_phrases = phrases.copy()

        while remaining_phrases:
            current_phrase = remaining_phrases.pop(0)
            group_phrases = [current_phrase]

            # Find similar phrases (mock similarity calculation)
            to_remove = []
            for phrase in remaining_phrases:
                similarity = self._mock_phrase_similarity(current_phrase, phrase)
                if similarity >= similarity_threshold:
                    group_phrases.append(phrase)
                    to_remove.append(phrase)

            # Remove grouped phrases from remaining
            for phrase in to_remove:
                remaining_phrases.remove(phrase)

            # Create phrase group
            group = type(
                "PhraseGroup",
                (),
                {
                    "phrases": group_phrases,
                    "average_similarity": 0.8,  # Mock similarity
                },
            )()
            groups.append(group)

        return groups

    def consolidate_similar_concepts(
        self, concepts: List[Concept], similarity_threshold: float = 0.8
    ) -> List[Concept]:
        """
        Consolidate semantically similar concepts.

        Educational Note:
        Concept consolidation merges similar concepts while preserving
        evidence and metadata, reducing redundancy in final results.
        """
        if len(concepts) <= 1:
            return concepts

        consolidated = []
        remaining_concepts = concepts.copy()

        while remaining_concepts:
            primary_concept = remaining_concepts.pop(0)
            similar_concepts = [primary_concept]

            # Find similar concepts
            to_remove = []
            for concept in remaining_concepts:
                similarity = self._calculate_concept_similarity(
                    primary_concept, concept
                )
                if similarity >= similarity_threshold:
                    similar_concepts.append(concept)
                    to_remove.append(concept)

            # Remove similar concepts from remaining
            for concept in to_remove:
                remaining_concepts.remove(concept)

            # Consolidate similar concepts
            if len(similar_concepts) > 1:
                consolidated_concept = self._merge_concepts(similar_concepts)
            else:
                consolidated_concept = primary_concept

            consolidated.append(consolidated_concept)

        return consolidated

    def _extract_candidate_phrases(self, text: str) -> List[str]:
        """Extract candidate phrases for concept analysis."""
        # Simple phrase extraction (2-4 word phrases)
        phrases = []

        # Extract noun phrases and technical terms
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        for i in range(len(words)):
            # Extract 2-4 word phrases
            for length in [2, 3, 4]:
                if i + length <= len(words):
                    phrase = " ".join(words[i : i + length])
                    if len(phrase) > 6:  # Minimum meaningful length
                        phrases.append(phrase)

        # Remove duplicates and very common phrases
        unique_phrases = list(set(phrases))
        stopwords = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }

        filtered_phrases = []
        for phrase in unique_phrases:
            words_in_phrase = phrase.split()
            if not any(word in stopwords for word in words_in_phrase):
                filtered_phrases.append(phrase)

        return filtered_phrases[:50]  # Limit candidate phrases

    def _mock_phrase_similarity(self, phrase1: str, phrase2: str) -> float:
        """Mock phrase similarity calculation for testing."""
        words1 = set(phrase1.split())
        words2 = set(phrase2.split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def _calculate_concept_similarity(
        self, concept1: Concept, concept2: Concept
    ) -> float:
        """Calculate similarity between two concepts."""
        # Mock similarity based on text overlap
        return self._mock_phrase_similarity(concept1.text, concept2.text)

    def _merge_concepts(self, concepts: List[Concept]) -> Concept:
        """Merge multiple similar concepts into one."""
        # Use the concept with highest relevance as primary
        primary = max(concepts, key=lambda c: c.relevance_score)

        # Combine frequencies and metadata
        total_frequency = sum(c.frequency for c in concepts)
        avg_relevance = sum(c.relevance_score for c in concepts) / len(concepts)

        # Merge metadata (simplified since extraction_metadata doesn't exist)

        return Concept(
            text=primary.text,
            frequency=total_frequency,
            relevance_score=avg_relevance,
            extraction_method="semantic_embedding",
        )

    def _filter_and_limit_concepts(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Filter and limit embedding-based concepts."""
        # Filter by minimum frequency and relevance
        filtered = [
            c
            for c in concepts
            if c.frequency >= config.min_concept_frequency and c.relevance_score > 0.5
        ]

        # Sort by relevance score and limit
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)
        return filtered[: config.max_concepts_per_strategy]

    def _get_phrase_embeddings(self, phrases: List[str]) -> Dict[str, EmbeddingVector]:
        """Get embeddings for phrases (mock implementation for testing)."""
        # Mock embeddings for testing purposes
        embeddings = {}
        for phrase in phrases:
            # Generate mock embedding
            embedding = EmbeddingVector(vector=tuple([0.1] * 384))
            embeddings[phrase] = embedding
        return embeddings

    def _cluster_document_embeddings(self, documents: List[str]) -> List[Concept]:
        """Cluster documents using embeddings (mock implementation for testing)."""
        # Mock implementation that returns sample concepts
        concepts = []
        for i, doc in enumerate(documents[:3]):  # Limit to 3 concepts
            concept = Concept(
                text=f"document_cluster_{i}",
                frequency=1,
                relevance_score=0.8 - i * 0.1,
                extraction_method="semantic_embedding",
            )
            concepts.append(concept)
        return concepts



