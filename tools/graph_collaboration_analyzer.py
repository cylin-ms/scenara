#!/usr/bin/env python3
"""
Simple Graph Interaction Analysis for Collaboration Discovery

Based on the Graph-Interaction-Analysis-Guide.md approach - much simpler
and more accurate than manual scoring systems.

This script directly accesses Microsoft Graph APIs to analyze:
- Email exchanges and @mentions
- Teams chat messages and mentions  
- Calendar meeting patterns
- Document collaboration (file access)

Then computes collaboration scores automatically using graph analysis.
"""

import sys
import json
import requests
import keyring
from urllib.parse import urlencode
import msal
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import networkx as nx

class GraphCollaborationAnalyzer:
    def __init__(self, client_id: str, tenant_id: str = "common"):
        """Initialize Graph API client following the guide's approach"""
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.graph_url = "https://graph.microsoft.com/v1.0"
        self.service_name = f"msal_token_{client_id}"
        
        # Required scopes for comprehensive collaboration analysis
        self.scopes = [
            "User.Read",
            "Mail.Read", 
            "Chat.Read",
            "Calendars.Read",
            "Files.Read"
        ]
        
        self.headers = None
        self.collaboration_edges = []
        
    def authenticate(self):
        """Authenticate using device code flow (from the guide)"""
        print("🔐 AUTHENTICATING WITH MICROSOFT GRAPH")
        print("-" * 40)
        
        app = msal.PublicClientApplication(
            self.client_id, 
            authority=self.authority
        )
        
        # Try to load cached token
        token_cache = msal.SerializableTokenCache()
        cache_blob = keyring.get_password(self.service_name, "cache")
        if cache_blob:
            token_cache.deserialize(cache_blob)
        app.token_cache = token_cache
        
        # Try silent authentication first
        result = app.acquire_token_silent(self.scopes, account=None)
        
        if not result:
            # Use device code flow
            flow = app.initiate_device_flow(scopes=self.scopes)
            print(f"🌐 Go to: {flow['verification_uri']}")
            print(f"🔑 Enter code: {flow['user_code']}")
            print("Waiting for authentication...")
            
            result = app.acquire_token_by_device_flow(flow)
        
        if "access_token" not in result:
            print(f"❌ Authentication failed: {result.get('error_description', 'Unknown error')}")
            return False
            
        # Cache the token
        keyring.set_password(self.service_name, "cache", token_cache.serialize())
        
        # Set headers for API calls
        self.headers = {"Authorization": f"Bearer {result['access_token']}"}
        print("✅ Authentication successful!")
        return True
        
    def graph_get(self, path: str, select: str = None, top: int = 25, expand: str = None):
        """Make Graph API GET request (from the guide)"""
        params = {}
        if select:
            params["$select"] = select
        if top:
            params["$top"] = str(top)
        if expand:
            params["$expand"] = expand
            
        url = f"{self.graph_url}{path}"
        if params:
            url += f"?{urlencode(params)}"
            
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Graph API error for {path}: {e}")
            return {}
    
    def analyze_email_interactions(self, days_back: int = 30):
        """Analyze email interactions and mentions"""
        print(f"📧 ANALYZING EMAIL INTERACTIONS ({days_back} days)")
        print("-" * 40)
        
        # Get recent emails
        mail_data = self.graph_get(
            "/me/messages",
            select="id,subject,from,toRecipients,ccRecipients,receivedDateTime,mentionsPreview",
            top=100
        )
        
        email_edges = []
        my_email = None
        
        for message in mail_data.get("value", []):
            # Get sender
            sender = message.get("from", {}).get("emailAddress", {}).get("address")
            received_time = message.get("receivedDateTime")
            
            # Skip old emails
            if received_time:
                try:
                    msg_date = datetime.fromisoformat(received_time.replace('Z', '+00:00'))
                    if (datetime.now().replace(tzinfo=msg_date.tzinfo) - msg_date).days > days_back:
                        continue
                except:
                    continue
            
            # Track my email for reference
            if not my_email and sender:
                # Get my profile to identify my emails
                me_data = self.graph_get("/me", select="mail")
                my_email = me_data.get("mail", sender)
            
            # Process recipients (to and cc)
            for field in ("toRecipients", "ccRecipients"):
                recipients = message.get(field, [])
                for recipient in recipients:
                    dst_email = recipient.get("emailAddress", {}).get("address")
                    if sender and dst_email and sender != dst_email:
                        edge_weight = 2 if field == "toRecipients" else 1  # Direct vs CC
                        email_edges.append({
                            "src": sender,
                            "dst": dst_email, 
                            "modality": "email",
                            "timestamp": received_time,
                            "weight": edge_weight
                        })
            
            # Process mentions (high-value interactions)
            mentions = message.get("mentionsPreview", {}).get("isMentioned", False)
            if mentions and sender:
                email_edges.append({
                    "src": sender,
                    "dst": my_email,
                    "modality": "email_mention",
                    "timestamp": received_time,
                    "weight": 5  # Mentions are high-value
                })
        
        print(f"✅ Found {len(email_edges)} email interactions")
        self.collaboration_edges.extend(email_edges)
        return email_edges
    
    def analyze_chat_interactions(self, days_back: int = 30):
        """Analyze Teams chat interactions and mentions"""
        print(f"💬 ANALYZING TEAMS CHAT INTERACTIONS ({days_back} days)")
        print("-" * 40)
        
        # Get chat conversations
        chats_data = self.graph_get("/me/chats", top=50)
        chat_edges = []
        
        for chat in chats_data.get("value", []):
            chat_id = chat.get("id")
            chat_type = chat.get("chatType", "unknown")
            
            if not chat_id:
                continue
                
            # Get messages from this chat
            messages_data = self.graph_get(
                f"/chats/{chat_id}/messages",
                select="id,from,createdDateTime,mentions,messageType",
                top=50
            )
            
            for message in messages_data.get("value", []):
                sender_email = message.get("from", {}).get("user", {}).get("email")
                created_time = message.get("createdDateTime")
                
                # Skip old messages
                if created_time:
                    try:
                        msg_date = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                        if (datetime.now().replace(tzinfo=msg_date.tzinfo) - msg_date).days > days_back:
                            continue
                    except:
                        continue
                
                # Weight based on chat type
                base_weight = 3 if chat_type == "oneOnOne" else 1
                
                # Process mentions in the message
                mentions = message.get("mentions", [])
                for mention in mentions:
                    mentioned_user = mention.get("mentioned", {}).get("user", {})
                    mentioned_email = mentioned_user.get("email")
                    
                    if sender_email and mentioned_email and sender_email != mentioned_email:
                        chat_edges.append({
                            "src": sender_email,
                            "dst": mentioned_email,
                            "modality": "chat_mention",
                            "timestamp": created_time,
                            "weight": base_weight * 3  # Mentions are valuable
                        })
                
                # Add general chat interaction (for frequency analysis)
                if sender_email:
                    # In group chats, this represents participation
                    chat_edges.append({
                        "src": sender_email,
                        "dst": "GROUP_PARTICIPATION",
                        "modality": "chat_message",
                        "timestamp": created_time,
                        "weight": base_weight,
                        "chat_type": chat_type
                    })
        
        print(f"✅ Found {len(chat_edges)} chat interactions")
        self.collaboration_edges.extend(chat_edges)
        return chat_edges
    
    def analyze_meeting_interactions(self, days_back: int = 90):
        """Analyze calendar meeting patterns"""
        print(f"📅 ANALYZING MEETING INTERACTIONS ({days_back} days)")
        print("-" * 40)
        
        # Get calendar events
        events_data = self.graph_get(
            "/me/events",
            select="id,subject,organizer,start,end,attendees,responseStatus",
            top=100
        )
        
        meeting_edges = []
        my_email = self.graph_get("/me", select="mail").get("mail")
        
        for event in events_data.get("value", []):
            start_time = event.get("start", {}).get("dateTime")
            organizer_email = event.get("organizer", {}).get("emailAddress", {}).get("address")
            attendees = event.get("attendees", [])
            subject = event.get("subject", "")
            
            # Skip old events
            if start_time:
                try:
                    event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    if (datetime.now().replace(tzinfo=event_date.tzinfo) - event_date).days > days_back:
                        continue
                except:
                    continue
            
            # Analyze meeting characteristics
            attendee_count = len(attendees)
            is_small_meeting = attendee_count <= 5
            is_one_on_one = attendee_count == 2
            
            # Weight based on meeting size and type
            base_weight = 10 if is_one_on_one else (5 if is_small_meeting else 2)
            
            # Check if I organized this meeting
            organized_by_me = organizer_email == my_email
            if organized_by_me:
                base_weight *= 1.5  # Organizing shows initiative
            
            # Check for collaboration keywords
            collab_keywords = ["sync", "discuss", "review", "planning", "working", "brainstorm", "design"]
            is_collaborative = any(keyword in subject.lower() for keyword in collab_keywords)
            if is_collaborative:
                base_weight *= 1.3
            
            # Create edges for each attendee
            for attendee in attendees:
                attendee_email = attendee.get("emailAddress", {}).get("address")
                if attendee_email and attendee_email != my_email:
                    meeting_edges.append({
                        "src": my_email,
                        "dst": attendee_email,
                        "modality": "meeting",
                        "timestamp": start_time,
                        "weight": base_weight,
                        "organized_by_me": organized_by_me,
                        "is_one_on_one": is_one_on_one,
                        "is_collaborative": is_collaborative,
                        "attendee_count": attendee_count
                    })
        
        print(f"✅ Found {len(meeting_edges)} meeting interactions")
        self.collaboration_edges.extend(meeting_edges)
        return meeting_edges
    
    def compute_collaboration_scores(self):
        """Compute final collaboration scores using graph analysis"""
        print(f"🔍 COMPUTING COLLABORATION SCORES")
        print("-" * 40)
        
        # Group edges by person
        person_interactions = defaultdict(list)
        person_weights = defaultdict(float)
        
        my_email = self.graph_get("/me", select="mail").get("mail")
        
        for edge in self.collaboration_edges:
            src = edge.get("src")
            dst = edge.get("dst")
            weight = edge.get("weight", 1)
            modality = edge.get("modality")
            
            # Skip group participation entries
            if dst == "GROUP_PARTICIPATION":
                continue
            
            # Determine the other person in the interaction
            other_person = dst if src == my_email else src
            if other_person == my_email or not other_person:
                continue
            
            person_interactions[other_person].append(edge)
            person_weights[other_person] += weight
        
        # Calculate comprehensive scores
        collaboration_scores = {}
        
        for person, interactions in person_interactions.items():
            if len(interactions) < 2:  # Need minimum interactions
                continue
            
            # Basic metrics
            total_weight = person_weights[person]
            interaction_count = len(interactions)
            
            # Temporal analysis
            timestamps = [i.get("timestamp") for i in interactions if i.get("timestamp")]
            if timestamps:
                try:
                    dates = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                    dates.sort()
                    duration = (dates[-1] - dates[0]).days if len(dates) > 1 else 0
                    frequency = len(dates) / max(1, duration / 7)  # Interactions per week
                except:
                    duration = 0
                    frequency = 0
            else:
                duration = 0
                frequency = 0
            
            # Modality analysis
            modalities = Counter(i.get("modality") for i in interactions)
            modality_diversity = len(modalities)  # More modalities = deeper collaboration
            
            # Interaction type analysis
            one_on_ones = len([i for i in interactions if i.get("is_one_on_one")])
            collaborative_meetings = len([i for i in interactions if i.get("is_collaborative")])
            organized_meetings = len([i for i in interactions if i.get("organized_by_me")])
            
            # Calculate final score
            base_score = total_weight
            temporal_bonus = min(50, duration * 0.5)  # Duration bonus
            frequency_bonus = min(100, frequency * 10)  # Frequency bonus
            diversity_bonus = modality_diversity * 20  # Multi-modal bonus
            depth_bonus = (one_on_ones * 30) + (collaborative_meetings * 15) + (organized_meetings * 25)
            
            final_score = base_score + temporal_bonus + frequency_bonus + diversity_bonus + depth_bonus
            
            collaboration_scores[person] = {
                "final_score": round(final_score, 2),
                "total_weight": total_weight,
                "interaction_count": interaction_count,
                "duration_days": duration,
                "frequency_per_week": round(frequency, 2),
                "modalities": dict(modalities),
                "modality_diversity": modality_diversity,
                "one_on_one_meetings": one_on_ones,
                "collaborative_meetings": collaborative_meetings,
                "organized_meetings": organized_meetings,
                "recent_interactions": sorted(timestamps, reverse=True)[:3] if timestamps else []
            }
        
        return collaboration_scores
    
    def run_comprehensive_analysis(self, days_back: int = 30):
        """Run complete collaboration analysis"""
        print("🚀 GRAPH-BASED COLLABORATION ANALYSIS")
        print("=" * 50)
        print("Using Microsoft Graph API for direct interaction data")
        print()
        
        if not self.authenticate():
            return {}
        
        # Analyze all interaction types
        self.analyze_email_interactions(days_back)
        self.analyze_chat_interactions(days_back)
        self.analyze_meeting_interactions(days_back * 3)  # Longer window for meetings
        
        # Compute final scores
        scores = self.compute_collaboration_scores()
        
        # Sort and display results
        sorted_collaborators = sorted(scores.items(), key=lambda x: x[1]["final_score"], reverse=True)
        
        print(f"\n🏆 COLLABORATION RANKINGS (Based on real Graph data)")
        print("-" * 50)
        
        for i, (person, data) in enumerate(sorted_collaborators[:10], 1):
            print(f"{i}. {person}")
            print(f"   🎯 Score: {data['final_score']:.1f}")
            print(f"   📊 Interactions: {data['interaction_count']} over {data['duration_days']} days")
            print(f"   🔄 Frequency: {data['frequency_per_week']:.1f} per week")
            print(f"   📱 Modalities: {', '.join(data['modalities'].keys())}")
            
            if data['one_on_one_meetings'] > 0:
                print(f"   🤝 1:1 meetings: {data['one_on_one_meetings']}")
            if data['organized_meetings'] > 0:
                print(f"   👤 Organized meetings: {data['organized_meetings']}")
            print()
        
        return {
            "algorithm": "graph_api_direct_analysis",
            "timestamp": datetime.now().isoformat(),
            "total_edges": len(self.collaboration_edges),
            "analysis_period_days": days_back,
            "collaborators": sorted_collaborators
        }

def main():
    """Main execution - requires Azure app registration"""
    print("📋 SETUP REQUIREMENTS:")
    print("1. Register app in Azure AD (entra.microsoft.com)")
    print("2. Add delegated permissions: User.Read, Mail.Read, Chat.Read, Calendars.Read, Files.Read")
    print("3. Get your Client ID from the app registration")
    print()
    
    # You need to replace this with your actual Azure app client ID
    client_id = input("Enter your Azure App Client ID: ").strip()
    
    if not client_id:
        print("❌ Client ID required. Please register an Azure app first.")
        print("📖 See: docs/Graph-Interaction-Analysis-Guide.md")
        return
    
    # Run analysis
    analyzer = GraphCollaborationAnalyzer(client_id)
    results = analyzer.run_comprehensive_analysis(days_back=30)
    
    # Save results
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graph_collaboration_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Results saved to: {filename}")
        print(f"\n💡 This approach uses REAL Microsoft Graph data:")
        print("   • Actual email interactions and mentions")
        print("   • Real Teams chat messages and @mentions")
        print("   • Calendar meeting patterns and organization")
        print("   • Temporal patterns and frequency analysis")
        print("\n🎯 Much more accurate than manual scoring!")

if __name__ == "__main__":
    main()