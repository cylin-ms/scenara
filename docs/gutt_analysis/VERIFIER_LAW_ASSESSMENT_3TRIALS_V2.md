# Verifier's Law Assessment - Calendar.AI Hero Prompts

**Assessment Date**: 2025-11-10 18:43:48  
**Framework**: Verifier's Law by Jason Wei  
**Model Used**: GPT-5 (3 trials per prompt)  
**Prompts Assessed**: 1 / 9

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


### 1. COLLABORATE-3 - 🥇 Tier 1 (High Priority)

**Composite Score**: 26.00

| Metric | Score | Details |
|--------|-------|---------|
| **Solvability** | 6/10 | The task requires multiple steps: (1) identify the upcoming meeting with customer Beta from the cale... |
| **Verification Ease** | 8/10 | Verification is relatively straightforward because the output can be checked against known facts: at... |
| **Verification Asymmetry** | 4 | Positive asymmetry: verification (8) is easier than solving (6), meaning this is a good candidate for AI improvement because correctness can be validated quickly while solving requires orchestration and reasoning. |
| **AI Readiness** | Soon (6mo) | Blockers: 3 |
| **Training Data Quality** | 7/10 | We can generate synthetic briefs from historical meeting notes and CRM data, and use human-in-the-lo... |

**Verification Methods**:
- Cross-check attendee list against calendar event metadata
- Validate company background against external APIs (e.g., Clearbit, Crunchbase)
- Check for presence of required sections: meeting summary, attendee dossiers, topics of interest
- User feedback loop for factual accuracy and relevance

**Key Insights**:
- Task complexity lies in data integration and personalization, not in text generation
- Verification is easy because factual checks and structural validation are straightforward
- Positive verification asymmetry makes this a strong candidate for iterative AI improvement
- Privacy and compliance are major non-technical blockers

**Recommendation**: HIGH priority for development. Focus on building robust data pipelines and entity resolution first, then fine-tune LLMs for structured brief generation. Implement automated verification checks and user feedback loops to accelerate RLHF.

---

## Quick Comparison Table

| Rank | Prompt ID | Solvability | Verification | Asymmetry | Composite | Tier |
|------|-----------|-------------|--------------|-----------|-----------|------|
| 1 | collaborate-3 | 6 | 8 | 4 | 26.0 | 🥇 |

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

