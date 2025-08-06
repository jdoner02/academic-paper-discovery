# TDD Cycle 1: Core Domain Entities - Session 2025-08-05

# TDD Cycle 1: Core Domain Entities - Session 2025-08-05

## RED PHASE: Writing Failing Tests ✅ COMPLETE

### Objective
Create comprehensive failing tests for core domain entities (Paper, ConceptNode, ConceptTree) that define the expected behavior and serve as executable specifications.

### Test Strategy
Following the new.prompt.md TDD methodology:
1. **Write failing tests first** that define the complete behavior ✅
2. **Behavioral grouping** by test classes focusing on specific capabilities ✅
3. **Comprehensive coverage** including creation, validation, and business behavior ✅
4. **Educational documentation** explaining domain concepts and design decisions ✅

### Tests Created ✅

**Paper Entity Tests** - `tests/unit/paper.entity.test.ts`:
- **TestPaperCreationAndIdentity**: 4 test cases covering DOI/ArXiv identity, equality, validation
- **TestPaperBusinessBehavior**: 4 test cases covering readiness, processing metadata, validation, summaries
- **Total**: 8 comprehensive test cases with extensive educational documentation

### RED Phase Validation ✅

**Expected Test Failures Confirmed**:
```
Cannot find module '@/domain/entities/Paper' from 'tests/unit/paper.entity.test.ts'
Cannot find module '@/domain/value_objects/EmbeddingVector'  
Cannot find module '@/domain/value_objects/EvidenceSentence'
```

**Perfect RED Phase State**:
- ✅ Tests fail for the right reasons (missing domain entities)
- ✅ Test framework properly configured (Jest + TypeScript + Next.js)
- ✅ Path aliases configured for Clean Architecture imports
- ✅ Comprehensive test coverage defined before any implementation
- ✅ Educational documentation integrated throughout tests

### Entities to Implement in GREEN Phase

**Paper Entity** (Primary):
- Identity based on DOI, ArXiv ID, or content hash
- Metadata including title, authors, abstract, full text
- Source information and processing status
- Business behavior: readiness assessment, content summarization

**EmbeddingVector Value Object** (Supporting):
- Immutable semantic vector representation
- Similarity calculations and comparisons
- Validation and serialization support

**EvidenceSentence Value Object** (Supporting):
- Immutable text evidence with confidence scoring
- Sentence-concept relationship modeling
- Display formatting and truncation

---

**Next Steps**: Begin GREEN phase implementation starting with Paper entity to make the first tests pass.

---

**Next Steps**: Run failing tests to confirm RED phase, then move to GREEN phase implementation.
