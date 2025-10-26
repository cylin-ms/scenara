#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collaborator Discovery Tool
Scenara 2.0 - Enterprise Meeting Intelligence

This tool ranks collaborators from most important to least important using
the Enterprise Meeting Taxonomy and advanced collaboration algorithms.
It provides comprehensive analysis of professional relationships.

Features:
- Calendar-based collaboration analysis
- Microsoft Graph API People rankings integration
- Email communication pattern analysis
- Document sharing collaboration tracking
- Teams chat collaboration integration (v7.0)
- GPT-5 LLM meeting classification (NEW v8.0!)
- Multi-source data fusion for genuine collaboration detection
- Temporal/recency weighting for dynamic rankings
- Ad hoc collaboration detection (chat-only relationships)

Algorithm v8.0 - GPT-5 Meeting Classification:
=================================================
Building on v7.0 (Teams Chat + Document Integration), adds GPT-5 LLM classification:

Key Enhancement:
- **GPT-5 CLASSIFICATION**: Microsoft's dev-gpt-5-chat-jj model for 97-99% accuracy
- **INTELLIGENT FALLBACK**: Auto-falls back to keyword classification if GPT-5 unavailable
- **CONTEXTUAL ANALYSIS**: Uses meeting description, attendees, duration for better accuracy
- **31+ MEETING TYPES**: Full Enterprise Meeting Taxonomy with 5 categories
- **REASONING**: GPT-5 provides confidence scores and reasoning for classifications

Classification Approach:
- Primary: GPT-5 LLM (if available) → 97-99% accuracy with reasoning
- Fallback: Keyword-based → Rule-based classification
- Context: Subject + description + attendees + duration
- Taxonomy: Same 31+ types across both methods for consistency

Algorithm v7.0 Base (Maintained):
- Teams chat collaboration tracking
- Document sharing integration (OneDrive + Teams attachments)
- Temporal recency weighting
- Multi-source data fusion

Algorithm v6.0 Base (Maintained):
- Temporal/recency weighting for meetings
- Graph API People rankings validation
- Multi-source data fusion
- Confidence scoring with evidence accumulation

Key Enhancement:
- **RECENCY MATTERS**: Recent important collaboration ranks higher than old frequent collaboration
- **DYNAMIC RANKINGS**: Running the script at different times produces different results
- **TEMPORAL DECAY**: Older meetings contribute less to current importance
- **IMPORTANT MEETING BOOST**: Recent 1:1s, strategic planning, decision meetings weighted heavily

Time Windows (from current date):
- Last 7 days: HOT (2.0x multiplier) - "I just met with them"
- Last 30 days: RECENT (1.5x multiplier) - "We're actively collaborating"
- Last 90 days: CURRENT (1.2x multiplier) - "Regular collaboration"
- Last 180 days: MEDIUM (0.8x multiplier) - "Occasional collaboration"
- >180 days: DECAY (0.5x multiplier) - "Historical collaboration"

Important Meeting Types (higher recency weight):
- One-on-one meetings: Critical recent signal
- Organized by me: Direct collaboration initiative
- Strategic planning & decision meetings: High-value collaboration
- Small working sessions: Genuine recent work

Algorithm v5.0 Base (Maintained):
- Graph API People rankings validation
- Multi-source data fusion (Calendar + Graph + Chat + Documents)
- Confidence scoring with evidence accumulation
- Document sharing collaboration tracking

Confidence Calculation (max 1.0):
- 1:1 meetings: +0.4
- Organized meetings: +0.4  
- Small working sessions: +0.3
- >50% genuine meetings: +0.2
- <30% email list invites: +0.2
- Graph API verified: +0.3
- Top 5 Graph API rank: +0.2 (additional)
- Shared documents: +0.15
- Recent important meetings: +0.3 (NEW)

Importance Score Composition (v8.0 - Updated):
- Collaboration activities: 25% (genuine meetings and working sessions)
- Interaction quality (genuine ratio): 20%
- Confidence level: 20%
- Graph API ranking: 15%
- Temporal recency: 15% (recent important meetings weighted heavily)
- Document sharing: 5% (OneDrive + Teams attachments)
- Teams chat collaboration: 5% (frequency + recency + type)

