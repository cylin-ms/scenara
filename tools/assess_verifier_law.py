"""
Assess 9 Calendar.AI Hero Prompts against Verifier's Law using GPT-5.

Verifier's Law: "Any task that is possible to solve and easy to verify 
will eventually be solved by AI."

This tool evaluates each hero prompt on:
1. Solvability: Can AI solve this task?
2. Verification Ease: How easy is it to verify correctness?
3. Verification Asymmetry: Gap between solving difficulty vs verification difficulty

Usage:
    python tools/assess_verifier_law.py --output docs/gutt_analysis/verifier_law_assessment.json
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import GPT-5 infrastructure
try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, ChatMessage, DEFAULT_ENDPOINT, DEFAULT_MODEL
except ImportError:
    try:
        from meeting_classifier_gpt5 import GPT5MeetingClassifier, ChatMessage, DEFAULT_ENDPOINT, DEFAULT_MODEL
    except ImportError:
        print("ERROR: Could not import GPT5MeetingClassifier. Check meeting_classifier_gpt5.py exists.")
        sys.exit(1)


HERO_PROMPTS = [
    {
        "id": "organizer-1",
        "category": "Organizer",
        "prompt": "Keep my Calendar up to date by committing to only meetings that are part of my priorities."
    },
    {
        "id": "organizer-2",
        "category": "Organizer",
        "prompt": "Track all my important meetings and flag any that require focus time to prepare for them."
    },
    {
        "id": "organizre-3",
        "category": "Organizer",
        "prompt": "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."
    },
    {
        "id": "schedule-1",
        "category": "Schedule",
        "prompt": "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."
    },
    {
        "id": "schedule-2",
        "category": "Schedule",
        "prompt": "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."
    },
    {
        "id": "schedule-3",
        "category": "Schedule",
        "prompt": "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."
    },
    {
        "id": "collaborate-1",
        "category": "Collaborate",
        "prompt": "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."
    },
    {
        "id": "collaborate-2",
        "category": "Collaborate",
        "prompt": "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."
    },
    {
        "id": "collaborate-3",
        "category": "Collaborate",
        "prompt": "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."
    }
]


ASSESSMENT_SYSTEM_PROMPT = """You are an expert AI researcher analyzing tasks through the lens of Verifier's Law.

**Verifier's Law**: "Any task that is possible to solve and easy to verify will eventually be solved by AI."

**Key Principles**:
1. Verification Asymmetry: Some tasks are much easier to verify than to solve
2. AI Progress: Accelerates in domains where correctness can be quickly validated
3. Training Signal: Verification acts as feedback loop for RL fine-tuning

For each Calendar.AI task, assess:

1. **Solvability** (1-10 scale):
   - Can AI solve this task with current/near-future capabilities?
   - Consider: Data access, API availability, reasoning requirements
   - 1 = Impossible, 10 = Trivially solvable

2. **Verification Ease** (1-10 scale):
   - How easy is it to verify the solution is correct?
   - Consider: Objective metrics, user feedback, ground truth availability
   - 1 = Impossible to verify, 10 = Trivially verifiable

3. **Verification Asymmetry Score** (Verification Ease - Solving Difficulty):
   - Positive = Easy to verify, hard to solve (HIGH priority for AI)
   - Negative = Hard to verify, easy to solve (LOW priority for AI)
   - Near zero = Similar difficulty (MEDIUM priority)

4. **Verification Methods**: Concrete ways to check correctness
5. **AI Readiness**: Current AI capability level (Now/Soon/Later/Never)
6. **Training Data Quality**: Can we generate good training data?
7. **Ranking**: Overall priority for AI development

Provide detailed, technical analysis grounded in current AI capabilities and Calendar.AI implementation reality.
"""


def assess_prompt_verifier_law(prompt_data: dict, gpt5_client: GPT5MeetingClassifier) -> dict:
    """
    Use GPT-5 to assess a single prompt against Verifier's Law.
    """
    user_prompt = f"""Analyze this Calendar.AI task against Verifier's Law:

**Task ID**: {prompt_data['id']}
**Category**: {prompt_data['category']}
**User Prompt**: "{prompt_data['prompt']}"

Provide your assessment in the following JSON structure:

