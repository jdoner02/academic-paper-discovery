"""
PaperDownloadService - Domain service for downloading research papers.

This service provides functionality to download research papers and organize
them in a structured file system. It demonstrates domain services in Clean
Architecture - business logic that doesn't naturally fit in entities.

Educational Notes:
- Domain Service: Business logic that operates on multiple entities
- Single Responsibility: Focused solely on paper downloading
- Clean Architecture: No dependencies on infrastructure details
- Repository Pattern: Uses repository to get download URLs

Design Decisions:
- Downloads to organized directory structure by date and strategy
- Saves metadata alongside PDFs for searchability
- Provides progress tracking for user feedback
- Handles download failures gracefully

Use Cases:
- Downloading papers found through search
- Building local research libraries
- Offline access to research papers
- Systematic literature review data collection
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Optional, Dict, Callable
from datetime import datetime, timezone

from src.domain.entities.research_paper import ResearchPaper


class PaperDownloadService:
    """
    Domain service for downloading and organizing research papers.

    This service coordinates paper downloading with file organization,
    demonstrating how domain services handle complex business operations
    that span multiple entities.
    """

    def __init__(self, base_output_dir: str = "outputs"):
        """
        Initialize download service with output directory.

        Args:
            base_output_dir: Root directory for downloaded papers
        """
        self.base_output_dir = Path(base_output_dir)
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Research-Paper-Aggregator/1.0 (Educational Purpose)"}
        )

    def download_papers(
        self,
        papers: List[ResearchPaper],
        strategy_name: str,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> Dict[str, str]:
        """
        Download a collection of research papers with progress tracking.

        Args:
            papers: List of ResearchPaper entities to download
            strategy_name: Name of search strategy used (for organization)
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary mapping paper titles to download status/file paths
        """
        # Create output directory structure
        output_dir = self._create_output_directory(strategy_name)

        # Track download results
        results = {}
        successful_downloads = []

        total_papers = len(papers)

        for i, paper in enumerate(papers):
            if progress_callback:
                progress_callback(i + 1, total_papers, paper.title)

            try:
                # Download paper PDF
                pdf_path = self._download_paper_pdf(paper, output_dir)
                if pdf_path:
                    results[paper.title] = str(pdf_path)
                    successful_downloads.append(paper)
                else:
                    results[paper.title] = "Download failed - No PDF URL available"

            except Exception as e:
                results[paper.title] = f"Download failed - {str(e)}"

        # Save metadata for successfully downloaded papers
        if successful_downloads:
            self._save_metadata(successful_downloads, output_dir, strategy_name)

        return results

    def download_single_paper(
        self, paper: ResearchPaper, output_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Download a single research paper.

        Args:
            paper: ResearchPaper entity to download
            output_dir: Optional custom output directory

        Returns:
            Path to downloaded PDF file, or None if download failed
        """
        if not output_dir:
            output_dir = self._create_output_directory("single_downloads")

        return self._download_paper_pdf(paper, output_dir)

    def _create_output_directory(self, strategy_name: str) -> Path:
        """
        Create organized output directory structure.

        Creates directories like: outputs/2025-08-05_comprehensive_research/

        Educational Note:
        - Uses timestamp prefix for chronological organization
        - Strategy name provides clear context for the search
        - Creates parent directories as needed for robustness
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        dir_name = f"{timestamp}_{strategy_name}"
        output_dir = self.base_output_dir / dir_name

        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def _download_paper_pdf(
        self, paper: ResearchPaper, output_dir: Path
    ) -> Optional[Path]:
        """
        Download PDF for a single paper.

        Args:
            paper: ResearchPaper entity with download information
            output_dir: Directory to save the PDF

        Returns:
            Path to downloaded file, or None if download failed
        """
        # Get PDF URL from paper
        pdf_url = self._get_pdf_url(paper)
        if not pdf_url:
            return None

        # Create safe filename from paper title
        safe_title = self._sanitize_filename(paper.title)
        pdf_filename = f"{safe_title}.pdf"
        pdf_path = output_dir / pdf_filename

        try:
            # Download PDF
            response = self.session.get(pdf_url, timeout=60, stream=True)
            response.raise_for_status()

            # Save PDF to file
            with open(pdf_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return pdf_path

        except requests.RequestException as e:
            print(f"Error downloading {paper.title}: {e}")
            return None
        except Exception as e:
            print(f"Error saving {paper.title}: {e}")
            return None

    def _get_pdf_url(self, paper: ResearchPaper) -> Optional[str]:
        """
        Extract PDF URL from ResearchPaper entity.

        Handles different types of PDF URLs and DOI resolution.
        """
        # Check for direct PDF URL (arXiv papers)
        if hasattr(paper, "pdf_url") and paper.pdf_url:
            return paper.pdf_url

        # Check for arXiv ID
        if hasattr(paper, "arxiv_id") and paper.arxiv_id:
            return f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"

        return None

    def _sanitize_filename(self, filename: str) -> str:
        """
        Create a safe filename from paper title.

        Removes characters that aren't safe for filenames across platforms.
        """
        # Remove or replace problematic characters
        safe_chars = []
        for char in filename:
            if char.isalnum() or char in (" ", "-", "_", "."):
                safe_chars.append(char)
            else:
                safe_chars.append("_")

        # Join and clean up multiple spaces/underscores
        safe_name = "".join(safe_chars)
        safe_name = " ".join(safe_name.split())  # Remove extra spaces
        safe_name = safe_name.replace(" ", "_")

        # Limit length for filesystem compatibility
        if len(safe_name) > 100:
            safe_name = safe_name[:97] + "..."

        return safe_name

    def _save_metadata(
        self, papers: List[ResearchPaper], output_dir: Path, strategy_name: str
    ) -> None:
        """
        Save metadata for downloaded papers.

        Creates a JSON file with all paper metadata for searchability
        and record-keeping.
        """
        metadata = {
            "download_info": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "strategy_name": strategy_name,
                "total_papers": len(papers),
                "download_directory": str(output_dir),
            },
            "papers": [],
        }

        for paper in papers:
            paper_data = {
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "publication_date": (
                    paper.publication_date.isoformat()
                    if paper.publication_date
                    else None
                ),
                "doi": paper.doi,
                "venue": paper.venue,
                "citation_count": paper.citation_count,
                "keywords": paper.keywords,
            }

            # Add arXiv-specific fields if present
            if hasattr(paper, "arxiv_id"):
                paper_data["arxiv_id"] = paper.arxiv_id
            if hasattr(paper, "pdf_url"):
                paper_data["pdf_url"] = paper.pdf_url

            metadata["papers"].append(paper_data)

        # Save metadata file
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def get_download_summary(self, results: Dict[str, str]) -> Dict[str, int]:
        """
        Generate summary statistics for download results.

        Args:
            results: Dictionary from download_papers method

        Returns:
            Summary with success/failure counts
        """
        successful = sum(
            1 for path in results.values() if not path.startswith("Download failed")
        )
        failed = len(results) - successful

        return {
            "total_attempted": len(results),
            "successful_downloads": successful,
            "failed_downloads": failed,
            "success_rate": (successful / len(results)) * 100 if results else 0,
        }
