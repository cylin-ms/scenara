"""
Example: Product Launch Workback Plan
Demonstrates basic usage of WorkbackPlan
"""

from datetime import datetime, timedelta
import sys
sys.path.insert(0, '../src')

from models import (
    Project, Task, Milestone, TeamMember,
    Priority, TaskStatus, DependencyType
)
from planner import WorkbackPlanner


def create_product_launch_project():
    """Create a sample product launch project"""
    
    # Create project
    project = Project(
        id="prod-launch-001",
        name="Q1 Product Launch",
        target_date=datetime(2025, 12, 31),
        description="Launch new feature set for Q1 2026",
        owner="Product Manager"
    )
    
    # Add team members
    project.team_members = [
        TeamMember(
            id="pm-001",
            name="Alex Product",
            email="alex@company.com",
            role="Product Manager"
        ),
        TeamMember(
            id="eng-001",
            name="Sam Engineer",
            email="sam@company.com",
            role="Engineering Lead"
        ),
        TeamMember(
            id="mkt-001",
            name="Jamie Marketing",
            email="jamie@company.com",
            role="Marketing Manager"
        )
    ]
    
    # Add milestones
    beta_release = Milestone(
        id="m1",
        name="Beta Release",
        target_date=datetime(2025, 12, 1),
        description="Beta version released to pilot users",
        deliverables=["Beta build", "Test plan", "User docs"],
        owner="eng-001"
    )
    
    marketing_launch = Milestone(
        id="m2",
        name="Marketing Campaign Launch",
        target_date=datetime(2025, 12, 15),
        description="Marketing campaign goes live",
        deliverables=["Landing page", "Email campaign", "Social media"],
        owner="mkt-001"
    )
    
    general_availability = Milestone(
        id="m3",
        name="General Availability",
        target_date=datetime(2025, 12, 31),
        description="Product available to all users",
        deliverables=["Production build", "Support docs", "Training materials"],
        owner="pm-001"
    )
    
    project.milestones = [beta_release, marketing_launch, general_availability]
    
    # Add tasks for Beta Release milestone
    project.tasks.extend([
        Task(
            id="t1",
            name="Feature Development",
            description="Implement core features",
            estimated_duration_hours=160,  # 4 weeks
            owner="eng-001",
            milestone_id="m1",
            priority=Priority.CRITICAL,
            dependencies=[]
        ),
        Task(
            id="t2",
            name="Code Review & Testing",
            description="Review code and run tests",
            estimated_duration_hours=40,  # 1 week
            owner="eng-001",
            milestone_id="m1",
            priority=Priority.HIGH,
            dependencies=["t1"]
        ),
        Task(
            id="t3",
            name="Beta Documentation",
            description="Write user documentation",
            estimated_duration_hours=20,  # 0.5 weeks
            owner="pm-001",
            milestone_id="m1",
            priority=Priority.MEDIUM,
            dependencies=["t1"]
        )
    ])
    
    # Add tasks for Marketing Campaign milestone
    project.tasks.extend([
        Task(
            id="t4",
            name="Marketing Strategy",
            description="Define marketing approach",
            estimated_duration_hours=40,  # 1 week
            owner="mkt-001",
            milestone_id="m2",
            priority=Priority.HIGH,
            dependencies=[]
        ),
        Task(
            id="t5",
            name="Create Marketing Materials",
            description="Design landing page, emails, social content",
            estimated_duration_hours=80,  # 2 weeks
            owner="mkt-001",
            milestone_id="m2",
            priority=Priority.HIGH,
            dependencies=["t4"]
        ),
        Task(
            id="t6",
            name="Beta Feedback Analysis",
            description="Analyze beta user feedback",
            estimated_duration_hours=20,  # 0.5 weeks
            owner="pm-001",
            milestone_id="m2",
            priority=Priority.MEDIUM,
            dependencies=["t2"]  # Depends on beta testing
        )
    ])
    
    # Add tasks for General Availability milestone
    project.tasks.extend([
        Task(
            id="t7",
            name="Production Deployment",
            description="Deploy to production environment",
            estimated_duration_hours=20,  # 0.5 weeks
            owner="eng-001",
            milestone_id="m3",
            priority=Priority.CRITICAL,
            dependencies=["t2", "t6"]  # After testing and feedback
        ),
        Task(
            id="t8",
            name="Launch Marketing Campaign",
            description="Execute marketing campaign",
            estimated_duration_hours=40,  # 1 week
            owner="mkt-001",
            milestone_id="m3",
            priority=Priority.HIGH,
            dependencies=["t5"]
        ),
        Task(
            id="t9",
            name="Support Team Training",
            description="Train support team on new features",
            estimated_duration_hours=16,  # 2 days
            owner="pm-001",
            milestone_id="m3",
            priority=Priority.MEDIUM,
            dependencies=["t3"]  # After documentation
        )
    ])
    
    return project


