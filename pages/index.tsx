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
 * - Responsive design for academic researchers and developers
 * - Professional presentation of open source project
 * - Integration with domain concepts through embedded demos
 */

import React from 'react';
import Head from 'next/head';
import LandingPage from '../src/components/LandingPage';

const HomePage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Research Paper Discovery Platform | Open Source Academic Tools</title>
        <meta 
          name="description" 
          content="Transform academic literature into interactive concept maps using Clean Architecture, Test-Driven Development, and modern web technologies. Open source research tools for HRV, TBI, and Apple Watch data analysis." 
        />
        <meta name="keywords" content="research papers, concept extraction, clean architecture, TDD, HRV, TBI, Apple Watch, academic tools, open source" />
        <meta name="author" content="Research Paper Discovery Team" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        
        {/* Open Graph tags for social sharing */}
        <meta property="og:title" content="Research Paper Discovery Platform" />
        <meta property="og:description" content="Transform academic literature into interactive concept maps using modern web technologies." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://jdoner02.github.io/research-paper-discovery-web/" />
        
        {/* Twitter Card tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Research Paper Discovery Platform" />
        <meta name="twitter:description" content="Open source academic research tools with Clean Architecture and TDD." />
        
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <LandingPage />
    </>
  );
};

export default HomePage;
