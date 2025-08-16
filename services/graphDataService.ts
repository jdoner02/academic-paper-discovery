import { GraphData } from '../types/conceptGraph';

/**
 * fetchGraphData - load the concept graph dataset from a static JSON file.
 *
 * This function encapsulates the data retrieval logic so our React components
 * can focus purely on presentation.  The separation adheres to the Single
 * Responsibility Principle and makes the fetch behaviour easy to unit test.
 *
 * @param url - location of the JSON file relative to the site root.  The default
 *              works for both local development and production deployments.
 * @throws Error when the response is not OK or the payload is malformed.
 * @returns A Promise resolving to the strongly typed GraphData object.
 */
export async function fetchGraphData(
  url = `${process.env.NEXT_PUBLIC_BASE_PATH || ''}/data/concept-graph-data.json`
): Promise<GraphData> {
  // The default URL pulls in an optional NEXT_PUBLIC_BASE_PATH environment
  // variable. Static sites often live inside a subdirectory, so this approach
  // lets the same code fetch the dataset whether the app is served from the
  // domain root or from a nested folder.
  const response = await fetch(url);

  // Guard clause: immediately report network failures to the caller.
  if (!response.ok) {
    throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
  }

  // Parse the JSON payload and let TypeScript check that it matches GraphData.
  const data: GraphData = await response.json();

  // Minimal runtime validation to provide helpful error messages in case the
  // file structure does not meet our expectations.
  if (!Array.isArray(data.nodes) || data.nodes.length === 0) {
    throw new Error('Invalid data structure: nodes array missing or empty');
  }

  // Ensure links is always an array to simplify downstream code.
  data.links = Array.isArray(data.links) ? data.links : [];
  return data;
}

