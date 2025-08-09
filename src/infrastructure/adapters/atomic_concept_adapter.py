"""
Atomic Concept Integration Adapter

Bridges mathematical atomic concepts with research paper con                        domain_concepts = []
                        for concept_data in concepts_data.get('concepts', []):
                            # Simple concept creation without ConceptId dependency
                            concept = type('Concept', (), {
                                'id': concept_data.get('id', ''),
                                'name': concept_data.get('name', ''),
                                'description': concept_data.get('description', ''),
                                'domain': concept_data.get('domain', domain_dir.name),
                                'confidence': concept_data.get('confidence', 0.5)
                            })()
                            domain_concepts.append(concept)ction workflow.
Demonstrates Adapter Pattern for integrating foundational mathematical knowledge
with domain-specific research concepts.

Educational Purpose:
- Shows how to integrate different concept representation systems
- Demonstrates Clean Architecture adapter implementation
- Bridges abstract mathematical foundations with concrete research applications
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from pathlib import Path
import json
import logging

# Use local imports that exist
from src.domain.entities.concept import Concept
from src.infrastructure.knowledge_graph import KnowledgeGraph, Entity, Relationship


@dataclass
class AtomicConceptMapping:
    """Maps atomic mathematical concepts to research domain concepts."""

    atomic_concept_id: str
    research_concepts: List[str]
    confidence_score: float
    mapping_type: str  # 'prerequisite', 'application', 'foundation'


class AtomicConceptAdapter:
    """
    Adapter that integrates atomic mathematical concepts with research concept extraction.

    Educational Concepts Demonstrated:
    - Adapter Pattern for system integration
    - Domain-Driven Design with bounded contexts
    - Knowledge graph integration patterns
    - Type safety with dataclasses and type hints
    """

    def __init__(
        self,
        atomic_concepts_path: Path,
        research_concepts_path: Path,
        knowledge_graph: KnowledgeGraph,
    ):
        self.atomic_concepts_path = atomic_concepts_path
        self.research_concepts_path = research_concepts_path
        self.knowledge_graph = knowledge_graph
        self.logger = logging.getLogger(__name__)

        # Cache for loaded concepts
        self._atomic_concepts_cache: Dict[str, Dict] = {}
        self._research_concepts_cache: Dict[str, List[Concept]] = {}
        self._mappings_cache: List[AtomicConceptMapping] = []

    def load_atomic_concepts(self) -> Dict[str, Dict]:
        """Load atomic mathematical concepts from JSON definitions."""
        if self._atomic_concepts_cache:
            return self._atomic_concepts_cache

        atomic_concepts = {}

        # Recursively find all JSON concept files
        for json_file in self.atomic_concepts_path.rglob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    concept_data = json.load(f)
                    concept_id = concept_data.get("id", json_file.stem)
                    atomic_concepts[concept_id] = concept_data

                self.logger.info(f"Loaded atomic concept: {concept_id}")

            except Exception as e:
                self.logger.error(f"Error loading {json_file}: {e}")

        self._atomic_concepts_cache = atomic_concepts
        return atomic_concepts

    def load_research_concepts(self) -> Dict[str, List[Concept]]:
        """Load research domain concepts from extracted data."""
        if self._research_concepts_cache:
            return self._research_concepts_cache

        research_concepts = {}

        # Load concepts from static_data directory
        for domain_dir in self.research_concepts_path.iterdir():
            if domain_dir.is_dir():
                concepts_file = domain_dir / "concepts.json"
                if concepts_file.exists():
                    try:
                        with open(concepts_file, "r", encoding="utf-8") as f:
                            concepts_data = json.load(f)

                        domain_concepts = []
                        for concept_data in concepts_data.get("concepts", []):
                            concept = Concept(
                                id=ConceptId(concept_data.get("id", "")),
                                name=concept_data.get("name", ""),
                                description=concept_data.get("description", ""),
                                domain=concept_data.get("domain", domain_dir.name),
                                confidence=concept_data.get("confidence", 0.5),
                            )
                            domain_concepts.append(concept)

                        research_concepts[domain_dir.name] = domain_concepts
                        self.logger.info(
                            f"Loaded {len(domain_concepts)} concepts from {domain_dir.name}"
                        )

                    except Exception as e:
                        self.logger.error(
                            f"Error loading concepts from {concepts_file}: {e}"
                        )

        self._research_concepts_cache = research_concepts
        return research_concepts

    def create_concept_mappings(self) -> List[AtomicConceptMapping]:
        """Create mappings between atomic and research concepts."""
        if self._mappings_cache:
            return self._mappings_cache

        atomic_concepts = self.load_atomic_concepts()
        research_concepts = self.load_research_concepts()
        mappings = []

        # Mathematical foundations mapping rules
        foundation_mappings = {
            "zfc_axiom_extensionality": [
                "set_theory",
                "formal_verification",
                "type_systems",
            ],
            "zfc_axiom_empty_set": ["null_values", "boundary_conditions", "edge_cases"],
            "zfc_axiom_union": ["data_aggregation", "merge_operations", "union_types"],
            "zfc_axiom_pairing": [
                "key_value_pairs",
                "ordered_pairs",
                "tuple_structures",
            ],
            "predicate_logic": [
                "boolean_logic",
                "conditional_statements",
                "formal_verification",
            ],
            "quantified_logic": [
                "loop_invariants",
                "universal_properties",
                "existence_proofs",
            ],
        }

        for atomic_id, atomic_concept in atomic_concepts.items():
            # Direct mapping based on mathematical foundations
            if atomic_id in foundation_mappings:
                related_terms = foundation_mappings[atomic_id]

                for domain_name, domain_concepts in research_concepts.items():
                    matching_concepts = []

                    for concept in domain_concepts:
                        # Check if any related terms appear in concept description
                        concept_text = f"{concept.name} {concept.description}".lower()

                        for term in related_terms:
                            if term.replace("_", " ") in concept_text:
                                matching_concepts.append(concept.name)
                                break

                    if matching_concepts:
                        mapping = AtomicConceptMapping(
                            atomic_concept_id=atomic_id,
                            research_concepts=matching_concepts,
                            confidence_score=0.8,
                            mapping_type="foundation",
                        )
                        mappings.append(mapping)

            # Prerequisite relationship mapping
            prerequisites = atomic_concept.get("prerequisites", [])
            if prerequisites:
                for domain_name, domain_concepts in research_concepts.items():
                    prereq_matches = []

                    for concept in domain_concepts:
                        concept_lower = concept.name.lower()
                        for prereq in prerequisites:
                            if prereq.replace("_", " ") in concept_lower:
                                prereq_matches.append(concept.name)

                    if prereq_matches:
                        mapping = AtomicConceptMapping(
                            atomic_concept_id=atomic_id,
                            research_concepts=prereq_matches,
                            confidence_score=0.6,
                            mapping_type="prerequisite",
                        )
                        mappings.append(mapping)

        self._mappings_cache = mappings
        self.logger.info(f"Created {len(mappings)} concept mappings")
        return mappings

    def integrate_with_knowledge_graph(self) -> None:
        """Add atomic concepts and mappings to the knowledge graph."""
        atomic_concepts = self.load_atomic_concepts()
        mappings = self.create_concept_mappings()

        # Add atomic concepts as entities
        for concept_id, concept_data in atomic_concepts.items():
            entity = Entity(
                id=concept_id,
                name=concept_data.get("name", concept_id),
                entity_type="atomic_mathematical_concept",
                metadata={
                    "formal_statement": concept_data.get("formal_statement", ""),
                    "informal_description": concept_data.get(
                        "informal_description", ""
                    ),
                    "level": concept_data.get("level", "undergraduate"),
                    "domain": concept_data.get("domain", "mathematics"),
                    "subdomain": concept_data.get("subdomain", ""),
                    "axiom": concept_data.get("type") == "axiom",
                },
            )

            self.knowledge_graph.add_entity(entity)

        # Add prerequisite relationships between atomic concepts
        for concept_id, concept_data in atomic_concepts.items():
            prerequisites = concept_data.get("prerequisites", [])
            for prereq in prerequisites:
                if prereq in atomic_concepts:
                    relationship = Relationship(
                        from_entity=prereq,
                        to_entity=concept_id,
                        relationship_type="mathematical_prerequisite",
                        metadata={"strength": 0.9},
                    )
                    self.knowledge_graph.add_relationship(relationship)

        # Add mappings to research concepts
        for mapping in mappings:
            for research_concept in mapping.research_concepts:
                relationship = Relationship(
                    from_entity=mapping.atomic_concept_id,
                    to_entity=research_concept,
                    relationship_type=f"atomic_{mapping.mapping_type}",
                    metadata={
                        "confidence": mapping.confidence_score,
                        "mapping_type": mapping.mapping_type,
                    },
                )
                self.knowledge_graph.add_relationship(relationship)

        self.logger.info("Successfully integrated atomic concepts with knowledge graph")

    def get_foundational_concepts_for_research(self, research_domain: str) -> List[str]:
        """Get atomic mathematical concepts that are foundational for a research domain."""
        mappings = self.create_concept_mappings()
        research_concepts = self.load_research_concepts()

        if research_domain not in research_concepts:
            return []

        foundational_concepts = set()
        domain_concept_names = {c.name for c in research_concepts[research_domain]}

        for mapping in mappings:
            if mapping.mapping_type == "foundation":
                # Check if any research concepts in this domain match the mapping
                if any(rc in domain_concept_names for rc in mapping.research_concepts):
                    foundational_concepts.add(mapping.atomic_concept_id)

        return list(foundational_concepts)

    def get_learning_path(self, target_research_concept: str) -> List[str]:
        """Generate a learning path from atomic concepts to research concept."""
        mappings = self.create_concept_mappings()
        atomic_concepts = self.load_atomic_concepts()

        # Find atomic concepts related to target
        related_atomic = []
        for mapping in mappings:
            if target_research_concept in mapping.research_concepts:
                related_atomic.append(mapping.atomic_concept_id)

        # Use knowledge graph to find prerequisite chain
        learning_path = []
        for atomic_id in related_atomic:
            if atomic_id in atomic_concepts:
                # Get all prerequisites recursively
                prereqs = self._get_all_prerequisites(atomic_id, atomic_concepts)
                learning_path.extend(prereqs)
                learning_path.append(atomic_id)

        # Remove duplicates while preserving order
        seen = set()
        ordered_path = []
        for concept in learning_path:
            if concept not in seen:
                ordered_path.append(concept)
                seen.add(concept)

        return ordered_path

    def _get_all_prerequisites(
        self, concept_id: str, atomic_concepts: Dict[str, Dict]
    ) -> List[str]:
        """Recursively get all prerequisites for a concept."""
        if concept_id not in atomic_concepts:
            return []

        prerequisites = []
        concept_prereqs = atomic_concepts[concept_id].get("prerequisites", [])

        for prereq in concept_prereqs:
            if prereq in atomic_concepts:
                # Recursively get prerequisites of prerequisites
                sub_prereqs = self._get_all_prerequisites(prereq, atomic_concepts)
                prerequisites.extend(sub_prereqs)
                prerequisites.append(prereq)

        return prerequisites

    def export_integration_report(self) -> Dict:
        """Export a comprehensive report of the integration."""
        atomic_concepts = self.load_atomic_concepts()
        research_concepts = self.load_research_concepts()
        mappings = self.create_concept_mappings()

        # Calculate statistics
        total_atomic = len(atomic_concepts)
        total_research_domains = len(research_concepts)
        total_research_concepts = sum(
            len(concepts) for concepts in research_concepts.values()
        )
        total_mappings = len(mappings)

        mapping_by_type = {}
        for mapping in mappings:
            mapping_type = mapping.mapping_type
            if mapping_type not in mapping_by_type:
                mapping_by_type[mapping_type] = 0
            mapping_by_type[mapping_type] += 1

        report = {
            "integration_summary": {
                "atomic_concepts": total_atomic,
                "research_domains": total_research_domains,
                "research_concepts": total_research_concepts,
                "total_mappings": total_mappings,
                "mapping_types": mapping_by_type,
            },
            "atomic_concepts": list(atomic_concepts.keys()),
            "research_domains": list(research_concepts.keys()),
            "mappings": [
                {
                    "atomic_concept": m.atomic_concept_id,
                    "research_concepts": m.research_concepts,
                    "confidence": m.confidence_score,
                    "type": m.mapping_type,
                }
                for m in mappings
            ],
        }

        return report


# Educational Usage Example
def create_concept_integration_demo():
    """
    Demonstration of how to use the Atomic Concept Adapter.

    Educational Purpose:
    - Shows practical application of Adapter Pattern
    - Demonstrates integration of different knowledge systems
    - Illustrates Clean Architecture in practice
    """
    from pathlib import Path

    # Initialize paths
    atomic_path = Path("concept_definitions")
    research_path = Path("static_data")

    # Create knowledge graph
    kg = KnowledgeGraph()

    # Create and use adapter
    adapter = AtomicConceptAdapter(atomic_path, research_path, kg)

    # Perform integration
    adapter.integrate_with_knowledge_graph()

    # Generate learning paths
    cybersecurity_foundations = adapter.get_foundational_concepts_for_research(
        "cybersecurity"
    )
    crypto_learning_path = adapter.get_learning_path("quantum_cryptography")

    # Export report
    integration_report = adapter.export_integration_report()

    return {
        "cybersecurity_foundations": cybersecurity_foundations,
        "crypto_learning_path": crypto_learning_path,
        "integration_report": integration_report,
    }


if __name__ == "__main__":
    # Run demonstration
    demo_results = create_concept_integration_demo()
    print("Atomic Concept Integration Demo Complete!")
    print(
        f"Integration Report: {demo_results['integration_report']['integration_summary']}"
    )
