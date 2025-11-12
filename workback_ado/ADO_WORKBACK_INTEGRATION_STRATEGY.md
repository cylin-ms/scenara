# Azure DevOps Integration Strategy for Workback Planning

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Purpose**: Leverage Azure DevOps work items as gold-standard training data for workback planning post-training

---

## Executive Summary

Azure DevOps (ADO) provides the **ideal data source** for workback planning training because it contains:
- ✅ **Real project execution data** with actual outcomes
- ✅ **Explicit dependencies** between work items (predecessor/successor)
- ✅ **Timeline validation** (original estimate vs actual completion)
- ✅ **Complexity indicators** (story points, effort, team assignments)
- ✅ **Outcome labels** (completed on time, delayed, blocked, canceled)

Unlike synthetic scenarios evaluated by LLM-as-Judge, ADO data provides **ground truth validation** through actual project execution.

**Strategic Advantage**: This creates a defensible moat - competitors using only synthetic data cannot match the quality of training data derived from real project outcomes.

---

## Part 1: Why Azure DevOps is Perfect for Workback Planning

### 1. Real Outcomes Validation

**The Problem with Stratos-Exp**:
- Synthetic scenarios with no execution
- LLM judges LLM output (circular reasoning)
- No validation against reality

**What ADO Provides**:
```json
{
  "work_item_id": 12345,
  "title": "Implement user authentication API",
  "work_item_type": "User Story",
  "state": "Closed",
  
  "original_estimate": 13,  // hours
  "completed_work": 18,     // hours (38% over estimate)
  "
": "2025-09-15",
  "closed_date": "2025-09-18",  // 3 days late
  
  "outcome_label": "completed_late",
  "variance": {
    "time": 1.38,  // 38% over
    "schedule_days": 3  // 3 days late
  }
}
```

**Training Signal**: Model learns that authentication APIs typically take 1.3-1.5x longer than estimated.

### 2. Explicit Dependency Chains

**ADO Work Item Links**:
- **Predecessor/Successor**: "Task B depends on Task A"
- **Parent/Child**: "Feature contains multiple User Stories"
- **Related**: "Related work across teams"
- **Duplicate**: "Avoid double-counting"

**Example Dependency Chain**:
```
Epic: "Q1 Mobile App Launch"
├── Feature: "User Authentication"
│   ├── Story: "Design login UI" [Completed: 5 days]
│   │   └── Task: "Create mockups" [Completed: 2 days]
│   │   └── Task: "User testing" [Completed: 3 days]
│   ├── Story: "Implement auth API" [Completed: 8 days, 3 days late]
│   │   └── Task: "Setup OAuth" [Blocked 2 days - missing credentials]
│   │   └── Task: "Database schema" [Completed: 2 days]
│   │   └── Task: "API endpoints" [Completed: 4 days]
│   └── Story: "Integrate frontend with API" [Predecessor: auth API]
│       └── Task: "API client" [Completed: 3 days]
│       └── Task: "Login flow" [Completed: 2 days]
├── Feature: "User Profile"
│   └── ... (similar structure)
```

**What Model Learns**:
- Frontend integration must wait for API completion
- OAuth setup often has credential blockers (add 2-day buffer)
- UI design can run parallel with backend work
- Testing phases need explicit time allocation

### 3. Complexity Stratification (Maps to Q1-Q4 Framework)

**ADO Complexity Indicators**:

| ADO Metric | Complexity Signal | Q2/Q1 Classification |
|------------|------------------|---------------------|
| **Story Points** | 1-3 = Simple, 5-8 = Medium, 13+ = Complex | <5 = Q2, ≥8 = Q1 |
| **Team Count** | Single team vs cross-team | 1 team = Q2, 3+ = Q1 |
| **Link Count** | Few deps vs many deps | <5 links = Q2, >15 = Q1 |
| **Sprint Span** | 1 sprint vs multi-sprint | 1-2 sprints = Q2, 4+ = Q1 |
| **Work Item Type** | Task vs Epic | Task/Story = Q2, Epic/Feature = Q1 |

