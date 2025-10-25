# Slide #1

# Unit Task Benchmarking Framework for Golden Prompts

**Contact**: Chin-Yew Lin  
Evaluating performance across complex task combinations effectively  
T+P DS DKI

---

# Slide #2

## Goal

Create a scalable, interpretable, human-aligned, and developer-friendly evaluation framework for Calendar.AI using golden prompts decomposed into unit tasks (UTs).

This framework will:
- Support **modular benchmarking** through unit task decomposition
- Enable **rubric-based scoring** for generative outputs
- Ensure **ecological validity** by aligning metrics with real-world user experiences
- Provide **actionable insights** for product and engineering teams

---

# Slide #3

## Golden Prompt Decomposition to Unit Tasks

Break down complex prompts into atomic, actionable units.

Each unit task is:
- **Atomic**: Single intent
- **Composable**: Reusable across prompts
- **Evaluable**: Independently testable

**Example:**  
“C1 Help me prepare for meetings with pre-reads by letting me know when they are available and give me the option to block time to review them.”

- C1.1 “Find meetings with pre-reads”
- C1.2 “Notify when pre-reads are available”
- C1.3 “Schedule time to review pre-reads”

---

# Slide #4

## Generalized Unit Task Templates (GUTTs)

- Abstracted patterns from unit tasks
- Enable prompt generation and consistent evaluation

**Example:**  
“C1 Help me prepare for meetings with pre-reads by letting me know when they are available and give me the option to block time to review them.”

---

# Slide #5

## Example: C2 Agenda Setting for Project Review

**Prompt:**  
Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.

---

# Slide #6

## Tiered Benchmarking

Stratify compound (golden) prompts by complexity.

---

# Slide #7

## Scoring Strategy

- **Per-UT scoring**: Track performance at unit task level
- **Compound prompt score**: Aggregated but tier-aware
- **Failure tolerance**: Partial credit for complex prompts
- **Rubric-based scoring for generative output**: Apply structured evaluation criteria to assess quality, relevance, usefulness, and clarity of generated responses

---

# Slide #8

## Per-UT (Unit Task) Scoring

**Definition:**  
Score each atomic unit task (UT) in a compound prompt independently, providing fine-grained insight into system strengths and weaknesses.

**How It’s Computed:**
- Assign a score to each UT (e.g., 1 = success, 0 = fail; or rubric-based 0–3).
- Scoring is based on whether the expected action or artifact is present and correct.

**Example:**  
Prompt: “Help me prepare for meetings with pre-reads.”

---

# Slide #9

## Per-Task Aggregation

**Definition:**  
Aggregate scores for each unit task (UT) across all compound prompts in the benchmark to measure how well the system performs on that specific task type.

**How It’s Computed:**
- For each UT (e.g., “Notify when pre-reads are available”), collect all instances across all prompts.
- Compute the average (or distribution) of scores for that UT.

**Usage:**
- Reveals system strengths and weaknesses at the feature level.
- Enables FCs to monitor, diagnose, and improve their owned UTs across all scenarios.

**Example:**  
Suppose “Notify when pre-reads are available” (GUTT.12) appears in 4 prompts:

> Per-task score for “Notify when pre-reads are available” (GUTT.12):  
> Per-Task Score = (1 + 0 + 1 + 1) / 4 = 0.75 (or 75%)

---

# Slide #10

## Compound (Golden) Prompt Scoring

**Definition:**  
Aggregate the scores of all UTs in a compound prompt to produce an overall prompt score, reflecting holistic system performance.

**How It’s Computed:**
- **Simple Average:**  
  Compound Score = (Sum of UT Scores) / (Number of UTs)
- **Weighted Average:**  
  Assign higher weights to more critical UTs if needed.

**Example:**  
From previous slide: Compound Score = (1 + 1 + 0) / 3 = 0.67 (or 67%)

**Usage:**
- Enables comparison across prompts and models.
- Used for reporting, benchmarking, and release criteria.

---

# Slide #11

## Failure Tolerance

**Definition:**  
Allows partial credit for compound prompts when some, but not all, UTs succeed—reflecting real-world complexity and supporting incremental improvement.

**How It’s Computed:**
- If at least one UT succeeds, partial credit is given.
- Failure tolerance can be tier-aware (e.g., higher tolerance for Tier 3/4 prompts).

**Usage:**
- Encourages progress on complex tasks.
- Prevents “all-or-nothing” scoring for multi-step prompts.

