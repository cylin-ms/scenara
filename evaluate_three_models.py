#!/usr/bin/env python3
"""
Three-Model GUTT Evaluation: Claude vs GPT-5 v2 vs Ollama

Evaluates all three models against the reference GUTT decompositions
using proper precision, recall, and F1 metrics.

Reference source: Hero_Prompts_Reference_GUTT_Decompositions.md
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class EvaluationMetrics:
    """Metrics for GUTT evaluation"""
    precision: float
    recall: float
    f1_score: float
    gutt_count: int
    reference_count: int
    matches: int
    
def load_model_gutts(filepath: Path) -> List[str]:
    """Load GUTT names from model output file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            gutts = data.get('gutts', [])
            return [g.get('name', '').lower().strip() for g in gutts if g.get('name')]
    except:
        return []

# Reference GUTT counts from Hero_Prompts_Reference_GUTT_Decompositions.md
REFERENCE_GUTTS = {
    'organizer-1': 6,
    'organizer-2': 7,
    'organizer-3': 8,
    'schedule-1': 7,
    'schedule-2': 8,
    'schedule-3': 9,
    'collaborate-1': 6,
    'collaborate-2': 7,
    'collaborate-3': 8
}

# Reference GUTT names (ground truth from documentation)
REFERENCE_GUTT_NAMES = {
    'organizer-1': [
        'priority definition & extraction',
        'calendar event retrieval',
        'meeting-priority alignment scoring',
        'accept/decline decision logic',
        'calendar action execution',
        'decision justification & reporting'
    ],
    'organizer-2': [
        'calendar data retrieval',
        'meeting importance classification',
        'preparation time estimation',
        'meeting flagging logic',
        'calendar gap analysis',
        'focus time block scheduling',
        'actionable recommendations & reporting'
    ],
    'organizer-3': [
        'calendar historical data retrieval',
        'meeting categorization & classification',
        'time aggregation & statistical analysis',
        'priority alignment assessment',
        'low-value meeting identification',
        'time reclamation opportunity analysis',
        'schedule optimization recommendations',
        'time usage reporting & visualization'
    ],
    # Note: schedule-* and collaborate-* reference GUTTs would need to be extracted
    # from the full documentation. Using counts only for now.
}

def calculate_metrics(model_gutts: List[str], reference_gutts: List[str]) -> EvaluationMetrics:
    """
    Calculate precision, recall, and F1 for GUTT decomposition.
    
    Uses fuzzy matching on GUTT names since exact matches are unlikely.
    A match occurs if key concepts overlap significantly.
    """
    model_count = len(model_gutts)
    ref_count = len(reference_gutts)
    
    if model_count == 0 or ref_count == 0:
        return EvaluationMetrics(0, 0, 0, model_count, ref_count, 0)
    
    # Simple matching: check if reference GUTT concepts appear in model GUTT
    matches = 0
    matched_model = set()
    matched_ref = set()
    
    for ref_idx, ref_gutt in enumerate(reference_gutts):
        ref_words = set(ref_gutt.split())
        best_match_score = 0
        best_match_idx = -1
        
        for model_idx, model_gutt in enumerate(model_gutts):
            if model_idx in matched_model:
                continue
            model_words = set(model_gutt.split())
            # Jaccard similarity
            intersection = len(ref_words & model_words)
            union = len(ref_words | model_words)
            score = intersection / union if union > 0 else 0
            
            if score > best_match_score:
                best_match_score = score
                best_match_idx = model_idx
        
        # Match if similarity > 30%
        if best_match_score > 0.3:
            matches += 1
            matched_model.add(best_match_idx)
            matched_ref.add(ref_idx)
    
    precision = matches / model_count if model_count > 0 else 0
    recall = matches / ref_count if ref_count > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return EvaluationMetrics(precision, recall, f1, model_count, ref_count, matches)

