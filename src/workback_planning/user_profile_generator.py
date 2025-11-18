#!/usr/bin/env python3
"""
User Profile Generator for Workback Planning

Generates realistic user profiles with comprehensive attributes that impact project success:
- Work habits and preferences
- Personality and communication style
- Skills and expertise levels
- Performance metrics
- Availability and constraints
- Family/personal factors

Uses gpt-oss:120b for generating authentic, diverse personas.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import random

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.llm_api import LLMAPIClient


class UserProfileGenerator:
    """Generate realistic user profiles for workback planning scenarios."""
    
    def __init__(self, llm_provider: str = "ollama", model: str = "gpt-oss:120b", base_url: Optional[str] = None):
        """
        Initialize the profile generator.
        
        Args:
            llm_provider: LLM provider (ollama, openai, anthropic)
            model: Model name (default: gpt-oss:120b)
            base_url: Base URL for remote Ollama server (optional)
        """
        self.llm_client = LLMAPIClient()
        self.provider = llm_provider
        self.model = model
        self.base_url = base_url
        
    def generate_profile(
        self,
        role: str,
        seniority: str = "mid",
        industry: Optional[str] = None,
        company_size: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive user profile.
        
        Args:
            role: Job role/title (e.g., "Software Engineer", "Product Manager")
            seniority: Career level (junior, mid, senior, lead, executive)
            industry: Industry context (optional)
            company_size: Company size (startup, small, medium, large, enterprise)
            
        Returns:
            Complete user profile dictionary
        """
        
        prompt = f"""Generate a realistic, detailed professional profile for a {seniority}-level {role}.

Create a comprehensive persona that includes:

1. BASIC INFORMATION:
   - Full name (realistic, diverse)
   - Age (appropriate for seniority)
   - Location (timezone consideration)
   - Years of experience
   - Education background

2. WORK HABITS & PREFERENCES:
   - Preferred working hours (early bird / night owl / flexible)
   - Peak productivity times
   - Communication style (async/sync preference, response time)
   - Meeting preferences (minimizes meetings / prefers face-to-face / etc.)
   - Work environment (remote / hybrid / office)
   - Focus time requirements

3. PERSONALITY & WORKING STYLE:
   - Myers-Briggs type or similar indicator
   - Decision-making approach (analytical / intuitive / collaborative)
   - Risk tolerance (conservative / moderate / aggressive)
   - Collaboration style (team player / independent / mentor)
   - Stress management approach
   - Conflict resolution style

4. SKILLS & EXPERTISE:
   - Core technical/functional skills (rate 1-10)
   - Leadership abilities (if applicable)
   - Domain expertise areas
   - Learning agility
   - Tools proficiency
   - Languages spoken

5. PERFORMANCE METRICS:
   - Typical task completion rate (% on-time)
   - Quality consistency (% error-free)
   - Estimation accuracy (typically over/under/accurate)
   - Multitasking ability (low/medium/high)
   - Deadline pressure response (thrives/manages/struggles)
   - Average work hours per week

6. AVAILABILITY & CONSTRAINTS:
   - Regular availability (hours per week)
   - Timezone
   - Vacation/PTO tendencies (minimal / moderate / frequent)
   - Other commitments (courses, side projects, etc.)
   - Travel requirements (if any)

7. PERSONAL FACTORS IMPACTING WORK:
   - Family status (single / partnered / children)
   - Caregiving responsibilities
   - Commute time (if applicable)
   - Health/wellness routine impact
   - Financial motivation level
   - Career ambitions

8. PROJECT IMPACT FACTORS:
   - Reliability score (1-10)
   - Innovation contribution (low/medium/high)
   - Documentation quality (poor/adequate/excellent)
   - Mentorship capability (if applicable)
   - Blockers/dependencies handling
   - Escalation comfort level

9. COLLABORATION PATTERNS:
   - Typical collaboration frequency
   - Preferred communication channels
   - Feedback style (direct / diplomatic / coaching)
   - Knowledge sharing tendency
   - Cross-functional effectiveness

10. RISK FACTORS FOR PROJECT PLANNING:
    - Potential bottleneck areas
    - Backup/redundancy needs
    - Training/ramp-up time for new areas
    - Context-switching overhead
    - Historical project challenge patterns"""

        if industry:
            prompt += f"\n\nIndustry context: {industry}"
        if company_size:
            prompt += f"\nCompany size: {company_size}"
            
        prompt += """

Generate a realistic, nuanced profile. Include specific numbers, percentages, and concrete details. 
Make the person feel real with both strengths and realistic weaknesses/constraints.

Output as JSON with the following structure:
{
  "basic_info": {...},
  "work_habits": {...},
  "personality": {...},
  "skills": {...},
  "performance": {...},
  "availability": {...},
  "personal_factors": {...},
  "project_impact": {...},
  "collaboration": {...},
  "risk_factors": {...}
}"""

        print(f"🤖 Generating profile for {seniority} {role}...")
        print(f"   Provider: {self.provider}, Model: {self.model}")
        if self.base_url:
            print(f"   Base URL: {self.base_url}")
        
        response = self.llm_client.query_llm(
            prompt=prompt,
            provider=self.provider,
            model=self.model,
            temperature=0.8,  # Higher for creative diversity
            base_url=self.base_url
        )
        
        # Parse JSON from response
        try:
            # Try to find JSON in response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                profile = json.loads(json_str)
                
                # Add metadata
                profile['metadata'] = {
                    'generated_at': datetime.now().isoformat(),
                    'generator': 'UserProfileGenerator',
                    'model': self.model,
                    'provider': self.provider,
                    'role': role,
                    'seniority': seniority,
                    'industry': industry,
                    'company_size': company_size
                }
                
                return profile
            else:
                print("⚠️ Could not find JSON in response")
                return self._create_fallback_profile(role, seniority)
                
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error: {e}")
            print("Raw response preview:", response[:500])
            return self._create_fallback_profile(role, seniority)
    
    def _create_fallback_profile(self, role: str, seniority: str) -> Dict[str, Any]:
        """Create a basic fallback profile if LLM generation fails."""
        return {
            "basic_info": {
                "name": f"{seniority.title()} {role}",
                "role": role,
                "seniority": seniority,
                "note": "Fallback profile - LLM generation failed"
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "UserProfileGenerator",
                "status": "fallback"
            }
        }
    
    def generate_team(
        self,
        team_composition: List[Dict[str, str]],
        industry: Optional[str] = None,
        company_size: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate profiles for an entire team.
        
        Args:
            team_composition: List of dicts with 'role' and 'seniority' keys
            industry: Industry context
            company_size: Company size
            
        Returns:
            List of user profiles
        """
        profiles = []
        
        print(f"\n🎭 Generating {len(team_composition)} team member profiles...")
        
        for i, member in enumerate(team_composition, 1):
            role = member.get('role', 'Team Member')
            seniority = member.get('seniority', 'mid')
            
            print(f"\n[{i}/{len(team_composition)}] Generating profile...")
            
            profile = self.generate_profile(
                role=role,
                seniority=seniority,
                industry=industry,
                company_size=company_size
            )
            
            profiles.append(profile)
            
        return profiles
    
    def save_profiles(self, profiles: List[Dict[str, Any]], output_file: str):
        """Save generated profiles to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "total_profiles": len(profiles),
            "profiles": profiles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved {len(profiles)} profiles to {output_path}")
        print(f"📦 File size: {output_path.stat().st_size / 1024:.1f} KB")


def main():
    """Example usage and testing."""
    
    # Example 1: Single profile using remote Ollama
    generator = UserProfileGenerator(
        llm_provider="ollama", 
        model="gpt-oss:120b",
        base_url="http://192.168.2.204:11434"
    )
    
    print("=" * 80)
    print("EXAMPLE 1: Generate Single Profile")
    print("=" * 80)
    
    profile = generator.generate_profile(
        role="Software Engineer",
        seniority="senior",
        industry="SaaS Technology",
        company_size="medium"
    )
    
    print("\n📋 Generated Profile Summary:")
    if 'basic_info' in profile:
        print(f"   Name: {profile['basic_info'].get('name', 'N/A')}")
        print(f"   Role: {profile['basic_info'].get('role', 'N/A')}")
        print(f"   Experience: {profile['basic_info'].get('years_of_experience', 'N/A')} years")
    
    # Save single profile
    generator.save_profiles(
        [profile],
        "data/user_profiles/sample_profile.json"
    )
    
    # Example 2: Generate team
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Generate Product Team")
    print("=" * 80)
    
    team_composition = [
        {"role": "Product Manager", "seniority": "senior"},
        {"role": "Software Engineer", "seniority": "senior"},
        {"role": "Software Engineer", "seniority": "mid"},
        {"role": "UX Designer", "seniority": "mid"},
        {"role": "QA Engineer", "seniority": "mid"},
    ]
    
    team_profiles = generator.generate_team(
        team_composition=team_composition,
        industry="Enterprise Software",
        company_size="large"
    )
    
    print("\n📊 Team Profile Summary:")
    for i, profile in enumerate(team_profiles, 1):
        if 'basic_info' in profile:
            name = profile['basic_info'].get('name', 'N/A')
            role = profile['basic_info'].get('role', 'N/A')
            print(f"   {i}. {name} - {role}")
    
    # Save team profiles
    generator.save_profiles(
        team_profiles,
        f"data/user_profiles/product_team_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    print("\n" + "=" * 80)
    print("✅ User Profile Generation Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
