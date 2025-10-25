#!/usr/bin/env python3
"""
GPT5-Based Meeting Classifier using SilverFlow LLM API
Enterprise meeting classification with dev-gpt-5-chat-jj model
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import msal
except ImportError:
    msal = None

try:
    import requests
except ImportError:
    requests = None

# SilverFlow LLM API Configuration
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
DEFAULT_APP_ID = "942b706f-826e-426b-98f7-59e1e376b37c"
DEFAULT_SCOPES = ["https://substrate.office.com/llmapi/LLMAPI.dev"]
DEFAULT_ENDPOINT = "https://fe-26.qas.bing.net/chat/completions"
DEFAULT_MODEL = "dev-gpt-5-chat-jj"

DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_READ_TIMEOUT = 60


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ClassificationResult:
    success: bool
    specific_type: Optional[str] = None
    primary_category: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    error: Optional[str] = None
    response_content: Optional[str] = None


class GPT5MeetingClassifier:
    """
    Enterprise Meeting Classifier using Microsoft's GPT-5 model via SilverFlow LLM API.
    
    Features:
    - Uses dev-gpt-5-chat-jj model for high-accuracy classification
    - Enterprise Meeting Taxonomy with 31+ meeting types
    - MSAL authentication with Azure AD
    - Fallback to keyword-based classification
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
        rate_limit_delay: float = 0.5,
    ):
        self.model = model
        self.endpoint = endpoint
        self.app_id = app_id
        self.scopes = scopes or DEFAULT_SCOPES
        self.access_token = access_token
        self._cached_token: Optional[str] = None
        
        # Rate limiting and retry configuration
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        
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
        """Test if GPT-5 model is available and accessible"""
        try:
            token = self._acquire_token()
            if not token:
                logging.warning("Failed to acquire access token for GPT-5 model")
                return False
            
            # Try a simple test query
            result = self._call_gpt5_api(
                system_message="You are a helpful assistant.",
                user_prompt="Respond with 'OK' if you can read this.",
                timeout=10
            )
            
            return result.success
        except Exception as e:
            logging.error(f"GPT-5 availability test failed: {e}")
            return False
    
    def classify_meeting_with_llm(
        self,
        subject: str,
        description: str = "",
        attendees: Optional[List[str]] = None,
        duration_minutes: int = 60
    ) -> Dict[str, Any]:
        """
        Classify meeting using GPT-5 LLM with contextual information.
        
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
        
        # Call GPT-5 API
        result = self._call_gpt5_api(
            system_message=system_message,
            user_prompt=prompt,
            timeout=DEFAULT_READ_TIMEOUT
        )
        
        if not result.success:
            logging.error(f"GPT-5 classification failed: {result.error}")
            # Fallback to keyword classification
            return self._fallback_classification(subject, description)
        
        # Parse LLM response
        classification = self._parse_llm_response(result.response_content or "")
        
        return classification
    
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
            try:
                return self.classify_meeting_with_llm(
                    subject, description, attendees, duration_minutes
                )
            except Exception as e:
                logging.error(f"LLM classification failed, using fallback: {e}")
        
        return self._fallback_classification(subject, description)
    
    def _acquire_token(self) -> Optional[str]:
        """Acquire access token using MSAL authentication"""
        
        # Use provided token if available
        if self.access_token:
            return self.access_token
        
        # Use cached token if available
        if self._cached_token:
            return self._cached_token
        
        # Acquire new token
        if msal is None:
            raise RuntimeError("msal is not installed. Install with `pip install msal`")
        
        try:
            authority = f"https://login.microsoftonline.com/{TENANT_ID}"
            app = msal.PublicClientApplication(
                self.app_id,
                authority=authority,
                enable_broker_on_windows=True,
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
            logging.error(f"Token acquisition failed: {e}")
            return None
    
    def _call_gpt5_api(
        self,
        system_message: str,
        user_prompt: str,
        timeout: float = DEFAULT_READ_TIMEOUT
    ) -> ClassificationResult:
        """
        Call GPT-5 API via SilverFlow endpoint with rate limiting and retry logic.
        
        Args:
            system_message: System message for the model
            user_prompt: User prompt content
            timeout: Request timeout in seconds
            
        Returns:
            ClassificationResult with success status and response
        """
        
        if requests is None:
            raise RuntimeError("requests is not installed. Install with `pip install requests`")
        
        # Retry loop for handling throttling
        for attempt in range(self.max_retries):
            try:
                # Rate limiting: ensure minimum delay between requests
                current_time = time.time()
                time_since_last_request = current_time - self._last_request_time
                if time_since_last_request < self.rate_limit_delay:
                    sleep_time = self.rate_limit_delay - time_since_last_request
                    logging.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                
                # Acquire token
                token = self._acquire_token()
                if not token:
                    return ClassificationResult(
                        success=False,
                        error="Failed to acquire access token"
                    )
                
                # Build request payload
                messages = [
                    ChatMessage(role="system", content=system_message),
                    ChatMessage(role="user", content=user_prompt),
                ]
                
                payload = {
                    "messages": [
                        {"role": m.role, "content": m.content} for m in messages
                    ],
                    "presence_penalty": 0,
                    "frequency_penalty": 0,
                    "max_completion_tokens": 2048,
                    "temperature": 0.1,  # Low temperature for consistent classification
                    "top_p": 0.95,
                    "n": 1,
                    "stream": False,
                    "response_format": None,
                }
                
                # Generate scenario GUID for telemetry
                scenario_guid = str(uuid.uuid4())
                
                # Build request headers
                headers = {
                    "Authorization": f"Bearer {token}",
                    "X-ModelType": self.model,
                    "X-ScenarioGUID": scenario_guid,
                    "Content-Type": "application/json",
                }
                
                # Make API request
                self._last_request_time = time.time()
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=timeout,
                )
                
                # Handle throttling (429 Too Many Requests)
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        retry_after = float(response.headers.get('Retry-After', self.retry_delay * (attempt + 1)))
                        logging.warning(f"Rate limited (429). Retrying in {retry_after}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(retry_after)
                        continue
                    else:
                        return ClassificationResult(
                            success=False,
                            error=f"Rate limit exceeded after {self.max_retries} attempts"
                        )
                
                # Handle other error responses
                if not response.ok:
                    error_message = self._extract_error_message(response)
                    
                    # Retry on server errors (5xx)
                    if response.status_code >= 500 and attempt < self.max_retries - 1:
                        logging.warning(f"Server error {response.status_code}. Retrying in {self.retry_delay}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                        continue
                    
                    return ClassificationResult(
                        success=False,
                        error=f"HTTP {response.status_code}: {error_message}"
                    )
                
                # Parse response
                try:
                    response_body = response.json()
                except Exception as exc:
                    return ClassificationResult(
                        success=False,
                        error=f"Failed to decode JSON response: {exc}"
                    )
                
                # Extract content
                content = self._extract_response_content(response_body)
                
                if content:
                    return ClassificationResult(
                        success=True,
                        response_content=content
                    )
                else:
                    return ClassificationResult(
                        success=False,
                        error="No content in response"
                    )
                    
            except Exception as exc:
                if attempt < self.max_retries - 1:
                    logging.warning(f"Request failed: {exc}. Retrying in {self.retry_delay}s (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return ClassificationResult(
                        success=False,
                        error=f"HTTP request failed after {self.max_retries} attempts: {exc}"
                    )
        
        return ClassificationResult(
            success=False,
            error=f"Failed after {self.max_retries} retry attempts"
        )
    
    def _extract_error_message(self, response) -> str:
        """Extract error message from failed response"""
        try:
            response_body = response.json()
            error_field = response_body.get("error")
            
            if isinstance(error_field, dict):
                return error_field.get("message") or error_field.get("code") or "Unknown error"
            elif isinstance(error_field, str):
                return error_field
            
            return json.dumps(response_body)[:400]
        except Exception:
            return response.text[:400]
    
    def _extract_response_content(self, response_body: Dict[str, Any]) -> Optional[str]:
        """Extract content from successful response"""
        choices = response_body.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message") if isinstance(choices[0], dict) else None
            if isinstance(message, dict):
                content_field = message.get("content")
                if isinstance(content_field, str):
                    return content_field
        return None
    
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
            # Clean up description
            clean_desc = re.sub(r'<[^>]+>', '', description)  # Remove HTML tags
            clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()  # Normalize whitespace
            if clean_desc and len(clean_desc) > 10:
                # Truncate very long descriptions
                if len(clean_desc) > 500:
                    clean_desc = clean_desc[:497] + "..."
                context_parts.append(f"Description: {clean_desc}")
        
        # Attendee analysis
        if attendees:
            attendee_count = len(attendees)
            context_parts.append(f"Number of Attendees: {attendee_count}")
            
            # Analyze attendee patterns
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
            # Try to extract JSON from response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', llm_output, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                classification = json.loads(json_str)
                
                # Validate required fields
                if all(k in classification for k in ["specific_type", "primary_category"]):
                    # Ensure confidence is float
                    if "confidence" in classification:
                        classification["confidence"] = float(classification.get("confidence", 0.8))
                    else:
                        classification["confidence"] = 0.8
                    
                    return classification
            
            # If JSON parsing fails, try to extract from text
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
        
        # Try to find category and type mentions
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
        
        # Keyword patterns for common meeting types
        patterns = [
            # One-on-One
            (["1:1", "one-on-one", "1-on-1", "individual"], 
             "One-on-One Meeting", "Internal Recurring (Cadence)"),
            
            # Status/Standup
            (["standup", "stand-up", "daily", "status", "sync", "check-in"],
             "Team Status Update/Standup", "Internal Recurring (Cadence)"),
            
            # All-Hands
            (["all-hands", "all hands", "town hall", "townhall"],
             "All-Hands/Town Hall", "Informational & Broadcast"),
            
            # Review meetings
            (["review", "retrospective", "retro", "postmortem"],
             "Progress Review Meeting", "Internal Recurring (Cadence)"),
            
            # Strategic/Planning
            (["strategic", "planning", "strategy", "roadmap"],
             "Strategic Planning Session", "Strategic Planning & Decision"),
            
            # Brainstorming
            (["brainstorm", "ideation", "workshop"],
             "Brainstorming Session", "Strategic Planning & Decision"),
            
            # Training
            (["training", "workshop", "learning", "onboarding"],
             "Training Session", "Informational & Broadcast"),
            
            # Sales/Client
            (["sales", "client", "customer", "prospect"],
             "Sales & Client Meeting", "External & Client-Facing"),
            
            # Interview
            (["interview", "candidate", "hiring"],
             "Interview Meeting", "External & Client-Facing"),
        ]
        
        for keywords, meeting_type, category in patterns:
            if any(keyword in text for keyword in keywords):
                return {
                    "specific_type": meeting_type,
                    "primary_category": category,
                    "confidence": 0.6,
                    "reasoning": f"Keyword-based classification (fallback mode)"
                }
        
        # Default classification
        return {
            "specific_type": "Team Status Update/Standup",
            "primary_category": "Internal Recurring (Cadence)",
            "confidence": 0.4,
            "reasoning": "Default classification - insufficient context"
        }


def main():
    """Demo usage of GPT5MeetingClassifier"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 80)
    print("GPT-5 Meeting Classifier Demo")
    print("=" * 80)
    
    # Initialize classifier
    print("\n1. Initializing GPT-5 Meeting Classifier...")
    classifier = GPT5MeetingClassifier()
    
    # Test availability
    print("\n2. Testing GPT-5 model availability...")
    is_available = classifier.test_model_availability()
    
    if is_available:
        print("✅ GPT-5 model is available and ready")
    else:
        print("⚠️  GPT-5 model not available - will use fallback classification")
    
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
        },
        {
            "subject": "Client Demo - Acme Corp",
            "description": "Product demo for Acme Corporation stakeholders",
            "attendees": ["Sales Rep", "Solutions Architect", "Acme CTO", "Acme Product Manager"],
            "duration": 60
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
