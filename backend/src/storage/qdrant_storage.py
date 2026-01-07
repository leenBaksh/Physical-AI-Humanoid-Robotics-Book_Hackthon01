from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import logging
import sys
import os
from uuid import uuid4

# Add the backend directory to Python path to resolve imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from src.models import ContentChunk, VectorRecord
from config.settings import settings
from src.utils import handle_exceptions, log_execution_time, CustomException

logger = logging.getLogger(__name__)

class QdrantStorage:
    """
    Class to store embeddings in Qdrant vector database
    """

    def __init__(self):
        if not settings.QDRANT_URL or not settings.QDRANT_API_KEY:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            timeout=10
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    @handle_exceptions
    @log_execution_time
    def store_in_qdrant(self, chunks: List[ContentChunk]) -> Dict[str, Any]:
        """
        Store content chunks with embeddings in Qdrant vector database
        """
        if not chunks:
            logger.warning("No chunks provided for storage")
            return {"inserted_count": 0, "updated_count": 0, "failed_count": 0}

        # Prepare points for Qdrant
        points = []
        for chunk in chunks:
            if chunk.embedding is not None:
                # Prepare payload with content and metadata
                payload = {
                    "content": chunk.content,
                    "source_url": chunk.source_url,
                    "chunk_index": chunk.chunk_index,
                    "created_at": chunk.created_at.isoformat()
                }

                # Add additional metadata if available
                if hasattr(chunk, 'metadata') and chunk.metadata:
                    # Flatten metadata to avoid nested structures that Qdrant might not handle well
                    for key, value in chunk.metadata.items():
                        payload[f"meta_{key}"] = value

                # Create a point with the embedding vector and metadata
                point = models.PointStruct(
                    id=str(uuid4()),  # Generate unique ID
                    vector=chunk.embedding,
                    payload=payload
                )
                points.append(point)

        if not points:
            logger.warning("No chunks with embeddings found for storage")
            return {"inserted_count": 0, "updated_count": 0, "failed_count": 0}

        # Determine vector size from the first embedding and ensure the collection exists
        if points and points[0].vector:
            vector_size = len(points[0].vector)
        else:
            vector_size = 1024  # Default size
        self._ensure_collection_exists(vector_size)

        # Upsert the points to Qdrant
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully stored {len(points)} vectors in Qdrant collection '{self.collection_name}'")
            return {
                "inserted_count": len(points),
                "updated_count": 0,
                "failed_count": 0
            }

        except Exception as e:
            logger.error(f"Error storing vectors in Qdrant: {str(e)}")
            raise CustomException(f"Vector storage failed: {str(e)}", "VECTOR_STORAGE_ERROR")

    def _ensure_collection_exists(self, vector_size: int = 1024):
        """
        Ensure the Qdrant collection exists with appropriate configuration
        """
        try:
            # Try to get collection info to check if it exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Collection doesn't exist, create it
            logger.info(f"Creating collection '{self.collection_name}' with vector size {vector_size}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")

    @handle_exceptions
    @log_execution_time
    def search_similar(self, query_embedding: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the Qdrant collection
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            # Format results
            formatted_results = []
            for result in results:
                # Extract metadata from payload
                payload = result.payload or {}
                metadata = {}

                # Extract any metadata fields that were prefixed with "meta_"
                for key, value in payload.items():
                    if key.startswith("meta_"):
                        metadata[key[5:]] = value  # Remove "meta_" prefix
                    elif key in ["content", "source_url", "chunk_index", "created_at"]:
                        continue  # Skip these as they're handled separately
                    else:
                        metadata[key] = value

                formatted_results.append({
                    "id": result.id,
                    "content": payload.get("content", ""),
                    "source_url": payload.get("source_url", ""),
                    "chunk_index": payload.get("chunk_index", 0),
                    "created_at": payload.get("created_at", ""),
                    "score": result.score,
                    "metadata": metadata
                })

            logger.info(f"Found {len(formatted_results)} similar results")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching for similar vectors: {str(e)}")
            raise CustomException(f"Similarity search failed: {str(e)}", "SIMILARITY_SEARCH_ERROR")

    @handle_exceptions
    @log_execution_time
    def create_collection(self, vector_size: int = 1024):
        """
        Create a Qdrant collection with appropriate configuration for embeddings
        """
        try:
            # Create collection with cosine distance for semantic similarity
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise CustomException(f"Collection creation failed: {str(e)}", "COLLECTION_CREATION_ERROR")

    @handle_exceptions
    @log_execution_time
    def validate_and_optimize_vectors(self, vectors: List[List[float]]) -> List[List[float]]:
        """
        Validate and optimize vectors before storage
        """
        validated_vectors = []
        for i, vector in enumerate(vectors):
            if not self._is_valid_vector(vector):
                logger.warning(f"Invalid vector at index {i}, skipping")
                continue
            validated_vectors.append(vector)

        logger.info(f"Validated {len(validated_vectors)} out of {len(vectors)} vectors")
        return validated_vectors

    def _is_valid_vector(self, vector: List[float]) -> bool:
        """
        Check if a vector is valid for storage
        """
        if not vector or not isinstance(vector, list):
            return False
        if not all(isinstance(val, (int, float)) for val in vector):
            return False
        if len(vector) == 0:
            return False
        return True

    @handle_exceptions
    @log_execution_time
    def batch_upsert_with_retry(self, vectors: List[VectorRecord], max_retries: int = 3) -> Dict[str, Any]:
        """
        Batch upsert with retry mechanism
        """
        for attempt in range(max_retries):
            try:
                result = self.batch_upsert(vectors)
                return result
            except Exception as e:
                logger.warning(f"Batch upsert attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:  # Last attempt
                    raise e
                import time
                time.sleep(2 ** attempt)  # Exponential backoff

        return {"inserted_count": 0, "updated_count": 0, "failed_count": len(vectors)}

    @handle_exceptions
    @log_execution_time
    def batch_upsert(self, vectors: List[VectorRecord]) -> Dict[str, Any]:
        """
        Batch upsert vector records with metadata
        """
        if not vectors:
            logger.warning("No vectors provided for batch upsert")
            return {"inserted_count": 0, "updated_count": 0, "failed_count": 0}

        # Prepare points for Qdrant
        points = []
        for vector_record in vectors:
            point = models.PointStruct(
                id=str(uuid4()),  # Generate unique ID
                vector=vector_record.vector,
                payload=vector_record.payload
            )
            points.append(point)

        # Ensure the collection exists
        self._ensure_collection_exists()

        # Upsert the points to Qdrant
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully batch upserted {len(points)} vectors")
            return {
                "inserted_count": len(points),
                "updated_count": 0,
                "failed_count": 0
            }

        except Exception as e:
            logger.error(f"Error batch upserting vectors: {str(e)}")
            raise CustomException(f"Batch upsert failed: {str(e)}", "BATCH_UPSERT_ERROR")

    def validate_connection(self) -> bool:
        """
        Validate connection to Qdrant
        """
        try:
            # Try to get collection info as a simple connectivity test
            self.client.get_collection(self.collection_name)
            return True
        except:
            try:
                # If collection doesn't exist, try to list collections
                self.client.get_collections()
                return True
            except:
                return False

    @handle_exceptions
    @log_execution_time
    def get_collection_size(self) -> int:
        """
        Get the number of points in the collection
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            logger.error(f"Error getting collection size: {str(e)}")
            raise

    @handle_exceptions
    @log_execution_time
    def get_random_chunks(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Get a random sample of chunks from the collection
        """
        try:
            # Get collection info to know the total number of points
            collection_info = self.client.get_collection(self.collection_name)
            total_points = collection_info.points_count

            if total_points == 0:
                return []

            # Limit count to the total number of points
            count = min(count, total_points)

            # Get random point IDs
            import random
            random_ids = random.sample(range(total_points), count) if total_points > count else list(range(total_points))

            # Actually, Qdrant doesn't have a random sampling method, so we'll just get the first few points
            # For true random sampling, we'd need to implement a different approach
            results = self.client.scroll(
                collection_name=self.collection_name,
                limit=count
            )

            formatted_results = []
            for point in results[0]:  # results[0] contains the points, results[1] contains next_page_offset
                payload = point.payload or {}
                metadata = {}

                # Extract metadata fields that were prefixed with "meta_"
                for key, value in payload.items():
                    if key.startswith("meta_"):
                        metadata[key[5:]] = value  # Remove "meta_" prefix
                    elif key in ["content", "source_url", "chunk_index", "created_at"]:
                        continue  # Skip these as they're handled separately
                    else:
                        metadata[key] = value

                formatted_results.append({
                    "id": point.id,
                    "content": payload.get("content", ""),
                    "source_url": payload.get("source_url", ""),
                    "chunk_index": payload.get("chunk_index", 0),
                    "created_at": payload.get("created_at", ""),
                    "metadata": metadata
                })

            return formatted_results

        except Exception as e:
            logger.error(f"Error getting random chunks: {str(e)}")
            raise