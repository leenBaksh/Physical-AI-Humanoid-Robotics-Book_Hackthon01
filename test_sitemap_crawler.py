#!/usr/bin/env python3
"""
Test script to verify sitemap crawler functionality
"""
import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from src.fetcher.sitemap_crawler import SitemapCrawler

def test_sitemap_crawling():
    """
    Test the sitemap crawler with the provided URLs
    """
    print("Testing sitemap crawler...")

    # Test with the URL from the issue
    test_url = "https://physical-ai-humanoid-robotics-book-kohl.vercel.app/"
    crawler = SitemapCrawler(max_depth=2, max_urls=100)

    print(f"Discovering URLs for: {test_url}")

    # Test sitemap discovery
    sitemap_urls = crawler.get_sitemap_urls(test_url)
    print(f"Found {len(sitemap_urls)} URLs from sitemap:")
    for url in sitemap_urls[:10]:  # Show first 10
        print(f"  - {url}")
    if len(sitemap_urls) > 10:
        print(f"  ... and {len(sitemap_urls) - 10} more")

    # Test crawling (this might take a while)
    print(f"\nCrawling website: {test_url}")
    crawled_urls = crawler.crawl_website(test_url, max_depth=1)  # Limit depth for testing
    print(f"Found {len(crawled_urls)} URLs from crawling:")
    for url in crawled_urls[:10]:  # Show first 10
        print(f"  - {url}")
    if len(crawled_urls) > 10:
        print(f"  ... and {len(crawled_urls) - 10} more")

    # Test combined approach
    print(f"\nGetting all URLs using both methods:")
    all_urls, sitemap_count, crawled_count = crawler.get_all_urls_with_source(test_url)
    print(f"Total URLs found: {len(all_urls)}")
    print(f"From sitemap: {sitemap_count}")
    print(f"From crawling: {crawled_count}")

    # Show some sample URLs
    print("\nSample URLs discovered:")
    for url in all_urls[:15]:  # Show first 15
        print(f"  - {url}")
    if len(all_urls) > 15:
        print(f"  ... and {len(all_urls) - 15} more")

def test_url_fetcher_with_subpages():
    """
    Test the URL fetcher with include_subpages enabled
    """
    print("\n" + "="*60)
    print("Testing URL fetcher with subpages...")

    from src.fetcher.url_fetcher import URLFetcher

    # Test with a simple URL
    test_urls = ["https://physical-ai-humanoid-robotics-book-kohl.vercel.app/"]
    fetcher = URLFetcher()

    print("Fetching with include_subpages=False (original behavior):")
    original_results = fetcher.fetch_urls(test_urls, include_subpages=False)
    print(f"Retrieved content from {len(original_results)} URLs")

    print("\nFetching with include_subpages=True (new behavior):")
    extended_results = fetcher.fetch_urls(test_urls, include_subpages=True)
    print(f"Retrieved content from {len(extended_results)} URLs")

    print("\nURLs fetched with subpages enabled:")
    for result in extended_results:
        print(f"  - {result['url']} (status: {result['status_code']})")


if __name__ == "__main__":
    print("Running sitemap crawler tests...\n")

    try:
        test_sitemap_crawling()
        test_url_fetcher_with_subpages()

        print("\n" + "="*60)
        print("All tests completed successfully!")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()