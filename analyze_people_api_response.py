#!/usr/bin/env python3
"""
Analyze Microsoft Graph People API Response
Helps interpret the results from Graph Explorer testing
"""

import json
from datetime import datetime

def analyze_people_api_response():
    """
    Guide for analyzing the People API response from Graph Explorer
    """
    
    print('🔍 People API Response Analysis Guide')
    print('=' * 60)
    
    print('📋 What to look for in the Graph Explorer response:')
    print()
    
    analysis_checklist = [
        {
            'field': 'personNotes',
            'importance': 'CRITICAL',
            'description': 'This is likely the official People Notes data!',
            'what_to_check': [
                'Does this field exist in person objects?',
                'Does it contain any text/notes?',
                'Is it empty string or null for everyone?',
                'Does the content look like meeting insights?'
            ]
        },
        {
            'field': 'displayName',
            'importance': 'HIGH',
            'description': 'Person identification',
            'what_to_check': [
                'Are these people you actually work with?',
                'Do you recognize names from recent meetings?',
                'Are they sorted by relevance?'
            ]
        },
        {
            'field': 'scoredEmailAddresses',
            'importance': 'MEDIUM',
            'description': 'Communication frequency scoring',
            'what_to_check': [
                'Do relevanceScore values make sense?',
                'Are high scores for people you email often?',
                'Does this correlate with meeting frequency?'
            ]
        },
        {
            'field': 'jobTitle / department',
            'importance': 'MEDIUM',
            'description': 'Professional context',
            'what_to_check': [
                'Does job context match your interactions?',
                'Are these people from relevant departments?'
            ]
        }
    ]
    
    for item in analysis_checklist:
        importance_icon = '🔥' if item['importance'] == 'CRITICAL' else '⚡' if item['importance'] == 'HIGH' else '💡'
        print(f'{importance_icon} {item["field"].upper()} ({item["importance"]}):')
        print(f'   📝 {item["description"]}')
        for check in item['what_to_check']:
            print(f'   ✓ {check}')
        print()
    
    return analysis_checklist

def create_response_template():
    """
    Create a template for pasting Graph Explorer results
    """
    
    print('📋 Response Analysis Template')
    print('=' * 60)
    
    template = '''
# PASTE YOUR GRAPH EXPLORER RESPONSE HERE
# Copy the JSON response from Graph Explorer and analyze it

Example response format to look for:
{
  "value": [
    {
      "id": "person-id",
      "displayName": "John Doe",
      "personNotes": "THIS IS WHAT WE'RE LOOKING FOR!",
      "scoredEmailAddresses": [
        {
          "address": "john@company.com",
          "relevanceScore": 85.0
        }
      ],
      "jobTitle": "Product Manager",
      "department": "Engineering"
    }
  ]
}

KEY QUESTIONS TO ANSWER:
1. Does personNotes field exist? YES/NO
2. Is personNotes populated with data? YES/NO  
3. What does the personNotes content look like?
4. How many people have non-empty personNotes?
5. Does the content look like meeting insights/notes?
'''
    
    print(template)
    
    with open('graph_explorer_response_template.txt', 'w') as f:
        f.write(template)
    
    print('💾 Saved template to: graph_explorer_response_template.txt')

def suggest_additional_tests():
    """
    Suggest additional Graph Explorer tests based on initial results
    """
    
    print('\n🔍 Additional Tests to Try')
    print('=' * 60)
    
    additional_tests = [
        {
            'test': 'Search for specific people',
            'query': 'GET /me/people?$search="person name"',
            'purpose': 'Test if personNotes exist for people you know have notes'
        },
        {
            'test': 'Filter by top relevance',
            'query': 'GET /me/people?$top=5&$select=displayName,personNotes',
            'purpose': 'Focus on most relevant people who likely have notes'
        },
        {
            'test': 'Check insights APIs',
            'query': 'GET /me/insights/shared',
            'purpose': 'Look for meeting-related files and documents'
        },
        {
            'test': 'Try beta People API',
            'query': 'GET /beta/me/people?$select=displayName,personNotes',
            'purpose': 'Beta version might have more complete notes'
        },
        {
            'test': 'Search for notes keyword',
            'query': 'GET /me/people?$search="notes"',
            'purpose': 'Search functionality might reveal note content'
        }
    ]
    
    print('📋 Try these if initial test works:')
    for i, test in enumerate(additional_tests, 1):
        print(f'\n{i}. {test["test"]}:')
        print(f'   🔗 {test["query"]}')
        print(f'   🎯 {test["purpose"]}')

def main():
    """
    Main analysis guide
    """
    
    print('🚀 Microsoft Graph People API Testing Guide')
    print('=' * 70)
    print('📊 Use this while testing in Graph Explorer')
    print()
    
    # Analysis guide
    analyze_people_api_response()
    
    # Response template
    create_response_template()
    
    # Additional tests
    suggest_additional_tests()
    
    print('\n💡 IMMEDIATE ACTION:')
    print('   1. 🔗 Test: GET https://graph.microsoft.com/v1.0/me/people')
    print('   2. 🔍 Look for personNotes field in each person object')
    print('   3. 📋 Use the analysis checklist above')
    print('   4. 🎯 Report back with findings!')
    print()
    print('🏆 If personNotes has data, we found the official People Notes API!')

if __name__ == "__main__":
    main()