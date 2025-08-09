"""
PDF Text Extractor - Infrastructure implementation for extracting text from PDF files.

This adapter demonstrates Clean Architecture infrastructure layer patterns by
implementing the PDFTextExtractorPort interface with actual PDF processing logic.

Educational Notes:
- Shows Adapter pattern for external library integration
- Demonstrates error handling for file processing
- Illustrates infrastructure concerns separated from domain logic
- Shows how to handle different PDF formats and encoding issues

Design Decisions:
- Uses PyPDF2 for broad compatibility
- Implements fallback strategies for problematic PDFs
- Handles text encoding and cleanup
- Provides detailed error reporting for debugging
- Optimizes text extraction for research papers

Use Cases:
- Extract text from academic paper PDFs
- Handle various PDF formats and encodings
- Clean and normalize extracted text
- Provide error diagnostics for failed extractions
"""

from typing import Optional, Dict, Any
from pathlib import Path
import logging
import re

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

from src.application.ports.pdf_extractor_port import PDFTextExtractorPort


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PyPDF2TextExtractor(PDFTextExtractorPort):
    """
    PDF text extraction implementation using PyPDF2.

    Educational Note:
    This adapter implements the PDFTextExtractorPort interface,
    demonstrating how infrastructure implementations can be
    swapped without affecting the application or domain layers.
    """

    def __init__(
        self,
        min_text_length: int = 100,
        max_text_length: int = 1_000_000,
        clean_text: bool = True,
    ):
        """
        Initialize PDF text extractor with configuration.

        Args:
            min_text_length: Minimum text length to consider valid
            max_text_length: Maximum text length to process
            clean_text: Whether to clean and normalize extracted text
        """
        self.min_text_length = min_text_length
        self.max_text_length = max_text_length
        self.clean_text = clean_text

    def extract_text_from_pdf(
        self, pdf_path: Path, extract_metadata: bool = True
    ) -> str:
        """
        Extract text content from a PDF file using PyPDF2.

        Educational Note:
        Main adapter method that handles the complexity of PDF
        processing while providing a clean interface to the
        application layer. Includes comprehensive error handling
        for real-world PDF processing challenges.

        Args:
            pdf_path: Path to the PDF file
            extract_metadata: Whether to extract document metadata (currently not used in text extraction)

        Returns:
            Extracted and cleaned text content

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be processed or contains insufficient text
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.is_file():
            raise ValueError(f"Path is not a file: {pdf_path}")

        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"File is not a PDF: {pdf_path}")

        logger.info(f"Extracting text from PDF: {pdf_path.name}")

        try:
            # Read PDF file
            with open(pdf_path, "rb") as file:
                pdf_reader = PdfReader(file)

                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    # Try to decrypt with empty password
                    if not pdf_reader.decrypt(""):
                        raise ValueError(f"PDF is password protected: {pdf_path}")

                # Extract text from all pages
                text_content = []
                total_pages = len(pdf_reader.pages)

                if total_pages == 0:
                    raise ValueError(f"PDF has no pages: {pdf_path}")

                logger.info(f"Processing {total_pages} pages from {pdf_path.name}")

                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            text_content.append(page_text)
                        else:
                            logger.warning(
                                f"No text extracted from page {page_num + 1}"
                            )

                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num + 1}: {e}")
                        continue

                # Combine all page text
                full_text = "\n".join(text_content)

                if not full_text.strip():
                    raise ValueError(f"No text content extracted from PDF: {pdf_path}")

                # Clean and validate text
                if self.clean_text:
                    full_text = self._clean_extracted_text(full_text)

                # Validate text length
                if len(full_text) < self.min_text_length:
                    raise ValueError(
                        f"Extracted text too short ({len(full_text)} chars, "
                        f"minimum {self.min_text_length}): {pdf_path}"
                    )

                if len(full_text) > self.max_text_length:
                    logger.warning(
                        f"Text very long ({len(full_text)} chars), truncating to "
                        f"{self.max_text_length} chars: {pdf_path.name}"
                    )
                    full_text = full_text[: self.max_text_length]

                logger.info(
                    f"Successfully extracted {len(full_text)} characters "
                    f"from {pdf_path.name}"
                )

                return full_text

        except PdfReadError as e:
            raise ValueError(f"PDF format error in {pdf_path}: {e}")

        except UnicodeDecodeError as e:
            raise ValueError(f"Text encoding error in {pdf_path}: {e}")

        except Exception as e:
            raise ValueError(f"Unexpected error processing {pdf_path}: {e}")

    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean and normalize extracted PDF text.

        Educational Note:
        Text preprocessing is crucial for quality concept extraction.
        This method handles common PDF extraction artifacts while
        preserving meaningful research content and formatting.

        Args:
            text: Raw extracted text

        Returns:
            Cleaned and normalized text
        """
        if not text:
            return ""

        # Fix common PDF extraction issues

        # 1. Remove excessive whitespace and normalize line breaks
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # 2. Fix word breaks caused by line wrapping
        text = re.sub(r"([a-z])-\s*\n\s*([a-z])", r"\1\2", text)

        # 3. Remove page headers/footers patterns
        # Remove isolated numbers (likely page numbers)
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

        # Remove copyright notices and similar
        text = re.sub(r"©.*?\d{4}.*?\n", "", text)
        text = re.sub(r"Copyright.*?\d{4}.*?\n", "", text, flags=re.IGNORECASE)

        # 4. Fix spacing around punctuation
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)
        text = re.sub(r"([,.;:!?])\s+", r"\1 ", text)

        # 5. Remove artifacts from tables and figures
        text = re.sub(
            r"\b(Figure|Fig|Table|Tab)\s*\d+[a-z]?\b.*?\n",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # 6. Clean up reference patterns
        text = re.sub(r"\[\s*\d+\s*\]", "", text)  # Remove [1], [2], etc.
        text = re.sub(r"\(\s*\d+\s*\)", "", text)  # Remove (1), (2), etc.

        # 7. Remove URLs and DOIs from text flow
        text = re.sub(r"https?://[^\s]+", "", text)
        text = re.sub(r"doi:\s*[^\s]+", "", text, flags=re.IGNORECASE)

        # 8. Normalize mathematical expressions
        text = re.sub(r"\s*=\s*", " = ", text)
        text = re.sub(r"\s*±\s*", " ± ", text)

        # 9. Final cleanup
        text = re.sub(r"\s+", " ", text)  # Normalize remaining whitespace
        text = text.strip()

        return text

    def extract_text_with_metadata(self, pdf_path: Path) -> dict:
        """
        Extract text along with PDF metadata.

        Educational Note:
        Extended extraction method that provides additional context
        about the PDF processing, useful for quality assessment
        and debugging extraction issues.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with text and metadata
        """
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PdfReader(file)

                # Extract metadata
                metadata = {
                    "file_path": str(pdf_path),
                    "file_size_mb": pdf_path.stat().st_size / 1_000_000,
                    "page_count": len(pdf_reader.pages),
                    "is_encrypted": pdf_reader.is_encrypted,
                    "pdf_metadata": {},
                }

                # Extract PDF document metadata if available
                if pdf_reader.metadata:
                    for key, value in pdf_reader.metadata.items():
                        if value:
                            metadata["pdf_metadata"][key] = str(value)

                # Extract text
                text = self.extract_text_from_pdf(pdf_path)

                # Add text statistics
                metadata.update(
                    {
                        "text_length": len(text),
                        "word_count": len(text.split()),
                        "paragraph_count": text.count("\n\n") + 1,
                        "extraction_success": True,
                    }
                )

                return {"text": text, "metadata": metadata}

        except Exception as e:
            return {
                "text": "",
                "metadata": {
                    "file_path": str(pdf_path),
                    "extraction_success": False,
                    "error": str(e),
                },
            }

    def validate_pdf_quality(self, pdf_path: Path) -> dict:
        """
        Validate PDF quality for text extraction.

        Educational Note:
        Quality assessment method that provides insights into
        whether a PDF is suitable for concept extraction,
        helping users understand extraction limitations.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with quality assessment results
        """
        try:
            extraction_result = self.extract_text_with_metadata(pdf_path)

            if not extraction_result["metadata"]["extraction_success"]:
                return {
                    "is_suitable": False,
                    "reason": extraction_result["metadata"]["error"],
                    "recommendations": ["File cannot be processed"],
                }

            text = extraction_result["text"]
            metadata = extraction_result["metadata"]

            issues = []
            recommendations = []

            # Check text length
            if len(text) < 500:
                issues.append("Very short text extracted")
                recommendations.append("Check if PDF contains mainly images")

            # Check word density per page
            avg_words_per_page = metadata["word_count"] / max(metadata["page_count"], 1)
            if avg_words_per_page < 100:
                issues.append("Low word density per page")
                recommendations.append("PDF may contain many figures/images")

            # Check for garbled text (high ratio of single characters)
            single_chars = len([w for w in text.split() if len(w) == 1])
            single_char_ratio = single_chars / max(metadata["word_count"], 1)
            if single_char_ratio > 0.3:
                issues.append("High ratio of single characters")
                recommendations.append("Text may be garbled or poorly extracted")

            # Check for reasonable sentence structure
            sentence_count = text.count(".") + text.count("!") + text.count("?")
            if sentence_count < metadata["word_count"] / 50:
                issues.append("Very few sentences detected")
                recommendations.append("Text may lack proper punctuation")

            return {
                "is_suitable": len(issues) < 2,  # Allow some minor issues
                "issues": issues,
                "recommendations": recommendations,
                "text_stats": {
                    "text_length": len(text),
                    "word_count": metadata["word_count"],
                    "avg_words_per_page": round(avg_words_per_page, 1),
                    "single_char_ratio": round(single_char_ratio, 3),
                },
            }

        except Exception as e:
            return {
                "is_suitable": False,
                "reason": str(e),
                "recommendations": ["Unable to process file"],
            }

    def get_pdf_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dict[str, Any]: Dictionary containing PDF metadata

        Educational Notes:
        - Separate metadata extraction for document analysis
        - Dictionary return type enables flexible metadata structure
        - Supports research paper metadata extraction
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PdfReader(file)

                metadata = {
                    "file_path": str(pdf_path),
                    "file_size_mb": round(pdf_path.stat().st_size / 1_000_000, 2),
                    "page_count": len(pdf_reader.pages),
                    "is_encrypted": pdf_reader.is_encrypted,
                    "pdf_info": {},
                }

                # Extract PDF document metadata if available
                if pdf_reader.metadata:
                    for key, value in pdf_reader.metadata.items():
                        if value:
                            # Clean up key names
                            clean_key = key.replace("/", "").lower()
                            metadata["pdf_info"][clean_key] = str(value)

                return metadata

        except PdfReadError as e:
            raise ValueError(f"PDF format error in {pdf_path}: {e}")
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error reading metadata from {pdf_path}: {e}"
            )

    def validate_pdf(self, pdf_path: Path) -> bool:
        """
        Validate if a file is a readable PDF.

        Args:
            pdf_path: Path to the file to validate

        Returns:
            bool: True if file is a valid, readable PDF

        Educational Notes:
        - Pre-processing validation prevents extraction errors
        - Boolean return enables simple validation checks
        - Supports batch processing workflows
        """
        try:
            # Check if file exists and is a file
            if not pdf_path.exists() or not pdf_path.is_file():
                return False

            # Check file extension
            if pdf_path.suffix.lower() != ".pdf":
                return False

            # Try to open and read basic PDF structure
            with open(pdf_path, "rb") as file:
                pdf_reader = PdfReader(file)

                # Check if we can access page count (basic validation)
                page_count = len(pdf_reader.pages)

                # Must have at least one page
                if page_count == 0:
                    return False

                # If encrypted, try to decrypt with empty password
                if pdf_reader.is_encrypted:
                    if not pdf_reader.decrypt(""):
                        return False

                # Try to extract text from first page as additional validation
                first_page = pdf_reader.pages[0]
                first_page.extract_text()  # This will raise exception if corrupted

                return True

        except (PdfReadError, ValueError, IOError, OSError):
            return False
        except Exception:
            # Catch any other unexpected errors
            return False
