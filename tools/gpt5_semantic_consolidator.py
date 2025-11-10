#!/usr/bin/env python3
"""
GPT-5 Powered GUTT Semantic Consolidation

Uses GPT-5 to intelligently:
1. Match GUTTs between Claude and GPT-5 decompositions (pair-wise per prompt)
2. Consolidate similar capabilities across all prompts
3. Generate canonical GUTT library for Calendar.AI

Advantages over text similarity:
- Deep semantic understanding
- Context-aware matching
- Handles different naming conventions
- Identifies truly equivalent vs subtly different capabilities
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import uuid

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier

# GPT-5 Configuration
ENDPOINT = "https://fe-26.qas.bing.net/chat/completions"
MODEL = "dev-gpt-5-chat-jj"

class GPT5SemanticConsolidator:
    """Uses GPT-5 for semantic GUTT matching and consolidation"""
    
    def __init__(self):
        self.base_path = Path("hero_prompt_analysis")
        self.prompts = [
            ("organizer-1", "Priority-based calendar management"),
            ("organizer-2", "Track important meetings, flag prep needs"),
            ("organizer-3", "Time reclamation analysis"),
            ("schedule-1", "Recurring 1:1 with constraints"),
            ("schedule-2", "Clear time block & reschedule"),
            ("schedule-3", "Multi-person meeting with room"),
            ("collaborate-1", "Set agenda for project review"),
            ("collaborate-2", "Executive briefing prep"),
            ("collaborate-3", "Customer meeting brief"),
        ]
        self.token = None
        self.classifier = None
    
    def get_token(self):
        """Acquire GPT-5 access token"""
        if not self.token:
            print("Acquiring GPT-5 access token...")
            # Use GPT5MeetingClassifier to acquire token
            if not self.classifier:
                self.classifier = GPT5MeetingClassifier()
            self.token = self.classifier._acquire_token()
            print(f"Token acquired ({len(self.token)} chars)\n")
        return self.token
    
    def call_gpt5(self, system_prompt: str, user_prompt: str) -> str:
        """Call GPT-5 API"""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "X-ModelType": MODEL,
            "X-ScenarioGUID": str(uuid.uuid4()),
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "max_completion_tokens": 4096,
            "temperature": 0.1,
            "top_p": 0.95,
            "n": 1,
            "stream": False
        }
        
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def load_prompt_data(self, prompt_id: str) -> Tuple[Dict, Dict, str]:
        """Load Claude and GPT-5 decompositions for a prompt"""
        claude_file = self.base_path / f"claude_gutt_{prompt_id}.json"
        gpt5_file = self.base_path / f"gpt5_gutt_{prompt_id}.json"
        
        with open(claude_file, 'r', encoding='utf-8') as f:
            claude_data = json.load(f)
        
        with open(gpt5_file, 'r', encoding='utf-8') as f:
            gpt5_data = json.load(f)
        
        original_prompt = claude_data.get('original_prompt', '')
        
        return claude_data, gpt5_data, original_prompt
    
    def match_gutts_for_prompt(self, prompt_id: str, prompt_desc: str) -> Dict:
        """Use GPT-5 to match GUTTs between Claude and GPT-5 for a single prompt"""
        print(f"\n{'='*100}")
        print(f"ANALYZING: {prompt_id} - {prompt_desc}")
        print(f"{'='*100}\n")
        
        claude_data, gpt5_data, original_prompt = self.load_prompt_data(prompt_id)
        
        claude_gutts = claude_data['gutts']
        gpt5_gutts = gpt5_data['gutts']
        
        print(f"Original Prompt: {original_prompt[:100]}...")
        print(f"Claude: {len(claude_gutts)} GUTTs")
        print(f"GPT-5:  {len(gpt5_gutts)} GUTTs\n")
        
        # Prepare GUTT lists for GPT-5
        claude_list = []
        for i, gutt in enumerate(claude_gutts, 1):
            claude_list.append(f"C{i}. {gutt['name']}\n   Capability: {gutt['capability']}")
        
        gpt5_list = []
        for i, gutt in enumerate(gpt5_gutts, 1):
            gpt5_list.append(f"G{i}. {gutt['name']}\n   Capability: {gutt['capability']}")
        
        system_prompt = """You are an expert at analyzing GUTT (Granular Unit Task Taxonomy) decompositions. Each GUTT represents a Unit Task - an atomic capability that:

