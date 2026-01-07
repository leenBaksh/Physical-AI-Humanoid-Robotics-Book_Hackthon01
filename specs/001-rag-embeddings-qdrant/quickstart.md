# Quickstart: RAG Embeddings and Qdrant Vector Database Integration

## Prerequisites

- Python 3.11+
- pip package manager
- Cohere API key
- Qdrant Cloud account and API key
- Git

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create virtual environment and install dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content_chunks
```

### 4. Initialize Qdrant collection (if not exists)
```bash
# This can be done via Qdrant dashboard or API
```

## Usage

### Run the full pipeline
```bash
python main.py
```

### Run specific pipeline steps
```bash
# Just fetch URLs
python -m src.fetcher.url_fetcher --urls "https://example.com/page1" "https://example.com/page2"

# Just generate embeddings for pre-fetched content
python -m src.embeddings.embedding_generator

# Just store vectors in Qdrant
python -m src.storage.qdrant_storage
```

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL of your Qdrant cluster
- `QDRANT_API_KEY`: API key for Qdrant access
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings (default: book_content_chunks)
- `CHUNK_SIZE`: Size of text chunks for embedding (default: 512)
- `OVERLAP_SIZE`: Overlap between chunks (default: 50)

## Pipeline Functions

The main pipeline consists of these sequential functions:

1. `fetch_urls()` - Gets all book page URLs
2. `chunk_content()` - Parses and chunks text from URLs
3. `generate_embeddings()` - Creates vectors via Cohere
4. `store_in_qdrant()` - Batch upserts vectors with metadata
5. `main()` - Orchestrates the full pipeline flow

## Testing

Run the tests to verify functionality:
```bash
pytest tests/
```

## Development

### Adding new functionality
- Add new modules in the `src/` directory
- Follow the same pattern as existing modules
- Write corresponding tests in the `tests/` directory

### Configuration
- Modify settings in `config/settings.py`
- Add new configuration options as needed