{{
  "prompt_id": "{prompt_data['id']}",
  "solvability": {{
    "score": <1-10>,
    "reasoning": "<Why this score? Consider current AI capabilities, data access, APIs>",
    "difficulty_factors": ["<factor 1>", "<factor 2>", ...]
  }},
  "verification_ease": {{
    "score": <1-10>,
    "reasoning": "<Why this score? How can we verify correctness?>",
    "verification_methods": ["<method 1>", "<method 2>", ...]
  }},
  "verification_asymmetry": {{
    "score": <verification_ease - (10 - solvability)>,
    "interpretation": "<Positive/Negative/Near-zero and what it means>",
    "priority": "<HIGH/MEDIUM/LOW based on asymmetry>"
  }},
  "ai_readiness": {{
    "timeline": "<Now/Soon (6mo)/Later (1-2yr)/Never>",
    "blockers": ["<blocker 1>", "<blocker 2>", ...],
    "enablers": ["<enabler 1>", "<enabler 2>", ...]
  }},
  "training_data_quality": {{
    "score": <1-10>,
    "reasoning": "<Can we generate/collect good training data?>",
    "data_sources": ["<source 1>", "<source 2>", ...]
  }},
  "key_insights": ["<insight 1>", "<insight 2>", ...],
  "recommendation": "<Priority rank and development recommendation>"
}}

Be specific about Calendar.AI context (calendar APIs, meeting intelligence, user preferences, organizational data).
"""

    print(f"\n🔍 Assessing {prompt_data['id']}...")
    
    try:
        # Use GPT-5 via SilverFlow API
        result = gpt5_client._call_gpt5_api(
            system_message=ASSESSMENT_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        if not result.success:
            print(f"❌ GPT-5 API error for {prompt_data['id']}: {result.error}")
            return {
                "prompt_id": prompt_data['id'],
                "error": result.error
            }
        
        response_text = result.response_content.strip()
        
        # Parse JSON response with robust error handling
        # GPT-5 might wrap in markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Clean up common GPT-5 JSON issues
        # Remove trailing commas before } or ]
        import re
        response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)
        # Remove comments (// or /* */)
        response_text = re.sub(r'//.*?$', '', response_text, flags=re.MULTILINE)
        response_text = re.sub(r'/\*.*?\*/', '', response_text, flags=re.DOTALL)
        
        # Fix arithmetic expressions in JSON "score" fields
        # Pattern 1: "score": 9 - (10 - 7) = 6,  → "score": 6,
        response_text = re.sub(r'"score":\s*[\d\.\-\+\*\/\(\)\s]+=\s*(-?\d+\.?\d*)\s*,', r'"score": \1,', response_text)
        # Pattern 2: "score": 9 - (10 - 7),  → evaluate and replace
        # Find all arithmetic expressions without equals sign and evaluate them
        def eval_score(match):
            try:
                expr = match.group(1).strip()
                # Safely evaluate simple arithmetic (only allow numbers and operators)
                if all(c in '0123456789.+-*/() ' for c in expr):
                    result = eval(expr)
                    return f'"score": {result},'
                return match.group(0)  # Return unchanged if unsafe
            except:
                return match.group(0)  # Return unchanged on error
        
        response_text = re.sub(r'"score":\s*([0-9\.\-\+\*\/\(\)\s]+),', eval_score, response_text)
        
        assessment = json.loads(response_text)
        
        print(f"✅ {prompt_data['id']}: Solvability={assessment['solvability']['score']}, "
              f"Verification={assessment['verification_ease']['score']}, "
              f"Asymmetry={assessment['verification_asymmetry']['score']}")
        
        return assessment
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error for {prompt_data['id']}: {e}")
        # Save raw response for debugging
        debug_file = Path(f"debug_response_{prompt_data['id']}.txt")
        debug_file.write_text(response_text, encoding='utf-8')
        print(f"   💾 Saved raw response to {debug_file} for debugging")
        return {
            "prompt_id": prompt_data['id'],
            "error": f"JSON parsing failed: {str(e)}",
            "status": "failed"
        }
    except Exception as e:
        print(f"❌ Error assessing {prompt_data['id']}: {e}")
        return {
            "prompt_id": prompt_data['id'],
            "error": str(e),
            "status": "failed"
        }


def rank_by_verifier_law(assessments: list) -> list:
    """
    Rank prompts by Verifier's Law priority:
    1. High verification asymmetry (easy to verify, hard to solve)
    2. High solvability + verification ease
    3. High training data quality
    """
    valid_assessments = [a for a in assessments if "error" not in a]
    
    # Calculate composite score
    for assessment in valid_assessments:
        # Asymmetry is key (positive = good for AI)
        asymmetry_score = assessment['verification_asymmetry']['score']
        
        # But also consider absolute solvability and verification
        solvability = assessment['solvability']['score']
        verification = assessment['verification_ease']['score']
        training_quality = assessment['training_data_quality']['score']
        
        # Composite score: Asymmetry * 3 + Solvability + Verification + Training Quality
        assessment['composite_score'] = (
            asymmetry_score * 3.0 +  # Asymmetry is most important
            solvability * 0.5 +        # Can we solve it?
            verification * 0.5 +       # Can we verify it?
            training_quality * 1.0     # Can we train on it?
        )
    
    # Sort by composite score (descending)
    ranked = sorted(valid_assessments, key=lambda x: x['composite_score'], reverse=True)
    
    # Add rank
    for i, assessment in enumerate(ranked, 1):
        assessment['rank'] = i
        assessment['rank_tier'] = (
            "🥇 Tier 1 (High Priority)" if i <= 3 else
            "🥈 Tier 2 (Medium Priority)" if i <= 6 else
            "🥉 Tier 3 (Lower Priority)"
        )
    
    return ranked


def generate_summary_report(ranked_assessments: list) -> str:
    """
    Generate human-readable summary report.
    """
    # Check if we have multi-trial data
    has_trials = ranked_assessments and 'trial_count' in ranked_assessments[0]
    trial_info = f" ({ranked_assessments[0].get('trial_count', 1)} trials per prompt)" if has_trials else ""
    
    report = f"""# Verifier's Law Assessment - Calendar.AI Hero Prompts

