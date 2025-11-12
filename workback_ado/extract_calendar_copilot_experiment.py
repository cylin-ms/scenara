#!/usr/bin/env python3
"""
Calendar Copilot Experiment - Extract work items related to calendar and AI features

This creates a focused experiment extracting Outlook work items related to:
- Calendar features
- Copilot/AI functionality
- Scheduling and meetings

Author: Chin-Yew Lin
Date: November 12, 2025
"""

import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from ado_workback_extraction import ADOWorkItemExtractor

def extract_calendar_copilot_items(
    org_url: str,
    pat_token: str,
    project: str = "Outlook",
    months_back: int = 12,
    max_items: int = 50,
    use_llm: bool = True
):
    """
    Extract calendar and AI-related work items from Outlook project
    
    Focus areas:
    - Scheduling and Meetings area path
    - Items with keywords: calendar, copilot, AI, scheduling, meetings
    - Time and Focus area (may include calendar features)
    """
    print("="*80)
    print("Calendar Copilot Experiment - Work Item Extraction")
    print("="*80)
    
    # Initialize extractor
    extractor = ADOWorkItemExtractor(org_url, pat_token, project, use_llm=use_llm)
    
    # Custom WIQL query for calendar/copilot items
    date_threshold = (datetime.now() - timedelta(days=months_back * 30)).strftime('%Y-%m-%d')
    
    wiql_query = f"""
    SELECT [System.Id], [System.Title], [System.State], 
           [System.WorkItemType], [System.AssignedTo],
           [System.AreaPath],
           [Microsoft.VSTS.Scheduling.StoryPoints],
           [Microsoft.VSTS.Scheduling.OriginalEstimate],
           [Microsoft.VSTS.Scheduling.CompletedWork],
           [System.CreatedDate], [System.ChangedDate],
           [Microsoft.VSTS.Common.ClosedDate],
           [Microsoft.VSTS.Common.Priority],
           [System.Description],
           [System.Tags]
    FROM WorkItems
    WHERE [System.TeamProject] = '{project}'
      AND [System.WorkItemType] IN ('Feature', 'User Story', 'Task')
      AND (
        [System.AreaPath] UNDER 'Outlook\\Scheduling and Meetings'
        OR [System.AreaPath] UNDER 'Outlook\\Time and Focus'
        OR [System.Title] CONTAINS 'calendar'
        OR [System.Title] CONTAINS 'copilot'
        OR [System.Title] CONTAINS 'AI'
        OR [System.Title] CONTAINS 'scheduling'
        OR [System.Tags] CONTAINS 'calendar'
        OR [System.Tags] CONTAINS 'copilot'
      )
      AND [System.ChangedDate] >= '{date_threshold}'
    ORDER BY [System.ChangedDate] DESC
    """
    
    print(f"\n🔍 Searching for Calendar/Copilot items...")
    print(f"   Area paths: Scheduling and Meetings, Time and Focus")
    print(f"   Keywords: calendar, copilot, AI, scheduling")
    print(f"   Date range: Last {months_back} months")
    
    from azure.devops.v7_0.work_item_tracking.models import Wiql
    
    wiql_object = Wiql(query=wiql_query)
    query_result = extractor.wit_client.query_by_wiql(wiql_object).work_items
    
    if not query_result:
        print("❌ No matching items found")
        return []
    
    print(f"📊 Found {len(query_result)} matching work items")
    
    # Fetch work items
    item_ids = [item.id for item in query_result[:max_items]]
    work_items = extractor.wit_client.get_work_items(item_ids, expand='All')
    
    print(f"✅ Retrieved {len(work_items)} work items")
    
    # Analyze area distribution
    area_counts = defaultdict(int)
    keyword_matches = defaultdict(int)
    
    for item in work_items:
        area = item.fields.get('System.AreaPath', 'Unknown')
        area_counts[area] += 1
        
        # Check keyword matches
        title = item.fields.get('System.Title', '').lower()
        tags = item.fields.get('System.Tags', '').lower()
        
        if 'calendar' in title or 'calendar' in tags:
            keyword_matches['calendar'] += 1
        if 'copilot' in title or 'copilot' in tags:
            keyword_matches['copilot'] += 1
        if 'ai' in title or 'ai' in tags:
            keyword_matches['ai'] += 1
        if 'scheduling' in title or 'scheduling' in tags:
            keyword_matches['scheduling'] += 1
    
    print(f"\n📊 Area Path Distribution:")
    for area, count in sorted(area_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {area}: {count}")
    
    print(f"\n🔑 Keyword Matches:")
    for keyword, count in sorted(keyword_matches.items(), key=lambda x: x[1], reverse=True):
        print(f"   {keyword}: {count}")
    
    # Classify with LLM (batch)
    print(f"\n🤖 Classifying {len(work_items)} items...")
    if use_llm:
        llm_classifications = extractor.llm_batch_classify(work_items)
    else:
        llm_classifications = {}
    
    # Build training examples
    print(f"\n🏗️  Building training examples...")
    training_examples = []
    complexity_counts = defaultdict(int)
    value_counts = defaultdict(int)
    
    for item in work_items:
        if item.id in llm_classifications:
            complexity = llm_classifications[item.id]['complexity']
            value = llm_classifications[item.id]['value']
        else:
            complexity = extractor.classify_complexity(item)
            value = extractor.assess_value(item)
        
        example = extractor._build_training_example_with_classification(
            item, complexity, value
        )
        
        # Add experiment-specific metadata
        example['experiment'] = {
            'name': 'calendar_copilot',
            'focus_area': 'calendar_ai_features',
            'extraction_date': datetime.now().isoformat()
        }
        
        training_examples.append(example)
        complexity_counts[complexity] += 1
        value_counts[value] += 1
    
    print(f"✅ Built {len(training_examples)} training examples")
    
    print(f"\n📊 Classification Distribution:")
    print(f"   Complexity: {dict(complexity_counts)}")
    print(f"   Value: {dict(value_counts)}")
    
    return training_examples

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extract Calendar Copilot experiment data from ADO'
    )
    parser.add_argument('--org-url', default='https://office.visualstudio.com',
                       help='Azure DevOps organization URL')
    parser.add_argument('--project', default='Outlook', help='Project name')
    parser.add_argument('--months-back', type=int, default=12, help='Months of history')
    parser.add_argument('--max-items', type=int, default=50, help='Maximum items to extract')
    parser.add_argument('--use-llm', action='store_true', help='Use LLM classification')
    parser.add_argument('--output', default='calendar_copilot_experiment.json',
                       help='Output file')
    
    args = parser.parse_args()
    
    # Get PAT from environment
    pat_token = os.environ.get('ADO_PAT')
    if not pat_token:
        print("ERROR: ADO_PAT environment variable not set")
        sys.exit(1)
    
    # Extract data
    examples = extract_calendar_copilot_items(
        args.org_url,
        pat_token,
        args.project,
        args.months_back,
        args.max_items,
        args.use_llm
    )
    
    if not examples:
        print("❌ No examples extracted")
        sys.exit(1)
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(examples, f, indent=2, default=str)
    
    print(f"\n💾 Saved {len(examples)} examples to: {args.output}")
    
    # Generate statistics
    stats_file = args.output.replace('.json', '_stats.json')
    stats = {
        'total_examples': len(examples),
        'complexity_distribution': defaultdict(int),
        'value_distribution': defaultdict(int),
        'area_distribution': defaultdict(int),
        'extraction_date': datetime.now().isoformat()
    }
    
    for ex in examples:
        stats['complexity_distribution'][ex['metadata']['complexity']] += 1
        stats['value_distribution'][ex['metadata']['value']] += 1
        area = ex['context'].get('area_path', 'Unknown')
        # Get last part of area path
        area_leaf = area.split('\\')[-1] if '\\' in area else area
        stats['area_distribution'][area_leaf] += 1
    
    # Convert defaultdicts to regular dicts
    stats['complexity_distribution'] = dict(stats['complexity_distribution'])
    stats['value_distribution'] = dict(stats['value_distribution'])
    stats['area_distribution'] = dict(stats['area_distribution'])
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"📊 Saved statistics to: {stats_file}")
    print("\n✅ Calendar Copilot experiment extraction complete!")
    print("\n📝 Next steps:")
    print(f"   1. Review {args.output}")
    print(f"   2. Generate expert review: python expert_review_workflow.py --input {args.output}")
    print(f"   3. Compare with other extractions")

if __name__ == '__main__':
    main()
