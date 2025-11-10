# Verifier's Law Assessment - Calendar.AI Hero Prompts

**Assessment Date**: 2025-11-10 18:26:01  
**Framework**: Verifier's Law by Jason Wei  
**Model Used**: GPT-5  
**Prompts Assessed**: 5 / 9

---

## Executive Summary

**Verifier's Law**: "Any task that is possible to solve and easy to verify will eventually be solved by AI."

This assessment evaluates each Calendar.AI hero prompt on:
- **Solvability**: Can AI solve this task? (1-10)
- **Verification Ease**: How easy to verify correctness? (1-10)
- **Verification Asymmetry**: Gap between verification and solving difficulty
- **AI Readiness**: Timeline for AI capability (Now/Soon/Later/Never)
- **Training Data Quality**: Can we generate good training data? (1-10)

**Key Finding**: Prompts with high verification asymmetry (easy to verify, hard to solve) are prime candidates for AI automation and benefit most from RL fine-tuning with verification feedback.

---

## Rankings by Verifier's Law Priority


### 1. COLLABORATE-1 - 🥇 Tier 1 (High Priority)

**Composite Score**: 40.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current LLMs can generate structured agendas from natural language prompts, especially when context ... |
| **Verification Ease** | 9/10 | Verifying an agenda is relatively easy because correctness is subjective but bounded by clear expect... |
| **Verification Asymmetry** | 8 | Positive and significant: The task is moderately hard to solve well (score 7) but very easy to verify (score 9). This means it fits Verifier's Law strongly—AI will improve rapidly here because feedback loops are cheap and reliable. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from historical meeting agendas, templates, and syntheti... |

**Verification Methods**:
- Automated semantic check for required topics (progress, confirmation, risks)
- User thumbs-up/down feedback after agenda generation
- Comparison against a reference set of good agendas for similar prompts

**Key Insights**:
- Agenda generation is a classic example of a task that is easy to verify but moderately hard to solve well.
- Integration with organizational data is the main barrier to high-quality outputs.
- User feedback provides a strong reinforcement signal for iterative improvement.
- This task aligns perfectly with Verifier's Law—expect rapid AI progress once feedback loops are in place.

**Recommendation**: HIGH priority for development. Start with generic agenda generation using LLMs and progressively integrate project context and organizational norms. Implement user feedback collection for RLHF to accelerate quality improvements.

---

### 2. SCHEDULE-1 - 🥇 Tier 1 (High Priority)

**Composite Score**: 37.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 8/10 | Current AI systems can already integrate with calendar APIs (Google Calendar, Outlook) to create rec... |
| **Verification Ease** | 9/10 | Verification is straightforward: we can check if a recurring 30-min meeting exists starting next wee... |
| **Verification Asymmetry** | 7 | Positive asymmetry: verification is much easier than solving because correctness can be checked with simple calendar queries, while solving requires multi-step reasoning and preference handling. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from historical scheduling logs, synthetic prompts, and ... |

**Verification Methods**:
- Compare scheduled events against user constraints (time of day, day of week)
- Check recurrence pattern and start date
- Simulate a decline and verify that a new slot is scheduled automatically
- Cross-check with both participants' calendars for conflicts

**Key Insights**:
- This task is a classic example of Verifier's Law: easy to verify (calendar state) but harder to solve (multi-party preference negotiation).
- Automation of rescheduling after declines is the most complex subtask, requiring event-driven logic and preference inference.
- Strong potential for RLHF or self-play simulation using synthetic calendars to improve performance.

**Recommendation**: HIGH priority for AI development. Focus on building a constraint-satisfaction engine integrated with LLM-based natural language parsing, and leverage easy verification for rapid iteration and RL fine-tuning.

---

### 3. ORGANIZER-2 - 🥇 Tier 1 (High Priority)

