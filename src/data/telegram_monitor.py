class TelegramMonitor:
    """Monitors Telegram channels for social sentiment"""
    
    def get_latest_sentiment(self) -> dict:
        """Get aggregated social sentiment"""
        return {"bullish": 50, "bearish": 50, "neutral": 0}
