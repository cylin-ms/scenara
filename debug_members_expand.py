#!/usr/bin/env python3
import requests
import msal

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

# Get first chat with members expanded
chats_url = 'https://graph.microsoft.com/v1.0/me/chats'
response = requests.get(chats_url, headers=headers, params={'$top': 3, '$expand': 'members'})
chats = response.json().get('value', [])

print(f'Found {len(chats)} chats\n')

for i, chat in enumerate(chats[:1]):
    print(f'Chat {i+1}:')
    chat_id = chat.get('id', '')
    print(f'  ID: {chat_id}')
    print(f'  Type: {chat.get("chatType", "")}')
    print(f'  Topic: {chat.get("topic", "No topic")}')
    
    members = chat.get('members', [])
    print(f'  Members: {len(members)}')
    for m in members:
        print(f'    - {m.get("displayName", "Unknown")}')
    
    # Get messages from this chat
    messages_url = f'https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages'
    msg_response = requests.get(messages_url, headers=headers, params={'$top': 50})
    messages = msg_response.json().get('value', [])
    
    print(f'\n  Messages: {len(messages)}')
    
    # Check for attachments
    for msg in messages:
        attachments = msg.get('attachments', [])
        if attachments:
            from_info = msg.get('from', {})
            user_info = from_info.get('user', {}) if isinstance(from_info, dict) else {}
            sender = user_info.get('displayName', 'Unknown')
            
            print(f'\n  Message from {sender} has {len(attachments)} attachment(s):')
            for att in attachments:
                print(f'    - {att.get("name", "Unknown")}: {att.get("contentType", "")}')
