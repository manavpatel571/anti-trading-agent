from src.core.state import AgentState
from src.config.llm_config import get_reasoning_llm

def bull_researcher_agent(state: AgentState) -> AgentState:
    """Builds bullish thesis"""
    llm = get_reasoning_llm()
    # Logic to be implemented
    return state
