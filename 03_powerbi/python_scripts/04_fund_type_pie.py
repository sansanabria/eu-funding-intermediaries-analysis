# ============================================================
# SCRIPT 04 — FUND TYPE DISTRIBUTION
# Columns to drag into Values: fund_type, eif_commitment_eur
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

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

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor(BG)

# --- Left: donut chart — count by type ---
type_counts = dataset['fund_type'].value_counts()
wedges, texts, autotexts = axes[0].pie(
    type_counts.values,
    labels=type_counts.index,
    autopct='%1.0f%%',
    colors=COLORS[:len(type_counts)],
    startangle=90,
    pctdistance=0.78,
    wedgeprops=dict(edgecolor=BG, linewidth=2.5, width=0.45)
)
for text in texts:
    text.set_fontsize(9)
    text.set_color(TXT_MED)
    text.set_fontfamily('Arial')
for text in autotexts:
    text.set_fontsize(10)
    text.set_fontweight('bold')
    text.set_color(TXT)
    text.set_fontfamily('Arial')
axes[0].set_title('Fund Managers by Type', fontsize=13,
                  fontweight='bold', color=NAVY, fontfamily='Arial', pad=14)
# Copper underline
axes[0].plot([0.1, 0.9], [-0.02, -0.02], transform=axes[0].transAxes,
             color=COPPER, linewidth=1.2, clip_on=False)

# --- Right: horizontal bar — EIF commitment by fund type ---
type_commit = dataset.groupby('fund_type')['eif_commitment_eur'].sum().sort_values(ascending=True)
bar_colors = COLORS[:len(type_commit)]

bars = axes[1].barh(type_commit.index, type_commit.values / 1e6,
                    color=bar_colors, edgecolor=BG, linewidth=0.5, height=0.55)
for bar, val in zip(bars, type_commit.values):
    axes[1].text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
                 f'EUR {val/1e6:.1f}M', va='center', fontsize=9,
                 color=COPPER, fontweight='bold', fontfamily='Arial')

axes[1].set_title('EIF Commitment by Fund Type', fontsize=13,
                  fontweight='bold', color=NAVY, fontfamily='Arial', pad=14)
axes[1].plot([0, 1], [1.02, 1.02], transform=axes[1].transAxes,
             color=COPPER, linewidth=1.2, clip_on=False)
axes[1].set_xlabel('EUR Millions', fontsize=10, color=TXT_MED, fontfamily='Arial')
axes[1].tick_params(colors=TXT_MED, labelsize=9)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].spines['left'].set_color(SURF2)
axes[1].spines['bottom'].set_color(SURF2)
axes[1].set_facecolor(BG)

plt.tight_layout()
plt.show()
