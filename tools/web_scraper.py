#!/usr/bin/env python3
"""
Web scraper utility for Scenara project
Used for gathering meeting-related information and research
"""

import argparse
import asyncio
import aiohttp
import sys
from typing import List, Dict, Any
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

class WebScraper:
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.session = None
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Scenara Meeting Research Bot 1.0'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single URL and extract content
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with URL, title, content, and metadata
        """
        try:
            print(f"Scraping: {url}", file=sys.stderr)
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    return {
                        "url": url,
                        "status": response.status,
                        "error": f"HTTP {response.status}",
                        "content": "",
                        "title": "",
                        "word_count": 0
                    }
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract title
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else "No title"
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Extract main content
                content_selectors = [
                    'main', 'article', '.content', '.main-content', 
                    '.post-content', '.entry-content', '#content'
                ]
                
                content_element = None
                for selector in content_selectors:
                    content_element = soup.select_one(selector)
                    if content_element:
                        break
                
                if not content_element:
                    content_element = soup.find('body')
                
                # Extract text content
                if content_element:
                    content = content_element.get_text()
                else:
                    content = soup.get_text()
                
                # Clean up content
                content = re.sub(r'\s+', ' ', content).strip()
                
                # Extract metadata
                word_count = len(content.split())
                
                return {
                    "url": url,
                    "status": response.status,
                    "title": title,
                    "content": content,
                    "word_count": word_count,
                    "content_type": response.headers.get('content-type', ''),
                    "scraped_at": time.time()
                }
        
        except Exception as e:
            print(f"Error scraping {url}: {e}", file=sys.stderr)
            return {
                "url": url,
                "error": str(e),
                "content": "",
                "title": "",
                "word_count": 0
            }
    
    async def scrape_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape multiple URLs concurrently
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of scraping results
        """
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def scrape_with_semaphore(url):
            async with semaphore:
                return await self.scrape_url(url)
        
        tasks = [scrape_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "url": urls[i],
                    "error": str(result),
                    "content": "",
                    "title": "",
                    "word_count": 0
                })
            else:
                processed_results.append(result)
        
        return processed_results

def extract_meeting_insights(content: str) -> Dict[str, Any]:
    """
    Extract meeting-related insights from scraped content
    
    Args:
        content: Text content from scraped page
        
    Returns:
        Dictionary with extracted insights
    """
    insights = {
        "meeting_keywords": [],
        "business_context": [],
        "preparation_hints": [],
        "stakeholder_mentions": []
    }
    
    # Meeting-related keywords
    meeting_keywords = [
        'meeting', 'conference', 'summit', 'workshop', 'seminar',
        'presentation', 'discussion', 'negotiation', 'planning',
        'strategy', 'review', 'sync', 'standup', 'retrospective'
    ]
    
    content_lower = content.lower()
    for keyword in meeting_keywords:
        if keyword in content_lower:
            insights["meeting_keywords"].append(keyword)
    
    # Business context indicators
    business_terms = [
        'enterprise', 'corporate', 'business', 'commercial',
        'executive', 'management', 'leadership', 'stakeholder',
        'customer', 'client', 'vendor', 'partner'
    ]
    
    for term in business_terms:
        if term in content_lower:
            insights["business_context"].append(term)
    
    # Extract sentences with preparation-related content
    prep_indicators = ['prepare', 'preparation', 'agenda', 'objectives', 'goals']
    sentences = content.split('.')
    
    for sentence in sentences[:10]:  # Check first 10 sentences
        sentence_lower = sentence.lower()
        for indicator in prep_indicators:
            if indicator in sentence_lower:
                insights["preparation_hints"].append(sentence.strip())
                break
    
    return insights

async def main():
    parser = argparse.ArgumentParser(description="Web scraper for PromptCoT meeting research")
    parser.add_argument("urls", nargs="+", help="URLs to scrape")
    parser.add_argument("--max-concurrent", type=int, default=3, 
                       help="Maximum concurrent requests")
    parser.add_argument("--extract-insights", action="store_true",
                       help="Extract meeting-related insights")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format")
    
    args = parser.parse_args()
    
    async with WebScraper(max_concurrent=args.max_concurrent) as scraper:
        results = await scraper.scrape_urls(args.urls)
        
        for result in results:
            if args.format == "json":
                import json
                if args.extract_insights and result.get("content"):
                    result["insights"] = extract_meeting_insights(result["content"])
                print(json.dumps(result, indent=2))
                print("---")
            else:
                print(f"URL: {result['url']}")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Status: {result.get('status', 'Error')}")
                
                if result.get('error'):
                    print(f"Error: {result['error']}")
                else:
                    print(f"Word Count: {result.get('word_count', 0)}")
                    
                    if args.extract_insights and result.get("content"):
                        insights = extract_meeting_insights(result["content"])
                        if insights["meeting_keywords"]:
                            print(f"Meeting Keywords: {', '.join(insights['meeting_keywords'])}")
                        if insights["preparation_hints"]:
                            print("Preparation Hints:")
                            for hint in insights["preparation_hints"][:3]:
                                print(f"  - {hint}")
                    
                    # Show content preview
                    content = result.get("content", "")
                    if content:
                        preview = content[:500] + "..." if len(content) > 500 else content
                        print(f"Content Preview: {preview}")
                
                print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())