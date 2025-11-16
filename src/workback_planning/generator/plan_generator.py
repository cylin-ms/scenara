"""
Workback Plan Generator

Generates workback plans using a two-stage LLM pipeline:
1. Analysis stage: O1 reasoning to break down objectives and create WBS
2. Structuring stage: GPT-4 to convert analysis into structured JSON

Adapted from Stratos-Exp for Scenara 2.0 with LLMAPIClient integration.
"""

import json
import os
from string import Template
from typing import Optional, Dict, Any

# Import Scenara's LLM client
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from tools.llm_api import LLMAPIClient


# Get current directory for prompt templates
_cur_path = os.path.dirname(os.path.abspath(__file__))
_prompts_path = os.path.join(os.path.dirname(_cur_path), 'prompts')


def _get_analyze_prompt() -> str:
    """Load the analysis prompt template"""
    file_path = os.path.join(_prompts_path, 'analyze.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def _get_structure_prompt() -> str:
    """Load the structuring prompt template"""
    file_path = os.path.join(_prompts_path, 'structure.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def _get_doc_format() -> str:
    """Load the document format schema"""
    file_path = os.path.join(_prompts_path, 'doc_format.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Model configurations for two-stage pipeline
_analysis_model = {
    "provider": "openai",  # O1 available only via OpenAI
    "model": "o1-preview",  # Use o1-preview as o1 is not yet available
    "temperature": 1.0  # O1 doesn't support reasoning_effort in standard API
}

_structure_model = {
    "provider": "openai",
    "model": "gpt-4o",  # Use gpt-4o (gpt-4.1 not yet available)
    "temperature": 0.1
}


def _generate_analysis(
    context: str,
    client: Optional[LLMAPIClient] = None,
    model_override: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate analysis using O1 reasoning model.
    
    Args:
        context: User context describing the objectives and constraints
        client: LLMAPIClient instance (creates new if None)
        model_override: Optional model configuration override
    
    Returns:
        Analysis text with hierarchical breakdown
    """
    client = client or LLMAPIClient()
    model_config = model_override or _analysis_model
    
    # Load and substitute the analyze prompt template
    prompt_template = Template(_get_analyze_prompt())
    prompt = prompt_template.substitute(context=context)
    
    # Query LLM
    try:
        response = client.query_llm(
            prompt=prompt,
            provider=model_config.get("provider", "openai"),
            model=model_config.get("model", "o1-preview"),
            base_url=model_config.get("base_url"),
            temperature=model_config.get("temperature"),
            timeout=model_config.get("timeout", 300.0)  # 5 minute default for analysis
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to generate analysis: {e}")


def _generate_structured(
    analysis: str,
    client: Optional[LLMAPIClient] = None,
    model_override: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Convert analysis to structured JSON using GPT-4.
    
    Args:
        analysis: Analysis text from _generate_analysis
        client: LLMAPIClient instance (creates new if None)
        model_override: Optional model configuration override
    
    Returns:
        Structured workback plan as dictionary
    """
    client = client or LLMAPIClient()
    model_config = model_override or _structure_model
    
    # Load and substitute the structure prompt template
    structure_template = Template(_get_structure_prompt())
    prompt = structure_template.substitute(
        docformat=_get_doc_format(),
        analysis=analysis
    )
    
    # Query LLM
    try:
        response = client.query_llm(
            prompt=prompt,
            provider=model_config.get("provider", "openai"),
            model=model_config.get("model", "gpt-4o"),
            base_url=model_config.get("base_url"),
            temperature=model_config.get("temperature"),
            timeout=model_config.get("timeout", 180.0)  # 3 minute default for structuring
        )
        
        # Parse JSON response
        structured = json.loads(response)
        return structured
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse structured response: {e}\nResponse: {response}")
    except Exception as e:
        raise RuntimeError(f"Failed to generate structured plan: {e}")


def generate_plan(
    context: str,
    client: Optional[LLMAPIClient] = None,
    analysis_model_override: Optional[Dict[str, Any]] = None,
    structure_model_override: Optional[Dict[str, Any]] = None,
    generate_structured: bool = True
) -> Dict[str, Any]:
    """
    Generate a workback plan based on the given context.
    
    This implements a two-stage pipeline:
    1. Analysis stage: Use O1 for deep reasoning and hierarchical breakdown
    2. Structuring stage: Use GPT-4 to convert analysis into structured JSON
    
    Args:
        context: User context describing objectives, constraints, participants, artifacts
        client: LLMAPIClient instance (creates new if None)
        analysis_model_override: Optional override for analysis model config
        structure_model_override: Optional override for structure model config
        generate_structured: If True, generate structured JSON; if False, return only analysis
    
    Returns:
        Dictionary with 'analysis' (str) and 'structured' (dict or None) keys
    
    Example:
        >>> context = '''
        ... Meeting: Product Launch Planning
        ... Date: 2025-12-15
        ... Participants: PM (alice@example.com), Engineering Lead (bob@example.com)
        ... Goal: Launch new feature by target date
        ... '''
        >>> result = generate_plan(context)
        >>> print(result['analysis'])  # Markdown analysis
        >>> print(result['structured'])  # JSON workback plan
    """
    client = client or LLMAPIClient()
    
    # Stage 1: Generate analysis with O1
    print("Stage 1: Generating analysis with O1...")
    analysis = _generate_analysis(context, client, analysis_model_override)
    
    # Stage 2: Convert to structured JSON with GPT-4
    structured = None
    if generate_structured:
        print("Stage 2: Converting to structured JSON with GPT-4...")
        structured = _generate_structured(analysis, client, structure_model_override)
    
    return {
        'analysis': analysis,
        'structured': structured
    }
