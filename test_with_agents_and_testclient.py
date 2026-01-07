#!/usr/bin/env python3
"""
Test to see if the issue occurs when using TestClient with agent import
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

# Import the agent components - this might cause the issue
print("Importing agent components...")
from agent import BookRetriever, BookAgent, retrieve_qdrant_chunks_impl
print("Agent components imported successfully")

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

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "Book Content Chat API is running", "status": "healthy"}

print("Testing with TestClient...")

try:
    from fastapi.testclient import TestClient

    client = TestClient(app)
    print("TestClient created successfully")

    print("Making request to root endpoint...")
    response = client.get("/")
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")

except Exception as e:
    print(f"ERROR during TestClient request: {e}")
    import traceback
    traceback.print_exc()