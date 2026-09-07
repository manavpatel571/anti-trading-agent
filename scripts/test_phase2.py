import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.state import AgentState
from src.core.graph import create_trading_graph
from datetime import datetime
import json

def test_pipeline():
    print("Starting LangGraph pipeline test...")
    state: AgentState = {
        "symbol": "RELIANCE.NS",
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
    
    graph = create_trading_graph()
    
    # Run the graph
    print("Running workflow...")
    final_state = graph.invoke(state)
    
    print("\n--- Workflow Complete ---")
    print(f"Market Snapshot: {final_state.get('market_snapshot') is not None}")
    print(f"Signals Generated: {len(final_state.get('signals', []))}")
    
    voting_res = final_state.get("voting_result")
    if voting_res:
        print(f"\nVoting Result: {voting_res.action}")
        print(f"Consensus: {voting_res.consensus_pct}%")
        print(f"Confidence: {voting_res.avg_confidence}%")
        print(f"Dissenting Views: {voting_res.dissenting_views}")
    
    risk_res = final_state.get("risk_assessment")
    if risk_res:
        print(f"\nRisk Assessment: Approved={risk_res.approved}")
        if risk_res.approved:
            print(f"Position Size: {risk_res.adjusted_position_size}")
            print(f"Stop Loss: {risk_res.stop_loss}")
            print(f"Take Profit: {risk_res.take_profit}")
        else:
            print(f"Reason: {risk_res.reason}")
    else:
        print("\nRisk Manager did not run (likely HOLD action).")
        
    print("\nPipeline test complete.")

if __name__ == "__main__":
    test_pipeline()
