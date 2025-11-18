#!/usr/bin/env python3
"""
Integrate ContextFlow Tool Data with BizChat Tool Registry
Extract tool calls from ContextFlow telemetry and update tool registry

Author: Chin-Yew Lin
Date: November 18, 2025
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict
from datetime import datetime
import argparse


class ContextFlowToolIntegrator:
    """
    Integrates tool call data from ContextFlow desktop app with BizChat tool registry.
    
    ContextFlow Architecture:
    - Desktop app (Tauri: TypeScript/React + Rust)
    - Captures ChatHub WebSocket streams (Sydney/Copilot)
    - Processes telemetry: messages, tools, prompts
    - Provides UI for inspecting BizChat internal flow
    
    Tool Data Sources:
    1. ChatHub Messages (role='tool' with tool results)
    2. Telemetry Metrics (service calls with input/output)
    3. Workflow Steps (tool-call type steps)
    """
    
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.registry = self._load_registry()
        self.tool_calls = []
        self.new_tools_discovered = []
    
    def _load_registry(self) -> Dict:
        """Load existing tool registry"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "environment": "Microsoft BizChat",
            "version": "2.0",
            "extraction_date": datetime.now().isoformat(),
            "total_tools": 0,
            "tool_calls_analyzed": 0,
            "tools": []
        }
    
    def process_contextflow_session(self, session_file: Path) -> None:
        """
        Process a ContextFlow session export (JSON)
        
        Expected structure (from CopilotSession interface):
        {
          "id": "session_xxx",
          "conversationId": "conv_xxx",
          "messages": [...],
          "workflowTrace": {"steps": [...]},
          "telemetry": {"metrics": [...]}
        }
        """
        print(f"\n📂 Processing ContextFlow session: {session_file.name}")
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session = json.load(f)
        
        # Extract from messages (role='tool')
        messages = session.get('messages', [])
        tool_messages = [m for m in messages if m.get('author') == 'tool']
        print(f"   Found {len(tool_messages)} tool messages")
        
        for msg in tool_messages:
            self._extract_from_tool_message(msg)
        
        # Extract from workflow steps (type='tool-call')
        workflow_steps = session.get('workflowTrace', {}).get('steps', [])
        tool_steps = [s for s in workflow_steps if s.get('type') == 'tool-call']
        print(f"   Found {len(tool_steps)} tool-call steps")
        
        for step in tool_steps:
            self._extract_from_workflow_step(step)
        
        # Extract from telemetry metrics
        telemetry = session.get('telemetry', {})
        metrics = telemetry.get('metrics', [])
        print(f"   Found {len(metrics)} telemetry metrics")
        
        for metric in metrics:
            self._extract_from_telemetry_metric(metric)
    
    def _extract_from_tool_message(self, message: Dict) -> None:
        """
        Extract tool calls from ChatHub tool messages
        
        Structure (from ToolsView.tsx):
        {
          "author": "tool",
          "messageType": "Tool",
          "content": "{\"results\": [{\"result\": {...}}]}",
          "timestamp": "...",
          ...
        }
        """
        content = message.get('content', '')
        if not content:
            return
        
        try:
            parsed = json.loads(content) if isinstance(content, str) else content
        except json.JSONDecodeError:
            return
        
        # Extract results array
        results = parsed.get('results', [])
        for result_wrapper in results:
            result = result_wrapper.get('result', result_wrapper)
            
            # Infer tool from result type
            result_type = result.get('type', '')
            tool_id = self._infer_tool_from_result_type(result_type)
            
            if tool_id:
                self.tool_calls.append({
                    'tool_id': tool_id,
                    'timestamp': message.get('timestamp'),
                    'result_type': result_type,
                    'reference_id': result.get('reference_id'),
                    'title': result.get('title', ''),
                    'source': 'tool_message',
                    'success': True
                })
    
    def _extract_from_workflow_step(self, step: Dict) -> None:
        """
        Extract tool calls from workflow steps
        
        Structure (from WorkflowStep interface):
        {
          "id": "step_xxx",
          "type": "tool-call",
          "timestamp": "...",
          "data": {...},
          "duration": 123,
          "status": "completed"
        }
        """
        step_data = step.get('data', {})
        tool_name = step_data.get('tool_name') or step_data.get('name')
        
        if tool_name:
            # Normalize tool name to tool_id
            tool_id = tool_name.lower().replace(' ', '_').replace('-', '_')
            
            self.tool_calls.append({
                'tool_id': tool_id,
                'tool_name': tool_name,
                'timestamp': step.get('timestamp'),
                'duration': step.get('duration'),
                'status': step.get('status'),
                'source': 'workflow_step',
                'success': step.get('status') == 'completed'
            })
    
    def _extract_from_telemetry_metric(self, metric: Dict) -> None:
        """
        Extract tool calls from telemetry metrics
        
        Structure (from TelemetryMetric interface):
        {
          "id": "metric_xxx",
          "serviceName": "DeepLeoImprovedNetworking",
          "input": "{...}",
          "output": "{...}",
          "path": "/api/...",
          "latencyMilliseconds": 123,
          "metricType": "...",
          "status": "success"
        }
        """
        service_name = metric.get('serviceName', '')
        path = metric.get('path', '')
        
        # Map service names to tool categories
        tool_mapping = {
            'DeepLeoImprovedNetworking': 'bizchat_context',
            'GraphAPI': 'graph_api',
            'SubstrateSearch': 'substrate_search',
            'LokiPeople': 'loki_people'
        }
        
        base_tool = tool_mapping.get(service_name)
        if base_tool:
            # Refine based on path
            tool_id = self._refine_tool_from_path(base_tool, path)
            
            self.tool_calls.append({
                'tool_id': tool_id,
                'service_name': service_name,
                'path': path,
                'timestamp': metric.get('timestamp'),
                'latency': metric.get('latencyMilliseconds'),
                'status': metric.get('status'),
                'source': 'telemetry_metric',
                'success': metric.get('status') == 'success'
            })
    
    def _infer_tool_from_result_type(self, result_type: str) -> Optional[str]:
        """Map result type to tool ID"""
        type_mapping = {
            'Event': 'graph_calendar_get_events',
            'Message': 'graph_get_chat_messages',
            'Mail': 'graph_get_mails',
            'DriveItem': 'graph_get_document',
            'Person': 'graph_get_people',
            'WorkItem': 'ado_get_work_items',
            'SearchResult': 'bizchat_search',
            'MeetingInsight': 'substrate_meeting_prep',
            'Recommendation': 'bizchat_recommendations'
        }
        return type_mapping.get(result_type)
    
    def _refine_tool_from_path(self, base_tool: str, path: str) -> str:
        """Refine tool ID based on API path"""
        if not path:
            return base_tool
        
        path_lower = path.lower()
        
        # Graph API refinements
        if 'calendar' in path_lower or 'event' in path_lower:
            return 'graph_calendar_get_events'
        elif 'chat' in path_lower or 'message' in path_lower:
            return 'graph_get_chats'
        elif 'mail' in path_lower:
            return 'graph_get_mails'
        elif 'people' in path_lower:
            return 'graph_get_people'
        elif 'drive' in path_lower or 'document' in path_lower:
            return 'graph_get_document'
        
        # Substrate refinements
        elif 'search' in path_lower:
            if 'meeting' in path_lower:
                return 'bizchat_search_meetings'
            elif 'chat' in path_lower:
                return 'bizchat_search_chats'
            elif 'mail' in path_lower:
                return 'bizchat_search_mail'
            else:
                return 'bizchat_search'
        elif 'recommendation' in path_lower:
            return 'bizchat_recommendations'
        elif 'context' in path_lower:
            return 'bizchat_context'
        
        return base_tool
    
    def update_registry(self) -> None:
        """Update tool registry with usage statistics from captured tool calls"""
        
        print(f"\n📊 Analyzing {len(self.tool_calls)} tool calls...")
        
        # Count frequencies and success rates
        tool_frequency = Counter(tc['tool_id'] for tc in self.tool_calls)
        success_counts = Counter(tc['tool_id'] for tc in self.tool_calls if tc.get('success'))
        
        # Calculate average latencies
        latencies = defaultdict(list)
        for tc in self.tool_calls:
            if 'latency' in tc or 'duration' in tc:
                latency = tc.get('latency') or tc.get('duration')
                if latency:
                    latencies[tc['tool_id']].append(latency)
        
        # Update existing tools in registry
        tools_by_id = {t['tool_id']: t for t in self.registry['tools']}
        
        for tool_id, count in tool_frequency.items():
            if tool_id in tools_by_id:
                tool = tools_by_id[tool_id]
                tool['frequency'] = tool.get('frequency', 0) + count
                
                # Update reliability
                success_rate = success_counts.get(tool_id, 0) / count
                if success_rate >= 0.95:
                    tool['reliability'] = 'high'
                elif success_rate >= 0.80:
                    tool['reliability'] = 'medium'
                else:
                    tool['reliability'] = 'low'
                
                # Add average latency if available
                if tool_id in latencies:
                    avg_latency = sum(latencies[tool_id]) / len(latencies[tool_id])
                    tool['avg_latency_ms'] = round(avg_latency, 2)
                
                print(f"   ✅ Updated {tool['tool_name']}: {count} calls, {success_rate:.1%} success")
            else:
                # New tool discovered
                print(f"   🆕 Discovered new tool: {tool_id} ({count} calls)")
                self.new_tools_discovered.append({
                    'tool_id': tool_id,
                    'frequency': count,
                    'success_rate': success_counts.get(tool_id, 0) / count
                })
        
        # Update metadata
        self.registry['tool_calls_analyzed'] += len(self.tool_calls)
        self.registry['extraction_date'] = datetime.now().isoformat()
        self.registry['contextflow_integrated'] = True
        self.registry['contextflow_integration_date'] = datetime.now().isoformat()
    
    def export_registry(self) -> None:
        """Export updated tool registry"""
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2)
        
        print(f"\n✅ Updated registry saved: {self.registry_path}")
        print(f"   Total tools: {len(self.registry['tools'])}")
        print(f"   Total calls analyzed: {self.registry['tool_calls_analyzed']}")
        
        if self.new_tools_discovered:
            print(f"\n🆕 New tools discovered: {len(self.new_tools_discovered)}")
            for tool in self.new_tools_discovered:
                print(f"   - {tool['tool_id']}: {tool['frequency']} calls, {tool['success_rate']:.1%} success")
            print("\n   ⚠️  Please add tool definitions for new tools in the registry")
    
    def generate_usage_report(self, output_path: Path) -> None:
        """Generate detailed usage report"""
        
        # Top tools by frequency
        tool_frequency = Counter(tc['tool_id'] for tc in self.tool_calls)
        top_tools = tool_frequency.most_common(10)
        
        # Tools by category
        tools_by_id = {t['tool_id']: t for t in self.registry['tools']}
        by_category = defaultdict(list)
        for tool_id, count in tool_frequency.items():
            if tool_id in tools_by_id:
                category = tools_by_id[tool_id]['category']
                by_category[category].append((tool_id, count))
        
        # Generate report
        report = {
            "report_date": datetime.now().isoformat(),
            "total_tool_calls": len(self.tool_calls),
            "unique_tools_used": len(tool_frequency),
            "top_tools": [
                {
                    "tool_id": tool_id,
                    "tool_name": tools_by_id.get(tool_id, {}).get('tool_name', tool_id),
                    "calls": count,
                    "percentage": f"{count/len(self.tool_calls)*100:.1f}%"
                }
                for tool_id, count in top_tools
            ],
            "usage_by_category": {
                category: {
                    "total_calls": sum(c for _, c in tools),
                    "tools": [
                        {
                            "tool_id": tid,
                            "calls": c,
                            "tool_name": tools_by_id.get(tid, {}).get('tool_name', tid)
                        }
                        for tid, c in sorted(tools, key=lambda x: x[1], reverse=True)
                    ]
                }
                for category, tools in by_category.items()
            },
            "new_tools_discovered": self.new_tools_discovered
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Usage report saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Integrate ContextFlow tool data with BizChat tool registry"
    )
    parser.add_argument(
        "--session-file",
        type=Path,
        help="ContextFlow session export JSON file"
    )
    parser.add_argument(
        "--session-dir",
        type=Path,
        help="Directory containing multiple ContextFlow session files"
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("../docs/bizchat_tool_registry.json"),
        help="Path to tool registry JSON"
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("../docs/tool_usage_report.json"),
        help="Output path for usage report"
    )
    
    args = parser.parse_args()
    
    print("🔗 ContextFlow → BizChat Tool Registry Integration")
    print("=" * 70)
    
    integrator = ContextFlowToolIntegrator(args.registry)
    
    # Process session file(s)
    if args.session_file:
        integrator.process_contextflow_session(args.session_file)
    elif args.session_dir:
        if args.session_dir.exists():
            session_files = list(args.session_dir.glob("*.json"))
            print(f"Found {len(session_files)} session files")
            for session_file in session_files:
                integrator.process_contextflow_session(session_file)
        else:
            print(f"⚠️  Session directory not found: {args.session_dir}")
    else:
        print("⚠️  No session file or directory provided")
        print("   Usage:")
        print("     --session-file path/to/session.json")
        print("     --session-dir path/to/sessions/")
        return
    
    # Update registry
    integrator.update_registry()
    integrator.export_registry()
    
    # Generate report
    args.report.parent.mkdir(parents=True, exist_ok=True)
    integrator.generate_usage_report(args.report)
    
    print("\n✨ Integration complete!")
    print("\n📝 Next steps:")
    print("   1. Review new tools discovered")
    print("   2. Add tool definitions to registry")
    print("   3. Update training data with real tool usage patterns")
    print("   4. Validate tool grounding in TOOL_GROUNDED_TRAINING.md")


if __name__ == "__main__":
    main()
