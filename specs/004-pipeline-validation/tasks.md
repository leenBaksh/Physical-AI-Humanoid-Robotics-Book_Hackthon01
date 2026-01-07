# Tasks: Pipeline Validation & Query Testing

## Feature Overview

**Feature**: Pipeline Validation & Query Testing
**Goal**: Create a `retrieve.py` script with core functions to validate collection integrity and perform similarity searches for testing purposes.

## User Stories

Based on spec.md, the primary user stories are:
1. As a developer, I need to validate that the Qdrant collection contains the expected number of chunks
2. As a developer, I need to spot-check text matches between source content and stored content in Qdrant
3. As a developer, I need to perform similarity searches with test queries and see results with scores and metadata
4. As a developer, I need an interactive query loop for testing the collection

## Dependencies

- Qdrant collection must be populated with embeddings from the pipeline
- Cohere API access for generating query embeddings
- Properly configured environment variables for Qdrant and Cohere

## Parallel Execution Examples

- [US1] Validate collection and [US2] Query collection can be developed in parallel after foundational setup
- [US3] Interactive loop can be developed after basic query functionality

## Implementation Strategy

MVP scope: Basic validation and query functionality. The core `validate_collection()` and `query_collection()` functions form the minimal viable implementation. The interactive loop is an enhancement that provides additional testing capability.

---

## Phase 1: Setup

### Goal
Initialize the project structure and set up dependencies for the validation and query functionality.

### Independent Test Criteria
- Environment variables are properly loaded
- Qdrant connection can be established
- Embedding generator can be initialized

### Tasks

- [x] T001 Create retrieve.py script with proper imports and dependencies
- [x] T002 Set up logging configuration for the retrieve script
- [x] T003 Validate environment settings and API access

## Phase 2: Foundational

### Goal
Implement foundational components that are required by all user stories.

### Independent Test Criteria
- Qdrant storage component can connect to the collection
- Embedding generator can create embeddings for queries
- Common data structures are properly defined

### Tasks

- [x] T004 [P] Implement Qdrant connection validation function
- [x] T005 [P] Create embedding generation helper function
- [x] T006 Define common data structures for validation results
- [x] T007 Implement error handling for API calls

## Phase 3: [US1] Collection Validation

### Goal
Implement `validate_collection()` function that counts chunks and spot-checks text matches between source and Qdrant.

### Independent Test Criteria
- Function returns correct chunk count from Qdrant collection
- Function performs sample text matching between source and stored content
- Function outputs validation summary with pass/fail status

### Tasks

- [x] T008 [US1] Implement get_collection_size function to count chunks in Qdrant
- [x] T009 [US1] Implement get_random_chunks function to retrieve samples for validation
- [x] T010 [US1] Create validate_collection function that counts and compares chunks
- [x] T011 [US1] Add spot-check functionality to compare text between source and Qdrant
- [x] T012 [US1] Format validation output with clear pass/fail indicators

## Phase 4: [US2] Query Collection

### Goal
Implement `query_collection()` function that performs similarity searches with test queries and prints top results with scores and metadata.

### Independent Test Criteria
- Function generates embeddings for input queries
- Function performs similarity search against Qdrant collection
- Function returns results with proper scores and metadata
- Function formats results in a user-friendly way

### Tasks

- [x] T013 [US2] Implement query embedding generation function
- [x] T014 [US2] Create similarity search function against Qdrant collection
- [x] T015 [US2] Format search results with scores and metadata
- [x] T016 [US2] Implement query_collection function with configurable result limit
- [x] T017 [US2] Add error handling for query failures

## Phase 5: [US3] Interactive Query Loop

### Goal
Implement an interactive query loop that allows users to test the collection with multiple queries.

### Independent Test Criteria
- Interactive loop accepts user input for queries
- Loop displays formatted results for each query
- Loop handles exit commands properly
- Loop includes error handling for invalid inputs

### Tasks

- [x] T018 [US3] Create interactive query loop skeleton
- [x] T019 [US3] Implement user input handling for queries
- [x] T020 [US3] Add result display formatting for interactive mode
- [x] T021 [US3] Implement quit/exit functionality
- [x] T022 [US3] Add error handling for interactive mode

## Phase 6: [US4] Main Function Integration

### Goal
Integrate all components into a main function that runs validation first, then enters interactive query loop.

### Independent Test Criteria
- Main function runs validation when started
- Main function enters interactive mode after validation
- Main function supports command-line arguments for specific modes
- Main function handles graceful shutdown

### Tasks

- [x] T023 [US4] Create main function that runs validation first
- [x] T024 [US4] Integrate interactive loop into main function
- [x] T025 [US4] Add command-line argument parsing for different modes
- [x] T026 [US4] Implement proper error handling and exit codes

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Finalize the implementation with documentation, testing, and optimization.

### Independent Test Criteria
- All functions are properly documented
- Error handling covers all edge cases
- Performance is optimized for typical usage
- User experience is intuitive and informative

### Tasks

- [x] T027 Add comprehensive docstrings to all functions
- [x] T028 Implement performance optimization for large collections
- [x] T029 Add configuration options for validation and query parameters
- [x] T030 Create usage examples and documentation
- [x] T031 Test the complete implementation with various scenarios
- [x] T032 Finalize error handling and logging