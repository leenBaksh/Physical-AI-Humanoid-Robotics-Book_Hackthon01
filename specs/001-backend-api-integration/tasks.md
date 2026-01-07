# Tasks: Backend API & Frontend Integration

## Feature Overview

**Feature**: Backend API & Frontend Integration
**Goal**: Create a FastAPI backend to serve the RAG agent and integrate it with the Docusaurus book frontend.

Based on spec.md, the primary user stories are:
1. As a user reading the book, I want to ask questions about the book content through a chat interface so that I can get immediate answers based on the book's content (Priority: P1)
2. As a user reading the book, I want to interact with a chat interface embedded in the Docusaurus site so that I can ask questions without leaving the book content (Priority: P2)
3. As a developer, I want the backend and frontend to work together locally so that I can test the complete integration before deployment (Priority: P3)

## Dependencies

- `agent.py` must be available with the BookAgent class
- Qdrant collection must be populated with book content embeddings
- OpenAI API access for generating responses
- Properly configured environment variables for API keys

## Parallel Execution Examples

- [US1] Backend API development can be done in parallel with [US2] Frontend component development after foundational setup
- [US2] Frontend development can be done in parallel with [US3] Integration testing once backend API is stable

## Implementation Strategy

MVP scope: Basic backend API with `/chat` endpoint that integrates with BookAgent. The core `api.py` file with the `/chat` endpoint forms the minimal viable implementation. Frontend integration and local testing are enhancements that provide additional value.

---

## Phase 1: Setup

### Goal
Initialize the project structure and set up dependencies for the backend API and frontend integration functionality.

### Independent Test Criteria
- Required Python dependencies are installed
- FastAPI application can be started
- Environment variables are properly loaded
- Connection to existing BookAgent can be established

### Tasks

- [ ] T001 Create api.py file with proper imports and dependencies
- [ ] T002 Install required dependencies (fastapi, uvicorn, python-dotenv, openai-agents)
- [ ] T003 Set up logging configuration for the API application

## Phase 2: Foundational

### Goal
Implement foundational components that are required by all user stories.

### Independent Test Criteria
- FastAPI app instance can be created
- CORS middleware is properly configured
- BookAgent from agent.py can be imported and instantiated
- Session management system can be initialized

### Tasks

- [ ] T004 [P] Create FastAPI app instance with proper configuration
- [ ] T005 [P] Configure CORS middleware for Docusaurus frontend integration
- [ ] T006 [P] Import and initialize BookAgent from existing agent.py module
- [ ] T007 [P] Create in-memory session storage for conversation management
- [ ] T008 [P] Create data models for ChatRequest and ChatResponse based on API contract

## Phase 3: [US1] Backend API Endpoint

### Goal
Implement the `/chat` POST endpoint that accepts user messages and session IDs, uses the BookAgent to generate responses, and returns answers with source citations.

### Independent Test Criteria
- Endpoint accepts POST requests with message and session_id
- Endpoint integrates with BookAgent to generate responses
- Endpoint returns responses with answer text and source citations
- Endpoint maintains conversation history per session ID
- Error conditions are handled gracefully

### Tasks

- [ ] T009 [US1] Create /chat POST endpoint with proper request/response models
- [ ] T010 [US1] Implement session management to maintain conversation history
- [ ] T011 [US1] Integrate BookAgent to process user queries and generate responses
- [ ] T012 [US1] Format responses with answer text and source citations as per API contract
- [ ] T013 [US1] Add error handling for various failure scenarios
- [ ] T014 [US1] Implement validation for incoming requests
- [ ] T015 [US1] Test the /chat endpoint with sample requests

## Phase 4: [US2] Frontend Chat Interface

### Goal
Implement a React component embedded in the Docusaurus site that serves as a chat UI and sends requests to the local backend API.

### Independent Test Criteria
- React chat component is created and functional
- Component can send API requests to the local backend
- Component displays responses with source citations
- Component maintains conversation history in the UI
- Error handling is implemented for API failures

### Tasks

- [ ] T016 [US2] Create React chat component structure for Docusaurus integration
- [ ] T017 [US2] Implement API communication layer to connect with backend
- [ ] T018 [US2] Create UI elements for message input and response display
- [ ] T019 [US2] Implement display of responses with source citations
- [ ] T020 [US2] Add conversation history management in the UI
- [ ] T021 [US2] Implement error handling for API communication failures
- [ ] T022 [US2] Style the chat component to match Docusaurus theme
- [ ] T023 [US2] Test the frontend component with the backend API

## Phase 5: [US3] Local Integration

### Goal
Ensure the backend and frontend work together locally, with proper communication and error handling.

### Independent Test Criteria
- Backend API runs locally without errors
- Frontend can connect to local backend API
- Messages flow correctly from frontend to backend and back
- CORS and connectivity issues are resolved
- Complete user flow works end-to-end

### Tasks

- [ ] T024 [US3] Configure local development environment for both backend and frontend
- [ ] T025 [US3] Test end-to-end flow from frontend to backend and back
- [ ] T026 [US3] Resolve any CORS or connectivity issues between frontend and backend
- [ ] T027 [US3] Verify that conversation history is maintained across frontend and backend
- [ ] T028 [US3] Test error handling in the complete flow
- [ ] T029 [US3] Optimize API communication for local development
- [ ] T030 [US3] Document local setup and testing procedures

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Finalize the implementation with documentation, testing, and optimization.

### Independent Test Criteria
- All components are properly documented
- Error handling covers all edge cases
- Performance is optimized for local development
- User experience is intuitive and informative
- Setup and deployment procedures are documented

### Tasks

- [ ] T031 Add comprehensive error handling for edge cases
- [ ] T032 Optimize session management performance
- [ ] T033 Create documentation for local setup and usage
- [ ] T034 Add input validation and sanitization
- [ ] T035 Test the complete implementation with various scenarios
- [ ] T036 Finalize error handling and logging