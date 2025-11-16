# Workback Planning Module

AI-powered workback planning for Scenara 2.0, adapted from Stratos-Exp.

## Overview

This module generates comprehensive project workback plans using a two-stage LLM pipeline:

1. **Analysis Stage (O1)**: Deep reasoning to break down objectives into hierarchical work breakdown structure
2. **Structuring Stage (GPT-4)**: Convert analysis into structured JSON with tasks, dependencies, participants

## Architecture

```
src/workback_planning/
├── __init__.py           # Module exports
├── models/               # Pydantic data models
│   ├── __init__.py
│   ├── artifact_reference.py  # ArtifactType, ArtifactReference
│   └── workback_plan.py       # WorkbackPlan, Task, Deliverable, Participant
├── generator/            # Plan generation (two-stage pipeline)
│   ├── __init__.py
│   └── plan_generator.py      # generate_plan() function
├── prompts/              # LLM prompt templates
│   ├── analyze.md        # O1 analysis prompt
│   ├── structure.md      # GPT-4 structuring prompt
│   └── doc_format.md     # JSON schema definition
├── evaluator/            # Quality assessment (future)
└── test_generator.py     # Integration test
```

## Installation

No additional dependencies required. Uses existing Scenara dependencies:
- `pydantic` for data models
- `tools/llm_api.py` for LLM integration (Ollama, OpenAI, Anthropic)

## Usage

### Basic Usage

```python
from src.workback_planning import generate_plan

context = """
Meeting: Product Launch Planning
Target Date: 2025-12-15
Participants: PM, Engineering Lead, Marketing
Goal: Launch new feature by target date
"""

result = generate_plan(context)

# Access analysis (markdown)
print(result['analysis'])

# Access structured plan (JSON)
print(result['structured'])
```

### Using Pydantic Models

```python
from src.workback_planning import generate_plan, WorkbackPlan

result = generate_plan(context)
workback_plan = WorkbackPlan(**result['structured'])

# Access structured data
print(f"Summary: {workback_plan.summary}")
print(f"Tasks: {len(workback_plan.tasks)}")
for task in workback_plan.tasks:
    print(f"  - {task.name}: {task.description}")
```

### Custom LLM Configuration

```python
from tools.llm_api import LLMAPIClient

client = LLMAPIClient()

# Override analysis model (O1)
analysis_override = {
    "provider": "openai",
    "model": "o1-preview",
    "temperature": 1.0
}

# Override structure model (GPT-4)
structure_override = {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.1
}

result = generate_plan(
    context,
    client=client,
    analysis_model_override=analysis_override,
    structure_model_override=structure_override
)
```

### Analysis-Only Mode

```python
# Skip structured generation (faster, cheaper)
result = generate_plan(context, generate_structured=False)
print(result['analysis'])  # Markdown analysis only
```

## Testing

Run the integration test:

```bash
python src/workback_planning/test_generator.py
```

This tests:
- Two-stage pipeline execution
- JSON output structure validation
- Pydantic model compatibility

## Data Models

### WorkbackPlan
Root document containing all plan information.

**Fields:**
- `summary`: Brief description of the plan
- `history`: List of history events
- `deliverables`: List of deliverables
- `participants`: List of participants
- `artifact_references`: List of artifact references
- `tasks`: List of tasks
- `notes`: List of notes

### Task
Represents an actionable task in the plan.

**Fields:**
- `id`: Unique identifier (e.g., "task-001")
- `name`: Short name
- `description`: Detailed description
- `participants`: List of assigned participants
- `artifacts`: List of related artifacts
- `dependencies`: List of task IDs this depends on
- `start_date`: Start date (optional)
- `due_date`: Due date hint (optional)

### Deliverable
Represents a deliverable artifact.

**Fields:**
- `id`: Unique identifier
- `name`: Deliverable name
- `description`: Description
- `due_date`: Due date hint (optional)
- `artifact`: Related artifact reference (optional)

### Participant
Represents a person involved in the project.

**Fields:**
- `name`: Full name
- `email`: Email address
- `role`: Role in the project

### ArtifactReference
Reference to an external artifact (meeting, email, document, chat).

**Fields:**
- `artifact_id`: Unique identifier
- `artifact_type`: Type (email, meeting, chat_thread, document)
- `summary`: Optional summary

## LLM Configuration

### Default Models

**Analysis Stage (O1):**
- Provider: OpenAI
- Model: `o1-preview` (will upgrade to `o1` when available)
- Temperature: 1.0

**Structuring Stage (GPT-4):**
- Provider: OpenAI
- Model: `gpt-4o` (will upgrade to `gpt-4.1` when available)
- Temperature: 0.1

### Multi-Provider Support

The module uses Scenara's `LLMAPIClient` which supports:
- **Ollama**: Local models (gpt-oss:20b, llama3, etc.)
- **OpenAI**: GPT-4, O1 models
- **Anthropic**: Claude models

## Integration with Scenara

### Phase 1: Core Adaptation ✅
- [x] Directory structure created
- [x] Data models adapted from Stratos-Exp
- [x] Prompt templates copied
- [x] LLM client integration (LLMAPIClient)
- [x] Two-stage pipeline implemented
- [ ] Integration test executed

### Phase 2: Meeting Intelligence Integration 🔄
- [ ] Connect to `meeting_intelligence.py` pipeline
- [ ] Use calendar data from `my_calendar_events_complete_attendees.json`
- [ ] Add workback planning to meeting preparation workflow
- [ ] Test with real DevBox-extracted meeting data

### Phase 3: CPM Enhancement Layer 🔮
- [ ] Integrate WorkbackPlan CPM algorithms
- [ ] Add critical path analysis
- [ ] Add resource allocation optimization
- [ ] Add risk scoring

### Phase 4: Evaluation & Quality 🔮
- [ ] Adapt O1-based evaluation from Stratos-Exp
- [ ] Integrate with GUTT v4.0 framework
- [ ] Create quality metrics dashboard

## Source Attribution

This module is adapted from [Stratos-Exp](../temp_stratos) with the following key changes:

1. **LLM Client**: Replaced `OpenAIClient` with Scenara's `LLMAPIClient` for multi-provider support
2. **Model Configs**: Updated to use available models (o1-preview, gpt-4o)
3. **Module Structure**: Reorganized for Scenara's architecture
4. **Documentation**: Enhanced with usage examples and integration guide

Original implementation credit: Stratos-Exp team

## License

Part of Scenara 2.0 project.
