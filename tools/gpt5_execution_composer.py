#!/usr/bin/env python3
"""
GPT-5 Execution Composition Analyzer

Given the 24 canonical unit tasks, analyze hero prompts and compose execution plans
by selecting and sequencing the appropriate canonical tasks.

This is COMPOSITION analysis, not task discovery.
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


# 24 Canonical Unit Tasks (Framework V2.0)
CANONICAL_TASKS = [
    {
        "id": "CAN-01",
        "name": "Calendar Events Retrieval",
        "description": "Retrieve calendar events from user's calendar within specified timeframe",
        "tier": 1,
        "frequency": "100%"
    },
    {
        "id": "CAN-02A",
        "name": "Meeting Type Classification",
        "description": "Classify meetings by format/structure (1:1, team sync, customer, etc.) - objective, format-based",
        "tier": 1,
        "frequency": "78%"
    },
    {
        "id": "CAN-02B",
        "name": "Meeting Importance Assessment",
        "description": "Assess strategic importance, urgency, reschedulability - subjective, value-based",
        "tier": 1,
        "frequency": "67%"
    },
    {
        "id": "CAN-03",
        "name": "Calendar Event Creation/Update",
        "description": "Create new calendar events or update existing ones (title, time, attendees, recurrence)",
        "tier": 1,
        "frequency": "44%"
    },
    {
        "id": "CAN-04",
        "name": "Natural Language Understanding (NLU)",
        "description": "Extract structured constraints, intents, entities from natural language input",
        "tier": 1,
        "frequency": "100%"
    },
    {
        "id": "CAN-05",
        "name": "Attendee/Contact Resolution",
        "description": "Resolve attendee names to directory entries, expand teams, handle disambiguation",
        "tier": 1,
        "frequency": "44%"
    },
    {
        "id": "CAN-06",
        "name": "Availability Checking",
        "description": "Check free/busy status across multiple calendars, find common available slots",
        "tier": 2,
        "frequency": "33%"
    },
    {
        "id": "CAN-07",
        "name": "Meeting Metadata Extraction",
        "description": "Extract RSVP status, attendees, attachments, notes, logistics from meetings (PARENT TASK)",
        "tier": 2,
        "frequency": "56%"
    },
    {
        "id": "CAN-08",
        "name": "Document/Content Retrieval",
        "description": "Retrieve attachments, pre-reads, shared documents from meetings",
        "tier": 2,
        "frequency": "33%"
    },
    {
        "id": "CAN-09",
        "name": "Document Generation/Formatting",
        "description": "Generate agendas, summaries, briefings using templates and LLMs",
        "tier": 2,
        "frequency": "33%"
    },
    {
        "id": "CAN-10",
        "name": "Time Aggregation/Statistical Analysis",
        "description": "Aggregate time spent in meetings, compute statistics, identify patterns",
        "tier": 2,
        "frequency": "11%"
    },
    {
        "id": "CAN-11",
        "name": "Priority/Preference Matching",
        "description": "Match meetings against user's stated priorities and preferences",
        "tier": 2,
        "frequency": "22%"
    },
    {
        "id": "CAN-12",
        "name": "Constraint Satisfaction",
        "description": "Solve scheduling constraints using CSP/optimization algorithms",
        "tier": 2,
        "frequency": "22%"
    },
    {
        "id": "CAN-13",
        "name": "RSVP Status Update/Notification",
        "description": "Update RSVP status, send meeting notifications to attendees",
        "tier": 2,
        "frequency": "11%"
    },
    {
        "id": "CAN-14",
        "name": "Recommendation Engine",
        "description": "Generate personalized recommendations based on calendar data and user behavior",
        "tier": 2,
        "frequency": "22%"
    },
    {
        "id": "CAN-15",
        "name": "Recurrence Rule Generation",
        "description": "Generate RRULE patterns for recurring meetings (daily, weekly, monthly, etc.)",
        "tier": 3,
        "frequency": "11%"
    },
    {
        "id": "CAN-16",
        "name": "Event Monitoring/Change Detection",
        "description": "Monitor calendar events for changes, trigger webhooks, detect conflicts",
        "tier": 3,
        "frequency": "11%"
    },
    {
        "id": "CAN-17",
        "name": "Automatic Rescheduling",
        "description": "Automatically reschedule meetings when conflicts or changes occur (orchestrated workflow)",
        "tier": 3,
        "frequency": "11%"
    },
    {
        "id": "CAN-18",
        "name": "Objection/Risk Anticipation",
        "description": "Analyze previous meetings to anticipate objections, risks, blockers",
        "tier": 3,
        "frequency": "11%"
    },
    {
        "id": "CAN-19",
        "name": "Resource/Logistics Booking",
        "description": "Book meeting rooms, equipment, catering, other logistics",
        "tier": 3,
        "frequency": "11%"
    },
    {
        "id": "CAN-20",
        "name": "Data Visualization/Reporting",
        "description": "Generate charts, graphs, dashboards showing calendar analytics",
        "tier": 3,
        "frequency": "11%"
    },
    {
        "id": "CAN-21",
        "name": "Task Duration Estimation",
        "description": "Estimate meeting prep time based on complexity, attachments, agenda",
        "tier": 2,
        "frequency": "11%"
    },
    {
        "id": "CAN-22",
        "name": "Work Attribution Discovery",
        "description": "Discover who works on what based on collaboration patterns, documents, meetings",
        "tier": 2,
        "frequency": "11%"
    },
    {
        "id": "CAN-23",
        "name": "Conflict Resolution",
        "description": "Handle unsatisfiable constraints with trade-off analysis and escalation",
        "tier": 3,
        "frequency": "11%"
    }
]


class GPT5ExecutionComposer:
    """
    Execution Composition Analyzer using GPT-5.
    
    Given 24 canonical unit tasks, compose execution plans by selecting
    and sequencing the appropriate tasks for each hero prompt.
    """
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        endpoint: str = DEFAULT_ENDPOINT,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """Initialize GPT-5 Execution Composer"""
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
        
        logger.info(f"Initialized GPT-5 Execution Composer with model: {model}")
    
    def compose_execution_plan(self, prompt: str, prompt_id: str = None) -> Dict[str, Any]:
        """
        Compose an execution plan by selecting from 24 canonical tasks.
        
        Args:
            prompt: The hero prompt to analyze
            prompt_id: Optional prompt identifier (e.g., "organizer-1")
            
        Returns:
            Dictionary with execution composition including:
            - source: "gpt-5"
            - model: Model identifier
            - timestamp: ISO timestamp
            - prompt_id: Prompt identifier
            - prompt_text: Input prompt
            - execution_plan: List of selected canonical tasks in sequence
            - tasks_covered: List of task IDs used
        """
        logger.info(f"Composing execution plan for: {prompt[:100]}...")
        
        # Construct canonical tasks reference
        tasks_reference = self._format_canonical_tasks()
        
        # Construct system message (OPTIMIZED VERSION - Nov 7, 2025)
        system_message = f"""You are an expert at composing execution plans for Calendar.AI prompts using a validated set of 24 canonical unit tasks.

