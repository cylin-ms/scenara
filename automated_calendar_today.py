#!/usr/bin/env python3
"""
Automated Microsoft Graph Explorer Calendar Access
Automates the browser interaction to fetch today's meetings via Graph Explorer
"""

import os
import sys
import json
import time
import zoneinfo
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from urllib.parse import quote
import subprocess

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.service import Service
except ImportError:
    print("❌ Required packages not installed. Installing...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium', 'webdriver-manager'])
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.service import Service

# Constants
GRAPH_EXPLORER_URL = "https://developer.microsoft.com/en-us/graph/graph-explorer"
WAIT_TIMEOUT = 30

def setup_browser(headless: bool = False) -> webdriver.Edge:
    """Setup Microsoft Edge browser with appropriate options."""
    edge_options = Options()
    
    if headless:
        edge_options.add_argument("--headless")
    
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    # Enable Microsoft authentication integration
    edge_options.add_argument("--enable-features=WebAuthentication")
    edge_options.add_argument("--enable-web-auth-deprecated-mojo-testing-api")
    
    # Enable logging for debugging
    edge_options.add_argument("--enable-logging")
    edge_options.add_argument("--log-level=0")
    
    try:
        # Auto-download and setup EdgeDriver
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        return driver
    except Exception as e:
        print(f"❌ Failed to setup Microsoft Edge browser: {e}")
        print("💡 Please ensure Microsoft Edge is installed:")
        print("   Download from: https://www.microsoft.com/en-us/edge")
        raise


def build_calendar_query() -> str:
    """Build the Graph API calendar query for today."""
    # Today's date range in UTC
    today = datetime.now(timezone.utc).date()
    start_datetime = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_datetime = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    start_iso = start_datetime.isoformat().replace('+00:00', 'Z')
    end_iso = end_datetime.isoformat().replace('+00:00', 'Z')
    
    query = f"/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}&$orderby=start/dateTime"
    return query


def wait_for_authentication(driver: webdriver.Edge, wait: WebDriverWait) -> bool:
    """Wait for user to complete Microsoft authentication."""
    print("🔐 Waiting for Microsoft authentication...")
    print("   Please sign in when the browser opens")
    
    # Wait for either the Graph Explorer interface or login completion
    auth_completed = False
    max_attempts = 60  # 5 minutes timeout
    
    for attempt in range(max_attempts):
        try:
            current_url = driver.current_url
            page_title = driver.title.lower()
            
            # Check if we're on Graph Explorer and authenticated
            if "graph-explorer" in current_url and ("graph explorer" in page_title or "microsoft graph" in page_title):
                # Look for key elements that indicate successful load
                try:
                    # Check for the query input or run button
                    query_elements = driver.find_elements(By.CSS_SELECTOR, 
                        'input[placeholder*="query"], input[aria-label*="query"], button[title*="Run"], button[aria-label*="Run"]')
                    if query_elements:
                        print("✅ Authentication completed and Graph Explorer loaded")
                        auth_completed = True
                        break
                except:
                    pass
            
            time.sleep(5)  # Wait 5 seconds between checks
            
        except Exception as e:
            print(f"   Checking authentication status... (attempt {attempt + 1})")
            time.sleep(5)
    
    return auth_completed


def execute_graph_query(driver: webdriver.Edge, wait: WebDriverWait, query: str) -> Optional[Dict[str, Any]]:
    """Execute the Graph API query in Graph Explorer."""
    try:
        print(f"🔍 Executing query: {query}")
        
        # Multiple strategies to find and interact with the query input
        query_selectors = [
            'input[placeholder*="query"]',
            'input[aria-label*="query"]',
            'input[type="text"]',
            '.query-input',
            '#query-input',
            'textarea[placeholder*="query"]',
            'div[contenteditable="true"]'
        ]
        
        query_element = None
        for selector in query_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    query_element = elements[0]
                    print(f"   Found query input using selector: {selector}")
                    break
            except:
                continue
        
        if not query_element:
            print("❌ Could not find query input field")
            print("   Page elements found:")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for i, inp in enumerate(inputs[:5]):  # Show first 5 inputs
                try:
                    placeholder = inp.get_attribute("placeholder") or ""
                    aria_label = inp.get_attribute("aria-label") or ""
                    print(f"     Input {i}: placeholder='{placeholder}', aria-label='{aria_label}'")
                except:
                    pass
            return None
        
        # Clear and enter the query
        query_element.clear()
        query_element.send_keys(query)
        time.sleep(1)
        
        # Find and click the run button
        run_selectors = [
            'button[title*="Run"]',
            'button[aria-label*="Run"]',
            'button:contains("Run")',
            '.run-button',
            '#run-button',
            'button[type="submit"]'
        ]
        
        run_button = None
        for selector in run_selectors:
            try:
                if ":contains(" in selector:
                    # Use XPath for text content
                    xpath = f"//button[contains(text(), 'Run')]"
                    elements = driver.find_elements(By.XPATH, xpath)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    run_button = elements[0]
                    print(f"   Found run button using selector: {selector}")
                    break
            except:
                continue
        
        if not run_button:
            # Try pressing Enter in the query field
            print("   Run button not found, trying Enter key...")
            query_element.send_keys(Keys.RETURN)
        else:
            run_button.click()
        
        print("   Query submitted, waiting for results...")
        
        # Wait for results to load
        time.sleep(5)
        
        # Look for JSON response in various possible containers
        result_selectors = [
            '.response-body',
            '.json-response',
            '.response-content',
            'pre',
            'code',
            '.response-panel',
            '[data-testid*="response"]'
        ]
        
        response_text = None
        for selector in result_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and (text.startswith('{') or text.startswith('[')):
                        response_text = text
                        print(f"   Found JSON response using selector: {selector}")
                        break
                if response_text:
                    break
            except:
                continue
        
        if not response_text:
            print("❌ Could not find JSON response")
            print("   Looking for any JSON-like content...")
            # Try to find any element containing JSON
            all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '{') or contains(text(), '[')]")
            for element in all_elements[:5]:  # Check first 5 elements
                try:
                    text = element.text.strip()
                    if len(text) > 50 and ('{' in text or '[' in text):
                        print(f"     Found potential JSON: {text[:100]}...")
                        response_text = text
                        break
                except:
                    pass
        
        if response_text:
            try:
                response_json = json.loads(response_text)
                print("✅ Successfully retrieved calendar data")
                return response_json
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print(f"   Response preview: {response_text[:200]}...")
                return None
        
        return None
        
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None


