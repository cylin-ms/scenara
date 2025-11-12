#!/usr/bin/env python3
"""
Expert Review Workflow for ADO Workback Planning Training Data

Exports extracted work items to reviewer-friendly formats and tracks corrections.

Author: Chin-Yew Lin
Date: November 11, 2025
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
import html

def export_to_csv(training_data: List[Dict], output_file: str):
    """
    Export training data to CSV for expert review in Excel
    
    Args:
        training_data: List of training examples
        output_file: Output CSV file path
    """
    print(f"📊 Exporting {len(training_data)} items to CSV...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'ID',
            'Title',
            'Work Type',
            'Duration (days)',
            'Story Points',
            'Tags',
            'Description (preview)',
            'LLM Complexity',
            'LLM Value',
            'Outcome',
            'Reviewer Notes',
            'Correct Complexity',
            'Correct Value',
            'Issues Found'
        ])
        
        # Data rows
        for item in training_data:
            context = item.get('context', {})
            plan = item.get('plan', {})
            task = plan.get('task', {})
            outcome = item.get('outcome', {})
            metadata = item.get('metadata', {})
            
            # Clean description
            desc = context.get('description', '')
            desc_text = html.unescape(desc)
            desc_text = desc_text.replace('<', '').replace('>', '')
            desc_preview = desc_text[:200] + '...' if len(desc_text) > 200 else desc_text
            
            writer.writerow([
                item.get('training_id', ''),
                context.get('goal', ''),
                context.get('work_item_type', ''),
                outcome.get('actual_duration_days', ''),
                task.get('story_points', ''),
                ', '.join(context.get('tags', [])),
                desc_preview,
                metadata.get('complexity', ''),
                metadata.get('value', ''),
                outcome.get('overall_outcome', ''),
                '',  # Reviewer notes (to be filled)
                '',  # Correct complexity (to be filled)
                '',  # Correct value (to be filled)
                ''   # Issues found (to be filled)
            ])
    
    print(f"✅ CSV exported to: {output_file}")
    print(f"📝 Expert reviewers can now edit columns K-N (Reviewer Notes through Issues Found)")

def export_to_review_html(training_data: List[Dict], output_file: str):
    """
    Export training data to interactive HTML for web-based review
    
    Args:
        training_data: List of training examples
        output_file: Output HTML file path
    """
    print(f"🌐 Generating HTML review interface...")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ADO Workback Training Data Review</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #0078d4;
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .work-item {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .work-item:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .title {{
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            margin-left: 8px;
        }}
        .complexity-Q2 {{ background: #d4edda; color: #155724; }}
        .complexity-Q3 {{ background: #fff3cd; color: #856404; }}
        .complexity-Q1 {{ background: #f8d7da; color: #721c24; }}
        .value-High {{ background: #cfe2ff; color: #084298; }}
        .value-Medium {{ background: #e7f1ff; color: #0a58ca; }}
        .value-Low {{ background: #f8f9fa; color: #495057; }}
        .metadata {{
            color: #666;
            font-size: 14px;
            margin: 10px 0;
        }}
        .description {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 14px;
            line-height: 1.6;
            max-height: 200px;
            overflow-y: auto;
        }}
        .review-section {{
            border-top: 2px solid #e9ecef;
            padding-top: 15px;
            margin-top: 15px;
        }}
        .review-form {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        .form-group {{
            display: flex;
            flex-direction: column;
        }}
        label {{
            font-weight: 500;
            margin-bottom: 5px;
            color: #495057;
        }}
        select, textarea {{
            padding: 8px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
        }}
        textarea {{
            resize: vertical;
            min-height: 60px;
            grid-column: 1 / -1;
        }}
        .save-btn {{
            background: #0078d4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            margin-top: 10px;
        }}
        .save-btn:hover {{
            background: #006cbe;
        }}
        .filter-bar {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .filter-bar select {{
            margin: 0 10px;
        }}
    </style>
</head>
<body>
    <h1>🔍 ADO Workback Training Data Expert Review</h1>
    
    <div class="stats">
        <h3>Dataset Statistics</h3>
        <p><strong>Total Items:</strong> {len(training_data)}</p>
        <p><strong>Export Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Project:</strong> {training_data[0].get('metadata', {}).get('project', 'N/A') if training_data else 'N/A'}</p>
    </div>
    
    <div class="filter-bar">
        <label>Filter by Complexity:</label>
        <select id="complexityFilter" onchange="filterItems()">
            <option value="all">All</option>
            <option value="Q2_Low_Complexity">Q2 (Low)</option>
            <option value="Q3_Medium_Complexity">Q3 (Medium)</option>
            <option value="Q1_High_Complexity">Q1 (High)</option>
        </select>
        
        <label>Filter by Value:</label>
        <select id="valueFilter" onchange="filterItems()">
            <option value="all">All</option>
            <option value="High_Value">High</option>
            <option value="Medium_Value">Medium</option>
            <option value="Low_Value">Low</option>
        </select>
    </div>
    
    <div id="itemsContainer">
"""
    
    # Add work items
    for idx, item in enumerate(training_data):
        context = item.get('context', {})
        plan = item.get('plan', {})
        task = plan.get('task', {})
        outcome = item.get('outcome', {})
        metadata = item.get('metadata', {})
        
        training_id = item.get('training_id', '')
        title = context.get('goal', 'Untitled')
        complexity = metadata.get('complexity', 'Unknown')
        value = metadata.get('value', 'Unknown')
        work_type = context.get('work_item_type', 'Task')
        duration = outcome.get('actual_duration_days', 'N/A')
        
        # Clean description
        desc = context.get('description', 'No description')
        desc_text = html.unescape(desc)
        desc_text = desc_text.replace('<p', '\\n<p').replace('<br>', '\\n')
        
        # Extract complexity level for badge
        comp_level = complexity.split('_')[0] if '_' in complexity else 'Q2'
        
        html_content += f"""
    <div class="work-item" data-complexity="{complexity}" data-value="{value}">
        <div class="header">
            <div class="title">
                {title}
                <span class="badge complexity-{comp_level}">{complexity}</span>
                <span class="badge value-{value.split('_')[0]}">{value}</span>
            </div>
            <div class="metadata">
                ID: {training_id} | Type: {work_type} | Duration: {duration} days
            </div>
        </div>
        
        <div class="description">
            {desc_text[:1000]}
        </div>
        
        <div class="review-section">
            <h4>Expert Review</h4>
            <form class="review-form" onsubmit="saveReview(event, '{training_id}')">
                <div class="form-group">
                    <label>Correct Complexity:</label>
                    <select name="complexity">
                        <option value="">-- Select --</option>
                        <option value="Q2_Low_Complexity">Q2 (Low Complexity)</option>
                        <option value="Q3_Medium_Complexity">Q3 (Medium Complexity)</option>
                        <option value="Q1_High_Complexity">Q1 (High Complexity)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Correct Value:</label>
                    <select name="value">
                        <option value="">-- Select --</option>
                        <option value="High_Value">High Value</option>
                        <option value="Medium_Value">Medium Value</option>
                        <option value="Low_Value">Low Value</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Reviewer Notes / Issues:</label>
                    <textarea name="notes" placeholder="Enter any corrections, issues, or insights..."></textarea>
                </div>
                
                <button type="submit" class="save-btn">💾 Save Review</button>
            </form>
        </div>
    </div>
"""
    
    html_content += """
    </div>
    
    <script>
        let reviews = {};
        
        function saveReview(event, itemId) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            
            reviews[itemId] = {
                complexity: formData.get('complexity'),
                value: formData.get('value'),
                notes: formData.get('notes'),
                timestamp: new Date().toISOString()
            };
            
            // Save to localStorage
            localStorage.setItem('ado_reviews', JSON.stringify(reviews));
            
            alert('✅ Review saved for ' + itemId);
        }
        
        function filterItems() {
            const complexityFilter = document.getElementById('complexityFilter').value;
            const valueFilter = document.getElementById('valueFilter').value;
            const items = document.querySelectorAll('.work-item');
            
            items.forEach(item => {
                const complexity = item.dataset.complexity;
                const value = item.dataset.value;
                
                const showComplexity = complexityFilter === 'all' || complexity === complexityFilter;
                const showValue = valueFilter === 'all' || value === valueFilter;
                
                item.style.display = (showComplexity && showValue) ? 'block' : 'none';
            });
        }
        
        function exportReviews() {
            const reviewsJson = JSON.stringify(reviews, null, 2);
            const blob = new Blob([reviewsJson], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'expert_reviews_' + new Date().toISOString().split('T')[0] + '.json';
            a.click();
        }
        
        // Load existing reviews
        const saved = localStorage.getItem('ado_reviews');
        if (saved) {
            reviews = JSON.parse(saved);
        }
    </script>
    
    <div style="text-align: center; margin: 40px 0;">
        <button onclick="exportReviews()" class="save-btn">📥 Export All Reviews as JSON</button>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML review interface generated: {output_file}")
    print(f"🌐 Open in browser to start reviewing")
    print(f"💾 Reviews are saved in browser localStorage and can be exported as JSON")

def create_review_summary(training_data_file: str, reviews_file: str, output_file: str):
    """
    Create summary report comparing LLM classifications with expert corrections
    
    Args:
        training_data_file: Original training data JSON
        reviews_file: Expert reviews JSON
        output_file: Output summary file
    """
    with open(training_data_file, 'r') as f:
        training_data = json.load(f)
    
    with open(reviews_file, 'r') as f:
        reviews = json.load(f)
    
    print(f"📊 Analyzing {len(reviews)} expert reviews...")
    
    complexity_agreement = 0
    value_agreement = 0
    total_reviewed = 0
    
    corrections = {
        'complexity': defaultdict(int),
        'value': defaultdict(int)
    }
    
    for item in training_data:
        item_id = item.get('training_id', '')
        if item_id in reviews:
            total_reviewed += 1
            review = reviews[item_id]
            
            llm_complexity = item.get('metadata', {}).get('complexity', '')
            llm_value = item.get('metadata', {}).get('value', '')
            
            expert_complexity = review.get('complexity', '')
            expert_value = review.get('value', '')
            
            if expert_complexity:
                if llm_complexity == expert_complexity:
                    complexity_agreement += 1
                else:
                    corrections['complexity'][f"{llm_complexity} -> {expert_complexity}"] += 1
            
            if expert_value:
                if llm_value == expert_value:
                    value_agreement += 1
                else:
                    corrections['value'][f"{llm_value} -> {expert_value}"] += 1
    
    report = f"""Expert Review Summary
