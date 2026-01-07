#!/usr/bin/env python3
"""
Test script to verify the new API endpoint for URL discovery
"""
import requests
import json

def test_api_discovery():
    """
    Test the new API endpoint for discovering URLs
    """
    # Assuming the API is running on localhost:8000
    api_url = "http://localhost:8000"

    # Test URL discovery endpoint
    discovery_endpoint = f"{api_url}/api/v1/content/discover-urls"

    # Test payload
    payload = {
        "url": "https://physical-ai-humanoid-robotics-book-kohl.vercel.app/",
        "use_sitemap": True,
        "use_crawling": True
    }

    try:
        print("Testing URL discovery API endpoint...")
        response = requests.post(discovery_endpoint, json=payload)

        if response.status_code == 200:
            result = response.json()
            print(f"Success! Found {result['total_urls']} URLs")
            print(f"From sitemap: {result['sitemap_urls_count']}")
            print(f"From crawling: {result['crawled_urls_count']}")

            print("\nFirst 10 URLs discovered:")
            for url in result['discovered_urls'][:10]:
                print(f"  - {url}")

            if len(result['discovered_urls']) > 10:
                print(f"  ... and {len(result['discovered_urls']) - 10} more")

        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the server is running on http://localhost:8000")
        print("To start the API server, run: uvicorn api:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"Error testing API: {e}")

def test_ingestion_with_subpages():
    """
    Test the ingestion API with include_subpages enabled
    """
    api_url = "http://localhost:8000"
    ingestion_endpoint = f"{api_url}/api/v1/content/ingest"

    # Test payload with include_subpages enabled
    payload = {
        "urls": ["https://physical-ai-humanoid-robotics-book-kohl.vercel.app/"],
        "include_subpages": True,
        "content_types": ["html", "pdf"]
    }

    try:
        print("\nTesting ingestion API with include_subpages=True...")
        response = requests.post(ingestion_endpoint, json=payload)

        if response.status_code == 200:
            result = response.json()
            print(f"Ingestion job started: {result['job_id']}")
            print(f"Status: {result['status']}")
            print(f"Total URLs to process: {result['total_urls']}")

            # Check job status
            status_endpoint = f"{api_url}/api/v1/content/ingest/{result['job_id']}"
            status_response = requests.get(status_endpoint)

            if status_response.status_code == 200:
                status_result = status_response.json()
                print(f"Job status: {status_result['status']}")
                print(f"Processed: {status_result['processed_count']}")
                print(f"Failed: {status_result['failed_count']}")
                print(f"Total chunks: {status_result['total_chunks']}")
        else:
            print(f"Ingestion API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error testing ingestion API: {e}")

if __name__ == "__main__":
    print("Testing API endpoints for sitemap and subpage functionality...\n")

    test_api_discovery()
    test_ingestion_with_subpages()

    print("\nAPI tests completed!")