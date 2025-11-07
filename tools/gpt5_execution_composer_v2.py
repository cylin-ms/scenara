#!/usr/bin/env python3
"""
GPT-5 Execution Composition Analyzer V2.0

Given the 25 canonical unit tasks (including new CAN-25: Event Annotation/Flagging),
analyze hero prompts and compose execution plans by selecting and sequencing 
the appropriate canonical tasks.

This is COMPOSITION analysis, not task discovery.

Version: 2.0 (Updated November 7, 2025)
Changes: Added CAN-25, renumbered tasks 1-25, optimized prompt instructions
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
import sys
from pathlib import Path
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

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


# 25 Canonical Unit Tasks (Framework V2.0 - Renumbered 1-25)
CANONICAL_TASKS_V2 = [
    {
        "id": "CAN-01",
        "name": "Calendar Events Retrieval",
        "description": "Retrieve calendar events from user's calendar within specified timeframe",
        "tier": 1,
        "frequency": "100%",
        "keywords": ["calendar", "events", "meetings", "retrieve", "get"]
    },
    {
        "id": "CAN-02",
        "name": "Meeting Type Classification",
        "description": "Classify meetings by format/structure (1:1, team sync, customer, etc.) - OBJECTIVE, format-based",
        "tier": 1,
        "frequency": "78%",
        "keywords": ["type", "format", "1:1", "team", "customer", "classify"]
    },
    {
        "id": "CAN-03",
        "name": "Meeting Importance Assessment",
        "description": "Assess strategic importance, urgency, priority level - SUBJECTIVE, value-based",
        "tier": 1,
        "frequency": "78%",
        "keywords": ["important", "priority", "urgent", "critical", "strategic"]
    },
    {
        "id": "CAN-04",
        "name": "Natural Language Understanding (NLU)",
        "description": "Extract structured constraints, intents, entities from natural language input",
        "tier": 1,
        "frequency": "100%",
        "keywords": ["parse", "understand", "extract", "intent", "constraints"]
    },
    {
        "id": "CAN-05",
        "name": "Attendee/Contact Resolution",
        "description": "Resolve attendee names to directory entries, expand teams, handle disambiguation",
        "tier": 1,
        "frequency": "67%",
        "keywords": ["attendees", "contacts", "resolve", "people", "participants"]
    },
    {
        "id": "CAN-06",
        "name": "Availability Checking (Free/Busy)",
        "description": "Check free/busy status across multiple calendars, find common available slots",
        "tier": 2,
        "frequency": "44%",
        "keywords": ["availability", "free", "busy", "slots", "schedule"]
    },
    {
        "id": "CAN-07",
        "name": "Meeting Metadata Extraction",
        "description": "Extract RSVP status, attendees, attachments, notes, logistics from meetings (PARENT TASK)",
        "tier": 2,
        "frequency": "78%",
        "keywords": ["RSVP", "invitations", "pending", "metadata", "details", "documents", "attachments"]
    },
    {
        "id": "CAN-08",
        "name": "Document/Content Retrieval",
        "description": "Retrieve attachments, pre-reads, shared documents from meetings",
        "tier": 2,
        "frequency": "44%",
        "keywords": ["documents", "attachments", "files", "content", "pre-read"]
    },
    {
        "id": "CAN-09",
        "name": "Document Generation/Formatting",
        "description": "Generate agendas, summaries, briefings using templates and LLMs",
        "tier": 2,
        "frequency": "56%",
        "keywords": ["generate", "create", "agenda", "summary", "brief", "dossier"]
    },
    {
        "id": "CAN-10",
        "name": "Time Aggregation/Statistical Analysis",
        "description": "Aggregate time spent in meetings, compute statistics, identify patterns",
        "tier": 2,
        "frequency": "22%",
        "keywords": ["time", "statistics", "aggregate", "analyze", "breakdown", "patterns"]
    },
    {
        "id": "CAN-11",
        "name": "Priority/Preference Matching",
        "description": "Match meetings against user's stated priorities and preferences",
        "tier": 2,
        "frequency": "56%",
        "keywords": ["prioritize", "match", "preferences", "align", "priorities"]
    },
    {
        "id": "CAN-12",
        "name": "Constraint Satisfaction",
        "description": "Solve scheduling constraints using CSP/optimization algorithms",
        "tier": 2,
        "frequency": "44%",
        "keywords": ["constraints", "satisfy", "optimize", "schedule", "find time"]
    },
    {
        "id": "CAN-13",
        "name": "RSVP Status Update",
        "description": "Update RSVP status, send meeting notifications to attendees (WRITE operation)",
        "tier": 2,
        "frequency": "33%",
        "keywords": ["accept", "decline", "respond", "RSVP", "notify"]
    },
    {
        "id": "CAN-14",
        "name": "Recommendation Engine",
        "description": "Generate personalized recommendations based on calendar data and user behavior",
        "tier": 2,
        "frequency": "33%",
        "keywords": ["recommend", "suggest", "should", "could", "consider"]
    },
    {
        "id": "CAN-15",
        "name": "Recurrence Rule Generation",
        "description": "Generate RRULE patterns for recurring meetings (daily, weekly, monthly, etc.)",
        "tier": 3,
        "frequency": "22%",
        "keywords": ["recurring", "weekly", "daily", "repeat", "every"]
    },
    {
        "id": "CAN-16",
        "name": "Event Monitoring/Change Detection",
        "description": "Monitor calendar events for changes, trigger webhooks, detect conflicts",
        "tier": 3,
        "frequency": "22%",
        "keywords": ["monitor", "track", "watch", "detect", "changes"]
    },
    {
        "id": "CAN-17",
        "name": "Automatic Rescheduling",
        "description": "Automatically reschedule meetings when conflicts or changes occur",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["auto-reschedule", "automatically", "reschedule", "move"]
    },
    {
        "id": "CAN-18",
        "name": "Objection/Risk Anticipation",
        "description": "Analyze previous meetings to anticipate objections, risks, blockers",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["anticipate", "risks", "objections", "blockers", "concerns", "pushback"]
    },
    {
        "id": "CAN-19",
        "name": "Resource Booking (Rooms/Equipment)",
        "description": "Book meeting rooms, equipment, catering, other logistics",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["room", "book", "equipment", "resources", "logistics"]
    },
    {
        "id": "CAN-20",
        "name": "Data Visualization/Reporting",
        "description": "Generate charts, graphs, dashboards showing calendar analytics",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["visualize", "show", "chart", "graph", "dashboard", "display"]
    },
    {
        "id": "CAN-21",
        "name": "Focus Time/Preparation Time Analysis",
        "description": "Estimate meeting prep time based on complexity, attachments, agenda",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["prep", "prepare", "focus time", "preparation", "ready"]
    },
    {
        "id": "CAN-22",
        "name": "Research/Intelligence Gathering",
        "description": "Discover who works on what based on collaboration patterns, documents, meetings",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["research", "discover", "find", "intelligence", "background"]
    },
    {
        "id": "CAN-23",
        "name": "Agenda Generation/Structuring",
        "description": "Generate structured meeting agendas with topics, time allocations, goals",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["agenda", "structure", "topics", "outline"]
    },
    {
        "id": "CAN-24",
        "name": "Multi-party Coordination/Negotiation",
        "description": "Coordinate and negotiate time slots across multiple parties with complex constraints",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["coordinate", "multi-party", "negotiate", "work around"]
    },
    {
        "id": "CAN-25",
        "name": "Event Annotation/Flagging",
        "description": "Add annotations, flags, or visual indicators to calendar events when predefined conditions are met (e.g., prep time needed, VIP attendee, budget approval)",
        "tier": 3,
        "frequency": "11%",
        "keywords": ["flag", "annotate", "mark", "highlight", "signal", "indicator"]
    }
]


class GPT5ExecutionComposerV2:
    """
    Execution Composition Analyzer V2.0 using GPT-5.
    
    Given 25 canonical unit tasks (including new CAN-25 for event annotation/flagging),
    compose execution plans by selecting and sequencing the appropriate tasks for each hero prompt.
    """
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        endpoint: str = DEFAULT_ENDPOINT,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """Initialize GPT-5 Execution Composer V2"""
        self.model = model
        self.endpoint = endpoint
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize GPT-5 client
        self.gpt5_client = GPT5MeetingClassifier(
            model=model,
            endpoint=endpoint,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        logger.info(f"Initialized GPT-5 Execution Composer V2.0 with model: {model}")
    
    def _format_canonical_tasks(self) -> str:
        """Format canonical tasks for system prompt"""
        formatted = []
        for task in CANONICAL_TASKS_V2:
            keywords_str = ", ".join(task['keywords'][:5])  # First 5 keywords
            formatted.append(
                f"{task['id']}: {task['name']}\n"
                f"   Description: {task['description']}\n"
                f"   Tier: {task['tier']} | Frequency: {task['frequency']} | Keywords: {keywords_str}"
            )
        return "\n\n".join(formatted)
    
    def compose_execution_plan(self, prompt: str, prompt_id: str = None) -> Dict[str, Any]:
        """
        Compose an execution plan by selecting from 25 canonical tasks.
        
        Args:
            prompt: The hero prompt to analyze
            prompt_id: Optional prompt identifier (e.g., "organizer-1")
            
        Returns:
            Dictionary with execution composition including:
            - source: "gpt-5"
            - model: Model identifier
            - framework_version: "2.0"
            - timestamp: ISO timestamp
            - prompt_id: Prompt identifier
            - prompt_text: Input prompt
            - execution_plan: List of selected canonical tasks in sequence
            - tasks_covered: List of task IDs used
        """
        logger.info(f"Composing execution plan V2.0 for: {prompt[:100]}...")
        
        # Construct canonical tasks reference
        tasks_reference = self._format_canonical_tasks()
        
        # Construct system message (OPTIMIZED V2.0 - Nov 7, 2025)
        system_message = f"""You are an expert at composing execution plans for Calendar.AI prompts using a validated set of 25 canonical unit tasks.

