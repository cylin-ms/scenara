#!/usr/bin/env python3
"""
Separated Training Data Management System
Maintains distinct tracks for real vs synthetic data to preserve data integrity
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple
import shutil

class SeparatedTrainingDataManager:
    def __init__(self):
        self.data_dir = "meeting_prep_data"
        self.backup_dir = "meeting_prep_data/backups"
        
        # Separate output files for different data tracks
        self.real_data_file = f"{self.data_dir}/training_scenarios_real.json"
        self.synthetic_data_file = f"{self.data_dir}/training_scenarios_synthetic.json"
        self.combined_file = f"{self.data_dir}/training_scenarios_combined.json"
        self.analysis_file = f"{self.data_dir}/training_analysis_separated.json"
        
        # Data source categorization
        self.real_sources = {
            'microsoft_calendar_manual',  # Real calendar data manually curated
            'real_calendar',             # Real calendar data from Graph API
            'mevals'                     # Real meeting evaluation data
        }
        
        self.synthetic_sources = {
            'generated_sample',              # AI-generated synthetic scenarios
            'microsoft_calendar_contextflow', # ContextFlow enhanced synthetic data
            'graph_api',                    # Generated Graph API scenarios
            'enhanced',                     # Enhanced synthetic scenarios
            'template',                     # Template-based scenarios
            'contextflow'                   # Pure ContextFlow scenarios
        }
        
    def backup_existing_data(self):
        """Backup existing training data files"""
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        files_to_backup = [
            (self.real_data_file, f"training_scenarios_real_{timestamp}.json"),
            (self.synthetic_data_file, f"training_scenarios_synthetic_{timestamp}.json"),
            (self.combined_file, f"training_scenarios_combined_{timestamp}.json")
        ]
        
        for source_file, backup_name in files_to_backup:
            if os.path.exists(source_file):
                backup_file = f"{self.backup_dir}/{backup_name}"
                shutil.copy2(source_file, backup_file)
                print(f"📦 Backed up {os.path.basename(source_file)} to {backup_name}")
    
    def load_mevals_data(self) -> List[Dict]:
        """Load MEvals data (REAL)"""
        mevals_file = f"{self.data_dir}/mevals_scenarios.json"
        if os.path.exists(mevals_file):
            with open(mevals_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 [REAL] Loaded {len(data)} MEvals scenarios")
                return data
        print("📂 [REAL] MEvals data not found (skipping)")
        return []
    
    def load_enhanced_data(self) -> List[Dict]:
        """Load enhanced synthetic data (SYNTHETIC)"""
        enhanced_file = f"{self.data_dir}/enhanced_scenarios.json"
        if os.path.exists(enhanced_file):
            with open(enhanced_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 [SYNTHETIC] Loaded {len(data)} enhanced scenarios")
                return data
        print("📂 [SYNTHETIC] Enhanced data not found (skipping)")
        return []
    
    def load_contextflow_data(self) -> List[Dict]:
        """Load ContextFlow enhanced data (SYNTHETIC)"""
        contextflow_file = f"{self.data_dir}/enhanced_contextflow_scenarios.json"
        if os.path.exists(contextflow_file):
            with open(contextflow_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"🎯 [SYNTHETIC] Loaded {len(data)} ContextFlow enhanced scenarios (GUTT v4.0)")
                return data
        print("🎯 [SYNTHETIC] ContextFlow data not found (skipping)")
        return []
    
    def load_graph_api_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Load Microsoft Graph API data, separating real vs synthetic"""
        real_data = []
        synthetic_data = []
        
        # Load generated graph data (SYNTHETIC)
        graph_file = f"{self.data_dir}/graph_api_scenarios.json"
        if os.path.exists(graph_file):
            with open(graph_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                synthetic_data.extend(data)
                print(f"📂 [SYNTHETIC] Loaded {len(data)} generated Graph API scenarios")
        
        # Load real calendar data (REAL)
        real_calendar_file = f"{self.data_dir}/real_calendar_scenarios.json"
        if os.path.exists(real_calendar_file):
            with open(real_calendar_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                real_data.extend(data)
                print(f"📂 [REAL] Loaded {len(data)} real calendar scenarios")
        
        if not real_data and not synthetic_data:
            print("📂 No Graph API data found (skipping)")
        
        return real_data, synthetic_data
    
    def load_template_data(self) -> List[Dict]:
        """Load template scenarios (SYNTHETIC)"""
        template_file = f"{self.data_dir}/template_scenarios.json"
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 [SYNTHETIC] Loaded {len(data)} template scenarios")
                return data
        print("📂 [SYNTHETIC] Template data not found (skipping)")
        return []
    
    def categorize_by_source(self, scenario: Dict) -> str:
        """Categorize scenario as real or synthetic based on source"""
        source = scenario.get('source', 'unknown')
        
        if source in self.real_sources:
            return 'real'
        elif source in self.synthetic_sources:
            return 'synthetic'
        else:
            # Default categorization logic
            if 'real' in source.lower() or 'manual' in source.lower() or 'mevals' in source.lower():
                return 'real'
            else:
                return 'synthetic'
    
    def normalize_scenario(self, scenario: Dict, source: str, data_type: str) -> Dict:
        """Normalize scenario format with data type tracking"""
        normalized = {
            'id': scenario.get('id', f"{source}_{datetime.now().timestamp()}"),
            'source': scenario.get('source', source),
            'data_type': data_type,  # 'real' or 'synthetic'
            'context': {},
            'meeting_type': scenario.get('meeting_type', 'General Business Meeting'),
            'preparation_requirements': scenario.get('preparation_requirements', []),
            'complexity': scenario.get('complexity', 'medium'),
            'quality_score': scenario.get('quality_score', 7.0),
            'last_updated': datetime.now().isoformat()
        }
        
        # Add data provenance information
        normalized['data_provenance'] = {
            'is_real_data': data_type == 'real',
            'collection_method': self._determine_collection_method(source),
            'validation_level': self._determine_validation_level(source, data_type)
        }
        
        # Normalize context based on source (same as before)
        if source == 'contextflow' or 'contextflow' in source:
            normalized.update({
                'framework': 'GUTT_v4.0_ACRUE',
                'enterprise_taxonomy': scenario.get('contextflow_integration', {}).get('enterprise_taxonomy', {}),
                'acrue_scores': scenario.get('contextflow_integration', {}).get('acrue_scores', {}),
                'gutt_tasks': scenario.get('contextflow_integration', {}).get('recommended_gutt_tasks', [])
            })
            normalized['context'] = scenario.get('context', {})
            normalized['quality_score'] = scenario.get('quality_score', 9.0)
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
        else:
            normalized['context'] = scenario.get('context', {})
        
        return normalized
    
    def _determine_collection_method(self, source: str) -> str:
        """Determine how the data was collected"""
        if 'manual' in source:
            return 'manual_curation'
        elif 'graph_api' in source or 'calendar' in source:
            return 'api_extraction'
        elif 'generated' in source or 'contextflow' in source:
            return 'ai_generation'
        elif 'template' in source:
            return 'template_based'
        else:
            return 'unknown'
    
    def _determine_validation_level(self, source: str, data_type: str) -> str:
        """Determine validation level of the data"""
        if data_type == 'real':
            if 'manual' in source:
                return 'human_validated'
            else:
                return 'api_verified'
        else:  # synthetic
            if 'contextflow' in source:
                return 'llm_enhanced'
            elif 'generated' in source:
                return 'ai_generated'
            else:
                return 'template_based'
    
    def deduplicate_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
        """Remove duplicate scenarios within each track"""
        seen_content = set()
        deduplicated = []
        
        for scenario in scenarios:
            # Create a content hash for deduplication
            content_key = (
                scenario.get('context', {}).get('subject', '').lower().strip(),
                scenario.get('meeting_type', '').lower().strip(),
                scenario.get('source', '')
            )
            
            if content_key not in seen_content:
                seen_content.add(content_key)
                deduplicated.append(scenario)
            else:
                subject = scenario.get('context', {}).get('subject', 'Unknown')[:50]
                print(f"🔄 Skipping duplicate: {subject}...")
        
        return deduplicated
    
    def analyze_separated_dataset(self, real_data: List[Dict], synthetic_data: List[Dict]) -> Dict[str, Any]:
        """Analyze both real and synthetic datasets"""
        def analyze_track(data: List[Dict], track_name: str) -> Dict[str, Any]:
            if not data:
                return {}
                
            analysis = {
                'total_scenarios': len(data),
                'sources': {},
                'meeting_types': {},
                'complexity_distribution': {},
                'quality_scores': {
                    'average': 0.0,
                    'min': 10.0,
                    'max': 0.0,
                    'high_quality': 0
                }
            }
            
            quality_scores = []
            
            for scenario in data:
                # Source distribution
                source = scenario.get('source', 'unknown')
                analysis['sources'][source] = analysis['sources'].get(source, 0) + 1
                
                # Meeting type distribution
                meeting_type = scenario.get('meeting_type', 'Unknown')
                analysis['meeting_types'][meeting_type] = analysis['meeting_types'].get(meeting_type, 0) + 1
                
                # Complexity distribution
                complexity = scenario.get('complexity', 'medium')
                analysis['complexity_distribution'][complexity] = analysis['complexity_distribution'].get(complexity, 0) + 1
                
                # Quality scores
                score = scenario.get('quality_score', 7.0)
                quality_scores.append(score)
                if score >= 8.0:
                    analysis['quality_scores']['high_quality'] += 1
            
            if quality_scores:
                analysis['quality_scores']['average'] = sum(quality_scores) / len(quality_scores)
                analysis['quality_scores']['min'] = min(quality_scores)
                analysis['quality_scores']['max'] = max(quality_scores)
            
            return analysis
        
        real_analysis = analyze_track(real_data, 'real')
        synthetic_analysis = analyze_track(synthetic_data, 'synthetic')
        
        combined_analysis = {
            'separation_summary': {
                'real_data_count': len(real_data),
                'synthetic_data_count': len(synthetic_data),
                'total_count': len(real_data) + len(synthetic_data),
                'real_percentage': (len(real_data) / (len(real_data) + len(synthetic_data))) * 100 if (len(real_data) + len(synthetic_data)) > 0 else 0,
                'synthetic_percentage': (len(synthetic_data) / (len(real_data) + len(synthetic_data))) * 100 if (len(real_data) + len(synthetic_data)) > 0 else 0
            },
            'real_data_analysis': real_analysis,
            'synthetic_data_analysis': synthetic_analysis,
            'generated_at': datetime.now().isoformat()
        }
        
        return combined_analysis
    
    def update_training_data(self):
        """Main method to update training data with separation"""
        print("🔄 Updating Meeting PromptCoT Training Data (Separated Tracks)")
        print("=" * 60)
        
        # Backup existing data
        self.backup_existing_data()
        
        # Load all data sources
        print("📂 Loading data sources:")
        
        # Real data sources
        real_scenarios = []
        real_scenarios.extend(self.load_mevals_data())
        
        # Graph API data (separated)
        real_graph_data, synthetic_graph_data = self.load_graph_api_data()
        real_scenarios.extend(real_graph_data)
        
        # Synthetic data sources
        synthetic_scenarios = []
        synthetic_scenarios.extend(self.load_contextflow_data())
        synthetic_scenarios.extend(self.load_enhanced_data())
        synthetic_scenarios.extend(self.load_template_data())
        synthetic_scenarios.extend(synthetic_graph_data)
        
        print(f"\n📊 Initial counts:")
        print(f"Real scenarios: {len(real_scenarios)}")
        print(f"Synthetic scenarios: {len(synthetic_scenarios)}")
        
        # Normalize scenarios
        normalized_real = []
        normalized_synthetic = []
        
        for scenario in real_scenarios:
            source = scenario.get('source', 'unknown')
            normalized = self.normalize_scenario(scenario, source, 'real')
            normalized_real.append(normalized)
        
        for scenario in synthetic_scenarios:
            source = scenario.get('source', 'unknown')
            normalized = self.normalize_scenario(scenario, source, 'synthetic')
            normalized_synthetic.append(normalized)
        
        # Deduplicate within each track
        print(f"\n🔄 Deduplicating scenarios:")
        real_before = len(normalized_real)
        synthetic_before = len(normalized_synthetic)
        
        normalized_real = self.deduplicate_scenarios(normalized_real)
        normalized_synthetic = self.deduplicate_scenarios(normalized_synthetic)
        
        print(f"Real: {real_before} → {len(normalized_real)} scenarios")
        print(f"Synthetic: {synthetic_before} → {len(normalized_synthetic)} scenarios")
        
        # Save separated datasets
        print(f"\n💾 Saving separated training data:")
        
        with open(self.real_data_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_real, f, indent=2, ensure_ascii=False)
        print(f"📁 Real data: {self.real_data_file} ({len(normalized_real)} scenarios)")
        
        with open(self.synthetic_data_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_synthetic, f, indent=2, ensure_ascii=False)
        print(f"📁 Synthetic data: {self.synthetic_data_file} ({len(normalized_synthetic)} scenarios)")
        
        # Create combined dataset for backward compatibility
        combined_scenarios = normalized_real + normalized_synthetic
        with open(self.combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_scenarios, f, indent=2, ensure_ascii=False)
        print(f"📁 Combined data: {self.combined_file} ({len(combined_scenarios)} scenarios)")
        
        # Generate analysis
        analysis = self.analyze_separated_dataset(normalized_real, normalized_synthetic)
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"📊 Analysis saved: {self.analysis_file}")
        
        # Print summary
        self.print_summary(analysis)
        
        return normalized_real, normalized_synthetic, analysis
    
    def print_summary(self, analysis: Dict[str, Any]):
        """Print detailed summary of separated datasets"""
        sep = analysis['separation_summary']
        
        print(f"\n📊 Separated Dataset Summary:")
        print(f"=" * 50)
        print(f"🔴 Real Data: {sep['real_data_count']} scenarios ({sep['real_percentage']:.1f}%)")
        print(f"🔵 Synthetic Data: {sep['synthetic_data_count']} scenarios ({sep['synthetic_percentage']:.1f}%)")
        print(f"📦 Total: {sep['total_count']} scenarios")
        
        # Real data details
        if analysis.get('real_data_analysis'):
            real_analysis = analysis['real_data_analysis']
            print(f"\n🔴 Real Data Analysis:")
            print(f"   Average quality: {real_analysis['quality_scores']['average']:.2f}/10.0")
            print(f"   High quality (8.0+): {real_analysis['quality_scores']['high_quality']}")
            print(f"   Top sources:")
            for source, count in sorted(real_analysis['sources'].items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"     - {source}: {count}")
        
        # Synthetic data details
        if analysis.get('synthetic_data_analysis'):
            synthetic_analysis = analysis['synthetic_data_analysis']
            print(f"\n🔵 Synthetic Data Analysis:")
            print(f"   Average quality: {synthetic_analysis['quality_scores']['average']:.2f}/10.0")
            print(f"   High quality (8.0+): {synthetic_analysis['quality_scores']['high_quality']}")
            print(f"   Top sources:")
            for source, count in sorted(synthetic_analysis['sources'].items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"     - {source}: {count}")
        
        print(f"\n✅ Training data separated successfully!")
        print(f"📁 Files created:")
        print(f"   - Real data: {self.real_data_file}")
        print(f"   - Synthetic data: {self.synthetic_data_file}")
        print(f"   - Combined (backward compatibility): {self.combined_file}")
        print(f"   - Analysis: {self.analysis_file}")


def main():
    """Main execution function"""
    updater = SeparatedTrainingDataManager()
    updater.update_training_data()


if __name__ == "__main__":
    main()