================================================================================
Total Training Examples: {len(training_data)}
Items Reviewed: {total_reviewed} ({total_reviewed/len(training_data)*100:.1f}%)

Complexity Classification:
  Agreement Rate: {complexity_agreement}/{total_reviewed} ({complexity_agreement/total_reviewed*100:.1f}%)
  Common Corrections:
"""
    
    for correction, count in sorted(corrections['complexity'].items(), key=lambda x: -x[1])[:5]:
        report += f"    - {correction}: {count} times\n"
    
    report += f"""
Value Classification:
  Agreement Rate: {value_agreement}/{total_reviewed} ({value_agreement/total_reviewed*100:.1f}%)
  Common Corrections:
"""
    
    for correction, count in sorted(corrections['value'].items(), key=lambda x: -x[1])[:5]:
        report += f"    - {correction}: {count} times\n"
    
    report += "\n================================================================================\n"
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(report)
    print(f"💾 Summary saved to: {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Expert Review Workflow for ADO Training Data'
    )
    parser.add_argument('--input', required=True, help='Input training data JSON file')
    parser.add_argument('--format', choices=['csv', 'html', 'both'], default='both',
                       help='Export format')
    parser.add_argument('--output-csv', default='expert_review.csv',
                       help='Output CSV file')
    parser.add_argument('--output-html', default='expert_review.html',
                       help='Output HTML file')
    
    args = parser.parse_args()
    
    # Load training data
    with open(args.input, 'r') as f:
        training_data = json.load(f)
    
    print(f"📂 Loaded {len(training_data)} training examples from {args.input}")
    
    # Export to requested formats
    if args.format in ['csv', 'both']:
        export_to_csv(training_data, args.output_csv)
    
    if args.format in ['html', 'both']:
        export_to_review_html(training_data, args.output_html)
    
    print("\n✅ Expert review workflow ready!")
    print(f"\n📝 Next steps:")
    if args.format in ['csv', 'both']:
        print(f"   1. Open {args.output_csv} in Excel for review")
    if args.format in ['html', 'both']:
        print(f"   2. Open {args.output_html} in browser for interactive review")
    print(f"   3. Expert reviewers fill in corrections")
    print(f"   4. Export reviews and analyze with --analyze flag")

if __name__ == '__main__':
    from collections import defaultdict
    main()