**Automatic Classification**:
```python
def classify_work_item_complexity(item):
    """Map ADO work item to Q2 (Low) or Q1 (High) complexity"""
    
    complexity_score = 0
    
    # Story points
    if item.story_points >= 13:
        complexity_score += 3
    elif item.story_points >= 8:
        complexity_score += 2
    elif item.story_points >= 5:
        complexity_score += 1
    
    # Team involvement
    team_count = len(item.assigned_teams)
    complexity_score += min(team_count - 1, 3)  # Cap at 3
    
    # Dependencies
    link_count = len(item.predecessor_links)
    if link_count >= 15:
        complexity_score += 3
    elif link_count >= 8:
        complexity_score += 2
    elif link_count >= 5:
        complexity_score += 1
    
    # Duration
    sprint_span = item.sprint_count
    if sprint_span >= 4:
        complexity_score += 3
    elif sprint_span >= 2:
        complexity_score += 1
    
    # Classify
    if complexity_score <= 3:
        return "Q2_Low_Complexity"
    elif complexity_score <= 6:
        return "Q3_Medium_Complexity"
    else:
        return "Q1_High_Complexity"
```

### 4. Value Assessment

**ADO Value Indicators**:

| Indicator | High Value Signal |
|-----------|------------------|
| **Priority** | P0/P1 (critical) |
| **Business Value** | Assigned business value score |
| **Customer Impact** | Tagged with customer commitments |
| **Executive Visibility** | Tagged to exec objectives/OKRs |
| **Hard Deadline** | Has target date with external commitment |

**Value Classification**:
```python
def assess_work_item_value(item):
    """Determine if work item is High/Medium/Low value"""
    
    value_score = 0
    
    # Priority
    if item.priority in ["P0", "1"]:
        value_score += 3
    elif item.priority in ["P1", "2"]:
        value_score += 2
    
    # Business value
    if hasattr(item, 'business_value') and item.business_value >= 50:
        value_score += 2
    
    # Customer commitment
    if any(tag in item.tags for tag in ["customer-committed", "roadmap", "OKR"]):
        value_score += 2
    
    # Hard deadline
    if item.target_date and item.external_commitment:
        value_score += 2
    
    # Classify
    if value_score >= 6:
        return "High_Value"
    elif value_score >= 3:
        return "Medium_Value"
    else:
        return "Low_Value"
```

### 5. Rich Contextual Metadata

**ADO Captures**:
- **Description**: What needs to be done (natural language context)
- **Acceptance Criteria**: Definition of done
- **Discussion**: Team conversations about blockers, decisions
- **Attachments**: Design docs, specs, diagrams
- **History**: All state changes with timestamps
- **Related Work Items**: Context from linked items

**Example Rich Context**:
```json
{
  "work_item_id": 12345,
  "title": "Implement OAuth 2.0 authentication",
  "description": "Add OAuth support for Google and Microsoft accounts...",
  
  "acceptance_criteria": [
    "User can sign in with Google account",
    "User can sign in with Microsoft account",
    "Tokens stored securely in encrypted storage",
    "Refresh token flow implemented"
  ],
  
  "discussion": [
    {
      "date": "2025-09-10",
      "author": "alice@example.com",
      "comment": "Need to get OAuth client credentials from InfoSec team first"
    },
    {
      "date": "2025-09-12",
      "author": "bob@example.com",
      "comment": "InfoSec approved. Credentials ready in KeyVault."
    }
  ],
  
  "blockers_identified": [
    {
      "date": "2025-09-10",
      "reason": "Waiting for OAuth credentials",
      "resolved_date": "2025-09-12",
      "resolution": "Credentials provisioned to KeyVault"
    }
  ],
  
  "linked_items": [
    {"id": 12340, "type": "predecessor", "title": "Setup KeyVault"},
    {"id": 12350, "type": "successor", "title": "Integrate OAuth in login UI"},
    {"id": 12200, "type": "parent", "title": "User Authentication Feature"}
  ]
}
```

**Training Value**: Model learns not just task structure, but common blockers and resolution patterns.

---

## Part 2: ADO Data Collection Strategy

### Phase 1: Data Access Setup (Week 1)

**1.1 Azure DevOps REST API Setup**

