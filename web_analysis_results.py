#!/usr/bin/env python3
"""
Web Analysis Results: Microsoft People Notes API Investigation
Based on web scraping of Microsoft documentation and Graph Explorer
"""

import json
from datetime import datetime

def analyze_web_scraping_results():
    """
    Analyze the findings from web scraping Microsoft documentation
    """
    
    print('🔍 Web Analysis Results: Microsoft People Notes API')
    print('=' * 70)
    
    findings = {
        'confirmed_apis': {
            'insights_shared': {
                'endpoint': '/me/insights/shared',
                'description': 'Files shared with or by a specific user',
                'relevance': 'Medium - might contain meeting-related files',
                'data_includes': ['Email attachments', 'OneDrive/SharePoint links']
            },
            'insights_trending': {
                'endpoint': '/me/insights/trending', 
                'description': 'Documents trending around the user',
                'relevance': 'Medium - shows relevant documents',
                'data_includes': ['OneDrive files', 'SharePoint team sites']
            },
            'people_api': {
                'endpoint': '/me/people',
                'description': 'People most relevant to user based on communication',
                'relevance': 'High - includes personNotes field!',
                'data_includes': ['Communication patterns', 'Business relationships', 'personNotes field']
            }
        },
        
        'potential_endpoints': [
            '/me/insights/used',
            '/me/people',
            '/me/analytics',
            '/me/profile',
            '/me/insights',
            # Beta endpoints that might exist
            '/beta/me/insights/peopleNotes',
            '/beta/me/peopleNotes', 
            '/beta/me/profile/notes',
            '/beta/me/analytics/peopleNotes'
        ],
        
        'key_discovery': {
            'people_api_has_notes': True,
            'field_name': 'personNotes',
            'description': 'The /me/people API includes a personNotes field for each person',
            'implication': 'This might BE the People Notes data we\'re looking for!'
        },
        
        'authentication_confirmed': {
            'sharepoint_access': True,
            'graph_permissions': ['People.Read', 'People.Read.All'],
            'user_has_access': True
        }
    }
    
    # Display confirmed APIs
    print('✅ Confirmed Available APIs:')
    for api_name, details in findings['confirmed_apis'].items():
        print(f'\n📋 {api_name.upper()}:')
        print(f'   🔗 Endpoint: {details["endpoint"]}')
        print(f'   📝 Description: {details["description"]}')
        print(f'   🎯 Relevance: {details["relevance"]}')
        print(f'   📊 Data: {", ".join(details["data_includes"])}')
    
    # Key discovery
    print(f'\n🎯 KEY DISCOVERY:')
    discovery = findings['key_discovery']
    print(f'   🏆 {discovery["description"]}')
    print(f'   💡 {discovery["implication"]}')
    
    return findings

def create_immediate_test_plan():
    """
    Create a plan to test the discovered APIs immediately
    """
    
    print('\n🚀 Immediate Test Plan')
    print('=' * 70)
    
    test_plan = [
        {
            'priority': 'CRITICAL',
            'action': 'Test /me/people API',
            'time': '15 minutes',
            'details': [
                'This API includes personNotes field for each person',
                'Might be the official People Notes data we need',
                'Easy to test with Graph Explorer'
            ],
            'commands': [
                'GET https://graph.microsoft.com/v1.0/me/people',
                'GET https://graph.microsoft.com/v1.0/me/people?$select=displayName,personNotes'
            ]
        },
        {
            'priority': 'HIGH',
            'action': 'Test insights APIs',
            'time': '30 minutes', 
            'details': [
                'Test shared, trending, and used insights',
                'Look for meeting-related files and patterns',
                'Check for any notes or annotations'
            ],
            'commands': [
                'GET https://graph.microsoft.com/v1.0/me/insights/shared',
                'GET https://graph.microsoft.com/v1.0/me/insights/trending',
                'GET https://graph.microsoft.com/v1.0/me/insights/used'
            ]
        },
        {
            'priority': 'MEDIUM',
            'action': 'Test beta endpoints',
            'time': '20 minutes',
            'details': [
                'Try beta versions of potential People Notes endpoints',
                'These might have newer People Notes features',
                'Some might fail but worth testing'
            ],
            'commands': [
                'GET https://graph.microsoft.com/beta/me/insights/peopleNotes',
                'GET https://graph.microsoft.com/beta/me/peopleNotes',
                'GET https://graph.microsoft.com/beta/me/profile/notes'
            ]
        }
    ]
    
    print('📋 Test Priority Order:')
    for i, test in enumerate(test_plan, 1):
        priority_icon = '🔥' if test['priority'] == 'CRITICAL' else '⚡' if test['priority'] == 'HIGH' else '💡'
        print(f'\n{i}. {priority_icon} {test["action"]} ({test["time"]})')
        print(f'   📝 {test["details"][0]}')
        for detail in test["details"][1:]:
            print(f'       {detail}')
        print(f'   🔗 Commands to test:')
        for cmd in test["commands"]:
            print(f'       {cmd}')
    
    return test_plan

