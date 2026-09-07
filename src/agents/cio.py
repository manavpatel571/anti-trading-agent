import os
import logging
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from src.core.state import AgentState
from src.core.models import ActionType

logger = logging.getLogger(__name__)

class CIODecision(BaseModel):
    approved: bool = Field(description="Whether the CIO approves the proposed trade")
    reasoning: str = Field(description="The CIO's rationale for approving or rejecting the trade")

def cio_agent(state: AgentState) -> AgentState:
    """Acts as the Chief Investment Officer (CIO) to make a final LLM-based approval."""
    logger.info("CIO Agent: Evaluating proposed trade...")
    
    voting_result = state.get("voting_result")
    
    if not voting_result or voting_result.action == ActionType.HOLD:
        logger.info("CIO Agent: No trade proposed. Passing.")
        return {"cio_approval": True, "cio_reasoning": "No action to approve"}
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("CIO Agent: GEMINI_API_KEY not found. Auto-approving trade.")
        return {"cio_approval": True, "cio_reasoning": "Auto-approved (No LLM key)"}
        
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            google_api_key=api_key,
            temperature=0.0
        )
        # Using with_structured_output for guaranteed boolean/string format
        structured_llm = llm.with_structured_output(CIODecision)
        
        prompt = PromptTemplate.from_template("""
        You are the Chief Investment Officer (CIO) of an AI hedge fund. 
        Your junior algorithmic agents have proposed a trade. Review the data and decide if the trade is safe.
        
        Symbol: {symbol}
        Action Proposed: {action}
        Consensus: {consensus}%
        Confidence: {confidence}%
        
        News & Sentiment Data:
        {sentiment}
        
        Market Snapshot:
        LTP: {ltp}, VIX: {vix}
        
        Dissenting Views (if any):
        {dissent}
        
        Should we execute this trade? Consider capital preservation your highest priority.
        If the VIX is very high or sentiment is highly negative against a BUY, you should reject.
        """)
        
        snapshot = state.get("market_snapshot")
        news = state.get("news_sentiment", {})
        
        response: CIODecision = structured_llm.invoke(prompt.format(
            symbol=state.get("symbol", "UNKNOWN"),
            action=voting_result.action.value,
            consensus=voting_result.consensus_pct,
            confidence=voting_result.avg_confidence,
            sentiment=str(news),
            ltp=snapshot.ltp if snapshot else "N/A",
            vix=snapshot.vix if snapshot else "N/A",
            dissent=str(voting_result.dissenting_views)
        ))
        
        logger.info(f"CIO Decision: Approved={response.approved}, Reason: {response.reasoning}")
        return {
            "cio_approval": response.approved,
            "cio_reasoning": response.reasoning
        }
        
    except Exception as e:
        logger.error(f"CIO Agent error: {e}")
        # Default to reject if LLM fails for safety
        return {
            "cio_approval": False,
            "cio_reasoning": f"LLM API Error: {str(e)}"
        }
