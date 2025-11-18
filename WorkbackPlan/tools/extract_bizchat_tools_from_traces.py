#!/usr/bin/env python3
"""
Extract BizChat Tool Inventory from Conversation Traces
Analyzes DevUI traces, BizChat responses, or conversation data to identify tool calls

Author: Chin-Yew Lin
Date: November 18, 2025
"""

import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class ToolCall:
    """Represents a single tool invocation"""
    tool_id: str
    tool_name: str
    description: str
    parameters: Dict[str, Any]
    context: str
    timestamp: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None


@dataclass
class ToolDefinition:
    """Complete tool definition for registry"""
    tool_id: str
    tool_name: str
    description: str
    category: str
    parameters: List[Dict[str, str]]
    returns: str
    examples: List[str]
    frequency: int
    reliability: str
    cost: str


class BizChatToolExtractor:
    """Extract tool calls from BizChat conversation traces"""
    
    def __init__(self):
        self.tool_calls: List[ToolCall] = []
        self.tool_registry: Dict[str, ToolDefinition] = {}
        
        # Known tool patterns (from SilverFlow analysis)
        self.known_tools = {
            # Graph API Tools
            "graph_calendar_get_events": {
                "name": "Get Calendar Events",
                "category": "Calendar & Scheduling",
                "description": "Retrieve calendar events for a user in date range"
            },
            "graph_get_meetings": {
                "name": "Get Meetings",
                "category": "Calendar & Scheduling",
                "description": "Fetch meeting details with attendees and metadata"
            },
            "graph_send_meeting_response": {
                "name": "Send Meeting Response",
                "category": "Calendar & Scheduling",
                "description": "Accept, tentative, or decline meeting invitations"
            },
            
            # Communication Tools
            "graph_get_chats": {
                "name": "Get Teams Chats",
                "category": "Communication",
                "description": "Retrieve Teams chat conversations"
            },
            "graph_get_chat_messages": {
                "name": "Get Chat Messages",
                "category": "Communication",
                "description": "Fetch messages from a specific chat thread"
            },
            "substrate_get_my_chats": {
                "name": "Get My Chats",
                "category": "Communication",
                "description": "List user's recent Teams chats with context"
            },
            
            # Email Tools
            "graph_get_mails": {
                "name": "Get Emails",
                "category": "Email",
                "description": "Retrieve email messages from mailbox"
            },
            "graph_get_mail_content": {
                "name": "Get Email Content",
                "category": "Email",
                "description": "Fetch full content of specific email"
            },
            "graph_send_mail": {
                "name": "Send Email",
                "category": "Email",
                "description": "Send email message to recipients"
            },
            
            # Search Tools
            "bizchat_search": {
                "name": "Search Content",
                "category": "Search & Discovery",
                "description": "Search across meetings, chats, documents, and email"
            },
            "bizchat_search_meetings": {
                "name": "Search Meetings",
                "category": "Search & Discovery",
                "description": "Search specifically for meeting content"
            },
            "bizchat_search_chats": {
                "name": "Search Chats",
                "category": "Search & Discovery",
                "description": "Search Teams chat history"
            },
            "bizchat_search_documents": {
                "name": "Search Documents",
                "category": "Search & Discovery",
                "description": "Search for documents and files"
            },
            
            # Document Tools
            "graph_get_document": {
                "name": "Get Document",
                "category": "Documents & Files",
                "description": "Retrieve document content and metadata"
            },
            "graph_get_loop_content": {
                "name": "Get Loop Content",
                "category": "Documents & Files",
                "description": "Fetch Loop workspace content"
            },
            "fetch_loop_content": {
                "name": "Fetch Loop Content",
                "category": "Documents & Files",
                "description": "Download Loop component content"
            },
            
            # People & Organization
            "graph_get_people": {
                "name": "Get People",
                "category": "People & Organization",
                "description": "Search for people and retrieve profiles"
            },
            "graph_get_manager": {
                "name": "Get Manager",
                "category": "People & Organization",
                "description": "Retrieve user's manager information"
            },
            "loki_get_person_recap": {
                "name": "Get Person Recap",
                "category": "People & Organization",
                "description": "Get comprehensive person profile with insights"
            },
            
            # Context & Intelligence
            "bizchat_context": {
                "name": "Get Context",
                "category": "Context & Intelligence",
                "description": "Retrieve contextual information for user's work"
            },
            "bizchat_recommendations": {
                "name": "Get Recommendations",
                "category": "Context & Intelligence",
                "description": "Get meeting recommendations and related content"
            },
            "substrate_meeting_prep": {
                "name": "Meeting Preparation",
                "category": "Context & Intelligence",
                "description": "Generate meeting preparation insights"
            },
            
            # Work Items (ADO)
            "ado_get_work_items": {
                "name": "Get Work Items",
                "category": "Work Tracking",
                "description": "Retrieve Azure DevOps work items"
            },
            "bizchat_search_ado": {
                "name": "Search ADO",
                "category": "Work Tracking",
                "description": "Search Azure DevOps content"
            }
        }
    
    def extract_from_devui_url(self, devui_url: str) -> List[ToolCall]:
        """
        Extract tool calls from a DevUI URL
        
        DevUI URLs typically encode conversation traces with tool invocations.
        This is a placeholder - actual implementation depends on DevUI URL structure.
        """
        print(f"⚠️ DevUI URL parsing not yet implemented")
        print(f"   URL: {devui_url}")
        print(f"   To implement: Need example DevUI URL structure")
        return []
    
    def extract_from_conversation_json(self, conversation_data: Dict[str, Any]) -> List[ToolCall]:
        """Extract tool calls from BizChat conversation JSON"""
        
        tool_calls = []
        
        # Pattern 1: Direct tool invocations in messages
        if "messages" in conversation_data:
            for msg in conversation_data["messages"]:
                tool_calls.extend(self._extract_from_message(msg))
        
        # Pattern 2: Tool results in adaptive cards
        if "adaptiveCards" in conversation_data:
            for card in conversation_data["adaptiveCards"]:
                tool_calls.extend(self._extract_from_adaptive_card(card))
        
        # Pattern 3: Plugin invocations
        if "plugins" in conversation_data:
            for plugin in conversation_data["plugins"]:
                tool_calls.extend(self._extract_from_plugin(plugin))
        
        # Pattern 4: Search results (indicate search tool usage)
        if "searchResults" in conversation_data:
            tool_calls.extend(self._extract_from_search_results(conversation_data["searchResults"]))
        
        return tool_calls
    
    def _extract_from_message(self, message: Dict[str, Any]) -> List[ToolCall]:
        """Extract tool calls from a message object"""
        tool_calls = []
        
        # Check for function calls in message metadata
        if "functionCalls" in message:
            for fc in message["functionCalls"]:
                tool_calls.append(ToolCall(
                    tool_id=fc.get("name", "unknown"),
                    tool_name=fc.get("displayName", fc.get("name", "Unknown")),
                    description=fc.get("description", ""),
                    parameters=fc.get("arguments", {}),
                    context=message.get("text", "")[:200],
                    timestamp=message.get("timestamp"),
                    success=fc.get("status") != "failed",
                    error_message=fc.get("error")
                ))
        
        # Check for tool mentions in message text
        text = message.get("text", "")
        for tool_id, tool_info in self.known_tools.items():
            if tool_info["name"].lower() in text.lower():
                # Infer tool usage from context
                tool_calls.append(ToolCall(
                    tool_id=tool_id,
                    tool_name=tool_info["name"],
                    description=tool_info["description"],
                    parameters={},
                    context=text[:200],
                    timestamp=message.get("timestamp")
                ))
        
        return tool_calls
    
    def _extract_from_adaptive_card(self, card: Dict[str, Any]) -> List[ToolCall]:
        """Extract tool calls from adaptive card data"""
        tool_calls = []
        
        # Adaptive cards often show results from tool calls
        if "body" in card:
            for element in card["body"]:
                if element.get("type") == "Container":
                    # Check for tool result indicators
                    facts = element.get("facts", [])
                    for fact in facts:
                        if "source" in fact.get("title", "").lower():
                            # Tool result found
                            source = fact.get("value", "")
                            tool_id = self._infer_tool_from_source(source)
                            if tool_id:
                                tool_calls.append(ToolCall(
                                    tool_id=tool_id,
                                    tool_name=self.known_tools.get(tool_id, {}).get("name", source),
                                    description=f"Retrieved from {source}",
                                    parameters={},
                                    context=json.dumps(card)[:200]
                                ))
        
        return tool_calls
    
    def _extract_from_plugin(self, plugin: Dict[str, Any]) -> List[ToolCall]:
        """Extract tool calls from plugin invocation"""
        tool_calls = []
        
        plugin_name = plugin.get("pluginName", "")
        invocations = plugin.get("invocations", [])
        
        for inv in invocations:
            tool_calls.append(ToolCall(
                tool_id=f"plugin_{plugin_name}_{inv.get('method', 'invoke')}",
                tool_name=f"{plugin_name} - {inv.get('method', 'invoke')}",
                description=inv.get("description", f"Plugin invocation: {plugin_name}"),
                parameters=inv.get("parameters", {}),
                context=json.dumps(plugin)[:200],
                success=inv.get("status") == "completed",
                error_message=inv.get("error")
            ))
        
        return tool_calls
    
    def _extract_from_search_results(self, search_results: Dict[str, Any]) -> List[ToolCall]:
        """Extract search tool usage from search results"""
        tool_calls = []
        
        # Determine search type from result categories
        result_types = set()
        if "results" in search_results:
            for result in search_results["results"]:
                result_type = result.get("@odata.type", "").split(".")[-1]
                result_types.add(result_type)
        
        # Map result types to search tools
        search_tool_mapping = {
            "message": "bizchat_search_chats",
            "event": "bizchat_search_meetings",
            "driveItem": "bizchat_search_documents",
            "mail": "bizchat_search_mail"
        }
        
        for result_type in result_types:
            tool_id = search_tool_mapping.get(result_type, "bizchat_search")
            tool_info = self.known_tools.get(tool_id, {})
            
            tool_calls.append(ToolCall(
                tool_id=tool_id,
                tool_name=tool_info.get("name", "Search"),
                description=tool_info.get("description", "Search operation"),
                parameters={"query": search_results.get("query", ""), "type": result_type},
                context=f"Search returned {len(search_results.get('results', []))} results"
            ))
        
        return tool_calls
    
    def _infer_tool_from_source(self, source: str) -> Optional[str]:
        """Infer tool ID from source string"""
        source_lower = source.lower()
        
        if "calendar" in source_lower or "meeting" in source_lower:
            return "graph_calendar_get_events"
        elif "chat" in source_lower or "teams" in source_lower:
            return "graph_get_chats"
        elif "mail" in source_lower or "email" in source_lower:
            return "graph_get_mails"
        elif "document" in source_lower or "file" in source_lower:
            return "graph_get_document"
        elif "people" in source_lower or "person" in source_lower:
            return "graph_get_people"
        
        return None
    
    def build_tool_registry(self) -> Dict[str, ToolDefinition]:
        """Build complete tool registry from extracted calls"""
        
        # Count tool frequencies
        tool_frequency = Counter(tc.tool_id for tc in self.tool_calls)
        success_counts = Counter(tc.tool_id for tc in self.tool_calls if tc.success)
        
        registry = {}
        
        for tool_id, tool_info in self.known_tools.items():
            frequency = tool_frequency.get(tool_id, 0)
            success_rate = success_counts.get(tool_id, 0) / max(frequency, 1)
            
            # Extract parameter schemas from actual usage
            params_seen = defaultdict(set)
            for tc in self.tool_calls:
                if tc.tool_id == tool_id:
                    for param_name, param_value in tc.parameters.items():
                        params_seen[param_name].add(type(param_value).__name__)
            
            parameters = [
                {
                    "name": param_name,
                    "type": "|".join(sorted(param_types)),
                    "required": True  # Conservative: assume required
                }
                for param_name, param_types in params_seen.items()
            ]
            
            # Determine reliability and cost
            reliability = "high" if success_rate >= 0.95 else "medium" if success_rate >= 0.80 else "low"
            cost = self._estimate_cost(tool_id)
            
            registry[tool_id] = ToolDefinition(
                tool_id=tool_id,
                tool_name=tool_info["name"],
                description=tool_info["description"],
                category=tool_info["category"],
                parameters=parameters,
                returns=self._infer_return_type(tool_id),
                examples=[tc.context for tc in self.tool_calls if tc.tool_id == tool_id][:3],
                frequency=frequency,
                reliability=reliability,
                cost=cost
            )
        
        return registry
    
    def _estimate_cost(self, tool_id: str) -> str:
        """Estimate tool invocation cost"""
        # Graph API calls are generally low cost
        if tool_id.startswith("graph_"):
            return "low"
        # Search operations are medium cost
        elif "search" in tool_id:
            return "medium"
        # LLM-enhanced operations are higher cost
        elif "context" in tool_id or "recommendation" in tool_id:
            return "high"
        else:
            return "medium"
    
    def _infer_return_type(self, tool_id: str) -> str:
        """Infer return type from tool ID"""
        if "calendar" in tool_id or "meeting" in tool_id:
            return "List[Event]"
        elif "chat" in tool_id or "message" in tool_id:
            return "List[Message]"
        elif "mail" in tool_id:
            return "List[Email]"
        elif "document" in tool_id:
            return "Document | List[Document]"
        elif "people" in tool_id:
            return "List[Person]"
        elif "search" in tool_id:
            return "SearchResults"
        else:
            return "Dict[str, Any]"
    
    def process_directory(self, input_dir: Path) -> None:
        """Process all JSON files in a directory"""
        
        print(f"🔍 Scanning directory: {input_dir}")
        
        json_files = list(input_dir.glob("**/*.json"))
        print(f"📁 Found {len(json_files)} JSON files")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Try to extract tool calls
                extracted = self.extract_from_conversation_json(data)
                self.tool_calls.extend(extracted)
                
                if extracted:
                    print(f"  ✅ {json_file.name}: {len(extracted)} tool calls")
                
            except Exception as e:
                print(f"  ⚠️ {json_file.name}: Error - {e}")
    
    def export_tool_registry(self, output_path: Path) -> None:
        """Export tool registry to JSON"""
        
        registry = self.build_tool_registry()
        
        output_data = {
            "environment": "Microsoft BizChat",
            "version": "2.0",
            "extraction_date": datetime.now().isoformat(),
            "total_tools": len(registry),
            "tool_calls_analyzed": len(self.tool_calls),
            "tools": [asdict(tool_def) for tool_def in registry.values()]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n✅ Tool registry exported: {output_path}")
        print(f"   Total tools: {len(registry)}")
        print(f"   Tool calls analyzed: {len(self.tool_calls)}")
        
        # Print summary by category
        by_category = defaultdict(list)
        for tool_def in registry.values():
            by_category[tool_def.category].append(tool_def)
        
        print(f"\n📊 Tools by Category:")
        for category, tools in sorted(by_category.items()):
            print(f"   {category}: {len(tools)} tools")
            for tool in sorted(tools, key=lambda t: t.frequency, reverse=True)[:3]:
                print(f"      - {tool.tool_name} (used {tool.frequency}x)")


def main():
    parser = argparse.ArgumentParser(
        description="Extract BizChat tool inventory from conversation traces"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("../SilverFlow/data/out"),
        help="Directory containing BizChat conversation JSON files"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("../docs/bizchat_tool_registry.json"),
        help="Output path for tool registry JSON"
    )
    parser.add_argument(
        "--devui-url",
        type=str,
        help="DevUI URL to parse (optional)"
    )
    
    args = parser.parse_args()
    
    print("🚀 BizChat Tool Extractor")
    print("=" * 70)
    
    extractor = BizChatToolExtractor()
    
    # Process DevUI URL if provided
    if args.devui_url:
        print(f"\n🔗 Processing DevUI URL...")
        extractor.extract_from_devui_url(args.devui_url)
    
    # Process directory
    if args.input_dir.exists():
        extractor.process_directory(args.input_dir)
    else:
        print(f"⚠️ Input directory not found: {args.input_dir}")
    
    # Export registry
    args.output.parent.mkdir(parents=True, exist_ok=True)
    extractor.export_tool_registry(args.output)
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
