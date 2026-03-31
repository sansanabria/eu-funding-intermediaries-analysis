"""
Build pitch_deck.pdf — 8-slide executive presentation for CEO/COO.
Senior-quality layout with polished typography, consistent branding.
"""
import os
import pandas as pd
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', '01_data', 'processed', 'eif_fund_managers_clean.csv')
CHARTS = os.path.join(BASE, '..', '03_powerbi', 'screenshots')
OUT = os.path.join(BASE, 'pitch_deck.pdf')

# ── Brand palette ──
NAVY_DK   = (25/255, 45/255, 75/255)
NAVY      = (35/255, 60/255, 100/255)
STEEL     = (75/255, 100/255, 140/255)
COPPER    = (170/255, 125/255, 60/255)
COPPER_LT = (210/255, 185/255, 140/255)
SAGE      = (55/255, 125/255, 85/255)
SAGE_LT   = (220/255, 238/255, 228/255)
ROSE      = (155/255, 80/255, 80/255)
ROSE_LT   = (242/255, 228/255, 228/255)
TEAL      = (55/255, 120/255, 130/255)
TXT       = (30/255, 35/255, 50/255)
TXT_MED   = (90/255, 100/255, 120/255)
TXT_LT    = (150/255, 158/255, 175/255)
WHITE     = (1, 1, 1)
SURFACE   = (248/255, 249/255, 252/255)
SURF2     = (237/255, 240/255, 247/255)
BORDER    = (220/255, 225/255, 235/255)

PW = 13.33 * inch
PH = 7.5 * inch
MX = 55  # horizontal margin
TOTAL_SLIDES = 8

# ── Load & clean data ──
df = pd.read_csv(DATA, encoding='utf-8-sig')
df['eif_commitment_eur'] = pd.to_numeric(df['eif_commitment_eur'], errors='coerce')
df['fit_score_10'] = pd.to_numeric(df['fit_score_10'], errors='coerce')
df['solar_fit'] = pd.to_numeric(df['solar_fit'], errors='coerce').fillna(0).astype(int)
df['hydrogen_fit'] = pd.to_numeric(df['hydrogen_fit'], errors='coerce').fillna(0).astype(int)
df['desalination_fit'] = pd.to_numeric(df['desalination_fit'], errors='coerce').fillna(0).astype(int)

def _clean(raw, country):
    raw = str(raw).strip()
    if 'Impact Bridge' in raw:
        if 'AgriFood' in raw or 'Carlos de Abajo' in raw: return 'Impact Bridge AgriFood'
        if 'MicroBank' in raw or 'Cristina Gonz' in raw: return 'Impact Bridge MicroBank'
        if 'Rebecca Eastmond' in raw or 'Greenwood' in raw: return 'Impact Bridge Impact Debt'
        if 'Louisa Brassey' in raw or 'Lucille' in raw: return 'Impact Bridge Direct Debt'
        return 'Impact Bridge Global'
    for k, v in {'Suma Capital': 'Suma Capital SGEIC SA', 'Arta Capital': 'Arta Capital Fund III',
                  'Axon Partners': 'Axon Partners Group', 'Alantra': 'Alantra Multi Asset SGIIC',
                  'NIAM': 'NIAM Infrastructure', 'Norrsken': 'Norrsken Impact Accelerator',
                  'OXY Capital': 'OXY Capital'}.items():
        if k in raw: return v
    return raw[:40]

df['short_name'] = df.apply(lambda r: _clean(r['manager_name'], r['country_primary']), axis=1)
df_sorted = df.sort_values('fit_score_10', ascending=False).reset_index(drop=True)