CANONICAL UNIT TASKS LIBRARY (Framework V2.0 - 25 tasks):

{tasks_reference}

CRITICAL TASK CONCEPTS (READ CAREFULLY):

1. **CAN-04 is UNIVERSAL (100% frequency)**: 
   - Natural Language Understanding - extract constraints/intents from user prompt
   - Include as FIRST STEP in ALL prompts - this is the entry point for every execution plan

2. **CAN-07 is a PARENT/FOUNDATIONAL TASK (78% frequency)**: 
   - Extracts meeting metadata (RSVP, attendees, attachments, notes, logistics)
   - ENABLES child tasks: CAN-13 (RSVP update), CAN-05 (Attendees), CAN-08 (Documents), CAN-09 (Generation), CAN-19 (Resources), CAN-21 (Prep time)
   - Use when prompt mentions: "pending invitations", "RSVP", "attendees", "documents", "prep materials", "meeting details"

3. **CAN-02 vs CAN-03 (DIFFERENT BUT OFTEN PAIRED)**:
   - CAN-02: Meeting Type Classification - format/structure (1:1, team sync, customer) - OBJECTIVE
   - CAN-03: Meeting Importance Assessment - strategic value, urgency, priority - SUBJECTIVE
   - Use BOTH when prompt asks to "prioritize meetings" (need type + importance)
   - Use CAN-02 alone for classification tasks
   - Use CAN-03 alone for importance/priority assessment

