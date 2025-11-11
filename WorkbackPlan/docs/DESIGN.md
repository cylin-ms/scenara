# WorkbackPlan Design Document

**Version**: 1.0  
**Date**: November 11, 2025  
**Status**: Draft

---

## Architecture Overview

WorkbackPlan uses a layered architecture designed for extensibility and AI integration:

```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│  (CLI, API, Web UI - Future)           │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│        Application Layer                │
│  (WorkbackPlanner, ProjectManager)     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Core Engine Layer               │
│  (Scheduling, Dependencies, AI)        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Integration & Data Layer           │
│  (Graph API, Storage, Export)          │
└─────────────────────────────────────────┘
```

## Core Data Models

### Project
```python
class Project(BaseModel):
    """Represents a complete project with timeline"""
    id: str
    name: str
    target_date: datetime
    start_date: Optional[datetime]
    description: str
    owner: str
    milestones: List[Milestone]
    tasks: List[Task]
    dependencies: List[Dependency]
    team_members: List[TeamMember]
    status: ProjectStatus
```

### Milestone
```python
class Milestone(BaseModel):
    """Major project checkpoint"""
    id: str
    name: str
    target_date: datetime
    description: str
    deliverables: List[str]
    owner: str
    dependencies: List[str]  # IDs of other milestones
    tasks: List[str]  # IDs of tasks required
```

### Task
```python
class Task(BaseModel):
    """Individual work item"""
    id: str
    name: str
    description: str
    estimated_duration_hours: float
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    owner: str
    dependencies: List[str]  # Task IDs
    milestone_id: str
    status: TaskStatus
    priority: Priority
```

### Dependency
```python
class Dependency(BaseModel):
    """Task/milestone dependency"""
    from_id: str  # Prerequisite task/milestone
    to_id: str    # Dependent task/milestone
    dependency_type: DependencyType  # FINISH_TO_START, START_TO_START, etc.
    lag_days: int  # Buffer between tasks
```

## Workback Algorithm

### Core Concept
Start from the target date and work backwards, scheduling tasks in reverse dependency order:

```
Target Date (Dec 31)
    ↑
Milestone 3 (Dec 15) - 2 weeks before target
    ↑
Milestone 2 (Dec 1) - 2 weeks before M3
    ↑
Milestone 1 (Nov 15) - 2 weeks before M2
    ↑
Start Date (Nov 11) - Calculated
```

### Algorithm Steps

1. **Parse Project Definition**
   - Extract milestones, tasks, dependencies
   - Build dependency graph
   - Identify critical path

2. **Calculate Critical Path**
   - Find longest path from start to target
   - Identify tasks that cannot be delayed
   - Calculate total project duration

3. **Schedule Backwards**
   - Start from target date
   - For each milestone (reverse order):
     - Calculate required completion date
     - Schedule dependent tasks
     - Add risk buffers
     - Assign to team members

4. **Optimize & Adjust**
   - Balance team capacity
   - Parallelize independent tasks
   - Add contingency time
   - Validate feasibility

5. **Generate Output**
   - Create timeline visualization
   - Export to calendar/project management
   - Generate task assignments

## AI Integration Points

### 1. Task Decomposition
**Input**: High-level milestone description  
**AI Model**: GPT-5 or Ollama  
**Output**: Detailed task breakdown with estimates

```python
def decompose_milestone(milestone: Milestone) -> List[Task]:
    """Use LLM to break down milestone into tasks"""
    prompt = f"""
    Break down this project milestone into detailed tasks:
    
    Milestone: {milestone.name}
    Description: {milestone.description}
    Target Date: {milestone.target_date}
    
    Generate 5-10 specific, actionable tasks with:
    - Task name
    - Description
    - Estimated duration (hours)
    - Dependencies
    - Priority
    """
    # Call LLM and parse response
```

### 2. Duration Estimation
**Input**: Task description + historical data  
**AI Model**: ML regression or LLM  
**Output**: Realistic time estimate with confidence interval

