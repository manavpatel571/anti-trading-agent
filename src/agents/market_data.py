import yfinance as yf
from datetime import datetime
import pandas as pd
from src.core.state import AgentState
from src.core.models import MarketSnapshot
import logging
import json
import os

logger = logging.getLogger(__name__)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cached_data(symbol: str) -> pd.DataFrame:
    """Load cached historical data if yfinance fails."""
    cache_file = os.path.join(CACHE_DIR, f"{symbol}_history.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            # Reconstruct datetime index if it exists in data
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
            elif 'index' in df.columns:
                df['index'] = pd.to_datetime(df['index'])
                df.set_index('index', inplace=True)
            return df
        except Exception as e:
            logger.error(f"Failed to load cache for {symbol}: {e}")
    return pd.DataFrame()

def save_cache_data(symbol: str, df: pd.DataFrame):
    """Save historical data to cache."""
    cache_file = os.path.join(CACHE_DIR, f"{symbol}_history.json")
    try:
        data = df.reset_index().to_dict(orient="records")
        # Convert Timestamps to strings for JSON serialization
        for row in data:
            for k, v in row.items():
                if isinstance(v, pd.Timestamp):
                    row[k] = v.isoformat()
        with open(cache_file, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Failed to save cache for {symbol}: {e}")

def market_data_agent(state: AgentState) -> AgentState:
    """Collects market data and updates state"""
    symbol = state.get("symbol", "RELIANCE.NS")
    logger.info(f"Market Data Agent: Fetching data for {symbol}")
    
    df = pd.DataFrame()
    try:
        # Using yfinance for fetching market data
        ticker = yf.Ticker(symbol)
        
        # Fetch 6 months of daily data
        df = ticker.history(period="6mo", interval="1d")
        
        if not df.empty:
            save_cache_data(symbol, df)
            
    except Exception as e:
        logger.error(f"Error fetching market data from yfinance: {str(e)}")
        
    # Fallback to cache if empty
    if df.empty:
        logger.info(f"Falling back to local cache for {symbol}")
        df = get_cached_data(symbol)
        
    if df.empty:
        logger.warning(f"No data returned for {symbol} (API and Cache failed)")
        return {}
        
    latest = df.iloc[-1]
    
    # Fetch India VIX (simplified without cache for now, fallback to 15.0)
    try:
        vix_ticker = yf.Ticker("^INDIAVIX")
        vix_df = vix_ticker.history(period="1d")
        vix_val = vix_df['Close'].iloc[-1] if not vix_df.empty else 15.0
    except Exception:
        vix_val = 15.0 # Fallback VIX
        
    snapshot = MarketSnapshot(
        timestamp=datetime.now(),
        symbol=symbol,
        ltp=float(latest['Close']),
        volume=int(latest.get('Volume', 0)),
        vix=float(vix_val)
    )
    
    return {
        "market_snapshot": snapshot,
        "macro_outlook": {
            **state.get("macro_outlook", {}),
            "historical_data": df.reset_index().to_dict(orient="records")
        }
    }
