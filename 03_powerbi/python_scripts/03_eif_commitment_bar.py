# ============================================================
# SCRIPT 03 — EIF COMMITMENT BY FUND MANAGER
# Columns to drag into Values: manager_name, eif_commitment_eur
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
TXT     = '#1E2332'
TXT_MED = '#5A6478'
BG      = '#FFFFFF'
SURFACE = '#F7F8FC'
SURF2   = '#EDF0F7'

d = dataset.dropna(subset=['eif_commitment_eur']).sort_values('eif_commitment_eur', ascending=True)
d['short_name'] = d['manager_name'].apply(lambda x: x[:30] + '...' if len(str(x)) > 30 else x)

fig, ax = plt.subplots(figsize=(12, 6.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# Tier-based coloring
colors = [NAVY if v >= 40e6 else STEEL if v >= 20e6 else SURF2
          for v in d['eif_commitment_eur']]
bar_text = [BG if v >= 20e6 else TXT_MED for v in d['eif_commitment_eur']]

bars = ax.barh(d['short_name'], d['eif_commitment_eur'] / 1e6,
               color=colors, edgecolor=BG, linewidth=0.5, height=0.65)

for bar, val, tc in zip(bars, d['eif_commitment_eur'], bar_text):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            f'EUR {val/1e6:.1f}M', va='center', fontsize=9,
            color=COPPER, fontweight='bold', fontfamily='Arial')

# Copper accent line under title
ax.set_title('EIF Commitment by Fund Manager', fontsize=14, fontweight='bold',
             color=NAVY, fontfamily='Arial', pad=18)
ax.plot([0, 1], [1.02, 1.02], transform=ax.transAxes,
        color=COPPER, linewidth=1.5, clip_on=False)

ax.set_xlabel('EUR Millions', fontsize=10, color=TXT_MED, fontfamily='Arial')
ax.tick_params(colors=TXT_MED, labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SURF2)
ax.spines['bottom'].set_color(SURF2)

legend = [mpatches.Patch(color=NAVY, label='≥ EUR 40M'),
          mpatches.Patch(color=STEEL, label='EUR 20M – 40M'),
          mpatches.Patch(color=SURF2, label='< EUR 20M')]
ax.legend(handles=legend, loc='lower right', fontsize=8,
          framealpha=0.9, edgecolor=SURF2, fancybox=False)

plt.tight_layout()
plt.show()
