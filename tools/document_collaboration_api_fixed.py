#!/usr/bin/env python3
"""
THIS IS A FIXED VERSION - Use this to replace the broken analyze_document_collaboration() function
"""

def analyze_document_collaboration(access_token: str, days: int = 30, max_files: int = 50) -> Dict:
    """
    Analyze OUTBOUND document sharing: Who YOU chose to share documents with
    This is the strongest signal - you sharing shows deliberate collaboration intent
    """
    safe_print(f"\n🔍 Analyzing YOUR document sharing patterns (past {days} days)...")
    
    # Get outbound sharing patterns
    patterns = get_document_sharing_patterns(access_token, days, max_files)
    
    collaboration_data = defaultdict(lambda: {
        'documents_shared': [],         # Documents I shared with this person
        'direct_shares': 0,             # 1:1 shares
        'small_group_shares': 0,        # Small group shares (<5 people)
        'collaboration_score': 0,
        'last_share': None
    })
    
    safe_print(f"\n📊 Analyzing {len(patterns['shared_by_me'])} outbound shares...")
    
    direct_count = 0
    group_count = 0
    
    # Analyze documents YOU shared
    for share in patterns['shared_by_me']:
        person_name = share.get('shared_to', '')
        if not person_name or person_name == 'System':
            continue
        
        doc_name = share.get('document_name', 'Unknown')
        share_type = share.get('share_type', 'direct')
        
        # Track the document
        if doc_name not in collaboration_data[person_name]['documents_shared']:
            collaboration_data[person_name]['documents_shared'].append(doc_name)
        
        # Score based on share type
        if share_type == 'direct':
            collaboration_data[person_name]['direct_shares'] += 1
            collaboration_data[person_name]['collaboration_score'] += 15  # VERY STRONG signal
            direct_count += 1
        elif share_type == 'small_group':
            collaboration_data[person_name]['small_group_shares'] += 1
            collaboration_data[person_name]['collaboration_score'] += 10  # STRONG signal
            group_count += 1
    
    safe_print(f"✅ Found {len(collaboration_data)} people YOU shared documents with")
    safe_print(f"   📨 {direct_count} direct (1:1) shares")
    safe_print(f"   👥 {group_count} small group shares")
    
    return dict(collaboration_data)


def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Analyze document collaboration patterns")
    parser.add_argument('--days', type=int, default=30, help="Days of history to analyze (default: 30)")
    parser.add_argument('--max-files', type=int, default=50, help="Maximum files to analyze (default: 50)")
    parser.add_argument('--output', type=str, help="Output JSON file path")
    args = parser.parse_args()
    
    safe_print("🚀 Scenara 2.0 Document Collaboration API")
    safe_print("=" * 60)
    safe_print("")
    safe_print("✅ TRACKING OUTBOUND SHARING (Your Intent):")
    safe_print("   - YOU shared to person (1:1) = +15 pts")
    safe_print("   - YOU shared to small group (<5) = +10 pts")
    safe_print("")
    safe_print("❌ FILTERED OUT:")
    safe_print("   - Documents shared TO you (inbound)")
    safe_print("   - Large group broadcasts")
    safe_print("")
    safe_print("💡 PHILOSOPHY: Direction matters - only YOUR outbound shares count")
    safe_print("=" * 60)
    
    # Authenticate
    safe_print("\n🔐 Authenticating...")
    result = acquire_token_with_broker()
    
    if not result or "access_token" not in result:
        err = (result or {}).get("error_description") or (result or {}).get("error") or "Unknown error"
        safe_print(f"❌ Authentication failed: {err}")
        return 1
    
    access_token = result["access_token"]
    safe_print("✅ Authentication successful")
    
    # Analyze collaboration
    collaboration_data = analyze_document_collaboration(access_token, args.days, args.max_files)
    
    # Prepare output
    output = {
        'analysis_timestamp': datetime.now(timezone.utc).isoformat(),
        'days_analyzed': args.days,
        'max_files': args.max_files,
        'total_collaborators': len(collaboration_data),
        'collaborators': []
    }
    
    # Sort by collaboration score (outbound sharing)
    for person_name, data in sorted(
        collaboration_data.items(),
        key=lambda x: x[1]['collaboration_score'],
        reverse=True
    ):
        docs_shared = data['documents_shared']
        
        output['collaborators'].append({
            'name': person_name,
            'documents_shared': docs_shared[:5],  # Top 5 documents
            'direct_shares': data['direct_shares'],
            'small_group_shares': data['small_group_shares'],
            'total_documents': len(docs_shared),
            'collaboration_score': data['collaboration_score'],
            'last_share': data['last_share']
        })
    
    # Display top collaborators
    safe_print(f"\n📊 People YOU Shared Documents With (OUTBOUND):")
    safe_print("-" * 85)
    safe_print(f"{'#':<3} {'Name':<40} {'Direct':<8} {'Group':<8} {'Docs':<6} {'Score':<6}")
    safe_print("-" * 85)
    for i, collab in enumerate(output['collaborators'][:20], 1):
        direct = collab['direct_shares']
        group = collab['small_group_shares']
        docs = collab['total_documents']
        score = collab['collaboration_score']
        name = collab['name'][:38]
        safe_print(f"{i:<3} {name:<40} {direct:<8} {group:<8} {docs:<6} {score:<6}")
    
    # Save output
    output_dir = Path('data/evaluation_results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"document_collaboration_analysis_{timestamp}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    safe_print(f"\n💾 Saving analysis results...")
    safe_print(f"✅ Results saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
