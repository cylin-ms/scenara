# Scenara Repository Transfer - macOS to Windows DevBox

**Source**: macOS `/Users/cyl/projects/Scenara`  
**Destination**: Windows DevBox `C:\Users\cyl\projects\Scenara` (or your preferred path)

---

## 🎯 Quick Transfer Options

### **Option 1: OneDrive/SharePoint (Recommended - Already Synced?)**

If your projects folder is already in OneDrive:

**On macOS**:
```bash
# Check if Scenara is in OneDrive
ls ~/OneDrive/projects/Scenara
# or
ls ~/Library/CloudStorage/OneDrive*/projects/Scenara
```

**On Windows DevBox**:
```powershell
# Navigate to synced folder
cd C:\Users\cyl\OneDrive\projects\Scenara

# Verify files are there
dir
```

If files sync automatically, you're done! 🎉

---

### **Option 2: Manual Copy via OneDrive**

**On macOS**:
```bash
# Copy entire Scenara to OneDrive
cp -r /Users/cyl/projects/Scenara ~/OneDrive/projects/

# Wait for sync (check OneDrive icon in menu bar)
```

**On Windows DevBox**:
```powershell
# Wait for OneDrive sync to complete
# Files will appear at: C:\Users\cyl\OneDrive\projects\Scenara

# Copy to local DevBox location (faster for development)
xcopy C:\Users\cyl\OneDrive\projects\Scenara C:\projects\Scenara /E /I /H

# Or just work directly from OneDrive location
cd C:\Users\cyl\OneDrive\projects\Scenara
```

---

### **Option 3: Zip and Transfer**

**On macOS**:
```bash
# Create compressed archive
cd /Users/cyl/projects
tar -czf Scenara_checkpoint_20251025.tar.gz Scenara/

# Copy to OneDrive/SharePoint for DevBox access
cp Scenara_checkpoint_20251025.tar.gz ~/OneDrive/
```

**On Windows DevBox**:
```powershell
# Download from OneDrive
# Extract (use 7-Zip or Windows built-in)
tar -xzf Scenara_checkpoint_20251025.tar.gz

# Or use PowerShell
Expand-Archive -Path Scenara_checkpoint_20251025.zip -DestinationPath C:\projects\
```

---

### **Option 4: Git Repository (Best for Long-term)**

If you want proper version control:

**On macOS**:
```bash
cd /Users/cyl/projects/Scenara

# Initialize git if not already done
git init

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
venv/
*.log
.DS_Store
.vscode/
*.ipynb_checkpoints/
data/evaluation_results/*.json
collaborator_discovery_results_*.json
EOF

# Add and commit all files
git add .
git commit -m "Checkpoint: Algorithm v6.0 + Teams Chat Integration Prep"

# Option A: Push to GitHub (private repo)
# Create private repo on GitHub, then:
git remote add origin https://github.com/cyl-microsoft/Scenara.git
git push -u origin main

# Option B: Push to Azure DevOps
# Create project in Azure DevOps, then push
```

**On Windows DevBox**:
```powershell
# Clone from GitHub
git clone https://github.com/cyl-microsoft/Scenara.git
cd Scenara

# Or clone from Azure DevOps
git clone https://dev.azure.com/microsoft/Scenara.git
cd Scenara
```

---

## 📦 What's in the Repository

### Directory Structure:
```
Scenara/
├── .cursorrules                 # Project state and lessons learned
├── tools/
│   ├── collaborator_discovery.py          # Algorithm v6.0 ✅
│   ├── collaborator_feedback_learning.py   # AI feedback system ✅
│   ├── direct_graph_api_extractor.py      # Teams chat collector ✅
│   └── [other tools...]
├── docs/
│   ├── graph_api_chat_permission_request.md
│   ├── register_custom_graph_app.md
│   ├── collaborator_discovery_enhancement_session_summary.md
│   ├── ai_native_feedback_quickstart.md
│   └── [other docs...]
├── data/
│   ├── evaluation_results/
│   │   └── graph_collaboration_analysis_20251025_043301.json
│   └── [other data...]
├── meeting_prep_data/
│   └── real_calendar_scenarios.json
├── config/
├── src/
├── tests/
├── venv/                       # Virtual environment (exclude from transfer)
├── requirements.txt
├── startup.py
├── CHECKPOINT_TEAMS_CHAT_INTEGRATION.md
├── TRANSFER_TO_DEVBOX.txt
└── [other files...]
```

