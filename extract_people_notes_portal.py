#!/usr/bin/env python3
"""
Extract data from Microsoft People Notes Portal
URL: aka.ms/pintfeedbackportal
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_from_portal():
    """
    Extract People Notes data from the official portal
    """
    
    print('🎯 Extracting from People Notes Portal')
    print('=' * 60)
    
    # Setup browser
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to portal
        portal_url = 'https://aka.ms/pintfeedbackportal'
        print(f'🔗 Navigating to: {portal_url}')
        
        driver.get(portal_url)
        
        # Wait for page to load
        print('⏳ Waiting for page to load...')
        time.sleep(10)
        
        # Look for People Notes data
        print('🔍 Looking for People Notes data...')
        
        # Common selectors for Microsoft portals
        selectors_to_try = [
            '[data-testid*="people"]',
            '[data-testid*="note"]',
            '.people-note',
            '.insight',
            '[role="grid"]',
            '[role="table"]',
            '.ms-List',
            '.ms-DetailsList'
        ]
        
        found_data = []
        
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f'✅ Found {len(elements)} elements with: {selector}')
                    for element in elements[:5]:  # Limit to first 5
                        text = element.text.strip()
                        if text and len(text) > 10:
                            found_data.append({
                                'selector': selector,
                                'text': text[:200] + '...' if len(text) > 200 else text,
                                'html': element.get_attribute('outerHTML')[:300] + '...'
                            })
            except:
                continue
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'people_notes_portal_data_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(found_data, f, indent=2)
        
        # Save page source
        page_source_file = f'people_notes_portal_source_{timestamp}.html'
        with open(page_source_file, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        print(f'\n📊 RESULTS:')
        print(f'   📝 Found {len(found_data)} data elements')
        print(f'   💾 Data saved to: {filename}')
        print(f'   💾 Page source: {page_source_file}')
        
        # Interactive examination
        print('\n👀 Browser is open - examine the portal page')
        input('Press Enter when done examining...')
        
        return found_data
        
    except Exception as e:
        print(f'❌ Portal extraction failed: {e}')
        return []
        
    finally:
        driver.quit()
        print('✅ Browser cleanup complete')

if __name__ == "__main__":
    extract_from_portal()
