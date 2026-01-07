# RAG Embeddings Pipeline

This project implements a content ingestion pipeline that fetches book content from website URLs, generates vector embeddings using Cohere models, and stores them in Qdrant vector database for RAG chatbot integration.

## Architecture

The pipeline follows a sequential flow:
1. **Fetch**: Retrieve content from specified URLs
2. **Chunk**: Parse and chunk text content with appropriate size limits
3. **Embed**: Generate vector embeddings using Cohere API
4. **Store**: Store embeddings in Qdrant vector database with metadata

## Project Structure

```
backend/
├── main.py              # Main pipeline orchestration script
├── api.py               # FastAPI endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── config/
│   └── settings.py      # Configuration management
├── src/
│   ├── fetcher/
│   │   ├── __init__.py
│   │   └── url_fetcher.py      # URL fetching and content extraction
│   ├── chunker/
│   │   ├── __init__.py
│   │   └── content_chunker.py  # Content parsing and chunking
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedding_generator.py  # Cohere embedding generation
│   ├── storage/
│   │   ├── __init__.py
│   │   └── qdrant_storage.py   # Qdrant vector storage
│   ├── validation.py           # Content validation
│   └── error_handler.py        # Error handling utilities
└── tests/
    ├── test_integration.py
    └── ...
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content_chunks
CHUNK_SIZE=512
OVERLAP_SIZE=50
```

## Usage

### Command Line Interface

Run the pipeline with specific URLs:

```bash
python main.py https://example.com/page1 https://example.com/page2
```

With verbose logging:
```bash
python main.py --verbose https://example.com/page1
```

To include subpages from sitemap and crawling:
```bash
python main.py --include-subpages https://example.com/
```

### API Usage

Start the API server:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API provides the following endpoints:

#### Content Ingestion
- `GET /api/v1/health` - Health check
- `POST /api/v1/content/ingest` - Ingest content from URLs (with optional `include_subpages` parameter)
- `GET /api/v1/content/ingest/{job_id}` - Get ingestion job status

#### URL Discovery
- `POST /api/v1/content/discover-urls` - Discover URLs from a website using sitemap and crawling

#### Vector Operations
- `POST /api/v1/vectors/batch-upsert` - Batch upsert vectors
- `POST /api/v1/search` - Search for similar content using semantic search

### URL Discovery Endpoint

The new `/api/v1/content/discover-urls` endpoint allows you to discover all URLs from a website:

```json
{
  "url": "https://example.com/",
  "use_sitemap": true,
  "use_crawling": true
}
```

Response includes:
- `base_url`: The base URL provided
- `discovered_urls`: List of all discovered URLs
- `sitemap_urls_count`: Number of URLs found via sitemap
- `crawled_urls_count`: Number of URLs found via crawling
- `total_urls`: Total unique URLs discovered

### Ingestion with Subpages

When using the ingestion endpoint, you can now include subpages by setting `include_subpages` to `true`:

```json
{
  "urls": ["https://example.com/"],
  "include_subpages": true,
  "content_types": ["html", "pdf"]
}
```

This will automatically discover and process all subpages from the provided URLs using both sitemap parsing and web crawling.

## Configuration

The system is configured through environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL of your Qdrant cluster
- `QDRANT_API_KEY`: API key for Qdrant access
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings (default: book_content_chunks)
- `CHUNK_SIZE`: Size of text chunks for embedding (default: 512)
- `OVERLAP_SIZE`: Overlap between chunks (default: 50)
- `LOG_LEVEL`: Logging level (default: INFO)

## Dependencies

- Python 3.11+
- FastAPI
- Cohere
- Qdrant Client
- BeautifulSoup4
- Requests
- Pydantic
- Python-dotenv
- PDFPlumber

## Testing

Run the tests:
```bash
pytest tests/
```