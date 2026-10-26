"""Build analysis.ipynb, executed with nbconvert."""
import os, subprocess, sys
import nbformat as nbf

BASE = os.path.expanduser("~/workspace/your_files/constellation-software-equity-research")
nb = nbf.v4.new_notebook()
nb.metadata = {"kernelspec": {"display_name": "tdvenv", "language": "python", "name": "tdvenv"},
               "language_info": {"name": "python", "version": "3.12"}}
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))

md("""# Constellation Software Inc. (TSX: CSU): Buffett-style investment memo
Date: October 2026. Price used: C$3,395, close on 23 Oct 2026. Company figures in USD millions. Share price in CAD.
This notebook is analysis for learning and portfolio use. It is not investment advice.
Method in brief: business model, competitive advantage, cash generation, capital allocation, risks, and valuation.
Sources are listed in the README and in the report. Secondary data sources differ in rounding, so figures are shown to the nearest million.""")

code("""import pandas as pd, numpy as np
pd.set_option("display.width", 200)
df = pd.read_csv("data/csu_annual_2016_2025.csv")
df""")

md("""## 1. Ten years: revenue, profit, and cash
Net income attributable is the profit for common shareholders. Total net income in some years differs because of noncontrolling interests and revaluation items. That difference is a key point in this memo: reported profit alone does not show cash generation.""")

code("""df["revenue_growth_pct"] = df["revenue_usd_m"].pct_change() * 100
df["operating_margin_pct"] = df["operating_income_usd_m"] / df["revenue_usd_m"] * 100
df["fcf_margin_pct"] = df["free_cash_flow_usd_m"] / df["revenue_usd_m"] * 100
df[["year", "revenue_usd_m", "revenue_growth_pct", "operating_income_usd_m", "operating_margin_pct",
    "net_income_attributable_usd_m", "operating_cash_flow_usd_m", "free_cash_flow_usd_m", "fcf_margin_pct"]].round(1)""")

code("""print("Revenue CAGR 2016 to 2025:", round(((11623/2125) ** (1/9) - 1) * 100, 1), "%")
print("Free cash flow CAGR 2016 to 2025:", round(((2664/472) ** (1/9) - 1) * 100, 1), "%")
print("Recurring revenue share 2024: 7,396 / 10,066 =", round(7396/10066 * 100, 1), "%")
print("Recurring revenue share 2025: 8,700 / 11,623 =", round(8700/11623 * 100, 1), "%")""")

md("""## 2. Owner earnings proxy and pre-tax return on invested capital
Owner earnings proxy = net income attributable + depreciation and amortisation - capital expenditure.
This proxy is an upper bound. Depreciation and amortisation includes amortisation of acquired intangibles, and that amortisation reflects part of the price paid for acquisitions. Free cash flow is shown beside it for comparison.
Invested capital = total equity attributable + minority interest + interest-bearing debt - cash and short-term investments.
Pre-tax return on invested capital = operating income / average invested capital. 2016 is not shown because 2015 invested capital was not verified on the same basis.""")

code("""df["avg_invested_capital"] = df["invested_capital_usd_m"].rolling(2).mean()
df["roic_pre_tax_pct"] = df["operating_income_usd_m"] / df["avg_invested_capital"] * 100
df[["year", "net_income_attributable_usd_m", "depreciation_amortisation_usd_m", "capex_usd_m",
    "owner_earnings_proxy_usd_m", "free_cash_flow_usd_m", "invested_capital_usd_m", "roic_pre_tax_pct"]].round(1)""")

md("""## 3. Capital allocation
Free cash flow is the cash after operating cash flow less capital expenditure. Other investing outflow is used as a proxy for acquisition spending. It is not a verified acquisition-only line, and the report states that limit. Dividends paid stayed near US$85 million in most years, except 2019, when the reported figure was US$509 million.""")

code("""df[["year", "free_cash_flow_usd_m", "other_investing_outflow_usd_m", "dividends_paid_usd_m"]].round(0)
print("Total free cash flow 2016 to 2025 (USD millions):", int(df["free_cash_flow_usd_m"].sum()))
print("Total other investing outflow 2016 to 2025 (USD millions):", int(df["other_investing_outflow_usd_m"].sum()))
print("Total dividends paid 2016 to 2025 (USD millions):", int(df["dividends_paid_usd_m"].sum()))""")

md("""## 4. Valuation check: price against free cash flow
Market value at the price used: 21.19 million shares x C$3,395 = C$71,940 million. At 1.40 CAD per USD, that is US$51,386 million. Divided by 2025 free cash flow of US$2,664 million, the multiple is 19.3 times. The full DCF, with cases and sensitivities, is in the Excel model.""")

code("""shares = 21.19
price_cad = 3395
fx = 1.40
market_value_cad = shares * price_cad
market_value_usd = market_value_cad / fx
print("Market value (CAD millions):", round(market_value_cad, 0))
print("Market value (USD millions):", round(market_value_usd, 0))
print("Price / 2025 free cash flow:", round(market_value_usd / 2664, 1))
print("Price in USD:", round(price_cad / fx, 0))
print("2025 earnings per share, attributable (USD): 24.15, from StockAnalysis")
print("Price in USD / 2025 earnings per share:", round((price_cad / fx) / 24.15, 1))""")

md("""## 5. Charts
Charts are built by scripts/build_charts.py and saved in charts/.""")

code("""from IPython.display import Image, display
for name in ["revenue_vs_income.png", "roic_and_owner_earnings.png", "capital_allocation.png", "price_history.png", "football_field.png"]:
    display(Image(filename=f"charts/{name}"))""")

nb.cells = cells
path = os.path.join(BASE, "analysis.ipynb")
nbf.write(nb, path)
subprocess.run([sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute",
                "--inplace", "--ExecutePreprocessor.timeout=120", path],
               cwd=BASE, check=True)
print("notebook built")
