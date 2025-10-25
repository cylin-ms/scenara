#!/usr/bin/env python3
"""
Me Notes Viewer Tool
Interactive tool for fetching and displaying Microsoft Me Notes in beautiful formats
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MeNotesCategory(Enum):
    """Me Notes categories"""
    WORK_RELATED = "WORK_RELATED"
    EXPERTISE = "EXPERTISE" 
    BEHAVIORAL_PATTERN = "BEHAVIORAL_PATTERN"
    INTERESTS = "INTERESTS"
    FOLLOW_UPS = "FOLLOW_UPS"
    COLLABORATION = "COLLABORATION"
    DECISION_MAKING = "DECISION_MAKING"

class TemporalDurability(Enum):
    """Temporal durability levels"""
    TEMPORAL_SHORT_LIVED = "TEMPORAL_SHORT_LIVED"  # Days to weeks
    TEMPORAL_MEDIUM_LIVED = "TEMPORAL_MEDIUM_LIVED"  # Weeks to months
    TEMPORAL_LONG_LIVED = "TEMPORAL_LONG_LIVED"  # Months to years

@dataclass
class MeNote:
    """Structure representing a Me Note from Microsoft's system"""
    note: str
    category: MeNotesCategory
    title: str
    temporal_durability: TemporalDurability
    timestamp: datetime
    confidence: float = 0.8
    source: str = "M365"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class MeNotesAPI:
    """Me Notes API integration (simulated for demo)"""
    
    def __init__(self, user_email: str):
        self.user_email = user_email
        self.api_base = "https://graph.microsoft.com/v1.0"
        self.cache_file = Path(f"me_notes_cache_{user_email.replace('@', '_').replace('.', '_')}.json")
        
    def fetch_me_notes(self, days_back: int = 30, category_filter: List[str] = None) -> List[MeNote]:
        """Fetch Me Notes from API or simulation"""
        # For demo purposes, we'll simulate realistic Me Notes data
        # In production, this would connect to actual Microsoft Me Notes APIs
        
        logger.info(f"📡 Fetching Me Notes for {self.user_email} (last {days_back} days)")
        
        if self.cache_file.exists():
            logger.info("📂 Loading from cache...")
            return self._load_from_cache()
        
        # Simulate Me Notes data
        simulated_notes = self._generate_realistic_me_notes(days_back)
        
        # Apply category filter if specified
        if category_filter:
            filtered_categories = [MeNotesCategory(cat) for cat in category_filter]
            simulated_notes = [note for note in simulated_notes if note.category in filtered_categories]
        
        # Cache the results
        self._save_to_cache(simulated_notes)
        
        logger.info(f"✅ Retrieved {len(simulated_notes)} Me Notes")
        return simulated_notes
    
    def _generate_realistic_me_notes(self, days_back: int) -> List[MeNote]:
        """Generate realistic Me Notes data for demonstration"""
        base_time = datetime.now()
        notes = []
        
        # Work-related notes
        work_notes = [
            ("Working on Priority Calendar project with advanced meeting intelligence", "Priority Calendar Project Progress", 
             TemporalDurability.TEMPORAL_MEDIUM_LIVED, 1),
            ("Leading LLM integration initiative for enterprise productivity tools", "LLM Integration Leadership",
             TemporalDurability.TEMPORAL_LONG_LIVED, 3),
            ("Collaborating with Microsoft Graph team on calendar API enhancements", "Graph API Collaboration",
             TemporalDurability.TEMPORAL_SHORT_LIVED, 5),
            ("Developing meeting intelligence frameworks for large organizations", "Meeting Intelligence Development",
             TemporalDurability.TEMPORAL_MEDIUM_LIVED, 7),
            ("Researching AI-powered productivity optimization solutions", "AI Productivity Research",
             TemporalDurability.TEMPORAL_LONG_LIVED, 10),
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
                metadata={"project": "Priority Calendar", "team": "Productivity AI"}
            ))
        
        # Expertise notes
        expertise_notes = [
            ("Expert in calendar intelligence and meeting optimization algorithms", "Calendar Intelligence Expertise",
             TemporalDurability.TEMPORAL_LONG_LIVED, 2),
            ("Deep knowledge of Microsoft Graph API and Office 365 integrations", "Graph API Expertise",
             TemporalDurability.TEMPORAL_LONG_LIVED, 4),
            ("Specialist in AI/ML integration for enterprise productivity solutions", "AI/ML Integration Specialist",
             TemporalDurability.TEMPORAL_LONG_LIVED, 6),
            ("Proficient in Python development and LLM framework integration", "Python & LLM Development",
             TemporalDurability.TEMPORAL_LONG_LIVED, 8),
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
                metadata={"skill_level": "Expert", "years_experience": "5+"}
            ))
        
        # Behavioral patterns
        behavioral_notes = [
            ("Prefers morning meetings for strategic discussions and decision-making", "Morning Strategic Preference",
             TemporalDurability.TEMPORAL_LONG_LIVED, 12),
            ("Carefully analyzes options before making critical decisions", "Analytical Decision Style",
             TemporalDurability.TEMPORAL_LONG_LIVED, 15),
            ("Values detailed preparation for important meetings", "Preparation-Focused Approach",
             TemporalDurability.TEMPORAL_LONG_LIVED, 18),
            ("Prefers collaborative problem-solving over individual work", "Collaborative Work Style",
             TemporalDurability.TEMPORAL_LONG_LIVED, 20),
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
                metadata={"pattern_strength": "Strong", "frequency": "Consistent"}
            ))
        
        # Interests
        interest_notes = [
            ("Passionate about productivity optimization and time management", "Productivity Optimization Interest",
             TemporalDurability.TEMPORAL_LONG_LIVED, 14),
            ("Interested in enterprise AI applications and automation", "Enterprise AI Interest",
             TemporalDurability.TEMPORAL_MEDIUM_LIVED, 16),
            ("Follows developments in calendar intelligence and smart scheduling", "Calendar Intelligence Interest",
             TemporalDurability.TEMPORAL_LONG_LIVED, 22),
            ("Enjoys learning about Microsoft Graph ecosystem and APIs", "Graph Ecosystem Interest",
             TemporalDurability.TEMPORAL_MEDIUM_LIVED, 25),
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
                metadata={"interest_level": "High", "engagement": "Active"}
            ))
        
        # Follow-ups and recent interactions
        followup_notes = [
            ("Recent discussion with Jane Smith about Priority Calendar integration timeline", "Jane Smith Follow-up",
             TemporalDurability.TEMPORAL_SHORT_LIVED, 2),
            ("Action item: Review LLM integration proposal with AI team by Friday", "AI Team Review Action",
             TemporalDurability.TEMPORAL_SHORT_LIVED, 4),
            ("Follow up with Graph API team on calendar enhancement specifications", "Graph Team Follow-up",
             TemporalDurability.TEMPORAL_SHORT_LIVED, 6),
            ("Pending response to meeting intelligence framework documentation review", "Documentation Review Pending",
             TemporalDurability.TEMPORAL_SHORT_LIVED, 8),
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
                metadata={"urgency": "Medium", "status": "Pending"}
            ))
        
        return notes
    
    def _save_to_cache(self, notes: List[MeNote]):
        """Save notes to cache file"""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "user_email": self.user_email,
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
        
        logger.info(f"💾 Cached {len(notes)} notes to {self.cache_file}")
    
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

