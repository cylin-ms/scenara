#!/usr/bin/env python3
"""
Enhanced Meeting Ranking Tool with Me Notes Integration
Proof-of-concept implementation showing how Me Notes can enhance meeting prioritization
"""

import json
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import re
from pathlib import Path

# Import base classes from our existing tool
import sys
sys.path.append(str(Path(__file__).parent))
from meeting_ranking_tool import (
    OllamaMeetingRanker, 
    MeetingRankingResult, 
    UserProfile,
    create_demo_user_profile,
    create_demo_meetings
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MeNote:
    """Structure representing a Me Note from Microsoft's system"""
    note: str
    category: str  # e.g., WORK_RELATED, FOLLOW_UPS, BEHAVIORAL_PATTERN
    title: str
    temporal_durability: str  # e.g., TEMPORAL_SHORT_LIVED, DURABLE
    timestamp: datetime
    confidence: float = 0.8
    
@dataclass
class EnhancedUserProfile(UserProfile):
    """User profile enhanced with Me Notes insights"""
    # Me Notes derived fields
    current_projects: List[str] = None
    expertise_areas: List[Dict[str, Any]] = None
    interests: List[Dict[str, Any]] = None
    behavioral_patterns: List[str] = None
    communication_style: str = None
    decision_making_style: str = None
    recent_interactions: List[str] = None
    
    # Me Notes metadata
    me_notes_last_updated: datetime = None
    me_notes_count: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        if self.current_projects is None:
            self.current_projects = []
        if self.expertise_areas is None:
            self.expertise_areas = []
        if self.interests is None:
            self.interests = []
        if self.behavioral_patterns is None:
            self.behavioral_patterns = []
        if self.recent_interactions is None:
            self.recent_interactions = []

class MeNotesSimulator:
    """
    Simulates Me Notes for demonstration purposes
    In production, this would connect to actual Me Notes APIs
    """
    
    def __init__(self, user_email: str):
        self.user_email = user_email
        self.demo_notes = self._generate_demo_notes()
    
    def _generate_demo_notes(self) -> List[MeNote]:
        """Generate realistic demo Me Notes for testing"""
        base_date = datetime.now() - timedelta(days=7)
        
        demo_notes = [
            # Current Projects (Level 1 - Factual)
            MeNote(
                note="John is actively working on the Priority Calendar project implementation",
                category="WORK_RELATED",
                title="Priority Calendar Project",
                temporal_durability="TEMPORAL_SHORT_LIVED",
                timestamp=base_date + timedelta(days=1),
                confidence=0.95
            ),
            MeNote(
                note="John is leading the Meeting Intelligence initiative for Q4",
                category="WORK_RELATED", 
                title="Meeting Intelligence Lead",
                temporal_durability="TEMPORAL_SHORT_LIVED",
                timestamp=base_date + timedelta(days=2),
                confidence=0.9
            ),
            MeNote(
                note="John is collaborating with the AI team on LLM integration",
                category="WORK_RELATED",
                title="LLM Integration Collaboration",
                temporal_durability="TEMPORAL_SHORT_LIVED",
                timestamp=base_date + timedelta(days=3),
                confidence=0.85
            ),
            
            # Expertise Areas (Level 2 - Synthesized)
            MeNote(
                note="John demonstrates strong expertise in calendar intelligence and meeting optimization",
                category="EXPERTISE",
                title="Calendar Intelligence Expert",
                temporal_durability="DURABLE",
                timestamp=base_date + timedelta(days=4),
                confidence=0.9
            ),
            MeNote(
                note="John has deep knowledge of AI/ML integration in productivity tools",
                category="EXPERTISE",
                title="AI/ML Integration Specialist",
                temporal_durability="DURABLE",
                timestamp=base_date + timedelta(days=5),
                confidence=0.85
            ),
            
            # Behavioral Patterns (Level 2 - Synthesized)
            MeNote(
                note="John prefers morning meetings for strategic discussions and decision making",
                category="BEHAVIORAL_PATTERN",
                title="Morning Strategic Preference",
                temporal_durability="DURABLE",
                timestamp=base_date + timedelta(days=1),
                confidence=0.8
            ),
            MeNote(
                note="John carefully analyzes technical requirements before making implementation decisions",
                category="BEHAVIORAL_PATTERN",
                title="Analytical Decision Style",
                temporal_durability="DURABLE",
                timestamp=base_date + timedelta(days=2),
                confidence=0.85
            ),
            MeNote(
                note="John values concise, well-structured meetings with clear agendas",
                category="BEHAVIORAL_PATTERN",
                title="Structured Meeting Preference",
                temporal_durability="DURABLE",
                timestamp=base_date + timedelta(days=3),
                confidence=0.9
            ),
            
            # Interests and Focus Areas
            MeNote(
                note="John shows strong interest in productivity optimization and automation",
                category="INTERESTS",
                title="Productivity Optimization Interest",
                temporal_durability="DURABLE",
                timestamp=base_date + timedelta(days=4),
                confidence=0.8
            ),
            MeNote(
                note="John is actively learning about advanced LLM applications in enterprise software",
                category="INTERESTS",
                title="Enterprise LLM Applications",
                temporal_durability="TEMPORAL_SHORT_LIVED",
                timestamp=base_date + timedelta(days=5),
                confidence=0.75
            ),
            
            # Recent Interactions and Follow-ups
            MeNote(
                note="John had productive discussions with Jane Smith about Q4 planning priorities",
                category="FOLLOW_UPS",
                title="Q4 Planning with Manager",
                temporal_durability="TEMPORAL_SHORT_LIVED",
                timestamp=base_date + timedelta(days=6),
                confidence=0.9
            ),
            MeNote(
                note="John needs to follow up on the production issue resolution with the DevOps team",
                category="FOLLOW_UPS",
                title="Production Issue Follow-up",
                temporal_durability="TEMPORAL_SHORT_LIVED",
                timestamp=base_date + timedelta(days=7),
                confidence=0.95
            )
        ]
        
        return demo_notes
    
    def get_me_notes(self, category_filter: List[str] = None, days_back: int = 30) -> List[MeNote]:
        """Retrieve Me Notes with optional filtering"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        filtered_notes = []
        for note in self.demo_notes:
            # Filter by category if specified
            if category_filter and note.category not in category_filter:
                continue
            
            # Include all durable notes, recent temporal notes
            if (note.temporal_durability == "DURABLE" or 
                note.timestamp > cutoff_date):
                filtered_notes.append(note)
        
        return filtered_notes

class MeNotesEnhancedRanker(OllamaMeetingRanker):
    """Meeting Ranker enhanced with Me Notes personalization"""
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 model_name: str = "gemma2:latest",
                 user_profile: Optional[EnhancedUserProfile] = None):
        
        # Initialize base ranker
        super().__init__(ollama_url, model_name, user_profile)
        
        # Initialize Me Notes integration
        self.me_notes_sim = MeNotesSimulator(user_profile.email if user_profile else "john.doe@company.com")
        
        # Enhanced signal weights including Me Notes signals
        self.enhanced_signal_weights = {
            **self.signal_weights,  # Original signals
            
            # Me Notes enhanced signals
            "active_project_match": 3.0,        # Meeting relates to current project
            "expertise_area_match": 2.5,        # Meeting in user's expertise area
            "high_interest_topic": 2.0,         # Meeting matches high-interest areas
            "recent_interaction_followup": 2.0, # Follows up on recent interactions
            "behavioral_alignment": 1.5,        # Aligns with behavioral preferences
            "learning_opportunity": 1.5,        # Offers learning in interest areas
            "strategic_initiative": 3.0,        # Relates to strategic initiatives
            "follow_up_required": 2.5,          # Addresses required follow-ups
        }
    
    def update_profile_from_me_notes(self, me_notes: List[MeNote]) -> EnhancedUserProfile:
        """Update user profile based on Me Notes insights"""
        profile = self.user_profile
        
        # Extract current projects
        profile.current_projects = []
        for note in me_notes:
            if note.category == "WORK_RELATED" and "project" in note.note.lower():
                project_keywords = self._extract_project_keywords(note.note)
                profile.current_projects.extend(project_keywords)
        
        # Extract expertise areas
        profile.expertise_areas = []
        for note in me_notes:
            if note.category == "EXPERTISE":
                expertise = {
                    "area": note.title,
                    "description": note.note,
                    "confidence": note.confidence,
                    "keywords": self._extract_keywords(note.note)
                }
                profile.expertise_areas.append(expertise)
        
        # Extract interests
        profile.interests = []
        for note in me_notes:
            if note.category == "INTERESTS":
                interest = {
                    "topic": note.title,
                    "description": note.note,
                    "strength": "high" if note.confidence > 0.8 else "medium",
                    "keywords": self._extract_keywords(note.note)
                }
                profile.interests.append(interest)
        
        # Extract behavioral patterns
        profile.behavioral_patterns = []
        for note in me_notes:
            if note.category == "BEHAVIORAL_PATTERN":
                profile.behavioral_patterns.append(note.note)
        
        # Extract recent interactions
        profile.recent_interactions = []
        for note in me_notes:
            if note.category == "FOLLOW_UPS":
                interactions = self._extract_people_mentions(note.note)
                profile.recent_interactions.extend(interactions)
        
        # Update metadata
        profile.me_notes_last_updated = datetime.now()
        profile.me_notes_count = len(me_notes)
        
        return profile
    
    def _extract_project_keywords(self, note_text: str) -> List[str]:
        """Extract project names and keywords from note text"""
        # Simple extraction - in production would use more sophisticated NLP
        projects = []
        
        # Look for common project patterns
        patterns = [
            r"Priority Calendar",
            r"Meeting Intelligence", 
            r"LLM integration",
            r"Q4 planning",
            r"Project (\w+)",
            r"(\w+) project",
            r"(\w+) initiative"
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, note_text, re.IGNORECASE)
            for match in matches:
                if match.group().lower() not in ["the", "a", "an", "this", "that"]:
                    projects.append(match.group())
        
        return list(set(projects))  # Remove duplicates
    
    def _extract_keywords(self, note_text: str) -> List[str]:
        """Extract relevant keywords from note text"""
        # Simple keyword extraction
        keywords = []
        
        # Common technical and business keywords
        keyword_patterns = [
            r"calendar", r"meeting", r"intelligence", r"AI", r"ML", r"LLM",
            r"productivity", r"automation", r"optimization", r"strategic",
            r"planning", r"decision", r"analysis", r"integration", r"collaboration"
        ]
        
        for pattern in keyword_patterns:
            if re.search(pattern, note_text, re.IGNORECASE):
                keywords.append(pattern)
        
        return keywords
    
    def _extract_people_mentions(self, note_text: str) -> List[str]:
        """Extract people mentions from note text"""
        # Simple people extraction
        people = []
        
        # Look for common name patterns and email patterns
        name_patterns = [
            r"[A-Z][a-z]+ [A-Z][a-z]+",  # First Last
            r"[a-zA-Z]+@[a-zA-Z]+\.com"  # email addresses
        ]
        
        for pattern in name_patterns:
            matches = re.finditer(pattern, note_text)
            for match in matches:
                people.append(match.group())
        
        return people
    
    def detect_me_notes_enhanced_signals(self, meeting: Dict[str, Any], me_notes: List[MeNote]) -> List[Tuple[str, float, str]]:
        """Detect enhanced signals using Me Notes insights"""
        signals = []
        meeting_subject = meeting.get('subject', '').lower()
        meeting_body = meeting.get('body', {}).get('content', '').lower()
        meeting_text = f"{meeting_subject} {meeting_body}"
        
        # 1. Active Project Match
        for note in me_notes:
            if note.category == "WORK_RELATED":
                project_keywords = self._extract_project_keywords(note.note)
                for keyword in project_keywords:
                    if keyword.lower() in meeting_text:
                        confidence_boost = note.confidence * 0.5  # Scale confidence to signal strength
                        weight = 3.0 + confidence_boost
                        signals.append(("active_project_match", weight, f"Relates to active project: {keyword}"))
        
        # 2. Expertise Area Match
        for note in me_notes:
            if note.category == "EXPERTISE":
                keywords = self._extract_keywords(note.note)
                for keyword in keywords:
                    if keyword.lower() in meeting_text:
                        weight = 2.5 + (note.confidence * 0.5)
                        signals.append(("expertise_area_match", weight, f"Matches expertise: {note.title}"))
        
        # 3. Interest Topic Match
        for note in me_notes:
            if note.category == "INTERESTS":
                keywords = self._extract_keywords(note.note)
                for keyword in keywords:
                    if keyword.lower() in meeting_text:
                        weight = 2.0 if note.confidence > 0.8 else 1.5
                        signals.append(("high_interest_topic", weight, f"Matches interest: {note.title}"))
        
        # 4. Recent Interaction Follow-up
        meeting_organizer = meeting.get('organizer', {}).get('emailAddress', {}).get('address', '')
        for note in me_notes:
            if note.category == "FOLLOW_UPS":
                people_mentioned = self._extract_people_mentions(note.note)
                for person in people_mentioned:
                    if person.lower() in meeting_organizer.lower() or person.lower() in meeting_text:
                        signals.append(("recent_interaction_followup", 2.0, f"Follow-up with {person}"))
        
        # 5. Behavioral Alignment  
        for note in me_notes:
            if note.category == "BEHAVIORAL_PATTERN":
                # Morning preference check
                if "morning" in note.note.lower() and "strategic" in note.note.lower():
                    meeting_time = meeting.get('start', {}).get('dateTime', '')
                    if meeting_time and self._is_morning_meeting(meeting_time):
                        if any(word in meeting_subject for word in ["planning", "strategy", "decision"]):
                            signals.append(("behavioral_alignment", 1.5, "Aligns with morning strategic preference"))
                
                # Structured meeting preference
                if "structured" in note.note.lower() and "agenda" in note.note.lower():
                    if any(word in meeting_subject for word in ["review", "planning", "standup"]):
                        signals.append(("behavioral_alignment", 1.5, "Aligns with structured meeting preference"))
        
        # 6. Strategic Initiative Match
        for note in me_notes:
            if "strategic" in note.note.lower() or "initiative" in note.note.lower():
                if any(word in meeting_subject for word in ["strategic", "initiative", "planning", "roadmap"]):
                    signals.append(("strategic_initiative", 3.0, "Relates to strategic initiative"))
        
        return signals
    
    def _is_morning_meeting(self, meeting_time: str) -> bool:
        """Check if meeting is in the morning"""
        try:
            dt = datetime.fromisoformat(meeting_time.replace('Z', '+00:00'))
            return dt.hour < 12
        except:
            return False
    
    def generate_enhanced_reasoning(self, meeting: Dict[str, Any], 
                                  all_signals: List[Tuple[str, float, str]], 
                                  me_notes: List[MeNote],
                                  ranking_result: Dict[str, Any]) -> str:
        """Generate enhanced reasoning using Me Notes context"""
        
        # Prepare Me Notes context summary
        current_projects = [note.title for note in me_notes if note.category == "WORK_RELATED"]
        expertise_areas = [note.title for note in me_notes if note.category == "EXPERTISE"]
        interests = [note.title for note in me_notes if note.category == "INTERESTS"]
        behavioral_patterns = [note.note for note in me_notes if note.category == "BEHAVIORAL_PATTERN"]
        
        context_summary = f"""
PERSONAL CONTEXT:
- Current Projects: {', '.join(current_projects[:3]) if current_projects else 'None'}
- Expertise Areas: {', '.join(expertise_areas[:2]) if expertise_areas else 'None'}
- Key Interests: {', '.join(interests[:2]) if interests else 'None'}
- Work Patterns: {behavioral_patterns[0][:50] + '...' if behavioral_patterns else 'None'}
"""
        
        # Enhanced prompt for LLM
        meeting_context = {
            "subject": meeting.get('subject', 'No subject'),
            "organizer": meeting.get('organizer', {}).get('emailAddress', {}).get('address', 'Unknown'),
            "attendee_count": len(meeting.get('attendees', [])),
            "start_time": meeting.get('start', {}).get('dateTime', 'Unknown')
        }
        
        signals_text = "\n".join([f"- {name}: {explanation} (weight: {weight})" 
                                for name, weight, explanation in all_signals])
        
        prompt = f"""
You are an expert meeting prioritization analyst with deep personal context about the user.

MEETING DETAILS:
- Subject: {meeting_context['subject']}
- Organizer: {meeting_context['organizer']}
- Attendees: {meeting_context['attendee_count']} people
- Time: {meeting_context['start_time']}

{context_summary}

DETECTED PRIORITY SIGNALS (Including Personal Context):
{signals_text}

RANKING RESULTS:
- Priority Score: {ranking_result['priority_score']}/10
- Engagement Level: {ranking_result['engagement_level']}

Provide a personalized explanation incorporating the user's current projects, expertise, interests, and work patterns. Explain how this meeting aligns with their personal context and priorities.

PERSONALIZED REASONING:"""

        return self.query_ollama(prompt, max_tokens=250)
    
    def rank_meetings(self, meetings: List[Dict[str, Any]]) -> List[MeetingRankingResult]:
        """Rank meetings with Me Notes enhancement"""
        
        if not self.test_ollama_connection():
            logger.warning("⚠️ Ollama not available, using basic ranking")
        
        # Get fresh Me Notes
        me_notes = self.me_notes_sim.get_me_notes()
        logger.info(f"📝 Retrieved {len(me_notes)} Me Notes for enhanced ranking")
        
        # Update profile with Me Notes insights
        self.user_profile = self.update_profile_from_me_notes(me_notes)
        
        ranking_results = []
        
        for meeting in meetings:
            try:
                # Detect standard signals
                standard_signals = self.detect_meeting_signals(meeting)
                
                # Detect Me Notes enhanced signals
                enhanced_signals = self.detect_me_notes_enhanced_signals(meeting, me_notes)
                
                # Combine all signals
                all_signals = standard_signals + enhanced_signals
                
                # Calculate enhanced priority score
                priority_score = self.calculate_priority_score(all_signals)
                
                # Classify engagement and preparation with enhanced context
                engagement_level = self.classify_engagement_level(all_signals, priority_score)
                preparation_level = self.assess_preparation_level(engagement_level, all_signals)
                timing_optimization = self.analyze_timing_factors(meeting)
                
                # Create ranking data for LLM reasoning
                ranking_data = {
                    "priority_score": priority_score,
                    "criticality_score": min(int(priority_score), 10),
                    "engagement_level": engagement_level,
                    "preparation_level": preparation_level
                }
                
                # Generate enhanced reasoning with personal context
                reasoning = self.generate_enhanced_reasoning(meeting, all_signals, me_notes, ranking_data)
                
                # Count Me Notes enhanced signals
                me_notes_signal_count = len(enhanced_signals)
                
                # Create enhanced result
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
                    signals_detected=[f"{name} ({weight})" for name, weight, _ in all_signals],
                    recommendations={},  # Will be filled after result creation
                    confidence="High" if len(all_signals) >= 3 else "Medium" if len(all_signals) >= 1 else "Low"
                )
                
                # Generate enhanced recommendations after result creation
                result.recommendations = self.generate_enhanced_recommendations(result, me_notes, me_notes_signal_count)
                
                ranking_results.append(result)
                
            except Exception as e:
                logger.error(f"Error ranking meeting {meeting.get('subject', 'Unknown')}: {e}")
                continue
        
        # Sort by priority score and assign ranks
        ranking_results.sort(key=lambda x: x.priority_score, reverse=True)
        for i, result in enumerate(ranking_results):
            result.rank = i + 1
        
        return ranking_results
    
    def generate_enhanced_recommendations(self, result: MeetingRankingResult, 
                                        me_notes: List[MeNote], 
                                        me_notes_signal_count: int) -> Dict[str, Any]:
        """Generate enhanced recommendations incorporating Me Notes insights"""
        recommendations = self.generate_recommendations(result)
        
        # Add Me Notes specific recommendations
        if me_notes_signal_count > 0:
            recommendations["personalization_note"] = f"Enhanced with {me_notes_signal_count} personal context signals"
        
        # Project-specific recommendations
        current_projects = [note.title for note in me_notes if note.category == "WORK_RELATED"]
        if current_projects and any(proj.lower() in result.subject.lower() for proj in current_projects):
            recommendations["project_relevance"] = "High - directly relates to active projects"
        
        # Expertise utilization
        expertise_areas = [note.title for note in me_notes if note.category == "EXPERTISE"]
        if expertise_areas and any(exp.lower() in result.subject.lower() for exp in expertise_areas):
            recommendations["expertise_utilization"] = "Leverages your expertise effectively"
        
        # Behavioral alignment
        behavioral_patterns = [note.note for note in me_notes if note.category == "BEHAVIORAL_PATTERN"]
        if behavioral_patterns:
            recommendations["behavioral_alignment"] = "Aligns with your work patterns and preferences"
        
        return recommendations

def create_enhanced_demo_user_profile() -> EnhancedUserProfile:
    """Create enhanced demo user profile"""
    base_profile = create_demo_user_profile()
    
    enhanced_profile = EnhancedUserProfile(
        email=base_profile.email,
        manager_email=base_profile.manager_email,
        direct_reports=base_profile.direct_reports,
        important_contacts=base_profile.important_contacts,
        important_organizers=base_profile.important_organizers,
        work_hours_start=base_profile.work_hours_start,
        work_hours_end=base_profile.work_hours_end,
        timezone=base_profile.timezone,
        preferred_prep_time=base_profile.preferred_prep_time,
        meeting_fatigue_threshold=base_profile.meeting_fatigue_threshold,
        
        # Enhanced fields (will be populated from Me Notes)
        current_projects=[],
        expertise_areas=[],
        interests=[],
        behavioral_patterns=[],
        recent_interactions=[],
        me_notes_last_updated=None,
        me_notes_count=0
    )
    
    return enhanced_profile

def demo_me_notes_enhanced_ranking():
    """Demonstrate Me Notes enhanced meeting ranking"""
    print("🧠 Me Notes Enhanced Meeting Ranking Demo")
    print("=" * 50)
    
    # Create enhanced user profile
    user_profile = create_enhanced_demo_user_profile()
    print(f"👤 User: {user_profile.email}")
    
    # Initialize enhanced ranker
    ranker = MeNotesEnhancedRanker(
        model_name="gemma2:latest",
        user_profile=user_profile
    )
    
    # Test Me Notes integration
    print("\n📝 Retrieving Me Notes...")
    me_notes = ranker.me_notes_sim.get_me_notes()
    print(f"✅ Retrieved {len(me_notes)} Me Notes")
    
    # Display sample Me Notes
    print("\n📋 Sample Me Notes:")
    for i, note in enumerate(me_notes[:3]):
        print(f"   {i+1}. [{note.category}] {note.title}")
        print(f"      {note.note[:80]}...")
        print(f"      Confidence: {note.confidence:.2f} | Durability: {note.temporal_durability}")
        print()
    
    # Update profile from Me Notes
    updated_profile = ranker.update_profile_from_me_notes(me_notes)
    print(f"🔄 Profile Updated:")
    print(f"   Current Projects: {updated_profile.current_projects[:3]}")
    print(f"   Expertise Areas: {len(updated_profile.expertise_areas)} areas")
    print(f"   Interests: {len(updated_profile.interests)} interests")
    print(f"   Behavioral Patterns: {len(updated_profile.behavioral_patterns)} patterns")
    
    # Create demo meetings
    demo_meetings = create_demo_meetings()
    
    # Add a meeting that should trigger Me Notes enhancements
    priority_calendar_meeting = {
        "id": "enhanced-meeting-001",
        "subject": "Priority Calendar Project Review and LLM Integration Planning",
        "organizer": {"emailAddress": {"address": "jane.smith@company.com"}},
        "attendees": [
            {"emailAddress": {"address": "john.doe@company.com"}},
            {"emailAddress": {"address": "ai.researcher@company.com"}},
            {"emailAddress": {"address": "product.manager@company.com"}}
        ],
        "start": {"dateTime": "2025-10-22T09:00:00Z"},  # Morning meeting
        "responseStatus": {"response": "accepted"},
        "body": {"content": "Strategic review of Priority Calendar implementation progress and planning for advanced LLM integration features"}
    }
    demo_meetings.append(priority_calendar_meeting)
    
    print(f"\n🎯 Ranking {len(demo_meetings)} meetings with Me Notes enhancement...")
    
    # Rank meetings with Me Notes enhancement
    ranked_meetings = ranker.rank_meetings(demo_meetings)
    
    # Display enhanced results
    print("\n📊 Me Notes Enhanced Rankings:")
    print("=" * 70)
    
    for meeting in ranked_meetings:
        # Enhanced priority indicator
        if meeting.priority_score >= 10:
            priority_emoji = "🔴⭐"  # Super critical with enhancement
            category = "ENHANCED CRITICAL"
        elif meeting.priority_score >= 8:
            priority_emoji = "🔴"
            category = "CRITICAL"
        elif meeting.priority_score >= 6:
            priority_emoji = "🟡"
            category = "IMPORTANT"
        elif meeting.priority_score >= 4:
            priority_emoji = "🟢"
            category = "STANDARD"
        else:
            priority_emoji = "🔵"
            category = "OPTIONAL"
        
        print(f"\n{priority_emoji} #{meeting.rank} {category} (Score: {meeting.priority_score}/10)")
        print(f"📋 Subject: {meeting.subject}")
        print(f"🎯 Engagement: {meeting.engagement_level} | 📚 Preparation: {meeting.preparation_level}")
        
        # Show Me Notes enhancement indicators
        me_notes_signals = [s for s in meeting.signals_detected if any(
            term in s for term in ["project_match", "expertise", "interest", "behavioral", "strategic"]
        )]
        
        if me_notes_signals:
            print(f"🧠 Me Notes Enhanced: {len(me_notes_signals)} personal signals detected")
            for signal in me_notes_signals[:2]:  # Show top 2
                print(f"   • {signal}")
        
        print(f"🤔 Enhanced Reasoning: {meeting.reasoning}")
        
        # Show enhanced recommendations
        if "personalization_note" in meeting.recommendations:
            print(f"⭐ {meeting.recommendations['personalization_note']}")
        
        print("-" * 50)
    
    # Generate Me Notes insights summary
    print("\n📈 Me Notes Integration Insights:")
    enhanced_meetings = [m for m in ranked_meetings if any(
        term in " ".join(m.signals_detected) for term in ["project_match", "expertise", "interest"]
    )]
    
    print(f"   🧠 Meetings Enhanced by Me Notes: {len(enhanced_meetings)}/{len(ranked_meetings)}")
    print(f"   📊 Average Priority Boost: {sum(m.priority_score for m in enhanced_meetings) / len(enhanced_meetings) - 5:.1f} points" if enhanced_meetings else "   📊 No enhancement applied")
    print(f"   🎯 Personal Context Utilization: {len(updated_profile.current_projects)} projects, {len(updated_profile.expertise_areas)} expertise areas")
    
    # Save enhanced results
    saved_files = ranker.save_ranking_results(
        ranked_meetings, 
        output_dir="me_notes_enhanced_rankings",
        date_suffix="demo_enhanced"
    )
    
    print(f"\n💾 Enhanced ranking results saved:")
    for format_type, filepath in saved_files.items():
        print(f"📄 {format_type.upper()}: {filepath}")
    
    print(f"\n✅ Me Notes Enhanced Meeting Ranking Demo Complete!")
    
    return {
        "enhanced_meetings": enhanced_meetings,
        "total_meetings": len(ranked_meetings),
        "me_notes_count": len(me_notes),
        "profile_updates": {
            "projects": len(updated_profile.current_projects),
            "expertise": len(updated_profile.expertise_areas),
            "interests": len(updated_profile.interests),
            "behaviors": len(updated_profile.behavioral_patterns)
        }
    }

if __name__ == "__main__":
    print("🚀 Me Notes Enhanced Meeting Ranking Tool")
    print("Demonstration of personalized meeting prioritization using Me Notes insights")
    print("=" * 80)
    
    try:
        # Run the enhanced demo
        demo_results = demo_me_notes_enhanced_ranking()
        
        print(f"\n🎉 Demo Results Summary:")
        print(f"   📊 Total Meetings Analyzed: {demo_results['total_meetings']}")
        print(f"   🧠 Meetings Enhanced by Me Notes: {demo_results['enhanced_meetings']}")
        print(f"   📝 Me Notes Processed: {demo_results['me_notes_count']}")
        print(f"   👤 Profile Enhancements: {demo_results['profile_updates']}")
        
        print(f"\n🔮 Next Steps:")
        print(f"   1. Connect to real Me Notes APIs for live data")
        print(f"   2. Implement continuous learning from user feedback")
        print(f"   3. Add cross-meeting pattern recognition")
        print(f"   4. Build personal insights dashboard")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()