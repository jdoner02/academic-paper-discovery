"""
PaperFingerprint - Duplicate detection across academic paper sources.

This value object provides robust duplicate detection for academic papers that may
appear across multiple sources (ArXiv, PubMed, Google Scholar, etc.) with slight
variations in metadata formatting.

Educational Notes:
The PaperFingerprint implements the Value Object pattern from Domain-Driven Design,
where identity is determined by the object's attributes rather than reference equality.
This is perfect for paper duplicate detection because we care about content identity,
not object instance identity.

Key Design Patterns Applied:
1. Value Object Pattern: Immutable, compared by attributes, no identity
2. Factory Method Pattern: from_paper() creates instances from domain entities
3. Strategy Pattern: Different hashing strategies for different identifier types
4. Normalize-Compare Pattern: Text normalization for robust comparison

Academic Paper Identity Challenges:
Academic papers present unique challenges for duplicate detection:
- Multiple identifiers: DOI (gold standard), ArXiv ID, PMID, PubMed Central ID
- Title variations: "Deep Learning" vs "DEEP LEARNING" vs "Deep learning"
- Author formatting: "J. Smith" vs "John Smith" vs "Smith, John"
- Version handling: ArXiv papers have versions (v1, v2, etc.)
- Publication stages: Preprint → Conference → Journal versions

Fingerprinting Strategy:
1. Primary Identifier: Use DOI if available, then ArXiv ID, then composite
2. Title Hash: Normalized, lowercased, common words removed
3. Author Hash: Normalized author names for fuzzy matching
4. Composite Identifier: Hash of (normalized title + first author) when no standard ID

Implementation Philosophy:
- Favor precision over recall: Better to miss some duplicates than create false positives
- Use hierarchical identification: Standard identifiers trump content-based matching
- Enable debugging: Store original identifiers for manual verification
- Performance matters: Fast enough for real-time duplicate checking

Architecture Integration:
PaperFingerprint works with:
- Domain Entities: Creates fingerprints from ResearchPaper objects
- Repository Pattern: Used by repositories to check for existing papers
- Multi-source Aggregation: Prevents duplicate storage across sources
- Analysis Pipeline: Ensures unique papers in research datasets
"""

import hashlib
import re
from dataclasses import dataclass
from typing import Optional, List, Set, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from domain.entities.research_paper import ResearchPaper


