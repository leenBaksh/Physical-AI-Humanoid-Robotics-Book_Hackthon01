import logging
import sys
import os
from typing import List, Dict, Any

# Add the backend directory to Python path to resolve imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from src.models import ContentChunk
from src.utils import handle_exceptions, log_execution_time
from config.settings import settings

logger = logging.getLogger(__name__)

class ContentChunker:
    """
    Class to parse and chunk text content from URLs
    """

    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.overlap_size = settings.OVERLAP_SIZE

    @handle_exceptions
    @log_execution_time
    def chunk_content(self, content: str, source_url: str, metadata: Dict[str, Any] = None) -> List[ContentChunk]:
        """
        Parse and chunk text content with appropriate size limits
        """
        if not content:
            return []

        # Split content into sentences
        sentences = self._split_into_sentences(content)

        # Create chunks from sentences
        chunks = self._create_chunks_from_sentences(sentences, source_url, metadata)

        logger.info(f"Created {len(chunks)} chunks from content of {len(content)} characters")
        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences with improved regex pattern
        """
        import re
        # More sophisticated sentence splitting that preserves abbreviations and handles edge cases
        # This pattern looks for sentence endings (., !, ?) followed by whitespace and capital letter or end of string
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])\s+(?=\n)|(?<=[.!?])$', text)
        # Filter out empty strings and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def _split_by_headings(self, text: str) -> List[str]:
        """
        Split text by headings/sections when available
        """
        # This is a placeholder for more advanced section-based splitting
        # In a real implementation, this would use the metadata from the fetcher
        return [text]

    def _create_chunks_from_sentences(self, sentences: List[str], source_url: str, metadata: Dict[str, Any] = None) -> List[ContentChunk]:
        """
        Create content chunks from sentences respecting size limits
        """
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_index = 0

        # Prepare base metadata for all chunks
        base_metadata = {"source_type": "chunked_content", "original_sentence_count": len(current_chunk)}
        if metadata:
            base_metadata.update(metadata)

        for sentence in sentences:
            # Skip empty sentences
            if not sentence.strip():
                continue

            sentence_size = len(sentence)

            # If adding this sentence would exceed the chunk size
            if current_size + sentence_size > self.chunk_size and current_chunk:
                # Create a chunk with the current sentences
                chunk_text = ' '.join(current_chunk)
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    "source_type": "chunked_content",
                    "original_sentence_count": len(current_chunk),
                    "chunk_size": len(chunk_text),
                    "chunk_index": chunk_index
                })

                chunk = ContentChunk(
                    id=f"{source_url.replace('://', '_').replace('/', '_')}_{chunk_index}",
                    content=chunk_text,
                    source_url=source_url,
                    chunk_index=chunk_index,
                    metadata=chunk_metadata
                )
                chunks.append(chunk)

                # Handle overlap
                if self.overlap_size > 0:
                    # Add overlapping sentences from the end of the current chunk
                    overlap_sentences = self._get_overlap_sentences(current_chunk, self.overlap_size)
                    current_chunk = overlap_sentences + [sentence]
                    current_size = sum(len(s) for s in current_chunk)
                else:
                    # Start a new chunk with the current sentence
                    current_chunk = [sentence]
                    current_size = sentence_size

                chunk_index += 1
            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_size += sentence_size

        # Add the last chunk if it has content
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk_metadata = base_metadata.copy()
            chunk_metadata.update({
                "source_type": "chunked_content",
                "original_sentence_count": len(current_chunk),
                "chunk_size": len(chunk_text),
                "chunk_index": chunk_index
            })

            chunk = ContentChunk(
                id=f"{source_url.replace('://', '_').replace('/', '_')}_{chunk_index}",
                content=chunk_text,
                source_url=source_url,
                chunk_index=chunk_index,
                metadata=chunk_metadata
            )
            chunks.append(chunk)

        return chunks

    def handle_large_documents(self, content: str, source_url: str, metadata: Dict[str, Any] = None) -> List[ContentChunk]:
        """
        Handle large documents that might exceed embedding model limits
        """
        # If the content is very large, we might need to process it in larger segments first
        # For now, we'll use the existing chunking logic which should handle this
        return self.chunk_content(content, source_url, metadata)

    def _get_overlap_sentences(self, sentences: List[str], overlap_size: int) -> List[str]:
        """
        Get sentences from the end of the list that fit within overlap_size
        """
        if not sentences:
            return []

        overlap_sentences = []
        current_size = 0

        # Work backwards through sentences until we reach overlap_size
        for sentence in reversed(sentences):
            if current_size + len(sentence) <= overlap_size:
                overlap_sentences.insert(0, sentence)  # Insert at beginning to maintain order
                current_size += len(sentence)
            else:
                break

        return overlap_sentences

    @handle_exceptions
    @log_execution_time
    def chunk_multiple_contents(self, contents: List[Dict[str, Any]]) -> List[ContentChunk]:
        """
        Chunk multiple content items
        """
        all_chunks = []
        for item in contents:
            url = item.get('url', '')
            content = item.get('content', '')
            metadata = item.get('metadata', {})
            if content:
                chunks = self.chunk_content(content, url, metadata)
                all_chunks.extend(chunks)

        logger.info(f"Total of {len(all_chunks)} chunks created from {len(contents)} content items")
        return all_chunks