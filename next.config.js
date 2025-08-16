/** @type {import('next').NextConfig} */
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for static export to GitHub Pages
  },
  // Only enable static export for production builds, not development
  ...(process.env.NODE_ENV === 'production' && {
    output: 'export', // Enable static export for GitHub Pages
    // When hosting from a subdirectory (such as GitHub Pages) Next.js needs to
    // know the mount point so it can generate correct links to scripts and
    // assets. The assetPrefix mirrors the basePath with a trailing slash.
    basePath,
    assetPrefix: `${basePath}/`,
    // Force cache busting for JavaScript chunks
    generateBuildId: () => Date.now().toString()
  }),
  
  // Set custom pages directory for Clean Architecture organization
  pageExtensions: ['tsx', 'ts'],
  
  // Educational Note: Configuration optimized for GitHub Pages deployment
  // - Static export eliminates need for Node.js server
  // - Asset prefix handles GitHub Pages subdirectory routing
  // - Image optimization disabled for static hosting compatibility
  // - Trailing slash ensures consistent routing behavior
  
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