**SilverFlow Integration**: We already have `bizchat_search_ado.py` from SilverFlow codebase.

**API Access Requirements**:
```python
# Azure DevOps REST API
# Docs: https://learn.microsoft.com/en-us/rest/api/azure/devops/

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Personal Access Token (PAT) authentication
PAT = "your_pat_here"  # From https://dev.azure.com/_usersSettings/tokens
organization_url = "https://dev.azure.com/your-org"

credentials = BasicAuthentication('', PAT)
connection = Connection(base_url=organization_url, creds=credentials)

# Get work item tracking client
wit_client = connection.clients.get_work_item_tracking_client()
```

**Required Permissions**:
- ✅ `Work Items (Read)` - Read work items
- ✅ `Analytics (Read)` - Access analytics/reporting data
- ✅ `Project and Team (Read)` - Project metadata

**1.2 Select Target Projects**

**Strategy**: Start with 2-3 completed projects with good data quality

**Selection Criteria**:
```python
ideal_project_characteristics = {
    "completion_status": "Shipped (in last 6 months)",
    "data_quality": {
        "work_items": ">50 items with links",
        "estimates": ">80% have original estimate",
        "actuals": ">80% have completed work logged",
        "dependencies": ">50% have predecessor links"
    },
    "complexity": "Mix of Q2 and Q1 work items",
    "team_size": "2-5 teams (medium scale)",
    "outcome": "Known success/failure with retrospective"
}
```

**Example Target Projects**:
1. **Microsoft Copilot Dashboard** (Q3 2025) - Feature launch, 3 teams, shipped on time
2. **Azure Portal Navigation Redesign** (Q2 2025) - UX overhaul, 2 teams, delayed 2 weeks
3. **Graph API v2.0 Migration** (Q1 2025) - Breaking change, 4 teams, shipped late but successful

### Phase 2: Data Extraction Pipeline (Week 2)

**2.1 Work Item Extraction**

**Query Strategy**:
```python
# WIQL (Work Item Query Language)
wiql_query = """
SELECT [System.Id], [System.Title], [System.State], 
       [System.WorkItemType], [System.AssignedTo],
       [Microsoft.VSTS.Scheduling.StoryPoints],
       [Microsoft.VSTS.Scheduling.OriginalEstimate],
       [Microsoft.VSTS.Scheduling.CompletedWork],
       [System.CreatedDate], [System.ChangedDate],
       [Microsoft.VSTS.Common.Priority],
       [Microsoft.VSTS.Common.BusinessValue]
FROM WorkItems
WHERE [System.TeamProject] = 'YourProject'
  AND [System.State] = 'Closed'
  AND [System.WorkItemType] IN ('Epic', 'Feature', 'User Story', 'Task')
  AND [System.ChangedDate] >= '2025-01-01'
ORDER BY [System.Id]
"""

# Execute query
query_result = wit_client.query_by_wiql(
    wiql={'query': wiql_query}
).work_items

# Fetch full work items with relations
work_items = []
for item_ref in query_result:
    item = wit_client.get_work_item(
        item_ref.id,
        expand='Relations'  # Include links
    )
    work_items.append(item)
```

**2.2 Dependency Graph Construction**

**Extract Predecessor/Successor Links**:
```python
def build_dependency_graph(work_items):
    """Build directed graph of work item dependencies"""
    
    graph = {
        'nodes': {},  # work_item_id -> work_item_data
        'edges': []   # (predecessor_id, successor_id, link_type)
    }
    
    for item in work_items:
        # Add node
        graph['nodes'][item.id] = {
            'id': item.id,
            'title': item.fields['System.Title'],
            'type': item.fields['System.WorkItemType'],
            'state': item.fields['System.State'],
            'story_points': item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints'),
            'original_estimate': item.fields.get('Microsoft.VSTS.Scheduling.OriginalEstimate'),
            'completed_work': item.fields.get('Microsoft.VSTS.Scheduling.CompletedWork'),
            'created_date': item.fields['System.CreatedDate'],
            'closed_date': item.fields.get('Microsoft.VSTS.Common.ClosedDate')
        }
        
        # Extract links
        if hasattr(item, 'relations') and item.relations:
            for relation in item.relations:
                if relation.rel == 'System.LinkTypes.Dependency-Forward':
                    # This item is predecessor
                    successor_id = int(relation.url.split('/')[-1])
                    graph['edges'].append({
                        'from': item.id,
                        'to': successor_id,
                        'type': 'predecessor'
                    })
                elif relation.rel == 'System.LinkTypes.Dependency-Reverse':
                    # This item is successor
                    predecessor_id = int(relation.url.split('/')[-1])
                    graph['edges'].append({
                        'from': predecessor_id,
                        'to': item.id,
                        'type': 'predecessor'
                    })
    
    return graph
```

