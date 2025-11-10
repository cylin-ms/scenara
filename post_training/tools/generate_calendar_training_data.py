#!/usr/bin/env python3
"""
Calendar-Based Training Data Generator using GPT-5

Generates realistic monthly calendars (20-40 meetings) for persona-based RLHF training.
Unlike the basic generator, this creates temporally coherent calendars with:
- Recurring meetings (weekly 1:1s, team syncs, etc.)
- Ad-hoc meetings (customer escalations, project discussions)
- Realistic temporal patterns (no 4am meetings, respect work hours)
- Time conflicts and overlaps (calendar pressure simulation)
- Multi-week context for importance evaluation

Usage:
    # Generate 1 month calendar for specific persona
    python post_training/tools/generate_calendar_training_data.py \
        --persona post_training/data/personas/tier1_sales_manager_pipeline.json \
        --weeks 4 \
        --output-dir post_training/data/training/calendars

    # Generate calendars for all Tier 1 personas
    python post_training/tools/generate_calendar_training_data.py \
        --tier 1 \
        --weeks 4 \
        --output-dir post_training/data/training/calendars
"""

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import random

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import GPT-5 infrastructure
try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, DEFAULT_ENDPOINT, DEFAULT_MODEL
except ImportError:
    print("ERROR: Could not import GPT5MeetingClassifier")
    print("Make sure tools/meeting_classifier_gpt5.py is available in project root")
    sys.exit(1)

# Import persona config
try:
    from post_training.tools.generate_persona_training_data import PersonaConfig
