#!/usr/bin/env python3
"""
Claude Sonnet 4.5 Execution Composition Analyzer

Given the 24 canonical unit tasks, analyze hero prompts and compose execution plans
by selecting and sequencing the appropriate canonical tasks.

This is COMPOSITION analysis, not task discovery.
"""

import os
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

try:
    import anthropic
except ImportError:
    print("❌ anthropic package not installed. Install with: pip install anthropic")
    sys.exit(1)


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


class ClaudeExecutionComposer:
    """
    Execution Composition Analyzer using Claude Sonnet 4.5.
    
    Given 24 canonical unit tasks, compose execution plans by selecting
    and sequencing the appropriate tasks for each hero prompt.
    """
    
    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str = None):
        """
        Initialize Claude execution composer
        
        Args:
            model: Claude model name (claude-sonnet-4-20250514 = Sonnet 4.5)
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
        """
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY env var or pass api_key parameter")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        print(f"✓ Initialized Claude Execution Composer with model: {model}")
    
    def compose_execution_plan(self, prompt: str, prompt_id: str = None, verbose: bool = True) -> Dict[str, Any]:
        """
        Compose an execution plan by selecting from 24 canonical tasks.
        
        Args:
            prompt: The hero prompt to analyze
            prompt_id: Optional prompt identifier (e.g., "organizer-1")
            verbose: Whether to show progress
            
        Returns:
            Dictionary with execution composition
        """
        
        # Format canonical tasks reference
        tasks_reference = self._format_canonical_tasks()
        
        analysis_prompt = f"""You are an expert at composing execution plans for Calendar.AI prompts using a validated set of canonical unit tasks.

CANONICAL UNIT TASKS LIBRARY (24 tasks - Framework V2.0):

{tasks_reference}

KEY CONCEPTS:
- **CAN-07 is a PARENT TASK**: It extracts metadata that enables CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21
- **CAN-02A vs CAN-02B**: CAN-02A is format-based type classification (1:1, team sync, etc.), CAN-02B is value-based importance assessment (strategic, urgent, etc.)
- **CAN-04 is UNIVERSAL**: Every prompt requires NLU to extract constraints/intents from natural language
- **Dependencies**: 
  - CAN-01 (retrieval) must precede CAN-06 (availability checking)
  - CAN-07 (metadata) enables child tasks: CAN-13, CAN-05, CAN-08, CAN-09, CAN-19, CAN-21
  - CAN-12 (CSP) may require CAN-23 (conflict resolution) for unsatisfiable constraints

**User Prompt**: "{prompt}"

Your task:
1. Analyze the user prompt and identify what capabilities are needed
2. SELECT only the canonical tasks required (from the 24 above - use task IDs CAN-01 to CAN-23)
3. SEQUENCE them in logical execution order
4. For each selected task, explain what it contributes to solving the prompt
5. Identify opportunities for parallel execution
6. Describe the orchestration pattern and error handling strategy

**CRITICAL Instructions**:
- Only use task IDs from the canonical library (CAN-01 through CAN-23, including CAN-02A and CAN-02B)
- Do NOT invent new task IDs
- Include CAN-04 (NLU) as first step for almost all prompts
- Respect task dependencies (CAN-01 before CAN-06, CAN-07 enables children)
- Be specific about what each task contributes
- Consider whether tasks can run in parallel

**Output Format**: Respond ONLY with valid JSON in this exact structure:
{{
  "execution_plan": [
    {{
      "step": 1,
      "task_id": "CAN-04",
      "task_name": "Natural Language Understanding",
      "description": "Extract user's scheduling constraints and intent from the prompt",
      "input_schema": {{"user_query": "string"}},
      "output_schema": {{"constraints": "object", "intent": "string"}},
      "parallel_execution": false,
      "note": "Optional: Dependencies or special considerations"
    }},
    {{
      "step": 2,
      "task_id": "CAN-01",
      "task_name": "Calendar Events Retrieval",
      "description": "Retrieve user's calendar events for the specified timeframe",
      "input_schema": {{"time_range": "object"}},
      "output_schema": {{"events": "array"}},
      "parallel_execution": false
    }}
  ],
  "tasks_covered": ["CAN-04", "CAN-01", ...],
  "orchestration": {{
    "pattern": "sequential / parallel / hybrid",
    "parallelization_opportunities": ["step 3 (can process all events in parallel)", "step 5"],
    "error_handling": "Description of how errors should be handled"
  }}
}}

**Important**: 
- Output ONLY valid JSON, no markdown formatting, no explanations outside JSON
- Use exact task IDs from the canonical library
- Sequence tasks logically
- Identify parallel execution opportunities
- Be specific about input/output schemas

Analyze the prompt now and output the execution composition:"""

        if verbose:
            print(f"\n🤖 Querying Claude ({self.model}) for execution composition...")
            print(f"   Prompt: {prompt[:100]}...")
            print("\n" + "=" * 80)
        
        try:
            # Query Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            if verbose:
                print("Claude Response Received")
                print("=" * 80 + "\n")
            
            # Parse JSON response
            try:
                # Try to find JSON in response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx == -1 or end_idx == 0:
                    print("⚠️  No JSON found in response")
                    return self._create_error_response(prompt, prompt_id, "No JSON in response")
                
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Validate structure
                if "execution_plan" not in result:
                    print("⚠️  Missing 'execution_plan' in response")
                    return self._create_error_response(prompt, prompt_id, "Missing execution_plan")
                
                # Extract tasks_covered if not present
                if "tasks_covered" not in result:
                    result["tasks_covered"] = [step["task_id"] for step in result["execution_plan"] if "task_id" in step]
                
                # Build final composition
                composition = {
                    "source": "claude",
                    "backend_llm": self.model,
                    "backend_llm_notes": "Claude Sonnet 4.5 (claude-sonnet-4-20250514) via Anthropic API",
                    "timestamp": datetime.now().isoformat(),
                    "prompt_id": prompt_id or "unknown",
                    "prompt_text": prompt,
                    "execution_plan": result["execution_plan"],
                    "tasks_covered": result["tasks_covered"],
                    "orchestration": result.get("orchestration", {}),
                }
                
                if verbose:
                    print(f"✓ Composed plan with {len(composition['tasks_covered'])} tasks")
                
                return composition
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {e}")
                print(f"Response excerpt: {response_text[:500]}")
                return self._create_error_response(prompt, prompt_id, f"JSON parse error: {e}")
                
        except Exception as e:
            print(f"❌ API error: {e}")
            return self._create_error_response(prompt, prompt_id, str(e))
    
    def _format_canonical_tasks(self) -> str:
        """Format canonical tasks as a reference list"""
        lines = []
        for task in CANONICAL_TASKS:
            lines.append(f"{task['id']}: {task['name']}")
            lines.append(f"   Description: {task['description']}")
            lines.append(f"   Tier: {task['tier']} | Frequency: {task['frequency']}")
            lines.append("")
        return "\n".join(lines)
    
    def _create_error_response(self, prompt: str, prompt_id: str, error: str) -> Dict[str, Any]:
        """Create error response structure"""
        return {
            "source": "claude",
            "backend_llm": self.model,
            "timestamp": datetime.now().isoformat(),
            "prompt_id": prompt_id or "unknown",
            "prompt_text": prompt,
            "error": error,
            "execution_plan": [],
            "tasks_covered": []
        }
    
    def save_composition(self, composition: Dict[str, Any], output_file: str):
        """Save execution composition to JSON file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(composition, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved composition to {output_path}")


def main():
    """Main entry point for Claude execution composer"""
    parser = argparse.ArgumentParser(
        description="Compose execution plans from 24 canonical tasks using Claude Sonnet 4.5"
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
        default="claude-sonnet-4-20250514",
        help="Claude model to use (default: claude-sonnet-4-20250514)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    # Initialize composer
    composer = ClaudeExecutionComposer(model=args.model)
    
    # Compose execution plan
    print(f"\n🔍 Composing execution plan with Claude Sonnet 4.5...")
    print(f"Model: {args.model}")
    print(f"Prompt: {args.prompt}\n")
    
    composition = composer.compose_execution_plan(
        args.prompt, 
        args.prompt_id,
        verbose=not args.quiet
    )
    
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
        output_file = f"claude_execution_composition_{prompt_id}_{timestamp}.json"
    
    composer.save_composition(composition, output_file)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