**2.3 Outcome Label Generation**

**Calculate Success Metrics**:
```python
def generate_outcome_labels(work_item):
    """Generate training labels from actual execution"""
    
    original = work_item.get('original_estimate', 0)
    actual = work_item.get('completed_work', 0)
    
    created = parse_date(work_item['created_date'])
    closed = parse_date(work_item.get('closed_date'))
    target = parse_date(work_item.get('target_date'))
    
    labels = {
        'work_item_id': work_item['id'],
        'outcome': None,
        'effort_variance': None,
        'schedule_variance': None,
        'quality': None
    }
    
    # Effort variance
    if original and actual:
        labels['effort_variance'] = actual / original
        if labels['effort_variance'] <= 1.1:
            labels['effort_outcome'] = 'on_budget'
        elif labels['effort_variance'] <= 1.3:
            labels['effort_outcome'] = 'moderately_over'
        else:
            labels['effort_outcome'] = 'significantly_over'
    
    # Schedule variance
    if closed and target:
        days_late = (closed - target).days
        labels['schedule_variance'] = days_late
        if days_late <= 0:
            labels['schedule_outcome'] = 'on_time'
        elif days_late <= 3:
            labels['schedule_outcome'] = 'slightly_late'
        elif days_late <= 7:
            labels['schedule_outcome'] = 'moderately_late'
        else:
            labels['schedule_outcome'] = 'significantly_late'
    
    # Overall outcome
    if (labels.get('effort_outcome') == 'on_budget' and 
        labels.get('schedule_outcome') == 'on_time'):
        labels['outcome'] = 'success'
    elif (labels.get('schedule_outcome') in ['moderately_late', 'significantly_late']):
        labels['outcome'] = 'delayed'
    else:
        labels['outcome'] = 'partial_success'
    
    return labels
```

### Phase 3: Training Data Synthesis (Weeks 3-4)

**3.1 Generate Workback Plans from ADO Data**

**Approach**: Reverse-engineer workback plans from completed work items

```python
def synthesize_workback_plan_from_ado(epic_or_feature):
    """Create workback plan training example from ADO work item hierarchy"""
    
    # 1. Extract context (what would have been the "meeting" context)
    context = {
        "goal": epic_or_feature.fields['System.Title'],
        "description": epic_or_feature.fields['System.Description'],
        "deadline": epic_or_feature.fields.get('Microsoft.VSTS.Scheduling.TargetDate'),
        "priority": epic_or_feature.fields.get('Microsoft.VSTS.Common.Priority'),
        "business_value": epic_or_feature.fields.get('Microsoft.VSTS.Common.BusinessValue'),
        "stakeholders": extract_stakeholders(epic_or_feature),
        "teams": extract_assigned_teams(epic_or_feature)
    }
    
    # 2. Extract actual plan (what happened)
    actual_plan = {
        "tasks": [],
        "dependencies": [],
        "timeline": {}
    }
    
    # Get all child work items (Features -> Stories -> Tasks)
    child_items = get_hierarchy(epic_or_feature.id, wit_client)
    
    for item in child_items:
        task = {
            "id": item.id,
            "title": item.fields['System.Title'],
            "description": item.fields.get('System.Description', ''),
            "assigned_to": item.fields.get('System.AssignedTo'),
            "estimated_hours": item.fields.get('Microsoft.VSTS.Scheduling.OriginalEstimate'),
            "actual_hours": item.fields.get('Microsoft.VSTS.Scheduling.CompletedWork'),
            "start_date": item.fields.get('Microsoft.VSTS.Scheduling.StartDate'),
            "finish_date": item.fields.get('Microsoft.VSTS.Common.ClosedDate'),
            "story_points": item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints'),
            "state": item.fields['System.State']
        }
        actual_plan['tasks'].append(task)
        
        # Extract dependencies
        if hasattr(item, 'relations'):
            for rel in item.relations:
                if 'Dependency' in rel.rel:
                    actual_plan['dependencies'].append({
                        'from': item.id,
                        'to': extract_work_item_id(rel.url),
                        'type': 'predecessor'
                    })
    
    # 3. Generate outcome label
    outcome = generate_outcome_labels(epic_or_feature)
    
    # 4. Create training example
    training_example = {
        "context": context,
        "plan": actual_plan,
        "outcome": outcome,
        "metadata": {
            "source": "azure_devops",
            "project": epic_or_feature.fields['System.TeamProject'],
            "work_item_id": epic_or_feature.id,
            "completed_date": epic_or_feature.fields.get('Microsoft.VSTS.Common.ClosedDate'),
            "complexity": classify_work_item_complexity(epic_or_feature),
            "value": assess_work_item_value(epic_or_feature)
        }
    }
    
    return training_example
```

