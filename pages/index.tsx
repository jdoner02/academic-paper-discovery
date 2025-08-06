/**
 * Next.js Index Page - Research Paper Discovery Platform Landing Page
 * 
 * Educational Note:
 * This is the main entry point for the web interface. In Clean Architecture,
 * this belongs to the Interface Layer, handling user interactions and
 * coordinating with the Application Layer use cases.
 * 
 * The page demonstrates:
 * - Next.js SSG (Static Site Generation) for GitHub Pages
 * - Responsive design for academic researchers
 * - Integration with domain concepts through use cases
 */

import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-4xl mx-auto px-6 py-12 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          Research Paper Discovery Platform
        </h1>
        
        <p className="text-xl text-gray-600 mb-8">
          Transform academic paper collections into intuitive visual concept maps
        </p>
        
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Coming Soon: Interactive Concept Mapping
          </h2>
          
          <p className="text-gray-600 mb-4">
            We're building an innovative platform that uses machine learning 
            and visualization to help researchers explore literature landscapes 
            without technical barriers.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-gray-800 mb-2">Visual Discovery</h3>
              <p className="text-sm text-gray-600">
                Interactive D3.js concept maps reveal research patterns
              </p>
            </div>
            
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-gray-800 mb-2">Evidence-Based</h3>
              <p className="text-sm text-gray-600">
                Click concepts to see supporting sentences from papers
              </p>
            </div>
            
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-gray-800 mb-2">No Barriers</h3>
              <p className="text-sm text-gray-600">
                Form-based configuration, mobile-responsive design
              </p>
            </div>
          </div>
        </div>
        
        <div className="text-sm text-gray-500">
          <p>Built with Clean Architecture • Test-Driven Development • Educational Focus</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
