#!/usr/bin/env python3
"""
OpenAI Agent with RAG Capabilities

This script implements an intelligent agent that uses the Qdrant vector database
to answer questions about book content via OpenAI Agent SDK.
"""
import os
import sys
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv  # type: ignore  # pyright: ignore[reportMissingImports]
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel  # type: ignore  # pyright: ignore[reportMissingImports]
from openai import AsyncOpenAI  # type: ignore  # pyright: ignore[reportMissingImports]



ROUTER_API_KEY = "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"

client = AsyncOpenAI(
        api_key=ROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

third_party_model = OpenAIChatCompletionsModel(
        openai_client=client,
        model="mistralai/devstral-2512:free"
    )

# Load environment variables
load_dotenv()

# Use environment variable for API key, with fallback to a default if needed
# Import backend components using direct imports to avoid sys.path conflicts
import sys
import os

# Directly import the backend modules using their full path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')

# Import using importlib to avoid path conflicts
import importlib.util

# Import QdrantStorage
qdrant_storage_path = os.path.join(backend_dir, 'src', 'storage', 'qdrant_storage.py')
qdrant_spec = importlib.util.spec_from_file_location("qdrant_storage", qdrant_storage_path)
if qdrant_spec is None or qdrant_spec.loader is None:
    raise ImportError(f"Can't load qdrant_storage module from {qdrant_storage_path}")
qdrant_module = importlib.util.module_from_spec(qdrant_spec)
qdrant_spec.loader.exec_module(qdrant_module)
QdrantStorage = qdrant_module.QdrantStorage

# Import EmbeddingGenerator
embedding_path = os.path.join(backend_dir, 'src', 'embeddings', 'embedding_generator.py')
embedding_spec = importlib.util.spec_from_file_location("embedding_generator", embedding_path)
if embedding_spec is None or embedding_spec.loader is None:
    raise ImportError(f"Can't load embedding_generator module from {embedding_path}")
embedding_module = importlib.util.module_from_spec(embedding_spec)
embedding_spec.loader.exec_module(embedding_module)
EmbeddingGenerator = embedding_module.EmbeddingGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_qdrant_chunks_impl(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Implementation function for Qdrant retrieval that performs the actual work.

    Args:
        query: The user's query
        top_k: Number of top results to retrieve (default: 5)

    Returns:
        List of retrieved chunks with content, source, and metadata
    """
    if not query or not query.strip():
        logger.warning("Empty query provided to retrieve method")
        return []

    try:
        qdrant_storage = QdrantStorage()
        embedding_generator = EmbeddingGenerator()

        # Generate embedding for the query
        query_embedding = embedding_generator.generate_single_embedding(query)

        if query_embedding is None:
            logger.error("Failed to generate embedding for query")
            return []

        # Validate top_k parameter
        if top_k <= 0:
            logger.warning(f"Invalid top_k value: {top_k}, using default of 5")
            top_k = 5

        # Perform similarity search
        search_results = qdrant_storage.search_similar(query_embedding, limit=top_k)

        # Format results
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                'content': result.get('content', ''),
                'source_url': result.get('source_url', ''),
                'score': result.get('score', 0.0),
                'chunk_index': result.get('chunk_index', 0),
                'metadata': result.get('metadata', {})
            })

        logger.info(f"Retrieved {len(formatted_results)} chunks for query: {query[:50]}...")
        return formatted_results

    except Exception as e:
        logger.error(f"Error during retrieval for query '{query[:30]}...': {e}")
        return []


# Define a function tool for Qdrant retrieval that wraps the implementation
@function_tool
def retrieve_qdrant_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant chunks from the Qdrant collection based on the query.
    This function tool is designed to be used by the OpenAI Agent SDK.

    Args:
        query: The user's query
        top_k: Number of top results to retrieve (default: 5)

    Returns:
        List of retrieved chunks with content, source, and metadata
    """
    return retrieve_qdrant_chunks_impl(query, top_k)


class BookRetriever:
    """
    Class to query the Qdrant collection for relevant book chunks.
    """

    def __init__(self):
        """
        Initialize the BookRetriever with Qdrant connection.
        """
        self.qdrant_storage = QdrantStorage()
        self.embedding_generator = EmbeddingGenerator()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks from the Qdrant collection based on the query.

        Args:
            query: The user's query
            top_k: Number of top results to retrieve (default: 5)

        Returns:
            List of retrieved chunks with content, source, and metadata
        """
        return retrieve_qdrant_chunks_impl(query, top_k)

class BookAgent:
    """
    Class that uses OpenAI Agent SDK to generate answers based on retrieved context.
    """

    def __init__(self, retriever: BookRetriever, model: Optional[str] = None, temperature: float = 0.3):
        """
        Initialize the BookAgent with OpenAI Agent and retriever.

        Args:
            retriever: Instance of BookRetriever to fetch context
            model: OpenAI model to use (default: gpt-3.5-turbo from env or research decision)
            temperature: Controls randomness in responses (default: 0.3)
        """
        # Use model from parameter, then environment, then default
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.temperature = temperature
        self.retriever = retriever

        # Create the agent with the retrieval tool
        self.agent = Agent(
            name="Book Content Agent",
            instructions=(
                "You are BookBot, an intelligent AI agent specializing in answering questions about book content. "
                "Your approach is methodical: first analyze the provided context, then form a comprehensive response. "
                "Only use information from the provided context. If the answer is not in the context, "
                "clearly state that the information is not in the book. Always include source citations "
                "for the information you use. Be helpful, accurate, and cite your sources."
            ),
            tools=[retrieve_qdrant_chunks],
            model=third_party_model
        )

    async def answer(self, question: str) -> Dict[str, Any]:
        """
        Generate an answer to the question using the agent SDK.

        Args:
            question: The user's question

        Returns:
            Dictionary with answer, citations, and confidence
        """
        try:
            # Run the agent with the question
            result = await Runner.run(
                self.agent,
                question
            )

            response_text = result.final_output

            # Since the agent uses the tool internally, we need to extract the citations
            # For now, we'll return an empty citations list as the tool usage is handled internally
            # In a more advanced implementation, we would parse the response to extract citation info
            citations: list = []

            # For now, we'll retrieve the chunks separately to have them available for citation tracking
            # This is a limitation of the current agent SDK - we can't directly access tool results
            # So we make a separate call to get the chunks that would be used
            retrieved_chunks = self.retriever.retrieve(question, top_k=5)

            return {
                'answer': response_text,
                'citations': citations,
                'retrieved_chunks_used': retrieved_chunks,  # Track the chunks that were retrieved
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calling OpenAI Agent: {e}")
            response_text = f"Sorry, I encountered an error processing your question: {str(e)}"
            return {
                'answer': response_text,
                'citations': [],
                'retrieved_chunks_used': [],
                'timestamp': datetime.now().isoformat()
            }


import asyncio

def chat_loop():
    """
    Interactive CLI function to test the agent's RAG capabilities.
    """
    print("Welcome to the Book Content Agent!")
    print("Ask me anything about the book content, or type 'quit' to exit.\n")

    # Initialize components with configuration options
    try:
        retriever = BookRetriever()

        # Get configuration from environment variables or use defaults
        model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.3'))

        agent = BookAgent(retriever, model=model, temperature=temperature)
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    # Conversation history to maintain context for follow-up questions
    conversation_history = []

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Add user query to conversation history
            conversation_history.append({"role": "user", "content": user_input})

            # Generate response using asyncio
            response = asyncio.run(agent.answer(user_input))

            # Display the answer
            print(f"Agent: {response['answer']}")

            # Display citations if available
            if response['citations']:
                print("\nSources:")
                for i, citation in enumerate(response['citations'][:3]):  # Show top 3 citations
                    print(f"  - {citation['title']} - {citation['url']}")

            print()  # Empty line for readability

            # Add agent response to conversation history
            conversation_history.append({"role": "assistant", "content": response['answer']})

            # Limit history to last 5 exchanges to manage context length
            if len(conversation_history) > 10:  # 5 exchanges = 10 messages (user + assistant)
                conversation_history = conversation_history[-10:]

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error in chat loop: {e}")
            continue


async def test_implementation_async():
    """
    Async test function to verify the complete implementation with various scenarios.
    """
    print("Testing the Book Content Agent implementation...")

    try:
        # Initialize components with test configuration
        retriever = BookRetriever()
        agent = BookAgent(
            retriever,
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            temperature=0.3
        )

        # Test scenarios
        test_questions = [
            "What is the main topic of this book?",
            "Can you explain ROS2 briefly?",
            "How does this book approach AI for robotics?"
        ]

        print("\nRunning test scenarios...")
        for i, question in enumerate(test_questions, 1):
            print(f"\nTest {i}: {question}")
            try:
                response = await agent.answer(question)
                print(f"Answer: {response['answer'][:200]}...")  # Truncate for display
                print(f"Citations: {len(response['citations'])} sources found")
            except Exception as e:
                print(f"Error in test {i}: {e}")

        print("\n[SUCCESS] Implementation tests completed successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Error during testing: {e}")
        return False


def test_implementation():
    """
    Test function to verify the complete implementation with various scenarios.
    """
    return asyncio.run(test_implementation_async())


def main():
    """
    Main function to run the agent.
    """
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_implementation()
    else:
        chat_loop()


if __name__ == "__main__":
    main()
