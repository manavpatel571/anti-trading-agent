import os
import time
import logging
from datetime import datetime
from src.core.graph import create_trading_graph
from src.core.state import AgentState
from src.agents.screener import get_top_stocks
from src.core.paper_ledger import PaperLedger
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_trading_cycle():
    """Runs one full cycle of the trading system."""
    logger.info("=== Starting New Trading Cycle ===")
    
    # 1. Screen for the best stocks dynamically
    symbols = get_top_stocks(limit=5)
    logger.info(f"Today's target symbols from Screener: {symbols}")
    
    graph = create_trading_graph()
    
    # Track the LTP of each symbol to calculate Portfolio Value later
    current_prices = {}
    
    for symbol in symbols:
        logger.info(f"--- Analyzing {symbol} ---")
        
        # Initialize fresh state for this symbol
        state: AgentState = {
            "symbol": symbol,
            "timestamp": datetime.now(),
            "market_snapshot": None,
            "news_sentiment": {},
            "macro_outlook": {},
            "signals": [],
            "bull_thesis": "",
            "bear_thesis": "",
            "voting_result": None,
            "risk_assessment": None,
            "cio_approval": True,
            "cio_reasoning": "",
            "trade_record": None
        }
        
        try:
            final_state = graph.invoke(state)
            
            # Store LTP for portfolio valuation
            snapshot = final_state.get("market_snapshot")
            if snapshot:
                current_prices[symbol] = snapshot.ltp
            
            voting = final_state.get("voting_result")
            if voting:
                logger.info(f"Result for {symbol}: {voting.action.value} (Confidence: {voting.avg_confidence}%)")
            else:
                logger.info(f"Result for {symbol}: No action determined.")
                
        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}")
            
    # Print Paper Trading P&L
    try:
        ledger = PaperLedger()
        summary = ledger.get_portfolio_summary(current_prices)
        logger.info("=== 📈 PAPER TRADING PORTFOLIO SUMMARY ===")
        logger.info(f"Available Cash : ₹{summary['cash']:,.2f}")
        logger.info(f"Stock Value    : ₹{summary['stock_value']:,.2f}")
        logger.info(f"Total Value    : ₹{summary['total_value']:,.2f}")
        logger.info(f"Total P&L      : ₹{summary['total_pnl']:,.2f} ({summary['total_pnl_pct']:.2f}%)")
        logger.info(f"Open Positions : {summary['open_positions']}")
        logger.info("==========================================")
    except Exception as e:
        logger.error(f"Failed to print portfolio summary: {e}")
        
    logger.info("=== Trading Cycle Complete ===")

if __name__ == "__main__":
    load_dotenv()
    
    logger.info("Initializing Agentic Trading System (with Screener & Paper Ledger)")
    
    run_once = os.getenv("RUN_ONCE", "False").lower() in ("true", "1", "yes")
    
    if run_once:
        run_trading_cycle()
    else:
        while True:
            try:
                run_trading_cycle()
                
                # Sleep for 15 minutes before the next cycle
                sleep_seconds = 15 * 60
                logger.info(f"Sleeping for {sleep_seconds} seconds...")
                time.sleep(sleep_seconds)
            except KeyboardInterrupt:
                logger.info("Trading system stopped by user.")
                break
            except Exception as e:
                logger.error(f"Critical error in main loop: {e}")
                time.sleep(60) # Sleep briefly before retrying
