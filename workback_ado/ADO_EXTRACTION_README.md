# Azure DevOps Work Item Extraction for Workback Planning

## Overview

This script extracts completed work items from Azure DevOps to create high-quality training data for workback planning post-training. It focuses on Q2 (high value, low complexity) work items as the initial pilot, implementing the strategy outlined in `ADO_POST_TRAINING_PROPOSAL.md`.

## Features

✅ **Automatic Classification**: Classifies work items by complexity (Q2/Q3/Q1) and value (High/Medium/Low)  
✅ **Outcome Labels**: Generates effort variance, schedule variance, and outcome classification  
✅ **Dependency Extraction**: Extracts predecessor/successor and parent/child relationships  
✅ **Data Quality Assessment**: Reports completeness of estimates, actuals, dependencies  
✅ **Flexible Filtering**: Filter by complexity, value, date range, story points  

## Prerequisites

### 1. Install Azure DevOps SDK

```bash
pip install azure-devops
```

### 2. Get Personal Access Token (PAT)

1. Go to Azure DevOps: `https://dev.azure.com/your-org`
2. Click on **User Settings** → **Personal Access Tokens**
3. Click **New Token**
4. Set scopes:
   - ✅ **Work Items (Read)**
   - ✅ **Analytics (Read)** (optional, for advanced queries)
5. Copy the token (save securely!)

### 3. Identify Target Project

- You need the exact project name (case-sensitive)
- Example: `"MyProject"` or `"Contoso.WebApp"`

## Quick Start

### Basic Usage (Q2 Pilot - 50 Examples)

```bash
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/your-org \
  --pat-token YOUR_PAT_TOKEN_HERE \
  --project YourProjectName \
  --max-examples 50 \
  --complexity Q2_Low_Complexity \
  --value High_Value
```

### Using Environment Variable for PAT

```bash
# Set environment variable
export ADO_PAT="your_pat_token_here"

# Run script (use 'env' for --pat-token)
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/your-org \
  --pat-token env \
  --project YourProjectName
```

### Extract All Complexities and Values

```bash
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/your-org \
  --pat-token env \
  --project YourProjectName \
  --complexity all \
  --value all \
  --max-examples 200
```

### Customize Date Range

```bash
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/your-org \
  --pat-token env \
  --project YourProjectName \
  --months-back 12 \
  --max-examples 100
```

## Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--org-url` | ✅ Yes | - | Azure DevOps org URL (e.g., https://dev.azure.com/contoso) |
| `--pat-token` | ✅ Yes | - | Personal Access Token (or 'env' to use $ADO_PAT) |
| `--project` | ✅ Yes | - | Project name (case-sensitive) |
| `--months-back` | No | 6 | How many months back to look for closed items |
| `--max-examples` | No | 50 | Maximum training examples to extract |
| `--complexity` | No | Q2_Low_Complexity | Target complexity (Q2/Q3/Q1/all) |
| `--value` | No | High_Value | Target value (High/Medium/Low/all) |
| `--output` | No | ado_workback_training_data.json | Output JSON file |
| `--stats-output` | No | ado_workback_statistics.json | Statistics output file |

## Output Files

### 1. Training Data: `ado_workback_training_data.json`

```json
[
  {
    "training_id": "ado_12345",
    "source": "azure_devops",
    "context": {
      "goal": "Implement OAuth authentication",
      "description": "Add OAuth support for Google and Microsoft accounts",
      "work_item_type": "User Story",
      "priority": 1,
      "business_value": 50,
      "tags": ["customer-committed", "security"],
      "assigned_to": "Alice Smith"
    },
    "plan": {
      "task": {
        "id": 12345,
        "title": "Implement OAuth authentication",
        "estimated_hours": 80,
        "actual_hours": 120,
        "story_points": 8,
        "state": "Closed",
        "created_date": "2025-09-01T00:00:00",
        "closed_date": "2025-09-18T00:00:00"
      },
      "dependencies": [
        {
          "type": "predecessor",
          "from": 12340,
          "to": 12345
        }
      ]
    },
    "outcome": {
      "work_item_id": 12345,
      "effort_variance": 1.5,
      "effort_outcome": "significantly_over",
      "schedule_variance_days": 3,
      "schedule_outcome": "slightly_late",
      "overall_outcome": "partial_success"
    },
    "metadata": {
      "project": "YourProject",
      "work_item_id": 12345,
      "work_item_url": "https://dev.azure.com/your-org/YourProject/_workitems/edit/12345",
      "complexity": "Q2_Low_Complexity",
      "value": "High_Value",
      "extracted_date": "2025-11-11T10:30:00"
    }
  }
]
```

### 2. Statistics: `ado_workback_statistics.json`

```json
{
  "total_examples": 50,
  "complexity_distribution": {
    "Q2_Low_Complexity": 45,
    "Q3_Medium_Complexity": 5
  },
  "value_distribution": {
    "High_Value": 48,
    "Medium_Value": 2
  },
  "outcome_distribution": {
    "success": 30,
    "partial_success": 15,
    "delayed": 5
  },
  "work_item_types": {
    "User Story": 40,
    "Task": 10
  },
  "average_story_points": 6.2,
  "average_effort_variance": 1.25,
  "data_quality": {
    "has_estimate": "85.0%",
    "has_actual": "82.0%",
    "has_dependencies": "48.0%",
    "has_description": "92.0%"
  }
}
```

