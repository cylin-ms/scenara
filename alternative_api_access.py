#!/usr/bin/env python3
"""
Alternative Official Me Notes Access Methods
Since SharePoint interface doesn't expose API, let's try other approaches
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, List

def test_direct_graph_api_endpoints():
    """
    Test Microsoft Graph API endpoints directly with current authentication
    """
    
    print('🔍 Testing Direct Microsoft Graph API Endpoints')
    print('=' * 60)
    
    # Endpoints to test based on Microsoft Me Notes documentation
    test_endpoints = [
        # Standard Graph insights
        'https://graph.microsoft.com/v1.0/me/insights/shared',
        'https://graph.microsoft.com/v1.0/me/insights/trending',
        'https://graph.microsoft.com/v1.0/me/insights/used',
        'https://graph.microsoft.com/v1.0/me/people',
        
        # Beta endpoints that might have People Notes
        'https://graph.microsoft.com/beta/me/insights/peopleNotes',
        'https://graph.microsoft.com/beta/me/peopleNotes',
        'https://graph.microsoft.com/beta/me/profile/notes',
        'https://graph.microsoft.com/beta/me/analytics/peopleNotes',
        
        # Viva Insights endpoints
        'https://graph.microsoft.com/beta/me/insights',
        'https://graph.microsoft.com/beta/me/analytics',
        'https://graph.microsoft.com/v1.0/me/inferenceClassification',
        
        # Search API for People Notes
        'https://graph.microsoft.com/v1.0/search/query',
    ]
    
    print('📋 Endpoints to test with your Microsoft authentication:')
    for i, endpoint in enumerate(test_endpoints, 1):
        print(f'   {i:2d}. {endpoint}')
    
    print('\n💡 How to test these:')
    print('   1. Use your existing Microsoft Graph authentication token')
    print('   2. Make GET requests to each endpoint')
    print('   3. Look for any endpoints that return People Notes data')
    print('   4. Check response headers for additional endpoint hints')
    
    return test_endpoints

def create_graph_api_test_script():
    """
    Create a script to systematically test Graph API endpoints
    """
    
    script_content = '''#!/usr/bin/env python3
"""
Microsoft Graph API People Notes Discovery Script
Test all potential endpoints with your authentication
"""

import requests
import json
from datetime import datetime

def test_graph_endpoints_with_auth():
    """
    Test Graph API endpoints with your authentication token
    
    Instructions:
    1. Get your access token from browser dev tools or existing auth
    2. Replace YOUR_ACCESS_TOKEN below
    3. Run this script to test all endpoints
    """
    
    # TODO: Replace with your actual access token
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    endpoints = [
        'https://graph.microsoft.com/v1.0/me/insights/shared',
        'https://graph.microsoft.com/v1.0/me/insights/trending',
        'https://graph.microsoft.com/v1.0/me/insights/used',
        'https://graph.microsoft.com/v1.0/me/people',
        'https://graph.microsoft.com/beta/me/insights/peopleNotes',
        'https://graph.microsoft.com/beta/me/peopleNotes',
        'https://graph.microsoft.com/beta/me/profile/notes',
        'https://graph.microsoft.com/beta/me/analytics/peopleNotes',
        'https://graph.microsoft.com/beta/me/insights',
        'https://graph.microsoft.com/beta/me/analytics',
    ]
    
    results = {}
    successful_endpoints = []
    
    print('🔍 Testing Microsoft Graph API Endpoints for People Notes')
    print('=' * 70)
    
    for endpoint in endpoints:
        try:
            print(f'\\n📡 Testing: {endpoint}')
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'headers': dict(response.headers),
                'content_type': response.headers.get('content-type', 'unknown')
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['data'] = data
                    result['data_keys'] = list(data.keys()) if isinstance(data, dict) else []
                    result['data_size'] = len(str(data))
                    
                    print(f'   ✅ SUCCESS! Status: {response.status_code}')
                    print(f'   📊 Data keys: {result["data_keys"]}')
                    print(f'   📏 Data size: {result["data_size"]} characters')
                    
                    successful_endpoints.append(endpoint)
                    
                    # Check if this looks like People Notes
                    if any(key in str(data).lower() for key in ['note', 'insight', 'people', 'person']):
                        print(f'   🎯 POTENTIAL PEOPLE NOTES DATA FOUND!')
                        
                except json.JSONDecodeError:
                    result['data'] = response.text
                    print(f'   ✅ SUCCESS! Status: {response.status_code} (non-JSON response)')
                    
            elif response.status_code == 401:
                print(f'   🔐 Authentication required: {response.status_code}')
                result['error'] = 'Authentication failed - check your access token'
                
            elif response.status_code == 403:
                print(f'   🚫 Forbidden: {response.status_code}')
                result['error'] = 'Insufficient permissions for this endpoint'
                
            elif response.status_code == 404:
                print(f'   ❌ Not found: {response.status_code}')
                result['error'] = 'Endpoint not available'
                
            else:
                print(f'   ⚠️  Other status: {response.status_code}')
                result['error'] = response.text
                
            results[endpoint] = result
            
        except requests.exceptions.RequestException as e:
            print(f'   ❌ Request failed: {e}')
            results[endpoint] = {
                'status_code': 'ERROR',
                'success': False,
                'error': str(e)
            }
    
    # Summary
    print(f'\\n📊 Summary:')
    print(f'   ✅ Successful endpoints: {len(successful_endpoints)}')
    print(f'   ❌ Failed endpoints: {len(endpoints) - len(successful_endpoints)}')
    
    if successful_endpoints:
        print(f'\\n🎯 Successful endpoints to investigate:')
        for endpoint in successful_endpoints:
            print(f'   • {endpoint}')
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'graph_api_test_results_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f'\\n💾 Results saved to: {filename}')
    
    return results

if __name__ == "__main__":
    # Instructions for getting access token
    print('🔑 Getting Your Access Token:')
    print('   1. Go to the SharePoint People Notes page')
    print('   2. Open browser Developer Tools (F12)')
    print('   3. Go to Network tab and refresh page')
    print('   4. Look for requests to graph.microsoft.com')
    print('   5. Copy the Authorization header (starts with "Bearer ")')
    print('   6. Paste it in this script and run')
    print()
    
    # Ask user to add their token
    print('⚠️  Edit this script and add your access token, then run it!')
'''
    
    with open('test_graph_api_people_notes.py', 'w') as f:
        f.write(script_content)
    
    print('💾 Created Graph API test script: test_graph_api_people_notes.py')

def investigate_alternative_access_methods():
    """
    Investigate alternative ways to access People Notes data
    """
    
    print('\n🔍 Alternative Access Methods Investigation')
    print('=' * 60)
    
    alternatives = {
        'Method 1: Browser Automation': {
            'description': 'Automate browser to extract data from SharePoint page',
            'tools': ['Selenium', 'Playwright', 'Puppeteer'],
            'pros': ['Works with any web interface', 'Can handle authentication'],
            'cons': ['More complex', 'Might break with UI changes'],
            'implementation_time': '2-3 days'
        },
        
        'Method 2: Network Traffic Analysis': {
            'description': 'Capture and replay API calls from SharePoint page',
            'tools': ['Browser dev tools', 'mitmproxy', 'Burp Suite'],
            'pros': ['Direct API access', 'Can automate discovered endpoints'],
            'cons': ['Need to find the right requests', 'Authentication complexity'],
            'implementation_time': '1-2 days'
        },
        
        'Method 3: Microsoft Graph Explorer': {
            'description': 'Use official Graph Explorer to test endpoints',
            'tools': ['https://developer.microsoft.com/graph/graph-explorer'],
            'pros': ['Official Microsoft tool', 'Handles authentication'],
            'cons': ['Limited to documented endpoints'],
            'implementation_time': '1 day'
        },
        
        'Method 4: PowerShell/CLI Tools': {
            'description': 'Use Microsoft CLI tools that might have People Notes access',
            'tools': ['Microsoft Graph PowerShell', 'Azure CLI', 'M365 CLI'],
            'pros': ['Official tools', 'Command-line friendly'],
            'cons': ['May not expose People Notes', 'Limited functionality'],
            'implementation_time': '1-2 days'
        },
        
        'Method 5: Contact Microsoft Support': {
            'description': 'Official request for API access or data export',
            'tools': ['Microsoft Support', 'Developer forums'],
            'pros': ['Official support', 'Might get proper API access'],
            'cons': ['May take weeks', 'No guarantee of access'],
            'implementation_time': '1-2 weeks'
        }
    }
    
    for method, details in alternatives.items():
        print(f'\n📋 {method}:')
        print(f'   📝 {details["description"]}')
        print(f'   🛠️ Tools: {", ".join(details["tools"])}')
        print(f'   ✅ Pros: {", ".join(details["pros"])}')
        print(f'   ❌ Cons: {", ".join(details["cons"])}')
        print(f'   ⏱️ Time: {details["implementation_time"]}')
    
    return alternatives

def recommend_next_steps():
    """
    Recommend the best next steps based on current situation
    """
    
    print('\n🎯 Recommended Next Steps')
    print('=' * 60)
    
    recommendations = [
        {
            'priority': 'HIGH',
            'action': 'Test Graph API endpoints with your auth token',
            'time': '1-2 hours',
            'description': 'Use the test script to systematically check all potential endpoints'
        },
        {
            'priority': 'HIGH', 
            'action': 'Analyze SharePoint page network traffic',
            'time': '1 hour',
            'description': 'Use browser dev tools to find API calls the page makes'
        },
        {
            'priority': 'MEDIUM',
            'action': 'Try Microsoft Graph Explorer',
            'time': '30 minutes',
            'description': 'Official tool might have People Notes endpoints'
        },
        {
            'priority': 'MEDIUM',
            'action': 'Browser automation fallback',
            'time': '1-2 days',
            'description': 'If APIs fail, automate the SharePoint interface'
        },
        {
            'priority': 'LOW',
            'action': 'Implement comprehensive Option C',
            'time': '2-4 weeks',
            'description': 'Full local inference with email/chat/transcripts'
        }
    ]
    
    print('📋 Action Plan (in priority order):')
    for i, rec in enumerate(recommendations, 1):
        priority_icon = '🔥' if rec['priority'] == 'HIGH' else '⚡' if rec['priority'] == 'MEDIUM' else '💡'
        print(f'\n{i}. {priority_icon} {rec["action"]} ({rec["time"]})')
        print(f'   📝 {rec["description"]}')

def main():
    """
    Main investigation function
    """
    
    print('🔍 Alternative Official Me Notes Access Investigation')
    print('=' * 70)
    print('📊 Since SharePoint interface doesn\'t expose APIs directly...')
    print()
    
    # Test Graph API endpoints
    test_direct_graph_api_endpoints()
    
    # Create test script
    create_graph_api_test_script()
    
    # Investigate alternatives
    investigate_alternative_access_methods()
    
    # Recommendations
    recommend_next_steps()
    
    print('\n💡 Key Insight:')
    print('   🏆 You DO have access to official People Notes (SharePoint page works)')
    print('   🔍 We just need to find the right way to extract the data')
    print('   📡 Most likely through Graph API endpoints or network traffic analysis')

if __name__ == "__main__":
    main()