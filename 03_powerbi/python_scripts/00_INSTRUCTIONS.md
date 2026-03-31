# How to Use These Scripts in Power BI Desktop

## Step 1 — Enable Python in Power BI Desktop
1. Open Power BI Desktop
2. Go to **File → Options and Settings → Options**
3. Click **Python scripting** (left menu)
4. Set the Python home directory to where Python is installed on your computer
   - Usually: `C:\Python3xx` or `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python3xx`
5. Click **OK**

---

## Step 2 — Load Your Data (do this FIRST)
1. Click **Home → Get Data → More → Other → Python Script**
2. Paste the contents of **`01_load_data.py`**
3. Click **OK**
4. Power BI will show a Navigator — check the `df` table and click **Load**
5. Your data is now in Power BI as a table called `df`

---

## Step 3 — Add Python Visuals (one per chart)
For each chart you want to add:
1. In the **Visualizations** pane, click the **Python visual** icon (Py)
2. A yellow warning bar will appear — click **Enable**
3. In the **Values** field, drag in the columns listed at the top of each script
4. The Python script editor appears at the bottom of the screen
5. **Delete** the placeholder code Power BI puts there
6. **Paste** the script for that chart
7. Click the **Run** button (▶)

---

## Scripts & What They Build

| Script | Visual | Columns Needed |
|---|---|---|
| `01_load_data.py` | Data source | — |
| `02_kpi_overview.py` | KPI summary table | All columns |
| `03_eif_commitment_bar.py` | EIF commitment by manager | manager_name, eif_commitment_eur |
| `04_fund_type_pie.py` | Fund type donut chart | fund_type, eif_commitment_eur |
| `05_project_fit_bar.py` | Solar/Hydrogen/Desalination fit | manager_name, solar_fit, hydrogen_fit, desalination_fit |
| `06_strategic_scores.py` | Ranked scoring chart | manager_name, score_project_fit, score_commitment, score_sdg, score_contact, score_geography, fit_score_10 |
| `07_sdg_heatmap.py` | SDG alignment heatmap | manager_name, sdg_tags |
| `08_country_bar.py` | Country distribution | country_primary, eif_commitment_eur |

---

## Tips
- If a visual shows an error, check that you dragged the correct columns into **Values**
- Power BI passes your selected columns as a dataframe called `dataset`
- Each script uses `dataset` as its input — do not rename it
- To resize a visual, drag its corners like any other Power BI visual
