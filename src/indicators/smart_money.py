import pandas as pd

class SmartMoneyConcepts:
    """ICT / SMC pattern detection"""
    
    @staticmethod
    def detect_bos(df: pd.DataFrame) -> dict:
        """Detect Break of Structure"""
        return {"bullish_bos": False, "bearish_bos": False}
        
    @staticmethod
    def detect_fvg(df: pd.DataFrame) -> list:
        """Detect Fair Value Gaps"""
        return []
