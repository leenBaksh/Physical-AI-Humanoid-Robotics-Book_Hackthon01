"""
Sitemap and web crawler functionality to discover and extract URLs from websites
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Set, Optional
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse, urlunparse
import logging
import re
from ..utils import handle_exceptions, validate_url

logger = logging.getLogger(__name__)

class SitemapCrawler:
    """
    Class to handle sitemap parsing and recursive web crawling
    """

    def __init__(self, max_depth: int = 2, max_urls: int = 1000):
        self.max_depth = max_depth
        self.max_urls = max_urls
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    @handle_exceptions
    def get_sitemap_urls(self, base_url: str) -> List[str]:
        """
        Extract URLs from sitemap.xml and any referenced sitemap index files
        """
        parsed_base = urlparse(base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

        sitemap_url = f"{base_domain}/sitemap.xml"
        urls = set()

        try:
            # Try to fetch the main sitemap
            response = self.session.get(sitemap_url, timeout=30)
            if response.status_code == 200:
                urls.update(self._parse_sitemap_content(response.text, base_domain))
            else:
                logger.info(f"No sitemap.xml found at {sitemap_url}")
        except requests.RequestException as e:
            logger.warning(f"Could not fetch sitemap from {sitemap_url}: {e}")

        # Also try common sitemap locations
        common_sitemap_paths = [
            f"{base_domain}/sitemap_index.xml",
            f"{base_domain}/sitemap_index.xml.gz",
            f"{base_domain}/wp-sitemap.xml",  # WordPress sitemap
        ]

        for sitemap_path in common_sitemap_paths:
            try:
                response = self.session.get(sitemap_path, timeout=30)
                if response.status_code == 200:
                    urls.update(self._parse_sitemap_content(response.text, base_domain))
            except requests.RequestException:
                continue

        return list(urls)

    def _parse_sitemap_content(self, content: str, base_domain: str) -> Set[str]:
        """
        Parse sitemap content and extract URLs
        """
        urls = set()

        try:
            # Handle gzipped sitemap content if needed
            if content.startswith(b'\x1f\x8b'.decode('latin1')):
                import gzip
                content = gzip.decompress(content).decode('utf-8')
        except:
            pass  # If not gzipped, continue with original content

        try:
            root = ET.fromstring(content)

            # Check if this is a sitemap index (contains other sitemaps)
            if root.tag.endswith('sitemapindex'):
                for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                    loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc is not None:
                        sitemap_url = loc.text.strip()
                        try:
                            response = self.session.get(sitemap_url, timeout=30)
                            if response.status_code == 200:
                                urls.update(self._parse_sitemap_content(response.text, base_domain))
                        except requests.RequestException:
                            logger.warning(f"Could not fetch nested sitemap: {sitemap_url}")
            else:
                # This is a regular sitemap with URLs
                for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                    loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc is not None:
                        url = loc.text.strip()
                        if self._is_valid_url_for_crawling(url, base_domain):
                            urls.add(url)
        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap XML: {e}")

        return urls

    @handle_exceptions
    def crawl_website(self, base_url: str, max_depth: Optional[int] = None) -> List[str]:
        """
        Recursively crawl a website to discover URLs
        """
        if max_depth is None:
            max_depth = self.max_depth

        parsed_base = urlparse(base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

        visited_urls = set()
        urls_to_visit = [(base_url, 0)]  # (url, depth)
        discovered_urls = set()

        while urls_to_visit and len(visited_urls) < self.max_urls:
            current_url, depth = urls_to_visit.pop(0)

            if current_url in visited_urls or depth > max_depth:
                continue

            visited_urls.add(current_url)

            try:
                response = self.session.get(current_url, timeout=30)
                if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Add current URL to discovered URLs if it's valid
                    if self._is_valid_url_for_crawling(current_url, base_domain):
                        discovered_urls.add(current_url)

                    # Find all links on the page
                    if depth < max_depth:  # Only crawl deeper if we haven't reached max depth
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            absolute_url = urljoin(current_url, href)

                            if (absolute_url not in visited_urls and
                                absolute_url not in [url for url, _ in urls_to_visit] and
                                self._is_valid_url_for_crawling(absolute_url, base_domain)):
                                urls_to_visit.append((absolute_url, depth + 1))

            except requests.RequestException as e:
                logger.warning(f"Error crawling {current_url}: {e}")
                continue

        return list(discovered_urls)

    def _is_valid_url_for_crawling(self, url: str, base_domain: str) -> bool:
        """
        Check if a URL is valid for crawling (same domain, not an excluded type)
        """
        if not validate_url(url):
            return False

        parsed = urlparse(url)
        if not parsed.netloc:
            return False

        # Check if URL is on the same domain
        if not parsed.netloc.endswith(urlparse(base_domain).netloc):
            return False

        # Exclude certain file types that aren't content pages
        excluded_extensions = {
            '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
            '.css', '.js', '.zip', '.exe', '.dmg', '.mp4', '.mp3', '.avi'
        }

        path = parsed.path.lower()
        if any(path.endswith(ext) for ext in excluded_extensions):
            return False

        # Exclude common non-content paths
        excluded_paths = {
            '/wp-admin', '/wp-includes', '/wp-content/plugins',
            '/admin', '/login', '/logout', '/register', '/signup',
            '/cart', '/checkout', '/account'
        }

        if any(path.startswith(ex_path) for ex_path in excluded_paths):
            return False

        return True

    @handle_exceptions
    def get_all_urls(self, base_url: str, use_sitemap: bool = True, use_crawling: bool = True) -> List[str]:
        """
        Get all URLs from a website using both sitemap and crawling if available
        """
        all_urls = set()
        sitemap_urls = []
        crawled_urls = []

        if use_sitemap:
            logger.info(f"Fetching URLs from sitemap for {base_url}")
            sitemap_urls = self.get_sitemap_urls(base_url)
            all_urls.update(sitemap_urls)
            logger.info(f"Found {len(sitemap_urls)} URLs from sitemap")

        if use_crawling:
            logger.info(f"Crawling website for additional URLs: {base_url}")
            crawled_urls = self.crawl_website(base_url)
            all_urls.update(crawled_urls)
            logger.info(f"Found {len(crawled_urls)} URLs from crawling")

        # Remove any URLs that were only discovered during crawling but are also in sitemap
        # to avoid duplicates
        return list(all_urls)

    @handle_exceptions
    def get_all_urls_with_source(self, base_url: str, use_sitemap: bool = True, use_crawling: bool = True) -> tuple[List[str], int, int]:
        """
        Get all URLs from a website using both sitemap and crawling, with source counts
        Returns: (all_urls, sitemap_count, crawled_count)
        """
        all_urls = set()
        sitemap_urls = []
        crawled_urls = []

        if use_sitemap:
            logger.info(f"Fetching URLs from sitemap for {base_url}")
            sitemap_urls = self.get_sitemap_urls(base_url)
            all_urls.update(sitemap_urls)
            logger.info(f"Found {len(sitemap_urls)} URLs from sitemap")

        if use_crawling:
            logger.info(f"Crawling website for additional URLs: {base_url}")
            crawled_urls = self.crawl_website(base_url)
            all_urls.update(crawled_urls)
            logger.info(f"Found {len(crawled_urls)} URLs from crawling")

        # Calculate unique counts
        # URLs that are only in sitemap (not in crawled)
        unique_sitemap_urls = set(sitemap_urls) - set(crawled_urls)
        # URLs that are only in crawled (not in sitemap)
        unique_crawled_urls = set(crawled_urls) - set(sitemap_urls)
        # URLs in both (would be counted once in total)
        common_urls = set(sitemap_urls) & set(crawled_urls)

        sitemap_count = len(unique_sitemap_urls) + len(common_urls)
        crawled_count = len(unique_crawled_urls) + len(common_urls)

        return list(all_urls), sitemap_count, crawled_count