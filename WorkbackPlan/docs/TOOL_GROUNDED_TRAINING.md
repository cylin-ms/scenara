# Tool-Grounded Plan Generation for Production Systems

**Version**: 1.0  
**Date**: November 18, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Ensure generated plans only use tools available in production (e.g., BizChat)

---

## Problem Statement

**Challenge**: Model generates workback plans that reference tools/actions not available in the production environment.

**Example Mismatch**:
- **Model generates**: `"Run sentiment analysis on customer feedback"`
- **BizChat reality**: No sentiment analysis tool available
- **Result**: Plan is unexecutable, user frustrated

**Root Cause**: Training and inference are disconnected from production tool constraints.

---

## Architecture: Tool-Aware Training

### Production Tool Registry

Define exactly what tools the production system (e.g., BizChat) has access to.

**File**: `test_tenant/tools/bizchat_tool_registry.json`

```json
{
  "environment": "Microsoft BizChat",
  "version": "2.0",
  "last_updated": "2025-11-18",
  "tools": [
    {
      "id": "graph_calendar_get_events",
      "name": "Get Calendar Events",
      "description": "Retrieve calendar events for a user within a date range",
      "category": "calendar",
      "parameters": {
        "user_email": "string (required)",
        "start_date": "ISO8601 datetime (required)",
        "end_date": "ISO8601 datetime (required)",
        "top": "integer (optional, default 50)"
      },
      "returns": "List of calendar events with subject, start, end, attendees",
      "example": {
        "input": {
          "user_email": "alice@company.com",
          "start_date": "2025-12-01T00:00:00Z",
          "end_date": "2025-12-31T23:59:59Z"
        },
        "output": [
          {
            "id": "evt001",
            "subject": "Q4 Board Review",
            "start": "2025-12-15T14:00:00Z",
            "end": "2025-12-15T16:00:00Z",
            "attendees": ["alice@company.com", "bob@company.com"]
          }
        ]
      },
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "graph_user_get_profile",
      "name": "Get User Profile",
      "description": "Get detailed information about a user",
      "category": "directory",
      "parameters": {
        "user_email": "string (required)"
      },
      "returns": "User profile with name, title, department, manager",
      "example": {
        "input": {"user_email": "alice@company.com"},
        "output": {
          "displayName": "Alice Johnson",
          "jobTitle": "CEO",
          "department": "Executive",
          "mail": "alice@company.com",
          "manager": null
        }
      },
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "graph_user_get_manager",
      "name": "Get User's Manager",
      "description": "Get the manager of a specified user",
      "category": "directory",
      "parameters": {
        "user_email": "string (required)"
      },
      "returns": "Manager's profile",
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "sharepoint_search_documents",
      "name": "Search SharePoint Documents",
      "description": "Search for documents in SharePoint by keyword or tags",
      "category": "documents",
      "parameters": {
        "query": "string (required)",
        "top": "integer (optional, default 10)",
        "filters": "object (optional) - {fileType, modifiedAfter, owner}"
      },
      "returns": "List of documents with name, URL, modified date, owner",
      "example": {
        "input": {
          "query": "Q4 Financial Report",
          "top": 5,
          "filters": {"fileType": "pptx", "modifiedAfter": "2025-10-01"}
        },
        "output": [
          {
            "name": "Q4_Financial_Report_Draft.pptx",
            "url": "https://company.sharepoint.com/sites/finance/Q4_Financial_Report_Draft.pptx",
            "modified": "2025-11-15T10:30:00Z",
            "owner": "bob.cfo@company.com"
          }
        ]
      },
      "cost": "medium",
      "reliability": "medium"
    },
    {
      "id": "sharepoint_get_file_metadata",
      "name": "Get File Metadata",
      "description": "Get detailed metadata for a SharePoint file",
      "category": "documents",
      "parameters": {
        "file_url": "string (required)"
      },
      "returns": "File metadata including size, permissions, version history",
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "planner_create_task",
      "name": "Create Planner Task",
      "description": "Create a task in Microsoft Planner",
      "category": "task_management",
      "parameters": {
        "plan_id": "string (required)",
        "title": "string (required)",
        "assigned_to": "string (optional) - user email",
        "due_date": "ISO8601 datetime (optional)",
        "description": "string (optional)"
      },
      "returns": "Created task with ID and details",
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "planner_get_plan_tasks",
      "name": "Get Plan Tasks",
      "description": "Get all tasks in a Planner plan",
      "category": "task_management",
      "parameters": {
        "plan_id": "string (required)"
      },
      "returns": "List of tasks with status, assignee, due date",
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "teams_send_message",
      "name": "Send Teams Message",
      "description": "Send a message to a Teams channel or chat",
      "category": "communication",
      "parameters": {
        "channel_id": "string (required)",
        "message": "string (required)",
        "mentions": "array of user emails (optional)"
      },
      "returns": "Message ID",
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "outlook_send_email",
      "name": "Send Outlook Email",
      "description": "Send an email via Outlook",
      "category": "communication",
      "parameters": {
        "to": "array of email addresses (required)",
        "subject": "string (required)",
        "body": "string (required)",
        "cc": "array of email addresses (optional)"
      },
      "returns": "Email ID",
      "cost": "low",
      "reliability": "high"
    },
    {
      "id": "graph_organization_get_holidays",
      "name": "Get Organization Holidays",
      "description": "Get list of company holidays for a date range",
      "category": "policies",
      "parameters": {
        "start_date": "ISO8601 date (required)",
        "end_date": "ISO8601 date (required)",
        "region": "string (optional) - US, EU, APAC"
      },
      "returns": "List of holidays with date, name, region",
      "cost": "low",
      "reliability": "high"
    }
  ],
  "tool_categories": {
    "calendar": ["graph_calendar_get_events"],
    "directory": ["graph_user_get_profile", "graph_user_get_manager"],
    "documents": ["sharepoint_search_documents", "sharepoint_get_file_metadata"],
    "task_management": ["planner_create_task", "planner_get_plan_tasks"],
    "communication": ["teams_send_message", "outlook_send_email"],
    "policies": ["graph_organization_get_holidays"]
  },
  "constraints": {
    "max_parallel_calls": 5,
    "rate_limit_per_minute": 60,
    "timeout_seconds": 30,
    "max_results_per_call": 100
  }
}
```

