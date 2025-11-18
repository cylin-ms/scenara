#!/usr/bin/env python3
"""
Batch User Profile Generator
Generates profiles for all stakeholders in workback planning scenarios.
Runs in the background using remote Ollama server.
"""

import json
import os
import sys
import time
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.llm_api import LLMAPIClient

class BatchProfileGenerator:
    """Generate user profiles for all stakeholders in batch mode."""
    
    def __init__(
        self, 
        llm_provider: str = "ollama", 
        model: str = "gpt-oss:120b",
        base_url: str = "http://192.168.2.204:11434"
    ):
        """
        Initialize batch profile generator.
        
        Args:
            llm_provider: LLM provider (ollama, openai, anthropic)
            model: Model name (default: gpt-oss:120b)
            base_url: Base URL for remote Ollama server
        """
        self.llm_client = LLMAPIClient()
        self.provider = llm_provider
        self.model = model
        self.base_url = base_url
        
    def extract_stakeholders_from_dashboard(self, dashboard_path: str) -> List[Dict[str, Any]]:
        """
        Extract unique stakeholders from the workback dashboard HTML.
        
        Args:
            dashboard_path: Path to dashboard HTML file
            
        Returns:
            List of stakeholder dictionaries with role, company, etc.
        """
        print(f"📖 Reading dashboard from: {dashboard_path}")
        
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        stakeholders = []
        seen_names = set()
        
        # Extract from org chart sections
        # Pattern: name in stakeholder cards with roles
        patterns = [
            # Executive Leadership pattern
            r'<div class="stakeholder-name">([^<]+)</div>\s*<div class="stakeholder-role">([^<]+)</div>',
            # Participants list pattern
            r'<strong>([^<]+)</strong>\s*-\s*([^<\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            for name, role in matches:
                name = name.strip()
                role = role.strip()
                
                if name and role and name not in seen_names:
                    # Infer company from context (simplified)
                    company = self._infer_company(name, role)
                    seniority = self._infer_seniority(role)
                    
                    stakeholders.append({
                        'name': name,
                        'role': role,
                        'seniority': seniority,
                        'company': company
                    })
                    seen_names.add(name)
        
        print(f"✅ Extracted {len(stakeholders)} unique stakeholders")
        return stakeholders
    
    def _infer_company(self, name: str, role: str) -> str:
        """Infer company from role/title."""
        # Common company indicators in roles
        company_keywords = {
            'Microsoft': ['Microsoft', 'Azure', 'M365'],
            'TechCorp': ['TechCorp', 'Tech Corp'],
            'Acme': ['Acme'],
            'GlobalTech': ['GlobalTech', 'Global Tech'],
        }
        
        for company, keywords in company_keywords.items():
            for keyword in keywords:
                if keyword.lower() in role.lower():
                    return company
        
        # Default company
        return "Enterprise Organization"
    
    def _infer_seniority(self, role: str) -> str:
        """Infer seniority level from role title."""
        role_lower = role.lower()
        
        if any(keyword in role_lower for keyword in ['ceo', 'cto', 'cfo', 'coo', 'chief', 'vp', 'vice president']):
            return 'executive'
        elif any(keyword in role_lower for keyword in ['director', 'head of', 'lead', 'principal', 'senior manager']):
            return 'senior'
        elif any(keyword in role_lower for keyword in ['manager', 'supervisor', 'team lead', 'scrum master']):
            return 'mid'
        elif any(keyword in role_lower for keyword in ['senior', 'sr.', 'staff']):
            return 'senior'
        elif any(keyword in role_lower for keyword in ['junior', 'jr.', 'associate']):
            return 'junior'
        else:
            return 'mid'  # Default
    
    def generate_profile(
        self,
        name: str,
        role: str,
        seniority: str,
        company: str,
        industry: str = "Technology",
        company_size: str = "large"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a comprehensive user profile.
        
        Args:
            name: Person's name
            role: Job role/title
            seniority: Career level (junior, mid, senior, executive)
            company: Company name
            industry: Industry context
            company_size: Company size (startup, small, medium, large, enterprise)
            
        Returns:
            Complete user profile dictionary or None on failure
        """
        
        prompt = f"""Generate a realistic, detailed professional profile for {name}, a {seniority}-level {role} at {company}.

Create a comprehensive persona that includes:

1. BASIC INFORMATION:
   - Full name: {name}
   - Age (appropriate for {seniority} seniority)
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
   - Myers-Briggs type (MBTI)
   - Decision-making approach
   - Risk tolerance
   - Collaboration style
   - Stress management approach
   - Conflict resolution style

4. SKILLS & EXPERTISE:
   - Core technical skills (rated 1-10)
   - Leadership abilities (rated 1-10)
   - Domain expertise areas
   - Learning agility (1-10)
   - Tools proficiency
   - Languages spoken

5. PERFORMANCE METRICS:
   - Task completion rate (%)
   - Quality score (%)
   - Estimation accuracy (%)
   - Multitasking ability (1-10)
   - Performance under pressure (1-10)

6. AVAILABILITY & CONSTRAINTS:
   - Available hours per week
   - Timezone and working hours
   - Planned time off (days/year)
   - Other commitments
   - Travel flexibility

7. PERSONAL FACTORS:
   - Family status (impacts availability)
   - Caregiving responsibilities
   - Commute situation
   - Health considerations
   - Career motivation

8. PROJECT IMPACT FACTORS:
   - Reliability (1-10)
   - Innovation tendency (1-10)
   - Documentation quality (1-10)
   - Mentorship capability (1-10)
   - Influence level (1-10)

9. COLLABORATION PATTERNS:
   - Meeting frequency preference
   - Communication channels preference
   - Feedback style (direct / diplomatic)
   - Knowledge sharing habits
   - Cross-team collaboration (1-10)

10. RISK FACTORS:
    - Potential bottlenecks
    - Backup person needed
    - Ramp-up time for new projects (weeks)
    - Context-switching tolerance (1-10)
    - Burnout risk factors

Output ONLY a valid JSON object (no markdown, no code blocks) with this structure:
{{
  "basic_info": {{}},
  "work_habits": {{}},
  "personality": {{}},
  "skills": {{}},
  "performance": {{}},
  "availability": {{}},
  "personal_factors": {{}},
  "project_impact": {{}},
  "collaboration": {{}},
  "risk_factors": {{}}
}}

Make the profile realistic with specific numbers, percentages, and concrete details.
Include both strengths AND weaknesses. Consider {industry} industry context and {company_size} company size.
"""

        try:
            response = self.llm_client.query_llm(
                prompt=prompt,
                provider=self.provider,
                model=self.model,
                temperature=0.8,  # Higher for creative diversity
                base_url=self.base_url
            )
            
            # Try to parse JSON from response
            # Remove markdown code blocks if present
            response = response.strip()
            if response.startswith('```'):
                # Extract content between code blocks
                lines = response.split('\n')
                json_lines = []
                in_code_block = False
                for line in lines:
                    if line.strip().startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block or not line.strip().startswith('```'):
                        json_lines.append(line)
                response = '\n'.join(json_lines)
            
            profile = json.loads(response)
            
            # Add metadata
            profile['_metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'name': name,
                'role': role,
                'seniority': seniority,
                'company': company,
                'model': self.model,
                'provider': self.provider
            }
            
            return profile
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error for {name}: {e}")
            print(f"Raw response preview: {response[:500]}")
            return None
        except Exception as e:
            print(f"❌ Error generating profile for {name}: {e}")
            return None
    
    def generate_all_profiles(
        self,
        stakeholders: List[Dict[str, Any]],
        output_dir: str = "data/user_profiles/stakeholders",
        resume_from: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate profiles for all stakeholders in batch.
        
        Args:
            stakeholders: List of stakeholder dicts
            output_dir: Directory to save profiles
            resume_from: Resume from specific stakeholder name (optional)
            
        Returns:
            Summary statistics
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print("=" * 80)
        print(f"🚀 BATCH PROFILE GENERATION")
        print("=" * 80)
        print(f"📊 Total stakeholders: {len(stakeholders)}")
        print(f"🤖 Model: {self.model}")
        print(f"🌐 Server: {self.base_url}")
        print(f"💾 Output: {output_path}")
        print("=" * 80)
        
        # Resume logic
        start_index = 0
        if resume_from:
            for i, s in enumerate(stakeholders):
                if s['name'] == resume_from:
                    start_index = i
                    print(f"🔄 Resuming from: {resume_from} (index {start_index})")
                    break
        
        profiles = []
        failed = []
        skipped = 0
        
        start_time = time.time()
        
        for i, stakeholder in enumerate(stakeholders[start_index:], start=start_index):
            name = stakeholder['name']
            role = stakeholder['role']
            seniority = stakeholder['seniority']
            company = stakeholder['company']
            
            print(f"\n[{i+1}/{len(stakeholders)}] Generating profile for {name}...")
            print(f"   Role: {role}")
            print(f"   Seniority: {seniority}")
            print(f"   Company: {company}")
            
            # Check if profile already exists
            profile_file = output_path / f"{name.replace(' ', '_').lower()}.json"
            if profile_file.exists():
                print(f"   ⏭️  Profile already exists, skipping...")
                skipped += 1
                continue
            
            profile = self.generate_profile(
                name=name,
                role=role,
                seniority=seniority,
                company=company
            )
            
            if profile:
                # Save individual profile
                with open(profile_file, 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2, ensure_ascii=False)
                
                profiles.append(profile)
                print(f"   ✅ Saved to {profile_file.name}")
            else:
                failed.append({
                    'name': name,
                    'role': role,
                    'reason': 'generation_failed'
                })
                print(f"   ❌ Failed to generate profile")
            
            # Progress update every 10 profiles
            if (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                avg_time = elapsed / (i + 1 - start_index)
                remaining = avg_time * (len(stakeholders) - i - 1)
                print(f"\n📊 Progress: {i+1}/{len(stakeholders)} ({(i+1)/len(stakeholders)*100:.1f}%)")
                print(f"⏱️  Elapsed: {elapsed/60:.1f}min | Est. remaining: {remaining/60:.1f}min")
        
        # Save summary
        total_time = time.time() - start_time
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_stakeholders': len(stakeholders),
            'profiles_generated': len(profiles),
            'profiles_failed': len(failed),
            'profiles_skipped': skipped,
            'failed_details': failed,
            'model': self.model,
            'provider': self.provider,
            'total_time_seconds': total_time,
            'avg_time_per_profile': total_time / len(profiles) if profiles else 0
        }
        
        summary_file = output_path / f"_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 80)
        print("✅ BATCH GENERATION COMPLETE")
        print("=" * 80)
        print(f"✅ Profiles generated: {len(profiles)}")
        print(f"⏭️  Profiles skipped: {skipped}")
        print(f"❌ Profiles failed: {len(failed)}")
        print(f"⏱️  Total time: {total_time/60:.1f} minutes")
        print(f"📊 Average time: {total_time/len(profiles):.1f}s per profile" if profiles else "")
        print(f"💾 Output directory: {output_path}")
        print(f"📄 Summary saved: {summary_file}")
        print("=" * 80)
        
        return summary


def main():
    """Main execution - generate all stakeholder profiles."""
    
    # Configuration
    dashboard_path = "workback_dashboard.html"
    output_dir = "data/user_profiles/stakeholders"
    
    print("🎭 Batch User Profile Generator")
    print("=" * 80)
    
    # Initialize generator
    generator = BatchProfileGenerator(
        llm_provider="ollama",
        model="gpt-oss:120b",
        base_url="http://192.168.2.204:11434"
    )
    
    # Define comprehensive stakeholder list for enterprise scenarios
    print("Using comprehensive stakeholder list for enterprise scenarios...")
    
    stakeholders = [
        # Executive Leadership
        {'name': 'Sarah Chen', 'role': 'CEO', 'seniority': 'executive', 'company': 'TechCorp'},
        {'name': 'Michael Rodriguez', 'role': 'CTO', 'seniority': 'executive', 'company': 'TechCorp'},
        {'name': 'Jennifer Kim', 'role': 'VP of Engineering', 'seniority': 'executive', 'company': 'TechCorp'},
        {'name': 'David Thompson', 'role': 'CFO', 'seniority': 'executive', 'company': 'TechCorp'},
        {'name': 'Rachel Martinez', 'role': 'Chief Product Officer', 'seniority': 'executive', 'company': 'TechCorp'},
        
        # Senior Leadership
        {'name': 'James Wilson', 'role': 'VP of Sales', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Emily Watson', 'role': 'VP of Marketing', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Robert Johnson', 'role': 'VP of Operations', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Lisa Anderson', 'role': 'VP of Human Resources', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Kevin Brown', 'role': 'Director of Engineering', 'seniority': 'senior', 'company': 'TechCorp'},
        
        # Directors & Managers
        {'name': 'Amanda Lee', 'role': 'Director of Product Management', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Christopher Davis', 'role': 'Director of Customer Success', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Michelle Garcia', 'role': 'Engineering Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Daniel Park', 'role': 'Product Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Jessica Taylor', 'role': 'Marketing Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Engineering Team
        {'name': 'Alex Nguyen', 'role': 'Senior Software Engineer', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Priya Sharma', 'role': 'Senior Software Engineer', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Marcus Johnson', 'role': 'Software Engineer', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Sophie Zhang', 'role': 'Software Engineer', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Jamal Williams', 'role': 'DevOps Engineer', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Product & Design
        {'name': 'Nina Patel', 'role': 'Senior Product Manager', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Carlos Rivera', 'role': 'UX/UI Designer', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Emma Thompson', 'role': 'UX Researcher', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Data & Analytics
        {'name': 'Ryan O\'Connor', 'role': 'Data Scientist', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Olivia Martinez', 'role': 'Data Analyst', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Thomas Wright', 'role': 'Business Intelligence Engineer', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Quality & Testing
        {'name': 'Laura Bennett', 'role': 'QA Lead', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Hassan Ahmed', 'role': 'QA Engineer', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Maria Santos', 'role': 'Test Automation Engineer', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Sales & Customer Success
        {'name': 'Jonathan Miller', 'role': 'Sales Director', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Rebecca Foster', 'role': 'Account Executive', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Tyler Jackson', 'role': 'Customer Success Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Marketing & Communications
        {'name': 'Samantha Brooks', 'role': 'Content Marketing Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Andrew Chen', 'role': 'Growth Marketing Lead', 'seniority': 'senior', 'company': 'TechCorp'},
        {'name': 'Victoria Lopez', 'role': 'Communications Specialist', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Operations & Support
        {'name': 'Brandon Mitchell', 'role': 'IT Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Catherine Lee', 'role': 'Operations Coordinator', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Gregory Hall', 'role': 'Technical Support Lead', 'seniority': 'mid', 'company': 'TechCorp'},
        
        # Finance & Legal
        {'name': 'Patricia Anderson', 'role': 'Finance Manager', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Richard Moore', 'role': 'Legal Counsel', 'seniority': 'senior', 'company': 'TechCorp'},
        
        # HR & People Operations
        {'name': 'Angela Robinson', 'role': 'HR Business Partner', 'seniority': 'mid', 'company': 'TechCorp'},
        {'name': 'Steven Clark', 'role': 'Talent Acquisition Manager', 'seniority': 'mid', 'company': 'TechCorp'},
    ]
    
    # Generate all profiles
    summary = generator.generate_all_profiles(
        stakeholders=stakeholders,
        output_dir=output_dir
    )
    
    print(f"\n🎉 All done! Check {output_dir}/ for individual profiles")


if __name__ == "__main__":
    main()
