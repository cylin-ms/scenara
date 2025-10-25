#!/usr/bin/env python3
import asyncio
from real_me_notes_integration import RealMeNotesAPI, load_config

async def test_integration():
    print("🧪 Testing Real Me Notes Integration")
    print("=" * 40)
    
    # Load config
    config = load_config()
    
    # Test API
    api = RealMeNotesAPI(
        user_email="cyl@microsoft.com",
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret"),
        tenant_id=config.get("tenant_id")
    )
    
    # Fetch notes
    notes = await api.fetch_real_me_notes()
    
    print(f"✅ Successfully retrieved {len(notes)} Me Notes")
    
    if notes:
        print("\n📋 Sample Note:")
        note = notes[0]
        print(f"   Category: {note.category.value}")
        print(f"   Note: {note.note}")
        print(f"   Source: {note.source}")

if __name__ == "__main__":
    asyncio.run(test_integration())
