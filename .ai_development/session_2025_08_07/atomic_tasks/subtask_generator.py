#!/usr/bin/env python3
"""
Subtask Generator - Creates granular implementation steps from complex tasks.

This system demonstrates the fifth and final level of explosive recursive decomposition
by taking complex tasks and breaking them down into precise implementation steps that
can be executed methodically by developers.

Educational Notes:
- Shows how complex tasks decompose into executable steps
- Demonstrates risk mitigation through incremental implementation
- Implements checklist-driven development for quality assurance
- Uses atomic commits pattern for version control best practices
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def create_subtasks_for_task_1_1_3():
    """
    Create subtasks for TASK-1-1-3: Migrate Existing PDF Files to LFS.

    This demonstrates how a complex migration task breaks down into safe,
    verifiable steps that minimize risk and ensure data integrity.
    """

    subtasks = [
        {
            "id": "SUBTASK-1-1-3-1",
            "type": "subtask",
            "title": "Audit Current PDF Files and Create Backup",
            "description": "Inventory existing PDF files and create repository backup before migration",
            "priority": "critical",
            "effort": {
                "minutes": 45,
                "complexity": "subtask",
                "atomic_operation": True,
            },
            "implementation_steps": [
                {
                    "step": 1,
                    "action": "Run file inventory command",
                    "command": "find . -name '*.pdf' -type f -exec ls -lh {} \\; > pdf_inventory_pre_migration.txt",
                    "expected_outcome": "Complete list of PDF files with sizes",
                    "verification": "File pdf_inventory_pre_migration.txt contains all PDFs",
                },
                {
                    "step": 2,
                    "action": "Calculate total repository size",
                    "command": "du -sh .git && git count-objects -vH",
                    "expected_outcome": "Baseline repository size metrics",
                    "verification": "Record sizes in migration log",
                },
                {
                    "step": 3,
                    "action": "Create repository backup",
                    "command": "cd .. && tar -czf research-paper-aggregator-backup-$(date +%Y%m%d).tar.gz research-paper-aggregator/",
                    "expected_outcome": "Complete repository backup created",
                    "verification": "Backup file exists and can be extracted",
                },
                {
                    "step": 4,
                    "action": "Verify backup integrity",
                    "command": "tar -tzf ../research-paper-aggregator-backup-*.tar.gz | head -20",
                    "expected_outcome": "Backup contains expected files",
                    "verification": "Key files present in backup listing",
                },
            ],
            "safety_checks": [
                "Backup file is created and verified",
                "Current working directory is preserved",
                "PDF inventory matches expected files",
                "No uncommitted changes in repository",
            ],
            "rollback_plan": [
                "Restore from backup if migration fails",
                "Commands: cd ..; tar -xzf research-paper-aggregator-backup-*.tar.gz",
            ],
            "parent_task": "TASK-1-1-3",
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {
                "blocks": ["SUBTASK-1-1-3-2"],
                "blocked_by": [],
                "related": [],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["backup", "audit", "safety"],
        },
        {
            "id": "SUBTASK-1-1-3-2",
            "type": "subtask",
            "title": "Test Migration on Feature Branch",
            "description": "Perform migration test on isolated branch to validate process",
            "priority": "high",
            "effort": {
                "minutes": 30,
                "complexity": "subtask",
                "atomic_operation": True,
            },
            "implementation_steps": [
                {
                    "step": 1,
                    "action": "Create migration test branch",
                    "command": "git checkout -b lfs-migration-test",
                    "expected_outcome": "New branch created and checked out",
                    "verification": "git branch shows lfs-migration-test as current",
                },
                {
                    "step": 2,
                    "action": "Run migration on test branch",
                    "command": "git lfs migrate import --include='*.pdf' --include-ref=refs/heads/lfs-migration-test",
                    "expected_outcome": "PDFs migrated to LFS on test branch",
                    "verification": "git lfs ls-files shows PDF files",
                },
                {
                    "step": 3,
                    "action": "Verify migrated files work",
                    "command": "ls -la outputs/ && file outputs/*/*.pdf | head -5",
                    "expected_outcome": "PDF files are accessible and valid",
                    "verification": "file command identifies PDFs correctly",
                },
                {
                    "step": 4,
                    "action": "Check repository size improvement",
                    "command": "git count-objects -vH",
                    "expected_outcome": "Significant reduction in repository size",
                    "verification": "Size-pack value decreased substantially",
                },
            ],
            "safety_checks": [
                "Working on isolated test branch",
                "Original branch unchanged",
                "All PDF files remain accessible",
                "Migration process completed without errors",
            ],
            "rollback_plan": [
                "Switch back to main branch",
                "Commands: git checkout main; git branch -D lfs-migration-test",
            ],
            "parent_task": "TASK-1-1-3",
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {
                "blocks": ["SUBTASK-1-1-3-3"],
                "blocked_by": ["SUBTASK-1-1-3-1"],
                "related": [],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["testing", "migration", "validation"],
        },
        {
            "id": "SUBTASK-1-1-3-3",
            "type": "subtask",
            "title": "Execute Production Migration",
            "description": "Perform the actual migration on main branch with team coordination",
            "priority": "high",
            "effort": {
                "minutes": 60,
                "complexity": "subtask",
                "atomic_operation": True,
            },
            "implementation_steps": [
                {
                    "step": 1,
                    "action": "Coordinate with team",
                    "command": "# Send team notification about migration window",
                    "expected_outcome": "Team aware of migration and timing",
                    "verification": "Confirmation from team members received",
                },
                {
                    "step": 2,
                    "action": "Switch to main branch and ensure clean state",
                    "command": "git checkout main && git status",
                    "expected_outcome": "On main branch with clean working directory",
                    "verification": "git status shows no uncommitted changes",
                },
                {
                    "step": 3,
                    "action": "Execute production migration",
                    "command": "git lfs migrate import --include='*.pdf'",
                    "expected_outcome": "All PDF files migrated to LFS",
                    "verification": "git lfs ls-files shows all expected PDFs",
                },
                {
                    "step": 4,
                    "action": "Force push with lease protection",
                    "command": "git push --force-with-lease origin main",
                    "expected_outcome": "Migration pushed to remote repository",
                    "verification": "Push succeeds without conflicts",
                },
            ],
            "safety_checks": [
                "Team coordination completed",
                "Clean working directory confirmed",
                "Migration matches test results",
                "Force-with-lease protects against overwrites",
            ],
            "rollback_plan": [
                "Restore from backup if critical issues occur",
                "Communicate rollback to team immediately",
            ],
            "parent_task": "TASK-1-1-3",
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {
                "blocks": ["SUBTASK-1-1-3-4"],
                "blocked_by": ["SUBTASK-1-1-3-2"],
                "related": [],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["production", "migration", "coordination"],
        },
        {
            "id": "SUBTASK-1-1-3-4",
            "type": "subtask",
            "title": "Verify Migration and Clean Up",
            "description": "Confirm migration success and remove temporary files",
            "priority": "medium",
            "effort": {
                "minutes": 30,
                "complexity": "subtask",
                "atomic_operation": True,
            },
            "implementation_steps": [
                {
                    "step": 1,
                    "action": "Generate post-migration inventory",
                    "command": "git lfs ls-files > lfs_files_post_migration.txt && wc -l lfs_files_post_migration.txt",
                    "expected_outcome": "Complete inventory of LFS-tracked files",
                    "verification": "File count matches pre-migration PDF count",
                },
                {
                    "step": 2,
                    "action": "Verify repository size reduction",
                    "command": "du -sh .git && git count-objects -vH",
                    "expected_outcome": "Significant repository size reduction",
                    "verification": "Size reduction >80% for large repositories",
                },
                {
                    "step": 3,
                    "action": "Test random PDF accessibility",
                    "command": "find outputs/ -name '*.pdf' | shuf -n 3 | xargs file",
                    "expected_outcome": "Sample PDFs are accessible and valid",
                    "verification": "file command confirms PDF format",
                },
                {
                    "step": 4,
                    "action": "Clean up temporary files",
                    "command": "rm -f pdf_inventory_pre_migration.txt lfs_files_post_migration.txt",
                    "expected_outcome": "Temporary files removed",
                    "verification": "Working directory is clean",
                },
            ],
            "safety_checks": [
                "All PDFs accessible through LFS",
                "Repository size significantly reduced",
                "No data loss during migration",
                "Team can access repository normally",
            ],
            "rollback_plan": [
                "Migration is complete - rollback requires backup restoration",
                "Document any issues for future improvements",
            ],
            "parent_task": "TASK-1-1-3",
            "parent_story": "STORY-1-1",
            "parent_feature": "FEAT-1",
            "parent_epic": "EPIC-1",
            "dependencies": {
                "blocks": [],
                "blocked_by": ["SUBTASK-1-1-3-3"],
                "related": [],
            },
            "status": "not_started",
            "created_date": datetime.now().isoformat(),
            "tags": ["verification", "cleanup", "completion"],
        },
    ]

    return subtasks


def save_subtasks(subtasks: List[Dict[str, Any]], output_dir: Path):
    """Save subtasks to individual JSON files."""
    output_dir.mkdir(exist_ok=True)

    for subtask in subtasks:
        subtask_file = output_dir / f"{subtask['id'].lower()}.json"
        with open(subtask_file, "w") as f:
            json.dump(subtask, f, indent=2)
        print(f"✅ Created subtask: {subtask['id']} - {subtask['title']}")


def main():
    """Generate subtasks for TASK-1-1-3 and demonstrate atomic implementation."""

    print("🔬 Subtask Generation System")
    print("   Creating atomic steps for TASK-1-1-3: Migrate Existing PDF Files to LFS")
    print()

    # Generate subtasks for TASK-1-1-3
    subtasks = create_subtasks_for_task_1_1_3()

    # Save to files
    output_dir = Path("subtasks")
    save_subtasks(subtasks, output_dir)

    print()
    print(f"⚛️  Generated {len(subtasks)} subtasks for TASK-1-1-3")
    print("   Subtasks demonstrate atomic implementation breakdown:")

    total_minutes = 0
    for subtask in subtasks:
        minutes = subtask["effort"]["minutes"]
        total_minutes += minutes
        print(f"   • {subtask['id']}: {subtask['title']}")
        print(
            f"     Duration: {minutes} minutes (atomic: {subtask['effort']['atomic_operation']})"
        )
        print(
            f"     Steps: {len(subtask['implementation_steps'])} implementation steps"
        )
        print()

    print("📊 Task Implementation Summary:")
    print(f"   • Total effort: {total_minutes} minutes ({total_minutes/60:.1f} hours)")
    print("   • Original estimate: 3 hours (180 minutes)")
    print(
        f"   • Subtask breakdown accuracy: {'✅ Good' if abs(total_minutes - 180) < 30 else '⚠️  Needs adjustment'}"
    )
    print()

    # Show execution sequence
    print("🔗 Execution Sequence:")
    print(
        "   TASK-1-1-3 → SUBTASK-1-1-3-1 → SUBTASK-1-1-3-2 → SUBTASK-1-1-3-3 → SUBTASK-1-1-3-4"
    )
    print()

    # Educational insights
    print("📚 Educational Insights:")
    print("   • Subtasks are atomic operations with clear start/end states")
    print("   • Each subtask includes detailed command-by-command implementation")
    print("   • Safety checks and rollback plans minimize risk")
    print("   • Verification steps ensure quality at each stage")
    print("   • Team coordination integrated into technical process")
    print("   • Incremental approach enables early problem detection")
    print()

    print("🏆 Complete Hierarchy Achieved:")
    print("   EPIC-1 → FEAT-1 → STORY-1-1 → TASK-1-1-3 → SUBTASK-1-1-3-1")
    print("   (Epic → Feature → User Story → Task → Subtask)")
    print()

    print("🎓 Final Educational Outcomes:")
    print("   • Demonstrated explosive recursive decomposition across 5 levels")
    print(
        "   • Showed practical application of educational hierarchy to software engineering"
    )
    print(
        "   • Created actionable implementation guidance for real-world Git LFS deployment"
    )
    print(
        "   • Integrated risk management and quality assurance into development process"
    )
    print(
        "   • Provided complete knowledge graph structure for academic project management"
    )


if __name__ == "__main__":
    main()
