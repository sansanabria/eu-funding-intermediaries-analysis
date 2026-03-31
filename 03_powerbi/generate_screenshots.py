"""
Generate all Power BI dashboard screenshots using the Python visual scripts.
Simulates the Power BI `dataset` variable by loading the CSV directly.
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', '01_data', 'processed', 'eif_fund_managers_clean.csv')
SCRIPTS_DIR = os.path.join(BASE, 'python_scripts')
OUT_DIR = os.path.join(BASE, 'screenshots')
os.makedirs(OUT_DIR, exist_ok=True)

# Load data (same as 01_load_data.py)
df = pd.read_csv(DATA, encoding='utf-8-sig')
df['short_name'] = df['manager_name'].apply(lambda x: x[:28] + '...' if len(str(x)) > 28 else x)
df['eif_commitment_eur'] = pd.to_numeric(df['eif_commitment_eur'], errors='coerce')
df['fit_score_10'] = pd.to_numeric(df['fit_score_10'], errors='coerce')
df['solar_fit'] = pd.to_numeric(df['solar_fit'], errors='coerce').fillna(0).astype(int)
df['hydrogen_fit'] = pd.to_numeric(df['hydrogen_fit'], errors='coerce').fillna(0).astype(int)
df['desalination_fit'] = pd.to_numeric(df['desalination_fit'], errors='coerce').fillna(0).astype(int)

# Script → output filename mapping
scripts = [
    ('02_kpi_overview.py',       'kpi_overview.png'),
    ('03_eif_commitment_bar.py', 'eif_commitments.png'),
    ('04_fund_type_pie.py',      'fund_type_breakdown.png'),
    ('05_project_fit_bar.py',    'project_fit_coverage.png'),
    ('06_strategic_scores.py',   'strategic_scores.png'),
    ('07_sdg_heatmap.py',        'sdg_alignment.png'),
    ('08_country_bar.py',        'geographic_distribution.png'),
]

for script_name, out_name in scripts:
    print(f'Generating {out_name}...')
    plt.close('all')

    # Each Power BI script expects `dataset`
    dataset = df.copy()

    # Read and execute the script
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Replace plt.show() with savefig
    code = code.replace('plt.show()', '')

    exec(code, {'dataset': dataset, '__builtins__': __builtins__})

    # Save current figure
    fig = plt.gcf()
    out_path = os.path.join(OUT_DIR, out_name)
    fig.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor(),
                edgecolor='none', pad_inches=0.3)
    print(f'  Saved: {out_path}')

print('\nAll screenshots generated.')