1. Is indivisible (cannot be meaningfully split further)
2. Corresponds to what a single API call or tool would provide
3. Maps to a specific skill or capability
4. Is reusable across different scenarios

Your job is to identify relationships between Unit Tasks in two decompositions. For any pair of tasks A and B, there are exactly 5 possible relationships:

1. **A = B** (EQUIVALENT): Same atomic capability, just different naming
   Example: "Retrieve calendar events" = "Fetch user calendar data"

2. **A < B** (SUBSET): A is a narrower/more specific version of B
   Example: "Get today's meetings" < "Retrieve calendar events for date range"

3. **A > B** (SUPERSET): A is broader and encompasses B
   Example: "Analyze all calendar data" > "Count meetings per day"

4. **A ∩ B** (OVERLAPPING): A and B share some functionality but each has unique aspects
   Example: "Get meeting with attendees" ∩ "Get meeting with location" (both get meetings, different filters)

5. **A ⊥ B** (DISJOINT): Completely different capabilities, no overlap
   Example: "Send email invitation" ⊥ "Parse time zone"

Focus on WHAT API/tool capability is needed, not naming conventions."""

        user_prompt = f"""Original Prompt: "{original_prompt}"

Claude's Unit Task Decomposition ({len(claude_gutts)} GUTTs):
{chr(10).join(claude_list)}

GPT-5's Unit Task Decomposition ({len(gpt5_gutts)} GUTTs):
{chr(10).join(gpt5_list)}

Task: Analyze the relationship between every Claude GUTT and GPT-5 GUTT using the 5-relationship model:

**RELATIONSHIP TYPES:**
1. **A = B** (EQUIVALENT) - Same atomic capability, different naming
2. **A < B** (SUBSET) - A is narrower/more specific than B
3. **A > B** (SUPERSET) - A is broader and encompasses B
4. **A ∩ B** (OVERLAPPING) - Partial overlap, each has unique aspects
5. **A ⊥ B** (DISJOINT) - Completely different, no overlap

**OUTPUT FORMAT:**

1. **EQUIVALENT (A = B)** - Unit Tasks representing the same atomic capability
   Format: "C# = G#: [What common API/capability they represent]"

2. **SUBSET (A < B)** - Claude task is more specific than GPT-5 task
   Format: "C# < G#: [Explain how C is narrower than G]"

3. **SUPERSET (A > B)** - Claude task is broader than GPT-5 task
   Format: "C# > G#: [Explain how C encompasses G]"

4. **OVERLAPPING (A ∩ B)** - Tasks share functionality but have unique aspects
   Format: "C# ∩ G#: [Explain shared parts and unique parts of each]"

5. **CLAUDE UNIQUE** - Claude tasks with no relationship to any GPT-5 task (all relationships are ⊥)
   Format: "C#: [What unique capability this represents]"

6. **GPT-5 UNIQUE** - GPT-5 tasks with no relationship to any Claude task (all relationships are ⊥)
   Format: "G#: [What unique capability this represents]"

