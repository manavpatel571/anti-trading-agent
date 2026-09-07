from src.core.state import AgentState
from src.config.llm_config import get_analysis_llm

def smart_money_agent(state: AgentState) -> AgentState:
    """Detects SMC patterns"""
    llm = get_analysis_llm()
    # Logic to be implemented
    return state
