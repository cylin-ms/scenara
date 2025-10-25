# MEvals macOS Adaptation Analysis

## Executive Summary

The **MEvals** codebase is a Windows-centric meeting data collection and evaluation system that uses **Microsoft Graph APIs** and **MSAL (Microsoft Authentication Library)** with **Windows Broker (WAM)** for authentication. To adapt this for macOS and integrate with **Meeting PromptCoT**, we need to address platform-specific dependencies while preserving the core functionality for real meeting data collection.

## Current Architecture Analysis

### Core Components

1. **Authentication System**
   - Uses MSAL Python with Windows Broker (WAM)
   - Enables seamless Microsoft 365 authentication
   - Leverages Windows Active Directory integration

2. **Data Collection Pipeline**
   - `step1_get_meeting_list.py`: Fetch meeting list via Microsoft Graph
   - `step2_generate_meeting_prep.py`: Download meeting preparation summaries
   - `step3_extract_gpt_requests.py`: Extract GPT request data
   - `step4_extract_context_variables.py`: Reconstruct context variables
   - `step5_render_from_context.py`: Re-render from context
   - `step6_generate_llm_responses.py`: Generate LLM responses
   - `step7_rebuild_meeting_prep.py`: Rebuild meeting preparation

3. **Evaluation Framework**
   - Multiple evaluation types: conflict, contradiction, cross-section, redundancy
   - SEval (Structured Evaluation) system
   - Professional meeting preparation assessment

4. **Data Structure**
   - Rich meeting samples with context variables
   - Professional evaluation criteria (Contextual Relevance, Comprehension, etc.)
   - Real-world Microsoft meeting data

## Windows-Specific Dependencies

### 1. PowerShell Scripts
**Issue**: Extensive use of PowerShell (.ps1) scripts for orchestration
```powershell
# Examples from codebase
.\setup.ps1
.\run_all.ps1 -AutoSetup -Force
pwsh .\run_contradiction_eval.ps1
```

### 2. Windows Authentication Broker (WAM)
**Issue**: All authentication relies on Windows-specific WAM integration
```python
# Current Windows-specific code
app = msal.PublicClientApplication(
    CLIENT_ID,
    authority=authority,
    enable_broker_on_windows=True,  # Windows-only feature
)
```

### 3. Windows-Specific Paths and Environment
**Issue**: Windows path conventions and environment variables
```python
# Windows-specific patterns
user = os.getenv("USERNAME")  # Windows env var
login_hint = f"{user}@microsoft.com"
```

### 4. Conda/Python Environment Setup
**Issue**: Windows-specific Miniconda installation and setup
```powershell
# Downloads Windows-specific Miniconda installer
Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
```

## macOS Adaptation Strategy

### Phase 1: Core Authentication Adaptation

#### 1.1 MSAL Authentication Without WAM
**Solution**: Use MSAL Python with device code flow or interactive authentication without Windows Broker

```python
# macOS-compatible authentication
def acquire_token_macos():
    """
    MSAL authentication for macOS using device code flow or browser redirect
    """
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=authority,
        # Remove enable_broker_on_windows=True
    )
    
    # Try silent first
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(GRAPH_SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result
    
    # Fallback to device code flow (works on any platform)
    flow = app.initiate_device_flow(scopes=GRAPH_SCOPES)
    if "user_code" in flow:
        print(f"Visit {flow['verification_uri']} and enter code: {flow['user_code']}")
        result = app.acquire_token_by_device_flow(flow)
        return result
    
    # Alternative: browser redirect (requires redirect URI setup)
    # result = app.acquire_token_interactive(GRAPH_SCOPES)
    # return result
```

#### 1.2 Environment Variable Adaptation
**Solution**: Cross-platform environment variable detection

```python
def _login_hint():
    """Cross-platform user detection"""
    # Try different environment variables
    user = (os.getenv("USERNAME") or  # Windows
            os.getenv("USER") or      # Unix/Linux/macOS
            os.getenv("LOGNAME"))     # Alternative Unix
    
    # Try to get email from git config as fallback
    if not user:
        try:
            import subprocess
            result = subprocess.run(['git', 'config', 'user.email'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                email = result.stdout.strip()
                if '@microsoft.com' in email:
                    return email
        except:
            pass
    
    return f"{user}@microsoft.com" if user else None
```

### Phase 2: Shell Script Conversion

