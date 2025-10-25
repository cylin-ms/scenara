#!/usr/bin/env python3
"""
Debug Teams chat message access
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

accounts = app.get_accounts()
result = app.acquire_token_silent(SCOPES, account=accounts[0] if accounts else None)
if not result:
    result = app.acquire_token_interactive(
        SCOPES,
        parent_window_handle=msal.application.PublicClientApplication.CONSOLE_WINDOW_HANDLE
    )

token = result['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Get chats
url = 'https://graph.microsoft.com/v1.0/me/chats'
response = requests.get(url, headers=headers, params={'$top': 3})
chats = response.json().get('value', [])

print(f'Found {len(chats)} chats\n')

for i, chat in enumerate(chats[:3]):
    chat_id = chat['id']
    chat_type = chat.get('chatType', 'Unknown')
    topic = chat.get('topic', 'No topic')
    
    print(f'\n{"="*70}')
    print(f'CHAT {i+1}: {topic} ({chat_type})')
    print(f'ID: {chat_id}')
    print(f'{"="*70}')
    
    # Try different approaches to get messages
    print('\nApproach 1: Basic message query')
    msg_url = f'https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages'
    msg_response = requests.get(msg_url, headers=headers, params={'$top': 10})
    print(f'Status: {msg_response.status_code}')
    
    if msg_response.ok:
        messages = msg_response.json().get('value', [])
        print(f'Messages: {len(messages)}')
        
        if messages:
            # Show first message details
            msg = messages[0]
            from_info = msg.get("from") or {}
            user_info = from_info.get("user") or {} if isinstance(from_info, dict) else {}
            print(f'\nFirst message:')
            print(f'  From: {user_info.get("displayName", "System/Unknown")}')
            print(f'  Created: {msg.get("createdDateTime", "")}')
            body_content = msg.get("body", {}).get("content", "") if msg.get("body") else ""
            print(f'  Body preview: {body_content[:100]}')
            print(f'  Attachments: {len(msg.get("attachments", []))}')
            
            if msg.get('attachments'):
                for att in msg.get('attachments', []):
                    print(f'    - {att.get("name", "Unknown")}: {att.get("contentType", "")}')
            
            # Check ALL messages for attachments
            total_attachments = 0
            for m in messages:
                atts = m.get('attachments', [])
                if atts:
                    total_attachments += len(atts)
                    from_msg = m.get("from") or {}
                    user_msg = from_msg.get("user") or {} if isinstance(from_msg, dict) else {}
                    sender = user_msg.get("displayName", "Unknown")
                    print(f'\n  📎 Message with {len(atts)} attachment(s) from {sender}:')
                    for att in atts:
                        print(f'     - {att.get("name", "Unnamed")}: {att.get("contentType", "unknown")}')
            
            if total_attachments > 0:
                print(f'\n  ✅ Total attachments in this chat: {total_attachments}')
    else:
        print(f'Error: {msg_response.text[:200]}')
    
    # Try beta endpoint
    print('\nApproach 2: Beta endpoint')
    msg_url_beta = f'https://graph.microsoft.com/beta/me/chats/{chat_id}/messages'
    msg_response_beta = requests.get(msg_url_beta, headers=headers, params={'$top': 10})
    print(f'Status: {msg_response_beta.status_code}')
    
    if msg_response_beta.ok:
        messages_beta = msg_response_beta.json().get('value', [])
        print(f'Messages: {len(messages_beta)}')
