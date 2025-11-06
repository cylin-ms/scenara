#!/usr/bin/env python3
"""
GUTT Decomposition using Local Ollama LLM

Uses locally hosted Ollama to analyze prompts and decompose them into GUTT tasks
following the GUTT v4.0 ACRUE evaluation framework.
"""

import json
import sys
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class OllamaGUTTAnalyzer:
    """Analyze prompts using Ollama LLM to identify GUTT tasks"""
    
    def __init__(self, model: str = "gpt-oss:20b", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama analyzer
        
        Args:
            model: Ollama model name
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            return False
    
    def query_ollama(self, prompt: str, stream: bool = False) -> str:
        """
        Query Ollama with a prompt
        
        Args:
            prompt: The prompt to send
            stream: Whether to stream response
            
        Returns:
            LLM response text
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=300)
            response.raise_for_status()
            
            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            full_response += chunk['response']
                            print(chunk['response'], end='', flush=True)
                print()  # New line after streaming
                return full_response
            else:
                # Handle non-streaming response
                result = response.json()
                return result.get('response', '')
        
        except Exception as e:
            print(f"❌ Error querying Ollama: {e}")
            return ""
    
    def decompose_prompt_to_gutts(self, user_prompt: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Decompose user prompt into GUTT tasks using Ollama
        
        Args:
            user_prompt: The original user prompt to analyze
            verbose: Whether to show streaming output
            
        Returns:
            Dictionary with GUTT decomposition
        """
        
        analysis_prompt = f"""You are an expert AI system evaluator specializing in GUTT (Granular Unit Task Taxonomy) analysis using the GUTT v4.0 ACRUE framework.

Your task: Analyze the following user prompt and decompose it into constituent GUTT tasks (unit tasks).

**User Prompt**: "{user_prompt}"

**Instructions**:
1. Identify all distinct capabilities required to fulfill this user request
2. For each capability, define it as a separate GUTT task
3. For each GUTT, provide:
   - Unique ID (gutt_1, gutt_2, etc.)
   - Name (concise descriptive name)
   - Capability description (what this GUTT does)
   - Required skills (list of specific skills needed)
   - User goal (what user wants to achieve with this GUTT)
   - Whether it was triggered/executed (based on the prompt)
   - Evidence of execution (if applicable)

**Output Format**: Respond ONLY with valid JSON in this exact structure:
{{
  "analysis": {{
    "original_prompt": "{user_prompt}",
    "total_gutts_identified": <number>,
    "gutts": [
      {{
        "id": "gutt_1",
        "name": "<GUTT name>",
        "capability": "<What this GUTT does>",
        "required_skills": ["skill1", "skill2"],
        "user_goal": "<What user wants to achieve>",
        "triggered": true/false,
        "evidence": "<Evidence of execution or null>"
      }}
    ]
  }}
}}

**Important**: 
- Focus on DISTINCT capabilities, not implementation details
- Each GUTT should represent a single, clear unit task
- Be specific about required skills
- Use clear, professional language
- Output ONLY valid JSON, no markdown formatting, no explanations outside JSON

Analyze the prompt now:"""

        if verbose:
            print("\n🤖 Querying Ollama for GUTT decomposition...")
            print(f"   Model: {self.model}")
            print(f"   Prompt: {user_prompt[:100]}...")
            print("\n" + "=" * 80)
            print("Ollama Response:")
            print("=" * 80 + "\n")
        
        # Query Ollama
        response = self.query_ollama(analysis_prompt, stream=verbose)
        
        if verbose:
            print("\n" + "=" * 80)
        
        # Parse JSON response
        try:
            # Try to find JSON in response (in case there's extra text)
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                print("⚠️  No JSON found in response")
                return self._create_error_response(user_prompt, "No JSON in response")
            
            json_str = response[start_idx:end_idx]
            result = json.loads(json_str)
            
            # Validate structure
            if 'analysis' not in result:
                print("⚠️  Invalid JSON structure (missing 'analysis' key)")
                return self._create_error_response(user_prompt, "Invalid structure")
            
            return result['analysis']
        
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"   Response: {response[:500]}...")
            return self._create_error_response(user_prompt, str(e))
    
    def _create_error_response(self, prompt: str, error: str) -> Dict[str, Any]:
        """Create error response structure"""
        return {
            "original_prompt": prompt,
            "total_gutts_identified": 0,
            "gutts": [],
            "error": error
        }
    
    def save_decomposition(self, decomposition: Dict[str, Any], output_file: str):
        """
        Save GUTT decomposition to file in evaluator format
        
        Args:
            decomposition: Decomposition result from decompose_prompt_to_gutts
            output_file: Output file path
        """
        # Transform to evaluator format
        evaluator_format = {
            "source": f"ollama_{self.model}",
            "backend_llm": self.model,
            "backend_llm_notes": "Locally hosted Ollama model - gpt-oss:20b (13 GB, based on GPT architecture)",
            "timestamp": datetime.now().isoformat(),
            "original_prompt": decomposition.get("original_prompt", ""),
            "gutts": decomposition.get("gutts", []),
            "track1_score": None,  # To be filled by evaluator
            "track2_score": None,
            "overall_score": None,
            "notes": f"Generated by Ollama {self.model} - Locally hosted LLM on macOS"
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(evaluator_format, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Decomposition saved to: {output_file}")
    
    def print_decomposition_summary(self, decomposition: Dict[str, Any]):
        """Print formatted summary of decomposition"""
        print("\n" + "=" * 80)
        print("📋 GUTT DECOMPOSITION SUMMARY")
        print("=" * 80)
        print(f"\n🤖 Backend LLM: {self.model} (Ollama - Locally Hosted)")
        
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
    
    parser = argparse.ArgumentParser(description='GUTT Decomposition using Ollama')
    parser.add_argument('prompt', nargs='?', help='User prompt to analyze')
    parser.add_argument('--model', default='gpt-oss:20b',
                       help='Ollama model name (default: gpt-oss:20b)')
    parser.add_argument('--url', default='http://localhost:11434',
                       help='Ollama server URL (default: http://localhost:11434)')
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Save decomposition to file')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress streaming output')
    parser.add_argument('--file', '-f', metavar='FILE',
                       help='Read prompt from file')
    
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
    analyzer = OllamaGUTTAnalyzer(model=args.model, base_url=args.url)
    
    # Check connection
    print(f"🔍 Checking Ollama connection at {args.url}...")
    if not analyzer.check_ollama_connection():
        print("❌ Ollama is not running or not accessible")
        print(f"   Make sure Ollama is running: ollama serve")
        print(f"   And model is available: ollama pull {args.model}")
        return 1
    
    print(f"✅ Connected to Ollama")
    
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
