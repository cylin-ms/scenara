# Step-by-Step Guide: Meeting PromptCoT Setup

## 🚀 Complete Setup Guide (15 minutes)

### Prerequisites Check
Before starting, make sure you have:
- ✅ Python 3.8+ installed
- ✅ Internet connection
- ✅ Microsoft account with calendar access
- ✅ VS Code or terminal access

---

## Step 1: Verify Your Environment (2 minutes)

Open terminal in the PromptCoT directory and check dependencies:

```bash
cd /Users/cyl/projects/PromptCoT
python --version
```

**Expected output:**
```
Python 3.x.x
```

Install required packages:
```bash
pip install requests streamlit plotly pandas seaborn
```

---

## Step 2: Extract Real Meeting Data (5 minutes)

Run the Graph API client to get 100+ meetings:

```bash
python meeting_graph_client.py
```

### What happens:
1. **Authentication prompt appears**
2. **Browser opens automatically** to Microsoft login
3. **Enter the device code** shown in terminal
4. **Sign in with your Microsoft account**
5. **Calendar data extraction begins**

### Expected interaction:
```
🔐 Authenticating with Microsoft Graph...
📱 Please visit: https://microsoft.com/devicelogin
🔢 Enter code: ABC123DEF
🌐 Opening browser automatically...
⏳ Waiting for authentication (you have 15 minutes)...
✅ Authentication successful!
✅ Connected as: Your Name (your.email@company.com)

📅 Fetching calendar events from last 90 days (targeting 100+ meetings)...
📥 Fetching page 1 (events 1-50)...
✅ Retrieved 50 events from this page (Total: 50)
📥 Fetching page 2 (events 51-100)...
✅ Retrieved 50 events from this page (Total: 100)
📥 Fetching page 3 (events 101-150)...
✅ Retrieved 45 events from this page (Total: 145)

🎯 Final result: Retrieved 145 calendar events
✅ SUCCESS: Got 145 meetings (target: 100+)
🎉 SUCCESS: Extracted 145 meetings (target achieved!)
```

### If you get fewer than 100 meetings:
Don't worry! The system will guide you to supplement with synthetic data.

---

## Step 3: Combine All Data Sources (1 minute)

Merge your real meeting data with any existing scenarios:

```bash
python update_training_data.py
```

### Expected output:
```
🔄 Updating Meeting PromptCoT Training Data
📂 Loaded 145 Graph API scenarios
📂 Enhanced data not found (skipping)
💾 Saved 145 training scenarios to meeting_prep_data/training_scenarios.json

📊 Dataset Summary:
Total scenarios: 145
Average quality score: 8.40/10.0
High quality scenarios (8.0+): 118
```

---

## Step 4: Launch the Data Explorer (2 minutes)

Start the web interface to explore your data:

```bash
streamlit run meeting_data_explorer.py
```

### Expected output:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.xxx:8501
```

**Your browser will automatically open to http://localhost:8501**

---

## Step 5: Explore Your Meeting Data (5 minutes)

### Interface Overview:
Navigate through the 6 tabs in your web interface:

#### 📈 **Overview Tab**
- Dataset summary with key metrics
- Data source distribution charts
- Meeting type breakdown
- Quality score analysis

#### 📋 **Training Data Tab**
- Browse all 145+ meeting scenarios
- Search and filter capabilities
- Detailed scenario viewer
- Preparation requirements analysis

#### 📅 **Real Meetings Tab**
- Your actual calendar events
- Meeting timeline visualization
- Attendee analysis
- Business context insights

#### 🔍 **Quality Analysis Tab**
- Quality score distribution
- Complexity analysis charts
- Business effectiveness metrics
- Meeting type performance

#### 💾 **Export Tab**
- Download JSON data
- Export CSV files
- Training data packages
- Integration guides

---

## 🎯 Success Checklist

After completing all steps, you should have:

- ✅ **100+ real meeting scenarios** extracted from your calendar
- ✅ **Professional web interface** running at http://localhost:8501
- ✅ **Rich business context** with attendees, complexity, and preparation insights
- ✅ **High quality data** with 8.0+ average effectiveness scores
- ✅ **Meeting intelligence** across different business scenarios

---

## 🔧 Troubleshooting

### Problem: "Authentication failed"
**Solution:**
```bash
# Check internet connection
ping microsoft.com

# Try authentication again
python meeting_graph_client.py
```

### Problem: "Fewer than 100 meetings found"
**Solution:**
```bash
# Add synthetic scenarios to reach 100+
python meeting_data_enhancer.py

# Combine all data
python update_training_data.py
```

### Problem: "Streamlit won't start"
**Solution:**
```bash
# Install streamlit
pip install streamlit

# Check if port is available
lsof -i :8501

# Start with different port if needed
streamlit run meeting_data_explorer.py --server.port 8502
```

### Problem: "No calendar access"
**Solution:**
- Make sure you're signed into the correct Microsoft account
- Check that your account has calendar events
- Verify calendar permissions in your Microsoft account settings

---

## 🚀 Quick Commands Summary

For future use, here's the complete command sequence:

```bash
# Extract real meetings (run weekly for updates)
python meeting_graph_client.py

# Add synthetic data (optional, for more variety)
python meeting_data_enhancer.py

# Combine all data sources
python update_training_data.py

# Launch data explorer
streamlit run meeting_data_explorer.py
```

---

## 📊 What You'll See

### Sample Data Explorer Interface:
```
Meeting PromptCoT Data Explorer
================================

📈 Overview
-----------
Total Scenarios: 145
Data Sources: Graph API (100%), Enhanced (0%)
Average Quality: 8.4/10.0
High Quality (8.0+): 118 scenarios

Top Meeting Types:
• Technical Design Review: 28 meetings
• Team Retrospective: 22 meetings  
• Product Strategy Session: 19 meetings
• Cross-team Collaboration: 18 meetings
• Budget Planning Meeting: 12 meetings
```

### Sample Meeting Scenario:
```
ID: graph_api_AAMkAGVmMDEzMTM4LWZmMzEtNGI4...
Subject: Q4 Product Strategy Review
Type: Product Strategy Session
Complexity: High
Quality Score: 8.7/10.0

Context:
• Attendees: 8 people (Product, Engineering, Marketing)
• Duration: 120 minutes
• Online: Yes (Microsoft Teams)
• Importance: High

Preparation Requirements:
• Review Q3 performance metrics
• Prepare competitive analysis
• Gather customer feedback summary
• Coordinate cross-team deliverables
```

---

## 🎯 Next Steps

Once your system is running:

1. **Weekly Updates**: Run `python meeting_graph_client.py` weekly to get new meetings
2. **Data Analysis**: Use the Quality Analysis tab to understand your meeting patterns
3. **Export Data**: Use the Export tab to download data for external analysis
4. **Meeting Prep**: Use preparation insights for actual meeting planning

Your Meeting PromptCoT system is now ready to provide intelligent meeting preparation insights! 🚀