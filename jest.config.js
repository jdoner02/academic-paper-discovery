const nextJest = require('next/jest')

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files
  dir: './',
})

// Add any custom config to be passed to Jest
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  testPathIgnorePatterns: [
    '<rootDir>/.next/',
    '<rootDir>/node_modules/',
    '<rootDir>/out/',
    '<rootDir>/cli-tool/',
    '<rootDir>/tests/future-integration/',
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/interface/pages/_app.tsx',
    '!src/interface/pages/_document.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    // Higher coverage requirements for domain and application layers
    'src/domain/**/*.ts': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    'src/application/**/*.ts': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
  },
  moduleNameMapper: {
    // Handle module aliases (same as tsconfig.json paths)
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@/domain/(.*)$': '<rootDir>/src/domain/$1',
    '^@/application/(.*)$': '<rootDir>/src/application/$1',
    '^@/infrastructure/(.*)$': '<rootDir>/src/infrastructure/$1',
    '^@/interface/(.*)$': '<rootDir>/src/interface/$1',
    '^@/tests/(.*)$': '<rootDir>/tests/$1',
  },
  testMatch: [
    '**/tests/unit/**/*.(js|jsx|ts|tsx)',
    '**/tests/integration/**/*.(js|jsx|ts|tsx)',
    '**/__tests__/**/*.(js|jsx|ts|tsx)',
    '**/*.(test|spec).(js|jsx|ts|tsx)',
  ],
  testPathIgnorePatterns: [
    '<rootDir>/.next/',
    '<rootDir>/node_modules/',
    '<rootDir>/out/',
    '<rootDir>/cli-tool/',
    '<rootDir>/tests/future-integration/',
  ],
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
  transformIgnorePatterns: [
    '/node_modules/',
    '^.+\\.module\\.(css|sass|scss)$',
  ],
  // Educational Note: Test configuration emphasizes quality over quantity
  // - Higher coverage thresholds for core business logic layers
  // - Module aliases support Clean Architecture organization
  // - Comprehensive file matching for different test patterns
  // - Transform configuration handles Next.js and TypeScript
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(customJestConfig)
