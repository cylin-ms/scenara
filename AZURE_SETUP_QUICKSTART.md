# AZURE APP REGISTRATION QUICK SETUP GUIDE

If you don't have Azure app registration credentials yet, here's how to get them:

## 🔧 Azure Portal Setup (5 minutes)

1. **Go to Azure Portal**: https://portal.azure.com
2. **Navigate to**: Azure Active Directory → App registrations 
3. **Click**: "New registration"
4. **Fill out**:
   - Name: "Meeting Intelligence Calendar Access"
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: Leave blank for now
5. **Click**: "Register"

## 📋 Get Required Information

After registration, you'll need these 3 values:

### 1. Application (Client) ID
- Found on the app's "Overview" page
- Copy this value

### 2. Directory (Tenant) ID  
- Also on the "Overview" page
- Copy this value

### 3. Client Secret
- Go to "Certificates & secrets" 
- Click "New client secret"
- Description: "Calendar Access Secret"
- Expires: 24 months
- Click "Add"
- **COPY THE VALUE IMMEDIATELY** (it won't show again)

## 🔑 API Permissions

1. Go to "API permissions"
2. Click "Add a permission"
3. Select "Microsoft Graph"
4. Choose "Application permissions"
5. Add these permissions:
   - `Calendars.Read`
   - `User.Read.All`
6. Click "Grant admin consent for [your organization]"

## ✅ Ready to Use

Once you have:
- ✅ Client ID (Application ID)
- ✅ Tenant ID (Directory ID) 
- ✅ Client Secret
- ✅ Admin consent granted

You can run the real calendar integration!

---

**Need Help?** The script will walk you through entering these values interactively.