CANONICAL UNIT TASKS LIBRARY (Framework V2.0 - 24 tasks):

{tasks_reference}

CRITICAL TASK CONCEPTS (READ CAREFULLY):

1. **CAN-07 is a PARENT/FOUNDATIONAL TASK**: 
   - Extracts meeting metadata (RSVP, attendees, attachments, notes, logistics)
   - ENABLES child tasks: CAN-13 (RSVP), CAN-05 (Attendees), CAN-08 (Documents), CAN-09 (Generation), CAN-19 (Resources), CAN-21 (Duration)
   - Use when prompt needs: "pending invitations", "RSVP", "attendees", "documents", "prep materials"

2. **CAN-02A vs CAN-02B (DIFFERENT TASKS)**:
   - CAN-02A: Meeting Type Classification - format/structure (1:1, team sync, customer) - OBJECTIVE
   - CAN-02B: Meeting Importance Assessment - strategic value, urgency, priority - SUBJECTIVE
   - Use BOTH when prompt asks about "prioritize" + "which meetings" (type + importance)

3. **CAN-04 is UNIVERSAL**: 
   - Natural Language Understanding - extract constraints/intents from user prompt
   - Include as FIRST STEP in nearly all prompts (100% frequency in gold standard)

4. **CAN-13 vs CAN-07**:
   - CAN-13: RSVP Status Update/Notification - SEND response, UPDATE status
   - CAN-07: Meeting Metadata Extraction - READ/EXTRACT RSVP status
   - "Pending invitations" = CAN-07 (read), "Respond to invitations" = CAN-13 (write)

