#!/usr/bin/env python3
"""
Data Separation Summary
Shows the complete separated data system status and benefits
"""

import json
import os
from datetime import datetime

def display_separation_summary():
    """Display comprehensive summary of the separated data system"""
    
    print("🎯 PromptCoT Meeting Data Separation System")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # File status check
    data_dir = "meeting_prep_data"
    files = {
        '🔴 Real Data': f"{data_dir}/training_scenarios_real.json",
        '🔵 Synthetic Data': f"{data_dir}/training_scenarios_synthetic.json",
        '📦 Combined Data': f"{data_dir}/training_scenarios_combined.json",
        '📊 Analysis': f"{data_dir}/training_analysis_separated.json",
        '📝 Legacy Data': f"{data_dir}/training_scenarios.json"
    }
    
    print("📁 File Status:")
    print("-" * 30)
    for label, filepath in files.items():
        if os.path.exists(filepath):
            size_kb = os.path.getsize(filepath) / 1024
            print(f"✅ {label}: {size_kb:.1f} KB")
        else:
            print(f"❌ {label}: Not found")
    print()
    
    # Load and analyze data
    try:
        with open(files['📊 Analysis'], 'r') as f:
            analysis = json.load(f)
        
        sep = analysis.get('separation_summary', {})
        
        print("📊 Data Distribution:")
        print("-" * 30)
        print(f"🔴 Real Data: {sep.get('real_data_count', 0)} scenarios ({sep.get('real_percentage', 0):.1f}%)")
        print(f"🔵 Synthetic Data: {sep.get('synthetic_data_count', 0)} scenarios ({sep.get('synthetic_percentage', 0):.1f}%)")
        print(f"📦 Total: {sep.get('total_count', 0)} scenarios")
        print()
        
        # Quality comparison
        real_analysis = analysis.get('real_data_analysis', {})
        synthetic_analysis = analysis.get('synthetic_data_analysis', {})
        
        print("📈 Quality Analysis:")
        print("-" * 30)
        
        if real_analysis.get('quality_scores'):
            real_quality = real_analysis['quality_scores']
            print(f"🔴 Real Data Quality:")
            print(f"   Average: {real_quality.get('average', 0):.2f}/10.0")
            print(f"   High Quality (8.0+): {real_quality.get('high_quality', 0)}")
            print(f"   Range: {real_quality.get('min', 0):.1f} - {real_quality.get('max', 0):.1f}")
        
        if synthetic_analysis.get('quality_scores'):
            synthetic_quality = synthetic_analysis['quality_scores']
            print(f"🔵 Synthetic Data Quality:")
            print(f"   Average: {synthetic_quality.get('average', 0):.2f}/10.0")
            print(f"   High Quality (8.0+): {synthetic_quality.get('high_quality', 0)}")
            print(f"   Range: {synthetic_quality.get('min', 0):.1f} - {synthetic_quality.get('max', 0):.1f}")
        print()
        
        # Source distribution
        print("🏭 Data Sources:")
        print("-" * 30)
        
        if real_analysis.get('sources'):
            print("🔴 Real Data Sources:")
            for source, count in sorted(real_analysis['sources'].items(), key=lambda x: x[1], reverse=True):
                print(f"   - {source}: {count}")
        
        if synthetic_analysis.get('sources'):
            print("🔵 Synthetic Data Sources:")
            for source, count in sorted(synthetic_analysis['sources'].items(), key=lambda x: x[1], reverse=True):
                print(f"   - {source}: {count}")
        print()
        
        # Meeting type coverage
        real_types = len(real_analysis.get('meeting_types', {}))
        synthetic_types = len(synthetic_analysis.get('meeting_types', {}))
        
        print("🏢 Meeting Type Coverage:")
        print("-" * 30)
        print(f"🔴 Real Data Types: {real_types}")
        print(f"🔵 Synthetic Data Types: {synthetic_types}")
        
        if real_analysis.get('meeting_types') and synthetic_analysis.get('meeting_types'):
            real_type_set = set(real_analysis['meeting_types'].keys())
            synthetic_type_set = set(synthetic_analysis['meeting_types'].keys())
            overlap = len(real_type_set.intersection(synthetic_type_set))
            print(f"⚖️ Overlapping Types: {overlap}")
            print(f"🔴 Unique to Real: {len(real_type_set - synthetic_type_set)}")
            print(f"🔵 Unique to Synthetic: {len(synthetic_type_set - real_type_set)}")
        print()
        
    except Exception as e:
        print(f"❌ Error loading analysis: {e}")
        print()
    
    # System benefits
    print("✨ Data Separation Benefits:")
    print("-" * 30)
    benefits = [
        "🎯 Data Integrity - Real and synthetic data never mix",
        "📊 Targeted Analysis - Analyze each data type independently",
        "🔬 Validation Studies - Compare model performance on real vs synthetic",
        "🏗️ Model Training - Train on synthetic, validate on real",
        "📈 Quality Tracking - Monitor quality differences between data types",
        "🔍 Source Transparency - Clear provenance for every scenario",
        "⚖️ Bias Detection - Identify synthetic data bias vs real patterns",
        "🚀 Scalability - Add new data sources without contamination"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    print()
    
    # Available tools
    print("🛠️ Available Tools:")
    print("-" * 30)
    tools = [
        ("update_training_data_separated.py", "Generate separated data tracks"),
        ("analyze_data_separation.py", "Analyze separation benefits"),
        ("meeting_data_explorer_separated.py", "Streamlit separated data explorer"),
        ("update_training_data.py", "Legacy combined data updater"),
        ("meeting_data_explorer.py", "Legacy combined data explorer")
    ]
    
    for tool, description in tools:
        if os.path.exists(tool):
            print(f"  ✅ {tool} - {description}")
        else:
            print(f"  ❌ {tool} - {description}")
    print()
    
    # Access information
    print("🌐 Access Information:")
    print("-" * 30)
    print("📊 Separated Data Explorer: http://localhost:8503")
    print("📦 Legacy Combined Explorer: http://localhost:8501")
    print("📁 Data Directory: meeting_prep_data/")
    print("📖 Documentation: docs/Data_Separation_System.md")
    print()
    
    # Quick commands
    print("⚡ Quick Commands:")
    print("-" * 30)
    print("# Generate separated data")
    print("python update_training_data_separated.py")
    print()
    print("# Analyze separation benefits")
    print("python analyze_data_separation.py")
    print()
    print("# Launch separated data explorer")
    print("streamlit run meeting_data_explorer_separated.py --server.port 8503")
    print()
    
    print("✅ Data separation system ready!")
    print("🎯 Real and synthetic data are now properly separated for maximum integrity!")


if __name__ == "__main__":
    display_separation_summary()