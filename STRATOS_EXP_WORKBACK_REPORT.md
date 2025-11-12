# Stratos-Exp Workback Implementation Report

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Source**: `temp_stratos/experiments/workback_model/`  
**Repository**: https://github.com/gim-home/stratos-exp.git

---

## Executive Summary

The Stratos-Exp workback planning implementation is a **two-stage LLM pipeline** that generates hierarchical work breakdown structures (WBS) from natural language meeting contexts. It uses **OpenAI O1 for deep reasoning** and **GPT-4.1 for structured output generation**, making it ideally suited for integration with Scenara 2.0's AI-first meeting intelligence architecture.

**Key Characteristics**:
- Natural language input (meetings, documents, chat threads)
- O1 reasoning with 100K token context window
- Rich artifact referencing system
- Built-in evaluation and optimization framework
- Part of "Time Berry" calendar/time management platform

---

## Architecture Overview

### Two-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Deep Reasoning & Analysis                         │
│ Model: OpenAI O1 (reasoning_effort="high")                 │
│ Max Tokens: 100,000                                         │
├─────────────────────────────────────────────────────────────┤
│ INPUT:                                                       │
│ • User context (natural language)                           │
│ • Artifact references (meetings, docs, chats)              │
│ • Priority information                                      │
│                                                             │
│ PROMPT: analyze.md                                          │
│ • Identify outcomes and deliverables                        │
│ • Provide reasoning for each outcome                        │
│ • Describe approach and alternatives                        │
│ • Create hierarchical work breakdown (1-4 levels)          │
│ • Capture dependencies explicitly                           │
│                                                             │
│ OUTPUT: Markdown analysis with detailed WBS                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: Structured Output Generation                      │
│ Model: GPT-4.1 (temperature=0.1)                           │
│ Max Tokens: 30,000                                          │
├─────────────────────────────────────────────────────────────┤
│ INPUT:                                                       │
│ • Analysis markdown from Stage 1                            │
│ • JSON schema (doc_format.md)                              │
│                                                             │
│ PROMPT: structure.md                                        │
│ • Convert markdown to JSON                                  │
│ • Follow exact schema format                                │
│ • Preserve all analysis details                             │
│ • Create proper references (@ref, @deliverable)            │
│                                                             │
│ OUTPUT: Structured JSON workback plan document             │
└─────────────────────────────────────────────────────────────┘
```

### Why Two Stages?

**Stage 1 (O1 Analysis)**: 
- Leverages O1's advanced reasoning for complex planning
- High reasoning effort for thorough analysis
- Large context window (100K tokens) handles extensive meeting/document context
- Produces human-readable analysis

**Stage 2 (GPT-4.1 Structuring)**:
- Lower temperature (0.1) for consistent JSON output
- Follows strict schema compliance
- Fast and cost-effective for conversion task
- Deterministic structured output

---

## Code Structure

### File Organization

```
temp_stratos/experiments/workback_model/default/
├── main.py                           # Entry point & orchestration
├── resources/
│   └── priority0.json               # Sample input data
└── (references to parent directories)

temp_stratos/assistant/components/workback/
├── generate/
│   ├── generate_plan.py             # Top-level API
│   └── v1/
│       ├── generate_plan.py         # Core pipeline implementation
│       ├── analyze.md               # Stage 1 prompt template
│       └── structure.md             # Stage 2 prompt template
├── evaluate/
│   └── v1/
│       └── evaluate_plan.py         # O1-based quality evaluation
├── common/
│   ├── resources.py                 # Resource utilities
│   └── doc_format.md                # JSON schema definition
└── scrape/
    └── workback_chat_blueprint.py   # Flask API endpoint
```

### Key Components

#### 1. Main Entry Point (`main.py`)

```python
def process(i):
    """Generate workback plan from priority input"""
    tools = None  # Optional: GetArtifactTool for context retrieval
    
    # Generate plan (two-stage pipeline)
    result = generate_plan_v1(load_priority(i), tools=tools)
    
    # Extract outputs
    analysis = result['analysis']      # Markdown WBS
    structured = result['structured']  # JSON document
    
    # Save artifacts
    analysis_resource.write(analysis)
    json_resource.write(structured)
    
    # Generate visualization
    html = generate_gantt_html(generate_gantt_from_workback_plan(structured))
    html_resource.write(html)

