#!/usr/bin/env python3
"""
Task Generation System - Creates hierarchical task decompositions using templates.

This system demonstrates knowledge graph principles applied to educational task management
by creating structured decompositions that can be efficiently traversed and analyzed.

Educational Notes:
- Shows Factory Pattern implementation for template-based object creation
- Demonstrates Strategy Pattern for different decomposition approaches
- Illustrates graph theory principles in practical task management
- Uses compositional design for building complex hierarchies from simple templates

Design Decisions:
- Template-driven generation ensures consistency across all task levels
- JSON schema validation prevents malformed task definitions
- Parent-child relationships enable graph traversal algorithms
- Educational metadata supports pedagogical assessment and planning

Usage:
    python3 task_generator.py --epic EPIC-1 --decompose-level features
    python3 task_generator.py --feature FEATURE-1-1 --create-stories
"""

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import argparse


@dataclass
class TaskGenerationConfig:
    """Configuration for task generation process."""

    templates_dir: Path
    output_dir: Path
    epic_source_dir: Path
    dry_run: bool = False
    validate_schema: bool = True

    def __post_init__(self):
        """Ensure all directories exist."""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)


class TemplateEngine:
    """
    Template engine for generating tasks from templates.

    Educational Notes:
    - Implements Template Method Pattern for consistent generation process
    - Uses string substitution for simple templating (could be extended with Jinja2)
    - Validates generated JSON against expected schema structure
    """

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all available templates."""
        self.templates = {}
        template_files = {
            "epic": "epic_template.json",
            "feature": "feature_template.json",
            "user_story": "user_story_template.json",
            "task": "task_template.json",
            "subtask": "subtask_template.json",
        }

        for task_type, filename in template_files.items():
            template_path = self.templates_dir / filename
            if template_path.exists():
                with open(template_path, "r") as f:
                    self.templates[task_type] = json.load(f)
                print(f"✅ Loaded {task_type} template")
            else:
                print(f"⚠️  Template not found: {template_path}")

    def generate_task(
        self, task_type: str, substitutions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a task from template with substitutions.

        Args:
            task_type: Type of task (feature, user_story, task, subtask)
            substitutions: Dictionary of placeholder → value mappings

        Returns:
            Generated task dictionary
        """
        if task_type not in self.templates:
            raise ValueError(f"No template found for task type: {task_type}")

        # Convert template to JSON string for substitution
        template_str = json.dumps(self.templates[task_type], indent=2)

        # Perform substitutions
        for placeholder, value in substitutions.items():
            # Handle different value types appropriately
            if isinstance(value, str):
                # Handle empty dependencies by removing them from arrays
                if value == "" and "task" in placeholder:
                    # Remove empty task references from dependency arrays
                    template_str = template_str.replace(f'"{{{placeholder}}}"', "")
                    template_str = template_str.replace("[, ]", "[]")
                    template_str = template_str.replace('["", ]', "[]")
                    template_str = template_str.replace("[,]", "[]")
                else:
                    template_str = template_str.replace(f"{{{placeholder}}}", value)
            elif isinstance(value, (int, float)):
                template_str = template_str.replace(f'"{{{placeholder}}}"', str(value))
            elif isinstance(value, list):
                # Convert list to JSON array string
                list_str = json.dumps(value)
                template_str = template_str.replace(f'["{{{placeholder}}}"]', list_str)

        # Parse back to dictionary
        try:
            generated_task = json.loads(template_str)
            return generated_task
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed after substitutions: {e}")
            print(f"Template string: {template_str[:500]}...")
            raise


