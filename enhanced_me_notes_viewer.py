#!/usr/bin/env python3
"""
Enhanced Me Notes Viewer with User-Specific Simulation
Generates more realistic data based on user context
"""

import json
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import sys
from enum import Enum
import re

# Import from existing me_notes_viewer
sys.path.append(str(Path(__file__).parent))
from me_notes_viewer import (
    MeNotesCategory, TemporalDurability, MeNote, 
    MeNotesFormatter, MeNotesViewer
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedMeNotesAPI:
    """Enhanced Me Notes API with user-specific simulation"""
    
    def __init__(self, user_email: str):
        self.user_email = user_email
        self.api_base = "https://graph.microsoft.com/v1.0"
        self.cache_file = Path(f"me_notes_cache_enhanced_{user_email.replace('@', '_').replace('.', '_')}.json")
        
        # Extract user context from email
        self.user_context = self._analyze_user_context(user_email)
        
    def _analyze_user_context(self, email: str) -> Dict[str, Any]:
        """Analyze user email to generate context-specific data"""
        
        domain = email.split('@')[1] if '@' in email else 'company.com'
        username = email.split('@')[0] if '@' in email else email
        
        # Microsoft-specific context
        if 'microsoft.com' in domain:
            return {
                'company': 'Microsoft',
                'domain': 'microsoft.com',
                'username': username,
                'likely_roles': ['Senior Engineer', 'Product Manager', 'Researcher', 'Technical Lead'],
                'common_projects': ['Office 365', 'Microsoft Graph', 'Azure', 'Teams', 'Copilot'],
                'likely_collaborators': [
                    'Sarah Chen', 'Mike Johnson', 'David Park', 'Lisa Rodriguez', 
                    'Alex Kim', 'Maria Garcia', 'James Wilson', 'Emily Zhang'
                ],
                'microsoft_teams': [
                    'Graph API team', 'Office Platform team', 'AI Research team',
                    'Productivity team', 'Security team', 'Data Platform team'
                ]
            }
        else:
            # Generic company context
            return {
                'company': domain.split('.')[0].title(),
                'domain': domain,
                'username': username,
                'likely_roles': ['Engineer', 'Manager', 'Analyst', 'Developer'],
                'common_projects': ['Product Development', 'Platform Integration', 'Customer Solutions'],
                'likely_collaborators': [
                    'John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Wilson'
                ],
                'microsoft_teams': ['Development team', 'Product team', 'Engineering team']
            }
    
    def fetch_me_notes(self, days_back: int = 30, category_filter: List[str] = None) -> List[MeNote]:
        """Fetch Me Notes with user-specific simulation"""
        
        logger.info(f"📡 Fetching enhanced Me Notes for {self.user_email} (last {days_back} days)")
        
        if self.cache_file.exists():
            logger.info("📂 Loading from enhanced cache...")
            return self._load_from_cache()
        
        # Generate user-specific simulated notes
        simulated_notes = self._generate_user_specific_me_notes(days_back)
        
        # Apply category filter if specified
        if category_filter:
            filtered_categories = [MeNotesCategory(cat) for cat in category_filter]
            simulated_notes = [note for note in simulated_notes if note.category in filtered_categories]
        
        # Cache the results
        self._save_to_cache(simulated_notes)
        
        logger.info(f"✅ Retrieved {len(simulated_notes)} user-specific Me Notes")
        return simulated_notes
    
    def _generate_user_specific_me_notes(self, days_back: int) -> List[MeNote]:
        """Generate user-specific realistic Me Notes data"""
        base_time = datetime.now()
        notes = []
        ctx = self.user_context
        
        # Work-related notes - Microsoft specific
        if 'microsoft.com' in ctx['domain']:
            work_notes = [
                (f"Leading Priority Calendar project with advanced meeting intelligence at {ctx['company']}", 
                 "Priority Calendar Project Leadership", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 1),
                (f"Collaborating with {ctx['microsoft_teams'][0]} on calendar API enhancements", 
                 f"{ctx['microsoft_teams'][0]} Collaboration", TemporalDurability.TEMPORAL_SHORT_LIVED, 3),
                (f"Developing meeting intelligence frameworks for enterprise customers", 
                 "Meeting Intelligence Development", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 5),
                (f"Research on AI-powered productivity optimization for Office 365", 
                 "AI Productivity Research", TemporalDurability.TEMPORAL_LONG_LIVED, 7),
                (f"Integration work with Microsoft Graph APIs for calendar intelligence", 
                 "Graph API Integration", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 10),
            ]
        else:
            work_notes = [
                (f"Working on Priority Calendar project with advanced meeting intelligence", 
                 "Priority Calendar Project Progress", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 1),
                (f"Leading integration initiative for enterprise productivity tools", 
                 "Integration Leadership", TemporalDurability.TEMPORAL_LONG_LIVED, 3),
                (f"Collaborating with external teams on calendar API enhancements", 
                 "External API Collaboration", TemporalDurability.TEMPORAL_SHORT_LIVED, 5),
            ]
        
        for note_text, title, durability, days_ago in work_notes:
            notes.append(MeNote(
                note=note_text,
                category=MeNotesCategory.WORK_RELATED,
                title=title,
                temporal_durability=durability,
                timestamp=base_time - timedelta(days=days_ago),
                confidence=0.9,
                source="Teams/Outlook",
                metadata={"project": "Priority Calendar", "company": ctx['company']}
            ))
        
        # Expertise notes - context-aware
        expertise_notes = [
            (f"Expert in calendar intelligence and meeting optimization algorithms", 
             "Calendar Intelligence Expertise", TemporalDurability.TEMPORAL_LONG_LIVED, 2),
            (f"Deep knowledge of {ctx['company']} APIs and enterprise integrations", 
             f"{ctx['company']} API Expertise", TemporalDurability.TEMPORAL_LONG_LIVED, 4),
            (f"Specialist in AI/ML integration for productivity solutions", 
             "AI/ML Integration Specialist", TemporalDurability.TEMPORAL_LONG_LIVED, 6),
            (f"Proficient in enterprise software development and system architecture", 
             "Enterprise Development Expert", TemporalDurability.TEMPORAL_LONG_LIVED, 8),
        ]
        
        for note_text, title, durability, days_ago in expertise_notes:
            notes.append(MeNote(
                note=note_text,
                category=MeNotesCategory.EXPERTISE,
                title=title,
                temporal_durability=durability,
                timestamp=base_time - timedelta(days=days_ago),
                confidence=0.95,
                source="Performance Reviews/Feedback",
                metadata={"skill_level": "Expert", "domain": ctx['company']}
            ))
        
        # Behavioral patterns
        behavioral_notes = [
            ("Prefers morning meetings for strategic discussions and technical planning", 
             "Morning Strategic Preference", TemporalDurability.TEMPORAL_LONG_LIVED, 12),
            ("Systematically analyzes technical options before implementation decisions", 
             "Analytical Technical Approach", TemporalDurability.TEMPORAL_LONG_LIVED, 15),
            ("Values thorough documentation and preparation for technical reviews", 
             "Documentation-Focused Approach", TemporalDurability.TEMPORAL_LONG_LIVED, 18),
            ("Collaborates effectively across teams and technical disciplines", 
             "Cross-team Collaboration Style", TemporalDurability.TEMPORAL_LONG_LIVED, 20),
        ]
        
        for note_text, title, durability, days_ago in behavioral_notes:
            notes.append(MeNote(
                note=note_text,
                category=MeNotesCategory.BEHAVIORAL_PATTERN,
                title=title,
                temporal_durability=durability,
                timestamp=base_time - timedelta(days=days_ago),
                confidence=0.85,
                source="Meeting Transcripts/Behavioral Analysis",
                metadata={"pattern_strength": "Strong", "context": "Technical Leadership"}
            ))
        
        # Interests - domain-specific
        if 'microsoft.com' in ctx['domain']:
            interest_notes = [
                ("Passionate about AI integration in productivity tools and Office ecosystem", 
                 "AI Productivity Integration Interest", TemporalDurability.TEMPORAL_LONG_LIVED, 14),
                ("Interested in Microsoft Graph capabilities and developer ecosystem", 
                 "Graph Ecosystem Interest", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 16),
                ("Follows developments in meeting intelligence and smart calendar technology", 
                 "Meeting Intelligence Interest", TemporalDurability.TEMPORAL_LONG_LIVED, 22),
                ("Enjoys learning about enterprise AI applications and automation frameworks", 
                 "Enterprise AI Interest", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 25),
            ]
        else:
            interest_notes = [
                ("Passionate about productivity optimization and time management solutions", 
                 "Productivity Optimization Interest", TemporalDurability.TEMPORAL_LONG_LIVED, 14),
                ("Interested in enterprise AI applications and automation", 
                 "Enterprise AI Interest", TemporalDurability.TEMPORAL_MEDIUM_LIVED, 16),
                ("Follows developments in calendar intelligence and smart scheduling", 
                 "Calendar Intelligence Interest", TemporalDurability.TEMPORAL_LONG_LIVED, 22),
            ]
        
        for note_text, title, durability, days_ago in interest_notes:
            notes.append(MeNote(
                note=note_text,
                category=MeNotesCategory.INTERESTS,
                title=title,
                temporal_durability=durability,
                timestamp=base_time - timedelta(days=days_ago),
                confidence=0.8,
                source="Search History/Document Access",
                metadata={"interest_level": "High", "domain": ctx['company']}
            ))
        
        # Follow-ups and recent interactions - realistic names
        collaborators = ctx['likely_collaborators']
        teams = ctx['microsoft_teams']
        
        followup_notes = [
            (f"Recent technical discussion with {collaborators[0]} about Priority Calendar architecture", 
             f"{collaborators[0]} Follow-up", TemporalDurability.TEMPORAL_SHORT_LIVED, 2),
            (f"Action item: Review integration proposal with {teams[0]} by end of week", 
             f"{teams[0]} Review Action", TemporalDurability.TEMPORAL_SHORT_LIVED, 4),
            (f"Follow up with {collaborators[1]} on calendar enhancement specifications", 
             f"{collaborators[1]} Technical Follow-up", TemporalDurability.TEMPORAL_SHORT_LIVED, 6),
            (f"Pending response from {teams[1]} on meeting intelligence framework documentation", 
             f"{teams[1]} Documentation Review", TemporalDurability.TEMPORAL_SHORT_LIVED, 8),
        ]
        
        for note_text, title, durability, days_ago in followup_notes:
            notes.append(MeNote(
                note=note_text,
                category=MeNotesCategory.FOLLOW_UPS,
                title=title,
                temporal_durability=durability,
                timestamp=base_time - timedelta(days=days_ago),
                confidence=0.9,
                source="Email/Teams Messages",
                metadata={"urgency": "Medium", "context": ctx['company']}
            ))
        
        return notes
    
    def _save_to_cache(self, notes: List[MeNote]):
        """Save notes to cache file"""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "user_email": self.user_email,
            "user_context": self.user_context,
            "notes": []
        }
        
        for note in notes:
            note_dict = asdict(note)
            note_dict['category'] = note.category.value
            note_dict['temporal_durability'] = note.temporal_durability.value
            note_dict['timestamp'] = note.timestamp.isoformat()
            cache_data["notes"].append(note_dict)
        
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        logger.info(f"💾 Cached {len(notes)} enhanced notes to {self.cache_file}")
    
    def _load_from_cache(self) -> List[MeNote]:
        """Load notes from cache file"""
        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)
        
        notes = []
        for note_dict in cache_data["notes"]:
            note_dict['category'] = MeNotesCategory(note_dict['category'])
            note_dict['temporal_durability'] = TemporalDurability(note_dict['temporal_durability'])
            note_dict['timestamp'] = datetime.fromisoformat(note_dict['timestamp'])
            notes.append(MeNote(**note_dict))
        
        return notes

