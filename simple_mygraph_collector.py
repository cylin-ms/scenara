#!/usr/bin/env python3
"""
Simple MyGraph Data Collector
Manual approach - you copy/paste, automation processes
"""

import json
import time
from datetime import datetime

def simple_collector():
    """Simple manual data collection"""
    print("📋 SIMPLE MYGRAPH DATA COLLECTOR")
    print("Copy/paste approach - much faster!")
    print("=" * 40)
    
    print("\n🎯 Instructions:")
    print("1. Open Graph Explorer: https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("2. Sign in")
    print("3. For each query below:")
    print("   • Copy the query into Graph Explorer")
    print("   • Click 'Run query'")
    print("   • Copy the JSON response")
    print("   • Paste it here")
    print()
    
    queries = [
        ("me", "Your profile data", "profile"),
        ("me/calendarView?startDateTime=2025-10-20T00:00:00Z&endDateTime=2025-11-20T00:00:00Z", "Calendar events (30 days)", "calendar"),
        ("me/manager", "Your manager", "manager"),
        ("me/directReports", "Your direct reports", "reports"),
        ("me/memberOf", "Groups/teams you're in", "groups")
    ]
    
    results = {}
    
    for query, description, key in queries:
        print(f"\n📡 {description}")
        print(f"🔗 Query: {query}")
        print("   1. Copy this query into Graph Explorer")
        print("   2. Run the query")
        print("   3. Copy the entire JSON response")
        print("   4. Paste it below (press Enter twice when done):")
        
        # Collect multi-line input
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "" and lines:
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\n⏹️  Skipped")
                break
        
        if lines:
            json_text = '\n'.join(lines)
            try:
                # Try to parse the JSON
                data = json.loads(json_text)
                results[key] = data
                print(f"✅ {description} collected!")
                
                # Show quick summary
                if isinstance(data, dict):
                    if 'displayName' in data:
                        print(f"   👤 Name: {data['displayName']}")
                    elif 'value' in data and isinstance(data['value'], list):
                        print(f"   📊 Items: {len(data['value'])}")
                    else:
                        print(f"   📄 Data: {len(str(data))} characters")
                
            except json.JSONDecodeError as e:
                print(f"⚠️  Invalid JSON: {e}")
                print("💡 Make sure you copied the complete JSON response")
        else:
            print("⏭️  Skipped")
    
    # Save results
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simple_mygraph_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n🎉 SUCCESS!")
        print(f"💾 Saved to: {filename}")
        print(f"📊 Collected: {list(results.keys())}")
        print(f"⏱️  Total time: ~5 minutes (much faster!)")
        
        return filename
    else:
        print("\n❌ No data collected")
        return None

def process_simple_data(filename):
    """Process the collected data into MyGraph format"""
    if not filename:
        return False
    
    print(f"\n🔄 Processing {filename} into MyGraph format...")
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Convert to MyGraph nodes and links format
        nodes = []
        links = []
        
        # Process profile
        if 'profile' in data:
            profile = data['profile']
            user_node = {
                "id": f"user:{profile.get('id', 'me')}",
                "type": "Person",
                "properties": {
                    "displayName": profile.get('displayName'),
                    "jobTitle": profile.get('jobTitle'),
                    "mail": profile.get('mail'),
                    "businessPhones": profile.get('businessPhones', [])
                }
            }
            nodes.append(user_node)
        
        # Process calendar events
        if 'calendar' in data and 'value' in data['calendar']:
            for event in data['calendar']['value']:
                event_node = {
                    "id": f"event:{event.get('id')}",
                    "type": "Meeting",
                    "properties": {
                        "subject": event.get('subject'),
                        "start": event.get('start', {}).get('dateTime'),
                        "end": event.get('end', {}).get('dateTime')
                    }
                }
                nodes.append(event_node)
        
        # Process manager
        if 'manager' in data:
            manager = data['manager']
            manager_node = {
                "id": f"user:{manager.get('id')}",
                "type": "Person",
                "properties": {
                    "displayName": manager.get('displayName'),
                    "jobTitle": manager.get('jobTitle')
                }
            }
            nodes.append(manager_node)
        
        # Create a simple MyGraph structure
        mygraph_data = {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "collected_at": datetime.now().isoformat(),
                "method": "simple_collector",
                "node_count": len(nodes),
                "link_count": len(links)
            }
        }
        
        # Save MyGraph format
        mygraph_filename = filename.replace('.json', '_mygraph.json')
        with open(mygraph_filename, 'w') as f:
            json.dump(mygraph_data, f, indent=2)
        
        print(f"✅ MyGraph data saved to: {mygraph_filename}")
        print(f"📊 {len(nodes)} nodes, {len(links)} links")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

def main():
    """Main function"""
    print("⚡ Choose collection method:")
    print("1. 📋 Simple copy/paste (recommended - fast & reliable)")
    print("2. 🤖 Try automated extraction debug")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        filename = simple_collector()
        if filename:
            process_simple_data(filename)
    elif choice == "2":
        from debug_extraction import debug_extraction
        debug_extraction()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()