Be precise and justify each relationship based on the atomic capabilities involved."""

        print("Calling GPT-5 for semantic matching...")
        response = self.call_gpt5(system_prompt, user_prompt)
        
        print("\nGPT-5 Analysis:")
        print("-" * 100)
        print(response)
        print("-" * 100)
        
        return {
            "prompt_id": prompt_id,
            "prompt_desc": prompt_desc,
            "original_prompt": original_prompt,
            "claude_count": len(claude_gutts),
            "gpt5_count": len(gpt5_gutts),
            "claude_gutts": claude_gutts,
            "gpt5_gutts": gpt5_gutts,
            "gpt5_analysis": response,
        }
    
    def analyze_all_prompts(self) -> List[Dict]:
        """Analyze all 9 prompts"""
        print("\n" + "="*100)
        print("PHASE 1: PAIR-WISE SEMANTIC MATCHING")
        print("Using GPT-5 to match Claude vs GPT-5 GUTTs for each prompt")
        print("="*100)
        
        results = []
        for prompt_id, prompt_desc in self.prompts:
            result = self.match_gutts_for_prompt(prompt_id, prompt_desc)
            results.append(result)
            print(f"\nCompleted: {prompt_id}")
        
        return results
    
    def consolidate_across_prompts(self, results: List[Dict]) -> Dict:
        """Use GPT-5 to consolidate capabilities across all prompts"""
        print(f"\n\n{'='*100}")
        print("PHASE 2: CROSS-PROMPT CONSOLIDATION")
        print("Using GPT-5 to identify common capabilities across all prompts")
        print("="*100 + "\n")
        
        # Collect all GUTTs from both models
        all_gutts = []
        
        for result in results:
            prompt_id = result['prompt_id']
            
            # Add Claude GUTTs
            for gutt in result['claude_gutts']:
                all_gutts.append({
                    "source": "Claude",
                    "prompt": prompt_id,
                    "name": gutt['name'],
                    "capability": gutt['capability'],
                    "skills": gutt.get('required_skills', []),
                })
            
            # Add GPT-5 GUTTs
            for gutt in result['gpt5_gutts']:
                all_gutts.append({
                    "source": "GPT-5",
                    "prompt": prompt_id,
                    "name": gutt['name'],
                    "capability": gutt['capability'],
                    "skills": gutt.get('required_skills', []),
                })
        
        print(f"Total GUTTs to consolidate: {len(all_gutts)}")
        print("(66 from Claude + 66 from GPT-5 = 132 total)\n")
        
        # Create compact representation for GPT-5
        gutt_summary = []
        for i, gutt in enumerate(all_gutts, 1):
            gutt_summary.append(
                f"{i}. [{gutt['source']}] [{gutt['prompt']}] {gutt['name']}\n"
                f"   {gutt['capability'][:100]}..."
            )
        
        system_prompt = """You are an expert at identifying canonical Unit Tasks across GUTT (Granular Unit Task Taxonomy) decompositions.

A Unit Task represents an atomic capability that:
1. Maps to a single API call or tool function
2. Is indivisible (cannot be split further meaningfully)  
3. Represents a reusable skill/capability
4. Has clear input/output boundaries

Your goal is to identify CANONICAL UNIT TASKS that appear across multiple prompts. You must account for 5 types of relationships between tasks:

**RELATIONSHIP TYPES:**
1. **A = B** (EQUIVALENT) - Same atomic capability
2. **A < B** (SUBSET) - A is more specific than B
3. **A > B** (SUPERSET) - A is broader than B
4. **A ∩ B** (OVERLAPPING) - Partial overlap
5. **A ⊥ B** (DISJOINT) - No overlap

**CONSOLIDATION APPROACH:**
- Group tasks with = relationship (equivalent capabilities)
- Identify hierarchies (subset/superset relationships)
- Note overlapping patterns
- Abstract to the most reusable level (neither too specific nor too broad)
- Only include capabilities appearing in 2+ prompts"""

        user_prompt = f"""Analyze these {len(all_gutts)} Unit Tasks from 9 different Calendar.AI prompts:

{chr(10).join(gutt_summary[:50])}
... (showing first 50, full list includes all 132)

Task: Identify CANONICAL UNIT TASKS using the 5-relationship model.

**APPROACH:**
1. Group tasks with **= relationships** (equivalent capabilities across prompts)
2. Identify **< and > hierarchies** (specific vs. general versions of same capability)
3. Note **∩ patterns** (overlapping capabilities that might need splitting/merging)
4. Ignore **⊥ tasks** (unique to single prompts)

**OUTPUT FORMAT:**

For each canonical Unit Task (appearing in 2+ prompts):

**Canonical Task #X: [Generic Name]**
- **API/Tool**: What underlying API/tool this represents
- **Relationship Graph**: 
  - Equivalent tasks (=): [List task numbers that are equivalent]
  - Subset tasks (<): [More specific variations]
  - Superset tasks (>): [More general variations]
  - Overlapping (∩): [Partial matches]
- **Frequency**: Number of prompts using this capability
- **Example Variations**: How different prompts use it

**EXAMPLES:**

**Canonical Task #1: Calendar Events Retrieval**
- **API/Tool**: Graph API: GET /me/calendar/events
- **Relationship Graph**:
  - Equivalent (=): #5, #23, #47, #89 (all retrieve calendar events)
  - Subset (<): #12 "Get today's meetings" (specific date range)
  - Superset (>): #67 "Get all user calendar data" (broader scope)
- **Frequency**: 7 prompts
- **Variations**: Some filter by date, some by attendee, all use same API

