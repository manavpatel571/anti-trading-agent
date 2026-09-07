class MacroDataFetcher:
    """Fetches macroeconomic data (FRED, Open Budgets India)"""
    
    def fetch_indicators(self) -> dict:
        """Fetch key macro indicators"""
        return {"vix": 15.0, "us_10y": 4.0, "in_10y": 7.0}
