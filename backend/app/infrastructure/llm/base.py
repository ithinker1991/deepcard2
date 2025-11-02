"""
Base LLM provider interface.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import asyncio


class LLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.timeout = kwargs.get('timeout', 30)
        self.max_retries = kwargs.get('max_retries', 3)
        self._config = kwargs

    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        pass

    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to the LLM provider."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get provider name."""
        pass

    async def generate_with_retry(self, prompt: str, **kwargs) -> str:
        """Generate text with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return await self.generate_text(prompt, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    # Exponential backoff
                    wait_time = min(2 ** attempt, 10)
                    await asyncio.sleep(wait_time)
                else:
                    break

        raise last_exception

    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration."""
        return {
            "provider": self.provider_name,
            "model": self.model,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            **self._config
        }


class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMConnectionError(LLMError):
    """Raised when connection to LLM provider fails."""
    pass


class LLMGenerationError(LLMError):
    """Raised when text generation fails."""
    pass


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""
    pass