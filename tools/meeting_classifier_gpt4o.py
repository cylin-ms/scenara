#!/usr/bin/env python3
"""
GPT-4o Meeting Classifier using OpenAI API
Enterprise meeting classification with the latest GPT-4o model

Supports multiple GPT-4o variants:
- gpt-4o (latest) - Most capable, multimodal
- gpt-4o-2024-11-20 - Specific version with 128K context
- gpt-4o-2024-08-06 - Structured outputs support
- gpt-4o-2024-05-13 - Original release
- gpt-4o-mini - Cost-effective variant
"""

import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional

# Try to import from tools directory or current directory
try:
    from tools.llm_api import LLMAPIClient
except ImportError:
    try:
        from llm_api import LLMAPIClient
    except ImportError:
        LLMAPIClient = None

try:
    import openai
except ImportError:
    openai = None

# Default model configuration
DEFAULT_MODEL = "gpt-4o"  # Latest GPT-4o
AVAILABLE_MODELS = {
    "gpt-4o": "Latest GPT-4o (recommended)",
    "gpt-4o-2024-11-20": "GPT-4o November 2024 (128K context)",
    "gpt-4o-2024-08-06": "GPT-4o August 2024 (structured outputs)",
    "gpt-4o-2024-05-13": "GPT-4o May 2024 (original)",
    "gpt-4o-mini": "GPT-4o Mini (cost-effective)",
    "gpt-4o-mini-2024-07-18": "GPT-4o Mini July 2024"
}


