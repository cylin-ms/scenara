# Meeting Classification Prompt System

**Version**: 1.0  
**Date**: October 28, 2025  
**Status**: Active

---

## Overview

The Meeting Classification Prompt System provides a **centralized, standardized prompt** for all meeting classifiers in the Scenara 2.0 project. This ensures:

1. **Consistency** - All classifiers use the same official Enterprise Meeting Taxonomy
2. **Maintainability** - Update prompt once, applies to all classifiers
3. **Traceability** - Prompt version tracked in experiment results
4. **Quality** - Based on Chin-Yew Lin's research taxonomy (>95% coverage)

---

## Architecture

### Directory Structure

```
prompts/
├── __init__.py                          # Prompt loading module
└── meeting_classification_prompt.md    # Official taxonomy and guidelines
```

### Classifiers Using This System

1. **GPT-5 Classifier** (`tools/meeting_classifier_gpt5.py`)
   - Model: dev-gpt-5-chat-jj
   - Provider: Microsoft SilverFlow LLM API
   - Updated: October 28, 2025

2. **Ollama Classifier** (`tools/meeting_classifier.py`)
   - Model: gpt-oss:20b (or user-specified)
   - Provider: Local Ollama
   - Updated: October 28, 2025

3. **Future Classifiers**
   - Any new classifier should import from `prompts/`
   - Ensures taxonomy alignment out of the box

---

## Prompt Components

### 1. System Message
```python
from prompts import get_system_message

system_msg = get_system_message()
# Returns: Expert business analyst role description
```

**Purpose**: Define the LLM's role and expertise for classification tasks.

### 2. Official Taxonomy
```python
from prompts import get_taxonomy_section

taxonomy = get_taxonomy_section()
# Returns: Complete 5-category, 31+ type taxonomy with descriptions
```

**Structure**:
1. **Internal Recurring Meetings (Cadence)** - 5 types
2. **Strategic Planning & Decision Meetings** - 5 types
3. **External & Client-Facing Meetings** - 5 types
4. **Informational & Broadcast Meetings** - 4 types
5. **Team-Building & Culture Meetings** - 3 types

**Each Type Includes**:
- Purpose description
- Example meetings
- Context signals (attendee count, duration, recurrence)
- Key indicator keywords

### 3. Classification Guidelines
```python
from prompts import get_classification_guidelines

guidelines = get_classification_guidelines()
# Returns: Primary purpose principle, context signals, confidence calibration
```

**Key Principles**:
- Identify PRIMARY purpose (meetings may blend types)
- Use context signals: attendee count, duration, recurrence, external domains
- Apply confidence calibration (95-99% = clear, 85-94% = strong, 75-84% = moderate)

### 4. Output Format
```python
from prompts import get_output_format

output_fmt = get_output_format()
# Returns: JSON schema and requirements
```

**Required Fields**:
```json
{
  "specific_type": "exact meeting type from taxonomy",
  "primary_category": "one of 5 main categories",
  "confidence": 0.95,
  "reasoning": "2-3 sentences citing signals",
  "key_indicators": ["signal 1", "signal 2", "signal 3"]
}
```

---

## Usage Guide

### For Classifier Development

#### Step 1: Import Prompt Functions
```python
from prompts import (
    create_classification_prompt,
    get_prompt_metadata,
    get_system_message
)
```

#### Step 2: Initialize with Metadata
```python
class MyClassifier:
    def __init__(self):
        self.prompt_metadata = get_prompt_metadata()
        print(f"Using prompt version {self.prompt_metadata['version']}")
```

#### Step 3: Create Classification Prompt
```python
def classify_meeting(self, subject, description, attendees, duration):
    # Prepare meeting context
    meeting_context = f"""
    Meeting Title: {subject}
    Description: {description}
    Attendees: {len(attendees)} people
    Duration: {duration} minutes
    """
    
    # Get complete prompt (uses official taxonomy)
    prompt = create_classification_prompt(meeting_context, style="detailed")
    
    # Send to LLM...
```

#### Step 4: Use System Message
```python
system_msg = get_system_message()

response = llm_client.chat(
    messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]
)
```

#### Step 5: Track Prompt Version in Results
```python
result = {
    "specific_type": "...",
    "confidence": 0.95,
    # ... other fields ...
    "prompt_version": self.prompt_metadata['version'],
    "taxonomy_source": self.prompt_metadata['taxonomy_source']
}
```

---

## Prompt Styles

### Detailed Style (Recommended)
```python
prompt = create_classification_prompt(meeting_context, style="detailed")
```

**Includes**:
- Complete taxonomy with descriptions
- Full classification guidelines
- Context signal explanations
- Edge case handling
- Output format specification

**Use When**: Running experiments, high-accuracy classification, ample token budget

### Compact Style
```python
prompt = create_classification_prompt(meeting_context, style="compact")
```

**Includes**:
- Key taxonomy types
- Essential guidelines
- Output format

**Use When**: Token constraints, batch processing, real-time classification

---

## Version Tracking

### Current Version
- **Version**: 1.0
- **Date**: 2025-10-28
- **Taxonomy Author**: Chin-Yew Lin (Microsoft Researcher)
- **Source**: ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md

### Getting Metadata Programmatically
```python
from prompts import get_prompt_metadata

metadata = get_prompt_metadata()
# {
#   "version": "1.0",
#   "date": "2025-10-28",
#   "taxonomy_author": "Chin-Yew Lin (Microsoft Researcher)",
#   "taxonomy_source": "ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md",
#   "prompt_file": "/path/to/prompts/meeting_classification_prompt.md"
# }
```

