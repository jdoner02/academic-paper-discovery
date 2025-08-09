"""
JSON-based concept parser for elastic stack compatible atomic concept definitions.
Replaces the             # Create ConceptNode
            concept = ConceptNode(
                name=concept_data['name'],
                type=concept_data['type'],
                description=concept_data['informal_description'],
                mathematical_definition=concept_data['formal_statement'],
                subject_area=concept_data['domain'],
                complexity_level=self._map_level_to_complexity(concept_data['level']),
                cognitive_load=min(10, max(1, concept_data.get('difficulty', 5))),
                prerequisites=frozenset(concept_data.get('depends_on', [])),
                examples=tuple(self._extract_examples(concept_data.get('examples', []))),
                pedagogical_notes=concept_data.get('pedagogical_notes', '')
            ) parser with JSON format for better programmatic access.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime

from .concept_node import ConceptNode
from .relationship_types import RelationshipType


@dataclass
class ConceptMetadata:
    """Rich metadata for concepts compatible with elastic stack indexing."""

    domain: str
    subdomain: Optional[str]
    level: str
    difficulty: int
    tags: List[str]
    timestamp: datetime
    elastic_metadata: Optional[Dict]


class JSONConceptParser:
    """
    Parser for JSON-based concept definitions with elastic stack compatibility.

    This parser reads concepts from hierarchically organized JSON files,
    validating against the schema and building relationship graphs.
    """

    def __init__(self, concepts_directory: str = "concept_definitions"):
        self.concepts_directory = Path(concepts_directory)
        self.schema_path = Path(
            "src/educational/atomic_concepts/schema/concept_schema.json"
        )
        self.concepts_cache: Dict[str, ConceptNode] = {}
        self.metadata_cache: Dict[str, ConceptMetadata] = {}

    def load_schema(self) -> Dict:
        """Load and return the JSON schema for validation."""
        try:
            with open(self.schema_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found at {self.schema_path}")

    def discover_concept_files(self) -> List[Path]:
        """
        Recursively discover all JSON concept files in the hierarchy.

        Returns:
            List of Path objects for all .json files in the concepts directory
        """
        concept_files = []

        if not self.concepts_directory.exists():
            return concept_files

        for json_file in self.concepts_directory.rglob("*.json"):
            concept_files.append(json_file)

        return sorted(concept_files)

    def load_concept_from_file(self, file_path: Path) -> Optional[ConceptNode]:
        """
        Load a single concept from a JSON file.

        Args:
            file_path: Path to the JSON concept file

        Returns:
            ConceptNode instance or None if loading fails
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                concept_data = json.load(f)

            # Validate required fields
            required_fields = [
                "id",
                "name",
                "type",
                "domain",
                "level",
                "formal_statement",
                "informal_description",
            ]

            for field in required_fields:
                if field not in concept_data:
                    print(f"Warning: Missing required field '{field}' in {file_path}")
                    return None

            # Create ConceptNode
            concept = ConceptNode(
                name=concept_data["name"],
                type=concept_data["type"],
                description=concept_data["informal_description"],
                mathematical_definition=concept_data["formal_statement"],
                subject_area=concept_data["domain"],
                complexity_level=self._map_level_to_complexity(concept_data["level"]),
                cognitive_load=min(10, max(1, concept_data.get("difficulty", 5))),
                prerequisites=frozenset(concept_data.get("depends_on", [])),
                examples=tuple(
                    self._extract_examples(concept_data.get("examples", []))
                ),
                pedagogical_notes=concept_data.get("pedagogical_notes", ""),
            )

            # Store metadata using JSON ID as key
            self.metadata_cache[concept_data["id"]] = ConceptMetadata(
                domain=concept_data["domain"],
                subdomain=concept_data.get("subdomain"),
                level=concept_data["level"],
                difficulty=concept_data.get("difficulty", 5),
                tags=concept_data.get("tags", []),
                timestamp=datetime.fromisoformat(
                    concept_data["timestamp"].replace("Z", "+00:00")
                ),
                elastic_metadata=concept_data.get("elastic_metadata"),
            )

            return concept

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {file_path}: {e}")
            return None
        except Exception as e:
            print(f"Error loading concept from {file_path}: {e}")
            return None

    def _extract_examples(self, examples_data: List[Dict]) -> List[str]:
        """Extract example descriptions from the examples data."""
        return [
            ex.get("explanation", ex.get("description", "")) for ex in examples_data
        ]

    def _map_level_to_complexity(self, level: str) -> str:
        """Map educational level to complexity level."""
        mapping = {
            "elementary": "fundamental",
            "middle_school": "fundamental",
            "high_school": "basic",
            "undergraduate": "intermediate",
            "graduate": "advanced",
            "research": "advanced",
        }
        return mapping.get(level, "fundamental")

    def load_all_concepts(self) -> Dict[str, ConceptNode]:
        """
        Load all concepts from the JSON files in the hierarchy.

        Returns:
            Dictionary mapping concept IDs to ConceptNode instances
        """
        concept_files = self.discover_concept_files()

        print(f"Discovered {len(concept_files)} concept files")

        for file_path in concept_files:
            print(f"Loading concept from {file_path}")

            # Get JSON data to extract ID
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    concept_data = json.load(f)
                concept_json_id = concept_data.get("id")

                concept = self.load_concept_from_file(file_path)

                if concept and concept_json_id:
                    self.concepts_cache[concept_json_id] = concept
                    print(f"  ✓ Loaded concept: {concept.name} (ID: {concept_json_id})")
                else:
                    print(f"  ✗ Failed to load concept from {file_path}")
            except Exception as e:
                print(f"  ✗ Error processing {file_path}: {e}")

        print(f"Successfully loaded {len(self.concepts_cache)} concepts")
        return self.concepts_cache.copy()

    def get_concept_metadata(self, concept_id: str) -> Optional[ConceptMetadata]:
        """Get rich metadata for a concept."""
        return self.metadata_cache.get(concept_id)

    def get_concepts_by_domain(self, domain: str) -> List[ConceptNode]:
        """Get all concepts in a specific domain."""
        return [
            concept
            for concept_id, concept in self.concepts_cache.items()
            if self.metadata_cache.get(
                concept_id, ConceptMetadata("", "", "", 0, [], datetime.now(), None)
            ).domain
            == domain
        ]

    def get_concepts_by_level(self, level: str) -> List[ConceptNode]:
        """Get all concepts at a specific educational level."""
        return [
            concept
            for concept_id, concept in self.concepts_cache.items()
            if self.metadata_cache.get(
                concept_id, ConceptMetadata("", "", "", 0, [], datetime.now(), None)
            ).level
            == level
        ]

    def get_concepts_by_tag(self, tag: str) -> List[ConceptNode]:
        """Get all concepts with a specific tag."""
        return [
            concept
            for concept_id, concept in self.concepts_cache.items()
            if tag
            in self.metadata_cache.get(
                concept_id, ConceptMetadata("", "", "", 0, [], datetime.now(), None)
            ).tags
        ]

    def export_for_elastic_search(self) -> List[Dict]:
        """
        Export all concepts in a format optimized for elastic search ingestion.

        Returns:
            List of dictionaries ready for bulk indexing in elasticsearch
        """
        elastic_docs = []

        for concept_id, concept in self.concepts_cache.items():
            metadata = self.metadata_cache.get(concept_id)
            if not metadata:
                continue

            doc = {
                "_index": (
                    metadata.elastic_metadata.get("index_name", "mathematical_concepts")
                    if metadata.elastic_metadata
                    else "mathematical_concepts"
                ),
                "_type": (
                    metadata.elastic_metadata.get("doc_type", "_doc")
                    if metadata.elastic_metadata
                    else "_doc"
                ),
                "_id": concept_id,
                "_source": {
                    "id": concept.id,
                    "name": concept.name,
                    "description": concept.description,
                    "formal_definition": concept.formal_definition,
                    "domain": metadata.domain,
                    "subdomain": metadata.subdomain,
                    "level": metadata.level,
                    "difficulty": metadata.difficulty,
                    "tags": metadata.tags,
                    "dependencies": concept.dependencies,
                    "examples": concept.examples,
                    "timestamp": metadata.timestamp.isoformat(),
                    "search_text": f"{concept.name} {concept.description} {' '.join(metadata.tags)}",
                },
            }

            # Add boost if specified
            if metadata.elastic_metadata and "boost" in metadata.elastic_metadata:
                doc["_boost"] = metadata.elastic_metadata["boost"]

            elastic_docs.append(doc)

        return elastic_docs

    def create_d3_visualization_data(self) -> Dict:
        """
        Create data structure for D3.js force-directed graph visualization.

        Returns:
            Dictionary with 'nodes' and 'links' arrays for D3.js
        """
        nodes = []
        links = []

        # Create nodes
        for concept_id, concept in self.concepts_cache.items():
            metadata = self.metadata_cache.get(concept_id)

            node = {
                "id": concept_id,  # Use the JSON ID as the node ID
                "name": concept.name,
                "group": metadata.domain if metadata else "unknown",
                "level": metadata.level if metadata else "unknown",
                "difficulty": metadata.difficulty if metadata else 5,
                "size": min(10, len(concept.prerequisites) + len(concept.examples) + 1),
                "description": (
                    concept.description[:200] + "..."
                    if len(concept.description) > 200
                    else concept.description
                ),
            }

            nodes.append(node)

        # Create links based on dependencies
        for concept_id, concept in self.concepts_cache.items():
            for dependency in concept.prerequisites:
                if dependency in self.concepts_cache:
                    link = {
                        "source": dependency,
                        "target": concept_id,
                        "type": "depends_on",
                        "strength": 0.8,
                    }
                    links.append(link)

        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_concepts": len(nodes),
                "total_dependencies": len(links),
                "domains": list({node["group"] for node in nodes}),
                "levels": list({node["level"] for node in nodes}),
            },
        }

    def validate_concept_relationships(self) -> List[str]:
        """
        Validate that all concept relationships are consistent.

        Returns:
            List of validation error messages
        """
        errors = []

        for concept_id, concept in self.concepts_cache.items():
            # Check that all dependencies exist
            for dependency in concept.dependencies:
                if dependency not in self.concepts_cache:
                    errors.append(
                        f"Concept '{concept_id}' depends on missing concept '{dependency}'"
                    )

        return errors
