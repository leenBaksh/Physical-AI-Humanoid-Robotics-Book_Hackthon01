#!/usr/bin/env python3
"""
FastAPI backend for the RAG agent with chat functionality.
This file implements the /chat endpoint that integrates with the BookAgent.
Fixed version that avoids the agents library conflict with FastAPI.
"""

import os
import sys
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Add backend directory to path to access Qdrant storage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import only the necessary components from agent.py, avoiding the agents library import
# We'll import the backend storage components directly
from backend.src.storage.qdrant_storage import QdrantStorage
from backend.src.embeddings.embedding_generator import EmbeddingGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Book Content Chat API",
    description="API for interacting with the Book Content RAG agent",
    version="1.0.0"
)

# Configure CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    message: str
    session_id: str
    options: Dict[str, Any] = {}


class Citation(BaseModel):
    url: str
    title: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    session_id: str
    timestamp: str
    metadata: Dict[str, Any] = {}


class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str


# In-memory session storage for conversation history (for local development)
# In production, this would use a proper database
session_storage: Dict[str, List[Dict[str, Any]]] = {}


def retrieve_qdrant_chunks_impl(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Implementation function for Qdrant retrieval that performs the actual work.
    This is a copy of the function from agent.py to avoid the agents library import.
    """
    if not query or not query.strip():
        logger.warning("Empty query provided to retrieve method")
        return []

    try:
        qdrant_storage = QdrantStorage()
        embedding_generator = EmbeddingGenerator()

        # Generate embedding for the query
        query_embedding = embedding_generator.generate_single_embedding(query)

        if query_embedding is None:
            logger.error("Failed to generate embedding for query")
            return []

        # Validate top_k parameter
        if top_k <= 0:
            logger.warning(f"Invalid top_k value: {top_k}, using default of 5")
            top_k = 5

        # Perform similarity search
        search_results = qdrant_storage.search_similar(query_embedding, limit=top_k)

        # Format results
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                'content': result.get('content', ''),
                'source_url': result.get('source_url', ''),
                'score': result.get('score', 0.0),
                'chunk_index': result.get('chunk_index', 0),
                'metadata': result.get('metadata', {})
            })

        logger.info(f"Retrieved {len(formatted_results)} chunks for query: {query[:50]}...")
        return formatted_results

    except Exception as e:
        logger.error(f"Error during retrieval for query '{query[:30]}...': {e}")
        return []


class BookRetriever:
    """
    Class to query the Qdrant collection for relevant book chunks.
    This is a simplified version that avoids the agents library dependency.
    """
    def __init__(self):
        """
        Initialize the BookRetriever with Qdrant connection.
        """
        self.qdrant_storage = QdrantStorage()
        self.embedding_generator = EmbeddingGenerator()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks from the Qdrant collection based on the query.
        """
        return retrieve_qdrant_chunks_impl(query, top_k)


class SimpleBookAgent:
    """
    Simplified BookAgent that doesn't rely on the problematic agents library.
    This uses the OpenAI API directly for RAG functionality.
    """
    def __init__(self, retriever: BookRetriever, model: str = None, temperature: float = 0.3):
        """
        Initialize the SimpleBookAgent with OpenAI API and retriever.
        """
        import openai
        from dotenv import load_dotenv
        import os

        load_dotenv()

        # Use model from parameter, then environment, then default
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.temperature = temperature
        self.retriever = retriever

        # Set up OpenAI API key
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # If no API key in environment, try to use a default one (for testing)
        if not openai.api_key:
            # You might need to set your own API key here
            pass

    async def answer(self, question: str) -> Dict[str, Any]:
        """
        Generate an answer to the question using OpenAI API directly.
        This is a simplified version that uses retrieved context.
        """
        try:
            # Retrieve relevant chunks
            retrieved_chunks = self.retriever.retrieve(question, top_k=5)

            # Format the context from retrieved chunks
            context_parts = []
            for chunk in retrieved_chunks:
                content = chunk.get('content', '')
                if content:
                    context_parts.append(f"Source: {chunk.get('source_url', 'Unknown')}\nContent: {content}")

            context = "\n\n".join(context_parts)

            # Prepare the prompt with context
            if context:
                system_prompt = f"""You are BookBot, an intelligent AI assistant specializing in answering questions about book content.
                Use the following context to answer the user's question. Only use information from the provided context.
                If the answer is not in the context, clearly state that the information is not in the book.
                Always include source citations for the information you use. Be helpful, accurate, and cite your sources.

                Context: {context}"""
            else:
                system_prompt = "You are BookBot, an intelligent AI assistant. Answer the user's question to the best of your ability."

            # Call OpenAI API directly
            import openai
            from openai import AsyncOpenAI

            # Use OpenRouter API key from agent.py for testing
            ROUTER_API_KEY = "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"
            client = AsyncOpenAI(
                api_key=ROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )

            response = await client.chat.completions.create(
                model="mistralai/devstral-2512:free",  # Using the same model as in agent.py
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=self.temperature
            )

            response_text = response.choices[0].message.content

            # Format citations from retrieved chunks
            citations = []
            for chunk in retrieved_chunks:
                source_url = chunk.get('source_url', '')
                metadata_title = chunk.get('metadata', {}).get('title', 'Book Content')

                if source_url:  # Only add citation if there's a URL
                    citations.append({
                        'url': source_url,
                        'title': metadata_title
                    })

            return {
                'answer': response_text,
                'citations': citations,
                'retrieved_chunks_used': retrieved_chunks,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            response_text = f"Sorry, I encountered an error processing your question: {str(e)}"
            return {
                'answer': response_text,
                'citations': [],
                'retrieved_chunks_used': [],
                'timestamp': datetime.now().isoformat()
            }


@app.on_event("startup")
async def startup_event():
    """Initialize the SimpleBookAgent when the application starts"""
    global book_agent

    # Get configuration from environment
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.3'))

    logger.info(f"Initializing SimpleBookAgent with model: {model}, temperature: {temperature}")

    try:
        # Initialize the BookRetriever and SimpleBookAgent
        logger.info("Creating BookRetriever...")
        retriever = BookRetriever()
        logger.info("BookRetriever created successfully")

        logger.info("Creating SimpleBookAgent...")
        book_agent = SimpleBookAgent(
            retriever=retriever,
            model=model,
            temperature=temperature
        )
        logger.info("SimpleBookAgent created successfully")

        logger.info("SimpleBookAgent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize SimpleBookAgent: {e}")
        import traceback
        traceback.print_exc()
        raise


@app.get("/")
async def root():
    """Root endpoint for health check"""
    try:
        logger.info("Root endpoint called")
        return {"message": "Book Content Chat API is running", "status": "healthy"}
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process a user message and return an AI response.
    This endpoint accepts a user message and session ID, uses the SimpleBookAgent
    to generate a context-aware response, and returns the answer with source citations.
    """
    try:
        logger.info(f"Received chat request for session: {request.session_id}")

        # Validate input
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        if not request.session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        # Get or initialize session
        if request.session_id not in session_storage:
            session_storage[request.session_id] = []

        # Add user message to session history
        user_message = {
            "id": f"user_{len(session_storage[request.session_id])}",
            "content": request.message,
            "sender_type": "user",
            "timestamp": datetime.now().isoformat()
        }
        session_storage[request.session_id].append(user_message)

        # Process the request with the SimpleBookAgent
        logger.info("Calling book_agent.answer()...")
        result = await book_agent.answer(request.message)
        logger.info(f"Got result from book_agent.answer(): {type(result)}")

        # Extract response components
        answer = result.get('answer', 'Sorry, I could not generate a response.')
        retrieved_chunks = result.get('retrieved_chunks_used', [])

        logger.info(f"Answer: {answer[:50]}...")
        logger.info(f"Retrieved chunks count: {len(retrieved_chunks)}")

        # Format citations from retrieved chunks
        citations = []
        for chunk in retrieved_chunks:
            source_url = chunk.get('source_url', '')
            metadata_title = chunk.get('metadata', {}).get('title', 'Book Content')

            if source_url:  # Only add citation if there's a URL
                citations.append(Citation(url=source_url, title=metadata_title))

        # Create response
        response = ChatResponse(
            answer=answer,
            citations=citations,
            session_id=request.session_id,
            timestamp=datetime.now().isoformat(),
            metadata={"retrieved_chunks_count": len(retrieved_chunks)}
        )

        # Add agent response to session history
        agent_message = {
            "id": f"agent_{len(session_storage[request.session_id])}",
            "content": answer,
            "sender_type": "agent",
            "timestamp": datetime.now().isoformat(),
            "citations": [c.dict() for c in citations]
        }
        session_storage[request.session_id].append(agent_message)

        logger.info(f"Processed chat request successfully for session: {request.session_id}")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        import traceback
        traceback.print_exc()

        # Return error response
        error_response = ErrorResponse(
            error="INTERNAL_ERROR",
            message=f"An error occurred while processing your request: {str(e)}",
            timestamp=datetime.now().isoformat()
        )

        # Log the error and return 500
        raise HTTPException(status_code=500, detail=error_response.dict())


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get the conversation history for a specific session.
    This is useful for frontend to retrieve previous messages.
    """
    if session_id not in session_storage:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "messages": session_storage[session_id],
        "message_count": len(session_storage[session_id])
    }


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clear the conversation history for a specific session.
    """
    if session_id not in session_storage:
        raise HTTPException(status_code=404, detail="Session not found")

    # Clear the session
    session_storage[session_id] = []

    return {"message": f"Session {session_id} cleared successfully"}


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "NOT_FOUND",
        "message": "The requested resource was not found",
        "timestamp": datetime.now().isoformat()
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "INTERNAL_ERROR",
        "message": "An internal server error occurred",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)