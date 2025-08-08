#!/usr/bin/env python3
"""
Simple Knowledge Graph Demonstration - Showcases graph algorithms on task hierarchies.

This demonstrates the practical application of knowledge graph traversal algorithms
on the educational atomic task framework, bridging theory and practice.

Educational Notes:
- Shows real-world application of graph theory concepts
- Demonstrates BFS, DFS, topological sorting, and PageRank on educational tasks
- Illustrates how computer science algorithms solve project management problems
"""

import json
from pathlib import Path
from atomic_task_graph import AtomicTaskGraph, AtomicTask


def create_sample_features():
    """Create sample features for EPIC-1 to demonstrate knowledge graph algorithms."""

    features = [
        {
            "id": "FEAT-1",
            "task_type": "feature",
            "title": "Git LFS Implementation & Large File Management",
            "description": "Implement Git LFS for managing large research datasets and PDF repositories efficiently within GitHub size limits",
            "priority": "high",
            "effort": {"hours": 40, "story_points": 8, "complexity": "feature"},
            "skills": {
                "primary_role": "DevOps Engineer",
                "required_skills": ["Git LFS Configuration", "Repository Management"],
                "skill_level": "intermediate",
            },
            "learning_objectives": {
                "cognitive_level": "apply",
                "objectives": ["Configure Git LFS for optimal repository performance"],
                "prerequisites": ["Basic Git knowledge"],
            },
            "acceptance_criteria": [
                {
                    "criterion": "Git LFS configured for PDF and dataset files",
                    "testable": True,
                }
            ],
            "definition_of_done": ["Git LFS setup complete", "Repository size reduced"],
            "dependencies": {"blocks": [], "blocked_by": [], "related": []},
            "status": "not_started",
        },
        {
            "id": "FEAT-2",
            "task_type": "feature",
            "title": "Code Quality Standards & Educational Documentation",
            "description": "Establish comprehensive code quality standards with educational documentation for academic repository excellence",
            "priority": "high",
            "effort": {"hours": 35, "story_points": 7, "complexity": "feature"},
            "skills": {
                "primary_role": "Software Architect",
                "required_skills": ["Clean Architecture", "Technical Documentation"],
                "skill_level": "advanced",
            },
            "learning_objectives": {
                "cognitive_level": "create",
                "objectives": ["Implement >90% test coverage standards"],
                "prerequisites": ["Software engineering principles"],
            },
            "acceptance_criteria": [
                {
                    "criterion": "Code quality standards documented and enforced",
                    "testable": True,
                }
            ],
            "definition_of_done": [
                "Quality standards implemented",
                "Educational annotations complete",
            ],
            "dependencies": {"blocks": [], "blocked_by": ["FEAT-1"], "related": []},
            "status": "not_started",
        },
        {
            "id": "FEAT-3",
            "task_type": "feature",
            "title": "GitHub Workflow Optimization & CI/CD",
            "description": "Optimize GitHub workflows for academic research with automated testing, quality gates, and deployment pipelines",
            "priority": "medium",
            "effort": {"hours": 30, "story_points": 6, "complexity": "feature"},
            "skills": {
                "primary_role": "DevOps Engineer",
                "required_skills": ["GitHub Actions", "CI/CD Pipelines"],
                "skill_level": "intermediate",
            },
            "learning_objectives": {
                "cognitive_level": "apply",
                "objectives": ["Automate quality assurance processes"],
                "prerequisites": ["Basic CI/CD knowledge"],
            },
            "acceptance_criteria": [
                {"criterion": "Automated test execution on all PRs", "testable": True}
            ],
            "definition_of_done": [
                "CI/CD pipelines configured",
                "Quality gates active",
            ],
            "dependencies": {"blocks": [], "blocked_by": ["FEAT-2"], "related": []},
            "status": "not_started",
        },
    ]

    return features


