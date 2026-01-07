import logging
from typing import List, Dict, Any
from .models import ContentChunk
from .utils import handle_exceptions, log_execution_time, CustomException

logger = logging.getLogger(__name__)

class PipelineValidator:
    """
    Class to validate the content pipeline for integrity and correctness
    """

    def __init__(self):
        pass

    @handle_exceptions
    @log_execution_time
    def validate_content_integrity(self, original_content: str, processed_chunks: List[ContentChunk]) -> Dict[str, Any]:
        """
        Validate that content integrity is maintained during processing
        """
        validation_result = {
            "status": "valid",
            "errors": [],
            "warnings": [],
            "original_length": len(original_content),
            "reconstructed_length": 0
        }

        # Reconstruct content from chunks
        reconstructed_content = ""
        for chunk in processed_chunks:
            reconstructed_content += chunk.content + " "

        validation_result["reconstructed_length"] = len(reconstructed_content.strip())

        # Check if original content is substantially preserved
        if len(original_content) > 0:
            preservation_ratio = len(reconstructed_content.strip()) / len(original_content)
            if preservation_ratio < 0.8:  # Less than 80% preserved
                validation_result["status"] = "invalid"
                validation_result["errors"].append(
                    f"Content preservation ratio too low: {preservation_ratio:.2%}"
                )
            elif preservation_ratio > 1.2:  # More than 120% (possible duplication)
                validation_result["warnings"].append(
                    f"Content expansion ratio high: {preservation_ratio:.2%}"
                )

        return validation_result

    @handle_exceptions
    @log_execution_time
    def validate_embeddings_quality(self, chunks: List[ContentChunk]) -> Dict[str, Any]:
        """
        Validate embeddings quality and correctness
        """
        validation_result = {
            "status": "valid",
            "errors": [],
            "valid_embeddings_count": 0,
            "invalid_embeddings_count": 0
        }

        for i, chunk in enumerate(chunks):
            if chunk.embedding is None:
                validation_result["invalid_embeddings_count"] += 1
                validation_result["errors"].append(f"Chunk {i} has no embedding")
                continue

            # Validate embedding structure
            if not isinstance(chunk.embedding, list) or len(chunk.embedding) == 0:
                validation_result["invalid_embeddings_count"] += 1
                validation_result["errors"].append(f"Chunk {i} has invalid embedding structure")
                continue

            # Validate that all values are numbers
            if not all(isinstance(val, (int, float)) for val in chunk.embedding):
                validation_result["invalid_embeddings_count"] += 1
                validation_result["errors"].append(f"Chunk {i} has non-numeric embedding values")
                continue

            validation_result["valid_embeddings_count"] += 1

        if validation_result["invalid_embeddings_count"] > 0:
            validation_result["status"] = "invalid"

        return validation_result

    @handle_exceptions
    @log_execution_time
    def validate_stored_embeddings(self, original_chunks: List[ContentChunk], stored_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that stored embeddings match original content
        """
        validation_result = {
            "status": "valid",
            "errors": [],
            "stored_count": stored_result.get("inserted_count", 0),
            "expected_count": len([c for c in original_chunks if c.embedding is not None])
        }

        if validation_result["stored_count"] != validation_result["expected_count"]:
            validation_result["status"] = "invalid"
            validation_result["errors"].append(
                f"Mismatch between expected ({validation_result['expected_count']}) "
                f"and stored ({validation_result['stored_count']}) embeddings"
            )

        return validation_result

    @handle_exceptions
    @log_execution_time
    def validate_metadata_integrity(self, chunks: List[ContentChunk]) -> Dict[str, Any]:
        """
        Validate metadata integrity for stored content
        """
        validation_result = {
            "status": "valid",
            "errors": [],
            "valid_metadata_count": 0,
            "invalid_metadata_count": 0
        }

        for i, chunk in enumerate(chunks):
            # Check required metadata fields
            if not chunk.source_url:
                validation_result["invalid_metadata_count"] += 1
                validation_result["errors"].append(f"Chunk {i} missing source_url")
                continue

            if chunk.chunk_index is None:
                validation_result["invalid_metadata_count"] += 1
                validation_result["errors"].append(f"Chunk {i} missing chunk_index")
                continue

            validation_result["valid_metadata_count"] += 1

        if validation_result["invalid_metadata_count"] > 0:
            validation_result["status"] = "invalid"

        return validation_result

    @handle_exceptions
    @log_execution_time
    def validate_pipeline_health(self, pipeline_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate overall pipeline health and performance
        """
        validation_result = {
            "status": "healthy",
            "errors": [],
            "step_results": []
        }

        for step in pipeline_steps:
            step_result = {
                "step_name": step.get("name", "unknown"),
                "status": step.get("status", "unknown"),
                "duration": step.get("duration", 0),
                "items_processed": step.get("items_processed", 0)
            }

            if step_result["status"] == "failed":
                validation_result["status"] = "unhealthy"
                validation_result["errors"].append(f"Step {step_result['step_name']} failed")

            validation_result["step_results"].append(step_result)

        return validation_result