---

## Training Data: Tool-Grounded Plans

### SFT Examples Must Use Real Tools

**Before (Ungrounded)**:
```json
{
  "scenario": "QBR on Dec 15, 2025",
  "plan": {
    "tasks": [
      {
        "name": "Analyze Q4 revenue trends",
        "action": "run_revenue_analysis_pipeline()",  // ← Not a BizChat tool!
        "owner": "CFO"
      }
    ]
  }
}
```

**After (Tool-Grounded)**:
```json
{
  "scenario": "QBR on Dec 15, 2025",
  "plan": {
    "tasks": [
      {
        "name": "Find previous Q4 financial reports",
        "tool": "sharepoint_search_documents",
        "tool_params": {
          "query": "Q4 Financial Report",
          "filters": {"fileType": "pptx", "modifiedAfter": "2024-10-01"}
        },
        "owner": "CFO",
        "output_used_by": ["task_002"]
      },
      {
        "id": "task_002",
        "name": "Review previous reports and identify format",
        "tool": null,
        "manual_action": "CFO reviews documents to identify standard format",
        "depends_on": ["task_001"],
        "owner": "CFO"
      }
    ]
  }
}
```

---

## Modified Plan Schema: Tool-Aware

**File**: `src/workback_planning/models/plan.py` (updated)

