#!/usr/bin/env python3
"""
Me Notes Analytics Dashboard
Advanced analytics and visualization for Me Notes data
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
from collections import Counter, defaultdict

# Add project paths
sys.path.append(str(Path(__file__).parent))

from enhanced_me_notes_viewer import EnhancedMeNotesAPI, EnhancedMeNotesViewer

def generate_analytics_dashboard(user_email: str):
    """Generate comprehensive analytics dashboard for Me Notes"""
    
    print(f"📊 Me Notes Analytics Dashboard for {user_email}")
    print("=" * 60)
    
    # Fetch enhanced Me Notes
    api = EnhancedMeNotesAPI(user_email)
    notes = api.fetch_me_notes(days_back=30)
    
    # Basic statistics
    print(f"\n📈 **Executive Summary**")
    print(f"   📧 User: {user_email}")
    print(f"   🏢 Context: {api.user_context['company']} ({api.user_context['domain']})")
    print(f"   📅 Period: Last 30 days")
    print(f"   📝 Total Insights: {len(notes)}")
    print(f"   🎯 Average Confidence: {sum(note.confidence for note in notes) / len(notes):.1%}")
    
    # Category analysis
    category_stats = Counter(note.category.value for note in notes)
    print(f"\n📋 **Category Distribution**")
    total_notes = len(notes)
    for category, count in category_stats.most_common():
        percentage = (count / total_notes) * 100
        bar = "█" * int(percentage / 5)  # Visual bar
        icon = {"WORK_RELATED": "💼", "EXPERTISE": "🎯", "BEHAVIORAL_PATTERN": "🧭", 
               "INTERESTS": "💡", "FOLLOW_UPS": "📋"}.get(category, "📝")
        print(f"   {icon} {category.replace('_', ' ').title()}: {count} ({percentage:.1f}%) {bar}")
    
    # Temporal analysis
    print(f"\n📅 **Temporal Analysis**")
    durability_stats = Counter(note.temporal_durability.value for note in notes)
    for durability, count in durability_stats.most_common():
        icon = {"TEMPORAL_SHORT_LIVED": "⏰", "TEMPORAL_MEDIUM_LIVED": "📅", "TEMPORAL_LONG_LIVED": "📆"}.get(durability, "⏳")
        clean_name = durability.replace('TEMPORAL_', '').replace('_', ' ').title()
        print(f"   {icon} {clean_name}: {count} insights")
    
    # Confidence analysis
    print(f"\n🎯 **Confidence Analysis**")
    high_conf = len([n for n in notes if n.confidence >= 0.9])
    med_conf = len([n for n in notes if 0.7 <= n.confidence < 0.9])
    low_conf = len([n for n in notes if n.confidence < 0.7])
    
    print(f"   🟢 High Confidence (90%+): {high_conf} insights")
    print(f"   🟡 Medium Confidence (70-89%): {med_conf} insights")
    print(f"   🔴 Low Confidence (<70%): {low_conf} insights")
    
    # Source analysis
    print(f"\n📡 **Source Analysis**")
    source_stats = Counter(note.source for note in notes)
    for source, count in source_stats.most_common():
        print(f"   📱 {source}: {count} insights")
    
    # Recent activity
    print(f"\n⚡ **Recent Activity (Last 7 Days)**")
    recent_cutoff = datetime.now() - timedelta(days=7)
    recent_notes = [n for n in notes if n.timestamp >= recent_cutoff]
    print(f"   📈 Recent Insights: {len(recent_notes)}")
    
    if recent_notes:
        recent_categories = Counter(note.category.value for note in recent_notes)
        print("   📊 Recent Activity by Category:")
        for category, count in recent_categories.most_common():
            icon = {"WORK_RELATED": "💼", "EXPERTISE": "🎯", "BEHAVIORAL_PATTERN": "🧭", 
                   "INTERESTS": "💡", "FOLLOW_UPS": "📋"}.get(category, "📝")
            print(f"      {icon} {category.replace('_', ' ').title()}: {count}")
    
    # Key insights extraction
    print(f"\n🔍 **Key Insights Extraction**")
    
    # Extract projects
    projects = set()
    collaborators = set()
    skills = set()
    
    for note in notes:
        note_text = note.note.lower()
        
        # Project extraction
        if "priority calendar" in note_text:
            projects.add("Priority Calendar")
        if "graph" in note_text and ("api" in note_text or "microsoft" in note_text):
            projects.add("Microsoft Graph")
        if "ai" in note_text or "llm" in note_text or "machine learning" in note_text:
            projects.add("AI/LLM Integration")
        if "office" in note_text and "365" in note_text:
            projects.add("Office 365")
        
        # Collaborator extraction (enhanced system specific)
        if "sarah chen" in note_text:
            collaborators.add("Sarah Chen")
        if "mike johnson" in note_text:
            collaborators.add("Mike Johnson")
        if "david park" in note_text:
            collaborators.add("David Park")
        if "lisa rodriguez" in note_text:
            collaborators.add("Lisa Rodriguez")
        
        # Skills extraction
        if note.category.value == "EXPERTISE":
            if "calendar" in note_text:
                skills.add("Calendar Intelligence")
            if "api" in note_text:
                skills.add("API Integration")
            if "ai" in note_text or "ml" in note_text:
                skills.add("AI/ML")
            if "graph" in note_text:
                skills.add("Graph API")
    
    print(f"   💼 Active Projects: {', '.join(sorted(projects)) if projects else 'None detected'}")
    print(f"   👥 Key Collaborators: {', '.join(sorted(collaborators)) if collaborators else 'None detected'}")
    print(f"   🎯 Core Skills: {', '.join(sorted(skills)) if skills else 'None detected'}")
    
    # Recommendations
    print(f"\n💡 **Recommendations**")
    recommendations = []
    
    if len(recent_notes) < 5:
        recommendations.append("🔄 Consider updating Me Notes data - low recent activity detected")
    
    if high_conf < total_notes * 0.7:
        recommendations.append("📊 Review data sources - confidence levels could be improved")
    
    follow_up_count = len([n for n in notes if n.category.value == "FOLLOW_UPS"])
    if follow_up_count > 5:
        recommendations.append(f"📋 {follow_up_count} follow-up items detected - consider prioritizing action items")
    
    if len(projects) >= 3:
        recommendations.append("⚡ Multiple active projects detected - consider using for meeting prioritization")
    
    if not recommendations:
        recommendations.append("✅ Me Notes profile looks healthy and comprehensive")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    return {
        "total_notes": len(notes),
        "categories": dict(category_stats),
        "confidence_avg": sum(note.confidence for note in notes) / len(notes),
        "recent_activity": len(recent_notes),
        "projects": list(projects),
        "collaborators": list(collaborators),
        "skills": list(skills)
    }

def generate_html_analytics_report(user_email: str, analytics_data: dict):
    """Generate beautiful HTML analytics report"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_safe = user_email.replace('@', '_').replace('.', '_')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Me Notes Analytics - {user_email}</title>
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
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            font-size: 1.2em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .category-chart {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .category-bar {{
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        
        .category-label {{
            width: 200px;
            font-weight: bold;
        }}
        
        .bar {{
            height: 20px;
            background: linear-gradient(135deg, #55a3ff 0%, #003d82 100%);
            border-radius: 10px;
            margin: 0 10px;
        }}
        
        .insights-section {{
            background: linear-gradient(135deg, #a8e6cf 0%, #56ab2f 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .insight-box {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
        }}
        
        .insight-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: white;
        }}
        
        .insight-list {{
            list-style: none;
            padding: 0;
        }}
        
        .insight-list li {{
            margin: 5px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .insight-list li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: rgba(255,255,255,0.7);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Me Notes Analytics</h1>
            <div class="subtitle">Comprehensive insights for {user_email}</div>
            <div class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">{analytics_data['total_notes']}</span>
                <span class="stat-label">Total Insights</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{len(analytics_data['categories'])}</span>
                <span class="stat-label">Categories</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{analytics_data['confidence_avg']:.0%}</span>
                <span class="stat-label">Avg Confidence</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{analytics_data['recent_activity']}</span>
                <span class="stat-label">Recent Activity</span>
            </div>
        </div>
        
        <div class="category-chart">
            <h2>📋 Category Distribution</h2>
"""
    
    # Add category bars
    total = analytics_data['total_notes']
    for category, count in analytics_data['categories'].items():
        percentage = (count / total) * 100
        bar_width = percentage * 3  # Scale for display
        clean_name = category.replace('_', ' ').title()
        
        html_content += f"""
            <div class="category-bar">
                <div class="category-label">{clean_name}</div>
                <div class="bar" style="width: {bar_width}px;"></div>
                <span>{count} ({percentage:.1f}%)</span>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="insights-section">
            <h2>🔍 Key Insights</h2>
            <div class="insights-grid">
                <div class="insight-box">
                    <div class="insight-title">💼 Active Projects</div>
                    <ul class="insight-list">
"""
    
    for project in analytics_data['projects'][:5]:  # Top 5
        html_content += f"<li>{project}</li>"
    
    html_content += f"""
                    </ul>
                </div>
                <div class="insight-box">
                    <div class="insight-title">👥 Key Collaborators</div>
                    <ul class="insight-list">
"""
    
    for collaborator in analytics_data['collaborators'][:5]:  # Top 5
        html_content += f"<li>{collaborator}</li>"
    
    html_content += f"""
                    </ul>
                </div>
                <div class="insight-box">
                    <div class="insight-title">🎯 Core Skills</div>
                    <ul class="insight-list">
"""
    
    for skill in analytics_data['skills'][:5]:  # Top 5
        html_content += f"<li>{skill}</li>"
    
    html_content += f"""
                    </ul>
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #7f8c8d;">
            📝 Generated by Me Notes Analytics Dashboard<br>
            🔄 Refresh by running the analytics tool again
        </div>
    </div>
</body>
</html>"""
    
    # Save the HTML report
    output_dir = Path("me_notes_reports")
    output_dir.mkdir(exist_ok=True)
    
    html_file = output_dir / f"me_notes_analytics_{user_safe}_{timestamp}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Analytics report saved: {html_file}")
    return str(html_file)

def main():
    """Generate analytics dashboard for a user"""
    
    user_email = "cyl@microsoft.com"  # Default to your account
    
    try:
        # Generate analytics
        analytics_data = generate_analytics_dashboard(user_email)
        
        # Generate HTML report
        html_file = generate_html_analytics_report(user_email, analytics_data)
        
        print(f"\n🎯 Analytics Dashboard Complete!")
        print(f"📊 View your analytics report: {html_file}")
        
        # Optionally open in browser
        import webbrowser
        try:
            webbrowser.open(f"file://{Path(html_file).absolute()}")
            print("🌐 Opening analytics dashboard in browser...")
        except:
            print("💡 You can manually open the HTML file in your browser")
        
    except Exception as e:
        print(f"❌ Error generating analytics: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()