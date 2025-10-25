#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick comparison of before/after document integration"""

import json

before = json.load(open('collaborator_discovery_results_20251026_002212.json'))
after = json.load(open('collaborator_discovery_results_20251026_014224.json'))

print('\n' + '='*70)
print('📊 DOCUMENT COLLABORATION INTEGRATION - BEFORE/AFTER COMPARISON')
print('='*70)

print(f'\n🔵 BEFORE: {before["algorithm_version"]}')
print(f'   Total Collaborators: {before["total_collaborators_found"]}')
print(f'   Data Sources: Calendar + Graph API + Teams Chat')

print(f'\n🟢 AFTER: {after["algorithm_version"]}')
print(f'   Total Collaborators: {after["total_collaborators_found"]}')
print(f'   Data Sources: Calendar + Graph API + Teams Chat + DOCUMENTS')

print(f'\n{"="*70}')
print('TOP 5 COLLABORATORS COMPARISON')
print('='*70)

print('\n🔵 BEFORE (without enhanced document tracking):')
for i, c in enumerate(before['collaborators'][:5], 1):
    print(f'  {i}. {c["name"]:<30} Score: {c["importance_score"]:6.2f}')

print('\n🟢 AFTER (with OneDrive + Teams chat attachment tracking):')
for i, c in enumerate(after['collaborators'][:5], 1):
    onedrive_d = c.get('onedrive_direct_shares', 0)
    onedrive_g = c.get('onedrive_group_shares', 0)
    teams_d = c.get('teams_direct_attachments', 0)
    teams_g = c.get('teams_group_attachments', 0)
    doc_score = c.get('document_collaboration_score', 0)
    sharing_days = c.get('sharing_days', 0)
    recency = c.get('document_recency_label', 'N/A')
    
    print(f'  {i}. {c["name"]:<30} Score: {c["importance_score"]:6.2f}')
    print(f'     📄 OneDrive: {onedrive_d} direct, {onedrive_g} group')
    print(f'     💬 Teams: {teams_d} direct, {teams_g} group')
    print(f'     📅 Sharing: {sharing_days} days, last {recency}')
    print(f'     ➕ Document contribution: +{doc_score} points')

print(f'\n{"="*70}')
print('KEY INSIGHTS')
print('='*70)

# Find people who benefited most from document scoring
score_increases = []
before_dict = {c['name']: c for c in before['collaborators']}
for c in after['collaborators']:
    if c['name'] in before_dict:
        old_score = before_dict[c['name']]['importance_score']
        new_score = c['importance_score']
        doc_score = c.get('document_collaboration_score', 0)
        if doc_score > 0:
            score_increases.append({
                'name': c['name'],
                'old_score': old_score,
                'new_score': new_score,
                'increase': new_score - old_score,
                'doc_contribution': doc_score,
                'total_shares': c.get('total_document_shares', 0)
            })

score_increases.sort(key=lambda x: x['doc_contribution'], reverse=True)

print('\n✨ TOP BENEFICIARIES from Document Collaboration Tracking:')
for item in score_increases[:5]:
    print(f'\n  • {item["name"]}')
    print(f'    Old score: {item["old_score"]:.2f} → New score: {item["new_score"]:.2f} (change: {item["increase"]:+.2f})')
    print(f'    Document contribution: +{item["doc_contribution"]} points')
    print(f'    Total documents shared: {item["total_shares"]}')

# Check for rank changes
print(f'\n📊 RANK CHANGES in Top 10:')
before_top10 = {c['name']: i+1 for i, c in enumerate(before['collaborators'][:10])}
after_top10_list = after['collaborators'][:10]

for i, c in enumerate(after_top10_list, 1):
    name = c['name']
    if name in before_top10:
        old_rank = before_top10[name]
        if old_rank != i:
            direction = '⬆️' if old_rank > i else '⬇️'
            change = abs(old_rank - i)
            print(f'  {direction} {name}: #{old_rank} → #{i} ({change} positions)')

print('\n' + '='*70)
print('✅ INTEGRATION SUCCESSFUL!')
print('='*70)
print('\n📌 Document collaboration now tracks:')
print('   • OneDrive permissions (direct 1:1 and small group <5)')
print('   • Teams chat file attachments (direct and group)')  
print('   • Temporal scoring (recency and continuity bonuses)')
print('   • Filtering (self-sharing and former employees)')
print('\n💡 This provides a more complete picture of collaboration beyond meetings!')
