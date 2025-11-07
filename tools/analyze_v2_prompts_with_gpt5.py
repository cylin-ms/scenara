#!/usr/bin/env python3
"""
Analyze V2 Hero Prompts using GPT-5 and 24 Canonical Tasks Framework

This script analyzes the v2 hero prompts from docs/9_hero_prompts_v2.txt
using GPT-5 to decompose them into the 24 canonical tasks framework.

Author: Chin-Yew Lin
Date: November 7, 2025
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

# Import GPT-5 infrastructure
try:
    from tools.gpt5_execution_composer import GPT5ExecutionComposer
except ImportError:
    try:
        from gpt5_execution_composer import GPT5ExecutionComposer
    except ImportError:
        print("ERROR: Could not import GPT5ExecutionComposer")
        print("Make sure tools/gpt5_execution_composer.py is available")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class V2PromptsAnalyzer:
    """Analyze v2 hero prompts using GPT-5 and 24 Canonical Tasks"""
    
    def __init__(self):
        """Initialize V2 Prompts Analyzer with GPT-5"""
        self.gpt5_composer = GPT5ExecutionComposer()
        self.v2_prompts_path = project_root / "docs/9_hero_prompts_v2.txt"
        self.gold_standard_path = project_root / "docs/gutt_analysis/CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md"
        
        logger.info("Initialized V2 Prompts Analyzer with GPT-5")
        
    def load_v2_prompts(self) -> Dict[str, str]:
        """Load v2 hero prompts from text file"""
        print(f"📖 Loading V2 Hero Prompts from: {self.v2_prompts_path}")
        
        if not self.v2_prompts_path.exists():
            raise FileNotFoundError(f"V2 prompts not found: {self.v2_prompts_path}")
        
        prompts = {}
        with open(self.v2_prompts_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Normalize non-breaking spaces to regular spaces
                line = line.replace('\xa0', ' ')
                
                if not line or line.startswith('#'):
                    continue
                
                # Parse format: "1. Organizer-1: "prompt text""
                if '. ' in line and ': ' in line:
                    parts = line.split(': ', 1)
                    if len(parts) == 2:
                        # Extract prompt ID (e.g., "Organizer-1")
                        id_part = parts[0].split('. ', 1)
                        if len(id_part) == 2:
                            prompt_id = id_part[1].strip()
                            # Remove quotes and clean prompt text
                            prompt_text = parts[1].strip().strip('"')
                            prompts[prompt_id] = prompt_text
        
        print(f"✅ Loaded {len(prompts)} v2 prompts:")
        for prompt_id in prompts.keys():
            print(f"   - {prompt_id}")
        
        return prompts
    
    def load_gold_standard(self) -> str:
        """Load 24 Canonical Tasks Gold Standard for context"""
        print(f"\n📚 Loading Gold Standard from: {self.gold_standard_path}")
        
        if not self.gold_standard_path.exists():
            raise FileNotFoundError(f"Gold standard not found: {self.gold_standard_path}")
        
        with open(self.gold_standard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Loaded gold standard ({len(content)} chars)")
        return content
    
    def analyze_prompt(self, prompt_id: str, prompt_text: str) -> Dict[str, Any]:
        """
        Analyze a single v2 prompt with GPT-5.
        
        Args:
            prompt_id: Prompt identifier (e.g., "Organizer-1")
            prompt_text: The actual prompt text
            
        Returns:
            Analysis results with canonical tasks, execution plan, etc.
        """
        print(f"\n🔍 Analyzing {prompt_id}...")
        print(f"   Prompt: {prompt_text[:80]}...")
        
        try:
            # Use GPT5ExecutionComposer to analyze the prompt
            result = self.gpt5_composer.compose_execution_plan(prompt_text, prompt_id=prompt_id)
            
            if result and 'execution_plan' in result:
                execution_plan = result.get('execution_plan', [])
                tasks_covered = result.get('tasks_covered', [])
                num_tasks = len(tasks_covered)
                num_steps = len(execution_plan)
                print(f"   ✅ Found {num_tasks} canonical tasks, {num_steps} execution steps")
                
                return {
                    'prompt_id': prompt_id,
                    'prompt_text': prompt_text,
                    'analysis': result,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print(f"   ⚠️ No results returned")
                return {
                    'prompt_id': prompt_id,
                    'prompt_text': prompt_text,
                    'error': 'No analysis results',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {
                'prompt_id': prompt_id,
                'prompt_text': prompt_text,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def analyze_all_prompts(self) -> Dict[str, Any]:
        """Analyze all v2 prompts and return comprehensive results"""
        
        # Load prompts and gold standard
        prompts = self.load_v2_prompts()
        gold_standard = self.load_gold_standard()
        
        print("\n" + "=" * 80)
        print("STARTING V2 PROMPTS ANALYSIS")
        print("=" * 80)
        
        results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'framework_version': '24 Canonical Tasks v2.0',
                'model': 'dev-gpt-5-chat-jj',
                'total_prompts': len(prompts),
                'prompts_file': str(self.v2_prompts_path),
                'gold_standard_file': str(self.gold_standard_path)
            },
            'prompts': []
        }
        
        # Analyze each prompt
        for prompt_id, prompt_text in prompts.items():
            analysis = self.analyze_prompt(prompt_id, prompt_text)
            results['prompts'].append(analysis)
        
        # Calculate summary statistics
        successful = sum(1 for p in results['prompts'] if 'error' not in p)
        failed = len(results['prompts']) - successful
        
        results['summary'] = {
            'total_analyzed': len(results['prompts']),
            'successful': successful,
            'failed': failed,
            'success_rate': f"{(successful/len(results['prompts'])*100):.1f}%"
        }
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"\nSuccessful: {successful}/{len(results['prompts'])}")
        print(f"Failed: {failed}/{len(results['prompts'])}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = project_root / "docs/gutt_analysis"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = output_dir / f"gpt5_v2_analysis_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {json_path}")
        
        return results
    
    def generate_comparison_report(self, v2_results: Dict[str, Any]) -> Path:
        """Generate markdown report comparing v2 results to gold standard"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = project_root / "docs/gutt_analysis"
        output_path = output_dir / f"GPT5_V2_Analysis_Report_{timestamp}.md"
        
        print(f"\n📊 Generating comparison report...")
        
        report = f"""# GPT-5 V2 Hero Prompts Analysis Report

**Date**: {datetime.now().strftime("%B %d, %Y")}  
**Model**: dev-gpt-5-chat-jj  
**Framework**: 24 Canonical Tasks v2.0  
**Prompts Analyzed**: {v2_results['metadata']['total_prompts']}

---

## Executive Summary

**Analysis Results**:
- **Total Prompts**: {v2_results['summary']['total_analyzed']}
- **Successful**: {v2_results['summary']['successful']}
- **Failed**: {v2_results['summary']['failed']}
- **Success Rate**: {v2_results['summary']['success_rate']}

**Framework**: 24 Canonical Tasks (23 unique + CAN-02A/CAN-02B split)
- **Tier 1 (Universal)**: 5 tasks - Core foundational capabilities
- **Tier 2 (Common)**: 9 tasks - Frequently used capabilities
- **Tier 3 (Specialized)**: 10 tasks - Advanced/specialized capabilities

---

## Prompt-by-Prompt Analysis

"""
        
        # Add analysis for each prompt
        for prompt_data in v2_results['prompts']:
            prompt_id = prompt_data['prompt_id']
            prompt_text = prompt_data['prompt_text']
            
            report += f"### {prompt_id}\n\n"
            report += f"**Prompt**: \"{prompt_text}\"\n\n"
            
            if 'error' in prompt_data:
                report += f"❌ **Error**: {prompt_data['error']}\n\n"
                report += "---\n\n"
                continue
            
            analysis = prompt_data.get('analysis', {})
            execution_plan = analysis.get('execution_plan', [])
            tasks_covered = analysis.get('tasks_covered', [])
            
            # Canonical Tasks
            report += f"**Canonical Tasks**: {len(tasks_covered)} tasks identified\n\n"
            if tasks_covered:
                report += "**Task IDs**: " + ", ".join(tasks_covered) + "\n\n"
            
            # Execution Plan
            num_steps = len(execution_plan)
            
            report += f"**Execution Plan**: {num_steps} steps\n\n"
            
            if execution_plan:
                report += "**Steps**:\n"
                for i, step in enumerate(execution_plan, 1):
                    task_id = step.get('task_id', 'Unknown')
                    task_name = step.get('task_name', 'Unknown')
                    description = step.get('description', '')
                    report += f"{i}. **{task_id}**: {task_name}\n"
                    if description:
                        report += f"   - {description}\n"
                report += "\n"
            
            report += "---\n\n"
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Report saved to: {output_path}")
        return output_path


def main():
    """Main execution function"""
    
    print("=" * 80)
    print("GPT-5 V2 HERO PROMPTS ANALYZER")
    print("24 Canonical Tasks Framework")
    print("=" * 80)
    print()
    
    analyzer = V2PromptsAnalyzer()
    
    try:
        # Run analysis
        results = analyzer.analyze_all_prompts()
        
        # Generate comparison report
        analyzer.generate_comparison_report(results)
        
        print("\n✅ V2 Analysis pipeline complete!")
        print("\nNext steps:")
        print("1. Review JSON results for detailed canonical task mappings")
        print("2. Review markdown report for human-readable analysis")
        print("3. Compare v2 results with v1 to validate consistency")
        print("4. Update gold standard if v2 reveals new patterns")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure the following files exist:")
        print("- docs/9_hero_prompts_v2.txt")
        print("- docs/gutt_analysis/CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