5. **SPECIALIZED TASKS** (use when keywords present):
   - CAN-18 (Objection/Risk): "anticipate", "risks", "objections", "blockers", "prepare for pushback"
   - CAN-20 (Visualization): "show", "visualize", "dashboard", "patterns", "trends", "display"
   - CAN-23 (Conflict Resolution): "auto-reschedule", "bump", "prioritize conflicts", "resolve"

6. **DEPENDENCIES** (must follow order):
   - CAN-01 (Calendar Retrieval) → CAN-06 (Availability Checking) - can't check availability without calendar
   - CAN-07 (Metadata Extraction) → CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21 - need metadata first
   - CAN-12 (Constraint Satisfaction) → CAN-23 (Conflict Resolution) - handle unsatisfiable constraints

YOUR TASK:
1. **READ** the user prompt carefully - identify ALL capabilities needed
2. **SELECT** canonical tasks required - be thorough, don't miss specialized tasks
3. **SEQUENCE** in logical execution order - respect dependencies
4. **EXPLAIN** what each task contributes - be specific about its role

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
✅ **DO**: Include CAN-04 (NLU) as step 1 for all prompts
✅ **DO**: Use CAN-07 when prompt mentions: invitations, RSVP, attendees, documents, prep
✅ **DO**: Use BOTH CAN-02A and CAN-02B when prioritizing meetings (type + importance)
✅ **DO**: Include specialized tasks (CAN-18, CAN-20, CAN-23) when keywords match
✅ **DO**: Respect dependencies (CAN-01 before CAN-06, CAN-07 before child tasks)
❌ **DON'T**: Invent task IDs not in the canonical library
❌ **DON'T**: Skip CAN-04 (needed 100% of time)
❌ **DON'T**: Confuse CAN-07 (extract) with CAN-13 (update)
❌ **DON'T**: Miss CAN-07 when prompt asks about "pending invitations"

