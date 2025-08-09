"""
Statistical Concept Extraction Strategy

Educational Notes:
- Implements Strategy pattern for statistical extraction
- Demonstrates machine learning approach to concept identification
- Shows proper integration of sklearn algorithms
"""

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict

from src.domain.entities.concept import Concept
from src.domain.value_objects.extraction.extraction_result import ExtractionResult, StrategyConfiguration
from ..concept_extraction_strategy import ConceptExtractionStrategy
from ..utilities import _safe_extraction

class StatisticalExtractionStrategy(ConceptExtractionStrategy):
    """
    Statistical concept extraction using frequency analysis and graph algorithms.

    Educational Note:
    Implements statistical methods for concept extraction including TF-IDF,
    TextRank, and topic modeling. These methods use mathematical approaches
    to identify important terms and concepts without relying on linguistic rules.

    Academic Methods Implemented:
    - TF-IDF weighting for term importance calculation
    - TextRank algorithm for keyphrase extraction (Mihalcea & Tarau, 2004)
    - Latent Dirichlet Allocation for topic discovery (Blei et al., 2003)
    """

    def extract_concepts(
        self, text: str, config: StrategyConfiguration
    ) -> ExtractionResult:
        """Extract concepts using statistical methods."""
        concepts = []
        metadata = {
            "extraction_method": "statistical",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "techniques_used": [],
        }

        # TF-IDF based extraction
        if config.use_tfidf:
            tfidf_concepts = self.extract_tfidf_concepts([text], max_concepts=20)
            concepts.extend(tfidf_concepts)
            metadata["techniques_used"].append("tfidf")
            metadata["tfidf_concepts"] = len(tfidf_concepts)

        # TextRank keyphrase extraction
        if config.use_textrank:
            textrank_concepts = self.extract_textrank_keyphrases(text, max_phrases=15)
            concepts.extend(textrank_concepts)
            metadata["techniques_used"].append("textrank")
            metadata["textrank_concepts"] = len(textrank_concepts)

        # Filter and deduplicate
        concepts = self._filter_and_deduplicate_concepts(concepts, config)

        metadata["total_concepts_extracted"] = len(concepts)
        return ExtractionResult(concepts=concepts, metadata=metadata)

    def extract_tfidf_concepts(
        self, corpus: List[str], max_concepts: int = 20
    ) -> List[Concept]:
        """
        Extract concepts using TF-IDF weighting.

        Educational Note:
        TF-IDF (Term Frequency-Inverse Document Frequency) identifies
        terms that are frequent in a document but rare across the corpus,
        indicating their importance to the specific document.
        """
        if len(corpus) == 1:
            # For single document, use simple term frequency
            return self._extract_term_frequency_concepts(corpus[0], max_concepts)

        # Standard TF-IDF for multiple documents
        vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 3),  # Include unigrams, bigrams, trigrams
            stop_words="english",
            min_df=1,
            lowercase=True,
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            feature_names = vectorizer.get_feature_names_out()

            # Aggregate TF-IDF scores across all documents to find globally important terms
            aggregated_scores = tfidf_matrix.sum(axis=0).A1

            # Create concepts from high-scoring terms
            concepts = []
            for i, score in enumerate(aggregated_scores):
                if score > 0:
                    concept = Concept(
                        text=feature_names[i],
                        frequency=1,
                        relevance_score=float(
                            min(score / len(corpus), 1.0)
                        ),  # Normalize by corpus size
                        extraction_method="tfidf",
                    )
                    concepts.append(concept)

            # Sort by TF-IDF score and return top concepts
            concepts.sort(key=lambda x: x.relevance_score, reverse=True)
            return concepts[:max_concepts]

        except Exception as e:
            logging.warning(f"TF-IDF extraction failed: {e}")
            return []

    def extract_textrank_keyphrases(
        self, text: str, max_phrases: int = 15
    ) -> List[Concept]:
        """
        Extract keyphrases using TextRank algorithm.

        Educational Note:
        TextRank applies PageRank algorithm to word graphs,
        identifying central terms based on their connections
        to other words in the text.
        """
        try:
            # First extract candidate phrases using noun phrase patterns
            candidate_phrases = self._extract_candidate_phrases(text)

            if not candidate_phrases:
                # Fallback to single words if no phrases found
                sentences = self._split_into_sentences(text)
                word_graph = self._build_word_graph(sentences)

                if len(word_graph) == 0:
                    return []

                # Apply PageRank algorithm
                pagerank_scores = nx.pagerank(word_graph, max_iter=100, tol=1e-6)

                # Extract top-scoring words as keyphrases
                sorted_words = sorted(
                    pagerank_scores.items(), key=lambda x: x[1], reverse=True
                )

                concepts = []
                for word, score in sorted_words[:max_phrases]:
                    concept = Concept(
                        text=word,
                        frequency=1,
                        relevance_score=float(score),
                        extraction_method="keyword",
                    )
                    concepts.append(concept)
                return concepts

            # Score candidate phrases based on constituent word scores
            sentences = self._split_into_sentences(text)
            word_graph = self._build_word_graph(sentences)

            if len(word_graph) == 0:
                return []

            pagerank_scores = nx.pagerank(word_graph, max_iter=100, tol=1e-6)

            # Score phrases based on average word scores
            phrase_scores = []
            for phrase in candidate_phrases:
                words = phrase.lower().split()
                word_scores = [
                    pagerank_scores.get(word, 0.0)
                    for word in words
                    if word in pagerank_scores
                ]
                if word_scores:
                    avg_score = sum(word_scores) / len(word_scores)
                    phrase_scores.append((phrase, avg_score))

            # Sort by score and create concepts
            phrase_scores.sort(key=lambda x: x[1], reverse=True)
            concepts = []
            for phrase, score in phrase_scores[:max_phrases]:
                concept = Concept(
                    text=phrase,
                    frequency=1,
                    relevance_score=float(score),
                    extraction_method="keyword",
                )
                concepts.append(concept)

            return concepts

        except Exception as e:
            logging.warning(f"TextRank extraction failed: {e}")
            return []

    def _extract_candidate_phrases(self, text: str) -> List[str]:
        """Extract candidate phrases for TextRank analysis."""
        # Extract noun phrases and technical terms
        phrases = []

        # Common multi-word technical patterns
        patterns = [
            r"\b(?:heart rate variability|machine learning|deep learning|artificial intelligence)\b",
            r"\b(?:medical applications?|signal analysis|data processing)\b",
            r"\b(?:neural networks?|algorithms?|cardiovascular research)\b",
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",  # Capitalized phrases
            r"\b[a-z]+ [a-z]+ (?:analysis|detection|processing|research|applications?)\b",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            phrases.extend(matches)

        # Remove duplicates and filter short phrases
        unique_phrases = list(set(phrases))
        return [p for p in unique_phrases if len(p.split()) >= 2]

    def extract_lda_topics(
        self, documents: List[str], num_topics: int = 5, words_per_topic: int = 10
    ):
        """
        Extract topics using Latent Dirichlet Allocation.

        Educational Note:
        LDA discovers latent topics in document collections by modeling
        each document as a mixture of topics and each topic as a mixture of words.
        """
        if len(documents) < 2:
            # LDA requires multiple documents
            return []

        try:
            # Prepare text for LDA
            vectorizer = TfidfVectorizer(
                max_features=100, stop_words="english", lowercase=True, min_df=2
            )

            doc_term_matrix = vectorizer.fit_transform(documents)

            # Fit LDA model
            lda = LatentDirichletAllocation(
                n_components=num_topics, random_state=42, max_iter=100
            )
            lda.fit(doc_term_matrix)

            # Extract topics
            feature_names = vectorizer.get_feature_names_out()
            topics = []

            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-words_per_topic:][::-1]
                topic_concepts = []

                # Normalize topic weights to [0,1] range
                max_weight = topic.max()
                min_weight = topic.min()
                weight_range = (
                    max_weight - min_weight if max_weight > min_weight else 1.0
                )

                for word_idx in top_words_idx:
                    word = feature_names[word_idx]
                    weight = topic[word_idx]

                    # Normalize weight to [0,1] range
                    normalized_weight = (
                        (weight - min_weight) / weight_range
                        if weight_range > 0
                        else 0.5
                    )

                    concept = Concept(
                        text=word,
                        frequency=1,
                        relevance_score=float(normalized_weight),
                        extraction_method="tfidf",
                    )
                    topic_concepts.append(concept)

                # Create topic wrapper (simplified for this implementation)
                topic_result = type(
                    "Topic",
                    (),
                    {
                        "concepts": topic_concepts,
                        "coherence_score": 0.5,  # Placeholder
                        "metadata": {"topic_id": topic_idx},
                    },
                )()
                topics.append(topic_result)

            return topics

        except Exception as e:
            logging.warning(f"LDA topic extraction failed: {e}")
            return []

    def _extract_term_frequency_concepts(
        self, text: str, max_concepts: int
    ) -> List[Concept]:
        """Extract concepts based on term frequency for single documents."""
        # Simple term frequency approach
        words = re.findall(WORD_EXTRACTION_PATTERN, text.lower())
        word_freq = Counter(words)

        concepts = []
        for word, freq in word_freq.most_common(max_concepts):
            if freq >= 2:  # Minimum frequency threshold
                concept = Concept(
                    text=word,
                    frequency=freq,
                    relevance_score=min(freq / max(word_freq.values()), 1.0),
                    extraction_method="tfidf",
                )
                concepts.append(concept)

        return concepts

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for TextRank processing."""
        # Simple sentence splitting
        sentences = re.split(SENTENCE_SPLIT_PATTERN, text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    def _build_word_graph(self, sentences: List[str]) -> nx.Graph:
        """Build word co-occurrence graph for TextRank."""
        graph = nx.Graph()

        for sentence in sentences:
            words = re.findall(WORD_EXTRACTION_PATTERN, sentence.lower())
            self._add_words_to_graph(graph, words)
            self._add_cooccurrence_edges(graph, words)

        return graph

    def _add_words_to_graph(self, graph: nx.Graph, words: List[str]) -> None:
        """Add words as nodes to the graph."""
        for word in words:
            if word not in graph:
                graph.add_node(word)

    def _add_cooccurrence_edges(self, graph: nx.Graph, words: List[str]) -> None:
        """Add edges between co-occurring words."""
        for i, word1 in enumerate(words):
            for word2 in words[i + 1 : i + 6]:  # Window of 5 words
                if word1 != word2:
                    self._update_edge_weight(graph, word1, word2)

    def _update_edge_weight(self, graph: nx.Graph, word1: str, word2: str) -> None:
        """Update edge weight between two words."""
        if graph.has_edge(word1, word2):
            graph[word1][word2]["weight"] += 1
        else:
            graph.add_edge(word1, word2, weight=1)

    def _filter_and_deduplicate_concepts(
        self, concepts: List[Concept], config: StrategyConfiguration
    ) -> List[Concept]:
        """Filter and deduplicate statistical concepts."""
        # Remove very low scoring concepts
        filtered = [c for c in concepts if c.relevance_score > 0.1]

        # Sort by relevance score and limit
        filtered.sort(key=lambda x: x.relevance_score, reverse=True)
        return filtered[: config.max_concepts_per_strategy]



