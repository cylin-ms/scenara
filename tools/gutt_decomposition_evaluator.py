#!/usr/bin/env python3
"""
GUTT Decomposition Evaluator - Interactive UX Tool

Compare and evaluate GUTT decomposition results from different sources
(human analysis, Claude, Ollama, GPT-4, etc.)

Features:
- Side-by-side comparison of GUTT decompositions
- Interactive scoring and evaluation
- Visual diff highlighting
- Export comparison reports
- Consensus analysis across multiple evaluators
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class GUTTQuality(Enum):
    """ACRUE quality levels"""
    EXCEPTIONAL = 4
    STRONG = 3
    ADEQUATE = 2
    POOR = 1


@dataclass
class GUTTTask:
    """Represents a single GUTT (unit task)"""
    id: str
    name: str
    capability: str
    required_skills: List[str]
    user_goal: str
    triggered: bool = False
    evidence: Optional[str] = None
    
    # ACRUE scores
    accurate: Optional[int] = None
    complete: Optional[int] = None
    relevant: Optional[int] = None
    useful: Optional[int] = None
    exceptional: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class GUTTDecomposition:
    """Complete GUTT decomposition from a source"""
    source: str
    timestamp: str
    original_prompt: str
    gutts: List[GUTTTask]
    track1_score: Optional[float] = None
    track2_score: Optional[float] = None
    overall_score: Optional[float] = None
    notes: str = ""
    is_reference: bool = False  # Mark as ground truth reference
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'source': self.source,
            'timestamp': self.timestamp,
            'original_prompt': self.original_prompt,
            'gutts': [g.to_dict() for g in self.gutts],
            'track1_score': self.track1_score,
            'track2_score': self.track2_score,
            'overall_score': self.overall_score,
            'notes': self.notes
        }


class GUTTDecompositionEvaluator:
    """Interactive UX tool for evaluating GUTT decompositions"""
    
    def __init__(self):
        """Initialize evaluator"""
        self.decompositions: List[GUTTDecomposition] = []
        self.comparison_results: Dict[str, Any] = {}
    
    def load_decomposition(self, file_path: str) -> GUTTDecomposition:
        """Load decomposition from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        gutts = [GUTTTask(**g) for g in data['gutts']]
        
        decomp = GUTTDecomposition(
            source=data['source'],
            timestamp=data['timestamp'],
            original_prompt=data['original_prompt'],
            gutts=gutts,
            track1_score=data.get('track1_score'),
            track2_score=data.get('track2_score'),
            overall_score=data.get('overall_score'),
            notes=data.get('notes')
        )
        
        return decomp
    
    def save_decomposition(self, decomposition: GUTTDecomposition, file_path: str):
        """Save decomposition to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(decomposition.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"✅ Saved decomposition to: {file_path}")
    
    def add_decomposition(self, decomposition: GUTTDecomposition):
        """Add decomposition for comparison"""
        self.decompositions.append(decomposition)
        print(f"✅ Added decomposition from: {decomposition.source}")
    
    def compare_decompositions(self) -> Dict[str, Any]:
        """Compare all loaded decompositions"""
        if len(self.decompositions) < 2:
            print("⚠️  Need at least 2 decompositions to compare")
            return {}
        
        # Analyze GUTT alignment
        all_gutt_names = set()
        for decomp in self.decompositions:
            for gutt in decomp.gutts:
                all_gutt_names.add(gutt.name)
        
        # Build comparison matrix
        comparison = {
            'total_unique_gutts': len(all_gutt_names),
            'sources': [d.source for d in self.decompositions],
            'gutt_coverage': {},
            'score_comparison': {},
            'consensus_gutts': [],
            'divergent_gutts': []
        }
        
        # Check which sources identified which GUTTs
        for gutt_name in all_gutt_names:
            sources_with_gutt = []
            for decomp in self.decompositions:
                if any(g.name == gutt_name for g in decomp.gutts):
                    sources_with_gutt.append(decomp.source)
            
            coverage = len(sources_with_gutt) / len(self.decompositions)
            comparison['gutt_coverage'][gutt_name] = {
                'sources': sources_with_gutt,
                'coverage_ratio': coverage
            }
            
            # Consensus if >50% agreement
            if coverage > 0.5:
                comparison['consensus_gutts'].append(gutt_name)
            else:
                comparison['divergent_gutts'].append(gutt_name)
        
        # Compare scores
        for decomp in self.decompositions:
            comparison['score_comparison'][decomp.source] = {
                'track1': decomp.track1_score,
                'track2': decomp.track2_score,
                'overall': decomp.overall_score,
                'num_gutts': len(decomp.gutts)
            }
        
        self.comparison_results = comparison
        return comparison
    
    def print_comparison_report(self):
        """Print formatted comparison report"""
        if not self.comparison_results:
            print("⚠️  No comparison results available. Run compare_decompositions() first.")
            return
        
        comp = self.comparison_results
        
        print("\n" + "=" * 80)
        print("📊 GUTT DECOMPOSITION COMPARISON REPORT")
        print("=" * 80)
        
        print(f"\n🔍 Analyzing {len(self.decompositions)} decompositions:")
        for source in comp['sources']:
            print(f"   • {source}")
        
        print(f"\n📋 Total Unique GUTTs Identified: {comp['total_unique_gutts']}")
        
        # Consensus GUTTs
        if comp['consensus_gutts']:
            print(f"\n✅ CONSENSUS GUTTs ({len(comp['consensus_gutts'])} - agreed by >50% of sources):")
            for i, gutt_name in enumerate(comp['consensus_gutts'], 1):
                coverage = comp['gutt_coverage'][gutt_name]
                sources = ", ".join(coverage['sources'])
                ratio = coverage['coverage_ratio'] * 100
                print(f"   {i}. {gutt_name}")
                print(f"      Coverage: {ratio:.0f}% ({sources})")
        
        # Divergent GUTTs
        if comp['divergent_gutts']:
            print(f"\n⚠️  DIVERGENT GUTTs ({len(comp['divergent_gutts'])} - identified by <50% of sources):")
            for i, gutt_name in enumerate(comp['divergent_gutts'], 1):
                coverage = comp['gutt_coverage'][gutt_name]
                sources = ", ".join(coverage['sources'])
                ratio = coverage['coverage_ratio'] * 100
                print(f"   {i}. {gutt_name}")
                print(f"      Coverage: {ratio:.0f}% ({sources})")
        
        # Score comparison
        print(f"\n📊 SCORE COMPARISON:")
        print(f"{'Source':<20} {'GUTTs':<8} {'Track 1':<10} {'Track 2':<10} {'Overall':<10}")
        print("-" * 80)
        for source, scores in comp['score_comparison'].items():
            t1 = f"{scores['track1']:.2f}" if scores['track1'] else "N/A"
            t2 = f"{scores['track2']:.2f}" if scores['track2'] else "N/A"
            overall = f"{scores['overall']:.2f}" if scores['overall'] else "N/A"
            print(f"{source:<20} {scores['num_gutts']:<8} {t1:<10} {t2:<10} {overall:<10}")
        
        print("\n" + "=" * 80)
    
    def print_side_by_side_comparison(self, gutt_name: str):
        """Print detailed side-by-side comparison for a specific GUTT"""
        print(f"\n{'=' * 80}")
        print(f"🔍 DETAILED COMPARISON: {gutt_name}")
        print("=" * 80)
        
        for decomp in self.decompositions:
            gutt = next((g for g in decomp.gutts if g.name == gutt_name), None)
            
            print(f"\n📌 Source: {decomp.source}")
            if gutt:
                print(f"   ✅ IDENTIFIED")
                print(f"   Capability: {gutt.capability}")
                print(f"   Required Skills: {', '.join(gutt.required_skills)}")
                print(f"   User Goal: {gutt.user_goal}")
                print(f"   Triggered: {'Yes' if gutt.triggered else 'No'}")
                if gutt.evidence:
                    print(f"   Evidence: {gutt.evidence}")
                
                # ACRUE scores if available
                if gutt.accurate:
                    print(f"   ACRUE Scores:")
                    print(f"      Accurate: {gutt.accurate}/4")
                    print(f"      Complete: {gutt.complete}/4")
                    print(f"      Relevant: {gutt.relevant}/4")
                    print(f"      Useful: {gutt.useful}/4")
                    print(f"      Exceptional: {gutt.exceptional}/4")
            else:
                print(f"   ❌ NOT IDENTIFIED")
        
        print("\n" + "=" * 80)
    
    def compare_to_reference(self, llm_decomp: GUTTDecomposition, 
                            reference_decomp: GUTTDecomposition) -> Dict[str, Any]:
        """
        Compare LLM decomposition against ground truth reference
        
        Args:
            llm_decomp: Decomposition from LLM to evaluate
            reference_decomp: Ground truth reference decomposition
            
        Returns:
            Comparison metrics including precision, recall, F1
        """
        ref_gutts = {g.name.lower(): g for g in reference_decomp.gutts}
        llm_gutts = {g.name.lower(): g for g in llm_decomp.gutts}
        
        # Find matches (exact or fuzzy)
        matches = []
        llm_matched = set()
        ref_matched = set()
        
        for ref_name, ref_gutt in ref_gutts.items():
            for llm_name, llm_gutt in llm_gutts.items():
                if llm_name in llm_matched:
                    continue
                    
                # Check for exact match or high similarity
                if ref_name == llm_name or self._similar_names(ref_name, llm_name):
                    matches.append({
                        'reference': ref_gutt.name,
                        'llm': llm_gutt.name,
                        'similarity': 1.0 if ref_name == llm_name else 0.8
                    })
                    llm_matched.add(llm_name)
                    ref_matched.add(ref_name)
                    break
        
        # Calculate metrics
        true_positives = len(matches)
        false_positives = len(llm_gutts) - true_positives
        false_negatives = len(ref_gutts) - true_positives
        
        precision = true_positives / len(llm_gutts) if llm_gutts else 0
        recall = true_positives / len(ref_gutts) if ref_gutts else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Granularity assessment
        granularity_ratio = len(llm_gutts) / len(ref_gutts) if ref_gutts else 0
        if granularity_ratio < 0.5:
            granularity_assessment = "Too Coarse (significant under-decomposition)"
        elif granularity_ratio < 0.8:
            granularity_assessment = "Somewhat Coarse (moderate under-decomposition)"
        elif granularity_ratio <= 1.2:
            granularity_assessment = "Appropriate (within acceptable range)"
        elif granularity_ratio <= 1.5:
            granularity_assessment = "Somewhat Fine (moderate over-decomposition)"
        else:
            granularity_assessment = "Too Fine (significant over-decomposition)"
        
        # Missing GUTTs
        missing_gutts = [g.name for name, g in ref_gutts.items() if name not in ref_matched]
        
        # Extra GUTTs
        extra_gutts = [g.name for name, g in llm_gutts.items() if name not in llm_matched]
        
        return {
            'llm_source': llm_decomp.source,
            'reference_source': reference_decomp.source,
            'metrics': {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'true_positives': true_positives,
                'false_positives': false_positives,
                'false_negatives': false_negatives
            },
            'granularity': {
                'reference_count': len(ref_gutts),
                'llm_count': len(llm_gutts),
                'ratio': granularity_ratio,
                'assessment': granularity_assessment
            },
            'matches': matches,
            'missing_gutts': missing_gutts,
            'extra_gutts': extra_gutts,
            'coverage_percentage': (true_positives / len(ref_gutts) * 100) if ref_gutts else 0
        }
    
    def _similar_names(self, name1: str, name2: str) -> bool:
        """Check if two GUTT names are similar (fuzzy match)"""
        # Simple similarity: check if one contains key words from the other
        words1 = set(name1.split())
        words2 = set(name2.split())
        
        # Remove common words
        common_words = {'and', 'the', 'a', 'an', 'of', 'for', 'to', 'in', 'with'}
        words1 = words1 - common_words
        words2 = words2 - common_words
        
        if not words1 or not words2:
            return False
        
        # Check overlap
        overlap = len(words1 & words2)
        min_size = min(len(words1), len(words2))
        
        return overlap / min_size >= 0.5
    
    def print_reference_comparison(self, comparison: Dict[str, Any]):
        """Print formatted reference comparison results"""
        print("\n" + "=" * 80)
        print("📊 REFERENCE COMPARISON RESULTS")
        print("=" * 80)
        
        print(f"\n🎯 Evaluating: {comparison['llm_source']}")
        print(f"📚 Reference: {comparison['reference_source']}")
        
        # Metrics
        metrics = comparison['metrics']
        print(f"\n📈 Performance Metrics:")
        print(f"   Precision: {metrics['precision']:.2%} ({metrics['true_positives']}/{metrics['true_positives'] + metrics['false_positives']} correct)")
        print(f"   Recall:    {metrics['recall']:.2%} ({metrics['true_positives']}/{metrics['true_positives'] + metrics['false_negatives']} found)")
        print(f"   F1 Score:  {metrics['f1_score']:.2%}")
        print(f"   Coverage:  {comparison['coverage_percentage']:.1f}% of reference GUTTs identified")
        
        # Granularity
        gran = comparison['granularity']
        print(f"\n🔍 Granularity Assessment:")
        print(f"   Reference GUTTs: {gran['reference_count']}")
        print(f"   LLM GUTTs:       {gran['llm_count']}")
        print(f"   Ratio:           {gran['ratio']:.2f}x")
        print(f"   Assessment:      {gran['assessment']}")
        
        # Matches
        if comparison['matches']:
            print(f"\n✅ Matched GUTTs ({len(comparison['matches'])}):")
            for match in comparison['matches']:
                print(f"   • {match['reference']}")
                if match['similarity'] < 1.0:
                    print(f"     ≈ {match['llm']} (fuzzy match)")
        
        # Missing
        if comparison['missing_gutts']:
            print(f"\n❌ Missing GUTTs ({len(comparison['missing_gutts'])}):")
            for gutt in comparison['missing_gutts']:
                print(f"   • {gutt}")
        
        # Extra
        if comparison['extra_gutts']:
            print(f"\n➕ Extra GUTTs ({len(comparison['extra_gutts'])}):")
            for gutt in comparison['extra_gutts']:
                print(f"   • {gutt}")
        
        print("\n" + "=" * 80)
    
    def export_comparison_report(self, output_file: str):
        """Export comparison to JSON file"""
        if not self.comparison_results:
            print("⚠️  No comparison results. Run compare_decompositions() first.")
            return
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'decompositions': [d.to_dict() for d in self.decompositions],
            'comparison': self.comparison_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Comparison report exported to: {output_file}")
    
    def interactive_mode(self):
        """Interactive mode for evaluating decompositions"""
        print("\n" + "=" * 80)
        print("🎯 GUTT DECOMPOSITION EVALUATOR - Interactive Mode")
        print("=" * 80)
        
        while True:
            print("\n📋 Options:")
            print("   1. Load decomposition from file")
            print("   2. View loaded decompositions")
            print("   3. Compare decompositions")
            print("   4. View detailed GUTT comparison")
            print("   5. Export comparison report")
            print("   6. Clear all decompositions")
            print("   0. Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                file_path = input("Enter decomposition file path: ").strip()
                try:
                    decomp = self.load_decomposition(file_path)
                    self.add_decomposition(decomp)
                except Exception as e:
                    print(f"❌ Error loading file: {e}")
            
            elif choice == '2':
                print(f"\n📚 Loaded Decompositions ({len(self.decompositions)}):")
                for i, decomp in enumerate(self.decompositions, 1):
                    print(f"   {i}. {decomp.source} - {len(decomp.gutts)} GUTTs - {decomp.timestamp}")
            
            elif choice == '3':
                if len(self.decompositions) < 2:
                    print("⚠️  Need at least 2 decompositions to compare")
                else:
                    self.compare_decompositions()
                    self.print_comparison_report()
            
            elif choice == '4':
                if not self.comparison_results:
                    print("⚠️  Run comparison first (option 3)")
                else:
                    print("\n📋 Available GUTTs:")
                    all_gutts = list(self.comparison_results['gutt_coverage'].keys())
                    for i, gutt in enumerate(all_gutts, 1):
                        print(f"   {i}. {gutt}")
                    
                    idx = input("\nSelect GUTT number: ").strip()
                    try:
                        gutt_name = all_gutts[int(idx) - 1]
                        self.print_side_by_side_comparison(gutt_name)
                    except (ValueError, IndexError):
                        print("❌ Invalid selection")
            
            elif choice == '5':
                output = input("Enter output file path (default: gutt_comparison.json): ").strip()
                if not output:
                    output = "gutt_comparison.json"
                self.export_comparison_report(output)
            
            elif choice == '6':
                self.decompositions.clear()
                self.comparison_results.clear()
                print("✅ All decompositions cleared")
            
            elif choice == '0':
                print("\n👋 Exiting GUTT Decomposition Evaluator")
                break
            
            else:
                print("❌ Invalid option")


def create_sample_decomposition(prompt: str, source: str, output_file: str):
    """Helper to create a sample decomposition JSON template"""
    
    decomp = GUTTDecomposition(
        source=source,
        timestamp=datetime.now().isoformat(),
        original_prompt=prompt,
        gutts=[
            GUTTTask(
                id="gutt_1",
                name="Example GUTT Task",
                capability="Describe the capability",
                required_skills=["skill_1", "skill_2"],
                user_goal="What the user wants to achieve",
                triggered=True,
                evidence="Evidence that this GUTT was executed",
                accurate=4,
                complete=4,
                relevant=4,
                useful=4,
                exceptional=4
            )
        ],
        track1_score=1.0,
        track2_score=4.0,
        overall_score=4.0,
        notes="Optional notes about this decomposition"
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(decomp.to_dict(), f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sample decomposition template created: {output_file}")
    print(f"   Edit this file and use it as a template for your evaluations")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GUTT Decomposition Evaluator')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Launch interactive mode')
    parser.add_argument('--create-template', metavar='FILE',
                       help='Create sample decomposition template')
    parser.add_argument('--compare', nargs='+', metavar='FILE',
                       help='Compare multiple decomposition files')
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Output file for comparison report')
    parser.add_argument('--prompt', metavar='TEXT',
                       help='Original prompt for template creation')
    parser.add_argument('--source', metavar='NAME', default='unknown',
                       help='Source name for template creation')
    
    args = parser.parse_args()
    
    evaluator = GUTTDecompositionEvaluator()
    
    if args.create_template:
        prompt = args.prompt or "Your prompt here"
        create_sample_decomposition(prompt, args.source, args.create_template)
    
    elif args.compare:
        # Load all files
        for file_path in args.compare:
            try:
                decomp = evaluator.load_decomposition(file_path)
                evaluator.add_decomposition(decomp)
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        # Compare and report
        if len(evaluator.decompositions) >= 2:
            evaluator.compare_decompositions()
            evaluator.print_comparison_report()
            
            if args.output:
                evaluator.export_comparison_report(args.output)
        else:
            print("⚠️  Need at least 2 valid decomposition files to compare")
    
    elif args.interactive:
        evaluator.interactive_mode()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
