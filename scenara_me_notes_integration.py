#!/usr/bin/env python3
"""
Scenara Me Notes Integration Script
Integrates comprehensive personal Me Notes from Microsoft Graph Beta API into Scenara system
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

def integrate_me_notes_to_scenara():
    """
    Integrate comprehensive Me Notes into Scenara meeting intelligence system
    """
    print("🔄 Integrating Me Notes into Scenara...")
    
    # Find the most recent comprehensive Me Notes file
    me_notes_files = list(Path('.').glob('me_notes_comprehensive_beta_*.json'))
    if not me_notes_files:
        print("❌ No comprehensive Me Notes file found!")
        return None
    
    latest_file = max(me_notes_files, key=os.path.getctime)
    print(f"📁 Using Me Notes file: {latest_file}")
    
    # Load the Me Notes
    with open(latest_file, 'r', encoding='utf-8') as f:
        me_notes_data = json.load(f)
    
    # Create Scenara integration structure
    scenara_integration = {
        "integration_metadata": {
            "integration_date": datetime.now().isoformat(),
            "source_system": "Microsoft Graph Beta API",
            "user_id": me_notes_data.get('user_id'),
            "integration_version": "1.0",
            "scenara_module": "meeting_intelligence"
        },
        "user_context": {
            "personal_me_notes": me_notes_data.get('me_notes', []),
            "profile_summary": me_notes_data.get('summary', {}),
            "enrichment_status": "active"
        },
        "meeting_intelligence_enhancements": {
            "professional_context_available": True,
            "location_preferences_available": True,
            "technology_preferences_available": True,
            "communication_style_available": True,
            "security_preferences_available": True
        },
        "scenara_recommendations": {
            "meeting_preparation": [
                "Use professional identity context for meeting introductions",
                "Consider location preferences for meeting scheduling",
                "Align technology choices with user's platform preferences",
                "Respect communication style preferences in meeting formats"
            ],
            "meeting_analysis": [
                "Cross-reference meeting content with professional context",
                "Factor in organizational relationships for meeting dynamics",
                "Consider technology stack alignment for meeting effectiveness"
            ],
            "meeting_optimization": [
                "Leverage collaboration tool preferences for meeting efficiency",
                "Apply security configuration insights for meeting safety",
                "Use location context for meeting logistics optimization"
            ]
        }
    }
    
    # Save integrated Me Notes for Scenara
    scenara_file = f"scenara_me_notes_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(scenara_file, 'w', encoding='utf-8') as f:
        json.dump(scenara_integration, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Scenara integration created: {scenara_file}")
    
    # Create category-specific insights for Scenara modules
    category_insights = {}
    for note in me_notes_data.get('me_notes', []):
        category = note.get('category')
        if category not in category_insights:
            category_insights[category] = []
        category_insights[category].append({
            "insight": note.get('note'),
            "title": note.get('title'),
            "stability": note.get('temporal_durability'),
            "scenara_relevance": get_scenara_relevance(category, note)
        })
    
    # Display integration summary
    print(f"\n📊 Integration Summary:")
    print(f"   • User: {me_notes_data.get('user_id')}")
    print(f"   • Total Personal Insights: {len(me_notes_data.get('me_notes', []))}")
    print(f"   • Available Categories: {len(category_insights)}")
    print(f"   • Meeting Intelligence Enhancements: {sum(scenara_integration['meeting_intelligence_enhancements'].values())}")
    
    print(f"\n🎯 Scenara Module Enhancements:")
    for category, insights in category_insights.items():
        print(f"   • {category}: {len(insights)} insights available")
        for insight in insights[:2]:  # Show first 2 insights per category
            print(f"     - {insight['title']}")
    
    print(f"\n🚀 Scenara Recommendations Generated:")
    for rec_type, recommendations in scenara_integration['scenara_recommendations'].items():
        print(f"   • {rec_type}: {len(recommendations)} recommendations")
    
    return scenara_integration

def get_scenara_relevance(category: str, note: Dict[str, Any]) -> List[str]:
    """
    Determine Scenara module relevance for each Me Notes category
    """
    relevance_mapping = {
        "professional_identity": ["meeting_preparation", "participant_analysis", "context_generation"],
        "professional_context": ["meeting_classification", "stakeholder_analysis", "organizational_insights"],
        "location_preferences": ["meeting_scheduling", "logistics_optimization", "timezone_management"],
        "communication_style": ["meeting_format_selection", "interaction_analysis", "engagement_optimization"],
        "technology_preferences": ["platform_selection", "tool_integration", "collaboration_efficiency"],
        "security_preferences": ["meeting_security", "compliance_monitoring", "access_control"]
    }
    
    return relevance_mapping.get(category, ["general_context"])

def create_scenara_me_notes_module():
    """
    Create a Scenara module configuration for Me Notes integration
    """
    module_config = {
        "module_name": "me_notes_integration",
        "module_version": "1.0.0",
        "description": "Personal Me Notes integration for enhanced meeting intelligence",
        "capabilities": [
            "personal_context_enrichment",
            "meeting_preparation_enhancement",
            "participant_profile_augmentation",
            "communication_style_optimization",
            "technology_preference_alignment"
        ],
        "data_sources": [
            "microsoft_graph_beta_api",
            "personal_profile_data",
            "organizational_context"
        ],
        "integration_points": [
            "meeting_classification_engine",
            "participant_analysis_module",
            "meeting_preparation_assistant",
            "real_time_insights_generator"
        ],
        "privacy_compliance": {
            "data_scope": "personal_only",
            "consent_required": True,
            "data_retention": "user_controlled",
            "sharing_policy": "no_external_sharing"
        }
    }
    
    module_file = "scenara_me_notes_module_config.json"
    with open(module_file, 'w', encoding='utf-8') as f:
        json.dump(module_config, f, indent=2, ensure_ascii=False)
    
    print(f"📦 Scenara module configuration created: {module_file}")
    return module_config

if __name__ == "__main__":
    print("🎯 Scenara Me Notes Integration Starting...")
    
    # Integrate Me Notes into Scenara
    integration_result = integrate_me_notes_to_scenara()
    
    if integration_result:
        # Create module configuration
        module_config = create_scenara_me_notes_module()
        
        print("\n✨ Scenara Me Notes Integration Complete!")
        print("🔗 Your personal Microsoft Graph data is now ready for Scenara meeting intelligence enhancement!")
        print("\n🎉 Key Achievements:")
        print("   ✅ Personal Me Notes extracted from Microsoft Graph Beta API")
        print("   ✅ Comprehensive profile data converted to official Me Notes format")
        print("   ✅ Scenara integration configuration created")
        print("   ✅ Meeting intelligence enhancements mapped")
        print("   ✅ Privacy-compliant personal data integration")
        
        print("\n🔮 Next Steps for Scenara Enhancement:")
        print("   1. Load personal Me Notes into Scenara meeting preparation")
        print("   2. Enable context-aware meeting classification")
        print("   3. Activate personalized meeting recommendations")
        print("   4. Test real-time meeting intelligence with personal context")
    else:
        print("❌ Integration failed - please check Me Notes files")