**Composite Score**: 34.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current AI can access calendar APIs (Google, Outlook) to retrieve meeting metadata (titles, attendee... |
| **Verification Ease** | 9/10 | Verification is straightforward because ground truth can be obtained from user feedback (e.g., user ... |
| **Verification Asymmetry** | 6 | Positive asymmetry: The task is moderately hard to solve (7/10 solvability) but very easy to verify (9/10). This means it's a strong candidate for AI improvement because feedback loops are cheap and reliable. |
| **AI Readiness** | Soon (6mo) | Blockers: 2 |
| **Training Data Quality** | 8/10 | High-quality training data can be generated from user feedback and historical calendar data. Many or... |

**Verification Methods**:
- User feedback loop (approve/reject flagged meetings)
- Comparison against historical patterns of user preparation
- A/B testing with user satisfaction metrics

**Key Insights**:
- Verification is cheap and scalable via user feedback loops, making RLHF viable.
- The main complexity lies in personalization and context inference, not in API integration.
- This task aligns well with Verifier's Law: easy verification accelerates AI progress.

**Recommendation**: HIGH priority for development. Start with rule-based + ML hybrid approach (e.g., keyword heuristics + LLM classification) and integrate user feedback for rapid improvement. Focus on personalization and context enrichment for long-term accuracy.

---

### 4. COLLABORATE-2 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 29.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 7/10 | Current LLMs (GPT-4, Claude, Gemini) can summarize meeting materials and generate discussion points ... |
| **Verification Ease** | 8/10 | Verification is relatively easy because the output can be checked against the source materials and j... |
| **Verification Asymmetry** | 5 | Positive asymmetry: Verification (8) is easier than solving (7 difficulty → 10-7=3; 8-3=5). This means the task is harder to solve than to verify, making it a strong candidate for AI improvement under Verifier's Law. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | We can generate synthetic training data by simulating meeting materials and leadership scenarios, an... |

**Verification Methods**:
- Semantic similarity scoring between suggested points and meeting materials
- Human-in-the-loop rating for relevance and tone
- Checklist: Are there exactly three points? Do they cover major agenda items?
- Objection plausibility scoring using LLM-based critique models

**Key Insights**:
- Task aligns well with Verifier's Law: easy to verify, moderately hard to solve
- Strong feedback loop potential via user ratings on summaries and objection handling
- Contextual grounding (org priorities, tone) is the main challenge, not core summarization
- High strategic value for Calendar.AI as it moves from scheduling to meeting intelligence

**Recommendation**: HIGH priority for development. Start with summarization and objection-generation MVP using current LLMs, integrate user feedback for RLHF, and progressively add organizational context tuning. Verification pipeline is straightforward, enabling rapid iteration.

---

### 5. ORGANIZER-1 - 🥈 Tier 2 (Medium Priority)

**Composite Score**: 22.50

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 5/10 | The task requires understanding user priorities (which are often implicit and dynamic), interpreting... |
| **Verification Ease** | 8/10 | Verification is relatively straightforward: we can check if the meetings accepted by the AI align wi... |
| **Verification Asymmetry** | 3 | Positive asymmetry: verification is easier than solving. This means the task fits Verifier's Law and is a good candidate for AI improvement over time. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | We can generate synthetic data by simulating user priorities and meeting metadata. Real-world data c... |

**Verification Methods**:
- Compare accepted meetings against explicit priority tags or categories
- User feedback loop (approve/reject AI decisions)
- Audit logs of scheduling decisions vs. user-stated preferences

**Key Insights**:
- The main challenge is preference inference, not API integration.
- Verification is easy because user feedback provides a strong ground truth signal.
- This task is ideal for RLHF (Reinforcement Learning from Human Feedback) due to clear accept/reject signals.
- Privacy-preserving personalization will be critical for adoption.

**Recommendation**: HIGH priority for AI development. Start with rule-based + LLM hybrid system using explicit priority lists, then evolve to preference-learning models with user feedback. Leverage easy verification for rapid iteration.

---

## Quick Comparison Table

| Rank | Prompt ID | Solvability | Verification | Asymmetry | Composite | Tier |
|------|-----------|-------------|--------------|-----------|-----------|------|
| 1 | collaborate-1 | 7 | 9 | 8 | 40.0 | 🥇 |
| 2 | schedule-1 | 8 | 9 | 7 | 37.5 | 🥇 |
| 3 | organizer-2 | 7 | 9 | 6 | 34.0 | 🥇 |
| 4 | collaborate-2 | 7 | 8 | 5 | 29.5 | 🥈 |
| 5 | organizer-1 | 5 | 8 | 3 | 22.5 | 🥈 |

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

