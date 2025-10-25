#!/usr/bin/env python3
"""
Integration script for Scenara rules into Scenara project
Provides utilities for task management, lessons learned, and tool integration
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class ScenaraRulesIntegration:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.cursorrules_path = self.project_root / ".cursorrules"
        self.tools_dir = self.project_root / "tools"
        
    def update_lesson_learned(self, category: str, lesson: str):
        """
        Add a new lesson to the .cursorrules file
        
        Args:
            category: Category of lesson ("user", "project", "technical")
            lesson: The lesson text to add
        """
        try:
            # Read current content
            if self.cursorrules_path.exists():
                with open(self.cursorrules_path, 'r') as f:
                    content = f.read()
            else:
                content = ""
            
            # Find the appropriate section
            section_map = {
                "user": "### User Specified Lessons",
                "project": "### Project Specific Lessons", 
                "technical": "### Technical Lessons"
            }
            
            section_header = section_map.get(category, "### Technical Lessons")
            
            # Add the lesson
            if section_header in content:
                # Insert after the section header
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == section_header:
                        # Find the end of this section (next ### or end of file)
                        insert_pos = i + 1
                        while (insert_pos < len(lines) and 
                               not lines[insert_pos].strip().startswith('###')):
                            insert_pos += 1
                        
                        # Insert the new lesson
                        lines.insert(insert_pos, f"- {lesson}")
                        break
                
                content = '\n'.join(lines)
            else:
                # Add the section and lesson at the end
                content += f"\n\n{section_header}\n- {lesson}\n"
            
            # Write back
            with open(self.cursorrules_path, 'w') as f:
                f.write(content)
            
            print(f"Added lesson to {category} section: {lesson}")
            
        except Exception as e:
            print(f"Error updating lesson: {e}", file=sys.stderr)
    
    def update_task_progress(self, task_name: str, completed: bool = True):
        """
        Update task progress in the scratchpad
        
        Args:
            task_name: Name of the task to update
            completed: Whether the task is completed
        """
        try:
            if not self.cursorrules_path.exists():
                print("No .cursorrules file found", file=sys.stderr)
                return
            
            with open(self.cursorrules_path, 'r') as f:
                content = f.read()
            
            # Find and update the task
            marker = "[X]" if completed else "[ ]"
            old_markers = ["[ ]", "[X]"]
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Check if this line contains the task
                if any(old_marker in line for old_marker in old_markers):
                    if task_name.lower() in line.lower():
                        # Replace the marker
                        for old_marker in old_markers:
                            if old_marker in line:
                                lines[i] = line.replace(old_marker, marker)
                                break
                        break
            
            content = '\n'.join(lines)
            
            with open(self.cursorrules_path, 'w') as f:
                f.write(content)
            
            status = "completed" if completed else "pending"
            print(f"Updated task '{task_name}' to {status}")
            
        except Exception as e:
            print(f"Error updating task progress: {e}", file=sys.stderr)
    
    def add_new_task(self, task_name: str, description: str = "", priority: str = "medium"):
        """
        Add a new task to the scratchpad
        
        Args:
            task_name: Name of the task
            description: Optional task description
            priority: Task priority ("high", "medium", "low")
        """
        try:
            if not self.cursorrules_path.exists():
                print("No .cursorrules file found", file=sys.stderr)
                return
            
            with open(self.cursorrules_path, 'r') as f:
                content = f.read()
            
            # Find a good place to insert the task
            # Look for existing task lists
            lines = content.split('\n')
            insert_pos = -1
            
            for i, line in enumerate(lines):
                if line.strip().startswith('[ ]') or line.strip().startswith('[X]'):
                    insert_pos = i + 1
            
            if insert_pos == -1:
                # No existing tasks, add at the end
                insert_pos = len(lines)
            
            # Create task line
            task_line = f"[ ] {task_name}"
            if description:
                task_line += f" - {description}"
            
            # Insert the task
            lines.insert(insert_pos, task_line)
            
            content = '\n'.join(lines)
            
            with open(self.cursorrules_path, 'w') as f:
                f.write(content)
            
            print(f"Added new task: {task_name}")
            
        except Exception as e:
            print(f"Error adding task: {e}", file=sys.stderr)
    
    def get_current_tasks(self) -> List[Dict[str, Any]]:
        """
        Get list of current tasks from the scratchpad
        
        Returns:
            List of task dictionaries with name, completed status, and description
        """
        tasks = []
        
        try:
            if not self.cursorrules_path.exists():
                return tasks
            
            with open(self.cursorrules_path, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('[ ]') or line.startswith('[X]'):
                    completed = line.startswith('[X]')
                    task_text = line[3:].strip()  # Remove marker
                    
                    # Split name and description if " - " is present
                    if " - " in task_text:
                        name, description = task_text.split(" - ", 1)
                    else:
                        name = task_text
                        description = ""
                    
                    tasks.append({
                        "name": name,
                        "description": description,
                        "completed": completed
                    })
            
            return tasks
            
        except Exception as e:
            print(f"Error reading tasks: {e}", file=sys.stderr)
            return tasks
    
    def run_tool(self, tool_name: str, args: List[str] = None) -> str:
        """
        Run a tool from the tools directory
        
        Args:
            tool_name: Name of the tool (without .py extension)
            args: List of arguments to pass to the tool
            
        Returns:
            Tool output as string
        """
        try:
            tool_path = self.tools_dir / f"{tool_name}.py"
            
            if not tool_path.exists():
                return f"Error: Tool {tool_name} not found"
            
            # Construct command
            cmd_args = [sys.executable, str(tool_path)]
            if args:
                cmd_args.extend(args)
            
            # Run the tool
            import subprocess
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Tool error: {result.stderr}"
                
        except Exception as e:
            return f"Error running tool: {e}"
    
    def generate_status_report(self) -> str:
        """
        Generate a status report based on current tasks and lessons
        
        Returns:
            Formatted status report
        """
        report = []
        report.append("# Scenara Project Status Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Tasks summary
        tasks = self.get_current_tasks()
        completed_tasks = [t for t in tasks if t['completed']]
        pending_tasks = [t for t in tasks if not t['completed']]
        
        report.append(f"## Task Summary")
        report.append(f"- Total Tasks: {len(tasks)}")
        report.append(f"- Completed: {len(completed_tasks)}")
        report.append(f"- Pending: {len(pending_tasks)}")
        report.append("")
        
        # Pending tasks
        if pending_tasks:
            report.append("### Pending Tasks")
            for task in pending_tasks:
                report.append(f"- [ ] {task['name']}")
                if task['description']:
                    report.append(f"      {task['description']}")
            report.append("")
        
        # Recent completions
        if completed_tasks:
            report.append("### Recently Completed")
            for task in completed_tasks[-5:]:  # Last 5 completed
                report.append(f"- [X] {task['name']}")
            report.append("")
        
        # Tools availability
        report.append("### Available Tools")
        if self.tools_dir.exists():
            tools = [f.stem for f in self.tools_dir.glob("*.py")]
            for tool in sorted(tools):
                report.append(f"- {tool}")
        else:
            report.append("- No tools directory found")
        
        return "\n".join(report)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Scenara Rules Integration Utility")
    parser.add_argument("--add-lesson", nargs=2, metavar=("CATEGORY", "LESSON"),
                       help="Add a lesson (category: user|project|technical)")
    parser.add_argument("--update-task", nargs=2, metavar=("TASK", "STATUS"),
                       help="Update task status (status: completed|pending)")
    parser.add_argument("--add-task", nargs=2, metavar=("NAME", "DESCRIPTION"),
                       help="Add a new task")
    parser.add_argument("--list-tasks", action="store_true", help="List current tasks")
    parser.add_argument("--status-report", action="store_true", help="Generate status report")
    parser.add_argument("--run-tool", nargs="+", metavar="TOOL_NAME [ARGS...]",
                       help="Run a tool with arguments")
    
    args = parser.parse_args()
    
    integration = ScenaraRulesIntegration()
    
    if args.add_lesson:
        category, lesson = args.add_lesson
        integration.update_lesson_learned(category, lesson)
    
    elif args.update_task:
        task, status = args.update_task
        completed = status.lower() == "completed"
        integration.update_task_progress(task, completed)
    
    elif args.add_task:
        name, description = args.add_task
        integration.add_new_task(name, description)
    
    elif args.list_tasks:
        tasks = integration.get_current_tasks()
        print("Current Tasks:")
        for task in tasks:
            marker = "[X]" if task['completed'] else "[ ]"
            print(f"  {marker} {task['name']}")
            if task['description']:
                print(f"      {task['description']}")
    
    elif args.status_report:
        report = integration.generate_status_report()
        print(report)
    
    elif args.run_tool:
        tool_name = args.run_tool[0]
        tool_args = args.run_tool[1:] if len(args.run_tool) > 1 else []
        output = integration.run_tool(tool_name, tool_args)
        print(output)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()