#!/usr/bin/env python3
"""
Azure DevOps Work Item Extraction for Workback Planning Training Data

This script extracts completed work items from Azure DevOps to create training data
for workback planning post-training. It focuses on Q2 (high value, low complexity)
work items as the initial pilot.

Author: Chin-Yew Lin
Date: November 11, 2025
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict
import sys

# Add parent directory to path for imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from azure.devops.connection import Connection
    from msrest.authentication import BasicAuthentication
    from azure.devops.v7_0.work_item_tracking import WorkItemTrackingClient
except ImportError:
    print("ERROR: azure-devops package not installed")
    print("Install with: pip install azure-devops")
    sys.exit(1)

# Import LLM API client
try:
    from tools.llm_api import LLMAPIClient
except ImportError:
    print("WARNING: LLMAPIClient not found. Will use heuristic classification only.")
    LLMAPIClient = None

# Add parent directory to path to import LLM API client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')))

LLMAPIClient = None
try:
    from tools.llm_api import LLMAPIClient
except ImportError:
    try:
        from llm_api import LLMAPIClient
    except ImportError:
        print("WARNING: LLMAPIClient not found. Will use heuristic classification only.")
        LLMAPIClient = None


class ADOWorkItemExtractor:
    """Extract and analyze ADO work items for workback planning training"""
    
    def __init__(self, organization_url: str, pat_token: str, project: str, use_llm: bool = True):
        """
        Initialize ADO connection
        
        Args:
            organization_url: Azure DevOps organization URL (e.g., https://dev.azure.com/your-org)
            pat_token: Personal Access Token with Work Items (Read) permission
            project: Project name to extract from
            use_llm: Whether to use LLM for intelligent classification (default: True)
        """
        self.organization_url = organization_url
        self.project = project
        self.use_llm = use_llm and LLMAPIClient is not None
        
        # Initialize LLM client if enabled
        if self.use_llm:
            self.llm_client = LLMAPIClient()
            print("🤖 LLM-powered classification enabled (gpt-oss:20b)")
        else:
            self.llm_client = None
            print("📊 Using heuristic classification only")
        
        # Authenticate
        credentials = BasicAuthentication('', pat_token)
        self.connection = Connection(base_url=organization_url, creds=credentials)
        
        # Get work item tracking client
        self.wit_client: WorkItemTrackingClient = self.connection.clients.get_work_item_tracking_client()
        
        print(f"✅ Connected to Azure DevOps: {organization_url}")
        print(f"📁 Project: {project}")
    
    def extract_completed_work_items(
        self,
        months_back: int = 6,
        min_story_points: int = 0,
        max_story_points: int = 13,
        work_item_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract completed work items from last N months
        
        Args:
            months_back: How many months back to look
            min_story_points: Minimum story points (for filtering)
            max_story_points: Maximum story points (for Q2 filtering)
            work_item_types: Work item types to extract (default: Feature, User Story, Task)
        
        Returns:
            List of work items with metadata
        """
        if work_item_types is None:
            work_item_types = ['Feature', 'User Story', 'Task']
        
        # Calculate date threshold
        date_threshold = (datetime.now() - timedelta(days=months_back * 30)).strftime('%Y-%m-%d')
        
        # Build WIQL query
        wiql_query = f"""
        SELECT [System.Id], [System.Title], [System.State], 
               [System.WorkItemType], [System.AssignedTo],
               [Microsoft.VSTS.Scheduling.StoryPoints],
               [Microsoft.VSTS.Scheduling.OriginalEstimate],
               [Microsoft.VSTS.Scheduling.CompletedWork],
               [System.CreatedDate], [System.ChangedDate],
               [Microsoft.VSTS.Common.ClosedDate],
               [Microsoft.VSTS.Common.Priority],
               [Microsoft.VSTS.Common.BusinessValue],
               [System.Description],
               [System.Tags]
        FROM WorkItems
        WHERE [System.TeamProject] = '{self.project}'
          AND [System.State] = 'Closed'
          AND [System.WorkItemType] IN ({', '.join(f"'{t}'" for t in work_item_types)})
          AND [Microsoft.VSTS.Common.ClosedDate] >= '{date_threshold}'
        ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC
        """
        
        print(f"\n🔍 Querying work items closed since {date_threshold}...")
        print(f"   Looking for: {', '.join(work_item_types)}")
        
        # Execute query (simplified - no team_context needed)
        from azure.devops.v7_0.work_item_tracking.models import Wiql
        
        wiql_object = Wiql(query=wiql_query)
        query_result = self.wit_client.query_by_wiql(wiql_object).work_items
        
        if not query_result:
            print("⚠️  No work items found matching criteria")
            return []
        
        print(f"📊 Found {len(query_result)} work items")
        
        # Fetch full work items with relations
        work_items = []
        for idx, item_ref in enumerate(query_result, 1):
            print(f"   Fetching {idx}/{len(query_result)}: ID {item_ref.id}...", end='\r')
            
            item = self.wit_client.get_work_item(
                item_ref.id,
                expand='Relations'  # Include links/dependencies
            )
            
            # Filter by story points if applicable
            story_points = item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints')
            if story_points is not None:
                if story_points < min_story_points or story_points > max_story_points:
                    continue
            
            work_items.append(item)
        
        print(f"\n✅ Extracted {len(work_items)} work items (after filtering)")
        return work_items
    
    def llm_batch_classify(self, work_items: List[Any]) -> Dict[int, Dict[str, str]]:
        """
        EFFICIENT: Batch classify multiple work items with single LLM conversation.
        Uses one system prompt and processes all items in sequence.
        
        Args:
            work_items: List of ADO work item objects
            
        Returns:
            Dict mapping work_item.id -> {'complexity': str, 'value': str}
        """
        if not self.llm_client or not work_items:
            return {}
        
        import re
        import ollama
        
        print(f"\n🤖 Batch LLM classification for {len(work_items)} items...")
        
        # System prompt (sent once)
        system_prompt = """You are an expert at classifying software work items by complexity and business value.

COMPLEXITY Levels:
- Q2_Low_Complexity: Single team, clear scope, 1-5 story points, <5 dependencies, routine work
- Q3_Medium_Complexity: 1-2 teams, moderate scope, 5-13 story points, 5-15 dependencies, some uncertainty  
- Q1_High_Complexity: Multiple teams, broad scope, 13+ story points, 15+ dependencies, high uncertainty

VALUE Levels:
- High_Value: Customer-facing, revenue impact, strategic priority, P0/P1
- Medium_Value: Internal improvements, moderate impact, P2
- Low_Value: Routine tasks, minor improvements, P3+

For each work item, respond with ONLY this format:
COMPLEXITY: [Q2_Low_Complexity|Q3_Medium_Complexity|Q1_High_Complexity]
VALUE: [High_Value|Medium_Value|Low_Value]"""

        classifications = {}
        
        # Process items in conversation context
        try:
            # Start chat with system context
            messages = [{"role": "system", "content": system_prompt}]
            
            for idx, item in enumerate(work_items, 1):
                # Prepare work item info
                title = item.fields.get('System.Title', '')
                description = item.fields.get('System.Description', '')
                work_type = item.fields.get('System.WorkItemType', '')
                story_points = item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints', 'N/A')
                priority = item.fields.get('Microsoft.VSTS.Common.Priority', '')
                tags = item.fields.get('System.Tags', '')
                
                # Get dependencies
                dep_count = 0
                if hasattr(item, 'relations') and item.relations:
                    dep_count = len([r for r in item.relations if 'System.Link' in r.rel or 'Dependency' in r.rel])
                
                # Clean description
                desc_text = re.sub('<[^<]+?>', '', description) if description else ''
                desc_text = desc_text[:800]  # Limit for token efficiency
                
                # User message for this item
                user_message = f"""Work Item {idx}/{len(work_items)}:
Title: {title}
Type: {work_type}
Story Points: {story_points}
Priority: {priority}
Dependencies: {dep_count}
Tags: {tags}
Description: {desc_text}

Classify this item."""
                
                messages.append({"role": "user", "content": user_message})
                
                # Get LLM response
                try:
                    response = self.llm_client.ollama_client.chat(
                        model="gpt-oss:20b",
                        messages=messages,
                        options={"temperature": 0.1}  # Low temp for consistency
                    )
                    
                    assistant_message = response['message']['content']
                    messages.append({"role": "assistant", "content": assistant_message})
                    
                    # Parse response
                    complexity = "Q2_Low_Complexity"  # Default
                    value = "Low_Value"  # Default
                    
                    if "Q3_Medium_Complexity" in assistant_message:
                        complexity = "Q3_Medium_Complexity"
                    elif "Q1_High_Complexity" in assistant_message:
                        complexity = "Q1_High_Complexity"
                    
                    if "High_Value" in assistant_message:
                        value = "High_Value"
                    elif "Medium_Value" in assistant_message:
                        value = "Medium_Value"
                    
                    classifications[item.id] = {
                        'complexity': complexity,
                        'value': value
                    }
                    
                    print(f"   {idx}/{len(work_items)}: ID {item.id} → {complexity}, {value}")
                    
                except Exception as e:
                    print(f"   ⚠️  Failed for ID {item.id}: {e}")
                    # Use heuristic fallback
                    classifications[item.id] = {
                        'complexity': self.classify_complexity(item),
                        'value': self.assess_value(item)
                    }
        
        except Exception as e:
            print(f"❌ Batch classification failed: {e}")
            # Return empty dict, caller will use heuristics
            return {}
        
        print(f"✅ Batch classified {len(classifications)}/{len(work_items)} items")
        return classifications
    
    def llm_classify_complexity(self, work_item: Any) -> str:
        """
        Use LLM to classify work item complexity intelligently
        NOTE: This is the per-item method. Use llm_batch_classify() for efficiency.
        
        Args:
            work_item: ADO work item object
            
        Returns:
            Complexity classification: Q2_Low_Complexity, Q3_Medium_Complexity, Q1_High_Complexity
        """
        if not self.llm_client:
            return self.classify_complexity(work_item)
        
        # Extract context for LLM
        title = work_item.fields.get('System.Title', '')
        description = work_item.fields.get('System.Description', '')
        work_type = work_item.fields.get('System.WorkItemType', '')
        story_points = work_item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints', 'N/A')
        tags = work_item.fields.get('System.Tags', '')
        
        # Get dependency count
        dep_count = 0
        if hasattr(work_item, 'relations') and work_item.relations:
            dep_count = len([r for r in work_item.relations if 'System.Link' in r.rel or 'Dependency' in r.rel])
        
        # Strip HTML from description
        import re
        description_text = re.sub('<[^<]+?>', '', description) if description else ''
        description_text = description_text[:1000]  # Limit to 1000 chars
        
        prompt = f"""Analyze this work item and classify its complexity as Q2 (Low), Q3 (Medium), or Q1 (High).

Work Item: {title}
Type: {work_type}
Story Points: {story_points}
Dependencies: {dep_count}
Tags: {tags}

Description:
{description_text}

Classification criteria:
- Q2 (Low Complexity): Single team, clear scope, 1-5 story points, <5 dependencies, routine work
- Q3 (Medium Complexity): 1-2 teams, moderate scope, 5-13 story points, 5-15 dependencies, some uncertainty
- Q1 (High Complexity): Multiple teams, broad scope, 13+ story points, 15+ dependencies, high uncertainty

Respond with ONLY one of: Q2_Low_Complexity, Q3_Medium_Complexity, Q1_High_Complexity"""

        try:
            response = self.llm_client.query_llm(
                prompt=prompt,
                provider="ollama",
                model="gpt-oss:20b"
            )
            
            # Extract classification from response
            response_text = response.strip()
            if "Q2_Low_Complexity" in response_text:
                return "Q2_Low_Complexity"
            elif "Q3_Medium_Complexity" in response_text:
                return "Q3_Medium_Complexity"
            elif "Q1_High_Complexity" in response_text:
                return "Q1_High_Complexity"
            else:
                # Fallback to heuristic
                print(f"⚠️  LLM response unclear for ID {work_item.id}: {response_text[:100]}")
                return self.classify_complexity(work_item)
                
        except Exception as e:
            print(f"⚠️  LLM classification failed for ID {work_item.id}: {e}")
            return self.classify_complexity(work_item)
    
    def llm_assess_value(self, work_item: Any) -> str:
        """
        Use LLM to assess work item business value intelligently
        
        Args:
            work_item: ADO work item object
            
        Returns:
            Value classification: High_Value, Medium_Value, or Low_Value
        """
        if not self.llm_client:
            return self.assess_value(work_item)
        
        # Extract context for LLM
        title = work_item.fields.get('System.Title', '')
        description = work_item.fields.get('System.Description', '')
        work_type = work_item.fields.get('System.WorkItemType', '')
        priority = work_item.fields.get('Microsoft.VSTS.Common.Priority', 'N/A')
        tags = work_item.fields.get('System.Tags', '')
        assigned_to = work_item.fields.get('System.AssignedTo', {})
        if isinstance(assigned_to, dict):
            assigned_to = assigned_to.get('displayName', 'N/A')
        
        # Strip HTML from description
        import re
        description_text = re.sub('<[^<]+?>', '', description) if description else ''
        description_text = description_text[:1000]  # Limit to 1000 chars
        
        prompt = f"""Analyze this work item and assess its business value as High, Medium, or Low.

Work Item: {title}
Type: {work_type}
Priority: {priority}
Tags: {tags}
Assigned To: {assigned_to}

Description:
{description_text}

Value assessment criteria:
- High_Value: Customer-committed, roadmap feature, executive visibility, revenue impact, OKR alignment
- Medium_Value: Important but not critical, team-level priority, quality improvement, technical debt
- Low_Value: Administrative, documentation, internal process, low impact

Respond with ONLY one of: High_Value, Medium_Value, Low_Value"""

        try:
            response = self.llm_client.query_llm(
                prompt=prompt,
                provider="ollama",
                model="gpt-oss:20b"
            )
            
            # Extract classification from response
            response_text = response.strip()
            if "High_Value" in response_text:
                return "High_Value"
            elif "Medium_Value" in response_text:
                return "Medium_Value"
            elif "Low_Value" in response_text:
                return "Low_Value"
            else:
                # Fallback to heuristic
                print(f"⚠️  LLM response unclear for ID {work_item.id}: {response_text[:100]}")
                return self.assess_value(work_item)
                
        except Exception as e:
            print(f"⚠️  LLM value assessment failed for ID {work_item.id}: {e}")
            return self.assess_value(work_item)
    
    def llm_analyze_outcome(self, work_item: Any) -> Dict[str, Any]:
        """
        Use LLM to analyze work item outcome and extract success signals
        
        Args:
            work_item: ADO work item object
            
        Returns:
            Dict with outcome analysis (success factors, failure signals, lessons learned)
        """
        if not self.llm_client:
            return self._heuristic_outcome_analysis(work_item)
        
        title = work_item.fields.get('System.Title', '')
        description = work_item.fields.get('System.Description', '')
        state = work_item.fields.get('System.State', '')
        created = work_item.fields.get('System.CreatedDate', '')
        closed = work_item.fields.get('Microsoft.VSTS.Common.ClosedDate', '')
        
        # Calculate duration
        from dateutil import parser as date_parser
        duration_days = None
        if created and closed:
            try:
                if isinstance(created, str):
                    created = date_parser.parse(created)
                if isinstance(closed, str):
                    closed = date_parser.parse(closed)
                duration_days = (closed - created).days
            except:
                pass
        
        # Strip HTML
        import re
        description_text = re.sub('<[^<]+?>', '', description) if description else ''
        description_text = description_text[:1500]
        
        prompt = f"""Analyze this completed work item and extract outcome insights.

Work Item: {title}
State: {state}
Duration: {duration_days} days
Description:
{description_text}

Analyze:
1. SUCCESS SIGNALS: What indicates this was successful? (delivery, quality, timeline)
2. FAILURE SIGNALS: What indicates problems or delays? (blockers, scope creep, rework)
3. KEY LEARNINGS: What lessons can be extracted for future planning?

Respond in JSON format:
{{
  "outcome_assessment": "success" | "partial_success" | "delayed" | "blocked",
  "success_signals": ["signal1", "signal2"],
  "failure_signals": ["signal1", "signal2"],
  "key_learnings": ["learning1", "learning2"],
  "confidence": 0.0-1.0
}}"""

        try:
            response = self.llm_client.query_llm(
                prompt=prompt,
                provider="ollama",
                model="gpt-oss:20b"
            )
            
            # Parse JSON response
            import json
            import re
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                response = json_match.group(1)
            else:
                # Try to find JSON object
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    response = json_match.group(0)
            
            outcome_data = json.loads(response)
            return outcome_data
            
        except Exception as e:
            print(f"⚠️  LLM outcome analysis failed for ID {work_item.id}: {e}")
            return self._heuristic_outcome_analysis(work_item)
    
    def _heuristic_outcome_analysis(self, work_item: Any) -> Dict[str, Any]:
        """Fallback heuristic outcome analysis"""
        return {
            "outcome_assessment": "partial_success",
            "success_signals": ["work_item_closed"],
            "failure_signals": [],
            "key_learnings": [],
            "confidence": 0.5
        }
    
    def llm_assess_risks(self, work_item: Any) -> Dict[str, Any]:
        """
        Use LLM to identify risks and blockers from work item context
        
        Args:
            work_item: ADO work item object
            
        Returns:
            Dict with risk assessment (risk_level, identified_risks, mitigation_suggestions)
        """
        if not self.llm_client:
            return self._heuristic_risk_assessment(work_item)
        
        title = work_item.fields.get('System.Title', '')
        description = work_item.fields.get('System.Description', '')
        work_type = work_item.fields.get('System.WorkItemType', '')
        tags = work_item.fields.get('System.Tags', '')
        
        # Get dependencies
        dep_count = 0
        if hasattr(work_item, 'relations') and work_item.relations:
            dep_count = len([r for r in work_item.relations if 'System.Link' in r.rel or 'Dependency' in r.rel])
        
        # Strip HTML
        import re
        description_text = re.sub('<[^<]+?>', '', description) if description else ''
        description_text = description_text[:1500]
        
        prompt = f"""Analyze this work item and identify potential risks and blockers.

Work Item: {title}
Type: {work_type}
Dependencies: {dep_count}
Tags: {tags}

Description:
{description_text}

Identify:
1. DEPENDENCY RISKS: Issues with dependent teams, services, or deliverables
2. TECHNICAL RISKS: Technical complexity, unknown solutions, integration challenges
3. RESOURCE RISKS: Skill gaps, capacity constraints, availability issues
4. SCOPE RISKS: Unclear requirements, scope creep potential, changing priorities

Respond in JSON format:
{{
  "risk_level": "low" | "medium" | "high",
  "identified_risks": [
    {{"category": "dependency|technical|resource|scope", "description": "...", "severity": "low|medium|high"}}
  ],
  "mitigation_suggestions": ["suggestion1", "suggestion2"],
  "confidence": 0.0-1.0
}}"""

        try:
            response = self.llm_client.query_llm(
                prompt=prompt,
                provider="ollama",
                model="gpt-oss:20b"
            )
            
            # Parse JSON response
            import json
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                response = json_match.group(1)
            else:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    response = json_match.group(0)
            
            risk_data = json.loads(response)
            return risk_data
            
        except Exception as e:
            print(f"⚠️  LLM risk assessment failed for ID {work_item.id}: {e}")
            return self._heuristic_risk_assessment(work_item)
    
    def _heuristic_risk_assessment(self, work_item: Any) -> Dict[str, Any]:
        """Fallback heuristic risk assessment"""
        dep_count = 0
        if hasattr(work_item, 'relations') and work_item.relations:
            dep_count = len([r for r in work_item.relations if 'System.Link' in r.rel])
        
        risk_level = "low"
        if dep_count >= 10:
            risk_level = "high"
        elif dep_count >= 5:
            risk_level = "medium"
        
        return {
            "risk_level": risk_level,
            "identified_risks": [{"category": "dependency", "description": f"{dep_count} dependencies", "severity": risk_level}],
            "mitigation_suggestions": [],
            "confidence": 0.5
        }
    
    def classify_complexity(self, work_item: Any) -> str:
        """
        Classify work item complexity (Q2/Q3/Q1) using heuristics
        
        Based on:
        - Story points
        - Team count (if available)
        - Dependency count
        - Sprint span (duration)
        """
        score = 0
        
        # Story points: 1-3=Low, 5-8=Medium, 13+=High
        story_points = work_item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints', 0)
        if story_points >= 13:
            score += 3
        elif story_points >= 8:
            score += 2
        elif story_points >= 5:
            score += 1
        
        # Dependencies
        if hasattr(work_item, 'relations') and work_item.relations:
            dep_count = sum(1 for rel in work_item.relations 
                          if 'Dependency' in rel.rel)
            if dep_count >= 15:
                score += 3
            elif dep_count >= 8:
                score += 2
            elif dep_count >= 5:
                score += 1
        
        # Duration (created to closed)
        created_date = work_item.fields.get('System.CreatedDate')
        closed_date = work_item.fields.get('Microsoft.VSTS.Common.ClosedDate')
        if created_date and closed_date:
            # Parse dates if they're strings
            from dateutil import parser as date_parser
            if isinstance(created_date, str):
                created_date = date_parser.parse(created_date)
            if isinstance(closed_date, str):
                closed_date = date_parser.parse(closed_date)
            
            duration_days = (closed_date - created_date).days
            if duration_days >= 90:  # ~4 sprints
                score += 3
            elif duration_days >= 30:  # ~2 sprints
                score += 1
        
        # Classify
        if score <= 3:
            return "Q2_Low_Complexity"
        elif score <= 6:
            return "Q3_Medium_Complexity"
        else:
            return "Q1_High_Complexity"
    
    def assess_value(self, work_item: Any) -> str:
        """
        Assess work item value (High/Medium/Low)
        
        Based on:
        - Priority (P0/P1 = high)
        - Business value score
        - Tags (customer-committed, OKR, roadmap)
        """
        value_score = 0
        
        # Priority
        priority = work_item.fields.get('Microsoft.VSTS.Common.Priority')
        if priority in [0, 1]:  # P0 or P1
            value_score += 3
        elif priority == 2:  # P2
            value_score += 2
        
        # Business value
        business_value = work_item.fields.get('Microsoft.VSTS.Common.BusinessValue', 0)
        if business_value >= 50:
            value_score += 2
        
        # Tags
        tags = work_item.fields.get('System.Tags', '').lower()
        high_value_tags = ['customer-committed', 'roadmap', 'okr', 'p0', 'critical']
        if any(tag in tags for tag in high_value_tags):
            value_score += 2
        
        # Classify
        if value_score >= 6:
            return "High_Value"
        elif value_score >= 3:
            return "Medium_Value"
        else:
            return "Low_Value"
    
    def calculate_outcome_labels(self, work_item: Any) -> Dict[str, Any]:
        """
        Calculate outcome labels from work item history
        
        Returns:
            Dictionary with effort_variance, schedule_variance, outcome classification
        """
        original_estimate = work_item.fields.get('Microsoft.VSTS.Scheduling.OriginalEstimate')
        completed_work = work_item.fields.get('Microsoft.VSTS.Scheduling.CompletedWork')
        created_date = work_item.fields.get('System.CreatedDate')
        closed_date = work_item.fields.get('Microsoft.VSTS.Common.ClosedDate')
        
        labels = {
            'work_item_id': work_item.id,
            'effort_variance': None,
            'effort_outcome': 'unknown',
            'schedule_variance_days': None,
            'schedule_outcome': 'unknown',
            'overall_outcome': 'unknown'
        }
        
        # Effort variance
        if original_estimate and completed_work and original_estimate > 0:
            labels['effort_variance'] = completed_work / original_estimate
            if labels['effort_variance'] <= 1.1:
                labels['effort_outcome'] = 'on_budget'
            elif labels['effort_variance'] <= 1.3:
                labels['effort_outcome'] = 'moderately_over'
            else:
                labels['effort_outcome'] = 'significantly_over'
        
        # Schedule variance (simplified - would need target date for accuracy)
        if created_date and closed_date:
            # Parse dates if they're strings
            from dateutil import parser as date_parser
            if isinstance(created_date, str):
                created_date = date_parser.parse(created_date)
            if isinstance(closed_date, str):
                closed_date = date_parser.parse(closed_date)
            
            duration_days = (closed_date - created_date).days
            labels['actual_duration_days'] = duration_days
            
            # Heuristic: Assume 1 story point = 1 day for simple estimation
            story_points = work_item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints')
            if story_points and story_points > 0:
                expected_days = story_points * 2  # Rough estimate
                variance_days = duration_days - expected_days
                labels['schedule_variance_days'] = variance_days
                
                if variance_days <= 0:
                    labels['schedule_outcome'] = 'on_time'
                elif variance_days <= 3:
                    labels['schedule_outcome'] = 'slightly_late'
                elif variance_days <= 7:
                    labels['schedule_outcome'] = 'moderately_late'
                else:
                    labels['schedule_outcome'] = 'significantly_late'
        
        # Overall outcome
        if (labels['effort_outcome'] == 'on_budget' and 
            labels['schedule_outcome'] in ['on_time', 'slightly_late']):
            labels['overall_outcome'] = 'success'
        elif labels['schedule_outcome'] in ['moderately_late', 'significantly_late']:
            labels['overall_outcome'] = 'delayed'
        else:
            labels['overall_outcome'] = 'partial_success'
        
        return labels
    
    def extract_dependencies(self, work_item: Any) -> List[Dict[str, Any]]:
        """Extract predecessor/successor dependencies"""
        dependencies = []
        
        if not hasattr(work_item, 'relations') or not work_item.relations:
            return dependencies
        
        for relation in work_item.relations:
            if 'Dependency-Forward' in relation.rel:
                # This item is predecessor
                successor_id = int(relation.url.split('/')[-1])
                dependencies.append({
                    'type': 'predecessor',
                    'from': work_item.id,
                    'to': successor_id
                })
            elif 'Dependency-Reverse' in relation.rel:
                # This item is successor
                predecessor_id = int(relation.url.split('/')[-1])
                dependencies.append({
                    'type': 'predecessor',
                    'from': predecessor_id,
                    'to': work_item.id
                })
            elif 'Hierarchy-Forward' in relation.rel:
                # Parent-child relationship
                child_id = int(relation.url.split('/')[-1])
                dependencies.append({
                    'type': 'child',
                    'from': work_item.id,
                    'to': child_id
                })
            elif 'Hierarchy-Reverse' in relation.rel:
                # Child-parent relationship
                parent_id = int(relation.url.split('/')[-1])
                dependencies.append({
                    'type': 'parent',
                    'from': work_item.id,
                    'to': parent_id
                })
        
        return dependencies
    
    def build_training_example(self, work_item: Any) -> Dict[str, Any]:
        """
        Build training example from work item
        
        Returns:
            Training example with context, plan, outcome, metadata
        """
        # Use LLM classification if enabled, otherwise fall back to heuristics
        if self.use_llm:
            complexity = self.llm_classify_complexity(work_item)
            value = self.llm_assess_value(work_item)
        else:
            complexity = self.classify_complexity(work_item)
            value = self.assess_value(work_item)
        
        return self._build_training_example_with_classification(
            work_item, complexity, value
        )
    
    def _build_training_example_with_classification(
        self, work_item: Any, complexity: str, value: str
    ) -> Dict[str, Any]:
        """
        Build training example from work item with pre-computed classification.
        Internal method used by batch processing.
        
        Args:
            work_item: ADO work item
            complexity: Pre-computed complexity classification
            value: Pre-computed value classification
            
        Returns:
            Training example with context, plan, outcome, metadata
        """
        outcome = self.calculate_outcome_labels(work_item)
        dependencies = self.extract_dependencies(work_item)
        
        training_example = {
            'training_id': f"ado_{work_item.id}",
            'source': 'azure_devops',
            
            'context': {
                'goal': work_item.fields.get('System.Title', ''),
                'description': work_item.fields.get('System.Description', ''),
                'work_item_type': work_item.fields.get('System.WorkItemType', ''),
                'priority': work_item.fields.get('Microsoft.VSTS.Common.Priority'),
                'business_value': work_item.fields.get('Microsoft.VSTS.Common.BusinessValue'),
                'tags': work_item.fields.get('System.Tags', '').split(';') if work_item.fields.get('System.Tags') else [],
                'assigned_to': work_item.fields.get('System.AssignedTo', {}).get('displayName') if work_item.fields.get('System.AssignedTo') else None
            },
            
            'plan': {
                'task': {
                    'id': work_item.id,
                    'title': work_item.fields.get('System.Title', ''),
                    'estimated_hours': work_item.fields.get('Microsoft.VSTS.Scheduling.OriginalEstimate'),
                    'actual_hours': work_item.fields.get('Microsoft.VSTS.Scheduling.CompletedWork'),
                    'story_points': work_item.fields.get('Microsoft.VSTS.Scheduling.StoryPoints'),
                    'state': work_item.fields.get('System.State', ''),
                    'created_date': work_item.fields.get('System.CreatedDate'),
                    'closed_date': work_item.fields.get('Microsoft.VSTS.Common.ClosedDate')
                },
                'dependencies': dependencies
            },
            
            'outcome': outcome,
            
            'metadata': {
                'project': self.project,
                'work_item_id': work_item.id,
                'work_item_url': f"{self.organization_url}/{self.project}/_workitems/edit/{work_item.id}",
                'complexity': complexity,
                'value': value,
                'extracted_date': datetime.now().isoformat()
            }
        }
        
        return training_example
    
    def extract_and_classify(
        self,
        months_back: int = 6,
        target_complexity: str = "Q2_Low_Complexity",
        target_value: str = "High_Value",
        max_examples: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Extract and filter work items for training
        
        Args:
            months_back: How many months to look back
            target_complexity: Target complexity level (Q2_Low_Complexity for pilot)
            target_value: Target value level (High_Value for pilot)
            max_examples: Maximum examples to extract
        
        Returns:
            List of training examples
        """
        # Extract work items (Q2 story points: 1-13)
        work_items = self.extract_completed_work_items(
            months_back=months_back,
            min_story_points=1,
            max_story_points=13,  # Q2 upper bound
            work_item_types=['Feature', 'User Story', 'Task']
        )
        
        print(f"\n🏗️  Building training examples...")
        
        # OPTIMIZATION: Use batch classification if LLM is enabled
        llm_classifications = {}
        if self.use_llm and work_items:
            llm_classifications = self.llm_batch_classify(work_items)
        
        # Build training examples
        training_examples = []
        complexity_counts = defaultdict(int)
        value_counts = defaultdict(int)
        
        for item in work_items:
            # Use pre-computed batch LLM results if available
            if item.id in llm_classifications:
                complexity = llm_classifications[item.id]['complexity']
                value = llm_classifications[item.id]['value']
            elif self.use_llm:
                # Fallback to per-item LLM (shouldn't happen often)
                complexity = self.llm_classify_complexity(item)
                value = self.llm_assess_value(item)
            else:
                # Use heuristics
                complexity = self.classify_complexity(item)
                value = self.assess_value(item)
            
            # Build example with classification
            example = self._build_training_example_with_classification(
                item, complexity, value
            )
            
            # Filter by target complexity and value
            complexity_match = (target_complexity is None or 
                              example['metadata']['complexity'] == target_complexity)
            value_match = (target_value is None or 
                         example['metadata']['value'] == target_value)
            
            if complexity_match and value_match:
                training_examples.append(example)
                complexity_counts[example['metadata']['complexity']] += 1
                value_counts[example['metadata']['value']] += 1
                
                if len(training_examples) >= max_examples:
                    break
        
        print(f"✅ Built {len(training_examples)} training examples")
        print(f"\n📊 Distribution:")
        print(f"   Complexity: {dict(complexity_counts)}")
        print(f"   Value: {dict(value_counts)}")
        
        return training_examples
    
    def save_to_file(self, training_examples: List[Dict[str, Any]], output_file: str):
        """Save training examples to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(training_examples, f, indent=2, default=str)
        
        print(f"\n💾 Saved {len(training_examples)} examples to: {output_file}")
    
    def generate_statistics(self, training_examples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics about extracted data"""
        stats = {
            'total_examples': len(training_examples),
            'complexity_distribution': defaultdict(int),
            'value_distribution': defaultdict(int),
            'outcome_distribution': defaultdict(int),
            'work_item_types': defaultdict(int),
            'average_story_points': 0,
            'average_effort_variance': 0,
            'data_quality': {
                'has_estimate': 0,
                'has_actual': 0,
                'has_dependencies': 0,
                'has_description': 0
            }
        }
        
        story_points_sum = 0
        story_points_count = 0
        effort_variance_sum = 0
        effort_variance_count = 0
        
        for example in training_examples:
            # Distributions
            stats['complexity_distribution'][example['metadata']['complexity']] += 1
            stats['value_distribution'][example['metadata']['value']] += 1
            stats['outcome_distribution'][example['outcome']['overall_outcome']] += 1
            stats['work_item_types'][example['context']['work_item_type']] += 1
            
            # Averages
            if example['plan']['task']['story_points']:
                story_points_sum += example['plan']['task']['story_points']
                story_points_count += 1
            
            if example['outcome']['effort_variance']:
                effort_variance_sum += example['outcome']['effort_variance']
                effort_variance_count += 1
            
            # Data quality
            if example['plan']['task']['estimated_hours']:
                stats['data_quality']['has_estimate'] += 1
            if example['plan']['task']['actual_hours']:
                stats['data_quality']['has_actual'] += 1
            if example['plan']['dependencies']:
                stats['data_quality']['has_dependencies'] += 1
            if example['context']['description']:
                stats['data_quality']['has_description'] += 1
        
        # Calculate averages
        if story_points_count > 0:
            stats['average_story_points'] = story_points_sum / story_points_count
        if effort_variance_count > 0:
            stats['average_effort_variance'] = effort_variance_sum / effort_variance_count
        
        # Convert to percentages
        total = len(training_examples)
        for key in stats['data_quality']:
            stats['data_quality'][key] = f"{(stats['data_quality'][key] / total * 100):.1f}%"
        
        return dict(stats)


def main():
    parser = argparse.ArgumentParser(
        description='Extract Azure DevOps work items for workback planning training'
    )
    parser.add_argument(
        '--org-url',
        required=True,
        help='Azure DevOps organization URL (e.g., https://dev.azure.com/your-org)'
    )
    parser.add_argument(
        '--pat-token',
        required=True,
        help='Personal Access Token (or use ADO_PAT environment variable)'
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Project name'
    )
    parser.add_argument(
        '--months-back',
        type=int,
        default=6,
        help='How many months back to look (default: 6)'
    )
    parser.add_argument(
        '--max-examples',
        type=int,
        default=50,
        help='Maximum examples to extract (default: 50 for pilot)'
    )
    parser.add_argument(
        '--complexity',
        default='Q2_Low_Complexity',
        choices=['Q2_Low_Complexity', 'Q3_Medium_Complexity', 'Q1_High_Complexity', 'all'],
        help='Target complexity level (default: Q2_Low_Complexity for pilot)'
    )
    parser.add_argument(
        '--value',
        default='High_Value',
        choices=['High_Value', 'Medium_Value', 'Low_Value', 'all'],
        help='Target value level (default: High_Value)'
    )
    parser.add_argument(
        '--output',
        default='ado_workback_training_data.json',
        help='Output JSON file (default: ado_workback_training_data.json)'
    )
    parser.add_argument(
        '--stats-output',
        default='ado_workback_statistics.json',
        help='Statistics output file (default: ado_workback_statistics.json)'
    )
    parser.add_argument(
        '--use-llm',
        action='store_true',
        default=True,
        help='Use LLM (gpt-oss:20b) for intelligent classification (default: True)'
    )
    parser.add_argument(
        '--no-llm',
        action='store_true',
        help='Disable LLM and use heuristic classification only'
    )
    
    args = parser.parse_args()
    
    # Determine LLM usage
    use_llm = args.use_llm and not args.no_llm
    
    # Allow PAT token from environment
    pat_token = args.pat_token
    if pat_token == 'env' or pat_token == '$ADO_PAT':
        pat_token = os.environ.get('ADO_PAT')
        if not pat_token:
            print("ERROR: ADO_PAT environment variable not set")
            exit(1)
    
    print("=" * 80)
    print("Azure DevOps Work Item Extraction for Workback Planning")
    print("=" * 80)
    
    # Initialize extractor
    extractor = ADOWorkItemExtractor(
        organization_url=args.org_url,
        pat_token=pat_token,
        project=args.project,
        use_llm=use_llm
    )
    
    # Extract and classify
    training_examples = extractor.extract_and_classify(
        months_back=args.months_back,
        target_complexity=args.complexity if args.complexity != 'all' else None,
        target_value=args.value if args.value != 'all' else None,
        max_examples=args.max_examples
    )
    
    if not training_examples:
        print("\n⚠️  No training examples matched criteria. Try:")
        print("   - Increasing --months-back")
        print("   - Using --complexity=all or --value=all")
        print("   - Checking if project has closed work items")
        return
    
    # Save to file
    extractor.save_to_file(training_examples, args.output)
    
    # Generate and save statistics
    stats = extractor.generate_statistics(training_examples)
    with open(args.stats_output, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    
    print(f"📊 Saved statistics to: {args.stats_output}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Total Examples: {stats['total_examples']}")
    print(f"Average Story Points: {stats['average_story_points']:.1f}")
    print(f"Average Effort Variance: {stats['average_effort_variance']:.2f}x" if stats['average_effort_variance'] else "N/A")
    print(f"\nComplexity Distribution:")
    for k, v in stats['complexity_distribution'].items():
        print(f"  {k}: {v}")
    print(f"\nValue Distribution:")
    for k, v in stats['value_distribution'].items():
        print(f"  {k}: {v}")
    print(f"\nOutcome Distribution:")
    for k, v in stats['outcome_distribution'].items():
        print(f"  {k}: {v}")
    print(f"\nData Quality:")
    for k, v in stats['data_quality'].items():
        print(f"  {k}: {v}")
    print("=" * 80)
    print("\n✅ Extraction complete!")
    print(f"\n📝 Next steps:")
    print(f"   1. Review extracted data: {args.output}")
    print(f"   2. Send to expert reviewers for correction")
    print(f"   3. Use corrected plans for model training")


if __name__ == '__main__':
    main()
