import logging
from src.core.graph import create_trading_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Anti-Trading Agent (Paper Trading Mode)")
    graph = create_trading_graph()
    logger.info("Trading graph compiled. Ready for execution.")
    # Implementation for running the graph on a schedule
    
if __name__ == "__main__":
    main()
