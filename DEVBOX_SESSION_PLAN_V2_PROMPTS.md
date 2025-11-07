# DevBox Session Plan - V2 Hero Prompts Analysis

**Date**: November 7, 2025  
**Platform**: Transition from macOS → Windows DevBox  
**Objective**: Analyze new v2 hero prompts with GPT-5 using 24 Canonical Tasks framework

---

## Current Status (macOS)

✅ **Completed Work**:
- Pulled latest changes from GitHub (30 files, 19,709 insertions)
- Identified 24 Canonical Unit Tasks framework (updated from 20)
- Located new hero prompts: `docs/9_hero_prompts_v2.txt`
- Identified analysis tool: `tools/analyze_prompt_with_gpt5.py`
- Verified GPT-5 infrastructure ready (MSAL + WAM via SilverFlow)

⚠️ **Blocked on macOS**:
- Cannot run GPT-5 analysis (requires Windows Broker authentication)
- GPT-5 requires: `dev-gpt-5-chat-jj` via SilverFlow LLM API
- Authentication: MSAL + Windows Broker (WAM) - Windows only

---

## New Hero Prompts v2

**File**: `docs/9_hero_prompts_v2.txt`

1. **Organizer-1**: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."
2. **Organizer-2**: "Track all my important meetings and flag any that require focus time to prepare for them."
3. **Organizer-3**: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities." *(Note: typo "Organizre-3" in file)*
4. **Schedule-1**: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."
5. **Schedule-2**: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."
6. **Schedule-3**: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."
7. **Collaborate-1**: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."
8. **Collaborate-2**: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."
9. **Collaborate-3**: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."

**Differences from v1**: Prompts are functionally identical, minor typo in Organizer-3.

---

## 24 Canonical Tasks Framework

**Current Framework**: Calendar.AI Canonical Unit Tasks Framework v2.0

**Key References**:
- `docs/gutt_analysis/CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md` (2,142 lines) - Authoritative gold standard
- `docs/gutt_analysis/CANONICAL_UNIT_TASKS_REFERENCE.md` (1,166 lines) - Complete specifications
- `docs/gutt_analysis/CANONICAL_TASKS_CAPABILITY_INVENTORY.md` - Implementation details

**Framework Statistics**:
- **24 Total Tasks** (23 unique + CAN-02A/CAN-02B split)
- **3 Tiers**: Universal (5), Common (9), Specialized (10)
- **Average Usage**: 7.8 tasks per prompt
- **100% Tier 1 coverage** across all prompts

**Top Tasks (100% frequency)**:
- CAN-04: Natural Language Understanding
- CAN-01: Calendar Events Retrieval
- CAN-07: Meeting Metadata Extraction

**Critical Split**:
- CAN-02A: Meeting Type Classification
- CAN-02B: Meeting Importance Assessment

---

## DevBox Tasks - Next Session

### Priority 1: Run GPT-5 Analysis on v2 Prompts ⭐

**Tool**: `tools/analyze_prompt_with_gpt5.py`

**Command**:
```bash
# On DevBox
cd /path/to/scenara
git pull origin master

# Run analysis for all 9 v2 prompts
python tools/analyze_prompt_with_gpt5.py
```

**Expected Outputs**:
1. JSON results: `docs/gutt_analysis/gpt5_canonical_analysis_v2_YYYYMMDD_HHMMSS.json`
2. Markdown report: `docs/gutt_analysis/GPT5_Canonical_Analysis_Report_v2_YYYYMMDD_HHMMSS.md`

**Analysis Includes**:
- Canonical task identification for each prompt
- Coverage analysis (Tier 1/2/3 usage)
- Implementation effort estimates
- Execution sequence planning
- Data flow diagrams

### Priority 2: Compare v1 vs v2 Results

**Compare**:
- v1 results: `docs/gutt_analysis/gpt5_canonical_analysis_20251106_230413.json`
- v2 results: (to be generated)

**Focus Areas**:
- Task selection differences
- Coverage percentage changes
- Effort estimate variations
- New insights from v2 prompts

### Priority 3: Update Gold Standard if Needed

If v2 prompts reveal new patterns:
- Update `CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md`
- Add v2-specific insights
- Document any framework refinements

---

## Files to Sync to DevBox

### New/Updated Files (Uncommitted):
- ✅ `docs/9_hero_prompts_v2.txt` - New hero prompts (will be committed)
- ✅ `DEVBOX_SESSION_PLAN_V2_PROMPTS.md` - This file (will be committed)

### Existing Analysis Tools (Already on DevBox):
- ✅ `tools/analyze_prompt_with_gpt5.py` - GPT-5 canonical task analyzer
- ✅ `tools/meeting_classifier_gpt5.py` - SilverFlow authentication
- ✅ `docs/gutt_analysis/CANONICAL_TASKS_GOLD_STANDARD_REFERENCE.md` - 24 tasks reference

---

## Git Workflow

```bash
# On macOS (now)
git add docs/9_hero_prompts_v2.txt DEVBOX_SESSION_PLAN_V2_PROMPTS.md
git commit -m "Add v2 hero prompts and DevBox session plan for GPT-5 analysis"
git push origin master

# On DevBox (next)
git pull origin master
python tools/analyze_prompt_with_gpt5.py
# ... analyze results ...
git add docs/gutt_analysis/gpt5_canonical_analysis_v2_*.json
git add docs/gutt_analysis/GPT5_Canonical_Analysis_Report_v2_*.md
git commit -m "Complete GPT-5 analysis of v2 hero prompts with 24 canonical tasks"
git push origin master
```

---

## Expected Analysis Results

Based on 24 Canonical Tasks framework:

**Per-Prompt Metrics**:
- Canonical tasks identified: 6-10 per prompt
- Tier distribution: ~60% Tier 1, ~30% Tier 2, ~10% Tier 3
- Coverage: 85-95% (most tasks already implemented)
- Effort: Varies by prompt complexity

**Key Insights Expected**:
1. Task composition patterns (sequential vs parallel)
2. Orchestration requirements (error handling, retries)
3. Data flow dependencies
4. Implementation priority recommendations

---

## Success Criteria

✅ **v2 Analysis Complete**:
- All 9 prompts analyzed with GPT-5
- JSON + Markdown reports generated
- Results committed to GitHub

✅ **Comparison Analysis**:
- v1 vs v2 differences documented
- Framework validation confirmed
- Any new canonical tasks identified

✅ **Documentation Updated**:
- `.cursorrules` updated with v2 session summary
- Daily interaction logger entries created
- Session logs committed

---

## Notes

- v2 prompts are essentially same as v1 (minor typo differences)
- Focus on validating 24 canonical tasks framework consistency
- GPT-5 proven stable: F1 78.40% ± 0.72% (3-trial test)
- All 24 tasks should be represented across 9 prompts
- CAN-02A/CAN-02B split should appear in most prompts

---

**Next Action**: Switch to Windows DevBox and pull latest code  
**Estimated Time**: 15-20 minutes for complete GPT-5 analysis  
**Platform**: Windows DevBox with SilverFlow LLM API access
