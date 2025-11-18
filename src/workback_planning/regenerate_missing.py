"""
Regenerate missing workback plans and scenarios

Identifies and regenerates only the missing scenarios and plans
from the full generation run.
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.workback_planning.generate_test_scenarios import ScenarioGenerator, MEETING_TYPES

DATA_DIR = Path("data/workback_scenarios")


def find_missing():
    """Find missing scenarios and plans"""
    master = json.load(open(DATA_DIR / "master_index.json"))
    
    missing_scenarios = []
    missing_plans = []
    
    for meeting_type, info in master.get("summary_by_type", {}).items():
        expected_scenarios = 3
        actual_scenarios = info.get("scenarios", 0)
        
        # Check for missing scenarios
        for scenario_num in range(1, expected_scenarios + 1):
            scenario_file = DATA_DIR / f"{meeting_type}_scenario_{scenario_num}.json"
            if not scenario_file.exists():
                missing_scenarios.append((meeting_type, scenario_num))
        
        # Check for missing plans (only for existing scenarios)
        for scenario_num in range(1, actual_scenarios + 1):
            for quality in ["low", "medium", "high"]:
                plan_file = DATA_DIR / f"{meeting_type}_scenario_{scenario_num}_{quality}.json"
                if not plan_file.exists():
                    missing_plans.append((meeting_type, scenario_num, quality))
    
    return missing_scenarios, missing_plans


def regenerate_missing():
    """Regenerate missing scenarios and plans"""
    missing_scenarios, missing_plans = find_missing()
    
    print(f"🔍 Found {len(missing_scenarios)} missing scenarios")
    print(f"🔍 Found {len(missing_plans)} missing plans")
    print()
    
    if not missing_scenarios and not missing_plans:
        print("✅ No missing files! All scenarios and plans are complete.")
        return
    
    generator = ScenarioGenerator()
    
    # Regenerate missing scenarios (which will also generate their plans)
    for meeting_type_key, scenario_num in missing_scenarios:
        print(f"📝 Regenerating {meeting_type_key} scenario {scenario_num}...")
        
        try:
            # Generate scenario
            scenario = generator.generate_scenario(meeting_type_key, scenario_num)
            
            if scenario:
                # Save scenario
                scenario_file = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}.json"
                with open(scenario_file, 'w') as f:
                    json.dump(scenario, f, indent=2)
                print(f"💾 Saved scenario to: {scenario_file.name}")
                
                # Generate all three quality plans
                for quality in ["low", "medium", "high"]:
                    print(f"  🔄 Generating {quality.upper()} quality plan...")
                    plan = generator.generate_workback_plan(scenario, quality)
                    if plan:
                        plan_file = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}_{quality}.json"
                        with open(plan_file, 'w') as f:
                            json.dump(plan, f, indent=2)
                        print(f"  ✅ {quality.upper()} plan complete")
                
                print(f"✅ Completed {meeting_type_key} scenario {scenario_num}\n")
        except Exception as e:
            print(f"❌ Failed: {e}\n")
    
    # Regenerate missing individual plans
    for meeting_type_key, scenario_num, quality in missing_plans:
        print(f"🔄 Regenerating {meeting_type_key} scenario {scenario_num} ({quality})...")
        
        try:
            # Load existing scenario
            scenario_file = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}.json"
            if not scenario_file.exists():
                print(f"⚠️  Scenario file not found, skipping...")
                continue
            
            scenario = json.load(open(scenario_file))
            
            # Generate the missing plan
            plan = generator.generate_workback_plan(scenario, quality)
            
            if plan:
                plan_file = DATA_DIR / f"{meeting_type_key}_scenario_{scenario_num}_{quality}.json"
                with open(plan_file, 'w') as f:
                    json.dump(plan, f, indent=2)
                print(f"✅ Completed {meeting_type_key} scenario {scenario_num} ({quality})\n")
            else:
                print(f"❌ Failed to generate plan\n")
        except Exception as e:
            print(f"❌ Failed: {e}\n")
    
    print("\n" + "="*70)
    print("REGENERATION COMPLETE")
    print("="*70)
    
    # Recheck status
    missing_scenarios_after, missing_plans_after = find_missing()
    print(f"\n📊 Final Status:")
    print(f"   Remaining missing scenarios: {len(missing_scenarios_after)}")
    print(f"   Remaining missing plans: {len(missing_plans_after)}")
    
    if missing_scenarios_after or missing_plans_after:
        print("\n⚠️  Some files still missing. May need manual review.")
    else:
        print("\n🎉 All files successfully regenerated!")


if __name__ == "__main__":
    regenerate_missing()