except ImportError:
    print("ERROR: Could not import PersonaConfig")
    print("Make sure post_training/tools/generate_persona_training_data.py exists")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CalendarTrainingDataGenerator:
    """Generate realistic monthly calendars for persona-based training."""
    
    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        model: str = DEFAULT_MODEL
    ):
        """Initialize generator with GPT-5 model."""
        self.classifier = GPT5MeetingClassifier(endpoint=endpoint, model=model)
        logger.info(f"Initialized Calendar Training Data Generator with model: {model}")
    
    def _call_gpt5_with_extended_tokens(
        self,
        system_message: str,
        user_prompt: str,
        max_tokens: int = 16000
    ) -> Dict[str, Any]:
        """
        Call GPT-5 API with extended token limit for calendar generation.
        Uses the classifier's auth but with custom payload for higher token limits.
        """
        import requests
        import json
        import uuid
        import time
        
        try:
            # Acquire token using classifier's method
            token = self.classifier._acquire_token()
            if not token:
                return {"success": False, "error": "Failed to acquire access token"}
            
            # Build request payload with higher token limit
            payload = {
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ],
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "max_completion_tokens": max_tokens,  # Extended limit
                "temperature": 0.8,  # Higher temp for variety
                "top_p": 0.95,
                "n": 1,
                "stream": False,
                "response_format": None,
            }
            
            # Build request headers
            headers = {
                "Authorization": f"Bearer {token}",
                "X-ModelType": self.classifier.model,
                "X-ScenarioGUID": str(uuid.uuid4()),
                "Content-Type": "application/json",
            }
            
            # Make API request
            response = requests.post(
                self.classifier.endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=120
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}: {response.text}"
                }
            
            # Parse response
            result = response.json()
            if 'choices' not in result or not result['choices']:
                return {"success": False, "error": "No choices in response"}
            
            content = result['choices'][0]['message']['content']
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_calendar(
        self,
        persona: PersonaConfig,
        weeks: int = 4,
        start_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate a realistic calendar for the persona spanning multiple weeks.
        
        Args:
            persona: Persona configuration with preference rules
            weeks: Number of weeks to generate (default: 4)
            start_date: Start date for calendar (default: next Monday)
        
        Returns:
            List of meeting dictionaries with labels
        """
        if start_date is None:
            # Start from next Monday
            today = datetime.now()
            days_until_monday = (7 - today.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7  # If today is Monday, start next Monday
            start_date = today + timedelta(days=days_until_monday)
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        logger.info(f"Processing: {persona.name} (Tier {persona.tier})")
        logger.info(f"Generating {weeks}-week calendar starting {start_date.strftime('%Y-%m-%d')}")
        
        # Calculate target meeting count based on persona's weekly load
        weekly_hours = self._parse_weekly_hours(persona.meeting_context.get('weekly_meeting_hours', '20-25'))
        avg_meeting_duration = 1.0  # hours
        meetings_per_week = int(weekly_hours / avg_meeting_duration)
        total_meetings = meetings_per_week * weeks
        
        logger.info(f"Target: ~{meetings_per_week} meetings/week ({total_meetings} total)")
        
        # Generate calendar in batches (max 20 meetings per batch to avoid truncation)
        batch_size = 20
        all_meetings = []
        
        for batch_num in range(0, total_meetings, batch_size):
            batch_count = min(batch_size, total_meetings - batch_num)
            batch_week_start = batch_num // meetings_per_week
            
            logger.info(f"Batch {batch_num//batch_size + 1}/{(total_meetings + batch_size - 1)//batch_size}: Generating {batch_count} meetings...")
            
            # Generate calendar structure with recurring + ad-hoc meetings
            meetings = self._generate_calendar_structure(
                persona=persona,
                start_date=start_date + timedelta(weeks=batch_week_start),
                weeks=min(2, weeks - batch_week_start),  # Generate 2 weeks at a time
                target_count=batch_count
            )
            
            all_meetings.extend(meetings)
            time.sleep(2)  # Rate limiting between batches
        
        meetings = all_meetings
        
        # Apply persona rules to label each meeting
        labeled_meetings = []
        for meeting in meetings:
            labeled_meeting = self._apply_persona_rules(meeting, persona)
            labeled_meetings.append(labeled_meeting)
        
        # Sort by start time
        labeled_meetings.sort(key=lambda m: m['start']['dateTime'])
        
        return labeled_meetings
    
    def _parse_weekly_hours(self, hours_str: str) -> float:
        """Parse weekly hours string like '20-25' or '28-32 hours'."""
        if isinstance(hours_str, (int, float)):
            return float(hours_str)
        
        # Clean string: remove " hours", "hrs", etc.
        hours_str = str(hours_str).lower().replace(' hours', '').replace('hrs', '').strip()
        
        # Handle range like "20-25"
        if '-' in hours_str:
            parts = hours_str.split('-')
            try:
                low = float(parts[0].strip())
                high = float(parts[1].strip())
                return (low + high) / 2
            except:
                return 20.0  # Default
        
        # Handle single number
        try:
            return float(hours_str)
        except:
            return 20.0  # Default
    
    def _generate_calendar_structure(
        self,
        persona: PersonaConfig,
        start_date: datetime,
        weeks: int,
        target_count: int
    ) -> List[Dict[str, Any]]:
        """
        Generate calendar structure using GPT-5 with temporal coherence.
        
        Creates a mix of:
        - Recurring meetings (30-40%): Weekly 1:1s, team syncs, standups
        - Ad-hoc meetings (60-70%): Project discussions, customer calls, reviews
        """
        # Generate prompt for GPT-5
        system_message, user_prompt = self._create_calendar_generation_prompt(
            persona=persona,
            start_date=start_date,
            weeks=weeks,
            total_meetings=target_count
        )
        
        # Call GPT-5 with extended token limit
        start_time = time.time()
        
        # Use custom API call with higher max_completion_tokens
        result = self._call_gpt5_with_extended_tokens(
            system_message=system_message,
            user_prompt=user_prompt,
            max_tokens=16000  # Allow 16K tokens for calendar generation
        )
        
        elapsed = time.time() - start_time
        
        if not result['success']:
            logger.error(f"GPT-5 API call failed: {result.get('error', 'Unknown error')}")
            return []
        
        response = result.get('content', '')
        
        # Parse JSON response
        try:
            # Extract JSON array from response
            content = response.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            meetings = json.loads(content)
            logger.info(f"✅ Generated {len(meetings)} meetings")
            return meetings
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT-5 response: {e}")
            logger.error(f"Response: {response[:500]}...")
            return []
    
    def _create_calendar_generation_prompt(
        self,
        persona: PersonaConfig,
        start_date: datetime,
        weeks: int,
        total_meetings: int
    ) -> Tuple[str, str]:
        """Create prompts for GPT-5 calendar generation."""
        
        end_date = start_date + timedelta(weeks=weeks)
        
        system_message = """You are a calendar generation system for enterprise meeting intelligence.

Your task: Generate a REALISTIC MONTHLY CALENDAR for a specific persona with temporal coherence.

Key Requirements:
1. **Temporal Realism**: 
   - Spread meetings across work hours (8am-6pm in persona's timezone)
   - No 4am meetings or late-night calls (unless emergency escalations)
   - Recurring meetings repeat weekly (same day/time)
   - Ad-hoc meetings scattered throughout weeks

2. **Meeting Mix** (realistic calendar composition):
   - 30-40% Recurring: Weekly 1:1s, team syncs, standups, reviews
   - 60-70% Ad-hoc: Project discussions, customer calls, planning sessions

3. **Recurring Meeting Patterns**:
   - Weekly 1:1 with manager (30-60 min, same day/time each week)
   - Team sync (30-60 min, same day/time each week)
   - Cross-functional sync (if applicable, 60 min weekly)
   - Staff meetings (if manager, 60-90 min weekly)

4. **Microsoft Graph API Schema** (REQUIRED):
```json
{
  "id": "evt-2025-11-18-pipeline-review",
  "subject": "Weekly Pipeline Review - APAC Team",
  "bodyPreview": "Detailed description of meeting purpose and agenda",
  "showAs": "busy",
  "type": "occurrence",
  "responseStatus": {
    "response": "organizer",
    "time": "0001-01-01T00:00:00Z"
  },
  "start": {
    "dateTime": "2025-11-18T09:00:00.0000000",
    "timeZone": "Asia/Shanghai"
  },
  "end": {
    "dateTime": "2025-11-18T10:30:00.0000000",
    "timeZone": "Asia/Shanghai"
  },
  "organizer": {
    "emailAddress": {
      "name": "Organizer Name",
      "address": "organizer@company.com"
    }
  },
  "attendees": [
    {
      "type": "required",
      "status": {
        "response": "none",
        "time": "0001-01-01T00:00:00Z"
      },
      "emailAddress": {
        "name": "Attendee Name",
        "address": "attendee@company.com"
      }
    }
  ]
}
```

5. **Meeting Types**:
   - "occurrence": Recurring meeting instance (weekly 1:1s, team syncs)
   - "singleInstance": One-time meeting (ad-hoc discussions, customer calls)
   - "exception": Modified recurring instance (reschedule)

6. **Attendees**:
   - Use realistic names and email addresses
   - Conference rooms as type "resource" (e.g., "Conf Rm 5F/Blue", "conf5fblue@company.com")
   - Mix of required/optional attendees
   - External attendees for customer/vendor meetings (@clientcompany.com)

Return ONLY a JSON array of meeting objects. No markdown, no explanations."""

        # Get persona details
        role = persona.demographics.get('function', 'Unknown')
        level = persona.demographics.get('level', 'Unknown')
        company = persona.demographics.get('company', 'Unknown')
        industry = persona.demographics.get('industry', 'Unknown')
        team_size = persona.demographics.get('team_size', 'Unknown')
        weekly_hours = persona.meeting_context.get('weekly_meeting_hours', 'Unknown')
        meeting_breakdown = persona.meeting_context.get('typical_breakdown', {})
        
        user_prompt = f"""Generate a {weeks}-week calendar ({total_meetings} meetings) for this persona:

**Persona Profile:**
- Name: {persona.name}
- Role: {role} at {level} level
- Company: {company} ({industry})
- Team Size: {team_size}
- Weekly Meeting Load: {weekly_hours} hours

**Meeting Context:**
{json.dumps(meeting_breakdown, indent=2)}

**Work Style:**
{persona.work_style}

**Stress Level:**
{persona.stress_level}

**Calendar Period:**
- Start: {start_date.strftime('%Y-%m-%d')} (Monday)
- End: {end_date.strftime('%Y-%m-%d')}
- Total: {weeks} weeks, ~{total_meetings} meetings

**Instructions:**
1. Create recurring meetings (30-40% of total):
   - Weekly 1:1 with manager (e.g., every Monday 10am)
   - Team sync (e.g., every Wednesday 2pm)
   - Other role-specific recurring meetings

2. Fill with ad-hoc meetings (60-70%):
   - Match persona's role (sales: customer calls, IC: design reviews, legal: contract reviews)
   - Realistic subjects and descriptions
   - Appropriate attendees and durations

3. Spread across work hours:
   - 8am-6pm in Asia/Shanghai timezone
   - No late-night meetings (unless emergency)
   - Realistic gaps between meetings

4. Use proper meeting types:
   - "occurrence" for recurring meeting instances
   - "singleInstance" for ad-hoc meetings

Generate {total_meetings} meetings as a JSON array following Microsoft Graph API schema."""

        return system_message, user_prompt
    
    def _apply_persona_rules(
        self,
        meeting: Dict[str, Any],
        persona: PersonaConfig
    ) -> Dict[str, Any]:
        """Apply persona preference rules to label meeting importance and prep needs."""
        
        # Extract meeting details
        subject = meeting.get('subject', '').lower()
        body = meeting.get('bodyPreview', '').lower()
        organizer_email = meeting.get('organizer', {}).get('emailAddress', {}).get('address', '')
        
        # Check attendees
        attendees = meeting.get('attendees', [])
        attendee_emails = [a.get('emailAddress', {}).get('address', '') for a in attendees]
        has_external = any('@' in email and not email.endswith('@company.com') and not email.endswith('@microsoft.com') for email in attendee_emails)
        
        # Combine text for pattern matching
        combined_text = f"{subject} {body}"
        
        # Initialize labels
        importance_label = "medium"  # Default
        prep_needed = False
        prep_time_minutes = 0
        reasoning_parts = []
        
        # Check ALWAYS IMPORTANT patterns (highest priority)
        always_important = persona.importance_criteria.get('always_important', [])
        for pattern in always_important:
            if pattern.lower() in combined_text:
                importance_label = "critical"
                reasoning_parts.append(f"Always important: {pattern}")
        
        # Check USUALLY IMPORTANT patterns
        if importance_label != "critical":
            usually_important = persona.importance_criteria.get('usually_important', [])
            for pattern in usually_important:
                if pattern.lower() in combined_text:
                    importance_label = "high"
                    reasoning_parts.append(f"Usually important: {pattern}")
        
        # Check SOMETIMES IMPORTANT patterns
        if importance_label not in ["critical", "high"]:
            sometimes_important = persona.importance_criteria.get('sometimes_important', [])
            for pattern in sometimes_important:
                if pattern.lower() in combined_text:
                    importance_label = "medium"
                    reasoning_parts.append(f"Sometimes important: {pattern}")
        
        # Check priority framework (active projects/goals)
        for priority in persona.priority_framework:
            priority_name = priority.get('name', '')
            priority_keywords = priority.get('keywords', [])
            for keyword in priority_keywords:
                if keyword.lower() in combined_text:
                    # Boost importance if matches active priority
                    if importance_label == "medium":
                        importance_label = "high"
                    elif importance_label == "low":
                        importance_label = "medium"
                    reasoning_parts.append(f"Matches priority: {priority_name}")
                    break
        
        # Check if prep time needed
        requires_prep = persona.prep_time_needs.get('requires_prep', [])
        for prep_pattern in requires_prep:
            if prep_pattern.lower() in combined_text:
                prep_needed = True
                # Estimate prep time based on importance
                if importance_label == "critical":
                    prep_time_minutes = 60
                elif importance_label == "high":
                    prep_time_minutes = 45
                else:
                    prep_time_minutes = 30
                break
        
        # External attendees often need prep
        if has_external and importance_label in ["critical", "high"]:
            prep_needed = True
            if prep_time_minutes == 0:
                prep_time_minutes = 30
        
        # Add labels to meeting
        meeting['importance_label'] = importance_label
        meeting['prep_needed'] = prep_needed
        meeting['prep_time_minutes'] = prep_time_minutes
        meeting['reasoning'] = "; ".join(reasoning_parts) if reasoning_parts else "Default priority level"
        meeting['persona_id'] = persona.id
        meeting['generation_timestamp'] = datetime.now().isoformat()
        
        return meeting
    
    def export_calendar(
        self,
        meetings: List[Dict[str, Any]],
        output_path: Path,
        format: str = 'jsonl'
    ):
        """Export labeled calendar to file."""
        
        if format == 'jsonl':
            with open(output_path, 'w', encoding='utf-8') as f:
                for meeting in meetings:
                    f.write(json.dumps(meeting) + '\n')
        else:  # json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(meetings, f, indent=2)
        
        logger.info(f"✅ Exported {len(meetings)} meetings to {output_path}")
        
        # Print statistics
        importance_dist = {}
        prep_count = 0
        total_prep_time = 0
        
        for meeting in meetings:
            label = meeting.get('importance_label', 'unknown')
            importance_dist[label] = importance_dist.get(label, 0) + 1
            if meeting.get('prep_needed', False):
                prep_count += 1
                total_prep_time += meeting.get('prep_time_minutes', 0)
        
        logger.info("\nCalendar Statistics:")
        logger.info(f"- Total Meetings: {len(meetings)}")
        logger.info(f"- Importance Distribution:")
        for label in ['critical', 'high', 'medium', 'low']:
            count = importance_dist.get(label, 0)
            pct = (count / len(meetings) * 100) if meetings else 0
            logger.info(f"  {label.capitalize()}: {count} ({pct:.1f}%)")
        logger.info(f"- Prep Needed: {prep_count} ({prep_count/len(meetings)*100:.1f}%)")
        logger.info(f"- Avg Prep Time: {total_prep_time/prep_count:.1f} minutes" if prep_count > 0 else "- Avg Prep Time: 0 minutes")


def load_persona(persona_path: Path) -> PersonaConfig:
    """Load persona from JSON file."""
    with open(persona_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return PersonaConfig.from_json(data)


def load_tier_personas(tier: int) -> List[PersonaConfig]:
    """Load all personas from a specific tier."""
    personas_dir = Path("post_training/data/personas")
    personas = []
    
    for persona_file in personas_dir.glob(f"tier{tier}_*.json"):
        persona = load_persona(persona_file)
        personas.append(persona)
    
    return personas


def main():
    parser = argparse.ArgumentParser(
        description="Generate calendar-based training data using GPT-5"
    )
    
    parser.add_argument(
        '--persona',
        type=Path,
        help='Path to persona JSON file'
    )
    
    parser.add_argument(
        '--tier',
        type=int,
        choices=[1, 2, 3],
        help='Generate calendars for all personas in tier (1, 2, or 3)'
    )
    
    parser.add_argument(
        '--weeks',
        type=int,
        default=4,
        help='Number of weeks to generate (default: 4)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path("post_training/data/training/calendars"),
        help='Output directory for calendar data (default: post_training/data/training/calendars)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'jsonl'],
        default='jsonl',
        help='Export format (default: jsonl)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.persona and not args.tier:
        parser.error("Must specify either --persona or --tier")
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize generator
    generator = CalendarTrainingDataGenerator()
    
    # Load personas
    personas = []
    if args.persona:
        persona = load_persona(args.persona)
        personas.append(persona)
    elif args.tier:
        personas = load_tier_personas(args.tier)
    
    if not personas:
        logger.error(f"No personas found!")
        return
    
    logger.info(f"Loaded {len(personas)} persona(s)")
    
    # Generate calendars for each persona
    for persona in personas:
        logger.info(f"\n{'='*60}")
        
        # Generate calendar
        meetings = generator.generate_calendar(
            persona=persona,
            weeks=args.weeks
        )
        
        if not meetings:
            logger.error(f"Failed to generate calendar for {persona.name}")
            continue
        
        # Export calendar
        output_filename = f"{persona.id}_calendar_{args.weeks}weeks.{args.format}"
        output_path = args.output_dir / output_filename
        
        generator.export_calendar(
            meetings=meetings,
            output_path=output_path,
            format=args.format
        )
    
    logger.info(f"\n{'='*60}")
    logger.info("✅ Calendar generation complete!")


if __name__ == "__main__":
    main()
