from src.core.state import AgentState
from src.config.llm_config import get_analysis_llm

def memory_eval_agent(state: AgentState) -> AgentState:
    """Stores trade history and evaluates performance"""
    llm = get_analysis_llm()
    # Logic to be implemented
    return state
