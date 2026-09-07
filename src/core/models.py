from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ActionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class MarketRegime(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"
    VOLATILE = "VOLATILE"

class MarketSnapshot(BaseModel):
    timestamp: datetime
    symbol: str
    ltp: float
    volume: int
    vix: float
    # Detailed OHLCV, option chain data etc. can be added here or referenced

class Signal(BaseModel):
    agent_name: str
    action: ActionType
    confidence: float = Field(..., ge=0.0, le=100.0)
    reasoning: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class VotingResult(BaseModel):
    timestamp: datetime
    symbol: str
    action: ActionType
    consensus_pct: float
    avg_confidence: float
    dissenting_views: List[str]
    signals: List[Signal]

class RiskAssessment(BaseModel):
    approved: bool
    reason: str
    adjusted_position_size: int = 0
    stop_loss: float = 0.0
    take_profit: Optional[float] = None
    
class TradeRecord(BaseModel):
    trade_id: str
    symbol: str
    action: ActionType
    quantity: int
    entry_price: float
    stop_loss: float
    take_profit: Optional[float] = None
    timestamp: datetime
    status: str = "OPEN" # OPEN, CLOSED, REJECTED
    exit_price: Optional[float] = None
    exit_timestamp: Optional[datetime] = None
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None
    reasoning: str = ""