# ── Shared drawing helpers ──
def draw_header(c, title, subtitle=None, page_num=1, full_height=False):
    h = PH * 0.48 if full_height else 82
    # Dark navy bar
    c.setFillColorRGB(*NAVY_DK)
    c.rect(0, PH - h, PW, h, fill=1, stroke=0)

    if full_height:
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 44)
        c.drawCentredString(PW/2, PH - 120, 'EU FUNDING INTERMEDIARIES')
        c.setFillColorRGB(*COPPER_LT)
        c.setFont('Helvetica-Bold', 44)
        c.drawCentredString(PW/2, PH - 175, 'ANALYSIS')
    else:
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 24)
        c.drawString(MX, PH - 48, title)
        if subtitle:
            c.setFillColorRGB(*COPPER_LT)
            c.setFont('Helvetica', 10)
            c.drawString(MX, PH - 66, subtitle)
        # Page indicator
        c.setFillColorRGB(45/255, 70/255, 110/255)
        bw = 42
        bx = PW - MX - bw
        c.roundRect(bx, PH - 55, bw, 20, 3, fill=1, stroke=0)
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica', 7)
        c.drawCentredString(bx + bw/2, PH - 49, f'{page_num} / {TOTAL_SLIDES}')

    draw_footer(c, page_num)


def draw_footer(c, page_num):
    # Footer line
    c.setStrokeColorRGB(*BORDER)
    c.setLineWidth(0.3)
    c.line(MX, 28, PW - MX, 28)
    # Source
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 6)
    c.drawString(MX, 16, 'Source: European Commission  //  Your Europe Portal  //  EIF Financial Intermediaries Database')
    c.drawRightString(PW - MX, 16, 'Q1 2025')


def draw_kpi(c, x, y, w, h, value, label, accent):
    # Card with border
    c.setFillColorRGB(*SURFACE)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    c.setStrokeColorRGB(*BORDER)
    c.setLineWidth(0.3)
    c.roundRect(x, y, w, h, 3, fill=0, stroke=1)
    # Accent top
    c.setFillColorRGB(*accent)
    c.rect(x + 1, y + h - 3, w - 2, 3, fill=1, stroke=0)
    # Value
    c.setFillColorRGB(*NAVY_DK)
    fs = 20 if len(value) > 6 else 26
    c.setFont('Helvetica-Bold', fs)
    c.drawCentredString(x + w/2, y + h/2 - 8, value)
    # Label
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 8)
    c.drawCentredString(x + w/2, y + 10, label)


# ================================================================
#  SLIDES
# ================================================================
def slide_title(c):
    draw_header(c, '', page_num=1, full_height=True)
    # Subtitle inside navy area
    c.setFillColorRGB(*COPPER_LT)
    c.setFont('Helvetica', 13)
    c.drawCentredString(PW/2, PH * 0.48 + 22, 'EIF Financial Intermediaries Research & Analysis')
    # White area content
    c.setFillColorRGB(*TXT)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(PW/2, PH * 0.35, 'Prepared for CEO, COO & Management Team')
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 11)
    c.drawCentredString(PW/2, PH * 0.27, 'European Commission  //  Your Europe Portal  //  Q1 2025')


def slide_metrics(c):
    draw_header(c, 'Key Metrics', 'Portfolio overview across 12 financial intermediaries', 2)
    total = len(df)
    countries = df['country_primary'].nunique()
    capital = f"EUR {df['eif_commitment_eur'].sum()/1e6:.0f}M"
    kpis = [
        (str(total), 'Fund Managers', NAVY),
        (str(countries), 'Countries', STEEL),
        (capital, 'EIF Capital Deployed', COPPER),
        (str(int(df['solar_fit'].sum())), 'Solar Fit', SAGE),
        (str(int(df['hydrogen_fit'].sum())), 'Hydrogen Fit', TEAL),
        (str(int(df['desalination_fit'].sum())), 'Desalination Fit', ROSE),
    ]
    card_w = 130
    gap = 16
    total_w = 6 * card_w + 5 * gap
    sx = (PW - total_w) / 2
    for i, (val, lab, acc) in enumerate(kpis):
        draw_kpi(c, sx + i * (card_w + gap), PH - 180, card_w, 70, val, lab, acc)

    chart_path = os.path.join(CHARTS, 'project_fit_coverage.png')
    if os.path.exists(chart_path):
        c.drawImage(chart_path, MX, 45, PW - 2*MX, PH - 300,
                   preserveAspectRatio=True, mask='auto')


