# n8n Workflow: Approval to Outreach Tracker

> Automated workflow that watches a Notion Research Database for CEO/COO-approved fund managers, creates entries in an Outreach Tracker database, and sends email notifications.

---

## Workflow Overview

```
[Watch Research DB] → [Filter Approved Only] → [Extract Fund Details] → [Create Outreach Entry] → [Send Email Notification]

[On Workflow Error] → [Log Error Details]
```

**Trigger:** When a fund manager's `Approval Status` changes to "Approved" in the Research Database.

**Actions:**
1. Filters for approved items only (ignores other status changes)
2. Extracts fund manager details into clean variables
3. Creates a new page in the Outreach Tracker database with status "To Contact"
4. Sends a branded HTML email notification with key details

---

## Prerequisites

- [n8n](https://n8n.io/) — self-hosted or cloud (free tier works for demo)
- Notion workspace with two databases (see [`notion_schema.md`](notion_schema.md))
- Notion Internal Integration with access to both databases
- SMTP email credentials (or Gmail OAuth)

---

## Setup

### 1. Create the Notion Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a new integration named **"EU Funding Automation"**
3. Select your workspace and grant **Read content** + **Insert content** + **Update content** capabilities
4. Copy the Internal Integration Secret (starts with `ntn_`)

### 2. Set Up Notion Databases

Follow the schemas in [`notion_schema.md`](notion_schema.md):

1. **Research Database** — import fund managers from `01_data/processed/eif_fund_managers_clean.csv`, add the Approval Status / Reviewed By / Review Date properties
2. **Outreach Tracker** — create empty with all properties defined
3. Share both databases with the "EU Funding Automation" integration (database page → `...` → Add connections)

### 3. Install and Configure n8n

```bash
# Option A: npm (requires Node.js 18+)
npm install n8n -g
n8n start

# Option B: Docker
docker run -it --rm -p 5678:5678 n8nio/n8n
```

Open `http://localhost:5678`.

### 4. Import the Workflow

1. In n8n: Workflows → Import from File → select `workflow_eu_funding_tracker.json`
2. Update placeholder values:
   - `YOUR_RESEARCH_DATABASE_ID` → your Research Database ID (from the Notion URL)
   - `YOUR_OUTREACH_TRACKER_DATABASE_ID` → your Outreach Tracker Database ID
3. Add credentials:
   - **Notion API:** paste the integration secret from step 1
   - **SMTP / Gmail:** configure your email sender
4. Update email addresses in the "Send Email Notification" node

### 5. Activate

Toggle the workflow to **Active**. It will poll the Research Database every minute.

---

## Testing the Workflow

1. Open the Research Database in Notion
2. Select **Suma Capital** (Tier 1, score 8.0)
3. Change `Approval Status` from "Pending Review" to **"Approved"**
4. Set `Reviewed By` to "CEO" and `Review Date` to today
5. Wait up to 1 minute for the polling trigger

**Expected results:**
- A new entry appears in the Outreach Tracker: "Suma Capital — SC Climate Impact Fund III" with status "To Contact"
- An email arrives with fund manager details in the branded template
- The n8n execution log shows green checkmarks on all nodes

Repeat with **Impact Bridge** (Tier 1) to verify multi-record handling.

---

## Workflow Nodes

| # | Node | Type | Purpose |
|---|---|---|---|
| 1 | Watch Research Database | Notion Trigger | Polls for updated pages every 1 min |
| 2 | Filter Approved Only | IF | Passes only `Approval Status == "Approved"` |
| 3 | Extract Fund Details | Set | Maps Notion JSON to clean variables |
| 4 | Create Outreach Entry | Notion | Creates page in Outreach Tracker DB |
| 5 | Send Email Notification | Email Send | Branded HTML email with fund details |
| 6 | On Workflow Error | Error Trigger | Catches and logs any node failures |
| 7 | Log Error Details | Set | Extracts error message, node, and timestamp |

---

## Email Notification

The email uses the project brand palette (Navy `#1B2A4A`, Copper `#B87333`) and includes:
- Fund manager name and priority tier
- Fit score and country
- EIF commitment amount
- Contact email
- Call-to-action: open the Outreach Tracker to assign ownership

---

## File Structure

```
06_n8n/
├── README.md                              ← You are here
├── workflow_eu_funding_tracker.json        ← Importable n8n workflow
├── notion_schema.md                       ← Database property definitions
└── screenshots/                           ← Workflow execution screenshots (for portfolio)
```

---

## Optional Enhancements

- **Update source record** — add a Notion Update node after step 4 to set Research DB `outreach_status` to "Outreach Initiated"
- **Conditional email subject** — "URGENT: Tier 1 Approved" vs "New Tier 2 Approved"
- **Webhook trigger** — add a manual webhook entry point for live demos
- **Duplicate check** — query Outreach Tracker before creating to prevent duplicates
