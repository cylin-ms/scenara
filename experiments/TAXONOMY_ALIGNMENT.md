# Meeting Classification Taxonomy Alignment

**Date**: October 28, 2025  
**Purpose**: Document taxonomy usage and prompt engineering for meeting classification

## Official Taxonomy Source

**Document**: `ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md`  
**Title**: Comprehensive Taxonomy of Enterprise Meeting Types for AI-driven Classification  
**Author**: Chin-Yew Lin, Microsoft Researcher  
**Coverage**: >95% of business meetings across Fortune 500 companies

## Taxonomy Structure

The official Enterprise Meeting Taxonomy has **5 main categories** covering **31+ meeting types**:

### 1. Internal Recurring Meetings (Cadence)
Regular within-organization meetings on repeating schedules to keep work on track:
- **Team Status Update Meetings** - daily stand-ups, shift huddles, weekly team meetings
- **Progress Review Meetings** - project status reviews, milestone checks, portfolio reviews
- **One-on-One Meetings** - manager 1:1s, coaching sessions, skip-levels, mentor meetings
- **Action Review Meetings** - sprint retrospectives, post-mortems, incident reviews, win/loss analysis
- **Governance & Strategy Cadence** - QBRs, executive leadership meetings, board meetings

### 2. Strategic Planning & Decision Meetings
Ad-hoc meetings focused on planning and decision-making:
- **Planning Sessions** - strategy planning, roadmap meetings, campaign planning, initiative scoping
- **Decision-Making Meetings** - hiring decisions, go/no-go launches, architecture reviews
- **Problem-Solving / Incident Resolution** - war rooms, crisis meetings, process breakdowns, escalations
- **Brainstorming / Innovation Meetings** - ideation, design thinking, blue-sky sessions, creative workshops
- **Workshops & Design Sessions** - design sprints, kickoff workshops, value-stream mapping, team offsites

### 3. External & Client-Facing Meetings
Meetings involving people outside the organization:
- **Sales & Client Meetings** - sales pitches, demos, client check-ins, QBRs, renewal negotiations
- **Vendor/Supplier Meetings** - vendor negotiations, supplier performance reviews, onboarding
- **Partnership/Business Development** - investor pitches, alliance discussions, M&A due diligence
- **Interviews and Recruiting** - phone screens, technical interviews, panel interviews, hiring
- **Client Training or Onboarding** - product training, customer onboarding, walkthrough sessions

### 4. Informational & Broadcast Meetings
One-way information dissemination to larger audiences:
- **All-Hands / Town Hall Meetings** - company-wide updates, executive addresses, quarterly updates
- **Informational Briefings** - policy announcements, org changes, reorg notifications, project findings
- **Training & Education Sessions** - compliance training, skill development, software training
- **Webinars and Broadcasts** - lunch & learns, knowledge sharing webinars, demo days

### 5. Team-Building & Culture Meetings
Focus on relationships, cohesion, and company culture:
- **Team-Building Activities** - team offsites, bonding workshops, ice-breaker sessions
- **Recognition & Social Events** - celebration ceremonies, retirement send-offs, casual coffee chats
- **Communities of Practice & Networking** - interest group meetups, cross-team forums, PM groups

## Classification Principles

From the official taxonomy document:

1. **Primary Purpose**: Meetings may blend types, but identify the DOMINANT purpose
2. **Context Signals**: 
   - Attendee count (2 = likely 1:1, 10-20 = team, >50 = broadcast)
   - External domains = client-facing
   - Recurrence = cadence meeting
   - Duration (15min = standup, 2-4hr = workshop)
3. **Multi-label Consideration**: Some meetings genuinely span multiple types
4. **Flexibility**: Taxonomy designed for real-world complexity, not rigid boxes

## Prompt Engineering Comparison

### GitHub Copilot (October 28, 2025 - Experiment 001)

**Approach**: I (GitHub Copilot) had access to the full Enterprise Meeting Taxonomy document in context and applied it directly during classification. 

**Prompt Structure** (Implicit):
```
Context: Full taxonomy document understanding
Method: Semantic analysis with 31+ meeting types
Categories: 5 main categories from official taxonomy
Output: Detailed reasoning with key indicators, alternate classifications, business value
```

**Strengths**:
- ✅ Full taxonomy knowledge in context
- ✅ Detailed reasoning (3-5 paragraphs per meeting)
- ✅ Key indicators listed explicitly
- ✅ Alternate classifications provided
- ✅ Inter-meeting relationship detection
- ✅ Business value assessment included

**Weaknesses**:
- ❌ Not reproducible via script (manual classification)
- ❌ Model version uncertain (estimated gpt-4-1106-preview)
- ❌ Cannot be automated for batch processing

---

### GPT-5 Initial Version (Before Fix)

**Prompt Used** (Simplified):
```
ENTERPRISE MEETING TAXONOMY (5 categories, 31+ types):

1. Strategic Planning & Decision
   - Strategic Planning Session, Decision-Making Meeting, Problem-Solving Meeting
   - Brainstorming Session, Workshop/Design Session, Budget Planning Meeting
   - Project Planning Meeting, Risk Assessment Meeting

2. Internal Recurring (Cadence)
   - Team Status Update/Standup, Progress Review Meeting, One-on-One Meeting
   - Team Retrospective, Governance/Leadership Meeting, Performance Review
   - Weekly/Monthly Check-in

[... abbreviated categories ...]
```

**Issues**:
- ❌ **Incomplete taxonomy** - Missing specific meeting type descriptions
- ❌ **No context guidance** - Doesn't explain WHEN to use each type
- ❌ **Simplified labels** - Lost nuance from official taxonomy
- ❌ **No classification principles** - Doesn't cite attendee/duration signals
- ❌ **Over-simplification** - "Progress Review Meeting" used for 4 different meetings

