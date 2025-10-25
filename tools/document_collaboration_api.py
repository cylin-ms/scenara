#!/usr/bin/env python3
"""
Document Collaboration Analysis - Targeted Sharing Signals

FOCUS: DIRECT/TARGETED sharing as collaboration signal
✅ I shared to specific person/small group = STRONG signal (intent to collaborate)
✅ Specific person shared to me = STRONG signal (they want to collaborate)
❌ Broadcast sharing to large groups = WEAK signal (filtered out)

APPROACH:
1. Get documents shared WITH me → Extract sharer name
2. Get documents I shared → Extract recipients (TODO: need share permissions API)
3. Filter: Only count shares to individuals or small groups (<5 people)
4. Score: Targeted sharing = +10 points, Broadcast = +1 point (filtered)

LIMITATIONS:
- Cannot detect if document was opened/commented
- Cannot get MY outbound share recipients easily (Graph API limitation)
- Focus on INBOUND targeted shares as primary signal
"""

import json
import os
import sys
import io
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from collections import defaultdict
from pathlib import Path

import msal
import requests

# Configuration
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
CLIENT_ID = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
GRAPH_SCOPES = ["https://graph.microsoft.com/.default"]  # Use .default scope like SilverFlow
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
GRAPH_BETA_URL = "https://graph.microsoft.com/beta"  # For richer collaboration features

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def safe_print(*args, **kwargs):
    """Print with UTF-8 encoding support for Windows"""
    sep = kwargs.pop('sep', ' ')
    end = kwargs.pop('end', '\n')
    file = kwargs.pop('file', sys.stdout)
    text = sep.join(str(a) for a in args)
    try:
        file.write(text + end)
        file.flush()
    except Exception:
        pass


def _login_hint():
    """Get login hint from environment"""
    user = os.getenv("USERNAME") or os.getenv("USER") or ""
    return f"{user}@microsoft.com" if user else None


def acquire_token_with_broker():
    """Acquire access token using MSAL + Windows Broker (WAM)"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=authority,
        enable_broker_on_windows=True,
    )

    login_hint = _login_hint()
    account = None
    
    try:
        if login_hint:
            accs = app.get_accounts(username=login_hint)
            if accs:
                account = accs[0]
                safe_print(f"   Found cached account: {account.get('username', 'Unknown')}")
        if not account:
            accs = app.get_accounts()
            if accs:
                account = accs[0]
                safe_print(f"   Found cached account: {account.get('username', 'Unknown')}")
    except Exception as e:
        safe_print(f"   ⚠️  Error checking cached accounts: {e}")

    # Try silent token acquisition first
    if account:
        safe_print("   Attempting silent token acquisition...")
        result = app.acquire_token_silent(GRAPH_SCOPES, account=account)
        if result and "access_token" in result:
            safe_print("   ✅ Got token from cache")
            return result
        safe_print("   ⚠️  Silent acquisition failed, need interactive login")

    # Interactive authentication
    safe_print("   🔐 Opening browser/login dialog...")
    safe_print("   ⏳ Please complete authentication in the browser window...")
    result = app.acquire_token_interactive(
        GRAPH_SCOPES,
        login_hint=login_hint,
        parent_window_handle=msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE,
    )
    return result


def get_document_sharing_patterns(access_token: str, days: int = 30, max_items: int = 100) -> Dict:
    """
    Get OUTBOUND sharing patterns: Documents YOU shared with others
    Strategy: Get your OneDrive files, check permissions to see who you shared with
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
    
    collaboration_patterns = {
        'shared_by_me': [],         # Documents I shared with specific people
    }
    
    # Get YOUR OneDrive files (recent)
    safe_print("� Fetching YOUR documents from OneDrive...")
    my_files_url = f"{GRAPH_BASE_URL}/me/drive/root/children"
    
    try:
        params = {'$top': max_items, '$select': 'id,name,lastModifiedDateTime,webUrl'}
        response = requests.get(my_files_url, headers=headers, params=params, timeout=30)
        if response.ok:
            files = response.json().get('value', [])
            safe_print(f"   ✅ Found {len(files)} files in your OneDrive")
            
            # For each file, check permissions to see who YOU shared with
            safe_print("📊 Checking sharing permissions...")
            shared_count = 0
            
            for file_info in files[:max_items]:
                file_id = file_info.get('id', '')
                file_name = file_info.get('name', '')
                file_url = file_info.get('webUrl', '')
                
                if not file_id:
                    continue
                
                # Get permissions for this file
                perm_url = f"{GRAPH_BASE_URL}/me/drive/items/{file_id}/permissions"
                try:
                    perm_response = requests.get(perm_url, headers=headers, timeout=10)
                    if perm_response.ok:
                        permissions = perm_response.json().get('value', [])
                        
                        # Check each permission
                        for perm in permissions:
                            # Skip inherited/default permissions
                            if perm.get('inheritedFrom'):
                                continue
                            
                            # Look for specific user grants (not links)
                            granted_to = perm.get('grantedTo', {})
                            granted_to_identities = perm.get('grantedToIdentities', [])
                            
                            # Single user permission
                            if granted_to:
                                user = granted_to.get('user', {})
                                user_name = user.get('displayName', '')
                                user_email = user.get('email', '')
                                
                                if user_name:
                                    collaboration_patterns['shared_by_me'].append({
                                        'document_name': file_name,
                                        'document_id': file_id,
                                        'document_url': file_url,
                                        'shared_to': user_name,
                                        'shared_to_email': user_email,
                                        'roles': perm.get('roles', []),
                                        'share_type': 'direct'
                                    })
                                    shared_count += 1
                            
                            # Multiple users (small group)
                            elif granted_to_identities and len(granted_to_identities) <= 5:  # Small group
                                for identity in granted_to_identities:
                                    user = identity.get('user', {})
                                    user_name = user.get('displayName', '')
                                    user_email = user.get('email', '')
                                    
                                    if user_name:
                                        collaboration_patterns['shared_by_me'].append({
                                            'document_name': file_name,
                                            'document_id': file_id,
                                            'document_url': file_url,
                                            'shared_to': user_name,
                                            'shared_to_email': user_email,
                                            'roles': perm.get('roles', []),
                                            'share_type': 'small_group'
                                        })
                                        shared_count += 1
                    
                except Exception as e:
                    continue  # Skip files with permission errors
            
            safe_print(f"   ✅ Found {shared_count} outbound shares to specific people")
        else:
            safe_print(f"   ⚠️  HTTP {response.status_code}")
    except Exception as e:
        safe_print(f"   ❌ Error: {e}")
    
    return collaboration_patterns


