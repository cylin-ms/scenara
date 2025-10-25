#!/usr/bin/env python3
"""
Enhanced Me Notes Generation Using SilverFlow Patterns
Leverages advanced Microsoft Graph and Loki API techniques from the SilverFlow project
"""

import json
import os
import sys
import base64
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from uuid import uuid4

import msal
import requests

# Microsoft Graph Configuration (from SilverFlow patterns)
DEFAULT_TENANT_ID = os.getenv("GRAPH_TENANT_ID", "72f988bf-86f1-41af-91ab-2d7cd011db47")
DEFAULT_CLIENT_ID = os.getenv("GRAPH_CLIENT_ID", "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11")
GRAPH_SCOPES = ["https://graph.microsoft.com/.default", "User.Read", "openid", "profile", "offline_access"]

# Loki Configuration (for organizational data)
LOKI_CLIENT_ID = os.getenv("LOKI_CLIENT_ID", "d3590ed6-52b3-4102-aeff-aad2292ab01c")
LOKI_RESOURCE = os.getenv("LOKI_RESOURCE", "https://loki.delve.office.com/")
LOKI_SCOPES = [f"{LOKI_RESOURCE}/.default"]

def _login_hint() -> Optional[str]:
    """Generate login hint from current user environment (SilverFlow pattern)"""
    user = os.getenv("USERNAME") or os.getenv("USER")
    return f"{user}@microsoft.com" if user else None

def acquire_token_interactive(tenant_id: str, client_id: str, scopes: List[str], login_hint: Optional[str] = None) -> Dict[str, Any]:
    """
    Acquire access token using MSAL with Windows broker support (SilverFlow pattern)
    """
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    
    # Try with broker first (Windows)
    try:
        app = msal.PublicClientApplication(
            client_id,
            authority=authority,
            enable_broker_on_windows=True,
        )
        broker_enabled = True
        print("🔐 Windows broker authentication enabled")
    except Exception:
        app = msal.PublicClientApplication(
            client_id,
            authority=authority,
            enable_broker_on_windows=False,
        )
        broker_enabled = False
        print("🔐 Windows broker not available, using standard auth")
    
    # Check for cached accounts
    account = None
    try:
        if login_hint:
            accounts = app.get_accounts(username=login_hint)
            if accounts:
                account = accounts[0]
                print(f"📋 Found cached account for {login_hint}")
        if not account:
            accounts = app.get_accounts()
            if accounts:
                account = accounts[0]
                print("📋 Found cached account")
    except Exception:
        account = None
    
    # Try silent token acquisition first
    if account:
        silent_result = app.acquire_token_silent(scopes, account=account)
        if silent_result and "access_token" in silent_result:
            print("✅ Token acquired silently from cache")
            return silent_result
    
    # Interactive authentication
    print("🔄 Starting interactive authentication...")
    kwargs = {"scopes": scopes}
    if login_hint:
        kwargs["login_hint"] = login_hint
    if broker_enabled:
        kwargs["parent_window_handle"] = msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE
    
    result = app.acquire_token_interactive(**kwargs)
    if "access_token" not in result:
        error_desc = result.get("error_description", "Unknown error")
        raise RuntimeError(f"Authentication failed: {error_desc}")
    
    print("✅ Interactive authentication successful")
    return result

def _decode_jwt_payload(token: str) -> Dict[str, Any]:
    """Decode JWT payload without signature validation (SilverFlow pattern)"""
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return {}
        payload = parts[1]
        # Add padding if needed
        padding = "=" * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload + padding)
        return json.loads(decoded.decode("utf-8"))
    except Exception:
        return {}

def extract_claim(token: str, claim: str) -> Optional[str]:
    """Extract specific claim from access token (SilverFlow pattern)"""
    payload = _decode_jwt_payload(token)
    return payload.get(claim)

