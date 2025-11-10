# Post-Training: Oracle Input Strategy & RLHF Implementation

**Purpose**: Generate synthetic training data using Oracle Input Strategy to enable RLHF (Reinforcement Learning from Human Feedback) pre-training **before** product launch.

**Impact**: Accelerates timeline by 4-6 months, achieves 75-80% baseline accuracy vs 50-60% zero-shot.

---

## 📁 Directory Structure

```
post_training/
├── README.md                           # Main implementation guide
├── INDEX.md                            # This file - directory index
├── tools/                              # Training data generation tools
│   ├── generate_persona_training_data.py    # GPT-5 synthetic data generator
│   └── validate_schema_alignment.py         # Schema validation tool
├── docs/                               # Strategy and analysis documents
│   ├── Oracle_Input_Strategy_Analysis.md           # Oracle strategy framework
│   ├── Persona_Diversity_Framework.md              # Persona design methodology
│   ├── High_Impact_Persona_Targeting.md            # Targeting strategy (corrected)
│   └── Graph_API_Schema_Alignment_Summary.md       # Schema alignment details
└── data/                               # Personas and training data
    ├── personas/                       # Persona JSON configurations
    │   └── tier1_sales_manager_pipeline.json  # Example Tier 1 persona
    └── training/                       # Generated training data (JSONL)
        ├── tier1/                      # Tier 1 training examples
        ├── tier2/                      # Tier 2 training examples
        └── tier3/                      # Tier 3 training examples
```

---

## 📚 Documentation Overview

### Core Documents (Read in Order)

1. **[README.md](README.md)** - Start here!
   - Overview of Oracle Input Strategy
   - Complete usage guide
   - Implementation timeline
   - Expected outcomes and validation

2. **[Oracle_Input_Strategy_Analysis.md](docs/Oracle_Input_Strategy_Analysis.md)**
   - Systematic analysis of all 9 prompts
   - Oracle opportunity assessment
   - Tier 1: Organizer-2 (EXCELLENT), Organizer-1 (EXCELLENT)
   - Expected outcomes: 21,000+ synthetic examples

3. **[Persona_Diversity_Framework.md](docs/Persona_Diversity_Framework.md)**
   - 6 orthogonal dimensions for persona design
   - Combinatorial, archetypal, and data-driven approaches
   - Diversity score formula (target >0.85)
   - Complete persona template with 10 sections

4. **[High_Impact_Persona_Targeting.md](docs/High_Impact_Persona_Targeting.md)**
   - 5-star scoring system (Pain, Value, Receptivity, Influence)
   - Top personas: Sales Manager (18/20), Eng Manager (16/20), VP (14/20)
   - **CRITICAL CORRECTION**: Accuracy-Pain Paradox
   - Reversed launch strategy: Tier 3 → Tier 2 → Tier 1

5. **[Graph_API_Schema_Alignment_Summary.md](docs/Graph_API_Schema_Alignment_Summary.md)**
   - Microsoft Graph API calendar format alignment
   - Before/after schema comparison
   - Validation checklist
   - Benefits and impact analysis

---

## 🛠️ Tools

### 1. Persona Training Data Generator (`tools/generate_persona_training_data.py`)

**Purpose**: Generate synthetic meetings using GPT-5 with persona-based labeling

**Features**:
- Uses `dev-gpt-5-chat-jj` model via SilverFlow API
- Generates Microsoft Graph API-compliant meetings
- Applies persona rules for ground truth labels
- Exports JSONL format for RLHF training
- Supports tier-based generation

**Usage**:
```bash
# Generate for single persona
python post_training/tools/generate_persona_training_data.py \
  --persona post_training/data/personas/tier1_sales_manager_pipeline.json \
  --count 200

# Generate for entire tier
python post_training/tools/generate_persona_training_data.py \
  --tier 1 \
  --count 200 \
  --output-dir post_training/data/training/tier1
```

### 2. Schema Alignment Validator (`tools/validate_schema_alignment.py`)

**Purpose**: Validate synthetic data matches Microsoft Graph API format

