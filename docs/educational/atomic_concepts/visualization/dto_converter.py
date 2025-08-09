"""
D3.js Visualization Data Transfer Objects (DTOs)

Converts ConceptDAG data structures into JSON format optimized for D3.js force-directed
graph visualizations. Creates beautiful, interactive concept maps for educational purposes.

Mathematical Foundation:
- Graph G = (V, E) converted to JSON with nodes and links arrays
- Node positioning uses force simulation physics
- Edge weights map to visual properties (thickness, color, etc.)
- Hierarchical clustering by subject area and complexity

Educational Purpose:
- Interactive exploration of concept dependencies
- Visual learning paths from axioms to advanced topics
- Adaptive highlighting based on prerequisite mastery
- Beautiful presentation encouraging mathematical exploration

D3.js Integration:
Outputs JSON format directly consumable by D3.js force-directed layouts
with rich metadata for interactive features and educational enhancements.
"""

import json
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from ..dag.concept_dag import ConceptDAG
from ..dag.concept_node import ConceptNode
from ..dag.relationship_types import RelationshipType, DependencyStrength


class VisualizationTheme(Enum):
    """Color themes for concept visualization."""

    MATHEMATICAL = "mathematical"
    EDUCATIONAL = "educational"
    TECHNICAL = "technical"
    COLORBLIND_FRIENDLY = "colorblind_friendly"


@dataclass
class VisualizationConfig:
    """Configuration for D3.js visualization export."""

    theme: VisualizationTheme = VisualizationTheme.EDUCATIONAL
    include_descriptions: bool = True
    include_definitions: bool = True
    max_description_length: int = 200
    group_by_subject: bool = True
    show_complexity_levels: bool = True
    highlight_learning_paths: bool = True
    physics_enabled: bool = True

    # Visual properties
    node_size_range: Tuple[int, int] = (20, 60)
    link_thickness_range: Tuple[int, int] = (1, 8)
    charge_strength: int = -300
    link_distance: int = 100


