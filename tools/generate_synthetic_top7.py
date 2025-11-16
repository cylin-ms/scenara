#!/usr/bin/env python3
"""
Generate Synthetic Training Data from Top 7 Meeting Types

Takes real meetings identified as matching the top 7 types and generates
synthetic variations for post-training data.

Usage:
    python tools/generate_synthetic_top7.py --input data/top7_meetings.json
    python tools/generate_synthetic_top7.py --variations 5 --output post_training/data/training/top7_synthetic.jsonl
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import random

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.llm_api import LLMAPIClient
except ImportError:
    print("ERROR: Could not import LLMAPIClient")
    sys.exit(1)


# Persona definitions for variations
PERSONAS = {
    "executive": {
        "name": "Executive",
        "prep_time_multiplier": 1.2,
        "importance_boost": 0.1,
        "focus": "strategic implications and high-level decisions"
    },
    "senior_manager": {
        "name": "Senior Manager",
        "prep_time_multiplier": 1.0,
        "importance_boost": 0.0,
        "focus": "execution planning and team coordination"
    },
    "individual_contributor": {
        "name": "Individual Contributor",
        "prep_time_multiplier": 0.8,
        "importance_boost": -0.1,
        "focus": "specific deliverables and tactical work"
    }
}


def load_identified_meetings(input_file: Path) -> Dict[str, Any]:
    """Load meetings identified as matching top 7 types."""
    print(f"\n📂 Loading identified meetings from: {input_file}")
    
    if not input_file.exists():
        print(f"❌ Error: File not found: {input_file}")
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    meetings = data.get('meetings', [])
    print(f"✅ Loaded {len(meetings)} meetings")
    
    return data


def generate_persona_variation(
    meeting: Dict[str, Any],
    persona_key: str,
    persona: Dict[str, Any],
    llm_client: LLMAPIClient
) -> Dict[str, Any]:
    """
    Generate a synthetic variation for a specific persona.
    
    Uses LLM to adjust reasoning and prep recommendations based on persona.
    """
    # Get original classification
    classification = meeting.get('_llm_classification', {})
    meeting_type = classification.get('meeting_type', 'Unknown')
    
    # Calculate adjusted prep time
    original_duration = calculate_meeting_duration(meeting)
    base_prep_time = estimate_prep_time(meeting_type, original_duration)
    adjusted_prep_time = int(base_prep_time * persona['prep_time_multiplier'])
    
    # Calculate adjusted importance
    base_confidence = classification.get('confidence', 0.7)
    adjusted_confidence = min(1.0, base_confidence + persona['importance_boost'])
    
    # Generate persona-specific reasoning with LLM
    prompt = f"""Generate preparation reasoning for this meeting from the perspective of a {persona['name']}.

Meeting Type: {meeting_type}
Meeting Subject: {meeting.get('subject', 'No Subject')}
Duration: {original_duration} minutes
Persona Focus: {persona['focus']}
Estimated Prep Time: {adjusted_prep_time} minutes

Generate a brief (2-3 sentences) reasoning for why this meeting requires {adjusted_prep_time} minutes of preparation from a {persona['name']}'s perspective. Focus on {persona['focus']}.

