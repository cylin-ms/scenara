#!/usr/bin/env python3
"""
Real Calendar Data Only - Analysis Generator
Creates training data using ONLY your real Microsoft calendar events
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class RealDataOnlyProcessor:
    def __init__(self):
        self.data_dir = "meeting_prep_data"
        self.backup_dir = "meeting_prep_data/backups"
        self.output_file = f"{self.data_dir}/training_scenarios.json"
        
    def backup_existing_data(self):
        """Backup existing training data"""
        if os.path.exists(self.output_file):
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.backup_dir}/training_scenarios_mixed_{timestamp}.json"
            os.rename(self.output_file, backup_file)
            print(f"📦 Backed up mixed data to {backup_file}")
    
    def load_real_calendar_data(self) -> List[Dict]:
        """Load ONLY real calendar data"""
        real_calendar_file = f"{self.data_dir}/real_calendar_scenarios.json"
        if os.path.exists(real_calendar_file):
            with open(real_calendar_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} REAL calendar scenarios")
                return data
        else:
            print("❌ Real calendar data not found!")
            print("Please run: python3 process_manual_calendar.py first")
            return []
    
    def analyze_real_dataset(self, scenarios: List[Dict]) -> Dict[str, Any]:
        """Analyze your real calendar data"""
        analysis = {
            'total_scenarios': len(scenarios),
            'data_source': 'real_calendar_only',
            'meeting_types': {},
            'complexity_distribution': {},
            'quality_scores': {
                'average': 0.0,
                'min': 10.0,
                'max': 0.0,
                'high_quality': 0
            },
            'temporal_patterns': {},
            'meeting_insights': {}
        }
        
        quality_scores = []
        durations = []
        attendee_counts = []
        
        for scenario in scenarios:
            # Meeting type distribution
            meeting_type = scenario.get('meeting_type', 'Unknown')
            analysis['meeting_types'][meeting_type] = analysis['meeting_types'].get(meeting_type, 0) + 1
            
            # Complexity distribution
            complexity = scenario.get('complexity', 'unknown')
            analysis['complexity_distribution'][complexity] = analysis['complexity_distribution'].get(complexity, 0) + 1
            
            # Quality scores
            quality = float(scenario.get('quality_score', 0))
            quality_scores.append(quality)
            if quality >= 8.0:
                analysis['quality_scores']['high_quality'] += 1
            
            # Meeting patterns
            context = scenario.get('context', {})
            duration = context.get('duration_minutes', 60)
            attendee_count = context.get('attendee_count', 0)
            
            durations.append(duration)
            attendee_counts.append(attendee_count)
        
        if quality_scores:
            analysis['quality_scores']['average'] = sum(quality_scores) / len(quality_scores)
            analysis['quality_scores']['min'] = min(quality_scores)
            analysis['quality_scores']['max'] = max(quality_scores)
        
        # Meeting insights
        if durations:
            analysis['meeting_insights']['avg_duration'] = sum(durations) / len(durations)
            analysis['meeting_insights']['avg_attendees'] = sum(attendee_counts) / len(attendee_counts)
            analysis['meeting_insights']['total_meeting_hours'] = sum(durations) / 60
        
        return analysis
    
    def save_real_data_only(self, scenarios: List[Dict], analysis: Dict):
        """Save ONLY real calendar data as training data"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Save main training data (real only)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        # Save analysis metadata
        analysis_file = f"{self.data_dir}/real_data_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(scenarios)} REAL scenarios to {self.output_file}")
        print(f"📊 Saved real data analysis to {analysis_file}")
    
    def process_real_data_only(self):
        """Main function to create real-data-only training set"""
        print("🎯 Creating Real Calendar Data Only Training Set")
        print("-" * 55)
        
        # Backup existing mixed data
        self.backup_existing_data()
        
        # Load only real calendar data
        print("\n📂 Loading REAL calendar data:")
        real_scenarios = self.load_real_calendar_data()
        
        if not real_scenarios:
            print("❌ No real calendar data found. Exiting.")
            return
        
        print(f"\n📊 Processing {len(real_scenarios)} real meeting scenarios")
        
        # Analyze real dataset
        analysis = self.analyze_real_dataset(real_scenarios)
        
        # Save real data only
        self.save_real_data_only(real_scenarios, analysis)
        
        # Print summary
        self.print_real_data_summary(analysis)
    
    def print_real_data_summary(self, analysis: Dict):
        """Print real data summary"""
        print("\n🎯 REAL CALENDAR DATA SUMMARY:")
        print(f"Total meetings: {analysis['total_scenarios']}")
        print(f"Data source: 100% Real Microsoft Calendar")
        print(f"Average quality score: {analysis['quality_scores']['average']:.2f}/10.0")
        print(f"High quality meetings (8.0+): {analysis['quality_scores']['high_quality']}")
        
        print("\n📊 YOUR MEETING PATTERNS:")
        
        print("\n🏢 Meeting Types (from your calendar):")
        for meeting_type, count in sorted(analysis['meeting_types'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / analysis['total_scenarios']) * 100
            print(f"  - {meeting_type}: {count} ({percentage:.1f}%)")
        
        print("\n⚡ Complexity Distribution:")
        for complexity, count in analysis['complexity_distribution'].items():
            percentage = (count / analysis['total_scenarios']) * 100
            print(f"  - {complexity}: {count} ({percentage:.1f}%)")
        
        insights = analysis.get('meeting_insights', {})
        if insights:
            print("\n📈 Meeting Insights:")
            print(f"  - Average meeting duration: {insights.get('avg_duration', 0):.0f} minutes")
            print(f"  - Average attendees per meeting: {insights.get('avg_attendees', 0):.1f}")
            print(f"  - Total meeting time analyzed: {insights.get('total_meeting_hours', 0):.1f} hours")
        
        print(f"\n✅ Real data training set created successfully!")
        print(f"📁 Location: {self.output_file}")

def main():
    """Main execution function"""
    processor = RealDataOnlyProcessor()
    processor.process_real_data_only()
    
    print("\n🎯 Next Steps:")
    print("1. Refresh Streamlit interface (it will auto-reload)")
    print("2. Access: http://localhost:8501")
    print("3. View your REAL meeting patterns in the interface")
    print("\n💡 Your interface now shows 100% real Microsoft calendar data!")

if __name__ == "__main__":
    main()