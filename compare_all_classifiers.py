#!/usr/bin/env python3
"""
Compare All Meeting Classifiers: Ollama, GPT-5, and GPT-4o
Comprehensive comparison of classification accuracy, confidence, and performance
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Import classifiers
try:
    from tools.meeting_classifier_ollama import OllamaMeetingClassifier
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️ Ollama classifier not available")

try:
    from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier
    GPT5_AVAILABLE = True
except ImportError:
    GPT5_AVAILABLE = False
    print("⚠️ GPT-5 classifier not available")

try:
    from tools.meeting_classifier_gpt4o import GPT4oMeetingClassifier
    GPT4O_AVAILABLE = True
except ImportError:
    GPT4O_AVAILABLE = False
    print("⚠️ GPT-4o classifier not available")


class ClassifierComparison:
    """Compare multiple meeting classifiers"""
    
    def __init__(self):
        self.classifiers = {}
        self.initialize_classifiers()
    
    def initialize_classifiers(self):
        """Initialize available classifiers"""
        print("\n" + "=" * 80)
        print("Initializing Classifiers")
        print("=" * 80)
        
        # Initialize Ollama
        if OLLAMA_AVAILABLE:
            try:
                ollama = OllamaMeetingClassifier()
                if ollama.test_model_availability():
                    self.classifiers['Ollama'] = ollama
                    print("✅ Ollama classifier ready")
                else:
                    print("⚠️ Ollama model not available")
            except Exception as e:
                print(f"❌ Ollama initialization failed: {e}")
        
        # Initialize GPT-5
        if GPT5_AVAILABLE:
            try:
                gpt5 = GPT5MeetingClassifier()
                if gpt5.test_model_availability():
                    self.classifiers['GPT-5'] = gpt5
                    print("✅ GPT-5 classifier ready")
                else:
                    print("⚠️ GPT-5 model not available")
            except Exception as e:
                print(f"❌ GPT-5 initialization failed: {e}")
        
        # Initialize GPT-4o
        if GPT4O_AVAILABLE:
            try:
                gpt4o = GPT4oMeetingClassifier()
                if gpt4o.test_model_availability():
                    self.classifiers['GPT-4o'] = gpt4o
                    print("✅ GPT-4o classifier ready")
                else:
                    print("⚠️ GPT-4o model not available")
            except Exception as e:
                print(f"❌ GPT-4o initialization failed: {e}")
        
        print(f"\nTotal classifiers available: {len(self.classifiers)}")
        if not self.classifiers:
            print("❌ No classifiers available for comparison!")
            raise RuntimeError("No classifiers initialized")
    
    def create_test_meetings(self) -> List[Dict[str, Any]]:
        """Create comprehensive test dataset covering all taxonomy categories"""
        
        return [
            # 1. Strategic Planning & Decision
            {
                "id": "TEST-001",
                "subject": "Q4 Strategic Planning Session",
                "description": "Strategic planning for Q4 initiatives, budget allocation, and resource planning",
                "attendees": ["VP Engineering", "VP Sales", "CFO", "CEO", "Product Director"],
                "duration": 120,
                "expected_type": "Strategic Planning Session",
                "expected_category": "Strategic Planning & Decision"
            },
            {
                "id": "TEST-002",
                "subject": "Risk Assessment - Cloud Migration",
                "description": "Evaluate risks and mitigation strategies for AWS cloud migration project",
                "attendees": ["CTO", "Security Lead", "DevOps Manager", "Architect"],
                "duration": 90,
                "expected_type": "Risk Assessment Meeting",
                "expected_category": "Strategic Planning & Decision"
            },
            {
                "id": "TEST-003",
                "subject": "Product Brainstorming Workshop",
                "description": "Ideation session for new feature concepts and user experience improvements",
                "attendees": ["Product Manager", "UX Designer", "Engineers", "Marketing"],
                "duration": 120,
                "expected_type": "Brainstorming Session",
                "expected_category": "Strategic Planning & Decision"
            },
            
            # 2. Internal Recurring (Cadence)
            {
                "id": "TEST-004",
                "subject": "Daily Standup - Engineering",
                "description": "Quick daily sync on sprint progress, blockers, and today's focus",
                "attendees": ["Dev Team (8 people)"],
                "duration": 15,
                "expected_type": "Team Status Update/Standup",
                "expected_category": "Internal Recurring (Cadence)"
            },
            {
                "id": "TEST-005",
                "subject": "1:1 with Sarah",
                "description": "Bi-weekly one-on-one check-in",
                "attendees": ["Manager", "Sarah"],
                "duration": 30,
                "expected_type": "One-on-One Meeting",
                "expected_category": "Internal Recurring (Cadence)"
            },
            {
                "id": "TEST-006",
                "subject": "Sprint Retrospective",
                "description": "Review Sprint 42: what went well, what to improve, action items",
                "attendees": ["Scrum Master", "Dev Team (6 people)"],
                "duration": 60,
                "expected_type": "Team Retrospective",
                "expected_category": "Internal Recurring (Cadence)"
            },
            
            # 3. External & Client-Facing
            {
                "id": "TEST-007",
                "subject": "Sales Demo - Enterprise Client",
                "description": "Product demonstration for Fortune 500 prospect, Q&A session",
                "attendees": ["Sales Rep", "Sales Engineer", "Client Team (5 people)"],
                "duration": 60,
                "expected_type": "Sales & Client Meeting",
                "expected_category": "External & Client-Facing"
            },
            {
                "id": "TEST-008",
                "subject": "Interview - Senior Engineer Candidate",
                "description": "Technical interview for senior backend engineer position",
                "attendees": ["Hiring Manager", "Tech Lead", "Candidate"],
                "duration": 60,
                "expected_type": "Interview Meeting",
                "expected_category": "External & Client-Facing"
            },
            {
                "id": "TEST-009",
                "subject": "Vendor Partnership Discussion",
                "description": "Strategic partnership discussion with AWS account team",
                "attendees": ["CTO", "Procurement", "AWS Account Manager", "AWS Solutions Architect"],
                "duration": 45,
                "expected_type": "Partnership Meeting",
                "expected_category": "External & Client-Facing"
            },
            
            # 4. Informational & Broadcast
            {
                "id": "TEST-010",
                "subject": "All-Hands - Company Quarterly Review",
                "description": "Quarterly company update, financial results, strategy updates",
                "attendees": ["All Employees (150 people)", "CEO", "Leadership Team"],
                "duration": 60,
                "expected_type": "All-Hands/Town Hall",
                "expected_category": "Informational & Broadcast"
            },
            {
                "id": "TEST-011",
                "subject": "Product Training - New Features",
                "description": "Training session on new product features for customer success team",
                "attendees": ["Product Manager", "Customer Success Team (12 people)"],
                "duration": 90,
                "expected_type": "Training Session",
                "expected_category": "Informational & Broadcast"
            },
            {
                "id": "TEST-012",
                "subject": "Tech Talk - Machine Learning Best Practices",
                "description": "Knowledge sharing session on ML model deployment and monitoring",
                "attendees": ["ML Engineer", "Data Science Team (15 people)"],
                "duration": 45,
                "expected_type": "Knowledge Sharing Session",
                "expected_category": "Informational & Broadcast"
            },
            
            # 5. Team-Building & Culture
            {
                "id": "TEST-013",
                "subject": "Team Social - Happy Hour",
                "description": "Casual team gathering at local brewery",
                "attendees": ["Engineering Team (20 people)"],
                "duration": 120,
                "expected_type": "Social/Networking Event",
                "expected_category": "Team-Building & Culture"
            },
            {
                "id": "TEST-014",
                "subject": "Quarterly Team Offsite",
                "description": "Team building activities and strategic planning offsite",
                "attendees": ["Product Team (12 people)", "Facilitator"],
                "duration": 480,  # Full day
                "expected_type": "Offsite/Retreat",
                "expected_category": "Team-Building & Culture"
            },
            {
                "id": "TEST-015",
                "subject": "Welcome Coffee - New Team Member",
                "description": "Meet and greet with new engineer joining the team",
                "attendees": ["Team Members (8 people)", "New Hire"],
                "duration": 30,
                "expected_type": "Welcome/Farewell Event",
                "expected_category": "Team-Building & Culture"
            }
        ]
    
    def classify_with_all(self, meeting: Dict[str, Any]) -> Dict[str, Any]:
        """Classify a meeting with all available classifiers"""
        
        results = {}
        
        for name, classifier in self.classifiers.items():
            try:
                start_time = time.time()
                
                # Call classifier
                classification = classifier.classify_meeting_with_llm(
                    subject=meeting['subject'],
                    description=meeting['description'],
                    attendees=meeting['attendees'],
                    duration_minutes=meeting['duration']
                )
                
                latency = time.time() - start_time
                
                results[name] = {
                    'specific_type': classification.get('specific_type', 'Unknown'),
                    'primary_category': classification.get('primary_category', 'Unknown'),
                    'confidence': classification.get('confidence', 0.0),
                    'reasoning': classification.get('reasoning', ''),
                    'latency_seconds': round(latency, 2),
                    'success': True
                }
                
            except Exception as e:
                results[name] = {
                    'specific_type': 'Error',
                    'primary_category': 'Error',
                    'confidence': 0.0,
                    'reasoning': str(e),
                    'latency_seconds': 0.0,
                    'success': False
                }
        
        return results
    
    def compare_classifiers(self):
        """Run full comparison across all test cases"""
        
        print("\n" + "=" * 80)
        print("Running Classifier Comparison")
        print("=" * 80)
        
        test_meetings = self.create_test_meetings()
        all_results = []
        
        for i, meeting in enumerate(test_meetings, 1):
            print(f"\n[{i}/{len(test_meetings)}] Testing: {meeting['subject']}")
            print(f"    Expected: {meeting['expected_type']} ({meeting['expected_category']})")
            
            # Classify with all classifiers
            classifications = self.classify_with_all(meeting)
            
            # Compare results
            print("\n    Results:")
            for classifier_name, result in classifications.items():
                if result['success']:
                    match_type = "✅" if result['specific_type'] == meeting['expected_type'] else "❌"
                    match_cat = "✅" if result['primary_category'] == meeting['expected_category'] else "❌"
                    
                    print(f"      {classifier_name}:")
                    print(f"        Type: {result['specific_type']} {match_type}")
                    print(f"        Category: {result['primary_category']} {match_cat}")
                    print(f"        Confidence: {result['confidence']:.1%}")
                    print(f"        Latency: {result['latency_seconds']}s")
                else:
                    print(f"      {classifier_name}: ❌ Failed - {result['reasoning']}")
            
            # Store results
            all_results.append({
                'meeting': meeting,
                'classifications': classifications
            })
            
            # Rate limiting
            time.sleep(1.0)
        
        # Generate comparison report
        self.generate_report(all_results)
    
    def generate_report(self, all_results: List[Dict]):
        """Generate comprehensive comparison report"""
        
        print("\n" + "=" * 80)
        print("COMPARISON SUMMARY")
        print("=" * 80)
        
        # Calculate metrics per classifier
        metrics = {}
        for classifier_name in self.classifiers.keys():
            metrics[classifier_name] = {
                'total_tests': 0,
                'successful': 0,
                'type_matches': 0,
                'category_matches': 0,
                'total_confidence': 0.0,
                'total_latency': 0.0
            }
        
        for result in all_results:
            expected_type = result['meeting']['expected_type']
            expected_category = result['meeting']['expected_category']
            
            for classifier_name, classification in result['classifications'].items():
                m = metrics[classifier_name]
                m['total_tests'] += 1
                
                if classification['success']:
                    m['successful'] += 1
                    
                    if classification['specific_type'] == expected_type:
                        m['type_matches'] += 1
                    
                    if classification['primary_category'] == expected_category:
                        m['category_matches'] += 1
                    
                    m['total_confidence'] += classification['confidence']
                    m['total_latency'] += classification['latency_seconds']
        
        # Print metrics
        print("\nPer-Classifier Performance:\n")
        for classifier_name, m in metrics.items():
            if m['total_tests'] > 0:
                success_rate = (m['successful'] / m['total_tests']) * 100
                type_accuracy = (m['type_matches'] / m['total_tests']) * 100
                category_accuracy = (m['category_matches'] / m['total_tests']) * 100
                avg_confidence = m['total_confidence'] / max(m['successful'], 1)
                avg_latency = m['total_latency'] / max(m['successful'], 1)
                
                print(f"{classifier_name}:")
                print(f"  Success Rate:       {success_rate:.1f}% ({m['successful']}/{m['total_tests']})")
                print(f"  Type Accuracy:      {type_accuracy:.1f}% ({m['type_matches']}/{m['total_tests']})")
                print(f"  Category Accuracy:  {category_accuracy:.1f}% ({m['category_matches']}/{m['total_tests']})")
                print(f"  Avg Confidence:     {avg_confidence:.1%}")
                print(f"  Avg Latency:        {avg_latency:.2f}s")
                print()
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"classifier_comparison_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'classifiers': list(self.classifiers.keys()),
                'test_results': all_results,
                'metrics': metrics
            }, f, indent=2)
        
        print(f"Detailed results saved to: {output_file}")
        print("=" * 80)


def main():
    """Main entry point"""
    
    print("=" * 80)
    print("Meeting Classifier Comparison Tool")
    print("Comparing: Ollama, GPT-5, and GPT-4o")
    print("=" * 80)
    
    try:
        comparison = ClassifierComparison()
        comparison.compare_classifiers()
    except Exception as e:
        print(f"\n❌ Comparison failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
