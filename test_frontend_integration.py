#!/usr/bin/env python3
"""
Test the frontend integration with the backend API
"""

import requests
import time
import subprocess
import signal
import os

def test_api_connection():
    """Test if the API is accessible"""
    print("Testing API connection...")

    try:
        # Test the health endpoint
        response = requests.get("http://localhost:8002/", timeout=5)
        print(f"Health check - Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] API is accessible")
            return True
        else:
            print(f"[ERROR] API returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API connection failed: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\nTesting chat endpoint...")

    try:
        payload = {
            "message": "Hello",
            "session_id": "test-session-frontend"
        }

        response = requests.post(
            "http://localhost:8002/chat",
            json=payload,
            timeout=10
        )

        print(f"Chat endpoint - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Chat response received")
            print(f"Answer preview: {data.get('answer', '')[:50]}...")
            return True
        else:
            print(f"[ERROR] Chat endpoint returned status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Chat endpoint test failed: {e}")
        return False

def main():
    print("Testing Frontend-Backend Integration")
    print("=" * 50)

    # Wait a moment for server to be ready
    time.sleep(2)

    api_accessible = test_api_connection()

    if api_accessible:
        chat_working = test_chat_endpoint()

        print("\n" + "=" * 50)
        print("INTEGRATION TEST RESULTS:")
        print(f"[SUCCESS] API Connection: {'PASS' if api_accessible else 'FAIL'}")
        print(f"[SUCCESS] Chat Endpoint: {'PASS' if chat_working else 'FAIL'}")

        if api_accessible and chat_working:
            print("\n[SUCCESS] Frontend-Backend Integration: SUCCESS")
            print("[READY] Chatbot UI will work with the backend API")
        else:
            print("\n[ERROR] Integration Issues Detected")
    else:
        print("\n❌ Cannot connect to backend API")
        print("💡 Please ensure the API server is running on port 8002")

if __name__ == "__main__":
    main()