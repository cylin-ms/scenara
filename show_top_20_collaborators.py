#!/usr/bin/env python3
"""
Show Top 20 Collaborators with GPT-4.1 Classification
Displays detailed evidence and ranking scores
"""

from tools.collaborator_discovery import CollaboratorDiscoveryTool
import json

def main():
    print("=" * 80)
    print("TOP 20 COLLABORATORS - LLM-Enhanced Classification")
    print("=" * 80)
    
    # Initialize with GPT-4.1 (default)
    print("\nInitializing Collaborator Discovery Tool...")
    print("Note: If rate limits hit, will automatically fall back to keyword classification")
    tool = CollaboratorDiscoveryTool()
    
    print(f"\nRunning discovery with {tool.llm_classifier_type}...")
    print("This may take a few minutes for large datasets...")
    print("-" * 80)
    
    # Run discovery
    results = tool.discover_collaborators()
    
    # Get top collaborators
    top_collaborators = results.get('top_collaborators', [])[:20]
    
    print(f"\n{'=' * 80}")
    print(f"TOP 20 COLLABORATORS (out of {len(results.get('top_collaborators', []))} total)")
    print(f"{'=' * 80}\n")
    
    for i, collab in enumerate(top_collaborators, 1):
        print(f"{'#' * 80}")
        print(f"RANK #{i}: {collab.get('name', 'Unknown')}")
        print(f"{'#' * 80}")
        
        # Ranking Score
        print(f"\n📊 RANKING SCORE: {collab.get('ranking_score', 0):.2f}")
        
        # Collaboration Metrics
        metrics = collab.get('collaboration_metrics', {})
        print(f"\n📈 COLLABORATION METRICS:")
        print(f"   Total Meetings: {metrics.get('total_meetings', 0)}")
        print(f"   Strategic Meetings: {metrics.get('strategic_meetings', 0)}")
        print(f"   Decision Meetings: {metrics.get('decision_meetings', 0)}")
        print(f"   One-on-One Meetings: {metrics.get('one_on_one_meetings', 0)}")
        print(f"   Collaboration Frequency: {metrics.get('collaboration_frequency', 'N/A')}")
        
        # Evidence
        evidence = collab.get('evidence', [])
        print(f"\n📋 EVIDENCE ({len(evidence)} meetings):")
        
        for j, ev in enumerate(evidence[:5], 1):  # Show first 5 pieces of evidence
            print(f"\n   [{j}] {ev.get('meeting_subject', 'No subject')}")
            print(f"       Date: {ev.get('meeting_date', 'N/A')}")
            print(f"       Type: {ev.get('meeting_type', 'Unknown')}")
            print(f"       Category: {ev.get('taxonomy_category', 'Unknown')}")
            print(f"       Attendees: {ev.get('attendee_count', 0)} people")
            print(f"       Role: {ev.get('role', 'N/A')}")
            
            # Show collaboration signals
            signals = ev.get('collaboration_signals', [])
            if signals:
                print(f"       Signals: {', '.join(signals[:3])}")
        
        if len(evidence) > 5:
            print(f"\n   ... and {len(evidence) - 5} more meetings")
        
        # Collaboration Strength
        strength = collab.get('collaboration_strength', 'N/A')
        print(f"\n💪 COLLABORATION STRENGTH: {strength}")
        
        # Recommended Actions
        recommendations = collab.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in recommendations[:3]:
                print(f"   • {rec}")
        
        print(f"\n{'-' * 80}\n")
    
    # Summary Statistics
    print(f"\n{'=' * 80}")
    print("SUMMARY STATISTICS")
    print(f"{'=' * 80}")
    print(f"Total Collaborators Found: {len(results.get('top_collaborators', []))}")
    print(f"LLM Classifier Used: {tool.llm_classifier_type}")
    print(f"Classification Accuracy: {results.get('metadata', {}).get('classification_accuracy', 'N/A')}")
    
    # Save detailed results
    output_file = "top_20_collaborators_gpt41.json"
    with open(output_file, 'w') as f:
        json.dump({
            'top_20': top_collaborators,
            'classifier': tool.llm_classifier_type,
            'total_found': len(results.get('top_collaborators', [])),
            'metadata': results.get('metadata', {})
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