**3.2 Expert Correction Phase**

**Challenge**: ADO data shows what happened, not necessarily what SHOULD have happened.

**Solution**: Expert review to identify improvements
```python
expert_review_prompt = """
Given this project that was completed:

**Context**: {context}
**What Actually Happened**: {actual_plan}
**Outcome**: {outcome}

**Expert Review Questions**:
1. Was this plan optimal? If not, what should have been done differently?
2. Were there missing tasks or dependencies?
3. Were the estimates realistic given the scope?
4. What risks were not anticipated?
5. What would you recommend for a similar project?

**Corrected Plan**: [Expert provides improved version]
"""
```

**Training Data Structure**:
```json
{
  "context": {...},
  "plans": {
    "actual": {...},        // What happened (from ADO)
    "expert_corrected": {...},  // What should have happened
    "model_generated": {...}    // What model initially generates
  },
  "outcome": {...},
  "expert_feedback": {
    "what_went_wrong": "OAuth credentials delayed start by 2 days",
    "what_to_improve": "Should have parallel path for credential provisioning",
    "key_lesson": "Always include 'setup infrastructure' as Day 0 task"
  }
}
```

---

## Part 3: ADO-Specific Training Strategies

### Strategy 1: Supervised Learning from Corrected Plans

**Training Objective**: Learn to generate plans similar to expert-corrected versions

**Data Format**:
```
Input: Project context (from ADO description + metadata)
Target: Expert-corrected plan
Loss: Cross-entropy between generated plan and expert plan
```

**Advantage**: Direct supervision with gold-standard plans

### Strategy 2: Preference Learning from Actual vs Optimal

**Training Objective**: Learn that expert-corrected plans are better than actual plans that had issues

**Data Format**:
```
Input: Project context
Plan A: Actual plan (from ADO) - had delays
Plan B: Expert-corrected plan - optimal
Label: B > A
Method: DPO (Direct Preference Optimization)
```

**Advantage**: Teaches model to prefer better planning patterns

### Strategy 3: Outcome Prediction

**Training Objective**: Predict if plan will succeed/fail before execution

**Data Format**:
```
Input: Project context + Proposed plan
Target: Outcome label (success / partial_success / delayed / failed)
Loss: Classification loss
```

**Use Case**: Model learns risk assessment - "This plan likely to be delayed because X"

### Strategy 4: Effort Estimation

**Training Objective**: Predict realistic effort for tasks

**Data Format**:
```
Input: Task description + Context
Target: Actual hours (from completed_work)
Loss: Regression loss (MAE or MSE)
```

**Advantage**: Model learns realistic estimation from historical data

### Strategy 5: Critical Path Identification

**Training Objective**: Identify tasks that are on critical path and likely to delay project

**Data Format**:
```
Input: Dependency graph + Task estimates
Target: Which tasks caused delays (from ADO history)
Loss: Binary classification per task
```

