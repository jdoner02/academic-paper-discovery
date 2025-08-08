#!/usr/bin/env python3
"""
Implementable Task Generator - Creates concrete technical tasks from user stories.

This system demonstrates the fourth level of explosive recursive decomposition by taking user stories
and breaking them down into implementable tasks that developers can complete in single sessions.

Educational Notes:
- Shows how user stories decompose into technical implementation tasks
- Demonstrates task sizing for single-session completion (2-4 hours each)
- Implements technical specifications with clear deliverables
- Uses incremental development patterns for risk reduction
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Constants to avoid linting warnings
DEVOPS_ENGINEER = "DevOps Engineer"
SOFTWARE_ENGINEER = "Software Engineer"
GIT_LFS_TAG = "git-lfs"


def create_tasks_for_story_1_1():
    """
    Create implementable tasks for STORY-1-1: Configure Git LFS for Academic Paper Storage.

    This demonstrates how a user story breaks down into specific technical tasks that can
    be completed independently while building toward the story's acceptance criteria.
    """

    tasks = [
        {
            "id": "TASK-1-1-1",
            "type": "task",
            "title": "Install and Initialize Git LFS",
            "description": "Set up Git LFS on the repository and verify basic functionality",
            "priority": "high",
            "effort": {"hours": 2, "complexity": "task", "session_size": "single"},
            "technical_specs": {
                "implementation_approach": "Command-line Git LFS setup",
                "deliverables": [
                    "Git LFS installed on development machine",
                    "Repository initialized with `git lfs install`",
                    "Verification script showing LFS status",
                ],
                "acceptance_tests": [
                    "Command `git lfs version` returns valid version",
                    "Command `git lfs env` shows correct configuration",
                    "Repository .git/hooks contains LFS hooks",
                ],
            },
            "skills": {
                "primary_role": DEVOPS_ENGINEER,
                "required_skills": ["Git CLI", "Command Line Interface"],
                "skill_level": "beginner",
                "learning_outcomes": [
                    "Understand Git LFS installation process",
                    "Verify LFS repository initialization",
                ],
            },
            "implementation_notes": {
                "platform_considerations": [
                    "macOS: brew install git-lfs",
                    "Ubuntu: apt install git-lfs",
                    "Windows: Download from GitHub releases",
                ],
                "verification_commands": [
                    "git lfs version",
                    "git lfs env",
                    "git lfs track",
                ],
                "common_pitfalls": [
                    "Forgetting to run git lfs install in repository",
                    "Permission issues with git hooks directory",
                ],
            },
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {"blocks": ["TASK-1-1-2"], "blocked_by": [], "related": []},
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": [GIT_LFS_TAG, "setup", "installation"],
        },
        {
            "id": "TASK-1-1-2",
            "type": "task",
            "title": "Create .gitattributes for PDF Tracking",
            "description": "Configure Git LFS to track PDF files and other large academic content",
            "priority": "high",
            "effort": {"hours": 1, "complexity": "task", "session_size": "single"},
            "technical_specs": {
                "implementation_approach": "File pattern configuration in .gitattributes",
                "deliverables": [
                    ".gitattributes file with PDF tracking rules",
                    "Documentation of tracking patterns used",
                    "Validation that patterns work correctly",
                ],
                "acceptance_tests": [
                    "File .gitattributes exists in repository root",
                    "Contains line: *.pdf filter=lfs diff=lfs merge=lfs -text",
                    "Command `git lfs track` shows PDF files tracked",
                ],
            },
            "skills": {
                "primary_role": DEVOPS_ENGINEER,
                "required_skills": ["Git Attributes", "File Pattern Matching"],
                "skill_level": "beginner",
                "learning_outcomes": [
                    "Understand .gitattributes file format",
                    "Configure LFS tracking patterns",
                ],
            },
            "implementation_notes": {
                "file_patterns": [
                    "*.pdf filter=lfs diff=lfs merge=lfs -text",
                    "*.zip filter=lfs diff=lfs merge=lfs -text",
                    "*.tar.gz filter=lfs diff=lfs merge=lfs -text",
                ],
                "best_practices": [
                    "Place .gitattributes in repository root",
                    "Test patterns with sample files before committing",
                    "Document why each pattern is tracked",
                ],
                "verification_steps": [
                    "Add test PDF file",
                    "Check `git lfs ls-files` output",
                    "Verify file shows as LFS pointer in Git",
                ],
            },
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {
                "blocks": ["TASK-1-1-3"],
                "blocked_by": ["TASK-1-1-1"],
                "related": [],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": [GIT_LFS_TAG, "configuration", "file-patterns"],
        },
        {
            "id": "TASK-1-1-3",
            "type": "task",
            "title": "Migrate Existing PDF Files to LFS",
            "description": "Convert existing PDF files in the repository to use Git LFS storage",
            "priority": "medium",
            "effort": {"hours": 3, "complexity": "task", "session_size": "single"},
            "technical_specs": {
                "implementation_approach": "Git LFS migration with history preservation",
                "deliverables": [
                    "All existing PDF files migrated to LFS",
                    "Git history cleaned of large file content",
                    "Migration verification report",
                ],
                "acceptance_tests": [
                    "Command `git lfs ls-files` shows all PDF files",
                    "Repository size significantly reduced",
                    "All PDF files still accessible and functional",
                ],
            },
            "skills": {
                "primary_role": DEVOPS_ENGINEER,
                "required_skills": ["Git LFS Migration", "Repository Maintenance"],
                "skill_level": "intermediate",
                "learning_outcomes": [
                    "Perform safe LFS migration of existing files",
                    "Understand Git history rewriting implications",
                ],
            },
            "implementation_notes": {
                "migration_commands": [
                    'git lfs migrate import --include="*.pdf"',
                    'git lfs migrate info --include="*.pdf"',
                    "git push --force-with-lease origin main",
                ],
                "safety_precautions": [
                    "Create repository backup before migration",
                    "Coordinate with team before force-push",
                    "Test migration on feature branch first",
                ],
                "verification_methods": [
                    "Compare repository sizes before/after",
                    "Verify all PDFs open correctly",
                    "Check LFS storage usage in GitHub",
                ],
            },
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {
                "blocks": ["TASK-1-1-4"],
                "blocked_by": ["TASK-1-1-2"],
                "related": [],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": [GIT_LFS_TAG, "migration", "repository-maintenance"],
        },
        {
            "id": "TASK-1-1-4",
            "type": "task",
            "title": "Document LFS Workflow and Train Team",
            "description": "Create documentation and training materials for Git LFS usage in academic workflows",
            "priority": "medium",
            "effort": {"hours": 2, "complexity": "task", "session_size": "single"},
            "technical_specs": {
                "implementation_approach": "Documentation creation with practical examples",
                "deliverables": [
                    "LFS workflow documentation in wiki",
                    "Quick reference card for common commands",
                    "Troubleshooting guide for common issues",
                ],
                "acceptance_tests": [
                    "Documentation exists in docs/wiki/infrastructure/",
                    "Contains practical examples with academic content",
                    "Team members can follow workflow independently",
                ],
            },
            "skills": {
                "primary_role": "Technical Writer",
                "required_skills": ["Technical Documentation", "Process Design"],
                "skill_level": "intermediate",
                "learning_outcomes": [
                    "Create effective technical documentation",
                    "Design user-friendly workflows",
                ],
            },
            "implementation_notes": {
                "documentation_sections": [
                    "Quick Start Guide",
                    "Daily Workflow Commands",
                    "Troubleshooting Common Issues",
                    "Best Practices for Academic Repositories",
                ],
                "example_workflows": [
                    "Adding new academic papers",
                    "Cloning repository for new team members",
                    "Handling LFS storage quota issues",
                ],
                "training_materials": [
                    "Command cheat sheet",
                    "Video walkthrough (optional)",
                    "FAQ based on common questions",
                ],
            },
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {"blocks": [], "blocked_by": ["TASK-1-1-3"], "related": []},
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["documentation", "training", "workflow"],
        },
    ]

    return tasks


def save_tasks(tasks: List[Dict[str, Any]], output_dir: Path):
    """Save tasks to individual JSON files."""
    output_dir.mkdir(exist_ok=True)

    for task in tasks:
        task_file = output_dir / f"{task['id'].lower()}.json"
        with open(task_file, "w") as f:
            json.dump(task, f, indent=2)
        print(f"✅ Created task: {task['id']} - {task['title']}")


def main():
    """Generate tasks for STORY-1-1 and demonstrate technical decomposition."""

    print("🔧 Task Generation System")
    print("   Creating implementable tasks for STORY-1-1: Configure Git LFS")
    print()

    # Generate tasks for STORY-1-1
    tasks = create_tasks_for_story_1_1()

    # Save to files
    output_dir = Path("tasks")
    save_tasks(tasks, output_dir)

    print()
    print(f"⚙️  Generated {len(tasks)} tasks for STORY-1-1")
    print("   Tasks demonstrate technical implementation breakdown:")

    total_hours = 0
    for task in tasks:
        hours = task["effort"]["hours"]
        total_hours += hours
        print(f"   • {task['id']}: {task['title']}")
        print(
            f"     Duration: {hours} hours ({task['effort']['session_size']} session)"
        )
        print(
            f"     Role: {task['skills']['primary_role']} ({task['skills']['skill_level']})"
        )
        print()

    print(f"📊 Story Implementation Summary:")
    print(f"   • Total effort: {total_hours} hours")
    print(f"   • Original estimate: 8 hours")
    print(
        f"   • Task breakdown accuracy: {'✅ Good' if total_hours == 8 else '⚠️  Needs adjustment'}"
    )
    print()

    # Show dependency chain
    print("🔗 Implementation Sequence:")
    print("   STORY-1-1 → TASK-1-1-1 → TASK-1-1-2 → TASK-1-1-3 → TASK-1-1-4")
    print()

    # Educational insights
    print("📚 Educational Insights:")
    print("   • Tasks sized for single development sessions (1-3 hours each)")
    print("   • Each task has clear technical specifications and deliverables")
    print("   • Implementation notes provide practical guidance and pitfall warnings")
    print("   • Acceptance tests enable verification before marking complete")
    print("   • Dependencies ensure logical implementation progression")
    print("   • Skills progression from beginner to intermediate within story")
    print()

    print("🎓 Next Steps:")
    print("   • Generate subtasks for complex tasks (TASK-1-1-3 migration)")
    print("   • Create similar task breakdowns for STORY-1-2 and STORY-1-3")
    print("   • Demonstrate complete 5-level hierarchy")
    print("   • Update knowledge graph with all relationships")


if __name__ == "__main__":
    main()
