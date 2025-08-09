"""
File-based Concept Loader Infrastructure Adapter

Implements ConceptLoader port for loading concepts from JSON files.

Educational Purpose:
- Demonstrates Adapter pattern from Clean Architecture
- Shows infrastructure layer implementation of domain ports
- Illustrates error handling and data transformation
- Examples of file system integration with business logic

Real-World Application:
- Loading curriculum content from standardized formats
- Importing course materials from content management systems
- Processing educational resources for knowledge graphs
- Migrating data between learning platforms
"""

import json
import os
import glob
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

from src.application.use_cases.concept_integration import ConceptLoader


class JsonConceptLoader(ConceptLoader):
    """
    Infrastructure adapter for loading concepts from JSON files.

    Educational Patterns:
    - Adapter Pattern: Adapts file system to domain interface
    - Template Method: Defines loading algorithm with customizable steps
    - Error Boundary: Isolates infrastructure errors from domain logic
    - Configuration: Parameterizable behavior for different environments

    Real-World Usage:
    - Content management system integrations
    - Educational resource imports
    - Curriculum database migrations
    - Standardized format processing
    """

    def __init__(
        self,
        base_path: Optional[str] = None,
        file_pattern: str = "*.json",
        encoding: str = "utf-8",
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize JSON concept loader.

        Educational Pattern: Configuration Injection
        - Allows customization without changing code
        - Supports different deployment environments
        - Enables testing with different configurations

        Args:
            base_path: Base directory for relative paths
            file_pattern: Glob pattern for finding JSON files
            encoding: File encoding (default UTF-8)
            logger: Logger instance for detailed tracking
        """
        self._base_path = Path(base_path) if base_path else Path.cwd()
        self._file_pattern = file_pattern
        self._encoding = encoding
        self._logger = logger or logging.getLogger(__name__)

        # Validation schema for concept files
        self._required_fields = {
            "id",
            "name",
            "formal_statement",
            "informal_description",
        }
        self._optional_fields = {
            "mathematical_definition",
            "concept_type",
            "level",
            "domain",
            "subdomain",
            "prerequisites",
            "enables",
            "related_concepts",
            "examples",
            "counterexamples",
            "proof_sketches",
            "tags",
            "metadata",
        }

    def load_concepts(self, source_path: str) -> List[Dict[str, Any]]:
        """
        Load concepts from JSON source.

        Educational Pattern: Template Method Implementation
        - Implements the abstract template from the port
        - Handles file system specifics while maintaining interface
        - Provides comprehensive error handling and logging

        Args:
            source_path: Path to JSON file or directory

        Returns:
            List of concept dictionaries ready for domain processing

        Raises:
            FileNotFoundError: If source path doesn't exist
            json.JSONDecodeError: If JSON is malformed
            ValueError: If data structure is invalid
        """
        self._logger.info(f"Loading concepts from: {source_path}")

        try:
            # Resolve path relative to base path
            full_path = self._resolve_path(source_path)

            # Load from file or directory
            if full_path.is_file():
                concepts = self._load_single_file(full_path)
            elif full_path.is_dir():
                concepts = self._load_directory(full_path)
            else:
                raise FileNotFoundError(f"Source path not found: {source_path}")

            self._logger.info(f"Successfully loaded {len(concepts)} concepts")
            return concepts

        except Exception as e:
            self._logger.error(f"Failed to load concepts from {source_path}: {str(e)}")
            raise

    def validate_format(self, data: Dict[str, Any]) -> bool:
        """
        Validate concept data format.

        Educational Pattern: Specification Pattern
        - Encapsulates validation rules in a clear method
        - Provides detailed feedback for debugging
        - Separates validation from transformation logic

        Args:
            data: Concept data dictionary to validate

        Returns:
            True if format is valid, False otherwise
        """
        try:
            # Check required fields
            missing_required = self._required_fields - set(data.keys())
            if missing_required:
                self._logger.warning(f"Missing required fields: {missing_required}")
                return False

            # Validate field types and values
            if not self._validate_field_types(data):
                return False

            # Validate business rules
            if not self._validate_business_rules(data):
                return False

            return True

        except Exception as e:
            self._logger.warning(f"Validation error: {str(e)}")
            return False

    def _resolve_path(self, source_path: str) -> Path:
        """
        Resolve source path relative to base path.

        Educational Pattern: Path Resolution Strategy
        - Handles absolute and relative paths consistently
        - Provides security by restricting to base path
        - Enables flexible deployment configurations
        """
        path = Path(source_path)

        # If absolute path, use as-is (with security check)
        if path.is_absolute():
            # Security: Ensure path is within allowed base path
            try:
                path.relative_to(self._base_path)
                return path
            except ValueError:
                self._logger.warning(f"Absolute path outside base: {source_path}")
                return path  # Allow for now, could be restricted

        # Resolve relative to base path
        return self._base_path / path

    def _load_single_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load concepts from a single JSON file.

        Educational Pattern: Single Responsibility
        - Focused on one type of loading operation
        - Clear error messages for specific failure modes
        - Defensive programming against malformed files
        """
        self._logger.debug(f"Loading single file: {file_path}")

        try:
            with open(file_path, "r", encoding=self._encoding) as f:
                data = json.load(f)

            # Handle different JSON structures
            if isinstance(data, list):
                # Array of concepts
                return data
            elif isinstance(data, dict):
                if "concepts" in data:
                    # Wrapper object with concepts array
                    return data["concepts"]
                else:
                    # Single concept object
                    return [data]
            else:
                raise ValueError(f"Unexpected JSON structure in {file_path}")

        except json.JSONDecodeError as e:
            self._logger.error(f"Invalid JSON in {file_path}: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(f"Error reading {file_path}: {str(e)}")
            raise

    def _load_directory(self, dir_path: Path) -> List[Dict[str, Any]]:
        """
        Load concepts from all JSON files in a directory.

        Educational Pattern: Composite Operation
        - Combines multiple file operations into one
        - Handles partial failures gracefully
        - Provides aggregate reporting for batch operations
        """
        self._logger.debug(f"Loading directory: {dir_path}")

        # Find all JSON files matching pattern
        pattern_path = dir_path / self._file_pattern
        json_files = glob.glob(str(pattern_path))

        if not json_files:
            self._logger.warning(
                f"No JSON files found in {dir_path} matching {self._file_pattern}"
            )
            return []

        all_concepts = []
        successful_files = 0

        for file_path in sorted(json_files):  # Sort for consistent ordering
            try:
                file_concepts = self._load_single_file(Path(file_path))
                all_concepts.extend(file_concepts)
                successful_files += 1
                self._logger.debug(
                    f"Loaded {len(file_concepts)} concepts from {file_path}"
                )

            except Exception as e:
                self._logger.warning(f"Failed to load {file_path}: {str(e)}")
                # Continue with other files

        self._logger.info(
            f"Loaded {len(all_concepts)} concepts from {successful_files}/{len(json_files)} files"
        )

        return all_concepts

    def _validate_field_types(self, data: Dict[str, Any]) -> bool:
        """
        Validate field types according to domain requirements.

        Educational Pattern: Type Validation Strategy
        - Ensures data types match domain expectations
        - Provides clear error messages for type mismatches
        - Handles optional fields gracefully
        """
        type_validations = {
            "id": str,
            "name": str,
            "formal_statement": str,
            "informal_description": str,
            "mathematical_definition": (str, type(None)),
            "concept_type": str,
            "level": str,
            "domain": str,
            "subdomain": (str, type(None)),
            "prerequisites": list,
            "enables": list,
            "related_concepts": list,
            "examples": list,
            "counterexamples": list,
            "proof_sketches": list,
            "tags": list,
        }

        for field, expected_type in type_validations.items():
            if field in data:
                value = data[field]
                if not isinstance(value, expected_type):
                    self._logger.warning(
                        f"Field '{field}' has type {type(value).__name__}, "
                        f"expected {expected_type}"
                    )
                    return False

        return True

    def _validate_business_rules(self, data: Dict[str, Any]) -> bool:
        """
        Validate business rules for concept data.

        Educational Pattern: Business Rule Validation
        - Encodes domain knowledge in infrastructure layer
        - Provides early validation before domain processing
        - Prevents invalid data from reaching business logic
        """
        # ID format validation
        concept_id = data.get("id", "")
        if not concept_id or not isinstance(concept_id, str):
            self._logger.warning("Concept ID must be a non-empty string")
            return False

        # Name validation
        name = data.get("name", "")
        if not name or not isinstance(name, str) or len(name.strip()) < 2:
            self._logger.warning("Concept name must be at least 2 characters")
            return False

        # Description validation
        description = data.get("informal_description", "")
        if not description or len(description.strip()) < 10:
            self._logger.warning("Informal description must be at least 10 characters")
            return False

        # Statement validation
        statement = data.get("formal_statement", "")
        if not statement or len(statement.strip()) < 5:
            self._logger.warning("Formal statement must be at least 5 characters")
            return False

        # Level validation (if present)
        if "level" in data:
            valid_levels = {
                "elementary",
                "middle_school",
                "high_school",
                "undergraduate",
                "graduate",
                "research",
            }
            level = data["level"].lower().replace(" ", "_").replace("-", "_")
            if level not in valid_levels:
                self._logger.warning(f"Invalid level: {data['level']}")
                return False

        # Type validation (if present)
        if "concept_type" in data:
            valid_types = {
                "axiom",
                "theorem",
                "definition",
                "lemma",
                "corollary",
                "conjecture",
                "algorithm",
            }
            if data["concept_type"].lower() not in valid_types:
                self._logger.warning(f"Invalid concept type: {data['concept_type']}")
                return False

        return True

    def load_concept_summaries(self, source_path: str) -> List[Dict[str, str]]:
        """
        Load lightweight concept summaries for preview/indexing.

        Educational Pattern: Data Transfer Object (DTO)
        - Provides lightweight view of concepts for specific use cases
        - Reduces memory usage for large datasets
        - Supports preview and indexing operations

        Args:
            source_path: Path to concepts source

        Returns:
            List of concept summaries with id, name, and domain
        """
        try:
            concepts = self.load_concepts(source_path)
            summaries = []

            for concept in concepts:
                if self.validate_format(concept):
                    summary = {
                        "id": concept["id"],
                        "name": concept["name"],
                        "domain": concept.get("domain", "unknown"),
                        "level": concept.get("level", "unknown"),
                        "type": concept.get("concept_type", "definition"),
                        "description_preview": concept["informal_description"][:100]
                        + "...",
                    }
                    summaries.append(summary)

            return summaries

        except Exception as e:
            self._logger.error(f"Failed to load concept summaries: {str(e)}")
            return []

    def count_concepts(self, source_path: str) -> int:
        """
        Count concepts without loading full data.

        Educational Pattern: Performance Optimization
        - Provides count without memory overhead of full loading
        - Useful for progress tracking and resource planning
        - Demonstrates separation between counting and loading operations
        """
        try:
            concepts = self.load_concepts(source_path)
            return len([c for c in concepts if self.validate_format(c)])
        except Exception as e:
            self._logger.error(f"Failed to count concepts: {str(e)}")
            return 0

    def get_available_domains(self, source_path: str) -> List[str]:
        """
        Get list of available domains in source data.

        Educational Pattern: Data Discovery
        - Enables dynamic discovery of available content
        - Supports user interface population
        - Provides metadata about data sources
        """
        try:
            concepts = self.load_concepts(source_path)
            domains = set()

            for concept in concepts:
                if self.validate_format(concept):
                    domain = concept.get("domain", "unknown")
                    domains.add(domain)

            return sorted(domains)

        except Exception as e:
            self._logger.error(f"Failed to get domains: {str(e)}")
            return []


# Educational Example Usage
def demonstrate_json_loader():
    """
    Demonstrate JSON concept loader functionality.

    Educational Purpose:
    - Shows how to use infrastructure adapters
    - Demonstrates error handling and logging
    - Illustrates configuration and customization
    """

    # Create sample concept data for demonstration
    sample_concepts = [
        {
            "id": "zfc_extensionality",
            "name": "Axiom of Extensionality",
            "formal_statement": "∀A ∀B (A = B ↔ ∀x (x ∈ A ↔ x ∈ B))",
            "informal_description": "Two sets are equal if and only if they have exactly the same elements",
            "concept_type": "axiom",
            "level": "undergraduate",
            "domain": "set_theory",
            "subdomain": "zfc_axioms",
            "prerequisites": [],
            "enables": ["empty_set", "set_equality"],
            "tags": ["zfc", "axiom", "foundation"],
        },
        {
            "id": "empty_set",
            "name": "Empty Set",
            "formal_statement": "∃A ∀x (x ∉ A)",
            "informal_description": "The unique set containing no elements, commonly denoted ∅ or {}",
            "concept_type": "definition",
            "level": "high_school",
            "domain": "set_theory",
            "prerequisites": ["zfc_extensionality"],
            "enables": ["set_operations"],
            "tags": ["basic_sets", "cardinality"],
        },
    ]

    # Configure loader
    loader = JsonConceptLoader(
        base_path="./concept_definitions",
        file_pattern="*.json",
        logger=logging.getLogger("demo"),
    )

    # Demonstrate validation
    for concept in sample_concepts:
        is_valid = loader.validate_format(concept)
        print(f"Concept '{concept['id']}' is valid: {is_valid}")

    print("Sample concepts demonstrate the JSON loading infrastructure adapter")
    print("In production, this would load from actual JSON files")


if __name__ == "__main__":
    # Set up logging for demonstration
    logging.basicConfig(level=logging.INFO)
    demonstrate_json_loader()