class ConceptGraphDTO:
    """
    Data Transfer Object for converting ConceptDAG to D3.js format.

    Transforms mathematical DAG structure into interactive visualization format
    with rich metadata, color coding, and educational enhancements.

    Mathematical Properties:
    - Preserves graph topology (nodes and edges)
    - Maps dependency strength to visual weights
    - Maintains transitive closure information
    - Provides hierarchical grouping data

    Visualization Features:
    - Subject area color coding
    - Complexity level sizing
    - Interactive tooltips with definitions
    - Learning path highlighting
    - Physics simulation parameters
    """

    def __init__(
        self, dag: ConceptDAG, config: VisualizationConfig = VisualizationConfig()
    ):
        """
        Initialize DTO with DAG and visualization configuration.

        Args:
            dag: ConceptDAG to convert
            config: Visualization configuration settings
        """
        self.dag = dag
        self.config = config
        self._color_schemes = self._initialize_color_schemes()

    def _initialize_color_schemes(self) -> Dict[VisualizationTheme, Dict[str, str]]:
        """Initialize color schemes for different visualization themes."""
        return {
            VisualizationTheme.MATHEMATICAL: {
                "set_theory": "#1f77b4",  # Blue
                "logic": "#ff7f0e",  # Orange
                "number_theory": "#2ca02c",  # Green
                "algebra": "#d62728",  # Red
                "geometry": "#9467bd",  # Purple
                "calculus": "#8c564b",  # Brown
                "discrete_math": "#e377c2",  # Pink
                "algorithms": "#7f7f7f",  # Gray
                "data_structures": "#bcbd22",  # Olive
                "complexity_theory": "#17becf",  # Cyan
                "programming": "#aec7e8",  # Light blue
                "default": "#1f77b4",
            },
            VisualizationTheme.EDUCATIONAL: {
                "set_theory": "#4e79a7",
                "logic": "#f28e2c",
                "number_theory": "#e15759",
                "algebra": "#76b7b2",
                "geometry": "#59a14f",
                "calculus": "#edc949",
                "discrete_math": "#af7aa1",
                "algorithms": "#ff9d9a",
                "data_structures": "#9c755f",
                "complexity_theory": "#bab0ab",
                "programming": "#1f77b4",
                "default": "#4e79a7",
            },
            VisualizationTheme.COLORBLIND_FRIENDLY: {
                "set_theory": "#0173b2",
                "logic": "#de8f05",
                "number_theory": "#cc78bc",
                "algebra": "#ca9161",
                "geometry": "#fbafe4",
                "calculus": "#949494",
                "discrete_math": "#ece133",
                "algorithms": "#56b4e9",
                "data_structures": "#029e73",
                "complexity_theory": "#d55e00",
                "programming": "#0173b2",
                "default": "#0173b2",
            },
        }

    def to_d3_format(self) -> Dict[str, Any]:
        """
        Convert DAG to D3.js-compatible JSON format.

        Returns:
            Dictionary with 'nodes' and 'links' arrays plus metadata
        """
        nodes = self._create_nodes()
        links = self._create_links()
        groups = self._create_groups() if self.config.group_by_subject else []

        return {
            "nodes": nodes,
            "links": links,
            "groups": groups,
            "metadata": self._create_metadata(),
            "config": self._create_config_object(),
        }

    def _create_nodes(self) -> List[Dict[str, Any]]:
        """Create D3.js node objects from DAG concepts."""
        nodes = []
        color_scheme = self._color_schemes.get(
            self.config.theme, self._color_schemes[VisualizationTheme.EDUCATIONAL]
        )

        for concept in self.dag.concepts:
            # Calculate node size based on complexity and connections
            base_size = self._calculate_node_size(concept)

            # Get color based on subject area
            color = color_scheme.get(concept.subject_area, color_scheme["default"])

            # Prepare description and definition
            description = self._truncate_text(
                concept.description, self.config.max_description_length
            )
            definition = (
                concept.mathematical_definition
                if self.config.include_definitions
                else ""
            )

            node = {
                "id": concept.name,
                "name": concept.name,
                "type": concept.type,
                "description": description if self.config.include_descriptions else "",
                "mathematical_definition": definition,
                "subject_area": concept.subject_area,
                "complexity_level": concept.complexity_level,
                "cognitive_load": concept.cognitive_load,
                "size": base_size,
                "color": color,
                "is_axiom": concept.is_axiom,
                "dependency_count": concept.dependency_count,
                "examples": list(concept.examples)[:3],  # Limit for visualization
                "learning_objectives": list(concept.learning_objectives)[:3],
                # Visualization-specific properties
                "group": concept.subject_area,
                "level": self._complexity_to_level(concept.complexity_level),
                "importance": self._calculate_importance(concept),
                # Interactive properties
                "tooltip": self._create_tooltip_content(concept),
                "searchable": f"{concept.name} {concept.description} {concept.subject_area}".lower(),
            }

            nodes.append(node)

        return nodes

    def _create_links(self) -> List[Dict[str, Any]]:
        """Create D3.js link objects from DAG dependencies."""
        links = []

        for concept in self.dag.concepts:
            for prereq in concept.prerequisites:
                # Get relationship metadata
                relationship_spec = concept.get_relationship_to(prereq)
                if relationship_spec:
                    rel_type, strength = relationship_spec
                else:
                    rel_type, strength = (
                        RelationshipType.PREREQUISITE,
                        DependencyStrength.STRONG,
                    )

                # Calculate visual properties
                thickness = self._calculate_link_thickness(strength)
                opacity = float(strength)
                color = self._get_link_color(rel_type)

                link = {
                    "source": prereq,
                    "target": concept.name,
                    "relationship_type": str(rel_type),
                    "strength": float(strength),
                    "thickness": thickness,
                    "opacity": opacity,
                    "color": color,
                    "distance": self.config.link_distance,
                    # Interactive properties
                    "tooltip": f"{prereq} → {concept.name} ({rel_type.value})",
                }

                links.append(link)

        return links

    def _create_groups(self) -> List[Dict[str, Any]]:
        """Create subject area groups for hierarchical layout."""
        subject_groups = {}

        for concept in self.dag.concepts:
            subject = concept.subject_area
            if subject not in subject_groups:
                color_scheme = self._color_schemes.get(
                    self.config.theme,
                    self._color_schemes[VisualizationTheme.EDUCATIONAL],
                )
                subject_groups[subject] = {
                    "id": subject,
                    "name": subject.replace("_", " ").title(),
                    "color": color_scheme.get(subject, color_scheme["default"]),
                    "concepts": [],
                    "concept_count": 0,
                }

            subject_groups[subject]["concepts"].append(concept.name)
            subject_groups[subject]["concept_count"] += 1

        return list(subject_groups.values())

    def _create_metadata(self) -> Dict[str, Any]:
        """Create metadata object for visualization."""
        return {
            "total_concepts": self.dag.node_count,
            "total_dependencies": self.dag.edge_count,
            "graph_density": round(self.dag.density, 3),
            "complexity_levels": self._get_complexity_distribution(),
            "subject_areas": self._get_subject_distribution(),
            "axiom_count": len(self.dag.get_axioms()),
            "max_depth": self._calculate_max_depth(),
            "generated_timestamp": self._get_timestamp(),
        }

    def _create_config_object(self) -> Dict[str, Any]:
        """Create configuration object for D3.js simulation."""
        return {
            "physics": {
                "enabled": self.config.physics_enabled,
                "charge_strength": self.config.charge_strength,
                "link_distance": self.config.link_distance,
                "collision_radius": max(self.config.node_size_range) + 5,
            },
            "visual": {
                "theme": self.config.theme.value,
                "node_size_range": self.config.node_size_range,
                "link_thickness_range": self.config.link_thickness_range,
                "show_complexity_levels": self.config.show_complexity_levels,
                "highlight_learning_paths": self.config.highlight_learning_paths,
            },
            "interaction": {
                "include_descriptions": self.config.include_descriptions,
                "include_definitions": self.config.include_definitions,
                "max_description_length": self.config.max_description_length,
            },
        }

    def _calculate_node_size(self, concept: ConceptNode) -> int:
        """Calculate node size based on importance and connections."""
        base_size = self.config.node_size_range[0]
        max_size = self.config.node_size_range[1]

        # Factors affecting size
        dependency_factor = min(
            concept.dependency_count / 5.0, 1.0
        )  # Normalize to max 5 deps
        complexity_factor = self._complexity_to_numeric(concept.complexity_level) / 4.0
        axiom_bonus = 0.3 if concept.is_axiom else 0.0

        # Weighted average
        size_factor = (
            dependency_factor * 0.4 + complexity_factor * 0.4 + axiom_bonus * 0.2
        )

        return int(base_size + (max_size - base_size) * size_factor)

    def _calculate_link_thickness(self, strength: DependencyStrength) -> int:
        """Calculate link thickness based on dependency strength."""
        min_thickness, max_thickness = self.config.link_thickness_range
        strength_ratio = float(strength)
        return int(min_thickness + (max_thickness - min_thickness) * strength_ratio)

    def _get_link_color(self, relationship_type: RelationshipType) -> str:
        """Get color for link based on relationship type."""
        color_map = {
            RelationshipType.PREREQUISITE: "#666666",
            RelationshipType.FOUNDATION: "#333333",
            RelationshipType.SPECIALIZATION: "#1f77b4",
            RelationshipType.APPLICATION: "#ff7f0e",
            RelationshipType.EXTENSION: "#2ca02c",
            RelationshipType.ANALOGY: "#d62728",
            RelationshipType.MOTIVATION: "#9467bd",
        }
        return color_map.get(relationship_type, "#666666")

    def _calculate_importance(self, concept: ConceptNode) -> float:
        """Calculate concept importance for visualization weighting."""
        # Concepts with many dependents are more important
        dependent_count = len(self.dag.get_dependents(concept.name))

        # Axioms are foundational
        axiom_bonus = 0.5 if concept.is_axiom else 0.0

        # Complexity adds importance
        complexity_factor = self._complexity_to_numeric(concept.complexity_level) / 4.0

        return min(dependent_count / 10.0 + axiom_bonus + complexity_factor, 1.0)

    def _complexity_to_level(self, complexity: str) -> int:
        """Convert complexity string to numeric level."""
        mapping = {"fundamental": 0, "basic": 1, "intermediate": 2, "advanced": 3}
        return mapping.get(complexity, 1)

    def _complexity_to_numeric(self, complexity: str) -> int:
        """Convert complexity to numeric value for calculations."""
        mapping = {"fundamental": 1, "basic": 2, "intermediate": 3, "advanced": 4}
        return mapping.get(complexity, 2)

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to maximum length with ellipsis."""
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    def _create_tooltip_content(self, concept: ConceptNode) -> str:
        """Create rich tooltip content for concept."""
        parts = [f"<strong>{concept.name}</strong>"]

        if concept.description:
            parts.append(f"<em>{concept.description}</em>")

        parts.append(f"Type: {concept.type.title()}")
        parts.append(f"Complexity: {concept.complexity_level.title()}")
        parts.append(f"Subject: {concept.subject_area.replace('_', ' ').title()}")

        if concept.prerequisites:
            prereq_list = ", ".join(sorted(concept.prerequisites))
            parts.append(f"Prerequisites: {prereq_list}")

        if concept.mathematical_definition:
            definition = self._truncate_text(concept.mathematical_definition, 150)
            parts.append(f"Definition: {definition}")

        return "<br>".join(parts)

    def _get_complexity_distribution(self) -> Dict[str, int]:
        """Get distribution of concepts by complexity level."""
        distribution = {"fundamental": 0, "basic": 0, "intermediate": 0, "advanced": 0}
        for concept in self.dag.concepts:
            distribution[concept.complexity_level] += 1
        return distribution

    def _get_subject_distribution(self) -> Dict[str, int]:
        """Get distribution of concepts by subject area."""
        distribution = {}
        for concept in self.dag.concepts:
            subject = concept.subject_area
            distribution[subject] = distribution.get(subject, 0) + 1
        return distribution

    def _calculate_max_depth(self) -> int:
        """Calculate maximum depth of dependency chain."""
        max_depth = 0
        for concept in self.dag.concepts:
            depth = len(self.dag.get_prerequisites(concept.name, transitive=True))
            max_depth = max(max_depth, depth)
        return max_depth

    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        from datetime import datetime

        return datetime.now().isoformat()

    def export_to_json(self, filepath: Path) -> None:
        """Export visualization data to JSON file."""
        data = self.to_d3_format()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def create_learning_path_visualization(self, target_concept: str) -> Dict[str, Any]:
        """
        Create visualization data focused on learning path to target concept.

        Highlights the prerequisite chain and dims unrelated concepts.
        """
        learning_path = self.dag.get_learning_path(target_concept)
        path_concepts = set(learning_path)

        # Create modified visualization with path highlighting
        data = self.to_d3_format()

        # Modify nodes to highlight path
        for node in data["nodes"]:
            if node["id"] in path_concepts:
                node["in_learning_path"] = True
                node["opacity"] = 1.0
                node["size"] = int(node["size"] * 1.2)  # Make path nodes larger
            else:
                node["in_learning_path"] = False
                node["opacity"] = 0.3

        # Modify links to highlight path dependencies
        for link in data["links"]:
            if link["source"] in path_concepts and link["target"] in path_concepts:
                link["in_learning_path"] = True
                link["opacity"] = 1.0
                link["thickness"] = int(link["thickness"] * 1.5)
            else:
                link["in_learning_path"] = False
                link["opacity"] = 0.2

        # Add path metadata
        data["learning_path"] = {
            "target_concept": target_concept,
            "path_length": len(learning_path),
            "concepts": learning_path,
            "total_cognitive_load": sum(
                self.dag[concept].cognitive_load for concept in learning_path
            ),
        }

        return data
