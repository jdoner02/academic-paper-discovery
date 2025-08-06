/**
 * _error.tsx - Custom Error Page Component
 * 
 * This component handles client-side and server-side errors in the Next.js application.
 * Required by Next.js for proper error handling and routing.
 * 
 * Educational Notes:
 * - Implements Next.js Error Page API for graceful error handling
 * - Provides user-friendly error messages with recovery options
 * - Supports both development and production error display
 * - Follows accessibility best practices with proper semantics
 * 
 * Design Decisions:
 * - Simple, clean design consistent with research application theme
 * - Clear error messaging without exposing sensitive details
 * - Recovery actions to help users continue their research workflow
 * 
 * Use Cases:
 * - 404 Not Found errors when users navigate to invalid pages
 * - 500 Server errors during static generation or API failures
 * - JavaScript runtime errors in the client application
 */

import React from 'react';
import { NextPage } from 'next';
import Head from 'next/head';

interface ErrorProps {
  statusCode: number;
  hasGetInitialPropsRun?: boolean;
  err?: Error;
}

/**
 * Custom error page component for handling application errors
 * 
 * @param statusCode - HTTP status code of the error
 * @param hasGetInitialPropsRun - Whether getInitialProps was executed
 * @param err - Error object (only in development)
 */
const ErrorPage: NextPage<ErrorProps> = ({ statusCode, err }) => {
  const getErrorMessage = (statusCode: number): string => {
    switch (statusCode) {
      case 404:
        return 'The research page you were looking for could not be found.';
      case 500:
        return 'An error occurred while processing your research request.';
      default:
        return 'An unexpected error occurred in the research platform.';
    }
  };

  const getErrorTitle = (statusCode: number): string => {
    switch (statusCode) {
      case 404:
        return 'Page Not Found';
      case 500:
        return 'Internal Server Error';
      default:
        return 'Application Error';
    }
  };

  return (
    <>
      <Head>
        <title>{`${statusCode} - ${getErrorTitle(statusCode)} | Research Paper Discovery`}</title>
        <meta 
          name="description" 
          content={`Error ${statusCode}: ${getErrorMessage(statusCode)}`} 
        />
      </Head>
      
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="text-center">
              <h1 className="text-6xl font-bold text-gray-900 mb-2">
                {statusCode}
              </h1>
              <h2 className="text-2xl font-semibold text-gray-700 mb-4">
                {getErrorTitle(statusCode)}
              </h2>
              <p className="text-gray-600 mb-6">
                {getErrorMessage(statusCode)}
              </p>
              
              {/* Recovery Actions */}
              <div className="space-y-4">
                <button
                  onClick={() => window.history.back()}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                  aria-label="Go back to previous page"
                >
                  ← Go Back
                </button>
                
                <a
                  href="/"
                  className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                  aria-label="Return to home page"
                >
                  🏠 Return Home
                </a>
              </div>
              
              {/* Development Error Details */}
              {process.env.NODE_ENV === 'development' && err && (
                <details className="mt-6 text-left">
                  <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
                    Show Error Details (Development Only)
                  </summary>
                  <pre className="mt-2 text-xs text-red-600 bg-red-50 p-2 rounded overflow-auto">
                    {err.stack}
                  </pre>
                </details>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

/**
 * Get initial props for error page
 * Required by Next.js Error Page API
 */
ErrorPage.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode ?? 404 : 404;
  return { statusCode };
};

export default ErrorPage;
