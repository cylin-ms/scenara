#!/usr/bin/env python3
"""
GUTT Consolidation Analyzer

Performs deep per-prompt analysis of Claude vs GPT-5 GUTT decompositions:
1. Maps individual GUTTs semantically (not just by count)
2. Identifies equivalent capabilities despite different naming
3. Finds unique GUTTs from each model
4. Consolidates cross-prompt capabilities into canonical GUTT library

Goal: Create reference GUTT set for Calendar.AI evaluation framework
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import re

class GUTTConsolidationAnalyzer:
    """Analyzes and consolidates GUTT decompositions across models and prompts"""
    
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
        
        # Canonical capability categories
        self.capability_categories = {
            "data_retrieval": ["retrieve", "fetch", "access", "load", "get", "extract data"],
            "parsing": ["parse", "extract", "identify", "resolve"],
            "classification": ["classify", "categorize", "identify type", "label"],
            "analysis": ["analyze", "evaluate", "assess", "compute", "calculate"],
            "decision_making": ["decide", "determine", "select", "choose", "rank"],
            "scheduling": ["schedule", "book", "reserve", "allocate time"],
            "validation": ["validate", "check", "verify", "confirm"],
            "optimization": ["optimize", "find best", "rank", "prioritize"],
            "execution": ["execute", "perform", "update", "modify", "create event"],
            "notification": ["notify", "send", "alert", "inform", "dispatch"],
            "reporting": ["report", "present", "visualize", "summarize", "generate"],
            "monitoring": ["monitor", "track", "detect", "watch"],
        }
    
    def load_prompt_data(self, prompt_id: str) -> Tuple[Dict, Dict]:
        """Load Claude and GPT-5 decompositions for a prompt"""
        claude_file = self.base_path / f"claude_gutt_{prompt_id}.json"
        gpt5_file = self.base_path / f"gpt5_gutt_{prompt_id}.json"
        
        with open(claude_file, 'r', encoding='utf-8') as f:
            claude_data = json.load(f)
        
        with open(gpt5_file, 'r', encoding='utf-8') as f:
            gpt5_data = json.load(f)
        
        return claude_data, gpt5_data
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def categorize_capability(self, capability: str) -> Set[str]:
        """Categorize a capability description into one or more categories"""
        normalized = self.normalize_text(capability)
        categories = set()
        
        for category, keywords in self.capability_categories.items():
            for keyword in keywords:
                if keyword in normalized:
                    categories.add(category)
                    break
        
        if not categories:
            categories.add("other")
        
        return categories
    
    def compute_semantic_similarity(self, gutt1: Dict, gutt2: Dict) -> float:
        """Compute semantic similarity between two GUTTs (0-1)"""
        score = 0.0
        
        # Name similarity (20%)
        name1 = self.normalize_text(gutt1['name'])
        name2 = self.normalize_text(gutt2['name'])
        common_words = set(name1.split()) & set(name2.split())
        name_score = len(common_words) / max(len(set(name1.split())), len(set(name2.split())), 1)
        score += name_score * 0.2
        
        # Capability similarity (40%)
        cap1 = self.normalize_text(gutt1['capability'])
        cap2 = self.normalize_text(gutt2['capability'])
        common_cap_words = set(cap1.split()) & set(cap2.split())
        cap_score = len(common_cap_words) / max(len(set(cap1.split())), len(set(cap2.split())), 1)
        score += cap_score * 0.4
        
        # Category overlap (20%)
        cats1 = self.categorize_capability(gutt1['capability'])
        cats2 = self.categorize_capability(gutt2['capability'])
        cat_score = len(cats1 & cats2) / max(len(cats1 | cats2), 1)
        score += cat_score * 0.2
        
        # Skills overlap (20%)
        skills1 = set(self.normalize_text(s) for s in gutt1.get('required_skills', []))
        skills2 = set(self.normalize_text(s) for s in gutt2.get('required_skills', []))
        if skills1 and skills2:
            skills_score = len(skills1 & skills2) / max(len(skills1 | skills2), 1)
            score += skills_score * 0.2
        
        return score
    
    def map_gutts(self, claude_gutts: List[Dict], gpt5_gutts: List[Dict], 
                  threshold: float = 0.3) -> Dict:
        """Map GUTTs between Claude and GPT-5 based on semantic similarity"""
        mapping = {
            "matches": [],      # (claude_gutt, gpt5_gutt, similarity)
            "claude_only": [],  # GUTTs unique to Claude
            "gpt5_only": [],    # GUTTs unique to GPT-5
        }
        
        # Track which GPT-5 GUTTs have been matched
        gpt5_matched = set()
        
        # For each Claude GUTT, find best GPT-5 match
        for c_gutt in claude_gutts:
            best_match = None
            best_score = threshold
            
            for i, g_gutt in enumerate(gpt5_gutts):
                if i in gpt5_matched:
                    continue
                
                score = self.compute_semantic_similarity(c_gutt, g_gutt)
                if score > best_score:
                    best_score = score
                    best_match = (i, g_gutt)
            
            if best_match:
                gpt5_matched.add(best_match[0])
                mapping["matches"].append((c_gutt, best_match[1], best_score))
            else:
                mapping["claude_only"].append(c_gutt)
        
        # Add unmatched GPT-5 GUTTs
        for i, g_gutt in enumerate(gpt5_gutts):
            if i not in gpt5_matched:
                mapping["gpt5_only"].append(g_gutt)
        
        return mapping
    
    def analyze_prompt(self, prompt_id: str, prompt_desc: str) -> Dict:
        """Perform detailed analysis for a single prompt"""
        print(f"\n{'='*100}")
        print(f"ANALYZING: {prompt_id} - {prompt_desc}")
        print(f"{'='*100}\n")
        
        claude_data, gpt5_data = self.load_prompt_data(prompt_id)
        
        claude_gutts = claude_data['gutts']
        gpt5_gutts = gpt5_data['gutts']
        
        print(f"Claude: {len(claude_gutts)} GUTTs")
        print(f"GPT-5:  {len(gpt5_gutts)} GUTTs")
        
        # Map GUTTs
        mapping = self.map_gutts(claude_gutts, gpt5_gutts)
        
        print(f"\nMapping Results:")
        print(f"  [MATCH] Matched pairs: {len(mapping['matches'])}")
        print(f"  [CLAUDE] Claude-only:  {len(mapping['claude_only'])}")
        print(f"  [GPT-5] GPT-5-only:    {len(mapping['gpt5_only'])}")
        
        # Show matches
        print(f"\n{'─'*100}")
        print(f"MATCHED GUTT PAIRS (semantic similarity > 0.3)")
        print(f"{'─'*100}")
        
        for i, (c_gutt, g_gutt, score) in enumerate(mapping['matches'], 1):
            print(f"\n{i}. Similarity: {score:.2f}")
            print(f"   Claude: {c_gutt['name']}")
            print(f"           {c_gutt['capability'][:80]}...")
            print(f"   GPT-5:  {g_gutt['name']}")
            print(f"           {g_gutt['capability'][:80]}...")
        
        # Show Claude-only
        if mapping['claude_only']:
            print(f"\n{'─'*100}")
            print(f"CLAUDE-ONLY GUTTs (no GPT-5 equivalent)")
            print(f"{'─'*100}")
            
            for i, gutt in enumerate(mapping['claude_only'], 1):
                print(f"\n{i}. {gutt['name']}")
                print(f"   {gutt['capability'][:80]}...")
                cats = self.categorize_capability(gutt['capability'])
                print(f"   Categories: {', '.join(cats)}")
        
        # Show GPT-5-only
        if mapping['gpt5_only']:
            print(f"\n{'─'*100}")
            print(f"GPT-5-ONLY GUTTs (no Claude equivalent)")
            print(f"{'─'*100}")
            
            for i, gutt in enumerate(mapping['gpt5_only'], 1):
                print(f"\n{i}. {gutt['name']}")
                print(f"   {gutt['capability'][:80]}...")
                cats = self.categorize_capability(gutt['capability'])
                print(f"   Categories: {', '.join(cats)}")
        
        return {
            "prompt_id": prompt_id,
            "prompt_desc": prompt_desc,
            "claude_count": len(claude_gutts),
            "gpt5_count": len(gpt5_gutts),
            "mapping": mapping,
            "claude_gutts": claude_gutts,
            "gpt5_gutts": gpt5_gutts,
        }
    
    def analyze_all_prompts(self) -> List[Dict]:
        """Analyze all prompts"""
        results = []
        
        for prompt_id, prompt_desc in self.prompts:
            result = self.analyze_prompt(prompt_id, prompt_desc)
            results.append(result)
        
        return results
    
    def consolidate_capabilities(self, results: List[Dict]) -> Dict:
        """Consolidate capabilities across all prompts to build canonical GUTT library"""
        print(f"\n\n{'='*100}")
        print(f"CROSS-PROMPT CAPABILITY CONSOLIDATION")
        print(f"{'='*100}\n")
        
        # Collect all unique capability descriptions
        capabilities = defaultdict(lambda: {
            "occurrences": [],
            "claude_count": 0,
            "gpt5_count": 0,
            "prompts": set(),
            "categories": set(),
            "skills": set(),
        })
        
        for result in results:
            prompt_id = result['prompt_id']
            
            # Claude GUTTs
            for gutt in result['claude_gutts']:
                cap_norm = self.normalize_text(gutt['capability'])
                capabilities[cap_norm]["occurrences"].append({
                    "source": "claude",
                    "prompt": prompt_id,
                    "name": gutt['name'],
                    "capability": gutt['capability'],
                })
                capabilities[cap_norm]["claude_count"] += 1
                capabilities[cap_norm]["prompts"].add(prompt_id)
                capabilities[cap_norm]["categories"].update(
                    self.categorize_capability(gutt['capability'])
                )
                capabilities[cap_norm]["skills"].update(gutt.get('required_skills', []))
            
            # GPT-5 GUTTs
            for gutt in result['gpt5_gutts']:
                cap_norm = self.normalize_text(gutt['capability'])
                capabilities[cap_norm]["occurrences"].append({
                    "source": "gpt5",
                    "prompt": prompt_id,
                    "name": gutt['name'],
                    "capability": gutt['capability'],
                })
                capabilities[cap_norm]["gpt5_count"] += 1
                capabilities[cap_norm]["prompts"].add(prompt_id)
                capabilities[cap_norm]["categories"].update(
                    self.categorize_capability(gutt['capability'])
                )
                capabilities[cap_norm]["skills"].update(gutt.get('required_skills', []))
        
        # Find capabilities that appear across multiple prompts
        cross_prompt_capabilities = {
            cap: data for cap, data in capabilities.items()
            if len(data["prompts"]) >= 2  # Appears in at least 2 prompts
        }
        
        print(f"Total unique capabilities: {len(capabilities)}")
        print(f"Cross-prompt capabilities (≥2 prompts): {len(cross_prompt_capabilities)}")
        
        # Sort by frequency
        sorted_caps = sorted(
            cross_prompt_capabilities.items(),
            key=lambda x: len(x[1]["prompts"]),
            reverse=True
        )
        
        print(f"\n{'─'*100}")
        print(f"TOP CROSS-PROMPT CAPABILITIES")
        print(f"{'─'*100}\n")
        
        for i, (cap_norm, data) in enumerate(sorted_caps[:20], 1):
            print(f"{i}. Appears in {len(data['prompts'])} prompts "
                  f"(Claude: {data['claude_count']}, GPT-5: {data['gpt5_count']})")
            print(f"   Categories: {', '.join(data['categories'])}")
            print(f"   Example: {data['occurrences'][0]['name']}")
            print(f"   Prompts: {', '.join(sorted(data['prompts']))}")
            print()
        
        return {
            "all_capabilities": capabilities,
            "cross_prompt_capabilities": cross_prompt_capabilities,
        }
    
    def generate_canonical_gutt_library(self, results: List[Dict], 
                                       consolidation: Dict) -> Dict:
        """Generate canonical GUTT library for Calendar.AI"""
        print(f"\n\n{'='*100}")
        print(f"CANONICAL GUTT LIBRARY GENERATION")
        print(f"{'='*100}\n")
        
        library = {
            "metadata": {
                "generated_date": "2025-11-06",
                "source_prompts": len(results),
                "total_gutts_analyzed": sum(r['claude_count'] + r['gpt5_count'] for r in results),
                "models": ["Claude Sonnet 4.5", "GPT-5 v2"],
            },
            "canonical_gutts": [],
        }
        
        # Group similar capabilities
        capability_groups = defaultdict(list)
        
        for result in results:
            for match in result['mapping']['matches']:
                c_gutt, g_gutt, score = match
                
                # Create canonical GUTT from matched pair
                canonical = {
                    "id": f"c_gutt_{len(library['canonical_gutts']) + 1}",
                    "canonical_name": c_gutt['name'],  # Prefer Claude naming
                    "alternative_names": [g_gutt['name']],
                    "capability": c_gutt['capability'],
                    "alternative_capabilities": [g_gutt['capability']],
                    "categories": list(self.categorize_capability(c_gutt['capability'])),
                    "required_skills": list(set(
                        c_gutt.get('required_skills', []) + 
                        g_gutt.get('required_skills', [])
                    )),
                    "sources": [
                        {"model": "Claude Sonnet 4.5", "prompt": result['prompt_id']},
                        {"model": "GPT-5 v2", "prompt": result['prompt_id']},
                    ],
                    "match_score": score,
                }
                
                library['canonical_gutts'].append(canonical)
        
        print(f"Generated {len(library['canonical_gutts'])} canonical GUTTs from matched pairs")
        
        # Add unique GUTTs from each model
        unique_claude = []
        unique_gpt5 = []
        
        for result in results:
            for gutt in result['mapping']['claude_only']:
                unique_claude.append({
                    "id": f"c_gutt_claude_{len(unique_claude) + 1}",
                    "canonical_name": gutt['name'],
                    "capability": gutt['capability'],
                    "categories": list(self.categorize_capability(gutt['capability'])),
                    "required_skills": gutt.get('required_skills', []),
                    "sources": [{"model": "Claude Sonnet 4.5", "prompt": result['prompt_id']}],
                    "note": "Unique to Claude - no GPT-5 equivalent found",
                })
            
            for gutt in result['mapping']['gpt5_only']:
                unique_gpt5.append({
                    "id": f"c_gutt_gpt5_{len(unique_gpt5) + 1}",
                    "canonical_name": gutt['name'],
                    "capability": gutt['capability'],
                    "categories": list(self.categorize_capability(gutt['capability'])),
                    "required_skills": gutt.get('required_skills', []),
                    "sources": [{"model": "GPT-5 v2", "prompt": result['prompt_id']}],
                    "note": "Unique to GPT-5 - no Claude equivalent found",
                })
        
        library['unique_claude_gutts'] = unique_claude
        library['unique_gpt5_gutts'] = unique_gpt5
        
        print(f"Added {len(unique_claude)} unique Claude GUTTs")
        print(f"Added {len(unique_gpt5)} unique GPT-5 GUTTs")
        print(f"\nTotal canonical GUTT library: {len(library['canonical_gutts']) + len(unique_claude) + len(unique_gpt5)} GUTTs")
        
        return library
    
    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        print("\n" + "="*100)
        print("GUTT CONSOLIDATION ANALYZER")
        print("Goal: Create canonical GUTT library for Calendar.AI evaluation framework")
        print("="*100)
        
        # Step 1: Per-prompt analysis
        results = self.analyze_all_prompts()
        
        # Step 2: Cross-prompt consolidation
        consolidation = self.consolidate_capabilities(results)
        
        # Step 3: Generate canonical library
        library = self.generate_canonical_gutt_library(results, consolidation)
        
        # Step 4: Save results
        output_path = Path("docs/gutt_analysis")
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save per-prompt analysis
        with open(output_path / "per_prompt_gutt_mapping.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        # Save canonical library
        with open(output_path / "canonical_gutt_library.json", 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=2, ensure_ascii=False)
        
        print(f"\n\n{'='*100}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*100}")
        print(f"\nOutput files:")
        print(f"  📄 {output_path / 'per_prompt_gutt_mapping.json'}")
        print(f"  📄 {output_path / 'canonical_gutt_library.json'}")
        print(f"\nNext steps:")
        print(f"  1. Review canonical GUTT library")
        print(f"  2. Manually validate and refine consolidation")
        print(f"  3. Use library to analyze new prompts")
        print(f"  4. Expand library as new capabilities are discovered\n")
        
        return results, consolidation, library


def main():
    analyzer = GUTTConsolidationAnalyzer()
    results, consolidation, library = analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
