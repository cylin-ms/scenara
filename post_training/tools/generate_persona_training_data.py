#!/usr/bin/env python3
"""
Persona-Based Training Data Generator using GPT-5

Generates synthetic meeting data for persona-based RLHF training.
Uses Oracle Input Strategy to create labeled training examples pre-launch.

Key Concepts:
- Oracle Personas: Synthetic personas with explicit preference rules
- Meeting Generation: GPT-5 creates realistic meeting scenarios
- Rule Application: Persona rules label importance + prep needed
- Training Export: JSONL format for RLHF/fine-tuning

Usage:
    # From project root
    python post_training/tools/generate_persona_training_data.py --persona post_training/data/personas/tier1_sales_manager_pipeline.json --count 200
    python post_training/tools/generate_persona_training_data.py --tier 1 --count 2400
"""

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directories to path to import from tools/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import GPT-5 infrastructure
try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, DEFAULT_ENDPOINT, DEFAULT_MODEL
except ImportError:
    print("ERROR: Could not import GPT5MeetingClassifier")
    print("Make sure tools/meeting_classifier_gpt5.py is available in project root")
    print("Run this script from project root: python post_training/tools/generate_persona_training_data.py")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PersonaConfig:
    """Oracle persona configuration with explicit preference rules."""
    id: str
    name: str
    tier: int
    demographics: Dict[str, Any]
    meeting_context: Dict[str, Any]
    importance_criteria: Dict[str, List[str]]
    priority_framework: List[Dict[str, Any]]
    rsvp_rules: Dict[str, List[str]]
    prep_time_needs: Dict[str, List[str]]
    work_style: str
    career_stage: str
    stress_level: str
    notes: str
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'PersonaConfig':
        """Load persona from JSON file."""
        return cls(
            id=data.get('id', 'unknown'),
            name=data.get('name', 'Unknown Persona'),
            tier=data.get('tier', 3),
            demographics=data.get('demographics', {}),
            meeting_context=data.get('meeting_context', {}),
            importance_criteria=data.get('importance_criteria', {}),
            priority_framework=data.get('priority_framework', []),
            rsvp_rules=data.get('rsvp_rules', {}),
            prep_time_needs=data.get('prep_time_needs', {}),
            work_style=data.get('work_style', ''),
            career_stage=data.get('career_stage', ''),
            stress_level=data.get('stress_level', ''),
            notes=data.get('notes', '')
        )


@dataclass
class SyntheticMeeting:
    """Synthetic meeting with persona-based labels."""
    meeting_id: str
    subject: str
    organizer: str
    attendees: List[str]
    start_time: str
    duration_minutes: int
    location: str
    body_preview: str
    importance_label: str  # "critical", "high", "medium", "low"
    prep_needed: bool
    prep_time_minutes: int
    reasoning: str
    persona_id: str
    generation_timestamp: str


class PersonaTrainingDataGenerator:
    """
    Generate synthetic training data using Oracle Input Strategy.
    
    Key Features:
    - GPT-5 generates realistic meeting scenarios
    - Persona rules provide ground truth labels
    - Exports JSONL format for RLHF training
    - Supports tier-based generation
    """
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        endpoint: str = DEFAULT_ENDPOINT,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """
        Initialize training data generator.
        
        Args:
            model: GPT-5 model name (default: dev-gpt-5-chat-jj)
            endpoint: SilverFlow API endpoint
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.model = model
        self.endpoint = endpoint
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize GPT-5 client using established pattern
        self.gpt5_client = GPT5MeetingClassifier(
            model=model,
            endpoint=endpoint,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info(f"Initialized Persona Training Data Generator with model: {model}")
    
    def _create_meeting_generation_prompt(self, persona: PersonaConfig, count: int) -> str:
        """
        Create GPT-5 prompt to generate synthetic meetings for persona.
        
        Args:
            persona: Persona configuration with preference rules
            count: Number of meetings to generate
            
        Returns:
            System message and user prompt for GPT-5
        """
        system_message = """You are an enterprise meeting data generator. Generate realistic meeting scenarios that match the given persona's typical work experience.

