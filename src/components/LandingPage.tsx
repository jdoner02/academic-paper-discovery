/**
 * LandingPage - Professional landing page for the Research Paper Discovery Platform
 * 
 * This component serves as the main public-facing interface for the GitHub Pages deployment.
 * It showcases the project's educational value, technical excellence, and practical utility.
 * 
 * Educational Notes:
 * - Demonstrates comprehensive React component architecture
 * - Shows integration of multiple UI patterns and responsive design
 * - Serves as template for professional open-source project presentation
 * - Combines marketing copy with technical demonstration
 * 
 * Design Decisions:
 * - Multi-section layout for different audience needs (researchers, developers, contributors)
 * - Progressive disclosure of technical complexity
 * - Embedded working demo to show immediate value
 * - Strong call-to-action for open source engagement
 * 
 * Use Cases:
 * - First impression for GitHub Pages visitors
 * - Documentation and onboarding for new contributors
 * - Portfolio showcase for technical architecture skills
 * - Research tool discovery for academic community
 */

import React from 'react';
import Link from 'next/link';
import ConceptExtractionDemo from './ConceptExtractionDemo';

/**
 * Hero section introducing the project and its value proposition
 */
const HeroSection: React.FC = () => (
  <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center">
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          Research Paper Discovery Platform
        </h1>
        <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
          Transform academic literature into interactive concept maps using Clean Architecture, 
          Test-Driven Development, and modern web technologies.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="#demo"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Try Live Demo
          </a>
          <a
            href="https://github.com/jdoner02/academic-paper-discovery"
            target="_blank"
            rel="noopener noreferrer"
            className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
          >
            View Source Code
          </a>
        </div>
      </div>
    </div>
  </section>
);

/**
 * Features section highlighting key technical and functional capabilities
 */
const FeaturesSection: React.FC = () => (
  <section className="py-20 bg-gray-50">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Built for Researchers, Designed for Developers
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          A comprehensive platform combining cutting-edge research methodologies 
          with exemplary software architecture patterns.
        </p>
      </div>
      
      <div className="grid md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="text-blue-600 mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-3">Clean Architecture</h3>
          <p className="text-gray-600">
            Domain-driven design with clear separation of concerns. 
            Business logic independent of frameworks and external dependencies.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="text-green-600 mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-3">Test-Driven Development</h3>
          <p className="text-gray-600">
            Comprehensive test coverage with RED-GREEN-REFACTOR methodology. 
            Every feature built with tests first, ensuring reliability.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="text-purple-600 mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 7.172V5L8 4z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-3">Research-Focused</h3>
          <p className="text-gray-600">
            Specialized for HRV research, TBI studies, and Apple Watch data analysis. 
            Built by researchers, for researchers.
          </p>
        </div>
      </div>
    </div>
  </section>
);

/**
 * Technical stack and architecture overview
 */
const TechnicalSection: React.FC = () => (
  <section className="py-20 bg-white">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Modern Tech Stack
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Built with industry best practices and cutting-edge technologies 
            for performance, maintainability, and educational value.
          </p>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <div className="bg-blue-100 text-blue-600 p-2 rounded-lg mr-4">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span className="text-lg">Next.js 14 with TypeScript for type-safe development</span>
            </div>
            <div className="flex items-center">
              <div className="bg-green-100 text-green-600 p-2 rounded-lg mr-4">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span className="text-lg">Jest testing framework with 100% coverage goals</span>
            </div>
            <div className="flex items-center">
              <div className="bg-purple-100 text-purple-600 p-2 rounded-lg mr-4">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span className="text-lg">D3.js for interactive data visualization</span>
            </div>
            <div className="flex items-center">
              <div className="bg-yellow-100 text-yellow-600 p-2 rounded-lg mr-4">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span className="text-lg">GitHub Actions CI/CD with automated deployment</span>
            </div>
          </div>
        </div>
        
        <div className="bg-gray-900 text-green-400 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <div className="mb-2 text-gray-400">// Clean Architecture Layers</div>
          <div>src/</div>
          <div>├── domain/           <span className="text-gray-400">// Business Logic</span></div>
          <div>│   ├── entities/     <span className="text-gray-400">// Core Objects</span></div>
          <div>│   └── value_objects/</div>
          <div>├── application/      <span className="text-gray-400">// Use Cases</span></div>
          <div>│   ├── use_cases/</div>
          <div>│   └── ports/        <span className="text-gray-400">// Interfaces</span></div>
          <div>├── infrastructure/   <span className="text-gray-400">// External</span></div>
          <div>│   └── repositories/</div>
          <div>└── interface/        <span className="text-gray-400">// UI Components</span></div>
          <div className="mt-4 text-gray-400">// Test Coverage: 33/33 passing ✅</div>
        </div>
      </div>
    </div>
  </section>
);

/**
 * Call-to-action section encouraging contribution and engagement
 */
const CTASection: React.FC = () => (
  <section className="py-20 bg-gray-900 text-white">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 className="text-3xl md:text-4xl font-bold mb-6">
        Contribute to Open Research
      </h2>
      <p className="text-xl mb-8 max-w-3xl mx-auto">
        This project is open source and welcomes contributions from researchers, 
        developers, and anyone passionate about improving academic research tools.
      </p>
      
      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <a
          href="https://github.com/jdoner02/academic-paper-discovery/issues"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-blue-600 hover:bg-blue-700 p-6 rounded-lg transition-colors"
        >
          <h3 className="text-lg font-semibold mb-2">Report Issues</h3>
          <p className="text-blue-200">Found a bug or have a feature request?</p>
        </a>
        
        <a
          href="https://github.com/jdoner02/academic-paper-discovery/pulls"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-green-600 hover:bg-green-700 p-6 rounded-lg transition-colors"
        >
          <h3 className="text-lg font-semibold mb-2">Submit PRs</h3>
          <p className="text-green-200">Contribute code improvements or new features</p>
        </a>
        
        <a
          href="https://github.com/jdoner02/academic-paper-discovery/discussions"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-purple-600 hover:bg-purple-700 p-6 rounded-lg transition-colors"
        >
          <h3 className="text-lg font-semibold mb-2">Join Discussion</h3>
          <p className="text-purple-200">Share ideas and collaborate with the community</p>
        </a>
      </div>
    </div>
  </section>
);

/**
 * Main landing page component combining all sections
 */
const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen">
      <HeroSection />
      <FeaturesSection />
      <TechnicalSection />
      
      {/* Live Demo Section */}
      <section id="demo" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Live Interactive Demo
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the concept extraction functionality in action. 
              This demo showcases the integration between Clean Architecture layers.
            </p>
          </div>
          
          {/* Embed the existing demo component */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <ConceptExtractionDemo />
          </div>
        </div>
      </section>
      
      <CTASection />
    </div>
  );
};

export default LandingPage;