def create_graph_explorer_instructions():
    """
    Create step-by-step instructions for using Graph Explorer
    """
    
    print('\n📋 Graph Explorer Testing Instructions')
    print('=' * 70)
    
    instructions = [
        {
            'step': 1,
            'title': 'Open Graph Explorer',
            'action': 'Go to https://developer.microsoft.com/graph/graph-explorer',
            'details': 'Official Microsoft tool for testing Graph API endpoints'
        },
        {
            'step': 2,
            'title': 'Sign in with your Microsoft account',
            'action': 'Click "Sign in" and use cyl@microsoft.com',
            'details': 'Use the same account that accessed SharePoint People Notes'
        },
        {
            'step': 3,
            'title': 'Test the People API first',
            'action': 'Enter: GET https://graph.microsoft.com/v1.0/me/people',
            'details': 'Look for personNotes field in the response'
        },
        {
            'step': 4,
            'title': 'Check permissions if needed',
            'action': 'Click "Modify Permissions" and enable People.Read',
            'details': 'You might need to consent to additional permissions'
        },
        {
            'step': 5,
            'title': 'Examine the response',
            'action': 'Look for personNotes field in each person object',
            'details': 'This might contain the official People Notes data!'
        },
        {
            'step': 6,
            'title': 'Test other endpoints',
            'action': 'Try insights/shared, insights/trending, etc.',
            'details': 'Look for any notes, annotations, or insights'
        }
    ]
    
    print('🎯 Step-by-Step Instructions:')
    for instruction in instructions:
        print(f'\n{instruction["step"]}. {instruction["title"]}')
        print(f'   🔗 {instruction["action"]}')
        print(f'   💡 {instruction["details"]}')
    
    return instructions