#### 2.1 PowerShell to Bash Conversion
**Solution**: Create equivalent bash scripts for macOS

```bash
#!/bin/bash
# run_all_macos.sh - macOS equivalent of run_all.ps1

set -euo pipefail

# Default parameters
DAYS=30
FORCE=false
V3=false
V4=false
AUTO_SETUP=false
CONDA_ENV="mevals"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --days)
            DAYS="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --v3)
            V3=true
            shift
            ;;
        --v4)
            V4=true
            shift
            ;;
        --auto-setup)
            AUTO_SETUP=true
            shift
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

# Auto setup conda environment if requested
if [ "$AUTO_SETUP" = true ]; then
    echo "Setting up conda environment..."
    if ! command -v conda &> /dev/null; then
        echo "Installing Miniconda for macOS..."
        curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
        bash Miniconda3-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda3
        eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    fi
    
    conda create -n $CONDA_ENV python=3.11 -y || true
    conda activate $CONDA_ENV
    pip install "msal>=1.20,<2" requests
fi

# Run the pipeline steps
echo "Running MEvals pipeline on macOS..."
python step1_get_meeting_list.py --days $DAYS
python step2_generate_meeting_prep.py $([ "$V3" = true ] && echo "--v3") $([ "$V4" = true ] && echo "--v4")
python step3_extract_gpt_requests.py $([ "$FORCE" = true ] && echo "--force")
python step4_extract_context_variables.py $([ "$FORCE" = true ] && echo "--force")
python step5_render_from_context.py $([ "$FORCE" = true ] && echo "--force")
```

#### 2.2 Setup Script Adaptation
**Solution**: macOS-specific setup script

```bash
#!/bin/bash
# setup_macos.sh - macOS equivalent of setup.ps1

set -euo pipefail

echo "Setting up MEvals for macOS..."

# 1. Ensure Downloads folder
mkdir -p "$PWD/Downloads"

# 2. Detect architecture and download appropriate Miniconda
if [[ $(uname -m) == "arm64" ]]; then
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
    INSTALLER="Miniconda3-latest-MacOSX-arm64.sh"
else
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
fi

DEST="$PWD/Downloads/$INSTALLER"

if [ ! -f "$DEST" ]; then
    echo "Downloading Miniconda for macOS..."
    curl -L "$MINICONDA_URL" -o "$DEST"
fi

# 3. Verify download
ls -la "$DEST"

# 4. Install Miniconda
echo "Installing Miniconda..."
bash "$DEST" -b -p "$HOME/miniconda3"

# 5. Initialize conda for current session
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"

# 6. Verify installation
conda --version

echo "Miniconda setup complete!"
```

### Phase 3: Core Pipeline Adaptation

#### 3.1 Authentication Module
**Solution**: Create cross-platform authentication module

```python
# auth_manager.py - Cross-platform authentication
import os
import sys
import platform
import msal
from typing import Optional, Dict, Any

class CrossPlatformAuthManager:
    """
    Cross-platform Microsoft Graph authentication manager
    Handles Windows WAM, macOS, and Linux authentication flows
    """
    
    def __init__(self, tenant_id: str, client_id: str, scopes: list):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.scopes = scopes
        self.platform = platform.system().lower()
        
    def get_msal_app(self) -> msal.PublicClientApplication:
        """Create MSAL app with platform-appropriate settings"""
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        
        if self.platform == "windows":
            # Use Windows Broker if available
            return msal.PublicClientApplication(
                self.client_id,
                authority=authority,
                enable_broker_on_windows=True
            )
        else:
            # Standard MSAL for macOS/Linux
            return msal.PublicClientApplication(
                self.client_id,
                authority=authority
            )
    
    def acquire_token(self) -> Optional[Dict[str, Any]]:
        """Acquire token using platform-appropriate method"""
        app = self.get_msal_app()
        
        # Try silent authentication first
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
            if result and "access_token" in result:
                return result
        
        # Platform-specific interactive authentication
        if self.platform == "windows":
            return self._acquire_token_windows(app)
        elif self.platform == "darwin":  # macOS
            return self._acquire_token_macos(app)
        else:  # Linux and others
            return self._acquire_token_linux(app)
    
    def _acquire_token_windows(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """Windows-specific authentication with WAM"""
        login_hint = self._get_login_hint()
        return app.acquire_token_interactive(
            self.scopes,
            login_hint=login_hint
        )
    
    def _acquire_token_macos(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """macOS-specific authentication"""
        # Try interactive browser flow first
        try:
            login_hint = self._get_login_hint()
            return app.acquire_token_interactive(
                self.scopes,
                login_hint=login_hint
            )
        except Exception as e:
            print(f"Browser authentication failed: {e}")
            return self._acquire_token_device_flow(app)
    
    def _acquire_token_linux(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """Linux-specific authentication (device flow)"""
        return self._acquire_token_device_flow(app)
    
    def _acquire_token_device_flow(self, app: msal.PublicClientApplication) -> Optional[Dict[str, Any]]:
        """Device code flow for headless or problematic environments"""
        flow = app.initiate_device_flow(scopes=self.scopes)
        if "user_code" in flow:
            print(f"\nPlease visit {flow['verification_uri']}")
            print(f"Enter this code: {flow['user_code']}")
            print("Waiting for authentication...")
            
            result = app.acquire_token_by_device_flow(flow)
            return result
        return None
    
    def _get_login_hint(self) -> Optional[str]:
        """Get login hint from various sources"""
        # Try environment variables
        user = (os.getenv("USERNAME") or  # Windows
                os.getenv("USER") or      # Unix/macOS
                os.getenv("LOGNAME"))     # Alternative
        
        if user:
            return f"{user}@microsoft.com"
        
        # Try git config
        try:
            import subprocess
            result = subprocess.run(['git', 'config', 'user.email'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                email = result.stdout.strip()
                if '@microsoft.com' in email:
                    return email
        except:
            pass
        
        return None
```