## Complexity Classification Algorithm

The script automatically classifies work items into Q2/Q3/Q1 based on:

### Q2: Low Complexity (Score 0-3)
- Story points: 1-5
- Dependencies: <5 links
- Duration: <30 days (~2 sprints)
- **Example**: Single-team feature, clear scope, 1-2 week delivery

### Q3: Medium Complexity (Score 4-6)
- Story points: 5-8
- Dependencies: 5-15 links
- Duration: 30-90 days (~2-4 sprints)
- **Example**: Cross-team feature, moderate dependencies

### Q1: High Complexity (Score 7+)
- Story points: 13+
- Dependencies: 15+ links
- Duration: 90+ days (4+ sprints)
- **Example**: Platform migration, multiple teams, complex dependencies

## Value Classification Algorithm

Work items classified as High/Medium/Low value based on:

### High Value (Score 6+)
- Priority: P0 or P1
- Business value: ≥50
- Tags: "customer-committed", "roadmap", "OKR"
- Has hard deadline with external commitment

### Medium Value (Score 3-5)
- Priority: P2
- Business value: 20-49
- Some stakeholder visibility

### Low Value (Score 0-2)
- Priority: P3 or lower
- Business value: <20
- Internal improvements, technical debt

## Data Quality Thresholds

For high-quality training data, look for:

✅ **>80% has_estimate**: Most items have original estimates  
✅ **>80% has_actual**: Most items have completed work logged  
✅ **>50% has_dependencies**: Good coverage of task relationships  
✅ **>90% has_description**: Rich context available  

If your data quality is low:
1. Check if team consistently logs estimates and actuals
2. Consider focusing on recent work (better data hygiene)
3. May need more manual curation by experts

## Example Workflows

### Workflow 1: Pilot Extraction (50 Q2 Examples)

```bash
# Step 1: Extract Q2 high-value work items
export ADO_PAT="your_token"
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/contoso \
  --pat-token env \
  --project "WebApp" \
  --max-examples 50 \
  --complexity Q2_Low_Complexity \
  --value High_Value \
  --output pilot_q2_examples.json

# Step 2: Review statistics
cat ado_workback_statistics.json

# Step 3: Send pilot_q2_examples.json to expert reviewers
```

### Workflow 2: Scale to 200 Mixed Examples

```bash
# Extract 200 examples with mix of complexities
python ado_workback_extraction.py \
  --org-url https://dev.azure.com/contoso \
  --pat-token env \
  --project "WebApp" \
  --max-examples 200 \
  --complexity all \
  --value all \
  --months-back 12 \
  --output scaled_mixed_examples.json

# Filter by complexity in post-processing if needed
```

### Workflow 3: Multiple Projects

```bash
# Extract from multiple projects
for project in "WebApp" "MobileApp" "Backend"; do
  python ado_workback_extraction.py \
    --org-url https://dev.azure.com/contoso \
    --pat-token env \
    --project "$project" \
    --max-examples 30 \
    --output "ado_${project}_examples.json"
done

# Merge files manually or with jq
jq -s 'add' ado_*_examples.json > ado_all_projects.json
```

## Troubleshooting

### Error: "azure-devops not installed"

```bash
pip install azure-devops
```

### Error: "Authentication failed"

1. Verify PAT token is correct
2. Check token hasn't expired
3. Verify token has "Work Items (Read)" permission
4. Try creating a new token

### Error: "No work items found"

Possible causes:
- Project name is incorrect (check capitalization)
- No closed work items in date range (try --months-back=12)
- Work items don't have story points (adjust filtering)
- Query permissions issue

### Low Data Quality (<50% completeness)

Solutions:
- Use more recent data (--months-back=3)
- Focus on teams with better data hygiene
- Accept lower completeness for pilot
- Plan for more expert curation

### Too Few Q2 Examples

Try:
- Increase date range: `--months-back=12`
- Relax complexity filter: `--complexity=all`
- Include Q3 examples: they're also low complexity
- Check if org uses different story point scale

## Integration with Scenara

After extracting ADO data, integrate with Scenara:

1. **Add meeting context**: Link work items to planning meetings
2. **Enrich with collaborator data**: Add Scenara's relationship intelligence
3. **Expert review**: Send to PMs for plan correction
4. **Training pipeline**: Feed corrected examples to model training

See `ADO_POST_TRAINING_PROPOSAL.md` for complete integration strategy.

## Next Steps

After extraction:

1. **Review Data Quality**: Check `ado_workback_statistics.json`
2. **Expert Review**: Send training examples to PM experts for correction
3. **Build Expert Correction UI**: Create interface for PMs to correct plans
4. **Model Training**: Use corrected examples for fine-tuning
5. **Continuous Learning**: Setup pipeline to extract new completed work items monthly

## Security Best Practices

🔒 **Never commit PAT tokens to Git**

```bash
# Add to .gitignore
echo "*.token" >> .gitignore
echo ".env" >> .gitignore

# Store in environment or secure vault
export ADO_PAT="your_token"

# Or use Azure Key Vault for production
```

## License

Part of Scenara 2.0 - Enterprise Meeting Intelligence System

---

**Author**: Chin-Yew Lin  
**Date**: November 11, 2025  
**Related Docs**: `ADO_POST_TRAINING_PROPOSAL.md`, `STRATOS_EXP_EVALUATION_ANALYSIS_V2.md`
