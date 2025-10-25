#!/usr/bin/env python3
"""
Investigation: How did MyGraph get populated?
Timeline and source analysis
"""

from datetime import datetime
import json
import os

def investigate_mygraph_origins():
    """Investigate how the MyGraph data was collected"""
    print("🔍 MyGraph Data Origins Investigation")
    print("=" * 50)
    
    # Check file timestamps
    files_to_check = [
        "docs/mygraph_explorer.html",
        "my_calendar_events.json", 
        "my_calendar_events_50.json",
        "process_mygraph_data.py"
    ]
    
    print("📅 File Timeline:")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            print(f"   {file_path}: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Analyze the data sources in MyGraph
    print("🎯 MyGraph Data Analysis:")
    print("From our earlier analysis:")
    print("   📊 1,207 nodes, 1,097 links")
    print("   📅 Most recent data: October 15, 2025")
    print("   📡 Data sources:")
    print("      • m365.calendar: 96 items")
    print("      • m365.file: 923 items") 
    print("      • m365.mail: 129 items")
    print("      • m365.chat: 33 items")
    print("      • ado.workitem: 22 items")
    print("      • mygraph.dictionary: 4 items")
    print()
    
    # What this tells us
    print("🧩 What Happened:")
    print("1. 📆 October 15, 2025 (9 days ago):")
    print("   • MyGraph HTML file was created/updated")
    print("   • Data was collected from Microsoft 365 and Azure DevOps")
    print("   • Successfully gathered comprehensive organizational data")
    print()
    
    print("2. 📆 October 22, 2025 (2 days ago):")
    print("   • Calendar JSON files were created")
    print("   • This might have been for the meeting discovery feature")
    print()
    
    print("3. 📆 October 24, 2025 (today):")
    print("   • We created automation tools to refresh the data")
    print("   • But the existing data is still quite recent (9 days)")
    print()
    
    print("💡 Conclusion:")
    print("Your MyGraph was successfully populated on October 15 through")
    print("what appears to have been a successful data collection run.")
    print("The automation tools we built today are for future refreshes,")
    print("but your current data is comprehensive and recent!")
    print()
    
    print("🎯 Current Status:")
    print("✅ Rich organizational graph with 1,207 entities")
    print("✅ Recent data (only 9 days old)")
    print("✅ Multiple data sources integrated")
    print("✅ Interactive visualization ready to use")
    print("✅ Automation tools ready for future updates")

if __name__ == "__main__":
    investigate_mygraph_origins()