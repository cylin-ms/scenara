# Verifier's Law Assessment - Calendar.AI Hero Prompts

**Assessment Date**: 2025-11-10 18:48:43  
**Framework**: Verifier's Law by Jason Wei  
**Model Used**: GPT-5 (3 trials per prompt)  
**Prompts Assessed**: 9 / 9

---

## Executive Summary

**Verifier's Law**: "Any task that is possible to solve and easy to verify will eventually be solved by AI."

This assessment evaluates each Calendar.AI hero prompt on:
- **Solvability**: Can AI solve this task? (1-10)
- **Verification Ease**: How easy to verify correctness? (1-10)
- **Verification Asymmetry**: Gap between verification and solving difficulty
- **AI Readiness**: Timeline for AI capability (Now/Soon/Later/Never)
- **Training Data Quality**: Can we generate good training data? (1-10)

**Methodology**: Multiple GPT-5 trials were run per prompt to ensure robust, evidence-based assessments. Statistical measures (mean ± std, range) provide confidence in the rankings.

**Key Finding**: Prompts with high verification asymmetry (easy to verify, hard to solve) are prime candidates for AI automation and benefit most from RL fine-tuning with verification feedback.

---

## Rankings by Verifier's Law Priority


### 1. SCHEDULE-1 - 🥇 Tier 1 (High Priority)

**Composite Score**: 37.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 8/10 | Current AI systems can already integrate with calendar APIs (Google Calendar, Outlook) to create rec... |
| **Verification Ease** | 9/10 | Verification is straightforward: we can check if the created recurring event matches the specified c... |
| **Verification Asymmetry** | 7 | Score = 9 - 2 = 7 (Positive). This means the task is significantly easier to verify than to solve, which aligns with Verifier's Law as a high-priority AI target. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | We can generate synthetic data by simulating user prompts and expected calendar actions, and also co... |

**Verification Methods**:
- Compare scheduled event metadata (time, recurrence, duration) against parsed constraints
- Simulate declines and verify automatic rescheduling occurs within constraints
- User confirmation or automated test harness with expected outputs

**Key Insights**:
- High verification asymmetry makes this an ideal candidate for rapid AI improvement
- Most technical challenges are in robust preference interpretation and conflict handling
- Strong availability of APIs and structured calendar data accelerates development

**Recommendation**: HIGH priority for development. Focus on building a hybrid system: LLM for intent parsing + deterministic scheduling engine for constraint satisfaction. Implement automated verification harness to leverage easy validation for RL fine-tuning.

---

### 2. ORGANIZER-2 - 🥇 Tier 1 (High Priority)

