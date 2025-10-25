#!/usr/bin/env python3
"""
Simple Manual Auth Graph Explorer Collaboration Extractor
User authenticates manually, then tool executes queries automatically
Targets the "Response preview" tab in the lower right panel
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

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


class SimpleManualAuthExtractor:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.driver = None
        
        # Key collaboration queries based on Graph Explorer query types
        self.collaboration_queries = {
            "people_api": {
                "query": "me/people?$top=50",
                "description": "People You Work With Most (Microsoft ML Rankings)"
            },
            "calendar_meetings": {
                "query": "me/calendarView?startDateTime=2025-09-01T00:00:00Z&endDateTime=2025-10-25T23:59:59Z&$select=subject,organizer,attendees,start,end,onlineMeeting",
                "description": "Recent Calendar Meetings with Attendees"
            },
            "recent_emails": {
                "query": "me/messages?$top=50&$select=sender,toRecipients,ccRecipients,subject,receivedDateTime,bodyPreview",
                "description": "Recent Email Communications"
            },
            "teams_chats": {
                "query": "me/chats?$expand=members&$top=20",
                "description": "Teams Chat Conversations"
            },
            "shared_files": {
                "query": "me/drive/sharedWithMe?$top=20&$select=name,createdBy,lastModifiedBy,sharedBy",
                "description": "Files Shared With You"
            },
            "teams_joined": {
                "query": "me/joinedTeams?$select=displayName,description,memberSettings",
                "description": "Teams You're Member Of"
            }
        }
        
    def setup_browser(self) -> bool:
        """Setup browser for manual authentication"""
        print("🌐 Setting up Chrome browser...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Keep browser fully visible for manual auth
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            
            print("🌐 Opening Microsoft Graph Explorer...")
            self.driver.get(self.base_url)
            
            print("✅ Browser ready - Graph Explorer loaded")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False

    def wait_for_manual_authentication(self) -> bool:
        """Wait for user to complete manual authentication"""
        print("\n🔐 MANUAL AUTHENTICATION")
        print("=" * 50)
        print("1. 📱 Please sign in to Microsoft Graph Explorer manually")
        print("2. ✅ Complete any authentication steps in the browser")
        print("3. 🔍 Make sure you can see the Graph Explorer interface with:")
        print("   • Query types panel on the lower left")
        print("   • Response preview tab on the lower right")
        print("4. ⏳ When ready, the tool will automatically proceed with queries")
        print()
        
        # Give user time to authenticate
        print("⏳ Waiting 30 seconds for manual authentication...")
        for i in range(30, 0, -1):
            print(f"   Starting automatic queries in {i} seconds... (Press Ctrl+C to cancel)", end='\r')
            time.sleep(1)
        
        print("\n✅ Proceeding with automatic query execution...")
        return True

    def execute_query_and_extract_response(self, query_name: str, query_info: Dict[str, str]) -> Optional[str]:
        """Execute query and extract from Response preview tab"""
        print(f"\n📡 Executing: {query_info['description']}")
        print(f"🔍 Query: {query_info['query']}")
        
        try:
            # Navigate to the query
            url = f"{self.base_url}?request={query_info['query']}&method=GET"
            print(f"🌐 Navigating to query...")
            self.driver.get(url)
            time.sleep(3)
            
            # Find and click the Run query button
            run_button_selectors = [
                "span.___1ej4kmx.f22iagw.f122n59.fkln5zr",  # Known working selector
                "button[aria-label*='Run']",
                "[data-testid='run-query']",
                "button:contains('Run query')",
                ".run-query-button"
            ]
            
            run_clicked = False
            for selector in run_button_selectors:
                try:
                    if "contains" in selector:
                        xpath = "//button[contains(text(), 'Run') or contains(text(), 'Run query')]"
                        run_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                    else:
                        run_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    print("🖱️  Clicking 'Run query' button...")
                    self.driver.execute_script("arguments[0].click();", run_button)
                    print("✅ Successfully clicked run button")
                    run_clicked = True
                    break
                    
                except TimeoutException:
                    continue
            
            if not run_clicked:
                print("❌ Could not find 'Run query' button")
                return None
            
            # Wait for query execution
            print("⏳ Waiting for query execution...")
            time.sleep(5)
            
            # Try to extract from "Response preview" tab in lower right panel
            print("🔍 Looking for Response preview tab...")
            
            # Look for response in multiple possible locations
            response_selectors = [
                # Response preview tab content
                "[data-testid='response-preview']",
                ".response-preview",
                # Monaco editor (where JSON appears)
                ".monaco-editor .view-lines",
                ".monaco-editor",
                # JSON response areas
                ".json-response",
                ".response-content",
                # Code editor content
                ".code-editor .view-lines",
                ".code-editor"
            ]
            
            for selector in response_selectors:
                try:
                    print(f"   Trying selector: {selector}")
                    response_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in response_elements:
                        response_text = element.text
                        if response_text and len(response_text.strip()) > 20:
                            print(f"✅ Found response content ({len(response_text)} characters)")
                            print(f"   Preview: {response_text[:100]}...")
                            return response_text
                    
                except Exception as e:
                    continue
            
            # Fallback: Look for any JSON-like content in page source
            print("🔄 Fallback: Searching page source for JSON...")
            page_source = self.driver.page_source
            
            # Look for JSON patterns
            import re
            json_patterns = [
                r'\{"@odata\.context"[^}]+\}',
                r'\{"value":\[[^\]]+\]\}',
                r'\{[^{}]*"displayName"[^{}]*\}',
                r'\{[^{}]*"emailAddress"[^{}]*\}'
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, page_source)
                if matches:
                    response_text = matches[0]
                    print(f"✅ Found JSON pattern in page source ({len(response_text)} characters)")
                    return response_text
            
            print("⚠️  No response content found")
            return None
            
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None

    def parse_and_analyze_responses(self, collected_responses: Dict[str, str]) -> Dict[str, Any]:
        """Parse responses and extract collaboration insights"""
        print("\n🔍 ANALYZING COLLABORATION DATA")
        print("=" * 50)
        
        analysis = {
            "collaboration_insights": [],
            "people_api_ranking": [],
            "meeting_collaborators": {},
            "email_collaborators": {},
            "teams_info": [],
            "summary": {
                "responses_collected": len([r for r in collected_responses.values() if r]),
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
        
        # Parse People API response (Microsoft's ML rankings)
        if collected_responses.get("people_api"):
            response_text = collected_responses["people_api"]
            try:
                # Try to parse as JSON
                import json
                people_data = json.loads(response_text)
                
                if isinstance(people_data, dict) and "value" in people_data:
                    people = people_data["value"]
                    analysis["summary"]["people_api_count"] = len(people)
                    
                    for i, person in enumerate(people[:10]):  # Top 10
                        if isinstance(person, dict):
                            name = person.get("displayName", "Unknown")
                            email = ""
                            if "scoredEmailAddresses" in person and person["scoredEmailAddresses"]:
                                email = person["scoredEmailAddresses"][0].get("address", "")
                            
                            analysis["people_api_ranking"].append({
                                "rank": i + 1,
                                "name": name,
                                "email": email,
                                "type": person.get("personType", {}).get("subclass", "Unknown")
                            })
                    
                    analysis["collaboration_insights"].append(f"Microsoft People API: Ranked {len(people)} collaborators using ML")
                
            except json.JSONDecodeError:
                analysis["collaboration_insights"].append("People API: Response received but could not parse JSON")
        
        # Parse calendar meetings
        if collected_responses.get("calendar_meetings"):
            response_text = collected_responses["calendar_meetings"]
            try:
                meetings_data = json.loads(response_text)
                
                if isinstance(meetings_data, dict) and "value" in meetings_data:
                    meetings = meetings_data["value"]
                    analysis["summary"]["meeting_count"] = len(meetings)
                    
                    # Extract meeting collaborators
                    collaborators = {}
                    for meeting in meetings:
                        if isinstance(meeting, dict):
                            # Organizer
                            organizer = meeting.get("organizer", {})
                            if isinstance(organizer, dict) and "emailAddress" in organizer:
                                email = organizer["emailAddress"].get("address", "")
                                if email:
                                    collaborators[email] = collaborators.get(email, 0) + 1
                            
                            # Attendees
                            attendees = meeting.get("attendees", [])
                            for attendee in attendees:
                                if isinstance(attendee, dict) and "emailAddress" in attendee:
                                    email = attendee["emailAddress"].get("address", "")
                                    if email:
                                        collaborators[email] = collaborators.get(email, 0) + 1
                    
                    # Sort by frequency
                    sorted_collaborators = sorted(collaborators.items(), key=lambda x: x[1], reverse=True)
                    analysis["meeting_collaborators"] = dict(sorted_collaborators[:15])
                    analysis["collaboration_insights"].append(f"Calendar: {len(meetings)} meetings, {len(collaborators)} unique collaborators")
                
            except json.JSONDecodeError:
                analysis["collaboration_insights"].append("Calendar: Response received but could not parse JSON")
        
        return analysis

    def run_simple_extraction(self) -> Dict[str, Any]:
        """Run complete simple manual auth extraction"""
        print("🚀 SIMPLE MANUAL AUTH GRAPH COLLABORATION EXTRACTOR")
        print("=" * 70)
        print("User authenticates manually, then automated query execution begins")
        print("Targets 'Response preview' tab in Graph Explorer interface")
        print()
        
        # Setup browser
        if not self.setup_browser():
            return {"error": "Browser setup failed"}
        
        # Wait for manual authentication
        if not self.wait_for_manual_authentication():
            if self.driver:
                self.driver.quit()
            return {"error": "Authentication process cancelled"}
        
        # Execute queries and collect responses
        collected_responses = {}
        success_count = 0
        
        for query_name, query_info in self.collaboration_queries.items():
            response = self.execute_query_and_extract_response(query_name, query_info)
            if response:
                collected_responses[query_name] = response
                success_count += 1
            else:
                collected_responses[query_name] = None
            
            # Brief delay between queries
            time.sleep(2)
        
        print(f"\n📊 QUERY EXECUTION SUMMARY:")
        print(f"   ✅ Successful responses: {success_count}/{len(self.collaboration_queries)}")
        
        # Analyze collected data
        analysis = self.parse_and_analyze_responses(collected_responses)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_results = {
            "timestamp": timestamp,
            "method": "simple_manual_auth_extraction",
            "authentication": "manual_user_authentication",
            "target_interface": "graph_explorer_response_preview_tab",
            "queries_executed": len(self.collaboration_queries),
            "successful_responses": success_count,
            "raw_responses": collected_responses,
            "collaboration_analysis": analysis
        }
        
        # Save to file
        output_file = f"simple_manual_collaboration_extraction_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(final_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Cleanup
        if self.driver:
            print("🧹 Closing browser...")
            self.driver.quit()
        
        return final_results


def main():
    """Main execution function"""
    extractor = SimpleManualAuthExtractor()
    
    try:
        results = extractor.run_simple_extraction()
        
        if "error" not in results:
            print("\n🎊 SIMPLE MANUAL AUTH EXTRACTION COMPLETE!")
            print("=" * 60)
            
            print(f"\n📊 EXECUTION SUMMARY:")
            print(f"   • Method: {results.get('method', 'Unknown')}")
            print(f"   • Authentication: {results.get('authentication', 'Unknown')}")
            print(f"   • Success Rate: {results.get('successful_responses', 0)}/{results.get('queries_executed', 0)}")
            
            # Show collaboration insights
            analysis = results.get("collaboration_analysis", {})
            insights = analysis.get("collaboration_insights", [])
            
            if insights:
                print(f"\n💡 COLLABORATION INSIGHTS:")
                for insight in insights:
                    print(f"   • {insight}")
            
            # Show Microsoft People API rankings (the key to finding Haidong Zhang!)
            people_ranking = analysis.get("people_api_ranking", [])
            if people_ranking:
                print(f"\n👥 MICROSOFT PEOPLE API TOP COLLABORATORS:")
                for person in people_ranking[:10]:
                    print(f"   {person['rank']}. {person['name']} ({person.get('email', 'No email')}) - {person.get('type', 'Unknown')}")
            
            # Show meeting collaborators
            meeting_collaborators = analysis.get("meeting_collaborators", {})
            if meeting_collaborators:
                print(f"\n📅 TOP MEETING COLLABORATORS:")
                for email, count in list(meeting_collaborators.items())[:5]:
                    print(f"   • {email}: {count} meetings")
            
            print(f"\n📄 Complete results: simple_manual_collaboration_extraction_{results['timestamp']}.json")
            
        else:
            print(f"❌ Extraction failed: {results['error']}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Extraction interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if extractor.driver:
            extractor.driver.quit()


if __name__ == "__main__":
    main()