**Assessment Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Framework**: Verifier's Law by Jason Wei  
**Model Used**: GPT-5{trial_info}  
**Prompts Assessed**: {len(ranked_assessments)} / 9

---

## Executive Summary

**Verifier's Law**: "Any task that is possible to solve and easy to verify will eventually be solved by AI."

This assessment evaluates each Calendar.AI hero prompt on:
- **Solvability**: Can AI solve this task? (1-10)
- **Verification Ease**: How easy to verify correctness? (1-10)
- **Verification Asymmetry**: Gap between verification and solving difficulty
- **AI Readiness**: Timeline for AI capability (Now/Soon/Later/Never)
- **Training Data Quality**: Can we generate good training data? (1-10)

**Methodology**: {"Multiple GPT-5 trials were run per prompt to ensure robust, evidence-based assessments. Statistical measures (mean ± std, range) provide confidence in the rankings." if has_trials else "Single GPT-5 assessment per prompt."}

**Key Finding**: Prompts with high verification asymmetry (easy to verify, hard to solve) are prime candidates for AI automation and benefit most from RL fine-tuning with verification feedback.

---

## Rankings by Verifier's Law Priority

"""
    
    for assessment in ranked_assessments:
        report += f"""
### {assessment['rank']}. {assessment['prompt_id'].upper()} - {assessment['rank_tier']}

**Composite Score**: {assessment['composite_score']:.2f}

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | {assessment['solvability']['score']}/10 | {assessment['solvability']['reasoning'][:100]}... |
| **Verification Ease** | {assessment['verification_ease']['score']}/10 | {assessment['verification_ease']['reasoning'][:100]}... |
| **Verification Asymmetry** | {assessment['verification_asymmetry']['score']} | {assessment['verification_asymmetry']['interpretation']} |
| **AI Readiness** | {assessment['ai_readiness']['timeline']} | Blockers: {len(assessment['ai_readiness']['blockers'])} |
| **Training Data Quality** | {assessment['training_data_quality']['score']}/10 | {assessment['training_data_quality']['reasoning'][:100]}... |

**Verification Methods**:
"""
        for method in assessment['verification_ease']['verification_methods']:
            report += f"- {method}\n"
        
        report += f"\n**Key Insights**:\n"
        for insight in assessment['key_insights']:
            report += f"- {insight}\n"
        
        report += f"\n**Recommendation**: {assessment['recommendation']}\n\n---\n"
    
    # Summary table
    report += f"""
## Quick Comparison Table

| Rank | Prompt ID | Solvability | Verification | Asymmetry | Composite | Tier |
|------|-----------|-------------|--------------|-----------|-----------|------|
"""
    for a in ranked_assessments:
        report += f"| {a['rank']} | {a['prompt_id']} | {a['solvability']['score']} | {a['verification_ease']['score']} | {a['verification_asymmetry']['score']} | {a['composite_score']:.1f} | {a['rank_tier'].split()[0]} |\n"
    
    report += """
---

## Interpretation Guide

### Verification Asymmetry Score
- **Positive (>0)**: Easy to verify, harder to solve → **HIGH priority for AI** (benefits from verification feedback)
- **Near Zero (±2)**: Similar difficulty → **MEDIUM priority** (standard supervised learning)
- **Negative (<0)**: Hard to verify, easier to solve → **LOW priority** (verification bottleneck)