def evaluate(i):
    """Evaluate plan quality with O1"""
    evaluation = evaluate_plan_v1(
        json.dumps(load_priority(i)),
        analysis_resource.get(),
        model_override={"model": "o1", "reasoning_effort": "high"}
    )
    
def optimize(i):
    """Optimize prompts based on issues"""
    optimization = optimize_prompt(
        original_prompt,
        input_data,
        analysis_output,
        known_issues
    )
```

**Workflow Modes**:
- `process`: Generate workback plan
- `evaluate`: Quality assessment with O1
- `optimize`: Prompt improvement pipeline
- `aggregate`: Multi-run evaluation aggregation

#### 2. Core Pipeline (`assistant/components/workback/generate/v1/generate_plan.py`)

```python
def generate_plan_v1(
    priority,                              # Input context
    tools: list[ToolBase] | None = None,  # Optional context tools
    client: LlmClient | None = None,       # LLM client
    analysis_model_override: dict | None = None,
    structure_model_override: dict | None = None,
    generate_structured: bool = True
) -> dict:
    """
    Generate workback plan using two-stage LLM pipeline.
    
    Returns:
        {
            'analysis': str,      # Markdown WBS
            'structured': dict    # JSON document
        }
    """
    
    client = client or OpenAIClient()
    
    # Stage 1: Deep reasoning analysis
    analysis = _generate_analysis(priority, client, tools, analysis_model_override)
    
    # Stage 2: Structured output
    if generate_structured:
        structured = _generate_structured(analysis, client, tools, structure_model_override)
    else:
        structured = None
    
    return {'analysis': analysis, 'structured': structured}
```

**Default Model Configuration**:
```python
_analysis_model = {
    "model": "o1",
    "reasoning_effort": "high",
    "max_completion_tokens": 100000
}

_structure_model = {
    "model": "gpt-4.1",
    "temperature": 0.1,
    "max_completion_tokens": 30000
}
```

#### 3. Analysis Generation (`_generate_analysis`)

```python
def _generate_analysis(priority, client: LlmClient, tools, model_override) -> str:
    """Stage 1: O1-powered deep analysis"""
    
    model = model_override or _analysis_model
    
    # Load prompt template
    prompt = Template(_get_analyze_prompt_v1())
    prompt = prompt.substitute(context=priority)
    
    # Call O1 with optional tools
    request = create_request(model, prompt)
    messages = timing.measure_time(
        "analysis llm",
        call_chat_completion_with_tools,
        client,
        request,
        tools
    )
    
    return messages[-1]['content']
```

**Tool Support**: Optional `GetArtifactTool` for retrieving meeting/document content during analysis.

#### 4. Structured Generation (`_generate_structured`)

```python
def _generate_structured(analysis: str, client: LlmClient, tools, model_override) -> dict:
    """Stage 2: GPT-4.1 JSON structuring"""
    
    model = model_override or _structure_model
    
    # Load structure prompt with schema
    structure_prompt = Template(_get_structure_prompt_v1())
    structure_prompt = structure_prompt.substitute(
        docformat=get_workback_doc_format(),  # JSON schema
        analysis=analysis                      # Stage 1 output
    )
    
    # Call GPT-4.1 for structured output
    request = create_request(model, structure_prompt)
    messages = timing.measure_time(
        "structured llm",
        call_chat_completion_with_tools,
        client,
        request,
        tools
    )
    
    structured = messages[-1]['content']
    return json.loads(structured)
