#!/usr/bin/env python3
"""
Enhanced Me Notes Viewer with Multi-User Access Controls
Privacy-first architecture for enterprise Me Notes access
"""

import json
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccessLevel(Enum):
    """Access levels for Me Notes"""
    SELF = "SELF"  # User accessing their own notes
    MANAGER = "MANAGER"  # Manager accessing team member's notes (with consent)
    HR_ANALYTICS = "HR_ANALYTICS"  # Anonymized organizational insights
    ADMIN = "ADMIN"  # System administrator access

class ConsentStatus(Enum):
    """Consent status for cross-user access"""
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"

@dataclass
class AccessRequest:
    """Represents an access request for Me Notes"""
    requesting_user: str
    target_user: str
    access_level: AccessLevel
    purpose: str
    consent_status: ConsentStatus
    expiry_date: datetime
    granted_categories: List[str]

class EnhancedMeNotesAPI:
    """Enhanced Me Notes API with privacy controls"""
    
    def __init__(self, requesting_user: str, access_token: str):
        self.requesting_user = requesting_user
        self.access_token = access_token
        self.api_base = "https://graph.microsoft.com/v1.0"
        
    def request_access(self, target_user: str, access_level: AccessLevel, 
                      purpose: str, categories: List[str] = None) -> AccessRequest:
        """Request access to another user's Me Notes"""
        
        if target_user == self.requesting_user:
            # Self-access always granted
            return AccessRequest(
                requesting_user=self.requesting_user,
                target_user=target_user,
                access_level=AccessLevel.SELF,
                purpose="Personal access",
                consent_status=ConsentStatus.GRANTED,
                expiry_date=datetime.now() + timedelta(days=365),
                granted_categories=categories or ["ALL"]
            )
        
        # For other users, check organizational policies and consent
        logger.info(f"🔐 Requesting access to {target_user}'s Me Notes")
        logger.info(f"   👤 Requesting user: {self.requesting_user}")
        logger.info(f"   🎯 Purpose: {purpose}")
        logger.info(f"   📋 Categories: {categories or ['ALL']}")
        
        # In production, this would:
        # 1. Check organizational policies
        # 2. Send consent request to target user
        # 3. Validate business justification
        # 4. Set appropriate expiry dates
        
        # For demo, simulate consent requirement
        return AccessRequest(
            requesting_user=self.requesting_user,
            target_user=target_user,
            access_level=access_level,
            purpose=purpose,
            consent_status=ConsentStatus.PENDING,
            expiry_date=datetime.now() + timedelta(days=30),
            granted_categories=categories or []
        )
    
    def fetch_me_notes_with_access_control(self, target_user: str, 
                                          access_request: AccessRequest) -> List[Dict]:
        """Fetch Me Notes with proper access controls"""
        
        # Validate access request
        if not self._validate_access_request(access_request):
            raise PermissionError("Access denied: Invalid or expired access request")
        
        # Log access attempt
        self._log_access_attempt(target_user, access_request)
        
        # Filter categories based on granted permissions
        if access_request.consent_status != ConsentStatus.GRANTED:
            logger.warning("⚠️ Access not granted - returning empty results")
            return []
        
        # In production, fetch from real API with appropriate filters
        logger.info(f"✅ Access granted - fetching Me Notes for {target_user}")
        
        # Apply category restrictions
        available_categories = access_request.granted_categories
        if "ALL" not in available_categories:
            logger.info(f"🔒 Restricted to categories: {available_categories}")
        
        # Simulate filtered results based on access level
        if access_request.access_level == AccessLevel.HR_ANALYTICS:
            # Return anonymized/aggregated data only
            return self._get_anonymized_insights(target_user)
        else:
            # Return filtered personal insights
            return self._get_filtered_insights(target_user, available_categories)
    
    def _validate_access_request(self, access_request: AccessRequest) -> bool:
        """Validate if access request is valid and not expired"""
        
        # Check if request is still valid
        if access_request.expiry_date < datetime.now():
            logger.error("❌ Access request expired")
            return False
        
        # Check if consent is granted
        if access_request.consent_status != ConsentStatus.GRANTED:
            logger.error(f"❌ Access not granted: {access_request.consent_status}")
            return False
        
        # Check if requesting user matches
        if access_request.requesting_user != self.requesting_user:
            logger.error("❌ Requesting user mismatch")
            return False
        
        return True
    
    def _log_access_attempt(self, target_user: str, access_request: AccessRequest):
        """Log access attempt for audit purposes"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "requesting_user": self.requesting_user,
            "target_user": target_user,
            "access_level": access_request.access_level.value,
            "purpose": access_request.purpose,
            "consent_status": access_request.consent_status.value,
            "categories": access_request.granted_categories,
            "success": access_request.consent_status == ConsentStatus.GRANTED
        }
        
        # In production, send to audit logging system
        logger.info(f"📝 Audit log: {json.dumps(log_entry, indent=2)}")
    
    def _get_anonymized_insights(self, target_user: str) -> List[Dict]:
        """Get anonymized insights for HR analytics"""
        
        # Return aggregated, non-personal insights
        return [
            {
                "category": "EXPERTISE_SUMMARY",
                "insight": "Team member has strong technical background",
                "confidence": 0.8,
                "temporal_pattern": "CONSISTENT"
            },
            {
                "category": "COLLABORATION_PATTERN", 
                "insight": "Active collaborator with cross-functional teams",
                "confidence": 0.9,
                "temporal_pattern": "INCREASING"
            }
        ]
    
    def _get_filtered_insights(self, target_user: str, categories: List[str]) -> List[Dict]:
        """Get filtered personal insights based on granted categories"""
        
        # Return category-filtered personal insights
        # In production, this would filter actual Me Notes data
        
        allowed_insights = []
        
        if "WORK_RELATED" in categories or "ALL" in categories:
            allowed_insights.append({
                "category": "WORK_RELATED",
                "note": "Currently focused on Priority Calendar project",
                "title": "Priority Calendar Project Involvement",
                "confidence": 0.9
            })
        
        if "EXPERTISE" in categories or "ALL" in categories:
            allowed_insights.append({
                "category": "EXPERTISE", 
                "note": "Expert in meeting intelligence and calendar optimization",
                "title": "Calendar Intelligence Expertise",
                "confidence": 0.95
            })
        
        return allowed_insights

class ConsentManager:
    """Manages consent requests for cross-user Me Notes access"""
    
    def __init__(self):
        self.consent_requests = {}
    
    def request_consent(self, requesting_user: str, target_user: str, 
                       purpose: str, categories: List[str]) -> str:
        """Send consent request to target user"""
        
        request_id = f"consent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        consent_request = {
            "request_id": request_id,
            "requesting_user": requesting_user,
            "target_user": target_user,
            "purpose": purpose,
            "requested_categories": categories,
            "status": ConsentStatus.PENDING,
            "created_at": datetime.now(),
            "expiry_at": datetime.now() + timedelta(days=7)  # Consent request expires in 7 days
        }
        
        self.consent_requests[request_id] = consent_request
        
        # In production, this would:
        # 1. Send notification to target user
        # 2. Provide consent interface
        # 3. Handle user response
        
        logger.info(f"📬 Consent request sent to {target_user}")
        logger.info(f"   📝 Request ID: {request_id}")
        logger.info(f"   🎯 Purpose: {purpose}")
        
        return request_id
    
    def grant_consent(self, request_id: str, granted_categories: List[str] = None) -> AccessRequest:
        """Grant consent for access request"""
        
        if request_id not in self.consent_requests:
            raise ValueError("Invalid consent request ID")
        
        consent_req = self.consent_requests[request_id]
        
        # Update consent status
        consent_req["status"] = ConsentStatus.GRANTED
        consent_req["granted_categories"] = granted_categories or consent_req["requested_categories"]
        consent_req["granted_at"] = datetime.now()
        
        # Create access request
        access_request = AccessRequest(
            requesting_user=consent_req["requesting_user"],
            target_user=consent_req["target_user"],
            access_level=AccessLevel.MANAGER,  # Default for cross-user access
            purpose=consent_req["purpose"],
            consent_status=ConsentStatus.GRANTED,
            expiry_date=datetime.now() + timedelta(days=30),  # Access expires in 30 days
            granted_categories=consent_req["granted_categories"]
        )
        
        logger.info(f"✅ Consent granted for request {request_id}")
        return access_request

# Example usage demonstration
def demo_enhanced_access_control():
    """Demonstrate enhanced access control features"""
    
    print("🔐 Enhanced Me Notes Access Control Demo")
    print("=" * 50)
    
    # Initialize components
    api = EnhancedMeNotesAPI("manager@company.com", "demo_token")
    consent_mgr = ConsentManager()
    
    # Scenario 1: Self-access (always allowed)
    print("\n📊 Scenario 1: Self-access")
    self_access = api.request_access(
        target_user="manager@company.com",
        access_level=AccessLevel.SELF,
        purpose="Personal productivity insights"
    )
    print(f"✅ Self-access: {self_access.consent_status}")
    
    # Scenario 2: Cross-user access (requires consent)
    print("\n📊 Scenario 2: Manager requesting team member access")
    team_access = api.request_access(
        target_user="team.member@company.com",
        access_level=AccessLevel.MANAGER, 
        purpose="Project assignment optimization",
        categories=["WORK_RELATED", "EXPERTISE"]
    )
    print(f"⏳ Initial status: {team_access.consent_status}")
    
    # Simulate consent process
    print("\n📬 Sending consent request...")
    request_id = consent_mgr.request_consent(
        requesting_user="manager@company.com",
        target_user="team.member@company.com",
        purpose="Project assignment optimization", 
        categories=["WORK_RELATED", "EXPERTISE"]
    )
    
    # Simulate consent being granted
    print("\n✅ Simulating consent granted...")
    granted_access = consent_mgr.grant_consent(
        request_id=request_id,
        granted_categories=["WORK_RELATED"]  # User grants partial access
    )
    
    # Try to access with granted consent
    print("\n📊 Attempting to fetch notes with granted access...")
    try:
        notes = api.fetch_me_notes_with_access_control(
            target_user="team.member@company.com",
            access_request=granted_access
        )
        print(f"✅ Retrieved {len(notes)} filtered insights")
        for note in notes:
            print(f"   📝 {note['category']}: {note['title']}")
    except PermissionError as e:
        print(f"❌ Access denied: {e}")
    
    print("\n🎯 Demo completed - Privacy controls working correctly!")

if __name__ == "__main__":
    demo_enhanced_access_control()