#!/usr/bin/env python3
"""
Auto-Triggering Graph Explorer Collaboration Extractor
Automatically triggers Microsoft authentication in Graph Explorer
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import webbrowser

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


class AutoTriggerGraphExtractor:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.wait_timeout = 30
        self.driver = None
        
        # Key collaboration queries
        self.key_queries = {
            "people_api": "me/people?$top=50",
            "calendar_meetings": "me/calendarView?startDateTime=2025-09-01T00:00:00Z&endDateTime=2025-10-25T23:59:59Z&$select=subject,organizer,attendees,start,end",
            "recent_emails": "me/messages?$top=50&$select=sender,toRecipients,ccRecipients,subject,receivedDateTime",
            "teams_chats": "me/chats?$expand=members&$top=20"
        }
        
    def setup_browser_and_trigger_auth(self) -> bool:
        """Setup browser and automatically trigger authentication"""
        print("🌐 Setting up Chrome browser with auto-authentication...")
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Keep browser visible for authentication
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            
            print("🌐 Opening Graph Explorer...")
            self.driver.get(self.base_url)
            
            # Wait for page to load
            time.sleep(3)
            
            print("🔑 Attempting to trigger authentication automatically...")
            
            # Strategy 1: Click on Sign In button if visible
            sign_in_selectors = [
                "button[aria-label*='Sign in']",
                "a[aria-label*='Sign in']", 
                ".sign-in-button",
                "[data-testid='sign-in']",
                "button:contains('Sign in')",
                "a:contains('Sign in')"
            ]
            
            for selector in sign_in_selectors:
                try:
                    if "contains" in selector:
                        # XPath approach
                        xpath_selector = f"//button[contains(text(), 'Sign in')] | //a[contains(text(), 'Sign in')]"
                        sign_in_element = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, xpath_selector))
                        )
                    else:
                        sign_in_element = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ Found sign-in button with selector: {selector}")
                    self.driver.execute_script("arguments[0].click();", sign_in_element)
                    print("🔑 Clicked sign-in button - authentication should start...")
                    time.sleep(5)  # Wait for auth redirect
                    return True
                    
                except TimeoutException:
                    continue
            
            # Strategy 2: Navigate to a protected resource to trigger auth
            print("🔄 Trying protected resource to trigger authentication...")
            protected_url = f"{self.base_url}?request=me&method=GET"
            self.driver.get(protected_url)
            time.sleep(3)
            
            # Try to click Run Query to trigger auth
            try:
                run_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr"))
                )
                print("🔑 Clicking Run Query to trigger authentication...")
                self.driver.execute_script("arguments[0].click();", run_button)
                time.sleep(3)
                
                # This should trigger authentication flow
                print("✅ Authentication flow should have started...")
                return True
                
            except TimeoutException:
                print("⚠️  Could not find Run Query button")
            
            # Strategy 3: Direct Microsoft login URL
            print("🔄 Opening Microsoft login directly...")
            microsoft_login_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=de8bc8b5-d9f9-48b1-a8ad-b748da725064&response_type=code&redirect_uri=https://developer.microsoft.com/en-us/graph/graph-explorer&scope=https://graph.microsoft.com/.default&state=graph-explorer"
            
            # Open in new tab
            self.driver.execute_script(f"window.open('{microsoft_login_url}', '_blank');")
            
            # Switch to new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("🔑 Microsoft login page opened - please complete authentication...")
            
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False

    def wait_for_authentication_completion(self) -> bool:
        """Wait for authentication to complete and return to Graph Explorer"""
        print("\n🔐 AUTHENTICATION IN PROGRESS")
        print("=" * 50)
        print("1. 🔑 Complete Microsoft authentication in the browser window")
        print("2. ✅ You should be redirected back to Graph Explorer")
        print("3. ⏳ Waiting to detect successful authentication...")
        
        max_wait_time = 300  # 5 minutes
        check_interval = 5
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                # Check current URL and page content
                current_url = self.driver.current_url
                
                # Check if we're back on Graph Explorer and authenticated
                if "graph-explorer" in current_url:
                    print(f"✅ Back on Graph Explorer: {current_url[:80]}...")
                    
                    # Look for authenticated state indicators
                    auth_indicators = [
                        "[aria-label*='Sign out']",
                        ".ms-Persona",
                        "[data-testid='persona']",
                        ".user-profile",
                        ".profile-button"
                    ]
                    
                    for indicator in auth_indicators:
                        try:
                            element = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, indicator))
                            )
                            if element:
                                print("✅ Authentication detected! Ready to collect data...")
                                return True
                        except TimeoutException:
                            continue
                    
                    # Try to run a simple query to test authentication
                    try:
                        # Navigate to a simple query
                        test_url = f"{self.base_url}?request=me&method=GET"
                        self.driver.get(test_url)
                        time.sleep(2)
                        
                        # Try to click run button
                        run_button = self.driver.find_element(By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr")
                        if run_button:
                            print("✅ Run button accessible - authentication likely successful!")
                            return True
                    except:
                        pass
                
                time.sleep(check_interval)
                elapsed_time += check_interval
                
                if elapsed_time % 15 == 0:  # Progress update every 15 seconds
                    print(f"⏳ Still waiting for authentication... ({elapsed_time}/{max_wait_time}s)")
                    print(f"   Current URL: {self.driver.current_url[:60]}...")
                
            except Exception as e:
                print(f"⚠️  Error during auth check: {e}")
                time.sleep(check_interval)
                elapsed_time += check_interval
        
        print("⏰ Authentication timeout reached")
        return False

    def extract_response_with_fallbacks(self) -> Optional[str]:
        """Extract response using multiple fallback strategies"""
        # Strategy 1: Monaco editor
        try:
            response_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".monaco-editor"))
            )
            response_text = response_element.text
            if response_text and len(response_text.strip()) > 10:
                return response_text
        except TimeoutException:
            pass
        
        # Strategy 2: Response preview area
        try:
            response_element = self.driver.find_element(By.CSS_SELECTOR, ".response-preview")
            response_text = response_element.text
            if response_text and len(response_text.strip()) > 10:
                return response_text
        except NoSuchElementException:
            pass
        
        # Strategy 3: JSON response area
        try:
            response_element = self.driver.find_element(By.CSS_SELECTOR, ".json-response")
            response_text = response_element.text
            if response_text and len(response_text.strip()) > 10:
                return response_text
        except NoSuchElementException:
            pass
        
        # Strategy 4: Code editor area
        try:
            response_element = self.driver.find_element(By.CSS_SELECTOR, ".code-editor")
            response_text = response_element.text
            if response_text and len(response_text.strip()) > 10:
                return response_text
        except NoSuchElementException:
            pass
        
        # Strategy 5: Get page source and extract JSON
        try:
            page_source = self.driver.page_source
            # Look for JSON patterns in page source
            import re
            json_match = re.search(r'\{[^{}]*"@odata\.context"[^{}]*\}', page_source)
            if json_match:
                return json_match.group()
        except Exception:
            pass
        
        print("⚠️  Could not extract response with any strategy")
        return None

    def execute_collaboration_queries(self) -> Dict[str, Any]:
        """Execute key collaboration queries"""
        print("\n📡 EXECUTING COLLABORATION QUERIES")
        print("=" * 50)
        
        results = {}
        
        for query_name, query in self.key_queries.items():
            print(f"\n🔍 Executing: {query_name}")
            print(f"   Query: {query}")
            
            try:
                # Navigate to query
                url = f"{self.base_url}?request={query}&method=GET"
                self.driver.get(url)
                time.sleep(2)
                
                # Click run button
                run_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.___1ej4kmx.f22iagw.f122n59.fkln5zr"))
                )
                self.driver.execute_script("arguments[0].click();", run_button)
                
                # Wait for response
                time.sleep(5)
                
                # Get response with enhanced extraction
                response_text = self.extract_response_with_fallbacks()
                
                if response_text and len(response_text.strip()) > 10:
                    print(f"✅ Got response ({len(response_text)} characters)")
                    
                    # Try to parse as JSON for validation
                    try:
                        parsed_response = json.loads(response_text)
                        results[query_name] = parsed_response
                        print(f"   ✅ Successfully parsed as JSON")
                    except json.JSONDecodeError:
                        # Store as text if not valid JSON
                        results[query_name] = response_text
                        print(f"   ⚠️  Stored as text (not valid JSON)")
                else:
                    print("⚠️  Empty or short response")
                    results[query_name] = None
                
            except Exception as e:
                print(f"❌ Error executing {query_name}: {e}")
                results[query_name] = None
        
        return results

    def run_auto_trigger_extraction(self) -> Dict[str, Any]:
        """Run complete auto-triggering extraction"""
        print("🚀 AUTO-TRIGGERING GRAPH COLLABORATION EXTRACTOR")
        print("=" * 70)
        print("Automatically triggers Microsoft authentication and collects collaboration data")
        print()
        
        # Setup browser and trigger authentication
        if not self.setup_browser_and_trigger_auth():
            return {"error": "Failed to setup browser or trigger authentication"}
        
        # Wait for authentication to complete
        if not self.wait_for_authentication_completion():
            if self.driver:
                self.driver.quit()
            return {"error": "Authentication not completed within timeout"}
        
        # Execute collaboration queries
        results = self.execute_collaboration_queries()
        
        # Process and save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_results = {
            "timestamp": timestamp,
            "method": "auto_trigger_graph_extraction",
            "authentication": "automatic_trigger",
            "queries_executed": len(self.key_queries),
            "successful_queries": len([r for r in results.values() if r is not None]),
            "raw_responses": results
        }
        
        # Save to file
        output_file = f"auto_trigger_collaboration_extraction_{timestamp}.json"
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
    extractor = AutoTriggerGraphExtractor()
    
    try:
        results = extractor.run_auto_trigger_extraction()
        
        if "error" not in results:
            print("\n🎊 AUTO-TRIGGER COLLABORATION EXTRACTION COMPLETE!")
            print("=" * 60)
            
            print(f"\n📊 EXECUTION SUMMARY:")
            print(f"   • Authentication: {results.get('authentication', 'Unknown')}")
            print(f"   • Queries Executed: {results.get('queries_executed', 0)}")
            print(f"   • Successful Queries: {results.get('successful_queries', 0)}")
            
            # Show raw responses summary
            raw_responses = results.get("raw_responses", {})
            print(f"\n📡 QUERY RESULTS:")
            for query_name, response in raw_responses.items():
                status = "✅ Success" if response else "❌ No data"
                length = len(response) if response else 0
                print(f"   • {query_name}: {status} ({length} chars)")
            
            print(f"\n📄 Complete results saved to: auto_trigger_collaboration_extraction_{results['timestamp']}.json")
            
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