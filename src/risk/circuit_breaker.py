class CircuitBreaker:
    """Monitors PnL and halts trading if loss limits are breached"""
    
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        
    def check_daily_limit(self, current_daily_pnl: float, max_loss_pct: float = 0.02) -> bool:
        """Returns True if trading should be halted"""
        max_loss_amount = self.initial_capital * max_loss_pct
        return current_daily_pnl <= -max_loss_amount
