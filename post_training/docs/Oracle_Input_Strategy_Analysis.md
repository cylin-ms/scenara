# Oracle Input Strategy for Post-Training Data Generation

**Author**: Chin-Yew Lin  
**Date**: November 10, 2025  
**Framework**: Decoupling Ground Truth Dependencies for Rapid RLHF Bootstrapping

---

## Executive Summary

**Key Insight**: For prompts requiring personal preferences, we can **create synthetic oracles** (simulated user profiles with explicit preferences) to generate training data WITHOUT waiting for real user interactions.

**Strategic Value**:
- ✅ **Decouple data collection from user availability**: Generate thousands of training examples upfront
- ✅ **Accelerate post-training timeline**: Start training before product launch
- ✅ **Test personalization infrastructure**: Validate RLHF pipeline with controlled data
- ✅ **Reduce cold start risk**: Launch with pre-trained personalized models

**Oracle Opportunity Score**: How well can we simulate ground truth for each prompt?

| Prompt | Oracle Feasibility | Strategy | Data Volume Potential | RLHF Readiness |
|--------|-------------------|----------|----------------------|----------------|
| **Organizer-2** | ✅ **EXCELLENT** | User importance profiles | 10K+ examples | **Ready to train** |
| **Organizer-1** | ✅ **EXCELLENT** | Priority frameworks | 10K+ examples | **Ready to train** |
| **Collaborate-1** | ⚠️ **GOOD** | Team/project contexts | 5K+ examples | **Useful baseline** |
| **Organizre-3** | ⚠️ **MODERATE** | Time preference profiles | 3K+ examples | **Recommendations only** |
| **Schedule-1/2/3** | ✅ **PERFECT** | Constraint specifications | Unlimited | **Not needed (deterministic)** |
| **Collaborate-2** | ❌ **POOR** | Context too complex | Limited | **Not recommended** |
| **Collaborate-3** | ❌ **N/A** | Factual data (no oracle) | N/A | **Not applicable** |

---

## Detailed Analysis by Prompt

### ✅ TIER 1: Excellent Oracle Opportunities (Ready for Synthetic Training Data)

---

#### 1. Organizer-2: Important Meeting Flagging
**Oracle Strategy**: Create synthetic user importance profiles

**Why This Works**:
- ✅ **Importance is role-based**: CEO, engineer, salesperson have predictable patterns
- ✅ **Can enumerate criteria**: External meetings, C-suite attendees, budget reviews, customer calls
- ✅ **Explicit preference modeling**: Can create 20+ distinct user personas

**Oracle Profile Template**:
```json
{
  "user_persona": "Senior Engineering Manager",
  "importance_criteria": {
    "high_importance": [
      "Meetings with direct reports (1:1s)",
      "Escalations or incidents",
      "Executive reviews (planning, roadmap)",
      "Customer escalations",
      "Cross-team architecture decisions"
    ],
    "medium_importance": [
      "Team standups",
      "Project syncs",
      "Recruiting interviews"
    ],
    "low_importance": [
      "All-hands (informational)",
      "Optional social events",
      "Recurring team lunches"
    ]
  },
  "prep_time_needed": {
    "always": ["Executive reviews", "Customer meetings"],
    "sometimes": ["Cross-team syncs", "Architecture discussions"],
    "rarely": ["1:1s with directs", "Standups"]
  }
}
```

**Data Generation Process**:
1. **Create 20-30 user personas** (CEO, VP Eng, IC Engineer, Sales Rep, PM, etc.)
2. **Define importance rules** for each persona (5-10 high-importance patterns each)
3. **Generate synthetic calendar data** (100-200 meetings per persona)
4. **Apply persona rules** to label meetings as important/not important
5. **Create training pairs**: (Meeting context, Persona) → Importance label

**Expected Output**:
- **10,000+ labeled examples**: 30 personas × 200 meetings × 2 labels (important + prep needed)
- **Diverse coverage**: Different roles, meeting types, attendee combinations
- **Ground truth quality**: 95%+ accurate labels (rule-based from explicit criteria)

**Training Approach**:
1. **Phase 1**: Train on synthetic oracle data (baseline personalization)
2. **Phase 2**: Fine-tune with real user feedback (post-launch)
3. **Validation**: Holdout test set from different persona types