4. **CAN-13 vs CAN-07 (READ vs WRITE)**:
   - CAN-13: RSVP Status Update - WRITE/SEND response, UPDATE status
   - CAN-07: Meeting Metadata Extraction - READ/EXTRACT RSVP status
   - "Pending invitations" = CAN-07 (read), "Accept/decline invitations" = CAN-13 (write)

5. **CAN-25: Event Annotation/Flagging (NEW in V2.0)**:
   - Add flags/annotations to calendar events when conditions are met
   - Use when prompt asks to: "flag meetings", "mark important", "highlight", "annotate", "signal"
   - Common use cases: Flag meetings needing prep time, VIP attendees, budget approval, deadlines
   - Example: "Flag any that require focus time to prepare for them" → Use CAN-25

6. **SPECIALIZED TASKS** (use when keywords present):
   - CAN-18 (Objection/Risk): "anticipate", "risks", "objections", "blockers", "prepare for pushback", "concerns"
   - CAN-20 (Visualization): "show breakdown", "visualize", "dashboard", "patterns", "trends", "display", "chart"
   - CAN-23 (Agenda): "set agenda", "structure meeting", "topics", "outline"
   - CAN-17 (Auto-reschedule): "automatically reschedule", "auto-bump", "move meetings"
   - CAN-21 (Prep Time): "prep time", "focus time", "preparation", "get ready"
   - CAN-22 (Research): "background", "research", "find information", "intelligence"

7. **DEPENDENCIES** (must follow order):
   - CAN-04 (NLU) → ALL tasks (understand intent first)
   - CAN-01 (Calendar Retrieval) → CAN-06 (Availability) - can't check availability without calendar data
   - CAN-07 (Metadata) → CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21 - need metadata before child tasks
   - CAN-12 (Constraints) → CAN-17 (Rescheduling) - satisfy constraints before rescheduling

