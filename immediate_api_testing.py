#!/usr/bin/env python3
"""
Immediate Official Me Notes API Testing
Let's test the actual access methods mentioned in the documentation
"""

import webbrowser
import requests
import json
from datetime import datetime

def test_aka_ms_pint():
    """Test aka.ms/pint access directly"""
    print('🔍 Testing aka.ms/pint access...')
    
    url = 'https://aka.ms/pint'
    
    print(f'📋 Action Required:')
    print(f'   1. Open: {url}')
    print(f'   2. Sign in with your Microsoft account (cyl@microsoft.com)')
    print(f'   3. Look for "People Notes" or "Me Notes" section')
    print(f'   4. Report back what you see!')
    
    # Open in browser automatically
    try:
        webbrowser.open(url)
        print(f'   ✅ Opening {url} in your default browser...')
    except:
        print(f'   ⚠️ Please manually open: {url}')
    
    return url

def test_potential_graph_endpoints():
    """Test potential Microsoft Graph endpoints"""
    print('\n🔍 Testing Microsoft Graph API endpoints...')
    
    # These are the endpoints we should test
    endpoints_to_test = [
        'https://graph.microsoft.com/v1.0/me/insights/shared',
        'https://graph.microsoft.com/v1.0/me/insights/trending',
        'https://graph.microsoft.com/v1.0/me/insights/used',
        'https://graph.microsoft.com/v1.0/me/people',
        'https://graph.microsoft.com/beta/me/insights/peopleNotes',  # Hypothetical
        'https://graph.microsoft.com/v1.0/me/analytics',  # Hypothetical
    ]
    
    print('📋 Endpoints to test with your current authentication:')
    for i, endpoint in enumerate(endpoints_to_test, 1):
        print(f'   {i}. {endpoint}')
    
    print('\n💡 How to test these:')
    print('   1. Use your existing Microsoft Graph authentication')
    print('   2. Try each endpoint and see what data is returned')
    print('   3. Look for any "peopleNotes" or similar data')
    
    return endpoints_to_test

def search_entity_serve():
    """Guide for finding EntityServe access"""
    print('\n🔍 Searching for EntityServe access...')
    
    search_actions = [
        'Search Microsoft internal sites for "EntityServe"',
        'Look for "ES explorer" in Microsoft tools',
        'Search for "People Notes" in Microsoft search',
        'Check Microsoft 365 admin center for insights',
        'Search Viva Insights for people analytics'
    ]
    
    print('📋 Search Actions:')
    for i, action in enumerate(search_actions, 1):
        print(f'   {i}. {action}')
    
    return search_actions

def contact_me_notes_team():
    """Contact information for Me Notes team"""
    print('\n📞 Contacting Microsoft Me Notes Team...')
    
    contact_info = {
        'official_contact': 'aka.ms/peoplenotes',
        'documentation_link': 'https://aka.ms/peoplenotes',
        'support_request': 'Submit request for Me Notes API access',
        'mention_context': 'Enterprise meeting intelligence system integration'
    }
    
    print('📋 Contact Strategy:')
    print(f'   🌐 Visit: {contact_info["official_contact"]}')
    print(f'   📧 Request: API access for personal Me Notes data')
    print(f'   💼 Context: Building enterprise meeting intelligence system')
    print(f'   👤 User: {contact_info.get("user_email", "cyl@microsoft.com")}')
    
    # Open contact page
    try:
        webbrowser.open('https://aka.ms/peoplenotes')
        print(f'   ✅ Opening contact page in browser...')
    except:
        print(f'   ⚠️ Please manually open: https://aka.ms/peoplenotes')
    
    return contact_info

def create_immediate_test_script():
    """Create a script to test Graph API access with current auth"""
    
    script_content = '''#!/usr/bin/env python3
"""
Test Script for Microsoft Graph Me Notes Access
Run this with your current Microsoft Graph authentication
"""

import requests
import json

def test_graph_access(access_token):
    """Test Graph API endpoints with your access token"""
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Test endpoints
    endpoints = [
        'https://graph.microsoft.com/v1.0/me',
        'https://graph.microsoft.com/v1.0/me/insights/shared',
        'https://graph.microsoft.com/v1.0/me/insights/trending', 
        'https://graph.microsoft.com/v1.0/me/insights/used',
        'https://graph.microsoft.com/v1.0/me/people',
        'https://graph.microsoft.com/beta/me/insights/peopleNotes',
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers)
            results[endpoint] = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'data': response.json() if response.status_code == 200 else response.text
            }
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            results[endpoint] = {
                'status_code': 'ERROR',
                'success': False,
                'error': str(e)
            }
            print(f"❌ {endpoint}: {e}")
    
    return results

# Usage:
# 1. Get your access token from your current Graph authentication
# 2. Run: test_graph_access("your_access_token_here")
'''
    
    with open('test_graph_me_notes.py', 'w') as f:
        f.write(script_content)
    
    print('\n💾 Created test script: test_graph_me_notes.py')
    print('📋 Usage:')
    print('   1. Get your current Microsoft Graph access token')
    print('   2. Edit test_graph_me_notes.py and add your token')
    print('   3. Run the script to test endpoints')

def main():
    """Execute immediate testing plan"""
    
    print('🚀 Immediate Official Me Notes API Access Testing')
    print('=' * 60)
    print(f'🕒 Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'👤 User: cyl@microsoft.com')
    print()
    
    # Test 1: aka.ms/pint
    test_aka_ms_pint()
    
    # Test 2: Graph API endpoints
    test_potential_graph_endpoints()
    
    # Test 3: EntityServe search
    search_entity_serve()
    
    # Test 4: Contact Me Notes team
    contact_me_notes_team()
    
    # Test 5: Create test script
    create_immediate_test_script()
    
    print('\n🎯 Priority Actions (do these RIGHT NOW):')
    print('   1. ✅ Check aka.ms/pint (opened in browser)')
    print('   2. 🔍 Test Graph API endpoints with your current auth')
    print('   3. 📞 Contact Me Notes team via aka.ms/peoplenotes (opened in browser)')
    print('   4. 🔄 Report back findings so we can adjust strategy')
    
    print('\n💡 Expected Outcomes:')
    print('   🏆 BEST: aka.ms/pint gives you direct access to your Me Notes')
    print('   🥈 GOOD: Graph API has peopleNotes endpoint we can use')
    print('   🥉 OK: Me Notes team provides API access instructions')
    print('   🔄 FALLBACK: Implement Option C comprehensive framework')

if __name__ == "__main__":
    main()