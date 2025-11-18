"""
Workback Plan Viewer - Interactive UI for exploring generated workback plans

This Streamlit application provides an interactive interface to:
- Browse scenarios by meeting type
- View workback plans (low/medium/high quality)
- Compare plans side-by-side
- Visualize timeline and dependencies
- Analyze ACRUE evaluation scores (when available)

Usage:
    streamlit run src/workback_planning/viewer/plan_viewer.py
"""

import json
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Workback Plan Viewer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
DATA_DIR = Path("data/workback_scenarios")
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
    "low": {"label": "Low Quality (50-65%)", "color": "#ff6b6b", "score_range": "50-65%"},
    "medium": {"label": "Medium Quality (70-80%)", "color": "#ffd93d", "score_range": "70-80%"},
    "high": {"label": "High Quality (85-95%)", "color": "#6bcf7f", "score_range": "85-95%"}
}


def load_master_index() -> Optional[Dict]:
    """Load the master index of all scenarios"""
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


def display_scenario_card(scenario: Dict):
    """Display scenario information in a nice card"""
    st.markdown(f"### 📋 {scenario['scenario_name']}")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Company Context:**")
        st.info(scenario['company_context'])
    
    with col2:
        st.markdown(f"**Meeting Type:**")
        st.write(scenario['meeting_type'])
        st.markdown(f"**Horizon:** {scenario['horizon']}")
        st.markdown(f"**Complexity:** {scenario['complexity']}")
    
    with col3:
        st.markdown(f"**Generated:**")
        gen_time = datetime.fromisoformat(scenario['generated_at'])
        st.write(gen_time.strftime("%Y-%m-%d %H:%M"))
    
    # Details in expander
    with st.expander("📅 Meeting Details"):
        st.write(scenario['meeting_event_details'])
    
    with st.expander("👥 Stakeholders"):
        for stakeholder in scenario.get('stakeholders', []):
            st.markdown(f"- {stakeholder}")
    
    with st.expander("📦 Deliverables"):
        for deliverable in scenario.get('deliverables', []):
            st.markdown(f"- {deliverable}")
    
    with st.expander("🎯 Success Criteria"):
        for criterion in scenario.get('success_criteria', []):
            st.markdown(f"- {criterion}")
    
    with st.expander("⚠️ Constraints"):
        for constraint in scenario.get('constraints', []):
            st.markdown(f"- {constraint}")


def display_plan_summary(plan: Dict, quality: str):
    """Display plan summary with key metrics"""
    quality_info = QUALITY_LEVELS[quality]
    
    # Header with quality indicator
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {quality_info['label']}")
    with col2:
        st.markdown(f"<div style='background-color: {quality_info['color']}; padding: 10px; border-radius: 5px; text-align: center;'><b>{quality_info['score_range']}</b></div>", unsafe_allow_html=True)
    
    # Extract plan details
    plan_data = plan.get('plan', {})
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    tasks = plan_data.get('tasks', [])
    milestones = plan_data.get('milestones', [])
    deliverables = plan_data.get('deliverables', [])
    participants = plan_data.get('participants', [])
    
    with col1:
        st.metric("Tasks", len(tasks))
    with col2:
        st.metric("Milestones", len(milestones))
    with col3:
        st.metric("Deliverables", len(deliverables))
    with col4:
        st.metric("Participants", len(participants))
    
    # Overview
    if plan_data.get('overview'):
        with st.expander("📝 Overview"):
            st.write(plan_data['overview'])


def display_task_list(tasks: List[Dict]):
    """Display tasks as a formatted table"""
    if not tasks:
        st.warning("No tasks defined in this plan")
        return
    
    # Convert tasks to DataFrame
    task_data = []
    for task in tasks:
        task_data.append({
            "ID": task.get('id', 'N/A'),
            "Title": task.get('title', 'N/A'),
            "Owner": task.get('owner', 'Unassigned'),
            "Start": task.get('start_date', 'N/A'),
            "Due": task.get('due_date', 'N/A'),
            "Status": task.get('status', 'Planned'),
            "Priority": task.get('priority', 'Medium')
        })
    
    df = pd.DataFrame(task_data)
    
    # Display with styling
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Task details in expander
    with st.expander("📋 Detailed Task Information"):
        for task in tasks:
            with st.container():
                st.markdown(f"**{task.get('id', 'N/A')}: {task.get('title', 'N/A')}**")
                st.write(f"*{task.get('description', 'No description')}*")
                
                if task.get('dependencies'):
                    st.write(f"**Dependencies:** {', '.join(task.get('dependencies', []))}")
                
                if task.get('deliverables'):
                    st.write(f"**Deliverables:** {', '.join(task.get('deliverables', []))}")
                
                st.divider()


