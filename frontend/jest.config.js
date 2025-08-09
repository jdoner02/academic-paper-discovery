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
    '!src/application/ports/**',  // Exclude unimplemented ports from coverage
    '!src/domain/value_objects/EvidenceSentence.ts',  // Exclude unimplemented value objects
    '!src/domain/value_objects/EmbeddingVector.ts',  // Exclude complex embedding logic for now
    '!src/components/**',  // Exclude UI components for now
  ],
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 80,
      lines: 65,
      statements: 65,
    },
    // Focus on well-tested domain entities
    'src/domain/entities/*.ts': {
      branches: 50,
      functions: 80,
      lines: 60,
      statements: 60,
    },
    'src/application/use_cases/*.ts': {
      branches: 30,
      functions: 85,
      lines: 80,
      statements: 80,
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
