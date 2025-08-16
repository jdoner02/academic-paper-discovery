/**
 * Concept Graph Data Types
 *
 * These TypeScript interfaces formally describe the shape of the concept graph
 * data used throughout the frontend. Defining types in a dedicated module keeps
 * them consistent across components and teaches the habit of centralising shared
 * contracts.
 *
 * Why interfaces?  In TypeScript an interface specifies the exact structure an
 * object must satisfy.  By exporting these interfaces we give both humans and
 * the compiler a clear specification of the data our visualisation expects.
 */

/** Represents a single concept extracted from research papers. */
export interface ConceptNode {
  /** Unique identifier, often a normalised concept string. */
  id: string;
  /** Full text of the concept as found in papers. */
  text: string;
  /** Optional shorter label for display purposes. */
  display_text?: string;
  /** Number of times the concept appears in the corpus. */
  frequency: number;
  /** Relevance score in the range [0,1] indicating importance. */
  relevance_score: number;
  /** Domain or research area from which the concept originated. */
  source_domain: string;
  /** List of paper identifiers that mention this concept. */
  source_papers: string[];
  /** Method used to extract the concept (e.g. "LLM" or "keyword"). */
  extraction_method: string;
  /** Visual size of the node in the graph. */
  size?: number;
  /** Colour assigned for domain grouping. */
  color?: string;
  /** Layout coordinates produced by D3's force simulation. */
  x?: number;
  y?: number;
  /** Fixed positions used when a node is dragged. */
  fx?: number | null;
  fy?: number | null;
}

/** Connection between two concepts. */
export interface ConceptLink {
  /** Identifier or node object at the start of the link. */
  source: string | ConceptNode;
  /** Identifier or node object at the end of the link. */
  target: string | ConceptNode;
  /** Strength of the relationship as a float in [0,1]. */
  strength: number;
  /** Descriptive label for the relationship type. */
  relationship_type: string;
  /** Optional weight used by the force simulation. */
  weight?: number;
}

/**
 * The full data set consumed by the graph visualisation.
 * Separating it from component state demonstrates the Single Responsibility
 * Principle (each module has one reason to change).
 */
export interface GraphData {
  nodes: ConceptNode[];
  links: ConceptLink[];
  /** Optional list of domains and any other metadata from the backend. */
  domains?: string[];
  metadata?: unknown;
}

