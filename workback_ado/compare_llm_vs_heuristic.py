#!/usr/bin/env python3
"""
Compare LLM vs Heuristic Classification for ADO Work Items

This script runs both classification methods on the same work items
and analyzes the differences to validate LLM accuracy improvements.

Author: Chin-Yew Lin
Date: November 11, 2025
"""

import os
import sys
import json
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Import the extractor class
from ado_workback_extraction import ADOWorkItemExtractor

def compare_classifications(
    org_url: str,
    pat_token: str,
    project: str,
    num_items: int = 50,
    months_back: int = 12
) -> Dict[str, Any]:
    """
    Extract work items and classify with both LLM and heuristics
    
    Returns:
        Comparison report with metrics and examples
    """
    print("="*80)
    print("LLM vs Heuristic Classification Comparison")
    print("="*80)
    
    # Initialize extractors
    print("\n🔧 Initializing extractors...")
    llm_extractor = ADOWorkItemExtractor(org_url, pat_token, project, use_llm=True)
    heuristic_extractor = ADOWorkItemExtractor(org_url, pat_token, project, use_llm=False)
    
    # Extract work items (shared between both)
    print(f"\n📥 Extracting {num_items} work items from {project}...")
    work_items = heuristic_extractor.extract_completed_work_items(
        months_back=months_back,
        min_story_points=0,
        max_story_points=100,
        work_item_types=['Feature', 'User Story', 'Task']
    )
    
    if not work_items:
        print("❌ No work items found")
        return {}
    
    print(f"✅ Found {len(work_items)} work items")
    work_items = work_items[:num_items]
    
    # Classify with both methods - using BATCH for efficiency
    print(f"\n🤖 Batch classifying {len(work_items)} items with LLM...")
    llm_classifications = llm_extractor.llm_batch_classify(work_items)
    
    llm_results = []
    for item in work_items:
        if item.id in llm_classifications:
            complexity_llm = llm_classifications[item.id]['complexity']
            value_llm = llm_classifications[item.id]['value']
        else:
            # Fallback to per-item
            complexity_llm = llm_extractor.llm_classify_complexity(item)
            value_llm = llm_extractor.llm_assess_value(item)
        
        llm_results.append({
            'id': item.id,
            'title': item.fields.get('System.Title', 'N/A'),
            'complexity': complexity_llm,
            'value': value_llm
        })
    print(f"✅ LLM classification complete")
    
    print(f"\n📊 Classifying {len(work_items)} items with heuristics...")
    heuristic_results = []
    for i, item in enumerate(work_items, 1):
        print(f"   Processing {i}/{len(work_items)}: ID {item.id}...", end='\r')
        complexity_h = heuristic_extractor.classify_complexity(item)
        value_h = heuristic_extractor.assess_value(item)
        heuristic_results.append({
            'id': item.id,
            'title': item.fields.get('System.Title', 'N/A'),
            'complexity': complexity_h,
            'value': value_h
        })
    print(f"\n✅ Heuristic classification complete")
    
    # Analyze differences
    print(f"\n📈 Analyzing classification differences...")
    
    comparison = {
        'metadata': {
            'org_url': org_url,
            'project': project,
            'num_items': len(work_items),
            'comparison_date': datetime.now().isoformat()
        },
        'complexity_comparison': analyze_classification_diff(
            llm_results, heuristic_results, 'complexity'
        ),
        'value_comparison': analyze_classification_diff(
            llm_results, heuristic_results, 'value'
        ),
        'detailed_items': []
    }
    
    # Add detailed item-by-item comparison
    for llm, heur, item in zip(llm_results, heuristic_results, work_items):
        assert llm['id'] == heur['id'], "Mismatch in work item IDs"
        
        comparison['detailed_items'].append({
            'id': llm['id'],
            'title': llm['title'],
            'llm': {
                'complexity': llm['complexity'],
                'value': llm['value']
            },
            'heuristic': {
                'complexity': heur['complexity'],
                'value': heur['value']
            },
            'agreement': {
                'complexity': llm['complexity'] == heur['complexity'],
                'value': llm['value'] == heur['value']
            },
            'description_length': len(item.fields.get('System.Description', '')),
            'has_story_points': item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints') is not None
        })
    
    return comparison

def analyze_classification_diff(
    llm_results: List[Dict],
    heuristic_results: List[Dict],
    field: str
) -> Dict[str, Any]:
    """Analyze differences between LLM and heuristic classifications"""
    
    llm_counts = defaultdict(int)
    heuristic_counts = defaultdict(int)
    agreements = 0
    disagreements = []
    
    for llm, heur in zip(llm_results, heuristic_results):
        llm_class = llm[field]
        heur_class = heur[field]
        
        llm_counts[llm_class] += 1
        heuristic_counts[heur_class] += 1
        
        if llm_class == heur_class:
            agreements += 1
        else:
            disagreements.append({
                'id': llm['id'],
                'title': llm['title'],
                'llm': llm_class,
                'heuristic': heur_class
            })
    
    total = len(llm_results)
    agreement_rate = (agreements / total * 100) if total > 0 else 0
    
    return {
        'total_items': total,
        'agreements': agreements,
        'disagreements': len(disagreements),
        'agreement_rate': f"{agreement_rate:.1f}%",
        'llm_distribution': dict(llm_counts),
        'heuristic_distribution': dict(heuristic_counts),
        'disagreement_examples': disagreements[:10]  # Top 10 examples
    }

