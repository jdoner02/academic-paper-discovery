---
mode: agent
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'memory', 'add_comment_to_pending_review', 'add_issue_comment', 'add_sub_issue', 'assign_copilot_to_issue', 'cancel_workflow_run', 'create_and_submit_pull_request_review', 'create_branch', 'create_gist', 'create_issue', 'create_or_update_file', 'create_pending_pull_request_review', 'create_pull_request', 'create_pull_request_with_copilot', 'create_repository', 'delete_file', 'delete_pending_pull_request_review', 'delete_workflow_run_logs', 'dismiss_notification', 'download_workflow_run_artifact', 'fork_repository', 'get_code_scanning_alert', 'get_commit', 'get_dependabot_alert', 'get_discussion', 'get_discussion_comments', 'get_file_contents', 'get_issue', 'get_issue_comments', 'get_job_logs', 'get_me', 'get_notification_details', 'get_pull_request', 'get_pull_request_comments', 'get_pull_request_diff', 'get_pull_request_files', 'get_pull_request_reviews', 'get_pull_request_status', 'get_secret_scanning_alert', 'get_tag', 'get_workflow_run', 'get_workflow_run_logs', 'get_workflow_run_usage', 'list_branches', 'list_code_scanning_alerts', 'list_commits', 'list_dependabot_alerts', 'list_discussion_categories', 'list_discussions', 'list_gists', 'list_issues', 'list_notifications', 'list_pull_requests', 'list_secret_scanning_alerts', 'list_sub_issues', 'list_tags', 'list_workflow_jobs', 'list_workflow_run_artifacts', 'list_workflow_runs', 'list_workflows', 'manage_notification_subscription', 'manage_repository_notification_subscription', 'mark_all_notifications_read', 'merge_pull_request', 'push_files', 'sequentialthinking', 'pylance mcp server', 'configurePythonEnvironment', 'getPythonEnvironmentInfo', 'getPythonExecutableCommand', 'installPythonPackage']
---

# Interactive Research Paper Discovery Platform - Development Instructions

## CRITICAL PROJECT STATE - AUGUST 2025

### **CURRENT PROJECT LOCATION**
**Absolute Path**: `/Users/jessicadoner/Projects/research-papers/research-paper-discovery-web/`

### **CURRENT DEVELOPMENT STATUS** ✅ APPLICATION LAYER STARTED
✅ **TDD Cycle 1 COMPLETE**: Paper Entity (8/8 tests passing)
✅ **TDD Cycle 2 COMPLETE**: ConceptNode Entity (21/21 tests passing) 
✅ **TDD Cycle 3 IN PROGRESS**: ExtractConceptsUseCase started (4/4 tests passing)
✅ **Infrastructure Setup**: GitHub Actions CI/CD workflow configured
✅ **Next.js Foundation**: TypeScript, Jest, D3.js dependencies installed
✅ **GitHub Pages**: Ready for deployment with automated workflow
⏳ **Next Priority**: Complete ExtractConceptsUseCase, add UI components
❌ **Not Started**: D3.js visualization, infrastructure implementations

### **VERIFIED TEST SUITE STATUS** ✅
```bash
Test Suites: 3 passed, 3 total
Tests:       33 passed, 33 total
Snapshots:   0 total
```

