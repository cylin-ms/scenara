#!/usr/bin/env python3
"""
Microsoft People Notes SharePoint Scraper
Automates browser to extract official People Notes data
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class PeopleNotesExtractor:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.people_notes_url = "https://microsoft.sharepoint-df.com/sites/personalization/SitePages/People-Notes.aspx"
        
    def setup_browser(self):
        """Setup Chrome browser with appropriate options"""
        
        print('🌐 Setting up browser automation...')
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Keep browser visible for authentication
        # chrome_options.add_argument('--headless')  # Uncomment for headless mode
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        
        print('✅ Browser setup complete')
        
    def authenticate_and_navigate(self):
        """Navigate to People Notes page and handle authentication"""
        
        print('🔐 Navigating to People Notes page...')
        
        try:
            self.driver.get(self.people_notes_url)
            
            # Wait for authentication to complete
            print('⏳ Waiting for authentication...')
            print('   📋 Please sign in if prompted')
            print('   ⌚ Waiting up to 60 seconds for page to load')
            
            # Wait for page content to load
            self.wait.until(
                lambda driver: "People" in driver.title or 
                              len(driver.find_elements(By.TAG_NAME, "body")) > 0
            )
            
            print('✅ Successfully navigated to People Notes page')
            return True
            
        except Exception as e:
            print(f'❌ Navigation failed: {e}')
            return False
    
    def extract_people_notes_data(self):
        """Extract People Notes data from the SharePoint page"""
        
        print('🔍 Extracting People Notes data...')
        
        try:
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Look for various patterns that might contain People Notes
            people_notes = []
            
            # Method 1: Look for data in script tags (common for SharePoint)
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'people' in script.string.lower():
                    # Try to extract JSON data
                    script_content = script.string
                    if 'notes' in script_content.lower() or 'insight' in script_content.lower():
                        people_notes.append({
                            'source': 'script_tag',
                            'content': script_content[:500] + '...' if len(script_content) > 500 else script_content
                        })
            
            # Method 2: Look for div/span elements with people data
            people_elements = soup.find_all(['div', 'span', 'p'], 
                                          string=lambda text: text and 'note' in text.lower())
            
            for element in people_elements:
                people_notes.append({
                    'source': 'html_element',
                    'tag': element.name,
                    'content': element.get_text().strip()
                })
            
            # Method 3: Look for table rows or list items
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) > 1:  # Has header and data rows
                    people_notes.append({
                        'source': 'table_data',
                        'rows': len(rows),
                        'content': str(table)[:200] + '...'
                    })
            
            # Method 4: Look for React/Angular component data
            react_elements = soup.find_all(attrs={'data-reactroot': True})
            for element in react_elements:
                people_notes.append({
                    'source': 'react_component',
                    'content': str(element)[:200] + '...'
                })
            
            print(f'✅ Extracted {len(people_notes)} potential data sources')
            return people_notes
            
        except Exception as e:
            print(f'❌ Data extraction failed: {e}')
            return []
    
    def interactive_extraction(self):
        """Interactive mode to help identify People Notes elements"""
        
        print('🎯 Interactive People Notes Identification')
        print('=' * 60)
        print('👀 Browser is open - please examine the People Notes page')
        print('📋 Look for:')
        print('   • Lists of people')
        print('   • Notes or insights about people')
        print('   • Export buttons')
        print('   • Data tables')
        print()
        
        input('Press Enter when you have examined the page...')
        
        # Try to find common SharePoint elements
        common_selectors = [
            '[role="grid"]',  # SharePoint lists
            '.ms-List',       # Microsoft Fabric lists
            '[data-automationid]',  # SharePoint automation IDs
            '.od-Items',      # OneDrive/SharePoint items
            '[aria-label*="people"]',  # Aria labels with "people"
            '[aria-label*="notes"]',   # Aria labels with "notes"
        ]
        
        found_elements = []
        
        for selector in common_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f'✅ Found {len(elements)} elements with selector: {selector}')
                    found_elements.extend(elements)
            except:
                continue
        
        # Extract text from found elements
        extracted_data = []
        for element in found_elements[:10]:  # Limit to first 10
            try:
                text = element.text.strip()
                if text and len(text) > 10:  # Only non-empty, substantial text
                    extracted_data.append({
                        'tag': element.tag_name,
                        'text': text[:100] + '...' if len(text) > 100 else text,
                        'attributes': element.get_attribute('outerHTML')[:200] + '...'
                    })
            except:
                continue
        
        return extracted_data
    
    def save_results(self, data, interactive_data=None):
        """Save extracted data to files"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save main extraction results
        main_file = f'people_notes_extracted_{timestamp}.json'
        with open(main_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f'💾 Main data saved to: {main_file}')
        
        # Save interactive results
        if interactive_data:
            interactive_file = f'people_notes_interactive_{timestamp}.json'
            with open(interactive_file, 'w') as f:
                json.dump(interactive_data, f, indent=2, default=str)
            
            print(f'💾 Interactive data saved to: {interactive_file}')
        
        # Save page source for manual analysis
        page_source_file = f'people_notes_page_source_{timestamp}.html'
        with open(page_source_file, 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
        
        print(f'💾 Page source saved to: {page_source_file}')
    
    def cleanup(self):
        """Clean up browser resources"""
        if self.driver:
            self.driver.quit()
            print('✅ Browser cleanup complete')
    
    def extract_people_notes(self):
        """Main extraction workflow"""
        
        print('🚀 Microsoft People Notes Extraction')
        print('=' * 70)
        
        try:
            # Setup browser
            self.setup_browser()
            
            # Navigate and authenticate
            if not self.authenticate_and_navigate():
                return None
            
            # Extract data automatically
            extracted_data = self.extract_people_notes_data()
            
            # Interactive identification
            interactive_data = self.interactive_extraction()
            
            # Save results
            self.save_results(extracted_data, interactive_data)
            
            print('\n🎯 EXTRACTION SUMMARY:')
            print(f'   📊 Automatic extraction: {len(extracted_data)} items')
            print(f'   🎯 Interactive extraction: {len(interactive_data)} items')
            print('   💾 All data saved to files')
            
            return {
                'automatic': extracted_data,
                'interactive': interactive_data,
                'success': True
            }
            
        except Exception as e:
            print(f'❌ Extraction failed: {e}')
            return {'success': False, 'error': str(e)}
            
        finally:
            self.cleanup()

def main():
    """Main function"""
    
    print('🔍 Microsoft People Notes Browser Automation')
    print('=' * 70)
    print('📋 This script will:')
    print('   1. Open Chrome browser')
    print('   2. Navigate to People Notes SharePoint page') 
    print('   3. Wait for you to authenticate')
    print('   4. Extract all available People Notes data')
    print('   5. Save results to files')
    print()
    
    extractor = PeopleNotesExtractor()
    results = extractor.extract_people_notes()
    
    if results and results.get('success'):
        print('\n🏆 SUCCESS! People Notes data extracted')
        print('📋 Check the generated files for extracted data')
    else:
        print('\n❌ Extraction failed')
        print('💡 You can manually examine the page and copy data')

if __name__ == "__main__":
    main()
