import { useState } from 'react';
import { ExtractConceptsUseCase } from '../application/use_cases/ExtractConceptsUseCase';

/**
 * ConceptExtractionDemo - React component demonstrating the concept extraction functionality.
 * 
 * This component provides a simple interface for testing the ExtractConceptsUseCase
 * and serves as a proof-of-concept for the larger visualization system.
 * 
 * Educational Notes:
 * - Shows integration between React components and Clean Architecture use cases
 * - Demonstrates dependency injection patterns in React
 * - Provides basic state management for async operations
 * - Serves as foundation for more complex D3.js visualizations
 * 
 * Design Decisions:
 * - Simple form-based interface for quick testing
 * - Basic error handling and loading states
 * - JSON display of results for development/debugging
 * - Responsive design with Tailwind CSS
 */
export default function ConceptExtractionDemo() {
  const [paperId, setPaperId] = useState('');
  const [results, setResults] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // For demo purposes, create mock implementations
  // In a real app, these would come from dependency injection container
  const mockPaperRepository = {
    findById: async (id: string) => ({
      id,
      title: 'Sample Research Paper',
      authors: ['Dr. Smith', 'Dr. Johnson'],
      abstract: 'This is a sample paper for demonstration purposes.',
    }),
    findAll: async () => [],
    findByQuery: async () => [],
    findWithSufficientContent: async () => [],
  };

  const mockConceptRepository = {
    saveConcepts: async () => {},
    findConceptsByPaperIds: async () => [],
    findRootConcepts: async () => [],
    findConceptHierarchies: async () => [],
    findConceptsByEmbeddingSimilarity: async () => [],
  };

  const mockEmbeddingService = {
    generateEmbedding: async () => ({ dimensions: [0.1, 0.2, 0.3] }),
    calculateSimilarity: async () => 0.8,
    batchGenerateEmbeddings: async () => [],
  };

  const useCase = new ExtractConceptsUseCase(
    mockPaperRepository as any,
    mockConceptRepository as any,
    mockEmbeddingService as any
  );

  const handleExtractConcepts = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!paperId.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const result = await useCase.execute({ paperId: paperId.trim() });
      setResults(result);
      
      if (!result.success) {
        setError(result.error || 'Unknown error occurred');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Research Paper Concept Extraction
          </h1>
          <p className="text-lg text-gray-600">
            Interactive demonstration of concept extraction from research papers
          </p>
        </div>

        {/* Extraction Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleExtractConcepts} className="space-y-4">
            <div>
              <label htmlFor="paperId" className="block text-sm font-medium text-gray-700 mb-2">
                Paper ID
              </label>
              <input
                id="paperId"
                type="text"
                value={paperId}
                onChange={(e) => setPaperId(e.target.value)}
                placeholder="Enter paper ID (e.g., sample-paper-123)"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                disabled={isLoading}
              />
            </div>
            
            <button
              type="submit"
              disabled={isLoading || !paperId.trim()}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Extracting Concepts...' : 'Extract Concepts'}
            </button>
          </form>
        </div>

        {/* Results Section */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-8">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Error
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  {error}
                </div>
              </div>
            </div>
          </div>
        )}

        {results && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Extraction Results
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-50 p-3 rounded-md">
                <div className="text-sm font-medium text-gray-500">Status</div>
                <div className={`text-lg font-semibold ${results.success ? 'text-green-600' : 'text-red-600'}`}>
                  {results.success ? 'Success' : 'Failed'}
                </div>
              </div>
              
              <div className="bg-gray-50 p-3 rounded-md">
                <div className="text-sm font-medium text-gray-500">Processing Time</div>
                <div className="text-lg font-semibold text-gray-900">
                  {results.processingTime.toFixed(2)}ms
                </div>
              </div>
              
              <div className="bg-gray-50 p-3 rounded-md">
                <div className="text-sm font-medium text-gray-500">Concepts Found</div>
                <div className="text-lg font-semibold text-gray-900">
                  {results.concepts.length}
                </div>
              </div>
            </div>

            {/* JSON Display for Development */}
            <details className="mt-4">
              <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
                View Raw Results (Development)
              </summary>
              <pre className="mt-2 p-4 bg-gray-100 rounded-md text-xs overflow-auto">
                {JSON.stringify(results, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {/* Coming Soon Section */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-md p-4">
          <h3 className="text-sm font-medium text-blue-800 mb-2">
            Coming Soon
          </h3>
          <ul className="text-sm text-blue-700 list-disc list-inside space-y-1">
            <li>Interactive D3.js concept hierarchy visualization</li>
            <li>Concept similarity mapping and clustering</li>
            <li>Evidence sentence highlighting and tooltips</li>
            <li>Export capabilities for research workflows</li>
          </ul>
        </div>

      </div>
    </div>
  );
}