def fetch_enhanced_graph_profile(token: str) -> Dict[str, Any]:
    """
    Fetch comprehensive user profile using Microsoft Graph beta API
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "Scenara-MeNotes/1.0"
    }
    
    # Use beta API for richer data (like our previous success)
    url = "https://graph.microsoft.com/beta/me"
    
    print("📡 Fetching enhanced profile from Graph beta API...")
    response = requests.get(url, headers=headers, timeout=60)
    
    if response.status_code >= 400:
        print(f"❌ Graph API error: {response.status_code} {response.reason}")
        return {}
    
    profile_data = response.json()
    print(f"✅ Enhanced profile data retrieved ({len(profile_data)} fields)")
    return profile_data

def fetch_loki_persona_card(token: str, aad_object_id: str) -> Dict[str, Any]:
    """
    Fetch persona card from Loki API for organizational context (SilverFlow pattern)
    """
    base_url = "https://df.loki.delve.office.com/api/v3/personacards"
    correlation_id = str(uuid4())
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Scenara-MeNotes/1.0",
        "X-ClientType": "OneOutlook",
        "X-ClientFeature": "LivePersonaCard",
        "X-ClientScenario": "CardTemplate",
        "X-CorrelationId": correlation_id,
    }
    
    params = {
        "viewType": "Card",
        "personaType": "User",
        "aadObjectId": aad_object_id,
        "ConvertGetPost": "true",
    }
    
    payload = {
        "viewType": "Card",
        "personaType": "User",
        "aadObjectId": aad_object_id,
    }
    
    print("📡 Fetching Loki persona card...")
    try:
        response = requests.post(base_url, params=params, headers=headers, json=payload, timeout=60)
        
        if response.status_code >= 400:
            print(f"⚠️  Loki API error: {response.status_code} {response.reason}")
            return {}
        
        loki_data = response.json()
        print(f"✅ Loki persona card retrieved")
        return loki_data
    except Exception as e:
        print(f"⚠️  Loki API request failed: {e}")
        return {}

def fetch_graph_people_connections(token: str) -> List[Dict[str, Any]]:
    """
    Fetch people connections from Graph API for relationship context
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    url = "https://graph.microsoft.com/v1.0/me/people?$top=50"
    
    print("📡 Fetching people connections...")
    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code >= 400:
            print(f"⚠️  People API error: {response.status_code}")
            return []
        
        data = response.json()
        people = data.get("value", [])
        print(f"✅ Retrieved {len(people)} people connections")
        return people
    except Exception as e:
        print(f"⚠️  People API request failed: {e}")
        return []