#### 3.2 Adapted Core Scripts
**Solution**: Update core Python scripts for cross-platform compatibility

```python
# step1_get_meeting_list_macos.py - macOS-adapted version
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cross-platform meeting list fetcher using Microsoft Graph API
Adapted from Windows-specific MEvals for macOS compatibility
"""

import os
import sys
import json
import csv
import pathlib
import argparse
import platform
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
import requests

# Import our cross-platform auth manager
from auth_manager import CrossPlatformAuthManager

# ======== Config ========
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
CLIENT_ID = "9ce97a32-d9ab-4ab2-aadc-f49b39b94e11"
GRAPH_SCOPES = ["Calendars.Read", "offline_access", "openid", "profile"]

def main():
    parser = argparse.ArgumentParser(description="Fetch meeting list via Microsoft Graph")
    parser.add_argument("--days", type=int, default=30, help="Days to look ahead")
    parser.add_argument("--output", default="out/meetings.csv", help="Output CSV file")
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Initialize cross-platform authentication
    auth_manager = CrossPlatformAuthManager(TENANT_ID, CLIENT_ID, GRAPH_SCOPES)
    
    print(f"Authenticating on {platform.system()}...")
    token_result = auth_manager.acquire_token()
    
    if not token_result or "access_token" not in token_result:
        print("❌ Authentication failed")
        sys.exit(1)
    
    print("✅ Authentication successful")
    
    # Calculate date range
    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=args.days)
    
    # Fetch meetings via Graph API
    meetings = fetch_meetings(token_result["access_token"], start_date, end_date)
    
    # Save to CSV
    save_meetings_csv(meetings, args.output)
    print(f"✅ Saved {len(meetings)} meetings to {args.output}")

def fetch_meetings(access_token: str, start_date: datetime, end_date: datetime) -> list:
    """Fetch meetings from Microsoft Graph API"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Format dates for Graph API
    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    
    # Graph API calendar view endpoint
    url = f"https://graph.microsoft.com/v1.0/me/calendarView"
    params = {
        "startDateTime": start_str,
        "endDateTime": end_str,
        "$select": "id,subject,start,end,organizer,attendees,location,bodyPreview",
        "$orderby": "start/dateTime"
    }
    
    meetings = []
    
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ Graph API error: {response.status_code}")
            print(response.text)
            break
        
        data = response.json()
        meetings.extend(data.get("value", []))
        
        # Check for pagination
        url = data.get("@odata.nextLink")
        params = None  # Parameters are included in nextLink
        
        print(f"📅 Fetched {len(meetings)} meetings so far...")
    
    return meetings

def save_meetings_csv(meetings: list, output_path: str) -> None:
    """Save meetings to CSV file"""
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Id', 'Subject', 'StartTime', 'EndTime', 'Organizer', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for meeting in meetings:
            writer.writerow({
                'Id': meeting['id'],
                'Subject': meeting['subject'],
                'StartTime': meeting['start']['dateTime'],
                'EndTime': meeting['end']['dateTime'],
                'Organizer': meeting['organizer']['emailAddress']['name'],
                'Location': meeting.get('location', {}).get('displayName', '')
            })

if __name__ == "__main__":
    main()
```

