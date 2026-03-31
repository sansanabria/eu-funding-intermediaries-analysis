# ============================================================
# SCRIPT 01 — LOAD DATA
# Use: Home → Get Data → More → Other → Python Script
# Paste this entire script and click OK
# ============================================================

import pandas as pd

from pathlib import Path

_csv = Path(__file__).resolve().parent.parent.parent / '01_data' / 'processed' / 'eif_fund_managers_clean.csv'
df = pd.read_csv(_csv, encoding='utf-8-sig')

# Short name for cleaner chart labels
df['short_name'] = df['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x
)

# Ensure numeric columns are correct type
df['eif_commitment_eur'] = pd.to_numeric(df['eif_commitment_eur'], errors='coerce')
df['fit_score_10'] = pd.to_numeric(df['fit_score_10'], errors='coerce')
df['solar_fit'] = pd.to_numeric(df['solar_fit'], errors='coerce').fillna(0).astype(int)
df['hydrogen_fit'] = pd.to_numeric(df['hydrogen_fit'], errors='coerce').fillna(0).astype(int)
df['desalination_fit'] = pd.to_numeric(df['desalination_fit'], errors='coerce').fillna(0).astype(int)
