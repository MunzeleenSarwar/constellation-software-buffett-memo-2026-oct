"""Build charts for the Constellation Software memo. All figures in USD millions unless stated."""
import os, json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.expanduser("~/workspace/your_files/constellation-software-equity-research")
CH = os.path.join(BASE, "charts")
os.makedirs(CH, exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "axes.grid": True, "grid.alpha": 0.3, "font.size": 9})
df = pd.read_csv(os.path.join(BASE, "data", "csu_annual_2016_2025.csv"))
years = df["year"].tolist()

# 1. Revenue vs net income attributable
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.bar([y - 0.2 for y in years], df["revenue_usd_m"], width=0.4, label="Revenue")
ax.bar([y + 0.2 for y in years], df["net_income_attributable_usd_m"], width=0.4, label="Net income attributable")
ax.set_title("Revenue and net income attributable, 2016 to 2025 (USD millions)")
ax.set_ylabel("USD millions")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(CH, "revenue_vs_income.png"))
plt.close(fig)

# 2. ROIC (pre-tax) and owner earnings proxy
df["avg_ic"] = df["invested_capital_usd_m"].rolling(2).mean()
df["roic_pre_tax_pct"] = df["operating_income_usd_m"] / df["avg_ic"] * 100
fig, ax1 = plt.subplots(figsize=(8, 3.6))
ax1.plot(years, df["owner_earnings_proxy_usd_m"], marker="o", label="Owner earnings proxy")
ax1.plot(years, df["free_cash_flow_usd_m"], marker="s", label="Free cash flow")
ax1.set_ylabel("USD millions")
ax2 = ax1.twinx()
ax2.plot(years, df["roic_pre_tax_pct"], marker="^", color="green", label="Pre-tax return on invested capital (%)")
ax2.set_ylabel("Percent")
ax1.set_title("Owner earnings proxy, free cash flow, and pre-tax return on invested capital")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(CH, "roic_and_owner_earnings.png"))
plt.close(fig)
df.to_csv(os.path.join(BASE, "data", "csu_with_roic.csv"), index=False)

# 3. Capital allocation: FCF vs other investing outflow and dividends paid
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.bar([y - 0.2 for y in years], df["free_cash_flow_usd_m"], width=0.4, label="Free cash flow")
ax.bar([y + 0.2 for y in years], df["other_investing_outflow_usd_m"], width=0.4, label="Other investing outflow, mainly acquisitions (proxy)")
ax.plot(years, df["dividends_paid_usd_m"], marker="o", color="red", label="Dividends paid")
ax.set_title("Cash generated and cash used for investing, 2016 to 2025 (USD millions)")
ax.set_ylabel("USD millions")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(CH, "capital_allocation.png"))
plt.close(fig)

# 4. Price history, Oct 2025 to Oct 2026, from the Finnhub daily candles saved with the price search
finnhub_path = "/home/hatch/workspace/agents/03ddb60c-05f4-4b2f-8424-1ba375a603eb/tool-output/browser-search-finance-call_01a178ddbc0274baa81acf486eaf78d2.json"
import datetime
prices = []
try:
    data = json.load(open(finnhub_path))
    candles = data["results"][0]["structured_entity"]["candles"]["daily"]
    for c in candles:
        d = datetime.datetime.fromtimestamp(c["timestamp"], datetime.timezone.utc).date()
        prices.append((d, c["close"]))
    prices.sort()
    with open(os.path.join(BASE, "data", "csu_price_daily_oct2025_oct2026.csv"), "w") as f:
        f.write("date,close_cad\n")
        for d, v in prices:
            f.write(f"{d},{v}\n")
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot([p[0] for p in prices], [p[1] for p in prices])
    ax.set_title("CSU share price, 14 Oct 2025 to 23 Oct 2026 (CAD)")
    ax.set_ylabel("CAD")
    fig.tight_layout()
    fig.savefig(os.path.join(CH, "price_history.png"))
    plt.close(fig)
except Exception as e:
    print("price chart skipped:", e)

# 5. Football field: DCF cases and current price
fig, ax = plt.subplots(figsize=(8, 3.2))
labels = ["Pessimistic", "Base", "Optimistic", "Price, 23 Oct 2026"]
values = [2121, 3567, 5663, 3395]
colors = ["#c0392b", "#1f3864", "#2e7d32", "#888888"]
ax.barh(labels, values, color=colors)
for i, v in enumerate(values):
    ax.text(v + 80, i, f"C${v:,}", va="center")
ax.set_xlim(0, 6500)
ax.set_title("DCF value per share by case, compared with the share price (CAD)")
fig.tight_layout()
fig.savefig(os.path.join(CH, "football_field.png"))
plt.close(fig)
print("charts built")
print(df[["year", "roic_pre_tax_pct"]].round(1).to_string(index=False))
