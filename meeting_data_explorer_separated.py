#!/usr/bin/env python3
"""
Enhanced Meeting Data Explorer with Separated Track Support
Supports viewing real vs synthetic data separately or combined
"""

import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="Meeting PromptCoT Data Explorer - Separated Tracks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SeparatedDataExplorer:
    def __init__(self):
        self.data_dir = "meeting_prep_data"
        self.real_data_file = f"{self.data_dir}/training_scenarios_real.json"
        self.synthetic_data_file = f"{self.data_dir}/training_scenarios_synthetic.json"
        self.combined_data_file = f"{self.data_dir}/training_scenarios_combined.json"
        self.analysis_file = f"{self.data_dir}/training_analysis_separated.json"
        
        # Legacy file for backward compatibility
        self.legacy_file = f"{self.data_dir}/training_scenarios.json"
        
    def load_data(self) -> Dict[str, Any]:
        """Load all available data files"""
        data = {
            'real': [],
            'synthetic': [],
            'combined': [],
            'analysis': {},
            'files_exist': {}
        }
        
        # Check file existence
        files_to_check = {
            'real': self.real_data_file,
            'synthetic': self.synthetic_data_file,
            'combined': self.combined_data_file,
            'legacy': self.legacy_file,
            'analysis': self.analysis_file
        }
        
        for key, file_path in files_to_check.items():
            data['files_exist'][key] = os.path.exists(file_path)
        
        # Load real data
        if data['files_exist']['real']:
            try:
                with open(self.real_data_file, 'r', encoding='utf-8') as f:
                    data['real'] = json.load(f)
            except Exception as e:
                st.error(f"Error loading real data: {e}")
        
        # Load synthetic data
        if data['files_exist']['synthetic']:
            try:
                with open(self.synthetic_data_file, 'r', encoding='utf-8') as f:
                    data['synthetic'] = json.load(f)
            except Exception as e:
                st.error(f"Error loading synthetic data: {e}")
        
        # Load combined data
        if data['files_exist']['combined']:
            try:
                with open(self.combined_data_file, 'r', encoding='utf-8') as f:
                    data['combined'] = json.load(f)
            except Exception as e:
                st.error(f"Error loading combined data: {e}")
        elif data['files_exist']['legacy']:
            # Fallback to legacy file
            try:
                with open(self.legacy_file, 'r', encoding='utf-8') as f:
                    data['combined'] = json.load(f)
            except Exception as e:
                st.error(f"Error loading legacy data: {e}")
        
        # Load analysis
        if data['files_exist']['analysis']:
            try:
                with open(self.analysis_file, 'r', encoding='utf-8') as f:
                    data['analysis'] = json.load(f)
            except Exception as e:
                st.error(f"Error loading analysis: {e}")
        
        return data
    
    def display_separation_overview(self, data: Dict[str, Any]):
        """Display overview of data separation"""
        st.header("📊 Data Separation Overview")
        
        if data['analysis'].get('separation_summary'):
            sep = data['analysis']['separation_summary']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🔴 Real Data",
                    f"{sep['real_data_count']} scenarios",
                    f"{sep['real_percentage']:.1f}%"
                )
            
            with col2:
                st.metric(
                    "🔵 Synthetic Data", 
                    f"{sep['synthetic_data_count']} scenarios",
                    f"{sep['synthetic_percentage']:.1f}%"
                )
            
            with col3:
                st.metric(
                    "📦 Total Data",
                    f"{sep['total_count']} scenarios",
                    "100%"
                )
            
            # Pie chart of data distribution
            fig = px.pie(
                values=[sep['real_data_count'], sep['synthetic_data_count']],
                names=['Real Data', 'Synthetic Data'],
                title="Data Type Distribution",
                color_discrete_map={
                    'Real Data': '#ff6b6b',
                    'Synthetic Data': '#4ecdc4'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No separation analysis available. Run update_training_data_separated.py to generate separated data.")
    
    def display_data_track_analysis(self, data: Dict[str, Any], track: str):
        """Display analysis for a specific data track"""
        if track not in ['real', 'synthetic']:
            return
            
        track_data = data[track]
        analysis_key = f"{track}_data_analysis"
        
        if not track_data:
            st.warning(f"No {track} data available.")
            return
            
        st.header(f"{'🔴' if track == 'real' else '🔵'} {track.title()} Data Analysis")
        
        # Basic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Scenarios", len(track_data))
        
        # Calculate metrics from data
        quality_scores = [s.get('quality_score', 7.0) for s in track_data]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        high_quality = sum(1 for score in quality_scores if score >= 8.0)
        
        with col2:
            st.metric("Average Quality", f"{avg_quality:.2f}/10.0")
        
        with col3:
            st.metric("High Quality (8.0+)", high_quality)
        
        with col4:
            sources = set(s.get('source', 'unknown') for s in track_data)
            st.metric("Data Sources", len(sources))
        
        # Source distribution
        source_counts = {}
        for scenario in track_data:
            source = scenario.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        if source_counts:
            fig = px.bar(
                x=list(source_counts.keys()),
                y=list(source_counts.values()),
                title=f"{track.title()} Data Sources Distribution",
                labels={'x': 'Source', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Meeting type distribution
        meeting_types = {}
        for scenario in track_data:
            meeting_type = scenario.get('meeting_type', 'Unknown')
            meeting_types[meeting_type] = meeting_types.get(meeting_type, 0) + 1
        
        if meeting_types:
            # Show top 10 meeting types
            sorted_types = sorted(meeting_types.items(), key=lambda x: x[1], reverse=True)[:10]
            
            fig = px.bar(
                x=[item[1] for item in sorted_types],
                y=[item[0] for item in sorted_types],
                orientation='h',
                title=f"Top 10 Meeting Types - {track.title()} Data",
                labels={'x': 'Count', 'y': 'Meeting Type'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Quality score distribution
        if quality_scores:
            fig = px.histogram(
                x=quality_scores,
                nbins=20,
                title=f"Quality Score Distribution - {track.title()} Data",
                labels={'x': 'Quality Score', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Data provenance (if available)
        st.subheader("Data Provenance")
        
        collection_methods = {}
        validation_levels = {}
        
        for scenario in track_data:
            prov = scenario.get('data_provenance', {})
            
            method = prov.get('collection_method', 'unknown')
            collection_methods[method] = collection_methods.get(method, 0) + 1
            
            validation = prov.get('validation_level', 'unknown')
            validation_levels[validation] = validation_levels.get(validation, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            if collection_methods:
                st.write("**Collection Methods:**")
                for method, count in sorted(collection_methods.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"- {method}: {count}")
        
        with col2:
            if validation_levels:
                st.write("**Validation Levels:**")
                for level, count in sorted(validation_levels.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"- {level}: {count}")
    
    def display_comparison_view(self, data: Dict[str, Any]):
        """Display side-by-side comparison of real vs synthetic data"""
        st.header("⚖️ Real vs Synthetic Data Comparison")
        
        if not data['real'] or not data['synthetic']:
            st.warning("Both real and synthetic data needed for comparison.")
            return
        
        # Quality comparison
        real_quality = [s.get('quality_score', 7.0) for s in data['real']]
        synthetic_quality = [s.get('quality_score', 7.0) for s in data['synthetic']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "🔴 Real Data Avg Quality",
                f"{sum(real_quality)/len(real_quality):.2f}/10.0"
            )
        
        with col2:
            st.metric(
                "🔵 Synthetic Data Avg Quality",
                f"{sum(synthetic_quality)/len(synthetic_quality):.2f}/10.0"
            )
        
        # Quality distribution comparison
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=real_quality,
            name='Real Data',
            marker_color='#ff6b6b',
            opacity=0.7,
            nbinsx=20
        ))
        
        fig.add_trace(go.Histogram(
            x=synthetic_quality,
            name='Synthetic Data',
            marker_color='#4ecdc4',
            opacity=0.7,
            nbinsx=20
        ))
        
        fig.update_layout(
            title="Quality Score Distribution Comparison",
            xaxis_title="Quality Score",
            yaxis_title="Count",
            barmode='overlay'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Meeting type coverage comparison
        real_types = set(s.get('meeting_type', 'Unknown') for s in data['real'])
        synthetic_types = set(s.get('meeting_type', 'Unknown') for s in data['synthetic'])
        
        st.subheader("Meeting Type Coverage")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Real Data Types", len(real_types))
        
        with col2:
            st.metric("Synthetic Data Types", len(synthetic_types))
        
        with col3:
            overlap = len(real_types.intersection(synthetic_types))
            st.metric("Overlapping Types", overlap)
        
        # Show unique types
        unique_real = real_types - synthetic_types
        unique_synthetic = synthetic_types - real_types
        
        if unique_real or unique_synthetic:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Unique to Real Data:**")
                for meeting_type in sorted(unique_real):
                    st.write(f"- {meeting_type}")
            
            with col2:
                st.write("**Unique to Synthetic Data:**")
                for meeting_type in sorted(unique_synthetic):
                    st.write(f"- {meeting_type}")
    
    def display_scenario_browser(self, data: Dict[str, Any], data_type: str):
        """Display scenario browser for specific data type"""
        if data_type not in data or not data[data_type]:
            st.warning(f"No {data_type} data available.")
            return
        
        scenarios = data[data_type]
        
        st.header(f"🔍 {data_type.title()} Scenario Browser")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sources = sorted(set(s.get('source', 'unknown') for s in scenarios))
            selected_source = st.selectbox("Filter by Source", ['All'] + sources)
        
        with col2:
            meeting_types = sorted(set(s.get('meeting_type', 'Unknown') for s in scenarios))
            selected_type = st.selectbox("Filter by Meeting Type", ['All'] + meeting_types)
        
        with col3:
            complexities = sorted(set(s.get('complexity', 'medium') for s in scenarios))
            selected_complexity = st.selectbox("Filter by Complexity", ['All'] + complexities)
        
        # Apply filters
        filtered_scenarios = scenarios
        
        if selected_source != 'All':
            filtered_scenarios = [s for s in filtered_scenarios if s.get('source') == selected_source]
        
        if selected_type != 'All':
            filtered_scenarios = [s for s in filtered_scenarios if s.get('meeting_type') == selected_type]
        
        if selected_complexity != 'All':
            filtered_scenarios = [s for s in filtered_scenarios if s.get('complexity') == selected_complexity]
        
        st.write(f"Showing {len(filtered_scenarios)} of {len(scenarios)} scenarios")
        
        # Display scenarios
        for i, scenario in enumerate(filtered_scenarios[:10]):  # Limit to first 10
            with st.expander(f"Scenario {i+1}: {scenario.get('context', {}).get('subject', 'No Subject')[:50]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Basic Info:**")
                    st.write(f"- **Source:** {scenario.get('source', 'Unknown')}")
                    st.write(f"- **Meeting Type:** {scenario.get('meeting_type', 'Unknown')}")
                    st.write(f"- **Complexity:** {scenario.get('complexity', 'Unknown')}")
                    st.write(f"- **Quality Score:** {scenario.get('quality_score', 'N/A')}/10.0")
                    
                    if scenario.get('data_provenance'):
                        prov = scenario['data_provenance']
                        st.write(f"- **Is Real Data:** {prov.get('is_real_data', 'Unknown')}")
                        st.write(f"- **Collection Method:** {prov.get('collection_method', 'Unknown')}")
                        st.write(f"- **Validation Level:** {prov.get('validation_level', 'Unknown')}")
                
                with col2:
                    st.write("**Context:**")
                    context = scenario.get('context', {})
                    st.write(f"- **Subject:** {context.get('subject', 'N/A')}")
                    st.write(f"- **Attendees:** {context.get('attendee_count', 'N/A')}")
                    st.write(f"- **Duration:** {context.get('duration_minutes', 'N/A')} minutes")
                    st.write(f"- **Online Meeting:** {context.get('is_online_meeting', 'N/A')}")
                
                # Show preparation requirements
                prep_reqs = scenario.get('preparation_requirements', [])
                if prep_reqs:
                    st.write("**Preparation Requirements:**")
                    for req in prep_reqs[:3]:  # Show first 3
                        st.write(f"- {req}")
                
                # Show ACRUE scores if available
                if scenario.get('acrue_scores'):
                    st.write("**ACRUE Scores:**")
                    acrue = scenario['acrue_scores']
                    for dimension, score in acrue.items():
                        if isinstance(score, (int, float)):
                            st.write(f"- **{dimension.title()}:** {score:.2f}/10.0")

def main():
    """Main Streamlit application"""
    explorer = SeparatedDataExplorer()
    
    # App header
    st.title("📊 Meeting PromptCoT Data Explorer")
    st.subheader("Separated Real vs Synthetic Data Tracks")
    
    # Load data
    with st.spinner("Loading data..."):
        data = explorer.load_data()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    pages = {
        "📊 Overview": "overview",
        "🔴 Real Data": "real",
        "🔵 Synthetic Data": "synthetic", 
        "⚖️ Comparison": "comparison",
        "🔍 Real Browser": "real_browser",
        "🔍 Synthetic Browser": "synthetic_browser",
        "📦 Combined View": "combined"
    }
    
    selected_page = st.sidebar.selectbox("Select View", list(pages.keys()))
    page_key = pages[selected_page]
    
    # Display file status in sidebar
    st.sidebar.subheader("📁 File Status")
    
    status_icons = {True: "✅", False: "❌"}
    file_labels = {
        'real': "Real Data",
        'synthetic': "Synthetic Data", 
        'combined': "Combined Data",
        'analysis': "Analysis"
    }
    
    for key, label in file_labels.items():
        exists = data['files_exist'].get(key, False)
        st.sidebar.write(f"{status_icons[exists]} {label}")
    
    # Display selected page
    if page_key == "overview":
        explorer.display_separation_overview(data)
    elif page_key == "real":
        explorer.display_data_track_analysis(data, "real")
    elif page_key == "synthetic":
        explorer.display_data_track_analysis(data, "synthetic")
    elif page_key == "comparison":
        explorer.display_comparison_view(data)
    elif page_key == "real_browser":
        explorer.display_scenario_browser(data, "real")
    elif page_key == "synthetic_browser":
        explorer.display_scenario_browser(data, "synthetic")
    elif page_key == "combined":
        # Legacy combined view
        if data['combined']:
            st.header("📦 Combined Data View (Legacy)")
            st.write(f"Total scenarios: {len(data['combined'])}")
            
            # Simple statistics
            sources = {}
            for scenario in data['combined']:
                source = scenario.get('source', 'unknown')
                sources[source] = sources.get(source, 0) + 1
            
            st.subheader("Source Distribution")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {source}: {count}")
        else:
            st.warning("No combined data available.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Data Separation Benefits:**")
    st.sidebar.markdown("• Maintains data integrity")
    st.sidebar.markdown("• Enables targeted analysis")
    st.sidebar.markdown("• Supports validation studies")
    st.sidebar.markdown("• Facilitates model training")


if __name__ == "__main__":
    main()