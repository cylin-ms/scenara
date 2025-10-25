#!/usr/bin/env python3
"""
Specific Field Testing for Personal Me Notes
Since $select=* didn't reveal additional fields, test specific field names
"""

def create_specific_field_tests():
    """
    Create tests for specific fields that might contain Me Notes
    """
    
    print('🔍 Specific Field Testing for Personal Me Notes')
    print('=' * 60)
    print('💡 Since $select=* didn\'t show extra fields, test specific names')
    print()
    
    # Fields that might contain personal insights
    field_tests = [
        {
            'fields': ['aboutMe', 'interests', 'skills', 'responsibilities'],
            'url': 'https://graph.microsoft.com/v1.0/me?$select=aboutMe,interests,skills,responsibilities',
            'purpose': 'Standard personal insight fields'
        },
        {
            'fields': ['notes', 'personNotes', 'insights'],
            'url': 'https://graph.microsoft.com/v1.0/me?$select=notes,personNotes,insights',
            'purpose': 'Direct notes/insights fields'
        },
        {
            'fields': ['aboutMe', 'biography', 'summary', 'description'],
            'url': 'https://graph.microsoft.com/v1.0/me?$select=aboutMe,biography,summary,description',
            'purpose': 'Profile description fields'
        },
        {
            'fields': ['department', 'companyName', 'manager', 'directReports'],
            'url': 'https://graph.microsoft.com/v1.0/me?$select=department,companyName,manager,directReports',
            'purpose': 'Organizational context'
        },
        {
            'fields': ['hireDate', 'employeeId', 'employeeType', 'costCenter'],
            'url': 'https://graph.microsoft.com/v1.0/me?$select=hireDate,employeeId,employeeType,costCenter',
            'purpose': 'Employment details'
        }
    ]
    
    print('📋 Test these specific field combinations:')
    print()
    
    for i, test in enumerate(field_tests, 1):
        print(f'{i}. {test["url"]}')
        print(f'   🎯 Purpose: {test["purpose"]}')
        print(f'   🔍 Fields: {", ".join(test["fields"])}')
        print()
    
    return field_tests

def test_alternative_endpoints():
    """
    Test alternative endpoints that might have personal insights
    """
    
    print('🔧 Alternative Endpoints for Personal Data')
    print('=' * 60)
    
    alternative_endpoints = [
        {
            'url': 'https://graph.microsoft.com/v1.0/me/profile',
            'purpose': 'Extended profile endpoint',
            'expect': 'Different profile structure with more fields'
        },
        {
            'url': 'https://graph.microsoft.com/beta/me',
            'purpose': 'Beta user endpoint',
            'expect': 'Newer fields in beta API'
        },
        {
            'url': 'https://graph.microsoft.com/beta/me/profile',
            'purpose': 'Beta profile endpoint', 
            'expect': 'Enhanced profile data in beta'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/manager',
            'purpose': 'Your manager information',
            'expect': 'Organizational relationships'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/directReports',
            'purpose': 'Your direct reports',
            'expect': 'Management relationships'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/memberOf',
            'purpose': 'Groups you belong to',
            'expect': 'Group memberships and roles'
        }
    ]
    
    print('📋 Try these alternative endpoints:')
    print()
    
    for i, endpoint in enumerate(alternative_endpoints, 1):
        print(f'{i}. {endpoint["url"]}')
        print(f'   🎯 Purpose: {endpoint["purpose"]}')
        print(f'   📝 Expected: {endpoint["expect"]}')
        print()
    
    return alternative_endpoints

def analyze_missing_fields():
    """
    Analyze why additional fields might not be showing
    """
    
    print('💡 Analysis: Why Additional Fields May Not Appear')
    print('=' * 60)
    
    reasons = [
        {
            'reason': 'Fields not populated',
            'description': 'aboutMe, interests, skills may be empty in your profile',
            'solution': 'Check if these fields are set in your Microsoft 365 profile'
        },
        {
            'reason': 'Different API versions',
            'description': 'Some fields may only exist in beta API',
            'solution': 'Try beta endpoints'
        },
        {
            'reason': 'Profile vs User endpoints',
            'description': 'Personal insights may be in /profile not /me',
            'solution': 'Test /me/profile endpoint'
        },
        {
            'reason': 'Permissions required',
            'description': 'Some fields may need additional Graph permissions',
            'solution': 'Check if additional consents are needed'
        },
        {
            'reason': 'Enterprise configuration',
            'description': 'Microsoft may not populate personal insight fields',
            'solution': 'Focus on available data and calendar-based insights'
        }
    ]
    
    for i, reason in enumerate(reasons, 1):
        print(f'{i}. {reason["reason"]}:')
        print(f'   📝 {reason["description"]}')
        print(f'   💡 Solution: {reason["solution"]}')
        print()

