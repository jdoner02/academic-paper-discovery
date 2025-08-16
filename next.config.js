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
  // Only enable static export and path rewriting for production builds.  This
  // block is omitted in development where a Node server provides assets
  // directly.
  ...(isProd && {
    // Produce plain HTML/JS/CSS that can be hosted without a Node server.
    output: 'export',
    // Prefix all built assets with the repository name so that requests such as
    // `/_next/static/...` resolve correctly when the site is served from
    // `/academic-paper-discovery` instead of the domain root.  Without this the
    // browser would request files from the wrong location and show 404 errors
    // like the ones in the problem statement.
    assetPrefix: `/${repoName}/`,
    basePath: `/${repoName}`,
    // Simple cache‑busting strategy: change build ID each deployment so browsers
    // fetch the latest JavaScript bundles.
    generateBuildId: () => Date.now().toString(),
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
  },
};

module.exports = nextConfig;
