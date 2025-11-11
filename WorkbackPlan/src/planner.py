"""
WorkbackPlan - Core scheduling engine
Implements workback scheduling algorithm and critical path analysis
"""

from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple
import networkx as nx

from .models import (
    Project, Task, Milestone, Dependency,
    DependencyType, WorkbackSchedule
)


class WorkbackPlanner:
    """Main workback planning engine"""
    
    def __init__(self, project: Project):
        """
        Initialize planner with project
        
        Args:
            project: Project to schedule
        """
        self.project = project
        self.dependency_graph: nx.DiGraph = None
        
    def generate(self) -> WorkbackSchedule:
        """
        Generate complete workback schedule
        
        Returns:
            WorkbackSchedule with calculated dates and analysis
        """
        # Step 1: Build dependency graph
        self.dependency_graph = self._build_dependency_graph()
        
        # Step 2: Calculate critical path
        critical_path = self._calculate_critical_path()
        
        # Step 3: Schedule backwards from target date
        self._schedule_backwards()
        
        # Step 4: Calculate project start date
        start_date = self._calculate_start_date()
        self.project.start_date = start_date
        
        # Step 5: Analyze and generate recommendations
        analysis = self._analyze_schedule()
        
        # Create workback schedule
        schedule = WorkbackSchedule(
            project=self.project,
            total_duration_days=(self.project.target_date - start_date).days,
            critical_path_tasks=[task.id for task in critical_path],
            **analysis
        )
        
        return schedule
    
    def _build_dependency_graph(self) -> nx.DiGraph:
        """
        Build directed graph of task dependencies
        
        Returns:
            NetworkX directed graph
        """
        G = nx.DiGraph()
        
        # Add all tasks as nodes
        for task in self.project.tasks:
            G.add_node(task.id, task=task)
        
        # Add dependency edges
        for dep in self.project.dependencies:
            # Add edge weight as lag days
            G.add_edge(dep.from_id, dep.to_id, weight=dep.lag_days)
        
        # Check for cycles
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("Circular dependencies detected in project")
        
        return G
    
    def _calculate_critical_path(self) -> List[Task]:
        """
        Calculate critical path using CPM (Critical Path Method)
        
        Returns:
            List of tasks on critical path
        """
        # Forward pass: Calculate earliest start/finish times
        self._forward_pass()
        
        # Backward pass: Calculate latest start/finish times
        self._backward_pass()
        
        # Identify critical tasks (zero slack)
        critical_tasks = [
            task for task in self.project.tasks
            if task.is_critical
        ]
        
        return critical_tasks
    
    def _forward_pass(self):
        """Calculate early start and early finish times"""
        # Process tasks in topological order
        for task_id in nx.topological_sort(self.dependency_graph):
            task = self.project.get_task(task_id)
            
            # Get predecessors
            predecessors = list(self.dependency_graph.predecessors(task_id))
            
            if not predecessors:
                # No predecessors: start at project start
                task.early_start = self.project.start_date or datetime.now()
            else:
                # Start after all predecessors finish
                earliest_start = max(
                    self.project.get_task(pred_id).early_finish
                    for pred_id in predecessors
                )
                task.early_start = earliest_start
            
            # Calculate early finish
            duration = timedelta(hours=task.estimated_duration_hours)
            task.early_finish = task.early_start + duration
    
    def _backward_pass(self):
        """Calculate late start and late finish times"""
        # Process tasks in reverse topological order
        for task_id in reversed(list(nx.topological_sort(self.dependency_graph))):
            task = self.project.get_task(task_id)
            
            # Get successors
            successors = list(self.dependency_graph.successors(task_id))
            
            if not successors:
                # No successors: must finish by project target
                task.late_finish = self.project.target_date
            else:
                # Must finish before all successors start
                latest_finish = min(
                    self.project.get_task(succ_id).late_start
                    for succ_id in successors
                )
                task.late_finish = latest_finish
            
            # Calculate late start
            duration = timedelta(hours=task.estimated_duration_hours)
            task.late_start = task.late_finish - duration
    
    def _schedule_backwards(self):
        """
        Schedule tasks backwards from target date
        Sets actual start/end dates for tasks
        """
        # Sort milestones by target date (latest first)
        sorted_milestones = sorted(
            self.project.milestones,
            key=lambda m: m.target_date,
            reverse=True
        )
        
        for milestone in sorted_milestones:
            # Get tasks for this milestone
            milestone_tasks = [
                task for task in self.project.tasks
                if task.milestone_id == milestone.id
            ]
            
            # Schedule tasks ending at milestone date
            current_date = milestone.target_date
            
            for task in reversed(milestone_tasks):
                duration = timedelta(hours=task.estimated_duration_hours)
                task.end_date = current_date
                task.start_date = current_date - duration
                current_date = task.start_date
    
    def _calculate_start_date(self) -> datetime:
        """
        Calculate project start date based on scheduled tasks
        
        Returns:
            Earliest task start date
        """
        if not self.project.tasks:
            return self.project.target_date
        
        earliest = min(
            task.start_date or datetime.now()
            for task in self.project.tasks
            if task.start_date
        )
        
        return earliest
    
    def _analyze_schedule(self) -> Dict:
        """
        Analyze schedule for risks and recommendations
        
        Returns:
            Dictionary with risk_score, feasibility_score, warnings, recommendations
        """
        warnings = []
        recommendations = []
        risk_score = 0.0
        
        # Check for tasks with very short duration
        short_tasks = [
            task for task in self.project.tasks
            if task.estimated_duration_hours < 4
        ]
        if short_tasks:
            warnings.append(
                f"{len(short_tasks)} tasks have very short durations (<4 hours). "
                "Consider combining or validating estimates."
            )
            risk_score += 0.1
        
        # Check for overloaded team members
        # TODO: Implement when resource allocation is added
        
        # Check for tasks on critical path
        critical_count = sum(1 for task in self.project.tasks if task.is_critical)
        critical_pct = critical_count / len(self.project.tasks) if self.project.tasks else 0
        
        if critical_pct > 0.5:
            warnings.append(
                f"{critical_pct:.0%} of tasks are on critical path. "
                "High risk of delays affecting target date."
            )
            risk_score += 0.3
            recommendations.append(
                "Add buffer time to critical path tasks or parallelize work where possible."
            )
        
        # Calculate feasibility score (inverse of risk)
        feasibility_score = max(0.0, 1.0 - risk_score)
        
        return {
            "risk_score": risk_score,
            "feasibility_score": feasibility_score,
            "warnings": warnings,
            "recommendations": recommendations
        }
    
    def add_task(self, task: Task):
        """Add a task to the project"""
        self.project.tasks.append(task)
    
    def add_milestone(self, milestone: Milestone):
        """Add a milestone to the project"""
        self.project.milestones.append(milestone)
    
    def add_dependency(self, from_task_id: str, to_task_id: str,
                      dependency_type: DependencyType = DependencyType.FINISH_TO_START,
                      lag_days: int = 0):
        """Add a dependency between tasks"""
        dep = Dependency(
            from_id=from_task_id,
            to_id=to_task_id,
            dependency_type=dependency_type,
            lag_days=lag_days
        )
        self.project.dependencies.append(dep)
