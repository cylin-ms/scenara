#!/usr/bin/env python3
"""
Enhanced ContextFlow Integration with GUTT v4.0 ACRUE Framework
Integrates the sophisticated GUTT v4.0 evaluation methodology with separated data tracks
"""

from contextflow_integration import EnhancedMeetingPromptCoT
from gutt_v4_acrue_evaluator import GUTTv4ACRUEEvaluator
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class GUTTv4ContextFlowIntegration:
    def __init__(self):
        self.contextflow = EnhancedMeetingPromptCoT()
        self.gutt_evaluator = GUTTv4ACRUEEvaluator()
        
    def process_scenarios_with_v4_evaluation(self, scenarios: List[Dict[str, Any]], 
                                           data_type: str = "synthetic") -> List[Dict[str, Any]]:
        """Process scenarios with enhanced GUTT v4.0 ACRUE evaluation"""
        
        print(f"🔄 Processing {len(scenarios)} {data_type} scenarios with GUTT v4.0 ACRUE Framework")
        print("=" * 70)
        
        enhanced_scenarios = []
        
        for i, scenario in enumerate(scenarios):
            print(f"\n📊 Processing scenario {i+1}/{len(scenarios)}: {scenario.get('context', {}).get('subject', 'Unknown')[:50]}...")
            
            try:
                # Apply ContextFlow integration (if not already done)
                if 'contextflow_integration' not in scenario:
                    enhanced_scenario = self._enhance_scenario_with_contextflow(scenario)
                else:
                    enhanced_scenario = scenario.copy()
                
                # Apply GUTT v4.0 ACRUE evaluation
                v4_evaluation = self.gutt_evaluator.evaluate_meeting_scenario_v4(enhanced_scenario)
                
                # Integrate v4.0 evaluation results
                enhanced_scenario['gutt_v4_evaluation'] = {
                    'framework_version': v4_evaluation['framework_version'],
                    'evaluation_date': v4_evaluation['evaluation_date'],
                    'track1_score': v4_evaluation['track1_score'],
                    'track2_score': v4_evaluation['track2_score'],
                    'gutt_score': v4_evaluation['gutt_score'],
                    'performance_level': v4_evaluation['performance_level'],
                    'acrue_details': v4_evaluation['acrue_details'],
                    'user_quality_prediction': v4_evaluation['user_quality_prediction'],
                    'competitive_analysis': v4_evaluation['competitive_analysis'],
                    'required_gutts_count': len(v4_evaluation.get('required_gutts', {}).get('required_gutts', []))
                }
                
                # Update quality score with GUTT v4.0 score
                enhanced_scenario['quality_score'] = v4_evaluation['gutt_score']
                enhanced_scenario['quality_framework'] = 'GUTT_v4.0_ACRUE'
                
                # Add data type and enhanced provenance
                enhanced_scenario['data_type'] = data_type
                enhanced_scenario['enhancement_level'] = 'GUTT_v4.0_ACRUE_Enhanced'
                enhanced_scenario['last_enhanced'] = datetime.now().isoformat()
                
                enhanced_scenarios.append(enhanced_scenario)
                
                # Print summary
                print(f"  ✅ GUTTScore: {v4_evaluation['gutt_score']:.2f}/4.0")
                print(f"     Performance: {v4_evaluation['performance_level']['name']}")
                print(f"     User Quality: {v4_evaluation['user_quality_prediction']['overall_prediction']}")
                
            except Exception as e:
                print(f"  ❌ Error processing scenario: {e}")
                # Keep original scenario with error marker
                scenario['processing_error'] = str(e)
                scenario['data_type'] = data_type
                enhanced_scenarios.append(scenario)
        
        # Calculate enhancement statistics
        successful_enhancements = [s for s in enhanced_scenarios if 'gutt_v4_evaluation' in s]
        
        print(f"\n📈 Enhancement Summary:")
        print(f"  Total scenarios: {len(scenarios)}")
        print(f"  Successfully enhanced: {len(successful_enhancements)}")
        print(f"  Success rate: {len(successful_enhancements)/len(scenarios)*100:.1f}%")
        
        if successful_enhancements:
            avg_gutt_score = sum(s['gutt_v4_evaluation']['gutt_score'] for s in successful_enhancements) / len(successful_enhancements)
            high_performance = len([s for s in successful_enhancements if s['gutt_v4_evaluation']['gutt_score'] >= 3.0])
            
            print(f"  Average GUTTScore: {avg_gutt_score:.2f}/4.0")
            print(f"  High performance (3.0+): {high_performance}/{len(successful_enhancements)} ({high_performance/len(successful_enhancements)*100:.1f}%)")
        
        return enhanced_scenarios
    
    def _enhance_scenario_with_contextflow(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance a scenario using the ContextFlow system"""
        
        context = scenario.get('context', {})
        
        # Apply meeting classification
        classification = self.contextflow.classify_enterprise_meeting(
            subject=context.get('subject', ''),
            description=context.get('description', ''),
            attendees=context.get('attendees', []),
            duration_minutes=context.get('duration_minutes', 60)
        )
        
        # Generate enhanced preparation requirements
        enhanced_prep = self.contextflow.generate_enhanced_preparation_requirements(
            classification, context
        )
        
        # Calculate ACRUE scores
        acrue_scores = self.contextflow.calculate_acrue_score(
            context, enhanced_prep, classification
        )
        
        # Create enhanced scenario
        enhanced_scenario = scenario.copy()
        enhanced_scenario['contextflow_integration'] = {
            'enterprise_taxonomy': classification,
            'enhanced_preparation_requirements': enhanced_prep,
            'acrue_scores': acrue_scores,
            'recommended_gutt_tasks': self.contextflow.get_gutt_recommendations(
                classification.get('category', 'General Business')
            )
        }
        
        # Update preparation requirements
        enhanced_scenario['preparation_requirements'] = enhanced_prep
        
        return enhanced_scenario
    
    def enhance_separated_datasets(self):
        """Enhance both real and synthetic datasets with GUTT v4.0 evaluation"""
        
        print("🚀 Enhancing Separated Datasets with GUTT v4.0 ACRUE Framework")
        print("=" * 70)
        
        data_dir = "meeting_prep_data"
        
        # Load separated datasets
        real_file = f"{data_dir}/training_scenarios_real.json"
        synthetic_file = f"{data_dir}/training_scenarios_synthetic.json"
        
        results = {}
        
        # Process Real Data
        if os.path.exists(real_file):
            print(f"\n🔴 Processing Real Data...")
            with open(real_file, 'r', encoding='utf-8') as f:
                real_scenarios = json.load(f)
            
            enhanced_real = self.process_scenarios_with_v4_evaluation(real_scenarios, "real")
            
            # Save enhanced real data
            enhanced_real_file = f"{data_dir}/training_scenarios_real_v4.json"
            with open(enhanced_real_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced_real, f, indent=2, ensure_ascii=False)
            
            results['real'] = {
                'original_count': len(real_scenarios),
                'enhanced_count': len(enhanced_real),
                'output_file': enhanced_real_file
            }
            
            print(f"💾 Enhanced real data saved: {enhanced_real_file}")
        
        # Process Synthetic Data  
        if os.path.exists(synthetic_file):
            print(f"\n🔵 Processing Synthetic Data...")
            with open(synthetic_file, 'r', encoding='utf-8') as f:
                synthetic_scenarios = json.load(f)
            
            enhanced_synthetic = self.process_scenarios_with_v4_evaluation(synthetic_scenarios, "synthetic")
            
            # Save enhanced synthetic data
            enhanced_synthetic_file = f"{data_dir}/training_scenarios_synthetic_v4.json"
            with open(enhanced_synthetic_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced_synthetic, f, indent=2, ensure_ascii=False)
            
            results['synthetic'] = {
                'original_count': len(synthetic_scenarios),
                'enhanced_count': len(enhanced_synthetic),
                'output_file': enhanced_synthetic_file
            }
            
            print(f"💾 Enhanced synthetic data saved: {enhanced_synthetic_file}")
        
        # Create combined enhanced dataset
        if 'real' in results and 'synthetic' in results:
            print(f"\n📦 Creating Combined Enhanced Dataset...")
            
            with open(f"{data_dir}/training_scenarios_real_v4.json", 'r') as f:
                enhanced_real = json.load(f)
            with open(f"{data_dir}/training_scenarios_synthetic_v4.json", 'r') as f:
                enhanced_synthetic = json.load(f)
            
            combined_enhanced = enhanced_real + enhanced_synthetic
            
            combined_file = f"{data_dir}/training_scenarios_combined_v4.json"
            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(combined_enhanced, f, indent=2, ensure_ascii=False)
            
            results['combined'] = {
                'total_count': len(combined_enhanced),
                'output_file': combined_file
            }
            
            print(f"💾 Combined enhanced data saved: {combined_file}")
        
        # Generate comprehensive analysis
        analysis = self._analyze_v4_enhancements(results)
        
        analysis_file = f"{data_dir}/gutt_v4_enhancement_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Enhancement analysis saved: {analysis_file}")
        
        # Print final summary
        self._print_enhancement_summary(results, analysis)
        
        return results, analysis
    
    def _analyze_v4_enhancements(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the GUTT v4.0 enhancement results"""
        
        analysis = {
            'enhancement_timestamp': datetime.now().isoformat(),
            'framework_version': 'GUTT_v4.0_ACRUE_Integration',
            'datasets_processed': list(results.keys()),
            'total_scenarios': sum(r.get('enhanced_count', 0) for r in results.values() if isinstance(r, dict)),
            'quality_analysis': {},
            'performance_distribution': {},
            'competitive_analysis': {}
        }
        
        # Analyze each dataset
        data_dir = "meeting_prep_data"
        
        for data_type in ['real', 'synthetic', 'combined']:
            file_path = f"{data_dir}/training_scenarios_{data_type}_v4.json"
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    scenarios = json.load(f)
                
                enhanced_scenarios = [s for s in scenarios if 'gutt_v4_evaluation' in s]
                
                if enhanced_scenarios:
                    # Quality analysis
                    gutt_scores = [s['gutt_v4_evaluation']['gutt_score'] for s in enhanced_scenarios]
                    track1_scores = [s['gutt_v4_evaluation']['track1_score'] for s in enhanced_scenarios]
                    track2_scores = [s['gutt_v4_evaluation']['track2_score'] for s in enhanced_scenarios]
                    
                    analysis['quality_analysis'][data_type] = {
                        'scenario_count': len(enhanced_scenarios),
                        'average_gutt_score': sum(gutt_scores) / len(gutt_scores),
                        'average_track1_score': sum(track1_scores) / len(track1_scores),
                        'average_track2_score': sum(track2_scores) / len(track2_scores),
                        'high_performance_count': len([s for s in gutt_scores if s >= 3.0]),
                        'exceptional_performance_count': len([s for s in gutt_scores if s >= 3.5])
                    }
                    
                    # Performance distribution
                    performance_levels = [s['gutt_v4_evaluation']['performance_level']['level'] for s in enhanced_scenarios]
                    level_counts = {}
                    for level in performance_levels:
                        level_counts[level] = level_counts.get(level, 0) + 1
                    
                    analysis['performance_distribution'][data_type] = level_counts
        
        return analysis
    
    def _print_enhancement_summary(self, results: Dict[str, Any], analysis: Dict[str, Any]):
        """Print comprehensive enhancement summary"""
        
        print(f"\n🎯 GUTT v4.0 Enhancement Summary")
        print("=" * 50)
        
        for data_type, stats in results.items():
            if isinstance(stats, dict) and 'enhanced_count' in stats:
                print(f"\n{'🔴' if data_type == 'real' else '🔵' if data_type == 'synthetic' else '📦'} {data_type.title()} Data:")
                print(f"  Scenarios processed: {stats['enhanced_count']}")
                
                if data_type in analysis['quality_analysis']:
                    qa = analysis['quality_analysis'][data_type]
                    print(f"  Average GUTTScore: {qa['average_gutt_score']:.2f}/4.0")
                    print(f"  High performance: {qa['high_performance_count']}/{qa['scenario_count']} ({qa['high_performance_count']/qa['scenario_count']*100:.1f}%)")
                    print(f"  Exceptional performance: {qa['exceptional_performance_count']}/{qa['scenario_count']} ({qa['exceptional_performance_count']/qa['scenario_count']*100:.1f}%)")
        
        print(f"\n✨ Key Benefits of GUTT v4.0 Integration:")
        print("  🎯 Multiplicative GUTTScore methodology ensures capability triggering")
        print("  📊 ACRUE framework aligns with user-perceived quality")
        print("  🔍 Comprehensive GUTT capability identification and evaluation")
        print("  🏆 Performance classification with business value assessment")
        print("  📈 User quality prediction and competitive analysis")
        
        print(f"\n📁 Enhanced Files Created:")
        for data_type, stats in results.items():
            if isinstance(stats, dict) and 'output_file' in stats:
                print(f"  - {stats['output_file']}")
        
        print(f"\n🚀 Your separated data system now includes:")
        print("  ✅ Original separated tracks (real vs synthetic)")
        print("  ✅ GUTT v4.0 ACRUE enhanced versions")
        print("  ✅ Comprehensive evaluation framework")
        print("  ✅ User quality prediction capabilities")
        print("  ✅ Competitive advantage analysis")


def main():
    """Test the enhanced GUTT v4.0 ContextFlow integration"""
    
    print("🚀 Testing GUTT v4.0 ContextFlow Integration")
    print("=" * 60)
    
    integration = GUTTv4ContextFlowIntegration()
    
    # Test with a small sample first
    test_scenario = {
        'id': 'test_v4_integration',
        'context': {
            'subject': 'Enterprise AI Strategy Planning',
            'description': 'Executive planning session to define AI integration strategy across business units',
            'attendee_count': 6,
            'duration_minutes': 90,
            'is_online_meeting': False
        },
        'meeting_type': 'Strategic Planning Meeting',
        'preparation_requirements': [
            'Research current AI market trends and competitor analysis',
            'Prepare ROI models for AI implementation across departments',
            'Identify potential AI use cases and business impact assessment'
        ]
    }
    
    print("🧪 Testing single scenario enhancement...")
    enhanced_scenarios = integration.process_scenarios_with_v4_evaluation([test_scenario], "test")
    
    if enhanced_scenarios and 'gutt_v4_evaluation' in enhanced_scenarios[0]:
        v4_eval = enhanced_scenarios[0]['gutt_v4_evaluation']
        
        print(f"\n📊 Test Results:")
        print(f"  GUTTScore: {v4_eval['gutt_score']:.2f}/4.0")
        print(f"  Track 1: {v4_eval['track1_score']:.2f}/1.0")
        print(f"  Track 2: {v4_eval['track2_score']:.2f}/4.0")
        print(f"  Performance: {v4_eval['performance_level']['name']}")
        print(f"  User Quality: {v4_eval['user_quality_prediction']['overall_prediction']}")
        
        print(f"\n✅ GUTT v4.0 integration working correctly!")
        
        # Uncomment to enhance full datasets
        # print(f"\n🔄 Enhancing full separated datasets...")
        # results, analysis = integration.enhance_separated_datasets()
        
    else:
        print(f"❌ Integration test failed")


if __name__ == "__main__":
    main()