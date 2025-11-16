"""
Workback Planning Module for Scenara 2.0

This module provides AI-powered workback planning capabilities adapted from Stratos-Exp.
It uses a two-stage LLM pipeline to generate comprehensive project plans from meeting context.

Key Components:
- Models: Pydantic data models for workback plans, tasks, deliverables
- Generator: Two-stage LLM pipeline (O1 analysis + GPT-4 structuring)
- Evaluator: Quality assessment (to be implemented)

Usage:
    from src.workback_planning import generate_plan
    
    context = '''
    Meeting: Product Launch Planning
    Date: 2025-12-15
    Participants: PM, Engineering Lead, Marketing
    Goal: Launch new feature by target date
    '''
    
    result = generate_plan(context)
    print(result['analysis'])  # Markdown analysis
    print(result['structured'])  # JSON workback plan
"""

from .generator import generate_plan
from .models import (
    WorkbackPlan,
    Task,
    Deliverable,
    Participant,
    HistoryEvent,
    ArtifactReference,
    ArtifactType
)

__version__ = "1.0.0"

__all__ = [
    'generate_plan',
    'WorkbackPlan',
    'Task',
    'Deliverable',
    'Participant',
    'HistoryEvent',
    'ArtifactReference',
    'ArtifactType'
]
