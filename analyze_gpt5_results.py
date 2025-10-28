import json
from collections import Counter

# Load GPT-5 results
data = json.load(open('experiments/2025-10-28/meeting_classification_gpt5.json', 'r', encoding='utf-8'))

# Extract categories and types
categories = [m['classification']['primary_category'] for m in data['meetings']]
types = [m['classification']['specific_type'] for m in data['meetings']]

print("\n" + "=" * 75)
print("  GPT-5 CLASSIFICATION RESULTS (With Centralized Prompt)")
print("=" * 75)

print("\nCATEGORY DISTRIBUTION:")
print("-" * 75)
for cat, count in Counter(categories).most_common():
    print(f"  {cat}: {count} meetings ({count/8*100:.0f}%)")

print("\nSPECIFIC TYPE DISTRIBUTION:")
print("-" * 75)
for typ, count in Counter(types).most_common():
    print(f"  {typ}: {count} meetings")

print("\n" + "=" * 75)
print(f"Total: {len(data['meetings'])} meetings")
print(f"Average Confidence: {sum(m['classification']['confidence'] for m in data['meetings']) / len(data['meetings']):.1%}")
print("=" * 75 + "\n")
