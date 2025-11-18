# DevUI Testing Workflow for Workback Planning

**Author**: Chin-Yew Lin  
**Created**: November 18, 2025  
**Purpose**: Guide for using ContextFlow to capture BizChat tool usage and update tool registry

---

## Overview

We have generated test prompts based on your actual calendar meetings to capture real BizChat tool usage patterns through ContextFlow. This data will:

1. **Update Tool Registry** - Add real usage statistics (frequency, success rates, latency)
2. **Discover New Tools** - Identify tools not yet in our baseline registry
3. **Validate Training Data** - Ensure only production tools are used in training
4. **Improve Quality** - Ground training data in actual Microsoft BizChat behavior

---

## Meeting Analysis Results

### ✅ Found Examples (7/10 types)

| Meeting Type | Count | Best Example | Attendees |
|--------------|-------|--------------|-----------|
| **Quarterly Business Review (QBR)** | 7 | STCA Monthly Extended PLT + Managers | 180 |
| **Product Launch** | 28 | How-to Navigate M365 Pulse: A 101 Beginner's Guide | 374 |
| **Conference/Event Preparation** | 9 | E+D: FY26 Kickoff | 261 |
| **Executive Presentation** | 11 | STCA Monthly Extended PLT + Managers | 180 |
| **Project Kickoff** | 6 | FY26 STCA Kickoff All Hands | 61 |
| **Budget Planning** | 10 | FY26 Q1 Business Review | 118 |
| **Hiring Committee** | 1 | Virtual Interview for Senior Applied Scientist | 5 |

### ❌ Missing Examples (3/10 types)

For these types, we created synthetic prompts:

- **Board Review Meeting** - No board meetings in your calendar
- **M&A Due Diligence** - No M&A meetings
- **Team Offsite Planning** - No offsite planning meetings

---

## ContextFlow Testing Workflow

### Step 1: Prepare ContextFlow Desktop App

```bash
cd /Users/cyl/projects/scenara/ContextFlow
# Follow app README for building and running
```

**ContextFlow Features**:
- Token acquisition (MSAL/WAM authentication)
- ChatHub WebSocket connection (BizChat backend)
- Real-time tool call visualization
- Session export (JSON format with telemetry)

### Step 2: Run Test Prompts in BizChat

Open the generated prompts file:
```bash
open /Users/cyl/projects/scenara/WorkbackPlan/docs/devui_test_prompts.md
```

For each test prompt (prioritize these first):

