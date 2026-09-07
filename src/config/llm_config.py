from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import settings

def get_reasoning_llm():
    """Returns Claude Opus for complex reasoning tasks"""
    # Fallback to Gemini Pro if Claude key is missing, or we can use Opus as intended
    if settings.ANTHROPIC_API_KEY:
        return ChatAnthropic(
            model="claude-3-opus-20240229",
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            temperature=0.2
        )
    return get_analysis_llm()

def get_analysis_llm():
    """Returns Gemini Pro for data analysis tasks"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.1
    )

def get_routine_llm():
    """Returns Gemini Flash for fast/cheap routine tasks"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.0
    )