def slide_rankings(c):
    draw_header(c, 'Fund Manager Rankings', 'Sorted by strategic fit score  //  12 intermediaries across 5 countries', 3)

    cols_def = [
        ('#',              MX,       25),
        ('FUND MANAGER',   MX+28,    260),
        ('COUNTRY',        MX+295,   140),
        ('TYPE',           MX+440,   70),
        ('EIF COMMITMENT', MX+515,   120),
        ('SCORE',          MX+640,   70),
        ('TIER',           MX+720,   PW-2*MX-720),
    ]

    header_y = PH - 130
    row_h = 28

    # Header
    c.setFillColorRGB(*NAVY_DK)
    c.rect(MX, header_y, PW - 2*MX, row_h, fill=1, stroke=0)
    c.setFillColorRGB(*WHITE)
    c.setFont('Helvetica-Bold', 7)
    for name, cx, cw in cols_def:
        c.drawString(cx + 4, header_y + 10, name)

    tier_meta = {
        'Tier 1 - Priority':  ('PRIORITY',  SAGE,  SAGE_LT),
        'Tier 2 - Secondary': ('SECONDARY', COPPER, (245/255, 238/255, 225/255)),
        'Tier 3 - Monitor':   ('MONITOR',   ROSE,  ROSE_LT),
    }

    for i, (_, row) in enumerate(df_sorted.iterrows()):
        y = header_y - (i + 1) * row_h
        tier = row.get('priority_tier', '')
        bg = SURFACE if i % 2 == 0 else WHITE
        c.setFillColorRGB(*bg)
        c.rect(MX, y, PW - 2*MX, row_h, fill=1, stroke=0)
        c.setStrokeColorRGB(*BORDER)
        c.setLineWidth(0.2)
        c.line(MX, y, PW - MX, y)

        ty = y + 10

        # #
        c.setFillColorRGB(*TXT_LT)
        c.setFont('Helvetica', 7)
        c.drawRightString(cols_def[0][1] + 20, ty, str(i + 1))

        # Name
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica', 8)
        c.drawString(cols_def[1][1] + 4, ty, row['short_name'][:35])

        # Country
        c.setFillColorRGB(*STEEL)
        c.setFont('Helvetica', 7.5)
        c.drawString(cols_def[2][1] + 4, ty, str(row['country_primary']))

        # Type
        c.setFillColorRGB(*TXT_MED)
        c.setFont('Helvetica', 7.5)
        c.drawString(cols_def[3][1] + 4, ty, str(row.get('fund_type', '')))

        # EIF
        eif = row['eif_commitment_eur']
        if pd.notna(eif) and eif > 100:
            c.setFillColorRGB(*COPPER)
            c.setFont('Helvetica-Bold', 7.5)
            c.drawRightString(cols_def[4][1] + cols_def[4][2] - 4, ty, f'{eif/1e6:,.1f}M')
        else:
            c.setFillColorRGB(*TXT_LT)
            c.setFont('Helvetica', 7.5)
            c.drawRightString(cols_def[4][1] + cols_def[4][2] - 4, ty, '\u2014')

        # Score bar + number
        score = row['fit_score_10']
        if pd.notna(score):
            sx = cols_def[5][1] + 4
            bw, bh = 30, 10
            by = y + 9
            c.setFillColorRGB(*SURF2)
            c.roundRect(sx, by, bw, bh, 2, fill=1, stroke=0)
            c.setFillColorRGB(*NAVY)
            c.roundRect(sx, by, max((score/10)*bw, 3), bh, 2, fill=1, stroke=0)
            c.setFillColorRGB(*NAVY_DK)
            c.setFont('Helvetica-Bold', 7.5)
            c.drawString(sx + bw + 4, ty, f'{score:.1f}')

        # Tier badge
        tm = tier_meta.get(tier)
        if tm:
            tl, tc, tbg = tm
            bx = cols_def[6][1] + 4
            badge_w = c.stringWidth(tl, 'Helvetica-Bold', 6.5) + 14
            c.setFillColorRGB(*tbg)
            c.roundRect(bx, y + 8, badge_w, 14, 3, fill=1, stroke=0)
            c.setFillColorRGB(*tc)
            c.setFont('Helvetica-Bold', 6.5)
            c.drawCentredString(bx + badge_w/2, y + 12, tl)

    # Bottom border
    c.setStrokeColorRGB(*NAVY)
    c.setLineWidth(0.5)
    y_bottom = header_y - len(df_sorted) * row_h
    c.line(MX, y_bottom, PW - MX, y_bottom)


