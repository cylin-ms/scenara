#!/usr/bin/env python3
"""
Claude vs GPT-5 GUTT Analysis Deep Dive

Uses Claude Sonnet 4.5 to analyze the differences between Claude and GPT-5 v2
GUTT decompositions, debate which analysis is more appropriate, and provide
reasoning for each difference.

This meta-analysis uses Claude to evaluate its own results vs GPT-5's results.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

try:
    import anthropic
except ImportError:
    print("❌ anthropic package not installed. Install with: pip install anthropic")
    sys.exit(1)

# Prompt metadata
PROMPTS = [
    ("organizer-1", "Calendar Prioritization", "Keep my Calendar up to date by committing to only meetings that are part of my priorities."),
    ("organizer-2", "Meeting Prep Tracking", "Track all my important meetings and flag any that require focus time to prepare for them."),
    ("organizer-3", "Time Reclamation", "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."),
    ("schedule-1", "Recurring 1:1 Scheduling", "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."),
    ("schedule-2", "Block Time & Reschedule", "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."),
    ("schedule-3", "Multi-Person Scheduling", "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."),
    ("collaborate-1", "Agenda Creation", "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."),
    ("collaborate-2", "Executive Briefing Prep", "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."),
    ("collaborate-3", "Customer Meeting Prep", "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."),
]


def load_decomposition(file_path: str) -> Dict[str, Any]:
    """Load GUTT decomposition from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Could not load {file_path}: {e}")
        return {"gutts": []}


def compare_decompositions(prompt_id: str, prompt_name: str, prompt_text: str, api_key: str) -> Dict[str, Any]:
    """Use Claude to analyze differences between Claude and GPT-5 decompositions."""
    
    # Load both decompositions
    claude_file = f"hero_prompt_analysis/claude_gutt_{prompt_id}.json"
    gpt5_file = f"hero_prompt_analysis/gpt5_gutt_{prompt_id}.json"
    
    claude_data = load_decomposition(claude_file)
    gpt5_data = load_decomposition(gpt5_file)
    
    claude_gutts = claude_data.get('gutts', [])
    gpt5_gutts = gpt5_data.get('gutts', [])
    
    # Format GUTTs for comparison
    def format_gutts(gutts: List[Dict]) -> str:
        return "\n".join([
            f"{i+1}. **{g.get('name', 'Unnamed')}**\n"
            f"   - Capability: {g.get('capability', 'N/A')}\n"
            f"   - Skills: {', '.join(g.get('required_skills', []))}\n"
            for i, g in enumerate(gutts)
        ])
    
    claude_formatted = format_gutts(claude_gutts)
    gpt5_formatted = format_gutts(gpt5_gutts)
    
    # Create analysis prompt
    analysis_prompt = f"""You are an expert in GUTT (Granular Unit Task Taxonomy) analysis. I need you to compare two different GUTT decompositions of the same prompt and provide a deep, reasoned analysis.

**Original Prompt ({prompt_name})**:
"{prompt_text}"

**Claude Sonnet 4.5 Decomposition** ({len(claude_gutts)} GUTTs):
{claude_formatted}

**GPT-5 Decomposition** ({len(gpt5_gutts)} GUTTs):
{gpt5_formatted}

Please analyze these two decompositions and provide:

1. **Agreement Analysis**: Which GUTTs are essentially the same between both models? (even if named differently)
   - List the matched pairs with brief explanation of why they're equivalent
   - Calculate: What percentage of GUTTs are in agreement?

2. **Difference Analysis**: What GUTTs appear in one but not the other?
   - Claude-only GUTTs: List and explain what these cover
   - GPT-5-only GUTTs: List and explain what these cover

3. **Granularity Debate**: For each major difference, debate which decomposition is more appropriate:
   - Is one model decomposing too finely (over-granular)?
   - Is one model grouping too much (under-granular)?
   - Which granularity better represents "atomic unit tasks"?

4. **Deep Dive Examples**: Pick the 2-3 most interesting differences and provide detailed reasoning:
   - What is the fundamental disagreement?
   - Which approach is more correct for GUTT framework?
   - What are the implementation implications?
   - Could both be valid (different decomposition philosophies)?

5. **Overall Assessment**:
   - Which decomposition is more complete?
   - Which is more implementable?
   - Which better serves the GUTT framework purpose?
   - Final verdict: If you had to choose one, which would it be and why?

**Important Context**:
- GUTT framework emphasizes "atomic unit tasks" - each GUTT should represent ONE independently implementable capability
- Both models received the same GUTT v4.0 ACRUE documentation
- This is meta-analysis: you (Claude) are evaluating your own decomposition vs GPT-5's

Be objective, thorough, and willing to critique your own decomposition if GPT-5's is more appropriate."""

    # Call Claude for analysis
    print(f"\n🤔 Analyzing {prompt_name} ({prompt_id})...")
    print(f"   Claude GUTTs: {len(claude_gutts)}, GPT-5 GUTTs: {len(gpt5_gutts)}")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": analysis_prompt}
        ]
    )
    
    analysis_text = message.content[0].text
    
    return {
        "prompt_id": prompt_id,
        "prompt_name": prompt_name,
        "prompt_text": prompt_text,
        "claude_gutt_count": len(claude_gutts),
        "gpt5_gutt_count": len(gpt5_gutts),
        "claude_gutts": claude_gutts,
        "gpt5_gutts": gpt5_gutts,
        "analysis": analysis_text,
        "model_used": "claude-sonnet-4-20250514"
    }


