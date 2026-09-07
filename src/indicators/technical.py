import pandas as pd
import numpy as np
try:
    import talib
except ImportError:
    talib = None

class TechnicalIndicators:
    """Calculates TA using TA-Lib"""
    
    @staticmethod
    def add_all(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or talib is None: return df
        df['RSI'] = talib.RSI(df['close'], timeperiod=14)
        df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['close'])
        df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
        # Add EMA, VWAP, Bollinger Bands etc
        return df
