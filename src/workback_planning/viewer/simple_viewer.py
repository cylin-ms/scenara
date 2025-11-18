"""
Simple HTML Workback Plan Viewer

Generates a static HTML page to view workback plans locally.
No dependencies on Streamlit or other web frameworks.

Usage:
    python src/workback_planning/viewer/simple_viewer.py
    # Opens generated HTML file in your default browser
"""

import json
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Constants
DATA_DIR = Path("data/workback_scenarios")
OUTPUT_FILE = Path("workback_plans_viewer.html")

MEETING_TYPES = {
    "1_weekly_newsletter": {"name": "Weekly Newsletter", "horizon": "T-7", "complexity": "Low"},
    "2_sprint_planning": {"name": "Sprint Planning", "horizon": "T-14", "complexity": "Low-Medium"},
    "3_monthly_review": {"name": "Monthly Business Review", "horizon": "T-30", "complexity": "Medium"},
    "4_feature_launch": {"name": "Feature Launch", "horizon": "T-30", "complexity": "Medium"},
    "5_squad_mission": {"name": "Squad Mission Planning", "horizon": "T-42 to T-56", "complexity": "Medium-High"},
    "6_quarterly_review": {"name": "Quarterly Business Review", "horizon": "T-60", "complexity": "High"},
    "7_annual_kickoff": {"name": "Annual Kickoff", "horizon": "T-60", "complexity": "High"},
    "8_product_launch": {"name": "Major Product Launch", "horizon": "T-90", "complexity": "Very High"},
    "9_strategic_offsite": {"name": "Strategic Offsite", "horizon": "T-90", "complexity": "Very High"},
    "10_board_meeting": {"name": "Board Meeting", "horizon": "T-90", "complexity": "Very High"},
    "11_ma_integration": {"name": "M&A Integration", "horizon": "T-90+", "complexity": "Extreme"}
}

QUALITY_LEVELS = {
    "low": {"label": "Low Quality (50-65%)", "color": "#ff6b6b"},
    "medium": {"label": "Medium Quality (70-80%)", "color": "#ffd93d"},
    "high": {"label": "High Quality (85-95%)", "color": "#6bcf7f"}
}


def load_master_index() -> Optional[Dict]:
    """Load the master index"""
    index_path = DATA_DIR / "master_index.json"
    if index_path.exists():
        with open(index_path) as f:
            return json.load(f)
    return None


def load_scenario(meeting_type_key: str, scenario_num: int) -> Optional[Dict]:
    """Load a specific scenario"""
    scenario_path = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}.json"
    if scenario_path.exists():
        with open(scenario_path) as f:
            return json.load(f)
    return None


def load_plan(meeting_type_key: str, scenario_num: int, quality: str) -> Optional[Dict]:
    """Load a specific workback plan"""
    plan_path = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}_{quality}.json"
    if plan_path.exists():
        with open(plan_path) as f:
            return json.load(f)
    return None


