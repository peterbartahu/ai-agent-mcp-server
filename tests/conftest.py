import pytest
from app.agent.llm import FakeLLM

@pytest.fixture
def fake_llm():
    return FakeLLM()