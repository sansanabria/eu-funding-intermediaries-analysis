# ============================================================
# SCRIPT 05 — PROJECT FIT COVERAGE
# Columns to drag into Values: manager_name, solar_fit,
#                               hydrogen_fit, desalination_fit
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
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
TXT_LT  = '#8C96AA'
BG      = '#FFFFFF'
SURFACE = '#F7F8FC'
SURF2   = '#EDF0F7'

dataset['short_name'] = dataset['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)

fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
fig.patch.set_facecolor(BG)

# --- Left: summary bar chart ---
labels = ['Solar Energy', 'Green Hydrogen', 'Desalination']
counts = [dataset['solar_fit'].sum(), dataset['hydrogen_fit'].sum(), dataset['desalination_fit'].sum()]
colors = [COPPER, NAVY, TEAL]

bars = axes[0].bar(labels, counts, color=colors, width=0.5, edgecolor=BG, linewidth=2)
for bar, count in zip(bars, counts):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                 f'{int(count)} funds', ha='center', fontsize=11,
                 fontweight='bold', color=TXT, fontfamily='Arial')

axes[0].set_title('Funds Available by Project Type', fontsize=13,
                  fontweight='bold', color=NAVY, fontfamily='Arial', pad=18)
axes[0].plot([0, 1], [1.02, 1.02], transform=axes[0].transAxes,
             color=COPPER, linewidth=1.2, clip_on=False)
axes[0].set_ylabel('Number of Fund Managers', fontsize=10, color=TXT_MED, fontfamily='Arial')
axes[0].set_ylim(0, max(counts) + 2)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].spines['left'].set_color(SURF2)
axes[0].spines['bottom'].set_color(SURF2)
axes[0].tick_params(colors=TXT_MED, labelsize=9)
axes[0].set_facecolor(BG)

# --- Right: heatmap — which manager fits which project ---
fit_cols = ['solar_fit', 'hydrogen_fit', 'desalination_fit']
fit_labels = ['Solar', 'Hydrogen', 'Desalination']
d = dataset.set_index('short_name')[fit_cols]

# Custom colormap: white for 0, navy for 1
from matplotlib.colors import ListedColormap
cmap = ListedColormap([SURFACE, NAVY])

im = axes[1].imshow(d.values, cmap=cmap, aspect='auto', vmin=0, vmax=1)

axes[1].set_xticks(range(3))
axes[1].set_xticklabels(fit_labels, fontsize=10, color=TXT_MED, fontfamily='Arial')
axes[1].set_yticks(range(len(d.index)))
axes[1].set_yticklabels(d.index, fontsize=8, color=TXT_MED, fontfamily='Arial')

for i in range(len(d.index)):
    for j in range(3):
        val = d.values[i, j]
        axes[1].text(j, i, '✓' if val == 1 else '—', ha='center', va='center',
                     fontsize=13, color=BG if val == 1 else TXT_LT, fontweight='bold')

# Grid lines for clean separation
for i in range(len(d.index) + 1):
    axes[1].axhline(i - 0.5, color=BG, linewidth=1.5)
for j in range(4):
    axes[1].axvline(j - 0.5, color=BG, linewidth=1.5)

axes[1].set_title('Project Fit by Fund Manager', fontsize=13,
                  fontweight='bold', color=NAVY, fontfamily='Arial', pad=18)
axes[1].plot([0, 1], [1.02, 1.02], transform=axes[1].transAxes,
             color=COPPER, linewidth=1.2, clip_on=False)
axes[1].set_facecolor(BG)

plt.tight_layout()
plt.show()
