#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teams Chat API Integration
Scenara 2.0 - Enterprise Meeting Intelligence

Microsoft Graph API Chat.Read implementation based on SilverFlow patterns.
Provides Teams chat collaboration data for collaborator discovery and Me Notes generation.

Features:
- MSAL authentication with Windows Broker (WAM)
- List Teams chats with lastMessagePreview
- Fetch messages from specific chats
- Automatic pagination support
- Temporal analysis (recency, frequency)
- Ad hoc collaboration detection

Based on SilverFlow implementation:
- graph_list_chats_last_preview.py (500 lines)
- graph_list_my_sent_messages.py (609 lines)

Authentication:
- Scopes: Chat.Read, User.Read, openid, profile, offline_access
- Client ID: 9ce97a32-d9ab-4ab2-aadc-f49b39b94e11
- Tenant ID: 72f988bf-86f1-41af-91ab-2d7cd011db47 (Microsoft)
- Windows Broker: enable_broker_on_windows=True

Author: Scenara 2.0 Team
Date: October 25, 2025
"""

import os
import sys
import json
import msal
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Configuration
GRAPH_RESOURCE = os.getenv('GRAPH_RESOURCE', 'https://graph.microsoft.com')
TENANT_ID = os.getenv('GRAPH_TENANT_ID', '72f988bf-86f1-41af-91ab-2d7cd011db47')
CLIENT_ID = os.getenv('GRAPH_CLIENT_ID', '9ce97a32-d9ab-4ab2-aadc-f49b39b94e11')
SCOPES = ["Chat.Read", "User.Read", "openid", "profile", "offline_access"]
DEFAULT_TOP = 50
DEFAULT_MAX = 200
OUT_DIR = Path("data/evaluation_results")


class TeamsChatAPI:
    """
    Microsoft Graph API Teams Chat integration.
    
    Provides access to Teams chat data for collaboration analysis:
    - List chats with message previews
    - Fetch messages from specific chats
    - Analyze chat patterns and recency
    - Detect ad hoc collaboration
    """
    
    def __init__(self, verbose: bool = False):
        """Initialize Teams Chat API client."""
        self.verbose = verbose
        self.token = None
        self.current_user_id = None
        self.current_user_name = None
        
    def _safe_print(self, *args, **kwargs):
        """Print text defensively for Windows consoles."""
        if not self.verbose:
            return
        sep = kwargs.pop('sep', ' ')
        end = kwargs.pop('end', '\n')
        file = kwargs.pop('file', sys.stdout)
        text = sep.join(str(a) for a in args)
        try:
            file.write(text + end)
        except UnicodeEncodeError:
            enc = getattr(file, 'encoding', None) or 'utf-8'
            safe = text.encode(enc, errors='replace').decode(enc, errors='replace')
            file.write(safe + end)
    
    def _login_hint(self) -> Optional[str]:
        """Derive login hint from environment."""
        user = os.getenv('USERNAME') or os.getenv('USER')
        return f"{user}@microsoft.com" if user else None
    
    def acquire_token(self) -> str:
        """
        Acquire access token using MSAL with Windows Broker.
        
        Returns:
            Access token string
            
        Raises:
            RuntimeError: If token acquisition fails
        """
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        
        try:
            app = msal.PublicClientApplication(
                CLIENT_ID,
                authority=authority,
                enable_broker_on_windows=True,
            )
            broker_enabled = True
            self._safe_print("✅ Windows Broker (WAM) enabled for authentication")
        except Exception as e:
            self._safe_print(f"⚠️ Windows Broker not available: {e}")
            app = msal.PublicClientApplication(
                CLIENT_ID,
                authority=authority,
                enable_broker_on_windows=False,
            )
            broker_enabled = False
        
        # Try silent acquisition first
        login_hint = self._login_hint()
        account = None
        
        try:
            if login_hint:
                accounts = app.get_accounts(username=login_hint)
                if accounts:
                    account = accounts[0]
            if not account:
                accounts = app.get_accounts()
                if accounts:
                    account = accounts[0]
        except Exception:
            pass
        
        if account:
            result = app.acquire_token_silent(SCOPES, account=account)
            if result and "access_token" in result:
                self._safe_print("✅ Token acquired silently from cache")
                self.token = result["access_token"]
                return self.token
        
        # Interactive acquisition
        kwargs: Dict[str, Any] = {"scopes": SCOPES}
        if login_hint:
            kwargs["login_hint"] = login_hint
        if broker_enabled:
            kwargs["parent_window_handle"] = msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE
        
        self._safe_print("🔐 Requesting interactive authentication...")
        result = app.acquire_token_interactive(**kwargs)
        
        if result and "access_token" in result:
            self._safe_print(f"✅ Token acquired for {result.get('id_token_claims', {}).get('preferred_username', 'user')}")
            self.token = result["access_token"]
            
            # Extract user info from token claims
            claims = result.get('id_token_claims', {})
            self.current_user_name = claims.get('name', claims.get('preferred_username', 'Unknown'))
            
            return self.token
        
        error = result.get('error_description', 'Unknown error') if result else 'No result'
        raise RuntimeError(f"Failed to acquire token: {error}")
    
    def _graph_get(self, url: str) -> Tuple[Optional[Any], Optional[str]]:
        """
        Execute GET request to Microsoft Graph API.
        
        Args:
            url: Full Graph API URL
            
        Returns:
            Tuple of (response_data, error_message)
        """
        if not self.token:
            self.acquire_token()
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        
        self._safe_print(f"[debug] GET {url}")
        
        try:
            resp = requests.get(url, headers=headers, timeout=60)
        except Exception as ex:
            return None, f"Network error: {ex}"
        
        if resp.status_code >= 400:
            return None, f"HTTP {resp.status_code} {resp.reason}: {resp.text[:400]}"
        
        try:
            return resp.json(), None
        except Exception as ex:
            return None, f"Failed to parse JSON: {ex}"
    
    def _parse_timestamp(self, iso_str: str) -> Optional[datetime]:
        """Parse ISO 8601 timestamp with 'Z' suffix."""
        if not iso_str or not isinstance(iso_str, str):
            return None
        try:
            if iso_str.endswith('Z'):
                return datetime.fromisoformat(iso_str[:-1]).replace(tzinfo=timezone.utc)
            return datetime.fromisoformat(iso_str)
        except Exception:
            return None
    
    def relative_age(self, iso_str: str) -> str:
        """Format timestamp as relative age (e.g., '2d', '3w', '1mo')."""
        dt = self._parse_timestamp(iso_str)
        if not dt:
            return '—'
        
        now = datetime.now(timezone.utc)
        delta = now - dt.astimezone(timezone.utc)
        seconds = int(delta.total_seconds())
        
        if seconds < 0:
            seconds = 0
        if seconds < 60:
            return f"{seconds}s"
        
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}m"
        
        hours = minutes // 60
        if hours < 24:
            return f"{hours}h"
        
        days = hours // 24
        if days < 7:
            return f"{days}d"
        
        weeks = days // 7
        if weeks < 5:
            return f"{weeks}w"
        
        months = days // 30
        if months < 12:
            return f"{months}mo"
        
        years = days // 365
        return f"{years}y"
    
    def list_chats(self, top: int = DEFAULT_TOP, max_results: int = DEFAULT_MAX) -> List[Dict]:
        """
        List Teams chats with lastMessagePreview, ordered by recency.
        
        Args:
            top: Page size (default 50)
            max_results: Maximum total results (default 200, 0 = unlimited)
            
        Returns:
            List of chat dictionaries with metadata and message previews
        """
        chats = []
        url = (
            f"{GRAPH_RESOURCE}/v1.0/chats?"
            f"$expand=lastMessagePreview&"
            f"$orderby=lastMessagePreview/createdDateTime desc&"
            f"$top={top}"
        )
        
        self._safe_print(f"📥 Fetching Teams chats (top={top}, max={max_results})...")
        
        while url:
            data, error = self._graph_get(url)
            
            if error:
                self._safe_print(f"❌ Error fetching chats: {error}")
                break
            
            if not data or 'value' not in data:
                self._safe_print("⚠️ No chat data in response")
                break
            
            batch = data['value']
            chats.extend(batch)
            self._safe_print(f"✅ Fetched {len(batch)} chats (total: {len(chats)})")
            
            # Check pagination
            if max_results > 0 and len(chats) >= max_results:
                chats = chats[:max_results]
                self._safe_print(f"✅ Reached max results limit: {max_results}")
                break
            
            # Get next page
            url = data.get('@odata.nextLink')
            if not url:
                self._safe_print("✅ No more pages")
                break
        
        self._safe_print(f"📊 Total chats retrieved: {len(chats)}")
        return chats
    
    def get_chat_messages(self, chat_id: str, top: int = 50) -> List[Dict]:
        """
        Fetch messages from a specific chat.
        
        Args:
            chat_id: Teams chat ID
            top: Maximum messages to fetch (default 50)
            
        Returns:
            List of message dictionaries ordered by recency
        """
        url = (
            f"{GRAPH_RESOURCE}/v1.0/chats/{chat_id}/messages?"
            f"$top={top}&"
            f"$orderby=createdDateTime desc"
        )
        
        messages = []
        data, error = self._graph_get(url)
        
        if error:
            self._safe_print(f"❌ Error fetching messages for chat {chat_id}: {error}")
            return messages
        
        if data and 'value' in data:
            messages = data['value']
            self._safe_print(f"✅ Fetched {len(messages)} messages from chat {chat_id}")
        
        return messages
    
    def analyze_chat_collaborators(self, chats: List[Dict], days_lookback: int = 90) -> Dict[str, Dict]:
        """
        Analyze chat data to identify collaboration patterns.
        
        Args:
            chats: List of chat dictionaries from list_chats()
            days_lookback: How many days to analyze (default 90)
            
        Returns:
            Dictionary mapping collaborator names to collaboration metrics:
            {
                "Collaborator Name": {
                    "chat_count": int,  # Number of chats with this person
                    "message_count": int,  # Estimated message count
                    "last_chat_date": str,  # ISO timestamp of most recent chat
                    "days_since_last_chat": int,
                    "chat_type": str,  # "oneOnOne" or "group"
                    "recency_score": float,  # Temporal recency score
                    "is_recent": bool,  # Chatted in last 30 days
                    "is_frequent": bool,  # 5+ chats in lookback period
                }
            }
        """
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=days_lookback)
        
        collaborators = {}
        
        for chat in chats:
            # Skip if no last message preview
            last_msg = chat.get('lastMessagePreview')
            if not last_msg:
                continue
            
            # Check if within lookback period
            created_str = last_msg.get('createdDateTime', '')
            created_dt = self._parse_timestamp(created_str)
            if not created_dt or created_dt < cutoff:
                continue
            
            # Get chat participants from members (for 1:1 detection)
            chat_type = chat.get('chatType', 'unknown')
            
            # Extract collaborator from message sender
            from_info = last_msg.get('from') or {}
            user_info = from_info.get('user') or {}
            collaborator_name = user_info.get('displayName', 'Unknown')
            
            # Skip messages without valid sender information
            if not from_info or not user_info or collaborator_name == 'Unknown':
                # Try to get chat topic for identification
                topic = chat.get('topic')
                if topic:
                    collaborator_name = topic
                else:
                    continue
            
            # Skip if it's the current user's own message
            if self.current_user_name and collaborator_name == self.current_user_name:
                # Try to get chat topic or other participant
                if chat_type == 'oneOnOne':
                    # For 1:1, we need to infer the other person from chat topic
                    topic = chat.get('topic')
                    if topic:
                        collaborator_name = topic
                else:
                    continue
            
            # Initialize or update collaborator entry
            if collaborator_name not in collaborators:
                collaborators[collaborator_name] = {
                    "chat_count": 0,
                    "message_count": 0,
                    "last_chat_date": created_str,
                    "days_since_last_chat": 0,
                    "chat_type": chat_type,
                    "recency_score": 0.0,
                    "is_recent": False,
                    "is_frequent": False,
                }
            
            collab = collaborators[collaborator_name]
            collab["chat_count"] += 1
            collab["message_count"] += 1  # Estimate (would need to fetch messages for accuracy)
            
            # Update last chat date if more recent
            if created_dt > self._parse_timestamp(collab["last_chat_date"]):
                collab["last_chat_date"] = created_str
                collab["days_since_last_chat"] = (now - created_dt).days
        
        # Calculate derived metrics
        for name, collab in collaborators.items():
            days_ago = collab["days_since_last_chat"]
            
            # Recency score (similar to temporal multiplier in collaborator_discovery)
            if days_ago <= 7:
                collab["recency_score"] = 2.0
            elif days_ago <= 30:
                collab["recency_score"] = 1.5
            elif days_ago <= 90:
                collab["recency_score"] = 1.2
            else:
                collab["recency_score"] = 0.8
            
            # Flags
            collab["is_recent"] = days_ago <= 30
            collab["is_frequent"] = collab["chat_count"] >= 5
        
        return collaborators
    
    def save_chat_analysis(self, chats: List[Dict], collaborators: Dict[str, Dict], 
                          filename: str = None) -> Path:
        """
        Save chat analysis results to JSON file.
        
        Args:
            chats: Raw chat data
            collaborators: Analyzed collaborator metrics
            filename: Output filename (default: teams_chat_analysis_TIMESTAMP.json)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"teams_chat_analysis_{timestamp}.json"
        
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        filepath = OUT_DIR / filename
        
        output = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "tool": "Scenara 2.0 Teams Chat API",
            "total_chats": len(chats),
            "collaborators_analyzed": len(collaborators),
            "chats": chats,
            "collaborators": collaborators,
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self._safe_print(f"💾 Saved chat analysis to: {filepath}")
        return filepath


