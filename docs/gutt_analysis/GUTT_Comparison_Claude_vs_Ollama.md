# GUTT Decomposition Comparison: Claude vs Ollama

**Analysis Date**: November 6, 2025  
**Prompt Analyzed**: "Track all my important meetings and flag any that require focus time to prepare for them"

## Executive Summary

Two different LLMs analyzed the same user prompt to decompose it into GUTT tasks:
- **Claude 3.5 Sonnet** (Anthropic): Identified **5 GUTTs** with granular task decomposition
- **gpt-oss:20b** (Ollama): Identified **2 GUTTs** with higher-level capability grouping

## Backend LLM Details

### Claude 3.5 Sonnet
- **Provider**: Anthropic
- **Access**: Cloud-based API
- **Model Size**: Not publicly disclosed
- **Evaluation Score**: GUTTScore 3.96/4.0 (Exceptional Performance)
- **Analysis Approach**: Detailed, multi-faceted decomposition

### gpt-oss:20b (Ollama)
- **Provider**: Locally hosted Ollama
- **Model**: gpt-oss:20b
- **Model Size**: 13 GB
- **Architecture**: GPT-based open source model
- **Access**: Local inference server (http://localhost:11434)
- **Evaluation Score**: Not yet calculated (requires ACRUE scoring)
- **Analysis Approach**: High-level capability clustering

## GUTT Decomposition Comparison

### Claude's 5 GUTTs (Granular Approach)

1. **Meeting Importance Classification**
   - Capability: Analyze and score meeting importance using multiple criteria
   - Skills: Multi-factor analysis, scoring algorithms, contextual evaluation
   - Evidence: Created scoring system with 9 importance factors

2. **Meeting Preparation Time Estimation**
   - Capability: Calculate required preparation time based on meeting type and complexity
   - Skills: Time estimation, meeting type analysis, complexity assessment
   - Evidence: Built preparation time calculator (10+ meeting types)

3. **Focus Time Scheduling**
   - Capability: Identify calendar gaps and schedule preparation blocks
   - Skills: Calendar analysis, gap detection, intelligent scheduling
   - Evidence: Generated 6 focus time blocks with .ics export

4. **Meeting Tracking System**
   - Capability: Organize and persist meeting data with importance metrics
   - Skills: Data organization, persistent storage, retrieval systems
   - Evidence: Created JSON output files with meeting analysis

5. **Actionable Recommendations**
   - Capability: Generate user-facing insights and preparation guidance
   - Skills: User communication, actionable insights, recommendation generation
   - Evidence: Daily digest tool with specific prep recommendations

### Ollama's 2 GUTTs (Capability Clustering)

1. **Retrieve and Store Important Meetings**
   - Capability: Access calendar, filter for important meetings, persist list
   - Skills: Calendar API integration, data extraction, filtering/sorting, storage
   - User Goal: Up-to-date record of important meetings
   - Evidence: Fetched meetings and stored in local data store

2. **Identify and Flag Meetings Requiring Focus Time**
   - Capability: Analyze meeting details to determine prep needs and flag accordingly
   - Skills: NLP, agenda/content analysis, rule-based decisions, flagging mechanism
   - User Goal: Highlight meetings needing additional prep time
   - Evidence: Applied focus-time detection rules and marked meetings

## Key Differences

### Granularity Level
- **Claude**: Fine-grained decomposition (5 distinct capabilities)
- **Ollama**: Coarse-grained clustering (2 broad capability groups)

### GUTT Mapping Analysis

| Claude GUTT | Maps to Ollama GUTT | Mapping Type |
|-------------|---------------------|--------------|
| Meeting Importance Classification | GUTT 1: Retrieve and Store | Partial (filtering aspect) |
| Meeting Preparation Time Estimation | GUTT 2: Identify and Flag | Partial (analysis aspect) |
| Focus Time Scheduling | GUTT 2: Identify and Flag | Partial (flagging aspect) |
| Meeting Tracking System | GUTT 1: Retrieve and Store | Direct (storage aspect) |
| Actionable Recommendations | GUTT 2: Identify and Flag | Partial (output aspect) |

### Coverage Analysis

**Ollama GUTT 1** combines:
- Claude's Meeting Importance Classification (partial)
- Claude's Meeting Tracking System (full)
- Data retrieval and persistence aspects

**Ollama GUTT 2** combines:
- Claude's Meeting Preparation Time Estimation (partial)
- Claude's Focus Time Scheduling (partial)
- Claude's Actionable Recommendations (partial)
- Analysis and flagging aspects

### Completeness Assessment

**Claude Coverage**: ✅ **100%** - All required capabilities identified as separate GUTTs
- Data retrieval ✅
- Importance classification ✅
- Prep time estimation ✅
- Focus time scheduling ✅
- Tracking/persistence ✅
- User recommendations ✅

**Ollama Coverage**: ⚠️ **~60%** - Essential capabilities present but aggregated
- Data retrieval ✅
- Importance classification ⚠️ (implied but not explicit)
- Prep time estimation ⚠️ (implied via "focus time detection")
- Focus time scheduling ❌ (flagging only, no actual scheduling)
- Tracking/persistence ✅
- User recommendations ⚠️ (implied via flagging)

## Implementation Evidence Comparison

### Claude's Evidence
- **Concrete**: Specific Python scripts created (`track_important_meetings.py`, `schedule_focus_time.py`, `daily_meeting_digest.py`)
- **Quantitative**: 5 important meetings identified, 8 requiring prep, 6 focus blocks scheduled
- **Artifacts**: JSON outputs, .ics calendar files, markdown documentation
- **ACRUE Scored**: Each GUTT individually evaluated on 5 dimensions

### Ollama's Evidence
- **Generic**: "Fetched meetings and stored", "Applied focus-time detection rules"
- **Qualitative**: No specific numbers or artifacts mentioned
- **Hypothetical**: Evidence describes what would happen, not what did happen
- **Not Scored**: Track 1/2 scores and ACRUE dimensions not yet calculated

## Evaluation Framework Differences

### Claude Evaluation (Complete ACRUE Analysis)
- ✅ **Track 1 Score**: 1.0 (All GUTTs triggered)
- ✅ **Track 2 Score**: 3.96/4.0 (Individual ACRUE scoring per GUTT)
- ✅ **Overall GUTTScore**: 3.96/4.0 (Exceptional Performance)
- ✅ **Dimension Breakdown**: Each GUTT scored on A-C-R-U-E dimensions

### Ollama Evaluation (Pending)
- ⏳ **Track 1 Score**: Not calculated
- ⏳ **Track 2 Score**: Not calculated
- ⏳ **Overall GUTTScore**: Not calculated
- ⏳ **Dimension Breakdown**: Not performed

## Implications for GUTT Framework

### Decomposition Philosophy
1. **Granularity Trade-off**: Claude favors fine-grained GUTTs; Ollama favors capability aggregation
2. **User Intent**: Both identify the core capabilities but at different abstraction levels
3. **Implementation Mapping**: Claude's decomposition maps more directly to code architecture

### Evaluator Agreement
- **Core Capabilities**: Both agree on fundamental needs (retrieval, analysis, flagging/scheduling)
- **Task Boundaries**: Significant disagreement on where to draw GUTT boundaries
- **Completeness**: Claude's approach captures more nuanced sub-capabilities

### Framework Robustness
- **Flexibility**: GUTT framework accommodates multiple decomposition strategies
- **Evaluator Variance**: Different LLMs produce valid but structurally different decompositions
- **Quality Correlation**: More granular decomposition (Claude) appears to correlate with higher implementation fidelity

## Recommendations

### For GUTT Evaluation Practice
1. **Multi-Evaluator Consensus**: Use multiple LLMs to identify both fine-grained and coarse-grained GUTTs
2. **Decomposition Guidelines**: Establish granularity standards to improve cross-evaluator consistency
3. **Capability Mapping**: Create explicit mapping between high-level capabilities and fine-grained tasks

### For This Use Case
1. **Implementation Guidance**: Claude's 5-GUTT decomposition provides better architecture blueprint
2. **Coverage Validation**: Ollama's 2-GUTT view confirms essential capability categories are present
3. **Comprehensive Approach**: Hybrid strategy combining both perspectives would be optimal

## Next Steps

1. **Complete Ollama ACRUE Scoring**: Calculate Track 1, Track 2, and overall GUTTScore for Ollama decomposition
2. **Side-by-Side Evaluation**: Use `tools/gutt_decomposition_evaluator.py` for interactive comparison
3. **Consensus Analysis**: Identify areas of agreement and divergence between evaluators
4. **Framework Refinement**: Update GUTT guidelines based on multi-evaluator insights

---

**Files Referenced**:
- Claude Analysis: `GUTT_Evaluation_Meeting_Prep_Prompt.md`
- Ollama Analysis: `ollama_gutt_decomposition_gpt-oss-20b.json`
- Comparison Tool: `tools/gutt_decomposition_evaluator.py`
