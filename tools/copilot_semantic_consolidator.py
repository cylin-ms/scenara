#!/usr/bin/env python3
"""
GitHub Copilot (Claude Sonnet 4.5) Powered GUTT Semantic Consolidation

Uses GitHub Copilot's agent mode (Claude Sonnet 4.5) to intelligently:
1. Match GUTTs between Claude and GPT-5 decompositions (pair-wise per prompt)
2. Consolidate similar capabilities across all prompts
3. Generate canonical GUTT library for Calendar.AI

This version leverages the AI agent's direct reasoning capabilities rather than API calls.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

class CopilotSemanticAnalyzer:
    """Uses direct AI reasoning for GUTT semantic analysis"""
    
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
    
    def analyze_all_prompts(self) -> Dict:
        """Load all prompt data for AI agent analysis"""
        print("\n" + "="*100)
        print("LOADING DATA FOR COPILOT AGENT ANALYSIS")
        print("="*100 + "\n")
        
        all_data = []
        
        for prompt_id, prompt_desc in self.prompts:
            claude_data, gpt5_data, original_prompt = self.load_prompt_data(prompt_id)
            
            all_data.append({
                "prompt_id": prompt_id,
                "prompt_desc": prompt_desc,
                "original_prompt": original_prompt,
                "claude_gutts": claude_data['gutts'],
                "gpt5_gutts": gpt5_data['gutts'],
            })
            
            print(f"✓ Loaded {prompt_id}: {len(claude_data['gutts'])} Claude GUTTs, {len(gpt5_data['gutts'])} GPT-5 GUTTs")
        
        print(f"\nTotal: {sum(len(d['claude_gutts']) for d in all_data)} Claude + {sum(len(d['gpt5_gutts']) for d in all_data)} GPT-5 = {sum(len(d['claude_gutts']) + len(d['gpt5_gutts']) for d in all_data)} GUTTs")
        
        return {
            "prompts": all_data,
            "metadata": {
                "total_prompts": len(all_data),
                "total_claude_gutts": sum(len(d['claude_gutts']) for d in all_data),
                "total_gpt5_gutts": sum(len(d['gpt5_gutts']) for d in all_data),
            }
        }
    
    def save_for_agent_analysis(self, data: Dict):
        """Save data in format ready for AI agent analysis"""
        output_path = Path("docs/gutt_analysis")
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_file = output_path / "copilot_analysis_input.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*100}")
        print(f"DATA PREPARED FOR AGENT ANALYSIS")
        print(f"{'='*100}")
        print(f"\nSaved to: {output_file}")
        print(f"\nNext: AI Agent will analyze this data to:")
        print(f"  1. Classify relationships (=, <, >, ∩, ⊥) for each Claude-GPT5 pair per prompt")
        print(f"  2. Identify canonical Unit Tasks across all prompts")
        print(f"  3. Build relationship graphs and hierarchies")
        print(f"\nReady for agent analysis!\n")
        
        return output_file


def main():
    analyzer = CopilotSemanticAnalyzer()
    
    # Load all GUTT data
    data = analyzer.analyze_all_prompts()
    
    # Save for agent analysis
    output_file = analyzer.save_for_agent_analysis(data)
    
    print("="*100)
    print("READY FOR COPILOT AGENT ANALYSIS")
    print("="*100)
    print(f"\nThe AI agent (Claude Sonnet 4.5) will now analyze:")
    print(f"  - 9 prompts with paired Claude/GPT-5 decompositions")
    print(f"  - {data['metadata']['total_claude_gutts']} + {data['metadata']['total_gpt5_gutts']} = {data['metadata']['total_claude_gutts'] + data['metadata']['total_gpt5_gutts']} total GUTTs")
    print(f"\nAnalysis framework: 5-relationship model (=, <, >, ∩, ⊥)")
    print(f"\nData file: {output_file}")


if __name__ == "__main__":
    main()
