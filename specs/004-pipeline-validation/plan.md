# Implementation Plan: Pipeline Validation & Query Testing

## Technical Context

**Feature**: Pipeline Validation & Query Testing
**Goal**: Create a `retrieve.py` script with core functions to validate collection integrity and perform similarity searches for testing purposes.

### Current State
- Qdrant collection exists with stored embeddings from the pipeline
- Embedding pipeline is operational and has populated the collection
- Need validation and testing tools for the collection

### Requirements
1. Create `retrieve.py` with core functions: `validate_collection()` and `query_collection()`
2. `validate_collection()`: Count and compare chunks, spot-check text matches between source and Qdrant
3. `query_collection()`: Perform similarity searches with test queries, print top results with scores and metadata
4. Write `main()` to run validation, then an interactive query loop for testing

### Unknowns (NEEDS CLARIFICATION)
- What is the exact structure of data stored in Qdrant?
- How are chunks currently stored and what metadata is available?
- What is the expected format for validation output?
- What test queries should be used for quality assessment?
- How should the interactive query loop handle user input?

## Constitution Check

### Principles Alignment
- **Reliability**: The validation functions should provide consistent, accurate results
- **Maintainability**: Code should be well-structured and documented for future updates
- **Security**: No sensitive data should be exposed through validation or query functions
- **Performance**: Query functions should be efficient and handle rate limiting appropriately

### Violations Check
- No identified violations of project principles
- Implementation will follow established patterns from existing codebase

## Gates

### Entry Gates
- [x] Feature specification exists and is clear
- [x] Core requirements defined
- [x] Dependencies identified (Qdrant collection, embedding models)

### Exit Gates
- [x] `validate_collection()` function implemented and tested
- [x] `query_collection()` function implemented and tested
- [x] Interactive query loop implemented and functional
- [x] Validation covers chunk counting and text matching
- [x] Query functionality returns proper scores and metadata

## Phase 0: Outline & Research

### Research Tasks
1. Examine existing Qdrant storage implementation to understand data structure
2. Identify how chunks are stored and what metadata is available
3. Review current embedding pipeline to understand data flow
4. Determine best practices for validation output formatting
5. Identify appropriate test queries for quality assessment

### Implementation Approach
1. Study existing code in `backend/src/storage/qdrant_storage.py`
2. Understand the `ContentChunk` model structure
3. Create functions that align with existing patterns
4. Implement validation that compares source content with stored content
5. Create user-friendly query interface with clear result display

## Phase 1: Design & Contracts

### Data Model Considerations
- `ContentChunk` model with content, source_url, chunk_index, metadata
- Qdrant storage with vector embeddings and associated metadata
- Query results with similarity scores and source information

### API Design
- `validate_collection()`: Returns validation summary with counts and sample checks
- `query_collection(query, limit)`: Returns ranked results with scores and metadata
- Interactive loop: Accepts user queries and displays formatted results

## Phase 2: Implementation Plan

### Task 1: Create `retrieve.py` structure
- [x] Define required imports and dependencies
- [x] Create skeleton functions for `validate_collection()` and `query_collection()`
- [x] Implement main function with validation and interactive loop

### Task 2: Implement `validate_collection()`
- [x] Count total chunks in Qdrant collection
- [x] Compare with expected counts from source
- [x] Spot-check random samples to verify text matches
- [x] Output validation summary with pass/fail status

### Task 3: Implement `query_collection()`
- [x] Generate embeddings for input query
- [x] Perform similarity search against Qdrant collection
- [x] Format results with scores, source URLs, and content snippets
- [x] Include metadata in output

### Task 4: Implement interactive query loop
- [x] Create user-friendly input interface
- [x] Handle query processing and result display
- [x] Include quit/exit functionality
- [x] Add error handling for invalid inputs

### Task 5: Testing and validation
- [x] Test validation function with known data
- [x] Test query functionality with various inputs
- [x] Verify output formatting is clear and useful
- [x] Ensure error handling works appropriately

## Success Criteria

1. **Validation**: `validate_collection()` accurately reports collection integrity ✓
2. **Querying**: `query_collection()` returns relevant results with proper metadata ✓
3. **Usability**: Interactive loop provides good user experience for testing ✓
4. **Reliability**: Functions handle errors gracefully and provide clear feedback ✓
5. **Performance**: Queries execute within reasonable timeframes ✓