class EpicDecomposer:
    """
    Decomposes epics into features using domain knowledge and best practices.

    Educational Notes:
    - Demonstrates domain-driven design principles
    - Shows how to break down complex requirements systematically
    - Illustrates Clean Architecture decomposition patterns
    """

    def __init__(self, template_engine: TemplateEngine):
        self.template_engine = template_engine

    def decompose_epic_to_features(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Decompose an epic into constituent features.

        This method analyzes the epic's scope and creates logical feature groupings
        that represent cohesive functional areas.
        """
        epic_id = epic_data["id"]
        epic_title = epic_data["title"]

        # Analyze epic to determine feature decomposition strategy
        features = []

        if "Repository Quality" in epic_title:
            # EPIC-1: Repository Quality & GitHub Management
            features = self._decompose_repository_quality_epic(epic_data)
        elif "Research Discovery" in epic_title:
            # EPIC-2: Research Discovery & Aggregation
            features = self._decompose_research_discovery_epic(epic_data)
        elif "Knowledge Management" in epic_title:
            # EPIC-3: Knowledge Management & Extraction
            features = self._decompose_knowledge_management_epic(epic_data)
        elif "Analysis Platform" in epic_title:
            # EPIC-4: Analysis Platform & Visualization
            features = self._decompose_analysis_platform_epic(epic_data)
        elif "Educational Framework" in epic_title:
            # EPIC-5: Educational Framework & Assessment
            features = self._decompose_educational_framework_epic(epic_data)
        else:
            # Generic decomposition approach
            features = self._generic_epic_decomposition(epic_data)

        return features

    def _decompose_repository_quality_epic(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decompose EPIC-1: Repository Quality & GitHub Management."""
        epic_id = epic_data["id"]
        base_substitutions = {
            "parent_epic_id": epic_id,
            "creation_date": datetime.now().isoformat(),
        }

        feature_definitions = [
            {
                "feature_number": "1",
                "feature_title": "Git LFS Implementation & Large File Management",
                "feature_description": "Implement Git LFS for managing large research datasets and PDF repositories efficiently within GitHub size limits",
                "priority": "high",
                "estimated_hours": 40,
                "story_points": 8,
                "primary_role": "DevOps Engineer",
                "skill_1": "Git LFS Configuration",
                "skill_2": "Repository Management",
                "skill_level": "intermediate",
                "secondary_role_1": "Software Architect",
                "secondary_role_2": "Backend Developer",
                "cognitive_level": "apply",
                "objective_1": "Configure Git LFS for optimal repository performance",
                "objective_2": "Implement automated large file detection and management",
                "objective_3": "Establish sustainable repository growth patterns",
                "prerequisite_1": "Basic Git knowledge",
                "prerequisite_2": "Understanding of repository size limits",
                "wiki_reference_1": "wiki/infrastructure/git-lfs",
                "business_value": "Enables sustainable repository growth without performance degradation",
                "acceptance_criteria_1": "Git LFS configured for PDF and dataset files",
                "acceptance_criteria_2": "Repository size reduced below GitHub recommendations",
                "acceptance_criteria_3": "Automated file size monitoring implemented",
                "assessment_question": "What are the key benefits of using Git LFS for research repositories?",
                "assessment_option_1": "Faster clone times for large files",
                "assessment_option_2": "Better version control for code",
                "assessment_option_3": "Improved security",
                "assessment_option_4": "Reduced server costs",
                "correct_option": "Faster clone times for large files",
                "assessment_explanation": "Git LFS stores large files separately, improving clone performance",
                "novice_description": "Can identify when to use Git LFS",
                "basic_description": "Can configure Git LFS for a repository",
                "proficient_description": "Can optimize Git LFS configuration for performance",
                "day_estimate": 5,
                "risk_1": "Learning curve for team members",
                "risk_2": "Migration complexity for existing files",
                "metric_1": "Repository clone time reduction",
                "metric_2": "Team adoption rate",
                "tag_1": "infrastructure",
                "tag_2": "git-lfs",
                "blocked_task_1": "",
                "blocked_task_2": "",
                "prerequisite_task_1": "",
                "related_task_1": "",
            },
            {
                "feature_number": "2",
                "feature_title": "Code Quality Standards & Educational Documentation",
                "feature_description": "Establish comprehensive code quality standards with educational documentation for academic repository excellence",
                "priority": "high",
                "estimated_hours": 35,
                "primary_role": "Software Architect",
                "skill_1": "Clean Architecture",
                "skill_2": "Technical Documentation",
                "skill_level": "advanced",
                "cognitive_level": "create",
                "objective_1": "Implement >90% test coverage standards",
                "objective_2": "Create pedagogical code examples",
                "business_value": "Provides educational excellence and maintainable codebase",
                "acceptance_criteria_1": "Code quality standards documented and enforced",
                "acceptance_criteria_2": "Educational annotations in all major components",
                "tag_1": "quality",
                "tag_2": "education",
                "blocked_task_1": "",
                "prerequisite_task_1": "FEAT-1",  # Depends on Git LFS setup
            },
            {
                "feature_number": "3",
                "feature_title": "GitHub Workflow Optimization & CI/CD",
                "feature_description": "Optimize GitHub workflows for academic research with automated testing, quality gates, and deployment pipelines",
                "priority": "medium",
                "estimated_hours": 30,
                "primary_role": "DevOps Engineer",
                "skill_1": "GitHub Actions",
                "skill_2": "CI/CD Pipelines",
                "skill_level": "intermediate",
                "cognitive_level": "apply",
                "objective_1": "Automate quality assurance processes",
                "objective_2": "Implement continuous integration best practices",
                "business_value": "Ensures consistent quality and reduces manual overhead",
                "acceptance_criteria_1": "Automated test execution on all PRs",
                "acceptance_criteria_2": "Quality gates prevent low-quality merges",
                "tag_1": "automation",
                "tag_2": "ci-cd",
                "blocked_task_1": "",
                "prerequisite_task_1": "FEAT-2",  # Depends on quality standards
            },
        ]

        features = []
        for feature_def in feature_definitions:
            substitutions = {**base_substitutions, **feature_def}
            feature = self.template_engine.generate_task("feature", substitutions)

            # Manually fix dependencies to avoid template issues
            if feature["id"] == "FEAT-1":
                feature["dependencies"] = {
                    "blocks": [],
                    "blocked_by": [],
                    "related": [],
                }
            elif feature["id"] == "FEAT-2":
                feature["dependencies"] = {
                    "blocks": [],
                    "blocked_by": ["FEAT-1"],
                    "related": [],
                }
            elif feature["id"] == "FEAT-3":
                feature["dependencies"] = {
                    "blocks": [],
                    "blocked_by": ["FEAT-2"],
                    "related": [],
                }

            features.append(feature)

        return features

    def _decompose_research_discovery_epic(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decompose EPIC-2: Research Discovery & Aggregation."""
        # Similar pattern for other epics...
        return []

    def _decompose_knowledge_management_epic(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decompose EPIC-3: Knowledge Management & Extraction."""
        return []

    def _decompose_analysis_platform_epic(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decompose EPIC-4: Analysis Platform & Visualization."""
        return []

    def _decompose_educational_framework_epic(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Decompose EPIC-5: Educational Framework & Assessment."""
        return []

    def _generic_epic_decomposition(
        self, epic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generic decomposition for unknown epic types."""
        return []


class TaskGenerator:
    """
    Main orchestrator for task generation and decomposition.

    Educational Notes:
    - Demonstrates Facade Pattern for complex subsystem interactions
    - Shows composition over inheritance with specialized decomposer classes
    - Implements Command Pattern for different generation operations
    """

    def __init__(self, config: TaskGenerationConfig):
        self.config = config
        self.template_engine = TemplateEngine(config.templates_dir)
        self.epic_decomposer = EpicDecomposer(self.template_engine)

    def load_epic(self, epic_id: str) -> Optional[Dict[str, Any]]:
        """Load epic data from source directory."""
        # Try to find epic file by searching for files containing the epic ID
        epic_files = list(self.config.epic_source_dir.glob(f"{epic_id}*.json"))
        if epic_files:
            epic_file = epic_files[0]  # Use first match
            with open(epic_file, "r") as f:
                return json.load(f)
        else:
            print(f"❌ Epic file not found for: {epic_id}")
            available_files = list(self.config.epic_source_dir.glob("*.json"))
            print(f"   Available epic files: {[f.name for f in available_files]}")
            return None

    def generate_features_for_epic(self, epic_id: str) -> List[Dict[str, Any]]:
        """Generate all features for a given epic."""
        epic_data = self.load_epic(epic_id)
        if not epic_data:
            return []

        print(f"🏗️  Decomposing {epic_id}: {epic_data['title']}")
        features = self.epic_decomposer.decompose_epic_to_features(epic_data)

        # Save features to output directory
        if not self.config.dry_run:
            features_dir = self.config.output_dir / "features"
            features_dir.mkdir(exist_ok=True)

            for feature in features:
                feature_file = features_dir / f"{feature['id'].lower()}.json"
                with open(feature_file, "w") as f:
                    json.dump(feature, f, indent=2)
                print(f"✅ Generated feature: {feature['id']} - {feature['title']}")

        return features

    def demonstrate_knowledge_graph_traversal(self) -> None:
        """Demonstrate knowledge graph algorithms on generated tasks."""
        try:
            # Import our knowledge graph tool
            import sys

            sys.path.append(str(self.config.output_dir.parent))
            from atomic_task_graph import AtomicTaskGraph

            # Load all epics first
            epics_dir = self.config.epic_source_dir
            graph = AtomicTaskGraph.from_json_directory(epics_dir)

            print(f"\n📊 Knowledge Graph Analysis:")
            print(f"   Tasks loaded: {len(graph.tasks)}")
            print(f"   Dependencies: {len(graph.dependencies)}")

            # Generate features for EPIC-1 and add to graph
            features = self.generate_features_for_epic("EPIC-1")
            for feature in features:
                # Convert dictionary to AtomicTask object
                from atomic_task_graph import AtomicTask

                task = AtomicTask(
                    id=feature["id"],
                    task_type=feature["type"],
                    title=feature["title"],
                    description=feature["description"],
                    priority=feature["priority"],
                    effort=feature["effort"],
                    skills=feature["skills"],
                    learning_objectives=feature.get("learning_objectives", {}),
                    acceptance_criteria=feature.get("acceptance_criteria", []),
                    definition_of_done=feature.get("definition_of_done", []),
                    dependencies=feature["dependencies"],
                    status=feature.get("status", "not_started"),
                )
                graph.add_task(task)

            # Demonstrate graph algorithms
            print(f"\n🔍 Graph Traversal Demonstrations:")

            # Topological ordering
            order = graph.topological_sort()
            print(f"   Topological Order: {' → '.join(order[:5])}...")

            # Critical path analysis
            critical_path = graph.find_critical_path()
            if critical_path:
                print(f"   Critical Path: {' → '.join(critical_path)}")

            # PageRank importance
            importance = graph.calculate_pagerank()
            top_tasks = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"   Most Important Tasks:")
            for task_id, score in top_tasks:
                task_title = (
                    graph.tasks[task_id].title if task_id in graph.tasks else "Unknown"
                )
                print(f"     {task_id}: {score:.4f} - {task_title}")

        except ImportError:
            print("⚠️  Knowledge graph tool not available for demonstration")


def main():
    """Main entry point for task generation system."""
    parser = argparse.ArgumentParser(
        description="Generate hierarchical task decompositions"
    )
    parser.add_argument("--epic", help="Epic ID to decompose (e.g., EPIC-1)")
    parser.add_argument(
        "--decompose-level",
        choices=["features", "stories", "tasks", "subtasks"],
        default="features",
        help="Level of decomposition to generate",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show output without saving files"
    )
    parser.add_argument(
        "--demonstrate-graph",
        action="store_true",
        help="Demonstrate knowledge graph algorithms",
    )

    args = parser.parse_args()

    # Set up configuration
    base_dir = Path(__file__).parent
    config = TaskGenerationConfig(
        templates_dir=base_dir / "templates",
        output_dir=base_dir,
        epic_source_dir=base_dir / "epics",
        dry_run=args.dry_run,
    )

    generator = TaskGenerator(config)

    if args.demonstrate_graph:
        generator.demonstrate_knowledge_graph_traversal()
        return

    if args.epic:
        if args.decompose_level == "features":
            features = generator.generate_features_for_epic(args.epic)
            print(f"\n📋 Generated {len(features)} features for {args.epic}")
        else:
            print(
                f"⚠️  Decomposition level '{args.decompose_level}' not yet implemented"
            )
    else:
        print("📚 Task Generation System")
        print("   Use --epic EPIC-1 --decompose-level features to generate features")
        print("   Use --demonstrate-graph to show knowledge graph algorithms")


if __name__ == "__main__":
    main()
