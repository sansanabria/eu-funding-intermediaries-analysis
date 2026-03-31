# Data Dictionary

## Source File
`01_data/raw/eif_fund_managers.xlsx` — Original data collected from the European Commission portal

## Processed File
`01_data/processed/eif_fund_managers_clean.csv` — Cleaned and structured output

---

## Field Definitions

| Field Name | Original Label | Type | Description | Example |
|---|---|---|---|---|
| `location` | Location under scope | Text | Country or region where the fund operates or invests | `Spain`, `Global`, `Sweden` |
| `fund_manager` | Financial Manager | Text | Name of the fund management company and description | `Suma Capital SGEIC SA` |
| `financial_product` | Financial Product Available | Text | Specific fund products offered by this manager | `SC Climate Impact Fund III` |
| `target_area` | Target Area | Text | Investment themes and sectors the fund focuses on | `Clean Energy Transition`, `Digital Connectivity` |
| `match_our_projects` | Match our projects | Text | Internal assessment of alignment with company projects | Populated during analysis |
| `opportunities` | Potential opportunities | Text | Specific funding opportunities available | `Funding, VC` |
| `how_to_approach` | How | Text | Recommended approach strategy for engagement | `Reach out with company overview` |
| `support_type` | Type of Support | Text | Category of financial support provided | `Infrastructure`, `Generalist`, `Social Impact` |
| `eif_commitment` | Commitment Under InvestEU | Currency (EUR) | EIF financial commitment allocated to this intermediary | `EUR 41,250,000` |
| `address` | Address | Text | Physical office address | `Av Diagonal 640 5F, 08017 Barcelona` |
| `website` | Website | URL | Fund manager website | `http://sumacapital.com/en` |
| `email` | email | Email | Contact email address | `info@sumacapital.com` |
| `phone` | phone | Text | Contact phone number | `(+34) 933 680 203` |

---

## Derived Fields (added during cleaning)

| Field Name | Type | Description |
|---|---|---|
| `country_clean` | Text | Standardized country name extracted from `location` |
| `fund_type` | Category | Classified fund type: `VC`, `PE`, `Debt`, `Infrastructure`, `Accelerator` |
| `sdg_tags` | List | SDG numbers aligned with the fund (e.g., `[6, 7, 9, 13]`) |
| `solar_fit` | Boolean | Whether this fund is relevant for solar projects |
| `hydrogen_fit` | Boolean | Whether this fund is relevant for hydrogen projects |
| `desalination_fit` | Boolean | Whether this fund is relevant for desalination projects |
| `eif_commitment_eur` | Float | Numeric value of EIF commitment, cleaned from text |
| `fit_score` | Integer (0–10) | Composite score ranking fund managers by overall project fit |

---

## Categorical Values

### `support_type`
- `Infrastructure` — Real assets, energy, transport
- `Generalist` — Broad sector coverage
- `Social Impact` — SDG/impact-focused
- `VC` — Venture capital for startups

### `fund_type`
- `VC` — Venture Capital
- `PE` — Private Equity
- `Debt` — Private debt / loans
- `Infrastructure` — Infrastructure-focused
- `Accelerator` — Startup accelerator programs

### `location` (standardized values)
- `Spain`, `Portugal`, `Sweden`, `Global`, `Spain & Portugal`, `Worldwide & Spain`, `Sweden & Nordic`
