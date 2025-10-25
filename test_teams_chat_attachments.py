#!/usr/bin/env python3
"""
Test if we can access Teams chat messages and file attachments
"""
import requests
import msal
import json

# Authenticate
TENANT_ID = '72f988bf-86f1-41af-91ab-2d7cd011db47'
CLIENT_ID = '9ce97a32-d9ab-4ab2-aadc-f49b39b94e11'
SCOPES = ['https://graph.microsoft.com/.default']

app = msal.PublicClientApplication(
    CLIENT_ID,
    authority=f'https://login.microsoftonline.com/{TENANT_ID}',
    enable_broker_on_windows=True
)

# Get token (silent or interactive)
accounts = app.get_accounts()
result = app.acquire_token_silent(SCOPES, account=accounts[0] if accounts else None)
if not result:
    print('Authenticating interactively...')
    result = app.acquire_token_interactive(
        SCOPES,
        parent_window_handle=msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE
    )
    if not result or 'access_token' not in result:
        print('Authentication failed!')
        exit(1)

token = result['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Test 1: Get my Teams chats
print('=' * 70)
print('TEST 1: Getting Teams chats...')
print('=' * 70)
url = 'https://graph.microsoft.com/v1.0/me/chats'
response = requests.get(url, headers=headers, params={'$top': 10})
if response.ok:
    chats = response.json().get('value', [])
    print(f'✅ Found {len(chats)} recent chats\n')
    
    # Test 2: Get messages from chats and look for attachments
    print('=' * 70)
    print('TEST 2: Checking for file attachments in chat messages...')
    print('=' * 70)
    
    attachment_count = 0
    messages_checked = 0
    
    for i, chat in enumerate(chats[:5]):  # Check first 5 chats
        chat_id = chat['id']
        chat_type = chat.get('chatType', 'Unknown')
        
        msg_url = f'https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages'
        msg_response = requests.get(msg_url, headers=headers, params={'$top': 20, '$select': 'id,from,attachments,createdDateTime'})
        
        if msg_response.ok:
            messages = msg_response.json().get('value', [])
            messages_checked += len(messages)
            
            for msg in messages:
                attachments = msg.get('attachments', [])
                if attachments:
                    from_user = msg.get('from', {}).get('user', {}).get('displayName', 'Unknown')
                    created = msg.get('createdDateTime', '')
                    
                    for att in attachments:
                        att_name = att.get('name', 'Unknown')
                        att_type = att.get('contentType', 'Unknown')
                        
                        # Check if it's a file (not inline images, etc.)
                        if 'reference' in att or 'application' in att_type or 'document' in att_type.lower():
                            print(f'\n📎 File attachment found:')
                            print(f'   From: {from_user}')
                            print(f'   Name: {att_name}')
                            print(f'   Type: {att_type}')
                            print(f'   Date: {created[:10]}')
                            attachment_count += 1
    
    print(f'\n' + '=' * 70)
    print(f'SUMMARY:')
    print(f'  Messages checked: {messages_checked}')
    print(f'  File attachments found: {attachment_count}')
    print('=' * 70)
    
    # Test 3: Can we identify if WE sent the file?
    print('\n' + '=' * 70)
    print('TEST 3: Checking message sender (from field)...')
    print('=' * 70)
    
    # Get my user info
    me_url = 'https://graph.microsoft.com/v1.0/me'
    me_response = requests.get(me_url, headers=headers, params={'$select': 'displayName,mail,userPrincipalName'})
    if me_response.ok:
        me_data = me_response.json()
        my_name = me_data.get('displayName', '')
        my_email = me_data.get('mail', '') or me_data.get('userPrincipalName', '')
        print(f'Your name: {my_name}')
        print(f'Your email: {my_email}')
        
        # Recheck messages to find ones YOU sent with attachments
        print('\nMessages YOU sent with file attachments:')
        your_attachments = 0
        
        for chat in chats[:5]:
            chat_id = chat['id']
            msg_url = f'https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages'
            msg_response = requests.get(msg_url, headers=headers, params={'$top': 20, '$select': 'id,from,attachments,createdDateTime'})
            
            if msg_response.ok:
                messages = msg_response.json().get('value', [])
                
                for msg in messages:
                    from_user = msg.get('from', {}).get('user', {})
                    from_name = from_user.get('displayName', '')
                    from_email = from_user.get('userPrincipalName', '') or from_user.get('email', '')
                    
                    # Check if YOU sent this message
                    if from_name == my_name or from_email == my_email:
                        attachments = msg.get('attachments', [])
                        if attachments:
                            for att in attachments:
                                att_name = att.get('name', 'Unknown')
                                att_type = att.get('contentType', 'Unknown')
                                
                                if 'reference' in att or 'application' in att_type:
                                    print(f'\n  📤 YOU sent: {att_name}')
                                    print(f'     Type: {att_type}')
                                    print(f'     Date: {msg.get("createdDateTime", "")[:10]}')
                                    
                                    # Get chat members to see who you shared with
                                    members_url = f'https://graph.microsoft.com/v1.0/me/chats/{chat_id}/members'
                                    members_response = requests.get(members_url, headers=headers)
                                    if members_response.ok:
                                        members = members_response.json().get('value', [])
                                        recipients = [m.get('displayName', '') for m in members if m.get('displayName') != my_name]
                                        print(f'     Shared with: {", ".join(recipients)}')
                                    
                                    your_attachments += 1
        
        print(f'\n✅ Found {your_attachments} files YOU shared in Teams chats')
        
else:
    print(f'❌ Failed: {response.status_code} - {response.text[:200]}')
