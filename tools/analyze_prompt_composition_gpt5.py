#!/usr/bin/env python3
"""
Analyze Calendar.AI Hero Prompts using GPT-5 and Canonical Unit Tasks Library

This script uses GPT-5 to decompose hero prompts into canonical unit tasks,
providing coverage analysis, implementation recommendations, and effort estimates.

Author: Chin-Yew Lin
Date: November 6, 2025
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import GPT-5 Meeting Classifier infrastructure
try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, DEFAULT_ENDPOINT, DEFAULT_MODEL
except ImportError:
    try:
        from meeting_classifier_gpt5 import GPT5MeetingClassifier, DEFAULT_ENDPOINT, DEFAULT_MODEL
    except ImportError:
        print("ERROR: Could not import GPT5MeetingClassifier")
        print("Make sure tools/meeting_classifier_gpt5.py is available")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CanonicalTaskAnalyzer:
    """Analyze prompts using GPT-5 and Canonical Unit Tasks library"""
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        endpoint: str = DEFAULT_ENDPOINT,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """
        Initialize Canonical Task Analyzer with GPT-5.
        
        Args:
            model: GPT-5 model name (default: dev-gpt-5-chat-jj)
            endpoint: SilverFlow API endpoint
            max_retries: Maximum retry attempts for rate limiting
            retry_delay: Delay between retries in seconds
        """
        self.model = model
        self.endpoint = endpoint
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize GPT-5 client
        self.gpt5_client = GPT5MeetingClassifier(
            model=model,
            endpoint=endpoint,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        self.canonical_tasks_path = project_root / "docs/gutt_analysis/CANONICAL_UNIT_TASKS_REFERENCE.md"
        self.hero_prompts_path = project_root / "docs/gutt_analysis/Hero_Prompts_Reference_GUTT_Decompositions.md"
        self.canonical_library = None
        
        logger.info(f"Initialized Canonical Task Analyzer with model: {model}")
        
    def load_canonical_library(self) -> str:
        """Load the Canonical Unit Tasks reference document"""
        print(f"📚 Loading Canonical Tasks Library from: {self.canonical_tasks_path}")
        
        if not self.canonical_tasks_path.exists():
            raise FileNotFoundError(f"Canonical library not found: {self.canonical_tasks_path}")
        
        with open(self.canonical_tasks_path, 'r', encoding='utf-8') as f:
            self.canonical_library = f.read()
        
        print(f"✅ Loaded {len(self.canonical_library)} characters")
        return self.canonical_library
    
    def load_hero_prompts(self) -> Dict[str, str]:
        """Load hero prompts from reference document"""
        print(f"\n📖 Loading Hero Prompts from: {self.hero_prompts_path}")
        
        if not self.hero_prompts_path.exists():
            raise FileNotFoundError(f"Hero prompts not found: {self.hero_prompts_path}")
        
        with open(self.hero_prompts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract prompts (simplified - looking for prompt sections)
        prompts = {}
        
        # Define the 9 hero prompts manually for clarity
        prompts_text = {
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
        
        prompts = prompts_text
        print(f"✅ Loaded {len(prompts)} hero prompts")
        
        return prompts
    
    def analyze_prompt_with_gpt5(self, prompt_id: str, prompt_text: str) -> Dict[str, Any]:
        """
        Use GPT-5 to analyze a prompt against the canonical tasks library
        
        Returns:
            Dictionary with analysis results including:
            - canonical_tasks: List of identified tasks
            - coverage_percentage: Coverage score
            - implementation_effort: Effort estimate
            - recommendations: Implementation recommendations
        """
        print(f"\n🤖 Analyzing {prompt_id} with GPT-5...")
        print(f"   Prompt: {prompt_text[:80]}...")
        
        # Construct analysis prompt for GPT-5
        analysis_prompt = f"""You are a Calendar.AI expert analyzing user prompts.

Your task: Analyze the given prompt and decompose it into the atomic Canonical Unit Tasks required to fulfill it.

CANONICAL UNIT TASKS LIBRARY:
{self.canonical_library}

USER PROMPT TO ANALYZE:
ID: {prompt_id}
Text: "{prompt_text}"

ANALYSIS INSTRUCTIONS:
1. Identify ALL canonical tasks needed (use task IDs: CAN-01, CAN-02, etc.)
2. Design an EXECUTION PLAN showing how tasks compose together computationally
3. For each step, show:
   - Which canonical task is used
   - Input data (what it receives)
   - Processing/transformation (what it does)
   - Output data (what it produces)
   - How output flows to next task
