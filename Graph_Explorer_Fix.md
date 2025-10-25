# Microsoft Graph Explorer - Working URLs

## 🔧 URL Encoding Issue Fixed

The Graph Explorer is having trouble with the complex URL. Let's use simpler approaches:

## ✅ Method 1: Simple URLs (Try These in Order)

### URL 1: Basic Events Query
```
https://graph.microsoft.com/v1.0/me/events
```
**What it does**: Gets your recent calendar events (default 10)

### URL 2: More Events
```
https://graph.microsoft.com/v1.0/me/events?$top=100
```
**What it does**: Gets your last 100 calendar events

### URL 3: Ordered Events  
```
https://graph.microsoft.com/v1.0/me/events?$top=100&$orderby=start/dateTime desc
```
**What it does**: Gets 100 events ordered by date (newest first)

## ✅ Method 2: Use Graph Explorer's Query Builder

Instead of pasting URLs, use Graph Explorer's interface:

1. Go to: https://developer.microsoft.com/graph/graph-explorer
2. Sign in with your Microsoft account
3. In the left sidebar, look for **"Sample queries"**
4. Find **"Outlook Mail"** or **"Calendar"** section
5. Click on **"get my events"** or similar
6. Click **"Run Query"**

## ✅ Method 3: Step-by-Step in Graph Explorer

1. **Resource**: Select `me`
2. **Path**: Type `events`
3. **Query Parameters**: 
   - Add `$top` with value `100`
   - Add `$orderby` with value `start/dateTime desc`
4. Click **"Run Query"**

## 🎯 What Success Looks Like

You should see a response starting with:
```json
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users('your-id')/events",
    "value": [
        {
            "subject": "Your Meeting Name",
            "start": {
                "dateTime": "2024-10-09T10:00:00.0000000"
            },
            ...
        }
    ]
}
```

## 🚨 If You Still Get Errors

**Error**: "Possible error found in URL"
**Solution**: Use Method 2 (Query Builder) or Method 3 (Step-by-Step)

**Error**: "Insufficient privileges"
**Solution**: 
1. In Graph Explorer, click "Modify permissions"
2. Find "Calendars.Read" and consent to it
3. Try the query again

**Error**: Empty results
**Solution**: Try the basic URL first: `https://graph.microsoft.com/v1.0/me/events`

## 📋 Quick Start

**Easiest approach**:
1. Go to Graph Explorer
2. Paste this simple URL: `https://graph.microsoft.com/v1.0/me/events?$top=100`
3. If it fails, just use: `https://graph.microsoft.com/v1.0/me/events`
4. Copy the entire JSON response
5. Save as `my_calendar_events.json`
6. Run: `python3 process_manual_calendar.py`