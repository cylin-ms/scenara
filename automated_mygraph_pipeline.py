#!/usr/bin/env python3
"""
Automated MyGraph Data Collection and Processing Pipeline
Fully automated process that bypasses authentication issues
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
from urllib.parse import quote

try:
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
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
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager

class AutomatedMyGraphPipeline:
    def __init__(self):
        self.base_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.wait_timeout = 30
        self.driver = None
        self.collected_data = {}
        
    def setup_browser(self, headless: bool = False) -> bool:
        """Setup browser (try Edge first, fallback to Chrome)"""
        print("🌐 Setting up browser for Microsoft Graph Explorer...")
        
        # Try Edge first (better for Microsoft services)
        try:
            print("🔵 Attempting Microsoft Edge...")
            options = webdriver.EdgeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            if headless:
                options.add_argument('--headless')
            
            self.driver = webdriver.Edge(options=options)
            self.driver.maximize_window()
            
            # Navigate to Graph Explorer
            print("🌐 Opening Graph Explorer with Edge...")
            self.driver.get(self.base_url)
            
            print("✅ Edge browser setup successful")
            return True
            
        except Exception as e:
            print(f"⚠️  Edge not available: {e}")
            print("� Trying Chrome as fallback...")
            
            # Fallback to Chrome
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                if headless:
                    options.add_argument('--headless')
                
                self.driver = webdriver.Chrome(options=options)
                self.driver.maximize_window()
                
                # Navigate to Graph Explorer
                print("🌐 Opening Graph Explorer with Chrome...")
                self.driver.get(self.base_url)
                
                print("✅ Chrome browser setup successful")
                return True
                
            except Exception as chrome_error:
                print(f"❌ Chrome also failed: {chrome_error}")
                print("\n💡 Browser setup failed. Please ensure you have:")
                print("   • Microsoft Edge WebDriver, or")
                print("   • Chrome WebDriver")
                print("   • Selenium package: pip install selenium")
                return False

    def wait_for_authentication(self) -> bool:
        """Wait for user to complete authentication manually"""
        print("\n🔐 AUTHENTICATION REQUIRED")
        print("=" * 50)
        print("1. 📱 Complete Microsoft authentication in the browser")
        print("2. ✅ Ensure you're signed in to Graph Explorer")
        print("3. ⏳ Waiting for authentication confirmation...")
        print("4. 🔄 Will check every 5 seconds for successful login")
        
        max_wait_time = 300  # 5 minutes
        check_interval = 5
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                # Check if we can find elements that indicate successful auth
                if self.driver.current_url.startswith(self.base_url):
                    # Look for signed-in indicators
                    try:
                        # Check for user profile or sign-out button
                        WebDriverWait(self.driver, 2).until(
                            EC.any_of(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label*='Sign out']")),
                                EC.presence_of_element_located((By.CSS_SELECTOR, ".ms-Persona")),
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='persona']")),
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign out')]"))
                            )
                        )
                        print("✅ Authentication detected! Proceeding with data collection...")
                        return True
                    except TimeoutException:
                        pass
                
                time.sleep(check_interval)
                elapsed_time += check_interval
                print(f"⏳ Still waiting... ({elapsed_time}/{max_wait_time}s)")
                
            except Exception as e:
                print(f"⚠️  Error during auth check: {e}")
                time.sleep(check_interval)
                elapsed_time += check_interval
        
        print("⏰ Authentication timeout reached")
        return False

    def _reconstruct_json_from_lines(self, text: str) -> str:
        """Reconstruct JSON from Monaco editor lines (handles fragmented display)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Build a proper JSON object from the fragmented lines
        properties = {}
        current_key = None
        
        for line in lines:
            # Skip obvious non-JSON lines
            if any(skip in line.lower() for skip in ['graph.tips', 'request only returns', 'learn.microsoft']):
                continue
                
            # Handle property lines: "key": value
            if '"' in line and ':' in line and not line.startswith(('@odata', 'properties')):
                try:
                    # Clean up the line
                    clean_line = line.rstrip(',').strip()
                    
                    # Extract key-value pairs
                    if clean_line.count('"') >= 2 and '":' in clean_line:
                        # Split on the first occurrence of ": 
                        parts = clean_line.split('": ', 1)
                        if len(parts) == 2:
                            key = parts[0].strip().strip('"')
                            value_str = parts[1].strip()
                            
                            # Parse the value
                            if value_str == 'null':
                                properties[key] = None
                            elif value_str.startswith('"') and value_str.endswith('"'):
                                properties[key] = value_str[1:-1]
                            elif value_str.lower() == 'true':
                                properties[key] = True
                            elif value_str.lower() == 'false':
                                properties[key] = False
                            elif value_str.startswith('['):
                                # Handle arrays (might be incomplete)
                                current_key = key
                                properties[key] = []
                                if value_str.endswith(']'):
                                    # Complete array in one line
                                    try:
                                        import json
                                        properties[key] = json.loads(value_str)
                                    except:
                                        properties[key] = [value_str.strip('[]"')]
                            else:
                                # Try as number
                                try:
                                    if '.' in value_str:
                                        properties[key] = float(value_str)
                                    else:
                                        properties[key] = int(value_str)
                                except:
                                    properties[key] = value_str
                except Exception as e:
                    continue
            
            # Handle array elements that appear on separate lines
            elif line.startswith('"') and not ':' in line and current_key:
                if isinstance(properties.get(current_key), list):
                    clean_value = line.strip('"').rstrip(',')
                    if clean_value:
                        properties[current_key].append(clean_value)
            
            # Handle array closing
            elif line.strip() in [']', '],']:
                current_key = None
        
        # Convert to JSON string
        if properties:
            try:
                import json
                return json.dumps(properties, indent=2)
            except:
                return None
        
        return None
    
    def _clean_and_fix_json(self, text: str) -> str:
        """Clean and fix common JSON formatting issues"""
        # Remove extra whitespace and newlines at start/end
        cleaned = text.strip()
        
        # Remove non-JSON content
        lines = cleaned.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Skip obvious non-JSON content
            if any(skip in line.lower() for skip in [
                'graph.tips', 'request only returns', 'learn.microsoft',
                'to find out what', 'your app will need'
            ]):
                continue
            clean_lines.append(line)
        
        if not clean_lines:
            return None
            
        cleaned = '\n'.join(clean_lines)
        
        # Try to fix common issues
        if '"@odata.context"' in cleaned or '"@microsoft.graph.tips"' in cleaned:
            # This looks like a Graph API response, try to extract just the main object
            # Remove @odata and tips
            lines = [line for line in cleaned.split('\n') 
                    if not any(skip in line for skip in ['@odata', '@microsoft.graph.tips'])]
            cleaned = '\n'.join(lines)
        
        # Ensure it starts and ends with braces
        if not cleaned.startswith('{') and ':' in cleaned:
            cleaned = '{' + cleaned
        if not cleaned.endswith('}') and cleaned.count('{') > cleaned.count('}'):
            cleaned = cleaned + '}'
            
        return cleaned

    def execute_graph_query(self, query: str, description: str) -> Optional[Dict]:
        """Execute a single Graph API query"""
        print(f"\n📡 Executing: {description}")
        print(f"🔍 Query: {query}")
        
        try:
            # Navigate to Graph Explorer with pre-filled query
            graph_url = f"{self.base_url}?request={quote(query)}&method=GET&version=v1.0"
            
            print(f"🌐 Navigating to: {graph_url[:80]}...")
            self.driver.get(graph_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Look for and click the "Run query" button
            try:
                run_button_selectors = [
                    # New selectors based on the actual HTML structure
                    "span.___1ej4kmx.f22iagw.f122n59.fkln5zr",
                    "span[class*='___1ej4kmx'][class*='f22iagw']",
                    "button span:contains('Run query')",
                    # Fallback selectors
                    "button[data-testid='run-query-button']",
                    "button[aria-label='Run query']",
                    ".run-query-button",
                    "#run-query",
                    "button.ms-Button--primary"
                ]
                
                run_button = None
                for selector in run_button_selectors:
                    try:
                        if "contains" in selector:
                            continue  # Skip CSS :contains selectors as they're not valid
                        run_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        print(f"✅ Found run button with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if not run_button:
                    # Try finding by text using XPath
                    xpath_selectors = [
                        "//span[contains(text(), 'Run query')]",
                        "//button[contains(., 'Run query')]",
                        "//span[contains(@class, '___1ej4kmx') and contains(text(), 'Run query')]",
                        "//button[contains(text(), 'Run')]"
                    ]
                    
                    for xpath in xpath_selectors:
                        try:
                            run_button = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, xpath))
                            )
                            print(f"✅ Found run button with XPath: {xpath}")
                            break
                        except TimeoutException:
                            continue
                
                if run_button:
                    print("🖱️  Clicking run query button...")
                    # Scroll the button into view first
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
                    time.sleep(1)
                    
                    # Try clicking
                    try:
                        run_button.click()
                        print("✅ Successfully clicked run button")
                    except Exception as click_error:
                        print(f"⚠️  Regular click failed: {click_error}")
                        print("🔄 Trying JavaScript click...")
                        self.driver.execute_script("arguments[0].click();", run_button)
                        print("✅ JavaScript click completed")
                else:
                    print("❌ Could not find run button with any selector")
                    # Take a screenshot for debugging
                    try:
                        self.driver.save_screenshot("graph_explorer_debug.png")
                        print("📸 Screenshot saved as graph_explorer_debug.png")
                    except:
                        pass
                    return None
                
            except TimeoutException:
                print("⚠️  Could not find run button, trying manual approach...")
                # Press Enter as fallback
                try:
                    self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RETURN)
                    print("⌨️  Sent Enter key as fallback")
                except Exception as e:
                    print(f"❌ Enter key fallback failed: {e}")
                    return None
            
            # Wait for results (much shorter wait)
            print("⏳ Waiting for query results...")
            time.sleep(1)  # Very short initial wait
            
            # Quick check for loading completion
            try:
                print("🔄 Checking if loading completed...")
                # Don't wait long for spinner - just check quickly
                WebDriverWait(self.driver, 3).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".fui-Spinner"))
                )
                print("✅ Loading completed")
            except TimeoutException:
                print("⚠️  No spinner found or already completed")
            
            # Very short wait for results to render
            time.sleep(0.5)
            
            # Quick response detection - try multiple times with short waits
            print("🔍 Quick response detection...")
            response_text = None
            max_attempts = 5
            
            for attempt in range(max_attempts):
                # Try to find JSON content immediately
                quick_selectors = ["pre", "code", ".monaco-editor"]
                
                for selector in quick_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 20 and ('{' in text or '[' in text or '@odata' in text):
                                response_text = text
                                print(f"✅ Found response in {selector} (attempt {attempt + 1})")
                                break
                        if response_text:
                            break
                    except Exception:
                        continue
                
                if response_text:
                    break
                
                # Short wait before next attempt
                if attempt < max_attempts - 1:
                    time.sleep(0.5)
                    print(f"🔄 Attempt {attempt + 1}/{max_attempts}...")
            
            # If still no response, try the Response preview tab approach
            if not response_text:
                print("🔍 Trying Response preview tab...")
                try:
                    # Look for and click Response preview tab
                    response_tab_selectors = [
                        "//button[contains(text(), 'Response preview')]",
                        "//*[@role='tab'][contains(text(), 'Response')]"
                    ]
                    
                    for selector in response_tab_selectors:
                        try:
                            response_tab = WebDriverWait(self.driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            response_tab.click()
                            time.sleep(1)
                            break
                        except TimeoutException:
                            continue
                    
                    # Quick check after clicking tab
                    time.sleep(1)
                    for selector in ["pre", "code"]:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 20 and ('{' in text or '[' in text):
                                response_text = text
                                print("✅ Found response in tab")
                                break
                        if response_text:
                            break
                            
                except Exception as e:
                    print(f"⚠️  Tab approach failed: {e}")
            
            # Final comprehensive search if still nothing found
            if not response_text:
                print("🔍 Comprehensive search...")
                all_selectors = [
                    "div[role='tabpanel'] pre",
                    "div[role='tabpanel'] code", 
                    ".monaco-editor .view-lines",
                    ".monaco-editor",
                    ".response-content", 
                    ".json-response"
                ]
                
                for selector in all_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 20 and ('{' in text or '[' in text):
                                response_text = text
                                print(f"✅ Found response in comprehensive search: {selector}")
                                break
                        if response_text:
                            break
                    except Exception as e:
                        continue
            
            # If still no response, try XPath selectors for JSON content
            if not response_text:
                xpath_selectors = [
                    "//*[contains(text(), '{') and contains(text(), '}')]",
                    "//*[contains(text(), '@odata')]", 
                    "//*[contains(text(), 'displayName')]",
                    "//*[contains(text(), 'value')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 20 and '{' in text:
                                response_text = text
                                print(f"✅ Found JSON response with XPath")
                                break
                        if response_text:
                            break
                    except Exception as e:
                        continue
            
            if not response_text:
                print("⚠️  Could not extract JSON response")
                return None
            
            # Try to parse JSON
            try:
                response_data = json.loads(response_text)
                print(f"✅ Successfully collected data")
                
                # Handle different types of responses
                if isinstance(response_data, dict):
                    # Check for empty results (not an error!)
                    if 'value' in response_data:
                        value_list = response_data['value']
                        if isinstance(value_list, list) and len(value_list) == 0:
                            print(f"✅ Empty result for {description} (no data available) - this is normal")
                            return {"empty": True, "query": description, "message": f"No {description.lower()} data available"}
                        else:
                            print(f"✅ Found {len(value_list)} items in {description}")
                            return response_data
                    elif 'error' in response_data:
                        error_msg = response_data['error'].get('message', 'Unknown error')
                        print(f"⚠️  API Error for {description}: {error_msg}")
                        return {"error": True, "query": description, "message": error_msg}
                    elif not response_data:  # Empty dict
                        print(f"✅ Empty result for {description} - this is normal")
                        return {"empty": True, "query": description, "message": f"No {description.lower()} data available"}
                    else:
                        print(f"✅ Valid data for {description}: {type(response_data)}")
                        return response_data
                elif isinstance(response_data, list):
                    if len(response_data) == 0:
                        print(f"✅ Empty list for {description} - this is normal")
                        return {"empty": True, "query": description, "message": f"No {description.lower()} data available"}
                    else:
                        print(f"✅ Found {len(response_data)} items in {description}")
                        return response_data
                else:
                    print(f"✅ Valid data for {description}: {type(response_data)}")
                    return response_data
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON parsing error: {e}")
                print(f"🔍 Response text preview: {response_text[:100]}...")
                
                # Try multiple JSON extraction strategies
                json_extraction_attempts = [
                    # Strategy 1: Find JSON between first { and last }
                    lambda t: t[t.find('{'):t.rfind('}') + 1] if '{' in t and '}' in t else None,
                    # Strategy 2: Find JSON between first [ and last ]
                    lambda t: t[t.find('['):t.rfind(']') + 1] if '[' in t and ']' in t else None,
                    # Strategy 3: Remove common prefixes/suffixes and wrap in braces
                    lambda t: '{' + t.strip().strip('`').strip('"').strip("'") + '}' if not t.strip().startswith('{') and ':' in t else t.strip(),
                    # Strategy 4: Split by lines and reconstruct JSON
                    lambda t: self._reconstruct_json_from_lines(t) if '\n' in t else None,
                    # Strategy 5: Clean and attempt to fix formatting
                    lambda t: self._clean_and_fix_json(t)
                ]
                
                for i, extract_func in enumerate(json_extraction_attempts):
                    try:
                        json_part = extract_func(response_text)
                        if json_part and json_part != response_text and len(json_part.strip()) > 5:
                            print(f"🔧 Trying extraction strategy {i+1}...")
                            response_data = json.loads(json_part)
                            
                            # Validate that we got meaningful data, not just empty structures
                            if isinstance(response_data, dict):
                                # For dictionaries, check if they have meaningful content
                                if len(response_data) > 1 or (len(response_data) == 1 and '@odata.context' not in response_data):
                                    print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                    return response_data
                                elif len(response_data) == 0:
                                    print(f"⚠️  Strategy {i+1} returned empty dict - trying next")
                                    continue
                                else:
                                    # Single key dictionary - check if it's meaningful
                                    first_key = list(response_data.keys())[0]
                                    if first_key != '@odata.context':
                                        print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                        return response_data
                                    else:
                                        print(f"⚠️  Strategy {i+1} returned only metadata - trying next")
                                        continue
                            elif isinstance(response_data, list):
                                # For lists, check if they have content
                                if len(response_data) > 0:
                                    print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                    return response_data
                                else:
                                    print(f"⚠️  Strategy {i+1} returned empty list - trying next")
                                    continue
                            else:
                                print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                return response_data
                    except (json.JSONDecodeError, AttributeError, TypeError) as e:
                        print(f"⚠️  Strategy {i+1} failed: {e}")
                        continue
                
                print("❌ Could not parse JSON response with any strategy")
                print(f"📝 Raw response (first 500 chars): {response_text[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return None

    def collect_all_data(self) -> Dict[str, Any]:
        """Collect all MyGraph data automatically"""
        print("\n🎯 Starting Automated Data Collection")
        print("=" * 50)
        
        # Define all queries to execute
        queries = [
            {
                "key": "profile",
                "query": "me",
                "description": "User Profile"
            },
            {
                "key": "manager",
                "query": "me/manager",
                "description": "Manager Information"
            },
            {
                "key": "direct_reports",
                "query": "me/directReports",
                "description": "Direct Reports"
            },
            {
                "key": "calendar_events",
                "query": f"me/calendarView?startDateTime={datetime.now().isoformat()}Z&endDateTime={(datetime.now() + timedelta(days=30)).isoformat()}Z",
                "description": "Calendar Events (Next 30 days)"
            },
            {
                "key": "recent_files",
                "query": "me/drive/recent",
                "description": "Recent Files"
            },
            {
                "key": "mail_folders",
                "query": "me/mailFolders",
                "description": "Mail Folders"
            },
            {
                "key": "groups",
                "query": "me/memberOf",
                "description": "Group Memberships"
            },
            {
                "key": "contacts",
                "query": "me/contacts?$top=20",
                "description": "Contacts (Top 20)"
            }
        ]
        
        collected_data = {}
        successful_queries = 0
        
        for query_info in queries:
            try:
                data = self.execute_graph_query(query_info["query"], query_info["description"])
                if data:
                    # Ensure data is properly parsed (not a string)
                    if isinstance(data, str):
                        try:
                            # Try to parse if it's a JSON string
                            parsed_data = json.loads(data)
                            collected_data[query_info["key"]] = parsed_data
                            print(f"🔧 Parsed string data for {query_info['key']}")
                        except json.JSONDecodeError:
                            print(f"⚠️  Invalid JSON string for {query_info['key']}: {data[:100]}...")
                            continue
                    else:
                        collected_data[query_info["key"]] = data
                    successful_queries += 1
                else:
                    print(f"⚠️  No data collected for {query_info['key']}")
                
                # Small delay between queries
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Failed to collect {query_info['key']}: {e}")
        
        print(f"\n📊 Data Collection Summary:")
        successful_queries = 0
        empty_results = 0
        error_results = 0
        
        for key, data in collected_data.items():
            if isinstance(data, dict):
                if data.get('empty'):
                    empty_results += 1
                    print(f"   📭 {key}: Empty (no data available)")
                elif data.get('error'):
                    error_results += 1
                    print(f"   ❌ {key}: Error - {data.get('message', 'Unknown error')}")
                else:
                    successful_queries += 1
                    if 'value' in data and isinstance(data['value'], list):
                        print(f"   ✅ {key}: {len(data['value'])} items")
                    else:
                        print(f"   ✅ {key}: Data collected")
            else:
                successful_queries += 1
                print(f"   ✅ {key}: Data collected")
        
        print(f"\n📈 Collection Results:")
        print(f"   ✅ Successful: {successful_queries}")
        print(f"   📭 Empty (normal): {empty_results}")
        print(f"   ❌ Errors: {error_results}")
        print(f"   📊 Total categories: {len(collected_data)}")
        
        return collected_data

    def process_collected_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw Graph data into MyGraph format"""
        print("\n🔄 Processing Data into MyGraph Format")
        print("=" * 40)
        
        # Debug: Print all data types first
        print("\n🔍 DEBUG: Data types analysis:")
        for key, data in raw_data.items():
            data_type = type(data).__name__
            if isinstance(data, dict):
                key_count = len(data.keys())
                print(f"   📊 {key}: {data_type} with {key_count} keys: {list(data.keys())[:3]}...")
            elif isinstance(data, list):
                print(f"   📊 {key}: {data_type} with {len(data)} items")
            elif isinstance(data, str):
                print(f"   📊 {key}: {data_type} content: '{data[:50]}...'")
            else:
                print(f"   📊 {key}: {data_type}")
        print()
        
        nodes = []
        links = []
        user_id = "urn:person:me:unknown"  # Fallback user ID
        
        # Process profile data
        if "profile" in raw_data:
            profile = raw_data["profile"]
            
            # Handle different data formats
            if isinstance(profile, list) and len(profile) > 0:
                # Take first item if it's a list
                profile = profile[0]
            
            if isinstance(profile, dict):
                # Dictionary response (expected)
                user_id = f"urn:person:me:{profile.get('mail', 'unknown')}"
                
                nodes.append({
                    "id": user_id,
                    "type": "person",
                    "properties": {
                        "name": profile.get('displayName'),
                        "email": profile.get('mail'),
                        "title": profile.get('jobTitle'),
                        "department": profile.get('department'),
                        "office": profile.get('officeLocation'),
                        "phone": profile.get('businessPhones', [None])[0] if profile.get('businessPhones') else None
                    },
                    "prov": {
                        "source": "graph.me",
                        "fetched_at": datetime.now().isoformat(),
                        "confidence": 1.0
                    }
                })
                print(f"✅ Processed user profile: {profile.get('displayName')}")
            else:
                print(f"❌ Invalid profile data format: {type(profile).__name__}")
                return None
        
        # Process manager data
        if "manager" in raw_data:
            manager = raw_data["manager"]
            
            # Handle different data formats
            if isinstance(manager, list) and len(manager) > 0:
                # Take first item if it's a list
                manager = manager[0]
            
            if isinstance(manager, dict):
                # Dictionary response
                if manager and not manager.get('empty') and not manager.get('error') and 'displayName' in manager:
                    manager_id = f"urn:person:manager:{manager.get('mail', 'unknown')}"
                    
                    nodes.append({
                        "id": manager_id,
                        "type": "person",
                        "properties": {
                            "name": manager.get('displayName'),
                            "email": manager.get('mail'),
                            "title": manager.get('jobTitle'),
                            "role": "manager"
                        },
                        "prov": {
                            "source": "graph.me.manager",
                            "fetched_at": datetime.now().isoformat(),
                            "confidence": 0.9
                        }
                    })
                    
                    # Create reporting relationship
                    links.append({
                        "source": user_id,
                        "target": manager_id,
                        "type": "REPORTS_TO",
                        "properties": {},
                        "prov": {
                            "source": "graph.me.manager",
                            "confidence": 0.9
                        }
                    })
                    
                    print(f"✅ Processed manager: {manager.get('displayName')}")
                elif manager and manager.get('empty'):
                    print("✅ No manager data (this is normal for top-level roles)")
                elif manager and manager.get('error'):
                    print(f"⚠️  Manager data error: {manager.get('message')}")
                else:
                    print("⚠️  No manager data")
            else:
                print(f"⚠️  Unexpected manager data format: {type(manager).__name__}")
        
        # Process direct reports
        if "direct_reports" in raw_data:
            reports = raw_data["direct_reports"]
            if isinstance(reports, list):
                # Direct list response
                for report in reports:
                    if report.get('displayName'):
                        report_id = f"urn:person:report:{report.get('mail', 'unknown')}"
                        
                        nodes.append({
                            "id": report_id,
                            "type": "person",
                            "properties": {
                                "name": report.get('displayName'),
                                "email": report.get('mail'),
                                "title": report.get('jobTitle'),
                                "role": "direct_report"
                            },
                            "prov": {
                                "source": "graph.me.directReports",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.9
                            }
                        })
                        
                        # Create reporting relationship
                        links.append({
                            "source": report_id,
                            "target": user_id,
                            "type": "REPORTS_TO",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.directReports",
                                "confidence": 0.9
                            }
                        })
                
                print(f"✅ Processed {len(reports)} direct reports")
            elif isinstance(reports, dict):
                # Dictionary response with metadata
                if reports and not reports.get('empty') and not reports.get('error') and 'value' in reports:
                    for report in reports['value']:
                        report_id = f"urn:person:report:{report.get('mail', 'unknown')}"
                        
                        nodes.append({
                            "id": report_id,
                            "type": "person",
                            "properties": {
                                "name": report.get('displayName'),
                                "email": report.get('mail'),
                                "title": report.get('jobTitle'),
                                "role": "direct_report"
                            },
                            "prov": {
                                "source": "graph.me.directReports",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.9
                            }
                        })
                        
                        # Create reporting relationship
                        links.append({
                            "source": report_id,
                            "target": user_id,
                            "type": "REPORTS_TO",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.directReports",
                                "confidence": 0.9
                            }
                        })
                    
                    print(f"✅ Processed {len(reports['value'])} direct reports")
                elif reports and reports.get('empty'):
                    print("✅ No direct reports (this is normal for many roles)")
                elif reports and reports.get('error'):
                    print(f"⚠️  Direct reports error: {reports.get('message')}")
                else:
                    print("⚠️  No direct reports data")
            else:
                print("⚠️  Unexpected direct reports data format")
        
        # Process calendar events
        if "calendar_events" in raw_data:
            events = raw_data["calendar_events"]
            event_count = 0
            
            if isinstance(events, list):
                # Direct list response
                for event in events[:15]:  # Limit to 15 recent events
                    if event.get('subject'):
                        event_id = f"urn:calendar:event:{event.get('id', f'event_{event_count}')}"
                        
                        nodes.append({
                            "id": event_id,
                            "type": "meeting",
                            "properties": {
                                "subject": event.get('subject'),
                                "start": event.get('start', {}).get('dateTime'),
                                "end": event.get('end', {}).get('dateTime'),
                                "organizer": event.get('organizer', {}).get('emailAddress', {}).get('name'),
                                "attendee_count": len(event.get('attendees', []))
                            },
                            "prov": {
                                "source": "graph.me.calendarView",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.8
                            }
                        })
                        
                        # Link user to meeting
                        links.append({
                            "source": user_id,
                            "target": event_id,
                            "type": "ATTENDS",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.calendarView",
                                "confidence": 0.8
                            }
                        })
                        event_count += 1
                        
                print(f"✅ Processed {event_count} calendar events")
            elif isinstance(events, dict) and events and 'value' in events:
                # Dictionary response with metadata
                for event in events['value'][:15]:  # Limit to 15 recent events
                    if event.get('subject'):
                        event_id = f"urn:calendar:event:{event.get('id', f'event_{event_count}')}"
                        
                        nodes.append({
                            "id": event_id,
                            "type": "meeting",
                            "properties": {
                                "subject": event.get('subject'),
                                "start": event.get('start', {}).get('dateTime'),
                                "end": event.get('end', {}).get('dateTime'),
                                "organizer": event.get('organizer', {}).get('emailAddress', {}).get('name'),
                                "attendee_count": len(event.get('attendees', []))
                            },
                            "prov": {
                                "source": "graph.me.calendarView",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.8
                            }
                        })
                        
                        # Link user to meeting
                        links.append({
                            "source": user_id,
                            "target": event_id,
                            "type": "ATTENDS",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.calendarView",
                                "confidence": 0.8
                            }
                        })
                        event_count += 1
                
                print(f"✅ Processed {event_count} calendar events")
            else:
                print("⚠️  No calendar events or unexpected format")
        
        # Process recent files
        if "recent_files" in raw_data:
            files = raw_data["recent_files"]
            file_count = 0
            
            if isinstance(files, list):
                # Direct list response
                for file_item in files[:10]:  # Limit to 10 recent files
                    if file_item.get('name'):
                        file_id = f"urn:file:{file_item.get('id', f'file_{file_count}')}"
                        
                        nodes.append({
                            "id": file_id,
                            "type": "document",
                            "properties": {
                                "name": file_item.get('name'),
                                "size": file_item.get('size'),
                                "lastModified": file_item.get('lastModifiedDateTime'),
                                "webUrl": file_item.get('webUrl')
                            },
                            "prov": {
                                "source": "graph.me.drive.recent",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.7
                            }
                        })
                        
                        # Link user to file
                        links.append({
                            "source": user_id,
                            "target": file_id,
                            "type": "OWNS",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.drive.recent",
                                "confidence": 0.7
                            }
                        })
                        file_count += 1
                        
                print(f"✅ Processed {file_count} recent files")
            elif isinstance(files, dict) and files and 'value' in files:
                # Dictionary response with metadata
                for file_item in files['value'][:10]:  # Limit to 10 recent files
                    file_id = f"urn:file:{file_item.get('id', f'file_{file_count}')}"
                    
                    nodes.append({
                        "id": file_id,
                        "type": "document",
                        "properties": {
                            "name": file_item.get('name'),
                            "size": file_item.get('size'),
                            "lastModified": file_item.get('lastModifiedDateTime'),
                            "webUrl": file_item.get('webUrl')
                        },
                        "prov": {
                            "source": "graph.me.drive.recent",
                            "fetched_at": datetime.now().isoformat(),
                            "confidence": 0.7
                        }
                    })
                    
                    # Link user to file
                    links.append({
                        "source": user_id,
                        "target": file_id,
                        "type": "OWNS",
                        "properties": {},
                        "prov": {
                            "source": "graph.me.drive.recent",
                            "confidence": 0.7
                        }
                    })
                    file_count += 1
                
                print(f"✅ Processed {file_count} recent files")
            else:
                print("⚠️  No recent files or unexpected format")
        
        # Process groups
        if "groups" in raw_data:
            groups = raw_data["groups"]
            group_count = 0
            
            if isinstance(groups, list):
                # Direct list response
                for group in groups[:10]:  # Limit to 10 groups
                    if group.get('displayName'):
                        group_id = f"urn:group:{group.get('id', f'group_{group_count}')}"
                        
                        nodes.append({
                            "id": group_id,
                            "type": "group",
                            "properties": {
                                "name": group.get('displayName'),
                                "description": group.get('description'),
                                "mail": group.get('mail')
                            },
                            "prov": {
                                "source": "graph.me.memberOf",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.8
                            }
                        })
                        
                        # Link user to group
                        links.append({
                            "source": user_id,
                            "target": group_id,
                            "type": "MEMBER_OF",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.memberOf",
                                "confidence": 0.8
                            }
                        })
                        group_count += 1
                        
                print(f"✅ Processed {group_count} group memberships")
            elif isinstance(groups, dict) and groups and 'value' in groups:
                # Dictionary response with metadata
                for group in groups['value'][:10]:  # Limit to 10 groups
                    group_id = f"urn:group:{group.get('id', f'group_{group_count}')}"
                    
                    nodes.append({
                        "id": group_id,
                        "type": "group",
                        "properties": {
                            "name": group.get('displayName'),
                            "description": group.get('description'),
                            "mail": group.get('mail')
                        },
                        "prov": {
                            "source": "graph.me.memberOf",
                            "fetched_at": datetime.now().isoformat(),
                            "confidence": 0.8
                        }
                    })
                    
                    # Link user to group
                    links.append({
                        "source": user_id,
                        "target": group_id,
                        "type": "MEMBER_OF",
                        "properties": {},
                        "prov": {
                            "source": "graph.me.memberOf",
                            "confidence": 0.8
                        }
                    })
                    group_count += 1
                
                print(f"✅ Processed {group_count} group memberships")
            else:
                print("⚠️  No groups or unexpected format")
        
        # Process contacts
        if "contacts" in raw_data:
            contacts = raw_data["contacts"]
            contact_count = 0
            
            if isinstance(contacts, list):
                # Direct list response
                for contact in contacts[:15]:  # Limit to 15 contacts
                    if contact.get('displayName'):
                        contact_id = f"urn:contact:{contact.get('id', f'contact_{contact_count}')}"
                        
                        nodes.append({
                            "id": contact_id,
                            "type": "contact",
                            "properties": {
                                "name": contact.get('displayName'),
                                "email": contact.get('emailAddresses', [{}])[0].get('address') if contact.get('emailAddresses') else None,
                                "company": contact.get('companyName'),
                                "title": contact.get('jobTitle')
                            },
                            "prov": {
                                "source": "graph.me.contacts",
                                "fetched_at": datetime.now().isoformat(),
                                "confidence": 0.7
                            }
                        })
                        
                        # Link user to contact
                        links.append({
                            "source": user_id,
                            "target": contact_id,
                            "type": "KNOWS",
                            "properties": {},
                            "prov": {
                                "source": "graph.me.contacts",
                                "confidence": 0.7
                            }
                        })
                        contact_count += 1
                        
                print(f"✅ Processed {contact_count} contacts")
            elif isinstance(contacts, dict):
                # Dictionary response with metadata
                if contacts and not contacts.get('empty') and not contacts.get('error') and 'value' in contacts:
                    for contact in contacts['value'][:15]:  # Limit to 15 contacts
                        if contact.get('displayName'):
                            contact_id = f"urn:contact:{contact.get('id', f'contact_{contact_count}')}"
                            
                            nodes.append({
                                "id": contact_id,
                                "type": "contact",
                                "properties": {
                                    "name": contact.get('displayName'),
                                    "email": contact.get('emailAddresses', [{}])[0].get('address') if contact.get('emailAddresses') else None,
                                    "company": contact.get('companyName'),
                                    "title": contact.get('jobTitle')
                                },
                                "prov": {
                                    "source": "graph.me.contacts",
                                    "fetched_at": datetime.now().isoformat(),
                                    "confidence": 0.7
                                }
                            })
                            
                            # Link user to contact
                            links.append({
                                "source": user_id,
                                "target": contact_id,
                                "type": "KNOWS",
                                "properties": {},
                                "prov": {
                                    "source": "graph.me.contacts",
                                    "confidence": 0.7
                                }
                            })
                            contact_count += 1
                    
                    print(f"✅ Processed {contact_count} contacts")
                elif contacts and contacts.get('empty'):
                    print("✅ No contacts (this is normal for some users)")
                elif contacts and contacts.get('error'):
                    print(f"⚠️  Contacts error: {contacts.get('message')}")
                else:
                    print("⚠️  No contacts data")
            else:
                print("⚠️  Unexpected contacts data format")
        
        # Create final MyGraph structure
        mygraph_data = {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "source": "automated_graph_explorer_collection",
                "total_nodes": len(nodes),
                "total_links": len(links),
                "data_sources": list(raw_data.keys())
            }
        }
        
        print(f"\n📊 Processing Complete:")
        print(f"   📦 Total nodes: {len(nodes)}")
        print(f"   🔗 Total links: {len(links)}")
        
        return mygraph_data

    def update_html_file(self, mygraph_data: Dict[str, Any]) -> bool:
        """Update the MyGraph HTML file with new data"""
        print("\n🔄 Updating MyGraph HTML File")
        print("=" * 35)
        
        html_file = Path("docs/mygraph_explorer.html")
        if not html_file.exists():
            print("❌ MyGraph HTML file not found")
            return False
        
        try:
            # Read current HTML
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Create backup
            backup_file = f"docs/mygraph_explorer_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"💾 Backup created: {backup_file}")
            
            # Find and replace the data section
            start_marker = "const graph = {"
            start_idx = html_content.find(start_marker)
            if start_idx == -1:
                print("❌ Could not find data section in HTML")
                return False
            
            # Find the end of the graph object
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
            
            # Replace data section
            updated_html = html_content[:start_idx] + new_data + html_content[end_idx:]
            
            # Save updated HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print("✅ MyGraph HTML file updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update HTML file: {e}")
            return False

    def save_data_files(self, raw_data: Dict[str, Any], processed_data: Dict[str, Any]):
        """Save collected data to files"""
        print("\n💾 Saving Data Files")
        print("=" * 25)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw data
        raw_file = f"mygraph_raw_data_{timestamp}.json"
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f, indent=2)
        print(f"📄 Raw data saved: {raw_file}")
        
        # Save processed data
        processed_file = f"mygraph_processed_data_{timestamp}.json"
        with open(processed_file, 'w') as f:
            json.dump(processed_data, f, indent=2)
        print(f"📄 Processed data saved: {processed_file}")

    def run_full_automation(self, headless: bool = False) -> bool:
        """Run the complete automated pipeline"""
        print("🚀 AUTOMATED MYGRAPH PIPELINE STARTING")
        print("=" * 50)
        print(f"🕐 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Setup browser
            if not self.setup_browser(headless):
                print("❌ Browser setup failed")
                return False
            
            # Step 2: Wait for authentication (browser is already on Graph Explorer)
            if not self.wait_for_authentication():
                print("❌ Authentication failed or timed out")
                return False
            
            # Step 4: Collect data
            raw_data = self.collect_all_data()
            if not raw_data:
                print("❌ No data collected")
                return False
            
            # Step 5: Process data
            processed_data = self.process_collected_data(raw_data)
            
            # Step 6: Save data files
            self.save_data_files(raw_data, processed_data)
            
            # Step 7: Update HTML file
            html_updated = self.update_html_file(processed_data)
            
            # Step 8: Final summary
            print(f"\n🎊 AUTOMATION COMPLETE!")
            print("=" * 30)
            print(f"✅ Data collection: SUCCESS")
            print(f"✅ Data processing: SUCCESS")
            print(f"✅ HTML update: {'SUCCESS' if html_updated else 'FAILED'}")
            print(f"📊 Nodes collected: {len(processed_data['nodes'])}")
            print(f"🔗 Links created: {len(processed_data['links'])}")
            print(f"🕐 Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Automation failed: {e}")
            return False
        
        finally:
            # Cleanup
            if self.driver:
                print("\n🧹 Cleaning up browser...")
                self.driver.quit()

def main():
    """Main automation entry point"""
    print("🎯 MyGraph Automation Pipeline")
    print("Fully automated data collection and processing")
    print()
    
    # Create pipeline instance
    pipeline = AutomatedMyGraphPipeline()
    
    # Run automation
    success = pipeline.run_full_automation(headless=False)
    
    if success:
        print("\n🎉 SUCCESS! Your MyGraph has been updated with fresh data.")
        print("📂 Open docs/mygraph_explorer.html to view your updated organizational graph!")
    else:
        print("\n❌ Automation failed. Check the error messages above.")
        print("💡 You can still use the manual Graph Explorer method as a fallback.")

if __name__ == "__main__":
    main()