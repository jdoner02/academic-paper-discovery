#!/usr/bin/env python3
"""
User Story Generator - Creates user stories from features following educational best practices.

This system demonstrates the explosive recursive decomposition pattern by taking features
and breaking them down into concrete user stories with acceptance criteria, educational
objectives, and assessment components.

Educational Notes:
- Shows how large features decompose into user-focused requirements
- Demonstrates user story format: "As a [role], I want [goal] so that [benefit]"
- Implements educational metadata for competency-based learning
- Uses domain-driven design for academic software engineering education
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def create_user_stories_for_feat1():
    """
    Create comprehensive user stories for FEAT-1: Git LFS Implementation & Large File Management.

    This demonstrates how to decompose a complex infrastructure feature into user-focused stories
    that can be implemented incrementally while maintaining educational value.
    """

    stories = [
        {
            "id": "STORY-1-1",
            "type": "user_story",
            "title": "Configure Git LFS for Academic Paper Storage",
            "description": "As a DevOps engineer, I want to configure Git LFS for PDF files so that academic papers can be stored efficiently without exceeding repository size limits",
            "priority": "high",
            "effort": {"hours": 8, "story_points": 5, "complexity": "user_story"},
            "skills": {
                "primary_role": "DevOps Engineer",
                "required_skills": ["Git LFS Configuration", "Repository Management"],
                "skill_level": "intermediate",
                "secondary_roles": ["Software Engineer"],
            },
            "learning_objectives": {
                "cognitive_level": "apply",
                "objectives": [
                    "Configure Git LFS tracking rules for academic content",
                    "Understand Git LFS workflow and commands",
                ],
                "prerequisites": [
                    "Basic Git knowledge",
                    "Understanding of file size limitations",
                ],
                "wiki_references": [
                    "wiki/infrastructure/git-lfs-configuration",
                    "wiki/academic-repositories/large-file-management",
                ],
            },
            "acceptance_criteria": [
                {
                    "criterion": "Given a repository with PDF files, when Git LFS is configured, then .gitattributes properly tracks *.pdf files",
                    "testable": True,
                    "test_method": "File inspection and git lfs track verification",
                },
                {
                    "criterion": "Given LFS configuration, when pushing large files, then files are stored in LFS rather than Git history",
                    "testable": True,
                    "test_method": "Repository size comparison before/after",
                },
                {
                    "criterion": "Given LFS setup, when cloning repository, then large files download on demand",
                    "testable": True,
                    "test_method": "Clone time and bandwidth measurement",
                },
            ],
            "definition_of_done": [
                "Git LFS installed and initialized",
                ".gitattributes file created with PDF tracking rules",
                "Existing PDF files migrated to LFS storage",
                "Documentation updated with LFS workflow",
                "Team trained on LFS commands and best practices",
            ],
            "dependencies": {"blocks": ["STORY-1-2"], "blocked_by": [], "related": []},
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "assessment": {
                "unit_test_question": {
                    "question": "What is the primary benefit of using Git LFS for academic repositories with large PDF collections?",
                    "type": "multiple_choice",
                    "options": [
                        "Faster clone times by storing large files separately",
                        "Better file compression for PDF documents",
                        "Enhanced security for sensitive research data",
                        "Automatic PDF text extraction capabilities",
                    ],
                    "correct_answer": "Faster clone times by storing large files separately",
                    "explanation": "Git LFS stores large files in separate storage while keeping lightweight pointers in Git history, dramatically improving clone and fetch performance for repositories with large binary files.",
                }
            },
            "competency_indicators": [
                {
                    "level": "novice",
                    "description": "Can identify when Git LFS is needed and follow setup instructions",
                },
                {
                    "level": "basic",
                    "description": "Can configure Git LFS for a repository and migrate existing files",
                },
                {
                    "level": "proficient",
                    "description": "Can optimize LFS configuration for team workflows and troubleshoot common issues",
                },
            ],
            "sprint_planning": {
                "estimated_days": 1.5,
                "ideal_assignee_level": "intermediate",
                "risk_factors": [
                    "Learning curve for team members unfamiliar with LFS",
                    "Large file migration may take significant time",
                ],
                "success_metrics": [
                    "Repository clone time reduced by >80%",
                    "Zero push failures due to file size limits",
                ],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["infrastructure", "git-lfs", "setup"],
        },
        {
            "id": "STORY-1-2",
            "type": "user_story",
            "title": "Automate Large File Detection and Management",
            "description": "As a repository maintainer, I want automated detection of large files so that new contributors cannot accidentally commit large files that should use LFS",
            "priority": "medium",
            "effort": {"hours": 12, "story_points": 8, "complexity": "user_story"},
            "skills": {
                "primary_role": "DevOps Engineer",
                "required_skills": [
                    "Git Hooks",
                    "Shell Scripting",
                    "Repository Automation",
                ],
                "skill_level": "intermediate",
                "secondary_roles": ["Software Engineer"],
            },
            "learning_objectives": {
                "cognitive_level": "create",
                "objectives": [
                    "Implement Git hooks for automated file size checking",
                    "Design repository quality gates and validation",
                ],
                "prerequisites": [
                    "Git LFS basic configuration",
                    "Shell scripting fundamentals",
                ],
                "wiki_references": [
                    "wiki/automation/git-hooks",
                    "wiki/quality-assurance/repository-validation",
                ],
            },
            "acceptance_criteria": [
                {
                    "criterion": "Given a pre-commit hook, when a large file is added, then the commit is rejected with helpful error message",
                    "testable": True,
                    "test_method": "Automated testing with sample large files",
                },
                {
                    "criterion": "Given file size validation, when LFS-tracked files are committed, then they pass validation",
                    "testable": True,
                    "test_method": "Integration test with proper LFS workflow",
                },
                {
                    "criterion": "Given automation scripts, when new team members join, then they receive clear guidance on large file handling",
                    "testable": False,
                    "test_method": "User experience evaluation",
                },
            ],
            "definition_of_done": [
                "Pre-commit hooks implemented and tested",
                "Size threshold validation configured",
                "Error messages provide clear remediation steps",
                "CI/CD pipeline validates file sizes",
                "Documentation includes troubleshooting guide",
            ],
            "dependencies": {
                "blocks": ["STORY-1-3"],
                "blocked_by": ["STORY-1-1"],
                "related": [],
            },
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "assessment": {
                "unit_test_question": {
                    "question": "Which Git hook is most appropriate for preventing large files from being committed?",
                    "type": "multiple_choice",
                    "options": [
                        "pre-commit",
                        "post-commit",
                        "pre-push",
                        "post-receive",
                    ],
                    "correct_answer": "pre-commit",
                    "explanation": "The pre-commit hook runs before the commit is finalized, allowing it to reject the commit if large files are detected. This prevents the large files from entering the repository history at all.",
                }
            },
            "competency_indicators": [
                {
                    "level": "novice",
                    "description": "Understands the purpose of Git hooks and file size validation",
                },
                {
                    "level": "basic",
                    "description": "Can implement basic pre-commit hooks with file size checking",
                },
                {
                    "level": "proficient",
                    "description": "Can design comprehensive repository validation systems with custom hooks",
                },
            ],
            "sprint_planning": {
                "estimated_days": 2,
                "ideal_assignee_level": "intermediate",
                "risk_factors": [
                    "Git hook complexity varies by platform",
                    "Team workflow disruption during implementation",
                ],
                "success_metrics": [
                    "Zero large files committed without LFS",
                    "Reduced support requests about repository issues",
                ],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["automation", "validation", "git-hooks"],
        },
        {
            "id": "STORY-1-3",
            "type": "user_story",
            "title": "Repository Health Monitoring and Reporting",
            "description": "As a project manager, I want repository health monitoring so that I can track LFS usage, costs, and performance metrics over time",
            "priority": "low",
            "effort": {"hours": 20, "story_points": 13, "complexity": "user_story"},
            "skills": {
                "primary_role": "DevOps Engineer",
                "required_skills": [
                    "Monitoring Systems",
                    "Data Analytics",
                    "GitHub API",
                ],
                "skill_level": "advanced",
                "secondary_roles": ["Data Analyst", "Project Manager"],
            },
            "learning_objectives": {
                "cognitive_level": "analyze",
                "objectives": [
                    "Implement repository metrics collection and analysis",
                    "Design dashboard for repository health visualization",
                ],
                "prerequisites": [
                    "Git LFS operational experience",
                    "API integration knowledge",
                ],
                "wiki_references": [
                    "wiki/monitoring/repository-analytics",
                    "wiki/project-management/metrics-dashboard",
                ],
            },
            "acceptance_criteria": [
                {
                    "criterion": "Given LFS usage monitoring, when reviewing monthly reports, then costs and storage trends are clearly visible",
                    "testable": True,
                    "test_method": "Automated report generation and validation",
                },
                {
                    "criterion": "Given performance tracking, when repository operations slow down, then alerts notify administrators",
                    "testable": True,
                    "test_method": "Performance threshold testing and alerting",
                },
                {
                    "criterion": "Given health metrics, when planning repository scaling, then data supports decision making",
                    "testable": False,
                    "test_method": "Stakeholder feedback on report utility",
                },
            ],
            "definition_of_done": [
                "Monitoring dashboard implemented",
                "Automated LFS cost tracking configured",
                "Performance metrics collection active",
                "Monthly health reports automated",
                "Alert system configured for thresholds",
            ],
            "dependencies": {"blocks": [], "blocked_by": ["STORY-1-2"], "related": []},
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "assessment": {
                "unit_test_question": {
                    "question": "Why is monitoring Git LFS usage important for academic repositories?",
                    "type": "multiple_choice",
                    "options": [
                        "To track bandwidth costs and storage quotas",
                        "To improve PDF search capabilities",
                        "To enhance Git security features",
                        "To enable automatic file compression",
                    ],
                    "correct_answer": "To track bandwidth costs and storage quotas",
                    "explanation": "Git LFS has monthly bandwidth and storage quotas with associated costs. Monitoring usage helps organizations stay within limits and budget appropriately for their academic research storage needs.",
                }
            },
            "competency_indicators": [
                {
                    "level": "novice",
                    "description": "Understands the importance of monitoring repository health",
                },
                {
                    "level": "basic",
                    "description": "Can implement basic monitoring and reporting for LFS usage",
                },
                {
                    "level": "proficient",
                    "description": "Can design comprehensive repository analytics and alerting systems",
                },
            ],
            "sprint_planning": {
                "estimated_days": 3,
                "ideal_assignee_level": "advanced",
                "risk_factors": [
                    "API rate limiting for GitHub data collection",
                    "Dashboard complexity may exceed initial estimates",
                ],
                "success_metrics": [
                    "Proactive identification of repository issues",
                    "Reduced unexpected LFS overage charges",
                ],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["monitoring", "analytics", "reporting"],
        },
    ]

    return stories


def save_user_stories(stories: List[Dict[str, Any]], output_dir: Path):
    """Save user stories to individual JSON files."""
    output_dir.mkdir(exist_ok=True)

    for story in stories:
        story_file = output_dir / f"{story['id'].lower()}.json"
        with open(story_file, "w") as f:
            json.dump(story, f, indent=2)
        print(f"✅ Created user story: {story['id']} - {story['title']}")


def main():
    """Generate user stories for FEAT-1 and demonstrate hierarchical decomposition."""

    print("🎯 User Story Generation System")
    print("   Creating user stories for FEAT-1: Git LFS Implementation")
    print()

    # Generate user stories for FEAT-1
    stories = create_user_stories_for_feat1()

    # Save to files
    output_dir = Path("user_stories")
    save_user_stories(stories, output_dir)

    print()
    print(f"📋 Generated {len(stories)} user stories for FEAT-1")
    print("   Stories demonstrate explosive recursive decomposition:")

    for story in stories:
        print(f"   • {story['id']}: {story['title']}")
        print(
            f"     Effort: {story['effort']['hours']} hours, {story['effort']['story_points']} story points"
        )
        print(
            f"     Role: {story['skills']['primary_role']} ({story['skills']['skill_level']})"
        )
        print()

    # Show hierarchy relationships
    print("🔗 Dependency Chain:")
    print("   FEAT-1 → STORY-1-1 → STORY-1-2 → STORY-1-3")
    print()

    # Educational insights
    print("📚 Educational Insights:")
    print(
        "   • User stories follow 'As a [role], I want [goal] so that [benefit]' format"
    )
    print(
        "   • Each story includes comprehensive acceptance criteria with testability markers"
    )
    print("   • Learning objectives map to Bloom's taxonomy (apply → create → analyze)")
    print("   • Assessment questions validate understanding of key concepts")
    print("   • Competency indicators support skill progression tracking")
    print("   • Sprint planning data enables realistic project estimation")
    print()

    print("🎓 Next Steps:")
    print("   • Generate tasks for each user story")
    print("   • Create subtasks for detailed implementation guidance")
    print("   • Demonstrate complete Epic → Feature → Story → Task → Subtask hierarchy")
    print("   • Update knowledge graph with new relationships")


if __name__ == "__main__":
    main()
