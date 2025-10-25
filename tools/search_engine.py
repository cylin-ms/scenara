#!/usr/bin/env python3
"""
Search engine utility for Scenara project
Enables web search for meeting-related research and information gathering
"""

import argparse
import asyncio
import aiohttp
import sys
from typing import List, Dict, Any
import urllib.parse
import json
import re
from datetime import datetime

class SearchEngine:
    def __init__(self):
        self.session = None
        # You would configure actual search APIs here
        # For demo purposes, we'll use a mock search
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                'User-Agent': 'Scenara Meeting Research Bot 1.0'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for content related to meeting preparation and business context
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with URL, title, and snippet
        """
        try:
            print(f"Searching for: {query}", file=sys.stderr)
            
            # For this demo, we'll create mock results based on the query
            # In a real implementation, you would integrate with:
            # - Google Custom Search API
            # - Bing Search API
            # - DuckDuckGo API
            # - Or other search services
            
            results = await self._mock_search(query, max_results)
            
            # Add metadata
            for result in results:
                result["searched_at"] = datetime.now().isoformat()
                result["query"] = query
            
            return results
        
        except Exception as e:
            print(f"Search error: {e}", file=sys.stderr)
            return []
    
    async def _mock_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Mock search implementation for demonstration
        In production, replace with actual search API
        """
        # Simulate search results based on query content
        meeting_results = [
            {
                "url": "https://hbr.org/2019/05/how-to-run-a-great-virtual-meeting",
                "title": "How to Run a Great Virtual Meeting - Harvard Business Review",
                "snippet": "Virtual meetings are here to stay. Here are evidence-based strategies for making them more productive and engaging for everyone involved."
            },
            {
                "url": "https://www.mckinsey.com/business-functions/organization/our-insights/making-meetings-work",
                "title": "Making meetings work: How to be more effective - McKinsey",
                "snippet": "Meetings are essential for collaboration, but they can be time-wasters. Here's how to make them more productive and purposeful."
            },
            {
                "url": "https://blog.microsoft.com/en-us/2021/03/30/the-future-of-work-the-good-the-challenging-the-unknown/",
                "title": "The Future of Work: Meeting Intelligence and Collaboration",
                "snippet": "Microsoft's vision for the future of work includes AI-powered meeting insights and intelligent collaboration tools."
            }
        ]
        
        strategy_results = [
            {
                "url": "https://www.strategy-business.com/article/Strategic-Planning-Best-Practices",
                "title": "Strategic Planning Best Practices for Modern Organizations",
                "snippet": "Effective strategic planning requires structured meetings, clear objectives, and stakeholder alignment across the organization."
            },
            {
                "url": "https://www.bcg.com/capabilities/strategy/strategic-planning",
                "title": "Strategic Planning and Decision Making - Boston Consulting Group",
                "snippet": "BCG's approach to strategic planning emphasizes data-driven decision making and structured analysis frameworks."
            }
        ]
        
        tech_results = [
            {
                "url": "https://techcrunch.com/2024/01/15/ai-meeting-assistants-revolution/",
                "title": "AI Meeting Assistants Are Revolutionizing Business Communication",
                "snippet": "AI-powered meeting assistants are transforming how businesses prepare for and conduct meetings, providing real-time insights and automation."
            },
            {
                "url": "https://www.wired.com/story/future-of-meetings-ai-collaboration/",
                "title": "The Future of Meetings: AI and Intelligent Collaboration",
                "snippet": "Advanced AI systems are making meetings more efficient by providing intelligent preparation, real-time assistance, and automated follow-up."
            }
        ]
        
        # Select results based on query keywords
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['meeting', 'virtual', 'collaboration']):
            selected_results = meeting_results
        elif any(word in query_lower for word in ['strategy', 'planning', 'decision']):
            selected_results = strategy_results
        elif any(word in query_lower for word in ['ai', 'technology', 'automation']):
            selected_results = tech_results
        else:
            # Mix of all types
            selected_results = meeting_results[:2] + strategy_results[:1] + tech_results[:1]
        
        # Add relevance scores and rank
        for i, result in enumerate(selected_results[:max_results]):
            result["rank"] = i + 1
            result["relevance_score"] = max(0.9 - (i * 0.1), 0.1)
            
            # Add query-specific enhancements
            if any(word in result["title"].lower() for word in query_lower.split()):
                result["relevance_score"] += 0.2
            
            if any(word in result["snippet"].lower() for word in query_lower.split()):
                result["relevance_score"] += 0.1
        
        return selected_results[:max_results]
    
    async def search_meeting_best_practices(self, meeting_type: str) -> List[Dict[str, Any]]:
        """
        Search for best practices specific to a meeting type
        
        Args:
            meeting_type: Type of meeting (e.g., "strategic planning", "team standup")
            
        Returns:
            List of relevant best practice articles and resources
        """
        query = f"{meeting_type} meeting best practices preparation agenda"
        return await self.search(query, max_results=5)
    
    async def search_industry_insights(self, industry: str, topic: str) -> List[Dict[str, Any]]:
        """
        Search for industry-specific insights on a topic
        
        Args:
            industry: Industry context (e.g., "technology", "healthcare", "finance")
            topic: Topic of interest (e.g., "digital transformation", "compliance")
            
        Returns:
            List of industry-specific insights and articles
        """
        query = f"{industry} {topic} trends insights analysis"
        return await self.search(query, max_results=8)

def format_search_results(results: List[Dict[str, Any]], format_type: str = "text") -> str:
    """
    Format search results for display
    
    Args:
        results: List of search results
        format_type: Output format ("text" or "json")
        
    Returns:
        Formatted string representation
    """
    if format_type == "json":
        return json.dumps(results, indent=2)
    
    output = []
    for result in results:
        output.append(f"URL: {result['url']}")
        output.append(f"Title: {result['title']}")
        output.append(f"Snippet: {result['snippet']}")
        
        if result.get('relevance_score'):
            output.append(f"Relevance: {result['relevance_score']:.2f}")
        
        if result.get('rank'):
            output.append(f"Rank: {result['rank']}")
        
        output.append("")  # Empty line between results
    
    return "\n".join(output)

async def main():
    parser = argparse.ArgumentParser(description="Search engine for PromptCoT meeting research")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10,
                       help="Maximum number of results")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format")
    parser.add_argument("--meeting-type", help="Search for meeting type best practices")
    parser.add_argument("--industry", help="Industry context for search")
    parser.add_argument("--topic", help="Topic for industry-specific search")
    
    args = parser.parse_args()
    
    async with SearchEngine() as search_engine:
        if args.meeting_type:
            results = await search_engine.search_meeting_best_practices(args.meeting_type)
        elif args.industry and args.topic:
            results = await search_engine.search_industry_insights(args.industry, args.topic)
        else:
            results = await search_engine.search(args.query, args.max_results)
        
        output = format_search_results(results, args.format)
        print(output)

if __name__ == "__main__":
    asyncio.run(main())