def main():
    """Main analysis function."""
    import os
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    print("=" * 100)
    print("🔬 CLAUDE vs GPT-5 GUTT DEEP DIVE ANALYSIS")
    print("=" * 100)
    print("\nUsing Claude Sonnet 4.5 to meta-analyze the differences between:")
    print("  • Claude Sonnet 4.5's own GUTT decompositions")
    print("  • GPT-5 v2's GUTT decompositions (with full GUTT documentation)")
    print("\n" + "=" * 100)
    
    # Analyze each prompt
    all_analyses = []
    
    for prompt_id, prompt_name, prompt_text in PROMPTS:
        try:
            analysis = compare_decompositions(prompt_id, prompt_name, prompt_text, api_key)
            all_analyses.append(analysis)
            
            print(f"✅ Completed analysis for {prompt_name}")
            
        except Exception as e:
            print(f"❌ Failed to analyze {prompt_name}: {e}")
            continue
    
    # Save all analyses
    output_file = "claude_vs_gpt5_deep_dive_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analyses, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ All analyses saved to: {output_file}")
    
    # Generate summary report
    print("\n" + "=" * 100)
    print("📊 GENERATING SUMMARY REPORT")
    print("=" * 100)
    
    generate_summary_report(all_analyses, api_key)


def generate_summary_report(analyses: List[Dict], api_key: str):
    """Generate a summary report across all prompts."""
    
    # Prepare data for summary
    summary_data = []
    for a in analyses:
        summary_data.append({
            "prompt": f"{a['prompt_name']} ({a['prompt_id']})",
            "claude_count": a['claude_gutt_count'],
            "gpt5_count": a['gpt5_gutt_count'],
            "difference": a['gpt5_gutt_count'] - a['claude_gutt_count'],
            "analysis_preview": a['analysis'][:500] + "..."
        })
    
    # Create summary prompt
    summary_prompt = f"""Based on these {len(analyses)} detailed GUTT decomposition comparisons between Claude Sonnet 4.5 and GPT-5 v2, provide a comprehensive summary:

**Prompt-by-Prompt Summary**:
{json.dumps(summary_data, indent=2)}

**Full Detailed Analyses Available**: {len(analyses)} complete analyses

Please provide:

1. **Overall Pattern Analysis**:
   - Does Claude tend to over-decompose, under-decompose, or match GPT-5?
   - What's the average difference in GUTT count?
   - Are there systematic differences in decomposition philosophy?

2. **Category Analysis** (Organizer, Schedule, Collaborate):
   - Do patterns differ by category?
   - Which category shows most agreement?
   - Which category shows most divergence?

3. **Key Insights**:
   - What are the 3-5 most important findings across all comparisons?
   - What do these differences reveal about each model's approach?
   - Are the differences due to granularity, comprehensiveness, or interpretation?

4. **Meta-Analysis Reflection**:
   - As Claude analyzing your own work vs GPT-5, what did you learn?
   - Were you objective in evaluating your own decompositions?
   - What surprised you about the comparison?

5. **Recommendations**:
   - For production GUTT analysis, which model should be used?
   - Should both models be used together (ensemble approach)?
   - What would be the ideal GUTT decomposition strategy?

6. **Final Verdict**:
   - Overall winner: Claude or GPT-5? (be honest!)
   - Confidence level in this verdict (0-100%)
   - Key deciding factors"""

    client = anthropic.Anthropic(api_key=api_key)
    
    print("\n🤔 Generating cross-prompt summary analysis...")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": summary_prompt}
        ]
    )
    
    summary_analysis = message.content[0].text
    
    # Save summary
    summary_file = "claude_vs_gpt5_summary_report.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Claude Sonnet 4.5 vs GPT-5 v2 - GUTT Analysis Summary\n\n")
        f.write(f"**Analysis Date**: November 6, 2025\n")
        f.write(f"**Prompts Analyzed**: {len(analyses)}\n")
        f.write(f"**Meta-Analyst**: Claude Sonnet 4.5 (claude-sonnet-4-20250514)\n\n")
        f.write("---\n\n")
        f.write(summary_analysis)
        f.write("\n\n---\n\n")
        f.write("## Detailed Analyses\n\n")
        f.write(f"See `claude_vs_gpt5_deep_dive_analysis.json` for complete prompt-by-prompt analyses.\n")
    
    print(f"✅ Summary report saved to: {summary_file}")
    
    # Print summary to console
    print("\n" + "=" * 100)
    print("📋 SUMMARY REPORT")
    print("=" * 100)
    print(summary_analysis)
    print("=" * 100)


if __name__ == "__main__":
    main()
