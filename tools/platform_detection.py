#!/usr/bin/env python3
"""
Platform Detection Utility for Scenara 2.0
Detects which AI assistant/editor is being used and recommends appropriate tools
"""

import os
import sys
import platform
import json
from pathlib import Path
from typing import Dict, List, Optional

class PlatformDetector:
    """Detects the current development platform and recommends appropriate tools"""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.platform_info = {}
        self.recommendations = {}
        
    def detect_platform(self) -> Dict[str, any]:
        """Comprehensive platform detection"""
        # Detect components in order
        os_info = self._detect_os()
        python_info = self._detect_python_env()
        editor_info = self._detect_editor()
        project_info = self._detect_project_context()
        
        # Store intermediate results for AI assistant detection
        self.platform_info = {
            "operating_system": os_info,
            "python_environment": python_info,
            "editor_environment": editor_info,
            "project_context": project_info
        }
        
        # Now detect AI assistant with access to editor info
        ai_info = self._detect_ai_assistant()
        
        # Build final results
        detection_results = {
            "timestamp": self._get_timestamp(),
            "operating_system": os_info,
            "python_environment": python_info,
            "editor_environment": editor_info,
            "ai_assistant": ai_info,
            "project_context": project_info,
            "recommended_tools": self._get_platform_tools()
        }
        
        self.platform_info = detection_results
        return detection_results
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _detect_os(self) -> Dict[str, str]:
        """Detect operating system details"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    
    def _detect_python_env(self) -> Dict[str, any]:
        """Detect Python environment details"""
        venv_path = self.project_root / "venv"
        conda_env = os.environ.get("CONDA_DEFAULT_ENV")
        virtual_env = os.environ.get("VIRTUAL_ENV")
        
        return {
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "venv_exists": venv_path.exists(),
            "venv_path": str(venv_path) if venv_path.exists() else None,
            "conda_env": conda_env,
            "virtual_env": virtual_env,
            "active_env": self._get_active_env()
        }
    
    def _get_active_env(self) -> str:
        """Determine the active Python environment"""
        if "venv" in sys.executable:
            return "venv"
        elif os.environ.get("CONDA_DEFAULT_ENV"):
            return f"conda:{os.environ.get('CONDA_DEFAULT_ENV')}"
        elif os.environ.get("VIRTUAL_ENV"):
            return "virtualenv"
        else:
            return "system"
    
    def _detect_editor(self) -> Dict[str, any]:
        """Detect which editor/IDE is being used"""
        # Check for environment variables that indicate specific editors
        editor_indicators = {
            "cursor": [
                "CURSOR_USER_DATA_DIR",
                "CURSOR_LOGS_DIR"
            ],
            "vscode": [
                "VSCODE_PID",
                "VSCODE_CWD",
                "TERM_PROGRAM",
                "VSCODE_INJECTION"
            ],
            "pycharm": [
                "PYCHARM_HOSTED",
                "PYCHARM_DISPLAY_PORT"
            ],
            "jupyter": [
                "JPY_PARENT_PID",
                "JUPYTER_CONFIG_DIR"
            ]
        }
        
        detected_editors = []
        for editor, env_vars in editor_indicators.items():
            for var in env_vars:
                if os.environ.get(var):
                    detected_editors.append(editor)
                    break
        
        # Special detection for VS Code via TERM_PROGRAM
        if os.environ.get("TERM_PROGRAM") == "vscode":
            detected_editors.append("vscode")
        
        return {
            "detected_editors": list(set(detected_editors)),
            "term_program": os.environ.get("TERM_PROGRAM"),
            "term": os.environ.get("TERM"),
            "shell": os.environ.get("SHELL", "unknown")
        }
    
    def _detect_ai_assistant(self) -> Dict[str, any]:
        """Detect which AI assistant is likely being used"""
        cursorrules_exists = (self.project_root / ".cursorrules").exists()
        copilot_instructions_exists = (self.project_root / ".github" / "copilot-instructions.md").exists()
        
        # Get editor info from already detected platform info
        editors = self.platform_info.get("editor_environment", {}).get("detected_editors", []) if hasattr(self, 'platform_info') else []
        
        ai_assistants = []
        
        # Cursor AI detection
        if "cursor" in editors or cursorrules_exists:
            ai_assistants.append("cursor_ai")
        
        # GitHub Copilot detection
        if "vscode" in editors or copilot_instructions_exists:
            ai_assistants.append("github_copilot")
        
        return {
            "detected_assistants": ai_assistants,
            "cursorrules_exists": cursorrules_exists,
            "copilot_instructions_exists": copilot_instructions_exists,
            "primary_assistant": self._determine_primary_assistant(ai_assistants, editors)
        }
    
    def _determine_primary_assistant(self, assistants: List[str], editors: List[str]) -> str:
        """Determine the primary AI assistant based on context"""
        # If VS Code is detected, prefer GitHub Copilot
        if "vscode" in editors:
            return "github_copilot"
        # If Cursor is detected, prefer Cursor AI
        elif "cursor" in editors:
            return "cursor_ai"
        # If both configuration files exist but no clear editor, prefer based on availability
        elif "github_copilot" in assistants and "cursor_ai" in assistants:
            return "github_copilot"  # VS Code is more commonly detected
        elif assistants:
            return assistants[0]
        else:
            return "unknown"
    
    def _detect_project_context(self) -> Dict[str, any]:
        """Detect project-specific context"""
        cursorrules_path = self.project_root / ".cursorrules"
        cursorrules_content = None
        
        if cursorrules_path.exists():
            try:
                with open(cursorrules_path, 'r', encoding='utf-8') as f:
                    cursorrules_content = f.read()
            except Exception as e:
                cursorrules_content = f"Error reading .cursorrules: {e}"
        
        return {
            "project_name": self.project_root.name,
            "project_path": str(self.project_root),
            "cursorrules_exists": cursorrules_path.exists(),
            "cursorrules_size": cursorrules_path.stat().st_size if cursorrules_path.exists() else 0,
            "has_requirements_txt": (self.project_root / "requirements.txt").exists(),
            "has_meeting_prep_requirements": (self.project_root / "requirements_meeting_prep.txt").exists(),
            "has_venv": (self.project_root / "venv").exists(),
            "tools_directory": (self.project_root / "tools").exists()
        }
    
    def _get_platform_tools(self) -> Dict[str, List[str]]:
        """Get recommended tools for the detected platform"""
        if not hasattr(self, 'platform_info') or not self.platform_info:
            return {}
        
        ai_assistant = self.platform_info.get("ai_assistant", {}).get("primary_assistant", "unknown")
        os_system = self.platform_info.get("operating_system", {}).get("system", "unknown")
        
        tools = {
            "cursor_ai": [
                "Use .cursorrules as primary configuration",
                "Task management with [X] and [ ] markers",
                "Real-time lesson learning integration",
                "Scratchpad functionality for planning",
                "Automatic project context awareness"
            ],
            "github_copilot": [
                "Read .cursorrules file first (mandatory)",
                "Follow .github/copilot-instructions.md workflow",
                "Respect completed/pending task states",
                "Apply lessons learned automatically",
                "Use established coding patterns"
            ],
            "python_development": [
                "Use ./venv Python environment",
                "Install from requirements_meeting_prep.txt",
                "Configure Python environment before tool usage",
                "Use tools/llm_api.py for LLM integration",
                "Follow timezone handling best practices"
            ],
            "meeting_intelligence": [
                "tools/meeting_extractor.py - Comprehensive meeting data",
                "daily_meeting_viewer.py - Beautiful formatted output",
                "tools/web_scraper.py - Research capabilities",
                "Graph Explorer - Microsoft calendar access",
                "tools/screenshot_utils.py - UI verification"
            ],
            f"{os_system.lower()}_specific": self._get_os_specific_tools(os_system)
        }
        
        return tools
    
    def _get_os_specific_tools(self, os_system: str) -> List[str]:
        """Get OS-specific tool recommendations"""
        if os_system.lower() == "darwin":  # macOS
            return [
                "Use zsh shell (default)",
                "Microsoft Edge for Graph API authentication",
                "AppleScript for automation when needed",
                "Avoid Windows-specific tools (SilverFlow)"
            ]
        elif os_system.lower() == "windows":
            return [
                "PowerShell for script execution",
                "Windows Authentication Manager (WAM) support",
                "SilverFlow patterns available",
                "Edge WebDriver for automation"
            ]
        elif os_system.lower() == "linux":
            return [
                "Bash/zsh shell support",
                "X11/Wayland display protocols",
                "Package manager integration",
                "Container deployment options"
            ]
        else:
            return ["Standard cross-platform tools"]
    
    def generate_startup_recommendations(self) -> str:
        """Generate startup recommendations based on platform detection"""
        info = self.detect_platform()
        
        recommendations = []
        recommendations.append("🎯 SCENARA 2.0 PLATFORM DETECTION RESULTS")
        recommendations.append("=" * 50)
        
        # Operating System
        os_info = info["operating_system"]
        recommendations.append(f"🖥️  Operating System: {os_info['system']} {os_info['release']}")
        
        # Python Environment
        py_info = info["python_environment"]
        recommendations.append(f"🐍 Python: {py_info['python_version']} ({py_info['active_env']})")
        
        # Editor Detection
        editor_info = info["editor_environment"]
        if editor_info["detected_editors"]:
            recommendations.append(f"✏️  Editor: {', '.join(editor_info['detected_editors'])}")
        
        # AI Assistant Detection
        ai_info = info["ai_assistant"]
        recommendations.append(f"🤖 AI Assistant: {ai_info['primary_assistant']}")
        
        # Configuration Status
        recommendations.append("\n📋 CONFIGURATION STATUS:")
        if ai_info["cursorrules_exists"]:
            recommendations.append("✅ .cursorrules found - Cursor AI configured")
        if ai_info["copilot_instructions_exists"]:
            recommendations.append("✅ .github/copilot-instructions.md found - GitHub Copilot configured")
        
        # Environment Setup
        recommendations.append("\n🛠️  ENVIRONMENT SETUP:")
        if py_info["venv_exists"]:
            recommendations.append("✅ ./venv directory found")
            recommendations.append("   → Activate: source ./venv/bin/activate")
        else:
            recommendations.append("⚠️  ./venv not found - create Python virtual environment")
        
        # Platform-Specific Recommendations
        primary_assistant = ai_info["primary_assistant"]
        recommendations.append(f"\n🎯 RECOMMENDATIONS FOR {primary_assistant.upper()}:")
        
        platform_tools = info["recommended_tools"]
        if primary_assistant in platform_tools:
            for tool in platform_tools[primary_assistant]:
                recommendations.append(f"   • {tool}")
        
        # Tool Availability
        recommendations.append("\n🔧 AVAILABLE TOOLS:")
        if "meeting_intelligence" in platform_tools:
            for tool in platform_tools["meeting_intelligence"]:
                recommendations.append(f"   • {tool}")
        
        # OS-Specific Tools
        os_system = info["operating_system"]["system"].lower()
        os_key = f"{os_system}_specific"
        if os_key in platform_tools:
            recommendations.append(f"\n🖥️  {os_system.upper()}-SPECIFIC TOOLS:")
            for tool in platform_tools[os_key]:
                recommendations.append(f"   • {tool}")
        
        return "\n".join(recommendations)
    
    def save_detection_results(self, output_path: Optional[str] = None) -> str:
        """Save detection results to JSON file"""
        if not output_path:
            output_path = self.project_root / "platform_detection_results.json"
        
        info = self.detect_platform()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        
        return str(output_path)

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect platform and recommend tools for Scenara 2.0")
    parser.add_argument("--project-root", help="Project root directory", default=".")
    parser.add_argument("--output", help="Output file for detection results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    detector = PlatformDetector(args.project_root)
    
    if args.json:
        info = detector.detect_platform()
        print(json.dumps(info, indent=2))
    elif args.quiet:
        info = detector.detect_platform()
        ai_assistant = info["ai_assistant"]["primary_assistant"]
        print(f"Platform: {ai_assistant}")
    else:
        recommendations = detector.generate_startup_recommendations()
        print(recommendations)
    
    if args.output:
        output_path = detector.save_detection_results(args.output)
        if not args.quiet:
            print(f"\nDetection results saved to: {output_path}")

if __name__ == "__main__":
    main()