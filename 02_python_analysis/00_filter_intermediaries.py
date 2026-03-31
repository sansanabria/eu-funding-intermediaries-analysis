"""
00 — Filter EIF Intermediaries by Company Profile
Project: EU Funding Intermediaries Analysis
Source: eif_pdf_intermediaries.csv (output of 00_parse_eif_pdfs.py)
Purpose: Filter the full intermediary list based on your company's country, sector, and needs

Usage:
    python 00_filter_intermediaries.py --country Spain
    python 00_filter_intermediaries.py --country Spain --sector energy
    python 00_filter_intermediaries.py --country Portugal --finance-type equity --min-amount 5000000
    python 00_filter_intermediaries.py --list-countries
    python 00_filter_intermediaries.py --list-sectors

Requirements:
    pip install pandas
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# ── Configuration ─────────────────────────────────────────────────────

INPUT_PATH = Path(__file__).parent.parent / '01_data' / 'processed' / 'eif_pdf_intermediaries.csv'
OUTPUT_PATH = Path(__file__).parent.parent / '01_data' / 'processed' / 'eif_filtered_intermediaries.csv'

# Sector keyword mapping — matches against target_area and sector_focus columns
SECTOR_KEYWORDS = {
    'energy': [
        'energy', 'climate', 'renewable', 'solar', 'wind', 'hydrogen',
        'clean tech', 'cleantech', 'green', 'sustainability', 'environment',
        'decarboni', 'transition', 'carbon',
    ],
    'digital': [
        'digital', 'ict', 'software', 'ai', 'artificial intelligence',
        'cyber', 'blockchain', 'fintech', 'tech', 'saas',
    ],
    'social': [
        'social', 'impact', 'education', 'inclusion', 'community',
    ],
    'infrastructure': [
        'infrastructure', 'transport', 'construction', 'real estate', 'building',
    ],
    'life-science': [
        'life science', 'health', 'biotech', 'pharma', 'medical', 'healthcare',
    ],
    'agrifood': [
        'agri', 'food', 'agriculture', 'farming', 'natural capital',
    ],
}


# ── Filtering ─────────────────────────────────────────────────────────

def filter_by_country(df, country):
    """Filter records matching the given country name (case-insensitive)."""
    mask = df['country'].str.lower() == country.lower()
    return df[mask]


def filter_by_sector(df, sector):
    """Filter records where target_area or sector_focus match sector keywords."""
    if sector.lower() not in SECTOR_KEYWORDS:
        print(f'WARNING: Unknown sector "{sector}". Available: {", ".join(sorted(SECTOR_KEYWORDS.keys()))}')
        return df

    keywords = SECTOR_KEYWORDS[sector.lower()]

    # Search in target_area and sector_focus columns
    searchable = (
        df['target_area'].fillna('').str.lower() + ' ' +
        df['sector_focus'].fillna('').str.lower() + ' ' +
        df['fund_name'].fillna('').str.lower()
    )
    mask = searchable.apply(lambda text: any(kw in text for kw in keywords))
    return df[mask]


def filter_by_finance_type(df, finance_type):
    """Filter records by support type (equity, debt, venture capital, etc.)."""
    ft_lower = finance_type.lower()
    mask = df['support_type'].fillna('').str.lower().str.contains(ft_lower, na=False)
    return df[mask]


def filter_by_amount(df, min_amount=None, max_amount=None):
    """Filter records by commitment amount range."""
    if min_amount is not None:
        df = df[df['commitment_eur'].fillna(0) >= min_amount]
    if max_amount is not None:
        df = df[df['commitment_eur'].fillna(float('inf')) <= max_amount]
    return df


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Filter EIF intermediaries by your company profile.',
        epilog='Example: python 00_filter_intermediaries.py --country Spain --sector energy'
    )
    parser.add_argument('--country', type=str, default=None,
                        help='Filter by country (e.g., Spain, Portugal, Sweden)')
    parser.add_argument('--sector', type=str, default=None,
                        help=f'Filter by sector. Options: {", ".join(sorted(SECTOR_KEYWORDS.keys()))}')
    parser.add_argument('--finance-type', type=str, default=None,
                        help='Filter by finance type (e.g., equity, debt, venture, infrastructure)')
    parser.add_argument('--min-amount', type=float, default=None,
                        help='Minimum EIF commitment amount in EUR')
    parser.add_argument('--max-amount', type=float, default=None,
                        help='Maximum EIF commitment amount in EUR')
    parser.add_argument('--input', type=str, default=None,
                        help=f'Input CSV path (default: {INPUT_PATH})')
    parser.add_argument('--output', type=str, default=None,
                        help=f'Output CSV path (default: {OUTPUT_PATH})')
    parser.add_argument('--list-countries', action='store_true',
                        help='List available countries in the dataset and exit')
    parser.add_argument('--list-sectors', action='store_true',
                        help='List available sector filters and exit')
    args = parser.parse_args()

    # List modes
    if args.list_sectors:
        print('Available sector filters:')
        for name, keywords in sorted(SECTOR_KEYWORDS.items()):
            print(f'  {name:20s} keywords: {", ".join(keywords[:5])}...')
        sys.exit(0)

    # Load data
    input_path = args.input or str(INPUT_PATH)
    if not Path(input_path).exists():
        print(f'ERROR: Input file not found: {input_path}')
        print(f'Run 00_parse_eif_pdfs.py first to generate the intermediary CSV.')
        sys.exit(1)

    df = pd.read_csv(input_path)
    print(f'\n{"="*70}')
    print(f'EIF Intermediary Filter')
    print(f'{"="*70}')
    print(f'Loaded: {len(df)} intermediaries from {df["country"].nunique()} countries\n')

    if args.list_countries:
        print('Countries in dataset:')
        print(df['country'].value_counts().to_string())
        sys.exit(0)

    # Apply filters
    filters_applied = []

    if args.country:
        df = filter_by_country(df, args.country)
        filters_applied.append(f'country={args.country}')
        print(f'  After country filter ({args.country}): {len(df)} records')

    if args.sector:
        df = filter_by_sector(df, args.sector)
        filters_applied.append(f'sector={args.sector}')
        print(f'  After sector filter ({args.sector}): {len(df)} records')

    if args.finance_type:
        df = filter_by_finance_type(df, args.finance_type)
        filters_applied.append(f'finance_type={args.finance_type}')
        print(f'  After finance type filter ({args.finance_type}): {len(df)} records')

    if args.min_amount or args.max_amount:
        df = filter_by_amount(df, args.min_amount, args.max_amount)
        if args.min_amount:
            filters_applied.append(f'min_amount={args.min_amount:,.0f}')
        if args.max_amount:
            filters_applied.append(f'max_amount={args.max_amount:,.0f}')
        print(f'  After amount filter: {len(df)} records')

    if not filters_applied:
        print('  No filters applied. Showing all records.')

    # Output
    if len(df) == 0:
        print('\nNo intermediaries match your filters.')
        sys.exit(0)

    output_path = args.output or str(OUTPUT_PATH)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f'\n{"="*70}')
    print(f'RESULTS — {" + ".join(filters_applied) if filters_applied else "all records"}')
    print(f'{"="*70}')
    print(f'Matching intermediaries: {len(df)}')
    print(f'Output: {output_path}')
    print()

    # Display results
    display_cols = ['country', 'fund_name', 'fund_manager', 'support_type',
                    'sector_focus', 'commitment_eur', 'website']
    display_cols = [c for c in display_cols if c in df.columns]
    print(df[display_cols].to_string())
    print()


if __name__ == '__main__':
    main()