def main():
    """Run the example"""
    print("=" * 70)
    print("WorkbackPlan Example: Product Launch")
    print("=" * 70)
    print()
    
    # Create project
    print("Creating project...")
    project = create_product_launch_project()
    print(f"✓ Project: {project.name}")
    print(f"  Target Date: {project.target_date.strftime('%Y-%m-%d')}")
    print(f"  Milestones: {len(project.milestones)}")
    print(f"  Tasks: {len(project.tasks)}")
    print(f"  Team Members: {len(project.team_members)}")
    print()
    
    # Create planner
    print("Initializing workback planner...")
    planner = WorkbackPlanner(project)
    
    # Generate schedule
    print("Generating workback schedule...")
    schedule = planner.generate()
    
    print("✓ Schedule generated!")
    print()
    
    # Display results
    print("=" * 70)
    print("SCHEDULE RESULTS")
    print("=" * 70)
    print()
    
    print(f"Project Start Date: {schedule.project.start_date.strftime('%Y-%m-%d')}")
    print(f"Project End Date: {schedule.project.target_date.strftime('%Y-%m-%d')}")
    print(f"Total Duration: {schedule.total_duration_days} days")
    print()
    
    print(f"Risk Score: {schedule.risk_score:.2f}")
    print(f"Feasibility Score: {schedule.feasibility_score:.2f}")
    print()
    
    # Show critical path
    print("Critical Path Tasks:")
    critical_tasks = schedule.project.get_critical_path()
    for task in critical_tasks:
        print(f"  • {task.name} ({task.estimated_duration_hours}h) - {task.owner}")
    print()
    
    # Show warnings
    if schedule.warnings:
        print("⚠️  Warnings:")
        for warning in schedule.warnings:
            print(f"  • {warning}")
        print()
    
    # Show recommendations
    if schedule.recommendations:
        print("💡 Recommendations:")
        for rec in schedule.recommendations:
            print(f"  • {rec}")
        print()
    
    # Show task schedule
    print("=" * 70)
    print("TASK SCHEDULE")
    print("=" * 70)
    print()
    
    for milestone in schedule.project.milestones:
        print(f"📍 {milestone.name} (Target: {milestone.target_date.strftime('%Y-%m-%d')})")
        milestone_tasks = [t for t in schedule.project.tasks if t.milestone_id == milestone.id]
        
        for task in sorted(milestone_tasks, key=lambda t: t.start_date or datetime.now()):
            critical_marker = "🔴" if task.is_critical else "  "
            start = task.start_date.strftime('%Y-%m-%d') if task.start_date else "TBD"
            end = task.end_date.strftime('%Y-%m-%d') if task.end_date else "TBD"
            print(f"  {critical_marker} {task.name}")
            print(f"     {start} → {end} ({task.estimated_duration_hours}h)")
            print(f"     Owner: {task.owner}, Priority: {task.priority.value}")
            if task.dependencies:
                deps = [schedule.project.get_task(dep_id).name for dep_id in task.dependencies]
                print(f"     Depends on: {', '.join(deps)}")
        print()
    
    print("=" * 70)
    print("✓ Workback plan complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
