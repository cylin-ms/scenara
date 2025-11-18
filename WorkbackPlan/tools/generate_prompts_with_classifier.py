#!/usr/bin/env python3
"""
Enhanced DevUI Prompt Generator with LLM-based Meeting Classification
Uses Qwen3-Embedding-0.6B for intelligent semantic matching of meetings to templates
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import shutil

# Try to import classifier if available
try:
    from simple_qwen3_classifier import SimpleQwen3Classifier
    HAS_CLASSIFIER = True
except ImportError:
    HAS_CLASSIFIER = False
    print("⚠️  Classifier not available. Falling back to keyword matching.")


class DevUIPromptGenerator:
    """Generate personalized DevUI test prompts with LLM classification"""
    
    # Template definitions (simplified from original)
    MEETING_TYPE_TEMPLATES = {
        "Quarterly Business Review (QBR)": {
            "category": "Strategic Planning",
            "complexity": "high",
            "leadTime": 45,
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_get_manager"]
        },
        "Product Launch": {
            "category": "Product Management",
            "complexity": "high",
            "leadTime": 90,
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_get_document"]
        },
        "Conference/Event Preparation": {
            "category": "Events & Communications",
            "complexity": "medium",
            "leadTime": 45,
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_send_mail"]
        },
        "Executive Presentation": {
            "category": "Leadership Communications",
            "complexity": "medium",
            "leadTime": 21,
            "expectedTools": ["graph_calendar_get_events", "graph_get_document", "bizchat_search"]
        },
        "Budget Planning": {
            "category": "Financial Planning",
            "complexity": "medium",
            "leadTime": 30,
            "expectedTools": ["graph_calendar_get_events", "graph_get_document"]
        },
        "Project Kickoff": {
            "category": "Project Management",
            "complexity": "medium",
            "leadTime": 14,
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "ado_get_work_items"]
        },
        "Hiring Committee": {
            "category": "Talent Acquisition",
            "complexity": "low",
            "leadTime": 7,
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_send_mail"]
        },
        "Training Workshop": {
            "category": "Learning & Development",
            "complexity": "medium",
            "leadTime": 60,
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_send_mail"]
        }
    }
    
    # Synthetic high-value/complex scenarios for exploration
    SYNTHETIC_SCENARIOS = [
        {
            "title": "Board of Directors Quarterly Strategy Review",
            "category": "Strategic Planning",
            "complexity": "high",
            "leadTime": 60,
            "description": "Present Q4 performance, annual strategy, and FY26 roadmap to the Board of Directors",
            "attendees": 15,
            "userRole": "organizer",
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_get_document", "bizchat_search"],
            "scenario": "You are presenting to the Board of Directors covering quarterly results, strategic initiatives, competitive landscape, and next year's investment priorities. This is a high-stakes presentation requiring extensive preparation, data analysis, and stakeholder alignment."
        },
        {
            "title": "Major Customer Executive Business Review (Fortune 100)",
            "category": "Strategic Planning",
            "complexity": "high",
            "leadTime": 45,
            "description": "Executive business review with a Fortune 100 customer covering partnership value, roadmap, and expansion opportunities",
            "attendees": 20,
            "userRole": "organizer",
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_get_document", "bizchat_search"],
            "scenario": "Conduct a strategic business review with your largest enterprise customer's C-suite. Need to demonstrate value delivered, address concerns, showcase future capabilities, and identify expansion opportunities worth millions in annual recurring revenue."
        },
        {
            "title": "Annual Product Strategy Offsite with CVP",
            "category": "Product Management",
            "complexity": "high",
            "leadTime": 90,
            "description": "3-day offsite to define product vision, strategy, and OKRs for the next fiscal year",
            "attendees": 30,
            "userRole": "organizer",
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_get_document", "ado_get_work_items"],
            "scenario": "Lead a 3-day offsite with product leadership and engineering directors to define the annual product strategy, prioritize investments across multiple product lines, set ambitious OKRs, and align on execution plans with CVP approval."
        },
        {
            "title": "Crisis Management: Major Service Outage Communication",
            "category": "Leadership Communications",
            "complexity": "high",
            "leadTime": 7,
            "description": "Coordinate crisis response and executive communications for a major service outage affecting millions of users",
            "attendees": 25,
            "userRole": "organizer",
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_send_mail", "bizchat_search"],
            "scenario": "A critical service outage has impacted millions of customers. You need to coordinate incident response, prepare executive communications, manage customer notifications, and organize war room logistics. Time is critical and stakes are high."
        },
        {
            "title": "Company-Wide Product Training Launch (M365 Pulse)",
            "category": "Learning & Development",
            "complexity": "high",
            "leadTime": 45,
            "description": "Launch enterprise-wide training program on new M365 Pulse features for 374+ participants across global offices",
            "attendees": 374,
            "userRole": "participant",
            "expectedTools": ["graph_calendar_get_events", "graph_get_people", "graph_send_mail", "graph_get_document"],
            "scenario": "Participate in planning the launch of a comprehensive training program introducing M365 Pulse to the entire organization. With 374 participants across multiple time zones, this requires coordinating trainers, preparing materials, setting up virtual infrastructure, creating feedback loops, and ensuring maximum adoption of critical productivity tools."
        }
    ]
    
    def __init__(
        self,
        calendar_path: str,
        user_name: str,
        user_email: str,
        output_dir: str,
        model_path: Optional[str] = None
    ):
        self.calendar_path = Path(calendar_path)
        self.user_name = user_name
        self.user_email = user_email.lower()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load calendar data
        with open(self.calendar_path, 'r') as f:
            data = json.load(f)
            # Handle different JSON formats
            if isinstance(data, dict):
                if 'events' in data:
                    self.meetings = data['events']
                elif 'value' in data:
                    self.meetings = data['value']
                else:
                    self.meetings = data
            else:
                self.meetings = data
        
        print(f"📅 Loaded {len(self.meetings)} meetings from calendar")
        print(f"👤 User: {self.user_name} ({self.user_email})")
        
        # Initialize classifier if available
        self.classifier = None
        if HAS_CLASSIFIER and model_path:
            try:
                self.classifier = SimpleQwen3Classifier(model_path)
                print("🤖 Using Qwen3-Embedding-0.6B for meeting classification")
            except Exception as e:
                print(f"⚠️  Could not load classifier: {e}")
                print("   Falling back to keyword matching")
        
        self.matched_prompts = []
    
    def _is_organizer(self, meeting: Dict) -> bool:
        """Check if user is the meeting organizer"""
        organizer = meeting.get('organizer', {})
        organizer_email = organizer.get('emailAddress', {}).get('address', '').lower()
        return organizer_email == self.user_email
    
    def _get_user_role(self, meeting: Dict) -> str:
        """Determine user's role in the meeting"""
        return "organizer" if self._is_organizer(meeting) else "participant"
    
    def classify_meetings(self) -> Dict[str, List[Dict]]:
        """Classify meetings into template categories using LLM or keywords"""
        classifications = {}
        
        if self.classifier:
            # Use LLM classification
            print("\n🔍 Classifying meetings with AI...")
            for meeting in self.meetings:
                if len(meeting.get('attendees', [])) < 3:
                    continue  # Skip small meetings
                
                category, confidence = self.classifier.classify_meeting(
                    title=meeting.get('subject', ''),
                    description=meeting.get('bodyPreview', ''),
                    attendee_count=len(meeting.get('attendees', []))
                )
                
                if confidence > 0.4:  # Confidence threshold
                    if category not in classifications:
                        classifications[category] = []
                    
                    # Add role and confidence to meeting data
                    classifications[category].append({
                        'meeting': meeting,
                        'confidence': confidence,
                        'role': self._get_user_role(meeting),
                        'is_organizer': self._is_organizer(meeting),
                        'attendee_count': len(meeting.get('attendees', []))
                    })
        else:
            # Fallback to keyword matching
            print("\n🔍 Classifying meetings with keywords...")
            classifications = self._keyword_classify()
        
        return classifications
    
    def _keyword_classify(self) -> Dict[str, List[Dict]]:
        """Fallback keyword-based classification"""
        # Simple keyword matching (original logic)
        classifications = {}
        
        keywords_map = {
            "Quarterly Business Review (QBR)": ["qbr", "quarterly", "business review"],
            "Product Launch": ["launch", "release", "ship", "ga"],
            "Conference/Event Preparation": ["conference", "summit", "event", "convention", "kickoff"],
            "Executive Presentation": ["presentation", "executive", "leadership"],
            "Budget Planning": ["budget", "financial", "fiscal"],
            "Project Kickoff": ["kickoff", "project start"],
            "Hiring Committee": ["interview", "candidate", "hiring"],
            "Training Workshop": ["training", "workshop", "boot camp", "course"]
        }
        
        for meeting in self.meetings:
            if len(meeting.get('attendees', [])) < 3:
                continue
            
            subject = meeting.get('subject', '').lower()
            for category, keywords in keywords_map.items():
                if any(kw in subject for kw in keywords):
                    if category not in classifications:
                        classifications[category] = []
                    classifications[category].append({
                        'meeting': meeting,
                        'confidence': 0.8,
                        'role': self._get_user_role(meeting),
                        'is_organizer': self._is_organizer(meeting),
                        'attendee_count': len(meeting.get('attendees', []))
                    })
                    break
        
        return classifications
    
    def generate_prompts(self, target_count: int = 20, min_organizer: int = 10, preserve_file: Optional[str] = None):
        """Generate prompts from classified meetings with smart selection
        
        Args:
            target_count: Total number of prompts to generate
            min_organizer: Minimum number of organizer meetings
            preserve_file: Path to JSON file with meetings to preserve from previous annotations
        """
        # Load preserved meetings if specified
        preserved_meetings = []
        if preserve_file and Path(preserve_file).exists():
            with open(preserve_file, 'r') as f:
                preserve_data = json.load(f)
                preserved_meetings = preserve_data.get('meetings_to_preserve', [])
                print(f"\n📌 Preserving {len(preserved_meetings)} previously annotated meetings")
        
        classifications = self.classify_meetings()
        
        print(f"\n📊 Classification results:")
        total_classified = 0
        organizer_count = 0
        participant_count = 0
        
        for category, matches in classifications.items():
            organizers = sum(1 for m in matches if m['is_organizer'])
            participants = len(matches) - organizers
            total_classified += len(matches)
            organizer_count += organizers
            participant_count += participants
            print(f"  {category}: {len(matches)} meetings (👤 {organizers} organizer, 👥 {participants} participant)")
        
        print(f"\n📈 Total: {total_classified} meetings classified")
        print(f"   👤 Organizer: {organizer_count} meetings")
        print(f"   👥 Participant: {participant_count} meetings")
        
        # Smart selection strategy
        print(f"\n🎯 Selection strategy: {target_count} prompts ({min_organizer}+ as organizer)")
        
        selected_meetings = []
        
        # Phase 0: Add preserved meetings first
        if preserved_meetings:
            print("\n📌 Phase 0: Adding preserved annotated meetings...")
            for preserved in preserved_meetings:
                # Extract meeting title without attendee count
                # e.g., "STCA Monthly Extended PLT + Managers (180 attendees)" -> "STCA Monthly Extended PLT + Managers"
                preserved_title = preserved['realMeeting']
                if ' (' in preserved_title and preserved_title.endswith(')'):
                    preserved_title = preserved_title.rsplit(' (', 1)[0]
                
                # Normalize for matching (lowercase, strip whitespace)
                preserved_norm = preserved_title.lower().strip()
                
                # Find this meeting in classifications
                found = False
                for category, matches in classifications.items():
                    for match in matches:
                        meeting_subject = match['meeting'].get('subject', '')
                        meeting_norm = meeting_subject.lower().strip()
                        
                        # Try exact match or fuzzy match (contains)
                        if (meeting_norm == preserved_norm or 
                            preserved_norm in meeting_norm or 
                            meeting_norm in preserved_norm):
                            selected_meetings.append((category, match))
                            print(f"  ✓ Preserved: {meeting_subject[:60]} ({category})")
                            found = True
                            break
                    if found:
                        break
                
                # If not found in classifications, search raw calendar and force-classify
                if not found:
                    print(f"  ⚠️  Not in classifications, searching raw calendar: {preserved_title[:50]}")
                    for event in self.meetings:
                        event_subject = event.get('subject', '') or ''
                        if not event_subject or not event_subject.strip():
                            continue  # Skip events with no subject
                        
                        event_norm = event_subject.lower().strip()
                        
                        # Match only if both strings have content
                        if preserved_norm and event_norm and (
                            event_norm == preserved_norm or 
                            preserved_norm in event_norm or 
                            event_norm in preserved_norm):
                            # Found in calendar! Classify it
                            print(f"      🔍 Found event: '{event_subject}'")
                            
                            if self.classifier:
                                category, confidence = self.classifier.classify_meeting(
                                    title=event.get('subject', ''),
                                    description=event.get('bodyPreview', ''),
                                    attendee_count=len(event.get('attendees', []))
                                )
                            else:
                                # Use keyword-based classification as fallback - use a valid template key
                                category = "Conference/Event Preparation"  # Default to a valid category
                                confidence = 0.8
                            
                            # Build result dict like in classify_meetings
                            result = {
                                'meeting': event,
                                'confidence': confidence,
                                'role': self._get_user_role(event),
                                'is_organizer': self._is_organizer(event),
                                'attendee_count': len(event.get('attendees', []))
                            }
                            
                            selected_meetings.append((category, result))
                            print(f"      ✓ Force-included: {event_subject[:50]} ({category})")
                            found = True
                            break
                
                if not found:
                    print(f"      ❌ Not found in calendar either")
            
            print(f"   Added {len(selected_meetings)} preserved meetings")
        
        # Phase 1: Select best organizer meetings (diversify across categories)
        print(f"\n📌 Phase 1: Selecting organizer meetings...")
        organizer_meetings = []
        selected_subjects = {m[1]['meeting'].get('subject') for m in selected_meetings}
        
        for category, matches in classifications.items():
            # Get organizer meetings for this category not already selected
            cat_organizers = [m for m in matches if m['is_organizer'] and m['meeting'].get('subject') not in selected_subjects]
            if cat_organizers:
                # Pick best by confidence and attendee count
                best = max(cat_organizers, key=lambda x: (x['confidence'], x['attendee_count']))
                organizer_meetings.append((category, best))
                print(f"  ✓ {category}: {best['meeting'].get('subject', 'Untitled')[:60]} ({best['attendee_count']} attendees)")
        
        # Add organizer meetings up to min_organizer (accounting for preserved)
        current_organizer_count = sum(1 for m in selected_meetings if m[1]['is_organizer'])
        organizers_needed = max(0, min_organizer - current_organizer_count)
        selected_meetings.extend(organizer_meetings[:organizers_needed])
        
        # Phase 2: Fill remaining slots with best meetings (any role, diversify categories)
        print(f"\n📌 Phase 2: Filling remaining slots ({target_count - len(selected_meetings)} needed)...")
        remaining_needed = target_count - len(selected_meetings)
        
        # Get all meetings not yet selected, sorted by quality
        all_meetings = []
        selected_subjects = {m[1]['meeting'].get('subject') for m in selected_meetings}
        
        for category, matches in classifications.items():
            for match in matches:
                subject = match['meeting'].get('subject')
                if subject not in selected_subjects:
                    all_meetings.append((category, match))
        
        # Sort by: role (organizer first), confidence, attendee count
        all_meetings.sort(
            key=lambda x: (
                0 if x[1]['is_organizer'] else 1,  # Organizer first
                -x[1]['confidence'],                 # Higher confidence
                -x[1]['attendee_count']             # More attendees
            )
        )
        
        # Add diverse meetings (avoid too many from same category)
        category_counts = {cat: 1 for cat, _ in selected_meetings}
        for category, match in all_meetings:
            if len(selected_meetings) >= target_count:
                break
            # Prefer categories with fewer selections (diversity, max 4 per category for 20 total)
            if category_counts.get(category, 0) < 4:
                selected_meetings.append((category, match))
                category_counts[category] = category_counts.get(category, 0) + 1
                role_icon = "👤" if match['is_organizer'] else "👥"
                print(f"  {role_icon} {category}: {match['meeting'].get('subject', 'Untitled')[:60]} ({match['attendee_count']} attendees)")
        
        # Phase 3: Generate prompts with role-specific content
        # Start IDs from 6 to leave room for synthetic prompts (1-5)
        print(f"\n📝 Generating {len(selected_meetings)} prompts...")
        prompt_id = 6  # Start from 6, synthetic will be 1-5
        for category, match in selected_meetings:
            template = self.MEETING_TYPE_TEMPLATES[category]
            meeting = match['meeting']
            role = match['role']
            
            prompt_data = self._create_prompt_data(
                prompt_id, category, template, meeting, role
            )
            self.matched_prompts.append(prompt_data)
            prompt_id += 1
        
        print(f"\n✅ Generated {len(self.matched_prompts)} prompts from real meetings")
        print(f"   👤 As organizer: {sum(1 for p in self.matched_prompts if p.get('userRole') == 'organizer')}")
        print(f"   👥 As participant: {sum(1 for p in self.matched_prompts if p.get('userRole') == 'participant')}")
        
        return self.matched_prompts
    
    def add_synthetic_scenarios(self, count: int = 5):
        """Add synthetic high-value/complex scenarios for exploration
        Synthetic scenarios get IDs 1-5, added at the beginning of the list"""
        print(f"\n🎭 Adding {count} synthetic high-value scenarios for exploration...")
        
        scenarios_to_add = self.SYNTHETIC_SCENARIOS[:count]
        synthetic_prompts = []
        
        for idx, scenario in enumerate(scenarios_to_add):
            prompt_id = idx + 1  # Synthetic prompts get IDs 1-5
            
            # Build role-specific context
            role = scenario['userRole']
            if role == 'organizer':
                role_context = "As the organizer and leader of this high-stakes meeting, you are responsible for its success and strategic outcomes."
                role_tasks = """- Define meeting objectives and desired outcomes
- Identify and invite key stakeholders and decision makers
- Prepare comprehensive presentation materials and data analysis
- Coordinate pre-reads and background materials
- Plan for contingencies and difficult questions
- Arrange logistics (venue, technology, catering for multi-day events)
- Schedule preparation sessions with your team
- Create detailed agenda with time allocations"""
            else:
                role_context = "As a key participant in this strategic meeting, you need to be thoroughly prepared to contribute effectively."
                role_tasks = """- Review all meeting materials and background documents
- Prepare your perspective and recommendations
- Identify questions and concerns to raise
- Coordinate with your team on unified position
- Research relevant data and competitive intelligence
- Prepare to take detailed notes and action items
- Plan follow-up actions and next steps"""
            
            prompt_text = f"""**[EXPLORATION SCENARIO - Not from your calendar]**

This is a hypothetical high-value scenario designed to explore how BizChat can help with complex meeting preparation.

Scenario: {scenario['title']}

{scenario['scenario']}

{role_context}

Meeting Details:
- Category: {scenario['category']}
- Complexity: {scenario['complexity'].upper()}
- Recommended Lead Time: {scenario['leadTime']} days
- Expected Attendees: ~{scenario['attendees']} people

Please use your imagination to create a comprehensive workback plan for this scenario:

{role_tasks}

**Goal**: Experience how BizChat assists with high-stakes, complex meeting preparation. Save the DevUI session link to help us collect data for improving high-value scenarios."""
            
            synthetic_prompt = {
                "id": prompt_id,
                "title": scenario['title'],
                "category": scenario['category'],
                "complexity": scenario['complexity'],
                "leadTime": scenario['leadTime'],
                "realMeeting": f"[Synthetic Scenario] {scenario['description']}",
                "userRole": scenario['userRole'],
                "prompt": prompt_text,
                "expectedTools": scenario['expectedTools'],
                "status": "not-started",
                "selected": False,
                "isSynthetic": True,  # Mark as synthetic
                "devuiLink": "",
                "sessionId": "",
                "dateCaptured": "",
                "toolsObserved": "",
                "zeroShotFeedback": "",
                "overallFeedback": "",
                "notes": ""
            }
            
            synthetic_prompts.append(synthetic_prompt)
            print(f"  ✨ Added: {scenario['title']}")
        
        # Insert synthetic prompts at the beginning (IDs 1-5)
        self.matched_prompts = synthetic_prompts + self.matched_prompts
        
        print(f"\n✅ Total prompts: {len(self.matched_prompts)} ({count} synthetic + {len(self.matched_prompts) - count} real)")
    
    def _create_prompt_data(self, prompt_id: int, category: str, template: Dict, meeting: Dict, role: str) -> Dict:
        """Create prompt data structure with role-specific content and rich meeting data"""
        subject = meeting.get('subject', 'Untitled')
        attendees = meeting.get('attendees', [])
        attendee_count = len(attendees)
        
        # Extract organizer information
        organizer = meeting.get('organizer', {}).get('emailAddress', {})
        organizer_name = organizer.get('name', 'Unknown')
        organizer_email = organizer.get('address', 'Unknown')
        
        # Extract datetime - handle various formats
        start_dt = meeting.get('start', {}).get('dateTime', '')
        end_dt = meeting.get('end', {}).get('dateTime', '')
        if start_dt:
            try:
                # Remove microseconds if present (e.g., .0000000)
                if '.' in start_dt:
                    start_dt = start_dt.split('.')[0]
                # Replace Z with +00:00 for ISO format
                start_dt = start_dt.replace('Z', '+00:00')
                dt_obj = datetime.fromisoformat(start_dt)
                date_str = dt_obj.strftime('%B %d, %Y')
                time_str = dt_obj.strftime('%I:%M %p')
                day_of_week = dt_obj.strftime('%A')
            except (ValueError, AttributeError):
                date_str = "TBD"
                time_str = "TBD"
                day_of_week = ""
        else:
            date_str = "TBD"
            time_str = "TBD"
            day_of_week = ""
        
        # Calculate duration
        duration_str = ""
        if start_dt and end_dt:
            try:
                if '.' in end_dt:
                    end_dt = end_dt.split('.')[0]
                end_dt = end_dt.replace('Z', '+00:00')
                start_obj = datetime.fromisoformat(start_dt)
                end_obj = datetime.fromisoformat(end_dt)
                duration = end_obj - start_obj
                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60
                if hours > 0:
                    duration_str = f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
                else:
                    duration_str = f"{minutes}m"
            except:
                duration_str = "TBD"
        
        location = meeting.get('location', {}).get('displayName', 'TBD')
        is_online = meeting.get('isOnlineMeeting', False)
        online_provider = meeting.get('onlineMeetingProvider', '')
        
        # Get body content (description)
        body_content = meeting.get('body', {}).get('content', 'No description available')
        # Strip HTML tags for cleaner text
        import re
        body_text = re.sub('<[^<]+?>', '', body_content)
        body_text = body_text.strip()[:300]  # Limit to 300 chars
        
        # Build attendee summary
        attendee_list = []
        for att in attendees[:10]:  # Show first 10 attendees
            att_email = att.get('emailAddress', {})
            att_name = att_email.get('name', 'Unknown')
            attendee_list.append(att_name)
        
        attendee_summary = ", ".join(attendee_list)
        if len(attendees) > 10:
            attendee_summary += f", and {len(attendees) - 10} more"
        
        # Role-specific prompt variations
        if role == "organizer":
            role_context = f"""As the organizer of this meeting, you are responsible for its success."""
            coordination_tasks = """
- Coordinate with all attendees and confirm their participation
- Ensure all required materials and documents are prepared
- Set up the meeting logistics (venue, technology, catering if applicable)
- Prepare and distribute the agenda in advance
- Assign preparation tasks to team members
- Plan for potential contingencies"""
        else:  # participant
            role_context = f"""As a participant in this meeting, you want to be well-prepared to contribute effectively."""
            coordination_tasks = """
- Review the meeting agenda and objectives
- Prepare any materials or updates you need to present
- Identify questions or topics you want to raise
- Review relevant background documents
- Coordinate with your team on your input
- Prepare to take notes and action items"""
        
        # Build rich meeting context
        meeting_details = f"""
📅 **Meeting Information:**
- **Title**: {subject}
- **Date**: {day_of_week}, {date_str}
- **Time**: {time_str} ({duration_str} duration)
- **Location**: {location}
- **Format**: {"Virtual ({})".format(online_provider) if is_online else "In-person"}
- **Organizer**: {organizer_name} ({organizer_email})
- **Attendees**: {attendee_count} people
- **Key Participants**: {attendee_summary}

📋 **Meeting Description:**
{body_text}
"""
        
        # Create prompt text with role-specific content (without meeting metadata)
        prompt_text = f"""I have an upcoming {category.lower()} meeting.

{role_context}

**Your Task:**
Please access my calendar event to retrieve the complete attendee list, full meeting description, and any linked documents. Then create a comprehensive workback plan that includes:

1. **Timeline Planning**: Work backwards from the meeting date to identify all preparation milestones
2. **Task Breakdown**: Specific actionable tasks with clear owners from the attendee list
3. **Dependencies**: Map out task dependencies and critical path
4. **Stakeholder Coordination**: Identify key decision makers and their roles
5. **Risk Mitigation**: Plan for potential delays or issues

**Consider:**
{coordination_tasks}
- Use actual attendee names for task assignments
- Reference the meeting location for logistics planning
- Check for related emails, documents, or previous meetings
- Account for review cycles and approval processes

Generate a detailed workback plan that ensures successful meeting preparation."""
        
        return {
            "id": prompt_id,
            "title": category,
            "category": template['category'],
            "complexity": template['complexity'],
            "leadTime": template['leadTime'],
            "realMeeting": f"{subject} ({attendee_count} attendees)",
            "meetingDate": date_str,
            "meetingTime": time_str,
            "meetingDuration": duration_str,
            "meetingLocation": location,
            "organizerName": organizer_name,
            "organizerEmail": organizer_email,
            "attendeeCount": attendee_count,
            "isOnline": is_online,
            "userRole": role,
            "prompt": prompt_text,
            "expectedTools": template['expectedTools'],
            "status": "not-started",
            "selected": False,  # User selection status
            "isSynthetic": False,  # Real meeting from calendar
            "devuiLink": "",
            "sessionId": "",
            "dateCaptured": "",
            "toolsObserved": "",
            "zeroShotFeedback": "",
            "overallFeedback": "",
            "notes": ""
        }
    
    def save_package(self):
        """Save generated prompts as JSON"""
        output_file = self.output_dir / f"prompts_{self.user_name.lower().replace(' ', '_')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.matched_prompts, f, indent=2)
        
        print(f"\n💾 Saved prompts to: {output_file}")
        return output_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate personalized DevUI test prompts with smart selection")
    parser.add_argument("--calendar", required=True, help="Path to calendar JSON file")
    parser.add_argument("--user", required=True, help="User name for personalization")
    parser.add_argument("--email", required=True, help="User email to determine organizer/participant role")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--model", help="Path to AI model for classification (optional)")
    parser.add_argument("--count", type=int, default=20, help="Number of prompts to generate (default: 20, recommended: 10)")
    parser.add_argument("--min-organizer", type=int, default=10, help="Minimum organizer meetings (default: 10)")
    parser.add_argument("--add-synthetic", type=int, default=5, help="Number of synthetic high-value scenarios to add (default: 5)")
    parser.add_argument("--preserve-annotated", action="store_true", help="Preserve previously annotated meetings (uses preserve_meetings.json)")
    
    args = parser.parse_args()
    
    generator = DevUIPromptGenerator(
        calendar_path=args.calendar,
        user_name=args.user,
        user_email=args.email,
        output_dir=args.output,
        model_path=args.model
    )
    
    # Determine preserve file path
    preserve_file = None
    if args.preserve_annotated:
        preserve_file = Path(__file__).parent / "preserve_meetings.json"
        if not preserve_file.exists():
            print("⚠️  --preserve-annotated specified but preserve_meetings.json not found")
            print("   Run: python check_annotated_meetings.py first")
            print("   Continuing without preservation...")
            preserve_file = None
    
    generator.generate_prompts(
        target_count=args.count, 
        min_organizer=args.min_organizer,
        preserve_file=str(preserve_file) if preserve_file else None
    )
    
    # Add synthetic high-value scenarios
    if hasattr(args, 'add_synthetic') and args.add_synthetic > 0:
        generator.add_synthetic_scenarios(count=args.add_synthetic)
    else:
        generator.add_synthetic_scenarios(count=5)  # Default 5 synthetic scenarios
    
    generator.save_package()
    
    print("\n✅ Package generation complete!")


if __name__ == "__main__":
    main()
