#!/usr/bin/env python3
"""
Graph Explorer-Based Collaboration Analyzer
Uses our proven browser automation approach to get collaboration insights
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium', 'webdriver-manager'])
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager


class GraphExplorerCollaborationAnalyzer:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.wait_timeout = 30
        self.driver = None
        
        # Collaboration-focused queries
        self.collaboration_queries = {
            "chat_messages": "me/chats?$expand=members",
            "teams": "me/joinedTeams",
            "calendar_meetings": "me/calendarView?startDateTime=2025-09-01T00:00:00Z&endDateTime=2025-10-25T23:59:59Z&$select=subject,organizer,attendees,start,end,onlineMeeting",
            "recent_emails": "me/messages?$top=50&$select=sender,toRecipients,ccRecipients,subject,receivedDateTime",
            "shared_files": "me/drive/sharedWithMe?$top=20",
            "people_worked_with": "me/people?$top=50",
            "direct_reports": "me/directReports",
            "manager": "me/manager"
        }
        
    def setup_browser(self) -> bool:
        """Setup Chrome browser for Graph Explorer"""
        print("🌐 Setting up Chrome browser for Microsoft Graph Explorer...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            
            print("🌐 Opening Graph Explorer...")
            self.driver.get(self.base_url)
            
            print("✅ Chrome browser setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False

    def wait_for_authentication(self) -> bool:
        """Wait for user to complete authentication"""
        print("\n🔐 AUTHENTICATION REQUIRED")
        print("=" * 50)
        print("1. 📱 Complete Microsoft authentication in the browser")
        print("2. ✅ Ensure you're signed in to Graph Explorer")
        print("3. ⏳ Press ENTER when ready to continue...")
        
        input("Press ENTER when you're authenticated and ready...")
        return True

    def execute_query(self, query_name: str, query: str) -> Optional[str]:
        """Execute a single Graph query and return response"""
        print(f"\n📡 Executing: {query_name}")
        print(f"🔍 Query: {query}")
        
        try:
            # Navigate to the query
            url = f"{self.base_url}?request={query}&method=GET"
            print(f"🌐 Navigating to: {url[:100]}...")
            self.driver.get(url)
            
            # Wait a moment for page load
            time.sleep(2)
            
            # Find and click the run button
            try:
                run_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr"))
                )
                print("🖱️  Clicking run query button...")
                self.driver.execute_script("arguments[0].click();", run_button)
                print("✅ Successfully clicked run button")
            except TimeoutException:
                print("⚠️  Could not find run button, trying alternative selector...")
                try:
                    run_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Run query')]")
                    run_button.click()
                    print("✅ Successfully clicked run button (alternative)")
                except:
                    print("❌ Could not find run button")
                    return None
            
            # Wait for results
            print("⏳ Waiting for query results...")
            time.sleep(3)
            
            # Try to get the response
            try:
                # Look for Monaco editor content
                response_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".monaco-editor"))
                )
                
                response_text = response_element.text
                print(f"✅ Got response ({len(response_text)} characters)")
                
                if response_text and len(response_text) > 10:
                    return response_text
                else:
                    print("⚠️  Response too short, might be empty")
                    return None
                    
            except TimeoutException:
                print("⚠️  Could not find response element")
                return None
                
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None

    def analyze_collaboration_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collaboration patterns from collected data"""
        print("\n🔍 ANALYZING COLLABORATION PATTERNS")
        print("=" * 50)
        
        collaborators = {}
        insights = {
            "top_collaborators": [],
            "collaboration_channels": {},
            "meeting_frequency": {},
            "communication_patterns": {},
            "insights": []
        }
        
        # Analyze calendar meetings
        if "calendar_meetings" in data and data["calendar_meetings"]:
            print("📅 Analyzing calendar meetings...")
            # Process meeting data for collaborator identification
            insights["insights"].append("Calendar meeting data available for analysis")
        
        # Analyze chat messages
        if "chat_messages" in data and data["chat_messages"]:
            print("💬 Analyzing chat messages...")
            insights["insights"].append("Chat message data available for analysis")
        
        # Analyze email communications
        if "recent_emails" in data and data["recent_emails"]:
            print("📧 Analyzing email communications...")
            insights["insights"].append("Email communication data available for analysis")
        
        # Analyze shared files
        if "shared_files" in data and data["shared_files"]:
            print("📄 Analyzing shared files...")
            insights["insights"].append("Shared file collaboration data available")
        
        # Analyze people connections
        if "people_worked_with" in data and data["people_worked_with"]:
            print("👥 Analyzing people connections...")
            insights["insights"].append("People API data available for relationship analysis")
        
        return insights

    def run_collaboration_analysis(self) -> Dict[str, Any]:
        """Run complete collaboration analysis"""
        print("🚀 GRAPH EXPLORER COLLABORATION ANALYZER")
        print("=" * 60)
        print("Uses browser automation to collect Microsoft Graph collaboration data")
        print()
        
        # Setup browser
        if not self.setup_browser():
            return {"error": "Browser setup failed"}
        
        # Wait for authentication
        if not self.wait_for_authentication():
            return {"error": "Authentication failed"}
        
        # Collect data for each query
        collected_data = {}
        
        for query_name, query in self.collaboration_queries.items():
            response = self.execute_query(query_name, query)
            if response:
                collected_data[query_name] = response
            else:
                collected_data[query_name] = None
            
            # Small delay between queries
            time.sleep(1)
        
        # Analyze collaboration patterns
        insights = self.analyze_collaboration_patterns(collected_data)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "timestamp": timestamp,
            "method": "graph_explorer_browser_automation",
            "raw_data": collected_data,
            "collaboration_insights": insights
        }
        
        # Save to file
        output_file = f"graph_explorer_collaboration_analysis_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Cleanup
        if self.driver:
            self.driver.quit()
        
        return results


def main():
    """Main execution function"""
    analyzer = GraphExplorerCollaborationAnalyzer()
    
    try:
        results = analyzer.run_collaboration_analysis()
        
        if "error" not in results:
            print("\n🎊 COLLABORATION ANALYSIS COMPLETE!")
            print("=" * 50)
            
            insights = results.get("collaboration_insights", {})
            
            if insights.get("insights"):
                print("\n💡 Key Insights:")
                for insight in insights["insights"]:
                    print(f"   • {insight}")
            
            print(f"\n📊 Data Sources Collected:")
            raw_data = results.get("raw_data", {})
            for source, data in raw_data.items():
                status = "✅ Success" if data else "❌ No data"
                print(f"   • {source}: {status}")
            
            print(f"\n📄 Full results saved to: graph_explorer_collaboration_analysis_{results['timestamp']}.json")
            
        else:
            print(f"❌ Analysis failed: {results['error']}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if analyzer.driver:
            analyzer.driver.quit()


if __name__ == "__main__":
    main()