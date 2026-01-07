#!/usr/bin/env python3
"""
Test script for the retrieval functionality.
This script tests the retrieval components from agent.py and related modules.
"""

import asyncio
import sys
import os

# Add the project root and backend to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

try:
    from agent import BookRetriever, retrieve_qdrant_chunks, retrieve_qdrant_chunks_impl
except ImportError as e:
    print(f"Could not import from agent module: {e}")
    sys.exit(1)


async def test_retrieval_functionality():
    """Test the retrieval functionality directly"""

    print("Testing retrieval functionality...")

    # Test the retrieve_qdrant_chunks_impl function directly
    try:
        print("Testing retrieve_qdrant_chunks_impl function...")
        result = retrieve_qdrant_chunks_impl("What is ROS2?", top_k=3)

        print(f"Retrieved {len(result)} chunks")
        if result:
            print("Sample result:")
            print(f"  Content: {result[0]['content'][:100]}...")
            print(f"  Source URL: {result[0]['source_url']}")
            print(f"  Score: {result[0]['score']}")
            print(f"  Chunk Index: {result[0]['chunk_index']}")
            print("SUCCESS: Retrieval function working correctly")
            return True
        else:
            print("WARNING: No chunks retrieved, but function executed without error")
            return True

    except Exception as e:
        print(f"ERROR in retrieval function: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_book_retriever_class():
    """Test the BookRetriever class"""

    print("\nTesting BookRetriever class...")

    try:
        # Initialize the BookRetriever
        retriever = BookRetriever()
        print("BookRetriever initialized successfully")

        # Test the retrieve method
        result = retriever.retrieve("What is ROS2?", top_k=2)

        print(f"Retrieved {len(result)} chunks using BookRetriever")
        if result:
            print("Sample result from BookRetriever:")
            print(f"  Content: {result[0]['content'][:100]}...")
            print(f"  Source URL: {result[0]['source_url']}")
            print("SUCCESS: BookRetriever class working correctly")
            return True
        else:
            print("WARNING: No chunks retrieved from BookRetriever, but function executed without error")
            return True

    except Exception as e:
        print(f"ERROR in BookRetriever: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_edge_cases():
    """Test edge cases for retrieval"""

    print("\nTesting edge cases...")

    try:
        # Test with empty query
        print("Testing with empty query...")
        result = retrieve_qdrant_chunks_impl("", top_k=3)
        if len(result) == 0:
            print("SUCCESS: Empty query handled correctly (returned empty list)")
        else:
            print("UNEXPECTED: Empty query returned results")

        # Test with very small top_k
        print("Testing with top_k=1...")
        result = retrieve_qdrant_chunks_impl("ROS2", top_k=1)
        if len(result) <= 1:
            print("SUCCESS: Small top_k handled correctly")
        else:
            print("UNEXPECTED: top_k=1 returned more than 1 result")

        # Test with BookRetriever using different top_k
        retriever = BookRetriever()
        result = retriever.retrieve("humanoid robotics", top_k=5)
        print(f"Retrieved {len(result)} chunks with top_k=5")

        return True

    except Exception as e:
        print(f"ERROR in edge case testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function"""
    print("="*60)
    print("Testing Retrieval Functionality")
    print("="*60)

    # Run the tests
    success1 = await test_retrieval_functionality()
    success2 = await test_book_retriever_class()
    success3 = await test_edge_cases()

    print("\n" + "="*60)
    print("Test Results:")
    print(f"Direct retrieval test: {'PASS' if success1 else 'FAIL'}")
    print(f"BookRetriever class test: {'PASS' if success2 else 'FAIL'}")
    print(f"Edge cases test: {'PASS' if success3 else 'FAIL'}")

    overall_success = success1 and success2 and success3
    if overall_success:
        print("\nOverall: ALL RETRIEVAL TESTS PASSED")
        return True
    else:
        print("\nOverall: SOME RETRIEVAL TESTS FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)