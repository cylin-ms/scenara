#!/usr/bin/env python3
"""
Analyze Hero Prompts with GPT-5: EXECUTION COMPOSITION Focus
Shows how Canonical Tasks compose together computationally
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, DEFAULT_ENDPOINT, DEFAULT_MODEL

class CompositionAnalyzer:
    """Analyze prompts for execution composition using GPT-5"""
    
    def __init__(self):
        self.gpt5_client = GPT5MeetingClassifier(
            model=DEFAULT_MODEL,
            endpoint=DEFAULT_ENDPOINT
        )
        self.canonical_library = self._load_canonical_library()
        self.hero_prompts = self._load_hero_prompts()
        
    def _load_canonical_library(self) -> str:
        """Load the canonical tasks library"""
        lib_path = project_root / "docs/gutt_analysis/CANONICAL_UNIT_TASKS_REFERENCE.md"
        print(f"[LOADING] Canonical Tasks Library from {lib_path.name}")
        
        with open(lib_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"[OK] Loaded {len(content):,} characters")
        return content
    
    def _load_hero_prompts(self) -> Dict[str, str]:
        """Load hero prompts - 9 hero prompts from analysis"""
        print(f"[LOADING] Hero Prompts (9 prompts)")
        
        prompts = {
            "organizer-1": "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy.",
            
            "organizer-2": "I have some important meetings this week—flag the ones I need to prep for, and put time on my calendar to prepare.",
            
            "organizer-3": "I'm spending too much time in meetings. Help me find patterns in my calendar and identify opportunities to reclaim time.",
            
            "schedule-1": "Land a weekly 30min 1:1 with Sarah for me, afternoons preferred, avoid Fridays. If her schedule changes, automatically find a new time.",
            
            "schedule-2": "Clear my Thursday afternoon—reschedule what you can, and decline the rest.",
            
            "schedule-3": "Land a time for Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s if needed, work around Kat's schedule. In person with a room.",
            
            "collaborate-1": "I have a Project Alpha review coming up. Help me set the agenda based on what the team has been working on.",
            
            "collaborate-2": "I have an executive meeting in 2 hours. Pull together a briefing on the topics we'll be discussing.",
            
            "collaborate-3": "I have a customer meeting tomorrow. Give me a dossier on the attendees and recent interactions."
        }
        
        print(f"[OK] Loaded {len(prompts)} hero prompts")
        return prompts
    
    def analyze_prompt(self, prompt_id: str, prompt_text: str) -> Dict:
        """Analyze a single prompt for execution composition"""
        
        print(f"\n{'='*80}")
        print(f"[ANALYZING] {prompt_id}")
        print(f"{'='*80}")
        print(f"Prompt: {prompt_text[:100]}...")
        
        # Construct analysis prompt
        analysis_prompt = f"""You are an expert at designing computational workflows for Calendar.AI prompts.

CANONICAL UNIT TASKS LIBRARY:
{self.canonical_library}

USER PROMPT TO ANALYZE:
ID: {prompt_id}
Text: "{prompt_text}"

ANALYSIS INSTRUCTIONS:
1. Identify ALL canonical tasks needed (use task IDs: CAN-01, CAN-02, etc.)
2. Design an EXECUTION PLAN showing how tasks compose together computationally
3. For each step, show:
   - Which canonical task is used (with tier)
   - Input data (what it receives - type, description, schema)
   - Processing/transformation (what it does in detail)
   - Output data (what it produces - description, schema)
   - How output flows to next tasks
4. Show the complete data flow from user input to final result
5. Identify orchestration logic needed:
   - Conditional branching
   - Error handling requirements
   - Retry or fallback strategies
   - Parallel vs sequential execution