@dataclass(frozen=True, eq=False)  # Disable auto-generated equality
class PaperFingerprint:
    """
    Immutable fingerprint for academic paper duplicate detection.

    Educational Note:
    This is a Value Object with custom equality logic. We disable the automatic
    dataclass equality (eq=False) and implement our own __eq__ and __hash__ methods
    to support hierarchical identification strategies.

    Academic Paper Identification Hierarchy:
    1. Reliable identifiers (DOI, ArXiv): If both papers have same reliable ID, they're equal
    2. Composite identifiers: Fall back to content-based comparison (title + author)
    3. Mixed scenarios: Conservative approach - assume different unless proven same

    This approach minimizes false positives while handling real-world variations
    in how academic papers appear across different sources.

    Design Decision: Custom equality over dataclass auto-generation
    Academic paper identification needs domain-specific logic that generic
    dataclass equality can't provide. Same DOI = same paper regardless of
    title formatting differences.

    Attributes:
        primary_identifier: The most reliable identifier (DOI > ArXiv > composite)
        title_hash: Normalized hash of paper title for fuzzy matching
        author_hash: Normalized hash of author names for fuzzy matching
        publication_year: Year for additional validation (papers don't change years)
        source_identifiers: Dict of all available identifiers for debugging
    """

    primary_identifier: str
    title_hash: str
    author_hash: str
    publication_year: Optional[int]
    source_identifiers: dict  # Store original identifiers for debugging

    @classmethod
    def from_paper(cls, paper: "ResearchPaper") -> "PaperFingerprint":
        """
        Factory method to create fingerprint from ResearchPaper entity.

        Educational Note:
        Factory methods are preferred over constructors when:
        1. Complex object creation logic is needed
        2. Multiple creation strategies exist
        3. Creation logic might change over time
        4. Clear intent needs to be expressed

        This factory encapsulates the complex logic of determining which
        identifier to use as primary and how to normalize text fields.

        Args:
            paper: ResearchPaper entity to create fingerprint for

        Returns:
            PaperFingerprint with appropriate identifiers and hashes

        Design Decision: Hierarchical identifier preference
        DOI > ArXiv ID > composite hash ensures consistent identification
        while handling cases where standard identifiers are missing.
        """
        # Collect all available identifiers for debugging
        source_identifiers = {}
        if paper.doi:
            source_identifiers["doi"] = paper.doi
        if hasattr(paper, "arxiv_id") and paper.arxiv_id:
            source_identifiers["arxiv_id"] = paper.arxiv_id
        if hasattr(paper, "pmid") and paper.pmid:
            source_identifiers["pmid"] = paper.pmid

        # Determine primary identifier using hierarchy
        primary_identifier = cls._determine_primary_identifier(paper)

        # Create normalized hashes for fuzzy matching
        title_hash = cls._normalize_title(paper.title)
        author_hash = cls._normalize_authors(paper.authors)

        # Extract publication year if available
        publication_year = None
        if paper.publication_date:
            publication_year = paper.publication_date.year

        return cls(
            primary_identifier=primary_identifier,
            title_hash=title_hash,
            author_hash=author_hash,
            publication_year=publication_year,
            source_identifiers=source_identifiers,
        )

    @staticmethod
    def _determine_primary_identifier(paper: "ResearchPaper") -> str:
        """
        Determine the primary identifier using hierarchical preference.

        Educational Note:
        This method implements the Strategy pattern - different strategies
        for different types of papers. DOI is gold standard when available,
        but we gracefully fall back to other identifiers.

        Hierarchy (most to least reliable):
        1. DOI: Universal, persistent, managed by publishers
        2. ArXiv ID: Reliable for preprints, version-aware
        3. Composite: Hash of normalized title + first author

        Args:
            paper: ResearchPaper to analyze

        Returns:
            String identifier with prefix indicating type
        """
        # DOI is gold standard - most reliable
        if paper.doi:
            return f"doi:{paper.doi.strip()}"

        # ArXiv ID is reliable but need to handle versions
        if hasattr(paper, "arxiv_id") and paper.arxiv_id:
            # Strip version number (v1, v2, etc.) for consistency
            arxiv_clean = re.sub(r"v\d+$", "", paper.arxiv_id.strip())
            return f"arxiv:{arxiv_clean}"

        # PMID for PubMed papers
        if hasattr(paper, "pmid") and paper.pmid:
            return f"pmid:{paper.pmid}"

        # Fall back to composite identifier
        return PaperFingerprint._create_composite_identifier(paper)

    @staticmethod
    def _create_composite_identifier(paper: "ResearchPaper") -> str:
        """
        Create composite identifier from title and first author.

        Educational Note:
        When standard identifiers are unavailable (common with Google Scholar
        or conference proceedings), we create a composite identifier from
        the most stable metadata: title and first author.

        This uses SHA-256 hashing for consistent, collision-resistant
        identification while being reproducible across different runs.

        Args:
            paper: ResearchPaper without standard identifiers

        Returns:
            Composite identifier with 'composite:' prefix
        """
        # Normalize title for consistent hashing
        title_normalized = PaperFingerprint._normalize_title(paper.title)

        # Get first author if available
        first_author = ""
        if paper.authors and len(paper.authors) > 0:
            first_author = PaperFingerprint._normalize_single_author(paper.authors[0])

        # Create composite string and hash
        composite_string = f"{title_normalized}|{first_author}"
        hash_obj = hashlib.sha256(composite_string.encode("utf-8"))
        hash_hex = hash_obj.hexdigest()[:16]  # Use first 16 chars for readability

        return f"composite:{hash_hex}"

    @staticmethod
    def _normalize_title(title: str) -> str:
        """
        Normalize paper title for consistent comparison.

        Educational Note:
        Title normalization is crucial for duplicate detection because:
        1. Different sources may have different capitalization
        2. Punctuation varies across databases
        3. Common words add noise to comparison
        4. Special characters may be encoded differently

        Normalization Strategy:
        - Convert to lowercase for case-insensitive matching
        - Remove punctuation and special characters
        - Remove common academic stopwords ("a", "the", "of", etc.)
        - Collapse whitespace
        - Remove leading/trailing whitespace

        Args:
            title: Original paper title

        Returns:
            Normalized title string suitable for hashing/comparison
        """
        if not title:
            return ""

        # Convert to lowercase
        normalized = title.lower()

        # Remove punctuation and special characters, keep spaces
        normalized = re.sub(r"[^\w\s]", " ", normalized)

        # Remove common academic stopwords that add noise
        stopwords = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "has",
            "he",
            "in",
            "is",
            "it",
            "its",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "were",
            "will",
            "with",
            "the",
            "using",
            "based",
        }

        words = normalized.split()
        words_filtered = [
            word for word in words if word not in stopwords and len(word) > 2
        ]

        # Rejoin and normalize whitespace
        normalized = " ".join(words_filtered)
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return normalized

    @staticmethod
    def _normalize_authors(authors: List[str]) -> str:
        """
        Normalize author list for consistent comparison.

        Educational Note:
        Author normalization handles variations in:
        1. Name formatting: "Dr. John Smith" vs "John Smith" vs "Smith, J."
        2. Title inclusion: "Prof.", "Dr.", "PhD" vs no title
        3. Order: Some sources may reorder authors
        4. Completeness: First author vs all authors

        Strategy:
        - Normalize each author name individually
        - Sort alphabetically for order independence
        - Join with consistent separator
        - Focus on last names which are most stable

        Args:
            authors: List of author names in various formats

        Returns:
            Normalized string of author names suitable for comparison
        """
        if not authors:
            return ""

        normalized_authors = []
        for author in authors:
            normalized_author = PaperFingerprint._normalize_single_author(author)
            if normalized_author:  # Skip empty results
                normalized_authors.append(normalized_author)

        # Sort for order independence
        normalized_authors.sort()

        return "|".join(normalized_authors)

    @staticmethod
    def _normalize_single_author(author: str) -> str:
        """
        Normalize individual author name with enhanced matching.

        Educational Note:
        Enhanced author normalization to handle common academic name variations:

        Common variations handled:
        - "Dr. John Smith" → "j smith"
        - "Smith, John" → "john smith"
        - "J. Smith" → "j smith"
        - "Bob Smith" → "b smith" (first initial + last name)
        - "Prof. Elena Rodriguez-Garcia" → "e rodriguez garcia"

        Strategy for better matching:
        1. Remove titles and honorifics
        2. Handle comma-separated formats (Last, First)
        3. Extract first initial + last name for consistency
        4. Normalize hyphenated names and punctuation

        This approach balances precision with recall for author identification
        across different academic sources that format names differently.

        Args:
            author: Single author name in any format

        Returns:
            Normalized author name (first initial + last name)
        """
        if not author:
            return ""

        # Remove titles and honorifics
        normalized = author.lower()
        titles = ["prof", "dr", "professor", "doctor", "phd", "md", "msc", "bsc"]
        for title in titles:
            # Remove title with various punctuation
            normalized = re.sub(rf"\b{title}\.?\s*", "", normalized)

        # Handle comma-separated format: "Smith, John" -> "John Smith"
        if "," in normalized:
            parts = normalized.split(",", 1)
            if len(parts) == 2:
                last_name = parts[0].strip()
                first_part = parts[1].strip()
                normalized = f"{first_part} {last_name}"

        # Remove punctuation except hyphens in names
        normalized = re.sub(r"[^\w\s\-]", " ", normalized)

        # Normalize whitespace and hyphens
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = re.sub(r"\-+", "-", normalized)
        normalized = normalized.strip()

        # Split into parts for processing
        parts = normalized.split()
        if not parts:
            return ""

        # Enhanced strategy: Extract first initial + last name
        # This handles "Bob Smith" vs "B. Smith" equivalence
        if len(parts) == 1:
            # Only one name - treat as last name
            return parts[0]
        elif len(parts) >= 2:
            # Multiple parts - extract first initial + last name
            first_name = parts[0]
            last_name = parts[-1]  # Last part is surname

            # Get first initial
            first_initial = first_name[0] if first_name else ""

            # Handle hyphenated last names properly
            return f"{first_initial} {last_name}".strip()

        return normalized

    def __eq__(self, other) -> bool:
        """
        Custom equality logic for academic paper identification.

        Educational Note:
        This implements domain-specific equality that matches academic practices:

        1. Reliable Identifier Match: If both papers have the same DOI or ArXiv ID,
           they are the same paper regardless of formatting differences in other fields.

        2. Composite Identifier Match: When both papers lack reliable identifiers,
           we compare all fields (title, author, year) for content-based matching.

        3. Mixed Identifier Types: Conservative approach - different identifier types
           suggest potentially different papers, so we return False for safety.

        This hierarchy prevents false positives while enabling proper duplicate
        detection across multiple academic sources with varying metadata quality.

        Args:
            other: Another object to compare against

        Returns:
            True if fingerprints represent the same academic paper
        """
        if not isinstance(other, PaperFingerprint):
            return False

        # Strategy 1: Reliable identifier comparison
        # If both have DOI or ArXiv identifiers, they are authoritative
        if self.primary_identifier.startswith(
            ("doi:", "arxiv:", "pmid:")
        ) and other.primary_identifier.startswith(("doi:", "arxiv:", "pmid:")):
            return self.primary_identifier == other.primary_identifier

        # Strategy 2: Composite identifier comparison
        # Both papers lack reliable identifiers - compare all content
        if self.primary_identifier.startswith(
            "composite:"
        ) and other.primary_identifier.startswith("composite:"):
            return (
                self.primary_identifier == other.primary_identifier
                and self.title_hash == other.title_hash
                and self.author_hash == other.author_hash
                and self.publication_year == other.publication_year
            )

        # Strategy 3: Mixed identifiers - conservative approach
        # Different identifier types suggest different papers
        return False

    def __hash__(self) -> int:
        """
        Custom hash function supporting hierarchical identification.

        Educational Note:
        Hash function must be consistent with equality. Since our equality
        primarily depends on primary_identifier for reliable IDs, we base
        the hash on that for consistent behavior in sets and dictionaries.

        For composite identifiers, we include all fields to maintain
        the property that equal objects have equal hashes.

        Returns:
            Hash value consistent with __eq__ implementation
        """
        if self.primary_identifier.startswith(("doi:", "arxiv:", "pmid:")):
            # Reliable identifier - hash based on primary identifier only
            return hash(self.primary_identifier)
        else:
            # Composite identifier - hash all relevant fields
            return hash(
                (
                    self.primary_identifier,
                    self.title_hash,
                    self.author_hash,
                    self.publication_year,
                )
            )

    def is_similar_to(self, other: "PaperFingerprint", threshold: float = 0.8) -> bool:
        """
        Check if this fingerprint is similar to another (future implementation).

        Educational Note:
        This method will implement fuzzy matching for papers that might be
        related but not identical. Useful for detecting:
        - Conference vs journal versions
        - Preprint vs published versions
        - Extended versions of the same work

        Args:
            other: Another PaperFingerprint to compare against
            threshold: Similarity threshold (0.0 = no similarity, 1.0 = identical)

        Returns:
            True if fingerprints are similar above threshold

        Implementation Note:
        This is a placeholder for future similarity scoring functionality.
        Will implement after basic equality detection is working properly.
        """
        # Future implementation for fuzzy matching
        # Will use techniques like:
        # - Levenshtein distance for title similarity
        # - Jaccard similarity for author overlap
        # - Publication year proximity
        return False  # Placeholder implementation

    def __str__(self) -> str:
        """
        Human-readable representation for debugging.

        Educational Note:
        Good __str__ methods help with debugging and logging. They should
        provide enough information to understand the object's state without
        being overwhelming.
        """
        return f"PaperFingerprint(id={self.primary_identifier}, title_hash='{self.title_hash[:30]}...', year={self.publication_year})"

    def __repr__(self) -> str:
        """
        Developer representation for debugging.

        Educational Note:
        __repr__ should provide unambiguous representation that could
        ideally be used to recreate the object. Useful for debugging
        and logging in development environments.
        """
        return (
            f"PaperFingerprint(primary_identifier='{self.primary_identifier}', "
            f"title_hash='{self.title_hash}', author_hash='{self.author_hash}', "
            f"publication_year={self.publication_year})"
        )