### Size Estimate:
- **Without venv**: ~50-100 MB
- **With venv**: ~500 MB - 1 GB

**Recommendation**: Exclude `venv/` and reinstall packages on DevBox

---

## 🚀 DevBox Setup After Transfer

### 1. Verify Transfer
```powershell
# Navigate to Scenara directory
cd C:\projects\Scenara
# or wherever you copied it

# Check key files exist
dir tools\collaborator_discovery.py
dir .cursorrules
dir CHECKPOINT_TEAMS_CHAT_INTEGRATION.md
```

### 2. Create Virtual Environment
```powershell
# Create new venv on DevBox
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies
```powershell
# Install from requirements.txt
pip install -r requirements.txt

# Or install minimal requirements for this task
pip install msal requests
```

### 4. Verify Python Setup
```powershell
# Check Python version
python --version

# Test imports
python -c "import msal; import requests; print('✅ Dependencies OK')"
```

### 5. Run Teams Chat Data Collection
```powershell
# This should work without Error 530033!
python tools\direct_graph_api_extractor.py
```

**Expected Output**:
```
🚀 Direct Graph API Collaboration Data Extractor
==================================================================
This tool uses device code authentication to collect collaboration data
including Teams chat, without requiring Graph Explorer access.
==================================================================
🔐 Starting authentication...
==================================================================

📱 To sign in:
   1. Open: https://microsoft.com/devicelogin
   2. Enter code: ABC123XYZ
   3. Sign in with your Microsoft account

⏳ Waiting for authentication...
```

✅ **No Error 530033!** DevBox is a managed device.

### 6. Continue Development
```powershell
# Test current algorithm
python tools\collaborator_discovery.py --limit 15

# After chat data collected, integrate into Algorithm v6.1
# (See CHECKPOINT_TEAMS_CHAT_INTEGRATION.md for details)

# Validate results
python tools\collaborator_discovery.py --explain "Vani Soff"
```

---

## 📝 Quick Reference

### Important Files for This Session:
```
✅ tools/collaborator_discovery.py              (Algorithm v6.0)
✅ tools/collaborator_feedback_learning.py       (AI feedback)
✅ tools/direct_graph_api_extractor.py          (Chat collector)
✅ .cursorrules                                  (Project state)
✅ CHECKPOINT_TEAMS_CHAT_INTEGRATION.md         (Session guide)
✅ data/evaluation_results/graph_collaboration_analysis_20251025_043301.json
✅ collaborator_discovery_results_20251025_044815.json
```

### Git Commands (if using version control):
```bash
# On macOS
git status                    # Check what's changed
git add .                     # Stage all files
git commit -m "message"       # Commit
git push origin main          # Push to remote

# On DevBox
git pull origin main          # Get latest changes
git status                    # Verify
```

---

## 🎯 Success Checklist

**On macOS** (Before Transfer):
- ✅ Algorithm v6.0 completed and tested
- ✅ AI feedback system implemented
- ✅ Teams chat extractor configured
- ✅ Documentation complete
- ✅ Local git commit done
- ✅ Repository ready for transfer

**On Windows DevBox** (After Transfer):
- ☐ Repository transferred successfully
- ☐ Virtual environment created
- ☐ Dependencies installed (msal, requests)
- ☐ direct_graph_api_extractor.py runs without Error 530033
- ☐ Teams chat data collected
- ☐ Algorithm v6.1 integration complete
- ☐ Vani Soff ranking validated

---

## 💡 Pro Tips

1. **Exclude Large Files**: Don't need to transfer `venv/`, `__pycache__/`, `*.pyc`
2. **Use OneDrive**: Fastest if already syncing
3. **Git is Best**: For long-term, use git for version control
4. **Test Quickly**: Run `python startup.py` on DevBox to verify platform detection
5. **Keep Synced**: Use OneDrive or git to keep macOS and DevBox in sync

---

## 🔧 Troubleshooting

### If files don't sync:
```powershell
# Check OneDrive status
Get-Process OneDrive

# Restart OneDrive
Stop-Process -Name OneDrive
Start-Process OneDrive
```

### If Python not found:
```powershell
# Check Python installation
where python
python --version

# Install if needed (DevBox should have it)
# Download from python.org or use Microsoft Store
```

### If pip install fails:
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -v msal requests
```

---

**Ready to transfer! Choose your preferred method and continue on DevBox.** 🚀
