#!/usr/bin/env python3
"""
Extract Personal Me Notes from Your Available Data
Focus on YOUR insights only, using accessible Microsoft Graph endpoints
"""

import json
import requests
from datetime import datetime

def extract_personal_insights_from_graph():
    """
    Extract personal insights from Microsoft Graph using your authentication
    """
    
    print('🔍 Extracting Your Personal Insights')
    print('=' * 60)
    
    # TODO: Get your access token from Graph Explorer
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Personal endpoints that might contain insights
    endpoints = [
        'https://graph.microsoft.com/v1.0/me',
        'https://graph.microsoft.com/v1.0/me/profile',
        'https://graph.microsoft.com/beta/me/profile',
        'https://graph.microsoft.com/beta/me/analytics',
        'https://graph.microsoft.com/v1.0/me/mailboxSettings',
        'https://graph.microsoft.com/v1.0/me/outlook/taskGroups',
        'https://graph.microsoft.com/v1.0/me/todo/lists'
    ]
    
    personal_insights = []
    
    for endpoint in endpoints:
        try:
            print(f'\n📡 Testing: {endpoint}')
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract any text that looks like insights or notes
                insights = extract_insights_from_data(data, endpoint)
                personal_insights.extend(insights)
                
                print(f'   ✅ Success - found {len(insights)} insights')
            else:
                print(f'   ❌ Status: {response.status_code}')
                
        except Exception as e:
            print(f'   ❌ Error: {e}')
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'personal_me_notes_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(personal_insights, f, indent=2)
    
    print(f'\n💾 Personal insights saved to: {filename}')
    return personal_insights

def extract_insights_from_data(data, source_endpoint):
    """
    Extract insight-like information from API response data
    """
    
    insights = []
    
    # Look for fields that might contain personal insights
    insight_fields = [
        'aboutMe', 'notes', 'summary', 'description', 
        'interests', 'skills', 'responsibilities',
        'jobTitle', 'department', 'officeLocation'
    ]
    
    def search_for_insights(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.lower() in insight_fields and value:
                    insights.append({
                        'field': key,
                        'value': str(value),
                        'source': source_endpoint,
                        'path': f"{path}.{key}" if path else key,
                        'timestamp': datetime.now().isoformat()
                    })
                elif isinstance(value, (dict, list)):
                    search_for_insights(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_for_insights(item, f"{path}[{i}]")
    
    search_for_insights(data)
    return insights

if __name__ == "__main__":
    print('🔑 INSTRUCTIONS:')
    print('   1. Go to Graph Explorer: https://developer.microsoft.com/graph/graph-explorer')
    print('   2. Sign in with your Microsoft account')
    print('   3. Run any query to get authenticated')
    print('   4. Copy your access token from browser dev tools')
    print('   5. Replace YOUR_ACCESS_TOKEN_HERE in this script')
    print('   6. Run this script to extract YOUR personal insights')
    print()
    
    extract_personal_insights_from_graph()
