from sqlalchemy.orm import Session
from src.db.models import Trade

class TradeRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def save_trade(self, trade_data: dict) -> Trade:
        trade = Trade(**trade_data)
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade
