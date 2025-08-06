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


class TestPaperCreationAndIdentity:
    """
    Test paper creation and identity management.
    
    Educational Note:
    Entity identity is crucial in domain modeling. Papers have natural
    identities (DOI, ArXiv ID) that persist even when metadata changes.
    This reflects how researchers think about papers - same paper,
    updated information.
    """
    
    def test_create_paper_with_doi_identity(self):
        """
        Test creating a paper with DOI as primary identity.
        
        Educational Note:
        DOI (Digital Object Identifier) is the gold standard for academic
        paper identification. It's immutable and globally unique.
        """
        # Arrange
        doi = "10.1000/xyz123"
        title = "Machine Learning in Academic Research"
        authors = ["Smith, J.", "Johnson, A."]
        abstract = "This paper explores ML applications in research."
        
        # Act
        paper = Paper.create_with_doi(
            doi=doi,
            title=title,
            authors=authors,
            abstract=abstract
        )
        
        # Assert
        assert paper.doi == doi
        assert paper.title == title
        assert paper.authors == authors
        assert paper.abstract == abstract
        assert paper.identity == doi  # DOI serves as identity
        
    def test_create_paper_with_arxiv_identity(self):
        """
        Test creating a paper with ArXiv ID as primary identity.
        
        Educational Note:
        ArXiv papers often don't have DOIs initially. The ArXiv ID
        serves as the persistent identifier for preprints.
        """
        # Arrange
        arxiv_id = "2301.12345"
        title = "Novel Approaches to Paper Discovery"
        authors = ["Davis, C."]
        
        # Act
        paper = Paper.create_with_arxiv_id(
            arxiv_id=arxiv_id,
            title=title,
            authors=authors
        )
        
        # Assert
        assert paper.arxiv_id == arxiv_id
        assert paper.identity == arxiv_id
        assert paper.doi is None  # No DOI for preprints
        
    def test_paper_equality_based_on_identity(self):
        """
        Test that paper equality is based on identity, not attributes.
        
        Educational Note:
        Entity equality is about identity, not current state. Two papers
        with the same DOI are the same paper, even if other attributes differ.
        This reflects real-world scenarios where metadata gets updated.
        """
        # Arrange
        doi = "10.1000/same-paper"
        
        paper1 = Paper.create_with_doi(
            doi=doi,
            title="Original Title",
            authors=["Smith, J."]
        )
        
        paper2 = Paper.create_with_doi(
            doi=doi,
            title="Updated Title",  # Different title
            authors=["Smith, J.", "Johnson, A."]  # Different authors
        )
        
        # Act & Assert
        assert paper1 == paper2  # Same identity = same paper
        assert hash(paper1) == hash(paper2)  # Consistent hashing
        
    def test_paper_identity_required_for_creation(self):
        """
        Test that papers require some form of identity.
        
        Educational Note:
        Entities must have identity. Papers without DOI or ArXiv ID
        need content-based identity generation to maintain entity semantics.
        """
        # Arrange
        title = "Paper Without External ID"
        authors = ["Anonymous"]
        
        # Act & Assert
        with pytest.raises(ValueError, match="identity required"):
            Paper.create_without_external_id(
                title="",  # Empty title can't generate identity
                authors=[]  # Empty authors can't generate identity
            )


class TestPaperBusinessBehavior:
    """
    Test paper business behavior and domain operations.
    
    Educational Note:
    Rich domain models include behavior relevant to the business domain.
    Papers aren't just data containers - they can validate themselves,
    provide derived information, and enforce business rules.
    """
    
    def test_paper_can_determine_research_readiness(self):
        """
        Test that papers can determine if they're ready for concept extraction.
        
        Educational Note:
        Business logic belongs in domain entities. Papers know what
        constitutes sufficient content for meaningful analysis.
        """
        # Arrange - Paper with sufficient content
        complete_paper = Paper.create_with_doi(
            doi="10.1000/complete",
            title="Complete Research Paper",
            authors=["Smith, J."],
            abstract="Detailed abstract with sufficient content for analysis.",
            full_text="Full paper content with multiple paragraphs and sections..."
        )
        
        # Arrange - Paper with insufficient content
        incomplete_paper = Paper.create_with_doi(
            doi="10.1000/incomplete", 
            title="Title Only",
            authors=["Smith, J."]
            # No abstract or full text
        )
        
        # Act & Assert
        assert complete_paper.is_ready_for_concept_extraction() is True
        assert incomplete_paper.is_ready_for_concept_extraction() is False
        
    def test_paper_can_add_processing_metadata(self):
        """
        Test that papers can track their processing status and metadata.
        
        Educational Note:
        Papers need to track processing state for efficient pipeline operations.
        This prevents reprocessing and provides audit trails.
        """
        # Arrange
        paper = Paper.create_with_doi(
            doi="10.1000/test",
            title="Test Paper",
            authors=["Test Author"]
        )
        
        processing_metadata = {
            "processed_at": "2025-08-05T10:30:00Z",
            "extraction_model": "all-MiniLM-L6-v2", 
            "concept_count": 15,
            "confidence_score": 0.89
        }
        
        # Act
        paper.add_processing_metadata(processing_metadata)
        
        # Assert
        assert paper.is_processed() is True
        assert paper.processing_metadata["concept_count"] == 15
        assert paper.processing_metadata["confidence_score"] == 0.89
        
    def test_paper_validates_author_format(self):
        """
        Test that papers validate author name formats.
        
        Educational Note:
        Domain entities should validate their own data consistency.
        Author names have academic conventions that should be enforced.
        """
        # Arrange & Act & Assert - Valid author formats
        valid_authors = ["Smith, J.", "Johnson, A.B.", "van der Berg, C."]
        paper = Paper.create_with_doi(
            doi="10.1000/valid-authors",
            title="Test Paper", 
            authors=valid_authors
        )
        assert paper.authors == valid_authors
        
        # Arrange & Act & Assert - Invalid author formats
        with pytest.raises(ValueError, match="Invalid author format"):
            Paper.create_with_doi(
                doi="10.1000/invalid",
                title="Test Paper",
                authors=[""]  # Empty author name
            )
            
    def test_paper_can_generate_content_summary(self):
        """
        Test that papers can generate content summaries for display.
        
        Educational Note:
        Domain objects should provide derived information useful for
        the business domain. Summaries help researchers quickly assess relevance.
        """
        # Arrange
        paper = Paper.create_with_doi(
            doi="10.1000/summary-test",
            title="Advanced Machine Learning Techniques for Natural Language Processing",
            authors=["Smith, J.", "Johnson, A.", "Brown, C."],
            abstract="This paper presents novel approaches to NLP using deep learning. " +
                    "We demonstrate significant improvements in text classification and " +
                    "sentiment analysis tasks through innovative neural architectures.",
            full_text="Extended content about neural networks and language models..."
        )
        
        # Act
        summary = paper.generate_content_summary(max_length=100)
        
        # Assert
        assert len(summary) <= 100
        assert "machine learning" in summary.lower()
        assert "nlp" in summary.lower() or "natural language" in summary.lower()
        assert summary.endswith("...")  # Truncation indicator
