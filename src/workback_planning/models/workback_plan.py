"""
Workback Plan Data Models

Core Pydantic models for workback planning, adapted from Stratos-Exp for Scenara 2.0.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .artifact_reference import ArtifactReference


class HistoryEvent(BaseModel):
    """
    Represents an event that happens to a history item.
    
    Attributes:
        artifact: Reference to the artifact related to the event
        event_time: Time when the event occurred
        event_summary: Summary of the event
    """
    artifact: Optional[ArtifactReference] = None  # Reference to the artifact
    event_time: Optional[datetime] = None  # Time when the event occurred
    event_summary: str  # Summary of the event


class Deliverable(BaseModel):
    """
    Represents a deliverable for an objective.
    
    Attributes:
        id: Unique identifier for the deliverable
        name: Name of the deliverable
        description: Description of the deliverable
        due_date: Optional due date hint for the deliverable
        artifact: Reference to the artifact related to the deliverable
    """
    id: str  # Unique identifier for the deliverable
    name: str  # Name of the deliverable
    description: str  # Description of the deliverable
    due_date: Optional[str] = None  # Optional due date hint
    artifact: Optional[ArtifactReference] = None  # Related artifact


class Participant(BaseModel):
    """
    Represents a participant in a project.
    
    Attributes:
        name: Name of the participant
        email: Email address of the participant
        role: Role of the participant in the project
    """
    name: str  # Name of the participant
    email: str  # Email address of the participant
    role: str  # Role in the project


class Task(BaseModel):
    """
    Represents a task in the workback plan.
    
    Attributes:
        id: Unique identifier for the task
        name: Name of the task
        description: Description of the task
        participants: List of participants involved in the task
        artifacts: List of artifacts related to the task
        dependencies: List of task IDs that this task depends on
        start_date: Start date of the task
        due_date: Optional due date hint for the task
    """
    id: str  # Unique identifier for the task
    name: str  # Name of the task
    description: str  # Description of the task
    participants: List[Participant] = []  # Participants involved
    artifacts: List[ArtifactReference] = []  # Related artifacts
    dependencies: List[str] = []  # Task IDs this task depends on
    start_date: Optional[datetime] = None  # Start date of the task
    due_date: Optional[str] = None  # Optional due date hint


class WorkbackPlan(BaseModel):
    """
    Represents a workback plan for a project.
    
    Attributes:
        summary: Brief textual description of the workback plan
        history: List of history events related to the project
        deliverables: List of deliverables for the project
        participants: List of participants involved in the project
        artifact_references: List of artifact references related to the project
        tasks: List of tasks in the workback plan
        notes: List of notes related to the project
    """
    summary: str  # Brief description of the workback plan
    history: List[HistoryEvent] = []  # History events
    deliverables: List[Deliverable] = []  # Project deliverables
    participants: List[Participant] = []  # Project participants
    artifact_references: List[ArtifactReference] = []  # Artifact references
    tasks: List[Task] = []  # Tasks in the workback plan
    notes: List[str] = []  # Notes related to the project
