"""
PDFTextExtractorPort - Port for PDF text extraction services.

This port defines the interface for PDF text extraction, following the
Port/Adapter pattern in Clean Architecture. It provides abstraction
between the application layer and infrastructure concerns.

Educational Notes:
- Shows Port/Adapter pattern for external service integration
- Demonstrates interface segregation and dependency inversion
- Illustrates how to abstract infrastructure concerns
- Provides contract for PDF processing implementations

Design Decisions:
- Abstract interface defines expected behavior
- Error handling contracts for robust extraction
- Metadata extraction for document analysis
- Support for different PDF formats and structures

Use Cases:
- Research paper PDF text extraction
- Academic document processing
- Batch PDF analysis workflows
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional


class PDFTextExtractorPort(ABC):
    """
    Abstract port for PDF text extraction services.

    This interface defines the contract for extracting text content
    from PDF files, enabling different PDF processing implementations
    while maintaining consistent application layer integration.

    Educational Notes:
    - Abstract base class ensures implementation compliance
    - Type hints provide clear interface contracts
    - Error handling enables robust extraction workflows
    - Metadata extraction supports document analysis
    """

    @abstractmethod
    def extract_text_from_pdf(
        self, pdf_path: Path, extract_metadata: bool = True
    ) -> str:
        """
        Extract text content from a PDF file.

        Args:
            pdf_path: Path to the PDF file to process
            extract_metadata: Whether to extract document metadata

        Returns:
            str: Extracted text content from the PDF

        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the PDF is corrupted or unreadable
            RuntimeError: If extraction fails due to processing issues

        Educational Notes:
        - Abstract method ensures all implementations provide this functionality
        - Path parameter enables file system abstraction
        - Metadata flag provides optional enhanced extraction
        - Clear error contracts enable robust error handling
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