Return only the reasoning text, no JSON or extra formatting."""

    try:
        reasoning = llm_client.query_llm(prompt, provider="ollama", model="gpt-oss:20b")
        reasoning = reasoning.strip()
    except Exception as e:
        print(f"⚠️  LLM reasoning generation failed: {e}")
        reasoning = f"As a {persona['name']}, {adjusted_prep_time} minutes of preparation needed to focus on {persona['focus']}."
    
    # Create synthetic variation
    synthetic = dict(meeting)
    
    # Add training-specific fields
    synthetic['importance_label'] = get_importance_label(adjusted_confidence)
    synthetic['prep_needed'] = True
    synthetic['prep_time_minutes'] = adjusted_prep_time
    synthetic['reasoning'] = reasoning
    synthetic['persona_id'] = persona_key
    synthetic['generation_timestamp'] = datetime.utcnow().isoformat() + "Z"
    
    # Add metadata
    synthetic['_synthetic_metadata'] = {
        'source': 'real_meeting_variation',
        'original_meeting_id': meeting.get('id'),
        'persona': persona['name'],
        'base_prep_time': base_prep_time,
        'prep_time_multiplier': persona['prep_time_multiplier'],
        'base_confidence': base_confidence,
        'confidence_adjustment': persona['importance_boost']
    }
    
    return synthetic


def calculate_meeting_duration(meeting: Dict) -> int:
    """Calculate meeting duration in minutes."""
    try:
        start_str = meeting.get('start', {}).get('dateTime')
        end_str = meeting.get('end', {}).get('dateTime')
        
        if not start_str or not end_str:
            return 60  # Default 1 hour
        
        start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except Exception:
        return 60


def estimate_prep_time(meeting_type: str, duration: int) -> int:
    """
    Estimate base preparation time based on meeting type and duration.
    
    Returns prep time in minutes.
    """
    # Base prep time estimates (in minutes)
    prep_estimates = {
        "Quarterly Business Review (QBR)": 300,  # 5 hours
        "Board of Directors Meeting": 360,  # 6 hours
        "Executive Sales Presentation": 180,  # 3 hours
        "Product Launch Go/No-Go Decision": 240,  # 4 hours
        "Annual SOX 404 Compliance Review": 300,  # 5 hours
        "Quarterly Earnings Call": 360,  # 6 hours
        "M&A Deal Approval (Board)": 480,  # 8 hours
    }
    
    base_prep = prep_estimates.get(meeting_type, 120)
    
    # Adjust based on meeting duration
    if duration > 180:  # > 3 hours
        base_prep = int(base_prep * 1.2)
    elif duration < 60:  # < 1 hour
        base_prep = int(base_prep * 0.8)
    
    return base_prep


def get_importance_label(confidence: float) -> str:
    """Convert confidence score to importance label."""
    if confidence >= 0.9:
        return "critical"
    elif confidence >= 0.7:
        return "high"
    elif confidence >= 0.5:
        return "medium"
    else:
        return "low"


def generate_synthetic_variations(
    meetings: List[Dict],
    variations_per_meeting: int,
    llm_client: LLMAPIClient
) -> List[Dict]:
    """
    Generate synthetic variations for all meetings.
    
    Creates variations for different personas.
    """
    print(f"\n🔄 Generating {variations_per_meeting} variations per meeting...")
    
    synthetic_data = []
    persona_keys = list(PERSONAS.keys())
    
    for i, meeting in enumerate(meetings, 1):
        subject = meeting.get('subject', 'No Subject')
        meeting_type = meeting.get('_llm_classification', {}).get('meeting_type', 'Unknown')
        
        print(f"\n[{i}/{len(meetings)}] {subject[:50]}...")
        print(f"   Type: {meeting_type}")
        
        # Generate variations for different personas
        for j in range(variations_per_meeting):
            persona_key = persona_keys[j % len(persona_keys)]
            persona = PERSONAS[persona_key]
            
            print(f"   [{j+1}/{variations_per_meeting}] Generating {persona['name']} variation...")
            
            variation = generate_persona_variation(meeting, persona_key, persona, llm_client)
            synthetic_data.append(variation)
    
    print(f"\n✅ Generated {len(synthetic_data)} synthetic examples")
    return synthetic_data


def save_synthetic_data(
    synthetic_data: List[Dict],
    output_file: Path,
    eval_split: float = 0.0
):
    """Save synthetic data to JSONL format with optional eval split."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if eval_split > 0:
        # Split into train and eval
        random.shuffle(synthetic_data)
        split_idx = int(len(synthetic_data) * (1 - eval_split))
        train_data = synthetic_data[:split_idx]
        eval_data = synthetic_data[split_idx:]
        
        # Save training data
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in train_data:
                f.write(json.dumps(item) + '\n')
        
        print(f"\n💾 Training data saved: {output_file} ({len(train_data)} examples)")
        
        # Save evaluation data
        eval_file = output_file.parent / f"{output_file.stem}_eval.jsonl"
        with open(eval_file, 'w', encoding='utf-8') as f:
            for item in eval_data:
                f.write(json.dumps(item) + '\n')
        
        print(f"💾 Evaluation data saved: {eval_file} ({len(eval_data)} examples)")
    else:
        # Save all as training data
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in synthetic_data:
                f.write(json.dumps(item) + '\n')
        
        print(f"\n💾 Data saved: {output_file} ({len(synthetic_data)} examples)")
    
    # Save statistics
    stats_file = output_file.parent / f"{output_file.stem}_stats.json"
    stats = generate_statistics(synthetic_data)
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"📊 Statistics saved: {stats_file}")


