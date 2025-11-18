#!/usr/bin/env python3
"""
Extract scenario-specific stakeholders from workback dashboard.
Parses the dashboard HTML to identify all unique stakeholders across 33 scenarios.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict
from datetime import datetime

class ScenarioStakeholderExtractor:
    """Extract stakeholders from workback planning scenarios."""
    
    def __init__(self, dashboard_path: str = "workback_dashboard.html"):
        self.dashboard_path = dashboard_path
        self.scenarios = []
        self.stakeholders = {}  # name -> full details
        self.company_map = {}  # stakeholder -> company
        
    def extract_scenarios(self) -> List[Dict[str, Any]]:
        """Extract all scenarios from dashboard."""
        print(f"📖 Reading dashboard: {self.dashboard_path}")
        
        with open(self.dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find scenario sections
        scenario_pattern = r'<div class="scenario-card"[^>]*>(.*?)</div>\s*</div>\s*</div>'
        matches = re.findall(scenario_pattern, content, re.DOTALL)
        
        print(f"✅ Found {len(matches)} scenario sections")
        
        # Extract from JSON data embedded in JavaScript
        json_pattern = r'const scenarios = (\[.*?\]);'
        json_matches = re.search(json_pattern, content, re.DOTALL)
        
        if json_matches:
            try:
                scenarios_json = json_matches.group(1)
                scenarios = json.loads(scenarios_json)
                print(f"✅ Parsed {len(scenarios)} scenarios from JSON")
                self.scenarios = scenarios
                return scenarios
            except:
                pass
        
        # Fallback: parse HTML structure
        print("⚠️  JSON parsing failed, using HTML extraction")
        return self._extract_from_html(content)
    
    def _extract_from_html(self, content: str) -> List[Dict[str, Any]]:
        """Extract scenarios from HTML structure."""
        scenarios = []
        
        # Look for scenario context sections
        context_pattern = r'<strong>Company:</strong>\s*([^<]+).*?<strong>Meeting Type:</strong>\s*([^<]+)'
        matches = re.findall(context_pattern, content, re.DOTALL)
        
        for i, (company, meeting_type) in enumerate(matches, 1):
            scenarios.append({
                'id': f'scenario-{i:03d}',
                'company': company.strip(),
                'meeting_type': meeting_type.strip(),
                'stakeholders': []
            })
        
        print(f"✅ Extracted {len(scenarios)} scenarios from HTML")
        return scenarios
    
    def extract_stakeholders_from_text(self, text: str, company: str) -> List[Dict[str, Any]]:
        """Extract stakeholder names and roles from text."""
        stakeholders = []
        
        # Pattern 1: "Name (Role)" or "Name - Role"
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*[\(–-]\s*([^)\n]+)[\)]?',
            r'<strong>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)</strong>\s*[–-]\s*([^<\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for name, role in matches:
                name = name.strip()
                role = role.strip()
                
                # Filter out false positives
                if len(name.split()) >= 2 and len(name.split()) <= 4:
                    if not any(word in name.lower() for word in ['meeting', 'company', 'team', 'office']):
                        stakeholders.append({
                            'name': name,
                            'role': role,
                            'company': company,
                            'seniority': self._infer_seniority(role)
                        })
        
        return stakeholders
    
    def extract_all_stakeholders(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all stakeholders grouped by company."""
        
        if not self.scenarios:
            self.extract_scenarios()
        
        print(f"\n🔍 Extracting stakeholders from {len(self.scenarios)} scenarios...")
        
        with open(self.dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stakeholders_by_company = defaultdict(list)
        seen_names = set()
        
        # Extract from scenario context sections
        scenario_sections = re.findall(
            r'<h3[^>]*>Scenario \d+:.*?</h3>(.*?)(?=<h3|<section|$)',
            content,
            re.DOTALL
        )
        
        for section in scenario_sections:
            # Extract company
            company_match = re.search(r'<strong>Company:</strong>\s*\*\*([^*]+)\*\*', section)
            if not company_match:
                company_match = re.search(r'<strong>Company:</strong>\s*([^<\n]+)', section)
            
            if company_match:
                company = company_match.group(1).strip()
                # Clean company name
                company = re.sub(r'\s*\(.*?\)', '', company)  # Remove parentheses
                company = company.split(',')[0].strip()  # Take first part before comma
                
                # Extract stakeholders from this section
                stakeholders = self.extract_stakeholders_from_text(section, company)
                
                for stakeholder in stakeholders:
                    name = stakeholder['name']
                    if name not in seen_names:
                        stakeholders_by_company[company].append(stakeholder)
                        seen_names.add(name)
                        self.stakeholders[name] = stakeholder
                        self.company_map[name] = company
        
        print(f"\n✅ Extracted stakeholders:")
        total = 0
        for company, stakeholders in sorted(stakeholders_by_company.items()):
            print(f"   {company}: {len(stakeholders)} stakeholders")
            total += len(stakeholders)
        
        print(f"\n📊 Total unique stakeholders: {total}")
        
        return dict(stakeholders_by_company)
    
    def _infer_seniority(self, role: str) -> str:
        """Infer seniority level from role title."""
        role_lower = role.lower()
        
        if any(keyword in role_lower for keyword in ['ceo', 'cto', 'cfo', 'coo', 'chief', 'president']):
            return 'executive'
        elif any(keyword in role_lower for keyword in ['vp', 'vice president', 'svp']):
            return 'executive'
        elif any(keyword in role_lower for keyword in ['director', 'head of', 'principal']):
            return 'senior'
        elif any(keyword in role_lower for keyword in ['senior', 'sr.', 'sr ', 'lead', 'staff']):
            return 'senior'
        elif any(keyword in role_lower for keyword in ['manager', 'supervisor', 'coordinator']):
            return 'mid'
        elif any(keyword in role_lower for keyword in ['junior', 'jr.', 'jr ', 'associate', 'assistant']):
            return 'junior'
        else:
            return 'mid'  # Default
    
    def save_stakeholder_list(self, output_path: str = "data/scenario_stakeholders.json"):
        """Save extracted stakeholders to JSON file."""
        
        stakeholders_by_company = self.extract_all_stakeholders()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'extracted_at': datetime.now().isoformat(),
            'total_companies': len(stakeholders_by_company),
            'total_stakeholders': len(self.stakeholders),
            'companies': stakeholders_by_company,
            'all_stakeholders': list(self.stakeholders.values())
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved to: {output_file}")
        print(f"📦 File size: {output_file.stat().st_size / 1024:.1f} KB")
        
        return data
    
    def generate_profile_commands(self, output_path: str = "data/generate_scenario_profiles.sh"):
        """Generate shell script to create profiles for all stakeholders."""
        
        if not self.stakeholders:
            self.extract_all_stakeholders()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        script_lines = [
            "#!/bin/bash",
            "# Auto-generated script to create scenario-specific stakeholder profiles",
            "",
            "# Configuration",
            'BASE_URL="http://192.168.2.204:11434"',
            'MODEL="gpt-oss:120b"',
            'OUTPUT_DIR="data/user_profiles/scenario_stakeholders"',
            "",
            "mkdir -p $OUTPUT_DIR",
            "",
            "# Generate profiles",
            ""
        ]
        
        for i, (name, details) in enumerate(self.stakeholders.items(), 1):
            role = details['role']
            company = details['company']
            seniority = details['seniority']
            
            script_lines.append(
                f'echo "[{i}/{len(self.stakeholders)}] Generating profile for {name}..."'
            )
            script_lines.append(
                f'python src/workback_planning/user_profile_generator.py '
                f'--name "{name}" --role "{role}" --company "{company}" '
                f'--seniority "{seniority}" --output "$OUTPUT_DIR/{name.replace(" ", "_").lower()}.json"'
            )
            script_lines.append("")
        
        script_lines.append('echo "✅ All scenario profiles generated!"')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(script_lines))
        
        output_file.chmod(0o755)  # Make executable
        
        print(f"\n📝 Generated script: {output_file}")
        print(f"   Run with: ./{output_file}")
        
        return output_file