def main():
    """Main entry point for standalone execution."""
    import argparse
    import io
    
    # Fix Windows console encoding for emoji/Unicode support
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description="Scenara 2.0 Teams Chat API - Extract and analyze Teams collaboration data"
    )
    parser.add_argument("--top", type=int, default=DEFAULT_TOP,
                       help=f"Page size for chat listing (default: {DEFAULT_TOP})")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX,
                       help=f"Maximum total chats to retrieve (default: {DEFAULT_MAX}, 0=unlimited)")
    parser.add_argument("--days", type=int, default=90,
                       help="Days lookback for collaboration analysis (default: 90)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--output", "-o", help="Output filename (default: auto-generated)")
    
    args = parser.parse_args()
    
    # Initialize API client
    api = TeamsChatAPI(verbose=args.verbose)
    
    print("🚀 Scenara 2.0 Teams Chat API")
    print("=" * 60)
    
    # Acquire token
    try:
        api.acquire_token()
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return 1
    
    # List chats
    print(f"\n📥 Fetching Teams chats...")
    chats = api.list_chats(top=args.top, max_results=args.max)
    
    if not chats:
        print("⚠️ No chats found")
        return 0
    
    print(f"✅ Retrieved {len(chats)} chats")
    
    # Analyze collaborators
    print(f"\n🔍 Analyzing collaboration patterns (last {args.days} days)...")
    collaborators = api.analyze_chat_collaborators(chats, days_lookback=args.days)
    
    print(f"✅ Identified {len(collaborators)} collaborators")
    
    # Display top collaborators
    print("\n📊 Top Chat Collaborators:")
    print("-" * 60)
    
    sorted_collabs = sorted(
        collaborators.items(),
        key=lambda x: (x[1]['recency_score'] * x[1]['chat_count'], x[1]['chat_count']),
        reverse=True
    )
    
    for i, (name, metrics) in enumerate(sorted_collabs[:10], 1):
        age = api.relative_age(metrics['last_chat_date'])
        print(f"{i:2}. {name:30} | Chats: {metrics['chat_count']:3} | "
              f"Last: {age:6} | Recency: {metrics['recency_score']:.1f}x | "
              f"Type: {metrics['chat_type']}")
    
    # Save results
    print(f"\n💾 Saving analysis results...")
    filepath = api.save_chat_analysis(chats, collaborators, filename=args.output)
    print(f"✅ Results saved to: {filepath}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
