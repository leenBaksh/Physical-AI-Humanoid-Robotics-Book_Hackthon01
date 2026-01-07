# Data Model: Pipeline Validation & Query Testing

## Entity: ContentChunk
**Description**: Represents a chunk of content that has been processed and stored in the vector database

### Fields
- `id` (str): Unique identifier for the chunk
- `content` (str): The actual text content of the chunk
- `source_url` (str): URL of the original source page
- `chunk_index` (int): Index position of the chunk in the original document
- `metadata` (Dict[str, Any]): Additional metadata about the content
- `embedding` (Optional[List[float]]): Vector embedding of the content
- `created_at` (datetime): Timestamp when the chunk was created

### Relationships
- Belongs to a Qdrant collection
- Part of a larger document from which it was extracted

### Validation Rules
- Content must not be empty
- Source URL must be valid
- Chunk index must be non-negative

## Entity: QdrantPoint
**Description**: Represents a point in the Qdrant vector database

### Fields
- `id` (str): Unique identifier for the point
- `vector` (List[float]): The embedding vector
- `payload` (Dict[str, Any]): Metadata and content associated with the vector

### Payload Structure
- `content` (str): The text content
- `source_url` (str): Original source URL
- `chunk_index` (int): Position in original document
- `created_at` (str): Creation timestamp in ISO format
- `meta_*` (Any): Flattened metadata fields with "meta_" prefix

### Relationships
- Part of a Qdrant collection
- Contains one ContentChunk's embedding

## Entity: ValidationResult
**Description**: Represents the result of a validation operation

### Fields
- `total_chunks` (int): Total number of chunks in the collection
- `expected_chunks` (int): Expected number of chunks (if known)
- `validation_passed` (bool): Whether validation passed
- `sample_checks` (List[Dict[str, Any]]): Sample validation checks
- `errors` (List[str]): Any errors found during validation

## Entity: QueryResult
**Description**: Represents the result of a similarity query

### Fields
- `id` (str): ID of the matched chunk
- `content` (str): Content snippet of the matched chunk
- `source_url` (str): Source URL of the matched chunk
- `chunk_index` (int): Index position of the chunk
- `score` (float): Similarity score (0.0-1.0)
- `metadata` (Dict[str, Any]): Additional metadata
- `created_at` (str): When the chunk was created

### Relationships
- Associated with a query string
- Part of a ranked list of results

## Entity: QueryResponse
**Description**: Represents a complete response to a query with multiple results

### Fields
- `query` (str): The original query string
- `results` (List[QueryResult]): Ranked list of matching results
- `total_results` (int): Total number of results returned
- `execution_time` (float): Time taken to execute the query in seconds