4. Show the complete data flow from user input to final result
5. Identify any orchestration logic needed between tasks

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
        "schema": "Brief schema or example"
      }},
      "processing": "Detailed description of the transformation/computation",
      "output": {{
        "description": "What data this step produces",
        "schema": "Brief schema or example"
      }},
      "flows_to": ["step_2", "step_5"]
    }}
  ],
  "data_flow_summary": "High-level description of how data flows through the composition",
  "orchestration_logic": [
    "Conditional logic needed",
    "Error handling requirements",
    "Retry or fallback strategies"
  ],
  "composition_pattern": "sequential|parallel|conditional|iterative",
  "final_output": {{
    "type": "JSON|UI_display|API_response|calendar_update",
    "description": "What the user ultimately receives",
    "schema": "Expected output structure"
  }}
}}

Provide ONLY the JSON output, no additional text.
"""
        
        try:
            # Construct system message
            system_message = """You are an expert at designing computational workflows for Calendar.AI prompts.

Your task: Analyze the given prompt and design an EXECUTION PLAN showing how Canonical Unit Tasks compose together to fulfill the request.

Focus on:
- Data flow and transformations
- How tasks chain together
- Input/output of each step
- Orchestration logic between tasks

Think like a software architect designing a processing pipeline."""
            
            # Call GPT-5 API using the same pattern as gpt5_gutt_analyzer
            result = self.gpt5_client._call_gpt5_api(
                system_message=system_message,
                user_prompt=analysis_prompt,
                timeout=60
            )
            
            if not result.success:
                logger.error(f"GPT-5 API call failed: {result.error}")
                return {
                    "error": result.error,
                    "prompt_id": prompt_id
                }
            
            # Parse JSON response
            response_text = result.response_content or ""
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(response_text)
            
            print(f"✅ Analysis complete:")
            print(f"   Tasks identified: {analysis['coverage_analysis']['total_tasks_identified']}")
            print(f"   Coverage: {analysis['coverage_analysis']['coverage_percentage']:.1f}%")
            print(f"   Effort: {analysis['implementation_effort']}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT-5 response as JSON: {e}")
            logger.debug(f"Response: {response_text[:200]}...")
            return {
                "error": "JSON parsing failed",
                "raw_response": response_text,
                "prompt_id": prompt_id
            }
        except Exception as e:
            logger.error(f"Error during GPT-5 analysis: {e}")
            return {
                "error": str(e),
                "prompt_id": prompt_id
            }
    
    def analyze_all_prompts(self, output_file: str = None) -> Dict[str, Any]:
        """Analyze all hero prompts and generate comprehensive report"""
        
        # Load resources
        self.load_canonical_library()
        hero_prompts = self.load_hero_prompts()
        
        # Analyze each prompt
        results = {
            "metadata": {
                "analysis_date": datetime.now().isoformat(),
                "analyzer": "GPT-5 with Canonical Unit Tasks Library",
                "total_prompts": len(hero_prompts),
                "library_version": "1.0",
                "author": "Chin-Yew Lin"
            },
            "prompt_analyses": {}
        }
        
        print("\n" + "="*80)
        print("🚀 STARTING CANONICAL TASK ANALYSIS")
        print("="*80)
        
        for prompt_id, prompt_text in hero_prompts.items():
            analysis = self.analyze_prompt_with_gpt5(prompt_id, prompt_text)
            results["prompt_analyses"][prompt_id] = analysis
        
        # Generate summary statistics
        total_tasks = 0
        total_implemented = 0
        total_needs_impl = 0
        effort_distribution = {"Low": 0, "Medium": 0, "High": 0}
        
        for prompt_id, analysis in results["prompt_analyses"].items():
            if "error" not in analysis:
                total_tasks += analysis["coverage_analysis"]["total_tasks_identified"]
                total_implemented += analysis["coverage_analysis"]["implemented_tasks"]
                total_needs_impl += analysis["coverage_analysis"]["needs_implementation"]
                effort_distribution[analysis["implementation_effort"]] += 1
        
        results["summary"] = {
            "total_canonical_tasks_used": total_tasks,
            "average_tasks_per_prompt": round(total_tasks / len(hero_prompts), 2),
            "total_implemented": total_implemented,
            "total_needs_implementation": total_needs_impl,
            "overall_coverage_percentage": round((total_implemented / total_tasks * 100) if total_tasks > 0 else 0, 2),
            "effort_distribution": effort_distribution
        }
        
        # Save results
        if output_file is None:
            output_file = project_root / f"docs/gutt_analysis/gpt5_canonical_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*80)
        print("📊 ANALYSIS COMPLETE")
        print("="*80)
        print(f"\n📁 Results saved to: {output_path}")
        print(f"\n📈 Summary Statistics:")
        print(f"   Total prompts analyzed: {len(hero_prompts)}")
        print(f"   Total canonical tasks used: {total_tasks}")
        print(f"   Average tasks per prompt: {results['summary']['average_tasks_per_prompt']}")
        print(f"   Overall coverage: {results['summary']['overall_coverage_percentage']:.1f}%")
        print(f"\n   Implementation effort distribution:")
        for effort, count in effort_distribution.items():
            print(f"      {effort}: {count} prompts")
        
        return results
    
    def generate_markdown_report(self, results: Dict[str, Any], output_file: str = None):
        """Generate a human-readable markdown report from analysis results"""
        
        if output_file is None:
            output_file = project_root / f"docs/gutt_analysis/GPT5_Canonical_Analysis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        output_path = Path(output_file)
        
        report = f"""# GPT-5 Canonical Unit Tasks Analysis Report