def print_comparison_report(comparison: Dict[str, Any]):
    """Print formatted comparison report"""
    
    print("\n" + "="*80)
    print("COMPARISON REPORT")
    print("="*80)
    
    meta = comparison['metadata']
    print(f"\n📋 Metadata:")
    print(f"   Project: {meta['project']}")
    print(f"   Items Analyzed: {meta['num_items']}")
    print(f"   Date: {meta['comparison_date']}")
    
    # Complexity comparison
    print(f"\n🎯 Complexity Classification:")
    comp_comp = comparison['complexity_comparison']
    print(f"   Agreement Rate: {comp_comp['agreement_rate']}")
    print(f"   Agreements: {comp_comp['agreements']}/{comp_comp['total_items']}")
    print(f"   Disagreements: {comp_comp['disagreements']}")
    
    print(f"\n   LLM Distribution:")
    for k, v in comp_comp['llm_distribution'].items():
        pct = (v / comp_comp['total_items'] * 100)
        print(f"      {k}: {v} ({pct:.1f}%)")
    
    print(f"\n   Heuristic Distribution:")
    for k, v in comp_comp['heuristic_distribution'].items():
        pct = (v / comp_comp['total_items'] * 100)
        print(f"      {k}: {v} ({pct:.1f}%)")
    
    if comp_comp['disagreement_examples']:
        print(f"\n   Top Disagreements (Complexity):")
        for ex in comp_comp['disagreement_examples'][:5]:
            print(f"      ID {ex['id']}: {ex['title'][:60]}")
            print(f"         LLM: {ex['llm']}, Heuristic: {ex['heuristic']}")
    
    # Value comparison
    print(f"\n💎 Value Classification:")
    val_comp = comparison['value_comparison']
    print(f"   Agreement Rate: {val_comp['agreement_rate']}")
    print(f"   Agreements: {val_comp['agreements']}/{val_comp['total_items']}")
    print(f"   Disagreements: {val_comp['disagreements']}")
    
    print(f"\n   LLM Distribution:")
    for k, v in val_comp['llm_distribution'].items():
        pct = (v / val_comp['total_items'] * 100)
        print(f"      {k}: {v} ({pct:.1f}%)")
    
    print(f"\n   Heuristic Distribution:")
    for k, v in val_comp['heuristic_distribution'].items():
        pct = (v / val_comp['total_items'] * 100)
        print(f"      {k}: {v} ({pct:.1f}%)")
    
    if val_comp['disagreement_examples']:
        print(f"\n   Top Disagreements (Value):")
        for ex in val_comp['disagreement_examples'][:5]:
            print(f"      ID {ex['id']}: {ex['title'][:60]}")
            print(f"         LLM: {ex['llm']}, Heuristic: {ex['heuristic']}")
    
    # Summary statistics
    print(f"\n📊 Summary Statistics:")
    items_with_desc = sum(1 for item in comparison['detailed_items'] 
                          if item['description_length'] > 0)
    items_with_points = sum(1 for item in comparison['detailed_items'] 
                            if item['has_story_points'])
    
    total = len(comparison['detailed_items'])
    print(f"   Items with descriptions: {items_with_desc}/{total} ({items_with_desc/total*100:.1f}%)")
    print(f"   Items with story points: {items_with_points}/{total} ({items_with_points/total*100:.1f}%)")
    
    # Key insights
    print(f"\n💡 Key Insights:")
    comp_agree = float(comp_comp['agreement_rate'].rstrip('%'))
    val_agree = float(val_comp['agreement_rate'].rstrip('%'))
    
    if comp_agree >= 80 and val_agree >= 80:
        print(f"   ✅ High agreement: LLM and heuristics are well-aligned")
    elif comp_agree >= 60 or val_agree >= 60:
        print(f"   ⚠️  Moderate agreement: LLM provides different perspective")
    else:
        print(f"   🔍 Low agreement: LLM classifications differ significantly")
    
    # LLM advantages
    llm_more_high_value = comp_comp['llm_distribution'].get('High_Value', 0) > \
                         comp_comp['heuristic_distribution'].get('High_Value', 0)
    if llm_more_high_value:
        print(f"   📈 LLM identifies MORE high-value items (better at extracting business value from text)")
    
    print("\n" + "="*80)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Compare LLM vs Heuristic ADO classification'
    )
    parser.add_argument('--org-url', required=True, help='Azure DevOps organization URL')
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--num-items', type=int, default=50, help='Number of items to compare')
    parser.add_argument('--months-back', type=int, default=12, help='Months of history')
    parser.add_argument('--output', default='classification_comparison.json', 
                       help='Output file for detailed comparison')
    
    args = parser.parse_args()
    
    # Get PAT token from environment
    pat_token = os.environ.get('ADO_PAT')
    if not pat_token:
        print("ERROR: ADO_PAT environment variable not set")
        sys.exit(1)
    
    # Run comparison
    comparison = compare_classifications(
        args.org_url,
        pat_token,
        args.project,
        args.num_items,
        args.months_back
    )
    
    if not comparison:
        print("❌ Comparison failed")
        sys.exit(1)
    
    # Save detailed results
    with open(args.output, 'w') as f:
        json.dump(comparison, f, indent=2)
    print(f"\n💾 Detailed comparison saved to: {args.output}")
    
    # Print report
    print_comparison_report(comparison)
    
    print(f"\n✅ Comparison complete!")

if __name__ == '__main__':
    main()