class EnhancedMeNotesViewer(MeNotesViewer):
    """Enhanced Me Notes Viewer with user-specific simulation"""
    
    def fetch_and_display(self, user_email: str, format_type: str = "both", 
                         days_back: int = 30, category_filter: List[str] = None) -> Dict[str, str]:
        """Fetch and display Me Notes with enhanced user-specific simulation"""
        
        print(f"🧠 Enhanced Me Notes Viewer - Fetching data for {user_email}")
        print("=" * 60)
        
        # Use enhanced API
        api = EnhancedMeNotesAPI(user_email)
        notes = api.fetch_me_notes(days_back=days_back, category_filter=category_filter)
        
        if not notes:
            print("❌ No Me Notes found")
            return {}
        
        print(f"✅ Found {len(notes)} user-specific Me Notes")
        
        # Show user context info
        print(f"🏢 Detected context: {api.user_context['company']} ({api.user_context['domain']})")
        
        # Generate reports using existing formatter
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_safe = user_email.replace('@', '_').replace('.', '_')
        
        if format_type in ["markdown", "both"]:
            print("📝 Generating enhanced Markdown report...")
            markdown_content = MeNotesFormatter.to_markdown(notes, user_email)
            
            md_file = self.output_dir / f"me_notes_enhanced_{user_safe}_{timestamp}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            results['markdown'] = str(md_file)
            print(f"✅ Enhanced Markdown report saved: {md_file}")
        
        if format_type in ["html", "both"]:
            print("🌐 Generating enhanced HTML report...")
            html_content = MeNotesFormatter.to_html(notes, user_email)
            
            html_file = self.output_dir / f"me_notes_enhanced_{user_safe}_{timestamp}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            results['html'] = str(html_file)
            print(f"✅ Enhanced HTML report saved: {html_file}")
        
        # Display enhanced summary
        print("\n📊 Enhanced Me Notes Summary:")
        print(f"   📧 User: {user_email}")
        print(f"   🏢 Context: {api.user_context['company']} environment")
        print(f"   📅 Date Range: {min(note.timestamp for note in notes).strftime('%Y-%m-%d')} to {max(note.timestamp for note in notes).strftime('%Y-%m-%d')}")
        print(f"   📈 Total Notes: {len(notes)}")
        
        # Category breakdown
        categorized = {}
        for note in notes:
            categorized[note.category] = categorized.get(note.category, 0) + 1
        
        print("   📋 By Category:")
        for category, count in categorized.items():
            icon = {"WORK_RELATED": "💼", "EXPERTISE": "🎯", "BEHAVIORAL_PATTERN": "🧭", 
                   "INTERESTS": "💡", "FOLLOW_UPS": "📋"}.get(category.value, "📝")
            print(f"      {icon} {category.value.replace('_', ' ').title()}: {count}")
        
        print(f"\n🎯 Enhanced reports generated in: {self.output_dir}")
        
        return results

