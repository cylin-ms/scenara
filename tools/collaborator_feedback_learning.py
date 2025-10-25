#!/usr/bin/env python3
"""
Collaborator Feedback Learning System
Scenara 2.0 - Enterprise Meeting Intelligence

AI-Native Feedback System for Collaborator Discovery
====================================================
This module implements an intelligent feedback system that:
1. Explains ranking decisions transparently
2. Captures user corrections and feedback
3. Analyzes discrepancies to identify data source gaps
4. Suggests improvements and learns from mistakes
5. Avoids simple manual overrides - focuses on root cause analysis

Philosophy:
- AI should explain WHY it made decisions
- AI should identify what data is missing
- AI should learn from corrections
- Users teach the system, not override it

Example Flow:
User: "Why isn't Xiaodong Liu in my top 10?"
System: "I found only 4 meetings with Xiaodong, all large broadcasts (150+ people).
         This suggests 0% genuine collaboration, so he was filtered out.
         
         Possible issues:
         - Calendar data incomplete (only 50 events loaded)
         - Recent 1:1 meetings not in dataset
         - Teams chat collaboration not captured (need Chat.Read permission)
         
         Can you describe your actual collaboration with Xiaodong?"
         
User: "We co-organized a workshop and have regular 1:1s"
System: "Thank you! This reveals DATA GAP:
         - Workshop co-organization not in calendar data
         - Regular 1:1s missing from dataset
         
         Action items:
         ✓ Re-run Graph API extractor for fresh calendar data
         ✓ Request additional permissions (Meeting.Read.All)
         ✓ Log this case for algorithm training
         
         I'll remember: Broadcast-only patterns may indicate data gaps, not lack of collaboration"
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class FeedbackEntry:
    """User feedback about a collaborator ranking"""
    timestamp: str
    collaborator_name: str
    expected_rank: Optional[int]  # What user expected
    actual_rank: Optional[int]     # What system produced
    user_comment: str
    system_analysis: Dict[str, Any]
    data_gaps_identified: List[str]
    action_items: List[str]
    learning_points: List[str]

@dataclass
class DataGapAnalysis:
    """Analysis of missing or incomplete data sources"""
    gap_type: str  # 'missing_meetings', 'missing_chat', 'missing_documents', 'permission_denied'
    affected_collaborators: List[str]
    evidence: str
    suggested_fix: str
    severity: str  # 'critical', 'high', 'medium', 'low'

class CollaboratorFeedbackLearning:
    """
    Intelligent feedback system for collaborator discovery.
    Focuses on explanation, learning, and data gap identification.
    """
    
    def __init__(self, feedback_log_file: str = "data/evaluation_results/collaborator_feedback_log.json"):
        self.feedback_log_file = Path(feedback_log_file)
        self.feedback_log_file.parent.mkdir(parents=True, exist_ok=True)
        self.feedback_entries: List[FeedbackEntry] = []
        self.data_gaps: List[DataGapAnalysis] = []
        self._load_feedback_log()
    
    def _load_feedback_log(self):
        """Load existing feedback log"""
        if self.feedback_log_file.exists():
            try:
                with open(self.feedback_log_file, 'r') as f:
                    data = json.load(f)
                    self.feedback_entries = [
                        FeedbackEntry(**entry) for entry in data.get('feedback_entries', [])
                    ]
                    self.data_gaps = [
                        DataGapAnalysis(**gap) for gap in data.get('data_gaps', [])
                    ]
            except Exception as e:
                print(f"⚠️ Warning: Could not load feedback log: {e}")
    
    def _save_feedback_log(self):
        """Save feedback log to file"""
        data = {
            'last_updated': datetime.now().isoformat(),
            'total_feedback_entries': len(self.feedback_entries),
            'total_data_gaps': len(self.data_gaps),
            'feedback_entries': [asdict(entry) for entry in self.feedback_entries],
            'data_gaps': [asdict(gap) for gap in self.data_gaps]
        }
        with open(self.feedback_log_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def explain_ranking(self, collaborator_name: str, ranking_data: Dict[str, Any], 
                       all_collaborators: List[Dict[str, Any]]) -> str:
        """
        Explain why a collaborator was ranked at their position.
        
        Args:
            collaborator_name: Name of the collaborator
            ranking_data: Data about this collaborator's ranking
            all_collaborators: List of all ranked collaborators for context
            
        Returns:
            Human-readable explanation
        """
        if not ranking_data:
            return self._explain_not_found(collaborator_name, all_collaborators)
        
        explanation = [
            f"\n📊 RANKING EXPLANATION: {collaborator_name}",
            "=" * 70,
            f"Rank: #{ranking_data.get('rank', 'N/A')}",
            f"Importance Score: {ranking_data.get('importance_score', 0):.2f}",
            f"Confidence: {ranking_data.get('confidence_score', 0):.1%}",
            "",
            "🔍 COLLABORATION EVIDENCE:",
        ]
        
        # Meeting analysis
        total_meetings = ranking_data.get('total_meetings', 0)
        genuine_meetings = ranking_data.get('genuine_meetings', 0)
        genuine_ratio = (genuine_meetings / total_meetings * 100) if total_meetings > 0 else 0
        
        explanation.append(f"  • Total meetings: {total_meetings}")
        explanation.append(f"  • Genuine collaboration meetings: {genuine_meetings} ({genuine_ratio:.0f}%)")
        
        # Meeting type breakdown
        one_on_ones = ranking_data.get('one_on_one_count', 0)
        organized = ranking_data.get('organized_count', 0)
        working = ranking_data.get('working_sessions_count', 0)
        
        if one_on_ones > 0:
            explanation.append(f"  • 1:1 meetings: {one_on_ones}")
        if organized > 0:
            explanation.append(f"  • Meetings you organized: {organized}")
        if working > 0:
            explanation.append(f"  • Working sessions attended: {working}")
        
        # Graph API verification
        graph_rank = ranking_data.get('graph_api_rank')
        if graph_rank:
            explanation.append(f"  • Microsoft Graph API rank: #{graph_rank} (ML-verified collaboration)")
        
        # Document sharing
        shared_docs = ranking_data.get('shared_documents_count', 0)
        if shared_docs > 0:
            explanation.append(f"  • Shared documents: {shared_docs}")
        
        explanation.append("")
        explanation.append("💡 SCORING BREAKDOWN:")
        explanation.append(f"  • Collaboration activities (30%): {ranking_data.get('activity_points', 0):.1f} points")
        explanation.append(f"  • Interaction quality (25%): {ranking_data.get('quality_points', 0):.1f} points")
        explanation.append(f"  • Confidence level (20%): {ranking_data.get('confidence_points', 0):.1f} points")
        explanation.append(f"  • Graph API ranking (15%): {ranking_data.get('graph_points', 0):.1f} points")
        explanation.append(f"  • Time consistency (10%): {ranking_data.get('consistency_points', 0):.1f} points")
        explanation.append(f"  • Document sharing (5%): {ranking_data.get('document_points', 0):.1f} points")
        
        return "\n".join(explanation)
    
    def _explain_not_found(self, collaborator_name: str, all_collaborators: List[Dict[str, Any]]) -> str:
        """Explain why a collaborator is not in the ranked list"""
        explanation = [
            f"\n❌ {collaborator_name} NOT FOUND in ranked collaborators",
            "=" * 70,
            "",
            "🔍 POSSIBLE REASONS:",
            "  1. No meetings found in calendar data",
            "  2. Only broadcast meetings (filtered out as non-collaboration)",
            "  3. Name spelling mismatch in data",
            "  4. Data source incomplete or outdated",
            "",
            "📋 DATA SOURCES CHECKED:",
            "  • Calendar events",
            "  • Microsoft Graph API People rankings",
            "  • Document sharing records",
            ""
        ]
        
        # Check if similar names exist
        similar_names = self._find_similar_names(collaborator_name, all_collaborators)
        if similar_names:
            explanation.append("🔎 SIMILAR NAMES FOUND:")
            for name, rank in similar_names[:5]:
                explanation.append(f"  • {name} (Rank #{rank})")
            explanation.append("")
        
        explanation.append("💡 NEXT STEPS:")
        explanation.append("  1. Verify name spelling")
        explanation.append("  2. Check if calendar data is current")
        explanation.append("  3. Consider re-running Graph API extractor")
        explanation.append("  4. Provide feedback to identify data gaps")
        
        return "\n".join(explanation)
    
    def _find_similar_names(self, target_name: str, all_collaborators: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
        """Find collaborators with similar names"""
        target_parts = set(target_name.lower().split())
        similar = []
        
        for collab in all_collaborators:
            name = collab.get('name', '')
            name_parts = set(name.lower().split())
            
            # Check for any matching parts
            if target_parts & name_parts:
                similar.append((name, collab.get('rank', 999)))
        
        return sorted(similar, key=lambda x: x[1])
    
    def analyze_feedback(self, collaborator_name: str, user_comment: str,
                        expected_rank: Optional[int], actual_rank: Optional[int],
                        ranking_data: Dict[str, Any]) -> FeedbackEntry:
        """
        Analyze user feedback to identify data gaps and learning opportunities.
        
        This is the core AI-native learning function that:
        1. Analyzes discrepancy between user expectation and system output
        2. Identifies potential data source gaps
        3. Suggests concrete action items
        4. Captures learning points for future improvement
        
        Args:
            collaborator_name: Name of the collaborator
            user_comment: User's feedback/description of actual collaboration
            expected_rank: What rank user expected (optional)
            actual_rank: Actual rank produced by system (None if not found)
            ranking_data: System's ranking data for this collaborator
            
        Returns:
            FeedbackEntry with analysis and action items
        """
        # Analyze the discrepancy
        system_analysis = self._analyze_discrepancy(
            collaborator_name, user_comment, expected_rank, actual_rank, ranking_data
        )
        
        # Identify data gaps
        data_gaps = self._identify_data_gaps(user_comment, ranking_data)
        
        # Generate action items
        action_items = self._generate_action_items(data_gaps, ranking_data)
        
        # Extract learning points
        learning_points = self._extract_learning_points(
            user_comment, ranking_data, data_gaps
        )
        
        # Create feedback entry
        entry = FeedbackEntry(
            timestamp=datetime.now().isoformat(),
            collaborator_name=collaborator_name,
            expected_rank=expected_rank,
            actual_rank=actual_rank,
            user_comment=user_comment,
            system_analysis=system_analysis,
            data_gaps_identified=data_gaps,
            action_items=action_items,
            learning_points=learning_points
        )
        
        # Save to log
        self.feedback_entries.append(entry)
        self._save_feedback_log()
        
        return entry
    
    def _analyze_discrepancy(self, collaborator_name: str, user_comment: str,
                            expected_rank: Optional[int], actual_rank: Optional[int],
                            ranking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze why system ranking differs from user expectation"""
        analysis = {
            'discrepancy_type': None,
            'severity': 'unknown',
            'likely_cause': [],
            'system_perspective': '',
            'user_perspective': user_comment
        }
        
        if actual_rank is None:
            # Collaborator not found/ranked
            analysis['discrepancy_type'] = 'not_found'
            analysis['severity'] = 'critical'
            analysis['system_perspective'] = f"No collaboration evidence found for {collaborator_name}"
            
            if ranking_data and ranking_data.get('total_meetings', 0) > 0:
                # Found meetings but filtered out
                genuine_ratio = ranking_data.get('genuine_meetings', 0) / ranking_data.get('total_meetings', 1)
                if genuine_ratio == 0:
                    analysis['likely_cause'].append('All meetings are broadcasts (150+ attendees)')
                    analysis['likely_cause'].append('No small group or 1:1 collaboration detected')
        
        elif expected_rank and actual_rank > expected_rank:
            # Ranked lower than expected
            analysis['discrepancy_type'] = 'ranked_too_low'
            analysis['severity'] = 'high' if actual_rank - expected_rank > 10 else 'medium'
            analysis['system_perspective'] = f"Ranked at #{actual_rank} based on available data"
            
        # Analyze user comment for collaboration patterns
        comment_lower = user_comment.lower()
        
        if '1:1' in comment_lower or 'one-on-one' in comment_lower:
            if ranking_data.get('one_on_one_count', 0) == 0:
                analysis['likely_cause'].append('User mentions 1:1s but none found in calendar data')
        
        if 'chat' in comment_lower or 'teams' in comment_lower:
            analysis['likely_cause'].append('Teams chat collaboration mentioned but not captured (need Chat.Read)')
        
        if 'workshop' in comment_lower or 'co-organized' in comment_lower:
            if ranking_data.get('organized_count', 0) == 0:
                analysis['likely_cause'].append('Co-organization mentioned but not reflected in meeting data')
        
        if 'document' in comment_lower or 'shared' in comment_lower or 'docs' in comment_lower:
            if ranking_data.get('shared_documents_count', 0) == 0:
                analysis['likely_cause'].append('Document sharing mentioned but not detected')
        
        if 'recent' in comment_lower or 'recently' in comment_lower:
            analysis['likely_cause'].append('Recent collaboration mentioned - calendar data may be outdated')
        
        return analysis
    
    def _identify_data_gaps(self, user_comment: str, ranking_data: Dict[str, Any]) -> List[str]:
        """Identify specific data source gaps based on feedback"""
        gaps = []
        comment_lower = user_comment.lower()
        
        # Calendar data gaps
        if 'recent' in comment_lower or '1:1' in comment_lower:
            if not ranking_data or ranking_data.get('total_meetings', 0) < 5:
                gaps.append("Calendar data incomplete - missing recent meetings")
        
        # Teams chat gap
        if 'chat' in comment_lower or 'teams' in comment_lower or 'messaging' in comment_lower:
            gaps.append("Teams chat data not captured - need Chat.Read permission")
        
        # Document sharing gap
        if 'document' in comment_lower or 'shared' in comment_lower or 'files' in comment_lower:
            if ranking_data.get('shared_documents_count', 0) == 0:
                gaps.append("Document sharing incomplete - may need additional Graph API scopes")
        
        # Co-organization gap
        if 'co-organized' in comment_lower or 'workshop' in comment_lower:
            gaps.append("Meeting co-organization not fully captured in calendar data")
        
        # Email communication gap
        if 'email' in comment_lower:
            gaps.append("Email collaboration analysis incomplete")
        
        return gaps
    
    def _generate_action_items(self, data_gaps: List[str], ranking_data: Dict[str, Any]) -> List[str]:
        """Generate concrete action items to address data gaps"""
        actions = []
        
        for gap in data_gaps:
            if 'calendar data incomplete' in gap.lower():
                actions.append("✓ Re-run Graph API extractor to get fresh calendar events")
            
            if 'teams chat' in gap.lower():
                actions.append("✓ Request Chat.Read permission in Graph Explorer")
                actions.append("✓ Add Teams chat analysis to extraction pipeline")
            
            if 'document sharing' in gap.lower():
                actions.append("✓ Verify Files.Read.All scope in Graph API permissions")
                actions.append("✓ Check shared documents query is working correctly")
            
            if 'meeting co-organization' in gap.lower():
                actions.append("✓ Verify Meeting.Read.All permission includes organizer data")
                actions.append("✓ Check calendar event organizer field parsing")
        
        # Always suggest data verification
        if not actions:
            actions.append("✓ Verify all data sources are current and complete")
        
        # Add algorithm improvement suggestion
        actions.append("✓ Log this feedback for algorithm training and improvement")
        
        return actions
    
    def _extract_learning_points(self, user_comment: str, ranking_data: Dict[str, Any],
                                 data_gaps: List[str]) -> List[str]:
        """Extract learning points for future algorithm improvement"""
        learning = []
        
        # Pattern: Broadcast-only may indicate data gap, not lack of collaboration
        if ranking_data:
            total = ranking_data.get('total_meetings', 0)
            genuine = ranking_data.get('genuine_meetings', 0)
            if total > 0 and genuine == 0:
                learning.append(
                    "PATTERN: Broadcast-only attendance may indicate data gap, not absence of collaboration. "
                    "Check for: missing 1:1s, recent meetings, chat history."
                )
        
        # Pattern: User mentions collaboration types not in our data model
        comment_lower = user_comment.lower()
        collaboration_types = []
        if 'chat' in comment_lower:
            collaboration_types.append('Teams chat')
        if 'workshop' in comment_lower:
            collaboration_types.append('workshop co-organization')
        if 'ad hoc' in comment_lower:
            collaboration_types.append('ad hoc meetings')
        
        if collaboration_types:
            learning.append(
                f"COVERAGE GAP: User collaborates via {', '.join(collaboration_types)} "
                f"which are not fully captured in current data sources."
            )
        
        # Pattern: Recency matters
        if 'recent' in comment_lower:
            learning.append(
                "TEMPORAL: Recent collaboration is important to users. "
                "Ensure data sources are refreshed regularly."
            )
        
        # Data source priority
        if data_gaps:
            learning.append(
                f"DATA PRIORITY: Missing {len(data_gaps)} data sources. "
                f"Multi-source fusion is critical for accuracy."
            )
        
        return learning
    
    def print_feedback_analysis(self, entry: FeedbackEntry):
        """Print a formatted feedback analysis"""
        print("\n" + "=" * 70)
        print("🧠 AI-NATIVE FEEDBACK ANALYSIS")
        print("=" * 70)
        print(f"\nCollaborator: {entry.collaborator_name}")
        print(f"Timestamp: {entry.timestamp}")
        
        if entry.actual_rank:
            print(f"System Rank: #{entry.actual_rank}")
        else:
            print("System Rank: NOT FOUND")
        
        if entry.expected_rank:
            print(f"Expected Rank: #{entry.expected_rank}")
        
        print(f"\n💬 USER FEEDBACK:")
        print(f"  {entry.user_comment}")
        
        print(f"\n🔍 SYSTEM ANALYSIS:")
        analysis = entry.system_analysis
        print(f"  Discrepancy Type: {analysis.get('discrepancy_type', 'unknown')}")
        print(f"  Severity: {analysis.get('severity', 'unknown')}")
        print(f"\n  System Perspective: {analysis.get('system_perspective', 'N/A')}")
        
        if analysis.get('likely_cause'):
            print(f"\n  Likely Causes:")
            for cause in analysis['likely_cause']:
                print(f"    • {cause}")
        
        if entry.data_gaps_identified:
            print(f"\n🔴 DATA GAPS IDENTIFIED:")
            for gap in entry.data_gaps_identified:
                print(f"  • {gap}")
        
        if entry.action_items:
            print(f"\n✅ ACTION ITEMS:")
            for action in entry.action_items:
                print(f"  {action}")
        
        if entry.learning_points:
            print(f"\n📚 LEARNING POINTS:")
            for point in entry.learning_points:
                print(f"  • {point}")
        
        print("\n" + "=" * 70)
    
    def get_data_gap_summary(self) -> Dict[str, Any]:
        """Get summary of all identified data gaps"""
        gap_counts = defaultdict(int)
        affected_collaborators = defaultdict(set)
        
        for entry in self.feedback_entries:
            for gap in entry.data_gaps_identified:
                gap_counts[gap] += 1
                affected_collaborators[gap].add(entry.collaborator_name)
        
        return {
            'total_gaps': sum(gap_counts.values()),
            'unique_gap_types': len(gap_counts),
            'gap_frequency': dict(gap_counts),
            'affected_collaborators': {k: list(v) for k, v in affected_collaborators.items()},
            'top_gaps': sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def suggest_improvements(self) -> List[str]:
        """Suggest system improvements based on accumulated feedback"""
        suggestions = []
        gap_summary = self.get_data_gap_summary()
        
        if gap_summary['total_gaps'] > 0:
            suggestions.append("\n🎯 SYSTEM IMPROVEMENT SUGGESTIONS:")
            suggestions.append("Based on user feedback analysis:\n")
            
            for gap, count in gap_summary['top_gaps']:
                suggestions.append(f"  Priority {count}: {gap}")
                suggestions.append(f"    Affects: {', '.join(gap_summary['affected_collaborators'][gap])}\n")
        
        # Algorithm improvements
        learning_patterns = defaultdict(int)
        for entry in self.feedback_entries:
            for point in entry.learning_points:
                if ':' in point:
                    pattern_type = point.split(':')[0]
                    learning_patterns[pattern_type] += 1
        
        if learning_patterns:
            suggestions.append("\n📈 ALGORITHM LEARNING PATTERNS:")
            for pattern, count in sorted(learning_patterns.items(), key=lambda x: x[1], reverse=True):
                suggestions.append(f"  • {pattern}: {count} occurrences")
        
        return suggestions


def main():
    """Interactive command-line interface for feedback learning"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI-Native Feedback Learning System for Collaborator Discovery'
    )
    parser.add_argument('--collaborator', type=str, help='Collaborator name to provide feedback on')
    parser.add_argument('--comment', type=str, help='Your feedback comment')
    parser.add_argument('--expected-rank', type=int, help='Expected rank (optional)')
    parser.add_argument('--summary', action='store_true', help='Show data gap summary')
    
    args = parser.parse_args()
    
    learning_system = CollaboratorFeedbackLearning()
    
    if args.summary:
        # Show data gap summary
        gap_summary = learning_system.get_data_gap_summary()
        print("\n📊 DATA GAP SUMMARY")
        print("=" * 70)
        print(f"Total gaps identified: {gap_summary['total_gaps']}")
        print(f"Unique gap types: {gap_summary['unique_gap_types']}")
        print("\nTop Data Gaps:")
        for gap, count in gap_summary['top_gaps']:
            print(f"  {count}x: {gap}")
        
        # Show improvement suggestions
        suggestions = learning_system.suggest_improvements()
        for suggestion in suggestions:
            print(suggestion)
        
    elif args.collaborator and args.comment:
        # Process feedback
        # Note: In real usage, this would load actual ranking data
        print(f"\n🔍 Processing feedback for {args.collaborator}...")
        
        ranking_data = {}  # Would load from actual collaborator discovery results
        actual_rank = None  # Would get from results
        
        entry = learning_system.analyze_feedback(
            collaborator_name=args.collaborator,
            user_comment=args.comment,
            expected_rank=args.expected_rank,
            actual_rank=actual_rank,
            ranking_data=ranking_data
        )
        
        learning_system.print_feedback_analysis(entry)
        print("\n✅ Feedback logged for system learning")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
