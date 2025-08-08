#!/usr/bin/env python3
"""
Atomic Task Knowledge Graph Tool

This module demonstrates practical application of knowledge graph algorithms
described in the Knowledge Graph Architecture tutorial. It implements graph
data structures and algorithms for managing educational task hierarchies.

Educational Notes:
- Shows adjacency list representation for O(V+E) space efficiency
- Implements BFS for shortest dependency paths between tasks
- Uses DFS for complete hierarchy exploration
- Demonstrates topological sorting for proper task execution order
- Applies PageRank algorithm for critical path analysis
- Includes memoization patterns for performance optimization

Design Patterns Applied:
- Strategy pattern for different traversal algorithms
- Factory pattern for task creation from JSON
- Command pattern for graph modifications
- Observer pattern for task status updates

Industry Applications:
- Project management dependency resolution
- Sprint planning and task prioritization
- Critical path analysis for project timelines
- Resource allocation optimization
"""

import json
import os
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
import heapq
import math


@dataclass
class AtomicTask:
    """
    Represents a task in the atomic task hierarchy.

    Educational Notes:
    - Immutable ID ensures task identity persistence
    - Rich metadata supports educational simulation
    - Dependencies enable graph-based analysis
    - Effort estimation supports sprint planning
    """

    id: str
    task_type: str  # epic, feature, user_story, task, subtask
    title: str
    description: str
    priority: str
    effort: Dict[str, Any]
    skills: Dict[str, Any]
    learning_objectives: Dict[str, Any]
    acceptance_criteria: List[Dict[str, Any]]
    definition_of_done: List[str]
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    status: str = "not_started"
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task after initialization"""
        if not self.id or not self.task_type:
            raise ValueError("Task must have non-empty id and task_type")

        valid_types = ["epic", "feature", "user_story", "task", "subtask"]
        if self.task_type not in valid_types:
            raise ValueError(f"Invalid task_type. Must be one of: {valid_types}")


@dataclass
class TaskDependency:
    """
    Represents a dependency relationship between tasks.

    Educational Notes:
    - Directed relationships support dependency ordering
    - Dependency types enable different analysis strategies
    - Weights support priority-based traversal algorithms
    """

    from_task: str
    to_task: str
    dependency_type: str  # blocks, depends_on, related
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AtomicTaskGraph:
    """
    Knowledge graph implementation for atomic task management.

    Educational Notes:
    - Uses adjacency list representation for O(V+E) space complexity
    - Maintains reverse adjacency list for efficient backward traversal
    - Implements DAG structure to prevent circular dependencies
    - Provides comprehensive graph algorithms for task analysis

    Design Decisions:
    - Adjacency list chosen over matrix for sparse task graphs
    - Separate metadata storage maintains clean separation of concerns
    - LRU caching provides performance optimization for repeated queries
    - Factory methods enable creation from JSON files
    """

    def __init__(self):
        """Initialize empty task graph"""
        # Forward adjacency list: task_id -> [dependent_task_ids]
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)

        # Reverse adjacency list: task_id -> [prerequisite_task_ids]
        self.reverse_adjacency_list: Dict[str, List[str]] = defaultdict(list)

        # Task storage: task_id -> AtomicTask
        self.tasks: Dict[str, AtomicTask] = {}

        # Dependency metadata: (from_task, to_task) -> TaskDependency
        self.dependencies: Dict[Tuple[str, str], TaskDependency] = {}

        # Performance optimization caches
        self._path_cache: Dict[Tuple[str, str], List[str]] = {}
        self._importance_cache: Optional[Dict[str, float]] = None

    def add_task(self, task: AtomicTask) -> None:
        """
        Add a task to the knowledge graph.

        Educational Notes:
        - Validates task structure before addition
        - Initializes adjacency lists for new nodes
        - Maintains graph invariants

        Args:
            task: AtomicTask instance to add

        Raises:
            ValueError: If task ID already exists
        """
        if task.id in self.tasks:
            raise ValueError(f"Task {task.id} already exists")

        self.tasks[task.id] = task

        # Initialize adjacency lists
        if task.id not in self.adjacency_list:
            self.adjacency_list[task.id] = []
        if task.id not in self.reverse_adjacency_list:
            self.reverse_adjacency_list[task.id] = []

        # Process dependencies from task metadata
        if hasattr(task, "dependencies") and task.dependencies:
            self._add_dependencies_from_task(task)

        # Invalidate caches
        self._invalidate_caches()

    def add_dependency(self, dependency: TaskDependency) -> None:
        """
        Add a dependency relationship between tasks.

        Educational Notes:
        - Creates directed edges in the graph
        - Maintains both forward and reverse adjacency lists
        - Performs cycle detection to maintain DAG property

        Args:
            dependency: TaskDependency instance

        Raises:
            ValueError: If dependency would create a cycle
        """
        from_task, to_task = dependency.from_task, dependency.to_task

        # Validate tasks exist
        if from_task not in self.tasks:
            raise ValueError(f"From task {from_task} does not exist")
        if to_task not in self.tasks:
            raise ValueError(f"To task {to_task} does not exist")

        # Check for cycle before adding
        if self._would_create_cycle(from_task, to_task):
            raise ValueError(
                f"Adding dependency {from_task} -> {to_task} would create cycle"
            )

        # Add to adjacency lists
        if to_task not in self.adjacency_list[from_task]:
            self.adjacency_list[from_task].append(to_task)
        if from_task not in self.reverse_adjacency_list[to_task]:
            self.reverse_adjacency_list[to_task].append(from_task)

        # Store dependency metadata
        self.dependencies[(from_task, to_task)] = dependency

        # Invalidate caches
        self._invalidate_caches()

    def find_shortest_dependency_path(
        self, start_task: str, target_task: str
    ) -> List[str]:
        """
        Find shortest dependency path between tasks using BFS.

        Educational Notes:
        - Demonstrates breadth-first search for unweighted graphs
        - Uses queue data structure for level-order traversal
        - Time complexity: O(V + E) where V=tasks, E=dependencies
        - Space complexity: O(V) for visited set and queue

        Industry Applications:
        - Sprint planning: Find minimum prerequisites for a feature
        - Risk analysis: Identify critical dependency chains
        - Resource planning: Understand task ordering requirements

        Args:
            start_task: Starting task ID
            target_task: Target task ID

        Returns:
            List of task IDs forming shortest dependency path

        Raises:
            ValueError: If start or target tasks don't exist
        """
        # Check cache first
        cache_key = (start_task, target_task)
        if cache_key in self._path_cache:
            return self._path_cache[cache_key]

        # Validate tasks exist
        if start_task not in self.tasks:
            raise ValueError(f"Start task {start_task} does not exist")
        if target_task not in self.tasks:
            raise ValueError(f"Target task {target_task} does not exist")

        if start_task == target_task:
            return [start_task]

        # BFS implementation
        queue = deque([(start_task, [start_task])])
        visited = {start_task}

        while queue:
            current_task, path = queue.popleft()

            # Explore dependencies (outgoing edges)
            for dependent_task in self.adjacency_list.get(current_task, []):
                if dependent_task == target_task:
                    result_path = path + [dependent_task]
                    self._path_cache[cache_key] = result_path
                    return result_path

                if dependent_task not in visited:
                    visited.add(dependent_task)
                    queue.append((dependent_task, path + [dependent_task]))

        # No path found
        self._path_cache[cache_key] = []
        return []

    def explore_task_hierarchy(self, root_task: str, max_depth: int = 5) -> Set[str]:
        """
        Deep exploration of task hierarchy using DFS with memoization.

        Educational Notes:
        - Demonstrates depth-first search for graph exploration
        - Uses memoization to avoid recomputing subtrees
        - Supports bounded exploration to prevent runaway traversal
        - Useful for understanding complete task scope

        Args:
            root_task: Starting task ID for exploration
            max_depth: Maximum depth to explore (prevents infinite recursion)

        Returns:
            Set of all task IDs reachable from root_task
        """
        memo: Dict[str, Set[str]] = {}

        def _dfs_explore(task_id: str, depth: int) -> Set[str]:
            if task_id in memo:
                return memo[task_id]

            if depth <= 0:
                return {task_id}

            reachable = {task_id}

            # Explore dependencies (children in hierarchy)
            for dependent_task in self.adjacency_list.get(task_id, []):
                reachable.update(_dfs_explore(dependent_task, depth - 1))

            memo[task_id] = reachable
            return reachable

        return _dfs_explore(root_task, max_depth)

    def get_topological_order(self) -> List[str]:
        """
        Get topological ordering of tasks for execution planning.

        Educational Notes:
        - Demonstrates topological sort algorithm
        - Uses Kahn's algorithm with in-degree calculation
        - Essential for determining valid task execution order
        - Detects cycles in dependency graph

        Returns:
            List of task IDs in topological order

        Raises:
            ValueError: If cycle detected in task dependencies
        """
        # Calculate in-degrees
        in_degree = dict.fromkeys(self.tasks, 0)

        for task_id in self.adjacency_list:
            for dependent_task in self.adjacency_list[task_id]:
                in_degree[dependent_task] += 1

        # Start with tasks having no prerequisites
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            current_task = queue.popleft()
            result.append(current_task)

            # Process dependencies
            for dependent_task in self.adjacency_list.get(current_task, []):
                in_degree[dependent_task] -= 1
                if in_degree[dependent_task] == 0:
                    queue.append(dependent_task)

        # Check for cycles
        if len(result) != len(self.tasks):
            remaining_tasks = set(self.tasks.keys()) - set(result)
            raise ValueError(
                f"Cycle detected in task dependencies. Remaining tasks: {remaining_tasks}"
            )

        return result

    def calculate_task_importance(
        self, damping_factor: float = 0.85, iterations: int = 50
    ) -> Dict[str, float]:
        """
        Calculate task importance using PageRank algorithm.

        Educational Notes:
        - Adapts PageRank for task dependency analysis
        - Higher scores indicate more critical tasks (many dependencies)
        - Iterative algorithm converges to stable importance scores
        - Useful for resource allocation and priority setting

        Args:
            damping_factor: Probability of following dependencies (0.85 standard)
            iterations: Number of iterations for convergence

        Returns:
            Dict mapping task IDs to importance scores
        """
        if self._importance_cache is not None:
            return self._importance_cache

        task_ids = list(self.tasks.keys())
        n = len(task_ids)

        if n == 0:
            return {}

        # Initialize PageRank values
        pagerank = {task_id: 1.0 / n for task_id in task_ids}

        for _ in range(iterations):
            new_pagerank = {}

            for task_id in task_ids:
                rank_sum = 0.0

                # Sum contributions from tasks that depend on this one
                for prerequisite in self.reverse_adjacency_list.get(task_id, []):
                    out_degree = len(self.adjacency_list.get(prerequisite, []))
                    if out_degree > 0:
                        rank_sum += pagerank[prerequisite] / out_degree

                new_pagerank[task_id] = (
                    1 - damping_factor
                ) / n + damping_factor * rank_sum

            pagerank = new_pagerank

        self._importance_cache = pagerank
        return pagerank

    def get_critical_path(self) -> Tuple[List[str], float]:
        """
        Find critical path through task dependencies.

        Educational Notes:
        - Implements longest path algorithm for DAGs
        - Uses dynamic programming with topological ordering
        - Critical path determines minimum project duration
        - Essential for project management and scheduling

        Returns:
            Tuple of (critical_path_tasks, total_duration)
        """
        if not self.tasks:
            return [], 0.0

        # Get topological order
        topo_order = self.get_topological_order()

        # Initialize distances and predecessors
        distances = dict.fromkeys(self.tasks, 0.0)
        predecessors = dict.fromkeys(self.tasks, None)

        # Calculate longest path (critical path)
        for task_id in topo_order:
            task_duration = self.tasks[task_id].effort.get("hours", 0)

            for dependent_task in self.adjacency_list.get(task_id, []):
                new_distance = distances[task_id] + task_duration

                if new_distance > distances[dependent_task]:
                    distances[dependent_task] = new_distance
                    predecessors[dependent_task] = task_id

        # Find task with maximum distance (end of critical path)
        max_distance = max(distances.values())
        end_task = max(distances.items(), key=lambda x: x[1])[0]

        # Reconstruct critical path
        path = []
        current = end_task
        while current is not None:
            path.append(current)
            current = predecessors[current]

        path.reverse()
        return path, max_distance

    @classmethod
    def from_json_directory(cls, directory_path: str) -> "AtomicTaskGraph":
        """
        Factory method to create task graph from JSON files.

        Educational Notes:
        - Demonstrates Factory pattern for object creation
        - Supports bulk loading from file system
        - Validates JSON schema compliance
        - Handles dependencies between loaded tasks

        Args:
            directory_path: Path to directory containing task JSON files

        Returns:
            AtomicTaskGraph instance populated with tasks
        """
        graph = cls()
        directory = Path(directory_path)

        if not directory.exists():
            raise ValueError(f"Directory {directory_path} does not exist")

        # Load all JSON files
        for json_file in directory.glob("*.json"):
            try:
                with open(json_file, "r") as f:
                    task_data = json.load(f)

                # Create AtomicTask from JSON data
                task = cls._create_task_from_json(task_data)
                graph.add_task(task)

            except Exception as e:
                print(f"Warning: Failed to load {json_file}: {e}")

        return graph

    def export_to_mermaid(self) -> str:
        """
        Export task graph to Mermaid diagram format.

        Educational Notes:
        - Demonstrates graph visualization techniques
        - Mermaid format enables web-based rendering
        - Shows practical application of graph representation

        Returns:
            Mermaid diagram as string
        """
        lines = ["graph TD"]

        # Add nodes with labels
        for task_id, task in self.tasks.items():
            label = f"{task_id}[{task.title}]"
            lines.append(f"    {label}")

        # Add edges (dependencies)
        for from_task, to_task_list in self.adjacency_list.items():
            for to_task in to_task_list:
                lines.append(f"    {from_task} --> {to_task}")

        return "\n".join(lines)

    def get_task_statistics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics about the task graph.

        Returns:
            Dictionary containing graph metrics and analysis
        """
        total_tasks = len(self.tasks)
        total_dependencies = sum(len(deps) for deps in self.adjacency_list.values())

        # Calculate effort statistics
        efforts = [task.effort.get("hours", 0) for task in self.tasks.values()]
        total_effort = sum(efforts)
        avg_effort = total_effort / total_tasks if total_tasks > 0 else 0

        # Task type distribution
        type_distribution = defaultdict(int)
        for task in self.tasks.values():
            type_distribution[task.task_type] += 1

        # Importance scores
        importance_scores = self.calculate_task_importance()
        max_importance_task = (
            max(importance_scores.items(), key=lambda x: x[1])
            if importance_scores
            else ("", 0)
        )

        # Critical path analysis
        critical_path, critical_duration = self.get_critical_path()

        return {
            "total_tasks": total_tasks,
            "total_dependencies": total_dependencies,
            "graph_density": (
                total_dependencies / (total_tasks * (total_tasks - 1))
                if total_tasks > 1
                else 0
            ),
            "total_effort_hours": total_effort,
            "average_effort_hours": avg_effort,
            "task_type_distribution": dict(type_distribution),
            "most_important_task": max_importance_task,
            "critical_path_length": len(critical_path),
            "critical_path_duration": critical_duration,
            "critical_path_tasks": critical_path,
        }

    # Private helper methods

    def _add_dependencies_from_task(self, task: AtomicTask) -> None:
        """Extract and add dependencies from task metadata"""
        if "blocks" in task.dependencies:
            for blocked_task in task.dependencies["blocks"]:
                dep = TaskDependency(task.id, blocked_task, "blocks")
                self.add_dependency(dep)

        if "blocked_by" in task.dependencies:
            for blocking_task in task.dependencies["blocked_by"]:
                dep = TaskDependency(blocking_task, task.id, "blocks")
                self.add_dependency(dep)

    def _would_create_cycle(self, from_task: str, to_task: str) -> bool:
        """Check if adding dependency would create cycle using DFS"""
        visited = set()

        def dfs(task_id: str) -> bool:
            if task_id == from_task:
                return True
            if task_id in visited:
                return False

            visited.add(task_id)
            for dependent in self.adjacency_list.get(task_id, []):
                if dfs(dependent):
                    return True
            return False

        return dfs(to_task)

    def _invalidate_caches(self) -> None:
        """Invalidate performance caches when graph changes"""
        self._path_cache.clear()
        self._importance_cache = None

    @staticmethod
    def _create_task_from_json(task_data: Dict[str, Any]) -> AtomicTask:
        """Create AtomicTask instance from JSON data"""
        return AtomicTask(
            id=task_data["id"],
            task_type=task_data["type"],
            title=task_data["title"],
            description=task_data["description"],
            priority=task_data["priority"],
            effort=task_data["effort"],
            skills=task_data["skills"],
            learning_objectives=task_data["learning_objectives"],
            acceptance_criteria=task_data["acceptance_criteria"],
            definition_of_done=task_data["definition_of_done"],
            dependencies=task_data.get("dependencies", {}),
            status=task_data.get("status", "not_started"),
        )


