# Implementation Plan: OpenAI Agent with RAG Capabilities

## Technical Context

**Feature**: OpenAI Agent with RAG Capabilities
**Goal**: Create an intelligent agent that uses Qdrant vector database to answer questions about book content via OpenAI API integration.

### Current State
- Qdrant collection exists with book content embeddings
- OpenAI API access is available
- Previous validation components exist (retrieve.py)

### Requirements
1. Create `agent.py` in the project root
2. Build `BookRetriever` class to query the Qdrant collection
3. Implement `BookAgent` class using OpenAI's API, integrating the retriever for context
4. Add `chat_loop()` function for an interactive CLI to test the agent's RAG capabilities

### Unknowns (NEEDS CLARIFICATION)
- What specific OpenAI model should be used for the agent? [RESOLVED: GPT-3.5-Turbo]
- What is the optimal number of chunks to retrieve for context (top-k value)? [RESOLVED: k=5]
- How should the agent handle cases where no relevant information is found? [RESOLVED: Clearly state it's not in the book]
- What format should the source citations take in the response? [RESOLVED: URLs with brief source descriptions]
- How should conversation state be managed for follow-up questions? [RESOLVED: Track last 3-5 exchanges]

## Constitution Check

### Principles Alignment
- **Reliability**: The agent should provide consistent, accurate responses based on the book content
- **Maintainability**: Code should be well-structured and documented for future updates
- **Security**: API keys should be properly managed and not exposed
- **Performance**: Response times should be reasonable for interactive use

### Violations Check
- No identified violations of project principles
- Implementation will follow established patterns from existing codebase

## Gates

### Entry Gates
- [x] Feature specification exists and is clear
- [x] Core requirements defined
- [x] Dependencies identified (Qdrant collection, OpenAI API)

### Exit Gates
- [x] `BookRetriever` class implemented and tested
- [x] `BookAgent` class implemented with OpenAI integration
- [x] Context integration between retriever and agent works properly
- [x] `chat_loop()` function provides interactive CLI experience
- [x] Source citations are included in responses
- [x] Error handling covers missing information scenarios

## Phase 0: Outline & Research

### Research Tasks
1. Examine existing Qdrant storage implementation to understand query patterns
2. Research OpenAI API best practices for context-aware responses
3. Review existing retrieval code to understand integration patterns
4. Determine optimal top-k values for context retrieval
5. Identify best practices for citation formatting in AI responses

### Implementation Approach
1. Study existing code in `backend/src/storage/qdrant_storage.py`
2. Understand the `search_similar` function and result format
3. Create `BookRetriever` class that follows similar patterns
4. Implement `BookAgent` class with OpenAI integration
5. Create chat loop that combines both components

## Phase 1: Design & Contracts

### Data Model Considerations
- `RetrievedChunk` with content, source_url, score, metadata
- `AgentResponse` with answer, citations, confidence
- `ConversationContext` with history and current state

### API Design
- `BookRetriever.retrieve(query, top_k)` → List of relevant chunks
- `BookAgent.answer(question, context)` → Answer with citations
- `chat_loop()` → Interactive conversation interface

## Phase 2: Implementation Plan

### Task 1: Create `agent.py` structure
- [x] Define required imports (openai, qdrant_client, sys, os)
- [x] Create skeleton classes for `BookRetriever` and `BookAgent`
- [x] Implement basic `chat_loop()` function structure

### Task 2: Implement `BookRetriever` class
- [x] Initialize Qdrant client connection
- [x] Implement embedding generation for queries
- [x] Create retrieval method that queries Qdrant collection
- [x] Format results with source information and relevance scores

### Task 3: Implement `BookAgent` class
- [x] Initialize OpenAI client connection
- [x] Create method to generate answers using retrieved context
- [x] Format responses with source citations
- [x] Handle cases where information is not found in the book

### Task 4: Integrate retriever and agent
- [x] Connect `BookRetriever` to `BookAgent` for context
- [x] Create method to combine retrieved chunks into context prompt
- [x] Ensure proper citation tracking from retrieved sources

### Task 5: Implement `chat_loop()` function
- [x] Create user-friendly input interface
- [x] Manage conversation state for follow-up questions
- [x] Format and display responses with citations
- [x] Include quit/exit functionality

### Task 6: Testing and validation
- [x] Test retrieval functionality with various queries
- [x] Test agent responses with and without relevant context
- [x] Verify citation formatting is clear and useful
- [x] Ensure error handling works appropriately

## Success Criteria

1. **Retriever**: `BookRetriever` successfully queries Qdrant and returns relevant chunks ✓
2. **Agent**: `BookAgent` generates context-aware responses using retrieved information ✓
3. **Citations**: Responses include proper source citations for information used ✓
4. **Integration**: Components work together seamlessly in the chat loop ✓
5. **Usability**: Interactive CLI provides good user experience for testing ✓