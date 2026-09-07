import yfinance as yf
from src.core.state import AgentState
from src.core.models import Signal, ActionType
import logging

logger = logging.getLogger(__name__)

def news_sentiment_agent(state: AgentState) -> AgentState:
    """Analyzes news sentiment and calculates Fear & Greed index"""
    logger.info("News Sentiment Agent: Analyzing sentiment")
    
    symbol = state.get("symbol", "RELIANCE.NS")
    
    # 1. Fetch News
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        news_count = len(news) if news else 0
        logger.info(f"Fetched {news_count} news items for {symbol}")
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        news = []
        
    # 2. Calculate synthetic Fear & Greed based on VIX
    # If VIX is high (> 20), Fear. If low (< 13), Greed.
    snapshot = state.get("market_snapshot")
    vix = snapshot.vix if snapshot else 15.0
    
    fear_greed_score = 50 # Neutral
    if vix > 25:
        fear_greed_score = 10 # Extreme Fear
    elif vix > 20:
        fear_greed_score = 30 # Fear
    elif vix < 12:
        fear_greed_score = 90 # Extreme Greed
    elif vix < 15:
        fear_greed_score = 70 # Greed
        
    action = ActionType.HOLD
    confidence = 0.0
    reason = "Neutral Sentiment"
    
    # Contrarian trading logic based on Fear & Greed
    if fear_greed_score <= 20:
        # Extreme fear can be a buying opportunity
        action = ActionType.BUY
        confidence = 60.0
        reason = f"Extreme Fear (VIX: {vix:.2f}), potential oversold bounce"
    elif fear_greed_score >= 80:
        # Extreme greed can be a selling opportunity
        action = ActionType.SELL
        confidence = 60.0
        reason = f"Extreme Greed (VIX: {vix:.2f}), potential overbought correction"
        
    signal = Signal(
        agent_name="NewsSentiment",
        action=action,
        confidence=confidence,
        reasoning=reason,
        metadata={"fear_greed_score": fear_greed_score, "news_count": len(news)}
    )
    
    logger.info(f"Sentiment signal generated: {signal.action.value} with {signal.confidence}% confidence")
    
    return {
        "signals": [signal],
        "news_sentiment": {
            "fear_greed_score": fear_greed_score,
            "vix": vix,
            "latest_headlines": [n.get("title", "") for n in news[:3]] if isinstance(news, list) else []
        }
    }
