"""
Artifact Reference Models

Defines artifact types and references for workback plans.
Artifacts can be emails, meetings, chat threads, or documents.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ArtifactType(str, Enum):
    """
    Enum representing different types of artifacts.
    """
    EMAIL = "email"
    MEETING = "meeting"
    CHAT_THREAD = "chat_thread"
    DOCUMENT = "document"


class ArtifactReference(BaseModel):
    """
    Represents a reference to an artifact (meeting, email, document, chat).
    
    Attributes:
        artifact_id: Unique identifier for the artifact
        artifact_type: Type of the artifact (email, meeting, chat_thread, document)
        summary: Optional summary of the artifact content
    """
    artifact_id: Optional[str] = None  # Unique identifier for the artifact
    artifact_type: ArtifactType  # Type of the artifact
    summary: Optional[str] = None  # Summary of the artifact

    def id(self) -> str:
        """
        Get the ID of the artifact reference.
        The ID is a combination of artifact type and artifact ID.
        
        Returns:
            Combined ID string in format "type:id"
        """
        return f"{self.artifact_type.value}:{self.artifact_id}"
