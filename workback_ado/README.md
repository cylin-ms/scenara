# Workback Planning with Azure DevOps

This directory contains all resources for using Azure DevOps work items as training data for workback planning post-training.

## 📁 Directory Contents

### Documentation
- **`ADO_POST_TRAINING_PROPOSAL.md`** (750 lines) - Focused proposal on why ADO is ideal for post-training, with implementation roadmap
- **`ADO_WORKBACK_INTEGRATION_STRATEGY.md`** (1,047 lines) - Comprehensive integration strategy with detailed code examples
- **`ADO_EXTRACTION_README.md`** (400 lines) - Setup guide and usage documentation for extraction script

### Code
- **`ado_workback_extraction.py`** (650 lines) - Production-ready Python script to extract ADO work items

## 🎯 Quick Start

### 1. Read the Proposal
Start with `ADO_POST_TRAINING_PROPOSAL.md` to understand:
- Why ADO solves the post-training challenge
- How it provides real outcomes vs synthetic data
- Implementation roadmap (50 → 200-500 → 1000+ examples)

### 2. Setup Extraction Script

```bash
# Install dependencies
pip install azure-devops

# Get PAT token from Azure DevOps
# https://dev.azure.com/your-org/_usersSettings/tokens

# Set environment variable
export ADO_PAT="your_personal_access_token"
```

### 3. Extract Pilot Data (50 Q2 Examples)

```bash
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/your-org \
  --pat-token env \
  --project YourProjectName \
  --max-examples 50 \
  --complexity Q2_Low_Complexity \
  --value High_Value
```

### 4. Review Output

```bash
# Training data
cat ado_workback_training_data.json

# Statistics
cat ado_workback_statistics.json
```

## 📊 Key Concepts

### Complexity Classification
- **Q2 (Low)**: 1-5 story points, <5 deps, <30 days - **START HERE**
- **Q3 (Medium)**: 5-8 story points, 5-15 deps, 30-90 days
- **Q1 (High)**: 13+ story points, 15+ deps, 90+ days - Graduate to this

### Value Assessment
- **High**: P0/P1 priority, customer-committed, OKRs
- **Medium**: P2 priority, some visibility
- **Low**: P3+, internal improvements

### Why ADO > Stratos-Exp

| Challenge | Stratos-Exp | ADO |
|-----------|-------------|-----|
| Ground truth | ❌ Synthetic | ✅ Real execution |
| Validation | ❌ LLM-as-Judge | ✅ Actual outcomes |
| Dependencies | ❌ Generated | ✅ Validated |
| Outcomes | ❌ None | ✅ Success/delayed/failed |

## 🚀 Implementation Phases

### Phase 1: Pilot (Month 1)
- Extract 50 Q2 (low complexity, high value) work items
- Expert review and correction
- Cost: $2,500-5,000

### Phase 2: Scale (Months 2-3)
- Extract 200-500 mixed complexity (60% Q2, 20% Q3, 15% Q1, 5% edge)
- Spot-check with experts
- Cost: $10,000-25,000

### Phase 3: Production (Months 4-6)
- Model training on ADO data
- Integration with Scenara (meeting context + ADO execution data)
- Continuous learning pipeline

## 🎓 Expected Outcomes

### Short-term (3 months)
- **65% "would use as-is"** plan quality (+25% vs Stratos-Exp baseline)
- **±30% estimate accuracy** (vs ±50% baseline)
- **75% critical dependencies** identified

### Medium-term (6 months)
- **60% on-time execution** when following generated plans
- **4.0/5.0 user satisfaction**

### Long-term (12 months)
- **20% reduction in project delays**
- **70% plan adoption rate**

## 🛡️ Competitive Advantage

**Data Moat**: General LLMs can't access enterprise ADO data  
**Network Effects**: More customers → more data → better models  
**Lead Time**: 12-18 months for competitors to replicate  

## 📖 Related Documents

In parent directory:
- `../STRATOS_EXP_EVALUATION_ANALYSIS_V2.md` - Why workback planning is hard for post-training
- `../WORKBACK_COMPARISON.md` - Comparison of CPM vs Stratos-Exp approaches
- `../WORKBACK_SUMMARY.md` - Overall integration strategy

## 🔗 Integration with Scenara

ADO data + Scenara context = Superior training data:

```
ADO Work Item (real execution)
  + Scenara Meeting (planning context)
  + Scenara Collaborators (team dynamics)
  + Expert Correction (domain knowledge)
  = Gold Standard Training Example
```

## 📝 Next Steps

After extraction:
1. **Review data quality**: Check statistics JSON
2. **Expert review**: Send to PMs for plan correction
3. **Build correction UI**: Interface for experts to fix plans
4. **Model training**: Fine-tune on corrected examples
5. **Continuous learning**: Monthly extraction pipeline

## 🔐 Security Notes

- Never commit PAT tokens to Git
- Use environment variables or Azure Key Vault
- On-premise deployment option for sensitive data
- Data anonymization for training (remove PII)

---

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Status**: Ready for Pilot Extraction
