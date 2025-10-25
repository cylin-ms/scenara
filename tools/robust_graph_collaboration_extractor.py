#!/usr/bin/env python3
"""
Robust Automatic Graph Explorer Collaboration Extractor
Enhanced version with improved JSON extraction and collaboration analysis
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


class RobustGraphCollaborationExtractor:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.wait_timeout = 30
        self.driver = None
        
        # Comprehensive collaboration queries
        self.collaboration_queries = {
            "profile": {
                "query": "me",
                "description": "User Profile",
                "collaboration_value": "identity"
            },
            "manager": {
                "query": "me/manager",
                "description": "Manager Information",
                "collaboration_value": "hierarchy"
            },
            "calendar_meetings": {
                "query": "me/calendarView?startDateTime=2025-09-01T00:00:00Z&endDateTime=2025-10-25T23:59:59Z&$select=subject,organizer,attendees,start,end,onlineMeeting&$top=100",
                "description": "Recent Calendar Meetings",
                "collaboration_value": "high"
            },
            "people_api": {
                "query": "me/people?$top=50",
                "description": "People You Work With Most",
                "collaboration_value": "high"
            },
            "teams_chats": {
                "query": "me/chats?$expand=members&$top=20",
                "description": "Teams Chat Conversations", 
                "collaboration_value": "high"
            },
            "recent_emails": {
                "query": "me/messages?$top=50&$select=sender,toRecipients,ccRecipients,subject,receivedDateTime,bodyPreview",
                "description": "Recent Email Communications",
                "collaboration_value": "high"
            },
            "shared_files": {
                "query": "me/drive/sharedWithMe?$top=20&$select=name,createdBy,lastModifiedBy,sharedBy",
                "description": "Files Shared With You",
                "collaboration_value": "medium"
            },
            "teams_joined": {
                "query": "me/joinedTeams?$select=displayName,description,members",
                "description": "Teams You're Member Of",
                "collaboration_value": "medium"
            },
            "direct_reports": {
                "query": "me/directReports",
                "description": "Direct Reports",
                "collaboration_value": "hierarchy"
            }
        }
        
    def setup_browser(self) -> bool:
        """Setup Chrome browser with optimized settings"""
        print("🌐 Setting up Chrome browser for Microsoft Graph Explorer...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=VizDisplayCompositor')
            
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
        """Enhanced authentication detection"""
        print("\n🔐 AUTHENTICATION REQUIRED")
        print("=" * 50)
        print("1. 📱 Complete Microsoft authentication in the browser")
        print("2. ✅ Ensure you're signed in to Graph Explorer")
        print("3. ⏳ Waiting for authentication confirmation...")
        
        max_wait_time = 300  # 5 minutes
        check_interval = 3
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                # Multiple authentication indicators
                auth_selectors = [
                    "[aria-label*='Sign out']",
                    ".ms-Persona",
                    "[data-testid='persona']",
                    "//*[contains(text(), 'Sign out')]",
                    ".profile-button",
                    "[title*='Sign out']",
                    ".user-profile"
                ]
                
                for selector in auth_selectors:
                    try:
                        if selector.startswith("//"):
                            # XPath selector
                            element = WebDriverWait(self.driver, 1).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                        else:
                            # CSS selector
                            element = WebDriverWait(self.driver, 1).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                        
                        if element:
                            print("✅ Authentication detected! Proceeding with data collection...")
                            return True
                    except TimeoutException:
                        continue
                
                time.sleep(check_interval)
                elapsed_time += check_interval
                if elapsed_time % 15 == 0:  # Progress update every 15 seconds
                    print(f"⏳ Still waiting for authentication... ({elapsed_time}/{max_wait_time}s)")
                
            except Exception as e:
                print(f"⚠️  Error during auth check: {e}")
                time.sleep(check_interval)
                elapsed_time += check_interval
        
        print("⏰ Authentication timeout reached")
        return False

    def enhanced_json_extraction(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Enhanced JSON extraction with 8 improved strategies"""
        if not response_text or len(response_text.strip()) < 5:
            return None
            
        # Strategy 1: Direct JSON parsing (fastest)
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Find complete JSON object between braces
        brace_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group())
            except json.JSONDecodeError:
                pass
        
        # Strategy 3: Find complete JSON array
        array_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if array_match:
            try:
                return json.loads(array_match.group())
            except json.JSONDecodeError:
                pass
        
        # Strategy 4: Monaco editor line reconstruction (enhanced)
        reconstructed = self._reconstruct_monaco_json(response_text)
        if reconstructed:
            try:
                return json.loads(reconstructed)
            except json.JSONDecodeError:
                pass
        
        # Strategy 5: Clean and fix common formatting issues
        cleaned = self._clean_json_text(response_text)
        if cleaned:
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
        
        # Strategy 6: Extract from code blocks
        code_block_match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', response_text, re.DOTALL)
        if code_block_match:
            try:
                return json.loads(code_block_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Strategy 7: Property-by-property reconstruction
        property_json = self._extract_properties(response_text)
        if property_json:
            try:
                return json.loads(property_json)
            except json.JSONDecodeError:
                pass
        
        # Strategy 8: Fallback - return structured text analysis
        return self._text_to_structure(response_text)

    def _reconstruct_monaco_json(self, text: str) -> Optional[str]:
        """Enhanced Monaco editor JSON reconstruction"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Skip non-JSON lines
        json_lines = []
        for line in lines:
            if any(skip in line.lower() for skip in [
                'graph.tips', 'request only returns', 'learn.microsoft',
                'to find out what', 'your app will need', 'the request returned'
            ]):
                continue
            if line.strip() and not line.startswith('//'):
                json_lines.append(line)
        
        if not json_lines:
            return None
        
        # Try to reconstruct complete JSON
        json_text = '\n'.join(json_lines)
        
        # Fix common Monaco formatting issues
        json_text = re.sub(r'^\s*```\s*', '', json_text)  # Remove code block markers
        json_text = re.sub(r'\s*```\s*$', '', json_text)
        json_text = re.sub(r'(\w+):', r'"\1":', json_text)  # Quote unquoted keys
        
        return json_text

    def _clean_json_text(self, text: str) -> Optional[str]:
        """Clean and fix JSON formatting"""
        # Remove common prefixes/suffixes
        cleaned = text.strip()
        cleaned = re.sub(r'^[^{[]*([{[].*[}\]])[^}\]]*$', r'\1', cleaned, flags=re.DOTALL)
        
        # Fix common issues
        cleaned = cleaned.replace('\\n', '\n')
        cleaned = cleaned.replace('\\"', '"')
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)  # Remove trailing commas
        
        return cleaned if cleaned != text else None

    def _extract_properties(self, text: str) -> Optional[str]:
        """Extract properties and reconstruct JSON"""
        properties = {}
        
        # Find property patterns: "key": value
        property_pattern = r'"([^"]+)"\s*:\s*([^,\n\r]+)'
        matches = re.findall(property_pattern, text)
        
        for key, value in matches:
            value = value.strip().rstrip(',')
            
            # Parse value types
            if value == 'null':
                properties[key] = None
            elif value.lower() == 'true':
                properties[key] = True
            elif value.lower() == 'false':
                properties[key] = False
            elif value.startswith('"') and value.endswith('"'):
                properties[key] = value[1:-1]
            elif value.isdigit():
                properties[key] = int(value)
            elif '.' in value and value.replace('.', '').isdigit():
                properties[key] = float(value)
            else:
                properties[key] = value
        
        return json.dumps(properties) if properties else None

    def _text_to_structure(self, text: str) -> Dict[str, Any]:
        """Convert text to structured data as fallback"""
        return {
            "raw_text": text[:1000],  # Limit size
            "extracted_at": datetime.now().isoformat(),
            "extraction_method": "fallback_text_analysis",
            "text_length": len(text)
        }

    def execute_query_robust(self, query_name: str, query_info: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Execute query with robust error handling and extraction"""
        print(f"\n📡 Executing: {query_info['description']}")
        print(f"🔍 Query: {query_info['query']}")
        
        try:
            # Navigate to the query
            url = f"{self.base_url}?request={query_info['query']}&method=GET"
            print(f"🌐 Navigating to query...")
            self.driver.get(url)
            
            # Wait for page load
            time.sleep(3)
            
            # Find and click run button with multiple selectors
            run_button_selectors = [
                "span.___1ej4kmx.f22iagw.f122n59.fkln5zr",
                "button[aria-label*='Run']",
                "button:contains('Run query')",
                ".run-query-button",
                "[data-testid='run-query']"
            ]
            
            run_clicked = False
            for selector in run_button_selectors:
                try:
                    if selector.startswith("button:contains"):
                        # XPath for contains
                        xpath = f"//button[contains(text(), 'Run')]"
                        run_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                    else:
                        run_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    self.driver.execute_script("arguments[0].click();", run_button)
                    print("✅ Successfully clicked run button")
                    run_clicked = True
                    break
                except TimeoutException:
                    continue
            
            if not run_clicked:
                print("❌ Could not find run button")
                return None
            
            # Wait for results with progressive timeouts
            print("⏳ Waiting for query results...")
            
            # Wait for loading to complete
            for wait_time in [3, 5, 8]:
                time.sleep(wait_time)
                
                # Try multiple selectors for response content
                response_selectors = [
                    ".monaco-editor",
                    ".response-preview",
                    ".json-response",
                    "[data-testid='response']",
                    ".code-editor"
                ]
                
                for selector in response_selectors:
                    try:
                        response_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        response_text = response_element.text
                        
                        if response_text and len(response_text.strip()) > 10:
                            print(f"✅ Got response ({len(response_text)} characters)")
                            
                            # Enhanced JSON extraction
                            result = self.enhanced_json_extraction(response_text)
                            if result:
                                print(f"✅ Successfully extracted structured data")
                                return result
                            else:
                                print("⚠️  Could not parse response as JSON")
                                return {"raw_response": response_text, "query": query_info['query']}
                        
                    except NoSuchElementException:
                        continue
                
                print(f"⏳ Still waiting... (attempt {wait_time})")
            
            print("⚠️  No response detected after multiple attempts")
            return None
                
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return None

    def analyze_collaboration_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive collaboration analysis"""
        print("\n🔍 ANALYZING COLLABORATION PATTERNS")
        print("=" * 50)
        
        analysis = {
            "collaboration_score": {},
            "meeting_partners": {},
            "email_partners": {},
            "chat_partners": {},
            "file_collaborators": {},
            "teams_membership": {},
            "summary": {
                "total_data_sources": len([k for k, v in collected_data.items() if v is not None]),
                "analysis_timestamp": datetime.now().isoformat(),
                "collaboration_insights": []
            }
        }
        
        # Analyze calendar meetings
        if collected_data.get("calendar_meetings"):
            meetings_data = collected_data["calendar_meetings"]
            if isinstance(meetings_data, dict) and "value" in meetings_data:
                meetings = meetings_data["value"]
                analysis["summary"]["meeting_count"] = len(meetings)
                
                # Extract meeting collaborators
                meeting_collaborators = {}
                for meeting in meetings:
                    if isinstance(meeting, dict):
                        # Organizer
                        organizer = meeting.get("organizer", {})
                        if isinstance(organizer, dict) and "emailAddress" in organizer:
                            email = organizer["emailAddress"].get("address", "")
                            if email:
                                meeting_collaborators[email] = meeting_collaborators.get(email, 0) + 1
                        
                        # Attendees
                        attendees = meeting.get("attendees", [])
                        if isinstance(attendees, list):
                            for attendee in attendees:
                                if isinstance(attendee, dict) and "emailAddress" in attendee:
                                    email = attendee["emailAddress"].get("address", "")
                                    if email:
                                        meeting_collaborators[email] = meeting_collaborators.get(email, 0) + 1
                
                # Sort and store top meeting partners
                sorted_partners = sorted(meeting_collaborators.items(), key=lambda x: x[1], reverse=True)
                analysis["meeting_partners"] = dict(sorted_partners[:20])
                analysis["summary"]["collaboration_insights"].append(f"Identified {len(meeting_collaborators)} unique meeting collaborators")
        
        # Analyze People API data
        if collected_data.get("people_api"):
            people_data = collected_data["people_api"]
            if isinstance(people_data, dict) and "value" in people_data:
                people = people_data["value"]
                analysis["summary"]["people_api_count"] = len(people)
                
                people_scores = []
                for person in people:
                    if isinstance(person, dict):
                        name = person.get("displayName", "Unknown")
                        email = ""
                        if "scoredEmailAddresses" in person and person["scoredEmailAddresses"]:
                            email = person["scoredEmailAddresses"][0].get("address", "")
                        
                        score_data = person.get("personType", {})
                        people_scores.append({
                            "name": name, 
                            "email": email, 
                            "type": score_data.get("subclass", "Unknown"),
                            "class": score_data.get("class", "Unknown")
                        })
                
                analysis["collaboration_score"]["people_api"] = people_scores[:15]
                analysis["summary"]["collaboration_insights"].append(f"People API ranked {len(people_scores)} collaborators")
        
        # Analyze email communications
        if collected_data.get("recent_emails"):
            emails_data = collected_data["recent_emails"]
            if isinstance(emails_data, dict) and "value" in emails_data:
                emails = emails_data["value"]
                analysis["summary"]["email_count"] = len(emails)
                
                email_collaborators = {}
                for email in emails:
                    if isinstance(email, dict):
                        # Sender
                        sender = email.get("sender", {})
                        if isinstance(sender, dict) and "emailAddress" in sender:
                            sender_email = sender["emailAddress"].get("address", "")
                            if sender_email:
                                email_collaborators[sender_email] = email_collaborators.get(sender_email, 0) + 1
                        
                        # Recipients
                        for recipient_type in ["toRecipients", "ccRecipients"]:
                            recipients = email.get(recipient_type, [])
                            if isinstance(recipients, list):
                                for recipient in recipients:
                                    if isinstance(recipient, dict) and "emailAddress" in recipient:
                                        rec_email = recipient["emailAddress"].get("address", "")
                                        if rec_email:
                                            email_collaborators[rec_email] = email_collaborators.get(rec_email, 0) + 1
                
                sorted_email_partners = sorted(email_collaborators.items(), key=lambda x: x[1], reverse=True)
                analysis["email_partners"] = dict(sorted_email_partners[:15])
                analysis["summary"]["collaboration_insights"].append(f"Email analysis: {len(email_collaborators)} unique email collaborators")
        
        # Analyze Teams data
        if collected_data.get("teams_joined"):
            teams_data = collected_data["teams_joined"]
            if isinstance(teams_data, dict) and "value" in teams_data:
                teams = teams_data["value"]
                analysis["summary"]["teams_count"] = len(teams)
                
                team_info = []
                for team in teams:
                    if isinstance(team, dict):
                        team_info.append({
                            "name": team.get("displayName", "Unknown"),
                            "description": team.get("description", "")[:100]
                        })
                
                analysis["teams_membership"] = team_info
                analysis["summary"]["collaboration_insights"].append(f"Member of {len(teams)} Teams")
        
        return analysis

    def run_robust_extraction(self) -> Dict[str, Any]:
        """Run complete robust collaboration extraction"""
        print("🚀 ROBUST AUTOMATIC GRAPH COLLABORATION EXTRACTOR")
        print("=" * 70)
        print("Enhanced version with 8 extraction strategies and comprehensive analysis")
        print()
        
        # Setup browser
        if not self.setup_browser():
            return {"error": "Browser setup failed"}
        
        # Wait for authentication
        if not self.wait_for_authentication():
            self.driver.quit()
            return {"error": "Authentication failed"}
        
        # Collect data for each query
        collected_data = {}
        success_count = 0
        
        for query_name, query_info in self.collaboration_queries.items():
            result = self.execute_query_robust(query_name, query_info)
            if result:
                collected_data[query_name] = result
                success_count += 1
            else:
                collected_data[query_name] = None
            
            # Delay between queries
            time.sleep(2)
        
        print(f"\n📊 DATA COLLECTION SUMMARY:")
        print(f"   ✅ Successful: {success_count}/{len(self.collaboration_queries)}")
        print(f"   📭 Failed: {len(self.collaboration_queries) - success_count}")
        
        # Analyze collaboration patterns
        analysis = self.analyze_collaboration_data(collected_data)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "timestamp": timestamp,
            "method": "robust_automatic_graph_extraction",
            "extraction_success_rate": f"{success_count}/{len(self.collaboration_queries)}",
            "raw_data": collected_data,
            "collaboration_analysis": analysis,
            "metadata": {
                "extraction_strategies": 8,
                "queries_executed": len(self.collaboration_queries),
                "successful_extractions": success_count
            }
        }
        
        # Save to file
        output_file = f"robust_collaboration_extraction_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Cleanup
        if self.driver:
            self.driver.quit()
        
        return results


def main():
    """Main execution function"""
    extractor = RobustGraphCollaborationExtractor()
    
    try:
        results = extractor.run_robust_extraction()
        
        if "error" not in results:
            print("\n🎊 ROBUST COLLABORATION EXTRACTION COMPLETE!")
            print("=" * 60)
            
            analysis = results.get("collaboration_analysis", {})
            summary = analysis.get("summary", {})
            
            # Show summary
            print(f"\n📊 EXTRACTION SUMMARY:")
            print(f"   • Success Rate: {results.get('extraction_success_rate', 'Unknown')}")
            print(f"   • Data Sources: {summary.get('total_data_sources', 0)}")
            print(f"   • Extraction Strategies: {results.get('metadata', {}).get('extraction_strategies', 0)}")
            
            # Show insights
            if summary.get("collaboration_insights"):
                print(f"\n💡 COLLABORATION INSIGHTS:")
                for insight in summary["collaboration_insights"]:
                    print(f"   • {insight}")
            
            # Show top meeting collaborators
            meeting_partners = analysis.get("meeting_partners", {})
            if meeting_partners:
                print(f"\n📅 TOP MEETING COLLABORATORS:")
                for email, count in list(meeting_partners.items())[:5]:
                    print(f"   • {email}: {count} meetings")
            
            # Show People API results
            people_api = analysis.get("collaboration_score", {}).get("people_api", [])
            if people_api:
                print(f"\n👥 PEOPLE API TOP COLLABORATORS:")
                for person in people_api[:5]:
                    print(f"   • {person['name']} ({person.get('email', 'No email')}) - {person.get('type', 'Unknown')}")
            
            # Show email collaborators
            email_partners = analysis.get("email_partners", {})
            if email_partners:
                print(f"\n📧 TOP EMAIL COLLABORATORS:")
                for email, count in list(email_partners.items())[:5]:
                    print(f"   • {email}: {count} emails")
            
            print(f"\n📄 Complete results saved to: robust_collaboration_extraction_{results['timestamp']}.json")
            
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