class GPT4oMeetingClassifier:
    """
    Enterprise Meeting Classifier using OpenAI's GPT-4o model.
    
    Features:
    - Uses latest GPT-4o for high-accuracy classification
    - Integrates with Scenara's LLMAPIClient infrastructure
    - Enterprise Meeting Taxonomy with 31+ meeting types
    - Rate limiting and retry logic for robustness
    - Fallback to keyword-based classification
    - Structured JSON output with confidence scores
    """
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        use_llm_api_client: bool = True,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        rate_limit_delay: float = 0.5,
    ):
        """
        Initialize GPT-4o classifier.
        
        Args:
            model: GPT-4o model variant to use
            use_llm_api_client: Use LLMAPIClient infrastructure (recommended)
            api_key: OpenAI API key (only if not using LLMAPIClient)
            max_retries: Maximum number of retry attempts
            retry_delay: Base delay between retries (seconds)
            rate_limit_delay: Minimum delay between requests (seconds)
        """
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        
        # Initialize LLM client
        self.use_llm_api_client = use_llm_api_client and LLMAPIClient is not None
        
        if self.use_llm_api_client:
            # Use Scenara's LLMAPIClient (preferred)
            try:
                self.llm_client = LLMAPIClient()
                
                # Check if OpenAI client is actually configured
                if hasattr(self.llm_client, 'openai_client') and self.llm_client.openai_client is not None:
                    self.client = None
                    logging.info("Using LLMAPIClient for GPT-4o integration")
                else:
                    logging.warning("LLMAPIClient initialized but OpenAI client not configured (missing OPENAI_API_KEY)")
                    self.use_llm_api_client = False
                    
            except Exception as e:
                logging.warning(f"Failed to initialize LLMAPIClient: {e}. Falling back to direct OpenAI client")
                self.use_llm_api_client = False
        
        if not self.use_llm_api_client:
            # Fallback to direct OpenAI client
            if openai is None:
                raise RuntimeError("openai package not installed. Install with `pip install openai`")
            
            api_key_to_use = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key_to_use:
                raise RuntimeError(
                    "OpenAI API key not configured. Set OPENAI_API_KEY environment variable or pass api_key parameter.\n"
                    "Get your API key from: https://platform.openai.com/api-keys"
                )
            
            self.client = openai.OpenAI(api_key=api_key_to_use)
            self.llm_client = None
            logging.info("Using direct OpenAI client for GPT-4o")
        
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
        """Test if GPT-4o model is available and accessible"""
        try:
            if self.use_llm_api_client:
                # Test using LLMAPIClient
                response = self.llm_client.query_llm(
                    prompt="Respond with 'OK' if you can read this.",
                    provider="openai",
                    model=self.model
                )
                return "OK" in response.upper()
            else:
                # Test using direct OpenAI client
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Respond with 'OK' if you can read this."}
                    ],
                    max_tokens=10,
                    temperature=0.1
                )
                return response.choices[0].message.content.strip().upper() == "OK"
        except Exception as e:
            logging.error(f"GPT-4o availability test failed: {e}")
            return False
    
    def classify_meeting_with_llm(
        self,
        subject: str,
        description: str = "",
        attendees: Optional[List[str]] = None,
        duration_minutes: int = 60
    ) -> Dict[str, Any]:
        """
        Classify meeting using GPT-4o with contextual information.
        
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
        
        # Call GPT-4o API with retry logic
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                current_time = time.time()
                time_since_last_request = current_time - self._last_request_time
                if time_since_last_request < self.rate_limit_delay:
                    sleep_time = self.rate_limit_delay - time_since_last_request
                    time.sleep(sleep_time)
                
                # Make API call
                self._last_request_time = time.time()
                
                if self.use_llm_api_client:
                    # Use LLMAPIClient - combine system message and prompt
                    full_prompt = f"{system_message}\n\n{prompt}\n\nIMPORTANT: Return ONLY valid JSON in this format:\n{{\n    \"specific_type\": \"meeting type\",\n    \"primary_category\": \"category name\",\n    \"confidence\": 0.95,\n    \"reasoning\": \"explanation\"\n}}"
                    
                    llm_output = self.llm_client.query_llm(
                        prompt=full_prompt,
                        provider="openai",
                        model=self.model
                    )
                else:
                    # Use direct OpenAI client with structured output
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,  # Low temperature for consistent classification
                        max_tokens=500,
                        response_format={"type": "json_object"}  # Force JSON output
                    )
                    llm_output = response.choices[0].message.content
                
                # Parse response
                classification = self._parse_llm_response(llm_output)
                
                return classification
                
            except Exception as e:
                error_str = str(e)
                
                # Handle rate limiting
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    if attempt < self.max_retries - 1:
                        retry_wait = self.retry_delay * (2 ** attempt)  # Exponential backoff
                        logging.warning(f"Rate limited. Retrying in {retry_wait}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(retry_wait)
                        continue
                
                # Handle other errors
                if attempt < self.max_retries - 1:
                    logging.warning(f"GPT-4o call failed: {e}. Retrying (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logging.error(f"GPT-4o classification failed after {self.max_retries} attempts: {e}")
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
            # Try to parse as JSON directly
            classification = json.loads(llm_output.strip())
            
            # Validate required fields
            if all(k in classification for k in ["specific_type", "primary_category"]):
                # Ensure confidence is float
                if "confidence" in classification:
                    classification["confidence"] = float(classification.get("confidence", 0.8))
                else:
                    classification["confidence"] = 0.8
                
                return classification
            
            # If missing fields, try to extract from text
            logging.warning("JSON missing required fields, using text extraction")
            return self._extract_from_text(llm_output)
            
        except json.JSONDecodeError:
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
    """Demo usage of GPT4oMeetingClassifier"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 80)
    print("GPT-4o Meeting Classifier Demo")
    print("=" * 80)
    
    # Show available models
    print("\nAvailable GPT-4o Models:")
    for model, description in AVAILABLE_MODELS.items():
        print(f"  - {model}: {description}")
    
    # Initialize classifier
    print(f"\n1. Initializing GPT-4o Meeting Classifier (model: {DEFAULT_MODEL})...")
    try:
        classifier = GPT4oMeetingClassifier()
        if classifier.use_llm_api_client:
            print(f"   ✅ Classifier initialized with LLMAPIClient")
        else:
            print(f"   ✅ Classifier initialized with direct OpenAI client")
        print(f"   Model: {classifier.model}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("\n   SETUP REQUIRED:")
        print("   1. Get OpenAI API key from: https://platform.openai.com/api-keys")
        print("   2. Set environment variable:")
        print("      Windows (PowerShell): $env:OPENAI_API_KEY = 'sk-...'")
        print("      Linux/Mac: export OPENAI_API_KEY='sk-...'")
        print("   3. Or add to .env file: OPENAI_API_KEY=sk-...")
        return
    
    # Test availability
    print("\n2. Testing GPT-4o model availability...")
    is_available = classifier.test_model_availability()
    
    if is_available:
        print("   OK GPT-4o model is available and ready")
    else:
        print("   WARNING GPT-4o model not available - will use fallback classification")
    
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
