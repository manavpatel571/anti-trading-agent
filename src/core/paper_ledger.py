import os
import json
import logging

logger = logging.getLogger(__name__)

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ledger.json")

class PaperLedger:
    """
    A simple JSON-based ledger for Paper Trading (tracking fake money and dummy trades).
    """
    def __init__(self, initial_balance: float = 50000.0):
        self.ledger_file = LEDGER_FILE
        self.initial_balance = initial_balance
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        if not os.path.exists(self.ledger_file):
            self._save_state({
                "available_cash": self.initial_balance,
                "positions": {} # e.g. {"RELIANCE.NS": {"quantity": 10, "avg_price": 2500.0}}
            })

    def _load_state(self) -> dict:
        try:
            with open(self.ledger_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"PaperLedger: Failed to load ledger: {e}")
            return {"available_cash": self.initial_balance, "positions": {}}

    def _save_state(self, state: dict):
        try:
            with open(self.ledger_file, "w") as f:
                json.dump(state, f, indent=4)
        except Exception as e:
            logger.error(f"PaperLedger: Failed to save ledger: {e}")

    def get_cash(self) -> float:
        return self._load_state().get("available_cash", 0.0)

    def get_positions(self) -> dict:
        return self._load_state().get("positions", {})

    def record_buy(self, symbol: str, quantity: float, price: float) -> bool:
        state = self._load_state()
        cost = quantity * price

        if state["available_cash"] < cost:
            logger.error(f"PaperLedger: Insufficient funds to buy {quantity} {symbol} at {price}. Available: {state['available_cash']}, Required: {cost}")
            return False

        # Deduct cash
        state["available_cash"] -= cost

        # Update position
        if symbol in state["positions"]:
            pos = state["positions"][symbol]
            new_qty = pos["quantity"] + quantity
            # Calculate new average price
            pos["avg_price"] = ((pos["quantity"] * pos["avg_price"]) + cost) / new_qty
            pos["quantity"] = new_qty
        else:
            state["positions"][symbol] = {"quantity": quantity, "avg_price": price}

        self._save_state(state)
        logger.info(f"PaperLedger: Recorded BUY {quantity} {symbol} @ {price}. Cash remaining: {state['available_cash']:.2f}")
        return True

    def record_sell(self, symbol: str, quantity: float, price: float) -> bool:
        state = self._load_state()

        if symbol not in state["positions"] or state["positions"][symbol]["quantity"] < quantity:
            logger.error(f"PaperLedger: Insufficient shares to sell {quantity} {symbol}.")
            return False

        revenue = quantity * price

        # Add cash
        state["available_cash"] += revenue

        # Update position
        pos = state["positions"][symbol]
        pos["quantity"] -= quantity
        
        # Calculate realized P&L for this trade
        pnl = (price - pos["avg_price"]) * quantity
        logger.info(f"PaperLedger: Realized P&L for {symbol} trade: {pnl:.2f}")

        # Remove if 0
        if pos["quantity"] <= 0:
            del state["positions"][symbol]

        self._save_state(state)
        logger.info(f"PaperLedger: Recorded SELL {quantity} {symbol} @ {price}. Cash remaining: {state['available_cash']:.2f}")
        return True

    def get_portfolio_summary(self, current_prices: dict) -> dict:
        """
        Calculates total portfolio value based on current market prices.
        current_prices: {"RELIANCE.NS": 2600.0, ...}
        """
        state = self._load_state()
        cash = state["available_cash"]
        positions = state["positions"]
        
        stock_value = 0.0
        for sym, pos in positions.items():
            current_price = current_prices.get(sym, pos["avg_price"]) # fallback to avg if not found
            stock_value += pos["quantity"] * current_price

        total_value = cash + stock_value
        pnl = total_value - self.initial_balance
        pnl_pct = (pnl / self.initial_balance) * 100 if self.initial_balance > 0 else 0

        return {
            "cash": cash,
            "stock_value": stock_value,
            "total_value": total_value,
            "total_pnl": pnl,
            "total_pnl_pct": pnl_pct,
            "open_positions": len(positions)
        }
