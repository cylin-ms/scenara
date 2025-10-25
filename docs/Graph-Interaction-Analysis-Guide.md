# Microsoft Graph Interaction Analysis Guide (macOS & Windows)

## ✅ Summary of Discussion
We covered:
- How to analyze **interaction between people** using Teams chats, meeting chats, email exchanges, and @mentions.
- Building an **interaction graph** with weighted edges for @mentions.
- Using **Microsoft Graph API** with **delegated permissions** for self-access (your own data only).
- Implementing on **macOS and Windows** using Python or Node.js.
- Ensuring **privacy, compliance, and least privilege**.
- Metrics: volume, reciprocity, latency, centrality, mention frequency.
- Visualization: Power BI dashboards for collaboration health.

---

## ✅ Implementation Guide for macOS & Windows

### 1. App Registration (Entra ID)
- Register an app in Azure AD.
- Redirect URI: `http://localhost:53682` (or use Device Code flow).
- Add **delegated permissions**:
  - `User.Read`
  - `Mail.Read`
  - `Chat.Read`
  - `Calendars.Read`
  - `Files.Read`
  - *(Optional)* `ChannelMessage.Read.All` (requires admin consent).

---

### 2. Install Tools

#### macOS:
```bash
# Install Homebrew if missing
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and dependencies
brew install python@3.11
python3 -m pip install --upgrade pip
pip3 install msal requests python-dateutil keyring
```

#### Windows:
```powershell
# Install Python (from https://www.python.org/downloads/)
# Then install dependencies
pip install --upgrade pip
pip install msal requests python-dateutil keyring
```

---

### 3. Python Script (Device Code + Keychain)

Create `graph_self_tool.py`:
```python
#!/usr/bin/env python3
import sys, json, requests, keyring
from urllib.parse import urlencode
import msal

TENANT = "common"  # or your tenant ID
CLIENT_ID = "<YOUR-APP-CLIENT-ID>"
SCOPES = ["User.Read","Mail.Read","Chat.Read","Calendars.Read","Files.Read"]
AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"
GRAPH = "https://graph.microsoft.com/v1.0"
SERVICE = f"msal_token_{CLIENT_ID}"

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
token_cache = msal.SerializableTokenCache()
cache_blob = keyring.get_password(SERVICE, "cache")
if cache_blob: token_cache.deserialize(cache_blob)
app.token_cache = token_cache

result = app.acquire_token_silent(SCOPES, account=None)
if not result:
    flow = app.initiate_device_flow(scopes=SCOPES)
    print(f"Go to {flow['verification_uri']} and enter code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result: sys.exit("Auth failed")
keyring.set_password(SERVICE, "cache", token_cache.serialize())
headers = {"Authorization": f"Bearer {result['access_token']}"}

def gget(path, select=None, top=25):
    params = {}
    if select: params["$select"] = select
    if top: params["$top"] = str(top)
    url = f"{GRAPH}{path}"
    if params: url += f"?{urlencode(params)}"
    r = requests.get(url, headers=headers); r.raise_for_status()
    return r.json()

# Emails
mail = gget("/me/messages", select="id,subject,from,toRecipients,ccRecipients,receivedDateTime,mentionsPreview", top=50)
email_edges = []
for m in mail.get("value", []):
    src = ((m.get("from") or {}).get("emailAddress") or {}).get("address")
    for field in ("toRecipients","ccRecipients"):
        for r in (m.get(field) or []):
            dst = (r.get("emailAddress") or {}).get("address")
            if src and dst and src != dst:
                email_edges.append({"src":src,"dst":dst,"modality":"email","ts":m["receivedDateTime"]})

# Chats
chats = gget("/me/chats", top=10)
chat_edges = []
for c in chats.get("value", []):
    msgs = gget(f"/chats/{c['id']}/messages", select="id,from,createdDateTime,mentions", top=20)
    for msg in msgs.get("value", []):
        src = (((msg.get("from") or {}).get("user") or {}).get("email"))
        ts = msg.get("createdDateTime")
        for ment in (msg.get("mentions") or []):
            user = (ment.get("mentioned") or {}).get("user")
            if user and src and user.get("email") and user["email"] != src:
                chat_edges.append({"src":src,"dst":user["email"],"modality":"chat_mention","ts":ts})

# Meetings
events = gget("/me/events", select="id,subject,organizer,start,end,attendees", top=10)
mtg_edges = []
for ev in events.get("value", []):
    org = ((ev.get("organizer") or {}).get("emailAddress") or {}).get("address")
    for a in (ev.get("attendees") or []):
        dst = ((a.get("emailAddress") or {}).get("address"))
        if org and dst and org != dst:
            mtg_edges.append({"src":org,"dst":dst,"modality":"meeting","ts":ev["start"]["dateTime"]})

print(json.dumps({"email_edges":email_edges[:5],"chat_edges":chat_edges[:5],"meeting_edges":mtg_edges[:5]}, indent=2))
```

