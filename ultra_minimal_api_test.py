#!/usr/bin/env python3
"""
Ultra minimal API test to isolate the middleware error.
"""

import os
import sys
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app WITHOUT any middleware
app = FastAPI(
    title="Book Content Chat API",
    description="API for interacting with the Book Content RAG agent",
    version="1.0.0"
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