```python
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Represents a grounded tool call available in production"""
    tool_id: str = Field(..., description="Tool ID from registry (e.g., 'graph_calendar_get_events')")
    tool_name: str = Field(..., description="Human-readable tool name")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")
    expected_output: str = Field(..., description="What this tool call should produce")
    fallback_manual: Optional[str] = Field(None, description="Manual fallback if tool fails")


class Task(BaseModel):
    """Task in workback plan with tool grounding"""
    id: str
    name: str
    description: str
    owner: str
    milestone: str
    
    # NEW: Tool grounding fields
    tool_call: Optional[ToolCall] = Field(None, description="If task uses a BizChat tool")
    manual_action: Optional[str] = Field(None, description="If task is manual (no tool)")
    
    # Existing fields
    depends_on: List[str] = Field(default_factory=list)
    estimated_hours: Optional[float] = None
    deliverables: List[str] = Field(default_factory=list)
    
    def is_automated(self) -> bool:
        """Check if task can be executed by tools"""
        return self.tool_call is not None
    
    def validate_tool_availability(self, available_tools: List[str]) -> bool:
        """Validate that tool_id exists in production environment"""
        if self.tool_call:
            return self.tool_call.tool_id in available_tools
        return True  # Manual tasks always valid
```

---

## Training: Inject Tool Registry into Prompts

### Updated Prompt Template

**File**: `src/workback_planning/prompts/structure.md` (updated section)

```markdown
# IMPORTANT: Tool Constraints

You are generating a workback plan for a system with LIMITED TOOLS.
You can ONLY use the following tools in task actions:

## Available Tools in Production (BizChat)

### Calendar Tools
- **graph_calendar_get_events**: Get user's calendar events in date range
  - Params: user_email (str), start_date (ISO8601), end_date (ISO8601)
  - Returns: List of events with subject, start, end, attendees

### Directory Tools
- **graph_user_get_profile**: Get user details
  - Params: user_email (str)
  - Returns: User profile (name, title, department, manager)

- **graph_user_get_manager**: Get user's manager
  - Params: user_email (str)
  - Returns: Manager profile

### Document Tools
- **sharepoint_search_documents**: Search SharePoint for documents
  - Params: query (str), top (int), filters (object)
  - Returns: List of documents with URL, owner, modified date

- **sharepoint_get_file_metadata**: Get file details
  - Params: file_url (str)
  - Returns: File metadata (size, permissions, version)

### Task Management Tools
- **planner_create_task**: Create a task in Microsoft Planner
  - Params: plan_id (str), title (str), assigned_to (str), due_date (ISO8601)
  - Returns: Task ID

- **planner_get_plan_tasks**: Get all tasks in a plan
  - Params: plan_id (str)
  - Returns: List of tasks with status, assignee, due date

### Communication Tools
- **teams_send_message**: Send Teams message
  - Params: channel_id (str), message (str), mentions (array)
  - Returns: Message ID

- **outlook_send_email**: Send email
  - Params: to (array), subject (str), body (str)
  - Returns: Email ID

### Policy Tools
- **graph_organization_get_holidays**: Get company holidays
  - Params: start_date (ISO8601), end_date (ISO8601), region (str)
  - Returns: List of holidays

## Task Action Rules

1. **If a task can be automated**: Specify `tool_call` with tool_id and parameters
2. **If a task is manual**: Set `tool_call` to null and describe action in `manual_action`
3. **Never invent tools**: Only use tools from the list above
4. **Chain tools properly**: If task B needs output from task A's tool, specify dependency

## Example Tool-Grounded Tasks

```json
{
  "tasks": [
    {
      "id": "T1",
      "name": "Find previous QBR decks",
      "tool_call": {
        "tool_id": "sharepoint_search_documents",
        "tool_name": "Search SharePoint Documents",
        "parameters": {
          "query": "QBR Q3 2025",
          "top": 5,
          "filters": {"fileType": "pptx"}
        },
        "expected_output": "List of 3-5 previous QBR presentations"
      },
      "manual_action": null,
      "owner": "PM",
      "depends_on": []
    },
    {
      "id": "T2",
      "name": "Review previous decks and extract template",
      "tool_call": null,
      "manual_action": "PM manually reviews previous decks to identify slide structure, key metrics, and format standards",
      "owner": "PM",
      "depends_on": ["T1"]
    },
    {
      "id": "T3",
      "name": "Notify team of QBR preparation kickoff",
      "tool_call": {
        "tool_id": "teams_send_message",
        "tool_name": "Send Teams Message",
        "parameters": {
          "channel_id": "exec-team-channel",
          "message": "QBR preparation starts today. Please submit your section inputs by T-14.",
          "mentions": ["cfo@company.com", "cto@company.com"]
        },
        "expected_output": "Teams message sent, team notified"
      },
      "manual_action": null,
      "owner": "PM",
      "depends_on": ["T2"]
    }
  ]
}
```
```

