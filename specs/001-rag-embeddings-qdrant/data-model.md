# Data Model: RAG Embeddings and Qdrant Vector Database Integration

## ContentChunk
- **id**: string (UUID) - Unique identifier for the content chunk
- **content**: string - The actual text content of the chunk
- **source_url**: string - URL where the content originated
- **chunk_index**: integer - Position of this chunk in the original document
- **metadata**: object - Additional metadata about the content
- **embedding**: list[float] - Vector embedding of the content
- **created_at**: datetime - Timestamp when the chunk was created

## VectorRecord
- **id**: string (UUID) - Unique identifier for the vector record
- **vector**: list[float] - The embedding vector for similarity search
- **payload**: object - Metadata associated with the vector
  - **content**: string - Original text content
  - **source_url**: string - URL where the content originated
  - **chunk_index**: integer - Position of this chunk in the original document
  - **created_at**: datetime - Timestamp when the record was created

## URLFetchRequest
- **urls**: list[string] - List of URLs to fetch content from
- **include_subpages**: boolean - Whether to include subpages from the same domain
- **content_types**: list[string] - Allowed content types (e.g., "html", "pdf")

## ProcessingResult
- **status**: string - Processing status ("success", "partial", "failed")
- **processed_count**: integer - Number of URLs successfully processed
- **failed_count**: integer - Number of URLs that failed processing
- **errors**: list[object] - Details about any errors that occurred
- **start_time**: datetime - When processing started
- **end_time**: datetime - When processing ended
- **duration**: float - Duration of processing in seconds