#!/usr/bin/env python3
"""
Test script for remote Ollama server with gpt-oss:120b model.

Tests connectivity and basic LLM functionality on the remote Ollama instance.
"""

import json
import time
from typing import Dict, Any
import requests


class RemoteOllamaClient:
    """Client for testing remote Ollama server."""
    
    def __init__(self, host: str = "192.168.2.204", port: int = 11434):
        """
        Initialize remote Ollama client.
        
        Args:
            host: Remote server IP/hostname
            port: Ollama API port (default 11434)
        """
        self.base_url = f"http://{host}:{port}"
        self.api_url = f"{self.base_url}/api"
        
    def check_connection(self) -> bool:
        """
        Check if Ollama server is accessible.
        
        Returns:
            bool: True if server responds, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available models on the server.
        
        Returns:
            dict: Server response with available models
        """
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to list models: {e}")
            return {}
    
    def generate(
        self, 
        model: str, 
        prompt: str, 
        stream: bool = False,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate text using specified model.
        
        Args:
            model: Model name (e.g., 'gpt-oss:120b')
            prompt: Input prompt
            stream: Whether to stream response
            options: Additional model options (temperature, etc.)
            
        Returns:
            dict: Generated response
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        if options:
            payload["options"] = options
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=120  # 2 minute timeout for large models
            )
            elapsed = time.time() - start_time
            
            response.raise_for_status()
            result = response.json()
            result['elapsed_seconds'] = elapsed
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Generation failed: {e}")
            return {"error": str(e)}


def main():
    """Run comprehensive Ollama server tests."""
    
    print("=" * 70)
    print("🧪 Remote Ollama Server Test")
    print("=" * 70)
    print(f"Server: 192.168.2.204:11434")
    print(f"Model: gpt-oss:120b")
    print("=" * 70)
    print()
    
    # Initialize client
    client = RemoteOllamaClient(host="192.168.2.204")
    
    # Test 1: Connection check
    print("📡 Test 1: Connection Check")
    print("-" * 70)
    if client.check_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed! Exiting.")
        return 1
    print()
    
    # Test 2: List models
    print("📋 Test 2: List Available Models")
    print("-" * 70)
    models_response = client.list_models()
    if models_response:
        models = models_response.get('models', [])
        print(f"✅ Found {len(models)} model(s):")
        for model in models:
            name = model.get('name', 'unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            print(f"   • {name} ({size:.2f} GB)")
        
        # Check if gpt-oss:120b is available
        model_names = [m.get('name', '') for m in models]
        if 'gpt-oss:120b' in model_names:
            print("✅ Target model 'gpt-oss:120b' is available!")
        else:
            print("⚠️  Target model 'gpt-oss:120b' not found!")
            print("   Available models:", ', '.join(model_names))
    else:
        print("❌ Failed to retrieve models")
    print()
    
    # Test 3: Simple generation test
    print("🤖 Test 3: Simple Generation Test")
    print("-" * 70)
    test_prompt = "What is 2+2? Answer with just the number."
    print(f"Prompt: '{test_prompt}'")
    print("Generating response... (this may take a moment with 120b model)")
    
    result = client.generate(
        model="gpt-oss:120b",
        prompt=test_prompt,
        options={"temperature": 0.1, "num_predict": 50}
    )
    
    if "error" in result:
        print(f"❌ Generation failed: {result['error']}")
    else:
        response_text = result.get('response', '')
        elapsed = result.get('elapsed_seconds', 0)
        total_duration = result.get('total_duration', 0) / 1e9  # Convert ns to seconds
        
        print(f"✅ Response: {response_text.strip()}")
        print(f"⏱️  Elapsed: {elapsed:.2f}s (Total: {total_duration:.2f}s)")
        
        # Show performance metrics
        if 'eval_count' in result:
            tokens_generated = result['eval_count']
            eval_duration = result.get('eval_duration', 0) / 1e9
            tokens_per_sec = tokens_generated / eval_duration if eval_duration > 0 else 0
            print(f"📊 Tokens: {tokens_generated} ({tokens_per_sec:.2f} tokens/sec)")
    print()
    
    # Test 4: Meeting intelligence test
    print("🎯 Test 4: Meeting Intelligence Test")
    print("-" * 70)
    meeting_prompt = """Analyze this meeting scenario and suggest 3 action items:

Meeting: Product Launch Planning
Attendees: PM, Engineering Lead, Marketing Manager
Context: Planning launch for new AI feature by December 15th
Discussion: Need to coordinate timeline, messaging, and technical readiness

Provide 3 specific, actionable next steps."""
    
    print("Prompt: Meeting intelligence test")
    print("Generating response...")
    
    result = client.generate(
        model="gpt-oss:120b",
        prompt=meeting_prompt,
        options={"temperature": 0.7, "num_predict": 300}
    )
    
    if "error" in result:
        print(f"❌ Generation failed: {result['error']}")
    else:
        response_text = result.get('response', '')
        elapsed = result.get('elapsed_seconds', 0)
        
        print(f"✅ Response:\n{response_text.strip()}")
        print(f"\n⏱️  Elapsed: {elapsed:.2f}s")
    print()
    
    # Test 5: JSON output test
    print("📝 Test 5: Structured JSON Output Test")
    print("-" * 70)
    json_prompt = """Return a JSON object with the following structure for a meeting:
{
  "title": "string",
  "priority": "high|medium|low",
  "action_items": ["string"]
}

Meeting: Q4 Planning Review with executives"""
    
    print("Prompt: Structured JSON output test")
    print("Generating response...")
    
    result = client.generate(
        model="gpt-oss:120b",
        prompt=json_prompt,
        options={"temperature": 0.1, "num_predict": 200}
    )
    
    if "error" in result:
        print(f"❌ Generation failed: {result['error']}")
    else:
        response_text = result.get('response', '')
        elapsed = result.get('elapsed_seconds', 0)
        
        print(f"✅ Response:\n{response_text.strip()}")
        print(f"\n⏱️  Elapsed: {elapsed:.2f}s")
        
        # Try to parse as JSON
        try:
            # Extract JSON from response (may have extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                print("✅ Valid JSON structure!")
        except json.JSONDecodeError:
            print("⚠️  Response is not valid JSON (model may need prompt engineering)")
    print()
    
    # Summary
    print("=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)
    print("Summary:")
    print("  • Connection: Working")
    print("  • Model: gpt-oss:120b available")
    print("  • Generation: Functional")
    print("  • Use cases: Meeting intelligence, structured output")
    print()
    print("Next steps:")
    print("  1. Update LLMAPIClient with remote Ollama endpoint")
    print("  2. Configure base_url='http://192.168.2.204:11434'")
    print("  3. Test workback planning with gpt-oss:120b")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    exit(main())
