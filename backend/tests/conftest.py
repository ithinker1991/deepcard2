"""
Test configuration and fixtures.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.shared.config import get_settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def test_settings():
    """Get test settings."""
    return get_settings()


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a test response from OpenAI."
                }
            }
        ]
    }


@pytest.fixture
def mock_deepseek_response():
    """Mock DeepSeek API response."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a test response from DeepSeek."
                }
            }
        ]
    }


# Test data
VALID_LLM_REQUEST = {
    "provider": "openai",
    "prompt": "What is machine learning?",
    "max_tokens": 100,
    "temperature": 0.7
}

INVALID_LLM_REQUEST = {
    "provider": "invalid_provider",
    "prompt": ""
}

LLM_TEST_REQUEST = {
    "provider": "openai",
    "api_key": "test-api-key"
}