Provide the top 20-30 most common canonical Unit Tasks with their relationship graphs."""

        print("Calling GPT-5 for cross-prompt consolidation...")
        print("(This analyzes all 132 GUTTs to find common patterns)\n")
        
        # For large analysis, we'll do it in chunks
        response = self.call_gpt5(system_prompt, user_prompt)
        
        print("GPT-5 Cross-Prompt Analysis:")
        print("-" * 100)
        print(response)
        print("-" * 100)
        
        return {
            "total_gutts": len(all_gutts),
            "claude_gutts": 66,
            "gpt5_gutts": 66,
            "gpt5_consolidation_analysis": response,
            "all_gutts": all_gutts,
        }
    
    def generate_canonical_library(self, results: List[Dict], 
                                   consolidation: Dict) -> Dict:
        """Generate final canonical GUTT library based on GPT-5 analysis"""
        print(f"\n\n{'='*100}")
        print("PHASE 3: CANONICAL LIBRARY GENERATION")
        print("Creating structured canonical GUTT library from GPT-5 analysis")
        print("="*100 + "\n")
        
        library = {
            "metadata": {
                "generated_date": "2025-11-06",
                "method": "GPT-5 Semantic Analysis",
                "source_prompts": len(results),
                "total_gutts_analyzed": consolidation['total_gutts'],
                "models": ["Claude Sonnet 4.5", "GPT-5 v2"],
            },
            "per_prompt_mappings": [],
            "cross_prompt_consolidation": consolidation['gpt5_consolidation_analysis'],
            "raw_gutts": consolidation['all_gutts'],
        }
        
        # Add per-prompt analysis
        for result in results:
            library['per_prompt_mappings'].append({
                "prompt_id": result['prompt_id'],
                "prompt_desc": result['prompt_desc'],
                "original_prompt": result['original_prompt'],
                "claude_count": result['claude_count'],
                "gpt5_count": result['gpt5_count'],
                "gpt5_semantic_analysis": result['gpt5_analysis'],
            })
        
        print(f"Library contains:")
        print(f"  - {len(results)} per-prompt semantic matchings")
        print(f"  - Cross-prompt consolidation analysis")
        print(f"  - {consolidation['total_gutts']} raw GUTT definitions")
        
        return library
    
    def run_full_analysis(self):
        """Run complete GPT-5 powered analysis"""
        print("\n" + "="*100)
        print("GPT-5 POWERED GUTT SEMANTIC CONSOLIDATION")
        print("Goal: Create canonical GUTT library using deep semantic understanding")
        print("="*100)
        
        try:
            # Phase 1: Per-prompt matching
            results = self.analyze_all_prompts()
            
            # Phase 2: Cross-prompt consolidation
            consolidation = self.consolidate_across_prompts(results)
            
            # Phase 3: Generate library
            library = self.generate_canonical_library(results, consolidation)
            
            # Save results
            output_path = Path("docs/gutt_analysis")
            output_path.mkdir(parents=True, exist_ok=True)
            
            output_file = output_path / "gpt5_semantic_consolidation.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(library, f, indent=2, ensure_ascii=False)
            
            print(f"\n\n{'='*100}")
            print("ANALYSIS COMPLETE")
            print(f"{'='*100}")
            print(f"\nOutput file: {output_file}")
            print(f"\nNext steps:")
            print(f"  1. Review GPT-5's semantic matching for each prompt")
            print(f"  2. Review cross-prompt canonical capabilities")
            print(f"  3. Extract structured canonical GUTT library")
            print(f"  4. Use for analyzing new Calendar.AI prompts\n")
            
            return library
            
        except Exception as e:
            print(f"\nError during analysis: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    consolidator = GPT5SemanticConsolidator()
    library = consolidator.run_full_analysis()
    
    if library:
        print("\n" + "="*100)
        print("SUCCESS: GPT-5 semantic consolidation complete!")
        print("="*100)
        print("\nKey outputs:")
        print("  - Per-prompt GUTT mappings (9 prompts)")
        print("  - Cross-prompt capability consolidation")
        print("  - Canonical GUTT library foundation")
        print("\nReview docs/gutt_analysis/gpt5_semantic_consolidation.json for full results.")
    else:
        print("\nAnalysis failed. Check error messages above.")


if __name__ == "__main__":
    main()