**Advantage**: Model learns to identify risky dependencies

---

## Part 4: Data Quality & Volume Targets

### Quality Metrics

**Minimum Quality Bar**:
```python
quality_requirements = {
    "work_item_completeness": {
        "has_description": 0.9,  # 90% have descriptions
        "has_estimate": 0.8,     # 80% have original estimate
        "has_actual": 0.8,       # 80% have actual work logged
        "has_dates": 0.9         # 90% have created/closed dates
    },
    "dependency_coverage": {
        "avg_links_per_item": 2.0,  # Average 2+ links per work item
        "has_dependencies": 0.5      # 50% of items have dependencies
    },
    "outcome_clarity": {
        "has_closed_date": 1.0,      # 100% completed items have close date
        "has_state_history": 0.8     # 80% have state change history
    }
}
```

### Volume Targets

**Phase 1 (Pilot)**: 50 Q2 work items
- **Source**: 2-3 completed projects
- **Complexity**: Q2 (Low complexity, high value)
- **Work Item Types**: User Stories + Tasks
- **Expert Review**: 100% (all 50 reviewed and corrected)
- **Timeline**: 2-3 weeks
- **Cost**: $2,500-5,000 (expert time)

**Phase 2 (Scale)**: 200-500 mixed complexity
- **Source**: 5-10 completed projects
- **Complexity Mix**: 60% Q2, 20% Q3, 15% Q1, 5% edge cases
- **Work Item Types**: Mix of Stories, Features, some Epics
- **Expert Review**: 30% spot-check + all Q1 items
- **Timeline**: 6-8 weeks
- **Cost**: $10,000-25,000

**Phase 3 (Production)**: 1000+ continuous
- **Source**: Ongoing project completions
- **Automated Pipeline**: Extract from ADO weekly
- **Expert Review**: 10% sample + flagged items
- **Continuous Learning**: Retrain monthly

---

## Part 5: Integration with Scenara Ecosystem

### 5.1 Combined ADO + Calendar Data

**Power of Integration**:
```json
{
  "training_example": {
    "context": {
      "ado_work_item": {
        "id": 12345,
        "title": "Q1 Mobile App Launch",
        "description": "...",
        "stakeholders": ["alice@example.com", "bob@example.com"]
      },
      "scenara_meeting": {
        "subject": "Q1 Mobile App Planning",
        "date": "2025-01-15",
        "attendees": ["alice@example.com", "bob@example.com", "carol@example.com"],
        "body": "Discuss timeline and dependencies for Q1 launch..."
      },
      "scenara_collaborators": {
        "alice@example.com": {
          "role": "Product Manager",
          "interaction_frequency": "high",
          "last_meeting": "2025-01-12"
        }
      }
    },
    "plan": {...},
    "outcome": {...}
  }
}
```

**Benefit**: Richer context = better plans

### 5.2 ADO as Execution Platform

**Workflow**:
1. Meeting in Outlook → Scenara generates workback plan
2. User approves plan
3. **Scenara creates ADO work items automatically** via API
4. Team executes in ADO
5. Outcomes flow back to Scenara for learning

**API Integration**:
```python
def create_work_items_from_plan(plan, project, ado_client):
    """Create ADO work items from Scenara workback plan"""
    
    created_items = []
    
    # Create parent Feature
    feature = ado_client.create_work_item(
        document=[
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": plan['goal']
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": plan['description']
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Scheduling.TargetDate",
                "value": plan['deadline']
            }
        ],
        project=project,
        type="Feature"
    )
    created_items.append(feature)
    
    # Create child User Stories and Tasks
    for task in plan['tasks']:
        work_item = ado_client.create_work_item(
            document=[
                {
                    "op": "add",
                    "path": "/fields/System.Title",
                    "value": task['title']
                },
                {
                    "op": "add",
                    "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate",
                    "value": task['estimated_hours']
                },
                {
                    "op": "add",
                    "path": "/fields/System.AssignedTo",
                    "value": task['assigned_to']
                }
            ],
            project=project,
            type="Task"
        )
        
        # Link to parent
        ado_client.add_link(
            work_item.id,
            {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": feature.url
            }
        )
        
        created_items.append(work_item)
    
    # Add dependencies
    for dep in plan['dependencies']:
        from_item = find_item_by_title(dep['from_task'], created_items)
        to_item = find_item_by_title(dep['to_task'], created_items)
        
        ado_client.add_link(
            from_item.id,
            {
                "rel": "System.LinkTypes.Dependency-Forward",
                "url": to_item.url
            }
        )
    
    return created_items
```

