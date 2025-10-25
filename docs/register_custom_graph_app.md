# Register Custom Graph API App (5 minutes)

Since Graph Explorer is blocked by your org's tenant policy, we need to register our own app.

## Quick Steps:

### 1. Go to Azure Portal
**URL**: https://portal.azure.com

### 2. Navigate to App Registrations
- Search bar: "App registrations"
- Click "App registrations" service
- Click "+ New registration"

### 3. Register the App
**Name**: `Scenara Collaboration Analyzer`  
**Supported account types**: "Accounts in this organizational directory only"  
**Redirect URI**: Leave blank (we'll use device code flow)

Click **"Register"**

### 4. Note the Application (client) ID
You'll see something like: `12345678-1234-1234-1234-123456789abc`

**COPY THIS ID** - you'll need it in the Python script

### 5. Add API Permissions
- Click "API permissions" in left menu
- Click "+ Add a permission"
- Select "Microsoft Graph"
- Select "Delegated permissions"
- Search and check these permissions:
  - ✅ `User.Read`
  - ✅ `People.Read`
  - ✅ `Calendars.Read`
  - ✅ `Mail.Read`
  - ✅ `Files.Read.All`
  - ✅ `Sites.Read.All`
  - ✅ `Chat.Read` ← **This is the key one!**
  - ✅ `Chat.ReadBasic`
- Click "Add permissions"

### 6. Enable Public Client Flow
- Click "Authentication" in left menu
- Scroll to "Advanced settings"
- Under "Allow public client flows":
  - Toggle "Enable the following mobile and desktop flows:" to **YES**
- Click "Save"

### 7. Use the Client ID
Copy your Application (client) ID and paste it into the Python script:

```python
self.client_id = "YOUR-APP-ID-HERE"  # Replace with your app ID
```

## Why This Works:

- **Your own app** = Not subject to Graph Explorer restrictions
- **Device code flow** = Works on any OS including macOS
- **Chat.Read permission** = You can consent directly since it doesn't require admin approval
- **Same tenant** = Your Microsoft org won't block your own registered app

## Expected Time:
- Registration: 2-3 minutes
- Permission setup: 2 minutes
- **Total: ~5 minutes**

## Next Step:
After registration, update `tools/direct_graph_api_extractor.py` line 24 with your new client ID, then run:

```bash
python tools/direct_graph_api_extractor.py
```

You'll see a device code, visit microsoft.com/devicelogin, enter the code, and authenticate!
