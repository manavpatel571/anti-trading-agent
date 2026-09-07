import pandas as pd
from src.core.state import AgentState
from src.core.models import Signal, ActionType
from src.indicators.technical_calculator import TechnicalCalculator
import logging

logger = logging.getLogger(__name__)

def technical_analysis_agent(state: AgentState) -> AgentState:
    """Calculates TA signals using TechnicalCalculator"""
    logger.info("Technical Analysis Agent: Analyzing data")
    
    historical_data = state.get("macro_outlook", {}).get("historical_data", [])
    
    if not historical_data:
        logger.warning("No historical data found in state")
        return {}
        
    df = pd.DataFrame(historical_data)
    
    # Calculate indicators
    df = TechnicalCalculator.calculate_all(df)
    
    # Get consensus signal
    signal_data = TechnicalCalculator.get_signal(df)
    
    action_str = signal_data.get("action", "HOLD")
    action = ActionType.HOLD
    if action_str == "BUY":
        action = ActionType.BUY
    elif action_str == "SELL":
        action = ActionType.SELL
        
    signal = Signal(
        agent_name="TechnicalAnalysis",
        action=action,
        confidence=signal_data.get("confidence", 0.0) * 100.0, # 0-100 scale
        reasoning=signal_data.get("reason", "No distinct signal")
    )
    
    logger.info(f"Technical signal generated: {signal.action.value} with {signal.confidence}% confidence")
    
    return {"signals": [signal]}
