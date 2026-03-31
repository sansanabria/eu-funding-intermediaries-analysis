# Notion Database Schemas

Two Notion databases power this workflow. The **Research Database** holds all fund manager research; the **Outreach Tracker** receives approved items automatically via n8n.

---

## Research Database

Source of truth for all researched EIF-backed fund managers. Populated from `01_data/processed/eif_fund_managers_clean.csv`.

| Property | Type | Options / Format | Notes |
|---|---|---|---|
| Fund Manager | Title | — | Clean names (see `NAME_MAP` in `generate_outreach_import.py`) |
| Country | Select | Spain, Portugal, Sweden, Global, Spain & Portugal, Worldwide & Spain, Sweden & Nordic | From `country_primary` |
| Fund Type | Select | VC, PE, Debt, Infrastructure | From `fund_type` |
| Priority Tier | Select | Tier 1 - Priority, Tier 2 - Secondary, Tier 3 - Monitor | From `priority_tier` |
| Fit Score | Number | 1 decimal, range 0–10 | From `fit_score_10` |
| EIF Commitment (EUR) | Number | EUR currency format | From `eif_commitment_eur` |
| Solar Fit | Checkbox | — | Boolean flag |
| Hydrogen Fit | Checkbox | — | Boolean flag |
| Desalination Fit | Checkbox | — | Boolean flag |
| SDG Tags | Multi-select | SDG 6, SDG 7, SDG 9, SDG 13, SDG 14 | From `sdg_tags` |
| Financial Product | Rich text | — | Fund product description |
| Approach Strategy | Rich text | — | How to contact/pitch |
| Website | URL | — | |
| Email | Email | — | |
| Phone | Phone | — | |
| **Approval Status** | **Select** | **Pending Review, Approved, Rejected, On Hold** | **n8n trigger property** |
| Reviewed By | Rich text | — | Simulated: "CEO" or "COO" |
| Review Date | Date | — | Date the status was changed |

### Import steps

1. Run `python 05_analysis_reports/generate_outreach_import.py` to generate the CSV
2. In Notion: New database → Import → upload `outreach_tracker_import.csv`
3. Add the extra properties manually: Approval Status, Reviewed By, Review Date
4. Set all records to `Approval Status: Pending Review`

---

## Outreach Tracker Database

Operational tracking database. Entries are created automatically by n8n when research items are approved.

| Property | Type | Options / Format | Auto-populated by n8n? |
|---|---|---|---|
| Program Name | Title | Fund Manager + Financial Product | Yes |
| Status | Select | To Contact, In Progress, Applied, Closed Won, Closed Lost | Yes (default: "To Contact") |
| Priority Tier | Select | Tier 1 - Priority, Tier 2 - Secondary, Tier 3 - Monitor | Yes |
| Fit Score | Number | 1 decimal, range 0–10 | Yes |
| Country | Select | Same options as Research DB | Yes |
| Contact Email | Email | — | Yes |
| Contact Phone | Phone | — | Yes |
| Website | URL | — | Yes |
| Deadline | Date | — | No (filled manually) |
| Assigned To | Person | — | No (assigned manually) |
| Next Action | Rich text | — | No |
| Notes | Rich text | — | No |
| Created By Automation | Checkbox | — | Yes (always `true`) |
| Source Record | URL | — | Yes (link to Research DB page) |

### Setup steps

1. Create a new empty database in Notion with the properties above
2. Do **not** populate it manually — n8n fills it when opportunities are approved
3. Share the database with the "EU Funding Automation" integration

---

## Status Flow

```
Research Database                    Outreach Tracker
┌──────────────────┐                 ┌──────────────────┐
│  Pending Review   │                 │                  │
│        ↓          │   n8n trigger   │                  │
│    Approved    ───────────────────→ │   To Contact     │
│        ↓          │                 │       ↓          │
│    (archived)     │                 │   In Progress    │
│                   │                 │       ↓          │
│    Rejected       │                 │   Applied        │
│    On Hold        │                 │       ↓          │
│                   │                 │  Closed Won/Lost │
└──────────────────┘                 └──────────────────┘
```
