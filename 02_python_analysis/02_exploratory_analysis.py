"""
02 — Exploratory Data Analysis
Project: EU Funding Intermediaries Analysis
Purpose: Explore the cleaned dataset to identify patterns, distributions, gaps, and insights
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
COLORS = ['#233C64', '#4B648C', '#377882', '#AA7D3C', '#377D55', '#9B5050', '#6B8EC2']

df = pd.read_csv('../01_data/processed/eif_fund_managers_clean.csv')
print(f'Dataset loaded: {df.shape[0]} fund managers, {df.shape[1]} columns')

# 1. Dataset overview
print('\n=== DATASET OVERVIEW ===')
print(f'Total fund managers: {len(df)}')
print(f'Countries covered: {df["country_primary"].nunique()}')
print(f'Fund types: {df["fund_type"].nunique()}')
print(f'Total EIF commitments: EUR {df["eif_commitment_eur"].sum():,.0f}')
print(f'Average EIF commitment: EUR {df["eif_commitment_eur"].mean():,.0f}')
print('\n=== DATA COMPLETENESS ===')
for col in ['manager_name', 'country_primary', 'fund_type', 'eif_commitment_eur', 'email', 'phone', 'website']:
    filled = df[col].notna().sum()
    pct = filled / len(df) * 100
    print(f'  {col}: {filled}/{len(df)} ({pct:.0f}% complete)')

# 2. Geographic distribution
df['short_name'] = df['manager_name'].apply(lambda x: x[:30] + '...' if len(str(x)) > 30 else x)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
country_counts = df['country_primary'].value_counts()
axes[0].bar(country_counts.index, country_counts.values, color=COLORS[:len(country_counts)])
axes[0].set_title('Fund Managers by Country', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Number of Fund Managers')
axes[0].tick_params(axis='x', rotation=15)

country_commit = df.groupby('country_primary')['eif_commitment_eur'].sum().sort_values(ascending=False)
axes[1].bar(country_commit.index, country_commit.values / 1e6, color=COLORS[:len(country_commit)])
axes[1].set_title('Total EIF Commitment by Country (EUR M)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('EUR Millions')
axes[1].tick_params(axis='x', rotation=15)
plt.tight_layout()
plt.savefig('../03_powerbi/screenshots/geographic_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('\nChart saved: geographic_distribution.png')

# 3. Fund type distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
type_counts = df['fund_type'].value_counts()
axes[0].pie(type_counts.values, labels=type_counts.index, autopct='%1.0f%%',
            colors=COLORS[:len(type_counts)], startangle=90)
axes[0].set_title('Fund Managers by Type', fontsize=12, fontweight='bold')
type_commit = df.groupby('fund_type')['eif_commitment_eur'].sum().sort_values()
axes[1].barh(type_commit.index, type_commit.values / 1e6, color=COLORS[:len(type_commit)])
axes[1].set_title('EIF Commitment by Fund Type (EUR M)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('EUR Millions')
plt.tight_layout()
plt.savefig('../03_powerbi/screenshots/fund_type_breakdown.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart saved: fund_type_breakdown.png')

# 4. EIF commitment analysis
df_sorted = df.dropna(subset=['eif_commitment_eur']).sort_values('eif_commitment_eur', ascending=True)
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(df_sorted['short_name'], df_sorted['eif_commitment_eur'] / 1e6, color=COLORS[0])
for bar, val in zip(bars, df_sorted['eif_commitment_eur']):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f'EUR {val/1e6:.1f}M', va='center', fontsize=9)
ax.set_title('EIF Commitment by Fund Manager (EUR Millions)', fontsize=13, fontweight='bold')
ax.set_xlabel('EUR Millions')
plt.tight_layout()
plt.savefig('../03_powerbi/screenshots/eif_commitments.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart saved: eif_commitments.png')
print(f'Funds with known EIF commitment: {df_sorted.shape[0]} / {len(df)}')
print(f'Total EIF commitment: EUR {df_sorted["eif_commitment_eur"].sum() / 1e6:.1f}M')

# 5. Project fit coverage
projects = ['solar_fit', 'hydrogen_fit', 'desalination_fit']
project_labels = ['Solar Energy', 'Green Hydrogen', 'Desalination / Water']
fit_counts = [df[p].sum() for p in projects]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(project_labels, fit_counts, color=['#AA7D3C', '#233C64', '#377882'], width=0.5)
for bar, count in zip(bars, fit_counts):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            f'{int(count)} funds', ha='center', fontsize=11, fontweight='bold')
ax.set_title('Fund Managers by Project Type Fit', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Fund Managers')
ax.set_ylim(0, max(fit_counts) + 2)
plt.tight_layout()
plt.savefig('../03_powerbi/screenshots/project_fit_coverage.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart saved: project_fit_coverage.png')

print('\nFund managers per project type:')
for label, count in zip(project_labels, fit_counts):
    managers = df[df[projects[project_labels.index(label)]] == 1]['manager_name'].tolist()
    print(f'  {label}: {int(count)} — {managers}')

# 6. SDG alignment heatmap
all_sdgs = sorted(set(
    sdg for tags in df['sdg_tags'].dropna()
    for sdg in [int(x.strip()) for x in str(tags).split(',') if x.strip().isdigit()]
))
sdg_cols = [f'SDG {s}' for s in all_sdgs]
matrix = pd.DataFrame(0, index=df['short_name'], columns=sdg_cols)
for _, row in df.iterrows():
    if pd.notna(row['sdg_tags']) and row['sdg_tags']:
        for s in [int(x.strip()) for x in str(row['sdg_tags']).split(',') if x.strip().isdigit()]:
            if f'SDG {s}' in matrix.columns:
                matrix.loc[row['short_name'], f'SDG {s}'] = 1

fig, ax = plt.subplots(figsize=(12, 7))
im = ax.imshow(matrix.values, cmap='Blues', aspect='auto')
ax.set_xticks(range(len(sdg_cols)))
ax.set_xticklabels(sdg_cols, rotation=45, ha='right')
ax.set_yticks(range(len(matrix.index)))
ax.set_yticklabels(matrix.index, fontsize=9)
ax.set_title('SDG Alignment by Fund Manager', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../03_powerbi/screenshots/sdg_alignment.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart saved: sdg_alignment.png')
print('\nSDG coverage count:')
print(matrix.sum().sort_values(ascending=False))

# 7. Summary
print('\n' + '=' * 60)
print('KEY FINDINGS')
print('=' * 60)
print(f'\n1. Total fund managers analyzed: {len(df)}')
print(f'   Countries: {sorted(df["country_primary"].unique())}')
print(f'\n2. Total accessible EIF capital: EUR {df["eif_commitment_eur"].sum() / 1e6:.1f}M')
print(f'   Largest single commitment: EUR {df["eif_commitment_eur"].max() / 1e6:.1f}M')
print(f'   ({df.loc[df["eif_commitment_eur"].idxmax(), "manager_name"]})')
print(f'\n3. Project fit coverage:')
for p, label in zip(projects, project_labels):
    print(f'   {label}: {int(df[p].sum())} fund managers')
print(f'\n4. Most common fund type: {df["fund_type"].value_counts().index[0]} ({df["fund_type"].value_counts().iloc[0]} funds)')
print(f'\n5. Dominant country: {df["country_primary"].value_counts().index[0]} ({df["country_primary"].value_counts().iloc[0]} funds)')
print(f'\n6. SDGs covered: {all_sdgs}')
print(f'   Most covered SDG: {matrix.sum().idxmax()} ({int(matrix.sum().max())} funds)')
