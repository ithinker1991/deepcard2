"""
LLM Provider Factory.
"""
from typing import Dict, Any

from app.infrastructure.llm.base import LLMProvider, LLMConfigurationError
from app.infrastructure.llm.openai import OpenAIProvider
from app.infrastructure.llm.deepseek import DeepSeekProvider
from app.infrastructure.llm.siliconflow import SiliconFlowProvider


class LLMFactory:
    """Factory for creating LLM provider instances."""

    # Registry of available providers
    _providers = {
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        "siliconflow": SiliconFlowProvider,
    }

    @classmethod
    def create_provider(
        cls,
        provider_name: str,
        api_key: str,
        model: str = None,
        **kwargs
    ) -> LLMProvider:
        """Create an LLM provider instance."""
        if provider_name not in cls._providers:
            raise LLMConfigurationError(f"Unknown LLM provider: {provider_name}")

        provider_class = cls._providers[provider_name]
        return provider_class(api_key=api_key, model=model, **kwargs)

    @classmethod
    def get_supported_providers(cls) -> list[str]:
        """Get list of supported LLM providers."""
        return list(cls._providers.keys())

    @classmethod
    def get_provider_models(cls, provider_name: str) -> Dict[str, Any]:
        """Get available models for a provider."""
        models_config = {
            "openai": {
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
                "default": "gpt-3.5-turbo",
                "description": "OpenAI GPT models"
            },
            "deepseek": {
                "models": ["deepseek-chat", "deepseek-coder"],
                "default": "deepseek-chat",
                "description": "DeepSeek AI models"
            },
            "siliconflow": {
                "models": ["deepseek-ai/DeepSeek-V3", "Qwen/Qwen2.5-7B-Instruct", "meta-llama/Llama-3.1-8B-Instruct"],
                "default": "deepseek-ai/DeepSeek-V3",
                "description": "SiliconFlow hosted models"
            }
        }
        return models_config.get(provider_name, {})

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new LLM provider."""
        cls._providers[name] = provider_class

    @classmethod
    def create_provider_from_config(cls, config: Dict[str, Any]) -> LLMProvider:
        """Create provider from configuration dictionary."""
        provider_name = config.get("provider")
        api_key = config.get("api_key")
        model = config.get("model")

        if not provider_name or not api_key:
            raise LLMConfigurationError("Provider name and API key are required")

        # Extract provider-specific config
        provider_config = {k: v for k, v in config.items()
                          if k not in ["provider", "api_key", "model"]}

        return cls.create_provider(
            provider_name=provider_name,
            api_key=api_key,
            model=model,
            **provider_config
        )