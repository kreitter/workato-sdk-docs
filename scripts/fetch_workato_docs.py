#!/usr/bin/env python3
"""
Workato SDK documentation fetcher with HTML to Markdown conversion.
Adapted from claude-code-docs for Workato Connector SDK documentation.
"""

import requests
import time
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
import logging
from datetime import datetime
import sys
import json
import hashlib
import os
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import html2text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Base URL for Workato documentation
BASE_URL = "https://docs.workato.com"
SDK_BASE_PATH = "/en/developing-connectors/sdk"

# Comprehensive list of SDK documentation URLs
# Last updated: 2025-08-14 from Workato documentation sitemap
SDK_URLS = [
    "https://docs.workato.com/en/developing-connectors/sdk/cli.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/download-streaming-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/methods.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/multistep-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/pick_lists.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/test.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/triggers.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/upload-streaming-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/getting-started.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/connector_spec.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/enable-ci-cd-on-github.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/file_streaming.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/vcr.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/writing_tests.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/security-guidelines.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/guides/troubleshooting.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/reference/cli-commands.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/reference/cli-project-directory-reference.html",
    "https://docs.workato.com/en/developing-connectors/sdk/cli/reference/rspec-commands.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-building-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-building-triggers.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-code-patterns.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-defining-schema.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-planning.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/introduction.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/api-key.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/aws_auth.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/basic-authentication.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/header-auth.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/jwt.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/multi_auth.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/oauth/auth-code-pkce.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/oauth/auth-code.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/oauth/client-credentials.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/oauth/ropc.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/on-prem.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/best-practices.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/create-objects.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/custom-action.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/get-objects.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/multi-threaded-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/multistep-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming/download-stream.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-chunk-id.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-content-range.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/update-objects.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/dynamic-webhook.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/hybrid-triggers.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/poll.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/securing-webhooks.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/static-webhook.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/config_fields.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/form-url-encoded.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/json-format.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/request_format_multipart_form.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/xml-format.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/debugging.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/error-handling.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/examples.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/trigger-limit.html",
    "https://docs.workato.com/en/developing-connectors/sdk/guides/walkthrough.html",
    "https://docs.workato.com/en/developing-connectors/sdk/limits.html",
    "https://docs.workato.com/en/developing-connectors/sdk/quickstart.html",
    "https://docs.workato.com/en/developing-connectors/sdk/quickstart/FAQ.html",
    "https://docs.workato.com/en/developing-connectors/sdk/quickstart/debugging.html",
    "https://docs.workato.com/en/developing-connectors/sdk/quickstart/sharing.html",
    "https://docs.workato.com/en/developing-connectors/sdk/quickstart/version-control.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/actions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/connection.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/connection/authorization.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/custom-action.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/http.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/methods.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/object_definitions.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/picklists.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/ruby_methods.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/schema.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/streams.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/test.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/triggers.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/whitelist-removal.html",
]

# Fallback entry points for crawling (if needed)
SDK_ENTRY_POINTS = [
    "https://docs.workato.com/en/developing-connectors/sdk.html",
    "https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html",
    "https://docs.workato.com/en/developing-connectors/sdk/platform-quickstart.html",
]

