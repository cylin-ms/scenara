#!/usr/bin/env python3
"""
Manual Authentication Graph Explorer Extractor

Based on analysis of Graph Explorer UI structure and .cursorrules documented success patterns.
Allows user to authenticate manually, then executes collaboration analysis queries.

Key UI Elements Identified:
- Response Preview tab: button[value="Response preview"]
- Monaco Editor: .view-line elements with JSON content
- Sample groups: People, Outlook Calendar, Users categories
- Run button: Standard execution trigger

References:
- .cursorrules: "5/8 perfect extractions, 2/8 partial, 1/8 needs improvement"
- Working patterns: short waits (0.5s, 1s), quick response detection
- UI Analysis: Response preview tab in lower right panel confirmed
"""

import time
import json
import re
from datetime import datetime
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ManualAuthGraphExtractor:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.graph_url = "https://developer.microsoft.com/en-us/graph/graph-explorer"
        
        # Collaboration analysis queries based on .cursorrules success patterns
        self.collaboration_queries = [
            {
                "name": "People API - Microsoft ML Collaboration Rankings",
                "method": "GET",
                "url": "https://graph.microsoft.com/v1.0/me/people",
                "description": "Get collaboration-ranked people list to find Haidong Zhang vs false positives"
            },
            {
                "name": "Calendar Meetings Analysis",
                "method": "GET", 
                "url": "https://graph.microsoft.com/v1.0/me/calendar/events?$select=subject,organizer,attendees,start,end&$filter=start/dateTime ge '2024-01-01T00:00:00.000Z'",
                "description": "Analyze meeting patterns and attendee collaboration"
            },
            {
                "name": "Email Communication Patterns",
                "method": "GET",
                "url": "https://graph.microsoft.com/v1.0/me/messages?$select=from,toRecipients,subject,receivedDateTime&$top=100",
                "description": "Email-based collaboration frequency analysis"
            },
            {
                "name": "Recent Collaboration Items",
                "method": "GET",
                "url": "https://graph.microsoft.com/v1.0/me/insights/shared?$top=50",
                "description": "Documents and items shared in collaboration"
            },
            {
                "name": "Teams Chat Collaboration",
                "method": "GET",
                "url": "https://graph.microsoft.com/v1.0/me/chats?$expand=members&$top=50",
                "description": "Teams chat frequency for collaboration ranking"
            }
        ]
        
    def init_browser(self):
        """Initialize browser using proven approach from automated_mygraph_pipeline.py."""
        print("🌐 Setting up browser for Microsoft Graph Explorer...")
        
        # Try Edge first (better for Microsoft services) - exact same approach as automated_mygraph_pipeline.py
        try:
            print("🔵 Attempting Microsoft Edge...")
            options = webdriver.EdgeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Don't use headless for manual authentication
            
            self.driver = webdriver.Edge(options=options)
            self.driver.maximize_window()
            
            # Navigate to Graph Explorer (stay in this window!)
            print("🌐 Opening Graph Explorer with Edge...")
            self.driver.get(self.graph_url)
            
            print("✅ Edge browser setup successful")
            self.wait = WebDriverWait(self.driver, 30)
            return True
            
        except Exception as e:
            print(f"⚠️ Edge not available: {e}")
            print("🔄 Trying Chrome as fallback...")
            
            # Fallback to Chrome - exact same approach
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                # Don't use headless for manual authentication
                
                self.driver = webdriver.Chrome(options=options)
                self.driver.maximize_window()
                
                # Navigate to Graph Explorer (stay in this window!)
                print("🌐 Opening Graph Explorer with Chrome...")
                self.driver.get(self.graph_url)
                
                print("✅ Chrome browser setup successful")
                self.wait = WebDriverWait(self.driver, 30)
                return True
                
            except Exception as chrome_error:
                print(f"❌ Both Chrome and Edge failed: {chrome_error}")
                print("\n💡 Browser setup failed. Please ensure you have:")
                print("   • Microsoft Edge WebDriver, or")
                print("   • Chrome WebDriver")
                print("   • Selenium package: pip install selenium")
                return False
        
    def wait_for_manual_authentication(self):
        """Wait for user to manually authenticate using proven .cursorrules approach."""
        print("\n� AUTHENTICATION REQUIRED")
        print("=" * 50)
        print("1. � Complete Microsoft authentication in the browser")
        print("2. ✅ Ensure you're signed in to Graph Explorer")
        print("3. ⏳ Waiting for authentication confirmation...")
        print("4. 🔄 Will check every 5 seconds for successful login")
        
        try:
            # NOTE: Browser is already on Graph Explorer from init_browser()
            # DO NOT navigate to a new URL - this is the key difference!
            
            # Wait for initial page load
            time.sleep(3)
            
            # Use proven authentication detection from .cursorrules documented approach
            max_wait_time = 300  # 5 minutes
            check_interval = 5
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                try:
                    # Check if we can find elements that indicate successful auth
                    # Stay on current URL - don't check URL like the working version
                    
                    # Look for signed-in indicators (exact same as automated_mygraph_pipeline.py)
                    try:
                        WebDriverWait(self.driver, 2).until(
                            EC.any_of(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label*='Sign out']")),
                                EC.presence_of_element_located((By.CSS_SELECTOR, ".ms-Persona")),
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='persona']")),
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign out')]"))
                            )
                        )
                        print("✅ Authentication detected! Ready to collect data...")
                        # Give the UI a moment to fully stabilize after authentication
                        time.sleep(2)
                        return True
                    except TimeoutException:
                        pass
                    
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                    print(f"⏳ Still waiting... ({elapsed_time}/{max_wait_time}s)")
                    
                except Exception as e:
                    print(f"⚠️ Error during auth check: {e}")
                    time.sleep(check_interval)
                    elapsed_time += check_interval
            
            print("⏰ Authentication timeout reached")
            return False
                
        except Exception as e:
            print(f"❌ Error during authentication setup: {e}")
            return False
                
        except Exception as e:
            print(f"❌ Error during authentication setup: {e}")
            return False
    
    def execute_query(self, query_info):
        """Execute a collaboration query using URL parameters (proven .cursorrules approach)."""
        print(f"\n🔍 Executing: {query_info['name']}")
        print(f"📊 Purpose: {query_info['description']}")
        
        try:
            # KEY LEARNING FROM .cursorrules: Use URL parameters to pre-fill query!
            # This is how automated_mygraph_pipeline.py works successfully
            query_path = query_info['url'].replace('https://graph.microsoft.com/v1.0/', '')
            
            # Navigate to Graph Explorer with pre-filled query (THE PROVEN APPROACH!)
            graph_url = f"{self.graph_url}?request={quote(query_path)}&method=GET&version=v1.0"
            
            print(f"🌐 Navigating to: {graph_url[:80]}...")
            self.driver.get(graph_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Click Run button using proven approach from automated_mygraph_pipeline.py
            print("🖱️ Looking for run query button...")
            
            try:
                run_button_selectors = [
                    # Proven selectors from automated_mygraph_pipeline.py
                    "span.___1ej4kmx.f22iagw.f122n59.fkln5zr",
                    "span[class*='___1ej4kmx'][class*='f22iagw']",
                    "button[data-testid='run-query-button']",
                    "button[aria-label='Run query']",
                    ".run-query-button",
                    "#run-query",
                    "button.ms-Button--primary"
                ]
                
                run_button = None
                for selector in run_button_selectors:
                    try:
                        run_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        print(f"✅ Found run button with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if not run_button:
                    # Try finding by text using XPath (proven approach)
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
                    print("🖱️ Clicking run query button...")
                    # Scroll the button into view first
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
                    time.sleep(1)
                    
                    # Try clicking
                    try:
                        run_button.click()
                        print("✅ Successfully clicked run button")
                    except Exception as click_error:
                        print(f"⚠️ Regular click failed: {click_error}")
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
                    
            except Exception as e:
                print(f"❌ Error finding run button: {e}")
                # Press Enter as fallback
                try:
                    self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RETURN)
                    print("⌨️ Sent Enter key as fallback")
                except Exception as fallback_error:
                    print(f"❌ Enter key fallback failed: {fallback_error}")
                    return None
            
            # Wait for results with proven timing
            print("⏳ Waiting for query results...")
            time.sleep(1)  # Short initial wait like automated_mygraph_pipeline.py
            
            # Quick check for loading completion
            try:
                print("🔄 Checking if loading completed...")
                WebDriverWait(self.driver, 3).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".fui-Spinner"))
                )
                print("✅ Loading completed")
            except TimeoutException:
                print("⚠️ No spinner found or already completed")
            
            print("✅ Query executed successfully")
            
            # Wait for response with quick detection (from .cursorrules pattern)
            time.sleep(1)
            
            # Extract response from Response Preview tab with pagination support
            response_data = self.extract_response_content()
            
            if response_data:
                print(f"✅ Response extracted: {len(str(response_data))} characters")
                
                # Check for pagination (@odata.nextLink)
                if isinstance(response_data, dict) and '@odata.nextLink' in response_data:
                    print("📄 Pagination detected - collecting all pages...")
                    response_data = self._collect_all_pages(response_data)
                
                return response_data
            else:
                print("⚠️ No response content found")
                return None
                
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return None
    
    def _check_for_pagination(self):
        """Check if response has @odata.nextLink pagination."""
        try:
            # Look for pagination indicators in the UI
            pagination_indicators = [
                "//div[contains(text(), '@odata.nextLink')]",
                "//a[contains(text(), 'nextLink')]", 
                "//button[contains(text(), 'next')]",
                "//*[contains(text(), 'Click here to follow the link')]"
            ]
            
            for xpath in pagination_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element:
                        print(f"📄 Found pagination indicator: @odata.nextLink")
                        return True
                except NoSuchElementException:
                    continue
            
            return False
        except Exception as e:
            print(f"⚠️ Error checking pagination: {e}")
            return False
    
    def extract_response_content(self):
        """Extract JSON response using proven 5-strategy approach from .cursorrules."""
        print("🔍 Extracting response content using proven strategies...")
        
        # Check for pagination FIRST
        has_pagination = self._check_for_pagination()
        if has_pagination:
            print("📄 Response has pagination - will extract first page only (nextLink handling TBD)")
        
        
        # Strategy 1: Target Response Preview tab (confirmed from HTML analysis)
        try:
            response_tab = self.driver.find_element(By.XPATH, "//button[@value='Response preview' and @aria-selected='true']")
            print("✅ Response Preview tab located")
        except NoSuchElementException:
            print("⚠️ Response Preview tab not active, trying to click it")
            try:
                response_tab = self.driver.find_element(By.XPATH, "//button[@value='Response preview']")
                response_tab.click()
                time.sleep(0.5)
            except NoSuchElementException:
                print("❌ Response Preview tab not found")
        
        # Get response text from multiple sources
        response_text = self._get_response_text()
        if not response_text:
            print("❌ No response text found")
            return None
        
        print(f"🔍 Response text preview: {response_text[:100]}...")
        
        # DEBUG: Save raw response
        with open('/tmp/raw_response.txt', 'w', encoding='utf-8') as f:
            f.write(response_text)
        print(f"💾 Saved raw response to /tmp/raw_response.txt ({len(response_text)} bytes)")
        
        # Try parsing as JSON first
        try:
            response_data = json.loads(response_text)
            print(f"✅ Direct JSON parsing successful ({len(str(response_data))} chars)")
            return response_data
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error: {e}")
            
            # Use proven 5-strategy extraction from automated_mygraph_pipeline.py
            # KEY FIX: Clean control characters FIRST to avoid "Invalid control character" errors
            # Monaco editor embeds actual newlines/tabs in the displayed JSON text
            json_extraction_attempts = [
                # Strategy 1: Clean ALL control chars (newlines, tabs, carriage returns) then parse
                lambda t: (lambda cleaned: json.loads(cleaned))(t.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')),
                # Strategy 2: Find JSON between first { and last }, clean control chars
                lambda t: (lambda cleaned: cleaned[cleaned.find('{'):cleaned.rfind('}') + 1] if '{' in cleaned and '}' in cleaned else None)(t.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')),
                # Strategy 3: Find JSON between first [ and last ], clean control chars
                lambda t: (lambda cleaned: cleaned[cleaned.find('['):cleaned.rfind(']') + 1] if '[' in cleaned and ']' in cleaned else None)(t.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')),
                # Strategy 4: Remove common prefixes/suffixes and wrap in braces
                lambda t: '{' + t.strip().strip('`').strip('"').strip("'") + '}' if not t.strip().startswith('{') and ':' in t else t.strip(),
                # Strategy 5: Clean and attempt to fix formatting
                lambda t: self._clean_and_fix_json(t)
            ]
            
            for i, extract_func in enumerate(json_extraction_attempts):
                try:
                    json_part = extract_func(response_text)
                    if json_part and json_part != response_text and len(json_part.strip()) > 5:
                        print(f"� Trying extraction strategy {i+1}...")
                        response_data = json.loads(json_part)
                        
                        # Validate that we got meaningful data (from automated_mygraph_pipeline.py)
                        if isinstance(response_data, dict):
                            if len(response_data) > 1 or (len(response_data) == 1 and '@odata.context' not in response_data):
                                print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                return response_data
                            elif len(response_data) == 0:
                                print(f"⚠️ Strategy {i+1} returned empty dict - trying next")
                                continue
                            else:
                                first_key = list(response_data.keys())[0]
                                if first_key != '@odata.context':
                                    print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                    return response_data
                                else:
                                    print(f"⚠️ Strategy {i+1} returned only metadata - trying next")
                                    continue
                        elif isinstance(response_data, list):
                            if len(response_data) > 0:
                                print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                                return response_data
                            else:
                                print(f"⚠️ Strategy {i+1} returned empty list - trying next")
                                continue
                        else:
                            print(f"✅ Extracted JSON with strategy {i+1} ({len(str(response_data))} chars)")
                            return response_data
                except (json.JSONDecodeError, AttributeError, TypeError) as e:
                    print(f"⚠️ Strategy {i+1} failed: {e}")
                    continue
            
            print("❌ Could not parse JSON response with any strategy")
            return None
    
    def _collect_all_pages(self, first_page_data):
        """Collect all paginated results by following @odata.nextLink."""
        all_items = first_page_data.get('value', [])
        page_count = 1
        print(f"📋 Page 1: Found {len(all_items)} items")
        
        # Check if there's a nextLink indicator in the UI
        max_pages = 10  # Safety limit
        current_page = first_page_data
        
        while '@odata.nextLink' in current_page and page_count < max_pages:
            try:
                print(f"🔗 Found @odata.nextLink - checking for pagination UI...")
                
                # Look for the "Click here to follow the link" element
                try:
                    next_link_element = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Click here to follow the link')]"))
                    )
                    print("🖱️ Clicking nextLink to load page {}...".format(page_count + 1))
                    next_link_element.click()
                    
                    # Wait for new results to load
                    time.sleep(2)
                    
                    # Extract next page
                    next_page_data = self.extract_response_content()
                    if next_page_data and isinstance(next_page_data, dict):
                        new_items = next_page_data.get('value', [])
                        all_items.extend(new_items)
                        page_count += 1
                        print(f"📋 Page {page_count}: Found {len(new_items)} items (total: {len(all_items)})")
                        current_page = next_page_data
                    else:
                        print("⚠️ Could not extract next page data")
                        break
                        
                except TimeoutException:
                    print("⚠️ No clickable nextLink found in UI - pagination complete")
                    break
                    
            except Exception as e:
                print(f"⚠️ Error during pagination: {e}")
                break
        
        # Update the first page data with all collected items
        result = first_page_data.copy()
        result['value'] = all_items
        if '@odata.nextLink' in result:
            del result['@odata.nextLink']  # Remove since we've collected all
        
        print(f"✅ Pagination complete: {len(all_items)} total items across {page_count} page(s)")
        return result
    
    def _get_response_text(self):
        """Get response text using proven quick detection approach from automated_mygraph_pipeline.py."""
        # Very short wait for results to render
        time.sleep(0.5)
        
        # CRITICAL FIX: Try to get Monaco editor's actual value via JavaScript first
        try:
            print("🔍 Attempting Monaco editor API extraction...")
            # Monaco editor stores the actual content in its model
            monaco_value = self.driver.execute_script("""
                try {
                    // Check if monaco is available
                    if (typeof monaco === 'undefined') {
                        return 'MONACO_UNDEFINED';
                    }
                    
                    // Try multiple approaches to get the content
                    
                    // Approach 1: Get all editor instances
                    var editors = monaco.editor.getEditors();
                    if (editors && editors.length > 0) {
                        for (var i = 0; i < editors.length; i++) {
                            var value = editors[i].getValue();
                            if (value && value.length > 20) {
                                return value;
                            }
                        }
                    }
                    
                    // Approach 2: Try to find editor in DOM
                    var editorElements = document.querySelectorAll('.monaco-editor');
                    for (var i = 0; i < editorElements.length; i++) {
                        var editor = editorElements[i];
                        // Check if this element has a Monaco editor attached
                        if (editor.classList.contains('monaco-editor')) {
                            // Try to get the model
                            var models = monaco.editor.getModels();
                            if (models && models.length > 0) {
                                for (var j = 0; j < models.length; j++) {
                                    var modelValue = models[j].getValue();
                                    if (modelValue && modelValue.length > 20) {
                                        return modelValue;
                                    }
                                }
                            }
                        }
                    }
                    
                    return 'NO_CONTENT_FOUND';
                } catch (e) {
                    return 'ERROR: ' + e.message;
                }
            """)
            
            if monaco_value and not monaco_value.startswith('MONACO_') and not monaco_value.startswith('NO_') and not monaco_value.startswith('ERROR') and not monaco_value.startswith('EMPTY') and len(monaco_value) > 20:
                print(f"✅ Extracted JSON via Monaco editor API ({len(monaco_value)} bytes)")
                return monaco_value
            else:
                print(f"⚠️ Monaco API returned: {monaco_value}, falling back to DOM extraction")
        except Exception as e:
            print(f"⚠️ Monaco API extraction failed: {e}, trying DOM extraction")
        
        # Quick response detection - try multiple times with short waits (PROVEN APPROACH!)
        print("🔍 Quick response detection via DOM...")
        response_text = None
        max_attempts = 5
        
        for attempt in range(max_attempts):
            # Try to find JSON content immediately
            quick_selectors = ["pre", "code", ".monaco-editor"]
            
            for selector in quick_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()  # KEY: Use .text not .get_attribute('textContent')!
                        if text and len(text) > 20 and ('{' in text or '[' in text or '@odata' in text):
                            response_text = text
                            print(f"✅ Found response in {selector} (attempt {attempt + 1})")
                            return response_text
                except Exception:
                    continue
            
            # Short wait before next attempt
            if attempt < max_attempts - 1:
                time.sleep(0.5)
                print(f"🔄 Attempt {attempt + 1}/{max_attempts}...")
        
        # If still no response, try comprehensive search
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
                            return response_text
                except Exception:
                    continue
        
        # Try XPath selectors for JSON content
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
                            return response_text
                except Exception:
                    continue
        
        return response_text
    
    def _reconstruct_json_from_lines(self, text: str) -> str:
        """Reconstruct JSON from Monaco editor lines (proven from automated_mygraph_pipeline.py)."""
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
                                except ValueError:
                                    properties[key] = value_str
                except Exception:
                    continue
        
        return json.dumps(properties) if properties else None
    
    def _clean_and_fix_json(self, text: str) -> str:
        """Clean and fix common JSON formatting issues (proven from automated_mygraph_pipeline.py)."""
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
        """Extract content from Monaco editor view lines (proven approach)."""
        try:
            # Look for Monaco editor container
            monaco_container = self.driver.find_element(By.CLASS_NAME, "monaco-editor")
            view_lines = monaco_container.find_elements(By.CLASS_NAME, "view-line")
            
            if view_lines:
                content_lines = []
                for line in view_lines:
                    line_text = line.get_attribute('textContent') or line.text
                    if line_text.strip():
                        content_lines.append(line_text)
                
                full_content = '\n'.join(content_lines)
                print(f"📝 Monaco content extracted: {len(content_lines)} lines")
                return full_content
        except Exception as e:
            print(f"Monaco extraction error: {e}")
        return None
    
    def _extract_text_content(self):
        """Fallback text extraction."""
        try:
            # Get page text and look for JSON
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            json_start = page_text.find('{')
            if json_start != -1:
                # Try to find the end of JSON
                brace_count = 0
                json_end = json_start
                for i, char in enumerate(page_text[json_start:], json_start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i
                            break
                
                potential_json = page_text[json_start:json_end+1]
                return potential_json
        except Exception:
            pass
        return None
    
    def _is_valid_json_response(self, content):
        """Validate if content looks like a valid Graph API response."""
        if not content or len(content) < 10:
            return False
        
        # Check for JSON structure
        if not ('{' in content or '[' in content):
            return False
        
        # Try to parse as JSON
        try:
            json.loads(content)
            return True
        except:
            # Might be partial JSON, check for Graph API indicators
            graph_indicators = [
                '@odata.context',
                'value',
                'displayName',
                'userPrincipalName',
                'microsoft.com'
            ]
            return any(indicator in content for indicator in graph_indicators)
    
    def analyze_collaboration_data(self, all_responses):
        """Analyze extracted collaboration data for insights."""
        print("\n📊 COLLABORATION ANALYSIS RESULTS")
        print("=" * 60)
        
        collaboration_ranking = {}
        
        for query_name, response in all_responses.items():
            if not response:
                continue
                
            print(f"\n🔍 Analyzing: {query_name}")
            
            try:
                if isinstance(response, str):
                    data = json.loads(response)
                else:
                    data = response
                
                if query_name == "People API - Microsoft ML Collaboration Rankings":
                    # Analyze People API results for Haidong Zhang
                    if 'value' in data:
                        people = data['value']
                        print(f"📋 Found {len(people)} ranked people")
                        
                        for i, person in enumerate(people[:10]):  # Top 10
                            name = person.get('displayName', 'Unknown')
                            email = person.get('userPrincipalName', person.get('emailAddresses', [{}])[0].get('address', ''))
                            score = person.get('relevanceScore', 0)
                            
                            print(f"  {i+1}. {name} ({email}) - Score: {score}")
                            
                            # Check for Haidong Zhang specifically
                            if 'haidong' in name.lower() or 'zhang' in name.lower():
                                collaboration_ranking['haidong_zhang_rank'] = i + 1
                                collaboration_ranking['haidong_zhang_score'] = score
                                print(f"  ⭐ FOUND HAIDONG ZHANG at rank #{i+1}!")
                
                elif "Calendar" in query_name:
                    # Analyze meeting patterns
                    if 'value' in data:
                        meetings = data['value']
                        print(f"📅 Found {len(meetings)} meetings")
                        
                        # Count attendee collaborations
                        attendee_counts = {}
                        for meeting in meetings:
                            attendees = meeting.get('attendees', [])
                            for attendee in attendees:
                                email = attendee.get('emailAddress', {}).get('address', '')
                                name = attendee.get('emailAddress', {}).get('name', '')
                                if email:
                                    attendee_counts[email] = attendee_counts.get(email, 0) + 1
                        
                        # Show top collaborators
                        sorted_attendees = sorted(attendee_counts.items(), key=lambda x: x[1], reverse=True)
                        print("📊 Top meeting collaborators:")
                        for email, count in sorted_attendees[:5]:
                            print(f"  • {email}: {count} meetings")
                
                elif "Email" in query_name:
                    # Analyze email patterns
                    if 'value' in data:
                        emails = data['value']
                        print(f"📧 Found {len(emails)} emails")
                        
                        # Count email collaborations
                        sender_counts = {}
                        for email in emails:
                            sender = email.get('from', {}).get('emailAddress', {}).get('address', '')
                            if sender:
                                sender_counts[sender] = sender_counts.get(sender, 0) + 1
                        
                        # Show top email collaborators
                        sorted_senders = sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)
                        print("📊 Top email collaborators:")
                        for sender, count in sorted_senders[:5]:
                            print(f"  • {sender}: {count} emails")
                
            except Exception as e:
                print(f"❌ Analysis error for {query_name}: {e}")
        
        # Summary
        print(f"\n🎯 COLLABORATION RANKING SUMMARY")
        print("=" * 40)
        if 'haidong_zhang_rank' in collaboration_ranking:
            print(f"✅ Haidong Zhang found at rank #{collaboration_ranking['haidong_zhang_rank']}")
            print(f"📊 Relevance score: {collaboration_ranking['haidong_zhang_score']}")
        else:
            print("❌ Haidong Zhang not found in top rankings")
            print("💡 This could indicate genuine collaboration vs false positive")
        
        return collaboration_ranking
    
    def run_collaboration_analysis(self):
        """Main execution method for collaboration analysis."""
        print("🚀 MANUAL AUTHENTICATION GRAPH COLLABORATION EXTRACTOR")
        print("=" * 65)
        print("📋 Purpose: Extract Microsoft Graph collaboration data")
        print("🎯 Goal: Find genuine Haidong Zhang collaboration vs false positives")
        print("=" * 65)
        
        if not self.init_browser():
            print("❌ Browser initialization failed")
            return None
        
        try:
            # Wait for manual authentication using proven approach
            if not self.wait_for_manual_authentication():
                print("❌ Authentication setup failed")
                return None
            
            # Execute all collaboration queries
            all_responses = {}
            
            print(f"\n🎯 Starting query execution - {len(self.collaboration_queries)} queries to run")
            
            for query in self.collaboration_queries:
                print(f"\n" + "="*60)
                response = self.execute_query(query)
                all_responses[query['name']] = response
                
                # Brief pause between queries
                time.sleep(0.5)
            
            # Analyze the collected data
            analysis_results = self.analyze_collaboration_data(all_responses)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/evaluation_results/graph_collaboration_analysis_{timestamp}.json"
            
            results = {
                'timestamp': timestamp,
                'queries_executed': list(all_responses.keys()),
                'responses': all_responses,
                'collaboration_analysis': analysis_results,
                'extraction_method': 'manual_authentication'
            }
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"\n💾 Results saved to: {output_file}")
            print("✅ Collaboration analysis completed successfully!")
            
            return results
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return None
        finally:
            if self.driver:
                print("🔒 Closing browser...")
                self.driver.quit()

def main():
    """Run the manual authentication Graph Explorer extraction."""
    extractor = ManualAuthGraphExtractor()
    results = extractor.run_collaboration_analysis()
    
    if results:
        print("\n🎉 SUCCESS: Collaboration data extracted and analyzed!")
        return True
    else:
        print("\n❌ FAILED: Unable to complete collaboration analysis")
        return False

if __name__ == "__main__":
    main()