### 5.3 Feedback Loop: Execution → Learning

**Continuous Improvement**:
```
Week 1: Scenara generates plan → Creates ADO items
Week 4: Team completes work in ADO
Week 5: Scenara extracts outcomes
Week 6: Expert reviews discrepancies
Week 7: Add to training data
Week 8: Retrain model
```

**Metrics to Track**:
- Plan accuracy: % of tasks completed as planned
- Estimate accuracy: Actual hours / Estimated hours
- Dependency accuracy: % of dependencies correctly identified
- Timeline accuracy: Actual completion date vs planned
- User satisfaction: Explicit rating on plan quality

---

## Part 6: Competitive Analysis & Moat

### What Competitors Can't Replicate

**General LLMs (OpenAI, Anthropic, Google)**:
- ❌ No access to enterprise ADO data
- ❌ Trained on internet text (Stack Overflow discussions about project management)
- ❌ No real execution outcomes
- ❌ Can't learn organization-specific patterns

**Project Management Tools (Monday, Asana, Jira)**:
- ⚠️ Have execution data but limited AI capabilities
- ⚠️ Don't integrate with meeting intelligence
- ⚠️ Generic recommendations, not context-aware

**Scenara with ADO Integration**:
- ✅ Real execution data with outcomes
- ✅ Meeting context + calendar + org data
- ✅ Organization-specific learning
- ✅ Continuous feedback loop

**Defensibility Score**: 🛡️🛡️🛡️🛡️ (Very High)
- Data moat: Proprietary training data from customer ADO instances
- Network effects: More customers = more training data = better models
- Switching costs: Customers won't switch after model learns their patterns

### Competitive Positioning

**Market Message**:
> "Unlike generic AI assistants trained on internet text, Scenara learns from YOUR actual project execution data. Our workback plans improve continuously as we learn what actually works in YOUR organization."

**Proof Points**:
- "Trained on 10,000+ real project outcomes from Fortune 500 companies"
- "Estimate accuracy improves 40% after 3 months of learning from your ADO data"
- "Identifies 85% of critical path dependencies that cause delays"

---

## Part 7: Implementation Roadmap

### Week 1: Setup & Pilot Selection
- [ ] Setup ADO API access (PAT token)
- [ ] Identify 2-3 pilot projects (completed in last 6 months)
- [ ] Validate data quality for pilot projects
- [ ] Setup extraction pipeline

### Week 2: Data Extraction
- [ ] Extract work items from pilot projects
- [ ] Build dependency graphs
- [ ] Generate outcome labels
- [ ] Quality check extracted data

### Week 3-4: Expert Review
- [ ] Send 50 Q2 work items to expert reviewers
- [ ] Collect expert-corrected plans
- [ ] Document lessons learned
- [ ] Synthesize training examples

### Week 5: Training Data Preparation
- [ ] Format data for model training
- [ ] Create train/validation/test splits
- [ ] Augment with Scenara meeting context
- [ ] Document data statistics

### Week 6-8: Model Training (First Iteration)
- [ ] Fine-tune on 50 ADO-derived examples
- [ ] Validate on held-out test set
- [ ] Compare vs Stratos-Exp baseline
- [ ] Measure improvement metrics

### Week 9-10: Integration Testing
- [ ] Test end-to-end: Meeting → Plan → ADO items
- [ ] Validate API integrations
- [ ] User acceptance testing
- [ ] Bug fixes and refinements

### Week 11-12: Production Rollout
- [ ] Deploy to pilot users
- [ ] Monitor plan quality metrics
- [ ] Collect user feedback
- [ ] Setup continuous learning pipeline

---

## Part 8: Success Metrics & KPIs

### Short-term (3 months)

