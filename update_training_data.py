#!/usr/bin/env python3
"""
Update Training Data with ContextFlow Integration
Combines all data sources including GUTT v4.0 ACRUE framework
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
import shutil

class ContextFlowTrainingDataUpdater:
    def __init__(self):
        self.data_dir = "meeting_prep_data"
        self.backup_dir = "meeting_prep_data/backups"
        self.output_file = f"{self.data_dir}/training_scenarios.json"
        
    def backup_existing_data(self):
        """Backup existing training data"""
        if os.path.exists(self.output_file):
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.backup_dir}/training_scenarios_{timestamp}.json"
            shutil.copy2(self.output_file, backup_file)
            print(f"📦 Backed up existing data to {backup_file}")
    
    def load_mevals_data(self) -> List[Dict]:
        """Load MEvals data if available"""
        mevals_file = f"{self.data_dir}/mevals_scenarios.json"
        if os.path.exists(mevals_file):
            with open(mevals_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} MEvals scenarios")
                return data
        print("📂 MEvals data not found (skipping)")
        return []
    
    def load_enhanced_data(self) -> List[Dict]:
        """Load enhanced synthetic data"""
        enhanced_file = f"{self.data_dir}/enhanced_scenarios.json"
        if os.path.exists(enhanced_file):
            with open(enhanced_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} enhanced scenarios")
                return data
        print("📂 Enhanced data not found (skipping)")
        return []
    
    def load_contextflow_data(self) -> List[Dict]:
        """Load ContextFlow enhanced data with GUTT v4.0 ACRUE framework"""
        contextflow_file = f"{self.data_dir}/enhanced_contextflow_scenarios.json"
        if os.path.exists(contextflow_file):
            with open(contextflow_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"🎯 Loaded {len(data)} ContextFlow enhanced scenarios (GUTT v4.0)")
                return data
        print("🎯 ContextFlow data not found (skipping)")
        return []
    
    def load_graph_api_data(self) -> List[Dict]:
        """Load Microsoft Graph API data (both generated and real calendar data)"""
        all_graph_data = []
        
        # Load generated graph data
        graph_file = f"{self.data_dir}/graph_api_scenarios.json"
        if os.path.exists(graph_file):
            with open(graph_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_graph_data.extend(data)
                print(f"📂 Loaded {len(data)} generated Graph API scenarios")
        
        # Load real calendar data
        real_calendar_file = f"{self.data_dir}/real_calendar_scenarios.json"
        if os.path.exists(real_calendar_file):
            with open(real_calendar_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_graph_data.extend(data)
                print(f"📂 Loaded {len(data)} REAL calendar scenarios")
        
        if not all_graph_data:
            print("📂 No Graph API data found (skipping)")
        
        return all_graph_data
    
    def load_template_data(self) -> List[Dict]:
        """Load template scenarios"""
        template_file = f"{self.data_dir}/template_scenarios.json"
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} template scenarios")
                return data
        print("📂 Template data not found (skipping)")
        return []
    
    def normalize_scenario(self, scenario: Dict, source: str) -> Dict:
        """Normalize scenario format across all sources"""
        normalized = {
            'id': scenario.get('id', f"{source}_{datetime.now().timestamp()}"),
            'source': scenario.get('source', source),
            'context': {},
            'meeting_type': scenario.get('meeting_type', 'General Business Meeting'),
            'preparation_requirements': scenario.get('preparation_requirements', []),
            'complexity': scenario.get('complexity', 'medium'),
            'quality_score': scenario.get('quality_score', 7.0),
            'last_updated': datetime.now().isoformat()
        }
        
        # Normalize context based on source
        if source == 'contextflow':
            # ContextFlow data has enhanced structure with GUTT framework
            normalized.update({
                'framework': 'GUTT_v4.0_ACRUE',
                'enterprise_taxonomy': scenario.get('contextflow_integration', {}).get('enterprise_taxonomy', {}),
                'acrue_scores': scenario.get('contextflow_integration', {}).get('acrue_scores', {}),
                'gutt_tasks': scenario.get('contextflow_integration', {}).get('recommended_gutt_tasks', [])
            })
            normalized['context'] = scenario.get('context', {})
            normalized['quality_score'] = scenario.get('quality_score', 9.0)  # ContextFlow has high quality
        elif source in ['mevals', 'microsoft_calendar_manual']:
            normalized['context'] = {
                'subject': scenario.get('subject', '') or scenario.get('context', {}).get('subject', ''),
                'description': scenario.get('bodyPreview', '') or scenario.get('context', {}).get('description', ''),
                'attendees': scenario.get('attendees', []) or scenario.get('context', {}).get('attendees', []),
                'attendee_count': len(scenario.get('attendees', []) or scenario.get('context', {}).get('attendees', [])),
                'duration_minutes': scenario.get('duration_minutes', 60) or scenario.get('context', {}).get('duration_minutes', 60),
                'is_online_meeting': scenario.get('isOnlineMeeting', False) or scenario.get('context', {}).get('is_online_meeting', False),
                'importance': scenario.get('importance', 'normal') or scenario.get('context', {}).get('importance', 'normal')
            }
        elif source == 'graph_api':
            normalized['context'] = scenario.get('context', {})
        elif source in ['enhanced', 'template']:
            normalized['context'] = scenario.get('context', {})
        
        return normalized
    
    def analyze_dataset(self, scenarios: List[Dict]) -> Dict[str, Any]:
        """Analyze the combined dataset"""
        analysis = {
            'total_scenarios': len(scenarios),
            'sources': {},
            'meeting_types': {},
            'complexity_distribution': {},
            'quality_scores': {
                'average': 0.0,
                'min': 10.0,
                'max': 0.0,
                'high_quality': 0  # 8.0+
            }
        }
        
        quality_scores = []
        
        for scenario in scenarios:
            # Source distribution
            source = scenario.get('source', 'unknown')
            analysis['sources'][source] = analysis['sources'].get(source, 0) + 1
            
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
        
        if quality_scores:
            analysis['quality_scores']['average'] = sum(quality_scores) / len(quality_scores)
            analysis['quality_scores']['min'] = min(quality_scores)
            analysis['quality_scores']['max'] = max(quality_scores)
        
        return analysis
    
    def deduplicate_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
        """Remove duplicate scenarios based on subject and content similarity"""
        unique_scenarios = []
        seen_subjects = set()
        
        for scenario in scenarios:
            context = scenario.get('context', {})
            subject = context.get('subject', '').strip().lower()
            
            # Create a simple hash for deduplication
            content_hash = f"{subject}_{context.get('attendee_count', 0)}_{scenario.get('meeting_type', '')}"
            
            if content_hash not in seen_subjects:
                seen_subjects.add(content_hash)
                unique_scenarios.append(scenario)
            else:
                print(f"🔄 Skipping duplicate: {subject[:50]}...")
        
        print(f"🔄 Deduplicated: {len(scenarios)} → {len(unique_scenarios)} scenarios")
        return unique_scenarios
    
    def save_training_data(self, scenarios: List[Dict], analysis: Dict):
        """Save combined training data with metadata"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Save main training data
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        # Save analysis metadata
        analysis_file = f"{self.data_dir}/training_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(scenarios)} training scenarios to {self.output_file}")
        print(f"📊 Saved dataset analysis to {analysis_file}")
    
    def update_training_data(self):
        """Main function to update training data"""
        print("🔄 Updating Meeting PromptCoT Training Data")
        print("-" * 50)
        
        # Backup existing data
        self.backup_existing_data()
        
        # Load all data sources
        print("\n📂 Loading data sources:")
        all_scenarios = []
        
        # Load ContextFlow data first (highest priority)
        contextflow_data = self.load_contextflow_data()
        all_scenarios.extend([self.normalize_scenario(s, 'contextflow') for s in contextflow_data])
        
        # Load MEvals data
        mevals_data = self.load_mevals_data()
        all_scenarios.extend([self.normalize_scenario(s, 'mevals') for s in mevals_data])
        
        # Load Graph API data
        graph_data = self.load_graph_api_data()
        all_scenarios.extend([self.normalize_scenario(s, 'graph_api') for s in graph_data])
        
        # Load enhanced data
        enhanced_data = self.load_enhanced_data()
        all_scenarios.extend([self.normalize_scenario(s, 'enhanced') for s in enhanced_data])
        
        # Load template data
        template_data = self.load_template_data()
        all_scenarios.extend([self.normalize_scenario(s, 'template') for s in template_data])
        
        print(f"\n📊 Total scenarios before deduplication: {len(all_scenarios)}")
        
        # Deduplicate
        unique_scenarios = self.deduplicate_scenarios(all_scenarios)
        
        # Analyze dataset
        analysis = self.analyze_dataset(unique_scenarios)
        
        # Save combined data
        self.save_training_data(unique_scenarios, analysis)
        
        # Print summary
        self.print_summary(analysis)
    
    def print_summary(self, analysis: Dict):
        """Print dataset summary"""
        print("\n📊 Dataset Summary:")
        print(f"Total scenarios: {analysis['total_scenarios']}")
        print(f"Average quality score: {analysis['quality_scores']['average']:.2f}/10.0")
        print(f"High quality scenarios (8.0+): {analysis['quality_scores']['high_quality']}")
        
        print("\n📍 Data Sources:")
        for source, count in analysis['sources'].items():
            percentage = (count / analysis['total_scenarios']) * 100
            print(f"  - {source}: {count} ({percentage:.1f}%)")
        
        print("\n🏢 Meeting Types:")
        for meeting_type, count in sorted(analysis['meeting_types'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {meeting_type}: {count}")
        
        print("\n⚡ Complexity Distribution:")
        for complexity, count in analysis['complexity_distribution'].items():
            percentage = (count / analysis['total_scenarios']) * 100
            print(f"  - {complexity}: {count} ({percentage:.1f}%)")
        
        print(f"\n✅ Training data updated successfully!")
        print(f"📁 Location: {self.output_file}")

def main():
    """Main execution function"""
    updater = ContextFlowTrainingDataUpdater()
    updater.update_training_data()
    
    print("\n🎯 Next Steps:")
    print("1. Launch Streamlit interface: streamlit run meeting_data_explorer.py")
    print("2. Access: http://localhost:8501")
    print("3. View your combined dataset in the 'Training Data' tab")

if __name__ == "__main__":
    main()