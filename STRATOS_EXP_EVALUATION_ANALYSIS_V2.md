# Why Workback Planning Is Challenging for Post-Training: A Critical Analysis

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Version**: 2.0  
**Focus**: Post-Training Data Requirements and Stratos-Exp Limitations

---

## Executive Summary

This document analyzes why **workback planning is particularly difficult for LLM post-training** and why **Stratos-Exp's proxy evaluation approach is insufficient** for creating effective training data. The fundamental challenge is that workback planning requires **causal reasoning, counterfactual analysis, and real-world validation** - none of which can be reliably approximated through LLM-as-Judge evaluation of synthetic scenarios.

**Key Insights**:
1. **Verification ≈ Generation complexity** - If we can't easily verify a plan is correct, we can't easily create training data from synthetic examples
2. **LLM-as-Judge creates circular reasoning** - Using one LLM to judge another's output for training data doesn't improve beyond the judge's capability
3. **Proxy metrics don't transfer to real-world effectiveness** - High "quality scores" don't guarantee plans work in practice
4. **Real outcomes are the only valid training signal** - We need actual execution data or expert validation with real contexts

---

## Part 1: Why Workback Planning Is Hard for Post-Training

### The Fundamental Difficulty

**Workback planning is uniquely challenging** compared to other LLM tasks because:

#### 1. No Objective Ground Truth

**Compare with easier tasks**:

| Task | Ground Truth | Verification |
|------|--------------|--------------|
| **Math (AIME)** | Objective answer (e.g., 1024) | ✅ Trivial (check equality) |
| **Code Generation** | Passes unit tests | ✅ Easy (run tests) |
| **Translation** | Reference translation | ✅ Moderate (BLEU, human eval) |
| **Summarization** | Source document facts | ✅ Moderate (factual consistency) |
| **Workback Planning** | ??? (no objective correct plan) | ❌ **Hard** (subjective, context-dependent) |

**The Core Problem**: There's no single "correct" workback plan for a given context. Multiple valid plans can exist, and the "best" plan depends on:
- Unstated organizational constraints
- Team capabilities and availability
- Risk tolerance
- Resource limitations
- Political considerations
- Historical context

**Implication for Training**: We can't use "answer key" style supervision like in math problems.

#### 2. Causal Reasoning Required

**Workback planning requires multi-hop causal inference**:

```
Question: "Will this plan achieve the goal?"

Required Reasoning:
1. If we do Task A → will it produce Output X?
2. If we have Output X → can we start Task B?
3. If Task B completes → will Dependency D be satisfied?
4. If Dependency D satisfied → can we achieve Goal G?
5. What if Task A fails? (Counterfactual)
6. What if Task A takes 2x longer? (Robustness)
```

**Why This Is Hard**:
- Requires **world knowledge** (how tasks actually work in practice)
- Requires **domain expertise** (typical project timelines, dependencies)
- Requires **counterfactual reasoning** (what-if scenarios)
- Requires **temporal reasoning** (timeline feasibility)

**Current LLMs struggle with** (= **Opportunities for Scenara**):
- 🎯 Multi-hop causal chains (beyond 3-4 hops) → **Opportunity**: Build specialized models with real project data
- 🎯 Counterfactual reasoning under uncertainty → **Opportunity**: Learn from actual outcomes (what worked/failed)
- 🎯 Domain-specific constraints (not in training data) → **Opportunity**: Leverage enterprise data (ADO, calendars, org charts)
- 🎯 Temporal planning with resource constraints → **Opportunity**: Train on real resource allocation patterns

**Implication for Training**: Can't learn causal reasoning from surface patterns alone → **BUT we can learn from real-world execution data!**

**Competitive Advantage**: General-purpose LLMs will continue to struggle with workback planning because they lack:
1. Real project execution outcomes
2. Domain-specific organizational constraints
3. Temporal resource allocation patterns
4. Multi-hop causal reasoning from validated examples

**Scenara's Edge**: We can collect this data through:
- **Azure DevOps integration** - Real work items, dependencies, outcomes
- **Calendar + org data** - Actual resource constraints and availability
- **Meeting intelligence** - Context for why projects succeeded/failed
- **Expert validation** - Domain knowledge to correct model mistakes

This creates a **defensible moat** - general LLMs can't replicate without access to enterprise execution data.

#### 3. Emergent Quality from Interaction Effects

**Plan quality is not compositional**:

```
Good Task A + Good Task B + Good Dependency A→B
≠ Good Plan

Why? Because:
- Hidden dependencies may exist
- Resource conflicts may emerge
- Timeline infeasibility may arise
- Organizational constraints may block execution
```

**Example**:
```
Task 1: "Design API" (3 weeks) ✓ Reasonable
Task 2: "Implement API" (4 weeks) ✓ Reasonable
Task 3: "Write docs" (2 weeks) ✓ Reasonable
Dependency: Task 2 depends on Task 1 ✓ Correct

Total timeline: 9 weeks
User deadline: 8 weeks
Result: Plan fails despite all components being "correct"
```

**The Problem**: Local quality checks don't guarantee global plan validity.

**Implication for Training**: Can't train on individual task quality - need holistic plan evaluation.

#### 4. Subjective and Context-Dependent

**"Good plan" varies by context**:

**Same meeting context, different valid plans based on**:
- **User experience level**: Junior PM needs more detail, senior PM wants high-level
- **Team culture**: Agile team wants flexible, waterfall team wants rigid
- **Risk profile**: Startup wants fast, enterprise wants thorough
- **Resource availability**: Small team needs sequential, large team can parallelize

**Example**:
```json
Context: "Q1 Product Launch"

Plan A (Startup approach):
- Fast iteration
- 2-week sprints
- Parallel workstreams
- Ship MVP then iterate
→ Valid for startup

Plan B (Enterprise approach):
- Thorough planning
- 6-week phases
- Sequential gates
- Complete before launch
→ Valid for enterprise

Both are "correct" for their context!
```

**Implication for Training**: Can't have universal "good plan" examples - training data must capture context variations.

#### 5. Delayed Feedback Loop

**Unlike other tasks, plan quality emerges over time**:

| Task | Feedback Timing |
|------|----------------|
| Math problem | Immediate (check answer) |
| Code generation | Minutes (run tests) |
| Translation | Hours (human review) |
| **Workback planning** | **Weeks-to-months (plan execution)** |