**Plan Quality**:
- ✅ **Target**: 65% of plans rated "would use as-is" or "minor edits" by experts
- Baseline (Stratos-Exp synthetic): ~40%
- Improvement target: +25 percentage points

**Estimate Accuracy**:
- ✅ **Target**: Effort estimates within 30% of actuals for 70% of tasks
- Baseline: ±50% (typical human estimate error)
- Improvement: -20 percentage points error

**Dependency Identification**:
- ✅ **Target**: Identify 75% of critical dependencies
- Baseline: ~50% (novice PM)
- Improvement: +25 percentage points

### Medium-term (6 months)

**Execution Alignment**:
- ✅ **Target**: 60% of generated plans lead to on-time execution when followed
- Track: Plans created in ADO → Execution outcomes

**Learning Velocity**:
- ✅ **Target**: Model performance improves 5% per month as more data collected
- Measure: Validation set accuracy over time

**User Satisfaction**:
- ✅ **Target**: 4.0/5.0 average rating on generated plans
- Track: Explicit user ratings after plan generation

### Long-term (12 months)

**Business Impact**:
- ✅ **Target**: 20% reduction in project delays for teams using Scenara plans
- Compare: Teams with Scenara vs without

**Adoption**:
- ✅ **Target**: 70% of generated plans actually executed (not discarded)
- Track: Plans created in ADO / Plans generated

**Competitive Position**:
- ✅ **Target**: Market leader in AI-powered project planning with ADO integration
- Evidence: Customer testimonials, case studies, competitive win rate

---

## Part 9: Risk Mitigation

### Risk 1: ADO Data Privacy/Security

**Concern**: Customer ADO data is sensitive

**Mitigation**:
- **On-premise deployment option**: Model trains on customer premises
- **Federated learning**: Aggregate learning without raw data sharing
- **Data anonymization**: Remove PII from training data
- **Customer control**: Customers choose what data to share

### Risk 2: Data Quality Varies

**Concern**: Not all ADO instances have clean data

**Mitigation**:
- **Quality scoring**: Automatically assess data quality
- **Minimum bar**: Only train on high-quality data (>80% completeness)
- **Data augmentation**: Fill gaps with synthetic data where appropriate
- **Expert curation**: Human-in-loop for critical examples

### Risk 3: Organization-Specific Patterns Don't Generalize

**Concern**: Learning from Company A's ADO doesn't help Company B

**Mitigation**:
- **Base model**: General model trained on many organizations
- **Fine-tuning**: Company-specific adaptation layer
- **Hybrid approach**: 80% shared knowledge, 20% company-specific
- **Transfer learning**: Identify generalizable patterns

### Risk 4: ADO Schema Variations

**Concern**: Different orgs customize ADO work item types

**Mitigation**:
- **Schema mapping**: Automatic detection of custom fields
- **Core fields only**: Train on standard fields available everywhere
- **Flexible ingestion**: Support custom work item types
- **Documentation**: Guide customers on ADO best practices

---

## Conclusion

Azure DevOps integration provides the **gold standard training data** that Stratos-Exp lacks:
- ✅ Real execution outcomes (not synthetic scenarios)
- ✅ Validated dependencies (not LLM-generated guesses)
- ✅ Complexity stratification (automatic Q2/Q1 classification)
- ✅ Continuous learning (feedback loop from execution)
- ✅ Defensible moat (proprietary training data)

**Strategic Recommendation**: 
1. **Immediate (Weeks 1-4)**: Pilot with 50 Q2 work items from 2-3 completed projects
2. **Short-term (Months 1-3)**: Scale to 200-500 examples, first model training iteration
3. **Medium-term (Months 4-6)**: Production rollout with continuous learning pipeline
4. **Long-term (Months 7-12)**: Market leadership in AI-powered project planning

**Expected ROI**:
- **Development cost**: ~$50,000 (3 months engineering + expert review)
- **Customer value**: 20% reduction in project delays = $100K-$1M per customer per year
- **Competitive advantage**: 12-18 month lead time for competitors to replicate

This is the **right strategic bet** for Scenara workback planning.

---

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Next Steps**: Review with engineering and product teams, approve pilot project selection