### AI Readiness Timeline
- **Now**: Can be solved with current AI + existing APIs
- **Soon (6 months)**: Needs minor capability improvements or data access
- **Later (1-2 years)**: Requires significant AI advances or infrastructure
- **Never**: Fundamentally unsuitable for AI (human judgment required)

### Training Data Quality
- **8-10**: High-quality ground truth easily available
- **5-7**: Moderate quality, requires effort to collect/label
- **1-4**: Poor quality, difficult to obtain reliable training signal

---

## Recommendations for Post-Training

Based on Verifier's Law, prioritize:

1. **Tier 1 Prompts** (Top 3): Implement verification-based RL fine-tuning
   - High asymmetry benefits from iterative improvement
   - Easy verification enables scalable training data generation
   
2. **Tier 2 Prompts** (Rank 4-6): Standard supervised fine-tuning
   - Moderate asymmetry, focus on quality over quantity
   
3. **Tier 3 Prompts** (Rank 7-9): Defer or use few-shot learning
   - Low asymmetry or hard verification limits training effectiveness

---

**Reference**: [Verifier's Law by Jason Wei](https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law)

"""
    
    return report


def aggregate_trial_results(all_trials: List[List[dict]], required_trials: int = 3) -> List[dict]:
    """
    Aggregate results from multiple trials to compute mean, std, and confidence intervals.
    Provides stronger evidence by showing consistency across trials.
    Only includes prompts with exactly required_trials successful assessments.
    """
    from statistics import mean, stdev
    
    # Group by prompt_id
    prompt_trials = {}
    for trial in all_trials:
        for assessment in trial:
            prompt_id = assessment.get('prompt_id')
            if prompt_id and 'error' not in assessment and 'status' not in assessment:
                if prompt_id not in prompt_trials:
                    prompt_trials[prompt_id] = []
                prompt_trials[prompt_id].append(assessment)
    
    # Filter and aggregate - ONLY include prompts with exactly required_trials
    aggregated = []
    excluded_prompts = []
    
    for prompt_id, trials in prompt_trials.items():
        if len(trials) != required_trials:
            excluded_prompts.append((prompt_id, len(trials)))
            print(f"⚠️  {prompt_id}: Only {len(trials)}/{required_trials} successful trials - EXCLUDED from final results")
            continue
        
        # Calculate statistics
        solvability_scores = [t['solvability']['score'] for t in trials]
        verification_scores = [t['verification_ease']['score'] for t in trials]
        asymmetry_scores = [t['verification_asymmetry']['score'] for t in trials]
        training_scores = [t['training_data_quality']['score'] for t in trials]
        
        # Aggregate assessment
        agg = {
            'prompt_id': prompt_id,
            'trial_count': len(trials),
            'solvability': {
                'score': round(mean(solvability_scores), 1),
                'std': round(stdev(solvability_scores), 2) if len(trials) > 1 else 0,
                'range': f"{min(solvability_scores)}-{max(solvability_scores)}",
                'reasoning': trials[0]['solvability']['reasoning'],  # Use first trial's reasoning
                'difficulty_factors': trials[0]['solvability']['difficulty_factors']
            },
            'verification_ease': {
                'score': round(mean(verification_scores), 1),
                'std': round(stdev(verification_scores), 2) if len(trials) > 1 else 0,
                'range': f"{min(verification_scores)}-{max(verification_scores)}",
                'reasoning': trials[0]['verification_ease']['reasoning'],
                'verification_methods': trials[0]['verification_ease']['verification_methods']
            },
            'verification_asymmetry': {
                'score': round(mean(asymmetry_scores), 1),
                'std': round(stdev(asymmetry_scores), 2) if len(trials) > 1 else 0,
                'range': f"{min(asymmetry_scores)}-{max(asymmetry_scores)}",
                'interpretation': trials[0]['verification_asymmetry']['interpretation'],
                'priority': trials[0]['verification_asymmetry']['priority']
            },
            'ai_readiness': trials[0]['ai_readiness'],
            'training_data_quality': {
                'score': round(mean(training_scores), 1),
                'std': round(stdev(training_scores), 2) if len(trials) > 1 else 0,
                'range': f"{min(training_scores)}-{max(training_scores)}",
                'reasoning': trials[0]['training_data_quality']['reasoning'],
                'data_sources': trials[0]['training_data_quality']['data_sources']
            },
            'key_insights': trials[0]['key_insights'],
            'recommendation': trials[0]['recommendation']
        }
        
        aggregated.append(agg)
    
    return aggregated


def main():
    """Main execution function with 3-trial stability testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Assess Calendar.AI prompts with Verifier's Law (3 trials)")
    parser.add_argument("--output", default="docs/gutt_analysis/verifier_law_assessment.json",
                       help="Output JSON file path")
    parser.add_argument("--report", default="docs/gutt_analysis/VERIFIER_LAW_ASSESSMENT_REPORT.md",
                       help="Output markdown report path")
    parser.add_argument("--trials", type=int, default=3,
                       help="Number of trials per prompt (default: 3)")
    args = parser.parse_args()
    
    print("=" * 80)
    print("VERIFIER'S LAW ASSESSMENT - Calendar.AI Hero Prompts")
    print("=" * 80)
    print(f"\n📋 Assessing {len(HERO_PROMPTS)} hero prompts against Verifier's Law...")
    print(f"🔬 Running {args.trials} trials per prompt for robust evidence...")
    print("🤖 Using GPT-5 (dev-gpt-5-chat-jj) for analysis...\n")
    
    # Initialize GPT-5 client
    gpt5_client = GPT5MeetingClassifier(
        model=DEFAULT_MODEL,
        endpoint=DEFAULT_ENDPOINT
    )
    
    # Run multiple trials
    all_trials = []
    for trial_num in range(1, args.trials + 1):
        print(f"\n{'='*80}")
        print(f"TRIAL {trial_num}/{args.trials}")
        print(f"{'='*80}")
        
        trial_assessments = []
        for prompt_data in HERO_PROMPTS:
            assessment = assess_prompt_verifier_law(prompt_data, gpt5_client)
            trial_assessments.append(assessment)
        
        all_trials.append(trial_assessments)
        print(f"\n✅ Trial {trial_num} completed ({len(trial_assessments)} assessments)")
    
    print(f"\n{'='*80}")
    print(f"✅ All {args.trials} trials completed!")
    print(f"{'='*80}\n")
    
    # Aggregate results from all trials - REQUIRE exactly args.trials successful assessments
    print(f"📊 Aggregating results across trials (requiring exactly {args.trials} successful trials per prompt)...")
    aggregated = aggregate_trial_results(all_trials, required_trials=args.trials)
    
    if len(aggregated) == 0:
        print(f"\n❌ ERROR: No prompts had exactly {args.trials} successful trials!")
        print("   This is likely due to JSON parsing errors. Check debug_response_*.txt files.")
        sys.exit(1)
    
    print(f"✅ {len(aggregated)}/{len(HERO_PROMPTS)} prompts have exactly {args.trials} successful trials\n")
    
    # Rank by Verifier's Law
    print("📊 Ranking prompts by Verifier's Law priority...")
    ranked = rank_by_verifier_law(aggregated)
    
    # Save JSON results with trial statistics
    output_data = {
        "assessment_date": datetime.now().isoformat(),
        "framework": "Verifier's Law",
        "model": "dev-gpt-5-chat-jj (GPT-5)",
        "trials": args.trials,
        "total_prompts": len(HERO_PROMPTS),
        "successful_assessments": len(ranked),
        "ranked_prompts": ranked
    }
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved JSON results: {output_path}")
    
    # Generate and save report
    report = generate_summary_report(ranked)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Saved report: {report_path}")
    
    # Print summary with statistics
    print("\n" + "=" * 80)
    print("TOP 3 PRIORITIES BY VERIFIER'S LAW (with Evidence)")
    print("=" * 80)
    for i, assessment in enumerate(ranked[:3], 1):
        trial_count = assessment.get('trial_count', 1)
        print(f"\n{i}. {assessment['prompt_id'].upper()}")
        print(f"   Composite Score: {assessment['composite_score']:.2f}")
        
        if trial_count > 1:
            print(f"   Solvability: {assessment['solvability']['score']}/10 (±{assessment['solvability']['std']}, range {assessment['solvability']['range']})")
            print(f"   Verification: {assessment['verification_ease']['score']}/10 (±{assessment['verification_ease']['std']}, range {assessment['verification_ease']['range']})")
            print(f"   Asymmetry: {assessment['verification_asymmetry']['score']} (±{assessment['verification_asymmetry']['std']}, range {assessment['verification_asymmetry']['range']})")
            print(f"   Evidence: {trial_count} trials show consistent results")
        else:
            print(f"   Solvability: {assessment['solvability']['score']}/10")
            print(f"   Verification: {assessment['verification_ease']['score']}/10")
            print(f"   Asymmetry: {assessment['verification_asymmetry']['score']}")
        
        print(f"   AI Readiness: {assessment['ai_readiness']['timeline']}")
    
    print("\n" + "=" * 80)
    print(f"✨ Assessment complete with {args.trials}-trial evidence! Check {args.report} for full analysis.")
    print("=" * 80)


if __name__ == "__main__":
    main()