### Phase 4: Integration with Meeting PromptCoT

#### 4.1 Data Bridge Module
**Solution**: Create bridge between MEvals data and Meeting PromptCoT

```python
# mevals_promptcot_bridge.py - Integration bridge
import json
import csv
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class MEValsPromptCoTBridge:
    """
    Bridge between MEvals real meeting data and Meeting PromptCoT training
    """
    
    def __init__(self, mevals_data_dir: str, promptcot_output_dir: str):
        self.mevals_data_dir = Path(mevals_data_dir)
        self.promptcot_output_dir = Path(promptcot_output_dir)
        self.promptcot_output_dir.mkdir(exist_ok=True)
    
    def extract_training_scenarios(self) -> List[Dict[str, Any]]:
        """Extract real meeting scenarios for Meeting PromptCoT training"""
        scenarios = []
        
        # Process each meeting sample
        sample_dirs = list(self.mevals_data_dir.glob("sample_*"))
        
        for sample_dir in sample_dirs:
            try:
                scenario = self._process_meeting_sample(sample_dir)
                if scenario:
                    scenarios.append(scenario)
            except Exception as e:
                print(f"⚠️ Error processing {sample_dir.name}: {e}")
        
        return scenarios
    
    def _process_meeting_sample(self, sample_dir: Path) -> Dict[str, Any]:
        """Process a single meeting sample"""
        # Read evaluation summary
        seval_summary = sample_dir / "seval.summary.md"
        if not seval_summary.exists():
            return None
        
        # Extract meeting context and evaluation
        context = self._extract_meeting_context(sample_dir)
        evaluation = self._extract_evaluation_scores(seval_summary)
        
        # Create Meeting PromptCoT compatible scenario
        scenario = {
            "scenario_id": sample_dir.name,
            "meeting_context": context,
            "real_world_data": True,
            "evaluation_scores": evaluation,
            "source": "MEvals",
            "timestamp": datetime.now().isoformat()
        }
        
        return scenario
    
    def _extract_meeting_context(self, sample_dir: Path) -> Dict[str, Any]:
        """Extract business context from meeting sample"""
        context = {}
        
        # Extract from various files in the sample
        input_dir = sample_dir / "input"
        if input_dir.exists():
            # Process meeting input data
            for file in input_dir.glob("*.json"):
                with open(file, 'r') as f:
                    data = json.load(f)
                    context.update(data)
        
        # Extract meeting subject and details from directory name
        dir_name = sample_dir.name
        parts = dir_name.split('_')
        if len(parts) >= 3:
            context["organizer"] = parts[1] + "_" + parts[2]
            context["meeting_subject"] = "_".join(parts[3:-1])
            context["meeting_date"] = parts[-1]
        
        return context
    
    def _extract_evaluation_scores(self, seval_file: Path) -> Dict[str, float]:
        """Extract evaluation scores from seval summary"""
        scores = {}
        
        with open(seval_file, 'r') as f:
            content = f.read()
        
        # Parse evaluation table
        lines = content.split('\n')
        for line in lines:
            if '|' in line and any(criterion in line.lower() for criterion in 
                                 ['contextual relevance', 'comprehension', 'sufficiency', 'page quality']):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    criterion = parts[1].lower().replace(' ', '_')
                    try:
                        score = float(parts[2]) / 100.0  # Convert to 0-1 scale
                        scores[criterion] = score
                    except:
                        pass
        
        return scores
    
    def convert_to_promptcot_format(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert MEvals data to Meeting PromptCoT training format"""
        promptcot_scenarios = []
        
        for scenario in scenarios:
            # Create rich company profile from meeting context
            company_profile = self._infer_company_profile(scenario["meeting_context"])
            
            # Generate Meeting PromptCoT compatible scenario
            promptcot_scenario = {
                "scenario_description": self._generate_scenario_description(scenario),
                "company_profile": company_profile,
                "meeting_objectives": self._extract_meeting_objectives(scenario),
                "stakeholder_dynamics": self._infer_stakeholder_dynamics(scenario),
                "business_context": self._extract_business_context(scenario),
                "success_metrics": scenario["evaluation_scores"],
                "source_data": {
                    "mevals_sample": scenario["scenario_id"],
                    "real_meeting": True,
                    "evaluation_quality": self._calculate_quality_score(scenario["evaluation_scores"])
                }
            }
            
            promptcot_scenarios.append(promptcot_scenario)
        
        return promptcot_scenarios
    
    def _infer_company_profile(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer company profile from meeting context"""
        # This is where we'd apply business intelligence to infer
        # company characteristics from meeting patterns and content
        
        organizer = meeting_context.get("organizer", "")
        subject = meeting_context.get("meeting_subject", "")
        
        # Basic inference - could be enhanced with ML models
        company_profile = {
            "company_name": "Microsoft Corporation",  # Known from data source
            "industry": "Technology",
            "size": "Large Enterprise (>10,000 employees)",
            "meeting_patterns": self._analyze_meeting_patterns(meeting_context),
            "organizational_structure": self._infer_org_structure(organizer),
            "business_focus": self._infer_business_focus(subject)
        }
        
        return company_profile
    
    def save_training_data(self, scenarios: List[Dict[str, Any]], filename: str = "mevals_training_data.jsonl"):
        """Save converted scenarios as JSONL for Meeting PromptCoT training"""
        output_file = self.promptcot_output_dir / filename
        
        with open(output_file, 'w') as f:
            for scenario in scenarios:
                f.write(json.dumps(scenario) + '\n')
        
        print(f"✅ Saved {len(scenarios)} training scenarios to {output_file}")
```

