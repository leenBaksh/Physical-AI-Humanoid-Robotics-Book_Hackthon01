from fastapi import FastAPI, BackgroundTasks, HTTPException  # type: ignore  # pyright: ignore[reportMissingImports]
from typing import Dict, Any, List
import uuid
import asyncio
from pydantic import BaseModel  # type: ignore  # pyright: ignore[reportMissingImports]
from datetime import datetime
from src.fetcher.url_fetcher import URLFetcher
from src.chunker.content_chunker import ContentChunker
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.storage.qdrant_storage import QdrantStorage
from src.models import URLFetchRequest, ProcessingResult
from src.fetcher.sitemap_crawler import SitemapCrawler
from src.validation import PipelineValidator
from src.error_handler import handle_pipeline_errors, setup_error_handlers

backend_app = FastAPI(title="RAG Embeddings API", version="1.0.0")

# Setup error handlers
setup_error_handlers(backend_app)

# In-memory job storage (in production, use a database)
jobs: Dict[str, Dict[str, Any]] = {}

class IngestionJob(BaseModel):
    job_id: str
    status: str
    total_urls: int
    processed_count: int = 0
    failed_count: int = 0
    start_time: datetime | None = None
    end_time: datetime | None = None
    estimated_completion: datetime | None = None

class IngestionResponse(BaseModel):
    job_id: str
    status: str
    total_urls: int
    estimated_completion: datetime

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    processed_count: int
    failed_count: int
    total_chunks: int
    start_time: datetime
    end_time: datetime
    duration_seconds: float

class BatchUpsertRequest(BaseModel):
    vectors: List[Dict[str, Any]]

class BatchUpsertResponse(BaseModel):
    inserted_count: int
    updated_count: int
    failed_count: int

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

class SearchResult(BaseModel):
    id: str
    content: str
    source_url: str
    chunk_index: int
    score: float
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_results: int

@backend_app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


class URLDiscoveryRequest(BaseModel):
    """Request model for URL discovery"""
    url: str
    use_sitemap: bool = True
    use_crawling: bool = True


class URLDiscoveryResponse(BaseModel):
    """Response model for URL discovery"""
    base_url: str
    discovered_urls: List[str]
    sitemap_urls_count: int = 0
    crawled_urls_count: int = 0
    total_urls: int


