"""Build Constellation_Software_Financial_Model.xlsx with live formulas.
All company figures in USD millions, except per-share figures. Share price in CAD.
Price: C$3,395, close on 23 Oct 2026. FX: 1.40 CAD per USD on 23 Oct 2026.
Net debt at 31 Dec 2025: total debt US$5,787m less cash and investments US$3,141m = US$2,646m.
Shares: 21.19 million."""
import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = os.path.expanduser("~/workspace/your_files/constellation-software-equity-research")
df = pd.read_csv(os.path.join(BASE, "data", "csu_annual_2016_2025.csv"))
wb = Workbook()
NAVY = "1F3864"
BOLD = Font(bold=True)
HDR = PatternFill("solid", fgColor=NAVY)
WHITE = Font(bold=True, color="FFFFFF")

def sheet(title, headers, rows, widths=None):
    ws = wb.create_sheet(title) if title not in wb.sheetnames else wb[title]
    ws.append(headers)
    for c in ws[1]:
        c.fill = HDR
        c.font = WHITE
    for r in rows:
        ws.append(r)
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return ws

# Historical sheet, with formulas for FCF, margins, ROIC where inputs allow
ws = wb.active
ws.title = "Historical"
headers = ["Year", "Revenue", "Operating income", "Net income attributable", "Operating cash flow",
           "Capex", "Free cash flow (formula)", "Depreciation and amortisation", "Owner earnings proxy (formula)",
           "Dividends paid", "Other investing outflow (proxy)", "Invested capital", "Pre-tax ROIC % (formula)"]
ws.append(headers)
for c in ws[1]:
    c.fill = HDR
    c.font = WHITE
for i, row in df.iterrows():
    r = i + 2
    ws.append([int(row["year"]), float(row["revenue_usd_m"]), float(row["operating_income_usd_m"]),
               float(row["net_income_attributable_usd_m"]), float(row["operating_cash_flow_usd_m"]),
               float(row["capex_usd_m"]), f"=E{r}-F{r}", float(row["depreciation_amortisation_usd_m"]),
               f"=D{r}+H{r}-F{r}", float(row["dividends_paid_usd_m"]),
               float(row["other_investing_outflow_usd_m"]), float(row["invested_capital_usd_m"]),
               f"=IF(ROW()=2,\"n/a\",C{r}/AVERAGE(L{r-1}:L{r})*100)"])