**Features**:
- Validates required Graph API fields
- Checks nested structure compliance
- Compares schemas with real data
- Calculates alignment score (target 90%+)
- Provides detailed error reporting

**Usage**:
```bash
# Validate synthetic data
python post_training/tools/validate_schema_alignment.py \
  --synthetic post_training/data/training/tier1_combined.jsonl

# Compare with real data
python post_training/tools/validate_schema_alignment.py \
  --real my_calendar_events_complete_attendees.json \
  --synthetic post_training/data/training/tier1_combined.jsonl
```

---

## 📊 Data

### Personas (`data/personas/`)

**Structure**: JSON files with explicit preference rules

**Example**: `tier1_sales_manager_pipeline.json`
- Demographics (role, level, company, industry)
- Meeting context (weekly hours, typical breakdown)
- Importance criteria (always/usually/sometimes/rarely important)
- Priority framework (3-5 priorities with keywords)
- RSVP rules (always accept/conditional/decline)
- Prep time needs (requires/optional/no prep)

**Tier Distribution**:
- **Tier 1** (12 personas): High-impact, overloaded managers/executives
- **Tier 2** (10 personas): Senior ICs, new leaders, customer-facing
- **Tier 3** (8 personas): Edge cases, specialized roles

### Training Data (`data/training/`)

**Format**: JSONL (JSON Lines) with Microsoft Graph API schema

**Label Fields**:
- `importance_label`: "critical", "high", "medium", "low"
- `prep_needed`: boolean
- `prep_time_minutes`: integer (15-90 minutes)
- `reasoning`: string (explanation of labels)
- `persona_id`: string (source persona)
- `generation_timestamp`: ISO 8601 timestamp

**Expected Volumes**:
- Tier 1: 2,400 examples (12 personas × 200 meetings)
- Tier 2: 1,500 examples (10 personas × 150 meetings)
- Tier 3: 800 examples (8 personas × 100 meetings)
- **Total**: 4,700 labeled training examples

---

## 🎯 Key Concepts

### Oracle Input Strategy

Instead of waiting for real users, create **synthetic personas** with explicit preference rules to generate labeled training data pre-launch.

**Benefits**:
1. Decouples training from user availability (4-6 month acceleration)
2. Systematic coverage (30 personas cover vast user space)
3. High-quality labels (explicit rules ensure consistency)
4. Pre-training baseline (75-80% accuracy vs 50-60% zero-shot)
5. Faster post-launch convergence (50 feedback events vs 200)

### Accuracy-Pain Paradox (CRITICAL)

**Original Assumption**: High pain users (⭐⭐⭐⭐⭐) tolerate 70% accuracy  
**CORRECTED**: High pain = High stakes = Need 85%+ accuracy

**Why**: 
- Sales Manager: Lost deal = $100K+, career damage
- VP/Executive: Unprepared for board = career-limiting
- Engineering Manager: Missed review prep = team attrition

**Solution**: Accuracy-gated rollout
- Tier 3 first (Month 2-3, can tolerate 75%, build to 85%)
- Tier 2 next (Month 3-4, prove 85%+ accuracy)
- Tier 1 last (Month 4-6, ONLY after 85%+ proven)

### Training vs Testing Split

**Training Data Distribution**:
- 60% Tier 1 patterns (high-impact personas)
- 30% Tier 2 patterns (medium-impact personas)
- 10% Tier 3 patterns (edge cases)

**Alpha Testing Users**:
- 0% Tier 1 users (too risky until proven)
- 20% Tier 2 users (medium stakes)
- 80% Tier 3 users (low stakes, can tolerate errors)

---

## 🚀 Quick Start

### Step 1: Generate Sample Data (5 minutes)
```bash
cd c:\Users\cyl\Projects\Scenara_v6.0_checkpoint\Scenara

python post_training/tools/generate_persona_training_data.py \
  --persona post_training/data/personas/tier1_sales_manager_pipeline.json \
  --count 10 \
  --output-dir post_training/data/training/samples
```

