#!/usr/bin/env python3
"""
Main entry point for the RAG embeddings pipeline.
This script orchestrates the full pipeline: fetch → chunk → embed → store
"""


import sys
import os
import logging
from typing import List
import argparse

# Add the backend directory to Python path to resolve imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from src.fetcher.url_fetcher import URLFetcher
from src.chunker.content_chunker import ContentChunker
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.storage.qdrant_storage import QdrantStorage
from src.models import ContentChunk

logger = logging.getLogger(__name__)

def main(urls: List[str], include_subpages: bool = False):
    """
    Main function to orchestrate the full pipeline: fetch → chunk → embed → store
    """
    print("Starting RAG embeddings pipeline...")
    logger.info("Starting RAG embeddings pipeline...")

    # Validate settings
    try:
        settings.validate()
        logger.info("Settings validated successfully")
    except ValueError as e:
        logger.error(f"Settings validation failed: {e}")
        print(f"Error: {e}")
        sys.exit(1)

    # Initialize components
    fetcher = URLFetcher()
    chunker = ContentChunker()
    embedder = EmbeddingGenerator()
    storage = QdrantStorage()

    try:
        # 1. Fetch URLs
        print("Step 1: Fetching content from URLs...")
        logger.info("Fetching content from URLs...")
        fetched_content = fetcher.fetch_urls(urls, include_subpages=include_subpages)
        logger.info(f"Fetched content from {len(fetched_content)} URLs")

        # Filter out any failed fetches
        successful_fetches = [item for item in fetched_content if item.get('content')]
        if not successful_fetches:
            logger.error("No content successfully fetched from URLs")
            print("Error: No content successfully fetched from URLs")
            return

        # 2. Chunk content
        print("Step 2: Chunking content...")
        logger.info("Chunking content...")
        all_chunks = []
        for item in successful_fetches:
            content = item.get('content', '')
            source_url = item.get('url', '')
            metadata = item.get('metadata', {})
            if content:
                chunks = chunker.chunk_content(content, source_url, metadata)
                all_chunks.extend(chunks)
        logger.info(f"Created {len(all_chunks)} content chunks")

        if not all_chunks:
            logger.error("No content chunks created")
            print("Error: No content chunks created")
            return

        # 3. Generate embeddings
        print("Step 3: Generating embeddings...")
        logger.info("Generating embeddings...")
        chunks_with_embeddings = embedder.generate_embeddings(all_chunks)
        chunks_with_embeddings = [chunk for chunk in chunks_with_embeddings if chunk.embedding is not None]
        logger.info(f"Generated embeddings for {len(chunks_with_embeddings)} chunks")

        if not chunks_with_embeddings:
            logger.error("No embeddings generated")
            print("Error: No embeddings generated")
            return

        # 4. Store in Qdrant
        print("Step 4: Storing embeddings in Qdrant...")
        logger.info("Storing embeddings in Qdrant...")
        storage_result = storage.store_in_qdrant(chunks_with_embeddings)
        logger.info(f"Storage result: {storage_result}")

        print("Pipeline completed successfully!")
        logger.info("Pipeline completed successfully!")
        print(f"Stored {storage_result['inserted_count']} vectors in Qdrant")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        print(f"Error: Pipeline failed: {str(e)}")
        sys.exit(1)

def cli_main():
    """
    Command-line interface for the pipeline
    """
    parser = argparse.ArgumentParser(description="RAG Embeddings Pipeline")
    parser.add_argument("urls", nargs="+", help="URLs to process")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--include-subpages", action="store_true",
                       help="Include subpages by discovering URLs from sitemap and crawling")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # For CLI usage, we'll pass the include_subpages parameter to main
    main(args.urls, include_subpages=args.include_subpages)

if __name__ == "__main__":
    cli_main()
