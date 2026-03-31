"""
03 — Strategic Scoring Model
Project: EU Funding Intermediaries Analysis
Purpose: Score and rank each fund manager based on fit with company projects

Scoring Methodology (out of 10):
  - Project fit:    3 pts (1 per match: Solar, Hydrogen, Desalination)
  - EIF commitment: 2 pts (larger = more capacity)
  - SDG alignment:  2 pts (more SDGs = broader impact fit)
  - Contact info:   2 pts (email + phone + website)
  - Geography:      1 pt  (priority countries score higher)
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')

df = pd.read_csv('../01_data/processed/eif_fund_managers_clean.csv')
print(f'Dataset loaded: {df.shape[0]} fund managers')

# 1. Score: Project fit (max 3)
df['score_project_fit'] = df['solar_fit'] + df['hydrogen_fit'] + df['desalination_fit']

# 2. Score: EIF commitment (max 2)
def score_commitment(amount):
    if pd.isna(amount):
        return 0
    if amount >= 40_000_000:
        return 2
    elif amount >= 20_000_000:
        return 1
    return 0.5

df['score_commitment'] = df['eif_commitment_eur'].apply(score_commitment)

# 3. Score: SDG alignment (max 2)
df['score_sdg'] = df['sdg_count'].apply(lambda x: 2 if x >= 3 else (1 if x >= 1 else 0))

# 4. Score: Contact completeness (max 2)
def score_contact(row):
    score = 0
    if pd.notna(row['email']) and row['email']:
        score += 0.75
    if pd.notna(row['phone']) and row['phone']:
        score += 0.75
    if pd.notna(row['website']) and row['website']:
        score += 0.5
    return min(score, 2)

df['score_contact'] = df.apply(score_contact, axis=1)

# 5. Score: Geography (max 1)
priority_countries = ['Spain', 'Spain & Portugal', 'Portugal', 'Global', 'Worldwide & Spain']
df['score_geography'] = df['country_primary'].apply(lambda c: 1 if c in priority_countries else 0.5)

# 6. Composite score
df['fit_score_10'] = (
    df['score_project_fit'] + df['score_commitment'] + df['score_sdg'] +
    df['score_contact'] + df['score_geography']
).round(1)

# 7. Priority tiers
def assign_tier(score):
    if score >= 7:
        return 'Tier 1 - Priority'
    elif score >= 4:
        return 'Tier 2 - Secondary'
    return 'Tier 3 - Monitor'

df['priority_tier'] = df['fit_score_10'].apply(assign_tier)

df_ranked = df.sort_values('fit_score_10', ascending=False)

print('\n=== FUND MANAGER RANKINGS ===')
print(df_ranked[['manager_name', 'country_primary', 'fund_type',
                  'score_project_fit', 'score_commitment', 'score_sdg',
                  'score_contact', 'score_geography', 'fit_score_10']].to_string())

# 8. Visualize rankings
df_ranked['short_name'] = df_ranked['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)
df_s = df_ranked.sort_values('fit_score_10', ascending=True).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(12, 7))
score_cols = ['score_project_fit', 'score_commitment', 'score_sdg', 'score_contact', 'score_geography']
score_labels = ['Project Fit', 'EIF Commitment', 'SDG Alignment', 'Contact Info', 'Geography']
colors = ['#233C64', '#4B648C', '#377882', '#AA7D3C', '#377D55']

bottoms = np.zeros(len(df_s))
for col, label, color in zip(score_cols, score_labels, colors):
    vals = pd.to_numeric(df_s[col], errors='coerce').fillna(0).values
    ax.barh(df_s['short_name'], vals, left=bottoms, label=label, color=color)
    bottoms += vals

for i, (_, row) in enumerate(df_s.iterrows()):
    ax.text(row['fit_score_10'] + 0.1, i, f"{row['fit_score_10']}/10", va='center', fontsize=9)

ax.set_title('Strategic Fit Score by Fund Manager (out of 10)', fontsize=13, fontweight='bold')
ax.set_xlabel('Score')
ax.set_xlim(0, 12)
ax.legend(loc='lower right', fontsize=9)
plt.tight_layout()
plt.savefig('../03_powerbi/screenshots/strategic_scores.png', dpi=150, bbox_inches='tight')
plt.close()
print('\nChart saved: strategic_scores.png')

# 9. Priority tiers summary
print('\n=== PRIORITY TIERS ===')
for tier in ['Tier 1 - Priority', 'Tier 2 - Secondary', 'Tier 3 - Monitor']:
    tier_funds = df_ranked[df_ranked['priority_tier'] == tier]['manager_name'].tolist()
    print(f'\n{tier} ({len(tier_funds)} funds):')
    for f in tier_funds:
        score = df_ranked.loc[df_ranked['manager_name'] == f, 'fit_score_10'].values[0]
        print(f'  - {f} -- Score: {score}/10')

# 10. Export scored dataset
output_path = '../01_data/processed/eif_fund_managers_clean.csv'
df_ranked.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f'\nScored dataset saved to: {output_path}')
print('Final columns added: fit_score_10, priority_tier, score_*')
print('This file is ready to import into Power BI.')
