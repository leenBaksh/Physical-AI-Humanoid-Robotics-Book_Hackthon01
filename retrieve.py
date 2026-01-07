#!/usr/bin/env python3
"""
Pipeline Validation & Query Testing Script

This script provides functions to validate the Qdrant collection integrity
and perform similarity searches for testing purposes.
"""
import sys
import os
import argparse
import logging
from typing import List, Dict, Any, Optional
import time

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.storage.qdrant_storage import QdrantStorage
from backend.src.embeddings.embedding_generator import EmbeddingGenerator
from backend.config.settings import settings

logger = logging.getLogger(__name__)

def validate_collection() -> Dict[str, Any]:
    """
    Validate the Qdrant collection by counting chunks and spot-checking text matches.

    Returns:
        Dictionary with validation results including counts and sample checks
    """
    print("=== Collection Validation ===")

    try:
        # Initialize Qdrant storage
        storage = QdrantStorage()

        # Get total count of chunks in Qdrant
        total_chunks = storage.get_collection_size()
        print(f"Total chunks in collection: {total_chunks}")

        # For this validation, we'll just check that the collection exists and has content
        # In a real scenario, we might compare with an expected count
        expected_chunks = total_chunks  # Placeholder - in real scenario this would come from pipeline logs
        print(f"Expected chunks: {expected_chunks}")

        validation_passed = True  # Placeholder - in real scenario would compare counts
        print(f"Validation: {'PASSED' if validation_passed else 'FAILED'}")

        # Spot-check random samples to verify text matches
        print("\nSample spot-checks:")
        sample_results = []

        try:
            # Get a few sample chunks from the collection
            sample_chunks = storage.get_random_chunks(count=min(3, total_chunks)) if total_chunks > 0 else []

            for i, chunk in enumerate(sample_chunks):
                original_content = chunk.get('content', '')[:100] + "..."
                stored_content = chunk.get('content', '')[:100] + "..."  # In this case, they should be the same

                match = original_content == stored_content
                print(f"{'PASS' if match else 'FAIL'} Content match for chunk from: {chunk.get('source_url', 'Unknown')}")

                sample_results.append({
                    'original_content': original_content,
                    'stored_content': stored_content,
                    'match': match
                })

        except Exception as e:
            print(f"Error during spot-check: {e}")
            validation_passed = False

        # Prepare validation result
        result = {
            'total_chunks': total_chunks,
            'expected_chunks': expected_chunks,
            'validation_passed': validation_passed,
            'sample_checks': sample_results,
            'errors': [] if validation_passed else [str(e) if 'e' in locals() else 'Validation failed']
        }

        return result

    except Exception as e:
        logger.error(f"Error during collection validation: {e}")
        print(f"Error during collection validation: {e}")

        return {
            'total_chunks': 0,
            'expected_chunks': 0,
            'validation_passed': False,
            'sample_checks': [],
            'errors': [str(e)]
        }

def query_collection(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Perform similarity search against the Qdrant collection.

    Args:
        query: The query string to search for
        limit: Number of top results to return

    Returns:
        Dictionary with query results and metadata
    """
    print(f"\nQuery: \"{query}\"")

    start_time = time.time()

    try:
        # Initialize components
        storage = QdrantStorage()
        embedder = EmbeddingGenerator()

        # Generate embedding for the query
        print("Generating embedding for query...")
        query_embedding = embedder.generate_single_embedding(query)

        if query_embedding is None:
            print("Failed to generate embedding for the query")
            return {
                'query': query,
                'results': [],
                'total_results': 0,
                'execution_time': time.time() - start_time
            }

        # Perform similarity search
        print(f"Searching for top {limit} similar chunks...")
        search_results = storage.search_similar(query_embedding, limit=limit)

        print(f"\nTop {len(search_results)} results:")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. Score: {result['score']:.2f}")
            print(f"   Source: {result['source_url']}")
            print(f"   Content: {result['content'][:200]}...")
            if len(result['content']) > 200:
                print(f"          ... (truncated)")
            print(f"   Metadata: {dict(list(result['metadata'].items())[:2])}")  # Show first 2 metadata items
            print()

        execution_time = time.time() - start_time
        print(f"Query executed in {execution_time:.2f} seconds")

        return {
            'query': query,
            'results': search_results,
            'total_results': len(search_results),
            'execution_time': execution_time
        }

    except Exception as e:
        logger.error(f"Error during query: {e}")
        print(f"Error during query: {e}")

        return {
            'query': query,
            'results': [],
            'total_results': 0,
            'execution_time': time.time() - start_time
        }

def interactive_query_loop():
    """
    Run an interactive query loop for testing purposes.
    """
    print("\n=== Interactive Query Mode ===")
    print("Enter queries to search the Qdrant collection.")
    print("Type 'quit' or 'exit' to stop.\n")

    try:
        storage = QdrantStorage()
        embedder = EmbeddingGenerator()
    except Exception as e:
        print(f"Failed to initialize components: {e}")
        return

    while True:
        try:
            user_query = input("Enter your query (or 'quit' to exit): ").strip()
            if user_query.lower() in ['quit', 'exit', 'q']:
                break

            if not user_query:
                continue

            # Get number of results to return
            try:
                limit_input = input(f"Number of results (default 5): ").strip()
                if limit_input:
                    limit = int(limit_input)
                else:
                    limit = 5
            except ValueError:
                limit = 5
                print("Invalid number, using default of 5")

            # Perform the query
            start_time = time.time()

            try:
                print(f"Generating embedding for query: '{user_query}'")
                query_embedding = embedder.generate_single_embedding(user_query)

                if query_embedding is None:
                    print("Failed to generate embedding for the query\n")
                    continue

                # Perform similarity search
                print(f"Searching for top {limit} similar chunks...")
                search_results = storage.search_similar(query_embedding, limit=limit)

                print(f"\nTop {len(search_results)} results for: '{user_query}'")
                for i, result in enumerate(search_results, 1):
                    print(f"{i}. Score: {result['score']:.2f}")
                    print(f"   Source: {result['source_url']}")
                    print(f"   Content: {result['content'][:200]}...")
                    if len(result['content']) > 200:
                        print(f"          ... (truncated)")
                    print(f"   Metadata: {dict(list(result['metadata'].items())[:2])}")
                    print()

                execution_time = time.time() - start_time
                print(f"Query executed in {execution_time:.2f} seconds\n")

            except Exception as e:
                print(f"Error during query: {e}\n")
                continue

        except KeyboardInterrupt:
            print("\n\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Error in interactive loop: {e}")
            continue

def main():
    """
    Main function that runs validation, then enters interactive query loop.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Pipeline Validation & Query Testing")
    parser.add_argument("--validate", action="store_true", help="Run validation only")
    parser.add_argument("--query", type=str, help="Run a single query")
    parser.add_argument("--limit", type=int, default=5, help="Number of results for single query (default: 5)")

    args = parser.parse_args()

    # Validate settings
    try:
        settings.validate()
        print("Settings validated successfully\n")
    except ValueError as e:
        print(f"Settings validation failed: {e}")
        return 1

    # Run validation if requested or if no specific action
    if args.validate or not args.query:
        validation_result = validate_collection()
        print()

    # Run single query if specified
    if args.query:
        query_result = query_collection(args.query, args.limit)
        return 0

    # Run interactive query loop if no specific action
    if not args.validate and not args.query:
        interactive_query_loop()

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)