```

---

## Prompt Engineering

### Stage 1: Analysis Prompt (`analyze.md`)

**Purpose**: Guide O1 to create detailed work breakdown structure

**Key Sections**:

1. **General Guidance**:
   - Do NOT solve the problem, advise on breaking it down
   - Rely only on provided context (no external knowledge)
   - Include only relevant artifacts
   - Do NOT assume specific technologies or tools
   - Use exact artifact reference format: `@[Title](artifact_type=<id>)`

2. **Outcomes Section**:
   - Identify future deliverables
   - Retain original wording
   - Cite supporting artifacts
   - For each outcome:
     - **Reasoning**: How identified, what evidence
     - **Approach**: Detailed step-by-step approach
     - Consider alternatives and risks

3. **Breakdown Section**:
   - Hierarchical WBS (1-4 levels depth)
   - Clear numbering/indentation
   - Explicit dependencies ("Depends on: step X")
   - Self-contained, actionable steps
   - Avoid overly prescriptive language

**Output Format**:
```markdown
# Outcomes

## <Outcome name>
<Brief description>
Artifact references: @[Artifact Title](artifact_type=<artifact_id>)

### Reasoning
<Reasoning for Outcome>

### Approach
<Description of Approach for Outcome>

## Breakdown
<Hierarchical WBS with dependencies>
```

### Stage 2: Structure Prompt (`structure.md`)

**Purpose**: Convert markdown analysis to strict JSON schema

**Rules**:
- Use only given information (no assumptions)
- Output JSON only (no preamble/postamble)
- Handle subsections as dependent tasks
  - Example: `1.1` depends on `1`, `1.2` depends on `1.1` and `1`

**Input Variables**:
- `${docformat}`: Complete JSON schema from `doc_format.md`
- `${analysis}`: Markdown WBS from Stage 1

---

## Data Model (JSON Schema)

### Document Structure

```json
{
  "id": "document-001",
  "name": "Plan Name",
  "details": "Detailed description",
  "draft": false,
  "participants": [...],
  "references": [...],
  "deliverables": [...],
  "tasks": [...],
  "history": [...]
}
```

### Standard Fields

**All Entities**:
- `id`: Unique immutable ID (format: `<entity-type>-XXX`)
- `name`: Short user-friendly name
- `details`: Detailed freeform textual description
- `draft`: Boolean indicating if currently being edited
- `history`: Array of historical entries (immutable, system-managed)

### Entity Types

#### 1. Participant

Represents a person involved in the plan.

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "details": "Engineering Lead for backend services",
  "draft": false
}
```

**Special Keywords**:
- `"you"`: Current user (implicit participant)
- `"system"`: System/automation (implicit participant)

#### 2. Reference

External artifacts referenced in the plan.

```json
{
  "name": "Time Expression Requirements.docx",
  "type": "word",  // email|chat|event|meeting|word|excel|powerpoint
  "id": "SPO@72f988bf-86f1-41af-91ab-2d7cd011db47...",
  "history": [],
  "draft": false
}
```

**Reference Format**: `@ref[<type>]/<id>`  
Example: `@ref[meeting]/19:meeting_YzQxNTNi...`

#### 3. Deliverable

Output artifacts to be created.

```json
{
  "name": "API Documentation",
  "type": "word",  // word|excel|powerpoint|code|design|...
  "id": "deliverable-001",
  "draft": true,
  "history": []
}
```

**Reference Format**: `@deliverable[<type>]/<id>`  
Example: `@deliverable[code]/deliverable-001`

#### 4. Task

Actionable work items with dependencies and assignments.

```json
{
  "id": "task-001",
  "name": "Review Requirements Document",
  "draft": true,
  "details": "Analyze the document to understand time constraints and edge cases",
  "dependencies": [],               // Array of task IDs this depends on
  "co-dependencies": [],            // Tasks that must run in parallel
  "state": "not-started",           // not-started|started|completed|abandoned|blocked
  "due-by": "2025-12-01T00:00:00Z", // Optional deadline
  "assignees": ["you", "alice@example.com"],
  "deliverables": ["@deliverable[word]/deliverable-001"],
  "references": ["@ref[word]/SPO@72f988bf..."],
  "history": []
}
```

**Task States**:
- `not-started`: Initial state
- `started`: Work in progress
- `completed`: Successfully finished
- `abandoned`: No longer relevant
- `blocked`: Waiting on external factors

#### 5. History

Immutable log entries from external systems.

