#!/usr/bin/env python3
"""
Email + Meeting Collaboration Integration Demo

Demonstrates Phase 1 email integration:
1. Extract sent emails from Graph API
2. Analyze email collaboration patterns
3. Identify email-only collaborators
4. Validate meeting collaborators with email data
5. Generate comprehensive collaboration report

Usage:
    python email_meeting_integration_demo.py
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Set, Dict, List

# Import our new tools
try:
    from tools.email_collaboration_analyzer import EmailCollaborationAnalyzer
except ImportError:
    print("❌ Could not import EmailCollaborationAnalyzer")
    print("   Make sure tools/email_collaboration_analyzer.py exists")
    sys.exit(1)


def extract_emails_from_graph():
    """Step 1: Extract emails using SilverFlow script."""
    print("\n" + "=" * 70)
    print("STEP 1: Extract Sent Emails from Microsoft Graph API")
    print("=" * 70)
    
    script = Path("SilverFlow/data/graph_get_sent_emails.py")
    
    if not script.exists():
        print(f"❌ Email extraction script not found: {script}")
        return None
    
    print(f"📧 Running email extraction...")
    print(f"   Script: {script}")
    print(f"   This will fetch your last 180 days of sent emails\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--top", "200", "--days", "180"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            email_file = Path("SilverFlow/data/out/graph_sent_emails.json")
            if email_file.exists():
                print(f"✅ Email extraction successful!")
                return str(email_file)
            else:
                print(f"⚠️  Extraction completed but file not found: {email_file}")
                return None
        else:
            print(f"❌ Email extraction failed:")
            print(result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Email extraction timed out (> 5 minutes)")
        return None
    except Exception as e:
        print(f"❌ Error running email extraction: {e}")
        return None


def analyze_email_collaboration(email_file: str):
    """Step 2: Analyze email patterns."""
    print("\n" + "=" * 70)
    print("STEP 2: Analyze Email Collaboration Patterns")
    print("=" * 70)
    
    analyzer = EmailCollaborationAnalyzer(email_data_file=email_file)
    analysis = analyzer.analyze_email_patterns()
    
    if not analysis:
        print("❌ Email analysis failed")
        return None
    
    # Save analysis
    output_file = "data/email_collaboration_analysis.json"
    analyzer.save_analysis(analysis, output_file)
    
    return analysis


def load_meeting_collaborators():
    """Step 3: Load meeting-based collaborators."""
    print("\n" + "=" * 70)
    print("STEP 3: Load Meeting-Based Collaborators")
    print("=" * 70)
    
    # Try to find existing collaborator discovery results
    collab_file = Path("data/collaborator_discovery_results.json")
    
    if not collab_file.exists():
        print(f"⚠️  Meeting collaborator data not found: {collab_file}")
        print("   Run collaborator discovery first to get full comparison")
        print("   For now, using email-only analysis")
        return set()
    
    try:
        with open(collab_file, 'r', encoding='utf-8') as f:
            collab_data = json.load(f)
        
        # Extract email addresses from collaborators
        meeting_emails = set()
        collaborators = collab_data.get('collaborators', [])
        
        for collab in collaborators:
            # Try different email field names
            email = (collab.get('email') or 
                    collab.get('email_address') or
                    collab.get('person', {}).get('email', ''))
            
            if email:
                meeting_emails.add(email.lower())
        
        print(f"✅ Loaded {len(meeting_emails)} meeting-based collaborators")
        return meeting_emails
        
    except Exception as e:
        print(f"❌ Error loading meeting collaborators: {e}")
        return set()


def identify_email_only(email_analysis: Dict, meeting_emails: Set[str]):
    """Step 4: Identify email-only collaborators."""
    print("\n" + "=" * 70)
    print("STEP 4: Identify Email-Only Collaborators")
    print("=" * 70)
    
    analyzer = EmailCollaborationAnalyzer()
    email_only = analyzer.identify_email_only_collaborators(
        email_analysis, 
        meeting_emails
    )
    
    return email_only


def generate_comprehensive_report(email_analysis: Dict, 
                                 email_only: List[Dict],
                                 meeting_emails: Set[str]):
    """Step 5: Generate comprehensive report."""
    print("\n" + "=" * 70)
    print("STEP 5: Generate Comprehensive Collaboration Report")
    print("=" * 70)
    
    report = {
        'generated_at': email_analysis.get('analysis_date'),
        'total_email_collaborators': email_analysis.get('total_email_collaborators', 0),
        'total_meeting_collaborators': len(meeting_emails),
        'email_only_collaborators': len(email_only),
        'multi_channel_collaborators': email_analysis.get('total_email_collaborators', 0) - len(email_only),
        'email_only_list': email_only[:20],  # Top 20
        'summary': email_analysis.get('summary', {}),
        'insights': []
    }
    
    # Generate insights
    if email_only:
        report['insights'].append({
            'type': 'email_only',
            'count': len(email_only),
            'message': f"Found {len(email_only)} email-only collaborators (people you email but never meet)"
        })
    
    if report['multi_channel_collaborators'] > 0:
        report['insights'].append({
            'type': 'multi_channel',
            'count': report['multi_channel_collaborators'],
            'message': f"{report['multi_channel_collaborators']} collaborators use both email and meetings"
        })
    
    # Calculate coverage
    total_unique = report['total_email_collaborators'] + len(meeting_emails)
    if total_unique > 0:
        email_coverage = (report['total_email_collaborators'] / total_unique) * 100
        meeting_coverage = (len(meeting_emails) / total_unique) * 100
        
        report['insights'].append({
            'type': 'coverage',
            'email_coverage_pct': email_coverage,
            'meeting_coverage_pct': meeting_coverage,
            'message': f"Email captures {email_coverage:.1f}% of collaboration, meetings capture {meeting_coverage:.1f}%"
        })
    
    # Save report
    report_file = Path("data/email_meeting_collaboration_report.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Report saved to: {report_file}")
    
    # Print summary
    print("\n📊 COLLABORATION SUMMARY")
    print("=" * 70)
    print(f"Total Email Collaborators:     {report['total_email_collaborators']}")
    print(f"Total Meeting Collaborators:   {report['total_meeting_collaborators']}")
    print(f"Email-Only Collaborators:      {report['email_only_collaborators']}")
    print(f"Multi-Channel Collaborators:   {report['multi_channel_collaborators']}")
    print()
    
    for insight in report['insights']:
        print(f"💡 {insight['message']}")
    
    if email_only:
        print(f"\n📧 TOP 10 EMAIL-ONLY COLLABORATORS:")
        print(f"{'Rank':<5} {'Name':<30} {'Emails':<8} {'Score':<8} {'Last Contact'}")
        print("-" * 80)
        
        for i, collab in enumerate(email_only[:10], 1):
            name = collab.get('name', 'Unknown')[:29]
            emails = collab.get('total_emails', 0)
            score = collab.get('email_score', 0)
            days = collab.get('days_since_last_email', 0)
            
            print(f"{i:<5} {name:<30} {emails:<8} {score:<8.1f} {days}d ago")
    
    return report


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("EMAIL + MEETING COLLABORATION INTEGRATION")
    print("Phase 1: Email-Only Collaborator Discovery")
    print("=" * 70)
    
    # Step 1: Extract emails
    email_file = extract_emails_from_graph()
    
    if not email_file:
        # Try to find existing email data
        email_file = "SilverFlow/data/out/graph_sent_emails.json"
        if not Path(email_file).exists():
            print("\n❌ No email data available. Cannot proceed.")
            print("\nTo extract emails:")
            print("   python SilverFlow/data/graph_get_sent_emails.py --top 200 --days 180")
            return 1
        else:
            print(f"\n⚠️  Using existing email data: {email_file}")
    
    # Step 2: Analyze email patterns
    email_analysis = analyze_email_collaboration(email_file)
    
    if not email_analysis:
        return 1
    
    # Step 3: Load meeting collaborators
    meeting_emails = load_meeting_collaborators()
    
    # Step 4: Identify email-only collaborators
    email_only = identify_email_only(email_analysis, meeting_emails)
    
    # Step 5: Generate comprehensive report
    report = generate_comprehensive_report(email_analysis, email_only, meeting_emails)
    
    print("\n" + "=" * 70)
    print("✅ EMAIL INTEGRATION COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("   - data/email_collaboration_analysis.json")
    print("   - data/email_meeting_collaboration_report.json")
    print("\nNext steps:")
    print("   1. Review email-only collaborators list")
    print("   2. Update collaborator_discovery.py to include email scores")
    print("   3. Re-run full collaborator discovery with email integration")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
