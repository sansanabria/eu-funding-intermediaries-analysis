# Research Methodology

## Objective

Identify, curate, and analyze EIF-backed financial intermediaries available through the European Commission's Access to EU Finance portal, with the goal of matching funding opportunities to specific company projects in clean energy, green hydrogen, and desalination.

---

## Research Process

### Phase 1 — Source Identification
- Identified the European Commission's financial intermediaries portal as the primary data source
- URL: https://youreurope.europa.eu/business/finance-funding/getting-funding/access-finance/en/
- Confirmed data is publicly available and reusable under EC reuse policy

### Phase 2 — Data Collection
- Applied filters on the portal: geographic scope (Spain, Portugal, Sweden, Global), fund type, and sustainability focus
- Manually reviewed each intermediary profile for relevance to target projects
- Recorded structured data across 13 fields per intermediary
- Data collected: March 2025

### Phase 3 — Data Structuring
- Organized raw data into a structured Excel workbook
- Defined consistent field names and value formats
- Identified and flagged missing or ambiguous data points

### Phase 4 — Analysis
- Cleaned and transformed data using Python (pandas)
- Performed exploratory data analysis to identify patterns, gaps, and clusters
- Built a scoring model to rank fund managers by fit with target projects

### Phase 5 — Framework Design
- Designed a 7-step decision framework for companies to self-assess funding eligibility
- Framework mirrors the portal's filter logic for direct applicability
- Documented in `docs/decision_framework.md`

### Phase 6 — Analysis Reports
- Translated analysis into audience-specific deliverables:
  - Executive summary (CEO/COO)
  - Outreach tracker (operational managers)
  - Power BI dashboard (leadership and analysts)

---

## Data Quality Notes

- Data was collected manually from a dynamic JavaScript-rendered portal
- Some fields (e.g., EIF commitment amounts) were not available for all intermediaries
- Contact information was verified against fund manager websites where possible
- Fund mandates and focus areas may change — data should be refreshed periodically

---

## Tools Used

| Tool | Purpose |
|---|---|
| Python (pandas) | Data cleaning, EDA, scoring model |
| Jupyter Notebooks | Analysis documentation and narrative |
| Power BI Desktop | Interactive dashboard and visualization |
| Excel | Raw data collection, opportunity matrix, outreach tracker |
| GitHub | Version control and portfolio publication |