**The Feedback Delay Problem**:
```
Time 0: Generate plan
Time +1 hour: Can check syntax (tasks, dependencies)
Time +1 day: Can check plausibility (expert review)
Time +1 week: Can check user acceptance
Time +4 weeks: Can check if plan being followed
Time +3 months: Can check if goal achieved

Training Signal Available: Only at Time +3 months!
```

**Implication for Training**: Can't rapidly iterate on training data with real feedback.

### The Verification Challenge (Verifier's Law)

**Theoretical Foundation**: For many problems, **verification complexity ≈ generation complexity**

#### When Verification Is Easy (Good for Training)

**NP-Complete problems**:
- **Generation**: Hard (exponential search)
- **Verification**: Easy (polynomial check)
- **Example**: "Is this a valid Sudoku solution?" → Just check constraints

**Learning friendly**: Can generate many examples, easily filter correct ones

#### When Verification Is Hard (Bad for Training)

**Planning problems**:
- **Generation**: Hard (exponential search space)
- **Verification**: **Also Hard** (requires simulation/execution)
- **Example**: "Is this a good project plan?" → Need to execute or deeply analyze

**Learning hostile**: Can't easily filter good examples from bad ones

#### Why Workback Plans Are Hard to Verify

**To truly verify a workback plan, you need to**:

1. **Check Logical Consistency** (Doable with algorithms)
   - No circular dependencies ✓
   - All dependencies declared ✓
   - Timeline math adds up ✓

2. **Check Factual Correctness** (Hard, requires knowledge)
   - Are referenced artifacts real? 
   - Are participant roles accurate?
   - Are technical constraints valid?

3. **Check Feasibility** (Very Hard, requires simulation)
   - Can tasks be done in estimated time?
   - Are resources actually available?
   - Are dependencies complete (no hidden ones)?

4. **Check Effectiveness** (Extremely Hard, requires execution)
   - Will this plan actually achieve the goal?
   - Is this the optimal approach?
   - What's the probability of success?

**Current state**:
- ✅ Can do #1 automatically (algorithms)
- ⚠️ Can do #2 partially (LLM fact-checking, but unreliable)
- ❌ Can't do #3 without real execution or expert analysis
- ❌ Can't do #4 without actually running the plan

**Implication for Training**: We can only train on **syntactically correct** plans, not **semantically correct** or **practically effective** plans (unless we have real execution data).

---

## Part 2: Why Stratos-Exp's Proxy Approach Fails for Post-Training

### Overview of Stratos-Exp's Evaluation Approach

**Stratos-Exp uses**:
1. **Synthetic scenarios** - Made-up meeting contexts
2. **LLM generation** - GPT-4/O1 creates plans
3. **LLM-as-Judge** - O1 evaluates plan quality (7 dimensions)
4. **Proxy metrics** - Quality scores as training signal

**The Claim**: High-quality synthetic examples (judged by O1) can be used for post-training.

**Why This Doesn't Work**: Four fundamental flaws.

### Flaw 1: Circular Reasoning

#### The Circular Logic

```
Step 1: Use GPT-4 to generate plan from context
        Input: Meeting context
        Output: Workback plan
        
Step 2: Use O1 to judge plan quality
        Input: Context + GPT-4 plan
        Output: Quality score (1-4)
        
Step 3: Select "high-quality" examples
        Filter: Keep plans with score ≥ 4
        
Step 4: Fine-tune GPT-4 on filtered examples
        Training Data: High-scoring plans
        
Result: GPT-4 learns to generate plans that O1 likes
```

**The Problem**: We're teaching GPT-4 to **satisfy O1's preferences**, not to **create effective plans**.

#### Why This Is Circular

**What O1 learned during pre-training**:
- Patterns of "good-looking" plans from internet text
- Heuristics like "plans should have dependencies"
- Surface features like "use professional language"

**What O1 doesn't know**:
- Whether plans actually work in practice
- Domain-specific constraints of user's organization
- Real-world success rates of different approaches

**When we train GPT-4 on O1-judged examples**:
- GPT-4 learns O1's heuristics
- GPT-4 learns to produce "professional-looking" plans
- GPT-4 **doesn't** learn to produce **effective** plans

**Analogy**:
```
Bad Approach:
- Student writes essay
- Teacher grades based on "sounds good"
- Student trained to write essays that "sound good" to teacher
- Result: Essays that sound good but may be wrong

Good Approach:
- Student writes essay
- Facts checked against ground truth
- Logic verified against formal rules
- Student trained on factually correct, logically sound essays
- Result: Essays that are actually correct
```

#### Empirical Evidence of Circularity

**What happens in practice**:

1. **Model collapse** - Fine-tuned model becomes deterministic, loses diversity
2. **Reward hacking** - Model learns to maximize score without improving quality
3. **Judge bias amplification** - Model inherits and amplifies judge's biases

**Example from RLHF literature**:
- Training LLMs on LLM-judged outputs → models become verbose, use certain phrases repeatedly
- Models learn to "game" the judge, not improve actual quality

**Stratos-Exp has same risk**:
- Plans become formulaic (always same structure)
- Plans use "safe" language judge prefers
- Plans don't take risks judge might penalize
- Result: **Homogeneous, conservative plans, not effective plans**

### Flaw 2: Synthetic Scenarios Lack Real-World Grounding

#### The Synthetic Data Problem

**Stratos-Exp's synthetic scenarios**:
```json
{
  "name": "Executive Strategy Alignment Workshop",
  "summary": "Executive workshop convened by Satya Nadella...",
  "artifact_refs": [
    {
      "artifact_type": "meeting",
      "artifact_id": "meet-001",  // Fake ID
      "title": "Stratos Standup",  // Made up
      "summary": "..."  // Generated, not real
    }
  ]
}
```

**What's missing**:
- ❌ Real meeting history (what actually happened in past meetings)
- ❌ Real participant dynamics (who works well with whom)
- ❌ Real organizational constraints (budget, timeline, politics)
- ❌ Real artifact content (actual documents referenced)
- ❌ Real user priorities (what user actually cares about)

#### Why Synthetic ≠ Real

**Distribution mismatch**:

