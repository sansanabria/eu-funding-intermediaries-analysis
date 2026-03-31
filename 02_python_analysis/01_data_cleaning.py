"""
01 — Data Cleaning
Project: EU Funding Intermediaries Analysis
Source: European Commission — Access to EU Finance Portal
Purpose: Transform raw Excel data into a clean, structured CSV
"""

import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

# 1. Load raw data
raw_path = '../01_data/raw/eif_fund_managers.xlsx'
df_raw = pd.read_excel(raw_path, sheet_name='EIF', header=None)
print(f'Raw shape: {df_raw.shape}')

# 2. Assign column names
column_names = [
    'location', 'fund_manager', 'financial_product', 'target_area',
    'match_our_projects', 'opportunities', 'how_to_approach', 'support_type',
    'eif_commitment', 'address', 'website', 'email', 'phone'
]
df = df_raw.iloc[2:].copy()
df.columns = column_names
df = df.reset_index(drop=True)
print(f'Data shape after removing headers: {df.shape}')

# 3. Clean text fields
def clean_text(val):
    if pd.isna(val) or str(val).strip() in ['nan', 'None', '']:
        return None
    val = str(val).replace('\n', ' ').replace('\r', ' ')
    return re.sub(r'\s+', ' ', val).strip()

text_cols = ['location', 'fund_manager', 'financial_product', 'target_area',
             'opportunities', 'how_to_approach', 'support_type', 'address',
             'website', 'email', 'phone']
for col in text_cols:
    df[col] = df[col].apply(clean_text)
print('Text fields cleaned.')

# 4. Extract and standardize country
def extract_country(loc):
    if loc is None:
        return 'Unknown'
    loc_lower = loc.lower()
    if 'spain' in loc_lower and 'portugal' in loc_lower:
        return 'Spain & Portugal'
    elif 'spain' in loc_lower:
        return 'Spain'
    elif 'portugal' in loc_lower:
        return 'Portugal'
    elif 'sweden' in loc_lower or 'nordic' in loc_lower:
        return 'Sweden'
    elif 'global' in loc_lower or 'worldwide' in loc_lower:
        return 'Global'
    return loc

df['country_primary'] = df['location'].apply(extract_country)
print(df['country_primary'].value_counts())

# 5. Clean EIF commitment amount
def extract_amount(val):
    if val is None:
        return None
    numbers = re.findall(r'[\d,\.]+', str(val))
    if numbers:
        amounts = []
        for n in numbers:
            try:
                amounts.append(float(n.replace(',', '')))
            except:
                pass
        return max(amounts) if amounts else None
    return None

df['eif_commitment_eur'] = df['eif_commitment'].apply(extract_amount)
print('EIF commitment amounts extracted:')
print(df[['fund_manager', 'eif_commitment', 'eif_commitment_eur']].to_string())

# 6. Classify fund type
def classify_fund_type(row):
    text = ' '.join(filter(None, [
        str(row.get('support_type', '') or ''),
        str(row.get('financial_product', '') or ''),
        str(row.get('opportunities', '') or '')
    ])).lower()
    if 'accelerator' in text or 'sprint' in text:
        return 'Accelerator'
    elif 'infrastructure' in text:
        return 'Infrastructure'
    elif 'venture capital' in text or 'vc' in text or 'fcr' in text or 'scr' in text:
        return 'VC'
    elif 'debt' in text or 'loan' in text:
        return 'Debt'
    elif 'private equity' in text or 'generalist' in text:
        return 'PE'
    return 'Other'

df['fund_type'] = df.apply(classify_fund_type, axis=1)
print(df['fund_type'].value_counts())

# 7. Extract fund manager name
def extract_manager_name(val):
    if val is None:
        return None
    name = val.split('.')[0].split(',')[0].strip()
    return name[:60] if len(name) > 60 else name

df['manager_name'] = df['fund_manager'].apply(extract_manager_name)
print(df[['manager_name', 'country_primary', 'fund_type']].to_string())

# 8. Project fit flags
def flag_project(row, keywords):
    text = ' '.join(filter(None, [
        str(row.get('how_to_approach', '') or ''),
        str(row.get('opportunities', '') or ''),
        str(row.get('target_area', '') or ''),
        str(row.get('financial_product', '') or '')
    ])).lower()
    return any(kw in text for kw in keywords)

df['solar_fit'] = df.apply(lambda r: flag_project(r, ['solar', 'photovoltaic', 'pv', 'renewable energy', 'energy transition']), axis=1)
df['hydrogen_fit'] = df.apply(lambda r: flag_project(r, ['hydrogen', 'electrolysis', 'decarboni']), axis=1)
df['desalination_fit'] = df.apply(lambda r: flag_project(r, ['desalination', 'water', 'sdg 6', 'sdg6', 'clean water', 'sanitation']), axis=1)
print('Project fit flags:')
print(df[['manager_name', 'solar_fit', 'hydrogen_fit', 'desalination_fit']].to_string())

# 9. SDG tags
def extract_sdgs(row):
    text = ' '.join(filter(None, [
        str(row.get('how_to_approach', '') or ''),
        str(row.get('target_area', '') or '')
    ]))
    sdgs = re.findall(r'sdg\s*(\d+)', text, re.IGNORECASE)
    return sorted(list(set([int(s) for s in sdgs]))) if sdgs else []

df['sdg_tags'] = df.apply(extract_sdgs, axis=1)
df['sdg_count'] = df['sdg_tags'].apply(len)
print(df[['manager_name', 'sdg_tags']].to_string())

# 10. Final clean dataset
clean_cols = [
    'manager_name', 'country_primary', 'fund_type', 'support_type',
    'eif_commitment_eur', 'solar_fit', 'hydrogen_fit', 'desalination_fit',
    'sdg_count', 'sdg_tags', 'financial_product', 'target_area',
    'opportunities', 'how_to_approach', 'address', 'website', 'email', 'phone',
    'fund_manager', 'location', 'eif_commitment'
]
df_clean = df[clean_cols].copy()
df_clean['solar_fit'] = df_clean['solar_fit'].astype(int)
df_clean['hydrogen_fit'] = df_clean['hydrogen_fit'].astype(int)
df_clean['desalination_fit'] = df_clean['desalination_fit'].astype(int)
df_clean['sdg_tags'] = df_clean['sdg_tags'].apply(lambda x: ', '.join(map(str, x)) if x else '')
df_clean['outreach_status'] = 'Not contacted'
df_clean['outreach_notes'] = ''

print(f'\nClean dataset shape: {df_clean.shape}')
print(df_clean[['manager_name', 'country_primary', 'fund_type', 'eif_commitment_eur', 'solar_fit', 'hydrogen_fit', 'desalination_fit']])

# 11. Export
output_path = '../01_data/processed/eif_fund_managers_clean.csv'
df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f'\nClean data exported to: {output_path}')
print(f'Rows: {len(df_clean)} | Columns: {len(df_clean.columns)}')
