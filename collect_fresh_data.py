#!/usr/bin/env python3
"""
Fresh Data Collection Pipeline using SilverFlow
Collects calendar, Teams chat, and runs collaborator discovery with latest data

Usage:
    python collect_fresh_data.py [--days DAYS] [--limit LIMIT]
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            encoding='utf-8'
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Collect fresh M365 data and run collaborator discovery"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Days of PAST calendar data to collect (default: 30). Data collected from N days ago to 30 minutes ago."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Limit number of collaborator results (default: 20)"
    )
    parser.add_argument(
        "--skip-chat",
        action="store_true",
        help="Skip Teams chat collection (faster)"
    )
    parser.add_argument(
        "--skip-calendar",
        action="store_true",
        help="Skip calendar collection (use existing data)"
    )
    
    args = parser.parse_args()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("#" * 70)
    print("#  FRESH DATA COLLECTION PIPELINE")
    print("#  Using SilverFlow Production Scripts")
    print("#" * 70)
    print(f"\n⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Calendar Range: PAST {args.days} days (to 30 min ago)")
    print(f"👥 Collaborator Limit: Top {args.limit}")
    print()
    
    success_count = 0
    total_steps = 3 if not args.skip_calendar and not args.skip_chat else (2 if args.skip_calendar or args.skip_chat else 1)
    
    # Step 1: Collect Fresh Calendar Data (PAST N days to 30 mins ago)
    if not args.skip_calendar:
        # Calculate date range: past N days to 30 minutes ago
        now_utc = datetime.now(timezone.utc)
        end_time = now_utc - timedelta(minutes=30)  # 30 minutes ago
        start_time = end_time - timedelta(days=args.days)  # N days before that
        
        start_iso = start_time.isoformat()
        end_iso = end_time.isoformat()
        
        calendar_cmd = (
            f"python SilverFlow/data/graph_get_meetings.py "
            f"\"{start_iso}\" \"{end_iso}\" "
            f"--select \"id,subject,start,end,type,organizer,attendees,bodyPreview,webLink,responseStatus,showAs\""
        )
        
        if run_command(calendar_cmd, f"STEP 1: Collect Calendar Data (Past {args.days} days to 30 min ago)"):
            success_count += 1
            print("✅ Calendar data collected")
            print(f"   📁 Saved to: SilverFlow/data/out/graph_meetings.json")
        else:
            print("⚠️  Calendar collection failed - will try with existing data")
    else:
        print("\n⏭️  Skipping calendar collection (using existing data)")
        success_count += 1
    
    # Step 2: Collect Fresh Teams Chat Data
    if not args.skip_chat:
        if run_command(
            f"python tools/teams_chat_api.py --top 50 --max 100 --days 90",
            "STEP 2: Collect Fresh Teams Chat Data"
        ):
            success_count += 1
            print("✅ Teams chat data collected")
            print(f"   📁 Saved to: data/evaluation_results/teams_chat_analysis_*.json")
        else:
            print("⚠️  Teams chat collection failed - continuing without chat data")
    else:
        print("\n⏭️  Skipping Teams chat collection")
        success_count += 1
    
    # Step 3: Run Collaborator Discovery
    if run_command(
        f"python tools/collaborator_discovery.py "
        f"--calendar-data SilverFlow/data/out/graph_meetings.json "
        f"--limit {args.limit}",
        "STEP 3: Run Collaborator Discovery (with fresh data)"
    ):
        success_count += 1
        print("✅ Collaborator discovery complete")
        print(f"   📁 Results saved to: collaborator_discovery_results_*.json")
    else:
        print("❌ Collaborator discovery failed")
    
    # Summary
    print("\n" + "=" * 70)
    print("  PIPELINE COMPLETE")
    print("=" * 70)
    print(f"\n✅ Successful steps: {success_count}/{total_steps}")
    print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if success_count == total_steps:
        print("🎉 All steps completed successfully!")
        print("💡 Fresh data collected and analyzed with latest information")
        return 0
    elif success_count > 0:
        print("⚠️  Some steps failed, but got partial results")
        return 1
    else:
        print("❌ Pipeline failed - no steps completed")
        return 2

if __name__ == "__main__":
    sys.exit(main())
