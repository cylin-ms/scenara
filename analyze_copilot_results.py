import json
from collections import Counter

# Load all three experiments
copilot = json.load(open('experiments/2025-10-28/meeting_classification_github_copilot.json', 'r'))

print("\n" + "=" * 75)
print("  GITHUB COPILOT CLASSIFICATION RESULTS (Centralized Prompt)")
print("=" * 75)

print("\nCATEGORY DISTRIBUTION:")
print("-" * 75)
cats = [m['classification']['primary_category'] for m in copilot['meetings']]
for cat, count in Counter(cats).most_common():
    print(f"  {cat}: {count} meetings ({count/8*100:.0f}%)")

print("\nSPECIFIC TYPE DISTRIBUTION:")
print("-" * 75)
types = [m['classification']['specific_type'] for m in copilot['meetings']]
for typ, count in Counter(types).most_common():
    print(f"  {typ}: {count} meetings")

avg_conf = sum(m['classification']['confidence'] for m in copilot['meetings']) / 8
print(f"\nAverage Confidence: {avg_conf:.1%}")
print("=" * 75 + "\n")
