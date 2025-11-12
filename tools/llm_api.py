#!/usr/bin/env python3
"""
LLM API utility for Scenara project
Supports multiple LLM providers for meeting analysis and evaluation
"""

import argparse
import os
import sys
import json
from typing import Optional, Dict, Any
import ollama
import openai
from anthropic import Anthropic

class LLMAPIClient:
    def __init__(self):
        self.configure_clients()
    
    def configure_clients(self):
        """Configure API clients for different providers"""
        # Ollama (local)
        self.ollama_client = ollama.Client()
        
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
        else:
            self.openai_client = None
        
        # Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic_client = Anthropic(api_key=anthropic_key)
        else:
            self.anthropic_client = None
    
    def query_llm(self, prompt: str, provider: str = "ollama", model: str = None, image_path: Optional[str] = None) -> str:
        """
        Query LLM with support for different providers
        
        Args:
            prompt: The prompt to send to the LLM
            provider: LLM provider ("ollama", "openai", "anthropic")
            model: Specific model to use (optional)
            image_path: Path to image for vision capabilities (optional)
        
        Returns:
            LLM response as string
        """
        try:
            if provider == "ollama":
                return self._query_ollama(prompt, model or "gpt-oss:20b", image_path)
            elif provider == "openai":
                return self._query_openai(prompt, model or "gpt-4o", image_path)
            elif provider == "anthropic":
                return self._query_anthropic(prompt, model or "claude-3-sonnet-20240229", image_path)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        
        except Exception as e:
            print(f"Error querying {provider}: {e}", file=sys.stderr)
            return f"Error: Failed to get response from {provider}: {str(e)}"
    
    def _query_ollama(self, prompt: str, model: str, image_path: Optional[str] = None) -> str:
        """Query Ollama local LLM"""
        try:
            # Check if model is available
            models_response = self.ollama_client.list()
            available_models = [m.model for m in models_response.models]
            
            if model not in available_models:
                # Try to pull the model
                print(f"Model {model} not found. Attempting to pull...", file=sys.stderr)
                self.ollama_client.pull(model)
            
            # Prepare message
            message = {"role": "user", "content": prompt}
            
            # Add image if provided
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    import base64
                    image_data = base64.b64encode(f.read()).decode()
                    message["images"] = [image_data]
            
            response = self.ollama_client.chat(
                model=model,
                messages=[message],
                options={"temperature": 0.3}
            )
            
            return response['message']['content']
        
        except Exception as e:
            raise Exception(f"Ollama query failed: {str(e)}")
    
    def _query_openai(self, prompt: str, model: str, image_path: Optional[str] = None) -> str:
        """Query OpenAI API"""
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
        
        try:
            messages = []
            
            if image_path and os.path.exists(image_path):
                # Vision-enabled query
                import base64
                with open(image_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode()
                
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                    ]
                })
            else:
                messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"OpenAI query failed: {str(e)}")
    
    def _query_anthropic(self, prompt: str, model: str, image_path: Optional[str] = None) -> str:
        """Query Anthropic API"""
        if not self.anthropic_client:
            raise Exception("Anthropic API key not configured")
        
        try:
            if image_path and os.path.exists(image_path):
                # Vision query (if supported)
                print("Warning: Image support for Anthropic not implemented", file=sys.stderr)
            
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=2048,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        
        except Exception as e:
            raise Exception(f"Anthropic query failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Query LLM for PromptCoT project")
    parser.add_argument("--prompt", required=True, help="Prompt to send to LLM")
    parser.add_argument("--provider", default="ollama", choices=["ollama", "openai", "anthropic"], 
                       help="LLM provider to use")
    parser.add_argument("--model", help="Specific model to use")
    parser.add_argument("--image", help="Path to image for vision queries")
    parser.add_argument("--json", action="store_true", help="Output response as JSON")
    
    args = parser.parse_args()
    
    # Initialize client
    client = LLMAPIClient()
    
    # Query LLM
    try:
        response = client.query_llm(
            prompt=args.prompt,
            provider=args.provider,
            model=args.model,
            image_path=args.image
        )
        
        if args.json:
            output = {
                "prompt": args.prompt,
                "provider": args.provider,
                "model": args.model,
                "response": response
            }
            print(json.dumps(output, indent=2))
        else:
            print(response)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()