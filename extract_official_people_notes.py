#!/usr/bin/env python3
"""
Microsoft People Notes API Extraction
Extract your People Notes data from the SharePoint interface
"""

import requests
import json
from datetime import datetime

def extract_people_notes_api():
    """
    Extract People Notes using discovered API endpoints
    """
    
    # TODO: Replace with actual endpoints discovered from SharePoint page
    potential_endpoints = [
        # These will be discovered from browser dev tools
        "https://graph.microsoft.com/v1.0/me/insights/peopleNotes",
        "https://graph.microsoft.com/beta/me/insights/peopleNotes", 
        "https://microsoft.sharepoint-df.com/sites/personalization/_api/...",
        # Add actual endpoints found in Network tab
    ]
    
    # TODO: Replace with actual authentication method
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # From browser or existing auth
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    results = {}
    
    for endpoint in potential_endpoints:
        try:
            print(f"🔍 Testing: {endpoint}")
            response = requests.get(endpoint, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                results[endpoint] = {
                    'status': 'SUCCESS',
                    'data': data,
                    'note_count': len(data.get('value', []))
                }
                print(f"   ✅ Success! Found {results[endpoint]['note_count']} notes")
            else:
                results[endpoint] = {
                    'status': 'FAILED',
                    'status_code': response.status_code,
                    'error': response.text
                }
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            results[endpoint] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"   ❌ Error: {e}")
    
    return results

def save_official_people_notes(data):
    """
    Save official People Notes data in our format
    """
    
    # Convert to our Me Notes format
    me_notes_format = {
        'user_email': 'cyl@microsoft.com',
        'data_source': 'OFFICIAL_MICROSOFT_PEOPLE_NOTES',
        'generation_method': 'OFFICIAL_API_EXTRACTION',
        'official_me_notes_api': True,
        'extracted_at': datetime.now().isoformat() + 'Z',
        'me_notes': data.get('value', []),
        'metadata': {
            'total_notes': len(data.get('value', [])),
            'source_authenticity': 'OFFICIAL_MICROSOFT_API',
            'extraction_method': 'SharePoint_People_Notes_Interface'
        }
    }
    
    # Save to our cache format
    with open('official_me_notes_cache_cyl_microsoft_com.json', 'w') as f:
        json.dump(me_notes_format, f, indent=2)
    
    print(f"💾 Saved official People Notes to: official_me_notes_cache_cyl_microsoft_com.json")

# Usage instructions will be filled in based on your SharePoint exploration
