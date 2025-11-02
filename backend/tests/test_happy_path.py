"""
Happy Path tests for Milestone 1.
"""
import pytest
from fastapi.testclient import TestClient


class TestHappyPath:
    """Happy path tests for core functionality."""

    def test_health_check_happy_path(self, client: TestClient):
        """Test: Health check returns successful response."""
        response = client.get("/health")

        # Assert successful response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "app" in data
        assert data["app"] == "DeepCard API"

    def test_get_llm_providers_happy_path(self, client: TestClient):
        """Test: Get supported LLM providers."""
        response = client.get("/api/v1/llm/providers")

        # Assert successful response
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert "openai" in data["providers"]
        assert "deepseek" in data["providers"]
        assert "details" in data
        assert "default_provider" in data

    def test_llm_factory_happy_path(self):
        """Test: LLM Factory creates providers correctly."""
        from app.infrastructure.llm import LLMFactory

        # Test getting supported providers
        providers = LLMFactory.get_supported_providers()
        assert isinstance(providers, list)
        assert "openai" in providers
        assert "deepseek" in providers

        # Test creating OpenAI provider
        openai_provider = LLMFactory.create_provider(
            provider_name="openai",
            api_key="test-key",
            model="gpt-3.5-turbo"
        )
        assert openai_provider.provider_name == "openai"
        assert openai_provider.model == "gpt-3.5-turbo"

        # Test creating DeepSeek provider
        deepseek_provider = LLMFactory.create_provider(
            provider_name="deepseek",
            api_key="test-key",
            model="deepseek-chat"
        )
        assert deepseek_provider.provider_name == "deepseek"
        assert deepseek_provider.model == "deepseek-chat"

    def test_llm_provider_initialization_happy_path(self):
        """Test: LLM providers initialize correctly."""
        from app.infrastructure.llm import OpenAIProvider, DeepSeekProvider

        # Test OpenAI provider initialization
        openai_provider = OpenAIProvider(
            api_key="test-key",
            model="gpt-3.5-turbo",
            timeout=30,
            max_retries=3
        )
        assert openai_provider.api_key == "test-key"
        assert openai_provider.model == "gpt-3.5-turbo"
        assert openai_provider.timeout == 30
        assert openai_provider.max_retries == 3
        assert openai_provider.provider_name == "openai"

        # Test DeepSeek provider initialization
        deepseek_provider = DeepSeekProvider(
            api_key="test-key",
            model="deepseek-chat",
            timeout=30,
            max_retries=3
        )
        assert deepseek_provider.api_key == "test-key"
        assert deepseek_provider.model == "deepseek-chat"
        assert deepseek_provider.timeout == 30
        assert deepseek_provider.max_retries == 3
        assert deepseek_provider.provider_name == "deepseek"

    def test_llm_provider_config_happy_path(self):
        """Test: LLM providers return correct config."""
        from app.infrastructure.llm import OpenAIProvider

        provider = OpenAIProvider(
            api_key="test-key",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=1000
        )

        config = provider.get_config()
        assert config["provider"] == "openai"
        assert config["model"] == "gpt-3.5-turbo"
        assert config["timeout"] == 30  # default value
        assert config["max_retries"] == 3  # default value

    def test_api_docs_happy_path(self, client: TestClient):
        """Test: API documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema_happy_path(self, client: TestClient):
        """Test: OpenAPI schema is available."""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_root_endpoint_happy_path(self, client: TestClient):
        """Test: Root endpoint returns welcome message."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "DeepCard" in data["message"]