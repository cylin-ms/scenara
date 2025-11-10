#!/usr/bin/env python3
"""
Quick test to verify GPT-5 API authentication is working.
"""

import sys
import json
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier

def test_gpt5_authentication():
    """Test GPT-5 API authentication and simple call."""
    
    print("=" * 80)
    print("GPT-5 API Authentication Test")
    print("=" * 80)
    
    # Initialize classifier
    print("\n1. Initializing GPT5MeetingClassifier...")
    try:
        classifier = GPT5MeetingClassifier()
        print("✅ Classifier initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False
    
    # Test simple classification call
    print("\n2. Testing simple meeting classification...")
    test_meeting = {
        "subject": "Weekly Team Sync",
        "organizer": "test@microsoft.com",
        "attendees": ["alice@microsoft.com", "bob@microsoft.com"],
        "duration_minutes": 30,
        "has_teams_link": True
    }
    
    try:
        result = classifier.classify_meeting(test_meeting)
        
        # Check if we got a valid classification (dict with specific_type means success)
        if isinstance(result, dict) and result.get('specific_type'):
            print("✅ GPT-5 API call successful!")
            print(f"\n   Classified as: {result['specific_type']}")
            print(f"   Category: {result.get('primary_category', 'N/A')}")
            confidence = result.get('confidence', 0)
            print(f"   Confidence: {confidence:.2%}" if confidence else f"   Confidence: N/A")
            reasoning = result.get('reasoning', '')
            print(f"   Reasoning: {reasoning[:100]}..." if reasoning else "")
            return True
        
        # Handle ClassificationResult object
        success = result.success if hasattr(result, 'success') else False
        
        if success:
            specific_type = result.specific_type if hasattr(result, 'specific_type') else result.get('specific_type')
            category = result.primary_category if hasattr(result, 'primary_category') else result.get('primary_category')
            confidence = result.confidence if hasattr(result, 'confidence') else result.get('confidence', 0)
            reasoning = result.reasoning if hasattr(result, 'reasoning') else result.get('reasoning', '')
            
            print("✅ GPT-5 API call successful!")
            print(f"\n   Classified as: {specific_type}")
            print(f"   Category: {category}")
            print(f"   Confidence: {confidence:.2%}")
            print(f"   Reasoning: {reasoning[:100]}..." if reasoning else "")
            return True
        else:
            error = result.error if hasattr(result, 'error') else result.get('error', 'Unknown error')
            print(f"❌ Classification failed: {error}")
            if "rate limit" in (error or "").lower():
                print("\n⚠️  Rate limit hit - API is working but throttled")
                print("   Try again in a few seconds")
                return True  # Auth works, just rate limited
            return False
            
    except Exception as e:
        print(f"❌ Exception during classification: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gpt5_token_only():
    """Test just token acquisition without API call."""
    
    print("\n" + "=" * 80)
    print("GPT-5 Token Acquisition Test (No API Call)")
    print("=" * 80)
    
    print("\n1. Attempting to acquire token...")
    try:
        classifier = GPT5MeetingClassifier()
        token = classifier._acquire_token()
        
        if token:
            print("✅ Token acquired successfully!")
            print(f"   Token length: {len(token)} characters")
            print(f"   Token preview: {token[:50]}...")
            return True
        else:
            print("❌ Failed to acquire token (returned None)")
            return False
            
    except Exception as e:
        print(f"❌ Exception during token acquisition: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🔍 Testing GPT-5 API Setup\n")
    
    # First test just token acquisition
    token_ok = test_gpt5_token_only()
    
    if token_ok:
        print("\n✅ Token acquisition works!")
        print("\n" + "=" * 80)
        
        # Ask if user wants to test full API call
        print("\n⚠️  Full API test will make a real GPT-5 call (rate limited)")
        response = input("Continue with full API test? (y/N): ").strip().lower()
        
        if response == 'y':
            api_ok = test_gpt5_authentication()
            
            if api_ok:
                print("\n" + "=" * 80)
                print("✅ GPT-5 API is fully operational!")
                print("=" * 80)
            else:
                print("\n" + "=" * 80)
                print("❌ GPT-5 API test failed")
                print("=" * 80)
        else:
            print("\n⏭️  Skipped full API test")
    else:
        print("\n" + "=" * 80)
        print("❌ Token acquisition failed - cannot proceed to API test")
        print("=" * 80)
        print("\n💡 Common fixes:")
        print("   1. Ensure you're on Windows DevBox (MSAL broker required)")
        print("   2. Check internet connectivity")
        print("   3. Verify Microsoft account has access to SilverFlow LLM API")
        print("   4. Try: pip install --upgrade msal")