**Example:**  
Prompt: “Help me set the agenda to review Project Alpha.”

> Compound Score: 0.5 (2/4 UTs succeeded)  
> System gets partial credit.  
> Dev team can prioritize fixing agenda generation and status tracking.

---

# Slide #12

## Rubric-Based Evaluation for Generative Output

**Key Principles:**
- Decompose golden prompts into atomic unit tasks (UTs) for modular evaluation.
- Apply rubric dimensions (e.g., relevance, clarity, coverage, conciseness) to each generative output, tailored to the unit task.
- Score each criterion using a consistent scale (e.g., 0–3), enabling fine-grained, actionable feedback.
- Leverage meeting type information to select or combine rubrics, ensuring contextually accurate evaluation for meeting prep scenarios.

**Benefits:**
- Enables consistent, transparent, and modular benchmarking.
- Supports targeted model improvement and feature team accountability.

---

# Slide #13

## Practical Workflow for Rubric Evaluation

**Step-by-Step Process:**
1. **Decompose Prompt:** Break down the generative prompt into unit tasks.
2. **Determine Meeting Type(s):** Identify all relevant meeting types for the scenario.
3. **Select/Combine Rubrics:** Choose rubric dimensions based on meeting type(s).
4. **Evaluate Output:** Score each unit task’s output against rubric criteria.
5. **Aggregate Scores:** Report per-task, per-prompt, and per-dimension performance.
6. **Actionable Feedback:** Use results to guide model and feature team improvements.

---

# Slide #14

## Golden Prompt: C.4 – Leadership Meeting Preparation

**Prompt:**  
"Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."

---

# Slide #15

## Example Evaluation C.4

**Generated Output:**  
**Summary Points:**
- Budget allocation for Q4
- Product roadmap alignment
- Risk mitigation strategies

**Objection:**  
"We’re concerned that the Q4 budget cuts will impact product delivery timelines."

**Response:**  
"We’ve adjusted the roadmap to prioritize critical features and maintain delivery targets despite budget constraints."

**Total Score:** 34/36 → High-quality generative output

**Benefits**
- Enables granular evaluation of generative capabilities
- Supports modular benchmarking tied to golden prompts
- Provides actionable feedback for model improvement

---

# Slide #16

## Developer Impact

Each UT maps to a feature team.  
UT scores help:
- Diagnose failures
- Track improvements
- Prioritize roadmap

---

# Slide #17

## Next Steps

- Create work backplan to meet Ignite deadline
- Generate synthetic compound prompts from GUTTs
- Collect and annotate data for evaluation
- Tag GUTTs with tier and owner
- Build dashboard for UT performance

---

# Slide #18

## Appendix

---

# Slide #19

## GUTT Templates

| GUTT ID  | Template                                      |
|----------|-----------------------------------------------|
| GUTT.1   | Identify where [resource] is spent            |
| GUTT.2   | Identify reclaimable [resource] from [source] |
| GUTT.3   | Align [resource] usage with [goal]            |
| GUTT.4   | Commit only to [entity] that match [criteria] |
| GUTT.5   | Track all [entity] that meet [criteria]       |
| GUTT.6   | Flag [entity] needing [action/resource]       |
| GUTT.7   | Create [timeframe] plan for [goal/project]    |
| GUTT.8   | Balance [plan/schedule] with [priorities]     |
| GUTT.9   | Ask probing questions to uncover [cause/issue]|
| GUTT.10  | Diagnose why [goal] is not achieved           |
| GUTT.11  | Find [entity] with [attribute]                |
| GUTT.12  | Notify when [entity] becomes [state]          |
| GUTT.13  | Schedule time to [action] for [entity]        |
| GUTT.14  | Identify [project/team/person] from context   |
| GUTT.15  | Track status of [project/task] from [source]  |
| GUTT.16  | Create agenda to [goal] using [context]       |
| GUTT.17  | Find content of [artifact] for [event]        |
| GUTT.18  | Identify incomplete parts of [artifact] and owners |
| GUTT.19  | Send reminder to [person] to complete [task]  |
| GUTT.20  | Summarize [materials] into [N] key points     |
| GUTT.21  | Generate possible [objections/risks] for [context] |
| GUTT.22  | Generate responses to [objections/risks]      |
| GUTT.23  | Prepare brief for [meeting/person]            |
| GUTT.24  | Create dossier for [person] with [interest/topics] |
| GUTT.25  | Provide background on [organization/topic]    |