def slide_eif(c):
    draw_header(c, 'EIF Commitment', 'Capital allocated per financial intermediary', 4)
    chart_path = os.path.join(CHARTS, 'eif_commitments.png')
    if os.path.exists(chart_path):
        c.drawImage(chart_path, MX, 45, PW - 2*MX, PH - 155,
                   preserveAspectRatio=True, mask='auto')


def slide_strategic(c):
    draw_header(c, 'Strategic Fit Scoring', 'Project Fit  //  EIF Commitment  //  SDG  //  Contact  //  Geography', 5)
    chart_path = os.path.join(CHARTS, 'strategic_scores.png')
    if os.path.exists(chart_path):
        c.drawImage(chart_path, MX, 45, PW - 2*MX, PH - 155,
                   preserveAspectRatio=True, mask='auto')


def slide_findings(c):
    draw_header(c, 'Key Findings', 'Strategic insights from the intermediary analysis', 6)

    findings = [
        ('Spain Hub', '7 of 12 fund managers based in Spain \u2014 strongest EIF entry point for our projects.', NAVY),
        ('Solar Coverage', 'Broadest fund coverage: 9 intermediaries support solar, giving developers multiple options.', COPPER),
        ('Desalination Gap', 'No fund directly targets desalination. Best route: SDG 6/14 alignment via Impact Bridge.', ROSE),
        ('Hydrogen Strategy', 'Multi-fund approach required: Suma Capital + Impact Bridge + Axon Partners Group.', TEAL),
        ('Nordic Scale', 'NIAM at EUR 5.2M \u2014 largest single commitment, ideal for infrastructure-scale capital.', SAGE),
        ('SDG Readiness', 'Impact funds require measurable metrics. Prepare quantifiable data before outreach.', STEEL),
    ]

    card_h = 58
    gap = 8
    start_y = PH - 140
    margin = 80

    for i, (title, desc, accent) in enumerate(findings):
        y = start_y - i * (card_h + gap)

        # Card
        c.setFillColorRGB(*SURFACE)
        c.roundRect(margin, y, PW - 2*margin, card_h, 4, fill=1, stroke=0)
        c.setStrokeColorRGB(*BORDER)
        c.setLineWidth(0.2)
        c.roundRect(margin, y, PW - 2*margin, card_h, 4, fill=0, stroke=1)

        # Left accent
        c.setFillColorRGB(*accent)
        c.rect(margin, y + 4, 3, card_h - 8, fill=1, stroke=0)

        # Number
        c.setFillColorRGB(*SURF2)
        cx = margin + 32
        cy = y + card_h/2
        c.circle(cx, cy, 16, fill=1, stroke=0)
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica-Bold', 12)
        c.drawCentredString(cx, cy - 4, str(i + 1))

        # Title
        c.setFillColorRGB(*accent)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(margin + 60, y + card_h - 20, title)

        # Desc
        c.setFillColorRGB(*TXT_MED)
        c.setFont('Helvetica', 9)
        c.drawString(margin + 60, y + 14, desc[:90])