Be comprehensive - it's better to include a task that might help than to miss a critical one."""

        # Construct user prompt (OPTIMIZED)
        user_prompt = f"""Analyze this Calendar.AI user prompt and compose an execution plan using the 24 canonical unit tasks:

**USER PROMPT**: "{prompt}"

ANALYSIS REQUIREMENTS:
1. **Identify ALL needed capabilities** - read carefully for:
   - "Pending invitations" or "RSVP" → Use CAN-07 (Metadata Extraction)
   - "Prioritize" + "meetings" → Use BOTH CAN-02A (Type) AND CAN-02B (Importance)
   - "Show patterns" or "visualize" → Use CAN-20 (Visualization)
   - "Auto-reschedule" or "bump" → Use CAN-23 (Conflict Resolution)
   - "Anticipate objections" → Use CAN-18 (Risk Anticipation)

2. **SELECT canonical tasks** - from the 24 tasks above:
   - ALWAYS start with CAN-04 (NLU) - universal first step
   - Include CAN-07 when metadata needed (RSVP, attendees, documents)
   - Use both CAN-02A and CAN-02B for priority-based meeting selection
   - Add specialized tasks (CAN-18, CAN-20, CAN-23) when keywords match

3. **SEQUENCE logically** - respect dependencies:
   - CAN-04 (NLU) first
   - CAN-01 (Retrieval) before CAN-06 (Availability)
   - CAN-07 (Metadata) before child tasks (CAN-13, CAN-05, CAN-08, CAN-09)

4. **EXPLAIN each task** - what does it contribute to solving this specific prompt?

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
                "timestamp": datetime.now().isoformat(),
                "prompt_id": prompt_id or "unknown",
                "prompt_text": prompt,
                "execution_plan": composition_data.get("execution_plan", []),
                "tasks_covered": composition_data.get("tasks_covered", []),
                "orchestration": composition_data.get("orchestration", {}),
            }
            
            logger.info(f"Successfully composed plan with {len(composition['tasks_covered'])} tasks")
            return composition
            
        except Exception as e:
            logger.error(f"Error during execution composition: {e}")
            return {
                "source": "gpt-5",
                "backend_llm": self.model,
                "timestamp": datetime.now().isoformat(),
                "prompt_id": prompt_id,
                "prompt_text": prompt,
                "error": str(e),
                "execution_plan": [],
                "tasks_covered": []
            }
    
    def _format_canonical_tasks(self) -> str:
        """Format canonical tasks as a reference list"""
        lines = []
        for task in CANONICAL_TASKS:
            lines.append(f"{task['id']}: {task['name']}")
            lines.append(f"   Description: {task['description']}")
            lines.append(f"   Tier: {task['tier']} | Frequency: {task['frequency']}")
            lines.append("")
        return "\n".join(lines)
    
    def _parse_gpt5_response(self, response_content: str) -> Dict[str, Any]:
        """Parse GPT-5 response to extract execution composition"""
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
            if "execution_plan" not in data:
                logger.warning("Response missing 'execution_plan' key")
                return {"execution_plan": [], "tasks_covered": []}
            
            if "tasks_covered" not in data:
                # Extract task IDs from execution plan
                tasks_covered = [step["task_id"] for step in data["execution_plan"] if "task_id" in step]
                data["tasks_covered"] = tasks_covered
            
            logger.info(f"Parsed execution plan with {len(data['execution_plan'])} steps")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {content[:500]}")
            return {"execution_plan": [], "tasks_covered": []}
    
    def save_composition(self, composition: Dict[str, Any], output_file: str):
        """Save execution composition to JSON file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(composition, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved composition to {output_path}")


def main():
    """Main entry point for GPT-5 execution composer"""
    parser = argparse.ArgumentParser(
        description="Compose execution plans from 24 canonical tasks using GPT-5"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Hero prompt to analyze"
    )
    parser.add_argument(
        "--prompt-id",
        type=str,
        default=None,
        help="Prompt identifier (e.g., organizer-1)"
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
        help="Output JSON file path"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize composer
    composer = GPT5ExecutionComposer(model=args.model)
    
    # Compose execution plan
    print(f"\n🔍 Composing execution plan with GPT-5...")
    print(f"Model: {args.model}")
    print(f"Prompt: {args.prompt}\n")
    
    composition = composer.compose_execution_plan(args.prompt, args.prompt_id)
    
    # Display results
    task_count = len(composition.get("tasks_covered", []))
    print(f"\n📊 Results:")
    print(f"Tasks used: {task_count}/24")
    print(f"Execution steps: {len(composition.get('execution_plan', []))}")
    
    if composition.get("error"):
        print(f"❌ Error: {composition['error']}")
    else:
        print(f"\nExecution Plan:")
        for step in composition.get("execution_plan", []):
            print(f"\n{step['step']}. {step['task_id']} - {step['task_name']}")
            print(f"   {step['description']}")
            if step.get('note'):
                print(f"   Note: {step['note']}")
        
        print(f"\n✅ Tasks Covered: {', '.join(composition.get('tasks_covered', []))}")
    
    # Save to file
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_id = args.prompt_id or "unknown"
        output_file = f"gpt5_execution_composition_{prompt_id}_{timestamp}.json"
    
    composer.save_composition(composition, output_file)
    print(f"\n💾 Saved to: {output_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