class MeNotesFormatter:
    """Format Me Notes for various output formats"""
    
    @staticmethod
    def to_markdown(notes: List[MeNote], user_email: str) -> str:
        """Generate beautiful Markdown report"""
        
        # Group notes by category
        categorized = {}
        for note in notes:
            if note.category not in categorized:
                categorized[note.category] = []
            categorized[note.category].append(note)
        
        # Sort each category by timestamp (newest first)
        for category in categorized:
            categorized[category].sort(key=lambda x: x.timestamp, reverse=True)
        
        # Generate markdown
        md_content = f"""# 🧠 Me Notes Report for {user_email}

*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*

---

## 📊 **Summary**

- **Total Notes**: {len(notes)}
- **Categories**: {len(categorized)}
- **Date Range**: {min(note.timestamp for note in notes).strftime('%Y-%m-%d')} to {max(note.timestamp for note in notes).strftime('%Y-%m-%d')}
- **Average Confidence**: {sum(note.confidence for note in notes) / len(notes):.1%}

---

"""

        # Category icons
        category_icons = {
            MeNotesCategory.WORK_RELATED: "💼",
            MeNotesCategory.EXPERTISE: "🎯", 
            MeNotesCategory.BEHAVIORAL_PATTERN: "🧭",
            MeNotesCategory.INTERESTS: "💡",
            MeNotesCategory.FOLLOW_UPS: "📋",
            MeNotesCategory.COLLABORATION: "🤝",
            MeNotesCategory.DECISION_MAKING: "⚖️"
        }
        
        # Add each category
        for category, notes_in_category in categorized.items():
            icon = category_icons.get(category, "📝")
            category_name = category.value.replace('_', ' ').title()
            
            md_content += f"""## {icon} **{category_name}**

*{len(notes_in_category)} insights*

"""
            
            for i, note in enumerate(notes_in_category, 1):
                # Durability indicator
                durability_icons = {
                    TemporalDurability.TEMPORAL_SHORT_LIVED: "⏰",
                    TemporalDurability.TEMPORAL_MEDIUM_LIVED: "📅", 
                    TemporalDurability.TEMPORAL_LONG_LIVED: "📆"
                }
                durability_icon = durability_icons.get(note.temporal_durability, "📝")
                
                # Confidence indicator
                confidence_indicator = "🟢" if note.confidence >= 0.9 else "🟡" if note.confidence >= 0.7 else "🔴"
                
                md_content += f"""### {i}. {note.title}

**Note**: {note.note}

**Details**: 
- {durability_icon} **Durability**: {note.temporal_durability.value.replace('TEMPORAL_', '').replace('_', ' ').title()}
- {confidence_indicator} **Confidence**: {note.confidence:.1%}
- 📅 **Date**: {note.timestamp.strftime('%B %d, %Y')}
- 📡 **Source**: {note.source}

"""
                
                # Add metadata if available
                if note.metadata:
                    md_content += "**Additional Context**:\n"
                    for key, value in note.metadata.items():
                        md_content += f"- **{key.replace('_', ' ').title()}**: {value}\n"
                
                md_content += "\n---\n\n"
        
        # Add insights summary
        md_content += f"""## 🎯 **Key Insights**

### **Current Focus Areas**
"""
        
        # Extract work-related projects
        work_notes = [n for n in notes if n.category == MeNotesCategory.WORK_RELATED]
        if work_notes:
            md_content += "- **Active Projects**: "
            projects = set()
            for note in work_notes:
                if "Priority Calendar" in note.note:
                    projects.add("Priority Calendar")
                if "LLM" in note.note or "AI" in note.note:
                    projects.add("AI/LLM Integration")
                if "Graph" in note.note:
                    projects.add("Microsoft Graph")
            md_content += ", ".join(projects) + "\n"
        
        # Extract expertise areas
        expertise_notes = [n for n in notes if n.category == MeNotesCategory.EXPERTISE]
        if expertise_notes:
            md_content += "- **Key Expertise**: "
            expertise_areas = [note.title for note in expertise_notes[:3]]
            md_content += ", ".join(expertise_areas) + "\n"
        
        # Extract behavioral patterns
        behavioral_notes = [n for n in notes if n.category == MeNotesCategory.BEHAVIORAL_PATTERN]
        if behavioral_notes:
            md_content += "- **Work Patterns**: "
            patterns = [note.title for note in behavioral_notes[:2]]
            md_content += ", ".join(patterns) + "\n"
        
        md_content += f"""
### **Engagement Level**
- **High Confidence Notes**: {len([n for n in notes if n.confidence >= 0.9])}
- **Recent Activity**: {len([n for n in notes if (datetime.now() - n.timestamp).days <= 7])} notes in last week
- **Follow-up Items**: {len([n for n in notes if n.category == MeNotesCategory.FOLLOW_UPS])}

---

*📝 This report was generated by the Me Notes Viewer Tool*  
*🔄 Refresh by running: `python me_notes_viewer.py --user {user_email}`*
"""
        
        return md_content
    
    @staticmethod
    def to_html(notes: List[MeNote], user_email: str) -> str:
        """Generate beautiful HTML report"""
        
        # Group and sort notes
        categorized = {}
        for note in notes:
            if note.category not in categorized:
                categorized[note.category] = []
            categorized[note.category].append(note)
        
        for category in categorized:
            categorized[category].sort(key=lambda x: x.timestamp, reverse=True)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Me Notes Report - {user_email}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }}
        
        .summary {{
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .summary-item {{
            text-align: center;
        }}
        
        .summary-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
        }}
        
        .category {{
            margin: 40px 0;
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .category-header {{
            background: linear-gradient(135deg, #55a3ff 0%, #003d82 100%);
            color: white;
            padding: 20px;
            font-size: 1.3em;
            font-weight: bold;
        }}
        
        .note {{
            padding: 25px;
            border-bottom: 1px solid #f0f0f0;
            transition: background-color 0.3s;
        }}
        
        .note:hover {{
            background-color: #f8f9ff;
        }}
        
        .note:last-child {{
            border-bottom: none;
        }}
        
        .note-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .note-content {{
            color: #5a6c7d;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        
        .note-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            font-size: 0.9em;
        }}
        
        .detail-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .confidence-high {{ color: #27ae60; }}
        .confidence-medium {{ color: #f39c12; }}
        .confidence-low {{ color: #e74c3c; }}
        
        .insights {{
            background: linear-gradient(135deg, #a8e6cf 0%, #56ab2f 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 40px 0;
        }}
        
        .insights h3 {{
            color: white;
            margin-top: 0;
        }}
        
        .insights ul {{
            list-style-type: none;
            padding: 0;
        }}
        
        .insights li {{
            background: rgba(255,255,255,0.1);
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 8px;
            border-left: 4px solid rgba(255,255,255,0.3);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Me Notes Report</h1>
        <p style="text-align: center; color: #7f8c8d; font-size: 1.1em;">
            Generated for <strong>{user_email}</strong> on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </p>
        
        <div class="summary">
            <div class="summary-item">
                <span class="summary-number">{len(notes)}</span>
                <span>Total Notes</span>
            </div>
            <div class="summary-item">
                <span class="summary-number">{len(categorized)}</span>
                <span>Categories</span>
            </div>
            <div class="summary-item">
                <span class="summary-number">{sum(note.confidence for note in notes) / len(notes):.0%}</span>
                <span>Avg Confidence</span>
            </div>
            <div class="summary-item">
                <span class="summary-number">{len([n for n in notes if (datetime.now() - n.timestamp).days <= 7])}</span>
                <span>Recent Notes</span>
            </div>
        </div>
"""

        # Category icons
        category_icons = {
            MeNotesCategory.WORK_RELATED: "💼",
            MeNotesCategory.EXPERTISE: "🎯", 
            MeNotesCategory.BEHAVIORAL_PATTERN: "🧭",
            MeNotesCategory.INTERESTS: "💡",
            MeNotesCategory.FOLLOW_UPS: "📋",
            MeNotesCategory.COLLABORATION: "🤝",
            MeNotesCategory.DECISION_MAKING: "⚖️"
        }
        
        # Add categories
        for category, notes_in_category in categorized.items():
            icon = category_icons.get(category, "📝")
            category_name = category.value.replace('_', ' ').title()
            
            html_content += f"""
        <div class="category">
            <div class="category-header">
                {icon} {category_name} ({len(notes_in_category)} insights)
            </div>
"""
            
            for note in notes_in_category:
                confidence_class = "confidence-high" if note.confidence >= 0.9 else "confidence-medium" if note.confidence >= 0.7 else "confidence-low"
                confidence_icon = "🟢" if note.confidence >= 0.9 else "🟡" if note.confidence >= 0.7 else "🔴"
                
                durability_icons = {
                    TemporalDurability.TEMPORAL_SHORT_LIVED: "⏰",
                    TemporalDurability.TEMPORAL_MEDIUM_LIVED: "📅", 
                    TemporalDurability.TEMPORAL_LONG_LIVED: "📆"
                }
                durability_icon = durability_icons.get(note.temporal_durability, "📝")
                
                html_content += f"""
            <div class="note">
                <div class="note-title">{note.title}</div>
                <div class="note-content">{note.note}</div>
                <div class="note-details">
                    <div class="detail-item">
                        {durability_icon} <strong>Durability:</strong> {note.temporal_durability.value.replace('TEMPORAL_', '').replace('_', ' ').title()}
                    </div>
                    <div class="detail-item">
                        <span class="{confidence_class}">{confidence_icon} <strong>Confidence:</strong> {note.confidence:.1%}</span>
                    </div>
                    <div class="detail-item">
                        📅 <strong>Date:</strong> {note.timestamp.strftime('%B %d, %Y')}
                    </div>
                    <div class="detail-item">
                        📡 <strong>Source:</strong> {note.source}
                    </div>
                </div>
            </div>
"""
            
            html_content += "        </div>\n"
        
        # Add insights
        work_notes = [n for n in notes if n.category == MeNotesCategory.WORK_RELATED]
        expertise_notes = [n for n in notes if n.category == MeNotesCategory.EXPERTISE]
        behavioral_notes = [n for n in notes if n.category == MeNotesCategory.BEHAVIORAL_PATTERN]
        followup_notes = [n for n in notes if n.category == MeNotesCategory.FOLLOW_UPS]
        
        html_content += f"""
        <div class="insights">
            <h3>🎯 Key Insights</h3>
            <ul>
                <li><strong>Active Projects:</strong> Priority Calendar, AI/LLM Integration, Microsoft Graph</li>
                <li><strong>Core Expertise:</strong> Calendar Intelligence, Graph API, AI/ML Integration</li>
                <li><strong>Work Style:</strong> Morning strategic meetings, collaborative approach, detail-oriented</li>
                <li><strong>Current Focus:</strong> {len(work_notes)} work items, {len(followup_notes)} pending follow-ups</li>
                <li><strong>Engagement Level:</strong> {len([n for n in notes if n.confidence >= 0.9])} high-confidence insights</li>
            </ul>
        </div>
        
        <div class="footer">
            📝 Generated by Me Notes Viewer Tool<br>
            🔄 Refresh by running: <code>python me_notes_viewer.py --user {user_email}</code>
        </div>
    </div>
</body>
</html>"""
        
        return html_content

class MeNotesViewer:
    """Main Me Notes Viewer Tool"""
    
    def __init__(self):
        self.output_dir = Path("me_notes_reports")
        self.output_dir.mkdir(exist_ok=True)
    
    def fetch_and_display(self, user_email: str, format_type: str = "both", 
                         days_back: int = 30, category_filter: List[str] = None) -> Dict[str, str]:
        """Fetch and display Me Notes in specified format(s)"""
        
        print(f"🧠 Me Notes Viewer - Fetching data for {user_email}")
        print("=" * 60)
        
        # Initialize API and fetch notes
        api = MeNotesAPI(user_email)
        notes = api.fetch_me_notes(days_back=days_back, category_filter=category_filter)
        
        if not notes:
            print("❌ No Me Notes found")
            return {}
        
        print(f"✅ Found {len(notes)} Me Notes")
        
        # Generate reports
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_safe = user_email.replace('@', '_').replace('.', '_')
        
        if format_type in ["markdown", "both"]:
            print("📝 Generating Markdown report...")
            markdown_content = MeNotesFormatter.to_markdown(notes, user_email)
            
            md_file = self.output_dir / f"me_notes_{user_safe}_{timestamp}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            results['markdown'] = str(md_file)
            print(f"✅ Markdown report saved: {md_file}")
        
        if format_type in ["html", "both"]:
            print("🌐 Generating HTML report...")
            html_content = MeNotesFormatter.to_html(notes, user_email)
            
            html_file = self.output_dir / f"me_notes_{user_safe}_{timestamp}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            results['html'] = str(html_file)
            print(f"✅ HTML report saved: {html_file}")
        
        # Display summary
        print("\n📊 Me Notes Summary:")
        print(f"   📧 User: {user_email}")
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
        
        print(f"\n🎯 Reports generated in: {self.output_dir}")
        
        return results

def main():
    """Command-line interface for Me Notes Viewer"""
    parser = argparse.ArgumentParser(description="Me Notes Viewer Tool")
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
        viewer = MeNotesViewer()
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
                print(f"🌐 Opening HTML report in browser...")
                webbrowser.open(f"file://{Path(results['html']).absolute()}")
            
            if 'markdown' in results:
                print(f"📝 Opening Markdown report...")
                try:
                    subprocess.run(['code', results['markdown']], check=True)
                except:
                    print(f"📝 Markdown report available at: {results['markdown']}")
        
        print("\n✅ Me Notes Viewer completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()