IMPORTANT: Generate meetings in Microsoft Graph API calendar format to match real meeting extraction data.

Each meeting MUST follow this exact schema:
{
  "id": "unique_meeting_id",
  "subject": "Meeting title",
  "bodyPreview": "1-2 sentence meeting description with agenda/context",
  "showAs": "busy" (or "tentative", "free", "oof", "workingElsewhere"),
  "type": "singleInstance" (or "occurrence", "exception", "seriesMaster"),
  "responseStatus": {
    "response": "organizer" (or "accepted", "declined", "tentativelyAccepted", "notResponded"),
    "time": "0001-01-01T00:00:00Z"
  },
  "start": {
    "dateTime": "2025-11-15T10:00:00.0000000",
    "timeZone": "Asia/Shanghai"
  },
  "end": {
    "dateTime": "2025-11-15T11:00:00.0000000",
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
      "type": "required" (or "optional", "resource"),
      "status": {
        "response": "none" (or "accepted", "declined", "tentativelyAccepted"),
        "time": "0001-01-01T00:00:00Z"
      },
      "emailAddress": {
        "name": "Attendee Name",
        "address": "attendee@company.com"
      }
    }
  ]
}

Meeting types:
- singleInstance: One-time meeting
- occurrence: Instance of recurring meeting
- exception: Modified instance of recurring series
- seriesMaster: Recurring meeting template

Generate meetings that:
1. Reflect the persona's organizational level and functional role
2. Match their typical meeting load and work patterns
3. Include realistic variety (team meetings, 1:1s, project discussions, client calls, etc.)
4. Have authentic subject lines and descriptions
5. Include appropriate mix of internal and external attendees (2-15 attendees)
6. Use realistic email addresses (@microsoft.com, @company.com, @client.com)
7. Conference rooms should have type "resource" (e.g., "Conf Rm Building/Room")

Return ONLY a JSON array of meeting objects. No additional text."""

        user_prompt = f"""Generate {count} realistic meeting scenarios for this persona:

**Persona Profile:**
- Name: {persona.name}
- Role: {persona.demographics.get('function', 'Unknown')} at {persona.demographics.get('level', 'Unknown')} level
- Company: {persona.demographics.get('company', 'Unknown')} ({persona.demographics.get('industry', 'Unknown')})
- Team Size: {persona.demographics.get('team_size', 'Unknown')}
- Tenure: {persona.demographics.get('tenure', 'Unknown')}

**Meeting Context:**
- Weekly Meeting Load: {persona.meeting_context.get('weekly_meeting_hours', 'Unknown')} hours
- Typical Breakdown: {json.dumps(persona.meeting_context.get('typical_breakdown', {}))}

**Work Style:**
{persona.work_style}

**Career Stage:**
{persona.career_stage}

**Stress Level:**
{persona.stress_level}

Generate {count} meetings as a JSON array following Microsoft Graph API calendar schema:
[
  {{
    "id": "unique_id_string",
    "subject": "Meeting title",
    "bodyPreview": "Meeting description with context",
    "showAs": "busy",
    "type": "singleInstance",
    "responseStatus": {{
      "response": "organizer",
      "time": "0001-01-01T00:00:00Z"
    }},
    "start": {{
      "dateTime": "2025-11-15T10:00:00.0000000",
      "timeZone": "Asia/Shanghai"
    }},
    "end": {{
      "dateTime": "2025-11-15T11:00:00.0000000",
      "timeZone": "Asia/Shanghai"
    }},
    "organizer": {{
      "emailAddress": {{
        "name": "Organizer Name",
        "address": "organizer@company.com"
      }}
    }},
    "attendees": [
      {{
        "type": "required",
        "status": {{
          "response": "none",
          "time": "0001-01-01T00:00:00Z"
        }},
        "emailAddress": {{
          "name": "Attendee Name",
          "address": "attendee@company.com"
        }}
      }}
    ]
  }}
]

