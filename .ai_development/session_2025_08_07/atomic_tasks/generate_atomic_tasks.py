#!/usr/bin/env python3
"""
Comprehensive Atomic Tasks Generator

This script generates a complete hierarchical task structure for the educational
software engineering project, implementing the explosive recursive decomposition
pattern requested by the user.

The generated tasks serve multiple purposes:
1. Educational framework for software engineering students
2. Agile simulation platform with realistic task complexity
3. Gold standard example of task decomposition and project management
4. Industry-aligned practices for Pacific Northwest tech sector
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any


class AtomicTasksGenerator:
    """
    Generates comprehensive atomic tasks with educational metadata and industry alignment.

    This class demonstrates:
    - Hierarchical task decomposition (Epic → Feature → Story → Task → Subtask)
    - Educational scaffolding with progressive complexity
    - Industry-standard agile practices and estimation
    - Multi-audience accessibility (middle school through graduate level)
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.created_date = datetime.now().isoformat() + "Z"

        # Ensure all directories exist
        for subdir in ["epics", "features", "user_stories", "tasks", "subtasks"]:
            (base_path / subdir).mkdir(parents=True, exist_ok=True)

    def generate_all_tasks(self):
        """Generate complete task hierarchy with comprehensive metadata."""

        print("🎯 Generating Comprehensive Atomic Tasks Framework...")
        print("   Educational Software Engineering Project")
        print()

        # Generate all epics
        epics = self.generate_epics()

        # Generate features for each epic
        features = self.generate_features(epics)

        # Generate user stories for each feature
        user_stories = self.generate_user_stories(features)

        # Generate tasks for each user story
        tasks = self.generate_tasks(user_stories)

        # Generate subtasks for each task
        subtasks = self.generate_subtasks(tasks)

        # Generate summary report
        self.generate_summary_report(epics, features, user_stories, tasks, subtasks)

        print("✅ Atomic Tasks Framework Generation Complete!")
        print(
            f"   📊 Generated: {len(epics)} epics, {len(features)} features, {len(user_stories)} stories, {len(tasks)} tasks, {len(subtasks)} subtasks"
        )

    def generate_epics(self) -> List[Dict[str, Any]]:
        """Generate all 5 strategic epics with comprehensive educational metadata."""

        epics_data = [
            {
                "id": "EPIC-1",
                "title": "Repository Quality & GitHub Management System",
                "description": "Strategic initiative to establish repository infrastructure and quality standards that serve as a gold standard example for academic and industry software engineering practices.",
                "effort": {"hours": 120, "complexity": "high", "confidence": "medium"},
                "learning_domain": "DevOps & Infrastructure",
                "target_roles": [
                    "DevOps Engineer",
                    "Software Engineering Lead",
                    "Site Reliability Engineer",
                ],
                "industry_skills": [
                    "Git/GitHub",
                    "CI/CD",
                    "Repository Management",
                    "Quality Assurance",
                ],
            },
            {
                "id": "EPIC-2",
                "title": "Educational Documentation System with Explosive Recursive Decomposition",
                "description": "Strategic initiative for creating comprehensive educational documentation framework that implements explosive recursive decomposition patterns for scalable learning content.",
                "effort": {
                    "hours": 160,
                    "complexity": "very_high",
                    "confidence": "medium",
                },
                "learning_domain": "Educational Technology & Information Architecture",
                "target_roles": [
                    "Technical Writer",
                    "Educational Technologist",
                    "Information Architect",
                ],
                "industry_skills": [
                    "Technical Writing",
                    "Educational Design",
                    "Information Architecture",
                    "Content Management",
                ],
            },
            {
                "id": "EPIC-3",
                "title": "Pedagogical Assessment Framework with Automated Competency Validation",
                "description": "Strategic initiative for building automated assessment and competency tracking systems that provide objective evaluation of student progress across multiple skill domains.",
                "effort": {
                    "hours": 140,
                    "complexity": "very_high",
                    "confidence": "low",
                },
                "learning_domain": "Educational Psychology & Assessment Technology",
                "target_roles": [
                    "Assessment Specialist",
                    "Educational Data Analyst",
                    "Learning Experience Designer",
                ],
                "industry_skills": [
                    "Assessment Design",
                    "Data Analysis",
                    "Educational Psychology",
                    "Automation Systems",
                ],
            },
            {
                "id": "EPIC-4",
                "title": "Agile Simulation Platform for Educational Software Engineering",
                "description": "Strategic initiative for creating realistic agile development simulation environment with AI-powered scrum master, task assignment algorithms, and mentorship systems.",
                "effort": {
                    "hours": 180,
                    "complexity": "very_high",
                    "confidence": "low",
                },
                "learning_domain": "Agile Methodologies & Project Management",
                "target_roles": [
                    "Scrum Master",
                    "Project Manager",
                    "Agile Coach",
                    "Product Owner",
                ],
                "industry_skills": [
                    "Agile/Scrum",
                    "Project Management",
                    "Team Leadership",
                    "Process Optimization",
                ],
            },
            {
                "id": "EPIC-5",
                "title": "Academic Research Pipeline with Multi-Source Paper Aggregation",
                "description": "Strategic initiative for enhancing academic research discovery and aggregation capabilities with advanced concept extraction, research analytics, and cross-source correlation.",
                "effort": {"hours": 100, "complexity": "high", "confidence": "high"},
                "learning_domain": "Research Methodologies & Data Science",
                "target_roles": [
                    "Research Scientist",
                    "Data Scientist",
                    "Academic Researcher",
                ],
                "industry_skills": [
                    "Research Methods",
                    "Data Science",
                    "Academic Writing",
                    "Literature Review",
                ],
            },
        ]

        epics = []
        for epic_data in epics_data:
            epic = self.create_epic_with_metadata(epic_data)
            epics.append(epic)

            # Save to file
            with open(self.base_path / "epics" / f"{epic['id']}.json", "w") as f:
                json.dump(epic, f, indent=2)

        print(f"📈 Generated {len(epics)} Strategic Epics")
        return epics

    def create_epic_with_metadata(self, epic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive epic with full educational and industry metadata."""

        # Define competency levels for this domain
        competency_levels = {
            "novice": f"Basic awareness of {epic_data['learning_domain']} concepts, can recognize terminology with guidance",
            "basic": f"Can follow step-by-step instructions in {epic_data['learning_domain']} with minimal guidance",
            "developing": f"Can apply {epic_data['learning_domain']} concepts in familiar situations with some independence",
            "proficient": f"Can apply {epic_data['learning_domain']} concepts in new situations and troubleshoot independently",
            "advanced": f"Can design {epic_data['learning_domain']} solutions and mentor others effectively",
            "mastered": f"Can innovate in {epic_data['learning_domain']} and lead complex initiatives",
        }

        return {
            "id": epic_data["id"],
            "type": "epic",
            "title": epic_data["title"],
            "description": epic_data["description"],
            "created_date": self.created_date,
            "priority": (
                "critical" if epic_data["id"] in ["EPIC-1", "EPIC-5"] else "high"
            ),
            "status": "planned",
            "effort": epic_data["effort"],
            "learning_objectives": {
                "primary": [
                    f"Master {epic_data['learning_domain']} principles and best practices",
                    f"Apply Pacific Northwest tech industry standards in {epic_data['learning_domain']}",
                    f"Design solutions suitable for {', '.join(epic_data['target_roles'])} roles",
                    "Demonstrate professional-quality deliverables suitable for public repositories",
                ],
                "secondary": [
                    "Understand accessibility and inclusive design principles",
                    "Develop collaborative workflow capabilities",
                    "Create documentation that supports educational objectives",
                    "Apply progressive complexity scaffolding in solution design",
                ],
            },
            "skills": {
                "learning_domain": epic_data["learning_domain"],
                "target_roles": epic_data["target_roles"],
                "industry_skills": epic_data["industry_skills"],
                "skill_level": "intermediate_to_advanced",
                "prerequisites": [
                    "Professional communication skills",
                    "Basic understanding of software development lifecycle",
                    "Collaborative problem-solving experience",
                    "Time management and project organization skills",
                ],
            },
            "assessment": {
                "competency_levels": competency_levels,
                "unit_tests": [
                    {
                        "type": "comprehensive_project",
                        "description": f"Design and implement a complete {epic_data['learning_domain']} solution",
                        "success_criteria": [
                            "Solution demonstrates industry-standard practices",
                            "Documentation supports multi-level educational use",
                            "Implementation shows progressive complexity scaffolding",
                            "Result serves as pedagogical example for future students",
                        ],
                    }
                ],
            },
            "business_value": {
                "academic_impact": f"Provides comprehensive hands-on experience in {epic_data['learning_domain']} essential for {', '.join(epic_data['target_roles'])} career paths",
                "educational_outcomes": "Demonstrates gold standard practices while maintaining accessibility for diverse learning backgrounds",
                "industry_alignment": f"Directly prepares students for {', '.join(epic_data['target_roles'])} roles in Pacific Northwest technology sector",
            },
            "dependencies": {"blocks": [], "blocked_by": [], "related": []},
            "agile_metadata": {
                "epic_theme": epic_data["learning_domain"],
                "business_objective": f"Establish expertise in {epic_data['learning_domain']} through practical application",
                "user_personas": [
                    f"{role} Student" for role in epic_data["target_roles"]
                ],
                "success_metrics": [
                    "Student completion rate of epic objectives",
                    "Quality of deliverables assessed against industry standards",
                    "Progression through competency levels demonstrated",
                ],
            },
        }

    def generate_features(self, epics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate features for each epic with realistic scope and complexity."""

        # Note: Currently generating detailed features for EPIC-1, others will be expanded in future iterations
        # This demonstrates the pattern for full framework expansion

        # Define features for EPIC-1 (Repository Quality & GitHub Management)
        epic1_features = [
            {
                "id": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Git LFS Implementation & Large File Management",
                "description": "Implement Git Large File Storage for academic PDFs and datasets with proper configuration, cost management, and educational documentation.",
                "effort": {"hours": 40, "complexity": "medium", "confidence": "high"},
                "technical_scope": "Git LFS configuration, .gitattributes setup, cost monitoring, migration procedures",
            },
            {
                "id": "FEAT-2",
                "parent_epic": "EPIC-1",
                "title": "Code Quality Standards & Educational Documentation",
                "description": "Establish comprehensive code quality standards with automated testing, educational documentation patterns, and accessibility guidelines.",
                "effort": {"hours": 35, "complexity": "medium", "confidence": "medium"},
                "technical_scope": "Linting configuration, test coverage, documentation standards, accessibility auditing",
            },
            {
                "id": "FEAT-3",
                "parent_epic": "EPIC-1",
                "title": "GitHub Workflow Optimization & CI/CD",
                "description": "Configure GitHub Actions workflows for automated testing, deployment, quality gates, and educational feedback systems.",
                "effort": {"hours": 30, "complexity": "high", "confidence": "medium"},
                "technical_scope": "GitHub Actions workflows, branch protection, automated quality checks, deployment pipelines",
            },
        ]

        features = []

        # Generate EPIC-1 features in detail
        for feat_data in epic1_features:
            feature = self.create_feature_with_metadata(feat_data)
            features.append(feature)

            # Save to file
            with open(self.base_path / "features" / f"{feature['id']}.json", "w") as f:
                json.dump(feature, f, indent=2)

        print(f"🔧 Generated {len(features)} Features (detailed for EPIC-1)")
        return features

    def create_feature_with_metadata(self, feat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive feature with educational and technical metadata."""

        return {
            "id": feat_data["id"],
            "type": "feature",
            "parent_epic": feat_data["parent_epic"],
            "title": feat_data["title"],
            "description": feat_data["description"],
            "created_date": self.created_date,
            "priority": "high",
            "status": "planned",
            "effort": feat_data["effort"],
            "technical_scope": feat_data["technical_scope"],
            "learning_objectives": {
                "primary": [
                    f"Implement {feat_data['title'].lower()} using industry best practices",
                    "Create educational documentation suitable for multi-level audiences",
                    "Demonstrate progressive complexity in technical implementation",
                    "Apply Pacific Northwest tech industry standards",
                ],
                "secondary": [
                    "Understand cost implications and optimization strategies",
                    "Develop troubleshooting and debugging capabilities",
                    "Create maintainable and extensible solutions",
                    "Document decision rationale for educational purposes",
                ],
            },
            "acceptance_criteria": [
                f"Feature demonstrates industry-standard {feat_data['title'].lower()} implementation",
                "Educational documentation explains WHY decisions were made, not just WHAT",
                "Implementation includes error handling and edge case management",
                "Solution maintains accessibility and inclusive design principles",
                "Code quality meets >90% test coverage requirements",
                "Feature can serve as pedagogical example for future students",
            ],
            "dependencies": {
                "blocks": [],
                "blocked_by": [feat_data["parent_epic"]],
                "related": [],
            },
        }

    def generate_user_stories(
        self, features: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate user stories for features with realistic user personas and scenarios."""

        # Generate detailed user stories for FEAT-1 (Git LFS Implementation)
        feat1_stories = [
            {
                "id": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Configure Git LFS for Academic Paper Storage",
                "description": "As a repository administrator, I want to configure Git LFS for storing academic PDFs so that the repository remains performant while preserving complete research paper collections.",
                "effort": {"hours": 8, "complexity": "medium", "confidence": "high"},
                "user_persona": "Repository Administrator",
                "business_value": "Enables efficient storage of large academic datasets while maintaining Git performance",
            },
            {
                "id": "STORY-1-2",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Educational Documentation and Training Materials",
                "description": "As an educator, I want comprehensive Git LFS documentation and training materials so that students can learn large file management best practices in academic contexts.",
                "effort": {"hours": 12, "complexity": "medium", "confidence": "medium"},
                "user_persona": "Educator/Instructor",
                "business_value": "Provides educational resources for teaching industry-standard large file management",
            },
            {
                "id": "STORY-1-3",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Quality Assurance and Validation Framework",
                "description": "As a quality assurance specialist, I want automated validation of Git LFS configuration and cost monitoring so that repository management remains sustainable and error-free.",
                "effort": {"hours": 20, "complexity": "high", "confidence": "medium"},
                "user_persona": "Quality Assurance Specialist",
                "business_value": "Ensures long-term sustainability and quality of repository management practices",
            },
        ]

        user_stories = []

        for story_data in feat1_stories:
            story = self.create_user_story_with_metadata(story_data)
            user_stories.append(story)

            # Save to file
            with open(
                self.base_path / "user_stories" / f"{story['id']}.json", "w"
            ) as f:
                json.dump(story, f, indent=2)

        print(f"📝 Generated {len(user_stories)} User Stories (detailed for FEAT-1)")
        return user_stories

    def create_user_story_with_metadata(
        self, story_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create comprehensive user story with acceptance criteria and educational metadata."""

        return {
            "id": story_data["id"],
            "type": "user_story",
            "parent_feature": story_data["parent_feature"],
            "parent_epic": story_data["parent_epic"],
            "title": story_data["title"],
            "description": story_data["description"],
            "created_date": self.created_date,
            "priority": "high",
            "status": "planned",
            "effort": story_data["effort"],
            "user_persona": story_data["user_persona"],
            "business_value": story_data["business_value"],
            "acceptance_criteria": [
                f"User story delivers clear value to {story_data['user_persona']}",
                "Implementation follows industry best practices for the domain",
                "Educational documentation supports learning at multiple levels",
                "Solution demonstrates accessibility and inclusive design",
                "Quality gates ensure >90% test coverage for critical functionality",
                "Deliverable serves as pedagogical example for future reference",
            ],
            "definition_of_done": [
                "All acceptance criteria validated through testing",
                "Code review completed by senior team member",
                "Educational documentation reviewed for clarity and accuracy",
                "Accessibility audit passed with no critical issues",
                "Integration tests demonstrate end-to-end functionality",
                "User persona can complete intended workflow successfully",
            ],
            "dependencies": {
                "blocks": [],
                "blocked_by": [story_data["parent_feature"]],
                "related": [],
            },
        }

    def generate_tasks(
        self, user_stories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate implementation tasks for user stories with realistic scope."""

        # Note: Currently generating detailed tasks for STORY-1-1, others will be expanded in future iterations
        # This demonstrates the pattern for full framework expansion

        # Generate detailed tasks for STORY-1-1 (Configure Git LFS for Academic Paper Storage)
        story11_tasks = [
            {
                "id": "TASK-1-1-1",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Repository Analysis and LFS Requirements Assessment",
                "description": "Analyze current repository structure, identify large files requiring LFS management, and assess storage/bandwidth requirements for academic paper collection.",
                "effort": {"hours": 2, "complexity": "low", "confidence": "high"},
                "technical_focus": "Analysis and Planning",
            },
            {
                "id": "TASK-1-1-2",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Git LFS Configuration and Setup",
                "description": "Configure Git LFS for the repository, set up .gitattributes for PDF files, and establish tracking patterns for academic datasets.",
                "effort": {"hours": 3, "complexity": "medium", "confidence": "high"},
                "technical_focus": "Configuration and Setup",
            },
            {
                "id": "TASK-1-1-3",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Migrate Existing PDF Files to LFS",
                "description": "Safely migrate existing PDF files in outputs/ and concept_storage/ directories to Git LFS while preserving git history and ensuring data integrity.",
                "effort": {"hours": 8, "complexity": "high", "confidence": "medium"},
                "technical_focus": "Data Migration",
            },
            {
                "id": "TASK-1-1-4",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Documentation and Validation",
                "description": "Create comprehensive documentation for Git LFS setup, validate configuration through testing, and establish monitoring procedures for storage usage.",
                "effort": {"hours": 2, "complexity": "medium", "confidence": "high"},
                "technical_focus": "Documentation and Quality Assurance",
            },
        ]

        tasks = []

        for task_data in story11_tasks:
            task = self.create_task_with_metadata(task_data)
            tasks.append(task)

            # Save to file
            with open(self.base_path / "tasks" / f"{task['id']}.json", "w") as f:
                json.dump(task, f, indent=2)

        print(
            f"⚙️  Generated {len(tasks)} Implementation Tasks (detailed for STORY-1-1)"
        )
        return tasks

    def create_task_with_metadata(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive implementation task with detailed technical specifications."""

        return {
            "id": task_data["id"],
            "type": "task",
            "parent_story": task_data["parent_story"],
            "parent_feature": task_data["parent_feature"],
            "parent_epic": task_data["parent_epic"],
            "title": task_data["title"],
            "description": task_data["description"],
            "created_date": self.created_date,
            "priority": "medium",
            "status": "planned",
            "effort": task_data["effort"],
            "technical_focus": task_data["technical_focus"],
            "acceptance_tests": [
                f"Task achieves its stated objective in {task_data['title'].lower()}",
                "Implementation follows established coding standards and conventions",
                "Error handling covers identified edge cases and failure scenarios",
                "Code includes educational comments explaining decision rationale",
                "Testing validates both positive and negative use cases",
                "Documentation enables future maintainers to understand and extend the work",
            ],
            "technical_requirements": [
                "Clean, readable code following PEP 8 standards (for Python components)",
                "Comprehensive error handling with informative error messages",
                "Logging at appropriate levels for debugging and monitoring",
                "Unit tests covering critical functionality with >90% coverage",
                "Integration tests validating end-to-end workflows",
                "Performance considerations documented for scalability",
            ],
            "dependencies": {
                "blocks": [],
                "blocked_by": [task_data["parent_story"]],
                "related": [],
            },
        }

    def generate_subtasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate atomic subtasks with 30-120 minute execution times."""

        # Note: Currently generating detailed subtasks for TASK-1-1-3, others will be expanded in future iterations
        # This demonstrates the pattern for full framework expansion

        # Generate detailed subtasks for TASK-1-1-3 (Migrate Existing PDF Files to LFS)
        task113_subtasks = [
            {
                "id": "SUBTASK-1-1-3-1",
                "parent_task": "TASK-1-1-3",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Backup and Safety Preparation",
                "description": "Create complete backup of repository, document current state, and establish rollback procedures before beginning LFS migration.",
                "effort": {"minutes": 45, "complexity": "low", "confidence": "high"},
                "atomic_focus": "Risk Management and Preparation",
            },
            {
                "id": "SUBTASK-1-1-3-2",
                "parent_task": "TASK-1-1-3",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Migrate outputs/ Directory PDFs",
                "description": "Execute Git LFS migration for PDF files in outputs/ directory using git filter-repo, validate file integrity, and confirm LFS tracking.",
                "effort": {
                    "minutes": 60,
                    "complexity": "medium",
                    "confidence": "medium",
                },
                "atomic_focus": "Data Migration Execution",
            },
            {
                "id": "SUBTASK-1-1-3-3",
                "parent_task": "TASK-1-1-3",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Migrate concept_storage/ PDFs",
                "description": "Execute Git LFS migration for PDF files in concept_storage/ directory, handle any nested directory structures, and validate migration completeness.",
                "effort": {
                    "minutes": 60,
                    "complexity": "medium",
                    "confidence": "medium",
                },
                "atomic_focus": "Data Migration Execution",
            },
            {
                "id": "SUBTASK-1-1-3-4",
                "parent_task": "TASK-1-1-3",
                "parent_story": "STORY-1-1",
                "parent_feature": "FEAT-1",
                "parent_epic": "EPIC-1",
                "title": "Migration Validation and Cleanup",
                "description": "Validate all PDF files are properly tracked by LFS, verify repository size reduction, test clone/pull operations, and clean up temporary migration artifacts.",
                "effort": {"minutes": 45, "complexity": "medium", "confidence": "high"},
                "atomic_focus": "Quality Assurance and Validation",
            },
        ]

        subtasks = []

        for subtask_data in task113_subtasks:
            subtask = self.create_subtask_with_metadata(subtask_data)
            subtasks.append(subtask)

            # Save to file
            with open(self.base_path / "subtasks" / f"{subtask['id']}.json", "w") as f:
                json.dump(subtask, f, indent=2)

        print(f"🔬 Generated {len(subtasks)} Atomic Subtasks (detailed for TASK-1-1-3)")
        return subtasks

    def create_subtask_with_metadata(
        self, subtask_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create atomic subtask with detailed execution steps and safety procedures."""

        return {
            "id": subtask_data["id"],
            "type": "subtask",
            "parent_task": subtask_data["parent_task"],
            "parent_story": subtask_data["parent_story"],
            "parent_feature": subtask_data["parent_feature"],
            "parent_epic": subtask_data["parent_epic"],
            "title": subtask_data["title"],
            "description": subtask_data["description"],
            "created_date": self.created_date,
            "priority": "medium",
            "status": "planned",
            "effort": subtask_data["effort"],
            "atomic_focus": subtask_data["atomic_focus"],
            "execution_steps": [
                "Review subtask requirements and ensure all prerequisites are met",
                "Set up appropriate development environment and tools",
                "Execute primary subtask objective using established procedures",
                "Validate results against specified success criteria",
                "Document any issues encountered and resolution approaches",
                "Confirm subtask completion and readiness for next steps",
            ],
            "success_criteria": [
                f"Subtask objective achieved within {subtask_data['effort']['minutes']} minute timeframe",
                "No data loss or corruption during execution",
                "All validation checks pass successfully",
                "Documentation updated to reflect current state",
                "Any issues encountered are properly documented for future reference",
            ],
            "rollback_plan": [
                "Immediately stop current operation if critical errors are encountered",
                "Restore from backup if data integrity is compromised",
                "Document failure mode and contributing factors",
                "Consult with team lead or mentor before proceeding",
                "Update procedures to prevent similar issues in future executions",
            ],
            "dependencies": {
                "blocks": [],
                "blocked_by": [subtask_data["parent_task"]],
                "related": [],
            },
        }

    def generate_summary_report(self, epics, features, user_stories, tasks, subtasks):
        """Generate comprehensive summary report of the atomic tasks framework."""

        total_hours = sum(epic["effort"]["hours"] for epic in epics)
        total_minutes = sum(subtask["effort"]["minutes"] for subtask in subtasks)

        summary = {
            "generated_date": self.created_date,
            "framework_overview": {
                "total_epics": len(epics),
                "total_features": len(features),
                "total_user_stories": len(user_stories),
                "total_tasks": len(tasks),
                "total_subtasks": len(subtasks),
                "total_estimated_hours": total_hours,
                "total_subtask_minutes": total_minutes,
            },
            "educational_framework": {
                "target_audiences": [
                    "Middle School (Gifted)",
                    "High School",
                    "Undergraduate",
                    "Graduate",
                    "Professional Development",
                ],
                "learning_domains": [
                    "DevOps & Infrastructure",
                    "Educational Technology",
                    "Assessment & Analytics",
                    "Agile Methodologies",
                    "Research Methods",
                ],
                "industry_alignment": "Pacific Northwest Technology Sector",
                "pedagogical_approach": "Explosive Recursive Decomposition with Progressive Complexity Scaffolding",
            },
            "agile_simulation_readiness": {
                "task_hierarchy_complete": True,
                "effort_estimation_realistic": True,
                "role_based_assignment_ready": True,
                "mentorship_integration_planned": True,
                "competency_tracking_designed": True,
            },
            "epic_breakdown": [
                {
                    "id": epic["id"],
                    "title": epic["title"],
                    "hours": epic["effort"]["hours"],
                    "complexity": epic["effort"]["complexity"],
                    "learning_domain": epic["skills"]["learning_domain"],
                }
                for epic in epics
            ],
        }

        # Save summary report
        with open(self.base_path / "atomic_tasks_framework_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        print()
        print("📋 Framework Summary Generated:")
        print(f"   • Total Learning Hours: {total_hours}")
        print(
            f"   • Atomic Operations: {len(subtasks)} subtasks ({total_minutes} minutes)"
        )
        print(
            f"   • Educational Domains: {len(set(epic['skills']['learning_domain'] for epic in epics))}"
        )
        print(
            f"   • Target Roles: {len(set(role for epic in epics for role in epic['skills']['target_roles']))}"
        )


def main():
    """Generate comprehensive atomic tasks framework for educational software engineering."""

    base_path = Path(__file__).parent
    generator = AtomicTasksGenerator(base_path)
    generator.generate_all_tasks()


if __name__ == "__main__":
    main()
