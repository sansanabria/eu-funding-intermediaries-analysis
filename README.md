# EU Funding Intermediaries Analysis

> How publicly available EU funding data was transformed into a structured decision framework for management to identify, evaluate, and prioritize fund managers aligned with company projects.

**Data source:** [European Commission — Access to EU Finance Portal](https://youreurope.europa.eu/business/finance-funding/getting-funding/access-finance/en/financial-intermediaries)
**EIF intermediary list (PDF):** [InvestEU Equity Visibility Report](https://www.eif.org/files/calls/ieu-equity-visibility-report-financial-intermediaries.pdf)
**Data collected:** March 2025

---

## The Business Problem

The European Investment Fund (EIF) backs hundreds of financial intermediaries across 27 EU member states — venture capital, private equity, infrastructure, and debt funds that channel EU capital into companies and projects. This data is publicly available through the European Commission's portal.

The challenge: **the portal lets companies filter by country and sector, but the result is a flat list — not a strategy.** It provides no scoring, no prioritisation, and no guidance on which fund managers are the best fit for a company's specific projects, how to approach them, or in what order.

---

## What Data Was Available

The EU portal and EIF publish structured intermediary data including:

- **152 financial intermediaries** across all EU/EEA countries (extracted from the [EIF PDF report](https://www.eif.org/files/calls/ieu-equity-visibility-report-financial-intermediaries.pdf))
- Fund manager name, country, fund type (VC, PE, Debt, Infrastructure)
- EIF commitment amounts (ranging from €2.8M to €51.7M per intermediary)
- Target sectors, SDG alignment, and investment focus areas
- Basic contact details (address, website)

For this analysis, the data was filtered and scored for **three project types — solar energy, green hydrogen, and desalination — across Spain, Portugal, and Sweden**, resulting in 12 relevant intermediaries. However, **the same approach can be reused for any combination of projects, sectors, and countries** covered by the EIF portfolio.

For these 12 shortlisted intermediaries, **additional contact research was conducted manually** (email, phone, key contacts) to identify specific points of contact relevant to solar, hydrogen, and desalination projects. This step can be fully automated in the future by scraping fund manager websites for contact details. Companies replicating this approach should first prioritise their intermediaries through the scoring pipeline, then conduct targeted contact research for their top-tier matches.

---

## How the Data Was Analyzed

The following analysis was performed for solar, hydrogen, and desalination projects in Spain, Portugal, and Sweden. Each step is configurable — the same pipeline can be re-run for different project types and locations by adjusting the filter and scoring parameters.

### 1. Data extraction and cleaning
Raw intermediary data was parsed from the EU portal and EIF PDF reports, standardized into a consistent format, and enriched with project-fit flags based on each fund's stated mandate and SDG alignment.

### 2. Strategic scoring model
Each fund manager was scored out of 10 using weighted criteria that reflect what matters for decision-making:

| Criterion | Weight | Why It Matters |
|---|---|---|
| Project fit | 3 pts | Does the fund explicitly cover the target project types? |
| EIF commitment size | 2 pts | Larger commitments signal stronger fund capacity |
| SDG alignment | 2 pts | Required by impact funds — determines eligibility |
| Contact availability | 2 pts | Does the fund have publicly available contact channels beyond the portal listing? |
| Geographic match | 1 pt | Preference for target countries and markets |

### 3. Gap analysis
Identified where funding coverage is strong, weak, or absent — so management knows where to invest outreach effort and where alternative funding routes are needed.

### 4. Priority tiering
Fund managers were grouped into actionable tiers:
- **Tier 1 (score >= 7):** Approach immediately — strong fit, high EIF commitment
- **Tier 2 (score >= 4):** Approach in 30–90 days — partial fit, requires tailored pitch
- **Tier 3 (score < 4):** Monitor — low fit or limited access

### 5. Approval-to-outreach automation (n8n + Notion)
An [n8n workflow](06_n8n/workflow_eu_funding_tracker.json) automates the handoff from analysis to action. Fund managers are loaded into a Notion Research Database where CEO/COO can review and approve them. When a fund manager is approved, the workflow automatically creates an entry in an Outreach Tracker database and sends a branded email notification with fund details and next steps. See [`06_n8n/README.md`](06_n8n/README.md) for setup.

---

## What Management Can Decide With This

### Which fund managers to approach first

| Priority | Fund Manager | Score | Why |
|---|---|---|---|
| **Immediate** | Suma Capital | 8/10 | Covers solar + hydrogen + desalination. €41.25M EIF commitment. Highest overall fit. |
| **Immediate** | Impact Bridge (Global) | 7/10 | Debt/hybrid products. SDG 6, 7, 9 alignment. Requires impact metrics. |
| **Short term** | Axon Partners | 6/10 | Deep tech + energy transition. Solar and water treatment. |
| **Short term** | OXY Capital | 5.5/10 | Portugal-specific. Solar + hydrogen. PE and mezzanine debt. |
| **Medium term** | Alantra | 5/10 | Pan-European solar energy fund. 1,665 MWp capacity. |
| **Medium term** | NIAM | 4/10 | Largest EIF commitment (€51.7M). Nordic infrastructure scale. |

Full timeline and contact details: [`04_business_analysis/strategic_recommendations.md`](04_business_analysis/strategic_recommendations.md)

### Where the gaps are

| Gap | Severity | What It Means for Decisions |
|---|---|---|
| No fund explicitly covers desalination | Medium-High | Must pitch through SDG framing (water/sanitation), not technology |
| No single fund covers hydrogen alone | Medium | Need multi-fund strategy with tailored pitches per fund type |
| Limited early-stage/startup funding | Medium | Only 2 of 12 funds target startups — consider accelerator route |
| Geographic concentration in Iberia | Low | Dataset covers Spain well but needs expansion for other markets |

Full analysis: [`04_business_analysis/gap_analysis.md`](04_business_analysis/gap_analysis.md)

### What to prepare before outreach

1. **Company overview + project portfolio** — required for all Tier 1 and Tier 2 approaches
2. **SDG impact measurement deck** — required by Impact Bridge and Norrsken before they evaluate
3. **Portugal-specific project brief** — required for OXY Capital
4. **Three hydrogen pitch variants** — infrastructure (Suma), impact/SDG (Impact Bridge), tech (Axon)

---

## Key Findings

See [`INSIGHTS.md`](INSIGHTS.md) for the full analysis. Highlights:

- **Solar energy has the broadest coverage** — 9 of 12 fund managers explicitly target solar, giving the company multiple competing options
- **Desalination must be pitched through SDGs, not technology** — no fund lists it directly, but SDG 6 (Clean Water) and SDG 14 (Life Below Water) provide the entry point
- **Impact funds require measurable SDG data** — approaching without it is a non-starter
- **Nordic funds operate at larger ticket sizes** — NIAM's €51.7M commitment is suited for infrastructure-scale projects, not early-stage

---

## Deliverables

| Deliverable | Audience | What It Contains |
|---|---|---|
| [Executive Summary (PDF)](05_analysis_reports/executive_summary.pdf) | CEO / COO | 1-page dashboard: key metrics, rankings, top recommendations |
| [Outreach Tracker (PDF)](05_analysis_reports/outreach_tracker.pdf) | Operations / BD | Fund manager contact details, status tracking, next actions |
| [Pitch Deck (PDF)](05_analysis_reports/pitch_deck.pdf) | External / investors | Company positioning for fund manager presentations |
| [Strategic Recommendations](04_business_analysis/strategic_recommendations.md) | Leadership | Prioritized 30/60/90/180-day action plan |
| [Gap Analysis](04_business_analysis/gap_analysis.md) | Strategy team | Where coverage is weak and what to do about it |
| [Decision Framework](docs/decision_framework.md) | Any company | 7-step guide to determine EU funding eligibility |
| [n8n Workflow](06_n8n/workflow_eu_funding_tracker.json) | Operations | Approval-to-outreach automation with Notion + email notifications |

---

## Replicable Approach

This analysis is a **template that can be adapted to any industry, project type, or country combination**. The EU portal covers all 27 member states across every sector the EIF supports.

To replicate for a different company or focus area:

| What to change | Where |
|---|---|
| Target countries | `00_filter_intermediaries.py --country` flag |
| Target sectors | `SECTOR_KEYWORDS` dict in `00_filter_intermediaries.py` |
| Project fit criteria | Scoring weights in `03_strategic_scoring.py` |
| SDG alignment targets | SDG flags in the scoring model |

**Example adaptations:**
- A biotech company targeting Germany, France, and the Netherlands
- An agri-tech startup focused on Nordic and Baltic countries
- A circular economy venture targeting Southern Europe

### Quick start
```bash
pip install -r requirements.txt

# Parse the full EIF intermediary list (152 records across all EU countries)
python 02_python_analysis/00_parse_eif_pdfs.py

# Filter for your country and sector
python 02_python_analysis/00_filter_intermediaries.py --country Germany --sector biotech
python 02_python_analysis/00_filter_intermediaries.py --list-countries
python 02_python_analysis/00_filter_intermediaries.py --list-sectors

# Run the scoring and analysis pipeline
python 02_python_analysis/01_data_cleaning.py
python 02_python_analysis/02_exploratory_analysis.py
python 02_python_analysis/03_strategic_scoring.py
```

---

## Repository Structure

```
eu-funding-intermediaries-analysis/
│
├── 01_data/
│   ├── raw/                             ← Source data from EU portal
│   └── processed/                       ← Cleaned CSVs (12 curated + 152 full list)
│
├── 02_python_analysis/
│   ├── 00_parse_eif_pdfs.py             ← Extract intermediaries from EIF PDF
│   ├── 00_filter_intermediaries.py      ← Filter by country, sector, finance type
│   ├── 01_data_cleaning.py              ← Raw → clean pipeline
│   ├── 02_exploratory_analysis.py       ← EDA: distributions, patterns, gaps
│   └── 03_strategic_scoring.py          ← Scoring model and priority tiers
│
├── 03_powerbi/                          ← Dashboard charts (Power BI + standalone)
├── 04_business_analysis/                ← Gap analysis + strategic recommendations
├── 05_analysis_reports/                 ← Executive summary, outreach tracker, pitch deck
├── 06_n8n/                              ← Approval-to-outreach automation (n8n + Notion)
└── docs/                                ← Methodology, data dictionary, decision framework
```

---

## Data Source & License

**Source:** European Commission — Your Europe Portal
**URL:** https://youreurope.europa.eu/business/finance-funding/getting-funding/access-finance/en/financial-intermediaries
**EIF PDF:** https://www.eif.org/files/calls/ieu-equity-visibility-report-financial-intermediaries.pdf
**Reuse policy:** European Commission reuse policy — public data, reuse permitted
**Collected:** March 2025
