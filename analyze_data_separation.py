#!/usr/bin/env python3
"""
Data Separation Benefits Demo
Demonstrates the advantages of maintaining separate real vs synthetic data tracks
"""

import json
import os
from typing import Dict, List, Any

def analyze_data_separation():
    """Analyze and demonstrate data separation benefits"""
    
    print("🔄 Data Separation Analysis")
    print("=" * 50)
    
    # Load separated data files
    data_dir = "meeting_prep_data"
    
    files = {
        'real': f"{data_dir}/training_scenarios_real.json",
        'synthetic': f"{data_dir}/training_scenarios_synthetic.json", 
        'analysis': f"{data_dir}/training_analysis_separated.json"
    }
    
    # Check file existence
    for data_type, file_path in files.items():
        if not os.path.exists(file_path):
            print(f"❌ {data_type.title()} data file not found: {file_path}")
            return
        print(f"✅ {data_type.title()} data file found")
    
    # Load data
    with open(files['real'], 'r') as f:
        real_data = json.load(f)
    
    with open(files['synthetic'], 'r') as f:
        synthetic_data = json.load(f)
    
    with open(files['analysis'], 'r') as f:
        analysis = json.load(f)
    
    print(f"\n📊 Dataset Overview:")
    print(f"Real Data: {len(real_data)} scenarios")
    print(f"Synthetic Data: {len(synthetic_data)} scenarios")
    print(f"Total: {len(real_data) + len(synthetic_data)} scenarios")
    
    # Quality Analysis
    print(f"\n📈 Quality Analysis:")
    
    real_quality = [s.get('quality_score', 7.0) for s in real_data]
    synthetic_quality = [s.get('quality_score', 7.0) for s in synthetic_data]
    
    real_avg = sum(real_quality) / len(real_quality) if real_quality else 0
    synthetic_avg = sum(synthetic_quality) / len(synthetic_quality) if synthetic_quality else 0
    
    print(f"Real Data Average Quality: {real_avg:.2f}/10.0")
    print(f"Synthetic Data Average Quality: {synthetic_avg:.2f}/10.0")
    
    real_high_quality = sum(1 for q in real_quality if q >= 8.0)
    synthetic_high_quality = sum(1 for q in synthetic_quality if q >= 8.0)
    
    print(f"Real Data High Quality (8.0+): {real_high_quality}/{len(real_data)} ({real_high_quality/len(real_data)*100:.1f}%)")
    print(f"Synthetic Data High Quality (8.0+): {synthetic_high_quality}/{len(synthetic_data)} ({synthetic_high_quality/len(synthetic_data)*100:.1f}%)")
    
    # Data Provenance Analysis
    print(f"\n🔍 Data Provenance Analysis:")
    
    real_provenance = {}
    synthetic_provenance = {}
    
    for scenario in real_data:
        prov = scenario.get('data_provenance', {})
        method = prov.get('collection_method', 'unknown')
        real_provenance[method] = real_provenance.get(method, 0) + 1
    
    for scenario in synthetic_data:
        prov = scenario.get('data_provenance', {})
        method = prov.get('collection_method', 'unknown')
        synthetic_provenance[method] = synthetic_provenance.get(method, 0) + 1
    
    print(f"\nReal Data Collection Methods:")
    for method, count in sorted(real_provenance.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {method}: {count}")
    
    print(f"\nSynthetic Data Collection Methods:")
    for method, count in sorted(synthetic_provenance.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {method}: {count}")
    
    # Meeting Type Coverage
    print(f"\n🏢 Meeting Type Coverage:")
    
    real_types = set(s.get('meeting_type', 'Unknown') for s in real_data)
    synthetic_types = set(s.get('meeting_type', 'Unknown') for s in synthetic_data)
    
    overlap = real_types.intersection(synthetic_types)
    unique_real = real_types - synthetic_types
    unique_synthetic = synthetic_types - real_types
    
    print(f"Real Data Meeting Types: {len(real_types)}")
    print(f"Synthetic Data Meeting Types: {len(synthetic_types)}")
    print(f"Overlapping Types: {len(overlap)}")
    print(f"Unique to Real: {len(unique_real)}")
    print(f"Unique to Synthetic: {len(unique_synthetic)}")
    
    if unique_real:
        print(f"\nMeeting Types Only in Real Data:")
        for meeting_type in sorted(unique_real)[:5]:  # Show first 5
            print(f"  - {meeting_type}")
        if len(unique_real) > 5:
            print(f"  ... and {len(unique_real) - 5} more")
    
    if unique_synthetic:
        print(f"\nMeeting Types Only in Synthetic Data:")
        for meeting_type in sorted(unique_synthetic)[:5]:  # Show first 5
            print(f"  - {meeting_type}")
        if len(unique_synthetic) > 5:
            print(f"  ... and {len(unique_synthetic) - 5} more")
    
    # Benefits Summary
    print(f"\n✨ Data Separation Benefits:")
    print(f"=" * 50)
    
    benefits = [
        "🎯 **Data Integrity**: Real and synthetic data never mix",
        "📊 **Targeted Analysis**: Analyze each data type independently", 
        "🔬 **Validation Studies**: Compare model performance on real vs synthetic",
        "🏗️ **Model Training**: Train on synthetic, validate on real",
        "📈 **Quality Tracking**: Monitor quality differences between data types",
        "🔍 **Source Transparency**: Clear provenance for every scenario",
        "⚖️ **Bias Detection**: Identify synthetic data bias vs real patterns",
        "🚀 **Scalability**: Add new data sources without contamination"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    # Recommendations
    print(f"\n🎯 Recommendations:")
    print(f"=" * 30)
    
    recommendations = []
    
    if real_avg > synthetic_avg:
        recommendations.append("Real data shows higher quality - use for validation")
    elif synthetic_avg > real_avg:
        recommendations.append("Synthetic data shows higher quality - check for overfitting")
    
    if len(unique_real) > 0:
        recommendations.append(f"Generate synthetic data for {len(unique_real)} real-only meeting types")
    
    if len(unique_synthetic) > 0:
        recommendations.append(f"Collect real data for {len(unique_synthetic)} synthetic-only meeting types")
    
    real_coverage = len(real_data) / (len(real_data) + len(synthetic_data)) * 100
    if real_coverage < 20:
        recommendations.append("Consider collecting more real data (currently <20%)")
    elif real_coverage > 80:
        recommendations.append("Consider generating more synthetic data for diversity")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\n✅ Data separation analysis complete!")
    print(f"📁 View detailed analysis in Streamlit: http://localhost:8503")


if __name__ == "__main__":
    analyze_data_separation()