### Step 2: Validate Schema (2 minutes)
```bash
python post_training/tools/validate_schema_alignment.py \
  --real my_calendar_events_complete_attendees.json \
  --synthetic post_training/data/training/samples/tier1_sales_manager_pipeline_meetings.jsonl
```

### Step 3: Test with Existing Tools (10 minutes)
```bash
# Test meeting classifier on synthetic data
python tools/meeting_classifier_gpt5.py \
  --input post_training/data/training/samples/tier1_sales_manager_pipeline_meetings.jsonl
```

### Step 4: Generate Full Dataset (1-2 hours)
```bash
# Tier 1: 2,400 examples
python post_training/tools/generate_persona_training_data.py --tier 1 --count 200

# Tier 2: 1,500 examples
python post_training/tools/generate_persona_training_data.py --tier 2 --count 150

# Tier 3: 800 examples
python post_training/tools/generate_persona_training_data.py --tier 3 --count 100
```

---

## 📈 Expected Outcomes

### Pre-Training Results (Month 2)
- **Organizer-2 (Meeting Importance)**: 75% F1 score (vs 50-60% zero-shot)
- **Organizer-1 (Prep Time)**: 70% accuracy (vs 55-60% zero-shot)
- Training examples: 10,000+ (Organizer-2), 8,000+ (Organizer-1)

### Alpha Testing (Month 3)
- Tier 3 users: 75-80% accuracy initially → 80-85% after 50 feedback events
- Churn rate: <10% (acceptable for alpha)

### Production Launch (Month 4-6)
- Tier 1 users: 85%+ accuracy required
- Adoption rate: 60-70% (vs 10-20% if launched too early)
- Churn rate: <5% (sustainable growth)

---

## 📝 Implementation Timeline

### Week 1: Persona Creation
- [x] Define persona framework (6 dimensions, 3 tiers)
- [x] Create Tier 1 example persona (Sales Manager)
- [ ] Create remaining 29 personas (11 Tier 1, 10 Tier 2, 8 Tier 3)

### Week 2: Data Generation
- [ ] Generate Tier 1 data (2,400 examples)
- [ ] Generate Tier 2 data (1,500 examples)
- [ ] Generate Tier 3 data (800 examples)
- [ ] Validate data quality (manual review of 100 examples)

### Week 3: Pre-Training
- [ ] Prepare JSONL for RLHF (Organizer-2 prompt)
- [ ] Pre-train model on synthetic data
- [ ] Validate on held-out personas
- [ ] Target: 75% F1 score

### Week 4: Validation & Alpha Prep
- [ ] Create validation personas (not in training set)
- [ ] Test accuracy on validation set
- [ ] Prepare alpha launch materials
- [ ] Recruit Tier 3 alpha users

---

## 🔗 Related Documentation

**In This Directory**:
- All post-training strategy, tools, and data
- Complete end-to-end implementation

**In Main Project**:
- `docs/gutt_analysis/Phased_Implementation_Plan_Verifier_Law.md` - Overall RLHF strategy
- `docs/gutt_analysis/VERIFIER_LAW_ASSESSMENT.md` - Verifier's Law framework
- `.cursorrules` - Project context and GPT-5 integration patterns

**Reference Data**:
- `my_calendar_events_complete_attendees.json` - Real meeting data (267 meetings)
- `SilverFlow/data/graph_get_meetings.py` - Meeting extraction script

---

## ⚙️ Technical Requirements

**Python Environment**:
- Python 3.8+
- Virtual environment: `./venv`
- Dependencies: `requirements.txt`

**GPT-5 Access**:
- Model: `dev-gpt-5-chat-jj` (Microsoft SilverFlow)
- Authentication: MSAL + Windows Broker (WAM)
- Reference: `.cursorrules` lines 1670-1750

**Data Format**:
- Microsoft Graph API calendar schema
- JSONL export for RLHF training
- Compatible with existing meeting classification tools

---

## 📞 Support

For questions or issues:
1. Check `README.md` in this directory
2. Review related documentation above
3. Check `.cursorrules` for project context
4. Contact: cyl@microsoft.com

---

**Status**: ✅ Implementation complete, ready for persona creation and data generation  
**Last Updated**: November 10, 2025
