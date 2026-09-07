# Anti-Trading Agent

A production-grade, SEBI-compliant, multi-agent AI trading system built on LangGraph. This system is designed to automate Indian Equities trading (NSE) using a team of specialized AI agents.

## 🏗️ Architecture: How It Works

The system uses a **Directed Acyclic Graph (DAG)** via `LangGraph`.

1. **Market Data Agent (`market_data.py`)**: Fetches historical OHLCV data and real-time prices for Indian stocks using `yfinance`. It also monitors `^INDIAVIX` for market volatility.
2. **Technical Analysis Agent (`technical.py`)**: Calculates indicators (RSI, MACD, Moving Averages) to generate quantitative `BUY`/`SELL` signals.
3. **News Sentiment Agent (`news_sentiment.py`)**: Analyzes breaking news to determine market sentiment.
4. **Voting Agent (`voting.py`)**: Forces consensus between technicals and sentiment.
5. **CIO Agent (Chief Investment Officer) (`cio.py`)**: Uses Google Gemini to act as a human oversight safety net and provide final approval.
6. **Risk Manager Agent (`risk_manager.py`)**: Calculates position sizing based on account balance and current volatility (VIX). Acts as a circuit breaker.
7. **Execution Agent (`execution.py`)**: Sends the approved, risk-adjusted trade to the stock broker (DhanHQ).

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10+ installed. Install the required dependencies:
```bash
python -m pip install -r requirements.txt
```

### 2. Configuration
1. Rename the `.env.example` file to `.env`.
2. Open the `.env` file and add your API keys:
   - **GEMINI_API_KEY**: Required for the CIO agent.
   - **DHAN_CLIENT_ID** / **DHAN_ACCESS_TOKEN**: Required for execution via DhanHQ.

### 3. Dry Run (Paper Trading) Mode
By default, the system is configured to **DRY RUN** mode. It will analyze data and propose trades without actually risking capital. Set `DRY_RUN=False` in `dhan.py` (or via environment variables when fully implemented) to go live.

### 4. Running the Bot
To start the continuous trading loop across your targeted stocks (`RELIANCE.NS`, `HDFCBANK.NS`, `TCS.NS`, `INFY.NS`, `SBIN.NS`), run:
```bash
python main.py
```

## 📁 Repository Structure
- `main.py`: The entry point and infinite loop runner.
- `src/core/graph.py`: Defines the LangGraph pipeline that wires the agents together.
- `src/core/state.py`: Defines the strict data structure passed between agents.
- `src/agents/`: Contains the logic for all 7 specialized agents.
- `src/brokers/dhan.py`: The integration for DhanHQ (Indian Equities).
