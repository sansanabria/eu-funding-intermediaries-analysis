# ============================================================
# SCRIPT 06 — STRATEGIC FIT SCORES RANKING
# Columns to drag into Values: manager_name, score_project_fit,
#   score_commitment, score_sdg, score_contact,
#   score_geography, fit_score_10, priority_tier
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
BG      = '#FFFFFF'
SURFACE = '#F7F8FC'
SURF2   = '#EDF0F7'

dataset['short_name'] = dataset['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)

df_s = dataset.sort_values('fit_score_10', ascending=True).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

score_cols   = ['score_project_fit', 'score_commitment', 'score_sdg', 'score_contact', 'score_geography']
score_labels = ['Project Fit', 'EIF Commitment', 'SDG Alignment', 'Contact Info', 'Geography']
colors       = [NAVY, COPPER, SAGE, TEAL, STEEL]

bottoms = np.zeros(len(df_s))
for col, label, color in zip(score_cols, score_labels, colors):
    vals = pd.to_numeric(df_s[col], errors='coerce').fillna(0).values
    ax.barh(df_s['short_name'], vals, left=bottoms, label=label,
            color=color, edgecolor=BG, linewidth=0.5, height=0.6)
    bottoms += vals

# Tier colors: Sage = Priority, Copper = Secondary, Rose = Monitor
tier_colors = {'Tier 1 - Priority': SAGE, 'Tier 2 - Secondary': COPPER, 'Tier 3 - Monitor': ROSE}

for i, row in df_s.iterrows():
    score = row['fit_score_10']
    tier  = row.get('priority_tier', '')
    color = tier_colors.get(tier, TXT_MED)
    ax.text(score + 0.15, i, f'{score}/10', va='center', fontsize=9,
            color=TXT, fontweight='bold', fontfamily='Arial')
    ax.text(-0.5, i, '●', va='center', ha='right', fontsize=14, color=color)

ax.set_title('Strategic Fit Score  —  Fund Manager Ranking', fontsize=14,
             fontweight='bold', color=NAVY, fontfamily='Arial', pad=18)
ax.plot([0, 1], [1.02, 1.02], transform=ax.transAxes,
        color=COPPER, linewidth=1.5, clip_on=False)

ax.set_xlabel('Score (out of 10)', fontsize=10, color=TXT_MED, fontfamily='Arial')
ax.set_xlim(-1, 13)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SURF2)
ax.spines['bottom'].set_color(SURF2)
ax.tick_params(colors=TXT_MED, labelsize=9)

# Legend — score components + tier indicators
legend_handles = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, score_labels)]
tier_handles   = [mpatches.Patch(color=c, label=t.replace('Tier 1 - ', '').replace('Tier 2 - ', '').replace('Tier 3 - ', ''))
                  for t, c in tier_colors.items()]
all_handles = legend_handles + [mpatches.Patch(color='none', label='')] + tier_handles
ax.legend(handles=all_handles, loc='lower right', fontsize=8,
          framealpha=0.95, edgecolor=SURF2, fancybox=False, ncol=2)

plt.tight_layout()
plt.show()
