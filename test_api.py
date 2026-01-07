#!/usr/bin/env python3
"""
Test script for the FastAPI backend API.
This script tests the /chat endpoint functionality.
"""

import asyncio
import json
import aiohttp
import sys
import os

# Add the project root to the path to access agent.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_chat_endpoint():
    """Test the /chat endpoint with sample data"""

    # Sample test data
    test_payload = {
        "message": "What is ROS2?",
        "session_id": "test-session-123",
        "options": {
            "top_k": 5,
            "temperature": 0.3
        }
    }

    # Define the API endpoint
    url = "http://localhost:8000/chat"

    print("Testing the /chat endpoint...")
    print(f"Sending request to: {url}")
    print(f"Payload: {json.dumps(test_payload, indent=2)}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=test_payload) as response:
                print(f"Response Status: {response.status}")

                if response.status == 200:
                    response_data = await response.json()
                    print("Response Data:")
                    print(json.dumps(response_data, indent=2))

                    # Validate response structure
                    required_fields = ["answer", "citations", "session_id", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in response_data]

                    if missing_fields:
                        print(f"ERROR: Missing required fields in response: {missing_fields}")
                        return False
                    else:
                        print("SUCCESS: Response contains all required fields")

                    # Check if citations is a list
                    if not isinstance(response_data.get("citations"), list):
                        print("ERROR: citations field should be a list")
                        return False

                    print("SUCCESS: Response structure is valid")
                    return True
                elif response.status == 422:
                    error_data = await response.json()
                    print(f"Validation Error: {json.dumps(error_data, indent=2)}")
                    return False
                else:
                    error_text = await response.text()
                    print(f"Error Response: {error_text}")
                    return False

    except aiohttp.ClientConnectorError:
        print("ERROR: Cannot connect to the API server. Please make sure the FastAPI server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"ERROR: An exception occurred during the test: {str(e)}")
        return False


async def test_invalid_request():
    """Test the /chat endpoint with invalid data to check error handling"""

    # Invalid test data (missing required fields)
    invalid_payload = {
        "message": "",  # Empty message
        "session_id": "test-session-123"
    }

    url = "http://localhost:8000/chat"

    print("\nTesting the /chat endpoint with invalid data...")
    print(f"Sending request to: {url}")
    print(f"Payload: {json.dumps(invalid_payload, indent=2)}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=invalid_payload) as response:
                print(f"Response Status: {response.status}")

                if response.status in [400, 422]:  # Expected error status codes
                    error_data = await response.json()
                    print(f"Expected Error Response: {json.dumps(error_data, indent=2)}")
                    print("SUCCESS: API properly handles invalid requests")
                    return True
                else:
                    print(f"Unexpected response status: {response.status}")
                    return False

    except aiohttp.ClientConnectorError:
        print("ERROR: Cannot connect to the API server. Please make sure the FastAPI server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"ERROR: An exception occurred during the test: {str(e)}")
        return False


async def main():
    """Main test function"""
    print("="*60)
    print("Testing FastAPI Backend API")
    print("="*60)

    # Test if the API server is running by checking the root endpoint first
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/") as response:
                if response.status == 200:
                    print("✓ API server is running")
                else:
                    print(f"✗ API server may not be running (status: {response.status})")
                    print("Please start the API server using: uvicorn api:app --reload --port 8000")
                    return
    except aiohttp.ClientConnectorError:
        print("✗ API server is not running")
        print("Please start the API server using: uvicorn api:app --reload --port 8000")
        return

    print()

    # Run the tests
    success1 = await test_chat_endpoint()
    success2 = await test_invalid_request()

    print("\n" + "="*60)
    print("Test Results:")
    print(f"Valid request test: {'PASS' if success1 else 'FAIL'}")
    print(f"Invalid request test: {'PASS' if success2 else 'FAIL'}")

    if success1 and success2:
        print("\nOverall: ALL TESTS PASSED")
        return True
    else:
        print("\nOverall: SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)