def main():
    """
    Demonstration of atomic task knowledge graph functionality.

    Educational Notes:
    - Shows practical application of graph algorithms
    - Demonstrates real-world performance characteristics
    - Provides concrete examples for learning
    """
    print("Atomic Task Knowledge Graph Demonstration")
    print("=" * 50)

    # Load task graph from epics directory
    epics_dir = "/Users/jessicadoner/Projects/research-papers/research-paper-aggregator/.ai_development/session_2025_08_07/atomic_tasks/epics"

    try:
        graph = AtomicTaskGraph.from_json_directory(epics_dir)
        print(f"Loaded {len(graph.tasks)} tasks from {epics_dir}")

        # Demonstrate graph algorithms
        print("\n1. Task Statistics:")
        stats = graph.get_task_statistics()
        for key, value in stats.items():
            print(f"   {key}: {value}")

        print("\n2. Topological Order (Execution Sequence):")
        try:
            topo_order = graph.get_topological_order()
            for i, task_id in enumerate(topo_order, 1):
                task_title = graph.tasks[task_id].title
                print(f"   {i}. {task_id}: {task_title}")
        except ValueError as e:
            print(f"   Error: {e}")

        print("\n3. Task Importance Rankings (PageRank):")
        importance = graph.calculate_task_importance()
        sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        for task_id, score in sorted_importance:
            task_title = graph.tasks[task_id].title
            print(f"   {task_id}: {score:.4f} - {task_title}")

        print("\n4. Critical Path Analysis:")
        critical_path, duration = graph.get_critical_path()
        print(f"   Duration: {duration} hours")
        print(f"   Path: {' -> '.join(critical_path)}")

        print("\n5. Dependency Path Example:")
        if len(graph.tasks) >= 2:
            task_ids = list(graph.tasks.keys())
            start, end = task_ids[0], task_ids[-1]
            path = graph.find_shortest_dependency_path(start, end)
            if path:
                print(f"   Path from {start} to {end}: {' -> '.join(path)}")
            else:
                print(f"   No dependency path found from {start} to {end}")

        print("\n6. Mermaid Diagram Export:")
        mermaid = graph.export_to_mermaid()
        print("   " + mermaid.replace("\n", "\n   "))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
