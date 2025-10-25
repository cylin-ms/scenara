#!/usr/bin/env python3
"""
Comprehensive Me Notes Viewer for Chin-Yew Lin
Display all Me Notes data in a beautiful, organized format
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_me_notes_files():
    """Load all Me Notes files for the user"""
    me_notes_files = {
        'real_data': 'real_me_notes_data.json',
        'enhanced_cyl': 'me_notes_cache_enhanced_cyl_microsoft_com.json', 
        'silverflow_enhanced': 'silverflow_enhanced_me_notes_20251022_045037.json',
        'projects_tasks': 'projects_tasks_me_notes_20251022_045939.json',
        'comprehensive_beta': 'me_notes_comprehensive_beta_20251022_044229.json'
    }
    
    loaded_data = {}
    for key, filename in me_notes_files.items():
        if Path(filename).exists():
            try:
                with open(filename, 'r') as f:
                    loaded_data[key] = json.load(f)
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"⚠️  Could not load {filename}: {e}")
        else:
            print(f"❌ File not found: {filename}")
    
    return loaded_data

def display_user_profile(data):
    """Display user profile information"""
    print("\n👤 USER PROFILE")
    print("=" * 60)
    
    # From SilverFlow enhanced data
    if 'silverflow_enhanced' in data:
        sf_data = data['silverflow_enhanced']
        if 'me_notes' in sf_data:
            for note in sf_data['me_notes']:
                if note.get('category') == 'professional_identity':
                    print(f"🏢 {note['note']}")
                    print(f"   📊 Confidence: {note.get('confidence_score', 'N/A')}")
                    break
    
    # From enhanced CYL data
    if 'enhanced_cyl' in data:
        cyl_data = data['enhanced_cyl']
        if 'user_context' in cyl_data:
            context = cyl_data['user_context']
            print(f"\n📧 Email: {context.get('user_email', 'N/A')}")
            print(f"🏢 Company: {context.get('company', 'N/A')}")
            print(f"🎯 Likely Roles: {', '.join(context.get('likely_roles', []))}")

def display_work_insights(data):
    """Display work-related insights"""
    print("\n💼 WORK & PROFESSIONAL INSIGHTS")
    print("=" * 60)
    
    work_notes = []
    
    # Collect work notes from all sources
    for source_name, source_data in data.items():
        if source_name == 'enhanced_cyl' and 'notes' in source_data:
            for note in source_data['notes']:
                if note.get('category') == 'WORK_RELATED':
                    work_notes.append({
                        'content': note['note'],
                        'title': note.get('title', 'Work Note'),
                        'source': 'Enhanced Analysis',
                        'confidence': note.get('confidence', 0.0),
                        'timestamp': note.get('timestamp', '')
                    })
        
        elif source_name == 'silverflow_enhanced' and 'me_notes' in source_data:
            for note in source_data['me_notes']:
                if note.get('category') in ['professional_context', 'technology_preferences']:
                    work_notes.append({
                        'content': note['note'],
                        'title': note.get('title', 'Professional Note'),
                        'source': 'SilverFlow Enhanced',
                        'confidence': note.get('confidence_score', 0.0),
                        'category': note.get('category', '')
                    })
        
        elif source_name == 'real_data' and isinstance(source_data, list):
            for note in source_data:
                if note.get('category') in ['WORK_RELATED', 'EXPERTISE']:
                    work_notes.append({
                        'content': note['note'],
                        'title': note.get('title', 'Real Data'),
                        'source': 'Real Integration',
                        'confidence': note.get('confidence', 0.0),
                        'category': note.get('category', '')
                    })
    
    # Display work notes
    for i, note in enumerate(work_notes[:8], 1):  # Show top 8
        print(f"\n📋 {i}. {note['title']}")
        print(f"   💡 {note['content']}")
        print(f"   📊 Confidence: {note['confidence']:.2f} | 📂 Source: {note['source']}")

def display_organizational_context(data):
    """Display organizational and relationship insights"""
    print("\n🏢 ORGANIZATIONAL CONTEXT")
    print("=" * 60)
    
    # From SilverFlow enhanced data
    if 'silverflow_enhanced' in data:
        sf_data = data['silverflow_enhanced']
        if 'me_notes' in sf_data:
            for note in sf_data['me_notes']:
                if note.get('category') == 'professional_context':
                    print(f"📊 {note['note']}")
                    if 'reporting_chain' in note:
                        print(f"   👥 Manager: {note['reporting_chain'].get('direct_manager', 'N/A')}")
                elif note.get('category') == 'location_preferences':
                    print(f"\n📍 {note['note']}")
                elif note.get('category') == 'communication_style':
                    print(f"\n📞 {note['note']}")
    
    # From enhanced CYL data - teams and collaborators
    if 'enhanced_cyl' in data:
        cyl_data = data['enhanced_cyl']
        if 'user_context' in cyl_data:
            context = cyl_data['user_context']
            
            if 'microsoft_teams' in context:
                print(f"\n🎯 Microsoft Teams:")
                for team in context['microsoft_teams'][:5]:
                    print(f"   • {team}")
            
            if 'likely_collaborators' in context:
                print(f"\n🤝 Frequent Collaborators:")
                for collab in context['likely_collaborators'][:6]:
                    print(f"   • {collab}")

def display_technology_ecosystem(data):
    """Display technology preferences and ecosystem"""
    print("\n💻 TECHNOLOGY ECOSYSTEM")
    print("=" * 60)
    
    # From SilverFlow enhanced data
    if 'silverflow_enhanced' in data:
        sf_data = data['silverflow_enhanced']
        if 'me_notes' in sf_data:
            for note in sf_data['me_notes']:
                if note.get('category') == 'technology_preferences':
                    print(f"🔧 {note['note']}")
                    if 'technology_matrix' in note:
                        tech = note['technology_matrix']
                        print(f"   📊 Total Services: {tech.get('total_enabled_services', 'N/A')}")
                        
                        if 'collaboration_platforms' in tech:
                            print(f"   🤝 Collaboration: {', '.join(tech['collaboration_platforms'][:3])}...")
                        if 'productivity_tools' in tech:
                            print(f"   ⚡ Productivity: {', '.join(tech['productivity_tools'])}")
    
    # From enhanced CYL data
    if 'enhanced_cyl' in data:
        cyl_data = data['enhanced_cyl']
        if 'user_context' in cyl_data:
            context = cyl_data['user_context']
            if 'common_projects' in context:
                print(f"\n🚀 Common Microsoft Projects:")
                for project in context['common_projects']:
                    print(f"   • {project}")

def display_recent_activities(data):
    """Display recent activities and projects"""
    print("\n📅 RECENT ACTIVITIES & PROJECTS")
    print("=" * 60)
    
    activities = []
    
    # Collect from all sources with timestamps
    for source_name, source_data in data.items():
        if source_name == 'enhanced_cyl' and 'notes' in source_data:
            for note in source_data['notes']:
                activities.append({
                    'content': note['note'],
                    'title': note.get('title', 'Activity'),
                    'timestamp': note.get('timestamp', ''),
                    'confidence': note.get('confidence', 0.0)
                })
        
        elif source_name == 'projects_tasks' and isinstance(source_data, dict) and 'notes' in source_data:
            for note in source_data['notes']:
                activities.append({
                    'content': note['note'],
                    'title': note.get('title', 'Project Activity'),
                    'timestamp': note.get('timestamp', ''),
                    'confidence': note.get('confidence', 0.0)
                })
    
    # Sort by timestamp (most recent first)
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Display recent activities
    for i, activity in enumerate(activities[:6], 1):
        timestamp = activity['timestamp'][:10] if activity['timestamp'] else 'Recent'
        print(f"\n📋 {i}. {activity['title']} ({timestamp})")
        print(f"   💡 {activity['content']}")
        print(f"   📊 Confidence: {activity['confidence']:.2f}")

def display_data_sources_summary(data):
    """Display summary of data sources"""
    print("\n📊 DATA SOURCES SUMMARY")
    print("=" * 60)
    
    for source_name, source_data in data.items():
        print(f"\n📂 {source_name.replace('_', ' ').title()}:")
        
        if isinstance(source_data, list):
            print(f"   📋 {len(source_data)} notes")
        elif isinstance(source_data, dict):
            if 'notes' in source_data:
                print(f"   📋 {len(source_data['notes'])} notes")
            if 'generation_metadata' in source_data:
                metadata = source_data['generation_metadata']
                print(f"   📅 Generated: {metadata.get('generated_at', 'N/A')[:10]}")
                print(f"   🔧 Method: {metadata.get('method', 'N/A')}")
            if 'user_context' in source_data:
                print(f"   👤 User Context: Available")

def main():
    """Main function to display comprehensive Me Notes"""
    print("🎯 CHIN-YEW LIN - COMPREHENSIVE ME NOTES")
    print("=" * 80)
    print(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📧 User: cyl@microsoft.com")
    print("🏢 Organization: Microsoft")
    
    # Load all Me Notes data
    data = load_me_notes_files()
    
    if not data:
        print("\n❌ No Me Notes data found!")
        return
    
    # Display comprehensive information
    display_user_profile(data)
    display_work_insights(data)
    display_organizational_context(data)
    display_technology_ecosystem(data)
    display_recent_activities(data)
    display_data_sources_summary(data)
    
    print("\n" + "=" * 80)
    print("📋 Summary: Comprehensive Me Notes displaying professional intelligence")
    print("🎯 Sources: Real data integration + Enhanced analysis + SilverFlow patterns")
    print("📈 Status: Multi-source intelligence aggregation successful")

if __name__ == "__main__":
    main()