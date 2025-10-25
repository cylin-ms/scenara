#!/usr/bin/env python3
"""
GPT-4.1 Meeting Classifier using SilverFlow LLMAPI
Enterprise meeting classification using Microsoft's GPT-4.1 via SilverFlow

Model: dev-gpt-41-shortco-2025-04-14
Endpoint: https://fe-26.qas.bing.net/chat/completions
Authentication: MSAL (Azure AD)
"""

import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import msal
import requests

# Configuration matching SilverFlow patterns
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
DEFAULT_APP_ID = "942b706f-826e-426b-98f7-59e1e376b37c"
DEFAULT_SCOPES = ["https://substrate.office.com/llmapi/LLMAPI.dev"]
DEFAULT_ENDPOINT = "https://fe-26.qas.bing.net/chat/completions"
DEFAULT_MODEL = "dev-gpt-41-shortco-2025-04-14"


@dataclass
class ClassificationResult:
    """Result of meeting classification"""
    success: bool
    specific_type: str
    primary_category: str
    confidence: float
    reasoning: str
    error: Optional[str] = None
    response_content: Optional[str] = None


class GPT41MeetingClassifier:
    """
    Enterprise Meeting Classifier using Microsoft's GPT-4.1 via SilverFlow.
    
    Features:
    - Uses dev-gpt-41-shortco-2025-04-14 model
    - MSAL authentication with Azure AD
    - Enterprise Meeting Taxonomy with 31+ meeting types
    - Rate limiting and retry logic for robustness
    - Fallback to keyword-based classification
    - Structured JSON output with confidence scores
    """
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        endpoint: str = DEFAULT_ENDPOINT,
        app_id: str = DEFAULT_APP_ID,
        scopes: Optional[List[str]] = None,
        access_token: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        rate_limit_delay: float = 2.0,  # Increased from 0.5s to 2.0s to avoid throttling
    ):
        """
        Initialize GPT-4.1 classifier.
        
        Args:
            model: GPT-4.1 model name
            endpoint: SilverFlow LLMAPI endpoint
            app_id: Azure AD application ID
            scopes: OAuth2 scopes for authentication
            access_token: Pre-acquired access token (optional)
            max_retries: Maximum number of retry attempts
            retry_delay: Base delay between retries (seconds)
            rate_limit_delay: Minimum delay between requests (seconds)
        """
        self.model = model
        self.endpoint = endpoint
        self.app_id = app_id
        self.scopes = scopes or DEFAULT_SCOPES
        self.access_token = access_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        
        # MSAL configuration (matches GPT-5 pattern)
        self.msal_app = None  # Initialized on-demand
        self._cached_token = None
        
        # Enterprise Meeting Taxonomy - 5 categories, 31+ types
        self.enterprise_taxonomy = {
            "Strategic Planning & Decision": [
                "Strategic Planning Session",
                "Decision-Making Meeting",
                "Problem-Solving Meeting",
                "Brainstorming Session",
                "Workshop/Design Session",
                "Budget Planning Meeting",
                "Project Planning Meeting",
                "Risk Assessment Meeting"
            ],
            "Internal Recurring (Cadence)": [
                "Team Status Update/Standup",
                "Progress Review Meeting",
                "One-on-One Meeting",
                "Team Retrospective",
                "Governance/Leadership Meeting",
                "Performance Review",
                "Weekly/Monthly Check-in"
            ],
            "External & Client-Facing": [
                "Sales & Client Meeting",
                "Vendor/Supplier Meeting",
                "Partnership Meeting",
                "Interview Meeting",
                "Client Training/Onboarding",
                "Customer Discovery Call",
                "Contract Negotiation"
            ],
            "Informational & Broadcast": [
                "All-Hands/Town Hall",
                "Informational Briefing",
                "Training Session",
                "Webinar/Presentation",
                "Knowledge Sharing Session",
                "Product Demo",
                "Announcement Meeting"
            ],
            "Team-Building & Culture": [
                "Team-Building Activity",
                "Recognition/Celebration Event",
                "Social/Networking Event",
                "Community Meeting",
                "Offsite/Retreat",
                "Welcome/Farewell Event"
            ]
        }
        
        # Flattened list for LLM prompt
        self.all_meeting_types = []
        for category, types in self.enterprise_taxonomy.items():
            for meeting_type in types:
                self.all_meeting_types.append(f"{meeting_type} ({category})")
    
    def test_model_availability(self) -> bool:
        """Test if GPT-4.1 model is available and accessible"""
        try:
            # Try to authenticate
            token = self._acquire_token()
            if not token:
                logging.error("Failed to acquire authentication token")
                return False
            
            # Try a simple test query
            import uuid
            test_prompt = "Respond with 'OK' if you can read this message."
            scenario_guid = str(uuid.uuid4())
            
            headers = {
                "Authorization": f"Bearer {token}",
                "X-ModelType": self.model,  # Required header!
                "X-ScenarioGUID": scenario_guid,
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": test_prompt}
                ],
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "max_completion_tokens": 10,
                "temperature": 0.1,
                "top_p": 1,
                "n": 1,
                "stream": False,
                "response_format": None,
            }
            
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return "OK" in content.upper()
            else:
                logging.error(f"Test request failed: {response.status_code}")
                logging.error(f"Response: {response.text[:500]}")
                return False
                
        except Exception as e:
            logging.error(f"GPT-4.1 availability test failed: {e}")
            return False
    
    def classify_meeting_with_llm(
        self,
        subject: str,
        description: str = "",
        attendees: Optional[List[str]] = None,
        duration_minutes: int = 60
    ) -> Dict[str, Any]:
        """
        Classify meeting using GPT-4.1 with contextual information.
        
        Args:
            subject: Meeting title/subject
            description: Meeting description or body
            attendees: List of attendee names/emails
            duration_minutes: Meeting duration in minutes
            
        Returns:
            Classification result with type, category, confidence, and reasoning
        """
        
        # Prepare meeting context
        meeting_context = self._prepare_meeting_context(
            subject, description, attendees, duration_minutes
        )
        
        # Create classification prompt
        prompt = self._create_classification_prompt(meeting_context)
        
        # System message
        system_message = (
            "You are an expert business analyst specializing in meeting classification. "
            "You analyze meeting information and classify them according to enterprise "
            "meeting taxonomy with high accuracy (97-99%). You provide specific meeting "
            "types with confidence scores and clear reasoning."
        )
        
        # Call GPT-4.1 API with retry logic
        for attempt in range(self.max_retries):
            try:
                # Rate limiting - enforce minimum delay between requests
                current_time = time.time()
                time_since_last_request = current_time - self._last_request_time
                if time_since_last_request < self.rate_limit_delay:
                    sleep_time = self.rate_limit_delay - time_since_last_request
                    time.sleep(sleep_time)
                
                # Make API call
                self._last_request_time = time.time()
                llm_output = self._call_gpt41_api(system_message, prompt)
                
                # Parse response
                classification = self._parse_llm_response(llm_output)
                
                return classification
                
            except Exception as e:
                error_str = str(e)
                
                # Handle rate limiting with proper Retry-After respect
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    if attempt < self.max_retries - 1:
                        # Extract retry_after from error message if present
                        retry_wait = self.retry_delay * (2 ** attempt)  # Default exponential backoff
                        
                        # Check if error message contains "Retry after Xs"
                        import re
                        match = re.search(r'Retry after (\d+)s', error_str)
                        if match:
                            retry_wait = int(match.group(1))
                            logging.warning(f"Rate limited (429). Server requested {retry_wait}s wait. Retrying (attempt {attempt + 1}/{self.max_retries})")
                        else:
                            logging.warning(f"Rate limited. Using exponential backoff: {retry_wait}s (attempt {attempt + 1}/{self.max_retries})")
                        
                        time.sleep(retry_wait)
                        continue
                    else:
                        logging.error(f"GPT-4.1 rate limit exceeded after {self.max_retries} attempts")
                        return self._fallback_classification(subject, description)
                
                # Handle other errors
                if attempt < self.max_retries - 1:
                    logging.warning(f"GPT-4.1 call failed: {e}. Retrying (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logging.error(f"GPT-4.1 classification failed after {self.max_retries} attempts: {e}")
                    # Fallback to keyword classification
                    return self._fallback_classification(subject, description)
        
        return self._fallback_classification(subject, description)
    
    def classify_meeting(
        self,
        subject: str,
        description: str = "",
        attendees: Optional[List[str]] = None,
        duration_minutes: int = 60,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        Convenience method for meeting classification.
        Falls back to keyword-based if LLM unavailable or use_llm=False.
        """
        if use_llm:
            return self.classify_meeting_with_llm(subject, description, attendees, duration_minutes)
        else:
            return self._fallback_classification(subject, description)
    
    def _acquire_token(self) -> Optional[str]:
        """Acquire authentication token using MSAL (matches GPT-5 pattern)"""
        
        # Use provided token if available
        if self.access_token:
            return self.access_token
        
        # Use cached token if available
        if self._cached_token:
            return self._cached_token
        
        try:
            # Initialize MSAL app with Windows broker support
            authority = f"https://login.microsoftonline.com/{TENANT_ID}"
            app = msal.PublicClientApplication(
                self.app_id,
                authority=authority,
                enable_broker_on_windows=True,  # Use Windows broker for auth
            )
            
            # Try to get cached account
            accounts = app.get_accounts()
            account = accounts[0] if accounts else None
            
            # Try silent token acquisition first
            if account:
                result = app.acquire_token_silent(self.scopes, account=account)
                if result and "access_token" in result:
                    self._cached_token = result["access_token"]
                    return self._cached_token
            
            # Interactive authentication if silent fails
            result = app.acquire_token_interactive(
                self.scopes,
                parent_window_handle=msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE,
            )
            
            if result and "access_token" in result:
                self._cached_token = result["access_token"]
                return self._cached_token
            
            error_desc = (result or {}).get("error_description", "Unknown error")
            logging.error(f"Failed to acquire token: {error_desc}")
            return None
                
        except Exception as e:
            logging.error(f"MSAL authentication failed: {e}")
            return None
    
    def _call_gpt41_api(self, system_message: str, user_prompt: str) -> str:
        """Call GPT-4.1 API with retry logic and throttling handling"""
        
        # Acquire token
        token = self._acquire_token()
        if not token:
            raise RuntimeError("Failed to acquire authentication token")
        
        # Prepare request (matching SilverFlow eval.py pattern)
        import uuid
        scenario_guid = str(uuid.uuid4())
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-ModelType": self.model,  # Critical header for SilverFlow
            "X-ScenarioGUID": scenario_guid,
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "max_completion_tokens": 2048,  # Note: max_completion_tokens, not max_tokens
            "temperature": 0.1,  # Low temperature for consistent classification
            "top_p": 1,
            "n": 1,
            "stream": False,
            "response_format": None,
        }
        
        # Make request
        response = requests.post(
            self.endpoint,
            headers=headers,
            data=json.dumps(payload),  # Note: data=json.dumps(), not json=
            timeout=120
        )
        
        # Handle response
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                return content
            else:
                raise RuntimeError("No choices in API response")
        elif response.status_code == 429:
            # Rate limited - get retry-after header
            retry_after = int(response.headers.get("Retry-After", self.retry_delay))
            raise RuntimeError(f"Rate limited (429). Retry after {retry_after}s")
        elif response.status_code >= 500:
            # Server error - retry
            raise RuntimeError(f"Server error ({response.status_code})")
        else:
            # Other error
            error_msg = response.text[:500]  # Truncate long errors
            raise RuntimeError(f"API call failed ({response.status_code}): {error_msg}")
    
    def _prepare_meeting_context(
        self,
        subject: str,
        description: str,
        attendees: Optional[List[str]],
        duration_minutes: int
    ) -> str:
        """Prepare comprehensive meeting context for LLM analysis"""
        
        context_parts = []
        
        # Subject
        if subject:
            context_parts.append(f"Meeting Title: {subject}")
        
        # Description
        if description:
            clean_desc = re.sub(r'<[^>]+>', '', description)
            clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
            if clean_desc and len(clean_desc) > 10:
                if len(clean_desc) > 500:
                    clean_desc = clean_desc[:497] + "..."
                context_parts.append(f"Description: {clean_desc}")
        
        # Attendee analysis
        if attendees:
            attendee_count = len(attendees)
            context_parts.append(f"Number of Attendees: {attendee_count}")
            
            if attendee_count == 2:
                context_parts.append("Meeting Pattern: One-on-one meeting")
            elif attendee_count > 50:
                context_parts.append("Meeting Pattern: Large broadcast meeting (>50 people)")
            elif attendee_count > 20:
                context_parts.append("Meeting Pattern: Large group meeting (20-50 people)")
            elif attendee_count > 10:
                context_parts.append("Meeting Pattern: Medium group meeting (10-20 people)")
            else:
                context_parts.append("Meeting Pattern: Small group meeting (<10 people)")
        
        # Duration analysis
        if duration_minutes:
            context_parts.append(f"Duration: {duration_minutes} minutes")
            
            if duration_minutes <= 15:
                context_parts.append("Duration Pattern: Very short (likely quick sync or standup)")
            elif duration_minutes <= 30:
                context_parts.append("Duration Pattern: Short (likely status update or brief discussion)")
            elif duration_minutes >= 240:
                context_parts.append("Duration Pattern: Very long (likely workshop, training, or strategic planning)")
            elif duration_minutes >= 120:
                context_parts.append("Duration Pattern: Long (likely deep-dive or collaborative session)")
        
        return "\n".join(context_parts)
    
    def _create_classification_prompt(self, meeting_context: str) -> str:
        """Create classification prompt for LLM"""
        
        prompt = f"""Classify the following meeting according to the Enterprise Meeting Taxonomy.

MEETING INFORMATION:
{meeting_context}

ENTERPRISE MEETING TAXONOMY (5 categories, 31+ types):

1. Strategic Planning & Decision
   - Strategic Planning Session, Decision-Making Meeting, Problem-Solving Meeting
   - Brainstorming Session, Workshop/Design Session, Budget Planning Meeting
   - Project Planning Meeting, Risk Assessment Meeting

2. Internal Recurring (Cadence)
   - Team Status Update/Standup, Progress Review Meeting, One-on-One Meeting
   - Team Retrospective, Governance/Leadership Meeting, Performance Review
   - Weekly/Monthly Check-in

3. External & Client-Facing
   - Sales & Client Meeting, Vendor/Supplier Meeting, Partnership Meeting
   - Interview Meeting, Client Training/Onboarding, Customer Discovery Call
   - Contract Negotiation

4. Informational & Broadcast
   - All-Hands/Town Hall, Informational Briefing, Training Session
   - Webinar/Presentation, Knowledge Sharing Session, Product Demo
   - Announcement Meeting

5. Team-Building & Culture
   - Team-Building Activity, Recognition/Celebration Event, Social/Networking Event
   - Community Meeting, Offsite/Retreat, Welcome/Farewell Event

TASK:
Analyze the meeting information and provide classification in this EXACT JSON format:
{{
    "specific_type": "exact meeting type from taxonomy above",
    "primary_category": "one of the 5 main categories",
    "confidence": 0.95,
    "reasoning": "brief explanation (1-2 sentences)"
}}

Return ONLY valid JSON, no additional text."""

        return prompt
    
    def _parse_llm_response(self, llm_output: str) -> Dict[str, Any]:
        """Parse LLM response to extract classification"""
        
        try:
            # Try to parse as JSON directly
            classification = json.loads(llm_output.strip())
            
            # Validate required fields
            if all(k in classification for k in ["specific_type", "primary_category"]):
                if "confidence" in classification:
                    classification["confidence"] = float(classification.get("confidence", 0.8))
                else:
                    classification["confidence"] = 0.8
                
                return classification
            
            # If missing fields, try to extract from text
            logging.warning("JSON missing required fields, using text extraction")
            return self._extract_from_text(llm_output)
            
        except json.JSONDecodeError:
            logging.warning("Failed to parse JSON from LLM response, using text extraction")
            return self._extract_from_text(llm_output)
        except Exception as e:
            logging.error(f"Failed to parse LLM response: {e}")
            return {
                "specific_type": "Unknown",
                "primary_category": "Unknown",
                "confidence": 0.3,
                "reasoning": "Failed to parse LLM response"
            }
    
    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract classification from unstructured text response"""
        
        for category, types in self.enterprise_taxonomy.items():
            if category.lower() in text.lower():
                for meeting_type in types:
                    if meeting_type.lower() in text.lower():
                        return {
                            "specific_type": meeting_type,
                            "primary_category": category,
                            "confidence": 0.7,
                            "reasoning": "Extracted from unstructured LLM response"
                        }
        
        return {
            "specific_type": "Unknown",
            "primary_category": "Unknown",
            "confidence": 0.3,
            "reasoning": "Could not extract classification from response"
        }
    
    def _fallback_classification(self, subject: str, description: str) -> Dict[str, Any]:
        """Fallback keyword-based classification when LLM is unavailable"""
        
        text = f"{subject} {description}".lower()
        
        patterns = [
            (["1:1", "one-on-one", "1-on-1"], "One-on-One Meeting", "Internal Recurring (Cadence)"),
            (["standup", "stand-up", "daily", "status", "sync"], "Team Status Update/Standup", "Internal Recurring (Cadence)"),
            (["all-hands", "town hall"], "All-Hands/Town Hall", "Informational & Broadcast"),
            (["review", "retrospective", "retro"], "Progress Review Meeting", "Internal Recurring (Cadence)"),
            (["strategic", "planning", "strategy"], "Strategic Planning Session", "Strategic Planning & Decision"),
            (["brainstorm", "ideation", "workshop"], "Brainstorming Session", "Strategic Planning & Decision"),
            (["training", "learning", "onboarding"], "Training Session", "Informational & Broadcast"),
            (["sales", "client", "customer"], "Sales & Client Meeting", "External & Client-Facing"),
            (["interview", "candidate"], "Interview Meeting", "External & Client-Facing"),
        ]
        
        for keywords, meeting_type, category in patterns:
            if any(keyword in text for keyword in keywords):
                return {
                    "specific_type": meeting_type,
                    "primary_category": category,
                    "confidence": 0.6,
                    "reasoning": "Keyword-based classification (fallback mode)"
                }
        
        return {
            "specific_type": "Team Status Update/Standup",
            "primary_category": "Internal Recurring (Cadence)",
            "confidence": 0.4,
            "reasoning": "Default classification - insufficient context"
        }


def main():
    """Demo usage of GPT41MeetingClassifier"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 80)
    print("GPT-4.1 Meeting Classifier Demo")
    print("Model: dev-gpt-41-shortco-2025-04-14")
    print("=" * 80)
    
    # Initialize classifier
    print("\n1. Initializing GPT-4.1 Meeting Classifier...")
    try:
        classifier = GPT41MeetingClassifier()
        print(f"   Classifier initialized")
        print(f"   Model: {classifier.model}")
        print(f"   Endpoint: {classifier.endpoint}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test availability
    print("\n2. Testing GPT-4.1 model availability...")
    is_available = classifier.test_model_availability()
    
    if is_available:
        print("   OK GPT-4.1 model is available and ready")
    else:
        print("   WARNING GPT-4.1 model not available - will use fallback classification")
    
    # Test classifications
    test_meetings = [
        {
            "subject": "Weekly Team Sync",
            "description": "Quick status update on current sprint progress",
            "attendees": ["Alice", "Bob", "Charlie", "Diana"],
            "duration": 30
        },
        {
            "subject": "Q4 Strategy Planning",
            "description": "Strategic planning session for Q4 2025 initiatives and budget allocation",
            "attendees": ["VP Sales", "VP Engineering", "CFO", "CEO", "Product Director"],
            "duration": 120
        },
        {
            "subject": "Coffee Chat with Sarah",
            "description": "1:1 catch up",
            "attendees": ["Me", "Sarah"],
            "duration": 30
        }
    ]
    
    print("\n3. Classifying test meetings...")
    print("=" * 80)
    
    for i, meeting in enumerate(test_meetings, 1):
        print(f"\nTest Meeting #{i}:")
        print(f"  Subject: {meeting['subject']}")
        print(f"  Attendees: {len(meeting['attendees'])} people")
        print(f"  Duration: {meeting['duration']} minutes")
        
        result = classifier.classify_meeting(
            subject=meeting['subject'],
            description=meeting['description'],
            attendees=meeting['attendees'],
            duration_minutes=meeting['duration'],
            use_llm=is_available
        )
        
        print(f"\n  Classification Result:")
        print(f"    Type: {result['specific_type']}")
        print(f"    Category: {result['primary_category']}")
        print(f"    Confidence: {result['confidence']:.1%}")
        print(f"    Reasoning: {result['reasoning']}")
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print("Demo completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