def slide_framework(c):
    draw_header(c, 'Decision Framework', 'Does EU funding apply to your company?', 7)

    steps = [
        ('01', 'LOCATION', 'EU27, EEA, outermost regions, or associated countries?', NAVY),
        ('02', 'COMPANY', 'Startup, SME, mid-cap, or infrastructure project?', STEEL),
        ('03', 'FINANCE', 'Loans, venture capital, microfinance, or grants?', COPPER),
        ('04', 'PARTNER', 'EIF, EIB, InvestEU, or national promotional banks?', ROSE),
        ('05', 'AMOUNT', 'From under EUR 500K to EUR 50M+?', TEAL),
        ('06', 'SDG', 'Which sustainable development goals apply?', SAGE),
        ('07', 'OUTPUT', 'Your filtered shortlist with direct portal link.', NAVY),
    ]

    start_y = PH - 140
    row_h = 52
    margin = 80

    for i, (num, label, desc, accent) in enumerate(steps):
        y = start_y - i * (row_h + 6)

        # Number pill
        c.setFillColorRGB(*accent)
        c.roundRect(margin, y, 48, 40, 4, fill=1, stroke=0)
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(margin + 24, y + 13, num)

        # Label badge
        c.setFillColorRGB(*SURFACE)
        c.roundRect(margin + 60, y, 130, 40, 4, fill=1, stroke=0)
        c.setStrokeColorRGB(*BORDER)
        c.setLineWidth(0.2)
        c.roundRect(margin + 60, y, 130, 40, 4, fill=0, stroke=1)
        c.setFillColorRGB(*accent)
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(margin + 125, y + 13, label)

        # Arrow
        c.setFillColorRGB(*TXT_LT)
        c.setFont('Helvetica', 12)
        c.drawString(margin + 200, y + 13, '\u203a')

        # Description
        c.setFillColorRGB(*SURFACE)
        dw = PW - 2*margin - 230
        c.roundRect(margin + 220, y, dw, 40, 4, fill=1, stroke=0)
        c.setStrokeColorRGB(*BORDER)
        c.roundRect(margin + 220, y, dw, 40, 4, fill=0, stroke=1)
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica', 9.5)
        c.drawCentredString(margin + 220 + dw/2, y + 13, desc)


def slide_actions(c):
    draw_header(c, 'Recommended Actions', 'Prioritized by timeline and strategic impact', 8)

    actions = [
        ('IMMEDIATE', 'Outreach to Tier 1 targets: Suma Capital (8.0/10) and Impact Bridge Global (7.0/10).', ROSE),
        ('Q2 2025', 'Prepare SDG-aligned pitch deck with quantifiable impact metrics for fund managers.', COPPER),
        ('Q2 2025', 'Develop Portugal strategy via OXY Capital \u2014 solar and green hydrogen focus.', COPPER),
        ('Q3 2025', 'Submit application for Norrsken Impact Accelerator 2026 cohort.', TEAL),
        ('ONGOING', 'Expand intermediary research across all 27 EU member states.', SAGE),
    ]

    start_y = PH - 140
    row_h = 70
    margin = 80

    for i, (timeline, desc, accent) in enumerate(actions):
        y = start_y - i * (row_h + 8)

        # Timeline pill
        c.setFillColorRGB(*accent)
        c.roundRect(margin, y, 140, 45, 5, fill=1, stroke=0)
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 11)
        c.drawCentredString(margin + 70, y + 16, timeline)

        # Description card
        cx = margin + 160
        cw = PW - 2*margin - 160
        c.setFillColorRGB(*SURFACE)
        c.roundRect(cx, y, cw, 45, 4, fill=1, stroke=0)
        c.setStrokeColorRGB(*BORDER)
        c.setLineWidth(0.2)
        c.roundRect(cx, y, cw, 45, 4, fill=0, stroke=1)
        # Left accent
        c.setFillColorRGB(*accent)
        c.rect(cx, y + 4, 3, 37, fill=1, stroke=0)
        # Text
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica', 10)
        c.drawCentredString(cx + cw/2, y + 16, desc)

    # Bottom CTA
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 9)
    c.drawCentredString(PW/2, 50, 'European Commission  //  Your Europe Portal  //  Q1 2025')


# ================================================================
#  BUILD
# ================================================================
def build():
    c_pdf = canvas.Canvas(OUT, pagesize=(PW, PH))

    slides = [
        slide_title, slide_metrics, slide_rankings, slide_eif,
        slide_strategic, slide_findings, slide_framework, slide_actions,
    ]

    for i, fn in enumerate(slides):
        if i > 0:
            c_pdf.showPage()
        c_pdf.setFillColorRGB(*WHITE)
        c_pdf.rect(0, 0, PW, PH, fill=1, stroke=0)
        fn(c_pdf)

    c_pdf.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