Ensure meetings:
- Match persona's role-specific patterns (e.g., sales calls for Sales Manager)
- Include realistic attendee names and email addresses
- Use appropriate meeting types (singleInstance for one-time, occurrence for recurring)
- Have proper start/end times with Asia/Shanghai timezone
- Include conference rooms as "resource" type attendees when relevant"""

        return system_message, user_prompt
    
    def _apply_persona_rules(
        self,
        meeting: Dict[str, Any],
        persona: PersonaConfig
    ) -> Dict[str, Any]:
        """
        Apply persona preference rules to label meeting importance and prep needs.
        
        This implements the Oracle Input Strategy - persona rules provide ground truth.
        
        Args:
            meeting: Generated meeting data (Microsoft Graph API format)
            persona: Persona with explicit preference rules
            
        Returns:
            Meeting with labels: importance_label, prep_needed, prep_time_minutes, reasoning
        """
        subject = meeting.get('subject', '').lower()
        body = meeting.get('bodyPreview', '').lower()
        attendees = meeting.get('attendees', [])
        
        # Extract attendee count (excluding resources like conference rooms)
        attendee_count = len([a for a in attendees if a.get('type') != 'resource'])
        
        # Initialize scores
        importance_score = 0
        prep_needed = False
        prep_time = 0
        reasons = []
        
        # Check importance criteria (from persona.importance_criteria)
        criteria = persona.importance_criteria
        
        # Always important patterns
        for pattern in criteria.get('always_important', []):
            if pattern.lower() in subject or pattern.lower() in body:
                importance_score += 4
                reasons.append(f"Always important: {pattern}")
        
        # Usually important patterns
        for pattern in criteria.get('usually_important', []):
            if pattern.lower() in subject or pattern.lower() in body:
                importance_score += 3
                reasons.append(f"Usually important: {pattern}")
        
        # Sometimes important patterns
        for pattern in criteria.get('sometimes_important', []):
            if pattern.lower() in subject or pattern.lower() in body:
                importance_score += 2
                reasons.append(f"Sometimes important: {pattern}")
        
        # Rarely important patterns
        for pattern in criteria.get('rarely_important', []):
            if pattern.lower() in subject or pattern.lower() in body:
                importance_score += 1
                reasons.append(f"Rarely important: {pattern}")
        
        # Check priority framework (specific priorities with time commitments)
        for priority in persona.priority_framework:
            priority_name = priority.get('name', '')
            keywords = priority.get('keywords', [])
            for keyword in keywords:
                if keyword.lower() in subject or keyword.lower() in body:
                    importance_score += 3
                    reasons.append(f"Matches priority: {priority_name}")
        
        # Check prep time needs (from persona.prep_time_needs)
        prep_rules = persona.prep_time_needs
        
        # Requires prep patterns
        for pattern in prep_rules.get('requires_prep', []):
            if pattern.lower() in subject or pattern.lower() in body:
                prep_needed = True
                prep_time = max(prep_time, 30)
                reasons.append(f"Requires prep: {pattern}")
        
        # Optional prep patterns
        for pattern in prep_rules.get('optional_prep', []):
            if pattern.lower() in subject or pattern.lower() in body:
                if importance_score >= 3:  # Only if important enough
                    prep_needed = True
                    prep_time = max(prep_time, 15)
                    reasons.append(f"Optional prep (important meeting): {pattern}")
        
        # Determine final importance label
        if importance_score >= 4:
            importance_label = "critical"
        elif importance_score >= 3:
            importance_label = "high"
        elif importance_score >= 2:
            importance_label = "medium"
        else:
            importance_label = "low"
        
        # Add labels to meeting (following Graph API pattern - add custom fields)
        meeting['importance_label'] = importance_label
        meeting['prep_needed'] = prep_needed
        meeting['prep_time_minutes'] = prep_time
        meeting['reasoning'] = "; ".join(reasons) if reasons else "No specific patterns matched"
        meeting['persona_id'] = persona.id
        meeting['generation_timestamp'] = datetime.now().isoformat()
        
        return meeting
    
    def generate_meetings_for_persona(
        self,
        persona: PersonaConfig,
        count: int = 200,
        batch_size: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Generate synthetic meetings for a persona using GPT-5.
        
        Args:
            persona: Persona configuration
            count: Total number of meetings to generate
            batch_size: Number of meetings per GPT-5 call (to avoid rate limits)
            
        Returns:
            List of labeled synthetic meetings
        """
        logger.info(f"Generating {count} meetings for persona: {persona.name} (Tier {persona.tier})")
        
        all_meetings = []
        batches = (count + batch_size - 1) // batch_size
        
        for batch_num in range(batches):
            batch_count = min(batch_size, count - len(all_meetings))
            logger.info(f"Batch {batch_num + 1}/{batches}: Generating {batch_count} meetings...")
            
            # Create GPT-5 prompt
            system_message, user_prompt = self._create_meeting_generation_prompt(persona, batch_count)
            
            # Call GPT-5 using established pattern
            result = self.gpt5_client._call_gpt5_api(
                system_message=system_message,
                user_prompt=user_prompt,
                timeout=60
            )
            
            if not result.success:
                logger.error(f"GPT-5 call failed: {result.error}")
                continue
            
            # Parse JSON response
            try:
                response_text = result.response_content
                # Clean markdown code blocks if present
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                meetings = json.loads(response_text)
                
                if not isinstance(meetings, list):
                    logger.error(f"Expected list, got {type(meetings)}")
                    continue
                
                # Apply persona rules to label each meeting
                labeled_meetings = []
                for meeting in meetings:
                    labeled_meeting = self._apply_persona_rules(meeting, persona)
                    labeled_meetings.append(labeled_meeting)
                
                all_meetings.extend(labeled_meetings)
                logger.info(f"Generated and labeled {len(labeled_meetings)} meetings (Total: {len(all_meetings)}/{count})")
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse GPT-5 response as JSON: {e}")
                logger.debug(f"Response: {result.response_content[:500]}")
                continue
            
            # Rate limiting
            time.sleep(self.retry_delay)
        
        logger.info(f"✅ Generated {len(all_meetings)} meetings for {persona.name}")
        return all_meetings
    
    def export_training_data(
        self,
        meetings: List[Dict[str, Any]],
        output_file: Path,
        format: str = "jsonl"
    ) -> None:
        """
        Export labeled meetings as training data.
        
        Args:
            meetings: List of labeled synthetic meetings
            output_file: Output file path
            format: Export format ("jsonl" or "json")
        """
        logger.info(f"Exporting {len(meetings)} meetings to {output_file} ({format} format)")
        
        if format == "jsonl":
            with open(output_file, 'w', encoding='utf-8') as f:
                for meeting in meetings:
                    f.write(json.dumps(meeting, ensure_ascii=False) + '\n')
        else:  # json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(meetings, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Exported to {output_file}")
    
    def generate_statistics(self, meetings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate statistics about the synthetic training data.
        
        Args:
            meetings: List of labeled meetings
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_meetings': len(meetings),
            'importance_distribution': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'prep_needed_count': 0,
            'avg_prep_time_minutes': 0,
            'personas': set()
        }
        
        total_prep_time = 0
        
        for meeting in meetings:
            # Importance distribution
            importance = meeting.get('importance_label', 'low')
            stats['importance_distribution'][importance] += 1
            
            # Prep needed
            if meeting.get('prep_needed', False):
                stats['prep_needed_count'] += 1
                total_prep_time += meeting.get('prep_time_minutes', 0)
            
            # Persona tracking
            stats['personas'].add(meeting.get('persona_id', 'unknown'))
        
        # Calculate averages
        if stats['prep_needed_count'] > 0:
            stats['avg_prep_time_minutes'] = total_prep_time / stats['prep_needed_count']
        
        stats['personas'] = len(stats['personas'])
        
        return stats


