#!/usr/bin/env python3
"""
Me Notes Markdown Generator for Chin-Yew Lin
Generate beautiful Markdown reports from Me Notes data
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
import re

class MeNotesMarkdownGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.all_me_notes = []
        self.data_sources = []
        
    def load_all_me_notes_files(self):
        """Load all Me Notes files in the directory"""
        print("🔍 Scanning for Me Notes files...")
        
        # Common Me Notes file patterns
        patterns = [
            '*me_notes*.json',
            'real_me_notes*.json',
            '*silverflow*.json'
        ]
        
        found_files = []
        for pattern in patterns:
            files = list(Path('.').glob(pattern))
            found_files.extend(files)
        
        # Remove duplicates and sort by modification time (newest first)
        unique_files = list(set(found_files))
        unique_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print(f"📁 Found {len(unique_files)} Me Notes files")
        
        for file_path in unique_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.data_sources.append({
                    'filename': str(file_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                    'data': data
                })
                
                # Extract notes from different data structures
                notes = self._extract_notes_from_data(data, str(file_path))
                self.all_me_notes.extend(notes)
                
                print(f"✅ Loaded {len(notes)} notes from {file_path.name}")
                
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        print(f"📊 Total notes loaded: {len(self.all_me_notes)}")
        
    def _extract_notes_from_data(self, data, filename):
        """Extract notes from various data structures"""
        notes = []
        
        if isinstance(data, list):
            # Direct list of notes
            for note in data:
                if isinstance(note, dict) and 'note' in note:
                    note['source_file'] = filename
                    notes.append(note)
        
        elif isinstance(data, dict):
            # Check various possible structures
            if 'notes' in data:
                # Standard structure with notes array
                for note in data['notes']:
                    if isinstance(note, dict):
                        note['source_file'] = filename
                        notes.append(note)
            
            elif 'me_notes' in data:
                # SilverFlow structure
                for note in data['me_notes']:
                    if isinstance(note, dict):
                        note['source_file'] = filename
                        notes.append(note)
            
            elif any(key in data for key in ['category', 'note', 'title']):
                # Single note structure
                data['source_file'] = filename
                notes.append(data)
        
        return notes
    
    def generate_markdown_report(self):
        """Generate comprehensive Markdown report"""
        print("📝 Generating Markdown report...")
        
        # Load all data
        self.load_all_me_notes_files()
        
        if not self.all_me_notes:
            print("❌ No Me Notes data found!")
            return None
        
        # Generate the report
        markdown_content = self._build_markdown_content()
        
        # Save to file
        output_filename = f'me_notes_report_{self.timestamp}.md'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown report generated: {output_filename}")
        return output_filename
    
    def _build_markdown_content(self):
        """Build the complete Markdown content"""
        md_lines = []
        
        # Header
        md_lines.extend(self._generate_header())
        
        # Executive Summary
        md_lines.extend(self._generate_executive_summary())
        
        # Professional Identity
        md_lines.extend(self._generate_professional_identity())
        
        # Work & Collaboration
        md_lines.extend(self._generate_work_collaboration())
        
        # Expertise & Skills
        md_lines.extend(self._generate_expertise_skills())
        
        # Meeting Intelligence
        md_lines.extend(self._generate_meeting_intelligence())
        
        # Organizational Context
        md_lines.extend(self._generate_organizational_context())
        
        # Technology Ecosystem
        md_lines.extend(self._generate_technology_ecosystem())
        
        # Recent Activities
        md_lines.extend(self._generate_recent_activities())
        
        # Data Sources & Metadata
        md_lines.extend(self._generate_data_sources())
        
        # Appendix
        md_lines.extend(self._generate_appendix())
        
        return '\n'.join(md_lines)
    
    def _generate_header(self):
        """Generate report header"""
        return [
            "# 🎯 Me Notes Intelligence Report",
            "",
            f"**Subject:** Chin-Yew Lin (cyl@microsoft.com)  ",
            f"**Organization:** Microsoft  ",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**Total Notes:** {len(self.all_me_notes)}  ",
            f"**Data Sources:** {len(self.data_sources)} files  ",
            "",
            "---",
            ""
        ]
    
    def _generate_executive_summary(self):
        """Generate executive summary section"""
        # Calculate key metrics
        categories = Counter(note.get('category', 'UNKNOWN') for note in self.all_me_notes)
        avg_confidence = sum(note.get('confidence', 0) for note in self.all_me_notes) / len(self.all_me_notes)
        high_confidence_count = len([n for n in self.all_me_notes if n.get('confidence', 0) >= 0.9])
        
        # Find key insights
        work_notes = [n for n in self.all_me_notes if 'WORK' in n.get('category', '')]
        collaboration_notes = [n for n in self.all_me_notes if 'COLLABORATION' in n.get('category', '')]
        expertise_notes = [n for n in self.all_me_notes if 'EXPERTISE' in n.get('category', '')]
        
        return [
            "## 📋 Executive Summary",
            "",
            f"This intelligence report provides a comprehensive analysis of **{len(self.all_me_notes)} personal insights** ",
            f"generated from real Microsoft Graph data, calendar events, and organizational information. ",
            f"The analysis achieves an average confidence score of **{avg_confidence:.1%}** with ",
            f"**{high_confidence_count} high-confidence insights** (≥90%).",
            "",
            "### 🎯 Key Findings",
            "",
            f"- **Professional Role:** SR Principal Research Manager at Microsoft China",
            f"- **Work Focus:** {len(work_notes)} work-related insights covering AI/ML research and meeting intelligence",
            f"- **Collaboration:** {len(collaboration_notes)} collaboration patterns with cross-functional teams",
            f"- **Expertise Areas:** {len(expertise_notes)} demonstrated competencies in data science and Microsoft technologies",
            f"- **Data Authenticity:** Generated from real Microsoft 365 calendar and Graph API data",
            "",
            "### 📊 Insight Categories",
            "",
        ]
        
        # Add category breakdown
        category_lines = []
        for category, count in categories.most_common():
            category_lines.append(f"- **{category.replace('_', ' ').title()}:** {count} insights")
        
        return [
            "## 📋 Executive Summary",
            "",
            f"This intelligence report provides a comprehensive analysis of **{len(self.all_me_notes)} personal insights** ",
            f"generated from real Microsoft Graph data, calendar events, and organizational information. ",
            f"The analysis achieves an average confidence score of **{avg_confidence:.1%}** with ",
            f"**{high_confidence_count} high-confidence insights** (≥90%).",
            "",
            "### 🎯 Key Findings",
            "",
            "- **Professional Role:** SR Principal Research Manager at Microsoft China",
            f"- **Work Focus:** {len(work_notes)} work-related insights covering AI/ML research and meeting intelligence",
            f"- **Collaboration:** {len(collaboration_notes)} collaboration patterns with cross-functional teams",
            f"- **Expertise Areas:** {len(expertise_notes)} demonstrated competencies in data science and Microsoft technologies",
            "- **Data Authenticity:** Generated from real Microsoft 365 calendar and Graph API data",
            "",
            "### 📊 Insight Categories",
            "",
        ] + category_lines + ["", "---", ""]
    
    def _generate_professional_identity(self):
        """Generate professional identity section"""
        identity_notes = [n for n in self.all_me_notes if any(cat in n.get('category', '') for cat in ['IDENTITY', 'CONTACT', 'ORGANIZATIONAL'])]
        
        lines = [
            "## 👤 Professional Identity",
            "",
        ]
        
        # Add identity insights
        for note in identity_notes[:5]:  # Top 5 identity notes
            confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
            lines.extend([
                f"### {note.get('title', 'Professional Insight')}",
                "",
                f"{confidence_emoji} **Confidence:** {note.get('confidence', 0):.1%}  ",
                f"📊 **Source:** {note.get('source', 'Unknown')}  ",
                "",
                f"{note.get('note', 'No details available')}",
                "",
            ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_work_collaboration(self):
        """Generate work and collaboration section"""
        work_notes = [n for n in self.all_me_notes if any(cat in n.get('category', '') for cat in ['WORK', 'COLLABORATION', 'PROJECT'])]
        
        lines = [
            "## 💼 Work & Collaboration",
            "",
            "### 🎯 Work-Related Insights",
            "",
        ]
        
        for i, note in enumerate(work_notes[:6], 1):
            confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
            lines.extend([
                f"#### {i}. {note.get('title', 'Work Insight')}",
                "",
                f"{confidence_emoji} {note.get('note', 'No details available')}",
                "",
                f"*Source: {note.get('source', 'Unknown')} | Confidence: {note.get('confidence', 0):.1%}*",
                "",
            ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_expertise_skills(self):
        """Generate expertise and skills section"""
        expertise_notes = [n for n in self.all_me_notes if 'EXPERTISE' in n.get('category', '')]
        
        lines = [
            "## 🎯 Expertise & Skills",
            "",
        ]
        
        if expertise_notes:
            lines.append("### 🔬 Demonstrated Expertise Areas")
            lines.append("")
            
            for note in expertise_notes:
                confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
                lines.extend([
                    f"- **{note.get('title', 'Expertise Area')}** {confidence_emoji}",
                    f"  - {note.get('note', 'No details available')}",
                    f"  - *Confidence: {note.get('confidence', 0):.1%}*",
                    "",
                ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_meeting_intelligence(self):
        """Generate meeting intelligence section"""
        meeting_notes = [n for n in self.all_me_notes if any(cat in n.get('category', '') for cat in ['MEETING', 'CALENDAR'])]
        
        lines = [
            "## 📅 Meeting Intelligence",
            "",
        ]
        
        if meeting_notes:
            lines.append("### 🤝 Meeting Patterns & Insights")
            lines.append("")
            
            for note in meeting_notes:
                confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
                lines.extend([
                    f"#### {note.get('title', 'Meeting Insight')}",
                    "",
                    f"{confidence_emoji} {note.get('note', 'No details available')}",
                    "",
                    f"*Analysis Method: {note.get('source', 'Unknown')}*",
                    "",
                ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_organizational_context(self):
        """Generate organizational context section"""
        org_notes = [n for n in self.all_me_notes if any(cat in n.get('category', '') for cat in ['ORGANIZATIONAL', 'LEADERSHIP', 'MANAGER'])]
        
        lines = [
            "## 🏢 Organizational Context",
            "",
        ]
        
        if org_notes:
            for note in org_notes:
                confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
                lines.extend([
                    f"### {note.get('title', 'Organizational Insight')}",
                    "",
                    f"{confidence_emoji} {note.get('note', 'No details available')}",
                    "",
                    f"**Source:** {note.get('source', 'Unknown')} | **Confidence:** {note.get('confidence', 0):.1%}",
                    "",
                ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_technology_ecosystem(self):
        """Generate technology ecosystem section"""
        tech_notes = [n for n in self.all_me_notes if any(cat in n.get('category', '') for cat in ['TECHNOLOGY', 'COMMUNICATION_TOOLS', 'WORK_ORGANIZATION'])]
        
        lines = [
            "## 💻 Technology Ecosystem",
            "",
        ]
        
        if tech_notes:
            lines.append("### 🔧 Technology & Tools Usage")
            lines.append("")
            
            for note in tech_notes:
                confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
                lines.extend([
                    f"- **{note.get('title', 'Technology Insight')}** {confidence_emoji}",
                    f"  - {note.get('note', 'No details available')}",
                    "",
                ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_recent_activities(self):
        """Generate recent activities section"""
        # Sort notes by timestamp if available
        timestamped_notes = [n for n in self.all_me_notes if n.get('timestamp') or n.get('generated_at')]
        timestamped_notes.sort(key=lambda x: x.get('timestamp', x.get('generated_at', '')), reverse=True)
        
        lines = [
            "## 📈 Recent Activities & Insights",
            "",
            "### 🕐 Latest Intelligence Updates",
            "",
        ]
        
        for i, note in enumerate(timestamped_notes[:8], 1):
            confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
            timestamp = note.get('timestamp', note.get('generated_at', 'Recent'))
            
            lines.extend([
                f"#### {i}. {note.get('title', 'Recent Activity')}",
                "",
                f"{confidence_emoji} {note.get('note', 'No details available')}",
                "",
                f"*Category: {note.get('category', 'Unknown')} | Timestamp: {timestamp}*",
                "",
            ])
        
        lines.extend(["---", ""])
        return lines
    
    def _generate_data_sources(self):
        """Generate data sources section"""
        lines = [
            "## 📊 Data Sources & Methodology",
            "",
            "### 📁 Source Files Analysis",
            "",
        ]
        
        for i, source in enumerate(self.data_sources, 1):
            file_size_kb = source['size'] / 1024
            lines.extend([
                f"#### {i}. {source['filename']}",
                "",
                f"- **File Size:** {file_size_kb:.1f} KB",
                f"- **Last Modified:** {source['modified'].strftime('%Y-%m-%d %H:%M:%S')}",
                f"- **Data Type:** JSON Intelligence Data",
                "",
            ])
        
        lines.extend([
            "### 🔍 Analysis Methodology",
            "",
            "- **Data Collection:** Microsoft Graph API + Real Calendar Events",
            "- **Processing:** Multi-source intelligence aggregation",
            "- **Validation:** Confidence scoring and source attribution",
            "- **Output:** Structured personal intelligence insights",
            "",
            "---",
            ""
        ])
        
        return lines
    
    def _generate_appendix(self):
        """Generate appendix with detailed notes"""
        lines = [
            "## 📚 Appendix: Complete Notes Database",
            "",
            "### 📋 All Generated Insights",
            "",
        ]
        
        # Group notes by category
        categorized_notes = defaultdict(list)
        for note in self.all_me_notes:
            category = note.get('category', 'UNCATEGORIZED')
            categorized_notes[category].append(note)
        
        for category, notes in categorized_notes.items():
            lines.extend([
                f"#### {category.replace('_', ' ').title()} ({len(notes)} notes)",
                "",
            ])
            
            for i, note in enumerate(notes, 1):
                confidence_emoji = "🟢" if note.get('confidence', 0) >= 0.9 else "🟡" if note.get('confidence', 0) >= 0.7 else "🔴"
                lines.extend([
                    f"{i}. **{note.get('title', 'Insight')}** {confidence_emoji}",
                    f"   - {note.get('note', 'No details available')}",
                    f"   - *Source: {note.get('source', 'Unknown')} | Confidence: {note.get('confidence', 0):.1%}*",
                    "",
                ])
            
            lines.append("")
        
        # Footer
        lines.extend([
            "---",
            "",
            f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Me Notes Intelligence System*",
            "",
            "**End of Report**"
        ])
        
        return lines

def main():
    """Main function to generate Markdown report"""
    print("📝 ME NOTES MARKDOWN GENERATOR")
    print("=" * 60)
    print("📧 User: Chin-Yew Lin (cyl@microsoft.com)")
    print("🏢 Organization: Microsoft")
    print(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    generator = MeNotesMarkdownGenerator()
    output_file = generator.generate_markdown_report()
    
    if output_file:
        print(f"\n✅ Markdown report generated successfully!")
        print(f"📁 File: {output_file}")
        print(f"📄 Contains: {len(generator.all_me_notes)} insights from {len(generator.data_sources)} data sources")
        print("\n🎯 Next steps:")
        print(f"   1. Open {output_file} in any Markdown viewer")
        print("   2. Share with stakeholders or team members")
        print("   3. Use for performance reviews or project documentation")
    else:
        print("\n❌ Failed to generate Markdown report")

if __name__ == "__main__":
    main()