YOUR TASK:
1. **READ** the user prompt carefully - identify ALL capabilities needed
2. **SELECT** canonical tasks required - be thorough, don't miss specialized tasks or new CAN-25
3. **SEQUENCE** in logical execution order - respect dependencies
4. **EXPLAIN** what each task contributes - be specific about its role in THIS prompt

OUTPUT FORMAT - Return ONLY valid JSON (no markdown, no code blocks):
{{
  "execution_plan": [
    {{
      "step": 1,
      "task_id": "CAN-04",
      "task_name": "Natural Language Understanding",
      "description": "Extract scheduling constraints, priorities, and intent from user prompt",
      "input_schema": {{"user_query": "string"}},
      "output_schema": {{"constraints": "object", "intent": "string", "priorities": "array"}},
      "parallel_execution": false,
      "note": "Universal first step - always needed to parse natural language"
    }},
    {{
      "step": 2,
      "task_id": "CAN-01",
      "task_name": "Calendar Events Retrieval",
      "description": "Retrieve user's calendar events for specified timeframe",
      "input_schema": {{"time_range": "object"}},
      "output_schema": {{"events": "array"}},
      "parallel_execution": false
    }}
  ],
  "tasks_covered": ["CAN-04", "CAN-01", "CAN-07", ...],
  "orchestration": {{
    "pattern": "sequential / parallel / hybrid",
    "parallelization_opportunities": ["step 3 and step 4 can run in parallel"],
    "error_handling": "Retry failed tasks, graceful degradation for non-critical steps"
  }}
}}

SELECTION GUIDELINES:
✅ **DO**: Include CAN-04 (NLU) as step 1 for ALL prompts (100% frequency)
✅ **DO**: Use CAN-07 when prompt mentions: invitations, RSVP, attendees, documents, prep, meeting details
✅ **DO**: Use BOTH CAN-02 and CAN-03 when prioritizing meetings (type + importance)
✅ **DO**: Use CAN-25 when prompt asks to flag/mark/annotate meetings
✅ **DO**: Include specialized tasks (CAN-18, CAN-20, CAN-21, CAN-22, CAN-23) when keywords match
✅ **DO**: Respect dependencies (CAN-04 first, CAN-01 before CAN-06, CAN-07 before child tasks)
❌ **DON'T**: Invent task IDs not in the canonical library (only CAN-01 through CAN-25)
❌ **DON'T**: Skip CAN-04 (needed 100% of time as universal first step)
❌ **DON'T**: Confuse CAN-07 (extract/read) with CAN-13 (update/write)
❌ **DON'T**: Miss CAN-07 when prompt asks about "pending invitations" or "meeting details"
❌ **DON'T**: Forget CAN-25 for flagging/annotation requests (new in V2.0)

