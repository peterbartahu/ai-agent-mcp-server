import os
from dotenv import load_dotenv
from app.agent.llm_fake import FakeLLM
from app.agent.llm_openai import OpenAILLM

load_dotenv()


def create_llm():
    """Factory method for selecting the LLM implementation.
    
    Defaults to FakeLLM for local development and tests.
    Set USE_OPENAI=true in .env to use OpenAI LLM.
    """
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    if use_openai:
        return OpenAILLM()
    return FakeLLM()