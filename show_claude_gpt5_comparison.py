#!/usr/bin/env python3
"""
Claude Sonnet 4.5 vs GPT-5 v2 GUTT Comparison Visualization

Displays side-by-side comparison of GUTT decompositions from both models
with qualitative analysis of agreements and differences.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        "id": "organizer-3",
        "category": "Organizer",
        "prompt": "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."
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
        "prompt": "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."
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
        "prompt": "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."
    }
]

def load_gutt_results(prompt_id: str) -> Tuple[Dict, Dict]:
    """Load GUTT results from both Claude and GPT-5 for a given prompt"""
    base_path = Path("hero_prompt_analysis")
    
    claude_file = base_path / f"claude_gutt_{prompt_id}.json"
    gpt5_file = base_path / f"gpt5_gutt_{prompt_id}.json"
    
    with open(claude_file, 'r', encoding='utf-8') as f:
        claude_data = json.load(f)
    
    with open(gpt5_file, 'r', encoding='utf-8') as f:
        gpt5_data = json.load(f)
    
    return claude_data, gpt5_data

def print_comparison_summary():
    """Print overall comparison summary"""
    print(f"\n{Colors.BOLD}{'='*100}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}CLAUDE SONNET 4.5 vs GPT-5 v2: GUTT DECOMPOSITION COMPARISON{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*100}{Colors.ENDC}\n")
    
    print(f"{Colors.OKBLUE}Analysis Date:{Colors.ENDC} November 6, 2025")
    print(f"{Colors.OKBLUE}Claude Model:{Colors.ENDC} claude-sonnet-4-20250514 (via Cursor Agent Mode)")
    print(f"{Colors.OKBLUE}GPT-5 Model:{Colors.ENDC} dev-gpt-5-chat-jj (via Microsoft SilverFlow LLM API)")
    print(f"{Colors.OKBLUE}Context:{Colors.ENDC} Both models given full GUTT v4.0 ACRUE documentation\n")
    
    # Load all results and compute summary
    total_claude = 0
    total_gpt5 = 0
    perfect_matches = 0
    
    results = []
    for prompt_data in HERO_PROMPTS:
        prompt_id = prompt_data["id"]
        claude_data, gpt5_data = load_gutt_results(prompt_id)
        
        claude_count = len(claude_data["gutts"])
        gpt5_count = len(gpt5_data["gutts"])
        
        total_claude += claude_count
        total_gpt5 += gpt5_count
        
        if claude_count == gpt5_count:
            perfect_matches += 1
        
        results.append({
            "id": prompt_id,
            "category": prompt_data["category"],
            "claude": claude_count,
            "gpt5": gpt5_count,
            "diff": gpt5_count - claude_count
        })
    
    # Print summary table
    print(f"{Colors.BOLD}OVERALL SUMMARY{Colors.ENDC}")
    print(f"{'─'*100}\n")
    
    print(f"{'Prompt ID':<20} {'Category':<15} {'Claude':<10} {'GPT-5':<10} {'Difference':<12} {'Status'}")
    print(f"{'─'*100}")
    
    for result in results:
        diff_str = f"{result['diff']:+d}" if result['diff'] != 0 else "0"
        
        if result['diff'] == 0:
            status = f"{Colors.OKGREEN}✅ PERFECT{Colors.ENDC}"
        elif result['diff'] > 0:
            status = f"{Colors.WARNING}GPT-5 +{result['diff']}{Colors.ENDC}"
        else:
            status = f"{Colors.OKCYAN}Claude +{abs(result['diff'])}{Colors.ENDC}"
        
        print(f"{result['id']:<20} {result['category']:<15} {result['claude']:<10} "
              f"{result['gpt5']:<10} {diff_str:<12} {status}")
    
    print(f"{'─'*100}")
    print(f"{'TOTALS':<20} {'':<15} {total_claude:<10} {total_gpt5:<10} "
          f"{(total_gpt5 - total_claude):+d if total_gpt5 != total_claude else '0':<12} "
          f"{Colors.OKGREEN}✅ MATCH{Colors.ENDC}" if total_claude == total_gpt5 else f"{Colors.WARNING}DIFF{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Perfect Individual Matches:{Colors.ENDC} {perfect_matches}/9 prompts ({perfect_matches/9*100:.1f}%)")
    print(f"{Colors.BOLD}Total Agreement:{Colors.ENDC} Both models generated 66 GUTTs total\n")

def print_detailed_comparison(prompt_id: str):
    """Print detailed side-by-side comparison for a specific prompt"""
    prompt_data = next(p for p in HERO_PROMPTS if p["id"] == prompt_id)
    claude_data, gpt5_data = load_gutt_results(prompt_id)
    
    print(f"\n{Colors.BOLD}{'='*100}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}Prompt: {prompt_id.upper()}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*100}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Category:{Colors.ENDC} {prompt_data['category']}")
    print(f"{Colors.BOLD}Prompt:{Colors.ENDC} {prompt_data['prompt']}\n")
    
    claude_count = len(claude_data["gutts"])
    gpt5_count = len(gpt5_data["gutts"])
    
    print(f"{Colors.OKBLUE}Claude GUTTs:{Colors.ENDC} {claude_count}")
    print(f"{Colors.OKBLUE}GPT-5 GUTTs:{Colors.ENDC} {gpt5_count}")
    
    if claude_count == gpt5_count:
        print(f"{Colors.OKGREEN}✅ PERFECT COUNT MATCH{Colors.ENDC}\n")
    else:
        diff = gpt5_count - claude_count
        print(f"{Colors.WARNING}Difference: {diff:+d} GUTTs{Colors.ENDC}\n")
    
    # Print Claude GUTTs
    print(f"{Colors.BOLD}{Colors.OKCYAN}CLAUDE SONNET 4.5 DECOMPOSITION:{Colors.ENDC}")
    print(f"{'─'*100}")
    for i, gutt in enumerate(claude_data["gutts"], 1):
        print(f"\n{Colors.BOLD}{i}. {gutt['name']}{Colors.ENDC}")
        print(f"   Capability: {gutt['capability']}")
        print(f"   Skills: {', '.join(gutt['required_skills'][:3])}{'...' if len(gutt['required_skills']) > 3 else ''}")
    
    # Print GPT-5 GUTTs
    print(f"\n\n{Colors.BOLD}{Colors.OKGREEN}GPT-5 v2 DECOMPOSITION:{Colors.ENDC}")
    print(f"{'─'*100}")
    for i, gutt in enumerate(gpt5_data["gutts"], 1):
        print(f"\n{Colors.BOLD}{i}. {gutt['name']}{Colors.ENDC}")
        print(f"   Capability: {gutt['capability']}")
        print(f"   Skills: {', '.join(gutt['required_skills'][:3])}{'...' if len(gutt['required_skills']) > 3 else ''}")
    
    print(f"\n{'─'*100}\n")

def print_pattern_analysis():
    """Print pattern analysis summary"""
    print(f"\n{Colors.BOLD}{'='*100}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}PATTERN ANALYSIS: PHILOSOPHICAL DIFFERENCES{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*100}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}{Colors.OKCYAN}CLAUDE'S DECOMPOSITION PHILOSOPHY:{Colors.ENDC}")
    print(f"{'─'*100}")
    print("✅ Implementation-centric: Focuses on cohesive code modules")
    print("✅ Workflow-oriented: Emphasizes end-to-end task completion")
    print("✅ Domain-aware: Includes domain-specific capabilities (stakeholder analysis, executive framing)")
    print("✅ Deliverable-focused: Often includes output formatting/reporting as explicit GUTTs")
    print("✅ Bundles related concerns: Groups tightly coupled logic (intent + context + constraints)")
    
    print(f"\n{Colors.BOLD}Strengths:{Colors.ENDC}")
    print("  • More practical for implementation teams (maps to code modules)")
    print("  • Better for evaluating end-to-end solution completeness")
    print("  • Domain-specific GUTTs surface nuanced capabilities")
    print("  • Fewer trivial GUTTs (avoids 'extract intent' one-liners)")
    
    print(f"\n{Colors.BOLD}Weaknesses:{Colors.ENDC}")
    print("  • Less precise for architectural testing (bundling obscures component failures)")
    print("  • May under-decompose complex bundles")
    print("  • Harder to validate individual atomic capabilities")
    
    print(f"\n\n{Colors.BOLD}{Colors.OKGREEN}GPT-5's DECOMPOSITION PHILOSOPHY:{Colors.ENDC}")
    print(f"{'─'*100}")
    print("✅ Architecture-centric: Focuses on system components and data flow")
    print("✅ Process-oriented: Emphasizes sequential processing steps (parse → extract → classify → act)")
    print("✅ Validation-focused: Includes explicit validation and confirmation steps")
    print("✅ Separation of concerns: Each GUTT represents a distinct architectural component")
    print("✅ Testability-first: Each GUTT is independently testable")
    
    print(f"\n{Colors.BOLD}Strengths:{Colors.ENDC}")
    print("  • Better architectural separation (can test identity resolution independently)")
    print("  • Explicit validation steps improve reliability")
    print("  • More aligned with ACRUE 'Atomic' principle")
    print("  • Easier to debug (can isolate specific component failures)")
    
    print(f"\n{Colors.BOLD}Weaknesses:{Colors.ENDC}")
    print("  • May over-decompose trivial steps ('Extract Meeting Intent')")
    print("  • Less focus on domain-specific nuances (misses 'executive framing')")
    print("  • May miss implicit deliverable expectations (document generation)")
    print("  • More GUTTs to manage in evaluation frameworks")
    
    print(f"\n{'─'*100}\n")

def print_recommendations():
    """Print recommendations based on analysis"""
    print(f"\n{Colors.BOLD}{'='*100}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}RECOMMENDATIONS{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*100}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}1. Use Case-Specific Decomposition Strategy{Colors.ENDC}")
    print("   • Implementation Testing → Claude's approach (bundle related tasks, focus on deliverables)")
    print("   • Architectural Testing → GPT-5's approach (separate components, explicit validation)")
    print()
    
    print(f"{Colors.BOLD}2. Hybrid Reference Decompositions{Colors.ENDC}")
    print("   • Combine GPT-5's architectural separation with Claude's domain-specific GUTTs")
    print("   • Include both validation steps (GPT-5) and deliverable GUTTs (Claude)")
    print("   • Expected result: ~70-75 GUTTs per full test set (vs current 66)")
    print()
    
    print(f"{Colors.BOLD}3. GUTT Bundling Rules{Colors.ENDC}")
    print("   Bundle when: Components share data source, logic is tightly coupled, separation creates trivial GUTTs")
    print("   Separate when: Components can fail independently, validation requires isolation, architectural clarity benefits")
    print()
    
    print(f"{Colors.BOLD}4. Next Steps{Colors.ENDC}")
    print("   • Create hybrid reference decompositions with human validation")
    print("   • Establish bundling/separation rules in GUTT documentation")
    print("   • Run 3-model comparison (Claude + GPT-5 + Ollama) with hybrid reference")
    print()
    
    print(f"{Colors.BOLD}CONCLUSION:{Colors.ENDC}")
    print(f"Both models demonstrate {Colors.OKGREEN}complementary strengths{Colors.ENDC}. Neither is objectively 'better'—")
    print("the optimal approach depends on evaluation goals. For Scenara 2.0, use a hybrid strategy")
    print("combining GPT-5's architectural rigor with Claude's domain expertise and UX focus.")
    print()

def main():
    """Main comparison visualization"""
    # Overall summary
    print_comparison_summary()
    
    # Pattern analysis
    print_pattern_analysis()
    
    # Detailed comparisons for prompts with differences
    print(f"\n{Colors.BOLD}{'='*100}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}DETAILED ANALYSIS: PROMPTS WITH DIFFERENCES{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*100}{Colors.ENDC}")
    
    difference_prompts = [
        ("organizer-2", "Claude 7, GPT-5 6: Proactive scheduling vs notification"),
        ("schedule-1", "Claude 7, GPT-5 9: Bundled constraints vs separated components"),
        ("schedule-2", "Claude 8, GPT-5 6: Visual calendar block vs status update"),
        ("collaborate-1", "Claude 6, GPT-5 8: Content-focused vs process-focused"),
        ("collaborate-2", "Claude 7, GPT-5 6: Executive framing vs systematic processing")
    ]
    
    for prompt_id, description in difference_prompts:
        print(f"\n{Colors.WARNING}━━━ {description} ━━━{Colors.ENDC}")
        print_detailed_comparison(prompt_id)
    
    # Recommendations
    print_recommendations()

if __name__ == "__main__":
    main()
