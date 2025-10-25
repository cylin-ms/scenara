#!/usr/bin/env python3
"""
Corrected Personal Graph Explorer Tests
Using the proper full URL format from Graph Explorer
"""

def corrected_personal_endpoints():
    """
    List the correct full URL endpoints to test in Graph Explorer
    """
    
    print('🔍 Corrected Personal Graph Explorer Endpoints')
    print('=' * 60)
    print('✅ Using the correct full URL format from Graph Explorer')
    print()
    
    personal_endpoints = [
        {
            'url': 'https://graph.microsoft.com/v1.0/me',
            'purpose': 'Your basic profile information',
            'look_for': 'aboutMe, jobTitle, department, displayName fields'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/profile',
            'purpose': 'Extended profile with potential notes',
            'look_for': 'Any notes, insights, or personal data fields'
        },
        {
            'url': 'https://graph.microsoft.com/beta/me/profile',
            'purpose': 'Beta profile features (newer API)',
            'look_for': 'Enhanced profile data with insights'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/mailboxSettings',
            'purpose': 'Your email settings and preferences',
            'look_for': 'Personal preferences, signatures, settings'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/insights/trending',
            'purpose': 'Documents trending for you personally',
            'look_for': 'Your document interaction patterns'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/insights/shared',
            'purpose': 'Documents shared with you',
            'look_for': 'Your collaboration patterns'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/insights/used',
            'purpose': 'Documents you have used recently',
            'look_for': 'Your document usage patterns'
        },
        {
            'url': 'https://graph.microsoft.com/beta/me/analytics',
            'purpose': 'Personal analytics (beta)',
            'look_for': 'Any analytics or insights about your activity'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/activities',
            'purpose': 'Your personal activities',
            'look_for': 'Activity patterns and insights'
        },
        {
            'url': 'https://graph.microsoft.com/v1.0/me/settings',
            'purpose': 'Your personal settings',
            'look_for': 'User preferences and configuration'
        }
    ]
    
    print('📋 Test these URLs in Graph Explorer (copy/paste into the URL field):')
    print()
    
    for i, endpoint in enumerate(personal_endpoints, 1):
        print(f'{i}. {endpoint["url"]}')
        print(f'   🎯 Purpose: {endpoint["purpose"]}')
        print(f'   👀 Look for: {endpoint["look_for"]}')
        print()
    
    return personal_endpoints

def create_step_by_step_guide():
    """
    Create step-by-step guide for testing in Graph Explorer
    """
    
    print('📋 Step-by-Step Graph Explorer Testing Guide')
    print('=' * 60)
    
    steps = [
        "Make sure you're signed in to Graph Explorer with your Microsoft account",
        "Copy the first URL: https://graph.microsoft.com/v1.0/me",
        "Paste it in the URL field (replacing the current URL)",
        "Click 'Run query' (blue button)",
        "Examine the response for personal data fields",
        "Look for: aboutMe, notes, jobTitle, department, or any insight fields",
        "Try the next URL and repeat",
        "Note any URLs that return interesting personal data"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f'{i}. {step}')
    
    print('\n💡 Key Fields to Look For:')
    key_fields = [
        'aboutMe - Personal description',
        'notes - Any note fields',
        'skills - Your skills',
        'interests - Your interests', 
        'responsibilities - Your responsibilities',
        'insights - Any insight data',
        'personNotes - Specific people notes field'
    ]
    
    for field in key_fields:
        print(f'   • {field}')

def main():
    """
    Main function with corrected endpoints
    """
    
    print('🔧 Corrected Graph Explorer Personal Data Testing')
    print('=' * 70)
    print('✅ Using proper full URL format from Graph Explorer')
    print('🎯 Focus: YOUR personal data only')
    print()
    
    # Show corrected endpoints
    endpoints = corrected_personal_endpoints()
    
    # Step-by-step guide
    create_step_by_step_guide()
    
    print('\n🚀 START HERE:')
    print('   1. Copy this URL: https://graph.microsoft.com/v1.0/me')
    print('   2. Paste it in Graph Explorer URL field')
    print('   3. Click "Run query"')
    print('   4. Check the response for personal insights')
    print()
    print('💡 This will show YOUR profile data that might contain Me Notes!')

if __name__ == "__main__":
    main()