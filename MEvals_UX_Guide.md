# 🔐 Running MEvals Native UX - Meeting Selection Interface

## 🎯 Overview

MEvals has a **sophisticated authentication-based UX** that allows users to select from their own Microsoft meetings through interactive Microsoft Graph authentication. Unlike traditional web UIs, this system provides a **secure, enterprise-grade interface** for accessing real meeting data.

## 🚀 How to Run MEvals Native UX

### 📋 **Prerequisites**

1. **Microsoft Organizational Account**: Access to Microsoft 365 with meeting data
2. **Windows Environment**: Optimal for Windows Broker (WAM) authentication
3. **Microsoft Graph API Access**: Permissions for calendar reading

### 🛠️ **Setup Process**

#### **Option 1: Quick Setup (Windows PowerShell)**
```powershell
# Navigate to MEvals directory
cd /Users/cyl/projects/PromptCoT/MEvals

# Run the complete setup
.\setup.ps1

# Or use the orchestration script
pwsh .\run_all.ps1 -AutoSetup -Force
```

#### **Option 2: Manual Setup (Cross-Platform)**
```bash
# Create conda environment
conda create -n mevals python=3.11 -y
conda activate mevals

# Install dependencies
pip install "msal[broker]>=1.20,<2" requests
```

### 🔐 **Authentication & Meeting Selection Process**

#### **Step 1: Interactive Authentication**
```bash
# Run the meeting list fetcher (this triggers the UX)
python step1_get_meeting_list.py
```

**What happens:**
1. **Browser-based authentication** launches automatically
2. **Microsoft login prompt** appears for organizational account
3. **Consent screen** for calendar access permissions
4. **Token caching** for subsequent runs

#### **Step 2: Meeting Selection Parameters**
```bash
# Fetch meetings for specific date range
python step1_get_meeting_list.py --start 2025-09-01T00:00:00 --end 2025-10-31T23:59:59

# Fetch last 30 days (default)
python step1_get_meeting_list.py

# Fetch with custom filters
python step1_get_meeting_list.py --days 14 --top 100
```

**Selection Options:**
- **Date Range**: Specify start/end dates for meeting retrieval
- **Meeting Count**: Limit number of meetings to process
- **Filter Criteria**: Exclude cancelled, out-of-office meetings
- **Pagination**: Automatic handling of large meeting lists

### 🎛️ **Complete Pipeline Execution**

#### **Full Meeting Processing Workflow**
```bash
# Step 1: Get meeting list (Interactive UX)
python step1_get_meeting_list.py

# Step 2: Generate meeting prep summaries
python step2_generate_meeting_prep.py

# Step 3: Extract GPT requests
python step3_extract_gpt_requests.py

# Step 4: Extract context variables
python step4_extract_context_variables.py

# Step 5: Render from context
python step5_render_from_context.py

# Step 6: Generate LLM responses
python step6_generate_llm_responses.py
```

#### **One-Command Orchestration (PowerShell)**
```powershell
# Complete pipeline with setup
pwsh .\run_all.ps1 -AutoSetup -Force -V4 -Days 30

# Quick test run
pwsh .\run_all.ps1 -V4 -Days 7 -Limit 5

# Validation only
pwsh .\run_all.ps1 -OnlyValidations
```

### 🔧 **macOS Adaptation**

Since you're on macOS, here's how to run it with our cross-platform adaptation:

```bash
# Use our macOS-adapted authentication
cd /Users/cyl/projects/PromptCoT
python mevals_auth_manager.py  # Test authentication

# Run MEvals with device flow
cd MEvals
export MSAL_DISABLE_BROKER=1  # Disable Windows Broker
python step1_get_meeting_list.py
```

### 📊 **Meeting Selection Interface Features**

#### **Authentication UX**
- **Device Flow Authentication**: For macOS/Linux compatibility
- **Windows Broker (WAM)**: Native Windows authentication
- **Token Caching**: Persistent authentication across sessions
- **Multi-tenant Support**: Enterprise and personal accounts

#### **Meeting Filtering**
- **Date Range Selection**: Past/future meeting windows
- **Meeting Type Filtering**: Exclude OOF, cancelled meetings
- **Organizer Filtering**: Focus on specific meeting organizers
- **Size Limits**: Handle large calendars efficiently

#### **Data Export Options**
- **CSV Export**: Meeting lists with metadata
- **JSONL Format**: Structured meeting preparation data
- **Template-based Rendering**: Customizable output formats

## 🎯 **Real Meeting Data Selection Process**

### **What MEvals UX Provides:**

1. **📅 Calendar Integration**: Direct access to user's Microsoft 365 calendar
2. **🔐 Secure Authentication**: Enterprise-grade Microsoft Graph access
3. **📊 Meeting Metadata**: Subject, organizer, participants, time, location
4. **📝 Content Access**: Meeting transcripts, chat, attachments, notes
5. **🎛️ Flexible Filtering**: Date ranges, meeting types, participants

### **Meeting Selection Workflow:**

```
User Authentication → Calendar Access → Meeting Discovery → Content Extraction → Processing
       ↓                    ↓               ↓                ↓               ↓
  Microsoft Login    →  Graph API     →  Meeting List   →  Transcripts   →  Training Data
  (Browser/WAM)         Permissions      (CSV/JSON)        & Content       (JSONL)
```

## 🌟 **Advantages of MEvals UX Approach**

### **Enterprise Security**
✅ **Microsoft Graph Integration**: Official API with enterprise security
✅ **OAuth 2.0 Authentication**: Industry-standard secure authentication
✅ **Token Management**: Secure token storage and refresh
✅ **Audit Trail**: Full logging of data access

### **Real Data Access**
✅ **Authentic Meetings**: Real Microsoft 365 meeting data
✅ **Rich Context**: Transcripts, chat, files, participants
✅ **Metadata Complete**: All meeting attributes and relationships
✅ **Live Updates**: Current meeting data from active calendars

### **Scalable Processing**
✅ **Batch Processing**: Handle hundreds of meetings efficiently
✅ **Parallel Execution**: Multi-threaded processing capabilities
✅ **Incremental Updates**: Process only new/changed meetings
✅ **Error Recovery**: Robust handling of API limits and failures

## 🔄 **Integration with Meeting PromptCoT**

To use MEvals UX data with our Meeting PromptCoT system:

```bash
# 1. Run MEvals to get real meeting data
cd MEvals
python step1_get_meeting_list.py
python step2_generate_meeting_prep.py

# 2. Convert to Meeting PromptCoT format
cd ..
python mevals_promptcot_bridge.py \
  --mevals-data MEvals/data/meeting_prep.prompt.samples \
  --output meeting_prep_real_data

# 3. Launch our enhanced UX interface
./launch_data_explorer.sh
```

## 🎉 **Result: Enterprise-Grade Meeting Selection**

MEvals provides a **professional, secure UX** for accessing real Microsoft meeting data through:

- **🔐 Enterprise Authentication**: Microsoft Graph OAuth integration
- **📅 Interactive Meeting Selection**: Date ranges, filters, and search
- **📊 Rich Data Export**: Multiple formats and processing pipelines
- **🛠️ Developer-Friendly**: Command-line interface with automation support

**The MEvals UX is designed for enterprise developers and data scientists who need secure, programmatic access to real Microsoft meeting data for AI training and evaluation!**