### **ACTUAL DIRECTORY STRUCTURE** (Updated August 5, 2025)
```
/Users/jessicadoner/Projects/research-papers/research-paper-discovery-web/
├── .github/
│   ├── prompts/
│   │   └── development-instructions.prompt.md    # This file
│   └── workflows/
│       └── ci-cd.yml                            # ✅ CI/CD pipeline
├── .ai_development/
│   ├── project_status.md                        # ✅ Current project status
│   ├── session_2025_08_05/
│   │   ├── current_state_and_next_steps.md
│   │   └── state_assessment_and_cleanup.md     # ✅ Previous session log
│   └── session_2025_08_06/
│       └── successful_application_layer_development.md  # ✅ Latest session log
├── .next/                                       # Next.js build output
├── tests/                                       # ✅ Jest test files
│   ├── unit/
│   │   ├── paper.entity.test.ts                # ✅ 8 tests passing
│   │   ├── concept-node.entity.test.ts         # ✅ 21 tests passing
│   │   └── extract-concepts-use-case.test.ts   # ✅ 4 tests passing (NEW)
│   ├── future-integration/                     # Integration tests for future use
│   │   ├── extract-concepts-use-case.test.ts
│   │   └── ExtractConceptsUseCase.test.ts
│   └── e2e/                                    # Empty - future E2E tests
├── node_modules/                               # Dependencies
├── pages/
│   ├── _app.tsx                                # Next.js app wrapper
│   └── index.tsx                               # Landing page placeholder
├── src/
│   ├── domain/                                 # ✅ COMPLETE - Domain Layer 
│   │   ├── entities/
│   │   │   ├── Paper.ts                        # ✅ 8 tests passing
│   │   │   └── ConceptNode.ts                  # ✅ 21 tests passing  
│   │   └── value_objects/
│   │       ├── EmbeddingVector.ts              # ✅ Supporting value object
│   │       └── EvidenceSentence.ts             # ✅ Supporting value object  
│   ├── application/                            # ⏳ IN PROGRESS - Application Layer
│   │   ├── ports/                              # ✅ Abstract interfaces
│   │   │   ├── PaperRepositoryPort.ts
│   │   │   ├── ConceptRepositoryPort.ts  
│   │   │   └── EmbeddingServicePort.ts
│   │   └── use_cases/                          # ⏳ IN PROGRESS - TDD Cycle 3
│   │       └── ExtractConceptsUseCase.ts       # ✅ 4 tests passing
│   ├── infrastructure/                         # ❌ EMPTY - Future implementations
│   │   ├── adapters/                           # External service integrations
│   │   └── repositories/                       # Data access implementations
│   └── interface/                              # ❌ BASIC - UI components needed
├── package.json                                # ✅ Complete dependencies
├── jest.config.js                              # ✅ FIXED - proper moduleNameMapper
├── next.config.js                              # ✅ GitHub Pages configuration
└── README.md                                   # Project documentation
```

## Project Mission

Build an interactive, web-based research paper discovery platform that transforms academic paper collections into intuitive visual concept maps. This platform bridges the gap between technical research tools and user-friendly interfaces, enabling researchers to explore literature landscapes without technical barriers.

## CRITICAL TDD METHODOLOGY - MANDATORY WORKFLOW ✅ PROVEN SUCCESSFUL

### Test-Driven Development Cycle - ALWAYS FOLLOW ✅ VALIDATED IN TDD CYCLE 1
**RED-GREEN-REFACTOR is non-negotiable for ALL development:**

1. **🔴 RED PHASE**: Write comprehensive failing tests first
   - Define expected behavior through test specifications
   - Include edge cases, error conditions, and integration scenarios
   - Tests serve as executable documentation and contracts
   - **LESSON LEARNED**: Start with 4-6 focused tests per entity
   - **VALIDATION**: Paper.test.ts demonstrates this approach perfectly

2. **🟢 GREEN PHASE**: Implement minimal solution to pass tests
   - Write only enough code to make current tests pass
   - Focus on functionality over elegance in this phase
   - Validate all tests pass before proceeding to refactor
   - **LESSON LEARNED**: TypeScript helps catch issues early in green phase

3. **🔵 REFACTOR PHASE**: Improve code quality while maintaining behavior
   - Apply Clean Architecture patterns and SOLID principles
   - Enhance readability, performance, and maintainability
   - Add comprehensive educational documentation
   - **LESSON LEARNED**: Educational documentation is as important as the code
   - **VALIDATION**: Paper.ts demonstrates extensive educational documentation

### Atomic Commit Strategy - MANDATORY ✅ PROVEN APPROACH
Every commit must represent a single, complete, working change:
- **Complete TDD Cycles**: Include tests + implementation + refactoring
- **Self-Contained Changes**: Each commit leaves system in working state
- **Descriptive Messages**: Follow conventional commit format
- **Clean History**: Logical progression of feature development
- **LESSON LEARNED**: GitHub Actions validates each commit automatically

## CLEAN ARCHITECTURE PRINCIPLES - STRICT ENFORCEMENT ✅ FOUNDATION ESTABLISHED

### Architectural Layers (Inner → Outer Dependency Flow Only)

**Domain Layer (Core Business Logic)** - ✅ PARTIALLY COMPLETE:
```
src/domain/
├── entities/           # Core business objects with identity
│   ├── Paper.ts       # ✅ COMPLETE - Research paper entity
│   └── ConceptNode.ts # ⏳ NEXT TARGET - Individual concept in hierarchy
└── value_objects/      # Immutable domain concepts
    ├── EmbeddingVector.ts   # ✅ COMPLETE - Semantic vector representation
    └── EvidenceSentence.ts  # ✅ COMPLETE - Text evidence for concepts
```

