# 🤖 Meeting Ranking Tool with Ollama LLM Integration

import json
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MeetingRankingResult:
    """Result of meeting ranking analysis"""
    meeting_id: str
    subject: str
    rank: int
    priority_score: float
    criticality_score: int  # 1-10
    engagement_level: str   # Drive/Participate/Attend/Monitor/Skip
    preparation_level: str  # Intensive/Standard/Minimal/None
    timing_optimization: str
    reasoning: str
    signals_detected: List[str]
    recommendations: Dict[str, Any]
    confidence: str  # High/Medium/Low

@dataclass
class UserProfile:
    """User profile for personalized ranking"""
    email: str
    manager_email: Optional[str] = None
    direct_reports: List[str] = None
    important_contacts: List[str] = None
    important_organizers: List[str] = None
    work_hours_start: str = "09:00"
    work_hours_end: str = "17:00"
    timezone: str = "UTC"
    preferred_prep_time: int = 30  # minutes
    meeting_fatigue_threshold: int = 6  # consecutive meetings

    def __post_init__(self):
        if self.direct_reports is None:
            self.direct_reports = []
        if self.important_contacts is None:
            self.important_contacts = []
        if self.important_organizers is None:
            self.important_organizers = []

class OllamaMeetingRanker:
    """
    Meeting Ranking Tool using Ollama LLM for intelligent prioritization
    
    Implements the Priority Calendar framework with multi-dimensional analysis:
    - Criticality Score (1-10): Automation decisions
    - Engagement Level (5 categories): User behavior guidance  
    - Preparation Level (4 categories): Time planning
    - Timing Optimization: Energy and schedule alignment
    """
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 model_name: str = "llama3.1",
                 user_profile: Optional[UserProfile] = None):
        """
        Initialize the Meeting Ranking Tool
        
        Args:
            ollama_url: Ollama server URL
            model_name: LLM model to use for ranking
            user_profile: User profile for personalized ranking
        """
        self.ollama_url = ollama_url
        self.model_name = model_name
        self.user_profile = user_profile or UserProfile(email="user@company.com")
        
        # Priority Calendar signal weights (from analysis)
        self.signal_weights = {
            # High Priority Signals (Weight: 3.0)
            "user_organizer": 3.0,
            "manager_chain": 3.0,
            "one_on_one": 3.0,
            "urgent_last_minute": 3.0,
            "personal_appointment": 3.0,
            
            # Medium Priority Signals (Weight: 2.0)
            "required_attendee": 2.0,
            "small_group": 2.0,
            "project_alignment": 2.0,
            "historical_importance": 2.0,
            "key_stakeholders": 2.0,
            
            # Standard Priority Signals (Weight: 1.0)
            "team_meeting": 1.0,
            "optional_status": 1.0,
            "training_learning": 1.0,
            "social_event": 1.0,
            
            # Low Priority Signals (Weight: 0.5)
            "information_sharing": 0.5,
            "adjacent_teams": 0.5,
            "recurring_low_value": 0.5,
            "outside_work_hours": 0.5,
            "no_response_history": 0.5
        }
    
    def test_ollama_connection(self) -> bool:
        """Test connection to Ollama server"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                logger.info(f"✅ Ollama connected. Available models: {available_models}")
                
                if not any(self.model_name in model for model in available_models):
                    logger.warning(f"⚠️ Model {self.model_name} not found. Available: {available_models}")
                    return False
                return True
            else:
                logger.error(f"❌ Ollama server responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to connect to Ollama: {e}")
            return False
    
    def detect_meeting_signals(self, meeting: Dict[str, Any]) -> List[Tuple[str, float, str]]:
        """
        Detect priority signals in meeting data
        
        Returns: List of (signal_name, weight, explanation) tuples
        """
        signals = []
        
        # Extract meeting properties
        organizer = meeting.get('organizer', {}).get('emailAddress', {}).get('address', '')
        attendees = [att.get('emailAddress', {}).get('address', '') for att in meeting.get('attendees', [])]
        subject = meeting.get('subject', '').lower()
        body = meeting.get('body', {}).get('content', '').lower()
        response_status = meeting.get('responseStatus', {}).get('response', '')
        
        # High Priority Signal Detection
        
        # User is organizer
        if organizer == self.user_profile.email:
            signals.append(("user_organizer", 3.0, "You are organizing this meeting"))
        
        # Manager/reporting chain involvement
        manager_involved = any(att in [self.user_profile.manager_email] + self.user_profile.direct_reports 
                             for att in attendees if att)
        if manager_involved:
            signals.append(("manager_chain", 3.0, "Manager or direct reports attending"))
        
        # 1-on-1 meeting (2 attendees including organizer)
        if len([att for att in attendees if att]) == 1:  # Only one other attendee
            signals.append(("one_on_one", 3.0, "One-on-one meeting"))
        
        # Last minute urgent
        if any(word in subject for word in ['urgent', 'asap', 'immediate', 'emergency']):
            signals.append(("urgent_last_minute", 3.0, "Urgent meeting"))
        
        # Personal appointments
        if any(word in subject for word in ['1:1', 'one-on-one', 'medical', 'doctor', 'personal', 'ooo', 'pto']):
            signals.append(("personal_appointment", 3.0, "Personal or strategic appointment"))
        
        # Medium Priority Signal Detection
        
        # Required attendee
        if response_status in ['accepted', 'organizer']:
            signals.append(("required_attendee", 2.0, "Marked as required or accepted"))
        
        # Small group (3-5 attendees)
        attendee_count = len([att for att in attendees if att])
        if 2 <= attendee_count <= 5:
            signals.append(("small_group", 2.0, f"Small group meeting ({attendee_count} attendees)"))
        
        # Key stakeholders
        key_attendees = any(att in self.user_profile.important_contacts for att in attendees if att)
        if key_attendees:
            signals.append(("key_stakeholders", 2.0, "Important contacts attending"))
        
        # Historical importance (organizer patterns)
        if organizer in self.user_profile.important_organizers:
            signals.append(("historical_importance", 2.0, f"Important organizer: {organizer}"))
        
        # Standard Priority Signal Detection
        
        # Team meetings
        if any(word in subject for word in ['standup', 'scrum', 'team', 'weekly', 'sync']):
            signals.append(("team_meeting", 1.0, "Regular team meeting"))
        
        # Training/Learning
        if any(word in subject for word in ['training', 'workshop', 'learning', 'demo', 'presentation']):
            signals.append(("training_learning", 1.0, "Training or learning session"))
        
        # Social events
        if any(word in subject for word in ['social', 'lunch', 'coffee', 'happy hour', 'celebration']):
            signals.append(("social_event", 1.0, "Social event"))
        
        # Low Priority Signal Detection
        
        # Information sharing (large groups)
        if attendee_count > 10:
            signals.append(("information_sharing", 0.5, f"Large group meeting ({attendee_count} attendees)"))
        
        # Optional status
        if response_status in ['tentative', 'declined', '']:
            signals.append(("optional_status", 0.5, "Optional or tentative attendance"))
        
        return signals
    
    def calculate_priority_score(self, signals: List[Tuple[str, float, str]]) -> float:
        """Calculate overall priority score from detected signals"""
        total_score = sum(weight for _, weight, _ in signals)
        
        # Apply Priority Calendar override logic: any high signal = high score
        high_signals = [s for s in signals if s[1] >= 3.0]
        if high_signals:
            base_score = max(8.0, total_score)  # Ensure high signals get 8+ score
        else:
            base_score = min(total_score, 10.0)  # Cap at 10
        
        return round(base_score, 1)
    
    def classify_engagement_level(self, signals: List[Tuple[str, float, str]], 
                                priority_score: float) -> str:
        """Determine engagement level based on signals and priority"""
        signal_names = [s[0] for s in signals]
        
        # Drive: User is organizing or leading
        if "user_organizer" in signal_names:
            return "Drive"
        
        # Participate: High priority with active role expected  
        if priority_score >= 7.0 and any(s in signal_names for s in ["manager_chain", "one_on_one", "key_stakeholders"]):
            return "Participate"
        
        # Attend: Medium priority, presence expected
        if priority_score >= 5.0:
            return "Attend"
        
        # Monitor: Low priority but worth tracking
        if priority_score >= 3.0:
            return "Monitor"
        
        # Skip: Very low priority
        return "Skip"
    
    def assess_preparation_level(self, engagement_level: str, signals: List[Tuple[str, float, str]]) -> str:
        """Determine preparation requirements"""
        signal_names = [s[0] for s in signals]
        
        if engagement_level == "Drive":
            return "Intensive"  # Organizing requires significant prep
        
        if engagement_level == "Participate":
            if any(s in signal_names for s in ["one_on_one", "key_stakeholders", "urgent_last_minute"]):
                return "Standard"  # Active participation needs prep
            return "Minimal"
        
        if engagement_level in ["Attend", "Monitor"]:
            return "Minimal" if "team_meeting" in signal_names else "None"
        
        return "None"  # Skip level
    
    def analyze_timing_factors(self, meeting: Dict[str, Any]) -> str:
        """Analyze timing optimization factors"""
        start_time = meeting.get('start', {}).get('dateTime', '')
        
        try:
            # Parse meeting time
            meeting_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            meeting_hour = meeting_dt.hour
            
            # Check work hours alignment
            work_start = int(self.user_profile.work_hours_start.split(':')[0])
            work_end = int(self.user_profile.work_hours_end.split(':')[0])
            
            if work_start <= meeting_hour <= work_end:
                return "Peak Hours"
            elif meeting_hour < work_start or meeting_hour > work_end:
                return "Off Hours"
            else:
                return "Standard Hours"
                
        except Exception:
            return "Unknown"
    
    def query_ollama(self, prompt: str, max_tokens: int = 500) -> str:
        """Query Ollama LLM for meeting analysis"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.1,  # Low temperature for consistent analysis
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return "Analysis unavailable"
                
        except Exception as e:
            logger.error(f"Ollama query failed: {e}")
            return "Analysis unavailable"
    
    def generate_reasoning_with_llm(self, meeting: Dict[str, Any], 
                                  signals: List[Tuple[str, float, str]], 
                                  ranking_result: Dict[str, Any]) -> str:
        """Generate detailed reasoning using Ollama LLM"""
        
        # Prepare meeting context for LLM
        meeting_context = {
            "subject": meeting.get('subject', 'No subject'),
            "organizer": meeting.get('organizer', {}).get('emailAddress', {}).get('address', 'Unknown'),
            "attendee_count": len(meeting.get('attendees', [])),
            "start_time": meeting.get('start', {}).get('dateTime', 'Unknown'),
            "response_status": meeting.get('responseStatus', {}).get('response', 'No response')
        }
        
        signals_text = "\n".join([f"- {name}: {explanation} (weight: {weight})" 
                                for name, weight, explanation in signals])
        
        prompt = f"""
You are an expert meeting prioritization analyst. Analyze this meeting and provide clear reasoning for its priority ranking.

MEETING DETAILS:
- Subject: {meeting_context['subject']}
- Organizer: {meeting_context['organizer']}
- Attendees: {meeting_context['attendee_count']} people
- Time: {meeting_context['start_time']}
- Your Response: {meeting_context['response_status']}

DETECTED PRIORITY SIGNALS:
{signals_text}

RANKING RESULTS:
- Priority Score: {ranking_result['priority_score']}/10
- Criticality: {ranking_result['criticality_score']}/10
- Engagement Level: {ranking_result['engagement_level']}
- Preparation Needed: {ranking_result['preparation_level']}

Provide a concise 2-3 sentence explanation of why this meeting received this priority ranking. Focus on the most important factors that influenced the decision.

REASONING:"""

        return self.query_ollama(prompt, max_tokens=200)
    
    def generate_recommendations(self, ranking_result: MeetingRankingResult) -> Dict[str, Any]:
        """Generate actionable recommendations based on ranking"""
        recommendations = {}
        
        # Auto-decision recommendation
        if ranking_result.criticality_score >= 8:
            recommendations["action"] = "auto_accept"
        elif ranking_result.criticality_score >= 5:
            recommendations["action"] = "suggest_accept"
        else:
            recommendations["action"] = "consider_decline"
        
        # Preparation time
        prep_times = {
            "Intensive": "2-3 hours",
            "Standard": "30-60 minutes", 
            "Minimal": "5-15 minutes",
            "None": "No preparation needed"
        }
        recommendations["prep_time"] = prep_times.get(ranking_result.preparation_level, "Unknown")
        
        # Buffer time recommendations
        if ranking_result.engagement_level in ["Drive", "Participate"]:
            recommendations["buffer_time"] = "15 minutes before, 10 minutes after"
        else:
            recommendations["buffer_time"] = "5 minutes before"
        
        # Focus protection
        if ranking_result.criticality_score >= 8:
            recommendations["focus_protection"] = "Block 30 minutes before for preparation"
        
        return recommendations
    
    def rank_meetings(self, meetings: List[Dict[str, Any]]) -> List[MeetingRankingResult]:
        """
        Rank a list of meetings using Priority Calendar framework
        
        Args:
            meetings: List of meeting dictionaries from Meeting Extraction Tool
            
        Returns:
            List of MeetingRankingResult objects, sorted by priority
        """
        if not self.test_ollama_connection():
            logger.warning("⚠️ Ollama not available, using basic ranking without LLM reasoning")
        
        ranking_results = []
        
        for meeting in meetings:
            try:
                # Detect priority signals
                signals = self.detect_meeting_signals(meeting)
                
                # Calculate priority score  
                priority_score = self.calculate_priority_score(signals)
                
                # Determine engagement and preparation levels
                engagement_level = self.classify_engagement_level(signals, priority_score)
                preparation_level = self.assess_preparation_level(engagement_level, signals)
                timing_optimization = self.analyze_timing_factors(meeting)
                
                # Create initial ranking result
                ranking_data = {
                    "priority_score": priority_score,
                    "criticality_score": min(int(priority_score), 10),
                    "engagement_level": engagement_level,
                    "preparation_level": preparation_level
                }
                
                # Generate LLM reasoning if available
                reasoning = self.generate_reasoning_with_llm(meeting, signals, ranking_data)
                
                # Create final result
                result = MeetingRankingResult(
                    meeting_id=meeting.get('id', f"meeting_{len(ranking_results)}"),
                    subject=meeting.get('subject', 'No subject'),
                    rank=0,  # Will be set after sorting
                    priority_score=priority_score,
                    criticality_score=ranking_data["criticality_score"],
                    engagement_level=engagement_level,
                    preparation_level=preparation_level,
                    timing_optimization=timing_optimization,
                    reasoning=reasoning,
                    signals_detected=[f"{name} ({weight})" for name, weight, _ in signals],
                    recommendations=self.generate_recommendations(
                        MeetingRankingResult(
                            meeting_id="temp", subject="temp", rank=0,
                            priority_score=priority_score, criticality_score=ranking_data["criticality_score"],
                            engagement_level=engagement_level, preparation_level=preparation_level,
                            timing_optimization=timing_optimization, reasoning="", signals_detected=[], 
                            recommendations={}, confidence="High"
                        )
                    ),
                    confidence="High" if len(signals) >= 2 else "Medium" if len(signals) == 1 else "Low"
                )
                
                ranking_results.append(result)
                
            except Exception as e:
                logger.error(f"Error ranking meeting {meeting.get('subject', 'Unknown')}: {e}")
                continue
        
        # Sort by priority score (descending) and assign ranks
        ranking_results.sort(key=lambda x: x.priority_score, reverse=True)
        for i, result in enumerate(ranking_results):
            result.rank = i + 1
        
        return ranking_results
    
    def display_ranked_meetings(self, ranked_meetings: List[MeetingRankingResult], 
                              format_type: str = "console") -> str:
        """Display ranked meetings in specified format"""
        
        if format_type == "console":
            return self._format_console_output(ranked_meetings)
        elif format_type == "markdown":
            return self._format_markdown_output(ranked_meetings)
        elif format_type == "json":
            return self._format_json_output(ranked_meetings)
        elif format_type == "html":
            return self._format_html_output(ranked_meetings)
        else:
            return self._format_console_output(ranked_meetings)
    
    def _format_console_output(self, ranked_meetings: List[MeetingRankingResult]) -> str:
        """Format for console display with colors"""
        output = []
        output.append("🗓️  MEETING PRIORITY RANKING")
        output.append("=" * 50)
        
        for meeting in ranked_meetings:
            # Priority color coding
            if meeting.priority_score >= 8:
                priority_color = "🔴"
                category = "CRITICAL"
            elif meeting.priority_score >= 6:
                priority_color = "🟡"
                category = "IMPORTANT"
            elif meeting.priority_score >= 4:
                priority_color = "🟢"
                category = "STANDARD"
            else:
                priority_color = "🔵"
                category = "OPTIONAL"
            
            output.append(f"\n{priority_color} #{meeting.rank} {category} (Score: {meeting.priority_score}/10)")
            output.append(f"📋 Subject: {meeting.subject}")
            output.append(f"🎯 Engagement: {meeting.engagement_level}")
            output.append(f"📚 Preparation: {meeting.preparation_level}")
            output.append(f"🤔 Reasoning: {meeting.reasoning}")
            output.append(f"🔧 Signals: {', '.join(meeting.signals_detected)}")
            output.append(f"✅ Action: {meeting.recommendations.get('action', 'N/A')}")
            output.append("-" * 40)
        
        return "\n".join(output)
    
    def _format_markdown_output(self, ranked_meetings: List[MeetingRankingResult]) -> str:
        """Format for Markdown display"""
        output = []
        output.append("# 🗓️ Meeting Priority Ranking Report")
        output.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        output.append("")
        
        # Summary table
        output.append("## 📊 Priority Summary")
        output.append("")
        output.append("| Priority | Count | Score Range |")
        output.append("|----------|-------|-------------|")
        
        critical = len([m for m in ranked_meetings if m.priority_score >= 8])
        important = len([m for m in ranked_meetings if 6 <= m.priority_score < 8])
        standard = len([m for m in ranked_meetings if 4 <= m.priority_score < 6])
        optional = len([m for m in ranked_meetings if m.priority_score < 4])
        
        output.append(f"| 🔴 Critical | {critical} | 8.0-10.0 |")
        output.append(f"| 🟡 Important | {important} | 6.0-7.9 |")
        output.append(f"| 🟢 Standard | {standard} | 4.0-5.9 |")
        output.append(f"| 🔵 Optional | {optional} | 0.0-3.9 |")
        output.append("")
        
        # Detailed rankings
        output.append("## 📋 Detailed Rankings")
        output.append("")
        
        for meeting in ranked_meetings:
            priority_emoji = "🔴" if meeting.priority_score >= 8 else "🟡" if meeting.priority_score >= 6 else "🟢" if meeting.priority_score >= 4 else "🔵"
            
            output.append(f"### {priority_emoji} #{meeting.rank} {meeting.subject}")
            output.append("")
            output.append(f"**Priority Score:** {meeting.priority_score}/10  ")
            output.append(f"**Engagement Level:** {meeting.engagement_level}  ")
            output.append(f"**Preparation:** {meeting.preparation_level}  ")
            output.append(f"**Timing:** {meeting.timing_optimization}  ")
            output.append(f"**Confidence:** {meeting.confidence}  ")
            output.append("")
            output.append(f"**Reasoning:** {meeting.reasoning}")
            output.append("")
            output.append(f"**Detected Signals:** {', '.join(meeting.signals_detected)}")
            output.append("")
            output.append("**Recommendations:**")
            for key, value in meeting.recommendations.items():
                output.append(f"- {key.replace('_', ' ').title()}: {value}")
            output.append("")
            output.append("---")
            output.append("")
        
        return "\n".join(output)
    
    def _format_json_output(self, ranked_meetings: List[MeetingRankingResult]) -> str:
        """Format as JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_meetings": len(ranked_meetings),
            "ranking_summary": {
                "critical": len([m for m in ranked_meetings if m.priority_score >= 8]),
                "important": len([m for m in ranked_meetings if 6 <= m.priority_score < 8]),
                "standard": len([m for m in ranked_meetings if 4 <= m.priority_score < 6]),
                "optional": len([m for m in ranked_meetings if m.priority_score < 4])
            },
            "ranked_meetings": [asdict(meeting) for meeting in ranked_meetings]
        }
        return json.dumps(data, indent=2, default=str)
    
    def _format_html_output(self, ranked_meetings: List[MeetingRankingResult]) -> str:
        """Format as HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Meeting Priority Ranking</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .critical {{ border-left: 5px solid #ff4444; background: #fff5f5; }}
        .important {{ border-left: 5px solid #ffaa44; background: #fffaf5; }}
        .standard {{ border-left: 5px solid #44ff44; background: #f5fff5; }}
        .optional {{ border-left: 5px solid #4444ff; background: #f5f5ff; }}
        .meeting {{ margin: 15px 0; padding: 15px; border-radius: 5px; }}
        .score {{ font-size: 1.2em; font-weight: bold; }}
        .signals {{ font-size: 0.9em; color: #666; }}
    </style>
</head>
<body>
    <h1>🗓️ Meeting Priority Ranking Report</h1>
    <p><em>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
"""
        
        for meeting in ranked_meetings:
            css_class = "critical" if meeting.priority_score >= 8 else "important" if meeting.priority_score >= 6 else "standard" if meeting.priority_score >= 4 else "optional"
            
            html += f"""
    <div class="meeting {css_class}">
        <h3>#{meeting.rank} {meeting.subject}</h3>
        <div class="score">Priority Score: {meeting.priority_score}/10</div>
        <p><strong>Engagement:</strong> {meeting.engagement_level} | 
           <strong>Preparation:</strong> {meeting.preparation_level} | 
           <strong>Confidence:</strong> {meeting.confidence}</p>
        <p><strong>Reasoning:</strong> {meeting.reasoning}</p>
        <div class="signals"><strong>Signals:</strong> {', '.join(meeting.signals_detected)}</div>
        <p><strong>Recommendation:</strong> {meeting.recommendations.get('action', 'N/A')}</p>
    </div>
"""
        
        html += """
</body>
</html>"""
        return html
    
    def save_ranking_results(self, ranked_meetings: List[MeetingRankingResult], 
                           output_dir: str = "meeting_rankings", 
                           date_suffix: str = None) -> Dict[str, str]:
        """Save ranking results in multiple formats"""
        if date_suffix is None:
            date_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        saved_files = {}
        
        # Save in all formats
        formats = {
            "markdown": self._format_markdown_output(ranked_meetings),
            "json": self._format_json_output(ranked_meetings),
            "html": self._format_html_output(ranked_meetings)
        }
        
        for format_type, content in formats.items():
            filename = f"meeting_rankings_{date_suffix}.{format_type}"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            saved_files[format_type] = str(filepath)
            logger.info(f"💾 Saved {format_type} ranking to: {filepath}")
        
        return saved_files


# Demo and testing functions
def create_demo_user_profile() -> UserProfile:
    """Create a demo user profile for testing"""
    return UserProfile(
        email="john.doe@company.com",
        manager_email="jane.smith@company.com",
        direct_reports=["alice.johnson@company.com", "bob.wilson@company.com"],
        important_contacts=["ceo@company.com", "vp.engineering@company.com"],
        important_organizers=["jane.smith@company.com", "project.manager@company.com"],
        work_hours_start="09:00",
        work_hours_end="17:00",
        timezone="UTC",
        preferred_prep_time=45,
        meeting_fatigue_threshold=5
    )

def create_demo_meetings() -> List[Dict[str, Any]]:
    """Create demo meetings for testing"""
    return [
        {
            "id": "meeting-001",
            "subject": "1:1 with Manager - Q4 Planning",
            "organizer": {"emailAddress": {"address": "jane.smith@company.com"}},
            "attendees": [
                {"emailAddress": {"address": "john.doe@company.com"}},
                {"emailAddress": {"address": "jane.smith@company.com"}}
            ],
            "start": {"dateTime": "2025-10-22T14:00:00Z"},
            "responseStatus": {"response": "accepted"},
            "body": {"content": "Quarterly planning and goal setting discussion"}
        },
        {
            "id": "meeting-002", 
            "subject": "Team Standup - Engineering",
            "organizer": {"emailAddress": {"address": "scrum.master@company.com"}},
            "attendees": [
                {"emailAddress": {"address": "john.doe@company.com"}},
                {"emailAddress": {"address": "alice.johnson@company.com"}},
                {"emailAddress": {"address": "bob.wilson@company.com"}},
                {"emailAddress": {"address": "charlie.brown@company.com"}}
            ],
            "start": {"dateTime": "2025-10-22T09:30:00Z"},
            "responseStatus": {"response": "accepted"},
            "body": {"content": "Daily standup meeting for engineering team"}
        },
        {
            "id": "meeting-003",
            "subject": "URGENT: Production Issue Review",
            "organizer": {"emailAddress": {"address": "john.doe@company.com"}},
            "attendees": [
                {"emailAddress": {"address": "alice.johnson@company.com"}},
                {"emailAddress": {"address": "bob.wilson@company.com"}},
                {"emailAddress": {"address": "devops.lead@company.com"}}
            ],
            "start": {"dateTime": "2025-10-22T16:00:00Z"},
            "responseStatus": {"response": "organizer"},
            "body": {"content": "Critical production issue needs immediate attention"}
        },
        {
            "id": "meeting-004",
            "subject": "Company All-Hands Meeting",
            "organizer": {"emailAddress": {"address": "ceo@company.com"}},
            "attendees": [{"emailAddress": {"address": f"employee{i}@company.com"}} for i in range(1, 51)],
            "start": {"dateTime": "2025-10-22T11:00:00Z"},
            "responseStatus": {"response": "tentative"},
            "body": {"content": "Monthly company update and announcements"}
        },
        {
            "id": "meeting-005",
            "subject": "Coffee Chat with New Team Member",
            "organizer": {"emailAddress": {"address": "hr@company.com"}},
            "attendees": [
                {"emailAddress": {"address": "john.doe@company.com"}},
                {"emailAddress": {"address": "new.hire@company.com"}}
            ],
            "start": {"dateTime": "2025-10-22T15:30:00Z"},
            "responseStatus": {"response": ""},
            "body": {"content": "Welcome coffee chat with new team member"}
        }
    ]

if __name__ == "__main__":
    # Demo execution
    print("🚀 Meeting Ranking Tool with Ollama LLM Integration")
    print("=" * 60)
    
    # Create demo profile and meetings
    user_profile = create_demo_user_profile()
    demo_meetings = create_demo_meetings()
    
    # Initialize ranker
    ranker = OllamaMeetingRanker(
        ollama_url="http://localhost:11434",
        model_name="llama3.1",
        user_profile=user_profile
    )
    
    # Test Ollama connection
    print("\n🔍 Testing Ollama connection...")
    if ranker.test_ollama_connection():
        print("✅ Ollama server is ready!")
    else:
        print("⚠️ Ollama not available - proceeding with basic ranking")
    
    # Rank the meetings
    print("\n🎯 Ranking meetings...")
    ranked_meetings = ranker.rank_meetings(demo_meetings)
    
    # Display results
    print("\n" + ranker.display_ranked_meetings(ranked_meetings, "console"))
    
    # Save results
    print("\n💾 Saving ranking results...")
    saved_files = ranker.save_ranking_results(ranked_meetings)
    
    for format_type, filepath in saved_files.items():
        print(f"📄 {format_type.upper()}: {filepath}")
    
    print("\n✅ Meeting ranking complete!")