@backend_app.post("/api/v1/content/discover-urls", response_model=URLDiscoveryResponse)
async def discover_urls(request: URLDiscoveryRequest):
    """Discover URLs from a website using sitemap and crawling"""
    try:
        crawler = SitemapCrawler()

        # Get all URLs using both sitemap and crawling with source counts
        all_urls, sitemap_count, crawled_count = crawler.get_all_urls_with_source(
            request.url,
            use_sitemap=request.use_sitemap,
            use_crawling=request.use_crawling
        )

        response = URLDiscoveryResponse(
            base_url=request.url,
            discovered_urls=all_urls,
            sitemap_urls_count=sitemap_count,
            crawled_urls_count=crawled_count,
            total_urls=len(all_urls)
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL discovery failed: {str(e)}")

@backend_app.post("/api/v1/content/ingest", response_model=IngestionResponse)
async def ingest_content(request: URLFetchRequest, background_tasks: BackgroundTasks):
    """Ingest content from specified URLs and generate embeddings"""
    job_id = str(uuid.uuid4())

    job = IngestionJob(
        job_id=job_id,
        status="processing",
        total_urls=len(request.urls),
        start_time=datetime.now()
    )

    jobs[job_id] = job.dict()

    # Run the ingestion in the background
    background_tasks.add_task(process_ingestion_job, job_id, request)

    response = IngestionResponse(
        job_id=job_id,
        status="processing",
        total_urls=len(request.urls),
        estimated_completion=datetime.now()
    )

    return response

def process_ingestion_job(job_id: str, request: URLFetchRequest):
    """Process the ingestion job in the background"""
    job = jobs.get(job_id)
    if not job:
        return

    try:
        # Initialize components
        fetcher = URLFetcher()
        chunker = ContentChunker()
        embedder = EmbeddingGenerator()
        storage = QdrantStorage()

        # Update job status
        job["status"] = "processing"
        job["start_time"] = datetime.now()

        # 1. Fetch URLs
        fetched_content = fetcher.fetch_urls(request.urls, include_subpages=request.include_subpages)

        # Count successful and failed fetches
        successful_fetches = [item for item in fetched_content if item.get('content')]
        failed_fetches = [item for item in fetched_content if not item.get('content')]

        job["processed_count"] = len(successful_fetches)
        job["failed_count"] = len(failed_fetches)

        if successful_fetches:
            # 2. Chunk content
            all_chunks = []
            for item in successful_fetches:
                content = item.get('content', '')
                source_url = item.get('url', '')
                metadata = item.get('metadata', {})
                if content:
                    chunks = chunker.chunk_content(content, source_url, metadata)
                    all_chunks.extend(chunks)

            # 3. Generate embeddings
            chunks_with_embeddings = embedder.generate_embeddings(all_chunks)
            valid_chunks = [chunk for chunk in chunks_with_embeddings if chunk.embedding is not None]

            # 4. Store in Qdrant
            if valid_chunks:
                storage_result = storage.store_in_qdrant(valid_chunks)

        # Update job completion status
        job["status"] = "completed"
        job["end_time"] = datetime.now()
        job["total_chunks"] = len([c for c in all_chunks if c.embedding is not None])

    except Exception as e:
        job["status"] = "failed"
        job["end_time"] = datetime.now()
        job["error"] = str(e)

@backend_app.get("/api/v1/content/ingest/{job_id}", response_model=JobStatusResponse)
async def get_ingestion_status(job_id: str):
    """Get status of a content ingestion job"""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Calculate duration if job is completed
    duration_seconds = 0
    if job.get("end_time") and job.get("start_time"):
        end_time = datetime.fromisoformat(job["end_time"]) if isinstance(job["end_time"], str) else job["end_time"]
        start_time = datetime.fromisoformat(job["start_time"]) if isinstance(job["start_time"], str) else job["start_time"]
        duration_seconds = int((end_time - start_time).total_seconds())

    response = JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        processed_count=job["processed_count"],
        failed_count=job["failed_count"],
        total_chunks=job.get("total_chunks", 0),
        start_time=datetime.fromisoformat(job["start_time"]) if isinstance(job["start_time"], str) else job["start_time"],
        end_time=datetime.fromisoformat(job["end_time"]) if isinstance(job["end_time"], str) else job["end_time"],
        duration_seconds=duration_seconds
    )

    return response

@backend_app.post("/api/v1/vectors/batch-upsert", response_model=BatchUpsertResponse)
async def batch_upsert_vectors(request: BatchUpsertRequest):
    """Batch upsert vector embeddings with metadata"""
    try:
        storage = QdrantStorage()

        # Convert the request vectors to VectorRecord objects
        from src.models import VectorRecord
        vector_records = []

        for vec_data in request.vectors:
            vector_record = VectorRecord(
                id=vec_data.get("id", str(uuid.uuid4())),
                vector=vec_data["vector"],
                payload=vec_data.get("payload", {})
            )
            vector_records.append(vector_record)

        result = storage.batch_upsert(vector_records)

        response = BatchUpsertResponse(
            inserted_count=result["inserted_count"],
            updated_count=result["updated_count"],
            failed_count=result["failed_count"]
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch upsert failed: {str(e)}")

@backend_app.post("/api/v1/search", response_model=SearchResponse)
async def search_content(request: SearchRequest):
    """Search for similar content using semantic search"""
    try:
        # Initialize embedder and storage
        embedder = EmbeddingGenerator()
        storage = QdrantStorage()

        # Generate embedding for the search query
        query_embedding = embedder.generate_single_embedding(request.query)

        # Search for similar content in Qdrant
        search_results = storage.search_similar(query_embedding, limit=request.limit)

        # Convert results to the expected format
        formatted_results = []
        for result in search_results:
            formatted_result = SearchResult(
                id=result["id"],
                content=result["content"],
                source_url=result["source_url"],
                chunk_index=result["chunk_index"],
                score=result["score"],
                metadata=result.get("metadata", {})
            )
            formatted_results.append(formatted_result)

        response = SearchResponse(
            results=formatted_results,
            query=request.query,
            total_results=len(formatted_results)
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn  # type: ignore  # pyright: ignore[reportMissingImports]
    uvicorn.run(backend_app, host="0.0.0.0", port=8000)