1. **QBR Prompt** (Test Prompt #2)
   - Subject: "STCA Monthly Extended PLT + Managers"
   - High complexity, 45-day lead time
   - Expected tools: calendar, people, context, recommendations

2. **Product Launch Prompt** (Test Prompt #3)
   - Subject: "How-to Navigate M365 Pulse"
   - High complexity, 90-day lead time
   - Expected tools: calendar, people, documents, search

3. **Project Kickoff Prompt** (Test Prompt #8)
   - Medium complexity, 14-day lead time
   - Expected tools: calendar, people, work tracking

4. **Budget Planning Prompt** (Test Prompt #9)
   - Medium complexity, 30-day lead time
   - Expected tools: calendar, documents, collaboration

5. **Hiring Committee Prompt** (Test Prompt #10)
   - Low complexity, 7-day lead time
   - Expected tools: calendar, people, email

### Step 3: Capture ContextFlow Sessions

For each prompt:

1. **Start Fresh Session**
   - Open ContextFlow app
   - Authenticate with Microsoft account
   - Connect to BizChat/ChatHub

2. **Enter Test Prompt**
   - Copy prompt from `devui_test_prompts.md`
   - Paste into BizChat
   - Observe tool calls in ContextFlow UI

3. **Monitor Tool Activity**
   - Watch ToolsView panel for tool results
   - Check MessagesView for message stream
   - Note workflow steps and telemetry

4. **Export Session**
   - Save session as JSON: `session_<meeting_type>_<date>.json`
   - Example: `session_qbr_20251118.json`
   - Store in: `/Users/cyl/projects/scenara/WorkbackPlan/data/contextflow_sessions/`

### Step 4: Extract Tool Usage Data

After capturing 5-10 sessions:

```bash
cd /Users/cyl/projects/scenara/WorkbackPlan

# Process individual session
python tools/integrate_contextflow_tools.py \
  --session-file data/contextflow_sessions/session_qbr_20251118.json \
  --output-report reports/tool_usage_qbr.json

# Batch process all sessions
for session in data/contextflow_sessions/*.json; do
  python tools/integrate_contextflow_tools.py \
    --session-file "$session" \
    --update-registry
done
```

**Tool Extraction Targets**:
- Tool messages (`author: "tool"`)
- Workflow steps (`type: "tool-call"`)
- Telemetry metrics (service calls)

**Registry Updates**:
- Tool call frequency
- Success/failure rates
- Average latency
- Parameter patterns
- Error patterns

### Step 5: Validate Updated Registry

```bash
# Check updated tool registry
cat WorkbackPlan/docs/bizchat_tool_registry.json | jq '.total_tools, .tool_calls_analyzed'

# Generate usage report
python tools/integrate_contextflow_tools.py \
  --generate-report \
  --output reports/tool_usage_summary.md
```

**Validation Checklist**:
- [ ] Tool call count > 0 (was 0 before)
- [ ] At least 10-15 tools with usage data
- [ ] Success rates between 70-95%
- [ ] Latencies reasonable (<5s typical)
- [ ] New tools discovered (if any)

---

## Expected Tool Calls by Meeting Type

Based on workback planning requirements:

### QBR/Board Reviews
- `graph_calendar_get_events` - Meeting details
- `graph_get_people` - Stakeholder information
- `graph_get_manager` - Reporting chains
- `bizchat_context` - Recent activities
- `bizchat_recommendations` - Related content
- `substrate_meeting_prep` - Preparation materials

### Product Launches
- `graph_calendar_get_events` - Launch timeline
- `graph_get_people` - Cross-functional teams
- `graph_get_document` - Product specs
- `bizchat_search_documents` - Related materials
- `ado_get_work_items` - Project status

### Project Kickoffs
- `graph_calendar_get_events` - Kickoff meeting
- `graph_get_people` - Project team
- `ado_get_work_items` - Work tracking
- `bizchat_search` - Related projects

### Budget Planning
- `graph_calendar_get_events` - Planning meetings
- `graph_get_document` - Budget templates
- `bizchat_search_documents` - Historical budgets

---

## Integration with Training Pipeline

Once tool registry is updated:

### 1. Validate Training Data

```bash
cd /Users/cyl/projects/scenara/WorkbackPlan

# Check that all training examples use real tools
python tools/validate_tool_usage.py \
  --training-data data/workback_planning_examples.json \
  --tool-registry docs/bizchat_tool_registry.json
```

### 2. Update Assertions

```bash
# Regenerate assertions with real tool data
python tools/generate_assertions.py \
  --meeting-types data/meeting_types.json \
  --tool-registry docs/bizchat_tool_registry.json \
  --output data/workback_planning_assertions.json
```

### 3. Generate Training Data

```bash
# Create tool-grounded training examples
python tools/generate_training_data.py \
  --tool-registry docs/bizchat_tool_registry.json \
  --meeting-examples data/meeting_examples.json \
  --output data/pft_training_data.jsonl
```

### 4. Quality Check with GUTT v4.0

```bash
# Evaluate training data quality
python tools/evaluate_training_quality.py \
  --training-data data/pft_training_data.jsonl \
  --gutt-version 4.0 \
  --output reports/training_quality_report.json
```

---

## File Locations

### Generated Files
- **Test Prompts**: `/Users/cyl/projects/scenara/WorkbackPlan/docs/devui_test_prompts.md`
- **Analysis Report**: `/Users/cyl/projects/scenara/WorkbackPlan/docs/meeting_analysis_report.json`
- **Tool Registry**: `/Users/cyl/projects/scenara/WorkbackPlan/docs/bizchat_tool_registry.json`

### Session Data (to be created)
- **ContextFlow Sessions**: `/Users/cyl/projects/scenara/WorkbackPlan/data/contextflow_sessions/`
- **Tool Usage Reports**: `/Users/cyl/projects/scenara/WorkbackPlan/reports/`

### Scripts
- **Meeting Analysis**: `tools/analyze_meetings_generate_prompts.py`
- **ContextFlow Integration**: `tools/integrate_contextflow_tools.py`
- **Tool Extraction**: `tools/extract_bizchat_tools_from_traces.py`

---

## Troubleshooting

### ContextFlow Connection Issues
- **Problem**: Cannot connect to ChatHub
- **Solution**: Verify Microsoft account authentication, check VPN if required

### No Tool Calls Captured
- **Problem**: ContextFlow shows empty tool results
- **Solution**: Ensure BizChat is using production backend, not mock data

### Session Export Fails
- **Problem**: Cannot save session JSON
- **Solution**: Check file permissions, ensure output directory exists

### Tool Registry Not Updating
- **Problem**: `tool_calls_analyzed` still 0
- **Solution**: Verify session JSON structure matches expected format

---

## Success Metrics

After completing ContextFlow testing, you should have:

- ✅ 5-10 ContextFlow sessions captured (JSON format)
- ✅ Tool registry updated with usage statistics
- ✅ Tool call count > 0 (previously was 0)
- ✅ At least 10-15 tools with real usage data
- ✅ Discovered new tools (if any exist in BizChat)
- ✅ Training data validated against production tools
- ✅ Assertions updated with real tool patterns
- ✅ GUTT v4.0 evaluation showing high quality

---

## Next Steps

1. **Build ContextFlow App** - Follow repository README
2. **Run Priority Prompts** - Start with QBR, Product Launch, Project Kickoff
3. **Capture 5-10 Sessions** - Export as JSON
4. **Extract Tool Data** - Run `integrate_contextflow_tools.py`
5. **Validate Registry** - Check tool counts and statistics
6. **Update Training Pipeline** - Regenerate assertions and training data
7. **Evaluate Quality** - Run GUTT v4.0 evaluation

---

**Ready to proceed?** Start with building ContextFlow app and running the first test prompt (QBR).