for i, w in enumerate([8, 12, 16, 20, 18, 10, 20, 24, 24, 14, 24, 16, 20], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.append([])
ws.append(["Notes: USD millions. Revenue, operating income, net income, operating cash flow, capex, dividends and debt/cash from StockAnalysis, AlphaSpread, MacroTrends and company reports, as listed in the README. Other investing outflow is a proxy for acquisition spending, not a verified acquisition-only line. ROIC is pre-tax operating income divided by average invested capital. 2016 ROIC is shown as n/a because 2015 invested capital was not verified on the same basis."])

# DCF sheet with live formulas
ws2 = wb.create_sheet("DCF")
ws2["A1"] = "DCF inputs"
ws2["A1"].font = BOLD
inputs = [
    ("2025 free cash flow (USD millions)", 2664),
    ("Shares outstanding (millions)", 21.19),
    ("Net debt at 31 Dec 2025 (USD millions)", 2646),
    ("Share price, 23 Oct 2026 (CAD)", 3395),
    ("FX, CAD per USD, 23 Oct 2026", 1.40),
]
for i, (k, v) in enumerate(inputs, 2):
    ws2.cell(row=i, column=1, value=k)
    ws2.cell(row=i, column=2, value=v)
ws2.column_dimensions["A"].width = 44
ws2.column_dimensions["B"].width = 18
ws2.column_dimensions["C"].width = 18
ws2.column_dimensions["D"].width = 18
ws2.column_dimensions["E"].width = 18
# Cases in rows 8-10: Case, Growth, WACC, Terminal growth
ws2["A8"] = "Case"
ws2["B8"] = "FCF growth"
ws2["C8"] = "Discount rate"
ws2["D8"] = "Terminal growth"
ws2["E8"] = "Value per share (CAD, formula)"
for c in ws2[8]:
    c.fill = HDR
    c.font = WHITE
cases = [("Base", 0.08, 0.09, 0.03), ("Optimistic", 0.12, 0.08, 0.035), ("Pessimistic", 0.04, 0.105, 0.02)]
for j, (name, g, w, t) in enumerate(cases, 9):
    ws2.cell(row=j, column=1, value=name)
    ws2.cell(row=j, column=2, value=g).number_format = "0.0%"
    ws2.cell(row=j, column=3, value=w).number_format = "0.0%"
    ws2.cell(row=j, column=4, value=t).number_format = "0.0%"
    # Forecast FCF years 1-5 are in the Forecast sheet; here value = (PV of 5 years + PV of terminal value - net debt) / shares * FX
    # Forecast sheet rows: base 2-6, optimistic 7-11, pessimistic 12-16, with PV in column C
    start = 2 + (j - 9) * 5
    end = start + 4
    ws2.cell(row=j, column=5, value=f"=(SUM(Forecast!C{start}:C{end})-B4)/B3*B6").number_format = "#,##0"
    # Note: terminal value PV is included as a separate line in Forecast column D, so add it below in a second formula step:
    ws2.cell(row=j, column=5, value=f"=(SUM(Forecast!C{start}:C{end})+Forecast!D{end}-B4)/B3*B6").number_format = "#,##0"

ws3 = wb.create_sheet("Forecast")
ws3.append(["Case", "Year", "PV of FCF (USD millions, formula)", "PV of terminal value (USD millions, formula)"])
for c in ws3[1]:
    c.fill = HDR
    c.font = WHITE
row = 2
for name, g, w, t in cases:
    for yr in range(1, 6):
        ws3.cell(row=row, column=1, value=name)
        ws3.cell(row=row, column=2, value=2025 + yr)
        # FCF = 2664 * (1+g)^yr ; PV = FCF / (1+w)^yr ; inputs are on DCF sheet B2, growth/discount in DCF rows 9-11
        case_row = 9 + cases.index((name, g, w, t))
        ws3.cell(row=row, column=3, value=f"=$B$2*(1+DCF!B{case_row})^{yr}/(1+DCF!C{case_row})^{yr}").number_format = "#,##0"
        if yr == 5:
            ws3.cell(row=row, column=4, value=f"=($B$2*(1+DCF!B{case_row})^5*(1+DCF!D{case_row})/(DCF!C{case_row}-DCF!D{case_row}))/(1+DCF!C{case_row})^5").number_format = "#,##0"
        row += 1
for i, w_ in enumerate([14, 10, 32, 36], 1):
    ws3.column_dimensions[get_column_letter(i)].width = w_
# Fix DCF input references: B2 in this file is on DCF sheet, so Forecast formulas must point to DCF!B2
for r in range(2, 17):
    for col in (3, 4):
        cell = ws3.cell(row=r, column=col)
        if cell.value and isinstance(cell.value, str):
            cell.value = cell.value.replace("$B$2", "DCF!$B$2")
# DCF sheet input references: net debt is B4? Inputs list: row2 FCF, row3 shares, row4 net debt, row5 price, row6 FX. Correct.
# Sensitivity sheet: growth rows, WACC columns, terminal growth 3%, formula replicates DCF value
ws4 = wb.create_sheet("Sensitivity")
ws4["A1"] = "Value per share (CAD) at terminal growth 3%. Rows: FCF growth. Columns: discount rate."
ws4["A1"].font = BOLD
for j, w_ in enumerate([0.08, 0.09, 0.10, 0.11], 2):
    ws4.cell(row=2, column=j, value=w_).number_format = "0%"
for i, g in enumerate([0.04, 0.06, 0.08, 0.10, 0.12], 3):
    ws4.cell(row=i, column=1, value=g).number_format = "0%"
    for j, w_ in enumerate([0.08, 0.09, 0.10, 0.11], 2):
        # Closed-form: PV of 5 years + PV of terminal value, less net debt, per share, times FX
        terms = "+".join([f"DCF!$B$2*(1+$A{i})^{k}/(1+{w_})^{k}" for k in range(1, 6)])
        ws4.cell(row=i, column=j, value=(
            f"=( {terms} +(DCF!$B$2*(1+$A{i})^5*1.03/({w_}-0.03))/(1+{w_})^5"
            f"-DCF!$B$4)/DCF!$B$3*DCF!$B$6"
        )).number_format = "#,##0"
ws4.column_dimensions["A"].width = 14
for col in "BCDE":
    ws4.column_dimensions[col].width = 14

wb.save(os.path.join(BASE, "Constellation_Software_Financial_Model.xlsx"))
print("model built")
