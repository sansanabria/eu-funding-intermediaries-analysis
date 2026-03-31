# ============================================================
# SCRIPT 02 — KPI OVERVIEW
# Columns to drag into Values: ALL columns
# Shows: Total funds, countries, EIF capital, top fund
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
ROSE    = '#9B5050'
TEAL    = '#377882'
TXT     = '#1E2332'
TXT_MED = '#5A6478'
BG      = '#FFFFFF'
SURFACE = '#F7F8FC'

fig, axes = plt.subplots(2, 3, figsize=(14, 6.5))
fig.patch.set_facecolor(BG)

kpis = [
    ('TOTAL FUND\nMANAGERS',      str(len(dataset)),                                        NAVY),
    ('COUNTRIES\nCOVERED',         str(dataset['country_primary'].nunique()),                 STEEL),
    ('TOTAL EIF\nCAPITAL',         f"EUR {dataset['eif_commitment_eur'].sum()/1e6:.1f}M",    COPPER),
    ('FUNDS FIT\nSOLAR',           str(int(dataset['solar_fit'].sum())),                      SAGE),
    ('FUNDS FIT\nHYDROGEN',        str(int(dataset['hydrogen_fit'].sum())),                   TEAL),
    ('FUNDS FIT\nDESALINATION',    str(int(dataset['desalination_fit'].sum())),                ROSE),
]

for ax, (label, value, accent) in zip(axes.flat, kpis):
    ax.set_facecolor(SURFACE)
    # Colored top accent bar
    ax.add_patch(plt.Rectangle((0, 1), 1, 0.06, transform=ax.transAxes,
                                color=accent, clip_on=False))
    # Value
    ax.text(0.5, 0.55, value, ha='center', va='center',
            fontsize=30, fontweight='bold', color=NAVY,
            fontfamily='Arial', transform=ax.transAxes)
    # Label
    ax.text(0.5, 0.18, label, ha='center', va='center',
            fontsize=9, color=TXT_MED, fontfamily='Arial',
            linespacing=1.4, transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

plt.suptitle('EU Funding Intermediaries Analysis  |  EIF Fund Managers Overview',
             fontsize=14, fontweight='bold', color=NAVY,
             fontfamily='Arial', y=1.02)
plt.subplots_adjust(hspace=0.35, wspace=0.25)
plt.tight_layout()
plt.show()