```json
{
  "date": "2025-11-10T15:30:00Z",
  "details": "Task marked as completed by Alice Johnson"
}
```

**Note**: History entries are **read-only** and managed by external systems.

### Example Complete Document

```json
{
  "id": "document-001",
  "name": "Calendar Scheduling Enhancement",
  "details": "Focus on refining time expressions and scheduling",
  "draft": false,
  "participants": [
    {
      "name": "Santhosh Paramesh",
      "email": "santhosh@microsoft.com",
      "details": "Lead engineer for time parsing",
      "draft": false
    },
    {
      "name": "Jothi Neelamegam",
      "email": "jothi@microsoft.com",
      "details": "PM for scheduling features",
      "draft": false
    }
  ],
  "references": [
    {
      "name": "Time Expression Requirements.docx",
      "type": "word",
      "id": "SPO@72f988bf-86f1-41af-91ab-2d7cd011db47",
      "draft": false
    },
    {
      "name": "Stratos Standup",
      "type": "meeting",
      "id": "19:meeting_YzQxNTNiNGMt...",
      "draft": false
    }
  ],
  "deliverables": [
    {
      "name": "Time Expression Parser Module",
      "type": "code",
      "id": "deliverable-001",
      "draft": true
    },
    {
      "name": "API Documentation",
      "type": "word",
      "id": "deliverable-002",
      "draft": true
    }
  ],
  "tasks": [
    {
      "id": "task-001",
      "name": "Review Time Expression Requirements",
      "details": "Analyze requirements document for time constraints",
      "dependencies": [],
      "state": "not-started",
      "assignees": ["you"],
      "references": ["@ref[word]/SPO@72f988bf-86f1-41af-91ab-2d7cd011db47"],
      "draft": true
    },
    {
      "id": "task-002",
      "name": "Design Parser Architecture",
      "details": "Create high-level design for NL to calendar action translation",
      "dependencies": ["task-001"],
      "state": "not-started",
      "assignees": ["you", "santhosh@microsoft.com"],
      "deliverables": ["@deliverable[code]/deliverable-001"],
      "references": ["@ref[meeting]/19:meeting_YzQxNTNiNGMt..."],
      "draft": true
    },
    {
      "id": "task-003",
      "name": "Implement Core Parser",
      "details": "Build the main parsing logic with edge case handling",
      "dependencies": ["task-002"],
      "co-dependencies": ["task-004"],
      "state": "not-started",
      "due-by": "2025-12-15T00:00:00Z",
      "assignees": ["santhosh@microsoft.com"],
      "deliverables": ["@deliverable[code]/deliverable-001"],
      "draft": true
    },
    {
      "id": "task-004",
      "name": "Write API Documentation",
      "details": "Document parser API for integration teams",
      "dependencies": ["task-002"],
      "co-dependencies": ["task-003"],
      "state": "not-started",
      "assignees": ["jothi@microsoft.com"],
      "deliverables": ["@deliverable[word]/deliverable-002"],
      "draft": true
    }
  ],
  "history": []
}
```

---

## Input Format

### Priority Context Structure

The input to `generate_plan_v1` is a priority context object:

```json
{
  "name": "Project/Initiative Name",
  "summary": "Brief description of the priority and context",
  "artifact_refs": [
    {
      "artifact_type": "document|meeting|chat_thread",
      "artifact_id": "Unique identifier (SPO@... for SharePoint, 19:meeting_... for Teams)",
      "title": "Human-readable title",
      "explanation": "Why this artifact is relevant"
    }
  ]
}
```

### Example Input (`priority0.json`)

