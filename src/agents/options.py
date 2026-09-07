from src.core.state import AgentState
from src.config.llm_config import get_analysis_llm

def options_agent(state: AgentState) -> AgentState:
    """Analyzes option chain data"""
    llm = get_analysis_llm()
    # Logic to be implemented
    return state
