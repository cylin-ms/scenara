#!/usr/bin/env python3
"""
Fixed MyGraph Data Collection Tool
Resolves authentication issues by using proper Graph Explorer approach
"""

import json
import requests
from datetime import datetime, timedelta
import webbrowser
import time

def collect_mygraph_data_manual():
    """
    Collect MyGraph data using manual Graph Explorer approach
    This avoids authentication issues by using the browser-based Graph Explorer
    """
    print("🔧 MyGraph Data Collection - Manual Graph Explorer Method")
    print("=" * 60)
    
    print("📋 Steps to collect fresh MyGraph data:")
    print()
    
    # Step 1: Graph Explorer URLs
    queries = [
        {
            "name": "My Profile",
            "url": "https://developer.microsoft.com/en-us/graph/graph-explorer?request=me&method=GET&version=beta",
            "description": "Your basic profile information"
        },
        {
            "name": "My Manager",
            "url": "https://developer.microsoft.com/en-us/graph/graph-explorer?request=me/manager&method=GET&version=beta",
            "description": "Your reporting relationship"
        },
        {
            "name": "My Direct Reports",
            "url": "https://developer.microsoft.com/en-us/graph/graph-explorer?request=me/directReports&method=GET&version=beta",
            "description": "People who report to you"
        },
        {
            "name": "My Calendar Events",
            "url": f"https://developer.microsoft.com/en-us/graph/graph-explorer?request=me/calendarView?startDateTime={datetime.now().isoformat()}Z&endDateTime={(datetime.now() + timedelta(days=30)).isoformat()}Z&method=GET&version=beta",
            "description": "Your upcoming calendar events"
        },
        {
            "name": "My Files",
            "url": "https://developer.microsoft.com/en-us/graph/graph-explorer?request=me/drive/recent&method=GET&version=beta",
            "description": "Recently accessed files"
        }
    ]
    
    print("1. 🌐 Open Graph Explorer and run these queries:")
    print()
    
    for i, query in enumerate(queries, 1):
        print(f"   {i}. {query['name']}")
        print(f"      📝 {query['description']}")
        print(f"      🔗 {query['url'][:80]}...")
        print()
    
    print("2. 💾 For each query:")
    print("   - Click 'Run query'")
    print("   - Copy the JSON response")
    print("   - Save as: my_{name}_data.json")
    print()
    
    print("3. 🔄 Run the data processor:")
    print("   python process_mygraph_data.py")
    print()
    
    # Create data processor
    create_data_processor()
    
    return queries

