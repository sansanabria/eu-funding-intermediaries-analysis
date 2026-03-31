"""
00 — Download & Parse EIF PDF Intermediary Lists
Project: EU Funding Intermediaries Analysis
Source: EIF official PDF reports (InvestEU equity intermediaries)
Purpose: Download the EIF PDF, extract ALL financial intermediaries, save as clean CSV

Usage:
    python 00_parse_eif_pdfs.py
    python 00_parse_eif_pdfs.py --no-cache    # re-download PDF

Output:
    ../01_data/processed/eif_pdf_intermediaries.csv  (all records, no filters)

Requirements:
    pip install pdfplumber requests pandas
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pdfplumber
import requests

# ── Configuration ─────────────────────────────────────────────────────

EIF_PDF_URL = 'https://www.eif.org/files/calls/ieu-equity-visibility-report-financial-intermediaries.pdf'
EIF_PDF_FILENAME = 'eif_equity_intermediaries.pdf'

DOWNLOAD_DIR = Path(__file__).parent.parent / '01_data' / 'raw' / 'eif_pdfs'
OUTPUT_PATH = Path(__file__).parent.parent / '01_data' / 'processed' / 'eif_pdf_intermediaries.csv'

# Column x-boundaries (derived from PDF header word positions)
COLUMNS = {
    'country':           (17, 53),
    'fund_name':         (54, 140),
    'financial_product': (141, 197),
    'fund_manager':      (198, 261),
    'address':           (262, 331),
    'target_area':       (332, 570),
    'support_type':      (571, 615),
    'sector_focus':      (616, 653),
    'currency':          (654, 680),
    'commitment':        (681, 729),
    'website':           (730, 820),
}

EU_COUNTRIES = {
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
    'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
    'Slovenia', 'Spain', 'Sweden', 'Multi-country',
}


# ── Download ──────────────────────────────────────────────────────────

def download_pdf(url, filepath):
    """Download the EIF PDF if not already cached."""
    if filepath.exists():
        print(f'  Using cached: {filepath.name}')
        return True

    print(f'  Downloading: {url}')
    try:
        resp = requests.get(url, timeout=60, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if resp.status_code == 200 and resp.content[:5] == b'%PDF-':
            filepath.write_bytes(resp.content)
            print(f'  Saved: {filepath.name} ({len(resp.content) / 1024:.0f} KB)')
            return True
        else:
            print(f'  Failed: not a valid PDF (HTTP {resp.status_code}).')
            return False
    except requests.RequestException as e:
        print(f'  Download error: {e}')
        return False


# ── PDF Parsing ───────────────────────────────────────────────────────

def extract_col(words, x_min, x_max, filter_short=False):
    """Extract text from words within an x-range.

    Args:
        filter_short: If True, remove single-character words (PDF garbling artifacts
                      from the vertically-rendered Financial Product column).
    """
    col_words = sorted([w for w in words if x_min <= w['x0'] < x_max], key=lambda w: w['x0'])
    if filter_short:
        col_words = [w for w in col_words if len(w['text']) >= 2 or w['text'] in '&()/,;.-']
    return ' '.join(w['text'] for w in col_words).strip()


def parse_pdf(filepath):
    """Parse the EIF PDF into a list of intermediary records.

    Strategy:
        The PDF has a multi-column table where the "Financial Product" column
        renders text vertically (individual characters), which garbles standard
        text extraction. We use word-level extraction with column x-boundaries
        to isolate each field. Records are anchored by rows containing a country
        name in the first column.
    """
    records = []

    with pdfplumber.open(filepath) as pdf:
        print(f'  Pages: {len(pdf.pages)}')

        for page in pdf.pages:
            words = page.extract_words()
            # Skip title/header area (y < 95)
            data_words = [w for w in words if w['top'] > 90]

            # Group words into y-bands (2-unit tolerance)
            rows = defaultdict(list)
            for w in data_words:
                y_key = round(w['top'] / 2) * 2
                rows[y_key].append(w)

            sorted_ys = sorted(rows.keys())

            # Find anchor rows (rows with a country name in x < 53)
            anchor_indices = []
            for idx, y_key in enumerate(sorted_ys):
                if any(w['x0'] < 53 and w['text'] in EU_COUNTRIES for w in rows[y_key]):
                    anchor_indices.append(idx)

            # Extract each record from its anchor row
            for i, anchor_idx in enumerate(anchor_indices):
                y_key = sorted_ys[anchor_idx]
                rw = rows[y_key]

                record = {}
                for col, (x0, x1) in COLUMNS.items():
                    # Filter single-char garbling in text-heavy columns
                    filt = col in ('fund_name', 'fund_manager', 'financial_product')
                    record[col] = extract_col(rw, x0, x1, filter_short=filt)

                # Fill empty fund_name from adjacent non-anchor rows
                if not record['fund_name'] or len(record['fund_name']) < 4:
                    record['fund_name'] = _find_in_adjacent_rows(
                        rows, sorted_ys, anchor_indices, i, anchor_idx, 54, 140
                    )

                # Fill empty fund_manager from adjacent rows
                if not record['fund_manager'] or len(record['fund_manager']) < 4:
                    fm = _find_in_adjacent_rows(
                        rows, sorted_ys, anchor_indices, i, anchor_idx, 198, 261
                    )
                    if fm:
                        record['fund_manager'] = fm

                records.append(record)

    return records


def _find_in_adjacent_rows(rows, sorted_ys, anchor_indices, i, anchor_idx, x_min, x_max):
    """Search adjacent non-anchor rows for text in a column range."""
    next_a = anchor_indices[i + 1] if i < len(anchor_indices) - 1 else len(sorted_ys)
    prev_a = anchor_indices[i - 1] if i > 0 else 0

    # Check rows above (between previous anchor and this one)
    for check_idx in range(anchor_idx - 1, max(prev_a, anchor_idx - 3), -1):
        if 0 <= check_idx < len(sorted_ys):
            text = extract_col(rows[sorted_ys[check_idx]], x_min, x_max, filter_short=True)
            if text and len(text) > 3:
                return text

    # Check rows below (between this anchor and next one)
    for check_idx in range(anchor_idx + 1, min(next_a, anchor_idx + 3)):
        if check_idx < len(sorted_ys):
            text = extract_col(rows[sorted_ys[check_idx]], x_min, x_max, filter_short=True)
            if text and len(text) > 3:
                return text

    return ''


# ── Post-processing ──────────────────────────────────────────────────

def clean_dataframe(records):
    """Convert parsed records to a clean DataFrame."""
    df = pd.DataFrame(records)

    # Clean commitment amount → numeric
    def parse_amount(val):
        if not val:
            return None
        numbers = re.findall(r'[\d,]+', str(val))
        if numbers:
            try:
                return float(numbers[0].replace(',', ''))
            except ValueError:
                return None
        return None

    df['commitment_eur'] = df['commitment'].apply(parse_amount)

    # Clean website URLs
    df['website'] = df['website'].apply(lambda x: x if x and x != 'NA' else '')

    # Clean fund_name: remove residual PDF artifacts
    def clean_name(name):
        if not name:
            return ''
        # Remove isolated single characters surrounded by spaces
        name = re.sub(r'(?<= )\w (?=\w)', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    df['fund_name'] = df['fund_name'].apply(clean_name)
    df['fund_manager'] = df['fund_manager'].apply(clean_name)

    # Select and order output columns
    output_cols = [
        'country', 'fund_name', 'fund_manager', 'financial_product',
        'target_area', 'support_type', 'sector_focus',
        'commitment_eur', 'currency', 'address', 'website',
    ]
    df = df[output_cols]

    return df


# ── Main ──────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Download and parse the EIF PDF intermediary list into CSV.',
    )
    parser.add_argument('--no-cache', action='store_true',
                        help='Re-download the PDF even if cached locally')
    parser.add_argument('--output', type=str, default=None,
                        help=f'Output CSV path (default: {OUTPUT_PATH})')
    args = parser.parse_args()

    print(f'\n{"="*70}')
    print(f'EIF PDF to CSV Converter')
    print(f'{"="*70}\n')

    # 1. Download
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DOWNLOAD_DIR / EIF_PDF_FILENAME

    if args.no_cache and filepath.exists():
        filepath.unlink()

    if not download_pdf(EIF_PDF_URL, filepath):
        print('\nFailed to download the PDF. Check the URL or try again later.')
        print(f'  URL: {EIF_PDF_URL}')
        sys.exit(1)

    # 2. Parse
    print('\nParsing PDF...')
    records = parse_pdf(filepath)
    print(f'  Extracted: {len(records)} records')

    if not records:
        print('\nNo records extracted. The PDF format may have changed.')
        sys.exit(1)

    # 3. Clean and export
    df = clean_dataframe(records)

    output_path = args.output or str(OUTPUT_PATH)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f'\n{"="*70}')
    print(f'RESULTS')
    print(f'{"="*70}')
    print(f'Total intermediaries: {len(df)}')
    print(f'Countries: {df["country"].nunique()}')
    print(f'Output: {output_path}')
    print(f'\nCountry breakdown:')
    print(df['country'].value_counts().to_string())
    print(f'\nSample records:')
    print(df[['country', 'fund_name', 'fund_manager', 'commitment_eur']].head(10).to_string())
    print()


if __name__ == '__main__':
    main()
