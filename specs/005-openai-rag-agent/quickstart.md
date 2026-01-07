# Quickstart: OpenAI Agent with RAG Capabilities

## Overview
This guide explains how to use the OpenAI Agent with RAG capabilities that answers questions about book content using vector database retrieval.

## Prerequisites
- Python 3.11+
- Access to OpenAI API with valid API key
- Access to Qdrant collection with book content embeddings
- Properly configured `.env` file with API keys:
  - `OPENAI_API_KEY` for OpenAI access
  - `QDRANT_URL` for Qdrant access
  - `QDRANT_API_KEY` for Qdrant access
  - `QDRANT_COLLECTION_NAME` for the collection name

## Setup
1. Ensure your environment is properly configured:
   ```bash
   # Make sure you have the required environment variables in .env:
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=book_content_chunks
   ```

2. Install required dependencies:
   ```bash
   pip install openai qdrant-client python-dotenv
   ```

## Running the Agent
To start the interactive chat loop:

```bash
python agent.py
```

This will:
- Initialize the BookRetriever to connect to Qdrant
- Initialize the BookAgent with OpenAI integration
- Start an interactive chat loop for testing

## Using the Interactive Chat
Once running, you can ask questions about the book content:

```
Welcome to the Book Content Agent!
Ask me anything about the book content, or type 'quit' to exit.

You: What is ROS2?
Agent: ROS2 (Robot Operating System 2) is a flexible framework for writing robot applications...
Source: https://physical-ai-humanoid-robotics-book-kohl.vercel.app/docs/module1/chapter-1-ros2-core/

You: How does it differ from ROS1?
Agent: ROS2 differs from ROS1 in several key ways including improved security, better real-time support, and a more robust communication system...
Source: https://physical-ai-humanoid-robotics-book-kohl.vercel.app/docs/module1/chapter-1-ros2-core/

You: quit
Goodbye!
```

## Expected Behavior
### Successful Response
- Agent provides an answer based on book content
- Response includes relevant source citations
- Citations link to the specific pages where information was found

### When Information is Not Found
- Agent clearly states that the information is not in the book
- Agent may suggest related topics that are available
- Example: "I couldn't find information about X in the book. However, I can tell you about Y which is covered in chapter Z."

## Troubleshooting
- If you get API errors, verify your OpenAI and Qdrant API keys are correct
- If queries return no results, verify the Qdrant collection is properly populated
- If responses seem irrelevant, the retrieval might need tuning of the top-k parameter
- For timeout errors, check your network connection to external services