from src.core.state import AgentState
from src.core.models import RiskAssessment, ActionType
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def risk_manager_agent(state: AgentState) -> AgentState:
    """Evaluates risk and determines position size based on ATR and Volatility."""
    logger.info("Risk Manager Agent: Assessing risk")
    
    # 1. Fetch required data from state
    voting_result = state.get("voting_result")
    historical_data = state.get("macro_outlook", {}).get("historical_data", [])
    snapshot = state.get("market_snapshot")
    
    # If no voting result or hold, no risk assessment needed
    if not voting_result or voting_result.action == ActionType.HOLD:
        logger.info("No trade action proposed. Risk assessment skipped.")
        return {"risk_assessment": None}
        
    # Check if CIO approved (if CIO is part of the flow before risk, or risk can just do its own check)
    if not state.get("cio_approval", True):
        logger.warning("CIO rejected the trade. Risk manager enforcing.")
        return {"risk_assessment": RiskAssessment(
            approved=False,
            reason="CIO Rejected trade",
            adjusted_position_size=0,
            stop_loss=0.0
        )}
        
    # 2. Extract ATR for stop loss calculation
    atr = 0.0
    if historical_data:
        df = pd.DataFrame(historical_data)
        if 'ATR_14' in df.columns and not df.empty:
            atr = df['ATR_14'].iloc[-1]
            
    if pd.isna(atr) or atr <= 0:
        logger.warning("ATR not available or invalid. Defaulting to 1% of price.")
        if snapshot:
            atr = snapshot.ltp * 0.01
        else:
            atr = 1.0 # arbitrary fallback
            
    # 3. Position Sizing
    # Max risk per trade: 1% of portfolio (assuming 100k capital for sandbox)
    capital = 100000.0
    max_risk_amount = capital * 0.01 
    
    # Position size = Risk Amount / Stop Loss Distance (ATR)
    # Using 1.5x ATR for Stop Loss
    stop_loss_distance = 1.5 * atr
    
    if stop_loss_distance > 0:
        position_size = int(max_risk_amount / stop_loss_distance)
    else:
        position_size = 0
        
    # 4. Volatility / Circuit Breakers
    vix = snapshot.vix if snapshot else 15.0
    
    if vix > 30:
        approved = False
        reason = f"Extreme Volatility (VIX: {vix:.2f} > 30). Circuit breaker tripped."
        position_size = 0
    elif position_size == 0:
        approved = False
        reason = "Calculated position size is 0."
    else:
        approved = True
        reason = "Risk checks passed. Position sized by ATR."
        
    # Calculate absolute stop loss price
    ltp = snapshot.ltp if snapshot else 0.0
    if voting_result.action == ActionType.BUY:
        stop_loss_price = ltp - stop_loss_distance
        take_profit = ltp + (stop_loss_distance * 2) # 1:2 R:R
    else: # SELL
        stop_loss_price = ltp + stop_loss_distance
        take_profit = max(0.0, ltp - (stop_loss_distance * 2))
        
    assessment = RiskAssessment(
        approved=approved,
        reason=reason,
        adjusted_position_size=position_size,
        stop_loss=round(stop_loss_price, 2),
        take_profit=round(take_profit, 2)
    )
    
    logger.info(f"Risk Assessment: Approved={approved}, Size={position_size}, Reason={reason}")
    
    return {"risk_assessment": assessment}
