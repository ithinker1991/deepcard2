"""
Test LLM provider functionality.
"""
import pytest
from unittest.mock import patch, AsyncMock

from app.infrastructure.llm import LLMFactory, LLMConfigurationError
from app.infrastructure.llm.openai import OpenAIProvider
from app.infrastructure.llm.deepseek import DeepSeekProvider


class TestLLMFactory:
    """Test LLM Factory."""

    def test_get_supported_providers(self):
        """Test getting supported providers."""
        providers = LLMFactory.get_supported_providers()
        assert "openai" in providers
        assert "deepseek" in providers
        assert isinstance(providers, list)

    def test_get_provider_models(self):
        """Test getting provider models."""
        openai_models = LLMFactory.get_provider_models("openai")
        assert "models" in openai_models
        assert "default" in openai_models
        assert "gpt-3.5-turbo" in openai_models["models"]

        deepseek_models = LLMFactory.get_provider_models("deepseek")
        assert "models" in deepseek_models
        assert "deepseek-chat" in deepseek_models["models"]

    def test_create_openai_provider(self):
        """Test creating OpenAI provider."""
        provider = LLMFactory.create_provider(
            provider_name="openai",
            api_key="test-key",
            model="gpt-3.5-turbo"
        )
        assert isinstance(provider, OpenAIProvider)
        assert provider.provider_name == "openai"
        assert provider.model == "gpt-3.5-turbo"

    def test_create_deepseek_provider(self):
        """Test creating DeepSeek provider."""
        provider = LLMFactory.create_provider(
            provider_name="deepseek",
            api_key="test-key",
            model="deepseek-chat"
        )
        assert isinstance(provider, DeepSeekProvider)
        assert provider.provider_name == "deepseek"
        assert provider.model == "deepseek-chat"

    def test_create_unknown_provider(self):
        """Test creating unknown provider raises error."""
        with pytest.raises(LLMConfigurationError):
            LLMFactory.create_provider(
                provider_name="unknown",
                api_key="test-key"
            )


class TestOpenAIProvider:
    """Test OpenAI provider."""

    def test_provider_initialization(self):
        """Test OpenAI provider initialization."""
        provider = OpenAIProvider(
            api_key="test-key",
            model="gpt-3.5-turbo",
            timeout=10,
            max_retries=2
        )
        assert provider.api_key == "test-key"
        assert provider.model == "gpt-3.5-turbo"
        assert provider.timeout == 10
        assert provider.max_retries == 2
        assert provider.provider_name == "openai"

    @patch('httpx.AsyncClient.post')
    async def test_generate_text_success(self, mock_post):
        """Test successful text generation."""
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Generated text"}}]
        }
        mock_post.return_value = mock_response

        provider = OpenAIProvider(api_key="test-key", model="gpt-3.5-turbo")
        result = await provider.generate_text("Test prompt")

        assert result == "Generated text"
        mock_post.assert_called_once()

    @patch('httpx.AsyncClient.post')
    async def test_test_connection_success(self, mock_post):
        """Test successful connection test."""
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello, OpenAI!"}}]
        }
        mock_post.return_value = mock_response

        provider = OpenAIProvider(api_key="test-key", model="gpt-3.5-turbo")
        result = await provider.test_connection()

        assert result["status"] == "success"
        assert result["provider"] == "openai"
        assert result["model"] == "gpt-3.5-turbo"
        assert "test_response" in result


class TestDeepSeekProvider:
    """Test DeepSeek provider."""

    def test_provider_initialization(self):
        """Test DeepSeek provider initialization."""
        provider = DeepSeekProvider(
            api_key="test-key",
            model="deepseek-chat",
            timeout=10,
            max_retries=2
        )
        assert provider.api_key == "test-key"
        assert provider.model == "deepseek-chat"
        assert provider.timeout == 10
        assert provider.max_retries == 2
        assert provider.provider_name == "deepseek"

    @patch('httpx.AsyncClient.post')
    async def test_generate_text_success(self, mock_post):
        """Test successful text generation."""
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Generated text"}}]
        }
        mock_post.return_value = mock_response

        provider = DeepSeekProvider(api_key="test-key", model="deepseek-chat")
        result = await provider.generate_text("Test prompt")

        assert result == "Generated text"
        mock_post.assert_called_once()

    @patch('httpx.AsyncClient.post')
    async def test_test_connection_success(self, mock_post):
        """Test successful connection test."""
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello, DeepSeek!"}}]
        }
        mock_post.return_value = mock_response

        provider = DeepSeekProvider(api_key="test-key", model="deepseek-chat")
        result = await provider.test_connection()

        assert result["status"] == "success"
        assert result["provider"] == "deepseek"
        assert result["model"] == "deepseek-chat"
        assert "test_response" in result