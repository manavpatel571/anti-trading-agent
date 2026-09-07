from src.core.state import AgentState
from src.config.llm_config import get_analysis_llm

def macro_agent(state: AgentState) -> AgentState:
    """Analyzes macro conditions"""
    llm = get_analysis_llm()
    # Logic to be implemented
    return state
