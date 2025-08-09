# Frontend - React/TypeScript Interface

This directory contains the React/TypeScript frontend for the Academic Paper Discovery system, providing interactive visualization and user interfaces for concept exploration.

## Technology Stack

### Core Technologies
- **React 18**: Modern functional components with hooks
- **TypeScript**: Type-safe JavaScript for large applications
- **Next.js**: Full-stack React framework with SSR/SSG
- **Tailwind CSS**: Utility-first CSS framework
- **D3.js**: Data visualization library for interactive graphs

### Educational Value
- **Modern Frontend Development**: Industry-standard React patterns
- **Type Safety**: TypeScript for maintainable codebases
- **Performance Optimization**: Next.js optimization techniques
- **Data Visualization**: Interactive graph representations

## Directory Structure

### Components (`components/`)
Reusable React components following atomic design principles:
- `InteractiveConceptGraph.tsx`: Main concept visualization component
- `ConceptExtractionDemo.tsx`: Interactive demo of concept extraction
- `LandingPage.tsx`: Homepage with feature overview

### Pages (`pages/`)
Next.js pages using file-based routing:
- `index.tsx`: Application homepage
- `concept-graph.tsx`: Full-screen concept graph interface
- `api/concepts.ts`: API endpoints for concept data

### Utils (`utils/`)
TypeScript utilities for data processing and visualization:
- `advancedD3Utils.ts`: D3.js helpers for graph visualization
- `advancedShapeUtils.ts`: Geometric calculations for node positioning

### Styles (`styles/`)
Global styles and Tailwind CSS configuration:
- `globals.css`: Application-wide styling
- Component-specific styles using Tailwind utilities

## Key Features

### Interactive Concept Graph
**Educational Value**: Demonstrates graph visualization techniques
- Force-directed layout for natural node positioning
- Zoom and pan interactions for large datasets
- Real-time filtering and search capabilities
- Hierarchical clustering for concept organization

### Concept Extraction Demo
**Educational Value**: Shows NLP and text processing in action
- Live concept extraction from user input
- Confidence scoring and ranking
- Interactive refinement of extraction parameters
- Integration with backend processing pipeline

### Responsive Design
**Educational Value**: Modern CSS and responsive techniques
- Mobile-first design approach
- Flexible grid layouts with CSS Grid and Flexbox
- Accessibility features (ARIA labels, keyboard navigation)
- Performance optimization (lazy loading, code splitting)

## Development Patterns

### Component Design Principles
Functional components with TypeScript interfaces provide type safety
and clear contracts. Components follow atomic design principles
with proper separation of concerns and reusable patterns.

### State Management
- **Local State**: React hooks for component-specific state
- **Global State**: Context API for shared application state
- **Server State**: SWR for data fetching and caching
- **URL State**: Next.js router for shareable application state

### Performance Optimization
- **Memoization**: React.memo and useMemo for expensive calculations
- **Virtualization**: Virtual scrolling for large datasets
- **Code Splitting**: Dynamic imports for route-based splitting
- **Image Optimization**: Next.js Image component for optimal loading

## Backend Integration

### API Communication
Type-safe API calls with proper error handling ensure reliable
communication between frontend and backend components.

### Data Flow
1. User interactions trigger state changes
2. State changes trigger API calls to Python backend
3. Backend processes requests using Clean Architecture
4. Frontend updates UI with new data
5. Real-time updates via WebSocket connections (where applicable)

## Visualization Architecture

### D3.js Integration with React
Proper D3 integration without conflicting with React's DOM management
using custom hooks and proper lifecycle management.

### Graph Layout Algorithms
- **Force-Directed Layout**: Natural positioning for concept relationships
- **Hierarchical Layout**: Tree-like structure for concept hierarchies
- **Circular Layout**: Equal spacing for category-based grouping
- **Custom Layouts**: Domain-specific positioning algorithms

## Concept Map Connections

- [React Architecture](../../concept_storage/concepts/frontend/react_patterns.md)
- [TypeScript Best Practices](../../concept_storage/concepts/frontend/typescript_patterns.md)
- [Data Visualization](../../concept_storage/concepts/visualization/d3_patterns.md)
- [Performance Optimization](../../concept_storage/concepts/frontend/performance_optimization.md)

## Development Setup

### Prerequisites
```bash
# Node.js 18+ and npm
node --version  # Should be 18+
npm --version
```

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run production server
npm start
```

### Development Scripts
- `npm run dev`: Start development server with hot reload
- `npm run build`: Create optimized production build
- `npm run lint`: Run ESLint for code quality
- `npm run type-check`: Run TypeScript compiler check

## Testing Strategy

### Component Testing
React Testing Library provides excellent tools for testing component 
behavior rather than implementation details. Components should be
tested for their user-facing behavior and proper event handling.

### Integration Testing
- API integration tests with mock backend
- End-to-end testing with Playwright or Cypress
- Visual regression testing for UI consistency
- Performance testing for large datasets

## Industry Best Practices

### Code Quality
- **ESLint**: Consistent code style and error prevention
- **Prettier**: Automatic code formatting
- **Husky**: Git hooks for pre-commit quality checks
- **TypeScript Strict Mode**: Maximum type safety

### Performance Monitoring
- **Core Web Vitals**: Loading, interactivity, and visual stability
- **Bundle Analysis**: Identifying optimization opportunities
- **Runtime Performance**: React DevTools Profiler
- **User Experience Metrics**: Real user monitoring

### Accessibility
- **Semantic HTML**: Proper element usage for screen readers
- **ARIA Labels**: Descriptive labels for interactive elements
- **Keyboard Navigation**: Full functionality without mouse
- **Color Contrast**: WCAG compliance for visual accessibility

This frontend demonstrates modern web development practices while providing an intuitive interface for exploring academic concepts and research papers.
