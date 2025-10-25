#!/bin/bash
# Microsoft Graph Environment Variables
# Set these with your actual values from Azure app registration

export MICROSOFT_CLIENT_ID="your-client-id-here"
export MICROSOFT_CLIENT_SECRET="your-client-secret-here"  
export MICROSOFT_TENANT_ID="your-tenant-id-here"

# To use this script:
# 1. Replace the placeholder values with your actual values
# 2. Run: source setup_env.sh
# 3. Verify: echo $MICROSOFT_CLIENT_ID

echo "✅ Microsoft Graph environment variables set"
echo "🔧 Client ID: $MICROSOFT_CLIENT_ID"
echo "🏢 Tenant ID: $MICROSOFT_TENANT_ID"
echo "🔐 Secret: [HIDDEN]"
