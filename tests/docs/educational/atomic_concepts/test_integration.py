"""
Integration Tests for Atomic Concept DAG System

Tests the complete pipeline from text file parsing through DAG construction
to D3.js visualization export. Verifies mathematical correctness and 
educational utility of the integrated system.

Mathematical Verification:
- Parsing preserves mathematical definitions
- DAG construction maintains all invariants
- Visualization export preserves graph structure
- Learning paths are mathematically valid

Educational Assessment:
- Concept relationships are educationally sound
- Progressive complexity is maintained
- Visualization supports learning objectives
"""

import unittest
import json
import tempfile
from pathlib import Path

from tests import MathematicalProofTestCase, mathematical_property
from docs.educational.atomic_concepts.concept_definitions.text_parser import ConceptDefinitionParser
from docs.educational.atomic_concepts.visualization.dto_converter import ConceptGraphDTO, VisualizationConfig, VisualizationTheme


class TestAtomicConceptIntegration(MathematicalProofTestCase):
    """
    Integration tests for the complete atomic concept system.
    
    Verifies that the entire pipeline from concept definitions to interactive
    visualizations maintains mathematical rigor and educational effectiveness.
    """
    
    def setUp(self):
        """Set up integration test environment."""
        self.parser = ConceptDefinitionParser()
        
        # Create test concept definition content
        self.test_concepts_content = """
[Axiom_A]
type: axiom
dependencies: 
description: Fundamental axiom A
mathematical_definition: Axiom A states that P holds
complexity: fundamental
subject_area: set_theory
cognitive_load: 1

[Concept_B]
type: concept
dependencies: Axiom_A
description: Concept B builds on Axiom A
mathematical_definition: B is defined as Q given P
complexity: basic
subject_area: set_theory
cognitive_load: 2

[Theorem_C]
type: theorem
dependencies: Concept_B, Axiom_A
description: Theorem C follows from A and B
mathematical_definition: If P and Q then R
complexity: intermediate
subject_area: set_theory
cognitive_load: 4

[Advanced_D]
type: concept
dependencies: Theorem_C
description: Advanced concept building on theorem
mathematical_definition: D extends R with additional properties
complexity: advanced
subject_area: set_theory
cognitive_load: 6
"""
        
    @mathematical_property
    def test_complete_pipeline_integration(self):
        """
        Mathematical Proof: Complete pipeline preserves mathematical structure.
        
        Verifies that parsing → DAG construction → visualization maintains
        all mathematical relationships and educational metadata.
        """
        # Step 1: Parse concepts from text
        concepts = self.parser.parse_content(self.test_concepts_content)
        
        # Verify parsing correctness
        self.assertEqual(len(concepts), 4, "Should parse exactly 4 concepts")
        
        concept_names = {c.name for c in concepts}
        expected_names = {"Axiom_A", "Concept_B", "Theorem_C", "Advanced_D"}
        self.assertEqual(concept_names, expected_names, "All concepts should be parsed")
        
        # Step 2: Build DAG from concepts
        dag = self.parser.build_dag_from_concepts(concepts)
        
        # Verify DAG construction correctness
        self.assertEqual(dag.node_count, 4, "DAG should contain all 4 concepts")
        self.assertEqual(dag.edge_count, 4, "DAG should have 4 dependency edges")
        
        # Verify mathematical properties are preserved
        self.assertTrue("Axiom_A" in dag, "Axiom A should be in DAG")
        self.assertTrue(dag["Axiom_A"].is_axiom, "Axiom A should be recognized as axiom")
        
        # Step 3: Verify topological ordering
        topo_order = dag.topological_sort()
        
        # Mathematical property: Axiom comes first
        self.assertEqual(topo_order[0], "Axiom_A", "Axiom should come first in learning order")
        
        # Mathematical property: Dependencies are respected
        axiom_pos = topo_order.index("Axiom_A")
        concept_b_pos = topo_order.index("Concept_B")
        theorem_c_pos = topo_order.index("Theorem_C")
        advanced_d_pos = topo_order.index("Advanced_D")
        
        self.assertLess(axiom_pos, concept_b_pos, "Axiom A before Concept B")
        self.assertLess(concept_b_pos, theorem_c_pos, "Concept B before Theorem C")
        self.assertLess(theorem_c_pos, advanced_d_pos, "Theorem C before Advanced D")
        
        # Step 4: Create visualization DTO
        config = VisualizationConfig(theme=VisualizationTheme.MATHEMATICAL)
        dto = ConceptGraphDTO(dag, config)
        viz_data = dto.to_d3_format()
        
        # Verify visualization structure
        self.assertIn("nodes", viz_data, "Visualization should have nodes array")
        self.assertIn("links", viz_data, "Visualization should have links array")
        self.assertIn("metadata", viz_data, "Visualization should have metadata")
        
        # Mathematical property: Node count preservation
        self.assertEqual(len(viz_data["nodes"]), 4, "All concepts should be in visualization")
        
        # Mathematical property: Edge count preservation  
        self.assertEqual(len(viz_data["links"]), 4, "All dependencies should be in visualization")
        
        # Step 5: Verify learning path generation
        learning_path = dag.get_learning_path("Advanced_D")
        expected_path = ["Axiom_A", "Concept_B", "Theorem_C", "Advanced_D"]
        self.assertEqual(learning_path, expected_path, "Learning path should follow dependency order")
        
    @mathematical_property
    def test_mathematical_definitions_preservation(self):
        """
        Mathematical Proof: Mathematical definitions are preserved through pipeline.
        
        Verifies that formal mathematical content maintains precision and
        accessibility throughout the processing pipeline.
        """
        # Parse and build DAG
        concepts = self.parser.parse_content(self.test_concepts_content)
        dag = self.parser.build_dag_from_concepts(concepts)
        
        # Check specific mathematical definitions are preserved
        axiom_a = dag["Axiom_A"]
        self.assertEqual(axiom_a.mathematical_definition, "Axiom A states that P holds")
        self.assertEqual(axiom_a.type, "axiom")
        self.assertEqual(axiom_a.complexity_level, "fundamental")
        
        theorem_c = dag["Theorem_C"]
        self.assertEqual(theorem_c.mathematical_definition, "If P and Q then R")
        self.assertEqual(theorem_c.type, "theorem")
        self.assertEqual(theorem_c.complexity_level, "intermediate")
        
        # Verify definitions appear in visualization
        dto = ConceptGraphDTO(dag)
        viz_data = dto.to_d3_format()
        
        # Find nodes in visualization data
        axiom_node = next(n for n in viz_data["nodes"] if n["id"] == "Axiom_A")
        theorem_node = next(n for n in viz_data["nodes"] if n["id"] == "Theorem_C")
        
        self.assertEqual(axiom_node["mathematical_definition"], "Axiom A states that P holds")
        self.assertEqual(theorem_node["mathematical_definition"], "If P and Q then R")
        
    @mathematical_property
    def test_educational_progression_validation(self):
        """
        Mathematical Proof: Educational progression follows cognitive load principles.
        
        Verifies that complexity levels and cognitive loads create valid
        learning progressions that respect educational psychology principles.
        """
        concepts = self.parser.parse_content(self.test_concepts_content)
        dag = self.parser.build_dag_from_concepts(concepts)
        
        # Get learning path for most advanced concept
        learning_path = dag.get_learning_path("Advanced_D")
        
        # Mathematical property: Cognitive load should generally increase
        cognitive_loads = [dag[concept].cognitive_load for concept in learning_path]
        
        # Verify progression is educationally sound
        self.assertEqual(cognitive_loads, [1, 2, 4, 6], "Cognitive load should increase progressively")
        
        # Mathematical property: Complexity levels should progress logically
        complexity_levels = [dag[concept].complexity_level for concept in learning_path]
        expected_complexities = ["fundamental", "basic", "intermediate", "advanced"]
        self.assertEqual(complexity_levels, expected_complexities, 
                        "Complexity should progress from fundamental to advanced")
        
        # Educational property: Prerequisites should have lower cognitive load
        for concept in dag.concepts:
            for prereq_name in concept.prerequisites:
                prereq = dag[prereq_name]
                self.assertLessEqual(prereq.cognitive_load, concept.cognitive_load,
                                   f"Prerequisite {prereq_name} should have cognitive load ≤ {concept.name}")
                
    def test_visualization_json_export(self):
        """Test complete visualization export to JSON file."""
        # Parse and create visualization
        concepts = self.parser.parse_content(self.test_concepts_content)
        dag = self.parser.build_dag_from_concepts(concepts)
        dto = ConceptGraphDTO(dag)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
            
        try:
            dto.export_to_json(temp_path)
            
            # Verify file was created and contains valid JSON
            self.assertTrue(temp_path.exists(), "JSON file should be created")
            
            with open(temp_path, 'r') as f:
                exported_data = json.load(f)
                
            # Verify structure
            self.assertIn("nodes", exported_data)
            self.assertIn("links", exported_data)
            self.assertIn("metadata", exported_data)
            
            # Verify content
            self.assertEqual(len(exported_data["nodes"]), 4)
            self.assertEqual(len(exported_data["links"]), 4)
            
        finally:
            # Cleanup
            if temp_path.exists():
                temp_path.unlink()
                
    @mathematical_property
    def test_real_mathematical_concepts(self):
        """
        Test with actual mathematical foundation concepts from our example file.
        
        Demonstrates the system working with real mathematical content.
        """
        # Use the actual mathematical foundations file
        foundations_path = Path(__file__).parent.parent.parent.parent / "concept_definitions" / "mathematical_foundations.txt"
        
        if foundations_path.exists():
            # Parse the real mathematical concepts
            concepts = self.parser.parse_file(foundations_path)
            
            # Verify we got substantial content
            self.assertGreater(len(concepts), 5, "Should parse multiple real concepts")
            
            # Build DAG and verify mathematical structure
            dag = self.parser.build_dag_from_concepts(concepts)
            
            # Mathematical property: Should have axioms as foundations
            axioms = dag.get_axioms()
            self.assertGreater(len(axioms), 0, "Should have at least one axiom")
            
            # Mathematical property: Should have valid topological ordering
            topo_order = dag.topological_sort()
            self.assertEqual(len(topo_order), len(concepts), "All concepts should be in topological order")
            
            # Educational property: Should have progression of complexity
            complexity_counts = {}
            for concept in concepts:
                complexity = concept.complexity_level
                complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
                
            self.assertIn("fundamental", complexity_counts, "Should have fundamental concepts")
            
            # Create visualization for real mathematical concepts
            dto = ConceptGraphDTO(dag, VisualizationConfig(theme=VisualizationTheme.MATHEMATICAL))
            viz_data = dto.to_d3_format()
            
            # Verify visualization can handle real mathematical content
            self.assertEqual(len(viz_data["nodes"]), len(concepts), "All real concepts should be visualizable")
            self.assertGreater(len(viz_data["links"]), 0, "Should have dependency relationships")
            
            # Mathematical property: Metadata should reflect actual graph structure
            metadata = viz_data["metadata"]
            self.assertEqual(metadata["total_concepts"], dag.node_count)
            self.assertEqual(metadata["total_dependencies"], dag.edge_count)
            self.assertGreater(metadata["max_depth"], 0, "Should have non-trivial dependency depth")
            
    def test_learning_path_visualization(self):
        """Test specialized learning path visualization."""
        concepts = self.parser.parse_content(self.test_concepts_content)
        dag = self.parser.build_dag_from_concepts(concepts)
        dto = ConceptGraphDTO(dag)
        
        # Create learning path visualization for advanced concept
        path_viz = dto.create_learning_path_visualization("Advanced_D")
        
        # Verify learning path structure
        self.assertIn("learning_path", path_viz)
        path_info = path_viz["learning_path"]
        
        self.assertEqual(path_info["target_concept"], "Advanced_D")
        self.assertEqual(path_info["path_length"], 4)
        self.assertEqual(path_info["concepts"], ["Axiom_A", "Concept_B", "Theorem_C", "Advanced_D"])
        
        # Verify visual highlighting
        highlighted_nodes = [n for n in path_viz["nodes"] if n.get("in_learning_path", False)]
        self.assertEqual(len(highlighted_nodes), 4, "All path concepts should be highlighted")
        
        dimmed_nodes = [n for n in path_viz["nodes"] if not n.get("in_learning_path", False)]
        self.assertEqual(len(dimmed_nodes), 0, "No nodes should be dimmed in this simple example")
        
    def test_error_handling_integration(self):
        """Test error handling throughout the integrated pipeline."""
        # Test malformed concept definition
        malformed_content = """
[Invalid_Concept]
type: invalid_type
dependencies: NonExistent_Concept
description: This should fail
"""
        
        with self.assertRaises(Exception):
            concepts = self.parser.parse_content(malformed_content)
            self.parser.build_dag_from_concepts(concepts)
            
        # Test missing dependency
        missing_dep_content = """
[Valid_Concept]
type: concept
dependencies: Missing_Prerequisite
description: This references a missing concept
complexity: basic
subject_area: set_theory
"""
        
        concepts = self.parser.parse_content(missing_dep_content)
        with self.assertRaises(Exception):
            self.parser.build_dag_from_concepts(concepts)


if __name__ == '__main__':
    unittest.main()