**Success Metrics**:
- Synthetic model achieves 75%+ F1 on held-out personas (vs 60% zero-shot baseline)
- Real user fine-tuning improves to 85%+ F1 within 50 feedback events
- Reduces cold start from "50 feedbacks to useful" → "10 feedbacks to personalized"

---

#### 2. Organizer-1: Priority-Based RSVP Recommendations
**Oracle Strategy**: Create explicit priority framework profiles

**Why This Works**:
- ✅ **Priorities are articulable**: Focus on customers, ship products, mentor team, etc.
- ✅ **Can enumerate common patterns**: Sales (customer meetings), Eng (heads-down time), Exec (strategy)
- ✅ **Meeting-priority alignment is logical**: Can create rules mapping meetings to priorities

**Oracle Profile Template**:
```json
{
  "user_persona": "Product Manager",
  "top_priorities": [
    {
      "priority": "Ship Q4 features on time",
      "importance": "critical",
      "meeting_indicators": ["sprint", "roadmap", "feature", "launch", "release"]
    },
    {
      "priority": "Customer feedback loops",
      "importance": "high",
      "meeting_indicators": ["customer", "user research", "feedback", "beta"]
    },
    {
      "priority": "Cross-functional alignment",
      "importance": "medium",
      "meeting_indicators": ["eng sync", "design review", "marketing"]
    }
  ],
  "low_value_meetings": [
    "Recurring all-hands (async updates)",
    "Non-urgent informational syncs",
    "Social events during crunch time"
  ],
  "accept_criteria": {
    "always_accept": ["Customer meetings", "Launch-critical decisions"],
    "accept_if_aligned": ["Team syncs on Q4 features"],
    "decline_unless_critical": ["Informational meetings", "Optional workshops"]
  }
}
```

**Data Generation Process**:
1. **Create 25+ user personas** across roles (IC, manager, exec) and functions (eng, sales, ops)
2. **Define 3-5 priorities per persona** with explicit keywords/patterns
3. **Generate synthetic invites** (150-300 per persona) with varied:
   - Titles, attendees, descriptions
   - Alignment levels with priorities (high/medium/low/none)
4. **Apply priority matching logic** to generate RSVP recommendations
5. **Create training triplets**: (Meeting, Priorities, Context) → Accept/Decline/Tentative

**Expected Output**:
- **8,000+ training examples**: 25 personas × 200 invites × 2 decisions (RSVP + reasoning)
- **Priority coverage**: Customer focus, shipping, team building, strategic planning, etc.
- **Context diversity**: Busy weeks, light weeks, conflicting priorities, clear alignment

**Training Approach**:
1. **Phase 1**: Train classifier on synthetic personas (learn priority-meeting alignment)
2. **Phase 2**: User onboarding collects 3-5 real priorities (explicit elicitation)
3. **Phase 3**: Few-shot personalization from 10-20 RSVP overrides
4. **Phase 4**: Continuous learning from all user decisions

**Success Metrics**:
- Synthetic model: 65%+ accuracy on held-out personas (vs 50% random baseline)
- With user elicitation: 75%+ accuracy immediately (persona + real priorities)
- With 20 overrides: 85%+ accuracy (fully personalized)

**Key Advantage**:
Even without ANY real user data, we can:
- ✅ Build personalization infrastructure
- ✅ Test RLHF pipeline end-to-end
- ✅ Launch with "smart defaults" that work 65-75% of the time
- ✅ Collect real feedback to quickly improve to 85%+

---

### ⚠️ TIER 2: Good Oracle Opportunities (Useful But Limited)

---

#### 3. Collaborate-1: Agenda Generation
**Oracle Strategy**: Create synthetic team/project contexts

**Why This Works (Partially)**:
- ✅ **Meeting types are enumerable**: Sprint planning, design reviews, 1:1s, strategy sessions
- ✅ **Coverage is objective**: Required topics for each meeting type can be listed
- ⚠️ **Style is subjective**: Bullet points vs narratives, detail level varies by team

