"""
Meeting Classification Prompts

This module provides standardized prompts for meeting classification
based on the official Enterprise Meeting Taxonomy (Chin-Yew Lin).

All classifiers (GPT-5, Ollama, etc.) should use these prompts to ensure
consistency and alignment with the official taxonomy.
"""

import os
from pathlib import Path
from typing import Dict, Optional

# Prompt directory
PROMPT_DIR = Path(__file__).parent

# Prompt version tracking
PROMPT_VERSION = "1.0"
PROMPT_DATE = "2025-10-28"
TAXONOMY_AUTHOR = "Chin-Yew Lin (Microsoft Researcher)"
TAXONOMY_SOURCE = "ContextFlow/docs/cyl/Enterprise_Meeting_Taxonomy.md"


def load_meeting_classification_prompt() -> str:
    """
    Load the official meeting classification prompt.
    
    This prompt contains:
    - Complete Enterprise Meeting Taxonomy (5 categories, 31+ types)
    - Detailed classification guidelines
    - Context signals (attendee count, duration, recurrence)
    - Output format specification
    - Edge case handling
    
    Returns:
        str: The complete prompt text
        
    Raises:
        FileNotFoundError: If prompt file is missing
    """
    prompt_file = PROMPT_DIR / "meeting_classification_prompt.md"
    
    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Meeting classification prompt not found at {prompt_file}. "
            f"This file contains the official taxonomy and must be present."
        )
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_system_message() -> str:
    """
    Extract just the system message portion of the prompt.
    
    Returns:
        str: System message for LLM initialization
    """
    full_prompt = load_meeting_classification_prompt()
    
    # Extract system message section
    lines = full_prompt.split('\n')
    system_msg = []
    in_system = False
    
    for line in lines:
        if line.startswith('## System Message'):
            in_system = True
            continue
        elif line.startswith('##') and in_system:
            break
        elif in_system:
            system_msg.append(line)
    
    return '\n'.join(system_msg).strip()


def get_taxonomy_section() -> str:
    """
    Extract the official taxonomy section.
    
    Returns:
        str: Complete taxonomy with all categories and types
    """
    full_prompt = load_meeting_classification_prompt()
    
    # Extract taxonomy section
    lines = full_prompt.split('\n')
    taxonomy = []
    in_taxonomy = False
    
    for line in lines:
        if line.startswith('## Official Enterprise Meeting Taxonomy'):
            in_taxonomy = True
            continue
        elif line.startswith('##') and in_taxonomy:
            break
        elif in_taxonomy:
            taxonomy.append(line)
    
    return '\n'.join(taxonomy).strip()


def get_classification_guidelines() -> str:
    """
    Extract the classification guidelines section.
    
    Returns:
        str: Guidelines for classification logic
    """
    full_prompt = load_meeting_classification_prompt()
    
    # Extract guidelines section
    lines = full_prompt.split('\n')
    guidelines = []
    in_guidelines = False
    
    for line in lines:
        if line.startswith('## Classification Guidelines'):
            in_guidelines = True
            continue
        elif line.startswith('##') and in_guidelines:
            break
        elif in_guidelines:
            guidelines.append(line)
    
    return '\n'.join(guidelines).strip()


def get_output_format() -> str:
    """
    Extract the output format specification.
    
    Returns:
        str: JSON output format and requirements
    """
    full_prompt = load_meeting_classification_prompt()
    
    # Extract output format section
    lines = full_prompt.split('\n')
    output_fmt = []
    in_output = False
    
    for line in lines:
        if line.startswith('## Output Format'):
            in_output = True
            continue
        elif line.startswith('##') and in_output:
            break
        elif in_output:
            output_fmt.append(line)
    
    return '\n'.join(output_fmt).strip()


def create_classification_prompt(meeting_context: str, style: str = "detailed") -> str:
    """
    Create a complete classification prompt for a specific meeting.
    
    Args:
        meeting_context: Meeting information to classify (title, attendees, etc.)
        style: Prompt style - "detailed" (full prompt) or "compact" (key sections only)
        
    Returns:
        str: Complete prompt ready to send to LLM
    """
    if style == "detailed":
        # Use full prompt
        base_prompt = load_meeting_classification_prompt()
        
        # Remove the markdown header section (first 6 lines)
        lines = base_prompt.split('\n')
        prompt_body = '\n'.join(lines[6:])  # Skip version info header
        
        return f"""{prompt_body}

---

## MEETING TO CLASSIFY

{meeting_context}

Analyze the above meeting information and provide your classification following the output format exactly.
"""
    
    else:  # compact
        system_msg = get_system_message()
        taxonomy = get_taxonomy_section()
        guidelines = get_classification_guidelines()
        output_fmt = get_output_format()
        
        return f"""{system_msg}

{taxonomy}

{guidelines}

{output_fmt}

---

## MEETING TO CLASSIFY

{meeting_context}

Analyze the above meeting information and provide your classification following the output format exactly.
"""


def get_prompt_metadata() -> Dict[str, str]:
    """
    Get metadata about the current prompt version.
    
    Returns:
        dict: Prompt metadata (version, date, author, source)
    """
    return {
        "version": PROMPT_VERSION,
        "date": PROMPT_DATE,
        "taxonomy_author": TAXONOMY_AUTHOR,
        "taxonomy_source": TAXONOMY_SOURCE,
        "prompt_file": str(PROMPT_DIR / "meeting_classification_prompt.md")
    }


# Quick validation on import
try:
    _prompt = load_meeting_classification_prompt()
    _has_taxonomy = "Official Enterprise Meeting Taxonomy" in _prompt
    _has_guidelines = "Classification Guidelines" in _prompt
    _has_output = "Output Format" in _prompt
    
    if not all([_has_taxonomy, _has_guidelines, _has_output]):
        raise ValueError(
            "Meeting classification prompt is incomplete. "
            "Required sections: taxonomy, guidelines, output format."
        )
except Exception as e:
    print(f"WARNING: Meeting classification prompt validation failed: {e}")