**Author**: {results['metadata']['author']}  
**Date**: {results['metadata']['analysis_date']}  
**Analyzer**: {results['metadata']['analyzer']}  
**Library Version**: {results['metadata']['library_version']}

---

## Executive Summary

**Total Prompts Analyzed**: {results['metadata']['total_prompts']}  
**Total Canonical Tasks Used**: {results['summary']['total_canonical_tasks_used']}  
**Average Tasks per Prompt**: {results['summary']['average_tasks_per_prompt']}  
**Overall Coverage**: {results['summary']['overall_coverage_percentage']}%

**Implementation Effort Distribution**:
"""
        
        for effort, count in results['summary']['effort_distribution'].items():
            report += f"- {effort}: {count} prompts\n"
        
        report += "\n---\n\n## Per-Prompt Analysis\n\n"
        
        # Generate detailed analysis for each prompt
        for prompt_id, analysis in results['prompt_analyses'].items():
            if "error" in analysis:
                report += f"### {prompt_id} ❌ ERROR\n\n"
                report += f"**Error**: {analysis['error']}\n\n"
                continue
            
            report += f"### {prompt_id}\n\n"
            report += f"**Prompt**: \"{analysis['prompt_text']}\"\n\n"
            report += f"**Implementation Effort**: {analysis['implementation_effort']}  \n"
            report += f"**Coverage**: {analysis['coverage_analysis']['coverage_percentage']:.1f}%\n\n"
            
            # Canonical tasks
            report += "**Canonical Tasks Required**:\n\n"
            for task in analysis['canonical_tasks']:
                status_icon = "✅" if task['implementation_status'] == "implemented" else "⚠️"
                report += f"{status_icon} **{task['task_id']}: {task['task_name']}** (Tier {task['tier']})\n"
                report += f"   - Why needed: {task['why_needed']}\n"
                report += f"   - How used: {task['how_used']}\n\n"
            
            # Execution sequence
            report += "**Execution Sequence**:\n\n"
            for i, step in enumerate(analysis['execution_sequence'], 1):
                report += f"{i}. {step}\n"
            
            report += "\n**Recommendations**:\n\n"
            for rec in analysis['recommendations']:
                report += f"- {rec}\n"
            
            report += "\n---\n\n"
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Markdown report saved to: {output_path}")
        return output_path


def main():
    """Main execution function"""
    
    print("=" * 80)
    print("GPT-5 CANONICAL UNIT TASKS ANALYZER")
    print("=" * 80)
    print()
    
    analyzer = CanonicalTaskAnalyzer()
    
    try:
        # Run analysis
        results = analyzer.analyze_all_prompts()
        
        # Generate markdown report
        analyzer.generate_markdown_report(results)
        
        print("\n✅ Analysis pipeline complete!")
        print("\nNext steps:")
        print("1. Review the JSON results for detailed analysis")
        print("2. Review the markdown report for human-readable summary")
        print("3. Use insights to prioritize implementation work")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure the following files exist:")
        print("- docs/gutt_analysis/CANONICAL_UNIT_TASKS_REFERENCE.md")
        print("- docs/gutt_analysis/Hero_Prompts_Reference_GUTT_Decompositions.md")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