def main():
    """Main execution."""
    
    print("=" * 80)
    print("🎯 SCENARIO STAKEHOLDER EXTRACTOR")
    print("=" * 80)
    
    extractor = ScenarioStakeholderExtractor()
    
    # Extract and save stakeholders
    data = extractor.save_stakeholder_list()
    
    # Show summary
    print("\n" + "=" * 80)
    print("📊 EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Total companies: {data['total_companies']}")
    print(f"Total stakeholders: {data['total_stakeholders']}")
    
    # Show top companies
    print("\n🏢 Top Companies by Stakeholder Count:")
    company_counts = [(c, len(s)) for c, s in data['companies'].items()]
    for company, count in sorted(company_counts, key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {company}: {count} stakeholders")
    
    # Show seniority distribution
    seniority_counts = defaultdict(int)
    for stakeholder in data['all_stakeholders']:
        seniority_counts[stakeholder['seniority']] += 1
    
    print("\n👥 Seniority Distribution:")
    for seniority, count in sorted(seniority_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {seniority.capitalize()}: {count}")
    
    print("\n" + "=" * 80)
    print("💡 Next Steps:")
    print("   1. Review: cat data/scenario_stakeholders.json | python -m json.tool | less")
    print("   2. Generate profiles: python src/workback_planning/batch_profile_generator.py --scenario-specific")
    print("=" * 80)


if __name__ == "__main__":
    main()
