#!/usr/bin/env python3
"""
Quick analysis of the current MyGraph data
"""

import re
import json
from datetime import datetime

def extract_graph_data():
    """Extract graph data from the HTML file"""
    html_file = "/Users/cyl/projects/Scenara/docs/mygraph_explorer.html"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the graph data
        pattern = r'const graph = \{ nodes: (\[.*?\]), links: (\[.*?\]) \};'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            nodes_str = match.group(1)
            links_str = match.group(2)
            
            try:
                nodes = json.loads(nodes_str)
                links = json.loads(links_str)
                return nodes, links
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON: {e}")
                return None, None
        else:
            print("❌ Could not find graph data in HTML file")
            return None, None
            
    except FileNotFoundError:
        print(f"❌ File not found: {html_file}")
        return None, None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None, None

def analyze_data(nodes, links):
    """Analyze the graph data"""
    print("🎯 MyGraph Data Analysis")
    print("=" * 50)
    
    # Basic stats
    print(f"📊 Total Nodes: {len(nodes)}")
    print(f"🔗 Total Links: {len(links)}")
    print()
    
    # Node types
    node_types = {}
    for node in nodes:
        node_type = node.get('type', 'Unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    print("📝 Node Types:")
    for node_type, count in sorted(node_types.items()):
        print(f"   {node_type}: {count}")
    print()
    
    # Link types
    link_types = {}
    for link in links:
        link_type = link.get('type', 'Unknown')
        link_types[link_type] = link_types.get(link_type, 0) + 1
    
    print("🔗 Link Types:")
    for link_type, count in sorted(link_types.items()):
        print(f"   {link_type}: {count}")
    print()
    
    # Data sources
    sources = {}
    for node in nodes:
        prov = node.get('prov', {})
        source = prov.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print("📡 Data Sources:")
    for source, count in sorted(sources.items()):
        print(f"   {source}: {count}")
    print()
    
    # Most recent data
    most_recent = None
    for node in nodes:
        prov = node.get('prov', {})
        fetched_at = prov.get('fetched_at')
        if fetched_at:
            try:
                dt = datetime.fromisoformat(fetched_at.replace('Z', '+00:00'))
                if most_recent is None or dt > most_recent:
                    most_recent = dt
            except:
                pass
    
    if most_recent:
        days_old = (datetime.now(most_recent.tzinfo) - most_recent).days
        print(f"📅 Most Recent Data: {most_recent.strftime('%Y-%m-%d %H:%M:%S')} ({days_old} days ago)")
    
    print()
    
    # Sample nodes
    print("🔍 Sample Nodes:")
    for i, node in enumerate(nodes[:5]):
        node_type = node.get('type', 'Unknown')
        display_name = ""
        if 'properties' in node:
            props = node['properties']
            display_name = props.get('displayName', props.get('topic', props.get('subject', '')))
        
        if not display_name:
            display_name = node.get('title', node.get('id', '')[:50])
        
        print(f"   {i+1}. [{node_type}] {display_name}")
    
    print(f"   ... and {len(nodes)-5} more")

def main():
    """Main function"""
    print("🌐 Analyzing MyGraph Data...")
    print()
    
    nodes, links = extract_graph_data()
    
    if nodes is not None and links is not None:
        analyze_data(nodes, links)
        
        print()
        print("💡 Next Steps:")
        print("1. View the graph: Open docs/mygraph_explorer.html in a browser")
        print("2. Fresh data: Use the automation tools to collect new data")
        print("3. Manual update: Use the fallback methods to add specific data")
    else:
        print("❌ Could not analyze graph data")

if __name__ == "__main__":
    main()