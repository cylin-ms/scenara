# ContextFlow Integration Guide

**Author**: Chin-Yew Lin  
**Date**: November 18, 2025  
**Purpose**: Extract real BizChat tool usage from ContextFlow desktop app to build production tool registry

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  TOOL EXTRACTION PIPELINE                        │
└─────────────────────────────────────────────────────────────────┘

Step 1: Capture                Step 2: Extract               Step 3: Train
┌──────────────┐              ┌──────────────┐             ┌──────────────┐
│ CONTEXTFLOW  │              │   SCRIPTS    │             │   TRAINING   │
│  Desktop App │  session.json│              │registry.json│              │
│              │─────────────►│ integrate_   │────────────►│ Tool-Grounded│
│ • ChatHub WS │              │ contextflow_ │             │ Plan Gen     │
│ • Telemetry  │              │ tools.py     │             │              │
│ • Tool calls │              │              │             │ • Validate   │
│ • Messages   │              │ extract_     │             │   tools      │
│ • Prompts    │              │ bizchat_     │             │ • RFT reward │
└──────────────┘              │ tools_...py  │             │ • SFT/PFT    │
                              └──────────────┘             └──────────────┘
```

---

## What is ContextFlow?

**ContextFlow** is a **Microsoft internal developer tool** for debugging BizChat:

### Technology Stack
- **Frontend**: TypeScript + React (Vite)
- **Backend**: Rust (Tauri 2.0)
- **Purpose**: Inspect BizChat internal context flow

### Key Capabilities
1. **Token Acquisition**: MSAL/WAM broker (Windows)
2. **ChatHub WebSocket**: Stream Sydney/Copilot conversations
3. **Telemetry Processing**: Capture metrics, messages, workflow steps
4. **Tool Inspection**: View tool calls, results, parameters
5. **Prompt Analysis**: Template vs rendered output diff

### Repository
- **Location**: `/Users/cyl/projects/scenara/ContextFlow/`
- **Source**: https://github.com/gim-home/ContextFlow.git
- **Components**:
  * `src/components/ToolsView.tsx` - Tool results visualization
  * `src/components/MessagesView.tsx` - Message stream viewer
  * `src/services/chatTelemetryProcessor.ts` - Session processing
  * `src-tauri/src/lib.rs` - Native backend (token, WebSocket)

---

## Usage Workflow

### Step 1: Run ContextFlow Desktop App

```bash
cd /Users/cyl/projects/scenara/ContextFlow

# Install dependencies
npm install

# Run in development mode
npm run tauri:dev

# Or build portable version
npm run build:portable
```

**What to do in the app:**
1. Authenticate with your Microsoft account (Windows WAM)
2. Start a BizChat conversation
3. Ask BizChat to perform tasks that use tools:
   - "Show my calendar for next week"
   - "Search for meetings about QBR"
   - "Get my recent emails from Alice"
   - "Find documents about project planning"
4. Watch tools being invoked in real-time
5. Export session data

### Step 2: Export Session Data

**Option A: Manual Export** (from ContextFlow UI)
- Click "Export Session" button
- Save to: `/Users/cyl/projects/scenara/ContextFlow/sessions/session_YYYYMMDD_HHMMSS.json`

**Option B: Access Internal State**
ContextFlow stores sessions in `CopilotSession` objects with this structure:

```typescript
interface CopilotSession {
  id: string;                    // "session_xxx"
  conversationId: string;        // "conv_xxx"
  messages: ChatHubMessage[];    // All messages including tool results
  workflowTrace: {
    steps: WorkflowStep[]        // Including type='tool-call' steps
  };
  telemetry?: {
    metrics: TelemetryMetric[]   // Service calls with latency
  };
}
```

**Typical export location**: Look for session state in:
- ContextFlow app data directory
- Browser DevTools → Application → Local Storage
- Export functionality in the UI (if implemented)

### Step 3: Extract Tool Calls

```bash
cd /Users/cyl/projects/scenara/WorkbackPlan

# Process single session
python tools/integrate_contextflow_tools.py \
  --session-file /path/to/session.json \
  --registry docs/bizchat_tool_registry.json \
  --report docs/tool_usage_report.json

# Process multiple sessions
python tools/integrate_contextflow_tools.py \
  --session-dir /Users/cyl/projects/scenara/ContextFlow/sessions/ \
  --registry docs/bizchat_tool_registry.json \
  --report docs/tool_usage_report.json
```

**What it does:**
1. Parses ContextFlow session JSON
2. Extracts tool calls from:
   - Messages with `author: "tool"`
   - Workflow steps with `type: "tool-call"`
   - Telemetry metrics (service calls)
3. Updates tool registry with:
   - Usage frequency
   - Success rates
   - Average latency
   - Real parameters observed
4. Generates usage report

### Step 4: Review & Validate

```bash
# View updated registry
cat docs/bizchat_tool_registry.json | python -m json.tool | head -50

