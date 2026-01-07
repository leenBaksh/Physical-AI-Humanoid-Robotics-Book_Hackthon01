import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import urljoin, urlparse
import pdfplumber  # For PDF handling
from io import BytesIO
import re
from ..utils import handle_exceptions, log_execution_time, CustomException, validate_url
from ..models import ContentChunk, URLFetchRequest
from .sitemap_crawler import SitemapCrawler

logger = logging.getLogger(__name__)

class URLFetcher:
    """
    Class to fetch content from URLs and extract text content
    """

    def __init__(self):
        self.session = requests.Session()
        # Set a user agent to avoid being blocked by some websites
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    @handle_exceptions
    @log_execution_time
    def fetch_urls(self, urls: List[str], include_subpages: bool = False) -> List[Dict[str, Any]]:
        """
        Fetch content from a list of URLs
        """
        # If include_subpages is True, expand the URLs using sitemap crawling
        if include_subpages:
            all_urls = set()
            crawler = SitemapCrawler()

            for url in urls:
                logger.info(f"Discovering additional URLs for {url}...")
                discovered_urls, sitemap_count, crawled_count = crawler.get_all_urls_with_source(url, use_sitemap=True, use_crawling=True)
                all_urls.update(discovered_urls)
                logger.info(f"Discovered {len(discovered_urls)} total URLs for {url} (from sitemap: {sitemap_count}, crawled: {crawled_count})")

            # Combine original URLs with discovered ones
            all_urls = list(set(urls) | all_urls)
        else:
            all_urls = urls

        results = []
        for url in all_urls:
            try:
                if not validate_url(url):
                    logger.warning(f"Invalid URL format: {url}")
                    continue

                response = self.session.get(url, timeout=30)
                response.raise_for_status()  # Raises an HTTPError for bad responses

                content_type = response.headers.get('content-type', '').lower()
                metadata = {}

                if 'application/pdf' in content_type:
                    content = self._extract_pdf_content(response.content)
                    content_type = 'pdf'
                elif 'text/html' in content_type or 'application/xhtml+xml' in content_type:
                    content = self._extract_html_content(response.text)
                    metadata = self._extract_html_metadata(response.text)
                    content_type = 'html'
                else:
                    # For other content types, treat as plain text
                    content = response.text
                    content_type = 'text'

                results.append({
                    'url': url,
                    'content': content,
                    'content_type': content_type,
                    'status_code': response.status_code,
                    'metadata': metadata
                })

                logger.info(f"Successfully fetched content from {url}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {url}: {str(e)}")
                results.append({
                    'url': url,
                    'content': '',
                    'content_type': 'unknown',
                    'status_code': getattr(e.response, 'status_code', 0) if hasattr(e, 'response') else 0,
                    'error': str(e),
                    'metadata': {}
                })

        return results

    def _extract_html_content(self, html_content: str) -> str:
        """
        Extract text content from HTML while preserving semantic structure
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script, style, nav, and footer elements that don't contain main content
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Try to find main content containers first
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article', re.I)) or soup

        # Get text content
        text = main_content.get_text(separator=' ')

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def _extract_html_metadata(self, html_content: str) -> Dict[str, Any]:
        """
        Extract metadata from HTML such as title, author, etc.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        metadata = {}

        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()

        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name.lower()] = content

        # Extract headings (h1-h6) as potential section titles
        headings = []
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append({
                'level': int(heading.name[1]),
                'text': heading.get_text().strip()
            })
        metadata['headings'] = headings

        return metadata

    def _extract_pdf_content(self, pdf_bytes: bytes) -> str:
        """
        Extract text content from PDF bytes
        """
        content = ""
        try:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        content += page_text + "\n"
        except Exception as e:
            logger.error(f"Error extracting PDF content: {str(e)}")
            raise CustomException(f"Failed to extract PDF content: {str(e)}", "PDF_EXTRACTION_ERROR")

        return content

    @handle_exceptions
    @log_execution_time
    def fetch_content_from_single_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from a single URL
        """
        if not validate_url(url):
            raise CustomException(f"Invalid URL format: {url}", "INVALID_URL")

        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '').lower()
        metadata = {}

        if 'application/pdf' in content_type:
            content = self._extract_pdf_content(response.content)
        elif 'text/html' in content_type or 'application/xhtml+xml' in content_type:
            content = self._extract_html_content(response.text)
            metadata = self._extract_html_metadata(response.text)
        else:
            content = response.text

        return {
            'url': url,
            'content': content,
            'content_type': content_type,
            'status_code': response.status_code,
            'metadata': metadata
        }