def parse_iso_datetime(iso_string: str) -> datetime:
    """Parse ISO datetime string and convert to local timezone."""
    try:
        # Parse the ISO string
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        
        # Convert to local timezone (PDT)
        try:
            local_tz = zoneinfo.ZoneInfo("America/Los_Angeles")
        except:
            # Fallback for PDT (UTC-7)
            local_tz = timezone(timedelta(hours=-7))
        
        return dt.astimezone(local_tz)
    except Exception as e:
        print(f"❌ Error parsing datetime '{iso_string}': {e}")
        return None


def format_meeting_time(start_dt: datetime, end_dt: datetime) -> str:
    """Format meeting time range in local timezone."""
    if not start_dt or not end_dt:
        return "❓ Time unavailable"
    
    # Check if same day
    if start_dt.date() == end_dt.date():
        return f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p PDT')}"
    else:
        return f"{start_dt.strftime('%m/%d %I:%M %p')} - {end_dt.strftime('%m/%d %I:%M %p PDT')}"


def extract_location(meeting: Dict[str, Any]) -> str:
    """Extract location information from meeting."""
    location = meeting.get('location', {})
    
    if isinstance(location, dict):
        display_name = location.get('displayName', '')
        if display_name:
            return f"📍 {display_name}"
    
    return ""