```json
{
  "name": "Calendar Scheduling & Time Expression Enhancement",
  "summary": "Focus on refining time expressions and scheduling by redesigning the system to translate natural language time constraints into robust calendar actions. Discussions include multi-turn dialogue improvements in Sydney, and architectural integration with meeting skills.",
  "artifact_refs": [
    {
      "artifact_type": "document",
      "artifact_id": "SPO@72f988bf-86f1-41af-91ab-2d7cd011db47,2UtmX5l7_...",
      "title": "Time Expression Requirements.docx",
      "explanation": "Document detailing requirements and design choices for capturing rich time constraints in scheduling scenarios."
    },
    {
      "artifact_type": "meeting",
      "artifact_id": "19:meeting_YzQxNTNiNGMtYTBjNS00ZGU4LTgxOGUtZGIwMTQ4ZTY0MTAw@thread.v2",
      "title": "Stratos Standup",
      "explanation": "Recurring standup meeting addressing deployment challenges, priorities CRUD development, and workback plan generation strategies."
    },
    {
      "artifact_type": "chat_thread",
      "artifact_id": "19:0627ef7118c44e94990438a093c14b63@thread.v2",
      "title": "Time Understanding & Fine-Tuning Strategy Discussion",
      "explanation": "Discussion on integrating time expressions with fine tuning to enhance the system's scheduling and reasoning capabilities."
    }
  ]
}
```

**Artifact Types Supported**:
- `document`: SharePoint documents (Word, Excel, PowerPoint)
- `meeting`: Teams meetings (past or scheduled)
- `chat_thread`: Teams chat conversations
- `email`: Outlook emails (not in example but schema supports)

---

## Tool Support

### GetArtifactTool

Optional tool for retrieving artifact content during analysis.

```python
class GetArtifactTool(ToolBase):
    def __init__(self, services: ContextServices):
        self._services = services
    
    def get_description(self) -> dict:
        return {
            "name": "get_artifact",
            "description": "Get an artifact by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "artifact_id": {
                        "description": "The ID of the artifact to retrieve",
                        "type": "string"
                    }
                },
                "required": ["artifact_id"]
            }
        }
    
    def execute(self, args: dict) -> Any:
        artifact_id = args.get("artifact_id")
        
        if artifact_id.startswith("SPO@"):
            # SharePoint document
            doc = self._services.data_store.get_document_by_id(artifact_id)
            return doc.model_dump_json()
        else:
            # Teams chat thread
            return self._services.data_store.get_chat_thread(artifact_id).model_dump_json()
```

**Usage**: Allows O1 to fetch and analyze actual artifact content during planning.

---

## Evaluation Framework

### Quality Evaluation (`evaluate_plan_v1`)

Uses O1 with high reasoning to assess plan quality.

```python
def evaluate_plan_v1(
    context: str,          # Original priority input
    analysis: str,         # Generated markdown WBS
    model_override: dict = None
) -> str:
    """
    Evaluate workback plan quality using O1 reasoning.
    
    Returns markdown evaluation report.
    """
    
    model = model_override or {
        "model": "o1",
        "reasoning_effort": "high",
        "max_completion_tokens": 100000
    }
    
    # Evaluation prompt assesses:
    # - Completeness of task breakdown
    # - Appropriateness of dependencies
    # - Realism of approach
    # - Clarity of reasoning
    # - Coverage of risks and alternatives
    
    evaluation = evaluate_with_llm(context, analysis, model)
    return evaluation
```

### Claim Extraction (`_extract_claims_v2`)

Extracts verifiable claims from analysis for validation.

```python
def _extract_claims_v2(context: str, analysis: str) -> str:
    """
    Extract specific claims that can be verified.
    
    Returns markdown list of claims with references.
    """
    
    # Identifies:
    # - Factual statements about artifacts
    # - Assumptions about people/roles
    # - Technical claims about approaches
    # - Timeline/dependency assertions
    
    claims = extract_claims_with_llm(context, analysis)
    return claims
```

### Prompt Optimization (`optimize_prompt`)

Iterative improvement of analysis prompt.

```python
def optimize_prompt(
    original_prompt: str,
    input_data: str,
    output_analysis: str,
    known_issues: str = None
) -> dict:
    """
    Suggest improvements to analysis prompt based on results.
    
    Returns:
        {
            'improved': str,    # Improved prompt version
            'notes': str        # Explanation of changes
        }
    """
    
    # Analyzes:
    # - Where analysis fell short
    # - What additional guidance needed
    # - How to improve output quality
    
    optimization = optimize_with_llm(
        original_prompt,
        input_data,
        output_analysis,
        known_issues
    )
    
    return optimization
```

