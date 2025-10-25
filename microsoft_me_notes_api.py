#!/usr/bin/env python3
"""
Microsoft Me Notes API Compatibility Layer
Provides access methods aligned with official Microsoft Me Notes specification
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class MeNotesAPI:
    """
    Microsoft Me Notes API compatibility layer
    Implements access patterns from official Me Notes specification
    """
    
    def __init__(self, user_email: str = "cyl@microsoft.com"):
        self.user_email = user_email
        self.cache_file = f'me_notes_cache_{user_email.replace("@", "_").replace(".", "_")}.json'
    
    def query_me_notes(self, category: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Query Me Notes using Microsoft-compatible format
        
        Args:
            category: Filter by category (WORK_RELATED, COLLABORATION, etc.)
            limit: Maximum number of notes to return
            
        Returns:
            List of Me Notes in Microsoft format
        """
        if not os.path.exists(self.cache_file):
            return []
        
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        notes = data.get('me_notes', [])
        
        # Filter by category if specified
        if category:
            notes = [note for note in notes if note.get('category') == category]
        
        # Apply limit if specified
        if limit:
            notes = notes[:limit]
        
        # Convert to Microsoft format
        microsoft_format_notes = []
        for note in notes:
            ms_note = {
                'note': note['note'],
                'title': note.get('title', 'Untitled'),
                'category': note['category'],
                'durability': note['durability'],
                'confidence': note.get('confidence', 0.85),
                'source': note.get('source', 'CALENDAR_DATA'),
                'data_authenticity': note.get('data_authenticity', 'REAL_USER_DATA'),
                'generated_at': note.get('generated_at', datetime.now().isoformat() + 'Z')
            }
            microsoft_format_notes.append(ms_note)
        
        return microsoft_format_notes
    
    def get_categories(self) -> List[str]:
        """Get all available categories in the Me Notes"""
        if not os.path.exists(self.cache_file):
            return []
        
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        notes = data.get('me_notes', [])
        categories = list(set(note.get('category', 'UNKNOWN') for note in notes))
        return sorted(categories)
    
    def get_note_distribution(self) -> Dict[str, int]:
        """Get distribution of notes by category (Microsoft-style analytics)"""
        if not os.path.exists(self.cache_file):
            return {}
        
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        notes = data.get('me_notes', [])
        distribution = {}
        
        for note in notes:
            category = note.get('category', 'UNKNOWN')
            distribution[category] = distribution.get(category, 0) + 1
        
        return distribution
    
    def get_user_summary(self) -> Dict[str, Any]:
        """Get comprehensive user summary from Me Notes"""
        if not os.path.exists(self.cache_file):
            return {}
        
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        notes = data.get('me_notes', [])
        metadata = data.get('metadata', {})
        
        return {
            'user_email': self.user_email,
            'data_source': data.get('data_source', 'UNKNOWN'),
            'total_notes': len(notes),
            'categories': self.get_categories(),
            'distribution': self.get_note_distribution(),
            'confidence_range': metadata.get('confidence_range', '0.00-0.00'),
            'data_authenticity': metadata.get('data_authenticity', 'UNKNOWN'),
            'last_updated': data.get('last_updated', ''),
            'total_meetings_analyzed': data.get('total_meetings_analyzed', 0),
            'unique_collaborators': metadata.get('unique_collaborators', 0)
        }

def demonstrate_microsoft_access_patterns():
    """Demonstrate official Microsoft Me Notes access patterns"""
    
    print('🧠 Microsoft Me Notes API Compatibility Demo')
    print('=' * 60)
    
    # Initialize API
    api = MeNotesAPI()
    
    # Get user summary (similar to aka.ms/pint)
    print('\n📊 User Summary (aka.ms/pint style):')
    summary = api.get_user_summary()
    for key, value in summary.items():
        print(f'   {key}: {value}')
    
    # Query all notes (similar to EntityServe)
    print('\n📝 All Me Notes (EntityServe style):')
    all_notes = api.query_me_notes()
    for i, note in enumerate(all_notes, 1):
        print(f'   {i}. [{note["category"]}] {note["title"]}')
        print(f'      Note: {note["note"][:80]}...')
        print(f'      Durability: {note["durability"]} | Confidence: {note["confidence"]*100:.0f}%')
        print()
    
    # Query by category (similar to IQAPI filtering)
    print('\n🎯 Work-Related Notes (IQAPI style filtering):')
    work_notes = api.query_me_notes(category='WORK_RELATED')
    for note in work_notes:
        print(f'   • {note["title"]}: {note["note"]}')
    
    # Get distribution (similar to analytics in MPS canvas)
    print('\n📈 Note Distribution (MPS Canvas analytics):')
    distribution = api.get_note_distribution()
    for category, count in distribution.items():
        print(f'   {category}: {count} notes')
    
    print('\n✅ Microsoft Me Notes compatibility demonstration complete!')

def main():
    """Main function for CLI usage"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'demo':
            demonstrate_microsoft_access_patterns()
        elif sys.argv[1] == 'query':
            api = MeNotesAPI()
            category = sys.argv[2] if len(sys.argv) > 2 else None
            notes = api.query_me_notes(category=category)
            
            print(json.dumps(notes, indent=2, ensure_ascii=False))
        elif sys.argv[1] == 'summary':
            api = MeNotesAPI()
            summary = api.get_user_summary()
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print('Usage:')
            print('  python microsoft_me_notes_api.py demo     # Show compatibility demo')
            print('  python microsoft_me_notes_api.py query    # Query all notes')
            print('  python microsoft_me_notes_api.py query WORK_RELATED  # Query by category')
            print('  python microsoft_me_notes_api.py summary  # Get user summary')
    else:
        demonstrate_microsoft_access_patterns()

if __name__ == "__main__":
    main()