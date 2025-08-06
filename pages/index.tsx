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
import ConceptExtractionDemo from '../src/components/ConceptExtractionDemo';

const HomePage: React.FC = () => {
  return <ConceptExtractionDemo />;
};

export default HomePage;
