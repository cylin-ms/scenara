#!/usr/bin/env python3
"""
GUTT Analysis Using Anthropic Claude API

Uses Claude Sonnet models via Anthropic API to perform GUTT decomposition
with better accuracy than local Ollama models.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

try:
    import anthropic
except ImportError:
    print("❌ anthropic package not installed. Install with: pip install anthropic")
    sys.exit(1)


class ClaudeGUTTAnalyzer:
    """Analyze prompts using Claude API to identify GUTT tasks"""
    
    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str = None):
        """
        Initialize Claude analyzer
        
        Args:
            model: Claude model name (claude-sonnet-4-20250514, claude-sonnet-3-5-20241022, etc.)
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
        """
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY env var or pass api_key parameter")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def decompose_prompt_to_gutts(self, user_prompt: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Decompose user prompt into GUTT tasks using Claude
        
        Args:
            user_prompt: The original user prompt to analyze
            verbose: Whether to show progress
            
        Returns:
            Dictionary with GUTT decomposition
        """
        
        # Read GUTT framework documentation for context
        gutt_context = self._load_gutt_context()
        
        analysis_prompt = f"""You are an expert AI system evaluator specializing in GUTT (Granular Unit Task Taxonomy) analysis using the GUTT v4.0 ACRUE framework.

{gutt_context}

Your task: Analyze the following user prompt and decompose it into constituent GUTT tasks (unit tasks).

**User Prompt**: "{user_prompt}"

**CRITICAL Instructions for GUTT Decomposition**:

1. **Granularity Level**: Decompose into ATOMIC unit tasks, not high-level capabilities
   - Each GUTT = ONE specific capability/operation
   - Typical complexity: 3-9 GUTTs for standard requests
   - Each GUTT should map to a distinct implementation component

2. **Unit Task Definition**:
   - Single, clear purpose (not a group of capabilities)
   - Independently implementable component
   - Distinct skill requirement
   - Can be evaluated separately for ACRUE quality

3. **Avoid These Mistakes**:
   - ❌ Grouping multiple capabilities into one GUTT
   - ❌ Using vague verbs like "handle", "manage", "process"
   - ❌ Combining data retrieval + analysis + output in single GUTT
   - ✅ Separate each distinct operation into its own GUTT

4. **Self-Check After Decomposition**:
   For each GUTT, verify:
   - Does this represent ONE atomic capability?
   - Could this be split into smaller unit tasks? (if yes, split it)
   - Does this require multiple distinct skills? (if yes, decompose further)

**Output Format**: Respond ONLY with valid JSON in this exact structure:
{{
  "analysis": {{
    "original_prompt": "{user_prompt}",
    "total_gutts_identified": <number>,
    "gutts": [
      {{
        "id": "gutt_1",
        "name": "<Concise GUTT name>",
        "capability": "<What this atomic unit task does>",
        "required_skills": ["skill1", "skill2"],
        "user_goal": "<What user wants to achieve with this GUTT>",
        "triggered": true,
        "evidence": "<Evidence this GUTT would be executed>"
      }}
    ]
  }}
}}

**Important**: 
- Output ONLY valid JSON, no markdown formatting, no explanations outside JSON
- Focus on ATOMIC unit tasks, not capability groups
- Be specific about required skills for each GUTT
- Ensure proper granularity (not too coarse, not too fine)

Analyze the prompt now and output the GUTT decomposition:"""

        if verbose:
            print(f"\n🤖 Querying Claude ({self.model}) for GUTT decomposition...")
            print(f"   Prompt: {user_prompt[:100]}...")
            print("\n" + "=" * 80)
        
        try:
            # Query Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            if verbose:
                print("Claude Response Received")
                print("=" * 80 + "\n")
            
            # Parse JSON response
            try:
                # Try to find JSON in response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx == -1 or end_idx == 0:
                    print("⚠️  No JSON found in response")
                    return self._create_error_response(user_prompt, "No JSON in response")
                
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Validate structure
                if 'analysis' not in result:
                    print("⚠️  Invalid JSON structure (missing 'analysis' key)")
                    return self._create_error_response(user_prompt, "Invalid structure")
                
                return result['analysis']
            
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print(f"   Response: {response_text[:500]}...")
                return self._create_error_response(user_prompt, str(e))
        
        except Exception as e:
            print(f"❌ Error querying Claude API: {e}")
            return self._create_error_response(user_prompt, str(e))
    
    def _load_gutt_context(self) -> str:
        """Load GUTT framework context from documentation"""
        context_parts = []
        
        # Try to load GUTT v4.0 documentation
        gutt_docs = [
            "docs/GUTT_v4.0_ACRUE_Integration_Documentation.md",
            "Hero_Prompts_Reference_GUTT_Decompositions.md"
        ]
        
        for doc_path in gutt_docs:
            if Path(doc_path).exists():
                try:
                    with open(doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Take first 1000 chars as context
                        context_parts.append(content[:1000])
                except:
                    pass
        
        if context_parts:
            return "\n\n**GUTT Framework Context**:\n" + "\n---\n".join(context_parts)
        else:
            return """**GUTT Framework Context**:
GUTT = Granular Unit Task Taxonomy
- Break down complex requests into atomic unit tasks
- Each unit task represents a single, specific capability
- Typical requests decompose into 3-9 unit tasks
- Each GUTT should be independently implementable and evaluable"""
    
    def _create_error_response(self, prompt: str, error: str) -> Dict[str, Any]:
        """Create error response structure"""
        return {
            "original_prompt": prompt,
            "total_gutts_identified": 0,
            "gutts": [],
            "error": error
        }
    
    def save_decomposition(self, decomposition: Dict[str, Any], output_file: str):
        """Save GUTT decomposition to file"""
        evaluator_format = {
            "source": f"claude_{self.model}",
            "backend_llm": self.model,
            "backend_llm_notes": f"Anthropic Claude API - {self.model}",
            "timestamp": datetime.now().isoformat(),
            "original_prompt": decomposition.get("original_prompt", ""),
            "gutts": decomposition.get("gutts", []),
            "track1_score": None,
            "track2_score": None,
            "overall_score": None,
            "notes": f"Generated by Claude {self.model} via Anthropic API"
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(evaluator_format, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Decomposition saved to: {output_file}")
    
    def print_decomposition_summary(self, decomposition: Dict[str, Any]):
        """Print formatted summary of decomposition"""
        print("\n" + "=" * 80)
        print("📋 GUTT DECOMPOSITION SUMMARY")
        print("=" * 80)
        print(f"\n🤖 Backend LLM: {self.model} (Anthropic Claude API)")
        
        print(f"\n📝 Original Prompt: {decomposition.get('original_prompt', 'N/A')}")
        print(f"\n🎯 Total GUTTs Identified: {decomposition.get('total_gutts_identified', 0)}")
        
        if 'error' in decomposition:
            print(f"\n❌ Error: {decomposition['error']}")
            return
        
        gutts = decomposition.get('gutts', [])
        
        for i, gutt in enumerate(gutts, 1):
            print(f"\n{i}. {gutt.get('name', 'Unnamed GUTT')}")
            print(f"   ID: {gutt.get('id', 'N/A')}")
            print(f"   Capability: {gutt.get('capability', 'N/A')}")
            print(f"   Required Skills: {', '.join(gutt.get('required_skills', []))}")
            print(f"   User Goal: {gutt.get('user_goal', 'N/A')}")
            print(f"   Triggered: {'✅ Yes' if gutt.get('triggered') else '❌ No'}")
            if gutt.get('evidence'):
                print(f"   Evidence: {gutt.get('evidence')}")
        
        print("\n" + "=" * 80)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GUTT Decomposition using Claude API')
    parser.add_argument('prompt', nargs='?', help='User prompt to analyze')
    parser.add_argument('--model', default='claude-sonnet-4-20250514',
                       choices=['claude-sonnet-4-20250514', 'claude-sonnet-3-5-20241022', 
                               'claude-3-5-sonnet-20240620', 'claude-sonnet-4.5'],
                       help='Claude model to use')
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Save decomposition to file')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress verbose output')
    parser.add_argument('--file', '-f', metavar='FILE',
                       help='Read prompt from file')
    parser.add_argument('--api-key', metavar='KEY',
                       help='Anthropic API key (or use ANTHROPIC_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Get prompt
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt
    else:
        print("📝 Enter your prompt (press Ctrl+D when done):")
        prompt = sys.stdin.read().strip()
    
    if not prompt:
        print("❌ No prompt provided")
        return 1
    
    # Initialize analyzer
    try:
        analyzer = ClaudeGUTTAnalyzer(model=args.model, api_key=args.api_key)
    except ValueError as e:
        print(f"❌ {e}")
        return 1
    
    # Decompose prompt
    decomposition = analyzer.decompose_prompt_to_gutts(prompt, verbose=not args.quiet)
    
    # Print summary
    analyzer.print_decomposition_summary(decomposition)
    
    # Save if requested
    if args.output:
        analyzer.save_decomposition(decomposition, args.output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
