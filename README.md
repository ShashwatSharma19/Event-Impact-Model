Event Impact Model Dashboard
A quantitative event study framework to analyze how financial markets react to high-impact macroeconomic announcements.

🚀 Introduction
The Event Impact Model is a data-driven tool designed to measure and compare market reactions to scheduled macroeconomic events, such as Federal Reserve (FOMC) meetings and Consumer Price Index (CPI) releases.
It answers key trading-desk questions:

How quickly do different assets incorporate new information?
Which markets are most efficient (price news fastest)?
How do volatility, returns, and drawdowns behave around announcements?
Are reactions consistent across multiple events?

The project combines:

Real-time-capable minute-level price data from Polygon.io
Statistical event study methodology
Cross-asset comparison (equities, bonds, forex, gold)
Interactive Streamlit dashboard for exploration

📅 What Are These Calendar Events?
These are high-impact, scheduled economic announcements that consistently move global markets.
FOMC (Federal Open Market Committee)

Organizer: US Federal Reserve
Frequency: ~8 meetings per year
Key time: Statement released at 2:00 PM ET on the second day of the meeting
What it decides: Federal Funds Rate (interest rate policy), forward guidance, balance sheet plans
Market impact:
Rate cuts → bullish for stocks, gold; bearish for USD
Rate hikes → opposite effect
"Surprises" (bigger/smaller moves than expected) cause largest volatility


CPI (Consumer Price Index)

Organizer: US Bureau of Labor Statistics (BLS)
Frequency: Monthly
Release time: 8:30 AM ET, usually around the 10th–13th of each month (data for previous month)
Key metrics: Headline CPI (YoY %), Core CPI (ex-food/energy)
Market impact:
Higher-than-expected ("hot") CPI → pressure for rate hikes → negative for stocks/bonds
Lower-than-expected ("cool") CPI → room for rate cuts → positive for risk assets


These events are scheduled in advance, allowing us to isolate their impact from random noise — perfect for event studies.
🔧 How the Model Works (Behind the Scenes)
1. Data Pipeline

Source: Polygon.io (professional-grade market data API)
Assets analyzed:
SPY – US equities (S&P 500)
TLT – Long-term US Treasury bonds
C:EURUSD – Major forex pair
GC=F – Gold futures

Granularity: Minute bars (±3–7 days around each event)
Caching: First run fetches and saves data locally (data/cache/) using joblib → subsequent runs are instant and offline-capable

2. Event Study Methodology
For each event:

Align all price series to t=0 (exact announcement second)
Define windows:
Pre-event (e.g., 4 hours before) → baseline volatility
Immediate post (first 30 minutes) → initial reaction
Extended post (24–48 hours) → full absorption and potential reversals


3. Metrics Computed

Immediate Return (30 min): Price change right after announcement
Volatility Change (%): Post-event vol vs pre-event (annualized)
Max Drawdown (%): Largest peak-to-trough decline post-event
Time to Peak Reaction (minutes): How long until the biggest absolute move occurs
Statistical tests (t-test for vol significance)

4. Aggregation & Insights

Average metrics across multiple events (reduces noise)
Compare assets → identify most efficient markets (fastest pricing = lowest time to peak)
Typical findings:
Bonds (TLT) and Forex (EURUSD): Fastest pricing (~5–15 minutes)
Equities (SPY): Slower (~25–40 minutes), higher volatility/drawdowns


5. Visualization & Dashboard

Streamlit web app (app.py):
Interactive filters (assets/events)
Summary table with color gradients
Bar chart: Speed of pricing
Simulated average price path overlay (classic event study style)
Full detailed results table

🛠️ Setup & Running Locally

1) Clone the repo
2) Create virtual environment:Bashpython -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
3) Install dependencies:Bashpip install -r requirements.txt
4) Run the dashboard:Bashstreamlit run app.py