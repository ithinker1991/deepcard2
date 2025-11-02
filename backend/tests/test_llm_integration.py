"""
Test LLM API endpoints integration.
"""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient


class TestLLMAPIEndpoints:
    """Test LLM API endpoints."""

    def test_get_llm_providers(self, client: TestClient):
        """Test getting LLM providers endpoint."""
        response = client.get("/api/v1/llm/providers")

        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert "openai" in data["providers"]
        assert "deepseek" in data["providers"]
        assert "details" in data
        assert "default_provider" in data

    @patch('app.infrastructure.llm.openai.OpenAIProvider.test_connection')
    async def test_test_llm_connection_success(self, mock_test, client: TestClient):
        """Test successful LLM connection test."""
        # Mock successful connection test
        mock_test.return_value = {
            "status": "success",
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "test_response": "Hello, OpenAI!",
            "message": "Connection successful"
        }

        response = client.post(
            "/api/v1/llm/test",
            json={
                "provider": "openai",
                "api_key": "test-key"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["provider"] == "openai"
        assert data["model"] == "gpt-3.5-turbo"

    def test_test_llm_connection_missing_provider(self, client: TestClient):
        """Test LLM connection test with missing provider."""
        response = client.post(
            "/api/v1/llm/test",
            json={"api_key": "test-key"}
        )

        assert response.status_code == 400
        data = response.json()
        assert "Provider name is required" in data["detail"]

    def test_test_llm_connection_missing_api_key(self, client: TestClient):
        """Test LLM connection test with missing API key."""
        response = client.post(
            "/api/v1/llm/test",
            json={"provider": "unknown_provider"}
        )

        assert response.status_code == 400
        assert "API key is required" in response.json()["detail"]

    @patch('app.infrastructure.llm.openai.OpenAIProvider.generate_with_retry')
    async def test_generate_text_success(self, mock_generate, client: TestClient):
        """Test successful text generation."""
        # Mock successful text generation
        mock_generate.return_value = "This is a generated response."

        response = client.post(
            "/api/v1/llm/generate",
            json={
                "provider": "openai",
                "prompt": "What is machine learning?",
                "max_tokens": 100,
                "temperature": 0.7
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "This is a generated response."
        assert data["provider"] == "openai"
        assert data["prompt"] == "What is machine learning?"
        assert data["parameters"]["max_tokens"] == 100
        assert data["parameters"]["temperature"] == 0.7

    def test_generate_text_missing_prompt(self, client: TestClient):
        """Test text generation with missing prompt."""
        response = client.post(
            "/api/v1/llm/generate",
            json={
                "provider": "openai",
                "max_tokens": 100
            }
        )

        assert response.status_code == 400
        assert "Prompt is required" in response.json()["detail"]

    @patch('app.infrastructure.llm.openai.OpenAIProvider.generate_with_retry')
    async def test_generate_text_with_default_provider(self, mock_generate, client: TestClient):
        """Test text generation with default provider."""
        mock_generate.return_value = "Generated text with default provider."

        response = client.post(
            "/api/v1/llm/generate",
            json={
                "prompt": "Test prompt"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Generated text with default provider."
        # Should use default provider from settings

    def test_generate_text_invalid_provider(self, client: TestClient):
        """Test text generation with invalid provider."""
        response = client.post(
            "/api/v1/llm/generate",
            json={
                "provider": "invalid_provider",
                "prompt": "Test prompt",
                "api_key": "test-key"
            }
        )

        assert response.status_code == 400
        assert "Unknown LLM provider" in response.json()["detail"]