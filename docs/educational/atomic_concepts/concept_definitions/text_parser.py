"""
Text Parser for Concept Definition Files

Parses simple, human-readable text files containing mathematical and computer science
concept definitions with their dependencies. Designed for educational clarity while
maintaining computational precision.

File Format:
```
[concept_name]
type: axiom|concept|theorem|algorithm
dependencies: prerequisite1, prerequisite2
description: "Human readable description"
mathematical_definition: "Formal mathematical definition"
complexity: fundamental|basic|intermediate|advanced
subject_area: set_theory|logic|algorithms|etc
cognitive_load: 1-10
examples: "Example 1", "Example 2"
learning_objectives: "Objective 1", "Objective 2"
```

Educational Purpose:
Demonstrates parsing algorithms, text processing, and the conversion of human-readable
specifications into rigorous computational objects.
"""

import re
import configparser
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from io import StringIO

from ..dag.concept_node import ConceptNode
from ..dag.concept_dag import ConceptDAG
from ..dag.relationship_types import RelationshipType, DependencyStrength


class ConceptParseError(Exception):
    """Raised when concept definition file cannot be parsed correctly."""

    def __init__(
        self,
        message: str,
        line_number: Optional[int] = None,
        concept_name: Optional[str] = None,
    ):
        self.line_number = line_number
        self.concept_name = concept_name
        super().__init__(
            f"Parse error{f' at line {line_number}' if line_number else ''}"
            f"{f' in concept {concept_name}' if concept_name else ''}: {message}"
        )


