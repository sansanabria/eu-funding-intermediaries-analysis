# ============================================================
# SCRIPT 07 — SDG ALIGNMENT HEATMAP
# Columns to drag into Values: manager_name, sdg_tags
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
TXT     = '#1E2332'
TXT_MED = '#5A6478'
BG      = '#FFFFFF'
SURFACE = '#F7F8FC'
SURF2   = '#EDF0F7'

dataset['short_name'] = dataset['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)

# Build SDG matrix
all_sdgs = []
for tags in dataset['sdg_tags'].dropna():
    for s in str(tags).split(','):
        s = s.strip()
        if s.isdigit():
            all_sdgs.append(int(s))
all_sdgs = sorted(set(all_sdgs))

sdg_cols = [f'SDG {s}' for s in all_sdgs]
matrix = pd.DataFrame(0, index=dataset['short_name'], columns=sdg_cols)

for _, row in dataset.iterrows():
    name = row['short_name']
    if pd.notna(row['sdg_tags']) and row['sdg_tags']:
        for s in str(row['sdg_tags']).split(','):
            s = s.strip()
            if s.isdigit() and f'SDG {s}' in matrix.columns:
                matrix.loc[name, f'SDG {s}'] = 1

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# Custom colormap: surface for 0, navy for 1
from matplotlib.colors import ListedColormap
cmap = ListedColormap([SURFACE, NAVY])

im = ax.imshow(matrix.values, cmap=cmap, aspect='auto', vmin=0, vmax=1)

# Checkmarks
for i in range(len(matrix.index)):
    for j in range(len(matrix.columns)):
        if matrix.values[i, j] == 1:
            ax.text(j, i, '✓', ha='center', va='center',
                    fontsize=12, color=BG, fontweight='bold')

# Grid lines for clean cell separation
for i in range(len(matrix.index) + 1):
    ax.axhline(i - 0.5, color=BG, linewidth=1.5)
for j in range(len(matrix.columns) + 1):
    ax.axvline(j - 0.5, color=BG, linewidth=1.5)

# SDG color stripe at top — using brand-aligned tones
sdg_brand = {6: TEAL, 7: COPPER, 9: STEEL, 13: SAGE, 14: TEAL}
for j, sdg_num in enumerate(all_sdgs):
    color = sdg_brand.get(sdg_num, NAVY)
    ax.add_patch(plt.Rectangle((j - 0.5, -0.9), 1, 0.45, color=color, clip_on=False))
    ax.text(j, -0.68, str(sdg_num), ha='center', va='center',
            fontsize=8, color=BG, fontweight='bold')

ax.set_xticks(range(len(sdg_cols)))
ax.set_xticklabels(sdg_cols, rotation=45, ha='right', fontsize=9,
                   color=TXT_MED, fontfamily='Arial')
ax.set_yticks(range(len(matrix.index)))
ax.set_yticklabels(matrix.index, fontsize=9, color=TXT_MED, fontfamily='Arial')

ax.set_title('SDG Alignment by Fund Manager', fontsize=14,
             fontweight='bold', color=NAVY, fontfamily='Arial', pad=24)
ax.plot([0, 1], [1.04, 1.04], transform=ax.transAxes,
        color=COPPER, linewidth=1.5, clip_on=False)

# Legend
legend = [mpatches.Patch(color=TEAL,   label='SDG 6 — Clean Water'),
          mpatches.Patch(color=COPPER,  label='SDG 7 — Renewable Energy'),
          mpatches.Patch(color=STEEL,   label='SDG 9 — Industry & Innovation'),
          mpatches.Patch(color=SAGE,    label='SDG 13 — Climate Action'),
          mpatches.Patch(color=TEAL,    label='SDG 14 — Life Below Water')]
ax.legend(handles=legend, loc='lower right', fontsize=8,
          bbox_to_anchor=(1.0, -0.35), ncol=3, framealpha=0.95,
          edgecolor=SURF2, fancybox=False)

plt.tight_layout()
plt.show()
