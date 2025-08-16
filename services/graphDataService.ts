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
  url = '/data/concept-graph-data.json'
): Promise<GraphData> {
  // Perform the HTTP request using the browser's Fetch API.  In a Next.js client
  // component this API is globally available.
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