def generate_statistics(synthetic_data: List[Dict]) -> Dict:
    """Generate statistics for synthetic data."""
    stats = {
        'total_examples': len(synthetic_data),
        'by_meeting_type': {},
        'by_persona': {},
        'by_importance': {},
        'average_prep_time': 0,
        'prep_time_range': {'min': 0, 'max': 0}
    }
    
    if not synthetic_data:
        return stats
    
    prep_times = []
    
    for item in synthetic_data:
        # Count by meeting type
        meeting_type = item.get('_llm_classification', {}).get('meeting_type', 'Unknown')
        stats['by_meeting_type'][meeting_type] = stats['by_meeting_type'].get(meeting_type, 0) + 1
        
        # Count by persona
        persona = item.get('persona_id', 'unknown')
        stats['by_persona'][persona] = stats['by_persona'].get(persona, 0) + 1
        
        # Count by importance
        importance = item.get('importance_label', 'unknown')
        stats['by_importance'][importance] = stats['by_importance'].get(importance, 0) + 1
        
        # Track prep times
        prep_time = item.get('prep_time_minutes', 0)
        prep_times.append(prep_time)
    
    stats['average_prep_time'] = sum(prep_times) / len(prep_times) if prep_times else 0
    stats['prep_time_range']['min'] = min(prep_times) if prep_times else 0
    stats['prep_time_range']['max'] = max(prep_times) if prep_times else 0
    
    return stats


def print_summary(stats: Dict):
    """Print summary statistics."""
    print(f"\n{'='*80}")
    print(f"SYNTHETIC DATA SUMMARY")
    print(f"{'='*80}")
    print(f"Total examples: {stats['total_examples']}")
    
    print(f"\n📊 By Meeting Type:")
    for meeting_type, count in sorted(stats['by_meeting_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {meeting_type}: {count}")
    
    print(f"\n👤 By Persona:")
    for persona, count in sorted(stats['by_persona'].items()):
        print(f"   {persona}: {count}")
    
    print(f"\n🎯 By Importance:")
    for importance, count in sorted(stats['by_importance'].items()):
        print(f"   {importance}: {count}")
    
    print(f"\n⏱️  Prep Time:")
    print(f"   Average: {stats['average_prep_time']:.0f} minutes")
    print(f"   Range: {stats['prep_time_range']['min']}-{stats['prep_time_range']['max']} minutes")
    print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate synthetic training data from top 7 meeting types'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/top7_meetings.json'),
        help='Input file with identified meetings'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('post_training/data/training/top7_synthetic.jsonl'),
        help='Output JSONL file'
    )
    parser.add_argument(
        '--variations',
        type=int,
        default=3,
        help='Number of variations per meeting (default: 3)'
    )
    parser.add_argument(
        '--eval-split',
        type=float,
        default=0.2,
        help='Fraction for evaluation set (0.0-1.0, default: 0.2)'
    )
    
    args = parser.parse_args()
    
    print(f"\n{'='*80}")
    print(f"SYNTHETIC DATA GENERATION - TOP 7 MEETING TYPES")
    print(f"{'='*80}")
    
    # Load identified meetings
    data = load_identified_meetings(args.input)
    meetings = data['meetings']
    
    if not meetings:
        print("❌ No meetings found in input file")
        return 1
    
    # Initialize LLM client
    llm_client = LLMAPIClient()
    
    # Generate synthetic variations
    synthetic_data = generate_synthetic_variations(meetings, args.variations, llm_client)
    
    # Generate statistics
    stats = generate_statistics(synthetic_data)
    
    # Print summary
    print_summary(stats)
    
    # Save data
    save_synthetic_data(synthetic_data, args.output, args.eval_split)
    
    print(f"✅ Complete! Generated {len(synthetic_data)} synthetic examples")
    return 0


if __name__ == '__main__':
    sys.exit(main())