## Implementation Plan

### Phase 1: Immediate Adaptation (1-2 weeks)
1. **Create macOS Setup Scripts**
   - `setup_macos.sh` - macOS equivalent of `setup.ps1`
   - `run_all_macos.sh` - macOS equivalent of `run_all.ps1`

2. **Implement Cross-Platform Authentication**
   - `auth_manager.py` - Platform-agnostic MSAL authentication
   - Handle browser-based and device code flows for macOS

3. **Adapt Core Pipeline Scripts**
   - Update import statements and environment variable handling
   - Remove Windows Broker dependencies
   - Test authentication flow on macOS

### Phase 2: Data Integration (2-3 weeks)
1. **Create Data Bridge**
   - `mevals_promptcot_bridge.py` - Convert MEvals data to Meeting PromptCoT format
   - Extract real meeting contexts and business scenarios
   - Preserve evaluation quality metrics

2. **Enhanced Context Extraction**
   - Analyze real meeting patterns for business intelligence
   - Infer company profiles from meeting characteristics
   - Extract stakeholder dynamics from meeting participants

3. **Training Data Generation**
   - Convert real MEvals data to synthetic training scenarios
   - Maintain privacy while preserving business realism
   - Generate high-quality Meeting PromptCoT training corpus

### Phase 3: Integration Testing (1 week)
1. **End-to-End Testing**
   - Verify authentication on macOS
   - Test data collection pipeline
   - Validate Meeting PromptCoT integration

2. **Quality Validation**
   - Compare real vs synthetic scenario quality
   - Verify business context preservation
   - Test evaluation metric alignment

## Expected Benefits

### 1. Real-World Training Data
- **Authentic Business Contexts**: Real Microsoft meeting scenarios
- **Professional Evaluation Metrics**: Proven quality assessment criteria
- **Stakeholder Dynamics**: Actual organizational relationships

### 2. Enhanced Meeting PromptCoT
- **Context Grounding**: Real company data improves context modeling
- **Quality Benchmarking**: Professional evaluation standards
- **Business Realism**: Authentic enterprise decision-making patterns

### 3. Cross-Platform Compatibility
- **macOS Support**: Native development environment compatibility
- **Scalable Architecture**: Platform-agnostic design principles
- **Cloud Integration**: Microsoft Graph API compatibility

## Conclusion

Adapting MEvals for macOS will provide **Meeting PromptCoT** with access to high-quality, real-world meeting data that addresses the fundamental context dependency problem. This integration creates a powerful training data generation system that combines:

- **Real business contexts** from actual Microsoft meetings
- **Professional evaluation standards** from enterprise meeting preparation
- **Cross-platform compatibility** for flexible development and deployment
- **Privacy-preserving data extraction** that maintains business realism

The adapted system will significantly enhance Meeting PromptCoT's ability to generate contextually grounded, professionally validated meeting preparation advice.