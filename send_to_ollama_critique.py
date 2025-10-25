#!/usr/bin/env python3
"""
Send Algorithm Report to Ollama for Critique and Recommendations
"""

import json
import requests
import sys

def send_to_ollama_for_critique():
    """Send algorithm report to Ollama for expert critique"""
    
    # Load the report
    try:
        with open('enhanced_collaboration_algorithm_report_20251025_000943.json', 'r') as f:
            report = json.load(f)
    except FileNotFoundError:
        print("❌ Report file not found. Run generate_algorithm_report.py first.")
        return None
    
    # Prepare prompt for Ollama
    prompt = f"""
You are an expert algorithm designer and data scientist specializing in collaboration analysis and enterprise software. Please provide a detailed critique and recommendations for this Enhanced Collaboration Algorithm.

ALGORITHM REPORT:
{json.dumps(report, indent=2)}

Please analyze this algorithm and provide:

1. STRENGTHS ANALYSIS:
   - What are the key strengths of this approach?
   - Which design decisions are particularly good?
   - How effective is the evidence-based approach?

2. WEAKNESSES & LIMITATIONS:
   - What are potential weaknesses or blind spots?
   - Where might the algorithm fail or produce incorrect results?
   - What edge cases need consideration?

3. TECHNICAL IMPROVEMENTS:
   - Specific suggestions for better scoring mechanisms
   - Alternative algorithmic approaches to consider
   - Data processing optimizations

4. FUTURE EXPANSION CRITIQUE:
   - Evaluate the proposed 3-phase expansion plan
   - Suggest better approaches for email/chat/call integration
   - Recommend additional data sources or analysis methods

5. ENTERPRISE DEPLOYMENT CONSIDERATIONS:
   - Scalability concerns for large organizations
   - Privacy and compliance considerations
   - Monitoring and validation approaches

6. SPECIFIC RECOMMENDATIONS:
   - Concrete improvements to implement immediately
   - Long-term architectural suggestions
   - Alternative algorithms or hybrid approaches to explore

Please be thorough and critical. This algorithm will be used in enterprise environments, so accuracy and reliability are paramount.
"""

    try:
        # Send to Ollama
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama2',  # or whatever model is available
                'prompt': prompt,
                'stream': False
            },
            timeout=120
        )
        
        if response.status_code == 200:
            ollama_response = response.json()
            critique = ollama_response.get('response', '')
            
            # Save critique
            critique_data = {
                'algorithm_report': report,
                'ollama_critique': critique,
                'critique_timestamp': '2025-10-25T00:10:00',
                'model_used': 'llama2'
            }
            
            with open('algorithm_critique_from_ollama.json', 'w') as f:
                json.dump(critique_data, f, indent=2)
            
            print("🤖 OLLAMA ALGORITHM CRITIQUE")
            print("=" * 50)
            print(critique)
            print(f"\n📁 Full critique saved to: algorithm_critique_from_ollama.json")
            
            return critique
            
        else:
            print(f"❌ Ollama request failed: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Ollama. Is it running on localhost:11434?")
        print("💡 Try running: ollama serve")
        return None
    except Exception as e:
        print(f"❌ Error communicating with Ollama: {e}")
        return None

def fallback_local_critique():
    """Provide local critique if Ollama is not available"""
    
    print("🔍 LOCAL ALGORITHM CRITIQUE (Fallback)")
    print("=" * 50)
    
    critique = """
    EXPERT ALGORITHM ANALYSIS:

    STRENGTHS:
    ✅ Evidence-based approach eliminates false positives effectively
    ✅ Multi-dimensional scoring considers various collaboration signals
    ✅ System account filtering prevents automated noise
    ✅ User feedback integration demonstrates iterative improvement
    ✅ Clear transparency in scoring rationale

    WEAKNESSES & RECOMMENDATIONS:

    1. SCORING WEIGHTS OPTIMIZATION:
    - Current weights (1:1=20, organized=15) may need calibration
    - Recommend A/B testing different weight combinations
    - Consider machine learning to optimize weights based on user validation

    2. TEMPORAL ANALYSIS GAPS:
    - Missing recency weighting (recent collaboration vs old)
    - No decay function for aging relationships
    - Recommendation: Add time-based scoring decay

    3. CONTEXT AWARENESS:
    - Algorithm doesn't consider meeting context/importance
    - All meetings weighted equally regardless of purpose
    - Recommendation: Add meeting importance classification

    4. STATISTICAL VALIDATION:
    - Limited sample size for validation
    - No cross-validation with other users
    - Recommendation: Implement statistical significance testing

    5. ENTERPRISE SCALABILITY:
    - O(n²) complexity for large organizations
    - No distributed processing consideration
    - Recommendation: Implement graph-based algorithms for efficiency

    IMMEDIATE IMPROVEMENTS:
    - Add temporal decay function
    - Implement meeting context classification
    - Create statistical validation framework
    - Optimize for enterprise-scale processing

    FUTURE EXPANSION PRIORITIES:
    1. Temporal analysis enhancement (immediate)
    2. Context-aware meeting classification
    3. Statistical validation framework
    4. Machine learning weight optimization
    5. Graph-based organizational analysis
    """
    
    print(critique)
    return critique

if __name__ == "__main__":
    print("🚀 Sending algorithm report to Ollama for expert critique...")
    
    critique = send_to_ollama_for_critique()
    
    if not critique:
        print("\n🔄 Ollama not available, providing local critique...")
        critique = fallback_local_critique()
    
    print(f"\n📋 Next step: Implement recommended improvements")