def generate_comprehensive_me_notes(graph_profile: Dict[str, Any], loki_data: Dict[str, Any], people_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate comprehensive Me Notes using all available data sources
    """
    me_notes = []
    
    # Enhanced Professional Identity (from Graph beta API)
    if graph_profile.get("displayName") and graph_profile.get("jobTitle"):
        professional_note = {
            "note": f"I am {graph_profile['displayName']}, working as {graph_profile['jobTitle']} at {graph_profile.get('companyName', 'my organization')}",
            "category": "professional_identity",
            "title": "Current Professional Role",
            "temporal_durability": "stable",
            "data_source": "microsoft_graph_beta",
            "confidence": 0.95
        }
        me_notes.append(professional_note)
    
    # Organizational Context Enhancement
    if graph_profile.get("department"):
        dept_note = {
            "note": f"I work in the {graph_profile['department']} department with employee ID {graph_profile.get('employeeId', 'N/A')}",
            "category": "professional_context",
            "title": "Organizational Position",
            "temporal_durability": "stable",
            "data_source": "microsoft_graph_beta",
            "confidence": 0.9
        }
        me_notes.append(dept_note)
    
    # Enhanced Location Information
    location_parts = []
    if graph_profile.get("city"):
        location_parts.append(graph_profile["city"])
    if graph_profile.get("officeLocation"):
        location_parts.append(f"office {graph_profile['officeLocation']}")
    
    # Add detailed address from extensions
    building_name = graph_profile.get("extension_18e31482d3fb4a8ea958aa96b662f508_BuildingName")
    address_line1 = graph_profile.get("extension_18e31482d3fb4a8ea958aa96b662f508_AddressLine1")
    if building_name and address_line1:
        location_parts.append(f"at {building_name}, {address_line1}")
    
    if location_parts:
        location_note = {
            "note": f"I am based in {', '.join(location_parts)}",
            "category": "location_preferences",
            "title": "Primary Work Location",
            "temporal_durability": "stable",
            "data_source": "microsoft_graph_beta",
            "confidence": 0.9
        }
        me_notes.append(location_note)
    
    # Communication Preferences (enhanced with multiple channels)
    contact_methods = []
    if graph_profile.get("mail"):
        contact_methods.append(f"email at {graph_profile['mail']}")
    if graph_profile.get("businessPhones"):
        for phone in graph_profile["businessPhones"]:
            contact_methods.append(f"phone at {phone}")
    if graph_profile.get("imAddresses"):
        for im in graph_profile["imAddresses"]:
            contact_methods.append(f"IM at {im}")
    
    if contact_methods:
        contact_note = {
            "note": f"I can be reached via {', '.join(contact_methods)}",
            "category": "communication_style",
            "title": "Preferred Contact Methods",
            "temporal_durability": "stable",
            "data_source": "microsoft_graph_beta",
            "confidence": 0.95
        }
        me_notes.append(contact_note)
    
    # Technology Platform Usage (from assigned plans)
    if "assignedPlans" in graph_profile:
        enabled_services = set()
        for plan in graph_profile["assignedPlans"]:
            if plan.get("capabilityStatus") == "Enabled":
                service = plan.get("service", "")
                if service:
                    enabled_services.add(service)
        
        # Categorize services
        collaboration_services = {"TeamspaceAPI", "MicrosoftCommunicationsOnline", "SharePoint", "exchange"}
        productivity_services = {"MicrosoftOffice", "PowerAppsService", "ProcessSimple", "OfficeForms"}
        
        collab_tools = enabled_services.intersection(collaboration_services)
        if collab_tools:
            tech_note = {
                "note": f"I actively use Microsoft collaboration platforms including {', '.join(sorted(collab_tools))}",
                "category": "technology_preferences",
                "title": "Collaboration Platform Usage",
                "temporal_durability": "stable",
                "data_source": "microsoft_graph_beta",
                "confidence": 0.85
            }
            me_notes.append(tech_note)
    
    # Organizational Relationships (from Graph extensions)
    manager_name = graph_profile.get("extension_18e31482d3fb4a8ea958aa96b662f508_ReportsToFullName")
    if manager_name:
        relationship_note = {
            "note": f"I report to {manager_name} in the organizational hierarchy",
            "category": "professional_context",
            "title": "Direct Reporting Relationship",
            "temporal_durability": "stable",
            "data_source": "microsoft_graph_beta",
            "confidence": 0.9
        }
        me_notes.append(relationship_note)
    
    # Loki-based Organizational Insights
    if loki_data and "Card" in loki_data:
        card_data = loki_data["Card"]
        if "headerInfo" in card_data and "attributedUserHeaderInfo" in card_data["headerInfo"]:
            header_info = card_data["headerInfo"]["attributedUserHeaderInfo"]
            
            # Additional job context from Loki
            if "title" in header_info and "value" in header_info["title"]:
                loki_title = header_info["title"]["value"]
                if loki_title and loki_title != graph_profile.get("jobTitle"):
                    loki_note = {
                        "note": f"My role is also described as {loki_title} in organizational systems",
                        "category": "professional_identity",
                        "title": "Extended Role Description",
                        "temporal_durability": "stable",
                        "data_source": "loki_persona_card",
                        "confidence": 0.8
                    }
                    me_notes.append(loki_note)
    
    # People Connections Analysis
    if people_data:
        frequent_contacts = [p for p in people_data if p.get("scoredEmailAddresses")][:10]
        if frequent_contacts:
            contact_note = {
                "note": f"I frequently collaborate with {len(frequent_contacts)} key contacts across the organization",
                "category": "professional_context",
                "title": "Key Professional Relationships",
                "temporal_durability": "dynamic",
                "data_source": "microsoft_graph_people",
                "confidence": 0.7
            }
            me_notes.append(contact_note)
    
    # Security and Compliance Context
    device_count = len(graph_profile.get("deviceKeys", []))
    if device_count > 0:
        security_note = {
            "note": f"I use {device_count} registered devices with secure authentication for enterprise access",
            "category": "security_preferences",
            "title": "Multi-Device Security Setup",
            "temporal_durability": "dynamic",
            "data_source": "microsoft_graph_beta",
            "confidence": 0.8
        }
        me_notes.append(security_note)
    
    return me_notes

def main():
    parser = argparse.ArgumentParser(description="Enhanced Me Notes generation using SilverFlow patterns")
    parser.add_argument("--tenant-id", default=DEFAULT_TENANT_ID, help="Azure AD tenant ID")
    parser.add_argument("--graph-client-id", default=DEFAULT_CLIENT_ID, help="Graph API client ID")
    parser.add_argument("--loki-client-id", default=LOKI_CLIENT_ID, help="Loki API client ID")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--include-loki", action="store_true", help="Include Loki organizational data")
    args = parser.parse_args()
    
    print("🚀 Enhanced Me Notes Generation with SilverFlow Patterns")
    print("=" * 60)
    
    # Step 1: Acquire Graph API token
    print("\n1️⃣ Microsoft Graph Authentication")
    login_hint = _login_hint()
    graph_token_result = acquire_token_interactive(
        args.tenant_id, 
        args.graph_client_id, 
        GRAPH_SCOPES, 
        login_hint
    )
    graph_token = graph_token_result["access_token"]
    
    # Extract user identity
    aad_object_id = extract_claim(graph_token, "oid")
    user_name = extract_claim(graph_token, "name") or extract_claim(graph_token, "preferred_username")
    print(f"👤 Authenticated as: {user_name}")
    print(f"🆔 AAD Object ID: {aad_object_id}")
    
    # Step 2: Fetch enhanced Graph profile
    print("\n2️⃣ Enhanced Microsoft Graph Data Collection")
    graph_profile = fetch_enhanced_graph_profile(graph_token)
    
    # Step 3: Fetch people connections
    people_data = fetch_graph_people_connections(graph_token)
    
    # Step 4: Optional Loki data
    loki_data = {}
    if args.include_loki and aad_object_id:
        print("\n3️⃣ Loki Organizational Data Collection")
        try:
            loki_token_result = acquire_token_interactive(
                args.tenant_id,
                args.loki_client_id,
                LOKI_SCOPES,
                login_hint
            )
            loki_token = loki_token_result["access_token"]
            loki_data = fetch_loki_persona_card(loki_token, aad_object_id)
        except Exception as e:
            print(f"⚠️  Loki data collection failed: {e}")
    
    # Step 5: Generate comprehensive Me Notes
    print("\n4️⃣ Me Notes Generation")
    me_notes = generate_comprehensive_me_notes(graph_profile, loki_data, people_data)
    
    # Step 6: Create final output
    output_data = {
        "user_id": graph_profile.get("userPrincipalName", "unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generation_method": "enhanced_silverflow_patterns",
        "data_sources": {
            "microsoft_graph_beta": bool(graph_profile),
            "loki_persona_card": bool(loki_data),
            "microsoft_graph_people": bool(people_data),
        },
        "me_notes": me_notes,
        "summary": {
            "total_notes": len(me_notes),
            "categories": list(set(note["category"] for note in me_notes)),
            "data_richness": "comprehensive" if len(me_notes) > 8 else "basic",
            "confidence_scores": [note.get("confidence", 0.5) for note in me_notes]
        },
        "raw_data": {
            "graph_profile_fields": len(graph_profile),
            "loki_data_available": bool(loki_data),
            "people_connections": len(people_data)
        }
    }
    
    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output or f"enhanced_me_notes_silverflow_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Enhanced Me Notes Generated Successfully!")
    print(f"📄 Output file: {output_file}")
    print(f"📊 Generated {len(me_notes)} insights across {len(output_data['summary']['categories'])} categories")
    print(f"🎯 Average confidence: {sum(output_data['summary']['confidence_scores'])/len(output_data['summary']['confidence_scores']):.2f}")
    
    # Display sample insights
    print(f"\n🔍 Sample Generated Insights:")
    for i, note in enumerate(me_notes[:5], 1):
        confidence = note.get("confidence", 0.5)
        print(f"{i}. [{note['category']}] {note['title']} (confidence: {confidence:.2f})")
        print(f"   → {note['note'][:100]}{'...' if len(note['note']) > 100 else ''}")
        print(f"   📡 Source: {note.get('data_source', 'unknown')}")
    
    if len(me_notes) > 5:
        print(f"   ... and {len(me_notes) - 5} more insights")
    
    print(f"\n🎉 Enhanced Me Notes integration ready for Scenara!")

if __name__ == "__main__":
    main()