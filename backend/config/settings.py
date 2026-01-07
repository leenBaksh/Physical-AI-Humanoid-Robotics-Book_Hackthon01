import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the RAG embeddings pipeline"""

    # Cohere API settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_content_chunks")

    # Content processing settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    OVERLAP_SIZE: int = int(os.getenv("OVERLAP_SIZE", "50"))

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Validation
    def validate(self):
        """Validate that required settings are present"""
        if not self.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is required")
        if not self.QDRANT_URL:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.QDRANT_API_KEY:
            raise ValueError("QDRANT_API_KEY environment variable is required")

# Global settings instance
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)