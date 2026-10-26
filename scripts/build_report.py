"""Build Constellation_Software_Buffett_Memo_Report.pdf. Plain, direct, professional language.
No em dashes. No first person. Author name appears only at the top of page 1, not in footers."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

BASE = os.path.expanduser("~/workspace/your_files/constellation-software-equity-research")
BLACK = HexColor("#000000"); GREY = HexColor("#000000"); PALE = HexColor("#FFFFFF"); RULE = HexColor("#000000")

def st(name, **kw):
    d = dict(fontName="Times-Roman", fontSize=10.5, leading=14.5, textColor=HexColor("#000000"), alignment=TA_LEFT, spaceAfter=7)
    d.update(kw)
    return ParagraphStyle(name, **d)

EYEBROW = st("EYEBROW", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=BLACK, spaceAfter=4)
TITLE = st("TITLE", fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=BLACK, spaceAfter=4)
SUBTITLE = st("SUBTITLE", fontName="Helvetica", fontSize=11, leading=15, textColor=GREY, spaceAfter=8)
H2 = st("H2", fontName="Helvetica-Bold", fontSize=12.5, leading=15, textColor=BLACK, spaceBefore=13, spaceAfter=5)
BODY = st("BODY")
BULLET = st("BULLET", leftIndent=14, firstLineIndent=0, bulletIndent=6, spaceAfter=4)
CAPTION = st("CAPTION", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=GREY, spaceAfter=10)
SMALL = st("SMALL", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=GREY, spaceAfter=6)
CELL = st("CELL", fontName="Helvetica", fontSize=8.5, leading=11, spaceAfter=0)
CELLB = st("CELLB", fontName="Helvetica-Bold", fontSize=8.5, leading=11, spaceAfter=0)
CELLW = st("CELLW", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=white, spaceAfter=0)
STAT_L = st("STAT_L", fontName="Helvetica", fontSize=9.5, leading=12, textColor=GREY, spaceAfter=0)
STAT_V = st("STAT_V", fontName="Helvetica-Bold", fontSize=10.5, leading=12, spaceAfter=0)
BOX = st("BOX", fontName="Times-Italic", fontSize=10.5, leading=14, spaceAfter=0)

def P(t, s=BODY): return Paragraph(t, s)
def tbl(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
             ("BACKGROUND", (0, 0), (-1, 0), BLACK)]
    for r in range(1, len(data)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), PALE))
    t.setStyle(TableStyle(style))
    return t
def fig(name, caption):
    return [Image(os.path.join(BASE, "charts", name), width=15.2*cm, height=7.2*cm), P(caption, CAPTION)]
def box(text):
    t = Table([[P(text, BOX)]], colWidths=[16.5*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                           ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return t
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.4*cm, "Constellation Software Equity Research  |  October 2026  |  Not investment advice")
    canvas.drawRightString(A4[0]-2*cm, 1.4*cm, f"Page {doc.page}")
    canvas.restoreState()

story = []
story.append(P("Munzeleen Sarwar", st("NAME", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=GREY, spaceAfter=6)))
story.append(P("BUFFETT-STYLE INVESTMENT MEMO  |  TSX: CSU", EYEBROW))
story.append(P("Constellation Software Inc.", TITLE))
story.append(P("A buyer and operator of small, niche software businesses. Strong cash generation, a high price, and a value that depends heavily on future acquisitions.", SUBTITLE))
stats = Table([
    [P("Rating", STAT_L), P("HOLD", STAT_V), P("Price (23 Oct 2026)", STAT_L), P("C$3,395", STAT_V)],
    [P("Base-case DCF value", STAT_L), P("C$3,567", STAT_V), P("Upside to base case", STAT_L), P("5.1%", STAT_V)],
    [P("Buy below", STAT_L), P("C$3,000", STAT_V), P("Pessimistic DCF value", STAT_L), P("C$2,121", STAT_V)],
    [P("2025 revenue", STAT_L), P("US$11,623m", STAT_V), P("2025 free cash flow", STAT_L), P("US$2,664m", STAT_V)],
], colWidths=[3.6*cm, 3.4*cm, 4.2*cm, 5.3*cm])
stats.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                           ("BACKGROUND", (0, 1), (-1, 1), PALE), ("BACKGROUND", (0, 3), (-1, 3), PALE)]))
story.append(stats)
story.append(Spacer(1, 8))
story.append(P("October 2026. Company figures in USD millions, unless stated. Share price in CAD. Price: C$3,395, close on 23 Oct 2026. Exchange rate: 1.40 CAD per USD on 23 Oct 2026. This memo covers the business model, competitive advantage, cash generation and capital allocation, risks, and valuation.", SMALL))
story.append(box("Bottom line: Constellation Software generates a large amount of cash from a low capital base. The price already reflects a strong future. HOLD at C$3,395. Add below C$3,000."))
story.append(Spacer(1, 4))

story.append(P("About this project", H2))
story.append(P("This project is a Buffett-style investment memo on Constellation Software Inc. (TSX: CSU). It was inspired by the shareholder letters of Warren Buffett and Charlie Munger. The purpose was to apply their ideas to a real Canadian company, and to practise judging a business on its own merits rather than following a share price. The memo follows their questions in order: what the business is worth compared with its price, what protects its returns from competitors, how much cash is available to owners after the investment needed to maintain the business, how management allocates cash between acquisitions, dividends, and retained cash, what could cause a permanent loss, and what evidence would change the rating. That is why the memo uses an owner earnings proxy, return on invested capital, a discounted cash flow valuation with optimistic, base, and pessimistic cases, and a set of thesis invalidation tests in Section 6. The goal is investment judgment that can be explained in plain language, not imitation of any portfolio."))
story.append(P("Investment summary", H2))
story.append(P("Constellation Software was founded in 1995 and is headquartered in Toronto. The company buys, manages, and builds vertical market software businesses. Vertical market software is software built for one industry, such as public sector, health care, or construction, rather than for all industries. Revenue rose from US$2,125 million in 2016 to US$11,623 million in 2025, a compound annual growth rate of 20.8%. Free cash flow rose from US$472 million to US$2,664 million over the same period, a compound annual growth rate of 21.2%. Much of that growth came from acquisitions, not only from sales growth inside existing businesses. That distinction matters for valuation."))
story.append(P("The rating is HOLD for a clear reason. The base-case discounted cash flow value is C$3,567, only 5.1% above the price of C$3,395. A 5.1% gap does not leave room for error if acquisition returns fall or if growth slows. The pessimistic case is C$2,121, which is 37.5% below the price. The optimistic case is C$5,663. The wide range shows that the value depends on assumptions about the next ten years, not only on past results."))

story.append(P("1. Business model", H2))
story.append(P("Constellation Software operates through six operating groups: Volaris, Harris, Jonas, Vela, Perseus, and Topicus. Each group has its own management team. Day-to-day decisions stay with the acquired businesses. Capital allocation decisions sit with group leaders and head office. The company buys businesses that are often small, with revenue from a few hundred thousand dollars to about US$1 billion, according to company descriptions. Acquired businesses usually keep their brand and management team. The head office stays small and focuses on capital allocation, performance measurement, and sharing operating practices across groups."))
story.append(P("Revenue comes mainly from recurring sources. In 2024, maintenance and other recurring revenue was US$7,396 million, or 73.5% of total revenue. In 2025, it was US$8,700 million, or 74.9% of total revenue. Licenses, professional services, and hardware and other revenue made up the rest. Recurring revenue is important because it is more stable than one-time license sales. It also gives the company cash each year to fund new acquisitions."))

story.append(P("2. Competitive advantage", H2))
story.append(P("The main advantage is switching cost. The software is mission-critical for customers. It runs billing, records, scheduling, compliance, or daily operations. Replacing it would disrupt work, require retraining, and risk data loss. Customers therefore tend to stay. That supports recurring revenue and pricing power."))
story.append(P("The second advantage is focus. Each business serves a narrow market. A general software company would need to learn that market, build trust, and compete for a small customer base. That limits direct competition for many of the acquired businesses."))
story.append(P("The third advantage is process. Constellation Software has bought many businesses over three decades. Group leaders track returns on capital and compare businesses against each other. That experience helps with pricing, cost control, and judging new acquisitions. It does not remove risk. Acquisition prices can rise, and good targets can become scarce. Section 6 lists the tests that would show the advantage is weakening."))

story.append(P("3. Ten years of results", H2))
story.append(P("The table below uses reported figures from secondary sources, rounded to the nearest million. Sources differ in rounding and in classification, so small differences between sources are normal. The direction of the results is consistent across sources."))
story.append(tbl([
    [P("Year", CELLW), P("Revenue", CELLW), P("Operating income", CELLW), P("Net income*", CELLW), P("Operating cash flow", CELLW), P("Free cash flow", CELLW)],
    [P("2016", CELL), P("2,125", CELL), P("339", CELL), P("207", CELL), P("491", CELL), P("472", CELL)],
    [P("2017", CELL), P("2,479", CELL), P("391", CELL), P("222", CELL), P("528", CELL), P("508", CELL)],
    [P("2018", CELL), P("3,060", CELL), P("478", CELL), P("379", CELL), P("662", CELL), P("637", CELL)],
    [P("2019", CELL), P("3,489", CELL), P("511", CELL), P("333", CELL), P("767", CELL), P("733", CELL)],
    [P("2020", CELL), P("3,969", CELL), P("682", CELL), P("436", CELL), P("1,186", CELL), P("1,161", CELL)],
    [P("2021", CELL), P("5,106", CELL), P("870", CELL), P("310", CELL), P("1,300", CELL), P("1,271", CELL)],
    [P("2022", CELL), P("6,622", CELL), P("920", CELL), P("512", CELL), P("1,297", CELL), P("1,256", CELL)],
    [P("2023", CELL), P("8,407", CELL), P("1,182", CELL), P("565", CELL), P("1,779", CELL), P("1,737", CELL)],
    [P("2024", CELL), P("10,066", CELL), P("1,471", CELL), P("731", CELL), P("2,196", CELL), P("2,129", CELL)],
    [P("2025", CELL), P("11,623", CELL), P("1,928", CELL), P("512", CELL), P("2,732", CELL), P("2,664", CELL)],
], [1.6*cm, 2.4*cm, 3.0*cm, 2.6*cm, 3.6*cm, 2.8*cm]))
story.append(P("* Net income attributable to common shareholders. USD millions. Free cash flow = operating cash flow less capital expenditure.", SMALL))
story += fig("revenue_vs_income.png", "Figure 1: Revenue and net income attributable, 2016 to 2025. Net income is volatile. Revenue and cash flow are steadier. Sources: StockAnalysis, MacroTrends, AlphaSpread, company reports.")
story.append(P("Net income fell in 2025 even though revenue and operating income rose. Net income attributable was US$512 million in 2025, down from US$731 million in 2024. That fall reflects non-cash and noncontrolling interest items, not a fall in operating cash flow. Operating cash flow rose to US$2,732 million in 2025. This is the core Buffett lesson in this memo: reported profit can move for reasons that do not change cash generation. Cash flow, owner earnings, and return on capital give a clearer view."))

story.append(P("4. Owner earnings and return on invested capital", H2))
story.append(P("Owner earnings proxy = net income attributable + depreciation and amortisation - capital expenditure. The proxy is an upper bound. Depreciation and amortisation includes amortisation of acquired intangibles. That amortisation reflects part of the price paid for acquisitions, so adding it all back overstates cash that is free for new uses. Free cash flow is shown beside the proxy for that reason."))
story.append(P("Pre-tax return on invested capital = operating income / average invested capital. Invested capital = total equity attributable + minority interest + interest-bearing debt - cash and short-term investments. The return was very high when the capital base was small. It fell as the capital base grew. It stayed high in absolute terms. In 2025, it was 31.5%. In 2024, it was 29.0%. The fall from above 80% in 2017 and 2018 to about 30% in recent years is expected. A larger company needs more capital to grow by the same percentage. The question for the future is whether new acquisitions can earn returns near recent levels, not whether the company can repeat the returns of its early years."))
story += fig("roic_and_owner_earnings.png", "Figure 2: Owner earnings proxy, free cash flow, and pre-tax return on invested capital. Return on capital is shown from 2017, because 2015 invested capital was not verified on the same basis. Sources: see data notes in the Excel model.")

story.append(P("5. Cash generation and capital allocation", H2))
story.append(P("Capital expenditure is very low for a company of this size. It was US$68 million in 2025, or 0.6% of revenue. That is normal for a software business. The main use of cash is acquisitions. Other investing outflow, used here as a proxy for acquisition spending, was US$1,800 million in 2025 and US$1,500 million in 2024. Total free cash flow from 2016 to 2025 was US$12,568 million. Total other investing outflow over the same period was US$9,686 million. Dividends paid were US$1,281 million over the same period, including US$509 million in 2019. The company therefore reinvested most of its cash into acquisitions and paid a small dividend. No material share buyback is shown in the dividend and investing data used here."))
story.append(P("The hurdle for acquisitions is central. Company descriptions report a target return of about 20% on new acquisitions. That target is not verified in the annual figures used here, and the report does not present it as a verified result. What can be verified is the outcome: pre-tax return on invested capital near 30% in recent years, and free cash flow growth of 21.2% a year from 2016 to 2025. If acquisition prices rise and returns fall below the cost of capital, growth would add less value. That is the main capital allocation risk."))
story += fig("capital_allocation.png", "Figure 3: Free cash flow, other investing outflow as a proxy for acquisition spending, and dividends paid. Other investing outflow is a proxy, not a verified acquisition-only line. Sources: AlphaSpread cash flow data, StockAnalysis.")

story.append(P("6. Risks and thesis invalidation", H2))
story.append(P("Each point below is one test. If a test fails, the thesis must be reviewed."))
for b in [
    "Acquisition returns fall: pre-tax return on invested capital falls below 20% for two years in a row, with no clear one-time cause.",
    "Acquisition prices rise: other investing outflow rises faster than free cash flow for two years, while revenue growth from acquisitions does not rise at the same rate.",
    "Organic weakness: recurring revenue share falls below 70%, or customer loss rises in a way that shows in slower maintenance revenue growth.",
    "Debt rises faster than cash: net debt rises above US$4,000 million without a matching rise in free cash flow.",
    "Key person and decentralisation risk: group leaders leave, or head office centralises decisions in a way that slows acquisition decisions.",
    "Valuation risk: the share price rises well above the base-case value, so future growth is already paid for in advance.",
    "Accounting risk: non-cash revaluation items continue to make net income hard to read, and cash flow conversion weakens.",
]:
    story.append(P("•  " + b, BULLET))
story.append(P("What would change the rating: a fall below C$3,000 would move the rating to BUY, if cash flow and return on capital stayed near recent levels. A rise in return on capital back above 35% for two years, with disciplined acquisition spending, would also support a higher rating. A failure of the tests above would move the rating to SELL, even if the share price had not yet fallen."))

story.append(P("7. Valuation", H2))
story.append(P("Method: discounted cash flow on free cash flow. Starting free cash flow is US$2,664 million in 2025. Forecast period is five years. Terminal value uses a constant growth rate after year five. Net debt at 31 Dec 2025 is US$2,646 million, from total debt of US$5,787 million less cash and investments of US$3,141 million. Shares outstanding are 21.19 million. The value in USD is converted at 1.40 CAD per USD."))
story.append(tbl([
    [P("Case", CELLW), P("FCF growth, 5 years", CELLW), P("Discount rate", CELLW), P("Terminal growth", CELLW), P("Value per share (CAD)", CELLW)],
    [P("Base", CELL), P("8.0%", CELL), P("9.0%", CELL), P("3.0%", CELL), P("3,567", CELLB)],
    [P("Optimistic", CELL), P("12.0%", CELL), P("8.0%", CELL), P("3.5%", CELL), P("5,663", CELLB)],
    [P("Pessimistic", CELL), P("4.0%", CELL), P("10.5%", CELL), P("2.0%", CELL), P("2,121", CELLB)],
    [P("Price, 23 Oct 2026", CELLB), P("", CELL), P("", CELL), P("", CELL), P("3,395", CELLB)],
], [3.2*cm, 3.4*cm, 2.8*cm, 2.8*cm, 4.3*cm]))
story.append(Spacer(1, 4))
story += fig("football_field.png", "Figure 4: DCF value per share by case, compared with the price. The range is wide. The terminal value makes up about 77% of the base-case enterprise value, so small changes in the discount rate or terminal growth rate change the result by a large amount.")
story.append(P("Sensitivity, at terminal growth of 3.0%, in CAD per share:"))
story.append(tbl([
    [P("FCF growth / Discount rate", CELLW), P("8.0%", CELLW), P("9.0%", CELLW), P("10.0%", CELLW), P("11.0%", CELLW)],
    [P("4.0%", CELL), P("3,614", CELL), P("2,980", CELL), P("2,528", CELL), P("2,188", CELL)],
    [P("6.0%", CELL), P("3,960", CELL), P("3,263", CELL), P("2,766", CELL), P("2,393", CELL)],
    [P("8.0%", CELL), P("4,331", CELL), P("3,567", CELL), P("3,021", CELL), P("2,612", CELL)],
    [P("10.0%", CELL), P("4,729", CELL), P("3,892", CELL), P("3,295", CELL), P("2,848", CELL)],
    [P("12.0%", CELL), P("5,157", CELL), P("4,241", CELL), P("3,588", CELL), P("3,099", CELL)],
], [4.5*cm, 2.7*cm, 2.7*cm, 2.7*cm, 2.7*cm]))
story.append(P("Why terminal value dominates: the DCF forecasts cash flow in detail for 2026 to 2030 only. The present value of those five years is about US$12,958 million, out of total enterprise value of about US$56,630 million. The rest, about 77%, is terminal value, the value assigned to all cash flow after 2030. Terminal value is year 5 cash flow, grown by 3%, divided by (9% discount rate minus 3% terminal growth). That denominator is only 6 percentage points, so a small change has a large effect. At 8% growth, a move in the discount rate from 9% to 10% lowers the value from C$3,567 to C$3,021. A move in terminal growth from 3% to 2% lowers the value to C$3,130. The HOLD rating therefore rests more on an assumption about the distant future than on the next five years. The value is a range, not a single precise price."))
story.append(P("Cross-check: market value at C$3,395 is C$71,940 million, or US$51,386 million at 1.40 CAD per USD. Divided by 2025 free cash flow of US$2,664 million, the multiple is 19.3 times. That multiple is not low. It requires continued free cash flow growth to be justified."))
story += fig("price_history.png", "Figure 5: CSU share price, 14 Oct 2025 to 23 Oct 2026, in CAD. The series is one year only, because that was the daily series verified for this memo. Source: Finnhub daily candles, as saved with the price search.")

story.append(P("8. Recommendation and limits", H2))
story.append(P("Recommendation: HOLD Constellation Software at C$3,395. Base-case value is C$3,567. Upside is 5.1%. That upside is too small to call the shares a buy, given the wide valuation range and the dependence on future acquisitions. Buy below C$3,000, if cash flow and return on capital stay near recent levels. Review the rating if any test in Section 6 fails."))
story.append(P("Limits: this memo uses secondary data sources, not a full audit of the annual reports. Operating income, net income, and equity figures differ slightly between sources because of classification and rounding. A full check would mean reading the annual reports and reconciling revenue, cash flow, debt, acquisitions, and share count line by line. That step was not done in this build, so the report states the limit instead of claiming full verification. Other investing outflow is a proxy for acquisition spending, not a verified acquisition-only line. Summary data does not separate acquisition cash cleanly, because the company buys many small private companies each year. The 20% acquisition hurdle rate appears in company profiles and descriptions of its discipline. It is not an audited result, and actual returns differ by deal, so it cannot be stated as a verified fact. The price history chart covers one year only, because the verified daily series retrieved for this memo covered Oct 2025 to Oct 2026 only. A longer price series, a full acquisition-by-acquisition review, and a check against the audited annual reports would improve this memo. Those steps are left as follow-up work. This memo is analysis for learning and portfolio use. It is not investment advice."))
story.append(P("Sources: Constellation Software Q4 2024 shareholder report (revenue split and net income attributable); StockAnalysis financials and revenue history (revenue, operating income, net income, operating cash flow, capital expenditure, debt, cash, shares, dividend per share); MacroTrends net income and operating cash flow history; AlphaSpread income statement, cash flow statement, and balance sheet (operating income, depreciation and amortisation, dividends paid, investing outflow, equity, debt, cash); Finnhub price data (close of C$3,395 on 23 Oct 2026, daily candles to 23 Oct 2026); exchange rate 1.40 CAD per USD on 23 Oct 2026. Model: Constellation_Software_Financial_Model.xlsx. Notebook: analysis.ipynb.", SMALL))

doc = SimpleDocTemplate(os.path.join(BASE, "Constellation_Software_Buffett_Memo_Report.pdf"), pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm,
                        title="Constellation Software Buffett Memo Report", author="Munzeleen Sarwar")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("report built")