| Aspect | Synthetic Scenarios | Real Scenarios |
|--------|-------------------|----------------|
| **Complexity** | Simplified, clean | Messy, ambiguous |
| **Completeness** | All info provided | Critical info missing |
| **Consistency** | Logically consistent | Often contradictory |
| **Constraints** | Stated explicitly | Implicit, must infer |
| **Ambiguity** | Minimal | High |
| **Politics** | Absent | Central |

**Example**:
```
Synthetic: "Plan product launch with marketing team"
→ Model generates: Standard product launch plan

Real: "Plan product launch with marketing team"
→ Reality: 
  - Marketing team is understaffed (not mentioned)
  - Legal review takes 3 weeks minimum (not mentioned)
  - CEO wants launch before competitor (not mentioned)
  - Budget just got cut 20% (not mentioned)
  - One team member going on leave (not mentioned)
  
→ Model's plan fails because it doesn't account for unstated constraints
```

**Training on synthetic data teaches model**:
- ✅ How to handle clean, well-specified problems
- ❌ How to handle messy, under-specified real problems

**Result**: Model works well on benchmarks, fails in production.

#### The 306K Lines of Synthetic Data

**Stratos-Exp has**:
- 306,037 lines of `workback_plan_samples.json`
- All synthetic meeting scenarios
- All generated plans

**What this corpus provides**:
- ✅ Large volume for evaluation
- ✅ Diverse scenario types
- ✅ Consistent format

**What this corpus lacks**:
- ❌ Real-world validation (no actual outcomes)
- ❌ Expert correction (no human-in-loop)
- ❌ Ground truth plans (no "correct answer")
- ❌ Execution feedback (no success/failure data)

**Conclusion**: Large synthetic corpus is useful for **evaluation research**, but insufficient for **production post-training**.

### Flaw 3: Proxy Metrics Don't Measure Effectiveness

#### The Seven Evaluation Dimensions

**Stratos-Exp evaluates on**:
1. **Correctness** - Factual accuracy
2. **Relevance** - Alignment with context
3. **Groundedness** - Based on provided data
4. **Completeness** - Covers all needs
5. **Usefulness** - Helps user achieve goal
6. **Simplicity** - No unnecessary complexity
7. **Coherence** - Internal consistency

**These are proxy metrics** - they correlate with but don't guarantee effectiveness.

#### Why Proxies Fail

**High scores don't guarantee success**:

```
Plan A:
- Correctness: 10/10 (all facts accurate) ✓
- Relevance: 10/10 (aligned with context) ✓
- Groundedness: 10/10 (based on data) ✓
- Completeness: 10/10 (covers everything) ✓
- Usefulness: 10/10 (addresses goals) ✓
- Simplicity: 10/10 (clear structure) ✓
- Coherence: 10/10 (no contradictions) ✓

Total Score: 70/70 (Perfect!)

Reality: Plan fails because timeline is too aggressive 
         (not captured by any dimension)
```

**The Gap**: Proxy metrics measure **plan properties**, not **plan outcomes**.

#### What's Not Measured

**Critical factors for real-world success**:

| Factor | Measured by Stratos-Exp? |
|--------|-------------------------|
| Timeline realism | ❌ No (can't know typical durations) |
| Resource availability | ❌ No (don't know org resources) |
| Hidden dependencies | ❌ No (can't discover unstated ones) |
| Team capability | ❌ No (don't know team skills) |
| Political feasibility | ❌ No (don't know org politics) |
| Risk management | ⚠️ Partial (identifies some risks) |
| Contingency planning | ⚠️ Partial (may suggest alternatives) |
| Execution probability | ❌ No (would need historical data) |

**Example of proxy failure**:
```
Context: "Launch new feature in 2 months"

LLM-generated plan:
- 8 tasks, well-structured
- Clear dependencies
- Milestone breakdown
- Risk mitigation steps
→ Scores 68/70 (Excellent!)

Expert review:
"This plan looks good on paper but will fail because:
1. Legal review alone takes 3-4 weeks (you budgeted 1)
2. Design team is fully booked (you assumed availability)
3. Backend API isn't ready (unstated dependency)
4. Launch requires VP approval (not in plan)
Realistic timeline: 4 months, not 2"

→ Plan would score high but fail in execution
```

**The Problem**: LLM judge evaluates **plan properties** it can see, not **hidden factors** that determine success.

### Flaw 4: No Validation Against Real Outcomes

#### The Missing Feedback Loop

**What post-training needs**:
```
Training Example = (Input Context, Output Plan, Outcome Label)

Where Outcome Label is:
- "Plan succeeded" (goal achieved, timeline met)
- "Plan failed" (goal missed or took much longer)
- Quality rating: How helpful was this plan? (1-5)
```

**What Stratos-Exp provides**:
```
Training Example = (Input Context, Output Plan, O1 Quality Score)

Where O1 Quality Score is:
- Model's judgment of plan properties
- No connection to real-world outcomes
- No validation through execution
```

**The Gap**: **Quality score ≠ Outcome label**

#### Why Outcomes Matter

**Learning from outcomes teaches**:
- ✅ What actually works in practice
- ✅ Common failure patterns to avoid
- ✅ Realistic timeline estimation
- ✅ Hidden dependencies that often appear
- ✅ Effective risk mitigation strategies

**Learning from quality scores teaches**:
- ⚠️ What looks good on paper
- ⚠️ How to satisfy a judge's heuristics
- ⚠️ Surface patterns of "professional" plans

**Example**:
```
Without outcomes:
Model learns: "Always include 'risk mitigation' section"
Why? Because judge gives higher scores when it's present

With outcomes:
Model learns: "Include legal review for product launches 
               because 73% of plans without it failed"
Why? Because historical data shows this dependency is critical
```

#### The Data Stratos-Exp Lacks

**To validate against outcomes, need**:

1. **Execution tracking**:
   ```json
   {
     "plan_id": "plan-123",
     "tasks_started": 15,
     "tasks_completed": 12,
     "tasks_blocked": 2,
     "tasks_abandoned": 1,
     "timeline_variance": +2.3,  // weeks over
     "outcome_achieved": false
   }
   ```

2. **User feedback**:
   ```json
   {
     "plan_id": "plan-123",
     "user_rating": 2.5,
     "would_use_again": false,
     "most_helpful_aspect": "Task breakdown",
     "least_helpful_aspect": "Timeline unrealistic",
     "time_spent_revising": 45  // minutes
   }
   ```

3. **Expert retrospective**:
   ```json
   {
     "plan_id": "plan-123",
     "expert_analysis": "Plan failed because it didn't 
                         account for Q3 planning freeze",
     "lessons_learned": [
       "Always check company calendar for blackout dates",
       "Add 30% buffer for cross-team dependencies"
     ]
   }
   ```

**Stratos-Exp has**: None of the above.

**Implication**: Training on Stratos-Exp data teaches **form**, not **function**.

---

## Part 3: What Effective Post-Training Requires

### The Gold Standard: Real Outcomes

**Minimum viable training example**:

```json
{
  "context": {
    "meeting": {
      "id": "real-meeting-12345",
      "subject": "Q1 Product Launch Planning",
      "date": "2025-09-15",
      "attendees": ["Alice (PM)", "Bob (Eng)", "Carol (Marketing)"],
      "body": "Discuss launch timeline and dependencies..."
    },
    "user_priorities": ["Ship MVP by Dec 1", "Marketing campaign"],
    "recent_history": [...]
  },
  
  "plan": {
    "generated_by": "Expert PM (8 years experience)",
    "outcomes": [...],
    "tasks": [...],
    "dependencies": [...]
  },
  
  "validation": {
    "method": "executed_in_real_project",
    "outcome": "success",
    "metrics": {
      "goal_achieved": true,
      "timeline_met": true,
      "completion_rate": 0.93,
      "user_rating": 4.5,
      "would_recommend": true
    }
  }
}
```

**Why this is gold standard**:
- ✅ Real context (actual meeting)
- ✅ Expert plan (proven approach)
- ✅ Real outcome (validated through execution)
- ✅ Learning signal (what worked/didn't work)

### Practical Alternatives When Outcomes Unavailable

#### Alternative 1: Expert Validation with Real Contexts

**If can't wait for execution outcomes**:

```json
{
  "context": {
    "meeting": "real-meeting-12345",  // Real meeting from Scenara
    // ... actual meeting data
  },
  
  "plan": {
    "generated_by": "model",
    "initial_plan": {...}
  },
  
  "expert_review": {
    "reviewer": "Senior PM (12 years)",
    "would_use_as_is": false,
    "critical_issues": [
      "Missing legal review step",
      "Timeline 2x too aggressive"
    ],
    "corrected_plan": {...},  // Expert's fixed version
    "correction_time": 20,  // minutes
    "teaching_points": [
      "Product launches always need legal review",
      "Backend changes typically take 4-6 weeks, not 2"
    ]
  }
}
```

**Training signal**: Learn from **expert corrections** on **real contexts**

**Why this works**:
- ✅ Real contexts (actual complexity)
- ✅ Expert knowledge (domain expertise)
- ✅ Concrete corrections (what to fix)
- ⚠️ No outcome validation (but expert judgment > LLM judgment)

#### Alternative 2: Preference Learning from Comparisons

**If absolute quality is hard to judge**:

```json
{
  "context": "real-meeting-12345",
  
  "plan_A": {
    "generator": "GPT-4",
    "plan": {...}
  },
  
  "plan_B": {
    "generator": "O1",
    "plan": {...}
  },
  
  "plan_C": {
    "generator": "Expert PM",
    "plan": {...}
  },
  
  "expert_ranking": {
    "best": "plan_C",
    "second": "plan_B",
    "worst": "plan_A",
    "rationale": [
      "Plan C has most realistic timeline",
      "Plan B correctly identified critical path",
      "Plan A missed key dependency"
    ]
  }
}
```

**Training method**: Direct Preference Optimization (DPO) or RLHF

**Why this works**:
- ✅ Easier to judge "A better than B" than "A is 4.2/5"
- ✅ More robust to annotator disagreement
- ✅ Learns relative quality effectively

#### Alternative 3: Behavioral Signals from Real Usage

**Track user behavior with generated plans**:

```json
{
  "plan_id": "plan-789",
  "context": "real-meeting-12345",
  "plan": {...},
  
  "user_behavior": {
    "viewed": true,
    "time_viewing": 180,  // 3 minutes
    "made_edits": true,
    "edit_summary": {
      "added_tasks": 2,
      "removed_tasks": 0,
      "changed_dependencies": 3,
      "adjusted_timelines": 5
    },
    "saved": true,
    "exported": true,
    "referred_back": 3,  // times user opened plan again
    "implicit_rating": 3.5  // inferred from behavior
  }
}
```

**Training signal**: Plans users engage with positively are better

**Why this works**:
- ✅ Reflects real user preferences
- ✅ Scales automatically
- ⚠️ Delayed signal (need to wait for user interaction)
- ⚠️ Noisy (behavior ≠ quality perfectly)

### Strategic Framework: Complexity vs. Value

Before diving into data collection, we need to **stratify projects by complexity and value** to optimize our rollout strategy and training data priorities.

**CRITICAL INSIGHT**: The challenges that make workback planning hard for LLMs are **exactly the opportunities** that make it valuable for enterprise customers - and create a defensible competitive moat when we solve them with real data.

#### The Two-Dimensional Framework

**Dimension 1: Project Complexity**

| Complexity Level | Characteristics | Examples |
|-----------------|-----------------|----------|
| **Low** | - Single team<br>- Clear dependencies<br>- Standard workflows<br>- 2-4 weeks duration<br>- 5-10 tasks | - Feature bug fix sprint<br>- Documentation update<br>- Internal tool enhancement |
| **Medium** | - 2-3 teams<br>- Some cross-functional deps<br>- Mostly standard workflows<br>- 1-3 months duration<br>- 10-20 tasks | - New feature launch<br>- API integration<br>- Marketing campaign |
| **High** | - 4+ teams<br>- Complex dependencies<br>- Custom workflows<br>- 3-6 months duration<br>- 20-50 tasks | - Product launch<br>- Platform migration<br>- Org-wide initiative |
| **Very High** | - Cross-org coordination<br>- External dependencies<br>- Regulatory/legal constraints<br>- 6+ months duration<br>- 50+ tasks | - Major product release<br>- M&A integration<br>- Compliance overhaul |

**Dimension 2: Workback Plan Value**

| Value Level | Impact | Why Workback Plan Helps |
|-------------|--------|------------------------|
| **High** | - Mission critical<br>- Hard deadline<br>- Multiple stakeholders<br>- High coordination needs<br>- Resource constraints | - Prevents missed deadlines<br>- Aligns stakeholders<br>- Optimizes resources<br>- Identifies risks early |
| **Medium** | - Important but flexible<br>- Few dependencies<br>- Clear ownership<br>- Adequate resources | - Provides structure<br>- Helps tracking<br>- Moderate benefit |
| **Low** | - Routine work<br>- Individual contributor<br>- Well-known process<br>- Low stakes | - Minimal benefit<br>- Overhead > value<br>- Not worth detailed planning |

#### The Strategic Quadrants

```
Value
  ^
  |
H |  Q2: High Value        Q1: High Value
I |      Low Complexity        High Complexity
G |      [START HERE]          [GRADUATE TO]
H |      ✅ Quick wins         🎯 Ultimate goal
  |      ✅ Easy to validate    ⚠️ Hard to master
  |
M |  Q3: Medium Value      Q4: Medium Value
E |      Low Complexity        High Complexity
D |      [LATER]               [DEPRIORITIZE]
  |      ⚠️ Lower ROI          ❌ High cost, low return
  |
L |  --------------------|--------------------
O |    LOW    MEDIUM    |    HIGH   VERY HIGH
W |                COMPLEXITY →
```

**Rollout Strategy**: Q2 → Q1 → Q3 → Q4

#### Quadrant 1: High Value + High Complexity (ULTIMATE GOAL)

**Project Types**:
- Product launches
- Platform migrations
- Cross-org initiatives
- Major feature releases

**Characteristics**:
- **Complexity**: 4+ teams, 20-50 tasks, 3-6 months
- **Value**: Mission critical, hard deadlines, exec visibility
- **Challenge**: Hardest to generate good plans
- **ROI**: Massive if done well

**Why Start Here Is Wrong**:
- ❌ Too complex to validate training data quality
- ❌ Expert bandwidth required is high
- ❌ Long feedback loops (months to see outcomes)
- ❌ Many confounding factors for failure
- ❌ Model will struggle, user trust damaged

**When to Graduate Here**: After proving value in Q2

#### Quadrant 2: High Value + Low Complexity (START HERE) ✅

**Project Types**:
- Feature launches (single team)
- Time-sensitive bug fixes
- Sprint planning with dependencies
- Quarterly planning meetings

**Characteristics**:
- **Complexity**: Single team, 5-15 tasks, 2-6 weeks
- **Value**: Important outcomes, clear deadlines, stakeholder alignment needed
- **Challenge**: Manageable - model can learn patterns
- **ROI**: High - real pain point, achievable quality

**Why Start Here**:
- ✅ **Quick validation** - See outcomes in weeks, not months
- ✅ **Clear success criteria** - Did we ship on time?
- ✅ **Easier for experts** - Can review 10 plans/hour vs 2 plans/hour
- ✅ **Model can succeed** - Within current LLM capabilities
- ✅ **Build user trust** - Early wins establish confidence
- ✅ **Fast iteration** - Learn and improve quickly

**Data Collection Priority**: **80% of initial training data should come from Q2**

**Example Scenarios**:
```json
{
  "scenario": "Launch new dashboard feature by Q4",
  "complexity": "Low",
  "value": "High",
  "why_high_value": "CEO committed to customers",
  "why_low_complexity": "Single eng team, existing UI framework",
  "ideal_for_training": true,
  "expected_plan_quality": "Model should generate 70%+ correct"
}
```

#### Quadrant 3: Medium Value + Low Complexity (LATER)

**Project Types**:
- Internal tooling improvements
- Documentation projects
- Process optimizations
- Team offsites

**Characteristics**:
- **Complexity**: Low (single team, simple deps)
- **Value**: Medium (nice to have, flexible deadlines)
- **Challenge**: Low
- **ROI**: Moderate - less urgency

**Prioritization**: After Q2 is working well

**Data Collection**: 10-15% of training data from Q3 for diversity

#### Quadrant 4: Medium-Low Value + High Complexity (DEPRIORITIZE)

**Project Types**:
- Exploratory research
- Long-term infrastructure
- Speculative initiatives

**Characteristics**:
- **Complexity**: High (many teams, complex deps)
- **Value**: Medium-Low (flexible, nice-to-have)
- **Challenge**: Very high
- **ROI**: Low - high effort, low urgency

**Prioritization**: Only after Q1 is mastered

**Data Collection**: <5% of training data, mostly for edge cases

### Revised Data Collection Roadmap for Scenara

**STRATEGIC PIVOT**: Start with Azure DevOps (ADO) data as primary training source, supplement with Scenara meetings for context enrichment.

#### Why Azure DevOps First?

**ADO provides the "gold standard" training data we identified as critical**:

| Required Component | ADO Provides | Scenara Meetings Provide |
|-------------------|--------------|-------------------------|
| **Real project contexts** | ✅ Actual work items, epics, features | ✅ Meeting discussions |
| **Expert-created plans** | ✅ Task breakdowns, dependencies | ⚠️ Implicit (need extraction) |
| **Execution outcomes** | ✅ Completed/delayed/blocked status | ❌ No execution tracking |
| **Timeline validation** | ✅ Estimated vs actual duration | ❌ No follow-through data |
| **Resource constraints** | ✅ Team assignments, capacity | ⚠️ Attendee availability only |
| **Complexity indicators** | ✅ Story points, effort, dependencies | ⚠️ Inferred from attendees |
| **Value indicators** | ✅ Priority, business value | ⚠️ Inferred from participants |

**ADO Advantages**:
1. **Built-in outcome validation** - Every work item has status (completed/blocked/abandoned)
2. **Natural complexity stratification** - Epic → Feature → User Story → Task hierarchy
3. **Explicit dependencies** - Predecessor/successor relationships already defined
4. **Timeline actuals** - Original estimate vs actual completion time
5. **Team and capacity data** - Who worked on what, how long it took
6. **No circular reasoning** - Human PMs created these plans, then executed them
7. **Scalable** - Organizations have thousands of completed work items

**Integration with Scenara**:
- Use ADO work items as **training data backbone**
- Enrich with Scenara meeting context (discussions that led to decisions)
- Link meetings → ADO work items → outcomes
- Best of both: **Real plans with conversational context**

#### Phase 0A: ADO Data Discovery & Classification (1 week)

**Goal**: Identify accessible ADO projects and classify by complexity/value

**Method**:
1. **Leverage SilverFlow's `bizchat_search_ado.py`** for ADO access
   - Already have authentication patterns
   - Can query work items, sprints, backlogs
2. **Sample ADO projects** from accessible organizations
   - Target: 10-20 completed projects
   - Various sizes and complexities
3. **Extract work item structure**:
   ```python
   {
     "project_id": "Project-123",
     "epic": "Q3 Product Launch",
     "features": [...],
     "user_stories": [...],
     "tasks": [...],
     "dependencies": [...],
     "sprint_assignments": [...],
     "actual_outcomes": {
       "planned_duration": "8 weeks",
       "actual_duration": "10 weeks",
       "completion_rate": 0.87,
       "blocked_items": 5,
       "scope_changes": 3
     }
   }
   ```
4. **Classify by complexity/value framework**:
   - Count teams involved (1 = Q2/Q3, 2-3 = Q1/Q4)
   - Measure dependency depth
   - Check business value/priority tags
   - Assess timeline (2-6 weeks = Q2/Q3, 3-6 months = Q1/Q4)

**Output**: 
- List of 10-20 ADO projects classified by quadrant
- 50-100 completed work items per project
- Total corpus: 500-2000 work items with outcomes

**ADO Query Example**:
```python
# Using Azure DevOps REST API
GET https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.0

{
  "query": "SELECT [System.Id], [System.Title], [System.State], 
           [System.WorkItemType], [Microsoft.VSTS.Scheduling.OriginalEstimate],
           [Microsoft.VSTS.Scheduling.CompletedWork]
           FROM WorkItems 
           WHERE [System.TeamProject] = 'MyProject' 
           AND [System.State] = 'Closed'
           AND [System.ClosedDate] >= '2024-01-01'
           ORDER BY [System.ChangedDate] DESC"
}
```

#### Phase 0B: Classify Existing Scenara Meetings (1 week - parallel)

**Goal**: Categorize 267 meetings by complexity and value

**Method**:
1. Analyze meeting metadata (attendees, subject, duration)
2. Apply classification heuristics:
   ```python
   complexity = f(num_teams, num_attendees, timeline, cross_functional)
   value = f(has_deadline, exec_attendance, follow_up_count, urgency_keywords)
   ```
3. Manual review for 20% sample
4. Generate distribution report

**Expected Distribution**:
- Q1 (High/High): ~15% (40 meetings)
- Q2 (High/Low): ~30% (80 meetings) ✅ **Primary target**
- Q3 (Med/Low): ~35% (93 meetings)
- Q4 (Med/High): ~20% (54 meetings)

**Output**: Classified meeting dataset with priority scores

#### Phase 1: Pilot with ADO Q2 Projects (2 weeks)

**Goal**: Collect 50-100 high-quality training examples from **ADO Q2 work items** (High Value + Low Complexity)

**Method**:
1. **Select 50-100 completed ADO work items** from Q2 category:
   - Single team scope (User Stories or small Features)
   - 2-6 week duration
   - High priority/business value
   - Completed in last 6 months (recent, relevant)
   - Clear outcome (shipped/completed successfully)

2. **Extract complete work item data**:
   ```python
   training_example = {
     "context": {
       "work_item_id": "12345",
       "title": "Implement user dashboard filters",
       "description": "Add filtering capability to admin dashboard...",
       "acceptance_criteria": [...],
       "business_value": "High",
       "story_points": 8,
       "team": "Frontend Team",
       "sprint": "Sprint 23",
       "related_meetings": [...]  # Link to Scenara meetings if available
     },
     
     "plan": {
       "tasks": [
         {
           "id": "12346",
           "title": "Design filter UI mockups",
           "assigned_to": "Alice",
           "estimated_hours": 8,
           "dependencies": [],
           "actual_hours": 10
         },
         {
           "id": "12347", 
           "title": "Implement filter backend API",
           "assigned_to": "Bob",
           "estimated_hours": 16,
           "dependencies": ["12346"],
           "actual_hours": 14
         }
         // ... more tasks
       ],
       "total_estimated": "40 hours",
       "total_actual": "42 hours"
     },
     
     "outcome": {
       "status": "Completed",
       "planned_duration_days": 10,
       "actual_duration_days": 11,
       "completion_rate": 1.0,
       "on_time": true,
       "blocked_count": 0,
       "scope_changes": 1,
       "quality": "Met acceptance criteria",
       "lessons": "UI mockups took longer than expected"
     }
   }
   ```

3. **Enrich with Scenara meeting context** (optional but valuable):
   - Search for meetings related to this work item
   - Extract discussion context, decisions made
   - Link meeting insights to work item planning

4. **Validate data quality**:
   - All work items have complete task breakdowns ✅
   - Dependencies are explicit ✅
   - Outcomes are recorded ✅
   - Timelines are realistic ✅

**Output**: 50-100 (ADO work item, task plan, actual outcome) triplets

**Cost**: FREE - data already exists in ADO!

**Success Criteria**:
- 100% have outcome data (vs 0% for synthetic)
- Task breakdown depth ≥ 3 levels (User Story → Tasks)
- Timeline accuracy within 20% (proves realistic estimates)
- Can identify success patterns (what made on-time projects succeed)

**Advantages over Scenara meetings**:
- ✅ **Execution data built-in** - no need to wait months for outcomes
- ✅ **Structured format** - tasks, dependencies already defined
- ✅ **Natural supervision signal** - completed vs blocked vs delayed
- ✅ **Scalable** - thousands of examples available
- ✅ **No expert annotation needed** - work was already done by real teams

#### Phase 2: Validate LLM Judge on Q2 Projects (1 week)

**Goal**: Determine if LLM judge correlates with experts **for Q2 complexity level**

**Method**:
1. Take 50 Q2 pilot examples
2. Get O1 quality scores
3. Get expert quality scores
4. Calculate correlation **by complexity tier**

**Critical Insight**: LLM judge may work for Q2 (low complexity) but fail for Q1 (high complexity)

**Decision Tree**:
```
Q2 Correlation > 0.7:
  → LLM judge reliable for low-complexity projects
  → Can scale Q2 synthetic data
  → Still need experts for Q1 data
  
Q2 Correlation 0.5-0.7:
  → LLM judge useful for filtering, not scoring
  → Use LLM to eliminate clearly bad plans
  → Expert review for final quality
  
Q2 Correlation < 0.5:
  → LLM judge unreliable even for simple cases
  → Need expert annotation for all data
  → Higher cost but better quality
```

#### Phase 3: Scale Q2 Collection (4-6 weeks)

**Focus**: Build robust Q2 dataset before tackling Q1

**If LLM validated for Q2 (correlation > 0.7)**:
- Generate 400 Q2 synthetic scenarios
- Filter with LLM (keep ≥ 4.0)
- Expert spot-check 10% (40 examples)
- Add 100 real Q2 Scenara meetings
- **Result**: 500 Q2 examples (80% synthetic, 20% real)

**If LLM not validated (correlation < 0.5)**:
- Prioritize real Scenara Q2 meetings
- Target: 200 Q2 examples
- All expert-annotated
- **Result**: 200 Q2 expert-validated examples

**Plus add diversity**:
- 50 Q3 examples (10%)
- 25 Q1 examples (5%) - aspirational/learning
- 25 edge cases (5%)

**Total corpus**: 500-600 examples, **80% from Q2 sweet spot**

#### Phase 4: Instrument Production System

**Long-term data collection**:
1. Log all plan generations
2. Track user interactions
3. Collect user feedback
4. Follow up on outcomes

**Continuous improvement**:
- Retrain monthly on new data
- A/B test improvements
- Monitor production metrics

---

## Part 4: Key Takeaways and Recommendations

### Critical Insights

#### 1. Workback Planning Is Uniquely Difficult

**Unlike math or code generation**:
- ❌ No objective ground truth
- ❌ Can't verify without execution
- ❌ Quality emerges over time
- ❌ Highly context-dependent

**Implication**: Need fundamentally different approach than typical supervised learning.

#### 2. LLM-as-Judge Is Insufficient

**Problems**:
- Circular reasoning (model learns judge's preferences)
- No real-world grounding
- Proxy metrics ≠ effectiveness
- No validation against outcomes

**Use case**: LLM-as-Judge useful for **evaluation research**, not **post-training data creation**.

#### 3. Real Outcomes Are Essential

**What matters**:
- Did the plan work in practice?
- Did user find it helpful?
- What needed to be corrected?

**Not**: What score did another LLM give it?

#### 4. Expert Knowledge Beats Synthetic Data

**50 expert-corrected real examples > 500 LLM-judged synthetic examples**

Why?
- Captures domain expertise
- Reflects real-world constraints
- Teaches practical patterns

### Recommendations for Scenara

#### DO ✅

1. **Start with Q2 projects (High Value + Low Complexity)**
   - 80% of initial training data from this quadrant
   - Quick validation cycles (weeks not months)
   - Build user trust with early wins
   - Prove value before tackling harder cases

2. **Use real meeting contexts** from Scenara calendar
   - We have 267 meetings (April-Oct 2025)
   - Classify by complexity and value first
   - Prioritize ~80 Q2 meetings for initial data
   - Real complexity and ambiguity

3. **Get expert validation/correction**
   - Have PMs/team leads review plans
   - Should take <15 min for Q2 projects
   - Collect corrections and rationales
   - Build corpus of expert knowledge

4. **Graduate complexity levels strategically**
   - Phase 1: Master Q2 (Low complexity, high value)
   - Phase 2: Add Q3 diversity (Low complexity, medium value)
   - Phase 3: Tackle Q1 (High complexity, high value)
   - Phase 4: Complete with Q4 if needed

5. **Track user behavior by complexity tier**
   - Separate metrics for Q1 vs Q2 vs Q3
   - Expect higher success rate on Q2
   - Don't penalize model for Q1 struggles early on
   - Use behavioral signals

6. **Validate LLM judge separately by complexity**
   - LLM may work well for Q2 but fail for Q1
   - Don't assume correlation transfers across tiers
   - Test separately: Q2 correlation, Q1 correlation
   - Scale synthetic only where validated

7. **Use preference learning**
   - Easier to get "A better than B" than absolute scores
   - More robust training signal
   - DPO/RLHF methodology

#### DON'T ❌

1. **Don't start with Q1 (High/High) projects**
   - Too complex to validate training data
   - Long feedback loops (months)
   - Model will struggle, damage user trust
   - Graduate here only after Q2 success

2. **Don't treat all projects the same**
   - Complexity matters for training difficulty
   - Value matters for prioritization
   - Track and report metrics by quadrant
   - Different success criteria per tier

3. **Don't rely solely on synthetic scenarios**
   - Distribution mismatch with real use cases
   - Missing critical context
   - Teaches wrong patterns
   - Even for Q2, validate with real data

4. **Don't use LLM quality scores as training labels**
   - Circular reasoning
   - Doesn't improve beyond judge
   - Amplifies judge's biases
   - Especially problematic for Q1 complexity

5. **Don't assume proxy metrics = effectiveness**
   - High scores ≠ plans work
   - Many failure modes not captured
   - Need real outcomes
   - More critical for higher complexity

6. **Don't skip expert validation**
   - Domain expertise essential
   - Catches issues LLMs miss
   - Provides teaching signal
   - Required even for Q2

7. **Don't ignore the value dimension**
   - Not all plans worth optimizing
   - Focus on high-value scenarios
   - Low-value + high-complexity = waste resources
   - ROI-driven prioritization

### The Path Forward

#### Short-term (Weeks 1-4)

1. **Classify Scenara meetings** (Week 1)
   - Analyze 267 meetings
   - Assign complexity level (Low/Medium/High/Very High)
   - Assign value level (High/Medium/Low)
   - Identify ~80 Q2 projects (High Value + Low Complexity)

2. **Collect Q2 pilot dataset** (Weeks 2-3)
   - 50 Q2 examples (High Value + Low Complexity)
   - Real Scenara meetings
   - Expert-corrected plans
   - Validate approach

3. **Instrument system** (Week 4)
   - Log generations by complexity tier
   - Track user interactions
   - Collect feedback by project type
   - Set up A/B testing framework

#### Medium-term (Weeks 5-12)

4. **Validate LLM judge for Q2** (Week 5)
   - Check correlation with experts
   - Q2-specific validation
   - Decide: Scale synthetic or continue expert annotation

5. **Scale Q2 collection** (Weeks 6-10)
   - 400-500 Q2 examples (target)
   - Mix: 80% Q2, 10% Q3, 5% Q1, 5% edge cases
   - Build robust low-complexity corpus

6. **First post-training iteration** (Weeks 11-12)
   - Fine-tune on Q2 data
   - A/B test vs baseline on Q2 projects
   - Success criteria: >60% win rate on Q2
   - Do NOT evaluate on Q1 yet

#### Long-term (Weeks 13+)

7. **Graduate to Q1 projects** (After Q2 success)
   - Add 100-200 Q1 examples
   - Higher complexity, higher value
   - Retrain with mixed Q1+Q2 data
   - Target: >50% win rate on Q1

8. **Continuous learning**
   - Monthly retraining with new data
   - Separate metrics by complexity tier
   - Outcome tracking when available
   - Expert feedback loop

9. **Build feedback culture**
   - Users rate plans by project type
   - Report issues with context
   - Suggest improvements

### Complexity-Based Success Metrics

**Different expectations by quadrant**:

| Quadrant | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|----------|---------------|----------------|----------------|
| **Q2 (High/Low)** | 60% win rate | 75% win rate | 85% win rate |
| **Q3 (Med/Low)** | 50% win rate | 65% win rate | 75% win rate |
| **Q1 (High/High)** | 30% win rate | 45% win rate | 60% win rate |
| **Q4 (Med/High)** | Not measured | 35% win rate | 50% win rate |

**Why different targets?**
- Q2 is easier → expect higher success
- Q1 is harder → accept lower success initially
- Don't penalize model for appropriate difficulty
- Track improvement trajectory, not absolute numbers

**Win rate definition**: Expert rates model plan vs baseline, "which would you use?"

**Gating criteria for graduation**:
- Must achieve 75%+ win rate on Q2 before focusing on Q1
- Must achieve 60%+ win rate on Q1 before claiming "solved"
- Must maintain Q2 performance when adding Q1 data

---

## Conclusion

**The Central Thesis**: Workback planning post-training cannot rely on LLM-as-Judge evaluation of synthetic scenarios because:

1. **Verification complexity ≈ Generation complexity** - Can't easily filter good from bad synthetic examples
2. **Circular reasoning** - LLM judging LLM doesn't improve beyond judge's capability  
3. **Proxy metrics ≠ Real outcomes** - Quality scores don't guarantee practical effectiveness
4. **Synthetic ≠ Real** - Distribution mismatch causes production failures
5. **Complexity varies dramatically** - Must stratify by project complexity and value

**The Solution**: Post-training requires **real contexts**, **expert knowledge**, **outcome validation**, and **strategic complexity graduation**.

**Strategic Framework**:
- **Start with Q2** (High Value + Low Complexity): Quick wins, build trust, prove value
- **Graduate to Q1** (High Value + High Complexity): After mastering Q2, tackle harder cases
- **Different success metrics by tier**: 85% win rate on Q2, 60% on Q1 is realistic
- **80/10/5/5 data split**: 80% Q2, 10% Q3, 5% Q1, 5% edge cases initially

**Stratos-Exp's contribution**: Excellent evaluation framework for research, but **insufficient for production post-training** because it:
- Doesn't differentiate by complexity
- Treats all scenarios uniformly
- Lacks real-world validation
- Uses circular LLM-as-Judge approach

**Scenara's opportunity**: We have 267 real meetings spanning complexity levels:
- Classify meetings by complexity and value
- Start with ~80 Q2 meetings (High Value + Low Complexity)
- Build robust Q2 performance first (75%+ win rate)
- Graduate to Q1 only after Q2 success (60%+ win rate target)
- Leverage real contexts with expert validation

**The key insight**: Not all workback planning tasks are equally hard. Strategic rollout from **high-value, low-complexity to low-value, high-complexity** optimizes learning efficiency and user trust.

**The takeaway**: Post-training for complex reasoning tasks like workback planning requires:
1. Fundamentally different approach than simpler tasks
2. Real-world grounding, not synthetic shortcuts
3. Strategic complexity graduation
4. Different success criteria by complexity tier
5. Continuous learning with outcome validation

---

## Appendix: Comparison to Other Domains

### Domains Where Synthetic + LLM-Judge Works

**Math reasoning (GSM8K, MATH)**:
- ✅ Objective ground truth
- ✅ Easy verification
- ✅ Can generate infinite examples
- **Verdict**: Synthetic data works well

**Code generation (HumanEval)**:
- ✅ Can run unit tests
- ✅ Clear pass/fail
- ✅ Many problems available
- **Verdict**: Synthetic + execution works

### Domains Where It Partially Works

**Summarization**:
- ⚠️ Can check factual consistency
- ⚠️ Quality is somewhat subjective
- ⚠️ Need human preference data eventually
- **Verdict**: Synthetic helps, but need human feedback for production

**Creative writing**:
- ⚠️ Highly subjective
- ⚠️ LLM judge correlates moderately with humans
- ⚠️ Style/tone hard to define
- **Verdict**: Synthetic useful for exploration, human judgment for quality

### Domains Where It Doesn't Work (Like Workback Planning)

**Strategic planning**:
- ❌ No ground truth
- ❌ Effectiveness delayed
- ❌ Context-dependent
- **Verdict**: Need expert knowledge + outcomes

**Medical diagnosis**:
- ❌ High stakes
- ❌ Rare cases underrepresented
- ❌ Need real validation
- **Verdict**: Must use real cases + expert review

**Legal reasoning**:
- ❌ Precedent-based
- ❌ Consequences matter
- ❌ Expert judgment essential
- **Verdict**: Cannot learn from synthetic alone

**Workback planning** falls into the last category - **complex, high-stakes reasoning that requires real-world grounding**.

---

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Version**: 2.0  

**Key Message**: For workback planning post-training, there are no shortcuts - we need real contexts, expert knowledge, and outcome validation. Stratos-Exp's LLM-as-Judge approach is useful for evaluation research but insufficient for production training data.
