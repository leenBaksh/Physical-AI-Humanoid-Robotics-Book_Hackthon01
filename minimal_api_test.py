#!/usr/bin/env python3
"""
Minimal API test to isolate the middleware error.
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


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)