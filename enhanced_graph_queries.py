#!/usr/bin/env python3
"""
Enhanced Graph Explorer Queries Based on Initial Profile Response
Using $select to get additional fields that might contain Me Notes
"""

def create_enhanced_queries():
    """
    Create enhanced queries based on the profile response
    """
    
    print('🔍 Enhanced Graph Explorer Queries for Full Personal Data')
    print('=' * 70)
    print('✅ Based on your successful /me query')
    print('💡 Using $select to get additional fields')
    print()
    
    enhanced_queries = [
        {
            'url': 'https://graph.microsoft.com/v1.0/me?$select=*',
            'purpose': 'Get ALL available fields (wildcard)',
            'priority': 'HIGH'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me?$select=aboutMe,interests,skills,responsibilities,notes,personNotes',
            'purpose': 'Target specific insight fields',
            'priority': 'HIGH'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me?$select=displayName,jobTitle,aboutMe,interests,skills,responsibilities,department,companyName',
            'purpose': 'Professional profile with insights',
            'priority': 'MEDIUM'
        },
        {
            'url': 'https://graph.microsoft.com/beta/me?$select=*',
            'purpose': 'Beta API with all fields (might have more data)',
            'priority': 'HIGH'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/profile',
            'purpose': 'Extended profile endpoint',
            'priority': 'MEDIUM'
        },
        {
            'url': 'https://graph.microsoft.com/beta/me/profile',
            'purpose': 'Beta profile endpoint',
            'priority': 'MEDIUM'
        }
    ]
    
    print('📋 Try these enhanced queries (in priority order):')
    print()
    
    for i, query in enumerate(enhanced_queries, 1):
        priority_icon = '🔥' if query['priority'] == 'HIGH' else '⚡'
        print(f'{i}. {priority_icon} {query["url"]}')
        print(f'   📝 Purpose: {query["purpose"]}')
        print()
    
    return enhanced_queries

def analyze_current_profile_data():
    """
    Analyze the profile data you already received
    """
    
    print('📊 Analysis of Your Current Profile Data')
    print('=' * 60)
    
    profile_insights = {
        'professional_role': 'SR PRINCIPAL RESEARCH MANAGER',
        'organization': 'Microsoft (cyl@microsoft.com)',
        'location': 'BEIJING-BJW-2/13463',
        'name': 'Chin-Yew Lin',
        'contact': '+86 (10) 59173481'
    }
    
    print('✅ Personal insights extracted from your profile:')
    for key, value in profile_insights.items():
        print(f'   • {key.replace("_", " ").title()}: {value}')
    
    print('\n💡 This data can be converted to Me Notes format:')
    
    me_notes_from_profile = [
        {
            'note': 'I am a Senior Principal Research Manager at Microsoft',
            'category': 'WORK_RELATED',
            'title': 'Professional Role',
            'temporal_durability': 'LONG_TERM',
            'source': 'Microsoft Graph Profile',
            'confidence': 1.0
        },
        {
            'note': 'I work in the Beijing office (BJW-2/13463) and can be reached at +86 (10) 59173481',
            'category': 'WORK_RELATED', 
            'title': 'Work Location & Contact',
            'temporal_durability': 'LONG_TERM',
            'source': 'Microsoft Graph Profile',
            'confidence': 1.0
        }
    ]
    
    for i, note in enumerate(me_notes_from_profile, 1):
        print(f'\n{i}. 📌 {note["title"]} ({note["category"]})')
        print(f'   📝 {note["note"]}')
        print(f'   🎯 Confidence: {note["confidence"]:.0%}')
    
    return me_notes_from_profile

def save_profile_based_me_notes():
    """
    Save Me Notes derived from your Graph profile
    """
    
    import json
    from datetime import datetime
    
    me_notes = analyze_current_profile_data()
    
    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'me_notes_from_graph_profile_{timestamp}.json'
    
    output = {
        'user': 'cyl@microsoft.com',
        'source': 'Microsoft Graph Profile API',
        'generated_at': datetime.now().isoformat(),
        'total_notes': len(me_notes),
        'notes': me_notes
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f'\n💾 Profile-based Me Notes saved to: {filename}')
    return filename

def main():
    """
    Main function for enhanced queries
    """
    
    print('🎯 Next Steps: Enhanced Personal Data Queries')
    print('=' * 70)
    print('✅ Your basic profile query worked!')
    print('🔍 Now let\'s get the complete data with enhanced queries')
    print()
    
    # Create enhanced queries
    enhanced_queries = create_enhanced_queries()
    
    # Analyze current data
    me_notes = analyze_current_profile_data()
    
    # Save what we have
    filename = save_profile_based_me_notes()
    
    print('\n🚀 NEXT ACTION:')
    print('   1. 🔥 Try: https://graph.microsoft.com/v1.0/me?$select=*')
    print('   2. 🔥 Try: https://graph.microsoft.com/beta/me?$select=*')
    print('   3. 🔍 Look for additional fields like aboutMe, interests, skills')
    print()
    print('💡 The $select=* will show ALL available fields in your profile!')

if __name__ == "__main__":
    main()