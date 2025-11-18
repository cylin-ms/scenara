"""
PFT Preference Pair Generation for Workback Planning

Uses existing Scenara components to generate preference pairs for DPO training:
1. WorkbackPlanGenerator.generate_plan() - creates candidate plans
2. LLM-as-Judge with ACRUE assertions - evaluates quality
3. Preference pair selection - picks best vs worst with 15%+ gap

Usage:
    python generate_pft_preference_pairs.py --vertical QBR --count 50
"""

import json
import sys
import os
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))
from workback_planning.generator.plan_generator import generate_plan
from tools.llm_api import LLMAPIClient


class PreferencePairGenerator:
    """Generate preference pairs for PFT/DPO training"""
    
    def __init__(self, client: Optional[LLMAPIClient] = None):
        """
        Initialize preference pair generator.
        
        Args:
            client: LLMAPIClient instance (creates new if None)
        """
        self.client = client or LLMAPIClient()
        self.acrue_assertions = self._load_acrue_checklist()
    
    def _load_acrue_checklist(self) -> List[str]:
        """
        Load ACRUE assertion checklist.
        
        Returns:
            List of assertion IDs (A1-A10, C1-C15, R1-R10, U1-U10, E1-E5)
        """
        # TODO: Load from WORKBACK_PLAN_EVALUATION_FRAMEWORK_V1.md
        # For now, return simplified checklist
        assertions = []
        assertions.extend([f"A{i}" for i in range(1, 11)])  # Accuracy (10)
        assertions.extend([f"C{i}" for i in range(1, 16)])  # Completeness (15)
        assertions.extend([f"R{i}" for i in range(1, 11)])  # Relevance (10)
        assertions.extend([f"U{i}" for i in range(1, 11)])  # Usefulness (10)
        assertions.extend([f"E{i}" for i in range(1, 6)])   # Exceptional (5)
        return assertions
    
    def generate_candidate_plan(
        self,
        scenario: str,
        temperature: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate a single candidate workback plan.
        
        This is the actual implementation of `model.generate()` from the docs.
        
        Args:
            scenario: Meeting context and requirements
            temperature: Sampling temperature (0.8=conservative, 1.5=creative)
        
        Returns:
            Dictionary with 'analysis' and 'structured' plan
        """
        # Override model config with specific temperature
        model_override = {
            "provider": "ollama",
            "model": "gpt-oss:120b",
            "base_url": "http://192.168.2.204:11434",
            "temperature": temperature,
            "timeout": 300.0
        }
        
        # Generate plan using existing pipeline
        result = generate_plan(
            context=scenario,
            client=self.client,
            analysis_model_override=model_override,
            structure_model_override=model_override
        )
        
        return result
    
    def evaluate_assertions(
        self,
        plan: Dict[str, Any],
        scenario: str
    ) -> Dict[str, Any]:
        """
        Evaluate plan against ACRUE assertions using LLM-as-Judge.
        
        Args:
            plan: Generated workback plan with 'structured' field
            scenario: Original meeting context
        
        Returns:
            Dictionary with:
                - score: Overall pass rate (0.0-1.0)
                - passed: List of assertion IDs that passed
                - failed: List of assertion IDs that failed
                - details: Detailed feedback per assertion
        """
        # Build evaluation prompt
        plan_json = json.dumps(plan.get('structured', {}), indent=2)
        
        evaluation_prompt = f"""You are evaluating a workback plan for quality using the ACRUE framework.

**Scenario:**
{scenario}

**Generated Plan:**
{plan_json}

**ACRUE Assertions to Evaluate:**

**Accuracy (A1-A10):**
- A1: Meeting goal correctly extracted from context
- A2: Timelines are realistic and feasible
- A3: Dates respect working days, holidays, weekends
- A4: Task owners are meeting attendees
- A5: Dependencies are logically sound (no circular dependencies)
- A6: Milestone sequencing is correct
- A7: Resource estimates are reasonable
- A8: Risk assessments are accurate
- A9: Artifact references are valid
- A10: Historical precedents correctly applied

**Completeness (C1-C15):**
- C1: All meeting objectives covered
- C2: Critical milestones present (data collection, draft, review, lock)
- C3: Tech readiness check included
- C4: Stakeholder reviews included
- C5: Backup plans documented
- C6: Communication checkpoints present
- C7: Quality gates defined
- C8: Risk mitigation steps included
- C9: Artifact deliverables specified
- C10: Dependencies fully mapped
- C11: Resource allocations complete
- C12: Timeline buffers included
- C13: Escalation paths defined
- C14: Success criteria specified
- C15: Exit criteria defined

**Relevance (R1-R10):**
- R1: Plan aligns with meeting type
- R2: Tasks directly support meeting goals
- R3: Participants match required expertise
- R4: Timeline fits meeting urgency
- R5: Scope appropriate for context
- R6: Deliverables match expectations
- R7: Risks relevant to objectives
- R8: Dependencies align with workflow
- R9: Resources match complexity
- R10: Format fits organizational standards

**Usefulness (U1-U10):**
- U1: Plan is actionable and executable
- U2: Backup presenters identified
- U3: Clear ownership for each task
- U4: Realistic effort estimates
- U5: Practical sequencing
- U6: Accessible artifacts
- U7: Clear success metrics
- U8: Executable within constraints
- U9: Adaptable to changes
- U10: Communicable to stakeholders

**Exceptional (E1-E5):**
- E1: Proactive risk mitigation documented
- E2: Contingency plans for blockers
- E3: Innovation or best practices applied
- E4: Efficiency optimizations included
- E5: Exceeds typical planning standards

**Instructions:**
For EACH assertion (A1-A10, C1-C15, R1-R10, U1-U10, E1-E5), evaluate whether the plan passes, partially passes, or fails.

Respond with a JSON object:
{{
    "passed": ["A1", "A2", "C1", ...],
    "partial": ["C2", "E1", ...],
    "failed": ["A4", "C3", ...],
    "score": 0.85,
    "feedback": {{
        "A1": "Pass - Goal correctly extracted",
        "A4": "Fail - Task owner 'John Smith' not in attendee list",
        ...
    }}
}}

Scoring: Pass=1.0, Partial=0.5, Fail=0.0. Overall score = sum(scores) / 50."""
        
        # Query LLM-as-Judge
        try:
            response = self.client.query_llm(
                prompt=evaluation_prompt,
                provider="ollama",
                model="gpt-oss:120b",
                base_url="http://192.168.2.204:11434",
                temperature=0.1,  # Low temp for consistent evaluation
                timeout=180.0
            )
            
            # Parse JSON response
            import re
            json_str = response.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("\n", 1)[1] if "\n" in json_str else json_str[3:]
                if json_str.endswith("```"):
                    json_str = json_str.rsplit("```", 1)[0]
                json_str = json_str.strip()
            
            # Clean up JSON
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            evaluation = json.loads(json_str)
            
            # Calculate score if not provided
            if 'score' not in evaluation:
                passed_count = len(evaluation.get('passed', []))
                partial_count = len(evaluation.get('partial', []))
                evaluation['score'] = (passed_count + partial_count * 0.5) / 50.0
            
            return evaluation
            
        except Exception as e:
            print(f"⚠️  Warning: Evaluation failed: {e}")
            # Return default low score
            return {
                "passed": [],
                "partial": [],
                "failed": self.acrue_assertions,
                "score": 0.0,
                "feedback": {"error": str(e)}
            }
    
    def generate_preference_pair(
        self,
        scenario: str,
        temperatures: List[float] = [0.8, 1.0, 1.2, 1.5, 1.8],
        min_score_gap: float = 0.15
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a preference pair (better plan vs worse plan).
        
        This implements the algorithm from ASSERTIONS_PFT_RFT_INTEGRATION.md:
        1. Generate N candidates with different temperatures
        2. Evaluate each with ACRUE assertions
        3. Select best and worst if score gap >= min_score_gap
        
        Args:
            scenario: Meeting context
            temperatures: List of temperatures for candidate generation
            min_score_gap: Minimum score difference (default 15%)
        
        Returns:
            Preference pair dictionary or None if no valid pair found
        """
        print(f"\n{'='*80}")
        print(f"Generating preference pair for scenario...")
        print(f"{'='*80}")
        
        # Step 1: Generate candidates
        candidates = []
        for i, temp in enumerate(temperatures):
            print(f"\n[{i+1}/{len(temperatures)}] Generating candidate with temperature={temp}...")
            try:
                plan = self.generate_candidate_plan(scenario, temperature=temp)
                candidates.append({
                    "plan": plan,
                    "temperature": temp
                })
                print(f"✓ Generated {len(plan.get('structured', {}).get('milestones', []))} milestones")
            except Exception as e:
                print(f"✗ Failed: {e}")
                continue
        
        if len(candidates) < 2:
            print(f"✗ Not enough candidates generated ({len(candidates)})")
            return None
        
        # Step 2: Evaluate candidates
        print(f"\n{'='*80}")
        print(f"Evaluating {len(candidates)} candidates with ACRUE assertions...")
        print(f"{'='*80}")
        
        evaluations = []
        for i, candidate in enumerate(candidates):
            print(f"\n[{i+1}/{len(candidates)}] Evaluating candidate (temp={candidate['temperature']})...")
            try:
                evaluation = self.evaluate_assertions(candidate['plan'], scenario)
                evaluations.append({
                    **candidate,
                    "evaluation": evaluation
                })
                score = evaluation.get('score', 0.0)
                passed = len(evaluation.get('passed', []))
                failed = len(evaluation.get('failed', []))
                print(f"✓ Score: {score:.2%} (Pass: {passed}, Fail: {failed})")
            except Exception as e:
                print(f"✗ Evaluation failed: {e}")
                continue
        
        if len(evaluations) < 2:
            print(f"✗ Not enough evaluations completed ({len(evaluations)})")
            return None
        
        # Step 3: Select best and worst
        evaluations.sort(key=lambda x: x['evaluation'].get('score', 0.0), reverse=True)
        best = evaluations[0]
        worst = evaluations[-1]
        
        best_score = best['evaluation'].get('score', 0.0)
        worst_score = worst['evaluation'].get('score', 0.0)
        score_gap = best_score - worst_score
        
        print(f"\n{'='*80}")
        print(f"Preference Pair Selection:")
        print(f"  Best score:  {best_score:.2%} (temp={best['temperature']})")
        print(f"  Worst score: {worst_score:.2%} (temp={worst['temperature']})")
        print(f"  Score gap:   {score_gap:.2%}")
        print(f"  Threshold:   {min_score_gap:.2%}")
        print(f"{'='*80}")
        
        if score_gap < min_score_gap:
            print(f"✗ Score gap too small ({score_gap:.2%} < {min_score_gap:.2%})")
            return None
        
        # Step 4: Build preference pair
        preference_pair = {
            "scenario": scenario,
            "timestamp": datetime.utcnow().isoformat(),
            "better": {
                "plan": best['plan']['structured'],
                "analysis": best['plan']['analysis'],
                "temperature": best['temperature'],
                "acrue_score": best_score,
                "passed": best['evaluation'].get('passed', []),
                "partial": best['evaluation'].get('partial', []),
                "failed": best['evaluation'].get('failed', []),
                "feedback": best['evaluation'].get('feedback', {})
            },
            "worse": {
                "plan": worst['plan']['structured'],
                "analysis": worst['plan']['analysis'],
                "temperature": worst['temperature'],
                "acrue_score": worst_score,
                "passed": worst['evaluation'].get('passed', []),
                "partial": worst['evaluation'].get('partial', []),
                "failed": worst['evaluation'].get('failed', []),
                "feedback": worst['evaluation'].get('feedback', {})
            },
            "score_gap": score_gap,
            "key_differences": self._identify_key_differences(best, worst)
        }
        
        print(f"✓ Valid preference pair created!")
        return preference_pair
    
    def _identify_key_differences(self, best: Dict, worst: Dict) -> List[str]:
        """
        Identify key quality differences between best and worst plans.
        
        Args:
            best: Best candidate with evaluation
            worst: Worst candidate with evaluation
        
        Returns:
            List of key differences
        """
        differences = []
        
        # Find assertions that passed in best but failed in worst
        best_passed = set(best['evaluation'].get('passed', []))
        worst_failed = set(worst['evaluation'].get('failed', []))
        critical_differences = best_passed & worst_failed
        
        # Map assertions to human-readable differences
        assertion_meanings = {
            "C2": "Better plan has complete milestone chain",
            "U2": "Better plan identifies backup presenters",
            "A2": "Better plan has realistic timelines",
            "A4": "Better plan assigns tasks to attendees",
            "A5": "Better plan has valid dependencies",
            "C3": "Better plan includes tech readiness check",
            "E1": "Better plan has proactive risk mitigation",
            "E2": "Better plan has contingency plans"
        }
        
        for assertion in critical_differences:
            if assertion in assertion_meanings:
                differences.append(assertion_meanings[assertion])
        
        # Generic difference if no specific ones found
        if not differences:
            differences.append(f"Better plan scores {best['evaluation'].get('score', 0):.0%} vs {worst['evaluation'].get('score', 0):.0%}")
        
        return differences


def main():
    """Generate sample preference pairs for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PFT preference pairs for workback planning")
    parser.add_argument("--vertical", default="QBR", help="Meeting vertical (QBR, M&A, Board)")
    parser.add_argument("--count", type=int, default=1, help="Number of preference pairs to generate")
    parser.add_argument("--output", default="preference_pairs.jsonl", help="Output file")
    args = parser.parse_args()
    
    # Sample scenario for testing
    scenario = """
Meeting: Quarterly Business Review (QBR)
Date: December 15, 2025
Meeting Time: 2:00 PM - 4:00 PM Pacific
Location: Executive Boardroom / Hybrid (Teams)

Attendees:
- CEO: Sarah Johnson (sarah.johnson@company.com)
- CFO: Michael Chen (michael.chen@company.com)
- VP Product: Alice Williams (alice.williams@company.com)
- VP Engineering: Bob Martinez (bob.martinez@company.com)
- VP Sales: Carol Davis (carol.davis@company.com)
- VP Marketing: David Lee (david.lee@company.com)

Meeting Objectives:
1. Review Q4 2025 financial performance vs targets
2. Present product roadmap progress and Q1 2026 plans
3. Discuss customer feedback and market trends
4. Review team capacity and hiring plans
5. Set priorities for Q1 2026

Key Deliverables:
- Financial performance deck (revenue, EBITDA, cash flow)
- Product progress report with key metrics
- Customer satisfaction analysis
- Q1 2026 OKRs and resource allocation

Constraints:
- CFO is traveling Nov 25 - Dec 5, not available for reviews
- Product roadmap needs legal review (7-day SLA)
- All materials must be finalized 3 days before meeting for pre-read
- Tech rehearsal required T-1 (Dec 14)

Historical Context:
- Last QBR (Sep 2025) had technical issues with video conferencing
- Previous decks were 80+ slides, too long
- CEO requested executive summary format (max 30 slides)
"""
    
    # Initialize generator
    print(f"Initializing PFT Preference Pair Generator for {args.vertical}...")
    generator = PreferencePairGenerator()
    
    # Generate preference pairs
    pairs_generated = 0
    with open(args.output, 'w') as f:
        for i in range(args.count):
            print(f"\n{'#'*80}")
            print(f"Generating preference pair {i+1}/{args.count}")
            print(f"{'#'*80}")
            
            pair = generator.generate_preference_pair(scenario)
            
            if pair:
                f.write(json.dumps(pair) + '\n')
                f.flush()
                pairs_generated += 1
                print(f"\n✓ Preference pair {pairs_generated} saved to {args.output}")
            else:
                print(f"\n✗ Failed to generate valid preference pair")
    
    print(f"\n{'#'*80}")
    print(f"Summary: Generated {pairs_generated}/{args.count} preference pairs")
    print(f"Output: {args.output}")
    print(f"{'#'*80}")


if __name__ == "__main__":
    main()
