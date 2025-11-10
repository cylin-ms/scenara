#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Collaboration Analyzer
Scenara 2.0 - Enterprise Meeting Intelligence

Analyzes email communication patterns to identify:
1. Email-only collaborators (people you email but never meet)
2. Email frequency and recency for existing collaborators
3. Temporal email patterns (hot/recent/current/decay)
4. Email-meeting correlation validation

Uses Microsoft Graph API Mail.Read permission via SilverFlow integration.
"""

import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import subprocess

class EmailCollaborationAnalyzer:
    """
    Analyzes email communication patterns for collaboration intelligence.
    """
    
    def __init__(self, email_data_file: str = None):
        self.email_data_file = email_data_file
        self.current_date = datetime.now()
        
        # Temporal windows (same as meeting analysis)
        self.time_windows = {
            'hot': 7,      # Last 7 days: 2.0x multiplier
            'recent': 30,   # Last 30 days: 1.5x multiplier
            'current': 90,  # Last 90 days: 1.2x multiplier
            'medium': 180,  # Last 180 days: 0.8x multiplier
            # > 180 days: 0.5x multiplier (decay)
        }
        
        # Temporal multipliers (aligned with meeting scoring)
        self.temporal_multipliers = {
            'hot': 2.0,
            'recent': 1.5,
            'current': 1.2,
            'medium': 0.8,
            'decay': 0.5
        }
        
        # Points per email by recency
        self.email_points = {
            'hot': 5,      # Last 7 days
            'recent': 3,   # Last 30 days
            'current': 2,  # Last 90 days
            'medium': 1,   # Last 180 days
            'decay': 0.5   # > 180 days
        }
    
    def extract_emails_from_graph_api(self, days_back: int = 180, max_emails: int = 500) -> bool:
        """
        Extract sent emails using SilverFlow Graph API tool.
        
        Args:
            days_back: How many days of email history to fetch
            max_emails: Maximum number of emails to retrieve
            
        Returns:
            bool: True if extraction successful
        """
        print(f"📧 Extracting sent emails from last {days_back} days...")
        
        silverflow_script = Path("SilverFlow/data/graph_list_my_sent_messages.py")
        
        if not silverflow_script.exists():
            print(f"❌ SilverFlow email script not found: {silverflow_script}")
            print("   Please ensure SilverFlow is properly integrated.")
            return False
        
        try:
            # Run SilverFlow email extraction
            # Note: graph_list_my_sent_messages.py is for Teams messages
            # We need to create a similar script for Outlook emails
            # For now, check if email data file exists
            
            output_file = Path("SilverFlow/data/out/graph_my_sent_messages.json")
            
            if output_file.exists():
                print(f"✅ Found existing email data: {output_file}")
                self.email_data_file = str(output_file)
                return True
            else:
                print(f"⚠️  Email data not found: {output_file}")
                print(f"   Run: cd SilverFlow/data && python graph_list_my_sent_messages.py --top {max_emails}")
                return False
                
        except Exception as e:
            print(f"❌ Error extracting emails: {e}")
            return False
    
    def analyze_email_patterns(self, email_data_file: str = None) -> Dict:
        """
        Analyze email communication patterns from Graph API data.
        
        Args:
            email_data_file: Path to email data JSON file
            
        Returns:
            Dict with email collaboration analysis
        """
        if email_data_file:
            self.email_data_file = email_data_file
        
        if not self.email_data_file or not Path(self.email_data_file).exists():
            print(f"❌ Email data file not found: {self.email_data_file}")
            return {}
        
        print(f"📊 Analyzing email patterns from: {self.email_data_file}")
        
        try:
            with open(self.email_data_file, 'r', encoding='utf-8') as f:
                email_data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading email data: {e}")
            return {}
        
        # Initialize collaborator tracking
        email_collaborators = defaultdict(lambda: {
            'name': '',
            'email': '',
            'total_emails': 0,
            'emails_by_window': {
                'hot': 0,      # Last 7 days
                'recent': 0,   # Last 30 days
                'current': 0,  # Last 90 days
                'medium': 0,   # Last 180 days
                'decay': 0     # > 180 days
            },
            'last_email_date': None,
            'days_since_last_email': None,
            'email_score': 0,
            'threads': set(),
            'is_email_only': True,  # Will be updated by collaborator_discovery
            'recency_multiplier': 1.0
        })
        
        # Parse email data
        emails = email_data if isinstance(email_data, list) else email_data.get('value', [])
        
        print(f"📧 Processing {len(emails)} emails...")
        
        for email in emails:
            # Extract recipients (To, CC)
            recipients = self._extract_recipients(email)
            
            # Get email date
            sent_date = self._parse_email_date(email)
            if not sent_date:
                continue
            
            # Get conversation thread ID
            thread_id = email.get('conversationId', email.get('id', ''))
            
            # Process each recipient
            for recipient_email, recipient_name in recipients:
                if not recipient_email:
                    continue
                
                key = recipient_email.lower()
                
                # Update name if not set
                if not email_collaborators[key]['name'] and recipient_name:
                    email_collaborators[key]['name'] = recipient_name
                    email_collaborators[key]['email'] = recipient_email
                
                # Count email
                email_collaborators[key]['total_emails'] += 1
                
                # Add thread
                email_collaborators[key]['threads'].add(thread_id)
                
                # Categorize by temporal window
                days_ago = (self.current_date - sent_date).days
                
                if days_ago <= self.time_windows['hot']:
                    email_collaborators[key]['emails_by_window']['hot'] += 1
                elif days_ago <= self.time_windows['recent']:
                    email_collaborators[key]['emails_by_window']['recent'] += 1
                elif days_ago <= self.time_windows['current']:
                    email_collaborators[key]['emails_by_window']['current'] += 1
                elif days_ago <= self.time_windows['medium']:
                    email_collaborators[key]['emails_by_window']['medium'] += 1
                else:
                    email_collaborators[key]['emails_by_window']['decay'] += 1
                
                # Track last email date
                if (email_collaborators[key]['last_email_date'] is None or 
                    sent_date > email_collaborators[key]['last_email_date']):
                    email_collaborators[key]['last_email_date'] = sent_date
        
        # Calculate scores and recency
        for email, data in email_collaborators.items():
            # Calculate days since last email
            if data['last_email_date']:
                data['days_since_last_email'] = (self.current_date - data['last_email_date']).days
            
            # Calculate email score with temporal weighting
            score = 0
            for window, count in data['emails_by_window'].items():
                points = self.email_points.get(window, 0)
                score += count * points
            
            data['email_score'] = score
            
            # Calculate recency multiplier (based on most recent email)
            days_since = data['days_since_last_email']
            if days_since is not None:
                if days_since <= self.time_windows['hot']:
                    data['recency_multiplier'] = self.temporal_multipliers['hot']
                elif days_since <= self.time_windows['recent']:
                    data['recency_multiplier'] = self.temporal_multipliers['recent']
                elif days_since <= self.time_windows['current']:
                    data['recency_multiplier'] = self.temporal_multipliers['current']
                elif days_since <= self.time_windows['medium']:
                    data['recency_multiplier'] = self.temporal_multipliers['medium']
                else:
                    data['recency_multiplier'] = self.temporal_multipliers['decay']
            
            # Convert thread set to count
            data['unique_threads'] = len(data['threads'])
            data['threads'] = list(data['threads'])[:5]  # Keep first 5 for reference
        
        # Convert defaultdict to regular dict for JSON serialization
        email_collaborators_dict = {
            email: dict(data) for email, data in email_collaborators.items()
        }
        
        # Sort by email score
        sorted_collaborators = sorted(
            email_collaborators_dict.items(),
            key=lambda x: x[1]['email_score'],
            reverse=True
        )
        
        result = {
            'analysis_date': self.current_date.isoformat(),
            'total_emails_analyzed': len(emails),
            'total_email_collaborators': len(email_collaborators_dict),
            'collaborators': dict(sorted_collaborators),
            'summary': {
                'hot_period_emails': sum(d['emails_by_window']['hot'] for d in email_collaborators_dict.values()),
                'recent_period_emails': sum(d['emails_by_window']['recent'] for d in email_collaborators_dict.values()),
                'current_period_emails': sum(d['emails_by_window']['current'] for d in email_collaborators_dict.values()),
            }
        }
        
        print(f"\n✅ Email Analysis Complete!")
        print(f"   Total email collaborators: {len(email_collaborators_dict)}")
        print(f"   Hot period (7d): {result['summary']['hot_period_emails']} emails")
        print(f"   Recent period (30d): {result['summary']['recent_period_emails']} emails")
        print(f"   Current period (90d): {result['summary']['current_period_emails']} emails")
        
        return result
    
    def identify_email_only_collaborators(self, email_analysis: Dict, 
                                         meeting_collaborators: Set[str]) -> List[Dict]:
        """
        Identify collaborators who only communicate via email (no meetings).
        
        Args:
            email_analysis: Email analysis result
            meeting_collaborators: Set of emails from meeting collaborators
            
        Returns:
            List of email-only collaborators with scores
        """
        email_only = []
        
        for email, data in email_analysis.get('collaborators', {}).items():
            # Check if this person is not in meeting collaborators
            if email.lower() not in meeting_collaborators:
                email_only.append({
                    'email': email,
                    'name': data.get('name', 'Unknown'),
                    'total_emails': data.get('total_emails', 0),
                    'email_score': data.get('email_score', 0),
                    'days_since_last_email': data.get('days_since_last_email'),
                    'unique_threads': data.get('unique_threads', 0),
                    'recency_multiplier': data.get('recency_multiplier', 1.0),
                    'collaboration_type': 'email_only'
                })
        
        # Sort by email score
        email_only.sort(key=lambda x: x['email_score'], reverse=True)
        
        print(f"\n📧 Email-Only Collaborators: {len(email_only)}")
        if email_only:
            print(f"   Top 5:")
            for i, collab in enumerate(email_only[:5], 1):
                print(f"   {i}. {collab['name']} ({collab['email']})")
                print(f"      Emails: {collab['total_emails']}, Score: {collab['email_score']:.1f}, "
                      f"Threads: {collab['unique_threads']}")
        
        return email_only
    
    def _extract_recipients(self, email: Dict) -> List[Tuple[str, str]]:
        """Extract recipient email addresses and names from email."""
        recipients = []
        
        # Process To recipients
        for recipient in email.get('toRecipients', []):
            email_addr = recipient.get('emailAddress', {})
            addr = email_addr.get('address', '')
            name = email_addr.get('name', '')
            if addr:
                recipients.append((addr, name))
        
        # Process CC recipients
        for recipient in email.get('ccRecipients', []):
            email_addr = recipient.get('emailAddress', {})
            addr = email_addr.get('address', '')
            name = email_addr.get('name', '')
            if addr:
                recipients.append((addr, name))
        
        return recipients
    
    def _parse_email_date(self, email: Dict) -> Optional[datetime]:
        """Parse email sent date."""
        sent_datetime = email.get('sentDateTime')
        if not sent_datetime:
            return None
        
        try:
            # Handle ISO format with Z or +00:00
            if sent_datetime.endswith('Z'):
                return datetime.fromisoformat(sent_datetime[:-1])
            return datetime.fromisoformat(sent_datetime.replace('+00:00', ''))
        except Exception:
            return None
    
    def save_analysis(self, analysis: Dict, output_file: str = "data/email_collaboration_analysis.json"):
        """Save email analysis to file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Analysis saved to: {output_path}")
        return str(output_path)


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze email collaboration patterns")
    parser.add_argument('--email-data', type=str, help="Path to email data JSON file")
    parser.add_argument('--extract', action='store_true', help="Extract emails from Graph API first")
    parser.add_argument('--days', type=int, default=180, help="Days of email history (default: 180)")
    parser.add_argument('--output', type=str, default="data/email_collaboration_analysis.json",
                       help="Output file path")
    
    args = parser.parse_args()
    
    analyzer = EmailCollaborationAnalyzer(email_data_file=args.email_data)
    
    # Extract emails if requested
    if args.extract:
        if not analyzer.extract_emails_from_graph_api(days_back=args.days):
            print("\n⚠️  Email extraction failed. Using existing data if available.")
    
    # Analyze email patterns
    if analyzer.email_data_file or args.email_data:
        analysis = analyzer.analyze_email_patterns(args.email_data)
        
        if analysis:
            # Save analysis
            analyzer.save_analysis(analysis, args.output)
            
            # Show top 10 email collaborators
            print(f"\n📊 Top 10 Email Collaborators:")
            print(f"{'Rank':<5} {'Name':<25} {'Email':<35} {'Total':<6} {'Score':<8} {'Recency'}")
            print("-" * 100)
            
            for i, (email, data) in enumerate(list(analysis['collaborators'].items())[:10], 1):
                name = data.get('name', 'Unknown')[:24]
                email_addr = email[:34]
                total = data.get('total_emails', 0)
                score = data.get('email_score', 0)
                days = data.get('days_since_last_email', 0)
                
                print(f"{i:<5} {name:<25} {email_addr:<35} {total:<6} {score:<8.1f} {days}d ago")
    else:
        print("\n❌ No email data file specified.")
        print("   Options:")
        print("   1. Extract from Graph API: python tools/email_collaboration_analyzer.py --extract")
        print("   2. Provide existing file: python tools/email_collaboration_analyzer.py --email-data path/to/emails.json")


if __name__ == "__main__":
    main()