**Application Layer (Use Cases and Coordination)** - ❌ NOT STARTED:
```
src/application/
├── use_cases/          # Business operations orchestration
│   ├── ExtractConceptsUseCase.ts    # Paper → concepts pipeline
│   ├── BuildVisualizationDataUseCase.ts # Prepare D3.js data
│   └── SearchPapersUseCase.ts       # Query interface
└── ports/              # Abstract interfaces for dependencies
    ├── PaperRepositoryPort.ts       # Data access abstraction
    ├── EmbeddingsServicePort.ts     # ML model abstraction
    └── VisualizationDataPort.ts     # Frontend data interface
```

**Infrastructure Layer (External Dependencies)** - ❌ NOT STARTED:
```
src/infrastructure/
├── repositories/       # Data access implementations
│   ├── GithubPaperRepository.ts    # CLI tool integration
│   ├── JsonConceptRepository.ts    # Concept data storage
│   └── FileSystemRepository.ts     # Local file operations
└── adapters/          # External service integrations
    ├── SentenceTransformersAdapter.ts # Embeddings model
    └── D3jsDataAdapter.ts             # Visualization formatting
```

**Interface Layer (User Interactions)** - ❌ BASIC FOUNDATION ONLY:
```
src/interface/
├── components/        # React UI components
├── pages/            # Next.js page routes (basic placeholder exists)
└── visualization/    # D3.js interactive components
```

## IMMEDIATE NEXT STEPS - CLEAR PRIORITY ORDER

### **Step 1: Fix Build and Deploy** ⏳ IMMEDIATE PRIORITY  
**Issue**: Next.js production build fails with webpack module resolution errors
**Status**: Development mode works, production build needs debugging
**Goal**: Get working demo deployed to GitHub Pages

**Commands to Debug**:
```bash
npm run dev     # ✅ Works - development server
npm run build   # ❌ Fails - webpack module resolution
npm test        # ✅ Works - 33/33 tests passing
```

**Next Actions**:
1. Fix Next.js build configuration issues
2. Test static export functionality  
3. Deploy to GitHub Pages via CI/CD pipeline
4. Verify live demo works end-to-end

### **Step 2: Enhanced Concept Extraction**
**After successful deployment:**
- Add real concept extraction logic to ExtractConceptsUseCase
- Implement executeBatch() method with comprehensive tests
- Create infrastructure layer repository implementations
- Add integration tests for end-to-end workflows

### **Step 3: D3.js Visualization** 
**After enhanced extraction:**
- Interactive force-directed graph components
- Concept hierarchy visualization
- Node interactions and evidence tooltips
- Advanced UI components and responsive design

### **Step 4: UI Component Development**
**After visualization core complete:**
- Landing page enhancement
- Configuration form components
- Results display components
- Mobile-responsive design

## ESSENTIAL COMMANDS FOR DEVELOPMENT

### **Working Directory Navigation**
```bash
cd /Users/jessicadoner/Projects/research-papers/research-paper-discovery-web
```

### **Test Execution (Critical for TDD)**
```bash
# Run all tests
npm test

# Run specific test file
npm test ConceptNode.test.ts

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### **Development Server**
```bash
# Start Next.js development server
npm run dev
# Opens on http://localhost:3000

# Build for GitHub Pages
npm run build
npm run export
```

### **GitHub Actions (Automated)**
- **Push to main**: Triggers CI/CD pipeline
- **Pull request**: Runs test suite validation
- **Successful build**: Deploys to GitHub Pages

## PROVEN PATTERNS FROM TDD CYCLE 1 ✅ APPLY TO ALL FUTURE DEVELOPMENT

### **Test Organization Pattern**
```typescript
// __tests__/ConceptNode.test.ts (NEXT TARGET)
describe('ConceptNode Entity', () => {
  describe('Creation and Identity', () => {
    // Basic construction, identity, validation tests
  });

  describe('Hierarchical Relationships', () => {
    // Parent/child relationship management tests
  });

  describe('Evidence Management', () => {
    // Evidence sentence collection and weighting tests
  });

  describe('Semantic Operations', () => {
    // Embedding vector and similarity calculation tests
  });
});
```

### **Entity Implementation Pattern** ✅ PROVEN SUCCESSFUL
```typescript
// src/domain/entities/ConceptNode.ts (NEXT TARGET)
/**
 * ConceptNode - Represents a single concept within a hierarchical research topic structure.
 * 
 * This entity demonstrates Clean Architecture principles by maintaining identity while
 * encapsulating complex hierarchical relationships and evidence management.
 * 
 * Educational Notes:
 * - Shows Entity pattern with clear identity and lifecycle
 * - Demonstrates bidirectional relationship management
 * - Illustrates aggregation of value objects (EvidenceSentences)
 * - Exemplifies domain logic encapsulation
 */

