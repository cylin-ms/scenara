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

# Get user info
me_response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers, params={'$select': 'displayName'})
my_name = me_response.json().get('displayName', '')
print(f'Your name: {my_name}\n')

# Search for chats with Mark or Caroline
chats_response = requests.get(
    'https://graph.microsoft.com/v1.0/me/chats',
    headers=headers,
    params={'$top': 100, '$expand': 'members'}
)

chats = chats_response.json().get('value', [])
print(f'Checking {len(chats)} chats for Mark or Caroline...\n')

mark_chats = []
caroline_chats = []

for chat in chats:
    members = chat.get('members', [])
    member_names = [m.get('displayName', '') for m in members if m.get('displayName') != my_name]
    
    for name in member_names:
        if 'Mark' in name or 'mark' in name:
            if chat not in mark_chats:
                mark_chats.append({
                    'chat_id': chat.get('id', ''),
                    'chat_type': chat.get('chatType', ''),
                    'members': ', '.join(member_names)
                })
        if 'Caroline' in name or 'caroline' in name:
            if chat not in caroline_chats:
                caroline_chats.append({
                    'chat_id': chat.get('id', ''),
                    'chat_type': chat.get('chatType', ''),
                    'members': ', '.join(member_names)
                })

print(f'Chats with Mark: {len(mark_chats)}')
for chat in mark_chats[:10]:
    print(f'  - {chat["chat_type"]}: {chat["members"]}')

print(f'\nChats with Caroline: {len(caroline_chats)}')
for chat in caroline_chats[:10]:
    print(f'  - {chat["chat_type"]}: {chat["members"]}')

# Check for file attachments in these chats
print(f'\n{"="*70}')
print('Checking for file attachments YOU sent to Mark or Caroline...')
print(f'{"="*70}\n')

def check_attachments(chats, person_name):
    total_attachments = 0
    for chat_info in chats:
        chat_id = chat_info['chat_id']
        messages_url = f'https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages'
        
        try:
            msg_response = requests.get(messages_url, headers=headers, params={'$top': 50}, timeout=10)
            if not msg_response.ok:
                continue
            
            messages = msg_response.json().get('value', [])
            
            for msg in messages:
                from_info = msg.get('from') or {}
                if not isinstance(from_info, dict):
                    continue
                
                user_info = from_info.get('user') or {}
                from_name = user_info.get('displayName', '')
                
                if from_name != my_name:
                    continue  # Not from you
                
                attachments = msg.get('attachments', [])
                if attachments:
                    for att in attachments:
                        att_type = att.get('contentType', '')
                        att_name = att.get('name', 'Unknown')
                        created = msg.get('createdDateTime', '')
                        
                        if att_type == 'reference' or 'application' in att_type:
                            print(f'  ✓ YOU sent to {person_name}: {att_name}')
                            print(f'    Chat: {chat_info["members"]}')
                            print(f'    Date: {created[:10] if created else "Unknown"}')
                            print()
                            total_attachments += 1
        except Exception as e:
            continue
    
    return total_attachments

if mark_chats:
    mark_att = check_attachments(mark_chats[:5], 'Mark')
    print(f'Total attachments to Mark: {mark_att}\n')

if caroline_chats:
    caroline_att = check_attachments(caroline_chats[:5], 'Caroline')
    print(f'Total attachments to Caroline: {caroline_att}')
