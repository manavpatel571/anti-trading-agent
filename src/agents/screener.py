import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Hardcoded list of Nifty 50 stocks (Sample of top highly liquid Indian stocks)
NIFTY_50 = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
    "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "BAJFINANCE.NS", "HINDUNILVR.NS",
    "KOTAKBANK.NS", "LT.NS", "AXISBANK.NS", "HCLTECH.NS", "ASIANPAINT.NS",
    "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "BAJAJFINSV.NS",
    "TATASTEEL.NS", "NTPC.NS", "TATAMOTORS.NS", "POWERGRID.NS", "ADANIENT.NS",
    "INDUSINDBK.NS", "ONGC.NS", "NESTLEIND.NS", "JSWSTEEL.NS", "GRASIM.NS",
    "TECHM.NS", "HINDALCO.NS", "ADANIPORTS.NS", "WIPRO.NS", "CIPLA.NS",
    "SBILIFE.NS", "DRREDDY.NS", "EICHERMOT.NS", "BRITANNIA.NS", "M&M.NS",
    "BAJAJ-AUTO.NS", "TATACONSUM.NS", "DIVISLAB.NS", "APOLLOHOSP.NS", "COALINDIA.NS",
    "HEROMOTOCO.NS", "LTIM.NS", "UPL.NS", "BPCL.NS", "HDFCLIFE.NS"
]

def get_top_stocks(limit: int = 5) -> list[str]:
    """
    Scans the Nifty 50 universe for the most active/volatile stocks of the day.
    Returns the top `limit` stock symbols.
    """
    logger.info("Screener Agent: Scanning the market (Nifty 50)...")
    try:
        # Download 2 days of data to calculate percentage change
        data = yf.download(NIFTY_50, period="2d", group_by="ticker", threads=True, progress=False)
        
        scores = []
        for ticker in NIFTY_50:
            try:
                # Access the specific ticker's data
                df = data[ticker] if isinstance(data.columns, pd.MultiIndex) else data
                if df.empty or len(df) < 2:
                    continue
                
                # Get the last two rows (yesterday and today)
                yesterday_close = df['Close'].iloc[-2]
                today_close = df['Close'].iloc[-1]
                today_volume = df['Volume'].iloc[-1]
                
                # Calculate absolute percentage change (volatility/momentum)
                pct_change = abs((today_close - yesterday_close) / yesterday_close) * 100
                
                # Calculate a custom "Action Score" = Volume * PctChange
                # We want stocks that are moving a lot WITH high volume
                score = today_volume * pct_change
                
                scores.append({"symbol": ticker, "score": score})
            except Exception as e:
                logger.debug(f"Screener: Error processing {ticker}: {e}")
                continue
                
        # Sort by score descending
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)
        
        top_stocks = [item["symbol"] for item in scores[:limit]]
        if not top_stocks:
            logger.warning("Screener Agent: Could not determine top stocks. Falling back to default.")
            return NIFTY_50[:limit]
            
        logger.info(f"Screener Agent: Top {limit} stocks identified -> {top_stocks}")
        return top_stocks

    except Exception as e:
        logger.error(f"Screener Agent: Failed to scan market: {e}")
        return NIFTY_50[:limit] # Fallback to top 5