---

## RFT Reward: Tool Compliance Check

**File**: `test_tenant/training/rft_reward_checker.py` (add new check)

```python
def check_tool_grounding(plan: Dict[str, Any], available_tools: List[str]) -> bool:
    """
    NEW: Check that all tool_calls reference valid production tools.
    
    This is critical for RFT training - model must learn to only use
    tools that actually exist in BizChat.
    """
    tasks = plan.get('tasks', [])
    
    for task in tasks:
        tool_call = task.get('tool_call')
        if tool_call:
            tool_id = tool_call.get('tool_id')
            
            # Check 1: Tool exists in registry
            if tool_id not in available_tools:
                return False
            
            # Check 2: Required parameters present
            # (Could validate against tool schema from registry)
            if 'parameters' not in tool_call:
                return False
    
    return True


def calculate_reward(plan: Dict[str, Any], scenario: Dict[str, Any]) -> float:
    """Enhanced reward with tool grounding check"""
    reward = 0.0
    
    # Load available tools from registry
    with open('test_tenant/tools/bizchat_tool_registry.json') as f:
        registry = json.load(f)
    available_tools = [t['id'] for t in registry['tools']]
    
    # Existing checks
    if check_no_circular_dependencies(plan.get('milestones', [])):
        reward += 1.0
    if check_dependencies_exist(plan.get('milestones', [])):
        reward += 1.0
    if check_working_days_correct(plan.get('milestones', [])):
        reward += 1.0
    if check_no_impossible_timelines(plan.get('milestones', [])):
        reward += 1.0
    if check_task_owners_in_attendees(plan.get('tasks', []), scenario.get('attendees', [])):
        reward += 1.0
    
    # NEW: Tool grounding check
    if check_tool_grounding(plan, available_tools):
        reward += 1.0
    else:
        # Severe penalty for using non-existent tools
        reward -= 2.0
    
    return max(0.0, reward)  # Clip to non-negative
```

---

## Test Tenant: Mock Tool Execution

**File**: `test_tenant/api/tool_executor.py`

