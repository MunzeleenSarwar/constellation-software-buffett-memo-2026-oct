# Constellation Software Inc. (TSX: CSU): Buffett-style investment memo

Date: October 2026.
Price used: C$3,395, close on 23 Oct 2026.
Company figures: USD millions, unless stated.
Share price: CAD.
Exchange rate used: 1.40 CAD per USD on 23 Oct 2026.

## Rating

- Rating: HOLD at C$3,395.
- Base-case DCF value: C$3,567.
- Upside to base case: 5.1%.
- Buy below: C$3,000, if cash flow and return on capital stay near recent levels.
- Optimistic DCF value: C$5,663.
- Pessimistic DCF value: C$2,121.

## What this project covers

- Business model: vertical market software, six operating groups, decentralised management.
- Competitive advantage: switching costs, narrow market focus, acquisition process.
- Cash generation: revenue, operating income, net income, operating cash flow, free cash flow.
- Owner earnings: net income attributable plus depreciation and amortisation, less capital expenditure.
- Return on invested capital: pre-tax operating income divided by average invested capital.
- Capital allocation: acquisitions, dividends, and reinvestment of free cash flow.
- Risks: tests that would prove the thesis wrong.
- Valuation: discounted cash flow with base, optimistic, and pessimistic cases, plus sensitivities.

## Key findings

- Revenue rose from US$2,125 million in 2016 to US$11,623 million in 2025.
- Free cash flow rose from US$472 million in 2016 to US$2,664 million in 2025.
- Recurring revenue was 74.9% of total revenue in 2025.
- Capital expenditure was US$68 million in 2025, or 0.6% of revenue.
- Pre-tax return on invested capital was 31.5% in 2025 and 29.0% in 2024.
- Net income attributable fell to US$512 million in 2025, from US$731 million in 2024, even though operating cash flow rose. Reported profit alone does not show cash generation.
- Terminal value makes up about 77% of base-case enterprise value. Small changes in the discount rate or terminal growth rate change the result by a large amount.

## Files

- `Constellation_Software_Buffett_Memo_Report.pdf`: 6-page report, plain professional language.
- `Constellation_Software_Financial_Model.xlsx`: historical data, owner earnings, return on invested capital, discounted cash flow with live formulas, and sensitivities.
- `analysis.ipynb`: executed notebook with tables and charts.
- `charts/`: revenue vs net income, return on invested capital and owner earnings, capital allocation, price history, DCF football field.
- `data/csu_annual_2016_2025.csv`: annual data used in the model and notebook.
- `data/csu_price_daily_oct2025_oct2026.csv`: daily closes from Finnhub, 14 Oct 2025 to 23 Oct 2026.
- `scripts/`: scripts used to build the charts, model, notebook, and report.

## Method and limits

- Discounted cash flow uses free cash flow, defined as operating cash flow less capital expenditure.
- Starting free cash flow is US$2,664 million in 2025.
- Base case: 8.0% free cash flow growth for five years, 9.0% discount rate, 3.0% terminal growth.
- Optimistic case: 12.0% growth, 8.0% discount rate, 3.5% terminal growth.
- Pessimistic case: 4.0% growth, 10.5% discount rate, 2.0% terminal growth.
- Net debt at 31 Dec 2025 is US$2,646 million: total debt US$5,787 million less cash and investments US$3,141 million.
- Shares outstanding are 21.19 million.
- Owner earnings proxy is an upper bound. It adds back depreciation and amortisation, which includes amortisation of acquired intangibles.
- Other investing outflow is used as a proxy for acquisition spending. It is not a verified acquisition-only line.
- Return on invested capital is pre-tax, to avoid tax distortions from non-cash revaluation items.
- Return on invested capital is shown from 2017, because 2015 invested capital was not verified on the same basis.
- Price history covers one year only, because that was the daily series verified for this memo.
- The 20% acquisition hurdle rate is reported in company descriptions. It is not verified here as a result.
- Secondary data sources differ in rounding and classification. Figures are shown to the nearest million.
- This project uses secondary sources, not a full audit of the annual reports. A check against the audited annual reports would improve the work.

## Sources

- Constellation Software Q4 2024 shareholder report: revenue split, net income attributable.
- StockAnalysis financials and revenue history: revenue, operating income, net income, operating cash flow, capital expenditure, debt, cash, shares, dividend per share.
- MacroTrends: net income and operating cash flow history.
- AlphaSpread: income statement, cash flow statement, balance sheet.
- Finnhub: close of C$3,395 on 23 Oct 2026, daily candles to 23 Oct 2026.
- Exchange rate: 1.40 CAD per USD on 23 Oct 2026.

## Status

- Local files only.
- Not published to GitHub, LinkedIn, or any public site.
- No LinkedIn post draft is included.
- Projects B and C from the Buffett brainstorm (owner earnings comparison, capital allocation scorecard) are for later work. They are not part of this project.

## Disclaimer

This is analysis for learning and portfolio use. It is not investment advice.
