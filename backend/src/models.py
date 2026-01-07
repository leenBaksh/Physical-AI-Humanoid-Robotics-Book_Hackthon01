from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4

class ContentChunk(BaseModel):
    """
    Represents a chunk of content extracted from a URL
    """
    id: str
    content: str
    source_url: str
    chunk_index: int
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None
    created_at: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True

class VectorRecord(BaseModel):
    """
    Represents a vector record for storage in Qdrant
    """
    id: str
    vector: List[float]
    payload: Dict[str, Any] = {}

class URLFetchRequest(BaseModel):
    """
    Request model for URL fetching
    """
    urls: List[str]
    include_subpages: bool = False
    content_types: List[str] = ["html", "pdf"]

class ProcessingResult(BaseModel):
    """
    Result model for processing operations
    """
    status: str  # "success", "partial", "failed"
    processed_count: int
    failed_count: int
    errors: List[Dict[str, Any]] = []
    start_time: datetime
    end_time: datetime
    duration: float  # in seconds