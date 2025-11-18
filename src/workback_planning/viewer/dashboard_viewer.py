"""
Interactive Dashboard Viewer for Workback Plans

Creates a self-contained HTML dashboard with:
- Executive summary with key metrics
- Company-based navigation and grouping
- Table of contents for easy exploration
- Responsive design for sharing

Usage:
    python src/workback_planning/viewer/dashboard_viewer.py
"""

import json
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

# Constants
DATA_DIR = Path("data/workback_scenarios")
OUTPUT_FILE = Path("workback_dashboard.html")

MEETING_TYPES = {
    "1_weekly_newsletter": {"name": "Weekly Newsletter", "icon": "📰", "horizon": "T-7"},
    "2_sprint_planning": {"name": "Sprint Planning", "icon": "🏃", "horizon": "T-14"},
    "3_monthly_review": {"name": "Monthly Business Review", "icon": "📊", "horizon": "T-30"},
    "4_feature_launch": {"name": "Feature Launch", "icon": "🚀", "horizon": "T-30"},
    "5_squad_mission": {"name": "Squad Mission Planning", "icon": "👥", "horizon": "T-42 to T-56"},
    "6_quarterly_review": {"name": "Quarterly Business Review", "icon": "📈", "horizon": "T-60"},
    "7_annual_kickoff": {"name": "Annual Kickoff", "icon": "🎯", "horizon": "T-60"},
    "8_product_launch": {"name": "Major Product Launch", "icon": "🎉", "horizon": "T-90"},
    "9_strategic_offsite": {"name": "Strategic Offsite", "icon": "🏔️", "horizon": "T-90"},
    "10_board_meeting": {"name": "Board Meeting", "icon": "👔", "horizon": "T-90"},
    "11_ma_integration": {"name": "M&A Integration", "icon": "🤝", "horizon": "T-90+"}
}


def load_all_data():
    """Load all scenarios and plans, organized by company"""
    master_index_path = DATA_DIR / "master_index.json"
    if not master_index_path.exists():
        return None
    
    with open(master_index_path) as f:
        master_index = json.load(f)
    
    # Organize scenarios by company
    companies = defaultdict(lambda: {
        'scenarios': [],
        'total_plans': 0,
        'meeting_types': set(),
        'total_stakeholders': 0,
        'total_deliverables': 0
    })
    
    for scenario in master_index.get('scenarios', []):
        # Extract company name from scenario
        company_name = extract_company_name(scenario.get('company_context', ''))
        scenario_name = scenario.get('scenario_name', 'Unnamed')
        
        # Load plans for this scenario
        meeting_type_key = scenario.get('meeting_type_key')
        scenario_num = scenario.get('scenario_number')
        
        plans = {
            'low': load_plan(meeting_type_key, scenario_num, 'low'),
            'medium': load_plan(meeting_type_key, scenario_num, 'medium'),
            'high': load_plan(meeting_type_key, scenario_num, 'high')
        }
        
        scenario['plans'] = plans
        scenario['company'] = company_name
        
        # Update company stats
        companies[company_name]['scenarios'].append(scenario)
        companies[company_name]['total_plans'] += sum(1 for p in plans.values() if p)
        companies[company_name]['meeting_types'].add(scenario.get('meeting_type'))
        companies[company_name]['total_stakeholders'] += len(scenario.get('stakeholders', []))
        companies[company_name]['total_deliverables'] += len(scenario.get('deliverables', []))
    
    # Convert sets to lists for JSON serialization
    for company_data in companies.values():
        company_data['meeting_types'] = list(company_data['meeting_types'])
    
    return {
        'master_index': master_index,
        'companies': dict(companies)
    }


def extract_company_name(company_context: str) -> str:
    """Extract company name from context string"""
    if not company_context:
        return "Unknown Company"
    
    # Look for patterns like "CompanyName is a..." or "CompanyName, Inc." etc.
    parts = company_context.split()
    if len(parts) > 0:
        # Take first 1-3 words as company name
        name_parts = []
        for part in parts[:5]:
            if part in ['is', 'was', '–', '-', '(', 'a', 'an', 'the']:
                break
            name_parts.append(part.strip('.,;:()[]{}'))
        
        if name_parts:
            return ' '.join(name_parts[:3])  # Max 3 words
    
    return "Unknown Company"


def load_plan(meeting_type_key: str, scenario_num: int, quality: str) -> Optional[Dict]:
    """Load a specific workback plan"""
    plan_path = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}_{quality}.json"
    if plan_path.exists():
        with open(plan_path) as f:
            return json.load(f)
    return None