def display_timeline_view(tasks: List[Dict]):
    """Display timeline visualization"""
    if not tasks:
        st.warning("No tasks to visualize")
        return
    
    st.markdown("### 📅 Timeline View")
    
    # Parse dates and create timeline data
    timeline_data = []
    for task in tasks:
        try:
            start = task.get('start_date', '')
            due = task.get('due_date', '')
            if start and due:
                timeline_data.append({
                    "Task": f"{task.get('id', '')} - {task.get('title', 'Untitled')[:30]}",
                    "Start": start,
                    "End": due,
                    "Owner": task.get('owner', 'Unassigned')
                })
        except:
            continue
    
    if timeline_data:
        df = pd.DataFrame(timeline_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No timeline data available (dates not properly formatted)")


def compare_plans(plans: Dict[str, Dict]):
    """Compare multiple plans side-by-side"""
    st.markdown("## 🔄 Plan Comparison")
    
    # Create comparison metrics
    comparison_data = []
    for quality, plan in plans.items():
        if plan:
            plan_data = plan.get('plan', {})
            comparison_data.append({
                "Quality": QUALITY_LEVELS[quality]['label'],
                "Tasks": len(plan_data.get('tasks', [])),
                "Milestones": len(plan_data.get('milestones', [])),
                "Deliverables": len(plan_data.get('deliverables', [])),
                "Participants": len(plan_data.get('participants', [])),
                "Has Overview": "✅" if plan_data.get('overview') else "❌",
                "Has Dependencies": "✅" if any(t.get('dependencies') for t in plan_data.get('tasks', [])) else "❌"
            })
    
    if comparison_data:
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)


# Main Application
def main():
    st.title("📋 Workback Plan Viewer")
    st.markdown("Interactive viewer for generated workback plans and scenarios")
    
    # Check if data directory exists
    if not DATA_DIR.exists():
        st.error(f"Data directory not found: {DATA_DIR}")
        st.info("Run the scenario generator first to create workback plans.")
        return
    
    # Load master index
    master_index = load_master_index()
    
    if not master_index:
        st.warning("No master index found. Generate scenarios first.")
        return
    
    # Sidebar - Meeting Type Selection
    st.sidebar.header("🔍 Filter Options")
    
    # Get available types from summary_by_type
    summary = master_index.get('summary_by_type', {})
    available_types = list(summary.keys())
    
    if not available_types:
        st.warning("No scenarios generated yet.")
        return
    
    selected_type = st.sidebar.selectbox(
        "Meeting Type",
        available_types,
        format_func=lambda x: MEETING_TYPES.get(x, {}).get('name', x)
    )
    
    # Get scenarios for selected type
    type_data = summary.get(selected_type, {})
    scenario_count = type_data.get('scenarios', 0)
    
    if scenario_count == 0:
        st.warning(f"No scenarios generated for {MEETING_TYPES.get(selected_type, {}).get('name', selected_type)}")
        return
    
    # Scenario selection
    scenario_num = st.sidebar.selectbox(
        "Scenario",
        range(1, scenario_count + 1),
        format_func=lambda x: f"Scenario {x}"
    )
    
    # Quality filter for plan view
    view_mode = st.sidebar.radio(
        "View Mode",
        ["Scenario Only", "Single Plan", "Compare All"]
    )
    
    if view_mode == "Single Plan":
        selected_quality = st.sidebar.selectbox(
            "Quality Level",
            ["low", "medium", "high"],
            format_func=lambda x: QUALITY_LEVELS[x]['label']
        )
    
    # Main content area
    st.divider()
    
    # Load and display scenario
    scenario = load_scenario(selected_type, scenario_num)
    
    if not scenario:
        st.error(f"Scenario not found: {selected_type}_scenario_{scenario_num}.json")
        return
    
    display_scenario_card(scenario)
    
    st.divider()
    
    # Display plans based on view mode
    if view_mode == "Scenario Only":
        st.info("💡 Select 'Single Plan' or 'Compare All' to view workback plans")
    
    elif view_mode == "Single Plan":
        plan = load_plan(selected_type, scenario_num, selected_quality)
        
        if not plan:
            st.warning(f"Plan not found: {selected_type}_scenario_{scenario_num}_{selected_quality}.json")
            st.info("The plan may still be generating. Check back in a few minutes.")
        else:
            display_plan_summary(plan, selected_quality)
            
            st.divider()
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📋 Tasks", "📅 Timeline", "📊 Details"])
            
            with tab1:
                tasks = plan.get('plan', {}).get('tasks', [])
                display_task_list(tasks)
            
            with tab2:
                tasks = plan.get('plan', {}).get('tasks', [])
                display_timeline_view(tasks)
            
            with tab3:
                st.json(plan.get('plan', {}))
    
    elif view_mode == "Compare All":
        plans = {
            'low': load_plan(selected_type, scenario_num, 'low'),
            'medium': load_plan(selected_type, scenario_num, 'medium'),
            'high': load_plan(selected_type, scenario_num, 'high')
        }
        
        # Filter out None plans
        plans = {k: v for k, v in plans.items() if v is not None}
        
        if not plans:
            st.warning("No plans found for this scenario yet. They may still be generating.")
        else:
            compare_plans(plans)
            
            # Show each plan in columns
            cols = st.columns(len(plans))
            
            for col, (quality, plan) in zip(cols, plans.items()):
                with col:
                    display_plan_summary(plan, quality)
                    
                    with st.expander("View Tasks"):
                        tasks = plan.get('plan', {}).get('tasks', [])
                        st.write(f"**{len(tasks)} tasks**")
                        for task in tasks[:5]:  # Show first 5
                            st.markdown(f"- {task.get('title', 'Untitled')}")
                        if len(tasks) > 5:
                            st.markdown(f"*... and {len(tasks) - 5} more*")
    
    # Footer with generation info
    st.divider()
    st.markdown(f"**Generation Info:** {master_index.get('total_scenarios', 0)} scenarios, {master_index.get('total_plans', 0)} plans")
    st.markdown(f"**Generated:** {master_index.get('generated_at', 'Unknown')}")


if __name__ == "__main__":
    main()
