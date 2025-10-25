#!/usr/bin/env python3
"""
Comprehensive Me Notes Generator from Microsoft Graph Beta API Data
Creates detailed personal Me Notes using the rich data available from the beta endpoint
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

def extract_personal_insights_from_beta(beta_profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract comprehensive personal insights from Microsoft Graph beta API profile data
    
    Args:
        beta_profile_data: Complete beta API response data
        
    Returns:
        List of Me Notes in official format
    """
    me_notes = []
    
    # Basic Professional Identity
    professional_note = {
        "note": f"I am {beta_profile_data.get('displayName', 'Unknown')} ({beta_profile_data.get('givenName', '')} {beta_profile_data.get('surname', '')}), working as {beta_profile_data.get('jobTitle', 'Unknown Role')} at {beta_profile_data.get('companyName', 'Unknown Company')}",
        "category": "professional_identity",
        "title": "Current Professional Role",
        "temporal_durability": "stable"
    }
    me_notes.append(professional_note)
    
    # Department and Organizational Context
    if beta_profile_data.get('department'):
        dept_note = {
            "note": f"I work in the {beta_profile_data['department']} department, with employee ID {beta_profile_data.get('employeeId', 'N/A')}",
            "category": "professional_context",
            "title": "Organizational Position",
            "temporal_durability": "stable"
        }
        me_notes.append(dept_note)
    
    # Geographic and Office Location
    location_parts = []
    if beta_profile_data.get('city'):
        location_parts.append(beta_profile_data['city'])
    if beta_profile_data.get('officeLocation'):
        location_parts.append(f"office location {beta_profile_data['officeLocation']}")
    
    if location_parts:
        location_note = {
            "note": f"I am based in {', '.join(location_parts)}",
            "category": "location_preferences",
            "title": "Primary Work Location",
            "temporal_durability": "stable"
        }
        me_notes.append(location_note)
    
    # Communication Preferences
    contact_methods = []
    if beta_profile_data.get('mail'):
        contact_methods.append(f"email at {beta_profile_data['mail']}")
    if beta_profile_data.get('businessPhones'):
        for phone in beta_profile_data['businessPhones']:
            contact_methods.append(f"phone at {phone}")
    if beta_profile_data.get('imAddresses'):
        for im in beta_profile_data['imAddresses']:
            contact_methods.append(f"IM at {im}")
    
    if contact_methods:
        contact_note = {
            "note": f"I can be reached via {', '.join(contact_methods)}",
            "category": "communication_style",
            "title": "Preferred Contact Methods",
            "temporal_durability": "stable"
        }
        me_notes.append(contact_note)
    
    # Technology and Platform Usage
    assigned_licenses = beta_profile_data.get('assignedLicenses', [])
    enabled_services = set()
    
    # Extract enabled services from assigned plans
    assigned_plans = beta_profile_data.get('assignedPlans', [])
    for plan in assigned_plans:
        if plan.get('capabilityStatus') == 'Enabled':
            service = plan.get('service', '')
            if service:
                enabled_services.add(service)
    
    # Categorize services for insights
    collaboration_services = {'TeamspaceAPI', 'MicrosoftCommunicationsOnline', 'SharePoint', 'exchange'}
    productivity_services = {'MicrosoftOffice', 'PowerAppsService', 'ProcessSimple', 'OfficeForms'}
    security_services = {'AADPremiumService', 'WindowsDefenderATP', 'Adallom', 'RMSOnline'}
    analytics_services = {'PowerBI', 'CRM', 'YammerEnterprise'}
    
    collab_tools = enabled_services.intersection(collaboration_services)
    productivity_tools = enabled_services.intersection(productivity_services)
    security_tools = enabled_services.intersection(security_services)
    analytics_tools = enabled_services.intersection(analytics_services)
    
    if collab_tools:
        collab_note = {
            "note": f"I actively use Microsoft collaboration tools including {', '.join(sorted(collab_tools))}",
            "category": "technology_preferences",
            "title": "Collaboration Platform Usage",
            "temporal_durability": "stable"
        }
        me_notes.append(collab_note)
    
    if productivity_tools:
        productivity_note = {
            "note": f"I work with Microsoft productivity suite including {', '.join(sorted(productivity_tools))}",
            "category": "technology_preferences", 
            "title": "Productivity Tool Preferences",
            "temporal_durability": "stable"
        }
        me_notes.append(productivity_note)
    
    # Device and Security Insights
    device_keys = beta_profile_data.get('deviceKeys', [])
    device_count = len(device_keys)
    if device_count > 0:
        device_note = {
            "note": f"I use {device_count} registered devices for secure authentication and access",
            "category": "technology_preferences",
            "title": "Multi-Device Security Setup",
            "temporal_durability": "dynamic"
        }
        me_notes.append(device_note)
    
    # Account and Identity Insights
    account_enabled = beta_profile_data.get('accountEnabled', False)
    if account_enabled:
        identity_note = {
            "note": f"I maintain an active Microsoft corporate identity with username {beta_profile_data.get('mailNickname', 'N/A')}",
            "category": "professional_identity",
            "title": "Corporate Identity Status",
            "temporal_durability": "stable"
        }
        me_notes.append(identity_note)
    
    # Regional and Language Preferences
    usage_location = beta_profile_data.get('usageLocation')
    preferred_data_location = beta_profile_data.get('preferredDataLocation')
    
    if usage_location or preferred_data_location:
        location_parts = []
        if usage_location:
            location_parts.append(f"usage location {usage_location}")
        if preferred_data_location:
            location_parts.append(f"preferred data region {preferred_data_location}")
        
        region_note = {
            "note": f"My regional preferences are set to {', '.join(location_parts)}",
            "category": "location_preferences",
            "title": "Regional and Data Preferences",
            "temporal_durability": "stable"
        }
        me_notes.append(region_note)
    
    # Advanced Security and Compliance
    password_policies = beta_profile_data.get('passwordPolicies')
    if password_policies:
        security_note = {
            "note": f"My account follows {password_policies} security policy",
            "category": "security_preferences",
            "title": "Account Security Configuration",
            "temporal_durability": "stable"
        }
        me_notes.append(security_note)
    
    # Organizational Hierarchy
    reports_to_name = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_ReportsToFullName')
    reports_to_email = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_ReportsToEmailName')
    
    if reports_to_name:
        reporting_note = {
            "note": f"I report to {reports_to_name}" + (f" ({reports_to_email})" if reports_to_email else ""),
            "category": "professional_context",
            "title": "Reporting Relationship",
            "temporal_durability": "stable"
        }
        me_notes.append(reporting_note)
    
    # Cost Center and Organizational Structure
    cost_center = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_CostCenterCode')
    company_code = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_CompanyCode')
    
    if cost_center or company_code:
        org_parts = []
        if cost_center:
            org_parts.append(f"cost center {cost_center}")
        if company_code:
            org_parts.append(f"company code {company_code}")
        
        org_note = {
            "note": f"I am organizationally assigned to {', '.join(org_parts)}",
            "category": "professional_context",
            "title": "Organizational Assignment",
            "temporal_durability": "stable"
        }
        me_notes.append(org_note)
    
    # Physical Office Details
    building_name = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_BuildingName')
    address_line1 = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_AddressLine1')
    address_line2 = beta_profile_data.get('extension_18e31482d3fb4a8ea958aa96b662f508_AddressLine2')
    
    if building_name or address_line1:
        address_parts = []
        if building_name:
            address_parts.append(building_name)
        if address_line2:
            address_parts.append(address_line2)
        if address_line1:
            address_parts.append(address_line1)
        
        office_note = {
            "note": f"My office is located at {', '.join(address_parts)}",
            "category": "location_preferences",
            "title": "Detailed Office Location",
            "temporal_durability": "stable"
        }
        me_notes.append(office_note)
    
    return me_notes