# Headers to identify the script
HEADERS = {
    'User-Agent': 'Workato-SDK-Docs-Fetcher/1.0',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # initial delay in seconds
MAX_RETRY_DELAY = 30  # maximum delay in seconds
RATE_LIMIT_DELAY = 1.0  # seconds between requests

# Manifest file
MANIFEST_FILE = "docs_manifest.json"


class WorkatoDocsConverter:
    """Converts Workato HTML documentation to Markdown."""
    
    def __init__(self):
        # Configure html2text
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0  # No line wrapping
        self.h2t.protect_links = True
        self.h2t.wrap_links = False
        self.h2t.skip_internal_links = False
        self.h2t.inline_links = True
        self.h2t.ignore_images = False
        self.h2t.images_to_alt = False
        self.h2t.mark_code = True
        
    def extract_main_content(self, html: str) -> str:
        """Extract the main content area from Workato documentation HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to find the main content area (adjust selectors based on actual structure)
        main_content = None
        
        # Common content selectors for documentation sites
        selectors = [
            'main.content',
            'div.content',
            'article.doc-content',
            'div.doc-body',
            'div#main-content',
            'div.markdown-body',
            'div.documentation-content',
            'section.content',
        ]
        
        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no specific content area found, try to extract body minus navigation
        if not main_content:
            # Remove navigation elements
            for nav in soup.find_all(['nav', 'header', 'footer']):
                nav.decompose()
            
            # Remove script and style tags
            for element in soup.find_all(['script', 'style', 'noscript']):
                element.decompose()
            
            # Remove sidebars
            for sidebar in soup.find_all(class_=re.compile(r'sidebar|side-nav|toc')):
                sidebar.decompose()
            
            # Try to find any remaining content
            main_content = soup.find('body') or soup
        
        return str(main_content)
    
    def html_to_markdown(self, html: str, url: str) -> str:
        """Convert HTML content to Markdown format."""
        # Extract main content
        main_html = self.extract_main_content(html)
        
        # Convert to markdown
        markdown = self.h2t.handle(main_html)
        
        # Post-process markdown
        markdown = self.post_process_markdown(markdown, url)
        
        return markdown
    
    def post_process_markdown(self, markdown: str, source_url: str) -> str:
        """Clean up and enhance the converted markdown."""
        lines = markdown.split('\n')
        processed_lines = []
        
        # Add header with source URL
        processed_lines.append(f"# Workato SDK Documentation")
        processed_lines.append(f"")
        processed_lines.append(f"> **Source**: {source_url}")
        processed_lines.append(f"> **Fetched**: {datetime.now().isoformat()}")
        processed_lines.append(f"")
        processed_lines.append("---")
        processed_lines.append("")
        
        # Process the content
        in_code_block = False
        for line in lines:
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            
            # Skip empty lines at the beginning
            if not processed_lines and not line.strip():
                continue
            
            # Clean up excessive whitespace (but preserve in code blocks)
            if not in_code_block:
                # Remove multiple consecutive empty lines
                if line.strip() == '' and processed_lines and processed_lines[-1] == '':
                    continue
            
            processed_lines.append(line)
        
        # Join and clean up
        markdown = '\n'.join(processed_lines)
        
        # Fix common conversion issues
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)  # Max 2 consecutive newlines
        markdown = re.sub(r'^\s+$', '', markdown, flags=re.MULTILINE)  # Clean empty lines with spaces
        
        # Replace [code] markers with proper markdown code blocks
        markdown = re.sub(r'\[code\]\s*\n', '```ruby\n', markdown)
        markdown = re.sub(r'\n\s*\[/code\]', '\n```', markdown)
        # Handle inline code (if any)
        markdown = re.sub(r'\[code\]([^\n]+?)\[/code\]', r'`\1`', markdown)
        
        return markdown


class WorkatoSDKCrawler:
    """Crawls Workato SDK documentation pages."""
    
    def __init__(self, session: requests.Session, converter: WorkatoDocsConverter):
        self.session = session
        self.converter = converter
        self.visited_urls = set()
        self.sdk_pages = []
        
    def is_sdk_url(self, url: str) -> bool:
        """Check if a URL is part of the SDK documentation."""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Check if it's an SDK-related page
        sdk_patterns = [
            '/developing-connectors/sdk',
            '/sdk-reference',
            '/connector-sdk',
        ]
        
        return any(pattern in path for pattern in sdk_patterns)
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from an HTML page."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)
            
            # Only include Workato docs URLs
            if absolute_url.startswith(BASE_URL) and self.is_sdk_url(absolute_url):
                # Normalize URL (remove fragments and query params for now)
                parsed = urlparse(absolute_url)
                normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                links.append(normalized)
        
        return list(set(links))  # Remove duplicates
    
    def crawl_page(self, url: str) -> Optional[Dict]:
        """Crawl a single page and extract its content and links."""
        if url in self.visited_urls:
            return None
        
        self.visited_urls.add(url)
        logger.info(f"Crawling: {url}")
        
        try:
            response = self.session.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            # Extract links for further crawling
            links = self.extract_links(response.text, url)
            
            # Convert to markdown
            markdown_content = self.converter.html_to_markdown(response.text, url)
            
            return {
                'url': url,
                'content': markdown_content,
                'links': links,
                'content_hash': hashlib.sha256(markdown_content.encode()).hexdigest()
            }
            
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")
            return None
    
    def crawl_sdk_docs(self, max_depth: int = 3) -> List[Dict]:
        """Crawl SDK documentation starting from entry points."""
        pages_to_crawl = SDK_ENTRY_POINTS.copy()
        crawled_pages = []
        depth = 0
        
        while pages_to_crawl and depth < max_depth:
            next_batch = []
            
            for url in pages_to_crawl:
                if url not in self.visited_urls:
                    # Rate limiting
                    time.sleep(RATE_LIMIT_DELAY)
                    
                    page_data = self.crawl_page(url)
                    if page_data:
                        crawled_pages.append(page_data)
                        # Add discovered links to next batch
                        next_batch.extend(page_data['links'])
            
            # Move to next depth level
            pages_to_crawl = list(set(next_batch) - self.visited_urls)
            depth += 1
            
            logger.info(f"Completed depth {depth}, found {len(pages_to_crawl)} new pages to crawl")
        
        return crawled_pages


def load_manifest(docs_dir: Path) -> dict:
    """Load the manifest of previously fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            if "files" not in manifest:
                manifest["files"] = {}
            return manifest
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
    return {"files": {}, "last_updated": None}


def save_manifest(docs_dir: Path, manifest: dict) -> None:
    """Save the manifest of fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    manifest["last_updated"] = datetime.now().isoformat()
    
    # Get GitHub repository from environment or use default
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'kreitter/workato-sdk-docs')
    github_ref = os.environ.get('GITHUB_REF_NAME', 'main')
    
    manifest["base_url"] = f"https://raw.githubusercontent.com/{github_repo}/{github_ref}/docs/"
    manifest["github_repository"] = github_repo
    manifest["github_ref"] = github_ref
    manifest["description"] = "Workato SDK documentation manifest"
    manifest["source"] = "https://docs.workato.com"
    
    manifest_path.write_text(json.dumps(manifest, indent=2))


def url_to_filename(url: str) -> str:
    """Convert a URL to a safe filename."""
    parsed = urlparse(url)
    path = parsed.path
    
    # Remove leading/trailing slashes and .html extension
    path = path.strip('/')
    if path.endswith('.html'):
        path = path[:-5]
    
    # Replace path separators with double underscores
    filename = path.replace('/', '__')
    
    # Remove common prefixes to keep filenames shorter
    prefixes_to_remove = [
        'en__developing-connectors__sdk__',
        'en__developing-connectors__'
    ]
    for prefix in prefixes_to_remove:
        if filename.startswith(prefix):
            filename = filename[len(prefix):]
            break
    
    # Handle special case where we might end up with just 'sdk'
    if filename == 'sdk':
        filename = 'sdk-overview'
    
    # Ensure .md extension
    if not filename.endswith('.md'):
        filename += '.md'
    
    return filename


def save_markdown_file(docs_dir: Path, filename: str, content: str) -> str:
    """Save markdown content and return its hash."""
    file_path = docs_dir / filename
    
    try:
        file_path.write_text(content, encoding='utf-8')
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        logger.info(f"Saved: {filename}")
        return content_hash
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise


def fetch_page_content(session: requests.Session, converter: WorkatoDocsConverter, url: str) -> Optional[Dict]:
    """Fetch and convert a single page."""
    try:
        logger.info(f"Fetching: {url}")
        response = session.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # Convert to markdown
        markdown_content = converter.html_to_markdown(response.text, url)
        
        return {
            'url': url,
            'content': markdown_content,
            'content_hash': hashlib.sha256(markdown_content.encode()).hexdigest()
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


def main():
    """Main function to fetch Workato SDK documentation."""
    start_time = datetime.now()
    logger.info("Starting Workato SDK documentation fetch")
    
    # Create docs directory
    docs_dir = Path(__file__).parent.parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {docs_dir}")
    
    # Load existing manifest
    manifest = load_manifest(docs_dir)
    
    # Statistics
    successful = 0
    failed = 0
    new_files = 0
    updated_files = 0
    unchanged_files = 0
    new_manifest = {"files": {}}
    
    # Create session and tools
    with requests.Session() as session:
        converter = WorkatoDocsConverter()
        
        # Use the hardcoded list of SDK URLs
        sdk_urls = SDK_URLS.copy()
        
        # Optional: Fallback to crawling if needed (unlikely)
        if not sdk_urls:
            logger.warning("No SDK URLs defined, falling back to crawling approach")
            crawler = WorkatoSDKCrawler(session, converter)
            crawled_pages = crawler.crawl_sdk_docs(max_depth=3)
            sdk_urls = [page['url'] for page in crawled_pages]
        
        logger.info(f"Processing {len(sdk_urls)} SDK documentation pages")
        
        # Process each URL
        for i, url in enumerate(sdk_urls, 1):
            # Rate limiting
            if i > 1:
                time.sleep(RATE_LIMIT_DELAY)
            
            # Progress indicator
            if i % 10 == 0 or i == len(sdk_urls):
                logger.info(f"Progress: {i}/{len(sdk_urls)} pages ({i*100//len(sdk_urls)}%)")
            
            try:
                page_data = fetch_page_content(session, converter, url)
                
                if page_data:
                    filename = url_to_filename(url)
                    
                    # Check if content has changed
                    old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
                    
                    if old_hash == "":
                        # New file
                        content_hash = save_markdown_file(docs_dir, filename, page_data['content'])
                        logger.info(f"NEW: {filename}")
                        last_updated = datetime.now().isoformat()
                        new_files += 1
                    elif page_data['content_hash'] != old_hash:
                        # Updated file
                        content_hash = save_markdown_file(docs_dir, filename, page_data['content'])
                        logger.info(f"UPDATED: {filename}")
                        last_updated = datetime.now().isoformat()
                        updated_files += 1
                    else:
                        # Unchanged file
                        content_hash = old_hash
                        logger.debug(f"Unchanged: {filename}")
                        last_updated = manifest.get("files", {}).get(filename, {}).get("last_updated", datetime.now().isoformat())
                        unchanged_files += 1
                    
                    new_manifest["files"][filename] = {
                        "original_url": url,
                        "hash": content_hash,
                        "last_updated": last_updated
                    }
                    
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                logger.error(f"Failed to process {url}: {e}")
                failed += 1
    
    # Add metadata to manifest
    new_manifest["fetch_metadata"] = {
        "last_fetch_completed": datetime.now().isoformat(),
        "fetch_duration_seconds": (datetime.now() - start_time).total_seconds(),
        "pages_processed": len(sdk_urls),
        "pages_saved_successfully": successful,
        "pages_failed": failed,
        "new_files": new_files,
        "updated_files": updated_files,
        "unchanged_files": unchanged_files,
        "total_files": len(new_manifest["files"]),
        "fetch_tool_version": "3.0",
        "fetch_method": "hardcoded_urls"
    }
    
    # Save manifest
    save_manifest(docs_dir, new_manifest)
    
    # Summary
    duration = datetime.now() - start_time
    logger.info("\n" + "="*50)
    logger.info(f"Fetch completed in {duration}")
    logger.info(f"Total pages processed: {len(sdk_urls)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"New files: {new_files}")
    logger.info(f"Updated files: {updated_files}")
    logger.info(f"Unchanged files: {unchanged_files}")
    
    if failed > 0 and successful == 0:
        logger.error("No pages were fetched successfully!")
        sys.exit(1)
    else:
        logger.info(f"\nWorkato SDK documentation fetch complete! Total files: {len(new_manifest['files'])}")


if __name__ == "__main__":
    main()