export class ConceptNode {
  // Implementation following Paper.ts patterns...
}
```

### **Value Object Integration Pattern** ✅ ESTABLISHED
- Import and use EmbeddingVector for semantic operations
- Aggregate EvidenceSentence instances for text evidence
- Follow immutability principles established in value objects

## GITHUB INTEGRATION STRATEGY ✅ INFRASTRUCTURE READY

### **Repository Configuration** ✅ COMPLETE
**Primary Repository** (CLI Tool): `research-papers/research-paper-aggregator`
**Web Interface Repository** (This Project): `research-papers/research-paper-discovery-web`
**GitHub Pages URL**: `https://jdoner02.github.io/research-paper-discovery-web/`

### **Automated CI/CD Pipeline** ✅ DEPLOYED
**Location**: `/Users/jessicadoner/Projects/research-papers/research-paper-discovery-web/.github/workflows/ci-cd.yml`

**Pipeline Features**:
- **Continuous Integration**: Automated testing on every push/PR
- **Type Checking**: TypeScript validation
- **Linting**: Code quality enforcement
- **Test Execution**: Complete test suite validation
- **GitHub Pages Deployment**: Automatic deployment on main branch success
- **Build Optimization**: Next.js static export for GitHub Pages compatibility

**Workflow Triggers**:
```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

### **Development Workflow** ✅ ESTABLISHED
1. **Local Development**: TDD cycles with comprehensive testing
2. **Commit**: Atomic commits following conventional commit format
3. **Push**: Triggers automated CI/CD pipeline
4. **GitHub Actions**: Validates all tests, builds, and deploys
5. **GitHub Pages**: Live updates at public URL

### **Integration with CLI Tool** (Future Enhancement)
**Git Submodule Approach** (Planned):
```bash
# Add CLI tool as submodule (when ready)
git submodule add ../research-paper-aggregator cli-tool
```

**Automated Data Pipeline** (Future):
- CLI tool completion triggers web repo update
- Concept extraction processes new papers
- Visualization data regeneration
- Automated GitHub Pages deployment

## TESTING STRATEGY - COMPREHENSIVE COVERAGE ✅ FOUNDATION PROVEN

### **Current Test Status** ✅ EXCELLENT FOUNDATION
```bash
# TDD Cycle 1 Results - ALL PASSING
Test Suites: 1 passed, 1 total
Tests:       8 passed, 8 total
Coverage:    ~95% for Paper entity
```

### **Test Pyramid Distribution** (Target)
**Unit Tests (70%)**:
- ✅ Domain entity behavior validation (Paper complete, ConceptNode next)
- ✅ Value object immutability and equality (EmbeddingVector, EvidenceSentence)
- ⏳ Service algorithm correctness (future)
- ⏳ Embedding vector operations (future)

**Integration Tests (20%)**: ⏳ Future Phase
- Repository implementation validation
- Use case coordination testing
- Data pipeline end-to-end flow

**End-to-End Tests (10%)**: ⏳ Future Phase
- Complete user workflow validation
- D3.js visualization rendering
- Mobile responsiveness validation

### **Testing Utilities Established** ✅ PROVEN PATTERNS
```typescript
// __tests__/ directory structure
describe('Entity Name', () => {
  describe('Creation and Identity', () => {
    // Constructor, validation, identity tests
  });
  
  describe('Business Behavior', () => {
    // Domain logic and method tests
  });
});
```

## DEVELOPMENT WORKFLOW STANDARDS ✅ ESTABLISHED & VALIDATED

### **Sequential Thinking Integration** ✅ PROVEN ESSENTIAL
- **MANDATORY**: Use `mcp_sequentialthi_sequentialthinking` for all architectural decisions
- **Planning First**: Structure approach through 6-8 logical steps before coding
- **Development Logs**: Track progress in `.ai_development/session_*/` directories
- **Decision Documentation**: Record architectural rationale for future sessions
- **LESSON LEARNED**: Sequential thinking prevents architectural mistakes

### **Code Quality Requirements** ✅ ENFORCED BY TOOLING
- **Type Hints**: Complete TypeScript typing (enforced by CI/CD)
- **Docstrings**: Comprehensive educational documentation (see Paper.ts example)
- **Error Handling**: Graceful degradation with clear error messages
- **Performance**: Efficient algorithms suitable for research datasets
- **Testing**: TDD methodology with >95% coverage on domain layer

### **Educational Documentation Standards** ✅ ESTABLISHED PATTERN

**Module-Level Documentation Pattern** (Apply to all future files):
```typescript
/**
 * ConceptNode.ts - Individual concept within hierarchical research topic structure.
 * 
 * This entity demonstrates Clean Architecture principles by maintaining identity while
 * encapsulating complex hierarchical relationships and evidence management.
 * 
 * Educational Notes:
 * - Shows Entity pattern with clear identity and lifecycle management
 * - Demonstrates bidirectional relationship management in domain entities
 * - Illustrates aggregation of value objects for complex data structures
 * - Exemplifies domain logic encapsulation following DDD principles
 * 
 * Design Decisions:
 * - Hierarchical Position: Enables tree navigation and relationship queries
 * - Evidence Aggregation: Links abstract concepts to concrete textual support
 * - Semantic Vectors: Enables similarity calculations for concept clustering
 * - Identity Management: Supports entity lifecycle and change tracking
 * 
 * Real-World Application:
 * Academic researchers need to understand how concepts relate within research domains.
 * This entity models individual nodes in concept hierarchies, enabling researchers
 * to navigate from broad themes to specific implementation details while maintaining
 * clear evidence trails back to source papers.
 * 
 * Integration Points:
 * - Works with EmbeddingVector for semantic similarity calculations
 * - Aggregates EvidenceSentence instances for textual evidence
 * - Participates in concept tree structures for hierarchical navigation
 * - Interfaces with visualization layer for interactive concept mapping
 */
