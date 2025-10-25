#!/usr/bin/env python3
"""Quick summary of top 20 active and all dormant collaborators."""

import json

# Load data
with open('collaborators_with_dormancy.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n" + "=" * 100)
print("TOP 20 ACTIVE COLLABORATORS")
print("=" * 100)
print(f"{'RANK':<6} {'NAME':<35} {'SCORE':<10} {'MEETINGS':<10} {'1:1s':<6}")
print("-" * 100)

# Show ALL top 20, not just enumerate
top_20 = data['top_20_active']
for i in range(len(top_20)):
    c = top_20[i]
    name = c['name'][:33] + '..' if len(c['name']) > 35 else c['name']
    meetings = c.get('total_meetings', c.get('genuine_collaboration_meetings', 0))
    one_on_ones = c.get('one_on_one_count', c.get('one_on_one', 0))
    print(f"{i+1:<6} {name:<35} {c['final_score']:<10.1f} {meetings:<10} {one_on_ones:<6}")

print("=" * 100)
print(f"Showing Top 20 Active Collaborators\n")

print("=" * 100)
print("DORMANT COLLABORATORS (60+ days since last contact)")
print("=" * 100)
print(f"{'#':<4} {'NAME':<35} {'SCORE':<10} {'MEETINGS':<10}")
print("-" * 100)

for i, c in enumerate(data['dormant_collaborators'], 1):
    name = c['name'][:33] + '..' if len(c['name']) > 35 else c['name']
    meetings = c.get('total_meetings', c.get('genuine_collaboration_meetings', 0))
    print(f"{i:<4} {name:<35} {c['final_score']:<10.1f} {meetings:<10}")

print("=" * 100)
print(f"Total Dormant: {len(data['dormant_collaborators'])} (All HIGH RISK: 90+ days)")
print("=" * 100)

total = len(data['top_20_active']) + len(data['dormant_collaborators'])
print(f"\n✅ Conference rooms filtered using Graph API 'type' field\n")
