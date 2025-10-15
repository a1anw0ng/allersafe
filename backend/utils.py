#!/usr/bin/env python3
"""Shared utilities for allergen detection and alternative finding"""

def is_valid_source_url(url: str) -> bool:
    """Check if URL is a valid, direct source (not a redirect)

    Args:
        url: URL to validate

    Returns:
        True if URL is valid and direct, False otherwise
    """
    if not url or not url.startswith('http'):
        return False

    # Filter out grounding API redirects and other invalid URLs
    invalid_patterns = [
        'vertexaisearch.cloud.google.com',
        'grounding-api-redirect',
        'localhost',
        '127.0.0.1'
    ]

    for pattern in invalid_patterns:
        if pattern in url.lower():
            return False

    return True

def extract_grounding_sources(response):
    """Extract source citations from Vertex AI grounding metadata

    Only returns direct, working URLs (filters out redirect/grounding URLs)

    Args:
        response: LiteLLM response object

    Returns:
        List of dicts with 'title' and 'url' keys, or empty list if no sources
    """
    sources = []

    # Check if grounding metadata exists
    if not hasattr(response, 'vertex_ai_grounding_metadata'):
        return sources

    grounding_data = response.vertex_ai_grounding_metadata
    if not grounding_data or not isinstance(grounding_data, list):
        return sources

    # Extract unique sources from grounding chunks
    seen_urls = set()
    for metadata in grounding_data:
        if not isinstance(metadata, dict):
            continue

        chunks = metadata.get('groundingChunks', [])
        for chunk in chunks:
            if not isinstance(chunk, dict):
                continue

            web_info = chunk.get('web', {})
            url = web_info.get('uri', '')
            title = web_info.get('title', '')

            # Only add unique, valid URLs
            if url and url not in seen_urls and is_valid_source_url(url):
                seen_urls.add(url)
                sources.append({
                    'title': title or url,
                    'url': url
                })

    return sources

def clean_sources_list(sources: list, max_sources: int = 5) -> list:
    """Clean a list of sources by removing invalid URLs and limiting to max_sources

    Args:
        sources: List of source dicts with 'url' keys
        max_sources: Maximum number of sources to return (default: 5)

    Returns:
        Filtered list with only valid sources, limited to max_sources
    """
    if not sources:
        return []

    cleaned = []
    seen_urls = set()

    for source in sources:
        if not isinstance(source, dict):
            continue

        url = source.get('url', '')

        # Skip if invalid or duplicate
        if not is_valid_source_url(url) or url in seen_urls:
            continue

        seen_urls.add(url)
        cleaned.append(source)

        # Stop once we reach the maximum
        if len(cleaned) >= max_sources:
            break

    return cleaned