def generate_dashboard_html(data: Dict) -> str:
    """Generate interactive dashboard HTML"""
    
    master_index = data['master_index']
    companies = data['companies']
    
    # Calculate aggregate statistics
    total_companies = len(companies)
    total_scenarios = master_index.get('total_scenarios', 0)
    total_plans = master_index.get('total_plans', 0)
    total_meeting_types = master_index.get('meeting_types', 0)
    
    # Calculate totals across all companies
    total_stakeholders = sum(c['total_stakeholders'] for c in companies.values())
    total_deliverables = sum(c['total_deliverables'] for c in companies.values())
    total_tasks = 0
    
    for company_data in companies.values():
        for scenario in company_data['scenarios']:
            for plan in scenario.get('plans', {}).values():
                if plan:
                    total_tasks += len(plan.get('plan', {}).get('tasks', []))
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workback Planning Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        :root {{
            --primary: #2c3e50;
            --secondary: #3498db;
            --success: #27ae60;
            --warning: #f39c12;
            --danger: #e74c3c;
            --light: #ecf0f1;
            --dark: #34495e;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }}
        
        /* Header */
        header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--dark) 100%);
            color: white;
            padding: 2rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        /* Navigation */
        nav {{
            background: white;
            border-bottom: 2px solid #dee2e6;
            position: sticky;
            top: 108px;
            z-index: 999;
        }}
        
        .nav-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .nav-link {{
            padding: 0.5rem 1rem;
            background: var(--light);
            border-radius: 4px;
            text-decoration: none;
            color: var(--primary);
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .nav-link:hover {{
            background: var(--secondary);
            color: white;
        }}
        
        /* Sidebar Navigation */
        .sidebar {{
            position: fixed;
            left: 0;
            top: 160px;
            width: 280px;
            height: calc(100vh - 160px);
            background: white;
            border-right: 2px solid #dee2e6;
            overflow-y: auto;
            padding: 1.5rem;
            z-index: 900;
        }}
        
        .sidebar h3 {{
            color: var(--primary);
            font-size: 1.1rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--secondary);
        }}
        
        .sidebar-nav {{
            list-style: none;
        }}
        
        .sidebar-nav li {{
            margin-bottom: 0.5rem;
        }}
        
        .sidebar-link {{
            display: block;
            padding: 0.6rem 0.8rem;
            color: var(--dark);
            text-decoration: none;
            border-radius: 4px;
            transition: all 0.3s;
            font-size: 0.95rem;
        }}
        
        .sidebar-link:hover {{
            background: var(--light);
            color: var(--secondary);
            transform: translateX(5px);
        }}
        
        .sidebar-link.active {{
            background: var(--secondary);
            color: white;
        }}
        
        .sidebar-section {{
            margin-bottom: 1.5rem;
        }}
        
        .sidebar-section-title {{
            font-weight: 600;
            color: var(--secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            margin-top: 1rem;
        }}
        
        /* Main Content */
        .container {{
            max-width: 1400px;
            margin: 2rem auto;
            margin-left: 300px;
            padding: 0 2rem;
        }}
        
        /* Mobile Responsive */
        @media (max-width: 1024px) {{
            .sidebar {{
                transform: translateX(-100%);
                transition: transform 0.3s;
            }}
            
            .sidebar.open {{
                transform: translateX(0);
            }}
            
            .container {{
                margin-left: 2rem;
            }}
        }}
        
        /* Dashboard Section */
        .dashboard {{
            background: white;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            scroll-margin-top: 160px;
        }}
        
        .dashboard h2 {{
            color: var(--primary);
            margin-bottom: 1.5rem;
            font-size: 2rem;
            border-bottom: 3px solid var(--secondary);
            padding-bottom: 0.5rem;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, var(--secondary) 0%, #5dade2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            cursor: pointer;
            text-decoration: none;
            display: block;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
        }}
        
        /* Company Cards */
        .company-card {{
            background: white;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-left: 5px solid var(--secondary);
            scroll-margin-top: 140px;
        }}
        
        .company-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .company-name {{
            font-size: 1.8rem;
            color: var(--primary);
            font-weight: bold;
        }}
        
        .company-stats {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }}
        
        .stat-badge {{
            background: var(--light);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            color: var(--dark);
        }}
        
        .stat-badge strong {{
            color: var(--secondary);
        }}
        
        /* Scenario Cards */
        .scenario-grid {{
            display: grid;
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .scenario-item {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1.5rem;
        }}
        
        .scenario-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
            gap: 1rem;
        }}
        
        .scenario-title {{
            font-size: 1.3rem;
            color: var(--primary);
            font-weight: 600;
            flex: 1;
        }}
        
        .meeting-badge {{
            background: var(--secondary);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            font-size: 0.85rem;
            white-space: nowrap;
        }}
        
        .scenario-info {{
            background: white;
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
        }}
        
        .info-row {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }}
        
        .info-label {{
            font-weight: 600;
            color: var(--dark);
        }}
        
        /* Plans Grid */
        .plans-container {{
            margin-top: 1rem;
        }}
        
        .plans-header {{
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 0.8rem;
            font-size: 1.1rem;
        }}
        
        .plans-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }}
        
        @media (max-width: 1200px) {{
            .plans-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .plans-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .plan-card {{
            background: white;
            border: 2px solid;
            border-radius: 6px;
            padding: 1rem;
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
            margin-bottom: 0.8rem;
        }}
        
        .plan-title {{
            font-weight: 600;
            font-size: 1.05rem;
        }}
        
        .quality-badge {{
            padding: 0.3rem 0.6rem;
            border-radius: 4px;
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
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
            gap: 0.5rem;
        }}
        
        .mini-metric {{
            background: #f8f9fa;
            padding: 0.5rem;
            border-radius: 4px;
            text-align: center;
        }}
        
        .mini-metric-label {{
            font-size: 0.75rem;
            color: #6c757d;
        }}
        
        .mini-metric-value {{
            font-size: 1.3rem;
            font-weight: bold;
            color: var(--primary);
        }}
        
        .not-available {{
            color: #95a5a6;
            font-style: italic;
            text-align: center;
            padding: 2rem;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        
        /* Table of Contents */
        .toc {{
            background: white;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            scroll-margin-top: 160px;
        }}
        
        .toc h3 {{
            color: var(--primary);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        
        .toc-list {{
            list-style: none;
        }}
        
        .toc-item {{
            margin-bottom: 0.8rem;
        }}
        
        .toc-link {{
            color: var(--secondary);
            text-decoration: none;
            font-size: 1.05rem;
            transition: all 0.3s;
            display: inline-block;
        }}
        
        .toc-link:hover {{
            color: var(--dark);
            transform: translateX(5px);
        }}
        
        .toc-count {{
            color: #6c757d;
            font-size: 0.9rem;
            margin-left: 0.5rem;
        }}
        
        /* Footer */
        footer {{
            background: var(--dark);
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--secondary);
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }}
        
        .back-to-top:hover {{
            background: var(--primary);
            transform: translateY(-5px);
        }}
        
        .back-to-nav {{
            display: inline-block;
            margin-top: 1.5rem;
            padding: 0.75rem 1.5rem;
            background: var(--secondary);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .back-to-nav:hover {{
            background: var(--primary);
            transform: translateX(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        .back-to-nav::before {{
            content: "← ";
            margin-right: 0.5rem;
        }}
        
        details {{
            margin-top: 0.8rem;
        }}
        
        summary {{
            cursor: pointer;
            font-weight: 600;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 4px;
            user-select: none;
        }}
        
        summary:hover {{
            background: #e9ecef;
        }}
        
        details[open] summary {{
            margin-bottom: 0.8rem;
        }}
        
        .detail-content {{
            padding: 1rem;
            background: white;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }}
        
        ul {{
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }}
        
        li {{
            margin-bottom: 0.3rem;
        }}
        
        /* Modal styles for task dependency viewer */
        .modal {{
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
        }}
        
        .modal-content {{
            background-color: #fefefe;
            margin: 2% auto;
            padding: 0;
            border: none;
            border-radius: 12px;
            width: 90%;
            max-width: 1400px;
            max-height: 90vh;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            animation: modalSlideIn 0.3s ease-out;
        }}
        
        @keyframes modalSlideIn {{
            from {{
                transform: translateY(-50px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        .modal-header {{
            background: linear-gradient(135deg, var(--secondary), var(--primary));
            color: white;
            padding: 1.5rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .modal-header h2 {{
            margin: 0;
            font-size: 1.5rem;
        }}
        
        .close-modal {{
            color: white;
            font-size: 2rem;
            font-weight: bold;
            cursor: pointer;
            background: none;
            border: none;
            padding: 0;
            line-height: 1;
            transition: transform 0.2s;
        }}
        
        .close-modal:hover {{
            transform: scale(1.2);
        }}
        
        .modal-body {{
            padding: 2rem;
            overflow-y: auto;
            max-height: calc(90vh - 120px);
        }}
        
        .task-network-view {{
            display: grid;
            grid-template-columns: 1fr 450px;
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .task-graph {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1.5rem;
            min-height: 400px;
        }}
        
        .task-detail-panel {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 1.5rem;
            position: sticky;
            top: 0;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .task-node {{
            background: white;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }}
        
        .task-node:hover {{
            border-color: var(--secondary);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
            transform: translateX(5px);
        }}
        
        .task-node.selected {{
            border-color: var(--secondary);
            background: #e7f3ff;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }}
        
        .task-node.dependency {{
            border-color: #ffc107;
            background: #fff9e6;
        }}
        
        .task-node.dependent {{
            border-color: #28a745;
            background: #f0fff4;
        }}
        
        .task-node-header {{
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 0.25rem;
            font-size: 0.95rem;
        }}
        
        .task-node-meta {{
            font-size: 0.8rem;
            color: #6c757d;
        }}
        
        .dependency-link {{
            color: var(--secondary);
            text-decoration: none;
            cursor: pointer;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            transition: background 0.2s;
            font-weight: 500;
        }}
        
        .dependency-link:hover {{
            background: #e7f3ff;
            text-decoration: underline;
        }}
        
        .task-detail-section {{
            margin-bottom: 1.5rem;
        }}
        
        .task-detail-section h4 {{
            color: var(--secondary);
            margin-bottom: 0.75rem;
            font-size: 1rem;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 0.5rem;
        }}
        
        .dependency-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .dependency-list li {{
            padding: 0.75rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 4px;
            font-size: 0.9rem;
            border-left: 3px solid #dee2e6;
            transition: all 0.2s;
        }}
        
        .dependency-list li:hover {{
            background: #e7f3ff;
            border-left-color: var(--secondary);
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }}
        
        .badge-not-started {{ background: #e9ecef; color: #495057; }}
        .badge-in-progress {{ background: #fff3cd; color: #856404; }}
        .badge-completed {{ background: #d4edda; color: #155724; }}
        .badge-blocked {{ background: #f8d7da; color: #721c24; }}
        
        .task-clickable {{
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .task-clickable:hover {{
            background: #e7f3ff !important;
            transform: translateX(3px);
        }}
        
        .view-dependencies-btn {{
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.4rem 0.8rem;
            background: var(--secondary);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .view-dependencies-btn:hover {{
            background: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        @media (max-width: 1024px) {{
            .task-network-view {{
                grid-template-columns: 1fr;
            }}
            
            .task-detail-panel {{
                position: static;
                max-height: none;
            }}
        }}
    </style>
    
    <script>
        // Task dependency viewer functionality
        let allTasks = {{}};
        let currentScenario = null;
        let currentQuality = null;
        
        function openTaskDependencyViewer(scenarioName, qualityLevel, tasks) {{
            allTasks = {{}};
            tasks.forEach(task => {{
                allTasks[task.id] = task;
            }});
            
            currentScenario = scenarioName;
            currentQuality = qualityLevel;
            
            const modal = document.getElementById('taskDependencyModal');
            const modalTitle = document.getElementById('modalTitle');
            const taskGraph = document.getElementById('taskGraph');
            
            modalTitle.textContent = `Task Dependencies: ${{scenarioName}} (${{qualityLevel.toUpperCase()}})`;
            
            // Render all tasks in the graph
            let graphHTML = '<div style="margin-bottom: 1rem;"><strong>All Tasks (${{tasks.length}} total)</strong></div>';
            tasks.forEach((task, index) => {{
                const stateEmoji = {{
                    'not-started': '⚪',
                    'in-progress': '🟡',
                    'completed': '✅',
                    'blocked': '🔴'
                }}[task.state] || '⚪';
                
                graphHTML += `
                    <div class="task-node" data-task-id="${{task.id}}" onclick="selectTask('${{task.id}}')">
                        <div class="task-node-header">${{index + 1}}. ${{task.name}}</div>
                        <div class="task-node-meta">
                            ${{stateEmoji}} ${{task.state.replace('-', ' ')}} | 
                            👤 ${{task.assignees.join(', ') || 'Unassigned'}}
                            ${{task.dependencies.length > 0 ? ` | 🔗 ${{task.dependencies.length}} deps` : ''}}
                        </div>
                    </div>
                `;
            }});
            
            taskGraph.innerHTML = graphHTML;
            
            // Select first task by default
            if (tasks.length > 0) {{
                selectTask(tasks[0].id);
            }}
            
            modal.style.display = 'block';
        }}
        
        function selectTask(taskId) {{
            const task = allTasks[taskId];
            if (!task) return;
            
            // Update selected state in graph
            document.querySelectorAll('.task-node').forEach(node => {{
                node.classList.remove('selected', 'dependency', 'dependent');
                const nodeId = node.getAttribute('data-task-id');
                
                if (nodeId === taskId) {{
                    node.classList.add('selected');
                }} else if (task.dependencies.includes(nodeId)) {{
                    node.classList.add('dependency');
                }} else if (allTasks[nodeId] && allTasks[nodeId].dependencies.includes(taskId)) {{
                    node.classList.add('dependent');
                }}
            }});
            
            // Update detail panel
            const detailPanel = document.getElementById('taskDetailPanel');
            const stateEmoji = {{
                'not-started': '⚪',
                'in-progress': '🟡',
                'completed': '✅',
                'blocked': '🔴'
            }}[task.state] || '⚪';
            
            const stateBadge = `badge-${{task.state}}`;
            
            let html = `
                <div class="task-detail-section">
                    <h3 style="color: var(--primary); margin-bottom: 1rem;">${{task.name}}</h3>
                    <div style="margin-bottom: 1rem;">
                        <span class="badge ${{stateBadge}}">${{stateEmoji}} ${{task.state.replace('-', ' ').toUpperCase()}}</span>
                    </div>
                </div>
                
                <div class="task-detail-section">
                    <h4>📋 Description</h4>
                    <p style="font-size: 0.9rem; color: #495057; line-height: 1.6;">
                        ${{task.details || '<em>No additional details provided</em>'}}
                    </p>
                </div>
                
                <div class="task-detail-section">
                    <h4>👤 Owner(s)</h4>
                    <p style="font-size: 0.9rem;">${{task.assignees.join(', ') || 'Unassigned'}}</p>
                </div>
            `;
            
            // Dependencies (tasks this task depends on)
            if (task.dependencies.length > 0) {{
                html += `
                    <div class="task-detail-section">
                        <h4>🔗 Dependencies (${{task.dependencies.length}})</h4>
                        <p style="font-size: 0.85rem; color: #6c757d; margin-bottom: 0.75rem;">This task depends on:</p>
                        <ul class="dependency-list">
                `;
                task.dependencies.forEach(depId => {{
                    const depTask = allTasks[depId];
                    if (depTask) {{
                        html += `
                            <li onclick="selectTask('${{depId}}')" style="cursor: pointer;">
                                <strong>${{depTask.name}}</strong><br>
                                <span style="font-size: 0.85rem; color: #6c757d;">
                                    👤 ${{depTask.assignees.join(', ') || 'Unassigned'}}
                                </span>
                            </li>
                        `;
                    }}
                }});
                html += `
                        </ul>
                    </div>
                `;
            }}
            
            // Dependents (tasks that depend on this task)
            const dependents = Object.values(allTasks).filter(t => 
                t.dependencies.includes(taskId)
            );
            
            if (dependents.length > 0) {{
                html += `
                    <div class="task-detail-section">
                        <h4>⬆️ Blocks These Tasks (${{dependents.length}})</h4>
                        <p style="font-size: 0.85rem; color: #6c757d; margin-bottom: 0.75rem;">These tasks depend on this one:</p>
                        <ul class="dependency-list">
                `;
                dependents.forEach(depTask => {{
                    html += `
                        <li onclick="selectTask('${{depTask.id}}')" style="cursor: pointer;">
                            <strong>${{depTask.name}}</strong><br>
                            <span style="font-size: 0.85rem; color: #6c757d;">
                                👤 ${{depTask.assignees.join(', ') || 'Unassigned'}}
                            </span>
                        </li>
                    `;
                }});
                html += `
                        </ul>
                    </div>
                `;
            }}
            
            // Deliverables
            if (task.deliverables && task.deliverables.length > 0) {{
                html += `
                    <div class="task-detail-section">
                        <h4>📦 Deliverables (${{task.deliverables.length}})</h4>
                        <ul style="margin-left: 1.5rem; font-size: 0.9rem;">
                `;
                task.deliverables.forEach(del => {{
                    html += `<li>${{del}}</li>`;
                }});
                html += `
                        </ul>
                    </div>
                `;
            }}
            
            detailPanel.innerHTML = html;
            
            // Scroll selected task into view
            const selectedNode = document.querySelector(`.task-node[data-task-id="${{taskId}}"]`);
            if (selectedNode) {{
                selectedNode.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }}
        }}
        
        function closeTaskDependencyViewer() {{
            document.getElementById('taskDependencyModal').style.display = 'none';
        }}
        
        // Toggle Me Notes profile visibility
        function toggleMeNotes(element) {{
            // Find the parent container that holds both the name and the profile
            let parent = element.parentElement;
            while (parent && !parent.querySelector('.me-notes-profile')) {{
                parent = parent.parentElement;
            }}
            
            if (parent) {{
                const meNotesProfile = parent.querySelector('.me-notes-profile');
                if (meNotesProfile) {{
                    if (meNotesProfile.style.display === 'none' || meNotesProfile.style.display === '') {{
                        meNotesProfile.style.display = 'block';
                        const span = element.querySelector('span');
                        if (span) span.textContent = '📋 Hide Profile';
                    }} else {{
                        meNotesProfile.style.display = 'none';
                        const span = element.querySelector('span');
                        if (span) span.textContent = '📋 View Profile';
                    }}
                }}
            }}
        }}
        
        // Close modal when clicking outside
        window.onclick = function(event) {{
            const modal = document.getElementById('taskDependencyModal');
            if (event.target === modal) {{
                closeTaskDependencyViewer();
            }}
        }}
        
        // Close modal on Escape key
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Escape') {{
                closeTaskDependencyViewer();
            }}
        }});
    </script>
</head>
<body>
    <!-- Task Dependency Modal -->
    <div id="taskDependencyModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Task Dependencies</h2>
                <button class="close-modal" onclick="closeTaskDependencyViewer()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="task-network-view">
                    <div class="task-graph" id="taskGraph">
                        <!-- Task nodes will be dynamically inserted here -->
                    </div>
                    <div class="task-detail-panel" id="taskDetailPanel">
                        <p style="color: #6c757d; text-align: center; padding: 2rem;">
                            Select a task to view details
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <header>
        <div class="header-content">
            <h1>📋 Workback Planning Dashboard</h1>
            <p class="subtitle">Comprehensive Test Suite: {total_scenarios} Scenarios × 3 Quality Levels = {total_plans} Workback Plans</p>
        </div>
    </header>
    
    <nav id="nav">
        <div class="nav-content">
            <a href="#dashboard" class="nav-link">📊 Dashboard</a>
            <a href="#companies-section" class="nav-link">🏢 Companies</a>
            <a href="#scenarios-section" class="nav-link">🎬 Scenarios</a>
            <a href="#plans-section" class="nav-link">📋 Plans</a>
            <a href="#meeting-types-section" class="nav-link">📅 Meeting Types</a>
        </div>
    </nav>
    
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
        <h3>📑 Quick Navigation</h3>
        
        <div class="sidebar-section">
            <div class="sidebar-section-title">Overview Sections</div>
            <ul class="sidebar-nav">
                <li><a href="#dashboard" class="sidebar-link">📊 Dashboard</a></li>
                <li><a href="#companies-section" class="sidebar-link">🏢 Companies</a></li>
                <li><a href="#scenarios-section" class="sidebar-link">🎬 Scenarios</a></li>
                <li><a href="#plans-section" class="sidebar-link">📋 Workback Plans</a></li>
                <li><a href="#meeting-types-section" class="sidebar-link">📅 Meeting Types</a></li>
                <li><a href="#tasks-section" class="sidebar-link">✅ Tasks</a></li>
                <li><a href="#stakeholders-section" class="sidebar-link">👥 Stakeholders</a></li>
                <li><a href="#deliverables-section" class="sidebar-link">📦 Deliverables</a></li>
                <li><a href="#model-section" class="sidebar-link">🤖 Model Info</a></li>
            </ul>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-section-title">Companies ({total_companies})</div>
            <ul class="sidebar-nav">
"""
    
    # Add company links to sidebar
    for company_name in sorted(companies.keys()):
        company_id = company_name.replace(' ', '-').replace(',', '').replace('.', '').lower()
        company_data = companies[company_name]
        scenario_count = len(company_data['scenarios'])
        html += f'                <li><a href="#{company_id}" class="sidebar-link" title="{scenario_count} scenarios">{company_name}</a></li>\n'
    
    html += """            </ul>
        </div>
    </aside>
    
    <div class="container">
        <!-- Dashboard Section -->
        <section id="dashboard" class="dashboard">
            <h2>📊 Executive Dashboard</h2>
            
            <div class="metrics-grid">
                <a href="#companies-section" class="metric-card">
                    <div class="metric-label">Companies</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#scenarios-section" class="metric-card">
                    <div class="metric-label">Scenarios</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#plans-section" class="metric-card">
                    <div class="metric-label">Workback Plans</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#meeting-types-section" class="metric-card">
                    <div class="metric-label">Meeting Types</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#tasks-section" class="metric-card">
                    <div class="metric-label">Total Tasks</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#stakeholders-section" class="metric-card">
                    <div class="metric-label">Stakeholders</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#deliverables-section" class="metric-card">
                    <div class="metric-label">Deliverables</div>
                    <div class="metric-value">{}</div>
                </a>
                <a href="#model-section" class="metric-card">
                    <div class="metric-label">Model Used</div>
                    <div class="metric-value" style="font-size: 1.5rem;">gpt-oss:120b</div>
                </a>
            </div>
            
            <p style="color: #6c757d; font-size: 0.95rem;">
                <strong>Generated:</strong> {} | 
                <strong>Last Updated:</strong> {}
            </p>
        </section>
""".format(
        total_companies,
        total_scenarios,
        total_plans,
        total_meeting_types,
        total_tasks,
        total_stakeholders,
        total_deliverables,
        master_index.get('generated_at', 'Unknown'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    # Companies Overview Section
    html += """
        <!-- Companies Overview -->
        <section id="companies-section" class="dashboard">
            <h2>🏢 Companies Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                This test suite spans <strong>{}</strong> diverse companies across different industries and organizational structures. 
                Each company represents a unique business context for evaluating workback planning capabilities. Companies were 
                extracted from scenario contexts to ensure realistic organizational settings and stakeholder dynamics. Use this 
                section to explore how workback planning adapts to different company sizes, cultures, and meeting requirements.
            </p>
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Context Diversity:</strong> Tests how well workback plans adapt to different organizational contexts</li>
                    <li><strong>Stakeholder Analysis:</strong> Validates appropriate stakeholder identification across company types</li>
                    <li><strong>Relevance Testing:</strong> Ensures plans are contextually appropriate for each company's needs</li>
                </ul>
            </div>
        </section>
        
        <!-- Scenarios Overview -->
        <section id="scenarios-section" class="dashboard">
            <h2>🎬 Scenarios Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                The test suite contains <strong>{}</strong> realistic meeting scenarios spanning 11 different meeting types. Each scenario 
                represents a unique business situation requiring workback planning, from routine weekly newsletters (T-7) to complex 
                M&A integrations (T-90+). Scenarios include detailed company context, meeting objectives, key stakeholders, and expected 
                deliverables to provide rich input for the workback planning generator.
            </p>
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Coverage Testing:</strong> Each scenario generates 3 quality levels (low/medium/high) for comparison</li>
                    <li><strong>Accuracy Validation:</strong> Rich context enables testing of fact extraction and timeline accuracy</li>
                    <li><strong>Completeness Assessment:</strong> Scenarios provide ground truth for required tasks and deliverables</li>
                </ul>
            </div>
        </section>
        
        <!-- Workback Plans Overview -->
        <section id="plans-section" class="dashboard">
            <h2>📋 Workback Plans Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                This dashboard showcases <strong>{}</strong> generated workback plans—three quality levels (low, medium, high) for each 
                of the 33 scenarios. Each plan includes structured tasks with dependencies, responsible parties, deliverables, milestones, 
                and risk considerations. The quality differentiation enables systematic evaluation of the ACRUE framework's ability to 
                distinguish between poor, acceptable, and exceptional workback plans.
            </p>
            
            <!-- Mini TOC for Plan Quality Levels -->
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Quick Jump to Quality Levels:</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <a href="#plan-quality-low" style="color: var(--secondary); text-decoration: none; padding: 1rem; border-radius: 4px; background: white; text-align: center; font-weight: 600;">🔴 Low Quality (50-65%)</a>
                    <a href="#plan-quality-medium" style="color: var(--secondary); text-decoration: none; padding: 1rem; border-radius: 4px; background: white; text-align: center; font-weight: 600;">🟡 Medium Quality (70-80%)</a>
                    <a href="#plan-quality-high" style="color: var(--secondary); text-decoration: none; padding: 1rem; border-radius: 4px; background: white; text-align: center; font-weight: 600;">🟢 High Quality (85-95%)</a>
                </div>
            </div>
            
            <!-- Low Quality Plans -->
            <div id="plan-quality-low" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: #dc3545; margin-bottom: 1rem;">🔴 Low Quality Plans (50-65% Expected Score)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Low-quality workback plans represent poorly prepared meeting scenarios with insufficient 
                    planning detail, missing critical tasks, vague descriptions, and inadequate risk management. These plans demonstrate 
                    common failure patterns and serve as negative examples for evaluation.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP Evaluation:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests ACRUE framework's ability to identify and score inadequate planning</li>
                        <li>Validates detection of missing tasks, unclear responsibilities, and poor dependencies</li>
                        <li>Establishes lower bound for acceptable workback planning quality</li>
                        <li>Demonstrates what NOT to do in meeting preparation</li>
                    </ul>
                </div>
                <div style="background: #fff5f5; padding: 1rem; border-radius: 6px; border-left: 4px solid #dc3545;">
                    <strong style="color: var(--primary);">Characteristics of Low Quality Plans:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 20-30 tasks (missing critical preparation steps, vague descriptions)</li>
                        <li><strong>Completeness:</strong> Missing key phases (approval cycles, risk management, contingency planning)</li>
                        <li><strong>Accuracy:</strong> Incorrect dependencies, unrealistic timelines, wrong stakeholder assignments</li>
                        <li><strong>Relevance:</strong> Generic tasks not tailored to meeting type or company context</li>
                        <li><strong>Usefulness:</strong> Vague task descriptions like "Prepare materials" without specifics</li>
                        <li><strong>Exceptional:</strong> No innovation, no risk mitigation, no optimization strategies</li>
                    </ul>
                </div>
            </div>
            
            <!-- Medium Quality Plans -->
            <div id="plan-quality-medium" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: #ffc107; margin-bottom: 1rem;">🟡 Medium Quality Plans (70-80% Expected Score)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Medium-quality workback plans represent adequate meeting preparation with most essential 
                    tasks included, reasonable detail, and basic dependencies mapped. These plans meet minimum standards but lack the 
                    sophistication, optimization, and risk management of high-quality plans.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP Evaluation:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests ACRUE framework's ability to recognize adequate but not exceptional planning</li>
                        <li>Validates scoring of plans that meet requirements without exceeding them</li>
                        <li>Establishes baseline for acceptable production-ready workback plans</li>
                        <li>Demonstrates "good enough" planning that gets meetings done but isn't optimal</li>
                    </ul>
                </div>
                <div style="background: #fffbf0; padding: 1rem; border-radius: 6px; border-left: 4px solid #ffc107;">
                    <strong style="color: var(--primary);">Characteristics of Medium Quality Plans:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 35-45 tasks (most essential steps covered, reasonable level of detail)</li>
                        <li><strong>Completeness:</strong> Core phases present (preparation, review, execution) but may lack refinement</li>
                        <li><strong>Accuracy:</strong> Dependencies mostly correct, timelines reasonable, stakeholders appropriately identified</li>
                        <li><strong>Relevance:</strong> Tasks generally appropriate for meeting type and context</li>
                        <li><strong>Usefulness:</strong> Task descriptions actionable with clear owners and due dates</li>
                        <li><strong>Exceptional:</strong> Limited innovation, basic risk identification, minimal optimization</li>
                    </ul>
                </div>
            </div>
            
            <!-- High Quality Plans -->
            <div id="plan-quality-high" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: #28a745; margin-bottom: 1rem;">🟢 High Quality Plans (85-95% Expected Score)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> High-quality workback plans represent exceptional meeting preparation with comprehensive 
                    task coverage, detailed execution guidance, sophisticated dependency management, proactive risk mitigation, and 
                    optimization strategies. These plans demonstrate best practices and production-ready excellence.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP Evaluation:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests ACRUE framework's ability to recognize and reward exceptional planning</li>
                        <li>Validates detection of innovation, optimization, and excellence indicators</li>
                        <li>Establishes gold standard for production-ready workback planning</li>
                        <li>Demonstrates best practices for enterprise meeting preparation</li>
                    </ul>
                </div>
                <div style="background: #f0fff4; padding: 1rem; border-radius: 6px; border-left: 4px solid #28a745;">
                    <strong style="color: var(--primary);">Characteristics of High Quality Plans:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 50-70+ tasks (comprehensive coverage with detailed execution steps)</li>
                        <li><strong>Completeness:</strong> All phases present (concept, planning, content, review, approval, execution, follow-up)</li>
                        <li><strong>Accuracy:</strong> Precise dependencies, realistic timelines with buffers, detailed stakeholder RACI</li>
                        <li><strong>Relevance:</strong> Tasks perfectly tailored to meeting type, company culture, and strategic context</li>
                        <li><strong>Usefulness:</strong> Highly actionable descriptions with acceptance criteria, templates, and examples</li>
                        <li><strong>Exceptional:</strong> Innovation in approach, proactive risk mitigation, optimization strategies, quality gates, stakeholder engagement excellence</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Quality Differentiation:</strong> Low (50-65%), Medium (70-80%), High (85-95%) scores expected</li>
                    <li><strong>Framework Validation:</strong> Tests all 50 ACRUE assertions across diverse plan qualities</li>
                    <li><strong>Model Comparison:</strong> Enables evaluation of different LLM models (gpt-oss:120b, GPT-4, Claude, etc.)</li>
                    <li><strong>Production Readiness:</strong> High-quality plans demonstrate production-ready workback planning capabilities</li>
                </ul>
            </div>
        </section>
        
        <!-- Meeting Types Overview -->
        <section id="meeting-types-section" class="dashboard">
            <h2>📅 Meeting Types Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                The test suite covers <strong>{}</strong> distinct meeting types, each with unique planning horizons and complexity levels. 
                Each type represents different enterprise scenarios that require workback planning, from routine operations to strategic 
                initiatives. Below are detailed descriptions of each meeting type, their relevance to our workback planning project, and 
                characteristics of ideal plans.
            </p>
            
            <!-- Mini TOC for Meeting Types -->
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Quick Jump to Meeting Types:</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem;">
                    <a href="#mt-1-weekly-newsletter" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">📰 Weekly Newsletter (T-7)</a>
                    <a href="#mt-2-sprint-planning" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">🏃 Sprint Planning (T-14)</a>
                    <a href="#mt-3-monthly-review" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">📊 Monthly Business Review (T-30)</a>
                    <a href="#mt-4-feature-launch" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">🚀 Feature Launch (T-30)</a>
                    <a href="#mt-5-squad-mission" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">👥 Squad Mission Planning (T-42 to T-56)</a>
                    <a href="#mt-6-quarterly-review" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">📈 Quarterly Business Review (T-60)</a>
                    <a href="#mt-7-annual-kickoff" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">🎯 Annual Kickoff (T-60)</a>
                    <a href="#mt-8-product-launch" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">🎉 Major Product Launch (T-90)</a>
                    <a href="#mt-9-strategic-offsite" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">🏔️ Strategic Offsite (T-90)</a>
                    <a href="#mt-10-board-meeting" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">👔 Board Meeting (T-90)</a>
                    <a href="#mt-11-ma-integration" style="color: var(--secondary); text-decoration: none; padding: 0.5rem; border-radius: 4px; background: white;">🤝 M&A Integration (T-90+)</a>
                </div>
            </div>
            
            <!-- Meeting Type 1: Weekly Newsletter -->
            <div id="mt-1-weekly-newsletter" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">📰 Weekly Newsletter (T-7)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Regular internal communication to teams, typically recurring weekly. Involves content 
                    gathering, editing, approval, and distribution. Represents the simplest meeting type with shortest planning horizon.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests minimal viable workback planning for routine, repeating events</li>
                        <li>Validates context-aware completeness (shouldn't require complex phases or approvals)</li>
                        <li>Establishes baseline for simple task sequencing and timeline management</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 15-25 tasks (content collection, draft, review, approval, distribution)</li>
                        <li><strong>Timeline:</strong> Simple linear sequence over 7 days</li>
                        <li><strong>Stakeholders:</strong> Editor, contributors (3-5), approver, distribution list</li>
                        <li><strong>Deliverables:</strong> Content submissions, draft newsletter, final newsletter</li>
                        <li><strong>Key Characteristics:</strong> No phases needed, minimal dependencies, straightforward approval chain</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 2: Sprint Planning -->
            <div id="mt-2-sprint-planning" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🏃 Sprint Planning (T-14)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Two-week agile sprint planning for software development teams. Involves backlog 
                    refinement, capacity planning, story estimation, and sprint goal setting. Common in technology organizations.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests agile methodology understanding and sprint preparation workflows</li>
                        <li>Validates technical stakeholder identification (Product Owner, Scrum Master, Dev Team)</li>
                        <li>Assesses understanding of iterative development practices and dependencies</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 20-30 tasks (backlog grooming, capacity review, story estimation, dependency mapping)</li>
                        <li><strong>Timeline:</strong> Two weeks with key milestones (refinement sessions, pre-planning, planning day)</li>
                        <li><strong>Stakeholders:</strong> Product Owner, Scrum Master, Development Team (5-9), stakeholders</li>
                        <li><strong>Deliverables:</strong> Refined backlog, estimated stories, sprint goal, committed work items</li>
                        <li><strong>Key Characteristics:</strong> Iterative preparation, technical terminology, velocity considerations</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 3: Monthly Business Review -->
            <div id="mt-3-monthly-review" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">📊 Monthly Business Review (T-30)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Regular business performance review covering metrics, KPIs, financial results, and 
                    operational updates. Involves data gathering, analysis, deck preparation, and executive presentations.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests data-driven planning with analytics and reporting workflows</li>
                        <li>Validates understanding of business metrics and KPI preparation</li>
                        <li>Assesses executive communication and presentation preparation patterns</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 30-40 tasks (data collection, analysis, deck creation, review cycles, rehearsals)</li>
                        <li><strong>Timeline:</strong> 30 days with phases (data gathering, analysis, content creation, review/approval)</li>
                        <li><strong>Stakeholders:</strong> Business leaders, analysts, finance team, executive reviewers</li>
                        <li><strong>Deliverables:</strong> Data reports, analysis documents, presentation deck, executive summary</li>
                        <li><strong>Key Characteristics:</strong> Data dependencies, multiple review cycles, executive-ready polish</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 4: Feature Launch -->
            <div id="mt-4-feature-launch" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🚀 Feature Launch (T-30)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Product feature release planning with go-to-market activities. Includes development 
                    completion, testing, documentation, marketing materials, and customer communication.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests cross-functional coordination (engineering, product, marketing, support)</li>
                        <li>Validates launch readiness criteria and go/no-go decision planning</li>
                        <li>Assesses risk management for customer-facing releases</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 35-45 tasks (feature complete, testing, docs, marketing, training, launch)</li>
                        <li><strong>Timeline:</strong> 30 days with clear phases (development wrap-up, validation, enablement, launch)</li>
                        <li><strong>Stakeholders:</strong> Product Manager, Engineering Lead, Marketing, Sales, Support, Customers</li>
                        <li><strong>Deliverables:</strong> Feature documentation, test reports, marketing materials, training guides, launch plan</li>
                        <li><strong>Key Characteristics:</strong> Launch readiness criteria, rollback plans, customer communication strategy</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 5: Squad Mission Planning -->
            <div id="mt-5-squad-mission" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">👥 Squad Mission Planning (T-42 to T-56)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Microsoft GXP-style squad planning using MMM (Mission, Metrics, Methods) framework. 
                    Cross-functional team (8-12 people: DRI, PM, Engineering, UX, Data Science) planning 6-8 week initiatives.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests Microsoft-specific planning methodologies and frameworks</li>
                        <li>Validates multi-disciplinary team coordination and role clarity</li>
                        <li>Assesses mission-driven planning with measurable outcomes</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 40-50 tasks (mission definition, metrics setup, method design, execution planning)</li>
                        <li><strong>Timeline:</strong> 42-56 days with MMM framework stages and checkpoint reviews</li>
                        <li><strong>Stakeholders:</strong> DRI, PM, Engineering Lead, UX Designer, Data Scientist, stakeholders (8-12 total)</li>
                        <li><strong>Deliverables:</strong> Mission statement, success metrics, method documentation, execution roadmap</li>
                        <li><strong>Key Characteristics:</strong> MMM framework adherence, cross-functional dependencies, checkpoint gates</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 6: Quarterly Business Review -->
            <div id="mt-6-quarterly-review" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">📈 Quarterly Business Review (T-60)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Comprehensive quarterly performance review with board-level stakeholders. Includes 
                    financial results, strategic progress, market analysis, and forward-looking plans for next quarter.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests executive-level planning with strategic content and board readiness</li>
                        <li>Validates financial reporting workflows and compliance requirements</li>
                        <li>Assesses high-stakes presentation preparation with multiple review layers</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 45-60 tasks (data consolidation, analysis, strategic narrative, exec reviews, board prep)</li>
                        <li><strong>Timeline:</strong> 60 days with distinct phases (data close, analysis, content, executive review, board prep)</li>
                        <li><strong>Stakeholders:</strong> CFO, COO, Business Unit Leaders, Finance Team, Board Members, Legal</li>
                        <li><strong>Deliverables:</strong> Financial reports, strategic analysis, board deck, Q&A prep, forward outlook</li>
                        <li><strong>Key Characteristics:</strong> Multi-level approvals, financial accuracy, strategic insights, board readiness</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 7: Annual Kickoff -->
            <div id="mt-7-annual-kickoff" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🎯 Annual Kickoff (T-60)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Company or team annual kickoff event with vision-setting, goal alignment, and team 
                    building. Includes venue planning, content development, logistics, and post-event follow-up.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests event planning combined with strategic messaging and team engagement</li>
                        <li>Validates logistical coordination alongside content and culture considerations</li>
                        <li>Assesses inspirational messaging and organizational alignment planning</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 40-55 tasks (theme/vision, venue, agenda, content, speakers, logistics, follow-up)</li>
                        <li><strong>Timeline:</strong> 60 days with phases (concept, planning, content creation, logistics, execution, follow-up)</li>
                        <li><strong>Stakeholders:</strong> Leadership team, event planners, content creators, speakers, attendees, vendors</li>
                        <li><strong>Deliverables:</strong> Vision narrative, event agenda, presentations, materials, post-event content</li>
                        <li><strong>Key Characteristics:</strong> Inspirational messaging, logistical precision, engagement activities, culture building</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 8: Major Product Launch -->
            <div id="mt-8-product-launch" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🎉 Major Product Launch (T-90)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Large-scale product release with market impact. Includes product readiness, go-to-market 
                    strategy, partnerships, press/analyst relations, customer migration, and post-launch monitoring.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests complex, multi-workstream planning with interdependent tracks</li>
                        <li>Validates market-facing launch orchestration with external stakeholders</li>
                        <li>Assesses risk management for high-visibility, high-impact releases</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 60-80 tasks across multiple tracks (product, marketing, sales, support, legal, PR)</li>
                        <li><strong>Timeline:</strong> 90 days with clear phases (readiness, GTM prep, launch execution, post-launch)</li>
                        <li><strong>Stakeholders:</strong> Product, Engineering, Marketing, Sales, PR, Legal, Partners, Analysts, Customers</li>
                        <li><strong>Deliverables:</strong> Product docs, GTM plan, marketing campaign, sales enablement, press kit, success metrics</li>
                        <li><strong>Key Characteristics:</strong> Multiple workstreams, launch readiness gates, crisis response plans, market coordination</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 9: Strategic Offsite -->
            <div id="mt-9-strategic-offsite" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🏔️ Strategic Offsite (T-90)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Executive strategy session at off-site location for deep strategic planning. Includes 
                    pre-work, facilitation design, strategic frameworks, scenario planning, and action planning.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests strategic planning preparation with pre-work and framework development</li>
                        <li>Validates facilitation design and executive engagement planning</li>
                        <li>Assesses long-term strategic thinking and scenario analysis preparation</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 50-65 tasks (pre-work, strategic analysis, facilitation design, venue, materials, follow-up)</li>
                        <li><strong>Timeline:</strong> 90 days with phases (pre-work, content prep, logistics, execution, action planning)</li>
                        <li><strong>Stakeholders:</strong> C-suite, Strategy team, facilitators, key leaders, external advisors</li>
                        <li><strong>Deliverables:</strong> Pre-read materials, strategic frameworks, session design, action plans, follow-up commitments</li>
                        <li><strong>Key Characteristics:</strong> Strategic depth, executive engagement, scenario planning, actionable outcomes</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 10: Board Meeting -->
            <div id="mt-10-board-meeting" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">👔 Board Meeting (T-90)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Formal board of directors meeting with fiduciary responsibilities. Includes financial 
                    reporting, governance matters, strategic decisions, risk oversight, and regulatory compliance.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests highest-level governance and compliance planning requirements</li>
                        <li>Validates legal/regulatory considerations and documentation standards</li>
                        <li>Assesses board-grade quality standards and fiduciary care in planning</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 55-70 tasks (materials prep, legal review, financial close, resolutions, minutes, compliance)</li>
                        <li><strong>Timeline:</strong> 90 days with rigorous phases (data close, materials, legal review, board prep, follow-up)</li>
                        <li><strong>Stakeholders:</strong> CEO, CFO, Board Members, Legal Counsel, Corporate Secretary, Audit Committee</li>
                        <li><strong>Deliverables:</strong> Board book, financial statements, resolutions, minutes, compliance certifications</li>
                        <li><strong>Key Characteristics:</strong> Legal compliance, fiduciary standards, formal documentation, audit trail, confidentiality</li>
                    </ul>
                </div>
            </div>
            
            <!-- Meeting Type 11: M&A Integration -->
            <div id="mt-11-ma-integration" style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; scroll-margin-top: 160px;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🤝 M&A Integration (T-90+)</h3>
                <p style="color: #495057; line-height: 1.6; margin-bottom: 1rem;">
                    <strong>Description:</strong> Post-acquisition integration planning covering systems, people, processes, and culture. 
                    Most complex meeting type with extended timeline, requiring coordination across organizations and managing uncertainty.
                </p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <strong style="color: var(--primary);">Why Relevant for WBP:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Tests maximum complexity planning with organizational change management</li>
                        <li>Validates handling of uncertainty, cultural integration, and change resistance</li>
                        <li>Assesses comprehensive risk planning and contingency strategies</li>
                    </ul>
                </div>
                <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px;">
                    <strong style="color: var(--primary);">Ideal Expected Plan:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li><strong>Tasks:</strong> 70-100+ tasks across integration tracks (systems, HR, finance, operations, culture, legal)</li>
                        <li><strong>Timeline:</strong> 90+ days with phased integration (Day 1 readiness, 30/60/90-day milestones, long-term)</li>
                        <li><strong>Stakeholders:</strong> Integration team, both company leaders, HR, IT, Finance, Legal, Communications, Employees</li>
                        <li><strong>Deliverables:</strong> Integration plan, Day 1 playbook, systems migration plan, org design, culture integration</li>
                        <li><strong>Key Characteristics:</strong> Multiple parallel tracks, change management, cultural sensitivity, risk mitigation, stakeholder communication</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--info); margin-top: 1.5rem;">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Complexity Scaling:</strong> Tests how well plans adapt from simple (T-7) to complex (T-90+) horizons</li>
                    <li><strong>Context-Aware Completeness:</strong> Simple meetings don't need phases; complex ones require multi-track coordination</li>
                    <li><strong>Relevance Testing:</strong> Tasks must match meeting type characteristics and industry best practices</li>
                    <li><strong>Accuracy Validation:</strong> Stakeholder roles, timelines, and deliverables must be contextually appropriate</li>
                </ul>
            </div>
        </section>
        
        <!-- Tasks Overview -->
        <section id="tasks-section" class="dashboard">
            <h2>✅ Tasks Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                Across all 99 workback plans, the system generated <strong>{}</strong> individual tasks with structured details including 
                descriptions, due dates, responsible parties, dependencies, and deliverables. Task counts vary by quality level: low-quality 
                plans typically have 20-30 tasks with vague descriptions, while high-quality plans include 40-60 detailed tasks with clear 
                dependencies and milestone markers. This variation enables testing of the Completeness dimension in the ACRUE framework.
            </p>
            
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary); margin-bottom: 1.5rem;">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Completeness (C):</strong> Tests presence of all necessary tasks for meeting success</li>
                    <li><strong>Accuracy (A):</strong> Validates correct dependencies, timelines, and responsible parties</li>
                    <li><strong>Usefulness (U):</strong> Ensures tasks are actionable with clear descriptions and owners</li>
                    <li><strong>Exceptional (E):</strong> High-quality plans show innovation in task optimization and risk management</li>
                </ul>
            </div>
            
            <!-- Task Statistics by Quality Level -->
            <div style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">📊 Task Statistics by Quality Level</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
"""
    
    # Calculate task statistics by quality level
    task_stats = {'low': {'count': 0, 'plans': 0}, 'medium': {'count': 0, 'plans': 0}, 'high': {'count': 0, 'plans': 0}}
    
    for company_data in companies.values():
        for scenario in company_data['scenarios']:
            for quality, plan in scenario.get('plans', {}).items():
                if plan and quality in task_stats:
                    tasks = plan.get('plan', {}).get('tasks', [])
                    task_stats[quality]['count'] += len(tasks)
                    task_stats[quality]['plans'] += 1
    
    html += f"""
                    <div style="background: #fff5f5; padding: 1rem; border-radius: 6px; border-left: 4px solid #dc3545;">
                        <div style="font-size: 0.85rem; color: #6c757d; margin-bottom: 0.5rem;">🔴 Low Quality</div>
                        <div style="font-size: 2rem; font-weight: bold; color: #dc3545; margin-bottom: 0.5rem;">{task_stats['low']['count']}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Across {task_stats['low']['plans']} plans</div>
                        <div style="font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;">Avg: {task_stats['low']['count'] // task_stats['low']['plans'] if task_stats['low']['plans'] > 0 else 0} tasks/plan</div>
                    </div>
                    <div style="background: #fffbf0; padding: 1rem; border-radius: 6px; border-left: 4px solid #ffc107;">
                        <div style="font-size: 0.85rem; color: #6c757d; margin-bottom: 0.5rem;">🟡 Medium Quality</div>
                        <div style="font-size: 2rem; font-weight: bold; color: #ffc107; margin-bottom: 0.5rem;">{task_stats['medium']['count']}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Across {task_stats['medium']['plans']} plans</div>
                        <div style="font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;">Avg: {task_stats['medium']['count'] // task_stats['medium']['plans'] if task_stats['medium']['plans'] > 0 else 0} tasks/plan</div>
                    </div>
                    <div style="background: #f0fff4; padding: 1rem; border-radius: 6px; border-left: 4px solid #28a745;">
                        <div style="font-size: 0.85rem; color: #6c757d; margin-bottom: 0.5rem;">🟢 High Quality</div>
                        <div style="font-size: 2rem; font-weight: bold; color: #28a745; margin-bottom: 0.5rem;">{task_stats['high']['count']}</div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Across {task_stats['high']['plans']} plans</div>
                        <div style="font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem;">Avg: {task_stats['high']['count'] // task_stats['high']['plans'] if task_stats['high']['plans'] > 0 else 0} tasks/plan</div>
                    </div>
                </div>
            </div>
            
            <!-- Task Explorer by Meeting Type -->
            <div style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🔍 Task Explorer by Meeting Type & Quality</h3>
                <p style="color: #6c757d; margin-bottom: 1rem; font-size: 0.95rem;">
                    Explore tasks organized by meeting type and quality level. Click to expand and see sample tasks from each plan.
                </p>
"""
    
    # Group tasks by meeting type
    for meeting_type_key in ['1_weekly_newsletter', '2_sprint_planning', '3_monthly_review', '4_feature_launch', 
                              '5_squad_mission', '6_quarterly_review', '7_annual_kickoff', '8_product_launch', 
                              '9_strategic_offsite', '10_board_meeting', '11_ma_integration']:
        
        meeting_info = MEETING_TYPES.get(meeting_type_key, {})
        meeting_name = meeting_info.get('name', 'Unknown')
        meeting_icon = meeting_info.get('icon', '📋')
        
        # Find scenarios for this meeting type
        meeting_scenarios = []
        for company_data in companies.values():
            for scenario in company_data['scenarios']:
                if scenario.get('meeting_type_key') == meeting_type_key:
                    meeting_scenarios.append(scenario)
        
        if not meeting_scenarios:
            continue
            
        html += f"""
                <details style="margin-bottom: 1rem;">
                    <summary style="cursor: pointer; font-weight: 600; padding: 1rem; background: #f8f9fa; border-radius: 6px; user-select: none;">
                        {meeting_icon} {meeting_name} ({len(meeting_scenarios)} scenarios)
                    </summary>
                    <div style="padding: 1rem; background: white; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 6px 6px;">
"""
        
        # Show tasks for each scenario and quality level
        for scenario_idx, scenario in enumerate(meeting_scenarios[:1], 1):  # Show first scenario as example
            scenario_name = scenario.get('scenario_name', 'Unnamed')
            html += f"""
                        <div style="margin-bottom: 1rem;">
                            <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">Example: {scenario_name}</div>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
"""
            
            for quality in ['low', 'medium', 'high']:
                plan = scenario.get('plans', {}).get(quality)
                if not plan:
                    continue
                    
                tasks = plan.get('plan', {}).get('tasks', [])
                quality_color = {'low': '#dc3545', 'medium': '#ffc107', 'high': '#28a745'}.get(quality, '#6c757d')
                quality_label = {'low': '🔴 Low', 'medium': '🟡 Medium', 'high': '🟢 High'}.get(quality, quality)
                
                html += f"""
                                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; border-left: 4px solid {quality_color};">
                                    <div style="font-weight: 600; color: {quality_color}; margin-bottom: 0.5rem;">{quality_label}</div>
                                    <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary); margin-bottom: 0.5rem;">{len(tasks)} tasks</div>
                                    <details style="margin-top: 0.5rem;">
                                        <summary style="cursor: pointer; font-size: 0.9rem; color: var(--secondary);">View sample tasks (first 5)</summary>
                                        <div style="margin-top: 0.5rem; padding: 0.5rem; background: white; border-radius: 4px; max-height: 300px; overflow-y: auto;">
                                            <ol style="margin: 0; padding-left: 1.5rem; font-size: 0.85rem;">
"""
                
                # Show first 5 tasks
                for task_idx, task in enumerate(tasks[:5], 1):
                    task_id = task.get('id', f'task-{task_idx}')
                    task_name = task.get('name', 'Unnamed task')
                    task_details = task.get('details', '')
                    task_assignees = task.get('assignees', [])
                    task_owner = ', '.join(task_assignees) if task_assignees else 'Unassigned'
                    task_state = task.get('state', 'not-started')
                    dependencies = task.get('dependencies', [])
                    deliverables = task.get('deliverables', [])
                    
                    # Format state with emoji
                    state_emoji = {'not-started': '⚪', 'in-progress': '🟡', 'completed': '✅', 'blocked': '🔴'}.get(task_state, '⚪')
                    
                    html += f"""
                                                <li style="margin-bottom: 1rem; line-height: 1.5; background: #f8f9fa; padding: 0.75rem; border-radius: 6px;">
                                                    <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">
                                                        {task_idx}. {task_name}
                                                    </div>
                                                    <div style="font-size: 0.85rem; color: #495057; margin-bottom: 0.5rem; padding-left: 1rem;">
                                                        {task_details if task_details else '<em style="color: #6c757d;">No additional details provided</em>'}
                                                    </div>
                                                    <div style="font-size: 0.8rem; color: #6c757d; padding-left: 1rem; border-left: 3px solid #dee2e6; margin-top: 0.5rem;">
                                                        <div style="margin-bottom: 0.25rem;">
                                                            <strong>Status:</strong> {state_emoji} {task_state.replace('-', ' ').title()}
                                                        </div>
                                                        <div style="margin-bottom: 0.25rem;">
                                                            <strong>Owner:</strong> 👤 {task_owner}
                                                        </div>
"""
                    if dependencies:
                        dep_list = ', '.join(dependencies) if len(dependencies) <= 3 else f"{', '.join(dependencies[:3])}... (+{len(dependencies)-3} more)"
                        html += f"""                                                        <div style="margin-bottom: 0.25rem;">
                                                            <strong>Dependencies:</strong> 🔗 {dep_list}
                                                        </div>
"""
                    if deliverables:
                        html += f"""                                                        <div>
                                                            <strong>Deliverables:</strong> 📦 {len(deliverables)} item(s)
                                                        </div>
"""
                    html += """                                                    </div>
                                                </li>
"""
                
                if len(tasks) > 5:
                    html += f"""
                                                <li style="font-style: italic; color: #6c757d;">... and {len(tasks) - 5} more tasks</li>
"""
                
                html += """                                            </ol>
                                        </div>
                                    </details>
"""
                
                # Add "View All Dependencies" button with task data
                tasks_json = json.dumps(tasks, ensure_ascii=False).replace("'", "\\'")
                scenario_name_safe = scenario_name.replace("'", "\\'")
                
                html += f"""
                                    <button class="view-dependencies-btn" onclick='openTaskDependencyViewer("{scenario_name_safe}", "{quality}", {tasks_json})'>
                                        🔍 View All {len(tasks)} Tasks & Dependencies
                                    </button>
"""
                
                html += """                                </div>
"""
            
            html += """                            </div>
                        </div>
"""
        
        if len(meeting_scenarios) > 1:
            html += f"""
                        <div style="margin-top: 1rem; padding: 0.75rem; background: #e7f3ff; border-radius: 6px; text-align: center; color: var(--primary);">
                            💡 {len(meeting_scenarios) - 1} more scenario(s) available for this meeting type
                        </div>
"""
        
        html += """                    </div>
                </details>
"""
    
    html += """            </div>
        </section>
        
        <!-- Stakeholders Overview -->
        <section id="stakeholders-section" class="dashboard">
            <h2>👥 Stakeholders Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                The test suite identifies <strong>{}</strong> stakeholders across all scenarios, representing diverse roles including 
                meeting organizers, key participants, reviewers, approvers, and informed parties. Stakeholder analysis is critical for 
                workback planning as it determines who needs to be involved in each task, who needs to approve deliverables, and who 
                should be kept informed. Quality differentiation shows up in stakeholder identification: low-quality plans miss key 
                stakeholders, while high-quality plans include appropriate RACI (Responsible, Accountable, Consulted, Informed) assignments.
            </p>
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary); margin-bottom: 1.5rem;">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Completeness (C):</strong> Tests identification of all necessary stakeholders and their roles</li>
                    <li><strong>Relevance (R):</strong> Validates stakeholders are appropriate for company context and meeting type</li>
                    <li><strong>Accuracy (A):</strong> Ensures correct role assignments and organizational relationships</li>
                    <li><strong>Exceptional (E):</strong> High-quality plans show sophisticated stakeholder engagement strategies</li>
                </ul>
            </div>
            
            <!-- Stakeholders by Company -->
            <div style="background: white; border: 2px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: var(--secondary); margin-bottom: 1rem;">🏢 Stakeholders by Company</h3>
                <p style="color: #6c757d; margin-bottom: 1.5rem; font-size: 0.95rem;">
                    Explore stakeholders organized by their companies. Each company profile includes context and key personnel involved in workback planning scenarios.
                </p>
"""
    
    # Organize stakeholders by company
    company_stakeholders = {}
    
    for company_name, company_data in companies.items():
        stakeholder_set = set()
        
        for scenario in company_data['scenarios']:
            # Get stakeholders from scenario context
            if 'stakeholders' in scenario:
                for stakeholder in scenario['stakeholders']:
                    # Handle both string and dict formats
                    if isinstance(stakeholder, str):
                        stakeholder_set.add(stakeholder)
                    elif isinstance(stakeholder, dict):
                        stakeholder_info = f"{stakeholder.get('name', 'Unknown')} – {stakeholder.get('role', stakeholder.get('details', 'No role'))}"
                        stakeholder_set.add(stakeholder_info)
            
            # Get participants from plans
            for quality in ['low', 'medium', 'high']:
                plan = scenario.get('plans', {}).get(quality)
                if plan and 'plan' in plan:
                    participants = plan['plan'].get('participants', [])
                    for participant in participants:
                        participant_info = f"{participant.get('name', 'Unknown')} – {participant.get('details', 'No details')}"
                        stakeholder_set.add(participant_info)
        
        if stakeholder_set:
            company_stakeholders[company_name] = {
                'stakeholders': sorted(list(stakeholder_set)),
                'context': company_data['scenarios'][0].get('company_context', 'No context available'),
                'scenario_count': len(company_data['scenarios'])
            }
    
    # Display companies and stakeholders
    for company_idx, (company_name, company_info) in enumerate(sorted(company_stakeholders.items()), 1):
        stakeholders = company_info['stakeholders']
        context = company_info['context']
        scenario_count = company_info['scenario_count']
        
        # Extract company type/industry from context
        company_intro = context[:200] + "..." if len(context) > 200 else context
        
        html += f"""
                <details style="margin-bottom: 1rem; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden;">
                    <summary style="cursor: pointer; font-weight: 600; padding: 1rem; background: #f8f9fa; user-select: none; transition: background 0.2s;">
                        <span style="color: var(--primary); font-size: 1.1rem;">🏢 {company_name}</span>
                        <span style="color: #6c757d; font-size: 0.9rem; margin-left: 1rem;">
                            ({len(stakeholders)} stakeholders | {scenario_count} scenarios)
                        </span>
                    </summary>
                    <div style="padding: 1.5rem; background: white;">
                        <!-- Company Context -->
                        <div style="background: #e7f3ff; padding: 1rem; border-radius: 6px; border-left: 4px solid var(--secondary); margin-bottom: 1.5rem;">
                            <h4 style="color: var(--primary); margin-bottom: 0.5rem; font-size: 1rem;">📋 Company Overview</h4>
                            <p style="font-size: 0.9rem; color: #495057; line-height: 1.6; margin: 0;">
                                {context}
                            </p>
                        </div>
                        
                        <!-- Team Structure / Org Chart -->
                        <div style="background: white; border: 2px solid #e9ecef; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
                            <h4 style="color: var(--secondary); margin-bottom: 1rem; font-size: 1rem;">
                                📊 Team Structure & Organization
                            </h4>
"""
        
        # Organize stakeholders by hierarchy levels
        executives = []
        managers = []
        specialists = []
        contributors = []
        
        # Function to generate Me Notes for a stakeholder
        def generate_me_notes(name, role, company_name):
            me_notes = []
            
            # IDENTITY note
            me_notes.append({
                'category': 'IDENTITY',
                'title': f'{name} - {role.split(".")[0] if "." in role else role.split(",")[0] if "," in role else role[:50]}',
                'icon': '🆔',
                'confidence': 0.95
            })
            
            # ORGANIZATIONAL note
            if any(kw in role.lower() for kw in ['director', 'vp', 'manager', 'lead', 'chief']):
                me_notes.append({
                    'category': 'ORGANIZATIONAL',
                    'title': 'Leadership Role',
                    'note': f'Holds leadership position as {role.split(".")[0] if "." in role else role[:100]}',
                    'icon': '🏢',
                    'confidence': 0.9
                })
            
            # WORK_ORGANIZATION note based on role type
            if 'content' in role.lower() or 'writer' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Content Creation Workflow',
                    'note': 'Primary responsibility for content creation, editing, and publication workflows',
                    'icon': '✍️',
                    'confidence': 0.85
                })
            elif 'review' in role.lower() or 'approver' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Approval Authority',
                    'note': 'Designated reviewer and approver for deliverables and sign-offs',
                    'icon': '✅',
                    'confidence': 0.9
                })
            elif 'engineer' in role.lower() or 'developer' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Technical Implementation',
                    'note': 'Responsible for technical development, implementation, and system integration',
                    'icon': '⚙️',
                    'confidence': 0.88
                })
            elif 'design' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Design and UX Responsibility',
                    'note': 'Manages user experience, visual design, and accessibility requirements',
                    'icon': '🎨',
                    'confidence': 0.87
                })
            
            # COLLABORATION note
            if 'coordinator' in role.lower() or 'manager' in role.lower():
                me_notes.append({
                    'category': 'COLLABORATION',
                    'title': 'Cross-functional Collaboration',
                    'note': f'Coordinates across teams and stakeholders in {company_name} for workback planning initiatives',
                    'icon': '🤝',
                    'confidence': 0.82
                })
            
            # MEETING_PATTERNS note
            if 'lead' in role.lower() or 'manager' in role.lower() or 'director' in role.lower():
                me_notes.append({
                    'category': 'MEETING_PATTERNS',
                    'title': 'Regular Meeting Cadence',
                    'note': 'Participates in planning meetings, status reviews, and stakeholder alignments',
                    'icon': '📅',
                    'confidence': 0.8
                })
            
            return me_notes
        
        # Function to render stakeholder card with Me Notes
        def render_stakeholder_card(name, role, icon, color, company_name):
            me_notes = generate_me_notes(name, role, company_name)
            
            card_html = f"""
                                        <div style="background: white; padding: 0.75rem; border-radius: 4px; border-left: 4px solid {color};">
                                            <div style="font-weight: 600; color: {color}; font-size: 0.95rem; cursor: pointer;" onclick="toggleMeNotes(this)">
                                                {icon} {name} <span style="font-size: 0.75rem; color: var(--secondary); margin-left: 0.5rem;">📋 View Profile</span>
                                            </div>
                                            <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.25rem;">{role}</div>
                                            
                                            <!-- Me Notes Profile -->
                                            <div class="me-notes-profile" style="display: none; margin-top: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 6px; border: 2px solid {color}; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                                                <div style="font-weight: 600; color: {color}; margin-bottom: 0.75rem; font-size: 0.95rem;">
                                                    📋 Professional Profile - Me Notes
                                                </div>
"""
            
            for note in me_notes:
                confidence_color = '#28a745' if note['confidence'] >= 0.9 else '#ffc107' if note['confidence'] >= 0.8 else '#6c757d'
                confidence_pct = int(note['confidence'] * 100)
                
                card_html += f"""
                                                <div style="margin-bottom: 0.75rem; padding: 0.75rem; background: white; border-radius: 4px; border-left: 3px solid {confidence_color};">
                                                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.25rem;">
                                                        <div style="font-weight: 600; font-size: 0.85rem; color: var(--primary);">
                                                            {note['icon']} {note['category'].replace('_', ' ').title()}
                                                        </div>
                                                        <div style="font-size: 0.75rem; padding: 0.15rem 0.5rem; background: {confidence_color}; color: white; border-radius: 10px;">
                                                            {confidence_pct}%
                                                        </div>
                                                    </div>
                                                    <div style="font-weight: 500; font-size: 0.85rem; color: #495057; margin-bottom: 0.25rem;">
                                                        {note['title']}
                                                    </div>
"""
                
                if 'note' in note:
                    card_html += f"""
                                                    <div style="font-size: 0.8rem; color: #6c757d; line-height: 1.5;">
                                                        {note['note']}
                                                    </div>
"""
                
                card_html += """
                                                </div>
"""
            
            card_html += """
                                                <div style="margin-top: 0.75rem; padding: 0.5rem; background: #e7f3ff; border-radius: 4px; font-size: 0.75rem; color: #6c757d; text-align: center;">
                                                    💡 Profile generated from workback planning scenario analysis
                                                </div>
                                            </div>
                                        </div>
"""
            return card_html
        
        for stakeholder in stakeholders:
            if '–' in stakeholder or '-' in stakeholder:
                parts = stakeholder.replace('–', '|').replace(' - ', '|').split('|')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    role = '|'.join(parts[1:]).strip()
                else:
                    name = stakeholder
                    role = "No role specified"
            else:
                name = stakeholder
                role = "No role specified"
            
            # Categorize by level
            role_lower = role.lower()
            if any(keyword in role_lower for keyword in ['director', 'vp', 'chief', 'president', 'ceo', 'cfo', 'cto', 'head of']):
                executives.append((name, role))
            elif any(keyword in role_lower for keyword in ['manager', 'lead', 'coordinator', 'supervisor']):
                managers.append((name, role))
            elif any(keyword in role_lower for keyword in ['specialist', 'expert', 'analyst', 'officer', 'consultant']):
                specialists.append((name, role))
            else:
                contributors.append((name, role))
        
        # Display org chart
        if executives:
            html += """
                            <div style="margin-bottom: 1.5rem;">
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1rem; border-radius: 6px 6px 0 0; font-weight: 600; font-size: 0.9rem;">
                                    ⭐ Executive Leadership
                                </div>
                                <div style="background: #f8f9fa; padding: 1rem; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 6px 6px;">
                                    <div style="display: grid; gap: 0.5rem;">
"""
            for name, role in executives:
                html += render_stakeholder_card(name, role, '⭐', '#667eea', company_name)
            html += """
                                    </div>
                                </div>
                            </div>
"""
        
        if managers:
            html += """
                            <div style="margin-bottom: 1.5rem;">
                                <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 0.5rem 1rem; border-radius: 6px 6px 0 0; font-weight: 600; font-size: 0.9rem;">
                                    👔 Management & Team Leads
                                </div>
                                <div style="background: #f8f9fa; padding: 1rem; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 6px 6px;">
                                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 0.5rem;">
"""
            for name, role in managers:
                html += render_stakeholder_card(name, role, '👔', '#3498db', company_name)
            html += """
                                    </div>
                                </div>
                            </div>
"""
        
        if specialists:
            html += """
                            <div style="margin-bottom: 1.5rem;">
                                <div style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); color: white; padding: 0.5rem 1rem; border-radius: 6px 6px 0 0; font-weight: 600; font-size: 0.9rem;">
                                    💼 Specialists & Subject Matter Experts
                                </div>
                                <div style="background: #f8f9fa; padding: 1rem; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 6px 6px;">
                                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.5rem;">
"""
            for name, role in specialists:
                html += render_stakeholder_card(name, role, '💼', '#27ae60', company_name)
            html += """
                                    </div>
                                </div>
                            </div>
"""
        
        if contributors:
            html += """
                            <div style="margin-bottom: 1rem;">
                                <div style="background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%); color: white; padding: 0.5rem 1rem; border-radius: 6px 6px 0 0; font-weight: 600; font-size: 0.9rem;">
                                    👥 Contributors & Team Members
                                </div>
                                <div style="background: #f8f9fa; padding: 1rem; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 6px 6px;">
                                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 0.5rem;">
"""
            for name, role in contributors:
                html += render_stakeholder_card(name, role, '👤', '#95a5a6', company_name)
            html += """
                                    </div>
                                </div>
                            </div>
"""
        
        html += """
                        </div>
                        
                        <!-- Stakeholder List -->
                        <div>
                            <h4 style="color: var(--secondary); margin-bottom: 1rem; font-size: 1rem;">
                                👥 All Stakeholders - Alphabetical List ({len(stakeholders)})
                            </h4>
                            <div style="display: grid; gap: 0.75rem;">
"""
        
        for stakeholder in stakeholders:
            # Parse stakeholder info (format: "Name – Role/Details" or just "Name")
            if '–' in stakeholder or '-' in stakeholder:
                # Split on both em dash and regular dash
                parts = stakeholder.replace('–', '|').replace(' - ', '|').split('|')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    role = '|'.join(parts[1:]).strip()
                else:
                    name = stakeholder
                    role = "No role specified"
            else:
                name = stakeholder
                role = "No role specified"
            
            # Assign icon based on role keywords
            icon = "👤"
            if any(keyword in role.lower() for keyword in ['director', 'vp', 'chief', 'head', 'president']):
                icon = "⭐"
            elif any(keyword in role.lower() for keyword in ['manager', 'lead', 'coordinator']):
                icon = "👔"
            elif any(keyword in role.lower() for keyword in ['engineer', 'developer', 'designer', 'analyst']):
                icon = "💻"
            elif any(keyword in role.lower() for keyword in ['approver', 'reviewer', 'compliance', 'legal']):
                icon = "✅"
            
            # Generate Me Note-style profile for each stakeholder
            me_notes = []
            
            # IDENTITY note
            me_notes.append({
                'category': 'IDENTITY',
                'title': f'{name} - {role.split(".")[0] if "." in role else role.split(",")[0] if "," in role else role[:50]}',
                'icon': '🆔',
                'confidence': 0.95
            })
            
            # ORGANIZATIONAL note
            if any(kw in role.lower() for kw in ['director', 'vp', 'manager', 'lead', 'chief']):
                me_notes.append({
                    'category': 'ORGANIZATIONAL',
                    'title': 'Leadership Role',
                    'note': f'Holds leadership position as {role.split(".")[0] if "." in role else role[:100]}',
                    'icon': '🏢',
                    'confidence': 0.9
                })
            
            # WORK_ORGANIZATION note based on role type
            if 'content' in role.lower() or 'writer' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Content Creation Workflow',
                    'note': 'Primary responsibility for content creation, editing, and publication workflows',
                    'icon': '✍️',
                    'confidence': 0.85
                })
            elif 'review' in role.lower() or 'approver' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Approval Authority',
                    'note': 'Designated reviewer and approver for deliverables and sign-offs',
                    'icon': '✅',
                    'confidence': 0.9
                })
            elif 'engineer' in role.lower() or 'developer' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Technical Implementation',
                    'note': 'Responsible for technical development, implementation, and system integration',
                    'icon': '⚙️',
                    'confidence': 0.88
                })
            elif 'design' in role.lower():
                me_notes.append({
                    'category': 'WORK_ORGANIZATION',
                    'title': 'Design and UX Responsibility',
                    'note': 'Manages user experience, visual design, and accessibility requirements',
                    'icon': '🎨',
                    'confidence': 0.87
                })
            
            # COLLABORATION note
            if 'coordinator' in role.lower() or 'manager' in role.lower():
                me_notes.append({
                    'category': 'COLLABORATION',
                    'title': 'Cross-functional Collaboration',
                    'note': f'Coordinates across teams and stakeholders in {company_name} for workback planning initiatives',
                    'icon': '🤝',
                    'confidence': 0.82
                })
            
            # MEETING_PATTERNS note
            if 'lead' in role.lower() or 'manager' in role.lower() or 'director' in role.lower():
                me_notes.append({
                    'category': 'MEETING_PATTERNS',
                    'title': 'Regular Meeting Cadence',
                    'note': 'Participates in planning meetings, status reviews, and stakeholder alignments',
                    'icon': '📅',
                    'confidence': 0.8
                })
            
            html += f"""
                                <div style="background: #f8f9fa; padding: 0.75rem 1rem; border-radius: 6px; border-left: 3px solid #dee2e6; transition: all 0.2s; position: relative;">
                                    <div style="display: flex; justify-content: space-between; align-items: start;">
                                        <div style="flex: 1;">
                                            <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.25rem; cursor: pointer;" onclick="toggleMeNotes(this)">
                                                {icon} {name} <span style="font-size: 0.8rem; color: var(--secondary); margin-left: 0.5rem;">📋 View Profile</span>
                                            </div>
                                            <div style="font-size: 0.85rem; color: #6c757d; line-height: 1.5;">
                                                {role}
                                            </div>
                                            
                                            <!-- Me Notes Profile (Hidden by default) -->
                                            <div class="me-notes-profile" style="display: none; margin-top: 1rem; padding: 1rem; background: white; border-radius: 6px; border: 2px solid var(--secondary); box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                                                <div style="font-weight: 600; color: var(--secondary); margin-bottom: 0.75rem; font-size: 1rem;">
                                                    📋 Professional Profile - Me Notes
                                                </div>
"""
            
            for note in me_notes:
                confidence_color = '#28a745' if note['confidence'] >= 0.9 else '#ffc107' if note['confidence'] >= 0.8 else '#6c757d'
                confidence_pct = int(note['confidence'] * 100)
                
                html += f"""
                                                <div style="margin-bottom: 0.75rem; padding: 0.75rem; background: #f8f9fa; border-radius: 4px; border-left: 3px solid {confidence_color};">
                                                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.25rem;">
                                                        <div style="font-weight: 600; font-size: 0.85rem; color: var(--primary);">
                                                            {note['icon']} {note['category'].replace('_', ' ').title()}
                                                        </div>
                                                        <div style="font-size: 0.75rem; padding: 0.15rem 0.5rem; background: {confidence_color}; color: white; border-radius: 10px;">
                                                            {confidence_pct}%
                                                        </div>
                                                    </div>
                                                    <div style="font-weight: 500; font-size: 0.85rem; color: #495057; margin-bottom: 0.25rem;">
                                                        {note['title']}
                                                    </div>
"""
                
                if 'note' in note:
                    html += f"""
                                                    <div style="font-size: 0.8rem; color: #6c757d; line-height: 1.5;">
                                                        {note['note']}
                                                    </div>
"""
                
                html += """
                                                </div>
"""
            
            html += """
                                                <div style="margin-top: 0.75rem; padding: 0.5rem; background: #e7f3ff; border-radius: 4px; font-size: 0.75rem; color: #6c757d; text-align: center;">
                                                    💡 Profile generated from workback planning scenario analysis
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
"""
        
        html += """                            </div>
                        </div>
                    </div>
                </details>
"""
    
    html += """            </div>
        </section>
        
        <!-- Deliverables Overview -->
        <section id="deliverables-section" class="dashboard">
            <h2>📦 Deliverables Overview</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                Across all scenarios, the system identified <strong>{}</strong> deliverables that need to be produced before meetings. 
                Deliverables range from simple artifacts (agenda, slide deck) to complex outputs (data analysis, prototype demos, legal 
                documentation). Each deliverable is linked to specific tasks, has responsible owners, and includes completion criteria. 
                Quality differentiation is evident: low-quality plans list generic deliverables, while high-quality plans specify detailed 
                formats, review cycles, and quality gates.
            </p>
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Completeness (C):</strong> Tests coverage of all required meeting artifacts and outputs</li>
                    <li><strong>Usefulness (U):</strong> Validates deliverables are actionable with clear specifications</li>
                    <li><strong>Relevance (R):</strong> Ensures deliverables align with meeting objectives and type</li>
                    <li><strong>Exceptional (E):</strong> High-quality plans include quality criteria and review processes</li>
                </ul>
            </div>
        </section>
        
        <!-- Model Information -->
        <section id="model-section" class="dashboard">
            <h2>🤖 Model Information</h2>
            <p style="margin-bottom: 1.5rem; color: #495057; line-height: 1.6;">
                All 99 workback plans in this test suite were generated using <strong>gpt-oss:120b</strong>, a 120-billion parameter 
                open-source language model running on remote Ollama (192.168.2.204:11434). The generation uses a sophisticated two-stage 
                pipeline: (1) Analysis stage with reasoning to understand context and requirements, and (2) Structuring stage to convert 
                analysis into structured JSON format. Total generation time was approximately 8 minutes per plan (5 min analysis + 3 min 
                structuring), resulting in ~12 hours for the complete test suite.
            </p>
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--secondary);">
                <h4 style="margin-top: 0; color: var(--primary);">Two-Stage Generation Pipeline:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Stage 1 - Analysis:</strong> LLM analyzes meeting context, identifies stakeholders, determines timeline, and plans task structure (Temperature: 0.7)</li>
                    <li><strong>Stage 2 - Structuring:</strong> LLM converts analysis into structured JSON with tasks, dependencies, deliverables, and milestones (Temperature: 0.1)</li>
                    <li><strong>Quality Instructions:</strong> Each quality level receives specific guidance (low: minimal tasks, medium: adequate coverage, high: comprehensive with risk management)</li>
                </ul>
            </div>
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--info); margin-top: 1rem;">
                <h4 style="margin-top: 0; color: var(--primary);">Purpose in ACRUE Evaluation:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Baseline Establishment:</strong> gpt-oss:120b serves as baseline for comparing other models (GPT-4, Claude Opus, etc.)</li>
                    <li><strong>Open Source Validation:</strong> Demonstrates that open-source models can generate quality workback plans</li>
                    <li><strong>Framework Testing:</strong> Provides consistent generation approach for evaluating ACRUE framework reliability</li>
                    <li><strong>Production Feasibility:</strong> Tests whether local/self-hosted models can meet enterprise requirements</li>
                </ul>
            </div>
        </section>
""".format(
        total_companies,
        total_scenarios,
        total_plans,
        total_meeting_types,
        total_tasks,
        total_stakeholders,
        total_deliverables
    )
    
    for company_name in sorted(companies.keys()):
        company_id = company_name.replace(' ', '-').replace(',', '').replace('.', '').lower()
        company_data = companies[company_name]
        scenario_count = len(company_data['scenarios'])
        html += f'                <li class="toc-item"><a href="#{company_id}" class="toc-link">{company_name}</a><span class="toc-count">({scenario_count} scenarios, {company_data["total_plans"]} plans)</span></li>\n'
    
    html += """            </ul>
        </section>
"""
    
    # Company Sections
    for company_name in sorted(companies.keys()):
        company_id = company_name.replace(' ', '-').replace(',', '').replace('.', '').lower()
        company_data = companies[company_name]
        scenarios = company_data['scenarios']
        
        html += f"""
        <!-- Company: {company_name} -->
        <section id="{company_id}" class="company-card">
            <div class="company-header">
                <div class="company-name">{company_name}</div>
                <div class="company-stats">
                    <span class="stat-badge"><strong>{len(scenarios)}</strong> Scenarios</span>
                    <span class="stat-badge"><strong>{company_data['total_plans']}</strong> Plans</span>
                    <span class="stat-badge"><strong>{company_data['total_stakeholders']}</strong> Stakeholders</span>
                    <span class="stat-badge"><strong>{company_data['total_deliverables']}</strong> Deliverables</span>
                </div>
            </div>
            
            <div class="scenario-grid">
"""
        
        for scenario in scenarios:
            meeting_type = scenario.get('meeting_type', 'Unknown')
            meeting_type_key = scenario.get('meeting_type_key', '')
            meeting_info = MEETING_TYPES.get(meeting_type_key, {})
            icon = meeting_info.get('icon', '📋')
            horizon = scenario.get('horizon', 'N/A')
            
            html += f"""
                <div class="scenario-item">
                    <div class="scenario-header">
                        <div class="scenario-title">{icon} {scenario.get('scenario_name', 'Unnamed Scenario')}</div>
                        <div class="meeting-badge">{meeting_type} | {horizon}</div>
                    </div>
                    
                    <div class="scenario-info">
                        <div class="info-row">
                            <span class="info-label">📅 Event:</span>
                            <span>{scenario.get('meeting_event_details', 'N/A')[:150]}...</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">🎯 Complexity:</span>
                            <span>{scenario.get('complexity', 'N/A')}</span>
                        </div>
                    </div>
                    
                    <details>
                        <summary>🏢 Company Context</summary>
                        <div class="detail-content">
                            {scenario.get('company_context', 'N/A')}
                        </div>
                    </details>
                    
                    <details>
                        <summary>👥 Stakeholders ({len(scenario.get('stakeholders', []))})</summary>
                        <div class="detail-content">
                            <ul>
"""
            
            for stakeholder in scenario.get('stakeholders', []):
                html += f"                                <li>{stakeholder}</li>\n"
            
            html += """                            </ul>
                        </div>
                    </details>
                    
                    <details>
                        <summary>📦 Deliverables ({}))</summary>
                        <div class="detail-content">
                            <ul>
""".format(len(scenario.get('deliverables', [])))
            
            for deliverable in scenario.get('deliverables', []):
                html += f"                                <li>{deliverable}</li>\n"
            
            html += """                            </ul>
                        </div>
                    </details>
                    
                    <div class="plans-container">
                        <div class="plans-header">📊 Workback Plans (3 Quality Levels)</div>
                        <div class="plans-grid">
"""
            
            # Generate plan cards
            for quality in ['low', 'medium', 'high']:
                plan = scenario.get('plans', {}).get(quality)
                
                if plan:
                    plan_data = plan.get('plan', {})
                    tasks = plan_data.get('tasks', [])
                    milestones = plan_data.get('milestones', [])
                    deliverables = plan_data.get('deliverables', [])
                    participants = plan_data.get('participants', [])
                    
                    html += f"""
                            <div class="plan-card {quality}">
                                <div class="plan-header">
                                    <div class="plan-title">{quality.capitalize()}</div>
                                    <div class="quality-badge {quality}">
                                        {'50-65%' if quality == 'low' else '70-80%' if quality == 'medium' else '85-95%'}
                                    </div>
                                </div>
                                <div class="plan-metrics">
                                    <div class="mini-metric">
                                        <div class="mini-metric-label">Tasks</div>
                                        <div class="mini-metric-value">{len(tasks)}</div>
                                    </div>
                                    <div class="mini-metric">
                                        <div class="mini-metric-label">Milestones</div>
                                        <div class="mini-metric-value">{len(milestones)}</div>
                                    </div>
                                    <div class="mini-metric">
                                        <div class="mini-metric-label">Deliverables</div>
                                        <div class="mini-metric-value">{len(deliverables)}</div>
                                    </div>
                                    <div class="mini-metric">
                                        <div class="mini-metric-label">People</div>
                                        <div class="mini-metric-value">{len(participants)}</div>
                                    </div>
                                </div>
"""
                    
                    if tasks:
                        html += f"""
                                <details style="margin-top: 0.8rem;">
                                    <summary style="font-size: 0.9rem;">📋 View Tasks ({len(tasks)})</summary>
                                    <div class="detail-content" style="max-height: 300px; overflow-y: auto;">
                                        <ul style="font-size: 0.85rem;">
"""
                        for task in tasks[:10]:  # Show first 10
                            html += f"                                            <li><strong>{task.get('id', 'N/A')}:</strong> {task.get('title', 'Untitled')}</li>\n"
                        
                        if len(tasks) > 10:
                            html += f"                                            <li style='color: #6c757d;'><em>... and {len(tasks) - 10} more tasks</em></li>\n"
                        
                        html += """                                        </ul>
                                    </div>
                                </details>
"""
                    
                    html += """                            </div>
"""
                else:
                    html += f"""
                            <div class="plan-card {quality}">
                                <div class="plan-header">
                                    <div class="plan-title">{quality.capitalize()}</div>
                                    <div class="quality-badge {quality}">
                                        {'50-65%' if quality == 'low' else '70-80%' if quality == 'medium' else '85-95%'}
                                    </div>
                                </div>
                                <div class="not-available">⏳ Plan not available</div>
                            </div>
"""
            
            html += """                        </div>
                    </div>
                </div>
"""
        
        html += """            </div>
        </section>
"""
    
    # Footer
    html += f"""
    </div>
    
    <footer>
        <p><strong>Workback Planning Test Suite</strong></p>
        <p>Generated with gpt-oss:120b on Ollama (192.168.2.204:11434)</p>
        <p>{total_scenarios} Scenarios × 3 Quality Levels = {total_plans} Workback Plans</p>
        <p style="margin-top: 1rem; opacity: 0.8;">© 2025 Scenara 2.0 | Meeting Intelligence System</p>
    </footer>
    
    <a href="#" class="back-to-top">↑</a>
</body>
</html>
"""
    
    return html


def main():
    """Generate dashboard and open in browser"""
    print("📊 Generating workback planning dashboard...")
    
    if not DATA_DIR.exists():
        print(f"❌ Data directory not found: {DATA_DIR}")
        return
    
    data = load_all_data()
    if not data:
        print("❌ No master index found")
        return
    
    print(f"✅ Loaded {len(data['companies'])} companies")
    print(f"✅ Loaded {data['master_index'].get('total_scenarios', 0)} scenarios")
    
    html_content = generate_dashboard_html(data)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated: {OUTPUT_FILE.absolute()}")
    print(f"📦 File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
    
    # Open in browser
    file_url = f"file://{OUTPUT_FILE.absolute()}"
    print(f"🌐 Opening in browser...")
    webbrowser.open(file_url)
    print("✅ Dashboard ready!")


if __name__ == "__main__":
    main()
