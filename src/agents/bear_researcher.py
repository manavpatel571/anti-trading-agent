from src.core.state import AgentState
from src.config.llm_config import get_reasoning_llm

def bear_researcher_agent(state: AgentState) -> AgentState:
    """Builds bearish thesis"""
    llm = get_reasoning_llm()
    # Logic to be implemented
    return state