def create_python_test_script():
    """
    Create a Python script to test the APIs once we have a token
    """
    
    script_content = '''#!/usr/bin/env python3
"""
Microsoft Graph API People Notes Test Script
Tests the discovered endpoints to find official People Notes data
"""

import requests
import json
from datetime import datetime

def test_people_notes_apis():
    """
    Test the discovered APIs with authentication token
    
    INSTRUCTIONS:
    1. Get your access token from Graph Explorer after signing in
    2. Replace YOUR_ACCESS_TOKEN below
    3. Run this script
    """
    
    # TODO: Replace with your actual access token from Graph Explorer
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Priority order based on web analysis
    endpoints_to_test = [
        {
            'name': 'People API (CRITICAL - has personNotes!)',
            'url': 'https://graph.microsoft.com/v1.0/me/people',
            'expected': 'personNotes field in each person object'
        },
        {
            'name': 'People API (filtered for notes)',
            'url': 'https://graph.microsoft.com/v1.0/me/people?$select=displayName,personNotes,scoredEmailAddresses',
            'expected': 'Only notes and basic info'
        },
        {
            'name': 'Shared Insights',
            'url': 'https://graph.microsoft.com/v1.0/me/insights/shared',
            'expected': 'Shared files and documents'
        },
        {
            'name': 'Trending Insights', 
            'url': 'https://graph.microsoft.com/v1.0/me/insights/trending',
            'expected': 'Trending documents'
        },
        {
            'name': 'Used Insights',
            'url': 'https://graph.microsoft.com/v1.0/me/insights/used',
            'expected': 'Recently used documents'
        },
        # Beta endpoints
        {
            'name': 'Beta People Notes (might not exist)',
            'url': 'https://graph.microsoft.com/beta/me/peopleNotes',
            'expected': 'Dedicated People Notes endpoint'
        },
        {
            'name': 'Beta Insights People Notes',
            'url': 'https://graph.microsoft.com/beta/me/insights/peopleNotes',
            'expected': 'People Notes via insights'
        }
    ]
    
    results = {}
    people_notes_found = []
    
    print('🔍 Testing Microsoft Graph APIs for People Notes')
    print('=' * 70)
    
    for endpoint in endpoints_to_test:
        try:
            print(f'\\n📡 Testing: {endpoint["name"]}')
            print(f'   🔗 URL: {endpoint["url"]}')
            
            response = requests.get(endpoint['url'], headers=headers, timeout=10)
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'expected': endpoint['expected']
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['data'] = data
                    
                    # Check for People Notes indicators
                    data_str = json.dumps(data, default=str).lower()
                    notes_indicators = ['note', 'insight', 'annotation', 'comment']
                    
                    found_indicators = [ind for ind in notes_indicators if ind in data_str]
                    
                    if found_indicators:
                        print(f'   🎯 SUCCESS! Found: {", ".join(found_indicators)}')
                        people_notes_found.append({
                            'endpoint': endpoint['name'],
                            'url': endpoint['url'],
                            'indicators': found_indicators,
                            'data_size': len(str(data))
                        })
                    else:
                        print(f'   ✅ Success, but no obvious notes found')
                    
                    print(f'   📊 Response size: {len(str(data))} characters')
                    
                    # Special handling for People API
                    if 'people' in endpoint['url'] and 'value' in data:
                        people_with_notes = [p for p in data.get('value', []) 
                                           if p.get('personNotes', '').strip()]
                        if people_with_notes:
                            print(f'   🏆 FOUND {len(people_with_notes)} people with personNotes!')
                            result['people_with_notes'] = len(people_with_notes)
                    
                except json.JSONDecodeError:
                    result['data'] = response.text
                    print(f'   ✅ Success (non-JSON response)')
                    
            elif response.status_code == 401:
                print(f'   🔐 Authentication failed - check your access token')
                
            elif response.status_code == 403:
                print(f'   🚫 Forbidden - you might need additional permissions')
                
            elif response.status_code == 404:
                print(f'   ❌ Endpoint not found')
                
            else:
                print(f'   ⚠️  Status: {response.status_code}')
                
            results[endpoint['name']] = result
            
        except requests.exceptions.RequestException as e:
            print(f'   ❌ Request failed: {e}')
            results[endpoint['name']] = {'error': str(e)}
    
    # Summary
    print(f'\\n📊 SUMMARY')
    print('=' * 70)
    
    successful_endpoints = [name for name, result in results.items() 
                          if result.get('success', False)]
    
    print(f'✅ Successful endpoints: {len(successful_endpoints)}')
    if successful_endpoints:
        for endpoint in successful_endpoints:
            print(f'   • {endpoint}')
    
    if people_notes_found:
        print(f'\\n🎯 PEOPLE NOTES FOUND!')
        for finding in people_notes_found:
            print(f'   🏆 {finding["endpoint"]}')
            print(f'       URL: {finding["url"]}')
            print(f'       Indicators: {", ".join(finding["indicators"])}')
            print(f'       Data size: {finding["data_size"]} chars')
    else:
        print(f'\\n❌ No obvious People Notes found, but check successful endpoints manually')
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'people_notes_test_results_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f'\\n💾 Results saved to: {filename}')
    
    return results

if __name__ == "__main__":
    print('🔑 BEFORE RUNNING:')
    print('   1. Go to https://developer.microsoft.com/graph/graph-explorer')
    print('   2. Sign in with your Microsoft account')
    print('   3. Run any query to authenticate')
    print('   4. Copy the access token from browser dev tools')
    print('   5. Replace YOUR_ACCESS_TOKEN_HERE in this script')
    print('   6. Run this script')
    print()
    
    test_people_notes_apis()
'''
    
    with open('test_people_notes_discovered.py', 'w') as f:
        f.write(script_content)
    
    print('\n💾 Created comprehensive test script: test_people_notes_discovered.py')

def main():
    """
    Main analysis function
    """
    
    print('🔍 Microsoft People Notes Web Analysis Results')
    print('=' * 70)
    print('📊 Based on web scraping of Microsoft Graph documentation')
    print()
    
    # Analyze findings
    findings = analyze_web_scraping_results()
    
    # Create test plan
    test_plan = create_immediate_test_plan()
    
    # Graph Explorer instructions
    instructions = create_graph_explorer_instructions()
    
    # Create test script
    create_python_test_script()
    
    print('\n💡 NEXT STEPS:')
    print('   🎯 PRIORITY 1: Test /me/people API - it has personNotes field!')
    print('   🔍 PRIORITY 2: Use Graph Explorer for quick testing')
    print('   🚀 PRIORITY 3: Use the Python script for comprehensive testing')
    print()
    print('🏆 KEY INSIGHT: The People API might already contain the People Notes data!')

if __name__ == "__main__":
    main()