def main():
    """Enhanced CLI interface"""
    parser = argparse.ArgumentParser(description="Enhanced Me Notes Viewer Tool with User-Specific Simulation")
    parser.add_argument("--user", "-u", required=True, help="User email address")
    parser.add_argument("--format", "-f", choices=["markdown", "html", "both"], 
                       default="both", help="Output format (default: both)")
    parser.add_argument("--days", "-d", type=int, default=30, 
                       help="Days back to fetch notes (default: 30)")
    parser.add_argument("--category", "-c", action="append", 
                       choices=["WORK_RELATED", "EXPERTISE", "BEHAVIORAL_PATTERN", 
                               "INTERESTS", "FOLLOW_UPS", "COLLABORATION", "DECISION_MAKING"],
                       help="Filter by category (can be used multiple times)")
    parser.add_argument("--open", "-o", action="store_true", 
                       help="Open generated reports in browser/editor")
    
    args = parser.parse_args()
    
    try:
        viewer = EnhancedMeNotesViewer()
        results = viewer.fetch_and_display(
            user_email=args.user,
            format_type=args.format,
            days_back=args.days,
            category_filter=args.category
        )
        
        # Optionally open files
        if args.open and results:
            import webbrowser
            import subprocess
            
            if 'html' in results:
                print(f"🌐 Opening enhanced HTML report in browser...")
                webbrowser.open(f"file://{Path(results['html']).absolute()}")
            
            if 'markdown' in results:
                print(f"📝 Opening enhanced Markdown report...")
                try:
                    subprocess.run(['code', results['markdown']], check=True)
                except:
                    print(f"📝 Enhanced Markdown report available at: {results['markdown']}")
        
        print("\n✅ Enhanced Me Notes Viewer completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()