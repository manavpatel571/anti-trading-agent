from langgraph.graph import StateGraph, END
from src.core.state import AgentState
from src.agents.market_data import market_data_agent
from src.agents.technical import technical_analysis_agent
from src.agents.news_sentiment import news_sentiment_agent
from src.agents.voting import voting_agent
from src.agents.risk_manager import risk_manager_agent
from src.agents.cio import cio_agent
from src.agents.execution import execution_agent
from src.core.models import ActionType

def should_route_to_risk(state: AgentState) -> str:
    """If voting decides to HOLD, we don't need to run CIO or Risk Manager"""
    voting_result = state.get("voting_result")
    if not voting_result or voting_result.action == ActionType.HOLD:
        return "end"
    return "cio_agent"

def create_trading_graph():
    """Builds the LangGraph trading workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("market_data", market_data_agent)
    workflow.add_node("technical", technical_analysis_agent)
    workflow.add_node("sentiment", news_sentiment_agent)
    workflow.add_node("voting", voting_agent)
    workflow.add_node("cio_agent", cio_agent)
    workflow.add_node("risk_manager", risk_manager_agent)
    workflow.add_node("execution", execution_agent)
    
    # Define edges
    # 1. Start with market data
    workflow.set_entry_point("market_data")
    
    # 2. Market data feeds into both technical and sentiment in parallel
    workflow.add_edge("market_data", "technical")
    workflow.add_edge("market_data", "sentiment")
    
    # 3. Both technical and sentiment feed into voting
    workflow.add_edge("technical", "voting")
    workflow.add_edge("sentiment", "voting")
    
    # 4. Voting routes to CIO if Action is BUY/SELL, else END
    workflow.add_conditional_edges(
        "voting",
        should_route_to_risk,
        {
            "cio_agent": "cio_agent",
            "end": END
        }
    )
    
    # 5. CIO goes to risk manager
    workflow.add_edge("cio_agent", "risk_manager")
    
    # 5. Risk manager goes to execution
    workflow.add_edge("risk_manager", "execution")
    
    # 6. Execution goes to END
    workflow.add_edge("execution", END)
    
    return workflow.compile()