### Evaluation Aggregation

Multi-run evaluation analysis:

```python
def aggregate(i):
    """Aggregate evaluations from multiple runs"""
    
    # Collect evaluation files from multiple experiment runs
    evaluation_files = find_all_evaluations(run_dirs, priority_index=i)
    
    # Load all evaluation markdown
    evaluations = [read_file(f) for f in evaluation_files]
    
    # Generate aggregate report
    aggregate_report = aggregate_evaluations(evaluations)
    
    # Save aggregate analysis
    save_aggregate_report(aggregate_report)
```

---

## Integration Points

### Context Services

```python
def get_context_services() -> ContextServices:
    """Create context services for artifact storage"""
    
    storage_path = os.path.join(env.common_resources_path, "stores")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path, exist_ok=True)
    
    return ContextServices.create_for_local(storage_path, use_local=True)
```

**Services Provided**:
- `data_store`: ChromaDB for document/chat storage
- Vector search for relevant context
- Artifact ID resolution

### Resource Management

```python
# Experiment resources (input data)
experiment_resource = ExperimentResource('priority0.json', ResourceKind.JSON)
priority_data = experiment_resource.get()

# Run resources (outputs)
analysis_resource = RunResource(f'analysis_{i}.md', ResourceKind.TEXT)
json_resource = RunResource(f'plan_{i}.json', ResourceKind.JSON)
html_resource = RunResource(f'workback_plan_{i}.html', ResourceKind.TEXT)

# Write outputs
analysis_resource.write(analysis)
json_resource.write(structured)
html_resource.write(html)
```

**Resource Types**:
- `ExperimentResource`: Input data for experiments
- `RunResource`: Output artifacts from runs
- Automatic directory management and versioning

### Visualization

```python
# Generate Gantt chart from workback plan
gantt_data = generate_gantt_from_workback_plan(structured_json)
html = generate_gantt_html_with_size(gantt_data)
```

Converts structured JSON to interactive Gantt chart visualization.

---

## Execution Modes

### Command-Line Interface

```bash
# Basic: Generate plan for priority index 0
python main.py --priority 0

# With specific run ID
python main.py --runid 42 --priority 0

# Evaluate generated plan
python main.py --priority 0 --evaluate

# Optimize prompt based on issues
python main.py --priority 0 --optimize

# Aggregate multi-run evaluations
python main.py --priority 0 --aggregate
```

### Default Mode (No Flags)

```python
if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()
    env.initialize(runid=args.runid)
    
    if args.optimize:
        optimize(args.priority)
    elif args.evaluate:
        evaluate(args.priority)
    elif args.aggregate:
        aggregate(args.priority)
    else:
        # Default: process then evaluate
        process(args.priority)
        evaluate(args.priority)
```

**Default Workflow**:
1. Generate workback plan (two-stage pipeline)
2. Save analysis (markdown) and structured (JSON) outputs
3. Generate Gantt visualization (HTML)
4. Evaluate plan quality with O1
5. Save evaluation report

---

## Performance Characteristics

### Token Usage

**Stage 1 (O1 Analysis)**:
- Input: ~2-5K tokens (priority context + prompt)
- Output: ~5-15K tokens (markdown WBS)
- Max: 100K tokens (configurable)
- Cost: High (O1 reasoning tokens expensive)

**Stage 2 (GPT-4.1 Structuring)**:
- Input: ~10-20K tokens (analysis + schema)
- Output: ~5-10K tokens (JSON document)
- Max: 30K tokens
- Cost: Moderate (GPT-4.1 more economical)

**Total Per Plan**: ~20-50K tokens

### Execution Time

**Typical Runtime** (measured with `timing.measure_time`):
- O1 Analysis: 30-120 seconds (depends on reasoning complexity)
- GPT-4.1 Structuring: 10-30 seconds
- Total: 40-150 seconds per plan

**Optimization Opportunities**:
- Cache frequently accessed artifacts
- Parallel processing for multiple priorities
- Selective O1 usage (use GPT-4 for simpler plans)

