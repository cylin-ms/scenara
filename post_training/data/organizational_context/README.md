# Organizational Context for Realistic Meeting Data

## Overview

To generate realistic meeting data, we need authentic organizational context including:
- **Teams and reporting structures**
- **Companies and partnerships** (internal + external)
- **Realistic attendee networks** (3-15 people per meeting)
- **Cross-team collaboration patterns**
- **Customer/vendor relationships**

This directory contains organizational structures that feed into calendar generation.

## Structure

```
organizational_context/
├── README.md                           # This file
├── companies/                          # Company definitions
│   ├── contoso_corp.json              # Our company (internal)
│   ├── fabrikam_inc.json              # Customer company
│   ├── adventure_works.json           # Customer company
│   ├── wingtip_toys.json              # Partner company
│   └── litware_inc.json               # Vendor company
├── teams/                             # Internal team structures
│   ├── sales_team.json                # Sales organization
│   ├── engineering_team.json          # Engineering organization
│   ├── product_team.json              # Product organization
│   ├── legal_team.json                # Legal organization
│   └── finance_team.json              # Finance organization
└── attendee_networks/                 # Pre-defined attendee groups
    ├── tier1_sales_network.json       # Who Tier 1 Sales Manager meets with
    ├── tier2_architect_network.json   # Who Tier 2 Architect meets with
    └── tier3_legal_network.json       # Who Tier 3 Legal meets with
```

## Design Principles

### 1. Realistic Attendee Counts
- **1:1 meetings**: 2 people (persona + 1)
- **Team meetings**: 5-12 people
- **Cross-team meetings**: 6-15 people
- **Customer calls**: 3-8 people (internal) + 2-5 (customer)
- **Executive reviews**: 5-10 people

### 2. Role-Based Networks
Each persona has a **network** of people they frequently meet with:
- **Direct reports** (for managers)
- **Manager** (reporting relationship)
- **Team members** (peers)
- **Cross-team partners** (collaborators)
- **Customers** (external contacts)
- **Vendors** (external suppliers)

### 3. Company Structures
- **Contoso Corp**: Our company (full structure)
- **Customer Companies**: External contacts for sales/support
- **Partner Companies**: Integration/collaboration partners
- **Vendor Companies**: Service providers

### 4. Meeting Type → Attendee Patterns
- **Weekly 1:1**: Persona + Manager (2 people)
- **Team Sync**: Entire team (8-12 people)
- **Customer Call**: Internal team (3-5) + Customer side (2-4)
- **Architecture Review**: Architect + Engineers + PM (6-10)
- **Contract Review**: Legal team (2-3) + Stakeholders (2-4)

## Next Steps

1. **Create Company Structures** (5 companies)
2. **Define Internal Teams** (5 teams with org charts)
3. **Build Attendee Networks** (persona-specific contact lists)
4. **Update Calendar Generator** (use networks for realistic attendees)
5. **Regenerate Calendars** (with proper attendee counts)
