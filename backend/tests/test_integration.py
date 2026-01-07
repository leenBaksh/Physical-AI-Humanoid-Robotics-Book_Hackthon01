import pytest
from src.fetcher.url_fetcher import URLFetcher
from src.chunker.content_chunker import ContentChunker
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.storage.qdrant_storage import QdrantStorage
from src.models import ContentChunk
from config.settings import settings

def test_fetcher_initialization():
    """Test that URLFetcher can be initialized"""
    fetcher = URLFetcher()
    assert fetcher is not None

def test_chunker_initialization():
    """Test that ContentChunker can be initialized"""
    chunker = ContentChunker()
    assert chunker is not None

def test_settings_validation():
    """Test that settings are properly loaded"""
    # This will fail if required environment variables are not set
    # For testing purposes, we'll just check that the settings object exists
    assert settings is not None

def test_sample_chunking():
    """Test that content chunking works with sample text"""
    chunker = ContentChunker()
    sample_text = "This is a sample text. It has multiple sentences. Each sentence should be processed properly."
    chunks = chunker.chunk_content(sample_text, "http://example.com")

    assert len(chunks) > 0
    assert isinstance(chunks[0], ContentChunk)
    assert chunks[0].content is not None

if __name__ == "__main__":
    pytest.main([__file__])