---

## Strengths & Advantages

### 1. Natural Language Input
- No manual task definition required
- Works directly from meeting context
- Understands implicit information from artifacts

### 2. Deep Reasoning
- O1's 100K context handles complex scenarios
- High reasoning effort for thorough analysis
- Considers alternatives and edge cases

### 3. Rich Artifact References
- Links to actual meetings, documents, chats
- Bidirectional traceability
- Context-aware planning

### 4. Enterprise Features
- Email-based participant management
- State tracking and history
- Draft mode for iterative refinement
- Explicit dependency modeling

### 5. Evaluation Built-In
- O1-based quality assessment
- Claim extraction for validation
- Prompt optimization pipeline
- Multi-run aggregation

### 6. Extensibility
- Tool support for runtime context retrieval
- Pluggable LLM clients
- Model override capability
- Resource management abstraction

---

## Limitations & Challenges

### 1. LLM Dependency
- **Hallucination Risk**: O1 may invent non-existent dependencies or tasks
- **Consistency**: Multiple runs may produce different breakdowns
- **Cost**: O1 reasoning tokens are expensive at scale

**Mitigation**:
- Claim extraction and verification
- Evaluation framework catches quality issues
- Consider GPT-4 for simpler cases

### 2. No Mathematical Scheduling
- **Missing**: Critical path calculation
- **Missing**: Slack time analysis
- **Missing**: Timeline optimization
- **Focus**: Planning and breakdown, not scheduling mathematics

**Mitigation**:
- Can be enhanced with CPM layer (from my WorkbackPlan)
- Duration estimation via LLM
- Timeline validation as separate step

### 3. Schema Rigidity
- JSON schema tightly coupled to Time Berry use case
- `draft` mode assumption (not all workflows need this)
- History tracking requires external system integration

**Adaptation Required**:
- Simplify schema for Scenara use cases
- Make some fields optional
- Adapt to Scenara's artifact types

### 4. Context Service Dependency
- Requires ChromaDB setup
- Artifact storage infrastructure needed
- Not self-contained

**Adaptation Required**:
- Use Scenara's existing data infrastructure
- Direct Microsoft Graph API integration
- Simpler artifact resolution

---

## Integration Recommendations for Scenara 2.0

### High Priority Adaptations

**1. LLM Client Abstraction**
```python
# Replace this:
from assistant.llm import OpenAIClient
client = OpenAIClient()

# With this:
from tools.llm_api import LLMAPIClient
client = LLMAPIClient()

# Adapt calls:
response = client.query_llm(
    prompt=prompt,
    provider="openai",  # or "ollama", "azure", "anthropic"
    model="o1-preview",
    reasoning_effort="high",
    max_tokens=100000
)
```

**2. Artifact Reference System**
```python
# Adapt artifact IDs to Scenara format:
# Meeting: calendar event ID from my_calendar_events_complete_attendees.json
# Document: SharePoint ID (already compatible)
# Chat: Teams chat thread ID (already compatible)

def resolve_artifact(artifact_id: str) -> dict:
    """Resolve artifact ID to content using Scenara infrastructure"""
    if artifact_id.startswith("calendar-"):
        return get_calendar_event(artifact_id)
    elif artifact_id.startswith("SPO@"):
        return get_sharepoint_document(artifact_id)
    elif artifact_id.startswith("19:"):
        return get_teams_chat(artifact_id)
```

**3. Simplified Schema**
```python
# Remove draft mode if not needed
# Make history optional (add later)
# Focus on core: participants, references, deliverables, tasks

SCENARA_SCHEMA = {
    "id": str,
    "name": str,
    "details": str,
    "participants": List[Participant],
    "references": List[Reference],
    "tasks": List[Task]
    # Optional: deliverables, history
}
```

**4. Meeting Context Extraction**
```python
def extract_workback_context(meeting_data: dict) -> dict:
    """Convert Scenara meeting data to workback context"""
    return {
        "name": meeting_data['subject'],
        "summary": f"Meeting on {meeting_data['start']} with {len(meeting_data['attendees'])} participants",
        "artifact_refs": [
            {
                "artifact_type": "meeting",
                "artifact_id": meeting_data['id'],
                "title": meeting_data['subject'],
                "explanation": meeting_data.get('body', 'Meeting context')
            }
        ]
    }
```