def analyze_meeting_conflicts(meetings: List[Dict[str, Any]]) -> None:
    """Analyze meetings for potential conflicts with Flight CI005 at 4:25 PM PDT."""
    flight_time = "4:25 PM PDT"
    print(f"\n✈️ Flight CI005 Conflict Analysis (Departure: {flight_time}):")
    print("=" * 50)
    
    conflicts_found = False
    
    for meeting in meetings:
        start_dt = parse_iso_datetime(meeting['start']['dateTime'])
        end_dt = parse_iso_datetime(meeting['end']['dateTime'])
        
        if not start_dt or not end_dt:
            continue
        
        # Flight departure time (4:25 PM PDT)
        flight_dt = start_dt.replace(hour=16, minute=25, second=0, microsecond=0)
        
        # Check for conflicts (meeting overlaps with 3:00-5:00 PM window)
        conflict_start = flight_dt - timedelta(hours=1, minutes=25)  # 3:00 PM
        conflict_end = flight_dt + timedelta(minutes=35)  # 5:00 PM
        
        if (start_dt <= conflict_end and end_dt >= conflict_start):
            conflicts_found = True
            time_range = format_meeting_time(start_dt, end_dt)
            print(f"⚠️  CONFLICT: {meeting.get('subject', 'No subject')} ({time_range})")
    
    if not conflicts_found:
        print("✅ No meeting conflicts with flight departure!")


def display_calendar_results(response_json: Dict[str, Any]) -> None:
    """Display the calendar results in a formatted way."""
    try:
        meetings = response_json.get('value', [])
        
        print("\n📅 Today's Meetings from Microsoft Graph Explorer")
        print("=" * 55)
        print(f"Found {len(meetings)} meeting(s) for today\n")
        
        if not meetings:
            print("🎉 No meetings scheduled for today!")
            return
        
        # Display meetings
        for i, meeting in enumerate(meetings, 1):
            subject = meeting.get('subject', 'No Subject')
            
            # Parse times
            start_dt = parse_iso_datetime(meeting['start']['dateTime'])
            end_dt = parse_iso_datetime(meeting['end']['dateTime'])
            time_range = format_meeting_time(start_dt, end_dt)
            
            # Get organizer
            organizer = meeting.get('organizer', {}).get('emailAddress', {})
            organizer_name = organizer.get('name', 'Unknown')
            
            # Get location
            location = extract_location(meeting)
            
            # Response status
            response = meeting.get('responseStatus', {}).get('response', 'none')
            status_emoji = {
                'accepted': '✅',
                'tentative': '❓',
                'declined': '❌',
                'none': '⏳'
            }.get(response, '⏳')
            
            print(f"{i}. {subject}")
            print(f"   ⏰ {time_range}")
            print(f"   👤 Organizer: {organizer_name}")
            if location:
                print(f"   {location}")
            print(f"   {status_emoji} Status: {response.title()}")
            print()
        
        # Analyze flight conflicts
        analyze_meeting_conflicts(meetings)
        
    except Exception as e:
        print(f"❌ Error displaying results: {e}")


def main():
    """Main automation function."""
    print("🤖 Automated Microsoft Graph Calendar Access with Edge")
    print("=" * 50)
    
    # Check for headless mode
    headless = '--headless' in sys.argv
    if headless:
        print("Running in headless mode...")
    
    driver = None
    try:
        # Setup browser
        print("🌐 Setting up Microsoft Edge browser...")
        driver = setup_browser(headless=headless)
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        
        # Navigate to Graph Explorer
        print("📱 Opening Microsoft Graph Explorer...")
        driver.get(GRAPH_EXPLORER_URL)
        
        # Wait for authentication
        if not wait_for_authentication(driver, wait):
            print("❌ Authentication timeout. Please try again.")
            return
        
        # Build the calendar query
        query = build_calendar_query()
        print(f"📅 Query for today: {query}")
        
        # Execute the query
        response_json = execute_graph_query(driver, wait, query)
        
        if response_json:
            # Display results
            display_calendar_results(response_json)
            
            # Save results to file
            output_file = f"calendar_today_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(response_json, f, indent=2)
            print(f"\n💾 Results saved to: {output_file}")
            
        else:
            print("❌ Failed to retrieve calendar data")
            print("💡 You can manually:")
            print("   1. Go to https://developer.microsoft.com/en-us/graph/graph-explorer")
            print(f"   2. Execute: GET {query}")
            print("   3. Use the parse_graph_explorer_response.py tool")
    
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Automation failed: {e}")
        print("💡 Falling back to manual process:")
        print("   1. Go to https://developer.microsoft.com/en-us/graph/graph-explorer")
        print(f"   2. Execute: GET {build_calendar_query()}")
        print("   3. Use the parse_graph_explorer_response.py tool")
    finally:
        if driver:
            print("🔄 Closing Microsoft Edge...")
            driver.quit()


if __name__ == "__main__":
    main()