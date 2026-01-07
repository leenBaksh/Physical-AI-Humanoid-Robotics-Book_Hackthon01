#!/usr/bin/env python3
"""
Test script to call the fixed API endpoint directly and capture errors
"""

import asyncio
import sys
import os

from api_fixed import app
from fastapi.testclient import TestClient

def test_api():
    print("Testing fixed API with TestClient...")

    try:
        client = TestClient(app)

        print("Testing root endpoint...")
        response = client.get("/")
        print(f"Root endpoint response: {response.status_code}")
        print(f"Response content: {response.text}")

        print("\nTesting chat endpoint...")
        chat_data = {
            "message": "Hello",
            "session_id": "test-session"
        }
        response = client.post("/chat", json=chat_data)
        print(f"Chat endpoint response: {response.status_code}")
        print(f"Response content: {response.text}")

    except Exception as e:
        print(f"Error during API test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()