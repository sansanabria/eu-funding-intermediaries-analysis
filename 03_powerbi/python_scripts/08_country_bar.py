# ============================================================
# SCRIPT 08 — GEOGRAPHIC DISTRIBUTION
# Columns to drag into Values: country_primary, eif_commitment_eur
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# --- Brand palette ---
NAVY    = '#233C64'
STEEL   = '#4B648C'
COPPER  = '#AA7D3C'
SAGE    = '#377D55'
TEAL    = '#377882'
ROSE    = '#9B5050'
TXT     = '#1E2332'
TXT_MED = '#5A6478'
BG      = '#FFFFFF'
SURFACE = '#F7F8FC'
SURF2   = '#EDF0F7'

COLORS = [NAVY, COPPER, SAGE, TEAL, STEEL, ROSE]

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor(BG)

# --- Left: count of fund managers by country ---
country_counts = dataset['country_primary'].value_counts()
bars = axes[0].bar(country_counts.index, country_counts.values,
                   color=COLORS[:len(country_counts)], edgecolor=BG, linewidth=2, width=0.55)
for bar, val in zip(bars, country_counts.values):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                 str(int(val)), ha='center', fontsize=11,
                 fontweight='bold', color=TXT, fontfamily='Arial')

axes[0].set_title('Fund Managers by Country', fontsize=13,
                  fontweight='bold', color=NAVY, fontfamily='Arial', pad=18)
axes[0].plot([0, 1], [1.02, 1.02], transform=axes[0].transAxes,
             color=COPPER, linewidth=1.2, clip_on=False)
axes[0].set_ylabel('Number of Fund Managers', fontsize=10, color=TXT_MED, fontfamily='Arial')
axes[0].set_ylim(0, country_counts.max() + 1.5)
axes[0].tick_params(axis='x', rotation=15, colors=TXT_MED, labelsize=9)
axes[0].tick_params(axis='y', colors=TXT_MED, labelsize=9)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].spines['left'].set_color(SURF2)
axes[0].spines['bottom'].set_color(SURF2)
axes[0].set_facecolor(BG)

# --- Right: total EIF commitment by country ---
country_commit = dataset.groupby('country_primary')['eif_commitment_eur'].sum().sort_values(ascending=False)
bars2 = axes[1].bar(country_commit.index, country_commit.values / 1e6,
                    color=COLORS[:len(country_commit)], edgecolor=BG, linewidth=2, width=0.55)
for bar, val in zip(bars2, country_commit.values):
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f'EUR {val/1e6:.0f}M', ha='center', fontsize=9,
                 fontweight='bold', color=COPPER, fontfamily='Arial')

axes[1].set_title('Total EIF Commitment by Country', fontsize=13,
                  fontweight='bold', color=NAVY, fontfamily='Arial', pad=18)
axes[1].plot([0, 1], [1.02, 1.02], transform=axes[1].transAxes,
             color=COPPER, linewidth=1.2, clip_on=False)
axes[1].set_ylabel('EUR Millions', fontsize=10, color=TXT_MED, fontfamily='Arial')
axes[1].tick_params(axis='x', rotation=15, colors=TXT_MED, labelsize=9)
axes[1].tick_params(axis='y', colors=TXT_MED, labelsize=9)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].spines['left'].set_color(SURF2)
axes[1].spines['bottom'].set_color(SURF2)
axes[1].set_facecolor(BG)

plt.tight_layout()
plt.show()
