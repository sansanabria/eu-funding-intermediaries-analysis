# Power BI Dashboard Guide

## Overview

The Power BI dashboard (`eif_dashboard.pbix`) provides an interactive visual analysis of the 12 EIF-backed fund managers. It is built on the cleaned dataset from `01_data/processed/eif_fund_managers_clean.csv`.

---

## Setup Instructions

### Step 1 — Prerequisites
- Download and install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
- Have `01_data/processed/eif_fund_managers_clean.csv` available locally

### Step 2 — Connect the Data
1. Open `eif_dashboard.pbix` in Power BI Desktop
2. Go to **Home → Transform Data → Data Source Settings**
3. Update the file path to point to your local copy of `eif_fund_managers_clean.csv`
4. Click **Refresh** to load the data

### Step 3 — Explore the Dashboard
Navigate using the tabs at the bottom of the screen.

---

## Dashboard Pages

### Page 1 — Overview
**Purpose:** Executive summary for CEO/COO audiences

**Visuals:**
- KPI cards: Total fund managers | Total EIF commitments (EUR) | Countries covered | Fund types
- Bar chart: EIF commitment by fund manager
- Donut chart: Distribution by fund type (VC, PE, Debt, Infrastructure)
- Slicer: Filter by country

---

### Page 2 — Country Map
**Purpose:** Geographic distribution of fund managers

**Visuals:**
- Filled map: Fund managers plotted by country
- Table: Country → Fund manager → EIF commitment
- Slicer: Filter by fund type

---

### Page 3 — Fund Type Breakdown
**Purpose:** Understand the financial product landscape

**Visuals:**
- Stacked bar: Fund types by country
- Matrix: Fund manager × Support type
- Card: Average EIF commitment by fund type

---

### Page 4 — SDG Alignment
**Purpose:** Map sustainability coverage and identify gaps

**Visuals:**
- Bar chart: Number of funds aligned to each SDG (SDG 1–17)
- Heatmap: Fund manager × SDG coverage
- Highlight: SDGs with zero or single coverage (gaps)

---

### Page 5 — Project Fit Matrix
**Purpose:** Match company projects to fund managers

**Visuals:**
- Matrix table: Fund manager × Project type (Solar / Hydrogen / Desalination) with fit score
- Conditional formatting: Green = strong fit, Yellow = partial, Red = no fit
- Filter: Select project type to highlight top matches

---

### Page 6 — Outreach Pipeline
**Purpose:** Operational tracker for managers

**Visuals:**
- Table: Fund manager | Contact | Status | Next action | Date
- Status slicer: Not contacted / Contacted / Meeting scheduled / Proposal submitted
- KPI: % of priority funds contacted

> Note: Update the status column in `01_data/processed/eif_fund_managers_clean.csv` to keep this page current.

---

## Screenshots

See the `screenshots/` folder for static previews of each dashboard page:
- `overview_page.png`
- `country_map.png`
- `fund_type_breakdown.png`
- `sdg_alignment.png`
- `project_fit_matrix.png`
- `outreach_pipeline.png`

---

## Publishing (Optional)

To share the dashboard online:
1. Sign in to Power BI Desktop with a Microsoft/work account
2. Click **Home → Publish**
3. Select your workspace
4. Share the link — add it to the main `README.md`
