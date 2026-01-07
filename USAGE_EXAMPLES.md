# Usage Examples: OpenAI Agent with RAG Capabilities

## Overview

This document provides usage examples for the Book Content Agent that answers questions about book content using vector database retrieval.

## Prerequisites

- Python 3.11+
- Access to OpenAI API with valid API key
- Access to Qdrant collection with book content embeddings
- Properly configured `.env` file with API keys:
  - `OPENAI_API_KEY` for OpenAI access
  - `QDRANT_URL` for Qdrant access
  - `QDRANT_API_KEY` for Qdrant access
  - `QDRANT_COLLECTION_NAME` for the collection name

## Configuration Options

The agent supports several configuration options via environment variables:

```bash
# OpenAI Configuration
OPENAI_MODEL=gpt-3.5-turbo          # Model to use (default: gpt-3.5-turbo)
OPENAI_TEMPERATURE=0.3              # Response randomness (default: 0.3)
OPENAI_MAX_TOKENS=1000              # Max tokens in response (default: 1000)

# Retrieval Configuration
RETRIEVAL_TOP_K=5                   # Number of chunks to retrieve (default: 5)
```

## Running the Agent

### Interactive Mode

To start the interactive chat loop:

```bash
python agent.py
```

This will:
- Initialize the BookRetriever to connect to Qdrant
- Initialize the BookAgent with OpenAI integration
- Start an interactive chat loop for testing

### Test Mode

To run the built-in tests:

```bash
python agent.py --test
```

This runs various test scenarios to verify the implementation.

## Example Usage

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

## Programmatic Usage

You can also use the agent programmatically:

```python
from agent import BookRetriever, BookAgent

# Initialize components
retriever = BookRetriever()
agent = BookAgent(
    retriever,
    model="gpt-3.5-turbo",      # Optional: specify model
    temperature=0.3,            # Optional: control randomness
    max_tokens=1000             # Optional: max response length
)

# Ask a question
response = agent.answer("What is the main topic of this book?")
print(response['answer'])
print("Citations:", response['citations'])
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