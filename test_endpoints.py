#!/usr/bin/env python3
"""
Test the API endpoints directly
"""

import sys
from api import app
from fastapi.testclient import TestClient

print("Testing API endpoints...")

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