### Medium Priority Enhancements

**5. CPM Enhancement Layer** (from my WorkbackPlan)
```python
def generate_enhanced_workback_plan(context: dict) -> dict:
    # Stage 1-2: Use stratos-exp pipeline
    result = generate_plan_v1(context)
    
    # Stage 3: Add CPM analysis if durations available
    if has_duration_estimates(result['structured']):
        cpm_result = calculate_critical_path(result['structured'])
        result['critical_path'] = cpm_result['critical_path']
        result['timeline'] = cpm_result['timeline']
    
    return result
```

**6. Duration Estimation**
```python
def estimate_task_durations(tasks: List[dict]) -> List[dict]:
    """Use LLM to estimate task durations"""
    for task in tasks:
        prompt = f"Estimate hours needed for: {task['name']}\nDetails: {task['details']}"
        duration = llm_client.query_llm(prompt, model="gpt-4")
        task['estimated_hours'] = parse_duration(duration)
    return tasks
```

### Low Priority (Future)

**7. Real-time Collaboration**
- Draft mode for iterative planning
- Multi-user concurrent editing
- Version control and history tracking

**8. Advanced Visualization**
- Interactive Gantt charts
- Dependency graphs
- Resource allocation views

---

## Comparison with My CPM Implementation

| Aspect | Stratos-Exp | My WorkbackPlan |
|--------|-------------|-----------------|
| **Input Method** | Natural language context | Python objects (manual) |
| **Planning Approach** | LLM reasoning (O1) | Mathematical (CPM algorithm) |
| **Strengths** | Easy to use, rich context | Deterministic, rigorous |
| **Weaknesses** | No math, LLM cost | Manual input barrier |
| **Scheduling** | Conceptual breakdown | Timeline calculation |
| **Dependencies** | Implicit (LLM inferred) | Explicit (typed) |
| **Critical Path** | Not computed | Computed via graph |
| **Artifacts** | Rich references | Not supported |
| **Best For** | Initial planning | Timeline validation |

**Recommendation**: Use stratos-exp for planning, enhance with CPM for scheduling.

---

## Next Steps for Integration

### Immediate (Week 1)
1. Copy core files to `src/workback_planning/`
2. Adapt `generate_plan_v1` to use `LLMAPIClient`
3. Test with sample meeting context
4. Verify JSON output structure

### Short-term (Week 2-4)
5. Integrate with `meeting_intelligence.py`
6. Connect to calendar data
7. Test with DevBox-extracted meetings
8. Add Gantt visualization

### Medium-term (Week 5-8)
9. Add CPM enhancement layer
10. Implement duration estimation
11. Integrate with GUTT v4.0 evaluation
12. Deploy in meeting preparation pipeline

---

## Conclusion

The Stratos-Exp workback implementation provides a **production-ready, LLM-powered planning system** that is ideally suited for integration with Scenara 2.0's meeting intelligence platform. Its natural language input, rich artifact referencing, and O1-powered reasoning make it superior to traditional manual planning approaches for meeting-centric workflows.

**Key Value Proposition**:
- Transforms meeting context into actionable work plans automatically
- Leverages existing Microsoft 365 artifacts (meetings, documents, chats)
- Provides enterprise features (participants, history, state tracking)
- Includes evaluation framework for quality assurance

**Integration Path**: Adopt as primary planning engine, optionally enhance with CPM algorithms from my WorkbackPlan for mathematical scheduling validation.

---

**Author**: Chin-Yew Lin  
**Report Date**: November 11, 2025  
**Source Code**: `temp_stratos/experiments/workback_model/`  
**Related Documents**: 
- `WORKBACK_COMPARISON.md` - Detailed comparison analysis
- `WORKBACK_SUMMARY.md` - Integration summary and roadmap
- `.cursorrules` - Current task tracking
