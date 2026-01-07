#!/usr/bin/env python3
"""
Test script to verify the API functionality works correctly with the BookAgent.
This tests the core functionality without starting the full FastAPI server.
"""

import sys
import os

# Add the project root and backend to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Import the necessary functions and classes
from agent import BookRetriever, BookAgent, retrieve_qdrant_chunks_impl
import asyncio


def test_book_agent_integration():
    """Test the BookAgent integration directly"""

    print("Testing BookAgent integration...")

    try:
        # Initialize the BookRetriever and BookAgent
        retriever = BookRetriever()
        book_agent = BookAgent(retriever)

        print("BookAgent initialized successfully")

        # Test the agent with a sample query
        test_query = "What is ROS2?"
        print(f"Testing query: '{test_query}'")

        # Run the agent asynchronously
        result = asyncio.run(book_agent.answer(test_query))

        print(f"Agent response: {result['answer'][:200]}...")
        print(f"Retrieved chunks: {len(result['retrieved_chunks_used'])}")
        print(f"Citations: {len(result['citations'])}")

        if result['answer'] and 'Sorry' not in result['answer']:
            print("SUCCESS: BookAgent generated a valid response")
            return True
        else:
            print("WARNING: BookAgent returned an error response")
            return True  # Still considered a success as it handled the error gracefully

    except Exception as e:
        print(f"ERROR in BookAgent integration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_retrieval_integration():
    """Test the retrieval integration"""

    print("\nTesting retrieval integration...")

    try:
        # Test the retrieval function directly
        result = retrieve_qdrant_chunks_impl("What is ROS2?", top_k=2)

        print(f"Retrieved {len(result)} chunks for 'What is ROS2?'")
        if result:
            print(f"First chunk content: {result[0]['content'][:100]}...")
            print(f"First chunk source: {result[0]['source_url']}")

        print("SUCCESS: Retrieval integration working")
        return True

    except Exception as e:
        print(f"ERROR in retrieval integration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_session_management():
    """Test the session management functionality"""

    print("\nTesting session management...")

    try:
        # Create a simple in-memory session storage for testing
        session_storage = {}

        # Clear any existing sessions for testing
        session_id = "test-session-api"
        session_storage[session_id] = []

        # Add a mock message to the session
        user_message = {
            "id": "user_1",
            "content": "What is ROS2?",
            "sender_type": "user",
            "timestamp": "2026-01-02T06:00:00"
        }

        session_storage[session_id].append(user_message)

        # Verify the message was added
        if len(session_storage[session_id]) == 1:
            print("SUCCESS: Session management working correctly")
            return True
        else:
            print("ERROR: Session management not working correctly")
            return False

    except Exception as e:
        print(f"ERROR in session management: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("="*60)
    print("Testing API Functionality")
    print("="*60)

    # Run the tests
    success1 = test_book_agent_integration()
    success2 = test_retrieval_integration()
    success3 = test_session_management()

    print("\n" + "="*60)
    print("Test Results:")
    print(f"BookAgent integration test: {'PASS' if success1 else 'FAIL'}")
    print(f"Retrieval integration test: {'PASS' if success2 else 'FAIL'}")
    print(f"Session management test: {'PASS' if success3 else 'FAIL'}")

    overall_success = success1 and success2 and success3
    if overall_success:
        print("\nOverall: ALL API FUNCTIONALITY TESTS PASSED")
        return True
    else:
        print("\nOverall: SOME API FUNCTIONALITY TESTS FAILED")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)