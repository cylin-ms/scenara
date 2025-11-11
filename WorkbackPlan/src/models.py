"""
WorkbackPlan - Intelligent Project Timeline Management
Core data models and types
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    """Project lifecycle status"""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    """Task completion status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(str, Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DependencyType(str, Enum):
    """Types of task dependencies"""
    FINISH_TO_START = "finish_to_start"  # Task B starts when Task A finishes
    START_TO_START = "start_to_start"    # Task B starts when Task A starts
    FINISH_TO_FINISH = "finish_to_finish"  # Task B finishes when Task A finishes
    START_TO_FINISH = "start_to_finish"  # Task B finishes when Task A starts


class TeamMember(BaseModel):
    """Team member with capacity information"""
    id: str
    name: str
    email: str
    role: str
    capacity_hours_per_week: float = 40.0
    skills: List[str] = []


class Dependency(BaseModel):
    """Task or milestone dependency"""
    from_id: str = Field(..., description="Prerequisite task/milestone ID")
    to_id: str = Field(..., description="Dependent task/milestone ID")
    dependency_type: DependencyType = DependencyType.FINISH_TO_START
    lag_days: int = Field(0, description="Buffer days between tasks")


class Task(BaseModel):
    """Individual work item"""
    id: str
    name: str
    description: str
    estimated_duration_hours: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner: str
    dependencies: List[str] = []  # Task IDs
    milestone_id: str
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: Priority = Priority.MEDIUM
    
    # Scheduling metadata
    early_start: Optional[datetime] = None
    early_finish: Optional[datetime] = None
    late_start: Optional[datetime] = None
    late_finish: Optional[datetime] = None
    
    @property
    def slack_hours(self) -> Optional[float]:
        """Calculate slack time (float) for this task"""
        if self.late_start and self.early_start:
            return (self.late_start - self.early_start).total_seconds() / 3600
        return None
    
    @property
    def is_critical(self) -> bool:
        """Check if task is on critical path (zero slack)"""
        slack = self.slack_hours
        return slack is not None and slack == 0


class Milestone(BaseModel):
    """Major project checkpoint"""
    id: str
    name: str
    target_date: datetime
    description: str
    deliverables: List[str] = []
    owner: str
    dependencies: List[str] = []  # IDs of other milestones
    tasks: List[str] = []  # IDs of tasks required
    
    # Calculated dates
    calculated_date: Optional[datetime] = None
    buffer_days: int = 0


class Project(BaseModel):
    """Complete project with timeline"""
    id: str
    name: str
    target_date: datetime
    start_date: Optional[datetime] = None
    description: str
    owner: str
    milestones: List[Milestone] = []
    tasks: List[Task] = []
    dependencies: List[Dependency] = []
    team_members: List[TeamMember] = []
    status: ProjectStatus = ProjectStatus.PLANNING
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return next((t for t in self.tasks if t.id == task_id), None)
    
    def get_milestone(self, milestone_id: str) -> Optional[Milestone]:
        """Get milestone by ID"""
        return next((m for m in self.milestones if m.id == milestone_id), None)
    
    def get_critical_path(self) -> List[Task]:
        """Get tasks on the critical path"""
        return [task for task in self.tasks if task.is_critical]


class WorkbackSchedule(BaseModel):
    """Generated workback schedule with analysis"""
    project: Project
    generated_at: datetime = Field(default_factory=datetime.now)
    
    # Analysis results
    total_duration_days: int
    critical_path_tasks: List[str]  # Task IDs
    risk_score: float = 0.0
    feasibility_score: float = 1.0
    
    # Recommendations
    warnings: List[str] = []
    recommendations: List[str] = []
    
    def export_to_dict(self) -> dict:
        """Export schedule to dictionary"""
        return {
            "project": self.project.dict(),
            "generated_at": self.generated_at.isoformat(),
            "analysis": {
                "total_duration_days": self.total_duration_days,
                "critical_path_tasks": self.critical_path_tasks,
                "risk_score": self.risk_score,
                "feasibility_score": self.feasibility_score
            },
            "warnings": self.warnings,
            "recommendations": self.recommendations
        }