class ConceptDefinitionParser:
    """
    Parser for educational concept definition files.

    Converts human-readable text specifications into rigorous ConceptNode objects
    with full mathematical and educational metadata.

    Mathematical Properties:
    - Validates concept name uniqueness
    - Ensures dependency references are resolvable
    - Maintains type safety for all fields

    Educational Features:
    - Intuitive syntax for educators
    - Rich error messages for debugging
    - Support for progressive complexity
    - Extensible metadata schema
    """

    def __init__(self):
        """Initialize parser with default configurations."""
        self.valid_types = {
            "axiom",
            "concept",
            "theorem",
            "algorithm",
            "definition",
            "property",
        }
        self.valid_complexities = {"fundamental", "basic", "intermediate", "advanced"}
        self.valid_subject_areas = {
            "set_theory",
            "logic",
            "number_theory",
            "algebra",
            "geometry",
            "calculus",
            "discrete_math",
            "algorithms",
            "data_structures",
            "complexity_theory",
            "programming",
            "software_engineering",
            "systems",
            "networks",
        }

    def parse_file(self, filepath: Path) -> List[ConceptNode]:
        """
        Parse concept definitions from a text file.

        Args:
            filepath: Path to concept definition file

        Returns:
            List of ConceptNode objects parsed from file

        Raises:
            ConceptParseError: If file format is invalid
            FileNotFoundError: If file doesn't exist
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Concept definition file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        return self.parse_content(content, str(filepath))

    def parse_content(
        self, content: str, source_name: str = "<string>"
    ) -> List[ConceptNode]:
        """
        Parse concept definitions from text content.

        Args:
            content: Text content containing concept definitions
            source_name: Name of source for error reporting

        Returns:
            List of parsed ConceptNode objects
        """
        # Preprocess content to handle our custom format
        processed_content = self._preprocess_content(content)

        # Use ConfigParser for robust parsing
        config = configparser.ConfigParser(
            interpolation=None,  # Disable variable interpolation
            allow_no_value=True,
            delimiters=(":",),
            comment_prefixes=("#",),
        )

        try:
            config.read_string(processed_content)
        except configparser.Error as e:
            raise ConceptParseError(
                f"Invalid file format: {e}", source_name=source_name
            )

        concepts = []
        for section_name in config.sections():
            try:
                concept = self._parse_concept_section(
                    section_name, config[section_name]
                )
                concepts.append(concept)
            except ConceptParseError as e:
                e.concept_name = section_name
                raise e
            except Exception as e:
                raise ConceptParseError(
                    f"Unexpected error parsing concept: {e}", concept_name=section_name
                )

        return concepts

    def _preprocess_content(self, content: str) -> str:
        """
        Preprocess content to handle our custom format with ConfigParser.

        Converts our human-readable format into ConfigParser-compatible format.
        """
        lines = content.split("\n")
        processed_lines = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                processed_lines.append(line)
                continue

            # Handle section headers [concept_name]
            if line.startswith("[") and line.endswith("]"):
                processed_lines.append(line)
                continue

            # Handle key-value pairs with special quote processing
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Remove surrounding quotes if present
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]

                processed_lines.append(f"{key}: {value}")
                continue

            # If we get here, line format is unexpected
            if line.strip():  # Only raise error for non-empty lines
                raise ConceptParseError(
                    f"Invalid line format: '{line}'", line_number=line_num
                )

        return "\n".join(processed_lines)

    def _parse_concept_section(
        self, concept_name: str, section: configparser.SectionProxy
    ) -> ConceptNode:
        """
        Parse a single concept section into a ConceptNode.

        Args:
            concept_name: Name of the concept (section header)
            section: ConfigParser section containing concept data

        Returns:
            ConceptNode object with parsed data
        """
        # Extract and validate required fields
        concept_type = section.get("type", "concept").lower()
        if concept_type not in self.valid_types:
            raise ConceptParseError(
                f"Invalid concept type '{concept_type}'. "
                f"Must be one of {self.valid_types}"
            )

        description = section.get("description", "")
        mathematical_definition = section.get("mathematical_definition", "")

        # Parse complexity level
        complexity = section.get("complexity", "basic").lower()
        if complexity not in self.valid_complexities:
            raise ConceptParseError(
                f"Invalid complexity level '{complexity}'. "
                f"Must be one of {self.valid_complexities}"
            )

        # Parse subject area
        subject_area = section.get("subject_area", "mathematics").lower()
        if subject_area not in self.valid_subject_areas:
            raise ConceptParseError(
                f"Invalid subject area '{subject_area}'. "
                f"Must be one of {self.valid_subject_areas}"
            )

        # Parse cognitive load
        try:
            cognitive_load = int(section.get("cognitive_load", "1"))
            if not 1 <= cognitive_load <= 10:
                raise ValueError("Cognitive load must be between 1 and 10")
        except ValueError as e:
            raise ConceptParseError(f"Invalid cognitive load: {e}")

        # Parse dependencies
        dependencies_str = section.get("dependencies", "").strip()
        if dependencies_str:
            prerequisites = set(
                dep.strip() for dep in dependencies_str.split(",") if dep.strip()
            )
        else:
            prerequisites = set()

        # Parse list fields (examples, learning objectives, etc.)
        examples = self._parse_list_field(section.get("examples", ""))
        learning_objectives = self._parse_list_field(
            section.get("learning_objectives", "")
        )
        assessment_criteria = self._parse_list_field(
            section.get("assessment_criteria", "")
        )
        misconceptions = self._parse_list_field(
            section.get("common_misconceptions", "")
        )

        # Parse pedagogical notes
        pedagogical_notes = section.get("pedagogical_notes", "")

        # Create dependency metadata with default relationship types
        dependency_metadata = {}
        for prereq in prerequisites:
            # Default to strong prerequisite relationship
            dependency_metadata[prereq] = (
                RelationshipType.PREREQUISITE,
                DependencyStrength.STRONG,
            )

        # Create and return ConceptNode
        return ConceptNode(
            name=concept_name,
            type=concept_type,
            description=description,
            mathematical_definition=mathematical_definition,
            subject_area=subject_area,
            complexity_level=complexity,
            cognitive_load=cognitive_load,
            prerequisites=frozenset(prerequisites),
            dependency_metadata=dependency_metadata,
            examples=tuple(examples),
            common_misconceptions=tuple(misconceptions),
            pedagogical_notes=pedagogical_notes,
            learning_objectives=tuple(learning_objectives),
            assessment_criteria=tuple(assessment_criteria),
        )

    def _parse_list_field(self, field_value: str) -> List[str]:
        """
        Parse comma-separated list field, handling quoted strings properly.

        Examples:
        - "item1, item2, item3" -> ["item1", "item2", "item3"]
        - '"quoted item", "another item"' -> ["quoted item", "another item"]
        """
        if not field_value.strip():
            return []

        # Simple case: no quotes
        if '"' not in field_value and "'" not in field_value:
            return [item.strip() for item in field_value.split(",") if item.strip()]

        # Complex case: handle quoted strings
        items = []
        current_item = ""
        in_quotes = False
        quote_char = None

        i = 0
        while i < len(field_value):
            char = field_value[i]

            if not in_quotes and char in ('"', "'"):
                in_quotes = True
                quote_char = char
            elif in_quotes and char == quote_char:
                in_quotes = False
                quote_char = None
            elif not in_quotes and char == ",":
                if current_item.strip():
                    items.append(current_item.strip())
                current_item = ""
                i += 1
                continue
            else:
                current_item += char

            i += 1

        # Add final item
        if current_item.strip():
            items.append(current_item.strip())

        return items

    def build_dag_from_concepts(self, concepts: List[ConceptNode]) -> ConceptDAG:
        """
        Build a ConceptDAG from a list of parsed concepts.

        Automatically resolves dependencies and validates the resulting graph.

        Args:
            concepts: List of ConceptNode objects

        Returns:
            ConceptDAG with all concepts and dependencies

        Raises:
            ConceptParseError: If dependencies cannot be resolved or cycles exist
        """
        dag = ConceptDAG()

        # First pass: Add all concepts
        for concept in concepts:
            dag.add_concept(concept)

        # Second pass: Add dependencies
        missing_dependencies = set()

        for concept in concepts:
            for prereq in concept.prerequisites:
                if prereq not in dag:
                    missing_dependencies.add(
                        f"'{prereq}' (required by '{concept.name}')"
                    )
                else:
                    try:
                        # Get relationship metadata if available
                        relationship_spec = concept.get_relationship_to(prereq)
                        if relationship_spec:
                            rel_type, strength = relationship_spec
                        else:
                            rel_type, strength = (
                                RelationshipType.PREREQUISITE,
                                DependencyStrength.STRONG,
                            )

                        dag.add_dependency(concept.name, prereq, rel_type, strength)
                    except Exception as e:
                        raise ConceptParseError(
                            f"Failed to add dependency {prereq} → {concept.name}: {e}"
                        )

        if missing_dependencies:
            raise ConceptParseError(
                f"Unresolved dependencies: {', '.join(sorted(missing_dependencies))}"
            )

        return dag

    def parse_file_to_dag(self, filepath: Path) -> ConceptDAG:
        """
        Convenience method to parse file directly into a DAG.

        Args:
            filepath: Path to concept definition file

        Returns:
            ConceptDAG with all concepts and dependencies
        """
        concepts = self.parse_file(filepath)
        return self.build_dag_from_concepts(concepts)
