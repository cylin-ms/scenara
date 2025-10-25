#!/usr/bin/env python3
"""
MyGraph Automation Fallback System
Alternative automation approaches when the main pipeline encounters issues
"""

import json
import os
import time
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
import urllib.parse

class MyGraphFallbackSystem:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.queries = self.get_predefined_queries()
        
    def get_predefined_queries(self) -> List[Dict[str, str]]:
        """Get all predefined Graph queries for data collection"""
        return [
            {
                "name": "User Profile",
                "query": "me",
                "description": "Basic user information",
                "file": "profile_data.json"
            },
            {
                "name": "Manager Info",
                "query": "me/manager",
                "description": "Reporting manager details",
                "file": "manager_data.json"
            },
            {
                "name": "Direct Reports",
                "query": "me/directReports",
                "description": "People reporting to you",
                "file": "reports_data.json"
            },
            {
                "name": "Calendar Events",
                "query": f"me/calendarView?startDateTime={datetime.now().isoformat()}Z&endDateTime={(datetime.now() + timedelta(days=30)).isoformat()}Z",
                "description": "Upcoming calendar events",
                "file": "calendar_data.json"
            },
            {
                "name": "Recent Files",
                "query": "me/drive/recent",
                "description": "Recently accessed files",
                "file": "files_data.json"
            },
            {
                "name": "Group Memberships",
                "query": "me/memberOf",
                "description": "Groups and teams you belong to",
                "file": "groups_data.json"
            },
            {
                "name": "Contacts",
                "query": "me/contacts?$top=20",
                "description": "Your top contacts",
                "file": "contacts_data.json"
            }
        ]

    def method1_guided_manual_collection(self):
        """Method 1: Guided manual data collection"""
        print("📋 Method 1: Guided Manual Collection")
        print("=" * 45)
        print("This method guides you through manual data collection with pre-built URLs")
        print()
        
        collected_files = []
        
        for i, query_info in enumerate(self.queries, 1):
            print(f"{i}. 📊 {query_info['name']}")
            print(f"   📝 {query_info['description']}")
            
            # Create Graph Explorer URL
            encoded_query = urllib.parse.quote(query_info['query'])
            graph_url = f"{self.base_url}?request={encoded_query}&method=GET&version=v1.0"
            
            print(f"   🔗 URL: {graph_url}")
            print()
            print("   📋 Steps:")
            print("   1. Click the URL above (or copy to browser)")
            print("   2. Sign in to Microsoft Graph Explorer")
            print("   3. Click 'Run query' button")
            print("   4. Copy the JSON response")
            print(f"   5. Save as: {query_info['file']}")
            print()
            
            # Ask if user wants to open the URL
            open_browser = input(f"   🌐 Open browser for {query_info['name']}? (y/n): ").lower().strip()
            if open_browser == 'y':
                webbrowser.open(graph_url)
                print("   ✅ Browser opened")
            
            # Check if file was created
            while True:
                file_exists = input(f"   💾 Saved {query_info['file']}? (y/n/skip): ").lower().strip()
                if file_exists == 'y':
                    if Path(query_info['file']).exists():
                        collected_files.append(query_info['file'])
                        print("   ✅ File confirmed")
                        break
                    else:
                        print("   ⚠️  File not found, please check the filename")
                elif file_exists == 'skip':
                    print("   ⏭️  Skipped")
                    break
                elif file_exists == 'n':
                    continue
            
            print("-" * 50)
        
        print(f"\n📊 Collection Summary: {len(collected_files)} files collected")
        return collected_files

    def method2_clipboard_based_collection(self):
        """Method 2: Clipboard-based collection with paste prompts"""
        print("📋 Method 2: Clipboard-Based Collection")
        print("=" * 42)
        print("This method uses clipboard for easy data transfer")
        print()
        
        # Check if pyperclip is available
        try:
            import pyperclip
            clipboard_available = True
        except ImportError:
            print("📦 Installing clipboard support...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyperclip'])
            import pyperclip
            clipboard_available = True
        
        collected_data = {}
        
        for i, query_info in enumerate(self.queries, 1):
            print(f"\n{i}. 📊 {query_info['name']}")
            print(f"   📝 {query_info['description']}")
            print(f"   🔍 Query: {query_info['query']}")
            
            # Copy query to clipboard
            if clipboard_available:
                pyperclip.copy(query_info['query'])
                print("   📋 Query copied to clipboard!")
            
            print("\n   📋 Steps:")
            print("   1. Go to Graph Explorer (browser will open)")
            print("   2. Paste the query in the request field")
            print("   3. Click 'Run query'")
            print("   4. Copy the entire JSON response")
            print("   5. Come back here and paste when prompted")
            
            # Open Graph Explorer
            proceed = input("\n   🌐 Open Graph Explorer? (y/n): ").lower().strip()
            if proceed == 'y':
                webbrowser.open(self.base_url)
            
            # Wait for user to get the data
            input("\n   ⏳ Press Enter when you have copied the JSON response...")
            
            # Get data from clipboard
            try:
                if clipboard_available:
                    json_data = pyperclip.paste()
                    # Try to parse JSON to validate
                    parsed_data = json.loads(json_data)
                    collected_data[query_info['name'].lower().replace(' ', '_')] = parsed_data
                    
                    # Save to file
                    with open(query_info['file'], 'w') as f:
                        json.dump(parsed_data, f, indent=2)
                    
                    print(f"   ✅ Data saved to {query_info['file']}")
                else:
                    print("   ⚠️  Clipboard not available, skipping...")
                    
            except json.JSONDecodeError:
                print("   ❌ Invalid JSON in clipboard, skipping...")
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
        
        return collected_data

    def method3_batch_url_generation(self):
        """Method 3: Generate batch of URLs for efficient collection"""
        print("📋 Method 3: Batch URL Generation")
        print("=" * 38)
        
        print("🔗 Generated Graph Explorer URLs for batch collection:")
        print()
        
        urls = []
        for i, query_info in enumerate(self.queries, 1):
            encoded_query = urllib.parse.quote(query_info['query'])
            graph_url = f"{self.base_url}?request={encoded_query}&method=GET&version=v1.0"
            urls.append(graph_url)
            
            print(f"{i}. {query_info['name']}")
            print(f"   File: {query_info['file']}")
            print(f"   URL: {graph_url}")
            print()
        
        # Save URLs to file
        urls_file = f"mygraph_urls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(urls_file, 'w') as f:
            f.write("MyGraph Data Collection URLs\n")
            f.write("=" * 35 + "\n\n")
            for i, (query_info, url) in enumerate(zip(self.queries, urls), 1):
                f.write(f"{i}. {query_info['name']}\n")
                f.write(f"   File: {query_info['file']}\n")
                f.write(f"   URL: {url}\n\n")
        
        print(f"💾 URLs saved to: {urls_file}")
        print("\n📋 Batch Collection Instructions:")
        print("1. Open each URL in a browser tab")
        print("2. Run queries and save responses")
        print("3. Use the file names shown above")
        print("4. Run process_mygraph_data.py when done")
        
        return urls_file

    def method4_auto_processor(self):
        """Method 4: Process any existing data files automatically"""
        print("📋 Method 4: Auto-Process Existing Data")
        print("=" * 40)
        
        # Look for any existing data files
        potential_files = [
            "profile_data.json", "manager_data.json", "reports_data.json",
            "calendar_data.json", "files_data.json", "groups_data.json",
            "contacts_data.json", "my_calendar_events.json", "my_calendar_events_50.json"
        ]
        
        found_files = []
        for file_name in potential_files:
            if Path(file_name).exists():
                found_files.append(file_name)
        
        if not found_files:
            print("❌ No data files found in current directory")
            print("💡 Use one of the other methods to collect data first")
            return False
        
        print(f"📂 Found {len(found_files)} data files:")
        for file_name in found_files:
            file_size = Path(file_name).stat().st_size
            print(f"   ✅ {file_name} ({file_size:,} bytes)")
        
        # Process the data
        try:
            nodes = []
            links = []
            
            # Create user node from any available profile data
            user_id = "urn:person:me:unknown"
            
            for file_name in found_files:
                try:
                    with open(file_name, 'r') as f:
                        data = json.load(f)
                    
                    if "profile" in file_name or file_name == "my_profile_data.json":
                        if 'displayName' in data:
                            user_id = f"urn:person:me:{data.get('mail', 'unknown')}"
                            nodes.append({
                                "id": user_id,
                                "type": "person",
                                "properties": {
                                    "name": data.get('displayName'),
                                    "email": data.get('mail'),
                                    "title": data.get('jobTitle')
                                },
                                "prov": {"source": file_name, "confidence": 1.0}
                            })
                    
                    elif "calendar" in file_name:
                        events = data.get('value', []) if 'value' in data else [data]
                        for event in events[:10]:  # Limit to 10 events
                            if event.get('subject'):
                                event_id = f"urn:calendar:event:{event.get('id', 'unknown')}"
                                nodes.append({
                                    "id": event_id,
                                    "type": "meeting",
                                    "properties": {
                                        "subject": event.get('subject'),
                                        "start": event.get('start', {}).get('dateTime')
                                    },
                                    "prov": {"source": file_name, "confidence": 0.8}
                                })
                                links.append({
                                    "source": user_id,
                                    "target": event_id,
                                    "type": "ATTENDS"
                                })
                    
                    print(f"   ✅ Processed {file_name}")
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing {file_name}: {e}")
            
            # Create MyGraph data structure
            mygraph_data = {
                "nodes": nodes,
                "links": links,
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "source": "auto_processor_existing_files",
                    "processed_files": found_files,
                    "total_nodes": len(nodes),
                    "total_links": len(links)
                }
            }
            
            # Save processed data
            output_file = f"mygraph_auto_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(mygraph_data, f, indent=2)
            
            print(f"\n📊 Processing Results:")
            print(f"   📦 Nodes: {len(nodes)}")
            print(f"   🔗 Links: {len(links)}")
            print(f"   💾 Saved: {output_file}")
            
            # Try to update HTML file
            self.update_html_file(mygraph_data)
            
            return True
            
        except Exception as e:
            print(f"❌ Auto-processing failed: {e}")
            return False

    def update_html_file(self, mygraph_data: Dict[str, Any]) -> bool:
        """Update the MyGraph HTML file with new data"""
        html_file = Path("docs/mygraph_explorer.html")
        if not html_file.exists():
            print("⚠️  MyGraph HTML file not found")
            return False
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Find and replace data section
            start_marker = "const graph = {"
            start_idx = html_content.find(start_marker)
            if start_idx == -1:
                return False
            
            # Find end of graph object
            brace_count = 0
            end_idx = start_idx + len(start_marker) - 1
            for i, char in enumerate(html_content[start_idx:], start_idx):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            # Create new data section
            new_data = f"""const graph = {{
  nodes: {json.dumps(mygraph_data['nodes'], indent=2)},
  links: {json.dumps(mygraph_data['links'], indent=2)}
}};"""
            
            # Create backup and update
            backup_file = f"docs/mygraph_explorer_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated_html = html_content[:start_idx] + new_data + html_content[end_idx:]
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"✅ MyGraph HTML updated (backup: {backup_file})")
            return True
            
        except Exception as e:
            print(f"⚠️  HTML update failed: {e}")
            return False

def main():
    print("🔧 MyGraph Automation Fallback System")
    print("=" * 45)
    print("When the main automation doesn't work, try these alternatives:")
    print()
    
    fallback = MyGraphFallbackSystem()
    
    while True:
        print("\n🎯 Choose your fallback method:")
        print("1. 📋 Guided Manual Collection (step-by-step)")
        print("2. 📋 Clipboard-Based Collection (copy/paste)")
        print("3. 🔗 Batch URL Generation (efficient)")
        print("4. 🤖 Auto-Process Existing Data")
        print("5. 📊 View Current MyGraph")
        print("6. ❌ Exit")
        print()
        
        choice = input("👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            fallback.method1_guided_manual_collection()
        elif choice == "2":
            fallback.method2_clipboard_based_collection()
        elif choice == "3":
            fallback.method3_batch_url_generation()
        elif choice == "4":
            fallback.method4_auto_processor()
        elif choice == "5":
            html_file = Path("docs/mygraph_explorer.html")
            if html_file.exists():
                webbrowser.open(f"file://{html_file.absolute()}")
                print("🌐 MyGraph opened in browser")
            else:
                print("❌ MyGraph HTML file not found")
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()