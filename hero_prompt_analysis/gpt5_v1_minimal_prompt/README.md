# GPT-5 GUTT Analysis v1 - Minimal Prompt (November 6, 2025)

## Overview

This directory contains GPT-5 GUTT decomposition results using a **minimal prompt** without full GUTT framework documentation.

**Date**: November 6, 2025  
**Model**: dev-gpt-5-chat-jj (Microsoft SilverFlow LLM API)  
**Prompt Type**: Minimal context (v1)  
**Status**: ⚠️ Not comparable to Claude/Ollama (different prompt context)

## Prompt Difference

### What GPT-5 v1 Received

**System Message** (Brief):
```
You are an expert at decomposing complex prompts into atomic Granular Unit Task Taxonomy (GUTT) components.

GUTT Framework (v4.0 ACRUE):
- Each GUTT represents ONE atomic, indivisible unit task
- GUTTs must be granular enough that each can be independently implemented
- Each GUTT has: unique ID, name, capability description, required skills, user goal, triggered status, evidence

Your task:
1. Analyze the prompt and identify ALL atomic unit tasks required
2. Decompose to the finest granularity - each GUTT should be ONE specific action/capability
3. Do NOT group related tasks - keep them as separate GUTTs
4. Ensure GUTTs are sequenced logically if they have dependencies
```

### What Claude/Ollama Received

**System Message** (Full Context):
- Complete GUTT v4.0 ACRUE Integration Documentation (first 1000 chars)
- Hero Prompts Reference GUTT Decompositions (first 1000 chars)
- Detailed granularity guidelines with examples
- Self-check instructions to avoid over/under-decomposition

## Results Summary (v1)

**Total GUTTs Generated**: 90 (vs Reference: 66)  
**Pattern**: Over-decomposition (+36% more GUTTs than reference)

| Prompt ID | v1 GUTTs | Reference | Difference |
|-----------|----------|-----------|------------|
| organizer-1 | 9 | 6 | +3 |
| organizer-2 | 6 | 7 | -1 |
| organizer-3 | 9 | 8 | +1 |
| schedule-1 | 14 | 7 | +7 🔥 |
| schedule-2 | 8 | 8 | 0 ✅ |
| schedule-3 | 17 | 9 | +8 🔥 |
| collaborate-1 | 11 | 6 | +5 |
| collaborate-2 | 7 | 7 | 0 ✅ |
| collaborate-3 | 9 | 8 | +1 |
| **TOTAL** | **90** | **66** | **+24** |

## Analysis

### Over-Decomposition Pattern

GPT-5 v1 generated **36% more GUTTs** than the reference decomposition. This likely occurred because:

1. **Emphasis on "finest granularity"** in minimal prompt
2. **Instruction to "do NOT group related tasks"**
3. **Missing context** about appropriate granularity level from full documentation
4. **No examples** of proper decomposition to calibrate against

### Comparison Impact

**Not Comparable**: These results should NOT be directly compared to Claude/Ollama because:
- Different prompt context provided
- Missing GUTT framework calibration documentation
- Different granularity guidelines

### Next Steps

**GPT-5 v2** will be run with:
- Full GUTT v4.0 ACRUE Integration Documentation
- Hero Prompts Reference GUTT Decompositions
- Same context as Claude/Ollama analyzers
- Results saved to `../` (main directory) as authoritative GPT-5 analysis

## Files in This Directory

- `gpt5_gutt_organizer-1.json` - Calendar Prioritization (9 GUTTs)
- `gpt5_gutt_organizer-2.json` - Meeting Prep Tracking (6 GUTTs)
- `gpt5_gutt_organizer-3.json` - Time Reclamation (9 GUTTs)
- `gpt5_gutt_schedule-1.json` - Recurring 1:1 Scheduling (14 GUTTs)
- `gpt5_gutt_schedule-2.json` - Block Time & Reschedule (8 GUTTs)
- `gpt5_gutt_schedule-3.json` - Multi-Person Scheduling (17 GUTTs)
- `gpt5_gutt_collaborate-1.json` - Agenda Creation (11 GUTTs)
- `gpt5_gutt_collaborate-2.json` - Executive Briefing Prep (7 GUTTs)
- `gpt5_gutt_collaborate-3.json` - Customer Meeting Prep (9 GUTTs)
- `gpt5_v1_batch_summary.json` - Batch analysis summary

## Conclusion

These v1 results demonstrate that **prompt context significantly impacts GUTT decomposition**:
- Minimal context → Over-decomposition (90 GUTTs)
- Full documentation context → Expected to align better with reference (66 GUTTs)

This validates the importance of providing comprehensive framework documentation to LLM analyzers.

---

**Next**: See parent directory for GPT-5 v2 results with full GUTT documentation context.
