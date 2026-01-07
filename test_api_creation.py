#!/usr/bin/env python3
"""
Test to see if creating the exact same API will trigger the issue
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

print("Creating FastAPI app with CORS middleware...")

try:
    # Initialize FastAPI app
    app = FastAPI(
        title="Book Content Chat API",
        description="API for interacting with the Book Content RAG agent",
        version="1.0.0"
    )

    print("FastAPI app created successfully")

    # Configure CORS middleware for local development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for local development
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )

    print("CORS middleware added successfully")

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

    print("Models and storage created successfully")

    @app.get("/")
    async def root():
        """Root endpoint for health check"""
        return {"message": "Book Content Chat API is running", "status": "healthy"}

    print("Route added successfully")

    print("Testing the app creation...")

    # Try to access the middleware stack to see if the error occurs
    print("Accessing middleware stack...")
    print(f"App middleware: {app.user_middleware}")

    print("SUCCESS: App created without error!")

except Exception as e:
    print(f"ERROR during app creation: {e}")
    import traceback
    traceback.print_exc()