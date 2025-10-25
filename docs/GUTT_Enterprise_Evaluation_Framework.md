# GUTT-Enterprise Meeting Intelligence Evaluation Framework

*Based on Microsoft's Unit Task Benchmarking Framework and Enterprise Meeting Taxonomy*

**Contact**: Chin-Yew Lin

## Framework Overview

This evaluation framework combines two official Microsoft methodologies:

1. **Unit Task Benchmarking Framework (GUTT)** - Modular evaluation through atomic task decomposition
2. **Enterprise Meeting Taxonomy** - Comprehensive classification of business meeting types

The framework provides scalable, interpretable, human-aligned evaluation of AI meeting intelligence systems through:

- **Meeting Type Classification** using the 5-category enterprise taxonomy
- **Unit Task Decomposition** breaking complex prompts into atomic GUTTs
- **Context-Aware Scoring** with meeting-type-specific rubrics
- **Modular Performance Tracking** at unit, task, and compound levels

## Enterprise Meeting Taxonomy Integration

### Primary Meeting Categories

1. **Internal Recurring Meetings (Cadence)**
   - Team Status Updates, Progress Reviews, One-on-Ones
   - Action Reviews, Governance & Strategy Cadence

2. **Strategic Planning & Decision Meetings** 
   - Planning Sessions, Decision-Making, Problem-Solving
   - Brainstorming/Innovation, Workshops & Design Sessions

3. **External & Client-Facing Meetings**
   - Sales & Client, Vendor/Supplier, Partnership/BD
   - Interviews & Recruiting, Client Training/Onboarding

4. **Informational & Broadcast Meetings**
   - All-Hands/Town Halls, Informational Briefings
   - Training & Education, Webinars & Broadcasts

5. **Team-Building & Culture Meetings**
   - Team-Building Activities, Recognition & Social Events
   - Communities of Practice & Networking

## GUTT Template Library

### Resource Management (GUTT.1-6)
- **GUTT.1**: Identify where [resource] is spent
- **GUTT.2**: Identify reclaimable [resource] from [source]  
- **GUTT.3**: Align [resource] usage with [goal]
- **GUTT.4**: Commit only to [entity] that match [criteria]
- **GUTT.5**: Track all [entity] that meet [criteria]
- **GUTT.6**: Flag [entity] needing [action/resource]

### Planning & Scheduling (GUTT.7-8, 13)
- **GUTT.7**: Create [timeframe] plan for [goal/project]
- **GUTT.8**: Balance [plan/schedule] with [priorities]
- **GUTT.13**: Schedule time to [action] for [entity]

### Analysis & Diagnosis (GUTT.9-10)
- **GUTT.9**: Ask probing questions to uncover [cause/issue]
- **GUTT.10**: Diagnose why [goal] is not achieved

### Information Retrieval (GUTT.11-12, 14-19)
- **GUTT.11**: Find [entity] with [attribute]
- **GUTT.12**: Notify when [entity] becomes [state]
- **GUTT.14**: Identify [project/team/person] from context
- **GUTT.15**: Track status of [project/task] from [source]
- **GUTT.16**: Create agenda to [goal] using [context]
- **GUTT.17**: Find content of [artifact] for [event]
- **GUTT.18**: Identify incomplete parts of [artifact] and owners
- **GUTT.19**: Send reminder to [person] to complete [task]

### Content Generation (GUTT.20-25)
- **GUTT.20**: Summarize [materials] into [N] key points
- **GUTT.21**: Generate possible [objections/risks] for [context]
- **GUTT.22**: Generate responses to [objections/risks]
- **GUTT.23**: Prepare brief for [meeting/person]
- **GUTT.24**: Create dossier for [person] with [interest/topics]
- **GUTT.25**: Provide background on [organization/topic]

## Meeting-Type-Specific Rubric Dimensions

### For Strategic Planning & Decision Meetings
- **Grounding** (0-3): Factual accuracy and data alignment
- **Understanding** (0-3): Context comprehension and stakeholder needs
- **Trust** (0-3): Reliability and confidence in recommendations
- **Transparency** (0-3): Clear rationale and decision criteria
- **Coverage** (0-3): Completeness of planning elements
- **Actionability** (0-3): Concrete next steps and ownership

### For External & Client-Facing Meetings
- **Grounding** (0-3): Client-specific data accuracy
- **Understanding** (0-3): Client context and relationship dynamics
- **Trust** (0-3): Professional credibility and reliability
- **Transparency** (0-3): Clear communication of value and process
- **Relevance** (0-3): Alignment with client interests and goals
- **Professionalism** (0-3): Appropriate tone and presentation

