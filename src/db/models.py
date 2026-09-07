from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(String, unique=True, index=True)
    symbol = Column(String, index=True)
    action = Column(String)
    quantity = Column(Integer)
    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float, nullable=True)
    timestamp = Column(DateTime)
    status = Column(String)
    exit_price = Column(Float, nullable=True)
    exit_timestamp = Column(DateTime, nullable=True)
    pnl = Column(Float, nullable=True)
    pnl_pct = Column(Float, nullable=True)
    reasoning = Column(String)
