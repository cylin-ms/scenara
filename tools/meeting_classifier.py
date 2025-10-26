#!/usr/bin/env python3
"""
LLM-Based Meeting Classifier using Ollama
Enhanced meeting classification with gpt-oss:20b model
"""

import ollama
import json
import re
from typing import Dict, Any, List, Optional
import logging

class OllamaLLMMeetingClassifier:
    def __init__(self, model_name: str = "gpt-oss:20b"):
        self.model_name = model_name
        self.client = ollama.Client()
        
        # Enterprise Meeting Taxonomy - updated with more specific categories
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
    
    def classify_meeting_with_llm(self, subject: str, description: str = "", attendees: List[str] = None, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Classify a meeting using the LLM and return structured results
        """
        # Also provide alias for backward compatibility
        return self._classify_meeting_internal(subject, description, attendees, duration_minutes)

    def classify_meeting(self, subject: str, description: str = "", attendees: List[str] = None, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Alias for classify_meeting_with_llm for backward compatibility
        """
        return self.classify_meeting_with_llm(subject, description, attendees, duration_minutes)
    
    def _classify_meeting_internal(self, subject: str, description: str = "", attendees: List[str] = None, duration_minutes: int = 60) -> Dict[str, Any]:
        """Classify meeting using LLM with contextual information"""
        
        # Prepare context for LLM
        meeting_context = self._prepare_meeting_context(subject, description, attendees, duration_minutes)
        
        # Create prompt for LLM
        prompt = self._create_classification_prompt(meeting_context)
        
        try:
            # Call Ollama LLM
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business analyst specializing in meeting classification. You analyze meeting information and classify them according to enterprise meeting taxonomy with high accuracy."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.1,  # Low temperature for consistent classification
                    "top_p": 0.9,
                    "num_ctx": 4096
                }
            )
            
            # Parse LLM response
            llm_output = response['message']['content']
            classification = self._parse_llm_response(llm_output)
            
            return classification
            
        except Exception as e:
            logging.error(f"LLM classification failed: {e}")
            # Fallback to simple keyword classification
            return self._fallback_classification(subject, description)
    
    def classify_meeting(self, subject: str, description: str = "", attendees: List[str] = None, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Alias for classify_meeting_with_llm for cross-platform compatibility
        """
        return self.classify_meeting_with_llm(subject, description, attendees, duration_minutes)
    
    def _prepare_meeting_context(self, subject: str, description: str, attendees: List[str], duration_minutes: int) -> str:
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
            if clean_desc:
                context_parts.append(f"Description: {clean_desc}")
        
        # Attendee analysis
        if attendees:
            attendee_count = len(attendees)
            context_parts.append(f"Number of Attendees: {attendee_count}")
            
            # Analyze attendee patterns for additional context
            if attendee_count == 2:
                context_parts.append("Meeting Pattern: One-on-one meeting")
            elif attendee_count > 20:
                context_parts.append("Meeting Pattern: Large group meeting (likely all-hands or broadcast)")
            elif attendee_count > 10:
                context_parts.append("Meeting Pattern: Medium group meeting")
        
        # Duration analysis
        if duration_minutes:
            context_parts.append(f"Duration: {duration_minutes} minutes")
            
            if duration_minutes <= 30:
                context_parts.append("Duration Pattern: Short meeting (likely status update or brief discussion)")
            elif duration_minutes >= 240:
                context_parts.append("Duration Pattern: Extended meeting (likely workshop, training, or strategic session)")
            elif duration_minutes >= 120:
                context_parts.append("Duration Pattern: Long meeting (likely planning or deep-dive session)")
        
        return "\n".join(context_parts)
    
    def _create_classification_prompt(self, meeting_context: str) -> str:
        """Create detailed classification prompt for LLM"""
        
        meeting_types_text = "\n".join([f"- {mt}" for mt in self.all_meeting_types])
        
        prompt = f"""
Please analyze the following meeting information and classify it according to the Enterprise Meeting Taxonomy.

MEETING INFORMATION:
{meeting_context}

AVAILABLE MEETING TYPES:
{meeting_types_text}

CLASSIFICATION REQUIREMENTS:
1. Select the most appropriate meeting type from the list above
2. Provide the primary category (e.g., "Strategic Planning & Decision")
3. Provide the specific meeting type (e.g., "Budget Planning Meeting")
4. Assign a confidence score from 0.0 to 1.0
5. Provide a brief reasoning for your classification

RESPONSE FORMAT (JSON):
{{
    "primary_category": "Category Name",
    "specific_type": "Specific Meeting Type",
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this classification was chosen",
    "alternative_matches": ["Alternative Type 1", "Alternative Type 2"]
}}

Analyze the meeting information and provide your classification:"""
        
        return prompt
    
    def _parse_llm_response(self, llm_output: str) -> Dict[str, Any]:
        """Parse LLM response and extract classification"""
        
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                classification = json.loads(json_text)
                
                # Validate and normalize the response
                result = {
                    "primary_category": classification.get("primary_category", "Unknown"),
                    "specific_type": classification.get("specific_type", "General Business Meeting"),
                    "confidence": float(classification.get("confidence", 0.5)),
                    "reasoning": classification.get("reasoning", "LLM classification"),
                    "alternative_matches": classification.get("alternative_matches", []),
                    "classification_method": "LLM",
                    "llm_model": self.model_name
                }
                
                # Validate that the category exists in our taxonomy
                if result["primary_category"] not in self.enterprise_taxonomy:
                    result["primary_category"] = self._find_best_category_match(result["specific_type"])
                
                return result
            
        except Exception as e:
            logging.error(f"Failed to parse LLM response: {e}")
        
        # If parsing fails, try to extract information manually
        return self._manual_parse_llm_response(llm_output)
    
    def _manual_parse_llm_response(self, llm_output: str) -> Dict[str, Any]:
        """Manually parse LLM response if JSON parsing fails"""
        
        # Default values
        result = {
            "primary_category": "Internal Recurring (Cadence)",
            "specific_type": "General Business Meeting", 
            "confidence": 0.5,
            "reasoning": "Manual parsing of LLM response",
            "alternative_matches": [],
            "classification_method": "LLM_manual_parse",
            "llm_model": self.model_name
        }
        
        # Try to extract category and type from text
        for category, types in self.enterprise_taxonomy.items():
            if category.lower() in llm_output.lower():
                result["primary_category"] = category
                
                # Look for specific type
                for meeting_type in types:
                    if meeting_type.lower() in llm_output.lower():
                        result["specific_type"] = meeting_type
                        result["confidence"] = 0.7  # Higher confidence if we found specific type
                        break
                break
        
        # Try to extract confidence score
        confidence_match = re.search(r'confidence["\s]*:?\s*([0-9.]+)', llm_output, re.IGNORECASE)
        if confidence_match:
            try:
                confidence = float(confidence_match.group(1))
                if 0.0 <= confidence <= 1.0:
                    result["confidence"] = confidence
            except:
                pass
        
        return result
    
    def _find_best_category_match(self, specific_type: str) -> str:
        """Find best category match for a specific type"""
        
        for category, types in self.enterprise_taxonomy.items():
            for meeting_type in types:
                if specific_type.lower() in meeting_type.lower() or meeting_type.lower() in specific_type.lower():
                    return category
        
        return "Internal Recurring (Cadence)"  # Default fallback
    
    def _fallback_classification(self, subject: str, description: str) -> Dict[str, Any]:
        """Fallback classification if LLM fails"""
        
        text = f"{subject} {description}".lower()
        
        # Simple keyword-based fallback
        if any(word in text for word in ['standup', 'status', 'weekly', 'daily', 'check-in']):
            return {
                "primary_category": "Internal Recurring (Cadence)",
                "specific_type": "Team Status Update/Standup",
                "confidence": 0.6,
                "reasoning": "Keyword-based fallback classification",
                "alternative_matches": [],
                "classification_method": "fallback_keywords"
            }
        elif any(word in text for word in ['planning', 'strategy', 'roadmap', 'decision']):
            return {
                "primary_category": "Strategic Planning & Decision", 
                "specific_type": "Strategic Planning Session",
                "confidence": 0.6,
                "reasoning": "Keyword-based fallback classification",
                "alternative_matches": [],
                "classification_method": "fallback_keywords"
            }
        else:
            return {
                "primary_category": "Internal Recurring (Cadence)",
                "specific_type": "General Business Meeting",
                "confidence": 0.3,
                "reasoning": "Default fallback classification",
                "alternative_matches": [],
                "classification_method": "fallback_default"
            }
    
    def test_model_availability(self) -> bool:
        """Test if the Ollama model is available"""
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hello"}],
                options={"num_ctx": 100}
            )
            return True
        except Exception as e:
            logging.error(f"Model {self.model_name} not available: {e}")
            return False

def test_llm_classifier():
    """Test the LLM classifier with sample data"""
    
    classifier = OllamaLLMMeetingClassifier()
    
    # Test model availability
    if not classifier.test_model_availability():
        print(f"❌ Model {classifier.model_name} is not available. Please ensure:")
        print("1. Ollama is running: ollama serve")
        print("2. Model is installed: ollama pull gpt-oss:20b")
        return
    
    # Test cases
    test_cases = [
        {
            "subject": "Q3 Sprint Planning", 
            "description": "Planning for the next quarter development sprint with product team",
            "attendees": ["john@company.com", "sarah@company.com", "mike@company.com"],
            "duration": 120
        },
        {
            "subject": "Daily Standup",
            "description": "Quick daily sync on progress and blockers",  
            "attendees": ["dev1@company.com", "dev2@company.com", "pm@company.com"],
            "duration": 15
        },
        {
            "subject": "Client Demo - Product Walkthrough",
            "description": "Demonstrating new features to potential client",
            "attendees": ["sales@company.com", "client@external.com"],
            "duration": 60
        }
    ]
    
    print("🧠 Testing LLM-based Meeting Classifier")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['subject']}")
        
        result = classifier.classify_meeting_with_llm(
            subject=test_case['subject'],
            description=test_case['description'], 
            attendees=test_case['attendees'],
            duration_minutes=test_case['duration']
        )
        
        print(f"Category: {result['primary_category']}")
        print(f"Type: {result['specific_type']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Method: {result['classification_method']}")
        print(f"Reasoning: {result['reasoning']}")

if __name__ == "__main__":
    test_llm_classifier()