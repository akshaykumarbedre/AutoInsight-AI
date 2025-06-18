import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from autogen_ext.models.openai import OpenAIChatCompletionClient

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def get_llm(api_key: str = None):
    """Get LangChain ChatOpenAI instance"""
    if not api_key:
        api_key = load_environment()
    
    return ChatOpenAI(
        model="gpt-4.1-mini-2025-04-14",
        api_key=api_key,
    )

def get_openai_client(model: str = "gpt-4o-mini"):
    """Get OpenAI chat completion client"""
    return OpenAIChatCompletionClient(model=model)