OUTPUT FORMAT (JSON):
{{
  "prompt_id": "{prompt_id}",
  "prompt_text": "{prompt_text}",
  "execution_plan": [
    {{
      "step": 1,
      "task_id": "CAN-XX",
      "task_name": "Task Name",
      "tier": 1,
      "input": {{
        "type": "user_prompt|previous_step_output|external_data",
        "description": "What data this step receives",
        "schema": "Brief schema or example (JSON object/array)"
      }},
      "processing": "Detailed description of the transformation/computation performed",
      "output": {{
        "description": "What data this step produces",
        "schema": "Brief schema or example (JSON object/array)"
      }},
      "flows_to": ["step_2", "step_5"]
    }}
  ],
  "data_flow_summary": "High-level description of how data flows through the composition",
  "orchestration_logic": [
    "Specific orchestration requirement 1",
    "Specific orchestration requirement 2"
  ],
  "composition_pattern": "sequential|parallel|conditional|iterative|hybrid",
  "final_output": {{
    "type": "JSON|UI_display|API_response|calendar_update",
    "description": "What the user ultimately receives",
    "schema": "Expected output structure"
  }}
}}

Provide ONLY the JSON output, no additional text.
Focus on showing the COMPUTATIONAL PIPELINE - how data transforms at each step.
"""

        # Call GPT-5
        print("[GPT-5] Analyzing composition...")
        
        system_message = """You are an expert at designing computational workflows for Calendar.AI prompts.