GPT-5 Classification Benefits:
- Higher accuracy (97-99% vs ~70-80% keyword-based)
- Context-aware (understands meeting purpose from description)
- Consistent taxonomy application across all meetings
- Confidence scores for classification quality
- Detailed reasoning for each classification
"""

import json
import sys
import platform
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import argparse
import glob

# Platform detection for LLM strategy
CURRENT_PLATFORM = platform.system()
IS_WINDOWS = CURRENT_PLATFORM == "Windows"
IS_MACOS = CURRENT_PLATFORM == "Darwin"
IS_LINUX = CURRENT_PLATFORM == "Linux"

# Import feedback learning system
try:
    from tools.collaborator_feedback_learning import CollaboratorFeedbackLearning
except ImportError:
    try:
        from collaborator_feedback_learning import CollaboratorFeedbackLearning
    except ImportError:
        CollaboratorFeedbackLearning = None  # Graceful degradation if not available

# Import GPT-5 Meeting Classifier
try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier
except ImportError:
    try:
        from meeting_classifier_gpt5 import GPT5MeetingClassifier
    except ImportError:
        GPT5MeetingClassifier = None

# Import GPT-4.1 Meeting Classifier  
try:
    from tools.meeting_classifier_gpt41 import GPT41MeetingClassifier
except ImportError:
    try:
        from meeting_classifier_gpt41 import GPT41MeetingClassifier
    except ImportError:
        GPT41MeetingClassifier = None

# Import GPT-4o Meeting Classifier
try:
    from tools.meeting_classifier_gpt4o import GPT4oMeetingClassifier
except ImportError:
    try:
        from meeting_classifier_gpt4o import GPT4oMeetingClassifier
    except ImportError:
        GPT4oMeetingClassifier = None

# Import Ollama Meeting Classifier
try:
    from tools.meeting_classifier import OllamaLLMMeetingClassifier
except ImportError:
    try:
        from meeting_classifier import OllamaLLMMeetingClassifier
    except ImportError:
        OllamaLLMMeetingClassifier = None

class CollaboratorDiscoveryTool:
    """
    Advanced collaborator discovery and ranking system based on
    Enterprise Meeting Taxonomy and genuine collaboration evidence.
    """
    
    def __init__(self, calendar_data_file: str = None, output_format: str = "json", preferred_model: str = "auto"):
        self.calendar_data_file = calendar_data_file or "meeting_prep_data/real_calendar_scenarios.json"
        self.output_format = output_format
        self.user_name = "Chin-Yew Lin"  # Default, can be overridden
        self.user_id = "88573e4b-a91e-4334-89c2-a61178320813"  # Chin-Yew Lin's user ID for self-exclusion
        
        # Platform-aware LLM strategy
        # DevBox Windows: GPT-4.1 > GPT-5 > GPT-4o > Keyword (MSAL-based, enterprise data extraction)
        # macOS: Ollama > GPT-4o > Keyword (local LLM, data processing)
        # Linux: Ollama > GPT-4o > Keyword (local LLM, similar to macOS)
        self.meeting_classifier = None
        self.use_llm_classifier = False
        self.llm_classifier_type = "None"
        
        # Auto-select platform-appropriate model if not specified
        if preferred_model == "auto":
            if IS_WINDOWS:
                preferred_model = "gpt-4.1"  # DevBox: Use enterprise MSAL-based LLMs
                print(f"🪟 Windows DevBox detected - Using enterprise LLM strategy")
            elif IS_MACOS:
                preferred_model = "ollama"  # macOS: Use local Ollama for LLM processing
                print(f"🍎 macOS detected - Using local Ollama strategy")
            elif IS_LINUX:
                preferred_model = "ollama"  # Linux: Similar to macOS, prefer local
                print(f"🐧 Linux detected - Using local Ollama strategy")
            else:
                preferred_model = "keyword"  # Unknown platform: fallback to keywords
                print(f"❓ Unknown platform detected - Using keyword fallback")
        
        # Initialize based on platform and preference
        self._initialize_llm_classifier(preferred_model)
        
        # Initialize feedback learning system if available
        self.feedback_system = None
        if CollaboratorFeedbackLearning:
            try:
                self.feedback_system = CollaboratorFeedbackLearning()
            except Exception as e:
                print(f"⚠️ Feedback system not available: {e}")
        
        # Enterprise Meeting Taxonomy weights
        self.taxonomy_weights = {
            # GENUINE COLLABORATION (High weight)
            'one_on_one': 30,
            'organized_by_me': 25,
            'attended_their_working_meetings': 20,
            'small_collaborative_working': 15,
            
            # MODERATE COLLABORATION (Medium weight)
            'small_internal_recurring': 8,
            'planning_decision_meetings': 12,
            
            # INFORMATION CONSUMPTION (Very low weight)
            'informational_briefing': 1,
            'broadcast_webinar': 0.1,
            'training_education': 2,
            
            # EMAIL LIST PENALTY
            'email_list_penalty': -5
        }
        
        # Email list patterns for bulk invitation detection
        self.email_list_patterns = [
            'EventsOnly', '@service.microsoft.com', 'AllHands', 'Everyone',
            'Distribution', 'DL-', 'Team-All', 'Broadcast', 'Announce'
        ]
        
        # Meeting classification keywords
        self.collaboration_keywords = [
            'planning', 'design', 'workshop', 'brainstorm', 'decision',
            'review', 'working', 'sync', 'alignment', 'strategy'
        ]
        
        self.informational_keywords = [
            'update', 'briefing', 'announcement', 'what\'s new', 'research update',
            'training', 'education', 'demo', 'presentation', 'showcase'
        ]
        
        self.broadcast_keywords = [
            'all-hands', 'town hall', 'webinar', 'broadcast', 'announcement',
            'launch', 'kickoff', 'intro'
        ]
    
    def _initialize_llm_classifier(self, preferred_model: str):
        """Initialize LLM classifier based on platform and preference"""
        
        print(f"🔧 Initializing LLM classifier: {preferred_model} on {CURRENT_PLATFORM}")
        
        # Strategy 1: Try preferred model first
        if preferred_model.lower() in ["ollama", "gpt-oss"] and OllamaLLMMeetingClassifier:
            if self._try_ollama_classifier():
                return
        
        if preferred_model.lower() == "gpt-5" and GPT5MeetingClassifier:
            if self._try_gpt5_classifier():
                return
                
        if preferred_model.lower() in ["gpt-4.1", "gpt41"] and GPT41MeetingClassifier:
            if self._try_gpt41_classifier():
                return
                
        if preferred_model.lower() in ["gpt-4o", "gpt4o"] and GPT4oMeetingClassifier:
            if self._try_gpt4o_classifier():
                return
        
        # Strategy 2: Platform-specific fallback cascade
        if IS_WINDOWS:
            # DevBox Windows: MSAL-based LLMs preferred
            self._try_gpt41_classifier() or self._try_gpt5_classifier() or self._try_gpt4o_classifier() or self._try_ollama_classifier()
        else:
            # macOS/Linux: Local LLMs preferred
            self._try_ollama_classifier() or self._try_gpt4o_classifier()
        
        # Final fallback message
        if not self.use_llm_classifier:
            print("ℹ️ Using keyword-based classification (LLM classifiers not available)")
    
    def _try_ollama_classifier(self) -> bool:
        """Try to initialize Ollama classifier"""
        if not OllamaLLMMeetingClassifier:
            return False
        try:
            ollama_classifier = OllamaLLMMeetingClassifier()
            if ollama_classifier.test_model_availability():
                self.meeting_classifier = ollama_classifier
                self.use_llm_classifier = True
                self.llm_classifier_type = "Ollama"
                print("✅ Using Ollama (gpt-oss:20b) for meeting classification")
                return True
            else:
                print("⚠️ Ollama not available (model gpt-oss:20b not found)")
        except Exception as e:
            print(f"⚠️ Ollama initialization failed: {e}")
        return False
    
    def _try_gpt41_classifier(self) -> bool:
        """Try to initialize GPT-4.1 classifier (DevBox MSAL)"""
        if not GPT41MeetingClassifier or not IS_WINDOWS:
            return False
        try:
            gpt41_classifier = GPT41MeetingClassifier()
            if gpt41_classifier.test_model_availability():
                self.meeting_classifier = gpt41_classifier
                self.use_llm_classifier = True
                self.llm_classifier_type = "GPT-4.1"
                print("✅ Using GPT-4.1 (dev-gpt-41-shortco-2025-04-14) for meeting classification [DevBox]")
                return True
            else:
                print("⚠️ GPT-4.1 not available")
        except Exception as e:
            print(f"⚠️ GPT-4.1 initialization failed: {e}")
        return False
    
    def _try_gpt5_classifier(self) -> bool:
        """Try to initialize GPT-5 classifier (DevBox MSAL)"""
        if not GPT5MeetingClassifier:
            return False
        try:
            gpt5_classifier = GPT5MeetingClassifier()
            if gpt5_classifier.test_model_availability():
                self.meeting_classifier = gpt5_classifier
                self.use_llm_classifier = True
                self.llm_classifier_type = "GPT-5"
                print("✅ Using GPT-5 (dev-gpt-5-chat-jj) for meeting classification")
                return True
            else:
                print("⚠️ GPT-5 not available")
        except Exception as e:
            print(f"⚠️ GPT-5 initialization failed: {e}")
        return False
    
    def _try_gpt4o_classifier(self) -> bool:
        """Try to initialize GPT-4o classifier (OpenAI API)"""
        if not GPT4oMeetingClassifier:
            return False
        try:
            gpt4o_classifier = GPT4oMeetingClassifier()
            if gpt4o_classifier.test_model_availability():
                self.meeting_classifier = gpt4o_classifier
                self.use_llm_classifier = True
                self.llm_classifier_type = "GPT-4o"
                print("✅ Using GPT-4o (OpenAI) for meeting classification")
                return True
            else:
                print("⚠️ GPT-4o not available")
        except Exception as e:
            print(f"⚠️ GPT-4o initialization failed: {e}")
        return False
    
    def classify_meeting_type(self, subject: str, attendee_count: int, organizer: str, has_email_list: bool, 
                             description: str = "", attendees: List[str] = None, duration_minutes: int = 60) -> Tuple[str, str]:
        """
        Classify meeting type using GPT-5 LLM (preferred) or keyword-based fallback.
        
        Args:
            subject: Meeting title/subject
            attendee_count: Number of attendees
            organizer: Meeting organizer name
            has_email_list: Whether meeting has distribution list
            description: Meeting description/body (optional, for LLM)
            attendees: List of attendee names (optional, for LLM)
            duration_minutes: Meeting duration in minutes (optional, for LLM)
            
        Returns: (meeting_type, taxonomy_category)
        """
        
        # Try LLM classification first
        if self.use_llm_classifier and self.meeting_classifier:
            try:
                # Use the appropriate method based on classifier type
                if self.llm_classifier_type == "Ollama":
                    result = self.meeting_classifier.classify_meeting_with_llm(
                        subject=subject,
                        description=description,
                        attendees=attendees if attendees else [],
                        duration_minutes=duration_minutes
                    )
                else:
                    # For GPT-5, GPT-4.1, GPT-4o classifiers
                    result = self.meeting_classifier.classify_meeting(
                        subject=subject,
                        description=description,
                        attendees=attendees if attendees else [],
                        duration_minutes=duration_minutes
                    )
                
                # Map LLM classification to our meeting types
                llm_type = result.get('specific_type', '')
                llm_category = result.get('primary_category', '')
                
                # Map to internal meeting type codes
                meeting_type = self._map_llm_to_meeting_type(llm_type, attendee_count, has_email_list)
                taxonomy_category = f"{llm_category} - {llm_type}"
                
                return meeting_type, taxonomy_category
                
            except Exception as e:
                # Fall through to keyword-based classification
                print(f"⚠️ LLM classification failed for '{subject}': {e}")
        
        # Fallback: Keyword-based classification
        return self._keyword_based_classification(subject, attendee_count, has_email_list)
    
    def _map_llm_to_meeting_type(self, llm_type: str, attendee_count: int, has_email_list: bool) -> str:
        """Map LLM classification to internal meeting type codes"""
        
        llm_lower = llm_type.lower()
        
        # Direct mappings
        if 'one-on-one' in llm_lower:
            return 'one_on_one'
        elif 'all-hands' in llm_lower or 'town hall' in llm_lower:
            return 'broadcast_webinar'
        elif 'webinar' in llm_lower or 'broadcast' in llm_lower:
            return 'broadcast_webinar'
        elif 'training' in llm_lower or 'onboarding' in llm_lower:
            return 'training_education'
        elif 'briefing' in llm_lower or 'announcement' in llm_lower:
            return 'informational_briefing'
        elif 'brainstorm' in llm_lower or 'workshop' in llm_lower or 'design' in llm_lower:
            return 'small_collaborative_working'
        elif 'strategic planning' in llm_lower or 'decision' in llm_lower or 'problem-solving' in llm_lower:
            return 'planning_decision_meetings'
        elif 'standup' in llm_lower or 'status update' in llm_lower or 'check-in' in llm_lower:
            return 'small_internal_recurring'
        elif 'retrospective' in llm_lower or 'review' in llm_lower:
            return 'small_internal_recurring'
        
        # Fallback based on attendee count
        if attendee_count == 2:
            return 'one_on_one'
        elif attendee_count > 50:
            return 'broadcast_webinar'
        elif attendee_count <= 10:
            return 'small_collaborative_working'
        else:
            return 'informational_briefing'
    
    def _keyword_based_classification(self, subject: str, attendee_count: int, has_email_list: bool) -> Tuple[str, str]:
        """Original keyword-based classification (fallback when LLM unavailable)"""
        
        subject_lower = subject.lower()
        
        # 1. Broadcast Meetings (Informational & Broadcast category)
        if attendee_count > 50 or any(keyword in subject_lower for keyword in self.broadcast_keywords):
            return 'broadcast_webinar', 'Informational & Broadcast - Webinars and Broadcasts'
        
        # 2. Informational Briefings
        if (any(keyword in subject_lower for keyword in self.informational_keywords) or has_email_list):
            return 'informational_briefing', 'Informational & Broadcast - Informational Briefings'
        
        # 3. Training/Education
        if 'research' in subject_lower or 'training' in subject_lower or 'education' in subject_lower:
            return 'training_education', 'Informational & Broadcast - Training & Education Sessions'
        
        # 4. One-on-One (highest collaboration value)
        if attendee_count == 2:
            return 'one_on_one', 'Internal Recurring - One-on-One Meetings'
        
        # 5. Strategic Planning & Decision Meetings
        if any(keyword in subject_lower for keyword in self.collaboration_keywords):
            if attendee_count <= 10:
                return 'small_collaborative_working', 'Strategic Planning & Decision - Planning/Workshop Sessions'
            else:
                return 'planning_decision_meetings', 'Strategic Planning & Decision - Planning Sessions'
        
        # 6. Internal Recurring (Status Updates)
        if attendee_count <= 10:
            return 'small_internal_recurring', 'Internal Recurring - Team Status Update Meetings'
        else:
            return 'informational_briefing', 'Internal Recurring - Progress Review Meetings'
    
    def calculate_temporal_multiplier(self, meeting_date: datetime, current_date: datetime, 
                                      is_important: bool = False) -> float:
        """
        Calculate temporal recency multiplier for a meeting.
        
        Recent important meetings get higher multipliers than old frequent meetings.
        
        Args:
            meeting_date: When the meeting occurred
            current_date: Current date/time for reference
            is_important: Whether this is an important meeting type (1:1, organized, strategic)
            
        Returns:
            Multiplier to apply to meeting score (0.5 to 2.0)
        """
        days_ago = (current_date - meeting_date).days
        
        # Time windows with multipliers
        if days_ago <= 7:  # Last week
            base_multiplier = 2.0  # HOT - just met with them
        elif days_ago <= 30:  # Last month
            base_multiplier = 1.5  # RECENT - actively collaborating
        elif days_ago <= 90:  # Last quarter
            base_multiplier = 1.2  # CURRENT - regular collaboration
        elif days_ago <= 180:  # Last 6 months
            base_multiplier = 0.8  # MEDIUM - occasional collaboration
        else:  # > 6 months
            base_multiplier = 0.5  # DECAY - historical collaboration
        
        # Boost important meeting types
        if is_important:
            # Important meetings retain value longer
            if days_ago <= 30:
                base_multiplier *= 1.3  # Recent important meetings are critical
            elif days_ago <= 90:
                base_multiplier *= 1.1  # Still valuable in last quarter
        
        return base_multiplier
    
    def is_important_meeting(self, meeting_type: str, is_organized_by_me: bool) -> bool:
        """
        Determine if a meeting type is considered 'important' for temporal weighting.
        
        Important meetings:
        - One-on-one meetings (direct collaboration)
        - Meetings I organized (my initiative)
        - Strategic planning & decision meetings
        - Small working sessions
        
        Args:
            meeting_type: Classification from classify_meeting_type
            is_organized_by_me: Whether I organized this meeting
            
        Returns:
            True if meeting is important, False otherwise
        """
        important_types = {
            'one_on_one',
            'organized_by_me',
            'small_collaborative_working',
            'planning_decision_meetings'
        }
        
        return meeting_type in important_types or is_organized_by_me
    
    def load_graph_api_data(self) -> Optional[Dict]:
        """
        Load Microsoft Graph API collaboration data from manual_auth_graph_extractor.py output
        Returns the most recent graph_collaboration_analysis_*.json file
        """
        try:
            # Find the most recent graph collaboration analysis file
            pattern = "data/evaluation_results/graph_collaboration_analysis_*.json"
            files = glob.glob(pattern)
            
            if not files:
                print("ℹ️ No Graph API data found - skipping Graph integration")
                return None
            
            # Get the most recent file
            latest_file = max(files, key=lambda x: Path(x).stat().st_mtime)
            print(f"📊 Loading Graph API data from: {Path(latest_file).name}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            
            return graph_data
            
        except Exception as e:
            print(f"⚠️ Could not load Graph API data: {e}")
            return None
    
    def enrich_with_graph_data(self, collaboration_scores: Dict, graph_data: Dict) -> Dict:
        """
        Enrich calendar-based collaboration scores with Microsoft Graph API People rankings
        and document sharing patterns
        """
        if not graph_data or 'responses' not in graph_data:
            return collaboration_scores
        
        # Extract People API rankings
        people_response = graph_data['responses'].get('People API - Microsoft ML Collaboration Rankings', {})
        people_list = people_response.get('value', [])
        
        if not people_list:
            print("ℹ️ No People API rankings found in Graph data")
        else:
            print(f"✅ Enriching with {len(people_list)} Graph API People rankings")
        
        # Extract document sharing patterns
        shared_items_response = graph_data['responses'].get('Recent Collaboration Items', {})
        shared_items = shared_items_response.get('value', [])
        
        # Count document sharing by person
        document_sharing = {}
        if shared_items:
            print(f"✅ Analyzing {len(shared_items)} shared document collaborations")
            for item in shared_items:
                if isinstance(item, dict):
                    shared_by_info = item.get('lastShared', {}).get('sharedBy', {})
                    shared_by = shared_by_info.get('displayName', '')
                    email = shared_by_info.get('address', '')
                    
                    if shared_by:
                        if shared_by not in document_sharing:
                            document_sharing[shared_by] = {'count': 0, 'email': email}
                        document_sharing[shared_by]['count'] += 1
        
        # Create email-to-rank mapping
        email_to_rank = {}
        for idx, person in enumerate(people_list, 1):
            email = person.get('scoredEmailAddresses', [{}])[0].get('address', '').lower()
            if not email:
                email = person.get('userPrincipalName', '').lower()
            if email:
                email_to_rank[email] = {
                    'rank': idx,
                    'display_name': person.get('displayName', ''),
                    'job_title': person.get('jobTitle', ''),
                    'relevance_score': person.get('relevanceScore', 0)
                }
        
        # Enrich collaboration scores with Graph rankings and document sharing
        for person_name, data in collaboration_scores.items():
            # Try to match by email domain pattern (name@microsoft.com)
            email_candidates = [
                f"{person_name.lower().replace(' ', '')}@microsoft.com",
                f"{person_name.lower().replace(' ', '.')}@microsoft.com",
                person_name.lower() if '@' in person_name else None
            ]
            
            for email in email_candidates:
                if email and email in email_to_rank:
                    graph_info = email_to_rank[email]
                    data['graph_api_rank'] = graph_info['rank']
                    data['graph_api_relevance'] = graph_info['relevance_score']
                    data['graph_api_matched'] = True
                    data['verified_name'] = graph_info['display_name']
                    data['job_title'] = graph_info['job_title']
                    
                    # Boost score for high Graph API rankings (top 10)
                    if graph_info['rank'] <= 10:
                        data['graph_api_boost'] = 20 - graph_info['rank']  # Rank 1 gets +19, rank 10 gets +10
                    break
            
            # Add document sharing data
            if person_name in document_sharing:
                doc_count = document_sharing[person_name]['count']
                data['shared_documents'] = doc_count
                data['document_collaboration_score'] = doc_count * 5  # 5 points per shared document
                print(f"  📄 {person_name}: {doc_count} shared documents (+{doc_count * 5} points)")
        
        return collaboration_scores
    
    def load_teams_chat_data(self) -> Optional[Dict]:
        """
        Load Teams chat collaboration data from teams_chat_api.py output.
        Returns the most recent teams_chat_analysis_*.json file.
        """
        try:
            # Find the most recent chat analysis file
            pattern = "data/evaluation_results/teams_chat_analysis_*.json"
            files = glob.glob(pattern)
            
            if not files:
                print("ℹ️ No Teams chat data found - skipping chat integration")
                print("   💡 Run: python tools/teams_chat_api.py to collect chat data")
                return None
            
            # Get the most recent file
            latest_file = max(files, key=lambda x: Path(x).stat().st_mtime)
            print(f"💬 Loading Teams chat data from: {Path(latest_file).name}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
            
            return chat_data
            
        except Exception as e:
            print(f"⚠️ Could not load Teams chat data: {e}")
            return None
    
    def enrich_with_chat_data(self, collaboration_scores: Dict, chat_data: Dict) -> Dict:
        """
        Enrich collaboration scores with Teams chat data.
        
        Adds chat collaboration metrics:
        - Chat frequency (number of chats with person)
        - Chat recency (days since last chat)
        - Chat type (1:1 vs group chats)
        - Ad hoc collaboration detection (chat-only relationships)
        """
        if not chat_data or 'collaborators' not in chat_data:
            return collaboration_scores
        
        chat_collaborators = chat_data['collaborators']
        
        if not chat_collaborators:
            print("ℹ️ No chat collaborators found in data")
        else:
            print(f"💬 Enriching with {len(chat_collaborators)} Teams chat collaborators")
        
        # Track chat-only collaborators (people you chat with but don't meet)
        chat_only_count = 0
        
        for person_name, chat_metrics in chat_collaborators.items():
            # Find matching person in collaboration scores (handle name variations)
            matched_person = None
            for cal_person in collaboration_scores.keys():
                # Exact match or partial match
                if person_name.lower() == cal_person.lower():
                    matched_person = cal_person
                    break
                # Check if one name is contained in the other
                elif person_name.lower() in cal_person.lower() or cal_person.lower() in person_name.lower():
                    matched_person = cal_person
                    break
            
            if matched_person:
                # Existing calendar collaborator - enrich with chat data
                data = collaboration_scores[matched_person]
                data['chat_count'] = chat_metrics['chat_count']
                data['chat_message_count'] = chat_metrics['message_count']
                data['last_chat_date'] = chat_metrics['last_chat_date']
                data['days_since_last_chat'] = chat_metrics['days_since_last_chat']
                data['chat_recency_score'] = chat_metrics['recency_score']
                data['is_recent_chat'] = chat_metrics['is_recent']
                data['is_frequent_chat'] = chat_metrics['is_frequent']
                data['chat_type'] = chat_metrics['chat_type']
                
                # Calculate chat collaboration score
                # Weight: 1:1 chats (2x), group chats (1x), recent chats (1.5x boost)
                chat_weight = 2.0 if chat_metrics['chat_type'] == 'oneOnOne' else 1.0
                recency_boost = 1.5 if chat_metrics['is_recent'] else 1.0
                chat_score = chat_metrics['chat_count'] * chat_weight * chat_metrics['recency_score'] * recency_boost
                data['chat_collaboration_score'] = chat_score
                
                print(f"  💬 {matched_person}: {chat_metrics['chat_count']} chats, "
                      f"recency={chat_metrics['recency_score']:.1f}x (+{chat_score:.1f} points)")
            else:
                # Chat-only collaborator - NOT in calendar data
                # Create new entry for this person
                collaboration_scores[person_name] = {
                    'total_meetings': 0,
                    'genuine_collaboration_meetings': 0,
                    'informational_meetings': 0,
                    'broadcast_meetings': 0,
                    'one_on_one_meetings': 0,
                    'small_working_meetings': 0,
                    'organized_by_me': 0,
                    'i_attended_their_meetings': 0,
                    'email_list_meetings': 0,
                    'meeting_details': [],
                    'time_periods': set(),
                    'taxonomy_classifications': [],
                    'collaboration_evidence': ['Teams chat collaboration (no calendar meetings)'],
                    'information_consumption_evidence': [],
                    'collaboration_score': 0,
                    'chat_only_collaborator': True,  # Flag for ad hoc collaboration
                    'chat_count': chat_metrics['chat_count'],
                    'chat_message_count': chat_metrics['message_count'],
                    'last_chat_date': chat_metrics['last_chat_date'],
                    'days_since_last_chat': chat_metrics['days_since_last_chat'],
                    'chat_recency_score': chat_metrics['recency_score'],
                    'is_recent_chat': chat_metrics['is_recent'],
                    'is_frequent_chat': chat_metrics['is_frequent'],
                    'chat_type': chat_metrics['chat_type'],
                }
                
                # Calculate chat-only collaboration score
                chat_weight = 2.0 if chat_metrics['chat_type'] == 'oneOnOne' else 1.0
                recency_boost = 1.5 if chat_metrics['is_recent'] else 1.0
                chat_score = chat_metrics['chat_count'] * chat_weight * chat_metrics['recency_score'] * recency_boost
                collaboration_scores[person_name]['chat_collaboration_score'] = chat_score
                collaboration_scores[person_name]['collaboration_score'] = chat_score * 0.7  # 70% weight for chat-only
                
                chat_only_count += 1
                print(f"  💬 {person_name}: Chat-only collaborator ({chat_metrics['chat_count']} chats, "
                      f"type={chat_metrics['chat_type']}, +{chat_score:.1f} points)")
        
        if chat_only_count > 0:
            print(f"✨ Discovered {chat_only_count} ad hoc chat-only collaborators (no calendar meetings)")
        
        return collaboration_scores
    
    def load_document_collaboration_data(self) -> Optional[Dict]:
        """
        Load document collaboration data from document_collaboration_api.py output.
        Returns the most recent document_collaboration_analysis_*.json file.
        """
        try:
            # Find the most recent document collaboration analysis file
            pattern = "data/evaluation_results/document_collaboration_analysis_*.json"
            files = glob.glob(pattern)
            
            if not files:
                print("ℹ️ No document collaboration data found - skipping document integration")
                print("   💡 Run: python tools/document_collaboration_api.py to collect document data")
                return None
            
            # Get the most recent file
            latest_file = max(files, key=lambda x: Path(x).stat().st_mtime)
            print(f"📄 Loading document collaboration data from: {Path(latest_file).name}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                doc_data = json.load(f)
            
            return doc_data
            
        except Exception as e:
            print(f"⚠️ Could not load document collaboration data: {e}")
            return None
    
    def enrich_with_document_data(self, collaboration_scores: Dict, doc_data: Dict) -> Dict:
        """
        Enrich collaboration scores with document sharing data from OneDrive and Teams chat attachments.
        
        Adds document collaboration metrics:
        - OneDrive direct shares (1:1)
        - OneDrive small group shares (<5 people)
        - Teams chat direct attachments (1:1)
        - Teams chat group attachments (<5 people)
        - Sharing frequency (days of sharing activity)
        - Sharing recency (last share date)
        - Temporal bonuses (recent shares weighted higher)
        """
        if not doc_data or 'collaborators' not in doc_data:
            return collaboration_scores
        
        # Convert list to dict for easier lookup
        doc_collaborators_list = doc_data['collaborators']
        doc_collaborators = {collab['name']: collab for collab in doc_collaborators_list}
        
        if not doc_collaborators:
            print("ℹ️ No document collaborators found in data")
        else:
            print(f"📄 Enriching with {len(doc_collaborators)} document sharing collaborators")
        
        # Track document-only collaborators (people you share docs with but don't meet/chat)
        doc_only_count = 0
        
        for person_name, doc_metrics in doc_collaborators.items():
            # Find matching person in collaboration scores (handle name variations)
            matched_person = None
            for cal_person in collaboration_scores.keys():
                # Exact match or partial match
                if person_name.lower() == cal_person.lower():
                    matched_person = cal_person
                    break
                # Check if one name is contained in the other
                elif person_name.lower() in cal_person.lower() or cal_person.lower() in person_name.lower():
                    matched_person = cal_person
                    break
            
            if matched_person:
                # Existing collaborator - enrich with document data
                data = collaboration_scores[matched_person]
                data['onedrive_direct_shares'] = doc_metrics.get('direct_shares', 0)
                data['onedrive_group_shares'] = doc_metrics.get('small_group_shares', 0)
                data['teams_direct_attachments'] = doc_metrics.get('chat_direct', 0)
                data['teams_group_attachments'] = doc_metrics.get('chat_group', 0)
                total_shares = (doc_metrics.get('direct_shares', 0) + doc_metrics.get('small_group_shares', 0) + 
                              doc_metrics.get('chat_direct', 0) + doc_metrics.get('chat_group', 0))
                data['total_document_shares'] = total_shares
                data['sharing_days'] = doc_metrics.get('sharing_days', 0)
                data['last_share_date'] = doc_metrics.get('last_share')
                data['document_recency_label'] = doc_metrics.get('recency_label', 'N/A')
                
                # Use the calculated collaboration_score from document API (includes temporal bonuses)
                doc_collab_score = doc_metrics.get('collaboration_score', 0)
                data['document_collaboration_score'] = doc_collab_score
                
                print(f"  📄 {matched_person}: OneDrive({doc_metrics.get('direct_shares', 0)}/{doc_metrics.get('small_group_shares', 0)}), "
                      f"Chat({doc_metrics.get('chat_direct', 0)}/{doc_metrics.get('chat_group', 0)}), "
                      f"{doc_metrics.get('sharing_days', 0)} days, last={doc_metrics.get('recency_label', 'N/A')} "
                      f"(+{doc_collab_score} points)")
            else:
                # Document-only collaborator - NOT in calendar or chat data
                # Create new entry for this person
                collaboration_scores[person_name] = {
                    'total_meetings': 0,
                    'genuine_collaboration_meetings': 0,
                    'informational_meetings': 0,
                    'broadcast_meetings': 0,
                    'one_on_one_meetings': 0,
                    'small_working_meetings': 0,
                    'organized_by_me': 0,
                    'i_attended_their_meetings': 0,
                    'email_list_meetings': 0,
                    'meeting_details': [],
                    'time_periods': set(),
                    'taxonomy_classifications': [],
                    'collaboration_evidence': ['Document sharing collaboration (no calendar meetings or chats)'],
                    'information_consumption_evidence': [],
                    'collaboration_score': 0,
                    'document_only_collaborator': True,  # Flag for document-only collaboration
                    'onedrive_direct_shares': doc_metrics.get('direct_shares', 0),
                    'onedrive_group_shares': doc_metrics.get('small_group_shares', 0),
                    'teams_direct_attachments': doc_metrics.get('chat_direct', 0),
                    'teams_group_attachments': doc_metrics.get('chat_group', 0),
                    'total_document_shares': (doc_metrics.get('direct_shares', 0) + doc_metrics.get('small_group_shares', 0) + 
                                            doc_metrics.get('chat_direct', 0) + doc_metrics.get('chat_group', 0)),
                    'sharing_days': doc_metrics.get('sharing_days', 0),
                    'last_share_date': doc_metrics.get('last_share'),
                    'document_recency_label': doc_metrics.get('recency_label', 'N/A'),
                }
                
                # Use calculated score with temporal bonuses
                doc_collab_score = doc_metrics.get('collaboration_score', 0)
                collaboration_scores[person_name]['document_collaboration_score'] = doc_collab_score
                collaboration_scores[person_name]['collaboration_score'] = doc_collab_score * 0.6  # 60% weight for doc-only
                
                doc_only_count += 1
                print(f"  📄 {person_name}: Document-only collaborator (OneDrive: {doc_metrics.get('direct_shares', 0)}/{doc_metrics.get('small_group_shares', 0)}, "
                      f"Chat: {doc_metrics.get('chat_direct', 0)}/{doc_metrics.get('chat_group', 0)}, +{doc_collab_score} points)")
        
        if doc_only_count > 0:
            print(f"✨ Discovered {doc_only_count} document-only collaborators (no calendar meetings or chats)")
        
        return collaboration_scores
    
    def analyze_collaboration_patterns(self, calendar_data: List[Dict]) -> Dict[str, Dict]:
        """
        Analyze calendar data to identify collaboration patterns
        """
        collaboration_scores = defaultdict(lambda: {
            'total_meetings': 0,
            'genuine_collaboration_meetings': 0,
            'informational_meetings': 0,
            'broadcast_meetings': 0,
            'one_on_one_meetings': 0,
            'small_working_meetings': 0,
            'organized_by_me': 0,
            'i_attended_their_meetings': 0,
            'email_list_meetings': 0,
            'meeting_details': [],
            'time_periods': set(),
            'taxonomy_classifications': [],
            'collaboration_evidence': [],
            'information_consumption_evidence': [],
            'collaboration_score': 0  # Initialize for temporal scoring
        })
        
        current_date = datetime.now()
        
        for event in calendar_data:
            attendees = event['context'].get('attendees', [])
            attendee_count = len(attendees)
            organizer = event['context'].get('organizer', 'Unknown')
            is_my_meeting = organizer == self.user_name
            start_time = event['context'].get('start_time', '')
            end_time = event['context'].get('end_time', '')
            subject = event['context'].get('subject', '').lower()
            description = event['context'].get('bodyPreview', '')
            
            # Calculate duration in minutes
            duration_minutes = 60  # default
            try:
                if start_time and end_time:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
            except:
                pass
            
            # Parse meeting date
            try:
                if start_time:
                    meeting_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                else:
                    meeting_date = current_date - timedelta(days=30)
            except:
                meeting_date = current_date - timedelta(days=30)
            
            time_period = start_time[:7] if start_time else 'unknown'
            
            # Check for email list invitations
            has_email_list = any(
                any(pattern in attendee for pattern in self.email_list_patterns)
                for attendee in attendees
            )
            
            for attendee in attendees:
                if attendee != self.user_name:
                    data = collaboration_scores[attendee]
                    
                    # Basic tracking
                    data['total_meetings'] += 1
                    data['time_periods'].add(time_period)
                    
                    # Classify meeting type with GPT-5 (if available) or keywords
                    meeting_type, taxonomy_category = self.classify_meeting_type(
                        subject=subject,
                        attendee_count=attendee_count,
                        organizer=organizer,
                        has_email_list=has_email_list,
                        description=description,
                        attendees=attendees,
                        duration_minutes=duration_minutes
                    )
                    data['taxonomy_classifications'].append(taxonomy_category)
                    
                    # Determine if this is an important meeting
                    is_important = self.is_important_meeting(meeting_type, is_my_meeting)
                    
                    # Calculate temporal multiplier
                    temporal_multiplier = self.calculate_temporal_multiplier(
                        meeting_date, current_date, is_important
                    )
                    
                    # Track email list meetings
                    if has_email_list:
                        data['email_list_meetings'] += 1
                    
                    # Calculate scores and evidence
                    base_meeting_score = 0
                    collaboration_evidence = []
                    information_evidence = []
                    
                    if meeting_type == 'one_on_one':
                        data['one_on_one_meetings'] += 1
                        data['genuine_collaboration_meetings'] += 1
                        base_meeting_score = self.taxonomy_weights['one_on_one']
                        collaboration_evidence.append('1:1 meeting - direct collaboration')
                        
                    elif meeting_type == 'small_collaborative_working':
                        data['small_working_meetings'] += 1
                        data['genuine_collaboration_meetings'] += 1
                        base_meeting_score = self.taxonomy_weights['small_collaborative_working']
                        collaboration_evidence.append('Small collaborative working session')
                        
                    elif meeting_type == 'planning_decision_meetings':
                        data['genuine_collaboration_meetings'] += 1
                        base_meeting_score = self.taxonomy_weights['planning_decision_meetings']
                        collaboration_evidence.append('Planning/decision meeting participation')
                        
                    elif meeting_type == 'small_internal_recurring':
                        base_meeting_score = self.taxonomy_weights['small_internal_recurring']
                        collaboration_evidence.append('Small internal recurring meeting')
                        
                    elif meeting_type == 'informational_briefing':
                        data['informational_meetings'] += 1
                        base_meeting_score = self.taxonomy_weights['informational_briefing']
                        information_evidence.append('Informational briefing attendance')
                        
                    elif meeting_type == 'broadcast_webinar':
                        data['broadcast_meetings'] += 1
                        base_meeting_score = self.taxonomy_weights['broadcast_webinar']
                        information_evidence.append('Broadcast/webinar attendance')
                        
                    elif meeting_type == 'training_education':
                        data['informational_meetings'] += 1
                        base_meeting_score = self.taxonomy_weights['training_education']
                        information_evidence.append('Training/education session attendance')
                    
                    # Apply temporal multiplier to base score
                    temporal_score = base_meeting_score * temporal_multiplier
                    
                    # Apply email list penalty
                    if has_email_list:
                        temporal_score += self.taxonomy_weights['email_list_penalty']
                        information_evidence.append('Email list invitation (bulk invite)')
                    
                    # Apply the temporal-weighted score
                    data['collaboration_score'] += temporal_score
                    
                    # Track recency metadata
                    if 'recency_data' not in data:
                        data['recency_data'] = {
                            'last_7_days': 0,
                            'last_30_days': 0,
                            'last_90_days': 0,
                            'most_recent_meeting': None,
                            'recent_important_meetings': 0
                        }
                    
                    days_ago = (current_date - meeting_date).days
                    if days_ago <= 7:
                        data['recency_data']['last_7_days'] += 1
                    if days_ago <= 30:
                        data['recency_data']['last_30_days'] += 1
                    if days_ago <= 90:
                        data['recency_data']['last_90_days'] += 1
                    
                    if is_important and days_ago <= 30:
                        data['recency_data']['recent_important_meetings'] += 1
                    
                    # Track most recent meeting
                    if data['recency_data']['most_recent_meeting'] is None or meeting_date > data['recency_data']['most_recent_meeting']:
                        data['recency_data']['most_recent_meeting'] = meeting_date
                    
                    # Organization tracking
                    if is_my_meeting:
                        data['organized_by_me'] += 1
                        data['genuine_collaboration_meetings'] += 1
                        org_score = self.taxonomy_weights['organized_by_me']
                        base_meeting_score += org_score
                        collaboration_evidence.append('Meeting you organized together')
                    
                    if organizer == attendee and meeting_type in ['small_collaborative_working', 'planning_decision_meetings']:
                        data['i_attended_their_meetings'] += 1
                        data['genuine_collaboration_meetings'] += 1
                        attend_score = self.taxonomy_weights['attended_their_working_meetings']
                        base_meeting_score += attend_score
                        collaboration_evidence.append('Attended their working meeting')
                    elif organizer == attendee:
                        information_evidence.append('Attended their informational meeting')
                    
                    # Store evidence
                    data['collaboration_evidence'].extend(collaboration_evidence)
                    data['information_consumption_evidence'].extend(information_evidence)
                    
                    # Meeting details
                    meeting_detail = {
                        'date': meeting_date.isoformat(),
                        'size': attendee_count,
                        'subject': subject,
                        'organizer': organizer,
                        'meeting_type': meeting_type,
                        'taxonomy_category': taxonomy_category,
                        'has_email_list': has_email_list,
                        'base_score': base_meeting_score,
                        'collaboration_evidence': collaboration_evidence,
                        'information_evidence': information_evidence
                    }
                    data['meeting_details'].append(meeting_detail)
        
        return collaboration_scores
    
    def rank_collaborators(self, collaboration_scores: Dict[str, Dict]) -> List[Dict]:
        """
        Rank collaborators from most important to least important
        ENHANCED v8.1: Support multi-source collaborators (calendar, chat, documents, Graph API)
        """
        genuine_collaborators = []
        debug_filtered = {'too_few_meetings': 0, 'no_evidence': 0, 'system_account': 0, 'low_score': 0, 'low_confidence': 0, 'self_user': 0}
        
        for person, data in collaboration_scores.items():
            # ENHANCED v8.1: Support collaborators from any source (not just calendar)
            # Calendar requirement: >= 2 meetings
            # OR Chat-only collaborator (chat_only_collaborator=True)
            # OR Significant chat activity (>= 2 chats) - NEW v8.2
            # OR Document-only collaborator (document_only_collaborator=True)
            # OR Graph API verified collaborator
            has_calendar_evidence = data['total_meetings'] >= 2
            has_chat_evidence = data.get('chat_only_collaborator', False)
            has_significant_chat_evidence = data.get('chat_count', 0) >= 2  # NEW v8.2
            has_document_evidence = data.get('document_only_collaborator', False)
            has_graph_api_evidence = data.get('graph_api_matched', False) and data.get('graph_api_rank', 999) <= 10
            
            if not (has_calendar_evidence or has_chat_evidence or has_significant_chat_evidence or has_document_evidence or has_graph_api_evidence):
                debug_filtered['too_few_meetings'] += 1
                continue
            
            if has_calendar_evidence or has_chat_evidence or has_significant_chat_evidence or has_document_evidence or has_graph_api_evidence:
                
                # Calculate collaboration metrics (handle zero meetings case)
                total_meetings = data['total_meetings']
                if total_meetings > 0:
                    genuine_ratio = data['genuine_collaboration_meetings'] / total_meetings
                    informational_ratio = data['informational_meetings'] / total_meetings
                    email_list_ratio = data['email_list_meetings'] / total_meetings
                else:
                    # Multi-source collaborator with no calendar meetings
                    genuine_ratio = 1.0  # Assume genuine if from chat/documents/Graph API
                    informational_ratio = 0.0
                    email_list_ratio = 0.0
                
                # Enhanced evidence requirements (UPDATED v8.1: Multi-source support)
                chat_only_flag = data.get('chat_only_collaborator', False)
                doc_only_flag = data.get('document_only_collaborator', False)
                graph_api_verified = data.get('graph_api_matched', False) and data.get('graph_api_rank', 999) <= 10
                has_significant_chat = data.get('chat_count', 0) >= 2  # NEW: 2+ chats counts as evidence
                
                has_genuine_collaboration = (
                    data['one_on_one_meetings'] > 0 or
                    data['organized_by_me'] > 0 or
                    data['small_working_meetings'] > 0 or
                    data['genuine_collaboration_meetings'] >= 2 or
                    # NEW: Accept chat-only/document-only/Graph API evidence
                    chat_only_flag or
                    doc_only_flag or
                    graph_api_verified or
                    has_significant_chat  # NEW: Significant chat activity counts
                )
                
                # Self-exclusion: Skip the primary user
                if person == self.user_name or person == "Chin-Yew Lin":
                    debug_filtered['self_user'] = debug_filtered.get('self_user', 0) + 1
                    continue
                
                # System account detection
                system_indicators = [
                    'rob', 'fte', 'extended', 'community', 'team', 'group',
                    'holiday', 'event', 'auto', 'system', 'notification',
                    'bot', 'service', 'admin', 'learning', 'events',
                    'conf room', 'conference room', 'room '  # Filter out conference rooms
                ]
                
                person_lower = person.lower()
                is_system_account = any(indicator in person_lower for indicator in system_indicators)
                
                # Calculate final score (UPDATED v8.1: Include chat/document collaboration scores)
                final_score = sum(detail['base_score'] for detail in data['meeting_details'])
                
                # BUGFIX v8.1: Chat-only and document-only collaborators have no meeting_details
                # Use their collaboration_score instead
                if final_score == 0 and (chat_only_flag or doc_only_flag):
                    final_score = data.get('collaboration_score', 0)
                
                # Add Graph API boost if available
                graph_api_boost = data.get('graph_api_boost', 0)
                final_score += graph_api_boost
                
                # Add document collaboration score
                doc_collab_score = data.get('document_collaboration_score', 0)
                final_score += doc_collab_score
                
                # Calculate confidence (Haidong Zhang case study: multi-source validation)
                confidence_factors = 0
                if data['one_on_one_meetings'] > 0:
                    confidence_factors += 0.4  # 1:1s are strong collaboration signal
                if data['organized_by_me'] > 0:
                    confidence_factors += 0.4  # Organized meetings show active collaboration
                if data['small_working_meetings'] > 0:
                    confidence_factors += 0.3  # Small working sessions are genuine collaboration
                if genuine_ratio > 0.5:
                    confidence_factors += 0.2  # Majority genuine meetings
                if email_list_ratio < 0.3:
                    confidence_factors += 0.2  # Low bulk invitation rate
                
                # HAIDONG ZHANG LESSON: Multi-source validation significantly boosts confidence
                if data.get('graph_api_matched'):
                    confidence_factors += 0.3  # Graph API People ranking confirms relationship
                    # Extra boost for top-ranked Graph API collaborators (ranks 1-5)
                    if data.get('graph_api_rank', 999) <= 5:
                        confidence_factors += 0.2  # Microsoft's ML model strongly confirms this person
                
                # Document sharing confirms non-meeting collaboration (ENHANCED v8.0)
                if data.get('total_document_shares', 0) > 0 or data.get('shared_documents', 0) > 0:
                    confidence_factors += 0.15  # Documents show working relationship
                    # Extra boost for frequent document sharing
                    if data.get('total_document_shares', 0) >= 3:
                        confidence_factors += 0.1  # Regular document collaboration
                
                # NEW: Recent important meetings boost confidence
                recency_data = data.get('recency_data', {})
                if recency_data.get('recent_important_meetings', 0) > 0:
                    confidence_factors += 0.3  # Recent important collaboration is strong signal
                
                confidence = min(confidence_factors, 1.0)
                
                # Importance score (UPDATED v6.0: Added temporal recency weighting)
                # Reduced collaboration activities from 30% to 25% to make room for temporal
                collaboration_activity_score = final_score * 0.25
                
                # Quality of interaction (genuine vs informational) - reduced from 25% to 20%
                interaction_quality_score = genuine_ratio * 100 * 0.20
                
                # Confidence level - maintained at 20%
                confidence_score = confidence * 50 * 0.20
                
                # Graph API ranking weight (HAIDONG ZHANG LESSON) - maintained at 15%
                graph_api_weight = 0
                if data.get('graph_api_rank'):
                    # Top 3 get significant boost, diminishing returns after that
                    rank = data['graph_api_rank']
                    if rank <= 3:
                        graph_api_weight = (4 - rank) * 20  # Rank 1: 60, Rank 2: 40, Rank 3: 20
                    elif rank <= 10:
                        graph_api_weight = (11 - rank) * 5   # Rank 4-10: 35 to 5
                
                # NEW: Temporal recency weight - 15% of total score
                temporal_recency_score = 0
                if recency_data:
                    # Recent meetings contribute more to recency score
                    last_7_score = recency_data.get('last_7_days', 0) * 15    # HOT - 15 points per meeting
                    last_30_score = recency_data.get('last_30_days', 0) * 8   # RECENT - 8 points per meeting
                    last_90_score = recency_data.get('last_90_days', 0) * 4   # CURRENT - 4 points per meeting
                    
                    # Bonus for recent important meetings (1:1s, organized, strategic)
                    important_bonus = recency_data.get('recent_important_meetings', 0) * 10
                    
                    temporal_recency_score = (last_7_score + last_30_score + last_90_score + important_bonus) * 0.15
                
                # Document collaboration weight - ENHANCED v8.0: Use comprehensive document score
                # This includes OneDrive + Teams chat attachments with temporal analysis
                document_score = data.get('document_collaboration_score', 0)
                
                # Chat collaboration weight - 20% for Teams chat messaging (ENHANCED from 5%)
                chat_score = data.get('chat_collaboration_score', 0)
                
                importance_score = (
                    collaboration_activity_score +
                    interaction_quality_score +
                    confidence_score +
                    graph_api_weight * 0.15 +      # 15% weight for Graph API ranking
                    temporal_recency_score +        # 15% weight for temporal recency
                    document_score * 0.05 +         # 5% weight for document sharing (ENHANCED: OneDrive + Teams attachments)
                    chat_score * 0.20               # 20% weight for Teams chat collaboration (ENHANCED from 5%)
                )
                
                # Filter for genuine collaborators (UPDATED v8.1: Multi-source support)
                # Relaxed filtering for chat-only/document-only/Graph API collaborators
                is_multi_source_only = (has_chat_evidence or has_document_evidence) and not has_calendar_evidence
                is_hybrid_collaborator = has_calendar_evidence and data.get('chat_count', 0) >= 2  # NEW: Calendar + significant chat (≥2 chats)
                has_any_meeting_and_chat = data['total_meetings'] > 0 and data.get('chat_count', 0) >= 2  # NEWER: Any meeting + 2+ chats
                
                if is_multi_source_only or is_hybrid_collaborator or has_any_meeting_and_chat:
                    # Chat-only/Document-only/Hybrid collaborators: More lenient filtering
                    passes_filter = (
                        has_genuine_collaboration and 
                        not is_system_account and
                        final_score > 5  # Lower threshold (was 15)
                    )
                else:
                    # Calendar-based collaborators: Standard filtering
                    passes_filter = (
                        has_genuine_collaboration and 
                        not is_system_account and 
                        final_score > 15 and 
                        confidence > 0.6 and
                        genuine_ratio > 0.3 and
                        email_list_ratio < 0.7
                    )
                
                if passes_filter:
                    print(f"✅ Adding {person} to results (final_score={final_score:.1f}, confidence={confidence:.2f})")
                    try:
                        genuine_collaborators.append({
                            'name': person,
                            'importance_score': round(importance_score, 2),
                            'final_score': round(final_score, 2),
                            'confidence': round(confidence, 3),
                            'genuine_collaboration_meetings': data['genuine_collaboration_meetings'],
                            'informational_meetings': data['informational_meetings'],
                            'broadcast_meetings': data['broadcast_meetings'],
                            'email_list_meetings': data['email_list_meetings'],
                            'genuine_ratio': round(genuine_ratio, 3),
                            'informational_ratio': round(informational_ratio, 3),
                            'email_list_ratio': round(email_list_ratio, 3),
                            'one_on_one': data['one_on_one_meetings'],
                            'organized_by_me': data['organized_by_me'],
                            'small_working_meetings': data['small_working_meetings'],
                            'attended_their_meetings': data['i_attended_their_meetings'],
                            'time_periods': len(data['time_periods']),
                            'total_meetings': data['total_meetings'],
                            'collaboration_evidence': list(set(data['collaboration_evidence'])),
                            'information_evidence': list(set(data['information_consumption_evidence'])),
                            'meeting_details': data['meeting_details'][-5:],  # Last 5 meetings for context
                            'graph_api_rank': data.get('graph_api_rank'),
                            'graph_api_relevance': data.get('graph_api_relevance'),
                            'graph_api_verified': data.get('graph_api_matched', False),
                            'verified_name': data.get('verified_name'),
                            'job_title': data.get('job_title'),
                            'shared_documents': data.get('shared_documents', 0),
                            'document_collaboration_score': data.get('document_collaboration_score', 0),
                            # NEW v8.0: Enhanced document sharing details
                            'onedrive_direct_shares': data.get('onedrive_direct_shares', 0),
                            'onedrive_group_shares': data.get('onedrive_group_shares', 0),
                            'teams_direct_attachments': data.get('teams_direct_attachments', 0),
                            'teams_group_attachments': data.get('teams_group_attachments', 0),
                            'total_document_shares': data.get('total_document_shares', 0),
                            'sharing_days': data.get('sharing_days', 0),
                            'last_share_date': data.get('last_share_date'),
                            'document_recency_label': data.get('document_recency_label', 'N/A'),
                            'document_only_collaborator': data.get('document_only_collaborator', False),
                            # NEW: Temporal recency data
                            'recency_data': {
                                'last_7_days': recency_data.get('last_7_days', 0),
                                'last_30_days': recency_data.get('last_30_days', 0),
                                'last_90_days': recency_data.get('last_90_days', 0),
                                'recent_important_meetings': recency_data.get('recent_important_meetings', 0),
                                'most_recent_meeting': recency_data.get('most_recent_meeting').isoformat() if recency_data.get('most_recent_meeting') else None,
                                'days_since_last_meeting': (datetime.now() - recency_data.get('most_recent_meeting')).days if recency_data.get('most_recent_meeting') else None
                            },
                            'temporal_recency_score': round(temporal_recency_score, 2),
                            # NEW: Teams chat collaboration data
                            'chat_count': data.get('chat_count', 0),
                            'chat_message_count': data.get('chat_message_count', 0),
                            'days_since_last_chat': data.get('days_since_last_chat'),
                            'chat_recency_score': data.get('chat_recency_score', 0),
                            'is_recent_chat': data.get('is_recent_chat', False),
                            'is_frequent_chat': data.get('is_frequent_chat', False),
                            'chat_type': data.get('chat_type'),
                            'chat_only_collaborator': data.get('chat_only_collaborator', False),
                            'chat_collaboration_score': round(data.get('chat_collaboration_score', 0), 2),
                            'algorithm_version': '8.1_multi_source_support'
                        })
                    except Exception as e:
                        print(f"⚠️ Error adding {person} to results: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    # Track why filtered out
                    if not has_genuine_collaboration:
                        debug_filtered['no_evidence'] += 1
                    elif is_system_account:
                        debug_filtered['system_account'] += 1
                    elif final_score <= (5 if is_multi_source_only else 15):
                        debug_filtered['low_score'] += 1
                    else:
                        debug_filtered['low_confidence'] += 1
        
        # Print debug info
        total_filtered = sum(debug_filtered.values())
        if total_filtered > 0:
            print(f"\n⚠️ Filtered {total_filtered} potential collaborators:")
            for reason, count in debug_filtered.items():
                if count > 0:
                    print(f"   - {reason}: {count}")
        
        # Sort by importance score (most important first)
        genuine_collaborators.sort(key=lambda x: x['importance_score'], reverse=True)
        
        return genuine_collaborators
    
    def load_calendar_data(self) -> List[Dict]:
        """
        Load calendar data with auto-detection of format (Scenara or SilverFlow)
        """
        try:
            with open(self.calendar_data_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Calendar data file not found: {self.calendar_data_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in calendar data file: {self.calendar_data_file}")
        
        # Detect format
        if isinstance(raw_data, list):
            # Scenara format: list of events with 'context' field
            print(f"✅ Detected Scenara format ({len(raw_data)} events)")
            return raw_data
        elif isinstance(raw_data, dict):
            # Check for SilverFlow format
            if 'events' in raw_data:
                # SilverFlow format
                events = raw_data['events']
                print(f"✅ Detected SilverFlow format ({len(events)} events)")
                print(f"   Generated: {raw_data.get('generatedAt', 'unknown')}")
                print(f"   Time range: {raw_data.get('startUtc', 'unknown')} to {raw_data.get('endUtc', 'unknown')}")
                
                # Convert to Scenara format on-the-fly
                scenara_events = []
                for idx, event in enumerate(events, 1):
                    # Extract organizer
                    organizer_data = event.get('organizer', {})
                    organizer_email = organizer_data.get('emailAddress', {})
                    organizer_name = organizer_email.get('name', 'Unknown')
                    organizer_address = organizer_email.get('address', '')
                    
                    # Extract attendees (if available in API response)
                    attendees_data = event.get('attendees', [])
                    if attendees_data:
                        attendees = [
                            att.get('emailAddress', {}).get('name', 'Unknown')
                            for att in attendees_data
                            if att.get('emailAddress', {}).get('name')
                            and att.get('type') != 'resource'  # Exclude conference rooms and resources
                        ]
                        # IMPORTANT: Remove self from attendees to get collaborators
                        attendees = [att for att in attendees if att != self.user_name]
                    else:
                        # No attendees in API response - use organizer as collaborator
                        # (This is the limitation of default $select fields)
                        attendees = [organizer_name] if organizer_name != self.user_name else []
                    
                    # Skip if no collaborators (after removing self)
                    if not attendees:
                        continue
                    
                    # Convert to Scenara format
                    scenara_event = {
                        'id': f"silverflow_{idx:03d}",
                        'source': 'silverflow_graph_meetings',
                        'context': {
                            'subject': event.get('subject', 'No Subject'),
                            'description': event.get('bodyPreview', ''),
                            'attendees': attendees if attendees else ['Unknown'],
                            'attendee_count': len(attendees) if attendees else 1,
                            'duration_minutes': self._calculate_duration(
                                event.get('start', {}),
                                event.get('end', {})
                            ),
                            'start_time': event.get('start', {}).get('dateTime', ''),
                            'end_time': event.get('end', {}).get('dateTime', ''),
                            'is_online_meeting': event.get('isOnlineMeeting', True),
                            'importance': 'normal',
                            'organizer': organizer_name,
                            'location': event.get('location', {}).get('displayName', 'Online'),
                            'response_status': event.get('responseStatus', {}).get('response', 'none'),
                            'show_as': event.get('showAs', 'busy'),
                            'webLink': event.get('webLink', '')
                        },
                        'meeting_type': 'General Business Meeting',
                        'preparation_requirements': [],
                        'complexity': 'medium',
                        'quality_score': 8.0,
                        'extracted_date': raw_data.get('generatedAt', datetime.now().isoformat())
                    }
                    scenara_events.append(scenara_event)
                
                print(f"✅ Converted {len(scenara_events)} SilverFlow events to Scenara format")
                
                # DEBUG: Check for Xiaodong Liu in converted events
                xiaodong_count = sum(1 for e in scenara_events 
                                    if any('xiaodong' in att.lower() 
                                          for att in e['context'].get('attendees', [])))
                if xiaodong_count > 0:
                    print(f"   🎯 DEBUG: Found {xiaodong_count} events with Xiaodong Liu")
                    for e in scenara_events:
                        if any('xiaodong' in att.lower() for att in e['context'].get('attendees', [])):
                            print(f"      • {e['context']['subject']}: {e['context']['attendees']}")
                
                return scenara_events
            
            elif 'scenarios' in raw_data:
                # Wrapped Scenara format
                scenarios = raw_data['scenarios']
                print(f"✅ Detected wrapped Scenara format ({len(scenarios)} scenarios)")
                return scenarios
        
        raise ValueError(f"Unknown calendar data format in {self.calendar_data_file}")
    
    def _calculate_duration(self, start: Dict, end: Dict) -> int:
        """Calculate meeting duration in minutes from start/end objects"""
        try:
            start_dt = datetime.fromisoformat(start.get('dateTime', '').replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.get('dateTime', '').replace('Z', '+00:00'))
            duration = (end_dt - start_dt).total_seconds() / 60
            return int(duration)
        except:
            return 60  # Default to 60 minutes
    
    def validate_data_sources(self) -> Dict[str, Any]:
        """
        Validate that all data sources are present and contain sufficient data.
        Returns validation report with warnings and recommendations.
        
        Per .cursorrules: Always check data quality before running discovery.
        """
        validation = {
            'calendar_valid': False,
            'calendar_event_count': 0,
            'calendar_file': self.calendar_data_file,
            'warnings': [],
            'recommendations': []
        }
        
        # Check calendar data file
        try:
            with open(self.calendar_data_file, 'r', encoding='utf-8') as f:
                calendar_data = json.load(f)
                
            # Determine event count based on format
            if isinstance(calendar_data, list):
                # Scenara format or direct event list
                validation['calendar_event_count'] = len(calendar_data)
            elif isinstance(calendar_data, dict) and 'value' in calendar_data:
                # Graph API format
                validation['calendar_event_count'] = len(calendar_data['value'])
            elif isinstance(calendar_data, dict) and 'events' in calendar_data:
                # SilverFlow format
                validation['calendar_event_count'] = len(calendar_data['events'])
            else:
                validation['warnings'].append("Unknown calendar data format")
                
            validation['calendar_valid'] = validation['calendar_event_count'] > 0
            
            # Warn if using small dataset
            if validation['calendar_event_count'] < 100:
                validation['warnings'].append(
                    f"⚠️ Calendar data has only {validation['calendar_event_count']} events - may miss important collaborations"
                )
                validation['recommendations'].append(
                    "Consider using my_calendar_events.json (full dataset) instead of my_calendar_events_50.json (sample)"
                )
                
        except FileNotFoundError:
            validation['warnings'].append(f"❌ Calendar file not found: {self.calendar_data_file}")
            validation['recommendations'].append("Run calendar extraction to create data file")
        except Exception as e:
            validation['warnings'].append(f"❌ Error reading calendar data: {e}")
            
        return validation
    
    def detect_dormant_collaborators(self, collaboration_scores: Dict[str, Dict], 
                                     dormancy_threshold_days: int = 60,
                                     min_historical_score: float = 50.0) -> List[Dict]:
        """
        Detect collaborators who were previously active but have become dormant.
        
        A collaborator is considered dormant if:
        - They had significant collaboration history (final_score > min_historical_score)
        - No meetings, chats, or document sharing in the last N days
        - Previously had regular interaction patterns
        
        Args:
            collaboration_scores: Dictionary of all collaboration data
            dormancy_threshold_days: Days without interaction to be considered dormant (default: 60)
            min_historical_score: Minimum historical collaboration score to qualify (default: 50)
            
        Returns:
            List of dormant collaborators sorted by historical importance
        """
        dormant = []
        current_time = datetime.now()
        
        print(f"\n🔍 Detecting dormant collaborators (no interaction in {dormancy_threshold_days} days)...")
        
        for person, data in collaboration_scores.items():
            # Calculate historical importance
            historical_score = sum(detail['base_score'] for detail in data.get('meeting_details', []))
            
            # Skip if below minimum threshold
            if historical_score < min_historical_score:
                continue
            
            # Check last interaction dates
            last_meeting = None
            last_chat = None
            last_document = None
            
            # Get most recent meeting
            if data.get('meeting_details'):
                meeting_dates = [
                    datetime.fromisoformat(m['start_time'].replace('Z', '+00:00'))
                    for m in data['meeting_details']
                    if m.get('start_time')
                ]
                if meeting_dates:
                    last_meeting = max(meeting_dates)
            
            # Get last chat date
            if data.get('days_since_last_chat') is not None:
                days_since_chat = data['days_since_last_chat']
                last_chat = current_time - timedelta(days=days_since_chat)
            
            # Get last document share date
            if data.get('last_share_date'):
                try:
                    last_document = datetime.fromisoformat(data['last_share_date'].replace('Z', '+00:00'))
                except:
                    pass
            
            # Find most recent interaction
            interaction_dates = [d for d in [last_meeting, last_chat, last_document] if d is not None]
            
            if not interaction_dates:
                continue
            
            most_recent_interaction = max(interaction_dates)
            days_since_interaction = (current_time - most_recent_interaction).days
            
            # Check if dormant
            if days_since_interaction >= dormancy_threshold_days:
                interaction_type = []
                if last_meeting == most_recent_interaction:
                    interaction_type.append(f"meeting {days_since_interaction}d ago")
                if last_chat == most_recent_interaction:
                    interaction_type.append(f"chat {days_since_interaction}d ago")
                if last_document == most_recent_interaction:
                    interaction_type.append(f"document {days_since_interaction}d ago")
                
                dormant.append({
                    'name': person,
                    'historical_score': round(historical_score, 1),
                    'days_since_last_interaction': days_since_interaction,
                    'last_interaction_date': most_recent_interaction.isoformat(),
                    'last_interaction_type': ', '.join(interaction_type),
                    'total_meetings': data.get('total_meetings', 0),
                    'total_chats': data.get('chat_count', 0),
                    'total_documents': data.get('total_document_shares', 0),
                    'last_meeting_date': last_meeting.isoformat() if last_meeting else None,
                    'last_chat_date': last_chat.isoformat() if last_chat else None,
                    'last_document_date': last_document.isoformat() if last_document else None,
                    'job_title': data.get('job_title', 'N/A'),
                    'dormancy_risk': 'HIGH' if days_since_interaction > 120 else 'MEDIUM'
                })
        
        # Sort by historical importance
        dormant.sort(key=lambda x: x['historical_score'], reverse=True)
        
        if dormant:
            print(f"⚠️  Found {len(dormant)} dormant collaborators:")
            for d in dormant[:5]:  # Show top 5
                print(f"   • {d['name']}: {d['days_since_last_interaction']}d inactive "
                      f"(historical score: {d['historical_score']:.0f}, {d['last_interaction_type']})")
        else:
            print("✅ No dormant collaborators detected")
        
        return dormant
    
    def discover_collaborators(self, limit: int = None) -> Dict[str, Any]:
        """
        Main function to discover and rank collaborators
        Integrates calendar data with Microsoft Graph API People rankings
        Supports both Scenara and SilverFlow calendar formats
        """
        # Validate data sources first (per .cursorrules requirement)
        print("🔍 Validating data sources...")
        validation = self.validate_data_sources()
        
        print(f"   Calendar: {validation['calendar_file']}")
        print(f"   Events: {validation['calendar_event_count']}")
        
        if validation['warnings']:
            for warning in validation['warnings']:
                print(f"   {warning}")
        if validation['recommendations']:
            for rec in validation['recommendations']:
                print(f"   💡 {rec}")
        
        if not validation['calendar_valid']:
            raise ValueError("Calendar data validation failed - cannot proceed with discovery")
        
        print()
        
        # Load calendar data (auto-detect format)
        calendar_data = self.load_calendar_data()
        
        # Analyze collaboration patterns from calendar
        print("📅 Analyzing calendar collaboration patterns...")
        collaboration_scores = self.analyze_collaboration_patterns(calendar_data)
        
        # Load and integrate Microsoft Graph API data
        graph_data = self.load_graph_api_data()
        if graph_data:
            collaboration_scores = self.enrich_with_graph_data(collaboration_scores, graph_data)
        
        # Load and integrate Teams chat data (NEW!)
        chat_data = self.load_teams_chat_data()
        if chat_data:
            collaboration_scores = self.enrich_with_chat_data(collaboration_scores, chat_data)
        
        # Load and integrate document collaboration data (ENHANCED!)
        doc_data = self.load_document_collaboration_data()
        if doc_data:
            collaboration_scores = self.enrich_with_document_data(collaboration_scores, doc_data)
        
        # Rank collaborators
        print("🎯 Ranking collaborators with multi-source data fusion...")
        ranked_collaborators = self.rank_collaborators(collaboration_scores)
        
        # Apply limit if specified
        if limit:
            ranked_collaborators = ranked_collaborators[:limit]
        
        # Prepare results
        results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'graph_api_integrated': graph_data is not None,
            'teams_chat_integrated': chat_data is not None,
            'document_sharing_integrated': doc_data is not None,  # NEW!
            'algorithm_version': '8.0_document_sharing_enhanced',
            'user_name': self.user_name,
            'total_collaborators_found': len(ranked_collaborators),
            'data_source': self.calendar_data_file,
            'data_sources': {
                'calendar': self.calendar_data_file,
                'graph_api': 'data/evaluation_results/graph_collaboration_analysis_*.json' if graph_data else None,
                'teams_chat': 'data/evaluation_results/teams_chat_analysis_*.json' if chat_data else None,
                'document_sharing': 'data/evaluation_results/document_collaboration_analysis_*.json' if doc_data else None,
            },
            'ranking_criteria': {
                'importance_calculation': 'collaboration(25%) + quality(20%) + confidence(20%) + graph_api(15%) + temporal_recency(15%) + documents_enhanced(5%) + teams_chat(5%)',
                'filtering_requirements': [
                    'Has genuine collaboration evidence',
                    'Not a system account',
                    'Final score > 15',
                    'Confidence > 60%',
                    'Genuine collaboration ratio > 30%',
                    'Email list ratio < 70%'
                ],
                'new_in_v8': [
                    'Enhanced document collaboration tracking (OneDrive + Teams chat attachments)',
                    'Document sharing temporal analysis (recency + continuity)',
                    'Separate OneDrive vs Teams chat attachment tracking',
                    'Document-only collaborator detection',
                    'Sharing frequency and pattern analysis',
                ],
                'maintained_from_v7': [
                    'Teams chat collaboration integration',
                    'Chat frequency and recency scoring',
                    'Ad hoc chat-only collaborator detection',
                    '1:1 vs group chat differentiation',
                    'Chat temporal weighting (7/30/90 days)',
                ]
            },
            'collaborators': ranked_collaborators
        }
        
        return results
    
    def export_results(self, results: Dict[str, Any], output_file: str = None) -> str:
        """
        Export results to file
        """
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'collaborator_discovery_results_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return output_file
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        """
        Print a summary of the results
        """
        print(f"\n🤝 COLLABORATOR DISCOVERY RESULTS")
        print("=" * 50)
        print(f"📅 Analysis Date: {results['analysis_timestamp'][:10]}")
        print(f"👤 User: {results['user_name']}")
        print(f"🎯 Algorithm: {results['algorithm_version']}")
        print(f"📊 Total Collaborators Found: {results['total_collaborators_found']}")
        if results.get('graph_api_integrated'):
            print(f"✅ Microsoft Graph API: Integrated")
        if results.get('teams_chat_integrated'):
            print(f"💬 Teams Chat: Integrated")
        print()
        
        print("🏆 TOP COLLABORATORS (Most Important to Least Important):")
        print("-" * 60)
        
        for i, collab in enumerate(results['collaborators'], 1):
            print(f"{i}. {collab['name']}")
            
            # Show Graph API verification if available
            if collab.get('graph_api_verified'):
                print(f"   ✅ Verified: {collab.get('verified_name', collab['name'])}")
                if collab.get('graph_api_rank'):
                    print(f"   🌐 Graph API Rank: #{collab['graph_api_rank']}")
                if collab.get('job_title'):
                    print(f"   💼 Title: {collab['job_title']}")
            
            print(f"   🎯 Importance Score: {collab['importance_score']}")
            print(f"   📊 Collaboration Score: {collab['final_score']}")
            print(f"   🔒 Confidence: {collab['confidence']:.1%}")
            print(f"   🤝 Genuine Meetings: {collab['genuine_collaboration_meetings']}/{collab['total_meetings']} ({collab['genuine_ratio']:.1%})")
            
            # NEW: Show recency information
            recency = collab.get('recency_data', {})
            if recency:
                recency_summary = []
                if recency.get('last_7_days', 0) > 0:
                    recency_summary.append(f"🔥 {recency['last_7_days']} this week")
                elif recency.get('last_30_days', 0) > 0:
                    recency_summary.append(f"🔄 {recency['last_30_days']} this month")
                elif recency.get('last_90_days', 0) > 0:
                    recency_summary.append(f"📅 {recency['last_90_days']} this quarter")
                
                if recency.get('days_since_last_meeting') is not None:
                    days = recency['days_since_last_meeting']
                    if days == 0:
                        recency_summary.append("Last: TODAY")
                    elif days == 1:
                        recency_summary.append("Last: YESTERDAY")
                    elif days <= 7:
                        recency_summary.append(f"Last: {days} days ago")
                    elif days <= 30:
                        recency_summary.append(f"Last: {days // 7} weeks ago")
                    else:
                        recency_summary.append(f"Last: {days // 30} months ago")
                
                if recency_summary:
                    print(f"   ⏱️  Recency: {', '.join(recency_summary)}")
            
            # Show document sharing if available
            if collab.get('shared_documents', 0) > 0:
                print(f"   📄 Shared Documents: {collab['shared_documents']} (+{collab['document_collaboration_score']} points)")
            
            # NEW: Show Teams chat collaboration
            if collab.get('chat_count', 0) > 0:
                chat_info = []
                chat_info.append(f"{collab['chat_count']} chats")
                if collab.get('chat_type'):
                    chat_info.append(f"type: {collab['chat_type']}")
                if collab.get('days_since_last_chat') is not None:
                    days = collab['days_since_last_chat']
                    if days <= 7:
                        chat_info.append(f"last: {days}d ago 🔥")
                    elif days <= 30:
                        chat_info.append(f"last: {days}d ago")
                    else:
                        chat_info.append(f"last: {days}d ago")
                if collab.get('chat_only_collaborator'):
                    chat_info.append("✨ CHAT-ONLY (ad hoc)")
                print(f"   💬 Teams Chat: {', '.join(chat_info)} (+{collab.get('chat_collaboration_score', 0):.1f} points)")
            
            # Show key evidence
            evidence = []
            if collab['one_on_one'] > 0:
                evidence.append(f"{collab['one_on_one']} 1:1s")
            if collab['organized_by_me'] > 0:
                evidence.append(f"{collab['organized_by_me']} organized")
            if collab['small_working_meetings'] > 0:
                evidence.append(f"{collab['small_working_meetings']} working sessions")
            if collab['attended_their_meetings'] > 0:
                evidence.append(f"{collab['attended_their_meetings']} attended theirs")
            
            if evidence:
                print(f"   ✅ Evidence: {', '.join(evidence)}")
            print()
    
    def explain_collaborator(self, collaborator_name: str, results: Dict[str, Any]) -> str:
        """
        Explain why a collaborator is ranked at their position.
        Uses the AI-native feedback learning system.
        
        Args:
            collaborator_name: Name of the collaborator to explain
            results: Full collaborator discovery results
            
        Returns:
            Explanation string
        """
        if not self.feedback_system:
            return "⚠️ Feedback system not available"
        
        # Find the collaborator in results
        ranking_data = None
        for collab in results.get('collaborators', []):
            if collab['name'].lower() == collaborator_name.lower():
                ranking_data = collab
                break
        
        # Get explanation
        return self.feedback_system.explain_ranking(
            collaborator_name=collaborator_name,
            ranking_data=ranking_data,
            all_collaborators=results.get('collaborators', [])
        )
    
    def submit_feedback(self, collaborator_name: str, user_comment: str,
                       expected_rank: Optional[int] = None,
                       results: Dict[str, Any] = None) -> None:
        """
        Submit feedback about a collaborator ranking.
        The AI will analyze the feedback, identify data gaps, and suggest improvements.
        
        Args:
            collaborator_name: Name of the collaborator
            user_comment: User's description of actual collaboration
            expected_rank: What rank the user expected (optional)
            results: Full collaborator discovery results
        """
        if not self.feedback_system:
            print("⚠️ Feedback system not available")
            return
        
        # Find actual ranking data
        ranking_data = {}
        actual_rank = None
        
        if results:
            for i, collab in enumerate(results.get('collaborators', []), 1):
                if collab['name'].lower() == collaborator_name.lower():
                    ranking_data = collab
                    actual_rank = i
                    break
        
        # Analyze feedback
        entry = self.feedback_system.analyze_feedback(
            collaborator_name=collaborator_name,
            user_comment=user_comment,
            expected_rank=expected_rank,
            actual_rank=actual_rank,
            ranking_data=ranking_data
        )
        
        # Print analysis
        self.feedback_system.print_feedback_analysis(entry)

def main():
    """
    Command-line interface for the Collaborator Discovery Tool
    """
    # Fix Windows console encoding for emoji/Unicode support
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(description='Discover and rank professional collaborators')
    parser.add_argument('--calendar-data', type=str, 
                       default='meeting_prep_data/real_calendar_scenarios.json',
                       help='Path to calendar data JSON file')
    parser.add_argument('--user-name', type=str, default='Chin-Yew Lin',
                       help='Name of the user for collaboration analysis')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--quiet', action='store_true', help='Suppress summary output')
    
    # Feedback system options
    parser.add_argument('--explain', type=str, help='Explain ranking for a specific collaborator')
    parser.add_argument('--feedback', type=str, help='Submit feedback about a collaborator')
    parser.add_argument('--feedback-comment', type=str, help='Your feedback comment (use with --feedback)')
    parser.add_argument('--expected-rank', type=int, help='Expected rank for feedback (optional)')
    parser.add_argument('--feedback-summary', action='store_true', help='Show data gap summary from all feedback')
    
    args = parser.parse_args()
    
    try:
        # Initialize tool
        tool = CollaboratorDiscoveryTool(
            calendar_data_file=args.calendar_data,
            output_format="json"
        )
        tool.user_name = args.user_name
        
        # Handle feedback-only operations
        if args.feedback_summary:
            if tool.feedback_system:
                gap_summary = tool.feedback_system.get_data_gap_summary()
                print("\n📊 DATA GAP SUMMARY")
                print("=" * 70)
                print(f"Total gaps identified: {gap_summary['total_gaps']}")
                print(f"Unique gap types: {gap_summary['unique_gap_types']}")
                print("\nTop Data Gaps:")
                for gap, count in gap_summary['top_gaps']:
                    print(f"  {count}x: {gap}")
                
                suggestions = tool.feedback_system.suggest_improvements()
                for suggestion in suggestions:
                    print(suggestion)
            else:
                print("⚠️ Feedback system not available")
            return
        
        # Discover collaborators
        print(f"🔍 Discovering collaborators for {args.user_name}...")
        results = tool.discover_collaborators(limit=args.limit)
        
        # Export results
        output_file = tool.export_results(results, args.output)
        print(f"✅ Results saved to: {output_file}")
        
        # Handle explain operation
        if args.explain:
            explanation = tool.explain_collaborator(args.explain, results)
            print(explanation)
        
        # Handle feedback operation
        if args.feedback and args.feedback_comment:
            tool.submit_feedback(
                collaborator_name=args.feedback,
                user_comment=args.feedback_comment,
                expected_rank=args.expected_rank,
                results=results
            )
        elif args.feedback:
            print("⚠️ Please provide --feedback-comment when submitting feedback")
        
        # Print summary unless quiet mode
        if not args.quiet and not args.explain and not args.feedback:
            tool.print_summary(results)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()