def generate_html() -> str:
    """Generate HTML for the viewer"""
    
    master_index = load_master_index()
    if not master_index:
        return "<html><body><h1>No scenarios found</h1><p>Run generate_test_scenarios.py first.</p></body></html>"
    
    summary = master_index.get('summary_by_type', {})
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workback Plan Viewer</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2em;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            background: #ecf0f1;
            padding: 15px 20px;
            border-radius: 8px;
            flex: 1;
            min-width: 150px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .scenario-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        
        .scenario-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .scenario-title {{
            font-size: 1.4em;
            color: #2c3e50;
            font-weight: bold;
        }}
        
        .scenario-meta {{
            display: flex;
            gap: 15px;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-horizon {{
            background: #3498db;
            color: white;
        }}
        
        .badge-complexity {{
            background: #e74c3c;
            color: white;
        }}
        
        .info-section {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
        }}
        
        .info-label {{
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
        }}
        
        .info-content {{
            color: #555;
            line-height: 1.6;
        }}
        
        ul {{
            margin-left: 20px;
            margin-top: 8px;
        }}
        
        li {{
            margin-bottom: 5px;
        }}
        
        .plans-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }}
        
        @media (max-width: 1400px) {{
            .plans-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 900px) {{
            .plans-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .plan-card {{
            border: 2px solid;
            border-radius: 8px;
            padding: 20px;
            background: white;
        }}
        
        .plan-card.low {{
            border-color: #ff6b6b;
        }}
        
        .plan-card.medium {{
            border-color: #ffd93d;
        }}
        
        .plan-card.high {{
            border-color: #6bcf7f;
        }}
        
        .plan-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .plan-title {{
            font-size: 1.2em;
            font-weight: bold;
        }}
        
        .quality-badge {{
            padding: 6px 12px;
            border-radius: 4px;
            color: white;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .quality-badge.low {{
            background: #ff6b6b;
        }}
        
        .quality-badge.medium {{
            background: #e6b800;
        }}
        
        .quality-badge.high {{
            background: #51a862;
        }}
        
        .plan-metrics {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .metric {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            text-align: center;
        }}
        
        .metric-label {{
            font-size: 0.8em;
            color: #7f8c8d;
        }}
        
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .task-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        
        .task-table th {{
            background: #34495e;
            color: white;
            padding: 8px;
            text-align: left;
            font-weight: 600;
        }}
        
        .task-table td {{
            padding: 8px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .task-table tr:hover {{
            background: #f8f9fa;
        }}
        
        details {{
            margin-top: 15px;
            cursor: pointer;
        }}
        
        summary {{
            font-weight: 600;
            padding: 10px;
            background: #ecf0f1;
            border-radius: 4px;
            user-select: none;
        }}
        
        summary:hover {{
            background: #d5dbdb;
        }}
        
        .not-available {{
            color: #95a5a6;
            font-style: italic;
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        
        .timestamp {{
            color: #95a5a6;
            font-size: 0.9em;
            margin-top: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Workback Plan Viewer</h1>
        <p class="subtitle">Generated Test Scenarios and Workback Plans</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Scenarios</div>
                <div class="stat-value">{master_index.get('total_scenarios', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Plans</div>
                <div class="stat-value">{master_index.get('total_plans', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Meeting Types</div>
                <div class="stat-value">{len(summary)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Model</div>
                <div class="stat-value" style="font-size: 1.2em;">{master_index.get('model', 'N/A')}</div>
            </div>
        </div>
"""
    
    # Generate content for each meeting type
    for meeting_type_key, type_info in summary.items():
        meeting_name = type_info.get('name', meeting_type_key)
        horizon = type_info.get('horizon', 'N/A')
        complexity = type_info.get('complexity', 'N/A')
        scenario_count = type_info.get('scenarios', 0)
        
        html += f"""
        <h2>📅 {meeting_name}</h2>
        <div class="scenario-meta">
            <span class="badge badge-horizon">{horizon}</span>
            <span class="badge badge-complexity">{complexity}</span>
            <span>{scenario_count} scenario(s)</span>
        </div>
"""
        
        # Load each scenario
        for scenario_num in range(1, scenario_count + 1):
            scenario = load_scenario(meeting_type_key, scenario_num)
            if not scenario:
                continue
            
            html += f"""
        <div class="scenario-card">
            <div class="scenario-header">
                <div class="scenario-title">{scenario.get('scenario_name', 'Unnamed Scenario')}</div>
            </div>
            
            <div class="info-section">
                <div class="info-label">🏢 Company Context</div>
                <div class="info-content">{scenario.get('company_context', 'N/A')}</div>
            </div>
            
            <div class="info-section">
                <div class="info-label">📅 Meeting Details</div>
                <div class="info-content">{scenario.get('meeting_event_details', 'N/A')}</div>
            </div>
            
            <details>
                <summary>👥 Stakeholders ({len(scenario.get('stakeholders', []))})</summary>
                <ul>
"""
            for stakeholder in scenario.get('stakeholders', []):
                html += f"                    <li>{stakeholder}</li>\n"
            
            html += f"""
                </ul>
            </details>
            
            <details>
                <summary>📦 Deliverables ({len(scenario.get('deliverables', []))})</summary>
                <ul>
"""
            
            for deliverable in scenario.get('deliverables', []):
                html += f"                    <li>{deliverable}</li>\n"
            
            html += f"""
                </ul>
            </details>
            
            <details>
                <summary>🎯 Success Criteria ({len(scenario.get('success_criteria', []))})</summary>
                <ul>
"""
            
            for criterion in scenario.get('success_criteria', []):
                html += f"                    <li>{criterion}</li>\n"
            
            html += f"""
                </ul>
            </details>
            
            <details>
                <summary>⚠️ Constraints ({len(scenario.get('constraints', []))})</summary>
                <ul>
"""
            
            for constraint in scenario.get('constraints', []):
                html += f"                    <li>{constraint}</li>\n"
            
            html += """
                </ul>
            </details>
            
            <h3>📊 Workback Plans</h3>
            <div class="plans-grid">
"""
            
            # Load all three quality levels
            for quality in ['low', 'medium', 'high']:
                plan = load_plan(meeting_type_key, scenario_num, quality)
                quality_info = QUALITY_LEVELS[quality]
                
                if plan:
                    plan_data = plan.get('plan', {})
                    tasks = plan_data.get('tasks', [])
                    milestones = plan_data.get('milestones', [])
                    deliverables = plan_data.get('deliverables', [])
                    participants = plan_data.get('participants', [])
                    
                    html += f"""
                <div class="plan-card {quality}">
                    <div class="plan-header">
                        <div class="plan-title">{quality.capitalize()} Quality</div>
                        <div class="quality-badge {quality}">{quality_info['label']}</div>
                    </div>
                    
                    <div class="plan-metrics">
                        <div class="metric">
                            <div class="metric-label">Tasks</div>
                            <div class="metric-value">{len(tasks)}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Milestones</div>
                            <div class="metric-value">{len(milestones)}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Deliverables</div>
                            <div class="metric-value">{len(deliverables)}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Participants</div>
                            <div class="metric-value">{len(participants)}</div>
                        </div>
                    </div>
"""
                    
                    if plan_data.get('overview'):
                        html += f"""
                    <details>
                        <summary>📝 Overview</summary>
                        <div style="padding: 10px; margin-top: 10px; background: #f8f9fa; border-radius: 4px;">
                            {plan_data['overview']}
                        </div>
                    </details>
"""
                    
                    if tasks:
                        html += f"""
                    <details>
                        <summary>📋 Tasks ({len(tasks)})</summary>
                        <table class="task-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Title</th>
                                    <th>Owner</th>
                                    <th>Due Date</th>
                                </tr>
                            </thead>
                            <tbody>
"""
                        for task in tasks[:10]:  # Show first 10 tasks
                            html += f"""
                                <tr>
                                    <td>{task.get('id', 'N/A')}</td>
                                    <td>{task.get('title', 'Untitled')}</td>
                                    <td>{task.get('owner', 'Unassigned')}</td>
                                    <td>{task.get('due_date', 'N/A')}</td>
                                </tr>
"""
                        
                        if len(tasks) > 10:
                            html += f"""
                                <tr>
                                    <td colspan="4" style="text-align: center; color: #7f8c8d; font-style: italic;">
                                        ... and {len(tasks) - 10} more tasks
                                    </td>
                                </tr>
"""
                        
                        html += """
                            </tbody>
                        </table>
                    </details>
"""
                    
                    html += """
                </div>
"""
                else:
                    html += f"""
                <div class="plan-card {quality}">
                    <div class="plan-header">
                        <div class="plan-title">{quality.capitalize()} Quality</div>
                        <div class="quality-badge {quality}">{quality_info['label']}</div>
                    </div>
                    <div class="not-available">
                        ⏳ Plan not yet generated or still processing...
                    </div>
                </div>
"""
            
            html += """
            </div>
        </div>
"""
    
    html += f"""
        <div class="timestamp">
            Generated: {master_index.get('generated_at', 'Unknown')} | 
            Last viewed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Generate HTML and open in browser"""
    print("📋 Generating workback plan viewer...")
    
    if not DATA_DIR.exists():
        print(f"❌ Data directory not found: {DATA_DIR}")
        print("   Run generate_test_scenarios.py first to create scenarios.")
        return
    
    html_content = generate_html()
    
    # Write HTML file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated: {OUTPUT_FILE.absolute()}")
    
    # Open in browser
    file_url = f"file://{OUTPUT_FILE.absolute()}"
    print(f"🌐 Opening in browser: {file_url}")
    webbrowser.open(file_url)


if __name__ == "__main__":
    main()