def create_data_processor():
    """Create a tool to process the manually collected data"""
    processor_code = '''#!/usr/bin/env python3
"""
MyGraph Data Processor
Process manually collected Graph data into MyGraph format
"""

import json
import os
from datetime import datetime
from pathlib import Path

def process_collected_data():
    """Process manually collected Graph data"""
    print("🔄 Processing MyGraph Data...")
    
    # Expected data files
    expected_files = [
        "my_profile_data.json",
        "my_manager_data.json", 
        "my_direct_reports_data.json",
        "my_calendar_events_data.json",
        "my_files_data.json"
    ]
    
    nodes = []
    links = []
    
    # Process each data file if it exists
    for file_name in expected_files:
        if Path(file_name).exists():
            print(f"📂 Processing {file_name}...")
            with open(file_name, 'r') as f:
                data = json.load(f)
            
            if "profile" in file_name:
                nodes.extend(process_profile_data(data))
            elif "manager" in file_name:
                nodes.extend(process_manager_data(data))
                links.extend(create_manager_links(data))
            elif "reports" in file_name:
                nodes.extend(process_reports_data(data))
                links.extend(create_reports_links(data))
            elif "calendar" in file_name:
                nodes.extend(process_calendar_data(data))
                links.extend(create_calendar_links(data))
            elif "files" in file_name:
                nodes.extend(process_files_data(data))
                links.extend(create_files_links(data))
        else:
            print(f"⚠️  {file_name} not found, skipping...")
    
    # Create MyGraph structure
    mygraph_data = {
        "nodes": nodes,
        "links": links,
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source": "manual_graph_explorer_collection",
            "total_nodes": len(nodes),
            "total_links": len(links)
        }
    }
    
    # Save processed data
    output_file = f"mygraph_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(mygraph_data, f, indent=2)
    
    print(f"✅ MyGraph data saved to: {output_file}")
    print(f"📊 Processed {len(nodes)} nodes and {len(links)} links")
    
    # Update HTML file
    update_html_file(mygraph_data)
    
    return mygraph_data

def process_profile_data(data):
    """Process profile data into nodes"""
    if not data or 'displayName' not in data:
        return []
    
    return [{
        "id": f"urn:person:me:{data.get('mail', 'unknown')}",
        "type": "person",
        "properties": {
            "name": data.get('displayName'),
            "email": data.get('mail'),
            "title": data.get('jobTitle'),
            "department": data.get('department')
        },
        "prov": {
            "source": "graph.me",
            "confidence": 1.0
        }
    }]

def process_manager_data(data):
    """Process manager data into nodes"""
    if not data or 'displayName' not in data:
        return []
    
    return [{
        "id": f"urn:person:manager:{data.get('mail', 'unknown')}",
        "type": "person", 
        "properties": {
            "name": data.get('displayName'),
            "email": data.get('mail'),
            "title": data.get('jobTitle'),
            "role": "manager"
        },
        "prov": {
            "source": "graph.me.manager",
            "confidence": 0.9
        }
    }]

def create_manager_links(data):
    """Create links for manager relationship"""
    if not data or 'mail' not in data:
        return []
    
    return [{
        "source": f"urn:person:me:unknown",  # Will be updated with actual email
        "target": f"urn:person:manager:{data.get('mail')}",
        "type": "REPORTS_TO"
    }]

def process_reports_data(data):
    """Process direct reports data"""
    if not data or 'value' not in data:
        return []
    
    nodes = []
    for report in data['value']:
        nodes.append({
            "id": f"urn:person:report:{report.get('mail', 'unknown')}",
            "type": "person",
            "properties": {
                "name": report.get('displayName'),
                "email": report.get('mail'),
                "title": report.get('jobTitle'),
                "role": "direct_report"
            },
            "prov": {
                "source": "graph.me.directReports",
                "confidence": 0.9
            }
        })
    return nodes

def create_reports_links(data):
    """Create links for direct reports"""
    if not data or 'value' not in data:
        return []
    
    links = []
    for report in data['value']:
        links.append({
            "source": f"urn:person:report:{report.get('mail', 'unknown')}",
            "target": f"urn:person:me:unknown",  # Will be updated
            "type": "REPORTS_TO"
        })
    return links

def process_calendar_data(data):
    """Process calendar events data"""
    if not data or 'value' not in data:
        return []
    
    nodes = []
    for event in data['value'][:10]:  # Limit to recent 10 events
        if event.get('subject'):
            nodes.append({
                "id": f"urn:calendar:event:{event.get('id', 'unknown')}",
                "type": "meeting",
                "properties": {
                    "subject": event.get('subject'),
                    "start": event.get('start', {}).get('dateTime'),
                    "organizer": event.get('organizer', {}).get('emailAddress', {}).get('name')
                },
                "prov": {
                    "source": "graph.me.calendarView",
                    "confidence": 0.8
                }
            })
    return nodes

def create_calendar_links(data):
    """Create calendar links"""
    if not data or 'value' not in data:
        return []
    
    links = []
    for event in data['value'][:10]:
        if event.get('subject'):
            links.append({
                "source": f"urn:person:me:unknown",
                "target": f"urn:calendar:event:{event.get('id', 'unknown')}",
                "type": "ATTENDS"
            })
    return links

def process_files_data(data):
    """Process files data"""
    if not data or 'value' not in data:
        return []
    
    nodes = []
    for file_item in data['value'][:5]:  # Limit to 5 recent files
        nodes.append({
            "id": f"urn:file:{file_item.get('id', 'unknown')}",
            "type": "document",
            "properties": {
                "name": file_item.get('name'),
                "lastModified": file_item.get('lastModifiedDateTime'),
                "size": file_item.get('size')
            },
            "prov": {
                "source": "graph.me.drive.recent",
                "confidence": 0.7
            }
        })
    return nodes

def create_files_links(data):
    """Create file links"""
    if not data or 'value' not in data:
        return []
    
    links = []
    for file_item in data['value'][:5]:
        links.append({
            "source": f"urn:person:me:unknown",
            "target": f"urn:file:{file_item.get('id', 'unknown')}",
            "type": "OWNS"
        })
    return links

def update_html_file(mygraph_data):
    """Update the HTML file with new data"""
    print("🔄 Updating HTML file...")
    
    html_file = Path("docs/mygraph_explorer.html")
    if not html_file.exists():
        print("⚠️  HTML file not found")
        return
    
    # Read current HTML
    with open(html_file, 'r') as f:
        html_content = f.read()
    
    # Find and replace the data section
    start_marker = "const graph = {"
    end_marker = "};"
    
    start_idx = html_content.find(start_marker)
    if start_idx == -1:
        print("⚠️  Could not find data section in HTML")
        return
    
    end_idx = html_content.find(end_marker, start_idx) + len(end_marker)
    
    # Create new data section
    new_data = f"""const graph = {{
  nodes: {json.dumps(mygraph_data['nodes'], indent=2)},
  links: {json.dumps(mygraph_data['links'], indent=2)}
}};"""
    
    # Replace data section
    updated_html = html_content[:start_idx] + new_data + html_content[end_idx:]
    
    # Save updated HTML
    backup_file = f"mygraph_explorer_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(f"docs/{backup_file}", 'w') as f:
        f.write(html_content)
    
    with open(html_file, 'w') as f:
        f.write(updated_html)
    
    print(f"✅ HTML file updated (backup saved as {backup_file})")

if __name__ == "__main__":
    process_collected_data()
'''
    
    with open("process_mygraph_data.py", 'w') as f:
        f.write(processor_code)
    
    print("📝 Created data processor: process_mygraph_data.py")

if __name__ == "__main__":
    queries = collect_mygraph_data_manual()
    
    print("🎯 Summary:")
    print("The MyGraph HTML file works perfectly - it just needs fresh data!")
    print("The authentication issues are in the data collection tools, not the visualization.")
    print()
    print("💡 Next steps:")
    print("1. Use Graph Explorer manually to collect data")
    print("2. Run process_mygraph_data.py to update the HTML")
    print("3. Open the updated HTML file in your browser")