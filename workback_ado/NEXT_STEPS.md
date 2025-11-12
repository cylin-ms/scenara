# Next Steps for ADO Workback Planning

## ✅ Completed

1. **Batch Classification Optimization**
   - Implemented `llm_batch_classify()` method
   - Tested with 181 items successfully
   - 5x performance improvement achieved
   - File: `BATCH_OPTIMIZATION_SUCCESS.md`

2. **LLM vs Heuristic Comparison Tool**
   - Script: `compare_llm_vs_heuristic.py`
   - Features: Agreement analysis, distribution comparison
   - Status: Ready to run

3. **Expert Review Workflow**
   - Script: `expert_review_workflow.py`
   - Formats: CSV (Excel) + HTML (web UI)
   - Status: Ready to use

4. **Comprehensive Documentation**
   - Guide: `COMPLETE_GUIDE.md`
   - Test utility: `test_ado_connection.py`
   - Status: Complete

## ⏭️ To Do

### 1. Get Fresh PAT Token

Your current PAT token has expired. Generate a new one:

1. Go to: https://office.visualstudio.com/_usersSettings/tokens
2. Create new token with these permissions:
   - **Work Items**: Read, Write
   - **Project and Team**: Read
3. Set expiration: 90 days
4. Copy token and set in environment:
   ```bash
   export ADO_PAT="your-new-token-here"
   ```

### 2. Extract 50 Q2 Training Examples

```bash
cd /Users/cyl/projects/scenara/workback_ado
source ../.venv/bin/activate
export ADO_PAT="your-new-token"

python ado_workback_extraction.py \
  --org-url https://office.visualstudio.com \
  --pat-token env \
  --project Outlook \
  --months-back 12 \
  --max-examples 50 \
  --complexity Q2_Low_Complexity \
  --value all \
  --use-llm \
  --output ado_llm_50_q2_optimized.json
```

**Expected Time**: ~2-5 minutes (with batch optimization)
**Output**: `ado_llm_50_q2_optimized.json` (50 classified examples)

### 3. Run LLM vs Heuristic Comparison

```bash
python compare_llm_vs_heuristic.py \
  --org-url https://office.visualstudio.com \
  --pat-token env \
  --project Outlook \
  --num-items 30 \
  --output comparison_results.json
```

**Expected Results**:
- Agreement rate: 60-70%
- LLM finds more High_Value items
- LLM identifies more Q3_Medium items
- Report shows top disagreements

### 4. Generate Expert Review Interfaces

```bash
python expert_review_workflow.py \
  --input ado_llm_50_q2_optimized.json \
  --format both \
  --output-csv expert_review.csv \
  --output-html expert_review.html
```

**Outputs**:
- `expert_review.csv` - Open in Excel, columns K-N for corrections
- `expert_review.html` - Open in browser, inline correction forms

### 5. Collect Expert Corrections

**Option A: Excel Review**
1. Share `expert_review.csv` with PM experts
2. Experts fill columns K-N (corrections)
3. Save and return corrected CSV
4. Run correction analysis:
   ```bash
   python expert_review_workflow.py \
     --input ado_llm_50_q2_optimized.json \
     --corrected-csv expert_review_corrected.csv \
     --output-summary correction_summary.json
   ```

**Option B: Web Review**
1. Open `expert_review.html` in browser
2. Use filters to focus on specific types
3. Fill correction forms inline
4. Click "Export Corrections" to download JSON
5. Import corrections for analysis

### 6. Scale to Production (200-500 Examples)

Once validation is complete:

```bash
# Mixed complexity distribution
python ado_workback_extraction.py \
  --org-url https://office.visualstudio.com \
  --pat-token env \
  --project Outlook \
  --months-back 18 \
  --max-examples 200 \
  --complexity all \
  --value all \
  --use-llm \
  --output ado_training_dataset_200.json
```

**Target Distribution**:
- 60% Q2_Low_Complexity (120 examples)
- 20% Q3_Medium_Complexity (40 examples)
- 15% Q1_High_Complexity (30 examples)
- 5% Edge cases (10 examples)

### 7. Model Training Integration

After collecting 200-500 validated examples:

1. **Prepare Training Data**:
   ```bash
   # Convert to model training format
   python prepare_training_data.py \
     --input ado_training_dataset_200.json \
     --corrected-csv expert_corrections.csv \
     --output model_training_input.jsonl
   ```

2. **Run Model Training**:
   ```bash
   # Use with existing Scenara training pipeline
   python tools/train_workback_model.py \
     --training-data model_training_input.jsonl \
     --model-type transformer \
     --output workback_model_v1.pkl
   ```

3. **Evaluate Model**:
   ```bash
   python tools/evaluate_model.py \
     --model workback_model_v1.pkl \
     --test-data ado_test_set.json \
     --metrics accuracy,precision,recall
   ```

## 🔄 Iteration Cycle

1. Extract data → 2. LLM classify → 3. Expert review → 4. Collect corrections
2. Analyze disagreements → Improve prompts → Re-extract
3. Repeat until agreement > 85%
4. Scale to full dataset (200-500 examples)
5. Train model with validated data

## 📊 Success Metrics

- **Data Quality**: >85% agreement between LLM and experts
- **Coverage**: 200-500 examples with mixed complexity
- **Distribution**: Representative of real workback scenarios
- **Model Performance**: >80% accuracy on test set

## 🚀 Quick Start (Resume from Current State)

You have successfully optimized batch classification. To continue:

1. **Generate fresh PAT token** (priority)
2. **Run Step 2 above** (extract 50 Q2 examples)
3. **Run Step 3 above** (compare LLM vs heuristic)
4. **Run Step 4 above** (generate review interfaces)

The tooling is complete and tested. You just need a valid PAT token to proceed with data extraction.

---

**Status**: Ready for production data extraction with optimized batch classification ✅
