#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meeting PromptCoT Data Explorer
Native UX interface for visualizing and exploring real MEvals meeting data
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import re
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Configure Streamlit page
st.set_page_config(
    page_title="Meeting PromptCoT Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .quality-excellent { color: #00C851; font-weight: bold; }
    .quality-high { color: #33B679; font-weight: bold; }
    .quality-good { color: #FF8800; font-weight: bold; }
    .quality-fair { color: #FF4444; font-weight: bold; }
    .scenario-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

class MeetingDataExplorer:
    """Main class for exploring meeting data"""
    
    def __init__(self):
        self.data = None
        self.df = None
        
    def load_data(self, file_path: str) -> bool:
        """Load meeting data from JSON or JSONL file"""
        try:
            scenarios = []
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.json'):
                    # Load JSON format
                    scenarios = json.load(f)
                else:
                    # Load JSONL format
                    for line in f:
                        if line.strip():
                            scenarios.append(json.loads(line))
            
            self.data = scenarios
            self.df = self._create_dataframe(scenarios)
            return True
            
        except FileNotFoundError:
            st.error(f"❌ Data file not found: {file_path}")
            return False
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            return False
    
    def _create_dataframe(self, scenarios: List[Dict]) -> pd.DataFrame:
        """Convert scenarios to pandas DataFrame for analysis"""
        rows = []
        
        for scenario in scenarios:
            # Handle different data formats
            context = scenario.get('context', {})
            
            # Check if this is ContextFlow enhanced data - now using correct field names
            source = scenario.get('source', '')
            is_contextflow = (source == 'microsoft_calendar_contextflow' or 
                            scenario.get('framework') == 'GUTT_v4.0_ACRUE' or
                            'enterprise_taxonomy' in scenario)
            
            # Extract basic information
            subject = context.get('subject', scenario.get('subject', ''))
            if not subject:
                # Try to extract from other fields
                subject = scenario.get('meeting_type', 'Unknown Meeting')
            
            # Extract quality scores
            quality_score = scenario.get('quality_score', 0)
            if is_contextflow:
                acrue_scores = scenario.get('acrue_scores', {})
                overall_quality = sum(acrue_scores.values()) / len(acrue_scores) if acrue_scores else quality_score
            else:
                overall_quality = quality_score
                acrue_scores = {}
            
            # Extract meeting classification
            if is_contextflow:
                taxonomy = scenario.get('enterprise_taxonomy', {})
                meeting_category = taxonomy.get('primary_category', 'Unknown')
                meeting_type = taxonomy.get('specific_type', 'Unknown')
                confidence = taxonomy.get('confidence', 0.0)
            else:
                meeting_category = scenario.get('meeting_type', 'Unknown')
                meeting_type = scenario.get('meeting_type', 'Unknown')
                confidence = 1.0
            
            # Extract attendee information
            attendees = context.get('attendees', [])
            attendee_count = context.get('attendee_count', len(attendees))
            
            # Extract other context
            duration = context.get('duration_minutes', 60)
            importance = context.get('importance', 'normal')
            is_online = context.get('is_online_meeting', False)
            complexity = scenario.get('complexity', 'medium')
            
            # Extract source information
            source = scenario.get('source', 'unknown')
            scenario_id = scenario.get('id', f"scenario_{len(rows)}")
            
            row = {
                'id': scenario_id,
                'source': source,
                'subject': subject,
                'meeting_category': meeting_category,
                'meeting_type': meeting_type,
                'quality_score': overall_quality,
                'classification_confidence': confidence,
                'attendee_count': attendee_count,
                'duration_minutes': duration,
                'importance': importance,
                'is_online': is_online,
                'complexity': complexity,
                'is_contextflow': is_contextflow,
                # ACRUE scores (if available)
                'acrue_accurate': acrue_scores.get('accurate', 0),
                'acrue_complete': acrue_scores.get('complete', 0),
                'acrue_relevant': acrue_scores.get('relevant', 0),
                'acrue_useful': acrue_scores.get('useful', 0),
                'acrue_exceptional': acrue_scores.get('exceptional', 0),
                'full_scenario': scenario
            }
            rows.append(row)
        
        return pd.DataFrame(rows)

def render_header():
    """Render the main header"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("📊 Meeting PromptCoT Data Explorer")
        st.markdown("**Visualizing Real Microsoft Meeting Data from MEvals**")

def render_data_overview(explorer: MeetingDataExplorer):
    """Render data overview section"""
    if explorer.df is None:
        return
    
    st.header("📈 Data Overview")
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Scenarios", len(explorer.df))
    
    with col2:
        avg_quality = explorer.df['quality_score'].mean()
        st.metric("Avg Quality Score", f"{avg_quality:.2f}/10.0")
    
    with col3:
        excellent_count = len(explorer.df[explorer.df['quality_score'] >= 8.0])
        st.metric("High Quality (8.0+)", f"{excellent_count} ({excellent_count/len(explorer.df)*100:.1f}%)")
    
    with col4:
        contextflow_count = len(explorer.df[explorer.df['is_contextflow'] == True])
        st.metric("ContextFlow Enhanced", f"{contextflow_count} ({contextflow_count/len(explorer.df)*100:.1f}%)")
    
    with col5:
        unique_sources = explorer.df['source'].nunique()
        st.metric("Data Sources", unique_sources)
    
    with col5:
        unique_types = explorer.df['meeting_type'].nunique()
        st.metric("Meeting Types", unique_types)

def render_quality_analysis(explorer: MeetingDataExplorer):
    """Render quality analysis section"""
    if explorer.df is None:
        return
    
    st.header("🎯 Quality Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quality score distribution
        fig = px.histogram(
            explorer.df, 
            x='quality_score', 
            nbins=20,
            title="Quality Score Distribution",
            labels={'quality_score': 'Quality Score', 'count': 'Number of Scenarios'}
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quality categories pie chart
        quality_categories = []
        for score in explorer.df['quality_score']:
            if score >= 0.95:
                quality_categories.append('Excellent (≥95%)')
            elif score >= 0.90:
                quality_categories.append('High (90-95%)')
            elif score >= 0.80:
                quality_categories.append('Good (80-90%)')
            else:
                quality_categories.append('Fair (<80%)')
        
        quality_df = pd.DataFrame({'category': quality_categories})
        quality_counts = quality_df['category'].value_counts()
        
        fig = px.pie(
            values=quality_counts.values,
            names=quality_counts.index,
            title="Quality Distribution by Category",
            color_discrete_map={
                'Excellent (≥95%)': '#00C851',
                'High (90-95%)': '#33B679', 
                'Good (80-90%)': '#FF8800',
                'Fair (<80%)': '#FF4444'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

def render_meeting_analysis(explorer: MeetingDataExplorer):
    """Render meeting analysis section"""
    if explorer.df is None:
        return
    
    st.header("📅 Meeting Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Meeting types
        meeting_type_counts = explorer.df['meeting_type'].value_counts()
        fig = px.bar(
            x=meeting_type_counts.values,
            y=meeting_type_counts.index,
            orientation='h',
            title="Meeting Types Distribution",
            labels={'x': 'Count', 'y': 'Meeting Type'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Meeting categories (for ContextFlow data) or complexity
        if 'meeting_category' in explorer.df.columns:
            category_counts = explorer.df['meeting_category'].value_counts()
            fig = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                title="Meeting Categories Distribution",
                labels={'x': 'Count', 'y': 'Meeting Category'}
            )
        else:
            complexity_counts = explorer.df['complexity'].value_counts()
            fig = px.bar(
                x=complexity_counts.values,
                y=complexity_counts.index,
                orientation='h',
                title="Meeting Complexity Distribution",
                labels={'x': 'Count', 'y': 'Complexity Level'}
            )
        st.plotly_chart(fig, use_container_width=True)

def render_organizer_analysis(explorer: MeetingDataExplorer):
    """Render source/organizer analysis section"""
    if explorer.df is None:
        return
    
    st.header("� Data Source Analysis")
    
    # Top sources
    source_counts = explorer.df['source'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            x=source_counts.values,
            y=source_counts.index,
            orientation='h',
            title="Data Source Distribution",
            labels={'x': 'Number of Scenarios', 'y': 'Source'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Source quality analysis
        source_quality = explorer.df.groupby('source')['quality_score'].agg(['mean', 'count']).reset_index()
        
        fig = px.scatter(
            source_quality,
            x='count',
            y='mean',
            size='count',
            title="Source Quality vs Volume",
            labels={'count': 'Number of Scenarios', 'mean': 'Average Quality Score'},
            hover_data=['source']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional source analysis
    st.subheader("📈 Quality by Source")
    
    # Create quality comparison table
    quality_by_source = explorer.df.groupby('source').agg({
        'quality_score': ['mean', 'std', 'count'],
        'is_contextflow': 'sum'
    }).round(2)
    
    quality_by_source.columns = ['Avg Quality', 'Std Dev', 'Count', 'ContextFlow Enhanced']
    st.dataframe(quality_by_source, use_container_width=True)

def render_detailed_metrics(explorer: MeetingDataExplorer):
    """Render detailed metrics analysis"""
    if explorer.df is None:
        return
    
    st.header("📊 Detailed Metrics Analysis")
    
    # Check which columns are available
    available_cols = [col for col in explorer.df.columns if 'acrue_' in col or col in ['quality_score', 'duration_minutes', 'attendee_count']]
    
    if len(available_cols) < 2:
        st.warning("Not enough metrics available for correlation analysis.")
        return
    
    # Create correlation matrix for available metrics
    correlation_matrix = explorer.df[available_cols].corr()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation heatmap
        fig = px.imshow(
            correlation_matrix,
            title="Available Metrics Correlation",
            color_continuous_scale='RdYlBu_r',
            aspect='auto'
        )
        fig.update_layout(width=400, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ACRUE metrics box plot (if available)
        acrue_cols = [col for col in explorer.df.columns if 'acrue_' in col]
        if acrue_cols:
            metrics_data = []
            for col in acrue_cols:
                for value in explorer.df[col]:
                    if value > 0:  # Only include non-zero values
                        metrics_data.append({
                            'metric': col.replace('acrue_', '').title(), 
                            'value': value
                        })
            
            if metrics_data:
                metrics_df = pd.DataFrame(metrics_data)
                fig = px.box(
                    metrics_df,
                    x='metric',
                    y='value',
                    title="ACRUE Metrics Distribution"
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to basic metrics
            st.metric("Average Quality Score", f"{explorer.df['quality_score'].mean():.2f}")
            st.metric("Quality Standard Deviation", f"{explorer.df['quality_score'].std():.2f}")
            st.metric("Total Scenarios", len(explorer.df))

def render_scenario_explorer(explorer: MeetingDataExplorer):
    """Render individual scenario explorer"""
    if explorer.df is None:
        return
    
    st.header("🔍 Scenario Explorer")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_source = st.selectbox(
            "Filter by Source",
            ['All'] + sorted(explorer.df['source'].unique().tolist())
        )
    
    with col2:
        selected_type = st.selectbox(
            "Filter by Meeting Type",
            ['All'] + sorted(explorer.df['meeting_type'].unique().tolist())
        )
    
    with col3:
        quality_threshold = st.slider(
            "Minimum Quality Score",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.1
        )
    
    # Apply filters
    filtered_df = explorer.df.copy()
    
    if selected_source != 'All':
        filtered_df = filtered_df[filtered_df['source'] == selected_source]
    
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['meeting_type'] == selected_type]
    
    filtered_df = filtered_df[filtered_df['quality_score'] >= quality_threshold]
    
    st.write(f"**Found {len(filtered_df)} scenarios matching filters**")
    
    # Display scenarios
    if len(filtered_df) > 0:
        # Sort by quality score
        filtered_df = filtered_df.sort_values('quality_score', ascending=False)
        
        for idx, row in filtered_df.iterrows():
            render_scenario_card(row)
    else:
        st.info("No scenarios match the current filters.")

def render_scenario_card(row):
    """Render an individual scenario card"""
    quality_class = get_quality_class(row['quality_score'])
    
    with st.expander(f"📋 {row['subject']} - Quality: {row['quality_score']:.2f}/10.0"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Meeting Details:**")
            st.write(f"• Source: {row['source']}")
            st.write(f"• Type: {row['meeting_type']}")
            st.write(f"• Category: {row.get('meeting_category', 'N/A')}")
            st.write(f"• Complexity: {row['complexity']}")
            st.write(f"• Attendees: {row['attendee_count']}")
            st.write(f"• Duration: {row['duration_minutes']} minutes")
            
        with col2:
            st.write("**Quality Metrics:**")
            st.write(f"• Overall Score: {row['quality_score']:.2f}/10.0")
            if row['is_contextflow']:
                st.write("**ACRUE Scores:**")
                st.write(f"• Accurate: {row['acrue_accurate']:.2f}")
                st.write(f"• Complete: {row['acrue_complete']:.2f}")
                st.write(f"• Relevant: {row['acrue_relevant']:.2f}")
                st.write(f"• Useful: {row['acrue_useful']:.2f}")
                st.write(f"• Exceptional: {row['acrue_exceptional']:.2f}")
            
            st.write(f"• Classification Confidence: {row['classification_confidence']:.2f}")
        
        # Show full scenario data if requested
        if st.button(f"Show Full Data", key=f"show_{row['id']}"):
            st.json(row['full_scenario'])

def get_quality_class(score: float) -> str:
    """Get CSS class for quality score"""
    if score >= 9.0:
        return "quality-excellent"
    elif score >= 8.0:
        return "quality-high"
    elif score >= 7.0:
        return "quality-good"
    else:
        return "quality-fair"

def render_export_section(explorer: MeetingDataExplorer):
    """Render data export section"""
    if explorer.df is None:
        return
    
    st.header("💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export as CSV"):
            csv = explorer.df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"meeting_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Export Summary Report"):
            report = generate_summary_report(explorer.df)
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"meeting_data_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()

def generate_summary_report(df: pd.DataFrame) -> str:
    """Generate a summary report"""
    report = f"""# Meeting PromptCoT Data Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
- Total Scenarios: {len(df)}
- Average Quality Score: {df['quality_score'].mean():.3f}
- Quality Range: {df['quality_score'].min():.3f} - {df['quality_score'].max():.3f}

## Quality Distribution
- Excellent (≥95%): {len(df[df['quality_score'] >= 0.95])} ({len(df[df['quality_score'] >= 0.95])/len(df)*100:.1f}%)
- High (90-95%): {len(df[(df['quality_score'] >= 0.90) & (df['quality_score'] < 0.95)])} ({len(df[(df['quality_score'] >= 0.90) & (df['quality_score'] < 0.95)])/len(df)*100:.1f}%)
- Good (80-90%): {len(df[(df['quality_score'] >= 0.80) & (df['quality_score'] < 0.90)])} ({len(df[(df['quality_score'] >= 0.80) & (df['quality_score'] < 0.90)])/len(df)*100:.1f}%)
- Fair (<80%): {len(df[df['quality_score'] < 0.80])} ({len(df[df['quality_score'] < 0.80])/len(df)*100:.1f}%)

## Top Organizers
{chr(10).join([f"- {org}: {count} meetings" for org, count in df['organizer'].value_counts().head(10).items()])}

## Meeting Types
{chr(10).join([f"- {type_}: {count} meetings" for type_, count in df['meeting_type'].value_counts().items()])}

## Business Functions
{chr(10).join([f"- {func}: {count} meetings" for func, count in df['business_function'].value_counts().items()])}
"""
    return report

def render_contextflow_analysis(explorer: MeetingDataExplorer):
    """Render ContextFlow GUTT v4.0 ACRUE analysis"""
    if explorer.df is None:
        return
    
    st.header("🎯 ContextFlow GUTT v4.0 ACRUE Analysis")
    
    # Filter ContextFlow data
    cf_data = explorer.df[explorer.df['is_contextflow'] == True]
    
    if len(cf_data) == 0:
        st.warning("No ContextFlow enhanced scenarios found in the dataset.")
        return
    
    st.success(f"✅ Found {len(cf_data)} ContextFlow enhanced scenarios")
    
    # ACRUE Framework Analysis
    st.subheader("📊 ACRUE Quality Framework")
    
    acrue_cols = ['acrue_accurate', 'acrue_complete', 'acrue_relevant', 'acrue_useful', 'acrue_exceptional']
    acrue_data = cf_data[acrue_cols]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ACRUE scores bar chart
        acrue_means = acrue_data.mean()
        fig = px.bar(
            x=acrue_means.index, 
            y=acrue_means.values,
            title="ACRUE Framework Average Scores",
            labels={'x': 'ACRUE Dimension', 'y': 'Score (0-10)'},
            color=acrue_means.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ACRUE scores table
        st.write("**ACRUE Detailed Scores:**")
        for col in acrue_cols:
            if col in cf_data.columns:
                avg_score = cf_data[col].mean()
                dimension = col.replace('acrue_', '').title()
                st.metric(f"{dimension}", f"{avg_score:.2f}/10.0")
    
    # Enterprise Meeting Taxonomy
    st.subheader("🏢 Enterprise Meeting Taxonomy Distribution")
    
    if 'meeting_category' in cf_data.columns:
        category_dist = cf_data['meeting_category'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=category_dist.values,
                names=category_dist.index,
                title="Meeting Categories Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Category Breakdown:**")
            for category, count in category_dist.items():
                percentage = (count / len(cf_data)) * 100
                st.write(f"- **{category}**: {count} ({percentage:.1f}%)")

def render_source_analysis(explorer: MeetingDataExplorer):
    """Render data source analysis"""
    if explorer.df is None:
        return
    
    st.header("📊 Data Source Analysis")
    
    # Source distribution
    source_dist = explorer.df['source'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            values=source_dist.values,
            names=source_dist.index,
            title="Data Sources Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Source Quality Comparison:**")
        for source in source_dist.index:
            source_data = explorer.df[explorer.df['source'] == source]
            avg_quality = source_data['quality_score'].mean()
            count = len(source_data)
            st.metric(f"{source}", f"{avg_quality:.2f}/10.0", f"{count} scenarios")

def render_training_data_analysis(explorer: MeetingDataExplorer):
    """Render training data analysis"""
    if explorer.df is None:
        return
    
    st.header("📋 Training Data Analysis")
    
    # Quality distribution for training
    st.subheader("📈 Quality Distribution for Training")
    
    # Create quality bins
    bins = [0, 6, 7, 8, 9, 10]
    labels = ['Fair (0-6)', 'Good (6-7)', 'High (7-8)', 'Excellent (8-9)', 'Outstanding (9-10)']
    explorer.df['quality_bin'] = pd.cut(explorer.df['quality_score'], bins=bins, labels=labels, include_lowest=True)
    
    quality_dist = explorer.df['quality_bin'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            x=quality_dist.index,
            y=quality_dist.values,
            title="Training Data Quality Distribution",
            labels={'x': 'Quality Category', 'y': 'Number of Scenarios'},
            color=quality_dist.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Training Recommendations:**")
        high_quality_count = len(explorer.df[explorer.df['quality_score'] >= 8.0])
        total_count = len(explorer.df)
        
        st.metric("High Quality Data", f"{high_quality_count}/{total_count}", f"{(high_quality_count/total_count)*100:.1f}%")
        
        if high_quality_count > 150:
            st.success("✅ Excellent training dataset quality!")
        elif high_quality_count > 100:
            st.info("📊 Good training dataset quality")
        else:
            st.warning("⚠️ Consider filtering for higher quality scenarios")
    
    # Complexity analysis
    st.subheader("⚖️ Complexity Distribution")
    complexity_dist = explorer.df['complexity'].value_counts()
    
    fig = px.bar(
        x=complexity_dist.index,
        y=complexity_dist.values,
        title="Meeting Complexity Distribution",
        labels={'x': 'Complexity Level', 'y': 'Number of Scenarios'}
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main Streamlit application"""
    render_header()
    
    # Initialize explorer
    explorer = MeetingDataExplorer()
    
    # Sidebar for data loading
    with st.sidebar:
        st.header("📁 Data Source")
        
        # Check for available data files
        training_data_path = "meeting_prep_data/training_scenarios.json"
        contextflow_path = "meeting_prep_data/enhanced_contextflow_scenarios.json"
        real_calendar_path = "meeting_prep_data/real_calendar_scenarios.json"
        
        # Default to the most comprehensive dataset
        default_path = training_data_path if Path(training_data_path).exists() else "meeting_prep_real_data/mevals_training_data.jsonl"
        
        # Check if data files exist
        if Path(training_data_path).exists():
            st.success("✅ Enhanced training data found!")
            st.info(f"📊 ContextFlow + GUTT v4.0 integrated")
            if explorer.load_data(training_data_path):
                st.success(f"📈 Loaded enhanced dataset")
        elif Path(contextflow_path).exists():
            st.success("✅ ContextFlow data found!")
            default_path = contextflow_path
            if explorer.load_data(contextflow_path):
                st.success(f"📈 Loaded ContextFlow dataset")
        elif Path(real_calendar_path).exists():
            st.success("✅ Real calendar data found!")
            default_path = real_calendar_path
            if explorer.load_data(real_calendar_path):
                st.success(f"📈 Loaded real calendar dataset")
        elif Path(default_path).exists():
            st.success("✅ Real meeting data found!")
            if st.button("🔄 Load Data"):
                if explorer.load_data(default_path):
                    st.success("Data loaded successfully!")
                    st.rerun()
        else:
            st.warning("⚠️ No real meeting data found")
            st.info("Run this command to generate data:")
            st.code("python mevals_promptcot_bridge.py --mevals-data MEvals/data/meeting_prep.prompt.samples --output meeting_prep_real_data")
        
        # Manual file upload
        st.header("📤 Upload Data")
        uploaded_file = st.file_uploader("Choose JSONL file", type=['jsonl'])
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if explorer.load_data(temp_path):
                st.success("Uploaded data loaded!")
                # Clean up temp file
                Path(temp_path).unlink()
    
    # Auto-load default data if available
    if explorer.data is None and Path(default_path).exists():
        explorer.load_data(default_path)
    
    # Main content
    if explorer.data is not None:
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📈 Overview", 
            "🎯 ContextFlow", 
            "📊 Quality", 
            "📅 Meetings", 
            "👥 Sources", 
            "� Training Data", 
            "🔍 Explorer"
        ])
        
        with tab1:
            render_data_overview(explorer)
        
        with tab2:
            render_contextflow_analysis(explorer)
        
        with tab3:
            render_quality_analysis(explorer)
        
        with tab4:
            render_meeting_analysis(explorer)
        
        with tab5:
            render_source_analysis(explorer)
        
        with tab6:
            render_training_data_analysis(explorer)
        
        with tab7:
            render_scenario_explorer(explorer)
        
        # Export section at bottom
        render_export_section(explorer)
        
    else:
        st.info("👈 Please load meeting data using the sidebar to start exploring!")
        
        # Show sample data generation instructions
        st.header("🚀 Getting Started")
        st.markdown("""
        To use this explorer:
        
        1. **Generate real meeting data** (if not already done):
           ```bash
           python mevals_promptcot_bridge.py --mevals-data MEvals/data/meeting_prep.prompt.samples --output meeting_prep_real_data
           ```
        
        2. **Load the data** using the sidebar
        
        3. **Explore** the different tabs to analyze your meeting data
        
        4. **Export** insights and reports for further analysis
        """)

if __name__ == "__main__":
    main()