**Oracle Profile Template**:
```json
{
  "meeting_type": "Sprint Planning",
  "team_context": {
    "team_name": "Platform Infrastructure",
    "size": 8,
    "sprint_length": "2 weeks",
    "methodology": "Scrum"
  },
  "required_topics": [
    "Review last sprint velocity and burndown",
    "Prioritize backlog items for next sprint",
    "Capacity planning (PTO, holidays)",
    "Dependencies on other teams",
    "Technical debt items"
  ],
  "optional_topics": [
    "Demo of completed work",
    "Process improvement discussions",
    "Team morale check-in"
  ],
  "style_preferences": {
    "format": "structured_with_time_boxes",
    "detail_level": "concise",
    "include_links": true
  }
}
```

**Data Generation Process**:
1. **Define 15-20 common meeting types** (sprint planning, design review, 1:1, quarterly planning, etc.)
2. **Create required/optional topic lists** for each type
3. **Generate 50+ synthetic team contexts** (different methodologies, team sizes, domains)
4. **Apply templates** to generate agendas
5. **Vary style** (some teams prefer detail, others prefer brevity)

**Expected Output**:
- **3,000+ agenda examples**: 20 meeting types × 50 contexts × 3 variations
- **Topic coverage**: Objective verification (all required topics present)
- **Style variation**: Different formats, detail levels, structures

**Limitations**:
- ⚠️ **Style is hard to oracle**: Team preferences for agenda format are idiosyncratic
- ⚠️ **Context depth**: Real team dynamics, politics, history are hard to simulate
- ⚠️ **Medium ROI**: Coverage is easy (rule-based), style personalization has diminishing returns

**Training Approach**:
1. **Phase 1**: Train on synthetic data for **coverage** (objective part)
2. **Phase 2**: Zero-shot for style (good enough for v1)
3. **Phase 3 (optional)**: RLHF for style if user engagement warrants

**Success Metrics**:
- Topic coverage: 95%+ (synthetic training ensures all required topics)
- Style satisfaction: 70%+ without RLHF (zero-shot), 80%+ with RLHF

---

#### 4. Organizre-3: Time Reclamation Recommendations
**Oracle Strategy**: Create time preference profiles

**Why This Works (Partially)**:
- ✅ **Time analytics are deterministic**: Meeting load, fragmentation are calculable
- ⚠️ **Recommendations are personal**: Some users prefer morning focus blocks, others prefer afternoons
- ⚠️ **Limited personalization value**: Generic recommendations work for 80% of users

**Oracle Profile Template**:
```json
{
  "user_persona": "Senior Engineer",
  "time_preferences": {
    "focus_time_preferred": ["9-11am", "2-4pm"],
    "meeting_clusters_preferred": "afternoons",
    "minimum_focus_block": "2 hours",
    "acceptable_meeting_load": "20 hours/week"
  },
  "reclamation_priorities": [
    "Cancel low-value recurring meetings",
    "Consolidate 1:1s to same day",
    "Block morning focus time",
    "Decline optional large meetings"
  ]
}
```

**Limitations**:
- ⚠️ **Low personalization ROI**: Most users want the same things (less meetings, more focus time)
- ⚠️ **Recommendations are generic**: "You have 30 meetings this week" → "Cancel some meetings"
- ⚠️ **Oracle doesn't add much value**: Generic rules work well without personalization

**Training Approach**:
- **Skip RLHF for v1**: Use deterministic analytics + generic recommendations
- **Optional v2**: If users want personalized recommendations (morning vs afternoon focus), collect preferences

---

### ❌ TIER 3: Poor/No Oracle Opportunities

---

#### 5-7. Schedule-1/2/3: Scheduling Automation
**Oracle Strategy**: N/A (Deterministic, no training needed)

**Why No Oracle Needed**:
- ✅ **Constraints are explicit**: "Weekly, 30min, afternoons, avoid Fridays"
- ✅ **Verification is deterministic**: Check if constraints satisfied
- ✅ **Already solvable**: Zero-shot LLM + constraint solver = 90%+ accuracy
- ❌ **No personalization needed**: Same logic for all users

**No Training Data Required**: Traditional software engineering suffices.

---

#### 8. Collaborate-2: Leadership Communication Prep
**Oracle Strategy**: Not recommended (context too complex)

**Why Oracle Doesn't Work**:
- ❌ **Context is unique**: Each leadership meeting has specific stakeholders, politics, history
- ❌ **Quality is subjective**: "Good talking points" vary by audience, culture, relationship
- ❌ **User lacks expertise**: Can't verify quality (seeking advice, not providing ground truth)
- ❌ **Better alternative**: RAG from expert-curated content (books, best practices)

