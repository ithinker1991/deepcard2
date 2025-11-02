"""
Test configuration and fixtures.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from typing import Generator

from app.main import app
from app.shared.config import get_settings
from app.shared.testing_config import get_testing_config

# 获取测试配置
testing_config = get_testing_config()


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


def pytest_configure(config):
    """pytest配置钩子"""
    config.addinivalue_line(
        "markers", "database: mark test as database test"
    )
    config.addinivalue_line(
        "markers", "llm: mark test as LLM test"
    )
    config.addinivalue_line(
        "markers", "external_api: mark test as external API test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )


def pytest_collection_modifyitems(config, items):
    """根据配置动态跳过测试"""
    skip_database = not testing_config.should_run_database_tests
    skip_llm = not testing_config.should_run_llm_tests
    skip_external = not testing_config.enable_external_api_tests
    skip_performance = not testing_config.enable_performance_tests

    for item in items:
        if skip_database and "database" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Database tests disabled"))
        if skip_llm and "llm" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="LLM tests disabled"))
        if skip_external and "external_api" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="External API tests disabled"))
        if skip_performance and "performance" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Performance tests disabled"))


# 测试装饰器
def requires_database(func):
    """需要数据库的测试装饰器"""
    func = pytest.mark.database(func)
    return func


def requires_llm(func):
    """需要LLM的测试装饰器"""
    func = pytest.mark.llm(func)
    return func


def requires_external_api(func):
    """需要外部API的测试装饰器"""
    func = pytest.mark.external_api(func)
    return func


def requires_performance(func):
    """需要性能测试的装饰器"""
    func = pytest.mark.performance(func)
    return func


# 数据库测试fixture
@pytest.fixture
def test_db_config():
    """提供测试数据库配置"""
    return testing_config.test_database_url


# LLM测试fixture
@pytest.fixture
def llm_test_config():
    """提供LLM测试配置"""
    return {
        "provider": testing_config.llm_test_provider,
        "model": testing_config.llm_test_model,
        "max_calls": testing_config.max_llm_test_calls
    }


# 性能测试fixture
@pytest.fixture
def performance_test_config():
    """提供性能测试配置"""
    return {
        "timeout": testing_config.performance_test_timeout
    }


@pytest.fixture
def cleanup_test_data():
    """测试数据清理fixture"""
    import os

    # 测试前不清理
    yield

    # 测试后根据配置清理
    if testing_config.cleanup_test_data:
        test_db_path = testing_config.test_database_url.replace("sqlite:///", "")
        if os.path.exists(test_db_path):
            try:
                os.remove(test_db_path)
            except Exception:
                pass  # 忽略清理错误