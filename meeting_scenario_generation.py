import argparse
import json
import torch
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from str2bool import str2bool
import os
from meeting_prep_taxonomy import get_random_meeting_scenario, format_scenario_description

def meeting_scenario_generation_prompt():
    """Generate prompt for creating meeting preparation scenarios"""
    
    prompt = """As an expert in enterprise meeting management and workplace productivity, generate ONE realistic and challenging meeting preparation scenario for training an AI assistant.

=== SCENARIO GENERATION TASK ===
Create a detailed meeting scenario that combines:
1. A specific meeting type with clear purpose and participants
2. Realistic workplace challenges or complications
3. Available context/resources for preparation
4. Specific preparation needs

=== EVALUATION CRITERIA ===
Your scenario should be selected based on one of these priorities:
1. HIGH-STAKES SITUATION - Critical meetings with significant business impact
2. COMPLEX DYNAMICS - Multiple stakeholders with different interests/concerns
3. RESOURCE CONSTRAINTS - Limited time, data, or preparation resources
4. COMMON PAIN POINT - Frequent workplace situations requiring expert preparation

=== REQUIRED OUTPUT FORMAT ===
Provide your response as a JSON object enclosed within code fence markers:

```json
{
  "scenario": "<detailed scenario description>",
  "meeting_type": "<type of meeting>", 
  "participants": ["<list of participant roles>"],
  "stakes": "<low/medium/high/extremely high>",
  "challenges": ["<list of specific challenges>"],
  "available_context": ["<list of available information/resources>"],
  "preparation_question": "<specific question asking how to prepare for this meeting>"
}
```

=== FORMAT REQUIREMENTS ===
- The JSON must be enclosed with ```json at the beginning and ``` at the end
- All fields must be present and properly formatted
- The scenario should be detailed enough to provide specific context
- The preparation_question should be specific to the scenario, not generic
- Example of correct format:
  ```json
  {
    "scenario": "A Quarterly Business Review with the board where you must present Q3 results, but the revenue targets were missed by 15% due to a major client cancellation, and two board members have already expressed concerns about the strategic direction. The meeting is in 2 days and you need to present both the shortfall analysis and a recovery plan.",
    "meeting_type": "Quarterly Business Review",
    "participants": ["CEO", "board members", "CFO", "VP Sales"],
    "stakes": "extremely high",
    "challenges": ["missed revenue targets", "skeptical board members", "short preparation time", "need recovery plan"],
    "available_context": ["Q3 financial data", "client cancellation details", "previous board feedback", "competitor analysis"],
    "preparation_question": "How should I prepare for this QBR meeting to address the revenue shortfall while maintaining board confidence?"
  }
  ```

=== IMPORTANT NOTES ===
- Your response should consist ONLY of the code-fenced JSON object
- Do not include any explanatory text before or after the JSON
- Focus on realistic enterprise scenarios that would benefit from expert preparation advice
- Ensure the scenario has enough specificity to enable targeted preparation guidance
- The preparation_question should be something a real employee might ask an AI assistant
"""

    return prompt

def meeting_preparation_response_prompt(scenario_json):
    """Generate prompt for creating meeting preparation responses given a scenario"""
    
    scenario = json.loads(scenario_json) if isinstance(scenario_json, str) else scenario_json
    
    prompt = f"""As an expert meeting preparation consultant, provide comprehensive preparation guidance for the following scenario:

=== MEETING SCENARIO ===
{scenario['scenario']}

Meeting Type: {scenario['meeting_type']}
Participants: {', '.join(scenario['participants'])}
Stakes: {scenario['stakes']}
Challenges: {', '.join(scenario['challenges'])}
Available Resources: {', '.join(scenario['available_context'])}

=== PREPARATION QUESTION ===
{scenario['preparation_question']}

=== RESPONSE REQUIREMENTS ===
Provide a detailed, actionable preparation plan that addresses:

1. **OBJECTIVES & SUCCESS CRITERIA**
   - Clear meeting goals and desired outcomes
   - How to measure meeting success

2. **AGENDA & STRUCTURE**
   - Recommended agenda outline
   - Time allocation for each section
   - Key discussion points

3. **STAKEHOLDER ANALYSIS**
   - Participant concerns and motivations
   - Potential objections or resistance
   - Strategies for different personality types

4. **CONTENT PREPARATION**
   - Key materials to gather/prepare
   - Data points and supporting evidence
   - Visual aids or presentations needed

5. **RISK MITIGATION**
   - Potential issues and contingency plans
   - Difficult questions and prepared responses
   - Backup strategies if things go poorly

6. **LOGISTICS & SETUP**
   - Pre-meeting preparations
   - Technology/equipment needs
   - Follow-up planning

=== QUALITY CRITERIA ===
Your response must be:
- **SPECIFIC**: Tailored to this exact scenario, not generic advice
- **ACTIONABLE**: Concrete steps the person can take
- **COMPREHENSIVE**: Covers all aspects of preparation
- **REALISTIC**: Considers time and resource constraints
- **STRATEGIC**: Addresses the stakes and challenges mentioned

=== OUTPUT FORMAT ===
Structure your response as a clear, well-organized preparation plan with numbered sections and bullet points for easy execution.
"""

    return prompt

def generate_meeting_scenarios(args):
    """Generate meeting scenarios using the specified model"""
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    
    # Load model
    model = LLM(
        model=args.model_path,
        tokenizer=args.model_path,
        tokenizer_mode="slow",
        dtype=args.dtype,
        tensor_parallel_size=args.n_gpus,
        seed=args.seed,
        enforce_eager=True,
        disable_custom_all_reduce=True,
        trust_remote_code=args.trust_remote_code,
    )
    
    # Setup sampling parameters
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_len,
    )
    
    # Generate scenarios
    scenarios = []
    prompt = meeting_scenario_generation_prompt()
    
    if args.use_chat_template:
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        formatted_prompt = prompt
    
    print(f"Generating {args.num_scenarios} meeting scenarios...")
    
    # Generate multiple scenarios
    prompts = [formatted_prompt] * args.num_scenarios
    outputs = model.generate(prompts, sampling_params)
    
    for i, output in enumerate(outputs):
        generated_text = output.outputs[0].text.strip()
        
        # Try to extract JSON from the response
        try:
            if "```json" in generated_text:
                json_start = generated_text.find("```json") + 7
                json_end = generated_text.find("```", json_start)
                json_str = generated_text[json_start:json_end].strip()
                scenario_data = json.loads(json_str)
                scenario_data["id"] = i
                scenarios.append(scenario_data)
                print(f"Successfully generated scenario {i+1}")
            else:
                print(f"Warning: No JSON found in output {i+1}")
        except Exception as e:
            print(f"Error parsing scenario {i+1}: {e}")
    
    return scenarios

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default="meeting_prep_scenarios.jsonl")
    parser.add_argument("--num_scenarios", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--max_len", type=int, default=2048)
    parser.add_argument("--n_gpus", type=int, default=1)
    parser.add_argument("--dtype", type=str, default="bfloat16")
    parser.add_argument("--trust_remote_code", type=str2bool, default=False)
    parser.add_argument("--use_chat_template", type=str2bool, default=True)
    
    args = parser.parse_args()
    
    # Generate scenarios
    scenarios = generate_meeting_scenarios(args)
    
    # Save scenarios
    with open(args.output_path, 'w') as f:
        for scenario in scenarios:
            f.write(json.dumps(scenario) + '\n')
    
    print(f"Generated {len(scenarios)} scenarios and saved to {args.output_path}")

if __name__ == "__main__":
    main()