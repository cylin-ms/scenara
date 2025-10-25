# 🎯 **Complete MEvals UX Guide - How to Run It**

## 📋 **MEvals UX Overview**

MEvals provides a **command-line interface (CLI) UX** that allows users to authenticate with Microsoft Graph and select from their own meetings. It's not a traditional web UI, but rather an **enterprise-grade authentication and data selection system**.

## 🚀 **How to Run MEvals UX**

### **Step 1: Setup Environment**
```bash
cd /Users/cyl/projects/PromptCoT/MEvals

# For macOS - disable Windows Broker
export MSAL_DISABLE_BROKER=1

# Ensure Python dependencies
pip install "msal[broker]>=1.20,<2" requests
```

### **Step 2: Run Meeting Selection Interface**

#### **Basic Meeting Retrieval (Next 7 days)**
```bash
python step1_get_meeting_list.py 7
```

#### **Custom Date Range**
```bash
# Specific start/end dates
python step1_get_meeting_list.py 2025-10-01T00:00:00 2025-10-31T23:59:59

# Last 30 days + next 14 days
python step1_get_meeting_list.py 44
```

#### **Advanced Options**
```bash
# Limit to 100 meetings max
python step1_get_meeting_list.py 30 --max-events 100

# Custom filters (exclude specific meeting types)
python step1_get_meeting_list.py 14 --filter "(isCancelled eq false) and (showAs ne 'oof')"

# Select specific meeting metadata
python step1_get_meeting_list.py 7 --select "id,subject,start,end,organizer"
```

## 🔐 **Authentication Flow**

### **What Happens When You Run MEvals:**

1. **🌐 Browser Launch**: MEvals opens your default browser
2. **🔐 Microsoft Login**: Standard Microsoft 365 organizational login
3. **✅ Consent Screen**: Permission request for calendar access
4. **🎟️ Token Storage**: Secure token caching for future runs
5. **📊 Data Retrieval**: Automatic meeting list fetching and export

### **Authentication Example:**
```bash
# First run - will trigger authentication
python step1_get_meeting_list.py 7

# Output you'll see:
# "Opening browser for authentication..."
# "Please login to your Microsoft account"
# "✅ Authentication successful"
# "📊 Fetched 25 meetings from your calendar"
# "💾 Exported to out/meetings-20251009134500.csv"
```

## 🎛️ **Meeting Selection Features**

### **Date Range Selection**
- **Days Forward**: `python step1_get_meeting_list.py 14` (next 14 days)
- **Specific Range**: `python step1_get_meeting_list.py 2025-10-01T00:00:00 2025-10-31T23:59:59`
- **Default Range**: Past 30 days + future 30 days if no arguments

### **Meeting Filtering**
- **Exclude Cancelled**: `--filter "(isCancelled eq false)"`
- **Exclude Out-of-Office**: `--filter "(showAs ne 'oof')"`
- **Organizer Filter**: `--filter "(organizer/emailAddress/address eq 'user@microsoft.com')"`

### **Data Export Options**
- **CSV Format**: Meeting list with all metadata
- **JSON Export**: Structured meeting preparation data
- **Custom Fields**: Select specific meeting attributes

## 📊 **Complete MEvals Pipeline**

### **Full Meeting Processing Workflow:**
```bash
# Step 1: Get meeting list (Interactive UX)
python step1_get_meeting_list.py 30

# Step 2: Generate meeting prep summaries
python step2_generate_meeting_prep.py

# Step 3: Extract GPT requests from summaries
python step3_extract_gpt_requests.py

# Step 4: Extract context variables
python step4_extract_context_variables.py

# Step 5: Render from context
python step5_render_from_context.py

# Step 6: Generate LLM responses
python step6_generate_llm_responses.py
```

### **One-Command Pipeline (PowerShell on Windows):**
```powershell
# Complete pipeline with auto-setup
pwsh .\run_all.ps1 -AutoSetup -Force -V4 -Days 30

# macOS equivalent (manual steps)
./run_all_macos.sh  # If we create this wrapper
```

## 🔗 **Integration with Meeting PromptCoT**

### **Convert MEvals Data to Meeting PromptCoT Format:**
```bash
# After running MEvals pipeline
cd /Users/cyl/projects/PromptCoT

# Convert to our format
python mevals_promptcot_bridge.py \
  --mevals-data MEvals/data/meeting_prep.prompt.samples \
  --output meeting_prep_real_data \
  --min-quality 0.8

# Launch our UX interface
./launch_data_explorer.sh
```

## 🎯 **Real Example Workflow**

### **Complete User Journey:**
```bash
# 1. Authenticate and select meetings
cd MEvals
export MSAL_DISABLE_BROKER=1
python step1_get_meeting_list.py 14
# → Browser opens, you login, meetings are fetched

# 2. Process meeting data
python step2_generate_meeting_prep.py
# → Meeting prep summaries generated

# 3. Convert to Meeting PromptCoT
cd ..
python mevals_promptcot_bridge.py --mevals-data MEvals/data/meeting_prep.prompt.samples --output real_data

# 4. Explore with our UX
streamlit run meeting_data_explorer.py
# → Beautiful web interface opens at http://localhost:8501
```

## 🌟 **MEvals UX vs Our UX Interface**

### **MEvals Native UX (CLI-based):**
✅ **Enterprise Authentication**: Direct Microsoft Graph integration
✅ **Real Data Access**: Your actual Microsoft 365 meetings  
✅ **Secure & Compliant**: Enterprise-grade security standards
✅ **Flexible Filtering**: Advanced OData query capabilities
✅ **Batch Processing**: Handle hundreds of meetings efficiently

### **Our Enhanced UX (Web-based):**
✅ **Visual Exploration**: Interactive charts and graphs
✅ **Quality Analysis**: Professional evaluation metrics visualization
✅ **Pattern Discovery**: Meeting type and organizer analysis
✅ **Export Capabilities**: CSV and report generation
✅ **User-Friendly**: Point-and-click data exploration

## 🎉 **Summary: Two Complementary UX Systems**

### **MEvals UX: Data Collection Interface**
- **Purpose**: Authenticate and select real Microsoft meetings
- **Interface**: Command-line with browser authentication
- **Output**: Raw meeting data and processing pipeline
- **Users**: Data scientists, developers, enterprise users

### **Meeting PromptCoT UX: Data Analysis Interface**  
- **Purpose**: Visualize and explore processed meeting data
- **Interface**: Modern web dashboard with interactive charts
- **Output**: Insights, patterns, and exportable reports
- **Users**: Product managers, researchers, stakeholders

---

## 🔧 **Quick Start Commands**

```bash
# Test MEvals authentication
cd MEvals && python step1_get_meeting_list.py 1

# Full MEvals pipeline  
python step1_get_meeting_list.py 30 && python step2_generate_meeting_prep.py

# Launch our analysis UX
cd .. && streamlit run meeting_data_explorer.py
```

**MEvals provides the enterprise-grade data collection UX, while our interface provides the beautiful data analysis UX!** 🌟