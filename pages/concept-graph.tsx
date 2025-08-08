/**
 * Concept Graph Page - Interactive visualization of research concepts
 * 
 * This page provides the main interface for exploring research concepts
 * through an interactive graph visualization. Users can filter, search,
 * and navigate through research domains and concept relationships.
 * 
 * Educational Notes:
 * - Demonstrates Next.js page structure and routing
 * - Shows integration of complex React components with data visualization
 * - Implements responsive design for research exploration workflows
 * - Serves as example of educational interface design
 * 
 * Design Decisions:
 * - Full-screen layout for immersive graph exploration
 * - Clean meta tags for SEO and social sharing
 * - Accessible design following WCAG guidelines
 * - Professional presentation suitable for academic use
 */

import React from 'react';
import Head from 'next/head';
import InteractiveConceptGraph from '../src/components/InteractiveConceptGraph';

const ConceptGraphPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Interactive Concept Graph | Research Paper Discovery Platform</title>
        <meta 
          name="description" 
          content="Explore research concepts through an interactive graph visualization. Discover connections between papers, domains, and research areas in cybersecurity, quantum computing, and infrastructure security." 
        />
        <meta name="keywords" content="concept graph, research visualization, academic networks, cybersecurity research, interactive exploration" />
        <meta name="author" content="Research Paper Discovery Team" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        
        {/* Open Graph tags for social sharing */}
        <meta property="og:title" content="Interactive Research Concept Graph" />
        <meta property="og:description" content="Explore research concepts through beautiful interactive visualization." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://jdoner02.github.io/research-paper-discovery-web/concept-graph" />
        
        {/* Twitter Card tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Interactive Research Concept Graph" />
        <meta name="twitter:description" content="Beautiful and intuitive concept graph for exploring research connections." />
        
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <InteractiveConceptGraph />
    </>
  );
};

export default ConceptGraphPage;
