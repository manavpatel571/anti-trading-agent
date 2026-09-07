class PositionSizer:
    """Determines optimal position size"""
    
    def calculate_atr_size(self, capital: float, risk_pct: float, entry_price: float, atr: float, atr_mult: float = 2.0) -> int:
        risk_amount = capital * risk_pct
        stop_distance = atr * atr_mult
        if stop_distance <= 0: return 0
        return int(risk_amount / stop_distance)
        
    def kelly_criterion(self, win_rate: float, win_loss_ratio: float, fraction: float = 0.5) -> float:
        if win_loss_ratio <= 0: return 0
        kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
        return max(0.0, kelly * fraction)