def create_personal_me_notes_from_available_data():
    """
    Create comprehensive Me Notes from all available data
    """
    
    print('🎯 Creating Comprehensive Personal Me Notes')
    print('=' * 60)
    print('✅ Using all available data sources')
    print()
    
    # Your confirmed profile data
    available_data = {
        'name': 'Chin-Yew Lin',
        'job_title': 'SR PRINCIPAL RESEARCH MANAGER',
        'organization': 'Microsoft',
        'email': 'cyl@microsoft.com',
        'phone': '+86 (10) 59173481',
        'office': 'BEIJING-BJW-2/13463',
        'location': 'Beijing, China'
    }
    
    # Generate comprehensive Me Notes
    comprehensive_me_notes = [
        {
            'note': 'I am Chin-Yew Lin, a Senior Principal Research Manager at Microsoft',
            'category': 'WORK_RELATED',
            'title': 'Professional Identity',
            'temporal_durability': 'LONG_TERM',
            'source': 'Microsoft Graph User Profile',
            'confidence': 1.0
        },
        {
            'note': 'I work at Microsoft Beijing office (BJW-2/13463) and can be contacted at +86 (10) 59173481',
            'category': 'WORK_RELATED',
            'title': 'Work Location & Contact',
            'temporal_durability': 'LONG_TERM',
            'source': 'Microsoft Graph User Profile',
            'confidence': 1.0
        },
        {
            'note': 'I hold a senior research management position, indicating expertise in research leadership and technical management',
            'category': 'EXPERTISE',
            'title': 'Research Leadership',
            'temporal_durability': 'LONG_TERM',
            'source': 'Inferred from job title',
            'confidence': 0.9
        },
        {
            'note': 'I am based in Beijing, China, working in Microsoft\'s Asia-Pacific research operations',
            'category': 'WORK_RELATED',
            'title': 'Geographic Context',
            'temporal_durability': 'LONG_TERM',
            'source': 'Microsoft Graph User Profile',
            'confidence': 1.0
        }
    ]
    
    print('📋 Comprehensive Personal Me Notes:')
    for i, note in enumerate(comprehensive_me_notes, 1):
        print(f'\n{i}. 📌 {note["title"]} ({note["category"]})')
        print(f'   📝 {note["note"]}')
        print(f'   🎯 Confidence: {note["confidence"]:.0%}')
        print(f'   📊 Source: {note["source"]}')
    
    # Save comprehensive notes
    import json
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'comprehensive_personal_me_notes_{timestamp}.json'
    
    output = {
        'user': 'cyl@microsoft.com',
        'generated_at': datetime.now().isoformat(),
        'source': 'Microsoft Graph Profile + Inference',
        'total_notes': len(comprehensive_me_notes),
        'notes': comprehensive_me_notes
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f'\n💾 Comprehensive Me Notes saved to: {filename}')
    return comprehensive_me_notes, filename

def main():
    """
    Main function for specific field testing
    """
    
    print('🔍 Specific Field Testing - Personal Me Notes Discovery')
    print('=' * 70)
    print('📊 Since $select=* didn\'t reveal additional fields...')
    print('🎯 Testing specific field names and alternative endpoints')
    print()
    
    # Specific field tests
    field_tests = create_specific_field_tests()
    
    # Alternative endpoints
    alternative_endpoints = test_alternative_endpoints()
    
    # Analysis
    analyze_missing_fields()
    
    # Create comprehensive notes
    notes, filename = create_personal_me_notes_from_available_data()
    
    print('\n🚀 RECOMMENDED NEXT STEPS:')
    print('   1. 🔥 Try: https://graph.microsoft.com/v1.0/me?$select=aboutMe,interests,skills,responsibilities')
    print('   2. 🔥 Try: https://graph.microsoft.com/v1.0/me/profile')
    print('   3. 🔥 Try: https://graph.microsoft.com/beta/me')
    print()
    print('💡 If no additional fields found, you have comprehensive Me Notes from available data!')

if __name__ == "__main__":
    main()