def evaluate_all_models():
    """Evaluate Claude, GPT-5 v2, and Ollama against reference"""
    
    analysis_dir = Path('hero_prompt_analysis')
    
    print("=" * 100)
    print("THREE-MODEL GUTT EVALUATION: Claude vs GPT-5 v2 vs Ollama")
    print("=" * 100)
    print("\nEvaluating against Reference GUTT Decompositions (Ground Truth)")
    print("=" * 100)
    
    # Results storage
    results = {
        'claude': {},
        'gpt5': {},
        'ollama': {}
    }
    
    total_claude = {'count': 0, 'ref': 0, 'perfect_matches': 0}
    total_gpt5 = {'count': 0, 'ref': 0, 'perfect_matches': 0}
    total_ollama = {'count': 0, 'ref': 0, 'perfect_matches': 0}
    
    for prompt_id in REFERENCE_GUTTS.keys():
        ref_count = REFERENCE_GUTTS[prompt_id]
        ref_names = REFERENCE_GUTT_NAMES.get(prompt_id, [])
        
        # Load model outputs
        claude_gutts = load_model_gutts(analysis_dir / f"claude_gutt_{prompt_id}.json")
        gpt5_gutts = load_model_gutts(analysis_dir / f"gpt5_gutt_{prompt_id}.json")
        ollama_gutts = load_model_gutts(analysis_dir / f"ollama_gutt_{prompt_id}.json")
        
        # For prompts with reference names, do detailed evaluation
        if ref_names:
            claude_metrics = calculate_metrics(claude_gutts, ref_names)
            gpt5_metrics = calculate_metrics(gpt5_gutts, ref_names)
            ollama_metrics = calculate_metrics(ollama_gutts, ref_names)
        else:
            # Count-based evaluation only
            claude_metrics = EvaluationMetrics(0, 0, 0, len(claude_gutts), ref_count, 0)
            gpt5_metrics = EvaluationMetrics(0, 0, 0, len(gpt5_gutts), ref_count, 0)
            ollama_metrics = EvaluationMetrics(0, 0, 0, len(ollama_gutts), ref_count, 0)
        
        # Track perfect matches (exact count)
        if len(claude_gutts) == ref_count:
            total_claude['perfect_matches'] += 1
        if len(gpt5_gutts) == ref_count:
            total_gpt5['perfect_matches'] += 1
        if len(ollama_gutts) == ref_count:
            total_ollama['perfect_matches'] += 1
        
        total_claude['count'] += len(claude_gutts)
        total_claude['ref'] += ref_count
        total_gpt5['count'] += len(gpt5_gutts)
        total_gpt5['ref'] += ref_count
        total_ollama['count'] += len(ollama_gutts)
        total_ollama['ref'] += ref_count
        
        results['claude'][prompt_id] = claude_metrics
        results['gpt5'][prompt_id] = gpt5_metrics
        results['ollama'][prompt_id] = ollama_metrics
    
    # Print summary table
    print("\n" + "=" * 100)
    print(f"{'Prompt ID':<20} {'Ref':>5} {'Claude':>7} {'GPT-5':>7} {'Ollama':>7} {'Best Model':<15}")
    print("-" * 100)
    
    for prompt_id in REFERENCE_GUTTS.keys():
        ref = REFERENCE_GUTTS[prompt_id]
        claude_c = results['claude'][prompt_id].gutt_count
        gpt5_c = results['gpt5'][prompt_id].gutt_count
        ollama_c = results['ollama'][prompt_id].gutt_count
        
        # Determine best (closest to reference)
        claude_diff = abs(claude_c - ref)
        gpt5_diff = abs(gpt5_c - ref)
        ollama_diff = abs(ollama_c - ref)
        min_diff = min(claude_diff, gpt5_diff, ollama_diff)
        
        best = []
        if claude_diff == min_diff:
            best.append("Claude")
        if gpt5_diff == min_diff:
            best.append("GPT-5")
        if ollama_diff == min_diff:
            best.append("Ollama")
        best_str = " & ".join(best) if best else "-"
        
        # Mark perfect matches with ✅
        claude_str = f"{claude_c}{'✅' if claude_c == ref else ''}"
        gpt5_str = f"{gpt5_c}{'✅' if gpt5_c == ref else ''}"
        ollama_str = f"{ollama_c}{'✅' if ollama_c == ref else ''}"
        
        print(f"{prompt_id:<20} {ref:>5} {claude_str:>7} {gpt5_str:>7} {ollama_str:>7} {best_str:<15}")
    
    print("-" * 100)
    print(f"{'TOTALS':<20} {total_claude['ref']:>5} {total_claude['count']:>7} {total_gpt5['count']:>7} {total_ollama['count']:>7}")
    print(f"{'Perfect Matches':<20} {'-':>5} {total_claude['perfect_matches']:>7} {total_gpt5['perfect_matches']:>7} {total_ollama['perfect_matches']:>7}")
    
    # Overall statistics
    print("\n" + "=" * 100)
    print("OVERALL STATISTICS")
    print("=" * 100)
    
    print(f"\n{'Model':<15} {'Total GUTTs':>12} {'Reference':>12} {'Difference':>12} {'Perfect Matches':>16} {'Accuracy':>10}")
    print("-" * 100)
    
    for model_name, total_data in [('Claude', total_claude), ('GPT-5 v2', total_gpt5), ('Ollama', total_ollama)]:
        diff = total_data['count'] - total_data['ref']
        accuracy = (9 - abs(diff) / 9) if diff == 0 else total_data['perfect_matches'] / 9
        
        print(f"{model_name:<15} {total_data['count']:>12} {total_data['ref']:>12} {diff:>+12} {total_data['perfect_matches']:>16} {accuracy:>9.1%}")
    
    print("\n" + "=" * 100)
    print("KEY FINDINGS")
    print("=" * 100)
    
    # Determine winner
    models_data = [
        ('Claude', total_claude),
        ('GPT-5 v2', total_gpt5),
        ('Ollama', total_ollama)
    ]
    
    # Sort by perfect matches (primary), then by closeness to total (secondary)
    models_ranked = sorted(models_data, key=lambda x: (x[1]['perfect_matches'], -abs(x[1]['count'] - x[1]['ref'])), reverse=True)
    
    print(f"\n🏆 WINNER: {models_ranked[0][0]}")
    print(f"   - {models_ranked[0][1]['perfect_matches']}/9 perfect prompt matches")
    print(f"   - Total GUTTs: {models_ranked[0][1]['count']} (Reference: {models_ranked[0][1]['ref']})")
    
    print(f"\n🥈 SECOND: {models_ranked[1][0]}")
    print(f"   - {models_ranked[1][1]['perfect_matches']}/9 perfect prompt matches")
    print(f"   - Total GUTTs: {models_ranked[1][1]['count']} (Reference: {models_ranked[1][1]['ref']})")
    
    print(f"\n🥉 THIRD: {models_ranked[2][0]}")
    print(f"   - {models_ranked[2][1]['perfect_matches']}/9 perfect prompt matches")
    print(f"   - Total GUTTs: {models_ranked[2][1]['count']} (Reference: {models_ranked[2][1]['ref']})")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    evaluate_all_models()