def create_comprehensive_me_notes():
    """
    Create comprehensive Me Notes from the beta API profile data
    """
    # Your actual beta profile data
    beta_profile_data = {
        "@odata.context": "https://graph.microsoft.com/beta/$metadata#users(*)/$entity",
        "@microsoft.graph.tips": "Use $select to choose only the properties your app needs, as this can lead to performance improvements. For example: GET me?$select=signInActivity,cloudLicensing",
        "id": "88573e4b-a91e-4334-89c2-a61178320813",
        "deletedDateTime": None,
        "accountEnabled": True,
        "ageGroup": None,
        "businessPhones": ["+86 (10) 59173481"],
        "city": "Beijing",
        "createdDateTime": None,
        "creationType": None,
        "companyName": "MICROSOFT CHINA CO LTD",
        "consentProvidedForMinor": None,
        "country": None,
        "department": "Time and Places - China 1107",
        "displayName": "Chin-Yew Lin",
        "employeeId": "296668",
        "employeeHireDate": None,
        "employeeLeaveDateTime": None,
        "employeeType": None,
        "faxNumber": None,
        "givenName": "Chin-Yew",
        "imAddresses": ["cyl@microsoft.com"],
        "infoCatalogs": [],
        "isLicenseReconciliationNeeded": False,
        "isManagementRestricted": None,
        "isResourceAccount": None,
        "jobTitle": "SR PRINCIPAL RESEARCH MANAGER",
        "legalAgeGroupClassification": None,
        "mail": "cyl@microsoft.com",
        "mailNickname": "cyl",
        "mobilePhone": None,
        "onPremisesDistinguishedName": "CN=Chin-Yew Lin,OU=MSE,OU=Users,OU=CoreIdentity,DC=redmond,DC=corp,DC=microsoft,DC=com",
        "officeLocation": "BEIJING-BJW-2/13463",
        "onPremisesDomainName": "redmond.corp.microsoft.com",
        "onPremisesImmutableId": "296668",
        "onPremisesLastSyncDateTime": "2025-09-01T15:17:15Z",
        "onPremisesSecurityIdentifier": "S-1-5-21-2127521184-1604012920-1887927527-2681880",
        "onPremisesSamAccountName": "cyl",
        "onPremisesSyncEnabled": True,
        "onPremisesUserPrincipalName": "cyl@microsoft.com",
        "otherMails": [],
        "passwordPolicies": "DisablePasswordExpiration",
        "postalCode": None,
        "preferredDataLocation": "APC",
        "preferredLanguage": None,
        "proxyAddresses": [
            "x500:/o=ExchangeLabs/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=microsoft.onmicrosoft.com-55760-Chin-Yew Lin",
            "x500:/o=ExchangeLabs/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=cyl76a7c118a4",
            "x500:/o=MSNBC/ou=Servers/cn=Recipients/cn=cyl",
            "x500:/o=SDF/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=cyl_microsoft.com78390e34",
            "x500:/o=microsoft/ou=First Administrative Group/cn=Recipients/cn=cyl",
            "x500:/o=microsoft/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=Chin-Yew Lin",
            "x500:/o=SDF/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=51490-cyl_ec67c12c81",
            "x500:/O=microsoft/OU=northamerica/cn=Recipients/cn=cyl",
            "x500:/O=Nokia/OU=HUB/cn=Recipients/cn=cyl",
            "x500:/o=SDF/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=sdflabs.com-51490-Chin-Yew Lin63da09fb",
            "X500:/o=MMS/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=Chin-Yew Lin92ec7b8c-a3d2-4549-9c51-84c1680ccc26",
            "x500:/o=SDF/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=sdflabs.com-51490-Chin-Yew Lin",
            "smtp:cyl@titanium.microsoft.com",
            "SMTP:cyl@microsoft.com",
            "smtp:cyl@Service.microsoft.com"
        ],
        "refreshTokensValidFromDateTime": "2023-12-02T12:18:07Z",
        "securityIdentifier": "S-1-12-1-2287418955-1127524638-296141449-319304312",
        "showInAddressList": True,
        "signInSessionsValidFromDateTime": "2023-12-02T12:18:07Z",
        "state": None,
        "streetAddress": None,
        "surname": "Lin",
        "usageLocation": "CN",
        "userPrincipalName": "cyl@microsoft.com",
        "externalUserConvertedOn": None,
        "externalUserState": None,
        "externalUserStateChangeDateTime": None,
        "userType": "Member",
        "identityParentId": None,
        "extension_18e31482d3fb4a8ea958aa96b662f508_ProfitCenterCode": "P21009085",
        "extension_18e31482d3fb4a8ea958aa96b662f508_CostCenterCode": "21009085",
        "extension_18e31482d3fb4a8ea958aa96b662f508_SupervisorInd": "N",
        "extension_18e31482d3fb4a8ea958aa96b662f508_ReportsToPersonnelNbr": "159898",
        "extension_18e31482d3fb4a8ea958aa96b662f508_ReportsToFullName": "Dongmei Zhang",
        "extension_18e31482d3fb4a8ea958aa96b662f508_ReportsToEmailName": "DONGMEIZ",
        "extension_18e31482d3fb4a8ea958aa96b662f508_PositionNumber": "72840924",
        "extension_18e31482d3fb4a8ea958aa96b662f508_StateProvinceCode": "BJ",
        "extension_18e31482d3fb4a8ea958aa96b662f508_CompanyCode": "1107",
        "extension_18e31482d3fb4a8ea958aa96b662f508_BuildingName": "BEIJING-BJW-2",
        "extension_18e31482d3fb4a8ea958aa96b662f508_ZipCode": "100080",
        "extension_18e31482d3fb4a8ea958aa96b662f508_CountryShortCode": "CN",
        "extension_18e31482d3fb4a8ea958aa96b662f508_CityName": "Beijing",
        "extension_18e31482d3fb4a8ea958aa96b662f508_AddressLine2": "Building 1",
        "extension_18e31482d3fb4a8ea958aa96b662f508_AddressLine1": "No.5 DanLing Street, Haidian Dst",
        "extension_18e31482d3fb4a8ea958aa96b662f508_BuildingID": "100874",
        "extension_18e31482d3fb4a8ea958aa96b662f508_LocationAreaCode": "CN",
        "extension_18e31482d3fb4a8ea958aa96b662f508_PersonnelNumber": "296668",
        "employeeOrgData": None,
        "passwordProfile": None,
        "assignedLicenses": [
            {"disabledPlans": [], "skuId": "18a4bd3f-0b5b-4887-b04f-61dd0ee15f5e"},
            {"disabledPlans": [], "skuId": "c8cd7c53-456a-4fc0-b38f-616cdcf4eaa9"}
            # ... (truncated for brevity)
        ],
        "assignedPlans": [
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "exchange", "servicePlanId": "9f431833-0334-42de-a7dc-70aa40db46db"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "MicrosoftCommunicationsOnline", "servicePlanId": "0feaeb32-d00e-4d66-bd5a-43b5b83db82c"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "SharePoint", "servicePlanId": "fe71d6c3-a2ea-4499-9778-da042bf08063"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "TeamspaceAPI", "servicePlanId": "57ff2da0-773e-42df-b2af-ffb7a2317929"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "MicrosoftOffice", "servicePlanId": "43de0ff5-c92c-492b-9116-175376d08c38"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "PowerAppsService", "servicePlanId": "9c0dab89-a30c-4117-86e7-97bda240acd2"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "AADPremiumService", "servicePlanId": "41781fb2-bc02-4b7c-bd55-b576c07bb09d"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "PowerBI", "servicePlanId": "70d33638-9c74-4d01-bfd3-562de28bd4ba"},
            {"assignedDateTime": "2025-10-08T20:50:43Z", "capabilityStatus": "Enabled", "service": "CRM", "servicePlanId": "60bf28f9-2b70-4522-96f7-335f5e06c941"}
            # ... (more services)
        ],
        "deviceKeys": [
            {"deviceId": "0db9e052-89d0-4705-bee3-bdb697b92b40", "keyMaterial": "...", "keyType": "NGC"},
            {"deviceId": "425213ca-cc5a-4056-8448-1938debca99e", "keyMaterial": "...", "keyType": "NGC"}
            # ... (more devices)
        ]
    }
    
    # Extract comprehensive insights
    me_notes = extract_personal_insights_from_beta(beta_profile_data)
    
    # Create the complete Me Notes structure
    comprehensive_me_notes = {
        "user_id": beta_profile_data.get('userPrincipalName', 'unknown'),
        "generated_at": datetime.now().isoformat(),
        "source": "Microsoft Graph Beta API",
        "api_endpoint": "https://graph.microsoft.com/beta/me",
        "me_notes": me_notes,
        "summary": {
            "total_notes": len(me_notes),
            "categories": list(set(note['category'] for note in me_notes)),
            "profile_completeness": "comprehensive",
            "data_richness": "high"
        }
    }
    
    # Save to file
    output_file = f"me_notes_comprehensive_beta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_me_notes, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Comprehensive Me Notes generated successfully!")
    print(f"📄 Saved to: {output_file}")
    print(f"📊 Generated {len(me_notes)} personal insights")
    print(f"🏷️  Categories: {', '.join(comprehensive_me_notes['summary']['categories'])}")
    
    # Display sample insights
    print("\n🔍 Sample Personal Insights:")
    for i, note in enumerate(me_notes[:5], 1):
        print(f"{i}. [{note['category']}] {note['title']}: {note['note']}")
    
    if len(me_notes) > 5:
        print(f"   ... and {len(me_notes) - 5} more insights")
    
    return comprehensive_me_notes

if __name__ == "__main__":
    print("🚀 Creating Comprehensive Me Notes from Microsoft Graph Beta API...")
    result = create_comprehensive_me_notes()
    print("\n✨ Me Notes generation complete!")