"""
Directed Acyclic Graph (DAG) Implementation for Atomic Concept Dependencies

This module implements DAG data structures from scratch to model mathematical and
computer science concept dependencies. Built with mathematical rigor to serve as
both functional code and educational resource.

Mathematical Foundation:
- A DAG is a directed graph G = (V, E) where V is vertices (concepts) and E is edges (dependencies)
- The acyclic property ensures no concept can depend on itself (directly or transitively)
- Topological ordering provides a valid learning sequence respecting all prerequisites

Educational Purpose:
Every implementation decision demonstrates fundamental computer science concepts:
- Graph theory applications in education
- Algorithm design and complexity analysis
- Mathematical proof verification through testing
- Clean Architecture principles in practice
"""

from .concept_node import ConceptNode
from .concept_dag import ConceptDAG
from .relationship_types import RelationshipType, DependencyStrength

__all__ = ["ConceptNode", "ConceptDAG", "RelationshipType", "DependencyStrength"]
