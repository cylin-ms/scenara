#!/usr/bin/env python3
"""
Batch GPT-5 GUTT Analysis for All 9 Hero Prompts

Runs GPT-5 GUTT decomposition on each of the 9 Calendar.AI hero prompts
using real Microsoft SilverFlow LLM API calls.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
import msal
import requests

# SilverFlow LLM API Configuration
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
APP_ID = "942b706f-826e-426b-98f7-59e1e376b37c"
SCOPES = ["https://substrate.office.com/llmapi/LLMAPI.dev"]
ENDPOINT = "https://fe-26.qas.bing.net/chat/completions"
MODEL = "dev-gpt-5-chat-jj"

# Hero prompts from Calendar.AI evaluation framework
HERO_PROMPTS = [
    {
        "id": "organizer-1",
        "name": "Calendar Prioritization",
        "prompt": "Keep my Calendar up to date by committing to only meetings that are part of my priorities.",
        "reference_gutts": 6
    },
    {
        "id": "organizer-2",
        "name": "Meeting Prep Tracking",
        "prompt": "Track all my important meetings and flag any that require focus time to prepare for them.",
        "reference_gutts": 7
    },
    {
        "id": "organizer-3",
        "name": "Time Reclamation Analysis",
        "prompt": "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities.",
        "reference_gutts": 8
    },
    {
        "id": "schedule-1",
        "name": "Recurring 1:1 Scheduling",
        "prompt": "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts.",
        "reference_gutts": 7
    },
    {
        "id": "schedule-2",
        "name": "Block Time & Reschedule",
        "prompt": "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}.",
        "reference_gutts": 8
    },
    {
        "id": "schedule-3",
        "name": "Multi-Person Meeting Scheduling",
        "prompt": "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room.",
        "reference_gutts": 9
    },
    {
        "id": "collaborate-1",
        "name": "Agenda Creation",
        "prompt": "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.",
        "reference_gutts": 6
    },
    {
        "id": "collaborate-2",
        "name": "Executive Briefing Prep",
        "prompt": "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses.",
        "reference_gutts": 7
    },
    {
        "id": "collaborate-3",
        "name": "Customer Meeting Prep",
        "prompt": "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company.",
        "reference_gutts": 8
    }
]


def acquire_token():
    """Acquire access token using MSAL interactive auth."""
    print("🔐 Acquiring access token...")
    
    # Use Windows broker for better authentication on Windows
    app = msal.PublicClientApplication(
        APP_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        enable_broker_on_windows=True  # Use Windows Account Manager
    )
    
    # Try silent acquisition first
    accounts = app.get_accounts()
    if accounts:
        print(f"   Found {len(accounts)} cached account(s)")
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            print("✅ Token acquired silently from cache")
            return result["access_token"]
    
    # Interactive acquisition with Windows broker
    print("   Launching interactive authentication...")
    try:
        result = app.acquire_token_interactive(
            scopes=SCOPES,
            parent_window_handle=None,  # Let MSAL handle it
            prompt="select_account"
        )
    except Exception as e:
        print(f"   ⚠️  Windows broker failed: {e}")
        print("   Trying device code flow...")
        
        # Fallback to device code flow
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise Exception(f"Failed to create device flow: {flow.get('error_description')}")
        
        print(f"\n{'=' * 80}")
        print(flow["message"])
        print(f"{'=' * 80}\n")
        
        result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        print("✅ Token acquired successfully")
        return result["access_token"]
    else:
        error = result.get("error_description", result.get("error", "Unknown error"))
        print(f"❌ Authentication failed: {error}")
        raise Exception(f"Failed to acquire token: {error}")


def call_gpt5_api(token: str, system_message: str, user_prompt: str) -> dict:
    """Call GPT-5 API with system and user messages."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4000
    }
    
    try:
        response = requests.post(
            ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ API call failed: {e}")
        raise


def parse_gpt5_response(response_json: dict) -> str:
    """Extract content from GPT-5 response."""
    try:
        content = response_json["choices"][0]["message"]["content"]
        return content.strip()
    except (KeyError, IndexError) as e:
        print(f"❌ Failed to parse response: {e}")
        return ""


def decompose_prompt(token: str, prompt: str) -> dict:
    """Decompose a hero prompt into GUTTs using GPT-5."""
    
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
      "evidence": "Specific implementation evidence or example"
    }
  ]
}"""

    user_prompt = f"""Decompose this Calendar.AI hero prompt into atomic GUTTs:

Prompt: "{prompt}"

Requirements:
- Maximum atomic granularity (each GUTT = ONE unit task)
- Each GUTT independently implementable
- Complete coverage of all capabilities required
- Logical sequencing where dependencies exist
- Clear, specific skill requirements

Provide the GUTT decomposition as JSON."""

    print(f"   📡 Calling GPT-5 API...")
    response = call_gpt5_api(token, system_message, user_prompt)
    content = parse_gpt5_response(response)
    
    # Clean markdown code blocks if present
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    try:
        data = json.loads(content)
        return data
    except json.JSONDecodeError as e:
        print(f"   ⚠️  Failed to parse JSON: {e}")
        print(f"   Response: {content[:200]}...")
        return {"gutts": []}


def run_batch_analysis():
    """Run GUTT analysis on all 9 hero prompts."""
    
    print("=" * 80)
    print("🎯 GPT-5 GUTT BATCH ANALYSIS - 9 Hero Prompts")
    print("=" * 80)
    print()
    
    # Acquire token once for all API calls
    try:
        token = acquire_token()
    except Exception as e:
        print(f"❌ Failed to acquire token: {e}")
        return
    
    output_dir = Path("hero_prompt_analysis")
    output_dir.mkdir(exist_ok=True)
    
    results = []
    successful = 0
    failed = 0
    
    for prompt_data in HERO_PROMPTS:
        prompt_id = prompt_data['id']
        prompt_name = prompt_data['name']
        prompt_text = prompt_data['prompt']
        reference_gutts = prompt_data['reference_gutts']
        
        print(f"\n{'=' * 80}")
        print(f"🎯 Analyzing: {prompt_name} ({prompt_id})")
        print(f"   Reference GUTTs: {reference_gutts}")
        print(f"{'=' * 80}")
        
        try:
            # Run GUTT decomposition
            gutts_data = decompose_prompt(token, prompt_text)
            gpt5_gutts = len(gutts_data.get("gutts", []))
            
            # Build result
            decomposition = {
                "source": "gpt-5",
                "backend_llm": MODEL,
                "backend_llm_notes": "GPT-5 via Microsoft SilverFlow LLM API - Real API calls",
                "timestamp": datetime.now().isoformat(),
                "original_prompt": prompt_text,
                "gutts": gutts_data.get("gutts", []),
                "track1_score": 1.0 if gpt5_gutts > 0 else 0.0,
                "track2_score": None,  # Manual evaluation needed
                "overall_score": None
            }
            
            # Save to file
            output_file = output_dir / f"gpt5_gutt_{prompt_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(decomposition, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Success: {gpt5_gutts} GUTTs identified (Reference: {reference_gutts})")
            print(f"   💾 Saved to: {output_file}")
            
            results.append({
                "prompt_id": prompt_id,
                "success": True,
                "gpt5_gutts": gpt5_gutts,
                "reference_gutts": reference_gutts,
                "output_file": str(output_file)
            })
            successful += 1
            
            # Rate limiting - wait between API calls
            time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append({
                "prompt_id": prompt_id,
                "success": False,
                "error": str(e)
            })
            failed += 1
    
    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL,
        "total_prompts": len(HERO_PROMPTS),
        "successful": successful,
        "failed": failed,
        "results": results
    }
    
    summary_file = output_dir / "gpt5_batch_analysis_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 80}")
    print("📊 BATCH ANALYSIS COMPLETE")
    print(f"{'=' * 80}")
    print(f"✅ Successful: {successful}/{len(HERO_PROMPTS)}")
    print(f"❌ Failed: {failed}/{len(HERO_PROMPTS)}")
    print(f"💾 Summary saved to: {summary_file}")
    print()


if __name__ == "__main__":
    run_batch_analysis()