```python
"""
Mock tool executor for test tenant.
Simulates BizChat tool execution during training.
"""

import json
from typing import Dict, Any


class ToolExecutor:
    """Executes tools against test tenant data"""
    
    def __init__(self, test_tenant_data_path: str = "test_tenant/"):
        self.data_path = test_tenant_data_path
        
        # Load synthetic data
        with open(f"{test_tenant_data_path}/calendar/synthetic_meetings.json") as f:
            self.meetings = json.load(f)['meetings']
        
        with open(f"{test_tenant_data_path}/users/synthetic_employees.json") as f:
            self.users = json.load(f)['users']
        
        with open(f"{test_tenant_data_path}/artifacts/synthetic_documents.json") as f:
            self.documents = json.load(f)['artifacts']
    
    def execute(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call against test tenant data"""
        
        if tool_id == "graph_calendar_get_events":
            return self._get_calendar_events(parameters)
        
        elif tool_id == "graph_user_get_profile":
            return self._get_user_profile(parameters)
        
        elif tool_id == "sharepoint_search_documents":
            return self._search_documents(parameters)
        
        elif tool_id == "planner_create_task":
            return self._create_task(parameters)
        
        elif tool_id == "teams_send_message":
            return self._send_message(parameters)
        
        else:
            raise ValueError(f"Unknown tool: {tool_id}")
    
    def _get_calendar_events(self, params):
        """Mock: Get calendar events from synthetic data"""
        user_email = params['user_email']
        # Filter meetings for this user
        user_meetings = [m for m in self.meetings 
                        if user_email in [a['email'] for a in m['attendees']]]
        return {"value": user_meetings[:params.get('top', 50)]}
    
    def _get_user_profile(self, params):
        """Mock: Get user profile from synthetic data"""
        user_email = params['user_email']
        for user in self.users:
            if user['email'] == user_email:
                return {
                    "displayName": user['displayName'],
                    "mail": user['email'],
                    "jobTitle": user['jobTitle'],
                    "department": user['department']
                }
        return None
    
    def _search_documents(self, params):
        """Mock: Search documents from synthetic data"""
        query = params['query'].lower()
        results = [d for d in self.documents 
                  if query in d['name'].lower() or 
                     any(query in tag.lower() for tag in d.get('tags', []))]
        return {"value": results[:params.get('top', 10)]}
    
    def _create_task(self, params):
        """Mock: Create planner task"""
        return {
            "id": f"task_{hash(params['title']) % 10000}",
            "title": params['title'],
            "assigned_to": params.get('assigned_to'),
            "due_date": params.get('due_date'),
            "status": "not_started"
        }
    
    def _send_message(self, params):
        """Mock: Send Teams message"""
        return {
            "id": f"msg_{hash(params['message']) % 10000}",
            "channel_id": params['channel_id'],
            "sent_at": "2025-11-18T10:00:00Z"
        }
```

---

## Training Integration

### SFT: Ensure Expert Plans Use Real Tools

```python
# validate_sft_data.py - Enhanced validation

def validate_tool_grounding(plan: dict, registry: dict) -> bool:
    """Validate all tool calls reference real BizChat tools"""
    available_tools = {t['id'] for t in registry['tools']}
    
    for task in plan.get('tasks', []):
        if task.get('tool_call'):
            tool_id = task['tool_call']['tool_id']
            if tool_id not in available_tools:
                print(f"❌ Task '{task['name']}' uses non-existent tool: {tool_id}")
                return False
    
    return True

# Load tool registry
with open('test_tenant/tools/bizchat_tool_registry.json') as f:
    registry = json.load(f)

# Validate SFT data
with jsonlines.open('data/sft/qbr_training.jsonl') as f:
    for item in f:
        if not validate_tool_grounding(item['plan'], registry):
            raise ValueError(f"SFT example has invalid tool reference")
```

### PFT: Better Plans Use Tools Effectively

Preference pairs should favor plans that:
- Use tools when available (not manual workarounds)
- Chain tools properly (dependencies)
- Handle tool failures gracefully (fallbacks)

### RFT: Reward Tool Compliance

Model gets positive reward for:
- ✅ Using only tools from registry
- ✅ Providing correct parameters
- ✅ Chaining tools logically

Model gets negative reward for:
- ❌ Inventing non-existent tools
- ❌ Missing required parameters
- ❌ Ignoring available tools (doing manually when tool exists)

---

## Summary: Complete Grounding Stack

**3-Layer Grounding**:

1. **Tool Registry** - Defines what's available in production (BizChat)
2. **Training Data** - All examples use only registered tools
3. **Reward Function** - RFT penalizes hallucinated tools

**Benefits**:
- ✅ Generated plans are **executable** in production
- ✅ No user frustration from impossible actions
- ✅ Model learns tool ecosystem constraints
- ✅ Training reflects production reality

**Key Insight**: Model doesn't just learn "good planning" - it learns "good planning within BizChat's tool constraints".
