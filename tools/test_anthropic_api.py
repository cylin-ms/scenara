#!/usr/bin/env python3
"""
Test Anthropic API Configuration

Quick test to verify Anthropic API key is set and working.
"""

import os
import sys

def test_api_configuration():
    """Test if Anthropic API is properly configured"""
    
    print("=" * 80)
    print("ANTHROPIC API CONFIGURATION TEST")
    print("=" * 80)
    
    # Check 1: API key environment variable
    print("\n✓ Checking ANTHROPIC_API_KEY environment variable...")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("  ❌ ANTHROPIC_API_KEY not set")
        print("\n  Please set your API key:")
        print("    Windows (PowerShell): $env:ANTHROPIC_API_KEY='your-key-here'")
        print("    Linux/Mac: export ANTHROPIC_API_KEY='your-key-here'")
        print("\n  Get your API key from: https://console.anthropic.com/")
        return False
    
    print(f"  ✅ ANTHROPIC_API_KEY is set (length: {len(api_key)} chars)")
    
    # Check 2: anthropic package
    print("\n✓ Checking anthropic package installation...")
    try:
        import anthropic
        print(f"  ✅ anthropic package installed (version: {anthropic.__version__})")
    except ImportError:
        print("  ❌ anthropic package not installed")
        print("\n  Install with: pip install anthropic")
        return False
    
    # Check 3: API connectivity test
    print("\n✓ Testing API connectivity with simple query...")
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Simple test query
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Reply with only the word 'SUCCESS' if you can read this."}
            ]
        )
        
        response_text = message.content[0].text
        
        if "SUCCESS" in response_text.upper():
            print("  ✅ API connection successful!")
            print(f"  Model: {message.model}")
            print(f"  Response: {response_text.strip()}")
        else:
            print(f"  ⚠️  Unexpected response: {response_text}")
            return False
        
    except anthropic.AuthenticationError:
        print("  ❌ Authentication failed - invalid API key")
        print("\n  Please check your API key at: https://console.anthropic.com/")
        return False
    except anthropic.RateLimitError:
        print("  ⚠️  Rate limit reached - but API key is valid!")
        print("  Wait a moment and try again.")
        return True  # Key is valid, just rate limited
    except Exception as e:
        print(f"  ❌ API error: {e}")
        return False
    
    # All checks passed
    print("\n" + "=" * 80)
    print("✅ ALL CHECKS PASSED - Ready to run Claude batch analysis!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Run batch analysis:")
    print("     python tools/run_claude_batch_composition.py")
    print("\n  2. Compare with gold standard:")
    print("     python tools/compare_to_gold.py <output_file>")
    print("\n" + "=" * 80)
    
    return True


def main():
    """Main entry point"""
    success = test_api_configuration()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