### 3. Risk Analysis
**Input**: Project timeline + dependencies  
**AI Model**: GPT-5 with Chain-of-Thought  
**Output**: Risk assessment + mitigation strategies

### 4. Resource Optimization
**Input**: Team capacity + task requirements  
**AI Model**: Constraint satisfaction solver  
**Output**: Optimal task assignments

## Integration Strategy

### Phase 1: Microsoft Calendar
- Export milestones as calendar events
- Block focus time for critical tasks
- Send meeting invites for checkpoints

### Phase 2: Microsoft Planner/To Do
- Create Planner plans for projects
- Sync tasks bidirectionally
- Track completion status

### Phase 3: Microsoft Teams
- Automated status updates in channels
- Milestone reminders
- Risk alerts

## Risk Buffer Calculation

Use historical variance data to calculate appropriate buffers:

```python
def calculate_buffer(task: Task, confidence_level: float = 0.8) -> float:
    """
    Calculate time buffer based on task characteristics
    
    Args:
        task: Task to calculate buffer for
        confidence_level: Desired confidence (0.8 = 80% confident)
    
    Returns:
        Additional hours to add as buffer
    """
    base_estimate = task.estimated_duration_hours
    
    # Complexity multiplier
    complexity_factor = get_complexity_factor(task)
    
    # Dependency risk (more dependencies = more risk)
    dependency_factor = 1 + (0.1 * len(task.dependencies))
    
    # Team experience factor
    experience_factor = get_team_experience(task.owner)
    
    buffer = base_estimate * complexity_factor * dependency_factor * experience_factor
    
    return buffer * (1 - confidence_level)  # Higher confidence = less buffer needed
```

## Critical Path Analysis

Use standard CPM (Critical Path Method):

1. **Forward Pass**: Calculate earliest start/finish times
2. **Backward Pass**: Calculate latest start/finish times
3. **Slack Calculation**: Identify float for each task
4. **Critical Path**: Tasks with zero slack

```python
def find_critical_path(project: Project) -> List[Task]:
    """Identify critical path using CPM"""
    # Build adjacency graph
    graph = build_dependency_graph(project.tasks)
    
    # Forward pass: Calculate early start/finish
    for task in topological_sort(graph):
        task.early_start = max(pred.early_finish for pred in task.predecessors)
        task.early_finish = task.early_start + task.duration
    
    # Backward pass: Calculate late start/finish
    for task in reversed(topological_sort(graph)):
        task.late_finish = min(succ.late_start for succ in task.successors)
        task.late_start = task.late_finish - task.duration
    
    # Identify critical tasks (zero slack)
    critical = [task for task in project.tasks if task.slack == 0]
    
    return critical
```

## Export Formats

### 1. iCalendar (.ics)
- Milestones as events
- Tasks as to-dos
- Dependencies as notes

### 2. Microsoft Project XML
- Full project structure
- Resource assignments
- Dependency relationships

### 3. Markdown Report
- Human-readable timeline
- Risk analysis
- Team assignments

### 4. JSON API
- Structured data for integrations
- RESTful endpoints
- Webhook support

## Performance Considerations

- **In-Memory Graphs**: Use NetworkX for dependency analysis
- **Caching**: Cache LLM responses for similar tasks
- **Batch Processing**: Schedule multiple projects in parallel
- **Incremental Updates**: Only recalculate affected paths on changes

## Security & Privacy

- **Authentication**: OAuth 2.0 for Microsoft integration
- **Data Storage**: Encrypt sensitive project data
- **Access Control**: Role-based permissions
- **Audit Trail**: Log all schedule changes

## Testing Strategy

- **Unit Tests**: Individual components (scheduling, dependencies)
- **Integration Tests**: End-to-end workflow
- **AI Tests**: LLM output validation and consistency
- **Performance Tests**: Large project scalability

---

**Next Implementation Steps**:
1. Implement core data models (Pydantic)
2. Build dependency graph construction
3. Implement workback scheduling algorithm
4. Add simple CLI interface
5. Test with sample projects
