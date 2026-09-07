import logging
from src.core.state import AgentState
from src.core.models import ActionType
from src.brokers.dhan import DhanBroker
from src.core.paper_ledger import PaperLedger

logger = logging.getLogger(__name__)

def execution_agent(state: AgentState) -> AgentState:
    """Executes trades via the broker if risk assessment is approved."""
    logger.info("Execution Agent: Preparing to execute trade")
    
    symbol = state.get("symbol")
    voting_result = state.get("voting_result")
    risk_assessment = state.get("risk_assessment")
    
    # Validation checks
    if not symbol:
        logger.error("Execution skipped: No symbol found in state")
        return {}
        
    if not voting_result or voting_result.action == ActionType.HOLD:
        logger.info("Execution skipped: Voting result is HOLD or None")
        return {}
        
    if not risk_assessment or not risk_assessment.approved:
        logger.warning(f"Execution skipped: Risk Assessment not approved. Reason: {risk_assessment.reason if risk_assessment else 'Unknown'}")
        return {}
        
    if risk_assessment.adjusted_position_size <= 0:
        logger.warning("Execution skipped: Position size is 0")
        return {}

    # Initialize Broker
    broker = DhanBroker()
    connected = broker.connect()
    
    if not connected:
        logger.error("Execution failed: Could not connect to DhanBroker")
        return {}
        
    # Get the action and price
    action_str = voting_result.action.value  # "BUY" or "SELL"
    quantity = risk_assessment.adjusted_position_size
    
    # We will use market snapshot's LTP to set a limit order just for safety
    snapshot = state.get("market_snapshot")
    if snapshot and snapshot.ltp > 0:
        price = snapshot.ltp
        # If BUY, maybe set limit slightly higher to ensure execution, or just use LIMIT exactly at LTP
        # For simplicity, using the exact LTP
    else:
        logger.error("Execution failed: No valid LTP found in MarketSnapshot")
        return {}
        
    # Execute trade
    logger.info(f"Placing {action_str} order for {quantity} shares of {symbol} at LIMIT {price}")
    order_id = broker.place_order(
        symbol=symbol,
        action=action_str,
        quantity=quantity,
        price=price,
        order_type="LIMIT"
    )
    
    if order_id:
        logger.info(f"Trade Execution Successful. Order ID: {order_id}")
        
        # If in DRY RUN, record to Paper Ledger
        if getattr(broker, 'dry_run', True):
            ledger = PaperLedger()
            if action_str == "BUY":
                ledger.record_buy(symbol, quantity, price)
            elif action_str == "SELL":
                ledger.record_sell(symbol, quantity, price)
                
        # Note: in a real system we might record this execution in a real database here.
    else:
        logger.error("Trade Execution Failed: Broker returned empty order ID")
        
    return {}
