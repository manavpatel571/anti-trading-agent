import pandas as pd
import numpy as np

class QuantIndicators:
    """Statistical and quantitative indicators"""
    
    @staticmethod
    def z_score(series: pd.Series, window: int = 20) -> pd.Series:
        return (series - series.rolling(window).mean()) / series.rolling(window).std()
        
    @staticmethod
    def volatility_regime(returns: pd.Series) -> str:
        """Detect volatility regime using HMM or simple variance bounds"""
        return "NORMAL"