**Composite Score**: 34.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current AI can access calendar APIs (Google, Outlook) to retrieve meeting metadata (titles, attendee... |
| **Verification Ease** | 9/10 | Verification is straightforward: we can check if flagged meetings match user feedback or historical ... |
| **Verification Asymmetry** | 6 | Positive asymmetry: verification is much easier than solving because correctness can be confirmed via user feedback or historical data, while solving requires nuanced interpretation of context and intent. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from historical calendars, user feedback, and organizati... |

**Verification Methods**:
- User feedback loop (approve/reject flagged meetings)
- Compare flagged meetings against historical prep time allocations
- Cross-check with meeting metadata (e.g., titles containing 'review', 'strategy')

**Key Insights**:
- Verification is trivial compared to solving, making this a strong candidate for AI automation per Verifier's Law.
- Personalization is the main complexity; generic models can achieve baseline performance quickly.
- Continuous feedback loop from user corrections will rapidly improve accuracy.

**Recommendation**: HIGH priority for development. Start with rule-based + LLM hybrid for initial deployment, then fine-tune with user feedback for personalization. Strong fit for Verifier's Law due to easy verification and moderate solving complexity.

---

### 3. COLLABORATE-1 - 🥇 Tier 1 (High Priority)

**Composite Score**: 34.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current LLMs can generate structured agendas from natural language prompts, especially when context ... |
| **Verification Ease** | 9/10 | Verifying an agenda is relatively easy because correctness can be judged by checking if it includes ... |
| **Verification Asymmetry** | 6 | Positive asymmetry: The task is moderately hard to solve (7/10) but very easy to verify (9/10). This means it's a strong candidate for AI improvement because feedback loops are cheap and reliable. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from historical meeting agendas, templates, and user fee... |

**Verification Methods**:
- Keyword/semantic matching against required topics (progress, blockers, risks)
- User feedback (thumbs up/down or edit acceptance)
- Comparison to historical agendas for similar meetings

**Key Insights**:
- Agenda generation is a text-structuring task with strong patterns, making it suitable for LLM fine-tuning.
- Verification is cheap and scalable via semantic checks and user feedback.
- Context integration (project status, team roles) is the main technical challenge, not language generation.

**Recommendation**: HIGH priority for AI development. Start with generic agenda generation using LLMs and progressively integrate organizational context via APIs. Leverage user feedback for rapid RLHF improvement.

---

### 4. SCHEDULE-2 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 30.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6/10 | The task involves multiple sub-steps: (1) interpreting 'Thursday afternoon' in the user's timezone, ... |
| **Verification Ease** | 9/10 | Verification is straightforward: we can check the calendar state before and after execution. Did all... |
| **Verification Asymmetry** | 5 | Score = 9 - 4 = 5 (Positive). This means the task is significantly easier to verify than to solve, which aligns with Verifier's Law as a high-priority candidate for AI automation. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 8/10 | We can generate synthetic data by simulating user requests and calendar states. Real-world data can ... |

**Verification Methods**:
- Compare event list before and after for Thursday afternoon
- Check new times for rescheduled events exist and are valid
- Verify RSVP statuses via API response
- Confirm user status field matches requested value

**Key Insights**:
- High verification asymmetry makes this an ideal RLHF candidate
- Complexity lies in multi-step reasoning and constraint satisfaction, not in API execution
- User preference and organizational norms are the hardest part to model
- Feedback loop is strong because calendar state provides objective ground truth

**Recommendation**: HIGH priority for AI development. Focus on building a reasoning layer for rescheduling logic and preference handling. Start with deterministic rule-based fallback for negotiation and gradually integrate LLM-based reasoning with RLHF using calendar state as the reward signal.

---

### 5. SCHEDULE-3 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 30.20

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6/10 | The task requires multi-constraint reasoning: finding a 1-hour slot within 2 weeks, prioritizing ove... |
| **Verification Ease** | 9/10 | Verification is straightforward: check if the scheduled event meets explicit constraints (participan... |
| **Verification Asymmetry** | 5 | Positive asymmetry: verification is much easier than solving. This means the task is a strong candidate for AI improvement because correctness can be quickly validated, enabling iterative refinement. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7.7/10 | High-quality training data can be generated from historical scheduling logs, synthetic scenarios, an... |

**Verification Methods**:
- Compare event participants to requested list
- Check event duration and date range
- Verify location field is a physical room
- Ensure no conflicts with Kat's schedule beyond allowed overrides
- Cross-check that the event exists in all participants' calendars

**Key Insights**:
- This is a classic constraint satisfaction problem with natural language front-end.
- Verification is almost trivial compared to solving, making it ideal for RLHF and self-play approaches.
- The main challenge is not algorithmic but integration: access to calendars, rooms, and organizational policies.
- Soft constraints (e.g., 'schedule over 1:1s if needed') require preference modeling and trade-off reasoning.

**Recommendation**: HIGH priority for AI development. Invest in building a constraint solver integrated with calendar APIs and fine-tune LLMs for interpreting scheduling instructions. Leverage easy verification for rapid iteration and RL-based improvement.

---

### 6. ORGANIZRE-3 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 29.20

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current AI can analyze calendar data, categorize events, and summarize time allocation using NLP and... |
| **Verification Ease** | 8/10 | Verification can be done by comparing AI-generated time breakdown with actual calendar data (objecti... |
| **Verification Asymmetry** | 5 | Score = 8 - 3 = +5 → Positive asymmetry: much easier to verify than to solve. This means the task is a strong candidate for AI improvement because correctness can be validated objectively while solution requires non-trivial reasoning. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 6.7/10 | We can generate synthetic data for time categorization and recommendations, but real-world labeled d... |

**Verification Methods**:
- Cross-check time allocation summary against raw calendar event durations
- User validation of identified top priorities and suggested changes
- A/B testing: measure user satisfaction and adoption of recommendations
- Heuristic checks: ensure recommendations reduce low-priority time blocks

**Key Insights**:
- Task has strong verification asymmetry, making it ideal for iterative AI improvement
- Main complexity lies in personalization and priority inference, not raw data processing
- Feedback loops from user validation can rapidly improve model performance
- Integration with calendar APIs is straightforward, but behavioral recommendations require careful UX design

**Recommendation**: HIGH priority for AI development. Start with accurate time categorization and visualization (easy win), then incrementally add priority inference and recommendation generation. Leverage user feedback for RLHF to refine suggestions.

---

### 7. COLLABORATE-2 - 🥉 Tier 3 (Lower Priority)

**Composite Score**: 26.75

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6.3/10 | Current LLMs (GPT-4, Claude, Gemini) can summarize documents and generate discussion points, but doi... |
| **Verification Ease** | 8/10 | Verification can be done by checking if the summary accurately reflects the meeting materials and if... |
| **Verification Asymmetry** | 4.3 | Positive asymmetry: The task is moderately hard to solve (6/10) but relatively easy to verify (8/10). This means it's a good candidate for AI improvement because correctness can be validated with automated and human-in-the-loop methods. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 6.7/10 | We can generate synthetic training data by simulating meeting summaries, objections, and responses u... |

**Verification Methods**:
- Semantic similarity scoring between generated summary and source materials
- Coverage metrics: Are all major agenda items represented?
- Human-in-the-loop evaluation for objection plausibility and response quality
- User feedback (thumbs up/down) after actual meeting outcomes

**Key Insights**:
- Task aligns well with Verifier's Law because verification is easier than generation
- Objection-response generation is the hardest subcomponent due to lack of explicit ground truth
- Calendar.AI can leverage user feedback loops to improve objection handling over time
- Integration with organizational knowledge bases will significantly boost performance

**Recommendation**: HIGH priority for development. Start with summarization and discussion point generation (already strong with current LLMs), then incrementally add objection modeling and response generation using RLHF and user feedback. Focus on building verification pipelines (semantic similarity, coverage checks, human review) to accelerate improvement.

---

### 8. COLLABORATE-3 - 🥉 Tier 3 (Lower Priority)

**Composite Score**: 26.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6/10 | The task requires multiple steps: (1) identify the upcoming meeting with customer Beta from the user... |
| **Verification Ease** | 8/10 | Verification is relatively straightforward because the output can be checked against known facts: co... |
| **Verification Asymmetry** | 4 | Positive score indicates the task is easier to verify than to solve, which aligns with Verifier's Law as a good candidate for AI improvement. The complexity is in data integration and reasoning, not in checking correctness. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | We can generate synthetic training data by simulating meeting briefs and dossiers using public compa... |

**Verification Methods**:
- Cross-check attendee list against calendar event metadata
- Validate company background against public sources (e.g., Wikipedia, company website)
- User feedback on relevance and correctness of topics
- Named entity matching for attendee dossiers

**Key Insights**:
- Task complexity is dominated by data integration and entity resolution, not language generation.
- Verification is easy because factual correctness and relevance can be objectively checked.
- User feedback provides a strong reinforcement signal for iterative improvement.
- This is a prime candidate for Verifier's Law acceleration due to high verification asymmetry.

**Recommendation**: HIGH priority for AI development. Focus on building robust data connectors and entity resolution pipelines, then leverage LLMs for summarization and dossier generation. Implement user feedback loops for rapid RLHF fine-tuning.

---

### 9. ORGANIZER-1 - 🥉 Tier 3 (Lower Priority)

**Composite Score**: 21.80

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 5/10 | The task requires interpreting user priorities (which may be implicit), mapping them to meeting meta... |
| **Verification Ease** | 8/10 | Verification is relatively straightforward: we can check if the meetings accepted align with a defin... |
| **Verification Asymmetry** | 3 | Positive asymmetry: verification is easier than solving, but not extremely skewed. This suggests moderate priority for AI development because correctness can be validated and used for iterative improvement. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 6.3/10 | We can collect historical calendar data and user decisions (accept/reject) as labeled examples. Howe... |

**Verification Methods**:
- Compare accepted meetings against user-defined priority tags
- User feedback loop (approve/reject decisions)
- Historical pattern matching (did the AI follow past behavior?)

**Key Insights**:
- Task difficulty lies in preference inference, not API integration
- Verification is easy because user feedback provides a clear signal
- Reinforcement learning from user corrections is a strong fit
- Synthetic data generation for priorities could bootstrap models

**Recommendation**: MEDIUM priority: Start with semi-automated approach (AI suggests, user confirms) to gather training data. Move toward full automation as preference models improve. Focus on building a feedback loop for continuous learning.

---

## Quick Comparison Table

| Rank | Prompt ID | Solvability | Verification | Asymmetry | Composite | Tier |
|------|-----------|-------------|--------------|-----------|-----------|------|
| 1 | schedule-1 | 8 | 9 | 7 | 37.5 | 🥇 |
| 2 | organizer-2 | 7 | 9 | 6 | 34.0 | 🥇 |
| 3 | collaborate-1 | 7 | 9 | 6 | 34.0 | 🥇 |
| 4 | schedule-2 | 6 | 9 | 5 | 30.5 | 🥈 |
| 5 | schedule-3 | 6 | 9 | 5 | 30.2 | 🥈 |
| 6 | organizre-3 | 7 | 8 | 5 | 29.2 | 🥈 |
| 7 | collaborate-2 | 6.3 | 8 | 4.3 | 26.7 | 🥉 |
| 8 | collaborate-3 | 6 | 8 | 4 | 26.0 | 🥉 |
| 9 | organizer-1 | 5 | 8 | 3 | 21.8 | 🥉 |

---

## Interpretation Guide

### Verification Asymmetry Score
- **Positive (>0)**: Easy to verify, harder to solve → **HIGH priority for AI** (benefits from verification feedback)
- **Near Zero (±2)**: Similar difficulty → **MEDIUM priority** (standard supervised learning)
- **Negative (<0)**: Hard to verify, easier to solve → **LOW priority** (verification bottleneck)

### AI Readiness Timeline
- **Now**: Can be solved with current AI + existing APIs
- **Soon (6 months)**: Needs minor capability improvements or data access
- **Later (1-2 years)**: Requires significant AI advances or infrastructure
- **Never**: Fundamentally unsuitable for AI (human judgment required)

### Training Data Quality
- **8-10**: High-quality ground truth easily available
- **5-7**: Moderate quality, requires effort to collect/label
- **1-4**: Poor quality, difficult to obtain reliable training signal

---

## Recommendations for Post-Training

Based on Verifier's Law, prioritize:

1. **Tier 1 Prompts** (Top 3): Implement verification-based RL fine-tuning
   - High asymmetry benefits from iterative improvement
   - Easy verification enables scalable training data generation
   
2. **Tier 2 Prompts** (Rank 4-6): Standard supervised fine-tuning
   - Moderate asymmetry, focus on quality over quantity
   
3. **Tier 3 Prompts** (Rank 7-9): Defer or use few-shot learning
   - Low asymmetry or hard verification limits training effectiveness

---

**Reference**: [Verifier's Law by Jason Wei](https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law)