**Result**: GPT-5 classified 50% of meetings as "Progress Review Meeting" due to lack of detailed guidance.

---

### GPT-5 Updated Version (After Fix - October 28, 2025)

**Prompt Structure** (Corrected):
```python
"""Classify the following meeting according to the official Enterprise Meeting Taxonomy 
(Comprehensive Taxonomy of Enterprise Meeting Types for AI-driven Classification by Chin-Yew Lin).

OFFICIAL ENTERPRISE MEETING TAXONOMY:
This taxonomy covers >95% of business meetings across Fortune 500 companies.

1. INTERNAL RECURRING MEETINGS (CADENCE)
Regular within-organization meetings on repeating schedules:
   • Team Status Update Meetings - routine check-ins, daily stand-ups, shift huddles
   • Progress Review Meetings - formal status reviews, milestone checks, project reviews
   • One-on-One Meetings - manager 1:1s, coaching sessions, skip-levels, peer check-ins
   • Action Review Meetings - retrospectives, post-mortems, sprint reviews, win/loss analysis
   • Governance & Strategy Cadence - QBRs, executive meetings, board meetings

[... full taxonomy with descriptions ...]

CLASSIFICATION GUIDELINES:
- Identify the PRIMARY purpose (meetings may blend types, but one is usually dominant)
- Use meeting title, description, attendee count/types, duration, and recurrence as signals
- Consider context: 2 people = likely 1:1, >50 people = likely broadcast, external domains = client-facing
- If genuinely unclear, choose the closest match with lower confidence

TASK:
Output JSON with: specific_type, primary_category, confidence, reasoning, key_indicators
"""
```

**Improvements**:
- ✅ **Complete taxonomy** with descriptions for each type
- ✅ **Context guidance** - explains when to use each classification
- ✅ **Classification principles** - cites attendee count, duration, external domains
- ✅ **Full detail** - matches official taxonomy structure
- ✅ **Key indicators** - requests evidence for classification
- ✅ **Confidence calibration** - guidance on certainty levels

**Expected Results**:
- More balanced category distribution
- Better differentiation between similar meeting types
- Higher quality reasoning
- Evidence-based classifications

## Recommendations

### For GitHub Copilot Classification
When using GitHub Copilot for meeting classification:

1. **Reference the taxonomy document**: Mention `ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md` explicitly
2. **Request structured output**: Ask for JSON with specific_type, category, confidence, reasoning, key_indicators
3. **Provide context**: Include attendee count, duration, recurrence, external domains
4. **Ask for evidence**: Request key signals that support the classification

**Example Prompt**:
```
Using the Enterprise Meeting Taxonomy from ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md,
classify these 8 meetings. For each meeting provide:
- Specific type (from the 31+ types)
- Primary category (from 5 main categories)
- Confidence score
- Reasoning with key indicators
- Alternate classification if confidence < 95%
```

### For GPT-5 Classification Script
The updated `tools/meeting_classifier_gpt5.py` now includes:

- ✅ Full official taxonomy in prompt
- ✅ Classification guidelines from research
- ✅ Context signal explanations
- ✅ Structured JSON output request
- ✅ Key indicators field

**Usage**:
```bash
python classify_with_gpt5.py
```

### For Future Experiments

**Best Practices**:
1. **Always use the official taxonomy** - Don't simplify or abbreviate
2. **Include classification guidelines** - Attendee count, duration, context matter
3. **Request evidence** - Key indicators improve transparency
4. **Cite the source** - Reference Chin-Yew Lin's taxonomy document
5. **Compare results** - Different models may emphasize different signals

**Experiment Protocol**:
1. Run classification with updated prompts
2. Compare with GitHub Copilot baseline (93% confidence, detailed reasoning)
3. Analyze category distribution (should be more balanced than 50% in one category)
4. Verify key indicators align with taxonomy principles
5. Document any taxonomy gaps or edge cases

## Updated Comparison Plan

### Re-run Experiment 002 with Corrected Taxonomy
To validate the taxonomy fix:

1. **Re-classify 8 meetings** using updated GPT-5 prompt
2. **Compare distributions**:
   - Old: 50% Internal Recurring (4/8)
   - Expected: More balanced across categories
3. **Evaluate reasoning quality**:
   - Check for key indicators
   - Verify context signals used
4. **Compare with GitHub Copilot**:
   - Same meetings, different classification approach
   - Document where models agree/disagree
   - Identify which is more aligned with official taxonomy

### Next Steps

1. ✅ **Update GPT-5 prompt** - Complete (October 28, 2025)
2. ⏳ **Re-run GPT-5 classification** - Use corrected taxonomy
3. ⏳ **Create Experiment 003** - GPT-5 with official taxonomy
4. ⏳ **Compare all three**: Original GPT-5, Corrected GPT-5, GitHub Copilot
5. ⏳ **Document findings** - Which approach best matches official taxonomy?

## Conclusion

The **official Enterprise Meeting Taxonomy** (Chin-Yew Lin, Microsoft) provides comprehensive guidance for meeting classification. Both GitHub Copilot and GPT-5 should use this taxonomy, but the prompt engineering matters significantly:

- **GitHub Copilot** had full context access → detailed, well-reasoned classifications
- **GPT-5 (initial)** used simplified taxonomy → over-concentration in one category
- **GPT-5 (updated)** now uses official taxonomy → expect better distribution

The key lesson: **Don't abbreviate the taxonomy** - include full descriptions, context signals, and classification principles for optimal results.

---

**Document Status**: ✅ Complete  
**Next Action**: Re-run GPT-5 classification with corrected taxonomy  
**Files Updated**: `tools/meeting_classifier_gpt5.py`
