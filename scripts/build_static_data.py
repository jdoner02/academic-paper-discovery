#!/usr/bin/env python3
"""
Static Data Builder for Research Paper Discovery Platform

This script transforms the existing concept_storage and outputs data into
optimized static JSON files for client-side consumption on GitHub Pages.

Educational Notes:
- Demonstrates data transformation for static web deployment
- Shows efficient client-server architecture patterns
- Illustrates GitHub Pages optimization strategies

Design Decisions:
- Static JSON over dynamic APIs for GitHub Pages compatibility
- Optimized data structures for fast client-side loading
- Preservation of all research work in accessible format
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import re


class StaticDataBuilder:
    """
    Transforms concept storage and PDF outputs into static web-friendly data.

    Educational Notes:
    - Builder Pattern: Constructs complex data structures step by step
    - Strategy Pattern: Different build strategies for different data types
    - Single Responsibility: Each method handles one aspect of data transformation
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.concept_storage_path = base_path / "concept_storage" / "concepts"
        self.outputs_path = base_path / "outputs"
        self.static_data_path = base_path / "static_data"

        # Ensure static data directory exists
        self.static_data_path.mkdir(exist_ok=True)

    def build_domain_index(self) -> Dict[str, Any]:
        """
        Build master index of all available research domains.

        Returns:
            dict: Domain metadata with paper counts and descriptions
        """
        domains = {}

        if not self.concept_storage_path.exists():
            return domains

        for domain_dir in sorted(self.concept_storage_path.iterdir()):
            if not domain_dir.is_dir():
                continue

            domain_name = domain_dir.name
            concept_files = list(domain_dir.glob("*.json"))

            # Filter out index files
            paper_files = [f for f in concept_files if not f.name.startswith("_")]

            domains[domain_name] = {
                "name": domain_name,
                "display_name": self._format_domain_name(domain_name),
                "paper_count": len(paper_files),
                "last_updated": self._get_latest_timestamp(paper_files),
                "description": self._generate_domain_description(domain_name),
            }

        return domains

    def build_domain_concepts(self, domain_name: str) -> Dict[str, Any]:
        """
        Build aggregated concept data for a specific domain.

        Args:
            domain_name: Name of the domain to process

        Returns:
            dict: Aggregated concepts with evidence and PDF links
        """
        domain_path = self.concept_storage_path / domain_name
        if not domain_path.exists():
            return {}

        concepts_data = {
            "domain": domain_name,
            "concepts": [],
            "papers": {},
            "statistics": {
                "total_concepts": 0,
                "total_papers": 0,
                "avg_concepts_per_paper": 0,
            },
        }

        concept_files = [
            f for f in domain_path.glob("*.json") if not f.name.startswith("_")
        ]

        all_concepts = {}
        papers = {}

        for concept_file in concept_files:
            try:
                with open(concept_file, "r", encoding="utf-8") as f:
                    paper_data = json.load(f)

                paper_id = paper_data.get("paper_doi", concept_file.stem)
                paper_title = paper_data.get("paper_title", "Unknown Title")

                # Find corresponding PDF
                pdf_path = self._find_pdf_for_paper(domain_name, paper_title)

                papers[paper_id] = {
                    "id": paper_id,
                    "title": paper_title,
                    "pdf_url": pdf_path,
                    "concept_count": len(paper_data.get("concepts", [])),
                }

                # Process concepts
                for concept in paper_data.get("concepts", []):
                    concept_text = concept.get("text", "")
                    if not concept_text:
                        continue

                    if concept_text not in all_concepts:
                        all_concepts[concept_text] = {
                            "text": concept_text,
                            "total_frequency": 0,
                            "avg_relevance": 0,
                            "source_papers": [],
                            "evidence_sentences": [],
                        }

                    # Aggregate concept data
                    all_concepts[concept_text]["total_frequency"] += concept.get(
                        "frequency", 0
                    )
                    all_concepts[concept_text]["source_papers"].append(paper_id)

                    # Add evidence sentences if available
                    if "evidence_sentences" in concept:
                        for sentence in concept["evidence_sentences"][
                            :3
                        ]:  # Limit to top 3
                            all_concepts[concept_text]["evidence_sentences"].append(
                                {
                                    "text": sentence,
                                    "paper_id": paper_id,
                                    "paper_title": paper_title,
                                }
                            )

            except Exception as e:
                print(f"Error processing {concept_file}: {e}")
                continue

        # Convert to list and calculate statistics
        concepts_list = []
        for concept_text, concept_data in all_concepts.items():
            # Calculate average relevance
            concept_data["avg_relevance"] = min(
                0.9, concept_data["total_frequency"] / 100
            )
            concept_data["source_papers"] = list(set(concept_data["source_papers"]))
            concepts_list.append(concept_data)

        # Sort by frequency
        concepts_list.sort(key=lambda x: x["total_frequency"], reverse=True)

        # Calculate statistics
        concepts_data["concepts"] = concepts_list[:100]  # Top 100 concepts
        concepts_data["papers"] = papers
        concepts_data["statistics"] = {
            "total_concepts": len(concepts_list),
            "total_papers": len(papers),
            "avg_concepts_per_paper": len(concepts_list) / max(len(papers), 1),
        }

        return concepts_data

    def _find_pdf_for_paper(self, domain_name: str, paper_title: str) -> str:
        """
        Find PDF file path for a given paper.

        Args:
            domain_name: Research domain
            paper_title: Title of the paper

        Returns:
            str: Relative path to PDF or empty string if not found
        """
        # Clean title for filename matching
        clean_title = re.sub(r"[^\w\s-]", "", paper_title).strip()
        clean_title = re.sub(r"\s+", "_", clean_title)

        # Search in outputs directory
        domain_outputs = self.outputs_path / domain_name
        if not domain_outputs.exists():
            return ""

        # Search in all strategy subdirectories
        for strategy_dir in domain_outputs.iterdir():
            if not strategy_dir.is_dir():
                continue

            pdfs_dir = strategy_dir / "pdfs"
            if not pdfs_dir.exists():
                continue

            # Look for matching PDF files
            for pdf_file in pdfs_dir.glob("*.pdf"):
                if clean_title.lower() in pdf_file.stem.lower():
                    # Return relative path from repository root
                    return str(pdf_file.relative_to(self.base_path))

        return ""

    def _format_domain_name(self, domain_name: str) -> str:
        """Convert snake_case domain name to human-readable format."""
        return domain_name.replace("_", " ").title()

    def _get_latest_timestamp(self, files: List[Path]) -> str:
        """Get the latest modification timestamp from a list of files."""
        if not files:
            return datetime.now().isoformat()

        latest = max(f.stat().st_mtime for f in files)
        return datetime.fromtimestamp(latest).isoformat()

    def _generate_domain_description(self, domain_name: str) -> str:
        """Generate a description for the research domain."""
        descriptions = {
            "incident_response_optimization": "Operations research and optimization models for emergency response and disaster recovery",
            "post_quantum_cryptography_implementation": "Implementation strategies and practical deployment of quantum-resistant cryptographic systems",
            "water_infrastructure_incident_response": "Cybersecurity incident response frameworks for water utility infrastructure",
            "cybersecurity_game_theory": "Game-theoretic approaches to cybersecurity strategy and defense optimization",
            "medical_device_cybersecurity": "Security frameworks and risk assessment for connected medical devices",
            "ai_driven_cyber_defense": "Artificial intelligence and machine learning applications in cybersecurity defense",
        }

        return descriptions.get(
            domain_name,
            f"Research and analysis in {self._format_domain_name(domain_name)}",
        )

    def build_all_static_data(self):
        """
        Build complete static data structure for the web application.

        Educational Notes:
        - Template Method Pattern: Defines skeleton of data building process
        - Facade Pattern: Provides simple interface to complex data transformation
        """
        print("Building static data for GitHub Pages deployment...")

        # Build domain index
        print("Building domain index...")
        domains = self.build_domain_index()

        with open(self.static_data_path / "domains.json", "w", encoding="utf-8") as f:
            json.dump(domains, f, indent=2, ensure_ascii=False)

        print(f"Built index for {len(domains)} domains")

        # Build concept data for each domain
        for domain_name in domains.keys():
            print(f"Building concept data for {domain_name}...")

            domain_data = self.build_domain_concepts(domain_name)

            # Create domain-specific directory
            domain_dir = self.static_data_path / domain_name
            domain_dir.mkdir(exist_ok=True)

            # Save concept data
            with open(domain_dir / "concepts.json", "w", encoding="utf-8") as f:
                json.dump(domain_data, f, indent=2, ensure_ascii=False)

            print(f"  - {len(domain_data['concepts'])} concepts")
            print(f"  - {len(domain_data['papers'])} papers")

        # Build overall statistics
        total_concepts = sum(
            len(self.build_domain_concepts(domain)["concepts"])
            for domain in domains.keys()
        )
        total_papers = sum(domains[domain]["paper_count"] for domain in domains.keys())

        statistics = {
            "total_domains": len(domains),
            "total_concepts": total_concepts,
            "total_papers": total_papers,
            "last_updated": datetime.now().isoformat(),
            "deployment_type": "static_github_pages",
        }

        with open(
            self.static_data_path / "statistics.json", "w", encoding="utf-8"
        ) as f:
            json.dump(statistics, f, indent=2, ensure_ascii=False)

        print("\n✅ Static data build complete!")
        print(f"   📊 {statistics['total_domains']} domains")
        print(f"   🔬 {statistics['total_concepts']} concepts")
        print(f"   📄 {statistics['total_papers']} papers")
        print(f"   📁 Data saved to: {self.static_data_path}")


def main():
    """Build static data for GitHub Pages deployment."""
    base_path = Path(__file__).parent.parent
    builder = StaticDataBuilder(base_path)
    builder.build_all_static_data()


if __name__ == "__main__":
    main()
