# Quick Azure App Registration Guide

## ✅ 2-Minute Setup for Graph Collaboration Analysis

### Step 1: Create Azure App (2 minutes)
1. Go to: https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
2. Click "New registration"
3. Name: "Graph Collaboration Analyzer"
4. Account types: "Accounts in any organizational directory and personal Microsoft accounts"
5. Redirect URI: Leave blank for now
6. Click "Register"

### Step 2: Get Client ID
1. Copy the "Application (client) ID" - you'll need this
2. Example: `12345678-1234-1234-1234-123456789abc`

### Step 3: Add Permissions
1. Go to "API permissions" in the left menu
2. Click "Add a permission"
3. Choose "Microsoft Graph" → "Delegated permissions"
4. Search and add these permissions:
   - `User.Read`
   - `Mail.Read`
   - `Chat.Read`  
   - `Calendars.Read`
   - `Files.Read`
5. Click "Add permissions"

### Step 4: Enable Public Client
1. Go to "Authentication" in the left menu
2. Click "Add a platform" → "Mobile and desktop applications"
3. Check "https://login.microsoftonline.com/common/oauth2/nativeclient"
4. Click "Configure"
5. Scroll down to "Advanced settings"
6. Set "Allow public client flows" to "Yes"
7. Click "Save"

### Step 5: Run Analysis
```bash
cd /Users/cyl/projects/Scenara
python tools/simple_graph_analyzer.py
# Enter your Client ID when prompted
```

That's it! The app registration gives you access to all Microsoft Graph APIs for collaboration analysis.

## Why This Approach Works Better
- ✅ **Your own app** - no dependency on Microsoft's public clients
- ✅ **Full control** - you control permissions and settings
- ✅ **No admin consent** - delegated permissions for your own data
- ✅ **Works everywhere** - any Microsoft tenant
- ✅ **Permanent** - won't break like public client IDs

## Security
- The app can only access **your own data** (delegated permissions)
- No one else can use your app without the client ID
- You can delete the app anytime from Azure portal