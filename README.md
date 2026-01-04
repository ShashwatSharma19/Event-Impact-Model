# Event Impact Model Dashboard

**Interactive dashboard analyzing how markets react to FOMC and CPI announcements.**


[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)

![Dashboard Hero Screenshot](images/hero-screenshot.png)

## 🚀 Introduction

The **Event Impact Model** is a data-driven tool designed to measure and compare **market reactions** to scheduled macroeconomic events, such as

- Federal Reserve (**FOMC**) meetings  
- Consumer Price Index (**CPI**) releases

It answers key trading-desk questions:

- How quickly do different assets incorporate new information?  
- Which markets are most efficient (price news fastest)?  
- How do volatility, returns, and drawdowns behave around announcements?  
- Are reactions consistent across multiple events?

The project combines:

- High-quality **minute-level price data** from Polygon.io  
- Statistical **event study methodology**  
- Cross-asset comparison (equities, bonds, forex, gold)  
- Interactive **Streamlit dashboard** for exploration

## 📅 What Are These Calendar Events?

These are **high-impact, scheduled economic announcements** that consistently move global markets.

### FOMC (Federal Open Market Committee)

- **Organizer**: US Federal Reserve  
- **Frequency**: ~8 meetings per year  
- **Key time**: Statement released at **14:00 ET** on the second day of the meeting  
- **What it decides**: Federal Funds Rate, forward guidance, balance sheet plans  
- **Market impact**:
  - Rate cuts → bullish for stocks & gold, bearish for USD  
  - Rate hikes → opposite effect  
  - “Surprises” (bigger/smaller moves than expected) cause largest volatility

### CPI (Consumer Price Index)

- **Organizer**: US Bureau of Labor Statistics (BLS)  
- **Frequency**: Monthly  
- **Release time**: **08:30 ET**, usually around the 10th–13th of each month (data for previous month)  
- **Key metrics**: Headline CPI (YoY %), Core CPI (ex-food & energy)  
- **Market impact**:
  - Higher-than-expected (“hot”) CPI → pressure for rate hikes → negative for stocks/bonds  
  - Lower-than-expected (“cool”) CPI → room for rate cuts → positive for risk assets

These events are scheduled in advance, making them ideal for **event studies** (isolating impact from random noise).

## 🔧 How the Model Works

1. **Data Pipeline**  
   - Source: Polygon.io (professional-grade market data API)  
   - Assets:  
     - SPY – US equities (S&P 500)  
     - TLT – Long-term US Treasury bonds  
     - C:EURUSD – Major forex pair  
     - GC=F – Gold futures  
   - Granularity: Minute bars (±3–7 days around each event)  
   - Caching: First run fetches and saves data locally (`data/cache/`) using `joblib` → subsequent runs are instant and offline-capable

2. **Event Study Methodology**  
   - Align all price series to **t=0** (exact announcement second)  
   - Define windows: pre-event, immediate post (first 30 min), extended post (24–48 h)

3. **Metrics Calculated**  
   - Immediate return (30 min)  
   - Volatility change (pre vs post) + statistical significance (t-test)  
   - Max drawdown  
   - Time to peak reaction (minutes until largest absolute move)

4. **Aggregation**  
   - Average metrics across multiple events to reveal consistent patterns



## 📊 Features

- Multi-asset analysis (equities, bonds, forex, gold)  
- Coverage of FOMC & CPI events (2024–2025 rate cycle)  
- Key metrics: returns, vol spikes, drawdowns, time to peak  
- Interactive filters (assets / events)  
- Simulated average price path overlay (classic event study style)  
- Local caching for fast re-runs

## 🎥 Screenshots

### Dashboard Overview
![Main Dashboard](images/dashboard-overview.png)

### Speed of Pricing Chart
![Speed Chart](images/speed-chart.png)

### Average Price Path
![Average Price Path](images/average-path.png)

## 🛠️ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/event-impact-model.git
cd event-impact-model

# 2. Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Get Polygon API key & put it in .env
# See .env.example

# 5. Run the dashboard
streamlit run app.py
