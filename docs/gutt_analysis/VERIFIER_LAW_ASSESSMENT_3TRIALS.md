# Verifier's Law Assessment - Calendar.AI Hero Prompts

**Assessment Date**: 2025-11-10 18:36:46  
**Framework**: Verifier's Law by Jason Wei  
**Model Used**: GPT-5 (2 trials per prompt)  
**Prompts Assessed**: 7 / 9

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
| **Verification Ease** | 9/10 | Verification is straightforward: we can check if the scheduled event meets all stated constraints (w... |
| **Verification Asymmetry** | 7 | Positive asymmetry: The task is moderately hard to solve (8/10 solvability) but extremely easy to verify (9/10). This means it's a strong candidate for AI automation because correctness can be objectively checked. |
| **AI Readiness** | Now | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from historical scheduling logs, synthetic data (varied ... |

**Verification Methods**:
- Compare scheduled event metadata against parsed constraints
- Simulate conflict scenarios and verify automatic rescheduling
- Check recurrence pattern and time slots against 'afternoons' and 'avoid Fridays' rules
- User confirmation feedback loop

**Key Insights**:
- Scheduling tasks exhibit strong verification asymmetry: easy to check, harder to solve.
- Calendar APIs provide structured ground truth, enabling automated evaluation and reinforcement learning.
- Dynamic rescheduling introduces complexity but is still verifiable through simulation.

**Recommendation**: HIGH priority for AI development. This task aligns perfectly with Verifier's Law: solvable with current tech, easy to verify, and high user value. Focus on robust NLP for constraint parsing and conflict resolution logic. Implement automated evaluation pipelines for rapid iteration.

---

### 2. ORGANIZER-2 - 🥇 Tier 1 (High Priority)

**Composite Score**: 34.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current AI systems can access calendar APIs (Google, Outlook) to retrieve meeting metadata (titles, ... |
| **Verification Ease** | 9/10 | Verification is straightforward because the ground truth can be obtained from user feedback (e.g., t... |
| **Verification Asymmetry** | 6 | Positive asymmetry: verification is much easier than solving because correctness can be quickly validated by user feedback, while solving requires nuanced reasoning and personalization. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated through user feedback loops and historical calendar data... |

**Verification Methods**:
- Direct user feedback on flagged meetings
- Comparison with user-defined tags or categories
- A/B testing: measure user engagement and satisfaction
- Retrospective analysis of whether flagged meetings correlate with actual preparation time

**Key Insights**:
- Verification is trivial compared to solving, making this an ideal candidate for RLHF (Reinforcement Learning from Human Feedback).
- Personalization is the main technical challenge, not data access.
- Cold-start can be mitigated with general heuristics (e.g., meetings with executives or external clients likely require prep).

**Recommendation**: HIGH priority for AI development. Start with heuristic + ML hybrid approach, then fine-tune with user feedback. Leverage verification asymmetry to rapidly improve models through reinforcement learning.

---

### 3. COLLABORATE-1 - 🥇 Tier 1 (High Priority)

**Composite Score**: 34.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current LLMs can generate structured agendas from natural language prompts, especially when context ... |
| **Verification Ease** | 9/10 | Verifying an agenda is straightforward: check if it includes key elements (progress review, confirma... |
| **Verification Asymmetry** | 6 | Positive asymmetry: The task is moderately hard to solve (7/10 solvability) but very easy to verify (9/10). This means it's a strong candidate for AI improvement because feedback loops are cheap and reliable. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from historical meeting agendas, templates, and user edi... |

**Verification Methods**:
- Keyword/semantic matching for required topics (progress, risks, blockers)
- User approval or edit tracking
- Comparison against historical agendas for similar meetings
- LLM-based rubric scoring for completeness and clarity

**Key Insights**:
- Agenda generation is a natural language structuring task with strong verification signals.
- User feedback provides a low-cost, high-quality reinforcement signal.
- Context integration (project status, prior meetings) is the main complexity driver.
- This task aligns well with Verifier's Law: easy verification accelerates AI progress.

**Recommendation**: HIGH priority for development. Start with context-light agenda generation using LLMs and calendar APIs, then progressively integrate project management data for richer agendas. Leverage user feedback for RLHF fine-tuning.

---

### 4. ORGANIZRE-3 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 29.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current AI can analyze calendar data, categorize events, and summarize time allocation using NLP and... |
| **Verification Ease** | 8/10 | Verification can be done by comparing AI-generated time breakdowns against actual calendar data (obj... |
| **Verification Asymmetry** | 5 | Positive asymmetry: The task is moderately hard to solve (7/10 solvability) but quite easy to verify (8/10). This means it's a good candidate for AI improvement because feedback loops are strong. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | We can generate synthetic data by simulating calendars and labeling priorities, and collect real-wor... |

**Verification Methods**:
- Cross-check time allocation summary with raw calendar event durations
- Validate categorization accuracy against labeled event types
- User feedback on whether suggested changes align with their priorities
- A/B testing: measure adoption of suggested changes

**Key Insights**:
- Verification is straightforward because calendar data provides ground truth for time allocation.
- The main challenge is inferring 'top priorities' and generating contextually relevant suggestions.
- Strong feedback loops make this an ideal candidate for RLHF (Reinforcement Learning from Human Feedback).
- Privacy and security considerations are critical for deployment.

**Recommendation**: HIGH priority for AI development. Focus on building a pipeline that combines calendar data analysis, user preference modeling, and suggestion generation. Start with explicit user input for priorities, then evolve toward implicit inference using historical patterns and feedback.

---

### 5. COLLABORATE-2 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 26.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6/10 | Current LLMs (GPT-4, Claude, Gemini) can summarize documents and generate discussion points, but doi... |
| **Verification Ease** | 8/10 | Verification can be done by checking if the summary accurately reflects the meeting materials and if... |
| **Verification Asymmetry** | 4 | Positive asymmetry: The task is moderately hard to solve (6/10) but quite easy to verify (8/10). This means it's a good candidate for iterative AI improvement because user feedback and automated checks can provide strong training signals. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | We can generate synthetic training data for summarization and objection-response pairs using LLMs an... |

**Verification Methods**:
- Semantic similarity scoring between summary points and source materials
- Human-in-the-loop feedback (thumbs up/down on suggestions)
- Fact-checking responses against provided documents
- Measuring coverage of key terms/topics from the original materials

**Key Insights**:
- Verification is straightforward because summaries can be compared to source materials and objections can be judged for plausibility.
- The main challenge is contextual alignment with leadership priorities, which requires either fine-tuning on domain-specific data or user-in-the-loop refinement.
- This task benefits strongly from RLHF because user feedback on suggestions is easy to collect and highly informative.

**Recommendation**: High-priority for AI development. Focus on building a pipeline that combines document summarization with objection-response generation, leveraging user feedback for rapid iteration. Start with a 'Now' MVP using generic business heuristics and improve with contextual fine-tuning.

---

### 6. COLLABORATE-3 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 26.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6/10 | The task requires multiple steps: (1) identifying the correct meeting and attendees from the calenda... |
| **Verification Ease** | 8/10 | Verification is relatively straightforward because the output can be checked against known facts: (a... |
| **Verification Asymmetry** | 4 | Positive asymmetry: verification is easier than solving because correctness can be checked against structured data and public sources, while solving requires multi-source integration and summarization. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | Synthetic training data can be generated by pairing real meeting briefs with CRM and company data. H... |

**Verification Methods**:
- Cross-check company background against public sources (LinkedIn, Crunchbase)
- Validate attendee names against calendar event
- Check dossier completeness (one per attendee)
- Keyword matching for known interest topics from CRM/email metadata

**Key Insights**:
- Task complexity lies in data integration, not language generation
- Verification benefits from structured data cross-checks
- Interest profiling is the weakest link due to sparse and private data
- LLMs can handle summarization and brief generation well once data is available

**Recommendation**: High-priority for AI development because verification is easy and solving is moderately hard. Focus on building robust data integration pipelines and entity resolution first, then fine-tune LLMs for structured-to-text generation. Start with company background and attendee list, then progressively add interest profiling.

---

### 7. ORGANIZER-1 - 🥉 Tier 3 (Lower Priority)

**Composite Score**: 21.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 5/10 | The task requires understanding user priorities (which are often implicit), interpreting meeting con... |
| **Verification Ease** | 8/10 | Verification is relatively straightforward: we can check if the meetings accepted or declined align ... |
| **Verification Asymmetry** | 3 | Positive asymmetry: verification is easier than solving, but not extremely so. This suggests moderate leverage for AI improvement through feedback loops. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 6/10 | We can generate labeled data from historical calendars where users marked meetings as important or d... |

**Verification Methods**:
- Compare scheduled meetings against explicit user-defined priority tags or lists
- User feedback loop (approve/reject AI decisions)
- Historical analysis: Did AI accept meetings previously marked as important by the user?

**Key Insights**:
- The hardest part is modeling implicit user priorities, not the mechanics of scheduling.
- Verification is easy because correctness is binary: did the AI schedule only priority meetings?
- This task benefits from iterative RLHF (Reinforcement Learning from Human Feedback) because user feedback is cheap and high-signal.

**Recommendation**: MEDIUM priority for development. Start with explicit priority tagging and rule-based filters, then incrementally add LLM-based reasoning for implicit priorities. Build strong feedback loops for continuous improvement.

---

## Quick Comparison Table

| Rank | Prompt ID | Solvability | Verification | Asymmetry | Composite | Tier |
|------|-----------|-------------|--------------|-----------|-----------|------|
| 1 | schedule-1 | 8 | 9 | 7 | 37.5 | 🥇 |
| 2 | organizer-2 | 7 | 9 | 6 | 34.0 | 🥇 |
| 3 | collaborate-1 | 7 | 9 | 6 | 34.0 | 🥇 |
| 4 | organizre-3 | 7 | 8 | 5 | 29.5 | 🥈 |
| 5 | collaborate-2 | 6 | 8 | 4 | 26.0 | 🥈 |
| 6 | collaborate-3 | 6 | 8 | 4 | 26.0 | 🥈 |
| 7 | organizer-1 | 5 | 8 | 3 | 21.5 | 🥉 |

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

