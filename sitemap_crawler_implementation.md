# Sitemap Crawler and Recursive Web Crawler Implementation

## Overview

The system now includes enhanced data ingestion capabilities that can automatically discover and process content from entire websites, not just individual pages. This addresses the issue where only landing pages were being ingested instead of all documentation pages.

## Key Features

### 1. Sitemap.xml Parsing
- Automatically discovers and parses `sitemap.xml` files from websites
- Handles sitemap indexes that reference multiple sitemap files
- Supports compressed sitemap files (gzip)

### 2. Recursive Web Crawling
- Discovers additional URLs by crawling website pages
- Respects max depth settings to prevent infinite crawling
- Filters out non-content URLs (images, PDFs, admin pages, etc.)

### 3. Combined Approach
- Uses both sitemap parsing and crawling to maximize coverage
- Eliminates duplicates between sitemap and crawled URLs
- Tracks source of each discovered URL

## Implementation Details

### Files Added/Modified

1. `backend/src/fetcher/sitemap_crawler.py` - New module implementing sitemap parsing and crawling
2. `backend/src/fetcher/url_fetcher.py` - Updated to use sitemap crawler when `include_subpages=True`
3. `backend/api.py` - Added new `/api/v1/content/discover-urls` endpoint
4. `backend/main.py` - Added `--include-subpages` CLI option
5. `backend/README.md` - Updated documentation

### New API Endpoint

`POST /api/v1/content/discover-urls`

Request:
```json
{
  "url": "https://example.com/",
  "use_sitemap": true,
  "use_crawling": true
}
```

Response:
```json
{
  "base_url": "https://example.com/",
  "discovered_urls": ["https://example.com/page1", "https://example.com/page2", ...],
  "sitemap_urls_count": 50,
  "crawled_urls_count": 25,
  "total_urls": 70
}
```

### Enhanced Ingestion Endpoint

The existing `POST /api/v1/content/ingest` endpoint now supports an `include_subpages` parameter:

```json
{
  "urls": ["https://example.com/"],
  "include_subpages": true,
  "content_types": ["html", "pdf"]
}
```

When `include_subpages` is `true`, the system will:
1. Discover all URLs from the provided base URL using sitemap and crawling
2. Fetch content from all discovered URLs
3. Process the content through the normal pipeline (chunk, embed, store)

## Usage Examples

### Command Line
```bash
# Process only the specified URLs (original behavior)
python main.py https://example.com/

# Process all discovered subpages as well
python main.py --include-subpages https://example.com/
```

### API Usage
```bash
# Discover URLs from a website
curl -X POST http://localhost:8000/api/v1/content/discover-urls \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://physical-ai-humanoid-robotics-book-kohl.vercel.app/",
    "use_sitemap": true,
    "use_crawling": true
  }'

# Ingest with subpages
curl -X POST http://localhost:8000/api/v1/content/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://physical-ai-humanoid-robotics-book-kohl.vercel.app/"],
    "include_subpages": true
  }'
```

## Configuration Options

The `SitemapCrawler` class accepts the following configuration:

- `max_depth`: Maximum depth to crawl (default: 2)
- `max_urls`: Maximum number of URLs to discover (default: 1000)

## URL Filtering

The crawler automatically excludes:

- Non-content file types (images, PDFs, executables, etc.)
- Administrative URLs (wp-admin, admin, login, etc.)
- URLs from different domains
- URLs with invalid formats

## Testing

The implementation was tested with the target website `https://physical-ai-humanoid-robotics-book-kohl.vercel.app/` and successfully discovered 70+ URLs from the sitemap and processed content from all documentation pages.