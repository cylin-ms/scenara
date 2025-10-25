#!/usr/bin/env python3
"""
Scenara Daily Interaction Logger
Tracks and summarizes daily AI interactions, progress, and achievements
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib


class ScenaraInteractionLogger:
    """
    Daily interaction logging system for Scenara project
    Tracks sessions, accomplishments, decisions, and lessons learned
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.logs_dir = self.project_root / "daily_logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Session tracking
        self.session_start = datetime.now(timezone.utc)
        self.current_date = self.session_start.strftime('%Y%m%d')
        self.log_file = self.logs_dir / f"daily_log_{self.current_date}.json"
        
        # Load or create today's log
        self.daily_log = self.load_daily_log()
    
    def load_daily_log(self) -> Dict:
        """Load existing daily log or create new one"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading daily log: {e}")
                return self.create_new_daily_log()
        else:
            return self.create_new_daily_log()
    
    def create_new_daily_log(self) -> Dict:
        """Create a new daily log structure"""
        return {
            'date': self.current_date,
            'date_readable': self.session_start.strftime('%B %d, %Y'),
            'created_at': self.session_start.isoformat(),
            'sessions': [],
            'daily_summary': {
                'total_sessions': 0,
                'total_duration_minutes': 0,
                'major_accomplishments': [],
                'tools_created': [],
                'tools_modified': [],
                'files_created': [],
                'files_modified': [],
                'lessons_learned': [],
                'decisions_made': [],
                'next_day_priorities': []
            },
            'metrics': {
                'lines_of_code_added': 0,
                'documentation_pages_created': 0,
                'tools_integrated': 0,
                'api_calls_made': 0,
                'tests_passed': 0,
                'errors_resolved': 0
            }
        }
    
    def start_session(self, session_description: str = "Scenara development session") -> str:
        """Start a new interaction session"""
        session_id = hashlib.md5(f"{self.session_start.isoformat()}_{session_description}".encode()).hexdigest()[:8]
        
        session = {
            'session_id': session_id,
            'start_time': self.session_start.isoformat(),
            'description': session_description,
            'interactions': [],
            'accomplishments': [],
            'tools_used': [],
            'files_touched': [],
            'decisions': [],
            'challenges': [],
            'end_time': None,
            'duration_minutes': None
        }
        
        self.daily_log['sessions'].append(session)
        self.save_daily_log()
        
        print(f"📅 Started session {session_id}: {session_description}")
        return session_id
    
    def log_interaction(self, 
                       interaction_type: str,
                       description: str,
                       details: Dict = None,
                       session_id: str = None) -> str:
        """
        Log a specific interaction within a session
        
        Args:
            interaction_type: Type of interaction (user_request, tool_creation, analysis, etc.)
            description: Brief description of the interaction
            details: Additional details and context
            session_id: Session ID (uses latest if not provided)
        """
        if not self.daily_log['sessions']:
            session_id = self.start_session("Auto-started session")
        
        # Use latest session if no session_id provided
        if session_id is None:
            current_session = self.daily_log['sessions'][-1]
        else:
            current_session = next((s for s in self.daily_log['sessions'] if s['session_id'] == session_id), None)
            if not current_session:
                raise ValueError(f"Session {session_id} not found")
        
        interaction = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': interaction_type,
            'description': description,
            'details': details or {}
        }
        
        current_session['interactions'].append(interaction)
        self.save_daily_log()
        
        return f"interaction_{len(current_session['interactions'])}"
    
    def log_accomplishment(self, 
                          accomplishment: str,
                          category: str = "development",
                          impact: str = "medium",
                          session_id: str = None):
        """
        Log a major accomplishment
        
        Args:
            accomplishment: Description of what was accomplished
            category: Category (development, analysis, documentation, integration)
            impact: Impact level (low, medium, high, critical)
            session_id: Session ID (uses latest if not provided)
        """
        if not self.daily_log['sessions']:
            session_id = self.start_session("Auto-started session")
        
        # Use latest session if no session_id provided
        if session_id is None:
            current_session = self.daily_log['sessions'][-1]
        else:
            current_session = next((s for s in self.daily_log['sessions'] if s['session_id'] == session_id), None)
            if not current_session:
                raise ValueError(f"Session {session_id} not found")
        
        accomplishment_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'description': accomplishment,
            'category': category,
            'impact': impact
        }
        
        current_session['accomplishments'].append(accomplishment_entry)
        self.daily_log['daily_summary']['major_accomplishments'].append(accomplishment_entry)
        self.save_daily_log()
        
        print(f"🎯 Logged accomplishment: {accomplishment}")
    
    def log_tool_activity(self, 
                         tool_name: str,
                         activity_type: str,  # created, modified, tested, documented
                         description: str = "",
                         file_path: str = "",
                         session_id: str = None):
        """Log tool-related activity"""
        if activity_type == "created":
            self.daily_log['daily_summary']['tools_created'].append({
                'name': tool_name,
                'file_path': file_path,
                'description': description,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        elif activity_type == "modified":
            self.daily_log['daily_summary']['tools_modified'].append({
                'name': tool_name,
                'file_path': file_path,
                'description': description,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        
        self.log_interaction(
            "tool_activity",
            f"{activity_type.title()} tool: {tool_name}",
            {
                'tool_name': tool_name,
                'activity_type': activity_type,
                'file_path': file_path,
                'description': description
            },
            session_id
        )
    
    def log_file_activity(self,
                         file_path: str,
                         activity_type: str,  # created, modified, deleted
                         description: str = "",
                         session_id: str = None):
        """Log file-related activity"""
        file_entry = {
            'path': file_path,
            'description': description,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        if activity_type == "created":
            self.daily_log['daily_summary']['files_created'].append(file_entry)
        elif activity_type == "modified":
            self.daily_log['daily_summary']['files_modified'].append(file_entry)
        
        self.log_interaction(
            "file_activity",
            f"{activity_type.title()} file: {Path(file_path).name}",
            {
                'file_path': file_path,
                'activity_type': activity_type,
                'description': description
            },
            session_id
        )
    
    def log_decision(self,
                    decision: str,
                    reasoning: str = "",
                    alternatives: List[str] = None,
                    impact: str = "medium",
                    session_id: str = None):
        """Log an important decision made during development"""
        decision_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'decision': decision,
            'reasoning': reasoning,
            'alternatives': alternatives or [],
            'impact': impact
        }
        
        self.daily_log['daily_summary']['decisions_made'].append(decision_entry)
        
        self.log_interaction(
            "decision",
            f"Decision: {decision}",
            decision_entry,
            session_id
        )
        
        print(f"🤔 Logged decision: {decision}")
    
    def end_session(self, session_id: str = None, summary: str = ""):
        """End a session and calculate duration"""
        if session_id is None and self.daily_log['sessions']:
            current_session = self.daily_log['sessions'][-1]
        else:
            current_session = next((s for s in self.daily_log['sessions'] if s['session_id'] == session_id), None)
            if not current_session:
                raise ValueError(f"Session {session_id} not found")
        
        end_time = datetime.now(timezone.utc)
        start_time = datetime.fromisoformat(current_session['start_time'])
        duration = (end_time - start_time).total_seconds() / 60
        
        current_session['end_time'] = end_time.isoformat()
        current_session['duration_minutes'] = round(duration, 1)
        
        if summary:
            current_session['summary'] = summary
        
        # Update daily summary
        self.daily_log['daily_summary']['total_sessions'] = len(self.daily_log['sessions'])
        self.daily_log['daily_summary']['total_duration_minutes'] = sum(
            s.get('duration_minutes', 0) for s in self.daily_log['sessions'] if s.get('duration_minutes')
        )
        
        self.save_daily_log()
        
        print(f"⏱️ Ended session {current_session['session_id']}: {duration:.1f} minutes")
        return current_session['session_id']
    
    def update_metrics(self, metric_name: str, value: int):
        """Update daily metrics"""
        if metric_name in self.daily_log['metrics']:
            self.daily_log['metrics'][metric_name] += value
        else:
            self.daily_log['metrics'][metric_name] = value
        
        self.save_daily_log()
    
    def set_next_day_priorities(self, priorities: List[str]):
        """Set priorities for the next day"""
        self.daily_log['daily_summary']['next_day_priorities'] = [
            {
                'priority': priority,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            for priority in priorities
        ]
        self.save_daily_log()
        print(f"📋 Set {len(priorities)} priorities for tomorrow")
    
    def save_daily_log(self):
        """Save the daily log to file"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.daily_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving daily log: {e}")
    
    def generate_daily_summary_markdown(self) -> str:
        """Generate a beautiful markdown summary of the day"""
        log = self.daily_log
        date_readable = log['date_readable']
        
        markdown = f"""# 📅 Scenara Daily Progress Report - {date_readable}

*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📊 Daily Overview

| Metric | Value |
|--------|-------|
| **Total Sessions** | {log['daily_summary']['total_sessions']} |
| **Total Time** | {log['daily_summary']['total_duration_minutes']:.1f} minutes |
| **Major Accomplishments** | {len(log['daily_summary']['major_accomplishments'])} |
| **Tools Created/Modified** | {len(log['daily_summary']['tools_created']) + len(log['daily_summary']['tools_modified'])} |
| **Files Touched** | {len(log['daily_summary']['files_created']) + len(log['daily_summary']['files_modified'])} |
| **Decisions Made** | {len(log['daily_summary']['decisions_made'])} |

---

## 🎯 Major Accomplishments

"""
        
        if log['daily_summary']['major_accomplishments']:
            for i, acc in enumerate(log['daily_summary']['major_accomplishments'], 1):
                impact_emoji = {'low': '🔵', 'medium': '🟡', 'high': '🟠', 'critical': '🔴'}.get(acc.get('impact', 'medium'), '🟡')
                markdown += f"{i}. **{acc['description']}** {impact_emoji}\n"
                markdown += f"   - *Category*: {acc.get('category', 'development').title()}\n"
                markdown += f"   - *Impact*: {acc.get('impact', 'medium').title()}\n\n"
        else:
            markdown += "*No major accomplishments recorded today.*\n\n"
        
        markdown += "---\n\n## 🛠️ Tools & Development\n\n"
        
        # Tools created
        if log['daily_summary']['tools_created']:
            markdown += "### ✨ New Tools Created\n\n"
            for tool in log['daily_summary']['tools_created']:
                markdown += f"- **{tool['name']}**\n"
                markdown += f"  - *File*: `{tool['file_path']}`\n"
                if tool['description']:
                    markdown += f"  - *Description*: {tool['description']}\n"
                markdown += "\n"
        
        # Tools modified
        if log['daily_summary']['tools_modified']:
            markdown += "### 🔧 Tools Modified\n\n"
            for tool in log['daily_summary']['tools_modified']:
                markdown += f"- **{tool['name']}**\n"
                markdown += f"  - *File*: `{tool['file_path']}`\n"
                if tool['description']:
                    markdown += f"  - *Description*: {tool['description']}\n"
                markdown += "\n"
        
        # Files created
        if log['daily_summary']['files_created']:
            markdown += "### 📄 New Files Created\n\n"
            for file_info in log['daily_summary']['files_created'][:10]:  # Limit to 10 for readability
                markdown += f"- `{file_info['path']}`"
                if file_info['description']:
                    markdown += f" - {file_info['description']}"
                markdown += "\n"
            if len(log['daily_summary']['files_created']) > 10:
                markdown += f"*... and {len(log['daily_summary']['files_created']) - 10} more files*\n"
            markdown += "\n"
        
        markdown += "---\n\n## 🤔 Decisions & Lessons\n\n"
        
        # Decisions made
        if log['daily_summary']['decisions_made']:
            markdown += "### 📋 Key Decisions\n\n"
            for decision in log['daily_summary']['decisions_made']:
                impact_emoji = {'low': '🔵', 'medium': '🟡', 'high': '🟠', 'critical': '🔴'}.get(decision.get('impact', 'medium'), '🟡')
                markdown += f"- **{decision['decision']}** {impact_emoji}\n"
                if decision['reasoning']:
                    markdown += f"  - *Reasoning*: {decision['reasoning']}\n"
                if decision['alternatives']:
                    markdown += f"  - *Alternatives considered*: {', '.join(decision['alternatives'])}\n"
                markdown += "\n"
        
        # Lessons learned
        if log['daily_summary']['lessons_learned']:
            markdown += "### 📚 Lessons Learned\n\n"
            for lesson in log['daily_summary']['lessons_learned']:
                markdown += f"- {lesson}\n"
            markdown += "\n"
        
        markdown += "---\n\n## 📈 Development Metrics\n\n"
        
        metrics = log['metrics']
        markdown += f"- **Lines of Code Added**: {metrics.get('lines_of_code_added', 0)}\n"
        markdown += f"- **Documentation Pages Created**: {metrics.get('documentation_pages_created', 0)}\n"
        markdown += f"- **Tools Integrated**: {metrics.get('tools_integrated', 0)}\n"
        markdown += f"- **API Calls Made**: {metrics.get('api_calls_made', 0)}\n"
        markdown += f"- **Tests Passed**: {metrics.get('tests_passed', 0)}\n"
        markdown += f"- **Errors Resolved**: {metrics.get('errors_resolved', 0)}\n\n"
        
        markdown += "---\n\n## 📋 Tomorrow's Priorities\n\n"
        
        if log['daily_summary']['next_day_priorities']:
            for i, priority in enumerate(log['daily_summary']['next_day_priorities'], 1):
                markdown += f"{i}. {priority['priority']}\n"
        else:
            markdown += "*No priorities set for tomorrow yet.*\n"
        
        markdown += "\n---\n\n## 📝 Session Details\n\n"
        
        for session in log['sessions']:
            duration = session.get('duration_minutes', 0)
            status = "✅ Completed" if session.get('end_time') else "🔄 In Progress"
            
            markdown += f"### Session {session['session_id']} {status}\n\n"
            markdown += f"- **Description**: {session['description']}\n"
            markdown += f"- **Duration**: {duration:.1f} minutes\n"
            markdown += f"- **Interactions**: {len(session['interactions'])}\n"
            markdown += f"- **Accomplishments**: {len(session['accomplishments'])}\n"
            
            if session.get('summary'):
                markdown += f"- **Summary**: {session['summary']}\n"
            
            markdown += "\n"
        
        markdown += "---\n\n*Daily Progress Report generated by Scenara Interaction Logger* 🚀\n"
        
        return markdown
    
    def get_recent_days_summary(self, days: int = 7) -> List[Dict]:
        """Get summary of recent days"""
        recent_logs = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y%m%d')
            log_file = self.logs_dir / f"daily_log_{date_str}.json"
            
            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        daily_data = json.load(f)
                        recent_logs.append(daily_data)
                except Exception:
                    continue
        
        return recent_logs


