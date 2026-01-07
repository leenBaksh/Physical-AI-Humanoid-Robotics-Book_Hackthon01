import cohere
import logging
import sys
import os
from typing import List, Dict, Any
import hashlib

# Add the backend directory to Python path to resolve imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from src.models import ContentChunk
from config.settings import settings
from src.utils import handle_exceptions, log_execution_time, CustomException

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Class to generate embeddings using Cohere API
    """

    def __init__(self):
        if not settings.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(settings.COHERE_API_KEY)
        self.model = "small"  # Using smaller model that should have lower rate limits
        self._cache = {}  # Simple in-memory cache for embeddings

    def _get_cache_key(self, text: str) -> str:
        """
        Generate a cache key for the given text
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _get_cached_embedding(self, text: str) -> List[float]:
        """
        Get embedding from cache if available
        """
        cache_key = self._get_cache_key(text)
        return self._cache.get(cache_key)

    def _cache_embedding(self, text: str, embedding: List[float]):
        """
        Cache the embedding for the given text
        """
        cache_key = self._get_cache_key(text)
        self._cache[cache_key] = embedding

    @handle_exceptions
    @log_execution_time
    def generate_embeddings(self, chunks: List[ContentChunk]) -> List[ContentChunk]:
        """
        Generate embeddings for a list of content chunks
        """
        if not chunks:
            logger.warning("No chunks provided for embedding generation")
            return []

        # Extract text content from chunks and identify which need embeddings
        texts_to_process = []
        text_to_chunk_map = {}  # Maps text to its chunk index for later assignment

        for i, chunk in enumerate(chunks):
            if chunk.content:
                # Check if we already have this text cached
                cached_embedding = self._get_cached_embedding(chunk.content)
                if cached_embedding:
                    chunk.embedding = cached_embedding
                    logger.info(f"Used cached embedding for chunk {i}")
                else:
                    texts_to_process.append(chunk.content)
                    text_to_chunk_map[chunk.content] = i

        if not texts_to_process:
            logger.info("All chunks had cached embeddings, no API calls needed")
            return chunks

        # Generate embeddings in batches to respect API limits
        batch_size = 96  # Cohere's recommended batch size
        all_embeddings = []
        processed_texts = []

        for i in range(0, len(texts_to_process), batch_size):
            batch = texts_to_process[i:i + batch_size]

            try:
                response = self.client.embed(
                    texts=batch,
                    model=self.model
                )

                batch_embeddings = response.embeddings
                all_embeddings.extend(batch_embeddings)
                processed_texts.extend(batch)

                logger.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(texts_to_process)-1)//batch_size + 1}")

                # Add a small delay to respect API rate limits
                import time
                time.sleep(0.1)  # 100ms delay between batches

            except Exception as e:
                logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                # Implement retry logic for rate limit errors
                if "rate limit" in str(e).lower() or "429" in str(e).lower() or "Please wait and try again later" in str(e):
                    import time
                    logger.info("Rate limit hit, waiting before retry...")
                    time.sleep(15)  # Wait 15 seconds before retry (increased from 10)
                    try:
                        # Retry the batch
                        response = self.client.embed(
                            texts=batch,
                            model=self.model
                        )
                        batch_embeddings = response.embeddings
                        all_embeddings.extend(batch_embeddings)
                        processed_texts.extend(batch)
                        logger.info(f"Successfully retried batch {i//batch_size + 1}")
                    except Exception as retry_error:
                        logger.error(f"Retry failed for batch {i//batch_size + 1}: {str(retry_error)}")
                        # Try one more time with a longer wait
                        time.sleep(30)  # Wait 30 seconds for second retry
                        try:
                            response = self.client.embed(
                                texts=batch,
                                model=self.model
                            )
                            batch_embeddings = response.embeddings
                            all_embeddings.extend(batch_embeddings)
                            processed_texts.extend(batch)
                            logger.info(f"Successfully retried batch {i//batch_size + 1} on second attempt")
                        except Exception as second_retry_error:
                            logger.error(f"Second retry failed for batch {i//batch_size + 1}: {str(second_retry_error)}")
                            raise CustomException(f"Embedding generation failed after multiple retries: {str(second_retry_error)}", "EMBEDDING_GENERATION_ERROR")
                else:
                    raise CustomException(f"Embedding generation failed: {str(e)}", "EMBEDDING_GENERATION_ERROR")

        # Update chunks with embeddings and cache them
        for text, embedding in zip(processed_texts, all_embeddings):
            chunk_idx = text_to_chunk_map[text]
            chunks[chunk_idx].embedding = embedding
            # Cache the embedding for future use
            self._cache_embedding(text, embedding)

        logger.info(f"Successfully generated embeddings for {len(processed_texts)} new chunks")
        return chunks

    @handle_exceptions
    @log_execution_time
    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate a single embedding for a text
        """
        if not text:
            raise CustomException("Text cannot be empty for embedding generation", "EMPTY_TEXT_ERROR")

        # Check if embedding is already cached
        cached_embedding = self._get_cached_embedding(text)
        if cached_embedding:
            logger.info("Using cached embedding for single text")
            return cached_embedding

        try:
            response = self.client.embed(
                texts=[text],
                model=self.model
            )

            embeddings = response.embeddings
            if embeddings and len(embeddings) > 0:
                embedding = embeddings[0]
                # Cache the embedding for future use
                self._cache_embedding(text, embedding)
                return embedding
            else:
                raise CustomException("No embeddings returned from Cohere API", "NO_EMBEDDINGS_ERROR")

        except Exception as e:
            logger.error(f"Error generating single embedding: {str(e)}")
            # Handle rate limit errors specifically
            if "rate limit" in str(e).lower() or "429" in str(e).lower() or "Please wait and try again later" in str(e):
                import time
                logger.info("Rate limit hit for single embedding, waiting before retry...")
                time.sleep(15)  # Wait before retry
                try:
                    response = self.client.embed(
                        texts=[text],
                        model=self.model
                    )
                    embeddings = response.embeddings
                    if embeddings and len(embeddings) > 0:
                        embedding = embeddings[0]
                        # Cache the embedding for future use
                        self._cache_embedding(text, embedding)
                        return embedding
                    else:
                        raise CustomException("No embeddings returned from Cohere API", "NO_EMBEDDINGS_ERROR")
                except Exception as retry_error:
                    logger.error(f"Retry failed for single embedding: {str(retry_error)}")
                    raise CustomException(f"Single embedding generation failed after retry: {str(retry_error)}", "SINGLE_EMBEDDING_ERROR")
            else:
                raise CustomException(f"Single embedding generation failed: {str(e)}", "SINGLE_EMBEDDING_ERROR")

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that an embedding is properly formed
        """
        if not embedding or not isinstance(embedding, list):
            return False

        # Check that all values are numbers
        if not all(isinstance(val, (int, float)) for val in embedding):
            return False

        # Embeddings should have reasonable length (Cohere typically returns 1024 dimensions)
        if len(embedding) == 0:
            return False

        return True