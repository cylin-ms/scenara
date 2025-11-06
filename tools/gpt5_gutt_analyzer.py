#!/usr/bin/env python3
"""
GPT-5 GUTT Analyzer using SilverFlow LLM API

Analyzes hero prompts to decompose them into Granular Unit Task Taxonomy (GUTT)
using Microsoft's GPT-5 model (dev-gpt-5-chat-jj).
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import GPT-5 Meeting Classifier infrastructure
try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, ChatMessage, DEFAULT_ENDPOINT, DEFAULT_MODEL
except ImportError:
    try:
        from meeting_classifier_gpt5 import GPT5MeetingClassifier, ChatMessage, DEFAULT_ENDPOINT, DEFAULT_MODEL
    except ImportError:
        print("ERROR: Could not import GPT5MeetingClassifier")
        print("Make sure tools/meeting_classifier_gpt5.py is available")
        sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed")
    print("Install with: pip install requests")
    sys.exit(1)

try:
    import msal
except ImportError:
    print("ERROR: msal library not installed")
    print("Install with: pip install msal")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GPT5GUTTAnalyzer:
    """
    GUTT Decomposition Analyzer using GPT-5 (dev-gpt-5-chat-jj).
    
    Uses Microsoft's SilverFlow LLM API to analyze prompts and decompose them
    into atomic Granular Unit Task Taxonomy (GUTT) components.
    """
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        endpoint: str = DEFAULT_ENDPOINT,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """
        Initialize GPT-5 GUTT Analyzer.
        
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
        
        # Initialize GPT-5 classifier for token acquisition
        self.gpt5_client = GPT5MeetingClassifier(
            model=model,
            endpoint=endpoint,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info(f"Initialized GPT-5 GUTT Analyzer with model: {model}")
    
    def decompose_prompt_to_gutts(self, prompt: str) -> Dict[str, Any]:
        """
        Decompose a hero prompt into atomic GUTTs using GPT-5.
        
        Args:
            prompt: The hero prompt to analyze
            
        Returns:
            Dictionary with decomposition results including:
            - source: "gpt-5"
            - backend_llm: Model identifier
            - timestamp: ISO timestamp
            - original_prompt: Input prompt
            - gutts: List of GUTT objects
        """
        logger.info(f"Analyzing prompt with GPT-5: {prompt[:100]}...")
        
        # Construct GUTT analysis system message
        system_message = """You are an expert at decomposing complex prompts into atomic Granular Unit Task Taxonomy (GUTT) components.

GUTT Framework (v4.0 ACRUE):
- Each GUTT represents ONE atomic, indivisible unit task
- GUTTs must be granular enough that each can be independently implemented
- Each GUTT has: unique ID, name, capability description, required skills, user goal, triggered status, evidence

Your task:
1. Analyze the prompt and identify ALL atomic unit tasks required
2. Decompose to the finest granularity - each GUTT should be ONE specific action/capability
3. Do NOT group related tasks - keep them as separate GUTTs
4. Ensure GUTTs are sequenced logically if they have dependencies

Return ONLY a valid JSON object (no markdown, no code blocks) with this structure:
{
  "gutts": [
    {
      "id": "gutt_1",
      "name": "Task Name",
      "capability": "What this task does",
      "required_skills": ["skill1", "skill2"],
      "user_goal": "What user wants to achieve",
      "triggered": true,
      "evidence": "Specific implementation evidence"
    }
  ]
}"""

        # Construct user prompt
        user_prompt = f"""Decompose this Calendar.AI hero prompt into atomic GUTTs:

Prompt: "{prompt}"

Requirements:
- Maximum atomic granularity (each GUTT = ONE unit task)
- Each GUTT independently implementable
- Complete coverage of all capabilities required
- Logical sequencing where dependencies exist
- Clear, specific skill requirements

Provide the GUTT decomposition as JSON."""

        # Call GPT-5 API
        try:
            result = self.gpt5_client._call_gpt5_api(
                system_message=system_message,
                user_prompt=user_prompt,
                timeout=60
            )
            
            if not result.success:
                logger.error(f"GPT-5 API call failed: {result.error}")
                return {
                    "source": "gpt-5",
                    "backend_llm": self.model,
                    "timestamp": datetime.now().isoformat(),
                    "original_prompt": prompt,
                    "error": result.error,
                    "gutts": []
                }
            
            # Parse JSON response
            response_content = result.response_content or ""
            gutts_data = self._parse_gpt5_response(response_content)
            
            # Build result
            decomposition = {
                "source": "gpt-5",
                "backend_llm": self.model,
                "backend_llm_notes": "GPT-5 via Microsoft SilverFlow LLM API - Enterprise-grade reasoning",
                "timestamp": datetime.now().isoformat(),
                "original_prompt": prompt,
                "gutts": gutts_data.get("gutts", []),
            }
            
            logger.info(f"Successfully decomposed into {len(decomposition['gutts'])} GUTTs")
            return decomposition
            
        except Exception as e:
            logger.error(f"Error during GUTT decomposition: {e}")
            return {
                "source": "gpt-5",
                "backend_llm": self.model,
                "timestamp": datetime.now().isoformat(),
                "original_prompt": prompt,
                "error": str(e),
                "gutts": []
            }
    
    def _parse_gpt5_response(self, response_content: str) -> Dict[str, Any]:
        """
        Parse GPT-5 response to extract GUTT decomposition.
        
        Args:
            response_content: Raw response from GPT-5
            
        Returns:
            Dictionary with 'gutts' key containing list of GUTT objects
        """
        # Clean response - remove markdown code blocks if present
        content = response_content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            data = json.loads(content)
            
            # Validate structure
            if "gutts" not in data:
                logger.warning("Response missing 'gutts' key")
                return {"gutts": []}
            
            # Validate each GUTT has required fields
            required_fields = ["id", "name", "capability", "required_skills", "user_goal", "triggered"]
            valid_gutts = []
            
            for gutt in data["gutts"]:
                if all(field in gutt for field in required_fields):
                    valid_gutts.append(gutt)
                else:
                    logger.warning(f"GUTT missing required fields: {gutt.get('name', 'Unknown')}")
            
            logger.info(f"Parsed {len(valid_gutts)} valid GUTTs from response")
            return {"gutts": valid_gutts}
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {content[:500]}")
            return {"gutts": []}
    
    def save_decomposition(self, decomposition: Dict[str, Any], output_file: str):
        """
        Save GUTT decomposition to JSON file.
        
        Args:
            decomposition: GUTT decomposition result
            output_file: Output file path
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(decomposition, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved decomposition to {output_path}")
    
    def test_model_availability(self) -> bool:
        """
        Test if GPT-5 model is available and accessible.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            test_prompt = "List the primary colors."
            result = self.gpt5_client._call_gpt5_api(
                system_message="You are a helpful assistant.",
                user_prompt=test_prompt,
                timeout=10
            )
            return result.success
        except Exception as e:
            logger.error(f"Model availability test failed: {e}")
            return False


def main():
    """Main entry point for GPT-5 GUTT analyzer"""
    parser = argparse.ArgumentParser(
        description="Analyze hero prompts using GPT-5 for GUTT decomposition"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Hero prompt to analyze"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"GPT-5 model to use (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (default: gpt5_gutt_decomposition.json)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test GPT-5 model availability"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize analyzer
    analyzer = GPT5GUTTAnalyzer(model=args.model)
    
    # Test model availability if requested
    if args.test:
        print(f"\n🧪 Testing GPT-5 Model Availability...")
        print(f"Model: {args.model}")
        print(f"Endpoint: {DEFAULT_ENDPOINT}")
        
        available = analyzer.test_model_availability()
        
        if available:
            print("✅ GPT-5 model is available and accessible")
            return 0
        else:
            print("❌ GPT-5 model is not available")
            return 1
    
    # Analyze prompt
    print(f"\n🔍 Analyzing prompt with GPT-5...")
    print(f"Model: {args.model}")
    print(f"Prompt: {args.prompt}\n")
    
    decomposition = analyzer.decompose_prompt_to_gutts(args.prompt)
    
    # Display results
    gutt_count = len(decomposition.get("gutts", []))
    print(f"\n📊 Results:")
    print(f"GUTTs identified: {gutt_count}")
    
    if decomposition.get("error"):
        print(f"❌ Error: {decomposition['error']}")
    else:
        print(f"\nGUTT Decomposition:")
        for i, gutt in enumerate(decomposition.get("gutts", []), 1):
            print(f"\n{i}. {gutt['name']}")
            print(f"   Capability: {gutt['capability']}")
            print(f"   Skills: {', '.join(gutt['required_skills'][:3])}{'...' if len(gutt['required_skills']) > 3 else ''}")
    
    # Save to file
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"gpt5_gutt_decomposition_{timestamp}.json"
    
    analyzer.save_decomposition(decomposition, output_file)
    print(f"\n💾 Saved to: {output_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
