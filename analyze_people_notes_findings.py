#!/usr/bin/env python3
"""
Analyze People Notes Extraction Results
Key finding: aka.ms/pintfeedbackportal for accessing your own People Notes
"""

import json
from datetime import datetime

def analyze_extraction_results():
    """
    Analyze the extracted People Notes data and identify key findings
    """
    
    print('🔍 People Notes Extraction Analysis')
    print('=' * 60)
    
    # Load the extracted data
    try:
        with open('people_notes_extracted_20251022_042349.json', 'r') as f:
            extracted_data = json.load(f)
    except FileNotFoundError:
        print('❌ Extraction file not found')
        return
    
    # Key findings from the extraction
    key_findings = {
        'access_portal': 'aka.ms/pintfeedbackportal',
        'description': 'Visit "aka.ms/pintfeedbackportal" to see your own people notes',
        'smart_notes': 'Smart Notes (representation of People Notes in LPC) is available for MSIT users',
        'purpose': 'AI-first people experiences with LLM enabled short-term and long-term memory capabilities',
        'features': [
            'Persistent information',
            'Managed content', 
            'Condensable data',
            'Searchable notes',
            'Partner integration'
        ]
    }
    
    print('🎯 KEY FINDING: Direct Access Portal!')
    print(f'   🔗 URL: {key_findings["access_portal"]}')
    print(f'   📝 Description: {key_findings["description"]}')
    print()
    
    print('💡 What we learned about People Notes:')
    print(f'   🤖 {key_findings["purpose"]}')
    print(f'   🏢 {key_findings["smart_notes"]}')
    print()
    
    print('✨ People Notes Features:')
    for feature in key_findings['features']:
        print(f'   • {feature}')
    
    return key_findings

def test_people_notes_portal():
    """
    Open the People Notes portal for direct access
    """
    
    print('\n🚀 Testing People Notes Portal Access')
    print('=' * 60)
    
    portal_url = 'https://aka.ms/pintfeedbackportal'
    
    print(f'🔗 Opening: {portal_url}')
    print('📋 This should take you directly to YOUR People Notes data!')
    
    # Open in browser
    import webbrowser
    try:
        webbrowser.open(portal_url)
        print('✅ Browser opened - check for your People Notes data')
        return True
    except Exception as e:
        print(f'❌ Failed to open browser: {e}')
        print(f'💡 Manually visit: {portal_url}')
        return False

def create_portal_extraction_script():
    """
    Create a script to extract data from the People Notes portal
    """
    
    portal_script_content = '''#!/usr/bin/env python3
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
        
        print(f'\\n📊 RESULTS:')
        print(f'   📝 Found {len(found_data)} data elements')
        print(f'   💾 Data saved to: {filename}')
        print(f'   💾 Page source: {page_source_file}')
        
        # Interactive examination
        print('\\n👀 Browser is open - examine the portal page')
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
'''
    
    with open('extract_people_notes_portal.py', 'w') as f:
        f.write(portal_script_content)
    
    print('\n💾 Created portal extraction script: extract_people_notes_portal.py')

def recommend_next_steps():
    """
    Recommend the next steps based on findings
    """
    
    print('\n🎯 Recommended Next Steps')
    print('=' * 60)
    
    steps = [
        {
            'priority': 'CRITICAL',
            'action': 'Visit aka.ms/pintfeedbackportal',
            'description': 'Direct access to YOUR People Notes data',
            'time': '5 minutes'
        },
        {
            'priority': 'HIGH',
            'action': 'Run portal extraction script',
            'description': 'Automate data extraction from the portal',
            'time': '15 minutes'
        },
        {
            'priority': 'MEDIUM',
            'action': 'Manual data copy',
            'description': 'If automation fails, manually copy the data',
            'time': '30 minutes'
        },
        {
            'priority': 'LOW',
            'action': 'Integrate with Scenara',
            'description': 'Add extracted data to Scenara system',
            'time': '1 hour'
        }
    ]
    
    for i, step in enumerate(steps, 1):
        priority_icon = '🔥' if step['priority'] == 'CRITICAL' else '⚡' if step['priority'] == 'HIGH' else '💡'
        print(f'{i}. {priority_icon} {step["action"]} ({step["time"]})')
        print(f'   📝 {step["description"]}')
        print()

def main():
    """
    Main analysis function
    """
    
    print('🏆 BREAKTHROUGH: Official People Notes Portal Found!')
    print('=' * 70)
    
    # Analyze extraction results
    findings = analyze_extraction_results()
    
    # Test portal access
    portal_opened = test_people_notes_portal()
    
    # Create portal extraction script
    create_portal_extraction_script()
    
    # Recommendations
    recommend_next_steps()
    
    print('\n💡 SUMMARY:')
    print('   🎯 Found direct portal: aka.ms/pintfeedbackportal')
    print('   🚀 This should show YOUR actual People Notes data')
    print('   🔧 Created automation script for data extraction')
    print('   📊 Ready to integrate with Scenara system')

if __name__ == "__main__":
    main()