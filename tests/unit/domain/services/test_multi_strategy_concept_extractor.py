"""
Tests for Multi-Strategy Concept Extraction Domain Services.

This test module validates the sophisticated concept extraction pipeline
implementing multiple extraction strategies as described in the requirements.

Educational Notes:
- Demonstrates Strategy Pattern testing with multiple implementations
- Shows how to test complex algorithmic components in isolation
- Validates academic-grade concept extraction methodologies
- Tests consolidation and deduplication of multi-source results

Design Patterns Tested:
- Strategy Pattern: Multiple extraction algorithms with common interface
- Template Method: Common extraction workflow with strategy-specific steps
- Factory Pattern: Strategy creation and configuration
- Composite Pattern: Multi-strategy result aggregation
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any, Tuple, Set
import numpy as np

from src.domain.entities.concept import Concept
from src.domain.value_objects.embedding_vector import EmbeddingVector
from src.domain.services.multi_strategy_concept_extractor import (
    ConceptExtractionStrategy,
    RuleBasedExtractionStrategy,
    StatisticalExtractionStrategy,
    EmbeddingBasedExtractionStrategy,
    MultiStrategyConceptExtractor,
    ExtractionResult,
    StrategyConfiguration,
)


class TestConceptExtractionStrategyInterface:
    """
    Test the abstract strategy interface for concept extraction.

    Educational Note:
    Tests abstract base class behavior and contract enforcement,
    demonstrating how interfaces define behavioral contracts.
    """

    def test_strategy_interface_is_abstract(self):
        """Test that ConceptExtractionStrategy cannot be instantiated directly."""
        with pytest.raises(TypeError):
            ConceptExtractionStrategy()

    def test_strategy_requires_extract_concepts_implementation(self):
        """Test that concrete strategies must implement extract_concepts method."""

        # This should fail because extract_concepts is not implemented
        class IncompleteStrategy(ConceptExtractionStrategy):
            pass

        with pytest.raises(TypeError):
            IncompleteStrategy()

    def test_strategy_with_complete_implementation_succeeds(self):
        """Test that strategies with all required methods can be instantiated."""

        class CompleteStrategy(ConceptExtractionStrategy):
            def extract_concepts(
                self, text: str, config: StrategyConfiguration
            ) -> ExtractionResult:
                return ExtractionResult(concepts=[], metadata={})

        strategy = CompleteStrategy()
        assert isinstance(strategy, ConceptExtractionStrategy)


class TestRuleBasedExtractionStrategy:
    """
    Test rule-based concept extraction strategy.

    Educational Note:
    Rule-based methods use linguistic patterns and predefined rules
    for concept identification, following traditional NLP approaches.
    """

    @pytest.fixture
    def rule_strategy(self):
        """Create rule-based extraction strategy for testing."""
        return RuleBasedExtractionStrategy()

    def test_extract_noun_phrases_from_academic_text(self, rule_strategy):
        """Test noun phrase extraction from academic text."""
        text = """
        Heart rate variability (HRV) is a physiological phenomenon. 
        Machine learning algorithms can analyze ECG signals for 
        traumatic brain injury detection in clinical settings.
        """

        result = rule_strategy.extract_noun_phrases(text)

        # Should extract key noun phrases
        expected_phrases = [
            "heart rate variability",
            "physiological phenomenon",
            "machine learning algorithms",
            "ECG signals",
            "traumatic brain injury detection",
            "clinical settings",
        ]

        for phrase in expected_phrases:
            assert any(phrase.lower() in extracted.lower() for extracted in result)

    def test_hearst_pattern_extraction_for_hierarchies(self, rule_strategy):
        """Test Hearst pattern extraction for concept hierarchies."""
        text = """
        Machine learning techniques such as neural networks, support vector machines,
        and decision trees are commonly used. Deep learning methods including 
        convolutional neural networks and recurrent neural networks show promise.
        Biomarkers like heart rate variability, blood pressure, and temperature 
        can indicate health status.
        """

        hierarchies = rule_strategy.extract_hearst_patterns(text)

        # Should find hierarchical relationships
        expected_hierarchies = [
            ("machine learning techniques", "neural networks"),
            ("machine learning techniques", "support vector machines"),
            ("machine learning techniques", "decision trees"),
            ("deep learning methods", "convolutional neural networks"),
            ("deep learning methods", "recurrent neural networks"),
            ("biomarkers", "heart rate variability"),
            ("biomarkers", "blood pressure"),
            ("biomarkers", "temperature"),
        ]

        for parent, child in expected_hierarchies:
            assert any(
                parent.lower() in h[0].lower() and child.lower() in h[1].lower()
                for h in hierarchies
            )

    def test_domain_ontology_matching(self, rule_strategy):
        """Test matching against domain-specific ontologies."""
        text = """
        The study examined heart rate variability, ECG analysis, and 
        machine learning applications in traumatic brain injury research.
        """

        # Mock domain ontology
        hrv_ontology = {
            "cardiovascular": ["heart rate variability", "ECG", "cardiac"],
            "neurology": ["traumatic brain injury", "brain", "neural"],
            "technology": ["machine learning", "artificial intelligence", "algorithms"],
        }

        matches = rule_strategy.match_domain_ontology(text, hrv_ontology)

        # Should match concepts from ontology categories
        assert "cardiovascular" in matches
        assert "neurology" in matches
        assert "technology" in matches
        assert len(matches["cardiovascular"]) >= 2
        assert len(matches["neurology"]) >= 1
        assert len(matches["technology"]) >= 1

    def test_rule_based_extraction_integration(self, rule_strategy):
        """Test complete rule-based extraction workflow."""
        text = """
        This research investigates heart rate variability analysis using 
        machine learning techniques such as neural networks and support vector machines.
        The study focuses on traumatic brain injury detection through ECG signal processing.
        """

        config = StrategyConfiguration(
            domain="medical_ai",
            min_concept_frequency=1,
            extract_hierarchies=True,
            use_domain_ontology=True,
        )

        result = rule_strategy.extract_concepts(text, config)

        # Validate extraction result structure
        assert isinstance(result, ExtractionResult)
        assert len(result.concepts) > 0
        assert "extraction_method" in result.metadata
        assert result.metadata["extraction_method"] == "rule_based"

        # Should contain expected concepts
        concept_texts = [c.text for c in result.concepts]
        assert any("heart rate variability" in text.lower() for text in concept_texts)
        assert any("machine learning" in text.lower() for text in concept_texts)


class TestStatisticalExtractionStrategy:
    """
    Test statistical concept extraction strategy.

    Educational Note:
    Statistical methods use frequency analysis, graph algorithms,
    and probability distributions for concept identification.
    """

    @pytest.fixture
    def stats_strategy(self):
        """Create statistical extraction strategy for testing."""
        return StatisticalExtractionStrategy()

    def test_tfidf_concept_extraction(self, stats_strategy):
        """Test TF-IDF based concept extraction."""
        corpus = [
            "Heart rate variability analysis in cardiovascular research",
            "Machine learning for heart rate variability detection",
            "ECG signal processing and heart rate variability",
            "Traumatic brain injury affects heart rate patterns",
            "Deep learning algorithms for medical signal analysis",
        ]

        concepts = stats_strategy.extract_tfidf_concepts(corpus, max_concepts=25)

        # Should extract high TF-IDF scored terms
        concept_texts = [concept.text for concept in concepts]
        assert any("heart rate variability" in text.lower() for text in concept_texts)
        assert any("machine learning" in text.lower() for text in concept_texts)

        # Concepts should have TF-IDF scores
        for concept in concepts:
            assert concept.relevance_score > 0
            assert concept.extraction_method == "tfidf"

    def test_textrank_keyphrase_extraction(self, stats_strategy):
        """Test TextRank algorithm for keyphrase extraction."""
        text = """
        Heart rate variability represents a crucial biomarker in cardiovascular health assessment.
        Machine learning algorithms enable automated analysis of heart rate variability patterns.
        Deep neural networks can process ECG signals to detect heart rate variability abnormalities.
        Clinical applications of heart rate variability analysis include stress monitoring and 
        disease prediction in healthcare systems.
        """

        keyphrases = stats_strategy.extract_textrank_keyphrases(text, max_phrases=8)

        # Should extract central keyphrases
        assert len(keyphrases) > 0
        keyphrase_texts = [kp.text for kp in keyphrases]
        assert any("heart rate variability" in text.lower() for text in keyphrase_texts)

        # Keyphrases should have centrality scores
        for phrase in keyphrases:
            assert phrase.relevance_score > 0
            assert phrase.extraction_method == "keyword"

    def test_lda_topic_modeling(self, stats_strategy):
        """Test LDA topic modeling for concept discovery."""
        documents = [
            "Heart rate variability analysis cardiovascular health monitoring",
            "Machine learning algorithms neural networks deep learning medical applications",
            "ECG signal processing digital filtering artifact removal techniques",
            "Traumatic brain injury neurological assessment cognitive impairment",
            "Clinical decision support systems electronic health records patient data",
        ]

        topics = stats_strategy.extract_lda_topics(
            documents, num_topics=3, words_per_topic=5
        )

        # Should discover coherent topics
        assert len(topics) == 3
        for topic in topics:
            assert len(topic.concepts) <= 5
            assert topic.coherence_score > 0
            assert "topic_id" in topic.metadata

    def test_statistical_extraction_integration(self, stats_strategy):
        """Test complete statistical extraction workflow."""
        text = """
        Heart rate variability analysis using machine learning approaches represents
        a significant advancement in cardiovascular medicine. Deep learning algorithms
        can process ECG signals to identify patterns associated with various cardiac
        conditions and neurological disorders including traumatic brain injury.
        """

        config = StrategyConfiguration(
            domain="cardiovascular_ai",
            min_concept_frequency=2,
            use_tfidf=True,
            use_textrank=True,
            use_topic_modeling=False,  # Skip for single document
        )

        result = stats_strategy.extract_concepts(text, config)

        # Validate statistical extraction result
        assert isinstance(result, ExtractionResult)
        assert len(result.concepts) > 0
        assert result.metadata["extraction_method"] == "statistical"
        assert "tfidf_concepts" in result.metadata
        assert "textrank_concepts" in result.metadata


class TestEmbeddingBasedExtractionStrategy:
    """
    Test embedding-based concept extraction strategy.

    Educational Note:
    Embedding methods use vector representations to capture
    semantic similarity and enable clustering-based concept discovery.
    """

    @pytest.fixture
    def embedding_strategy(self):
        """Create embedding-based extraction strategy for testing."""
        return EmbeddingBasedExtractionStrategy()

    def test_document_embedding_clustering(self, embedding_strategy):
        """Test document-level embedding and clustering."""
        documents = [
            "Heart rate variability analysis in clinical cardiology",
            "Machine learning for automated ECG interpretation",
            "Deep learning neural networks for medical imaging",
            "Traumatic brain injury assessment using biomarkers",
            "Clinical decision support systems in healthcare",
        ]

        # Mock the internal clustering method
        with patch.object(
            embedding_strategy, "_cluster_document_embeddings"
        ) as mock_cluster:
            mock_concepts = [
                Concept(
                    text="cardiac analysis",
                    frequency=2,
                    relevance_score=0.9,
                    extraction_method="semantic_embedding",
                ),
                Concept(
                    text="machine learning healthcare",
                    frequency=1,
                    relevance_score=0.8,
                    extraction_method="semantic_embedding",
                ),
                Concept(
                    text="medical imaging",
                    frequency=1,
                    relevance_score=0.7,
                    extraction_method="semantic_embedding",
                ),
            ]
            mock_cluster.return_value = mock_concepts

            clusters = embedding_strategy.cluster_documents(documents, num_clusters=3)

        # Should create document clusters
        assert len(clusters) == 3
        for cluster in clusters:
            assert len(cluster.documents) > 0
            assert cluster.centroid_embedding is not None
            assert cluster.coherence_score > 0

    def test_phrase_embedding_similarity(self, embedding_strategy):
        """Test phrase-level embedding similarity calculation."""
        phrases = [
            "heart rate variability",
            "cardiac rhythm analysis",
            "machine learning algorithms",
            "artificial intelligence methods",
            "traumatic brain injury",
        ]

        # Mock embedding service
        with patch.object(embedding_strategy, "_get_phrase_embeddings") as mock_embed:
            mock_embeddings = {
                phrase: EmbeddingVector(vector=tuple(np.random.rand(384).tolist()))
                for phrase in phrases
            }
            mock_embed.return_value = mock_embeddings

            similarity_groups = embedding_strategy.group_similar_phrases(
                phrases, similarity_threshold=0.7
            )

            # Should group semantically similar phrases
            assert len(similarity_groups) > 0
            for group in similarity_groups:
                assert len(group.phrases) > 0
                assert group.average_similarity > 0.7

    def test_semantic_concept_consolidation(self, embedding_strategy):
        """Test consolidation of semantically similar concepts."""
        concepts = [
            Concept(text="heart rate variability", frequency=5, relevance_score=0.9),
            Concept(text="HRV analysis", frequency=3, relevance_score=0.8),
            Concept(text="cardiac rhythm analysis", frequency=2, relevance_score=0.7),
            Concept(text="machine learning", frequency=4, relevance_score=0.85),
            Concept(text="artificial intelligence", frequency=2, relevance_score=0.75),
            Concept(text="traumatic brain injury", frequency=6, relevance_score=0.95),
        ]

        # Mock similarity calculations
        with patch.object(
            embedding_strategy, "_calculate_concept_similarity"
        ) as mock_sim:
            # Simulate high similarity between HRV-related concepts
            def similarity_side_effect(c1, c2):
                hrv_terms = [
                    "heart rate variability",
                    "HRV analysis",
                    "cardiac rhythm analysis",
                ]
                ai_terms = ["machine learning", "artificial intelligence"]

                if c1.text in hrv_terms and c2.text in hrv_terms:
                    return 0.85
                elif c1.text in ai_terms and c2.text in ai_terms:
                    return 0.80
                else:
                    return 0.3

            mock_sim.side_effect = similarity_side_effect

            consolidated = embedding_strategy.consolidate_similar_concepts(
                concepts, similarity_threshold=0.75
            )

            # Should consolidate similar concepts
            assert len(consolidated) < len(concepts)

            # Primary concepts should be preserved with enhanced metadata
            consolidated_texts = [c.text for c in consolidated]
            assert "heart rate variability" in consolidated_texts
            assert "machine learning" in consolidated_texts
            assert "traumatic brain injury" in consolidated_texts


class TestMultiStrategyConceptExtractor:
    """
    Test the multi-strategy orchestrator for concept extraction.

    Educational Note:
    The orchestrator combines results from multiple strategies,
    demonstrating the Composite pattern and result consolidation.
    """

    @pytest.fixture
    def multi_extractor(self):
        """Create multi-strategy extractor with mocked strategies."""
        rule_strategy = Mock(spec=RuleBasedExtractionStrategy)
        stats_strategy = Mock(spec=StatisticalExtractionStrategy)
        embedding_strategy = Mock(spec=EmbeddingBasedExtractionStrategy)

        return MultiStrategyConceptExtractor(
            strategies=[rule_strategy, stats_strategy, embedding_strategy]
        )

    def test_multi_strategy_extraction_orchestration(self, multi_extractor):
        """Test orchestration of multiple extraction strategies."""
        text = "Heart rate variability analysis using machine learning for medical applications"

        # Mock strategy results
        rule_concepts = [
            Concept(
                text="heart rate variability",
                frequency=1,
                relevance_score=0.9,
                extraction_method="keyword",
            ),
            Concept(
                text="machine learning",
                frequency=1,
                relevance_score=0.8,
                extraction_method="keyword",
            ),
        ]

        stats_concepts = [
            Concept(
                text="heart rate variability",
                frequency=2,
                relevance_score=0.95,
                extraction_method="tfidf",
            ),
            Concept(
                text="medical applications",
                frequency=1,
                relevance_score=0.7,
                extraction_method="tfidf",
            ),
        ]

        embedding_concepts = [
            Concept(
                text="HRV analysis",
                frequency=1,
                relevance_score=0.85,
                extraction_method="semantic_embedding",
            ),
            Concept(
                text="machine learning",
                frequency=1,
                relevance_score=0.9,
                extraction_method="semantic_embedding",
            ),
        ]

        # Configure strategy mocks
        multi_extractor.strategies[0].extract_concepts.return_value = ExtractionResult(
            concepts=rule_concepts, metadata={"method": "rule_based"}
        )
        multi_extractor.strategies[1].extract_concepts.return_value = ExtractionResult(
            concepts=stats_concepts, metadata={"method": "statistical"}
        )
        multi_extractor.strategies[2].extract_concepts.return_value = ExtractionResult(
            concepts=embedding_concepts, metadata={"method": "embedding_based"}
        )

        config = StrategyConfiguration(
            domain="medical_ai", enable_all_strategies=True, consolidate_results=True
        )

        result = multi_extractor.extract_concepts_comprehensive(text, config)

        # Should consolidate results from all strategies
        assert isinstance(result, ExtractionResult)
        assert len(result.concepts) > 0
        assert "strategies_used" in result.metadata
        assert len(result.metadata["strategies_used"]) == 3

        # Should contain concepts from multiple strategies
        concept_texts = [c.text for c in result.concepts]
        assert any("heart rate variability" in text.lower() for text in concept_texts)
        assert any("machine learning" in text.lower() for text in concept_texts)

    def test_strategy_weight_configuration(self, multi_extractor):
        """Test weighted combination of strategy results."""
        text = "Sample text for extraction"

        # Mock weighted results
        multi_extractor.strategies[0].extract_concepts.return_value = ExtractionResult(
            concepts=[Concept(text="concept1", frequency=1, relevance_score=0.8)],
            metadata={},
        )
        multi_extractor.strategies[1].extract_concepts.return_value = ExtractionResult(
            concepts=[Concept(text="concept2", frequency=1, relevance_score=0.7)],
            metadata={},
        )
        multi_extractor.strategies[2].extract_concepts.return_value = ExtractionResult(
            concepts=[Concept(text="concept3", frequency=1, relevance_score=0.9)],
            metadata={},
        )

        config = StrategyConfiguration(
            domain="test",
            strategy_weights={
                "rule_based": 0.5,
                "statistical": 0.3,
                "embedding_based": 0.2,
            },
        )

        result = multi_extractor.extract_concepts_comprehensive(text, config)

        # Should apply strategy weights to final scores
        assert len(result.concepts) == 3
        assert "weighted_combination" in result.metadata

    def test_concept_deduplication_and_merging(self, multi_extractor):
        """Test deduplication and merging of concepts from multiple strategies."""
        text = "Test text"

        # Create overlapping concepts from different strategies
        overlapping_concepts = [
            Concept(
                text="heart rate variability",
                frequency=2,
                relevance_score=0.9,
                extraction_method="keyword",
            ),
            Concept(
                text="heart rate variability",
                frequency=3,
                relevance_score=0.8,
                extraction_method="tfidf",
            ),
            Concept(
                text="HRV",
                frequency=1,
                relevance_score=0.7,
                extraction_method="semantic_embedding",
            ),  # Abbreviation
        ]

        # Mock all strategies returning similar concepts
        for strategy in multi_extractor.strategies:
            strategy.extract_concepts.return_value = ExtractionResult(
                concepts=overlapping_concepts, metadata={}
            )

        config = StrategyConfiguration(
            domain="medical",
            consolidate_results=True,
            merge_similar_concepts=True,
            similarity_threshold=0.8,
        )

        result = multi_extractor.extract_concepts_comprehensive(text, config)

        # Should deduplicate and merge similar concepts
        concept_texts = [c.text for c in result.concepts]
        hrv_concepts = [c for c in result.concepts if "heart rate" in c.text.lower()]

        # Should merge evidence from multiple strategies
        if hrv_concepts:
            merged_concept = hrv_concepts[0]
            assert merged_concept.frequency >= 2  # Combined frequencies
            # Verify extraction method indicates consolidation
            assert merged_concept.extraction_method in [
                "keyword",
                "tfidf",
                "semantic_embedding",
            ]


class TestExtractionResultDataStructures:
    """
    Test data structures for extraction results.

    Educational Note:
    Tests value objects and entities that encapsulate
    extraction results with proper validation and metadata.
    """

    def test_extraction_result_creation(self):
        """Test creation of ExtractionResult with validation."""
        concepts = [Concept(text="test concept", frequency=1, relevance_score=0.8)]
        metadata = {"extraction_method": "test", "timestamp": "2024-01-01"}

        result = ExtractionResult(concepts=concepts, metadata=metadata)

        assert result.concepts == concepts
        assert result.metadata == metadata
        assert result.total_concepts == 1

    def test_strategy_configuration_validation(self):
        """Test StrategyConfiguration validation and defaults."""
        # Test with minimal configuration
        config = StrategyConfiguration(domain="test")

        assert config.domain == "test"
        assert config.min_concept_frequency >= 1
        assert isinstance(config.enable_all_strategies, bool)

        # Test with full configuration
        full_config = StrategyConfiguration(
            domain="medical_ai",
            min_concept_frequency=2,
            enable_all_strategies=True,
            strategy_weights={"rule_based": 0.4, "statistical": 0.6},
            consolidate_results=True,
        )

        assert full_config.domain == "medical_ai"
        assert full_config.min_concept_frequency == 2
        assert full_config.strategy_weights["rule_based"] == 0.4

    def test_extraction_result_aggregation_methods(self):
        """Test aggregation methods on ExtractionResult."""
        concepts = [
            Concept(text="concept1", frequency=3, relevance_score=0.9),
            Concept(text="concept2", frequency=1, relevance_score=0.7),
            Concept(text="concept3", frequency=2, relevance_score=0.8),
        ]

        result = ExtractionResult(concepts=concepts, metadata={})

        # Test aggregation methods
        assert result.total_concepts == 3
        assert result.average_relevance_score == pytest.approx(0.8, rel=1e-2)
        assert result.total_frequency == 6

        # Test filtering methods
        high_relevance = result.filter_by_relevance(min_score=0.8)
        assert len(high_relevance) == 2

        frequent_concepts = result.filter_by_frequency(min_frequency=2)
        assert len(frequent_concepts) == 2
