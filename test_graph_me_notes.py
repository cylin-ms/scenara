#!/usr/bin/env python3
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
