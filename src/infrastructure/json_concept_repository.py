"""
JSON Concept Repository - Infrastructure implementation for concept persistence.

This repository demonstrates Clean Architecture infrastructure layer patterns by
implementing concept storage using JSON files for simplicity and portability.

Educational Notes:
- Shows Repository pattern implementation
- Demonstrates file-based persistence strategy
- Illustrates data serialization and deserialization
- Shows how to maintain data consistency with file operations

Design Decisions:
- JSON format for human readability and debugging
- Domain-based file organization for scalability
- Atomic file operations to prevent corruption
- Comprehensive error handling and validation
- Statistics caching for performance

Use Cases:
- Persist concept extraction results
- Query concepts by domain or paper
- Generate analytics and statistics
- Export data for visualization tools
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import os
from datetime import datetime, timezone
from collections import defaultdict

from src.application.use_cases.extract_paper_concepts_use_case import (
    ConceptRepositoryPort,
)
from src.domain.entities.paper_concepts import PaperConcepts


class JSONConceptRepository(ConceptRepositoryPort):
    """
    JSON file-based repository for concept persistence.

    Educational Note:
    This repository implementation demonstrates how infrastructure
    can be kept simple and maintainable while still providing
    all necessary persistence functionality for the domain.
    """

    def __init__(self, storage_directory: Path):
        """
        Initialize repository with storage directory.

        Args:
            storage_directory: Directory to store concept files
        """
        self.storage_directory = Path(storage_directory)
        self.storage_directory.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.concepts_dir = self.storage_directory / "concepts"
        self.stats_dir = self.storage_directory / "statistics"
        self.concepts_dir.mkdir(exist_ok=True)
        self.stats_dir.mkdir(exist_ok=True)

    def save_paper_concepts(self, paper_concepts: PaperConcepts) -> None:
        """
        Save paper concepts to JSON file.

        Educational Note:
        Implements atomic file operations to ensure data consistency
        even if the process is interrupted during writing. Uses
        temporary files and atomic moves for reliability.

        Args:
            paper_concepts: PaperConcepts entity to save
        """
        if not isinstance(paper_concepts, PaperConcepts):
            raise ValueError("Must provide PaperConcepts entity")

        # Create domain directory if it doesn't exist
        domain = (
            paper_concepts.concepts[0].source_domain
            if paper_concepts.concepts
            else "unknown"
        )
        domain_dir = self.concepts_dir / domain
        domain_dir.mkdir(exist_ok=True)

        # Generate filename from DOI (sanitize for filesystem)
        safe_doi = self._sanitize_filename(paper_concepts.paper_doi)
        file_path = domain_dir / f"{safe_doi}.json"

        # Prepare data for serialization
        data = paper_concepts.to_dict()
        data["_metadata"] = {
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "repository_version": "1.0",
            "domain": domain,
        }

        # Atomic write operation
        temp_path = file_path.with_suffix(".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic move (rename is atomic on most filesystems)
            temp_path.replace(file_path)

            # Update domain index
            self._update_domain_index(
                domain, paper_concepts.paper_doi, paper_concepts.paper_title
            )

        except Exception as e:
            # Cleanup temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            raise ValueError(f"Failed to save paper concepts: {e}")

    def find_paper_concepts_by_doi(self, doi: str) -> Optional[PaperConcepts]:
        """
        Find paper concepts by DOI.

        Educational Note:
        Demonstrates how repositories can provide efficient lookups
        by maintaining indices and using filesystem organization
        to minimize search space.

        Args:
            doi: DOI of the paper to find

        Returns:
            PaperConcepts if found, None otherwise
        """
        if not doi:
            return None

        # Search across all domain directories
        safe_doi = self._sanitize_filename(doi)

        for domain_dir in self.concepts_dir.iterdir():
            if not domain_dir.is_dir():
                continue

            file_path = domain_dir / f"{safe_doi}.json"
            if file_path.exists():
                try:
                    return self._load_paper_concepts_from_file(file_path)
                except Exception as e:
                    print(f"Error loading concepts from {file_path}: {e}")
                    continue

        return None

    def find_all_concepts_in_domain(self, domain: str) -> List[PaperConcepts]:
        """
        Find all paper concepts in a specific domain.

        Educational Note:
        Batch loading method that demonstrates efficient file
        processing and error recovery for large datasets.

        Args:
            domain: Research domain to search

        Returns:
            List of all PaperConcepts in the domain
        """
        if not domain:
            return []

        domain_dir = self.concepts_dir / domain
        if not domain_dir.exists():
            return []

        results = []
        errors = []

        for file_path in domain_dir.glob("*.json"):
            try:
                paper_concepts = self._load_paper_concepts_from_file(file_path)
                if paper_concepts:
                    results.append(paper_concepts)
            except Exception as e:
                errors.append(f"Error loading {file_path}: {e}")

        if errors:
            print(f"Encountered {len(errors)} errors loading domain {domain}")
            for error in errors[:3]:  # Show first 3 errors
                print(f"  - {error}")

        return results

    def get_extraction_statistics(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive statistics about concept extractions.

        Educational Note:
        Analytics method that demonstrates how repositories can
        provide business intelligence by aggregating data across
        multiple entities and domains.

        Args:
            domain: Specific domain to analyze (all domains if None)

        Returns:
            Dictionary with extraction statistics
        """
        try:
            # Cache statistics to avoid expensive recalculation
            cache_file = self.stats_dir / f"stats_{domain or 'all'}.json"

            # Check if cached stats are recent (less than 1 hour old)
            if cache_file.exists():
                cache_age = datetime.now().timestamp() - cache_file.stat().st_mtime
                if cache_age < 3600:  # 1 hour in seconds
                    with open(cache_file, "r", encoding="utf-8") as f:
                        cached_stats = json.load(f)
                        cached_stats["_cached"] = True
                        return cached_stats

            # Calculate fresh statistics
            stats = self._calculate_statistics(domain)

            # Cache the results
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(stats, f, indent=2, ensure_ascii=False)
            except Exception:
                pass  # Don't fail if caching fails

            return stats

        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    def _load_paper_concepts_from_file(
        self, file_path: Path
    ) -> Optional[PaperConcepts]:
        """
        Load paper concepts from JSON file.

        Educational Note:
        Deserialization method that handles file format evolution
        and validation to ensure data integrity during loading.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate data structure
            required_fields = ["paper_doi", "paper_title", "concepts"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            # Convert back to entity
            return PaperConcepts.from_dict(data)

        except Exception as e:
            raise ValueError(f"Failed to load paper concepts from {file_path}: {e}")

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize DOI or other identifier for use as filename.

        Educational Note:
        Utility method that handles the common infrastructure
        concern of converting identifiers to filesystem-safe names
        while maintaining uniqueness and readability.
        """
        # Replace problematic characters
        safe_chars = []
        for char in filename:
            if char.isalnum() or char in "-_.":
                safe_chars.append(char)
            elif char in "/\\:":
                safe_chars.append("_")
            else:
                safe_chars.append("_")

        result = "".join(safe_chars)

        # Ensure not too long for filesystem limits
        if len(result) > 200:
            result = result[:200]

        # Ensure not empty
        if not result:
            result = "unnamed"

        return result

    def _update_domain_index(self, domain: str, doi: str, title: str) -> None:
        """
        Update domain index with new paper information.

        Educational Note:
        Maintains an index file for each domain to enable efficient
        queries and statistics generation without scanning all files.
        """
        try:
            index_file = self.concepts_dir / domain / "_index.json"

            # Load existing index
            if index_file.exists():
                with open(index_file, "r", encoding="utf-8") as f:
                    index = json.load(f)
            else:
                index = {
                    "domain": domain,
                    "papers": {},
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }

            # Update index
            index["papers"][doi] = {
                "title": title,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            index["last_updated"] = datetime.now(timezone.utc).isoformat()

            # Save index
            with open(index_file, "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)

        except Exception as e:
            # Index update failure shouldn't prevent main operation
            print(f"Warning: Failed to update domain index for {domain}: {e}")

    def _calculate_statistics(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics across domains.

        Educational Note:
        Statistics calculation method that demonstrates data
        aggregation and analysis capabilities of repositories
        for business intelligence purposes.
        """
        stats = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain": domain or "all",
            "total_papers": 0,
            "total_concepts": 0,
            "domains": {},
            "extraction_methods": defaultdict(int),
            "concept_frequency": defaultdict(int),
            "quality_metrics": {
                "high_quality_concepts": 0,
                "average_relevance": 0.0,
                "concepts_per_paper": 0.0,
            },
        }

        # Determine which domains to process
        domains_to_process = []
        if domain:
            domain_dir = self.concepts_dir / domain
            if domain_dir.exists():
                domains_to_process = [domain]
        else:
            domains_to_process = [
                d.name for d in self.concepts_dir.iterdir() if d.is_dir()
            ]

        # Process each domain
        all_relevance_scores = []
        for domain_name in domains_to_process:
            domain_stats = self._calculate_domain_statistics(domain_name)
            stats["domains"][domain_name] = domain_stats

            # Aggregate totals
            stats["total_papers"] += domain_stats["paper_count"]
            stats["total_concepts"] += domain_stats["concept_count"]

            # Aggregate extraction methods
            for method, count in domain_stats["extraction_methods"].items():
                stats["extraction_methods"][method] += count

            # Aggregate concept frequencies
            for concept, freq in domain_stats["top_concepts"][:20]:  # Top 20 per domain
                stats["concept_frequency"][concept] += freq

            # Collect relevance scores
            all_relevance_scores.extend(domain_stats.get("relevance_scores", []))

        # Calculate quality metrics
        if all_relevance_scores:
            stats["quality_metrics"]["average_relevance"] = sum(
                all_relevance_scores
            ) / len(all_relevance_scores)
            stats["quality_metrics"]["high_quality_concepts"] = len(
                [s for s in all_relevance_scores if s >= 0.7]
            )

        if stats["total_papers"] > 0:
            stats["quality_metrics"]["concepts_per_paper"] = (
                stats["total_concepts"] / stats["total_papers"]
            )

        # Convert defaultdicts to regular dicts for JSON serialization
        stats["extraction_methods"] = dict(stats["extraction_methods"])
        stats["concept_frequency"] = dict(
            sorted(
                stats["concept_frequency"].items(), key=lambda x: x[1], reverse=True
            )[:50]
        )  # Top 50 concepts overall

        return stats

    def _calculate_domain_statistics(self, domain: str) -> Dict[str, Any]:
        """Calculate statistics for a specific domain."""
        domain_dir = self.concepts_dir / domain
        if not domain_dir.exists():
            return {}

        paper_count = 0
        concept_count = 0
        extraction_methods = defaultdict(int)
        concept_frequency = defaultdict(int)
        relevance_scores = []

        for file_path in domain_dir.glob("*.json"):
            if file_path.name.startswith("_"):  # Skip index files
                continue

            try:
                paper_concepts = self._load_paper_concepts_from_file(file_path)
                if not paper_concepts:
                    continue

                paper_count += 1
                concept_count += len(paper_concepts.concepts)

                for concept in paper_concepts.concepts:
                    extraction_methods[concept.extraction_method] += 1
                    concept_frequency[concept.text.lower()] += concept.frequency
                    relevance_scores.append(concept.relevance_score)

            except Exception:
                continue  # Skip problematic files

        # Top concepts for this domain
        top_concepts = sorted(
            concept_frequency.items(), key=lambda x: x[1], reverse=True
        )[:30]

        return {
            "domain": domain,
            "paper_count": paper_count,
            "concept_count": concept_count,
            "extraction_methods": dict(extraction_methods),
            "top_concepts": top_concepts,
            "relevance_scores": relevance_scores,
            "avg_concepts_per_paper": round(concept_count / max(paper_count, 1), 2),
        }

    def export_domain_for_visualization(self, domain: str, output_path: Path) -> None:
        """
        Export domain data in format suitable for web visualization.

        Educational Note:
        Data export method that demonstrates how repositories can
        serve as integration points between internal data storage
        and external presentation systems.

        Args:
            domain: Domain to export
            output_path: Directory to write visualization files
        """
        try:
            all_paper_concepts = self.find_all_concepts_in_domain(domain)

            if not all_paper_concepts:
                print(f"No data found for domain: {domain}")
                return

            output_path.mkdir(parents=True, exist_ok=True)

            # Export raw paper concepts data
            papers_data = []
            for paper_concepts in all_paper_concepts:
                papers_data.append(paper_concepts.to_dict())

            with open(output_path / "papers_concepts.json", "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "domain": domain,
                        "papers": papers_data,
                        "exported_at": datetime.now(timezone.utc).isoformat(),
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

            # Export domain statistics
            stats = self.get_extraction_statistics(domain)
            with open(
                output_path / "domain_statistics.json", "w", encoding="utf-8"
            ) as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)

            print(f"Visualization data exported to {output_path}")

        except Exception as e:
            raise ValueError(f"Failed to export domain data: {e}")
