from typing import Annotated, TypedDict, List, Dict, Any, Optional
from datetime import datetime
import operator

from src.core.models import MarketSnapshot, Signal, VotingResult, RiskAssessment, TradeRecord

def merge_signals(old: List[Signal], new: List[Signal]) -> List[Signal]:
    if not new:
        return old
    return old + new

class AgentState(TypedDict):
    # Context
    symbol: str
    timestamp: datetime
    market_snapshot: Optional[MarketSnapshot]
    
    # Intelligence inputs
    news_sentiment: Dict[str, Any]
    macro_outlook: Dict[str, Any]
    
    # Analysis signals
    signals: Annotated[List[Signal], merge_signals]
    
    # Debate texts
    bull_thesis: str
    bear_thesis: str
    
    # Decisions
    voting_result: Optional[VotingResult]
    risk_assessment: Optional[RiskAssessment]
    cio_approval: bool
    cio_reasoning: str
    
    # Execution
    trade_record: Optional[TradeRecord]
