#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Document Collaboration Integration
Compare collaborator rankings before and after document API integration

This script will:
1. Run document_collaboration_api.py to get fresh data
2. Run collaborator_discovery.py BEFORE integration (using old data)
3. Run collaborator_discovery.py AFTER integration (using new data)
4. Compare the rankings and show differences
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

def safe_print(text: str) -> None:
    """Print with Windows UTF-8 handling"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def run_command(cmd: List[str], description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output"""
    safe_print(f"\n{'='*60}")
    safe_print(f"🚀 {description}")
    safe_print(f"{'='*60}")
    safe_print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            safe_print(f"✅ {description} - SUCCESS")
            return True, result.stdout
        else:
            safe_print(f"❌ {description} - FAILED")
            safe_print(f"Error: {result.stderr}")
            return False, result.stderr
            
    except Exception as e:
        safe_print(f"❌ {description} - EXCEPTION: {e}")
        return False, str(e)

def get_latest_file(pattern: str) -> str:
    """Get the most recent file matching pattern"""
    files = list(Path('.').glob(pattern))
    if not files:
        return None
    return str(max(files, key=lambda x: x.stat().st_mtime))

def load_results(filepath: str) -> Dict:
    """Load JSON results file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_rankings(before: Dict, after: Dict) -> None:
    """Compare collaborator rankings before and after integration"""
    safe_print(f"\n{'='*60}")
    safe_print("📊 COMPARISON: BEFORE vs AFTER Document Integration")
    safe_print(f"{'='*60}")
    
    before_collabs = {c['name']: c for c in before['collaborators']}
    after_collabs = {c['name']: c for c in after['collaborators']}
    
    # Get top 10 from each
    before_top10 = before['collaborators'][:10]
    after_top10 = after['collaborators'][:10]
    
    safe_print(f"\n🔵 BEFORE Integration (Algorithm: {before['algorithm_version']})")
    safe_print(f"Total Collaborators: {len(before['collaborators'])}")
    safe_print(f"Data Sources: Calendar + Graph API + Teams Chat")
    safe_print(f"\nTop 10:")
    for i, collab in enumerate(before_top10, 1):
        safe_print(f"  {i:2d}. {collab['name']:<30} Score: {collab['importance_score']:6.2f}")
    
    safe_print(f"\n🟢 AFTER Integration (Algorithm: {after['algorithm_version']})")
    safe_print(f"Total Collaborators: {len(after['collaborators'])}")
    safe_print(f"Data Sources: Calendar + Graph API + Teams Chat + DOCUMENTS")
    safe_print(f"\nTop 10:")
    for i, collab in enumerate(after_top10, 1):
        # Find previous rank
        prev_rank = None
        for j, prev in enumerate(before['collaborators'], 1):
            if prev['name'] == collab['name']:
                prev_rank = j
                break
        
        rank_change = ""
        if prev_rank:
            if prev_rank > i:
                rank_change = f" ⬆️ +{prev_rank - i}"
            elif prev_rank < i:
                rank_change = f" ⬇️ -{i - prev_rank}"
            else:
                rank_change = " ➡️ Same"
        else:
            rank_change = " ✨ NEW!"
        
        doc_score = collab.get('document_collaboration_score', 0)
        doc_info = f" [+{doc_score} docs]" if doc_score > 0 else ""
        
        safe_print(f"  {i:2d}. {collab['name']:<30} Score: {collab['importance_score']:6.2f}{doc_info}{rank_change}")
    
    # Find new entries in top 10
    before_top10_names = set(c['name'] for c in before_top10)
    after_top10_names = set(c['name'] for c in after_top10)
    
    new_in_top10 = after_top10_names - before_top10_names
    dropped_from_top10 = before_top10_names - after_top10_names
    
    if new_in_top10:
        safe_print(f"\n✨ NEW Collaborators in Top 10:")
        for name in new_in_top10:
            collab = after_collabs[name]
            doc_score = collab.get('document_collaboration_score', 0)
            onedrive = collab.get('onedrive_direct_shares', 0) + collab.get('onedrive_group_shares', 0)
            teams_att = collab.get('teams_direct_attachments', 0) + collab.get('teams_group_attachments', 0)
            safe_print(f"  • {name}: OneDrive={onedrive}, Teams={teams_att}, Score={collab['importance_score']:.2f}")
    
    if dropped_from_top10:
        safe_print(f"\n⬇️ Dropped from Top 10:")
        for name in dropped_from_top10:
            safe_print(f"  • {name}")
    
    # Document-only collaborators
    doc_only = [c for c in after['collaborators'] if c.get('document_only_collaborator', False)]
    if doc_only:
        safe_print(f"\n📄 Document-Only Collaborators (no meetings/chats):")
        safe_print(f"Found {len(doc_only)} document-only relationships:")
        for collab in doc_only[:5]:  # Show top 5
            onedrive = collab.get('onedrive_direct_shares', 0) + collab.get('onedrive_group_shares', 0)
            teams_att = collab.get('teams_direct_attachments', 0) + collab.get('teams_group_attachments', 0)
            recency = collab.get('document_recency_label', 'N/A')
            safe_print(f"  • {collab['name']}: OneDrive={onedrive}, Teams={teams_att}, Last={recency}")
    
    # Biggest score changes
    safe_print(f"\n📈 Biggest Score Increases (due to document sharing):")
    score_changes = []
    for name in before_collabs.keys():
        if name in after_collabs:
            before_score = before_collabs[name]['importance_score']
            after_score = after_collabs[name]['importance_score']
            change = after_score - before_score
            if change > 0:
                doc_score = after_collabs[name].get('document_collaboration_score', 0)
                score_changes.append((name, change, doc_score, after_score))
    
    score_changes.sort(key=lambda x: x[1], reverse=True)
    for name, change, doc_score, final_score in score_changes[:5]:
        safe_print(f"  • {name:<30} +{change:5.2f} points (doc contribution: {doc_score:.2f}, new total: {final_score:.2f})")

def main():
    safe_print("=" * 60)
    safe_print("🧪 DOCUMENT COLLABORATION INTEGRATION TEST")
    safe_print("=" * 60)
    safe_print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Collect fresh document collaboration data
    safe_print("\n" + "="*60)
    safe_print("STEP 1: Collect Document Collaboration Data")
    safe_print("="*60)
    
    success, output = run_command(
        ['python', 'tools/document_collaboration_api.py', '--days', '365', '--max-files', '50', '--max-chats', '50'],
        "Collecting document collaboration data (OneDrive + Teams chat attachments)"
    )
    
    if not success:
        safe_print("❌ Failed to collect document data. Aborting test.")
        return 1
    
    # Find the latest document collaboration file
    doc_file = get_latest_file('data/evaluation_results/document_collaboration_analysis_*.json')
    if not doc_file:
        safe_print("❌ No document collaboration file found. Aborting test.")
        return 1
    
    safe_print(f"✅ Document data saved: {doc_file}")
    
    # Load document data to show summary
    doc_data = load_results(doc_file)
    safe_print(f"\n📊 Document Collaboration Summary:")
    safe_print(f"   Collaborators found: {len(doc_data['collaborators'])}")
    
    # Calculate totals from collaborators
    total_onedrive = sum(c.get('direct_shares', 0) + c.get('small_group_shares', 0) for c in doc_data['collaborators'])
    total_teams = sum(c.get('chat_direct', 0) + c.get('chat_group', 0) for c in doc_data['collaborators'])
    
    safe_print(f"   OneDrive shares analyzed: {total_onedrive}")
    safe_print(f"   Teams chat attachments: {total_teams}")
    
    # Step 2: Run collaborator discovery WITH document integration
    safe_print("\n" + "="*60)
    safe_print("STEP 2: Run Collaborator Discovery WITH Document Integration")
    safe_print("="*60)
    
    success, output = run_command(
        ['python', 'tools/collaborator_discovery.py'],
        "Running collaborator discovery with document integration"
    )
    
    if not success:
        safe_print("❌ Failed to run collaborator discovery. Check the error above.")
        return 1
    
    # Find the latest collaborator discovery file
    after_file = get_latest_file('collaborator_discovery_results_*.json')
    if not after_file:
        safe_print("❌ No collaborator discovery file found. Aborting test.")
        return 1
    
    safe_print(f"✅ Results saved: {after_file}")
    
    # Step 3: Load a previous run for comparison (if exists)
    safe_print("\n" + "="*60)
    safe_print("STEP 3: Compare with Previous Run (if available)")
    safe_print("="*60)
    
    # Get all discovery files and find the second most recent
    all_files = sorted(Path('.').glob('collaborator_discovery_results_*.json'), 
                      key=lambda x: x.stat().st_mtime, reverse=True)
    
    if len(all_files) < 2:
        safe_print("⚠️ No previous run found for comparison.")
        safe_print("   This is the first run with document integration.")
        safe_print(f"\n✅ Test completed! Check results in: {after_file}")
        return 0
    
    before_file = str(all_files[1])  # Second most recent
    
    safe_print(f"📊 Comparing:")
    safe_print(f"   BEFORE: {before_file}")
    safe_print(f"   AFTER:  {after_file}")
    
    # Load both files
    before = load_results(before_file)
    after = load_results(after_file)
    
    # Compare rankings
    compare_rankings(before, after)
    
    safe_print(f"\n{'='*60}")
    safe_print("✅ TEST COMPLETED!")
    safe_print(f"{'='*60}")
    safe_print(f"Results files:")
    safe_print(f"  • Document data: {doc_file}")
    safe_print(f"  • Before: {before_file}")
    safe_print(f"  • After: {after_file}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