**Why Synthetic Data Fails**:
- Synthetic contexts lack the nuance of real organizational dynamics
- User feedback is noisy (they're seeking advice, not validating quality)
- Training on synthetic scenarios teaches generic patterns, not personalization

**Better Approach**: RAG from leadership communication books, expert frameworks, case studies.

---

#### 9. Collaborate-3: Customer Intelligence Dossiers
**Oracle Strategy**: N/A (Factual retrieval, not personalization)

**Why No Oracle**:
- ❌ **Facts are objective**: Customer business updates, attendee profiles are external data
- ❌ **No personalization**: Same facts for all users (customer name determines content)
- ❌ **User can't verify**: Doesn't know if dossier is complete until after meeting
- ❌ **Challenge is data access**: API integration, not ML training

**Better Approach**: Improve data sources (news APIs, LinkedIn, CRM integration).

---

## Oracle Implementation Strategy

### Phase 1: Synthetic Data Generation (Months 1-2)

**Priority 1: Organizer-2 Oracle**
1. Create 30 user persona profiles (roles × functions)
2. Define importance criteria for each persona (5-10 rules)
3. Generate 200 synthetic meetings per persona (6,000 meetings total)
4. Apply persona rules to label importance + prep needed
5. Output: 10,000+ training examples

**Priority 2: Organizer-1 Oracle**
1. Create 25 priority framework profiles
2. Define 3-5 priorities per persona with keywords
3. Generate 200 synthetic invites per persona (5,000 invites total)
4. Apply priority matching logic for RSVP recommendations
5. Output: 8,000+ training examples

**Priority 3 (Optional): Collaborate-1 Oracle**
1. Define 20 meeting types with required topics
2. Create 50 team contexts
3. Generate agenda templates (3,000 examples)
4. Focus on objective coverage (not style)

**Tools Needed**:
- Persona definition framework (JSON schemas)
- Meeting generator (synthetic calendar data)
- Rule-based labeling engine
- Training data export (JSONL format for RLHF)

### Phase 2: Model Pre-Training (Months 2-3)

**Organizer-2**:
- Train importance classifier on synthetic persona data
- Expected: 75% F1 on held-out personas (vs 60% zero-shot)
- Validates that personalization signal exists

**Organizer-1**:
- Train RSVP recommender on synthetic priority frameworks
- Expected: 65% accuracy on held-out personas (vs 50% random)
- Proves priority-meeting alignment is learnable

**Infrastructure**:
- RLHF pipeline (DPO or PPO)
- Evaluation harness (held-out persona test sets)
- Model versioning and A/B testing framework

### Phase 3: Real User Fine-Tuning (Months 3-6)

**Cold Start Advantage**:
- Launch with pre-trained models (synthetic data)
- Users see "smart defaults" immediately (70-75% accuracy)
- Collect 50-100 feedback events per user
- Fine-tune on real preferences → 85%+ accuracy

**Comparison Without Oracle Strategy**:
- ❌ Launch with zero-shot (50-60% accuracy)
- ❌ Requires 100-200 feedback events to reach 75%
- ❌ Poor initial experience, user churn risk

**With Oracle Strategy**:
- ✅ Launch with 70-75% accuracy (synthetic pre-training)
- ✅ Requires only 20-50 feedback events to reach 85%
- ✅ Good initial experience, users trust system faster

---

## Expected Outcomes

### Data Volume Generated

| Prompt | Synthetic Training Examples | Persona Count | Time to Generate |
|--------|----------------------------|---------------|------------------|
| **Organizer-2** | 10,000+ | 30 personas | 2 weeks (automated) |
| **Organizer-1** | 8,000+ | 25 personas | 2 weeks (automated) |
| **Collaborate-1** | 3,000+ | 50 contexts | 1 week (templates) |
| **Total** | **21,000+** | - | **3-4 weeks** |

### Model Performance Gains

| Metric | Zero-Shot Baseline | Synthetic Pre-Training | Real User Fine-Tuning |
|--------|-------------------|------------------------|----------------------|
| **Organizer-2 F1** | 60% | 75% (+15%) | 85% (+10%) |
| **Organizer-1 Accuracy** | 50% | 70% (+20%) | 85% (+15%) |
| **Collaborate-1 Coverage** | 85% | 95% (+10%) | 95% (no change) |

### Timeline Acceleration

| Milestone | Without Oracle Strategy | With Oracle Strategy | Time Saved |
|-----------|------------------------|---------------------|------------|
| **Start Training** | Month 6 (after launch) | Month 2 (pre-launch) | 4 months |
| **Useful Model** | Month 9 (100+ feedbacks) | Month 3 (pre-trained) | 6 months |
| **85% Accuracy** | Month 12 (200+ feedbacks) | Month 6 (50 feedbacks) | 6 months |

---

## Key Insights

### 1. **Decoupling is Transformative**
- Traditional: Wait for product → launch → collect data → train → deploy (12+ months)
- Oracle strategy: Generate data → pre-train → launch smart → fine-tune (6 months)
- **Accelerates time-to-personalization by 50%**

### 2. **Personal Preference is Oraclable**
- ✅ **Organizer-2**: Importance criteria are articulable (role-based patterns)
- ✅ **Organizer-1**: Priorities are explicit (can enumerate common frameworks)
- ❌ **Collaborate-2**: Quality judgment requires expertise (not oraclable)
- ❌ **Collaborate-3**: Facts are external data (not personalization)

### 3. **Synthetic Data Quality Matters**
- High-quality oracles (explicit persona rules) → 75% F1 pre-training
- Low-quality oracles (vague heuristics) → 55% F1 (marginal over zero-shot)
- **Investment in persona design pays off**

### 4. **Real User Data Still Essential**
- Synthetic data provides **baseline personalization** (70-75%)
- Real feedback provides **true personalization** (85%+)
- Oracle strategy **reduces feedback volume needed** (50 vs 200 events)

### 5. **Infrastructure Validation**
- Building oracle framework validates RLHF pipeline before launch
- Identifies data quality issues, model architecture problems early
- **Reduces risk of post-launch surprises**

---

## Recommendations

### Immediate Actions (Month 1)

1. **Build Organizer-2 Oracle** (Priority 1):
   - Define 30 user personas (roles × functions)
   - Create importance rule sets (5-10 per persona)
   - Generate 10K+ synthetic training examples
   - Train baseline model, evaluate on held-out personas

2. **Build Organizer-1 Oracle** (Priority 2):
   - Define 25 priority frameworks (common patterns)
   - Create RSVP decision rules (priority-meeting alignment)
   - Generate 8K+ synthetic training examples
   - Train baseline model, validate priority learning

3. **Design Infrastructure**:
   - Persona definition schemas (JSON)
   - Synthetic data generators (automated)
   - RLHF training pipeline
   - Evaluation framework (held-out test sets)

### Success Criteria (Month 3)

- ✅ **20K+ synthetic training examples generated**
- ✅ **Pre-trained models achieve 70-75% accuracy** (vs 50-60% zero-shot)
- ✅ **RLHF pipeline validated** (can train and deploy models)
- ✅ **Launch with smart defaults** (good initial user experience)

### Long-Term Value (Month 6+)

- ✅ **Reduces cold start time** from 200 feedback events → 50 events
- ✅ **Accelerates personalization** by 6 months
- ✅ **Improves initial experience** (70% vs 50% accuracy at launch)
- ✅ **Validates feasibility** of personalization before committing to full RLHF investment

---

## Conclusion

**The "Oracle Input Strategy" is game-changing for personal preference prompts**:

1. **Decouple data collection from user availability**: Generate training data pre-launch
2. **Accelerate timeline**: Start training 4 months earlier
3. **Reduce risk**: Validate personalization feasibility with synthetic data
4. **Improve launch experience**: 70% accuracy vs 50% (users trust system faster)
5. **Lower feedback burden**: Need 50 events instead of 200 to reach 85% accuracy

**Highest ROI**:
- ✅ **Organizer-2**: 10K synthetic examples, 75% F1 pre-training (vs 60% zero-shot)
- ✅ **Organizer-1**: 8K synthetic examples, 70% accuracy pre-training (vs 50% random)

**Key Principle**: Personal preferences are **articulable** (can be written as rules). Oracle strategy converts explicit rules into implicit learning, enabling rapid bootstrapping without real user data.

**Next Steps**: Build persona frameworks and synthetic data generators for Organizer-2 and Organizer-1 in Month 1.
