import pandas as pd
import pandas_ta as ta
import numpy as np

class TechnicalCalculator:
    """Wrapper around pandas_ta to calculate technical indicators"""
    
    @staticmethod
    def calculate_all(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate a suite of technical indicators for the given OHLCV dataframe"""
        if df.empty or len(df) < 50:
            return df
            
        # Ensure column names are standard lowercase for pandas_ta
        # e.g., Open, High, Low, Close, Volume
        col_map = {c: str(c).lower() for c in df.columns}
        df = df.rename(columns=col_map)
        df_ta = df
        
        # Calculate moving averages
        df['EMA_9'] = ta.ema(df_ta['close'], length=9)
        df['EMA_21'] = ta.ema(df_ta['close'], length=21)
        df['EMA_50'] = ta.ema(df_ta['close'], length=50)
        df['EMA_200'] = ta.ema(df_ta['close'], length=200)
        
        # Calculate MACD
        macd = ta.macd(df_ta['close'], fast=12, slow=26, signal=9)
        if macd is not None and not macd.empty:
            df['MACD'] = macd['MACD_12_26_9']
            df['MACD_signal'] = macd['MACDs_12_26_9']
            df['MACD_hist'] = macd['MACDh_12_26_9']
        
        # Calculate RSI
        df['RSI_14'] = ta.rsi(df_ta['close'], length=14)
        
        # Calculate ATR
        df['ATR_14'] = ta.atr(df_ta['high'], df_ta['low'], df_ta['close'], length=14)
        
        # Calculate VWAP
        # Note: VWAP requires an anchor or time column usually, assuming index is datetime
        if isinstance(df.index, pd.DatetimeIndex):
            try:
                df['VWAP'] = ta.vwap(df_ta['high'], df_ta['low'], df_ta['close'], df_ta['volume'])
            except Exception:
                pass
                
        # Calculate Supertrend
        supertrend = ta.supertrend(df_ta['high'], df_ta['low'], df_ta['close'], length=7, multiplier=3.0)
        if supertrend is not None and not supertrend.empty:
            df['Supertrend'] = supertrend['SUPERT_7_3.0']
            df['Supertrend_Direction'] = supertrend['SUPERTd_7_3.0']
            
        return df

    @staticmethod
    def get_signal(df: pd.DataFrame) -> dict:
        """Determine a basic consensus signal based on indicators"""
        if df.empty or 'EMA_21' not in df.columns:
            return {"action": "HOLD", "confidence": 0.0, "reason": "Insufficient data"}
            
        latest = df.iloc[-1]
        
        bullish_points = 0
        bearish_points = 0
        total_checks = 4
        
        reasons = []
        
        # 1. Trend (EMA)
        if latest['close'] > latest['EMA_21']:
            bullish_points += 1
            reasons.append("Price above 21 EMA")
        elif latest['close'] < latest['EMA_21']:
            bearish_points += 1
            reasons.append("Price below 21 EMA")
            
        # 2. Momentum (RSI)
        if 'RSI_14' in latest and not pd.isna(latest['RSI_14']):
            if latest['RSI_14'] < 30:
                bullish_points += 1
                reasons.append("RSI Oversold")
            elif latest['RSI_14'] > 70:
                bearish_points += 1
                reasons.append("RSI Overbought")
                
        # 3. MACD
        if 'MACD' in latest and 'MACD_signal' in latest:
            if latest['MACD'] > latest['MACD_signal']:
                bullish_points += 1
                reasons.append("MACD Bullish Cross")
            else:
                bearish_points += 1
                reasons.append("MACD Bearish Cross")
                
        # 4. Supertrend
        if 'Supertrend_Direction' in latest and not pd.isna(latest['Supertrend_Direction']):
            if latest['Supertrend_Direction'] == 1:
                bullish_points += 1
                reasons.append("Supertrend Bullish")
            else:
                bearish_points += 1
                reasons.append("Supertrend Bearish")
                
        if bullish_points >= 3:
            return {"action": "BUY", "confidence": bullish_points / total_checks, "reason": ", ".join(reasons)}
        elif bearish_points >= 3:
            return {"action": "SELL", "confidence": bearish_points / total_checks, "reason": ", ".join(reasons)}
        else:
            return {"action": "HOLD", "confidence": max(bullish_points, bearish_points) / total_checks, "reason": "Mixed signals"}