# View usage report
cat docs/tool_usage_report.json | python -m json.tool
```

**Check for:**
- ✅ Tool frequencies match your expectations
- ✅ Success rates are high (>90%)
- ✅ New tools discovered (add definitions)
- ✅ Parameter schemas captured correctly

---

## Tool Data Extraction Patterns

### Pattern 1: Tool Messages (Direct Results)

**Source**: `messages` array where `author: "tool"`

**Example**:
```json
{
  "author": "tool",
  "messageType": "Tool",
  "content": "{
    \"results\": [
      {
        \"result\": {
          \"type\": \"Event\",
          \"reference_id\": \"evt_001\",
          \"title\": \"Q4 Planning\",
          \"snippet\": \"...\",
          ...
        }
      }
    ]
  }",
  "timestamp": "2025-11-18T12:00:00Z"
}
```

**Extraction**: `result.type` → `graph_calendar_get_events`

### Pattern 2: Workflow Steps (Tool Invocations)

**Source**: `workflowTrace.steps` where `type: "tool-call"`

**Example**:
```json
{
  "id": "step_12345",
  "type": "tool-call",
  "timestamp": "2025-11-18T12:00:00Z",
  "data": {
    "tool_name": "Get Calendar Events",
    "parameters": {
      "start_date": "2025-11-18",
      "end_date": "2025-11-25"
    }
  },
  "duration": 234,
  "status": "completed"
}
```

**Extraction**: `data.tool_name` → `graph_calendar_get_events`

### Pattern 3: Telemetry Metrics (Service Calls)

**Source**: `telemetry.metrics` array

**Example**:
```json
{
  "id": "metric_67890",
  "serviceName": "DeepLeoImprovedNetworking",
  "path": "/api/v1/calendar/events",
  "input": "{...}",
  "output": "{...}",
  "latencyMilliseconds": 234,
  "status": "success"
}
```

**Extraction**: `serviceName` + `path` → tool mapping

---

## Integration with Training Pipeline

### Current State

**Before ContextFlow**:
```json
{
  "tool_id": "graph_calendar_get_events",
  "tool_name": "Get Calendar Events",
  "frequency": 0,          // ❌ No usage data
  "reliability": "low",    // ❌ No success rate
  "parameters": []         // ❌ No real schemas
}
```

**After ContextFlow**:
```json
{
  "tool_id": "graph_calendar_get_events",
  "tool_name": "Get Calendar Events",
  "frequency": 47,         // ✅ Real usage count
  "reliability": "high",   // ✅ 97.9% success rate
  "avg_latency_ms": 234.5, // ✅ Performance data
  "parameters": [          // ✅ Observed schemas
    {
      "name": "start_date",
      "type": "string",
      "required": true,
      "example": "2025-11-18T00:00:00Z"
    },
    {
      "name": "end_date",
      "type": "string",
      "required": true
    }
  ]
}
```

### Training Data Validation

With real tool usage data, you can now:

1. **Validate SFT Plans**: Ensure expert plans only use real tools
2. **Generate PFT Pairs**: Prefer plans using high-reliability tools
3. **Calculate RFT Rewards**: Penalize plans using low-reliability or non-existent tools
4. **Update Prompts**: Include real tool examples in training prompts

**Example RFT Reward Update**:
```python
def calculate_reward(plan: Dict, tool_registry: Dict) -> float:
    reward = 0.0
    tools_by_id = {t['tool_id']: t for t in tool_registry['tools']}
    
    for task in plan['tasks']:
        if task.get('tool_call'):
            tool_id = task['tool_call']['tool_id']
            
            # Check tool exists
            if tool_id not in tools_by_id:
                reward -= 2.0  # ❌ Hallucinated tool
                continue
            
            tool = tools_by_id[tool_id]
            
            # Reward based on reliability
            if tool['frequency'] > 0:  # ✅ Real usage data from ContextFlow
                if tool['reliability'] == 'high':
                    reward += 1.0
                elif tool['reliability'] == 'medium':
                    reward += 0.5
                # Low reliability: no reward
    
    return reward
```

---

## Troubleshooting

### Issue: ContextFlow app won't start

**Solution**:
1. Check you're on Windows (MSAL/WAM is Windows-only)
2. Ensure Rust and Node.js are installed
3. Run `npm install` and `cargo check`

### Issue: No sessions exported

**Solution**:
1. Check if export feature is implemented in your ContextFlow version
2. Look for session data in app state:
   - DevTools → Application → Local Storage
   - Check `CopilotSession` state in React DevTools
3. Manually construct session JSON from UI data

### Issue: Tool extraction finds no tools

**Solution**:
1. Verify session JSON structure matches expected format
2. Check if tool messages have `author: "tool"`
3. Look for workflow steps with `type: "tool-call"`
4. Enable verbose logging in extraction script

### Issue: New tools discovered but not defined

**Solution**:
1. Review `tool_usage_report.json` for new tool IDs
2. Add tool definitions to registry manually:
   ```json
   {
     "tool_id": "new_tool_id",
     "tool_name": "New Tool Name",
     "description": "What it does",
     "category": "Calendar & Scheduling",
     "parameters": [],
     "returns": "What it returns",
     "cost": "low",
     "reliability": "high"
   }
   ```
3. Re-run extraction to update statistics

---

## Files Created

1. **`integrate_contextflow_tools.py`** (418 lines)
   - Main integration script
   - Processes ContextFlow sessions
   - Updates tool registry with usage data

2. **`extract_bizchat_tools_from_traces.py`** (665 lines)
   - Baseline tool extractor
   - Works with any BizChat conversation JSON
   - Fallback if ContextFlow not available

3. **`bizchat_tool_registry.json`** (Updated)
   - Current: 24 tools, 0 calls analyzed
   - After ContextFlow: Real usage statistics

4. **`tool_usage_report.json`** (New)
   - Top tools by frequency
   - Usage by category
   - Success rates and latencies

---

## Next Steps

1. **Run ContextFlow**: Capture real BizChat sessions
2. **Export Sessions**: Save to JSON format
3. **Extract Tools**: Run integration script
4. **Update Training Docs**: Incorporate real tool data into `TOOL_GROUNDED_TRAINING.md`
5. **Validate Plans**: Ensure all training examples use real tools
6. **Generate Training Data**: Create SFT/PFT/RFT datasets with validated tools

**Goal**: Production-ready tool registry backed by real usage data for tool-grounded plan generation training! 🎯
