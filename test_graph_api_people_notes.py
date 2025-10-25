#!/usr/bin/env python3
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
            print(f'\n📡 Testing: {endpoint}')
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
    print(f'\n📊 Summary:')
    print(f'   ✅ Successful endpoints: {len(successful_endpoints)}')
    print(f'   ❌ Failed endpoints: {len(endpoints) - len(successful_endpoints)}')
    
    if successful_endpoints:
        print(f'\n🎯 Successful endpoints to investigate:')
        for endpoint in successful_endpoints:
            print(f'   • {endpoint}')
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'graph_api_test_results_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f'\n💾 Results saved to: {filename}')
    
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