def main():
    """Command line interface for the interaction logger"""
    parser = argparse.ArgumentParser(description="Scenara Daily Interaction Logger")
    parser.add_argument('action', choices=['start', 'log', 'accomplish', 'decide', 'end', 'summary', 'priorities'],
                       help='Action to perform')
    parser.add_argument('--session-id', help='Session ID for session-specific actions')
    parser.add_argument('--description', required=False, help='Description of the action')
    parser.add_argument('--type', help='Type of interaction/accomplishment')
    parser.add_argument('--category', default='development', help='Category for accomplishments')
    parser.add_argument('--impact', default='medium', choices=['low', 'medium', 'high', 'critical'],
                       help='Impact level')
    parser.add_argument('--reasoning', help='Reasoning for decisions')
    parser.add_argument('--file', help='File path for file activities')
    parser.add_argument('--output', help='Output file for summary')
    parser.add_argument('--priorities', nargs='+', help='List of priorities for tomorrow')
    
    args = parser.parse_args()
    
    logger = ScenaraInteractionLogger()
    
    try:
        if args.action == 'start':
            description = args.description or "Scenara development session"
            session_id = logger.start_session(description)
            print(f"Started session: {session_id}")
        
        elif args.action == 'log':
            if not args.description:
                print("❌ --description required for log action")
                sys.exit(1)
            interaction_id = logger.log_interaction(
                args.type or 'general',
                args.description,
                session_id=args.session_id
            )
            print(f"Logged interaction: {interaction_id}")
        
        elif args.action == 'accomplish':
            if not args.description:
                print("❌ --description required for accomplish action")
                sys.exit(1)
            logger.log_accomplishment(
                args.description,
                args.category,
                args.impact,
                args.session_id
            )
        
        elif args.action == 'decide':
            if not args.description:
                print("❌ --description required for decide action")
                sys.exit(1)
            logger.log_decision(
                args.description,
                args.reasoning or "",
                impact=args.impact,
                session_id=args.session_id
            )
        
        elif args.action == 'end':
            session_id = logger.end_session(args.session_id, args.description or "")
            print(f"Ended session: {session_id}")
        
        elif args.action == 'summary':
            summary_md = logger.generate_daily_summary_markdown()
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(summary_md)
                print(f"📄 Summary saved to: {args.output}")
            else:
                # Save to default location
                output_file = logger.logs_dir / f"daily_summary_{logger.current_date}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(summary_md)
                print(f"📄 Summary saved to: {output_file}")
                
                # Also display key metrics
                print("\n📊 Today's Quick Stats:")
                print(f"   Sessions: {logger.daily_log['daily_summary']['total_sessions']}")
                print(f"   Duration: {logger.daily_log['daily_summary']['total_duration_minutes']:.1f} min")
                print(f"   Accomplishments: {len(logger.daily_log['daily_summary']['major_accomplishments'])}")
                print(f"   Tools: {len(logger.daily_log['daily_summary']['tools_created']) + len(logger.daily_log['daily_summary']['tools_modified'])}")
        
        elif args.action == 'priorities':
            if not args.priorities:
                print("❌ --priorities required for priorities action")
                sys.exit(1)
            logger.set_next_day_priorities(args.priorities)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()