def demonstrate_knowledge_graph():
    """Demonstrate knowledge graph algorithms on educational task hierarchies."""

    print("🎓 Knowledge Graph Traversal Demonstration")
    print("   Showcasing graph algorithms on educational task management")
    print()

    # Load existing epics
    epics_dir = Path("./epics")
    graph = AtomicTaskGraph.from_json_directory(epics_dir)

    print(f"📊 Initial Graph State:")
    print(f"   Epics loaded: {len(graph.tasks)}")
    print(f"   Dependencies: {len(graph.dependencies)}")
    print()

    # Add features for EPIC-1
    features = create_sample_features()
    print(f"🏗️  Adding Features for EPIC-1:")

    for feature_data in features:
        # Convert to AtomicTask
        task = AtomicTask(
            id=feature_data["id"],
            task_type=feature_data["task_type"],
            title=feature_data["title"],
            description=feature_data["description"],
            priority=feature_data["priority"],
            effort=feature_data["effort"],
            skills=feature_data["skills"],
            learning_objectives=feature_data["learning_objectives"],
            acceptance_criteria=feature_data["acceptance_criteria"],
            definition_of_done=feature_data["definition_of_done"],
            dependencies=feature_data["dependencies"],
            status=feature_data["status"],
        )
        graph.add_task(task)
        print(f"   ✅ {task.id}: {task.title}")

    print()

    # Demonstrate graph algorithms
    print("🔍 Graph Algorithm Demonstrations:")
    print()

    # 1. Topological Ordering (Dependency Resolution)
    print("1. 📋 Topological Ordering (Dependency Resolution):")
    try:
        order = graph.get_topological_order()
        print(f"   Execution Order: {' → '.join(order)}")
    except Exception as e:
        print(f"   ⚠️  Topological sort failed: {e}")
    print()

    # 2. Critical Path Analysis
    print("2. ⏱️  Critical Path Analysis:")
    try:
        critical_path, total_hours = graph.get_critical_path()
        if critical_path:
            print(f"   Critical Path: {' → '.join(critical_path)}")
            print(f"   Total Duration: {total_hours} hours")
        else:
            print("   No critical path found")
    except Exception as e:
        print(f"   ⚠️  Critical path analysis failed: {e}")
    print()

    # 3. PageRank Importance Analysis
    print("3. 🏆 PageRank Importance Analysis:")
    try:
        importance = graph.calculate_task_importance()
        top_tasks = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]
        print("   Most Important Tasks:")
        for task_id, score in top_tasks:
            if task_id in graph.tasks:
                task_title = graph.tasks[task_id].title
                print(f"     {task_id}: {score:.4f} - {task_title}")
    except Exception as e:
        print(f"   ⚠️  PageRank analysis failed: {e}")
    print()

    # 4. Breadth-First Search (Finding shortest dependency paths)
    print("4. 🔍 Breadth-First Search (Shortest Dependency Path):")
    try:
        # Find path from EPIC-1 to FEAT-3
        if "EPIC-1" in graph.tasks and "FEAT-3" in graph.tasks:
            path = graph.find_shortest_dependency_path("EPIC-1", "FEAT-3")
            if path:
                print(f"   Shortest path EPIC-1 → FEAT-3: {' → '.join(path)}")
            else:
                print("   No path found between EPIC-1 and FEAT-3")
        else:
            print("   Tasks not found for path analysis")
    except Exception as e:
        print(f"   ⚠️  BFS analysis failed: {e}")
    print()

    # 5. Graph Statistics
    print("5. 📈 Graph Statistics:")
    stats = graph.get_task_statistics()
    print(f"   Total Tasks: {stats['total_tasks']}")
    print(f"   Total Dependencies: {stats['total_dependencies']}")
    print(f"   Graph Density: {stats['graph_density']:.3f}")
    print(f"   Total Effort: {stats['total_effort_hours']} hours")
    print()

    # 6. Export Capabilities
    print("6. 📤 Export Demonstration:")
    try:
        mermaid_graph = graph.export_to_mermaid()
        print("   ✅ Mermaid diagram generated")
        print("   📊 Graph visualization ready for documentation")

        # Save to file for inspection
        with open("graph_visualization.mmd", "w") as f:
            f.write(mermaid_graph)
        print("   💾 Saved to: graph_visualization.mmd")
    except Exception as e:
        print(f"   ⚠️  Export failed: {e}")

    print()
    print("🎯 Knowledge Graph Demonstration Complete!")
    print("   Practical algorithms successfully applied to educational task management")


if __name__ == "__main__":
    demonstrate_knowledge_graph()
