/**
 * Next.js configuration used by both development and production builds.
 *
 * The configuration is intentionally verbose to teach how each option affects
 * deployment.  Variables declared above the exported object keep related
 * values grouped and make the conditional logic easier to read.
 */

// GitHub Pages serves the site from a subdirectory named after the repository.
// In production we prefix all asset URLs with this directory so that
// `https://<user>.github.io/academic-paper-discovery/` can locate the static
// files.  During local development we keep paths root‑relative for simplicity.
const repoName = 'academic-paper-discovery';
const isProd = process.env.NODE_ENV === 'production';

/** @type {import('next').NextConfig} */
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';

const nextConfig = {
  // Enforces additional React runtime checks which highlight common mistakes.
  reactStrictMode: true,
  // Uses the faster SWC compiler for minification rather than terser.
  swcMinify: true,
  // Ensures every route ends with a trailing slash, matching GitHub Pages
  // behaviour and avoiding duplicate content issues.
  trailingSlash: true,
  images: {
    // GitHub Pages is a static host and cannot run Next.js' dynamic image
    // optimisation pipeline, so images are served as‑is.
    unoptimized: true,
  },
  }),
  
  // Set custom pages directory for Clean Architecture organization
  pageExtensions: ['tsx', 'ts'],
  
  // Educational Note: Configuration optimised for GitHub Pages deployment
  // - Static export eliminates need for a Node.js server.
  // - `assetPrefix` and `basePath` route requests to the correct subdirectory.
  // - Image optimisation is disabled to suit static hosting.
  // - Trailing slashes keep navigation consistent across environments.
  
  // Webpack configuration for Clean Architecture path aliases
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, 'src'),
      '@/domain': require('path').resolve(__dirname, 'src/domain'),
      '@/application': require('path').resolve(__dirname, 'src/application'),
      '@/infrastructure': require('path').resolve(__dirname, 'src/infrastructure'),
      '@/interface': require('path').resolve(__dirname, 'src/interface'),
    };
    
    return config;
  },
  
  // Environment variables for configuration
  env: {
    CUSTOM_KEY: 'my-value',
    // Expose the base path to client-side code so fetches can build URLs that
    // work both locally and in production.
    NEXT_PUBLIC_BASE_PATH: basePath,
  },
};

module.exports = nextConfig;
