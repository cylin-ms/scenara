#!/usr/bin/env python3
"""
Hybrid Auto-Trigger Graph Collaboration Extractor
Combines working authentication trigger with proven extraction method
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

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


class HybridAutoTriggerExtractor:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.wait_timeout = 30
        self.driver = None
        
        # Focused collaboration queries
        self.collaboration_queries = {
            "people_api": {
                "query": "me/people?$top=50",
                "description": "People You Work With Most"
            },
            "calendar_meetings": {
                "query": "me/calendarView?startDateTime=2025-09-01T00:00:00Z&endDateTime=2025-10-25T23:59:59Z&$select=subject,organizer,attendees,start,end",
                "description": "Recent Calendar Meetings"
            },
            "recent_emails": {
                "query": "me/messages?$top=50&$select=sender,toRecipients,ccRecipients,subject,receivedDateTime",
                "description": "Recent Email Communications"
            },
            "teams_chats": {
                "query": "me/chats?$expand=members&$top=20",
                "description": "Teams Chat Conversations"
            }
        }
        
    def setup_browser_and_trigger_auth(self) -> bool:
        """Setup browser and automatically trigger authentication"""
        print("🌐 Setting up Chrome browser with auto-authentication...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            
            print("🌐 Opening Graph Explorer...")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            print("🔑 Triggering authentication with protected resource...")
            # Navigate to protected resource to trigger auth
            protected_url = f"{self.base_url}?request=me&method=GET"
            self.driver.get(protected_url)
            time.sleep(2)
            
            # Click Run Query to trigger authentication flow
            try:
                run_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr"))
                )
                print("🔑 Clicking Run Query to trigger authentication...")
                self.driver.execute_script("arguments[0].click();", run_button)
                time.sleep(3)
                
                print("✅ Authentication flow triggered!")
                return True
                
            except TimeoutException:
                print("⚠️  Could not find Run Query button")
                return False
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False

    def wait_for_authentication_completion(self) -> bool:
        """Wait for authentication with optimized detection"""
        print("\n🔐 AUTHENTICATION IN PROGRESS")
        print("=" * 50)
        print("1. 🔑 Complete Microsoft authentication in the browser")
        print("2. ✅ You'll be redirected back to Graph Explorer")
        print("3. ⏳ Detecting authentication completion...")
        
        max_wait_time = 300
        check_interval = 3
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                current_url = self.driver.current_url
                
                if "graph-explorer" in current_url:
                    print(f"✅ Back on Graph Explorer")
                    
                    # Test authentication by trying to access a simple resource
                    try:
                        simple_url = f"{self.base_url}?request=me&method=GET"
                        self.driver.get(simple_url)
                        time.sleep(1)
                        
                        # Try to find and click run button
                        run_button = self.driver.find_element(By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr")
                        if run_button.is_enabled():
                            print("✅ Authentication successful! Run button accessible.")
                            return True
                    except:
                        pass
                
                time.sleep(check_interval)
                elapsed_time += check_interval
                
                if elapsed_time % 15 == 0:
                    print(f"⏳ Still waiting... ({elapsed_time}/{max_wait_time}s)")
                
            except Exception as e:
                time.sleep(check_interval)
                elapsed_time += check_interval
        
        print("⏰ Authentication timeout")
        return False

    def execute_query_with_proven_extraction(self, query_name: str, query_info: Dict[str, str]) -> Optional[Any]:
        """Execute query using proven extraction method from automated_mygraph_pipeline.py"""
        print(f"\n📡 Executing: {query_info['description']}")
        print(f"🔍 Query: {query_info['query']}")
        
        try:
            # Navigate to query
            url = f"{self.base_url}?request={query_info['query']}&method=GET"
            print(f"🌐 Navigating to query...")
            self.driver.get(url)
            time.sleep(3)  # Match proven timing
            
            # Find and click run button
            try:
                run_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr"))
                )
                print("🖱️  Clicking run query button...")
                self.driver.execute_script("arguments[0].click();", run_button)
                print("✅ Successfully clicked run button")
            except TimeoutException:
                print("❌ Could not find run button")
                return None
            
            # Wait for results (using proven timing)
            print("⏳ Waiting for query results...")
            time.sleep(1)  # Very short initial wait (from proven method)
            
            # Quick response detection (from proven method)
            print("🔍 Quick response detection...")
            for attempt in range(1, 4):  # Try multiple times like proven method
                try:
                    response_element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".monaco-editor"))
                    )
                    
                    response_text = response_element.text
                    
                    if response_text and len(response_text.strip()) > 10:
                        print(f"✅ Found response in .monaco-editor (attempt {attempt})")
                        
                        # Apply proven JSON extraction strategies
                        extracted_data = self.extract_json_with_proven_strategies(response_text)
                        if extracted_data:
                            print(f"✅ Successfully extracted data")
                            return extracted_data
                        else:
                            print(f"⚠️  Could not parse response, storing as text")
                            return response_text
                    
                    time.sleep(0.5)  # Short wait between attempts (from proven method)
                    
                except TimeoutException:
                    if attempt < 3:
                        print(f"⏳ Attempt {attempt} - still waiting...")
                        time.sleep(1)
                    else:
                        print("⚠️  No response detected after multiple attempts")
            
            return None
            
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None

    def extract_json_with_proven_strategies(self, response_text: str) -> Optional[Any]:
        """Extract JSON using the proven strategies from automated_mygraph_pipeline.py"""
        if not response_text or len(response_text.strip()) < 5:
            return None
        
        # Try direct JSON parsing first
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # Apply proven extraction strategies
        json_extraction_attempts = [
            # Strategy 1: Find JSON between first { and last }
            lambda t: t[t.find('{'):t.rfind('}') + 1] if '{' in t and '}' in t else None,
            # Strategy 2: Find JSON between first [ and last ]
            lambda t: t[t.find('['):t.rfind(']') + 1] if '[' in t and ']' in t else None,
            # Strategy 3: Remove common prefixes/suffixes and wrap in braces
            lambda t: '{' + t.strip().strip('`').strip('"').strip("'") + '}' if not t.strip().startswith('{') and ':' in t else t.strip(),
            # Strategy 4: Clean and attempt to fix formatting
            lambda t: self.clean_and_fix_json(t)
        ]
        
        for i, extract_func in enumerate(json_extraction_attempts):
            try:
                json_part = extract_func(response_text)
                if json_part and json_part != response_text and len(json_part.strip()) > 5:
                    print(f"🔧 Trying extraction strategy {i+1}...")
                    response_data = json.loads(json_part)
                    
                    # Validate meaningful data (from proven method)
                    if isinstance(response_data, dict):
                        if len(response_data) > 1 or (len(response_data) == 1 and '@odata.context' not in response_data):
                            print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                            return response_data
                    elif isinstance(response_data, list) and len(response_data) > 0:
                        print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                        return response_data
                        
            except (json.JSONDecodeError, AttributeError, TypeError) as e:
                continue
        
        return None
    
    def clean_and_fix_json(self, text: str) -> Optional[str]:
        """Clean and fix JSON formatting issues"""
        cleaned = text.strip()
        
        # Remove non-JSON content
        lines = cleaned.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Skip obvious non-JSON content (from proven method)
            if any(skip in line.lower() for skip in [
                'graph.tips', 'request only returns', 'learn.microsoft',
                'to find out what', 'your app will need'
            ]):
                continue
            clean_lines.append(line)
        
        if not clean_lines:
            return None
            
        return '\n'.join(clean_lines)

    def analyze_collaboration_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collaboration patterns from collected data"""
        print("\n🔍 ANALYZING COLLABORATION PATTERNS")
        print("=" * 50)
        
        analysis = {
            "collaboration_insights": [],
            "meeting_collaborators": {},
            "email_collaborators": {},
            "people_api_ranking": [],
            "summary": {
                "total_data_sources": len([k for k, v in collected_data.items() if v is not None]),
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
        
        # Analyze People API (Microsoft's ML rankings)
        if collected_data.get("people_api"):
            people_data = collected_data["people_api"]
            if isinstance(people_data, dict) and "value" in people_data:
                people = people_data["value"]
                analysis["summary"]["people_api_count"] = len(people)
                
                for person in people[:10]:  # Top 10
                    if isinstance(person, dict):
                        name = person.get("displayName", "Unknown")
                        email = ""
                        if "scoredEmailAddresses" in person and person["scoredEmailAddresses"]:
                            email = person["scoredEmailAddresses"][0].get("address", "")
                        
                        analysis["people_api_ranking"].append({
                            "name": name,
                            "email": email,
                            "type": person.get("personType", {}).get("subclass", "Unknown")
                        })
                
                analysis["collaboration_insights"].append(f"People API: Microsoft ranked {len(people)} collaborators")
        
        # Analyze calendar meetings
        if collected_data.get("calendar_meetings"):
            meetings_data = collected_data["calendar_meetings"]
            if isinstance(meetings_data, dict) and "value" in meetings_data:
                meetings = meetings_data["value"]
                analysis["summary"]["meeting_count"] = len(meetings)
                
                collaborators = {}
                for meeting in meetings:
                    if isinstance(meeting, dict):
                        # Extract organizer and attendees
                        organizer = meeting.get("organizer", {})
                        if isinstance(organizer, dict) and "emailAddress" in organizer:
                            email = organizer["emailAddress"].get("address", "")
                            if email:
                                collaborators[email] = collaborators.get(email, 0) + 1
                        
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
        
        return analysis

    def run_hybrid_extraction(self) -> Dict[str, Any]:
        """Run complete hybrid auto-trigger extraction"""
        print("🚀 HYBRID AUTO-TRIGGER GRAPH COLLABORATION EXTRACTOR")
        print("=" * 70)
        print("Combines working authentication trigger with proven extraction method")
        print()
        
        # Setup browser and trigger authentication
        if not self.setup_browser_and_trigger_auth():
            return {"error": "Failed to setup browser or trigger authentication"}
        
        # Wait for authentication completion
        if not self.wait_for_authentication_completion():
            if self.driver:
                self.driver.quit()
            return {"error": "Authentication not completed"}
        
        # Execute collaboration queries with proven extraction
        collected_data = {}
        success_count = 0
        
        for query_name, query_info in self.collaboration_queries.items():
            result = self.execute_query_with_proven_extraction(query_name, query_info)
            if result:
                collected_data[query_name] = result
                success_count += 1
            else:
                collected_data[query_name] = None
            
            time.sleep(2)  # Delay between queries
        
        print(f"\n📊 DATA COLLECTION SUMMARY:")
        print(f"   ✅ Successful: {success_count}/{len(self.collaboration_queries)}")
        
        # Analyze collaboration patterns
        analysis = self.analyze_collaboration_data(collected_data)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_results = {
            "timestamp": timestamp,
            "method": "hybrid_auto_trigger_with_proven_extraction",
            "authentication": "automatic_trigger",
            "extraction_strategies": "proven_5_strategy_method",
            "queries_executed": len(self.collaboration_queries),
            "successful_extractions": success_count,
            "raw_data": collected_data,
            "collaboration_analysis": analysis
        }
        
        # Save to file
        output_file = f"hybrid_collaboration_extraction_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(final_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Cleanup
        if self.driver:
            self.driver.quit()
        
        return final_results


def main():
    """Main execution function"""
    extractor = HybridAutoTriggerExtractor()
    
    try:
        results = extractor.run_hybrid_extraction()
        
        if "error" not in results:
            print("\n🎊 HYBRID COLLABORATION EXTRACTION COMPLETE!")
            print("=" * 60)
            
            print(f"\n📊 EXECUTION SUMMARY:")
            print(f"   • Method: {results.get('method', 'Unknown')}")
            print(f"   • Authentication: {results.get('authentication', 'Unknown')}")
            print(f"   • Success Rate: {results.get('successful_extractions', 0)}/{results.get('queries_executed', 0)}")
            
            # Show collaboration insights
            analysis = results.get("collaboration_analysis", {})
            insights = analysis.get("collaboration_insights", [])
            
            if insights:
                print(f"\n💡 COLLABORATION INSIGHTS:")
                for insight in insights:
                    print(f"   • {insight}")
            
            # Show People API rankings (Microsoft's ML-powered rankings)
            people_ranking = analysis.get("people_api_ranking", [])
            if people_ranking:
                print(f"\n👥 MICROSOFT PEOPLE API TOP COLLABORATORS:")
                for i, person in enumerate(people_ranking[:5], 1):
                    print(f"   {i}. {person['name']} ({person.get('email', 'No email')}) - {person.get('type', 'Unknown')}")
            
            # Show meeting collaborators
            meeting_collaborators = analysis.get("meeting_collaborators", {})
            if meeting_collaborators:
                print(f"\n📅 TOP MEETING COLLABORATORS:")
                for email, count in list(meeting_collaborators.items())[:5]:
                    print(f"   • {email}: {count} meetings")
            
            print(f"\n📄 Complete results: hybrid_collaboration_extraction_{results['timestamp']}.json")
            
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