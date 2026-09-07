from datetime import datetime
from src.core.state import AgentState
from src.core.models import VotingResult, ActionType, Signal

def voting_agent(state: AgentState) -> dict:
    """Aggregates signals and debates to form consensus"""
    signals = state.get("signals", [])
    
    if not signals:
        return {"voting_result": None}
        
    bull_signals = [s for s in signals if s.action == ActionType.BUY]
    bear_signals = [s for s in signals if s.action == ActionType.SELL]
    
    # Check for vetoes
    veto = False
    action = ActionType.HOLD
    reason = ""
    
    for s in signals:
        if s.agent_name == "NewsSentiment" and s.action == ActionType.SELL and s.confidence >= 75:
            veto = True
            action = ActionType.SELL
            reason = "VETO: Strong negative news sentiment overrides technicals."
            break
            
    if not veto:
        if len(bull_signals) > len(bear_signals):
            action = ActionType.BUY
        elif len(bear_signals) > len(bull_signals):
            action = ActionType.SELL
        else:
            action = ActionType.HOLD

    avg_confidence = sum(s.confidence for s in signals) / len(signals) if signals else 0
    consensus_pct = max(len(bull_signals), len(bear_signals)) / len(signals) * 100 if signals else 0
    
    if veto:
        consensus_pct = 100.0 # Veto represents absolute consensus
        
    dissenting_views = []
    if action == ActionType.BUY:
        dissenting_views = [f"{s.agent_name} says SELL" for s in bear_signals]
    elif action == ActionType.SELL:
        dissenting_views = [f"{s.agent_name} says BUY" for s in bull_signals]
        
    result = VotingResult(
        timestamp=datetime.now(),
        symbol=state.get("symbol", ""),
        action=action,
        consensus_pct=consensus_pct,
        avg_confidence=avg_confidence,
        dissenting_views=dissenting_views,
        signals=signals
    )
    
    return {"voting_result": result}
