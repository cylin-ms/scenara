#!/usr/bin/env python3
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
    print('\n🔄 Converted to Scenara format:')
    print(json.dumps(scenara_format, indent=2))