Focus on data flow, transformations, and how tasks compose together.
Think like a software architect designing a processing pipeline.
Always respond with valid JSON."""

        result = self.gpt5_client._call_gpt5_api(
            system_message=system_message,
            user_prompt=analysis_prompt,
            timeout=60
        )
        
        if not result.success:
            print(f"[ERROR] GPT-5 API call failed: {result.error}")
            return {
                "prompt_id": prompt_id,
                "error": result.error,
                "status": "failed"
            }
        
        # Parse JSON response
        response_text = result.response_content.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        try:
            analysis = json.loads(response_text)
            print(f"[OK] Received execution plan with {len(analysis.get('execution_plan', []))} steps")
            print(f"     Composition: {analysis.get('composition_pattern', 'N/A')}")
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON: {e}")
            print(f"[DEBUG] First 200 chars: {response_text[:200]}")
            return {
                "prompt_id": prompt_id,
                "error": f"JSON parse error: {str(e)}",
                "raw_response": response_text[:500],
                "status": "parse_failed"
            }
    
    def analyze_all_prompts(self) -> List[Dict]:
        """Analyze all hero prompts"""
        results = []
        
        print(f"\n{'='*80}")
        print(f"STARTING COMPOSITION ANALYSIS FOR {len(self.hero_prompts)} PROMPTS")
        print(f"{'='*80}\n")
        
        for i, (prompt_id, prompt_text) in enumerate(self.hero_prompts.items(), 1):
            print(f"\n[{i}/{len(self.hero_prompts)}] Processing {prompt_id}...")
            
            analysis = self.analyze_prompt(prompt_id, prompt_text)
            results.append(analysis)
        
        return results
    
    def save_results(self, results: List[Dict]):
        """Save analysis results to JSON and Markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_path = project_root / f"docs/gutt_analysis/gpt5_composition_analysis_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "timestamp": timestamp,
                    "total_prompts": len(results),
                    "model": DEFAULT_MODEL,
                    "endpoint": DEFAULT_ENDPOINT,
                    "analysis_type": "execution_composition"
                },
                "results": results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SAVED] JSON results to {json_path.name}")
        
        # Generate Markdown report
        md_path = project_root / f"docs/gutt_analysis/GPT5_Composition_Report_{timestamp}.md"
        self._generate_markdown_report(results, md_path, timestamp)
        
        print(f"[SAVED] Markdown report to {md_path.name}")
        
        # Summary
        successful = sum(1 for r in results if 'execution_plan' in r)
        failed = len(results) - successful
        total_steps = sum(len(r.get('execution_plan', [])) for r in results)
        
        print(f"\n{'='*80}")
        print(f"ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"Total prompts analyzed: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total execution steps: {total_steps}")
        print(f"Average steps per prompt: {total_steps/len(results):.1f}")
        print(f"{'='*80}\n")
    
    def _generate_markdown_report(self, results: List[Dict], output_path: Path, timestamp: str):
        """Generate comprehensive markdown report"""
        
        lines = []
        lines.append("# GPT-5 Execution Composition Analysis Report")
        lines.append("")
        lines.append(f"**Generated**: {timestamp}")
        lines.append(f"**Model**: {DEFAULT_MODEL}")
        lines.append(f"**Analysis Type**: Execution Composition & Data Flow")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Executive Summary
        successful = [r for r in results if 'execution_plan' in r]
        total_steps = sum(len(r.get('execution_plan', [])) for r in successful)
        
        # Count composition patterns
        patterns = {}
        for r in successful:
            pattern = r.get('composition_pattern', 'unknown')
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(f"- **Total Prompts Analyzed**: {len(results)}")
        lines.append(f"- **Successful Analyses**: {len(successful)}")
        lines.append(f"- **Total Execution Steps**: {total_steps}")
        lines.append(f"- **Average Steps per Prompt**: {total_steps/len(successful):.1f}")
        lines.append("")
        lines.append("### Composition Patterns")
        lines.append("")
        for pattern, count in sorted(patterns.items(), key=lambda x: -x[1]):
            lines.append(f"- **{pattern}**: {count} prompts")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Per-prompt detailed analysis
        lines.append("## Detailed Execution Plans")
        lines.append("")
        
        for i, result in enumerate(successful, 1):
            prompt_id = result.get('prompt_id', f'unknown-{i}')
            prompt_text = result.get('prompt_text', 'N/A')
            
            lines.append(f"### {i}. {prompt_id}")
            lines.append("")
            lines.append(f"**Prompt**: {prompt_text}")
            lines.append("")
            lines.append(f"**Composition Pattern**: {result.get('composition_pattern', 'N/A')}")
            lines.append("")
            
            # Execution Plan
            execution_plan = result.get('execution_plan', [])
            lines.append(f"**Execution Steps**: {len(execution_plan)}")
            lines.append("")
            
            for step in execution_plan:
                step_num = step.get('step', '?')
                task_id = step.get('task_id', 'N/A')
                task_name = step.get('task_name', 'N/A')
                tier = step.get('tier', '?')
                
                lines.append(f"#### Step {step_num}: {task_id} - {task_name} (Tier {tier})")
                lines.append("")
                
                # Input
                input_info = step.get('input', {})
                lines.append(f"**Input**:")
                lines.append(f"- Type: `{input_info.get('type', 'N/A')}`")
                lines.append(f"- Description: {input_info.get('description', 'N/A')}")
                if 'schema' in input_info:
                    lines.append(f"- Schema: `{json.dumps(input_info['schema'])}`")
                lines.append("")
                
                # Processing
                lines.append(f"**Processing**: {step.get('processing', 'N/A')}")
                lines.append("")
                
                # Output
                output_info = step.get('output', {})
                lines.append(f"**Output**:")
                lines.append(f"- Description: {output_info.get('description', 'N/A')}")
                if 'schema' in output_info:
                    lines.append(f"- Schema: `{json.dumps(output_info['schema'])}`")
                lines.append("")
                
                # Data flow
                flows_to = step.get('flows_to', [])
                if flows_to:
                    lines.append(f"**Flows To**: {', '.join(flows_to)}")
                else:
                    lines.append(f"**Flows To**: [Final Output]")
                lines.append("")
            
            # Data Flow Summary
            lines.append("**Data Flow Summary**:")
            lines.append("")
            lines.append(result.get('data_flow_summary', 'N/A'))
            lines.append("")
            
            # Orchestration Logic
            orchestration = result.get('orchestration_logic', [])
            if orchestration:
                lines.append("**Orchestration Logic**:")
                lines.append("")
                for logic in orchestration:
                    lines.append(f"- {logic}")
                lines.append("")
            
            # Final Output
            final_output = result.get('final_output', {})
            lines.append("**Final Output**:")
            lines.append(f"- Type: `{final_output.get('type', 'N/A')}`")
            lines.append(f"- Description: {final_output.get('description', 'N/A')}")
            if 'schema' in final_output:
                lines.append(f"- Schema: `{json.dumps(final_output['schema'])}`")
            lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def main():
    """Main execution"""
    analyzer = CompositionAnalyzer()
    results = analyzer.analyze_all_prompts()
    analyzer.save_results(results)


if __name__ == "__main__":
    main()