Run:
```bash
python3 graph_self_tool.py   # macOS
python graph_self_tool.py    # Windows
```

---

### 4. Node.js PKCE Flow (Local Web App)
```bash
npm init -y
npm i @azure/msal-node-express express node-fetch
```

Create `server.js`:
```javascript
const express = require("express");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { msalExpressWrapper } = require("@azure/msal-node-express");

const app = express();
const msal = new msalExpressWrapper({
  auth: { clientId: "YOUR-APP-CLIENT-ID", authority: "https://login.microsoftonline.com/common" }
}, {
  authRoutes: { redirect: "/", error: "/error", unauthorized: "/unauthorized" },
  protectedRoutes: { "/me": ["User.Read"], "/mail": ["Mail.Read"], "/chats": ["Chat.Read"] }
});

app.use(msal.router);
app.get("/", (req,res)=>res.send('/signinSign in</a>'));
app.get("/me", msal.guard, async (req,res)=>{
  const token=req.session.protectedResources["/me"].accessToken;
  const r=await fetch("https://graph.microsoft.com/v1.0/me",{headers:{Authorization:`Bearer ${token}`}});
  res.send(await r.json());
});
app.listen(3000,()=>console.log("http://localhost:3000"));
```

Run:
```bash
node server.js
```

---

### 5. Power BI Schema for Visualization
Export edges as CSV:
```
src,dst,modality,timestamp,weight
alice@contoso.com,bob@contoso.com,email,2025-10-24T10:00Z,1
alice@contoso.com,charlie@contoso.com,chat_mention,2025-10-24T11:00Z,3
```

**Power BI Model**:
- **Tables**: `Edges`, `Users`.
- **Relationships**: `Edges.src` → `Users.email`, `Edges.dst` → `Users.email`.
- **Visuals**:
    - Matrix: interaction counts by modality.
    - Network chart: nodes sized by degree, edges weighted by mentions.
    - KPI cards: latency, reciprocity, cross-team ratio.

---

### 6. Advanced Analytics (NetworkX + Fabric)
#### Local Python (NetworkX)
```python
import networkx as nx
import pandas as pd

edges = pd.read_csv("edges.csv")
G = nx.from_pandas_edgelist(edges, source="src", target="dst", edge_attr=True, create_using=nx.DiGraph())

# Centrality
degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
print(sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10])
```

#### Microsoft Fabric Notebook
- Load edge lists into **Lakehouse** (Delta/Parquet).
- Compute rolling snapshots and persist metrics for Power BI.

---

### 7. Graph Data Connect (Large-Scale, Enterprise Exports)
**Why use it:** For historical, at-scale datasets across Exchange, Teams, SharePoint with **governed** movement into Azure Data Lake.

**Steps:**
1. Approvals & governance (Purview, DPIA).
2. Azure subscription & ADLS Gen2 setup.
3. Enable Graph Data Connect in M365 admin center.
4. Select datasets (Exchange, Teams, SharePoint).
5. Provision pipelines (Synapse, Databricks, Fabric).
6. Model fact/dimension tables.
7. Compute metrics & snapshots.
8. Apply RBAC and audit logs.

**Schema example:**
```sql
CREATE TABLE fact_email_edges (...);
CREATE TABLE fact_chat_edges (...);
CREATE TABLE fact_meeting_edges (...);
```

---

### ✅ Next Steps
- Confirm app registration and scopes.
- Run Python script on macOS or Windows.
- Export edges → NetworkX or Fabric for analytics.
- For scale: use Graph Data Connect + Power BI dashboards.