### Experiment Tracking
All experiments should include prompt metadata:
```json
{
  "experiment_id": "meeting_classification_20251028_003",
  "classifier": {
    "model": "dev-gpt-5-chat-jj",
    "provider": "Microsoft SilverFlow",
    "prompt_version": "1.0",
    "taxonomy_source": "ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md"
  },
  "results": [...]
}
```

---

## Taxonomy Alignment History

### Discovery (October 28, 2025)

**Issue Found**: GPT-5 Experiment 002 showed 50% over-concentration in "Progress Review Meeting"

**Root Cause**: GPT-5 classifier was using **simplified taxonomy** (abbreviated categories without descriptions)

**Evidence**:
- GPT-5 original: Abbreviated type names only
- GitHub Copilot: Full taxonomy in context
- Result: GPT-5 96% confidence but 50% concentrated

**Fix Applied**:
1. Created `prompts/meeting_classification_prompt.md` with complete official taxonomy
2. Created `prompts/__init__.py` for programmatic access
3. Updated `tools/meeting_classifier_gpt5.py` to import from `prompts/`
4. Updated `tools/meeting_classifier.py` (Ollama) to import from `prompts/`

**Key Lesson**: **NEVER abbreviate the taxonomy** - Full descriptions and context signals are essential for accurate classification.

---

## Quality Assurance

### Prompt Validation (Automatic)
The `prompts/__init__.py` module validates on import:
```python
# Validates that prompt contains required sections
_has_taxonomy = "Official Enterprise Meeting Taxonomy" in _prompt
_has_guidelines = "Classification Guidelines" in _prompt
_has_output = "Output Format" in _prompt
```

### Testing Checklist
Before running experiments:
- [ ] Prompt file exists: `prompts/meeting_classification_prompt.md`
- [ ] Classifier imports from `prompts/`
- [ ] System message uses `get_system_message()`
- [ ] Classification prompt uses `create_classification_prompt()`
- [ ] Results include `prompt_version` metadata

---

## Updating the Prompt

### When to Update
- New meeting types discovered (taxonomy expansion)
- Classification guidelines refined
- Context signal improvements
- Edge case handling additions

### Update Process
1. **Edit**: `prompts/meeting_classification_prompt.md`
2. **Version Bump**: Update `PROMPT_VERSION` in `prompts/__init__.py`
3. **Document**: Note changes in this file
4. **Test**: Run experiments with both old and new versions
5. **Compare**: Analyze impact on classification quality
6. **Commit**: Include version number in commit message

### Backward Compatibility
- Keep old prompt versions in `prompts/archive/`
- Experiment results track prompt version
- Can reproduce old results using archived prompts

---

## Examples

### Example 1: GPT-5 Classifier
```python
# tools/meeting_classifier_gpt5.py

from prompts import create_classification_prompt, get_system_message

class GPT5MeetingClassifier:
    def _create_classification_prompt(self, meeting_context: str) -> str:
        """Use standardized prompt from prompts/"""
        return create_classification_prompt(meeting_context, style="detailed")
    
    def classify_meeting(self, meeting_data):
        context = self._prepare_meeting_context(meeting_data)
        prompt = self._create_classification_prompt(context)
        
        # Send to GPT-5...
        response = self.llm_client.chat(
            messages=[
                {"role": "system", "content": get_system_message()},
                {"role": "user", "content": prompt}
            ]
        )
        # Parse and return...
```

### Example 2: Ollama Classifier
```python
# tools/meeting_classifier.py

from prompts import create_classification_prompt, get_prompt_metadata

class OllamaLLMMeetingClassifier:
    def __init__(self, model_name="gpt-oss:20b"):
        self.model_name = model_name
        self.prompt_metadata = get_prompt_metadata()
    
    def _create_classification_prompt(self, meeting_context: str) -> str:
        """Use standardized prompt from prompts/"""
        return create_classification_prompt(meeting_context, style="detailed")
    
    def classify_meeting(self, subject, description, attendees, duration):
        context = self._prepare_meeting_context(subject, description, attendees, duration)
        prompt = self._create_classification_prompt(context)
        
        # Send to Ollama...
        response = self.client.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": get_system_message()},
                {"role": "user", "content": prompt}
            ]
        )
        # Parse and add metadata...
        result['prompt_version'] = self.prompt_metadata['version']
        return result
```

---

## Benefits

### 1. Consistency
- All classifiers use **same taxonomy**
- Same classification principles
- Same output format

### 2. Maintainability
- **One file to update**: `prompts/meeting_classification_prompt.md`
- Changes propagate to all classifiers
- No code changes needed for taxonomy updates

### 3. Traceability
- Prompt version in every result
- Can reproduce experiments
- Track taxonomy evolution impact

### 4. Quality
- Based on **official research** (Chin-Yew Lin)
- >95% business meeting coverage
- Detailed context signals
- Edge case handling

### 5. Collaboration
- Shared understanding across team
- Easy to onboard new classifiers
- Centralized taxonomy source of truth

---

## Future Enhancements

### Planned
- [ ] Multi-language support (prompt translations)
- [ ] Few-shot examples in prompt
- [ ] Domain-specific taxonomy variants (healthcare, finance, etc.)
- [ ] Prompt A/B testing framework
- [ ] Automated prompt optimization based on experiment results

### Ideas
- LLM-powered prompt refinement
- User feedback incorporation
- Taxonomy expansion based on edge cases
- Prompt compression for token efficiency

---

## References

1. **Official Taxonomy**: `ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md`
2. **Taxonomy Author**: Chin-Yew Lin (Microsoft Researcher)
3. **Discovery Document**: `experiments/TAXONOMY_ALIGNMENT.md`
4. **Lessons Learned**: `.cursorrules` (Taxonomy Alignment section)

---

**Maintained By**: Scenara 2.0 Project Team  
**Last Updated**: October 28, 2025  
**Next Review**: After 50+ classifications or 30 days
