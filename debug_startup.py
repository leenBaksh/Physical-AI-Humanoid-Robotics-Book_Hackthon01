#!/usr/bin/env python3
"""
Debug script to test the startup event separately
"""

import os
import sys

# Add backend directory to path to access Qdrant storage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Testing startup event logic...")

try:
    from agent import BookRetriever, BookAgent, retrieve_qdrant_chunks_impl

    # Get configuration from environment
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.3'))

    print(f"Using model: {model}, temperature: {temperature}")

    # Initialize the BookRetriever and BookAgent (this is what happens in startup_event)
    print("Creating BookRetriever...")
    retriever = BookRetriever()
    print("BookRetriever created successfully")

    print("Creating BookAgent...")
    book_agent = BookAgent(
        retriever=retriever,
        model=model,
        temperature=temperature
    )
    print("BookAgent created successfully")

    print("Testing book_agent.answer()...")
    import asyncio

    async def test_answer():
        result = await book_agent.answer("Hello")
        print(f"Answer: {result['answer'][:100]}...")
        print(f"Citations: {len(result.get('citations', []))}")
        print(f"Retrieved chunks: {len(result.get('retrieved_chunks_used', []))}")

    asyncio.run(test_answer())

    print("SUCCESS: Startup event logic works correctly!")

except Exception as e:
    print(f"ERROR during startup event test: {e}")
    import traceback
    traceback.print_exc()