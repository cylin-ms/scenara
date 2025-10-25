#!/usr/bin/env python3
"""
Personal Me Notes Access - Your Own Data Only
Since you only need YOUR data, use your existing M365 authentication
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Any

def access_personal_me_notes():
    """
    Access your personal Me Notes using standard Microsoft Graph authentication
    """
    
    print('🔐 Personal Me Notes Access Strategy')
    print('=' * 60)
    print('🎯 Goal: Get YOUR Me Notes data only')
    print('✅ You have: Microsoft 365 access (cyl@microsoft.com)')
    print()
    
    # Your personal data endpoints to try
    personal_endpoints = [
        {
            'name': 'Your Profile Notes',
            'url': '/me/profile',
            'description': 'Personal profile might contain Me Notes'
        },
        {
            'name': 'Your Analytics',
            'url': '/me/analytics',
            'description': 'Personal analytics and insights'
        },
        {
            'name': 'Your Insights Summary',
            'url': '/me/insights',
            'description': 'Personal insights aggregation'
        },
        {
            'name': 'Your Activity',
            'url': '/me/activities',
            'description': 'Personal activity insights'
        },
        {
            'name': 'Your Settings',
            'url': '/me/settings',
            'description': 'User settings might contain preferences'
        },
        {
            'name': 'Beta Profile',
            'url': '/beta/me/profile',
            'description': 'Beta profile with potential Me Notes'
        },
        {
            'name': 'Beta Analytics',
            'url': '/beta/me/analytics',
            'description': 'Beta analytics with insights'
        }
    ]
    
    print('📋 Personal Data Endpoints to Test in Graph Explorer:')
    for i, endpoint in enumerate(personal_endpoints, 1):
        print(f'{i}. GET https://graph.microsoft.com{endpoint["url"]}')
        print(f'   📝 {endpoint["description"]}')
        print()
    
    return personal_endpoints

def create_simple_personal_extraction():
    """
    Create a simple script to extract your personal insights from available data
    """
    
    script_content = '''#!/usr/bin/env python3
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
            print(f'\\n📡 Testing: {endpoint}')
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
    
    print(f'\\n💾 Personal insights saved to: {filename}')
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
'''
    
    with open('extract_personal_me_notes.py', 'w') as f:
        f.write(script_content)
    
    print('💾 Created personal extraction script: extract_personal_me_notes.py')

def create_personal_me_notes_from_calendar():
    """
    Generate personal Me Notes from your calendar data (that we already have)
    """
    
    print('\n🔧 Generate Personal Me Notes from Your Calendar')
    print('=' * 60)
    
    # Load existing calendar data
    try:
        with open('real_me_notes_20251022_040030.json', 'r') as f:
            calendar_insights = json.load(f)
        
        print(f'✅ Found {len(calendar_insights)} calendar-based insights')
        
        # Convert to personal Me Notes format
        personal_me_notes = []
        
        for insight in calendar_insights:
            personal_note = {
                'note': f"I {insight['insight'].lower()}",  # Make it personal
                'category': 'WORK_RELATED',
                'title': f"My {insight.get('context', 'Activity')}",
                'temporal_durability': 'TEMPORAL_SHORT_LIVED',
                'source': 'Personal Calendar Analysis',
                'confidence': insight.get('confidence', 0.8),
                'timestamp': insight.get('timestamp', datetime.now().isoformat())
            }
            personal_me_notes.append(personal_note)
        
        # Save personal Me Notes
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'personal_me_notes_calendar_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(personal_me_notes, f, indent=2)
        
        print(f'💾 Personal Me Notes saved to: {filename}')
        
        # Show samples
        print('\n📋 Sample Personal Me Notes:')
        for i, note in enumerate(personal_me_notes[:3], 1):
            print(f'{i}. {note["title"]}')
            print(f'   📝 {note["note"]}')
            print(f'   🏷️ Category: {note["category"]}')
            print()
        
        return personal_me_notes
        
    except FileNotFoundError:
        print('❌ Calendar insights file not found')
        return None

def main():
    """
    Main function for personal Me Notes access
    """
    
    print('🎯 Personal Me Notes Access - YOUR Data Only')
    print('=' * 70)
    print('✅ Simplified approach: Focus on YOUR insights only')
    print('🔐 Using your existing Microsoft 365 authentication')
    print()
    
    # Show personal endpoints
    personal_endpoints = access_personal_me_notes()
    
    # Create extraction script
    create_simple_personal_extraction()
    
    # Generate from calendar data
    personal_notes = create_personal_me_notes_from_calendar()
    
    print('\n🎯 RECOMMENDED APPROACH:')
    print('   1. ✅ Use calendar-based personal Me Notes (ready now)')
    print('   2. 🔍 Test personal Graph endpoints in Graph Explorer')
    print('   3. 🔧 Extract additional personal insights if available')
    print('   4. 🚀 Integrate into Scenara system')
    print()
    print('💡 KEY INSIGHT: Your calendar data already provides rich personal insights!')

if __name__ == "__main__":
    main()