### For Internal Recurring Meetings (Cadence)
- **Grounding** (0-3): Current status accuracy and metrics
- **Understanding** (0-3): Team dynamics and project context
- **Trust** (0-3): Consistent and reliable updates
- **Transparency** (0-3): Clear progress and blockers communication
- **Efficiency** (0-3): Concise and focused content
- **Continuity** (0-3): Connection to previous meetings and goals

### For Informational & Broadcast Meetings
- **Grounding** (0-3): Information accuracy and currency
- **Understanding** (0-3): Audience needs and comprehension level
- **Trust** (0-3): Authoritative and credible content
- **Transparency** (0-3): Clear messaging and expectations
- **Clarity** (0-3): Accessible and understandable presentation
- **Engagement** (0-3): Compelling and attention-holding content

### For Team-Building & Culture Meetings
- **Understanding** (0-3): Team dynamics and individual needs
- **Trust** (0-3): Safe and inclusive environment creation
- **Transparency** (0-3): Clear objectives and expectations
- **Engagement** (0-3): Interactive and participatory content
- **Inclusivity** (0-3): Consideration of diverse perspectives
- **Cultural Alignment** (0-3): Consistency with organizational values

## Scoring Methodology

### 1. Meeting Classification
- **Primary Type**: Single dominant meeting category
- **Secondary Types**: Additional relevant categories (multi-label)
- **Confidence Score**: Classification certainty (0-1)

### 2. Unit Task Decomposition
- Break compound prompt into atomic Unit Tasks
- Map each UT to appropriate GUTT template
- Identify UT dependencies and relationships

### 3. Per-UT Scoring
- **Binary Success**: 1 = success, 0 = failure
- **Rubric-Based**: 0-3 scale across relevant dimensions
- **Evidence Citation**: Specific examples supporting scores

### 4. Per-Task Aggregation
- Aggregate scores for each GUTT across all instances
- Calculate mean, median, and distribution
- Identify systematic strengths/weaknesses

### 5. Compound Prompt Scoring
- **Simple Average**: Sum of UT scores / Number of UTs
- **Weighted Average**: Critical UTs weighted higher
- **Failure Tolerance**: Partial credit for complex scenarios

### 6. Meeting-Type Performance
- Aggregate scores by meeting category
- Compare performance across different meeting contexts
- Identify meeting-specific optimization opportunities

## Evaluation Workflow

### Step 1: System Interaction Context
- **User Prompt**: Original request
- **System Response**: AI-generated output
- **Interaction Metadata**: Timing, iterations, user feedback

### Step 2: Meeting Classification
- Apply Enterprise Meeting Taxonomy
- Identify primary and secondary meeting types
- Select appropriate rubric dimensions

### Step 3: Unit Task Decomposition
- Parse compound prompt into atomic tasks
- Map to GUTT templates
- Validate completeness and dependencies

### Step 4: Evidence-Based Scoring
- Score each UT against rubric dimensions
- Cite specific evidence from system response
- Document reasoning and context

### Step 5: Performance Aggregation
- Calculate per-UT, per-task, and compound scores
- Generate meeting-type-specific insights
- Identify improvement opportunities

### Step 6: Actionable Recommendations
- Map weaknesses to specific feature teams
- Prioritize improvements by impact and feasibility
- Provide concrete enhancement suggestions

## Quality Assurance

### Inter-Rater Reliability
- Multiple evaluators score same interactions
- Calculate Cohen's kappa for consistency
- Calibrate rubric understanding across team

### Validation Methods
- **Face Validity**: Framework alignment with real-world needs
- **Construct Validity**: GUTT templates cover intended capabilities
- **Criterion Validity**: Correlation with user satisfaction metrics

### Continuous Improvement
- Regular framework updates based on usage patterns
- New GUTT templates for emerging capabilities
- Meeting taxonomy expansion for evolving business needs

## Implementation Considerations

### Tool Integration
- Calendar and scheduling system APIs
- Meeting transcript and content analysis
- Performance dashboard and reporting

### Privacy and Security
- Anonymization of sensitive meeting content
- Access controls for evaluation data
- Compliance with enterprise policies

### Scalability
- Automated GUTT template matching
- Batch processing for large datasets
- Incremental learning from evaluation feedback

This framework provides a comprehensive, standardized approach to evaluating AI meeting intelligence systems while maintaining flexibility for different organizational contexts and meeting types.