/** @type {import('next').NextConfig} */
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
    assetPrefix: '/research-paper-discovery-web',
    basePath: '/research-paper-discovery-web',
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
  },
};

module.exports = nextConfig;