def load_tier_personas(tier: int, persona_dir: Path = Path("post_training/data/personas")) -> List[PersonaConfig]:
    """
    Load all personas for a specific tier.
    
    Args:
        tier: Tier number (1, 2, or 3)
        persona_dir: Directory containing persona JSON files
        
    Returns:
        List of PersonaConfig objects
    """
    personas = []
    
    if not persona_dir.exists():
        logger.error(f"Persona directory not found: {persona_dir}")
        return personas
    
    # Look for tier-specific files
    pattern = f"tier{tier}_*.json"
    persona_files = list(persona_dir.glob(pattern))
    
    logger.info(f"Found {len(persona_files)} persona files for Tier {tier}")
    
    for persona_file in persona_files:
        try:
            with open(persona_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                persona = PersonaConfig.from_json(data)
                personas.append(persona)
                logger.info(f"Loaded persona: {persona.name}")
        except Exception as e:
            logger.error(f"Failed to load {persona_file}: {e}")
    
    return personas


def main():
    parser = argparse.ArgumentParser(
        description="Generate persona-based training data using GPT-5"
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
        help='Generate for all personas in tier (1, 2, or 3)'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=200,
        help='Number of meetings to generate per persona (default: 200)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path("post_training/data/training"),
        help='Output directory for training data (default: post_training/data/training)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'jsonl'],
        default='jsonl',
        help='Export format (default: jsonl)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=20,
        help='Number of meetings per GPT-5 call (default: 20)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.persona and not args.tier:
        parser.error("Must specify either --persona or --tier")
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize generator
    generator = PersonaTrainingDataGenerator()
    
    # Load personas
    personas = []
    if args.persona:
        with open(args.persona, 'r', encoding='utf-8') as f:
            data = json.load(f)
            persona = PersonaConfig.from_json(data)
            personas.append(persona)
    elif args.tier:
        personas = load_tier_personas(args.tier)
    
    if not personas:
        logger.error("No personas loaded. Exiting.")
        return 1
    
    logger.info(f"Loaded {len(personas)} personas")
    
    # Generate training data for each persona
    all_meetings = []
    for persona in personas:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {persona.name} (Tier {persona.tier})")
        logger.info(f"{'='*60}")
        
        meetings = generator.generate_meetings_for_persona(
            persona=persona,
            count=args.count,
            batch_size=args.batch_size
        )
        
        all_meetings.extend(meetings)
        
        # Export per-persona file
        persona_output = args.output_dir / f"{persona.id}_meetings.{args.format}"
        generator.export_training_data(meetings, persona_output, args.format)
    
    # Export combined file
    if args.tier:
        combined_output = args.output_dir / f"tier{args.tier}_combined.{args.format}"
        generator.export_training_data(all_meetings, combined_output, args.format)
    
    # Generate and display statistics
    stats = generator.generate_statistics(all_meetings)
    logger.info(f"\n{'='*60}")
    logger.info("Training Data Statistics")
    logger.info(f"{'='*60}")
    logger.info(f"Total Meetings: {stats['total_meetings']}")
    logger.info(f"Personas: {stats['personas']}")
    logger.info(f"Importance Distribution:")
    for level, count in stats['importance_distribution'].items():
        pct = (count / stats['total_meetings'] * 100) if stats['total_meetings'] > 0 else 0
        logger.info(f"  {level.capitalize()}: {count} ({pct:.1f}%)")
    logger.info(f"Prep Needed: {stats['prep_needed_count']} ({stats['prep_needed_count']/stats['total_meetings']*100:.1f}%)")
    logger.info(f"Avg Prep Time: {stats['avg_prep_time_minutes']:.1f} minutes")
    
    # Export statistics
    stats_output = args.output_dir / f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(stats_output, 'w', encoding='utf-8') as f:
        # Convert set to int for JSON serialization
        stats_copy = stats.copy()
        json.dump(stats_copy, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✅ Training data generation complete!")
    logger.info(f"Output directory: {args.output_dir}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