def get_teams_chat_attachments(access_token: str, days: int = 30, max_chats: int = 50) -> Dict:
    """
    Get file attachments YOU shared in Teams chats and meeting chats
    
    Strategy:
    1. Get recent Teams chats (1:1, group, meeting)
    2. Fetch messages from each chat
    3. Find messages with attachments that YOU sent
    4. Extract recipient information from chat members
    
    Returns:
        Dict with 'shared_in_chats' list of attachment shares
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
    
    chat_attachments = {
        'shared_in_chats': [],  # Files YOU shared in Teams chats
    }
    
    # Get current user info to identify YOUR messages
    safe_print("\n📱 Fetching Teams chat attachments...")
    try:
        me_url = f"{GRAPH_BASE_URL}/me"
        me_response = requests.get(me_url, headers=headers, params={'$select': 'displayName,mail,userPrincipalName'}, timeout=10)
        if not me_response.ok:
            safe_print(f"   ⚠️  Failed to get user info: {me_response.status_code}")
            return chat_attachments
        
        me_data = me_response.json()
        my_name = me_data.get('displayName', '')
        my_email = me_data.get('mail', '') or me_data.get('userPrincipalName', '')
        safe_print(f"   👤 User: {my_name}")
        
        # Get recent chats
        chats_url = f"{GRAPH_BASE_URL}/me/chats"
        chats_response = requests.get(
            chats_url, 
            headers=headers, 
            params={'$top': max_chats, '$expand': 'members'},
            timeout=30
        )
        
        if not chats_response.ok:
            safe_print(f"   ⚠️  Failed to get chats: {chats_response.status_code}")
            return chat_attachments
        
        chats = chats_response.json().get('value', [])
        safe_print(f"   ✅ Found {len(chats)} recent chats")
        
        # Calculate cutoff date
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        total_attachments = 0
        chats_with_attachments = 0
        
        # Check each chat for attachments
        safe_print(f"   🔍 Checking messages for attachments YOU sent...")
        for chat in chats[:max_chats]:
            chat_id = chat.get('id', '')
            chat_type = chat.get('chatType', 'unknown')
            chat_topic = chat.get('topic', '') or f"{chat_type} chat"
            
            # Get chat members (who you shared with)
            members = chat.get('members', [])
            recipients = []
            for member in members:
                member_name = member.get('displayName', '')
                if member_name and member_name != my_name:
                    recipients.append(member_name)
            
            if not recipients:
                safe_print(f"      ⚠️  Skipping chat {chat_id[:20]}... (no other members)")
                continue  # Skip if no other members
            
            # Determine share type
            if chat_type == 'oneOnOne':
                share_type = 'direct'
            elif len(recipients) <= 4:  # Small group (≤5 total people including you)
                share_type = 'small_group'
            else:
                continue  # Skip large group chats
            
            # Get messages from this chat
            messages_url = f"{GRAPH_BASE_URL}/me/chats/{chat_id}/messages"
            try:
                messages_response = requests.get(
                    messages_url,
                    headers=headers,
                    params={'$top': 50},  # Removed $select - causing 400 errors
                    timeout=10
                )
                
                if not messages_response.ok:
                    safe_print(f"      ⚠️  Failed to get messages: {messages_response.status_code}")
                    continue
                
                messages = messages_response.json().get('value', [])
                safe_print(f"      ✓ Chat with {', '.join(recipients[:2])} ({chat_type}): {len(messages)} messages")
                chat_has_attachments = False
                
                for msg in messages:
                    # Check if message is recent
                    created = msg.get('createdDateTime', '')
                    if created:
                        try:
                            msg_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
                            if msg_date < cutoff_date:
                                continue
                        except:
                            pass
                    
                    # Check if YOU sent this message
                    from_info = msg.get('from') or {}
                    if not isinstance(from_info, dict):
                        continue
                    
                    user_info = from_info.get('user') or {}
                    if not isinstance(user_info, dict):
                        continue
                    
                    from_name = user_info.get('displayName', '')
                    from_email = user_info.get('userPrincipalName', '') or user_info.get('email', '')
                    
                    # Skip if not from you
                    if from_name != my_name and from_email != my_email:
                        continue
                    
                    # Check for attachments
                    attachments = msg.get('attachments', [])
                    if not attachments:
                        continue
                    
                    # Process attachments YOU sent
                    for att in attachments:
                        att_name = att.get('name', 'Unknown')
                        att_type = att.get('contentType', '')
                        
                        # Filter for actual file attachments (not inline images, etc.)
                        # 'reference' type = file shared from OneDrive/SharePoint
                        # 'application/*' = Office documents, PDFs, etc.
                        if att_type == 'reference' or 'application' in att_type or 'document' in att_type.lower():
                            # Add to results for each recipient
                            for recipient in recipients:
                                chat_attachments['shared_in_chats'].append({
                                    'document_name': att_name,
                                    'shared_to': recipient,
                                    'share_type': share_type,
                                    'chat_type': chat_type,
                                    'chat_topic': chat_topic,
                                    'shared_date': created
                                })
                                total_attachments += 1
                            
                            chat_has_attachments = True
                
                if chat_has_attachments:
                    chats_with_attachments += 1
                    
            except Exception as e:
                safe_print(f"      ❌ Error checking chat: {e}")
                continue  # Skip chats with errors
        
        safe_print(f"   ✅ Found {total_attachments} file attachments in {chats_with_attachments} chats")
        
    except Exception as e:
        safe_print(f"   ❌ Error: {e}")
    
    return chat_attachments


def analyze_document_collaboration(access_token: str, days: int = 30, max_files: int = 50, max_chats: int = 50) -> Dict:
    """
    Analyze OUTBOUND document sharing: Who YOU chose to share documents with
    Combines:
    1. OneDrive file permission shares
    2. Teams chat file attachments
    
    This is the strongest signal - you sharing shows deliberate collaboration intent
    """
    safe_print(f"\n🔍 Analyzing YOUR document sharing patterns (past {days} days)...")
    
    # Get both types of outbound sharing
    onedrive_patterns = get_document_sharing_patterns(access_token, days, max_files)
    teams_patterns = get_teams_chat_attachments(access_token, days, max_chats)
    
    collaboration_data = defaultdict(lambda: {
        'documents_shared': [],         # Documents I shared with this person
        'chat_attachments': [],         # Files shared via Teams chat
        'direct_shares': 0,             # 1:1 shares (OneDrive)
        'small_group_shares': 0,        # Small group shares (OneDrive)
        'chat_direct': 0,               # 1:1 chat attachments
        'chat_group': 0,                # Small group chat attachments
        'collaboration_score': 0,
        'last_share': None,
        'first_share': None,
        'share_dates': [],              # All sharing timestamps for frequency analysis
        'sharing_days': 0               # Number of unique days with sharing activity
    })
    
    safe_print(f"\n📊 Processing sharing data...")
    
    # Get current user info for filtering
    me_url = f"{GRAPH_BASE_URL}/me"
    me_response = requests.get(me_url, headers={'Authorization': f'Bearer {access_token}'}, params={'$select': 'displayName'}, timeout=10)
    my_name = me_response.json().get('displayName', '') if me_response.ok else ''
    
    # Known former employees to filter out (optional)
    FORMER_EMPLOYEES = {'Jin-Ge Yao', 'Zhiwei Yu'}
    
    # Process OneDrive permission shares
    direct_count = 0
    group_count = 0
    filtered_self = 0
    filtered_former = 0
    
    for share in onedrive_patterns['shared_by_me']:
        person_name = share.get('shared_to', '')
        if not person_name or person_name == 'System':
            continue
        
        # Filter out self-sharing
        if person_name == my_name:
            filtered_self += 1
            continue
        
        # Filter out former employees
        if person_name in FORMER_EMPLOYEES:
            filtered_former += 1
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
        
        # Note: OneDrive permissions don't have timestamps, so we can't track temporal patterns for these
    
    # Process Teams chat attachments
    chat_direct_count = 0
    chat_group_count = 0
    chat_filtered_self = 0
    chat_filtered_former = 0
    
    for attachment in teams_patterns['shared_in_chats']:
        person_name = attachment.get('shared_to', '')
        if not person_name or person_name == 'System':
            continue
        
        # Filter out self
        if person_name == my_name:
            chat_filtered_self += 1
            continue
        
        # Filter out former employees
        if person_name in FORMER_EMPLOYEES:
            chat_filtered_former += 1
            continue
        
        doc_name = attachment.get('document_name', 'Unknown')
        share_type = attachment.get('share_type', 'direct')
        chat_type = attachment.get('chat_type', '')
        shared_date = attachment.get('shared_date', '')
        
        # Track the attachment
        chat_info = f"{doc_name} (via {chat_type} chat)"
        if chat_info not in collaboration_data[person_name]['chat_attachments']:
            collaboration_data[person_name]['chat_attachments'].append(chat_info)
        
        # Track temporal data
        if shared_date:
            collaboration_data[person_name]['share_dates'].append(shared_date)
            
            # Update last_share (most recent)
            if not collaboration_data[person_name]['last_share'] or shared_date > collaboration_data[person_name]['last_share']:
                collaboration_data[person_name]['last_share'] = shared_date
            
            # Update first_share (earliest)
            if not collaboration_data[person_name]['first_share'] or shared_date < collaboration_data[person_name]['first_share']:
                collaboration_data[person_name]['first_share'] = shared_date
        
        # Score based on chat type
        if share_type == 'direct':
            collaboration_data[person_name]['chat_direct'] += 1
            collaboration_data[person_name]['collaboration_score'] += 12  # STRONG signal (chat = intent)
            chat_direct_count += 1
        elif share_type == 'small_group':
            collaboration_data[person_name]['chat_group'] += 1
            collaboration_data[person_name]['collaboration_score'] += 8  # GOOD signal
            chat_group_count += 1
    
    # Calculate temporal bonuses
    now = datetime.now(timezone.utc)
    for person_name, data in collaboration_data.items():
        if data['share_dates']:
            # Calculate unique sharing days
            unique_dates = set()
            for date_str in data['share_dates']:
                try:
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    unique_dates.add(dt.date())
                except:
                    pass
            data['sharing_days'] = len(unique_dates)
            
            # Recency bonus (last share within...)
            if data['last_share']:
                try:
                    last_dt = datetime.fromisoformat(data['last_share'].replace('Z', '+00:00'))
                    days_since = (now - last_dt).days
                    
                    if days_since <= 7:
                        data['collaboration_score'] += 20  # Last week: +20 pts
                    elif days_since <= 30:
                        data['collaboration_score'] += 15  # Last month: +15 pts
                    elif days_since <= 90:
                        data['collaboration_score'] += 10  # Last quarter: +10 pts
                    elif days_since <= 180:
                        data['collaboration_score'] += 5   # Last 6 months: +5 pts
                except:
                    pass
            
            # Continuity bonus (sharing across multiple days)
            if data['sharing_days'] >= 5:
                data['collaboration_score'] += 15  # 5+ days: +15 pts (sustained collaboration)
            elif data['sharing_days'] >= 3:
                data['collaboration_score'] += 10  # 3-4 days: +10 pts
            elif data['sharing_days'] >= 2:
                data['collaboration_score'] += 5   # 2 days: +5 pts
    
    safe_print(f"\n✅ Document sharing summary:")
    safe_print(f"   📁 OneDrive: {direct_count} direct, {group_count} group shares")
    safe_print(f"   💬 Teams chat: {chat_direct_count} direct, {chat_group_count} group attachments")
    safe_print(f"   ❌ Filtered: {filtered_self + chat_filtered_self} self-shares, {filtered_former + chat_filtered_former} former employees")
    safe_print(f"   👥 Total collaborators: {len(collaboration_data)}")
    
    return dict(collaboration_data)


def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Analyze document collaboration patterns")
    parser.add_argument('--days', type=int, default=30, help="Days of history to analyze (default: 30)")
    parser.add_argument('--max-files', type=int, default=50, help="Maximum OneDrive files to check (default: 50)")
    parser.add_argument('--max-chats', type=int, default=50, help="Maximum Teams chats to check (default: 50)")
    parser.add_argument('--output', type=str, help="Output JSON file path")
    args = parser.parse_args()
    
    safe_print("🚀 Scenara 2.0 Document Collaboration API")
    safe_print("=" * 70)
    safe_print("")
    safe_print("✅ TRACKING OUTBOUND SHARING (Your Intent):")
    safe_print("   📁 OneDrive permissions: Direct (1:1) = +15 pts, Group (<5) = +10 pts")
    safe_print("   💬 Teams chat attachments: Direct (1:1) = +12 pts, Group (<5) = +8 pts")
    safe_print("")
    safe_print("❌ FILTERED OUT:")
    safe_print("   - Documents shared TO you (inbound)")
    safe_print("   - Large group broadcasts (>5 people)")
    safe_print("")
    safe_print("💡 PHILOSOPHY: Direction matters - only YOUR outbound shares count")
    safe_print("=" * 70)
    
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
    collaboration_data = analyze_document_collaboration(access_token, args.days, args.max_files, args.max_chats)
    
    # Prepare output
    output = {
        'analysis_timestamp': datetime.now(timezone.utc).isoformat(),
        'days_analyzed': args.days,
        'max_files': args.max_files,
        'max_chats': args.max_chats,
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
        chat_attachments = data['chat_attachments']
        
        # Calculate recency label
        recency_label = 'N/A'
        if data['last_share']:
            try:
                last_dt = datetime.fromisoformat(data['last_share'].replace('Z', '+00:00'))
                days_ago = (datetime.now(timezone.utc) - last_dt).days
                if days_ago <= 7:
                    recency_label = f'{days_ago}d'  # Days ago
                elif days_ago <= 30:
                    recency_label = f'{days_ago}d'
                elif days_ago <= 365:
                    recency_label = f'{days_ago//30}mo'  # Months ago
                else:
                    recency_label = f'{days_ago//365}y'  # Years ago
            except:
                pass
        
        output['collaborators'].append({
            'name': person_name,
            'documents_shared': docs_shared[:5],  # Top 5 OneDrive documents
            'chat_attachments': chat_attachments[:5],  # Top 5 chat attachments
            'direct_shares': data['direct_shares'],
            'small_group_shares': data['small_group_shares'],
            'chat_direct': data['chat_direct'],
            'chat_group': data['chat_group'],
            'total_documents': len(docs_shared),
            'total_chat_attachments': len(chat_attachments),
            'collaboration_score': data['collaboration_score'],
            'last_share': data['last_share'],
            'first_share': data['first_share'],
            'sharing_days': data['sharing_days'],
            'recency_label': recency_label
        })
    
    # Display top collaborators
    safe_print(f"\n📊 People YOU Shared Documents With (OUTBOUND):")
    safe_print("-" * 115)
    safe_print(f"{'#':<3} {'Name':<30} {'OneDrive':<12} {'Chat':<12} {'Days':<6} {'Last':<8} {'Score':<6}")
    safe_print(f"{'':3} {'':30} {'D/G':<12} {'D/G':<12} {'':6} {'':8} {'':<6}")
    safe_print("-" * 115)
    for i, collab in enumerate(output['collaborators'][:20], 1):
        onedrive = f"{collab['direct_shares']}/{collab['small_group_shares']}"
        chat = f"{collab['chat_direct']}/{collab['chat_group']}"
        sharing_days = collab.get('sharing_days', 0)
        recency = collab.get('recency_label', 'N/A')
        score = collab['collaboration_score']
        name = collab['name'][:28]
        safe_print(f"{i:<3} {name:<30} {onedrive:<12} {chat:<12} {sharing_days:<6} {recency:<8} {score:<6}")
    
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
