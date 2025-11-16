#!/usr/bin/env python3
"""
Test Workback Planning Generator with Ollama

This script tests the workback planning generator using Ollama local models.
Useful for testing without OpenAI API keys.
"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.workback_planning import generate_plan


def test_ollama_generation():
    """Test workback plan generation with Ollama"""
    
    context = """
Meeting: Sprint Planning
Target Date: 2025-11-20
Duration: 60 minutes

Participants:
- Alice (alice@team.com) - Scrum Master
- Bob (bob@team.com) - Developer

Objectives:
1. Plan 2-week sprint
2. Define 5 user stories
3. Assign tasks to team members

Key Constraints:
- 2 developers available
- 80 hours capacity per developer
- Must complete by sprint end
"""
    
    print("=" * 80)
    print("WORKBACK PLAN GENERATOR TEST (OLLAMA)")
    print("=" * 80)
    print("\nContext:")
    print(context)
    print("\n" + "=" * 80)
    
    try:
        # Use Ollama for both stages
        ollama_config = {
            "provider": "ollama",
            "model": "gpt-oss:20b",
            "temperature": 0.1
        }
        
        print("\n🚀 Generating workback plan with Ollama (gpt-oss:20b)...")
        print("   Note: This uses Ollama instead of O1, so reasoning may be less sophisticated")
        
        result = generate_plan(
            context,
            analysis_model_override=ollama_config,
            structure_model_override=ollama_config
        )
        
        # Validate analysis
        print("\n" + "=" * 80)
        print("STAGE 1: ANALYSIS (Ollama)")
        print("=" * 80)
        if result['analysis']:
            print(result['analysis'][:500] + "..." if len(result['analysis']) > 500 else result['analysis'])
            print(f"\n✅ Analysis generated successfully ({len(result['analysis'])} chars)")
        else:
            print("❌ Analysis generation failed")
            return False
        
        # Validate structured output
        print("\n" + "=" * 80)
        print("STAGE 2: STRUCTURED JSON (Ollama)")
        print("=" * 80)
        if result['structured']:
            print(json.dumps(result['structured'], indent=2)[:500] + "..." if len(json.dumps(result['structured'])) > 500 else json.dumps(result['structured'], indent=2))
            print(f"\n✅ Structured plan generated successfully")
        else:
            print("❌ Structured generation failed")
            return False
        
        print("\n" + "=" * 80)
        print("✅ TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 Starting Workback Planning Generator Test (Ollama)\n")
    print("⚠️  Make sure Ollama is running: ollama serve")
    print("⚠️  Make sure gpt-oss:20b is installed: ollama pull gpt-oss:20b\n")
    
    success = test_ollama_generation()
    
    if success:
        print("\n✅ Test passed!")
        sys.exit(0)
    else:
        print("\n❌ Test failed")
        sys.exit(1)
