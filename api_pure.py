#!/usr/bin/env python3
"""
Minimal API test to completely isolate the issue.
This version imports nothing that might trigger the agents library.
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    Process a user message and return a mock AI response.
    This is a mock implementation for testing purposes.
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

        # Mock response for testing
        response = ChatResponse(
            answer="This is a mock response for testing purposes.",
            citations=[Citation(url="https://example.com", title="Example Source")],
            session_id=request.session_id,
            timestamp=datetime.now().isoformat(),
            metadata={"retrieved_chunks_count": 0}
        )

        # Add agent response to session history
        agent_message = {
            "id": f"agent_{len(session_storage[request.session_id])}",
            "content": response.answer,
            "sender_type": "agent",
            "timestamp": datetime.now().isoformat(),
            "citations": [c.dict() for c in response.citations]
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


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)