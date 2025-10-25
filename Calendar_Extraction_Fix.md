# Corrected Microsoft Graph Explorer Instructions

## 🔧 Issue Found
You're getting user profile data instead of calendar events. Let's fix this!

## ✅ Correct Steps for Calendar Data

### Step 1: Open Microsoft Graph Explorer
Go to: https://developer.microsoft.com/graph/graph-explorer

### Step 2: Use the Correct Calendar Query
**IMPORTANT**: Use this URL for calendar events (not the /me endpoint):

```
https://graph.microsoft.com/v1.0/me/events?$top=150&$orderby=start/dateTime desc&$filter=start/dateTime ge '2024-07-01T00:00:00Z'&$select=subject,bodyPreview,start,end,attendees,organizer,isOnlineMeeting,onlineMeetingProvider,location,recurrence,importance,sensitivity
```

### Step 3: What You Should See
The response should look like this:
```json
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users('88573e4b-a91e-4334-89c2-a61178320813')/events(subject,bodyPreview,start,end,attendees,organizer,isOnlineMeeting,onlineMeetingProvider,location,recurrence,importance,sensitivity)",
    "value": [
        {
            "subject": "Team Meeting",
            "bodyPreview": "Weekly team sync...",
            "start": {
                "dateTime": "2024-10-09T10:00:00.0000000",
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": "2024-10-09T11:00:00.0000000",
                "timeZone": "UTC"
            },
            "attendees": [...],
            "organizer": {...},
            "isOnlineMeeting": true,
            ...
        }
    ]
}
```

### Step 4: Common Issues & Solutions

**Problem**: Getting user profile instead of events
**Solution**: Make sure you're using `/me/events` not just `/me`

**Problem**: Empty events array
**Solutions**: 
- Try removing the date filter: `https://graph.microsoft.com/v1.0/me/events?$top=150`
- Check if you have calendar permissions
- Try different date range: `$filter=start/dateTime ge '2024-01-01T00:00:00Z'`

**Problem**: "Insufficient privileges" error
**Solution**: Make sure you've granted Calendar.Read permissions in Graph Explorer

## 🎯 Quick Test URLs

Try these in order until you get calendar data:

1. **Full query** (150 events since July 2024):
   ```
   https://graph.microsoft.com/v1.0/me/events?$top=150&$orderby=start/dateTime desc&$filter=start/dateTime ge '2024-07-01T00:00:00Z'&$select=subject,bodyPreview,start,end,attendees,organizer,isOnlineMeeting,onlineMeetingProvider,location,recurrence,importance,sensitivity
   ```

2. **Simple query** (if the above fails):
   ```
   https://graph.microsoft.com/v1.0/me/events?$top=50
   ```

3. **Minimal query** (just to test access):
   ```
   https://graph.microsoft.com/v1.0/me/events
   ```

## 📋 Next Steps

1. Use the **correct calendar events URL** above
2. Copy the JSON response (should contain "value" array with meeting objects)
3. Save as `my_calendar_events.json`
4. Run: `python3 process_manual_calendar.py`

The key difference is:
- ❌ Wrong: `https://graph.microsoft.com/v1.0/me` (user profile)
- ✅ Correct: `https://graph.microsoft.com/v1.0/me/events` (calendar events)