#!/usr/bin/env python3
"""
Me Notes Access Following Official Instructions
Based on me_notes_one_pager.md - using the documented methods
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Any

def analyze_me_notes_access_methods():
    """
    Analyze the official Me Notes access methods from the documentation
    """
    
    print('📋 Official Me Notes Access Methods')
    print('=' * 60)
    print('📖 Based on me_notes_one_pager.md instructions')
    print()
    
    access_methods = {
        'viewing_and_interaction': [
            {
                'method': 'PINT Portal',
                'url': 'aka.ms/pint',
                'access': 'SDFv2 only',
                'description': 'Primary portal for viewing Me Notes'
            },
            {
                'method': 'MPS Canvas',
                'url': 'Personalization V1',
                'access': 'SDFv2',
                'description': 'Canvas interface for Me Notes'
            },
            {
                'method': 'PowerShell Script',
                'file': 'me_journal_v1.ps1',
                'access': 'MSIT, use DAT tool and AzVPN',
                'description': 'LLM API interaction with notes'
            }
        ],
        'api_integrations': [
            {
                'method': 'IQAPI',
                'access': 'DEV debugging only',
                'description': 'Direct API access with pre-filled query'
            },
            {
                'method': 'AnnotationStore',
                'file': 'readMePeopleNotesFromAS.http',
                'access': 'DEV debugging only',
                'description': 'Repository-based access'
            },
            {
                'method': 'Substrate Query',
                'access': 'Specific person queries',
                'description': 'Advanced query interface'
            },
            {
                'method': 'EntityServe',
                'type': 'People Notes',
                'access': 'ES explorer',
                'description': 'Search-based access'
            },
            {
                'method': 'AugLoop Skills/Plugins',
                'access': 'Utils and integration examples',
                'description': 'Plugin-based integration'
            }
        ]
    }
    
    print('🔍 VIEWING AND LIGHT INTERACTIONS:')
    for method in access_methods['viewing_and_interaction']:
        print(f'  • {method["method"]}')
        if 'url' in method:
            print(f'    🔗 URL: {method["url"]}')
        if 'file' in method:
            print(f'    📄 File: {method["file"]}')
        print(f'    🔐 Access: {method["access"]}')
        print(f'    📝 {method["description"]}')
        print()
    
    print('🔧 API INTEGRATIONS (DEV DEBUGGING):')
    for method in access_methods['api_integrations']:
        print(f'  • {method["method"]}')
        if 'file' in method:
            print(f'    📄 File: {method["file"]}')
        if 'type' in method:
            print(f'    🏷️ Type: {method["type"]}')
        print(f'    🔐 Access: {method["access"]}')
        print(f'    📝 {method["description"]}')
        print()
    
    return access_methods

def implement_proper_me_notes_access():
    """
    Implement the proper Me Notes access following the documentation
    """
    
    print('🚀 Implementing Proper Me Notes Access')
    print('=' * 60)
    
    # Priority 1: PINT Portal (aka.ms/pint)
    print('🔥 PRIORITY 1: PINT Portal Access')
    print('   🔗 URL: https://aka.ms/pint')
    print('   📋 This is the PRIMARY method for viewing Me Notes')
    print('   ✅ You already have SDFv2 access (Microsoft employee)')
    print()
    
    # Open PINT portal
    import webbrowser
    try:
        webbrowser.open('https://aka.ms/pint')
        print('✅ PINT portal opened in browser')
    except Exception as e:
        print(f'❌ Failed to open browser: {e}')
    
    return True

def create_me_notes_object_parser():
    """
    Create parser for Me Notes objects based on documentation
    """
    
    parser_content = '''#!/usr/bin/env python3
"""
Me Notes Object Parser
Based on the official Me Notes object structure from documentation
"""

import json
from datetime import datetime
from typing import Dict, List, Any

class MeNotesObject:
    """
    Official Me Notes object structure
    """
    
    def __init__(self, note_data: Dict[str, Any]):
        self.note = note_data.get('note', '')  # The actual note text
        self.category = note_data.get('category', '')  # Type (FOLLOW_UPS, WORK_RELATED, etc.)
        self.title = note_data.get('title', '')  # Short description
        self.temporal_durability = note_data.get('temporal_durability', '')  # TEMPORAL_SHORT_LIVED, etc.
        self.raw_data = note_data
    
    def to_scenara_format(self) -> Dict[str, Any]:
        """
        Convert Me Notes object to Scenara format
        """
        
        return {
            'person': 'Me (User)',
            'insight': self.note,
            'category': self.category,
            'title': self.title,
            'temporal_durability': self.temporal_durability,
            'source': 'Official Microsoft Me Notes',
            'confidence': 1.0,
            'timestamp': datetime.now().isoformat()
        }
    
    def __str__(self):
        return f"Me Note: {self.title} ({self.category}) - {self.note[:50]}..."

def parse_me_notes_response(response_data):
    """
    Parse Me Notes API response into structured objects
    """
    
    me_notes = []
    
    if isinstance(response_data, list):
        # Array of notes
        for note_data in response_data:
            me_notes.append(MeNotesObject(note_data))
    elif isinstance(response_data, dict):
        if 'value' in response_data:
            # Microsoft Graph-style response
            for note_data in response_data['value']:
                me_notes.append(MeNotesObject(note_data))
        else:
            # Single note object
            me_notes.append(MeNotesObject(response_data))
    
    return me_notes

def convert_to_scenara_format(me_notes: List[MeNotesObject]) -> List[Dict[str, Any]]:
    """
    Convert Me Notes to Scenara format for integration
    """
    
    scenara_notes = []
    
    for note in me_notes:
        scenara_note = note.to_scenara_format()
        scenara_notes.append(scenara_note)
    
    return scenara_notes

# Example usage
if __name__ == "__main__":
    # Example Me Notes object (based on documentation)
    example_note = {
        'note': 'Reza is working on Project Atlas and focusing on sustainability initiatives',
        'category': 'WORK_RELATED',
        'title': 'Project Atlas Work',
        'temporal_durability': 'TEMPORAL_SHORT_LIVED'
    }
    
    note_obj = MeNotesObject(example_note)
    print('📋 Example Me Notes Object:')
    print(f'   📝 Note: {note_obj.note}')
    print(f'   🏷️ Category: {note_obj.category}')
    print(f'   📌 Title: {note_obj.title}')
    print(f'   ⏱️ Temporal: {note_obj.temporal_durability}')
    
    scenara_format = note_obj.to_scenara_format()
    print('\\n🔄 Converted to Scenara format:')
    print(json.dumps(scenara_format, indent=2))
'''
    
    with open('me_notes_object_parser.py', 'w') as f:
        f.write(parser_content)
    
    print('💾 Created Me Notes object parser: me_notes_object_parser.py')

def next_steps_following_documentation():
    """
    Outline next steps following the official documentation
    """
    
    print('\n🎯 Next Steps Following Official Documentation')
    print('=' * 60)
    
    steps = [
        {
            'step': 1,
            'action': 'Access PINT Portal',
            'details': 'Visit aka.ms/pint to view your Me Notes',
            'priority': 'CRITICAL'
        },
        {
            'step': 2,
            'action': 'Examine Me Notes Structure',
            'details': 'Look for note, category, title, temporal_durability fields',
            'priority': 'HIGH'
        },
        {
            'step': 3,
            'action': 'Try MPS Canvas',
            'details': 'Use Personalization V1 interface as backup',
            'priority': 'MEDIUM'
        },
        {
            'step': 4,
            'action': 'PowerShell Script (if needed)',
            'details': 'Use me_journal_v1.ps1 for LLM API interaction',
            'priority': 'LOW'
        },
        {
            'step': 5,
            'action': 'Integrate with Scenara',
            'details': 'Parse Me Notes objects and integrate into Scenara system',
            'priority': 'HIGH'
        }
    ]
    
    for step in steps:
        priority_icon = '🔥' if step['priority'] == 'CRITICAL' else '⚡' if step['priority'] == 'HIGH' else '💡'
        print(f'{step["step"]}. {priority_icon} {step["action"]}')
        print(f'   📝 {step["details"]}')
        print()

def main():
    """
    Main function following official documentation
    """
    
    print('📖 Following Official Me Notes Documentation')
    print('=' * 70)
    print('📄 Based on: me_notes_one_pager.md')
    print()
    
    # Analyze official methods
    access_methods = analyze_me_notes_access_methods()
    
    # Implement proper access
    implement_proper_me_notes_access()
    
    # Create parser
    create_me_notes_object_parser()
    
    # Next steps
    next_steps_following_documentation()
    
    print('\n💡 APOLOGY:')
    print('   🙏 You were right - I should have read the documentation first')
    print('   📋 The me_notes_one_pager.md has all the proper access methods')
    print('   🔗 Primary method: aka.ms/pint portal')
    print('   📊 Proper object structure with note/category/title/temporal fields')

if __name__ == "__main__":
    main()