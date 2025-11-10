#!/usr/bin/env python3
"""
Batch GPT-5 GUTT Analysis for All 9 Hero Prompts - Version 2

**Version 2 Changes**:
- Now loads full GUTT v4.0 ACRUE Integration Documentation (same as Claude/Ollama)
- Includes Hero Prompts Reference GUTT Decompositions for context
- Uses same prompt structure as Claude/Ollama analyzers for fair comparison
- Results marked as "v2_full_context" for distinction from v1 (minimal prompt)

**v1 Results** (minimal prompt, over-decomposition): Saved to hero_prompt_analysis/gpt5_v1_minimal_prompt/

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
    """Acquire access token using MSAL interactive auth - same method as meeting classifier."""
    print("🔐 Acquiring access token...")
    
    # Use same authentication as GPT5MeetingClassifier (which works!)
    app = msal.PublicClientApplication(
        APP_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        enable_broker_on_windows=True
    )
    
    # Try to get cached account first
    accounts = app.get_accounts()
    account = accounts[0] if accounts else None
    
    # Try silent token acquisition first
    if account:
        print(f"   Found cached account: {account.get('username', 'unknown')}")
        result = app.acquire_token_silent(SCOPES, account=account)
        if result and "access_token" in result:
            print("✅ Token acquired silently from cache")
            return result["access_token"]
    
    # Interactive authentication if silent fails (same as GPT5MeetingClassifier)
    print("   Launching interactive authentication...")
    result = app.acquire_token_interactive(
        SCOPES,
        parent_window_handle=msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE,
    )
    
    if result and "access_token" in result:
        print("✅ Token acquired successfully")
        return result["access_token"]
    
    error = result.get("error_description", result.get("error", "Unknown error"))
    print(f"❌ Authentication failed: {error}")
    raise Exception(f"Failed to acquire token: {error}")


def call_gpt5_api(token: str, system_message: str, user_prompt: str) -> dict:
    """Call GPT-5 API with system and user messages - matches working GPT5MeetingClassifier format."""
    import uuid
    
    # Build payload matching working classifier
    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ],
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "max_completion_tokens": 4000,
        "temperature": 0.3,
        "top_p": 0.95,
        "n": 1,
        "stream": False,
        "response_format": None,
    }
    
    # Generate scenario GUID for telemetry (matches working classifier)
    scenario_guid = str(uuid.uuid4())
    
    # Build headers matching working classifier
    headers = {
        "Authorization": f"Bearer {token}",
        "X-ModelType": MODEL,  # Critical: working classifier uses X-ModelType header
        "X-ScenarioGUID": scenario_guid,
        "Content-Type": "application/json"
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


def load_gutt_context() -> str:
    """Load GUTT framework context from documentation - same as Claude/Ollama analyzers"""
    from pathlib import Path
    
    context_parts = []
    
    # Try to load GUTT v4.0 documentation (same files as Claude/Ollama)
    gutt_docs = [
        "docs/gutt_analysis/GUTT_v4.0_ACRUE_Integration_Documentation.md",
        "docs/gutt_analysis/Hero_Prompts_Reference_GUTT_Decompositions.md"
    ]
    
    for doc_path in gutt_docs:
        if Path(doc_path).exists():
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Take first 1000 chars as context (same as Claude/Ollama)
                    context_parts.append(content[:1000])
                    print(f"   ✅ Loaded {len(content[:1000])} chars from {doc_path}")
            except Exception as e:
                print(f"   ⚠️  Could not load {doc_path}: {e}")
    
    if context_parts:
        return "\n\n**GUTT Framework Context**:\n" + "\n---\n".join(context_parts)
    else:
        # Fallback context if files not found
        return """**GUTT Framework Context**:
GUTT = Granular Unit Task Taxonomy
- Break down complex requests into atomic unit tasks
- Each unit task represents a single, specific capability
- Typical requests decompose into 3-9 unit tasks
- Each GUTT should be independently implementable and evaluable"""


def decompose_prompt(token: str, prompt: str, gutt_context: str) -> dict:
    """Decompose a hero prompt into GUTTs using GPT-5 with full GUTT documentation.
    
    Args:
        token: Authentication token for API
        prompt: User prompt to decompose
        gutt_context: Pre-loaded GUTT framework documentation (loaded once for entire batch)
    """
    
    system_message = f"""You are an expert AI system evaluator specializing in GUTT (Granular Unit Task Taxonomy) analysis using the GUTT v4.0 ACRUE framework.

{gutt_context}

Your task: Analyze the following user prompt and decompose it into constituent GUTT tasks (unit tasks).

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

Return ONLY a valid JSON object (no markdown, no code blocks) with this structure:
{{
  "gutts": [
    {{
      "id": "gutt_1",
      "name": "Task Name",
      "capability": "What this task does",
      "required_skills": ["skill1", "skill2"],
      "user_goal": "What user wants to achieve",
      "triggered": true,
      "evidence": "Specific implementation evidence or example"
    }}
  ]
}}"""

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
    print("🎯 GPT-5 GUTT BATCH ANALYSIS v2 - 9 Hero Prompts")
    print("=" * 80)
    print()
    
    # Load GUTT documentation ONCE for entire batch (optimize bandwidth/tokens)
    print("📚 Loading GUTT framework documentation (once for entire batch)...")
    gutt_context = load_gutt_context()
    context_length = len(gutt_context)
    print(f"✅ Loaded {context_length:,} characters of GUTT documentation")
    print(f"💡 Will reuse this context for all 9 prompts (saves ~{context_length * 8:,} tokens total)\n")
    
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
            # Run GUTT decomposition (pass pre-loaded context)
            gutts_data = decompose_prompt(token, prompt_text, gutt_context)
            gpt5_gutts = len(gutts_data.get("gutts", []))
            
            # Build result
            decomposition = {
                "source": "gpt-5-v2",
                "backend_llm": MODEL,
                "backend_llm_notes": "GPT-5 via Microsoft SilverFlow LLM API - v2 with full GUTT documentation context (same as Claude/Ollama)",
                "prompt_version": "v2_full_context",
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
