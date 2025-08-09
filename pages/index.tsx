/**
 * Next.js Index Page - Interactive Research Concept Graph Landing Page
 * 
 * Educational Note:
 * This is the main entry point for the web interface. In Clean Architecture,
 * this belongs to the Interface Layer, handling user interactions and
 * coordinating with the Application Layer use cases.
 * 
 * The page demonstrates:
 * - Next.js SSG (Static Site Generation) for GitHub Pages
 * - Responsive design for academic researchers and developers
 * - Professional presentation of open source project
 * - Interactive D3.js visualization as primary user interface
 * - Real-time exploration of 600+ research concepts across 30 domains
 */

import React from 'react';
import Head from 'next/head';
import InteractiveConceptGraph from '../components/InteractiveConceptGraphNew';

const HomePage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Interactive Research Concept Graph | 600+ Cybersecurity Concepts</title>
        <meta 
          name="description" 
          content="Explore 600+ research concepts across 30 cybersecurity domains through interactive D3.js visualization. Real-time filtering, semantic search, and concept relationship discovery." 
        />
        <meta name="keywords" content="research concepts, cybersecurity, D3.js visualization, graph, semantic search, concept mapping, interactive research, academic exploration" />
        <meta name="author" content="Research Paper Discovery Team" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        
        {/* Open Graph tags for social sharing */}
        <meta property="og:title" content="Interactive Research Concept Graph" />
        <meta property="og:description" content="Explore 600+ cybersecurity research concepts through interactive visualization. Click domains to filter, search concepts in real-time." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://jdoner02.github.io/academic-paper-discovery/" />
        
        {/* Twitter Card tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Interactive Research Concept Graph" />
        <meta name="twitter:description" content="600+ cybersecurity research concepts with interactive D3.js visualization and real-time filtering." />
        
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <InteractiveConceptGraph />
    </>
  );
};

export default HomePage;
