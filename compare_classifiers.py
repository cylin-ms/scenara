#!/usr/bin/env python3
"""
Compare Meeting Classifiers: Ollama vs GPT-5
Side-by-side comparison of classification accuracy and performance
"""

import json
import logging
import time
from typing import Dict, Any, List
from pathlib import Path

# Import both classifiers
from tools.meeting_classifier import OllamaLLMMeetingClassifier
from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier


class ClassifierComparison:
    """Compare Ollama and GPT-5 meeting classifiers"""
    
    def __init__(self):
        self.ollama_classifier = None
        self.gpt5_classifier = None
        self.results = []
    
    def initialize_classifiers(self):
        """Initialize both classifiers and test availability"""
        
        print("\n" + "=" * 80)
        print("INITIALIZING CLASSIFIERS")
        print("=" * 80)
        
        # Initialize Ollama classifier
        print("\n1. Testing Ollama (gpt-oss:20b)...")
        try:
            self.ollama_classifier = OllamaLLMMeetingClassifier()
            ollama_available = self.ollama_classifier.test_model_availability()
            
            if ollama_available:
                print("   ✅ Ollama classifier ready")
            else:
                print("   ⚠️  Ollama classifier not available")
        except Exception as e:
            print(f"   ❌ Ollama initialization failed: {e}")
            ollama_available = False
        
        # Initialize GPT-5 classifier
        print("\n2. Testing GPT-5 (dev-gpt-5-chat-jj)...")
        try:
            self.gpt5_classifier = GPT5MeetingClassifier()
            gpt5_available = self.gpt5_classifier.test_model_availability()
            
            if gpt5_available:
                print("   ✅ GPT-5 classifier ready")
            else:
                print("   ⚠️  GPT-5 classifier not available")
        except Exception as e:
            print(f"   ❌ GPT-5 initialization failed: {e}")
            gpt5_available = False
        
        return ollama_available, gpt5_available
    
    def classify_with_both(
        self,
        subject: str,
        description: str = "",
        attendees: List[str] = None,
        duration_minutes: int = 60,
        expected_type: str = None,
        expected_category: str = None
    ) -> Dict[str, Any]:
        """Classify a meeting with both classifiers and compare results"""
        
        result = {
            "meeting": {
                "subject": subject,
                "description": description,
                "attendee_count": len(attendees) if attendees else 0,
                "duration": duration_minutes,
                "expected_type": expected_type,
                "expected_category": expected_category
            },
            "ollama": None,
            "gpt5": None,
            "comparison": {}
        }
        
        # Classify with Ollama
        if self.ollama_classifier:
            print(f"\n   Testing Ollama classifier...")
            start_time = time.time()
            try:
                ollama_result = self.ollama_classifier.classify_meeting_with_llm(
                    subject, description, attendees, duration_minutes
                )
                ollama_time = time.time() - start_time
                
                result["ollama"] = {
                    **ollama_result,
                    "latency_seconds": ollama_time
                }
                print(f"      Type: {ollama_result['specific_type']}")
                print(f"      Confidence: {ollama_result.get('confidence', 0):.1%}")
                print(f"      Latency: {ollama_time:.2f}s")
                
            except Exception as e:
                print(f"      ❌ Error: {e}")
                result["ollama"] = {"error": str(e)}
        
        # Classify with GPT-5
        if self.gpt5_classifier:
            print(f"\n   Testing GPT-5 classifier...")
            start_time = time.time()
            try:
                gpt5_result = self.gpt5_classifier.classify_meeting_with_llm(
                    subject, description, attendees, duration_minutes
                )
                gpt5_time = time.time() - start_time
                
                result["gpt5"] = {
                    **gpt5_result,
                    "latency_seconds": gpt5_time
                }
                print(f"      Type: {gpt5_result['specific_type']}")
                print(f"      Confidence: {gpt5_result.get('confidence', 0):.1%}")
                print(f"      Latency: {gpt5_time:.2f}s")
                
            except Exception as e:
                print(f"      ❌ Error: {e}")
                result["gpt5"] = {"error": str(e)}
        
        # Compare results
        if result["ollama"] and result["gpt5"]:
            ollama_type = result["ollama"].get("specific_type", "")
            gpt5_type = result["gpt5"].get("specific_type", "")
            
            result["comparison"] = {
                "types_match": ollama_type == gpt5_type,
                "ollama_correct": ollama_type == expected_type if expected_type else None,
                "gpt5_correct": gpt5_type == expected_type if expected_type else None,
                "confidence_diff": abs(
                    result["gpt5"].get("confidence", 0) - 
                    result["ollama"].get("confidence", 0)
                ),
                "latency_diff": result["gpt5"]["latency_seconds"] - result["ollama"]["latency_seconds"]
            }
            
            if result["comparison"]["types_match"]:
                print(f"\n   ✅ AGREEMENT: Both classified as '{ollama_type}'")
            else:
                print(f"\n   ⚠️  DISAGREEMENT:")
                print(f"      Ollama: {ollama_type}")
                print(f"      GPT-5:  {gpt5_type}")
        
        return result
    
    def run_test_suite(self) -> List[Dict[str, Any]]:
        """Run comprehensive test suite with known meeting types"""
        
        test_cases = [
            {
                "subject": "Weekly Team Standup",
                "description": "Quick 15-minute sync on sprint progress, blockers, and priorities",
                "attendees": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
                "duration": 15,
                "expected_type": "Team Status Update/Standup",
                "expected_category": "Internal Recurring (Cadence)"
            },
            {
                "subject": "1:1 with Sarah",
                "description": "Monthly one-on-one check-in to discuss career development and feedback",
                "attendees": ["Manager", "Sarah"],
                "duration": 30,
                "expected_type": "One-on-One Meeting",
                "expected_category": "Internal Recurring (Cadence)"
            },
            {
                "subject": "Q4 2025 Strategic Planning",
                "description": "Leadership team strategic planning session for Q4 initiatives, budget allocation, and resource planning",
                "attendees": ["CEO", "CFO", "VP Sales", "VP Engineering", "VP Product", "VP Marketing"],
                "duration": 180,
                "expected_type": "Strategic Planning Session",
                "expected_category": "Strategic Planning & Decision"
            },
            {
                "subject": "Acme Corp Product Demo",
                "description": "Product demonstration for Acme Corporation stakeholders showcasing new features",
                "attendees": ["Sales Rep", "Solutions Architect", "Acme CTO", "Acme Product Manager", "Acme VP Engineering"],
                "duration": 60,
                "expected_type": "Product Demo",
                "expected_category": "External & Client-Facing"
            },
            {
                "subject": "All-Hands: Q3 Results",
                "description": "Quarterly all-hands meeting to share Q3 results, company updates, and Q4 priorities",
                "attendees": ["All Employees"] * 150,  # Simulate 150 attendees
                "duration": 60,
                "expected_type": "All-Hands/Town Hall",
                "expected_category": "Informational & Broadcast"
            },
            {
                "subject": "Engineering Brainstorm - API Design",
                "description": "Collaborative brainstorming session for new API architecture design",
                "attendees": ["Tech Lead", "Senior Engineer 1", "Senior Engineer 2", "Architect", "Product Manager"],
                "duration": 90,
                "expected_type": "Brainstorming Session",
                "expected_category": "Strategic Planning & Decision"
            },
            {
                "subject": "Sprint Retrospective",
                "description": "Sprint 42 retrospective - what went well, what to improve, action items",
                "attendees": ["Scrum Master", "Dev 1", "Dev 2", "Dev 3", "QA Engineer", "Product Owner"],
                "duration": 60,
                "expected_type": "Team Retrospective",
                "expected_category": "Internal Recurring (Cadence)"
            },
            {
                "subject": "Customer Interview - Enterprise AI",
                "description": "Candidate interview for Senior Machine Learning Engineer position",
                "attendees": ["Hiring Manager", "Tech Lead", "Candidate", "HR Representative"],
                "duration": 60,
                "expected_type": "Interview Meeting",
                "expected_category": "External & Client-Facing"
            },
            {
                "subject": "New Hire Onboarding Workshop",
                "description": "Week 1 onboarding training for new engineers covering tools, processes, and culture",
                "attendees": ["Onboarding Lead", "New Hire 1", "New Hire 2", "New Hire 3", "HR"],
                "duration": 120,
                "expected_type": "Training Session",
                "expected_category": "Informational & Broadcast"
            },
            {
                "subject": "Team Social - Happy Hour",
                "description": "Monthly team social event at local brewery to celebrate recent wins",
                "attendees": ["Team Member 1", "Team Member 2", "Team Member 3", "Team Member 4", "Manager"],
                "duration": 120,
                "expected_type": "Social/Networking Event",
                "expected_category": "Team-Building & Culture"
            }
        ]
        
        print("\n" + "=" * 80)
        print("RUNNING TEST SUITE (10 Test Cases)")
        print("=" * 80)
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'=' * 80}")
            print(f"Test Case #{i}: {test_case['subject']}")
            print(f"{'=' * 80}")
            print(f"Description: {test_case['description'][:80]}...")
            print(f"Attendees: {test_case['duration']} minutes, {len(test_case['attendees'])} people")
            print(f"Expected: {test_case['expected_type']} ({test_case['expected_category']})")
            
            result = self.classify_with_both(**test_case)
            results.append(result)
            
            # Brief pause to avoid rate limiting
            time.sleep(1)
        
        return results
    
    def generate_report(self, results: List[Dict[str, Any]]):
        """Generate comprehensive comparison report"""
        
        print("\n" + "=" * 80)
        print("COMPARISON REPORT")
        print("=" * 80)
        
        # Calculate statistics
        total_tests = len(results)
        ollama_successes = sum(1 for r in results if r.get("ollama") and not r["ollama"].get("error"))
        gpt5_successes = sum(1 for r in results if r.get("gpt5") and not r["gpt5"].get("error"))
        
        agreements = sum(1 for r in results if r.get("comparison", {}).get("types_match"))
        
        ollama_correct = sum(1 for r in results 
                            if r.get("comparison", {}).get("ollama_correct") == True)
        gpt5_correct = sum(1 for r in results 
                          if r.get("comparison", {}).get("gpt5_correct") == True)
        
        # Average latencies
        ollama_latencies = [r["ollama"]["latency_seconds"] for r in results 
                           if r.get("ollama") and "latency_seconds" in r["ollama"]]
        gpt5_latencies = [r["gpt5"]["latency_seconds"] for r in results 
                         if r.get("gpt5") and "latency_seconds" in r["gpt5"]]
        
        avg_ollama_latency = sum(ollama_latencies) / len(ollama_latencies) if ollama_latencies else 0
        avg_gpt5_latency = sum(gpt5_latencies) / len(gpt5_latencies) if gpt5_latencies else 0
        
        # Average confidence
        ollama_confidences = [r["ollama"].get("confidence", 0) for r in results 
                             if r.get("ollama") and not r["ollama"].get("error")]
        gpt5_confidences = [r["gpt5"].get("confidence", 0) for r in results 
                           if r.get("gpt5") and not r["gpt5"].get("error")]
        
        avg_ollama_conf = sum(ollama_confidences) / len(ollama_confidences) if ollama_confidences else 0
        avg_gpt5_conf = sum(gpt5_confidences) / len(gpt5_confidences) if gpt5_confidences else 0
        
        # Print summary
        print(f"\n📊 SUMMARY STATISTICS")
        print(f"{'─' * 80}")
        print(f"Total Test Cases: {total_tests}")
        print()
        print(f"Ollama Classifier:")
        print(f"  Success Rate: {ollama_successes}/{total_tests} ({ollama_successes/total_tests:.1%})")
        print(f"  Accuracy: {ollama_correct}/{total_tests} ({ollama_correct/total_tests:.1%})")
        print(f"  Avg Confidence: {avg_ollama_conf:.1%}")
        print(f"  Avg Latency: {avg_ollama_latency:.2f}s")
        print()
        print(f"GPT-5 Classifier:")
        print(f"  Success Rate: {gpt5_successes}/{total_tests} ({gpt5_successes/total_tests:.1%})")
        print(f"  Accuracy: {gpt5_correct}/{total_tests} ({gpt5_correct/total_tests:.1%})")
        print(f"  Avg Confidence: {avg_gpt5_conf:.1%}")
        print(f"  Avg Latency: {avg_gpt5_latency:.2f}s")
        print()
        print(f"Agreement Rate: {agreements}/{total_tests} ({agreements/total_tests:.1%})")
        
        # Detailed results table
        print(f"\n📋 DETAILED RESULTS")
        print(f"{'─' * 80}")
        
        for i, result in enumerate(results, 1):
            meeting = result["meeting"]
            print(f"\n{i}. {meeting['subject']}")
            print(f"   Expected: {meeting['expected_type']}")
            
            if result.get("ollama") and not result["ollama"].get("error"):
                ollama = result["ollama"]
                correct = "✅" if result["comparison"].get("ollama_correct") else "❌"
                print(f"   Ollama:   {ollama['specific_type']} ({ollama.get('confidence', 0):.1%}) {correct}")
            else:
                print(f"   Ollama:   ❌ Error")
            
            if result.get("gpt5") and not result["gpt5"].get("error"):
                gpt5 = result["gpt5"]
                correct = "✅" if result["comparison"].get("gpt5_correct") else "❌"
                print(f"   GPT-5:    {gpt5['specific_type']} ({gpt5.get('confidence', 0):.1%}) {correct}")
            else:
                print(f"   GPT-5:    ❌ Error")
        
        # Save detailed results to JSON
        output_file = Path("data/evaluation_results") / f"classifier_comparison_{time.strftime('%Y%m%d_%H%M%S')}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_tests": total_tests,
                "ollama": {
                    "success_rate": ollama_successes / total_tests,
                    "accuracy": ollama_correct / total_tests,
                    "avg_confidence": avg_ollama_conf,
                    "avg_latency": avg_ollama_latency
                },
                "gpt5": {
                    "success_rate": gpt5_successes / total_tests,
                    "accuracy": gpt5_correct / total_tests,
                    "avg_confidence": avg_gpt5_conf,
                    "avg_latency": avg_gpt5_latency
                },
                "agreement_rate": agreements / total_tests
            },
            "detailed_results": results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        
        return report_data


def main():
    """Main comparison execution"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.WARNING,  # Reduce noise from classifiers
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 80)
    print("MEETING CLASSIFIER COMPARISON")
    print("Ollama (gpt-oss:20b) vs GPT-5 (dev-gpt-5-chat-jj)")
    print("=" * 80)
    
    # Initialize comparison
    comparison = ClassifierComparison()
    
    # Initialize classifiers
    ollama_available, gpt5_available = comparison.initialize_classifiers()
    
    if not ollama_available and not gpt5_available:
        print("\n❌ Neither classifier is available. Exiting.")
        return
    
    if not ollama_available:
        print("\n⚠️  Only GPT-5 classifier available. Running GPT-5 only tests.")
    
    if not gpt5_available:
        print("\n⚠️  Only Ollama classifier available. Running Ollama only tests.")
    
    # Run test suite
    results = comparison.run_test_suite()
    
    # Generate report
    report = comparison.generate_report(results)
    
    print("\n" + "=" * 80)
    print("COMPARISON COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
