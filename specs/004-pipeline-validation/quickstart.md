# Quickstart: Pipeline Validation & Query Testing

## Overview
This guide explains how to use the validation and query testing tools for the RAG embeddings pipeline.

## Prerequisites
- Python 3.11+
- Access to Qdrant collection with populated embeddings
- Properly configured `.env` file with Qdrant and Cohere API keys
- Completed pipeline execution that populated the collection

## Setup
1. Ensure your environment is properly configured:
   ```bash
   # Make sure you have the required environment variables in .env:
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

## Running Validation
To run the validation script:

```bash
python retrieve.py --validate
```

This will:
- Count chunks in the Qdrant collection
- Compare with expected counts
- Spot-check sample content matches
- Display validation results

## Using Interactive Query Mode
To start the interactive query loop:

```bash
python retrieve.py
```

This will:
- Run validation first
- Enter interactive mode where you can enter queries
- Display results with scores and metadata
- Type 'quit' or 'exit' to exit

## Using Command-Line Queries
To run a single query from the command line:

```bash
python retrieve.py --query "your query here" --limit 5
```

## Expected Output
### Validation Output
```
=== Collection Validation ===
Total chunks in collection: 150
Expected chunks: 150
Validation: PASSED

Sample spot-checks:
✓ Content match for chunk from: https://example.com/page1
✓ Content match for chunk from: https://example.com/page2
```

### Query Output
```
Query: "What is ROS2?"

Top 3 results:
1. Score: 0.85
   Source: https://example.com/ros2-intro
   Content: "ROS2 is a flexible framework for writing robot applications..."

2. Score: 0.78
   Source: https://example.com/ros2-core-concepts
   Content: "The core concepts of ROS2 include nodes, topics, services..."
```

## Troubleshooting
- If validation fails, check that your Qdrant collection is properly populated
- If queries return no results, verify that embeddings were generated correctly
- If API rate limits are hit, consider adding delays between requests
- Ensure your Cohere API key has sufficient quota for embedding generation