```

**Function-Level Documentation Pattern** (Educational Focus):
```typescript
public addChildConcept(child: ConceptNode): ConceptNode {
  /**
   * Add a child concept to this node, establishing bidirectional relationship.
   * 
   * Educational Note:
   * This method demonstrates the Aggregate pattern by managing relationships
   * between entities while maintaining referential integrity. The bidirectional
   * nature ensures consistent navigation in both directions of the hierarchy.
   * 
   * Domain Logic:
   * In academic concept hierarchies, relationships must be bidirectional for
   * effective navigation. Researchers need to move both up (specialization to
   * generalization) and down (generalization to specialization) the concept tree.
   */
}
```

## CRITICAL SUCCESS FACTORS ✅ PROVEN APPROACH

### **Technical Excellence** ✅ FOUNDATION ESTABLISHED
- **Test Coverage**: >95% achieved for Paper entity (8/8 tests passing)
- **CI/CD Pipeline**: Automated validation and deployment configured
- **TypeScript**: Full type safety with educational documentation
- **Clean Architecture**: Strict layer separation enforced

### **Educational Value** ✅ EXEMPLIFIED IN PAPER.TS
- **Pattern Demonstration**: Clear examples of Entity, Value Object patterns
- **Documentation Quality**: Comprehensive explanations of design decisions
- **Code Readability**: Self-documenting code with extensive comments
- **Knowledge Transfer**: Concepts applicable across software domains

### **Development Continuity** ✅ CRITICAL FOR MULTI-SESSION WORK
- **State Documentation**: Clear development progress tracking
- **Instruction Updates**: Living document reflecting current reality
- **Lesson Capture**: Experience-based improvements to methodology
- **Path Forward**: Clear next steps for efficient continuation

## IMMEDIATE ACTION PLAN - START HERE 🎯

### **Current Session Continuation**
1. **Navigate to Project**: `cd /Users/jessicadoner/Projects/research-papers/research-paper-discovery-web`
2. **Verify Foundation**: `npm test` (expect 8/8 tests passing)
3. **Begin TDD Cycle 2**: Create `__tests__/ConceptNode.test.ts` with failing tests
4. **Implement Entity**: Create `src/domain/entities/ConceptNode.ts` following Paper.ts patterns
5. **Complete Cycle**: Refactor with educational documentation

### **Quality Validation Steps**
- **Test Execution**: All tests must pass before committing
- **Type Checking**: `npm run type-check` must succeed
- **Documentation**: Educational comments required for all public methods
- **Clean Architecture**: Verify no outer-layer dependencies in domain code

Remember: This project demonstrates professional software development practices while solving genuine problems for the academic research community. Every line of code should advance both the technical implementation and educational mission.