Be comprehensive - it's better to include a task that might help than to miss a critical one."""

        # Construct user prompt (OPTIMIZED V2.0)
        user_prompt = f"""Analyze this Calendar.AI user prompt and compose an execution plan using the 25 canonical unit tasks:

**USER PROMPT**: "{prompt}"

ANALYSIS REQUIREMENTS:
1. **Identify ALL needed capabilities** - read carefully for:
   - "Pending invitations" or "RSVP" or "meeting details" → Use CAN-07 (Metadata Extraction)
   - "Prioritize meetings" → Use BOTH CAN-02 (Type) AND CAN-03 (Importance)
   - "Show breakdown" or "visualize" → Use CAN-20 (Visualization)
   - "Auto-reschedule" or "bump" → Use CAN-17 (Automatic Rescheduling)
   - "Anticipate objections" or "risks" → Use CAN-18 (Risk Anticipation)
   - "Flag" or "mark" or "highlight" → Use CAN-25 (Event Annotation/Flagging) - NEW!
   - "Prep time" or "focus time" → Use CAN-21 (Preparation Time Analysis)
   - "Agenda" or "structure" → Use CAN-23 (Agenda Generation)
   - "Background" or "research" → Use CAN-22 (Research/Intelligence)

2. **SELECT canonical tasks** - from the 25 tasks above:
   - ALWAYS start with CAN-04 (NLU) - universal first step (100% frequency)
   - Include CAN-07 when metadata needed (RSVP, attendees, documents, details)
   - Use both CAN-02 and CAN-03 for priority-based meeting selection
   - Add specialized tasks when keywords match (especially new CAN-25 for flagging)

3. **SEQUENCE logically** - respect dependencies:
   - CAN-04 (NLU) first - always step 1
   - CAN-01 (Retrieval) before CAN-06 (Availability)
   - CAN-07 (Metadata) before child tasks (CAN-13, CAN-05, CAN-08, CAN-09, CAN-21, CAN-25)

4. **EXPLAIN each task** - what does it contribute to solving THIS specific prompt?

5. **OUTPUT valid JSON** - no markdown, no code blocks, just the JSON structure specified above.

Analyze the prompt now and return the execution composition as JSON:"""

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
                    "framework_version": "2.0",
                    "total_canonical_tasks": 25,
                    "timestamp": datetime.now().isoformat(),
                    "prompt_id": prompt_id,
                    "prompt_text": prompt,
                    "error": result.error,
                    "execution_plan": [],
                    "tasks_covered": []
                }
            
            # Parse JSON response
            response_content = result.response_content or ""
            composition_data = self._parse_gpt5_response(response_content)
            
            # Build result
            composition = {
                "source": "gpt-5",
                "backend_llm": self.model,
                "backend_llm_notes": "GPT-5 (dev-gpt-5-chat-jj) via Microsoft SilverFlow API",
                "framework_version": "2.0",
                "total_canonical_tasks": 25,
                "timestamp": datetime.now().isoformat(),
                "prompt_id": prompt_id or "unknown",
                "prompt_text": prompt,
                "execution_plan": composition_data.get("execution_plan", []),
                "tasks_covered": composition_data.get("tasks_covered", []),
                "orchestration": composition_data.get("orchestration", {}),
            }
            
            logger.info(f"Successfully composed plan V2.0 with {len(composition['tasks_covered'])} tasks")
            return composition
            
        except Exception as e:
            logger.error(f"Error during execution composition: {e}")
            return {
                "source": "gpt-5",
                "backend_llm": self.model,
                "framework_version": "2.0",
                "total_canonical_tasks": 25,
                "timestamp": datetime.now().isoformat(),
                "prompt_id": prompt_id or "unknown",
                "prompt_text": prompt,
                "error": str(e),
                "execution_plan": [],
                "tasks_covered": []
            }
    
    def _parse_gpt5_response(self, response_content: str) -> Dict[str, Any]:
        """Parse GPT-5 JSON response, handling markdown code blocks"""
        try:
            # Remove markdown code blocks if present
            content = response_content.strip()
            if content.startswith("```"):
                # Find the first { and last }
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    content = content[start:end+1]
            
            # Parse JSON
            data = json.loads(content)
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT-5 response as JSON: {e}")
            logger.error(f"Response content: {response_content[:500]}...")
            return {
                "execution_plan": [],
                "tasks_covered": [],
                "orchestration": {},
                "parse_error": str(e)
            }


def main():
    """Command-line interface for testing"""
    parser = argparse.ArgumentParser(
        description="GPT-5 Execution Composer V2.0 - Analyze prompts using 25 canonical tasks"
    )
    parser.add_argument(
        "prompt",
        help="Hero prompt to analyze"
    )
    parser.add_argument(
        "--prompt-id",
        help="Prompt identifier (e.g., organizer-1)",
        default=None
    )
    parser.add_argument(
        "--output",
        help="Output file for results (JSON)",
        default=None
    )
    parser.add_argument(
        "--model",
        help=f"GPT-5 model to use (default: {DEFAULT_MODEL})",
        default=DEFAULT_MODEL
    )
    parser.add_argument(
        "--endpoint",
        help=f"API endpoint (default: {DEFAULT_ENDPOINT})",
        default=DEFAULT_ENDPOINT
    )
    
    args = parser.parse_args()
    
    # Initialize composer
    composer = GPT5ExecutionComposerV2(
        model=args.model,
        endpoint=args.endpoint
    )
    
    # Compose execution plan
    print(f"\nAnalyzing prompt: {args.prompt}\n")
    result = composer.compose_execution_plan(
        prompt=args.prompt,
        prompt_id=args.prompt_id
    )
    
    # Display results
    print("\n" + "="*80)
    print("EXECUTION PLAN V2.0")
    print("="*80)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Results saved to: {output_path}")


if __name__ == "__main__":
    main()
