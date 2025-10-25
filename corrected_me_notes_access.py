#!/usr/bin/env python3
"""
Access Me Notes via MPS Canvas - Personalization V1
Since aka.ms/pint goes to feedback portal, try the alternative method
"""

import webbrowser
from datetime import datetime

def try_mps_canvas_access():
    """
    Try accessing Me Notes via MPS Canvas: Personalization V1
    """
    
    print('🔍 Trying MPS Canvas: Personalization V1')
    print('=' * 60)
    
    # Common Microsoft internal URLs for personalization
    potential_urls = [
        'https://microsoft.sharepoint.com/sites/personalization',
        'https://microsoft.sharepoint-df.com/sites/personalization',
        'https://personalization.microsoft.com',
        'https://mps.microsoft.com',
        'https://canvas.microsoft.com/personalization',
    ]
    
    print('🔗 Potential MPS Canvas URLs to try:')
    for i, url in enumerate(potential_urls, 1):
        print(f'   {i}. {url}')
    
    print('\n📋 Manual steps:')
    print('   1. Try visiting the URLs above')
    print('   2. Look for "Personalization V1" or "Me Notes" section')
    print('   3. Navigate to any personalization dashboard/canvas')
    
    # Try opening the most likely one
    primary_url = potential_urls[1]  # sharepoint-df site we found earlier
    print(f'\n🚀 Opening primary candidate: {primary_url}')
    
    try:
        webbrowser.open(primary_url)
        print('✅ Browser opened - look for Personalization V1 or Me Notes section')
    except Exception as e:
        print(f'❌ Failed to open: {e}')
    
    return potential_urls

def suggest_api_access_methods():
    """
    Suggest the API access methods mentioned in documentation
    """
    
    print('\n🔧 API Access Methods from Documentation')
    print('=' * 60)
    
    api_methods = [
        {
            'name': 'IQAPI',
            'description': 'Direct API with pre-filled query',
            'note': 'DEV debugging only - need to reach out for prod'
        },
        {
            'name': 'AnnotationStore', 
            'file': 'readMePeopleNotesFromAS.http',
            'description': 'Repository-based access',
            'note': 'DEV debugging only'
        },
        {
            'name': 'Substrate Query',
            'description': 'Query for specific person',
            'note': 'Has instructions somewhere'
        },
        {
            'name': 'EntityServe',
            'description': 'Search with "People Notes" type in ES explorer',
            'note': 'Search-based interface'
        },
        {
            'name': 'AugLoop Skills/Plugins',
            'description': 'Integration examples available',
            'note': 'Utils and DocumentRelevance example'
        }
    ]
    
    print('📋 Available API methods (for DEV debugging):')
    for method in api_methods:
        print(f'\n• {method["name"]}:')
        print(f'  📝 {method["description"]}')
        if 'file' in method:
            print(f'  📄 File: {method["file"]}')
        print(f'  ⚠️  {method["note"]}')

def search_for_me_notes_files():
    """
    Search for any Me Notes related files in the project
    """
    
    print('\n🔍 Searching for Me Notes Related Files')
    print('=' * 60)
    
    # Search patterns
    search_patterns = [
        '**/*me*notes*',
        '**/*people*notes*',
        '**/*personalization*',
        '**/*.ps1',
        '**/*.http',
        '**/*annotation*',
        '**/*substrate*',
        '**/*entity*serve*'
    ]
    
    print('🔍 Search patterns to try:')
    for pattern in search_patterns:
        print(f'   • {pattern}')
    
    return search_patterns

def create_me_notes_access_guide():
    """
    Create a guide for accessing Me Notes based on available information
    """
    
    guide_content = '''# Me Notes Access Guide
Based on me_notes_one_pager.md documentation

## Issue Found
- aka.ms/pint redirects to feedback portal, not actual Me Notes data
- Need to use alternative access methods from documentation

## Next Steps to Try

### 1. MPS Canvas: Personalization V1 (SDFv2)
- Visit Microsoft SharePoint personalization sites
- Look for "Personalization V1" section
- Navigate to Me Notes dashboard/canvas

### 2. PowerShell Script Method
- Find: me_journal_v1.ps1 
- Requires: MSIT access, DAT tool, AzVPN
- Allows: LLM API interaction with notes

### 3. API Methods (DEV debugging only)
- IQAPI: Direct API access
- AnnotationStore: readMePeopleNotesFromAS.http
- Substrate Query: Person-specific queries  
- EntityServe: Search with "People Notes" type
- AugLoop: Skills/plugins integration

### 4. File Search Needed
- Look for: "How to test Me Notes.loop" file
- Find: me_journal_v1.ps1 script
- Find: readMePeopleNotesFromAS.http file
- Find: Integration examples and utils

## Me Notes Object Structure
When accessed properly, each note contains:
- **note**: The insight text
- **category**: Type (FOLLOW_UPS, WORK_RELATED, etc.)
- **title**: Short description  
- **temporal_durability**: Duration (TEMPORAL_SHORT_LIVED, etc.)

## Expected Data Volume
- P50: 12 notes per week
- P95: 40 notes per week
- Rich user-to-user knowledge
'''
    
    with open('me_notes_access_guide.md', 'w') as f:
        f.write(guide_content)
    
    print('💾 Created access guide: me_notes_access_guide.md')

def main():
    """
    Main function to handle the corrected Me Notes access
    """
    
    print('🔄 Corrected Me Notes Access Approach')
    print('=' * 70)
    print('❌ aka.ms/pint → feedback portal (not data)')
    print('✅ Trying alternative documented methods')
    print()
    
    # Try MPS Canvas
    potential_urls = try_mps_canvas_access()
    
    # Suggest API methods
    suggest_api_access_methods()
    
    # Search for files
    search_patterns = search_for_me_notes_files()
    
    # Create guide
    create_me_notes_access_guide()
    
    print('\n🎯 IMMEDIATE ACTIONS:')
    print('   1. 🔍 Check the opened SharePoint personalization site')
    print('   2. 📄 Look for missing files: me_journal_v1.ps1, How to test Me Notes.loop')
    print('   3. 🔧 Try EntityServe with "People Notes" type if available')
    print('   4. 💬 Contact the Me Notes team for proper access instructions')

if __name__ == "__main__":
    main()