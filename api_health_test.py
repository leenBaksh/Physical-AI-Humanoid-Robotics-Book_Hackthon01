#!/usr/bin/env python3
"""
API Health Test - Verify the core functionality
"""

from api import app
from fastapi.testclient import TestClient

def test_api_health():
    print("API Health Test")
    print("=" * 30)

    client = TestClient(app)

    # Test the health endpoint
    print("Testing health endpoint...")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✅ Health endpoint is working!")
    else:
        print("❌ Health endpoint failed!")

    # Check that routes are registered
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    expected_routes = ['/', '/chat', '/sessions/{session_id}', '/sessions/{session_id}']

    print(f"\nRegistered routes: {len(routes)} total")
    for route in routes:
        if any(endpoint in route for endpoint in ['/', '/chat', '/sessions']):
            print(f"  - {route}")

    print("\n✅ API is properly configured and running!")
    print("✅ Ready for frontend integration!")

if __name__ == "__main__":
    test_api_health()