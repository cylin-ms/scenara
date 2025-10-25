#!/usr/bin/env python3
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
            print(f'\n📡 Testing: {endpoint["name"]}')
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
    print(f'\n📊 SUMMARY')
    print('=' * 70)
    
    successful_endpoints = [name for name, result in results.items() 
                          if result.get('success', False)]
    
    print(f'✅ Successful endpoints: {len(successful_endpoints)}')
    if successful_endpoints:
        for endpoint in successful_endpoints:
            print(f'   • {endpoint}')
    
    if people_notes_found:
        print(f'\n🎯 PEOPLE NOTES FOUND!')
        for finding in people_notes_found:
            print(f'   🏆 {finding["endpoint"]}')
            print(f'       URL: {finding["url"]}')
            print(f'       Indicators: {", ".join(finding["indicators"])}')
            print(f'       Data size: {finding["data_size"]} chars')
    else:
        print(f'\n❌ No obvious People Notes found, but check successful endpoints manually')
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'people_notes_test_results_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f'\n💾 Results saved to: {filename}')
    
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
